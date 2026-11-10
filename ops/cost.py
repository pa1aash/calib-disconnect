"""Cost ledger: runs/COST_LEDGER.csv, columns pipeline.contracts.layout.COST_LEDGER_COLUMNS.

A row is appended at every launch with the hourly price the operator supplies (required, with the
text naming where the price came from), and completed at stop with GPU-hours and cost. GPU-hours are
wall-clock hours of one GPU from pod creation to stop.
"""

from __future__ import annotations

import csv
import datetime as _dt
import math
import os
import tempfile
from pathlib import Path
from typing import Any

from pipeline.contracts.layout import COST_LEDGER, COST_LEDGER_COLUMNS

from .redact import redact

TS_FMT = "%Y-%m-%dT%H:%M:%SZ"


class LedgerError(ValueError):
    pass


def parse_utc(s: str) -> _dt.datetime:
    return _dt.datetime.strptime(s, TS_FMT).replace(tzinfo=_dt.timezone.utc)


def fmt_utc(t: _dt.datetime) -> str:
    return t.astimezone(_dt.timezone.utc).strftime(TS_FMT)


def validate_price(hourly_price_usd: Any, price_source: Any) -> float:
    try:
        price = float(hourly_price_usd)
    except (TypeError, ValueError):
        raise LedgerError("an hourly price in USD is required (--hourly-price-usd)") from None
    if not math.isfinite(price) or price <= 0:
        raise LedgerError("the hourly price must be a positive finite number")
    if not price_source or not str(price_source).strip():
        raise LedgerError("a price source is required (--price-source), for example where the price was read")
    return price


def read_rows(path: Path = COST_LEDGER) -> list[dict[str, str]]:
    path = Path(path)
    if not path.is_file():
        return []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def _write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".ledger.", suffix=".tmp")
    with os.fdopen(fd, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COST_LEDGER_COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, path)


def append_launch(path: Path, *, launch: _dt.datetime, pod_id: str, gpu_type: str, hourly_price_usd: Any,
                  price_source: str, run_id: str, git_sha: str) -> dict[str, str]:
    price = validate_price(hourly_price_usd, price_source)
    row = {c: "" for c in COST_LEDGER_COLUMNS}
    row.update({"launch_utc": fmt_utc(launch), "pod_id_prefix": redact(pod_id), "gpu_type": gpu_type,
                "hourly_price_usd": repr(price), "price_source": str(price_source).strip(), "run_id": run_id,
                "git_sha": git_sha})
    rows = read_rows(path)
    rows.append(row)
    _write_rows(path, rows)
    return row


def open_row_index(rows: list[dict[str, str]], pod_id: str, run_id: str | None = None) -> int | None:
    pref = redact(pod_id)
    for i in range(len(rows) - 1, -1, -1):
        r = rows[i]
        if r["pod_id_prefix"] == pref and not r["stop_utc"] and (run_id is None or r["run_id"] == run_id):
            return i
    return None


def launched_at(path: Path, pod_id: str, run_id: str | None = None) -> _dt.datetime | None:
    rows = read_rows(path)
    i = open_row_index(rows, pod_id, run_id)
    return parse_utc(rows[i]["launch_utc"]) if i is not None else None


def complete(path: Path, *, pod_id: str, stop: _dt.datetime, reason: str, run_id: str | None = None) -> dict[str, str]:
    rows = read_rows(path)
    i = open_row_index(rows, pod_id, run_id)
    if i is None:
        raise LedgerError(f"no open ledger row for pod {redact(pod_id)}")
    r = rows[i]
    hours = max(0.0, (stop - parse_utc(r["launch_utc"])).total_seconds() / 3600.0)
    r.update({"stop_utc": fmt_utc(stop), "gpu_hours": f"{hours:.4f}",
              "cost_usd": f"{hours * float(r['hourly_price_usd']):.4f}", "reason_stopped": reason})
    _write_rows(path, rows)
    return r


def summarize(path: Path = COST_LEDGER) -> dict[str, float]:
    rows = read_rows(path)
    done = [r for r in rows if r["stop_utc"]]
    return {"rows": float(len(rows)), "open_rows": float(len(rows) - len(done)),
            "gpu_hours": sum(float(r["gpu_hours"]) for r in done),
            "cost_usd": sum(float(r["cost_usd"]) for r in done)}
