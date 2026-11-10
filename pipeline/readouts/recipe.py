"""Training-recipe plumbing shared by the masked-LoRA readout, the R-Tuning readout, the capacity
ladder, and the mock-backend surrogate (design 7.4, 7.3, and K4 of section 13).

Nothing here touches a model. A trainer implements `AdapterTrainer.fit`; this module decides what to
train, for how long, and what to do with the results:

  * `select_recipes`: per (fold seed, outer fold), learning rate in LORA_LR_GRID and step count chosen by
    inner-validation log loss on the FIRST inner split, evaluated every LORA_EVAL_EVERY_STEPS steps, with
    the cosine schedule set to LORA_MAX_EPOCHS epochs. K4 (judged per fit seed, over its outer folds): if
    for a majority of outer folds no learning rate beats the training base rate's log loss, retry once
    with learning rate K4_RETRY_LR and K4_RETRY_EPOCHS epochs; if the retry also fails on a majority, keep
    the best grid point by inner-validation loss and flag it. Only inner-validation losses are used.
  * `transfer_steps`: step transfer. The selected step count becomes an epoch fraction of the
    three-fold training set; a model trained on a different number of rows trains for the same epoch
    fraction of its own training set (the cosine schedule is set to that length).
  * `inner_cross_fit`: the four inner adapters whose out-of-fold scores feed the isotonic map (7.3); the
    first inner split's selection adapter is reused when its validation scores were kept.
  * `RecipeTable`: the recorded mapping (fold seed, outer fold) -> recipe, saved as JSON so that the
    original suite, LiveCodeBench, and the base and trajectory checkpoints can reuse it.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping, Protocol, Sequence

import numpy as np

from pipeline.contracts import constants as K

from .common import Folds, base_rate_logloss, logloss_from_logodds, record_fit

B_EFF = K.LORA_EFFECTIVE_BATCH


def steps_per_epoch(n_rows: int) -> int:
    return max(1, math.ceil(n_rows / B_EFF))


def lr_at(step: int, base_lr: float, schedule_steps: int, warmup_fraction: float = K.LORA_WARMUP_FRACTION) -> float:
    """Learning rate for optimizer step `step` (0-based): linear warmup over warmup_fraction of the
    schedule (at least one step), then cosine decay to zero at the end of the schedule."""
    warm = max(1, int(round(warmup_fraction * schedule_steps)))
    if step < warm:
        return base_lr * (step + 1) / warm
    prog = (step - warm) / max(1, schedule_steps - warm)
    return base_lr * 0.5 * (1.0 + math.cos(math.pi * min(prog, 1.0)))


def transfer_steps(epoch_fraction: float, n_rows: int, max_steps: int | None = None) -> int:
    """Steps for a training set of n_rows that trains for `epoch_fraction` epochs of itself."""
    steps = max(1, int(round(epoch_fraction * n_rows / B_EFF)))
    return min(steps, max_steps) if max_steps else steps


def epoch_fraction_of(steps: int, n_rows: int) -> float:
    """The selected step count as a fraction of an epoch of the n_rows training set."""
    return steps * B_EFF / max(n_rows, 1)


@dataclass
class FitOutcome:
    curve: list[tuple[int, float]]                    # (step, validation log loss) at each evaluation
    val_scores: dict[int, np.ndarray] = field(default_factory=dict)    # step -> log-odds on eval_rows
    final_scores: dict[str, np.ndarray] = field(default_factory=dict)  # name -> log-odds at the last step
    steps_run: int = 0


class AdapterTrainer(Protocol):
    surrogate: bool

    def fit(self, train_rows: np.ndarray, y: np.ndarray, *, lr: float, total_steps: int, schedule_steps: int,
            eval_rows: np.ndarray | None = None, eval_every: int = K.LORA_EVAL_EVERY_STEPS,
            score_sets: Mapping[str, np.ndarray] | None = None, seed: int = 0,
            save_path: str | None = None) -> FitOutcome:
        """Train from scratch on `train_rows` (labels y[train_rows]) for `total_steps` optimizer steps under
        a cosine schedule of `schedule_steps` steps; evaluate on `eval_rows` every `eval_every` steps and at
        the last step (curve and val_scores); return the log-odds of each named row set at the last step."""


@dataclass
class Recipe:
    lr: float
    steps: int                       # selected step count on the three-fold inner training set
    n_train_inner: int               # rows of that training set
    epoch_fraction: float
    schedule_epochs: int             # 2, or 4 for the K4 retry
    inner_val_logloss: float
    base_rate_logloss: float
    retried: bool = False
    flagged: bool = False
    val_rows0: np.ndarray | None = None      # first inner split's validation rows (not serialized)
    val_scores0: np.ndarray | None = None    # its log-odds at the selected step (not serialized)

    def to_dict(self) -> dict:
        return {"lr": self.lr, "steps": self.steps, "n_train_inner": self.n_train_inner,
                "epoch_fraction": self.epoch_fraction, "schedule_epochs": self.schedule_epochs,
                "inner_val_logloss": self.inner_val_logloss, "base_rate_logloss": self.base_rate_logloss,
                "retried": self.retried, "flagged": self.flagged}

    @classmethod
    def from_dict(cls, d: Mapping) -> "Recipe":
        return cls(**{k: d[k] for k in ("lr", "steps", "n_train_inner", "epoch_fraction", "schedule_epochs",
                                         "inner_val_logloss", "base_rate_logloss", "retried", "flagged")})


class RecipeTable:
    """(fold seed, outer fold) -> Recipe, with JSON persistence."""

    def __init__(self, recipes: Mapping[tuple[int, int], Recipe] | None = None):
        self.recipes: dict[tuple[int, int], Recipe] = dict(recipes or {})

    def get(self, seed: int, fold: int) -> Recipe | None:
        return self.recipes.get((seed, fold))

    def put(self, seed: int, fold: int, r: Recipe) -> None:
        self.recipes[(seed, fold)] = r

    def has_seed(self, seed: int, folds: Sequence[int]) -> bool:
        return all((seed, f) in self.recipes for f in folds)

    def to_dict(self) -> dict:
        return {f"{s}:{f}": r.to_dict() for (s, f), r in sorted(self.recipes.items())}

    @classmethod
    def from_dict(cls, d: Mapping) -> "RecipeTable":
        out = {}
        for k, v in d.items():
            s, f = k.split(":")
            out[(int(s), int(f))] = Recipe.from_dict(v)
        return cls(out)

    def save(self, path: Path) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(self.to_dict(), indent=1, sort_keys=True) + "\n")

    @classmethod
    def load(cls, path: Path) -> "RecipeTable":
        return cls.from_dict(json.loads(Path(path).read_text()))


# ---------------------------------------------------------------------------------------------------
# Recipe selection with K4
# ---------------------------------------------------------------------------------------------------
@dataclass
class _GridPoint:
    lr: float
    step: int
    loss: float
    scores: np.ndarray


def _best_over_lrs(trainer: AdapterTrainer, F: Folds, f: int, lrs: Sequence[float], epochs: int, eval_every: int,
                   max_steps: int | None, seed: int) -> tuple[_GridPoint | None, float, int, int, np.ndarray, np.ndarray]:
    tr0, va0 = F.inner(f)[0]
    if len(tr0) == 0 or len(va0) == 0:
        return None, float("nan"), 0, 0, tr0, va0
    record_fit(f"adapter_select:outer{f}", F.problems_of(tr0))
    total = epochs * steps_per_epoch(len(tr0))
    if max_steps:
        total = min(total, max_steps)
    best: _GridPoint | None = None
    for lr in lrs:
        out = trainer.fit(tr0, F.y, lr=lr, total_steps=total, schedule_steps=total, eval_rows=va0,
                          eval_every=eval_every, seed=seed)
        if not out.curve:
            continue
        step, loss = min(out.curve, key=lambda sl: sl[1])  # first minimum
        if best is None or loss < best.loss:
            best = _GridPoint(lr, step, loss, out.val_scores[step])
    return best, base_rate_logloss(F.y[tr0], F.y[va0]), len(tr0), total, tr0, va0


def select_recipes(trainer: AdapterTrainer, F: Folds, *, lr_grid: Sequence[float] = K.LORA_LR_GRID,
                   max_epochs: int = K.LORA_MAX_EPOCHS, eval_every: int = K.LORA_EVAL_EVERY_STEPS,
                   max_steps: int | None = None) -> dict[int, Recipe]:
    """Select a recipe for every outer fold of F (one fit seed). See the module docstring for K4."""
    folds = F.outer_folds
    seed0 = F.plan.fold_seed * 1000
    grid = {f: _best_over_lrs(trainer, F, f, lr_grid, max_epochs, eval_every, max_steps, seed0 + f) for f in folds}

    def fails(res) -> bool:
        best, base = res[0], res[1]
        return best is None or not (best.loss < base)

    def majority(flags: list[bool]) -> bool:
        return sum(flags) * 2 > len(flags)

    use, retried, flagged = grid, False, False
    if folds and majority([fails(grid[f]) for f in folds]):
        retried = True
        retry = {f: _best_over_lrs(trainer, F, f, (K.K4_RETRY_LR,), K.K4_RETRY_EPOCHS, eval_every, max_steps,
                                   seed0 + 500 + f) for f in folds}
        if majority([fails(retry[f]) for f in folds]):
            flagged = True            # keep the best grid point by inner-validation loss
        else:
            use = retry
    out: dict[int, Recipe] = {}
    for f in folds:
        best, base, n3, total, tr0, va0 = use[f]
        if best is None:
            continue
        epochs = K.K4_RETRY_EPOCHS if use is not grid else max_epochs
        out[f] = Recipe(lr=best.lr, steps=best.step, n_train_inner=n3,
                        epoch_fraction=epoch_fraction_of(best.step, n3), schedule_epochs=epochs,
                        inner_val_logloss=best.loss, base_rate_logloss=base, retried=retried, flagged=flagged,
                        val_rows0=va0, val_scores0=best.scores)
    return out


# ---------------------------------------------------------------------------------------------------
# Final adapters and inner cross-fitting
# ---------------------------------------------------------------------------------------------------
def fit_final(trainer: AdapterTrainer, F: Folds, f: int, recipe: Recipe, *, max_steps: int | None = None,
              seed: int = 0, save_path: str | None = None, want_train: bool = True) -> tuple[FitOutcome, int, np.ndarray, np.ndarray, int]:
    """The four-fold adapter of outer fold f: epoch fraction of the recipe on its own training set.
    Returns (outcome with final_scores["test"] and ["train"], rows_test, rows_train, steps used)."""
    tr, te = F.outer_train(f), F.outer_test(f)
    record_fit(f"adapter_final:outer{f}", F.problems_of(tr))
    steps = transfer_steps(recipe.epoch_fraction, len(tr), max_steps)
    out = trainer.fit(tr, F.y, lr=recipe.lr, total_steps=steps, schedule_steps=steps,
                      score_sets={"test": te, "train": tr} if want_train else {"test": te}, seed=seed,
                      save_path=save_path)
    return out, te, tr, steps, len(tr)


def inner_cross_fit(trainer: AdapterTrainer, F: Folds, f: int, recipe: Recipe, *, reuse_split0: bool,
                    splits: Sequence[int] = (0, 1, 2, 3), max_steps: int | None = None, seed: int = 0
                    ) -> tuple[np.ndarray, np.ndarray]:
    """Inner cross-fitted log-odds for the training rows of outer fold f: for each inner split, the
    adapter trained with the recipe on three training folds scores the fourth. Split 0's selection
    adapter is reused when `reuse_split0` and its validation scores were kept on the recipe.
    Returns (rows, log-odds) over the union of the requested splits' validation rows."""
    rows, vals = [], []
    for j, (tr, va) in enumerate(F.inner(f)):
        if j not in splits or len(tr) == 0 or len(va) == 0:
            continue
        if j == 0 and reuse_split0 and recipe.val_scores0 is not None and recipe.val_rows0 is not None \
                and np.array_equal(recipe.val_rows0, va):
            rows.append(va)
            vals.append(np.asarray(recipe.val_scores0))
            continue
        record_fit(f"adapter_inner{j}:outer{f}", F.problems_of(tr))
        steps = transfer_steps(recipe.epoch_fraction, len(tr), max_steps)
        out = trainer.fit(tr, F.y, lr=recipe.lr, total_steps=steps, schedule_steps=steps,
                          score_sets={"val": va}, seed=seed + 10 * (j + 1))
        rows.append(va)
        vals.append(out.final_scores["val"])
    if not rows:
        return np.zeros(0, dtype=np.int64), np.zeros(0)
    return np.concatenate(rows), np.concatenate(vals)


def inner_val_loss_at(scores: np.ndarray, y: np.ndarray) -> float:
    return logloss_from_logodds(y, scores)
