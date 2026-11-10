"""Pinned benchmark files (docs/s7/BENCHMARK_PINS.md; docs/s7/parts/bench-A2/MANIFEST.json).

pins.json lists every file the pipeline reads, with URL, revision, byte count, and SHA-256 copied from
the bench-A2 manifest. Nothing here trusts a file by name: callers verify the hash before reading.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

PINS_PATH = Path(__file__).with_name("pins.json")
# Desktop browser User-Agent for the two allowed hosts (github.com, huggingface.co).
USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
              "Version/17.4 Safari/605.1.15")
ALLOWED_HOSTS = ("github.com", "huggingface.co")

LCB_SHARD_KEYS = tuple(f"lcb_v6_test{s}" for s in ("", "2", "3", "4", "5", "6"))
LCB_LOADER_KEY = "lcb_v6_loader"


class PinError(RuntimeError):
    """A pinned file is missing or does not match its pin."""


@dataclass(frozen=True)
class Pin:
    key: str
    benchmark: str
    role: str
    url: str
    download_url: str
    revision: Mapping[str, Any]
    bytes: int
    sha256: str
    relpath: str
    rows: int | None = None
    alt_relpaths: tuple[str, ...] = field(default_factory=tuple)

    @property
    def filename(self) -> str:
        return Path(self.relpath).name

    def candidates(self, cache_dir: Path) -> list[Path]:
        """Places the file may sit under a bench cache directory, in search order."""
        cache_dir = Path(cache_dir)
        return [cache_dir / self.relpath] + [cache_dir / a for a in self.alt_relpaths]


def load_pins(path: Path = PINS_PATH) -> dict[str, Pin]:
    raw = json.loads(Path(path).read_text())
    out: dict[str, Pin] = {}
    for d in raw["pins"]:
        out[d["key"]] = Pin(key=d["key"], benchmark=d["benchmark"], role=d["role"], url=d["url"],
                            download_url=d["download_url"], revision=d["revision"], bytes=d["bytes"],
                            sha256=d["sha256"], relpath=d["relpath"], rows=d.get("rows"),
                            alt_relpaths=tuple(d.get("alt_relpaths", ())))
    return out


PINS: dict[str, Pin] = load_pins()


def sha256_and_size(path: Path, chunk: int = 1 << 22) -> tuple[str, int]:
    h = hashlib.sha256()
    n = 0
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
            n += len(b)
    return h.hexdigest(), n


def verify_file(path: Path, pin: Pin) -> bool:
    """True when the file exists and both its byte count and SHA-256 equal the pin."""
    path = Path(path)
    if not path.is_file():
        return False
    if path.stat().st_size != pin.bytes:
        return False
    digest, _ = sha256_and_size(path)
    return digest == pin.sha256


def require_file(path: Path, pin: Pin) -> Path:
    """Return path after verification; raise PinError on a missing file or any mismatch."""
    path = Path(path)
    if not path.is_file():
        raise PinError(f"pinned file {pin.key} is missing: {path}")
    if not verify_file(path, pin):
        raise PinError(f"pinned file {pin.key} does not match its pin (bytes or SHA-256): {path}")
    return path


def locate(pin: Pin, cache_dir: Path) -> Path | None:
    for p in pin.candidates(cache_dir):
        if p.is_file():
            return p
    return None


def locate_verified(pin: Pin, cache_dir: Path) -> Path:
    """Find the pinned file under cache_dir and verify it. Refuses on a mismatch."""
    p = locate(pin, cache_dir)
    if p is None:
        tried = ", ".join(str(c) for c in pin.candidates(cache_dir))
        raise PinError(f"pinned file {pin.key} not found (tried {tried})")
    return require_file(p, pin)


def _check_host(url: str) -> None:
    from urllib.parse import urlparse

    host = urlparse(url).hostname or ""
    if host not in ALLOWED_HOSTS:
        raise PinError(f"refusing to fetch from host {host!r}; allowed: {ALLOWED_HOSTS}")


def fetch(pin: Pin, dest: Path, dry_run: bool = False, *, timeout: float = 60.0) -> Path:
    """Download pin into the directory dest as dest/<filename>.

    The bytes go to a temporary file in dest, are checked against the pinned byte count and SHA-256,
    and only then renamed into place. A file already in place that verifies is kept. dry_run prints
    the action and touches nothing.
    """
    dest = Path(dest)
    target = dest / pin.filename
    _check_host(pin.download_url)
    if target.is_file() and verify_file(target, pin):
        print(f"[fetch] {pin.key}: already present and verified at {target}")
        return target
    if dry_run:
        print(f"[fetch] DRY RUN {pin.key}: would download {pin.download_url} ({pin.bytes} bytes) to {target}")
        return target

    import requests  # imported late so that dry runs and verification need no network stack

    dest.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=dest, prefix=f".{pin.filename}.", suffix=".part")
    h = hashlib.sha256()
    n = 0
    try:
        with os.fdopen(fd, "wb") as out:
            with requests.get(pin.download_url, headers={"User-Agent": USER_AGENT}, stream=True,
                              timeout=timeout, allow_redirects=True) as r:
                r.raise_for_status()
                for block in r.iter_content(chunk_size=1 << 20):
                    if block:
                        out.write(block)
                        h.update(block)
                        n += len(block)
        if n != pin.bytes:
            raise PinError(f"{pin.key}: downloaded {n} bytes, pin says {pin.bytes}")
        if h.hexdigest() != pin.sha256:
            raise PinError(f"{pin.key}: SHA-256 mismatch after download")
        os.replace(tmp, target)
    except BaseException:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise
    print(f"[fetch] {pin.key}: verified and stored at {target}", file=sys.stdout)
    return target


def pins_for_benchmark(benchmark: str) -> list[Pin]:
    """The pins a benchmark needs. lcb_v6: six shards plus the loader file."""
    if benchmark == "humaneval_plus":
        return [PINS["humaneval_plus"]]
    if benchmark == "mbpp_plus":
        return [PINS["mbpp_plus"], PINS["mbpp_plus_patch"]]
    if benchmark == "lcb_v6":
        return [PINS[k] for k in LCB_SHARD_KEYS] + [PINS[LCB_LOADER_KEY]]
    raise KeyError(f"unknown benchmark {benchmark!r}")
