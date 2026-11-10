"""Shapley game, gap cells, routing replay, and generation shift."""

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from analysis import gap as G
from analysis import metrics as M
from analysis import routing as RT
from analysis import shapley as SH
from analysis._common import make_scored_set
from analysis.bootstrap import draw
from analysis.budget import model_budget, pooled_budget
from analysis.generation_shift import GenSet, contrasts, set_rates
from synth import make_inputs, v2_chain


def game(fn):
    return {k: fn(dict(zip("rtdl", map(int, k)))) for k in SH.all_keys()}


# ---------------------------------------------------------------------------------------------------
# Shapley
# ---------------------------------------------------------------------------------------------------
def test_shapley_additive_game_hand():
    # v(S) = 1 + sum of a_i over members: phi = a, all interactions 0, both orders give a
    a = {"r": 0.1, "t": -0.3, "d": 0.2, "l": 0.05}
    res = SH.shapley(game(lambda x: 1 + sum(a[p] * x[p] for p in "rtdl")))
    for p in "rtdl":
        assert res.phi[p] == pytest.approx(a[p], abs=1e-15)
        assert res.seq_labels_first[p] == pytest.approx(a[p], abs=1e-15)
    assert all(abs(v) < 1e-15 for v in res.interactions.values())
    assert res.g0 == 1.0 and abs(res.efficiency_gap) < 1e-15


def test_shapley_unanimity_game_hand():
    # v(S) = 1 if {r, t} in S: phi_r = phi_t = 1/2, phi_d = phi_l = 0, I_rt = 1, other pairs 0
    # labels first (l, d, t, r): t enters without r -> 0, r enters after t -> 1
    # readout first (r, t, d, l): r enters first -> 0, t -> 1
    res = SH.shapley(game(lambda x: float(x["r"] and x["t"])))
    assert res.phi == pytest.approx({"r": 0.5, "t": 0.5, "d": 0.0, "l": 0.0})
    assert res.interactions["rt"] == pytest.approx(1.0)
    assert all(res.interactions[k] == pytest.approx(0.0) for k in ("rd", "rl", "td", "tl", "dl"))
    assert res.seq_labels_first == pytest.approx({"l": 0, "d": 0, "t": 0, "r": 1})
    assert res.seq_readout_first == pytest.approx({"r": 0, "t": 1, "d": 0, "l": 0})


def test_shapley_weights_hand():
    # v(S) = 1 if l in S and |S| >= 2 (others symmetric). phi_l: sum over S without l of
    # w(|S|)[v(S+l) - v(S)] = 3 * (1! 2!/4!) + 3 * (2! 1!/4!) + 1 * (3! 0!/4!) = 3/12 + 3/12 + 6/24 = 0.75
    res = SH.shapley(game(lambda x: float(x["l"] and sum(x.values()) >= 2)))
    assert res.phi["l"] == pytest.approx(0.75, abs=1e-15)
    assert res.phi["r"] == pytest.approx(0.25 / 3, abs=1e-15)


cell_values = st.lists(st.floats(-1, 1, allow_nan=False), min_size=16, max_size=16)


@settings(max_examples=100, deadline=None)
@given(cell_values)
def test_shapley_efficiency_property(vals):
    cells = dict(zip(SH.all_keys(), vals))
    res = SH.shapley(cells)
    assert abs(res.g0 + sum(res.phi.values()) - res.residual) <= 1e-12
    for order in (res.seq_labels_first, res.seq_readout_first):
        assert abs(res.g0 + sum(order.values()) - res.residual) <= 1e-12


@settings(max_examples=100, deadline=None)
@given(st.lists(st.floats(-1, 1, allow_nan=False), min_size=12, max_size=12))
def test_shapley_symmetry_and_dummy_property(vals):
    # d is a dummy (payoff ignores it); r and t are symmetric (payoff depends on r + t)
    table = {(rt, l): v for (rt, l), v in zip([(a, b) for a in range(3) for b in range(2)], vals)}
    res = SH.shapley(game(lambda x: table[(x["r"] + x["t"], x["l"])]))
    assert abs(res.phi["d"]) <= 1e-12
    assert abs(res.phi["r"] - res.phi["t"]) <= 1e-12
    assert all(abs(res.interactions[k]) <= 1e-12 for k in ("rd", "td", "dl"))


def test_readout_change_split_hand():
    # V1 chain t=0 cell at (1,1,1) "1011" = 0.30; V2 chain "1011" = 0.20; t=1 "1111" = 0.05
    # format = 0.20 - 0.30 = -0.10; training = 0.05 - 0.20 = -0.15; total = -0.25
    c1 = {k: 0.0 for k in SH.all_keys()}
    c2 = dict(c1)
    c1["1011"], c2["1011"], c1["1111"], c2["1111"] = 0.30, 0.20, 0.05, 0.05
    sp = SH.readout_change_split(c1, c2, (1, 1, 1))
    assert float(sp["format"]) == pytest.approx(-0.10) and float(sp["training"]) == pytest.approx(-0.15)
    assert float(sp["total"]) == pytest.approx(-0.25)
    c2["1111"] = 0.06
    with pytest.raises(ValueError):
        SH.readout_change_split(c1, c2, (1, 1, 1))


# ---------------------------------------------------------------------------------------------------
# Gap cells
# ---------------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def inp():
    return make_inputs(0, n_problems=40)


def test_cells_match_direct_and_r_is_null_at_d1(inp):
    out = G.discrimination_cells(inp)
    cells = out["cells"]
    for key in SH.all_keys():
        r, t, d, l = map(int, key)
        suite = inp.suites[l]
        role, fit = G.stated_name(r, t, l, inp.suites)
        sp = G.scored(inp, inp.probe[suite], suite)
        ssd = G.scored(inp, G._scores_for(inp, role, fit), suite)
        f = M.within_problem_auroc if d else M.auroc_pooled
        assert cells[key] == pytest.approx(f(sp) - f(ssd), abs=1e-12)
    for t in "01":
        for l in "01":
            assert cells[f"0{t}1{l}"] == cells[f"1{t}1{l}"]
    res = SH.shapley(cells)
    # r enters labels-first last; at d = 1 its sequential term is exactly zero
    assert res.seq_labels_first["r"] == 0.0


def test_cell_replicates_match_weighted_direct(inp):
    d = draw([str(i) for i in range(40)], b=6, seed=4)
    rep = G.discrimination_cells(inp, d.counts)["cells"]
    for b in range(6):
        w = d.counts[b].astype(float)[inp.problem_index]
        sp = G.scored(inp, inp.probe["E"], "E")
        st_ = G.scored(inp, inp.trained_iso["E"], "E")
        want = M.within_problem_auroc(sp, w, n_problems=40) - M.within_problem_auroc(st_, w, n_problems=40)
        assert rep["1111"][b] == pytest.approx(want, abs=1e-12)


def test_secondary_sign_convention(inp):
    sec = G.secondary_cells(inp, "brier")
    sp = G.scored(inp, inp.probe["O"], "O")
    sz = G.scored(inp, inp.zero_shot, "O")
    # stated minus probe
    assert sec["cells"]["0000"] == pytest.approx(M.brier(sz) - M.brier(sp), abs=1e-14)
    se = G.scored(inp, inp.trained_iso["E"], "E")
    pe = G.scored(inp, inp.probe["E"], "E")
    assert sec["cells"]["1111"] == pytest.approx(M.demeaned_brier(se) - M.demeaned_brier(pe), abs=1e-14)
    d = draw([str(i) for i in range(40)], b=3, seed=2)
    rep = G.secondary_cells(inp, "ece_debiased_equal_mass", d.counts)
    from analysis.calibration import ece_debiased_equal_mass
    w = d.counts[1].astype(float)[inp.problem_index]
    want = ece_debiased_equal_mass(sz, weights=w) - ece_debiased_equal_mass(sp, weights=w)
    assert rep["cells"]["0000"][1] == pytest.approx(want, abs=1e-12)


def test_per_seed_residual_iso_equality(inp):
    pt, _ = G.per_seed_residual(inp.problem_index, 40, inp.labels["E"], inp.probe["E"], inp.trained["E"],
                                inp.trained_iso["E"])
    assert pt == pytest.approx(G.discrimination_cells(inp)["cells"]["1111"], abs=1e-15)
    bad = G.Scores(rank_score=-inp.trained["E"].rank_score, rank_tiebreak=inp.trained["E"].rank_tiebreak,
                   prob=inp.trained["E"].prob)
    with pytest.raises(AssertionError):
        G.per_seed_residual(inp.problem_index, 40, inp.labels["E"], inp.probe["E"], inp.trained["E"], bad)


def test_l_and_d_diagnostics_consistent(inp):
    ld = G.l_diagnostics(inp)
    cells = G.discrimination_cells(inp)["cells"]
    assert ld["gamma_1110"] == pytest.approx(cells["1110"]) and ld["gamma_1111"] == pytest.approx(cells["1111"])
    assert ld["refit_step"] + ld["relabel_step"] == pytest.approx(cells["1111"] - cells["1110"])
    c = ld["counts"]
    assert c["mixed_l1"] - c["mixed_l0"] == c["entering"] - c["leaving"]
    dd = G.d_diagnostics(inp)
    assert dd["00x0"]["pooled"] == pytest.approx(cells["0000"]) and dd["00x0"]["within"] == pytest.approx(cells["0010"])


def test_model_budget_and_pooling_runs(inp):
    d = draw([str(i) for i in range(40)], b=20, seed=3)
    rep, store = model_budget(inp, d.counts, v2_chain(inp))
    sh = rep["discrimination"]["shapley"]
    assert abs(sh["efficiency_gap"]) <= 1e-12
    iv = rep["discrimination"]["term_intervals"]["phi_t"]
    assert set(iv) == {"0.95", "0.9875"}
    assert iv["0.9875"]["lo"] <= iv["0.95"]["lo"]
    assert "full_rdl_111" in rep["readout_change_split"]
    pb = pooled_budget({"a": store, "b": store})
    assert pb["shapley"]["phi"]["t"] == pytest.approx(sh["phi"]["t"])
    assert pb["heterogeneity"]["phi_t"]["tau2_hat"] == 0.0


# ---------------------------------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------------------------------
def test_best_of_k_hand():
    # problem 0: fail 0.9, pass 0.5 -> selects the fail: 0
    # problem 1: pass 0.3, fail 0.3 (tie at the top) -> 0.5
    # selected 0.25; random (0.5 + 0.5)/2 = 0.5; oracle 1; regret 0.75
    s = make_scored_set([0, 0, 1, 1], [0, 1, 1, 0], [0.9, 0.5, 0.3, 0.3])
    r = RT.best_of_k(s)
    assert r == pytest.approx({"selected": 0.25, "random": 0.5, "oracle": 1.0, "regret": 0.75, "regret_random": 0.5})


def test_triage_hand():
    # ascending keys: {0.3 pass, 0.3 fail} tie group, 0.5 pass, 0.9 fail; n = 4, n_fail = 2
    # b = 0.5: budget 2 takes the whole tie group: 1 failure of 2 -> 0.5; oracle min(1, 2/2) = 1
    # b = 0.25: budget 1, half of the tie group: 0.5 failures -> 0.25; oracle 0.5
    s = make_scored_set([0, 0, 1, 1], [1, 0, 1, 0], [0.3, 0.3, 0.5, 0.9])
    r = RT.triage(s, (0.25, 0.5))
    assert r["0.5"]["achieved"] == pytest.approx(0.5) and r["0.5"]["oracle"] == 1.0
    assert r["0.25"]["achieved"] == pytest.approx(0.25) and r["0.25"]["oracle"] == pytest.approx(0.5)
    assert r["0.25"]["regret"] == pytest.approx(0.25) and r["0.25"]["random"] == 0.25


def test_routing_batch_matches_weighted(inp):
    d = draw([str(i) for i in range(40)], b=5, seed=9)
    s = G.scored(inp, inp.probe["E"], "E")
    tb = RT.triage_batch(s, d.counts, 40)
    bb = RT.best_of_k_batch(s, d.counts, 40)
    for b in range(5):
        w = d.counts[b].astype(float)[inp.problem_index]
        t1 = RT.triage(s, weights=w)
        b1 = RT.best_of_k(s, weights=w, n_problems=40)
        for frac in t1:
            assert tb[frac]["achieved"][b] == pytest.approx(t1[frac]["achieved"], abs=1e-12)
        assert bb["regret"][b] == pytest.approx(b1["regret"], abs=1e-12)


def test_routing_game_efficiency(inp):
    rc = RT.routing_cells(inp)
    for g in rc["games"].values():
        res = SH.shapley(g["cells"])
        assert abs(res.efficiency_gap) <= 1e-12
        # r is a null player for best-of-k with the tie rule
        assert g["cells"]["0111"] == g["cells"]["1111"]


# ---------------------------------------------------------------------------------------------------
# Generation shift
# ---------------------------------------------------------------------------------------------------
def test_generation_shift_identical_sets_give_zero(inp):
    gs = GenSet(problem_index=inp.problem_index, labels=inp.labels, probe=inp.probe, sr=inp.trained,
                extraction_failed=np.zeros(inp.problem_index.size, bool))
    out = contrasts(gs, gs, 40)
    for v in out.values():
        assert v["delta_gamma_g"][0] == pytest.approx(0.0, abs=1e-15)
        assert v["probe_shift"][0] == pytest.approx(0.0, abs=1e-15)
        assert v["cross_contrast"][0] == pytest.approx(v["gamma_g0"][0], abs=1e-15)
    rates = set_rates(gs, 40)
    assert rates["pass_rate_E"][0] == pytest.approx(np.mean(inp.labels["E"]))
    assert rates["extraction_failure_rate"][0] == 0.0
