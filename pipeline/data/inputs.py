"""Input encodings for HumanEval+ and MBPP+ suites.

A TestSuite stores inputs in the EvalPlus JSON form (the form inside HumanEvalPlus.jsonl.gz and
MbppPlus.jsonl.gz): each input is a list of arguments made of lists, numbers, strings, booleans, and
null. MBPP+ needs a per-task step that turns some lists back into tuples, sets, or complex numbers
(EvalPlus `mbpp_deserialize_inputs`). `decode_inputs` applies that step and returns Python objects
ready to be passed as `fn(*args)`. The execute module must call it before running any MBPP+ input.

`canonical_repr` is the canonicalization used to remove agreement inputs that equal a label input.
"""

from __future__ import annotations

import copy
import json
import math
from typing import Any, Iterable, Sequence

from pipeline.contracts import constants, hashing


def decode_inputs(problem_id: str, inputs: Iterable[Sequence[Any]]) -> list[list[Any]]:
    """JSON-form inputs -> Python argument lists (a deep copy; the arguments are never shared)."""
    raw = [json.loads(json.dumps(list(i))) for i in inputs]  # plain lists, fresh objects
    if problem_id.startswith("Mbpp/"):
        from evalplus.data.mbpp import mbpp_deserialize_inputs

        return [list(x) for x in mbpp_deserialize_inputs(problem_id, raw)]
    return raw


def _jsonify(x: Any) -> Any:
    if isinstance(x, (list, tuple)):
        return [_jsonify(v) for v in x]
    if isinstance(x, (set, frozenset)):
        return sorted((_jsonify(v) for v in x), key=repr)
    if isinstance(x, dict):
        return {k: _jsonify(v) for k, v in x.items()}
    return x


def encode_input(problem_id: str, args: Sequence[Any]) -> list[Any]:
    """Python argument list -> EvalPlus JSON form (inverse of decode_inputs for generated inputs)."""
    args = list(args)
    if problem_id.startswith("Mbpp/"):
        from evalplus.data.mbpp import mbpp_serialize_inputs

        args = list(mbpp_serialize_inputs(problem_id, [copy.deepcopy(args)])[0])
    return json.loads(json.dumps(_jsonify(args)))


def _num(x: float, sig: int) -> str:
    if not math.isfinite(x):
        return repr(x)
    return repr(float(f"{x:.{sig}g}"))


def _canon(x: Any, sig: int) -> str:
    if x is None or isinstance(x, (bool, str, bytes)):
        return repr(x)
    if isinstance(x, int):
        return repr(x)
    if isinstance(x, float):
        return _num(x, sig)
    if isinstance(x, complex):
        return f"complex({_num(x.real, sig)},{_num(x.imag, sig)})"
    if isinstance(x, list):
        return "[" + ",".join(_canon(v, sig) for v in x) + "]"
    if isinstance(x, tuple):
        inner = ",".join(_canon(v, sig) for v in x)
        return "(" + inner + ("," if len(x) == 1 else "") + ")"
    if isinstance(x, (set, frozenset)):
        name = "set" if isinstance(x, set) else "frozenset"
        return name + "{" + ",".join(sorted(_canon(v, sig) for v in x)) + "}"
    if isinstance(x, dict):
        items = sorted((_canon(k, sig), _canon(v, sig)) for k, v in x.items())
        return "{" + ",".join(f"{k}:{v}" for k, v in items) + "}"
    return repr(x)


def canonical_repr(args: Sequence[Any], sig: int = constants.AGREEMENT_DEDUP_FLOAT_SIG) -> str:
    """repr of the parsed argument tuple with floats rounded to `sig` significant digits.

    Reading of "containers sorted where the contract makes order irrelevant": sets and frozensets are
    sorted by the canonical text of their elements, and dicts by the canonical text of their keys
    (dict equality ignores order). Lists and tuples keep their order, because the contracts of
    HumanEval+ and MBPP+ treat them as ordered sequences.
    """
    return _canon(tuple(args), sig)


def input_set_sha256(inputs: Sequence[Any]) -> str:
    """SHA-256 of the canonical JSON of the inputs (a list, in suite order)."""
    return hashing.sha256_text(hashing.canonical_json([list(i) if isinstance(i, tuple) else i for i in inputs]))
