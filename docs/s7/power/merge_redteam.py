"""Stores power_r2_redteam.json under r2_refit_rule.redteam in power_r2.json and thresholds_r2.json; writes redteam_tables.md."""
import json
from pathlib import Path
H = Path(__file__).resolve().parent
r = json.loads((H / "power_r2_redteam.json").read_text())
p = json.loads((H / "power_r2.json").read_text()); p["r2_refit_rule"]["redteam"] = r
(H / "power_r2.json").write_text(json.dumps(p, indent=1) + "\n")
t = json.loads((H / "thresholds_r2.json").read_text())
t["r2_refit_rule"]["redteam"] = {"T": r["T_corrected"], "crossings_raw": r["crossings"], "T_first_pass_superseded_for_k20": r["T"], "verification_first_pass": r["verification"],
    "note": "delta 0.03, t_{12,0.95} = 1.782, R2 refit rule, nominal heterogeneity; mixed counts are means over six models at n = 542 unless an n sweep"}
(H / "thresholds_r2.json").write_text(json.dumps(t, indent=1) + "\n")

def trio(s, dl, tag):
    b = s["by_R"]; o = []
    for nm, R in (("D1", 0.0), ("D2", round(2 * dl, 3)), ("D3", round(-2 * dl, 3))):
        c = b[str(R)][f"delta_{dl}_{tag}"]; o.append((c[nm], c[nm + "_se"]))
    return o
L = ["### RT1. Widening multiplier 1.645 versus t = 1.782 (R2 rule, n = 542, 480 replicates; D1 / D2 / D3, min; SE of min-limiting cell in last column)\n",
     "| Heterogeneity | k | delta | mean mixed | unwidened | z = 1.645 | t = 1.782 | SE (t = 1.782, D1) |", "|---|---|---|---|---|---|---|---|"]
for h in ("nominal", "conservative"):
    for k, dls in ((10, (0.03, 0.02)), (20, (0.03,))):
        s = r["headline"][f"head|{h}|{k}"]
        for dl in dls:
            cs = {tg: trio(s, dl, tg) for tg in ("unwidened", "z1.645", "t1.782")}
            f = lambda c: f"{c[0][0]:.3f} / {c[1][0]:.3f} / {c[2][0]:.3f}, min {min(x for x, _ in c):.3f}"
            L.append(f"| {h} | {k} | {dl} | {s['mean_mixed_per_model']} | {f(cs['unwidened'])} | {f(cs['z1.645'])} | {f(cs['t1.782'])} | {cs['t1.782'][0][1]:.3f} |")
L += ["\n(The k = 20, delta 0.02 cells are also in the JSON: nominal min 0.858 and conservative 0.848 at t = 1.782.)\n",
      "### RT2. Heterogeneous mixed counts (k = 10, delta 0.03, n = 542, 480 replicates): one model at 60 mixed, five near 207 to 259\n",
      "| Heterogeneity | mixed per model (six) | unwidened | z = 1.645 | t = 1.782 |", "|---|---|---|---|---|"]
for h in ("nominal", "conservative"):
    s = r["hetcount"][f"hetcount|{h}"]
    f = lambda c: f"{c[0][0]:.3f} / {c[1][0]:.3f} / {c[2][0]:.3f}, min {min(x for x, _ in c):.3f}"
    L.append(f"| {h} | {s['mixed_per_model_vector']} | {f(trio(s, 0.03, 'unwidened'))} | {f(trio(s, 0.03, 'z1.645'))} | {f(trio(s, 0.03, 't1.782'))} |")
L += ["\n### RT3. Residual-error correlation rho_e (delta 0.03, n = 542, 480 replicates; baseline rho_e = 0.5 is in RT1)\n",
      "| Heterogeneity | k | rho_e | SD of point | bootstrap h | t = 1.782: D1 / D2 / D3, min |", "|---|---|---|---|---|---|"]
for key, s in sorted(r["rho_e"].items()):
    _, h, k, rho = key.split("|")
    c = trio(s, 0.03, "t1.782")
    L.append(f"| {h} | {k} | {rho} | {s['by_R']['0.0']['sd_point']} | {s['by_R']['0.0']['mean_h']} | {c[0][0]:.3f} / {c[1][0]:.3f} / {c[2][0]:.3f}, min {min(x for x, _ in c):.3f} |")
L += ["\n### RT4. Min power (t = 1.782, delta 0.03) versus mean mixed count and mean pass-fail pairs per model\n",
      "n sweep: 240 replicates per point (20 worlds x 12) except the n = 542 point (480). mu and kappa scenarios: n = 542, nominal heterogeneity, 240 replicates, all six models' mu shifted together (offset in `scenario_info`) or kappa changed.\n",
      "| k | scenario | setting | mean mixed | mean pairs | D1 / D2 / D3 | min |", "|---|---|---|---|---|---|---|"]
for k in ("k10", "k20"):
    for nm in ("n_sweep", "mu_sweep", "kappa_sweep"):
        for q in sorted(r["curves"][k][nm], key=lambda x: x["mixed"]):
            st = q.get("n") if nm == "n_sweep" else q.get("scen")
            if nm == "n_sweep": st = f"n = {st}"
            elif q.get("scen") == "baseline": st = "baseline (mu 0.72/0.80, kappa 0.801, n = 542)"
            elif nm == "mu_sweep": st = f"mu offset +{r['scenario_info'][q['scen']]['mu_offset']}"
            else: st = f"kappa {r['scenario_info'][q['scen']]['kappa']}"
            L.append(f"| {k[1:]} | {nm} | {st} | {q['mixed']} | {q['pairs']:.0f} | {q['D1']:.3f} / {q['D2']:.3f} / {q['D3']:.3f} | {q['min']:.3f} |")
T = r["T_corrected"]
L += ["\n### RT5. Thresholds T10 and T20 (delta 0.03, t = 1.782)\n",
      "| k | bracketed crossings of 0.90 (mean mixed per model) | not bracketed | T (largest bracketed crossing x 1.10, rounded up to 5) | verification run (480 replicates, separate seeds) |", "|---|---|---|---|---|"]
for k in ("k10", "k20"):
    v = T[k]["verification"]
    L.append(f"| {k[1:]} | {T[k]['bracketed_crossings_vs_mixed']} | {'; '.join(T[k]['not_bracketed'].values())} | **{T[k]['T' + k[1:]]}** | mixed {v['mixed']}, pairs {v['pairs']:.0f}: D1 {v['D1']}, D2 {v['D2']}, D3 {v['D3']}, min {v['min']} |")
(H / "redteam_tables.md").write_text("\n".join(L) + "\n")
print("ok")
