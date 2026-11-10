"""Stage run on a small subset in a temporary run root."""

from __future__ import annotations

import json

import pytest

from data_helpers import needs_cache
from pipeline.contracts import hashing
from pipeline.contracts.interfaces import RunConfig
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest
from pipeline.contracts.schemas import FoldPlan, Problem, TestSuite
from pipeline.data import stage
from pipeline.data.inputs import canonical_repr


def _cfg(**kw):
    d = dict(run_id="t", models=("MOCK",), benchmarks=("humaneval_plus", "mbpp_plus"), problem_limit=5, fold_seeds=(0, 1))
    d.update(kw)
    return RunConfig(**d)


@pytest.fixture(scope="module")
def run_root(tmp_path_factory):
    root = tmp_path_factory.mktemp("runs")
    cfg = _cfg()
    layout = RunLayout.for_run("t", root)
    manifest = Manifest(run_id="t")
    from data_helpers import _cache_present

    if not _cache_present():
        pytest.skip("bench-A2 cache is absent")
    report = stage.run(cfg, layout, manifest)
    return cfg, layout, manifest, report


def test_entry_point_is_registered():
    from pipeline.contracts.interfaces import STAGES
    import importlib

    mod, fn = STAGES["data"].split(":")
    assert getattr(importlib.import_module(mod), fn) is stage.run


@needs_cache
def test_stage_outputs_and_manifest(run_root):
    cfg, layout, manifest, report = run_root
    assert report.ok and report.stage == "data"
    want = {"data/problems_humaneval_plus.jsonl", "data/suites_humaneval_plus.jsonl", "data/problems_mbpp_plus.jsonl",
            "data/suites_mbpp_plus.jsonl", "data/near_duplicates.json", "data/folds_label_validity_seed0.json",
            "data/folds_label_validity_seed1.json", "data/agreement_inputs_stats.json"}
    assert set(report.outputs) == want == set(manifest.entries)
    for rel in want:
        assert (layout.root / rel).is_file()
    assert manifest.verify(layout.root, require_present=True).passed
    assert manifest.unlisted(layout.root) == []
    e = manifest.entries["data/problems_mbpp_plus.jsonl"]
    assert e.producer == "pipeline.data.stage:run" and e.config_hash == hashing.config_hash(cfg.to_dict())
    assert e.sha256 == hashing.sha256_file(layout.problems("mbpp_plus"))


@needs_cache
def test_stage_problem_selection_is_first_n_sorted(run_root):
    _, layout, _, _ = run_root
    he = [Problem.from_dict(json.loads(x)) for x in layout.problems("humaneval_plus").read_text().splitlines()]
    mb = [Problem.from_dict(json.loads(x)) for x in layout.problems("mbpp_plus").read_text().splitlines()]
    all_he = sorted(f"HumanEval/{i}" for i in range(164))
    assert [p.problem_id for p in he] == all_he[:5] == ["HumanEval/0", "HumanEval/1", "HumanEval/10", "HumanEval/100", "HumanEval/101"]
    assert len(mb) == 5 and [p.problem_id for p in mb] == sorted(p.problem_id for p in mb)


@needs_cache
def test_stage_suites_include_agree_and_roundtrip(run_root):
    _, layout, _, report = run_root
    rows = [TestSuite.from_dict(json.loads(x)) for x in layout.suites("humaneval_plus").read_text().splitlines()]
    assert len(rows) == 15 and report.metrics["humaneval_plus_suites"] == 15
    by = {}
    for s in rows:
        by.setdefault(s.problem_id, {})[s.suite_id] = s
    assert all(set(v) == {"O", "E", "agree"} for v in by.values())
    for v in by.values():
        assert len(v["agree"].inputs) <= 50 and v["agree"].expected is None
        assert not {canonical_repr(x) for x in v["agree"].inputs} & {canonical_repr(x) for x in v["E"].inputs}


@needs_cache
def test_stage_folds_and_near_duplicates(run_root):
    cfg, layout, _, _ = run_root
    plan = FoldPlan.from_dict(json.loads(layout.folds("label_validity", 1).read_text()))
    assert plan.fold_seed == 1 and plan.population == "label_validity" and len(plan.assignment) == 10
    key_of = {m: g.group_key for g in plan.groups for m in g.members}
    for pid, fold in plan.assignment.items():
        assert fold == hashing.fold_of(1, key_of.get(pid, pid))
    nd = json.loads(layout.near_duplicates.read_text())
    assert nd["n_groups"] == len(nd["groups"]) and nd["diagnostics"]["n_problems_considered"] == 542
    stats = json.loads(stage.stats_path(layout).read_text())
    s = stats["per_benchmark"]["humaneval_plus"]["HumanEval/0"]
    assert set(s) >= {"generated", "removed_label_duplicates", "kept", "status"}
    assert stats["provenance"]["mbpp_plus_patch_file_sha256"].startswith("3d7579ae")
    assert stats["provenance"]["mbpp_plus_patched_ids"] == ["Mbpp/102", "Mbpp/459", "Mbpp/559"]


@needs_cache
def test_stage_is_deterministic_in_content(run_root, tmp_path):
    cfg, layout, _, _ = run_root
    layout2 = RunLayout.for_run("t", tmp_path)
    m2 = Manifest(run_id="t")
    stage.run(cfg, layout2, m2)
    for rel in ("data/problems_humaneval_plus.jsonl", "data/suites_humaneval_plus.jsonl", "data/suites_mbpp_plus.jsonl",
                "data/folds_label_validity_seed0.json", "data/near_duplicates.json", "data/agreement_inputs_stats.json"):
        assert (layout.root / rel).read_bytes() == (layout2.root / rel).read_bytes(), rel


@needs_cache
def test_problem_ids_then_limit(tmp_path):
    cfg = _cfg(benchmarks=("mbpp_plus",), problem_ids=("Mbpp/459", "Mbpp/2", "Mbpp/3", "Mbpp/4"), problem_limit=3, fold_seeds=(0,))
    layout = RunLayout.for_run("t", tmp_path)
    m = Manifest(run_id="t")
    r = stage.run(cfg, layout, m)
    ids = [json.loads(x)["problem_id"] for x in layout.problems("mbpp_plus").read_text().splitlines()]
    assert ids == ["Mbpp/2", "Mbpp/3", "Mbpp/4"]
    assert r.metrics["mbpp_plus_problems"] == 3
    patched = _cfg(benchmarks=("mbpp_plus",), problem_ids=("Mbpp/459",), fold_seeds=(0,), problem_limit=None)
    stage.run(patched, RunLayout.for_run("p", tmp_path), Manifest(run_id="p"))
    row = json.loads(RunLayout.for_run("p", tmp_path).problems("mbpp_plus").read_text())
    assert row["patched"] is True
    with pytest.raises(stage.DataStageError):
        stage.run(_cfg(problem_ids=("Mbpp/99999",)), RunLayout.for_run("q", tmp_path), Manifest(run_id="q"))


def test_dry_run_writes_nothing(tmp_path):
    layout = RunLayout.for_run("t", tmp_path)
    m = Manifest(run_id="t")
    r = stage.run(_cfg(), layout, m, dry_run=True)
    assert r.ok and len(r.outputs) == 8 and "data/near_duplicates.json" in r.outputs
    assert not layout.root.exists() and m.entries == {}


def test_lcb_without_shards_raises_with_fetch_command(tmp_path):
    cfg = _cfg(benchmarks=("lcb_v6",), bench_cache=str(tmp_path / "empty_cache"))
    layout = RunLayout.for_run("t", tmp_path)
    with pytest.raises(stage.DataStageError, match="pipeline.data fetch --benchmark lcb_v6"):
        stage.run(cfg, layout, Manifest(run_id="t"))
    r = stage.run(cfg, layout, Manifest(run_id="t"), dry_run=True)  # a dry run only notes it
    assert r.ok and any("shards missing" in n for n in r.notes)
    assert "data/folds_lcb_seed0.json" in r.outputs


def test_unknown_benchmark_rejected(tmp_path):
    with pytest.raises(stage.DataStageError):
        stage.run(_cfg(benchmarks=("nope",)), RunLayout.for_run("t", tmp_path), Manifest(run_id="t"))
