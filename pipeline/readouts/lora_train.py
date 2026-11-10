"""Training loop for the masked-LoRA stated readout S^T and its controls (design 7.4, 7.11).

`MaskedLoraTrainer` implements `recipe.AdapterTrainer` on a `MaskedLoraModel`:

  * loss: binary cross-entropy of sigmoid(log-odds) against the label (log-odds at p3 over the Yes and
    No token sets, float32 LM head); for the head control, BCE of a linear head on the p3 state;
  * optimizer: AdamW over the LoRA parameters (and the head), learning rate from `recipe.lr_at`
    (5 percent linear warmup, cosine to zero over `schedule_steps`), effective batch
    LORA_EFFECTIVE_BATCH sequences by gradient accumulation over micro-batches; gradient norm clipped
    at 1.0 and weight decay 0.0 (two choices the design does not fix);
  * gradients only through elicitation tokens: with `economy=True` the prefix runs under no_grad and its
    KV cache is reused (`MaskedLoraModel.final_state`); `economy=False` runs the full masked forward,
    which gives the same loss and gradients (tested);
  * data order: each epoch is a seeded permutation; step s uses batch (s mod steps_per_epoch) of epoch
    s // steps_per_epoch, so a schedule longer than one epoch revisits the data;
  * evaluation every `eval_every` steps and at the last step on `eval_rows`, in eval mode (no dropout).

Every `fit` starts from a fresh adapter (A kaiming-uniform from the seed, B zero), so fits are
independent of earlier fits on the same base model.
"""

from __future__ import annotations

from typing import Mapping, Sequence

import numpy as np
import torch

from pipeline.contracts import constants as K
from pipeline.contracts.interfaces import TeacherForcedLayout

from .common import logloss_from_logodds
from .masked_lora import MaskedLoraModel, PaddedBatch, bce_on_logodds, collate_layouts
from .recipe import B_EFF, FitOutcome, lr_at, steps_per_epoch


def group_micro_batches(layouts: Sequence[TeacherForcedLayout], rows: np.ndarray, micro_batch: int) -> list[np.ndarray]:
    """Split rows into micro-batches whose sequences share one elicitation length (needed by the economy
    path), sorted by total length within a group to limit padding."""
    groups: dict[int, list[int]] = {}
    for r in rows:
        groups.setdefault(len(layouts[r].elicitation_ids), []).append(int(r))
    out = []
    for _, g in sorted(groups.items()):
        g.sort(key=lambda r: len(layouts[r].prompt_ids) + len(layouts[r].completion_ids))
        for i in range(0, len(g), micro_batch):
            out.append(np.asarray(g[i:i + micro_batch]))
    return out


class MaskedLoraTrainer:
    surrogate = False

    def __init__(self, mlm: MaskedLoraModel, layouts: Sequence[TeacherForcedLayout], yes_ids: Sequence[int],
                 no_ids: Sequence[int], *, pad_id: int = 0, micro_batch: int = 8, eval_batch: int = 16,
                 economy: bool = True, head: bool = False, grad_clip: float = 1.0, weight_decay: float = 0.0,
                 init_std: float | None = None):
        self.mlm = mlm
        self.layouts = layouts
        self.yes_ids, self.no_ids = list(yes_ids), list(no_ids)
        self.pad_id = pad_id
        self.micro_batch, self.eval_batch = micro_batch, eval_batch
        self.economy = economy
        self.head = head
        self.grad_clip = grad_clip
        self.weight_decay = weight_decay
        self.init_std = init_std
        if head and mlm.head is None:
            mlm.add_head()
        self.device = next(mlm.hf.parameters()).device

    # -- scoring -----------------------------------------------------------------------------------
    def _batch(self, rows: np.ndarray, y: np.ndarray | None) -> PaddedBatch:
        return collate_layouts([self.layouts[r] for r in rows], self.pad_id, self.device,
                               y=None if y is None else y[rows])

    def _z(self, batch: PaddedBatch) -> torch.Tensor:
        if self.head:
            return self.mlm.head_logit(batch, economy=self.economy)
        return self.mlm.logodds(batch, self.yes_ids, self.no_ids, economy=self.economy)

    @torch.no_grad()
    def score(self, rows: np.ndarray) -> np.ndarray:
        """Log-odds of `rows` in eval mode (the engine that produces S^T), aligned to `rows`."""
        self.mlm.eval()
        rows = np.asarray(rows)
        out = np.zeros(len(rows), dtype=np.float32)
        pos = {int(r): i for i, r in enumerate(rows)}
        for mb in group_micro_batches(self.layouts, rows, self.eval_batch):
            z = self._z(self._batch(mb, None)).float().cpu().numpy()
            for r, v in zip(mb, z):
                out[pos[int(r)]] = v
        return out

    # -- loss on rows (used by the training step and by tests) --------------------------------------
    def loss_on(self, rows: np.ndarray, y: np.ndarray, reduction: str = "mean") -> torch.Tensor:
        batch = self._batch(rows, y.astype(np.float32))
        return bce_on_logodds(self._z(batch), batch.y, reduction=reduction)

    # -- training ----------------------------------------------------------------------------------
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
        outcome = FitOutcome(curve=[])
        eval_steps = {s for s in range(1, total_steps + 1) if s % eval_every == 0} | {total_steps}
        for step in range(total_steps):
            epoch, idx = divmod(step, spe)
            perm = np.random.default_rng(seed * 7919 + epoch).permutation(n)
            rows = train_rows[perm[idx * B_EFF:(idx + 1) * B_EFF]]
            for g in opt.param_groups:
                g["lr"] = lr_at(step, lr, schedule_steps)
            mlm.train()
            opt.zero_grad(set_to_none=True)
            for mb in group_micro_batches(self.layouts, rows, self.micro_batch):
                loss = self.loss_on(mb, y, reduction="sum") / len(rows)
                loss.backward()
            torch.nn.utils.clip_grad_norm_(params, self.grad_clip)
            opt.step()
            done = step + 1
            if eval_rows is not None and done in eval_steps:
                z = self.score(eval_rows)
                outcome.curve.append((done, logloss_from_logodds(y[eval_rows], z)))
                outcome.val_scores[done] = z
        outcome.steps_run = total_steps
        if score_sets:
            for name, r in score_sets.items():
                outcome.final_scores[name] = self.score(r)
        if save_path:
            mlm.save_adapter(save_path)
        return outcome
