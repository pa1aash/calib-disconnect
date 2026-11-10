"""Pins: agreement with the bench-A2 manifest, verification, and the guarded download."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from pipeline.contracts.layout import REPO_ROOT
from pipeline.data import pins as pm

from data_helpers import CACHE, needs_cache

MANIFEST = REPO_ROOT / "docs" / "s7" / "parts" / "bench-A2" / "MANIFEST.json"


def _fake_pin(content: bytes, **kw) -> pm.Pin:
    d = dict(key="fake", benchmark="x", role="pinned", url="https://github.com/a/b/raw/c/d.bin",
             download_url="https://github.com/a/b/raw/c/d.bin", revision={}, bytes=len(content),
             sha256=hashlib.sha256(content).hexdigest(), relpath="sub/d.bin")
    d.update(kw)
    return pm.Pin(**d)


def test_pins_match_manifest():
    if not MANIFEST.exists():
        pytest.skip("manifest absent")
    files = {f["url"]: f for f in json.loads(MANIFEST.read_text())["files"]}
    assert len(pm.PINS) == 10
    for pin in pm.PINS.values():
        f = files[pin.url]
        assert (f["bytes"], f["sha256"]) == (pin.bytes, pin.sha256), pin.key
    assert [pm.PINS[k].rows for k in pm.LCB_SHARD_KEYS] == [400, 111, 101, 101, 167, 175]
    assert sum(pm.PINS[k].rows for k in pm.LCB_SHARD_KEYS) == 1055
    assert all(pm.PINS[k].revision["commit"] == "0fe84c3912ea0c4d4a78037083943e8f0c4dd505"
               for k in pm.LCB_SHARD_KEYS + (pm.LCB_LOADER_KEY,))
    assert pm.PINS["mbpp_plus_patch"].sha256.startswith("3d7579ae")


@needs_cache
def test_pinned_files_verify_against_local_cache():
    for key in ("humaneval_plus", "mbpp_plus", "mbpp_plus_patch"):
        p = pm.locate_verified(pm.PINS[key], CACHE)
        assert pm.verify_file(p, pm.PINS[key])


def test_verify_file_detects_changes(tmp_path):
    content = b"hello pinned world"
    pin = _fake_pin(content)
    f = tmp_path / "d.bin"
    assert not pm.verify_file(f, pin)  # missing
    f.write_bytes(content)
    assert pm.verify_file(f, pin)
    f.write_bytes(b"hello pinned worle")  # same length, one byte different
    assert not pm.verify_file(f, pin)
    with pytest.raises(pm.PinError):
        pm.require_file(f, pin)
    f.write_bytes(content + b"!")
    assert not pm.verify_file(f, pin)


def test_fetch_dry_run_writes_nothing(tmp_path, capsys):
    pin = _fake_pin(b"abc")
    out = pm.fetch(pin, tmp_path / "dest", dry_run=True)
    assert not (tmp_path / "dest").exists() and out.name == "d.bin"
    assert "DRY RUN" in capsys.readouterr().out


class _Resp:
    def __init__(self, data: bytes):
        self.data = data

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def raise_for_status(self):
        pass

    def iter_content(self, chunk_size):
        for i in range(0, len(self.data), 4):
            yield self.data[i:i + 4]


def test_fetch_verifies_then_renames(tmp_path, monkeypatch):
    import requests

    content = b"payload-bytes-123"
    seen = {}

    def fake_get(url, headers=None, **kw):
        seen["ua"] = headers["User-Agent"]
        return _Resp(content)

    monkeypatch.setattr(requests, "get", fake_get)
    pin = _fake_pin(content)
    out = pm.fetch(pin, tmp_path / "dest")
    assert out.read_bytes() == content and seen["ua"].startswith("Mozilla/5.0")
    assert [p.name for p in (tmp_path / "dest").iterdir()] == ["d.bin"]


def test_fetch_rejects_wrong_bytes_and_leaves_nothing(tmp_path, monkeypatch):
    import requests

    monkeypatch.setattr(requests, "get", lambda url, **kw: _Resp(b"tampered-bytes!!!"))
    pin = _fake_pin(b"payload-bytes-123")  # same length, different content
    with pytest.raises(pm.PinError):
        pm.fetch(pin, tmp_path / "dest")
    assert list((tmp_path / "dest").iterdir()) == []
    monkeypatch.setattr(requests, "get", lambda url, **kw: _Resp(b"short"))
    with pytest.raises(pm.PinError):
        pm.fetch(pin, tmp_path / "dest")
    assert list((tmp_path / "dest").iterdir()) == []


def test_fetch_refuses_other_hosts(tmp_path):
    pin = _fake_pin(b"abc", download_url="https://example.org/x.bin")
    with pytest.raises(pm.PinError):
        pm.fetch(pin, tmp_path, dry_run=True)


def test_cli_dry_run_lists_all_lcb_files(tmp_path, capsys):
    from pipeline.data.__main__ import main

    assert main(["fetch", "--benchmark", "lcb_v6", "--dest", str(tmp_path / "x"), "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert out.count("DRY RUN") == 7 and "test6.jsonl" in out and "code_generation_lite.py" in out
    assert not (tmp_path / "x").exists()
