"""Phase 1 driver — sample n+1 solutions, execute per-test, build per-group labels, serialize.

Runs the full labeling chain and evaluates GATE-0 (execution wall-clock/budget) and GATE-1
(label validity + spread). GPU is used ONLY for `generator.generate` (vLLM); everything else
(execution, grouping, labeling) is CPU. Local dry-run with StubGenerator proves the chain works.

Usage on the box:
    python label_dataset.py --sources mbpp apps taco livecodebench --limit 3000 --model qwen2.5-coder-7b
Local dry-run (no GPU):
    python label_dataset.py            # 5 HumanEval problems via StubGenerator
"""
from __future__ import annotations
import argparse
import time
import numpy as np

import config
from sampling import build_prompt, clean_code, StubGenerator
from pertest_harness import pertest_matrix, discard_flaky, run_solution_pertest
from serialization import build_labeled, write_manifest


def label_problems(problems, generator, out_path, n_samples=config.N_SAMPLES,
                   n_extra=config.N_LABEL_EXTRA, exec_timeout=config.EXEC_TIMEOUT, verbose=True, chunk=40):
    # Chunked generate->execute->append so a crash loses at most one chunk (not hours of a long run)
    # and progress is visible. Records kept in memory for the end-of-run manifest.
    import json
    from dataclasses import asdict
    open(out_path, "w").close()                       # truncate/create
    records, n_exec, exec_secs, gen_secs = [], 0, 0.0, 0.0
    for start in range(0, len(problems), chunk):
        batch = problems[start:start + chunk]
        t_gen = time.time()
        gens = generator.generate([build_prompt(p) for p in batch], n=n_samples + n_extra)
        gen_secs += time.time() - t_gen
        with open(out_path, "a", encoding="utf-8") as f:
            for prob, comps in zip(batch, gens):
                codes = [clean_code(c, prob) for c in comps]
                solutions, independent = codes[:n_samples], codes[n_samples]
                if prob.canonical_solution:
                    kept_idx, rep = discard_flaky(prob.canonical_solution, prob.units, exec_timeout)
                else:
                    kept_idx, rep = list(range(len(prob.units))), {"note": "no canonical; flaky-discard skipped"}
                kept = [prob.units[i] for i in kept_idx]
                if not kept:
                    continue
                t0 = time.time()
                mat = pertest_matrix(solutions, kept, exec_timeout)
                indep_row = np.array(run_solution_pertest(independent, kept, exec_timeout), dtype=bool)
                exec_secs += time.time() - t0
                n_exec += (len(solutions) + 1) * len(kept)
                rec = build_labeled(prob, solutions, independent, kept, mat, indep_row, rep)
                records.append(rec)
                f.write(json.dumps(asdict(rec)) + "\n")
        if verbose:
            print(f"  [{min(start+chunk,len(problems))}/{len(problems)}] {len(records)} labeled", flush=True)

    timing = {"gen_secs": round(gen_secs, 2), "exec_secs": round(exec_secs, 2),
              "n_executions": n_exec,
              "exec_per_sec": round(n_exec / exec_secs, 1) if exec_secs else None}
    manifest = write_manifest(records, str(out_path).replace(".jsonl", "_manifest.json"),
                              level=config.GROUPING_LEVEL_L1, timing=timing)

    if verbose:
        print(f"labeled {len(records)} problems -> {out_path}")
        print(f"timing: {timing}")
        print(f"manifest: n_problems={manifest['n_problems']} "
              f"with>=2groups={manifest['n_problems_with_2plus_groups']} "
              f"spread_frac={manifest['spread_fraction_intermediate']} by_source={manifest['by_source']}")
    return records, manifest, timing


def check_gate1(manifest, pool_target=config.POOL_TARGET):
    """GATE-1: enough problems survive with >=2 groups AND targets show spread."""
    ok_problems = manifest["n_problems_with_2plus_groups"]
    spread = manifest["spread_fraction_intermediate"]
    # scale the min-problems threshold to the fraction of the target pool actually labeled
    scaled_min = config.GATE1_MIN_PROBLEMS * (manifest["n_problems"] / pool_target) if pool_target else 0
    pass_problems = ok_problems >= max(1, scaled_min * 0.5)   # lenient for partial/dry runs
    pass_spread = spread >= config.GATE1_MIN_SPREAD_FRAC
    verdict = "PASS" if (pass_problems and pass_spread) else "FAIL"
    print(f"\n[GATE-1] problems_with_2groups={ok_problems} spread_frac={spread} "
          f"(need spread>={config.GATE1_MIN_SPREAD_FRAC}) -> {verdict}")
    if not pass_spread:
        print("  -> spread too low: enrich pool with harder TACO/LiveCodeBench problems.")
    return verdict == "PASS"


def estimate_gate0(timing, pool_target=config.POOL_TARGET, n_labeled=None):
    """GATE-0: extrapolate full-pool execution wall-clock from the measured exec rate."""
    if not timing.get("exec_per_sec") or not n_labeled:
        print("[GATE-0] insufficient timing to extrapolate."); return
    per_prob = timing["n_executions"] / n_labeled
    full_exec = per_prob * pool_target
    est_days = full_exec / timing["exec_per_sec"] / 86400
    verdict = "PASS" if est_days <= config.GATE0_MAX_EXEC_WALLCLOCK_DAYS else "FAIL (de-scope pool / add CPU)"
    print(f"[GATE-0] est full-pool executions={int(full_exec):,} @ {timing['exec_per_sec']}/s "
          f"-> ~{est_days:.2f} days -> {verdict}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", nargs="*", default=None)
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--model", default=config.PRIMARY_MODEL)
    ap.add_argument("--out", default=str(config.LABELS_DIR / "labels_dryrun.jsonl"))
    ap.add_argument("--stub", action="store_true", help="use StubGenerator (no GPU)")
    ap.add_argument("--backend", default="vllm", choices=["vllm", "hf"],
                    help="GPU generation backend: vllm (fast) or hf (transformers .generate, no CUDA-wheel matching)")
    args = ap.parse_args()

    from loaders import LOADERS
    if args.sources:
        problems = []
        for s in args.sources:
            problems += LOADERS[s](min_tests=config.MIN_TESTS_PER_PROBLEM, limit=args.limit)
    else:
        # default local dry-run: HumanEval (has canonical solutions -> Stub works)
        from loaders import load_humaneval
        problems = load_humaneval(min_tests=1, limit=args.limit)

    if args.stub or not args.sources:
        gen = StubGenerator({build_prompt(p): p for p in problems})
        print(f"[dry-run] StubGenerator over {len(problems)} problems (no GPU)")
    elif args.backend == "hf":
        from sampling import HFGenerator
        gen = HFGenerator(args.model)
        print(f"[HF backend] {args.model} over {len(problems)} problems")
    else:
        from sampling import VLLMGenerator
        gen = VLLMGenerator(args.model)

    recs, manifest, timing = label_problems(problems, gen, args.out)
    estimate_gate0(timing, n_labeled=len(recs))
    check_gate1(manifest)
