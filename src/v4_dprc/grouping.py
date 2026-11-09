"""Requirement-grouping rule (PRE-REGISTERED — freeze before any run).

Defines the unit at which the model expresses confidence. The de-scope ladder fixes two levels:
  L1 (bold)  = per-INDIVIDUAL-TEST  -> group_id = test_id (identity). "Which test will fail?"
  L2 (safe)  = per-CATEGORY         -> group_id = a deterministic requirement-category label.

The ONLY design choice here is the L2 category taxonomy. DEFAULT (below) is a deterministic,
benchmark-agnostic classifier over the literals appearing in each test's INPUT side:
  empty_or_zero | negative | large | typical | other
Rationale: these are semantically-meaningful "requirement classes" ("I'm unsure about the
empty-input case"), they need no semantic model, they are reproducible, and they reduce the
per-test correlation that drives the §8B smearing risk. Swap `L2_TAXONOMY` / `classify_unit`
to change the rule — but freeze it before Phase 1 and record it in the reproducibility checklist.

`per_group_pass_rate` turns a per-test pass matrix (from pertest_harness) into the continuous
per-group confidence TARGETS used for training, and the per-(solution, group) labels used for eval.
"""
from __future__ import annotations
import ast
import numpy as np

L2_TAXONOMY = ["empty_or_zero", "negative", "large", "typical", "other"]
LARGE_THRESHOLD = 1_000_000


def _literals(node: ast.AST):
    """Yield literal values under `node`, resolving unary minus (so -3 reads as -3, not 3)."""
    for n in ast.walk(node):
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub) \
                and isinstance(n.operand, ast.Constant) and isinstance(n.operand.value, (int, float)) \
                and not isinstance(n.operand.value, bool):
            yield -n.operand.value
        elif isinstance(n, ast.Constant):
            yield n.value


def _input_nodes(tree: ast.AST):
    """The INPUT subtrees of a test assertion = arguments of the FIRST function call.
    Classifying on inputs (not the expected output on the RHS) is the principled requirement rule.
    Falls back to the whole tree if no call is found."""
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            return list(n.args) + [kw.value for kw in n.keywords]
    return [tree]


def classify_unit(unit) -> str:
    """Deterministic L2 category for one TestUnit, from the literals in its INPUT arguments."""
    src = f"{getattr(unit, 'assertion', '')}"
    if not src:  # io units: category from stdin, deterministic
        stdin = getattr(unit, "io_stdin", "")
        if stdin.strip() == "":
            return "empty_or_zero"
        return "large" if len(stdin) > 200 else "typical"
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return "other"
    inputs = _input_nodes(tree)
    vals = []
    for sub in inputs:
        vals.extend(_literals(sub))
    # structural checks over the INPUT AST (empty/large containers are List/Tuple/Dict/Set nodes)
    containers = [n for sub in inputs for n in ast.walk(sub)
                  if isinstance(n, (ast.List, ast.Tuple, ast.Set, ast.Dict))]
    def _clen(n):
        return len(n.keys) if isinstance(n, ast.Dict) else len(n.elts)

    has_empty = (
        any(v in (0, "", None) or (isinstance(v, (list, tuple, dict, set, str)) and len(v) == 0) for v in vals)
        or any(_clen(c) == 0 for c in containers)
    )
    has_neg = any(isinstance(v, (int, float)) and not isinstance(v, bool) and v < 0 for v in vals)
    has_large = (
        any(isinstance(v, (int, float)) and not isinstance(v, bool) and abs(v) >= LARGE_THRESHOLD for v in vals)
        or any(isinstance(v, str) and len(v) >= 200 for v in vals)
        or any(_clen(c) >= 50 for c in containers)
    )
    if not vals and not containers:
        return "other"
    if has_empty:
        return "empty_or_zero"
    if has_neg:
        return "negative"
    if has_large:
        return "large"
    return "typical"


def assign_groups(units, level: str = "l1") -> list[str]:
    """Return a group_id per unit. level='l1' -> per-test identity; 'l2' -> per-category."""
    if level == "l1":
        return [u.test_id for u in units]
    if level == "l2":
        return [classify_unit(u) for u in units]
    raise ValueError(f"unknown grouping level: {level!r}")


def group_indices(units, level: str = "l1") -> dict[str, list[int]]:
    """Map each group_id -> list of unit indices in that group (order-stable)."""
    gids = assign_groups(units, level)
    out: dict[str, list[int]] = {}
    for i, g in enumerate(gids):
        out.setdefault(g, []).append(i)
    return out


def per_group_pass_rate(pass_matrix: np.ndarray, units, level: str = "l1") -> dict:
    """Collapse a [n_solutions x n_units] pass matrix into per-group statistics.

    Returns:
      {
        "groups": [group_id...],                         # stable order
        "target": {group_id: continuous pass rate in [0,1]},   # mean over solutions AND units-in-group
        "per_solution": {group_id: [0/1 per solution]},  # did solution s pass ALL units in the group
      }
    - `target` is the TRAINING label (continuous per-group pass rate).
    - `per_solution[g][s]` (all-units-pass) is the per-(solution, group) EVAL label:
      a solution "satisfies requirement g" iff it passes every test in g.
    """
    gi = group_indices(units, level)
    n_sol = pass_matrix.shape[0]
    groups = list(gi.keys())
    target, per_solution = {}, {}
    for g in groups:
        cols = gi[g]
        sub = pass_matrix[:, cols]                 # [n_sol x |g|]
        # per-solution satisfaction of the requirement = passes ALL tests in the group
        sol_pass = sub.all(axis=1).astype(int) if n_sol else np.zeros(0, dtype=int)
        per_solution[g] = sol_pass.tolist()
        # continuous target = mean pass fraction across solutions x tests in the group
        target[g] = float(sub.mean()) if sub.size else float("nan")
    return {"groups": groups, "target": target, "per_solution": per_solution}


if __name__ == "__main__":
    from pertest_harness import split_humaneval, pertest_matrix

    prob = {
        "prompt": "def f(xs):\n",
        "entry_point": "f",
        "test": (
            "def check(candidate):\n"
            "    assert candidate([]) == 0\n"          # empty_or_zero
            "    assert candidate([-3, -1]) == -4\n"   # negative
            "    assert candidate([2, 3]) == 5\n"      # typical
            "    assert candidate([2000000]) == 2000000\n"  # large
        ),
    }
    units = split_humaneval(prob)
    cats = assign_groups(units, "l2")
    print("L1 groups:", assign_groups(units, "l1"))
    print("L2 groups:", cats)

    good = "def f(xs):\n    return sum(xs)\n"
    bad  = "def f(xs):\n    return sum(xs) if xs else 1\n"   # fails the empty case only
    mat = pertest_matrix([good, bad], units)
    print("matrix:\n", mat.astype(int))
    stats_l1 = per_group_pass_rate(mat, units, "l1")
    stats_l2 = per_group_pass_rate(mat, units, "l2")
    print("L1 targets:", stats_l1["target"])
    print("L2 targets:", stats_l2["target"])
    print("L2 per_solution (satisfies requirement?):", stats_l2["per_solution"])

    # checks: 'good' passes all; 'bad' fails only the empty_or_zero group
    assert cats == ["empty_or_zero", "negative", "typical", "large"], cats
    assert stats_l2["per_solution"]["empty_or_zero"] == [1, 0], stats_l2["per_solution"]
    assert stats_l2["per_solution"]["typical"] == [1, 1], stats_l2["per_solution"]
    assert abs(stats_l1["target"]["he_0"] - 0.5) < 1e-9  # empty test: good passes, bad fails -> 0.5
    print("\nSELF-TEST PASSED: L1/L2 grouping + per-group targets behave correctly.")
