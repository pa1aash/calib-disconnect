"""Credential access: environment variables first, then an untracked .env file at the repo root.

The .env file is parsed without printing values. Values are never written anywhere by this module.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Mapping

REPO_ROOT = Path(__file__).resolve().parents[1]

RUNPOD_API_KEY = "RUNPOD_API_KEY"
HF_TOKEN = "HF_TOKEN"


def parse_env_file(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    path = Path(path)
    if not path.is_file():
        return out
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export "):]
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
            v = v[1:-1]
        if k:
            out[k] = v
    return out


def get_env(name: str, environ: Mapping[str, str] | None = None, env_file: Path | None = None) -> str | None:
    environ = os.environ if environ is None else environ
    if environ.get(name):
        return environ[name]
    f = env_file if env_file is not None else REPO_ROOT / ".env"
    v = parse_env_file(f).get(name)
    return v or None


def require_env(name: str, environ: Mapping[str, str] | None = None, env_file: Path | None = None) -> str:
    v = get_env(name, environ, env_file)
    if not v:
        raise SystemExit(f"{name} is not set. Export it or put it in the untracked .env file at the repo root.")
    return v
