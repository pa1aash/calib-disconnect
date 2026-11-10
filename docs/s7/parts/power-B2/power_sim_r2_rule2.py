"""R2 refit rule rerun (repeated cross-fitting). Imports power_sim_r2.py unchanged (R1-rule record kept).

R2 rule: every readout of every model (probe and trained LoRA readout) is fit under fold seeds 0, 1, 2 (EvalPlus suite).
Point estimate: Rbar = mean over models of the seed-mean of R_m. Bootstrap: seed-averaged Rbar per resample (same problem
resample for all seeds). sigma2_m = between-seed sample variance (ddof 1, 2 df) of R_m; s2_refit = (1/3)(1/M^2) sum_m sigma2_m.
Interval half-width sqrt(h^2 + (1.645 s_refit)^2) about the percentile-interval center. No sub-study branch.

Run: python3 -I docs/s7/parts/power-B2/power_sim_r2_rule2.py [--quick]
Output: power_r2_rule2.json (merged into power_r2.json / thresholds_r2.json by merge_rule2.py)
"""
import sys, json, math, time, os
from pathlib import Path
from multiprocessing import Pool
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import power_sim_r2 as P

QUICK = "--quick" in sys.argv
RL = [0.0, 0.02, 0.03, 0.04, 0.06, -0.04, -0.06]
RL_SWEEP = [0.0, 0.04, 0.06, -0.04, -0.06]


def ratio_m(Wall, num_mat, pr):
    den = Wall @ pr
    return (Wall @ num_mat) / np.where(den > 0, den, 1.0)[:, None]


def run_group2(task):
    het, kid, kap, k, n, w = (task[x] for x in ("het", "kid", "kappa", "k", "n", "w"))
    reps, B, models, cal = task["reps"], task["B"], task["models"], task["cal"]
    rel_L, rel_P, Rs = task["rel_lora"], task["rel_probe"], task["R_list"]
    world = P.make_world(het, w, models, fe=True)
    M = len(models)
    rng = np.random.default_rng(np.random.SeedSequence([P.BASE_SEED, task["stream"], P.HET_ID[het], P.KAPPA_ID[kid], k, n, w]))
    d1 = np.zeros((M, len(Rs)))
    nclip = 0
    for m in range(M):
        for ri, R in enumerate(Rs):
            d1[m, ri], cl = P.d1_for(cal["models"][m], cal["models"][m]["W_P"] - (R + world["u"][m]))
            nclip += cl
    out = np.full((reps, len(Rs), 7), np.nan)   # pt, L, U, Lw, Uw, s_refit, h
    mixed = np.zeros(reps)
    for rep in range(reps):
        p = P.draw_p_models(rng, n, models, kap)
        Wall = P.make_W(rng, n, B)
        epsP = rng.normal(0, rel_P, (M, 3))
        epsS = rng.normal(0, rel_L, (M, 3))
        boot = np.zeros((len(Rs), B + 1))
        sig2 = np.zeros(len(Rs))
        mx = 0
        for m in range(M):
            pm = p[:, m]
            z = P.std_logit(pm)
            y, het_, shock, eP, eS = P.draw_noise(rng, pm, k)
            base = world["aS"][m] * z[:, None] + eS
            dpb = np.maximum(world["D_P"][m] + het_ + shock, 0)
            nP = np.empty((n, 3))
            for s in range(3):
                sP = (dpb * (1 + epsP[m, s]))[:, None] * y + world["aP"][m] * z[:, None] + eP
                nP[:, s], pr = P.nums_pairs(sP, y)
            mx += (pr > 0).sum()
            WPb = ratio_m(Wall, nP, pr)             # (B+1, 3)
            WPavg = WPb.mean(1)
            for ri in range(len(Rs)):
                ds = np.maximum(d1[m, ri] + het_, 0)
                nS = np.empty((n, 3))
                for s in range(3):
                    sS = P.to_bin((ds * (1 + epsS[m, s]))[:, None] * y + base)
                    nS[:, s], _ = P.nums_pairs(sS, y)
                WSb = ratio_m(Wall, nS, pr)
                boot[ri] += WPavg - WSb.mean(1)
                sig2[ri] += np.var(WPb[0] - WSb[0], ddof=1)
        boot /= M
        mixed[rep] = mx / M
        for ri in range(len(Rs)):
            L, U = np.nanquantile(boot[ri, 1:], [0.05, 0.95])
            s_ref = math.sqrt(sig2[ri] / (3.0 * M * M))
            c, h = 0.5 * (L + U), 0.5 * (U - L)
            hw = math.sqrt(h * h + (P.Z90 * s_ref) ** 2)
            out[rep, ri] = [boot[ri, 0], L, U, c - hw, c + hw, s_ref, h]
    return {"key": task["key"], "w": w, "out": out, "mixed": mixed, "nclip": nclip,
            "true_mean_R": [float(Rs[ri]) for ri in range(len(Rs))]}


def summ2(results, Rs):
    res = sorted(results, key=lambda r: r["w"])
    out = {"n_worlds": len(res), "reps_total": int(sum(r["out"].shape[0] for r in res)),
           "mean_mixed_per_model": round(float(np.mean([r["mixed"].mean() for r in res])), 1), "by_R": {}}
    for ri, R in enumerate(Rs):
        A = [r["out"][:, ri, :] for r in res]
        allA = np.vstack(A)
        d = {"R_true": R, "mean_point": round(float(allA[:, 0].mean()), 4), "sd_point": round(float(allA[:, 0].std(ddof=1)), 4),
             "mean_halfwidth_bootstrap": round(float(allA[:, 6].mean()), 4),
             "rms_s_refit": round(float(np.sqrt((allA[:, 5] ** 2).mean())), 4),
             "mean_halfwidth_widened": round(float(((allA[:, 4] - allA[:, 3]) / 2).mean()), 4)}
        for delta in (0.02, 0.03):
            for tag, (Lc, Uc) in (("widened", (3, 4)), ("unwidened", (1, 2))):
                row = {}
                for nm, idx in (("D1", 0), ("D2", 1), ("D3", 2)):
                    xs = [P.rates(a[:, 0], a[:, Lc], a[:, Uc], delta)[idx] for a in A]
                    pooled = float(np.mean(np.concatenate(xs)))
                    row[nm] = round(pooled, 3)
                    row[nm + "_se_cluster"] = round(P.cluster_se(xs), 3)
                    row[nm + "_se_binom"] = round(math.sqrt(max(pooled * (1 - pooled), 1e-12) / sum(len(x) for x in xs)), 3)
                row["inconclusive"] = round(1 - row["D1"] - row["D2"] - row["D3"], 3)
                d[f"delta_{delta}_{tag}"] = row
        out["by_R"][str(R)] = d
    return out


def curve_row(s, tag="widened"):
    row = {"mean_mixed_per_model": s["mean_mixed_per_model"]}
    for dl in (0.02, 0.03):
        b = s["by_R"]
        v = [b["0.0"][f"delta_{dl}_{tag}"]["D1"], b[str(2 * dl)][f"delta_{dl}_{tag}"]["D2"], b[str(-2 * dl)][f"delta_{dl}_{tag}"]["D3"]]
        row[f"delta_{dl}"] = {"D1": v[0], "D2": v[1], "D3": v[2], "min": min(v)}
    return row


def crossing(rows, dl):
    xs = [r["mean_mixed_per_model"] for r in rows]; ys = [r[f"delta_{dl}"]["min"] for r in rows]; ns = [r["n"] for r in rows]
    for i in range(len(xs)):
        if ys[i] >= 0.90:
            if i == 0:
                return {"mixed": xs[0], "n": ns[0]}
            f = (0.90 - ys[i - 1]) / (ys[i] - ys[i - 1])
            return {"mixed": round(xs[i - 1] + f * (xs[i] - xs[i - 1]), 1), "n": round(ns[i - 1] + f * (ns[i] - ns[i - 1]), 1)}
    return None


def main():
    t0 = time.time()
    log = lambda s: print(f"[{time.time() - t0:6.0f}s] {s}", file=sys.stderr, flush=True)
    cfg = P.load_config(HERE / "config_models.json")
    kap = min(r["kappa"] for r in P.kappa_analysis().values())
    models = P.resolve_models(cfg, kap)
    W_H, REPS_H = (4, 3) if QUICK else (40, 12)
    W_S, REPS_S = (3, 3) if QUICK else (30, 10)
    B = 100 if QUICK else 500
    ncal = {10: 3000 if QUICK else 20000, 20: 2000 if QUICK else 10000}
    ns_sweep = [150, 300] if QUICK else [100, 150, 200, 250, 300, 400]
    hets = ["nominal"] if QUICK else ["nominal", "conservative"]
    base = {"kid": "k080", "kappa": kap, "B": B, "models": models}
    with Pool(int(os.environ.get("WORKERS", 8))) as pool:
        ct = [dict(base, het=h, k=k, w=w, ncal=ncal[k]) for h in hets for k in (10, 20) for w in range(W_H)]
        cals = {(c["het"], c["k"], c["w"]): c for c in pool.imap_unordered(P.calib_world, ct, chunksize=1)}
        log("calibration done")

        def mk(key, h, k, n, worlds, reps, stream, rl=0.10, rp=0.05, R_list=RL):
            return [dict(base, key=key, het=h, k=k, n=n, w=w, reps=reps, stream=stream, cal=cals[(h, k, w)], rel_lora=rl, rel_probe=rp, R_list=R_list)
                    for w in range(worlds)]
        tasks = []
        for h in hets:
            for k in (10, 20):
                tasks += mk(("head", h, k, 542), h, k, 542, W_H, REPS_H, 22)
                if not QUICK:
                    tasks += mk(("stress2", h, k, 542), h, k, 542, W_H, REPS_H, 22, 0.20, 0.10)
                for n in ns_sweep:
                    tasks += mk(("sweep", h, k, n), h, k, n, W_S, REPS_S, 23, R_list=RL_SWEEP)
        tasks.sort(key=lambda t: -(t["n"] * t["k"] ** 2 * t["reps"] * len(t["R_list"])))
        groups = {}
        for r in pool.imap_unordered(run_group2, tasks, chunksize=1):
            groups.setdefault(r["key"], []).append(r)
        log(f"groups done ({len(tasks)} tasks)")
        head = {"|".join(map(str, k)): summ2(v, RL) for k, v in groups.items() if k[0] in ("head", "stress2")}
        sweep = {}
        for h in hets:
            for k in (10, 20):
                rows = []
                for n in ns_sweep:
                    r = curve_row(summ2(groups[("sweep", h, k, n)], RL_SWEEP)); r["n"] = n; rows.append(r)
                hs = summ2(groups[("head", h, k, 542)], RL); r = curve_row(hs); r["n"] = 542; r["source"] = "headline cell (480 replicates)"; rows.append(r)
                sweep[f"{h}_k{k}"] = rows
        sweep_unw = {}
        for h in hets:
            for k in (10, 20):
                rows = []
                for n in ns_sweep:
                    r = curve_row(summ2(groups[("sweep", h, k, n)], RL_SWEEP), "unwidened"); r["n"] = n; rows.append(r)
                r = curve_row(summ2(groups[("head", h, k, 542)], RL), "unwidened"); r["n"] = 542; rows.append(r)
                sweep_unw[f"{h}_k{k}"] = rows
        thr = {}
        for name, rows in sweep.items():
            for dl in (0.02, 0.03):
                thr[f"{name}_delta{dl}"] = crossing(rows, dl) or {"not_reached": True, "max_min_power": max(r[f"delta_{dl}"]["min"] for r in rows), "largest_n": 542}
        # verification at crossings (separate stream 24, headline-size replicates)
        vt, vkeys = [], {}
        for key, c in thr.items():
            if "n" in c:
                h, k, dl = key.split("_")[0], int(key.split("_")[1][1:]), key.split("_delta")[1]
                nv = int(math.ceil(c["n"]))
                if (h, k, nv) not in vkeys:
                    vkeys[(h, k, nv)] = True
                    vt += mk(("verify", h, k, nv), h, k, nv, W_H, REPS_H, 24, R_list=RL_SWEEP)
        vg = {}
        for r in pool.imap_unordered(run_group2, vt, chunksize=1):
            vg.setdefault(r["key"], []).append(r)
        verify = {}
        for k_, v in vg.items():
            s = summ2(v, RL_SWEEP); r = curve_row(s); r["n"] = k_[3]; r["reps_total"] = s["reps_total"]
            verify[f"{k_[1]}_k{k_[2]}_n{k_[3]}"] = r
        log("verification done")
    doc = {"rule": "R2 repeated cross-fitting; see module docstring", "quick": QUICK,
           "settings": {"headline_worlds_x_reps": [W_H, REPS_H], "sweep_worlds_x_reps": [W_S, REPS_S], "B": B, "kappa": kap,
                        "refit_rel_lora_probe_primary": [0.10, 0.05], "stress_rel_lora_probe": [0.20, 0.10], "sweep_n": ns_sweep},
           "headline_n542": head, "sweep_widened": sweep, "sweep_unwidened": sweep_unw, "thresholds": thr, "verification": verify,
           "runtime_seconds": round(time.time() - t0, 1)}
    (HERE / ("power_r2_rule2_quick.json" if QUICK else "power_r2_rule2.json")).write_text(json.dumps(doc, indent=1, default=str) + "\n")
    log("wrote")


if __name__ == "__main__":
    main()
