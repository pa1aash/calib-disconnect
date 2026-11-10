"""Shards: parquet generations, safetensors capture arrays plus an index parquet (design 5, 12.5).

Writes go to a hidden temp file in the destination directory and are renamed into place, so an
interrupted job never leaves a torn shard. A shard is complete when its file exists and the manifest
entry of its path has the file's SHA-256 and the expected config hash; complete shards are skipped.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from pipeline.contracts.hashing import sha256_file
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest
from pipeline.contracts.schemas import TABLE_COLUMNS, CaptureRecord, GenerationRecord, HiddenStateRef

_GEN_TYPES = {
    "seed": pa.uint64(), "sample_index": pa.int64(), "completion_token_ids": pa.list_(pa.int64()),
    "truncated": pa.bool_(), "thinking": pa.bool_(),
}
_IDX_TYPES = {
    "row": pa.int64(), "layers": pa.list_(pa.int64()), "n_code_tokens": pa.int64(),
    "code_token_span": pa.list_(pa.int64()), "p1": pa.int64(), "p2": pa.int64(), "p3": pa.int64(),
    "elicitation_span": pa.list_(pa.int64()), "yes_no_logodds": pa.float64(), "v1_value": pa.float64(),
    "sum_logprob": pa.float64(), "mean_logprob": pa.float64(), "min_logprob": pa.float64(),
}


def atomic_write(path: Path, write: Callable[[Path], None]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    try:
        write(tmp)
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def _table(columns: Sequence[str], rows: list[dict[str, Any]], types: Mapping[str, pa.DataType]) -> pa.Table:
    arrays = []
    for c in columns:
        vals = [r[c] for r in rows]
        arrays.append(pa.array(vals, type=types.get(c)))
    return pa.Table.from_arrays(arrays, names=list(columns))


# ---- generations -------------------------------------------------------------------------------------
def write_generation_shard(path: Path, records: Sequence[GenerationRecord]) -> None:
    cols = TABLE_COLUMNS["generations"]
    rows = [{c: (list(getattr(r, c)) if c == "completion_token_ids" else getattr(r, c)) for c in cols} for r in records]
    table = _table(cols, rows, _GEN_TYPES)
    atomic_write(path, lambda tmp: pq.write_table(table, tmp))


def read_generation_shard(path: Path) -> list[GenerationRecord]:
    t = pq.read_table(path)
    if tuple(t.column_names) != TABLE_COLUMNS["generations"]:
        raise ValueError(f"{path}: columns differ from TABLE_COLUMNS['generations']")
    out = []
    for row in t.to_pylist():
        row["completion_token_ids"] = tuple(row["completion_token_ids"])
        out.append(GenerationRecord(**row))
    return out


# ---- capture -----------------------------------------------------------------------------------------
def write_capture_shard(shard_path: Path, index_path: Path, records: Sequence[CaptureRecord],
                        arrays: Mapping[str, Any], shard_file_rel: str) -> list[CaptureRecord]:
    """Write the safetensors arrays and the index parquet. Returns the records with shard_file set."""
    import torch
    from safetensors.torch import save_file
    tensors = {}
    for k, v in arrays.items():
        t = v if isinstance(v, torch.Tensor) else torch.from_numpy(np.ascontiguousarray(v))
        tensors[k] = t.contiguous()
    layers = records[0].hidden.layers if records else ()
    meta = {"format": "calib-disconnect/capture/v1", "layers": ",".join(str(x) for x in layers),
            "positions": "p1,p2,p3,mean_code", "n": str(len(records))}
    atomic_write(shard_path, lambda tmp: save_file(tensors, str(tmp), metadata=meta))
    fixed = [CaptureRecord(**{**r.__dict__, "hidden": HiddenStateRef(
        shard_file=shard_file_rel, row=r.hidden.row, layers=tuple(r.hidden.layers), positions=r.hidden.positions,
        dtype=r.hidden.dtype)}) for r in records]
    cols = TABLE_COLUMNS["capture_index"]
    rows = []
    for r in fixed:
        rows.append({"sample_uid": r.sample_uid, "shard_file": r.hidden.shard_file, "row": r.hidden.row,
                     "layers": list(r.hidden.layers), "n_code_tokens": r.n_code_tokens,
                     "code_token_span": list(r.code_token_span), "p1": r.p1, "p2": r.p2, "p3": r.p3,
                     "elicitation_span": list(r.elicitation_span), "yes_no_logodds": r.yes_no_logodds,
                     "v1_text": r.v1_text, "v1_value": r.v1_value, "sum_logprob": r.sum_logprob,
                     "mean_logprob": r.mean_logprob, "min_logprob": r.min_logprob})
    table = _table(cols, rows, _IDX_TYPES)
    atomic_write(index_path, lambda tmp: pq.write_table(table, tmp))
    return fixed


def read_capture_index(path: Path) -> list[CaptureRecord]:
    t = pq.read_table(path)
    if tuple(t.column_names) != TABLE_COLUMNS["capture_index"]:
        raise ValueError(f"{path}: columns differ from TABLE_COLUMNS['capture_index']")
    out = []
    for r in t.to_pylist():
        out.append(CaptureRecord(
            sample_uid=r["sample_uid"], hidden=HiddenStateRef(shard_file=r["shard_file"], row=r["row"], layers=tuple(r["layers"])),
            n_code_tokens=r["n_code_tokens"], code_token_span=tuple(r["code_token_span"]), p1=r["p1"], p2=r["p2"], p3=r["p3"],
            elicitation_span=tuple(r["elicitation_span"]), yes_no_logodds=r["yes_no_logodds"], v1_text=r["v1_text"],
            v1_value=r["v1_value"], sum_logprob=r["sum_logprob"], mean_logprob=r["mean_logprob"],
            min_logprob=r["min_logprob"]))
    return out


def load_capture_shard(path: Path) -> dict[str, np.ndarray]:
    """Read a capture shard; bfloat16 hidden states come back as float32 numpy (numpy has no bfloat16)."""
    from safetensors import safe_open
    out: dict[str, np.ndarray] = {}
    with safe_open(str(path), framework="pt") as f:
        for k in f.keys():
            t = f.get_tensor(k)
            out[k] = t.float().numpy() if str(t.dtype) == "torch.bfloat16" else t.numpy()
    return out


# ---- resumability ------------------------------------------------------------------------------------
def shard_complete(manifest: Manifest, layout: RunLayout, paths: Sequence[Path], config_hash: str) -> bool:
    for p in paths:
        if not Path(p).exists():
            return False
        e = manifest.entries.get(os.path.relpath(p, layout.root))
        if e is None or e.config_hash != config_hash or e.sha256 != sha256_file(p):
            return False
    return True


def register(manifest: Manifest, layout: RunLayout, paths: Sequence[Path], producer: str, config_hash: str) -> list[str]:
    rels = []
    for p in paths:
        manifest.add(layout.root, p, producer, config_hash)
        rels.append(os.path.relpath(p, layout.root))
    manifest.save(layout.manifest)
    return rels
