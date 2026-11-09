"""Make-or-break test of the UTILITY path (the last open direction).

On PARTIAL-PASS solutions (fail >=1 requirement, pass >=1), does ORACLE-localized TARGETED repair
(tell the model exactly which requirement failed, ask it to fix only that) beat WHOLE-solution
regeneration at matched budget (1 generation each)? This is the UPPER BOUND on targeted-repair utility.

  targeted repair clearly > whole regen (more requirements passed / more full-pass conversions,
    Wilcoxon significant) => the probe-driven version is worth building; utility path alive.
  targeted repair ~ whole regen => localization adds nothing (failures too correlated); utility dead.

Runs on the box under the vLLM venv (generation) + CPU (execution).
"""
from __future__ import annotations
import argparse
import json
import numpy as np

import config
from loaders import load_bigcodebench
from serialization import load_labeled
from pertest_harness import run_solution_pertest
from sampling import clean_code


def build_repair_prompt(prompt_text, solution, fail_ids):
    fails = ", ".join(fail_ids)
    return ("The following Python solution is INCORRECT: it fails the unit test(s): " + fails + ". "
            "Fix the code so it passes ALL of the task's tests, changing as little as possible. "
            "Output ONLY the corrected complete function.\n\n"
            f"Task:\n{prompt_text}\n\nCurrent (buggy) solution:\n{solution}\n")


def build_regen_prompt(prompt_text):
    return ("Complete the following Python function. Only output the complete function, no explanations.\n\n"
            + prompt_text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", default="/workspace/data/v4_dprc/labels/bcb_full.jsonl")
    ap.add_argument("--model", default=config.PRIMARY_MODEL)
    ap.add_argument("--per-problem", type=int, default=2, help="partial-pass solutions per problem")
    ap.add_argument("--limit", type=int, default=1200)
    args = ap.parse_args()

    probs = {p.problem_id: p for p in load_bigcodebench(min_tests=2, limit=args.limit)}
    recs = load_labeled(args.labels)

    tasks = []   # (units, solution, fail_ids, prompt)
    for r in recs:
        p = probs.get(r.problem_id)
        if not p:
            continue
        unit_by_id = {u.test_id: u for u in p.units}
        kept = [unit_by_id[t] for t in r.test_ids if t in unit_by_id]
        if len(kept) != len(r.test_ids):
            continue
        taken = 0
        for si, sol in enumerate(r.solutions):
            row = [r.per_solution_l1[t][si] for t in r.test_ids]
            npass = int(sum(row))
            if 0 < npass < len(row):
                fails = [r.test_ids[j] for j in range(len(row)) if row[j] == 0]
                tasks.append((kept, sol, fails, p.prompt))
                taken += 1
                if taken >= args.per_problem:
                    break
    print(f"partial-pass repair tasks: {len(tasks)}")

    from sampling import VLLMGenerator
    gen = VLLMGenerator(args.model)
    reps = gen.generate([build_repair_prompt(pr, s, f) for (_, s, f, pr) in tasks], n=1, max_tokens=768)
    regs = gen.generate([build_regen_prompt(pr) for (_, _, _, pr) in tasks], n=1, max_tokens=768)

    orig_pass, rep_pass, reg_pass = [], [], []
    orig_full, rep_full, reg_full = 0, 0, 0
    for (units, sol, fails, pr), rc, gc in zip(tasks, reps, regs):
        k = len(units)
        o = int(k - len(fails))                        # original requirements passed
        r_pass = int(sum(run_solution_pertest(clean_code(rc[0]), units)))
        g_pass = int(sum(run_solution_pertest(clean_code(gc[0]), units)))
        orig_pass.append(o / k); rep_pass.append(r_pass / k); reg_pass.append(g_pass / k)
        orig_full += (o == k); rep_full += (r_pass == k); reg_full += (g_pass == k)
    n = len(tasks)
    op, rp, gp = np.array(orig_pass), np.array(rep_pass), np.array(reg_pass)
    print(f"\nmean requirement-pass fraction:  original {op.mean():.3f} | REPAIR {rp.mean():.3f} | regen {gp.mean():.3f}")
    print(f"full-pass conversions: repair {rep_full}/{n} ({rep_full/n:.3f}) | regen {reg_full}/{n} ({reg_full/n:.3f}) | (orig {orig_full}/{n})")
    from scipy import stats
    if n > 5:
        w = stats.wilcoxon(rp, gp, zero_method="zsplit")
        print(f"Wilcoxon REPAIR vs regen (requirement-pass): stat={w.statistic:.0f}, p={w.pvalue:.2e}")
        print(f"mean delta (repair - regen) = {(rp-gp).mean():+.3f}")
        print("  verdict:", "TARGETED REPAIR WINS -> utility path alive" if (w.pvalue < 0.05 and (rp-gp).mean() > 0.02)
              else "no clear win -> utility path also weak")


if __name__ == "__main__":
    main()
