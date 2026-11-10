"""Stage tests on a tiny synthetic run directory. Samples are hand-written fixtures; the executor used for
the label path is a test subclass that skips isolation (the fixtures are trusted)."""

import json
import os

import pandas as pd
import pytest

from execute_helpers import build
from pipeline.contracts.hashing import config_hash
from pipeline.contracts.interfaces import RunConfig
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest
from pipeline.contracts.schemas import TABLE_COLUMNS, TestSuite
from pipeline.execute import SandboxConfig, SandboxExecutor, stage

BENCH = "humaneval_plus"
GOOD = "```python\ndef add(x: int, y: int):\n    return x + y\n```"
BAD = "```python\ndef add(x: int, y: int):\n    return x - y\n```"


class FixtureExecutor(SandboxExecutor):
    """Runs hand-written fixtures only. Isolation is not available on this machine."""

    def _require_allowed(self, trusted):
        return

    def preflight(self):
        self.preflight_report = {"fixture": True}


def gen_row(model, idx, text, truncated=False, pid="HumanEval/53"):
    d = dict.fromkeys(TABLE_COLUMNS["generations"], None)
    d.update(sample_uid=f"{model}|frozen|{BENCH}|{pid}|{idx}", model_key=model, model_id="m", revision="r",
             benchmark=BENCH, problem_id=pid, sample_index=idx, generation_set="frozen", seed=1, prompt_sha256="a",
             rendered_prompt_sha256="b", completion_text=text, completion_token_ids=[1, 2], finish_reason="stop",
             truncated=truncated, engine="mock", thinking=False)
    return d


@pytest.fixture()
def run_dir(heplus, tmp_path):
    layout = RunLayout.for_run("t", tmp_path)
    p, s = build(heplus, "HumanEval/53", BENCH, max_plus=25)
    s["agree"] = TestSuite(p.problem_id, "agree", ((1, 2), (5, 5), (0, 9)), None, 0.0, "x", "")
    (layout.root / "data").mkdir(parents=True)
    layout.problems(BENCH).write_text(json.dumps(p.to_dict()) + "\n")
    layout.suites(BENCH).write_text("".join(json.dumps(v.to_dict()) + "\n" for v in s.values()))
    rows = [gen_row("P1", 1, GOOD), gen_row("P1", 2, BAD), gen_row("P1", 3, "no code here"),
            gen_row("P1", 4, GOOD, truncated=True)]
    rows += [gen_row("B1", 1, "    return x + y\n\ndef junk():\n    pass\n"), gen_row("B1", 2, "    return x * y\n")]
    for m in ("P1", "B1"):
        sub = [r for r in rows if r["model_key"] == m]
        path = layout.generation_shard(m, BENCH, "frozen", 0)
        path.parent.mkdir(parents=True)
        pd.DataFrame(sub).to_parquet(path)
    return layout


def cfg(**kw):
    base = dict(run_id="t", models=("P1", "B1"), benchmarks=(BENCH,), sandbox="trusted-only", execute_untrusted=False)
    base.update(kw)
    return RunConfig(**base)


def tree(root):
    return sorted(os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs)


def test_dry_run_writes_nothing(run_dir):
    before = tree(run_dir.root)
    m = Manifest(run_id="t")
    rep = stage.run(cfg(), run_dir, m, dry_run=True)
    assert tree(run_dir.root) == before and not m.entries
    assert rep.ok and any("execute_untrusted is False" in n for n in rep.notes)


def test_dry_run_reports_missing_inputs(tmp_path):
    rep = stage.run(cfg(), RunLayout.for_run("t", tmp_path), Manifest(run_id="t"), dry_run=True)
    assert not rep.ok and any("input missing" in n for n in rep.notes)


def test_stage_without_untrusted_permission_runs_only_the_reference_check(run_dir):
    m = Manifest(run_id="t")
    rep = stage.run(cfg(), run_dir, m)
    assert rep.ok and rep.stage == "execute"
    assert any("no extracted sample was executed" in n for n in rep.notes)
    # reference check outputs
    ref = pd.read_parquet(run_dir.reference_checks)
    assert list(ref.columns) == list(TABLE_COLUMNS["reference_checks"])
    assert set(ref.suite_id) == {"O", "E", "agree"} and ref.passed.all() and not ref.excluded.any()
    assert run_dir.reference_outputs(BENCH).exists() and rep.metrics["k1_triggered"] is False
    assert (run_dir.root / "execute" / "agreement_label_proxy.json").exists()
    # extraction tables only
    for model in ("P1", "B1"):
        assert run_dir.extractions(model, BENCH, "frozen").exists()
        assert not run_dir.labels(model, BENCH, "frozen").exists()
        assert not run_dir.agreement_outputs(model, BENCH, "frozen").exists()
    assert not run_dir.exec_cache.exists()
    ex = pd.read_parquet(run_dir.extractions("P1", BENCH, "frozen"))
    assert list(ex.columns) == list(TABLE_COLUMNS["extractions"])
    assert list(ex.failure.fillna("-")) == ["-", "-", "no_block", "truncated"]
    # base model: completion mode with the problem prompt, cut at the stop string
    exb = pd.read_parquet(run_dir.extractions("B1", BENCH, "frozen"))
    assert exb.method.tolist() == ["completion", "completion"] and "def junk" not in exb.code[0]
    assert rep.metrics["extraction_failures"]["P1/humaneval_plus/frozen"] == {"no_block": 1, "truncated": 1}
    # every written file is in the manifest with a matching hash
    assert set(rep.outputs) == set(m.entries) and m.verify(run_dir.root).passed
    assert all(e.producer == "pipeline.execute.stage:run" for e in m.entries.values())
    assert next(iter(m.entries.values())).config_hash == config_hash(cfg().to_dict())


def test_stage_refuses_to_execute_on_trusted_only_even_if_asked(run_dir):
    rep = stage.run(cfg(execute_untrusted=True), run_dir, Manifest(run_id="t"))
    assert not rep.ok and any("trusted-only" in n for n in rep.notes)
    assert not run_dir.labels("P1", BENCH, "frozen").exists()
    assert run_dir.extractions("P1", BENCH, "frozen").exists()


def test_stage_full_path_with_a_fixture_executor(run_dir, monkeypatch):
    def make(c, store):
        return FixtureExecutor(SandboxConfig(backend="trusted-only", execute_untrusted=True, min_time_limit=0.5),
                               references=store)

    monkeypatch.setattr(stage, "_make_executor", make)
    c = cfg(sandbox="bwrap", execute_untrusted=True)
    m = Manifest(run_id="t")
    rep = stage.run(c, run_dir, m)
    assert rep.ok, rep.notes
    lab = pd.read_parquet(run_dir.labels("P1", BENCH, "frozen"))
    assert list(lab.columns) == list(TABLE_COLUMNS["labels"]) and len(lab) == 8
    got = {(r.sample_uid.split("|")[-1], r.suite_id): (r.y, r.source, r.failure) for r in lab.itertuples()}
    assert got[("1", "E")][:2] == (1, "execution") and pd.isna(got[("1", "E")][2]) and got[("2", "E")][0] == 0
    assert got[("3", "O")] == (0, "extraction_failure", "no_block") and got[("4", "E")][2] == "truncated"
    labb = pd.read_parquet(run_dir.labels("B1", BENCH, "frozen"))
    assert dict(zip(labb.sample_uid.str.split("|").str[-1] + labb.suite_id, labb.y)) == {"1O": 1, "1E": 1, "2O": 0, "2E": 0}
    agr = pd.read_parquet(run_dir.agreement_outputs("P1", BENCH, "frozen"))
    sig = {r.sample_uid.split("|")[-1]: r.signature for r in agr.itertuples()}
    assert json.loads(sig["1"]) == ["3", "10", "9"] and json.loads(sig["2"]) == ["-1", "0", "-9"]
    assert pd.isna(sig["3"]) and pd.isna(sig["4"])
    assert run_dir.exec_cache.exists() and rep.metrics["cache"]["puts"] > 0
    assert rep.metrics["flip_table"]["P1"]["fail_to_pass"] == 0
    assert set(rep.outputs) == set(m.entries) and m.verify(run_dir.root).passed
    # resumable: a second run skips finished sets
    rep2 = stage.run(c, run_dir, m)
    assert sorted(rep2.skipped) == ["B1/humaneval_plus/frozen", "P1/humaneval_plus/frozen"]


def test_dry_run_lists_the_label_outputs_when_execution_is_allowed(run_dir):
    rep = stage.run(cfg(sandbox="bwrap", execute_untrusted=True), run_dir, Manifest(run_id="t"), dry_run=True)
    assert any("labels" in o for o in rep.outputs) and any("agreement" in o for o in rep.outputs)


def test_mbpp_inputs_are_decoded_before_running(mbppplus):
    # Mbpp/2 stores tuples inside the argument lists; JSON turns them into lists, decode_suite restores them
    from pipeline.contracts.schemas import Problem

    p, s = build(mbppplus, "Mbpp/2", "mbpp_plus", max_plus=3)
    raw = TestSuite.from_dict(json.loads(json.dumps(s["O"].to_dict())))
    assert isinstance(raw.inputs[0][0], list)
    dec = stage.decode_suite(raw)
    assert isinstance(dec.inputs[0][0], tuple) and dec.inputs == s["O"].inputs
