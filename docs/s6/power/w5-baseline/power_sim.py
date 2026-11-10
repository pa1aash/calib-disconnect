"""Design-stage power simulation for the primary contrast of PIPELINE_DESIGN (wave 5).

This is a planning calculation, not pipeline code and not a result. It simulates the
pair-weighted within-problem AUROC gap G = W(probe) - W(trained stated readout) under stated
assumptions and reports how often the problem-clustered bootstrap decides each outcome.
The assumptions are listed in ASSUMPTIONS below and copied into power_sim.json.

Run: python3 -I docs/s5/power/power_sim.py  (numpy only; deterministic seed).
"""

import json
import math
import sys
from pathlib import Path

import numpy as np

ASSUMPTIONS = {
    "pass_rate_distribution": "per-problem pass probability p_i ~ Beta(0.6, 0.5), U-shaped as on code benchmarks",
    "score_model": "within problem, readout score = d_r * y + u_i + e, e ~ N(0,1); binormal, so AUROC_within = Phi(d_r/sqrt(2))",
    "problem_heterogeneity": "per-problem separation d_ri = d_r + N(0, 0.3^2), shared shift for both readouts (rho_het = 1)",
    "readout_noise_correlation": "corr(e_probe, e_stated) = 0.5 within sample",
    "stated_readout_ties": "stated readout rounded to 11 bins after a per-problem logistic squashing, which creates ties",
    "baseline_within_auroc_stated": 0.65,
    "delta": 0.03,
    "bootstrap": "problem-clustered percentile bootstrap, B = 400 in simulation (B = 10000 in the study), one-sided 95 percent bounds",
    "models_pooled": "M models share the problem set; the pooled gap is the mean of per-model gaps; problem-level gap shocks shared across models with SD 0.05",
    "replicates": 200,
}


def phi_inv(p):
    # inverse standard normal CDF via erfinv-free bisection (avoids scipy dependency)
    lo, hi = -10.0, 10.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if 0.5 * (1 + math.erf(mid / math.sqrt(2))) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def d_for_auc(a):
    return math.sqrt(2.0) * phi_inv(a)


def pair_stats(scores, y):
    """Per-problem numerator (pass-fail pairs ordered correctly, ties half) and pair count."""
    pos = scores[y == 1]
    neg = scores[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return 0.0, 0
    diff = pos[:, None] - neg[None, :]
    num = float((diff > 0).sum() + 0.5 * (diff == 0).sum())
    return num, len(pos) * len(neg)


def simulate_model(rng, n_problems, k, d_probe, d_stated, shared_shock):
    nums_p = np.zeros(n_problems)
    nums_s = np.zeros(n_problems)
    pairs = np.zeros(n_problems)
    p = rng.beta(0.6, 0.5, size=n_problems)
    for i in range(n_problems):
        y = (rng.random(k) < p[i]).astype(int)
        if y.min() == y.max():
            continue
        het = rng.normal(0, 0.3)
        dp = max(d_probe + het + shared_shock[i], 0.0)
        ds = max(d_stated + het, 0.0)
        e1 = rng.normal(size=k)
        e2 = 0.5 * e1 + math.sqrt(1 - 0.25) * rng.normal(size=k)
        u = rng.normal()
        sp = dp * y + u + e1
        raw_s = ds * y + u + e2
        ss = np.round(10.0 / (1.0 + np.exp(-raw_s))) / 10.0
        nums_p[i], pairs[i] = pair_stats(sp, y)
        nums_s[i], _ = pair_stats(ss, y)
    return nums_p, nums_s, pairs


def bootstrap_bounds(rng, nums_p_list, nums_s_list, pairs_list, B):
    n = len(pairs_list[0])
    idx = rng.integers(0, n, size=(B, n))
    gaps = np.zeros(B)
    for npm, nsm, prm in zip(nums_p_list, nums_s_list, pairs_list):
        w_p = npm[idx].sum(1) / prm[idx].sum(1)
        w_s = nsm[idx].sum(1) / prm[idx].sum(1)
        gaps += (w_p - w_s)
    gaps /= len(pairs_list)
    return float(np.quantile(gaps, 0.05)), float(np.quantile(gaps, 0.95))


def point_gap(nums_p_list, nums_s_list, pairs_list):
    g = [npm.sum() / prm.sum() - nsm.sum() / prm.sum() for npm, nsm, prm in zip(nums_p_list, nums_s_list, pairs_list)]
    return float(np.mean(g))


def run(scenarios, reps, B, seed):
    rng = np.random.default_rng(seed)
    a_s = ASSUMPTIONS["baseline_within_auroc_stated"]
    delta = ASSUMPTIONS["delta"]
    out = []
    for sc in scenarios:
        d_s = d_for_auc(a_s)
        d_p = d_for_auc(min(a_s + sc["true_gap_nominal"], 0.99))
        dec_gap = dec_eq = 0
        mixed = []
        realized = []
        for _ in range(reps):
            shock = rng.normal(0, 0.05, size=sc["n_problems"]) / 0.26  # 0.05 AUROC units, near dA/dd = 0.26
            res = [simulate_model(rng, sc["n_problems"], sc["k"], d_p, d_s, shock) for _ in range(sc["models"])]
            npl = [r[0] for r in res]
            nsl = [r[1] for r in res]
            prl = [r[2] for r in res]
            mixed.append(float(np.mean([(pr > 0).sum() for pr in prl])))
            realized.append(point_gap(npl, nsl, prl))
            lo, hi = bootstrap_bounds(rng, npl, nsl, prl, B)
            dec_gap += lo > delta
            dec_eq += hi < delta
        out.append({
            **sc,
            "mean_mixed_problems_per_model": round(float(np.mean(mixed)), 1),
            "mean_realized_gap": round(float(np.mean(realized)), 4),
            "p_decide_controlled_gap": round(dec_gap / reps, 3),
            "p_decide_no_controlled_gap": round(dec_eq / reps, 3),
            "p_inconclusive": round(1 - (dec_gap + dec_eq) / reps, 3),
        })
        print(json.dumps(out[-1]), file=sys.stderr)
    return out


def main():
    reps = ASSUMPTIONS["replicates"]
    scen = []
    for k in (5, 10, 16):
        for n in (300, 600, 1100):
            for g in (0.0, 0.06, 0.08):
                scen.append({"k": k, "n_problems": n, "models": 1, "true_gap_nominal": g})
    for k in (10,):
        for n in (600, 1100):
            for g in (0.0, 0.05, 0.06):
                scen.append({"k": k, "n_problems": n, "models": 6, "true_gap_nominal": g})
    res = run(scen, reps=reps if "--quick" not in sys.argv else 40, B=400, seed=20261110)
    path = Path(__file__).with_name("power_sim.json")
    path.write_text(json.dumps({"assumptions": ASSUMPTIONS, "results": res}, indent=1) + "\n")
    print(f"wrote {path.name}")


if __name__ == "__main__":
    main()
