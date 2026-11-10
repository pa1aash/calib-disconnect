"""Offline routing replay (design section 10).

Both decision problems use the lexicographic keys of analysis.ranking (the discrimination tie rule),
on out-of-fold scores.

1. Best-of-k selection per problem (within-problem use). For each problem the sample with the
   highest key is selected; if several samples share the highest key, the value is their mean pass
   indicator (the expected value of a uniform choice among them). Values are means over problems:
   selected pass rate; random = mean over problems of the problem's pass rate; oracle = share of
   problems with at least one passing sample (pass@k with k = all samples); regret = oracle - selected.
2. Global verification triage (pooled use). With n samples and budget fraction b, the b n samples
   with the lowest keys are sent to execution; a tie group straddling the cutoff is included in
   proportion to the budget left (expected value of a uniform choice inside the group). Value =
   share of all failing samples caught; random = b; oracle = min(1, b n / n_fail);
   regret = oracle - achieved. Undefined with no failing sample.
Weights (bootstrap multiplicities) act as duplication counts in both.

Decision cost of a term (section 10): the Shapley value in the game whose payoff at cell x is the
regret of routing by S^(r,t,l) minus the regret of routing by P^(l) (positive when the probe routes
better, the orientation of Gamma). d selects the decision problem: d = 0 global triage, d = 1
best-of-k. Triage has one budget per fraction, so there is one game per fraction in TRIAGE_FRACTIONS;
the d = 1 cells (best-of-k) are shared by the five games.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np

from pipeline.contracts.constants import TRIAGE_FRACTIONS
from pipeline.contracts.schemas import ScoredSet

from ._common import as_weights, n_problems_of
from .metrics import problem_weights
from .ranking import keys_of


# ---------------------------------------------------------------------------------------------------
# Best-of-k
# ---------------------------------------------------------------------------------------------------
def best_of_k_per_problem(s: ScoredSet, n_problems: int | None = None, use_tiebreak: bool = True) -> dict[str, np.ndarray]:
    """Per-problem selected, random, and oracle values and a presence mask (unweighted)."""
    n_p = n_problems_of(s, n_problems)
    keys = keys_of(s, use_tiebreak)
    y = np.asarray(s.y, dtype=np.float64)
    pi = s.problem_index
    present = np.bincount(pi, minlength=n_p) > 0
    top = np.full(n_p, -1, dtype=np.int64)
    np.maximum.at(top, pi, keys)
    at_top = keys == top[pi]
    n_top = np.bincount(pi, weights=at_top.astype(float), minlength=n_p)
    pass_top = np.bincount(pi, weights=at_top * y, minlength=n_p)
    n_all = np.bincount(pi, minlength=n_p).astype(float)
    pas = np.bincount(pi, weights=y, minlength=n_p)
    safe_t = np.where(n_top > 0, n_top, 1.0)
    safe_a = np.where(n_all > 0, n_all, 1.0)
    return {"selected": pass_top / safe_t, "random": pas / safe_a, "oracle": (pas > 0).astype(float),
            "present": present}


def best_of_k(s: ScoredSet, weights: np.ndarray | None = None, n_problems: int | None = None,
              use_tiebreak: bool = True) -> dict[str, float] | None:
    n_p = n_problems_of(s, n_problems)
    pp = best_of_k_per_problem(s, n_p, use_tiebreak)
    pw = problem_weights(s, as_weights(s.y.size, weights), n_p) * pp["present"]
    tot = pw.sum()
    if tot <= 0:
        return None
    sel = float(pw @ pp["selected"] / tot)
    rnd = float(pw @ pp["random"] / tot)
    orc = float(pw @ pp["oracle"] / tot)
    return {"selected": sel, "random": rnd, "oracle": orc, "regret": orc - sel, "regret_random": orc - rnd}


def best_of_k_batch(s: ScoredSet, counts: np.ndarray | None, n_problems: int) -> dict[str, np.ndarray]:
    """Vectorized over resamples: per-problem values are fixed, so each resample is a weighted mean."""
    pp = best_of_k_per_problem(s, n_problems)
    c = np.ones((1, n_problems)) if counts is None else np.atleast_2d(np.asarray(counts, float))
    c = c * pp["present"][None, :]
    tot = c.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        sel = np.where(tot > 0, (c @ pp["selected"]) / tot, np.nan)
        rnd = np.where(tot > 0, (c @ pp["random"]) / tot, np.nan)
        orc = np.where(tot > 0, (c @ pp["oracle"]) / tot, np.nan)
    return {"selected": sel, "random": rnd, "oracle": orc, "regret": orc - sel, "regret_random": orc - rnd}


# ---------------------------------------------------------------------------------------------------
# Global triage
# ---------------------------------------------------------------------------------------------------
def _triage_from_groups(gw: np.ndarray, gf: np.ndarray, fractions: Sequence[float]) -> dict[str, np.ndarray]:
    """gw, gf: (B, G) weight and failing weight per key group in ascending key order."""
    cw = np.cumsum(gw, axis=1)
    cf = np.cumsum(gf, axis=1)
    n = cw[:, -1]
    nf = cf[:, -1]
    out = {}
    for b in fractions:
        budget = b * n
        # first group whose cumulative weight reaches the budget
        j = np.sum(cw < budget[:, None], axis=1)
        j = np.minimum(j, gw.shape[1] - 1)
        rows = np.arange(cw.shape[0])
        before_w = np.where(j > 0, cw[rows, np.maximum(j - 1, 0)], 0.0)
        before_f = np.where(j > 0, cf[rows, np.maximum(j - 1, 0)], 0.0)
        gwj, gfj = gw[rows, j], gf[rows, j]
        with np.errstate(invalid="ignore", divide="ignore"):
            frac = np.where(gwj > 0, np.clip((budget - before_w) / np.where(gwj > 0, gwj, 1.0), 0.0, 1.0), 0.0)
            caught = before_f + frac * gfj
            achieved = np.where(nf > 0, caught / np.where(nf > 0, nf, 1.0), np.nan)
            oracle = np.where(nf > 0, np.minimum(1.0, budget / np.where(nf > 0, nf, 1.0)), np.nan)
        out[f"{b:g}"] = {"achieved": achieved, "random": np.where(nf > 0, b, np.nan), "oracle": oracle,
                         "regret": oracle - achieved, "regret_random": oracle - b}
    return out


def triage(s: ScoredSet, fractions: Sequence[float] = TRIAGE_FRACTIONS, weights: np.ndarray | None = None,
           use_tiebreak: bool = True) -> dict:
    keys = keys_of(s, use_tiebreak)
    w = as_weights(s.y.size, weights)
    kk = int(keys.max()) + 1 if keys.size else 1
    gw = np.bincount(keys, weights=w, minlength=kk)[None, :]
    gf = np.bincount(keys, weights=w * (np.asarray(s.y) == 0), minlength=kk)[None, :]
    res = _triage_from_groups(gw, gf, fractions)
    return {b: {k: float(v[0]) for k, v in d.items()} for b, d in res.items()}


def triage_batch(s: ScoredSet, counts: np.ndarray | None, n_problems: int,
                 fractions: Sequence[float] = TRIAGE_FRACTIONS) -> dict:
    """Vectorized over resamples: the group of each sample is fixed, so the per-resample group
    weights are counts @ (problem x group) matrices."""
    keys = keys_of(s)
    kk = int(keys.max()) + 1 if keys.size else 1
    y0 = (np.asarray(s.y) == 0).astype(float)
    Hw = np.zeros((n_problems, kk))
    Hf = np.zeros((n_problems, kk))
    np.add.at(Hw, (s.problem_index, keys), 1.0)
    np.add.at(Hf, (s.problem_index, keys), y0)
    c = np.ones((1, n_problems)) if counts is None else np.atleast_2d(np.asarray(counts, float))
    out: dict = {}
    for start in range(0, c.shape[0], 512):
        cc = c[start:start + 512]
        part = _triage_from_groups(cc @ Hw, cc @ Hf, fractions)
        for b, d in part.items():
            slot = out.setdefault(b, {k: [] for k in d})
            for k, v in d.items():
                slot[k].append(v)
    return {b: {k: np.concatenate(v) for k, v in d.items()} for b, d in out.items()}


# ---------------------------------------------------------------------------------------------------
# Decision-cost games
# ---------------------------------------------------------------------------------------------------
def routing_cells(inp, counts: np.ndarray | None = None, fractions: Sequence[float] = TRIAGE_FRACTIONS) -> dict:
    """Per triage fraction, the 16 payoff cells regret(S) - regret(P) (d = 0 triage at that
    fraction, d = 1 best-of-k). `inp` is an analysis.gap.GapInputs. Also returns the anchors."""
    from .gap import _set, cell_roles
    from .shapley import all_keys

    cache: dict = {}

    def reg(role, fit, suite, d):
        key = (role, fit, suite, d)
        if key not in cache:
            s = _set(inp, role, fit, suite)
            if d:
                cache[key] = best_of_k_batch(s, counts, inp.n_problems)
            else:
                cache[key] = triage_batch(s, counts, inp.n_problems, fractions)
        return cache[key]

    games = {f"{b:g}": {"cells": {}, "probe_regret": {}, "stated_regret": {}} for b in fractions}
    anchors: dict = {}
    for key in all_keys():
        (pr, pf), (sr, sf), suite, d = cell_roles(inp, key)
        rp, rs = reg(pr, pf, suite, d), reg(sr, sf, suite, d)
        for b in fractions:
            bk = f"{b:g}"
            gp = rp["regret"] if d else rp[bk]["regret"]
            gs = rs["regret"] if d else rs[bk]["regret"]
            if counts is None:
                gp, gs = float(gp[0]), float(gs[0])
            games[bk]["cells"][key] = gs - gp
            games[bk]["probe_regret"][key] = gp
            games[bk]["stated_regret"][key] = gs
    if counts is None:
        for suite in inp.suites:
            bk_ = reg("P", suite, suite, 1)
            tr = reg("P", suite, suite, 0)
            anchors[suite] = {"best_of_k": {k: float(v[0]) for k, v in bk_.items()},
                              "triage": {b: {k: float(v[0]) for k, v in d.items()} for b, d in tr.items()}}
    return {"games": games, "anchors": anchors}
