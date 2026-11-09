"""Calibration + discrimination metrics.

The scalar metric functions are copied VERBATIM from src/v3_multimodel/exp_v3_all.py:62-117
(already validated + used for the v3 paper) so DPRC numbers are directly comparable to the base
study. Added below: `bootstrap_grouped` — a PROBLEM-level bootstrap for the per-requirement AUROC
headline, because pooling (problem, group) pairs violates independence and a flat/test-level
resample would give a dishonestly narrow CI (plan verification requirement).
"""
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression


# ==================== scalar metrics (verbatim from exp_v3_all.py) ====================

def compute_ece(c, a, n_bins=10):
    c, a = np.array(c, dtype=float), np.array(a, dtype=float)
    bounds = np.linspace(0, 1, n_bins + 1)
    ece = 0.0; bins = []
    for i in range(n_bins):
        m = (c >= bounds[i]) & (c < bounds[i+1]) if i < n_bins-1 else (c >= bounds[i]) & (c <= bounds[i+1])
        if m.sum() > 0:
            ba, bc, bs = float(a[m].mean()), float(c[m].mean()), int(m.sum())
            ece += (bs / len(c)) * abs(ba - bc)
            bins.append({"lo": float(bounds[i]), "hi": float(bounds[i+1]), "acc": ba, "conf": bc, "n": bs})
    return float(ece), bins


def compute_tace(c, a, threshold=0.01):
    """Thresholded Adaptive Calibration Error — robust to small bins."""
    c, a = np.array(c, dtype=float), np.array(a, dtype=float)
    sorted_idx = np.argsort(c)
    c_s, a_s = c[sorted_idx], a[sorted_idx]
    n = len(c)
    n_bins = max(1, int(np.sqrt(n)))
    bin_size = n // n_bins
    tace = 0.0
    for i in range(n_bins):
        start = i * bin_size
        end = start + bin_size if i < n_bins - 1 else n
        bc = c_s[start:end]; ba = a_s[start:end]
        if len(bc) > 0:
            gap = abs(ba.mean() - bc.mean())
            if gap > threshold:
                tace += (len(bc) / n) * gap
    return float(tace)


def compute_brier(c, a):
    return float(np.mean((np.array(c, dtype=float) - np.array(a, dtype=float)) ** 2))


def compute_auroc(c, a):
    c, a = np.array(c, dtype=float), np.array(a, dtype=float)
    return float(roc_auc_score(a, c)) if len(np.unique(a)) >= 2 else float('nan')


def bootstrap_all(c, a, n_boot=1000, seed=42):
    """Flat (i.i.d.) bootstrap over items. Correct for per-PROBLEM confidence (scalar tier);
    do NOT use for pooled per-group AUROC — use bootstrap_grouped for that."""
    rng = np.random.RandomState(seed); c, a = np.array(c, dtype=float), np.array(a, dtype=float)
    ece_fn = lambda c, a: compute_ece(c, a)[0]
    results = {}
    for name, fn in [("ece", ece_fn), ("brier", compute_brier), ("auroc", compute_auroc), ("tace", compute_tace)]:
        vals = []
        for _ in range(n_boot):
            idx = rng.randint(0, len(c), len(c))
            try:
                v = fn(c[idx], a[idx])
                if not np.isnan(v):
                    vals.append(v)
            except Exception:
                pass
        if vals:
            vals = sorted(vals)
            results[name] = float(np.mean(vals))
            results[f"{name}_ci"] = [float(vals[int(0.025*len(vals))]), float(vals[int(0.975*len(vals))])]
        else:
            results[name] = float('nan'); results[f"{name}_ci"] = [float('nan'), float('nan')]
    return results


# ==================== per-requirement (grouped) bootstrap — NEW for DPRC ====================

def per_requirement_auroc(records):
    """Pool all (problem, group) pairs and compute one AUROC.

    records: list of dicts, each {"problem_id": str, "conf": float, "label": 0/1}
      conf  = the model's self-reported confidence for that requirement group
      label = did the sampled solution pass that requirement group (1) or not (0)
    Returns float AUROC over the pooled pairs (nan if single-class).
    """
    confs = [r["conf"] for r in records]
    labels = [r["label"] for r in records]
    return compute_auroc(confs, labels)


def bootstrap_grouped(records, n_boot=1000, seed=42):
    """PROBLEM-level bootstrap of per-requirement AUROC.

    Resamples PROBLEMS with replacement (not individual (problem,group) pairs), then re-pools that
    problem's groups. This respects the dependence structure: multiple requirement groups from one
    problem are correlated, so resampling problems (the independent unit) is the honest CI.
    Returns {"auroc": mean, "auroc_ci": [lo, hi], "n_problems": int, "n_pairs": int}.
    """
    rng = np.random.RandomState(seed)
    by_prob = {}
    for r in records:
        by_prob.setdefault(r["problem_id"], []).append(r)
    prob_ids = list(by_prob.keys())
    point = per_requirement_auroc(records)
    vals = []
    for _ in range(n_boot):
        chosen = rng.randint(0, len(prob_ids), len(prob_ids))
        pooled = []
        for j in chosen:
            pooled.extend(by_prob[prob_ids[j]])
        v = per_requirement_auroc(pooled)
        if not np.isnan(v):
            vals.append(v)
    if vals:
        vals = sorted(vals)
        return {
            "auroc": float(point),
            "auroc_boot_mean": float(np.mean(vals)),
            "auroc_ci": [float(vals[int(0.025*len(vals))]), float(vals[int(0.975*len(vals))])],
            "n_problems": len(prob_ids),
            "n_pairs": len(records),
        }
    return {"auroc": float(point), "auroc_boot_mean": float('nan'),
            "auroc_ci": [float('nan'), float('nan')], "n_problems": len(prob_ids), "n_pairs": len(records)}


def localization_precision_at_1(problem_groups):
    """Fraction of problems where the model's LEAST-confident group is one that actually failed.

    problem_groups: list of per-problem dicts:
        {"confs": [c_g...], "labels": [0/1...]}  where label 1 = group passed, 0 = group failed.
    Only problems with >=1 failing group AND >=2 groups count (others are undefined for localization).
    """
    hits = 0; total = 0
    for p in problem_groups:
        confs, labels = p["confs"], p["labels"]
        if len(confs) < 2 or all(labels):   # need a failing group to localize
            continue
        total += 1
        least_conf_idx = int(np.argmin(confs))
        if labels[least_conf_idx] == 0:      # the least-confident group did fail
            hits += 1
    return (hits / total) if total else float('nan'), total


# ==================== post-hoc calibrators (baselines, verbatim from exp_v3_all.py) ====================

def isotonic_calibrate(confs_train, labels_train, confs_test):
    ir = IsotonicRegression(out_of_bounds='clip')
    ir.fit(confs_train, labels_train)
    return ir.predict(confs_test)


def platt_calibrate(confs_train, labels_train, confs_test):
    lr = LogisticRegression()
    lr.fit(np.array(confs_train).reshape(-1, 1), labels_train)
    return lr.predict_proba(np.array(confs_test).reshape(-1, 1))[:, 1]
