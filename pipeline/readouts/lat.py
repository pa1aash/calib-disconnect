"""LAT direction readout (Ribeiro analog, design section 2.2; not binding).

Direction: for every training problem with at least one passing and one failing sample, the difference
between the mean hidden state (at p2) of its passing samples and of its failing samples. The first
principal axis of these per-problem differences is the top right singular vector of the stacked,
uncentered difference matrix (the mean difference is the signal, so the matrix is not centered). The
sign is aligned so that passing training samples have the higher mean projection. Score of a sample:
the projection of its centered state (training mean subtracted) on the direction. The layer is chosen on
the first inner split by pooled AUROC of the projection on the inner validation fold. `prob` is a
one-dimensional logistic calibration of the projection fit on the outer training rows (it is only used
where a probability is needed). If no training problem is mixed, the score is 0 and prob the training
base rate.
"""

from __future__ import annotations

import warnings
from collections import defaultdict

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

from pipeline.contracts.interfaces import ReadoutData
from pipeline.contracts.schemas import FitRecord, FoldPlan, ReadoutScore

from .common import Folds, base_rate_logloss, fit_record, hidden_array, record_fit, scores_from_arrays, train_base_rate


def lat_direction(X: np.ndarray, y: np.ndarray, problems: np.ndarray) -> tuple[np.ndarray | None, np.ndarray]:
    mu = X.mean(axis=0)
    by: dict[str, list[int]] = defaultdict(list)
    for i, p in enumerate(problems):
        by[p].append(i)
    diffs = []
    for idx in by.values():
        idx = np.asarray(idx)
        yp, yf = idx[y[idx] == 1], idx[y[idx] == 0]
        if len(yp) and len(yf):
            diffs.append(X[yp].mean(axis=0) - X[yf].mean(axis=0))
    if not diffs:
        return None, mu
    _, _, vt = np.linalg.svd(np.stack(diffs), full_matrices=False)
    v = vt[0]
    proj = (X - mu) @ v
    if proj[y == 1].size and proj[y == 0].size and proj[y == 1].mean() < proj[y == 0].mean():
        v = -v
    return v, mu


def _auc(y: np.ndarray, s: np.ndarray) -> float:
    return float(roc_auc_score(y, s)) if len(np.unique(y)) == 2 else 0.5


def crossfit_lat(data: ReadoutData, plan: FoldPlan, label_suite: str, model_key: str, population: str, *,
                 key: str = "hs_p2") -> tuple[list[ReadoutScore], list[FitRecord]]:
    H = hidden_array(data, key)
    F = Folds(data, plan, label_suite)
    scores, fits = [], []
    for f in F.outer_folds:
        tr0, va0 = F.inner(f)[0]
        best_l, best_auc = 0, -1.0
        if len(tr0) and len(va0):
            record_fit(f"lat:outer{f}:inner0", F.problems_of(tr0))
            for l in range(H.shape[1]):
                v, mu = lat_direction(H[tr0, l, :].astype(np.float64), F.y[tr0], F.pid[tr0])
                a = 0.5 if v is None else _auc(F.y[va0], (H[va0, l, :] - mu) @ v)
                if a > best_auc:
                    best_l, best_auc = l, a
        tr, te = F.outer_train(f), F.outer_test(f)
        record_fit(f"lat:outer{f}:final", F.problems_of(tr))
        Xtr = H[tr, best_l, :].astype(np.float64)
        v, mu = lat_direction(Xtr, F.y[tr], F.pid[tr])
        if v is None:
            rank = np.zeros(len(te))
            prob = np.full(len(te), train_base_rate(F.y[tr]))
        else:
            ptr = (Xtr - mu) @ v
            rank = (H[te, best_l, :] - mu) @ v
            if len(np.unique(F.y[tr])) < 2:
                prob = np.full(len(te), train_base_rate(F.y[tr]))
            else:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    cal = LogisticRegression(C=1.0).fit(ptr.reshape(-1, 1), F.y[tr])
                prob = cal.predict_proba(rank.reshape(-1, 1))[:, 1]
        scores += scores_from_arrays(data, te, rank, prob, folds=F, model_key=model_key, population=population,
                                     readout="LAT", label_suite=label_suite)
        base = base_rate_logloss(F.y[tr0], F.y[va0]) if len(tr0) and len(va0) else float("nan")
        fits.append(fit_record(model_key, "LAT", label_suite, plan, f,
                               {"layer": best_l, "position": key.replace("hs_", ""), "inner_val_auroc": best_auc},
                               float("nan"), base))
    return scores, fits
