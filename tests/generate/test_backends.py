import subprocess
import sys
import types

import numpy as np
import pytest
import torch

from pipeline.contracts import constants as C
from pipeline.contracts.hashing import sha256_text
from pipeline.contracts.schemas import GenerationRequest
from pipeline.generate import backends as B
from pipeline.generate import capture as CP
from pipeline.generate import requests as R
from pipeline.generate import stage as S
from pipeline.generate.prompts import render_prompt
from pipeline.generate.tokens import extract_fallback

import gen_tinylm as T


def _problems(n=4):
    return [T.problem(f"HumanEval/{i}") for i in range(n)]


def _req(prompts, j=1, pid="HumanEval/0", max_new=10):
    r = R.build_requests("SMOKE", [T.problem(pid)], j, prompts=prompts)[-1]
    return GenerationRequest(**{**r.__dict__, "max_new_tokens": max_new})


# ---- mock ---------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def mapping():
    return S.mock_mapping(_problems(6))


def test_mock_variants_come_from_reference_code(mapping):
    correct, wrong = mapping["HumanEval/0"]
    assert correct == 'def add(a, b):\n    """Add two numbers."""\n    return a + b'
    assert len(wrong) >= 3 and len(set(wrong)) == len(wrong) and correct not in wrong
    assert wrong[0].endswith("return None") and "raise RuntimeError" in wrong[-1]


def test_mock_backend_is_deterministic_and_mixes_outcomes(prompts, mapping):
    be = B.MockBackend(mapping, p_correct=0.5, garbage_share=0.2, prompts=prompts)
    reqs = R.build_requests("MOCK", _problems(6), 10, prompts=prompts)
    a, b = be.generate(reqs), be.generate(reqs)
    assert a == b and len(a) == 60
    assert B.MockBackend(mapping, p_correct=0.5, garbage_share=0.2, prompts=prompts).generate(reqs) == a
    kinds = [be.choose(r)[1] for r in reqs]
    assert -1 in kinds and -2 in kinds and any(k >= 0 for k in kinds)
    for rec, k in zip(a, kinds):
        assert rec.engine == "mock" and rec.finish_reason == "stop" and not rec.truncated
        assert ("```python" in rec.completion_text) == (k != -2)
        assert rec.completion_token_ids[-1] == B.MOCK_EOT_ID
        assert "".join(chr(t) for t in rec.completion_token_ids[:-1]) == rec.completion_text


def test_mock_backend_truncation_and_unknown_problem(prompts, mapping):
    be = B.MockBackend(mapping, p_correct=1.0, prompts=prompts)
    r = R.build_requests("MOCK", _problems(1), 1, prompts=prompts)[0]
    short = GenerationRequest(**{**r.__dict__, "max_new_tokens": 12})
    rec = be.generate([short])[0]
    assert rec.truncated and rec.finish_reason == "length" and len(rec.completion_token_ids) == 12
    unknown = GenerationRequest(**{**r.__dict__, "problem_id": "HumanEval/99"})
    assert "```" not in be.generate([unknown])[0].completion_text


def _code(rec):
    return extract_fallback(rec.sample_uid, rec.completion_text, "add", False, use_execute=False)[0]


def test_mock_capture_has_signal_and_recoverable_labels(prompts, mapping):
    probs = {p.problem_id: p for p in _problems(6)}
    be = B.MockBackend(mapping, p_correct=0.5, garbage_share=0.1, prompts=prompts)
    recs = be.generate(R.build_requests("MOCK", list(probs.values()), 10, prompts=prompts))
    mc = CP.MockCapture(mapping, n_layers=8, hidden=16, prompts=prompts)
    out, arr = mc.capture(recs, {}, probs)
    assert arr["hs_p2"].shape == (60, 7, 16) and arr["hs_p2"].dtype == torch.bfloat16
    y = np.array([mc.label(r, _code(r)) for r in recs])
    assert 5 < y.sum() < 55
    yn = arr["yes_no_logodds"]
    assert yn[y == 1].mean() - yn[y == 0].mean() > 1.5
    d = np.random.default_rng(12345).normal(size=16)
    proj = (arr["hs_p2"].float().numpy() @ (d / np.linalg.norm(d))).mean(1)
    assert proj[y == 1].mean() > proj[y == 0].mean() + 0.8
    assert any(c.v1_value is None for c in out) and any(c.v1_value is not None for c in out)
    assert [repr(c) for c in out] == [repr(c) for c in mc.capture(recs, {}, probs)[0]]     # deterministic (NaN-safe)
    bad = [c for c, r in zip(out, recs) if "```" not in r.completion_text]
    assert bad and all(c.n_code_tokens == 0 and np.isnan(c.sum_logprob) for c in bad)


# ---- transformers ---------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def tb(model, tok, prompts):
    return B.TransformersBackend(model, tok, prompts=prompts, stop_ids=())


def test_transformers_backend_is_seeded_and_batch_independent(tb, prompts, tok):
    r1, r2 = _req(prompts, 1), _req(prompts, 2)
    a = tb.generate([r1, r2])
    b = tb.generate([r2])
    assert a[1] == b[0] and a[0] == tb.generate([r1])[0]
    assert a[0].completion_token_ids != a[1].completion_token_ids
    rec = a[0]
    assert rec.finish_reason == "length" and rec.truncated and len(rec.completion_token_ids) == 10
    assert rec.engine.startswith("transformers==") and rec.model_key == "SMOKE" and rec.seed == r1.seed
    assert rec.sample_uid == f"SMOKE|frozen|humaneval_plus|HumanEval/0|{r1.sample_index}"
    rendered = render_prompt(tok, r1.prompt_text, chat=True, thinking=False)
    assert rec.rendered_prompt_sha256 == sha256_text(rendered.text)
    assert rec.prompt_sha256 == prompts.template_sha256("payload_function.txt", base=False)
    assert rec.completion_text == tok.decode(rec.completion_token_ids, skip_special_tokens=True)


def test_transformers_backend_stops_at_end_of_turn(model, tok, prompts):
    eots = tuple(range(0, 120))
    be = B.TransformersBackend(model, tok, prompts=prompts, stop_ids=eots)
    rec = be.generate([_req(prompts, 1, max_new=300)])[0]
    assert rec.finish_reason == "stop" and not rec.truncated
    assert rec.completion_token_ids[-1] in eots and not any(t in eots for t in rec.completion_token_ids[:-1])
    assert rec.completion_text == tok.decode(rec.completion_token_ids[:-1], skip_special_tokens=True)


def test_sampling_follows_the_softmax_at_temperature_one(model, tok, prompts):
    r = _req(prompts, 3, max_new=1)
    be = B.TransformersBackend(model, tok, prompts=prompts, stop_ids=())
    rec = be.generate([r])[0]
    ids = tok(render_prompt(tok, r.prompt_text, chat=True, thinking=False).text, add_special_tokens=False)["input_ids"]
    with torch.no_grad():
        logits = model(input_ids=torch.tensor([ids])).logits[0, -1]
    g = torch.Generator().manual_seed(B.to_engine_seed(r.seed))
    want = int(torch.multinomial(torch.softmax(logits, -1), 1, generator=g))
    assert rec.completion_token_ids == (want,)


def test_peft_adapter_generation_and_clean_unload(model, tok, prompts, tmp_path):
    from peft import LoraConfig, get_peft_model
    donor = get_peft_model(T.build_model(tok, seed=0), LoraConfig(r=4, lora_alpha=64, target_modules=["q_proj", "v_proj", "o_proj", "down_proj"]))
    with torch.no_grad():
        for n, p in donor.named_parameters():
            if "lora_B" in n:
                p.normal_(0, 8.0)
    donor.save_pretrained(tmp_path / "ad")
    be = B.TransformersBackend(model, tok, prompts=prompts, stop_ids=())
    reqs = [_req(prompts, j, max_new=12) for j in (1, 2)]
    base = be.generate(reqs)
    with_ad = be.generate(reqs, adapter_path=str(tmp_path / "ad"))
    assert [r.completion_token_ids for r in base] != [r.completion_token_ids for r in with_ad]
    assert not any("lora" in n for n, _ in model.named_modules())     # adapter removed
    assert be.generate(reqs) == base                                  # base weights restored exactly
    assert with_ad == be.generate(reqs, adapter_path=str(tmp_path / "ad"))


# ---- vLLM (stubbed engine; the real engine is pod only) ---------------------------------------------------
class _Out:
    def __init__(self, text, ids, finish, stop_reason=None):
        self.outputs = [types.SimpleNamespace(text=text, token_ids=ids, finish_reason=finish, stop_reason=stop_reason)]


def _install_stub(monkeypatch, version="0.33.0"):
    calls = {}

    class SamplingParams:
        def __init__(self, **kw):
            self.kw = kw

    class LLM:
        def __init__(self, **kw):
            calls["llm"] = kw

        def generate(self, prompts, sampling_params=None, lora_request=None):
            calls["generate"] = (prompts, sampling_params, lora_request)
            return [_Out("def f(): pass", [5, 6, 7, 258], "stop") for _ in prompts]

    class LoRARequest:
        def __init__(self, name, i, path):
            self.args = (name, i, path)

    mod = types.ModuleType("vllm")
    mod.__version__, mod.LLM, mod.SamplingParams = version, LLM, SamplingParams
    lora = types.ModuleType("vllm.lora")
    req = types.ModuleType("vllm.lora.request")
    req.LoRARequest = LoRARequest
    for name, m in (("vllm", mod), ("vllm.lora", lora), ("vllm.lora.request", req)):
        monkeypatch.setitem(sys.modules, name, m)
    return calls


def test_vllm_backend_settings(monkeypatch, tok, prompts):
    calls = _install_stub(monkeypatch)
    be = B.VLLMBackend("org/m", "rev123", tokenizer=tok, prompts=prompts, hf_cache="cache", enable_lora=True)
    assert be.engine == "vllm==0.33.0"
    kw = calls["llm"]
    assert kw["enable_prefix_caching"] is True and kw["revision"] == "rev123" and kw["generation_config"] == "vllm"
    assert kw["enable_lora"] is True and kw["max_lora_rank"] == C.LORA_RANK
    reqs = [_req(prompts, 1, max_new=33), _req(prompts, 2, max_new=33)]
    recs = be.generate(reqs)
    prompts_in, params, lora = calls["generate"]
    assert lora is None and len(params) == 2
    for req, p, pi in zip(reqs, params, prompts_in):
        k = p.kw
        assert (k["temperature"], k["top_p"], k["top_k"], k["repetition_penalty"]) == (1.0, 1.0, -1, 1.0)
        assert k["max_tokens"] == 33 and k["seed"] == B.to_engine_seed(req.seed) and -2**63 <= k["seed"] < 2**63
        assert be.stop_ids and set(be.stop_ids) <= set(k["stop_token_ids"]) and k["stop"] is None
        assert pi["prompt_token_ids"] == tok(render_prompt(tok, req.prompt_text, chat=True, thinking=False).text,
                                             add_special_tokens=False)["input_ids"]
    assert recs[0].engine == "vllm==0.33.0" and recs[0].finish_reason == "stop"
    assert recs[0].completion_token_ids == (5, 6, 7, 258)
    be.generate(reqs[:1], adapter_path="/some/adapter")
    assert calls["generate"][2].args[2] == "/some/adapter"


def test_vllm_version_pin_and_lazy_import(monkeypatch, tok, prompts):
    _install_stub(monkeypatch, version="0.99.0")
    with pytest.raises(RuntimeError, match="0.33.0"):
        B.VLLMBackend("org/m", "rev", tokenizer=tok, prompts=prompts)
    out = subprocess.run([sys.executable, "-c", "import sys, pipeline.generate.backends, pipeline.generate.stage; "
                          "assert 'vllm' not in sys.modules"], capture_output=True, text=True)
    assert out.returncode == 0, out.stderr


def test_engine_seed_is_signed_64_bit():
    assert B.to_engine_seed(5) == 5 and B.to_engine_seed(2**64 - 1) == -1 and B.to_engine_seed(2**63) == -2**63
    assert (B.to_engine_seed(2**63 + 7) & (2**64 - 1)) == 2**63 + 7
