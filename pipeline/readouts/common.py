"""Shared helpers for the readouts: fold geometry, log loss, score-row construction, fit audit.

Row geometry (`Folds`) is the single place where problem-grouped folds become row indices, so
every readout uses the same outer split and the same inner splits (`FoldPlan.inner_splits`).
A sample whose problem is absent from the plan, or whose label under the active suite is -1
(no label: for example a problem excluded by the reference check), is not used and not scored.

The fit audit is a test hook. Every component that fits something (a scaler, a PCA, a classifier,
an imputation median, an isotonic map, an adapter) calls `record_fit(tag, problem_ids)` with the
problem IDs it was fit on. Tests switch the audit on and assert that no recorded set intersects
the outer test fold the fit belongs to (section 7: no test-fold information in any fit).
"""

from __future__ import annotations

import contextlib
import math
from dataclasses import dataclass
from typing import Iterable, Iterator, Sequence

import numpy as np
from scipy.special import expit

from pipeline.contracts.interfaces import ReadoutData
from pipeline.contracts.schemas import FitRecord, FoldPlan, ReadoutScore

EPS = 1e-12
NO_LABEL = -1

# ---------------------------------------------------------------------------------------------------
# Fit audit (test hook)
# ---------------------------------------------------------------------------------------------------
_AUDIT: list | None = None


@contextlib.contextmanager
def audit_fits() -> Iterator[list]:
    """Collect (tag, frozenset of problem IDs) for every fit made inside the context."""
    global _AUDIT
    prev = _AUDIT
    _AUDIT = []
    try:
        yield _AUDIT
    finally:
        _AUDIT = prev


def record_fit(tag: str, problem_ids: Iterable[str]) -> None:
    if _AUDIT is not None:
        _AUDIT.append((tag, frozenset(problem_ids)))


# ---------------------------------------------------------------------------------------------------
# Numerics
# ---------------------------------------------------------------------------------------------------
def sigmoid(x):
    return expit(np.asarray(x, dtype=np.float64))


def logit(p, eps: float = 1e-6):
    p = np.clip(np.asarray(p, dtype=np.float64), eps, 1.0 - eps)
    return np.log(p) - np.log1p(-p)


def logloss(y: np.ndarray, p: np.ndarray) -> float:
    """Mean binary log loss with probabilities clipped to [EPS, 1 - EPS]."""
    y = np.asarray(y, dtype=np.float64)
    p = np.clip(np.asarray(p, dtype=np.float64), EPS, 1.0 - EPS)
    if y.size == 0:
        return float("nan")
    return float(-np.mean(y * np.log(p) + (1.0 - y) * np.log1p(-p)))


def logloss_sum(y: np.ndarray, p: np.ndarray) -> float:
    y = np.asarray(y, dtype=np.float64)
    p = np.clip(np.asarray(p, dtype=np.float64), EPS, 1.0 - EPS)
    return float(-np.sum(y * np.log(p) + (1.0 - y) * np.log1p(-p)))


def logloss_from_logodds(y: np.ndarray, z: np.ndarray) -> float:
    """Binary cross-entropy of sigmoid(z) against y, computed stably from the log-odds."""
    y = np.asarray(y, dtype=np.float64)
    z = np.asarray(z, dtype=np.float64)
    if y.size == 0:
        return float("nan")
    return float(np.mean(np.logaddexp(0.0, z) - y * z))


def train_base_rate(y_train: np.ndarray) -> float:
    y_train = np.asarray(y_train)
    if y_train.size == 0:
        return 0.5
    return float(np.clip(np.mean(y_train), 1e-6, 1.0 - 1e-6))


def base_rate_logloss(y_train: np.ndarray, y_val: np.ndarray) -> float:
    """Log loss of the training base rate on a validation fold (the K4 reference)."""
    return logloss(y_val, np.full(len(y_val), train_base_rate(y_train)))


# ---------------------------------------------------------------------------------------------------
# Fold geometry
# ---------------------------------------------------------------------------------------------------
class Folds:
    """Row indices of the outer and inner splits for one (data, plan, label suite)."""

    def __init__(self, data: ReadoutData, plan: FoldPlan, label_suite: str | None):
        self.data = data
        self.plan = plan
        self.suite = label_suite
        self.n = len(data.sample_uids)
        self.pid = np.asarray(data.problem_ids, dtype=object)
        self.row_fold = np.array([plan.assignment.get(p, -1) for p in data.problem_ids], dtype=np.int64)
        if label_suite is None:
            self.y = np.full(self.n, NO_LABEL, dtype=np.int64)
        else:
            self.y = np.asarray(data.labels[label_suite]).astype(np.int64)
        self.valid = (self.row_fold >= 0) & (self.y != NO_LABEL if label_suite is not None else True)

    def rows_in_problems(self, problems: Sequence[str]) -> np.ndarray:
        m = np.isin(self.pid, np.asarray(list(problems), dtype=object)) & self.valid
        return np.flatnonzero(m)

    def outer_train(self, f: int) -> np.ndarray:
        return np.flatnonzero(self.valid & (self.row_fold != f))

    def outer_test(self, f: int) -> np.ndarray:
        return np.flatnonzero(self.valid & (self.row_fold == f))

    def inner(self, f: int) -> list[tuple[np.ndarray, np.ndarray]]:
        """Four (train rows, validation rows) inner splits; element 0 is the first inner split."""
        return [(self.rows_in_problems(tr), self.rows_in_problems(va)) for tr, va in self.plan.inner_splits(f)]

    def problems_of(self, rows: np.ndarray) -> set[str]:
        return set(self.pid[rows].tolist())

    @property
    def outer_folds(self) -> list[int]:
        return [f for f in range(self.plan.n_folds) if np.any(self.valid & (self.row_fold == f))]


# ---------------------------------------------------------------------------------------------------
# Score rows
# ---------------------------------------------------------------------------------------------------
def make_score(data: ReadoutData, row: int, *, model_key: str, population: str, readout: str,
               label_suite: str | None, fold_seed: int | None, fold: int | None, prob: float,
               rank_score: float, rank_tiebreak: float = float("nan"), missing: bool = False,
               imputed: bool = False, generation_set: str = "frozen", flagged: bool = False) -> ReadoutScore:
    return ReadoutScore(sample_uid=data.sample_uids[row], model_key=model_key, population=population,
                        readout=readout, label_suite=label_suite, fold_seed=fold_seed, fold=fold,
                        prob=float(prob), rank_score=float(rank_score), rank_tiebreak=float(rank_tiebreak),
                        missing=bool(missing), imputed=bool(imputed), generation_set=generation_set,
                        flagged=bool(flagged))


def scores_from_arrays(data: ReadoutData, rows: np.ndarray, rank: np.ndarray, prob: np.ndarray, *, folds: Folds,
                       model_key: str, population: str, readout: str, label_suite: str | None,
                       flagged: bool = False, fold_override: int | None = None) -> list[ReadoutScore]:
    out = []
    for r, rs, p in zip(rows, rank, prob):
        out.append(make_score(data, int(r), model_key=model_key, population=population, readout=readout,
                              label_suite=label_suite, fold_seed=folds.plan.fold_seed,
                              fold=int(folds.row_fold[r]) if fold_override is None else fold_override,
                              prob=float(p), rank_score=float(rs), flagged=flagged))
    return out


def fit_record(model_key: str, readout: str, label_suite: str, plan: FoldPlan, outer_fold: int, selected: dict,
               inner_val_logloss: float, base_rate_ll: float, retried: bool = False, flagged: bool = False) -> FitRecord:
    return FitRecord(model_key=model_key, readout=readout, label_suite=label_suite, fold_seed=plan.fold_seed,
                     outer_fold=int(outer_fold), selected=_jsonable(selected),
                     inner_val_logloss=float(inner_val_logloss), base_rate_logloss=float(base_rate_ll),
                     retried=bool(retried), flagged=bool(flagged))


def _jsonable(o):
    if isinstance(o, dict):
        return {str(k): _jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_jsonable(v) for v in o]
    if isinstance(o, np.generic):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    return o


def hidden_array(data: ReadoutData, key: str) -> np.ndarray:
    if data.hidden is None or key not in data.hidden:
        raise KeyError(f"ReadoutData.hidden lacks {key!r}")
    return data.hidden[key]


def is_finite(x: float) -> bool:
    return isinstance(x, (int, float)) and math.isfinite(x)
