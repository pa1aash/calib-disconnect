"""
Streamlined Experiment 1: Baseline Calibration Measurement
Optimized for faster execution: fewer samples, focused evaluation.
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

MODELS = {
    "qwen2.5-coder-7b": "Qwen/Qwen2.5-Coder-7B-Instruct",
    "deepseek-coder-6.7b": "deepseek-ai/deepseek-coder-6.7b-instruct",
    "starcoder2-7b": "bigcode/starcoder2-7b-instruct-v0.1",
}

NUM_SAMPLES = 10  # Reduced from 20 for speed
TEMPERATURE = 0.8
MAX_NEW_TOKENS = 512


def compute_ece(confidences, accuracies, n_bins=10):
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    bin_data = []
    for i in range(n_bins):
        if i == n_bins - 1:
            mask = (confidences >= bin_boundaries[i]) & (confidences <= bin_boundaries[i + 1])
        else:
            mask = (confidences >= bin_boundaries[i]) & (confidences < bin_boundaries[i + 1])
        if mask.sum() > 0:
            bin_acc = accuracies[mask].mean()
            bin_conf = confidences[mask].mean()
            bin_size = mask.sum()
            ece += (bin_size / len(confidences)) * abs(bin_acc - bin_conf)
            bin_data.append({"bin_lower": float(bin_boundaries[i]), "bin_upper": float(bin_boundaries[i+1]),
                           "accuracy": float(bin_acc), "confidence": float(bin_conf), "count": int(bin_size)})
    return float(ece), bin_data


def compute_brier(c, a): return float(np.mean((c - a) ** 2))

def compute_auroc(c, a):
    from sklearn.metrics import roc_auc_score
    if len(np.unique(a)) < 2: return float('nan')
    return float(roc_auc_score(a, c))


def execute_code_safe(code, test_code, timeout=10):
    full_code = code + "\n" + test_code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(full_code)
        f.flush()
        try:
            r = subprocess.run(['python3', f.name], capture_output=True, text=True, timeout=timeout)
            return r.returncode == 0
        except: return False
        finally: os.unlink(f.name)


def extract_code(response):
    blocks = re.findall(r'```(?:python)?\n?(.*?)```', response, re.DOTALL)
    return blocks[0].strip() if blocks else response.strip()


def extract_verbalized_conf(response):
    m = re.search(r'CONFIDENCE:\s*(\d)', response)
    if m: return min(max(int(m.group(1)), 1), 5) / 5.0
    m = re.search(r'(\d)\s*/\s*5', response)
    if m: return int(m.group(1)) / 5.0
    rl = response.lower()
    if 'very confident' in rl or 'certainly correct' in rl: return 0.9
    if 'confident' in rl and 'not' not in rl: return 0.8
    if 'fairly' in rl or 'should work' in rl: return 0.6
    if 'unsure' in rl or 'not confident' in rl: return 0.3
    return 0.6


def run_model_benchmark(model_key, model_path, problems, bench_name, is_humaneval):
    print(f"\n{'='*50}")
    print(f"  {model_key} on {bench_name} ({len(problems)} problems)")
    print(f"{'='*50}")
    
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    model.eval()
    
    logit_confs, sampling_confs, verbal_confs, correctness = [], [], [], []
    per_problem = []
    
    for idx, prob in enumerate(problems):
        if idx % 25 == 0: print(f"    [{idx}/{len(problems)}]", flush=True)
        
        prompt = prob["prompt"]
        
        # --- Sampling for logit + sampling confidence ---
        msgs = [{"role": "system", "content": "Complete the Python function. Only output code, no explanations."},
                {"role": "user", "content": f"Complete:\n\n{prompt}"}]
        try:
            ti = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        except: ti = msgs[-1]["content"]
        
        iids = tokenizer(ti, return_tensors="pt", truncation=True, max_length=2048).input_ids.to(model.device)
        
        sample_ok = []
        sample_lconfs = []
        
        for s in range(NUM_SAMPLES):
            with torch.no_grad():
                out = model.generate(iids, max_new_tokens=MAX_NEW_TOKENS, temperature=TEMPERATURE,
                                     top_p=0.95, do_sample=True, return_dict_in_generate=True,
                                     output_scores=True, pad_token_id=tokenizer.pad_token_id)
            
            gen = out.sequences[0][iids.shape[1]:]
            resp = tokenizer.decode(gen, skip_special_tokens=True)
            code = extract_code(resp)
            
            # Logit confidence
            if out.scores:
                tprobs = [torch.softmax(sc[0], dim=-1).max().item() for sc in out.scores[:50]]  # Cap at 50 tokens
                lc = np.mean(tprobs)
            else: lc = 0.5
            
            # Execute
            if is_humaneval:
                fc = code if prompt in code else prompt + code
                tc = prob["test"] + f"\ncheck({prob['entry_point']})"
            else:
                fc = code
                tc = prob["test"]
            ok = execute_code_safe(fc, tc)
            
            sample_ok.append(ok)
            sample_lconfs.append(lc)
        
        pr = sum(sample_ok) / len(sample_ok)
        ml = np.mean(sample_lconfs)
        
        # --- Verbalized confidence ---
        cmsg = [{"role": "system", "content": "Before solving, rate confidence 1-5 (1=unsure, 5=very confident). Format: CONFIDENCE: [N]. Then solve."},
                {"role": "user", "content": f"Rate confidence and solve:\n\n{prompt}"}]
        try: cti = tokenizer.apply_chat_template(cmsg, tokenize=False, add_generation_prompt=True)
        except: cti = cmsg[-1]["content"]
        ciids = tokenizer(cti, return_tensors="pt", truncation=True, max_length=2048).input_ids.to(model.device)
        
        with torch.no_grad():
            cout = model.generate(ciids, max_new_tokens=MAX_NEW_TOKENS, temperature=0.1, do_sample=True, pad_token_id=tokenizer.pad_token_id)
        cresp = tokenizer.decode(cout[0][ciids.shape[1]:], skip_special_tokens=True)
        vc = extract_verbalized_conf(cresp)
        
        logit_confs.append(ml)
        sampling_confs.append(pr)
        verbal_confs.append(vc)
        correctness.append(float(sample_ok[0]))
        per_problem.append({"task_id": prob.get("task_id", f"{bench_name}_{idx}"), "pass_count": sum(sample_ok), "pass_rate": pr})
    
    # Metrics
    results = {"model": model_key, "benchmark": bench_name}
    for cname, confs in [("logit", logit_confs), ("sampling", sampling_confs), ("verbalized", verbal_confs)]:
        c, a = np.array(confs), np.array(correctness)
        ece, bins = compute_ece(c, a)
        results[f"{cname}_ece"] = ece
        results[f"{cname}_brier"] = compute_brier(c, a)
        results[f"{cname}_auroc"] = compute_auroc(c, a)
        results[f"{cname}_bins"] = bins
        results[f"{cname}_confidences"] = [float(x) for x in confs]
        print(f"    {cname}: ECE={ece:.4f}, Brier={results[f'{cname}_brier']:.4f}, AUROC={results[f'{cname}_auroc']:.4f}")
    
    results["correctness"] = [float(x) for x in correctness]
    results["per_problem"] = per_problem
    
    p1 = np.mean(correctness)
    p10 = np.mean([1.0 - comb(NUM_SAMPLES - pp["pass_count"], min(10, NUM_SAMPLES)) / comb(NUM_SAMPLES, min(10, NUM_SAMPLES)) if NUM_SAMPLES - pp["pass_count"] >= min(10, NUM_SAMPLES) else 1.0 for pp in per_problem])
    results["pass_at_1"] = float(p1)
    results["pass_at_10"] = float(p10)
    print(f"    pass@1={p1:.4f}, pass@10={p10:.4f}")
    
    # Save
    sp = os.path.join(RESULTS_DIR, f"exp1_{model_key}_{bench_name}.json")
    with open(sp, 'w') as f: json.dump(results, f, indent=2)
    print(f"    Saved: {sp}")
    
    del model, tokenizer
    torch.cuda.empty_cache()
    return results


if __name__ == "__main__":
    print("EXPERIMENT 1: Baseline Calibration Measurement")
    print("="*60)
    
    # Load benchmarks
    he_ds = load_dataset("openai_humaneval", split="test")
    humaneval = [{"task_id": i["task_id"], "prompt": i["prompt"], "canonical_solution": i["canonical_solution"],
                  "test": i["test"], "entry_point": i["entry_point"]} for i in he_ds]
    
    mbpp_ds = load_dataset("google-research-datasets/mbpp", "sanitized", split="test")
    mbpp = [{"task_id": f"mbpp_{i['task_id']}", "prompt": i["prompt"], 
             "test": "\n".join(i["test_list"]), "code": i["code"]} for i in mbpp_ds]
    
    print(f"HumanEval: {len(humaneval)}, MBPP: {len(mbpp)}")
    
    all_res = {}
    for mk, mp in MODELS.items():
        print(f"\n### {mk} ###")
        try:
            r = run_model_benchmark(mk, mp, humaneval, "humaneval", True)
            all_res[f"{mk}_humaneval"] = r
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback; traceback.print_exc()
        
        try:
            r = run_model_benchmark(mk, mp, mbpp, "mbpp", False)
            all_res[f"{mk}_mbpp"] = r
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback; traceback.print_exc()
    
    # Summary
    summary = {}
    for k, r in all_res.items():
        summary[k] = {m: r.get(m) for m in ["pass_at_1","pass_at_10","logit_ece","sampling_ece","verbalized_ece","logit_auroc","sampling_auroc","verbalized_auroc"]}
    
    with open(os.path.join(RESULTS_DIR, "experiment1_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "="*60)
    print("EXPERIMENT 1 COMPLETE")
    print("="*60)
    for k, s in summary.items():
        print(f"\n{k}:")
        for m, v in s.items():
            if v is not None: print(f"  {m}: {v:.4f}")
