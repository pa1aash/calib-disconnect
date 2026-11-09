"""Build #3 — persist per-test outcomes + generated code + labels.

The v2/v3 results discarded generated code and stored only whole-problem pass counts, so they can't
be relabeled per-test. This module persists everything DPRC needs, so labeling is a one-time cost:

  LabeledProblem  — one problem's samples, per-test pass matrix, and per-group targets/labels.
  save_labeled / iter_labeled  — JSONL round-trip (streamable; one problem per line).
  write_manifest  — dataset composition + GATE-1 spread statistics.

Stored per problem (after flaky/broken-test discard, kept units only):
  solutions[n]              generated code samples (the confidence targets come from these)
  independent_solution      the (n+1)th sample (unbiased eval label source)
  pass_matrix[n][t]         0/1 per (solution, kept-test)
  independent_pass_row[t]   0/1 for the (n+1)th sample per kept-test
  test_ids[t], categories[t]
  targets_l1/l2             {group: continuous pass-rate target}   <- TRAINING labels
  per_solution_l1/l2        {group: [0/1 per solution]}            <- did solution satisfy the requirement
  indep_label_l1/l2         {group: 0/1}                           <- EVAL label (from independent sample)
"""
from __future__ import annotations
import json
from dataclasses import dataclass, asdict, field
from pathlib import Path
import numpy as np

from grouping import assign_groups, per_group_pass_rate


@dataclass
class LabeledProblem:
    problem_id: str
    source: str
    prompt: str
    style: str
    solutions: list[str]
    independent_solution: str
    test_ids: list[str]
    categories: list[str]                     # L2 category per kept test
    pass_matrix: list[list[int]]              # [n_sol x n_tests]
    independent_pass_row: list[int]           # [n_tests]
    targets_l1: dict = field(default_factory=dict)
    targets_l2: dict = field(default_factory=dict)
    per_solution_l1: dict = field(default_factory=dict)
    per_solution_l2: dict = field(default_factory=dict)
    indep_label_l1: dict = field(default_factory=dict)
    indep_label_l2: dict = field(default_factory=dict)
    discard_report: dict = field(default_factory=dict)


def build_labeled(problem, solutions: list[str], independent_solution: str,
                  kept_units: list, pass_matrix: np.ndarray, independent_pass_row: np.ndarray,
                  discard_report: dict) -> LabeledProblem:
    """Assemble a LabeledProblem from raw execution output. `kept_units` are the TestUnits that
    survived flaky/broken discard; `pass_matrix` is [n_sol x len(kept_units)]."""
    cats = assign_groups(kept_units, "l2")
    stats_l1 = per_group_pass_rate(pass_matrix, kept_units, "l1")
    stats_l2 = per_group_pass_rate(pass_matrix, kept_units, "l2")
    # eval labels from the independent sample: satisfies requirement g iff it passes all tests in g
    indep_mat = independent_pass_row.reshape(1, -1)
    indep_l1 = {g: int(v[0]) for g, v in per_group_pass_rate(indep_mat, kept_units, "l1")["per_solution"].items()}
    indep_l2 = {g: int(v[0]) for g, v in per_group_pass_rate(indep_mat, kept_units, "l2")["per_solution"].items()}
    return LabeledProblem(
        problem_id=problem.problem_id, source=problem.source, prompt=problem.prompt, style=problem.style,
        solutions=solutions, independent_solution=independent_solution,
        test_ids=[u.test_id for u in kept_units], categories=cats,
        pass_matrix=pass_matrix.astype(int).tolist(),
        independent_pass_row=independent_pass_row.astype(int).tolist(),
        targets_l1=stats_l1["target"], targets_l2=stats_l2["target"],
        per_solution_l1=stats_l1["per_solution"], per_solution_l2=stats_l2["per_solution"],
        indep_label_l1=indep_l1, indep_label_l2=indep_l2,
        discard_report=discard_report,
    )


def save_labeled(records: list[LabeledProblem], path: str | Path):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(asdict(r)) + "\n")


def iter_labeled(path: str | Path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield LabeledProblem(**json.loads(line))


def load_labeled(path: str | Path) -> list[LabeledProblem]:
    return list(iter_labeled(path))


def write_manifest(records: list[LabeledProblem], path: str | Path, level: str = "l1",
                   timing: dict | None = None) -> dict:
    """Dataset composition + GATE-1 spread stats. `level` picks which targets to measure spread on."""
    by_source: dict[str, int] = {}
    n_groups = 0
    n_intermediate = 0
    n_problems_ok = 0
    for r in records:
        by_source[r.source] = by_source.get(r.source, 0) + 1
        targets = r.targets_l1 if level == "l1" else r.targets_l2
        if len(targets) >= 2:
            n_problems_ok += 1
        for t in targets.values():
            n_groups += 1
            if 0.1 < t < 0.9:                      # an intermediate (non-degenerate) target
                n_intermediate += 1
    spread_frac = (n_intermediate / n_groups) if n_groups else 0.0
    manifest = {
        "n_problems": len(records),
        "n_problems_with_2plus_groups": n_problems_ok,
        "by_source": by_source,
        "grouping_level": level,
        "n_groups_total": n_groups,
        "spread_fraction_intermediate": round(spread_frac, 4),
        "timing": timing or {},
    }
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


if __name__ == "__main__":
    # round-trip self-test using the harness + grouping on a synthetic problem
    from pertest_harness import split_humaneval, pertest_matrix, discard_flaky
    from types import SimpleNamespace

    prob = SimpleNamespace(
        problem_id="test/1", source="humaneval", style="call",
        prompt="def f(xs):\n",
        test=("def check(candidate):\n"
              "    assert candidate([]) == 0\n"
              "    assert candidate([1,2]) == 3\n"
              "    assert candidate([5]) == 5\n"),
        entry_point="f",
    )
    prob.__dict__["prompt"] = prob.prompt  # split_humaneval reads dict-style
    units = split_humaneval({"prompt": prob.prompt, "test": prob.test, "entry_point": "f"})
    sols = ["def f(xs):\n    return sum(xs)\n", "def f(xs):\n    return sum(xs) if xs else 9\n"]
    indep = "def f(xs):\n    return sum(xs)\n"
    canonical = "def f(xs):\n    return sum(xs)\n"
    kept_idx, rep = discard_flaky(canonical, units)
    kept = [units[i] for i in kept_idx]
    mat = pertest_matrix(sols, kept)
    indep_row = pertest_matrix([indep], kept)[0]

    rec = build_labeled(prob, sols, indep, kept, mat, indep_row, rep)
    save_labeled([rec], "/tmp/_dprc_test.jsonl")
    back = load_labeled("/tmp/_dprc_test.jsonl")[0]
    man = write_manifest([rec], "/tmp/_dprc_manifest.json", level="l1")

    print("kept tests:", rec.test_ids, "| categories:", rec.categories)
    print("targets_l1:", rec.targets_l1)
    print("per_solution_l1:", rec.per_solution_l1)
    print("indep_label_l1:", rec.indep_label_l1)
    print("manifest:", man)
    assert back.problem_id == "test/1" and back.targets_l1 == rec.targets_l1, "round-trip mismatch"
    assert man["n_problems"] == 1
    print("\nSELF-TEST PASSED: build/save/load + manifest round-trip correct.")
