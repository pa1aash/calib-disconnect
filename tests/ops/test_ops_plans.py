import pytest

from ops.plans import STAGE_ORDER, available_plans, job_config, load_plan, model_repo, order_jobs
from pipeline.contracts import constants as C


def test_available_plans():
    assert {"smoke", "pilot", "pilot-mixed-only", "full"} <= set(available_plans())


def test_smoke_plan():
    p = load_plan("smoke")
    c = p.cfg
    assert c.models == ("SMOKE",) and c.benchmarks == ("humaneval_plus",) and c.problem_limit == 5 and c.k == 2
    assert (c.backend, c.device, c.sandbox, c.execute_untrusted) == ("transformers", "cpu", "trusted-only", False)
    assert len(p.jobs) == 6 and p.download_models() == ()
    assert [j.stage for j in order_jobs(p.jobs)] == ["data", "generate", "execute", "capture", "readouts", "analysis"]


def test_pilot_plan_counts_and_stage_restriction():
    p = load_plan("pilot")
    c = p.cfg
    assert len(p.jobs) == 39 and len({j.id for j in p.jobs}) == 39
    assert c.seal_gamma is True and c.k == 10 and c.generation_only_models == C.PRIMARY_MODELS
    assert set(c.benchmarks) == set(C.LABEL_VALIDITY_BENCHMARKS)
    normal = [j for j in p.jobs if j.kind == "normal"]
    t1 = {j.stage for j in normal if j.model_key == C.PILOT_MODEL}
    assert t1 == {"generate", "execute", "capture", "readouts"}                 # every stage for T1
    assert [j.stage for j in p.jobs if j.stage == "analysis"] == ["analysis"]
    for m in C.PRIMARY_MODELS:                                                   # P1..P6: data, generate, execute only
        mine = [j for j in normal if j.model_key == m]
        assert {j.stage for j in mine} == {"generate", "execute"}
        assert len(mine) == 2 * len(C.LABEL_VALIDITY_BENCHMARKS)
        assert all(j.gen_set == "frozen" for j in mine)
    assert {j.stage for j in p.jobs if j.model_key in C.PRIMARY_MODELS and j.kind == "normal"}.isdisjoint({"capture", "readouts"})
    assert [j.stage for j in p.jobs if j.stage == "data"] == ["data", "data"]


def test_pilot_timing_probes_are_timing_only():
    p = load_plan("pilot")
    t = [j for j in p.jobs if j.kind == "timing"]
    assert sorted((j.model_key, j.stage) for j in t) == [("P4", "capture"), ("P4", "readouts"), ("P6", "capture"),
                                                         ("P6", "readouts"), ("S1", "generate")]
    assert {m for m in C.THROUGHPUT_PROBE_MODELS} == {"P4", "P6", "S1"}
    for j in t:
        assert j.overrides["extra"]["timing_only"] is True and j.gen_set == "timing"
    lora = [j for j in t if j.stage == "readouts"]
    assert all(j.overrides["lora_max_steps"] == 200 and j.overrides["problem_limit"] == 50 for j in lora)
    think = [j for j in t if j.model_key == "S1"][0]
    assert think.overrides["problem_limit"] == 100 and think.overrides["k"] == 2
    assert all(j.id.startswith("timing.") for j in t)


def test_pilot_mixed_only():
    p = load_plan("pilot-mixed-only")
    assert {j.stage for j in p.jobs} == {"data", "generate", "execute"}
    assert len(p.jobs) == 2 + 6 * 2 * 2
    assert p.cfg.models == C.PRIMARY_MODELS and p.cfg.stages == ("data", "generate", "execute")


def test_full_is_a_stub_listing_jobs_only():
    p = load_plan("full")
    assert p.launchable is False and len(p.jobs) > 100
    assert set(p.download_models()) == set(C.MODELS)


def test_run_id_override_and_ids_stable():
    a, b = load_plan("pilot"), load_plan("pilot", run_id="pilot-b")
    assert b.cfg.run_id == "pilot-b" and [j.id for j in a.jobs] == [j.id for j in b.jobs]
    assert all("/" not in j.id and ":" not in j.id and " " not in j.id for j in a.jobs)


def test_models_resolve_to_pinned_revisions():
    for n in ("pilot", "pilot-mixed-only", "full"):
        for k in load_plan(n).download_models():
            repo, rev = model_repo(k)
            assert repo == C.MODELS[k][0] and rev == C.MODELS[k][1] and len(rev) == 40
    assert model_repo("SMOKE") == C.SMOKE_MODEL
    with pytest.raises(KeyError):
        model_repo("NOPE")


def test_order_puts_data_first_models_in_blocks_analysis_last():
    p = load_plan("pilot")
    rev = list(reversed(p.jobs))
    o = order_jobs(rev)
    assert [j.stage for j in o[:2]] == ["data", "data"] and o[-1].stage == "analysis"
    seen, last = [], None
    for j in o[2:-1]:
        if j.model_key != last:
            assert j.model_key not in seen                       # one contiguous block per model
            seen.append(j.model_key)
            last = j.model_key
    rank = {s: i for i, s in enumerate(STAGE_ORDER)}
    t1 = [j for j in o if j.model_key == "T1"]
    assert [rank[j.stage] for j in t1] == sorted(rank[j.stage] for j in t1)
    p4 = [j.kind for j in o if j.model_key == "P4"]
    assert p4 == sorted(p4, key=lambda k: k == "timing")


def test_job_config_restricts_one_model_one_stage():
    p = load_plan("pilot")
    by = {j.id: j for j in p.jobs}
    c = job_config(p.cfg, by["generate.P1.mbpp_plus.frozen"])
    assert c.models == ("P1",) and c.benchmarks == ("mbpp_plus",) and c.stages == ("generate",) and c.seal_gamma
    assert c.extra["job_id"] == "generate.P1.mbpp_plus.frozen"
    r = job_config(p.cfg, by["readouts.T1.label_validity.frozen"])
    assert r.benchmarks == ("humaneval_plus", "mbpp_plus") and "T1" not in r.generation_only_models
    t = job_config(p.cfg, by["timing.readouts.P4.humaneval_plus.timing.lora200"])
    assert t.lora_max_steps == 200 and t.problem_limit == 50 and t.extra["timing_only"] is True
