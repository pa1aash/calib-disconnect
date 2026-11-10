"""Surrogate adapter trainer for the mock backend (`cfg.backend == "mock"`).

S^T and S^R are replaced by a logistic regression on two features of the capture: the stored V2 log-odds
and the first component of the mock hidden state (the last candidate layer at p3). It implements the same
`AdapterTrainer` interface as the LoRA trainers, so the stage runs exactly the same cross-fitting,
recipe selection (with K4), step transfer, inner-adapter, isotonic, and FitRecord code. FitRecords carry
`surrogate=True` in `selected`.

Training mimics the adapter loop: mini-batches of LORA_EFFECTIVE_BATCH rows, Adam, the same warmup and
cosine schedule, the same evaluation steps. Because the learning-rate grid is meant for LoRA, the
surrogate multiplies the learning rate by SURROGATE_LR_SCALE so that a few steps move a two-parameter
model; this scale is the only difference from the real loop.
"""

from __future__ import annotations

from typing import Mapping

import numpy as np

from pipeline.contracts import constants as K
from pipeline.contracts.interfaces import ReadoutData

from .common import logloss_from_logodds, sigmoid
from .recipe import B_EFF, FitOutcome, lr_at, steps_per_epoch

SURROGATE_LR_SCALE = 1000.0


def surrogate_features(data: ReadoutData) -> np.ndarray:
    if data.capture is None or data.hidden is None:
        raise ValueError("the surrogate needs capture records and hidden states")
    z = np.array([float(np.float32(c.yes_no_logodds)) for c in data.capture])
    h = np.asarray(data.hidden["hs_p3"][:, -1, 0], dtype=np.float64)
    return np.stack([z, h], axis=1)


class SurrogateTrainer:
    surrogate = True

    def __init__(self, features: np.ndarray):
        self.X = np.asarray(features, dtype=np.float64)

    def _score(self, w: np.ndarray, b: float, mu: np.ndarray, sd: np.ndarray, rows: np.ndarray) -> np.ndarray:
        return (((self.X[rows] - mu) / sd) @ w + b).astype(np.float32)

    def fit(self, train_rows: np.ndarray, y: np.ndarray, *, lr: float, total_steps: int, schedule_steps: int,
            eval_rows: np.ndarray | None = None, eval_every: int = K.LORA_EVAL_EVERY_STEPS,
            score_sets: Mapping[str, np.ndarray] | None = None, seed: int = 0,
            save_path: str | None = None) -> FitOutcome:
        train_rows = np.asarray(train_rows)
        n = len(train_rows)
        Xtr = self.X[train_rows]
        mu, sd = Xtr.mean(0), Xtr.std(0)
        sd = np.where(sd < 1e-8, 1.0, sd)
        Z = (Xtr - mu) / sd
        yt = y[train_rows].astype(np.float64)
        w, b = np.zeros(Z.shape[1]), 0.0
        m_w, v_w, m_b, v_b = np.zeros_like(w), np.zeros_like(w), 0.0, 0.0
        spe = steps_per_epoch(n)
        out = FitOutcome(curve=[], steps_run=total_steps)
        eval_steps = {s for s in range(1, total_steps + 1) if s % eval_every == 0} | {total_steps}
        beta1, beta2, eps = 0.9, 0.999, 1e-8
        for step in range(total_steps):
            epoch, idx = divmod(step, spe)
            perm = np.random.default_rng(seed * 7919 + epoch).permutation(n)
            sel = perm[idx * B_EFF:(idx + 1) * B_EFF]
            d = sigmoid(Z[sel] @ w + b) - yt[sel]
            gw, gb = Z[sel].T @ d / len(sel), float(d.mean())
            a = lr_at(step, lr * SURROGATE_LR_SCALE, schedule_steps)
            t = step + 1
            m_w, v_w = beta1 * m_w + (1 - beta1) * gw, beta2 * v_w + (1 - beta2) * gw ** 2
            m_b, v_b = beta1 * m_b + (1 - beta1) * gb, beta2 * v_b + (1 - beta2) * gb ** 2
            w = w - a * (m_w / (1 - beta1 ** t)) / (np.sqrt(v_w / (1 - beta2 ** t)) + eps)
            b = b - a * (m_b / (1 - beta1 ** t)) / (np.sqrt(v_b / (1 - beta2 ** t)) + eps)
            if eval_rows is not None and t in eval_steps:
                zs = self._score(w, b, mu, sd, np.asarray(eval_rows))
                out.curve.append((t, logloss_from_logodds(y[eval_rows], zs)))
                out.val_scores[t] = zs
        if score_sets:
            for name, r in score_sets.items():
                out.final_scores[name] = self._score(w, b, mu, sd, np.asarray(r))
        if save_path:   # persisted "adapter" of the surrogate (used for the fresh-set step on the mock backend)
            from pathlib import Path
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, "wb") as fh:
                np.savez(fh, mu=mu, sd=sd, w=w, b=np.array(b))
        return out


def apply_saved_surrogate(path, features: np.ndarray) -> np.ndarray:
    z = np.load(path)
    return (((np.asarray(features, dtype=np.float64) - z["mu"]) / z["sd"]) @ z["w"] + float(z["b"])).astype(np.float32)
