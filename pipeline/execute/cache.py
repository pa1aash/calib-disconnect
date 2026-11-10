"""Execution cache (design section 6, red team V14a).

SQLite file at ``layout.exec_cache``. Key: ``hashing.exec_cache_key(normalize_code(code), problem_id,
suite id, evaluator version, time-limit rule, memory limit, interpreter hash)``, computed by
``SandboxExecutor.cache_key``. Value: the ``ExecutionResult`` (pass, failure code, per-test outcomes,
outputs for the agreement input set, runtime). Identical programs across samples and models share one
entry.

Flakiness audit: a seeded 1 percent (``constants.CACHE_AUDIT_SHARE``) of cache hits is re-executed;
any difference in (passed, failure, per_test, outputs) is appended to ``logs/cache_audit.jsonl``. The
cached value is kept; the log is the record. ``sandbox_error`` results are never cached.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
from pathlib import Path
from typing import Callable

from pipeline.contracts import constants
from pipeline.contracts.manifest import utc_now
from pipeline.contracts.schemas import ExecutionResult

NEVER_CACHED = frozenset({"sandbox_error"})


def _comparable(r: ExecutionResult) -> dict:
    return {"passed": r.passed, "failure": r.failure, "per_test": list(r.per_test),
            "outputs": None if r.outputs is None else list(r.outputs)}


class ExecCache:
    def __init__(self, path: Path | str, *, audit_share: float = constants.CACHE_AUDIT_SHARE, audit_seed: int = 0,
                 audit_log: Path | str | None = None):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.audit_share = audit_share
        self.audit_seed = audit_seed
        self.audit_log = Path(audit_log) if audit_log is not None else None
        self._lock = threading.Lock()
        self._db = sqlite3.connect(str(self.path), check_same_thread=False)
        self._db.execute("PRAGMA journal_mode=WAL")
        self._db.execute("PRAGMA synchronous=NORMAL")
        self._db.execute("CREATE TABLE IF NOT EXISTS exec_cache (key TEXT PRIMARY KEY, problem_id TEXT NOT NULL, "
                         "suite_id TEXT NOT NULL, value TEXT NOT NULL, created_utc TEXT NOT NULL)")
        self._db.commit()
        self.hits = self.misses = self.puts = self.audits = self.mismatches = 0

    # -- access
    def get(self, key: str) -> ExecutionResult | None:
        with self._lock:
            row = self._db.execute("SELECT value FROM exec_cache WHERE key = ?", (key,)).fetchone()
            if row is None:
                self.misses += 1
                return None
            self.hits += 1
        return ExecutionResult.from_dict(json.loads(row[0]))

    def put(self, result: ExecutionResult) -> bool:
        if result.failure in NEVER_CACHED:
            return False
        with self._lock:
            self._db.execute("INSERT OR REPLACE INTO exec_cache VALUES (?, ?, ?, ?, ?)",
                             (result.cache_key, result.problem_id, result.suite_id,
                              json.dumps(result.to_dict(), sort_keys=True), utc_now()))
            self._db.commit()
            self.puts += 1
        return True

    def __len__(self) -> int:
        with self._lock:
            return self._db.execute("SELECT COUNT(*) FROM exec_cache").fetchone()[0]

    def close(self) -> None:
        with self._lock:
            self._db.commit()
            self._db.close()

    # -- audit
    def should_audit(self, key: str) -> bool:
        """Seeded and a pure function of (seed, key): the same hits are audited on every rerun."""
        d = hashlib.sha256(f"{self.audit_seed}|audit|{key}".encode()).digest()
        return int.from_bytes(d[:8], "big") / 2**64 < self.audit_share

    def audit(self, key: str, cached: ExecutionResult, rerun: Callable[[], ExecutionResult]) -> bool:
        """Re-execute and compare. Returns True on a mismatch (which is also logged)."""
        fresh = rerun()
        with self._lock:
            self.audits += 1
        if _comparable(fresh) == _comparable(cached):
            return False
        with self._lock:
            self.mismatches += 1
            if self.audit_log is not None:
                self.audit_log.parent.mkdir(parents=True, exist_ok=True)
                with open(self.audit_log, "a") as f:
                    f.write(json.dumps({"utc": utc_now(), "key": key, "problem_id": cached.problem_id,
                                        "suite_id": cached.suite_id, "cached": _comparable(cached),
                                        "rerun": _comparable(fresh)}, sort_keys=True) + "\n")
        return True

    def stats(self) -> dict[str, int]:
        return {"hits": self.hits, "misses": self.misses, "puts": self.puts, "audits": self.audits,
                "audit_mismatches": self.mismatches}
