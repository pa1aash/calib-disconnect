"""Generation-shift contrast (design section 1.5).

Two generation sets are scored by the probe P and the [2610.31820]-style readout S^R: frozen
(g = 0, S^R teacher-forced, reading B) and fresh (g = 1, generated with the adapter active, reading A).
Both sets cover the same problems, indexed into the same bootstrap problem list, so every contrast
is paired over problems with the same draws.

At r = 0, for d in {0, 1} (M_0 pooled AUROC, M_1 = W) and l in {0, 1}:
    Delta Gamma_g = [M_d(P) - M_d(S^R)]_{g=0} - [M_d(P) - M_d(S^R)]_{g=1}
    cross contrast (unpaired in samples) = M_d(P)_{g=0} - M_d(S^R)_{g=1}
    probe shift = M_d(P)_{g=0} - M_d(P)_{g=1}
and at d = 1 the same quantities recomputed on the problems mixed in both generation sets. Beside
them: pass rate, mixed count, and extraction-failure rate of each set.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np

from pipeline.contracts.schemas import ScoredSet

from .gap import Scores
from .metrics import RankStats


@dataclass(frozen=True)
class GenSet:
    """One generation set for one model: samples aligned across readouts."""

    problem_index: np.ndarray
    labels: Mapping[str, np.ndarray]        # suite -> y
    probe: Mapping[str, Scores]             # fit suite -> P^(l) read on this set
    sr: Mapping[str, Scores]                # fit suite -> S^R read on this set
    extraction_failed: np.ndarray | None = None


def _rs(gs: GenSet, sc: Scores, suite: str, n_problems: int) -> RankStats:
    s = ScoredSet(problem_index=gs.problem_index, y=np.asarray(gs.labels[suite], dtype=np.int8),
                  rank_score=np.asarray(sc.rank_score, float), rank_tiebreak=np.asarray(sc.rank_tiebreak, float),
                  prob=np.asarray(sc.prob, float))
    return RankStats(s, n_problems)


def _m(rs: RankStats, d: int, counts, mask=None):
    return rs.W(counts, mask) if d else rs.auroc_pooled(counts, mask)


def contrasts(frozen: GenSet, fresh: GenSet, n_problems: int, suites: tuple[str, ...] = ("O", "E"),
              counts: np.ndarray | None = None) -> dict:
    """All section 1.5 contrasts for each suite in `suites` (the suites that have a fresh set);
    keys "d<d>_<suite>_<all|mixed_both>". Values are arrays of length 1 (counts=None) or B."""
    out = {}
    for suite in suites:
        rp0, rs0 = _rs(frozen, frozen.probe[suite], suite, n_problems), _rs(frozen, frozen.sr[suite], suite, n_problems)
        rp1, rs1 = _rs(fresh, fresh.probe[suite], suite, n_problems), _rs(fresh, fresh.sr[suite], suite, n_problems)
        both = rp0.mixed & rp1.mixed
        for d in (0, 1):
            masks = {"all": None} if d == 0 else {"all": None, "mixed_both": both}
            for mname, mask in masks.items():
                p0, s0 = _m(rp0, d, counts, mask), _m(rs0, d, counts, mask)
                p1, s1 = _m(rp1, d, counts, mask), _m(rs1, d, counts, mask)
                out[f"d{d}_{suite}_{mname}"] = {
                    "delta_gamma_g": (p0 - s0) - (p1 - s1),
                    "cross_contrast": p0 - s1,
                    "probe_shift": p0 - p1,
                    "gamma_g0": p0 - s0, "gamma_g1": p1 - s1,
                    "probe_g0": p0, "sr_g0": s0, "probe_g1": p1, "sr_g1": s1,
                }
    return out


def set_rates(gs: GenSet, n_problems: int, suites: tuple[str, ...] = ("O", "E"),
              counts: np.ndarray | None = None) -> dict:
    """Pass rate and mixed count per suite, and the extraction-failure rate, of one set."""
    c = np.ones((1, n_problems)) if counts is None else np.atleast_2d(np.asarray(counts, float))
    n_i = np.bincount(gs.problem_index, minlength=n_problems).astype(float)
    out = {}
    for suite in suites:
        y = np.asarray(gs.labels[suite])
        pas = np.bincount(gs.problem_index, weights=(y == 1).astype(float), minlength=n_problems)
        mixed = ((pas > 0) & (pas < n_i)).astype(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            out[f"pass_rate_{suite}"] = (c @ pas) / (c @ n_i)
        out[f"mixed_count_{suite}"] = c @ mixed
    if gs.extraction_failed is not None:
        ef = np.bincount(gs.problem_index, weights=np.asarray(gs.extraction_failed, float), minlength=n_problems)
        with np.errstate(invalid="ignore", divide="ignore"):
            out["extraction_failure_rate"] = (c @ ef) / (c @ n_i)
    return out
