import json
import os
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
import torch

from pipeline.contracts import constants as C
from pipeline.contracts.hashing import sha256_file
from pipeline.contracts.interfaces import RunConfig
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest
from pipeline.contracts.schemas import TABLE_COLUMNS, CAPTURE_ARRAYS
from pipeline.generate import requests as R
from pipeline.generate import stage as S
from pipeline.generate import storage as ST
from pipeline.generate.backends import MockBackend
from pipeline.generate.capture import MockCapture

import gen_tinylm as T


def _setup(tmp_path, n_problems=3, benchmark="humaneval_plus"):
    layout = RunLayout.for_run("r1", tmp_path)
    probs = [T.problem(f"HumanEval/{i}") for i in range(n_problems)]
    path = layout.problems(benchmark)
    path.parent.mkdir(parents=True)
    path.write_text("\n".join(json.dumps(p.to_dict()) for p in probs) + "\n")
    return layout, probs, Manifest(run_id="r1")


def _cfg(**kw):
    base = dict(run_id="r1", models=("MOCK",), benchmarks=("humaneval_plus",), k=4, backend="mock", device="cpu", shard_size=5)
    base.update(kw)
    return RunConfig(**base)


# ---- storage --------------------------------------------------------------------------------------------
def test_generation_shard_roundtrip_has_exact_columns(tmp_path, prompts):
    probs = [T.problem(f"HumanEval/{i}") for i in range(2)]
    recs = MockBackend(S.mock_mapping(probs), prompts=prompts).generate(R.build_requests("MOCK", probs, 3, prompts=prompts))
    path = tmp_path / "a" / "shard-00000.parquet"
    ST.write_generation_shard(path, recs)
    assert tuple(pq.read_table(path).column_names) == TABLE_COLUMNS["generations"]
    assert ST.read_generation_shard(path) == recs
    assert [p.name for p in path.parent.iterdir()] == ["shard-00000.parquet"]       # no temp file left


def test_seed_survives_parquet_as_uint64(tmp_path, tok):
    r = T.make_record(tok, T.problem(), T.GOOD)
    big = type(r)(**{**r.__dict__, "seed": 2**64 - 1})
    ST.write_generation_shard(tmp_path / "s.parquet", [big])
    assert ST.read_generation_shard(tmp_path / "s.parquet")[0].seed == 2**64 - 1


def test_capture_shard_roundtrip(tmp_path, prompts):
    probs = [T.problem(f"HumanEval/{i}") for i in range(2)]
    mapping = S.mock_mapping(probs)
    recs = MockBackend(mapping, prompts=prompts).generate(R.build_requests("MOCK", probs, 3, prompts=prompts))
    out, arrays = MockCapture(mapping, prompts=prompts).capture(recs, {}, {p.problem_id: p for p in probs})
    sp, ip = tmp_path / "c" / "shard-00000.safetensors", tmp_path / "c" / "index-00000.parquet"
    fixed = ST.write_capture_shard(sp, ip, out, arrays, "c/shard-00000.safetensors")
    assert tuple(pq.read_table(ip).column_names) == TABLE_COLUMNS["capture_index"]
    back = ST.read_capture_index(ip)
    assert [repr(b) for b in back] == [repr(f) for f in fixed] and back[0].hidden.shard_file == "c/shard-00000.safetensors"
    loaded = ST.load_capture_shard(sp)
    assert set(loaded) == set(CAPTURE_ARRAYS)
    np.testing.assert_array_equal(loaded["hs_p2"], arrays["hs_p2"].float().numpy())
    np.testing.assert_array_equal(loaded["yes_no_logodds"], arrays["yes_no_logodds"])
    from safetensors import safe_open
    with safe_open(str(sp), framework="pt") as f:
        assert f.get_tensor("hs_p3").dtype == torch.bfloat16 and f.get_tensor("code_logprob_offsets").dtype == torch.int64


# ---- generation stage -----------------------------------------------------------------------------------
def test_run_generate_writes_shards_and_manifest_and_resumes(tmp_path):
    layout, probs, man = _setup(tmp_path)
    rep = S.run_generate(_cfg(), layout, man)
    shards = sorted((layout.root / "generations/MOCK/humaneval_plus/frozen").glob("shard-*.parquet"))
    assert [s.name for s in shards] == ["shard-00000.parquet", "shard-00001.parquet", "shard-00002.parquet"]
    recs = [r for s in shards for r in ST.read_generation_shard(s)]
    assert len(recs) == 12 and len({r.sample_uid for r in recs}) == 12
    assert not list(layout.root.rglob(".*.tmp"))
    rels = {os.path.relpath(s, layout.root) for s in shards}
    assert rels <= set(man.entries) and rels <= set(rep.outputs)
    for rel in rels:
        e = man.entries[rel]
        assert e.sha256 == sha256_file(layout.root / rel) and e.producer == S.PRODUCER_GEN
    assert Manifest.load(layout.manifest).entries.keys() == man.entries.keys()
    assert rep.metrics["MOCK/humaneval_plus/frozen"]["samples"] == 12 and "tokens_per_second" in rep.metrics["total"]
    assert (layout.root / "config/prompts.json").exists() and "config/prompts.json" in man.entries
    # resume: nothing rewritten
    before = {s.name: (sha256_file(s), s.stat().st_mtime_ns) for s in shards}
    rep2 = S.run_generate(_cfg(), layout, man)
    assert not [o for o in rep2.outputs if o.startswith("generations")] and len(rep2.skipped) == 3
    assert before == {s.name: (sha256_file(s), s.stat().st_mtime_ns) for s in shards}


def test_corrupt_or_unlisted_shard_is_regenerated(tmp_path):
    layout, probs, man = _setup(tmp_path)
    S.run_generate(_cfg(), layout, man)
    d = layout.root / "generations/MOCK/humaneval_plus/frozen"
    good = sha256_file(d / "shard-00001.parquet")
    with open(d / "shard-00001.parquet", "ab") as f:
        f.write(b"x")
    del man.entries[os.path.relpath(d / "shard-00002.parquet", layout.root)]
    rep = S.run_generate(_cfg(), layout, man)
    assert sorted(o for o in rep.outputs if "shard" in o) == [os.path.relpath(d / f"shard-0000{i}.parquet", layout.root) for i in (1, 2)]
    assert len(rep.skipped) == 1 and sha256_file(d / "shard-00001.parquet") == good


def test_changed_config_invalidates_shards(tmp_path):
    layout, probs, man = _setup(tmp_path)
    S.run_generate(_cfg(), layout, man)
    rep = S.run_generate(_cfg(shard_size=4), layout, man)         # different partition: nothing is reused
    assert rep.outputs                                              # shards were rewritten
    d = layout.root / "generations/MOCK/humaneval_plus/frozen"
    recs = [r for s in sorted(d.glob("shard-*.parquet")) for r in ST.read_generation_shard(s)]
    assert len(recs) == 12 and len(sorted(d.glob("shard-*.parquet"))) == 3


def test_k_extension_adds_shards_without_touching_samples_1_to_10(tmp_path):
    layout, probs, man = _setup(tmp_path)
    cfg10 = _cfg(k=10)
    S.run_generate(cfg10, layout, man)
    d = layout.root / "generations/MOCK/humaneval_plus/frozen"
    first = {s.name: sha256_file(s) for s in sorted(d.glob("shard-*.parquet"))}
    assert len(first) == 6                                          # 30 samples / 5
    rep = S.run_generate(_cfg(k=20), layout, man)
    assert len(rep.skipped) == 6 and len(sorted(d.glob("shard-*.parquet"))) == 12
    assert {n: sha256_file(d / n) for n in first} == first
    late = [r for s in sorted(d.glob("shard-*.parquet"))[6:] for r in ST.read_generation_shard(s)]
    assert {r.sample_index for r in late} == set(range(11, 21))
    # explicit sample indices produce the same late shards in a separate run
    layout2, _, man2 = _setup(tmp_path / "b")
    S.run_generate(_cfg(k=10, extra={"sample_indices": list(range(11, 21))}), layout2, man2)
    d2 = layout2.root / "generations/MOCK/humaneval_plus/frozen"
    assert [r.seed for s in sorted(d2.glob("shard-*.parquet")) for r in ST.read_generation_shard(s)] == [r.seed for r in late]


def test_dry_run_writes_nothing(tmp_path):
    layout, probs, man = _setup(tmp_path)
    rep = S.run_generate(_cfg(), layout, man, dry_run=True)
    assert rep.ok and not rep.outputs and any("would write" in n for n in rep.notes)
    assert not (layout.root / "generations").exists() and not man.entries
    S.run_generate(_cfg(), layout, man)
    rc = S.run_capture(_cfg(), layout, man, dry_run=True)
    assert not rc.outputs and any("would write" in n for n in rc.notes) and not (layout.root / "capture").exists()


def test_problem_limit_and_ids(tmp_path):
    layout, probs, man = _setup(tmp_path, n_problems=4)
    S.run_generate(_cfg(problem_limit=2, k=2), layout, man)
    d = layout.root / "generations/MOCK/humaneval_plus/frozen"
    recs = [r for s in sorted(d.glob("shard-*.parquet")) for r in ST.read_generation_shard(s)]
    assert {r.problem_id for r in recs} == {"HumanEval/0", "HumanEval/1"}
    layout2, _, man2 = _setup(tmp_path / "z", n_problems=4)
    S.run_generate(_cfg(problem_ids=("HumanEval/3",), k=1), layout2, man2)
    d = layout2.root / "generations/MOCK/humaneval_plus/frozen"
    assert {r.problem_id for s in d.glob("shard-*.parquet") for r in ST.read_generation_shard(s)} == {"HumanEval/3"}


def test_fresh_pass_with_adapter_uses_separate_set_and_seeds(tmp_path):
    layout, probs, man = _setup(tmp_path)
    extra = {"fresh": [{"model_key": "MOCK", "benchmark": "humaneval_plus", "adapter_id": "f0s1", "adapter_path": "/x", "k_g": 2}]}
    S.run_generate(_cfg(k=2, extra=extra), layout, man)
    base = layout.root / "generations/MOCK/humaneval_plus"
    frozen = [r for s in sorted((base / "frozen").glob("*.parquet")) for r in ST.read_generation_shard(s)]
    fresh = [r for s in sorted((base / "fresh_f0s1").glob("*.parquet")) for r in ST.read_generation_shard(s)]
    assert layout.generation_shard("MOCK", "humaneval_plus", "fresh:f0s1", 0).parent == base / "fresh_f0s1"
    assert len(fresh) == 6 and {r.generation_set for r in fresh} == {"fresh:f0s1"}
    assert {r.seed for r in fresh}.isdisjoint({r.seed for r in frozen})
    assert all(r.sample_uid.startswith("MOCK|fresh:f0s1|") for r in fresh)


# ---- capture stage --------------------------------------------------------------------------------------
def test_run_capture_mock_with_extractions_resume_and_skips(tmp_path):
    layout, probs, man = _setup(tmp_path)
    cfg = _cfg(k=3, shard_size=5)
    S.run_generate(cfg, layout, man)
    gdir = layout.root / "generations/MOCK/humaneval_plus/frozen"
    recs = [r for s in sorted(gdir.glob("shard-*.parquet")) for r in ST.read_generation_shard(s)]
    # extraction table: mark the first sample as an extraction failure
    epath = layout.extractions("MOCK", "humaneval_plus", "frozen")
    epath.parent.mkdir(parents=True)
    rows = [{"sample_uid": recs[0].sample_uid, "code": None, "method": None, "failure": "no_block"}]
    pq.write_table(pa.Table.from_pylist(rows, schema=pa.schema([("sample_uid", pa.string()), ("code", pa.string()),
                                                                 ("method", pa.string()), ("failure", pa.string())])), epath)
    rep = S.run_capture(cfg, layout, man)
    sh = sorted((layout.root / "capture/MOCK/humaneval_plus/frozen").glob("shard-*.safetensors"))
    ix = sorted((layout.root / "capture/MOCK/humaneval_plus/frozen").glob("index-*.parquet"))
    assert len(sh) == len(ix) == 2
    for p in sh + ix:
        assert os.path.relpath(p, layout.root) in man.entries
    index = ST.read_capture_index(ix[0])
    assert index[0].sample_uid == recs[0].sample_uid and index[0].n_code_tokens == 0          # extraction table used
    assert index[0].hidden.shard_file == os.path.relpath(sh[0], layout.root)
    assert sum(len(ST.read_capture_index(i)) for i in ix) == 9
    assert rep.metrics["MOCK/humaneval_plus/frozen"]["samples"] == 9 and "tokens_per_second" in rep.metrics["MOCK/humaneval_plus/frozen"]
    rep2 = S.run_capture(cfg, layout, man)
    assert not rep2.outputs and len(rep2.skipped) == 2
    # a new extraction table changes the capture config hash and invalidates the shards
    pq.write_table(pa.Table.from_pylist([], schema=pa.schema([("sample_uid", pa.string()), ("code", pa.string()),
                                                               ("method", pa.string()), ("failure", pa.string())])), epath)
    assert len(S.run_capture(cfg, layout, man).skipped) == 0
    # generation-only models are skipped
    rep3 = S.run_capture(_cfg(k=3, generation_only_models=("MOCK",)), layout, man)
    assert not rep3.outputs and any("generation only" in n for n in rep3.notes)


def test_base_models_skip_lcb(tmp_path):
    layout, probs, man = _setup(tmp_path)
    rep = S.run_generate(_cfg(models=("B1",), benchmarks=("humaneval_plus", "lcb_v6"), k=1), layout, man)
    assert any("lcb_v6 skipped" in n for n in rep.notes)
    d = layout.root / "generations/B1/humaneval_plus/frozen"
    recs = [r for s in d.glob("*.parquet") for r in ST.read_generation_shard(s)]
    assert len(recs) == 3 and all(r.model_key == "B1" for r in recs)


# ---- transformers path through the stage (tiny random model in place of a download) ----------------------
def test_transformers_backend_through_the_stage(tmp_path, monkeypatch, model, tok):
    layout, probs, man = _setup(tmp_path, n_problems=2)
    monkeypatch.setattr(S, "load_hf", lambda cfg, spec: (model, tok))
    monkeypatch.setattr(R, "max_new_tokens_for", lambda thinking: 6)
    cfg = _cfg(models=("SMOKE",), backend="transformers", k=2, shard_size=3)
    rep = S.run_generate(cfg, layout, man)
    assert rep.metrics["SMOKE/humaneval_plus/frozen"]["samples"] == 4
    assert rep.metrics["SMOKE/humaneval_plus/frozen"]["tokens_per_second"] > 0
    cfgfile = json.loads((layout.root / "config/prompts.json").read_text())
    assert cfgfile["model:SMOKE"]["chat_template_sha256"] and cfgfile["_prompts"]["format"] == "calib-disconnect/prompts/v1"
    rc = S.run_capture(cfg, layout, man)
    assert rc.metrics["SMOKE/humaneval_plus/frozen"]["samples"] == 4
    at = json.loads((layout.root / "config/answer_tokens.json").read_text())["SMOKE"]
    assert {d["token"] for d in at["yes"]} == {" Yes", "Yes"}
    ms = json.loads((layout.root / "config/mask_spans.json").read_text())["SMOKE"]
    assert ms["first_span_token"] == "<|im_start|>" and ms["elicitation_n_tokens"]["V2"] > 5
    for rel in ("config/answer_tokens.json", "config/mask_spans.json"):
        assert rel in man.entries
    ix = sorted((layout.root / "capture/SMOKE/humaneval_plus/frozen").glob("index-*.parquet"))
    idx = [c for i in ix for c in ST.read_capture_index(i)]
    assert len(idx) == 4 and all(c.p3 == c.elicitation_span[1] - 1 for c in idx)
    arr = ST.load_capture_shard(sorted((layout.root / "capture/SMOKE/humaneval_plus/frozen").glob("shard-*.safetensors"))[0])
    assert arr["hs_p3"].shape[1:] == (7, 64) and np.isfinite(arr["hs_p3"]).all()
