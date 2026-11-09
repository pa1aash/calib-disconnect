"""Focused SFT evaluation only. Loads one model at a time."""

import json, os, time, re, subprocess, tempfile, gc
import numpy as np
import torch
from math import comb
from collections import Counter
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from datasets import load_dataset

RESULTS_DIR = "/home/ubuntu/dl4c/results_v2"
SFT_DIR = "/home/ubuntu/dl4c/models/qwen_confidence_sft"
BASE_MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct"
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
            bins.append({"lo": float(bounds[i]), "hi": float(bounds[i+1]), "acc": ba, "conf": bc, "n": bs})
    return float(ece), bins

def compute_brier(c, a): return float(np.mean((np.array(c) - np.array(a)) ** 2))
def compute_auroc(c, a):
    from sklearn.metrics import roc_auc_score
    c, a = np.array(c), np.array(a)
    return float(roc_auc_score(a, c)) if len(np.unique(a)) >= 2 else float('nan')

def bootstrap_all(c, a, n_boot=1000):
    rng = np.random.RandomState(42); c, a = np.array(c), np.array(a)
    ece_fn = lambda c, a: compute_ece(c, a)[0]
    results = {}
    for name, fn in [("ece", ece_fn), ("brier", compute_brier), ("auroc", compute_auroc)]:
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

def extract_trained_conf(resp):
    rl = resp.lower()
    if 'i am confident this solution is correct' in rl: return 0.9
    if 'should work for most cases' in rl or 'please verify' in rl: return 0.6
    if 'not confident' in rl or 'may contain bugs' in rl: return 0.3
    m = re.search(r'CONFIDENCE:\s*(\d)', resp)
    if m: return min(max(int(m.group(1)), 1), 5) / 5.0
    rl = resp.lower()
    if 'confident' in rl and 'not' not in rl: return 0.8
    if 'should work' in rl: return 0.6
    if 'unsure' in rl: return 0.4
    return 0.6

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

def fmt(tokenizer, msgs):
    try: return tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    except: return msgs[-1]["content"]

def eval_model(model, tokenizer, problems, model_name, use_trained_prompt):
    print(f"\n  Evaluating {model_name} on {len(problems)} problems...", flush=True)
    t0 = time.time()
    sampling_confs, verbal_confs, labels, per_problem = [], [], [], []
    
    for idx, prob in enumerate(problems):
        if idx % 10 == 0: print(f"    [{idx}/{len(problems)}] ({time.time()-t0:.0f}s)", flush=True)
        
        pi = fmt(tokenizer, [{"role": "user", "content": f"Complete the following Python function. Only output the function.\n\n{prob['prompt']}"}])
        samples = gen(model, tokenizer, pi, 10, temp=0.8)
        sample_ok = [execute_humaneval(extract_code(s), prob) for s in samples]
        pr = sum(sample_ok) / len(sample_ok)
        
        if use_trained_prompt:
            ci = fmt(tokenizer, [{"role": "system", "content": "Before solving, state your confidence:\n- 'I am confident this solution is correct' for high\n- 'This should work for most cases, but please verify edge cases' for medium\n- 'I am not confident in this solution, it may contain bugs' for low\nThen solve."},
                                 {"role": "user", "content": f"State confidence and complete:\n\n{prob['prompt']}"}])
        else:
            ci = fmt(tokenizer, [{"role": "user", "content": f"Rate confidence 1-5. Format: CONFIDENCE: [N]. Then solve.\n\n{prob['prompt']}"}])
        cresp = gen(model, tokenizer, ci, 1, temp=0.1)[0]
        vc = extract_trained_conf(cresp) if use_trained_prompt else extract_trained_conf(cresp)
        
        sampling_confs.append(float(pr)); verbal_confs.append(float(vc))
        labels.append(float(sample_ok[0]))
        per_problem.append({"task_id": prob["task_id"], "pass_count": sum(sample_ok),
                           "sampling_conf": float(pr), "verbal_conf": float(vc),
                           "correct": float(sample_ok[0])})
    
    elapsed = time.time() - t0
    results = {"model": model_name, "n_problems": len(problems), "time_seconds": elapsed,
               "pass_at_1": float(np.mean(labels))}
    
    for cn, cv in [("sampling", sampling_confs), ("verbal", verbal_confs)]:
        ece, bins = compute_ece(cv, labels)
        metrics = bootstrap_all(cv, labels)
        results[f"{cn}_ece"] = ece; results[f"{cn}_ece_ci"] = metrics["ece_ci"]
        results[f"{cn}_brier"] = metrics["brier"]; results[f"{cn}_brier_ci"] = metrics["brier_ci"]
        results[f"{cn}_auroc"] = metrics["auroc"]; results[f"{cn}_auroc_ci"] = metrics["auroc_ci"]
        results[f"{cn}_bins"] = bins; results[f"{cn}_confs"] = cv
        print(f"    {cn}: ECE={ece:.4f} [{metrics['ece_ci'][0]:.4f},{metrics['ece_ci'][1]:.4f}] AUROC={metrics['auroc']:.4f}")
    
    results["labels"] = labels; results["per_problem"] = per_problem
    results["verbal_dist"] = dict(Counter([round(v, 1) for v in verbal_confs]))
    return results

if __name__ == "__main__":
    print("=== SFT EVALUATION (sequential model loading) ===", flush=True)
    
    ds = load_dataset("openai_humaneval", split="test")
    humaneval = [{"task_id": i["task_id"], "prompt": i["prompt"], "canonical_solution": i["canonical_solution"],
                  "test": i["test"], "entry_point": i["entry_point"]} for i in ds]
    subset = humaneval[:80]
    
    all_results = {}
    
    # 1. Base model
    print("\n--- BASE MODEL ---", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    model.eval()
    all_results["base"] = eval_model(model, tokenizer, subset, "base", False)
    del model, tokenizer; torch.cuda.empty_cache(); gc.collect()
    
    # 2. SFT model  
    print("\n--- SFT MODEL ---", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    base_m = AutoModelForCausalLM.from_pretrained(BASE_MODEL, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    sft_m = PeftModel.from_pretrained(base_m, SFT_DIR)
    sft_m.eval()
    all_results["sft"] = eval_model(sft_m, tokenizer, subset, "sft", True)
    del sft_m, base_m, tokenizer; torch.cuda.empty_cache(); gc.collect()
    
    # Save
    sp = os.path.join(RESULTS_DIR, "sft_evaluation.json")
    with open(sp, 'w') as f: json.dump(all_results, f, indent=2)
    
    # Summary
    print("\n=== BASE vs SFT ===")
    print(f"{'Metric':<25} {'Base':>15} {'SFT':>15} {'Delta':>10}")
    for m in ["pass_at_1", "verbal_ece", "verbal_auroc", "verbal_brier"]:
        bv = all_results["base"].get(m, 0); sv = all_results["sft"].get(m, 0)
        print(f"{m:<25} {bv:>15.4f} {sv:>15.4f} {sv-bv:>+10.4f}")
    
    print("\nBase verbal dist:", all_results["base"]["verbal_dist"])
    print("SFT verbal dist:", all_results["sft"]["verbal_dist"])
    print(f"\nSaved: {sp}")
