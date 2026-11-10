"""Reconciliation checks as paired bootstrap contrasts (design sections 2.1 to 2.4; orchestrator mapping
of 2026-11-10).

A check compares statistic A with statistic B (another readout's statistic on the same samples, or a
fixed reference value) and classifies the paired 95 percent percentile interval of A - B with
analysis.reconciliation.classify. The same problem draws are used for both terms, so every interval
is paired. The diagnostic recomputes the check with extraction-failure and truncated samples removed
(section 2.1, K12); the outcome uses the full set.

Statistics: "auroc" (pooled AUROC), "W" (pair-weighted within-problem AUROC), "rank1" (pass@rank-1,
the best-of-k selected pass rate of analysis.routing), "random" (mean over problems of the problem's
pass rate). `problem_mask` restricts a check to a subset of the population's problems (HumanEval for
[Ribeiro]).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from pipeline.contracts.constants import RECONCILIATION_LEVEL
from pipeline.contracts.schemas import ScoredSet

from ._common import subset
from .bootstrap import interval_dict, percentile_interval
from .metrics import RankStats
from .reconciliation import make_check
from .routing import best_of_k_batch


@dataclass(frozen=True)
class Term:
    s: ScoredSet
    stat: str
    excluded: np.ndarray | None = None      # bool per sample: extraction failure or truncation


def stat_values(s: ScoredSet, stat: str, counts: np.ndarray | None, n_problems: int,
                problem_mask: np.ndarray | None = None) -> np.ndarray:
    """Values for counts=None (length 1) or per resample."""
    c = np.ones((1, n_problems)) if counts is None else np.atleast_2d(np.asarray(counts, dtype=np.float64))
    if problem_mask is not None:
        c = c * np.asarray(problem_mask, dtype=np.float64)[None, :]
    if stat in ("auroc", "W"):
        rs = RankStats(s, n_problems)
        return rs.auroc_pooled(c) if stat == "auroc" else rs.W(c)
    if stat in ("rank1", "random"):
        r = best_of_k_batch(s, c, n_problems)
        return r["selected"] if stat == "rank1" else r["random"]
    raise KeyError(stat)


def _drop(t: Term) -> Term:
    if t.excluded is None:
        return t
    return Term(subset(t.s, ~np.asarray(t.excluded, dtype=bool)), t.stat, None)


def contrast(a: Term, b: Term | float, counts: np.ndarray, n_problems: int,
             problem_mask: np.ndarray | None = None, level: float = RECONCILIATION_LEVEL) -> dict:
    pa = stat_values(a.s, a.stat, None, n_problems, problem_mask)[0]
    ra = stat_values(a.s, a.stat, counts, n_problems, problem_mask)
    if isinstance(b, Term):
        pb = stat_values(b.s, b.stat, None, n_problems, problem_mask)[0]
        rb = stat_values(b.s, b.stat, counts, n_problems, problem_mask)
    else:
        pb, rb = float(b), float(b)
    iv = percentile_interval(pa - pb, ra - rb, level)
    return {"a": float(pa), "b": float(pb), "value": float(pa - pb), "interval": iv}


def run_check(check_id: str, paper: str, reading: str | None, model_key: str, kind: str, direction: int,
              tie_width: float | None, a: Term, b: Term | float, counts: np.ndarray, n_problems: int,
              problem_mask: np.ndarray | None = None) -> dict:
    full = contrast(a, b, counts, n_problems, problem_mask)
    diag = contrast(_drop(a), _drop(b) if isinstance(b, Term) else b, counts, n_problems, problem_mask)
    iv, dv = full["interval"], diag["interval"]
    chk = make_check(check_id, paper, reading, model_key, kind, direction, tie_width, full["value"],
                     (iv.lo, iv.hi), (dv.lo, dv.hi))
    return {"check": chk.to_dict(), "a": full["a"], "b": full["b"], "interval": interval_dict(iv),
            "diagnostic": {"value": diag["value"], "interval": interval_dict(dv)}}
