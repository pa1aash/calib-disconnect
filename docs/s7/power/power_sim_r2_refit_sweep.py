"""Supplement to power_sim_r2.py: n sweep (mixed-count curve) at reduced refit noise.
Run: python3 -I docs/s7/parts/power-B2/power_sim_r2_refit_sweep.py [--quick]
Reuses the functions of power_sim_r2.py unchanged. Nominal heterogeneity, kappa conservative, FE."""
import sys, json, time, os
from pathlib import Path
from multiprocessing import Pool
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import power_sim_r2 as P

def main():
    t0 = time.time()
    quick = "--quick" in sys.argv
    cfg = P.load_config(HERE / "config_models.json")
    kan = P.kappa_analysis()
    kap = min(r["kappa"] for r in kan.values())
    models = P.resolve_models(cfg, kap)
    M = len(models)
    sub = [i for i, m in enumerate(models) if m.get("refit_substudy")]
    W_N, REPS, B = (4, 3, 100) if quick else (40, 12, 500)
    ncal = {10: 3000 if quick else 20000, 20: 2000 if quick else 10000}
    ns = [150, 300] if quick else [100, 150, 200, 250, 300, 400, 542]
    scales = {"x0.5": (0.05, 0.025), "x0.25": (0.025, 0.0125)}
    Rl = [0.0, 0.04, -0.04, 0.06, -0.06]
    with Pool(8) as pool:
        ct = [{"het": "nominal", "kid": "k080", "kappa": kap, "k": k, "w": w, "ncal": ncal[k], "models": models} for k in (10, 20) for w in range(W_N)]
        cals = {(c["het"], c["kid"], c["k"], c["w"]): c for c in pool.imap_unordered(P.calib_world, ct, chunksize=1)}
        tasks = []
        for sc, (rl, rp) in scales.items():
            for k in (10, 20):
                for n in ns:
                    for w in range(W_N):
                        tasks.append({"key": (sc, k, n), "het": "nominal", "mode": "FE", "kid": "k080", "kappa": kap, "k": k, "n": n, "w": w,
                                      "reps": REPS, "B": B, "models": models, "cal": cals[("nominal", "k080", k, w)], "stream": 12,
                                      "rel_lora": rl, "rel_probe": rp, "sub": sub, "active": list(range(M)), "share_het": False, "R_list": Rl})
        tasks.sort(key=lambda t: -(t["n"] * t["k"] ** 2))
        groups = {}
        for r in pool.imap_unordered(P.run_group, tasks, chunksize=1):
            groups.setdefault(r["key"], []).append(r)
    out = {}
    for (sc, k, n), v in sorted(groups.items()):
        s = P.summarize(v, Rl)
        row = {"mean_mixed_per_model": s["mean_mixed_per_model"], "reps_total": s["reps_total"]}
        for d in (0.02, 0.03):
            b = s["by_R"]
            p = [b["0.0"][f"delta_{d}_widened"]["D1"], b[str(2 * d)][f"delta_{d}_widened"]["D2"], b[str(-2 * d)][f"delta_{d}_widened"]["D3"]]
            row[f"delta_{d}"] = {"D1": p[0], "D2": p[1], "D3": p[2], "min": min(p)}
        out[f"{sc}|k{k}|n{n}"] = row
    doc = {"purpose": "mixed-count curve at reduced refit noise", "refit_scales_rel_lora_rel_probe": scales,
           "settings": {"worlds": W_N, "reps_per_world": REPS, "B": B, "kappa": kap, "het": "nominal"}, "rows": out,
           "runtime_seconds": round(time.time() - t0, 1)}
    (HERE / ("power_r2_refit_sweep_quick.json" if quick else "power_r2_refit_sweep.json")).write_text(json.dumps(doc, indent=1, default=str) + "\n")
    print("done", round(time.time() - t0), file=sys.stderr)

if __name__ == "__main__":
    main()
