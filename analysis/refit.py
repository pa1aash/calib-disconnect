"""Repeated cross-fitting and the refit widening of the decision interval (design section 9).

- Per model m and fold seed s in FOLD_SEEDS (0, 1, 2): the per-seed residual R_{m,s}.
- R_m = mean over the three seeds; R_bar = mean of R_m over the models.
- Bootstrap: the same problem draw is applied to all three seeds, so the replicate of R_bar is the
  seed-averaged statistic and h is the bootstrap half-width of its percentile interval.
- sigma2_m = between-seed sample variance (ddof 1, 2 degrees of freedom) of the three R_{m,s}.
- s2_refit = (1/3) (1/M^2) sum_m sigma2_m, with M = 6 primary models: (1/3)(1/36) sum_m sigma2_m,
  pooled over 2M = 12 degrees of freedom.
- Widened interval: centered at the percentile interval's center (lo + hi)/2, half-width
  sqrt(h^2 + (t s_refit)^2), t = t_{12, 0.95} = 1.782 (T12_QUANTILE). For another number of models
  (the K4 sensitivity over unflagged models) the degrees of freedom are 2M and t is the Student
  quantile at that df; at other one-sided levels (the Holm steps) t is t_{df, 1 - alpha'}.
"""

from __future__ import annotations

from typing import Mapping, Sequence

import numpy as np
from scipy.stats import t as student_t

from pipeline.contracts.constants import FOLD_SEEDS, N_REFIT_DF, T12_QUANTILE


def seed_average(per_model_seed_r: Mapping[str, Sequence[float]]) -> dict[str, float]:
    out = {}
    for m, v in per_model_seed_r.items():
        a = np.asarray(v, dtype=np.float64)
        if a.shape != (len(FOLD_SEEDS),):
            raise ValueError(f"model {m}: need one residual per fold seed {FOLD_SEEDS}")
        out[m] = float(a.mean())
    return out


def seed_averaged_replicates(per_model_seed_reps: Mapping[str, Sequence[np.ndarray]]) -> dict[str, np.ndarray]:
    """Per-model seed-averaged replicates; the three arrays must come from the same draws."""
    out = {}
    for m, reps in per_model_seed_reps.items():
        a = np.vstack([np.asarray(r, dtype=np.float64) for r in reps])
        if a.shape[0] != len(FOLD_SEEDS):
            raise ValueError(f"model {m}: need replicates for each fold seed")
        out[m] = a.mean(axis=0)          # NaN if any seed is undefined in that resample
    return out


def mean_over_models(per_model: Mapping[str, np.ndarray | float]):
    vals = [np.asarray(v, dtype=np.float64) for v in per_model.values()]
    return np.mean(np.stack(vals), axis=0)


def between_seed_variance(per_model_seed_r: Mapping[str, Sequence[float]]) -> dict[str, float]:
    return {m: float(np.var(np.asarray(v, dtype=np.float64), ddof=1)) for m, v in per_model_seed_r.items()}


def s2_refit(sigma2: Mapping[str, float]) -> float:
    """(1/3) (1/M^2) sum_m sigma2_m."""
    m = len(sigma2)
    if m == 0:
        raise ValueError("no models")
    return float(np.sum(list(sigma2.values())) / (len(FOLD_SEEDS) * m * m))


def s2_refit_single_model(sigma2: Mapping[str, float]) -> float:
    """Refit variance of one model's seed mean under the pooling assumption of section 9 (equal
    between-seed variance across models): (1/3) times the pooled sigma2, mean_m sigma2_m."""
    return float(np.mean(list(sigma2.values())) / len(FOLD_SEEDS))


def refit_df(n_models: int) -> int:
    return (len(FOLD_SEEDS) - 1) * n_models


def t_quantile(df: int, one_sided_level: float = 0.95) -> float:
    """t_{df, level}; the design's constant 1.782 at df = 12 and level 0.95."""
    if df == N_REFIT_DF and abs(one_sided_level - 0.95) < 1e-15:
        return T12_QUANTILE
    return float(student_t.ppf(one_sided_level, df))


def widen(lo: float, hi: float, s_refit: float, t: float) -> dict[str, float]:
    """Symmetric widening about the percentile interval's center."""
    center = (lo + hi) / 2.0
    h = (hi - lo) / 2.0
    half = float(np.sqrt(h * h + (t * s_refit) ** 2))
    return {"center": center, "h": h, "half": half, "lo": center - half, "hi": center + half}
