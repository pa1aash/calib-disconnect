"""Offline tiny tokenizer, chat templates, and random models for the B3 tests (no downloads)."""

from __future__ import annotations

import torch
from tokenizers import AddedToken, Tokenizer, decoders, models, pre_tokenizers
from transformers import PreTrainedTokenizerFast, Qwen3Config, Qwen3ForCausalLM

from pipeline.contracts.hashing import sha256_text
from pipeline.contracts.schemas import GenerationRecord, Problem, sample_uid
from pipeline.generate.prompts import load_prompts, render_prompt

_TAIL = ("{% if add_generation_prompt %}<|im_start|>assistant\n"
         "{% if enable_thinking is defined and not enable_thinking %}<think>\n\n</think>\n\n{% endif %}{% endif %}")
T_PLAIN = ("{% for m in messages %}<|im_start|>{{ m['role'] }}\n{{ m['content'] }}<|im_end|>\n{% endfor %}" + _TAIL)
# No thinking logic: the full-conversation render reproduces prompt + completion + turn.
T_STABLE = ("{% for m in messages %}<|im_start|>{{ m['role'] }}\n{{ m['content'] }}<|im_end|>\n{% endfor %}"
            "{% if add_generation_prompt %}<|im_start|>assistant\n{% endif %}")
# Qwen3-like: assistant turns before the last user query lose the empty thought block.
T_REWRITE = ("{% set ns = namespace(last=-1) %}{% for m in messages %}{% if m['role'] == 'user' %}"
             "{% set ns.last = loop.index0 %}{% endif %}{% endfor %}"
             "{% for m in messages %}{% if m['role'] == 'assistant' and loop.index0 > ns.last %}"
             "<|im_start|>assistant\n<think>\n\n</think>\n\n{{ m['content'] }}<|im_end|>\n{% else %}"
             "<|im_start|>{{ m['role'] }}\n{{ m['content'] }}<|im_end|>\n{% endif %}{% endfor %}" + _TAIL)
# Default system turn and a leading BOS-like token when the caller gives no system turn.
T_SYSTEM = ("<|endoftext|>{% if messages[0]['role'] != 'system' %}<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n{% endif %}"
            + T_PLAIN)

SPECIALS = ["<|endoftext|>", "<|im_start|>", "<|im_end|>", "<pad>"]
WORDS = [" Yes", "Yes", "yes", "YES", "Yes!", " No", "No", "no", "\nNo", "Nope", "<think>", "</think>"]


def _bytes_to_unicode() -> dict[int, str]:
    bs = list(range(ord("!"), ord("~") + 1)) + list(range(0xA1, 0xAC + 1)) + list(range(0xAE, 0xFF + 1))
    cs, n = bs[:], 0
    for b in range(256):
        if b not in bs:
            bs.append(b)
            cs.append(256 + n)
            n += 1
    return dict(zip(bs, (chr(c) for c in cs)))


def build_tokenizer(template: str = T_PLAIN, words: list[str] | None = None) -> PreTrainedTokenizerFast:
    vocab = {ch: i for i, ch in enumerate(sorted(_bytes_to_unicode().values()))}
    tok = Tokenizer(models.BPE(vocab=vocab, merges=[]))
    tok.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    tok.decoder = decoders.ByteLevel()
    tok.add_special_tokens(SPECIALS)
    tok.add_tokens([AddedToken(w, normalized=False, special=False) for w in (WORDS if words is None else words)])
    return PreTrainedTokenizerFast(tokenizer_object=tok, eos_token="<|im_end|>", pad_token="<pad>",
                                   chat_template=template)


def build_model(tok, n_layers: int = 8, tie: bool = False, seed: int = 0) -> Qwen3ForCausalLM:
    cfg = Qwen3Config(vocab_size=len(tok), hidden_size=64, intermediate_size=128, num_hidden_layers=n_layers,
                      num_attention_heads=4, num_key_value_heads=2, head_dim=16, max_position_embeddings=2048,
                      tie_word_embeddings=tie, eos_token_id=tok.convert_tokens_to_ids("<|im_end|>"),
                      pad_token_id=tok.convert_tokens_to_ids("<pad>"))
    torch.manual_seed(seed)
    return Qwen3ForCausalLM(cfg).eval()


def problem(pid: str = "HumanEval/0") -> Problem:
    return Problem(problem_id=pid, benchmark="humaneval_plus",
                   prompt='def add(a, b):\n    """Add two numbers."""\n', entry_point="add",
                   canonical_solution="    return a + b\n", io_kind="function", release_date=None)


GOOD = "Here is the code.\n```python\ndef add(a, b):\n    return a + b\n```"
NOFENCE = "I cannot say how to do this."


def make_record(tok, prob: Problem, text: str, *, finish: str = "stop", thinking: bool = False, j: int = 1,
                chat: bool = True, ids: list[int] | None = None, add_stop: bool = True) -> GenerationRecord:
    prompts = load_prompts()
    ptext = prompts.generation_prompt_text(prob, base=not chat)
    rendered = render_prompt(tok, ptext, chat=chat, thinking=thinking)
    body = ids if ids is not None else tok(text, add_special_tokens=False)["input_ids"]
    if finish == "stop" and add_stop and chat:
        body = list(body) + [tok.convert_tokens_to_ids("<|im_end|>")]
    return GenerationRecord(
        sample_uid=sample_uid("SMOKE", prob.benchmark, prob.problem_id, j), model_key="SMOKE", model_id="t/t",
        revision="r", benchmark=prob.benchmark, problem_id=prob.problem_id, sample_index=j, generation_set="frozen",
        seed=j, prompt_sha256="x", rendered_prompt_sha256=rendered.sha256, completion_text=text,
        completion_token_ids=tuple(body), finish_reason=finish, truncated=finish == "length", engine="test",
        thinking=thinking)
