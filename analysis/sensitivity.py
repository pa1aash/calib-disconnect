"""Pre-specified sensitivity analyses (design sections 1.2, 1.3, 1.5, 4, 6, 7.1 to 7.4, 7.11).

Each sensitivity is a paired difference against the primary quantity on the same problem draws,
with a 95 percent percentile interval, labeled unadjusted. The primary residual here is the seed-0
residual R^(0) = W(P^(l1)) - W(iso:S^T(l1)) of the 16-cell game (the substitute readouts exist at fold
seed 0 only).

- Readout substitutions (`r_substitutions`): R with the probe replaced by a probe-family member (P2,
  P3, Pmulti), the single-split probe (P2_single_split), or the MLP probe; and with S^T replaced by a
  capacity rung (ST_r1, ST_r4, ST_r16) or the LoRA-plus-head control (ST_head). The ladder's rank-0
  rung is the linear probe P3 at the elicitation position, against which R is W(P) - W(P3).
- Capacity rule (section 7.11): the residual "depends on the readout's capacity" when the paired
  95 percent interval of W(ST_r16) - W(ST_r1) lies entirely outside (-delta, delta), that is
  lo >= delta or hi <= -delta, on either capacity model (CAPACITY_MODELS).
- LoRA-plus-head contrast: W(ST_head) - W(ST), reported as a contrast, not as a stated readout.
- Budget sensitivities (`budget_vs_primary`): the discrimination budget recomputed on altered inputs
  (no tie-break; V1 unparsed samples dropped; the iso:ST map replaced by iso:ST_inner234 or
  iso:ST_insample; extraction-failure and truncated samples excluded; the LiveCodeBench full suite as
  the label analog), with every cell and term reported and its paired difference from the primary.
- Readout-format contrast (section 1.5): M_d(S^R) - M_d(S^T) at g = 0, d in {0, 1}, per suite.
"""

from __future__ import annotations

from typing import Mapping

import numpy as np

from pipeline.contracts.constants import DELTA, SHAPLEY_MARGINAL_LEVEL

from . import gap as G
from .bootstrap import interval_dict, percentile_interval
from .budget import game_report
from .metrics import RankStats
from .shapley import point_terms, shapley

LEVEL = SHAPLEY_MARGINAL_LEVEL
PROBE_SUBSTITUTES = ("P2", "P3", "Pmulti", "P2_single_split", "MLP")
STATED_SUBSTITUTES = ("ST_r1", "ST_r4", "ST_r16", "ST_head")


def _w(inp: G.GapInputs, sc: G.Scores, suite: str, counts, stat: str = "W"):
    rs = RankStats(G.scored(inp, sc, suite), inp.n_problems, inp.use_tiebreak)
    f = rs.W if stat == "W" else rs.auroc_pooled
    return float(f()[0]), (None if counts is None else f(counts))


def paired(pt_a: float, rep_a, pt_b: float, rep_b, level: float = LEVEL) -> dict:
    """a, b, a - b and the percentile interval of the paired difference."""
    d = pt_a - pt_b
    out = {"a": pt_a, "b": pt_b, "diff": d}
    if rep_a is not None and rep_b is not None:
        out["interval"] = interval_dict(percentile_interval(d, np.asarray(rep_a) - np.asarray(rep_b), level))
    return out


def r_substitutions(inp: G.GapInputs, substitutes: Mapping[str, G.Scores], counts) -> dict:
    """R with one readout substituted, and its paired difference from the primary R^(0)."""
    l1 = inp.suites[1]
    wp, wp_r = _w(inp, inp.probe[l1], l1, counts)
    ws, ws_r = _w(inp, inp.trained_iso[l1], l1, counts)
    r0, r0_r = wp - ws, (None if counts is None else wp_r - ws_r)
    out: dict = {"primary_r0": r0}
    for name, sc in substitutes.items():
        wx, wx_r = _w(inp, sc, l1, counts)
        if name in PROBE_SUBSTITUTES:
            rx, rx_r = wx - ws, (None if counts is None else wx_r - ws_r)
            role = "probe"
        else:
            rx, rx_r = wp - wx, (None if counts is None else wp_r - wx_r)
            role = "stated"
        entry = {"role": role, "r": rx, "minus_primary": paired(rx, rx_r, r0, r0_r)}
        if counts is not None:
            entry["r_interval"] = interval_dict(percentile_interval(rx, rx_r, LEVEL))
        out[name] = entry
    if "P3" in substitutes:
        # rank-0 rung of the capacity ladder: the linear probe at the elicitation position as the readout
        w3, w3_r = _w(inp, substitutes["P3"], l1, counts)
        out["ladder_rank0_P3"] = {"r": wp - w3, "minus_primary": paired(wp - w3, None if counts is None else wp_r - w3_r,
                                                                        r0, r0_r)}
    return out


def capacity_rule(inp: G.GapInputs, st_r16: G.Scores, st_r1: G.Scores, counts, delta: float = DELTA) -> dict:
    l1 = inp.suites[1]
    a, a_r = _w(inp, st_r16, l1, counts)
    b, b_r = _w(inp, st_r1, l1, counts)
    p = paired(a, a_r, b, b_r)
    iv = p.get("interval")
    fires = bool(iv is not None and not iv["unavailable"] and (iv["lo"] >= delta or iv["hi"] <= -delta))
    return {"W_r16_minus_W_r1": p, "outside_margin": fires, "delta": delta}


def head_contrast(inp: G.GapInputs, st_head: G.Scores, counts) -> dict:
    l1 = inp.suites[1]
    a, a_r = _w(inp, st_head, l1, counts)
    b, b_r = _w(inp, inp.trained[l1], l1, counts)
    return {"W_head_minus_W_ST": paired(a, a_r, b, b_r)}


def readout_format_contrast(inp: G.GapInputs, sr: Mapping[str, G.Scores], counts) -> dict:
    """M_d(S^R) - M_d(S^T) at g = 0 for each suite with S^R scores (section 1.5)."""
    out = {}
    for suite, sc in sr.items():
        for d, stat in ((0, "auroc"), (1, "W")):
            a, a_r = _w(inp, sc, suite, counts, stat)
            b, b_r = _w(inp, inp.trained[suite], suite, counts, stat)
            out[f"d{d}_{suite}"] = paired(a, a_r, b, b_r)
    return out


def budget_vs_primary(primary_store: dict, alt: G.GapInputs, counts) -> dict:
    """Discrimination budget on altered inputs, and the paired difference of every cell and term
    from the primary budget."""
    pt = G.discrimination_cells(alt)["cells"]
    rp = None if counts is None else G.discrimination_cells(alt, counts)["cells"]
    rep, terms_rep = game_report(pt, rp)
    terms_pt = point_terms(shapley(pt))
    diffs = {}
    for k, v in pt.items():
        diffs[f"cell_{k}"] = paired(v, None if rp is None else rp[k], primary_store["disc_cells_pt"][k],
                                    None if primary_store.get("disc_cells_rep") is None else primary_store["disc_cells_rep"][k])
    for k, v in terms_pt.items():
        diffs[k] = paired(v, None if terms_rep is None else terms_rep[k], primary_store["disc_terms_pt"][k],
                          None if primary_store.get("disc_terms_rep") is None else primary_store["disc_terms_rep"][k])
    rep["minus_primary"] = diffs
    return rep
