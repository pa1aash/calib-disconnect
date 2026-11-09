"""Direction B — generate a model's OWN unit tests per BigCodeBench problem.

For the code/test blind-spot study: we later score, per reference requirement R, whether any
self-generated test method discriminates R (matches R's pass/fail signature across our labeled
10-solution pool), then correlate that per-requirement TEST competence with the model's per-requirement
CODE competence. This module only does the generation half. Runs on the box under the vLLM venv.
"""
from __future__ import annotations
import argparse
import json

import config
from loaders import load_bigcodebench
from sampling import clean_code


def build_test_prompt(problem) -> str:
    """Ask the model for its own unittest suite for task_func. It must NOT define task_func (we inject
    a candidate solution at scoring time) — only a TestCases class of independent test_* methods."""
    return ("Write a thorough Python `unittest` test suite for the function `task_func` specified below. "
            "Define exactly one class `TestCases(unittest.TestCase)` with several independent `test_*` "
            "methods covering typical, edge, empty/zero, and error cases. Do NOT define or import "
            "`task_func` yourself — assume it already exists in scope. Output ONLY one python code block.\n\n"
            + problem.prompt)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=1140)
    ap.add_argument("--model", default=config.PRIMARY_MODEL)
    ap.add_argument("--n", type=int, default=1, help="self-test suites per problem")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    probs = load_bigcodebench(min_tests=2, limit=args.limit)
    from sampling import VLLMGenerator
    gen = VLLMGenerator(args.model)
    prompts = [build_test_prompt(p) for p in probs]
    outs = gen.generate(prompts, n=args.n, max_tokens=768)     # test suites can be long
    with open(args.out, "w", encoding="utf-8") as f:
        for p, comps in zip(probs, outs):
            for i, c in enumerate(comps):
                f.write(json.dumps({"problem_id": p.problem_id, "model": args.model,
                                    "sample": i, "test_code": clean_code(c, p)}) + "\n")
    print(f"wrote {len(probs)}x{args.n} self-test suites -> {args.out}")


if __name__ == "__main__":
    main()
