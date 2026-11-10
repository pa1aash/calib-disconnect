"""Stage entry points: run_generate and run_capture (STAGES: pipeline.generate.stage:run_generate / :run_capture).

Configuration read from RunConfig:
    backend        "vllm" | "transformers" | "mock"
    models         keys of constants.MODELS, "SMOKE", or "MOCK"
    k, shard_size, device, hf_cache, problem_limit, problem_ids, generation_only_models
    extra["sample_indices"]   explicit sample indices instead of 1..k (for example 11..20 after the k rule)
    extra["fresh"]            list of {"model_key", "benchmark", "adapter_id", "adapter_path", "k_g",
                              optional "problem_ids"} for the generation-shift pass (design 5, 7.5)
    extra["batch_size"], extra["padding_side"]   capture batching
    extra["mock_p_correct"], extra["mock_garbage_share"]   MockBackend settings

Resumability (12.5): a shard whose files exist and whose manifest entries carry the same SHA-256 and
config hash is skipped. Every shard written is added to the manifest and the manifest is saved.
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Any, Sequence

import pyarrow.parquet as pq

from pipeline.contracts import constants as C
from pipeline.contracts.hashing import config_hash, sha256_file, sha256_text
from pipeline.contracts.interfaces import RunConfig, StageReport
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest
from pipeline.contracts.schemas import ExtractionResult, GenerationRecord, Problem

from .backends import MockBackend, TransformersBackend, VLLMBackend
from .capture import MockCapture, TransformersCapture
from .prompts import PromptSet, chat_template_sha256, load_prompts, supports_thinking_flag
from .requests import ModelSpec, build_fresh_requests, build_requests, model_spec
from .cards import load_tracked as load_tracked_cards
from .storage import (atomic_write, load_capture_shard, read_generation_shard, register, shard_complete,
                      write_capture_shard, write_generation_shard)
from .tokens import answer_token_variants, derive_turns

PRODUCER_GEN = "pipeline.generate.stage:run_generate"
PRODUCER_CAP = "pipeline.generate.stage:run_capture"
TIMING_SET = "timing"


# ---------------------------------------------------------------------------------------------------
# Problems and mock reference variants
# ---------------------------------------------------------------------------------------------------
def load_problems(layout: RunLayout, benchmark: str, cfg: RunConfig | None = None) -> list[Problem]:
    path = layout.problems(benchmark)
    probs = [Problem.from_dict(json.loads(line)) for line in path.read_text().splitlines() if line.strip()]
    if cfg is not None:
        if cfg.problem_ids:
            keep = set(cfg.problem_ids)
            probs = [p for p in probs if p.problem_id in keep]
        elif cfg.problem_limit is not None:
            probs = sorted(probs, key=lambda p: p.problem_id)[:cfg.problem_limit]
    return probs


_RETURN = re.compile(r"(?m)^(\s*)return\b.*$")


def reference_code(problem: Problem) -> str | None:
    """Full function source from the canonical solution (EvalPlus HumanEval solutions are bodies)."""
    cs = problem.canonical_solution
    if cs is None:
        return None
    if problem.entry_point and re.search(rf"(?m)^def\s+{re.escape(problem.entry_point)}\b", cs):
        return cs.rstrip("\n")
    return (problem.prompt + cs).rstrip("\n")


def mock_variants(problem: Problem, correct: str) -> list[str]:
    """Wrong variants built by hand-written mutation rules on reference code, never from a model:
    1. every return expression becomes None; 2. only the last return becomes None;
    3. the body is replaced by a stub that returns None; 4. a module-level raise (import-time failure)."""
    out: list[str] = []
    out.append(_RETURN.sub(lambda m: f"{m.group(1)}return None", correct))
    rets = list(_RETURN.finditer(correct))
    if rets:
        m = rets[-1]
        out.append(correct[:m.start()] + f"{m.group(1)}return None" + correct[m.end():])
    lines = correct.split("\n")
    start = next((i for i, ln in enumerate(lines) if problem.entry_point and re.match(rf"def\s+{re.escape(problem.entry_point)}\b", ln)), None)
    if start is not None:
        end = next((i for i in range(start, len(lines)) if lines[i].rstrip().endswith(":")), start)
        out.append("\n".join(lines[:end + 1] + ["    return None"]))
    out.append(correct + "\n\nraise RuntimeError('mock failure')")
    seen, uniq = {correct}, []
    for v in out:
        if v not in seen:
            seen.add(v)
            uniq.append(v)
    return uniq


def mock_mapping(problems: Sequence[Problem]) -> dict[str, tuple[str, list[str]]]:
    m = {}
    for p in problems:
        code = reference_code(p)
        if code is not None:
            m[p.problem_id] = (code, mock_variants(p, code))
    return m


# ---------------------------------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------------------------------
def load_hf(cfg: RunConfig, spec: ModelSpec):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(spec.model_id, revision=spec.revision, cache_dir=cfg.hf_cache)
    dtype = torch.float32 if cfg.device == "cpu" else torch.bfloat16
    model = AutoModelForCausalLM.from_pretrained(spec.model_id, revision=spec.revision, cache_dir=cfg.hf_cache, dtype=dtype)
    model.to(cfg.device).eval()
    return model, tok


def _write_json_merged(layout: RunLayout, manifest: Manifest, path: Path, key: str, value: Any, producer: str) -> None:
    data = json.loads(path.read_text()) if path.exists() else {}
    data[key] = value
    text = json.dumps(data, indent=1, sort_keys=True) + "\n"
    atomic_write(path, lambda tmp: tmp.write_text(text))
    manifest.add(layout.root, path, producer, sha256_text(text))
    manifest.save(layout.manifest)


def _metrics_add(m: dict[str, Any], name: str, n: int, tokens: int, seconds: float, **extra: Any) -> None:
    d = m.setdefault(name, {"samples": 0, "tokens": 0, "seconds": 0.0})
    d["samples"] += n
    d["tokens"] += tokens
    d["seconds"] += seconds
    d["tokens_per_second"] = d["tokens"] / d["seconds"] if d["seconds"] > 0 else None
    for k, v in extra.items():
        d[k] = d.get(k, 0) + v


# ---------------------------------------------------------------------------------------------------
# Generate
# ---------------------------------------------------------------------------------------------------
def _chunks(requests: list, shard_size: int) -> list[list]:
    """Shards within each block of K_DEFAULT sample indices, so adding samples 11..20 later leaves the
    shards of samples 1..10 (and their numbering) unchanged."""
    by_block: dict[int, list] = {}
    for r in requests:
        by_block.setdefault((r.sample_index - 1) // C.K_DEFAULT, []).append(r)
    out: list[list] = []
    for b in sorted(by_block):
        reqs = by_block[b]
        out.extend(reqs[i:i + shard_size] for i in range(0, len(reqs), shard_size))
    return out


def _gen_hash(spec: ModelSpec, benchmark: str, gen_set: str, shard_size: int, prompts: PromptSet, backend: str,
              reqs: Sequence) -> str:
    return config_hash({"stage": "generate", "model_id": spec.model_id, "revision": spec.revision,
                        "thinking": spec.thinking, "benchmark": benchmark, "generation_set": gen_set,
                        "shard_size": shard_size, "backend": backend, "prompts": dict(prompts.file_sha256),
                        "requests": sha256_text("\n".join(f"{r.problem_id}|{r.sample_index}|{r.seed}|{r.max_new_tokens}" for r in reqs))})


class _LazyGenBackend:
    def __init__(self, cfg: RunConfig, spec: ModelSpec, problems: Sequence[Problem], prompts: PromptSet, lora: bool):
        self.cfg, self.spec, self.problems, self.prompts, self.lora = cfg, spec, problems, prompts, lora
        self._b: Any = None
        self.tokenizer: Any = None

    def get(self):
        if self._b is None:
            cfg, spec = self.cfg, self.spec
            if cfg.backend == "mock":
                self._b = MockBackend(mock_mapping(self.problems), p_correct=cfg.extra.get("mock_p_correct", 0.5),
                                      garbage_share=cfg.extra.get("mock_garbage_share", 0.0), prompts=self.prompts)
            elif cfg.backend == "transformers":
                model, self.tokenizer = load_hf(cfg, spec)
                self._b = TransformersBackend(model, self.tokenizer, chat=spec.chat, prompts=self.prompts)
            elif cfg.backend == "vllm":
                self._b = VLLMBackend(spec.model_id, spec.revision, chat=spec.chat, hf_cache=cfg.hf_cache,
                                      prompts=self.prompts, enable_lora=self.lora)
                self.tokenizer = self._b.tokenizer
            else:
                raise ValueError(f"unknown backend {cfg.backend!r}")
        return self._b


def _run_sets(cfg: RunConfig, layout: RunLayout, manifest: Manifest, rep: StageReport, prompts: PromptSet, spec: ModelSpec,
              benchmark: str, problems: list[Problem], reqs: list, gen_set: str, backend: _LazyGenBackend,
              adapter_path: str | None, dry_run: bool, *, force: bool = False,
              collect: list | None = None) -> None:
    shards = _chunks(reqs, cfg.shard_size)
    n_done = 0
    for idx, chunk in enumerate(shards):
        path = layout.generation_shard(spec.key, benchmark, gen_set, idx)
        h = _gen_hash(spec, benchmark, gen_set, cfg.shard_size, prompts, cfg.backend, chunk)
        rel = os.path.relpath(path, layout.root)
        if not force and shard_complete(manifest, layout, [path], h):
            rep.skipped.append(rel)
            continue
        if dry_run:
            rep.notes.append(f"would write {rel} ({len(chunk)} samples)")
            continue
        t0 = time.time()
        recs = backend.get().generate(chunk, adapter_path=adapter_path)
        dt = time.time() - t0
        write_generation_shard(path, recs)
        if collect is not None:
            collect.extend(recs)
        rep.outputs.extend(register(manifest, layout, [path], PRODUCER_GEN, h))
        _metrics_add(rep.metrics, f"{spec.key}/{benchmark}/{gen_set}", len(recs),
                     sum(len(r.completion_token_ids) for r in recs), dt,
                     truncated=sum(r.truncated for r in recs))
        n_done += 1
    rep.metrics.setdefault("shards", {})[f"{spec.key}/{benchmark}/{gen_set}"] = {"total": len(shards), "written": n_done}


def run_generate(cfg: RunConfig, layout: RunLayout, manifest: Manifest, *, dry_run: bool = False) -> StageReport:
    rep = StageReport(stage="generate", ok=True)
    prompts = load_prompts()
    if cfg.extra.get("timing_only"):
        return _run_generate_timing(cfg, layout, manifest, rep, prompts, dry_run)
    fresh = list(cfg.extra.get("fresh", []))
    indices = cfg.extra.get("sample_indices")
    for key in cfg.models:
        spec = model_spec(key)
        backend: _LazyGenBackend | None = None
        if spec.is_base and any(b == "lcb_v6" for b in cfg.benchmarks):
            rep.notes.append(f"{key}: base models run on the label-validity population only; lcb_v6 skipped")
        for bench in cfg.benchmarks:
            if spec.is_base and bench == "lcb_v6":
                continue
            problems = load_problems(layout, bench, cfg)
            lora = any(f["model_key"] == key and f["benchmark"] == bench for f in fresh)
            backend = _LazyGenBackend(cfg, spec, problems, prompts, lora)
            reqs = build_requests(key, problems, cfg.k, "frozen", indices, prompts=prompts)
            _run_sets(cfg, layout, manifest, rep, prompts, spec, bench, problems, reqs, "frozen", backend, None, dry_run)
            for f in fresh:
                if f["model_key"] != key or f["benchmark"] != bench:
                    continue
                sub = problems
                if f.get("problem_ids"):
                    keep = set(f["problem_ids"])
                    sub = [p for p in problems if p.problem_id in keep]
                freqs = build_fresh_requests(key, sub, int(f.get("k_g", cfg.k)), f["adapter_id"], prompts=prompts)
                _run_sets(cfg, layout, manifest, rep, prompts, spec, bench, sub, freqs, f"fresh:{f['adapter_id']}", backend,
                          f["adapter_path"], dry_run)
        if not dry_run and backend is not None:
            _record_prompts(layout, manifest, prompts, spec, backend)
    if not dry_run:
        _write_json_merged(layout, manifest, layout.prompts, "_prompts", prompts.describe(), PRODUCER_GEN)
        _write_json_merged(layout, manifest, layout.prompts, "card_recommendations_not_used",
                           {k: v for k, v in load_tracked_cards()["models"].items() if k in cfg.models or not cfg.models},
                           PRODUCER_GEN)
        tot_tok = sum(v["tokens"] for k, v in rep.metrics.items() if isinstance(v, dict) and "tokens" in v)
        tot_s = sum(v["seconds"] for k, v in rep.metrics.items() if isinstance(v, dict) and "seconds" in v)
        rep.metrics["total"] = {"tokens": tot_tok, "seconds": tot_s, "tokens_per_second": tot_tok / tot_s if tot_s else None}
    return rep


def _record_prompts(layout: RunLayout, manifest: Manifest, prompts: PromptSet, spec: ModelSpec, backend: _LazyGenBackend) -> None:
    tok = backend.tokenizer
    if tok is None:
        return
    info = {"model_id": spec.model_id, "revision": spec.revision, "chat": spec.chat, "thinking": spec.thinking,
            "chat_template_sha256": chat_template_sha256(tok), "supports_enable_thinking": supports_thinking_flag(tok)}
    _write_json_merged(layout, manifest, layout.prompts, f"model:{spec.key}", info, PRODUCER_GEN)


# ---------------------------------------------------------------------------------------------------
# Capture
# ---------------------------------------------------------------------------------------------------
def read_extractions(path: Path) -> dict[str, ExtractionResult]:
    if not path.exists():
        return {}
    return {r["sample_uid"]: ExtractionResult(sample_uid=r["sample_uid"], code=r.get("code"), method=r.get("method"),
                                              failure=r.get("failure")) for r in pq.read_table(path).to_pylist()}


def _gen_shards(layout: RunLayout, key: str, bench: str) -> list[Path]:
    base = layout.root / "generations" / key / bench
    return sorted(p for p in base.glob("*/shard-*.parquet") if p.parent.name != TIMING_SET) if base.exists() else []


def run_capture(cfg: RunConfig, layout: RunLayout, manifest: Manifest, *, dry_run: bool = False) -> StageReport:
    rep = StageReport(stage="capture", ok=True)
    prompts = load_prompts()
    if cfg.extra.get("timing_only"):
        return _run_capture_timing(cfg, layout, rep, prompts, dry_run)
    for key in cfg.models:
        if key in cfg.generation_only_models:
            rep.notes.append(f"{key}: generation only; capture skipped")
            continue
        spec = model_spec(key)
        cap: Any = None
        for bench in cfg.benchmarks:
            shards = _gen_shards(layout, key, bench)
            if not shards:
                continue
            problems = {p.problem_id: p for p in load_problems(layout, bench)}
            for gpath in shards:
                idx = int(gpath.stem.split("-")[1])
                recs = read_generation_shard(gpath)
                if not recs:
                    continue
                gen_set = recs[0].generation_set
                spath = layout.capture_shard(key, bench, gen_set, idx)
                ipath = layout.capture_index(key, bench, gen_set, idx)
                epath = layout.extractions(key, bench, gen_set)
                h = config_hash({"stage": "capture", "generation_shard": sha256_file(gpath),
                                 "extractions": sha256_file(epath) if epath.exists() else None,
                                 "model_id": spec.model_id, "revision": spec.revision, "backend": cfg.backend,
                                 "prompts": dict(prompts.file_sha256), "layers": list(C.LAYER_FRACTIONS)})
                rel = os.path.relpath(spath, layout.root)
                if shard_complete(manifest, layout, [spath, ipath], h):
                    rep.skipped.append(rel)
                    continue
                if dry_run:
                    rep.notes.append(f"would write {rel} ({len(recs)} samples)")
                    continue
                if cap is None:
                    cap = _make_capture(cfg, layout, manifest, spec, problems, prompts)
                t0 = time.time()
                crecs, arrays = cap.capture(recs, read_extractions(epath), problems)
                dt = time.time() - t0
                fixed = write_capture_shard(spath, ipath, crecs, arrays, rel)
                rep.outputs.extend(register(manifest, layout, [spath, ipath], PRODUCER_CAP, h))
                ntok = int(sum(c.elicitation_span[1] for c in fixed))
                _metrics_add(rep.metrics, f"{key}/{bench}/{gen_set}", len(fixed), ntok, dt,
                             v1_unparsed=sum(c.v1_value is None for c in fixed))
    return rep


def _make_capture(cfg: RunConfig, layout: RunLayout, manifest: Manifest | None, spec: ModelSpec, problems: dict[str, Problem],
                  prompts: PromptSet):
    if cfg.backend == "mock":
        mapping = mock_mapping(list(problems.values()))
        if manifest is not None:
            _write_json_merged(layout, manifest, layout.answer_tokens, spec.key, {"backend": "mock"}, PRODUCER_CAP)
            _write_json_merged(layout, manifest, layout.mask_spans, spec.key, {"backend": "mock"}, PRODUCER_CAP)
        return MockCapture(mapping, prompts=prompts)
    model, tok = load_hf(cfg, spec)
    cap = TransformersCapture(model, tok, prompts, chat=spec.chat, batch_size=int(cfg.extra.get("batch_size", 4)),
                              padding_side=cfg.extra.get("padding_side", "left"))
    if manifest is None:
        return cap
    _write_json_merged(layout, manifest, layout.answer_tokens, spec.key,
                       {"model_id": spec.model_id, "revision": spec.revision, **cap.answer_tokens}, PRODUCER_CAP)
    _write_json_merged(layout, manifest, layout.mask_spans, spec.key,
                       {"model_id": spec.model_id, "revision": spec.revision, **cap.spec.describe(tok)}, PRODUCER_CAP)
    return cap


# ---------------------------------------------------------------------------------------------------
# Timing-only jobs (design 13, throughput probes; G10)
# ---------------------------------------------------------------------------------------------------
def _write_timing(layout: RunLayout, key: str, part: str, value: dict[str, Any]) -> None:
    """logs/timing_<model>.json (not a run product: no manifest entry, no analyzable content)."""
    path = layout.logs / f"timing_{key}.json"
    data = json.loads(path.read_text()) if path.exists() else {"model_key": key}
    data[part] = value
    text = json.dumps(data, indent=1, sort_keys=True) + "\n"
    atomic_write(path, lambda tmp: tmp.write_text(text))


def thinking_tokens(rec: GenerationRecord, tokenizer: Any | None) -> int:
    """Tokens up to the end of the last thought block (0 when there is none). Without a tokenizer the
    mock convention of one token per character applies."""
    from .tokens import char_span_to_token_span, decode_ids, thought_end
    ids = list(rec.completion_token_ids)
    if tokenizer is None:
        return thought_end(rec.completion_text)
    end = thought_end(decode_ids(tokenizer, ids))
    span = char_span_to_token_span(tokenizer, ids, 0, end) if end else None
    return span[1] if span else 0


def _run_generate_timing(cfg, layout, manifest, rep, prompts, dry_run) -> StageReport:
    """Generate into the "timing" set only: no frozen path, no capture, no score. Timings go to the
    report and to logs/timing_<model>.json. Timing shards are always rewritten (never skipped)."""
    rep.notes.append("timing_only: generation set 'timing'")
    for key in cfg.models:
        spec = model_spec(key)
        per_bench: dict[str, Any] = {}
        for bench in cfg.benchmarks:
            if spec.is_base and bench == "lcb_v6":
                continue
            problems = load_problems(layout, bench, cfg)
            backend = _LazyGenBackend(cfg, spec, problems, prompts, False)
            reqs = build_requests(key, problems, cfg.k, TIMING_SET, cfg.extra.get("sample_indices"), prompts=prompts)
            recs: list[GenerationRecord] = []
            _run_sets(cfg, layout, manifest, rep, prompts, spec, bench, problems, reqs, TIMING_SET, backend, None,
                      dry_run, force=True, collect=recs)
            if dry_run or not recs:
                continue
            m = rep.metrics[f"{key}/{bench}/{TIMING_SET}"]
            d = {"samples": m["samples"], "tokens": m["tokens"], "seconds": m["seconds"],
                 "tokens_per_second": m["tokens_per_second"], "mean_generated_tokens": m["tokens"] / m["samples"],
                 "truncated": m.get("truncated", 0)}
            if spec.thinking:
                d["mean_thinking_tokens"] = sum(thinking_tokens(r, backend.tokenizer) for r in recs) / len(recs)
            m.update({k: v for k, v in d.items() if k not in m})
            per_bench[bench] = d
        if per_bench and not dry_run:
            _write_timing(layout, key, "generate", {"benchmarks": per_bench, "thinking": spec.thinking})
    return rep


def _run_capture_timing(cfg, layout, rep, prompts, dry_run) -> StageReport:
    """Run the capture forward passes over the timing set and discard every array: no hidden state,
    log-prob, or readout is written. generation_only_models does not apply to timing jobs."""
    rep.notes.append("timing_only: capture over the 'timing' set; nothing is stored")
    for key in cfg.models:
        spec = model_spec(key)
        per_bench: dict[str, Any] = {}
        cap: Any = None
        for bench in cfg.benchmarks:
            base = layout.root / "generations" / key / bench / TIMING_SET
            shards = sorted(base.glob("shard-*.parquet")) if base.exists() else []
            if not shards:
                rep.notes.append(f"{key}/{bench}: no timing generations to capture")
                continue
            if dry_run:
                rep.notes.append(f"would time capture over {len(shards)} timing shards of {key}/{bench}")
                continue
            problems = {p.problem_id: p for p in load_problems(layout, bench)}
            if cap is None:
                cap = _make_capture(cfg, layout, None, spec, problems, prompts)
            n = ntok = 0
            secs = 0.0
            for g in shards:
                recs = read_generation_shard(g)
                t0 = time.time()
                crecs, _ = cap.capture(recs, {}, problems)
                secs += time.time() - t0
                n += len(crecs)
                ntok += int(sum(c.elicitation_span[1] for c in crecs))
            d = {"samples": n, "tokens": ntok, "seconds": secs, "tokens_per_second": ntok / secs if secs else None}
            rep.metrics[f"{key}/{bench}/{TIMING_SET}"] = d
            per_bench[bench] = d
        if per_bench:
            _write_timing(layout, key, "capture", {"benchmarks": per_bench})
    return rep
