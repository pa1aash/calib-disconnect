"""Definitive test (Direction: latent skills) — semantically TYPE each requirement, so we can ask
whether requirement TYPE predicts failure consistently ACROSS problems (a cross-problem skill), which
the within-problem de-risk could not reach.

Each requirement = a BigCodeBench unittest method (test_id) within a problem. We classify it into one
of a fixed skill taxonomy using the model, from the task prompt + the test method name. Runs on the box
under the vLLM venv. Output: {problem_id, test_id, type} per requirement.
"""
from __future__ import annotations
import argparse
import json
import re

import config
from serialization import load_labeled

TYPES = ["edge_boundary", "error_handling", "core_logic", "type_format",
         "data_structure", "numeric", "io_external", "other"]


def build_type_prompt(prompt_text: str, test_id: str) -> str:
    return ("Classify what SKILL a unit test checks, into EXACTLY ONE label from this list:\n"
            "edge_boundary (empty/zero/single/large/boundary inputs), error_handling (raises/invalid input/exceptions), "
            "core_logic (main computation correctness), type_format (return type/format/shape), "
            "data_structure (dict/list/dataframe manipulation), numeric (floats/rounding/precision), "
            "io_external (file/network/mock/plot), other.\n\n"
            f"Task:\n{prompt_text[:500]}\n\nUnit test method name: {test_id}\n\n"
            "Answer with ONLY the single label, nothing else.")


def parse_type(text: str) -> str:
    t = text.strip().lower()
    for ty in TYPES:
        if ty in t:
            return ty
    return "other"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", default="/workspace/data/v4_dprc/labels/bcb_full.jsonl")
    ap.add_argument("--model", default=config.PRIMARY_MODEL)
    ap.add_argument("--out", default="/workspace/data/v4_dprc/labels/req_types.jsonl")
    args = ap.parse_args()

    recs = load_labeled(args.labels)
    items = []                                   # (problem_id, test_id, prompt)
    for r in recs:
        for tid in r.test_ids:
            items.append((r.problem_id, tid, r.prompt))
    from sampling import VLLMGenerator
    gen = VLLMGenerator(args.model)
    prompts = [build_type_prompt(pr, tid) for _, tid, pr in items]
    outs = gen.generate(prompts, n=1, temperature=0.0, max_tokens=8)
    with open(args.out, "w", encoding="utf-8") as f:
        for (pid, tid, _), comps in zip(items, outs):
            f.write(json.dumps({"problem_id": pid, "test_id": tid, "type": parse_type(comps[0])}) + "\n")
    print(f"typed {len(items)} requirements -> {args.out}")


if __name__ == "__main__":
    main()
