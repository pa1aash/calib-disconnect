"""Stage run on mock-shaped inputs in a temporary run root (backend "mock": surrogate trainer)."""

import json

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
import torch
from safetensors.torch import save_file

from pipeline.contracts.interfaces import STAGES, RunConfig
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest
from pipeline.contracts.schemas import TABLE_COLUMNS
from pipeline.readouts import stage
from readouts_helpers import make_data, make_plan

pytestmark = pytest.mark.filterwarnings("ignore")


def build_run(tmp_path, seeds=(0, 1), model="MOCK", gen_set="frozen", d=None, layout=None, plans=True):
    d = d if d is not None else make_data(n_problems=30, k=4)
    layout = layout or RunLayout.for_run("t", tmp_path)
    root = layout.root
    n = len(d.sample_uids)
    shard = layout.capture_shard(model, "humaneval_plus", gen_set, 0)
    shard.parent.mkdir(parents=True, exist_ok=True)
    offs = np.concatenate([[0], np.cumsum([len(x) for x in d.code_logprobs])]).astype(np.int64)
    arrays = {k: torch.tensor(v).to(torch.bfloat16) for k, v in d.hidden.items()}
    arrays["code_logprobs"] = torch.tensor(np.concatenate(d.code_logprobs))
    arrays["code_logprob_offsets"] = torch.tensor(offs)
    arrays["yes_no_logodds"] = torch.tensor([c.yes_no_logodds for c in d.capture], dtype=torch.float32)
    save_file(arrays, str(shard))
    rows = []
    for i, c in enumerate(d.capture):
        rows.append(dict(sample_uid=c.sample_uid, shard_file=str(shard.relative_to(root)), row=i, layers=list(c.hidden.layers),
                         n_code_tokens=c.n_code_tokens, code_token_span=list(c.code_token_span), p1=c.p1, p2=c.p2, p3=c.p3,
                         elicitation_span=list(c.elicitation_span), yes_no_logodds=c.yes_no_logodds, v1_text=c.v1_text,
                         v1_value=c.v1_value, sum_logprob=c.sum_logprob, mean_logprob=c.mean_logprob, min_logprob=c.min_logprob))
    pq.write_table(pa.Table.from_pylist(rows), layout.capture_index(model, "humaneval_plus", gen_set, 0))
    lab = layout.labels(model, "humaneval_plus", gen_set)
    lab.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.Table.from_pylist([dict(sample_uid=u, suite_id=s, y=int(d.labels[s][i]), source="execution", failure=None, cache_key=None)
                                         for i, u in enumerate(d.sample_uids) for s in ("O", "E")]), lab)
    ext = layout.extractions(model, "humaneval_plus", gen_set)
    ext.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.Table.from_pylist([dict(sample_uid=u, code=d.code_texts[i], method="fenced", failure=None)
                                         for i, u in enumerate(d.sample_uids)]), ext)
    ag = layout.agreement_outputs(model, "humaneval_plus", gen_set)
    ag.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.Table.from_pylist([dict(sample_uid=u, signature=None if d.agreement_outputs[u] is None else json.dumps(list(d.agreement_outputs[u]))) for u in d.sample_uids]), ag)
    for s in (seeds if plans else ()):
        p = layout.folds("label_validity", s)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(make_plan(set(d.problem_ids), seed=s).to_dict()))
    return d, layout


def test_stage_is_registered():
    assert STAGES["readouts"] == "pipeline.readouts.stage:run"


def test_stage_dry_run_writes_nothing(tmp_path):
    layout = RunLayout.for_run("t", tmp_path)
    cfg = RunConfig(run_id="t", models=("MOCK", "P1"), benchmarks=("humaneval_plus", "mbpp_plus"), backend="mock",
                    generation_only_models=("P1",), readouts=("P", "SZ_V2"))
    rep = stage.run(cfg, layout, Manifest(run_id="t"), dry_run=True)
    assert rep.ok and rep.metrics["planned"] and not layout.root.exists() and rep.skipped


def test_stage_mock_run(tmp_path):
    d, layout = build_run(tmp_path)
    cfg = RunConfig(run_id="t", models=("MOCK",), benchmarks=("humaneval_plus",), backend="mock", device="cpu",
                    fold_seeds=(0, 1), readouts=("P", "P2", "SZ_V1", "SZ_V1_drop", "SZ_V2", "TL_geo", "AGREE", "AGREE_problem", "AST",
                                                 "PROMPT", "CODETEXT", "LAT", "ST", "ST_r1", "ST_r4", "ST_r16", "ST_head", "SR"),
                    lora_max_steps=4)
    man = Manifest(run_id="t")
    rep = stage.run(cfg, layout, man, dry_run=False)
    assert rep.ok, rep.notes
    rel = set(rep.outputs)
    assert rel <= set(man.entries) and layout.manifest.exists()
    assert man.verify(layout.root).passed
    sc = lambda *a: layout.scores("MOCK", "label_validity", *a)   # noqa: E731
    for name, suite, seed in [("P", "E", 0), ("P", "O", 1), ("P2", "E", 0), ("SZ_V1", None, 0), ("SZ_V1_drop", None, 1),
                              ("iso:SZ_V1", "E", 0), ("iso:SZ_V2", "O", 1), ("iso:TL_geo", "E", 0), ("SZ_V2", None, None),
                              ("TL_geo", None, None), ("AGREE", None, None), ("AGREE_problem", None, None), ("AST", None, None),
                              ("PROMPT", "E", 0), ("CODETEXT", "E", 0), ("LAT", "E", 1), ("ST", "E", 0), ("ST", "O", 0), ("ST", "E", 1),
                              ("iso:ST", "E", 0), ("iso:ST_inner234", "E", 0), ("iso:ST_insample", "O", 0), ("iso:ST", "E", 1),
                              ("ST_r1", "E", 0), ("ST_r4", "E", 0), ("ST_r16", "E", 0), ("ST_head", "E", 0), ("SR", "E", 0), ("SR", "O", 0)]:
        assert sc(name, suite, seed).exists(), (name, suite, seed)
    assert not sc("ST", "O", 1).exists()          # seed refits of S^T are EvalPlus-suite only
    t = pq.read_table(sc("ST", "E", 0))
    assert tuple(t.column_names) == TABLE_COLUMNS["scores"] and t.num_rows == len(d.sample_uids)
    fits = json.loads(layout.fits("MOCK", "label_validity", "ST", "E", 0).read_text())
    assert len(fits) == 5 and all(f["selected"]["surrogate"] is True and f["selected"]["inner_adapters"] for f in fits)
    assert json.loads(layout.fits("MOCK", "label_validity", "ST", "E", 1).read_text())[0]["selected"]["inner_adapters"] is False
    rec0 = layout.root / "readouts/MOCK/label_validity/ST/recipes_seed0.json"
    assert rec0.exists() and (layout.root / "readouts/MOCK/label_validity/ST/recipes_seed1.json").exists()
    # the O-suite fit reused the recipe selected under E
    o_fit = json.loads(layout.fits("MOCK", "label_validity", "ST", "O", 0).read_text())[0]["selected"]
    assert o_fit["recipe_from"] == "reused"
    v1 = json.loads((layout.root / "readouts/MOCK/label_validity/SZ_V1/none/parse_rate.json").read_text())
    assert 0 < v1["parse_rate"] < 1 and "k3_switch_to_v2" in v1
    imp = pq.read_table(sc("SZ_V1", None, 0)).to_pandas()
    assert imp["imputed"].sum() == imp["missing"].sum() > 0
    iso = pq.read_table(sc("iso:ST", "E", 0)).to_pandas()
    assert iso["rank_tiebreak"].notna().all() and (iso["prob"] == iso["rank_score"]).all()


def test_stage_skips_generation_only_models_and_missing_capture(tmp_path):
    d, layout = build_run(tmp_path, seeds=(0,))
    cfg = RunConfig(run_id="t", models=("MOCK", "P1"), benchmarks=("humaneval_plus",), backend="mock", generation_only_models=("P1",),
                    readouts=("SZ_V2",))
    rep = stage.run(cfg, layout, Manifest(run_id="t"))
    assert rep.ok and any("P1" in s for s in rep.skipped)
