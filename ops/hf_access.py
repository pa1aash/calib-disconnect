"""Hugging Face access check and sequential model download at pinned revisions.

The check calls the model API for the pinned revision through an injectable session (an object with
get(url, headers=..., timeout=..., allow_redirects=...) returning status_code and json()). It fails
fast with a message naming the model and the action needed. The token is read from HF_TOKEN (or the
untracked .env) and is sent only as a request header; it is never printed or written.

Status handling:
  revision endpoint 200, repo not gated            -> open
  revision endpoint 200, repo gated                -> probe config.json: 200/redirect = access granted,
                                                      401/403 = gated without access
  revision endpoint 401 or 403                     -> not accessible (gated without access, or private,
                                                      or the ID is wrong; the Hub answers 401 for missing
                                                      repositories when unauthenticated)
  revision endpoint 404                            -> repository query without revision decides between
                                                      "repository missing" and "revision absent"
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable

from . import env as _env
from . import progress
from .plans import load_plan, model_repo
from .redact import redact

HF_BASE = "https://huggingface.co"
TIMEOUT_S = 30
OK_FILE_STATUS = (200, 301, 302, 307, 308)
UNKNOWN_SIZE_MIN_FREE_BYTES = 100 * 1024**3
SIZE_MARGIN = 1.10


@dataclass
class AccessResult:
    model_key: str
    repo: str
    revision: str
    ok: bool
    message: str


def _headers(token: str | None) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"} if token else {}


def check_model(key: str, session: Any, token: str | None, base: str = HF_BASE) -> AccessResult:
    repo, rev = model_repo(key)

    def res(ok: bool, msg: str) -> AccessResult:
        return AccessResult(key, repo, rev, ok, f"{key} ({repo} @ {rev[:8]}): {msg}")

    h = _headers(token)
    gate_hint = ("accept the licence on its Hub page (https://huggingface.co/" + repo + ") while logged in, "
                 "and set HF_TOKEN to a token of that account" if token else
                 "set HF_TOKEN to a Hugging Face access token and, if the repository is gated, accept the "
                 "licence on its Hub page (https://huggingface.co/" + repo + ") while logged in")
    r = session.get(f"{base}/api/models/{repo}/revision/{rev}", headers=h, timeout=TIMEOUT_S, allow_redirects=True)
    st = r.status_code
    if st in (401, 403):
        return res(False, f"not accessible (HTTP {st}). Action: {gate_hint}.")
    if st == 404:
        r2 = session.get(f"{base}/api/models/{repo}", headers=h, timeout=TIMEOUT_S, allow_redirects=True)
        if r2.status_code == 200:
            return res(False, "the repository exists but the pinned revision is absent (HTTP 404). Action: "
                              "check the revision in pipeline/contracts/constants.py; do not change it without a deviation entry.")
        if r2.status_code in (401, 403):
            return res(False, f"not accessible (HTTP {r2.status_code}). Action: {gate_hint}.")
        return res(False, "repository not found (HTTP 404). Action: check the repository ID in "
                          "pipeline/contracts/constants.py.")
    if st != 200:
        return res(False, f"unexpected HTTP {st} from the model API. Action: retry; if it persists, check the Hub status.")
    info = r.json()
    sha = info.get("sha")
    if sha and sha != rev:
        return res(False, "the Hub resolved the pinned revision to a different commit. Action: do not proceed.")
    if not info.get("gated"):
        return res(True, "open")
    f = session.get(f"{base}/{repo}/resolve/{rev}/config.json", headers=h, timeout=TIMEOUT_S, allow_redirects=False)
    if f.status_code in OK_FILE_STATUS:
        return res(True, "gated, access granted")
    if f.status_code in (401, 403):
        return res(False, f"gated and access is not granted (HTTP {f.status_code}). Action: {gate_hint}.")
    if f.status_code == 404:
        return res(True, "gated, access not contradicted (config.json absent at this revision)")
    return res(False, f"gated; unexpected HTTP {f.status_code} on the file probe. Action: retry.")


def check_models(keys: Iterable[str], session: Any, token: str | None, base: str = HF_BASE) -> list[AccessResult]:
    """Check every distinct (repo, revision) once, in order; stops at the first failure (fail fast)."""
    seen: set[tuple[str, str]] = set()
    out: list[AccessResult] = []
    for k in keys:
        rr = model_repo(k)
        if rr in seen:
            continue
        seen.add(rr)
        r = check_model(k, session, token, base)
        out.append(r)
        if not r.ok:
            break
    return out


# ---- download -------------------------------------------------------------------------------------
def repo_size_bytes(repo: str, rev: str, session: Any, token: str | None, base: str = HF_BASE) -> int | None:
    r = session.get(f"{base}/api/models/{repo}/revision/{rev}?blobs=true", headers=_headers(token),
                    timeout=TIMEOUT_S, allow_redirects=True)
    if r.status_code != 200:
        return None
    sizes = [s.get("size") for s in r.json().get("siblings", [])]
    return sum(s for s in sizes if isinstance(s, int)) or None


def free_bytes(path: Path) -> int:
    p = Path(path)
    while not p.exists() and p != p.parent:
        p = p.parent
    return shutil.disk_usage(p).free


def marker_path(state_dir: Path, repo: str, rev: str) -> Path:
    return Path(state_dir) / f"download-{repo.replace('/', '__')}-{rev[:8]}.done"


def default_download(repo: str, rev: str, hf_home: Path, token: str | None) -> None:
    from huggingface_hub import snapshot_download  # lazy: only on the pod, only when downloading

    snapshot_download(repo_id=repo, revision=rev, cache_dir=str(Path(hf_home) / "hub"), token=token)


def fetch_models(keys: Iterable[str], *, hf_home: Path, state_dir: Path, session: Any, token: str | None,
                 logs_dir: Path | None = None, dry_run: bool = False, out: Callable[[str], None] = print,
                 downloader: Callable[[str, str, Path, str | None], None] | None = None,
                 free_fn: Callable[[Path], int] = free_bytes, base: str = HF_BASE) -> bool:
    """Download each distinct model in sequence. Returns False (after printing why) on the first failure."""
    downloader = downloader or default_download
    done: set[tuple[str, str]] = set()
    for k in keys:
        repo, rev = model_repo(k)
        if (repo, rev) in done:
            continue
        done.add((repo, rev))
        mk = marker_path(state_dir, repo, rev)
        if dry_run:
            out(f"[dry-run] {k}: would check free disk under {hf_home}, then download {repo} @ {rev[:8]} "
                f"(skipped if {mk.name} exists)")
            continue
        if mk.exists():
            out(f"[skip] {k}: already downloaded ({mk.name})")
            continue
        size = repo_size_bytes(repo, rev, session, token, base)
        need = int(size * SIZE_MARGIN) if size else UNKNOWN_SIZE_MIN_FREE_BYTES
        free = free_fn(Path(hf_home))
        if free < need:
            out(f"[FAIL] {k}: needs about {need / 1e9:.0f} GB free under the model cache, has {free / 1e9:.0f} GB. "
                f"Action: enlarge the pod volume or free space, then re-run (completed models are skipped).")
            return False
        if logs_dir:
            progress.heartbeat(logs_dir, {"job": f"download.{k}", "start": progress.now_iso(), "end": None,
                                          "status": "running", "outputs": 0})
        out(f"[run ] {k}: downloading {repo} @ {rev[:8]} ({need / 1e9:.0f} GB with margin)")
        try:
            downloader(repo, rev, Path(hf_home), token)
        except Exception as exc:  # noqa: BLE001
            msg = str(exc).replace(token, redact(token)) if token else str(exc)
            out(f"[FAIL] {k}: download failed: {type(exc).__name__}: {msg[:200]}")
            return False
        Path(state_dir).mkdir(parents=True, exist_ok=True)
        mk.write_text(f"{repo} {rev}\n")
        if logs_dir:
            progress.heartbeat(logs_dir, {"job": f"download.{k}", "start": progress.now_iso(), "end": progress.now_iso(),
                                          "status": "done", "outputs": 1})
    return True


# ---- command line ---------------------------------------------------------------------------------
def _models_from_args(a: argparse.Namespace) -> list[str]:
    if a.models:
        return list(a.models)
    return list(load_plan(a.plan).download_models())


def main(argv: list[str] | None = None, session: Any = None, out: Callable[[str], None] = print) -> int:
    p = argparse.ArgumentParser(prog="python -m ops.hf_access")
    p.add_argument("action", choices=["check", "fetch"])
    p.add_argument("--plan", default="pilot")
    p.add_argument("--models", nargs="*")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--hf-home", default=os.environ.get("HF_HOME", "/workspace/hf-cache"))
    p.add_argument("--state-dir", default=os.environ.get("OPS_STATE_DIR", "/workspace/ops-state"))
    p.add_argument("--logs-dir")
    p.add_argument("--base-url", default=HF_BASE)
    a = p.parse_args(argv)
    keys = _models_from_args(a)
    token = _env.get_env(_env.HF_TOKEN)
    out(f"models: {', '.join(keys) if keys else '(none)'}; HF_TOKEN {'set' if token else 'not set'}")
    if a.dry_run:
        for k in dict.fromkeys(model_repo(k) for k in keys):
            out(f"[dry-run] would GET {a.base_url}/api/models/{k[0]}/revision/{k[1][:8]}...")
        if a.action == "fetch":
            fetch_models(keys, hf_home=Path(a.hf_home), state_dir=Path(a.state_dir), session=None, token=token,
                         dry_run=True, out=out)
        return 0
    if session is None:
        import requests

        session = requests.Session()
    results = check_models(keys, session, token, a.base_url)
    for r in results:
        out(("[ok]   " if r.ok else "[FAIL] ") + r.message)
    if not all(r.ok for r in results):
        return 2
    if a.action == "fetch":
        ok = fetch_models(keys, hf_home=Path(a.hf_home), state_dir=Path(a.state_dir), session=session, token=token,
                          logs_dir=Path(a.logs_dir) if a.logs_dir else None, out=out, base=a.base_url)
        return 0 if ok else 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
