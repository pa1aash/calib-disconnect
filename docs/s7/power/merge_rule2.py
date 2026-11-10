"""Adds the R2-refit-rule results to power_r2.json and thresholds_r2.json (key r2_refit_rule) and writes rule2_tables.md."""
import json
from pathlib import Path
H = Path(__file__).resolve().parent
r = json.loads((H / "power_r2_rule2.json").read_text())
p = json.loads((H / "power_r2.json").read_text()); p["r2_refit_rule"] = r
(H / "power_r2.json").write_text(json.dumps(p, indent=1) + "\n")
t = json.loads((H / "thresholds_r2.json").read_text()); t["r2_refit_rule"] = {"thresholds": r["thresholds"], "verification": r["verification"],
    "note": "crossing = first interpolated 0.90 of min(D1 at R=0, D2 at +2delta, D3 at -2delta), widened by the R2 rule; refit relative SD 0.10 trained / 0.05 probe"}
(H / "thresholds_r2.json").write_text(json.dumps(t, indent=1) + "\n")
L = []
H_ = r["headline_n542"]
def cells(v, dl, tag):
    b = v["by_R"]; out = []
    for nm, R in (("D1", 0.0), ("D2", 2 * dl), ("D3", -2 * dl)):
        c = b[str(round(R, 3) if R else 0.0)][f"delta_{dl}_{tag}"]
        out.append((c[nm], max(c[nm + "_se_cluster"], c[nm + "_se_binom"])))
    return out
L.append("### T11. R2 rule, power at n = 542 (widened; unwidened min in the last-but-one column; SE = larger of binomial and cluster SE)\n")
L.append("| Refit noise | Heterogeneity | k | delta | mean mixed | D1 at R=0 | D2 at +2delta | D3 at -2delta | min | min unwidened | P(inconclusive) at R=delta |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|")
for pre, lab in (("head", "0.10 / 0.05 (primary)"), ("stress2", "0.20 / 0.10 (stress, 2x)")):
    for h in ("nominal", "conservative"):
        for k in (10, 20):
            v = H_[f"{pre}|{h}|{k}|542"]
            for dl in (0.02, 0.03):
                c = cells(v, dl, "widened"); u = cells(v, dl, "unwidened")
                L.append(f"| {lab} | {h} | {k} | {dl} | {v['mean_mixed_per_model']} | " + " | ".join(f"{a:.3f} ({s:.3f})" for a, s in c)
                         + f" | {min(a for a, _ in c):.3f} | {min(a for a, _ in u):.3f} | {v['by_R'][str(dl)][f'delta_{dl}_widened']['inconclusive']:.3f} |")
L.append("\n### T12. R2 rule, interval components at n = 542, R = 0 (means over replicates)\n")
L.append("| Refit noise | Heterogeneity | k | SD of point estimate | bootstrap half-width h | rms s_refit | widened half-width |")
L.append("|---|---|---|---|---|---|---|")
for pre, lab in (("head", "primary"), ("stress2", "2x")):
    for h in ("nominal", "conservative"):
        for k in (10, 20):
            b = H_[f"{pre}|{h}|{k}|542"]["by_R"]["0.0"]
            L.append(f"| {lab} | {h} | {k} | {b['sd_point']} | {b['mean_halfwidth_bootstrap']} | {b['rms_s_refit']} | {b['mean_halfwidth_widened']} |")
L.append("\n### T13. R2 rule, sweep over n (widened; D1 / D2 / D3 and min), then unwidened min\n")
L.append("| Heterogeneity | k | n | mean mixed | delta 0.03 D1 / D2 / D3 | min | unwidened min | delta 0.02 D1 / D2 / D3 | min | unwidened min |")
L.append("|---|---|---|---|---|---|---|---|---|---|")
for name, rows in r["sweep_widened"].items():
    h, k = name.split("_")
    for a, u in zip(rows, r["sweep_unwidened"][name]):
        x, y = a["delta_0.03"], a["delta_0.02"]
        L.append(f"| {h} | {k[1:]} | {a['n']} | {a['mean_mixed_per_model']} | {x['D1']:.3f} / {x['D2']:.3f} / {x['D3']:.3f} | {x['min']:.3f} | {u['delta_0.03']['min']:.3f} | {y['D1']:.3f} / {y['D2']:.3f} / {y['D3']:.3f} | {y['min']:.3f} | {u['delta_0.02']['min']:.3f} |")
L.append("\n### T14. R2 rule, minimum mean mixed count per model for min-power 0.90 (T10 = k 10, T20 = k 20), with verification at the crossing\n")
L.append("| Heterogeneity | k | delta | crossing: mean mixed (n) | verification run (separate seeds, 480 replicates): D1 / D2 / D3, min |")
L.append("|---|---|---|---|---|")
for key, c in r["thresholds"].items():
    h, kk, dl = key.split("_"); dl = dl[5:]
    if "n" in c:
        vk = f"{h}_{kk}_n{int(-(-c['n'] // 1))}"
        v = r["verification"][vk]["delta_" + dl]
        L.append(f"| {h} | {kk[1:]} | {dl} | {c['mixed']} ({c['n']}) | {v['D1']:.3f} / {v['D2']:.3f} / {v['D3']:.3f}, min {v['min']:.3f} (mixed {r['verification'][vk]['mean_mixed_per_model']}) |")
    else:
        L.append(f"| {h} | {kk[1:]} | {dl} | no crossing on the available pool (n up to 542): max min-power {c['max_min_power']:.3f} at n = 542 | not run |")
(H / "rule2_tables.md").write_text("\n".join(L) + "\n")
print("ok")
