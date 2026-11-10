"""Section 8 metrics: hand-computed cases, invariances, and weighted-equals-duplicated checks."""

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from analysis import metrics as M
from analysis._common import make_scored_set
from analysis.ranking import lex_keys


def ss(pi, y, score, tb=None, prob=None):
    return make_scored_set(pi, y, score, tb, prob)


# ---------------------------------------------------------------------------------------------------
# Ranking
# ---------------------------------------------------------------------------------------------------
def test_lex_keys_hand():
    # pairs (score, tiebreak): (1, 2), (1, 1), (0, 5), (1, 2) -> order (0,5) < (1,1) < (1,2) = (1,2)
    k = lex_keys(np.array([1.0, 1.0, 0.0, 1.0]), np.array([2.0, 1.0, 5.0, 2.0]))
    assert k.tolist() == [2, 1, 0, 2]
    # all-NaN tie-break means no tie-break
    k2 = lex_keys(np.array([1.0, 1.0, 0.0]), np.full(3, np.nan))
    assert k2.tolist() == [1, 1, 0]
    with pytest.raises(ValueError):
        lex_keys(np.array([1.0, 1.0]), np.array([np.nan, 1.0]))


def test_equal_score_different_tiebreak_not_a_tie():
    # pass (0.5, tb 2), fail (0.5, tb 1): pass ranks above -> AUROC 1; without tie-break a tie -> 0.5
    s = ss([0, 0], [1, 0], [0.5, 0.5], [2.0, 1.0])
    assert M.auroc_pooled(s) == 1.0
    assert M.auroc_pooled(s, use_tiebreak=False) == 0.5
    assert M.tie_rate_within(s) == 0.0
    assert M.tie_rate_within(s, use_tiebreak=False) == 1.0


# ---------------------------------------------------------------------------------------------------
# Hand cases
# ---------------------------------------------------------------------------------------------------
def test_auroc_pooled_hand():
    # pos {0.9, 0.5}, neg {0.5, 0.1}: pairs 1 + 1 + 0.5 + 1 = 3.5 of 4 -> 0.875
    s = ss([0, 0, 1, 1], [1, 0, 1, 0], [0.9, 0.5, 0.5, 0.1])
    assert M.auroc_pooled(s) == pytest.approx(0.875, abs=1e-15)
    assert M.auroc_pooled(ss([0, 1], [1, 1], [0.1, 0.2])) is None


W_CASE = dict(
    # problem 0: pass {0.8}, fail {0.3, 0.8}       -> A = 1 + 0.5 = 1.5, pairs 2 (one tie)
    # problem 1: pass {0.2, 0.6, 0.7}, fail {0.4}  -> A = 0 + 1 + 1 = 2,  pairs 3
    # problem 2: all pass {0.1, 0.9}               -> drops out
    pi=[0, 0, 0, 1, 1, 1, 1, 2, 2],
    y=[1, 0, 0, 1, 1, 1, 0, 1, 1],
    s=[0.8, 0.3, 0.8, 0.2, 0.6, 0.7, 0.4, 0.1, 0.9],
)


def test_within_problem_auroc_hand():
    s = ss(W_CASE["pi"], W_CASE["y"], W_CASE["s"])
    # W = (1.5 + 2) / (2 + 3) = 0.7
    assert M.within_problem_auroc(s) == pytest.approx(0.7, abs=1e-15)
    # W_avg = (1.5/2 + 2/3) / 2 = 0.708333...
    assert M.within_problem_auroc_avg(s) == pytest.approx((0.75 + 2 / 3) / 2, abs=1e-15)
    # tie rate within: 1 tied pair of 5
    assert M.tie_rate_within(s) == pytest.approx(0.2, abs=1e-15)
    assert M.mixed_counts(s) == {"n_samples": 9, "n_problems": 3, "mixed": 2, "all_pass": 1,
                                 "all_fail": 0, "pass_fail_pairs": 5}
    assert M.pass_count_histogram(s) == {1: 1, 2: 1, 3: 1}
    assert M.within_problem_auroc(ss([0, 0, 1], [1, 1, 0], [0.1, 0.2, 0.3])) is None


def test_auprc_hand():
    # descending: 0.9 pass, 0.8 fail, 0.7 pass, 0.1 fail; P = 2
    # AP(pass) = 0.5 * 1 + 0.5 * 2/3 = 0.83333...
    # ascending for fail: 0.1 fail (prec 1), 0.7 pass, 0.8 fail (prec 2/3) -> 0.83333...
    s = ss([0, 1, 2, 3], [1, 0, 1, 0], [0.9, 0.8, 0.7, 0.1])
    assert M.auprc(s, 1) == pytest.approx(0.5 + 1 / 3, abs=1e-15)
    assert M.auprc(s, 0) == pytest.approx(0.5 + 1 / 3, abs=1e-15)
    assert M.base_rate(s, 1) == 0.5
    # tie between a pass and a fail at the top: both enter together, precision 1/2, recall 1/1
    assert M.auprc(ss([0, 1], [1, 0], [0.5, 0.5]), 1) == pytest.approx(0.5)


def test_brier_and_murphy_hand():
    # probs 0.1, 0.2, 0.7, 0.9; y 0, 1, 1, 1; two equal-mass bins {0.1, 0.2} and {0.7, 0.9}
    s = ss([0, 1, 2, 3], [0, 1, 1, 1], [0.1, 0.2, 0.7, 0.9])
    # BS = (0.01 + 0.64 + 0.09 + 0.01) / 4 = 0.1875
    assert M.brier(s) == pytest.approx(0.1875, abs=1e-15)
    d = M.murphy(s, n_bins=2)
    # REL = 0.5 (0.15 - 0.5)^2 + 0.5 (0.8 - 1)^2 = 0.08125
    # RES = 0.5 (0.5 - 0.75)^2 + 0.5 (1 - 0.75)^2 = 0.0625; UNC = 0.75 * 0.25 = 0.1875
    # WBV = (0.0025 * 2 + 0.01 * 2) / 4 = 0.00625; WBC = ((-0.05)(-0.5) + (0.05)(0.5)) / 4 = 0.0125
    assert d["reliability"] == pytest.approx(0.08125, abs=1e-15)
    assert d["resolution"] == pytest.approx(0.0625, abs=1e-15)
    assert d["uncertainty"] == pytest.approx(0.1875, abs=1e-15)
    assert d["within_bin_variance"] == pytest.approx(0.00625, abs=1e-15)
    assert d["within_bin_covariance"] == pytest.approx(0.0125, abs=1e-15)
    # identity: 0.08125 - 0.0625 + 0.1875 + 0.00625 - 2 * 0.0125 = 0.1875
    assert abs(d["identity_residual"]) < 1e-15


def test_demeaned_brier_hand():
    # problem 0 mixed: s 0.8, 0.4; y 1, 0; means 0.6, 0.5 -> errors -0.3, 0.3 -> 0.18 over 2 samples
    # problem 1 all pass: excluded
    s = ss([0, 0, 1, 1], [1, 0, 1, 1], [0.8, 0.4, 0.9, 0.2])
    assert M.demeaned_brier(s) == pytest.approx(0.09, abs=1e-15)
    assert M.demeaned_brier(ss([0, 0], [1, 1], [0.1, 0.2])) is None


def test_pass_at_k_hand():
    assert M.pass_at_k(10, 3, 1) == pytest.approx(0.3, abs=1e-15)
    assert M.pass_at_k(10, 3, 10) == 1.0
    # 1 - C(3, 2) / C(5, 2) = 1 - 3/10
    assert M.pass_at_k(5, 2, 2) == pytest.approx(0.7, abs=1e-15)
    assert M.pass_at_k(5, 0, 2) == 0.0


def test_d_diagnostics_hand():
    # problems 0 (mixed), 1 (all fail), 2 (mixed); folds 0, 0, 1
    s = ss([0, 0, 1, 2, 2], [1, 0, 0, 1, 0], [0.9, 0.2, 0.95, 0.3, 0.6])
    # pooled over mixed problems only: pos {0.9, 0.3}, neg {0.2, 0.6}: 1 + 1 + 1 + 0 = 3 of 4
    assert M.auroc_pooled_mixed(s) == pytest.approx(0.75)
    # fold 0: pos {0.9}, neg {0.2, 0.95} -> 1/2; fold 1: pos {0.3}, neg {0.6} -> 0; mean 0.25
    assert M.auroc_fold_averaged(s, np.array([0, 0, 1])) == pytest.approx(0.25)


def test_imputation_tie_share_hand():
    # pos {a: 0.5 imputed, b: 0.9}, neg {c: 0.5 imputed, d: 0.5 not imputed}
    # pooled pairs 4; tied and both imputed: (a, c) -> 1/4
    s = ss([0, 0, 1, 1], [1, 1, 0, 0], [0.5, 0.9, 0.5, 0.5])
    assert M.imputation_tie_share(s, np.array([1, 0, 1, 0], bool)) == pytest.approx(0.25)


# ---------------------------------------------------------------------------------------------------
# Fast path against direct computation
# ---------------------------------------------------------------------------------------------------
def _random_set(rng, n_p=25, k=5, ties=True):
    pi = np.repeat(np.arange(n_p), k)
    score = rng.integers(0, 6, pi.size).astype(float) if ties else rng.normal(size=pi.size)
    y = (rng.uniform(size=pi.size) < 0.5).astype(int)
    return ss(pi, y, score, prob=1 / (1 + np.exp(-score)))


def test_rankstats_matches_direct_weighted():
    rng = np.random.default_rng(5)
    s = _random_set(rng)
    rs = M.RankStats(s, 25)
    counts = rng.multinomial(25, np.full(25, 1 / 25), size=20)
    fold = rng.integers(0, 5, 25)
    pooled, w_, wavg = rs.auroc_pooled(counts), rs.W(counts), rs.W_avg(counts)
    fa = rs.auroc_fold_averaged(fold, counts)
    for b in range(20):
        w = counts[b][s.problem_index].astype(float)
        assert pooled[b] == pytest.approx(M.auroc_pooled(s, w), abs=1e-12)
        assert w_[b] == pytest.approx(M.within_problem_auroc(s, w, n_problems=25), abs=1e-12)
        assert wavg[b] == pytest.approx(M.within_problem_auroc_avg(s, w, n_problems=25), abs=1e-12)
        d = M.auroc_fold_averaged(s, fold, w)
        assert (np.isnan(fa[b]) and d is None) or fa[b] == pytest.approx(d, abs=1e-12)
    assert rs.auroc_pooled()[0] == pytest.approx(M.auroc_pooled(s), abs=1e-14)
    assert np.allclose(rs.A, M.per_problem_counts(s, 25)["A"])


# ---------------------------------------------------------------------------------------------------
# Property-based tests
# ---------------------------------------------------------------------------------------------------
@st.composite
def scored_sets(draw, max_p=6, max_k=5):
    n_p = draw(st.integers(1, max_p))
    k = draw(st.integers(1, max_k))
    pi = np.repeat(np.arange(n_p), k)
    y = np.array(draw(st.lists(st.integers(0, 1), min_size=pi.size, max_size=pi.size)))
    sc = np.array(draw(st.lists(st.integers(-3, 3), min_size=pi.size, max_size=pi.size)), dtype=float)
    mult = np.array(draw(st.lists(st.integers(1, 3), min_size=n_p, max_size=n_p)))
    return pi, y, sc, mult


def duplicate(pi, y, sc, mult):
    """Each problem i copied mult[i] times, every copy a new problem."""
    P, Y, S, nxt = [], [], [], 0
    for i, m in enumerate(mult):
        idx = np.flatnonzero(pi == i)
        for _ in range(m):
            P += [nxt] * idx.size
            Y += list(y[idx])
            S += list(sc[idx])
            nxt += 1
    return np.array(P), np.array(Y), np.array(S, dtype=float)


def _eq(a, b):
    if a is None or b is None:
        return a is None and b is None
    return abs(a - b) <= 1e-12


@settings(max_examples=60, deadline=None)
@given(scored_sets())
def test_weighted_equals_duplicated(data):
    from analysis import calibration as C
    pi, y, sc, mult = data
    prob = (sc + 3.5) / 7.0
    s = ss(pi, y, sc, prob=prob)
    w = mult[pi].astype(float)
    P, Y, S = duplicate(pi, y, sc, mult)
    d = ss(P, Y, S, prob=(S + 3.5) / 7.0)
    assert _eq(M.auroc_pooled(s, w), M.auroc_pooled(d))
    assert _eq(M.within_problem_auroc(s, w), M.within_problem_auroc(d))
    assert _eq(M.within_problem_auroc_avg(s, w), M.within_problem_auroc_avg(d))
    assert _eq(M.auprc(s, 1, w), M.auprc(d, 1))
    assert _eq(M.auprc(s, 0, w), M.auprc(d, 0))
    assert _eq(M.brier(s, w), M.brier(d))
    assert _eq(M.demeaned_brier(s, w), M.demeaned_brier(d))
    assert _eq(M.pass_at_k_mean(s, 1, w), M.pass_at_k_mean(d, 1))
    assert _eq(M.auroc_pooled_mixed(s, w), M.auroc_pooled_mixed(d))
    for key in ("reliability", "resolution", "uncertainty", "brier"):
        assert _eq(M.murphy(s, 15, w)[key], M.murphy(d, 15)[key])
    assert _eq(C.ece_debiased_squared(s, 15, w), C.ece_debiased_squared(d, 15))
    assert _eq(C.ks_calibration_error(s, w), C.ks_calibration_error(d))
    assert _eq(C.ece_equal_width(s, 10, w), C.ece_equal_width(d, 10))
    assert _eq(C.smooth_ece(s, w), C.smooth_ece(d))


@settings(max_examples=60, deadline=None)
@given(scored_sets(), st.sampled_from(["cube", "exp", "affine"]))
def test_auroc_and_W_invariant_to_monotone_transform(data, kind):
    pi, y, sc, _ = data
    f = {"cube": lambda x: x ** 3 + 2 * x, "exp": np.exp, "affine": lambda x: 3 * x - 7}[kind]
    a, b = ss(pi, y, sc), ss(pi, y, f(sc))
    assert _eq(M.auroc_pooled(a), M.auroc_pooled(b))
    assert _eq(M.within_problem_auroc(a), M.within_problem_auroc(b))
    assert _eq(M.within_problem_auroc_avg(a), M.within_problem_auroc_avg(b))


@settings(max_examples=60, deadline=None)
@given(scored_sets(), st.integers(1, 4))
def test_W_invariant_to_monotone_map_with_tie_rule(data, steps):
    # an isotonic-like step map that merges scores; with the pre-map score as tie-break nothing merges
    pi, y, sc, _ = data
    mapped = np.floor((sc + 3) / 7 * steps) / steps
    raw = ss(pi, y, sc)
    iso = ss(pi, y, mapped, tb=sc)
    assert _eq(M.within_problem_auroc(raw), M.within_problem_auroc(iso))
    assert _eq(M.auroc_pooled(raw), M.auroc_pooled(iso))
    assert _eq(M.tie_rate_within(raw), M.tie_rate_within(iso))
