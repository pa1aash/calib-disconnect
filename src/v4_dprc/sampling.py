"""Generation backends behind a small interface, so the labeling pipeline is testable off-GPU.

  Generator.generate(prompts, n) -> list[list[str]]     # n completions per prompt (code strings)

  VLLMGenerator  — real, batched, GPU (lazy-imports vllm; reuse of exp1_vllm.py settings).
  StubGenerator  — deterministic, CPU; returns canonical solution + perturbations, so the full
                   label pipeline can be dry-run locally before the box exists.
"""
from __future__ import annotations
import os
import re
import config


def build_prompt(problem) -> str:
    """Instruction prompt. IO-style -> stdin/stdout program. Call-style -> complete-the-function,
    showing sample asserts so the model uses the REQUIRED function name (MBPP's name lives only in
    its tests, not the description — standard MBPP eval convention)."""
    if problem.style == "io":
        return ("Write a complete Python program that reads from standard input and writes the answer "
                "to standard output.\n\n" + problem.prompt + "\n\n# Solution:\n")
    asserts = [u.assertion for u in getattr(problem, "units", [])
               if getattr(u, "assertion", "").strip().startswith("assert")][:3]
    tests = ("\nYour code must pass these tests:\n" + "\n".join(asserts) + "\n") if asserts else ""
    return ("Complete the following Python function. Only output the complete function, "
            "no explanations.\n\n" + problem.prompt + tests)


_FENCE = re.compile(r"```(?:python)?\s*(.*?)```", re.DOTALL)


def clean_code(text: str, problem=None) -> str:
    """Fenced block if present, else drop prose before the first code line. Never prepend the prompt
    (instruct models emit full functions; prepending NL prompts breaks execution).
    # ponytail: if HumanEval solutions fail on a missing `from typing import List`, prepend that
    #           stub import — until the pilot shows it, YAGNI."""
    m = _FENCE.search(text)
    code = m.group(1) if m else text
    lines = code.splitlines()
    for i, ln in enumerate(lines):
        if re.match(r"^\s*(def |class |import |from |@)", ln):
            return "\n".join(lines[i:]).strip() + "\n"
    return code.strip() + "\n"


class VLLMGenerator:
    """GPU backend. Mirrors exp1_vllm.py: bf16, top_p, temperature, n. Lazy import so this module
    loads without vllm/torch installed (local dev)."""
    def __init__(self, model_key: str = config.PRIMARY_MODEL, gpu_mem_util: float | None = None,
                 max_model_len: int = 4096):
        from vllm import LLM
        from transformers import AutoTokenizer
        # ponytail: default 0.9 (dedicated GPU / released code). On a SHARED GPU set VLLM_GPU_MEM
        #           (e.g. 0.35) to fit alongside another container -> no source edits per session.
        if gpu_mem_util is None:
            gpu_mem_util = float(os.environ.get("VLLM_GPU_MEM", "0.9"))
        self.model_id = config.MODELS[model_key]
        self.llm = LLM(model=self.model_id, dtype="bfloat16", max_model_len=max_model_len,
                       gpu_memory_utilization=gpu_mem_util, trust_remote_code=True)
        # instruct models need the chat template; raw prompts make them ramble (prose/test-harness
        # instead of the function) -> ~1% pass. Mirror HFGenerator's apply_chat_template.
        self.tok = AutoTokenizer.from_pretrained(self.model_id, trust_remote_code=True)

    def generate(self, prompts: list[str], n: int, temperature: float = config.TEMPERATURE,
                 top_p: float = config.TOP_P, max_tokens: int = config.MAX_NEW_TOKENS) -> list[list[str]]:
        from vllm import SamplingParams
        chat = []
        for p in prompts:
            try:
                chat.append(self.tok.apply_chat_template([{"role": "user", "content": p}],
                                                         tokenize=False, add_generation_prompt=True))
            except Exception:
                chat.append(p)
        sp = SamplingParams(n=n, temperature=temperature, top_p=top_p, max_tokens=max_tokens, seed=config.SEED)
        outs = self.llm.generate(chat, sp)
        return [[o.text for o in out.outputs] for out in outs]


class HFGenerator:
    """Transformers `model.generate` backend. Slower than vLLM but has no vLLM/CUDA-wheel matching
    issues (works with any CUDA-matched torch). Fine for the pilot; usable for the full run if vLLM
    can't be pinned to the pod's CUDA. Batches n via num_return_sequences per prompt."""
    def __init__(self, model_key: str = config.PRIMARY_MODEL, batch_size: int = 8):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.model_id = config.MODELS[model_key]
        self.tok = AutoTokenizer.from_pretrained(self.model_id, trust_remote_code=True)
        if self.tok.pad_token is None:
            self.tok.pad_token = self.tok.eos_token
        self.tok.padding_side = "left"          # left-pad so completions start at a common offset
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
        self.model.eval()
        self._torch = torch
        self.batch_size = batch_size

    def generate(self, prompts: list[str], n: int, temperature: float = config.TEMPERATURE,
                 top_p: float = config.TOP_P, max_tokens: int = config.MAX_NEW_TOKENS) -> list[list[str]]:
        torch = self._torch
        texts = []
        for p in prompts:
            try:
                texts.append(self.tok.apply_chat_template([{"role": "user", "content": p}],
                                                          tokenize=False, add_generation_prompt=True))
            except Exception:
                texts.append(p)
        out = []
        for i in range(0, len(texts), self.batch_size):     # batch prompts through one forward pass
            batch = texts[i:i + self.batch_size]
            enc = self.tok(batch, return_tensors="pt", padding=True).to(self.model.device)
            with torch.no_grad():
                gen = self.model.generate(**enc, do_sample=True, temperature=temperature, top_p=top_p,
                                          max_new_tokens=max_tokens, num_return_sequences=n,
                                          pad_token_id=self.tok.pad_token_id)
            plen = enc["input_ids"].shape[1]
            comp = gen[:, plen:]                             # [len(batch)*n, new_tokens]
            for b in range(len(batch)):
                seqs = comp[b * n:(b + 1) * n]
                out.append([self.tok.decode(s, skip_special_tokens=True) for s in seqs])
        return out


class StubGenerator:
    """CPU backend for local dry-runs. Deterministic. Requires each problem to carry a
    `canonical_solution`; returns it for most samples and a perturbed (buggy) variant for a couple,
    so the per-test matrix is non-degenerate and GATE-1 spread is exercised."""
    def __init__(self, problems_by_prompt: dict):
        self._by_prompt = problems_by_prompt

    def generate(self, prompts: list[str], n: int, **kw) -> list[list[str]]:
        out = []
        for p in prompts:
            prob = self._by_prompt[p]
            canon = prob.canonical_solution or (prob.prompt + "    pass\n")
            samples = []
            for k in range(n):
                if k % 4 == 3:                       # ~1/4 buggy: append an off-by-one so edge tests fail
                    samples.append(_perturb(canon))
                else:
                    samples.append(canon)
            out.append(samples)
        return out


def _perturb(code: str) -> str:
    """A crude deterministic 'bug': wrap returns so empty/zero cases differ. Enough to break some tests."""
    return code.replace("return sum(", "return 1 + sum(") if "return sum(" in code else code + "\n# noop\n"


if __name__ == "__main__":  # ponytail: smallest check that fails if extraction breaks
    assert clean_code("Sure! Here it is:\ndef f(x):\n    return x+1\n").strip() == "def f(x):\n    return x+1"
    assert clean_code("```python\nfrom math import pi\ndef g(): return pi\n```").startswith("from math import pi")
    print("clean_code ok")
