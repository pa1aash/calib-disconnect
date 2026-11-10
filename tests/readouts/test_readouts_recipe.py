"""Recipe selection, step transfer, K4 retry and flagging, inner adapters, and the LoRA pipeline on a tiny model."""

import numpy as np
import pytest

from pipeline.contracts import constants as K
from pipeline.contracts.interfaces import ReadoutData
from pipeline.readouts.adapter_readout import AdapterReadout
from pipeline.readouts.common import Folds
from pipeline.readouts.isotonic import crossfit_isotonic
from pipeline.readouts.recipe import (FitOutcome, RecipeTable, epoch_fraction_of, lr_at, select_recipes,
                                      steps_per_epoch, transfer_steps)
from readouts_helpers import make_data, make_plan

pytestmark = pytest.mark.filterwarnings("ignore")


def test_step_transfer_arithmetic():
    assert steps_per_epoch(4336) == 68            # the design's example
    frac = epoch_fraction_of(60, 3200)            # 60 steps of 64 rows on 3200 rows = 1.2 epochs
    assert frac == pytest.approx(1.2)
    assert transfer_steps(frac, 4000) == 75       # 1.2 epochs of 4000 rows
    assert transfer_steps(frac, 4000, max_steps=10) == 10
    assert transfer_steps(0.001, 100) == 1


def test_lr_schedule():
    S = 100
    lrs = [lr_at(s, 1e-3, S) for s in range(S)]
    assert lrs[0] == pytest.approx(1e-3 / 5) and lrs[4] == pytest.approx(1e-3)   # 5 percent warmup = 5 steps
    assert all(a >= b for a, b in zip(lrs[5:], lrs[6:])) and lrs[-1] < 1e-5


class Fake:
    """Trainer whose validation curve is set by the test; records calls."""
    surrogate = False

    def __init__(self, F, loss_fn):
        self.F, self.loss_fn, self.calls = F, loss_fn, []

    def fit(self, train_rows, y, *, lr, total_steps, schedule_steps, eval_rows=None, eval_every=20,
            score_sets=None, seed=0, save_path=None):
        self.calls.append(dict(lr=lr, total=total_steps, sched=schedule_steps, n=len(train_rows),
                               has_eval=eval_rows is not None, sets=sorted(score_sets or {})))
        out = FitOutcome(curve=[], steps_run=total_steps)
        if eval_rows is not None:
            fold = (set(range(5)) - set(self.F.row_fold[train_rows].tolist())
                    - set(self.F.row_fold[eval_rows].tolist())).pop()
            for s in sorted({t for t in range(1, total_steps + 1) if t % eval_every == 0} | {total_steps}):
                out.curve.append((s, self.loss_fn(fold, lr, total_steps, s)))
                out.val_scores[s] = np.full(len(eval_rows), float(s))
        for k, r in (score_sets or {}).items():
            out.final_scores[k] = np.zeros(len(r))
        return out


@pytest.fixture(scope="module")
def setup():
    d = make_data()
    plan = make_plan(set(d.problem_ids))
    return d, plan, Folds(d, plan, "E")


GOOD, BAD = 0.3, 5.0


def test_recipe_selection_picks_lr_and_step_by_inner_validation_loss(setup):
    d, plan, F = setup

    def loss(fold, lr, total, step):
        return (0.2 if lr == 1e-4 else 0.4) + abs(step - 2) * 0.01
    tr = Fake(F, loss)
    rec = select_recipes(tr, F, eval_every=1)
    assert set(rec) == set(range(5))
    for r in rec.values():
        assert r.lr == 1e-4 and r.steps == 2 and not r.retried and not r.flagged and r.schedule_epochs == 2
        assert r.inner_val_logloss == pytest.approx(0.2) and r.val_scores0[0] == 2.0
        assert r.epoch_fraction == pytest.approx(2 * 64 / r.n_train_inner)
    # three learning rates per fold, all on the first inner split, schedule = two epochs
    assert len(tr.calls) == 15 and {c["lr"] for c in tr.calls} == set(K.LORA_LR_GRID)
    assert all(c["total"] == c["sched"] == 2 * steps_per_epoch(c["n"]) for c in tr.calls)


def test_lora_max_steps_caps_selection_and_final(setup):
    d, plan, F = setup
    tr = Fake(F, lambda *a: GOOD)
    select_recipes(tr, F, eval_every=1, max_steps=3)
    assert all(c["total"] <= 3 for c in tr.calls)


def test_k4_minority_failure_does_not_retry(setup):
    d, plan, F = setup
    tr = Fake(F, lambda fold, lr, total, step: BAD if fold in (0, 1) else GOOD)
    rec = select_recipes(tr, F, eval_every=1)
    assert not any(r.retried or r.flagged for r in rec.values()) and len(tr.calls) == 15


def test_k4_majority_failure_retries_with_fixed_setting(setup):
    d, plan, F = setup

    def loss(fold, lr, total, step):
        return GOOD if lr == K.K4_RETRY_LR else BAD
    tr = Fake(F, loss)
    rec = select_recipes(tr, F, eval_every=1)
    retry_calls = [c for c in tr.calls if c["lr"] == K.K4_RETRY_LR]
    assert len(retry_calls) == 5 and all(c["total"] == K.K4_RETRY_EPOCHS * steps_per_epoch(c["n"]) for c in retry_calls)
    for r in rec.values():
        assert r.retried and not r.flagged and r.lr == 1e-3 and r.schedule_epochs == 4


def test_k4_failure_after_retry_keeps_best_grid_point_and_flags(setup):
    d, plan, F = setup

    def loss(fold, lr, total, step):
        return BAD + (0.5 if lr == K.K4_RETRY_LR else 0.0) + (0.0 if lr == 3e-4 else 0.1)
    rec = select_recipes(Fake(F, loss), F, eval_every=1)
    for r in rec.values():
        assert r.retried and r.flagged and r.lr == 3e-4 and r.schedule_epochs == 2

    # the flag reaches the FitRecords and the scores through the readout
    tr = Fake(F, loss)
    from pipeline.readouts.surrogate import SurrogateTrainer
    res = AdapterReadout("ST", Fake(F, loss), RecipeTable(), select=True).crossfit_full(d, plan, "E", "MOCK", "label_validity")
    assert all(f.flagged and f.retried for f in res.fits) and all(s.flagged for s in res.scores)
    del tr, SurrogateTrainer


def test_final_adapter_uses_step_transfer_and_inner_adapter_counts(setup):
    d, plan, F = setup
    tr = Fake(F, lambda fold, lr, total, step: GOOD + abs(step - 3) * 0.01)
    res = AdapterReadout("ST", tr, RecipeTable(), select=True, inner_adapters=True).crossfit_full(d, plan, "E", "MOCK", "label_validity")
    finals = [c for c in tr.calls if c["sets"] == ["test", "train"]]
    inner = [c for c in tr.calls if c["sets"] == ["val"]]
    assert len(finals) == 5 and len(inner) == 15            # split 1's selection adapter is reused: 3 inner adapters per fold
    for f, c in zip(range(5), finals):
        rec = res.recipes[f]
        assert c["total"] == c["sched"] == transfer_steps(rec.epoch_fraction, c["n"])
    assert len(res.inner_train_scores[0]) == len(F.outer_train(0))
    assert all(fit.selected["final_steps"] >= 1 and fit.selected["inner_adapters"] for fit in res.fits)
    # without selection (suite O reuses the recipe) all four inner adapters are trained
    tr2 = Fake(F, lambda *a: GOOD)
    table = RecipeTable({(0, f): r for f, r in res.recipes.items()})
    AdapterReadout("ST", tr2, table, inner_adapters=True).crossfit_full(d, plan, "O", "MOCK", "label_validity")
    assert len([c for c in tr2.calls if c["sets"] == ["val"]]) == 20 and not any(c["has_eval"] for c in tr2.calls)


def test_recipe_table_roundtrip(tmp_path, setup):
    d, plan, F = setup
    rec = select_recipes(Fake(F, lambda *a: GOOD), F, eval_every=1)
    t = RecipeTable({(0, f): r for f, r in rec.items()})
    t.save(tmp_path / "r.json")
    t2 = RecipeTable.load(tmp_path / "r.json")
    assert t2.get(0, 3).lr == t.get(0, 3).lr and t2.has_seed(0, range(5)) and not t2.has_seed(1, range(5))


def test_surrogate_pipeline_end_to_end_with_isotonic(setup):
    from pipeline.readouts.surrogate import SurrogateTrainer, surrogate_features
    d, plan, F = setup
    res = AdapterReadout("ST", SurrogateTrainer(surrogate_features(d)), RecipeTable(), select=True,
                         inner_adapters=True, eval_every=1).crossfit_full(d, plan, "E", "MOCK", "label_validity")
    assert len(res.scores) == len(d.sample_uids)
    assert all(f.selected["surrogate"] is True for f in res.fits)
    assert all(s.prob == pytest.approx(1 / (1 + np.exp(-s.rank_score))) for s in res.scores)
    iso = crossfit_isotonic(res.scores, d, plan, "E", res.inner_train_scores)
    assert len(iso) == len(res.scores) and iso[0].readout == "iso:ST"


def test_masked_lora_trainer_pipeline_on_tiny_model():
    """Real masked-LoRA training, recipe selection, inner adapters, and isotonic on a tiny Qwen3."""
    from pipeline.readouts.lora_train import MaskedLoraTrainer
    from pipeline.readouts.masked_lora import LoraSpec, MaskedLoraModel
    from readouts_helpers import build_tiny, synth_layouts
    lays, y = synth_layouts(100, seed=2)
    pids = [f"HumanEval/{i // 4}" for i in range(100)]
    d = ReadoutData(sample_uids=[f"MOCK|frozen|humaneval_plus|{p}|{i}" for i, p in enumerate(pids)], problem_ids=pids,
                    labels={"E": y.astype(np.int8)})
    plan = make_plan(set(pids))
    m = build_tiny("qwen3")
    ad = MaskedLoraModel(m, LoraSpec())
    tr = MaskedLoraTrainer(ad, lays, [1], [2], micro_batch=16)
    res = AdapterReadout("ST", tr, RecipeTable(), select=True, inner_adapters=True, max_steps=3,
                         eval_every=1).crossfit_full(d, plan, "E", "TINY", "label_validity")
    ad.close()
    assert len(res.scores) == 100 and len(res.fits) == 5
    assert all(f.selected["lr"] in K.LORA_LR_GRID and f.selected["final_steps"] <= 3 for f in res.fits)
    assert all(f.selected["surrogate"] is False for f in res.fits)
    assert all(np.isfinite(s.rank_score) for s in res.scores)
    iso = crossfit_isotonic(res.scores, d, plan, "E", res.inner_train_scores)
    assert len(iso) == 100


def test_masked_lora_training_reduces_loss():
    from pipeline.readouts.lora_train import MaskedLoraTrainer
    from pipeline.readouts.masked_lora import LoraSpec, MaskedLoraModel
    from readouts_helpers import build_tiny, synth_layouts
    lays, y = synth_layouts(64, seed=1)
    ad = MaskedLoraModel(build_tiny("olmo3"), LoraSpec())
    tr = MaskedLoraTrainer(ad, lays, [1], [2], micro_batch=16)
    ev = np.arange(48, 64)
    base = tr.fit(np.arange(48), y, lr=3e-3, total_steps=1, schedule_steps=40, eval_rows=ev, eval_every=1).curve[0][1]
    out = tr.fit(np.arange(48), y, lr=3e-3, total_steps=40, schedule_steps=40, eval_rows=ev, eval_every=10)
    assert out.curve[-1][1] < base - 0.05
    ad.close()
