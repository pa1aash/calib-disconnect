"""N1 population-coverage guard, N3 fresh-only jobs, G10 timing probe."""

import hashlib
import json
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from pipeline.contracts.interfaces import RunConfig, ReadoutData
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest
from pipeline.readouts import files, stage, timing
from pipeline.readouts.masked_lora import synthetic_layouts
from pipeline.readouts.real_backend import RealBackend
from readouts_helpers import VOCAB, build_tiny, make_data, make_plan
from test_readouts_conformance import GS, cfg_for, write_reference_checks
from test_readouts_stage import build_run

pytestmark = pytest.mark.filterwarnings("ignore")


def small(n=15, k=3, seed=0):
    return make_data(n_problems=n, k=k, seed=seed)


# ---------------------------------------------------------------------------------------------------
# N1
# ---------------------------------------------------------------------------------------------------
def test_labeled_problem_missing_from_the_fold_plan_raises(tmp_path):
    d, layout = build_run(tmp_path, seeds=(0,), d=small())
    p = layout.folds("label_validity", 0)
    plan = json.loads(p.read_text())
    gone = sorted(set(d.problem_ids))[:3]
    for g in gone:
        del plan["assignment"][g]
    p.write_text(json.dumps(plan))
    with pytest.raises(stage.PopulationCoverageError, match=r"fold plan of seed 0.*humaneval_plus: 3 of 15"):
        stage.run(cfg_for(["MOCK"], ["SZ_V2"]), layout, Manifest(run_id="t"))
    assert not layout.root.joinpath("readouts").exists()       # nothing was written


def test_labeled_problem_missing_from_the_reference_checks_raises(tmp_path):
    d, layout = build_run(tmp_path, seeds=(0,), d=small())
    probs = sorted(set(d.problem_ids))
    write_reference_checks(layout, probs[:-2], set())
    with pytest.raises(stage.PopulationCoverageError, match=r"reference_checks.*humaneval_plus: 2 of 15"):
        stage.run(cfg_for(["MOCK"], ["SZ_V2"]), layout, Manifest(run_id="t"))


def test_complete_coverage_and_unlabeled_problems_pass(tmp_path):
    d = small()
    unlabeled = d.problem_ids[0]
    for s in d.labels:
        d.labels[s] = np.where(np.array(d.problem_ids) == unlabeled, -1, d.labels[s]).astype(np.int8)
    d, layout = build_run(tmp_path, seeds=(0,), d=d)
    plan = json.loads(layout.folds("label_validity", 0).read_text())
    del plan["assignment"][unlabeled]                 # a problem without any label need not be in the plan
    layout.folds("label_validity", 0).write_text(json.dumps(plan))
    write_reference_checks(layout, sorted(set(d.problem_ids) - {unlabeled}), set())
    assert stage.run(cfg_for(["MOCK"], ["SZ_V2"]), layout, Manifest(run_id="t")).ok


# ---------------------------------------------------------------------------------------------------
# N3
# ---------------------------------------------------------------------------------------------------
def snapshot(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file() and p.name != "MANIFEST.json"}


def test_fresh_job_leaves_frozen_files_byte_identical(tmp_path):
    d, layout = build_run(tmp_path, seeds=(0,), d=small())
    cfg = cfg_for(["MOCK"], ["P", "SR"], lora_max_steps=2)
    man = Manifest(run_id="t")
    stage.run(cfg, layout, man)
    build_run(tmp_path, d=make_data(n_problems=4, k=3, seed=11), layout=layout, gen_set=GS, plans=False)
    before = snapshot(layout.root)
    fresh_cfg = cfg_for(["MOCK"], ["P", "SR"], lora_max_steps=2, extra={"gen_set": GS})
    rep = stage.run(fresh_cfg, layout, man)
    assert rep.ok, rep.notes
    after = snapshot(layout.root)
    assert all(after[k] == v for k, v in before.items())            # every pre-existing file is byte-identical
    new = set(after) - set(before)
    assert len(new) == 2 and all("fresh_SR_E_seed0_fold2" in k for k in new)
    assert {Path(o).name for o in rep.outputs} == {"seed0.parquet"} and all("fresh_SR" in o for o in rep.outputs)
    # a fresh job does not need the frozen capture at all
    assert not any("frozen" in o for o in rep.outputs)


def test_fresh_job_dry_run_plans_only_fresh_paths(tmp_path):
    layout = RunLayout.for_run("t", tmp_path)
    rep = stage.run(cfg_for(["MOCK"], ["SR"], extra={"gen_set": GS}), layout, Manifest(run_id="t"), dry_run=True)
    assert rep.ok and not layout.root.exists()


# ---------------------------------------------------------------------------------------------------
# G10
# ---------------------------------------------------------------------------------------------------
def test_time_lora_steps_on_a_tiny_model():
    model = build_tiny("qwen3")
    be = RealBackend(model, synthetic_layouts(VOCAB, n=8, seed=2), [1], [2])
    res = timing.time_lora_steps(be, 3)
    assert res["steps"] == 3 and res["n_samples"] == 8 and res["seconds_per_step"] > 0 and res["peak_memory_bytes"] > 0
    assert not any("lora" in n for n, _ in model.named_parameters())      # the adapter was unwrapped, nothing kept


def test_timing_only_stage_writes_no_scores_and_ignores_generation_only(tmp_path, monkeypatch):
    layout = RunLayout.for_run("t", tmp_path)
    g = layout.generation_shard("P4", "humaneval_plus", "timing", 0)
    g.parent.mkdir(parents=True)
    pq.write_table(pa.Table.from_pylist([dict(sample_uid=f"P4|timing|humaneval_plus|HumanEval/{i}|1") for i in range(8)]), g)
    tiny = RealBackend(build_tiny("qwen3"), synthetic_layouts(VOCAB, n=8, seed=3), [1], [2])
    monkeypatch.setattr(RealBackend, "from_pretrained", classmethod(lambda cls, *a, **k: tiny))
    cfg = RunConfig(run_id="t", models=("P4",), benchmarks=("humaneval_plus",), backend="transformers", device="cpu",
                    generation_only_models=("P4",), lora_max_steps=3, extra={"timing_only": True})
    man = Manifest(run_id="t")
    rep = stage.run(cfg, layout, man)
    assert rep.ok and not rep.skipped
    t = rep.metrics["timing"]["P4/label_validity"]
    assert t["steps"] == 3 and t["seconds_per_step"] > 0 and t["peak_memory_bytes"] > 0
    log = json.loads((layout.logs / "timing_readouts_P4.json").read_text())
    assert log["seconds_per_step"] == t["seconds_per_step"]
    assert not (layout.root / "readouts").exists() and not (layout.root / "adapters").exists() and not man.entries


def test_timing_only_with_the_mock_backend_times_nothing(tmp_path):
    layout = RunLayout.for_run("t", tmp_path)
    g = layout.generation_shard("MOCK", "humaneval_plus", "timing", 0)
    g.parent.mkdir(parents=True)
    pq.write_table(pa.Table.from_pylist([dict(sample_uid="MOCK|timing|humaneval_plus|HumanEval/0|1")]), g)
    rep = stage.run(cfg_for(["MOCK"], [], extra={"timing_only": True}), layout, Manifest(run_id="t"))
    assert rep.ok and any("mock" in n for n in rep.notes) and "timing" not in rep.metrics
