import json
import sys

import pytest

from ops import plans, runner
from ops.plans import Job, Plan
from ops.runner import Runner
from pipeline.contracts.hashing import sha256_file
from pipeline.contracts.interfaces import RunConfig, StageReport
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest

CFG = RunConfig(run_id="t", models=("M1", "M2", "M3"), benchmarks=("humaneval_plus",), stages=plans.STAGE_ORDER)


def make_plan(launchable=True):
    jobs = [Job("analysis", None, None), Job("readouts", "M1", "label_validity"),
            Job("execute", "M2", "humaneval_plus"), Job("generate", "M1", "humaneval_plus"),
            Job("generate", "M2", "humaneval_plus"), Job("data", None, "humaneval_plus"),
            Job("generate", "M3", "humaneval_plus"), Job("execute", "M1", "humaneval_plus"),
            Job("capture", "M1", "humaneval_plus")]
    return Plan("t", "test", CFG, tuple(jobs), launchable=launchable)


class Fake:
    """Fake stage functions; records calls; optionally fails for chosen (stage, model) pairs."""

    def __init__(self, fail=(), register=True, bad_report=()):
        self.calls, self.fail, self.register, self.bad = [], set(fail), register, set(bad_report)
        self.resolved = []

    def resolver(self, stage):
        self.resolved.append(stage)

        def fn(cfg, layout, manifest, *, dry_run=False):
            m = cfg.models[0] if len(cfg.models) == 1 else None
            self.calls.append((stage, m, cfg.benchmarks, cfg.stages))
            assert dry_run is False
            if (stage, m) in self.fail:
                raise RuntimeError("simulated failure token=hf_SECRETVALUE123")
            if (stage, m) in self.bad:
                return StageReport(stage, ok=False, notes=["bad"])
            rel = f"out/{stage}_{m}_{cfg.extra['scope']}.txt"
            p = layout.root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(f"{stage}{m}{cfg.extra['scope']}")
            if self.register:
                manifest.add(layout.root, p, "fake", "h", "g")
            return StageReport(stage, ok=True, outputs=[rel])
        return fn


def run(tmp_path, fake, plan=None, **kw):
    layout = RunLayout.for_run("t", tmp_path)
    r = Runner(plan or make_plan(), layout, resolver=fake.resolver, git="g", out=lambda s: None, **kw)
    return r.run(), layout


def test_order_and_single_model_stage_config(tmp_path):
    fake = Fake()
    s, _ = run(tmp_path, fake)
    got = [(c[0], c[1]) for c in fake.calls]
    assert got == [("data", None), ("generate", "M1"), ("execute", "M1"), ("capture", "M1"), ("readouts", "M1"),
                   ("generate", "M2"), ("execute", "M2"), ("generate", "M3"), ("analysis", None)]
    assert all(c[3] == (c[0],) for c in fake.calls)           # each job sees only its own stage
    assert s.exit_code == 0 and s.count("done") == 9


def test_done_marker_skip_and_outputs_recorded(tmp_path):
    fake = Fake()
    _, layout = run(tmp_path, fake)
    mk = layout.done_marker("generate.M1.humaneval_plus.frozen")
    rec = json.loads(mk.read_text())
    assert rec["outputs"] == ["out/generate_M1_humaneval_plus.txt"]
    fake2 = Fake()
    s2, _ = run(tmp_path, fake2)
    assert fake2.calls == [] and s2.count("skipped_done") == 9 and fake2.resolved == []


def test_marker_rerun_when_output_changed_or_missing(tmp_path):
    fake = Fake()
    _, layout = run(tmp_path, fake)
    (layout.root / "out/execute_M1_humaneval_plus.txt").write_text("tampered")
    (layout.root / "out/generate_M2_humaneval_plus.txt").unlink()
    fake2 = Fake()
    s2, _ = run(tmp_path, fake2)
    assert [(c[0], c[1]) for c in fake2.calls] == [("execute", "M1"), ("generate", "M2")]
    assert s2.count("done") == 2 and s2.count("skipped_done") == 7
    assert Manifest.load(layout.manifest).verify(layout.root).passed


def test_runner_registers_unlisted_outputs_in_manifest(tmp_path):
    fake = Fake(register=False)
    _, layout = run(tmp_path, fake)
    m = Manifest.load(layout.manifest)
    assert "out/generate_M1_humaneval_plus.txt" in m.entries and "config/run_config.json" in m.entries
    e = m.entries["out/generate_M1_humaneval_plus.txt"]
    assert e.sha256 == sha256_file(layout.root / "out/generate_M1_humaneval_plus.txt")
    assert m.unlisted(layout.root) == []
    assert json.loads((layout.root / "config/run_config.json").read_text())["run_id"] == "t"


def test_failure_stops_run_then_resume_continues_and_manifest_checkpointed(tmp_path):
    fake = Fake(fail={("generate", "M2")})
    s, layout = run(tmp_path, fake)
    assert s.count("failed") == 1 and s.exit_code == 1
    assert [r.status for r in s.results][-4:] == ["failed", "not_run", "not_run", "not_run"]
    saved = Manifest.load(layout.manifest)                       # checkpoint survived the failure
    assert "out/readouts_M1_label_validity.txt" in saved.entries
    assert not layout.done_marker("generate.M2.humaneval_plus.frozen").exists()
    fake2 = Fake()                                               # failure fixed: resume
    s2, _ = run(tmp_path, fake2)
    assert [(c[0], c[1]) for c in fake2.calls] == [("generate", "M2"), ("execute", "M2"), ("generate", "M3"), ("analysis", None)]
    assert s2.exit_code == 0 and s2.count("skipped_done") == 5


def test_manifest_saved_after_every_job(tmp_path, monkeypatch):
    saves = []
    orig = Manifest.save
    monkeypatch.setattr(Manifest, "save", lambda self, path: (saves.append(len(self.entries)), orig(self, path))[1])
    run(tmp_path, Fake())
    assert len(saves) >= 1 + 9 and saves == sorted(saves) and saves[-1] >= 10


def test_keep_going_continues_with_next_model_and_skips_dependents(tmp_path):
    fake = Fake(fail={("execute", "M1")})
    s, layout = run(tmp_path, fake, keep_going=True)
    st = {r.job_id: r.status for r in s.results}
    assert st["execute.M1.humaneval_plus.frozen"] == "failed"
    assert st["capture.M1.humaneval_plus.frozen"] == "skipped_model_failed"
    assert st["readouts.M1.label_validity.frozen"] == "skipped_model_failed"
    assert st["generate.M2.humaneval_plus.frozen"] == "done" and st["generate.M3.humaneval_plus.frozen"] == "done"
    assert st["analysis.all.all.frozen"] == "skipped_dependency" and s.exit_code == 1


def test_data_failure_is_fatal_even_with_keep_going(tmp_path):
    fake = Fake(fail={("data", None)})
    s, _ = run(tmp_path, fake, keep_going=True)
    assert s.count("failed") == 1 and s.count("not_run") == 8 and len(fake.calls) == 1


def test_stage_returning_not_ok_or_missing_output_fails(tmp_path):
    s, _ = run(tmp_path, Fake(bad_report={("generate", "M1")}))
    assert s.results[1].status == "failed" and "ok=False" in s.results[1].note

    class Ghost(Fake):
        def resolver(self, stage):
            return lambda cfg, layout, manifest, *, dry_run=False: StageReport(stage, ok=True, outputs=["nope.txt"])
    s2, _ = run(tmp_path / "x", Ghost())
    assert s2.results[0].status == "failed" and "missing" in s2.results[0].note


def test_error_text_is_scrubbed(tmp_path, monkeypatch):
    monkeypatch.setenv("HF_TOKEN", "hf_SECRETVALUE123")
    s, layout = run(tmp_path, Fake(fail={("generate", "M1")}))
    note = [r for r in s.results if r.status == "failed"][0].note
    assert "SECRETVALUE" not in note and "hf_S..." in note
    assert "SECRETVALUE" not in (layout.logs / "progress.jsonl").read_text()


def test_progress_and_queue_files(tmp_path):
    _, layout = run(tmp_path, Fake())
    rows = [json.loads(l) for l in (layout.logs / "progress.jsonl").read_text().splitlines()]
    done = [r for r in rows if r["status"] == "done"]
    assert len(done) == 9 and len([r for r in rows if r["status"] == "running"]) == 9
    for r in done:
        assert {"ts", "job", "start", "end", "status", "outputs"} <= set(r) and r["outputs"] == 1
    q = json.loads((layout.logs / "queue.json").read_text())
    assert q["finished"] is True and q["pending"] == 0 and q["running"] is False


def test_dry_run_prints_and_imports_nothing(tmp_path, monkeypatch):
    def boom(*a, **k):
        raise AssertionError("dry run imported a module")
    monkeypatch.setattr(runner.importlib, "import_module", boom)
    lines = []
    plan = plans.load_plan("pilot")
    layout = RunLayout.for_run("pilot", tmp_path)
    before = {m for m in ("torch", "vllm", "transformers") if m in sys.modules}
    s = Runner(plan, layout, dry_run=True, out=lines.append).run()
    assert len(lines) == 1 + 39 and "pipeline.generate.stage:run_generate" in "\n".join(lines)
    assert not layout.root.exists()                                  # a dry run writes nothing
    assert {m for m in ("torch", "vllm", "transformers") if m in sys.modules} == before
    assert s.count("not_run") == 39


def test_real_resolver_imports_through_stages_table(monkeypatch):
    seen = []
    monkeypatch.setattr(runner.importlib, "import_module", lambda n: (seen.append(n), type("M", (), {"f": staticmethod(lambda: 1)}))[1])
    fn = runner.import_stage("data", {"data": "some.mod:f"})
    assert seen == ["some.mod"] and fn() == 1


def test_stub_plan_refused(tmp_path):
    with pytest.raises(SystemExit):
        run(tmp_path, Fake(), plan=make_plan(launchable=False))
