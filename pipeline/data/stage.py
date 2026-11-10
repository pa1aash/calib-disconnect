"""Data stage (STAGES["data"] = "pipeline.data.stage:run").

Writes, under the run root (pipeline.contracts.layout):
  data/problems_<benchmark>.jsonl         one Problem.to_dict() per line, sorted by problem ID
  data/suites_<benchmark>.jsonl           one TestSuite.to_dict() per line (every suite, including "agree")
  data/near_duplicates.json               groups, reasons, and the HumanEval+ pair diagnostic
  data/folds_<population>_seed<s>.json    FoldPlan for "label_validity" and "lcb"
  data/agreement_inputs_stats.json        per-problem generated / removed / kept counts, pins, hashes

Selection: cfg.problem_ids first (ids not in a benchmark are ignored for it), then cfg.problem_limit
(the first N IDs in sorted string order, per benchmark). Near-duplicate groups are always computed on
the full HumanEval+ and MBPP+ sets, so a subset run assigns each problem the fold the full run does.
The stage adds every file it writes to the manifest and does not save the manifest file itself.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

from pipeline.contracts import constants, hashing
from pipeline.contracts.interfaces import RunConfig, StageReport
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest

from . import agreement as agr
from . import folds as fl
from . import pins as pinmod
from .loader import EVALPLUS_BENCHMARKS, DataLoader

PRODUCER = "pipeline.data.stage:run"
STATS_NAME = "agreement_inputs_stats.json"
POPULATION_OF = {"humaneval_plus": "label_validity", "mbpp_plus": "label_validity", "lcb_v6": "lcb"}


class DataStageError(RuntimeError):
    pass


def stats_path(layout: RunLayout) -> Path:
    return layout.root / "data" / STATS_NAME


def _dump(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=True)


class _AtomicText:
    """Write text to a temp file next to the target; rename on close, remove on error."""

    def __init__(self, path: Path) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, self.tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
        self.f = os.fdopen(fd, "w", encoding="utf-8")

    def __enter__(self) -> "_AtomicText":
        return self

    def write(self, s: str) -> None:
        self.f.write(s)

    def __exit__(self, et, ev, tb) -> None:
        self.f.close()
        if et is None:
            os.replace(self.tmp, self.path)
        else:
            try:
                os.unlink(self.tmp)
            except FileNotFoundError:
                pass


def select_ids(all_ids: Iterable[str], cfg: RunConfig) -> list[str]:
    ids = sorted(all_ids)
    if cfg.problem_ids:
        want = set(cfg.problem_ids)
        ids = [i for i in ids if i in want]
    if cfg.problem_limit is not None:
        ids = ids[: cfg.problem_limit]
    return ids


def planned_outputs(cfg: RunConfig, layout: RunLayout) -> list[Path]:
    out: list[Path] = []
    for b in cfg.benchmarks:
        out += [layout.problems(b), layout.suites(b)]
    out.append(layout.near_duplicates)
    for pop in sorted({POPULATION_OF[b] for b in cfg.benchmarks}):
        out += [layout.folds(pop, s) for s in cfg.fold_seeds]
    out.append(stats_path(layout))
    return out


def run(cfg: RunConfig, layout: RunLayout, manifest: Manifest, *, dry_run: bool = False) -> StageReport:
    unknown = [b for b in cfg.benchmarks if b not in constants.BENCHMARKS]
    if unknown:
        raise DataStageError(f"unknown benchmarks {unknown}; known: {constants.BENCHMARKS}")
    rel = lambda p: os.path.relpath(p, layout.root)  # noqa: E731
    planned = planned_outputs(cfg, layout)
    loader = DataLoader(cfg.bench_cache, agreement_seed=int(cfg.extra.get("agreement_seed", 0)),
                        workers=int(cfg.extra.get("data_workers", min(8, os.cpu_count() or 2))))
    notes: list[str] = []

    if "lcb_v6" in cfg.benchmarks:
        missing = loader.lcb.missing_shards()
        if missing and not dry_run:
            raise DataStageError(f"LiveCodeBench shards missing from {loader.cache_dir}: {missing}. "
                                 f"Fetch them with: {loader.lcb.fetch_command()}")
        if missing:
            notes.append(f"LiveCodeBench shards missing ({len(missing)}); a real run needs: {loader.lcb.fetch_command()}")

    if dry_run:
        notes.append("dry run: nothing written, manifest unchanged")
        return StageReport(stage="data", ok=True, outputs=[rel(p) for p in planned], notes=notes,
                           metrics={"dry_run": True, "benchmarks": list(cfg.benchmarks)})

    cfg_hash = hashing.config_hash(cfg.to_dict())
    written: list[Path] = []

    # -- pins and label-validity problems (always the full sets, for near-duplicate groups)
    lv_wanted = [b for b in cfg.benchmarks if b in EVALPLUS_BENCHMARKS]
    pin_checks = loader.verify_pins(EVALPLUS_BENCHMARKS if lv_wanted else ())
    bad = [f for f, ok in pin_checks if not ok]
    if bad:
        raise DataStageError(f"pinned files do not match their pins: {bad}")
    full_lv = []
    if lv_wanted:
        for b in EVALPLUS_BENCHMARKS:
            full_lv += loader.problems(b)
    report = fl.near_duplicate_report(full_lv)

    all_ids_by_bench: dict[str, list[str]] = {}
    problems_by_bench: dict[str, dict[str, Any]] = {}
    for b in cfg.benchmarks:
        probs = {p.problem_id: p for p in loader.problems(b)}
        problems_by_bench[b] = probs
        all_ids_by_bench[b] = list(probs)
    if cfg.problem_ids:
        known = {i for ids in all_ids_by_bench.values() for i in ids}
        missing_ids = sorted(set(cfg.problem_ids) - known)
        if missing_ids:
            raise DataStageError(f"problem_ids not found in the configured benchmarks: {missing_ids[:5]}")

    selected: dict[str, list[str]] = {b: select_ids(all_ids_by_bench[b], cfg) for b in cfg.benchmarks}
    agree_stats: dict[str, Any] = {}
    metrics: dict[str, Any] = {}

    for b in cfg.benchmarks:
        ids = selected[b]
        probs = [problems_by_bench[b][i] for i in ids]
        with _AtomicText(layout.problems(b)) as f:
            for p in probs:
                f.write(_dump(p.to_dict()) + "\n")
        written.append(layout.problems(b))

        n_suites = 0
        if b in EVALPLUS_BENCHMARKS:
            base = {p.problem_id: loader.suites(p) for p in probs}
            agree = loader.agreement_batch(probs, base) if probs else {}
            with _AtomicText(layout.suites(b)) as f:
                for p in probs:
                    allsuites = dict(base[p.problem_id])
                    allsuites["agree"] = agree[p.problem_id]
                    for sid in sorted(allsuites):
                        f.write(_dump(allsuites[sid].to_dict()) + "\n")
                        n_suites += 1
            stats = {pid: loader.agreement_stats[pid] for pid in ids}
            agree_stats[b] = stats
            metrics[f"{b}_agreement_empty"] = sum(1 for s in stats.values() if s.get("kept", 0) == 0)
            metrics[f"{b}_agreement_kept_total"] = sum(s.get("kept", 0) for s in stats.values())
        else:
            loader.lcb.zero_agreement.clear()
            with _AtomicText(layout.suites(b)) as f:
                for p in probs:
                    s = loader.lcb_suites_with_agree(p)
                    for sid in sorted(s):
                        f.write(_dump(s[sid].to_dict()) + "\n")
                        n_suites += 1
            agree_stats[b] = {"n_problems": len(ids), "n_zero_agreement": len(loader.lcb.zero_agreement),
                              "zero_agreement_ids": sorted(loader.lcb.zero_agreement)}
            metrics["lcb_zero_agreement"] = len(loader.lcb.zero_agreement)
        written.append(layout.suites(b))
        metrics[f"{b}_problems"] = len(ids)
        metrics[f"{b}_suites"] = n_suites

    # -- near duplicates and folds
    with _AtomicText(layout.near_duplicates) as f:
        f.write(json.dumps(report.to_dict(), sort_keys=True, indent=1) + "\n")
    written.append(layout.near_duplicates)
    metrics["near_duplicate_groups"] = len(report.groups)
    for pop in sorted({POPULATION_OF[b] for b in cfg.benchmarks}):
        pop_ids = [i for b in cfg.benchmarks if POPULATION_OF[b] == pop for i in selected[b]]
        groups = report.groups if pop == "label_validity" else []
        for s in cfg.fold_seeds:
            plan = fl.build_folds(pop_ids, groups, s, pop)
            with _AtomicText(layout.folds(pop, s)) as f:
                f.write(json.dumps(plan.to_dict(), sort_keys=True, indent=1) + "\n")
            written.append(layout.folds(pop, s))

    # -- stats and provenance
    used = []
    for b in cfg.benchmarks:
        used += [p.key for p in pinmod.pins_for_benchmark(b)]
    if lv_wanted:
        used += [p.key for b in EVALPLUS_BENCHMARKS for p in pinmod.pins_for_benchmark(b)]
    prov: dict[str, Any] = {"pins": {k: pinmod.PINS[k].sha256 for k in sorted(set(used))}}
    if loader.patch_sha256:
        prov["mbpp_plus_patch_file_sha256"] = loader.patch_sha256
        rows = [loader._rows[i] for i in sorted(loader._rows) if i.startswith("Mbpp/")]
        prov["mbpp_plus_patched_rows_sha256"] = hashing.config_hash(rows)
        prov["mbpp_plus_patched_ids"] = [p.problem_id for p in loader.problems("mbpp_plus") if p.patched]
    stats_doc = {"format": "calib-disconnect/agreement_stats/v1", "agreement_seed": loader.agreement_seed,
                 "n_generate": agr.N_GENERATE, "cap": constants.AGREEMENT_INPUT_CAP,
                 "max_attempts": agr.MAX_ATTEMPTS, "per_benchmark": agree_stats, "provenance": prov}
    with _AtomicText(stats_path(layout)) as f:
        f.write(json.dumps(stats_doc, sort_keys=True, indent=1) + "\n")
    written.append(stats_path(layout))

    for p in written:
        manifest.add(layout.root, p, producer=PRODUCER, config_hash=cfg_hash)
    return StageReport(stage="data", ok=True, outputs=[rel(p) for p in written], notes=notes, metrics=metrics)
