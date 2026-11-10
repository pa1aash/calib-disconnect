"""Model-backed trainers for the stage: loads the base model and builds S^T, ladder, head, and S^R trainers.

`RealBackend` owns one Hugging Face causal LM (base weights, frozen) plus the teacher-forced token
layouts of the samples of one (model, population). Each `st(...)` / `sr(...)` context wraps the model
with a fresh peft adapter, yields a trainer, and unwraps the adapter on exit, so ranks 1, 4, 16 and the
R-Tuning adapter can follow one another on the same weights.

Token layouts come from the generate module (see CONTRACT_REQUESTS.md): they are not recoverable from the
capture index alone. `load_layouts_provider` resolves a "module:function" path from
`cfg.extra["layouts_provider"]`, defaulting to `pipeline.generate.layouts:teacher_forced_layouts`.
"""

from __future__ import annotations

import contextlib
import importlib
import json
from pathlib import Path
from typing import Callable, Sequence

import numpy as np

from pipeline.contracts import constants as K
from pipeline.contracts.interfaces import RunConfig, TeacherForcedLayout

from .lora_train import MaskedLoraTrainer
from .masked_lora import LoraSpec, MaskedLoraModel, answer_token_ids
from .rtuning import RTuningTokens, RTuningTrainer, rtuning_tokens_from_tokenizer

DEFAULT_LAYOUTS_PROVIDER = "pipeline.generate.layouts:teacher_forced_layouts"


def load_layouts_provider(cfg: RunConfig) -> Callable:
    path = cfg.extra.get("layouts_provider", DEFAULT_LAYOUTS_PROVIDER)
    mod, _, fn = path.partition(":")
    try:
        return getattr(importlib.import_module(mod), fn)
    except (ImportError, AttributeError) as e:
        raise RuntimeError(f"LoRA readouts need a token-layout provider ({path}): {e}. "
                           "See pipeline/readouts/CONTRACT_REQUESTS.md.") from e


def answer_ids_from_config(layout_answer_tokens: Path, model_key: str, tokenizer) -> tuple[list[int], list[int]]:
    """Yes/No token sets from config/answer_tokens.json when present ({model_key: {"yes": [...], "no": [...]}}),
    else scanned from the tokenizer (7.12)."""
    p = Path(layout_answer_tokens)
    if p.exists():
        d = json.loads(p.read_text()).get(model_key)
        if isinstance(d, dict) and d.get("yes") and d.get("no"):
            return [int(i) for i in d["yes"]], [int(i) for i in d["no"]]
    return answer_token_ids(tokenizer)


class RealBackend:
    def __init__(self, model, layouts: Sequence[TeacherForcedLayout], yes_ids: Sequence[int], no_ids: Sequence[int], *,
                 rtuning_tokens: RTuningTokens | None = None, pad_id: int = 0, micro_batch: int = 8,
                 eval_batch: int = 16, sr_micro_batch: int = 2, economy: bool = True):
        self.model, self.layouts = model, list(layouts)
        self.yes_ids, self.no_ids = list(yes_ids), list(no_ids)
        self.rtuning_tokens = rtuning_tokens
        self.pad_id, self.micro_batch, self.eval_batch, self.sr_micro_batch = pad_id, micro_batch, eval_batch, sr_micro_batch
        self.economy = economy

    @classmethod
    def from_pretrained(cls, cfg: RunConfig, model_key: str, layouts_fn: Callable, answer_tokens_path: Path):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        repo, rev = (K.SMOKE_MODEL if model_key == "SMOKE" else K.MODELS[model_key][:2])
        tok = AutoTokenizer.from_pretrained(repo, revision=rev, cache_dir=cfg.hf_cache)
        dtype = torch.bfloat16 if cfg.device == "cuda" else torch.float32
        model = AutoModelForCausalLM.from_pretrained(repo, revision=rev, cache_dir=cfg.hf_cache, dtype=dtype)
        model.to(cfg.device).eval()
        for p in model.parameters():
            p.requires_grad_(False)
        yes, no = answer_ids_from_config(answer_tokens_path, model_key, tok)
        eot = getattr(tok, "eos_token_id", None)
        tokens = rtuning_tokens_from_tokenizer(tok, eot_id=eot if isinstance(eot, int) else None)
        return cls(model, layouts_fn(tok), yes, no, rtuning_tokens=tokens,
                   pad_id=tok.pad_token_id if tok.pad_token_id is not None else 0)

    @contextlib.contextmanager
    def st(self, rank: int = K.LORA_RANK, head: bool = False, seed: int = 0):
        spec = LoraSpec.ladder(rank) if rank != K.LORA_RANK else LoraSpec()
        mlm = MaskedLoraModel(self.model, spec, seed=seed)
        try:
            yield MaskedLoraTrainer(mlm, self.layouts, self.yes_ids, self.no_ids, pad_id=self.pad_id,
                                    micro_batch=self.micro_batch, eval_batch=self.eval_batch, economy=self.economy,
                                    head=head)
        finally:
            mlm.close()

    @contextlib.contextmanager
    def sr(self, seed: int = 0):
        if self.rtuning_tokens is None:
            raise RuntimeError("no R-Tuning token set")
        mlm = MaskedLoraModel(self.model, LoraSpec(), seed=seed)
        try:
            yield RTuningTrainer(mlm, self.layouts, self.rtuning_tokens, pad_id=self.pad_id,
                                 micro_batch=self.sr_micro_batch, eval_batch=self.eval_batch)
        finally:
            mlm.close()
