"""Generation backends implementing pipeline.contracts.interfaces.GenerationBackend.

    VLLMBackend         pod only; vllm is imported lazily inside the class
    TransformersBackend CPU smoke test; one sample at a time with a per-sample torch.Generator
    MockBackend         deterministic, no model; wrong variants come from reference code (integration test)

All real backends sample at temperature 1.0, top-p 1.0, no top-k, no repetition penalty, stop at end
of turn. A seed is passed to engines as a signed 64-bit integer (two's complement of the unsigned
value from hashing.sample_seed) because vLLM validates seeds as signed longs.
"""

from __future__ import annotations

import contextlib
import random
from typing import Any, Callable, Iterator, Mapping, Sequence

from pipeline.contracts import constants as C
from pipeline.contracts.hashing import sha256_text
from pipeline.contracts.schemas import GenerationRecord, GenerationRequest, sample_uid

from .prompts import (BASE_STOP_STRINGS, PromptSet, encode_prompt, load_prompts, render_prompt)
from .requests import model_spec
from .tokens import align_ids_to_text, derive_turns, stop_token_ids

PINNED_VLLM = "0.33.0"
VLLM_TOP_K_DISABLED = -1        # vLLM accepts -1 (and 0) as "no top-k"; not verified against 0.33.0 here
MOCK_EOT_ID = 0x110000          # one token per Unicode code point; this id is outside that range


def to_engine_seed(seed: int) -> int:
    """Unsigned 64-bit seed to the signed 64-bit integer with the same bits."""
    return seed - (1 << 64) if seed >= (1 << 63) else seed


def build_record(req: GenerationRequest, *, prompts: PromptSet, chat: bool, rendered_sha256: str, text: str,
                 ids: Sequence[int], finish_reason: str, engine: str) -> GenerationRecord:
    return GenerationRecord(
        sample_uid=sample_uid(req.model_key, req.benchmark, req.problem_id, req.sample_index, req.generation_set),
        model_key=req.model_key, model_id=req.model_id, revision=req.revision, benchmark=req.benchmark,
        problem_id=req.problem_id, sample_index=req.sample_index, generation_set=req.generation_set,
        seed=req.seed,
        prompt_sha256=prompts.template_sha256_for_prompt(req.benchmark, req.prompt_text, base=not chat),
        rendered_prompt_sha256=rendered_sha256, completion_text=text,
        completion_token_ids=tuple(int(i) for i in ids), finish_reason=finish_reason,
        truncated=finish_reason == "length", engine=engine, thinking=req.thinking)


# ---------------------------------------------------------------------------------------------------
# Mock
# ---------------------------------------------------------------------------------------------------
GARBAGE_TEXTS = (
    "I am not able to determine a solution without more context about the requirements.",
    "The problem is interesting. One could approach it in several ways, but no code is given here.",
)


def mock_completion_text(code: str) -> str:
    return f"Here is my solution.\n\n```python\n{code}\n```\n"


class MockBackend:
    """Deterministic generation without a model.

    mapping: problem_id -> (correct_code, [wrong variants]). Each request is turned into a correct or
    a wrong variant by a stable draw from its seed, wrapped in a fenced block. garbage_share of the
    requests return text without any fence (extraction failures). p_correct is a float or a mapping
    problem_id -> probability. Token ids are Unicode code points (invertible, no tokenizer needed);
    the end-of-turn id is MOCK_EOT_ID.
    """

    engine = "mock"

    def __init__(self, mapping: Mapping[str, tuple[str, Sequence[str]]], *, p_correct: float | Mapping[str, float] = 0.5,
                 garbage_share: float = 0.0, prompts: PromptSet | None = None):
        self.mapping = dict(mapping)
        self.p_correct = p_correct
        self.garbage_share = garbage_share
        self.prompts = prompts or load_prompts()

    def _p(self, problem_id: str) -> float:
        return self.p_correct.get(problem_id, 0.5) if isinstance(self.p_correct, Mapping) else float(self.p_correct)

    def choose(self, req: GenerationRequest) -> tuple[str, int]:
        """(text, variant) with variant -2 garbage, -1 correct, >= 0 index of the wrong variant."""
        rng = random.Random(req.seed)
        u_garbage, u_correct, pick = rng.random(), rng.random(), rng.random()
        entry = self.mapping.get(req.problem_id)
        if entry is None or u_garbage < self.garbage_share:
            return GARBAGE_TEXTS[int(pick * len(GARBAGE_TEXTS)) % len(GARBAGE_TEXTS)], -2
        correct, wrong = entry
        if u_correct < self._p(req.problem_id) or not wrong:
            return mock_completion_text(correct), -1
        v = int(pick * len(wrong)) % len(wrong)
        return mock_completion_text(wrong[v]), v

    def generate(self, requests: Sequence[GenerationRequest], adapter_path: str | None = None) -> list[GenerationRecord]:
        out = []
        for req in requests:
            text, _ = self.choose(req)
            ids = [ord(ch) for ch in text]
            if len(ids) > req.max_new_tokens:
                ids, text, finish = ids[:req.max_new_tokens], text[:req.max_new_tokens], "length"
            else:
                ids, finish = ids + [MOCK_EOT_ID], "stop"
            out.append(build_record(req, prompts=self.prompts, chat=True, rendered_sha256=sha256_text(req.prompt_text),
                                    text=text, ids=ids, finish_reason=finish, engine=self.engine))
        return out


# ---------------------------------------------------------------------------------------------------
# Transformers (CPU smoke test)
# ---------------------------------------------------------------------------------------------------
class TransformersBackend:
    """One sample at a time, sampled with a torch.Generator seeded from the request seed.

    Own sampling loop (softmax at temperature 1.0, multinomial with the generator): top-p 1.0 and no
    top-k mean no filtering, and the loop does not depend on generate()'s handling of generators.
    """

    def __init__(self, model: Any, tokenizer: Any, *, chat: bool = True, prompts: PromptSet | None = None,
                 stop_ids: Sequence[int] | None = None, stop_strings: Sequence[str] | None = None):
        import transformers
        self.engine = f"transformers=={transformers.__version__}"
        self.model, self.tokenizer, self.chat = model, tokenizer, chat
        self.prompts = prompts or load_prompts()
        if stop_ids is None:
            stop_ids = stop_token_ids(tokenizer, model, derive_turns(tokenizer, self.prompts, chat=chat))
            if not chat and getattr(tokenizer, "eos_token_id", None) is not None:
                stop_ids = (int(tokenizer.eos_token_id),)
        self.stop_ids = tuple(stop_ids)
        self.stop_strings = tuple(stop_strings) if stop_strings is not None else (() if chat else BASE_STOP_STRINGS)

    @contextlib.contextmanager
    def _adapter(self, adapter_path: str | None) -> Iterator[Any]:
        if adapter_path is None:
            yield self.model
            return
        from peft import PeftModel
        pm = PeftModel.from_pretrained(self.model, adapter_path)
        pm.eval()
        try:
            yield pm
        finally:
            pm.unload()          # restore the plain base modules

    def _sample_one(self, model: Any, req: GenerationRequest) -> tuple[str, list[int], str, str]:
        import torch
        tok = self.tokenizer
        rendered = render_prompt(tok, req.prompt_text, chat=self.chat, thinking=req.thinking)
        prompt_ids = encode_prompt(tok, rendered, chat=self.chat)
        device = next(model.parameters()).device
        gen = torch.Generator(device="cpu")
        gen.manual_seed(to_engine_seed(req.seed))
        ids: list[int] = []
        finish = "length"
        with torch.inference_mode():
            out = model(input_ids=torch.tensor([prompt_ids], device=device), use_cache=True)
            past, logits = out.past_key_values, out.logits[0, -1]
            for _ in range(req.max_new_tokens):
                probs = torch.softmax(logits.float() / C.TEMPERATURE, dim=-1).cpu()
                t = int(torch.multinomial(probs, 1, generator=gen).item())
                ids.append(t)
                if t in self.stop_ids:
                    finish = "stop"
                    break
                if self.stop_strings and any(s in decode_tail(tok, ids) for s in self.stop_strings):
                    finish = "stop"
                    break
                out = model(input_ids=torch.tensor([[t]], device=device), past_key_values=past, use_cache=True)
                past, logits = out.past_key_values, out.logits[0, -1]
        body = ids[:-1] if ids and ids[-1] in self.stop_ids else ids
        text = tok.decode(body, skip_special_tokens=True, clean_up_tokenization_spaces=False)
        if self.stop_strings:
            cut = min((i for i in (text.find(s) for s in self.stop_strings) if i >= 0), default=-1)
            if cut >= 0:
                text = text[:cut]
                ids = align_ids_to_text(tok, ids, text)
        return text, ids, finish, rendered.sha256

    def generate(self, requests: Sequence[GenerationRequest], adapter_path: str | None = None) -> list[GenerationRecord]:
        out: list[GenerationRecord] = []
        with self._adapter(adapter_path) as model:
            for req in requests:
                text, ids, finish, rsha = self._sample_one(model, req)
                out.append(build_record(req, prompts=self.prompts, chat=self.chat, rendered_sha256=rsha, text=text,
                                        ids=ids, finish_reason=finish, engine=self.engine))
        return out


def decode_tail(tokenizer: Any, ids: Sequence[int], n: int = 8) -> str:
    return tokenizer.decode(list(ids[-n:]), skip_special_tokens=False, clean_up_tokenization_spaces=False)


# ---------------------------------------------------------------------------------------------------
# vLLM (pod only)
# ---------------------------------------------------------------------------------------------------
class VLLMBackend:
    """vLLM 0.33.0 engine. Pod only: vllm is imported inside __init__ and generate, never at module
    import, so this Mac never imports it.

    Sampling: temperature 1.0, top-p 1.0, top-k disabled, no repetition penalty, per-request seed,
    max_tokens per request, stop at the end-of-turn token (and the EvalPlus-style stop strings for
    base models). Prefix caching is on. generation_config="vllm" so the model card's recommended
    sampling settings are not used (design 5). A LoRA adapter is applied per call through a LoRARequest.
    """

    def __init__(self, model_id: str, revision: str, *, chat: bool = True, hf_cache: str | None = None,
                 prompts: PromptSet | None = None, tokenizer: Any | None = None, dtype: str = "bfloat16",
                 gpu_memory_utilization: float = 0.90, max_model_len: int | None = None,
                 tensor_parallel_size: int = 1, enable_lora: bool = False, llm_factory: Callable[..., Any] | None = None):
        import vllm   # lazy: pod only
        if vllm.__version__ != PINNED_VLLM:
            raise RuntimeError(f"vllm=={vllm.__version__} installed; the design pins {PINNED_VLLM}")
        self.engine = f"vllm=={vllm.__version__}"
        self.chat, self.prompts = chat, prompts or load_prompts()
        if tokenizer is None:
            from transformers import AutoTokenizer
            tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision, cache_dir=hf_cache)
        self.tokenizer = tokenizer
        spec = derive_turns(tokenizer, self.prompts, chat=chat)
        self.stop_ids = stop_token_ids(tokenizer, None, spec)
        self.stop_strings = () if chat else BASE_STOP_STRINGS
        kwargs: dict[str, Any] = dict(model=model_id, revision=revision, tokenizer=model_id, tokenizer_revision=revision,
                                      dtype=dtype, download_dir=hf_cache, enable_prefix_caching=True,
                                      gpu_memory_utilization=gpu_memory_utilization, tensor_parallel_size=tensor_parallel_size,
                                      generation_config="vllm", seed=0)
        if max_model_len:
            kwargs["max_model_len"] = max_model_len
        if enable_lora:
            kwargs.update(enable_lora=True, max_lora_rank=C.LORA_RANK)
        self.llm = (llm_factory or vllm.LLM)(**kwargs)
        self._adapter_ids: dict[str, int] = {}

    def generate(self, requests: Sequence[GenerationRequest], adapter_path: str | None = None) -> list[GenerationRecord]:
        from vllm import SamplingParams   # lazy
        rendered, prompt_inputs, params = [], [], []
        for req in requests:
            r = render_prompt(self.tokenizer, req.prompt_text, chat=self.chat, thinking=req.thinking)
            rendered.append(r)
            prompt_inputs.append({"prompt_token_ids": encode_prompt(self.tokenizer, r, chat=self.chat)})
            params.append(SamplingParams(
                n=1, temperature=C.TEMPERATURE, top_p=C.TOP_P, top_k=VLLM_TOP_K_DISABLED, repetition_penalty=1.0,
                seed=to_engine_seed(req.seed), max_tokens=req.max_new_tokens,
                stop=list(self.stop_strings) or None, stop_token_ids=list(self.stop_ids), skip_special_tokens=True))
        lora = None
        if adapter_path is not None:
            from vllm.lora.request import LoRARequest   # lazy
            aid = self._adapter_ids.setdefault(adapter_path, len(self._adapter_ids) + 1)
            lora = LoRARequest(f"adapter-{aid}", aid, adapter_path)
        outputs = self.llm.generate(prompt_inputs, sampling_params=params, lora_request=lora)
        records = []
        for req, r, o in zip(requests, rendered, outputs):
            c = o.outputs[0]
            ids, text = list(c.token_ids), c.text
            if self.stop_strings and isinstance(getattr(c, "stop_reason", None), str):
                ids = align_ids_to_text(self.tokenizer, ids, text)
            finish = "length" if c.finish_reason == "length" else "stop"
            records.append(build_record(req, prompts=self.prompts, chat=self.chat, rendered_sha256=r.sha256, text=text,
                                        ids=ids, finish_reason=finish, engine=self.engine))
        return records
