"""Heartbeat and queue files under <run>/logs/, read by the guard.

logs/progress.jsonl   one JSON object per line: ts, job, start, end, status, outputs (plus seconds, note)
logs/queue.json       {"pending": n, "running": bool, "finished": bool, "ts": ...}
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import tempfile
from pathlib import Path
from typing import Any

PROGRESS_NAME = "progress.jsonl"
QUEUE_NAME = "queue.json"


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(s: str) -> float:
    return _dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.timezone.utc).timestamp()


def heartbeat(logs_dir: Path, row: dict[str, Any]) -> None:
    logs_dir = Path(logs_dir)
    logs_dir.mkdir(parents=True, exist_ok=True)
    row = {"ts": now_iso(), **row}
    with open(logs_dir / PROGRESS_NAME, "a") as f:
        f.write(json.dumps(row, sort_keys=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def write_queue(logs_dir: Path, pending: int, running: bool, finished: bool = False) -> None:
    logs_dir = Path(logs_dir)
    logs_dir.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=logs_dir, prefix=".queue.", suffix=".tmp")
    with os.fdopen(fd, "w") as f:
        json.dump({"pending": pending, "running": running, "finished": finished, "ts": now_iso()}, f)
    os.replace(tmp, logs_dir / QUEUE_NAME)


def last_progress_ts(text: str | None) -> float | None:
    """Epoch seconds of the last parseable line of a progress.jsonl text, or None."""
    if not text:
        return None
    for line in reversed(text.strip().splitlines()):
        try:
            return parse_iso(json.loads(line)["ts"])
        except (ValueError, KeyError, TypeError):
            continue
    return None


def queue_is_empty(text: str | None) -> bool:
    """True when a queue file exists and says nothing is pending or running, or the runner finished."""
    if not text:
        return False
    try:
        q = json.loads(text)
    except ValueError:
        return False
    return bool(q.get("finished")) or (int(q.get("pending", 1)) == 0 and not q.get("running", True))
