"""Cross-fitted adapter readouts: S^T (masked LoRA, 7.4), the capacity ladder and the head control
(7.11), S^R (R-Tuning-style, 7.5), and the mock-backend surrogate, all through one code path.

`AdapterReadout` takes an `AdapterTrainer` (real or surrogate) and a `RecipeTable`. With `select=True`
it first selects the recipe per outer fold on the first inner split (with K4, see `recipe.py`) and
records it in the table; otherwise it reuses the table's recipe for (fold seed, outer fold). Then, per
outer fold: the final adapter trains on the four training folds for the recipe's epoch fraction and
scores the test fold; its in-sample training-fold scores are kept; with `inner_adapters=True` the four
inner adapters give inner cross-fitted training-fold scores for the isotonic map (7.3).

Scores: rank_score = log-odds (float32 range), prob = sigmoid(rank_score), rank_tiebreak NaN.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np

from pipeline.contracts import constants as K
from pipeline.contracts.interfaces import ReadoutData
from pipeline.contracts.schemas import FitRecord, FoldPlan, ReadoutScore

from .common import Folds, fit_record, make_score, sigmoid
from .recipe import (AdapterTrainer, Recipe, RecipeTable, fit_final, inner_cross_fit, select_recipes)


@dataclass
class AdapterResult:
    scores: list[ReadoutScore] = field(default_factory=list)
    fits: list[FitRecord] = field(default_factory=list)
    inner_train_scores: dict[int, list[ReadoutScore]] = field(default_factory=dict)      # outer fold -> rows
    insample_train_scores: dict[int, list[ReadoutScore]] = field(default_factory=dict)   # outer fold -> rows
    recipes: dict[int, Recipe] = field(default_factory=dict)


class AdapterReadout:
    def __init__(self, name: str, trainer: AdapterTrainer, recipes: RecipeTable, *, select: bool = False,
                 inner_adapters: bool = False, keep_insample: bool = True, max_steps: int | None = None,
                 eval_every: int = K.LORA_EVAL_EVERY_STEPS, lr_grid=K.LORA_LR_GRID,
                 save_path_fn: Callable[[int, int, str], str | None] | None = None, extra_selected: dict | None = None):
        self.name = name
        self.trainer = trainer
        self.recipes = recipes
        self.select = select
        self.inner_adapters = inner_adapters
        self.max_steps = max_steps
        self.keep_insample = keep_insample
        self.eval_every = eval_every
        self.lr_grid = lr_grid
        self.save_path_fn = save_path_fn
        self.extra_selected = extra_selected or {}

    def crossfit(self, data: ReadoutData, plan: FoldPlan, label_suite: str, model_key: str, population: str):
        r = self.crossfit_full(data, plan, label_suite, model_key, population)
        return r.scores, r.fits

    def _rows(self, data, F: Folds, rows, z, model_key, population, label_suite, flagged):
        return [make_score(data, int(i), model_key=model_key, population=population, readout=self.name,
                           label_suite=label_suite, fold_seed=F.plan.fold_seed, fold=int(F.row_fold[i]),
                           prob=float(sigmoid(v)), rank_score=float(v), flagged=flagged)
                for i, v in zip(rows, z)]

    def crossfit_full(self, data: ReadoutData, plan: FoldPlan, label_suite: str, model_key: str,
                      population: str) -> AdapterResult:
        F = Folds(data, plan, label_suite)
        res = AdapterResult()
        seed = plan.fold_seed
        selected_here: dict[int, Recipe] = {}
        if self.select:
            selected_here = select_recipes(self.trainer, F, lr_grid=self.lr_grid, eval_every=self.eval_every,
                                           max_steps=self.max_steps)
            for f, rec in selected_here.items():
                self.recipes.put(seed, f, rec)
        for f in F.outer_folds:
            rec = self.recipes.get(seed, f)
            if rec is None:
                continue
            res.recipes[f] = rec
            save = self.save_path_fn(seed, f, label_suite) if self.save_path_fn else None
            out, te, tr, steps, n4 = fit_final(self.trainer, F, f, rec, max_steps=self.max_steps,
                                               seed=seed * 1000 + 100 + f, save_path=save, want_train=self.keep_insample)
            res.scores += self._rows(data, F, te, out.final_scores["test"], model_key, population, label_suite, rec.flagged)
            if self.keep_insample:
                res.insample_train_scores[f] = self._rows(data, F, tr, out.final_scores["train"], model_key,
                                                          population, label_suite, rec.flagged)
            if self.inner_adapters:
                rows, z = inner_cross_fit(self.trainer, F, f, rec, reuse_split0=self.select and f in selected_here,
                                          max_steps=self.max_steps, seed=seed * 1000 + 200 + f)
                res.inner_train_scores[f] = self._rows(data, F, rows, z, model_key, population, label_suite, rec.flagged)
            info = {"lr": rec.lr, "steps": rec.steps, "epoch_fraction": rec.epoch_fraction,
                    "schedule_epochs": rec.schedule_epochs, "n_train_inner": rec.n_train_inner,
                    "final_steps": steps, "n_train_final": n4,
                    "recipe_from": "selected here" if f in selected_here else "reused",
                    "inner_adapters": bool(self.inner_adapters),
                    "surrogate": bool(getattr(self.trainer, "surrogate", False)), **self.extra_selected}
            res.fits.append(fit_record(model_key, self.name, label_suite, plan, f, info, rec.inner_val_logloss,
                                       rec.base_rate_logloss, retried=rec.retried, flagged=rec.flagged))
        return res
