"""Primary decisions, per-model Holm decisions, heterogeneity, and the K4 sensitivity
(design sections 1.6, 1.8 rule 5, 9, and 13 K4).

Decisions at margin delta on an interval (L, U) (section 1.6):
    D1 (equivalence, TOST)            -delta < L and U < delta
    D2 (probe ahead by > delta)       L > delta
    D3 (stated ahead by > delta)      U < -delta
    otherwise inconclusive. At most one can hold (asserted). Conventional bounds L > 0 and U < 0 are
reported beside them as secondary. The primary interval is the 90 percent percentile interval of the
seed-averaged R_bar widened for refit variance (analysis.refit).

Per-model secondary decisions with Holm (section 9). Holm is applied separately to each decision
family (D1, D2, D3) across the six models, in its adjusted-level form: with alpha = 0.05, every model
is first tested at alpha/6; the models rejected are removed, and the rest are tested again at
alpha/(6 - number rejected), until a step rejects nothing. A one-sided test at level a uses the
one-sided bounds at 1 - a, i.e. the two-sided 1 - 2a percentile interval of the model's seed-averaged
replicates, widened with the per-model refit variance (pooled sigma2 / 3) and t_{12, 1 - a}; D2
rejects when L > delta, D3 when U < -delta, D1 (both one-sided tests at level a) when
-delta < L and U < delta. This step-down form gives the same rejections as Holm on p-values whenever
rejection is monotone in the level (a test that rejects at a also rejects at any larger level), and
it needs no p-value for an interval that is widened for refit variance; it was chosen for that
reason. A model whose interval is unavailable is counted among the hypotheses and never rejected.

Heterogeneity (section 9): between-model SD of point estimates (ddof 1);
tau2_hat = max(0, Var_m(point_m) - mean_m Var_boot(point_m)), Var_m with ddof 1 and the bootstrap
variance with ddof 1 over defined replicates; its bootstrap interval comes from
tau2_b = max(0, Var_m(rep_{m,b}) - mean_m Var_boot), with the bootstrap-variance term held at its
full-sample value. The heterogeneity sentence fires when tau_hat > delta, or when per-model
decision intervals disagree in sign (one entirely above +delta and another entirely below -delta).
"""

from __future__ import annotations

from typing import Mapping, Sequence

import numpy as np

from pipeline.contracts.constants import (ALPHA, DECISION_INTERVAL_LEVEL, DELTA, DELTA_SENSITIVITY,
                                          POOLED_RESIDUAL_MARGIN, SHAPLEY_MARGINAL_LEVEL)
from pipeline.contracts.schemas import DecisionResult

from .bootstrap import interval_dict, one_sided_bounds, percentile_interval, undefined_summary
from .refit import (between_seed_variance, mean_over_models, refit_df, s2_refit, s2_refit_single_model,
                    seed_average, seed_averaged_replicates, t_quantile, widen)

FAMILIES = {"qwen3": ("P1", "P2"), "olmo3": ("P3", "P4"), "gemma4": ("P5", "P6")}


def classify_interval(lo: float, hi: float, delta: float) -> str:
    if not (np.isfinite(lo) and np.isfinite(hi)):
        return "inconclusive"
    reached = []
    if -delta < lo and hi < delta:
        reached.append("D1")
    if lo > delta:
        reached.append("D2")
    if hi < -delta:
        reached.append("D3")
    assert len(reached) <= 1, f"decisions not mutually exclusive: {reached}"
    return reached[0] if reached else "inconclusive"


def decide(r_bar: float, replicates: np.ndarray, per_model_seed_r: Mapping[str, Sequence[float]],
           delta: float = DELTA, level: float = DECISION_INTERVAL_LEVEL) -> DecisionResult:
    """Primary decision on R_bar with the refit-widened interval (sections 1.6 and 9)."""
    iv = percentile_interval(r_bar, replicates, level)
    sigma2 = between_seed_variance(per_model_seed_r)
    s2 = s2_refit(sigma2)
    t = t_quantile(refit_df(len(sigma2)), 1.0 - (1.0 - level) / 2.0)
    if iv.unavailable:
        nan = float("nan")
        return DecisionResult(delta=delta, r_bar=float(r_bar), h=nan, s_refit=float(np.sqrt(s2)),
                              t_quantile=t, unwidened=(nan, nan), widened=(nan, nan),
                              decision="inconclusive", conventional_positive=False,
                              conventional_negative=False, per_model_sigma2=sigma2)
    w = widen(iv.lo, iv.hi, float(np.sqrt(s2)), t)
    return DecisionResult(delta=delta, r_bar=float(r_bar), h=w["h"], s_refit=float(np.sqrt(s2)), t_quantile=t,
                          unwidened=(iv.lo, iv.hi), widened=(w["lo"], w["hi"]),
                          decision=classify_interval(w["lo"], w["hi"], delta),
                          conventional_positive=bool(w["lo"] > 0), conventional_negative=bool(w["hi"] < 0),
                          per_model_sigma2=sigma2)


def decide_unwidened(point: float, replicates: np.ndarray, delta: float,
                     level: float = DECISION_INTERVAL_LEVEL) -> dict:
    """Three decisions on a percentile interval with no refit component (R_pool, section 1.6:
    secondary, at its own margin, fit at fold seed 0 only)."""
    iv = percentile_interval(point, replicates, level)
    dec = classify_interval(iv.lo, iv.hi, delta) if not iv.unavailable else "inconclusive"
    return {"delta": delta, "interval": interval_dict(iv), "decision": dec,
            "conventional_positive": bool(not iv.unavailable and iv.lo > 0),
            "conventional_negative": bool(not iv.unavailable and iv.hi < 0)}


# ---------------------------------------------------------------------------------------------------
# Per-model decisions
# ---------------------------------------------------------------------------------------------------
def _model_bounds(reps: np.ndarray, a: float, s_refit: float, df: int) -> tuple[float, float]:
    lo, hi = one_sided_bounds(reps, a)
    w = widen(lo, hi, s_refit, t_quantile(df, 1.0 - a))
    return w["lo"], w["hi"]


def _rejects(decision: str, L: float, U: float, delta: float) -> bool:
    if decision == "D1":
        return -delta < L and U < delta
    if decision == "D2":
        return L > delta
    if decision == "D3":
        return U < -delta
    raise ValueError(decision)


def holm_per_model(per_model_reps: Mapping[str, np.ndarray], s_refit_model: float, df: int,
                   delta: float = DELTA, alpha: float = ALPHA) -> dict[str, dict]:
    """Holm across models for each decision family (module docstring). Returns, per model, a dict
    with D1, D2, D3 (bool), the level at which each was rejected, and the resulting decision."""
    models = list(per_model_reps)
    k = len(models)
    available = {m for m in models if not undefined_summary(per_model_reps[m])[2]}
    out = {m: {"D1": False, "D2": False, "D3": False, "level": {}} for m in models}
    for dec in ("D1", "D2", "D3"):
        rejected: set[str] = set()
        while True:
            a = alpha / (k - len(rejected))
            new = set()
            for m in sorted(available - rejected):
                L, U = _model_bounds(per_model_reps[m], a, s_refit_model, df)
                if _rejects(dec, L, U, delta):
                    new.add(m)
            if not new:
                break
            for m in new:
                out[m]["level"][dec] = a
            rejected |= new
            if len(rejected) == k:
                break
        for m in rejected:
            out[m][dec] = True
    for m in models:
        reached = [d for d in ("D1", "D2", "D3") if out[m][d]]
        out[m]["holm_conflict"] = len(reached) > 1
        out[m]["decision"] = reached[0] if len(reached) == 1 else "inconclusive"
        out[m]["available"] = m in available
    return out


def per_model_intervals(points: Mapping[str, float], per_model_reps: Mapping[str, np.ndarray],
                        s_refit_model: float, df: int, delta: float = DELTA,
                        level: float = DECISION_INTERVAL_LEVEL) -> dict[str, dict]:
    """Each model's 90 percent interval, unwidened and widened, and its unadjusted classification
    (rule 5 counts: within the margin, entirely above, entirely below)."""
    t = t_quantile(df, 1.0 - (1.0 - level) / 2.0)
    out = {}
    for m, reps in per_model_reps.items():
        iv = percentile_interval(points[m], reps, level)
        if iv.unavailable:
            out[m] = {"point": points[m], "unwidened": interval_dict(iv), "widened": None,
                      "within_margin": False, "above": False, "below": False}
            continue
        w = widen(iv.lo, iv.hi, s_refit_model, t)
        out[m] = {"point": points[m], "unwidened": interval_dict(iv),
                  "widened": {"lo": w["lo"], "hi": w["hi"], "half": w["half"], "h": w["h"]},
                  "within_margin": bool(-delta < w["lo"] and w["hi"] < delta),
                  "above": bool(w["lo"] > delta), "below": bool(w["hi"] < -delta)}
    return out


# ---------------------------------------------------------------------------------------------------
# Heterogeneity
# ---------------------------------------------------------------------------------------------------
def heterogeneity(points: Mapping[str, float], per_model_reps: Mapping[str, np.ndarray],
                  levels: Sequence[float] = (DECISION_INTERVAL_LEVEL, SHAPLEY_MARGINAL_LEVEL)) -> dict:
    models = list(points)
    pts = np.array([points[m] for m in models], dtype=np.float64)
    reps = np.vstack([np.asarray(per_model_reps[m], dtype=np.float64) for m in models])
    var_m = float(np.var(pts, ddof=1)) if len(models) > 1 else float("nan")
    boot_var = []
    for i in range(len(models)):
        r = reps[i][np.isfinite(reps[i])]
        boot_var.append(float(np.var(r, ddof=1)) if r.size > 1 else float("nan"))
    mean_boot = float(np.mean(boot_var))
    tau2 = max(0.0, var_m - mean_boot) if np.isfinite(var_m) and np.isfinite(mean_boot) else float("nan")
    with np.errstate(invalid="ignore"):
        var_b = np.var(reps, axis=0, ddof=1) if len(models) > 1 else np.full(reps.shape[1], np.nan)
    tau2_b = np.where(np.isfinite(var_b), np.maximum(0.0, var_b - mean_boot), np.nan)
    sd_b = np.sqrt(var_b)
    out = {"models": models, "between_model_sd": float(np.sqrt(var_m)) if np.isfinite(var_m) else None,
           "var_between": var_m, "boot_var_per_model": dict(zip(models, boot_var)),
           "mean_boot_var": mean_boot, "tau2_hat": tau2,
           "tau_hat": float(np.sqrt(tau2)) if np.isfinite(tau2) else None,
           "intervals": {}}
    for lv in levels:
        out["intervals"][f"{lv:g}"] = {
            "tau2": interval_dict(percentile_interval(tau2, tau2_b, lv)),
            "between_model_sd": interval_dict(percentile_interval(out["between_model_sd"], sd_b, lv)),
        }
    return out


def family_means(points: Mapping[str, float], per_model_reps: Mapping[str, np.ndarray],
                 level: float = SHAPLEY_MARGINAL_LEVEL) -> dict:
    """Per-family mean of two models each, descriptive (section 9)."""
    out = {}
    for fam, (a, b) in FAMILIES.items():
        if a in points and b in points:
            pt = (points[a] + points[b]) / 2.0
            rep = (np.asarray(per_model_reps[a]) + np.asarray(per_model_reps[b])) / 2.0
            out[fam] = interval_dict(percentile_interval(pt, rep, level))
    return out


def heterogeneity_fires(tau_hat: float | None, per_model: Mapping[str, dict], delta: float = DELTA) -> dict:
    above = [m for m, v in per_model.items() if v.get("above")]
    below = [m for m, v in per_model.items() if v.get("below")]
    sign = bool(above) and bool(below)
    tau = tau_hat is not None and np.isfinite(tau_hat) and tau_hat > delta
    return {"fires": bool(sign or tau), "tau_exceeds_delta": bool(tau), "sign_disagreement": sign,
            "above": above, "below": below}


# ---------------------------------------------------------------------------------------------------
# Full primary report
# ---------------------------------------------------------------------------------------------------
def decision_dict(d: DecisionResult) -> dict:
    out = d.to_dict()
    out["unwidened"] = [None if not np.isfinite(x) else x for x in d.unwidened]
    out["widened"] = [None if not np.isfinite(x) else x for x in d.widened]
    out["h"] = None if not np.isfinite(d.h) else d.h
    return out


def primary_report(per_model_seed_r: Mapping[str, Sequence[float]],
                   per_model_seed_reps: Mapping[str, Sequence[np.ndarray]],
                   flagged: Mapping[str, bool] | None = None, delta: float = DELTA,
                   sensitivity_deltas: Sequence[float] = DELTA_SENSITIVITY,
                   bca: dict | None = None) -> dict:
    """R_bar, its decisions at delta and at the sensitivity margins, per-model intervals and Holm
    decisions, heterogeneity, per-family means, and the K4 sensitivity over unflagged models."""
    r_m = seed_average(per_model_seed_r)
    rep_m = seed_averaged_replicates(per_model_seed_reps)
    r_bar = float(np.mean(list(r_m.values())))
    rep_bar = mean_over_models(rep_m)
    sigma2 = between_seed_variance(per_model_seed_r)
    df = refit_df(len(sigma2))
    s_model = float(np.sqrt(s2_refit_single_model(sigma2)))
    main = decide(r_bar, rep_bar, per_model_seed_r, delta)
    out: dict = {
        "r_bar": r_bar, "r_m": r_m, "per_seed": {m: list(map(float, v)) for m, v in per_model_seed_r.items()},
        "decision": decision_dict(main),
        "sensitivity": {f"{d:g}": decision_dict(decide(r_bar, rep_bar, per_model_seed_r, d))
                        for d in sensitivity_deltas},
        "per_model_refit_sd": s_model, "refit_df": df,
    }
    pm = per_model_intervals(r_m, rep_m, s_model, df, delta)
    out["per_model"] = pm
    out["per_model_holm"] = holm_per_model(rep_m, s_model, df, delta)
    out["per_model_counts"] = {"within_margin": sum(v["within_margin"] for v in pm.values()),
                               "above": sum(v["above"] for v in pm.values()),
                               "below": sum(v["below"] for v in pm.values()),
                               "min": min(r_m.values()), "max": max(r_m.values())}
    het = heterogeneity(r_m, rep_m)
    out["heterogeneity"] = het
    out["heterogeneity_sentence"] = heterogeneity_fires(het["tau_hat"], pm, delta)
    out["family_means"] = family_means(r_m, rep_m)
    if bca is not None:
        out["bca"] = bca
    flagged = dict(flagged or {})
    unflagged = [m for m in r_m if not flagged.get(m, False)]
    k4: dict = {"flagged": sorted(m for m in r_m if flagged.get(m, False))}
    if 0 < len(unflagged) < len(r_m):
        sub_r = {m: per_model_seed_r[m] for m in unflagged}
        sub_rep = mean_over_models({m: rep_m[m] for m in unflagged})
        r_bar_u = float(np.mean([r_m[m] for m in unflagged]))
        dec_u = decide(r_bar_u, sub_rep, sub_r, delta)
        k4.update({"r_bar_unflagged": r_bar_u, "decision": decision_dict(dec_u),
                   "decision_only_through_flagged": bool(main.decision != "inconclusive"
                                                         and dec_u.decision != main.decision)})
    elif not unflagged:
        k4.update({"r_bar_unflagged": None, "decision": None, "decision_only_through_flagged": None,
                   "note": "every model is flagged"})
    else:
        k4.update({"r_bar_unflagged": r_bar, "decision": None, "decision_only_through_flagged": False,
                   "note": "no model is flagged"})
    out["k4_sensitivity"] = k4
    return out


def pooled_residual_report(per_model_point: Mapping[str, float], per_model_reps: Mapping[str, np.ndarray],
                           margin: float = POOLED_RESIDUAL_MARGIN) -> dict:
    """R_pool = Gamma(1, 1, 0, 1), mean over models at fold seed 0, with the three decisions at its
    own margin, labeled secondary and unadjusted (section 1.6)."""
    pt = float(np.mean(list(per_model_point.values())))
    rep = mean_over_models(per_model_reps)
    out = decide_unwidened(pt, rep, margin)
    out["label"] = "secondary, unadjusted; fold seed 0; no refit component"
    out["point"] = pt
    out["per_model"] = {m: interval_dict(percentile_interval(per_model_point[m], per_model_reps[m],
                                                             DECISION_INTERVAL_LEVEL))
                        for m in per_model_point}
    return out
