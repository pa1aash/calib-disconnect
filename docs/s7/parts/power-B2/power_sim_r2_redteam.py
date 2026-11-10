"""Red-team follow-up under the R2 refit rule (repeated cross-fitting). Imports power_sim_r2.py unchanged.

Adds: (1) widening multiplier t_{12,0.95} = 1.782 (both 1.645 and 1.782 reported); (2) mu and kappa scenarios at n = 542 and an n sweep,
min power versus mean mixed count and mean pass-fail pairs; thresholds T10, T20 with verification; (3) heterogeneous mixed counts
(one model at about 60 mixed) and residual-error correlation rho_e in {0.2, 0.8}.
Run: python3 -I docs/s7/parts/power-B2/power_sim_r2_redteam.py [--quick]     Output: power_r2_redteam.json
"""
import sys, json, math, time, os
from pathlib import Path
from multiprocessing import Pool
import numpy as np
from scipy.optimize import brentq
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import power_sim_r2 as P

QUICK = "--quick" in sys.argv
RL = [0.0, 0.02, 0.03, 0.04, 0.06, -0.04, -0.06]
R3 = [0.0, 0.06, -0.06]
ZS = {"z1.645": 1.645, "t1.782": 1.782}


def ratio_m(Wall, num_mat, pr):
    den = Wall @ pr
    return (Wall @ num_mat) / np.where(den > 0, den, 1.0)[:, None]


def calib2(task):
    P.RHO_E = task.get("rho_e", 0.5)
    return P.calib_world(task)


def run3(task):
    P.RHO_E = task.get("rho_e", 0.5)
    het, kap, k, n, w = (task[x] for x in ("het", "kappa", "k", "n", "w"))
    reps, B, models, cal, Rs = task["reps"], task["B"], task["models"], task["cal"], task["R_list"]
    world = P.make_world(het, w, models, fe=True)
    M = len(models)
    rng = np.random.default_rng(np.random.SeedSequence([P.BASE_SEED, task["stream"], w]))
    d1 = np.zeros((M, len(Rs)))
    for m in range(M):
        for ri, R in enumerate(Rs):
            d1[m, ri], _ = P.d1_for(cal["models"][m], cal["models"][m]["W_P"] - (R + world["u"][m]))
    out = np.full((reps, len(Rs), 5), np.nan)   # pt, L, U, s_refit, h
    mixed = np.zeros((reps, M))
    pairs = np.zeros((reps, M))
    for rep in range(reps):
        p = P.draw_p_models(rng, n, models, kap)
        Wall = P.make_W(rng, n, B)
        epsP = rng.normal(0, task["rel_probe"], (M, 3))
        epsS = rng.normal(0, task["rel_lora"], (M, 3))
        boot = np.zeros((len(Rs), B + 1))
        sig2 = np.zeros(len(Rs))
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
            mixed[rep, m] = (pr > 0).sum()
            pairs[rep, m] = pr.sum()
            WPb = ratio_m(Wall, nP, pr)
            WPavg = WPb.mean(1)
            for ri in range(len(Rs)):
                ds = np.maximum(d1[m, ri] + het_, 0)
                nS = np.empty((n, 3))
                for s in range(3):
                    nS[:, s], _ = P.nums_pairs(P.to_bin((ds * (1 + epsS[m, s]))[:, None] * y + base), y)
                WSb = ratio_m(Wall, nS, pr)
                boot[ri] += WPavg - WSb.mean(1)
                sig2[ri] += np.var(WPb[0] - WSb[0], ddof=1)
        boot /= M
        for ri in range(len(Rs)):
            L, U = np.nanquantile(boot[ri, 1:], [0.05, 0.95])
            out[rep, ri] = [boot[ri, 0], L, U, math.sqrt(sig2[ri] / (3.0 * M * M)), 0.5 * (U - L)]
    return {"key": task["key"], "w": w, "out": out, "mixed": mixed, "pairs": pairs}


def decide(a, delta, z):
    pt, L, U, s, h = (a[:, i] for i in range(5))
    if z is None:
        Lw, Uw = L, U
    else:
        c = 0.5 * (L + U)
        hw = np.sqrt(h * h + (z * s) ** 2)
        Lw, Uw = c - hw, c + hw
    return (Lw > -delta) & (Uw < delta), Lw > delta, Uw < -delta


def summ(results, Rs):
    res = sorted(results, key=lambda r: r["w"])
    out = {"n_worlds": len(res), "reps_total": int(sum(r["out"].shape[0] for r in res)),
           "mean_mixed_per_model": round(float(np.mean([r["mixed"].mean() for r in res])), 1),
           "mixed_per_model_vector": [round(float(x), 1) for x in np.mean([r["mixed"].mean(0) for r in res], axis=0)],
           "mean_pairs_per_model": round(float(np.mean([r["pairs"].mean() for r in res])), 0),
           "by_R": {}}
    for ri, R in enumerate(Rs):
        A = [r["out"][:, ri, :] for r in res]
        allA = np.vstack(A)
        d = {"mean_point": round(float(allA[:, 0].mean()), 4), "sd_point": round(float(allA[:, 0].std(ddof=1)), 4),
             "mean_h": round(float(allA[:, 4].mean()), 4), "rms_s_refit": round(float(np.sqrt((allA[:, 3] ** 2).mean())), 4)}
        for delta in (0.02, 0.03):
            for tag, z in (("unwidened", None), ("z1.645", 1.645), ("t1.782", 1.782)):
                row = {}
                for nm, idx in (("D1", 0), ("D2", 1), ("D3", 2)):
                    xs = [decide(a, delta, z)[idx] for a in A]
                    pooled = float(np.mean(np.concatenate(xs)))
                    row[nm] = round(pooled, 3)
                    row[nm + "_se"] = round(max(P.cluster_se(xs), math.sqrt(max(pooled * (1 - pooled), 1e-12) / sum(len(x) for x in xs))), 3)
                row["inconclusive"] = round(1 - row["D1"] - row["D2"] - row["D3"], 3)
                d[f"delta_{delta}_{tag}"] = row
        out["by_R"][str(R)] = d
    return out


def minpow(s, delta=0.03, tag="t1.782"):
    b = s["by_R"]
    v = [b["0.0"][f"delta_{delta}_{tag}"]["D1"], b[str(2 * delta)][f"delta_{delta}_{tag}"]["D2"], b[str(-2 * delta)][f"delta_{delta}_{tag}"]["D3"]]
    return {"D1": v[0], "D2": v[1], "D3": v[2], "min": min(v)}


def crossing(pts, xkey):
    """pts: list of dicts with xkey and 'min'; first upward crossing of 0.90 scanning from the smallest x."""
    pts = sorted(pts, key=lambda r: r[xkey])
    for i in range(len(pts)):
        if pts[i]["min"] >= 0.90:
            if i == 0:
                return {xkey: pts[0][xkey], "note": "already at 0.90 at the smallest x tested"}
            f = (0.90 - pts[i - 1]["min"]) / (pts[i]["min"] - pts[i - 1]["min"])
            return {xkey: round(pts[i - 1][xkey] + f * (pts[i][xkey] - pts[i - 1][xkey]), 1)}
    return None


def main():
    t0 = time.time()
    log = lambda s: print(f"[{time.time() - t0:6.0f}s] {s}", file=sys.stderr, flush=True)
    cfg = P.load_config(HERE / "config_models.json")
    kap0 = min(r["kappa"] for r in P.kappa_analysis().values())
    models0 = P.resolve_models(cfg, kap0)
    M = len(models0)
    W_H, REPS = (4, 3) if QUICK else (40, 12)
    W_S = 3 if QUICK else 20
    B = 100 if QUICK else 500
    ncal = {10: (3000 if QUICK else 20000), 20: (2000 if QUICK else 10000)}
    ncal_sc = {10: (3000 if QUICK else 12000), 20: (2000 if QUICK else 6000)}
    hets = ["nominal", "conservative"]

    def with_mu(offset=0.0, override=None):
        ms = []
        for i, m in enumerate(models0):
            mm = dict(m); mm["mu"] = float(np.clip(m["mu"] + offset, 0.05, 0.995))
            if override and i in override: mm["mu"] = override[i]
            ms.append(mm)
        return ms

    def mean_mixed(models, kap, k, n=542):
        return n * float(np.mean([P.mixed_frac(m["mu"], kap, k) for m in models]))

    def solve_offset(target, kap, k):
        return brentq(lambda o: mean_mixed(with_mu(o), kap, k) - target, -0.3, 0.27)

    scen = []   # (name, k, models, kap)
    for k, targets in ((10, [200, 170, 140, 120, 100]), (20, [230, 190, 150, 120, 95, 75])):
        for t in targets:
            o = solve_offset(t, kap0, k)
            scen.append((f"mu_k{k}_target{t}", k, with_mu(o), kap0, {"mu_offset": round(o, 4), "target_mixed": t}))
        for kp in (0.4, 0.5, 0.6, 0.7):
            scen.append((f"kappa_k{k}_{kp}", k, models0, kp, {"kappa": kp}))
    if QUICK:
        scen = scen[:2]
    # heterogeneous counts: model index 3 reduced to about 60 mixed at k = 10
    mu_low = brentq(lambda mu: 542 * P.mixed_frac(mu, kap0, 10) - 60.0, 0.5, 0.9999)
    models_het = with_mu(0.0, {3: mu_low})
    hc_info = {"model_index": 3, "mu_low": round(mu_low, 5), "analytic_mixed_per_model": [round(542 * P.mixed_frac(m["mu"], kap0, 10), 1) for m in models_het]}

    def mk(key, h, k, n, models, kap, worlds, cals, stream, R_list, rho_e=0.5, rl=0.10, rp=0.05):
        return [{"key": key, "het": h, "kappa": kap, "k": k, "n": n, "w": w, "reps": REPS, "B": B, "models": models, "cal": cals[w],
                 "stream": stream, "R_list": R_list, "rho_e": rho_e, "rel_lora": rl, "rel_probe": rp} for w in range(worlds)]

    with Pool(int(os.environ.get("WORKERS", 8))) as pool:
        # calibrations
        def do_cals(specs):
            tasks = [{"het": h, "kid": "k080", "kappa": kap, "k": k, "w": w, "ncal": nc, "models": ms, "tag": tag}
                     for (tag, h, k, ms, kap, nc, worlds) in specs for w in range(worlds)]
            tasks.sort(key=lambda t: -t["k"])
            res = {}
            for c in pool.imap_unordered(calib2, tasks, chunksize=1):
                pass
            return None
        # (calib_world does not return the tag; run per spec to keep association)
        cal = {}
        specs = [((h, k), h, k, models0, kap0, ncal[k], W_H) for h in hets for k in (10, 20)]
        specs += [(("hetcount", h), h, 10, models_het, kap0, ncal[10], W_H) for h in hets]
        specs += [(("scen", nm, "nominal"), "nominal", k, ms, kp, ncal_sc[k], W_S) for (nm, k, ms, kp, _) in scen]
        alltasks = []
        for (tag, h, k, ms, kp, nc, worlds) in specs:
            for w in range(worlds):
                alltasks.append((tag, {"het": h, "kid": "k080", "kappa": kp, "k": k, "w": w, "ncal": nc, "models": ms}))
        order = sorted(range(len(alltasks)), key=lambda i: -alltasks[i][1]["k"] * alltasks[i][1]["ncal"])
        outs = pool.map(calib2, [alltasks[i][1] for i in order], chunksize=1)
        for i, o in zip(order, outs):
            cal.setdefault(alltasks[i][0], {})[alltasks[i][1]["w"]] = o
        log("calibration done")
        tasks = []
        for h in hets:
            for k in (10, 20):
                tasks += mk(("head", h, k), h, k, 542, models0, kap0, W_H, cal[(h, k)], 31, RL)
        for h in hets:
            tasks += mk(("hetcount", h), h, 10, 542, models_het, kap0, W_H, cal[("hetcount", h)], 32, R3)
        for rho in (0.2, 0.8):
            tasks += mk(("rho", "nominal", 10, rho), "nominal", 10, 542, models0, kap0, W_H, cal[("nominal", 10)], 33, R3, rho_e=rho)
            tasks += mk(("rho", "conservative", 10, rho), "conservative", 10, 542, models0, kap0, W_H, cal[("conservative", 10)], 33, R3, rho_e=rho)
            tasks += mk(("rho", "nominal", 20, rho), "nominal", 20, 542, models0, kap0, W_H, cal[("nominal", 20)], 33, R3, rho_e=rho)
        ns = [150, 250] if QUICK else [150, 200, 250, 300, 400]
        for k in (10, 20):
            for n in ns:
                tasks += mk(("nsweep", k, n), "nominal", k, n, models0, kap0, W_S, cal[("nominal", k)], 34, R3)
        for (nm, k, ms, kp, info) in scen:
            tasks += mk(("scen", nm), "nominal", k, 542, ms, kp, W_S, cal[("scen", nm, "nominal")], 35, R3)
        tasks.sort(key=lambda t: -(t["n"] * t["k"] ** 2 * t["reps"] * len(t["R_list"])))
        groups = {}
        for r in pool.imap_unordered(run3, tasks, chunksize=1):
            groups.setdefault(r["key"], []).append(r)
        log(f"groups done ({len(tasks)} tasks)")
        S = {k: summ(v, RL if k[0] == "head" else R3) for k, v in groups.items()}

        # curves and crossings (delta 0.03, t = 1.782)
        def pt_of(s, **extra):
            d = minpow(s); d.update(mixed=s["mean_mixed_per_model"], pairs=s["mean_pairs_per_model"], reps=s["reps_total"]); d.update(extra); return d
        curves = {}
        thr = {}
        for k in (10, 20):
            base = pt_of(S[("head", "nominal", k)], source="headline n=542, 480 replicates")
            nsw = [pt_of(S[("nsweep", k, n)], n=n) for n in ns] + [dict(base, n=542)]
            sc_mu = [pt_of(S[("scen", nm)], scen=nm, **info) for (nm, kk, ms, kp, info) in scen if kk == k and nm.startswith("mu")] + [dict(base, scen="baseline")]
            sc_ka = [pt_of(S[("scen", nm)], scen=nm, **info) for (nm, kk, ms, kp, info) in scen if kk == k and nm.startswith("kappa")] + [dict(base, scen="baseline", kappa=round(kap0, 3))]
            curves[f"k{k}"] = {"n_sweep": nsw, "mu_sweep": sc_mu, "kappa_sweep": sc_ka}
            thr[f"k{k}"] = {}
            for nm, pts in (("n_sweep", nsw), ("mu_sweep", sc_mu), ("kappa_sweep", sc_ka)):
                thr[f"k{k}"][nm] = {"vs_mixed": crossing(pts, "mixed"), "vs_pairs": crossing(pts, "pairs")}
        # verification at margin-adjusted T
        Tinfo = {}
        vtasks = []
        for k in (10, 20):
            raws = []
            for nm in ("n_sweep", "mu_sweep", "kappa_sweep"):
                c = thr[f"k{k}"][nm]["vs_mixed"]
                if c and "mixed" in c: raws.append((c["mixed"], nm))
            if not raws:
                Tinfo[f"k{k}"] = {"status": "no crossing in any sweep"}; continue
            raw, which = max(raws)
            T = int(math.ceil(raw * 1.10 / 5.0) * 5)
            Tinfo[f"k{k}"] = {"crossings_vs_mixed": {nm: c for c, nm in raws} if False else {nm: c for c, nm in raws}, "largest": raw, "from": which, "T_rounded_up_with_10pct_margin": T}
            o = solve_offset(T, kap0, k)
            ms = with_mu(o)
            vt = [{"het": "nominal", "kid": "k080", "kappa": kap0, "k": k, "w": w, "ncal": ncal[k], "models": ms} for w in range(W_H)]
            vc = {o_["w"]: o_ for o_ in pool.map(calib2, vt, chunksize=1)}
            vtasks += mk(("verify", k, T), "nominal", k, 542, ms, kap0, W_H, vc, 36, R3)
            Tinfo[f"k{k}"]["verification_mu_offset"] = round(o, 4)
        vg = {}
        for r in pool.imap_unordered(run3, vtasks, chunksize=1):
            vg.setdefault(r["key"], []).append(r)
        verify = {}
        for key, v in vg.items():
            s = summ(v, R3); verify[f"k{key[1]}_T{key[2]}"] = dict(minpow(s), mixed=s["mean_mixed_per_model"], pairs=s["mean_pairs_per_model"], reps=s["reps_total"])
        log("verification done")
    doc = {"purpose": "red-team follow-up under the R2 refit rule", "quick": QUICK,
           "settings": {"headline_worlds_x_reps": [W_H, REPS], "sweep_worlds_x_reps": [W_S, REPS], "B": B, "kappa": kap0,
                        "refit_rel_lora_probe": [0.10, 0.05], "t_12_0.95": 1.782, "scenario_het": "nominal"},
           "headline": {"|".join(map(str, k)): v for k, v in S.items() if k[0] == "head"},
           "hetcount": {"info": hc_info, **{"|".join(map(str, k)): v for k, v in S.items() if k[0] == "hetcount"}},
           "rho_e": {"|".join(map(str, k)): v for k, v in S.items() if k[0] == "rho"},
           "scenario_info": {nm: dict(info, k=k, kappa=kp, mean_mu=round(float(np.mean([m['mu'] for m in ms])), 4),
                                      analytic_mixed=round(mean_mixed(ms, kp, k), 1)) for (nm, k, ms, kp, info) in scen},
           "curves": curves, "crossings": thr, "T": Tinfo, "verification": verify, "runtime_seconds": round(time.time() - t0, 1)}
    (HERE / ("power_r2_redteam_quick.json" if QUICK else "power_r2_redteam.json")).write_text(json.dumps(doc, indent=1, default=str) + "\n")
    log("wrote")


if __name__ == "__main__":
    main()
