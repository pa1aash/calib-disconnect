"""Command line: uv run python -m ops <command> ...

Every command that would call an API or create cost is a dry run unless --execute is given; a dry run
prints each action and calls nothing.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

from pipeline.contracts.layout import COST_LEDGER, RunLayout
from pipeline.contracts.manifest import git_sha

from . import cost, env as _env, guard as _guard, sync as _sync
from .plans import available_plans, load_plan, order_jobs
from .redact import redact
from .runner import Runner
from .runpod_api import DEFAULT_GPU_TYPE_ID, PodSpec, RunPodClient

REPO = _env.REPO_ROOT


def local_state_path() -> Path:
    base = Path(os.environ.get("OPS_LOCAL_STATE") or REPO / "scratch" / "ops")
    return base / "pod.json"


def save_pod_state(path: Path, pod_id: str, run_id: str, launched_utc: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"pod_id": pod_id, "run_id": run_id, "launched_utc": launched_utc}))


def load_pod_state(path: Path) -> dict[str, str]:
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return {}


def resolve_pod_id(arg: str | None, state: dict[str, str]) -> str | None:
    return arg or os.environ.get("RUNPOD_POD_ID") or state.get("pod_id")


def make_client(execute: bool, out: Callable[[str], None], factory: Callable[..., Any] | None = None) -> Any:
    key = _env.get_env(_env.RUNPOD_API_KEY)
    if execute and not key:
        raise SystemExit("RUNPOD_API_KEY is not set. Export it or put it in the untracked .env file.")
    return (factory or RunPodClient)(key, dry_run=not execute, out=out)


# ---- commands --------------------------------------------------------------------------------------
def cmd_plan(a: argparse.Namespace, out: Callable[[str], None]) -> int:
    plan = load_plan(a.plan, a.run_id)
    jobs = order_jobs(plan.jobs)
    if a.json:
        out(json.dumps({"plan": plan.name, "run_id": plan.cfg.run_id, "launchable": plan.launchable,
                        "config": plan.cfg.to_dict(), "jobs": [j.id for j in jobs],
                        "download_models": list(plan.download_models())}, indent=1, default=list))
        return 0
    out(f"plan {plan.name} (run_id {plan.cfg.run_id}): {plan.description}")
    out(f"launchable: {plan.launchable}; jobs: {len(jobs)}; models to download: {', '.join(plan.download_models()) or 'none'}")
    for j in jobs:
        out(f"  {j.describe()}")
    return 0


def cmd_launch(a: argparse.Namespace, out: Callable[[str], None], client_factory=None) -> int:
    plan = load_plan(a.plan, a.run_id)
    if not plan.launchable or not plan.pod:
        raise SystemExit(f"plan {plan.name!r} is not launchable on a pod")
    price = cost.validate_price(a.hourly_price_usd, a.price_source)       # refuse before anything else
    env_names = tuple(n for n in a.env_names if n)
    spec = PodSpec(name=f"calib-{plan.cfg.run_id}", gpu_type_id=a.gpu_type_id,
                   image=a.image or os.environ.get("RUNPOD_IMAGE"), template_id=a.template_id,
                   container_disk_gb=a.container_disk_gb, volume_gb=a.volume_gb, env_names=env_names)
    execute = a.execute
    out(f"launch {'(EXECUTE)' if execute else '(dry run; add --execute to create the pod)'}: plan={plan.name} "
        f"run_id={plan.cfg.run_id} gpu_type={spec.gpu_type_id} price=${price}/h source={a.price_source!r}")
    client = make_client(execute, out, client_factory)
    pod = client.create_pod(spec)
    launch_t = _dt.datetime.now(_dt.timezone.utc)
    launched = cost.fmt_utc(launch_t)
    run_id = plan.cfg.run_id
    if execute:
        pod_id = str(pod["id"])
        cost.append_launch(Path(a.ledger), launch=launch_t, pod_id=pod_id, gpu_type=spec.gpu_type_id,
                           hourly_price_usd=price, price_source=a.price_source, run_id=run_id, git_sha=git_sha(REPO))
        save_pod_state(local_state_path(), pod_id, run_id, launched)
        out(f"pod created: {redact(pod_id)}; ledger row appended to {a.ledger}; pod ID saved to the untracked local state file")
    else:
        out(f"[dry-run] would append a ledger row to {a.ledger} (price ${price}/h) and save the pod ID locally")
    out("On the pod (after copying or cloning the repo to /workspace/calib-disconnect):")
    out(f"  cd /workspace/calib-disconnect && bash ops/bootstrap.sh --plan {plan.name}")
    out(f"  uv run python -m ops run --plan {plan.name} --run-id {run_id} --execute --keep-going")
    out(f"  uv run python -m ops guard --run-id {run_id} --launched-at {launched} --execute   (pod-side or local)")
    return 0


def cmd_bootstrap(a: argparse.Namespace, out: Callable[[str], None], runner=subprocess.run) -> int:
    cmd = ["bash", str(REPO / "ops" / "bootstrap.sh"), "--plan", a.plan]
    if not a.execute:
        cmd.append("--dry-run")
    out("$ " + " ".join(cmd))
    return runner(cmd).returncode


def cmd_run(a: argparse.Namespace, out: Callable[[str], None], resolver=None) -> int:
    plan = load_plan(a.plan, a.run_id)
    layout = RunLayout.for_run(plan.cfg.run_id, Path(a.runs_root) if a.runs_root else None)
    r = Runner(plan, layout, resolver=resolver, keep_going=a.keep_going, dry_run=not a.execute, repo_root=REPO, out=out)
    summary = r.run()
    if a.execute:
        out(f"done: {summary.count('done')}, skipped: {summary.count('skipped_done')}, failed: {summary.count('failed')}, "
            f"skipped after failure: {summary.count('skipped_model_failed') + summary.count('skipped_dependency')}, "
            f"not run: {summary.count('not_run')}")
        return summary.exit_code
    return 0


def _complete_ledger(ledger: Path, pod_id: str, run_id: str | None, reason: str, stop_ts: float, out) -> None:
    try:
        row = cost.complete(ledger, pod_id=pod_id, stop=_dt.datetime.fromtimestamp(stop_ts, _dt.timezone.utc),
                            reason=reason, run_id=run_id)
        out(f"ledger completed: gpu_hours={row['gpu_hours']} cost_usd={row['cost_usd']}")
    except cost.LedgerError as exc:
        out(f"[warn] ledger not completed here: {exc}. Run `ledger complete` on the machine that holds the launch row.")


def cmd_guard(a: argparse.Namespace, out: Callable[[str], None], client_factory=None, sleep=None) -> int:
    state = load_pod_state(local_state_path())
    pod_id = resolve_pod_id(a.pod_id, state)
    if not pod_id:
        raise SystemExit("no pod ID: pass --pod-id, set RUNPOD_POD_ID, or launch from this machine")
    run_id = a.run_id or state.get("run_id")
    if not run_id:
        raise SystemExit("--run-id is required")
    launched = a.launched_at or state.get("launched_utc") or os.environ.get("POD_LAUNCHED_UTC")
    if not launched:
        t = cost.launched_at(Path(a.ledger), pod_id, run_id)
        launched = cost.fmt_utc(t) if t else None
    if not launched:
        raise SystemExit("launch time unknown: pass --launched-at (UTC, %Y-%m-%dT%H:%M:%SZ)")
    cfg = _guard.GuardConfig(stall_s=a.stall_minutes * 60, gpu_hour_cap=a.gpu_hour_cap, poll_s=a.poll_seconds,
                             empty_grace_s=a.empty_grace_seconds, terminate=a.terminate)
    if a.remote:
        p = _sync.SshParams.from_env()
        reader: Any = _guard.SshReader(p.host, p.port, p.key, f"{p.remote_root}/runs/{run_id}", p.user)
    else:
        reader = _guard.LocalReader(Path(a.runs_root) / run_id if a.runs_root else RunLayout.for_run(run_id).root)
    client = make_client(a.execute, out, client_factory)
    g = _guard.Guard(cfg, client, pod_id, cost.parse_utc(launched).timestamp(), reader,
                     on_stop=(lambda reason, ts: _complete_ledger(Path(a.ledger), pod_id, run_id, reason, ts, out)) if a.execute else None,
                     out=out, **({"sleep": sleep} if sleep else {}))
    out(f"guard {'(EXECUTE)' if a.execute else '(dry run: one check, no loop)'}: pod={redact(pod_id)} run={run_id} "
        f"stall={a.stall_minutes} min, cap={a.gpu_hour_cap} GPU-h, empty grace={a.empty_grace_seconds}s")
    if not a.execute:
        reason = g.check()
        out(f"[dry-run] condition now: {reason or 'none (the pod would keep running)'}; gpu_hours={g.gpu_hours():.3f}")
        if reason:
            g.stop(reason)           # the client is in dry-run mode: prints the request, sends nothing
        return 0
    reason = g.run()
    return 0 if reason else 1


def cmd_stop(a: argparse.Namespace, out: Callable[[str], None], client_factory=None) -> int:
    state = load_pod_state(local_state_path())
    pod_id = resolve_pod_id(a.pod_id, state)
    if not pod_id:
        raise SystemExit("no pod ID: pass --pod-id, set RUNPOD_POD_ID, or launch from this machine")
    client = make_client(a.execute, out, client_factory)
    out(f"stop {'(EXECUTE)' if a.execute else '(dry run)'}: pod={redact(pod_id)} {'terminate' if a.terminate else 'stop'}")
    (client.terminate_pod if a.terminate else client.stop_pod)(pod_id)
    if a.execute:
        _complete_ledger(Path(a.ledger), pod_id, a.run_id or state.get("run_id"), a.reason, _dt.datetime.now().timestamp(), out)
    else:
        out("[dry-run] would complete the ledger row with GPU-hours and cost")
    return 0


def cmd_ledger(a: argparse.Namespace, out: Callable[[str], None]) -> int:
    path = Path(a.ledger)
    if a.action == "complete":
        pod = a.pod_id or load_pod_state(local_state_path()).get("pod_id")
        if not pod:
            raise SystemExit("--pod-id is required")
        stop = cost.parse_utc(a.stop_utc) if a.stop_utc else _dt.datetime.now(_dt.timezone.utc)
        row = cost.complete(path, pod_id=pod, stop=stop, reason=a.reason, run_id=a.run_id)
        out(f"completed: gpu_hours={row['gpu_hours']} cost_usd={row['cost_usd']}")
        return 0
    rows = cost.read_rows(path)
    if a.action == "show":
        for r in rows:
            out(",".join(r[c] for c in r))
    s = cost.summarize(path)
    out(f"rows={int(s['rows'])} open={int(s['open_rows'])} gpu_hours={s['gpu_hours']:.4f} cost_usd={s['cost_usd']:.4f}")
    return 0


# ---- parser ----------------------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m ops", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    plans = available_plans()

    def add_plan(sp, default="pilot"):
        sp.add_argument("--plan", default=default, choices=plans)
        sp.add_argument("--run-id")

    sp = sub.add_parser("plan", help="print the jobs of a plan")
    add_plan(sp); sp.add_argument("--json", action="store_true")

    sp = sub.add_parser("launch", help="create the pod and record a ledger row (dry run unless --execute)")
    add_plan(sp)
    sp.add_argument("--hourly-price-usd", required=True, type=float)
    sp.add_argument("--price-source", required=True)
    sp.add_argument("--gpu-type-id", default=os.environ.get("RUNPOD_GPU_TYPE_ID", DEFAULT_GPU_TYPE_ID))
    sp.add_argument("--image"); sp.add_argument("--template-id")
    sp.add_argument("--container-disk-gb", type=int, default=100)
    sp.add_argument("--volume-gb", type=int, default=400)
    sp.add_argument("--env-names", nargs="*", default=["HF_TOKEN"])
    sp.add_argument("--ledger", default=str(COST_LEDGER))
    sp.add_argument("--execute", action="store_true")

    sp = sub.add_parser("bootstrap", help="run ops/bootstrap.sh on the pod (dry run unless --execute)")
    sp.add_argument("--plan", default="pilot", choices=plans); sp.add_argument("--execute", action="store_true")

    sp = sub.add_parser("run", help="run a plan locally or on the pod (dry run unless --execute)")
    add_plan(sp)
    sp.add_argument("--keep-going", action="store_true"); sp.add_argument("--execute", action="store_true")
    sp.add_argument("--runs-root")

    sp = sub.add_parser("guard", help="stop the pod on empty queue, stalled progress, or the GPU-hour cap")
    sp.add_argument("--run-id"); sp.add_argument("--pod-id"); sp.add_argument("--launched-at")
    sp.add_argument("--stall-minutes", type=float, default=_guard.DEFAULT_STALL_S / 60)
    sp.add_argument("--gpu-hour-cap", type=float, default=_guard.DEFAULT_GPU_HOUR_CAP)
    sp.add_argument("--poll-seconds", type=float, default=60.0)
    sp.add_argument("--empty-grace-seconds", type=float, default=900.0)
    sp.add_argument("--remote", action="store_true", help="read queue and progress over SSH (POD_SSH_*)")
    sp.add_argument("--terminate", action="store_true")
    sp.add_argument("--ledger", default=str(COST_LEDGER)); sp.add_argument("--runs-root")
    sp.add_argument("--execute", action="store_true")

    sp = sub.add_parser("sync", help="pull a run from the pod and verify it (dry run unless --execute)")
    sp.add_argument("--run-id", required=True); sp.add_argument("--tarball")
    sp.add_argument("--skip-large", action="store_true"); sp.add_argument("--verify-only", action="store_true")
    sp.add_argument("--execute", action="store_true")

    sp = sub.add_parser("stop", help="stop (or terminate) the pod and complete the ledger row")
    sp.add_argument("--pod-id"); sp.add_argument("--run-id"); sp.add_argument("--reason", default="operator_stop")
    sp.add_argument("--terminate", action="store_true"); sp.add_argument("--ledger", default=str(COST_LEDGER))
    sp.add_argument("--execute", action="store_true")

    sp = sub.add_parser("ledger", help="show, summarize, or complete the cost ledger (local file)")
    sp.add_argument("action", nargs="?", default="show", choices=["show", "summary", "complete"])
    sp.add_argument("--ledger", default=str(COST_LEDGER)); sp.add_argument("--pod-id"); sp.add_argument("--run-id")
    sp.add_argument("--reason", default="operator_stop"); sp.add_argument("--stop-utc")
    return p


def main(argv: list[str] | None = None, out: Callable[[str], None] = print) -> int:
    a = build_parser().parse_args(argv)
    if a.cmd == "sync":
        sargv = ["--run-id", a.run_id] + (["--tarball", a.tarball] if a.tarball else []) + \
            (["--skip-large"] if a.skip_large else []) + (["--verify-only"] if a.verify_only else []) + \
            (["--execute"] if a.execute else [])
        return _sync.main(sargv, out=out)
    return {"plan": cmd_plan, "launch": cmd_launch, "bootstrap": cmd_bootstrap, "run": cmd_run, "guard": cmd_guard,
            "stop": cmd_stop, "ledger": cmd_ledger}[a.cmd](a, out)


if __name__ == "__main__":
    sys.exit(main())
