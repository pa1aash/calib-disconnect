"""On-disk layout under runs/ and analysis/.

runs/<run_id>/ holds raw outputs. Large files (parquet, safetensors, sqlite, adapters) are git-ignored;
runs/<run_id>/MANIFEST.json is tracked and lists every file with its SHA-256 (pipeline.contracts.manifest).
analysis/ holds the statistics code; derived JSON goes to analysis/results/<run_id>/, computed only
from files listed in a run manifest.

    runs/
      COST_LEDGER.csv                                tracked; one row per pod launch (ops.cost)
      <run_id>/
        MANIFEST.json                                tracked
        config/run_config.json                       resolved config (its SHA-256 is the config hash)
        config/prompts.json                          prompt file hashes and rendered chat-template hashes
        config/answer_tokens.json                    Yes/No token variants per tokenizer (7.12)
        config/mask_spans.json                       elicitation span rule per model (7.12)
        data/problems_<benchmark>.jsonl              problems (LiveCodeBench text never leaves the pod/cache)
        data/suites_<benchmark>.jsonl                test suites, including agreement inputs
        data/reference_checks.parquet
        data/folds_<population>_seed<s>.json         FoldPlan
        data/near_duplicates.json
        generations/<model_key>/<benchmark>/<gen_set>/shard-<nnnnn>.parquet
        capture/<model_key>/<benchmark>/<gen_set>/shard-<nnnnn>.safetensors
        capture/<model_key>/<benchmark>/<gen_set>/index-<nnnnn>.parquet
        execute/extractions/<model_key>/<benchmark>/<gen_set>.parquet
        execute/labels/<model_key>/<benchmark>/<gen_set>.parquet
        execute/cache.sqlite                         execution cache (section 6)
        readouts/<model_key>/<population>/<readout>/<suite>/seed<s>.parquet   ReadoutScore rows
        readouts/<model_key>/<population>/<readout>/<suite>/seed<s>.fits.json FitRecord list
        adapters/<model_key>/...                     LoRA adapters (git-ignored)
        sealed/                                      pilot T1 Gamma cells: written, hashed, not opened (13)
        logs/
        state/<job>.done                             resumability markers (ops.runner)
    analysis/
      <python modules>                               statistics code (hashed before the pilot, section 13)
      results/<run_id>/*.json                        derived statistics with their inputs' manifest hashes
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNS_ROOT = REPO_ROOT / "runs"
ANALYSIS_ROOT = REPO_ROOT / "analysis"
COST_LEDGER = RUNS_ROOT / "COST_LEDGER.csv"
COST_LEDGER_COLUMNS = ("launch_utc", "stop_utc", "pod_id_prefix", "gpu_type", "hourly_price_usd",
                       "price_source", "gpu_hours", "cost_usd", "reason_stopped", "run_id", "git_sha")


@dataclass(frozen=True)
class RunLayout:
    run_id: str
    root: Path

    @classmethod
    def for_run(cls, run_id: str, runs_root: Path | None = None) -> "RunLayout":
        base = runs_root if runs_root is not None else RUNS_ROOT
        return cls(run_id=run_id, root=base / run_id)

    # -- config and data
    @property
    def manifest(self) -> Path:
        return self.root / "MANIFEST.json"

    @property
    def config_dir(self) -> Path:
        return self.root / "config"

    @property
    def run_config(self) -> Path:
        return self.config_dir / "run_config.json"

    @property
    def prompts(self) -> Path:
        return self.config_dir / "prompts.json"

    @property
    def answer_tokens(self) -> Path:
        return self.config_dir / "answer_tokens.json"

    @property
    def mask_spans(self) -> Path:
        return self.config_dir / "mask_spans.json"

    def problems(self, benchmark: str) -> Path:
        return self.root / "data" / f"problems_{benchmark}.jsonl"

    def suites(self, benchmark: str) -> Path:
        return self.root / "data" / f"suites_{benchmark}.jsonl"

    @property
    def reference_checks(self) -> Path:
        return self.root / "data" / "reference_checks.parquet"

    def folds(self, population: str, fold_seed: int) -> Path:
        return self.root / "data" / f"folds_{population}_seed{fold_seed}.json"

    @property
    def near_duplicates(self) -> Path:
        return self.root / "data" / "near_duplicates.json"

    # -- generation and capture
    @staticmethod
    def _gs(gen_set: str) -> str:
        return gen_set.replace(":", "_")

    def generation_shard(self, model_key: str, benchmark: str, gen_set: str, shard: int) -> Path:
        return self.root / "generations" / model_key / benchmark / self._gs(gen_set) / f"shard-{shard:05d}.parquet"

    def capture_shard(self, model_key: str, benchmark: str, gen_set: str, shard: int) -> Path:
        return self.root / "capture" / model_key / benchmark / self._gs(gen_set) / f"shard-{shard:05d}.safetensors"

    def capture_index(self, model_key: str, benchmark: str, gen_set: str, shard: int) -> Path:
        return self.root / "capture" / model_key / benchmark / self._gs(gen_set) / f"index-{shard:05d}.parquet"

    # -- execution
    def extractions(self, model_key: str, benchmark: str, gen_set: str) -> Path:
        return self.root / "execute" / "extractions" / model_key / benchmark / f"{self._gs(gen_set)}.parquet"

    def labels(self, model_key: str, benchmark: str, gen_set: str) -> Path:
        return self.root / "execute" / "labels" / model_key / benchmark / f"{self._gs(gen_set)}.parquet"

    @property
    def exec_cache(self) -> Path:
        return self.root / "execute" / "cache.sqlite"

    # -- readouts
    def scores(self, model_key: str, population: str, readout: str, suite: str | None, fold_seed: int | None) -> Path:
        r = readout.replace(":", "_")
        s = suite or "none"
        fs = "na" if fold_seed is None else str(fold_seed)
        return self.root / "readouts" / model_key / population / r / s / f"seed{fs}.parquet"

    def fits(self, model_key: str, population: str, readout: str, suite: str, fold_seed: int) -> Path:
        return self.scores(model_key, population, readout, suite, fold_seed).with_suffix(".fits.json")

    def adapters(self, model_key: str) -> Path:
        return self.root / "adapters" / model_key

    @property
    def sealed(self) -> Path:
        return self.root / "sealed"

    @property
    def logs(self) -> Path:
        return self.root / "logs"

    def done_marker(self, job_id: str) -> Path:
        return self.root / "state" / f"{job_id}.done"


@dataclass(frozen=True)
class AnalysisLayout:
    run_id: str
    root: Path

    @classmethod
    def for_run(cls, run_id: str, analysis_root: Path | None = None) -> "AnalysisLayout":
        base = analysis_root if analysis_root is not None else ANALYSIS_ROOT
        return cls(run_id=run_id, root=base / "results" / run_id)

    def result(self, name: str) -> Path:
        return self.root / f"{name}.json"
