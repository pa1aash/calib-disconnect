"""Synthetic data and tiny in-memory models for the readouts tests (no weights are downloaded)."""

from __future__ import annotations

import numpy as np
import torch

from pipeline.contracts.interfaces import ReadoutData, TeacherForcedLayout
from pipeline.contracts.schemas import CaptureRecord, FoldPlan, HiddenStateRef

VOCAB = 50


# ---------------------------------------------------------------------------------------------------
# Tiny models, one per architecture class
# ---------------------------------------------------------------------------------------------------
def build_tiny(kind: str, seed: int = 0, sliding_window: int = 64):
    torch.manual_seed(seed)
    common = dict(vocab_size=VOCAB, hidden_size=64, intermediate_size=128, num_hidden_layers=2,
                  num_attention_heads=4, num_key_value_heads=2, max_position_embeddings=256,
                  bos_token_id=1, eos_token_id=2, pad_token_id=0)
    if kind == "qwen3":
        from transformers import Qwen3Config, Qwen3ForCausalLM
        m = Qwen3ForCausalLM(Qwen3Config(head_dim=16, **common))
    elif kind == "olmo3":
        from transformers import Olmo3Config, Olmo3ForCausalLM
        m = Olmo3ForCausalLM(Olmo3Config(**common))
    elif kind == "qwen2":
        from transformers import Qwen2Config, Qwen2ForCausalLM
        m = Qwen2ForCausalLM(Qwen2Config(**common))
    elif kind == "gemma4":
        from transformers.models.gemma4.configuration_gemma4 import Gemma4TextConfig
        from transformers.models.gemma4.modeling_gemma4 import Gemma4ForCausalLM
        common.update(head_dim=16, hidden_size_per_layer_input=16, vocab_size_per_layer_input=VOCAB,
                      sliding_window=sliding_window, global_head_dim=16)
        m = Gemma4ForCausalLM(Gemma4TextConfig(**common))
    else:
        raise ValueError(kind)
    return m.float().eval()


ARCHS = ("qwen3", "olmo3", "gemma4", "qwen2")


# ---------------------------------------------------------------------------------------------------
# Synthetic ReadoutData with a planted linear direction
# ---------------------------------------------------------------------------------------------------
def make_plan(problem_ids, seed: int = 0, n_folds: int = 5) -> FoldPlan:
    rng = np.random.default_rng(1000 + seed)
    pids = sorted(problem_ids)
    folds = np.arange(len(pids)) % n_folds
    rng.shuffle(folds)
    return FoldPlan(fold_seed=seed, population="label_validity", n_folds=n_folds,
                    assignment={p: int(f) for p, f in zip(pids, folds)})


def make_data(n_problems: int = 40, k: int = 4, d: int = 12, L: int = 3, seed: int = 0, v1_missing: float = 0.3,
              with_agreement: bool = True) -> ReadoutData:
    """Label depends on problem difficulty and a per-sample latent; hidden states at layer 1 (p2) carry the
    label along a planted direction; p1 carries the problem difficulty only."""
    rng = np.random.default_rng(seed)
    w = rng.normal(size=d)
    w /= np.linalg.norm(w)
    w2 = rng.normal(size=d)
    uids, pids, ys = [], [], []
    hs = {k_: [] for k_ in ("hs_p1", "hs_p2", "hs_p3", "hs_mean_code")}
    caps, lps, codes, agree = [], [], [], {}
    gain = [0.0, 2.5, 0.4][:L] + [0.0] * max(0, L - 3)
    for pi in range(n_problems):
        pid = f"HumanEval/{pi}"
        u = rng.normal()
        prompt_vec = rng.normal(size=(L, d)) + u * w2
        for j in range(1, k + 1):
            y = int(0.8 * u + rng.normal() > 0)
            sgn = 2 * y - 1
            uid = f"MOCK|frozen|humaneval_plus|{pid}|{j}"
            uids.append(uid)
            pids.append(pid)
            ys.append(y)
            hs["hs_p1"].append(prompt_vec.copy())
            hs["hs_p2"].append(rng.normal(size=(L, d)) + np.outer(gain, w) * sgn)
            hs["hs_p3"].append(rng.normal(size=(L, d)) + 0.3 * np.outer(gain, w) * sgn)
            hs["hs_mean_code"].append(rng.normal(size=(L, d)) + 0.2 * np.outer(gain, w) * sgn)
            n_tok = int(rng.integers(5, 15))
            lp = -np.abs(rng.normal(0.5 - 0.3 * y, 0.2, size=n_tok))
            lps.append(lp.astype(np.float32))
            v1 = None if rng.random() < v1_missing else float(np.clip(0.5 + 0.3 * sgn + rng.normal(0, 0.1), 0, 1))
            caps.append(CaptureRecord(
                sample_uid=uid, hidden=HiddenStateRef("capture/x.safetensors", len(caps), tuple(range(L))),
                n_code_tokens=n_tok, code_token_span=(5, 5 + n_tok), p1=4, p2=5 + n_tok, p3=5 + n_tok + 8,
                elicitation_span=(6 + n_tok, 6 + n_tok + 9),
                yes_no_logodds=float(np.float32(0.8 * sgn + rng.normal(0, 1.5))), v1_text="Confidence: 80",
                v1_value=v1, sum_logprob=float(lp.sum()), mean_logprob=float(lp.mean()), min_logprob=float(lp.min())))
            body = "return x + 1" if y else "return x - 1"
            codes.append(f"def f(x):\n    # note {j}\n    y = x\n    {body.replace('x', 'y', 1) if j % 2 else body}\n")
            agree[uid] = (str(y), "1.0000000001") if rng.random() < 0.8 else ("2", "3")
    data = ReadoutData(
        sample_uids=uids, problem_ids=pids, labels={"E": np.array(ys, dtype=np.int8), "O": np.array(ys, dtype=np.int8)},
        capture=caps, hidden={k_: np.stack(v).astype(np.float32) for k_, v in hs.items()}, code_texts=codes,
        code_logprobs=lps, agreement_outputs=agree if with_agreement else None,
        extraction_failed=np.zeros(len(uids), dtype=bool), truncated=np.zeros(len(uids), dtype=bool))
    return data


def synth_layouts(n: int, seed: int = 0, signal: bool = True):
    """Layouts and labels for the tiny LoRA model: the label is the parity of a marker token in the completion."""
    rng = np.random.default_rng(seed)
    lays, ys = [], []
    for i in range(n):
        y = int(rng.integers(0, 2))
        p = rng.integers(3, 20, size=int(rng.integers(3, 6))).tolist()
        c = rng.integers(3, 20, size=int(rng.integers(5, 10))).tolist()
        if signal:
            c[2] = 30 if y else 31
        e = [40, 41, 42, 43, 44]
        lays.append(TeacherForcedLayout(tuple(p), tuple(c), tuple(e), (len(p), len(p) + len(c))))
        ys.append(y)
    return lays, np.array(ys, dtype=np.int64)
