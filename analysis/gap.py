"""The 16 cells of the gap function for one model, and their diagnostics (design sections 1.2 to 1.4, 8, 9).

Gamma(r, t, d, l) = M_d(P^(l), y^(l)) - M_d(S^(r, t, l), y^(l)), on the population of problems valid
under both suites, with M_0 = pooled AUROC and M_1 = W (pair-weighted within-problem AUROC).
- l selects the label suite for fitting and scoring: suites[0] (l = 0, original "O"; LiveCodeBench
  analog "lcb_public") or suites[1] (l = 1, EvalPlus "E"; analog "lcb_label").
- S^(r, t, l): t = 0 is the zero-shot stated readout of the model's chain (V1 primary, or V2 for the
  sensitivity chain and for models switched by K3); t = 1 is S^T fit on suite l; r = 1 is the
  isotonic version fit on suite l (iso:<name>, ranked lexicographically by (isotonic value,
  pre-map score)). The raw zero-shot readout is not fit, so it is the same at l = 0 and l = 1; only
  its labels change.
- Cells are keyed "rtdl", for example "0000" = G0 and "1111" = R^(0) (fold seed 0).

Secondary budgets (section 8, red team V13e): for Brier and the three calibration estimators the
gap is the stated readout's value minus the probe's value, Gamma = M_d(S) - M_d(P), so positive
means the stated readout is worse. M_0 is the estimator itself; M_1 is the problem-demeaned Brier
analog, the only within-problem calibration measure section 8 defines, so all four secondary
budgets share their d = 1 cells.

Per-seed residual for the decision (section 9): R_{m,s} = W(P^(E,s)) - W(S^(E,s)), where seed 0
uses iso:ST and seeds 1 and 2 use ST directly. W is invariant to the isotonic map under the
lexicographic tie rule, so at seed 0 W(iso:ST) = W(ST) exactly; this is asserted.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Mapping

import numpy as np

from pipeline.contracts.schemas import ScoredSet

from . import calibration as cal
from . import metrics as M
from .bootstrap import replicate
from .shapley import all_keys

SECONDARY_ESTIMATORS = ("brier", "ece_debiased_equal_mass", "smooth_ece", "ks_calibration_error")


@dataclass(frozen=True)
class Scores:
    """One readout's scores aligned to the population's sample order."""

    rank_score: np.ndarray
    rank_tiebreak: np.ndarray
    prob: np.ndarray
    imputed: np.ndarray | None = None


@dataclass(frozen=True)
class GapInputs:
    problem_index: np.ndarray                 # int64[n], row of the bootstrap problem list
    n_problems: int
    labels: Mapping[str, np.ndarray]          # suite -> int8[n]
    probe: Mapping[str, Scores]               # fit suite -> P^(l)
    zero_shot: Scores                         # S^Z of the chain (raw)
    zero_shot_iso: Mapping[str, Scores]       # fit suite -> iso:S^Z
    trained: Mapping[str, Scores]             # fit suite -> S^T
    trained_iso: Mapping[str, Scores]         # fit suite -> iso:S^T
    suites: tuple[str, str] = ("O", "E")
    fold_of_problem: np.ndarray | None = None  # fold seed 0 fold of each problem (d diagnostics)
    _cache: dict = field(default_factory=dict, compare=False, repr=False)


def scored(inp: GapInputs, sc: Scores, suite: str) -> ScoredSet:
    return ScoredSet(problem_index=inp.problem_index, y=np.asarray(inp.labels[suite], dtype=np.int8),
                     rank_score=np.asarray(sc.rank_score, dtype=np.float64),
                     rank_tiebreak=np.asarray(sc.rank_tiebreak, dtype=np.float64),
                     prob=np.asarray(sc.prob, dtype=np.float64))


def stated_name(r: int, t: int, l: int, suites: tuple[str, str]) -> tuple[str, str | None]:
    """(readout role, fit suite) of S^(r, t, l)."""
    suite = suites[l]
    if t == 0:
        return ("iso:SZ", suite) if r else ("SZ", None)
    return ("iso:ST", suite) if r else ("ST", suite)


def _scores_for(inp: GapInputs, role: str, fit: str | None) -> Scores:
    if role == "P":
        return inp.probe[fit]
    if role == "SZ":
        return inp.zero_shot
    if role == "iso:SZ":
        return inp.zero_shot_iso[fit]
    if role == "ST":
        return inp.trained[fit]
    if role == "iso:ST":
        return inp.trained_iso[fit]
    raise KeyError(role)


def _set(inp: GapInputs, role: str, fit: str | None, label_suite: str) -> ScoredSet:
    return scored(inp, _scores_for(inp, role, fit), label_suite)


def rank_stats(inp: GapInputs, role: str, fit: str | None, label_suite: str, use_tiebreak: bool = True) -> M.RankStats:
    key = ("rank", role, fit, label_suite, use_tiebreak)
    if key not in inp._cache:
        inp._cache[key] = M.RankStats(_set(inp, role, fit, label_suite), inp.n_problems, use_tiebreak)
    return inp._cache[key]


def _disc(inp, role, fit, suite, d, counts, mask=None):
    rs = rank_stats(inp, role, fit, suite)
    return rs.W(counts, mask) if d else rs.auroc_pooled(counts, mask)


def _first(a: np.ndarray) -> float:
    return float(a[0])


def cell_roles(inp: GapInputs, key: str):
    r, t, d, l = (int(ch) for ch in key)
    suite = inp.suites[l]
    return ("P", suite), stated_name(r, t, l, inp.suites), suite, d


# ---------------------------------------------------------------------------------------------------
# Discrimination cells
# ---------------------------------------------------------------------------------------------------
def discrimination_cells(inp: GapInputs, counts: np.ndarray | None = None) -> dict:
    """Point cells (counts=None) or per-resample cells (counts = BootstrapDraws.counts). Returns
    {"cells": {key: value or array}, "probe": {...}, "stated": {...}} with the two components."""
    cells, probe, stated = {}, {}, {}
    for key in all_keys():
        (pr, pf), (sr, sf), suite, d = cell_roles(inp, key)
        mp = _disc(inp, pr, pf, suite, d, counts)
        ms = _disc(inp, sr, sf, suite, d, counts)
        if counts is None:
            mp, ms = _first(mp), _first(ms)
        probe[key], stated[key] = mp, ms
        cells[key] = mp - ms
    return {"cells": cells, "probe": probe, "stated": stated}


# ---------------------------------------------------------------------------------------------------
# Secondary (Brier and calibration) cells
# ---------------------------------------------------------------------------------------------------
class _LinearStats:
    """Brier and problem-demeaned Brier as weighted sums over problems."""

    def __init__(self, s: ScoredSet, n_problems: int):
        p = np.asarray(s.prob, dtype=np.float64)
        y = np.asarray(s.y, dtype=np.float64)
        pi = s.problem_index
        self.n = np.bincount(pi, minlength=n_problems).astype(float)
        self.sq = np.bincount(pi, weights=(p - y) ** 2, minlength=n_problems)
        ys = np.bincount(pi, weights=y, minlength=n_problems)
        ss = np.bincount(pi, weights=p, minlength=n_problems)
        safe = np.where(self.n > 0, self.n, 1.0)
        e = (p - (ss / safe)[pi]) - (y - (ys / safe)[pi])
        mixed = (ys > 0) & (ys < self.n)
        self.dsq = np.where(mixed, np.bincount(pi, weights=e * e, minlength=n_problems), 0.0)
        self.dn = np.where(mixed, self.n, 0.0)

    @staticmethod
    def _ratio(num, den):
        with np.errstate(invalid="ignore", divide="ignore"):
            return np.where(den > 0, num / np.where(den > 0, den, 1.0), np.nan)

    def brier(self, c):
        return self._ratio(c @ self.sq, c @ self.n)

    def demeaned(self, c):
        return self._ratio(c @ self.dsq, c @ self.dn)


def _lin(inp, role, fit, suite) -> _LinearStats:
    key = ("lin", role, fit, suite)
    if key not in inp._cache:
        inp._cache[key] = _LinearStats(_set(inp, role, fit, suite), inp.n_problems)
    return inp._cache[key]


_LOOP_FNS: dict[str, Callable] = {
    "ece_debiased_equal_mass": lambda s, w: cal.ece_debiased_equal_mass(s, weights=w),
    "smooth_ece": lambda s, w: cal.smooth_ece(s, weights=w),
    "ks_calibration_error": lambda s, w: cal.ks_calibration_error(s, weights=w),
}


def _secondary_metric(inp, estimator, role, fit, suite, d, counts):
    c = np.ones((1, inp.n_problems)) if counts is None else np.atleast_2d(np.asarray(counts, dtype=np.float64))
    lin = _lin(inp, role, fit, suite)
    if d == 1:
        return lin.demeaned(c)
    if estimator == "brier":
        return lin.brier(c)
    key = ("loop", estimator, role, fit, suite, None if counts is None else id(counts))
    if key not in inp._cache:
        s = _set(inp, role, fit, suite)
        fn = _LOOP_FNS[estimator]
        if counts is None:
            inp._cache[key] = np.array([fn(s, None)], dtype=np.float64)
        elif estimator == "smooth_ece":
            inp._cache[key] = cal.smooth_ece_batch(s.prob, s.y, inp.problem_index, c, inp.n_problems)
        else:
            inp._cache[key] = replicate(lambda w: fn(s, w), c, inp.problem_index)
    return inp._cache[key]


def secondary_cells(inp: GapInputs, estimator: str, counts: np.ndarray | None = None) -> dict:
    """Cells of the Brier or calibration budget, Gamma = M_d(S) - M_d(P) (sign convention V13e)."""
    if estimator not in SECONDARY_ESTIMATORS:
        raise KeyError(estimator)
    cells, probe, stated = {}, {}, {}
    for key in all_keys():
        (pr, pf), (sr, sf), suite, d = cell_roles(inp, key)
        mp = _secondary_metric(inp, estimator, pr, pf, suite, d, counts)
        ms = _secondary_metric(inp, estimator, sr, sf, suite, d, counts)
        if counts is None:
            mp, ms = _first(mp), _first(ms)
        probe[key], stated[key] = mp, ms
        cells[key] = ms - mp
    return {"cells": cells, "probe": probe, "stated": stated, "sign": "stated minus probe"}


# ---------------------------------------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------------------------------------
def mixed_masks(inp: GapInputs) -> dict[str, np.ndarray]:
    out = {}
    for suite in inp.suites:
        y = np.asarray(inp.labels[suite])
        p = np.bincount(inp.problem_index, weights=(y == 1).astype(float), minlength=inp.n_problems)
        f = np.bincount(inp.problem_index, weights=(y == 0).astype(float), minlength=inp.n_problems)
        out[suite] = (p > 0) & (f > 0)
    return out


def d_diagnostics(inp: GapInputs, counts: np.ndarray | None = None) -> dict:
    """Beside phi_d (section 1.3, 8): for each (r, t, l) at d = 0, the gap in pooled AUROC, in pooled
    AUROC restricted to mixed problems, and in fold-averaged pooled AUROC, beside the d = 1 gap."""
    out = {}
    for key in all_keys():
        r, t, d, l = (int(ch) for ch in key)
        if d:
            continue
        (pr, pf), (sr, sf), suite, _ = cell_roles(inp, key)
        rp, rs_ = rank_stats(inp, pr, pf, suite), rank_stats(inp, sr, sf, suite)
        row = {
            "pooled": rp.auroc_pooled(counts) - rs_.auroc_pooled(counts),
            "pooled_mixed_only": rp.auroc_pooled_mixed(counts) - rs_.auroc_pooled_mixed(counts),
            "within": rp.W(counts) - rs_.W(counts),
        }
        if inp.fold_of_problem is not None:
            row["pooled_fold_averaged"] = (rp.auroc_fold_averaged(inp.fold_of_problem, counts)
                                           - rs_.auroc_fold_averaged(inp.fold_of_problem, counts))
        if counts is None:
            row = {k: _first(v) for k, v in row.items()}
        out[f"{r}{t}x{l}"] = row
    return out


def l_diagnostics(inp: GapInputs, counts: np.ndarray | None = None) -> dict:
    """Beside phi_l (section 1.3, 8), at (r, t, d) = (1, 1, 1): the change from refitting on suite
    l = 1 while scoring on suite l = 0 labels, then the change from scoring on suite l = 1 labels;
    and W on the problems mixed under both suites, with counts entering and leaving the mixed set."""
    s0, s1 = inp.suites
    g10 = _disc(inp, "P", s0, s0, 1, counts) - _disc(inp, "iso:ST", s0, s0, 1, counts)
    gmid = _disc(inp, "P", s1, s0, 1, counts) - _disc(inp, "iso:ST", s1, s0, 1, counts)
    g11 = _disc(inp, "P", s1, s1, 1, counts) - _disc(inp, "iso:ST", s1, s1, 1, counts)
    mm = mixed_masks(inp)
    both = mm[s0] & mm[s1]
    g10b = _disc(inp, "P", s0, s0, 1, counts, both) - _disc(inp, "iso:ST", s0, s0, 1, counts, both)
    g11b = _disc(inp, "P", s1, s1, 1, counts, both) - _disc(inp, "iso:ST", s1, s1, 1, counts, both)
    row = {"gamma_1110": g10, "gamma_refit_on_l1_scored_on_l0": gmid, "gamma_1111": g11,
           "refit_step": gmid - g10, "relabel_step": g11 - gmid,
           "gamma_1110_mixed_both": g10b, "gamma_1111_mixed_both": g11b,
           "phi_l_full_config_mixed_both": g11b - g10b}
    if counts is None:
        row = {k: _first(v) for k, v in row.items()}
        row["counts"] = {"mixed_l0": int(mm[s0].sum()), "mixed_l1": int(mm[s1].sum()),
                         "mixed_both": int(both.sum()), "entering": int((mm[s1] & ~mm[s0]).sum()),
                         "leaving": int((mm[s0] & ~mm[s1]).sum())}
    return row


def rt_diagnostics(inp: GapInputs, counts: np.ndarray | None = None) -> dict:
    """Pooled AUROC of S^T with and without the isotonic map, per suite (section 1.3)."""
    out = {}
    for suite in inp.suites:
        a = _disc(inp, "ST", suite, suite, 0, counts)
        b = _disc(inp, "iso:ST", suite, suite, 0, counts)
        row = {"auroc_ST": a, "auroc_iso_ST": b, "iso_minus_raw": b - a}
        if counts is None:
            row = {k: _first(v) for k, v in row.items()}
        out[suite] = row
    return out


def tie_rates(inp: GapInputs) -> dict:
    """Within-problem tie rates with and without the lexicographic rule (sections 1.2, 7.12) for the
    readouts of the game, under the suite they are scored on."""
    out = {}
    for suite in inp.suites:
        for role in ("P", "SZ", "iso:SZ", "ST", "iso:ST"):
            fit = None if role == "SZ" else suite
            s = _set(inp, role, fit, suite)
            out[f"{role}|{suite}"] = {"with_rule": M.tie_rate_within(s, True, inp.n_problems),
                                      "without_rule": M.tie_rate_within(s, False, inp.n_problems)}
    return out


def imputation_tie_share(inp: GapInputs) -> dict | None:
    """Share of pass-fail pairs tied by V1 imputation, beside G0 (pooled, labels of l = 0), and the
    within-problem share."""
    if inp.zero_shot.imputed is None:
        return None
    s = _set(inp, "SZ", None, inp.suites[0])
    return {"pooled": M.imputation_tie_share(s, inp.zero_shot.imputed, within=False),
            "within": M.imputation_tie_share(s, inp.zero_shot.imputed, within=True),
            "share_imputed_samples": float(np.mean(np.asarray(inp.zero_shot.imputed, dtype=bool)))}


# ---------------------------------------------------------------------------------------------------
# Per-seed residual
# ---------------------------------------------------------------------------------------------------
def per_seed_residual(problem_index: np.ndarray, n_problems: int, labels_l1: np.ndarray, probe: Scores,
                      trained: Scores, trained_iso: Scores | None = None,
                      counts: np.ndarray | None = None) -> tuple[float, np.ndarray | None]:
    """R_{m,s} = W(P) - W(S) under suite l = 1 (section 9). Pass trained_iso at seed 0: the function
    asserts W(iso:ST) = W(ST) and uses iso:ST as the design states."""
    y = np.asarray(labels_l1, dtype=np.int8)

    def ss(sc: Scores) -> ScoredSet:
        return ScoredSet(problem_index=problem_index, y=y, rank_score=np.asarray(sc.rank_score, float),
                         rank_tiebreak=np.asarray(sc.rank_tiebreak, float), prob=np.asarray(sc.prob, float))

    rp = M.RankStats(ss(probe), n_problems)
    rs = M.RankStats(ss(trained), n_problems)
    if trained_iso is not None:
        ri = M.RankStats(ss(trained_iso), n_problems)
        a, b = _first(ri.W()), _first(rs.W())
        assert (np.isnan(a) and np.isnan(b)) or a == b, f"W(iso:ST) = {a} differs from W(ST) = {b}"
        rs = ri
    point = _first(rp.W()) - _first(rs.W())
    reps = None if counts is None else rp.W(counts) - rs.W(counts)
    return point, reps
