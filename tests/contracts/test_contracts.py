"""Tests for pipeline.contracts (hand-checked encodings, round trips, frozen values)."""

import hashlib
import json
from pathlib import Path

import pytest

from pipeline.contracts import constants as C
from pipeline.contracts import hashing as H
from pipeline.contracts.interfaces import RunConfig, TeacherForcedLayout
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest
from pipeline.contracts.schemas import FoldPlan, GenerationRecord, NearDuplicateGroup, sample_uid

ROOT = Path(__file__).resolve().parents[2]


def test_frozen_design_hash_matches_record():
    want = (ROOT / C.DESIGN_SHA256_PATH).read_text().split()[0]
    have = hashlib.sha256((ROOT / C.DESIGN_PATH).read_bytes()).hexdigest()
    assert want == have


def test_design_values():
    assert C.DELTA == 0.03 and C.T10 == 185 and C.T20 == 125 and C.T12_QUANTILE == 1.782
    assert C.K_DEFAULT == 10 and C.K_EXPANDED == 20 and C.B_BOOTSTRAP == 10_000
    assert len(C.MBPP_PLUS_REMOVED_IDS) == 21 and C.PRIMARY_MODELS == ("P1", "P2", "P3", "P4", "P5", "P6")
    assert abs(C.SHAPLEY_SIMULTANEOUS_LEVEL - 0.9875) < 1e-12


def test_sample_seed_hand_computed():
    d = hashlib.sha256("m\x1fr\x1fb\x1fp\x1f1".encode()).digest()
    assert H.sample_seed("m", "r", "b", "p", 1) == int.from_bytes(d[:8], "big")
    with pytest.raises(ValueError):
        H.sample_seed("m", "r", "b", "p", 0)


def test_fold_of_hand_computed_and_range():
    d = hashlib.sha256("0\x1fHumanEval/0".encode()).digest()
    assert H.fold_of(0, "HumanEval/0") == int.from_bytes(d, "big") % 5
    assert {H.fold_of(1, f"Mbpp/{i}") for i in range(200)} == set(range(5))


def test_lcb_agreement_split_counts():
    for n, want in [(0, 0), (1, 0), (2, 0), (3, 1), (4, 1), (5, 1), (10, 2), (20, 4)]:
        idx = H.lcb_agreement_indices([f"in{i}" for i in range(n)])
        assert len(idx) == want and idx == sorted(idx)
    assert H.lcb_agreement_indices(["a", "b", "c", "d", "e"]) == H.lcb_agreement_indices(["a", "b", "c", "d", "e"])


def test_exec_cache_key_changes_with_every_field():
    base = ("code", "HumanEval/0", "E", "evalplus==0.3.1", "rule", 2**31, "abc")
    k0 = H.exec_cache_key(*base)
    for i in range(len(base)):
        alt = list(base)
        alt[i] = str(alt[i]) + "x" if not isinstance(alt[i], int) else alt[i] + 1
        assert H.exec_cache_key(*alt) != k0


def test_prompt_files_match_hashes_and_verbatim_text():
    pdir = ROOT / "pipeline" / "prompts"
    rec = json.loads((pdir / "PROMPTS.sha256.json").read_text())["files"]
    for name, sha in rec.items():
        assert hashlib.sha256((pdir / name).read_bytes()).hexdigest() == sha, name
    assert (pdir / "elicit_v1.txt").read_text() == C.V1_TEXT
    assert (pdir / "elicit_v2.txt").read_text() == C.V2_TEXT


def test_foldplan_inner_splits():
    assign = {f"p{i}": i % 5 for i in range(10)}
    plan = FoldPlan(fold_seed=0, population="label_validity", n_folds=5, assignment=assign,
                    groups=(NearDuplicateGroup("p0", ("p0", "p5"), ("ast_identical",)),))
    splits = plan.inner_splits(2)
    assert len(splits) == 4
    assert splits[0][1] == ["p0", "p5"]  # first inner split validates on the lowest training fold
    for tr, va in splits:
        assert not set(tr) & set(va) and not set(va) & set(plan.outer_test(2))
    assert FoldPlan.from_dict(json.loads(json.dumps(plan.to_dict()))) == plan


def test_teacher_forced_layout():
    lay = TeacherForcedLayout(prompt_ids=(1, 2, 3), completion_ids=(4, 5), elicitation_ids=(6, 7, 8), code_span=(3, 4))
    assert lay.p1 == 2 and lay.elicitation_span == (5, 8) and lay.p3 == 7
    assert lay.mask().tolist() == [0, 0, 0, 0, 0, 1, 1, 1]


def test_record_round_trip():
    r = GenerationRecord(sample_uid=sample_uid("MOCK", "humaneval_plus", "HumanEval/0", 1), model_key="MOCK",
                         model_id="m", revision="r", benchmark="humaneval_plus", problem_id="HumanEval/0",
                         sample_index=1, generation_set="frozen", seed=1, prompt_sha256="a",
                         rendered_prompt_sha256="b", completion_text="x", completion_token_ids=(1, 2),
                         finish_reason="stop", truncated=False, engine="mock", thinking=False)
    assert GenerationRecord.from_dict(json.loads(json.dumps(r.to_dict()))) == r
    cfg = RunConfig(run_id="t", models=("MOCK",), benchmarks=("humaneval_plus",))
    assert RunConfig.from_dict(json.loads(json.dumps(cfg.to_dict()))) == cfg


def test_manifest_add_verify_and_completeness(tmp_path):
    lay = RunLayout.for_run("r1", runs_root=tmp_path)
    f = lay.root / "data" / "x.txt"
    f.parent.mkdir(parents=True)
    f.write_text("hello")
    m = Manifest(run_id="r1")
    m.add(lay.root, f, producer="test", config_hash="c", git="g")
    m.save(lay.manifest)
    m2 = Manifest.load(lay.manifest)
    assert m2.verify(lay.root).passed and m2.unlisted(lay.root) == []
    f.write_text("changed")
    assert not m2.verify(lay.root).passed
    (lay.root / "data" / "y.txt").write_text("unlisted")
    assert m2.unlisted(lay.root) == ["data/y.txt"]
