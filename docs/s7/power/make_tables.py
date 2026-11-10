"""Reads power_r2.json and power_r2_refit_sweep.json; writes tables_generated.md and thresholds_r2.json. No new simulation."""
import json
from pathlib import Path
H = Path(__file__).resolve().parent
d = json.loads((H / "power_r2.json").read_text())
s = json.loads((H / "power_r2_refit_sweep.json").read_text())
G = d["groups"]
L = []
def cell(key, delta, tag="widened"):
    b = G[key]["by_R"]
    out = {}
    for nm, R in (("D1", 0.0), ("D2", 2 * delta), ("D3", -2 * delta)):
        c = b[str(round(R, 3) if R else 0.0)][f"delta_{delta}_{tag}"]
        out[nm] = (c[nm], max(c[nm + "_se_cluster"], c[nm + "_se_binom"]))
    cb = b[str(delta)][f"delta_{delta}_{tag}"]
    out["inc"] = cb["inconclusive"]; out["bD1"] = cb["D1"]; out["bD2"] = cb["D2"]; out["bD3"] = cb["D3"]
    return out
def fmt(c):
    return f"{c['D1'][0]:.3f} ({c['D1'][1]:.3f}) | {c['D2'][0]:.3f} ({c['D2'][1]:.3f}) | {c['D3'][0]:.3f} ({c['D3'][1]:.3f}) | {min(c[x][0] for x in ('D1','D2','D3')):.3f}"
L.append("### T1. Power at n = 542 (widened by the refit rule; SE in parentheses = larger of binomial and cluster-over-worlds SE)\n")
L.append("| Heterogeneity | k | delta | mean mixed per model | D1 at R=0 | D2 at R=+2delta | D3 at R=-2delta | min | min unwidened | P(inconclusive) at R=delta | P(D1) at R=delta |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|")
for h in ("nominal", "conservative", "extreme"):
    for k in (10, 20):
        key = f"main|{h}|FE|k080|{k}|542"
        for dl in (0.02, 0.03):
            c, u = cell(key, dl), cell(key, dl, "unwidened")
            L.append(f"| {h} | {k} | {dl} | {G[key]['mean_mixed_per_model']} | {fmt(c)} | {min(u[x][0] for x in ('D1','D2','D3')):.3f} | {c['inc']:.3f} | {c['bD1']:.3f} |")
L.append("\n### T2. Sweep over n (mean mixed count per model), widened, kappa 0.80, delta = 0.03 then 0.02: D1 / D2 / D3\n")
L.append("| Heterogeneity | k | n | mean mixed | delta 0.03 D1 / D2 / D3 | min | delta 0.02 D1 / D2 / D3 | min |")
L.append("|---|---|---|---|---|---|---|---|")
for name, cur in d["threshold_curves_widened"].items():
    h, k = name.split("_")
    for r in cur:
        a, b = r["delta_0.03"], r["delta_0.02"]
        L.append(f"| {h} | {k[1:]} | {r['n']} | {r['mean_mixed_per_model']} | {a['D1']:.3f} / {a['D2']:.3f} / {a['D3']:.3f} | {a['min']:.3f} | {b['D1']:.3f} / {b['D2']:.3f} / {b['D3']:.3f} | {b['min']:.3f} |")
# thresholds
def crossing(rows, delta):
    xs = [r["mean_mixed_per_model"] for r in rows]; ys = [r[f"delta_{delta}"]["min"] for r in rows]; ns = [r["n"] for r in rows]
    for i in range(len(xs)):
        if ys[i] >= 0.90:
            if i == 0: return {"mixed": xs[0], "n": ns[0]}
            f = (0.90 - ys[i-1]) / (ys[i] - ys[i-1])
            return {"mixed": round(xs[i-1] + f * (xs[i] - xs[i-1]), 1), "n": round(ns[i-1] + f * (ns[i] - ns[i-1]), 1)}
    return None
thr = {"rule": "linear interpolation of the min-over-decisions power on the sweep, first crossing of 0.90; None = not reached on the sweep (max n 900 for the main sweep, 542 for the reduced-refit sweep)", "main_refit_rel_lora_0.10": {}, "reduced_refit": {}}
for name, cur in d["threshold_curves_widened"].items():
    for dl in (0.02, 0.03):
        thr["main_refit_rel_lora_0.10"][f"{name}_delta{dl}"] = crossing(cur, dl) or {"not_reached": True, "max_min_power": max(r[f"delta_{dl}"]["min"] for r in cur)}
for sc in ("x0.5", "x0.25"):
    for k in (10, 20):
        cur = [dict(v, n=int(key.split("|n")[1])) for key, v in s["rows"].items() if key.startswith(f"{sc}|k{k}|")]
        cur.sort(key=lambda r: r["n"])
        for dl in (0.02, 0.03):
            thr["reduced_refit"][f"{sc}_k{k}_delta{dl}"] = crossing(cur, dl) or {"not_reached": True, "max_min_power": max(r[f"delta_{dl}"]["min"] for r in cur)}
thr["verification_runs"] = {k: {"mean_mixed": v["mean_mixed_per_model"], "D1_R0_delta0.03": v["by_R"]["0.0"]["delta_0.03_widened"]["D1"],
    "D2_R0.06": v["by_R"]["0.06"]["delta_0.03_widened"]["D2"], "D3_R-0.06": v["by_R"]["-0.06"]["delta_0.03_widened"]["D3"], "reps": v["reps_total"]} for k, v in d["threshold_verification"].items()}
(H / "thresholds_r2.json").write_text(json.dumps(thr, indent=1) + "\n")
L.append("\n### T3. Mixed-count thresholds for min-power 0.90 (from thresholds_r2.json)\n")
L.append("| Refit noise (rel SD LoRA / probe) | Heterogeneity | k | delta | mean mixed per model at 0.90 | equivalent n |")
L.append("|---|---|---|---|---|---|")
for k_, v in thr["main_refit_rel_lora_0.10"].items():
    h, kk, dl = k_.split("_"); 
    L.append(f"| 0.10 / 0.05 | {h} | {kk[1:]} | {dl[5:]} | " + (f"{v['mixed']} | {v['n']}" if "mixed" in v else f"not reached (max min-power {v['max_min_power']:.3f} at the largest n)") + " |")
for k_, v in thr["reduced_refit"].items():
    sc, kk, dl = k_.split("_")
    rr = "0.05 / 0.025" if sc == "x0.5" else "0.025 / 0.0125"
    L.append(f"| {rr} | nominal | {kk[1:]} | {dl[5:]} | " + (f"{v['mixed']} | {v['n']}" if "mixed" in v else f"not reached (max min-power {v['max_min_power']:.3f} at n = 542)") + " |")
L.append("\nVerification runs at an interpolated n (800 replicates, separate seed stream 13):\n")
for k_, v in thr["verification_runs"].items():
    L.append(f"- {k_}: mean mixed {v['mean_mixed']}; delta 0.03: D1 {v['D1_R0_delta0.03']}, D2 {v['D2_R0.06']}, D3 {v['D3_R-0.06']} ({v['reps']} replicates)")
L.append("\n### T4. Sensitivities and stress tests at n = 542, delta = 0.03 then 0.02 (D1 | D2 | D3 | min; widened)\n")
L.append("| Variant | k | mean mixed | delta 0.03 D1 | D2 | D3 | min | delta 0.02 D1 | D2 | D3 | min |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|")
variants = [("main (nominal)", "main|nominal|FE|k080|{k}|542"), ("random effects, nominal (sensitivity only)", "RE|nominal|RE|k080|{k}|542"),
            ("random effects, conservative (sensitivity only)", "RE|conservative|RE|k080|{k}|542"),
            ("kappa 1.835 (Qwen anchor)", "kappa183|nominal|FE|k183|{k}|542"), ("kappa 0.40 (stress)", "kappa040|nominal|FE|k040|{k}|542"),
            ("no refit noise", "stress_no_refit|nominal|FE|k080|{k}|542"), ("refit noise x0.25", "stress_refit_x0.25|nominal|FE|k080|{k}|542"),
            ("refit noise x0.5", "stress_refit_x0.5|nominal|FE|k080|{k}|542"), ("LoRA refit noise only (probe noise 0)", "stress_lora_only_x1|nominal|FE|k080|{k}|542"),
            ("refit noise x2", "stress_refit_x2|nominal|FE|k080|{k}|542"),
            ("problem-level het and shock shared by all models", "stress_shared_problem_shock|nominal|FE|k080|{k}|542"),
            ("M = 1 (one model, mu 0.80)", "stress_M1|nominal|FE|k080|{k}|542")]
for nm, kt in variants:
    for k in (10, 20):
        key = kt.format(k=k); a, b = cell(key, 0.03), cell(key, 0.02)
        f3 = lambda c: " | ".join(f"{c[x][0]:.3f}" for x in ("D1", "D2", "D3")) + f" | {min(c[x][0] for x in ('D1','D2','D3')):.3f}"
        L.append(f"| {nm} | {k} | {G[key]['mean_mixed_per_model']} | {f3(a)} | {f3(b)} |")
L.append("\n### T5. Interval components at n = 542, nominal, R = 0 (means over replicates)\n")
L.append("| k | SD of point estimate | bootstrap half-width h | s_refit probe part | s_refit LoRA part (scaled by 3) | widened half-width |")
L.append("|---|---|---|---|---|---|")
for k in (10, 20):
    b = G[f"main|nominal|FE|k080|{k}|542"]["by_R"]["0.0"]
    L.append(f"| {k} | {b['sd_point']} | {b['mean_halfwidth_bootstrap']} | {b['mean_s_refit_probe']} | {b['mean_s_refit_lora_scaled']} | {b['mean_halfwidth_widened']} |")
L.append("\n### T6. Shapley terms at M = 6, k = 10, n = 542, true R = 0 (B = 300, 8 worlds x 4 replicates; 95 percent percentile half-widths, no refit widening)\n")
L.append("| Heterogeneity | Term | mean point | 95% half-width | between-model SD of per-model point |")
L.append("|---|---|---|---|---|")
for sh in d["shapley_M6"]:
    for t in sh["mean_point"]:
        L.append(f"| {sh['het']} | {t} | {sh['mean_point'][t]} | {sh['mean_ci95_halfwidth'][t]} | {sh['between_model_sd_of_point'][t]} |")
L.append("\n### T7. Mixed fraction grid (analytic, 1 - E[p^k] - E[(1-p)^k], p ~ Beta(mu kappa, (1-mu) kappa))\n")
for kk in ("k10", "k20"):
    mus = [x for x in d["mixed_fraction_grid"][kk][0] if x.startswith("mu_")]
    L.append(f"\n{kk[1:]} samples per problem:\n")
    L.append("| kappa | " + " | ".join(m.replace("mu_", "mu ") for m in mus) + " |")
    L.append("|---|" + "---|" * len(mus))
    for r in d["mixed_fraction_grid"][kk]:
        L.append(f"| {r['kappa']} | " + " | ".join(f"{r[m]:.3f}" for m in mus) + " |")
L.append("\n### T8. Mixed fraction per model in the config\n")
L.append("| Model | mu | kappa 0.801 k=10 | k=20 | kappa 1.835 k=10 | k=20 | kappa 0.40 k=10 | k=20 |")
L.append("|---|---|---|---|---|---|---|---|")
pm = d["mixed_per_model_analytic"]
for i, m in enumerate(pm["kappa_k080"]):
    a, b, c = pm["kappa_k080"][i], pm["kappa_k183"][i], pm["kappa_k040"][i]
    L.append(f"| {a['name']} | {a['mu']} | {a['mixed_k10']} | {a['mixed_k20']} | {b['mixed_k10']} | {b['mixed_k20']} | {c['mixed_k10']} | {c['mixed_k20']} |")
L.append("\nMean mixed count per model at n = 542 (analytic): " + json.dumps(d["mean_mixed_count_n542_analytic"]))
L.append("\n### T9. Heterogeneity check (population level, 30 worlds)\n")
L.append("| Setting | mean G0 | between-model SD of G0 | mean W_P | between-model SD of W_P |")
L.append("|---|---|---|---|---|")
for h, v in d["heterogeneity_check"].items():
    L.append(f"| {h} | {v['mean_G0']} | {v['between_model_sd_G0_mean_over_worlds']} | {v['mean_W_P']} | {v['between_model_sd_W_P']} |")
(H / "tables_generated.md").write_text("\n".join(L) + "\n")
print("ok")
