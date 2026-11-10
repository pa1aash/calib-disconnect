import copy
import math

import numpy as np
import pytest
import torch

from pipeline.contracts import constants as C
from pipeline.contracts.interfaces import TeacherForcedLayout
from pipeline.contracts.schemas import ExtractionResult
from pipeline.generate import capture as CP
from pipeline.generate import tokens as K
from pipeline.generate.prompts import apply_chat

import gen_tinylm as T

CODE = "def add(a, b):\n    return a + b\n"
ELIC_V2 = "<|im_start|>user\n" + C.V2_TEXT + "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"


def ext(rec, code=None, failure=None):
    if code is None and failure is None:
        code, failure = K.extract_fallback(rec.sample_uid, rec.completion_text, "add", False, use_execute=False)
    return ExtractionResult(rec.sample_uid, code if failure is None else None,
                            "fenced" if failure is None else None, failure)


@pytest.fixture(scope="module")
def prob():
    return T.problem()


@pytest.fixture(scope="module")
def cap(model, tok, prompts):
    return CP.TransformersCapture(model, tok, prompts, batch_size=4)


@pytest.fixture(scope="module")
def recs(tok, prob):
    texts = [T.GOOD, "Sure.\n```python\ndef add(a, b):\n    # sum\n    return a + b\n```\nDone, enjoy it all.",
             T.GOOD.replace("Here is the code.", "x")]
    return [T.make_record(tok, prob, t, j=i + 1) for i, t in enumerate(texts)]


def test_layout_construction(cap, tok, prob, recs, prompts):
    r = recs[0]
    lay = cap.build_layout(r, prob, ext(r))
    assert isinstance(lay, TeacherForcedLayout)
    rendered = apply_chat(tok, [{"role": "user", "content": prompts.generation_message(prob)}],
                          add_generation_prompt=True, thinking=False)
    assert lay.prompt_ids == tuple(tok(rendered, add_special_tokens=False)["input_ids"])
    eot, nl = tok.convert_tokens_to_ids("<|im_end|>"), tok("\n")["input_ids"][0]
    assert lay.completion_ids == tuple(r.completion_token_ids) + (nl,) and r.completion_token_ids[-1] == eot
    assert tok.decode(lay.elicitation_ids) == ELIC_V2
    full = lay.prompt_ids + lay.completion_ids + lay.elicitation_ids
    assert tok.decode(full) == rendered + T.GOOD + "<|im_end|>\n" + ELIC_V2
    # spans and positions
    assert lay.p1 == len(lay.prompt_ids) - 1 and tok.decode(full[lay.p1]) == "\n"
    s, e = lay.code_span
    assert tok.decode(full[s:e]) == CODE.rstrip("\n")
    assert lay.elicitation_span == (len(lay.prompt_ids) + len(lay.completion_ids), len(full))
    assert lay.p3 == len(full) - 1
    m = lay.mask()
    assert m.sum() == len(lay.elicitation_ids) and m[lay.elicitation_span[0]:].all() and not m[:lay.elicitation_span[0]].any()
    assert tok.convert_ids_to_tokens(full[lay.elicitation_span[0]]) == "<|im_start|>"


def test_eot_appended_when_missing_and_truncation_untouched(cap, tok, prob):
    r = T.make_record(tok, prob, T.GOOD, add_stop=False)
    lay = cap.build_layout(r, prob, ext(r))
    eot = tok.convert_tokens_to_ids("<|im_end|>")
    assert lay.completion_ids[-2] == eot and lay.completion_ids[:-2] == tuple(r.completion_token_ids)
    t = T.make_record(tok, prob, T.GOOD + " and more", finish="length")
    lt = cap.build_layout(t, prob, ext(t))
    assert lt.completion_ids == tuple(t.completion_token_ids)        # no end-of-turn token, no bridge


def test_strict_mode_matches_full_conversation_render(tok, prompts, prob):
    tk = T.build_tokenizer(T.T_STABLE)
    m = T.build_model(tk)
    c = CP.TransformersCapture(m, tk, prompts, strict=True)
    r = T.make_record(tk, prob, T.GOOD)
    lay = c.build_layout(r, prob, ext(r))        # raises AssertionError if the layout differs from the render
    assert tk.decode(lay.elicitation_ids).startswith("<|im_start|>user\n")


def test_extraction_failure_positions(cap, tok, prob):
    r = T.make_record(tok, prob, T.NOFENCE, j=4)
    p = cap.prepare(r, prob, ext(r, failure="no_block"))
    core = len(r.completion_token_ids) - 1
    off = len(p.layout.prompt_ids)
    assert p.failure and p.p2 == off + core - 1                      # last generated token before the end-of-turn token
    assert tok.decode(p.full[p.p2]) == "."
    assert p.layout.code_span == (p.p2 + 1, p.p2 + 1) and p.mean_span == (off, off + core)
    assert cap.prepare(r, prob, None).failure                         # fallback extraction finds no block


def test_code_location_failure_is_treated_as_failure(cap, tok, prob):
    r = T.make_record(tok, prob, T.GOOD)
    p = cap.prepare(r, prob, ext(r, code="def other(): pass"))
    assert p.failure and "code_locate_failed" in p.notes


def test_shapes_layers_and_values_against_direct_forward(cap, model, tok, prob, recs):
    out, arrays = cap.capture(recs, {r.sample_uid: ext(r) for r in recs}, {prob.problem_id: prob})
    n, L, D = len(recs), 7, 64
    assert cap.layers == (2, 3, 4, 5, 6, 7, 8) == tuple(math.floor(f * 8) for f in C.LAYER_FRACTIONS)
    for k in ("hs_p1", "hs_p2", "hs_p3", "hs_mean_code"):
        assert arrays[k].shape == (n, L, D) and arrays[k].dtype == torch.bfloat16
    assert arrays["yes_no_logodds"].dtype == np.float32 and arrays["code_logprobs"].dtype == np.float32
    offs = arrays["code_logprob_offsets"]
    assert offs.dtype == np.int64 and len(offs) == n + 1 and offs[-1] == len(arrays["code_logprobs"])
    for i, (r, c) in enumerate(zip(recs, out)):
        p = cap.prepare(r, prob, ext(r))
        assert c.hidden.layers == cap.layers and c.hidden.row == i and c.hidden.dtype == "bfloat16"
        assert (c.p1, c.p2, c.p3) == (p.p1, p.p2, p.p3) and c.elicitation_span == p.layout.elicitation_span
        assert c.n_code_tokens == offs[i + 1] - offs[i] == p.layout.code_span[1] - p.layout.code_span[0]
        with torch.no_grad():
            ref = model(input_ids=torch.tensor([p.full]), output_hidden_states=True)
        hs = ref.hidden_states
        assert len(hs) == 9
        for key, pos in (("hs_p1", p.p1), ("hs_p2", p.p2), ("hs_p3", p.p3)):
            want = torch.stack([hs[l][0, pos] for l in cap.layers]).to(torch.bfloat16)
            assert torch.allclose(arrays[key][i].float(), want.float(), atol=2e-2, rtol=2e-2), key
        s, e = p.layout.code_span
        want = torch.stack([hs[l][0, s:e].mean(0) for l in cap.layers])
        assert torch.allclose(arrays["hs_mean_code"][i].float(), want, atol=2e-2, rtol=2e-2)
        # code-token log-probs: log-softmax of the previous position's logits
        lp = torch.log_softmax(ref.logits[0].float(), -1)
        want_lp = np.array([lp[t - 1, p.full[t]].item() for t in range(s, e)], dtype=np.float32)
        got = arrays["code_logprobs"][offs[i]:offs[i + 1]]
        np.testing.assert_allclose(got, want_lp, atol=1e-4)
        assert math.isclose(c.sum_logprob, float(want_lp.sum()), rel_tol=1e-4) and math.isclose(c.min_logprob, float(want_lp.min()), rel_tol=1e-4)
        assert math.isclose(c.mean_logprob, float(want_lp.mean()), rel_tol=1e-4)


def test_final_hidden_state_is_post_norm(model, tok):
    ids = torch.tensor([tok("abc def", add_special_tokens=False)["input_ids"]])
    with torch.no_grad():
        o = model(input_ids=ids, output_hidden_states=True)
    assert torch.allclose(model.lm_head(o.hidden_states[-1]), o.logits, atol=1e-5)


def test_yes_no_logodds_float32_against_manual_computation(cap, model, tok, prob, recs):
    out, arrays = cap.capture(recs[:2], {r.sample_uid: ext(r) for r in recs[:2]}, {prob.problem_id: prob})
    yes = [d["id"] for d in cap.answer_tokens["yes"]]
    no = [d["id"] for d in cap.answer_tokens["no"]]
    assert len(yes) == 2 and len(no) == 3
    for i, r in enumerate(recs[:2]):
        p = cap.prepare(r, prob, ext(r))
        with torch.no_grad():
            h = model(input_ids=torch.tensor([p.full]), output_hidden_states=True).hidden_states[-1][0, p.p3].float()
        logits = h @ model.lm_head.weight.float().T
        want = torch.logsumexp(logits[yes], 0) - torch.logsumexp(logits[no], 0)
        assert abs(out[i].yes_no_logodds - want.item()) < 1e-5
        assert arrays["yes_no_logodds"][i] == np.float32(out[i].yes_no_logodds)
        probs = torch.softmax(logits, 0)
        assert abs(math.log(probs[yes].sum().item()) - math.log(probs[no].sum().item()) - want.item()) < 1e-4


def test_head_is_applied_in_float32_even_for_a_bfloat16_model(model, tok, prompts, prob, recs):
    bf = copy.deepcopy(model).to(torch.bfloat16)
    c = CP.TransformersCapture(bf, tok, prompts, batch_size=2)
    r = recs[0]
    out, _ = c.capture([r], {r.sample_uid: ext(r)}, {prob.problem_id: prob})
    p = c.prepare(r, prob, ext(r))
    with torch.no_grad():
        h = bf(input_ids=torch.tensor([p.full]), output_hidden_states=True).hidden_states[-1][0, p.p3].float()
    W = bf.lm_head.weight.float()
    yes = [d["id"] for d in c.answer_tokens["yes"]]
    no = [d["id"] for d in c.answer_tokens["no"]]
    l = h @ W.T
    want = (torch.logsumexp(l[yes], 0) - torch.logsumexp(l[no], 0)).item()
    assert abs(out[0].yes_no_logodds - want) < 1e-3


def test_failure_sample_records_nan_logprobs_and_mean_over_completion(cap, tok, prob):
    r = T.make_record(tok, prob, T.NOFENCE, j=9)
    out, arrays = cap.capture([r], {r.sample_uid: ext(r, failure="no_block")}, {prob.problem_id: prob})
    c = out[0]
    assert c.n_code_tokens == 0 and math.isnan(c.sum_logprob) and math.isnan(c.min_logprob)
    assert len(arrays["code_logprobs"]) == 0 and torch.isfinite(arrays["hs_mean_code"].float()).all()


@pytest.mark.parametrize("text,want", [
    ("Confidence: 85", 0.85), ("Confidence:7", 0.07), ("Confidence: 150", 1.0), ("Confidence: 999", 1.0),
    ("Sure thing. Confidence: 40", 0.4), ("I think it is likely", None), ("", None), ("Confidence:", None),
    ("Confidence: abc", None), ("confidence: 50", None), ("Confidence: 0", 0.0),
])
def test_parse_v1_cases(text, want):
    assert CP.parse_v1(text) == want


def test_v1_kv_cache_reuse_equals_no_cache_decode(cap, model, tok, prob, recs):
    for r in recs:
        p = cap.prepare(r, prob, ext(r))
        want = cap.v1_ids_nocache(p)
        assert 1 <= len(want) <= C.V1_MAX_NEW_TOKENS
        # cache sliced out of the forward pass
        rows = cap._run_batch([p])
        got = cap.v1_ids(p, rows[0]["cache"])
        assert rows[0]["cache"] is not None and got == want
        # fresh prefill of the prefix, then cache
        assert cap.v1_ids(p, None) == want


def test_v1_cache_reuse_in_a_padded_batch_equals_no_cache_decode(model, tok, prompts, prob, recs):
    for side in ("left", "right"):
        c = CP.TransformersCapture(model, tok, prompts, batch_size=3, padding_side=side)
        preps = [c.prepare(r, prob, ext(r)) for r in recs]
        rows = c._run_batch(preps)
        for p, row in zip(preps, rows):
            assert row["cache"] is not None
            assert c.v1_ids(p, row["cache"]) == c.v1_ids_nocache(p), side


@pytest.mark.parametrize("side", ["left", "right"])
def test_batched_equals_unbatched(model, tok, prompts, prob, recs, side):
    extra = T.make_record(tok, prob, T.NOFENCE, j=7)
    allr = list(recs) + [extra]
    exts = {r.sample_uid: ext(r) for r in recs}
    exts[extra.sample_uid] = ext(extra, failure="no_block")
    probs = {prob.problem_id: prob}
    single = CP.TransformersCapture(model, tok, prompts, batch_size=1, padding_side=side)
    batch = CP.TransformersCapture(model, tok, prompts, batch_size=4, padding_side=side)
    o1, a1 = single.capture(allr, exts, probs)
    o2, a2 = batch.capture(allr, exts, probs)
    assert [c.v1_text for c in o1] == [c.v1_text for c in o2]
    for k in ("hs_p1", "hs_p2", "hs_p3", "hs_mean_code"):
        assert torch.allclose(a1[k].float(), a2[k].float(), atol=2e-2, rtol=2e-2), k
    np.testing.assert_allclose(a1["yes_no_logodds"], a2["yes_no_logodds"], atol=1e-4)
    np.testing.assert_allclose(a1["code_logprobs"], a2["code_logprobs"], atol=1e-4)
    assert (a1["code_logprob_offsets"] == a2["code_logprob_offsets"]).all()
    for c1, c2 in zip(o1, o2):
        assert (c1.p1, c1.p2, c1.p3, c1.code_token_span) == (c2.p1, c2.p2, c2.p3, c2.code_token_span)


def test_rewriting_template_layout_and_thinking_on_elicitation(tok, prompts, prob):
    tk = T.build_tokenizer(T.T_REWRITE)
    m = T.build_model(tk)
    c = CP.TransformersCapture(m, tk, prompts)
    r = T.make_record(tk, prob, "<think>\nhmm\n</think>\n" + T.GOOD, thinking=True)
    lay = c.build_layout(r, prob, ext(r))
    # thinking-on prompt has no empty thought block, but the elicitation turn is rendered thinking-off
    assert not tk.decode(lay.prompt_ids).endswith("</think>\n\n")
    assert tk.decode(lay.elicitation_ids) == ELIC_V2
    s, e = lay.code_span
    full = lay.prompt_ids + lay.completion_ids + lay.elicitation_ids
    assert tk.decode(full[s:e]) == CODE.rstrip("\n")
    # the thought block is not in the code span
    assert "</think>" in tk.decode(full[:s]) and "hmm" not in tk.decode(full[s:e])


def test_base_model_layout(tok, model, prompts, prob):
    c = CP.TransformersCapture(model, tok, prompts, chat=False)
    body = "    return a + b\n"
    r = T.make_record(tok, prob, body, chat=False)
    lay = c.build_layout(r, prob, ExtractionResult(r.sample_uid, prob.prompt + body, "fallback_def", None))
    assert tok.decode(lay.prompt_ids) == prob.prompt
    assert tok.decode(lay.completion_ids) == body
    assert tok.decode(lay.elicitation_ids) == f"\n\nQuestion: {C.V2_TEXT}\nAnswer:"
    assert lay.code_span == (len(lay.prompt_ids), len(lay.prompt_ids) + len(lay.completion_ids))
    out, _ = c.capture([r], {}, {prob.problem_id: prob})
    assert out[0].p3 == len(lay.prompt_ids + lay.completion_ids + lay.elicitation_ids) - 1


def test_hash_mismatch_between_record_and_prompt_is_refused(cap, tok, prob):
    r = T.make_record(tok, prob, T.GOOD)
    bad = type(r)(**{**r.__dict__, "rendered_prompt_sha256": "0" * 64})
    with pytest.raises(ValueError, match="rendered prompt hash"):
        cap.prepare(bad, prob, ext(r))
