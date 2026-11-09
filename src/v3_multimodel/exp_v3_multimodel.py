"""
DL4C V3: Multi-model experiments + SFT evaluation + n=20 sensitivity.

Addresses the key gaps in the v2 paper:
1. Second model (DeepSeek-Coder-V2-Lite-Instruct) to show generalizability
2. Quantitative SFT evaluation with bootstrap CIs
3. Complete n=20 sensitivity analysis
4. Cross-model comparison summary

Run on GH200 (98GB VRAM, bf16):
  PYTHONUNBUFFERED=1 nohup python3 -u exp_v3_multimodel.py > v3_log.txt 2>&1 &
"""

import json, os, time, re, subprocess, tempfile, gc, sys
import numpy as np
import torch
from math import comb
from collections import Counter

RESULTS_DIR = "/home/ubuntu/dl4c_experiments/results_v3"
MODEL_DIR = "/home/ubuntu/dl4c_experiments/models"
os.makedirs(RESULTS_DIR, exist_ok=True)

MAX_TOKENS = 512

# Models to evaluate
MODELS = {
    "qwen2.5-coder-7b": "Qwen/Qwen2.5-Coder-7B-Instruct",
    "deepseek-coder-v2-lite": "deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct",
}

# SFT model (LoRA adapter on Qwen)
SFT_ADAPTER = os.path.join(MODEL_DIR, "qwen_confidence_sft")


# ==================== METRICS ====================

def compute_ece(c, a, n_bins=10):
    c, a = np.array(c, dtype=float), np.array(a, dtype=float)
    bounds = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    bins = []
    for i in range(n_bins):
        if i < n_bins - 1:
            m = (c >= bounds[i]) & (c < bounds[i + 1])
        else:
            m = (c >= bounds[i]) & (c <= bounds[i + 1])
        if m.sum() > 0:
            ba = float(a[m].mean())
            bc = float(c[m].mean())
            bs = int(m.sum())
            ece += (bs / len(c)) * abs(ba - bc)
            bins.append({"lo": float(bounds[i]), "hi": float(bounds[i + 1]),
                         "acc": ba, "conf": bc, "n": bs})
    return float(ece), bins


def compute_brier(c, a):
    return float(np.mean((np.array(c) - np.array(a)) ** 2))


def compute_auroc(c, a):
    from sklearn.metrics import roc_auc_score
    c, a = np.array(c), np.array(a)
    if len(np.unique(a)) < 2:
        return float('nan')
    return float(roc_auc_score(a, c))


def bootstrap_metric(metric_fn, c, a, n_boot=1000, seed=42):
    rng = np.random.RandomState(seed)
    c, a = np.array(c), np.array(a)
    vals = []
    for _ in range(n_boot):
        idx = rng.randint(0, len(c), len(c))
        try:
            v = metric_fn(c[idx], a[idx])
            if not np.isnan(v):
                vals.append(v)
        except:
            pass
    if not vals:
        return float('nan'), float('nan'), float('nan')
    vals = sorted(vals)
    return (float(np.mean(vals)),
            float(vals[int(0.025 * len(vals))]),
            float(vals[int(0.975 * len(vals))]))


def bootstrap_all(c, a, n_boot=1000):
    ece_fn = lambda c, a: compute_ece(c, a)[0]
    ece_mean, ece_lo, ece_hi = bootstrap_metric(ece_fn, c, a, n_boot)
    brier_mean, brier_lo, brier_hi = bootstrap_metric(compute_brier, c, a, n_boot)
    auroc_mean, auroc_lo, auroc_hi = bootstrap_metric(compute_auroc, c, a, n_boot)
    return {
        "ece": ece_mean, "ece_ci": [ece_lo, ece_hi],
        "brier": brier_mean, "brier_ci": [brier_lo, brier_hi],
        "auroc": auroc_mean, "auroc_ci": [auroc_lo, auroc_hi],
    }


# ==================== EXECUTION ====================

def _run_code(code, timeout=10):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        f.flush()
        try:
            result = subprocess.run(['python3', f.name], capture_output=True,
                                    text=True, timeout=timeout)
            return result.returncode == 0
        except:
            return False
        finally:
            os.unlink(f.name)


def execute_humaneval(code, prob):
    full_code = code if prob["prompt"] in code else prob["prompt"] + code
    test_code = prob["test"] + f"\ncheck({prob['entry_point']})"
    return _run_code(full_code + "\n" + test_code)


def execute_mbpp_fixed(code, prob):
    test_lines = prob["test"]
    ok = _run_code(code + "\n" + test_lines)
    if ok:
        return True
    func_match = re.search(r'assert\s+(\w+)\s*\(', test_lines)
    if func_match:
        expected_fn = func_match.group(1)
        if f"def {expected_fn}" not in code:
            def_match = re.search(r'def\s+(\w+)\s*\(', code)
            if def_match:
                actual_fn = def_match.group(1)
                aliased = code + f"\n{expected_fn} = {actual_fn}\n"
                return _run_code(aliased + "\n" + test_lines)
    return False


def extract_code(resp):
    blocks = re.findall(r'```(?:python)?\n?(.*?)```', resp, re.DOTALL)
    if blocks:
        return blocks[0].strip()
    lines = resp.split('\n')
    code_lines = []
    in_code = False
    for line in lines:
        if line.strip().startswith('def ') or line.strip().startswith('class ') or in_code:
            in_code = True
            code_lines.append(line)
        elif in_code and line.strip() == '':
            code_lines.append(line)
        elif in_code and not line.startswith(' ') and not line.startswith('\t') and line.strip():
            break
    return '\n'.join(code_lines).strip() if code_lines else resp.strip()


def extract_numeric_conf(resp):
    m = re.search(r'CONFIDENCE:\s*(\d)', resp)
    if m:
        return min(max(int(m.group(1)), 1), 5) / 5.0
    m = re.search(r'(\d)\s*/\s*5', resp)
    if m:
        return int(m.group(1)) / 5.0
    rl = resp.lower()
    if 'very confident' in rl or '5/5' in rl:
        return 1.0
    if 'quite confident' in rl or ('confident' in rl and 'not' not in rl):
        return 0.8
    if 'moderately' in rl or 'should work' in rl or 'fairly' in rl:
        return 0.6
    if 'somewhat' in rl or 'unsure' in rl:
        return 0.4
    if 'not confident' in rl or 'unlikely' in rl:
        return 0.2
    return 0.6


def extract_trained_conf(resp):
    rl = resp.lower()
    if 'i am confident this solution is correct' in rl:
        return 0.9
    if 'should work for most cases' in rl or 'please verify' in rl:
        return 0.6
    if 'not confident' in rl or 'may contain bugs' in rl:
        return 0.3
    return extract_numeric_conf(resp)


# ==================== GENERATION ====================

@torch.no_grad()
def gen(model, tokenizer, prompt, n=1, temp=0.8):
    ids = tokenizer(prompt, return_tensors="pt", truncation=True,
                    max_length=2048).input_ids.to(model.device)
    results = []
    for _ in range(n):
        try:
            out = model.generate(
                ids, max_new_tokens=MAX_TOKENS,
                temperature=max(temp, 0.01),
                top_p=0.95, do_sample=True,
                pad_token_id=tokenizer.pad_token_id
            )
            results.append(tokenizer.decode(out[0][ids.shape[1]:],
                                            skip_special_tokens=True))
        except Exception as e:
            print(f"    gen error: {e}", flush=True)
            results.append("")
    return results


@torch.no_grad()
def gen_with_logprobs(model, tokenizer, prompt, temp=0.8):
    ids = tokenizer(prompt, return_tensors="pt", truncation=True,
                    max_length=2048).input_ids.to(model.device)
    out = model.generate(
        ids, max_new_tokens=MAX_TOKENS,
        temperature=max(temp, 0.01),
        top_p=0.95, do_sample=True,
        pad_token_id=tokenizer.pad_token_id
    )
    gen_ids = out[0][ids.shape[1]:]
    text = tokenizer.decode(gen_ids, skip_special_tokens=True)

    # Forward pass to get log probs
    logits = model(out).logits[0]
    gen_logits = logits[ids.shape[1] - 1:-1]
    log_probs = torch.log_softmax(gen_logits, dim=-1)
    actual_ids = gen_ids[:len(gen_logits)]
    token_log_probs = log_probs[torch.arange(len(actual_ids)), actual_ids]
    mean_lp = token_log_probs.mean().item()
    confidence = 1.0 / (1.0 + np.exp(-mean_lp))  # sigmoid transform

    return text, float(confidence)


def fmt(tokenizer, msgs):
    try:
        return tokenizer.apply_chat_template(msgs, tokenize=False,
                                              add_generation_prompt=True)
    except:
        return msgs[-1]["content"]


# ==================== DATA ====================

def load_humaneval():
    from datasets import load_dataset
    ds = load_dataset("openai_humaneval", split="test")
    return [{"task_id": i["task_id"], "prompt": i["prompt"],
             "canonical_solution": i["canonical_solution"],
             "test": i["test"], "entry_point": i["entry_point"]} for i in ds]


def load_mbpp():
    from datasets import load_dataset
    ds = load_dataset("google-research-datasets/mbpp", "sanitized", split="test")
    return [{"task_id": f"mbpp_{i['task_id']}", "prompt": i["prompt"],
             "test": "\n".join(i["test_list"]), "code": i["code"]} for i in ds]


# ==================== PROMPTS ====================

PROMPT_DIRECT = "Complete the following Python function. Only output the complete function, no explanations.\n\n{}"
PROMPT_MBPP = "Write a Python function to solve: {}\nOnly output the function, no explanations."

PROMPT_NUMERIC = "Rate your confidence from 1-5 (1=very unsure, 5=very confident) that your solution is correct. Format: CONFIDENCE: [N]\nThen provide the solution.\n\n{}"

PROMPT_CRITIQUE = """Before solving, briefly critique the problem for potential pitfalls (edge cases, tricky constraints). Then rate your confidence 1-5 that you can solve it correctly. Format: CONFIDENCE: [N]
Then provide the solution.

{}"""

PROMPT_COT = """Think step by step about how to solve this problem. Consider edge cases and potential bugs. After your reasoning, rate confidence 1-5. Format: CONFIDENCE: [N]
Then provide the solution.

{}"""

PROMPT_SFT = """Before providing your solution, state your confidence:
- 'I am confident this solution is correct' for high confidence
- 'This should work for most cases, but please verify edge cases' for medium confidence
- 'I am not confident in this solution, it may contain bugs' for low confidence
Then provide the complete Python solution.

{}"""


# ==================== CORE EXPERIMENT ====================

def run_experiment(model, tokenizer, problems, is_humaneval, bench_name,
                   n_samples=10, temperature=0.8, methods=None):
    """
    Run confidence methods on problems.
    methods: list of method names to run. Default = all 5.
    """
    if methods is None:
        methods = ["sampling", "logprob", "verbal_numeric", "verbal_critique", "verbal_cot"]

    print(f"\n  === {bench_name} (n={len(problems)}, samples={n_samples}, "
          f"tau={temperature}, methods={methods}) ===", flush=True)
    t0 = time.time()

    data = []
    latency_per_sample = []

    for idx, prob in enumerate(problems):
        if idx % 20 == 0:
            print(f"    [{idx}/{len(problems)}] ({time.time()-t0:.0f}s)", flush=True)

        prompt = prob["prompt"]
        entry = {"task_id": prob.get("task_id", f"{bench_name}_{idx}")}

        # ---- Sampling confidence ----
        if "sampling" in methods:
            gen_prompt = PROMPT_DIRECT.format(prompt) if is_humaneval else PROMPT_MBPP.format(prompt)
            pi = fmt(tokenizer, [{"role": "user", "content": gen_prompt}])

            t_gen_start = time.time()
            samples = gen(model, tokenizer, pi, n_samples, temp=temperature)
            t_gen_end = time.time()
            latency_per_sample.append((t_gen_end - t_gen_start) / n_samples)

            sample_results = []
            for s in samples:
                code = extract_code(s)
                ok = execute_humaneval(code, prob) if is_humaneval else execute_mbpp_fixed(code, prob)
                sample_results.append({"correct": ok})

            pass_count = sum(1 for s in sample_results if s["correct"])
            entry["sampling_conf"] = pass_count / len(sample_results)
            entry["first_correct"] = sample_results[0]["correct"]
            entry["pass_count"] = pass_count
            entry["n_samples"] = n_samples

        # ---- Log-probability confidence ----
        if "logprob" in methods:
            gen_prompt = PROMPT_DIRECT.format(prompt) if is_humaneval else PROMPT_MBPP.format(prompt)
            pi = fmt(tokenizer, [{"role": "user", "content": gen_prompt}])
            try:
                _, logprob_conf = gen_with_logprobs(model, tokenizer, pi, temp=temperature)
            except:
                logprob_conf = 0.5
            entry["logprob_conf"] = logprob_conf

        # ---- Verbal: numeric ----
        if "verbal_numeric" in methods:
            ci = fmt(tokenizer, [{"role": "user", "content": PROMPT_NUMERIC.format(prompt)}])
            resp = gen(model, tokenizer, ci, 1, temp=0.1)[0]
            entry["conf_numeric"] = extract_numeric_conf(resp)
            entry["resp_numeric_preview"] = resp[:200]

        # ---- Verbal: critique-then-rate ----
        if "verbal_critique" in methods:
            ci = fmt(tokenizer, [{"role": "user", "content": PROMPT_CRITIQUE.format(prompt)}])
            resp = gen(model, tokenizer, ci, 1, temp=0.1)[0]
            entry["conf_critique"] = extract_numeric_conf(resp)

        # ---- Verbal: CoT ----
        if "verbal_cot" in methods:
            ci = fmt(tokenizer, [{"role": "user", "content": PROMPT_COT.format(prompt)}])
            resp = gen(model, tokenizer, ci, 1, temp=0.1)[0]
            entry["conf_cot"] = extract_numeric_conf(resp)

        data.append(entry)

    elapsed = time.time() - t0

    # ---- Compute metrics ----
    labels = [d["first_correct"] for d in data]

    results = {
        "benchmark": bench_name,
        "n_problems": len(problems),
        "n_samples": n_samples,
        "temperature": temperature,
        "time_seconds": elapsed,
        "pass_at_1": float(np.mean(labels)),
    }

    if latency_per_sample:
        results["mean_latency_per_sample_s"] = float(np.mean(latency_per_sample))
        results["total_latency_n_samples_s"] = float(np.mean(latency_per_sample) * n_samples)

    # pass@10
    if n_samples >= 10:
        p10 = []
        for d in data:
            n, c = d["n_samples"], d["pass_count"]
            k = min(10, n)
            p10.append(1.0 if n - c < k else 1.0 - comb(n - c, k) / comb(n, k))
        results["pass_at_10"] = float(np.mean(p10))

    # Per-method metrics
    method_conf_keys = {
        "sampling": "sampling_conf",
        "logprob": "logprob_conf",
        "verbal_numeric": "conf_numeric",
        "verbal_critique": "conf_critique",
        "verbal_cot": "conf_cot",
    }

    for method_name in methods:
        conf_key = method_conf_keys[method_name]
        if conf_key not in data[0]:
            continue
        confs = [d[conf_key] for d in data]
        ece, bins = compute_ece(confs, labels)
        metrics = bootstrap_all(confs, labels)

        results[f"{method_name}_ece"] = ece
        results[f"{method_name}_ece_ci"] = metrics["ece_ci"]
        results[f"{method_name}_brier"] = metrics["brier"]
        results[f"{method_name}_brier_ci"] = metrics["brier_ci"]
        results[f"{method_name}_auroc"] = metrics["auroc"]
        results[f"{method_name}_auroc_ci"] = metrics["auroc_ci"]
        results[f"{method_name}_bins"] = bins
        results[f"{method_name}_confs"] = confs

        print(f"    {method_name}: ECE={ece:.4f} "
              f"[{metrics['ece_ci'][0]:.4f},{metrics['ece_ci'][1]:.4f}], "
              f"AUROC={metrics['auroc']:.4f} "
              f"[{metrics['auroc_ci'][0]:.4f},{metrics['auroc_ci'][1]:.4f}]",
              flush=True)

    results["labels"] = [float(x) for x in labels]
    results["per_problem"] = data

    # Distribution analysis for verbal methods
    for method in ["conf_numeric", "conf_critique", "conf_cot"]:
        vals = [d[method] for d in data if method in d]
        if vals:
            results[f"{method}_dist"] = dict(Counter([round(v, 1) for v in vals]))

    return results


# ==================== SFT EVALUATION ====================

def run_sft_evaluation(humaneval):
    """Quantitative SFT evaluation comparing base vs fine-tuned verbal confidence."""
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel

    print("\n" + "#" * 60)
    print("# SFT MODEL EVALUATION")
    print("#" * 60, flush=True)

    if not os.path.exists(os.path.join(SFT_ADAPTER, "adapter_config.json")):
        print(f"  SFT adapter not found at {SFT_ADAPTER}, skipping.", flush=True)
        return None

    base_model_name = MODELS["qwen2.5-coder-7b"]
    tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    base_m = AutoModelForCausalLM.from_pretrained(
        base_model_name, torch_dtype=torch.bfloat16,
        device_map="auto", trust_remote_code=True
    )
    sft_m = PeftModel.from_pretrained(base_m, SFT_ADAPTER)
    sft_m.eval()

    subset = humaneval[:80]  # Use same 80-problem subset as sensitivity analysis

    print(f"  Evaluating SFT model on HumanEval ({len(subset)} problems)...", flush=True)
    t0 = time.time()

    sampling_confs, sft_verbal_confs, base_verbal_confs, labels = [], [], [], []
    per_problem = []

    for idx, prob in enumerate(subset):
        if idx % 10 == 0:
            print(f"    [{idx}/{len(subset)}] ({time.time()-t0:.0f}s)", flush=True)

        # Sampling confidence with SFT model
        pi = fmt(tokenizer, [{"role": "user", "content": PROMPT_DIRECT.format(prob['prompt'])}])
        samples = gen(sft_m, tokenizer, pi, 10, temp=0.8)

        sample_ok = []
        for s in samples:
            code = extract_code(s)
            ok = execute_humaneval(code, prob)
            sample_ok.append(ok)

        pr = sum(sample_ok) / len(sample_ok)
        sampling_confs.append(float(pr))
        labels.append(float(sample_ok[0]))

        # SFT verbal confidence (trained prompt)
        ci = fmt(tokenizer, [
            {"role": "system", "content": "Before solving, state your confidence:\n"
             "- 'I am confident this solution is correct' for high confidence\n"
             "- 'This should work for most cases, but please verify edge cases' for medium\n"
             "- 'I am not confident in this solution, it may contain bugs' for low\n"
             "Then solve."},
            {"role": "user", "content": f"State confidence and complete:\n\n{prob['prompt']}"}
        ])
        cresp = gen(sft_m, tokenizer, ci, 1, temp=0.1)[0]
        vc = extract_trained_conf(cresp)
        sft_verbal_confs.append(float(vc))

        # Base model verbal confidence (same prompt, for comparison)
        # We use the numeric prompt from the base model to compare
        ci_base = fmt(tokenizer, [
            {"role": "user", "content": PROMPT_NUMERIC.format(prob['prompt'])}
        ])
        resp_base = gen(sft_m, tokenizer, ci_base, 1, temp=0.1)[0]
        bvc = extract_numeric_conf(resp_base)
        base_verbal_confs.append(float(bvc))

        per_problem.append({
            "task_id": prob["task_id"],
            "pass_count": sum(sample_ok),
            "sampling_conf": float(pr),
            "sft_verbal_conf": float(vc),
            "base_verbal_conf": float(bvc),
            "correct": float(sample_ok[0]),
            "sft_response_preview": cresp[:200],
        })

    results = {
        "model": "qwen-sft",
        "base_model": "Qwen/Qwen2.5-Coder-7B-Instruct",
        "n_problems": len(subset),
        "time_seconds": time.time() - t0,
        "pass_at_1": float(np.mean(labels)),
    }

    for cn, cv in [("sampling", sampling_confs),
                   ("sft_verbal", sft_verbal_confs),
                   ("base_verbal", base_verbal_confs)]:
        ece, bins = compute_ece(cv, labels)
        metrics = bootstrap_all(cv, labels)
        results[f"{cn}_ece"] = ece
        results[f"{cn}_ece_ci"] = metrics["ece_ci"]
        results[f"{cn}_brier"] = metrics["brier"]
        results[f"{cn}_brier_ci"] = metrics["brier_ci"]
        results[f"{cn}_auroc"] = metrics["auroc"]
        results[f"{cn}_auroc_ci"] = metrics["auroc_ci"]
        results[f"{cn}_bins"] = bins
        results[f"{cn}_confs"] = cv
        print(f"    {cn}: ECE={ece:.4f} "
              f"[{metrics['ece_ci'][0]:.4f},{metrics['ece_ci'][1]:.4f}], "
              f"AUROC={metrics['auroc']:.4f} "
              f"[{metrics['auroc_ci'][0]:.4f},{metrics['auroc_ci'][1]:.4f}]",
              flush=True)

    results["labels"] = labels
    results["per_problem"] = per_problem

    # Distribution analysis
    results["sft_verbal_dist"] = dict(Counter([round(v, 1) for v in sft_verbal_confs]))
    results["base_verbal_dist"] = dict(Counter([round(v, 1) for v in base_verbal_confs]))

    del sft_m, base_m, tokenizer
    torch.cuda.empty_cache()
    gc.collect()

    sp = os.path.join(RESULTS_DIR, "sft_evaluation.json")
    with open(sp, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"  Saved: {sp}", flush=True)

    return results


# ==================== MAIN ====================

def load_model(model_name):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    print(f"\nLoading model: {model_name}...", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, torch_dtype=torch.bfloat16,
        device_map="auto", trust_remote_code=True
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model.eval()
    print(f"  Model loaded. Device: {model.device}", flush=True)
    return model, tokenizer


def main():
    t_start = time.time()
    print("=" * 60)
    print("DL4C V3: MULTI-MODEL + SFT + N=20 EXPERIMENTS")
    print("=" * 60, flush=True)

    humaneval = load_humaneval()
    mbpp = load_mbpp()
    print(f"HumanEval: {len(humaneval)}, MBPP: {len(mbpp)}", flush=True)

    # ===================================================================
    # PHASE 1: DeepSeek-Coder-V2-Lite-Instruct — full evaluation
    # ===================================================================
    ds_model_key = "deepseek-coder-v2-lite"
    ds_model_name = MODELS[ds_model_key]

    # HumanEval
    ds_he_path = os.path.join(RESULTS_DIR, f"{ds_model_key}_humaneval.json")
    if not os.path.exists(ds_he_path):
        model, tokenizer = load_model(ds_model_name)

        print("\n" + "#" * 60)
        print(f"# PHASE 1a: {ds_model_key} on HumanEval (all methods)")
        print("#" * 60, flush=True)
        he_results = run_experiment(model, tokenizer, humaneval, True,
                                    f"{ds_model_key}_humaneval",
                                    n_samples=10, temperature=0.8)
        he_results["model"] = ds_model_name
        with open(ds_he_path, 'w') as f:
            json.dump(he_results, f, indent=2)
        print(f"  Saved: {ds_he_path}", flush=True)

        # MBPP
        ds_mbpp_path = os.path.join(RESULTS_DIR, f"{ds_model_key}_mbpp.json")
        if not os.path.exists(ds_mbpp_path):
            print("\n" + "#" * 60)
            print(f"# PHASE 1b: {ds_model_key} on MBPP (all methods)")
            print("#" * 60, flush=True)
            mbpp_results = run_experiment(model, tokenizer, mbpp, False,
                                          f"{ds_model_key}_mbpp",
                                          n_samples=10, temperature=0.8)
            mbpp_results["model"] = ds_model_name
            with open(ds_mbpp_path, 'w') as f:
                json.dump(mbpp_results, f, indent=2)
            print(f"  Saved: {ds_mbpp_path}", flush=True)

        del model, tokenizer
        torch.cuda.empty_cache()
        gc.collect()
    else:
        print(f"\n{ds_model_key} HumanEval already done, skipping.", flush=True)

    # ===================================================================
    # PHASE 2: N=20 sensitivity (Qwen model, HumanEval subset)
    # ===================================================================
    n20_path = os.path.join(RESULTS_DIR, "sensitivity_n_20.json")
    if not os.path.exists(n20_path):
        print("\n" + "#" * 60)
        print("# PHASE 2: N=20 sensitivity (Qwen, HumanEval subset)")
        print("#" * 60, flush=True)

        model, tokenizer = load_model(MODELS["qwen2.5-coder-7b"])
        subset = humaneval[:80]

        r = run_experiment(model, tokenizer, subset, True, "he_n20",
                           n_samples=20, temperature=0.8,
                           methods=["sampling"])
        r["model"] = MODELS["qwen2.5-coder-7b"]
        with open(n20_path, 'w') as f:
            json.dump(r, f, indent=2)
        print(f"  Saved: {n20_path}", flush=True)

        del model, tokenizer
        torch.cuda.empty_cache()
        gc.collect()
    else:
        print("\nN=20 sensitivity already done, skipping.", flush=True)

    # ===================================================================
    # PHASE 3: SFT evaluation
    # ===================================================================
    sft_path = os.path.join(RESULTS_DIR, "sft_evaluation.json")
    if not os.path.exists(sft_path):
        sft_results = run_sft_evaluation(humaneval)
    else:
        print("\nSFT evaluation already done, skipping.", flush=True)

    # ===================================================================
    # PHASE 4: Cross-model comparison summary
    # ===================================================================
    print("\n" + "#" * 60)
    print("# PHASE 4: Cross-Model Comparison Summary")
    print("#" * 60, flush=True)

    summary = {"generated_at": time.strftime("%Y-%m-%d %H:%M:%S")}

    # Load all results
    for fname in os.listdir(RESULTS_DIR):
        if fname.endswith('.json') and fname != 'cross_model_summary.json':
            fpath = os.path.join(RESULTS_DIR, fname)
            with open(fpath) as f:
                data = json.load(f)
            key = fname.replace('.json', '')
            summary[key] = {
                "benchmark": data.get("benchmark", ""),
                "model": data.get("model", ""),
                "n_problems": data.get("n_problems", 0),
                "pass_at_1": data.get("pass_at_1", None),
                "pass_at_10": data.get("pass_at_10", None),
            }
            for method in ["sampling", "logprob", "verbal_numeric",
                           "verbal_critique", "verbal_cot",
                           "sft_verbal", "base_verbal"]:
                ece_key = f"{method}_ece"
                auroc_key = f"{method}_auroc"
                if ece_key in data:
                    summary[key][ece_key] = data[ece_key]
                    summary[key][f"{ece_key}_ci"] = data.get(f"{ece_key}_ci")
                    summary[key][auroc_key] = data.get(auroc_key)
                    summary[key][f"{auroc_key}_ci"] = data.get(f"{auroc_key}_ci")

    summary_path = os.path.join(RESULTS_DIR, "cross_model_summary.json")
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"  Saved: {summary_path}", flush=True)

    # ===== Print final summary =====
    total_time = (time.time() - t_start) / 60
    print("\n" + "=" * 60)
    print(f"ALL V3 EXPERIMENTS COMPLETE ({total_time:.1f} min)")
    print("=" * 60, flush=True)
    for f_name in sorted(os.listdir(RESULTS_DIR)):
        sz = os.path.getsize(os.path.join(RESULTS_DIR, f_name))
        print(f"  {f_name} ({sz} bytes)")


if __name__ == "__main__":
    main()
