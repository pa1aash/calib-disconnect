"""Design-stage power simulation, wave 6 B9 (systematics budget). Planning arithmetic, not a result.

Adapted from docs/s6/power/w5-baseline/power_sim.py (baseline not edited). Simulates the gap
Gap(S) = M_P(S) - M_S(S) over 16 cells defined by four toggles (RECAL, TRAIN, DIFF, LABEL), its
Shapley and sequential decompositions, and the decisions of a problem-clustered percentile bootstrap
on the residual R = Gap(all on), averaged over M models.

Run: python3 -I docs/s6/parts/power-B9/power_sim.py [--quick]   (numpy only; deterministic seeds).
"""

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"

import itertools
import json
import math
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

QUICK = "--quick" in sys.argv

ASSUMPTIONS = {
    "status": "design-stage planning arithmetic under stated assumptions; not a result",
    "pass_rate_distribution": "per-problem pass probability p_i ~ Beta(0.6, 0.5), shared across models; samples y_ij ~ Bernoulli(p_i), independent across models given p_i; a new problem set is drawn each replicate",
    "z": "z_i = standardized logit(p_i) (p clipped to [1e-3, 1-1e-3]; standardized over the simulated problem set)",
    "score_model": "s_P = d_P*y + a_P*z_i + e_P; s_S = d_S(level)*y + a_S*z_i + e_S; e ~ N(0,1); corr(e_P, e_S) = 0.5",
    "difficulty_loadings": {"a_P": 0.8, "a_S": 0.3, "note": "a_P > a_S: probe captures difficulty, inflating pooled AUROC; values are assumptions"},
    "probe_within_auroc": "0.72, d_P = sqrt(2)*Phi^-1(0.72), before heterogeneity, clipping, and shocks",
    "zero_shot_stated": "d0 = sqrt(2)*Phi^-1(0.60) (within AUROC about 0.60 before 11-bin rounding)",
    "trained_stated": "d1 is calibrated per (k, true R) by bisection on a 30000-problem simulation so that the population residual R (all toggles on) equals the scenario value; calibration results are in the calibration block",
    "problem_heterogeneity": "per-problem separation shift het ~ N(0, 0.3^2), shared by both readouts; separation clipped at 0",
    "gap_shocks": "per-model, per-problem shock on the probe separation, SD 0.05 AUROC units / 0.26 (dA/dd near 0.26), independent across models, added to d_P",
    "stated_ties": "stated score rounded to 11 bins: bin = round(10*sigmoid(s_S)), integers 0..10",
    "RECAL": "isotonic (PAV, weighted by bin counts) of the active label on the stated bin, cross-fit: fit on even-index problems and apply to odd-index problems, and vice versa; empty bins forward-filled; probe unchanged; effect only through merged ties and cross-half value differences in the pooled metric",
    "TRAIN": "stated separation d0 (off) versus d1 (on); the probe is the same in both",
    "DIFF": "off = pooled AUROC over all samples of all problems (ties half); on = pair-weighted within-problem AUROC (sum of correct pass-fail pairs over sum of pairs; all-pass and all-fail problems carry zero pairs)",
    "LABEL": "off = original weak suite label y_w; on = EvalPlus label y (true). Signals always relate to y",
    "weak_suite_false_passes": "fraction f = 0.08 of truly failing samples (in expectation) become false passes in the weak suite; per-problem rate q_i = min(1, c*w_i), w_i = exp(-0.5*((p_i-0.5)/0.15)^2), c set so the expected failing-sample false-pass fraction is f",
    "multi_model": "M models share the problem set; primary statistic is the mean over models of R; the bootstrap resamples problems jointly across models (paired, clustered)",
    "bootstrap": "problem-clustered percentile bootstrap, B = 400 draws (B = 10000 in the study); pooled AUROC in the bootstrap is computed from counts, with the probe discretized into 128 quantile bins (negligible tie error); within metrics are exact",
    "decisions": "equivalence (TOST): 90 percent percentile CI of R inside (-delta, delta), i.e. 5th percentile > -delta and 95th percentile < delta; superiority: 5th percentile of R > delta (one-sided 95 percent lower bound); else inconclusive; also P(5th percentile > 0)",
    "delta": 0.03,
    "replicates_decisions": 200,
    "replicates_shapley_ci": 60,
    "shapley": "exact over 4 players and 16 cells (24 orderings); sequential decompositions in orders RECAL,TRAIN,DIFF,LABEL and the reverse; CI half-width = half of the 2.5-97.5 percentile range of the bootstrap draws, averaged over replicates",
    "monte_carlo_error": "with 200 replicates the SE of a probability near 0.8 is about 0.028",
    "base_seed": 20261110,
}

A_P, A_S = ASSUMPTIONS["difficulty_loadings"]["a_P"], ASSUMPTIONS["difficulty_loadings"]["a_S"]
F_FP = 0.08
AUC_P, AUC_0 = 0.72, 0.60
HET_SD, SHOCK_SD = 0.3, 0.05 / 0.26
RHO = 0.5
PROBE_BINS = 128
BASE_SEED = ASSUMPTIONS["base_seed"]


def phi_inv(p):
    lo, hi = -10.0, 10.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if 0.5 * (1 + math.erf(mid / math.sqrt(2))) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


D_P = math.sqrt(2.0) * phi_inv(AUC_P)
D_0 = math.sqrt(2.0) * phi_inv(AUC_0)


# ---------------------------------------------------------------- problem set and model simulation
def draw_problems(rng, n):
    p = rng.beta(0.6, 0.5, size=n)
    pc = np.clip(p, 1e-3, 1 - 1e-3)
    lg = np.log(pc / (1 - pc))
    z = (lg - lg.mean()) / lg.std()
    w = np.exp(-0.5 * ((p - 0.5) / 0.15) ** 2)
    c = F_FP * (1 - p).sum() / max(((1 - p) * w).sum(), 1e-12)
    q = np.minimum(1.0, c * w)
    return p, z, q


def sim_model(rng, p, z, q, k, d1):
    n = len(p)
    y = rng.random((n, k)) < p[:, None]
    fp = (~y) & (rng.random((n, k)) < q[:, None])
    yw = y | fp
    het = rng.normal(0, HET_SD, n)
    shock = rng.normal(0, SHOCK_SD, n)
    dp = np.maximum(D_P + het + shock, 0.0)[:, None]
    ds0 = np.maximum(D_0 + het, 0.0)[:, None]
    ds1 = np.maximum(d1 + het, 0.0)[:, None]
    eP = rng.normal(size=(n, k))
    eS = RHO * eP + math.sqrt(1 - RHO**2) * rng.normal(size=(n, k))
    sP = dp * y + A_P * z[:, None] + eP
    base = A_S * z[:, None] + eS
    sS0 = ds0 * y + base
    sS1 = ds1 * y + base
    to_bin = lambda s: np.rint(10.0 / (1.0 + np.exp(-s))).astype(np.int64)
    return {"y": y, "yw": yw, "sP": sP, "b0": to_bin(sS0), "b1": to_bin(sS1)}


def pav_map(pos, tot):
    nb = len(tot)
    blocks = []
    for b in range(nb):
        if tot[b] > 0:
            blocks.append([float(pos[b]), float(tot[b]), [b]])
            while len(blocks) > 1 and blocks[-2][0] / blocks[-2][1] >= blocks[-1][0] / blocks[-1][1]:
                b2 = blocks.pop()
                blocks[-1][0] += b2[0]
                blocks[-1][1] += b2[1]
                blocks[-1][2] += b2[2]
    out = np.full(nb, np.nan)
    for s, t, mem in blocks:
        out[mem] = s / t
    if not blocks:
        return np.full(nb, 0.5)
    last = out[np.isfinite(out)][0]
    for b in range(nb):
        if np.isfinite(out[b]):
            last = out[b]
        else:
            out[b] = last
    return out


def recal(bins, lab, half):
    out = np.empty(bins.shape)
    for h in (0, 1):
        fit = half == h
        bf = bins[fit]
        tot = np.bincount(bf.ravel(), minlength=11)
        pos = np.bincount(bf[lab[fit]], minlength=11)
        m = pav_map(pos, tot)
        out[~fit] = m[bins[~fit]]
    return out


def nums_pairs(s, lab):
    d = s[:, :, None] - s[:, None, :]
    m = lab[:, :, None] & ~lab[:, None, :]
    num = ((d > 0) & m).sum((1, 2)) + 0.5 * ((d == 0) & m).sum((1, 2))
    return num.astype(float), m.sum((1, 2)).astype(float)


def counts(bins, lab, nb):
    n = bins.shape[0]
    flat = np.arange(n)[:, None] * nb + bins
    pos = np.bincount(flat[lab], minlength=n * nb).reshape(n, nb).astype(float)
    neg = np.bincount(flat[~lab], minlength=n * nb).reshape(n, nb).astype(float)
    return pos, neg


def pooled_auc(Wall, pos, neg):
    P = Wall @ pos
    N = Wall @ neg
    cum = np.cumsum(N, axis=1) - N
    return (P * (cum + 0.5 * N)).sum(1) / (P.sum(1) * N.sum(1))


def model_metrics(sim, Wall, full, half):
    """Return dict of metric arrays over rows of Wall (row 0 should be all ones = point estimate)."""
    res = {}
    labs = {1: sim["y"], 0: sim["yw"]}
    sP = sim["sP"]
    if full:
        edges = np.quantile(sP, np.arange(1, PROBE_BINS) / PROBE_BINS)
        pb = np.searchsorted(edges, sP)
    pair_cache = {}
    for l in ((0, 1) if full else (1,)):
        lab = labs[l]
        nP, pr = nums_pairs(sP, lab)
        pair_cache[l] = pr
        res[("P", l, 1)] = (Wall @ nP) / (Wall @ pr)
        if full:
            ps, ng = counts(pb, lab, PROBE_BINS)
            res[("P", l, 0)] = pooled_auc(Wall, ps, ng)
        for t in ((0, 1) if full else (1,)):
            bins = sim["b1"] if t else sim["b0"]
            for r in ((0, 1) if full else (1,)):
                if r:
                    vals = recal(bins, lab, half)
                else:
                    vals = bins.astype(float)
                nS, _ = nums_pairs(vals, lab)
                res[("S", t, r, l, 1)] = (Wall @ nS) / (Wall @ pr)
                if full:
                    u, inv = np.unique(vals, return_inverse=True)
                    ib = inv.reshape(vals.shape)
                    ps, ng = counts(ib, lab, len(u))
                    res[("S", t, r, l, 0)] = pooled_auc(Wall, ps, ng)
    return res, pair_cache[1]


def make_W(rng, n, B):
    idx = rng.integers(0, n, size=(B, n))
    flat = (idx + np.arange(B)[:, None] * n).ravel()
    W = np.bincount(flat, minlength=B * n).reshape(B, n).astype(float)
    return np.vstack([np.ones((1, n)), W])


# ---------------------------------------------------------------- Shapley and sequential decompositions
PLAYERS = ["RECAL", "TRAIN", "DIFF", "LABEL"]


def cell_gap(models_metrics, mask):
    r, t, d, l = [(mask >> i) & 1 for i in range(4)]
    g = 0
    for res in models_metrics:
        g = g + res[("P", l, d)] - res[("S", t, r, l, d)]
    return g / len(models_metrics)


def decompose(v):
    """v: list of 16 arrays indexed by bitmask. Returns dict of terms."""
    out = {"G0": v[0], "R": v[15]}
    fact = [math.factorial(i) for i in range(5)]
    for i in range(4):
        acc = 0
        for mask in range(16):
            if (mask >> i) & 1:
                continue
            s = bin(mask).count("1")
            w = fact[s] * fact[3 - s] / fact[4]
            acc = acc + w * (v[mask | (1 << i)] - v[mask])
        out["shapley_" + PLAYERS[i]] = acc
    for name, order in (("seq_fwd", [0, 1, 2, 3]), ("seq_rev", [3, 2, 1, 0])):
        mask = 0
        for i in order:
            out[f"{name}_{PLAYERS[i]}"] = v[mask | (1 << i)] - v[mask]
            mask |= 1 << i
    return out


# ---------------------------------------------------------------- calibration
def calibrate(task):
    k, R = task["k"], task["R"]
    n = 30000 if not QUICK else 8000
    seed = np.random.SeedSequence([BASE_SEED, 1, k])
    half = (np.arange(n) % 2)
    W = np.ones((1, n))

    def realized(d1, full=False):
        rng = np.random.default_rng(seed)
        p, z, q = draw_problems(rng, n)
        sim = sim_model(rng, p, z, q, k, d1)
        m, pr = model_metrics(sim, W, False, half)
        return float(m[("P", 1, 1)][0] - m[("S", 1, 1, 1, 1)][0]), sim, pr

    lo, hi = D_0, D_P + 1.0
    for _ in range(14):
        mid = 0.5 * (lo + hi)
        if realized(mid)[0] > R:
            lo = mid
        else:
            hi = mid
    d1 = 0.5 * (lo + hi)
    got, sim, pr = realized(d1)
    # realized within AUROC diagnostics (true labels, no recal)
    nP, _ = nums_pairs(sim["sP"], sim["y"])
    n0, _ = nums_pairs(sim["b0"].astype(float), sim["y"])
    n1, _ = nums_pairs(sim["b1"].astype(float), sim["y"])
    return {"k": k, "R_target": R, "d1": round(d1, 4), "R_achieved": round(got, 4),
            "within_auroc_probe": round(float(nP.sum() / pr.sum()), 4),
            "within_auroc_stated_zero_shot": round(float(n0.sum() / pr.sum()), 4),
            "within_auroc_stated_trained_norecal": round(float(n1.sum() / pr.sum()), 4),
            "calibration_problems": n}


# ---------------------------------------------------------------- grid cells
def run_decision_cell(task):
    M, k, n, R, d1, reps, B, idx = (task[x] for x in ("M", "k", "n", "R", "d1", "reps", "B", "idx"))
    rng = np.random.default_rng(np.random.SeedSequence([BASE_SEED, 2, idx]))
    half = np.arange(n) % 2
    los, his, pts, mixed = [], [], [], []
    for _ in range(reps):
        p, z, q = draw_problems(rng, n)
        Wall = make_W(rng, n, B)
        acc = 0
        mx = []
        for _m in range(M):
            sim = sim_model(rng, p, z, q, k, d1)
            m, pr = model_metrics(sim, Wall, False, half)
            acc = acc + (m[("P", 1, 1)] - m[("S", 1, 1, 1, 1)])
            mx.append((pr > 0).sum())
        acc = acc / M
        pts.append(acc[0])
        los.append(np.quantile(acc[1:], 0.05))
        his.append(np.quantile(acc[1:], 0.95))
        mixed.append(np.mean(mx))
    return {"M": M, "k": k, "n_problems": n, "R_true": R, "d1": d1, "reps": reps,
            "lo": np.array(los), "hi": np.array(his), "pt": np.array(pts), "mixed": float(np.mean(mixed))}


def dec_stats(lo, hi, delta):
    eq = (lo > -delta) & (hi < delta)
    sup = lo > delta
    return {"p_equivalence": round(float(eq.mean()), 3), "p_superiority": round(float(sup.mean()), 3),
            "p_inconclusive": round(float(1 - eq.mean() - sup.mean()), 3)}


def run_shapley_cell(task):
    M, k, n, R, d1, reps, B, idx = (task[x] for x in ("M", "k", "n", "R", "d1", "reps", "B", "idx"))
    rng = np.random.default_rng(np.random.SeedSequence([BASE_SEED, 3, idx]))
    half = np.arange(n) % 2
    pts, hws, mixed = {}, {}, []
    for _ in range(reps):
        p, z, q = draw_problems(rng, n)
        Wall = make_W(rng, n, B)
        mms = []
        mx = []
        for _m in range(M):
            sim = sim_model(rng, p, z, q, k, d1)
            m, pr = model_metrics(sim, Wall, True, half)
            mms.append(m)
            mx.append((pr > 0).sum())
        v = [cell_gap(mms, mask) for mask in range(16)]
        terms = decompose(v)
        for name, arr in terms.items():
            pts.setdefault(name, []).append(arr[0])
            lo, hi = np.quantile(arr[1:], [0.025, 0.975])
            hws.setdefault(name, []).append((hi - lo) / 2)
        mixed.append(np.mean(mx))
        pts.setdefault("cells", []).append([float(x[0]) for x in v])
    cells_mean = np.mean(pts.pop("cells"), axis=0)
    return {"M": M, "k": k, "n_problems": n, "R_true": R, "reps": reps, "B": B,
            "mean_mixed_problems_per_model": round(float(np.mean(mixed)), 1),
            "mean_point": {a: round(float(np.mean(b)), 4) for a, b in pts.items()},
            "mean_ci95_halfwidth": {a: round(float(np.mean(b)), 4) for a, b in hws.items()},
            "mean_cell_gap_by_mask": {"order_bits": "bit0 RECAL, bit1 TRAIN, bit2 DIFF, bit3 LABEL",
                                      "values": [round(float(c), 4) for c in cells_mean]}}


def dispatch(task):
    return run_shapley_cell(task) if task["kind"] == "shapley" else run_decision_cell(task)


def main():
    t0 = time.time()
    if QUICK:
        Ms, ks, ns, Rs = (1, 9), (10,), (542,), (0.0, 0.06)
        reps, reps_sh, B = 10, 3, 100
        sh_ns = (542,)
        out_name = "power_sim_quick.json"
    else:
        Ms, ks, ns, Rs = (1, 6, 9), (8, 10, 16), (542, 900, 1600), (0.0, 0.015, 0.03, 0.05, 0.06)
        reps, reps_sh, B = ASSUMPTIONS["replicates_decisions"], ASSUMPTIONS["replicates_shapley_ci"], 400
        sh_ns = (542, 1600)
        out_name = "power_sim.json"
    nproc = min(8, os.cpu_count() or 1)
    with Pool(nproc) as pool:
        cal_tasks = [{"k": k, "R": R} for k in ks for R in Rs]
        cal = pool.map(calibrate, cal_tasks)
        d1map = {(c["k"], c["R_target"]): c["d1"] for c in cal}
        print(f"calibration done {time.time() - t0:.0f}s", file=sys.stderr, flush=True)
        tasks = []
        idx = 0
        for M in Ms:
            for k in ks:
                for n in ns:
                    for R in Rs:
                        tasks.append({"kind": "dec", "M": M, "k": k, "n": n, "R": R, "d1": d1map[(k, R)],
                                      "reps": reps, "B": B, "idx": idx})
                        idx += 1
        sh_tasks = []
        for n in sh_ns:
            for R in (0.0, 0.06):
                sh_tasks.append({"kind": "shapley", "M": 9, "k": 10, "n": n, "R": R, "d1": d1map[(10, R)],
                                 "reps": reps_sh, "B": B, "idx": 1000 + len(sh_tasks)})
        alltasks = sorted(tasks + sh_tasks, key=lambda t: -(t["M"] * t["n"] * t["k"] * (4 if t["kind"] == "shapley" else 1)))
        results = pool.map(dispatch, alltasks, chunksize=1)
    dec = [r for r in results if "lo" in r]
    sh = [r for r in results if "lo" not in r]
    delta = ASSUMPTIONS["delta"]
    grid = []
    for r in sorted(dec, key=lambda r: (r["M"], r["k"], r["n_problems"], r["R_true"])):
        row = {x: r[x] for x in ("M", "k", "n_problems", "R_true", "d1", "reps")}
        row["mean_mixed_problems_per_model"] = round(r["mixed"], 1)
        row["mean_point_R"] = round(float(r["pt"].mean()), 4)
        row["mean_lower_bound"] = round(float(r["lo"].mean()), 4)
        row["mean_upper_bound"] = round(float(r["hi"].mean()), 4)
        row.update(dec_stats(r["lo"], r["hi"], delta))
        row["p_lower_bound_gt_0"] = round(float((r["lo"] > 0).mean()), 3)
        grid.append(row)
    sens = []
    for r in sorted(dec, key=lambda r: (r["n_problems"], r["R_true"])):
        if r["M"] == 9 and r["k"] == 10 and r["n_problems"] in (542, 1600):
            for dl in (0.02, 0.03, 0.05):
                sens.append({"M": 9, "k": 10, "n_problems": r["n_problems"], "R_true": r["R_true"], "delta": dl,
                             **dec_stats(r["lo"], r["hi"], dl)})
    # recommendation
    byk = {(g["M"], g["k"], g["n_problems"], g["R_true"]): g for g in grid}
    cands = []
    for k in ks:
        for n in ns:
            a, b = byk.get((9, k, n, 0.0)), byk.get((9, k, n, 0.06))
            if a and b and a["p_equivalence"] >= 0.80 and b["p_superiority"] >= 0.80:
                cands.append({"k": k, "n_problems": n, "total_samples_per_model": k * n,
                              "p_equivalence_R0": a["p_equivalence"], "p_superiority_R006": b["p_superiority"]})
    cands.sort(key=lambda c: (c["total_samples_per_model"], c["n_problems"]))
    rec = {"rule": "smallest k*n at M=9, delta 0.03, with P(equivalence | R=0) >= 0.80 and P(superiority | R=0.06) >= 0.80",
           "qualifying_cells": cands, "recommended": cands[0] if cands else "none in grid"}
    runtime = time.time() - t0
    doc = {"assumptions": ASSUMPTIONS, "calibration": cal, "bootstrap_draws_B": B,
           "numpy_version": np.__version__, "python_version": sys.version.split()[0], "quick": QUICK,
           "runtime_seconds": round(runtime, 1), "decision_grid": grid, "delta_sensitivity": sens,
           "shapley_ci_main_setting": sh, "recommendation": rec}
    path = Path(__file__).with_name(out_name)
    path.write_text(json.dumps(doc, indent=1) + "\n")
    print(f"wrote {path} in {runtime:.0f}s", file=sys.stderr)


if __name__ == "__main__":
    main()
