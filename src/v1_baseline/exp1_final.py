"""
Experiment 1 (Final): Baseline Calibration Measurement
Uses HF transformers with optimized generation. No vLLM dependency.
"""

import json
import os
import sys
import time
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
import re
import subprocess
import tempfile
from math import comb

RESULTS_DIR = "/home/ubuntu/dl4c_experiments/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

MODELS = [
    ("qwen2.5-coder-7b", "Qwen/Qwen2.5-Coder-7B-Instruct"),
    ("deepseek-coder-6.7b", "deepseek-ai/deepseek-coder-6.7b-instruct"),
]

NUM_SAMPLES = 10
MAX_TOKENS = 512


def compute_ece(confidences, accuracies, n_bins=10):
    c, a = np.array(confidences, dtype=float), np.array(accuracies, dtype=float)
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    bin_data = []
    for i in range(n_bins):
        mask = (c >= bin_boundaries[i]) & (c < bin_boundaries[i + 1])
        if i == n_bins - 1:
            mask = (c >= bin_boundaries[i]) & (c <= bin_boundaries[i + 1])
        if mask.sum() > 0:
            ba = a[mask].mean(); bc = c[mask].mean(); bs = int(mask.sum())
            ece += (bs / len(c)) * abs(ba - bc)
            bin_data.append({"bin_lower": float(bin_boundaries[i]), "bin_upper": float(bin_boundaries[i+1]),
                           "accuracy": float(ba), "confidence": float(bc), "count": bs})
    return float(ece), bin_data

def compute_brier(c, a): return float(np.mean((np.array(c) - np.array(a)) ** 2))

def compute_auroc(c, a):
    from sklearn.metrics import roc_auc_score
    c, a = np.array(c), np.array(a)
    return float(roc_auc_score(a, c)) if len(np.unique(a)) >= 2 else float('nan')

def execute_code_safe(code, test_code, timeout=10):
    full = code + "\n" + test_code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(full); f.flush()
        try:
            r = subprocess.run(['python3', f.name], capture_output=True, text=True, timeout=timeout)
            return r.returncode == 0
        except: return False
        finally: os.unlink(f.name)

def extract_code(resp):
    blocks = re.findall(r'```(?:python)?\n?(.*?)```', resp, re.DOTALL)
    return blocks[0].strip() if blocks else resp.strip()

def extract_verbalized_conf(resp):
    m = re.search(r'CONFIDENCE:\s*(\d)', resp)
    if m: return min(max(int(m.group(1)), 1), 5) / 5.0
    m = re.search(r'(\d)\s*/\s*5', resp)
    if m: return int(m.group(1)) / 5.0
    rl = resp.lower()
    if 'very confident' in rl: return 0.9
    if 'confident' in rl and 'not' not in rl: return 0.8
    if 'fairly' in rl or 'should work' in rl: return 0.6
    if 'unsure' in rl or 'not confident' in rl: return 0.3
    return 0.6

def load_humaneval():
    ds = load_dataset("openai_humaneval", split="test")
    return [{"task_id": i["task_id"], "prompt": i["prompt"], "canonical_solution": i["canonical_solution"],
             "test": i["test"], "entry_point": i["entry_point"]} for i in ds]

def load_mbpp():
    ds = load_dataset("google-research-datasets/mbpp", "sanitized", split="test")
    return [{"task_id": f"mbpp_{i['task_id']}", "prompt": i["prompt"],
             "test": "\n".join(i["test_list"]), "code": i["code"]} for i in ds]


@torch.no_grad()
def generate_samples(model, tokenizer, prompt_text, n_samples, temperature=0.8, max_tokens=512):
    """Generate multiple samples efficiently."""
    input_ids = tokenizer(prompt_text, return_tensors="pt", truncation=True, max_length=2048).input_ids.to(model.device)
    
    results = []
    for _ in range(n_samples):
        out = model.generate(
            input_ids,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
        )
        gen_ids = out[0][input_ids.shape[1]:]
        text = tokenizer.decode(gen_ids, skip_special_tokens=True)
        
        # Compute logit confidence via a forward pass on generated tokens
        # Use the mean of top-1 token probabilities
        full_ids = out[0].unsqueeze(0)
        logits = model(full_ids).logits[0]
        # Only look at positions corresponding to generated tokens
        gen_logits = logits[input_ids.shape[1]-1:-1]  # shifted by 1 for next-token prediction
        probs = torch.softmax(gen_logits, dim=-1)
        # Probability assigned to the actual generated tokens
        gen_token_ids = gen_ids[:len(gen_logits)]
        token_probs = probs[torch.arange(len(gen_token_ids)), gen_token_ids]
        logit_conf = token_probs.mean().item()
        
        results.append({"text": text, "logit_conf": logit_conf})
    
    return results


def run_model(model_key, model_path, humaneval, mbpp):
    print(f"\n{'#'*60}")
    print(f"# Model: {model_key}")
    print(f"{'#'*60}", flush=True)
    
    print(f"Loading {model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model.eval()
    print("Model loaded.", flush=True)
    
    all_results = {}
    
    for bench_name, problems, is_humaneval in [("humaneval", humaneval, True), ("mbpp", mbpp, False)]:
        print(f"\n  --- {bench_name} ({len(problems)} problems) ---", flush=True)
        t0 = time.time()
        
        logit_confs, sampling_confs, verbal_confs, corr = [], [], [], []
        per_problem = []
        
        for idx, prob in enumerate(problems):
            if idx % 10 == 0:
                print(f"    [{idx}/{len(problems)}] ({time.time()-t0:.0f}s)", flush=True)
            
            prompt = prob["prompt"]
            
            # Code generation prompt
            msgs = [{"role": "user", "content": f"Complete the following Python function. Only output the complete function, no explanations.\n\n{prompt}"}]
            try:
                ti = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
            except:
                ti = msgs[-1]["content"]
            
            # Generate samples
            samples = generate_samples(model, tokenizer, ti, NUM_SAMPLES, temperature=0.8, max_tokens=MAX_TOKENS)
            
            sample_correct = []
            sample_lconfs = []
            for s in samples:
                code = extract_code(s["text"])
                if is_humaneval:
                    fc = code if prompt in code else prompt + code
                    tc = prob["test"] + f"\ncheck({prob['entry_point']})"
                else:
                    fc, tc = code, prob["test"]
                ok = execute_code_safe(fc, tc)
                sample_correct.append(ok)
                sample_lconfs.append(s["logit_conf"])
            
            pr = sum(sample_correct) / len(sample_correct)
            ml = np.mean(sample_lconfs)
            
            # Verbalized confidence
            cmsg = [{"role": "user", "content": f"Before solving, rate your confidence from 1-5 (1=very unsure, 5=very confident). Format: CONFIDENCE: [N]\nThen provide the solution.\n\n{prompt}"}]
            try: cti = tokenizer.apply_chat_template(cmsg, tokenize=False, add_generation_prompt=True)
            except: cti = cmsg[-1]["content"]
            
            csamples = generate_samples(model, tokenizer, cti, 1, temperature=0.1, max_tokens=MAX_TOKENS)
            vc = extract_verbalized_conf(csamples[0]["text"])
            
            logit_confs.append(float(ml))
            sampling_confs.append(float(pr))
            verbal_confs.append(float(vc))
            corr.append(float(sample_correct[0]))
            per_problem.append({"task_id": prob.get("task_id", f"{bench_name}_{idx}"),
                               "pass_count": sum(sample_correct), "pass_rate": float(pr)})
        
        elapsed = time.time() - t0
        results = {"model": model_key, "benchmark": bench_name, "time_seconds": elapsed,
                   "num_problems": len(problems), "num_samples": NUM_SAMPLES}
        
        for cn, cv in [("logit", logit_confs), ("sampling", sampling_confs), ("verbalized", verbal_confs)]:
            ece, bins = compute_ece(cv, corr)
            results[f"{cn}_ece"] = ece
            results[f"{cn}_brier"] = compute_brier(cv, corr)
            results[f"{cn}_auroc"] = compute_auroc(cv, corr)
            results[f"{cn}_bins"] = bins
            results[f"{cn}_confidences"] = cv
            print(f"    {cn}: ECE={ece:.4f}, Brier={results[f'{cn}_brier']:.4f}, AUROC={results[f'{cn}_auroc']:.4f}")
        
        results["correctness"] = corr
        results["per_problem"] = per_problem
        p1 = np.mean(corr)
        p10_list = []
        for pp in per_problem:
            n, c = NUM_SAMPLES, pp["pass_count"]
            k = min(10, n)
            p10_list.append(1.0 if n - c < k else 1.0 - comb(n - c, k) / comb(n, k))
        results["pass_at_1"] = float(p1)
        results["pass_at_10"] = float(np.mean(p10_list))
        print(f"    pass@1={p1:.4f}, pass@10={results['pass_at_10']:.4f}")
        
        sp = os.path.join(RESULTS_DIR, f"exp1_{model_key}_{bench_name}.json")
        with open(sp, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"    Saved: {sp}", flush=True)
        all_results[f"{model_key}_{bench_name}"] = results
    
    del model, tokenizer
    torch.cuda.empty_cache()
    import gc; gc.collect()
    return all_results


if __name__ == "__main__":
    print("="*60)
    print("EXPERIMENT 1: Baseline Calibration")
    print("="*60, flush=True)
    
    humaneval = load_humaneval()
    mbpp = load_mbpp()
    print(f"HumanEval: {len(humaneval)}, MBPP: {len(mbpp)}")
    
    all_results = {}
    for mk, mp in MODELS:
        try:
            r = run_model(mk, mp, humaneval, mbpp)
            all_results.update(r)
        except Exception as e:
            print(f"  ERROR with {mk}: {e}")
            import traceback; traceback.print_exc()
    
    summary = {}
    for k, r in all_results.items():
        summary[k] = {m: r.get(m) for m in [
            "pass_at_1", "pass_at_10", "logit_ece", "sampling_ece", "verbalized_ece",
            "logit_brier", "sampling_brier", "verbalized_brier",
            "logit_auroc", "sampling_auroc", "verbalized_auroc"]}
    
    with open(os.path.join(RESULTS_DIR, "experiment1_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "="*60)
    print("EXPERIMENT 1 COMPLETE")
    print("="*60)
    for k, s in summary.items():
        print(f"\n{k}:")
        for m, v in s.items():
            if v is not None: print(f"  {m}: {v:.4f}")
