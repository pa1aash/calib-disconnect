"""Thin RunPod client over the REST API.

API used (RunPod REST reference, base URL configurable via RUNPOD_API_BASE or the constructor):
    POST   {base}/pods              create a pod
    GET    {base}/pods/{id}         status
    POST   {base}/pods/{id}/stop    stop (volume kept)
    DELETE {base}/pods/{id}         terminate
    header Authorization: Bearer <RUNPOD_API_KEY>
Request field names follow the REST reference as recalled by the author and were NOT verified against
a live API in this task (no network was used). The operator should check one dry-run request against
the console documentation before the first real launch.

The transport is injectable: transport(method, url, headers, json_body) -> (status_code, data).
A dry run prints each request with the key redacted and sends nothing.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

from .redact import redact, scrub

DEFAULT_BASE = "https://rest.runpod.io/v1"
# Needs operator confirmation in the RunPod console (GPU type list); override with RUNPOD_GPU_TYPE_ID.
DEFAULT_GPU_TYPE_ID = "NVIDIA RTX PRO 6000 Blackwell Server Edition"

Transport = Callable[[str, str, Mapping[str, str], Any], tuple[int, Any]]


class RunPodError(RuntimeError):
    pass


@dataclass(frozen=True)
class PodSpec:
    name: str
    gpu_type_id: str = DEFAULT_GPU_TYPE_ID
    image: str | None = None
    template_id: str | None = None
    container_disk_gb: int = 100
    volume_gb: int = 400
    volume_mount_path: str = "/workspace"
    gpu_count: int = 1
    env_names: tuple[str, ...] = ()
    ports: tuple[str, ...] = ("22/tcp",)

    def validate(self) -> None:
        if not self.image and not self.template_id:
            raise RunPodError("give an image (--image or RUNPOD_IMAGE) or a template (--template-id); none is assumed")
        if self.gpu_count != 1:
            raise RunPodError("the design budgets one GPU")


def requests_transport(method: str, url: str, headers: Mapping[str, str], body: Any) -> tuple[int, Any]:
    import requests

    r = requests.request(method, url, headers=dict(headers), json=body, timeout=60)
    try:
        data = r.json() if r.content else None
    except ValueError:
        data = {"raw": r.text[:200]}
    return r.status_code, data


class RunPodClient:
    def __init__(self, api_key: str | None, base_url: str | None = None, transport: Transport | None = None,
                 dry_run: bool = True, out: Callable[[str], None] = print,
                 environ: Mapping[str, str] | None = None) -> None:
        self.api_key = api_key
        self.base = (base_url or os.environ.get("RUNPOD_API_BASE") or DEFAULT_BASE).rstrip("/")
        self.transport = transport or requests_transport
        self.dry_run, self.out = dry_run, out
        self.environ = os.environ if environ is None else environ

    # ---- request plumbing
    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key or ''}", "Content-Type": "application/json"}

    def _shown_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {redact(self.api_key)}", "Content-Type": "application/json"}

    def _call(self, method: str, path: str, body: Any = None, shown_body: Any = None) -> Any:
        url = f"{self.base}{path}"
        if self.dry_run:
            self.out(f"[dry-run] {method} {redact_path(url)}")
            self.out(f"          headers: {json.dumps(self._shown_headers())}")
            if body is not None:
                self.out(f"          body: {json.dumps(shown_body if shown_body is not None else body, sort_keys=True)}")
            return {"dry_run": True}
        if not self.api_key:
            raise RunPodError("RUNPOD_API_KEY is not set")
        status, data = self.transport(method, url, self._headers(), body)
        if not 200 <= status < 300:
            msg = scrub(json.dumps(data)[:200] if data is not None else "", {"k": self.api_key}, ("k",))
            raise RunPodError(f"{method} {redact_path(url)} failed with HTTP {status}: {msg}")
        return data

    # ---- operations
    def _body(self, spec: PodSpec) -> tuple[dict[str, Any], dict[str, Any]]:
        spec.validate()
        env = {n: self.environ.get(n) for n in spec.env_names}
        if not self.dry_run:
            missing = [n for n, v in env.items() if not v]
            if missing:
                raise RunPodError(f"environment variable(s) not set: {', '.join(missing)}")
        body: dict[str, Any] = {
            "name": spec.name, "gpuTypeIds": [spec.gpu_type_id], "gpuCount": spec.gpu_count,
            "containerDiskInGb": spec.container_disk_gb, "volumeInGb": spec.volume_gb,
            "volumeMountPath": spec.volume_mount_path, "ports": list(spec.ports), "env": env,
        }
        if spec.template_id:
            body["templateId"] = spec.template_id
        else:
            body["imageName"] = spec.image
        shown = dict(body)
        shown["env"] = {n: redact(v) for n, v in env.items()}
        return body, shown

    def create_pod(self, spec: PodSpec) -> dict[str, Any]:
        body, shown = self._body(spec)
        return self._call("POST", "/pods", body, shown)

    def get_pod(self, pod_id: str) -> dict[str, Any]:
        return self._call("GET", f"/pods/{pod_id}")

    def stop_pod(self, pod_id: str) -> dict[str, Any]:
        return self._call("POST", f"/pods/{pod_id}/stop")

    def terminate_pod(self, pod_id: str) -> dict[str, Any]:
        return self._call("DELETE", f"/pods/{pod_id}")


def redact_path(url: str) -> str:
    """Hide the pod ID segment of /pods/<id>[/stop] in anything printed."""
    parts = url.split("/")
    for i, p in enumerate(parts[:-1]):
        if p == "pods":
            parts[i + 1] = redact(parts[i + 1])
            break
    return "/".join(parts)
