"""Masked LoRA: the 7.12 mask unit test on four architectures, KV-cache identity, padded layout, and the
no-grad-prefix equivalence of loss and gradients."""

import numpy as np
import pytest
import torch

from pipeline.contracts import constants as K
from pipeline.readouts.masked_lora import (LoraSpec, MaskedLoraModel, bce_on_logodds, collate_layouts, find_decoder_layers,
                                           mask_unit_test, synthetic_layouts, target_module_names)
from readouts_helpers import ARCHS, VOCAB, build_tiny

pytestmark = pytest.mark.filterwarnings("ignore")
YES, NO = [1], [2]


@pytest.mark.parametrize("arch", ARCHS)
def test_mask_unit_test_on_each_architecture(arch):
    model = build_tiny(arch)
    layouts = synthetic_layouts(VOCAB, n=4, seed=1)
    rep = mask_unit_test(model, layouts)       # builds a nonzero adapter (B ~ N(0, 0.1))
    assert rep["atol"] == K.MASK_TEST_ATOL == 1e-3
    # (a) non-masked positions match the base model: hidden states of every layer and the KV cache
    assert rep["a_nonmasked_match"], rep
    assert rep["nonmasked_hidden_maxdiff"] <= 1e-3 and rep["nonmasked_kv_maxdiff"] <= 1e-3
    # (b) positive control: masked positions differ by more than the tolerance
    assert rep["b_masked_differ"] and rep["masked_last_hidden_maxdiff"] > 1e-3 and rep["masked_kv_maxdiff"] > 1e-3
    # economy path equals the full masked forward, and the prefix KV cache with the masked adapter attached equals the base's
    assert rep["c_economy_matches"], rep
    assert rep["prefix_cache_masked_vs_base_maxdiff"] <= 1e-3
    # negative control: the R-Tuning-style full adapter changes non-masked positions
    assert rep["d_negative_control_differs"] and rep["negative_control_nonmasked_hidden_maxdiff"] > 1e-3
    assert rep["passed"]
    assert rep["n_lora_layers"] == 14        # 7 projections x 2 layers
    # the adapter was removed again: the model is the base model
    assert not any("lora" in n for n, _ in model.named_parameters())


def test_mask_unit_test_with_sliding_window_cache_shorter_than_the_sequence():
    model = build_tiny("gemma4", sliding_window=8)
    rep = mask_unit_test(model, synthetic_layouts(VOCAB, n=3, seed=2, elic_len=3))
    assert rep["passed"], rep


def test_mask_unit_test_accepts_a_tokenizer_like_object():
    class Tok:
        vocab_size = VOCAB
    assert mask_unit_test(build_tiny("qwen3"), Tok())["passed"]


def test_mask_unit_test_detects_a_leaky_mask():
    """Control for the test itself: an adapter whose mask is 1 everywhere (mask hook broken) must fail (a)."""
    model = build_tiny("qwen3")
    ad = MaskedLoraModel(model, LoraSpec(), init_std=0.1)
    layouts = synthetic_layouts(VOCAB, n=3)
    orig = ad._hook
    ad._hook = lambda module, inputs, output: output     # drops the mask: the adapter acts on all positions
    for h in ad._handles:
        h.remove()
    ad._handles = [m.register_forward_hook(ad._hook) for m in ad._lora_b]
    rep = mask_unit_test(model, layouts, ad)
    ad._hook = orig
    assert not rep["a_nonmasked_match"] and not rep["passed"]
    ad.close()


def test_target_modules_are_all_attention_and_mlp_projections():
    for arch in ARCHS:
        m = build_tiny(arch)
        names = target_module_names(m)
        prefix, layers = find_decoder_layers(m)
        assert prefix == "model.layers" and len(layers) == 2
        leaves = {n.rsplit(".", 1)[-1] for n in names}
        assert leaves == {"q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"}
        assert len(names) == 14
        assert not any("per_layer" in n for n in names)


def test_adapter_uses_the_design_lora_settings():
    spec = LoraSpec()
    assert (spec.rank, spec.alpha, spec.dropout) == (K.LORA_RANK, K.LORA_ALPHA, K.LORA_DROPOUT) == (16, 32, 0.05)
    assert LoraSpec.ladder(4).alpha == 8
    m = build_tiny("qwen3")
    ad = MaskedLoraModel(m, spec)
    cfg = ad.peft.peft_config["default"]
    assert cfg.r == 16 and cfg.lora_alpha == 32 and cfg.lora_dropout == 0.05 and cfg.bias == "none"
    ad.close()


def test_zero_initialized_adapter_equals_base_everywhere():
    m = build_tiny("qwen2")
    lays = synthetic_layouts(VOCAB, n=3)
    b = collate_layouts(lays)
    ad = MaskedLoraModel(m, LoraSpec())      # B = 0
    with torch.no_grad():
        z_on = ad.logodds(b, YES, NO, economy=False)
        z_off = ad.logodds_from_state(ad.forward_full(b, "off").last_hidden_state[:, -1], YES, NO)
    assert torch.allclose(z_on, z_off, atol=1e-6)
    ad.close()


def test_padded_batch_equals_unpadded_rows():
    m = build_tiny("qwen3")
    ad = MaskedLoraModel(m, LoraSpec(dropout=0.0), init_std=0.1)
    ad.eval()
    lays = synthetic_layouts(VOCAB, n=4, seed=3)
    with torch.no_grad():
        zb = ad.logodds(collate_layouts(lays), YES, NO)
        zs = torch.cat([ad.logodds(collate_layouts([l]), YES, NO) for l in lays])
    assert torch.allclose(zb, zs, atol=1e-5)
    ad.close()


def test_close_restores_base_outputs():
    m = build_tiny("olmo3")
    b = collate_layouts(synthetic_layouts(VOCAB, n=2))
    with torch.no_grad():
        before = m.model(input_ids=b.input_ids, attention_mask=b.attention_mask, position_ids=b.position_ids).last_hidden_state
    ad = MaskedLoraModel(m, LoraSpec(), init_std=0.1)
    ad.close()
    with torch.no_grad():
        after = m.model(input_ids=b.input_ids, attention_mask=b.attention_mask, position_ids=b.position_ids).last_hidden_state
    assert torch.equal(before, after)


@pytest.mark.parametrize("arch", ARCHS)
@pytest.mark.parametrize("head", [False, True])
def test_no_grad_prefix_gives_the_same_loss_and_gradients(arch, head):
    """The 12.5 economy: prefix under no_grad with its KV cache reused equals the full masked forward."""
    m = build_tiny(arch)
    ad = MaskedLoraModel(m, LoraSpec(dropout=0.0), init_std=0.05, seed=3)
    if head:
        ad.add_head()
        torch.nn.init.normal_(ad.head.weight, std=0.1)
    ad.train()
    lays = synthetic_layouts(VOCAB, n=5, seed=4)
    batch = collate_layouts(lays, y=np.array([0, 1, 1, 0, 1]))
    grads = {}
    losses = {}
    for economy in (False, True):
        for p in ad.trainable_parameters():
            p.grad = None
        z = ad.head_logit(batch, economy=economy) if head else ad.logodds(batch, YES, NO, economy=economy)
        loss = bce_on_logodds(z, batch.y)
        loss.backward()
        losses[economy] = loss.item()
        grads[economy] = [p.grad.clone() for p in ad.trainable_parameters()]
    assert losses[True] == pytest.approx(losses[False], abs=1e-6)
    gmax = max(g.abs().max().item() for g in grads[False])
    assert gmax > 1e-6      # non-trivial gradients
    for gf, ge in zip(grads[False], grads[True]):
        assert torch.allclose(gf, ge, atol=1e-6 + 1e-4 * gmax)
    ad.close()


def test_economy_prefix_runs_without_grad_and_no_prefix_state_requires_grad():
    m = build_tiny("qwen3")
    ad = MaskedLoraModel(m, LoraSpec(dropout=0.0), init_std=0.05)
    batch = collate_layouts(synthetic_layouts(VOCAB, n=3, seed=5))
    h = ad.final_state(batch, economy=True)
    assert h.requires_grad
    # base parameters never receive gradients
    h.sum().backward()
    assert all(p.grad is None for n, p in m.named_parameters() if "lora_" not in n)
    ad.close()


def test_yes_no_logodds_is_float32_and_matches_manual_head():
    m = build_tiny("gemma4").to(torch.float32)
    ad = MaskedLoraModel(m, LoraSpec(), init_std=0.05)
    batch = collate_layouts(synthetic_layouts(VOCAB, n=3))
    with torch.no_grad():
        h = ad.final_state(batch, economy=True)
        z = ad.logodds_from_state(h, [1, 5], [2, 6])
        logits = (h @ m.get_output_embeddings().weight.float().T)
        cap = m.config.get_text_config().final_logit_softcapping
        if cap:
            logits = torch.tanh(logits / cap) * cap
        lp = torch.log_softmax(logits, -1)
        manual = torch.logsumexp(lp[:, [1, 5]], -1) - torch.logsumexp(lp[:, [2, 6]], -1)
    assert z.dtype == torch.float32 and torch.allclose(z, manual, atol=1e-5)
    ad.close()
