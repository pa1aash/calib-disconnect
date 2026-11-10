"""Discrimination and Brier metrics (design section 8), with problem-weighted fast paths (section 9).

Conventions.
- Ranking metrics use the dense lexicographic keys of analysis.ranking, so ties are exact ties of
  (rank_score, rank_tiebreak), and every Mann-Whitney count scores a tie as one half.
- `weights` are per-sample weights equal to the bootstrap multiplicity of the sample's problem.
  A weighted value equals the unweighted value on the data in which each problem is duplicated that
  many times, each copy being a distinct problem (the cluster bootstrap). Pooled metrics therefore
  weight a pair (a, b) by w_a w_b; within-problem metrics weight problem i by its multiplicity c_i,
  because pairs across two copies of a problem are pairs of different problems. Within-problem
  functions require weights that are constant within a problem.
- A metric that is undefined returns None (pooled AUROC with one class, W with no mixed problem,
  AUPRC with no positive). It is never imputed (section 11, row 7.7).

Fast path (section 9, cost note). `RankStats` precomputes, once per (readout, label suite), the
per-problem pass and fail counts p_i and f_i, and the matrix U with
U[i, j] = sum over passing a of problem i and failing b of problem j of 1[s_a > s_b] + 1/2 1[s_a = s_b].
For a resample with problem multiplicities c (one row of BootstrapDraws.counts):

    pooled AUROC = c' U c / ((c . p)(c . f)),
    W            = sum_i c_i U[i, i] / sum_i c_i p_i f_i,

so every resample is a weighted sum over problems. Tests verify both against the direct functions
on the duplicated data.
"""

from __future__ import annotations

from typing import Mapping

import numpy as np

from pipeline.contracts.constants import ECE_EQUAL_MASS_BINS
from pipeline.contracts.schemas import ScoredSet

from ._common import as_weights, n_problems_of
from .calibration import equal_mass_bin_index
from .ranking import keys_of

MURPHY_IDENTITY_TOL = 1e-12


# ---------------------------------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------------------------------
def _mw_from_keys(keys: np.ndarray, y: np.ndarray, w: np.ndarray) -> tuple[float, float, float]:
    """Weighted Mann-Whitney count sum_{a pass, b fail} w_a w_b (1[k_a > k_b] + 1/2 1[k_a = k_b]),
    and the weighted pass and fail totals."""
    if keys.size == 0:
        return 0.0, 0.0, 0.0
    k = int(keys.max()) + 1
    pos = np.bincount(keys, weights=w * (y == 1), minlength=k)
    neg = np.bincount(keys, weights=w * (y == 0), minlength=k)
    neg_lt = np.cumsum(neg) - neg
    return float(np.sum(pos * (neg_lt + 0.5 * neg))), float(pos.sum()), float(neg.sum())


def problem_weights(s: ScoredSet, w: np.ndarray, n_problems: int) -> np.ndarray:
    """Per-problem weight, checking that weights are constant within each problem."""
    pi = s.problem_index
    wmax = np.full(n_problems, -np.inf)
    wmin = np.full(n_problems, np.inf)
    np.maximum.at(wmax, pi, w)
    np.minimum.at(wmin, pi, w)
    present = np.isfinite(wmax)
    if np.any(wmax[present] != wmin[present]):
        raise ValueError("within-problem metrics need weights that are constant within a problem")
    out = np.zeros(n_problems)
    out[present] = wmax[present]
    return out


def per_problem_counts(s: ScoredSet, n_problems: int | None = None, use_tiebreak: bool = True) -> dict[str, np.ndarray]:
    """Unweighted per-problem pass count p, fail count f, Mann-Whitney count A (ties one half),
    and tied pass-fail pair count T."""
    n_p = n_problems_of(s, n_problems)
    keys = keys_of(s, use_tiebreak)
    y = np.asarray(s.y)
    pi = s.problem_index
    npos = np.bincount(pi, weights=(y == 1).astype(float), minlength=n_p)
    nneg = np.bincount(pi, weights=(y == 0).astype(float), minlength=n_p)
    A = np.zeros(n_p)
    T = np.zeros(n_p)
    if keys.size:
        kk = int(keys.max()) + 1
        comp = pi.astype(np.int64) * kk + keys
        uc, inv = np.unique(comp, return_inverse=True)
        pos = np.bincount(inv, weights=(y == 1).astype(float), minlength=uc.size)
        neg = np.bincount(inv, weights=(y == 0).astype(float), minlength=uc.size)
        prob_u = uc // kk
        cneg = np.cumsum(neg) - neg
        first = np.searchsorted(prob_u, prob_u, side="left")
        neg_lt = cneg - cneg[first]
        A = np.bincount(prob_u, weights=pos * (neg_lt + 0.5 * neg), minlength=n_p)
        T = np.bincount(prob_u, weights=pos * neg, minlength=n_p)
    return {"p": npos, "f": nneg, "A": A, "T": T}


# ---------------------------------------------------------------------------------------------------
# Pooled discrimination
# ---------------------------------------------------------------------------------------------------
def auroc_pooled(s: ScoredSet, weights: np.ndarray | None = None, use_tiebreak: bool = True) -> float | None:
    """Pooled AUROC (Mann-Whitney, ties one half)."""
    w = as_weights(s.y.size, weights)
    num, p, f = _mw_from_keys(keys_of(s, use_tiebreak), np.asarray(s.y), w)
    if p <= 0 or f <= 0:
        return None
    return num / (p * f)


def auroc_pooled_mixed(s: ScoredSet, weights: np.ndarray | None = None, n_problems: int | None = None,
                       use_tiebreak: bool = True) -> float | None:
    """d diagnostic: pooled AUROC restricted to the samples of mixed problems (section 8)."""
    n_p = n_problems_of(s, n_problems)
    c = per_problem_counts(s, n_p, use_tiebreak)
    mixed = (c["p"] > 0) & (c["f"] > 0)
    m = mixed[s.problem_index]
    if not m.any():
        return None
    w = as_weights(s.y.size, weights)
    keys = keys_of(s, use_tiebreak)
    num, p, f = _mw_from_keys(keys[m], np.asarray(s.y)[m], w[m])
    if p <= 0 or f <= 0:
        return None
    return num / (p * f)


def auroc_fold_averaged(s: ScoredSet, fold_of_problem: np.ndarray, weights: np.ndarray | None = None,
                        use_tiebreak: bool = True) -> float | None:
    """d diagnostic: mean over folds of the per-fold pooled AUROC (section 8). Undefined if any fold
    that holds samples has zero total weight or an undefined AUROC."""
    w = as_weights(s.y.size, weights)
    keys = keys_of(s, use_tiebreak)
    fold = np.asarray(fold_of_problem)[s.problem_index]
    vals = []
    for f_id in np.unique(fold):
        m = (fold == f_id) & (w > 0)
        if not m.any():
            return None
        num, p, f = _mw_from_keys(keys[m], np.asarray(s.y)[m], w[m])
        if p <= 0 or f <= 0:
            return None
        vals.append(num / (p * f))
    return float(np.mean(vals)) if vals else None


def auprc(s: ScoredSet, positive: int = 1, weights: np.ndarray | None = None,
          use_tiebreak: bool = True) -> float | None:
    """Average precision for the class `positive` (1 = pass, ranked by descending confidence;
    0 = fail, ranked by ascending confidence): AP = sum_k (TP_k - TP_{k-1}) / P * TP_k / (TP_k + FP_k)
    over the distinct key values from the most to the least confident for that class (tied samples
    enter together)."""
    if positive not in (0, 1):
        raise ValueError("positive must be 0 or 1")
    w = as_weights(s.y.size, weights)
    keys = keys_of(s, use_tiebreak)
    if keys.size == 0:
        return None
    is_pos = (np.asarray(s.y) == positive)
    kk = int(keys.max()) + 1
    tp = np.bincount(keys, weights=w * is_pos, minlength=kk)
    fp = np.bincount(keys, weights=w * ~is_pos, minlength=kk)
    if positive == 1:
        tp, fp = tp[::-1], fp[::-1]
    total = tp.sum()
    if total <= 0:
        return None
    TP = np.cumsum(tp)
    FP = np.cumsum(fp)
    nz = (TP + FP) > 0
    return float(np.sum(tp[nz] / total * TP[nz] / (TP[nz] + FP[nz])))


def base_rate(s: ScoredSet, positive: int = 1, weights: np.ndarray | None = None) -> float | None:
    """Share of the class `positive`, printed beside AUPRC (section 8)."""
    w = as_weights(s.y.size, weights)
    n = w.sum()
    if n <= 0:
        return None
    return float(np.sum(w * (np.asarray(s.y) == positive)) / n)


# ---------------------------------------------------------------------------------------------------
# Within-problem discrimination
# ---------------------------------------------------------------------------------------------------
def within_problem_auroc(s: ScoredSet, weights: np.ndarray | None = None, use_tiebreak: bool = True,
                         n_problems: int | None = None) -> float | None:
    """W, the pair-weighted within-problem AUROC (section 8):
    W = sum_i sum_{a in P_i} sum_{b in F_i} (1[s_a > s_b] + 1/2 1[s_a = s_b]) / sum_i |P_i||F_i|.
    All-pass and all-fail problems drop out. None if no mixed problem."""
    n_p = n_problems_of(s, n_problems)
    c = per_problem_counts(s, n_p, use_tiebreak)
    pw = problem_weights(s, as_weights(s.y.size, weights), n_p)
    den = float(np.sum(pw * c["p"] * c["f"]))
    if den <= 0:
        return None
    return float(np.sum(pw * c["A"]) / den)


def within_problem_auroc_avg(s: ScoredSet, weights: np.ndarray | None = None, use_tiebreak: bool = True,
                             n_problems: int | None = None) -> float | None:
    """W_avg: the mean over mixed problems of the per-problem AUROC, each mixed problem weighted
    equally (section 8, secondary; Miglani et al. 2609.36783)."""
    n_p = n_problems_of(s, n_problems)
    c = per_problem_counts(s, n_p, use_tiebreak)
    pw = problem_weights(s, as_weights(s.y.size, weights), n_p)
    pairs = c["p"] * c["f"]
    m = (pairs > 0) & (pw > 0)
    if not m.any():
        return None
    return float(np.sum(pw[m] * c["A"][m] / pairs[m]) / np.sum(pw[m]))


def mixed_counts(s: ScoredSet, n_problems: int | None = None) -> dict[str, int]:
    """Problem counts by type and the number of within-problem pass-fail pairs."""
    n_p = n_problems_of(s, n_problems)
    y = np.asarray(s.y)
    p = np.bincount(s.problem_index, weights=(y == 1).astype(float), minlength=n_p)
    f = np.bincount(s.problem_index, weights=(y == 0).astype(float), minlength=n_p)
    present = (p + f) > 0
    return {
        "n_samples": int(y.size),
        "n_problems": int(present.sum()),
        "mixed": int(np.sum((p > 0) & (f > 0))),
        "all_pass": int(np.sum((p > 0) & (f == 0))),
        "all_fail": int(np.sum((p == 0) & (f > 0))),
        "pass_fail_pairs": int(np.sum(p * f)),
    }


def pass_count_histogram(s: ScoredSet, n_problems: int | None = None) -> dict[int, int]:
    """Number of problems with each per-problem pass count (problems with samples only)."""
    n_p = n_problems_of(s, n_problems)
    y = np.asarray(s.y)
    p = np.bincount(s.problem_index, weights=(y == 1).astype(float), minlength=n_p)
    n = np.bincount(s.problem_index, minlength=n_p)
    vals, cnt = np.unique(p[n > 0].astype(int), return_counts=True)
    return {int(v): int(c) for v, c in zip(vals, cnt)}


def tie_rate_within(s: ScoredSet, use_tiebreak: bool = True, n_problems: int | None = None) -> float | None:
    """Share of within-problem pass-fail pairs with equal scores (section 7.12). None if no pair."""
    c = per_problem_counts(s, n_problems, use_tiebreak)
    den = float(np.sum(c["p"] * c["f"]))
    if den <= 0:
        return None
    return float(np.sum(c["T"]) / den)


def tie_rate_pooled(s: ScoredSet, use_tiebreak: bool = True) -> float | None:
    """Share of all pass-fail pairs (pooled) with equal scores."""
    keys = keys_of(s, use_tiebreak)
    if keys.size == 0:
        return None
    y = np.asarray(s.y)
    kk = int(keys.max()) + 1
    pos = np.bincount(keys, weights=(y == 1).astype(float), minlength=kk)
    neg = np.bincount(keys, weights=(y == 0).astype(float), minlength=kk)
    den = pos.sum() * neg.sum()
    return float(np.sum(pos * neg) / den) if den > 0 else None


def imputation_tie_share(s: ScoredSet, imputed: np.ndarray, within: bool = False,
                         use_tiebreak: bool = True) -> float | None:
    """Share of pass-fail pairs (pooled, or within problem if within=True) in which both samples
    carry an imputed V1 value and the two scores are tied (section 1.4, reported beside G0)."""
    imp = np.asarray(imputed, dtype=bool)
    keys = keys_of(s, use_tiebreak)
    y = np.asarray(s.y)
    if within:
        c = per_problem_counts(s, None, use_tiebreak)
        den = float(np.sum(c["p"] * c["f"]))
        if den <= 0:
            return None
        sub = per_problem_counts(_subset(s, imp), int(s.problem_index.max()) + 1, use_tiebreak)
        return float(np.sum(sub["T"]) / den)
    n_pos, n_neg = float(np.sum(y == 1)), float(np.sum(y == 0))
    if n_pos * n_neg <= 0:
        return None
    if not imp.any():
        return 0.0
    kk = int(keys.max()) + 1
    pos = np.bincount(keys[imp], weights=(y[imp] == 1).astype(float), minlength=kk)
    neg = np.bincount(keys[imp], weights=(y[imp] == 0).astype(float), minlength=kk)
    return float(np.sum(pos * neg) / (n_pos * n_neg))


def _subset(s: ScoredSet, m: np.ndarray) -> ScoredSet:
    return ScoredSet(problem_index=s.problem_index[m], y=s.y[m], rank_score=s.rank_score[m],
                     rank_tiebreak=s.rank_tiebreak[m], prob=s.prob[m])


# ---------------------------------------------------------------------------------------------------
# Brier score, Murphy decomposition, problem-demeaned Brier analog
# ---------------------------------------------------------------------------------------------------
def brier(s: ScoredSet, weights: np.ndarray | None = None) -> float:
    """BS = (1/n) sum (s - y)^2 on `prob`."""
    w = as_weights(s.y.size, weights)
    n = w.sum()
    if n <= 0:
        return float("nan")
    return float(np.sum(w * (np.asarray(s.prob) - np.asarray(s.y)) ** 2) / n)


def murphy(s: ScoredSet, n_bins: int = ECE_EQUAL_MASS_BINS, weights: np.ndarray | None = None) -> dict[str, float]:
    """Murphy decomposition with equal-mass bins (the bins of analysis.calibration).

    With bins b of (weighted) size n_b, mean probability sbar_b, mean label ybar_b, overall mean
    label ybar:
        reliability  REL = sum_b (n_b/n) (sbar_b - ybar_b)^2
        resolution   RES = sum_b (n_b/n) (ybar_b - ybar)^2
        uncertainty  UNC = ybar (1 - ybar)
        within-bin variance   WBV = (1/n) sum_b sum_{i in b} (s_i - sbar_b)^2
        within-bin covariance WBC = (1/n) sum_b sum_{i in b} (s_i - sbar_b)(y_i - ybar_b)
    Identity check (exact for binned forecasts with continuous values; Stephenson et al. 2008):
        BS = REL - RES + UNC + WBV - 2 WBC,
    asserted to 1e-12 and returned as identity_residual."""
    p = np.asarray(s.prob, dtype=np.float64)
    y = np.asarray(s.y, dtype=np.float64)
    w = as_weights(p.size, weights)
    n = w.sum()
    if n <= 0:
        raise ValueError("murphy: no samples")
    idx = equal_mass_bin_index(p, w, n_bins)
    nb = int(idx.max()) + 1
    n_b = np.bincount(idx, weights=w, minlength=nb)
    sb = np.bincount(idx, weights=w * p, minlength=nb)
    yb = np.bincount(idx, weights=w * y, minlength=nb)
    safe = np.where(n_b > 0, n_b, 1.0)
    sbar, ybar_b = sb / safe, yb / safe
    ybar = float(np.sum(w * y) / n)
    rel = float(np.sum(n_b / n * (sbar - ybar_b) ** 2))
    res = float(np.sum(n_b / n * (ybar_b - ybar) ** 2))
    unc = ybar * (1.0 - ybar)
    ds = p - sbar[idx]
    dy = y - ybar_b[idx]
    wbv = float(np.sum(w * ds * ds) / n)
    wbc = float(np.sum(w * ds * dy) / n)
    bs = float(np.sum(w * (p - y) ** 2) / n)
    resid = bs - (rel - res + unc + wbv - 2.0 * wbc)
    assert abs(resid) <= MURPHY_IDENTITY_TOL, f"Murphy identity residual {resid}"
    return {"brier": bs, "reliability": rel, "resolution": res, "uncertainty": unc,
            "within_bin_variance": wbv, "within_bin_covariance": wbc, "identity_residual": resid,
            "n_bins_used": int(np.sum(n_b > 0))}


def demeaned_brier(s: ScoredSet, weights: np.ndarray | None = None, n_problems: int | None = None) -> float | None:
    """Problem-demeaned Brier analog for d = 1 (section 8), over mixed problems only:
    (1/n_mixed) sum_i sum_{a in i} ((s_a - sbar_i) - (y_a - ybar_i))^2, where sbar_i and ybar_i are
    problem means and n_mixed counts the samples of mixed problems. None if no mixed problem."""
    n_p = n_problems_of(s, n_problems)
    pw = problem_weights(s, as_weights(s.y.size, weights), n_p)
    p = np.asarray(s.prob, dtype=np.float64)
    y = np.asarray(s.y, dtype=np.float64)
    pi = s.problem_index
    cnt = np.bincount(pi, minlength=n_p).astype(float)
    ys = np.bincount(pi, weights=y, minlength=n_p)
    ss = np.bincount(pi, weights=p, minlength=n_p)
    safe = np.where(cnt > 0, cnt, 1.0)
    mixed = (ys > 0) & (ys < cnt)
    e = (p - (ss / safe)[pi]) - (y - (ys / safe)[pi])
    sq = np.bincount(pi, weights=e * e, minlength=n_p)
    den = float(np.sum(pw[mixed] * cnt[mixed]))
    if den <= 0:
        return None
    return float(np.sum(pw[mixed] * sq[mixed]) / den)


# ---------------------------------------------------------------------------------------------------
# pass@k
# ---------------------------------------------------------------------------------------------------
def pass_at_k(n: int, c: int, k: int) -> float:
    """Unbiased estimator 1 - C(n - c, k) / C(n, k) (section 11, row 4.11), computed as
    1 - prod_{i = n - c + 1}^{n} (1 - k / i)."""
    if not (0 <= c <= n) or k < 1 or k > n:
        raise ValueError("need 0 <= c <= n and 1 <= k <= n")
    if n - c < k:
        return 1.0
    return float(1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1, dtype=np.float64)))


def pass_at_k_mean(s: ScoredSet, k: int, weights: np.ndarray | None = None, n_problems: int | None = None) -> float | None:
    """Mean over problems of the unbiased pass@k estimate."""
    n_p = n_problems_of(s, n_problems)
    pw = problem_weights(s, as_weights(s.y.size, weights), n_p)
    y = np.asarray(s.y)
    n = np.bincount(s.problem_index, minlength=n_p)
    c = np.bincount(s.problem_index, weights=(y == 1).astype(float), minlength=n_p).astype(int)
    m = (n >= k) & (pw > 0)
    if not m.any():
        return None
    vals = np.array([pass_at_k(int(n[i]), int(c[i]), k) for i in np.flatnonzero(m)])
    return float(np.sum(pw[m] * vals) / np.sum(pw[m]))


# ---------------------------------------------------------------------------------------------------
# Precomputed fast path for resamples
# ---------------------------------------------------------------------------------------------------
class RankStats:
    """Per-problem precomputation for one ScoredSet (module docstring, fast path)."""

    def __init__(self, s: ScoredSet, n_problems: int, use_tiebreak: bool = True):
        self.n_problems = int(n_problems)
        keys = keys_of(s, use_tiebreak)
        y = np.asarray(s.y)
        pi = s.problem_index
        n_p = self.n_problems
        self.p = np.bincount(pi, weights=(y == 1).astype(float), minlength=n_p)
        self.f = np.bincount(pi, weights=(y == 0).astype(float), minlength=n_p)
        self.mixed = (self.p > 0) & (self.f > 0)
        U = np.zeros((n_p, n_p))
        pos = y == 1
        pk, pp = keys[pos], pi[pos]
        neg = ~pos
        nk, nprob = keys[neg], pi[neg]
        if pk.size and nk.size:
            order = np.lexsort((nk, nprob))
            nk, nprob = nk[order], nprob[order]
            probs, starts = np.unique(nprob, return_index=True)
            ends = np.append(starts[1:], nk.size)
            for j, a, b in zip(probs, starts, ends):
                fk = nk[a:b]
                lt = np.searchsorted(fk, pk, side="left")
                le = np.searchsorted(fk, pk, side="right")
                U[:, j] = np.bincount(pp, weights=lt + 0.5 * (le - lt), minlength=n_p)
        self.U = U
        self.A = np.diag(U).copy()
        self.pairs = self.p * self.f

    def _counts(self, counts: np.ndarray | None, problem_mask: np.ndarray | None = None) -> np.ndarray:
        if counts is None:
            c = np.ones((1, self.n_problems))
        else:
            c = np.atleast_2d(np.asarray(counts, dtype=np.float64))
            if c.shape[1] != self.n_problems:
                raise ValueError("counts must have one column per problem")
        if problem_mask is not None:
            c = c * np.asarray(problem_mask, dtype=np.float64)[None, :]
        return c

    def auroc_pooled(self, counts: np.ndarray | None = None, problem_mask: np.ndarray | None = None) -> np.ndarray:
        """Pooled AUROC per resample (NaN where undefined)."""
        c = self._counts(counts, problem_mask)
        num = np.einsum("bi,bi->b", c @ self.U, c)
        den = (c @ self.p) * (c @ self.f)
        with np.errstate(invalid="ignore", divide="ignore"):
            return np.where(den > 0, num / np.where(den > 0, den, 1.0), np.nan)

    def W(self, counts: np.ndarray | None = None, problem_mask: np.ndarray | None = None) -> np.ndarray:
        """Pair-weighted within-problem AUROC per resample (NaN where no mixed problem is drawn)."""
        c = self._counts(counts, problem_mask)
        num = c @ self.A
        den = c @ self.pairs
        with np.errstate(invalid="ignore", divide="ignore"):
            return np.where(den > 0, num / np.where(den > 0, den, 1.0), np.nan)

    def W_avg(self, counts: np.ndarray | None = None, problem_mask: np.ndarray | None = None) -> np.ndarray:
        c = self._counts(counts, problem_mask)
        per = np.where(self.mixed, self.A / np.where(self.mixed, self.pairs, 1.0), 0.0)
        num = c @ per
        den = c @ self.mixed.astype(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            return np.where(den > 0, num / np.where(den > 0, den, 1.0), np.nan)

    def auroc_pooled_mixed(self, counts: np.ndarray | None = None) -> np.ndarray:
        return self.auroc_pooled(counts, problem_mask=self.mixed)

    def auroc_fold_averaged(self, fold_of_problem: np.ndarray, counts: np.ndarray | None = None) -> np.ndarray:
        """Mean over folds of per-fold pooled AUROC; NaN if any fold with data is undefined. A fold is
        counted when it holds at least one sample in the full data."""
        fold = np.asarray(fold_of_problem)
        present = (self.p + self.f) > 0
        vals = []
        for f_id in np.unique(fold[present]):
            vals.append(self.auroc_pooled(counts, problem_mask=(fold == f_id)))
        if not vals:
            return np.full(self._counts(counts).shape[0], np.nan)
        return np.mean(np.vstack(vals), axis=0)


def counts_to_weights(counts_row: np.ndarray, problem_index: np.ndarray) -> np.ndarray:
    """Per-sample weights from one resample's problem multiplicities."""
    return np.asarray(counts_row, dtype=np.float64)[problem_index]


def metric_table(s: ScoredSet, n_problems: int, fold_of_problem: np.ndarray | None = None) -> Mapping[str, object]:
    """Point values of every section 8 metric for one ScoredSet (no intervals)."""
    from . import calibration as cal
    from pipeline.contracts.constants import ECE_EQUAL_WIDTH_BINS_MARGIN, ECE_EQUAL_WIDTH_BINS_RECON

    out: dict[str, object] = {}
    out["auroc_pooled"] = auroc_pooled(s)
    out["auroc_pooled_no_tiebreak"] = auroc_pooled(s, use_tiebreak=False)
    out["W"] = within_problem_auroc(s, n_problems=n_problems)
    out["W_no_tiebreak"] = within_problem_auroc(s, use_tiebreak=False, n_problems=n_problems)
    out["W_avg"] = within_problem_auroc_avg(s, n_problems=n_problems)
    out["auprc_pass"] = auprc(s, 1)
    out["auprc_fail"] = auprc(s, 0)
    out["base_rate_pass"] = base_rate(s, 1)
    out["base_rate_fail"] = base_rate(s, 0)
    out["brier"] = brier(s)
    out["murphy"] = murphy(s)
    out["brier_demeaned"] = demeaned_brier(s, n_problems=n_problems)
    out["ece_debiased_equal_mass"] = cal.ece_debiased_equal_mass(s)
    sm, bw = cal.smooth_ece(s, return_bandwidth=True)
    out["smooth_ece"] = sm
    out["smooth_ece_bandwidth"] = bw
    out["ks_calibration_error"] = cal.ks_calibration_error(s)
    out["ece_equal_width_15"] = cal.ece_equal_width(s, ECE_EQUAL_WIDTH_BINS_RECON)
    out["ece_equal_width_10"] = cal.ece_equal_width(s, ECE_EQUAL_WIDTH_BINS_MARGIN)
    out["tie_rate_within"] = tie_rate_within(s, n_problems=n_problems)
    out["tie_rate_within_no_tiebreak"] = tie_rate_within(s, use_tiebreak=False, n_problems=n_problems)
    out["tie_rate_pooled"] = tie_rate_pooled(s)
    out["auroc_pooled_mixed"] = auroc_pooled_mixed(s, n_problems=n_problems)
    if fold_of_problem is not None:
        out["auroc_fold_averaged"] = auroc_fold_averaged(s, fold_of_problem)
    out["counts"] = mixed_counts(s, n_problems)
    return out
