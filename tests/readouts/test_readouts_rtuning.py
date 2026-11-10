"""R-Tuning-style readout on a tiny model."""

import numpy as np
import pytest
import torch

from pipeline.readouts.masked_lora import LoraSpec, MaskedLoraModel
from pipeline.readouts.rtuning import (RTuningTokens, RTuningTrainer, build_sft_example, context_ids, score_rtuning,
                                       strip_eot)
from readouts_helpers import build_tiny, synth_layouts

pytestmark = pytest.mark.filterwarnings("ignore")
TOK = RTuningTokens(joiner_ids=(10,), am_ids=(11, 12), sure_ids=(13,), unsure_ids=(14, 15), eot_id=2)


def test_sft_example_layout_and_supervision():
    ids, sup = build_sft_example([3, 4], [5, 6, 2], True, TOK)
    assert ids == [3, 4, 5, 6, 10, 11, 12, 13, 2] and sup == [False, False] + [True] * 7
    ids, _ = build_sft_example([3, 4], [5, 6, 2], False, TOK)
    assert ids[-4:] == [12, 14, 15, 2]
    assert strip_eot([5, 2], 2) == [5] and context_ids([3], [5, 2], TOK) == [3, 5, 10, 11, 12]


def test_score_multi_token_continuation_matches_manual_logprobs():
    m = build_tiny("qwen3")
    seqs = [((3, 4, 5), (6, 7, 2)), ((8,), (9, 9, 9, 2))]
    got = score_rtuning(m, None, seqs, TOK, batch_size=1)
    for (p, c), g in zip(seqs, got):
        ctx = context_ids(p, c, TOK)
        def lp(cont):
            ids = torch.tensor([ctx + list(cont)])
            lg = torch.log_softmax(m(ids).logits[0], -1)
            return sum(lg[len(ctx) - 1 + i, t].item() for i, t in enumerate(cont))
        assert g.lp_sure == pytest.approx(lp(TOK.sure_ids), abs=1e-4)
        assert g.lp_unsure == pytest.approx(lp(TOK.unsure_ids), abs=1e-4)
        assert g.prob == pytest.approx(1 / (1 + np.exp(-(g.lp_sure - g.lp_unsure))), abs=1e-6)
        assert 0 < g.prob < 1
    # batching and padding do not change the scores
    again = score_rtuning(m, None, seqs, TOK, batch_size=8)
    assert [a.logit for a in again] == pytest.approx([a.logit for a in got], abs=1e-4)


def test_training_learns_the_sure_unsure_label_and_adapter_is_unmasked():
    lays, y = synth_layouts(32, seed=3)
    m = build_tiny("qwen3")
    ad = MaskedLoraModel(m, LoraSpec())
    tr = RTuningTrainer(ad, lays, TOK, micro_batch=8)
    rows = np.arange(24)
    before = tr.score(np.arange(24, 32))
    out = tr.fit(rows, y, lr=3e-3, total_steps=30, schedule_steps=30, score_sets={"test": np.arange(24, 32), "train": rows})
    tr_scores = out.final_scores["train"]
    assert tr_scores[y[rows] == 1].mean() > tr_scores[y[rows] == 0].mean()
    assert not np.allclose(before, out.final_scores["test"])
    ad.close()
