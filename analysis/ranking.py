"""Lexicographic ranking by (rank_score, rank_tiebreak) (design sections 1.2 and 7.3).

A recalibrated score is ranked by the pair (isotonic value, pre-map score). Two samples are tied only
when both coordinates are equal; equal rank_score with different tie-breaks are not ties. A NaN
rank_tiebreak means "no tie-break": a readout without a tie-break has NaN in every row, and ranking
then uses rank_score alone. A readout that mixes NaN and finite tie-breaks is a contract violation
(pipeline.readouts writes a tie-break for every row of an iso:<name> readout) and raises ValueError.

Every ranking metric works on the dense integer keys returned here, so a metric depends on the scores
only through their order. That makes invariance to strictly monotone transforms exact.
"""

from __future__ import annotations

import numpy as np

from pipeline.contracts.schemas import ScoredSet


def lex_keys(rank_score: np.ndarray, rank_tiebreak: np.ndarray | None = None,
             use_tiebreak: bool = True) -> np.ndarray:
    """Dense ranks 0..u-1 (int64) of the pairs (rank_score, rank_tiebreak) in lexicographic order.

    Equal keys mean an exact tie. use_tiebreak=False ignores the tie-break (the no-tie-break
    sensitivity analysis of section 1.2)."""
    s = np.asarray(rank_score, dtype=np.float64)
    if s.ndim != 1:
        raise ValueError("rank_score must be one-dimensional")
    if s.size == 0:
        return np.zeros(0, dtype=np.int64)
    if not np.all(np.isfinite(s)):
        raise ValueError("rank_score must be finite")
    tb = None
    if use_tiebreak and rank_tiebreak is not None:
        t = np.asarray(rank_tiebreak, dtype=np.float64)
        if t.shape != s.shape:
            raise ValueError("rank_tiebreak must align with rank_score")
        nan = np.isnan(t)
        if nan.all():
            tb = None
        elif nan.any():
            raise ValueError("rank_tiebreak mixes NaN and finite values; a tie-break must be present "
                             "for every row or for none")
        else:
            if not np.all(np.isfinite(t)):
                raise ValueError("rank_tiebreak must be finite where present")
            tb = t
    if tb is None:
        order = np.argsort(s, kind="stable")
        ss = s[order]
        new = np.empty(s.size, dtype=bool)
        new[0] = True
        new[1:] = ss[1:] != ss[:-1]
    else:
        order = np.lexsort((tb, s))
        ss, tt = s[order], tb[order]
        new = np.empty(s.size, dtype=bool)
        new[0] = True
        new[1:] = (ss[1:] != ss[:-1]) | (tt[1:] != tt[:-1])
    dense_sorted = np.cumsum(new) - 1
    keys = np.empty(s.size, dtype=np.int64)
    keys[order] = dense_sorted
    return keys


def keys_of(s: ScoredSet, use_tiebreak: bool = True) -> np.ndarray:
    """Dense lexicographic keys of a ScoredSet."""
    return lex_keys(s.rank_score, s.rank_tiebreak, use_tiebreak=use_tiebreak)
