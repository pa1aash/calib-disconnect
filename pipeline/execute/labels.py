"""Labels, flip table, behavior signatures, and the agreement label-proxy share.

``label_samples`` gives one ``Label`` per (sample, label suite) of the sample's benchmark. An extraction
failure is labeled y = 0 with source "extraction_failure" and is never executed (design section 6, row
5.9). Otherwise y = 1 exactly when every test of the suite passes within its limit with a normal exit
and no exception. Pairs excluded by the reference check have no row (the analysis uses only
non-excluded problems per suite).
"""

from __future__ import annotations

import json
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Mapping, Sequence

from pipeline.contracts import constants
from pipeline.contracts.schemas import (
    LABEL_SUITES_LCB, LABEL_SUITES_LV, ExecutionResult, ExtractionResult, Label, Problem, TestSuite,
)

from . import harness
from .extract import parse_sample_uid
from .reference import ReferenceStore, inputs_fingerprint
from .sandbox import ReferenceUnavailable

LABEL_SUITE_ORDER: tuple[str, ...] = LABEL_SUITES_LV + LABEL_SUITES_LCB


def label_suite_ids(suites: Mapping[str, TestSuite]) -> list[str]:
    return [s for s in LABEL_SUITE_ORDER if s in suites]


def _execute_many(tasks: Mapping[str, tuple[str, Problem, TestSuite, bool]], executor: Any, cache: Any, *,
                  trusted: bool, workers: int) -> dict[str, ExecutionResult]:
    """Run each distinct cache key once; reuse and audit cached results."""
    results: dict[str, ExecutionResult] = {}
    todo: list[str] = []
    audits: list[str] = []
    for key in tasks:
        cached = cache.get(key) if cache is not None else None
        if cached is None:
            todo.append(key)
        else:
            results[key] = cached
            if cache.should_audit(key):
                audits.append(key)

    def run(key: str) -> ExecutionResult:
        code, problem, suite, capture = tasks[key]
        return executor.run(code, problem, suite, trusted=trusted, capture_outputs=capture)

    def parallel(keys: Sequence[str], fn: Callable[[str], Any]) -> list[Any]:
        if workers > 1 and len(keys) > 1:
            with ThreadPoolExecutor(max_workers=workers) as pool:
                return list(pool.map(fn, keys))
        return [fn(k) for k in keys]

    for key, res in zip(todo, parallel(todo, run)):
        results[key] = res
        if cache is not None:
            cache.put(res)
    if cache is not None and audits:
        parallel(audits, lambda k: cache.audit(k, results[k], lambda: run(k)))
    return results


def label_samples(extractions: Sequence[ExtractionResult], problems: Mapping[str, Problem],
                  suites: Mapping[str, Mapping[str, TestSuite]], executor: Any, cache: Any, *,
                  trusted: bool = False, workers: int = 1,
                  excluded: frozenset[tuple[str, str]] | set[tuple[str, str]] = frozenset()) -> list[Label]:
    """One Label per (sample, label suite). ``excluded`` holds (problem_id, suite_id) pairs from the
    reference check; they get no row. ``trusted`` is for hand-written fixtures only."""
    excluded = set(excluded)
    plan: list[tuple[ExtractionResult, str, str | None]] = []   # (extraction, suite id, cache key or None)
    tasks: dict[str, tuple[str, Problem, TestSuite, bool]] = {}
    for ex in extractions:
        pid = parse_sample_uid(ex.sample_uid)["problem_id"]
        problem = problems[pid]
        for sid in label_suite_ids(suites[pid]):
            if (pid, sid) in excluded:
                continue
            if ex.failure is not None or ex.code is None:
                plan.append((ex, sid, None))
                continue
            suite = suites[pid][sid]
            try:
                key = executor.cache_key(ex.code, problem, suite)
            except ReferenceUnavailable:
                excluded.add((pid, sid))
                continue
            tasks.setdefault(key, (ex.code, problem, suite, False))
            plan.append((ex, sid, key))
    results = _execute_many(tasks, executor, cache, trusted=trusted, workers=workers)
    out: list[Label] = []
    for ex, sid, key in plan:
        if key is None:
            out.append(Label(ex.sample_uid, sid, 0, "extraction_failure", ex.failure, None))
        else:
            r = results[key]
            out.append(Label(ex.sample_uid, sid, int(r.passed), "execution", r.failure, key))
    return out


def flip_table(labels: Sequence[Label], *, from_suite: str = "O", to_suite: str = "E") -> dict[str, dict[str, Any]]:
    """Per model: counts of samples whose label differs between two suites (default O versus E).
    ``pass_to_fail`` is y_O = 1, y_E = 0 (expected: plus inputs catch wrong programs);
    ``fail_to_pass`` is y_O = 0, y_E = 1 (can only come from flaky tests or changed time limits; each is
    listed in ``fail_to_pass_uids`` for investigation). Samples missing either label are counted in
    ``n_unpaired``."""
    by_sample: dict[str, dict[str, int]] = defaultdict(dict)
    for lab in labels:
        if lab.suite_id in (from_suite, to_suite):
            by_sample[lab.sample_uid][lab.suite_id] = lab.y
    table: dict[str, dict[str, Any]] = {}
    for uid in sorted(by_sample):
        model = parse_sample_uid(uid)["model_key"]
        t = table.setdefault(model, {"n_paired": 0, "n_unpaired": 0, "both_pass": 0, "both_fail": 0,
                                     "pass_to_fail": 0, "fail_to_pass": 0, "fail_to_pass_uids": [],
                                     "from_suite": from_suite, "to_suite": to_suite})
        d = by_sample[uid]
        if from_suite not in d or to_suite not in d:
            t["n_unpaired"] += 1
            continue
        t["n_paired"] += 1
        a, b = d[from_suite], d[to_suite]
        if a and b:
            t["both_pass"] += 1
        elif not a and not b:
            t["both_fail"] += 1
        elif a and not b:
            t["pass_to_fail"] += 1
        else:
            t["fail_to_pass"] += 1
            t["fail_to_pass_uids"].append(uid)
    return table


def agreement_signatures(extractions: Sequence[ExtractionResult], problems: Mapping[str, Problem],
                         suites: Mapping[str, Mapping[str, TestSuite]], executor: Any, cache: Any, *,
                         trusted: bool = False, workers: int = 1) -> dict[str, tuple[str, ...] | None]:
    """sample_uid -> behavior signature (design section 7.7): the canonical output repr per agreement
    input, '!<ExceptionType>' where the program raised or timed out. None when the sample has no code
    (extraction failure), its problem has no agreement input, or the program as a whole failed (program
    cap, killed, memory, sandbox error): an absent signature, never an imputed one."""
    plan: list[tuple[str, str | None]] = []
    tasks: dict[str, tuple[str, Problem, TestSuite, bool]] = {}
    for ex in extractions:
        pid = parse_sample_uid(ex.sample_uid)["problem_id"]
        suite = suites.get(pid, {}).get("agree")
        if ex.failure is not None or ex.code is None or suite is None or len(suite.inputs) == 0:
            plan.append((ex.sample_uid, None))
            continue
        key = executor.cache_key(ex.code, problems[pid], suite, capture_outputs=True)
        tasks.setdefault(key, (ex.code, problems[pid], suite, True))
        plan.append((ex.sample_uid, key))
    results = _execute_many(tasks, executor, cache, trusted=trusted, workers=workers)
    return {uid: (None if key is None else results[key].outputs) for uid, key in plan}


def signature_to_json(sig: tuple[str, ...] | None) -> str | None:
    return None if sig is None else json.dumps(list(sig), ensure_ascii=False, separators=(",", ":"))


def signature_from_json(s: str | None) -> tuple[str, ...] | None:
    return None if s is None else tuple(json.loads(s))


def agreement_label_proxy(problems: Sequence[Problem], suites: Mapping[str, Mapping[str, TestSuite]],
                          store: ReferenceStore) -> dict[str, Any]:
    """Per problem, the share of agreement inputs whose reference output equals (canonical repr, 9
    significant digits) the reference output on some label input (design section 4, red team V14b).
    HumanEval+ and MBPP+ only: LiveCodeBench has no reference outputs for its agreement inputs. Problems
    whose reference was excluded on the agreement set or on the label suite are listed under 'skipped'."""
    per: dict[str, Any] = {}
    skipped: dict[str, str] = {}
    for p in problems:
        s = suites.get(p.problem_id, {})
        if p.canonical_solution is None or "agree" not in s:
            continue
        agree = store.get(p.problem_id, "agree", inputs_fingerprint(s["agree"]))
        label_sid = "E" if "E" in s else ("O" if "O" in s else None)
        label = store.get(p.problem_id, label_sid, inputs_fingerprint(s[label_sid])) if label_sid else None
        if agree is None or not agree.ok or label is None or not label.ok:
            skipped[p.problem_id] = "reference unavailable"
            continue
        label_outputs = set(label.outputs_canon)
        n = len(agree.outputs_canon)
        k = sum(1 for o in agree.outputs_canon if o in label_outputs)
        per[p.problem_id] = {"n_agree": n, "n_equal_to_a_label_output": k, "share": (k / n) if n else None,
                             "label_suite": label_sid}
    shares = [v["share"] for v in per.values() if v["share"] is not None]
    return {"definition": ("share of agreement inputs whose reference output (canonical repr, "
                           f"{constants.AGREEMENT_SIGNATURE_FLOAT_SIG} significant digits) equals the reference output "
                           "on some input of the label suite E (O when E is absent)"),
            "mean_share": (sum(shares) / len(shares)) if shares else None, "n_problems": len(per),
            "problems": per, "skipped": skipped}
