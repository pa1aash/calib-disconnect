"""Sync outputs from the pod to the operator's runs/<run_id>/ and verify them against the manifest.

Transport: rsync over SSH (POD_SSH_HOST, POD_SSH_PORT, POD_SSH_KEY from the environment; POD_SSH_USER
defaults to root, POD_REMOTE_ROOT to /workspace/calib-disconnect) or a tarball. Host, port, and key are
never printed in full. After the pull, every manifest entry's SHA-256 is recomputed locally.

Exit codes: 0 verified; 1 a file differs from the manifest hash; 2 files missing that were not
deliberately left on the pod (--skip-large leaves hidden-state shards, adapters, and sqlite caches);
3 the pull itself failed.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tarfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping

from pipeline.contracts.layout import RUNS_ROOT
from pipeline.contracts.manifest import Manifest

from .redact import redact

LARGE_EXCLUDES = ("capture/**/*.safetensors", "adapters/", "*.sqlite")


def is_large(rel: str) -> bool:
    return (rel.startswith("capture/") and rel.endswith(".safetensors")) or rel.startswith("adapters/") \
        or rel.endswith(".sqlite")


@dataclass
class SshParams:
    host: str
    port: str
    key: str
    user: str = "root"
    remote_root: str = "/workspace/calib-disconnect"

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None, strict: bool = True) -> "SshParams":
        e = os.environ if environ is None else environ
        missing = [n for n in ("POD_SSH_HOST", "POD_SSH_PORT", "POD_SSH_KEY") if not e.get(n)]
        if missing and not strict:
            e = {**e, **{n: f"<{n}>" for n in missing}}
            missing = []
        if missing:
            raise SystemExit(f"set {', '.join(missing)} (pod connection details come from the RunPod console)")
        return cls(e["POD_SSH_HOST"], e["POD_SSH_PORT"], e["POD_SSH_KEY"], e.get("POD_SSH_USER", "root"),
                   e.get("POD_REMOTE_ROOT", "/workspace/calib-disconnect"))


def build_rsync_cmd(p: SshParams, run_id: str, dest: Path, skip_large: bool, shown: bool = False) -> list[str]:
    host, port, key = (redact(p.host), redact(p.port), redact(p.key)) if shown else (p.host, p.port, p.key)
    cmd = ["rsync", "-az", "--partial", "-e", f"ssh -p {port} -i {key} -o StrictHostKeyChecking=accept-new"]
    if skip_large:
        cmd += [f"--exclude={x}" for x in LARGE_EXCLUDES]
    cmd += [f"{p.user}@{host}:{p.remote_root}/runs/{run_id}/", f"{dest}/"]
    return cmd


def extract_tarball(tar_path: Path, dest: Path) -> int:
    """Extract with the 'data' filter (no absolute paths, no links out of dest, no device files)."""
    dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(tar_path) as tf:
        members = tf.getmembers()
        tf.extractall(dest, filter="data")
    return len(members)


@dataclass
class SyncReport:
    ok: list[str] = field(default_factory=list)
    mismatched: list[str] = field(default_factory=list)
    missing_expected: list[str] = field(default_factory=list)     # left on the pod on purpose
    missing_unexpected: list[str] = field(default_factory=list)

    @property
    def exit_code(self) -> int:
        return 1 if self.mismatched else (2 if self.missing_unexpected else 0)


def verify_run(run_root: Path, skip_large: bool = False) -> SyncReport:
    mpath = Path(run_root) / "MANIFEST.json"
    if not mpath.is_file():
        raise SystemExit("MANIFEST.json not found in the run root; nothing to verify against")
    rep = Manifest.load(mpath).verify(Path(run_root))
    out = SyncReport(ok=rep.ok, mismatched=rep.mismatched)
    for m in rep.missing:
        (out.missing_expected if (skip_large and is_large(m)) else out.missing_unexpected).append(m)
    return out


def main(argv: list[str] | None = None, environ: Mapping[str, str] | None = None,
         runner: Callable[..., Any] = subprocess.run, out: Callable[[str], None] = print,
         runs_root: Path | None = None) -> int:
    p = argparse.ArgumentParser(prog="ops sync")
    p.add_argument("--run-id", required=True)
    p.add_argument("--tarball", help="extract this tarball instead of using rsync")
    p.add_argument("--skip-large", action="store_true")
    p.add_argument("--execute", action="store_true", help="pull and extract; without it, print the command only")
    p.add_argument("--verify-only", action="store_true", help="do not pull; verify what is on disk")
    a = p.parse_args(argv)
    dest = (runs_root or RUNS_ROOT) / a.run_id
    if a.verify_only:
        pass
    elif a.tarball:
        out(f"{'' if a.execute else '[dry-run] '}extract {a.tarball} into {dest}")
        if a.execute:
            n = extract_tarball(Path(a.tarball), dest)
            out(f"extracted {n} members")
    else:
        params = SshParams.from_env(environ, strict=a.execute)
        out(f"{'' if a.execute else '[dry-run] '}" + " ".join(build_rsync_cmd(params, a.run_id, dest, a.skip_large, shown=True)))
        if a.execute:
            dest.mkdir(parents=True, exist_ok=True)
            if runner(build_rsync_cmd(params, a.run_id, dest, a.skip_large)).returncode != 0:
                out("[FAIL] rsync failed")
                return 3
    if not a.execute and not a.verify_only:
        out("[dry-run] would then verify every manifest entry's SHA-256 locally")
        return 0
    rep = verify_run(dest, a.skip_large)
    out(f"verified ok: {len(rep.ok)}; mismatched: {len(rep.mismatched)}; "
        f"missing (left on the pod on purpose): {len(rep.missing_expected)}; missing (unexpected): {len(rep.missing_unexpected)}")
    for m in rep.mismatched:
        out(f"[MISMATCH] {m}")
    for m in rep.missing_unexpected:
        out(f"[MISSING]  {m}")
    return rep.exit_code


if __name__ == "__main__":
    sys.exit(main())
