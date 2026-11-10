"""Typed data schemas for every object that crosses a module boundary.

Records are frozen dataclasses with to_dict / from_dict for JSON lines. Tabular stores (parquet)
use the column lists in TABLE_COLUMNS; a module that writes a table writes exactly those columns.
Section references are to docs/s7/PIPELINE_DESIGN_FROZEN.md.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Any, Literal, Mapping, Sequence

import numpy as np

# ---------------------------------------------------------------------------------------------------
# Vocabularies
# ---------------------------------------------------------------------------------------------------
Benchmark = Literal["humaneval_plus", "mbpp_plus", "lcb_v6"]
Population = Literal["label_validity", "lcb"]
# Label suites. HumanEval+/MBPP+: "O" original (EvalPlus base inputs), "E" EvalPlus (base + plus).
# LiveCodeBench: "lcb_label" (public + the 80 percent of private tests not held out), "lcb_public"
# (public example tests only, the label-validity analog), "lcb_full" (official full suite,
# labeling sensitivity only). Agreement input sets are "agree" (never a label suite).
SuiteId = Literal["O", "E", "lcb_label", "lcb_public", "lcb_full", "agree"]
LABEL_SUITES_LV: tuple[str, ...] = ("O", "E")
LABEL_SUITES_LCB: tuple[str, ...] = ("lcb_public", "lcb_label", "lcb_full")
ExtractionFailure = Literal["no_block", "syntax_error", "missing_entry_point", "empty_output", "truncated"]
ExecFailure = Literal["wrong_output", "exception", "timeout", "memory", "killed", "program_cap", "sandbox_error"]
Decision = Literal["D1", "D2", "D3", "inconclusive"]
ReconOutcome = Literal["consistent", "not_consistent", "undetermined"]
Toggle = Literal["r", "t", "d", "l"]
TOGGLES: tuple[str, ...] = ("r", "t", "d", "l")

# Readout names (section 7). "iso:<name>" is the isotonic-recalibrated version of <name> (7.3).
READOUTS: tuple[str, ...] = (
    "P",          # selected probe from the family (7.1)
    "P2", "P3", "Pmulti",  # probe family members, reported separately (7.1)
    "P2_single_split",     # probe selected on the first inner split only (7.4 sensitivity)
    "MLP",        # MLP probe sensitivity (7.11)
    "SZ_V1", "SZ_V2",      # zero-shot stated readouts (7.2)
    "ST",         # trained stated readout, masked LoRA, V2 (7.4)
    "ST_r1", "ST_r4", "ST_r16", "ST_head",  # capacity ladder and LoRA plus linear head (7.11)
    "SR",         # [2610.31820]-style readout, full adapter (7.5)
    "TL_geo", "TL_min", "TL_sum",  # token-likelihood variants (7.6); TL_geo is also Ribeiro Intrinsic
    "AGREE",      # sampling agreement on disjoint inputs (7.7)
    "AST",        # alpha-renamed AST cluster share (7.8)
    "PROMPT",     # prompt-only probe (7.9)
    "CODETEXT",   # code-text-only classifier (7.10)
    "LAT",        # [Ribeiro] LAT direction (2.2)
)
SUPERVISED_READOUTS = frozenset({"P", "P2", "P3", "Pmulti", "P2_single_split", "MLP", "ST", "ST_r1",
                                 "ST_r4", "ST_r16", "ST_head", "SR", "PROMPT", "CODETEXT", "LAT"})


def iso(name: str) -> str:
    return f"iso:{name}"


class _Record:
    """Mixin: dict round-trip for frozen dataclasses."""

    def to_dict(self) -> dict[str, Any]:
        out = {}
        for f in dataclasses.fields(self):  # type: ignore[arg-type]
            v = getattr(self, f.name)
            if isinstance(v, tuple):
                v = list(v)
            out[f.name] = v
        return out

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]):
        names = {f.name: f for f in dataclasses.fields(cls)}  # type: ignore[arg-type]
        kwargs = {}
        for k, v in d.items():
            if k not in names:
                raise KeyError(f"{cls.__name__}: unknown field {k}")
            if isinstance(v, list) and "tuple" in str(names[k].type):
                v = tuple(tuple(x) if isinstance(x, list) else x for x in v)
            kwargs[k] = v
        return cls(**kwargs)


# ---------------------------------------------------------------------------------------------------
# Problems, suites, folds (pipeline.data)
# ---------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Problem(_Record):
    problem_id: str                 # "HumanEval/0", "Mbpp/2", "lcb/<question_id>"
    benchmark: str                  # Benchmark
    prompt: str                     # payload for the generation prompt (signature + docstring, or statement)
    entry_point: str | None         # function name; None for stdin LiveCodeBench problems
    canonical_solution: str | None  # None for LiveCodeBench (section 6)
    io_kind: str                    # "function" | "stdin"
    release_date: str | None        # ISO day; LiveCodeBench contest_date only
    starter_code: str | None = None # LiveCodeBench functional problems
    source_sha256: str = ""         # SHA-256 of the pinned file it was read from
    patched: bool = False           # MBPP+ ground-truth patch applied (Mbpp/459, 102, 559)


@dataclass(frozen=True)
class TestSuite(_Record):
    __test__ = False                # not a pytest class
    problem_id: str
    suite_id: str                   # SuiteId
    inputs: tuple                   # tuple of argument tuples (function) or stdin strings
    expected: tuple | None          # expected outputs; None when recomputed from the reference at run time
    atol: float = 0.0               # EvalPlus absolute tolerance where defined
    time_limit_rule: str = ""       # textual rule recorded in the cache key (section 6)
    input_set_sha256: str = ""      # SHA-256 of the canonical JSON of inputs


@dataclass(frozen=True)
class NearDuplicateGroup(_Record):
    group_key: str                  # smallest problem ID in the group (Python string order)
    members: tuple[str, ...]
    reasons: tuple[str, ...]        # "ast_identical" | "jaccard>=0.8" per linking edge


@dataclass(frozen=True)
class FoldPlan(_Record):
    """Problem-grouped folds for one population and one fold seed (section 7)."""

    fold_seed: int
    population: str
    n_folds: int
    assignment: Mapping[str, int]   # problem_id -> fold in 0..n_folds-1
    groups: tuple[NearDuplicateGroup, ...] = ()

    def problems_in(self, folds: Sequence[int]) -> list[str]:
        s = set(folds)
        return sorted(p for p, f in self.assignment.items() if f in s)

    def outer_train(self, outer_fold: int) -> list[str]:
        return self.problems_in([f for f in range(self.n_folds) if f != outer_fold])

    def outer_test(self, outer_fold: int) -> list[str]:
        return self.problems_in([outer_fold])

    def inner_splits(self, outer_fold: int) -> list[tuple[list[str], list[str]]]:
        """Inner 4-fold problem-grouped CV: each of the four training folds in turn is the inner
        validation fold, in ascending order of outer fold index. Element 0 is "the first inner split"
        used for LoRA recipe selection (section 7.4)."""
        train_folds = [f for f in range(self.n_folds) if f != outer_fold]
        out = []
        for v in train_folds:
            out.append((self.problems_in([f for f in train_folds if f != v]), self.problems_in([v])))
        return out

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d["assignment"] = dict(sorted(self.assignment.items()))
        d["groups"] = [g.to_dict() for g in self.groups]
        return d

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "FoldPlan":
        return cls(fold_seed=d["fold_seed"], population=d["population"], n_folds=d["n_folds"],
                   assignment=dict(d["assignment"]),
                   groups=tuple(NearDuplicateGroup.from_dict(g) for g in d.get("groups", [])))


# ---------------------------------------------------------------------------------------------------
# Generation and capture (pipeline.generate)
# ---------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class GenerationRequest(_Record):
    model_key: str                  # "P1", ..., "SMOKE", "MOCK"
    model_id: str
    revision: str
    benchmark: str
    problem_id: str
    sample_index: int               # 1-based
    seed: int                       # hashing.sample_seed(...)
    prompt_text: str                # rendered user message (before the chat template)
    max_new_tokens: int
    thinking: bool
    generation_set: str = "frozen"  # "frozen" | "fresh:<adapter_id>"


@dataclass(frozen=True)
class GenerationRecord(_Record):
    sample_uid: str                 # see sample_uid()
    model_key: str
    model_id: str
    revision: str
    benchmark: str
    problem_id: str
    sample_index: int
    generation_set: str
    seed: int
    prompt_sha256: str              # SHA-256 of the frozen prompt template file used
    rendered_prompt_sha256: str     # SHA-256 of the chat-template-rendered prompt text
    completion_text: str
    completion_token_ids: tuple[int, ...]
    finish_reason: str              # "stop" | "length"
    truncated: bool                 # finish_reason == "length"
    engine: str                     # "vllm==0.33.0" | "transformers==5.20.2" | "mock"
    thinking: bool


def sample_uid(model_key: str, benchmark: str, problem_id: str, sample_index: int,
               generation_set: str = "frozen") -> str:
    return f"{model_key}|{generation_set}|{benchmark}|{problem_id}|{sample_index}"


@dataclass(frozen=True)
class HiddenStateRef(_Record):
    """Where a sample's captured states live (section 5): one row of a capture shard."""

    shard_file: str                 # path relative to the run root, a .safetensors file
    row: int
    layers: tuple[int, ...]         # decoder layer indices for LAYER_FRACTIONS, rounded down
    positions: tuple[str, ...] = ("p1", "p2", "p3", "mean_code")
    dtype: str = "bfloat16"


@dataclass(frozen=True)
class CaptureRecord(_Record):
    """Index row for the single teacher-forced pass of one sample (section 5)."""

    sample_uid: str
    hidden: HiddenStateRef
    n_code_tokens: int              # tokens of the code span used by 7.6 (fence and EOT excluded)
    code_token_span: tuple[int, int]  # [start, end) in the teacher-forced sequence
    p1: int                         # last prompt token before the code
    p2: int                         # last code token (or last generated token before EOT on failure)
    p3: int                         # last token of the V2 elicitation span (last prefix token before answer)
    elicitation_span: tuple[int, int]  # [start, end) adapter mask span (section 7.12)
    yes_no_logodds: float           # float32 log P(Yes) - log P(No) at the answer position (7.12)
    v1_text: str                    # greedy V1 decode (up to 8 tokens)
    v1_value: float | None          # parsed N / 100, clipped; None if unparsed (7.2)
    sum_logprob: float              # sum of code-token log-probs
    mean_logprob: float
    min_logprob: float


# Arrays in a capture shard (.safetensors), N samples, L = len(LAYER_FRACTIONS), D = hidden size:
CAPTURE_ARRAYS = {
    "hs_p1": "bfloat16[N, L, D]",
    "hs_p2": "bfloat16[N, L, D]",
    "hs_p3": "bfloat16[N, L, D]",
    "hs_mean_code": "bfloat16[N, L, D]",
    "yes_no_logodds": "float32[N]",
    "code_logprobs": "float32[sum of n_code_tokens]",  # concatenated
    "code_logprob_offsets": "int64[N + 1]",
}


# ---------------------------------------------------------------------------------------------------
# Extraction, execution, labels (pipeline.execute)
# ---------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class ExtractionResult(_Record):
    sample_uid: str
    code: str | None                # None on failure
    method: str | None              # "fenced" | "fallback_def" | None
    failure: str | None             # ExtractionFailure or None


@dataclass(frozen=True)
class ExecutionResult(_Record):
    cache_key: str
    problem_id: str
    suite_id: str
    passed: bool
    failure: str | None             # ExecFailure or None
    per_test: tuple[bool, ...]      # one entry per input, in suite order; may stop early on failure
    outputs: tuple[str, ...] | None # canonical repr per input; only for the "agree" input set (7.7)
    runtime_s: float
    evaluator: str                  # "evalplus==0.3.1" | "lcb@<commit>" | "fixture"
    sandbox: str                    # "container" | "rlimit-subprocess" | "fixture"


@dataclass(frozen=True)
class Label(_Record):
    sample_uid: str
    suite_id: str
    y: int                          # 1 pass, 0 fail
    source: str                     # "execution" | "extraction_failure"
    failure: str | None
    cache_key: str | None


@dataclass(frozen=True)
class ReferenceCheck(_Record):
    problem_id: str
    suite_id: str
    passed: bool
    failure: str | None
    excluded: bool                  # excluded from analyses that use this suite (section 6)


# ---------------------------------------------------------------------------------------------------
# Readouts (pipeline.readouts)
# ---------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class ReadoutScore(_Record):
    """One out-of-fold (or unsupervised) score for one sample.

    prob in [0, 1] is used for Brier and calibration. Ranking metrics sort by (rank_score,
    rank_tiebreak) lexicographically; rank_tiebreak is NaN when there is no tie-break. For Yes/No
    readouts rank_score is the float32 log-odds (7.12). For iso:<name>, prob = rank_score = the
    isotonic value and rank_tiebreak = the pre-map rank_score (section 1.2)."""

    sample_uid: str
    model_key: str
    population: str                 # Population
    readout: str                    # READOUTS or iso:<name>
    label_suite: str | None         # suite the readout was fit on; None for unsupervised readouts
    fold_seed: int | None
    fold: int | None                # outer fold holding the sample's problem
    prob: float
    rank_score: float
    rank_tiebreak: float
    missing: bool = False           # V1 unparsed (before imputation), AGREE with no inputs
    imputed: bool = False           # V1 median-imputed (7.2)
    generation_set: str = "frozen"
    flagged: bool = False           # K4 failed-training flag for the model


@dataclass(frozen=True)
class FitRecord(_Record):
    """What a supervised fit selected, written beside its scores (no test-fold information)."""

    model_key: str
    readout: str
    label_suite: str
    fold_seed: int
    outer_fold: int
    selected: Mapping[str, Any]     # e.g. {"member": "P2", "layer": 12, "C": 0.1} or {"lr": 1e-4, "steps": 60}
    inner_val_logloss: float
    base_rate_logloss: float
    retried: bool = False           # K4 retry used
    flagged: bool = False           # K4 failure after retry


# ---------------------------------------------------------------------------------------------------
# Statistics (analysis)
# ---------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class ScoredSet:
    """Arrays for one (model, population, label suite, readout) cell, aligned by sample.

    problem_index maps each sample to a row of the problem list used by the bootstrap."""

    problem_index: np.ndarray       # int64[n]
    y: np.ndarray                   # int8[n]
    rank_score: np.ndarray          # float64[n]
    rank_tiebreak: np.ndarray       # float64[n], NaN where absent
    prob: np.ndarray                # float64[n]


@dataclass(frozen=True)
class Interval(_Record):
    point: float
    lo: float
    hi: float
    level: float
    n_undefined: int = 0            # dropped replicates (section 9, V13a)
    unavailable: bool = False       # more than 1 percent undefined


@dataclass(frozen=True)
class MetricResult(_Record):
    metric: str                     # "auroc_pooled" | "W" | "W_avg" | "auprc_pass" | "auprc_fail" | "brier" | ...
    model_key: str
    population: str
    label_suite: str
    readout: str
    value: float | None             # None when undefined
    undefined_reason: str | None
    n_samples: int
    n_problems: int
    n_mixed: int
    extra: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BootstrapDraws:
    """Problem-clustered resamples: counts[b, i] = multiplicity of problem i in resample b."""

    seed: int
    problem_ids: tuple[str, ...]
    counts: np.ndarray              # uint16[B, n_problems]


@dataclass(frozen=True)
class ShapleyResult(_Record):
    players: tuple[str, ...]        # ("r", "t", "d", "l")
    cells: Mapping[str, float]      # key "rtdl" bit string, e.g. "0000" -> Gamma
    phi: Mapping[str, float]
    interactions: Mapping[str, float]       # "rt", "rd", ... Shapley interaction index, order 2
    seq_labels_first: Mapping[str, float]   # order (l, d, t, r)
    seq_readout_first: Mapping[str, float]  # order (r, t, d, l)
    g0: float
    residual: float                 # Gamma(1111) = R^(0) at fold seed 0
    efficiency_gap: float           # g0 + sum(phi) - residual (zero up to float error)


@dataclass(frozen=True)
class DecisionResult(_Record):
    delta: float
    r_bar: float
    h: float                        # bootstrap half-width of the seed-averaged statistic
    s_refit: float
    t_quantile: float
    unwidened: tuple[float, float]
    widened: tuple[float, float]
    decision: str                   # Decision
    conventional_positive: bool     # secondary: interval lower bound > 0
    conventional_negative: bool     # secondary: interval upper bound < 0
    per_model_sigma2: Mapping[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class KRuleResult(_Record):
    per_model_mixed: Mapping[str, int]
    m_bar: float
    t10: int
    k: int                          # 10 or 20
    t20: int
    m_bar_k20: float | None = None  # filled after k = 20 generation, reported only
    below_t20: bool | None = None


@dataclass(frozen=True)
class ReconciliationCheck(_Record):
    check_id: str
    paper: str                      # "ribeiro" | "campos" | "r2610"
    reading: str | None             # "A" | "B" for r2610
    model_key: str
    kind: str                       # "ordering" | "tie" | "above_value"
    direction: int                  # +1: first above second (ordering, above_value); 0 for tie
    tie_width: float | None
    value: float                    # paired difference (or value minus reference for above_value)
    interval: tuple[float, float]   # paired 95 percent interval
    outcome: str                    # ReconOutcome
    diagnostic_excluding_truncation: str | None = None


TABLE_COLUMNS: dict[str, tuple[str, ...]] = {
    "generations": tuple(f.name for f in dataclasses.fields(GenerationRecord)),
    "extractions": tuple(f.name for f in dataclasses.fields(ExtractionResult)),
    "labels": tuple(f.name for f in dataclasses.fields(Label)),
    "reference_checks": tuple(f.name for f in dataclasses.fields(ReferenceCheck)),
    "capture_index": ("sample_uid", "shard_file", "row", "layers", "n_code_tokens", "code_token_span",
                      "p1", "p2", "p3", "elicitation_span", "yes_no_logodds", "v1_text", "v1_value",
                      "sum_logprob", "mean_logprob", "min_logprob"),
    "scores": tuple(f.name for f in dataclasses.fields(ReadoutScore)),
    "fits": tuple(f.name for f in dataclasses.fields(FitRecord)),
}
