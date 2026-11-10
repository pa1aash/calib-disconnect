"""Reference outputs and the reference-solution check (design section 6 and 4).

``ReferenceStore`` holds, per (problem, suite), the outputs of the canonical solution, its per-input
runtimes, and the per-test time limits derived from them with the EvalPlus rule
``max(min_time_limit, gt_time_limit_factor * ref_time)`` (1.0 and 4.0, evalplus/config.py 0.3.1). It is
persisted as JSON lines at ``layout.reference_outputs(benchmark)``. The outputs travel as a base64
pickle that is only ever unpickled inside the sandbox; the host works with canonical reprs.

``reference_check`` implements the design's check: a reference that raises, times out, or fails its own
pass criterion on a suite is excluded from that suite, listed with the reason, never repaired.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

from pipeline.contracts import constants, hashing
from pipeline.contracts.schemas import Problem, ReferenceCheck, TestSuite

from . import harness

FUNCTION_BENCHMARKS = ("humaneval_plus", "mbpp_plus")
LABEL_SUITES = ("O", "E")


def inputs_fingerprint(suite: TestSuite) -> str:
    """The suite's recorded input-set hash, or a hash of the canonical reprs of its inputs."""
    if suite.input_set_sha256:
        return suite.input_set_sha256
    h = hashlib.sha256()
    for x in suite.inputs:
        h.update(harness.canonical_repr(x).encode("utf-8", "replace"))
        h.update(b"\n")
    return h.hexdigest()


@dataclass
class RefEntry:
    problem_id: str
    suite_id: str
    input_set_sha256: str
    ok: bool
    failure: str | None             # ExecFailure of the reference run when not ok
    error: str | None               # exception token when not ok
    runtimes_s: list[float] = field(default_factory=list)
    time_limits_s: list[float] = field(default_factory=list)
    outputs_canon: list[str] = field(default_factory=list)
    expected_pickle_b64: str | None = None
    evaluator: str = f"evalplus=={constants.EVALPLUS_TOOL_VERSION}"
    min_time_limit: float = harness.DEFAULT_MIN_TIME_LIMIT
    gt_time_limit_factor: float = harness.DEFAULT_GT_TIME_LIMIT_FACTOR

    @property
    def ref_hash(self) -> str:
        """Identifies the expected outputs and the per-test limits; part of the cache-key time-limit rule."""
        return hashing.sha256_text(hashing.canonical_json(
            {"out": self.outputs_canon, "lim": [round(x, 9) for x in self.time_limits_s]}))

    def to_dict(self) -> dict[str, Any]:
        d = dict(self.__dict__)
        d["ref_hash"] = self.ref_hash
        return d

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "RefEntry":
        d = {k: v for k, v in d.items() if k != "ref_hash"}
        return cls(**d)


def reference_program(problem: Problem) -> str:
    """The complete canonical program. B1 stores HumanEval+ as prompt + body already; if the stored text
    does not define the entry point at top level (a bare body), the prompt is prepended."""
    sol = problem.canonical_solution
    if sol is None:
        raise ValueError(f"{problem.problem_id} has no canonical solution")
    import ast

    try:
        tree = ast.parse(sol)
        if any(isinstance(n, ast.FunctionDef) and n.name == problem.entry_point for n in tree.body):
            return sol
    except SyntaxError:
        pass
    return problem.prompt + sol


class ReferenceStore:
    """In-memory table of RefEntry, optionally backed by a JSON-lines file."""

    def __init__(self, path: Path | None = None, *, min_time_limit: float = harness.DEFAULT_MIN_TIME_LIMIT,
                 gt_time_limit_factor: float = harness.DEFAULT_GT_TIME_LIMIT_FACTOR):
        self.path = Path(path) if path is not None else None
        self.min_time_limit = min_time_limit
        self.gt_time_limit_factor = gt_time_limit_factor
        self._entries: dict[tuple[str, str], RefEntry] = {}
        if self.path is not None:
            self.load(self.path)

    def load(self, path: Path) -> int:
        """Merge the entries of a JSON-lines file (missing file: nothing). Returns the number read."""
        path = Path(path)
        n = 0
        if path.exists():
            for line in path.read_text().splitlines():
                if line.strip():
                    e = RefEntry.from_dict(json.loads(line))
                    self._entries[(e.problem_id, e.suite_id)] = e
                    n += 1
        return n

    def get(self, problem_id: str, suite_id: str, input_set_sha256: str | None = None) -> RefEntry | None:
        e = self._entries.get((problem_id, suite_id))
        if e is not None and input_set_sha256 is not None and e.input_set_sha256 != input_set_sha256:
            return None  # the suite changed since this entry was computed
        return e

    def put(self, e: RefEntry) -> None:
        self._entries[(e.problem_id, e.suite_id)] = e

    def entries(self) -> list[RefEntry]:
        return [self._entries[k] for k in sorted(self._entries)]

    def compute(self, executor: Any, problem: Problem, suite: TestSuite) -> RefEntry:
        """Run the canonical solution (trusted) on every input of the suite and store the entry."""
        fp = inputs_fingerprint(suite)
        e = self.get(problem.problem_id, suite.suite_id, fp)
        if e is not None:
            return e
        raw = executor.run_reference(problem, suite)
        limits = harness.time_limits_for(raw["runtimes"], self.min_time_limit, self.gt_time_limit_factor)
        e = RefEntry(problem_id=problem.problem_id, suite_id=suite.suite_id, input_set_sha256=fp,
                     ok=bool(raw["ok"]), failure=raw["failure"], error=raw["error"],
                     runtimes_s=list(raw["runtimes"]), time_limits_s=limits,
                     outputs_canon=list(raw["outputs_canon"]), expected_pickle_b64=raw["outputs_pickle_b64"],
                     min_time_limit=self.min_time_limit, gt_time_limit_factor=self.gt_time_limit_factor)
        if e.ok and len(e.outputs_canon) != len(suite.inputs):
            e.ok, e.failure, e.error = False, "sandbox_error", "output_count_mismatch"
        self.put(e)
        return e

    def save(self, path: Path | None = None, *, only: set[str] | None = None) -> Path:
        """Atomic write, sorted by (problem_id, suite_id); ``only`` restricts to some problem IDs."""
        path = Path(path) if path is not None else self.path
        if path is None:
            raise ValueError("no path")
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".ref.", suffix=".tmp")
        with os.fdopen(fd, "w") as f:
            for e in self.entries():
                if only is not None and e.problem_id not in only:
                    continue
                f.write(json.dumps(e.to_dict(), sort_keys=True) + "\n")
        os.replace(tmp, path)
        return path


def reference_check(problems: Sequence[Problem], suites: Mapping[str, Mapping[str, TestSuite]],
                    executor: Any, *, store: ReferenceStore | None = None, workers: int = 1) -> list[ReferenceCheck]:
    """One ReferenceCheck per (problem, suite) for problems that have a canonical solution.

    Steps per suite: (1) run the canonical solution on every input, recording outputs and runtimes
    (raising, timing out, or an unpicklable output excludes the pair); (2) for the label suites O and E,
    run the reference through the normal pass protocol against its own recorded outputs, so that a
    nondeterministic reference or one rejected by the special oracles is excluded too ("fails its own
    contract" is read as: fails its own suite). For the "agree" input set only step 1 applies.
    LiveCodeBench problems have no canonical solution and produce no rows (design section 6).
    """
    store = store if store is not None else getattr(executor, "references", None) or ReferenceStore()
    if getattr(executor, "references", None) is None:
        executor.references = store

    def one(problem: Problem, suite: TestSuite) -> ReferenceCheck:
        entry = store.compute(executor, problem, suite)
        if not entry.ok:
            return ReferenceCheck(problem.problem_id, suite.suite_id, False, entry.failure or "exception", True)
        if suite.suite_id in LABEL_SUITES:
            res = executor.run(reference_program(problem), problem, suite, trusted=True)
            if not res.passed:
                return ReferenceCheck(problem.problem_id, suite.suite_id, False, res.failure or "wrong_output", True)
        return ReferenceCheck(problem.problem_id, suite.suite_id, True, None, False)

    jobs: list[tuple[Problem, TestSuite]] = []
    for p in problems:
        if p.canonical_solution is None or p.benchmark not in FUNCTION_BENCHMARKS:
            continue
        for sid in sorted(suites.get(p.problem_id, {})):
            jobs.append((p, suites[p.problem_id][sid]))
    if workers > 1:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            return list(pool.map(lambda pj: one(*pj), jobs))
    return [one(p, s) for p, s in jobs]


def exclusion_report(checks: Sequence[ReferenceCheck]) -> dict[str, Any]:
    """Excluded share per suite, the share of problems excluded from either label suite, the listed
    reasons, and the K1 trigger (any label suite above constants.K1_MAX_REFERENCE_EXCLUSION)."""
    per: dict[str, dict[str, Any]] = {}
    for c in checks:
        d = per.setdefault(c.suite_id, {"n": 0, "excluded": 0, "reasons": {}})
        d["n"] += 1
        if c.excluded:
            d["excluded"] += 1
            d["reasons"][c.problem_id] = c.failure
    for d in per.values():
        d["share"] = d["excluded"] / d["n"] if d["n"] else 0.0
    label = {s: d for s, d in per.items() if s in LABEL_SUITES}
    either = {c.problem_id for c in checks if c.suite_id in LABEL_SUITES and c.excluded}
    n_problems = len({c.problem_id for c in checks if c.suite_id in LABEL_SUITES})
    share_either = len(either) / n_problems if n_problems else 0.0
    k1 = any(d["share"] > constants.K1_MAX_REFERENCE_EXCLUSION for d in label.values()) or \
        share_either > constants.K1_MAX_REFERENCE_EXCLUSION
    return {"per_suite": per, "share_either_label_suite": share_either, "n_problems": n_problems,
            "k1_threshold": constants.K1_MAX_REFERENCE_EXCLUSION, "k1_triggered": bool(k1)}
