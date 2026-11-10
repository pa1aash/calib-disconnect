import io
import tarfile

import pytest

from ops import sync
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest

HOST, PORT, KEY = "203.0.113.77", "22222", "/home/op/.ssh/pod_ed25519_key"
ENV = {"POD_SSH_HOST": HOST, "POD_SSH_PORT": PORT, "POD_SSH_KEY": KEY}


def build_run(tmp_path, run_id="r1"):
    lay = RunLayout.for_run(run_id, tmp_path)
    files = {"data/a.jsonl": "alpha", "generations/m/b.parquet": "beta",
             "capture/m/h/f/shard-00000.safetensors": "hidden", "adapters/m/x.safetensors": "lora"}
    m = Manifest(run_id=run_id)
    for rel, txt in files.items():
        p = lay.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(txt)
        m.add(lay.root, p, "t", "h", "g")
    m.save(lay.manifest)
    return lay


def test_verify_ok(tmp_path):
    lay = build_run(tmp_path)
    r = sync.verify_run(lay.root)
    assert len(r.ok) == 4 and r.exit_code == 0


def test_verify_mismatch_exits_nonzero(tmp_path):
    lay = build_run(tmp_path)
    (lay.root / "data/a.jsonl").write_text("changed")
    r = sync.verify_run(lay.root)
    assert r.mismatched == ["data/a.jsonl"] and r.exit_code == 1


def test_verify_missing_unexpected_vs_skip_large(tmp_path):
    lay = build_run(tmp_path)
    (lay.root / "capture/m/h/f/shard-00000.safetensors").unlink()
    (lay.root / "adapters/m/x.safetensors").unlink()
    r = sync.verify_run(lay.root, skip_large=True)
    assert len(r.missing_expected) == 2 and r.exit_code == 0
    r2 = sync.verify_run(lay.root, skip_large=False)
    assert len(r2.missing_unexpected) == 2 and r2.exit_code == 2
    (lay.root / "generations/m/b.parquet").unlink()                  # not a large file: unexpected even with skip-large
    r3 = sync.verify_run(lay.root, skip_large=True)
    assert r3.missing_unexpected == ["generations/m/b.parquet"] and r3.exit_code == 2
    (lay.root / "data/a.jsonl").write_text("x")
    assert sync.verify_run(lay.root, skip_large=True).exit_code == 1   # mismatch outranks missing


def test_rsync_command_shown_is_redacted():
    p = sync.SshParams.from_env(ENV)
    real = " ".join(sync.build_rsync_cmd(p, "r1", sync.Path("/tmp/x"), True))
    shown = " ".join(sync.build_rsync_cmd(p, "r1", sync.Path("/tmp/x"), True, shown=True))
    assert HOST in real and KEY in real and "--exclude=adapters/" in real
    for secret in (HOST, KEY, "pod_ed25519_key", PORT):
        assert secret not in shown
    assert "203." in shown and "..." in shown


def test_main_dry_run_prints_redacted_and_runs_nothing(tmp_path):
    out, calls = [], []
    rc = sync.main(["--run-id", "r1", "--skip-large"], environ=ENV, runner=lambda *a, **k: calls.append(a), out=out.append, runs_root=tmp_path)
    text = "\n".join(out)
    assert rc == 0 and calls == [] and "[dry-run]" in text and HOST not in text and "pod_ed25519" not in text


def test_main_execute_pulls_then_verifies(tmp_path):
    lay = build_run(tmp_path)
    out = []

    class R:
        returncode = 0
    rc = sync.main(["--run-id", "r1", "--execute"], environ=ENV, runner=lambda cmd, **k: R(), out=out.append, runs_root=tmp_path)
    assert rc == 0 and "verified ok: 4" in "\n".join(out)
    (lay.root / "data/a.jsonl").write_text("tampered")
    assert sync.main(["--run-id", "r1", "--execute"], environ=ENV, runner=lambda cmd, **k: R(), out=out.append, runs_root=tmp_path) == 1

    class F:
        returncode = 23
    assert sync.main(["--run-id", "r1", "--execute"], environ=ENV, runner=lambda cmd, **k: F(), out=out.append, runs_root=tmp_path) == 3


def test_missing_env_is_refused():
    with pytest.raises(SystemExit):
        sync.SshParams.from_env({})


def test_tarball_extract_and_verify(tmp_path):
    src = build_run(tmp_path / "src")
    tar = tmp_path / "run.tar.gz"
    with tarfile.open(tar, "w:gz") as tf:
        for p in sorted(src.root.rglob("*")):
            if p.is_file():
                tf.add(p, arcname=str(p.relative_to(src.root)))
    out = []
    rc = sync.main(["--run-id", "r1", "--tarball", str(tar), "--execute"], out=out.append, runs_root=tmp_path / "dst")
    assert rc == 0 and (tmp_path / "dst/r1/data/a.jsonl").read_text() == "alpha"


def test_tarball_path_traversal_rejected(tmp_path):
    tar = tmp_path / "evil.tar"
    with tarfile.open(tar, "w") as tf:
        ti = tarfile.TarInfo("../evil.txt")
        ti.size = 3
        tf.addfile(ti, io.BytesIO(b"abc"))
    with pytest.raises(Exception):
        sync.extract_tarball(tar, tmp_path / "dest")
    assert not (tmp_path / "evil.txt").exists()
