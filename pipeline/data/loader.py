"""BenchmarkLoader implementation (pipeline.contracts.interfaces.BenchmarkLoader)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

from pipeline.contracts.layout import REPO_ROOT
from pipeline.contracts.schemas import LABEL_SUITES_LV, Problem, TestSuite

from . import agreement as agr
from . import evalplus_data as ed
from . import lcb as lcbmod
from . import pins as pinmod
from .inputs import input_set_sha256

DEFAULT_AGREEMENT_SEED = 0
EVALPLUS_BENCHMARKS = ("humaneval_plus", "mbpp_plus")


def resolve_cache(bench_cache: str | Path) -> Path:
    p = Path(bench_cache)
    return p if p.is_absolute() else REPO_ROOT / p


class DataLoader:
    def __init__(self, bench_cache: str | Path, *, agreement_seed: int = DEFAULT_AGREEMENT_SEED,
                 workers: int = 4, lcb_store: lcbmod.LcbStore | None = None) -> None:
        self.cache_dir = resolve_cache(bench_cache)
        self.agreement_seed = agreement_seed
        self.workers = workers
        self._rows: dict[str, dict[str, Any]] = {}
        self._gen_contract: dict[str, str] = {}  # patched MBPP+ tasks: contract adapted to the patched signature
        self._problems: dict[str, list[Problem]] = {}
        self._lcb = lcb_store
        self.agreement_stats: dict[str, dict[str, Any]] = {}
        self.patch_sha256: str | None = None

    # -- LiveCodeBench store (created lazily)
    @property
    def lcb(self) -> lcbmod.LcbStore:
        if self._lcb is None:
            self._lcb = lcbmod.LcbStore(self.cache_dir)
        return self._lcb

    # -- BenchmarkLoader protocol
    def verify_pins(self, benchmarks: Sequence[str] = EVALPLUS_BENCHMARKS) -> list[tuple[str, bool]]:
        """(file, sha256 matches) for every pinned file the benchmarks need. A missing file raises
        PinError; a mismatch is reported as False. LiveCodeBench shards are hashed in full (slow)."""
        out = []
        for b in benchmarks:
            for pin in pinmod.pins_for_benchmark(b):
                path = pinmod.locate(pin, self.cache_dir)
                if path is None:
                    raise pinmod.PinError(f"pinned file {pin.key} is missing under {self.cache_dir}")
                out.append((str(path), pinmod.verify_file(path, pin)))
        return out

    def _load_evalplus(self, benchmark: str) -> None:
        if benchmark in self._problems:
            return
        if benchmark == "humaneval_plus":
            rows, sha = ed.load_humaneval_plus(self.cache_dir)
            probs = ed.humaneval_plus_problems(rows, sha)
        else:
            raw, sha, self.patch_sha256 = ed.read_mbpp_plus_raw(self.cache_dir)
            rows = ed.apply_mbpp_patch(raw)
            self._gen_contract.update(ed.generation_contracts(raw, rows))
            probs = ed.mbpp_plus_problems(rows, sha)
        self._problems[benchmark] = probs
        for r in rows:
            self._rows[r["task_id"]] = r

    def problems(self, benchmark: str) -> list[Problem]:
        if benchmark in EVALPLUS_BENCHMARKS:
            self._load_evalplus(benchmark)
            return list(self._problems[benchmark])
        if benchmark == "lcb_v6":
            if benchmark not in self._problems:
                self._problems[benchmark] = self.lcb.problems()
            return list(self._problems[benchmark])
        raise KeyError(f"unknown benchmark {benchmark!r}")

    def suites(self, problem: Problem) -> dict[str, TestSuite]:
        if problem.benchmark in EVALPLUS_BENCHMARKS:
            self._load_evalplus(problem.benchmark)
            return ed.evalplus_suites(self._rows[problem.problem_id])
        if problem.benchmark == "lcb_v6":
            s = self.lcb.suites_for(problem.problem_id.removeprefix("lcb/"))
            s.pop("agree")
            return s
        raise KeyError(f"unknown benchmark {problem.benchmark!r}")

    def lcb_suites_with_agree(self, problem: Problem) -> dict[str, TestSuite]:
        """All four LiveCodeBench suites of one problem, read once."""
        return self.lcb.suites_for(problem.problem_id.removeprefix("lcb/"))

    def agreement_inputs(self, problem: Problem, suites: Mapping[str, TestSuite], seed: int | None = None) -> TestSuite:
        seed = self.agreement_seed if seed is None else seed
        if problem.benchmark == "lcb_v6":
            return self.lcb.suites_for(problem.problem_id.removeprefix("lcb/"))["agree"]
        return self.agreement_batch([problem], {problem.problem_id: suites}, seed, workers=1)[problem.problem_id]

    def generation_row(self, problem_id: str) -> dict[str, Any]:
        """The raw record used to generate agreement inputs (patched MBPP+ tasks carry the adapted contract)."""
        row = self._rows[problem_id]
        if problem_id in self._gen_contract:
            row = {**row, "contract": self._gen_contract[problem_id]}
        return row

    # -- batch interface used by the stage
    def agreement_batch(self, problems: Sequence[Problem], suites: Mapping[str, Mapping[str, TestSuite]],
                        seed: int | None = None, workers: int | None = None) -> dict[str, TestSuite]:
        """HumanEval+/MBPP+ agreement suites for many problems, generated in isolated child processes.
        Per-problem counts are stored in self.agreement_stats."""
        seed = self.agreement_seed if seed is None else seed
        jobs = []
        for p in problems:
            self._load_evalplus(p.benchmark)
            label = [i for sid in LABEL_SUITES_LV if sid in suites[p.problem_id]
                     for i in suites[p.problem_id][sid].inputs]
            jobs.append((p.problem_id, self.generation_row(p.problem_id), label))
        res = agr.run_isolated(jobs, seed, workers=workers or self.workers)
        out = {}
        for p in problems:
            r = res[p.problem_id]
            inputs = tuple(tuple(i) for i in r["inputs"])
            self.agreement_stats[p.problem_id] = dict(r["stats"])
            atol = suites[p.problem_id]["E"].atol if "E" in suites[p.problem_id] else 0.0
            out[p.problem_id] = TestSuite(problem_id=p.problem_id, suite_id="agree", inputs=inputs, expected=None,
                                          atol=atol, time_limit_rule=ed.TIME_LIMIT_RULE,
                                          input_set_sha256=input_set_sha256(inputs))
        return out
