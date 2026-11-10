import pytest

from pipeline.contracts import constants as C
from pipeline.contracts.hashing import sample_seed
from pipeline.generate import requests as R

import gen_tinylm as T


def _probs(n=3):
    return [T.problem(f"HumanEval/{i}") for i in range(n)]


def test_seeds_follow_the_design_rule(prompts):
    reqs = R.build_requests("P1", _probs(), 3, prompts=prompts)
    mid, rev = C.MODELS["P1"][:2]
    assert len(reqs) == 9
    for r in reqs:
        assert r.seed == sample_seed(mid, rev, "humaneval_plus", r.problem_id, r.sample_index)
        assert 1 <= r.sample_index <= 3 and r.max_new_tokens == 1024 and not r.thinking
        assert r.generation_set == "frozen" and r.model_id == mid and r.revision == rev
    assert len({r.seed for r in reqs}) == 9


def test_k_extension_leaves_samples_1_to_10_unchanged(prompts):
    ps = _probs(4)
    r10 = R.build_requests("P1", ps, 10, prompts=prompts)
    r20 = R.build_requests("P1", ps, 20, prompts=prompts)
    assert r20[:len(r10)] == r10                                   # same order, same seeds, same prompts
    late = R.build_requests("P1", ps, 20, sample_indices=range(11, 21), prompts=prompts)
    assert late == r20[len(r10):]
    assert {r.sample_index for r in late} == set(range(11, 21))


def test_thinking_and_base_and_special_models(prompts):
    s1 = R.build_requests("S1", _probs(1), 1, prompts=prompts)[0]
    assert s1.thinking and s1.max_new_tokens == C.MAX_NEW_TOKENS_REASONING == 16_384
    b1 = R.build_requests("B1", _probs(1), 1, prompts=prompts)[0]
    assert b1.prompt_text == T.problem("HumanEval/0").prompt and not R.model_spec("B1").chat
    smoke = R.build_requests("SMOKE", _probs(1), 1, prompts=prompts)[0]
    assert (smoke.model_id, smoke.revision) == C.SMOKE_MODEL and smoke.prompt_text.startswith("Solve the following")
    assert R.model_spec("MOCK").model_id == R.MOCK_MODEL[0]
    with pytest.raises(KeyError):
        R.model_spec("nope")
    with pytest.raises(ValueError):
        R.build_requests("P1", _probs(1), 1, sample_indices=[0], prompts=prompts)


def test_fresh_seeds_never_reuse_frozen_seeds(prompts):
    ps = _probs(3)
    frozen = R.build_requests("P3", ps, 4, prompts=prompts)
    fresh = R.build_fresh_requests("P3", ps, 4, "ad1", prompts=prompts)
    fresh2 = R.build_fresh_requests("P3", ps, 4, "ad2", prompts=prompts)
    assert {r.seed for r in frozen}.isdisjoint({r.seed for r in fresh})
    assert {r.seed for r in fresh}.isdisjoint({r.seed for r in fresh2})
    mid, rev = C.MODELS["P3"][:2]
    for r in fresh:
        assert r.generation_set == "fresh:ad1" and r.benchmark == "humaneval_plus"
        assert r.seed == sample_seed(mid, rev, "humaneval_plus#fresh:ad1", r.problem_id, r.sample_index)
        assert r.prompt_text == next(f for f in frozen if f.problem_id == r.problem_id).prompt_text
