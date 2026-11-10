"""HumanEval+ v0.1.10 and MBPP+ v0.2.0 (with the pinned ground-truth patch): problems and suites.

Every file is read only after its byte count and SHA-256 match pins.json. The MBPP+ patch is the data
transform of evalplus tools/mbpp/fix_v020.py at commit 26d6d00 (pinned, SHA-256 in pins.json),
re-expressed as a pure function; tests execute the pinned file and compare the two results.
"""

from __future__ import annotations

import ast
import copy
import gzip
import json
import textwrap
from pathlib import Path
from typing import Any, Mapping

from pipeline.contracts import constants
from pipeline.contracts.schemas import Problem, TestSuite

from . import pins as pinmod
from .inputs import input_set_sha256

# EvalPlus 0.3.1 config: DEFAULT_MIN_TIME_LIMIT = 1.0, DEFAULT_GT_TIME_LIMIT_FACTOR = 4.0
TIME_LIMIT_RULE = f"evalplus=={constants.EVALPLUS_TOOL_VERSION}:max(1.0, 4.0*ref_time)"

# (row index in MbppPlus.jsonl v0.2.0, task ID, replacement canonical solution). Same strings as fix().
MBPP_PATCH: tuple[tuple[int, str, str], ...] = (
    (215, "Mbpp/459", """
def remove_uppercase(str1):
  return ''.join(c for c in str1 if not c.isupper())
"""),
    (55, "Mbpp/102", """
def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])
"""),
    (236, "Mbpp/559", """
def max_sub_array_sum(arr, n):
    max_so_far = arr[0] if len(arr) else 0
    max_ending_here = arr[0] if len(arr) else 0
    for i in range(1, n):
        max_ending_here = max(arr[i], max_ending_here + arr[i])
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far
"""),
)


def apply_mbpp_patch(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """fix_v020.fix as a pure function: returns a patched deep copy; asserts each row index holds the
    expected task ID before replacing its canonical solution."""
    data = copy.deepcopy(rows)
    for n, task_id, solution in MBPP_PATCH:
        assert data[n]["task_id"] == task_id, f"row {n} is {data[n]['task_id']}, expected {task_id}"
        data[n]["canonical_solution"] = solution
    return data


def read_jsonl_gz(path: Path) -> list[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_humaneval_plus(cache_dir: Path) -> tuple[list[dict[str, Any]], str]:
    pin = pinmod.PINS["humaneval_plus"]
    path = pinmod.locate_verified(pin, cache_dir)
    rows = read_jsonl_gz(path)
    if len(rows) != 164:
        raise pinmod.PinError(f"HumanEval+ has {len(rows)} rows, expected 164")
    return rows, pin.sha256


def read_mbpp_plus_raw(cache_dir: Path) -> tuple[list[dict[str, Any]], str, str]:
    """(unpatched rows of MbppPlus.jsonl v0.2.0, its SHA-256, the patch file SHA-256). Both files are
    verified against their pins first."""
    pin = pinmod.PINS["mbpp_plus"]
    patch_pin = pinmod.PINS["mbpp_plus_patch"]
    path = pinmod.locate_verified(pin, cache_dir)
    pinmod.locate_verified(patch_pin, cache_dir)  # the patch file must be the pinned one
    rows = read_jsonl_gz(path)
    ids = {r["task_id"] for r in rows}
    assert len(rows) == 378 and len(ids) == 378, f"MBPP+ has {len(rows)} rows ({len(ids)} distinct IDs)"
    assert not (ids & set(constants.MBPP_PLUS_REMOVED_IDS)), "a removed MBPP+ ID is present"
    return rows, pin.sha256, patch_pin.sha256


def load_mbpp_plus(cache_dir: Path) -> tuple[list[dict[str, Any]], str, str]:
    """(patched rows, MbppPlus.jsonl SHA-256, patch file SHA-256)."""
    rows, sha, patch_sha = read_mbpp_plus_raw(cache_dir)
    return apply_mbpp_patch(rows), sha, patch_sha


def _def_node(code: str, entry_point: str) -> ast.FunctionDef:
    for n in ast.parse(code).body:
        if isinstance(n, ast.FunctionDef) and n.name == entry_point:
            return n
    raise ValueError(f"no def {entry_point}")


def adapt_contract(contract: str, original_solution: str, patched_solution: str, entry_point: str) -> str:
    """Contract text that fits a patched solution.

    The EvalPlus contract is written against the parameter names of the ORIGINAL canonical solution
    and indented to match it. The pinned patch renames parameters of Mbpp/102 (word -> snake_str) and
    Mbpp/559 (a, size -> arr, n) and re-indents the body, so the stored contract would raise
    NameError or IndentationError when spliced into the patched solution. This renames the
    parameters inside the contract and re-indents it to the patched body. Used only to generate
    agreement inputs; the stored contract and every label input are unchanged.
    """
    old = [a.arg for a in _def_node(original_solution, entry_point).args.args]
    new_def = _def_node(patched_solution, entry_point)
    new = [a.arg for a in new_def.args.args]
    mapping = {o: n for o, n in zip(old, new) if o != n}

    class Rename(ast.NodeTransformer):
        def visit_Name(self, node: ast.Name) -> ast.AST:
            return ast.copy_location(ast.Name(id=mapping.get(node.id, node.id), ctx=node.ctx), node)

    tree = Rename().visit(ast.parse(textwrap.dedent(contract)))
    lines = patched_solution.split("\n")
    def_idx = next(i for i, ln in enumerate(lines) if ln.startswith(f"def {entry_point}"))
    body_line = next(ln for ln in lines[def_idx + 1:] if ln.strip())
    indent = body_line[: len(body_line) - len(body_line.lstrip())]
    text = ast.unparse(tree)
    return "\n" + "\n".join(indent + ln for ln in text.split("\n")) + "\n"


def generation_contracts(raw_rows: list[dict[str, Any]], patched_rows: list[dict[str, Any]]) -> dict[str, str]:
    """task ID -> adapted contract, for the rows the patch changed."""
    raw = {r["task_id"]: r for r in raw_rows}
    out = {}
    for r in patched_rows:
        o = raw[r["task_id"]]
        if r["canonical_solution"] != o["canonical_solution"]:
            out[r["task_id"]] = adapt_contract(r["contract"], o["canonical_solution"], r["canonical_solution"],
                                               r["entry_point"])
    return out


def _problem(row: Mapping[str, Any], benchmark: str, source_sha256: str, patched: bool) -> Problem:
    if benchmark == "humaneval_plus":
        # HumanEval stores only the function body as canonical_solution; the complete program is
        # prompt + body, so that is what Problem.canonical_solution holds (it parses and runs).
        solution = row["prompt"] + row["canonical_solution"]
    else:
        solution = row["canonical_solution"]
    return Problem(problem_id=row["task_id"], benchmark=benchmark, prompt=row["prompt"],
                   entry_point=row["entry_point"], canonical_solution=solution, io_kind="function",
                   release_date=None, starter_code=None, source_sha256=source_sha256, patched=patched)


def humaneval_plus_problems(rows: list[dict[str, Any]], sha: str) -> list[Problem]:
    return [_problem(r, "humaneval_plus", sha, False) for r in rows]


def mbpp_plus_problems(rows: list[dict[str, Any]], sha: str) -> list[Problem]:
    patched = set(constants.MBPP_PATCHED_IDS)
    return [_problem(r, "mbpp_plus", sha, r["task_id"] in patched) for r in rows]


def evalplus_suites(row: Mapping[str, Any]) -> dict[str, TestSuite]:
    """"O" = base inputs, "E" = base + plus inputs. expected=None: outputs are recomputed from the
    canonical solution by the execute module (so the patched solutions define the labels)."""
    pid = row["task_id"]
    base = tuple(tuple(i) for i in row["base_input"])
    plus = tuple(tuple(i) for i in row["plus_input"])
    atol = float(row.get("atol") or 0.0)
    out = {}
    for sid, inputs in (("O", base), ("E", base + plus)):
        out[sid] = TestSuite(problem_id=pid, suite_id=sid, inputs=inputs, expected=None, atol=atol,
                             time_limit_rule=TIME_LIMIT_RULE, input_set_sha256=input_set_sha256(inputs))
    return out
