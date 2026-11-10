"""Job runner. Stages are resolved through pipeline.contracts.interfaces.STAGES (importlib) and called
with the contract signature run(cfg, layout, manifest, *, dry_run=False) -> StageReport.

Rules:
  * jobs run in dependency order (plans.order_jobs); one model is active at a time;
  * a job whose done marker exists and whose recorded outputs verify against the manifest is skipped;
  * the done marker (state/<job>.done, JSON with the outputs list) is written after success;
  * the manifest is saved after every job, including failed ones (partial entries stay listed);
  * a model-level failure skips that model's remaining jobs and continues with the next model only
    with keep_going; a failure of a model-free job (data) always stops the run;
  * progress is appended to logs/progress.jsonl and the queue state to logs/queue.json;
  * a dry run prints the plan and imports no stage module.
"""

from __future__ import annotations

import gc
import importlib
import json
import os
import platform
import sys
import tempfile
import time
import traceback
from dataclasses import dataclass, field
from importlib import metadata
from pathlib import Path
from typing import Callable

from pipeline.contracts.hashing import config_hash, sha256_file
from pipeline.contracts.interfaces import STAGES, RunConfig, StageReport
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest, git_sha, utc_now

from . import progress
from .plans import Job, Plan, job_config, order_jobs
from .redact import scrub

StageFn = Callable[..., StageReport]
ENV_PACKAGES = ("torch", "transformers", "vllm", "peft", "accelerate", "evalplus", "numpy", "pandas")


def import_stage(stage: str, stages: dict[str, str] | None = None) -> StageFn:
    target = (stages or STAGES)[stage]
    mod, _, fn = target.partition(":")
    return getattr(importlib.import_module(mod), fn)


@dataclass
class JobResult:
    job_id: str
    status: str          # done | skipped_done | failed | skipped_model_failed | skipped_dependency | not_run
    outputs: int = 0
    seconds: float = 0.0
    note: str = ""
    outputs_list: list[str] = field(default_factory=list)


@dataclass
class RunSummary:
    results: list[JobResult] = field(default_factory=list)

    def count(self, status: str) -> int:
        return sum(1 for r in self.results if r.status == status)

    @property
    def failed(self) -> bool:
        return self.count("failed") > 0

    @property
    def exit_code(self) -> int:
        return 1 if (self.failed or self.count("not_run") or self.count("skipped_dependency")) else 0


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp.", suffix=".part")
    with os.fdopen(fd, "w") as f:
        f.write(text)
    os.replace(tmp, path)


class Runner:
    def __init__(self, plan: Plan, layout: RunLayout, *, resolver: Callable[[str], StageFn] | None = None,
                 keep_going: bool = False, dry_run: bool = False, repo_root: Path | None = None,
                 out: Callable[[str], None] = print, clock: Callable[[], float] = time.time,
                 git: str | None = None) -> None:
        self.plan, self.layout, self.cfg = plan, layout, plan.cfg
        self.resolver = resolver or import_stage
        self.keep_going, self.dry_run = keep_going, dry_run
        self.repo_root = repo_root
        self.out, self.clock = out, clock
        self.git = git
        self.jobs = order_jobs(plan.jobs)

    # ---- done markers
    def marker_valid(self, job: Job, manifest: Manifest) -> tuple[bool, str]:
        mk = self.layout.done_marker(job.id)
        if not mk.is_file():
            return False, "no marker"
        try:
            rec = json.loads(mk.read_text())
            outs = list(rec["outputs"])
        except (ValueError, KeyError, TypeError):
            return False, "unreadable marker"
        for rel in outs:
            e = manifest.entries.get(rel)
            p = self.layout.root / rel
            if e is None:
                return False, f"output not in manifest: {rel}"
            if not p.is_file():
                return False, f"output missing: {rel}"
            if sha256_file(p) != e.sha256:
                return False, f"output hash differs from manifest: {rel}"
        return True, "outputs verified"

    def _write_marker(self, job: Job, outputs: list[str], seconds: float) -> None:
        rec = {"job": job.id, "stage": job.stage, "model": job.model_key, "scope": job.scope,
               "gen_set": job.gen_set, "finished_utc": utc_now(), "seconds": round(seconds, 3), "outputs": outputs}
        _atomic_write(self.layout.done_marker(job.id), json.dumps(rec, indent=1) + "\n")

    # ---- manifest setup
    def _prepare(self) -> Manifest:
        root = self.layout.root
        root.mkdir(parents=True, exist_ok=True)
        manifest = Manifest.load_or_new(self.layout.manifest, self.layout.run_id)
        git = self.git if self.git is not None else git_sha(self.repo_root)
        rr = self.repo_root
        if rr is not None:
            if not manifest.lock_sha256 and (rr / "uv.lock").is_file():
                manifest.lock_sha256 = sha256_file(rr / "uv.lock")
            sha_file = rr / "docs" / "s7" / "FROZEN_SHA256.txt"
            if not manifest.design_sha256 and sha_file.is_file():
                txt = sha_file.read_text().split()
                manifest.design_sha256 = txt[0] if txt else ""
        env = {"python": platform.python_version()}
        for pkg in ENV_PACKAGES:
            try:
                env[pkg] = metadata.version(pkg)
            except metadata.PackageNotFoundError:
                pass
        manifest.environment.update(env)
        cfg_path = self.layout.run_config
        text = json.dumps(self.cfg.to_dict(), indent=1, sort_keys=True, default=list) + "\n"
        if not cfg_path.is_file():
            _atomic_write(cfg_path, text)
        manifest.add(root, cfg_path, "ops.runner:write_run_config", config_hash(self.cfg.to_dict()), git)
        manifest.save(self.layout.manifest)
        return manifest

    # ---- running
    def run(self) -> RunSummary:
        if self.dry_run:
            return self._dry()
        if not self.plan.launchable:
            raise SystemExit(f"plan {self.plan.name!r} is a stub and is not launchable in this wave")
        manifest = self._prepare()
        git = self.git if self.git is not None else git_sha(self.repo_root)
        logs = self.layout.logs
        summary = RunSummary()
        failed_models: set[str] = set()
        fatal = False
        any_failed = False
        fns: dict[str, StageFn] = {}
        last_model: str | None = None
        total = len(self.jobs)
        progress.write_queue(logs, pending=total, running=False)

        for i, job in enumerate(self.jobs):
            pending = total - i
            if fatal:
                summary.results.append(JobResult(job.id, "not_run"))
                continue
            if job.model_key and job.model_key in failed_models:
                summary.results.append(JobResult(job.id, "skipped_model_failed"))
                self._log_end(job, "skipped_model_failed", 0, 0.0, utc_now())
                continue
            if job.model_key is None and job.stage != "data" and any_failed:
                summary.results.append(JobResult(job.id, "skipped_dependency"))
                self._log_end(job, "skipped_dependency", 0, 0.0, utc_now())
                continue
            ok, why = self.marker_valid(job, manifest)
            if ok:
                n = len(json.loads(self.layout.done_marker(job.id).read_text())["outputs"])
                self.out(f"[skip] {job.id}: done marker present, {why}")
                summary.results.append(JobResult(job.id, "skipped_done", n))
                self._log_end(job, "skipped_done", n, 0.0, utc_now())
                continue
            if last_model is not None and job.model_key != last_model:
                self._release_model()
            last_model = job.model_key
            progress.write_queue(logs, pending=pending, running=True)
            start_iso, t0 = utc_now(), self.clock()
            progress.heartbeat(logs, {"job": job.id, "start": start_iso, "end": None, "status": "running", "outputs": 0})
            self.out(f"[run ] {job.id}")
            res = self._execute(job, manifest, fns, git)
            res.seconds = self.clock() - t0
            manifest.save(self.layout.manifest)
            if res.status == "done":
                self._write_marker(job, res.outputs_list, res.seconds)
            self._log_end(job, res.status, res.outputs, res.seconds, start_iso, res.note)
            summary.results.append(JobResult(res.job_id, res.status, res.outputs, res.seconds, res.note))
            if res.status == "failed":
                any_failed = True
                self.out(f"[FAIL] {job.id}: {res.note}")
                if job.model_key is None or not self.keep_going:
                    fatal = True
                else:
                    failed_models.add(job.model_key)
        progress.write_queue(logs, pending=0 if not fatal else sum(1 for r in summary.results if r.status == "not_run"),
                             running=False, finished=True)
        return summary

    def _execute(self, job: Job, manifest: Manifest, fns: dict[str, StageFn], git: str) -> JobResult:
        res = JobResult(job.id, "failed")
        try:
            if job.stage not in fns:
                fns[job.stage] = self.resolver(job.stage)
            jcfg = job_config(self.cfg, job)
            report = fns[job.stage](jcfg, self.layout, manifest, dry_run=False)
            if not report.ok:
                res.note = scrub("stage reported ok=False: " + "; ".join(report.notes)[:300])
                if report.metrics.get("k1_triggered") or any("K1" in n for n in report.notes):
                    res.note = ("K1: reference-solution failures exclude more than 5 percent of a suite; the run is "
                                "stopped for this model. Fix the harness or suite version, or the operator accepts the "
                                "excluded list by writing config/k1_accepted.json (the excluded problem IDs) in the "
                                "run directory, then re-run. " + res.note)
                return res
            outs = sorted(set(report.outputs))
            ch = config_hash(jcfg.to_dict())
            for rel in outs:
                p = self.layout.root / rel
                if not p.is_file():
                    res.note = f"declared output missing: {rel}"
                    return res
                if rel not in manifest.entries:
                    manifest.add(self.layout.root, p, f"{STAGES.get(job.stage, job.stage)}", ch, git)
            res.status, res.outputs, res.outputs_list = "done", len(outs), outs
            if report.skipped:
                res.note = f"{len(report.skipped)} resumable shard(s) already complete"
        except BaseException as exc:  # a failed job must not take down the heartbeat or the manifest
            if isinstance(exc, (KeyboardInterrupt, SystemExit)):
                manifest.save(self.layout.manifest)
                self._log_end(job, "failed", 0, 0.0, utc_now(), type(exc).__name__)
                raise
            res.note = scrub(f"{type(exc).__name__}: {exc}")[:300]
            self.out(scrub(traceback.format_exc(limit=3)))
        return res

    def _release_model(self) -> None:
        """Free memory between models. Does nothing heavy: torch is touched only if already imported."""
        gc.collect()
        torch = sys.modules.get("torch")
        if torch is not None and getattr(torch, "cuda", None) is not None:
            try:
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
            except Exception:  # noqa: BLE001
                pass

    def _log_end(self, job: Job, status: str, outputs: int, seconds: float, start_iso: str, note: str = "") -> None:
        row = {"job": job.id, "start": start_iso, "end": utc_now(), "status": status, "outputs": outputs,
               "seconds": round(seconds, 3)}
        if note:
            row["note"] = note
        progress.heartbeat(self.layout.logs, row)

    def _dry(self) -> RunSummary:
        self.out(f"plan {self.plan.name}: run_id={self.cfg.run_id} jobs={len(self.jobs)} (dry run; no stage module is imported)")
        manifest = Manifest.load_or_new(self.layout.manifest, self.layout.run_id)
        summary = RunSummary()
        for job in self.jobs:
            ok, why = self.marker_valid(job, manifest)
            target = STAGES[job.stage]
            self.out(f"  {'skip (done)' if ok else 'run        '} {job.describe()} -> {target}")
            summary.results.append(JobResult(job.id, "skipped_done" if ok else "not_run"))
        if not self.plan.launchable:
            self.out("  note: this plan is a stub and would be refused at execution")
        return summary
