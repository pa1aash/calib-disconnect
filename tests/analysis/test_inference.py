"""Bootstrap, refit widening, decisions, Holm, heterogeneity, k rule, and reconciliation."""

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from scipy.stats import norm

from analysis import bootstrap as B
from analysis import decisions as D
from analysis import refit as RF
from analysis._common import make_scored_set
from analysis.krule import k_from_mean, k_rule, k_rule_report
from analysis.metrics import auroc_pooled, within_problem_auroc
from analysis.reconciliation import classify, make_check, paper_verb
from pipeline.contracts.constants import BOOTSTRAP_SEED, PRIMARY_MODELS, T12_QUANTILE


# ---------------------------------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------------------------------
def test_draw_determinism_and_shape():
    ids = [f"p{i}" for i in range(17)]
    a, b = B.draw(ids, 50), B.draw(ids, 50)
    assert a.seed == BOOTSTRAP_SEED and a.counts.dtype == np.uint16
    assert np.array_equal(a.counts, b.counts)
    assert np.all(a.counts.sum(axis=1) == 17)
    assert not np.array_equal(a.counts, B.draw(ids, 50, seed=1).counts)
    with pytest.raises(ValueError):
        B.draw(["a", "a"], 5)


@settings(max_examples=20, deadline=None)
@given(st.integers(1, 30), st.integers(1, 40), st.integers(0, 2**31))
def test_draw_determinism_property(n, b, seed):
    ids = [str(i) for i in range(n)]
    assert np.array_equal(B.draw(ids, b, seed).counts, B.draw(ids, b, seed).counts)


def test_pairing_same_draws_across_statistics():
    rng = np.random.default_rng(2)
    pi = np.repeat(np.arange(12), 4)
    y = (rng.uniform(size=pi.size) < 0.5).astype(int)
    s1 = make_scored_set(pi, y, rng.normal(size=pi.size))
    s2 = make_scored_set(pi, y, rng.normal(size=pi.size))
    d = B.draw([str(i) for i in range(12)], 40)
    r1 = B.replicate(lambda w: auroc_pooled(s1, w), d, pi)
    r2 = B.replicate(lambda w: auroc_pooled(s2, w), d, pi)
    rd = B.replicate(lambda w: _diff(s1, s2, w), d, pi)
    # the replicate of a paired difference is the difference of replicates on the same draws
    ok = np.isfinite(rd)
    assert np.allclose(rd[ok], (r1 - r2)[ok], atol=1e-14)


def _diff(a, b, w):
    x, y = auroc_pooled(a, w), auroc_pooled(b, w)
    return None if x is None or y is None else x - y


def test_replicate_marks_undefined():
    d = np.array([[1, 0], [0, 1]])
    out = B.replicate(lambda c: None if c[0] == 0 else 1.0, d)
    assert np.isnan(out[1]) and out[0] == 1.0


def test_percentile_interval_hand_and_undefined_rule():
    reps = np.arange(101, dtype=float)       # quantiles 0.05 and 0.95 with linear method: 5 and 95
    iv = B.percentile_interval(50.0, reps, 0.90)
    # (1 - 0.9)/2 is 0.04999... in floating point, so compare to 1e-12
    assert iv.lo == pytest.approx(5.0, abs=1e-12) and iv.hi == pytest.approx(95.0, abs=1e-12)
    assert (iv.n_undefined, iv.unavailable) == (0, False)
    r = np.linspace(0, 1, 1000)
    r10 = r.copy()
    r10[:10] = np.nan                          # exactly 1 percent undefined: dropped, still available
    iv10 = B.percentile_interval(0.5, r10, 0.95)
    assert iv10.n_undefined == 10 and not iv10.unavailable
    assert iv10.lo == pytest.approx(np.quantile(r[10:], 0.025))
    r11 = r.copy()
    r11[:11] = np.nan                          # more than 1 percent: unavailable
    iv11 = B.percentile_interval(0.5, r11, 0.95)
    assert iv11.unavailable and iv11.n_undefined == 11 and np.isnan(iv11.lo)
    assert B.percentile_interval(None, r, 0.95).unavailable


@settings(max_examples=40, deadline=None)
@given(st.integers(100, 400), st.integers(0, 20))
def test_undefined_rule_property(n, k):
    r = np.linspace(0, 1, n)
    k = min(k, n - 1)
    r[:k] = np.nan
    iv = B.percentile_interval(0.5, r, 0.9)
    assert iv.n_undefined == k
    assert iv.unavailable == (k > 0.01 * n)


def test_bca_reduces_to_percentile_when_symmetric():
    # point at the median of symmetric replicates (z0 = 0) and a symmetric jackknife (a = 0)
    reps = norm.ppf((np.arange(2000) + 0.5) / 2000)
    jk = np.array([-1.0, 1.0, -2.0, 2.0])
    iv = B.bca_interval(0.0, reps, jk, 0.9)
    pc = B.percentile_interval(0.0, reps, 0.9)
    assert iv.lo == pytest.approx(pc.lo, abs=1e-12) and iv.hi == pytest.approx(pc.hi, abs=1e-12)


# ---------------------------------------------------------------------------------------------------
# Refit widening and decisions
# ---------------------------------------------------------------------------------------------------
def test_refit_widening_hand():
    # every model's seeds 0, 0.01, 0.02: sigma2 = var(ddof 1) = 0.0001
    # s2_refit = (1/3)(1/36)(6 * 0.0001) = 5.5556e-6
    per = {m: [0.0, 0.01, 0.02] for m in PRIMARY_MODELS}
    s2 = RF.s2_refit(RF.between_seed_variance(per))
    assert s2 == pytest.approx(0.0001 / 18, rel=1e-12)
    # replicates linspace(-0.01, 0.01, 1001): 90 percent interval (-0.009, 0.009), h = 0.009
    reps = np.linspace(-0.01, 0.01, 1001)
    d = D.decide(0.01, reps, per, delta=0.03)
    assert d.unwidened[0] == pytest.approx(-0.009, abs=1e-15) and d.unwidened[1] == pytest.approx(0.009, abs=1e-15)
    assert d.h == pytest.approx(0.009, abs=1e-15) and d.t_quantile == T12_QUANTILE
    # half = sqrt(0.009^2 + (1.782^2)(0.0001/18)) = sqrt(8.1e-5 + 1.7641800e-5) = 0.0099318...
    half = np.sqrt(8.1e-5 + 1.782 ** 2 * 0.0001 / 18)
    assert half == pytest.approx(0.00993186, abs=1e-8)
    assert d.widened[0] == pytest.approx(-half, abs=1e-15) and d.widened[1] == pytest.approx(half, abs=1e-15)
    assert d.decision == "D1" and not d.conventional_positive and not d.conventional_negative


def test_decision_rules_hand():
    assert D.classify_interval(-0.02, 0.02, 0.03) == "D1"
    assert D.classify_interval(0.031, 0.05, 0.03) == "D2"
    assert D.classify_interval(-0.05, -0.031, 0.03) == "D3"
    assert D.classify_interval(-0.03, 0.02, 0.03) == "inconclusive"   # -delta < L is strict
    assert D.classify_interval(0.03, 0.05, 0.03) == "inconclusive"    # L > delta is strict
    assert D.classify_interval(0.01, 0.05, 0.03) == "inconclusive"


@settings(max_examples=200, deadline=None)
@given(st.floats(-1, 1), st.floats(0, 1), st.sampled_from([0.02, 0.03, 0.05]))
def test_decisions_mutually_exclusive(lo, width, delta):
    hi = lo + width
    dec = D.classify_interval(lo, hi, delta)
    reached = [-delta < lo and hi < delta, lo > delta, hi < -delta]
    assert sum(reached) <= 1
    assert dec == (["D1", "D2", "D3"][reached.index(True)] if any(reached) else "inconclusive")


def _grid_reps(mu, sd, n=100_000):
    return mu + sd * norm.ppf((np.arange(n) + 0.5) / n)


def test_holm_step_down_hand():
    # D2 at delta 0.03, no refit component. Lower bound at level a is mu + sd z_a.
    # Model B: mu 0.0536, sd 0.01: at a = 0.05/6, L = 0.0536 - 0.02394 = 0.02966 < 0.03 (not rejected);
    # at a = 0.05/5 = 0.01, L = 0.0536 - 0.02326 = 0.03034 > 0.03 (rejected).
    # Model A: mu 0.2 rejected at step 1, which lets B be tested at 0.05/5.
    reps = {m: _grid_reps(0.0, 0.01) for m in PRIMARY_MODELS}
    reps["P1"] = _grid_reps(0.2, 0.01)
    reps["P2"] = _grid_reps(0.0536, 0.01)
    out = D.holm_per_model(reps, 0.0, 12, delta=0.03)
    assert out["P1"]["D2"] and out["P2"]["D2"]
    assert out["P1"]["level"]["D2"] == pytest.approx(0.05 / 6)
    assert out["P2"]["level"]["D2"] == pytest.approx(0.05 / 5)
    assert not any(out[m]["D2"] for m in ("P3", "P4", "P5", "P6"))
    # every other model is within the margin at every Holm level: D1 for all of them
    assert all(out[m]["D1"] for m in ("P3", "P4", "P5", "P6"))
    # without model A, B is tested only at 0.05/6 and is not rejected
    reps["P1"] = _grid_reps(0.0, 0.01)
    out2 = D.holm_per_model(reps, 0.0, 12, delta=0.03)
    assert not out2["P2"]["D2"]


def test_heterogeneity_hand():
    # points alternate +-0.1: Var_m (ddof 1) = 6 * 0.01 / 5 = 0.012
    # replicates point + (-0.01, 0.01): bootstrap variance (ddof 1) = 2 * 0.0001 = 0.0002
    # tau2 = 0.012 - 0.0002 = 0.0118
    pts = {m: (0.1 if i % 2 == 0 else -0.1) for i, m in enumerate(PRIMARY_MODELS)}
    reps = {m: pts[m] + np.array([-0.01, 0.01]) for m in PRIMARY_MODELS}
    h = D.heterogeneity(pts, reps)
    assert h["var_between"] == pytest.approx(0.012, abs=1e-15)
    assert h["mean_boot_var"] == pytest.approx(0.0002, abs=1e-15)
    assert h["tau2_hat"] == pytest.approx(0.0118, abs=1e-15)
    fire = D.heterogeneity_fires(h["tau_hat"], {"a": {"above": True}, "b": {"below": False}}, 0.03)
    assert fire["fires"] and fire["tau_exceeds_delta"] and not fire["sign_disagreement"]
    sign = D.heterogeneity_fires(0.0, {"a": {"above": True}, "b": {"below": True}}, 0.03)
    assert sign["fires"] and sign["sign_disagreement"]
    fam = D.family_means(pts, reps)
    assert fam["qwen3"]["point"] == pytest.approx(0.0)


def test_primary_report_and_k4():
    rng = np.random.default_rng(0)
    per = {m: [0.0, 0.002, -0.002] for m in PRIMARY_MODELS}
    per["P6"] = [0.3, 0.3, 0.3]
    reps = {m: [np.mean(v) + rng.normal(0, 0.003, 400) for _ in range(3)] for m, v in per.items()}
    rep = D.primary_report(per, reps, flagged={"P6": True})
    # R_bar = 0.3 / 6 = 0.05 driven by P6
    assert rep["r_bar"] == pytest.approx(0.05)
    assert rep["decision"]["decision"] == "D2"
    k4 = rep["k4_sensitivity"]
    assert k4["flagged"] == ["P6"] and k4["decision"]["decision"] == "D1"
    assert k4["decision_only_through_flagged"] is True
    assert rep["per_model_counts"]["above"] == 1


# ---------------------------------------------------------------------------------------------------
# k rule
# ---------------------------------------------------------------------------------------------------
def test_k_rule_boundary():
    assert k_from_mean(184.99) == 20 and k_from_mean(185) == 10
    r = k_rule({m: 184.99 for m in PRIMARY_MODELS})
    assert r.k == 20 and r.m_bar == pytest.approx(184.99)
    assert k_rule({m: 185 for m in PRIMARY_MODELS}).k == 10
    # mean of (180, 190, 185, 185, 185, 184) = 1109/6 = 184.83 -> 20
    vals = dict(zip(PRIMARY_MODELS, (180, 190, 185, 185, 185, 184)))
    assert k_rule(vals).k == 20
    with pytest.raises(ValueError):
        k_rule({"P1": 200})
    r20 = k_rule({m: 100 for m in PRIMARY_MODELS}, m_bar_k20=124.9)
    assert r20.below_t20 is True
    with pytest.raises(ValueError):
        k_rule({m: 300 for m in PRIMARY_MODELS}, m_bar_k20=124.9)
    rep = k_rule_report({m: 190 for m in PRIMARY_MODELS}, {m: 5 for m in PRIMARY_MODELS},
                        {m: {0: 1, 3: 2} for m in PRIMARY_MODELS})
    assert rep["k"] == 10 and rep["pass_count_histograms"]["P1"] == {"0": 1, "3": 2}


# ---------------------------------------------------------------------------------------------------
# Reconciliation
# ---------------------------------------------------------------------------------------------------
def test_classify_boundaries():
    assert classify("ordering", (0.001, 0.2), 1) == "consistent"
    assert classify("ordering", (0.0, 0.2), 1) == "undetermined"
    assert classify("ordering", (-0.2, -0.001), 1) == "not_consistent"
    assert classify("ordering", (-0.2, -0.001), -1) == "consistent"
    assert classify("ordering", (0.001, 0.2), -1) == "not_consistent"
    assert classify("tie", (-0.029, 0.029), tie_width=0.03) == "consistent"
    assert classify("tie", (-0.03, 0.01), tie_width=0.03) == "undetermined"
    assert classify("tie", (0.03, 0.05), tie_width=0.03) == "not_consistent"
    assert classify("tie", (-0.05, -0.03), tie_width=0.03) == "not_consistent"
    assert classify("tie", (0.02, 0.04), tie_width=0.03) == "undetermined"
    assert classify("above_value", (0.01, 0.1), 1) == "consistent"
    assert classify("ordering", (np.nan, np.nan), 1) == "undetermined"
    with pytest.raises(ValueError):
        classify("tie", (0, 1))


@settings(max_examples=200, deadline=None)
@given(st.floats(-0.5, 0.5), st.floats(0, 0.5), st.floats(0.005, 0.1))
def test_classify_tie_property(lo, width, w):
    hi = lo + width
    out = classify("tie", (lo, hi), tie_width=w)
    inside = -w < lo and hi < w
    outside = hi <= -w or lo >= w
    assert out == ("consistent" if inside else "not_consistent" if outside else "undetermined")


def test_paper_verb():
    assert paper_verb(["consistent", "consistent"])[0] == "consistent"
    assert paper_verb(["consistent", "not_consistent"])[0] == "not consistent"
    v, c = paper_verb(["consistent", "undetermined", "consistent"])
    assert v == "partly consistent" and c == {"n": 3, "consistent": 2, "not_consistent": 0, "undetermined": 1}
    chk = make_check("c1", "campos", None, "X1", "tie", 0, 0.03, 0.01, (-0.01, 0.02), (-0.04, 0.0))
    assert chk.outcome == "consistent" and chk.diagnostic_excluding_truncation == "undetermined"


def test_within_problem_auroc_used_for_above_value():
    s = make_scored_set([0, 0, 0], [1, 0, 0], [0.9, 0.1, 0.2])
    assert within_problem_auroc(s) == 1.0
