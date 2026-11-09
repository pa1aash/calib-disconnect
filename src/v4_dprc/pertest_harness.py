"""Build #1 — per-test-case execution harness.

The v1/v2/v3 harness (`execute_humaneval` / `execute_mbpp_fixed`) runs the WHOLE test block as one
subprocess and returns a single boolean. DPRC needs, for each generated solution, a vector of
per-test outcomes so we can compute per-REQUIREMENT pass rates. This module provides that:

  split_humaneval(prob) / split_mbpp(prob)  -> list[TestUnit]   (one runnable unit per assert)
  run_solution_pertest(code, units)         -> list[bool]       (pass/fail for each unit)
  pertest_matrix(solutions, units)          -> np.ndarray[n_sol, n_units] (CPU-parallel)
  discard_flaky(canonical_code, units)      -> (kept_idx, report)  drop nondeterministic/broken tests

Design choices (frozen for reproducibility):
- Each test unit runs in its own subprocess (`sys.executable`), isolated temp file, hard timeout.
- Determinism: we do NOT inject seeds into user code, but flaky tests are DETECTED (run the canonical
  solution twice) and DISCARDED, and tests the canonical solution fails are treated as broken and
  discarded. Label validity, not just test count, is a first-class control (plan GATE-1).
- CPU-bound: run this OFF the GPU (your own machine / a cheap CPU VM). Never on paid GPU time.
- HumanEval `check()` is split at TOP-LEVEL asserts. Loop-based checks with no top-level assert are
  not splittable -> the whole check becomes one unit (n_tests=1). Dense per-test structure comes from
  MBPP/APPS/TACO/LiveCodeBench, not HumanEval; HumanEval per-test is a legacy bonus.
"""
from __future__ import annotations
import ast
import os
import sys
import tempfile
import subprocess
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import numpy as np

DEFAULT_TIMEOUT = 10  # seconds per test, matches the v3 harness


@dataclass
class TestUnit:
    """One runnable per-test unit. `build_script(solution_code)` returns a complete .py program
    that is True (exit 0) iff the solution passes THIS single test."""
    test_id: str
    preamble: str          # setup lines (assignments, helpers, candidate= alias) run before the assert
    assertion: str         # the single assert / test body
    kind: str              # "humaneval" | "mbpp" | "io" | "whole"
    def build_script(self, solution_code: str) -> str:
        return f"{solution_code}\n{self.preamble}\n{self.assertion}\n"


# ---------------------------------------------------------------- HumanEval splitting

def split_humaneval(prob: dict) -> list[TestUnit]:
    """Split a HumanEval problem's check() into per-assert units.
    prob keys used: 'prompt', 'test', 'entry_point'. Solution code passed later must define entry_point."""
    entry = prob["entry_point"]
    test_src = prob["test"]
    try:
        tree = ast.parse(test_src)
    except SyntaxError:
        return [TestUnit("whole", f"candidate = {entry}", _wrap_whole_check(test_src, entry), "whole")]

    check_fn = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "check"), None)
    if check_fn is None:
        return [TestUnit("whole", f"candidate = {entry}", _wrap_whole_check(test_src, entry), "whole")]

    # candidate is the check() parameter name (usually 'candidate'); bind it to the entry point.
    cand_param = check_fn.args.args[0].arg if check_fn.args.args else "candidate"
    setup_lines, asserts = [], []
    for stmt in check_fn.body:
        if isinstance(stmt, ast.Assert):
            asserts.append(ast.unparse(stmt))
        else:
            setup_lines.append(ast.unparse(stmt))
    preamble = f"{cand_param} = {entry}\n" + "\n".join(setup_lines)

    if not asserts:
        # loop-based / no top-level asserts -> not splittable; run the whole check as one unit
        return [TestUnit("whole", f"{cand_param} = {entry}", _wrap_whole_check(test_src, entry), "whole")]
    return [TestUnit(f"he_{i}", preamble, a, "humaneval") for i, a in enumerate(asserts)]


def _wrap_whole_check(test_src: str, entry: str) -> str:
    return f"{test_src}\ncheck({entry})"


# ---------------------------------------------------------------- MBPP splitting

def split_mbpp(prob: dict) -> list[TestUnit]:
    """Split an MBPP (sanitized) problem into per-assert units.
    prob keys used: 'test_list' (list[str] of asserts), optional 'test_setup_code'."""
    setup = prob.get("test_setup_code", "") or ""
    tests = list(prob.get("test_list", []) or [])
    tests += list(prob.get("challenge_test_list", []) or [])  # extra hidden tests if present
    return [TestUnit(f"mbpp_{i}", setup, t, "mbpp") for i, t in enumerate(tests)]


# ---------------------------------------------------------------- IO-style (APPS / CodeContests / LCB)

def split_io(io_pairs: list[tuple[str, str]]) -> list[TestUnit]:
    """One unit per (stdin, expected_stdout) pair. The solution is run as a script fed `stdin`,
    and its stdout is compared to `expected` (see _run_io). Used for APPS/CodeContests/LiveCodeBench."""
    units = []
    for i, (stdin, expected) in enumerate(io_pairs):
        u = TestUnit(f"io_{i}", "", "", "io")
        u.io_stdin = stdin           # attached dynamically; consumed by run_io_unit
        u.io_expected = expected
        units.append(u)
    return units


# ---------------------------------------------------------------- execution

def _run_script(script: str, timeout: int) -> bool:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(script); f.flush(); path = f.name
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0
    except Exception:
        return False
    finally:
        try: os.unlink(path)
        except OSError: pass


def _norm(s: str) -> str:
    return "\n".join(ln.rstrip() for ln in s.strip().splitlines())


def _run_io(solution_code: str, stdin: str, expected: str, timeout: int) -> bool:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(solution_code); f.flush(); path = f.name
    try:
        r = subprocess.run([sys.executable, path], input=stdin, capture_output=True, text=True, timeout=timeout)
        if r.returncode != 0:
            return False
        return _norm(r.stdout) == _norm(expected)   # judge-style: ignore trailing whitespace per line
    except Exception:
        return False
    finally:
        try: os.unlink(path)
        except OSError: pass


def run_one(solution_code: str, unit: TestUnit, timeout: int = DEFAULT_TIMEOUT) -> bool:
    if unit.kind == "io":
        return _run_io(solution_code, getattr(unit, "io_stdin", ""), getattr(unit, "io_expected", ""), timeout)
    return _run_script(unit.build_script(solution_code), timeout)


def run_solution_pertest(solution_code: str, units: list[TestUnit], timeout: int = DEFAULT_TIMEOUT,
                         max_workers: int | None = None) -> list[bool]:
    """Per-test outcomes for ONE solution across all units (threads launch subprocesses concurrently)."""
    workers = max_workers or min(len(units) or 1, (os.cpu_count() or 2))
    if workers <= 1 or len(units) <= 1:
        return [run_one(solution_code, u, timeout) for u in units]
    with ThreadPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(lambda u: run_one(solution_code, u, timeout), units))


def pertest_matrix(solutions: list[str], units: list[TestUnit], timeout: int = DEFAULT_TIMEOUT,
                   max_workers: int | None = None) -> np.ndarray:
    """[n_solutions x n_units] boolean pass matrix. Parallelized across all (solution, unit) jobs."""
    if not solutions or not units:
        return np.zeros((len(solutions), len(units)), dtype=bool)
    workers = max_workers or (os.cpu_count() or 2)
    jobs = [(si, ui) for si in range(len(solutions)) for ui in range(len(units))]
    mat = np.zeros((len(solutions), len(units)), dtype=bool)
    def _do(job):
        si, ui = job
        return si, ui, run_one(solutions[si], units[ui], timeout)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for si, ui, ok in ex.map(_do, jobs):
            mat[si, ui] = ok
    return mat


# ---------------------------------------------------------------- flaky / broken test discard (GATE-1)

def discard_flaky(canonical_code: str, units: list[TestUnit], timeout: int = DEFAULT_TIMEOUT,
                  runs: int = 2) -> tuple[list[int], dict]:
    """Run the canonical solution `runs` times against each unit. Keep a unit only if
    (a) it is DETERMINISTIC across runs, and (b) the canonical solution PASSES it (else the test is
    broken / mis-specified). Returns (kept_unit_indices, report)."""
    results = [run_solution_pertest(canonical_code, units, timeout) for _ in range(runs)]
    kept, dropped_flaky, dropped_broken = [], [], []
    for i in range(len(units)):
        outcomes = [results[r][i] for r in range(runs)]
        if len(set(outcomes)) > 1:
            dropped_flaky.append(units[i].test_id)
        elif not outcomes[0]:
            dropped_broken.append(units[i].test_id)   # canonical fails a supposedly-correct test
        else:
            kept.append(i)
    report = {"n_units": len(units), "kept": len(kept),
              "dropped_flaky": dropped_flaky, "dropped_broken": dropped_broken}
    return kept, report


# ---------------------------------------------------------------- self-test

if __name__ == "__main__":
    # Synthetic problem: add(a,b). Two good tests, one deliberately-broken test.
    fake_prob = {
        "prompt": "def add(a, b):\n",
        "entry_point": "add",
        "test": (
            "def check(candidate):\n"
            "    assert candidate(1, 2) == 3\n"
            "    assert candidate(0, 0) == 0\n"
            "    assert candidate(2, 2) == 5  # BROKEN test (2+2 != 5)\n"
        ),
    }
    units = split_humaneval(fake_prob)
    print(f"split -> {len(units)} units: {[u.test_id for u in units]}")

    correct = "def add(a, b):\n    return a + b\n"
    buggy   = "def add(a, b):\n    return a + b + 1\n"   # off-by-one: fails test0/test1, 'passes' broken test2

    mat = pertest_matrix([correct, buggy], units)
    print("pass matrix [correct; buggy]:\n", mat.astype(int))

    kept, rep = discard_flaky(correct, units)
    print("flaky/broken report:", rep)
    print("kept unit ids:", [units[i].test_id for i in kept])

    # assertions for the self-test
    assert mat.shape == (2, 3), mat.shape
    assert list(mat[0]) == [True, True, False], "correct add must pass the 2 good tests, fail the broken one"
    assert list(mat[1]) == [False, False, True], "buggy add must fail the good tests, 'pass' the broken one"
    assert rep["dropped_broken"] == ["he_2"], rep
    assert kept == [0, 1], kept
    print("\nSELF-TEST PASSED: per-test matrix + flaky/broken discard behave correctly.")
