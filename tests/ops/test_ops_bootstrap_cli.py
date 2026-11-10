import json
import os
import stat
import subprocess
from pathlib import Path

import pytest

from ops import cli, cost
from ops.runpod_api import RunPodClient

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "ops" / "bootstrap.sh"


def test_bootstrap_syntax():
    assert subprocess.run(["bash", "-n", str(SCRIPT)]).returncode == 0


def test_bootstrap_dry_run_prints_actions_and_never_the_token():
    env = {**os.environ, "HF_TOKEN": "hf_TOPSECRETVALUE", "PATH": os.environ["PATH"]}
    r = subprocess.run(["bash", str(SCRIPT), "--plan", "pilot", "--dry-run"], capture_output=True, text=True, env=env, timeout=30)
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "TOPSECRET" not in out and "TOPSECRET" not in r.stderr and "HF_TOKEN: set" in out
    for frag in ("RTX PRO 6000", "uv sync --group pod --frozen", "hf_access check", "free-disk check", "/workspace/hf-cache", "T1 P1 P2"):
        assert frag in out
    assert out.count("[dry-run]") >= 6


def test_bootstrap_unknown_plan_and_arg():
    assert subprocess.run(["bash", str(SCRIPT), "--plan", "nope", "--dry-run"], capture_output=True).returncode == 64
    assert subprocess.run(["bash", str(SCRIPT), "--bogus"], capture_output=True).returncode == 64


def test_bootstrap_stops_on_wrong_gpu(tmp_path):
    fake = tmp_path / "bin"
    fake.mkdir()
    smi = fake / "nvidia-smi"
    smi.write_text("#!/bin/sh\necho 'NVIDIA A100-SXM4-80GB'\n")
    smi.chmod(smi.stat().st_mode | stat.S_IXUSR)
    env = {**os.environ, "PATH": f"{fake}:{os.environ['PATH']}", "OPS_STATE_DIR": str(tmp_path / "st"), "HF_HOME": str(tmp_path / "hf")}
    r = subprocess.run(["bash", str(SCRIPT), "--plan", "pilot"], capture_output=True, text=True, env=env, timeout=30)
    assert r.returncode == 3 and "RTX PRO 6000" in r.stderr
    assert not (tmp_path / "st").exists()                       # stopped before touching anything


class FakeClient(RunPodClient):
    created = []

    def __init__(self, key, dry_run=True, out=print, **kw):
        super().__init__(key, dry_run=dry_run, out=out, transport=self._t, environ={"HF_TOKEN": "hf_x"})

    @staticmethod
    def _t(method, url, headers, body):
        FakeClient.created.append((method, url))
        return 200, {"id": "podFAKE0000001"}


@pytest.fixture
def tmp_state(tmp_path, monkeypatch):
    monkeypatch.setenv("OPS_LOCAL_STATE", str(tmp_path / "state"))
    monkeypatch.setenv("RUNPOD_API_KEY", "rpa_SECRETKEY000000")
    FakeClient.created = []
    return tmp_path


def run_cli(argv, factory, out):
    a = cli.build_parser().parse_args(argv)
    return {"launch": lambda: cli.cmd_launch(a, out.append, factory), "stop": lambda: cli.cmd_stop(a, out.append, factory),
            "guard": lambda: cli.cmd_guard(a, out.append, factory)}[a.cmd]()


def test_launch_requires_price_flags():
    with pytest.raises(SystemExit):
        cli.build_parser().parse_args(["launch", "--plan", "pilot"])
    with pytest.raises(SystemExit):
        cli.build_parser().parse_args(["launch", "--plan", "pilot", "--hourly-price-usd", "2"])


def test_launch_dry_run_default_creates_nothing(tmp_state):
    out = []
    led = tmp_state / "L.csv"
    rc = run_cli(["launch", "--plan", "pilot", "--hourly-price-usd", "2.1", "--price-source", "console", "--image", "i/m:t",
                  "--ledger", str(led)], FakeClient, out)
    assert rc == 0 and FakeClient.created == [] and not led.exists()
    text = "\n".join(out)
    assert "dry run" in text and "bootstrap.sh --plan pilot" in text and "SECRETKEY" not in text


def test_launch_execute_appends_ledger_then_stop_completes_it(tmp_state):
    out = []
    led = tmp_state / "L.csv"
    assert run_cli(["launch", "--plan", "pilot", "--hourly-price-usd", "2.1", "--price-source", "console 2026-11-10",
                    "--image", "i/m:t", "--ledger", str(led), "--execute"], FakeClient, out) == 0
    rows = cost.read_rows(led)
    assert len(rows) == 1 and rows[0]["pod_id_prefix"] == "podF..." and rows[0]["run_id"] == "pilot" and rows[0]["stop_utc"] == ""
    state = json.loads((tmp_state / "state" / "pod.json").read_text())
    assert state["pod_id"] == "podFAKE0000001"
    text = "\n".join(out)
    assert "podFAKE0000001" not in text and "SECRETKEY" not in text
    out.clear()
    assert run_cli(["stop", "--ledger", str(led), "--reason", "operator_stop", "--execute"], FakeClient, out) == 0
    assert FakeClient.created[-1][0] == "POST" and FakeClient.created[-1][1].endswith("/stop")
    done = cost.read_rows(led)[0]
    assert done["stop_utc"] and done["reason_stopped"] == "operator_stop" and float(done["gpu_hours"]) >= 0


def test_stop_and_guard_default_to_dry_run(tmp_state):
    out = []
    assert run_cli(["stop", "--pod-id", "podABCDEF123456"], FakeClient, out) == 0
    assert run_cli(["guard", "--pod-id", "podABCDEF123456", "--run-id", "r", "--launched-at", "2026-11-10T00:00:00Z"], FakeClient, out) == 0
    assert FakeClient.created == []
    assert "podABCDEF123456" not in "\n".join(out) and "[dry-run]" in "\n".join(out)


def test_launch_refuses_stub_plan(tmp_state):
    with pytest.raises(SystemExit):
        run_cli(["launch", "--plan", "full", "--hourly-price-usd", "2", "--price-source", "x", "--image", "i"], FakeClient, [])


def test_plan_json_and_ledger_summary(tmp_path, capsys):
    assert cli.main(["plan", "--plan", "pilot", "--json"]) == 0
    d = json.loads(capsys.readouterr().out)
    assert len(d["jobs"]) == 40 and d["download_models"][0] == "T1"
    assert cli.main(["ledger", "summary", "--ledger", str(tmp_path / "none.csv")]) == 0
    assert "rows=0" in capsys.readouterr().out
