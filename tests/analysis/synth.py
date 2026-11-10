"""Synthetic data for analysis tests (no study data)."""

from __future__ import annotations

import numpy as np
from scipy.special import expit

from analysis.gap import GapInputs, Scores


def iso_like(score: np.ndarray, fold: np.ndarray, n_steps: int = 4) -> np.ndarray:
    """A per-fold monotone non-decreasing step map of score (a stand-in for an isotonic map)."""
    out = np.empty_like(score)
    for f in np.unique(fold):
        m = fold == f
        qs = np.quantile(score[m], np.linspace(0, 1, n_steps + 1)[1:-1])
        out[m] = (np.searchsorted(qs, score[m], side="right") + 0.5 + 0.1 * f) / (n_steps + 1)
    return np.clip(out, 0.0, 1.0)


def make_inputs(seed: int = 0, n_problems: int = 40, k: int = 6, separation: float = 1.5,
                suites=("O", "E")) -> GapInputs:
    rng = np.random.default_rng(seed)
    pi = np.repeat(np.arange(n_problems), k)
    n = pi.size
    diff = rng.normal(0, 1.5, n_problems)[pi]
    latent = diff + rng.normal(0, 1, n)
    yE = (latent > 0.3).astype(np.int8)
    yO = np.maximum(yE, (latent > -0.1).astype(np.int8))      # weaker suite passes more
    labels = {suites[0]: yO, suites[1]: yE}
    fold_of_problem = rng.integers(0, 5, n_problems)
    fold = fold_of_problem[pi]

    def sc(x, tb=None, prob=None, imputed=None):
        return Scores(rank_score=x, rank_tiebreak=np.full(n, np.nan) if tb is None else tb,
                      prob=expit(x) if prob is None else prob, imputed=imputed)

    probe = {s: sc(separation * latent + rng.normal(0, 1, n)) for s in suites}
    v1 = np.round(np.clip(expit(0.5 * latent + rng.normal(0, 1.5, n)), 0, 1), 1)
    imputed = rng.uniform(size=n) < 0.1
    v1 = np.where(imputed, 0.8, v1)
    zs = Scores(rank_score=v1, rank_tiebreak=np.full(n, np.nan), prob=v1, imputed=imputed)
    st = {s: sc(0.8 * separation * latent + rng.normal(0, 1, n)) for s in suites}

    def iso_of(raw: Scores) -> Scores:
        v = iso_like(raw.rank_score, fold)
        return Scores(rank_score=v, rank_tiebreak=raw.rank_score.copy(), prob=v)

    zs_iso = {s: iso_of(zs) for s in suites}
    st_iso = {s: iso_of(st[s]) for s in suites}
    return GapInputs(problem_index=pi, n_problems=n_problems, labels=labels, probe=probe, zero_shot=zs,
                     zero_shot_iso=zs_iso, trained=st, trained_iso=st_iso, suites=tuple(suites),
                     fold_of_problem=fold_of_problem)


def v2_chain(inp: GapInputs, seed: int = 1) -> GapInputs:
    rng = np.random.default_rng(seed)
    n = inp.problem_index.size
    lo = inp.probe[inp.suites[1]].rank_score * 0.3 + rng.normal(0, 1, n)
    zs = Scores(rank_score=lo, rank_tiebreak=np.full(n, np.nan), prob=expit(lo))
    fold = inp.fold_of_problem[inp.problem_index]
    zs_iso = {}
    for s in inp.suites:
        v = iso_like(lo, fold)
        zs_iso[s] = Scores(rank_score=v, rank_tiebreak=lo.copy(), prob=v)
    return GapInputs(problem_index=inp.problem_index, n_problems=inp.n_problems, labels=inp.labels,
                     probe=inp.probe, zero_shot=zs, zero_shot_iso=zs_iso, trained=inp.trained,
                     trained_iso=inp.trained_iso, suites=inp.suites, fold_of_problem=inp.fold_of_problem)
