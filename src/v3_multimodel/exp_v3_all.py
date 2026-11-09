"""
DL4C V3: Complete revised experiments addressing ALL reviewer R2 concerns.

NEW experiments:
1. Independent label draw (n+1th sample) to remove dependence
2. Same-temperature verbal elicitation (tau=0.8) for apples-to-apples
3. Isotonic regression on log-prob baseline
4. AST-clustering proxy confidence (no-test setting)
5. SFT per-problem discrimination analysis (hard vs easy)
6. TACE (Thresholded Adaptive Calibration Error) metric
7. Second model: DeepSeek-Coder-6.7B for generality
8. Exact harness documentation
"""

import json, os, time, re, subprocess, tempfile, gc, sys, ast, platform
import numpy as np
import torch
from math import comb
from collections import Counter
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from datasets import load_dataset
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

RESULTS_DIR = "/home/ubuntu/dl4c/results_v3"
MODEL_DIR = "/home/ubuntu/dl4c/models"
SFT_DIR = os.path.join(MODEL_DIR, "qwen_confidence_sft")
os.makedirs(RESULTS_DIR, exist_ok=True)
MAX_TOKENS = 512

MODELS = [
    ("qwen2.5-coder-7b", "Qwen/Qwen2.5-Coder-7B-Instruct"),
    ("deepseek-coder-6.7b", "deepseek-ai/deepseek-coder-6.7b-instruct"),
]

# ==================== HARNESS DOCUMENTATION ====================
def log_harness_info():
    info = {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "torch_version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "gpu_memory_gb": round(torch.cuda.get_device_properties(0).total_memory / 1e9, 1) if torch.cuda.is_available() else None,
        "humaneval_source": "openai_humaneval (HuggingFace datasets)",
        "mbpp_source": "google-research-datasets/mbpp sanitized split",
        "execution_method": "subprocess with 10s timeout, isolated temp files",
        "humaneval_runner": "direct function execution + check() test harness from dataset",
        "max_generation_tokens": MAX_TOKENS,
        "sampling_top_p": 0.95,
        "no_modifications_to_test_harness": True,
    }
    with open(os.path.join(RESULTS_DIR, "harness_info.json"), 'w') as f:
        json.dump(info, f, indent=2)
    print(f"  Harness: Python {info['python_version']}, torch {info['torch_version']}, GPU {info['gpu_name']}")
    return info

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

def compute_tace(c, a, threshold=0.01):
    """Thresholded Adaptive Calibration Error — robust to small bins."""
    c, a = np.array(c, dtype=float), np.array(a, dtype=float)
    sorted_idx = np.argsort(c)
    c_s, a_s = c[sorted_idx], a[sorted_idx]
    n = len(c)
    n_bins = max(1, int(np.sqrt(n)))
    bin_size = n // n_bins
    tace = 0.0
    for i in range(n_bins):
        start = i * bin_size
        end = start + bin_size if i < n_bins - 1 else n
        bc = c_s[start:end]; ba = a_s[start:end]
        if len(bc) > 0:
            gap = abs(ba.mean() - bc.mean())
            if gap > threshold:
                tace += (len(bc) / n) * gap
    return float(tace)

def compute_brier(c, a): return float(np.mean((np.array(c) - np.array(a)) ** 2))

def compute_auroc(c, a):
    c, a = np.array(c), np.array(a)
    return float(roc_auc_score(a, c)) if len(np.unique(a)) >= 2 else float('nan')

def bootstrap_all(c, a, n_boot=1000):
    rng = np.random.RandomState(42); c, a = np.array(c), np.array(a)
    ece_fn = lambda c, a: compute_ece(c, a)[0]
    results = {}
    for name, fn in [("ece", ece_fn), ("brier", compute_brier), ("auroc", compute_auroc), ("tace", compute_tace)]:
        vals = []
        for _ in range(n_boot):
            idx = rng.randint(0, len(c), len(c))
            try:
                v = fn(c[idx], a[idx])
                if not np.isnan(v): vals.append(v)
            except: pass
        if vals:
            vals = sorted(vals)
            results[name] = float(np.mean(vals))
            results[f"{name}_ci"] = [float(vals[int(0.025*len(vals))]), float(vals[int(0.975*len(vals))])]
        else:
            results[name] = float('nan'); results[f"{name}_ci"] = [float('nan'), float('nan')]
    return results

def isotonic_calibrate(confs_train, labels_train, confs_test):
    """Apply isotonic regression calibration."""
    ir = IsotonicRegression(out_of_bounds='clip')
    ir.fit(confs_train, labels_train)
    return ir.predict(confs_test)

def platt_calibrate(confs_train, labels_train, confs_test):
    """Apply Platt scaling (logistic regression on confidence)."""
    lr = LogisticRegression()
    lr.fit(np.array(confs_train).reshape(-1, 1), labels_train)
    return lr.predict_proba(np.array(confs_test).reshape(-1, 1))[:, 1]

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

def extract_code(resp):
    blocks = re.findall(r'```(?:python)?\n?(.*?)```', resp, re.DOTALL)
    if blocks: return blocks[0].strip()
    lines = resp.split('\n'); code_lines = []; in_code = False
    for line in lines:
        if line.strip().startswith('def ') or in_code:
            in_code = True; code_lines.append(line)
        elif in_code and line.strip() == '': code_lines.append(line)
        elif in_code and not line.startswith(' ') and not line.startswith('\t') and line.strip(): break
    return '\n'.join(code_lines).strip() if code_lines else resp.strip()

def extract_numeric_conf(resp):
    m = re.search(r'CONFIDENCE:\s*(\d)', resp)
    if m: return min(max(int(m.group(1)), 1), 5) / 5.0
    m = re.search(r'(\d)\s*/\s*5', resp)
    if m: return int(m.group(1)) / 5.0
    rl = resp.lower()
    if 'very confident' in rl: return 1.0
    if 'confident' in rl and 'not' not in rl: return 0.8
    if 'should work' in rl or 'moderately' in rl: return 0.6
    if 'unsure' in rl or 'not confident' in rl: return 0.4
    return 0.6

def extract_trained_conf(resp):
    rl = resp.lower()
    if 'i am confident this solution is correct' in rl: return 0.9
    if 'should work for most cases' in rl or 'please verify' in rl: return 0.6
    if 'not confident' in rl or 'may contain bugs' in rl: return 0.3
    return extract_numeric_conf(resp)

def normalize_code_for_ast(code):
    """Normalize code to canonical AST form for clustering."""
    try:
        tree = ast.parse(code)
        return ast.dump(tree, annotate_fields=False)
    except:
        return code.strip()

@torch.no_grad()
def gen(model, tokenizer, prompt, n=1, temp=0.8):
    ids = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048).input_ids.to(model.device)
    results = []
    for _ in range(n):
        try:
            out = model.generate(ids, max_new_tokens=MAX_TOKENS, temperature=max(temp, 0.01),
                                top_p=0.95, do_sample=True, pad_token_id=tokenizer.pad_token_id)
            results.append(tokenizer.decode(out[0][ids.shape[1]:], skip_special_tokens=True))
        except: results.append("")
    return results

@torch.no_grad()
def gen_with_logprob(model, tokenizer, prompt, temp=0.8):
    ids = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048).input_ids.to(model.device)
    out = model.generate(ids, max_new_tokens=MAX_TOKENS, temperature=max(temp, 0.01),
                        top_p=0.95, do_sample=True, pad_token_id=tokenizer.pad_token_id)
    gen_ids = out[0][ids.shape[1]:]
    text = tokenizer.decode(gen_ids, skip_special_tokens=True)
    logits = model(out).logits[0]
    gen_logits = logits[ids.shape[1]-1:-1]
    log_probs = torch.log_softmax(gen_logits, dim=-1)
    actual_ids = gen_ids[:len(gen_logits)]
    token_lps = log_probs[torch.arange(len(actual_ids)), actual_ids]
    mean_lp = token_lps.mean().item()
    return text, float(np.exp(mean_lp))

def fmt(tokenizer, msgs):
    try: return tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    except: return msgs[-1]["content"]

def load_humaneval():
    ds = load_dataset("openai_humaneval", split="test")
    return [{"task_id": i["task_id"], "prompt": i["prompt"], "canonical_solution": i["canonical_solution"],
             "test": i["test"], "entry_point": i["entry_point"]} for i in ds]

# ==================== MAIN V3 EXPERIMENT ====================

def run_v3_experiment(model, tokenizer, problems, model_name):
    """
    Run complete V3 experiment for one model:
    - n=11 samples (10 for confidence, 1 independent for label)
    - log-prob with isotonic/Platt calibration
    - verbal at both tau=0.1 and tau=0.8
    - AST-clustering proxy
    - TACE metric
    """
    print(f"\n{'='*60}")
    print(f"  V3 EXPERIMENT: {model_name} on HumanEval ({len(problems)} problems)")
    print(f"{'='*60}", flush=True)
    t0 = time.time()
    
    data = []
    latencies = []
    
    for idx, prob in enumerate(problems):
        if idx % 20 == 0: print(f"    [{idx}/{len(problems)}] ({time.time()-t0:.0f}s)", flush=True)
        
        prompt = prob["prompt"]
        pi = fmt(tokenizer, [{"role": "user", "content": f"Complete the following Python function. Only output the complete function, no explanations.\n\n{prompt}"}])
        
        # Generate n+1=11 samples: first 10 for confidence, 11th for independent label
        ts = time.time()
        all_samples = gen(model, tokenizer, pi, 11, temp=0.8)
        latencies.append((time.time() - ts) / 11)
        
        conf_samples = all_samples[:10]
        label_sample = all_samples[10]  # INDEPENDENT label
        
        # Execute all
        conf_codes = [extract_code(s) for s in conf_samples]
        conf_ok = [execute_humaneval(c, prob) for c in conf_codes]
        label_code = extract_code(label_sample)
        label_ok = execute_humaneval(label_code, prob)
        
        # Also get first-sample label (for comparison with V2)
        first_sample_ok = conf_ok[0]
        
        # Sampling confidence (from 10 conf samples)
        sampling_conf = sum(conf_ok) / len(conf_ok)
        
        # AST-clustering proxy: count unique AST structures
        ast_clusters = len(set(normalize_code_for_ast(c) for c in conf_codes))
        # Agreement = 1 - (unique_clusters - 1) / (n - 1), clamped to [0,1]
        ast_agreement = max(0.0, 1.0 - (ast_clusters - 1) / 9.0)
        
        # Log-probability confidence
        try:
            _, logprob_conf = gen_with_logprob(model, tokenizer, pi, temp=0.8)
        except:
            logprob_conf = 0.5
        
        # Verbal at tau=0.1 (standard)
        ci_01 = fmt(tokenizer, [{"role": "user", "content": f"Rate your confidence from 1-5 (1=very unsure, 5=very confident). Format: CONFIDENCE: [N]\nThen provide the solution.\n\n{prompt}"}])
        resp_01 = gen(model, tokenizer, ci_01, 1, temp=0.1)[0]
        conf_verbal_01 = extract_numeric_conf(resp_01)
        
        # Verbal at tau=0.8 (same as sampling — apples-to-apples)
        resp_08 = gen(model, tokenizer, ci_01, 1, temp=0.8)[0]
        conf_verbal_08 = extract_numeric_conf(resp_08)
        
        data.append({
            "task_id": prob["task_id"],
            "independent_label": label_ok,  # NEW: independent draw
            "first_sample_label": first_sample_ok,  # For comparison
            "pass_count": sum(conf_ok),
            "sampling_conf": sampling_conf,
            "logprob_conf": logprob_conf,
            "ast_agreement": ast_agreement,
            "ast_clusters": ast_clusters,
            "verbal_01": conf_verbal_01,
            "verbal_08": conf_verbal_08,
        })
    
    elapsed = time.time() - t0
    
    # Labels: use INDEPENDENT draw
    indep_labels = [d["independent_label"] for d in data]
    first_labels = [d["first_sample_label"] for d in data]
    
    results = {
        "model": model_name, "n_problems": len(problems), "time_seconds": elapsed,
        "mean_latency_per_sample_s": float(np.mean(latencies)),
        "pass_at_1_independent": float(np.mean(indep_labels)),
        "pass_at_1_first_sample": float(np.mean(first_labels)),
    }
    
    # ---- Compute metrics with INDEPENDENT labels ----
    methods = {
        "sampling": [d["sampling_conf"] for d in data],
        "logprob": [d["logprob_conf"] for d in data],
        "ast_proxy": [d["ast_agreement"] for d in data],
        "verbal_tau01": [d["verbal_01"] for d in data],
        "verbal_tau08": [d["verbal_08"] for d in data],
    }
    
    for mname, confs in methods.items():
        ece, bins = compute_ece(confs, indep_labels)
        tace = compute_tace(confs, indep_labels)
        metrics = bootstrap_all(confs, indep_labels)
        
        results[f"{mname}_ece"] = ece
        results[f"{mname}_ece_ci"] = metrics["ece_ci"]
        results[f"{mname}_brier"] = metrics["brier"]
        results[f"{mname}_brier_ci"] = metrics["brier_ci"]
        results[f"{mname}_auroc"] = metrics["auroc"]
        results[f"{mname}_auroc_ci"] = metrics["auroc_ci"]
        results[f"{mname}_tace"] = tace
        results[f"{mname}_tace_ci"] = metrics["tace_ci"]
        results[f"{mname}_bins"] = bins
        results[f"{mname}_confs"] = confs
        
        print(f"    {mname:15s}: ECE={ece:.4f} [{metrics['ece_ci'][0]:.4f},{metrics['ece_ci'][1]:.4f}] "
              f"AUROC={metrics['auroc']:.4f} [{metrics['auroc_ci'][0]:.4f},{metrics['auroc_ci'][1]:.4f}] "
              f"TACE={tace:.4f}")
    
    # ---- Also compute with FIRST SAMPLE labels for V2 comparison ----
    for mname, confs in methods.items():
        ece_fs, _ = compute_ece(confs, first_labels)
        try: auroc_fs = compute_auroc(confs, first_labels)
        except: auroc_fs = float('nan')
        results[f"{mname}_ece_firstsample"] = ece_fs
        results[f"{mname}_auroc_firstsample"] = auroc_fs
    
    # ---- Isotonic and Platt calibration on log-prob ----
    lp_confs = np.array(methods["logprob"])
    lp_labels = np.array(indep_labels)
    
    # 5-fold cross-validated calibration
    from sklearn.model_selection import KFold
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    iso_preds = np.zeros(len(lp_confs))
    platt_preds = np.zeros(len(lp_confs))
    
    for train_idx, test_idx in kf.split(lp_confs):
        try:
            # Isotonic
            ir = IsotonicRegression(out_of_bounds='clip')
            ir.fit(lp_confs[train_idx], lp_labels[train_idx])
            iso_preds[test_idx] = ir.predict(lp_confs[test_idx])
            # Platt
            if len(np.unique(lp_labels[train_idx])) >= 2:
                lr = LogisticRegression()
                lr.fit(lp_confs[train_idx].reshape(-1,1), lp_labels[train_idx])
                platt_preds[test_idx] = lr.predict_proba(lp_confs[test_idx].reshape(-1,1))[:,1]
            else:
                platt_preds[test_idx] = np.mean(lp_labels[train_idx])
        except Exception as e:
            print(f"    Calibration fold error: {e}")
            iso_preds[test_idx] = lp_confs[test_idx]
            platt_preds[test_idx] = np.mean(lp_labels) if len(lp_labels) > 0 else 0.5
    
    for cal_name, cal_confs in [("logprob_isotonic", iso_preds.tolist()), ("logprob_platt", platt_preds.tolist())]:
        ece, bins = compute_ece(cal_confs, indep_labels)
        tace = compute_tace(cal_confs, indep_labels)
        metrics = bootstrap_all(cal_confs, indep_labels)
        results[f"{cal_name}_ece"] = ece
        results[f"{cal_name}_ece_ci"] = metrics["ece_ci"]
        results[f"{cal_name}_brier"] = metrics["brier"]
        results[f"{cal_name}_brier_ci"] = metrics["brier_ci"]
        results[f"{cal_name}_auroc"] = metrics["auroc"]
        results[f"{cal_name}_auroc_ci"] = metrics["auroc_ci"]
        results[f"{cal_name}_tace"] = tace
        results[f"{cal_name}_confs"] = cal_confs
        print(f"    {cal_name:15s}: ECE={ece:.4f} AUROC={metrics['auroc']:.4f} (post-hoc calibrated)")
    
    results["indep_labels"] = indep_labels
    results["first_labels"] = first_labels
    results["per_problem"] = data
    
    # Distributions
    for k in ["verbal_01", "verbal_08"]:
        vals = [d[k] for d in data]
        results[f"{k}_dist"] = dict(Counter([round(v, 1) for v in vals]))
    
    return results


def run_sft_discrimination(humaneval):
    """SFT per-problem discrimination: hard vs easy subsets."""
    print("\n" + "="*60)
    print("  SFT DISCRIMINATION ANALYSIS")
    print("="*60, flush=True)
    
    if not os.path.exists(os.path.join(SFT_DIR, "adapter_config.json")):
        print("  SFT model not found, skipping.")
        return None
    
    BASE = "Qwen/Qwen2.5-Coder-7B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(BASE, trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    base_m = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    sft_m = PeftModel.from_pretrained(base_m, SFT_DIR)
    sft_m.eval()
    
    subset = humaneval[:80]
    t0 = time.time()
    
    sft_data = []
    for idx, prob in enumerate(subset):
        if idx % 10 == 0: print(f"    [{idx}/{len(subset)}] ({time.time()-t0:.0f}s)", flush=True)
        
        pi = fmt(tokenizer, [{"role": "user", "content": f"Complete the following Python function. Only output the function.\n\n{prob['prompt']}"}])
        samples = gen(sft_m, tokenizer, pi, 10, temp=0.8)
        sample_ok = [execute_humaneval(extract_code(s), prob) for s in samples]
        pr = sum(sample_ok) / len(sample_ok)
        
        ci = fmt(tokenizer, [{"role": "system", "content": "Before solving, state your confidence:\n- 'I am confident this solution is correct' for high confidence\n- 'This should work for most cases, but please verify edge cases' for medium\n- 'I am not confident in this solution, it may contain bugs' for low\nThen solve."},
                             {"role": "user", "content": f"State confidence and complete:\n\n{prob['prompt']}"}])
        cresp = gen(sft_m, tokenizer, ci, 1, temp=0.1)[0]
        vc = extract_trained_conf(cresp)
        
        sft_data.append({"task_id": prob["task_id"], "pass_rate": pr, "verbal_conf": vc,
                        "correct": sample_ok[0], "pass_count": sum(sample_ok)})
    
    # Split into easy (pass_rate >= 0.8) and hard (pass_rate < 0.5) subsets
    easy = [d for d in sft_data if d["pass_rate"] >= 0.8]
    hard = [d for d in sft_data if d["pass_rate"] < 0.5]
    medium = [d for d in sft_data if 0.5 <= d["pass_rate"] < 0.8]
    
    results = {"n_easy": len(easy), "n_hard": len(hard), "n_medium": len(medium)}
    
    for subset_name, subset_data in [("all", sft_data), ("easy", easy), ("hard", hard)]:
        if len(subset_data) < 3: continue
        confs = [d["verbal_conf"] for d in subset_data]
        labels = [float(d["correct"]) for d in subset_data]
        ece, _ = compute_ece(confs, labels)
        try: auroc = compute_auroc(confs, labels)
        except: auroc = float('nan')
        results[f"{subset_name}_verbal_ece"] = ece
        results[f"{subset_name}_verbal_auroc"] = auroc
        results[f"{subset_name}_mean_conf"] = float(np.mean(confs))
        results[f"{subset_name}_mean_correct"] = float(np.mean(labels))
        results[f"{subset_name}_conf_dist"] = dict(Counter([round(v,1) for v in confs]))
        print(f"    {subset_name:8s}: n={len(subset_data):3d}, mean_conf={np.mean(confs):.3f}, ECE={ece:.4f}, AUROC={auroc:.4f}")
    
    results["per_problem"] = sft_data
    
    del sft_m, base_m, tokenizer; torch.cuda.empty_cache(); gc.collect()
    
    sp = os.path.join(RESULTS_DIR, "sft_discrimination.json")
    with open(sp, 'w') as f: json.dump(results, f, indent=2)
    print(f"  Saved: {sp}")
    return results


# ==================== MAIN ====================

if __name__ == "__main__":
    t_start = time.time()
    print("="*60)
    print("DL4C V3: COMPLETE REVISED EXPERIMENTS")
    print("="*60, flush=True)
    
    harness = log_harness_info()
    humaneval = load_humaneval()
    print(f"HumanEval: {len(humaneval)} problems")
    
    # Run V3 experiment for each model
    for model_key, model_path in MODELS:
        result_path = os.path.join(RESULTS_DIR, f"v3_{model_key}_humaneval.json")
        if os.path.exists(result_path):
            print(f"\n{model_key} already done, skipping.")
            continue
        
        print(f"\n  Loading {model_path}...", flush=True)
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(model_path, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
        if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
        model.eval()
        
        results = run_v3_experiment(model, tokenizer, humaneval, model_key)
        with open(result_path, 'w') as f: json.dump(results, f, indent=2)
        print(f"  Saved: {result_path}")
        
        del model, tokenizer; torch.cuda.empty_cache(); gc.collect()
    
    # SFT discrimination analysis
    sft_disc_path = os.path.join(RESULTS_DIR, "sft_discrimination.json")
    if not os.path.exists(sft_disc_path):
        run_sft_discrimination(humaneval)
    else:
        print("\nSFT discrimination already done, skipping.")
    
    total = (time.time() - t_start) / 60
    print(f"\n{'='*60}")
    print(f"ALL V3 EXPERIMENTS COMPLETE ({total:.1f} min)")
    print("="*60)
    for f_name in sorted(os.listdir(RESULTS_DIR)):
        print(f"  {f_name} ({os.path.getsize(os.path.join(RESULTS_DIR, f_name))} bytes)")
