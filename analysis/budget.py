"""Per-model and model-pooled budgets with intervals (design sections 1.4, 1.8, 9, 10).

Interval levels (section 9, multiplicity): model-pooled Shapley terms carry simultaneous Bonferroni
intervals (98.75 percent, four terms) with 95 percent marginal intervals beside them; per-model and
per-stratum terms are at 95 percent, labeled unadjusted (both levels are computed and labeled, and
the paper uses the one its section names). Cells, interactions, sequential terms, and diagnostics get
95 percent percentile intervals from the same draws.
"""

from __future__ import annotations

from typing import Mapping

import numpy as np

from pipeline.contracts.constants import SHAPLEY_MARGINAL_LEVEL, SHAPLEY_SIMULTANEOUS_LEVEL

from . import gap as G
from . import routing as RT
from .bootstrap import interval_dict, percentile_interval
from .decisions import heterogeneity
from .shapley import SPLIT_POSITIONS, point_terms, readout_change_split, shapley, shapley_replicates

LEVELS = (SHAPLEY_MARGINAL_LEVEL, SHAPLEY_SIMULTANEOUS_LEVEL)


def _lvl(lv: float) -> str:
    return f"{lv:g}"


def intervals(points: Mapping[str, float], reps: Mapping[str, np.ndarray], levels=LEVELS) -> dict:
    return {k: {_lvl(lv): interval_dict(percentile_interval(points[k], reps[k], lv)) for lv in levels}
            for k in points}


def game_report(cells_pt: Mapping[str, float], cells_rep: Mapping[str, np.ndarray] | None) -> tuple[dict, dict | None]:
    """Shapley result with intervals. Returns (serializable report, per-resample term arrays)."""
    res = shapley(cells_pt)
    rep_terms = None
    out = {"shapley": res.to_dict()}
    if cells_rep is not None:
        rep_terms = shapley_replicates(cells_rep)
        out["term_intervals"] = intervals(point_terms(res), rep_terms)
        out["cell_intervals"] = intervals(dict(cells_pt), dict(cells_rep), (SHAPLEY_MARGINAL_LEVEL,))
    return out, rep_terms


def model_budget(inp: G.GapInputs, counts: np.ndarray | None, inp_v2: G.GapInputs | None = None,
                 secondary: bool = True, routing: bool = True) -> tuple[dict, dict]:
    """Everything per model at fold seed 0. Returns (report, replicate store); the store holds the
    per-resample cells and terms used for model pooling and is not serialized."""
    report: dict = {}
    store: dict = {}
    d_pt = G.discrimination_cells(inp)
    d_rep = G.discrimination_cells(inp, counts) if counts is not None else None
    disc, disc_terms = game_report(d_pt["cells"], None if d_rep is None else d_rep["cells"])
    disc["probe_component"] = d_pt["probe"]
    disc["stated_component"] = d_pt["stated"]
    report["discrimination"] = disc
    store["disc_cells_pt"] = d_pt["cells"]
    store["disc_cells_rep"] = None if d_rep is None else d_rep["cells"]
    store["disc_terms_rep"] = disc_terms

    if inp_v2 is not None:
        v_pt = G.discrimination_cells(inp_v2)
        v_rep = G.discrimination_cells(inp_v2, counts) if counts is not None else None
        v2, v2_terms = game_report(v_pt["cells"], None if v_rep is None else v_rep["cells"])
        report["discrimination_v2_chain"] = v2
        store["v2_cells_pt"] = v_pt["cells"]
        store["v2_cells_rep"] = None if v_rep is None else v_rep["cells"]
        store["v2_terms_rep"] = v2_terms
        split = {}
        for name, rdl in SPLIT_POSITIONS.items():
            sp = {k: float(v) for k, v in readout_change_split(d_pt["cells"], v_pt["cells"], rdl).items()}
            entry: dict = {"point": sp}
            if v_rep is not None:
                sr = readout_change_split(d_rep["cells"], v_rep["cells"], rdl)
                entry["intervals"] = intervals(sp, sr)
                store.setdefault("split_rep", {})[name] = sr
            split[name] = entry
        report["readout_change_split"] = split
        store["split_pt"] = {name: split[name]["point"] for name in split}

    report["diagnostics"] = {}
    dd_pt = G.d_diagnostics(inp)
    entry = {"point": dd_pt}
    if counts is not None:
        dd_rep = G.d_diagnostics(inp, counts)
        entry["intervals"] = {k: intervals(dd_pt[k], dd_rep[k], (SHAPLEY_MARGINAL_LEVEL,)) for k in dd_pt}
    report["diagnostics"]["d"] = entry
    ll_pt = G.l_diagnostics(inp)
    entry = {"point": ll_pt}
    if counts is not None:
        ll_rep = G.l_diagnostics(inp, counts)
        num = {k: v for k, v in ll_pt.items() if k != "counts"}
        entry["intervals"] = intervals(num, ll_rep, (SHAPLEY_MARGINAL_LEVEL,))
    report["diagnostics"]["l"] = entry
    rt_pt = G.rt_diagnostics(inp)
    entry = {"point": rt_pt}
    if counts is not None:
        rt_rep = G.rt_diagnostics(inp, counts)
        entry["intervals"] = {k: intervals(rt_pt[k], rt_rep[k], (SHAPLEY_MARGINAL_LEVEL,)) for k in rt_pt}
    report["diagnostics"]["rt"] = entry
    report["tie_rates"] = G.tie_rates(inp)
    report["imputation_tie_share"] = G.imputation_tie_share(inp)

    if secondary:
        report["secondary"] = {}
        store["secondary"] = {}
        for est in G.SECONDARY_ESTIMATORS:
            s_pt = G.secondary_cells(inp, est)
            s_rep = G.secondary_cells(inp, est, counts) if counts is not None else None
            sec, sec_terms = game_report(s_pt["cells"], None if s_rep is None else s_rep["cells"])
            sec["sign"] = s_pt["sign"]
            sec["probe_component"] = s_pt["probe"]
            sec["stated_component"] = s_pt["stated"]
            report["secondary"][est] = sec
            store["secondary"][est] = {"pt": s_pt["cells"], "rep": None if s_rep is None else s_rep["cells"]}

    if routing:
        r_pt = RT.routing_cells(inp)
        r_rep = RT.routing_cells(inp, counts) if counts is not None else None
        rr = {"anchors": r_pt["anchors"], "games": {}}
        for b, g in r_pt["games"].items():
            gr, _ = game_report(g["cells"], None if r_rep is None else r_rep["games"][b]["cells"])
            gr["probe_regret"] = g["probe_regret"]
            gr["stated_regret"] = g["stated_regret"]
            rr["games"][b] = gr
        report["routing"] = rr
    return report, store


def pooled_budget(stores: Mapping[str, dict], key_pt: str = "disc_cells_pt", key_rep: str = "disc_cells_rep") -> dict:
    """Model-pooled budget: cells averaged over models (point and per resample), Shapley terms of the
    averaged game (equal to the average of per-model terms, by linearity), simultaneous 98.75 and
    marginal 95 percent intervals, and heterogeneity of G0 and every term across models."""
    models = list(stores)
    keys = list(stores[models[0]][key_pt])
    cells_pt = {k: float(np.mean([stores[m][key_pt][k] for m in models])) for k in keys}
    have_rep = all(stores[m].get(key_rep) is not None for m in models)
    cells_rep = ({k: np.mean(np.vstack([stores[m][key_rep][k] for m in models]), axis=0) for k in keys}
                 if have_rep else None)
    rep, _ = game_report(cells_pt, cells_rep)
    rep["models"] = models
    if have_rep:
        per_model_terms = {}
        for m in models:
            res = shapley(stores[m][key_pt])
            per_model_terms[m] = (point_terms(res), shapley_replicates(stores[m][key_rep]))
        het = {}
        for term in per_model_terms[models[0]][0]:
            het[term] = heterogeneity({m: per_model_terms[m][0][term] for m in models},
                                      {m: per_model_terms[m][1][term] for m in models})
        rep["heterogeneity"] = het
    return rep
