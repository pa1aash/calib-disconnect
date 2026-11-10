"""Reading A of the generation shift (design 1.5 and 7.5): scoring the fresh sets.

A fresh set "fresh:SR_<suite>_seed<s>_fold<f>" holds k_g samples per test-fold problem generated with the
S^R adapter of that suite, fold seed, and outer fold, and its base-weights capture (same capture layout,
with the generation set). For each such set this step writes, with `generation_set` set and files under
`layout.scores(..., gen_set=...)`:

  * P rows: the persisted fitted probe of that (model, population, suite, fold seed, outer fold), read on the
    fresh samples' base-weights hidden states (the probe is the same fitted member as on frozen samples);
  * SR rows: S^R of that fold's saved adapter, scored from each sample's own suffix position (the token after
    the last "I am" the sample contains; without one, "I am" is teacher-forced after the completion).

Names: probes are persisted at `adapters/<model>/probes/P_<population>_<suite>_seed<s>_fold<f>.npz`; S^R adapters
at `adapters/<model>/sr_<population>_<suite>_seed<s>_fold<f>` (peft directory; `.npz` for the mock surrogate).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from pipeline.contracts.interfaces import ReadoutData
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.schemas import ReadoutScore

from .common import sigmoid
from .probe import FittedProbe

FRESH_DIR = re.compile(r"^fresh_SR_(?P<suite>.+)_seed(?P<seed>\d+)_fold(?P<fold>\d+)$")


@dataclass(frozen=True)
class FreshSet:
    gen_set: str      # "fresh:SR_E_seed0_fold3"
    suite: str
    seed: int
    fold: int


def discover_fresh_sets(layout: RunLayout, model_key: str, benches: Sequence[str]) -> list[FreshSet]:
    found: dict[str, FreshSet] = {}
    for b in benches:
        d = layout.root / "capture" / model_key / b
        if not d.exists():
            continue
        for sub in sorted(d.iterdir()):
            m = FRESH_DIR.match(sub.name)
            if m and sub.is_dir():
                gs = "fresh:" + sub.name[len("fresh_"):]
                found[gs] = FreshSet(gs, m["suite"], int(m["seed"]), int(m["fold"]))
    return [found[k] for k in sorted(found)]


def probe_path(layout: RunLayout, model_key: str, population: str, suite: str, seed: int, fold: int) -> Path:
    return layout.adapters(model_key) / "probes" / f"P_{population}_{suite}_seed{seed}_fold{fold}.npz"


def sr_adapter_path(layout: RunLayout, model_key: str, population: str, suite: str, seed: int, fold: int,
                    surrogate: bool = False) -> Path:
    return layout.adapters(model_key) / (f"sr_{population}_{suite}_seed{seed}_fold{fold}" + (".npz" if surrogate else ""))


def _rows(data: ReadoutData, z: np.ndarray, *, model_key: str, population: str, readout: str, fs: FreshSet,
          flagged: bool = False) -> list[ReadoutScore]:
    p = sigmoid(z)
    return [ReadoutScore(sample_uid=u, model_key=model_key, population=population, readout=readout,
                         label_suite=fs.suite, fold_seed=fs.seed, fold=fs.fold, prob=float(pi), rank_score=float(zi),
                         rank_tiebreak=float("nan"), generation_set=fs.gen_set, flagged=flagged)
            for u, zi, pi in zip(data.sample_uids, z, p)]


def probe_rows(data: ReadoutData, probe: FittedProbe, model_key: str, population: str, fs: FreshSet) -> list[ReadoutScore]:
    return _rows(data, probe.logits(data.hidden), model_key=model_key, population=population, readout="P", fs=fs)


def sr_rows(data: ReadoutData, z: np.ndarray, model_key: str, population: str, fs: FreshSet) -> list[ReadoutScore]:
    return _rows(data, np.asarray(z, dtype=np.float64), model_key=model_key, population=population, readout="SR", fs=fs)
