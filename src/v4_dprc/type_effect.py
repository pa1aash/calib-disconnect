"""Does requirement TYPE predict failure CONSISTENTLY across problems (a cross-problem skill)?

competence(problem, req) = per-requirement pass rate (targets_l1). We residualize by problem mean
(removing problem-level difficulty), group residuals by TYPE, and test whether type is a consistent
factor: some skill types systematically harder than their problem's average, across many problems.

  strong + significant type effect (eta^2 well above 0, ANOVA p<<0.05, coherent per-type ordering)
    => cross-problem skills EXIST -> the psychometric paper has substance.
  ~0 type effect / no significance => code competence has no stable per-type skill structure -> stop.
"""
from __future__ import annotations
import argparse
import json
import numpy as np
from scipy import stats

from serialization import load_labeled


def run(labels_path, types_path):
    types = {}
    for line in open(types_path, encoding="utf-8"):
        if line.strip():
            d = json.loads(line)
            types[(d["problem_id"], d["test_id"])] = d["type"]
    recs = load_labeled(labels_path)

    comp, typ, prob_mean = [], [], []
    per_prob = {}
    rows = []
    for r in recs:
        vals = {tid: float(r.targets_l1[tid]) for tid in r.test_ids if tid in r.targets_l1}
        if len(vals) < 2:
            continue
        pm = float(np.mean(list(vals.values())))
        for tid, c in vals.items():
            t = types.get((r.problem_id, tid), "other")
            rows.append((c, c - pm, t, r.problem_id))
    comp = np.array([x[0] for x in rows])
    resid = np.array([x[1] for x in rows])          # competence minus problem difficulty
    typ = np.array([x[2] for x in rows])
    n = len(rows)

    from collections import Counter
    print(f"requirements: {n} | type dist: {dict(Counter(typ))}")
    # per-type residual competence (deviation from problem difficulty), sorted
    groups = {t: resid[typ == t] for t in set(typ) if (typ == t).sum() >= 20}
    print("\nper-type mean RESIDUAL competence (competence minus problem difficulty), n>=20:")
    for t, g in sorted(groups.items(), key=lambda kv: kv[1].mean()):
        se = g.std() / np.sqrt(len(g))
        print(f"  {t:15s} n={len(g):4d}  resid={g.mean():+.3f} +/-{1.96*se:.3f}  (raw comp {comp[typ==t].mean():.3f})")

    # ANOVA: does type explain residual competence?
    gl = list(groups.values())
    if len(gl) >= 2:
        F, p = stats.f_oneway(*gl)
        # eta^2 (variance explained by type on residual)
        allr = np.concatenate(gl); grand = allr.mean()
        ss_between = sum(len(g) * (g.mean() - grand) ** 2 for g in gl)
        ss_total = ((allr - grand) ** 2).sum()
        eta2 = ss_between / ss_total if ss_total > 0 else 0.0
        print(f"\nANOVA type effect on residual competence: F={F:.2f}, p={p:.2e}, eta^2={eta2:.4f}")
        print("  eta^2 is the fraction of cross-problem-controlled competence variance explained by skill TYPE.")
        print("  verdict:", "SKILLS EXIST (type is a real cross-problem factor)" if (p < 0.01 and eta2 > 0.03)
              else "WEAK/NO stable per-type skill structure")
    return rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", default="/workspace/data/v4_dprc/labels/bcb_full.jsonl")
    ap.add_argument("--types", default="/workspace/data/v4_dprc/labels/req_types.jsonl")
    args = ap.parse_args()
    run(args.labels, args.types)
