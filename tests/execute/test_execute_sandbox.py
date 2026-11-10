"""Trusted-only executor on hand-written fixtures (two HumanEval+ problems and one MBPP+ problem),
refusal rules, reference check, labels, flips, and agreement signatures. Only trusted fixtures and the
benchmark reference solutions run here."""

import pytest

from execute_helpers import build
from pipeline.contracts.schemas import ExtractionResult
from pipeline.execute import (
    IsolationError, ReferenceStore, SandboxConfig, SandboxExecutor, UntrustedExecutionRefused,
    agreement_label_proxy, agreement_signatures, exclusion_report, flip_table, label_samples, reference_check,
)
from pipeline.execute.cache import ExecCache
from pipeline.execute.reference import reference_program

# ---- hand-written fixtures ---------------------------------------------------------------------
ADD_OK = "def add(x: int, y: int):\n    return x + y\n"
ADD_WRONG = "def add(x: int, y: int):\n    return x - y\n"
ADD_RAISES = "def add(x: int, y: int):\n    raise ValueError('boom')\n"
ADD_LOOP = "def add(x: int, y: int):\n    while True:\n        pass\n"
ADD_SWALLOW = ("def add(x: int, y: int):\n    while True:\n        try:\n            while True:\n"
               "                pass\n        except BaseException:\n            pass\n")
ADD_MEMORY = "def add(x: int, y: int):\n    L = []\n    while True:\n        L.append(b'x' * (64 * 1024 * 1024))\n"
ADD_NAMEERROR = "def add(x, y):\n    return undefined_name + x\n"
ADD_PRINTS = "def add(x, y):\n    print('noise')\n    import sys\n    sys.stderr.write('err')\n    return x + y\n"
ADD_EXIT = "import sys\ndef add(x, y):\n    sys.exit(0)\n"

STRLEN_OK = "def strlen(string: str) -> int:\n    return len(string)\n"
STRLEN_WRONG_ON_LONG = "def strlen(string: str) -> int:\n    return min(len(string), 5)\n"

SIM_OK = "def similar_elements(test_tup1, test_tup2):\n    return tuple(sorted(set(test_tup1) & set(test_tup2)))\n"
SIM_WRONG = "def similar_elements(test_tup1, test_tup2):\n    return ()\n"


@pytest.fixture()
def add_problem(heplus):
    return build(heplus, "HumanEval/53", "humaneval_plus", max_plus=40)


@pytest.fixture()
def strlen_problem(heplus):
    return build(heplus, "HumanEval/23", "humaneval_plus", max_plus=60)


@pytest.fixture()
def sim_problem(mbppplus):
    return build(mbppplus, "Mbpp/2", "mbpp_plus", max_plus=40)


def run(ex, code, pair, suite="E"):
    p, s = pair
    return ex.run(code, p, s[suite], trusted=True)


# ---- pass, wrong output, exception, timeout, memory ------------------------------------------------
def test_correct_solution_passes_both_suites(executor, add_problem):
    for sid in ("O", "E"):
        r = run(executor, ADD_OK, add_problem, sid)
        n = len(add_problem[1][sid].inputs)
        assert r.passed and r.failure is None and r.per_test == (True,) * n and r.outputs is None
        assert r.evaluator == "evalplus==0.3.1" and r.sandbox == "rlimit-subprocess"
        assert r.runtime_s >= 0 and r.problem_id == "HumanEval/53" and r.suite_id == sid


def test_wrong_output_stops_at_first_failure(executor, add_problem):
    r = run(executor, ADD_WRONG, add_problem)
    assert not r.passed and r.failure == "wrong_output" and r.per_test[-1] is False and len(r.per_test) <= 3


def test_second_problem_wrong_only_on_long_strings(executor, strlen_problem):
    assert run(executor, STRLEN_OK, strlen_problem).passed
    r = run(executor, STRLEN_WRONG_ON_LONG, strlen_problem)
    assert not r.passed and r.failure == "wrong_output" and any(r.per_test) is True


def test_mbpp_set_oracle_accepts_any_order(executor, sim_problem):
    assert run(executor, SIM_OK, sim_problem).passed
    r = run(executor, SIM_WRONG, sim_problem)
    assert not r.passed and r.failure == "wrong_output"


def test_exception_is_a_failure(executor, add_problem):
    r = run(executor, ADD_RAISES, add_problem)
    assert not r.passed and r.failure == "exception" and r.per_test == (False,)


def test_module_level_error_is_an_exception_with_no_tests(executor, add_problem):
    r = run(executor, ADD_NAMEERROR, add_problem)
    assert not r.passed and r.failure == "exception" and len(r.per_test) == 1
    r = run(executor, "def add(x, y:\n  pass", add_problem)       # does not even compile
    assert not r.passed and r.failure == "exception" and r.per_test == ()
    r = run(executor, "def other():\n    pass\n", add_problem)    # entry point absent at run time
    assert not r.passed and r.failure == "exception"


def test_infinite_loop_times_out_per_test(executor, add_problem):
    r = run(executor, ADD_LOOP, add_problem, "O")
    assert not r.passed and r.failure == "timeout" and r.per_test == (False,)
    assert 0.25 < r.runtime_s < 5


def test_loop_that_swallows_the_alarm_hits_the_program_cap(add_problem):
    ex = SandboxExecutor(SandboxConfig(backend="trusted-only", min_time_limit=0.3, program_cap_s=2.0,
                                       startup_slack_s=0.5))
    r = run(ex, ADD_SWALLOW, add_problem, "O")
    assert not r.passed and r.failure == "program_cap"


def test_memory_limit_stops_an_allocating_program(add_problem):
    ex = SandboxExecutor(SandboxConfig(backend="trusted-only", min_time_limit=20.0, program_cap_s=30.0,
                                       memory_bytes=384 * 1024 * 1024))
    r = run(ex, ADD_MEMORY, add_problem, "O")
    assert not r.passed and r.failure == "memory"


def test_candidate_output_and_exit_do_not_break_the_result(executor, add_problem):
    assert run(executor, ADD_PRINTS, add_problem, "O").passed
    r = run(executor, ADD_EXIT, add_problem, "O")      # SystemExit is a failing test, not a clean exit
    assert not r.passed and r.failure == "exception"


def test_results_are_deterministic_across_runs(executor, add_problem):
    a, b = run(executor, ADD_OK, add_problem), run(executor, ADD_OK, add_problem)
    assert (a.cache_key, a.passed, a.per_test) == (b.cache_key, b.passed, b.per_test)


# ---- refusal rules and interpreter pinning -------------------------------------------------------------
def test_untrusted_call_is_refused_when_execute_untrusted_is_false(add_problem):
    ex = SandboxExecutor(SandboxConfig(backend="trusted-only", execute_untrusted=False))
    p, s = add_problem
    with pytest.raises(UntrustedExecutionRefused):
        ex.run(ADD_OK, p, s["O"])
    with pytest.raises(UntrustedExecutionRefused):
        ex.run(ADD_OK, p, s["O"], trusted=False, capture_outputs=True)


def test_trusted_only_backend_refuses_untrusted_even_when_enabled(add_problem):
    ex = SandboxExecutor(SandboxConfig(backend="trusted-only", execute_untrusted=True))
    p, s = add_problem
    with pytest.raises(UntrustedExecutionRefused):
        ex.run(ADD_OK, p, s["O"])


def test_preflight_cannot_prove_isolation_on_trusted_only(executor):
    with pytest.raises(IsolationError):
        executor.preflight()
    assert executor.preflight_limits()["memory_limit_triggers"] is True


def test_interpreter_must_be_an_absolute_path():
    with pytest.raises(ValueError, match="absolute"):
        SandboxExecutor(SandboxConfig(backend="trusted-only", interpreter="python3"))
    with pytest.raises(ValueError):
        SandboxExecutor(SandboxConfig(backend="trusted-only", interpreter="/nonexistent/python"))
    with pytest.raises(ValueError):
        SandboxExecutor(SandboxConfig(backend="nope"))


def test_interpreter_hash_is_in_the_cache_key(executor, add_problem):
    import hashlib
    import os
    import sys

    assert executor.interpreter == sys.executable
    assert executor.interpreter_sha256 == hashlib.sha256(open(os.path.realpath(sys.executable), "rb").read()).hexdigest()
    p, s = add_problem
    k1 = executor.cache_key(ADD_OK, p, s["O"])
    executor.interpreter_sha256 = "0" * 64
    assert executor.cache_key(ADD_OK, p, s["O"]) != k1


def test_container_backend_needs_a_pinned_digest_and_a_runtime():
    with pytest.raises(ValueError):
        SandboxExecutor(SandboxConfig(backend="container"))
    with pytest.raises((ValueError, IsolationError)):
        SandboxExecutor(SandboxConfig(backend="container", container_image="python:3.12"))


def test_no_silent_fallback_when_bwrap_is_missing():
    import shutil

    if shutil.which("bwrap"):
        pytest.skip("bubblewrap present")
    with pytest.raises(IsolationError):
        SandboxExecutor(SandboxConfig(backend="bwrap", execute_untrusted=True))


# ---- cache keys ----------------------------------------------------------------------------------------
def test_cache_key_depends_on_every_field(executor, add_problem, strlen_problem):
    p, s = add_problem
    base = executor.cache_key(ADD_OK, p, s["O"])
    assert executor.cache_key(ADD_OK, p, s["O"]) == base                              # deterministic
    assert executor.cache_key("def add(x:int,y:int):\n  return (x+y)  # c\n", p, s["O"]) == base   # normalized
    assert executor.cache_key(ADD_WRONG, p, s["O"]) != base
    assert executor.cache_key(ADD_OK, p, s["E"]) != base
    assert executor.cache_key(ADD_OK, strlen_problem[0], strlen_problem[1]["O"]) != base
    ex2 = SandboxExecutor(SandboxConfig(backend="trusted-only", min_time_limit=0.7))
    assert ex2.cache_key(ADD_OK, p, s["O"]) != base                                   # time-limit rule
    ex3 = SandboxExecutor(SandboxConfig(backend="trusted-only", min_time_limit=0.3, memory_bytes=256 * 1024**2))
    assert ex3.cache_key(ADD_OK, p, s["O"]) != base                                   # memory limit
    assert executor.cache_key(ADD_OK, p, s["O"], capture_outputs=True) != base         # capture is its own entry


def test_returned_cache_key_matches_executor_key(executor, add_problem):
    p, s = add_problem
    assert run(executor, ADD_OK, add_problem, "O").cache_key == executor.cache_key(ADD_OK, p, s["O"])


# ---- reference check ------------------------------------------------------------------------------------
FIVE = ["HumanEval/0", "HumanEval/1", "HumanEval/32", "HumanEval/53", "HumanEval/23"]


def test_reference_check_on_five_real_humaneval_plus_problems(heplus, tmp_path):
    ex = SandboxExecutor(SandboxConfig(backend="trusted-only", program_cap_s=60.0))
    problems, suites = [], {}
    for tid in FIVE:
        p, s = build(heplus, tid, "humaneval_plus", max_plus=80)
        problems.append(p)
        suites[tid] = s
    store = ReferenceStore(tmp_path / "ref.jsonl")
    checks = reference_check(problems, suites, ex, store=store, workers=2)
    assert len(checks) == 10
    assert all(c.passed and not c.excluded and c.failure is None for c in checks), checks   # incl. find_zero (HumanEval/32)
    rep = exclusion_report(checks)
    assert rep["per_suite"]["O"]["share"] == 0.0 and rep["k1_triggered"] is False
    # outputs, runtimes, and limits are recorded and persist
    e = store.get("HumanEval/53", "O")
    assert e.ok and len(e.outputs_canon) == len(suites["HumanEval/53"]["O"].inputs) == len(e.time_limits_s)
    assert all(t >= 1.0 for t in e.time_limits_s)
    store.save()
    again = ReferenceStore(tmp_path / "ref.jsonl")
    assert again.get("HumanEval/53", "O").ref_hash == e.ref_hash


def test_reference_that_raises_or_times_out_is_excluded_not_repaired(add_problem):
    import dataclasses

    p, s = add_problem
    ex = SandboxExecutor(SandboxConfig(backend="trusted-only", program_cap_s=10.0, reference_test_timeout_s=0.5))
    bad_raise = dataclasses.replace(p, problem_id="X/raise", canonical_solution=ADD_RAISES)
    bad_loop = dataclasses.replace(p, problem_id="X/loop", canonical_solution=ADD_LOOP)
    bad_nondet = dataclasses.replace(p, problem_id="X/nondet", canonical_solution=(
        "import random\ndef add(x, y):\n    return x + y + random.randint(0, 10 ** 9)\n"))
    suites = {q.problem_id: {k: dataclasses.replace(v, problem_id=q.problem_id) for k, v in s.items()}
              for q in (bad_raise, bad_loop, bad_nondet)}
    checks = {(c.problem_id, c.suite_id): c for c in reference_check([bad_raise, bad_loop, bad_nondet], suites, ex)}
    assert checks[("X/raise", "O")].excluded and checks[("X/raise", "O")].failure == "exception"
    assert checks[("X/loop", "E")].excluded and checks[("X/loop", "E")].failure == "timeout"
    c = checks[("X/nondet", "O")]
    assert c.excluded and not c.passed and c.failure == "wrong_output"   # fails its own pass criterion
    rep = exclusion_report(list(checks.values()))
    assert rep["per_suite"]["O"]["share"] == 1.0 and rep["k1_triggered"] is True


def test_k1_threshold_is_five_percent():
    from pipeline.contracts.schemas import ReferenceCheck

    mk = lambda i, ex: ReferenceCheck(f"p{i}", "E", not ex, "exception" if ex else None, ex)   # noqa: E731
    ok = [mk(i, i < 5) for i in range(100)]         # exactly 5 percent: not above the threshold
    assert exclusion_report(ok)["k1_triggered"] is False
    assert exclusion_report([mk(i, i < 6) for i in range(100)])["k1_triggered"] is True


def test_reference_program_handles_body_only_solutions(heplus):
    r = heplus["HumanEval/53"]
    from pipeline.contracts.schemas import Problem

    body_only = Problem("HumanEval/53", "humaneval_plus", r["prompt"], r["entry_point"], r["canonical_solution"],
                        "function", None)
    full = Problem("HumanEval/53", "humaneval_plus", r["prompt"], r["entry_point"],
                   r["prompt"] + r["canonical_solution"], "function", None)
    assert reference_program(body_only) == reference_program(full) == r["prompt"] + r["canonical_solution"]


# ---- labels, flips, cache reuse ----------------------------------------------------------------------------
def _ext(model, idx, code, pid="HumanEval/53", failure=None, bench="humaneval_plus"):
    uid = f"{model}|frozen|{bench}|{pid}|{idx}"
    return ExtractionResult(uid, None if failure else code, None if failure else "fenced", failure)


def test_label_samples_and_cache_reuse(add_problem, tmp_path):
    ex = SandboxExecutor(SandboxConfig(backend="trusted-only", min_time_limit=0.3))
    p, s = add_problem
    calls = []
    real_run = ex.run
    ex.run = lambda *a, **k: (calls.append(1), real_run(*a, **k))[1]
    cache = ExecCache(tmp_path / "c.sqlite", audit_share=0.0)
    exts = [_ext("P1", 1, ADD_OK), _ext("P1", 2, ADD_WRONG), _ext("P3", 1, "def add(x:int,y:int):\n    return (x + y)  # same\n"),
            _ext("P1", 3, None, failure="no_block"), _ext("P1", 4, None, failure="truncated")]
    labs = label_samples(exts, {p.problem_id: p}, {p.problem_id: s}, ex, cache, trusted=True)
    assert len(labs) == 10
    by = {(l.sample_uid.split("|")[0], l.sample_uid.split("|")[-1], l.suite_id): l for l in labs}
    assert by[("P1", "1", "O")].y == 1 and by[("P1", "1", "E")].y == 1 and by[("P1", "1", "E")].source == "execution"
    assert by[("P1", "2", "E")].y == 0 and by[("P1", "2", "E")].failure == "wrong_output"
    assert by[("P3", "1", "O")].cache_key == by[("P1", "1", "O")].cache_key       # identical program, shared
    for sid in ("O", "E"):
        l = by[("P1", "3", sid)]
        assert (l.y, l.source, l.failure, l.cache_key) == (0, "extraction_failure", "no_block", None)
        assert by[("P1", "4", sid)].failure == "truncated"
    assert len(calls) == 4                                  # 2 distinct programs x 2 suites; duplicates and failures not run
    calls.clear()
    again = label_samples(exts, {p.problem_id: p}, {p.problem_id: s}, ex, cache, trusted=True)
    assert again == labs and calls == []                    # served from the cache
    assert cache.stats()["hits"] >= 4
    cache.close()


def test_excluded_pairs_get_no_label_row(add_problem, tmp_path):
    ex = SandboxExecutor(SandboxConfig(backend="trusted-only"))
    p, s = add_problem
    labs = label_samples([_ext("P1", 1, ADD_OK)], {p.problem_id: p}, {p.problem_id: s}, ex, None, trusted=True,
                         excluded={("HumanEval/53", "E")})
    assert [l.suite_id for l in labs] == ["O"]


def test_label_samples_refuses_untrusted_without_permission(add_problem):
    ex = SandboxExecutor(SandboxConfig(backend="trusted-only"))
    p, s = add_problem
    with pytest.raises(UntrustedExecutionRefused):
        label_samples([_ext("P1", 1, ADD_OK)], {p.problem_id: p}, {p.problem_id: s}, ex, None)
    # extraction failures need no execution, so they are labeled even then
    labs = label_samples([_ext("P1", 1, None, failure="no_block")], {p.problem_id: p}, {p.problem_id: s}, ex, None)
    assert [l.y for l in labs] == [0, 0]


def test_cache_audit_logs_a_mismatch(add_problem, tmp_path):
    ex = SandboxExecutor(SandboxConfig(backend="trusted-only", min_time_limit=0.3))
    p, s = add_problem
    log = tmp_path / "logs" / "cache_audit.jsonl"
    cache = ExecCache(tmp_path / "c.sqlite", audit_share=1.0, audit_log=log)
    exts = [_ext("P1", 1, ADD_OK)]
    label_samples(exts, {p.problem_id: p}, {p.problem_id: s}, ex, cache, trusted=True)
    assert cache.mismatches == 0
    label_samples(exts, {p.problem_id: p}, {p.problem_id: s}, ex, cache, trusted=True)   # hits are audited
    assert cache.audits == 2 and cache.mismatches == 0 and not log.exists()
    # corrupt one entry: the audit must notice and log it
    key = ex.cache_key(ADD_OK, p, s["O"])
    import dataclasses

    bad = dataclasses.replace(cache.get(key), passed=False, failure="timeout")
    cache.put(bad)
    label_samples(exts, {p.problem_id: p}, {p.problem_id: s}, ex, cache, trusted=True)
    assert cache.mismatches == 1 and log.exists()
    assert key in log.read_text()
    cache.close()


def test_flip_table():
    from pipeline.contracts.schemas import Label

    L = lambda uid, sid, y: Label(uid, sid, y, "execution", None, None)   # noqa: E731
    u = lambda m, i: f"{m}|frozen|humaneval_plus|HumanEval/1|{i}"          # noqa: E731
    labels = [L(u("P1", 1), "O", 1), L(u("P1", 1), "E", 0),               # pass to fail
              L(u("P1", 2), "O", 0), L(u("P1", 2), "E", 1),               # fail to pass (investigate)
              L(u("P1", 3), "O", 1), L(u("P1", 3), "E", 1),
              L(u("P1", 4), "O", 0), L(u("P1", 4), "E", 0),
              L(u("P3", 1), "O", 1), L(u("P3", 1), "E", 0),
              L(u("P3", 2), "O", 1)]                                      # unpaired
    t = flip_table(labels)
    assert t["P1"]["pass_to_fail"] == 1 and t["P1"]["fail_to_pass"] == 1 and t["P1"]["both_pass"] == 1
    assert t["P1"]["both_fail"] == 1 and t["P1"]["fail_to_pass_uids"] == [u("P1", 2)]
    assert t["P3"]["pass_to_fail"] == 1 and t["P3"]["n_unpaired"] == 1 and t["P3"]["fail_to_pass_uids"] == []


# ---- agreement signatures --------------------------------------------------------------------------------------
def test_agreement_signatures_and_label_proxy(heplus, tmp_path):
    import dataclasses

    from pipeline.contracts.schemas import TestSuite

    ex = SandboxExecutor(SandboxConfig(backend="trusted-only", min_time_limit=0.3))
    p, s = build(heplus, "HumanEval/53", "humaneval_plus", max_plus=30)
    inputs = ((1, 2), (0, 0), (-5, 5), (10, 20), (7, 0))          # (7, 0), (0, 0) and (10, 20) also occur as label outputs
    s["agree"] = TestSuite(p.problem_id, "agree", inputs, None, 0.0, "x", "")
    exts = [_ext("P1", 1, ADD_OK), _ext("P1", 2, "def add(x, y):\n    return y + x\n"), _ext("P1", 3, ADD_WRONG),
            _ext("P1", 4, ADD_RAISES), _ext("P1", 5, None, failure="syntax_error"), _ext("P1", 6, ADD_NAMEERROR)]
    cache = ExecCache(tmp_path / "c.sqlite", audit_share=0.0)
    sigs = agreement_signatures(exts, {p.problem_id: p}, {p.problem_id: s}, ex, cache, trusted=True)
    u = lambda i: f"P1|frozen|humaneval_plus|HumanEval/53|{i}"      # noqa: E731
    assert sigs[u(1)] == ("3", "0", "0", "30", "7") == sigs[u(2)]  # commutative variant agrees
    assert sigs[u(3)] == ("-1", "0", "-10", "-10", "7")
    assert sigs[u(4)] == ("!ValueError",) * 5
    assert sigs[u(5)] is None                                       # extraction failure: no signature
    assert sigs[u(6)] == ("!NameError",) * 5                         # error at call time, per input
    assert sigs[u(1)] != sigs[u(3)]
    # the executed program also gets a cached entry for the agree input set
    assert len(cache) == 5
    # label proxy: reference outputs on agree inputs that also occur among label-input outputs
    store = ReferenceStore(None)
    ex.references = store
    reference_check([p], {p.problem_id: s}, ex, store=store)
    proxy = agreement_label_proxy([p], {p.problem_id: s}, store)
    e = proxy["problems"]["HumanEval/53"]
    label_out = set(store.get(p.problem_id, "E").outputs_canon)
    assert e["n_agree"] == 5 and e["n_equal_to_a_label_output"] == sum(o in label_out for o in ("3", "0", "0", "30", "7"))
    assert 0.0 <= e["share"] <= 1.0
    cache.close()


def test_no_agreement_inputs_means_no_signature(add_problem):
    ex = SandboxExecutor(SandboxConfig(backend="trusted-only"))
    p, s = add_problem
    sigs = agreement_signatures([_ext("P1", 1, ADD_OK)], {p.problem_id: p}, {p.problem_id: s}, ex, None, trusted=True)
    assert list(sigs.values()) == [None]


def test_agree_run_returns_outputs_in_the_result(executor, add_problem):
    import dataclasses

    p, s = add_problem
    agree = dataclasses.replace(s["O"], suite_id="agree", inputs=((1, 2), (3, 4)))
    r = executor.run(ADD_OK, p, agree, trusted=True)
    assert r.passed and r.outputs == ("3", "7") and r.per_test == (True, True)
    r = executor.run(ADD_OK, p, s["O"], trusted=True, capture_outputs=True)
    assert r.outputs is not None and len(r.outputs) == len(s["O"].inputs)


def test_agree_signature_normalizes_floats(heplus):
    import dataclasses

    from pipeline.contracts.schemas import TestSuite

    ex = SandboxExecutor(SandboxConfig(backend="trusted-only"))
    p, s = build(heplus, "HumanEval/53", "humaneval_plus", max_plus=1)
    agree = TestSuite(p.problem_id, "agree", ((0.1, 0.2),), None, 0.0, "x", "")
    a = ex.run("def add(x, y):\n    return x + y\n", p, agree, trusted=True).outputs
    b = ex.run("def add(x, y):\n    return 0.3\n", p, agree, trusted=True).outputs
    assert a == b == ("0.3",)
