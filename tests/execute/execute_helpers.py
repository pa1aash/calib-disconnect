"""Builds Problem and TestSuite objects from the pinned EvalPlus files in the benchmark cache."""

import gzip
import json
from pathlib import Path

from pipeline.contracts.schemas import Problem, TestSuite

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "docs" / "s7" / "parts" / "bench-A2" / "cache" / "evalplus"
HEPLUS = CACHE / "heplus_v0.1.10" / "HumanEvalPlus.jsonl.gz"
MBPPPLUS = CACHE / "mbppplus_v0.2.0" / "MbppPlus.jsonl.gz"


def _read(path):
    if not path.exists():
        return None
    with gzip.open(path, "rt") as f:
        return {r["task_id"]: r for r in map(json.loads, f)}


def load_heplus():
    return _read(HEPLUS)


def load_mbppplus():
    rows = _read(MBPPPLUS)
    if rows is None:
        return None
    from evalplus.data.mbpp import mbpp_deserialize_inputs

    for tid, r in rows.items():
        r["base_input"] = mbpp_deserialize_inputs(tid, r["base_input"])
        r["plus_input"] = mbpp_deserialize_inputs(tid, r["plus_input"])
    return rows


def build(rows, task_id, benchmark, max_plus=None):
    """(Problem, {"O": TestSuite, "E": TestSuite}) with expected=None (recomputed from the reference)."""
    r = rows[task_id]
    sol = r["prompt"] + r["canonical_solution"] if benchmark == "humaneval_plus" else r["canonical_solution"]
    p = Problem(task_id, benchmark, r["prompt"], r["entry_point"], sol, "function", None)
    base = tuple(tuple(i) for i in r["base_input"])
    plus = tuple(tuple(i) for i in r["plus_input"])
    if max_plus is not None:
        plus = plus[:max_plus]
    atol = float(r.get("atol") or 0.0)
    rule = "evalplus max(1.0, 4.0*ref)"
    suites = {"O": TestSuite(task_id, "O", base, None, atol, rule, ""),
              "E": TestSuite(task_id, "E", base + plus, None, atol, rule, "")}
    return p, suites
