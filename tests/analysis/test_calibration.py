"""Calibration estimators: hand cases and reference cross-checks."""

import numpy as np
import pytest

from analysis import calibration as C
from analysis._common import make_scored_set
from analysis.bootstrap import draw


def ss(y, p, pi=None):
    pi = np.zeros(len(y), int) if pi is None else pi
    return make_scored_set(pi, y, p)


def test_equal_mass_bins_ties_share_a_bin():
    # sorted [0.1, 0.2, 0.2, 0.2, 0.9, 0.9], 2 parts of 3 -> boundary (0.2 + 0.2)/2 = 0.2, and all
    # three 0.2 values go left (searchsorted "left")
    idx = C.equal_mass_bin_index(np.array([0.2, 0.9, 0.1, 0.2, 0.9, 0.2]), None, 2)
    assert idx.tolist() == [0, 1, 0, 0, 1, 0]


def test_debiased_ece_hand():
    # bins {0.1, 0.2} (ybar 0.5) and {0.7, 0.9} (ybar 1):
    # bin 1: (0.15 - 0.5)^2 - 0.5 * 0.5 / 1 = -0.1275; bin 2: (0.8 - 1)^2 - 0 = 0.04
    # CE2 = 0.5 * -0.1275 + 0.5 * 0.04 = -0.04375 -> reported sqrt(max(0, .)) = 0
    s = ss([0, 1, 1, 1], [0.1, 0.2, 0.7, 0.9])
    assert C.ece_debiased_squared(s, 2) == pytest.approx(-0.04375, abs=1e-15)
    assert C.ece_debiased_equal_mass(s, 2) == 0.0
    # second case: bins {0.1, 0.1} y (0, 0) and {0.9, 0.9} y (0, 1)
    # bin 1: 0.01 - 0; bin 2: (0.9 - 0.5)^2 - 0.25 = -0.09 -> CE2 = 0.5 * 0.01 + 0.5 * -0.09 = -0.04
    s2 = ss([0, 0, 0, 1], [0.1, 0.1, 0.9, 0.9])
    assert C.ece_debiased_squared(s2, 2) == pytest.approx(-0.04, abs=1e-15)
    # third: bins {0.1, 0.1} y (1, 1) -> 0.81; {0.9, 0.9} y (0, 0) -> 0.81; CE2 = 0.81 -> 0.9
    s3 = ss([1, 1, 0, 0], [0.1, 0.1, 0.9, 0.9])
    assert C.ece_debiased_equal_mass(s3, 2) == pytest.approx(0.9, abs=1e-15)


def test_ks_hand():
    # sorted groups: 0.2 (y 0): -0.2; 0.6 (y 1, y 0): +0.4 - 0.6 = -0.2 -> cum -0.4; 0.9 (y 1): +0.1 -> -0.3
    # KS = 0.4 / 4 = 0.1
    s = ss([0, 1, 0, 1], [0.2, 0.6, 0.6, 0.9])
    assert C.ks_calibration_error(s) == pytest.approx(0.1, abs=1e-15)


def test_equal_width_hand():
    # 10 bins: bin 0 {0.05, y 0}: 0.05; bin 1 {0.15, y 1}: 0.85; bin 9 {0.95, 1.0, y 1, 1}: 0.025
    # ECE = 0.25 * 0.05 + 0.25 * 0.85 + 0.5 * 0.025 = 0.2375
    s = ss([0, 1, 1, 1], [0.05, 0.15, 0.95, 1.0])
    assert C.ece_equal_width(s, 10) == pytest.approx(0.2375, abs=1e-15)


def test_reference_cross_check_values():
    # Values observed by running the reference packages on the same data (build log, step 5):
    # relplot smECE (apple/ml-calibration aae71be7) and verified_calibration
    # lower_bound_scaling_ce(p=2, debias=True, num_bins=15) (p-lambda, ee81c346).
    rng = np.random.default_rng(0)
    f = rng.beta(2, 2, 50)
    y = (rng.uniform(size=50) < f ** 1.5).astype(int)
    s = ss(y, f)
    assert C.smooth_ece(s) == pytest.approx(0.134972778596420, abs=1e-14)
    assert C.ece_debiased_equal_mass(s) == pytest.approx(0.146900589191708, abs=1e-14)


def test_smooth_ece_perfectly_calibrated_is_small_and_bandwidth_fixed_point():
    rng = np.random.default_rng(1)
    f = rng.uniform(size=4000)
    y = (rng.uniform(size=4000) < f).astype(int)
    v, sigma = C.smooth_ece(ss(y, f), return_bandwidth=True)
    assert v < 0.03
    # fixed point: sigma >= smECE_sigma (the bisection keeps the "not too small" end)
    assert sigma >= C.smooth_ece_at(f, y, sigma) or sigma < C.SMECE_EPS


def test_smooth_ece_batch_equals_scalar():
    rng = np.random.default_rng(3)
    n_p, k = 40, 5
    pi = np.repeat(np.arange(n_p), k)
    f = rng.beta(2, 2, pi.size)
    y = (rng.uniform(size=pi.size) < f ** 1.3).astype(int)
    s = ss(y, f, pi)
    d = draw([str(i) for i in range(n_p)], b=30, seed=1)
    batch = C.smooth_ece_batch(f, y, pi, d.counts, n_p)
    scalar = [C.smooth_ece(s, weights=d.counts[i].astype(float)[pi]) for i in range(30)]
    assert np.max(np.abs(batch - np.array(scalar))) < 1e-12
