"""Run manifest format: every file a run produces is listed with its SHA-256.

MANIFEST.json (tracked) has this shape:

    {
      "format": "calib-disconnect/manifest/v1",
      "run_id": "...",
      "design_sha256": "<SHA-256 of the frozen design>",
      "lock_sha256": "<SHA-256 of uv.lock>",
      "environment": {"python": "...", "torch": "...", ...},
      "entries": {
        "<path relative to the run root>": {
          "sha256": "...", "bytes": 123, "producer": "pipeline.generate.runner:generate_shard",
          "config_hash": "...", "git_sha": "...", "created_utc": "2026-11-10T22:00:00Z"
        }, ...
      }
    }

Entries are keyed by path so that a resumed job replaces its own entry. verify() recomputes every
hash present on disk and reports missing files separately, because large shards are git-ignored and
may live only on the pod or in a restored archive.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .hashing import sha256_file

FORMAT = "calib-disconnect/manifest/v1"


def git_sha(repo: Path | None = None) -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True)
        sha = out.stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=repo,
                               capture_output=True, text=True, check=True).stdout.strip()
        return sha + ("-dirty" if dirty else "")
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def utc_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class ManifestEntry:
    sha256: str
    bytes: int
    producer: str
    config_hash: str
    git_sha: str
    created_utc: str

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass
class Manifest:
    run_id: str
    design_sha256: str = ""
    lock_sha256: str = ""
    environment: dict[str, str] = field(default_factory=dict)
    entries: dict[str, ManifestEntry] = field(default_factory=dict)

    # -- io
    def to_dict(self) -> dict[str, Any]:
        return {"format": FORMAT, "run_id": self.run_id, "design_sha256": self.design_sha256,
                "lock_sha256": self.lock_sha256, "environment": dict(sorted(self.environment.items())),
                "entries": {k: self.entries[k].to_dict() for k in sorted(self.entries)}}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Manifest":
        if d.get("format") != FORMAT:
            raise ValueError(f"unknown manifest format {d.get('format')!r}")
        return cls(run_id=d["run_id"], design_sha256=d.get("design_sha256", ""),
                   lock_sha256=d.get("lock_sha256", ""), environment=dict(d.get("environment", {})),
                   entries={k: ManifestEntry(**v) for k, v in d.get("entries", {}).items()})

    @classmethod
    def load(cls, path: Path) -> "Manifest":
        return cls.from_dict(json.loads(Path(path).read_text()))

    @classmethod
    def load_or_new(cls, path: Path, run_id: str) -> "Manifest":
        return cls.load(path) if Path(path).exists() else cls(run_id=run_id)

    def save(self, path: Path) -> None:
        """Atomic write (temp file plus rename) so an interrupted job never leaves a torn manifest."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".manifest.", suffix=".tmp")
        with os.fdopen(fd, "w") as f:
            json.dump(self.to_dict(), f, indent=1, sort_keys=False)
            f.write("\n")
        os.replace(tmp, path)

    # -- entries
    def add(self, run_root: Path, file: Path, producer: str, config_hash: str, git: str | None = None) -> ManifestEntry:
        file = Path(file)
        rel = os.path.relpath(file, run_root)
        if rel.startswith(".."):
            raise ValueError(f"{file} is outside the run root {run_root}")
        e = ManifestEntry(sha256=sha256_file(file), bytes=file.stat().st_size, producer=producer,
                          config_hash=config_hash, git_sha=git if git is not None else git_sha(),
                          created_utc=utc_now())
        self.entries[rel] = e
        return e

    def verify(self, run_root: Path, require_present: bool = False) -> "VerifyReport":
        rep = VerifyReport()
        for rel, e in sorted(self.entries.items()):
            p = Path(run_root) / rel
            if not p.exists():
                rep.missing.append(rel)
                continue
            if sha256_file(p) != e.sha256:
                rep.mismatched.append(rel)
            else:
                rep.ok.append(rel)
        if require_present and rep.missing:
            rep.mismatched.extend(f"missing:{m}" for m in rep.missing)
        return rep

    def unlisted(self, run_root: Path, ignore: tuple[str, ...] = ("MANIFEST.json", "logs/", "state/")) -> list[str]:
        """Files under the run root that no entry lists (manifest completeness check)."""
        out = []
        for p in sorted(Path(run_root).rglob("*")):
            if p.is_file():
                rel = os.path.relpath(p, run_root)
                if any(rel == i or rel.startswith(i) for i in ignore) or Path(rel).name.startswith("."):
                    continue
                if rel not in self.entries:
                    out.append(rel)
        return out


@dataclass
class VerifyReport:
    ok: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    mismatched: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.mismatched
