"""Isotonic recalibration of a stated readout (design 7.3 and the tie rule of 1.2).

`crossfit_isotonic` follows the contract signature. For each outer fold f an isotonic regression of y
on the readout's rank_score is fit on the training-fold samples and applied to the test-fold samples:

  * the training-fold scores are `train_scores[f]` when given (S^T: inner cross-fitted scores, or the
    final adapter's in-sample scores for the secondary strata, LiveCodeBench, and seed refits), else the
    readout's own scores for samples of the other folds (zero-shot readouts);
  * out_of_bounds = "clip"; a single-class training set maps to the training base rate;
  * output rows are `iso:<name>` with prob = rank_score = the mapped value and rank_tiebreak = the
    pre-map rank_score, so ranking by (rank_score, rank_tiebreak) never merges samples that the pre-map
    score separated (an isotonic map is non-decreasing, so within a problem the lexicographic order
    equals the pre-map order).

Rows that are missing and not imputed (AGREE without inputs, TL without code tokens) or that have a
non-finite score are not mapped and not used to fit; imputed V1 rows are mapped like any other score.
"""

from __future__ import annotations

from typing import Mapping, Sequence

import numpy as np
from sklearn.isotonic import IsotonicRegression

from pipeline.contracts.interfaces import ReadoutData
from pipeline.contracts.schemas import FoldPlan, ReadoutScore, iso

from .common import NO_LABEL, record_fit, train_base_rate


def fit_isotonic(x: np.ndarray, y: np.ndarray):
    """Return a callable mapping scores to [0, 1]. Single-class training sets give the base rate."""
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    if len(x) == 0 or len(np.unique(y)) < 2:
        c = train_base_rate(y)
        return lambda z: np.full(len(np.atleast_1d(z)), c)
    ir = IsotonicRegression(increasing=True, y_min=0.0, y_max=1.0, out_of_bounds="clip")
    ir.fit(x, y)
    return lambda z: ir.predict(np.asarray(z, dtype=np.float64))


def _usable(s: ReadoutScore) -> bool:
    # imputed rows (V1) are missing AND imputed: their imputed value is the score. Plain missing rows have none.
    return (s.imputed or not s.missing) and bool(np.isfinite(s.rank_score))


def crossfit_isotonic(scores: Sequence[ReadoutScore], data: ReadoutData, plan: FoldPlan, label_suite: str,
                      train_scores: Mapping[int, Sequence[ReadoutScore]] | None = None) -> list[ReadoutScore]:
    uid_row = {u: i for i, u in enumerate(data.sample_uids)}
    y_all = np.asarray(data.labels[label_suite]).astype(np.int64)

    def info(s: ReadoutScore):
        i = uid_row.get(s.sample_uid)
        if i is None:
            return None
        f = plan.assignment.get(data.problem_ids[i], -1)
        if f < 0 or y_all[i] == NO_LABEL:
            return None
        return i, f, int(y_all[i])

    own = [(s, info(s)) for s in scores if _usable(s)]
    own = [(s, t) for s, t in own if t is not None]
    out: list[ReadoutScore] = []
    folds = sorted({t[1] for _, t in own})
    for f in folds:
        if train_scores is not None and f in train_scores:
            tr = [(s, info(s)) for s in train_scores[f] if _usable(s)]
            tr = [(s, t) for s, t in tr if t is not None]
            tr = [(s, t) for s, t in tr if t[1] != f]  # defensive: a training row never comes from the test fold
        else:
            tr = [(s, t) for s, t in own if t[1] != f]
        record_fit(f"isotonic:outer{f}", [data.problem_ids[t[0]] for _, t in tr])
        m = fit_isotonic(np.array([s.rank_score for s, _ in tr]), np.array([t[2] for _, t in tr]))
        te = [(s, t) for s, t in own if t[1] == f]
        if not te:
            continue
        mapped = m(np.array([s.rank_score for s, _ in te]))
        for (s, t), v in zip(te, mapped):
            out.append(ReadoutScore(sample_uid=s.sample_uid, model_key=s.model_key, population=s.population,
                                    readout=iso(_base_name(s.readout)), label_suite=label_suite,
                                    fold_seed=plan.fold_seed, fold=f, prob=float(v), rank_score=float(v),
                                    rank_tiebreak=float(s.rank_score), missing=s.missing, imputed=s.imputed,
                                    generation_set=s.generation_set, flagged=s.flagged))
    return out


def _base_name(readout: str) -> str:
    return readout[4:] if readout.startswith("iso:") else readout


def rename_iso(rows: Sequence[ReadoutScore], name: str) -> list[ReadoutScore]:
    """Relabel `iso:<x>` rows as `iso:<name>` (for the sensitivity variants)."""
    import dataclasses
    return [dataclasses.replace(r, readout=iso(name)) for r in rows]


def drop_inner_split(train_scores: Mapping[int, Sequence[ReadoutScore]], data: ReadoutData, plan: FoldPlan,
                     split: int = 0) -> dict[int, list[ReadoutScore]]:
    """Sensitivity (red team V13f): the training scores of outer fold f without the rows of inner split
    `split`'s validation fold (default the first inner split, so the map uses inner splits 2 to 4 only)."""
    uid_row = {u: i for i, u in enumerate(data.sample_uids)}
    out: dict[int, list[ReadoutScore]] = {}
    for f, rows in train_scores.items():
        train_folds = [g for g in range(plan.n_folds) if g != f]
        drop_fold = train_folds[split]
        keep = []
        for s in rows:
            i = uid_row.get(s.sample_uid)
            if i is not None and plan.assignment.get(data.problem_ids[i], -1) != drop_fold:
                keep.append(s)
        out[f] = keep
    return out
