"""Held-out agreement inputs for HumanEval+ and MBPP+ (design section 4, red team V14b).

Inputs come from EvalPlus TypedMutGen seeded by the base inputs only, filtered by the problem's own
contract (TypedMutGen runs contract + canonical solution on each candidate, which are trusted
benchmark files), deduplicated against every label input after canonicalization, and capped at 50.

Determinism. TypedMutGen draws only from Python's `random`, which is seeded per problem from
hashing.tuple_digest(("agree", seed, problem_id)). Two things in EvalPlus 0.3.1 would still vary
between processes through string hash randomization, and are fixed here without changing the
sampling distribution:
  * the ingredient pools are Python sets; DeterministicTypedMutGen keeps them in insertion order;
  * the set mutator iterates a set; the re-registered mutator iterates it in canonical order.
The attempt count is capped (MAX_ATTEMPTS) so that the output does not depend on wall-clock time;
a wall-clock soft limit and a hard process timeout exist only as safety nets and are recorded.

Problems run in worker subprocesses (agreement_worker) so that a hang (TypedMutGen.mutate can loop
forever on an input it cannot change) or a crash costs one problem, never the run. A timed-out worker
is killed and replaced.
"""

from __future__ import annotations

import json
import random
import selectors
import subprocess
import sys
import time
from typing import Any, Mapping, Sequence

from pipeline.contracts import constants, hashing
from pipeline.contracts.layout import REPO_ROOT

from .inputs import canonical_repr, decode_inputs, encode_input

N_GENERATE = 100          # candidates requested from TypedMutGen before deduplication
MAX_ATTEMPTS = 20_000     # mutation attempts per problem (deterministic stop)
SOFT_TIMEOUT_S = 40.0     # wall-clock safety net inside the child
HARD_TIMEOUT_S = 90.0     # the parent kills the child after this long


def problem_seed(seed: int, problem_id: str) -> int:
    return int.from_bytes(hashing.tuple_digest(("agree", seed, problem_id))[:8], "big")


# ---------------------------------------------------------------------------------------------------
# Deterministic TypedMutGen
# ---------------------------------------------------------------------------------------------------
class _OrderedPool:
    """Insertion-ordered set exposing the few set operations TypedMutGen uses."""

    def __init__(self) -> None:
        self._d: dict[Any, None] = {}

    def add(self, x: Any) -> None:
        self._d[x] = None

    def __iter__(self):
        return iter(self._d)

    def __len__(self) -> int:
        return len(self._d)

    def __bool__(self) -> bool:
        return bool(self._d)


def _install_deterministic_set_mutator() -> None:
    """Replace the (set,) entry of TypedMutGen.typed_mutate by one that does not depend on set order."""
    from evalplus.gen.type_mut import TypedMutGen

    disp = TypedMutGen.__dict__["typed_mutate"]

    def typed_mutate_set(self, seed_input):  # same logic as EvalPlus; only the iteration order differs
        return set(self.typed_mutate(sorted(seed_input, key=lambda v: canonical_repr((v,)))))

    disp.add((set,), typed_mutate_set)


def make_generator(base_inputs: list, entry_point: str, contract_code: str):
    from evalplus.gen.type_mut import MAX_MULTI_STEP_SIZE, TypedMutGen
    from evalplus.gen.util import trusted_check_exec

    _install_deterministic_set_mutator()

    class DeterministicTypedMutGen(TypedMutGen):
        def __init__(self, inputs, signature, contract):
            super().__init__(inputs, signature, contract)
            self.ingredients = {int: _OrderedPool(), float: _OrderedPool(), str: _OrderedPool(),
                                complex: _OrderedPool()}
            for x in inputs:
                self.fetch_ingredient(x)
            self.attempts = 0

        def generate(self, num: int):  # EvalPlus TypedMutGen.generate with a deterministic attempt cap
            start = time.time()
            while len(self.new_inputs) < num and self.attempts < MAX_ATTEMPTS and time.time() - start < self.timeout:
                self.attempts += 1
                new_input = self.seed_selection()
                for _ in range(random.randint(1, MAX_MULTI_STEP_SIZE)):
                    new_input = self.mutate(new_input)
                if hash(str(new_input)) not in self.seed_hash:
                    if trusted_check_exec(self.contract, [new_input], self.entry_point):
                        self.typed_fetch(new_input)
                        self.seed_pool.append(new_input)
                        self.new_inputs.append(new_input)
                    self.seed_hash.add(hash(str(new_input)))
            return self.new_inputs[:num]

    gen = DeterministicTypedMutGen(base_inputs, entry_point, contract_code)
    gen.timeout = SOFT_TIMEOUT_S
    return gen


def contract_code(row: Mapping[str, Any]) -> str:
    """Prompt + contract + canonical solution, as EvalPlus inputgen builds it."""
    if row["task_id"].startswith("HumanEval/"):
        return row["prompt"] + row["contract"] + row["canonical_solution"]
    lines = row["canonical_solution"].split("\n")
    idx = lines.index(next(line for line in lines if line.startswith(f"def {row['entry_point']}")))
    lines.insert(idx + 1, row["contract"])
    return row["prompt"] + "\n".join(lines)


# ---------------------------------------------------------------------------------------------------
# One problem
# ---------------------------------------------------------------------------------------------------
def compute_agreement(row: Mapping[str, Any], label_inputs: Sequence[Sequence[Any]], seed: int,
                      n_generate: int = N_GENERATE, cap: int = constants.AGREEMENT_INPUT_CAP) -> dict[str, Any]:
    """Pure function of its arguments (given a fixed process): returns {"inputs": [...JSON form...],
    "stats": {...}}. Seeds `random`; call it in a child process or accept that `random` is reseeded."""
    pid = row["task_id"]
    random.seed(problem_seed(seed, pid))
    base = decode_inputs(pid, row["base_input"])
    gen = make_generator(base, row["entry_point"], contract_code(row))
    new = gen.generate(n_generate)
    label_canon = {canonical_repr(a) for a in decode_inputs(pid, label_inputs)}
    kept: list[list[Any]] = []
    seen: set[str] = set()
    st = {"generated": len(new), "attempts": gen.attempts, "removed_label_duplicates": 0,
          "removed_self_duplicates": 0, "removed_roundtrip": 0, "dropped_over_cap": 0, "kept": 0,
          "status": "ok"}
    for cand in new:
        c = canonical_repr(cand)
        try:
            enc = encode_input(pid, cand)
            ok = canonical_repr(decode_inputs(pid, [enc])[0]) == c
        except (ValueError, TypeError, KeyError, IndexError, OverflowError):
            enc, ok = None, False
        if not ok:
            st["removed_roundtrip"] += 1  # not representable in the JSON form of the suite
        elif c in label_canon:
            st["removed_label_duplicates"] += 1
        elif c in seen:
            st["removed_self_duplicates"] += 1
        elif len(kept) >= cap:
            st["dropped_over_cap"] += 1
        else:
            seen.add(c)
            kept.append(enc)
    st["kept"] = len(kept)
    if not kept:
        st["status"] = "empty"
    return {"inputs": kept, "stats": st}


# ---------------------------------------------------------------------------------------------------
# Isolation: long-lived worker subprocesses (python -I -m pipeline.data.agreement_worker)
# ---------------------------------------------------------------------------------------------------
READY = "@@READY@@"
RESULT = "@@RESULT@@ "


def _empty(status: str) -> dict[str, Any]:
    return {"inputs": [], "stats": {"generated": 0, "kept": 0, "status": status}}


class _Worker:
    def __init__(self) -> None:
        self.proc = subprocess.Popen([sys.executable, "-I", "-m", "pipeline.data.agreement_worker"],
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                     text=True, bufsize=1, cwd=str(REPO_ROOT))
        self.ready = False
        self.job: str | None = None
        self.started = 0.0

    def send(self, job_id: str, payload: dict[str, Any]) -> None:
        self.job = job_id
        self.started = time.time()
        assert self.proc.stdin is not None
        self.proc.stdin.write(json.dumps(payload) + "\n")
        self.proc.stdin.flush()

    def kill(self) -> None:
        try:
            self.proc.kill()
        except OSError:
            pass
        for f in (self.proc.stdin, self.proc.stdout):
            try:
                f.close()  # type: ignore[union-attr]
            except OSError:
                pass
        self.proc.wait(timeout=10)

    def close(self) -> None:
        try:
            assert self.proc.stdin is not None
            self.proc.stdin.close()
            self.proc.wait(timeout=10)
        except (OSError, subprocess.TimeoutExpired):
            self.kill()


def run_isolated(jobs: Sequence[tuple[str, Mapping[str, Any], Sequence[Sequence[Any]]]], seed: int, *,
                 workers: int = 4, n_generate: int = N_GENERATE, cap: int = constants.AGREEMENT_INPUT_CAP,
                 hard_timeout_s: float = HARD_TIMEOUT_S, _sleep_s: float = 0.0) -> dict[str, dict[str, Any]]:
    """Run compute_agreement for each (problem_id, record, label_inputs) in worker subprocesses, at
    most `workers` at a time. A job that exceeds hard_timeout_s kills its worker and gives an empty
    input list with status "timeout"; a crash gives status "error: ...". Never raises for a job."""
    results: dict[str, dict[str, Any]] = {}
    pending = list(jobs)
    if not pending:
        return results
    sel = selectors.DefaultSelector()
    pool: list[_Worker] = []

    def spawn() -> _Worker:
        w = _Worker()
        assert w.proc.stdout is not None
        sel.register(w.proc.stdout, selectors.EVENT_READ, w)
        pool.append(w)
        return w

    def retire(w: _Worker) -> None:
        try:
            sel.unregister(w.proc.stdout)  # type: ignore[arg-type]
        except (KeyError, ValueError):
            pass
        w.kill()
        pool.remove(w)

    try:
        for _ in range(max(1, min(workers, len(pending)))):
            spawn()
        while pending or any(w.job for w in pool):
            for w in pool:  # hand out work
                if w.ready and w.job is None and pending:
                    pid, row, label = pending.pop(0)
                    w.send(pid, {"row": row, "label": [list(i) for i in label], "seed": seed,
                                 "n_generate": n_generate, "cap": cap, "sleep_s": _sleep_s})
            for key, _ in sel.select(timeout=1.0):
                w = key.data
                line = w.proc.stdout.readline()  # type: ignore[union-attr]
                if line == "":  # worker exited
                    if w.job is not None:
                        results[w.job] = _empty("error: worker exited without a result")
                    retire(w)
                    if pending or any(x.job for x in pool):
                        spawn()
                elif line.startswith(READY):
                    w.ready = True
                elif line.startswith(RESULT) and w.job is not None:
                    results[w.job] = json.loads(line[len(RESULT):])
                    w.job = None
            now = time.time()
            for w in list(pool):
                if w.job is not None and now - w.started > hard_timeout_s:
                    results[w.job] = _empty("timeout")
                    retire(w)
                    if pending:
                        spawn()
    finally:
        for w in list(pool):
            try:
                sel.unregister(w.proc.stdout)  # type: ignore[arg-type]
            except (KeyError, ValueError):
                pass
            w.close()
        sel.close()
    return results
