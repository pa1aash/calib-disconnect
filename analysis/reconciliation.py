"""Reconciliation outcome rules (design section 2.1; red team K9 to K12).

Each check gives a paired 95 percent interval (lo, hi) (RECONCILIATION_LEVEL) and is classified:
- "ordering" (interval of first minus second; direction +1 if the published pattern has the first
  above the second, -1 if below): consistent when the interval excludes zero in the published
  direction (direction +1: lo > 0; direction -1: hi < 0); not consistent when it excludes zero in the
  opposite direction; otherwise undetermined.
- "tie" (interval of the difference, tie width w > 0): consistent when the interval lies inside
  (-w, w), i.e. -w < lo and hi < w; not consistent when it lies entirely outside (-w, w), i.e.
  hi <= -w or lo >= w; otherwise undetermined.
- "above_value" (interval of the value minus the reference value, for example W - 0.5): classified
  like an ordering against the reference.
An unavailable interval (NaN bounds) is undetermined.

Per paper, one verb (section 2.1): "consistent" if every check is consistent, "not consistent" if any
check is not consistent, otherwise "partly consistent", with the counts.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np

from pipeline.contracts.schemas import ReconciliationCheck

CONSISTENT, NOT_CONSISTENT, UNDETERMINED = "consistent", "not_consistent", "undetermined"


def classify(kind: str, interval: tuple[float, float], direction: int = 1, tie_width: float | None = None) -> str:
    lo, hi = float(interval[0]), float(interval[1])
    if not (np.isfinite(lo) and np.isfinite(hi)):
        return UNDETERMINED
    if lo > hi:
        raise ValueError("interval lower bound exceeds upper bound")
    if kind in ("ordering", "above_value"):
        if direction not in (1, -1):
            raise ValueError("direction must be +1 or -1")
        if (direction == 1 and lo > 0) or (direction == -1 and hi < 0):
            return CONSISTENT
        if (direction == 1 and hi < 0) or (direction == -1 and lo > 0):
            return NOT_CONSISTENT
        return UNDETERMINED
    if kind == "tie":
        if tie_width is None or not tie_width > 0:
            raise ValueError("a tie check needs a positive tie width")
        w = float(tie_width)
        if -w < lo and hi < w:
            return CONSISTENT
        if hi <= -w or lo >= w:
            return NOT_CONSISTENT
        return UNDETERMINED
    raise ValueError(f"unknown check kind {kind!r}")


def paper_verb(outcomes: Sequence[str]) -> tuple[str, dict[str, int]]:
    if not outcomes:
        raise ValueError("no checks")
    bad = [o for o in outcomes if o not in (CONSISTENT, NOT_CONSISTENT, UNDETERMINED)]
    if bad:
        raise ValueError(f"unknown outcomes {bad}")
    counts = {"n": len(outcomes), "consistent": sum(o == CONSISTENT for o in outcomes),
              "not_consistent": sum(o == NOT_CONSISTENT for o in outcomes),
              "undetermined": sum(o == UNDETERMINED for o in outcomes)}
    if counts["consistent"] == counts["n"]:
        verb = "consistent"
    elif counts["not_consistent"] > 0:
        verb = "not consistent"
    else:
        verb = "partly consistent"
    return verb, counts


def make_check(check_id: str, paper: str, reading: str | None, model_key: str, kind: str, direction: int,
               tie_width: float | None, value: float, interval: tuple[float, float],
               diagnostic_interval: tuple[float, float] | None = None) -> ReconciliationCheck:
    """Build a ReconciliationCheck; the outcome uses the full set and the truncation- and
    extraction-excluded interval, if given, gives the diagnostic outcome (section 2.1, K12)."""
    out = classify(kind, interval, direction if kind != "tie" else 1, tie_width)
    diag = None
    if diagnostic_interval is not None:
        diag = classify(kind, diagnostic_interval, direction if kind != "tie" else 1, tie_width)
    return ReconciliationCheck(check_id=check_id, paper=paper, reading=reading, model_key=model_key, kind=kind,
                               direction=0 if kind == "tie" else direction, tie_width=tie_width,
                               value=float(value), interval=(float(interval[0]), float(interval[1])),
                               outcome=out, diagnostic_excluding_truncation=diag)
