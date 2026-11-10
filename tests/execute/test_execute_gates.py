"""K1 gate, bwrap uid and fork limit, infrastructure retries, and NameError counts."""

import dataclasses
import json

import pandas as pd
import pytest

from execute_helpers import build
from pipeline.contracts.schemas import ExecutionResult, ExtractionResult, TestSuite
from pipeline.execute import SandboxConfig, SandboxExecutor, label_samples, agreement_signatures
from pipeline.execute import harness as H
from pipeline.execute import sandbox as sb
from pipeline.execute.cache import ExecCache

import test_execute_stage as T      # reuses the synthetic run directory helpers
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest
from pipeline.execute import stage


# ---- G7: K1 gate --------------------------------------------------------------------------------------
@pytest.fixture()
def bad_run(heplus, tmp_path):
    """Run directory with the good problem plus HumanEval/900 whose reference raises: 1 of 2 excluded."""
    layout = RunLayout.for_run("t", tmp_path)
    p, s = build(heplus, "HumanEval/53", T.BENCH, max_plus=10)
    bad = dataclasses.replace(p, problem_id="HumanEval/900",
                              canonical_solution="def add(x, y):\n    raise ValueError('bad reference')\n")
    bs = {k: dataclasses.replace(v, problem_id="HumanEval/900") for k, v in s.items()}
    (layout.root / "data").mkdir(parents=True)
    layout.problems(T.BENCH).write_text("".join(json.dumps(q.to_dict()) + "\n" for q in (p, bad)))
    layout.suites(T.BENCH).write_text("".join(json.dumps(v.to_dict()) + "\n" for v in [*s.values(), *bs.values()]))
    path = layout.generation_shard("P1", T.BENCH, "frozen", 0)
    path.parent.mkdir(parents=True)
    pd.DataFrame([T.gen_row("P1", 1, T.GOOD)]).to_parquet(path)
    return layout


EXCLUDED = [["HumanEval/900", "E"], ["HumanEval/900", "O"]]


def test_k1_stops_before_extraction_and_labeling(bad_run):
    m = Manifest(run_id="t")
    rep = stage.run(T.cfg(models=("P1",)), bad_run, m)
    assert not rep.ok and rep.metrics["k1_triggered"] is True and rep.metrics["k1_accepted"] is False
    assert any("K1" in n and "stopping" in n for n in rep.notes)
    assert not bad_run.extractions("P1", T.BENCH, "frozen").exists()
    assert bad_run.reference_outputs(T.BENCH).exists()      # the reference record is kept for the operator


def test_k1_accepted_with_exactly_the_excluded_pairs(bad_run):
    bad_run.config_dir.mkdir(parents=True)
    (bad_run.config_dir / "k1_accepted.json").write_text(json.dumps(EXCLUDED))
    rep = stage.run(T.cfg(models=("P1",)), bad_run, Manifest(run_id="t"))
    assert rep.ok and rep.metrics["k1_accepted"] is True
    assert bad_run.extractions("P1", T.BENCH, "frozen").exists()
    (bad_run.config_dir / "k1_accepted.json").write_text(json.dumps({"excluded": EXCLUDED}))   # dict form
    assert stage.run(T.cfg(models=("P1",)), bad_run, Manifest(run_id="t2")).ok


@pytest.mark.parametrize("listed", [[["HumanEval/900", "E"]], EXCLUDED + [["HumanEval/53", "E"]], "garbage"])
def test_k1_acceptance_must_list_exactly_the_excluded_pairs(bad_run, listed):
    bad_run.config_dir.mkdir(parents=True)
    (bad_run.config_dir / "k1_accepted.json").write_text(json.dumps(listed))
    rep = stage.run(T.cfg(models=("P1",)), bad_run, Manifest(run_id="t"))
    assert not rep.ok and not bad_run.extractions("P1", T.BENCH, "frozen").exists()


# ---- G11: bwrap uid, cgroup, fork probe -------------------------------------------------------------------
def test_bwrap_runs_as_a_non_root_uid_in_its_own_user_namespace():
    a = sb.build_bwrap_argv(**{**dict(bwrap="/usr/bin/bwrap", interpreter="/p/python", job_dir="/j", bundle_dir="/b",
                                      ro_binds=("/usr",))})
    assert "--unshare-user" in a and "--unshare-all" in a
    assert a[a.index("--uid") + 1] == "65534" and a[a.index("--gid") + 1] == "65534"
    assert a.index("--unshare-user") < a.index("--uid")


def test_fork_probe_logic():
    r = H.fork_probe(3)                      # no limit applied here: all 6 children start, then are killed
    assert r["result"] == "UNLIMITED" and r["forked"] == 6
    assert not H.fork_limit_enforced(r, 3)
    assert H.fork_limit_enforced({"probe": "fork", "result": "LIMITED", "forked": 3}, 3)
    assert H.fork_limit_enforced({"probe": "fork", "result": "LIMITED", "forked": 0}, 3)
    assert not H.fork_limit_enforced({"probe": "fork", "result": "LIMITED", "forked": 5}, 3)
    assert not H.fork_limit_enforced(None, 3) and not H.fork_limit_enforced({}, 3)


def test_fork_probe_job_runs_through_the_harness(executor):
    raw = executor._probe("fork", limit=2)
    assert raw.result["probe"] == "fork" and raw.result["forked"] <= 4


def test_cgroup_helpers_on_a_fake_hierarchy(tmp_path):
    assert not sb.cgroup_pids_available(tmp_path)
    (tmp_path / "cgroup.controllers").write_text("cpu memory pids\n")
    assert sb.cgroup_pids_available(tmp_path)
    d = sb.cgroup_create("calib-x", 64, tmp_path)
    assert d is not None and (d / "pids.max").read_text() == "64"
    assert sb.cgroup_create("calib-x", 64, tmp_path) is None          # already exists
    (tmp_path / "cgroup.controllers").write_text("cpu memory\n")
    assert not sb.cgroup_pids_available(tmp_path)


def test_infrastructure_signals_are_not_candidate_signals():
    assert sb.infrastructure_signal(-15) and sb.infrastructure_signal(-1) and sb.infrastructure_signal(143)
    for rc in (-9, -11, -6, -24, -25, 137, 0, None):
        assert not sb.infrastructure_signal(rc)


# ---- G19: infrastructure failures ---------------------------------------------------------------------------
class FakeExecutor:
    """Fails the first n_fail runs of each program with sandbox_error, then passes."""

    def __init__(self, n_fail, always_fail_codes=()):
        self.n_fail, self.always = n_fail, tuple(always_fail_codes)
        self.calls = {}
        self.run_info = {}

    def cache_key(self, code, problem, suite, *, capture_outputs=False):
        return f"{code}|{suite.suite_id}|{capture_outputs}"

    def run(self, code, problem, suite, *, trusted=False, capture_outputs=False):
        key = self.cache_key(code, problem, suite, capture_outputs=capture_outputs)
        self.calls[key] = self.calls.get(key, 0) + 1
        bad = any(c in code for c in self.always) or self.calls[key] <= self.n_fail
        outputs = None if bad or not capture_outputs else ("1",)
        self.run_info[key] = {"first_exception": "!NameError" if "NameErr" in code else None}
        return ExecutionResult(key, problem.problem_id, suite.suite_id, not bad and not ("WRONG" in code),
                               "sandbox_error" if bad else ("wrong_output" if "WRONG" in code else None),
                               (), outputs, 0.0, "fixture", "fixture")


def _setup(heplus):
    p, s = build(heplus, "HumanEval/53", T.BENCH, max_plus=2)
    s["agree"] = TestSuite(p.problem_id, "agree", ((1, 2),), None, 0.0, "x", "")
    return p, s


def _ext(i, code, model="P1"):
    return ExtractionResult(f"{model}|frozen|{T.BENCH}|HumanEval/53|{i}", code, "fenced", None)


def test_infrastructure_failure_is_retried_twice_then_succeeds(heplus):
    p, s = _setup(heplus)
    ex = FakeExecutor(n_fail=2)
    rep = {}
    labs = label_samples([_ext(1, "OK")], {p.problem_id: p}, {p.problem_id: s}, ex, None, report=rep)
    assert [l.y for l in labs] == [1, 1] and rep["infrastructure_failures"] == []
    assert set(ex.calls.values()) == {3}                 # first run plus two retries


def test_persistent_infrastructure_failure_leaves_no_label_never_zero(heplus):
    p, s = _setup(heplus)
    ex = FakeExecutor(n_fail=0, always_fail_codes=["BROKEN"])
    rep = {}
    labs = label_samples([_ext(1, "OK"), _ext(2, "BROKEN"), _ext(3, "WRONG")], {p.problem_id: p},
                         {p.problem_id: s}, ex, None, report=rep)
    assert {l.sample_uid.split("|")[-1] for l in labs} == {"1", "3"}          # sample 2 has no row at all
    assert [l.y for l in labs if l.sample_uid.endswith("|3")] == [0, 0]      # a real wrong answer is still 0
    fails = rep["infrastructure_failures"]
    assert sorted(f["suite_id"] for f in fails) == ["E", "O"] and all(f["sample_uid"].endswith("|2") for f in fails)
    assert all(c == 3 for k, c in ex.calls.items() if "BROKEN" in k)


def test_infrastructure_failures_are_not_cached(heplus, tmp_path):
    p, s = _setup(heplus)
    cache = ExecCache(tmp_path / "c.sqlite", audit_share=0.0)
    ex = FakeExecutor(n_fail=0, always_fail_codes=["BROKEN"])
    label_samples([_ext(1, "BROKEN")], {p.problem_id: p}, {p.problem_id: s}, ex, cache)
    assert len(cache) == 0
    cache.close()


def test_agreement_signature_is_missing_after_persistent_infrastructure_failure(heplus):
    p, s = _setup(heplus)
    rep = {}
    sigs = agreement_signatures([_ext(1, "BROKEN"), _ext(2, "OK")], {p.problem_id: p}, {p.problem_id: s},
                                FakeExecutor(0, ["BROKEN"]), None, report=rep)
    assert list(sigs.values()) == [None, ("1",)] and rep["infrastructure_failures"][0]["suite_id"] == "agree"


def test_annotations_are_evaluated_like_plain_evalplus(executor, heplus):
    p, s = _setup(heplus)
    r = executor.run("def add(x: List[int], y):\n    return 0\n", p, s["E"], trusted=True)
    assert r.failure == "exception" and r.per_test == ()


# ---- G8: NameError share --------------------------------------------------------------------------------------
def test_name_error_counts_per_model_benchmark_and_suite(heplus, tmp_path):
    p, s = _setup(heplus)
    ex = SandboxExecutor(SandboxConfig(backend="trusted-only", min_time_limit=0.3))
    cache = ExecCache(tmp_path / "c.sqlite", audit_share=0.0)
    exts = [_ext(1, "def add(x: int, y: int):\n    return x + y\n"),
            _ext(2, "def add(x: List[int], y):\n    return 0\n"),            # NameError when the def runs
            _ext(3, "def add(x, y):\n    return undefined_helper(x)\n"),     # NameError on the first call
            _ext(4, "def add(x, y):\n    return int('x')\n"),                # other exception
            _ext(5, "def add(x, y):\n    return x - y\n", model="P3")]
    for attempt in range(2):                                                  # second pass is served by the cache
        rep = {}
        label_samples(exts, {p.problem_id: p}, {p.problem_id: s}, ex, cache, trusted=True, report=rep)
        ne = rep["name_errors"]
        assert ne["P1"][T.BENCH]["E"] == {"n_executed": 4, "name_error": 2}
        assert ne["P1"][T.BENCH]["O"] == {"n_executed": 4, "name_error": 2}
        assert ne["P3"][T.BENCH]["E"] == {"n_executed": 1, "name_error": 0}
    assert cache.hits > 0
    cache.close()
