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
from pipeline.contracts.schemas import TOGGLES

from .shapley import (LABELS_FIRST, READOUT_FIRST, SPLIT_POSITIONS, point_terms, readout_change_split, shapley,
                      shapley_replicates)

THREE_PLAYERS = ("r", "t", "d")
THREE_LABELS_FIRST = ("d", "t", "r")      # the labels-first order without l
THREE_READOUT_FIRST = ("r", "t", "d")


def three_player_cells(cells4: Mapping[str, object], l: int = 1) -> dict:
    """Cells of the (r, t, d) game at a fixed label coordinate l, keyed "rtd" (section 4: the
    LiveCodeBench budget has three toggles, at l = lcb_label)."""
    return {k[:3]: cells4[k] for k in cells4 if k[3] == str(l)}


def three_player_report(cells4_pt, cells4_rep, l: int = 1) -> tuple[dict, dict | None]:
    pt = three_player_cells(cells4_pt, l)
    rp = None if cells4_rep is None else three_player_cells(cells4_rep, l)
    return game_report(pt, rp, THREE_PLAYERS, (THREE_LABELS_FIRST, THREE_READOUT_FIRST))

LEVELS = (SHAPLEY_MARGINAL_LEVEL, SHAPLEY_SIMULTANEOUS_LEVEL)


def simultaneous_level(n_terms: int) -> float:
    """Section 9 Bonferroni construction over a game's Shapley terms: 1 - 0.05 / n_terms (98.75 percent
    for the four-player game, SHAPLEY_SIMULTANEOUS_LEVEL; 1 - 0.05 / 3 for the three-player game)."""
    return 1 - (1 - SHAPLEY_MARGINAL_LEVEL) / n_terms


def pooled_levels(n_players: int) -> tuple:
    """Levels for model-pooled terms: the 95 percent marginal level, the game's own Bonferroni level, and
    (for games with fewer than four players) the four-term 98.75 percent level beside it for comparison."""
    out = [SHAPLEY_MARGINAL_LEVEL, simultaneous_level(n_players)]
    if SHAPLEY_SIMULTANEOUS_LEVEL not in out:
        out.append(SHAPLEY_SIMULTANEOUS_LEVEL)
    return tuple(out)


def _lvl(lv: float) -> str:
    return f"{lv:g}"


def intervals(points: Mapping[str, float], reps: Mapping[str, np.ndarray], levels=LEVELS) -> dict:
    return {k: {_lvl(lv): interval_dict(percentile_interval(points[k], reps[k], lv)) for lv in levels}
            for k in points}


def game_report(cells_pt: Mapping[str, float], cells_rep: Mapping[str, np.ndarray] | None,
                players=TOGGLES, orders=(LABELS_FIRST, READOUT_FIRST), term_levels=LEVELS) -> tuple[dict, dict | None]:
    """Shapley result with intervals. Returns (serializable report, per-resample term arrays)."""
    res = shapley(cells_pt, players, orders)
    rep_terms = None
    out = {"shapley": res.to_dict()}
    if cells_rep is not None:
        rep_terms = shapley_replicates(cells_rep, players, orders)
        out["term_intervals"] = intervals(point_terms(res), rep_terms, term_levels)
        out["cell_intervals"] = intervals(dict(cells_pt), dict(cells_rep), (SHAPLEY_MARGINAL_LEVEL,))
    return out, rep_terms


def model_budget(inp: G.GapInputs, counts: np.ndarray | None, inp_v2: G.GapInputs | None = None,
                 secondary: bool = True, routing: bool = True, three_player: bool = False,
                 diagnostics: bool = True) -> tuple[dict, dict]:
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
    store["disc_terms_pt"] = point_terms(shapley(d_pt["cells"]))
    if three_player:
        tp, tp_terms = three_player_report(d_pt["cells"], None if d_rep is None else d_rep["cells"])
        tp["label_coordinate"] = inp.suites[1]
        tp["primary"] = True              # DEV-011: the three-player game is primary on LiveCodeBench
        report["discrimination"]["primary"] = False
        report["discrimination_three_player"] = tp
        store["three_terms_pt"] = point_terms(shapley(three_player_cells(d_pt["cells"]), THREE_PLAYERS,
                                                      (THREE_LABELS_FIRST, THREE_READOUT_FIRST)))
        store["three_terms_rep"] = tp_terms

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

    if not diagnostics:
        return report, store
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


def pooled_budget(stores: Mapping[str, dict], key_pt: str = "disc_cells_pt", key_rep: str = "disc_cells_rep",
                  three_player: bool = False) -> dict:
    """Model-pooled budget: cells averaged over models (point and per resample), Shapley terms of the
    averaged game (equal to the average of per-model terms, by linearity), simultaneous Bonferroni
    and marginal 95 percent intervals, and heterogeneity of G0 and every term across models.

    four-player game: simultaneous 98.75 percent (four terms). three_player=True: the (r, t, d) game at
    l = 1 (DEV-011, primary on LiveCodeBench), with the same construction over its three terms
    (1 - 0.05 / 3) and the 98.75 percent level beside it. Pooled Shapley terms are not refit-widened in
    either game (section 9 widens R and the decisions only)."""
    models = list(stores)
    if three_player:
        players, orders = THREE_PLAYERS, (THREE_LABELS_FIRST, THREE_READOUT_FIRST)
        cut = lambda c: three_player_cells(c)  # noqa: E731
    else:
        players, orders = TOGGLES, (LABELS_FIRST, READOUT_FIRST)
        cut = lambda c: c  # noqa: E731
    per_pt = {m: cut(stores[m][key_pt]) for m in models}
    keys = list(per_pt[models[0]])
    cells_pt = {k: float(np.mean([per_pt[m][k] for m in models])) for k in keys}
    have_rep = all(stores[m].get(key_rep) is not None for m in models)
    per_rep = {m: cut(stores[m][key_rep]) for m in models} if have_rep else None
    cells_rep = ({k: np.mean(np.vstack([per_rep[m][k] for m in models]), axis=0) for k in keys}
                 if have_rep else None)
    levels = pooled_levels(len(players))
    rep, _ = game_report(cells_pt, cells_rep, players, orders, levels)
    rep["models"] = models
    rep["players"] = list(players)
    rep["interval_levels"] = {"marginal": SHAPLEY_MARGINAL_LEVEL, "simultaneous": simultaneous_level(len(players)),
                              "all": list(levels)}
    if have_rep:
        per_model_terms = {}
        for m in models:
            res = shapley(per_pt[m], players, orders)
            per_model_terms[m] = (point_terms(res), shapley_replicates(per_rep[m], players, orders))
        het = {}
        for term in per_model_terms[models[0]][0]:
            het[term] = heterogeneity({m: per_model_terms[m][0][term] for m in models},
                                      {m: per_model_terms[m][1][term] for m in models})
        rep["heterogeneity"] = het
    return rep
