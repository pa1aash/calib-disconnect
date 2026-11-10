"""Shared helpers: weight validation and ScoredSet construction."""

from __future__ import annotations

import numpy as np

from pipeline.contracts.schemas import ScoredSet


def as_weights(n: int, weights: np.ndarray | None) -> np.ndarray:
    """Per-sample weights as float64. None means unit weights. Weights are the bootstrap
    multiplicity of the sample's problem, so they are non-negative integers in every use; the
    functions that need integer weights (equal-mass binning) check that separately."""
    if weights is None:
        return np.ones(n, dtype=np.float64)
    w = np.asarray(weights, dtype=np.float64)
    if w.shape != (n,):
        raise ValueError(f"weights must have shape ({n},), got {w.shape}")
    if not np.all(np.isfinite(w)) or np.any(w < 0):
        raise ValueError("weights must be finite and non-negative")
    return w


def require_integer_weights(w: np.ndarray) -> None:
    if not np.all(w == np.round(w)):
        raise ValueError("this estimator needs integer weights (bootstrap multiplicities)")


def make_scored_set(problem_index, y, rank_score, rank_tiebreak=None, prob=None) -> ScoredSet:
    """Build a ScoredSet with the dtypes of the contract. prob defaults to rank_score and
    rank_tiebreak to NaN (no tie-break)."""
    pi = np.asarray(problem_index, dtype=np.int64)
    yy = np.asarray(y)
    if not np.all((yy == 0) | (yy == 1)):
        raise ValueError("labels must be 0 or 1")
    rs = np.asarray(rank_score, dtype=np.float64)
    tb = np.full(rs.shape, np.nan) if rank_tiebreak is None else np.asarray(rank_tiebreak, dtype=np.float64)
    pr = rs.copy() if prob is None else np.asarray(prob, dtype=np.float64)
    n = pi.shape[0]
    for name, a in (("y", yy), ("rank_score", rs), ("rank_tiebreak", tb), ("prob", pr)):
        if a.shape != (n,):
            raise ValueError(f"{name} must have shape ({n},)")
    if np.any(pi < 0):
        raise ValueError("problem_index must be non-negative")
    return ScoredSet(problem_index=pi, y=yy.astype(np.int8), rank_score=rs, rank_tiebreak=tb, prob=pr)


def subset(s: ScoredSet, mask: np.ndarray) -> ScoredSet:
    m = np.asarray(mask, dtype=bool)
    return ScoredSet(problem_index=s.problem_index[m], y=s.y[m], rank_score=s.rank_score[m],
                     rank_tiebreak=s.rank_tiebreak[m], prob=s.prob[m])


def n_problems_of(s: ScoredSet, n_problems: int | None = None) -> int:
    if n_problems is not None:
        return int(n_problems)
    return int(s.problem_index.max()) + 1 if s.problem_index.size else 0


def none_if_nan(x: float) -> float | None:
    return None if x is None or not np.isfinite(x) else float(x)
