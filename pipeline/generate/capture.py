"""Capture: the single teacher-forced pass per sample and the V1 greedy decode (design 5, 7.6, 7.12).

TransformersCapture builds the TeacherForcedLayout of each sample, runs one forward pass over
[prompt, completion, V2 elicitation turn] with output_hidden_states=True, and reads:
    * code-token log-probs: log-softmax of the previous position's logits, from the final-norm hidden
      state through the model's output head (model dtype, upcast to float32);
    * hidden states at layer indices floor(f * n_layers), f in LAYER_FRACTIONS (index into the
      hidden_states tuple, 0 = embeddings) at p1, p2, p3 and the mean over code tokens, as bfloat16;
    * the Yes/No log-odds at p3: float32 final hidden state through the float32 output-head rows of
      the Yes and No token sets, log-sum-exp difference.
V1 is a greedy decode of up to 8 tokens after [prompt, completion, bridge, V1 turn] from the KV cache of
the prefix (the cache of the same forward pass, sliced per row; or a fresh prefill of the prefix).

Divergences from the layout description are listed in pipeline/generate/CONTRACT_REQUESTS.md.
"""

from __future__ import annotations

import hashlib
import math
import re
import time
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

import numpy as np

from pipeline.contracts import constants as C
from pipeline.contracts.interfaces import TeacherForcedLayout
from pipeline.contracts.schemas import (CaptureRecord, ExtractionResult, GenerationRecord, HiddenStateRef,
                                        Problem)

from .prompts import PromptSet, apply_chat, encode_prompt, load_prompts, render_prompt
from .tokens import (TurnSpec, answer_token_variants, char_span_to_token_span, decode_ids, derive_turns,
                     extract_fallback, locate_code, stop_token_ids, strip_range)

_V1 = re.compile(C.V1_REGEX)


def layer_indices(n_layers: int, fractions: Sequence[float] = C.LAYER_FRACTIONS) -> tuple[int, ...]:
    """Index into the hidden_states tuple (0 = embeddings) for each depth fraction, rounded down."""
    return tuple(int(math.floor(f * n_layers)) for f in fractions)


def parse_v1(text: str) -> float | None:
    """Section 7.2: first match of V1_REGEX anywhere in the text, clipped to [0, 100], divided by 100."""
    m = _V1.search(text)
    if not m:
        return None
    return min(max(int(m.group(1)), 0), 100) / 100.0


# ---------------------------------------------------------------------------------------------------
# Per-sample preparation
# ---------------------------------------------------------------------------------------------------
@dataclass
class Prepared:
    record: GenerationRecord
    layout: TeacherForcedLayout
    prefix_len: int                 # prompt + completion (with end-of-turn and bridge)
    full: list[int]
    p2: int
    mean_span: tuple[int, int]
    failure: bool                   # no code span (extraction failure or location failure)
    notes: list[str] = field(default_factory=list)

    @property
    def p1(self) -> int:
        return self.layout.p1

    @property
    def p3(self) -> int:
        return self.layout.p3


class TransformersCapture:
    """CaptureBackend on a transformers causal LM (CPU float32 in tests, CUDA bfloat16 on the pod)."""

    def __init__(self, model: Any, tokenizer: Any, prompts: PromptSet | None = None, *, chat: bool = True,
                 batch_size: int = 4, padding_side: str = "left", v1_mode: str = "reuse", strict: bool = False):
        if padding_side not in ("left", "right"):
            raise ValueError("padding_side must be left or right")
        if v1_mode not in ("reuse", "prefill"):
            raise ValueError("v1_mode must be reuse or prefill")
        import torch
        self.torch = torch
        self.model, self.tokenizer, self.chat = model, tokenizer, chat
        self.prompts = prompts or load_prompts()
        self.batch_size, self.padding_side, self.v1_mode, self.strict = batch_size, padding_side, v1_mode, strict
        self.device = next(model.parameters()).device
        self.spec: TurnSpec = derive_turns(tokenizer, self.prompts, chat=chat)
        self.stop_ids = set(stop_token_ids(tokenizer, model, self.spec))
        if not chat and getattr(tokenizer, "eos_token_id", None) is not None:
            self.stop_ids = {int(tokenizer.eos_token_id)}
        text_cfg = model.config.get_text_config()
        self.n_layers = int(text_cfg.num_hidden_layers)
        self.layers = layer_indices(self.n_layers)
        self.softcap = getattr(text_cfg, "final_logit_softcapping", None)
        self.answer_tokens = answer_token_variants(tokenizer)
        self.pad_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else (tokenizer.eos_token_id or 0)
        self._yn_rows: tuple[Any, Any, Any, Any] | None = None
        self.stats: dict[str, float] = {}
        self.notes: list[str] = []

    # ---- layout --------------------------------------------------------------------------------
    def prepare(self, record: GenerationRecord, problem: Problem, extraction: ExtractionResult | None) -> Prepared:
        tok = self.tokenizer
        text = self.prompts.generation_prompt_text(problem, base=not self.chat)
        rendered = render_prompt(tok, text, chat=self.chat, thinking=record.thinking)
        if rendered.sha256 != record.rendered_prompt_sha256:
            raise ValueError(f"{record.sample_uid}: rendered prompt hash differs from the generation record")
        prompt_ids = encode_prompt(tok, rendered, chat=self.chat)
        gen_ids = [int(i) for i in record.completion_token_ids]
        notes: list[str] = []
        if self.chat:
            has_stop = bool(gen_ids) and gen_ids[-1] in self.stop_ids
            core = gen_ids[:-1] if has_stop else gen_ids
            comp = list(gen_ids)
            if record.finish_reason == "stop":
                if not has_stop and self.spec.eot_id is not None:
                    comp.append(int(self.spec.eot_id))
                comp.extend(self.spec.bridge_ids)
        else:
            core = list(gen_ids)
            while core and core[-1] in self.stop_ids:
                core.pop()
            comp = list(core)
        elic = list(self.spec.elicitation_ids["V2"])
        off = len(prompt_ids)
        # code span
        uid = record.sample_uid
        if extraction is None:
            code, failure = extract_fallback(uid, record.completion_text, problem.entry_point, record.truncated)
        else:
            code, failure = extraction.code, extraction.failure
        span: tuple[int, int] | None = None
        if code is not None and core:
            if not self.chat:
                span = (0, len(core))
            else:
                decoded = decode_ids(tok, core)
                loc = locate_code(decoded, code)
                rng = strip_range(decoded, *loc) if loc else None
                span = char_span_to_token_span(tok, core, *rng) if rng else None
                if span is None:
                    notes.append("code_locate_failed")
        if span is None:
            p2 = off + max(len(core), 1) - 1 if core else off - 1
            code_span = (p2 + 1, p2 + 1)
            mean_span = (off, off + len(core)) if core else (off - 1, off)
            fail = True
        else:
            code_span = (off + span[0], off + span[1])
            p2 = code_span[1] - 1
            mean_span = code_span
            fail = False
        layout = TeacherForcedLayout(prompt_ids=tuple(prompt_ids), completion_ids=tuple(comp),
                                     elicitation_ids=tuple(elic), code_span=code_span)
        full = list(prompt_ids) + comp + elic
        prep = Prepared(record=record, layout=layout, prefix_len=off + len(comp), full=full, p2=p2,
                        mean_span=mean_span, failure=fail, notes=notes)
        if self.strict and self.chat and self.spec.prefix_identity and record.finish_reason == "stop":
            self._verify_identity(prep, text, record)
        return prep

    def build_layout(self, record: GenerationRecord, problem: Problem, extraction: ExtractionResult | None = None
                     ) -> TeacherForcedLayout:
        return self.prepare(record, problem, extraction).layout

    def _verify_identity(self, prep: Prepared, user_text: str, record: GenerationRecord) -> None:
        full = apply_chat(self.tokenizer, [{"role": "user", "content": user_text},
                                           {"role": "assistant", "content": record.completion_text},
                                           {"role": "user", "content": self.prompts.elicit_text("V2")}],
                          add_generation_prompt=True, thinking=False)
        ids = self.tokenizer(full, add_special_tokens=False)["input_ids"]
        if list(ids[:len(prep.layout.prompt_ids) + len(prep.layout.completion_ids)]) != \
                list(prep.layout.prompt_ids) + list(prep.layout.completion_ids):
            raise AssertionError(f"{record.sample_uid}: full-conversation prefix differs from prompt + completion ids")
        if list(ids) != prep.full:
            raise AssertionError(f"{record.sample_uid}: full-conversation render differs from the layout")

    # ---- model helpers ---------------------------------------------------------------------------
    def _cap(self, logits):
        return logits if not self.softcap else self.torch.tanh(logits / self.softcap) * self.softcap

    def _head_logprobs(self, h, target_ids):
        torch = self.torch
        emb = self.model.get_output_embeddings()
        logits = self._cap(emb(h.to(emb.weight.dtype)).float())
        lp = torch.log_softmax(logits, dim=-1)
        return lp.gather(-1, target_ids.unsqueeze(-1)).squeeze(-1)

    def _yes_no_rows(self):
        if self._yn_rows is None:
            torch = self.torch
            emb = self.model.get_output_embeddings()
            yes = torch.tensor([d["id"] for d in self.answer_tokens["yes"]], device=self.device)
            no = torch.tensor([d["id"] for d in self.answer_tokens["no"]], device=self.device)
            w = emb.weight.detach()
            b = getattr(emb, "bias", None)
            self._yn_rows = (w[yes].float(), w[no].float(),
                             None if b is None else b.detach()[yes].float(), None if b is None else b.detach()[no].float())
        return self._yn_rows

    def yes_no_logodds(self, h_final):
        """float32 log P(Yes set) - log P(No set) from a final hidden state (any dtype, upcast here)."""
        torch = self.torch
        wy, wn, by, bn = self._yes_no_rows()
        h = h_final.float()
        ly, ln = h @ wy.T, h @ wn.T
        if by is not None:
            ly, ln = ly + by, ln + bn
        ly, ln = self._cap(ly), self._cap(ln)
        return (torch.logsumexp(ly, dim=-1) - torch.logsumexp(ln, dim=-1))

    # ---- forward ---------------------------------------------------------------------------------
    def _pad_batch(self, preps: Sequence[Prepared]):
        torch = self.torch
        B, T = len(preps), max(len(p.full) for p in preps)
        ids = torch.full((B, T), int(self.pad_id), dtype=torch.long)
        attn = torch.zeros((B, T), dtype=torch.long)
        pos = torch.zeros((B, T), dtype=torch.long)
        offs = []
        for b, p in enumerate(preps):
            n = len(p.full)
            o = T - n if self.padding_side == "left" else 0
            offs.append(o)
            ids[b, o:o + n] = torch.tensor(p.full)
            attn[b, o:o + n] = 1
            pos[b, o:o + n] = torch.arange(n)
        return ids.to(self.device), attn.to(self.device), pos.to(self.device), offs

    def _forward(self, **kw):
        try:
            return self.model(logits_to_keep=1, **kw)
        except TypeError:
            return self.model(**kw)

    def _run_batch(self, preps: Sequence[Prepared]) -> list[dict[str, Any]]:
        torch = self.torch
        ids, attn, pos, offs = self._pad_batch(preps)
        with torch.inference_mode():
            out = self._forward(input_ids=ids, attention_mask=attn, position_ids=pos, output_hidden_states=True,
                                use_cache=self.v1_mode == "reuse")
            hs = out.hidden_states
            final = hs[-1]
            rows = []
            for b, p in enumerate(preps):
                o = offs[b]
                at = lambda q: torch.stack([hs[l][b, o + q] for l in self.layers]).to(torch.bfloat16)  # noqa: E731
                s, e = p.mean_span
                mean = torch.stack([hs[l][b, o + s:o + e].float().mean(0) for l in self.layers]).to(torch.bfloat16)
                cs, ce = p.layout.code_span
                if ce > cs:
                    tgt = torch.tensor(p.full[cs:ce], device=self.device)
                    lp = self._head_logprobs(final[b, o + cs - 1:o + ce - 1], tgt).float().cpu().numpy()
                else:
                    lp = np.zeros(0, dtype=np.float32)
                yn = self.yes_no_logodds(final[b, o + p.p3]).float().cpu().item()
                cache = None
                if self.v1_mode == "reuse":
                    cache = self._row_cache(out.past_key_values, b, o, p.prefix_len)
                rows.append({"p1": at(p.p1), "p2": at(p.p2), "p3": at(p.p3), "mean": mean, "lp": lp.astype(np.float32),
                             "yn": yn, "cache": cache})
        return rows

    def _row_cache(self, cache: Any, b: int, off: int, length: int):
        from transformers import DynamicCache
        new = DynamicCache()
        try:
            for li, layer in enumerate(cache.layers):
                if getattr(layer, "is_sliding", False) or not hasattr(layer, "keys"):
                    return None
                new.update(layer.keys[b:b + 1, :, off:off + length].contiguous(),
                           layer.values[b:b + 1, :, off:off + length].contiguous(), li)
        except Exception:
            return None
        return new

    # ---- V1 --------------------------------------------------------------------------------------
    def _greedy(self, cache: Any, new_ids: Sequence[int]) -> list[int]:
        torch = self.torch
        gen: list[int] = []
        with torch.inference_mode():
            out = self.model(input_ids=torch.tensor([list(new_ids)], device=self.device), past_key_values=cache, use_cache=True)
            for step in range(C.V1_MAX_NEW_TOKENS):
                t = int(out.logits[0, -1].argmax().item())
                gen.append(t)
                if t in self.stop_ids or step == C.V1_MAX_NEW_TOKENS - 1:
                    break
                out = self.model(input_ids=torch.tensor([[t]], device=self.device), past_key_values=out.past_key_values,
                                 use_cache=True)
        return gen

    def v1_ids(self, prep: Prepared, cache: Any | None) -> list[int]:
        """Greedy V1 token ids. cache covers the prefix (prompt + completion + bridge) or is None, in
        which case the prefix is prefilled here."""
        torch = self.torch
        v1 = list(self.spec.elicitation_ids["V1"])
        if cache is None:
            with torch.inference_mode():
                out = self.model(input_ids=torch.tensor([prep.full[:prep.prefix_len]], device=self.device), use_cache=True)
            cache = out.past_key_values
            if self.v1_mode == "reuse":
                self.stats["v1_cache_fallbacks"] = self.stats.get("v1_cache_fallbacks", 0) + 1
        return self._greedy(cache, v1)

    def v1_ids_nocache(self, prep: Prepared) -> list[int]:
        """Reference decode without any KV cache: the full sequence is re-run for every new token."""
        torch = self.torch
        seq = prep.full[:prep.prefix_len] + list(self.spec.elicitation_ids["V1"])
        gen: list[int] = []
        with torch.inference_mode():
            for step in range(C.V1_MAX_NEW_TOKENS):
                logits = self.model(input_ids=torch.tensor([seq + gen], device=self.device), use_cache=False).logits
                t = int(logits[0, -1].argmax().item())
                gen.append(t)
                if t in self.stop_ids:
                    break
        return gen

    def v1_text(self, gen: Sequence[int]) -> str:
        body = [t for t in gen if t not in self.stop_ids]
        return self.tokenizer.decode(body, skip_special_tokens=True, clean_up_tokenization_spaces=False)

    # ---- CaptureBackend --------------------------------------------------------------------------
    def capture(self, records: Sequence[GenerationRecord], extractions: Mapping[str, ExtractionResult],
                problems: Mapping[str, Problem]) -> tuple[list[CaptureRecord], dict[str, Any]]:
        torch = self.torch
        t0 = time.time()
        preps = [self.prepare(r, problems[r.problem_id], extractions.get(r.sample_uid)) for r in records]
        order = sorted(range(len(preps)), key=lambda i: len(preps[i].full))
        results: list[dict[str, Any] | None] = [None] * len(preps)
        for k in range(0, len(order), self.batch_size):
            idx = order[k:k + self.batch_size]
            rows = self._run_batch([preps[i] for i in idx])
            for i, row in zip(idx, rows):
                gen = self.v1_ids(preps[i], row.pop("cache"))
                row["v1_text"] = self.v1_text(gen)
                results[i] = row
        out_recs: list[CaptureRecord] = []
        n, L = len(preps), len(self.layers)
        D = int(self.model.config.get_text_config().hidden_size)
        arrays: dict[str, Any] = {k: torch.zeros((n, L, D), dtype=torch.bfloat16) for k in ("hs_p1", "hs_p2", "hs_p3", "hs_mean_code")}
        yn = np.zeros(n, dtype=np.float32)
        lps, offsets = [], [0]
        for i, (p, r) in enumerate(zip(preps, results)):
            assert r is not None
            arrays["hs_p1"][i], arrays["hs_p2"][i] = r["p1"].cpu(), r["p2"].cpu()
            arrays["hs_p3"][i], arrays["hs_mean_code"][i] = r["p3"].cpu(), r["mean"].cpu()
            yn[i] = r["yn"]
            lp = r["lp"] if not p.failure else np.zeros(0, dtype=np.float32)
            lps.append(lp)
            offsets.append(offsets[-1] + len(lp))
            v1 = parse_v1(r["v1_text"])
            out_recs.append(CaptureRecord(
                sample_uid=p.record.sample_uid, hidden=HiddenStateRef(shard_file="", row=i, layers=tuple(self.layers)),
                n_code_tokens=int(len(lp)), code_token_span=tuple(p.layout.code_span), p1=p.p1, p2=p.p2, p3=p.p3,
                elicitation_span=tuple(p.layout.elicitation_span), yes_no_logodds=float(yn[i]),
                v1_text=r["v1_text"], v1_value=v1,
                sum_logprob=float(lp.sum()) if len(lp) else float("nan"),
                mean_logprob=float(lp.mean()) if len(lp) else float("nan"),
                min_logprob=float(lp.min()) if len(lp) else float("nan")))
        arrays["yes_no_logodds"] = yn
        arrays["code_logprobs"] = np.concatenate(lps).astype(np.float32) if lps else np.zeros(0, np.float32)
        arrays["code_logprob_offsets"] = np.asarray(offsets, dtype=np.int64)
        s = self.stats
        s["samples"] = s.get("samples", 0) + n
        s["tokens"] = s.get("tokens", 0) + sum(len(p.full) for p in preps)
        s["seconds"] = s.get("seconds", 0.0) + time.time() - t0
        s["failure_path"] = s.get("failure_path", 0) + sum(p.failure for p in preps)
        s["code_locate_failed"] = s.get("code_locate_failed", 0) + sum("code_locate_failed" in p.notes for p in preps)
        s["v1_unparsed"] = s.get("v1_unparsed", 0) + sum(r.v1_value is None for r in out_recs)
        return out_recs, arrays


# ---------------------------------------------------------------------------------------------------
# Mock capture
# ---------------------------------------------------------------------------------------------------
GARBAGE_V1 = ("I think it is probably fine", "Hard to say.", "Confidence maybe high", "")


class MockCapture:
    """Deterministic synthetic states for the integration test. The label is recovered from the
    completion text (the extracted code equals the reference code), and the synthetic quantities
    shift with it, so every readout has signal. The mock tokens are Unicode code points (MockBackend)."""

    N_HEADER = 8        # synthetic header tokens added to the V2 text length

    def __init__(self, mapping: Mapping[str, tuple[str, Sequence[str]]], *, n_layers: int = 8, hidden: int = 16,
                 shift: float = 1.0, v1_unparseable_share: float = 0.2, prompts: PromptSet | None = None):
        self.mapping = dict(mapping)
        self.n_layers, self.hidden, self.shift = n_layers, hidden, shift
        self.v1_unparseable_share = v1_unparseable_share
        self.prompts = prompts or load_prompts()
        self.layers = layer_indices(n_layers)
        self.stats: dict[str, float] = {}

    def label(self, record: GenerationRecord, code: str | None) -> int:
        entry = self.mapping.get(record.problem_id)
        return int(code is not None and entry is not None and code.strip() == entry[0].strip())

    def capture(self, records: Sequence[GenerationRecord], extractions: Mapping[str, ExtractionResult],
                problems: Mapping[str, Problem]) -> tuple[list[CaptureRecord], dict[str, Any]]:
        import torch
        n, L, D = len(records), len(self.layers), self.hidden
        direction = np.random.default_rng(12345).normal(size=D)
        direction /= np.linalg.norm(direction)
        hs = {k: np.zeros((n, L, D), dtype=np.float32) for k in ("hs_p1", "hs_p2", "hs_p3", "hs_mean_code")}
        yn = np.zeros(n, dtype=np.float32)
        lps, offsets, recs = [], [0], []
        for i, r in enumerate(records):
            ext = extractions.get(r.sample_uid)
            code, _fail = (ext.code, ext.failure) if ext is not None else \
                extract_fallback(r.sample_uid, r.completion_text, problems[r.problem_id].entry_point, r.truncated)
            y = self.label(r, code)
            rng = np.random.default_rng(int.from_bytes(hashlib.sha256(r.sample_uid.encode()).digest()[:8], "big"))
            sign = 2 * y - 1
            plen = len(self.prompts.generation_message(problems[r.problem_id]))
            core = [t for t in r.completion_token_ids if t != 0x110000]
            comp_len = len(core) + (1 if r.finish_reason == "stop" else 0)
            decoded = "".join(chr(t) for t in core)
            loc = locate_code(decoded, code) if code else None
            rngc = strip_range(decoded, *loc) if loc else None
            if rngc is None:
                p2 = plen + max(len(core), 1) - 1
                span = (p2 + 1, p2 + 1)
            else:
                span = (plen + rngc[0], plen + rngc[1])
                p2 = span[1] - 1
            elen = len(self.prompts.elicit_text("V2")) + self.N_HEADER
            e0 = plen + comp_len
            for key, strength in (("hs_p1", 0.2), ("hs_p2", 1.0), ("hs_p3", 1.2), ("hs_mean_code", 0.8)):
                hs[key][i] = rng.normal(size=(L, D)) + strength * self.shift * sign * direction
            yn[i] = np.float32(rng.normal() + 1.5 * sign)
            nlp = span[1] - span[0]
            lp = (-rng.exponential(0.5, size=nlp) - 0.05 * (1 - y)).astype(np.float32)
            lps.append(lp)
            offsets.append(offsets[-1] + nlp)
            if rng.random() < self.v1_unparseable_share:
                v1_text = GARBAGE_V1[int(rng.integers(len(GARBAGE_V1)))]
            else:
                v1_text = f"Confidence: {int(np.clip(round(50 + 25 * sign + rng.normal() * 15), 0, 100))}"
            recs.append(CaptureRecord(
                sample_uid=r.sample_uid, hidden=HiddenStateRef(shard_file="", row=i, layers=tuple(self.layers)),
                n_code_tokens=nlp, code_token_span=span, p1=plen - 1, p2=p2, p3=e0 + elen - 1,
                elicitation_span=(e0, e0 + elen), yes_no_logodds=float(yn[i]), v1_text=v1_text,
                v1_value=parse_v1(v1_text),
                sum_logprob=float(lp.sum()) if nlp else float("nan"),
                mean_logprob=float(lp.mean()) if nlp else float("nan"),
                min_logprob=float(lp.min()) if nlp else float("nan")))
        arrays: dict[str, Any] = {k: torch.from_numpy(v).to(torch.bfloat16) for k, v in hs.items()}
        arrays["yes_no_logodds"] = yn
        arrays["code_logprobs"] = np.concatenate(lps).astype(np.float32) if lps else np.zeros(0, np.float32)
        arrays["code_logprob_offsets"] = np.asarray(offsets, dtype=np.int64)
        self.stats["samples"] = self.stats.get("samples", 0) + n
        return recs, arrays
