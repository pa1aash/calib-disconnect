"""Problem-clustered paired bootstrap (design section 9; section 11, rows 8.1 to 8.5).

- `draw` makes B resamples of problems with replacement from one generator seeded with
  BOOTSTRAP_SEED: resample b draws n problem indices uniformly with replacement (a multinomial draw
  with equal probabilities), and counts[b, i] is the multiplicity of problem i. The same draws are
  reused for every statistic, model, readout, suite, and cell, so every comparison is paired.
- `replicate` maps a statistic over resamples and returns NaN where it is undefined.
- `percentile_interval` drops undefined replicates for that statistic only, reports how many were
  dropped, and reports the interval as unavailable when more than UNDEFINED_REPLICATE_MAX_SHARE
  (1 percent) of resamples are undefined (section 9, red team V13a). Nothing is imputed.
  Section 11, row 8.4 says undefined replicates are "kept and counted"; section 9 (the later red-team
  fix) governs, and this module implements section 9.
- Quantiles use numpy's default "linear" method (Hyndman and Fan type 7).
- `bca_interval` is the bias-corrected and accelerated interval (Efron 1987), a sensitivity analysis
  for the primary statistic only, with the acceleration from the leave-one-problem-out jackknife.
"""

from __future__ import annotations

from typing import Callable, Sequence

import numpy as np
from scipy.stats import norm

from pipeline.contracts.constants import B_BOOTSTRAP, BOOTSTRAP_SEED, UNDEFINED_REPLICATE_MAX_SHARE
from pipeline.contracts.schemas import BootstrapDraws, Interval


def draw(problem_ids: Sequence[str], b: int = B_BOOTSTRAP, seed: int = BOOTSTRAP_SEED) -> BootstrapDraws:
    """B problem-clustered resamples. Column i of counts belongs to problem_ids[i]; callers pass the
    population's problem IDs in sorted order so the draws are the same in every stage."""
    ids = tuple(problem_ids)
    n = len(ids)
    if len(set(ids)) != n:
        raise ValueError("problem_ids must be unique")
    if n == 0 or b < 1:
        raise ValueError("need at least one problem and one resample")
    if n > np.iinfo(np.uint16).max:
        raise ValueError("too many problems for uint16 counts")
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(b, n))
    flat = (idx + (np.arange(b) * n)[:, None]).ravel()
    counts = np.bincount(flat, minlength=b * n).reshape(b, n).astype(np.uint16)
    return BootstrapDraws(seed=int(seed), problem_ids=ids, counts=counts)


def jackknife_counts(n_problems: int) -> np.ndarray:
    """Leave-one-problem-out multiplicities: row i is all ones except a zero at problem i. Fed to the
    same vectorized statistics as bootstrap counts."""
    return np.ones((n_problems, n_problems), dtype=np.float64) - np.eye(n_problems)


def _as_float(v) -> float:
    if v is None:
        return float("nan")
    v = float(v)
    return v if np.isfinite(v) else float("nan")


def replicate(stat_fn: Callable[[np.ndarray], float | None], draws: BootstrapDraws | np.ndarray,
              problem_index: np.ndarray | None = None) -> np.ndarray:
    """Evaluate stat_fn on every resample. If problem_index is given, stat_fn receives per-sample
    weights counts[b, problem_index]; otherwise it receives the problem multiplicity row counts[b].
    Returns float64[B] with NaN where stat_fn returns None or a non-finite value."""
    counts = draws.counts if isinstance(draws, BootstrapDraws) else np.asarray(draws)
    out = np.empty(counts.shape[0], dtype=np.float64)
    for b in range(counts.shape[0]):
        row = counts[b].astype(np.float64)
        arg = row[problem_index] if problem_index is not None else row
        out[b] = _as_float(stat_fn(arg))
    return out


def undefined_summary(replicates: np.ndarray, max_share: float = UNDEFINED_REPLICATE_MAX_SHARE) -> tuple[np.ndarray, int, bool]:
    r = np.asarray(replicates, dtype=np.float64)
    ok = np.isfinite(r)
    n_undef = int((~ok).sum())
    unavailable = r.size == 0 or n_undef > max_share * r.size
    return r[ok], n_undef, unavailable


def percentile_interval(point: float | None, replicates: np.ndarray, level: float,
                        max_undefined_share: float = UNDEFINED_REPLICATE_MAX_SHARE) -> Interval:
    """Percentile interval at `level` (two-sided). Undefined replicates are dropped and counted;
    the interval is unavailable when more than max_undefined_share of them are undefined or when the
    point estimate itself is undefined."""
    pt = _as_float(point)
    good, n_undef, unavailable = undefined_summary(replicates, max_undefined_share)
    if unavailable or not np.isfinite(pt) or good.size == 0:
        return Interval(point=pt, lo=float("nan"), hi=float("nan"), level=float(level),
                        n_undefined=n_undef, unavailable=True)
    a = (1.0 - level) / 2.0
    lo, hi = np.quantile(good, [a, 1.0 - a])
    return Interval(point=pt, lo=float(lo), hi=float(hi), level=float(level), n_undefined=n_undef,
                    unavailable=False)


def one_sided_bounds(replicates: np.ndarray, alpha: float) -> tuple[float, float]:
    """(alpha quantile, 1 - alpha quantile) of the defined replicates: the two one-sided bounds at
    level 1 - alpha, i.e. the two-sided 1 - 2 alpha percentile interval."""
    good = np.asarray(replicates, dtype=np.float64)
    good = good[np.isfinite(good)]
    lo, hi = np.quantile(good, [alpha, 1.0 - alpha])
    return float(lo), float(hi)


def bca_interval(point: float | None, replicates: np.ndarray, jackknife_values: np.ndarray, level: float,
                 max_undefined_share: float = UNDEFINED_REPLICATE_MAX_SHARE) -> Interval:
    """BCa interval. Bias correction z0 = Phi^{-1}((#{theta*_b < theta} + 0.5 #{theta*_b = theta}) / B)
    over defined replicates; acceleration a = sum (m - theta_(i))^3 / (6 (sum (m - theta_(i))^2)^{3/2})
    with theta_(i) the leave-one-problem-out values and m their mean. Endpoints are the quantiles at
    Phi(z0 + (z0 + z_q) / (1 - a (z0 + z_q))) for q = (1 - level)/2 and 1 - (1 - level)/2.
    Unavailable under the same undefined-replicate rule, or when z0 is infinite or a jackknife value
    is undefined."""
    pt = _as_float(point)
    good, n_undef, unavailable = undefined_summary(replicates, max_undefined_share)
    jk = np.asarray(jackknife_values, dtype=np.float64)
    bad = Interval(point=pt, lo=float("nan"), hi=float("nan"), level=float(level), n_undefined=n_undef,
                   unavailable=True)
    if unavailable or not np.isfinite(pt) or good.size == 0 or not np.all(np.isfinite(jk)) or jk.size < 2:
        return bad
    prop = (np.sum(good < pt) + 0.5 * np.sum(good == pt)) / good.size
    if prop <= 0.0 or prop >= 1.0:
        return bad
    z0 = norm.ppf(prop)
    m = jk.mean()
    d = m - jk
    ss = np.sum(d * d)
    acc = float(np.sum(d ** 3) / (6.0 * ss ** 1.5)) if ss > 0 else 0.0
    q = (1.0 - level) / 2.0
    out = []
    for zq in (norm.ppf(q), norm.ppf(1.0 - q)):
        den = 1.0 - acc * (z0 + zq)
        if den <= 0:
            return bad
        out.append(norm.cdf(z0 + (z0 + zq) / den))
    lo, hi = np.quantile(good, out)
    return Interval(point=pt, lo=float(lo), hi=float(hi), level=float(level), n_undefined=n_undef,
                    unavailable=False)


def interval_dict(iv: Interval) -> dict:
    d = iv.to_dict()
    for k in ("point", "lo", "hi"):
        if d[k] is not None and not np.isfinite(d[k]):
            d[k] = None
    return d
