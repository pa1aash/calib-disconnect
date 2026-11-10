"""Conformance fixes: G1 (both-suite population), G3 (pilot model), G9 (NaN missing), G18 (roles), G4 (reading A)."""

import json

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
import torch

from pipeline.contracts import constants as K
from pipeline.contracts.interfaces import RunConfig, StageReport
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest
from pipeline.readouts import files, fresh, stage
from pipeline.readouts.masked_lora import LoraSpec, MaskedLoraModel, synthetic_layouts
from pipeline.readouts.probe import FittedProbe, crossfit_family
from pipeline.readouts.real_backend import RealBackend
from pipeline.readouts.rtuning import RTuningTokens, own_suffix_context, context_ids, score_rtuning
from test_readouts_stage import build_run
from readouts_helpers import VOCAB, build_tiny, make_data, make_plan

pytestmark = pytest.mark.filterwarnings("ignore")
TOK = RTuningTokens(joiner_ids=(10,), am_ids=(11, 12), sure_ids=(13,), unsure_ids=(14, 15), eot_id=2)


def cfg_for(models, readouts, seeds=(0,), **kw):
    return RunConfig(run_id="t", models=tuple(models), benchmarks=("humaneval_plus",), backend="mock", device="cpu",
                     fold_seeds=tuple(seeds), readouts=tuple(readouts), **kw)


def small(n_problems=15, k=3, seed=0):
    return make_data(n_problems=n_problems, k=k, seed=seed)


# ---------------------------------------------------------------------------------------------------
# G1
# ---------------------------------------------------------------------------------------------------
def write_reference_checks(layout, problems, excluded):
    rows = []
    for p in problems:
        for s in ("O", "E"):
            ex = (p, s) in excluded
            rows.append(dict(problem_id=p, suite_id=s, passed=not ex, failure="wrong_output" if ex else None, excluded=ex))
    layout.reference_checks.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), layout.reference_checks)


def test_no_reference_file_means_no_restriction(tmp_path):
    assert files.valid_label_validity_problems(RunLayout.for_run("t", tmp_path)) is None


def test_problem_excluded_under_one_suite_is_absent_from_every_suite(tmp_path):
    d = small()
    bad = d.problem_ids[0]
    d, layout = build_run(tmp_path, seeds=(0,), d=d)
    write_reference_checks(layout, sorted(set(d.problem_ids)), {(bad, "E")})
    assert files.valid_label_validity_problems(layout) == set(d.problem_ids) - {bad}
    rep = stage.run(cfg_for(["MOCK"], ["P", "P2", "SZ_V2", "CODETEXT", "SZ_V1"]), layout, Manifest(run_id="t"))
    assert rep.ok, rep.notes
    n_bad = sum(p == bad for p in d.problem_ids)
    assert rep.metrics["reference_excluded_samples"]["MOCK/label_validity"] == n_bad > 0
    uid_problem = dict(zip(d.sample_uids, d.problem_ids))
    for name in ("P", "P2", "CODETEXT"):
        for suite in ("O", "E"):
            t = pq.read_table(layout.scores("MOCK", "label_validity", name, suite, 0)).to_pylist()
            assert len(t) == len(d.sample_uids) - n_bad
            assert all(uid_problem[r["sample_uid"]] != bad for r in t), (name, suite)
    for suite in ("O", "E"):
        iso = pq.read_table(layout.scores("MOCK", "label_validity", "iso:SZ_V2", suite, 0)).to_pylist()
        assert iso and all(uid_problem[r["sample_uid"]] != bad for r in iso)
        iso1 = pq.read_table(layout.scores("MOCK", "label_validity", "iso:SZ_V1", suite, 0)).to_pylist()
        assert all(uid_problem[r["sample_uid"]] != bad for r in iso1)
    # the problem's samples are in the unsupervised, label-free readout only
    sz = pq.read_table(layout.scores("MOCK", "label_validity", "SZ_V2", None, None)).to_pylist()
    assert len(sz) == len(d.sample_uids)


def test_fit_sample_counts_use_the_both_suite_population(tmp_path):
    d = small()
    bad = d.problem_ids[0]
    d2, layout = build_run(tmp_path, seeds=(0,), d=d)
    write_reference_checks(layout, sorted(set(d.problem_ids)), {(bad, "E")})
    stage.run(cfg_for(["MOCK"], ["P2"]), layout, Manifest(run_id="t"))
    plan = files.load_plan(layout, "label_validity", 0)
    valid = [(u, p) for u, p in zip(d.sample_uids, d.problem_ids) if p != bad]
    for suite in ("O", "E"):
        for fit in json.loads(layout.fits("MOCK", "label_validity", "P2", suite, 0).read_text()):
            expect = sum(1 for _, p in valid if plan.assignment[p] != fit["outer_fold"])
            assert fit["selected"]["n_train"] == expect


# ---------------------------------------------------------------------------------------------------
# G3
# ---------------------------------------------------------------------------------------------------
def test_pilot_model_gets_seed_refits_and_inner_adapters(tmp_path):
    d, layout = build_run(tmp_path, seeds=(0, 1, 2), model="T1", d=small())
    cfg = cfg_for(["T1"], ["ST"], seeds=(0, 1, 2), lora_max_steps=3, extra={"allow_own_recipe": True})
    rep = stage.run(cfg, layout, Manifest(run_id="t"))
    assert rep.ok, rep.notes
    for seed in (0, 1, 2):
        assert layout.scores("T1", "label_validity", "ST", "E", seed).exists()
    assert not layout.scores("T1", "label_validity", "ST", "E", 3).exists()
    f0 = json.loads(layout.fits("T1", "label_validity", "ST", "E", 0).read_text())
    f1 = json.loads(layout.fits("T1", "label_validity", "ST", "E", 1).read_text())
    assert all(f["selected"]["inner_adapters"] for f in f0) and not any(f["selected"]["inner_adapters"] for f in f1)
    assert layout.scores("T1", "label_validity", "iso:ST_inner234", "E", 0).exists()
    assert not layout.scores("T1", "label_validity", "ST", "O", 1).exists()     # seed refits are EvalPlus only


def test_pilot_model_without_allow_flag_cannot_select_its_own_recipe(tmp_path):
    d, layout = build_run(tmp_path, seeds=(0,), model="T1", d=small())
    with pytest.raises(stage.MissingRecipeError):
        stage.run(cfg_for(["T1"], ["ST"]), layout, Manifest(run_id="t"))


def test_non_primary_model_keeps_seed_zero_only(tmp_path):
    d, layout = build_run(tmp_path, seeds=(0, 1), model="C1", d=small())
    stage.run(cfg_for(["C1"], ["ST"], seeds=(0, 1), lora_max_steps=3), layout, Manifest(run_id="t"))
    assert layout.scores("C1", "label_validity", "ST", "E", 0).exists()
    assert not layout.scores("C1", "label_validity", "ST", "E", 1).exists()
    f0 = json.loads(layout.fits("C1", "label_validity", "ST", "E", 0).read_text())
    assert not any(f["selected"]["inner_adapters"] for f in f0)


# ---------------------------------------------------------------------------------------------------
# G9
# ---------------------------------------------------------------------------------------------------
def test_missing_counts_are_reported_and_nan(tmp_path):
    d = small()
    d.code_logprobs[0] = np.zeros(0, dtype=np.float32)
    d.agreement_outputs[d.sample_uids[1]] = None
    d, layout = build_run(tmp_path, seeds=(0,), d=d)
    rep = stage.run(cfg_for(["MOCK"], ["TL_geo", "TL_min", "TL_sum", "AGREE"]), layout, Manifest(run_id="t"))
    mc = rep.metrics["missing_counts"]["MOCK/label_validity"]
    assert mc["TL_geo"]["missing"] == mc["TL_min"]["missing"] == mc["TL_sum"]["missing"] == 1 and mc["AGREE"]["missing"] == 1
    for name in ("TL_geo", "TL_sum"):
        r = {x["sample_uid"]: x for x in pq.read_table(layout.scores("MOCK", "label_validity", name, None, None)).to_pylist()}
        x = r[d.sample_uids[0]]
        assert x["missing"] and np.isnan(x["prob"]) and np.isnan(x["rank_score"])
    a = {x["sample_uid"]: x for x in pq.read_table(layout.scores("MOCK", "label_validity", "AGREE", None, None)).to_pylist()}
    assert a[d.sample_uids[1]]["missing"] and np.isnan(a[d.sample_uids[1]]["prob"])


# ---------------------------------------------------------------------------------------------------
# G18
# ---------------------------------------------------------------------------------------------------
def test_role_tables():
    assert not stage.st_allowed("X1", "label_validity") and not stage.st_allowed("X2", "lcb")
    assert all(stage.st_allowed(m, "label_validity") for m in ("P1", "B1", "T1", "C3", "S1"))
    assert all(stage.st_allowed(m, "lcb") for m in K.PRIMARY_MODELS) and stage.st_allowed("S1", "lcb")
    assert not any(stage.st_allowed(m, "lcb") for m in ("B1", "T1", "C1", "C3"))
    assert [m for m in list(K.MODELS) if stage.sr_allowed(m, "label_validity")] == ["P1", "S1"]
    assert [m for m in list(K.MODELS) if stage.sr_allowed(m, "lcb")] == ["S1"]
    assert [m for m in list(K.MODELS) if stage.ladder_allowed(m, "label_validity")] == ["P2", "P3"]
    assert not stage.ladder_allowed("P3", "lcb")


def test_stage_skips_readouts_outside_a_models_role(tmp_path):
    d, layout = build_run(tmp_path, seeds=(0,), model="B1", d=small())
    rep = stage.run(cfg_for(["B1"], ["MLP", "SR", "ST_r1", "ST_head"]), layout, Manifest(run_id="t"))
    assert rep.ok and not (layout.root / "readouts" / "B1" / "label_validity").exists()
    assert any("MLP" in n for n in rep.notes) and any("not run for this model's role" in n for n in rep.notes)


# ---------------------------------------------------------------------------------------------------
# G4: reading A
# ---------------------------------------------------------------------------------------------------
GS = "fresh:SR_E_seed0_fold2"


def test_discover_fresh_sets(tmp_path):
    layout = RunLayout.for_run("t", tmp_path)
    for gs in (GS, "fresh:SR_lcb_label_seed1_fold0", "frozen"):
        layout.capture_index("MOCK", "humaneval_plus", gs, 0).parent.mkdir(parents=True)
    found = fresh.discover_fresh_sets(layout, "MOCK", ["humaneval_plus"])
    assert [(f.gen_set, f.suite, f.seed, f.fold) for f in found] == [
        (GS, "E", 0, 2), ("fresh:SR_lcb_label_seed1_fold0", "lcb_label", 1, 0)]


def test_fitted_probe_roundtrip_matches_the_scores(tmp_path):
    d = make_data(n_problems=25, k=3)
    plan = make_plan(set(d.problem_ids))
    fam = crossfit_family(d, plan, "E", "MOCK", "label_validity", want=("P", "P2", "Pmulti"))
    for name in ("P", "Pmulti"):
        by_uid = {r.sample_uid: r.rank_score for r in fam.scores[name]}
        for f in range(5):
            fp = fam.fitted[(f, name)]
            fp.save(tmp_path / f"{name}{f}.npz")
            fp2 = FittedProbe.load(tmp_path / f"{name}{f}.npz")
            rows = [i for i, p in enumerate(d.problem_ids) if plan.assignment[p] == f]
            z = fp2.logits({k: v[rows] for k, v in d.hidden.items()})
            assert np.allclose(z, [by_uid[d.sample_uids[i]] for i in rows], atol=1e-4)
            assert fp2.fold_seed == 0 and fp2.outer_fold == f and fp2.label_suite == "E"


def test_reading_a_on_a_fake_fresh_set_with_the_mock_backend(tmp_path):
    frozen = small(n_problems=15, k=3)
    d, layout = build_run(tmp_path, seeds=(0,), d=frozen)
    cfg = cfg_for(["MOCK"], ["P", "SR"], lora_max_steps=2)
    man = Manifest(run_id="t")
    stage.run(cfg, layout, man)
    for f in range(5):
        assert fresh.probe_path(layout, "MOCK", "label_validity", "E", 0, f).exists()
        assert fresh.sr_adapter_path(layout, "MOCK", "label_validity", "E", 0, f, surrogate=True).exists()
    fake = make_data(n_problems=4, k=3, seed=11)
    build_run(tmp_path, d=fake, layout=layout, gen_set=GS, plans=False)
    rep = stage.run(cfg, layout, man)
    assert rep.ok, rep.notes
    fs = fresh.FreshSet(GS, "E", 0, 2)
    for name in ("P", "SR"):
        path = layout.scores("MOCK", "label_validity", name, "E", 0, GS)
        assert path.exists() and "fresh_SR_E_seed0_fold2" in str(path)
        rows = pq.read_table(path).to_pylist()
        assert len(rows) == len(fake.sample_uids)
        assert all(r["generation_set"] == GS and r["fold"] == 2 and r["fold_seed"] == 0 and r["label_suite"] == "E" for r in rows)
        assert str(path.relative_to(layout.root)) in man.entries
    # the P rows are the persisted fold-2 probe applied to the fresh set's base-weights states
    fp = FittedProbe.load(fresh.probe_path(layout, "MOCK", "label_validity", "E", 0, 2))
    got = {r["sample_uid"]: r["rank_score"] for r in pq.read_table(layout.scores("MOCK", "label_validity", "P", "E", 0, GS)).to_pylist()}
    want = fp.logits(files.load_readout_data(layout, "MOCK", ["humaneval_plus"], GS).hidden)
    uids = files.load_readout_data(layout, "MOCK", ["humaneval_plus"], GS).sample_uids
    assert np.allclose([got[u] for u in uids], want, atol=1e-5)
    # frozen scores are untouched and live in a different file
    assert layout.scores("MOCK", "label_validity", "P", "E", 0).exists()
    assert len(pq.read_table(layout.scores("MOCK", "label_validity", "P", "E", 0)).to_pylist()) == len(frozen.sample_uids)
    del fs


def test_adapter_save_load_roundtrip_on_a_tiny_model(tmp_path):
    m1 = build_tiny("qwen3", seed=0)
    a1 = MaskedLoraModel(m1, LoraSpec(), init_std=0.1, seed=3)
    a1.save_adapter(tmp_path / "ad")
    m2 = build_tiny("qwen3", seed=0)
    a2 = MaskedLoraModel(m2, LoraSpec(), seed=9)                 # a different (zero-B) adapter
    seqs = [((3, 4, 5), (6, 7, 2)), ((8,), (9, 9, 9, 2))]
    before = [s.logit for s in score_rtuning(m2, a2, seqs, TOK)]
    a2.load_adapter(tmp_path / "ad")
    after = [s.logit for s in score_rtuning(m2, a2, seqs, TOK)]
    ref = [s.logit for s in score_rtuning(m1, a1, seqs, TOK)]
    assert not np.allclose(before, ref) and np.allclose(after, ref, atol=1e-5)
    a1.close(); a2.close()


def test_own_suffix_context_and_scoring():
    comp_with = [6, 7, 10, 11, 12, 13, 2]            # code, joiner, "I am", " sure", end of turn
    assert own_suffix_context([3, 4], comp_with, TOK) == [3, 4, 6, 7, 10, 11, 12]
    comp_without = [6, 7, 2]
    assert own_suffix_context([3, 4], comp_without, TOK) == context_ids([3, 4], comp_without, TOK)
    m = build_tiny("qwen3")
    s = score_rtuning(m, None, [((3, 4), comp_with)], TOK, own_suffix=True)[0]
    ctx = [3, 4, 6, 7, 10, 11, 12]
    lg = torch.log_softmax(m(torch.tensor([ctx + [13]])).logits[0], -1)
    assert s.lp_sure == pytest.approx(lg[len(ctx) - 1, 13].item(), abs=1e-4)


def fake_provider(cfg, layout, model_key, benches, sample_uids, tokenizer, model, gen_set="frozen"):
    return synthetic_layouts(VOCAB, n=len(sample_uids), seed=21)


def test_reading_a_with_a_tiny_real_model(tmp_path):
    frozen = small(n_problems=12, k=3)
    d, layout = build_run(tmp_path, seeds=(0,), d=frozen)
    fake = make_data(n_problems=3, k=3, seed=5)
    build_run(tmp_path, d=fake, layout=layout, gen_set=GS, plans=False)
    # a saved S^R adapter and a persisted probe for (E, seed 0, fold 2)
    model = build_tiny("qwen3")
    ad = MaskedLoraModel(model, LoraSpec(), init_std=0.1, seed=4)
    ad_path = fresh.sr_adapter_path(layout, "MOCK", "label_validity", "E", 0, 2)
    ad.save_adapter(ad_path)
    ad.close()
    fam = crossfit_family(frozen, files.load_plan(layout, "label_validity", 0), "E", "MOCK", "label_validity", want=("P",))
    fam.fitted[(2, "P")].save(fresh.probe_path(layout, "MOCK", "label_validity", "E", 0, 2))
    cfg = RunConfig(run_id="t", models=("MOCK",), benchmarks=("humaneval_plus",), backend="transformers", device="cpu",
                    readouts=("P", "SR"), extra={"layouts_provider": "test_readouts_conformance:fake_provider"})
    man = Manifest(run_id="t")
    rep = StageReport(stage="readouts", ok=True)
    ctx = stage._Ctx(cfg, layout, files.Writer(cfg, layout, man, rep), rep, "MOCK", "label_validity", ("humaneval_plus",), frozen)
    ctx._real = RealBackend(model, synthetic_layouts(VOCAB, n=6, seed=1), [1], [2], rtuning_tokens=TOK)
    ctx.run_fresh()
    rows = pq.read_table(layout.scores("MOCK", "label_validity", "SR", "E", 0, GS)).to_pylist()
    assert len(rows) == len(fake.sample_uids)
    # expected: the loaded adapter scored from each sample's own suffix over the provider's layouts
    ref_model = build_tiny("qwen3")
    ref = MaskedLoraModel(ref_model, LoraSpec(), seed=0)
    ref.load_adapter(ad_path)
    lays = synthetic_layouts(VOCAB, n=len(fake.sample_uids), seed=21)
    exp = score_rtuning(ref_model, ref, [(l.prompt_ids, l.completion_ids) for l in lays], TOK, own_suffix=True)
    got = {r["sample_uid"]: r["rank_score"] for r in rows}
    uids = files.load_readout_data(layout, "MOCK", ["humaneval_plus"], GS).sample_uids
    assert np.allclose([got[u] for u in uids], [e.logit for e in exp], atol=1e-4)
    assert all(r["generation_set"] == GS for r in rows)
    assert (layout.root / "config" / "mask_test_qwen3.json").exists()      # the gate ran before scoring
    assert layout.scores("MOCK", "label_validity", "P", "E", 0, GS).exists()
    ref.close()
