"""Canonical hash encodings shared by every module.

Every hash that the design defines (per-sample seeds, fold assignment, execution cache keys, config
hashes) is computed here and only here, so that two modules can never disagree on an encoding.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable

SEP = "\x1f"  # ASCII unit separator between fields of a hashed tuple


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def sha256_file(path: str | Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def tuple_digest(fields: Iterable[Any]) -> bytes:
    """SHA-256 digest of fields joined by SEP, each rendered with str()."""
    return hashlib.sha256(SEP.join(str(f) for f in fields).encode("utf-8")).digest()


def sample_seed(model_id: str, revision: str, benchmark: str, problem_id: str, sample_index: int) -> int:
    """Section 5: the first 8 bytes of SHA-256 over (model ID, revision, benchmark, problem ID,
    sample index), read big-endian as an unsigned 64-bit integer. sample_index is 1-based (j = 1..k).
    """
    if sample_index < 1:
        raise ValueError("sample_index is 1-based")
    return int.from_bytes(tuple_digest((model_id, revision, benchmark, problem_id, sample_index))[:8], "big")


def fold_of(fold_seed: int, group_key: str, n_folds: int = 5) -> int:
    """Section 7: fold = SHA-256 of (fold seed, problem ID) modulo 5. For a near-duplicate group
    (section 4), group_key is the group's smallest problem ID (Python string order)."""
    return int.from_bytes(tuple_digest((fold_seed, group_key)), "big") % n_folds


def lcb_agreement_indices(private_inputs: list[str], share: float = 0.20) -> list[int]:
    """Section 4: a fixed SHA-256 hash of each private test's input string selects 20 percent of the
    private tests of a problem as agreement inputs. The tests are ordered by (SHA-256 of the input
    string, position) and the first floor(share * n + 0.5) are selected, so a problem with fewer
    than 5 private tests gets 0 or 1 agreement inputs, as the design states. Returns sorted indices.
    """
    n = len(private_inputs)
    n_sel = int(math.floor(share * n + 0.5))
    order = sorted(range(n), key=lambda i: (hashlib.sha256(private_inputs[i].encode("utf-8")).hexdigest(), i))
    return sorted(order[:n_sel])


def canonical_json(obj: Any) -> str:
    """Deterministic JSON: sorted keys, no whitespace, finite floats only."""

    def _check(o: Any) -> Any:
        if isinstance(o, float) and not math.isfinite(o):
            raise ValueError("non-finite float in canonical JSON")
        return o

    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=_default)


def _default(o: Any) -> Any:
    if hasattr(o, "to_dict"):
        return o.to_dict()
    if isinstance(o, (set, frozenset)):
        return sorted(o)
    if isinstance(o, Path):
        return str(o)
    raise TypeError(f"not JSON serializable: {type(o).__name__}")


def config_hash(config: Any) -> str:
    """SHA-256 of the canonical JSON of a configuration object."""
    return sha256_text(canonical_json(config))


def exec_cache_key(
    normalized_code: str,
    problem_id: str,
    suite_id: str,
    evaluator_version: str,
    time_limit_rule: str,
    memory_limit_bytes: int,
    interpreter_sha256: str,
) -> str:
    """Section 6 (red team V14a): SHA-256 of (normalized code, problem ID, suite ID or agreement
    input-set ID, evaluator version, time-limit rule and memory limit, interpreter binary hash)."""
    return tuple_digest((normalized_code, problem_id, suite_id, evaluator_version, time_limit_rule,
                         memory_limit_bytes, interpreter_sha256)).hex()
