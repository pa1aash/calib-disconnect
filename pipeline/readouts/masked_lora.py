"""Masked LoRA: an adapter that is active only on the elicitation span (design 7.4 and 7.12).

REVIEW GUIDE. This file holds everything that the position mask touches:

  1. `MaskedLoraModel` wraps a Hugging Face causal LM with peft LoRA layers (rank, alpha, dropout from
     `LoraSpec`, no bias, on every attention and MLP projection of the text decoder). The mask is applied
     by a forward hook on each `lora_B` module: the LoRA branch output is multiplied by a per-token 0/1
     tensor, so for a token with mask 0 the layer computes exactly `base(x)` and for a token with mask 1
     it computes `base(x) + scaling * B(A(dropout(x)))`. The mask tensor is set on the wrapper before
     the forward pass and cleared afterwards (`_run`).
  2. Because queries, keys, and values of masked-out positions come only from base weights, and a
     position only attends to earlier positions, the hidden states and the KV cache at every position
     before the elicitation span equal the base model's. Two forward paths use this:
       * `full` path: one forward over prompt + completion + elicitation tokens with the mask;
       * `economy` path (the 12.5 economy): the prefix (prompt + completion) runs once under `no_grad`
         with the adapter disabled and its KV cache is reused for the elicitation tokens, which run
         with the adapter on (mask all ones). Gradients can only flow through elicitation tokens.
     `tests/readouts/test_readouts_masked_lora.py` checks that both paths give the same log-odds, loss,
     and gradients.
  3. The batch layout is LEFT padded: every sequence ends at the same column, so p3 (the last token of
     the elicitation span) is always the last column, and the elicitation tokens of a batch occupy the
     same trailing columns when their lengths are equal. Position ids are computed from the attention
     mask, so a padded row equals its unpadded run.
  4. The readout S^T is the float32 log-odds log sum_{Yes set} P - log sum_{No set} P at p3: the LM head
     is applied in float32 to the final normed state and only to the rows of the Yes and No tokens (the
     softmax normalizer cancels in the difference; Gemma's final-logit soft-capping is applied). The
     logistic transform of the log-odds is the probability on which the binary cross-entropy is taken.
  5. `mask_unit_test` is the 7.12 unit test: with a nonzero adapter, hidden states and KV cache at every
     non-masked, non-pad position match the base model within MASK_TEST_ATOL (float32); states at masked
     positions differ by more than that (positive control); the same adapter without the mask (the
     R-Tuning-style full adapter) changes non-masked positions (negative control).

Training loops, recipes, and K4 are in `lora_train.py` and `recipe.py`; they only call this file.
"""

from __future__ import annotations

import contextlib
import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np
import torch
from torch import nn

from pipeline.contracts import constants as K
from pipeline.contracts.interfaces import TeacherForcedLayout

TARGET_LEAVES = ("q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj")
_NON_TEXT = ("vision", "audio", "encoder", "visual")


# ---------------------------------------------------------------------------------------------------
# Adapter specification and target enumeration
# ---------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class LoraSpec:
    rank: int = K.LORA_RANK
    alpha: int = K.LORA_ALPHA
    dropout: float = K.LORA_DROPOUT

    @classmethod
    def ladder(cls, rank: int) -> "LoraSpec":
        """Capacity ladder (7.11): alpha is twice the rank."""
        return cls(rank=rank, alpha=2 * rank, dropout=K.LORA_DROPOUT)


def find_decoder_layers(model: nn.Module) -> tuple[str, nn.ModuleList]:
    """The text decoder's layer stack: `model.layers` (Qwen, Olmo), `model.language_model.layers`
    (Gemma 4 conditional generation). Vision and audio towers are skipped."""
    for name, mod in model.named_modules():
        if isinstance(mod, nn.ModuleList) and (name == "layers" or name.endswith(".layers")):
            if any(t in name for t in _NON_TEXT):
                continue
            return name, mod
    raise ValueError("no decoder layer stack found")


def target_module_names(model: nn.Module) -> list[str]:
    """Full names of every attention and MLP projection (nn.Linear) inside the decoder layers."""
    prefix, _ = find_decoder_layers(model)
    names = []
    for name, mod in model.named_modules():
        if name.startswith(prefix + ".") and isinstance(mod, nn.Linear) and name.rsplit(".", 1)[-1] in TARGET_LEAVES:
            names.append(name)
    if not names:
        raise ValueError("no LoRA target modules found")
    return names


# ---------------------------------------------------------------------------------------------------
# Padded batch layout
# ---------------------------------------------------------------------------------------------------
@dataclass
class PaddedBatch:
    input_ids: torch.Tensor        # long [B, T], left padded
    attention_mask: torch.Tensor   # long [B, T]
    position_ids: torch.Tensor     # long [B, T]
    mask: torch.Tensor             # float32 [B, T], 1 exactly on the elicitation span
    elic_len: list[int]
    y: torch.Tensor | None = None  # float32 [B]

    @property
    def B(self) -> int:
        return self.input_ids.shape[0]

    @property
    def T(self) -> int:
        return self.input_ids.shape[1]

    @property
    def uniform_elicitation(self) -> bool:
        return len(set(self.elic_len)) == 1

    @property
    def prefix_len(self) -> int:
        if not self.uniform_elicitation:
            raise ValueError("economy path needs equal elicitation lengths in a batch")
        return self.T - self.elic_len[0]


def collate_layouts(layouts: Sequence[TeacherForcedLayout], pad_id: int = 0, device=None,
                    y: Sequence[float] | np.ndarray | None = None) -> PaddedBatch:
    seqs = [list(l.prompt_ids) + list(l.completion_ids) + list(l.elicitation_ids) for l in layouts]
    T = max(len(s) for s in seqs)
    B = len(seqs)
    ids = torch.full((B, T), pad_id, dtype=torch.long)
    am = torch.zeros((B, T), dtype=torch.long)
    mk = torch.zeros((B, T), dtype=torch.float32)
    for b, (lay, s) in enumerate(zip(layouts, seqs)):
        n = len(s)
        ids[b, T - n:] = torch.tensor(s, dtype=torch.long)
        am[b, T - n:] = 1
        mk[b, T - n:] = torch.from_numpy(lay.mask().astype(np.float32))  # length n, 1 on the elicitation span
    pos = (am.cumsum(-1) - 1).clamp(min=0)
    yt = None if y is None else torch.as_tensor(np.asarray(y, dtype=np.float32))
    batch = PaddedBatch(ids, am, pos, mk, [len(l.elicitation_ids) for l in layouts], yt)
    return to_device(batch, device) if device is not None else batch


def to_device(b: PaddedBatch, device) -> PaddedBatch:
    return PaddedBatch(b.input_ids.to(device), b.attention_mask.to(device), b.position_ids.to(device),
                       b.mask.to(device), b.elic_len, None if b.y is None else b.y.to(device))


def answer_token_ids(tokenizer) -> tuple[list[int], list[int]]:
    """Yes and No sets (7.12): every single token whose decoded text, stripped of leading whitespace, is
    exactly "Yes" (resp. "No"). `tokenizer` needs `get_vocab()` or `vocab_size`, and `decode([id])`."""
    n = len(tokenizer.get_vocab()) if hasattr(tokenizer, "get_vocab") else tokenizer.vocab_size
    ids = range(max(n, getattr(tokenizer, "vocab_size", 0)))
    yes, no = [], []
    for i in ids:
        try:
            t = tokenizer.decode([i]).lstrip()
        except Exception:  # noqa: BLE001 - unmapped ids
            continue
        if t in K.YES_STRINGS:
            yes.append(i)
        elif t in K.NO_STRINGS:
            no.append(i)
    if not yes or not no:
        raise ValueError("empty Yes or No token set")
    return yes, no


# ---------------------------------------------------------------------------------------------------
# The wrapper
# ---------------------------------------------------------------------------------------------------
class MaskedLoraModel:
    """peft LoRA on all attention and MLP projections, with a per-token mask on the LoRA branch.

    modes of `_run` / forward helpers:
      "masked": adapter on, LoRA output multiplied by `batch.mask` (the S^T adapter);
      "full":   adapter on at every position, no mask (the R-Tuning-style adapter, 7.5);
      "off":    adapter disabled (the base model).
    """

    def __init__(self, model: nn.Module, spec: LoraSpec = LoraSpec(), *, seed: int = 0, init_std: float | None = None):
        from peft import LoraConfig, get_peft_model

        self.hf = model
        self.spec = spec
        self.targets = target_module_names(model)
        cfg = LoraConfig(r=spec.rank, lora_alpha=spec.alpha, lora_dropout=spec.dropout, bias="none",
                         target_modules=self.targets, task_type="CAUSAL_LM")
        self.peft = get_peft_model(model, cfg)
        self._mask: torch.Tensor | None = None
        self._handles = []
        self._lora_b = []
        for _, mod in self.peft.named_modules():
            lb = getattr(mod, "lora_B", None)
            if isinstance(lb, nn.ModuleDict) and "default" in lb:
                self._lora_b.append(lb["default"])
        if len(self._lora_b) != len(self.targets):
            raise RuntimeError(f"expected {len(self.targets)} LoRA layers, found {len(self._lora_b)}")
        for m in self._lora_b:
            self._handles.append(m.register_forward_hook(self._hook))
        self.head: nn.Linear | None = None
        self._closed = False
        self.reset(seed, init_std=init_std)

    # -- mask hook ---------------------------------------------------------------------------------
    def _hook(self, module, inputs, output):
        if self._mask is None:
            return output
        return output * self._mask.to(output.dtype)

    # -- parameters --------------------------------------------------------------------------------
    @property
    def backbone(self) -> nn.Module:
        return getattr(self.hf, self.hf.base_model_prefix)

    @property
    def n_lora_layers(self) -> int:
        return len(self._lora_b)

    def trainable_parameters(self) -> list[nn.Parameter]:
        ps = [p for p in self.peft.parameters() if p.requires_grad]
        if self.head is not None:
            ps += list(self.head.parameters())
        return ps

    def lora_state(self) -> dict[str, torch.Tensor]:
        return {k: v.detach().clone() for k, v in self.peft.named_parameters() if "lora_" in k}

    def reset(self, seed: int = 0, init_std: float | None = None) -> None:
        """Re-initialize the adapter: A kaiming-uniform, B zero (or N(0, init_std) for tests with a
        nonzero adapter). Also re-initializes the linear head if present (zeros)."""
        g = torch.Generator().manual_seed(int(seed))
        for _, mod in self.peft.named_modules():
            la, lb = getattr(mod, "lora_A", None), getattr(mod, "lora_B", None)
            if isinstance(la, nn.ModuleDict) and "default" in la:
                nn.init.kaiming_uniform_(la["default"].weight, a=math.sqrt(5), generator=g)
                if init_std is None:
                    nn.init.zeros_(lb["default"].weight)
                else:
                    nn.init.normal_(lb["default"].weight, std=init_std, generator=g)
        if self.head is not None:
            nn.init.zeros_(self.head.weight)
            nn.init.zeros_(self.head.bias)

    def add_head(self) -> None:
        """Logistic head on the final normed state at p3 (the LoRA-plus-linear-head control, 7.11)."""
        d = self.hf.get_input_embeddings().weight.shape[1]
        dev = self.hf.get_input_embeddings().weight.device
        self.head = nn.Linear(d, 1).to(device=dev, dtype=torch.float32)
        nn.init.zeros_(self.head.weight)
        nn.init.zeros_(self.head.bias)

    def train(self, mode: bool = True):
        self.peft.train(mode)
        if self.head is not None:
            self.head.train(mode)
        return self

    def eval(self):
        return self.train(False)

    def save_adapter(self, path) -> None:
        self.peft.save_pretrained(str(path))

    def close(self) -> None:
        """Remove hooks and unwrap the LoRA layers, restoring the base model in place."""
        if self._closed:
            return
        for h in self._handles:
            h.remove()
        self._handles = []
        self.peft.unload()
        self._closed = True

    # -- forward -----------------------------------------------------------------------------------
    def _run(self, input_ids, attention_mask, position_ids, mode: str, mask: torch.Tensor | None = None,
             past=None, use_cache: bool = False, hidden: bool = False):
        if mode not in ("masked", "full", "off"):
            raise ValueError(mode)
        if mode == "masked" and mask is None:
            raise ValueError("masked mode needs a mask")
        self._mask = mask.unsqueeze(-1) if (mode == "masked" and mask is not None) else None
        ctx = self.peft.disable_adapter() if mode == "off" else contextlib.nullcontext()
        try:
            with ctx:
                out = self.backbone(input_ids=input_ids, attention_mask=attention_mask, position_ids=position_ids,
                                    past_key_values=past, use_cache=use_cache, output_hidden_states=hidden)
        finally:
            self._mask = None
        return out

    def forward_full(self, batch: PaddedBatch, mode: str = "masked", *, use_cache: bool = False, hidden: bool = False):
        """One forward over the whole padded batch. mode "masked" uses batch.mask."""
        return self._run(batch.input_ids, batch.attention_mask, batch.position_ids, mode,
                         mask=batch.mask if mode == "masked" else None, use_cache=use_cache, hidden=hidden)

    def final_state(self, batch: PaddedBatch, *, economy: bool = True) -> torch.Tensor:
        """Final normed hidden state at p3 (the last column), float32 [B, D], masked adapter."""
        if not economy:
            return self.forward_full(batch, "masked").last_hidden_state[:, -1].float()
        Tp = batch.prefix_len
        E = batch.elic_len[0]
        with torch.no_grad():
            pre = self._run(batch.input_ids[:, :Tp], batch.attention_mask[:, :Tp], batch.position_ids[:, :Tp], "off",
                            use_cache=True)
        ones = torch.ones((batch.B, E), dtype=torch.float32, device=batch.input_ids.device)
        out = self._run(batch.input_ids[:, Tp:], batch.attention_mask, batch.position_ids[:, Tp:], "masked",
                        mask=ones, past=pre.past_key_values, use_cache=True)
        return out.last_hidden_state[:, -1].float()

    def logodds_from_state(self, h: torch.Tensor, yes_ids: Sequence[int], no_ids: Sequence[int]) -> torch.Tensor:
        """float32 log P(Yes set) - log P(No set). The LM head is applied in float32, restricted to the
        answer-token rows (the softmax normalizer cancels in the difference)."""
        w = self.hf.get_output_embeddings().weight
        dev = w.device
        wy = w[torch.as_tensor(list(yes_ids), device=dev)].float()
        wn = w[torch.as_tensor(list(no_ids), device=dev)].float()
        h = h.float()
        zy, zn = h @ wy.T, h @ wn.T
        cap = getattr(self.hf.config.get_text_config(), "final_logit_softcapping", None)
        if cap:
            zy, zn = torch.tanh(zy / cap) * cap, torch.tanh(zn / cap) * cap
        return torch.logsumexp(zy, -1) - torch.logsumexp(zn, -1)

    def logodds(self, batch: PaddedBatch, yes_ids: Sequence[int], no_ids: Sequence[int], *, economy: bool = True) -> torch.Tensor:
        return self.logodds_from_state(self.final_state(batch, economy=economy), yes_ids, no_ids)

    def head_logit(self, batch: PaddedBatch, *, economy: bool = True) -> torch.Tensor:
        if self.head is None:
            raise RuntimeError("no head; call add_head()")
        return self.head(self.final_state(batch, economy=economy)).squeeze(-1)


# ---------------------------------------------------------------------------------------------------
# Loss
# ---------------------------------------------------------------------------------------------------
def bce_on_logodds(z: torch.Tensor, y: torch.Tensor, reduction: str = "mean") -> torch.Tensor:
    """Binary cross-entropy of sigmoid(z) against y, stable in the log-odds."""
    return nn.functional.binary_cross_entropy_with_logits(z.float(), y.float(), reduction=reduction)


# ---------------------------------------------------------------------------------------------------
# Mask unit test (7.12)
# ---------------------------------------------------------------------------------------------------
def synthetic_layouts(vocab_size: int, n: int = 4, seed: int = 0, elic_len: int = 5) -> list[TeacherForcedLayout]:
    """Random token layouts with different prompt and completion lengths (so the batch is padded) and a
    common elicitation length. Ids are drawn from [3, vocab_size)."""
    rng = np.random.default_rng(seed)
    out = []
    for i in range(n):
        p = rng.integers(3, vocab_size, size=int(rng.integers(4, 9))).tolist()
        c = rng.integers(3, vocab_size, size=int(rng.integers(6, 15))).tolist()
        e = rng.integers(3, vocab_size, size=elic_len).tolist()
        out.append(TeacherForcedLayout(tuple(p), tuple(c), tuple(e), (len(p), len(p) + len(c))))
    return out


def _tail_positions(T: int, length: int) -> slice:
    return slice(T - length, T)


def _kv(cache) -> list[tuple[torch.Tensor, torch.Tensor]]:
    return [(l.keys, l.values) for l in cache.layers]


def _maxdiff(a: torch.Tensor, b: torch.Tensor, pos: torch.Tensor) -> float:
    """Max |a-b| over selected positions. a, b: [B, ..., T', D] with T' on dim -2 or dim 1."""
    d = (a - b).abs()
    if pos.sum() == 0:
        return 0.0
    return float(d[pos].max()) if d.dim() == 3 else float(d.permute(0, 2, 1, 3)[pos].max())


def mask_unit_test(model: nn.Module, layouts_or_tokenizer, adapter: "MaskedLoraModel | LoraSpec | None" = None, *,
                   atol: float = K.MASK_TEST_ATOL, pad_id: int = 0, yes_ids: Sequence[int] = (1,),
                   no_ids: Sequence[int] = (2,), init_std: float = 0.1, seed: int = 0,
                   negative_control: bool = True) -> dict:
    """The 7.12 mask unit test. Returns a report dict; `report["passed"]` is the conjunction of:

    (a) non-masked, non-pad positions: hidden states of every layer and the KV cache of every layer match
        the base model (adapter disabled) within `atol`, in the padded batch layout, with a nonzero adapter
        and the position mask on;
    (b) masked positions differ from the base by more than `atol` (positive control), in the last hidden
        state and in the KV cache;
    (c) the log-odds of the economy path (cached no-grad prefix) equal those of the full masked forward
        within `atol`, and the economy path's cached prefix equals the base prefix cache;
    (d) negative control: the same adapter with no mask (the R-Tuning-style full adapter) changes the
        states at non-masked positions by more than `atol`.

    `layouts_or_tokenizer`: a sequence of TeacherForcedLayout, or an object with `vocab_size` (random
    layouts are built). `adapter`: a MaskedLoraModel on `model`, a LoraSpec, or None (defaults, nonzero B).
    """
    own = False
    if adapter is None or isinstance(adapter, LoraSpec):
        adapter = MaskedLoraModel(model, adapter or LoraSpec(), seed=seed, init_std=init_std)
        own = True
    elif adapter.hf is not model:
        raise ValueError("adapter must wrap `model`")
    if hasattr(layouts_or_tokenizer, "vocab_size") and not isinstance(layouts_or_tokenizer, (list, tuple)):
        layouts = synthetic_layouts(int(layouts_or_tokenizer.vocab_size), seed=seed)
    else:
        layouts = list(layouts_or_tokenizer)
    dev = next(model.parameters()).device
    batch = collate_layouts(layouts, pad_id=pad_id, device=dev)
    was_training = adapter.peft.training
    adapter.eval()
    try:
        with torch.no_grad():
            base = adapter.forward_full(batch, "off", use_cache=True, hidden=True)
            msk = adapter.forward_full(batch, "masked", use_cache=True, hidden=True)
            full = adapter.forward_full(batch, "full", use_cache=True, hidden=True)
            real = batch.attention_mask.bool()
            masked_pos = batch.mask.bool() & real
            nonmasked_pos = (~batch.mask.bool()) & real

            def compare(a, b, pos):
                h = max(_maxdiff(x, y, pos) for x, y in zip(a.hidden_states, b.hidden_states))
                kv = 0.0
                for (ka, va), (kb, vb) in zip(_kv(a.past_key_values), _kv(b.past_key_values)):
                    Lc = ka.shape[-2]
                    sub = pos[:, _tail_positions(batch.T, Lc)]
                    kv = max(kv, _maxdiff(ka, kb, sub), _maxdiff(va, vb, sub))
                return h, kv

            nm_h, nm_kv = compare(msk, base, nonmasked_pos)
            m_h, m_kv = compare(msk, base, masked_pos)
            last_m = _maxdiff(msk.last_hidden_state, base.last_hidden_state, masked_pos)
            f_h, f_kv = compare(full, base, nonmasked_pos)
            # (c) economy versus full masked forward, through the same log-odds code used for S^T
            z_full = adapter.logodds(batch, yes_ids, no_ids, economy=False)
            z_eco = adapter.logodds(batch, yes_ids, no_ids, economy=True)
            z_base = adapter.logodds_from_state(base.last_hidden_state[:, -1], yes_ids, no_ids)
            Tp = batch.prefix_len
            pre = adapter._run(batch.input_ids[:, :Tp], batch.attention_mask[:, :Tp], batch.position_ids[:, :Tp], "off",
                               use_cache=True)
            pre_masked = adapter._run(batch.input_ids[:, :Tp], batch.attention_mask[:, :Tp], batch.position_ids[:, :Tp],
                                      "masked", mask=batch.mask[:, :Tp], use_cache=True)
            pref_kv = 0.0
            for (ka, va), (kb, vb) in zip(_kv(pre.past_key_values), _kv(pre_masked.past_key_values)):
                Lc = ka.shape[-2]
                sub = real[:, _tail_positions(Tp, Lc)]
                pref_kv = max(pref_kv, _maxdiff(ka, kb, sub), _maxdiff(va, vb, sub))
        report = {
            "atol": atol,
            "batch_shape": [batch.B, batch.T],
            "n_lora_layers": adapter.n_lora_layers,
            "nonmasked_hidden_maxdiff": nm_h,
            "nonmasked_kv_maxdiff": nm_kv,
            "masked_hidden_maxdiff": m_h,
            "masked_kv_maxdiff": m_kv,
            "masked_last_hidden_maxdiff": last_m,
            "economy_vs_full_logodds_maxdiff": float((z_full - z_eco).abs().max()),
            "adapter_changes_logodds": float((z_full - z_base).abs().max()),
            "prefix_cache_masked_vs_base_maxdiff": pref_kv,
        }
        report["a_nonmasked_match"] = bool(nm_h <= atol and nm_kv <= atol)
        report["b_masked_differ"] = bool(last_m > atol and m_kv > atol)
        report["c_economy_matches"] = bool(report["economy_vs_full_logodds_maxdiff"] <= atol and pref_kv <= atol)
        if negative_control:
            report["negative_control_nonmasked_hidden_maxdiff"] = f_h
            report["negative_control_nonmasked_kv_maxdiff"] = f_kv
            report["d_negative_control_differs"] = bool(f_h > atol and f_kv > atol)
        report["passed"] = bool(report["a_nonmasked_match"] and report["b_masked_differ"]
                                and report["c_economy_matches"]
                                and (not negative_control or report["d_negative_control_differs"]))
        return report
    finally:
        adapter.train(was_training)
        if own:
            adapter.close()
