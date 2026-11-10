"""Named plans: each expands into a RunConfig and an ordered job list.

A plan file (ops/plans/<name>.json) holds "config" (RunConfig fields) and "groups". A group expands to
the product stages x models x scopes (a missing list means one entry with None). A scope is a
benchmark or a population name ("label_validity"). A job is (stage, model_key, scope, generation set);
its ID is stable and names the done marker under <run>/state/.
"""

from __future__ import annotations

import dataclasses
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from pipeline.contracts import constants as C
from pipeline.contracts.interfaces import RunConfig
from pipeline.contracts.layout import RunLayout

PLANS_DIR = Path(__file__).resolve().parent / "plans"
STAGE_ORDER = ("data", "generate", "execute", "capture", "readouts", "analysis")
POPULATIONS = ("label_validity",)
NON_REPO_MODELS = ("SMOKE", "MOCK")
_ID_BAD = re.compile(r"[^A-Za-z0-9_.-]")


@dataclass(frozen=True)
class Job:
    stage: str
    model_key: str | None
    scope: str | None
    gen_set: str = "frozen"
    kind: str = "normal"            # "normal" | "timing" (outputs timed, never analyzed)
    name: str = ""                  # distinguishes timing probes that share stage, model, and scope
    overrides: Mapping[str, Any] = field(default_factory=dict, compare=False, hash=False)

    @property
    def id(self) -> str:
        parts = [self.stage, self.model_key or "all", self.scope or "all", self.gen_set]
        if self.kind == "timing":
            parts.insert(0, "timing")
            parts.append(self.name or "probe")
        return _ID_BAD.sub("_", ".".join(parts))

    def describe(self) -> str:
        extra = f" kind={self.kind}" if self.kind != "normal" else ""
        return f"{self.id}  (stage={self.stage} model={self.model_key} scope={self.scope} gen_set={self.gen_set}{extra})"


@dataclass(frozen=True)
class Plan:
    name: str
    description: str
    cfg: RunConfig
    jobs: tuple[Job, ...]
    launchable: bool = True
    pod: bool = True

    def download_models(self) -> tuple[str, ...]:
        """Model keys whose weights the plan needs, in first-use order (job order), without SMOKE or MOCK."""
        seen: list[str] = []
        for j in self.jobs:
            if j.model_key and j.model_key not in NON_REPO_MODELS and j.model_key not in seen:
                seen.append(j.model_key)
        return tuple(seen)


def available_plans() -> list[str]:
    return sorted(p.stem for p in PLANS_DIR.glob("*.json"))


def model_repo(key: str) -> tuple[str, str]:
    """(repository ID, pinned revision) for a model key."""
    if key == "SMOKE":
        return C.SMOKE_MODEL
    if key not in C.MODELS:
        raise KeyError(f"unknown model key {key!r}")
    repo, rev = C.MODELS[key][:2]
    return repo, rev


def _expand_groups(groups: list[dict[str, Any]], valid_fields: set[str]) -> list[Job]:
    jobs: dict[str, Job] = {}
    for g in groups:
        ov = dict(g.get("overrides", {}))
        bad = set(ov) - valid_fields
        if bad:
            raise ValueError(f"unknown RunConfig override(s) {sorted(bad)}")
        for stage in g["stages"]:
            if stage not in STAGE_ORDER:
                raise ValueError(f"unknown stage {stage!r}")
            for model in g.get("models") or [None]:
                for scope in g.get("scopes") or [None]:
                    j = Job(stage=stage, model_key=model, scope=scope, gen_set=g.get("gen_set", "frozen"),
                            kind=g.get("kind", "normal"), name=g.get("name", ""), overrides=ov)
                    if j.id in jobs:
                        raise ValueError(f"duplicate job id {j.id}")
                    jobs[j.id] = j
    return list(jobs.values())


def with_container_image(plan: Plan, image: str | None) -> Plan:
    """--container-image: switch the sandbox backend to "container" with the pinned image (name@sha256:...)."""
    if not image:
        return plan
    cfg = dataclasses.replace(plan.cfg, sandbox="container", extra={**dict(plan.cfg.extra), "container_image": image})
    return dataclasses.replace(plan, cfg=cfg)


def load_plan(name: str, run_id: str | None = None, plans_dir: Path | None = None,
              container_image: str | None = None) -> Plan:
    path = (plans_dir or PLANS_DIR) / f"{name}.json"
    if not path.is_file():
        raise SystemExit(f"unknown plan {name!r}; available: {', '.join(available_plans())}")
    spec = json.loads(path.read_text())
    cfg = RunConfig.from_dict({"run_id": run_id or spec["name"], **spec["config"]})
    jobs = _expand_groups(spec["groups"], {f.name for f in dataclasses.fields(RunConfig)})
    for j in jobs:
        if j.model_key and j.model_key not in cfg.models:
            raise ValueError(f"job {j.id}: model {j.model_key} is not in the plan config")
        if j.stage not in cfg.stages:
            raise ValueError(f"job {j.id}: stage not in the plan config stages")
    plan = Plan(name=spec["name"], description=spec.get("description", ""), cfg=cfg, jobs=tuple(jobs),
                launchable=bool(spec.get("launchable", True)), pod=bool(spec.get("pod", True)))
    return with_container_image(plan, container_image)


def order_jobs(jobs: list[Job] | tuple[Job, ...]) -> list[Job]:
    """Dependency order: data jobs, then one block per model in first-appearance order (stages in
    STAGE_ORDER, timing probes after the model's normal jobs), then the model-free later stages
    (analysis). One model is active at a time."""
    idx = {j.id: i for i, j in enumerate(jobs)}
    rank = {s: i for i, s in enumerate(STAGE_ORDER)}

    def key(j: Job) -> tuple:
        # fresh generation-shift sets need the S^R adapters, which the model's frozen readouts train
        return (j.kind == "timing", j.gen_set.startswith("fresh:"), rank[j.stage], idx[j.id])

    pre = [j for j in jobs if j.model_key is None and j.stage == "data"]
    post = [j for j in jobs if j.model_key is None and j.stage != "data"]
    models: list[str] = []
    for j in jobs:
        if j.model_key and j.model_key not in models:
            models.append(j.model_key)
    out = sorted(pre, key=key)
    for m in models:
        out += sorted((j for j in jobs if j.model_key == m), key=key)
    return out + sorted(post, key=key)


_SR_ID = re.compile(r"^SR_(?P<suite>.+)_seed(?P<seed>\d+)_fold(?P<fold>\d+)$")
FRESH_POPULATION = {"P1": "label_validity", "S1": "lcb"}


def sr_adapter_rel(model_key: str, adapter_id: str) -> str:
    """Run-root-relative path where the readouts stage saves the S^R adapter, built with the layout's
    own adapters() directory and the stage's name rule sr_<population>_<suite>_seed<s>_fold<f>."""
    m = _SR_ID.match(adapter_id)
    if not m:
        raise ValueError(f"not an S^R adapter id: {adapter_id}")
    pop = FRESH_POPULATION[model_key]
    name = f"sr_{pop}_{m['suite']}_seed{m['seed']}_fold{m['fold']}"
    lay = RunLayout.for_run("x", Path("."))
    return (lay.adapters(model_key) / name).relative_to(lay.root).as_posix()


def resolve_fresh(f: Mapping[str, Any], k: int) -> dict[str, Any]:
    out = dict(f)
    out["k_g"] = k if out.get("k_g", "k") == "k" else int(out["k_g"])
    out["adapter_path"] = sr_adapter_rel(out["model_key"], out["adapter_id"])
    return out


def job_config(cfg: RunConfig, job: Job) -> RunConfig:
    """The RunConfig a stage sees for one job: one model, one benchmark (or the plan's benchmarks for a
    population scope), and only its own stage. Job overrides apply last; "extra" is merged."""
    ov = dict(job.overrides)
    extra = {**dict(cfg.extra), "job_id": job.id, "gen_set": job.gen_set, "scope": job.scope,
             "job_kind": job.kind, **dict(ov.pop("extra", {}))}
    kw: dict[str, Any] = {"stages": (job.stage,), "extra": extra}
    if job.model_key:
        kw["models"] = (job.model_key,)
    if job.scope in C.BENCHMARKS:
        kw["benchmarks"] = (job.scope,)
    elif job.scope == "lcb":
        kw["benchmarks"] = tuple(b for b in cfg.benchmarks if b == "lcb_v6")
    elif job.scope == "label_validity":
        kw["benchmarks"] = tuple(b for b in cfg.benchmarks if b in C.LABEL_VALIDITY_BENCHMARKS)
    if job.kind == "timing" and job.model_key:
        # timing-only probes are exempt from the generation-only skip (G10)
        kw["generation_only_models"] = tuple(m for m in cfg.generation_only_models if m != job.model_key)
    if "fresh" in extra:
        extra["fresh"] = [resolve_fresh(f, cfg.k) for f in extra["fresh"]]
    kw.update({k: (tuple(v) if isinstance(v, list) else v) for k, v in ov.items()})
    return dataclasses.replace(cfg, **kw)
