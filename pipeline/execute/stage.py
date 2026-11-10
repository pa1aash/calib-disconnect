"""Execute stage: ``pipeline.execute.stage:run`` (STAGES["execute"]).

Order of work (design section 6):
  1. read problems and suites written by the data stage;
  2. reference-solution check for HumanEval+ and MBPP+ (trusted canonical solutions; also writes the
     reference outputs and the agreement label-proxy shares);
  3. for each model and benchmark: read the generation shards, extract code (completion mode for models
     whose role is "base" or "coder_base"), write the extraction table;
  4. if cfg.execute_untrusted: preflight the sandbox, label every sample on every suite of its
     benchmark, compute behavior signatures on the agreement inputs, write both tables.
     If not: nothing extracted is executed; the report says so.

A dry run reads nothing heavy and writes nothing.
"""

from __future__ import annotations

import dataclasses
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

from pipeline.contracts import constants, hashing
from pipeline.contracts.interfaces import RunConfig, StageReport
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest
from pipeline.contracts.schemas import (
    TABLE_COLUMNS, ExtractionResult, Problem, TestSuite,
)

from .cache import ExecCache
from .extract import extract_code
from .labels import agreement_label_proxy, agreement_signatures, flip_table, label_samples, signature_to_json
from .reference import FUNCTION_BENCHMARKS, ReferenceStore, exclusion_report, reference_check
from .sandbox import IsolationError, SandboxConfig, SandboxExecutor

PRODUCER = "pipeline.execute.stage:run"
COMPLETION_ROLES = frozenset({"base", "coder_base"})


# ----------------------------------------------------------------------------------------------------
# IO helpers
# ----------------------------------------------------------------------------------------------------
def decode_suite(suite: TestSuite) -> TestSuite:
    """Suites are stored in the EvalPlus JSON form. MBPP+ needs the per-task step that turns some lists
    back into tuples, sets, or complex numbers (EvalPlus ``mbpp_deserialize_inputs``) before any input
    is run (pipeline/data/inputs.py documents the same requirement). The recorded input-set hash is the
    hash of the JSON form and is kept."""
    raw = [json.loads(json.dumps(list(i))) for i in suite.inputs]
    if suite.problem_id.startswith("Mbpp/"):
        from evalplus.data.mbpp import mbpp_deserialize_inputs

        raw = mbpp_deserialize_inputs(suite.problem_id, raw)
    return dataclasses.replace(suite, inputs=tuple(tuple(i) for i in raw))


def read_problems(layout: RunLayout, benchmark: str, cfg: RunConfig) -> list[Problem]:
    path = layout.problems(benchmark)
    probs = [Problem.from_dict(json.loads(line)) for line in path.read_text().splitlines() if line.strip()]
    if cfg.problem_ids:
        keep = set(cfg.problem_ids)
        probs = [p for p in probs if p.problem_id in keep]
    elif cfg.problem_limit is not None:
        probs = sorted(probs, key=lambda p: p.problem_id)[: cfg.problem_limit]
    return probs


def read_suites(layout: RunLayout, benchmark: str, problem_ids: set[str]) -> dict[str, dict[str, TestSuite]]:
    out: dict[str, dict[str, TestSuite]] = {}
    with open(layout.suites(benchmark)) as f:
        for line in f:
            if not line.strip():
                continue
            s = TestSuite.from_dict(json.loads(line))
            if s.problem_id in problem_ids:
                if benchmark in FUNCTION_BENCHMARKS:
                    s = decode_suite(s)
                out.setdefault(s.problem_id, {})[s.suite_id] = s
    return out


def _write_parquet(rows: list[dict[str, Any]], columns: tuple[str, ...], path: Path) -> None:
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq

    path.parent.mkdir(parents=True, exist_ok=True)
    table = pa.Table.from_pandas(pd.DataFrame(rows, columns=list(columns)), preserve_index=False)
    for i, f in enumerate(table.schema):  # an all-null column would be written with the null type
        if pa.types.is_null(f.type):
            table = table.set_column(i, f.name, table.column(i).cast(pa.string()))
    tmp = path.with_name(path.name + ".tmp")
    pq.write_table(table, tmp)
    os.replace(tmp, path)


def _read_shards(shard_dir: Path) -> list[dict[str, Any]]:
    import pandas as pd

    rows: list[dict[str, Any]] = []
    cols = ["sample_uid", "model_key", "benchmark", "problem_id", "generation_set", "completion_text", "truncated"]
    for f in sorted(shard_dir.glob("shard-*.parquet")):
        rows.extend(pd.read_parquet(f, columns=cols).to_dict("records"))
    return rows


def _make_executor(cfg: RunConfig, store: ReferenceStore) -> SandboxExecutor:
    x = dict(cfg.extra)
    sc = SandboxConfig(backend=cfg.sandbox, interpreter=x.get("interpreter"), execute_untrusted=cfg.execute_untrusted,
                       container_runtime=x.get("container_runtime"), container_image=x.get("container_image"),
                       bwrap_path=x.get("bwrap_path"))
    return SandboxExecutor(sc, references=store)


def _add(manifest: Manifest, layout: RunLayout, path: Path, cfg_hash: str, report: StageReport) -> None:
    manifest.add(layout.root, path, PRODUCER, cfg_hash)
    rel = os.path.relpath(path, layout.root)
    if rel not in report.outputs:
        report.outputs.append(rel)


def generation_dirs(layout: RunLayout, model: str, benchmark: str) -> list[Path]:
    base = layout.generation_shard(model, benchmark, "frozen", 0).parent.parent
    return sorted(d for d in base.glob("*") if d.is_dir()) if base.exists() else []


# ----------------------------------------------------------------------------------------------------
# Stage
# ----------------------------------------------------------------------------------------------------
def run(cfg: RunConfig, layout: RunLayout, manifest: Manifest, *, dry_run: bool = False) -> StageReport:
    rep = StageReport(stage="execute", ok=True)
    cfg_hash = hashing.config_hash(cfg.to_dict())
    workers = int(cfg.extra.get("workers", max(1, (os.cpu_count() or 2) - 1)))

    if dry_run:
        for b in cfg.benchmarks:
            for p in (layout.problems(b), layout.suites(b)):
                if not p.exists():
                    rep.notes.append(f"dry run: input missing: {os.path.relpath(p, layout.root)}")
                    rep.ok = False
        for m in cfg.models:
            for b in cfg.benchmarks:
                n = len(generation_dirs(layout, m, b))
                rep.notes.append(f"dry run: {m}/{b}: {n} generation set(s) found")
                rep.outputs.append(os.path.relpath(layout.extractions(m, b, "frozen"), layout.root))
                if cfg.execute_untrusted:
                    rep.outputs.append(os.path.relpath(layout.labels(m, b, "frozen"), layout.root))
                    rep.outputs.append(os.path.relpath(layout.agreement_outputs(m, b, "frozen"), layout.root))
        if not cfg.execute_untrusted:
            rep.notes.append("dry run: execute_untrusted is False, no extracted sample would be executed")
        return rep

    store = ReferenceStore(None)
    problems: dict[str, dict[str, Problem]] = {}
    suites: dict[str, dict[str, dict[str, TestSuite]]] = {}
    for b in cfg.benchmarks:
        plist = read_problems(layout, b, cfg)
        problems[b] = {p.problem_id: p for p in plist}
        suites[b] = read_suites(layout, b, set(problems[b]))
        store.load(layout.reference_outputs(b))
    executor = _make_executor(cfg, store)
    rep.metrics["sandbox"] = executor.sandbox_label
    rep.metrics["interpreter_sha256"] = executor.interpreter_sha256
    rep.metrics["harness_sha256"] = executor.bundle_sha256

    # -- 1. reference check ---------------------------------------------------------------------------
    checks = []
    excluded: set[tuple[str, str]] = set()
    proxies: dict[str, Any] = {}
    for b in cfg.benchmarks:
        if b not in FUNCTION_BENCHMARKS:
            continue
        plist = list(problems[b].values())
        cks = reference_check(plist, suites[b], executor, store=store, workers=workers)
        checks.extend(cks)
        excluded |= {(c.problem_id, c.suite_id) for c in cks if c.excluded}
        refp = store.save(layout.reference_outputs(b), only=set(problems[b]))
        _add(manifest, layout, refp, cfg_hash, rep)
        proxies[b] = agreement_label_proxy(plist, suites[b], store)
        er = exclusion_report([c for c in cks])
        for sid, d in sorted(er["per_suite"].items()):
            rep.metrics[f"reference_excluded_share/{b}/{sid}"] = d["share"]
            for pid, why in sorted(d["reasons"].items()):
                rep.notes.append(f"reference excluded: {b} {sid} {pid}: {why}")
        rep.metrics[f"reference_excluded_share_either_label_suite/{b}"] = er["share_either_label_suite"]
        if er["k1_triggered"]:
            rep.metrics["k1_triggered"] = True
            rep.notes.append(f"K1 TRIGGERED on {b}: reference exclusion above {constants.K1_MAX_REFERENCE_EXCLUSION}")
    if checks:
        _write_parquet([c.to_dict() for c in checks], TABLE_COLUMNS["reference_checks"], layout.reference_checks)
        _add(manifest, layout, layout.reference_checks, cfg_hash, rep)
        pj = layout.root / "execute" / "agreement_label_proxy.json"
        pj.parent.mkdir(parents=True, exist_ok=True)
        pj.write_text(json.dumps(proxies, indent=1, sort_keys=True) + "\n")
        _add(manifest, layout, pj, cfg_hash, rep)
    rep.metrics.setdefault("k1_triggered", False)

    # -- 2. extraction, labels, agreement ---------------------------------------------------------------
    can_execute = cfg.execute_untrusted
    if can_execute and cfg.sandbox == "trusted-only":
        rep.ok = False
        rep.notes.append("execute_untrusted is True but the sandbox is trusted-only, which never runs extracted "
                         "samples: extraction tables only")
        can_execute = False
    if not cfg.execute_untrusted:
        rep.notes.append("execute_untrusted is False: only the reference check ran; no extracted sample was "
                         "executed; labels and agreement outputs were not written")
    cache = None
    if can_execute:
        try:
            executor.preflight()
        except IsolationError as e:
            rep.ok = False
            rep.notes.append(f"isolation preflight failed, extracted samples were not executed: {e}")
            can_execute = False
        rep.metrics["preflight"] = executor.preflight_report
    if can_execute:
        cache = ExecCache(layout.exec_cache, audit_seed=int(cfg.extra.get("cache_audit_seed", 0)),
                          audit_log=layout.logs / "cache_audit.jsonl")

    all_labels = []
    fail_counts: dict[str, dict[str, int]] = {}
    for model in cfg.models:
        role = constants.MODELS[model][2] if model in constants.MODELS else "primary"
        mode = "completion" if role in COMPLETION_ROLES else "chat"
        for b in cfg.benchmarks:
            for d in generation_dirs(layout, model, b):
                rows = _read_shards(d)
                if not rows:
                    continue
                by_set: dict[str, list[dict[str, Any]]] = {}
                for r in rows:
                    by_set.setdefault(r["generation_set"], []).append(r)
                for gen_set, grows in sorted(by_set.items()):
                    _one_set(cfg, layout, manifest, rep, cfg_hash, executor, cache, model, b, gen_set, grows,
                             mode, problems[b], suites[b], excluded, workers, can_execute, fail_counts, all_labels)
    if cache is not None:
        rep.metrics["cache"] = cache.stats()
        cache.close()
        _add(manifest, layout, layout.exec_cache, cfg_hash, rep)
        if cache.mismatches:
            rep.notes.append(f"cache audit found {cache.mismatches} mismatch(es): see logs/cache_audit.jsonl")
    if all_labels:
        rep.metrics["flip_table"] = flip_table(all_labels)
    rep.metrics["extraction_failures"] = fail_counts
    if executor.diagnostics:
        rep.notes.append(f"{len(executor.diagnostics)} sandbox_error/killed run(s); first: {list(executor.diagnostics)[0][1:3]}")
    return rep


def _one_set(cfg, layout, manifest, rep, cfg_hash, executor, cache, model, b, gen_set, grows, mode, problems,
             suites, excluded, workers, can_execute, fail_counts, all_labels) -> None:
    ext_path = layout.extractions(model, b, gen_set)
    lab_path = layout.labels(model, b, gen_set)
    agr_path = layout.agreement_outputs(model, b, gen_set)
    done = ext_path.exists() and (not can_execute or (lab_path.exists() and agr_path.exists()))
    rels = [os.path.relpath(p, layout.root) for p in (ext_path, lab_path, agr_path)]
    if done and all(r in manifest.entries for r in rels[: 3 if can_execute else 1]):
        rep.skipped.append(f"{model}/{b}/{gen_set}")
        return
    extractions: list[ExtractionResult] = []
    for r in grows:
        p = problems.get(r["problem_id"])
        if p is None:
            rep.notes.append(f"{r['sample_uid']}: problem not in the problem file; skipped")
            continue
        use_mode = mode
        if mode == "completion" and b not in FUNCTION_BENCHMARKS:
            use_mode = "chat"  # base models run on the label-validity population only (section 10)
        extractions.append(extract_code(r["sample_uid"], r["completion_text"], p.entry_point, bool(r["truncated"]),
                                        mode=use_mode, prompt=p.prompt if use_mode == "completion" else None,
                                        benchmark=b))
    _write_parquet([e.to_dict() for e in extractions], TABLE_COLUMNS["extractions"], ext_path)
    _add(manifest, layout, ext_path, cfg_hash, rep)
    fail_counts[f"{model}/{b}/{gen_set}"] = dict(Counter(e.failure for e in extractions if e.failure))
    if not can_execute:
        return
    labels = label_samples(extractions, problems, suites, executor, cache, trusted=False, workers=workers,
                           excluded=excluded)
    _write_parquet([lab.to_dict() for lab in labels], TABLE_COLUMNS["labels"], lab_path)
    _add(manifest, layout, lab_path, cfg_hash, rep)
    all_labels.extend(labels)
    sigs = agreement_signatures(extractions, problems, suites, executor, cache, trusted=False, workers=workers)
    _write_parquet([{"sample_uid": e.sample_uid, "signature": signature_to_json(sigs.get(e.sample_uid))}
                    for e in extractions], ("sample_uid", "signature"), agr_path)
    _add(manifest, layout, agr_path, cfg_hash, rep)
