"""Wave 8, step C1: end-to-end integration test on synthetic data.

A mock backend with deterministic outputs (correct reference solutions and hand-written mutations of
them, never model output) flows through every stage: data, generation, execution on fixtures, labels,
capture, readouts, metrics, bootstrap, Shapley, and decisions. Asserted invariants: every stage
succeeds; Shapley efficiency; fold integrity (every out-of-fold score sits in its problem's fold, and
near-duplicate groups share a fold); no problem leakage across folds; the manifest lists every file
with a matching hash; and pilot sealing keeps Gamma cells out of the open results.
"""

from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from pipeline.contracts.interfaces import STAGES, RunConfig
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest
from pipeline.contracts.schemas import FoldPlan

pytestmark = pytest.mark.slow

N_PROBLEMS = 8
K = 4


def _cfg(tmp: Path, **kw) -> RunConfig:
    base = dict(run_id="it", models=("MOCK",), benchmarks=("humaneval_plus",), k=K, fold_seeds=(0, 1, 2),
                backend="mock", device="cpu", sandbox="trusted-only", execute_untrusted=False,
                problem_limit=N_PROBLEMS,
                extra={"mock_fixtures_trusted": True, "mock_p_correct": 0.5, "bootstrap_b": 60,
                       "analysis_root": str(tmp / "analysis")})
    base.update(kw)
    return RunConfig(**base)


def _run(cfg: RunConfig, layout: RunLayout, manifest: Manifest, stages):
    reports = {}
    for st in stages:
        mod, fn = STAGES[st].split(":")
        rep = getattr(importlib.import_module(mod), fn)(cfg, layout, manifest)
        manifest.save(layout.manifest)
        reports[st] = rep
    return reports


@pytest.fixture(scope="module")
def run(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("c1")
    cfg = _cfg(tmp)
    layout = RunLayout.for_run(cfg.run_id, runs_root=tmp / "runs")
    manifest = Manifest(run_id=cfg.run_id)
    reports = _run(cfg, layout, manifest, ["data", "generate", "execute", "capture", "readouts", "analysis"])
    return tmp, cfg, layout, manifest, reports


def test_every_stage_succeeds(run):
    *_, reports = run
    for st, rep in reports.items():
        assert rep.ok, (st, rep.notes)


def test_labels_cover_every_sample_under_both_suites(run):
    _, _, layout, _, _ = run
    d = pd.read_parquet(layout.labels("MOCK", "humaneval_plus", "frozen"))
    assert set(d.suite_id) == {"O", "E"}
    assert len(d) == 2 * N_PROBLEMS * K
    assert 0 < d.y.mean() < 1  # both classes present, so the readouts have something to rank


def _budgets(tmp: Path) -> dict:
    return json.loads((tmp / "analysis" / "results" / "it" / "budgets.json").read_text())["budgets"]


def test_shapley_efficiency(run):
    tmp, *_ = run
    for key, b in _budgets(tmp).items():
        for chain in ("discrimination", "discrimination_v2_chain"):
            sh = b[chain]["shapley"]
            total = sh["g0"] + sum(sh["phi"].values())
            assert abs(total - sh["residual"]) < 1e-12, (key, chain)
            assert abs(sh["efficiency_gap"]) < 1e-12
            assert sh["cells"]["0000"] == sh["g0"] and sh["cells"]["1111"] == sh["residual"]


def _plan(layout: RunLayout, seed: int) -> FoldPlan:
    return FoldPlan.from_dict(json.loads(layout.folds("label_validity", seed).read_text()))


def test_fold_integrity_and_no_leakage(run):
    _, cfg, layout, _, _ = run
    plans = {s: _plan(layout, s) for s in cfg.fold_seeds}
    for s, plan in plans.items():
        for g in plan.groups:  # near-duplicate groups share a fold under every seed
            assert len({plan.assignment[m] for m in g.members}) == 1
        for f in range(plan.n_folds):  # outer train and test are disjoint, inner splits never see test
            test = set(plan.outer_test(f))
            assert not test & set(plan.outer_train(f))
            for tr, va in plan.inner_splits(f):
                assert not test & (set(tr) | set(va))
    files = sorted((layout.root / "readouts").rglob("*.parquet"))
    assert files
    checked = 0
    for fp in files:
        d = pd.read_parquet(fp)
        d = d[d.fold.notna() & d.fold_seed.notna()]
        for uid, seed, fold in zip(d.sample_uid, d.fold_seed, d.fold):
            pid = uid.split("|")[3]
            assert plans[int(seed)].assignment[pid] == int(fold), (fp.name, uid)
            checked += 1
    assert checked > 0


def test_manifest_complete_and_verified(run):
    _, _, layout, manifest, _ = run
    m = Manifest.load(layout.manifest)
    rep = m.verify(layout.root)
    assert rep.passed and not rep.missing, (rep.mismatched, rep.missing)
    assert m.unlisted(layout.root) == []


def test_sealed_pilot_mode(run):
    tmp, cfg, layout, manifest, _ = run
    sealed_cfg = _cfg(tmp, run_id="it", seal_gamma=True,
                      extra={**cfg.extra, "analysis_root": str(tmp / "analysis_sealed")})
    rep = _run(sealed_cfg, layout, manifest, ["analysis"])["analysis"]
    assert rep.ok
    sealed = layout.sealed / "gamma_sealed.json"
    digest = (layout.sealed / "gamma_sealed.sha256").read_text().split()[0]
    assert hashlib.sha256(sealed.read_bytes()).hexdigest() == digest
    assert "sealed/gamma_sealed.json" in Manifest.load(layout.manifest).entries
    open_dir = tmp / "analysis_sealed" / "results" / "it"
    for f in open_dir.glob("*.json"):  # no Gamma cell, Shapley term, or residual in the open results
        text = f.read_text()
        assert '"shapley"' not in text and '"cells"' not in text, f.name
    assert "shapley" not in json.dumps(rep.metrics)
