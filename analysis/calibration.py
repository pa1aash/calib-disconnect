"""Calibration estimators (design section 8).

Estimators and exact definitions. In every formula, n is the (weighted) number of samples, s_i the
probability `prob`, y_i the label, and per-sample weights w_i (the bootstrap multiplicity of the
sample's problem) act as integer duplication counts, so a weighted value equals the unweighted value
on the explicitly duplicated data.

1. Equal-mass bins (`equal_mass_bin_index`). The scheme of `get_equal_bins` in the reference code of
   Kumar, Liang, and Ma (2019), github.com/p-lambda/verified_calibration, calibration/utils.py,
   read at commit ee81c346: sort the n probabilities, split the sorted list into B parts with
   numpy.array_split (the first n mod B parts have one more element), put a boundary at the midpoint
   of the last value of a part and the first value of the next, append 1.0, drop duplicate
   boundaries, and assign each probability to the first bin whose boundary is >= it
   (searchsorted, side "left"). Equal probabilities always share a bin. B is reduced to n when
   n < B. With weights, the sorted list is the duplicated list, computed from cumulative weights.

2. Debiased equal-mass ECE (`ece_debiased_equal_mass`), the squared-error (l2) version of Kumar,
   Liang, and Ma (2019), as implemented by `unbiased_square_ce` and `unbiased_l2_ce` in the same
   file. With bins b of size n_b, mean probability sbar_b, and mean label ybar_b:

       CE2_debiased = sum_b (n_b / n) * [ (sbar_b - ybar_b)^2 - ybar_b (1 - ybar_b) / (n_b - 1) ]

   where a bin with n_b < 2 contributes 0, and the reported value is sqrt(max(0, CE2_debiased)).
   The subtracted term is the unbiased estimate of the variance of ybar_b, which removes the upward
   bias of the plug-in squared gap. `ece_debiased_squared` returns CE2_debiased before clipping.

3. Smooth ECE (`smooth_ece`), Blasiok and Nakkiran (2023), implemented from the definition with the
   discretization and bandwidth rule of the authors' package relplot (github.com/apple/ml-calibration,
   src/relplot/metrics.py and kernels.py, commit aae71be7, default configuration):
   residual r_i = s_i - y_i; for bandwidth sigma, the residual mass w_i r_i and the density mass w_i
   are spread linearly onto a uniform grid of G = floor(max(2000, round(20 / sigma)) / 2) + 1
   points on [0, 1], convolved with a Gaussian kernel of standard deviation sigma reflected once at
   0 and at 1, and linearly interpolated at E = max(round(10 / sigma), 200) evaluation points
   t_k = linspace(0, 1, E). With R(t) the smoothed residual mass and D(t) = (smoothed density
   mass) + 1e-4,

       smECE_sigma = sum_k |R(t_k) / D(t_k)| D(t_k) / sum_k D(t_k).

   Bandwidth rule (the default "smECE" of the package): sigma* is the fixed point of
   sigma = smECE_sigma, found by bisection on [0, 1] with 10 refinements, starting from the bracket
   (1, 0); the bisection returns the smallest examined sigma with sigma >= smECE_sigma (a sigma
   below 0.001 counts as too small). As in the package, sigma = 1 is returned directly in the edge
   case 1 < smECE_1. The reported value is
   smECE at sigma*. The convolution uses scipy.signal.fftconvolve (the package uses numpy.convolve;
   the two agree to floating-point rounding).

4. KS calibration error (`ks_calibration_error`), Gupta et al. (2021, arXiv 2006.12800), binary form:
   sort by s; KS = max_k | (1/n) sum_{i <= k} (y_i - s_i) |. With tied probabilities the partial
   sums are evaluated only at the end of each group of equal s (this design's rule, which makes the
   value independent of the order of tied samples; it equals the paper's value when there are no
   ties).

5. Equal-width ECE (`ece_equal_width`), used only for the [2610.31820] reconciliation (15 bins) and
   the MARGIN comparison (10 bins): bin index min(floor(s * B), B - 1);
   ECE = sum_b (n_b / n) |sbar_b - ybar_b|.

Sign convention for the Brier and calibration budgets (section 8, red team V13e): the gap is the
stated readout's value minus the probe's value (`analysis.gap`), so a positive gap means the stated
readout is worse.
"""

from __future__ import annotations

import numpy as np
from scipy.signal import fftconvolve

from pipeline.contracts.constants import ECE_EQUAL_MASS_BINS
from pipeline.contracts.schemas import ScoredSet

from ._common import as_weights, require_integer_weights

SMECE_EPS = 0.001          # relplot smECE eps: bandwidths below this count as too small
SMECE_DENSITY_EPS = 1e-4   # relplot BaseKernelMixin.smooth eps
SMECE_MESH_PTS = 200       # relplot config.smECE_mesh_pts
SMECE_REFINE = 10          # relplot search_param refine


# ---------------------------------------------------------------------------------------------------
# Equal-mass binning
# ---------------------------------------------------------------------------------------------------
def equal_mass_bin_index(prob: np.ndarray, weights: np.ndarray | None = None,
                         n_bins: int = ECE_EQUAL_MASS_BINS) -> np.ndarray:
    """Bin index per sample under the equal-mass scheme described in the module docstring."""
    p = np.asarray(prob, dtype=np.float64)
    w = as_weights(p.size, weights)
    require_integer_weights(w)
    keep = w > 0
    if not keep.any():
        return np.zeros(p.size, dtype=np.int64)
    vals, inv = np.unique(p[keep], return_inverse=True)
    wv = np.bincount(inv, weights=w[keep], minlength=vals.size)
    cum = np.cumsum(wv)                       # cum[j] = number of duplicated elements <= vals[j]
    n = int(round(cum[-1]))
    nb = min(int(n_bins), n)
    q, r = divmod(n, nb)
    sizes = np.full(nb, q, dtype=np.int64)
    sizes[:r] += 1
    ends = np.cumsum(sizes)                   # exclusive end position of each part

    def value_at(pos: np.ndarray) -> np.ndarray:
        # value of the element at 0-based position pos of the duplicated sorted list
        return vals[np.searchsorted(cum, pos, side="right")]

    bounds = []
    if nb > 1:
        e = ends[:-1]
        bounds = list((value_at(e - 1) + value_at(e)) / 2.0)
    bounds.append(1.0)
    edges = np.array(sorted(set(float(b) for b in bounds)))
    idx = np.searchsorted(edges, p, side="left")
    return np.minimum(idx, edges.size - 1).astype(np.int64)


def _bin_stats(prob, y, w, idx):
    nb = int(idx.max()) + 1 if idx.size else 0
    n_b = np.bincount(idx, weights=w, minlength=nb)
    s_b = np.bincount(idx, weights=w * prob, minlength=nb)
    y_b = np.bincount(idx, weights=w * y, minlength=nb)
    with np.errstate(invalid="ignore", divide="ignore"):
        sbar = np.where(n_b > 0, s_b / np.where(n_b > 0, n_b, 1), 0.0)
        ybar = np.where(n_b > 0, y_b / np.where(n_b > 0, n_b, 1), 0.0)
    return n_b, sbar, ybar


# ---------------------------------------------------------------------------------------------------
# Debiased equal-mass ECE (Kumar, Liang, and Ma 2019)
# ---------------------------------------------------------------------------------------------------
def ece_debiased_squared(s: ScoredSet, n_bins: int = ECE_EQUAL_MASS_BINS,
                         weights: np.ndarray | None = None) -> float:
    p = np.asarray(s.prob, dtype=np.float64)
    y = np.asarray(s.y, dtype=np.float64)
    w = as_weights(p.size, weights)
    n = w.sum()
    if n <= 0:
        return float("nan")
    idx = equal_mass_bin_index(p, w, n_bins)
    n_b, sbar, ybar = _bin_stats(p, y, w, idx)
    ok = n_b >= 2
    err = np.zeros_like(n_b)
    err[ok] = (sbar[ok] - ybar[ok]) ** 2 - ybar[ok] * (1.0 - ybar[ok]) / (n_b[ok] - 1.0)
    return float(np.sum(n_b / n * err))


def ece_debiased_equal_mass(s: ScoredSet, n_bins: int = ECE_EQUAL_MASS_BINS,
                            weights: np.ndarray | None = None) -> float:
    v = ece_debiased_squared(s, n_bins, weights)
    if not np.isfinite(v):
        return v
    return float(np.sqrt(max(v, 0.0)))


# ---------------------------------------------------------------------------------------------------
# Smooth ECE (Blasiok and Nakkiran 2023)
# ---------------------------------------------------------------------------------------------------
def _round_to_grid(f: np.ndarray, mass: np.ndarray, g: int) -> np.ndarray:
    pos = f * (g - 1)
    b = np.clip(pos.astype(np.int64), 0, g - 2)
    frac = pos - b
    out = np.bincount(b, weights=(1.0 - frac) * mass, minlength=g)
    out += np.bincount(b + 1, weights=frac * mass, minlength=g)
    return out[:g]


def _reflected_smooth(values: np.ndarray, sigma: float, g: int) -> np.ndarray:
    return _reflected_smooth_rows(values[None, :], sigma, g)[0]


def _interpolate(t: np.ndarray, yv: np.ndarray) -> np.ndarray:
    m = yv.size
    size = 1.0 / (m - 1)
    inds = np.clip((t * (m - 1)).astype(np.int64), 0, m - 2)
    res = (t - inds * size) / size
    return yv[inds] * (1.0 - res) + yv[inds + 1] * res


def smooth_ece_at(prob: np.ndarray, y: np.ndarray, sigma: float, weights: np.ndarray | None = None) -> float:
    """smECE at a fixed bandwidth sigma (module docstring, item 3)."""
    f = np.asarray(prob, dtype=np.float64)
    w = as_weights(f.size, weights)
    r = f - np.asarray(y, dtype=np.float64)
    e = max(round(10.0 / sigma), SMECE_MESH_PTS)
    t = np.linspace(0.0, 1.0, e)
    g = _grid_size(sigma)
    rs = _interpolate(t, _reflected_smooth(_round_to_grid(f, w * r, g), sigma, g))
    dens = _interpolate(t, _reflected_smooth(_round_to_grid(f, w, g), sigma, g)) + SMECE_DENSITY_EPS
    return float(np.sum(np.abs(rs / dens) * dens) / np.sum(dens))


def smooth_ece(s: ScoredSet, weights: np.ndarray | None = None, return_bandwidth: bool = False):
    """smECE at the fixed-point bandwidth (module docstring, item 3)."""
    f = np.asarray(s.prob, dtype=np.float64)
    y = np.asarray(s.y, dtype=np.float64)
    w = as_weights(f.size, weights)
    if w.sum() <= 0:
        return (float("nan"), float("nan")) if return_bandwidth else float("nan")

    def too_small(alpha: float) -> bool:
        return alpha < SMECE_EPS or alpha < smooth_ece_at(f, y, alpha, w)

    if too_small(1.0):
        sigma = 1.0            # relplot's edge case: returned when 1 < smECE_1
    else:
        lo, hi = 1.0, 0.0      # lo: not too small; hi: too small (relplot search_param names start, end)
        for _ in range(SMECE_REFINE):
            mid = (lo + hi) / 2.0
            if too_small(mid):
                hi = mid
            else:
                lo = mid
        sigma = lo
    v = smooth_ece_at(f, y, sigma, w)
    return (v, sigma) if return_bandwidth else v


def _grid_size(sigma: float) -> int:
    return max(2000, round(20.0 / sigma)) // 2 + 1


def _reflected_smooth_rows(values: np.ndarray, sigma: float, g: int) -> np.ndarray:
    """_reflected_smooth applied to every row of a (rows, g) array."""
    t = np.linspace(0.0, 1.0, g)
    ker = np.exp(-(t - 0.5) ** 2 / (2.0 * sigma * sigma)) / (np.sqrt(2.0 * np.pi) * sigma)
    ext = np.concatenate([values[:, ::-1][:, :-1], values, values[:, ::-1][:, 1:]], axis=1)
    conv = fftconvolve(ext, ker[None, :], mode="valid", axes=1)
    return conv[:, g // 2: g // 2 + g]


def smooth_ece_batch(prob: np.ndarray, y: np.ndarray, problem_index: np.ndarray, counts: np.ndarray,
                     n_problems: int) -> np.ndarray:
    """smooth_ece for every resample (rows of counts, problem multiplicities), vectorized.

    The bisection of the bandwidth rule visits dyadic midpoints, so at each step the resamples are
    grouped by their current midpoint and each group is evaluated in one batch. Grid assignment,
    reflected smoothing, and interpolation are linear in the masses, so for a bandwidth shared by at
    least n_problems resamples each problem's smoothed curves are computed once and a resample's
    curves are counts @ (per-problem curves); smaller groups are smoothed row by row.
    Values equal smooth_ece with the per-sample weights counts[b, problem_index] up to floating-point
    summation order (tested)."""
    f = np.asarray(prob, dtype=np.float64)
    r = f - np.asarray(y, dtype=np.float64)
    pi = np.asarray(problem_index)
    C = np.atleast_2d(np.asarray(counts, dtype=np.float64))
    nb = C.shape[0]
    grids: dict[int, tuple[np.ndarray, np.ndarray]] = {}

    def problem_grids(g: int):
        if g not in grids:
            pos = f * (g - 1)
            b = np.clip(pos.astype(np.int64), 0, g - 2)
            frac = pos - b
            Hr = np.zeros((n_problems, g))
            Hd = np.zeros((n_problems, g))
            np.add.at(Hr, (pi, b), (1.0 - frac) * r)
            np.add.at(Hr, (pi, b + 1), frac * r)
            np.add.at(Hd, (pi, b), 1.0 - frac)
            np.add.at(Hd, (pi, b + 1), frac)
            grids[g] = (Hr, Hd)
        return grids[g]

    smoothed: dict[float, tuple[np.ndarray, np.ndarray]] = {}

    def problem_curves(sigma: float):
        # Smoothing and interpolation are linear in the grid masses, so each problem's smoothed
        # residual and density curves at the evaluation points are computed once per bandwidth.
        if sigma not in smoothed:
            g = _grid_size(sigma)
            Hr, Hd = problem_grids(g)
            e = max(round(10.0 / sigma), SMECE_MESH_PTS)
            tt = np.linspace(0.0, 1.0, e)
            size = 1.0 / (g - 1)
            inds = np.clip((tt * (g - 1)).astype(np.int64), 0, g - 2)
            res = (tt - inds * size) / size
            R = _reflected_smooth_rows(Hr, sigma, g)
            D = _reflected_smooth_rows(Hd, sigma, g)
            smoothed[sigma] = (R[:, inds] * (1.0 - res) + R[:, inds + 1] * res,
                               D[:, inds] * (1.0 - res) + D[:, inds + 1] * res)
        return smoothed[sigma]

    def evaluate(rows: np.ndarray, sigma: float) -> np.ndarray:
        out = np.empty(rows.size)
        if sigma in smoothed or rows.size >= n_problems:
            Sr, Sd = problem_curves(sigma)
            for start in range(0, rows.size, 1024):
                cc = C[rows[start:start + 1024]]
                rs = cc @ Sr
                ds = cc @ Sd + SMECE_DENSITY_EPS
                out[start:start + 1024] = np.sum(np.abs(rs / ds) * ds, axis=1) / np.sum(ds, axis=1)
            return out
        # few resamples at this bandwidth: smooth their grids directly
        g = _grid_size(sigma)
        Hr, Hd = problem_grids(g)
        e = max(round(10.0 / sigma), SMECE_MESH_PTS)
        tt = np.linspace(0.0, 1.0, e)
        size = 1.0 / (g - 1)
        inds = np.clip((tt * (g - 1)).astype(np.int64), 0, g - 2)
        res = (tt - inds * size) / size
        for start in range(0, rows.size, 256):
            cc = C[rows[start:start + 256]]
            R = _reflected_smooth_rows(cc @ Hr, sigma, g)
            D = _reflected_smooth_rows(cc @ Hd, sigma, g)
            rs = R[:, inds] * (1.0 - res) + R[:, inds + 1] * res
            ds = D[:, inds] * (1.0 - res) + D[:, inds + 1] * res + SMECE_DENSITY_EPS
            out[start:start + 256] = np.sum(np.abs(rs / ds) * ds, axis=1) / np.sum(ds, axis=1)
        return out

    def too_small(rows: np.ndarray, alpha: float) -> np.ndarray:
        if alpha < SMECE_EPS:
            return np.ones(rows.size, dtype=bool)
        return alpha < evaluate(rows, alpha)

    all_rows = np.arange(nb)
    valid = C @ np.bincount(pi, minlength=n_problems).astype(float) > 0
    sigma = np.ones(nb)
    edge = np.zeros(nb, dtype=bool)
    edge[valid] = too_small(all_rows[valid], 1.0)
    lo = np.ones(nb)
    hi = np.zeros(nb)
    active = valid & ~edge
    for _ in range(SMECE_REFINE):
        mid = (lo + hi) / 2.0
        for mval in np.unique(mid[active]):
            rows = np.flatnonzero(active & (mid == mval))
            ts = too_small(rows, float(mval))
            hi[rows[ts]] = mval
            lo[rows[~ts]] = mval
    sigma[active] = lo[active]
    out = np.full(nb, np.nan)
    for sval in np.unique(sigma[valid]):
        rows = np.flatnonzero(valid & (sigma == sval))
        out[rows] = evaluate(rows, float(sval))
    return out


# ---------------------------------------------------------------------------------------------------
# KS calibration error (Gupta et al. 2021)
# ---------------------------------------------------------------------------------------------------
def ks_calibration_error(s: ScoredSet, weights: np.ndarray | None = None) -> float:
    f = np.asarray(s.prob, dtype=np.float64)
    y = np.asarray(s.y, dtype=np.float64)
    w = as_weights(f.size, weights)
    n = w.sum()
    if n <= 0:
        return float("nan")
    vals, inv = np.unique(f, return_inverse=True)
    d = np.bincount(inv, weights=w * (y - f), minlength=vals.size)
    return float(np.max(np.abs(np.cumsum(d))) / n)


# ---------------------------------------------------------------------------------------------------
# Equal-width ECE (reconciliation only)
# ---------------------------------------------------------------------------------------------------
def ece_equal_width(s: ScoredSet, n_bins: int, weights: np.ndarray | None = None) -> float:
    f = np.asarray(s.prob, dtype=np.float64)
    y = np.asarray(s.y, dtype=np.float64)
    w = as_weights(f.size, weights)
    n = w.sum()
    if n <= 0:
        return float("nan")
    idx = np.minimum(np.floor(f * n_bins).astype(np.int64), n_bins - 1)
    idx = np.maximum(idx, 0)
    n_b, sbar, ybar = _bin_stats(f, y, w, idx)
    return float(np.sum(n_b / n * np.abs(sbar - ybar)))
