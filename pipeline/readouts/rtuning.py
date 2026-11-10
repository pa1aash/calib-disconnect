"""R-Tuning-style readout S^R (design 7.5).

Same LoRA settings and the selected recipe as S^T, but the adapter is active at every position (mode
"full" of `MaskedLoraModel`). Supervised fine-tuning on training-fold frozen samples: each sequence is
generation prompt + frozen completion (its end-of-turn token removed) + joiner + "I am" + "sure" or
"unsure" (pass or fail under the active suite) + end-of-turn token. The loss is next-token
cross-entropy on the assistant tokens: the completion, the suffix, and the end-of-turn token.

Readout: P(sure) / (P(sure) + P(unsure)) after "I am". Tokenizations where " sure" and " unsure" take
several tokens are handled by comparing the log-probabilities of the two full continuations, so
`logit = log P(sure tokens | ctx) - log P(unsure tokens | ctx)` and `prob = sigmoid(logit)`.

Reading B (g = 0): `RTuningTrainer.fit` scores the frozen test-fold sequences followed by "I am".
Reading A (g = 1): the generate module produces fresh samples with the adapter and calls
`score_rtuning(model, adapter, sequences, tokens)` on them.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np
import torch

from pipeline.contracts import constants as K
from pipeline.contracts.interfaces import TeacherForcedLayout

from .masked_lora import MaskedLoraModel
from .recipe import B_EFF, FitOutcome, lr_at, steps_per_epoch


@dataclass(frozen=True)
class RTuningTokens:
    joiner_ids: tuple[int, ...]   # tokens between the completion and "I am" (for example a newline)
    am_ids: tuple[int, ...]       # "I am"
    sure_ids: tuple[int, ...]     # continuation of "I am" that spells "I am sure" (for example " sure")
    unsure_ids: tuple[int, ...]   # continuation that spells "I am unsure"
    eot_id: int | None = None     # end-of-turn token appended after the suffix and stripped from completions


def rtuning_tokens_from_tokenizer(tok, joiner: str = "\n", eot_id: int | None = None) -> RTuningTokens:
    """Split the tokenization of "I am sure" and "I am unsure" at the end of "I am". If the tokenizer does
    not keep "I am" as a prefix of both, the continuations are tokenized on their own with a leading space."""
    enc = lambda s: tuple(tok.encode(s, add_special_tokens=False))  # noqa: E731
    am = enc(K.RTUNING_PREFIX)
    full_s, full_u = enc(K.RTUNING_SURE), enc(K.RTUNING_UNSURE)
    if full_s[:len(am)] == am and full_u[:len(am)] == am:
        sure, unsure = full_s[len(am):], full_u[len(am):]
    else:
        sure, unsure = enc(" sure"), enc(" unsure")
    if not sure or not unsure or sure == unsure:
        raise ValueError("cannot separate the sure and unsure continuations")
    return RTuningTokens(enc(joiner) if joiner else (), am, sure, unsure, eot_id)


def strip_eot(completion_ids: Sequence[int], eot_id: int | None) -> list[int]:
    ids = list(completion_ids)
    if eot_id is not None and ids and ids[-1] == eot_id:
        ids = ids[:-1]
    return ids


def context_ids(prompt_ids: Sequence[int], completion_ids: Sequence[int], tokens: RTuningTokens) -> list[int]:
    """prompt + completion (no end-of-turn) + joiner + "I am": the context for the readout."""
    return list(prompt_ids) + strip_eot(completion_ids, tokens.eot_id) + list(tokens.joiner_ids) + list(tokens.am_ids)


def build_sft_example(prompt_ids: Sequence[int], completion_ids: Sequence[int], passed: bool,
                      tokens: RTuningTokens) -> tuple[list[int], list[bool]]:
    """(token ids, supervised flags). Supervised: completion, suffix, end-of-turn. Not: the prompt."""
    comp = strip_eot(completion_ids, tokens.eot_id)
    suffix = list(tokens.joiner_ids) + list(tokens.am_ids) + list(tokens.sure_ids if passed else tokens.unsure_ids)
    tail = [tokens.eot_id] if tokens.eot_id is not None else []
    ids = list(prompt_ids) + comp + suffix + tail
    sup = [False] * len(prompt_ids) + [True] * (len(comp) + len(suffix) + len(tail))
    return ids, sup


@dataclass(frozen=True)
class RTuningScore:
    lp_sure: float
    lp_unsure: float
    logit: float       # lp_sure - lp_unsure
    prob: float        # P(sure) / (P(sure) + P(unsure))


def _backbone(model, adapter: MaskedLoraModel | None, ids, am, pos):
    if adapter is not None:
        return adapter._run(ids, am, pos, "full")
    return getattr(model, model.base_model_prefix)(input_ids=ids, attention_mask=am, position_ids=pos, use_cache=False)


def _logits(model, h: torch.Tensor) -> torch.Tensor:
    z = model.get_output_embeddings()(h).float()
    cap = getattr(model.config.get_text_config(), "final_logit_softcapping", None)
    return torch.tanh(z / cap) * cap if cap else z


def _left_pad(seqs: Sequence[Sequence[int]], pad_id: int, device):
    T = max(len(s) for s in seqs)
    ids = torch.full((len(seqs), T), pad_id, dtype=torch.long)
    am = torch.zeros((len(seqs), T), dtype=torch.long)
    for b, s in enumerate(seqs):
        ids[b, T - len(s):] = torch.tensor(list(s), dtype=torch.long)
        am[b, T - len(s):] = 1
    pos = (am.cumsum(-1) - 1).clamp(min=0)
    return ids.to(device), am.to(device), pos.to(device)


@torch.no_grad()
def score_rtuning(model, adapter: MaskedLoraModel | None, sequences: Sequence[tuple[Sequence[int], Sequence[int]]],
                  tokens: RTuningTokens, *, batch_size: int = 8, pad_id: int = 0) -> list[RTuningScore]:
    """Score (prompt_ids, completion_ids) pairs after "I am". `adapter` is a MaskedLoraModel used in full
    (unmasked) mode, or None for the base weights."""
    device = next(model.parameters()).device
    if adapter is not None:
        adapter.eval()
    ctxs = [context_ids(p, c, tokens) for p, c in sequences]
    lps = {}
    for tag, cont in (("sure", tokens.sure_ids), ("unsure", tokens.unsure_ids)):
        L = len(cont)
        vals = np.zeros(len(ctxs))
        order = sorted(range(len(ctxs)), key=lambda i: len(ctxs[i]))
        for s in range(0, len(order), batch_size):
            idx = order[s:s + batch_size]
            ids, am, pos = _left_pad([ctxs[i] + list(cont) for i in idx], pad_id, device)
            T = ids.shape[1]
            h = _backbone(model, adapter, ids, am, pos).last_hidden_state[:, T - 1 - L:T - 1]   # predicts the L tokens
            logp = torch.log_softmax(_logits(model, h), dim=-1)
            tgt = torch.as_tensor(list(cont), device=device)
            lp = logp.gather(-1, tgt.view(1, L, 1).expand(len(idx), L, 1)).squeeze(-1).sum(-1)
            for i, v in zip(idx, lp.cpu().numpy()):
                vals[i] = v
        lps[tag] = vals
    out = []
    for a, b in zip(lps["sure"], lps["unsure"]):
        z = float(a - b)
        out.append(RTuningScore(float(a), float(b), z, float(1.0 / (1.0 + np.exp(-z)))))
    return out


class RTuningTrainer:
    """`AdapterTrainer` for S^R. Rows index `layouts` (prompt_ids and completion_ids are used; the
    elicitation ids are ignored). Labels y are the pass/fail labels of the active suite."""

    surrogate = False

    def __init__(self, mlm: MaskedLoraModel, layouts: Sequence[TeacherForcedLayout], tokens: RTuningTokens, *,
                 pad_id: int = 0, micro_batch: int = 2, eval_batch: int = 8, grad_clip: float = 1.0,
                 weight_decay: float = 0.0, init_std: float | None = None):
        self.mlm, self.layouts, self.tokens = mlm, layouts, tokens
        self.pad_id, self.micro_batch, self.eval_batch = pad_id, micro_batch, eval_batch
        self.grad_clip, self.weight_decay, self.init_std = grad_clip, weight_decay, init_std
        self.device = next(mlm.hf.parameters()).device

    def score(self, rows: np.ndarray) -> np.ndarray:
        seqs = [(self.layouts[r].prompt_ids, self.layouts[r].completion_ids) for r in rows]
        sc = score_rtuning(self.mlm.hf, self.mlm, seqs, self.tokens, batch_size=self.eval_batch, pad_id=self.pad_id)
        return np.array([s.logit for s in sc], dtype=np.float32)

    def _loss(self, rows: np.ndarray, y: np.ndarray, n_sup_total: int) -> torch.Tensor:
        exs = [build_sft_example(self.layouts[r].prompt_ids, self.layouts[r].completion_ids, bool(y[r]), self.tokens)
               for r in rows]
        ids, am, pos = _left_pad([e[0] for e in exs], self.pad_id, self.device)
        T = ids.shape[1]
        sup = torch.zeros((len(exs), T), dtype=torch.bool)
        for b, e in enumerate(exs):
            sup[b, T - len(e[0]):] = torch.tensor(e[1], dtype=torch.bool)
        sup = sup.to(self.device)
        h = self.mlm._run(ids, am, pos, "full").last_hidden_state[:, :-1]
        target_sup = sup[:, 1:]
        h_sel = h[target_sup]
        tgt = ids[:, 1:][target_sup]
        logits = _logits(self.mlm.hf, h_sel)
        return torch.nn.functional.cross_entropy(logits, tgt, reduction="sum") / n_sup_total

    def fit(self, train_rows: np.ndarray, y: np.ndarray, *, lr: float, total_steps: int, schedule_steps: int,
            eval_rows: np.ndarray | None = None, eval_every: int = K.LORA_EVAL_EVERY_STEPS,
            score_sets: Mapping[str, np.ndarray] | None = None, seed: int = 0,
            save_path: str | None = None) -> FitOutcome:
        mlm = self.mlm
        mlm.reset(seed, init_std=self.init_std)
        params = mlm.trainable_parameters()
        opt = torch.optim.AdamW(params, lr=lr, weight_decay=self.weight_decay)
        train_rows = np.asarray(train_rows)
        n = len(train_rows)
        spe = steps_per_epoch(n)
        for step in range(total_steps):
            epoch, idx = divmod(step, spe)
            perm = np.random.default_rng(seed * 7919 + epoch).permutation(n)
            rows = train_rows[perm[idx * B_EFF:(idx + 1) * B_EFF]]
            for g in opt.param_groups:
                g["lr"] = lr_at(step, lr, schedule_steps)
            mlm.train()
            opt.zero_grad(set_to_none=True)
            # supervised tokens of the whole effective batch (the prompt is excluded)
            n_sup = sum(len(build_sft_example(self.layouts[r].prompt_ids, self.layouts[r].completion_ids, bool(y[r]),
                                              self.tokens)[0]) - len(self.layouts[r].prompt_ids) for r in rows)
            for i in range(0, len(rows), self.micro_batch):
                self._loss(rows[i:i + self.micro_batch], y, n_sup).backward()
            torch.nn.utils.clip_grad_norm_(params, self.grad_clip)
            opt.step()
        out = FitOutcome(curve=[], steps_run=total_steps)
        if score_sets:
            for name, r in score_sets.items():
                out.final_scores[name] = self.score(r)
        if save_path:
            mlm.save_adapter(save_path)
        return out
