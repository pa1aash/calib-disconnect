"""Code-text-only classifier CODETEXT (design 7.10, required version).

Features: character 3- to 5-gram TF-IDF (sublinear tf, min_df TFIDF_MIN_DF) of the extracted code,
fit on the training rows only (the vectorizer is refit inside every inner split and for the final fit).
Model: L2 logistic regression; C is chosen from PROBE_C_GRID by pooled log loss over the inner 4-fold
problem-grouped splits. A sample without extracted code is the empty string. If the training texts
leave an empty vocabulary the fit falls back to the training base rate.
"""

from __future__ import annotations

import warnings

import numpy as np
from scipy.special import expit
from sklearn.exceptions import ConvergenceWarning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from pipeline.contracts import constants as K
from pipeline.contracts.interfaces import ReadoutData
from pipeline.contracts.schemas import FitRecord, FoldPlan, ReadoutScore

from .common import Folds, base_rate_logloss, fit_record, logit, logloss_sum, record_fit, scores_from_arrays, train_base_rate


def _fit_predict(texts: np.ndarray, ytr: np.ndarray, tr: np.ndarray, aps: list[np.ndarray], Cs, tag: str, pids):
    """Logits per C for each apply set. texts: object array of code strings."""
    record_fit(f"{tag}:tfidf", pids)
    if len(np.unique(ytr)) < 2:
        c = float(logit(train_base_rate(ytr)))
        return {C: [np.full(len(a), c) for a in aps] for C in Cs}
    vec = TfidfVectorizer(analyzer="char", ngram_range=K.TFIDF_NGRAM_RANGE, sublinear_tf=True, min_df=K.TFIDF_MIN_DF,
                          lowercase=False, dtype=np.float32)
    try:
        Xtr = vec.fit_transform(texts[tr])
    except ValueError:  # empty vocabulary
        c = float(logit(train_base_rate(ytr)))
        return {C: [np.full(len(a), c) for a in aps] for C in Cs}
    Xaps = [vec.transform(texts[a]) for a in aps]
    record_fit(f"{tag}:classifier", pids)
    clf = LogisticRegression(max_iter=500, warm_start=True)
    out = {}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ConvergenceWarning)
        for C in sorted(Cs):
            clf.set_params(C=C)
            clf.fit(Xtr, ytr)
            out[C] = [clf.decision_function(X).astype(np.float64) for X in Xaps]
    return out


def crossfit_codetext(data: ReadoutData, plan: FoldPlan, label_suite: str, model_key: str, population: str, *,
                      C_grid=K.PROBE_C_GRID) -> tuple[list[ReadoutScore], list[FitRecord]]:
    if data.code_texts is None:
        raise ValueError("CODETEXT needs ReadoutData.code_texts")
    texts = np.array([t or "" for t in data.code_texts], dtype=object)
    F = Folds(data, plan, label_suite)
    scores, fits = [], []
    for f in F.outer_folds:
        inner = F.inner(f)
        acc = {C: 0.0 for C in C_grid}
        n_val, base_sum = 0, 0.0
        for j, (tr, va) in enumerate(inner):
            if len(tr) == 0 or len(va) == 0:
                continue
            lg = _fit_predict(texts, F.y[tr], tr, [va], C_grid, f"codetext:outer{f}:inner{j}", F.problems_of(tr))
            for C in C_grid:
                acc[C] += logloss_sum(F.y[va], expit(lg[C][0]))
            n_val += len(va)
            base_sum += base_rate_logloss(F.y[tr], F.y[va]) * len(va)
        cv = {C: acc[C] / max(n_val, 1) for C in C_grid}
        C_best = min(C_grid, key=lambda C: cv[C])
        tr, te = F.outer_train(f), F.outer_test(f)
        lg = _fit_predict(texts, F.y[tr], tr, [te], [C_best], f"codetext:outer{f}:final", F.problems_of(tr))[C_best][0]
        scores += scores_from_arrays(data, te, lg, expit(lg), folds=F, model_key=model_key, population=population,
                                     readout="CODETEXT", label_suite=label_suite)
        fits.append(fit_record(model_key, "CODETEXT", label_suite, plan, f, {"C": C_best, "ngram_range": list(K.TFIDF_NGRAM_RANGE)},
                               cv[C_best], base_sum / max(n_val, 1)))
    return scores, fits
