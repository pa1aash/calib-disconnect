"""Per-test benchmark loaders → unified Problem objects with TestUnits.

Every loader returns list[Problem]; a Problem carries the prompt, an optional canonical solution
(for flaky/broken-test discard), and the per-test units (from pertest_harness.split_*). The
>=3-test filter (plan GATE-0/Phase-1) is applied via `min_tests`.

Reuses the exact dataset ids/splits from the v2/v3 code:
  HumanEval : openai_humaneval (test)                         [assert-based]
  MBPP      : google-research-datasets/mbpp, 'sanitized'      [assert-based]
  APPS      : codeparrot/apps (train, introductory)           [stdin/stdout IO]
  TACO      : BAAI/TACO                                        [stdin/stdout IO]   (Build #2)
  LiveCodeBench : livecodebench/code_generation_lite          [stdin/stdout IO]   (Build #2)

CONTAMINATION CONTROL: `livecodebench(..., start_date=, end_date=)` filters by contest_date so the
eval window is disjoint from training and post-dates the model's cutoff (plan Phase 1/3).

NOTE (honest): TACO and LiveCodeBench schemas evolve across releases. The IO-extraction helpers
below target the current public schema; if a field name differs on the box's installed version,
adjust `_lcb_tests` / `_io_pairs_from_apps_like`. HumanEval/MBPP/APPS are stable and smoke-tested.
"""
from __future__ import annotations
import json
import base64
import zlib
import pickle
from dataclasses import dataclass, field

from pertest_harness import TestUnit, split_humaneval, split_mbpp, split_io


@dataclass
class Problem:
    problem_id: str
    source: str                       # humaneval | mbpp | apps | taco | livecodebench
    prompt: str                       # the text/signature shown to the model
    units: list[TestUnit]
    canonical_solution: str | None = None
    style: str = "call"               # "call" (assert-based) | "io" (stdin/stdout)
    meta: dict = field(default_factory=dict)

    def n_tests(self) -> int:
        return len(self.units)


def _filter(problems: list[Problem], min_tests: int) -> list[Problem]:
    return [p for p in problems if p.n_tests() >= min_tests]


# ---------------------------------------------------------------- HumanEval (assert-based)

def load_humaneval(min_tests: int = 1, limit: int | None = None) -> list[Problem]:
    from datasets import load_dataset
    ds = load_dataset("openai/openai_humaneval", split="test")  # namespaced id (datasets>=3 requires it)
    out = []
    for row in ds:
        units = split_humaneval(row)
        out.append(Problem(
            problem_id=f"humaneval/{row['task_id']}",
            source="humaneval",
            prompt=row["prompt"],
            units=units,
            canonical_solution=row["prompt"] + row["canonical_solution"],
            style="call",
            meta={"entry_point": row["entry_point"]},
        ))
        if limit and len(out) >= limit:
            break
    return _filter(out, min_tests)


# ---------------------------------------------------------------- MBPP sanitized (assert-based)

def load_mbpp(min_tests: int = 1, limit: int | None = None) -> list[Problem]:
    from datasets import load_dataset
    ds = load_dataset("google-research-datasets/mbpp", "sanitized", split="test")
    out = []
    for row in ds:
        units = split_mbpp(row)
        prompt = (row.get("prompt") or row.get("text") or "").strip()
        out.append(Problem(
            problem_id=f"mbpp/{row['task_id']}",
            source="mbpp",
            prompt=prompt + "\n",
            units=units,
            canonical_solution=row.get("code"),
            style="call",
            meta={"test_setup_code": row.get("test_setup_code", "")},
        ))
        if limit and len(out) >= limit:
            break
    return _filter(out, min_tests)


# ---------------------------------------------------------------- APPS (stdin/stdout IO)

def _io_pairs_from_apps_like(io_field) -> list[tuple[str, str]]:
    """APPS/TACO store tests as JSON {'inputs': [...], 'outputs': [...]}. Returns (stdin, expected)."""
    if not io_field:
        return []
    io = json.loads(io_field) if isinstance(io_field, str) else io_field
    if "fn_name" in io:            # call-based problem (function-args, not stdin/stdout) -> skip
        return []                  # ponytail: only stdin/stdout; thousands remain, don't build call-based
    ins, outs = io.get("inputs", []), io.get("outputs", [])
    pairs = []
    for i, o in zip(ins, outs):
        s = i if isinstance(i, str) else "\n".join(map(str, i)) + "\n"
        e = o if isinstance(o, str) else ("\n".join(map(str, o)) if isinstance(o, list) else str(o))
        pairs.append((s, e))
    return pairs


def load_apps(min_tests: int = 3, difficulty: str = "introductory", limit: int | None = None) -> list[Problem]:
    from datasets import load_dataset
    ds = load_dataset("codeparrot/apps", split="train", trust_remote_code=True)
    out = []
    for row in ds:
        if difficulty and row.get("difficulty") != difficulty:
            continue
        pairs = _io_pairs_from_apps_like(row.get("input_output"))
        if len(pairs) < min_tests:
            continue
        units = split_io(pairs)
        sols = row.get("solutions")
        canonical = None
        if sols:
            try:
                canonical = json.loads(sols)[0] if isinstance(sols, str) else sols[0]
            except Exception:
                canonical = None
        out.append(Problem(
            problem_id=f"apps/{row.get('problem_id', len(out))}",
            source="apps",
            prompt=row.get("question", ""),
            units=units,
            canonical_solution=canonical,
            style="io",
            meta={"difficulty": row.get("difficulty")},
        ))
        if limit and len(out) >= limit:
            break
    return _filter(out, min_tests)


# ---------------------------------------------------------------- TACO (Build #2, stdin/stdout IO)

def load_taco(min_tests: int = 3, split: str = "train", limit: int | None = None) -> list[Problem]:
    """TACO (BAAI/TACO) — dense per-problem tests (~50-200). Same input_output JSON shape as APPS.
    Verify the split/field names against the installed version on the box if extraction is empty."""
    from datasets import load_dataset
    ds = load_dataset("BAAI/TACO", split=split, trust_remote_code=True)
    out = []
    for row in ds:
        pairs = _io_pairs_from_apps_like(row.get("input_output"))
        if len(pairs) < min_tests:
            continue
        units = split_io(pairs)
        sols = row.get("solutions")
        canonical = None
        if sols:
            try:
                canonical = (json.loads(sols)[0] if isinstance(sols, str) else sols[0])
            except Exception:
                canonical = None
        out.append(Problem(
            problem_id=f"taco/{row.get('id', len(out))}",
            source="taco",
            prompt=row.get("question", ""),
            units=units,
            canonical_solution=canonical,
            style="io",
            meta={"difficulty": row.get("difficulty"), "source": row.get("source")},
        ))
        if limit and len(out) >= limit:
            break
    return _filter(out, min_tests)


# ---------------------------------------------------------------- LiveCodeBench (Build #2, contamination-controlled)

def _decode_lcb_private(row):
    """LiveCodeBench 'lite' compresses private_test_cases (base64(zlib(pickle))) in some releases."""
    raw = row.get("private_test_cases")
    if not raw:
        return []
    if isinstance(raw, str):
        try:
            return pickle.loads(zlib.decompress(base64.b64decode(raw.encode("utf-8"))))
        except Exception:
            try:
                return json.loads(raw)
            except Exception:
                return []
    return raw


def _lcb_tests(row) -> list[tuple[str, str]]:
    pairs = []
    for key in ("public_test_cases",):
        tc = row.get(key)
        if isinstance(tc, str):
            try: tc = json.loads(tc)
            except Exception: tc = []
        for t in (tc or []):
            pairs.append((t.get("input", ""), t.get("output", "")))
    for t in _decode_lcb_private(row):
        if isinstance(t, dict):
            pairs.append((t.get("input", ""), t.get("output", "")))
    return pairs


def load_livecodebench(min_tests: int = 3, start_date: str | None = None, end_date: str | None = None,
                       version_tag: str = "release_latest", limit: int | None = None) -> list[Problem]:
    """LiveCodeBench code_generation_lite. `start_date`/`end_date` = ISO 'YYYY-MM-DD' filter on
    contest_date for a contamination-controlled window (and to split train vs eval windows)."""
    from datasets import load_dataset
    ds = load_dataset("livecodebench/code_generation_lite", split="test",
                      version_tag=version_tag, trust_remote_code=True)
    out = []
    for row in ds:
        cdate = str(row.get("contest_date", ""))[:10]
        if start_date and cdate and cdate < start_date:
            continue
        if end_date and cdate and cdate > end_date:
            continue
        pairs = _lcb_tests(row)
        if len(pairs) < min_tests:
            continue
        out.append(Problem(
            problem_id=f"lcb/{row.get('question_id', len(out))}",
            source="livecodebench",
            prompt=row.get("question_content", ""),
            units=split_io(pairs),
            canonical_solution=None,   # LCB does not ship reference solutions in lite; discard uses generated-sample stability
            style="io",
            meta={"contest_date": cdate, "difficulty": row.get("difficulty"),
                  "platform": row.get("platform"), "starter_code": row.get("starter_code", "")},
        ))
        if limit and len(out) >= limit:
            break
    return _filter(out, min_tests)


# ---------------------------------------------------------------- BigCodeBench (per-unittest-method requirements)

def split_bigcodebench(prob: dict):
    """One TestUnit per unittest `test_*` method — each is a distinct semantic requirement.
    The unit runs just that method and exits nonzero on failure."""
    import re
    test_src = prob["test"]
    methods = re.findall(r"def (test_\w+)\s*\(", test_src)
    units = []
    for m in methods:
        runner = (f"import unittest as _ut, sys as _s\n"
                  f"_r=_ut.TestResult(); TestCases('{m}').run(_r); _s.exit(0 if _r.wasSuccessful() else 1)")
        units.append(TestUnit(test_id=m, preamble=test_src, assertion=runner, kind="unittest"))
    return units


def load_bigcodebench(min_tests: int = 3, limit: int | None = None, version: str = "v0.1.2") -> list[Problem]:
    from datasets import load_dataset
    ds = load_dataset("bigcode/bigcodebench", split=version, trust_remote_code=True)
    out = []
    for row in ds:
        units = split_bigcodebench(row)
        out.append(Problem(
            problem_id=f"bcb/{row['task_id']}",
            source="bigcodebench",
            prompt=row.get("complete_prompt", ""),
            units=units,
            canonical_solution=(row.get("complete_prompt", "") + row.get("canonical_solution", "")),
            style="call",
            meta={"entry_point": row.get("entry_point")},
        ))
        if limit and len(out) >= limit:
            break
    return _filter(out, min_tests)


LOADERS = {
    "humaneval": load_humaneval, "mbpp": load_mbpp, "apps": load_apps,
    "taco": load_taco, "livecodebench": load_livecodebench, "bigcodebench": load_bigcodebench,
}


if __name__ == "__main__":
    # Smoke-test only the small, stable, fast benchmarks (HumanEval + MBPP).
    he = load_humaneval(min_tests=1, limit=5)
    print(f"HumanEval: {len(he)} problems; first has {he[0].n_tests()} test units, "
          f"prompt starts: {he[0].prompt[:40]!r}")
    from grouping import assign_groups
    print("  L2 groups of problem 0:", assign_groups(he[0].units, "l2"))
    assert he and he[0].n_tests() >= 1

    mb = load_mbpp(min_tests=1, limit=5)
    print(f"MBPP: {len(mb)} problems; first has {mb[0].n_tests()} test units")
    assert mb and mb[0].n_tests() >= 1
    print("\nSMOKE TEST PASSED (HumanEval + MBPP). TACO/LiveCodeBench loaders run on the box.")
