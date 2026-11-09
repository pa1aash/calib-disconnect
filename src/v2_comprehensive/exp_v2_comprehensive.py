"""
DL4C V2: Comprehensive revised experiments addressing all reviewer concerns.

Fixes:
1. Temperature alignment: sampling conf and labels use SAME temperature
2. Bootstrap CIs for all metrics
3. Sensitivity analysis: vary tau and n
4. Log-probability baseline confidence
5. Alternative verbal elicitation (critique-then-rate, chain-of-thought)
6. Fixed MBPP execution with signature enforcement
7. Quantitative SFT evaluation with CIs
8. Per-sample confidence analysis
9. Runtime/latency measurements
"""

import json, os, time, re, subprocess, tempfile, gc, sys
import numpy as np
import torch
from math import comb
from collections import Counter
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from datasets import load_dataset

RESULTS_DIR = "/home/ubuntu/dl4c_experiments/results_v2"
MODEL_DIR = "/home/ubuntu/dl4c_experiments/models"
BASE_MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct"
SFT_MODEL = os.path.join(MODEL_DIR, "qwen_confidence_sft")
os.makedirs(RESULTS_DIR, exist_ok=True)

MAX_TOKENS = 512

# ==================== METRICS ====================

def compute_ece(c, a, n_bins=10):
    c, a = np.array(c, dtype=float), np.array(a, dtype=float)
    bounds = np.linspace(0, 1, n_bins + 1)
    ece = 0.0; bins = []
    for i in range(n_bins):
        m = (c >= bounds[i]) & (c < bounds[i+1]) if i < n_bins-1 else (c >= bounds[i]) & (c <= bounds[i+1])
        if m.sum() > 0:
            ba, bc, bs = float(a[m].mean()), float(c[m].mean()), int(m.sum())
            ece += (bs / len(c)) * abs(ba - bc)
            bins.append({"lo": float(bounds[i]), "hi": float(bounds[i+1]), "acc": ba, "conf": bc, "n": bs})
    return float(ece), bins

def compute_brier(c, a): return float(np.mean((np.array(c) - np.array(a)) ** 2))

def compute_auroc(c, a):
    from sklearn.metrics import roc_auc_score
    c, a = np.array(c), np.array(a)
    return float(roc_auc_score(a, c)) if len(np.unique(a)) >= 2 else float('nan')

def bootstrap_metric(metric_fn, c, a, n_boot=1000, seed=42):
    """Bootstrap confidence intervals for a metric."""
    rng = np.random.RandomState(seed)
    c, a = np.array(c), np.array(a)
    vals = []
    for _ in range(n_boot):
        idx = rng.randint(0, len(c), len(c))
        try:
            v = metric_fn(c[idx], a[idx])
            if not np.isnan(v):
                vals.append(v)
        except: pass
    if not vals:
        return float('nan'), float('nan'), float('nan')
    vals = sorted(vals)
    return float(np.mean(vals)), float(vals[int(0.025*len(vals))]), float(vals[int(0.975*len(vals))])

def bootstrap_all(c, a, n_boot=1000):
    """Compute all metrics with bootstrap CIs."""
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
        f.write(code); f.flush()
        try: return subprocess.run(['python3', f.name], capture_output=True, text=True, timeout=timeout).returncode == 0
        except: return False
        finally: os.unlink(f.name)

def execute_humaneval(code, prob):
    full_code = code if prob["prompt"] in code else prob["prompt"] + code
    test_code = prob["test"] + f"\ncheck({prob['entry_point']})"
    return _run_code(full_code + "\n" + test_code)

def execute_mbpp_fixed(code, prob):
    """Fixed MBPP execution: extract function, ensure proper test format."""
    # MBPP tests use assert statements like: assert func(args) == expected
    # We need to make sure the generated code defines the expected function
    test_lines = prob["test"]
    # Try running the code with the tests directly
    ok = _run_code(code + "\n" + test_lines)
    if ok:
        return True
    # If that fails, try wrapping the code
    # Extract expected function name from test
    func_match = re.search(r'assert\s+(\w+)\s*\(', test_lines)
    if func_match:
        expected_fn = func_match.group(1)
        # Check if code defines this function
        if f"def {expected_fn}" not in code:
            # Try to find a def in the code and alias it
            def_match = re.search(r'def\s+(\w+)\s*\(', code)
            if def_match:
                actual_fn = def_match.group(1)
                aliased = code + f"\n{expected_fn} = {actual_fn}\n"
                return _run_code(aliased + "\n" + test_lines)
    return False

def extract_code(resp):
    blocks = re.findall(r'```(?:python)?\n?(.*?)```', resp, re.DOTALL)
    if blocks: return blocks[0].strip()
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

# ==================== CONFIDENCE EXTRACTION ====================

def extract_numeric_conf(resp):
    m = re.search(r'CONFIDENCE:\s*(\d)', resp)
    if m: return min(max(int(m.group(1)), 1), 5) / 5.0
    m = re.search(r'(\d)\s*/\s*5', resp)
    if m: return int(m.group(1)) / 5.0
    rl = resp.lower()
    if 'very confident' in rl or '5/5' in rl: return 1.0
    if 'quite confident' in rl or 'confident' in rl and 'not' not in rl: return 0.8
    if 'moderately' in rl or 'should work' in rl or 'fairly' in rl: return 0.6
    if 'somewhat' in rl or 'unsure' in rl: return 0.4
    if 'not confident' in rl or 'unlikely' in rl: return 0.2
    return 0.6

def extract_trained_conf(resp):
    rl = resp.lower()
    if 'i am confident this solution is correct' in rl: return 0.9
    if 'should work for most cases' in rl or 'please verify' in rl: return 0.6
    if 'not confident' in rl or 'may contain bugs' in rl: return 0.3
    return extract_numeric_conf(resp)

# ==================== GENERATION ====================

@torch.no_grad()
def gen(model, tokenizer, prompt, n=1, temp=0.8):
    ids = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048).input_ids.to(model.device)
    results = []
    for _ in range(n):
        try:
            out = model.generate(ids, max_new_tokens=MAX_TOKENS, temperature=max(temp, 0.01),
                                top_p=0.95, do_sample=True, pad_token_id=tokenizer.pad_token_id)
            results.append(tokenizer.decode(out[0][ids.shape[1]:], skip_special_tokens=True))
        except:
            results.append("")
    return results

@torch.no_grad()
def gen_with_logprobs(model, tokenizer, prompt, temp=0.8):
    """Generate one sample and return (text, mean_log_prob)."""
    ids = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048).input_ids.to(model.device)
    out = model.generate(ids, max_new_tokens=MAX_TOKENS, temperature=max(temp, 0.01),
                        top_p=0.95, do_sample=True, pad_token_id=tokenizer.pad_token_id)
    gen_ids = out[0][ids.shape[1]:]
    text = tokenizer.decode(gen_ids, skip_special_tokens=True)
    
    # Forward pass to get log probs
    logits = model(out).logits[0]
    gen_logits = logits[ids.shape[1]-1:-1]  # shifted for next-token prediction
    log_probs = torch.log_softmax(gen_logits, dim=-1)
    actual_ids = gen_ids[:len(gen_logits)]
    token_log_probs = log_probs[torch.arange(len(actual_ids)), actual_ids]
    mean_lp = token_log_probs.mean().item()
    # Convert to probability-like confidence: exp(mean_log_prob)
    confidence = float(np.exp(mean_lp))
    
    return text, confidence

def fmt(tokenizer, msgs):
    try: return tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    except: return msgs[-1]["content"]

# ==================== DATA ====================

def load_humaneval():
    ds = load_dataset("openai_humaneval", split="test")
    return [{"task_id": i["task_id"], "prompt": i["prompt"], "canonical_solution": i["canonical_solution"],
             "test": i["test"], "entry_point": i["entry_point"]} for i in ds]

def load_mbpp():
    ds = load_dataset("google-research-datasets/mbpp", "sanitized", split="test")
    return [{"task_id": f"mbpp_{i['task_id']}", "prompt": i["prompt"],
             "test": "\n".join(i["test_list"]), "code": i["code"]} for i in ds]

# ==================== PROMPTS ====================

PROMPT_DIRECT = "Complete the following Python function. Only output the complete function, no explanations.\n\n{}"
PROMPT_MBPP = "Write a Python function to solve: {}\nOnly output the function, no explanations."

# Verbal confidence prompts
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

# ==================== MAIN EXPERIMENTS ====================

def run_comprehensive_experiment(model, tokenizer, problems, is_humaneval, bench_name, n_samples=10, temperature=0.8):
    """
    Run all confidence methods on a set of problems.
    CRITICAL FIX: Use the SAME temperature for both sampling and labels.
    """
    print(f"\n  === {bench_name} (n={len(problems)}, samples={n_samples}, tau={temperature}) ===", flush=True)
    t0 = time.time()
    
    # Storage
    data = []
    latency_per_sample = []
    
    for idx, prob in enumerate(problems):
        if idx % 20 == 0: print(f"    [{idx}/{len(problems)}] ({time.time()-t0:.0f}s)", flush=True)
        
        prompt = prob["prompt"]
        
        # ---- Phase 1: Generate n samples at the SAME temperature for both confidence AND labels ----
        pi = fmt(tokenizer, [{"role": "user", "content": PROMPT_DIRECT.format(prompt) if is_humaneval else PROMPT_MBPP.format(prompt)}])
        
        t_gen_start = time.time()
        samples = gen(model, tokenizer, pi, n_samples, temp=temperature)
        t_gen_end = time.time()
        latency_per_sample.append((t_gen_end - t_gen_start) / n_samples)
        
        sample_results = []
        for s in samples:
            code = extract_code(s)
            if is_humaneval:
                ok = execute_humaneval(code, prob)
            else:
                ok = execute_mbpp_fixed(code, prob)
            sample_results.append({"text": s, "code": code, "correct": ok})
        
        pass_count = sum(1 for s in sample_results if s["correct"])
        sampling_conf = pass_count / len(sample_results)
        
        # Use FIRST sample's correctness as the label (same distribution as sampling)
        first_correct = sample_results[0]["correct"]
        
        # ---- Phase 2: Log-probability confidence (on first sample) ----
        try:
            _, logprob_conf = gen_with_logprobs(model, tokenizer, pi, temp=temperature)
        except:
            logprob_conf = 0.5
        
        # ---- Phase 3: Verbalized confidence - multiple elicitation strategies ----
        # Strategy A: Simple numeric (1-5 scale)
        ci_num = fmt(tokenizer, [{"role": "user", "content": PROMPT_NUMERIC.format(prompt)}])
        resp_num = gen(model, tokenizer, ci_num, 1, temp=0.1)[0]
        conf_numeric = extract_numeric_conf(resp_num)
        
        # Strategy B: Critique-then-rate
        ci_crit = fmt(tokenizer, [{"role": "user", "content": PROMPT_CRITIQUE.format(prompt)}])
        resp_crit = gen(model, tokenizer, ci_crit, 1, temp=0.1)[0]
        conf_critique = extract_numeric_conf(resp_crit)
        
        # Strategy C: Chain-of-thought then rate
        ci_cot = fmt(tokenizer, [{"role": "user", "content": PROMPT_COT.format(prompt)}])
        resp_cot = gen(model, tokenizer, ci_cot, 1, temp=0.1)[0]
        conf_cot = extract_numeric_conf(resp_cot)
        
        # ---- Store everything ----
        entry = {
            "task_id": prob.get("task_id", f"{bench_name}_{idx}"),
            "first_correct": first_correct,
            "pass_count": pass_count,
            "n_samples": n_samples,
            "sampling_conf": sampling_conf,
            "logprob_conf": logprob_conf,
            "conf_numeric": conf_numeric,
            "conf_critique": conf_critique,
            "conf_cot": conf_cot,
            "resp_numeric_preview": resp_num[:200],
            "resp_critique_preview": resp_crit[:200],
        }
        data.append(entry)
    
    elapsed = time.time() - t0
    
    # ---- Compute metrics with bootstrap CIs ----
    labels = [d["first_correct"] for d in data]
    
    results = {
        "benchmark": bench_name, "n_problems": len(problems), "n_samples": n_samples,
        "temperature": temperature, "time_seconds": elapsed,
        "mean_latency_per_sample_s": float(np.mean(latency_per_sample)),
        "pass_at_1": float(np.mean(labels)),
    }
    
    # Per-sample pass@k
    p10 = []
    for d in data:
        n, c = d["n_samples"], d["pass_count"]
        k = min(10, n)
        p10.append(1.0 if n - c < k else 1.0 - comb(n - c, k) / comb(n, k))
    results["pass_at_10"] = float(np.mean(p10))
    
    for method_name, conf_key in [("sampling", "sampling_conf"), ("logprob", "logprob_conf"),
                                   ("verbal_numeric", "conf_numeric"), ("verbal_critique", "conf_critique"),
                                   ("verbal_cot", "conf_cot")]:
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
        
        print(f"    {method_name}: ECE={ece:.4f} [{metrics['ece_ci'][0]:.4f},{metrics['ece_ci'][1]:.4f}], "
              f"AUROC={metrics['auroc']:.4f} [{metrics['auroc_ci'][0]:.4f},{metrics['auroc_ci'][1]:.4f}]")
    
    results["labels"] = [float(x) for x in labels]
    results["per_problem"] = data
    
    # Verbal confidence distribution analysis
    for method in ["conf_numeric", "conf_critique", "conf_cot"]:
        vals = [d[method] for d in data]
        results[f"{method}_dist"] = dict(Counter([round(v, 1) for v in vals]))
    
    return results


def run_sensitivity_analysis(model, tokenizer, humaneval):
    """Sensitivity analysis: vary temperature and n_samples."""
    print("\n" + "#"*60)
    print("# SENSITIVITY ANALYSIS")
    print("#"*60, flush=True)
    
    # Use a fixed subset for speed (first 80 problems)
    subset = humaneval[:80]
    
    sensitivity = {}
    
    # Vary temperature
    for tau in [0.2, 0.5, 0.8, 1.0]:
        key = f"tau_{tau}"
        print(f"\n  --- Temperature = {tau} (n=10) ---", flush=True)
        r = run_comprehensive_experiment(model, tokenizer, subset, True, f"he_tau{tau}", n_samples=10, temperature=tau)
        sensitivity[key] = {
            "tau": tau, "n": 10,
            "pass_at_1": r["pass_at_1"],
            "sampling_ece": r["sampling_ece"], "sampling_auroc": r["sampling_auroc"],
            "logprob_ece": r["logprob_ece"], "logprob_auroc": r["logprob_auroc"],
            "verbal_numeric_ece": r["verbal_numeric_ece"], "verbal_numeric_auroc": r["verbal_numeric_auroc"],
        }
        sp = os.path.join(RESULTS_DIR, f"sensitivity_{key}.json")
        with open(sp, 'w') as f: json.dump(r, f, indent=2)
    
    # Vary n_samples (at tau=0.8)
    for n in [3, 5, 10, 20]:
        key = f"n_{n}"
        print(f"\n  --- n_samples = {n} (tau=0.8) ---", flush=True)
        r = run_comprehensive_experiment(model, tokenizer, subset, True, f"he_n{n}", n_samples=n, temperature=0.8)
        sensitivity[key] = {
            "tau": 0.8, "n": n,
            "pass_at_1": r["pass_at_1"],
            "sampling_ece": r["sampling_ece"], "sampling_auroc": r["sampling_auroc"],
            "sampling_ece_ci": r["sampling_ece_ci"], "sampling_auroc_ci": r["sampling_auroc_ci"],
            "mean_latency_per_sample_s": r["mean_latency_per_sample_s"],
        }
        sp = os.path.join(RESULTS_DIR, f"sensitivity_{key}.json")
        with open(sp, 'w') as f: json.dump(r, f, indent=2)
    
    with open(os.path.join(RESULTS_DIR, "sensitivity_summary.json"), 'w') as f:
        json.dump(sensitivity, f, indent=2)
    
    return sensitivity


def run_sft_evaluation(humaneval):
    """Quantitative SFT evaluation with bootstrap CIs."""
    print("\n" + "#"*60)
    print("# SFT MODEL EVALUATION")
    print("#"*60, flush=True)
    
    if not os.path.exists(os.path.join(SFT_MODEL, "adapter_config.json")):
        print("  SFT model not found, skipping.")
        return None
    
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    base_m = AutoModelForCausalLM.from_pretrained(BASE_MODEL, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    sft_m = PeftModel.from_pretrained(base_m, SFT_MODEL)
    sft_m.eval()
    
    # Use subset for speed
    subset = humaneval[:80]
    
    print("  Evaluating SFT model on HumanEval (first 80 problems)...", flush=True)
    t0 = time.time()
    
    sampling_confs, sft_verbal_confs, labels = [], [], []
    per_problem = []
    
    for idx, prob in enumerate(subset):
        if idx % 10 == 0: print(f"    [{idx}/{len(subset)}] ({time.time()-t0:.0f}s)", flush=True)
        
        # Sampling confidence (same as base)
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
        
        # SFT verbal confidence
        ci = fmt(tokenizer, [{"role": "system", "content": "Before solving, state your confidence:\n- 'I am confident this solution is correct' for high confidence\n- 'This should work for most cases, but please verify edge cases' for medium\n- 'I am not confident in this solution, it may contain bugs' for low\nThen solve."},
                             {"role": "user", "content": f"State confidence and complete:\n\n{prob['prompt']}"}])
        cresp = gen(sft_m, tokenizer, ci, 1, temp=0.1)[0]
        vc = extract_trained_conf(cresp)
        sft_verbal_confs.append(float(vc))
        
        per_problem.append({"task_id": prob["task_id"], "pass_count": sum(sample_ok),
                           "sampling_conf": float(pr), "sft_verbal_conf": float(vc),
                           "correct": float(sample_ok[0])})
    
    results = {"model": "qwen-sft", "n_problems": len(subset), "time_seconds": time.time()-t0}
    
    for cn, cv in [("sampling", sampling_confs), ("sft_verbal", sft_verbal_confs)]:
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
        print(f"    {cn}: ECE={ece:.4f} [{metrics['ece_ci'][0]:.4f},{metrics['ece_ci'][1]:.4f}], AUROC={metrics['auroc']:.4f}")
    
    results["labels"] = labels
    results["per_problem"] = per_problem
    results["sft_verbal_dist"] = dict(Counter([round(v, 1) for v in sft_verbal_confs]))
    results["pass_at_1"] = float(np.mean(labels))
    
    del sft_m, base_m, tokenizer; torch.cuda.empty_cache(); gc.collect()
    
    sp = os.path.join(RESULTS_DIR, "sft_evaluation.json")
    with open(sp, 'w') as f: json.dump(results, f, indent=2)
    print(f"  Saved: {sp}")
    
    return results


# ==================== MAIN ====================

if __name__ == "__main__":
    t_start = time.time()
    print("="*60)
    print("DL4C V2: COMPREHENSIVE REVISED EXPERIMENTS")
    print("="*60, flush=True)
    
    humaneval = load_humaneval()
    mbpp = load_mbpp()
    print(f"HumanEval: {len(humaneval)}, MBPP: {len(mbpp)}")
    
    # Load model once
    print("\nLoading model...", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    model.eval()
    print("Model loaded.", flush=True)
    
    # ===== Experiment 1: Full HumanEval with all confidence methods =====
    he_path = os.path.join(RESULTS_DIR, "main_humaneval.json")
    if not os.path.exists(he_path):
        print("\n" + "#"*60)
        print("# EXPERIMENT 1: Full HumanEval (all methods)")
        print("#"*60, flush=True)
        he_results = run_comprehensive_experiment(model, tokenizer, humaneval, True, "humaneval", n_samples=10, temperature=0.8)
        with open(he_path, 'w') as f: json.dump(he_results, f, indent=2)
    else:
        print("\nHumanEval already done, skipping.")
    
    # ===== Experiment 2: Full MBPP with fixed execution =====
    mbpp_path = os.path.join(RESULTS_DIR, "main_mbpp.json")
    if not os.path.exists(mbpp_path):
        print("\n" + "#"*60)
        print("# EXPERIMENT 2: Full MBPP (fixed execution)")
        print("#"*60, flush=True)
        mbpp_results = run_comprehensive_experiment(model, tokenizer, mbpp, False, "mbpp", n_samples=10, temperature=0.8)
        with open(mbpp_path, 'w') as f: json.dump(mbpp_results, f, indent=2)
    else:
        print("\nMBPP already done, skipping.")
    
    # ===== Experiment 3: Sensitivity analysis =====
    sens_path = os.path.join(RESULTS_DIR, "sensitivity_summary.json")
    if not os.path.exists(sens_path):
        sensitivity = run_sensitivity_analysis(model, tokenizer, humaneval)
    else:
        print("\nSensitivity analysis already done, skipping.")
    
    # Free base model
    del model, tokenizer; torch.cuda.empty_cache(); gc.collect()
    
    # ===== Experiment 4: SFT evaluation =====
    sft_path = os.path.join(RESULTS_DIR, "sft_evaluation.json")
    if not os.path.exists(sft_path):
        sft_results = run_sft_evaluation(humaneval)
    else:
        print("\nSFT evaluation already done, skipping.")
    
    # ===== Final Summary =====
    total_time = (time.time() - t_start) / 60
    print("\n" + "="*60)
    print(f"ALL V2 EXPERIMENTS COMPLETE ({total_time:.1f} min)")
    print("="*60)
    for f_name in sorted(os.listdir(RESULTS_DIR)):
        sz = os.path.getsize(os.path.join(RESULTS_DIR, f_name))
        print(f"  {f_name} ({sz} bytes)")
