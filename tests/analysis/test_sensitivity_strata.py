"""Sensitivities, strata, the three-player game, and the LiveCodeBench stage outputs."""

import json

import numpy as np
import pandas as pd

from analysis import gap as G
from analysis import sensitivity as SENS
from analysis import strata as ST
from analysis import stage
from analysis.bootstrap import draw
from analysis.budget import pooled_budget, simultaneous_level, THREE_LABELS_FIRST, THREE_PLAYERS, THREE_READOUT_FIRST, model_budget, three_player_cells, three_player_report
from analysis.gap import Scores, replace_inputs, subset_inputs
from analysis.shapley import shapley
from pipeline.contracts.constants import BOOTSTRAP_SEED, PRIMARY_MODELS
from pipeline.contracts.interfaces import RunConfig
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest
from pipeline.contracts.schemas import TABLE_COLUMNS, sample_uid
from synth import make_inputs, v2_chain


def _draws(inp, b=60):
    return draw(list(range(inp.n_problems)), b, BOOTSTRAP_SEED).counts


# ---------------------------------------------------------------------------------------------------
# Contamination partition
# ---------------------------------------------------------------------------------------------------
def test_contamination_partition_labels():
    probs = ["a", "b", "c", "d"]
    rd = {"a": "2024-06-01", "b": "2025-01-01", "c": "2025-03-01", "d": None}
    olmo = ST.contamination_partition("P3", probs, rd)          # stated count date 2024-12-31
    assert olmo["count_date_stated"] and olmo["has_stratum"]
    assert olmo["masks"]["post"].tolist() == [False, True, True, False]
    assert olmo["masks"]["pre"].tolist() == [True, False, False, False]
    assert olmo["masks"]["pre_or_unknown"].tolist() == [False, False, False, True]
    qwen = ST.contamination_partition("P1", probs, rd)           # upper bound 2025-04-27
    assert not qwen["count_date_stated"] and not qwen["has_stratum"]
    assert set(qwen["masks"]) == {"post", "pre_or_unknown"}
    assert qwen["masks"]["pre_or_unknown"].all()
    # the boundary day itself is not "post"
    assert not ST.contamination_partition("P3", ["e"], {"e": "2024-12-31"})["masks"]["post"].any()
    assert ST.count_date_is_stated("P5") and not ST.count_date_is_stated("C1")


# ---------------------------------------------------------------------------------------------------
# Three-player game
# ---------------------------------------------------------------------------------------------------
def test_three_player_cells_and_efficiency():
    inp = make_inputs(3, n_problems=20, k=5)
    cells = G.discrimination_cells(inp)["cells"]
    c3 = three_player_cells(cells, l=1)
    assert len(c3) == 8 and all(len(k) == 3 for k in c3)
    for k, v in c3.items():
        assert v == cells[k + "1"]
    res = shapley(c3, players=THREE_PLAYERS, orders=(THREE_LABELS_FIRST, THREE_READOUT_FIRST))
    tot = c3["111"] - c3["000"]
    assert abs(sum(res.phi.values()) - tot) <= 1e-12
    assert abs(sum(res.seq_labels_first.values()) - tot) <= 1e-12
    counts = _draws(inp, 40)
    rep, _ = three_player_report(cells, G.discrimination_cells(inp, counts)["cells"])
    assert abs(rep["shapley"]["efficiency_gap"]) <= 1e-12


def test_pooled_three_player_levels_and_linearity():
    stores = {}
    for i, m in enumerate(("P1", "P2", "P3")):
        inp = make_inputs(30 + i, n_problems=20, k=5)
        _, stores[m] = model_budget(inp, _draws(inp, 50), None, secondary=False, routing=False, three_player=True)
    pb = pooled_budget(stores, three_player=True)
    lv3 = simultaneous_level(3)
    assert abs(lv3 - (1 - 0.05 / 3)) <= 1e-15 and pb["interval_levels"]["simultaneous"] == lv3
    assert pb["players"] == ["r", "t", "d"]
    for term, ivs in pb["term_intervals"].items():
        assert {f"{0.95:g}", f"{lv3:g}", f"{1 - 0.05 / 4:g}"} == set(ivs)
        sim, mar = ivs[f"{lv3:g}"], ivs[f"{0.95:g}"]
        assert sim["lo"] <= mar["lo"] and sim["hi"] >= mar["hi"]     # simultaneous is wider
    # pooled terms equal the mean of per-model three-player terms (linearity)
    for p in ("r", "t", "d"):
        want = np.mean([stores[m]["three_terms_pt"][f"phi_{p}"] for m in stores])
        assert abs(pb["shapley"]["phi"][p] - want) <= 1e-12
    assert set(pb["heterogeneity"]) == set(pb["term_intervals"])
    p4 = pooled_budget(stores)
    assert p4["interval_levels"]["simultaneous"] == 1 - 0.05 / 4


# ---------------------------------------------------------------------------------------------------
# Sensitivities
# ---------------------------------------------------------------------------------------------------
def test_identity_sensitivities_are_zero():
    inp = make_inputs(4, n_problems=20, k=5)
    counts = _draws(inp)
    _, store = model_budget(inp, counts, None, secondary=False, routing=False)
    l1 = inp.suites[1]
    out = SENS.r_substitutions(inp, {"P2": inp.probe[l1], "ST_r4": inp.trained_iso[l1]}, counts)
    for name in ("P2", "ST_r4"):
        d = out[name]["minus_primary"]
        assert d["diff"] == 0.0 and d["interval"]["lo"] == 0.0 and d["interval"]["hi"] == 0.0
    bvp = SENS.budget_vs_primary(store, replace_inputs(inp), counts)
    assert all(abs(v["diff"]) <= 1e-15 for v in bvp["minus_primary"].values())
    sc = ST.stratum_contrasts({"P1": store, "B1": store})
    for v in sc["instruct_minus_base"]["P1-B1"]["terms"].values():
        assert v["diff"] == 0.0 and v["interval"]["lo"] == 0.0
    assert sc["adjustment"].startswith("unadjusted")


def test_capacity_rule_boolean():
    inp = make_inputs(5, n_problems=30, k=5)
    counts = _draws(inp, 80)
    l1 = inp.suites[1]
    same = SENS.capacity_rule(inp, inp.trained[l1], inp.trained[l1], counts)
    assert not same["outside_margin"]
    rng = np.random.default_rng(0)
    noise = rng.normal(size=inp.problem_index.size)
    good = inp.probe[l1]
    bad = Scores(rank_score=noise, rank_tiebreak=np.full(noise.size, np.nan), prob=noise)
    assert SENS.capacity_rule(inp, good, bad, counts, delta=0.02)["outside_margin"]
    rev = SENS.capacity_rule(inp, bad, good, counts, delta=0.02)
    assert rev["outside_margin"] and rev["W_r16_minus_W_r1"]["interval"]["hi"] <= -0.02


def test_no_tiebreak_and_subset_inputs():
    inp = make_inputs(6, n_problems=20, k=5)
    alt = replace_inputs(inp, use_tiebreak=False)
    assert alt.use_tiebreak is False and inp.use_tiebreak is True
    mask = inp.problem_index < 10
    sub = subset_inputs(inp, mask)
    assert sub.problem_index.size == int(mask.sum()) and sub.n_problems == inp.n_problems
    # a problem-aligned subset equals the full set with zero weight on the dropped problems
    w = (np.arange(inp.n_problems) < 10).astype(np.uint16)[None, :]
    a = G.discrimination_cells(sub)["cells"]
    b = G.discrimination_cells(inp, w)["cells"]
    assert all(abs(a[k] - float(b[k][0])) <= 1e-12 for k in a)
    # dropping the tie-break changes at least one cell (the isotonic readouts carry raw-score tie-breaks)
    c0, c1 = G.discrimination_cells(inp)["cells"], G.discrimination_cells(alt)["cells"]
    assert any(abs(c0[k] - c1[k]) > 1e-9 for k in c0)


# ---------------------------------------------------------------------------------------------------
# LiveCodeBench stage run: three-player game, contamination, listings, sensitivities, sealing
# ---------------------------------------------------------------------------------------------------
N_P, K = 20, 5
LCB = ("lcb_public", "lcb_label")


def _df(model, readout, suite, seed, uids, sc):
    n = len(uids)
    return pd.DataFrame({
        "sample_uid": uids, "model_key": model, "population": "lcb", "readout": readout, "label_suite": suite,
        "fold_seed": seed, "fold": 0, "prob": sc.prob, "rank_score": sc.rank_score,
        "rank_tiebreak": sc.rank_tiebreak, "missing": np.zeros(n, bool), "imputed": np.zeros(n, bool),
        "generation_set": "frozen", "flagged": False,
    })[list(TABLE_COLUMNS["scores"])]


def build_lcb_run(tmp_path):
    layout = RunLayout.for_run("l", tmp_path / "runs")
    (layout.root / "data").mkdir(parents=True)
    problems = [f"lcb/q{i:02d}" for i in range(N_P)]
    # first half before every count date, second half after Olmo 3 and Gemma 4, before Qwen3
    with layout.problems("lcb_v6").open("w") as fh:
        for i, q in enumerate(problems):
            fh.write(json.dumps({"problem_id": q, "release_date": "2024-06-01" if i < 10 else "2025-03-01"}) + "\n")
    for mi, m in enumerate(PRIMARY_MODELS):
        inp = make_inputs(20 + mi, n_problems=N_P, k=K, suites=LCB)
        v2 = v2_chain(inp)
        uids = [sample_uid(m, "lcb_v6", problems[i], j + 1) for i in range(N_P) for j in range(K)]
        y_full = inp.labels["lcb_label"].copy()
        y_pub = inp.labels["lcb_public"].copy()
        y_pub[inp.problem_index == 0] = 0                     # nobody passes q00 publicly
        y_full[inp.problem_index == 1] = 0                    # q01: public passes all fail the full suite
        y_pub[(inp.problem_index == 1) & (np.arange(len(uids)) % K == 0)] = 1
        lab = [{"sample_uid": u, "suite_id": s, "y": int(y[n]), "source": "execution", "failure": None,
                "cache_key": None}
               for n, u in enumerate(uids) for s, y in (("lcb_public", y_pub), ("lcb_label", inp.labels["lcb_label"]),
                                                        ("lcb_full", y_full))]
        lp = layout.labels(m, "lcb_v6", "frozen")
        lp.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(lab).to_parquet(lp)
        tabs = [_df(m, "SZ_V1", None, 0, uids, inp.zero_shot), _df(m, "SZ_V2", None, None, uids, v2.zero_shot)]
        for s in LCB + ("lcb_full",):
            src = s if s in LCB else "lcb_label"
            tabs += [_df(m, "P", s, 0, uids, inp.probe[src]), _df(m, "ST", s, 0, uids, inp.trained[src]),
                     _df(m, "iso:ST", s, 0, uids, inp.trained_iso[src]),
                     _df(m, "iso:SZ_V1", s, 0, uids, inp.zero_shot_iso[src]),
                     _df(m, "iso:SZ_V2", s, 0, uids, v2.zero_shot_iso[src])]
        if m == "P3":
            l1 = "lcb_label"
            tabs += [_df(m, "P2", l1, 0, uids, inp.probe[l1]), _df(m, "ST_r1", l1, 0, uids, inp.trained[l1]),
                     _df(m, "ST_r16", l1, 0, uids, inp.trained[l1]), _df(m, "ST_head", l1, 0, uids, inp.trained[l1]),
                     _df(m, "SR", l1, 0, uids, inp.trained[l1])]
            for s in LCB:
                tabs.append(_df(m, "iso:ST_insample", s, 0, uids, inp.trained_iso[s]))
        for t in tabs:
            r = t.iloc[0]
            p = layout.scores(m, "lcb", r["readout"], r["label_suite"],
                              None if pd.isna(r["fold_seed"]) else int(r["fold_seed"]))
            p.parent.mkdir(parents=True, exist_ok=True)
            t.to_parquet(p)
    Manifest(run_id="l").save(layout.manifest)
    return layout


def _cfg(tmp_path, seal):
    return RunConfig(run_id="l", models=PRIMARY_MODELS, benchmarks=("lcb_v6",), seal_gamma=seal,
                     extra={"bootstrap_b": 30, "analysis_root": str(tmp_path / "analysis"),
                            "secondary_budgets": False, "routing": False})


def test_stage_lcb_outputs(tmp_path):
    layout = build_lcb_run(tmp_path)
    rep = stage.run(_cfg(tmp_path, False), layout, Manifest.load(layout.manifest))
    assert rep.ok, rep.notes
    res = tmp_path / "analysis" / "results" / "l"
    budgets = json.loads((res / "budgets.json").read_text())["budgets"]
    tp = budgets["P3|lcb"]["discrimination_three_player"]
    assert set(tp["shapley"]["phi"]) == set(THREE_PLAYERS)
    pooled = json.loads((res / "pooled.json").read_text())["pooled"]["lcb"]
    assert pooled["budget_three_player"]["primary"] is True and pooled["budget_primary_chain"]["primary"] is False
    assert pooled["budget_three_player"]["interval_levels"]["simultaneous"] == simultaneous_level(3)
    assert tp["primary"] is True and budgets["P3|lcb"]["discrimination"]["primary"] is False
    con = json.loads((res / "contamination.json").read_text())["contamination"]
    assert con["P1"]["has_stratum"] is False and con["P2"]["has_stratum"] is False
    assert con["P3"]["has_stratum"] and con["P3"]["partitions"]["post"]["n_problems"] == 10
    assert "post_minus_pre" in con["P3"]
    pc = con["pooled_olmo3_gemma4"]
    assert pc["no_stratum"] == ["P1", "P2"] and "post_minus_pre" in pc
    assert pc["post"]["three_player"]["primary"] is True and pc["post"]["four_player"]["primary"] is False
    sens = json.loads((res / "sensitivity.json").read_text())["sensitivity"]
    s3 = sens["P3|lcb"]
    for key in ("readout_substitutions", "capacity_rule", "head_contrast", "no_tiebreak_budget",
                "iso_map_ST_insample", "readout_format_contrast_g0", "lcb_full_labeling"):
        assert key in s3, key
    assert s3["capacity_rule"]["outside_margin"] is False          # identical rungs
    assert abs(s3["iso_map_ST_insample"]["minus_primary"]["cell_1111"]["diff"]) <= 1e-15
    assert "capacity_rule" not in sens["P1|lcb"] and "lcb_full_labeling" in sens["P1|lcb"]
    strata = json.loads((res / "strata.json").read_text())["strata"]
    assert "family" in strata["lcb"] and "scale" in strata["lcb"]
    ops = json.loads((res / "operational.json").read_text())
    lst = ops["lcb_listings"]
    assert "lcb/q00" in lst["no_sample_passes_public"]
    assert "lcb/q01" in lst["public_full_disagree_for_every_passing_sample"]
    idx = json.loads((res / "INDEX.json").read_text())["files"]
    assert {"sensitivity.json", "contamination.json", "strata.json"} <= set(idx)


def test_stage_lcb_sealed(tmp_path):
    layout = build_lcb_run(tmp_path)
    rep = stage.run(_cfg(tmp_path, True), layout, Manifest.load(layout.manifest))
    assert rep.ok
    res = tmp_path / "analysis" / "results" / "l"
    assert sorted(p.name for p in res.iterdir()) == ["INDEX.json", "operational.json"]
    text = (res / "operational.json").read_text()
    for banned in ("shapley", "phi", "cells", "terms", "minus_primary", "post_minus", "three_player", "residual",
                   "primary\": true", "interval_levels"):
        assert banned not in text, banned
    sealed = json.loads((layout.sealed / "gamma_sealed.json").read_text())
    assert {"sensitivity", "contamination", "strata"} <= set(sealed)
    assert "lcb_listings" in json.loads(text)
