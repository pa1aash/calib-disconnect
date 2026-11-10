"""Zero-shot verbal readouts (design 7.2).

V1: the parsed integer / 100 (`CaptureRecord.v1_value`; None means unparsed). An unparsed answer is
missing and is never set to a default. The primary score imputes it with the training-fold median of
the parsed values of the same model (per outer fold, never the test fold's values), flags it
`missing=True, imputed=True`, and imputed samples tie. A sensitivity readout (`SZ_V1_drop`) drops the
missing rows instead. K3: when the parse rate is below K3_MIN_V1_PARSE_RATE the model's primary
chain switches to V2 (`v1_parse_report`).

V2: the stored float32 log-odds log P(Yes) - log P(No) at p3 is the rank score; prob is its logistic
transform. It is never missing.

Edge case (documented): if a training fold holds no parsed value at all, the imputation value is
0.5 and `imputed=True`; the readout is degenerate for that fold anyway.
"""

from __future__ import annotations

import numpy as np

from pipeline.contracts import constants as K
from pipeline.contracts.interfaces import ReadoutData
from pipeline.contracts.schemas import FoldPlan, ReadoutScore

from .common import make_score, record_fit, sigmoid


def v1_parse_report(data: ReadoutData) -> dict:
    """Parse rate over all samples and whether the K3 switch to V2 fires."""
    n = len(data.sample_uids)
    parsed = sum(1 for c in (data.capture or []) if c.v1_value is not None)
    rate = parsed / n if n else float("nan")
    return {"n": n, "n_parsed": parsed, "parse_rate": rate,
            "k3_switch_to_v2": bool(n and rate < K.K3_MIN_V1_PARSE_RATE)}


def _row_folds(data: ReadoutData, plan: FoldPlan) -> np.ndarray:
    return np.array([plan.assignment.get(p, -1) for p in data.problem_ids], dtype=np.int64)


def _v1_values(data: ReadoutData) -> tuple[np.ndarray, np.ndarray]:
    if data.capture is None:
        raise ValueError("V1 needs ReadoutData.capture")
    parsed = np.array([c.v1_value is not None for c in data.capture], dtype=bool)
    vals = np.array([float(c.v1_value) if c.v1_value is not None else np.nan for c in data.capture])
    return vals, parsed


def v1_training_median(data: ReadoutData, plan: FoldPlan, outer_fold: int) -> float:
    """Median of the parsed V1 values over samples of the training folds of `outer_fold`."""
    vals, parsed = _v1_values(data)
    rf = _row_folds(data, plan)
    m = parsed & (rf >= 0) & (rf != outer_fold)
    record_fit(f"v1_median:outer{outer_fold}", [p for p, k in zip(data.problem_ids, m) if k])
    return float(np.median(vals[m])) if m.any() else 0.5


def v1_scores(data: ReadoutData, plan: FoldPlan, model_key: str, population: str, *, drop_missing: bool = False,
              rows_of_fold: dict[int, np.ndarray] | None = None, mode: str = "test",
              readout: str | None = None) -> list[ReadoutScore]:
    """V1 rows. mode="test": each sample is scored with the median of its own outer fold's training folds
    (the out-of-fold analysis set). mode="train": returns, for the isotonic map, the training-fold rows of
    each outer fold; use `v1_train_scores`."""
    name = readout or ("SZ_V1_drop" if drop_missing else "SZ_V1")
    vals, parsed = _v1_values(data)
    rf = _row_folds(data, plan)
    meds = {f: v1_training_median(data, plan, f) for f in range(plan.n_folds)}
    out = []
    for i in range(len(data.sample_uids)):
        f = int(rf[i])
        if f < 0:
            continue
        if parsed[i]:
            v, miss, imp = float(vals[i]), False, False
        elif drop_missing:
            continue
        else:
            v, miss, imp = meds[f], True, True
        out.append(make_score(data, i, model_key=model_key, population=population, readout=name, label_suite=None,
                              fold_seed=plan.fold_seed, fold=f, prob=v, rank_score=v, missing=miss, imputed=imp))
    return out


def v1_train_scores(data: ReadoutData, plan: FoldPlan, model_key: str, population: str, *,
                    drop_missing: bool = False) -> dict[int, list[ReadoutScore]]:
    """For each outer fold f, the V1 scores of the training-fold samples with fold f's imputation value.
    Pass to `crossfit_isotonic(..., train_scores=...)` so that no imputation value comes from the test fold."""
    name = "SZ_V1_drop" if drop_missing else "SZ_V1"
    vals, parsed = _v1_values(data)
    rf = _row_folds(data, plan)
    out: dict[int, list[ReadoutScore]] = {}
    for f in range(plan.n_folds):
        med = v1_training_median(data, plan, f)
        rows = []
        for i in range(len(data.sample_uids)):
            if rf[i] < 0 or rf[i] == f:
                continue
            if parsed[i]:
                v, miss, imp = float(vals[i]), False, False
            elif drop_missing:
                continue
            else:
                v, miss, imp = med, True, True
            rows.append(make_score(data, i, model_key=model_key, population=population, readout=name, label_suite=None,
                                   fold_seed=plan.fold_seed, fold=int(rf[i]), prob=v, rank_score=v, missing=miss,
                                   imputed=imp))
        out[f] = rows
    return out


def v2_scores(data: ReadoutData, model_key: str, population: str) -> list[ReadoutScore]:
    """rank_score = the stored float32 log-odds; prob = sigmoid(log-odds). Unsupervised: no fold fields."""
    if data.capture is None:
        raise ValueError("V2 needs ReadoutData.capture")
    out = []
    for i, c in enumerate(data.capture):
        z = float(np.float32(c.yes_no_logodds))
        out.append(make_score(data, i, model_key=model_key, population=population, readout="SZ_V2", label_suite=None,
                              fold_seed=None, fold=None, prob=float(sigmoid(z)), rank_score=z))
    return out


class V1Readout:
    """UnsupervisedReadout-shaped wrapper (fold fields are filled from the plan given at construction)."""

    def __init__(self, plan: FoldPlan, drop_missing: bool = False):
        self.plan, self.drop_missing = plan, drop_missing
        self.name = "SZ_V1_drop" if drop_missing else "SZ_V1"

    def score(self, data: ReadoutData, model_key: str, population: str) -> list[ReadoutScore]:
        return v1_scores(data, self.plan, model_key, population, drop_missing=self.drop_missing)


class V2Readout:
    name = "SZ_V2"

    def score(self, data: ReadoutData, model_key: str, population: str) -> list[ReadoutScore]:
        return v2_scores(data, model_key, population)
