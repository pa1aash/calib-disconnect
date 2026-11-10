"""Reading capture, label, extraction, agreement, and fold files into `ReadoutData`; writing score and fit files.

Inputs (all under the run root, paths from `RunLayout`):
  capture index parquet (`TABLE_COLUMNS["capture_index"]`) + safetensors shard (arrays hs_p1, hs_p2, hs_p3,
  hs_mean_code of shape [N, L, D], code_logprobs, code_logprob_offsets); labels parquet in long format
  (sample_uid, suite_id, y, ...); extractions parquet (sample_uid, code, method, failure); agreement
  parquet (sample_uid, signature as canonical JSON or null); folds JSON (`FoldPlan.to_dict()`).

A sample with no label under a suite gets -1 (excluded from that suite's fits and scores).
Scores are written with exactly `TABLE_COLUMNS["scores"]`; fits as JSON lists of `FitRecord.to_dict()`
(NaN written as null).
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Sequence

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from pipeline.contracts.hashing import config_hash
from pipeline.contracts.interfaces import ReadoutData, StageReport
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest
from pipeline.contracts.schemas import (TABLE_COLUMNS, CaptureRecord, FitRecord, FoldPlan, HiddenStateRef,
                                        ReadoutScore)

from .common import NO_LABEL

PRODUCER = "pipeline.readouts.stage:run"
HIDDEN_KEYS = ("hs_p1", "hs_p2", "hs_p3", "hs_mean_code")

SCORE_SCHEMA = pa.schema([
    ("sample_uid", pa.string()), ("model_key", pa.string()), ("population", pa.string()), ("readout", pa.string()),
    ("label_suite", pa.string()), ("fold_seed", pa.int64()), ("fold", pa.int64()), ("prob", pa.float64()),
    ("rank_score", pa.float64()), ("rank_tiebreak", pa.float64()), ("missing", pa.bool_()), ("imputed", pa.bool_()),
    ("generation_set", pa.string()), ("flagged", pa.bool_()),
])
assert tuple(SCORE_SCHEMA.names) == TABLE_COLUMNS["scores"]


def problem_id_of(sample_uid: str) -> str:
    """sample_uid = model|generation_set|benchmark|problem_id|sample_index (schemas.sample_uid)."""
    parts = sample_uid.split("|")
    return "|".join(parts[3:-1])


def _load_tensors(path: Path) -> dict[str, np.ndarray]:
    from safetensors import safe_open
    out = {}
    with safe_open(str(path), framework="pt") as f:
        for k in f.keys():
            t = f.get_tensor(k)
            out[k] = t.float().numpy() if t.dtype.is_floating_point else t.numpy()
    return out


def _read_parquet_rows(path: Path):
    return pq.read_table(path).to_pylist()


def load_readout_data(layout: RunLayout, model_key: str, benchmarks: Sequence[str], gen_set: str = "frozen",
                      suites: Sequence[str] | None = None) -> ReadoutData | None:
    """Assemble ReadoutData over the given benchmarks (one population). None if no capture exists."""
    recs: list[CaptureRecord] = []
    hs: dict[str, list[np.ndarray]] = {k: [] for k in HIDDEN_KEYS}
    lps: list[np.ndarray] = []
    labels_by_uid: dict[str, dict[str, int]] = {}
    codes: dict[str, str | None] = {}
    failures: dict[str, str | None] = {}
    agree: dict[str, tuple | None] = {}
    for bench in benchmarks:
        shard_cache: dict[Path, dict[str, np.ndarray]] = {}
        s = 0
        while layout.capture_index(model_key, bench, gen_set, s).exists():
            for r in _read_parquet_rows(layout.capture_index(model_key, bench, gen_set, s)):
                shard_path = layout.root / r["shard_file"]
                if not shard_path.exists():
                    shard_path = layout.capture_shard(model_key, bench, gen_set, s)
                if shard_path not in shard_cache:
                    shard_cache[shard_path] = _load_tensors(shard_path)
                arr = shard_cache[shard_path]
                row = int(r["row"])
                recs.append(CaptureRecord(
                    sample_uid=r["sample_uid"],
                    hidden=HiddenStateRef(shard_file=r["shard_file"], row=row, layers=tuple(r["layers"])),
                    n_code_tokens=int(r["n_code_tokens"]), code_token_span=tuple(r["code_token_span"]),
                    p1=int(r["p1"]), p2=int(r["p2"]), p3=int(r["p3"]), elicitation_span=tuple(r["elicitation_span"]),
                    yes_no_logodds=float(r["yes_no_logodds"]), v1_text=r["v1_text"], v1_value=r["v1_value"],
                    sum_logprob=float(r["sum_logprob"]), mean_logprob=float(r["mean_logprob"]),
                    min_logprob=float(r["min_logprob"])))
                for k in HIDDEN_KEYS:
                    hs[k].append(arr[k][row])
                off = arr["code_logprob_offsets"]
                lps.append(np.asarray(arr["code_logprobs"][int(off[row]):int(off[row + 1])], dtype=np.float32))
            s += 1
        lp = layout.labels(model_key, bench, gen_set)
        if lp.exists():
            for r in _read_parquet_rows(lp):
                labels_by_uid.setdefault(r["sample_uid"], {})[r["suite_id"]] = int(r["y"])
        ep = layout.extractions(model_key, bench, gen_set)
        if ep.exists():
            for r in _read_parquet_rows(ep):
                codes[r["sample_uid"]] = r.get("code")
                failures[r["sample_uid"]] = r.get("failure")
        ap = layout.agreement_outputs(model_key, bench, gen_set)
        if ap.exists():
            for r in _read_parquet_rows(ap):
                sig = r.get("signature")
                if sig is None:
                    agree[r["sample_uid"]] = None
                else:
                    agree[r["sample_uid"]] = tuple(e if isinstance(e, str) else json.dumps(e, sort_keys=True)
                                                   for e in json.loads(sig))
    if not recs:
        return None
    order = sorted(range(len(recs)), key=lambda i: recs[i].sample_uid)
    recs = [recs[i] for i in order]
    uids = [r.sample_uid for r in recs]
    suite_ids = sorted(suites if suites is not None else {s for d in labels_by_uid.values() for s in d})
    labels = {s: np.array([labels_by_uid.get(u, {}).get(s, NO_LABEL) for u in uids], dtype=np.int8) for s in suite_ids}
    fails = [failures.get(u) for u in uids]
    return ReadoutData(
        sample_uids=uids, problem_ids=[problem_id_of(u) for u in uids], labels=labels, capture=recs,
        hidden={k: np.stack([hs[k][i] for i in order]).astype(np.float32) for k in HIDDEN_KEYS},
        code_texts=[codes.get(u) for u in uids], code_logprobs=[lps[i] for i in order],
        agreement_outputs={u: agree.get(u) for u in uids} if agree else None,
        extraction_failed=np.array([f is not None for f in fails], dtype=bool),
        truncated=np.array([f == "truncated" for f in fails], dtype=bool))


def load_plan(layout: RunLayout, population: str, fold_seed: int) -> FoldPlan | None:
    p = layout.folds(population, fold_seed)
    return FoldPlan.from_dict(json.loads(p.read_text())) if p.exists() else None


# ---------------------------------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------------------------------
def _nan_to_none(o):
    if isinstance(o, float) and not math.isfinite(o):
        return None
    if isinstance(o, dict):
        return {k: _nan_to_none(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_nan_to_none(v) for v in o]
    return o


def scores_table(rows: Sequence[ReadoutScore]) -> pa.Table:
    cols = {name: [getattr(r, name) for r in rows] for name in SCORE_SCHEMA.names}
    return pa.table(cols, schema=SCORE_SCHEMA)


def read_scores(path: Path) -> list[ReadoutScore]:
    return [ReadoutScore(**r) for r in pq.read_table(path).to_pylist()]


class Writer:
    """Writes score parquet and fit JSON files, adds each to the manifest, and lists it in the report."""

    def __init__(self, cfg, layout: RunLayout, manifest: Manifest, report: StageReport):
        self.layout, self.manifest, self.report = layout, manifest, report
        self.cfg_hash = config_hash(cfg.to_dict())

    def _register(self, path: Path) -> None:
        self.manifest.add(self.layout.root, path, PRODUCER, self.cfg_hash)
        rel = str(path.relative_to(self.layout.root))
        if rel not in self.report.outputs:
            self.report.outputs.append(rel)

    def scores(self, model_key: str, population: str, readout: str, suite: str | None, seed: int | None,
               rows: Sequence[ReadoutScore]) -> Path | None:
        if not rows:
            self.report.notes.append(f"no rows: {model_key}/{population}/{readout}/{suite}/seed{seed}")
            return None
        p = self.layout.scores(model_key, population, readout, suite, seed)
        p.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(scores_table(rows), p)
        self._register(p)
        return p

    def fits(self, model_key: str, population: str, readout: str, suite: str, seed: int,
             records: Sequence[FitRecord]) -> Path | None:
        if not records:
            return None
        p = self.layout.fits(model_key, population, readout, suite, seed)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps([_nan_to_none(r.to_dict()) for r in records], indent=1) + "\n")
        self._register(p)
        return p

    def json(self, path: Path, obj) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(_nan_to_none(obj), indent=1, sort_keys=True) + "\n")
        self._register(path)
        return path

    def tree(self, directory: Path) -> None:
        for p in sorted(Path(directory).rglob("*")):
            if p.is_file():
                self._register(p)


def json_load_fits(path: Path) -> list[FitRecord]:
    return [FitRecord.from_dict({k: (float("nan") if v is None and k.endswith("logloss") else v) for k, v in d.items()})
            for d in json.loads(Path(path).read_text())]
