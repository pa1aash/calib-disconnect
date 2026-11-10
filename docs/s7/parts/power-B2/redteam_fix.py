"""Corrects the k = 20 threshold in power_r2_redteam.json: the kappa sweep never fell below 0.90 (no bracketed crossing), so the
k = 20 largest bracketed crossing is the mu-sweep value (110.7); verify at the margin value T = 125 (separate seed stream 37).
Run: python3 -I docs/s7/parts/power-B2/redteam_fix.py"""
import sys, json, math
from pathlib import Path
from multiprocessing import Pool
import numpy as np
from scipy.optimize import brentq
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import power_sim_r2 as P
import power_sim_r2_redteam as R

def main():
    d = json.loads((HERE / "power_r2_redteam.json").read_text())
    cfg = P.load_config(HERE / "config_models.json")
    kap = min(r["kappa"] for r in P.kappa_analysis().values())
    models0 = P.resolve_models(cfg, kap)
    k, T = 20, 125
    def with_mu(o): return [dict(m, mu=float(np.clip(m["mu"] + o, 0.05, 0.995))) for m in models0]
    mm = lambda ms: 542 * float(np.mean([P.mixed_frac(m["mu"], kap, k) for m in ms]))
    o = brentq(lambda o: mm(with_mu(o)) - T, -0.3, 0.27)
    ms = with_mu(o)
    with Pool(8) as pool:
        cal = {c["w"]: c for c in pool.map(R.calib2, [{"het": "nominal", "kid": "k080", "kappa": kap, "k": k, "w": w, "ncal": 10000, "models": ms} for w in range(40)], chunksize=1)}
        tasks = [{"key": ("verify", k, T), "het": "nominal", "kappa": kap, "k": k, "n": 542, "w": w, "reps": 12, "B": 500, "models": ms, "cal": cal[w],
                  "stream": 37, "R_list": R.R3, "rho_e": 0.5, "rel_lora": 0.10, "rel_probe": 0.05} for w in range(40)]
        res = list(pool.imap_unordered(R.run3, tasks, chunksize=1))
    s = R.summ(res, R.R3)
    v = dict(R.minpow(s), mixed=s["mean_mixed_per_model"], pairs=s["mean_pairs_per_model"], reps=s["reps_total"], mu_offset=round(o, 4))
    d["T_corrected"] = {
        "k10": {"bracketed_crossings_vs_mixed": {"n_sweep": 143.1, "mu_sweep": 167.7}, "not_bracketed": {"kappa_sweep": "min power >= 0.90 at every kappa tested (mixed 152.7 to 233.4)"},
                "T10": 185, "verification": d["verification"]["k10_T185"]},
        "k20": {"bracketed_crossings_vs_mixed": {"mu_sweep": 110.7}, "not_bracketed": {"n_sweep": "min power >= 0.90 at every n tested (mixed 76.6 to 277.6)", "kappa_sweep": "min power >= 0.90 at every kappa tested (mixed 186.0 to 277.6)"},
                "T20": T, "verification": v, "superseded": "the k20 entry under T (205, from the unbracketed kappa sweep) and verification k20_T205 are superseded"}}
    (HERE / "power_r2_redteam.json").write_text(json.dumps(d, indent=1, default=str) + "\n")
    print(v)

if __name__ == "__main__":
    main()
