"""Seeded generation requests (design section 5).

Seeds: hashing.sample_seed(model_id, revision, benchmark, problem_id, j) with j 1-based. The k rule
(samples 11..20 added later) holds because a seed depends only on its own sample index; the request
order places samples in blocks of K_DEFAULT so that shard numbering of samples 1..10 does not change
when 11..20 are added (see request_blocks).

Fresh samples for the generation-shift term (sections 1.5 and 7.5) use the benchmark field
f"{benchmark}#fresh:{adapter_id}" inside the seed hash, so they never reuse a frozen seed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from pipeline.contracts import constants as C
from pipeline.contracts.hashing import sample_seed
from pipeline.contracts.schemas import GenerationRequest, Problem

from .prompts import PromptSet, load_prompts

MOCK_MODEL = ("mock/model", "mock-revision-0")
BASE_ROLES = ("base", "coder_base")


@dataclass(frozen=True)
class ModelSpec:
    key: str
    model_id: str
    revision: str
    role: str
    thinking: bool

    @property
    def is_base(self) -> bool:
        return self.role in BASE_ROLES

    @property
    def chat(self) -> bool:
        return not self.is_base


def model_spec(model_key: str) -> ModelSpec:
    if model_key == "SMOKE":
        mid, rev = C.SMOKE_MODEL
        return ModelSpec("SMOKE", mid, rev, "smoke", False)
    if model_key == "MOCK":
        return ModelSpec("MOCK", MOCK_MODEL[0], MOCK_MODEL[1], "mock", False)
    if model_key not in C.MODELS:
        raise KeyError(f"unknown model key {model_key!r}")
    mid, rev, role, thinking = C.MODELS[model_key]
    return ModelSpec(model_key, mid, rev, role, thinking)


def max_new_tokens_for(thinking: bool) -> int:
    return C.MAX_NEW_TOKENS_REASONING if thinking else C.MAX_NEW_TOKENS


def request_blocks(sample_indices: Sequence[int]) -> list[int]:
    """Block number of each sample index: (j - 1) // K_DEFAULT. Blocks keep shard order stable."""
    return [(j - 1) // C.K_DEFAULT for j in sample_indices]


def _build(spec: ModelSpec, problems: Sequence[Problem], indices: Sequence[int], generation_set: str,
           seed_benchmark_suffix: str, prompts: PromptSet) -> list[GenerationRequest]:
    if any(j < 1 for j in indices):
        raise ValueError("sample indices are 1-based")
    reqs: list[GenerationRequest] = []
    # Order: block of K_DEFAULT samples, then problem order as given, then sample index.
    for block in sorted({(j - 1) // C.K_DEFAULT for j in indices}):
        block_idx = [j for j in indices if (j - 1) // C.K_DEFAULT == block]
        for p in problems:
            text = prompts.generation_prompt_text(p, base=spec.is_base)
            for j in sorted(block_idx):
                reqs.append(GenerationRequest(
                    model_key=spec.key, model_id=spec.model_id, revision=spec.revision,
                    benchmark=p.benchmark, problem_id=p.problem_id, sample_index=j,
                    seed=sample_seed(spec.model_id, spec.revision, p.benchmark + seed_benchmark_suffix,
                                     p.problem_id, j),
                    prompt_text=text, max_new_tokens=max_new_tokens_for(spec.thinking),
                    thinking=spec.thinking, generation_set=generation_set))
    return reqs


def build_requests(model_key: str, problems: Sequence[Problem], k: int, generation_set: str = "frozen",
                   sample_indices: Iterable[int] | None = None, *, prompts: PromptSet | None = None
                   ) -> list[GenerationRequest]:
    """Requests for samples j = 1..k (or the explicit sample_indices, for example 11..20)."""
    spec = model_spec(model_key)
    idx = list(sample_indices) if sample_indices is not None else list(range(1, k + 1))
    return _build(spec, problems, idx, generation_set, "", prompts or load_prompts())


def build_fresh_requests(model_key: str, problems: Sequence[Problem], k_g: int, adapter_id: str, *,
                         prompts: PromptSet | None = None) -> list[GenerationRequest]:
    """k_g fresh samples per problem for adapter_id (reading A). Same prompts as the frozen set; seeds
    from the benchmark field f"{benchmark}#fresh:{adapter_id}"."""
    spec = model_spec(model_key)
    return _build(spec, problems, list(range(1, k_g + 1)), f"fresh:{adapter_id}", f"#fresh:{adapter_id}",
                  prompts or load_prompts())
