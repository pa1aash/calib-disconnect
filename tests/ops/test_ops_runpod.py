import json

import pytest

from ops.runpod_api import PodSpec, RunPodClient, RunPodError, redact_path

KEY = "fakekeyfakekeyfakekey"


def spec(**kw):
    return PodSpec(name="calib-x", image="example/img:tag", env_names=("HF_TOKEN",), **kw)


def test_dry_run_prints_redacted_and_sends_nothing():
    out, calls = [], []
    c = RunPodClient(KEY, transport=lambda *a: calls.append(a), dry_run=True, out=out.append, environ={"HF_TOKEN": "hf_SECRETVALUE123"})
    c.create_pod(spec())
    c.get_pod("podABCDEF123456")
    c.stop_pod("podABCDEF123456")
    c.terminate_pod("podABCDEF123456")
    text = "\n".join(out)
    assert calls == []
    assert KEY not in text and "TESTKEY" not in text and "SECRETVALUE" not in text and "podABCDEF123456" not in text
    assert "fake..." in text and "hf_S..." in text and "[dry-run] POST" in text and "DELETE" in text
    assert '"gpuTypeIds"' in text and '"HF_TOKEN"' in text


def test_fake_transport_requests():
    calls = []

    def transport(method, url, headers, body):
        calls.append((method, url, dict(headers), body))
        if method == "POST" and url.endswith("/pods"):
            return 201, {"id": "podNEW0000001"}
        return 200, {"desiredStatus": "EXITED"}

    c = RunPodClient(KEY, base_url="https://api.example.test/v9/", transport=transport, dry_run=False,
                     out=lambda s: None, environ={"HF_TOKEN": "hf_value"})
    assert c.create_pod(spec(volume_gb=500))["id"] == "podNEW0000001"
    c.get_pod("podNEW0000001")
    c.stop_pod("podNEW0000001")
    c.terminate_pod("podNEW0000001")
    assert [(m, u) for m, u, *_ in calls] == [
        ("POST", "https://api.example.test/v9/pods"), ("GET", "https://api.example.test/v9/pods/podNEW0000001"),
        ("POST", "https://api.example.test/v9/pods/podNEW0000001/stop"), ("DELETE", "https://api.example.test/v9/pods/podNEW0000001")]
    assert calls[0][2]["Authorization"] == f"Bearer {KEY}"
    body = calls[0][3]
    assert body["env"] == {"HF_TOKEN": "hf_value"}                       # passed through by name
    assert body["volumeInGb"] == 500 and body["gpuCount"] == 1 and body["imageName"] == "example/img:tag"


def test_template_instead_of_image():
    c = RunPodClient(KEY, dry_run=True, out=lambda s: None, environ={})
    body, _ = c._body(PodSpec(name="n", template_id="tpl123"))
    assert body["templateId"] == "tpl123" and "imageName" not in body


def test_image_or_template_required():
    c = RunPodClient(KEY, dry_run=True, out=lambda s: None, environ={})
    with pytest.raises(RunPodError):
        c.create_pod(PodSpec(name="n"))


def test_error_does_not_leak_key():
    c = RunPodClient(KEY, transport=lambda *a: (401, {"error": f"bad key {KEY}"}), dry_run=False, out=lambda s: None, environ={"HF_TOKEN": "x"})
    with pytest.raises(RunPodError) as e:
        c.get_pod("podABCDEF123456")
    assert "TESTKEY" not in str(e.value) and "podABCDEF123456" not in str(e.value) and "401" in str(e.value)


def test_missing_key_or_env_refused_when_live():
    with pytest.raises(RunPodError):
        RunPodClient(None, transport=lambda *a: (200, {}), dry_run=False, environ={}).get_pod("p")
    with pytest.raises(RunPodError):
        RunPodClient(KEY, transport=lambda *a: (200, {}), dry_run=False, environ={}).create_pod(spec())


def test_redact_path():
    assert redact_path("https://h/v1/pods/podABCDEF123456/stop") == "https://h/v1/pods/podA.../stop"
    assert redact_path("https://h/v1/pods") == "https://h/v1/pods"
