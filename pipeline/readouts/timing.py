"""LoRA step-timing probe (pilot throughput probes, design 13; `cfg.extra["timing_only"]`).

Trains the masked LoRA for a few optimizer steps on the capture inputs of the "timing" generation set and
reports seconds per optimizer step and peak memory. It writes no score, adapter, or probe, and no manifest
entry: the result goes to `StageReport.metrics` and `logs/timing_readouts_<model>.json`. The timing capture
stores nothing, so the token layouts come straight from the timing generations through the same layout
code as the real readouts (`layouts.default_layouts_provider` with gen_set="timing"). Labels are
alternating dummies: only speed is measured.
"""

from __future__ import annotations

import json
import resource
import sys
import time

import numpy as np
import pyarrow.parquet as pq

from pipeline.contracts.layout import RunLayout

TIMING_SET = "timing"


def timing_uids(layout: RunLayout, model_key: str, benches) -> list[str]:
    uids: list[str] = []
    for b in benches:
        s = 0
        while layout.generation_shard(model_key, b, TIMING_SET, s).exists():
            uids += pq.read_table(layout.generation_shard(model_key, b, TIMING_SET, s), columns=["sample_uid"]).column(
                "sample_uid").to_pylist()
            s += 1
    return sorted(uids)


def _peak_memory() -> tuple[int, str]:
    import torch
    if torch.cuda.is_available():
        return int(torch.cuda.max_memory_allocated()), "cuda_max_memory_allocated"
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(rss if sys.platform == "darwin" else rss * 1024), "process_max_rss"


def time_lora_steps(backend, n_steps: int, lr: float = 1e-4) -> dict:
    """Train a fresh masked LoRA on all of `backend.layouts` for n_steps optimizer steps; nothing is saved."""
    import torch
    n = len(backend.layouts)
    if n == 0:
        return {"n_samples": 0, "note": "no timing samples"}
    y = (np.arange(n) % 2).astype(np.int64)
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()
    with backend.st() as tr:
        t0 = time.perf_counter()
        tr.fit(np.arange(n), y, lr=lr, total_steps=n_steps, schedule_steps=n_steps, seed=0)
        dt = time.perf_counter() - t0
    mem, kind = _peak_memory()
    return {"n_samples": n, "steps": n_steps, "seconds": dt, "seconds_per_step": dt / n_steps,
            "peak_memory_bytes": mem, "memory_kind": kind}


def write_timing_log(layout: RunLayout, model_key: str, result: dict) -> None:
    layout.logs.mkdir(parents=True, exist_ok=True)
    (layout.logs / f"timing_readouts_{model_key}.json").write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
