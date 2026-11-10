"""Sensitivity of the primary decision to gap shocks shared across models (wave 6 orchestrator).

The B9 simulation (power_sim.py) draws each model's per-problem gap shock independently,
which narrows the interval of the model-pooled residual. This script reruns the main
setting (M = 6, k = 10, n = 542) with a shock that is shared across models in a fraction
rho of its variance: shock_m = sqrt(rho) * shared + sqrt(1 - rho) * own_m.
Planning arithmetic under the B9 assumptions, not a result.

Run: python3 -I docs/s6/power/power_shared_shock.py
"""
import json
import math
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import power_sim as ps  # noqa: E402


def sim_model_shared(rng, p, z, q, k, d1, shared, rho):
    n = len(p)
    y = rng.random((n, k)) < p[:, None]
    fp = (~y) & (rng.random((n, k)) < q[:, None])
    yw = y | fp
    het = rng.normal(0, ps.HET_SD, n)
    own = rng.normal(0, ps.SHOCK_SD, n)
    shock = math.sqrt(rho) * shared + math.sqrt(1 - rho) * own
    dp = np.maximum(ps.D_P + het + shock, 0.0)[:, None]
    ds0 = np.maximum(ps.D_0 + het, 0.0)[:, None]
    ds1 = np.maximum(d1 + het, 0.0)[:, None]
    eP = rng.normal(size=(n, k))
    eS = ps.RHO * eP + math.sqrt(1 - ps.RHO**2) * rng.normal(size=(n, k))
    sP = dp * y + ps.A_P * z[:, None] + eP
    base = ps.A_S * z[:, None] + eS
    to_bin = lambda s: np.rint(10.0 / (1.0 + np.exp(-s))).astype(np.int64)
    return {"y": y, "yw": yw, "sP": sP, "b0": to_bin(ds0 * y + base), "b1": to_bin(ds1 * y + base)}


def cell(task):
    M, k, n, R, d1, rho, reps, B, idx = (task[x] for x in ("M", "k", "n", "R", "d1", "rho", "reps", "B", "idx"))
    rng = np.random.default_rng(np.random.SeedSequence([ps.BASE_SEED, 7, idx]))
    half = np.arange(n) % 2
    los, his = [], []
    for _ in range(reps):
        p, z, q = ps.draw_problems(rng, n)
        Wall = ps.make_W(rng, n, B)
        shared = rng.normal(0, ps.SHOCK_SD, n)
        acc = 0
        for _m in range(M):
            sim = sim_model_shared(rng, p, z, q, k, d1, shared, rho)
            m, _ = ps.model_metrics(sim, Wall, False, half)
            acc = acc + (m[("P", 1, 1)] - m[("S", 1, 1, 1, 1)])
        acc = acc / M
        los.append(np.quantile(acc[1:], 0.05))
        his.append(np.quantile(acc[1:], 0.95))
    lo, hi = np.array(los), np.array(his)
    out = {"M": M, "k": k, "n_problems": n, "R_true": R, "rho_shared": rho, "reps": reps, "B": B,
           "mean_lower_bound": round(float(lo.mean()), 4), "mean_upper_bound": round(float(hi.mean()), 4)}
    out.update(ps.dec_stats(lo, hi, ps.ASSUMPTIONS["delta"]))
    out["p_stated_superiority"] = round(float((hi < -ps.ASSUMPTIONS["delta"]).mean()), 3)
    out["by_delta"] = {str(dl): ps.dec_stats(lo, hi, dl) for dl in (0.01, 0.015, 0.02, 0.05)}
    return out


def main():
    t0 = time.time()
    b9 = json.loads((Path(__file__).parent / "power_sim.json").read_text())
    d1map = {(c["k"], c["R_target"]): c["d1"] for c in b9["calibration"]}
    tasks, idx = [], 0
    for rho in (0.0, 0.5, 1.0):
        for M in (6, 1):
            for R in (0.0, 0.03, 0.06):
                tasks.append({"M": M, "k": 10, "n": 542, "R": R, "d1": d1map[(10, R)], "rho": rho,
                              "reps": 100, "B": 400, "idx": idx})
                idx += 1
    with Pool(8) as pool:
        res = pool.map(cell, tasks, chunksize=1)
    doc = {"purpose": "shared-shock sensitivity of the primary decision (orchestrator, wave 6)",
           "base_assumptions": "power_sim.json ASSUMPTIONS", "results": res,
           "runtime_seconds": round(time.time() - t0, 1)}
    (Path(__file__).parent / "power_shared_shock.json").write_text(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(res, indent=0))


if __name__ == "__main__":
    main()
