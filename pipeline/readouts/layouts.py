"""Token layouts of the frozen samples, built by the generate stage's own construction.

`default_layouts_provider` loads the generation records, problems, and extractions of a run and calls
`pipeline.generate.capture.TransformersCapture.build_layout` for every sample, so the elicitation span
the adapter mask uses is the span capture used for p3 and the V2 log-odds (design 7.12). No second
definition of the span exists in this package.
"""

from __future__ import annotations

import json
from typing import Mapping, Sequence

import pyarrow.parquet as pq

from pipeline.contracts.interfaces import TeacherForcedLayout
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.schemas import ExtractionResult, GenerationRecord, Problem


def load_generation_inputs(layout: RunLayout, model_key: str, benches: Sequence[str], gen_set: str = "frozen"
                           ) -> tuple[dict[str, GenerationRecord], dict[str, Problem], dict[str, ExtractionResult]]:
    recs: dict[str, GenerationRecord] = {}
    problems: dict[str, Problem] = {}
    exts: dict[str, ExtractionResult] = {}
    for b in benches:
        s = 0
        while layout.generation_shard(model_key, b, gen_set, s).exists():
            for r in pq.read_table(layout.generation_shard(model_key, b, gen_set, s)).to_pylist():
                rec = GenerationRecord.from_dict(r)
                recs[rec.sample_uid] = rec
            s += 1
        if layout.problems(b).exists():
            for line in layout.problems(b).read_text().splitlines():
                if line.strip():
                    p = Problem.from_dict(json.loads(line))
                    problems[p.problem_id] = p
        if layout.extractions(model_key, b, gen_set).exists():
            for r in pq.read_table(layout.extractions(model_key, b, gen_set)).to_pylist():
                exts[r["sample_uid"]] = ExtractionResult(**r)
    return recs, problems, exts


def build_layouts(capture, sample_uids: Sequence[str], records: Mapping[str, GenerationRecord],
                  problems: Mapping[str, Problem], extractions: Mapping[str, ExtractionResult]) -> list[TeacherForcedLayout]:
    out = []
    for u in sample_uids:
        rec = records[u]
        out.append(capture.build_layout(rec, problems[rec.problem_id], extractions.get(u)))
    return out


def default_layouts_provider(cfg, layout: RunLayout, model_key: str, benches: Sequence[str],
                             sample_uids: Sequence[str], tokenizer, model) -> list[TeacherForcedLayout]:
    from pipeline.generate.capture import TransformersCapture
    from pipeline.generate.requests import model_spec
    spec = model_spec(model_key)
    cap = TransformersCapture(model, tokenizer, chat=spec.chat, padding_side=cfg.extra.get("padding_side", "left"))
    recs, problems, exts = load_generation_inputs(layout, model_key, benches)
    missing = [u for u in sample_uids if u not in recs]
    if missing:
        raise RuntimeError(f"{len(missing)} samples have no generation record (first: {missing[0]})")
    return build_layouts(cap, sample_uids, recs, problems, exts)
