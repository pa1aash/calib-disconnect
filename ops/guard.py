"""Cost guard: stops the pod when (a) the job queue is empty, (b) no progress line was written for
stall_s seconds, or (c) the GPU-hour cap is reached. Runs on the pod or locally against the API; the
queue and progress files are read through a reader (local files, or over SSH).

(c) is checked first (it is the hard cost limit), then (a) after an optional grace period that lets the
operator sync before the pod stops, then (b). Time, sleeping, the API, and the readers are injected.
"""

from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from . import progress
from .redact import redact, scrub

PILOT_BUDGET_GPU_HOURS = 6.0
CONTINGENCY = 0.25
DEFAULT_GPU_HOUR_CAP = PILOT_BUDGET_GPU_HOURS * (1 + CONTINGENCY)   # 7.5
DEFAULT_STALL_S = 45 * 60

REASON_EMPTY, REASON_STALL, REASON_CAP = "queue_empty", "no_progress", "gpu_hour_cap"


@dataclass
class GuardConfig:
    stall_s: float = DEFAULT_STALL_S
    gpu_hour_cap: float = DEFAULT_GPU_HOUR_CAP
    poll_s: float = 60.0
    empty_grace_s: float = 0.0
    terminate: bool = False


class LocalReader:
    def __init__(self, run_root: Path) -> None:
        self.root = Path(run_root)

    def read_text(self, rel: str) -> str | None:
        p = self.root / rel
        try:
            return p.read_text() if p.is_file() else None
        except OSError:
            return None


class SshReader:
    """Reads <remote_root>/<rel> with `ssh ... cat`. Host, port, and key come from the caller."""

    def __init__(self, host: str, port: str, key: str, remote_root: str, user: str = "root",
                 runner: Callable[..., Any] = subprocess.run) -> None:
        self.host, self.port, self.key, self.remote_root, self.user, self.runner = host, port, key, remote_root, user, runner

    def command(self, rel: str, shown: bool = False) -> list[str]:
        h, p, k = (redact(self.host), redact(self.port), redact(self.key)) if shown else (self.host, self.port, self.key)
        return ["ssh", "-p", p, "-i", k, "-o", "BatchMode=yes", "-o", "ConnectTimeout=20",
                f"{self.user}@{h}", "cat", f"{self.remote_root}/{rel}"]

    def read_text(self, rel: str) -> str | None:
        try:
            r = self.runner(self.command(rel), capture_output=True, text=True, timeout=60)
        except (OSError, subprocess.SubprocessError):
            return None
        return r.stdout if r.returncode == 0 else None


class Guard:
    def __init__(self, cfg: GuardConfig, api: Any, pod_id: str, launched_ts: float, reader: Any,
                 clock: Callable[[], float] = time.time, sleep: Callable[[float], None] = time.sleep,
                 on_stop: Callable[[str, float], None] | None = None, out: Callable[[str], None] = print) -> None:
        self.cfg, self.api, self.pod_id, self.launched_ts = cfg, api, pod_id, launched_ts
        self.reader, self.clock, self.sleep, self.on_stop, self.out = reader, clock, sleep, on_stop, out
        self.started_ts = clock()
        self._empty_since: float | None = None

    def gpu_hours(self) -> float:
        return max(0.0, self.clock() - self.launched_ts) / 3600.0

    def check(self) -> str | None:
        now = self.clock()
        if self.gpu_hours() >= self.cfg.gpu_hour_cap:
            return REASON_CAP
        if progress.queue_is_empty(self.reader.read_text(f"logs/{progress.QUEUE_NAME}")):
            if self._empty_since is None:
                self._empty_since = now
            if now - self._empty_since >= self.cfg.empty_grace_s:
                return REASON_EMPTY
        else:
            self._empty_since = None
        last = progress.last_progress_ts(self.reader.read_text(f"logs/{progress.PROGRESS_NAME}"))
        ref = max(self.started_ts, last if last is not None else self.started_ts)
        if now - ref >= self.cfg.stall_s:
            return REASON_STALL
        return None

    def stop(self, reason: str) -> None:
        self.out(f"[guard] stopping pod {redact(self.pod_id)}: {reason} (gpu_hours={self.gpu_hours():.3f})")
        if self.cfg.terminate:
            self.api.terminate_pod(self.pod_id)
        else:
            self.api.stop_pod(self.pod_id)
        if self.on_stop:
            self.on_stop(reason, self.clock())

    def run(self, max_polls: int | None = None) -> str | None:
        n = 0
        while max_polls is None or n < max_polls:
            n += 1
            reason = self.check()
            if reason:
                try:
                    self.stop(reason)
                    return reason
                except Exception as exc:  # noqa: BLE001  retry on the next poll; never loop silently
                    self.out(f"[guard] stop failed, will retry: {scrub(str(exc))[:200]}")
            self.sleep(self.cfg.poll_s)
        return None
