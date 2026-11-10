"""Interfaces each module implements. Module builders code against these signatures.

Ownership (wave 8):
    pipeline.data      B1   problems, suites, MBPP+ patch, LiveCodeBench by ID, agreement inputs, folds
    pipeline.execute   B2   extraction, sandboxed execution, cache, labels, reference check
    pipeline.generate  B3   backends (vLLM, transformers, mock), prompts, seeded sampling, capture, shards
    pipeline.readouts  B4   every readout of section 7, cross-fitting, isotonic, masked LoRA, R-Tuning
    analysis           B5   metrics, bootstrap, refit widening, Shapley, decisions, k rule, reconciliation
    ops                B6   pod bootstrap, job runner, sync, cost guard, RunPod API, dry run

Every stage entry point has the signature of `Stage.run` and is listed in STAGES. The ops runner and
the integration test call stages only through STAGES. A contract change after Part B starts is made
by the orchestrator only and logged in pipeline/contracts/CHANGELOG.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol, Sequence, runtime_checkable

import numpy as np

from .layout import RunLayout
from .manifest import Manifest
from .schemas import (
    BootstrapDraws, CaptureRecord, DecisionResult, ExecutionResult, ExtractionResult, FitRecord,
    FoldPlan, GenerationRecord, GenerationRequest, Interval, KRuleResult, Label, NearDuplicateGroup,
    Problem, ReadoutScore, ReconciliationCheck, ReferenceCheck, ScoredSet, ShapleyResult, TestSuite,
)


# ---------------------------------------------------------------------------------------------------
# Run configuration and stages
# ---------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class RunConfig:
    run_id: str
    models: tuple[str, ...]                 # keys of constants.MODELS, or "SMOKE" / "MOCK"
    benchmarks: tuple[str, ...]             # subset of constants.BENCHMARKS
    k: int = 10
    fold_seeds: tuple[int, ...] = (0,)
    backend: str = "vllm"                   # "vllm" | "transformers" | "mock"
    device: str = "cuda"                    # "cuda" | "cpu"
    sandbox: str = "container"              # "container" | "bwrap" | "trusted-only"
    execute_untrusted: bool = True          # False on the operator Mac: generated code is never run
    problem_limit: int | None = None        # smoke test: first N problems by ID
    problem_ids: tuple[str, ...] = ()       # explicit subset (overrides problem_limit)
    stages: tuple[str, ...] = ("data", "generate", "execute", "capture", "readouts", "analysis")
    generation_only_models: tuple[str, ...] = ()  # pilot mixed-count: generate + execute only (section 13)
    readouts: tuple[str, ...] = ()          # empty = all readouts applicable to the population
    lora_max_steps: int | None = None       # smoke only: cap on LoRA steps; None = the design's schedule
    seal_gamma: bool = False                # pilot: write, hash, and do not open Gamma cells (section 13)
    hf_cache: str = ".hf-cache"
    bench_cache: str = "docs/s7/parts/bench-A2/cache"
    shard_size: int = 512                   # samples per generation / capture shard
    extra: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = dict(self.__dict__)
        d["extra"] = dict(self.extra)
        return d

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "RunConfig":
        tup = {"models", "benchmarks", "fold_seeds", "problem_ids", "stages", "generation_only_models", "readouts"}
        return cls(**{k: (tuple(v) if k in tup else v) for k, v in d.items()})


@dataclass
class StageReport:
    stage: str
    ok: bool
    outputs: list[str] = field(default_factory=list)   # paths relative to the run root, all in the manifest
    skipped: list[str] = field(default_factory=list)   # resumable shards already complete
    notes: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)  # operational counts only (rates, timings)


@runtime_checkable
class Stage(Protocol):
    def __call__(self, cfg: RunConfig, layout: RunLayout, manifest: Manifest, *, dry_run: bool = False) -> StageReport: ...


STAGES: dict[str, str] = {
    "data": "pipeline.data.stage:run",
    "generate": "pipeline.generate.stage:run_generate",
    "execute": "pipeline.execute.stage:run",
    "capture": "pipeline.generate.stage:run_capture",
    "readouts": "pipeline.readouts.stage:run",
    "analysis": "analysis.stage:run",
}


# ---------------------------------------------------------------------------------------------------
# B1 pipeline.data
# ---------------------------------------------------------------------------------------------------
class BenchmarkLoader(Protocol):
    def verify_pins(self) -> list[tuple[str, bool]]:
        """(file, sha256 matches) for every pinned file needed; raises if a needed file is missing."""

    def problems(self, benchmark: str) -> list[Problem]:
        """MBPP+: v0.2.0 with the pinned patch applied (Mbpp/459, 102, 559) and the 21 removed IDs
        absent. LiveCodeBench: release_v6 at the pinned commit, read through the fetch script."""

    def suites(self, problem: Problem) -> dict[str, TestSuite]:
        """HumanEval+/MBPP+: {"O", "E"}; LiveCodeBench: {"lcb_public", "lcb_label", "lcb_full"}."""

    def agreement_inputs(self, problem: Problem, suites: Mapping[str, TestSuite], seed: int) -> TestSuite:
        """suite_id "agree": TypedMutGen inputs (HumanEval/MBPP), contract-filtered, deduplicated
        against every label input after canonicalization, capped at 50; LiveCodeBench: the 20 percent
        private split from hashing.lcb_agreement_indices. Records removed counts in a side table."""


def near_duplicate_groups(problems: Sequence[Problem]) -> list[NearDuplicateGroup]: ...
def build_folds(problem_ids: Sequence[str], groups: Sequence[NearDuplicateGroup], fold_seed: int,
                population: str) -> FoldPlan: ...


# ---------------------------------------------------------------------------------------------------
# B2 pipeline.execute
# ---------------------------------------------------------------------------------------------------
def extract_code(sample_uid: str, completion_text: str, entry_point: str | None, truncated: bool) -> ExtractionResult: ...
def normalize_code(code: str) -> str:
    """ast.unparse of the parsed module, or the raw text if parsing fails (section 6)."""


class Executor(Protocol):
    name: str           # "container" | "bwrap" | "fixture"

    def preflight(self) -> None:
        """Prove isolation before any untrusted run: no network, read-only root, limits. Raises."""

    def run(self, code: str, problem: Problem, suite: TestSuite, *, trusted: bool = False,
            capture_outputs: bool = False) -> ExecutionResult:
        """Execute code against one suite. trusted=True is allowed only for reference solutions and
        hand-written fixtures; an executor configured with execute_untrusted=False raises on
        trusted=False."""


def reference_check(problems: Sequence[Problem], suites: Mapping[str, Mapping[str, TestSuite]],
                    executor: Executor) -> list[ReferenceCheck]: ...
def label_samples(extractions: Sequence[ExtractionResult], problems: Mapping[str, Problem],
                  suites: Mapping[str, Mapping[str, TestSuite]], executor: Executor,
                  cache: Any) -> list[Label]: ...


# ---------------------------------------------------------------------------------------------------
# B3 pipeline.generate
# ---------------------------------------------------------------------------------------------------
class GenerationBackend(Protocol):
    engine: str     # "vllm==0.33.0" | "transformers==5.20.2" | "mock"

    def generate(self, requests: Sequence[GenerationRequest], adapter_path: str | None = None) -> list[GenerationRecord]:
        """Seeded sampling at temperature 1.0, top-p 1.0, no top-k, stop at end of turn."""


@dataclass(frozen=True)
class TeacherForcedLayout:
    """Token layout of the single teacher-forced pass (section 5, 7.12):
    prompt_ids (rendered generation prompt, as used for generation) + completion_ids (frozen, as
    generated, including the end-of-turn token) + elicitation_ids (the V2 user turn from the first
    token of its header through the assistant header, i.e. the last prefix token before the answer).
    The adapter mask is 1 exactly on elicitation_ids (section 7.12)."""

    prompt_ids: tuple[int, ...]
    completion_ids: tuple[int, ...]
    elicitation_ids: tuple[int, ...]
    code_span: tuple[int, int]      # [start, end) within the full sequence; excludes fences, EOT, thought block

    @property
    def p1(self) -> int:
        return len(self.prompt_ids) - 1

    @property
    def elicitation_span(self) -> tuple[int, int]:
        s = len(self.prompt_ids) + len(self.completion_ids)
        return (s, s + len(self.elicitation_ids))

    @property
    def p3(self) -> int:
        return self.elicitation_span[1] - 1

    def mask(self) -> np.ndarray:
        n = self.elicitation_span[1]
        m = np.zeros(n, dtype=np.int8)
        a, b = self.elicitation_span
        m[a:b] = 1
        return m


class CaptureBackend(Protocol):
    def capture(self, records: Sequence[GenerationRecord], extractions: Mapping[str, ExtractionResult],
                problems: Mapping[str, Problem]) -> tuple[list[CaptureRecord], dict[str, np.ndarray]]:
        """One teacher-forced pass per sample: code-token log-probs, hidden states at the layers of
        LAYER_FRACTIONS (index floor(f * n_layers) into output_hidden_states, 0 = embeddings) at
        p1, p2, p3 and the code-token mean, float32 Yes/No log-odds at the answer position, and the
        greedy V1 decode from the cached prefix. Returns index rows and CAPTURE_ARRAYS."""


# ---------------------------------------------------------------------------------------------------
# B4 pipeline.readouts
# ---------------------------------------------------------------------------------------------------
@dataclass
class ReadoutData:
    """Everything a readout may read for one (model, population, generation set). Rows aligned."""

    sample_uids: list[str]
    problem_ids: list[str]
    labels: dict[str, np.ndarray]           # suite -> int8[n]
    capture: list[CaptureRecord] | None = None
    hidden: dict[str, np.ndarray] | None = None   # "hs_p1", "hs_p2", "hs_p3", "hs_mean_code": float32[n, L, D]
    code_texts: list[str | None] | None = None
    code_logprobs: list[np.ndarray] | None = None
    agreement_outputs: dict[str, tuple[str, ...] | None] | None = None   # sample_uid -> signature
    extraction_failed: np.ndarray | None = None   # bool[n]
    truncated: np.ndarray | None = None           # bool[n]


class SupervisedReadout(Protocol):
    name: str

    def crossfit(self, data: ReadoutData, plan: FoldPlan, label_suite: str, model_key: str,
                 population: str) -> tuple[list[ReadoutScore], list[FitRecord]]:
        """Fit on four folds, score the fifth, for every outer fold of plan. Every selection uses
        only the inner splits of the outer training set (section 7)."""


class UnsupervisedReadout(Protocol):
    name: str

    def score(self, data: ReadoutData, model_key: str, population: str) -> list[ReadoutScore]: ...


def crossfit_isotonic(scores: Sequence[ReadoutScore], data: ReadoutData, plan: FoldPlan, label_suite: str,
                      train_scores: Mapping[int, Sequence[ReadoutScore]] | None = None) -> list[ReadoutScore]:
    """Section 7.3. Returns iso:<name> rows: prob = rank_score = isotonic value, rank_tiebreak =
    pre-map rank_score. train_scores[outer_fold] are the inner-cross-fitted training-fold scores for
    S^T; for zero-shot readouts the training-fold scores are used directly. out_of_bounds = clip;
    single-class training set falls back to the training base rate."""


# ---------------------------------------------------------------------------------------------------
# B5 analysis (pure functions on arrays; no file IO except analysis.stage)
# ---------------------------------------------------------------------------------------------------
class AnalysisAPI(Protocol):
    """Names and signatures analysis/ exports (module: function)."""

    # analysis.metrics
    def auroc_pooled(self, s: ScoredSet, weights: np.ndarray | None = None) -> float | None: ...
    def within_problem_auroc(self, s: ScoredSet, weights: np.ndarray | None = None) -> float | None: ...  # W
    def within_problem_auroc_avg(self, s: ScoredSet, weights: np.ndarray | None = None) -> float | None: ...
    def auprc(self, s: ScoredSet, positive: int = 1, weights: np.ndarray | None = None) -> float | None: ...
    def brier(self, s: ScoredSet, weights: np.ndarray | None = None) -> float: ...
    def murphy(self, s: ScoredSet, n_bins: int = 15) -> dict[str, float]: ...
    def mixed_counts(self, s: ScoredSet) -> dict[str, int]: ...
    def tie_rate_within(self, s: ScoredSet) -> float | None: ...
    # analysis.calibration
    def ece_debiased_equal_mass(self, s: ScoredSet, n_bins: int = 15) -> float: ...
    def smooth_ece(self, s: ScoredSet) -> float: ...
    def ks_calibration_error(self, s: ScoredSet) -> float: ...
    def ece_equal_width(self, s: ScoredSet, n_bins: int) -> float: ...
    # analysis.bootstrap
    def draw(self, problem_ids: Sequence[str], b: int, seed: int) -> BootstrapDraws: ...
    def percentile_interval(self, point: float, replicates: np.ndarray, level: float) -> Interval: ...
    # analysis.refit / analysis.decisions
    def decide(self, r_bar: float, replicates: np.ndarray, per_model_seed_r: Mapping[str, Sequence[float]],
               delta: float) -> DecisionResult: ...
    # analysis.shapley
    def shapley(self, cells: Mapping[str, float]) -> ShapleyResult: ...
    # analysis.krule
    def k_rule(self, per_model_mixed: Mapping[str, int]) -> KRuleResult: ...
    # analysis.reconciliation
    def classify(self, kind: str, interval: tuple[float, float], direction: int = 1,
                 tie_width: float | None = None) -> str: ...
