"""
Experiment 1 (Optimized): Baseline Calibration Measurement
Removes forward-pass logit computation. Uses token-level log-probs from generate().
"""

import json
import os
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

def compute_ece(c, a, n_bins=10):
    c, a = np.array(c, dtype=float), np.array(a, dtype=float)
    bounds = np.linspace(0, 1, n_bins + 1)
    ece = 0.0; bins = []
    for i in range(n_bins):
        m = (c >= bounds[i]) & (c < bounds[i+1]) if i < n_bins-1 else (c >= bounds[i]) & (c <= bounds[i+1])
        if m.sum() > 0:
            ba, bc, bs = float(a[m].mean()), float(c[m].mean()), int(m.sum())
            ece += (bs / len(c)) * abs(ba - bc)
            bins.append({"bin_lower": float(bounds[i]), "bin_upper": float(bounds[i+1]), "accuracy": ba, "confidence": bc, "count": bs})
    return float(ece), bins

def compute_brier(c, a): return float(np.mean((np.array(c) - np.array(a)) ** 2))

def compute_auroc(c, a):
    from sklearn.metrics import roc_auc_score
    c, a = np.array(c), np.array(a)
    return float(roc_auc_score(a, c)) if len(np.unique(a)) >= 2 else float('nan')

def execute_code_safe(code, test_code, timeout=10):
    full = code + "\n" + test_code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(full); f.flush()
        try: return subprocess.run(['python3', f.name], capture_output=True, text=True, timeout=timeout).returncode == 0
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
    if 'should work' in rl or 'most cases' in rl: return 0.6
    if 'unsure' in rl or 'not confident' in rl or 'not sure' in rl: return 0.3
    return 0.6

@torch.no_grad()
def batch_generate(model, tokenizer, prompt, n, temp=0.8):
    """Generate n samples from a single prompt."""
    ids = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048).input_ids.to(model.device)
    results = []
    for _ in range(n):
        out = model.generate(ids, max_new_tokens=MAX_TOKENS, temperature=temp, top_p=0.95, do_sample=True, pad_token_id=tokenizer.pad_token_id)
        text = tokenizer.decode(out[0][ids.shape[1]:], skip_special_tokens=True)
        results.append(text)
    return results

def run_model(model_key, model_path, humaneval, mbpp):
    print(f"\n{'#'*60}\n# Model: {model_key}\n{'#'*60}", flush=True)
    
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    model.eval()
    print("Model loaded.", flush=True)
    
    all_results = {}
    
    for bname, probs, is_he in [("humaneval", humaneval, True), ("mbpp", mbpp, False)]:
        print(f"\n  --- {bname} ({len(probs)} problems) ---", flush=True)
        t0 = time.time()
        
        sampling_confs, verbal_confs, corr_list = [], [], []
        per_problem = []
        
        for idx, prob in enumerate(probs):
            if idx % 10 == 0: print(f"    [{idx}/{len(probs)}] ({time.time()-t0:.0f}s)", flush=True)
            
            prompt = prob["prompt"]
            
            # Format prompt
            msgs = [{"role": "user", "content": f"Complete the following Python function. Only output the complete function, no explanations.\n\n{prompt}"}]
            try: pi = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
            except: pi = msgs[-1]["content"]
            
            # Generate samples
            samples = batch_generate(model, tokenizer, pi, NUM_SAMPLES, temp=0.8)
            
            sample_ok = []
            for s in samples:
                code = extract_code(s)
                if is_he:
                    fc = code if prompt in code else prompt + code
                    tc = prob["test"] + f"\ncheck({prob['entry_point']})"
                else: fc, tc = code, prob["test"]
                sample_ok.append(execute_code_safe(fc, tc))
            
            pr = sum(sample_ok) / len(sample_ok)
            
            # Verbalized confidence (single generation)
            cmsg = [{"role": "user", "content": f"Rate your confidence from 1-5 (1=unsure, 5=confident). Format: CONFIDENCE: [N]. Then solve.\n\n{prompt}"}]
            try: ci = tokenizer.apply_chat_template(cmsg, tokenize=False, add_generation_prompt=True)
            except: ci = cmsg[-1]["content"]
            cresp = batch_generate(model, tokenizer, ci, 1, temp=0.1)[0]
            vc = extract_verbalized_conf(cresp)
            
            sampling_confs.append(float(pr))
            verbal_confs.append(float(vc))
            corr_list.append(float(sample_ok[0]))
            per_problem.append({"task_id": prob.get("task_id", f"{bname}_{idx}"), "pass_count": sum(sample_ok), "pass_rate": float(pr)})
        
        elapsed = time.time() - t0
        results = {"model": model_key, "benchmark": bname, "time_seconds": elapsed}
        
        for cn, cv in [("sampling", sampling_confs), ("verbalized", verbal_confs)]:
            ece, bins = compute_ece(cv, corr_list)
            results[f"{cn}_ece"] = ece
            results[f"{cn}_brier"] = compute_brier(cv, corr_list)
            results[f"{cn}_auroc"] = compute_auroc(cv, corr_list)
            results[f"{cn}_bins"] = bins
            results[f"{cn}_confidences"] = cv
            print(f"    {cn}: ECE={ece:.4f}, Brier={results[f'{cn}_brier']:.4f}, AUROC={results[f'{cn}_auroc']:.4f}")
        
        results["correctness"] = corr_list
        results["per_problem"] = per_problem
        results["pass_at_1"] = float(np.mean(corr_list))
        p10 = [1.0 if NUM_SAMPLES - p["pass_count"] < min(10, NUM_SAMPLES) else 1.0 - comb(NUM_SAMPLES - p["pass_count"], min(10, NUM_SAMPLES)) / comb(NUM_SAMPLES, min(10, NUM_SAMPLES)) for p in per_problem]
        results["pass_at_10"] = float(np.mean(p10))
        print(f"    pass@1={results['pass_at_1']:.4f}, pass@10={results['pass_at_10']:.4f}")
        
        sp = os.path.join(RESULTS_DIR, f"exp1_{model_key}_{bname}.json")
        with open(sp, 'w') as f: json.dump(results, f, indent=2)
        print(f"    Saved: {sp}", flush=True)
        all_results[f"{model_key}_{bname}"] = results
    
    del model, tokenizer; torch.cuda.empty_cache()
    return all_results

if __name__ == "__main__":
    print("="*60 + "\nEXPERIMENT 1: Baseline Calibration\n" + "="*60, flush=True)
    
    he = [{"task_id": i["task_id"], "prompt": i["prompt"], "canonical_solution": i["canonical_solution"],
           "test": i["test"], "entry_point": i["entry_point"]} for i in load_dataset("openai_humaneval", split="test")]
    mb = [{"task_id": f"mbpp_{i['task_id']}", "prompt": i["prompt"], "test": "\n".join(i["test_list"]), "code": i["code"]}
          for i in load_dataset("google-research-datasets/mbpp", "sanitized", split="test")]
    print(f"HumanEval: {len(he)}, MBPP: {len(mb)}")
    
    ar = {}
    for mk, mp in MODELS:
        try: ar.update(run_model(mk, mp, he, mb))
        except Exception as e:
            print(f"  ERROR: {e}"); import traceback; traceback.print_exc()
    
    summary = {k: {m: r.get(m) for m in ["pass_at_1","pass_at_10","sampling_ece","verbalized_ece","sampling_brier","verbalized_brier","sampling_auroc","verbalized_auroc"]} for k, r in ar.items()}
    with open(os.path.join(RESULTS_DIR, "experiment1_summary.json"), 'w') as f: json.dump(summary, f, indent=2)
    
    print("\n" + "="*60 + "\nEXPERIMENT 1 COMPLETE\n" + "="*60)
    for k, s in summary.items():
        print(f"\n{k}:")
        for m, v in s.items():
            if v is not None: print(f"  {m}: {v:.4f}")
