"""Fixes from the independent review of the masked-LoRA code (B1, B2, M1 to M4, positive controls, minors)."""

import json
import sys
from pathlib import Path

import numpy as np
import pytest
import torch

from pipeline.contracts import constants as K
from pipeline.contracts.interfaces import RunConfig, StageReport, TeacherForcedLayout
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest
from pipeline.readouts import files, gate, masked_lora, probe, stage
from pipeline.readouts.masked_lora import (LoraSpec, MaskedLoraModel, bce_on_logodds, collate_layouts, mask_unit_test,
                                           synthetic_layouts)
from pipeline.readouts.real_backend import RealBackend, answer_ids_from_config
from readouts_helpers import VOCAB, build_tiny, make_data, make_plan

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "generate"))
import gen_tinylm as T  # noqa: E402

pytestmark = pytest.mark.filterwarnings("ignore")


# ---------------------------------------------------------------------------------------------------
# B1: answer-token file written by the generate stage
# ---------------------------------------------------------------------------------------------------
def test_answer_ids_read_the_file_the_generate_stage_writes(tmp_path):
    from pipeline.generate.stage import PRODUCER_CAP, _write_json_merged
    from pipeline.generate.tokens import answer_token_variants
    tok = T.build_tokenizer()
    variants = answer_token_variants(tok)
    layout = RunLayout.for_run("t", tmp_path)
    man = Manifest(run_id="t")
    layout.root.mkdir(parents=True)
    _write_json_merged(layout, man, layout.answer_tokens, "P1", {"model_id": "x/y", "revision": "r", **variants}, PRODUCER_CAP)
    _write_json_merged(layout, man, layout.answer_tokens, "MOCK", {"backend": "mock"}, PRODUCER_CAP)
    yes, no = answer_ids_from_config(layout.answer_tokens, "P1", tok)
    assert yes == [d["id"] for d in variants["yes"]] and no == [d["id"] for d in variants["no"]] and yes and no
    assert isinstance(json.loads(layout.answer_tokens.read_text())["P1"]["yes"][0], dict)
    # the mock placeholder and a missing file fall back to the generate stage's tokenizer scan: the same sets
    assert answer_ids_from_config(layout.answer_tokens, "MOCK", tok) == (yes, no)
    assert answer_ids_from_config(tmp_path / "none.json", "P1", tok) == (yes, no)
    # plain integer ids (an older file) are still accepted
    old = tmp_path / "old.json"
    old.write_text(json.dumps({"P1": {"yes": [5, 6], "no": [7]}}))
    assert answer_ids_from_config(old, "P1", tok) == ([5, 6], [7])


# ---------------------------------------------------------------------------------------------------
# B2: initialization does not depend on a generator device
# ---------------------------------------------------------------------------------------------------
def test_reset_is_seeded_and_uses_cpu_generator_then_copies():
    m = build_tiny("qwen3")
    a = MaskedLoraModel(m, LoraSpec(), seed=5, init_std=0.1)
    s1 = a.lora_state()
    a.reset(5, init_std=0.1)
    s2 = a.lora_state()
    a.reset(6, init_std=0.1)
    s3 = a.lora_state()
    assert all(torch.equal(s1[k], s2[k]) for k in s1) and not all(torch.equal(s1[k], s3[k]) for k in s1)
    a.close()


@pytest.mark.skipif(not torch.cuda.is_available(), reason="needs a GPU")
def test_reset_on_cuda():
    m = build_tiny("qwen3").cuda()
    a = MaskedLoraModel(m, LoraSpec(), seed=1, init_std=0.1)
    a.reset(2)
    a.close()


# ---------------------------------------------------------------------------------------------------
# M1: the mask-test gate
# ---------------------------------------------------------------------------------------------------
def _real(tmp_path, model=None):
    model = model or build_tiny("qwen3")
    return RealBackend(model, synthetic_layouts(VOCAB, n=6, seed=1), [1], [2])


@pytest.mark.parametrize("arch", ["qwen3", "gemma4"])
def test_gate_runs_on_a_float32_slice_of_a_bf16_model(tmp_path, arch):
    m = build_tiny(arch).to(torch.bfloat16)
    reg = []
    rep = gate.run_mask_gate(m, synthetic_layouts(VOCAB, n=6), tmp_path / "config" / f"mask_test_{gate.arch_key(m)}.json",
                             yes_ids=[1], no_ids=[2], register=reg.append, n_slice_layers=1)
    assert rep["passed"] and rep["tested_dtype"] == "float32" and "slice" in rep["tested_on"] and rep["model_dtype"] == "torch.bfloat16"
    assert len(reg) == 1 and json.loads(reg[0].read_text())["arch"] == gate.arch_key(m)
    assert next(m.parameters()).dtype == torch.bfloat16 and not any("lora" in n for n, _ in m.named_parameters())


def test_gate_failure_raises_and_writes_report(tmp_path, monkeypatch):
    m = build_tiny("qwen3")
    monkeypatch.setattr(gate, "mask_unit_test", lambda *a, **k: {"passed": False, "a_nonmasked_match": False})
    p = tmp_path / "mask_test_qwen3.json"
    with pytest.raises(gate.MaskTestFailed):
        gate.run_mask_gate(m, synthetic_layouts(VOCAB, n=4), p, yes_ids=[1], no_ids=[2])
    assert json.loads(p.read_text())["passed"] is False


def _ctx(tmp_path, real, monkeypatch=None):
    from test_readouts_stage import build_run
    d, layout = build_run(tmp_path, seeds=(0,))
    cfg = RunConfig(run_id="t", models=("MOCK",), benchmarks=("humaneval_plus",), backend="transformers", device="cpu")
    man = Manifest(run_id="t")
    rep = StageReport(stage="readouts", ok=True)
    ctx = stage._Ctx(cfg, layout, files.Writer(cfg, layout, man, rep), rep, "MOCK", "label_validity", ("humaneval_plus",), d)
    ctx._real = real
    return ctx, layout, man


def test_stage_runs_the_gate_before_training_and_registers_the_report(tmp_path):
    ctx, layout, man = _ctx(tmp_path, _real(tmp_path))
    with ctx.trainer("st") as tr:
        assert tr.mlm.n_lora_layers == 14
    rp = layout.config_dir / "mask_test_qwen3.json"
    assert rp.exists() and json.loads(rp.read_text())["passed"] and str(rp.relative_to(layout.root)) in man.entries


def test_stage_refuses_to_train_when_the_mask_test_fails(tmp_path, monkeypatch):
    ctx, layout, man = _ctx(tmp_path, _real(tmp_path))
    monkeypatch.setattr(gate, "mask_unit_test", lambda *a, **k: {"passed": False})
    with pytest.raises(gate.MaskTestFailed):
        with ctx.trainer("st"):
            raise AssertionError("trainer must not be created")


# ---------------------------------------------------------------------------------------------------
# M2: recipes of checkpoints come from the source model's FitRecords
# ---------------------------------------------------------------------------------------------------
def _source_fits(layout, man, model="P3", seed=0):
    from pipeline.contracts.schemas import FitRecord
    rep = StageReport(stage="readouts", ok=True)
    w = files.Writer(RunConfig(run_id="t", models=(model,), benchmarks=()), layout, man, rep)
    recs = [FitRecord(model, "ST", "E", seed, f, {"lr": 1e-4 * (f + 1), "steps": 40 + f, "n_train_inner": 3000,
                                                   "epoch_fraction": 0.85, "schedule_epochs": 2}, 0.5, 0.69)
            for f in range(5)]
    w.fits(model, "label_validity", "ST", "E", seed, recs)


def test_recipe_source_table():
    s = stage.RECIPE_SOURCE
    assert [s[f"B{i}"] for i in range(1, 7)] == [f"P{i}" for i in range(1, 7)]
    assert s["T1"] == s["T2"] == s["B3"] == "P3" and s["S1"] == "P1"


@pytest.mark.parametrize("model,source", [("T2", "P3"), ("B3", "P3"), ("S1", "P1")])
def test_checkpoints_reuse_the_source_recipe_per_seed_and_fold(tmp_path, model, source):
    ctx, layout, man = _ctx(tmp_path, None)
    ctx.model = model
    with pytest.raises(stage.MissingRecipeError):
        ctx.table(0)
    ctx.tables.clear()
    _source_fits(layout, man, source)
    t = ctx.table(0)
    assert t.get(0, 3).lr == pytest.approx(4e-4) and t.get(0, 3).steps == 43 and t.has_seed(0, range(5))
    assert ctx.recipe_origin == f"{source} FitRecords"


def test_pilot_model_may_select_its_own_recipe(tmp_path):
    ctx, layout, man = _ctx(tmp_path, None)
    ctx.model = "T1"
    object.__setattr__(ctx.cfg, "extra", {"allow_own_recipe": True})
    assert not ctx.table(0).recipes and "allow_own_recipe" in ctx.recipe_origin


def test_lcb_without_label_validity_recipe_raises(tmp_path):
    ctx, layout, man = _ctx(tmp_path, None)
    ctx.pop = "lcb"
    with pytest.raises(stage.MissingRecipeError):
        ctx.table(0)


# ---------------------------------------------------------------------------------------------------
# M3: the mask span against an independent count, with a real chat template
# ---------------------------------------------------------------------------------------------------
ELIC_V2 = "<|im_start|>user\n" + K.V2_TEXT + "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"


def _span_ok(tok, lay: TeacherForcedLayout) -> bool:
    """Independent check: the elicitation tokens are exactly the tokenization of the V2 turn text."""
    ref = tok(ELIC_V2, add_special_tokens=False)["input_ids"]
    return list(lay.elicitation_ids) == ref and tok.decode(list(lay.elicitation_ids)) == ELIC_V2


@pytest.fixture(scope="module")
def tiny_chat():
    from pipeline.generate import capture as CP
    from pipeline.generate.prompts import load_prompts
    tok = T.build_tokenizer()
    model = T.build_model(tok)
    cap = CP.TransformersCapture(model, tok, load_prompts(), batch_size=4)
    prob = T.problem()
    recs = [T.make_record(tok, prob, t, j=i + 1) for i, t in enumerate(
        [T.GOOD, "Sure.\n```python\ndef add(a, b):\n    # sum\n    return a + b\n```\nDone, enjoy it all.", T.GOOD.replace("Here is", "x")])]
    return tok, model, cap, prob, recs


def test_mask_span_from_generate_layouts_matches_independent_count(tiny_chat):
    tok, model, cap, prob, recs = tiny_chat
    lays = [cap.build_layout(r, prob) for r in recs]
    n_ref = len(tok(ELIC_V2, add_special_tokens=False)["input_ids"])
    batch = collate_layouts(lays, pad_id=tok.pad_token_id)
    start = tok.convert_tokens_to_ids("<|im_start|>")
    for b, lay in enumerate(lays):
        assert _span_ok(tok, lay) and len(lay.elicitation_ids) == n_ref
        assert int(batch.mask[b].sum()) == n_ref                         # the mask covers exactly the V2 turn
        assert batch.mask[b, -n_ref:].all() and batch.input_ids[b, -n_ref].item() == start
        assert batch.input_ids[b, -n_ref - 1].item() != start            # one token earlier is outside the span
        assert lay.p3 == len(lay.prompt_ids) + len(lay.completion_ids) + n_ref - 1
    # the unit test passes on these layouts with the model's own answer tokens
    from pipeline.generate.tokens import answer_token_variants
    v = answer_token_variants(tok)
    rep = mask_unit_test(model, lays, LoraSpec(), pad_id=tok.pad_token_id, yes_ids=[d["id"] for d in v["yes"]],
                         no_ids=[d["id"] for d in v["no"]])
    assert rep["passed"], rep


def test_a_wrong_span_fails_the_independent_check(tiny_chat):
    tok, model, cap, prob, recs = tiny_chat
    lay = cap.build_layout(recs[0], prob)
    assert _span_ok(tok, lay)
    e = lay.elicitation_ids
    short = TeacherForcedLayout(lay.prompt_ids, lay.completion_ids, e[1:], lay.code_span)            # missing header token
    long_ = TeacherForcedLayout(lay.prompt_ids, lay.completion_ids[:-1], (lay.completion_ids[-1],) + e, lay.code_span)  # bridge included
    thought = TeacherForcedLayout(lay.prompt_ids, lay.completion_ids, e[:-2], lay.code_span)         # cut inside the thought block
    assert not _span_ok(tok, short) and not _span_ok(tok, long_) and not _span_ok(tok, thought)


def test_default_provider_builds_layouts_from_generate_records(tiny_chat):
    from pipeline.readouts.layouts import build_layouts
    tok, model, cap, prob, recs = tiny_chat
    lays = build_layouts(cap, [r.sample_uid for r in recs], {r.sample_uid: r for r in recs}, {prob.problem_id: prob}, {})
    assert all(_span_ok(tok, l) for l in lays) and len(lays) == 3


def test_collate_rejects_a_mask_that_is_not_the_trailing_span():
    class Shifted(TeacherForcedLayout):
        def mask(self):
            m = super().mask()
            m[-1], m[-2 - len(self.elicitation_ids)] = 0, 1
            return m
    l = synthetic_layouts(VOCAB, n=1)[0]
    bad = Shifted(l.prompt_ids, l.completion_ids, l.elicitation_ids, l.code_span)
    with pytest.raises(ValueError):
        collate_layouts([bad])


# ---------------------------------------------------------------------------------------------------
# M4: the probe's K4 retry
# ---------------------------------------------------------------------------------------------------
def _patched_selection(monkeypatch, fail_unless_extra: bool):
    seen = []
    real = probe.select_over_specs

    def fake(feats, F, f, specs, Cs, tag):
        sel = real(feats, F, f, specs, Cs, tag)
        seen.append(tuple(sorted(Cs)))
        base = sel.base_rate_pooled
        for k in list(sel.loss):
            good = fail_unless_extra and k[2] in probe.PROBE_RETRY_EXTRA_C
            sel.loss[k] = base - 0.05 if good else base + 0.1
            sel.loss_split0[k] = sel.loss[k]
        return sel
    monkeypatch.setattr(probe, "select_over_specs", fake)
    return seen


def test_probe_k4_retry_succeeds_with_extra_c_values(monkeypatch):
    d = make_data(n_problems=20, k=3)
    plan = make_plan(set(d.problem_ids))
    seen = _patched_selection(monkeypatch, fail_unless_extra=True)
    fam = probe.crossfit_family(d, plan, "E", "MOCK", "label_validity", want=("P", "P2"))
    assert seen[0] == tuple(sorted(K.PROBE_C_GRID)) and set(seen[-1]) == set(K.PROBE_C_GRID) | {1e-4, 100.0}
    for f in fam.fits["P"] + fam.fits["P2"]:
        assert f.retried and not f.flagged and f.selected["C"] in (1e-4, 100.0)
    assert not any(s.flagged for s in fam.scores["P"])


def test_probe_k4_flags_when_the_retry_also_fails(monkeypatch):
    d = make_data(n_problems=20, k=3)
    plan = make_plan(set(d.problem_ids))
    _patched_selection(monkeypatch, fail_unless_extra=False)
    fam = probe.crossfit_family(d, plan, "E", "MOCK", "label_validity", want=("P",))
    assert all(f.retried and f.flagged for f in fam.fits["P"]) and all(s.flagged for s in fam.scores["P"])


def test_probe_without_failure_does_not_retry():
    d = make_data(n_problems=40, k=4)
    fam = probe.crossfit_family(d, make_plan(set(d.problem_ids)), "E", "MOCK", "label_validity", want=("P",))
    assert not any(f.retried or f.flagged for f in fam.fits["P"])
    assert all(set(f.selected["C_grid"]) == set(K.PROBE_C_GRID) for f in fam.fits["P"])


# ---------------------------------------------------------------------------------------------------
# Positive controls fail when they should; other minors
# ---------------------------------------------------------------------------------------------------
def test_positive_control_fails_for_a_zero_adapter():
    m = build_tiny("qwen3")
    ad = MaskedLoraModel(m, LoraSpec(), init_std=None)       # B = 0: the adapter does nothing
    rep = mask_unit_test(m, synthetic_layouts(VOCAB, n=3), ad)
    assert not rep["b_masked_differ"] and not rep["passed"] and rep["adapter_changes_logodds"] <= 1e-3
    ad.close()


def test_positive_control_fails_for_a_zero_mask(monkeypatch):
    real = masked_lora.collate_layouts

    def zero_mask(*a, **k):
        b = real(*a, **k)
        b.mask = torch.zeros_like(b.mask)
        return b
    monkeypatch.setattr(masked_lora, "collate_layouts", zero_mask)
    rep = mask_unit_test(build_tiny("qwen3"), synthetic_layouts(VOCAB, n=3))
    assert not rep["b_masked_differ"] and not rep["passed"]


def test_hook_gives_exact_zero_off_the_span_even_for_non_finite_branch_output():
    ad = MaskedLoraModel(build_tiny("olmo3"), LoraSpec(), init_std=0.05)
    out = torch.tensor([[[float("inf"), float("nan")], [1.0, 2.0]]])
    ad._mask = torch.tensor([[[0.0], [1.0]]])
    res = ad._hook(None, None, out)
    ad._mask = None
    assert torch.equal(res[0, 0], torch.zeros(2)) and torch.equal(res[0, 1], torch.tensor([1.0, 2.0]))
    ad.close()


def test_right_padded_batch_is_rejected():
    m = build_tiny("qwen3")
    ad = MaskedLoraModel(m, LoraSpec())
    b = collate_layouts(synthetic_layouts(VOCAB, n=3, seed=9))
    b.attention_mask = b.attention_mask.flip(-1)
    with pytest.raises(ValueError):
        ad.final_state(b)
    ad.close()


def test_gradient_equivalence_with_a_sliding_window_shorter_than_the_sequence():
    m = build_tiny("gemma4", sliding_window=8)
    ad = MaskedLoraModel(m, LoraSpec(dropout=0.0), init_std=0.05, seed=3)
    ad.train()
    batch = collate_layouts(synthetic_layouts(VOCAB, n=4, seed=4), y=np.array([0, 1, 1, 0]))
    g = {}
    for eco in (False, True):
        for p in ad.trainable_parameters():
            p.grad = None
        bce_on_logodds(ad.logodds(batch, [1], [2], economy=eco), batch.y).backward()
        g[eco] = [p.grad.clone() for p in ad.trainable_parameters()]
    mx = max(x.abs().max().item() for x in g[False])
    assert mx > 1e-6 and all(torch.allclose(a, b, atol=1e-6 + 1e-4 * mx) for a, b in zip(g[False], g[True]))
    ad.close()


def test_slice_keeps_every_layer_type_in_order():
    inter = ["sliding_attention"] * 5 + ["full_attention"] + ["sliding_attention"] * 5 + ["full_attention"]
    assert gate.slice_layer_indices(inter, 12) == [0, 5]
    assert gate.slice_layer_indices(["a", "b", "a", "c"], 4) == [0, 1, 3]
    assert gate.slice_layer_indices(["full_attention"] * 4, 4) == [0, 1]       # padded to two layers
    assert gate.slice_layer_indices(None, 40) == [0, 1] and gate.slice_layer_indices([], 1) == [0]


def test_slice_of_interleaved_model_copies_the_chosen_layers_and_reports_indices(tmp_path):
    from transformers.models.gemma4.configuration_gemma4 import Gemma4TextConfig
    from transformers.models.gemma4.modeling_gemma4 import Gemma4ForCausalLM
    torch.manual_seed(0)
    cfg = Gemma4TextConfig(vocab_size=VOCAB, vocab_size_per_layer_input=VOCAB, hidden_size=64, intermediate_size=128,
                           num_hidden_layers=6, num_attention_heads=4, num_key_value_heads=2, head_dim=16,
                           hidden_size_per_layer_input=16, sliding_window=8, global_head_dim=16, eos_token_id=2,
                           bos_token_id=1, pad_token_id=0, layer_types=["sliding_attention"] * 5 + ["full_attention"])
    m = Gemma4ForCausalLM(cfg).eval().to(torch.bfloat16)
    small, idx = gate.float32_slice(m, 2)
    assert idx == [0, 5] and small.config.get_text_config().layer_types == ["sliding_attention", "full_attention"]
    assert torch.equal(small.model.layers[1].self_attn.q_proj.weight, m.model.layers[5].self_attn.q_proj.weight.float())
    rep = gate.run_mask_gate(m, synthetic_layouts(VOCAB, n=5), tmp_path / "r.json", yes_ids=[1], no_ids=[2])
    assert rep["passed"] and rep["slice_layer_indices"] == [0, 5] and "full_attention" in rep["layer_types"]


def test_reused_passing_mask_report_is_registered(tmp_path):
    # Smoke-run finding: a passing report reused from an earlier run must still enter the manifest.
    import json as _json
    from pipeline.readouts.gate import run_mask_gate
    rp = tmp_path / "config" / "mask_test_x.json"
    rp.parent.mkdir(parents=True)
    rp.write_text(_json.dumps({"passed": True, "arch": "x"}))
    seen = []
    out = run_mask_gate(object(), [], rp, yes_ids=[1], no_ids=[2], register=seen.append)
    assert out["passed"] and seen == [rp]
