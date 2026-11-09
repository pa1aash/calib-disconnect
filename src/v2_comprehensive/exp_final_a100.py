"""
DL4C V2 Final: Run remaining experiments on A100-40GB.
1. n=20 sensitivity analysis (80 HumanEval subset)
2. SFT training on confidence-labeled data  
3. SFT quantitative evaluation with bootstrap CIs
"""

import json, os, time, re, subprocess, tempfile, gc, sys
import numpy as np
import torch
from math import comb
from collections import Counter
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, PeftModel, TaskType
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset, Dataset

RESULTS_DIR = "/home/ubuntu/dl4c/results_v2"
MODEL_DIR = "/home/ubuntu/dl4c/models"
DATA_DIR = "/home/ubuntu/dl4c/data"
BASE_MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct"
SFT_DIR = os.path.join(MODEL_DIR, "qwen_confidence_sft")
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

def bootstrap_all(c, a, n_boot=1000):
    rng = np.random.RandomState(42)
    c, a = np.array(c), np.array(a)
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
            results[name] = float('nan')
            results[f"{name}_ci"] = [float('nan'), float('nan')]
    return results

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
    lines = resp.split('\n')
    code_lines = []; in_code = False
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

def load_humaneval():
    ds = load_dataset("openai_humaneval", split="test")
    return [{"task_id": i["task_id"], "prompt": i["prompt"], "canonical_solution": i["canonical_solution"],
             "test": i["test"], "entry_point": i["entry_point"]} for i in ds]

# ==================== CONFIDENCE LABELS ====================

CONF_HIGH = "I am confident this solution is correct. The logic handles the requirements and edge cases well."
CONF_MED = "This solution should work for most cases, but please verify edge cases. There may be subtle issues."
CONF_LOW = "I am not confident in this solution. It may contain bugs or miss important edge cases. Please review carefully."

# ==================== EXPERIMENT 1: n=20 SENSITIVITY ====================

def run_n20_sensitivity(model, tokenizer, problems):
    """Run n=20 sensitivity on HumanEval subset."""
    print("\n" + "="*60)
    print("EXPERIMENT: n=20 Sensitivity")
    print("="*60, flush=True)
    
    subset = problems[:80]
    t0 = time.time()
    
    sampling_confs, verbal_confs, labels, per_problem = [], [], [], []
    latencies = []
    
    for idx, prob in enumerate(subset):
        if idx % 10 == 0: print(f"  [{idx}/{len(subset)}] ({time.time()-t0:.0f}s)", flush=True)
        
        pi = fmt(tokenizer, [{"role": "user", "content": f"Complete the following Python function. Only output the complete function, no explanations.\n\n{prob['prompt']}"}])
        
        t_s = time.time()
        samples = gen(model, tokenizer, pi, 20, temp=0.8)
        latencies.append((time.time() - t_s) / 20)
        
        sample_ok = [execute_humaneval(extract_code(s), prob) for s in samples]
        pr = sum(sample_ok) / len(sample_ok)
        
        # Verbal confidence
        ci = fmt(tokenizer, [{"role": "user", "content": f"Rate your confidence from 1-5 (1=very unsure, 5=very confident). Format: CONFIDENCE: [N]\nThen provide the solution.\n\n{prob['prompt']}"}])
        cresp = gen(model, tokenizer, ci, 1, temp=0.1)[0]
        vc = extract_numeric_conf(cresp)
        
        sampling_confs.append(float(pr))
        verbal_confs.append(float(vc))
        labels.append(float(sample_ok[0]))
        per_problem.append({"task_id": prob["task_id"], "pass_count": sum(sample_ok), "pass_rate": float(pr)})
    
    elapsed = time.time() - t0
    
    results = {"n_samples": 20, "temperature": 0.8, "n_problems": len(subset), "time_seconds": elapsed,
               "mean_latency_per_sample_s": float(np.mean(latencies)),
               "pass_at_1": float(np.mean(labels))}
    
    for cn, cv in [("sampling", sampling_confs), ("verbal_numeric", verbal_confs)]:
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
        print(f"  {cn}: ECE={ece:.4f} [{metrics['ece_ci'][0]:.4f},{metrics['ece_ci'][1]:.4f}] AUROC={metrics['auroc']:.4f}")
    
    results["labels"] = labels
    results["per_problem"] = per_problem
    
    sp = os.path.join(RESULTS_DIR, "sensitivity_n_20.json")
    with open(sp, 'w') as f: json.dump(results, f, indent=2)
    print(f"  Saved: {sp}")
    return results

# ==================== EXPERIMENT 2: SFT TRAINING + EVAL ====================

def generate_sft_data(model, tokenizer, problems):
    """Generate SFT training data from HumanEval execution feedback."""
    print("\n  Generating SFT training data...", flush=True)
    
    sft_data = []
    for idx, prob in enumerate(problems):
        if idx % 20 == 0: print(f"    [{idx}/{len(problems)}]", flush=True)
        
        pi = fmt(tokenizer, [{"role": "user", "content": f"Complete the following Python function:\n\n{prob['prompt']}"}])
        samples = gen(model, tokenizer, pi, 10, temp=0.8)
        
        sample_ok = [execute_humaneval(extract_code(s), prob) for s in samples]
        n_correct = sum(sample_ok)
        difficulty = n_correct / len(sample_ok)
        
        if difficulty >= 0.7: conf_label = CONF_HIGH
        elif difficulty >= 0.3: conf_label = CONF_MED
        else: conf_label = CONF_LOW
        
        correct_codes = [extract_code(s) for s, ok in zip(samples, sample_ok) if ok]
        incorrect_codes = [extract_code(s) for s, ok in zip(samples, sample_ok) if not ok]
        
        # Create training examples: correct code + calibrated confidence
        if correct_codes:
            chosen_resp = f"{conf_label}\n\n```python\n{correct_codes[0]}\n```"
            prompt_text = f"State your confidence level, then complete the following Python function.\n\n{prob['prompt']}"
            sft_data.append({"messages": [{"role": "user", "content": prompt_text},
                                          {"role": "assistant", "content": chosen_resp}],
                            "difficulty": difficulty, "type": "correct_calibrated"})
        
        # Also: incorrect code + honest low confidence
        if incorrect_codes and difficulty < 0.5:
            honest_resp = f"{CONF_LOW}\n\n```python\n{incorrect_codes[0]}\n```"
            prompt_text = f"State your confidence level, then complete the following Python function.\n\n{prob['prompt']}"
            sft_data.append({"messages": [{"role": "user", "content": prompt_text},
                                          {"role": "assistant", "content": honest_resp}],
                            "difficulty": difficulty, "type": "incorrect_honest"})
    
    print(f"  Generated {len(sft_data)} SFT examples", flush=True)
    types = Counter(d["type"] for d in sft_data)
    for t, c in types.items(): print(f"    {t}: {c}")
    
    dp = os.path.join(DATA_DIR, "sft_confidence_data.json")
    with open(dp, 'w') as f: json.dump(sft_data, f, indent=2)
    return sft_data


def train_sft(sft_data):
    """Train SFT model with LoRA."""
    print("\n  === SFT TRAINING ===", flush=True)
    
    ds = Dataset.from_list(sft_data)
    split = ds.train_test_split(test_size=0.1, seed=42)
    print(f"  Train: {len(split['train'])}, Eval: {len(split['test'])}", flush=True)
    
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    
    lora_cfg = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05,
        target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
        task_type=TaskType.CAUSAL_LM, bias="none")
    
    args = SFTConfig(output_dir=SFT_DIR, num_train_epochs=3, per_device_train_batch_size=1,
        per_device_eval_batch_size=1, gradient_accumulation_steps=16, learning_rate=2e-5,
        lr_scheduler_type="cosine", warmup_ratio=0.1, bf16=True, logging_steps=5,
        eval_strategy="epoch", save_strategy="epoch",
        max_length=2048, report_to="none", gradient_checkpointing=True)
    
    def fmt_fn(ex):
        return tokenizer.apply_chat_template(ex["messages"], tokenize=False, add_generation_prompt=False)
    
    trainer = SFTTrainer(model=model, args=args, train_dataset=split["train"],
                        eval_dataset=split["test"], processing_class=tokenizer,
                        peft_config=lora_cfg, formatting_func=fmt_fn)
    
    t0 = time.time()
    trainer.train()
    elapsed = (time.time() - t0) / 60
    print(f"  SFT done in {elapsed:.1f} min", flush=True)
    
    trainer.save_model(SFT_DIR)
    tokenizer.save_pretrained(SFT_DIR)
    
    # Get final losses
    logs = trainer.state.log_history
    train_losses = [l["loss"] for l in logs if "loss" in l]
    eval_losses = [l["eval_loss"] for l in logs if "eval_loss" in l]
    
    metrics = {"time_minutes": elapsed, "n_train": len(split["train"]), "n_eval": len(split["test"]),
               "train_losses": train_losses, "eval_losses": eval_losses}
    with open(os.path.join(RESULTS_DIR, "sft_training_metrics.json"), 'w') as f:
        json.dump(metrics, f, indent=2)
    
    del model, tokenizer, trainer; torch.cuda.empty_cache(); gc.collect()
    return SFT_DIR


def evaluate_sft(humaneval):
    """Quantitative SFT evaluation with bootstrap CIs."""
    print("\n  === SFT EVALUATION ===", flush=True)
    
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    
    # Load base model for comparison
    base = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    base.eval()
    
    # Load SFT model
    sft_base = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    sft = PeftModel.from_pretrained(sft_base, SFT_DIR)
    sft.eval()
    
    subset = humaneval[:80]
    results = {"base": {}, "sft": {}}
    
    for model_name, model_obj, use_trained in [("base", base, False), ("sft", sft, True)]:
        print(f"\n  Evaluating {model_name}...", flush=True)
        t0 = time.time()
        
        sampling_confs, verbal_confs, labels = [], [], []
        per_problem = []
        
        for idx, prob in enumerate(subset):
            if idx % 10 == 0: print(f"    [{idx}/{len(subset)}] ({time.time()-t0:.0f}s)", flush=True)
            
            # Sampling confidence (10 samples)
            pi = fmt(tokenizer, [{"role": "user", "content": f"Complete the following Python function. Only output the function.\n\n{prob['prompt']}"}])
            samples = gen(model_obj, tokenizer, pi, 10, temp=0.8)
            sample_ok = [execute_humaneval(extract_code(s), prob) for s in samples]
            pr = sum(sample_ok) / len(sample_ok)
            
            # Verbal confidence
            if use_trained:
                ci = fmt(tokenizer, [{"role": "system", "content": "Before solving, state your confidence:\n- 'I am confident this solution is correct' for high confidence\n- 'This should work for most cases, but please verify edge cases' for medium\n- 'I am not confident in this solution, it may contain bugs' for low\nThen solve."},
                                     {"role": "user", "content": f"State confidence and complete:\n\n{prob['prompt']}"}])
                cresp = gen(model_obj, tokenizer, ci, 1, temp=0.1)[0]
                vc = extract_trained_conf(cresp)
            else:
                ci = fmt(tokenizer, [{"role": "user", "content": f"Rate confidence 1-5. Format: CONFIDENCE: [N]. Then solve.\n\n{prob['prompt']}"}])
                cresp = gen(model_obj, tokenizer, ci, 1, temp=0.1)[0]
                vc = extract_numeric_conf(cresp)
            
            sampling_confs.append(float(pr))
            verbal_confs.append(float(vc))
            labels.append(float(sample_ok[0]))
            per_problem.append({"task_id": prob["task_id"], "pass_count": sum(sample_ok),
                               "sampling_conf": float(pr), "verbal_conf": float(vc),
                               "correct": float(sample_ok[0]), "verbal_response": cresp[:300]})
        
        elapsed = time.time() - t0
        model_results = {"model": model_name, "n_problems": len(subset), "time_seconds": elapsed,
                        "pass_at_1": float(np.mean(labels))}
        
        for cn, cv in [("sampling", sampling_confs), ("verbal", verbal_confs)]:
            ece, bins = compute_ece(cv, labels)
            metrics = bootstrap_all(cv, labels)
            model_results[f"{cn}_ece"] = ece
            model_results[f"{cn}_ece_ci"] = metrics["ece_ci"]
            model_results[f"{cn}_brier"] = metrics["brier"]
            model_results[f"{cn}_brier_ci"] = metrics["brier_ci"]
            model_results[f"{cn}_auroc"] = metrics["auroc"]
            model_results[f"{cn}_auroc_ci"] = metrics["auroc_ci"]
            model_results[f"{cn}_bins"] = bins
            model_results[f"{cn}_confs"] = cv
            print(f"    {cn}: ECE={ece:.4f} [{metrics['ece_ci'][0]:.4f},{metrics['ece_ci'][1]:.4f}] AUROC={metrics['auroc']:.4f}")
        
        model_results["labels"] = labels
        model_results["per_problem"] = per_problem
        model_results["verbal_dist"] = dict(Counter([round(v, 1) for v in verbal_confs]))
        results[model_name] = model_results
    
    del base, sft, sft_base, tokenizer; torch.cuda.empty_cache(); gc.collect()
    
    sp = os.path.join(RESULTS_DIR, "sft_evaluation.json")
    with open(sp, 'w') as f: json.dump(results, f, indent=2)
    print(f"  Saved: {sp}")
    
    # Print comparison
    print("\n  === SFT vs BASE COMPARISON ===")
    print(f"  {'Metric':<25} {'Base':>15} {'SFT':>15} {'Delta':>10}")
    for m in ["pass_at_1", "verbal_ece", "verbal_auroc", "verbal_brier"]:
        bv = results["base"].get(m, 0)
        sv = results["sft"].get(m, 0)
        delta = sv - bv
        print(f"  {m:<25} {bv:>15.4f} {sv:>15.4f} {delta:>+10.4f}")
    
    return results


# ==================== MAIN ====================

if __name__ == "__main__":
    t_start = time.time()
    print("="*60)
    print("DL4C V2 FINAL: Remaining Experiments (A100)")
    print("="*60, flush=True)
    
    humaneval = load_humaneval()
    print(f"HumanEval: {len(humaneval)} problems")
    
    # Load base model
    print("\nLoading base model...", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    model.eval()
    print("Loaded.", flush=True)
    
    # 1. n=20 sensitivity
    n20_path = os.path.join(RESULTS_DIR, "sensitivity_n_20.json")
    if not os.path.exists(n20_path):
        run_n20_sensitivity(model, tokenizer, humaneval)
    else:
        print("n=20 already done, skipping.")
    
    # 2. Generate SFT data
    sft_data_path = os.path.join(DATA_DIR, "sft_confidence_data.json")
    if not os.path.exists(sft_data_path):
        sft_data = generate_sft_data(model, tokenizer, humaneval)
    else:
        print("SFT data exists, loading...")
        with open(sft_data_path) as f: sft_data = json.load(f)
        print(f"  {len(sft_data)} examples")
    
    # Free base model before training
    del model, tokenizer; torch.cuda.empty_cache(); gc.collect()
    
    # 3. SFT training
    if not os.path.exists(os.path.join(SFT_DIR, "adapter_config.json")):
        train_sft(sft_data)
    else:
        print("SFT model exists, skipping training.")
    
    # 4. SFT evaluation
    sft_eval_path = os.path.join(RESULTS_DIR, "sft_evaluation.json")
    if not os.path.exists(sft_eval_path):
        evaluate_sft(humaneval)
    else:
        print("SFT evaluation exists, skipping.")
    
    total = (time.time() - t_start) / 60
    print(f"\n{'='*60}")
    print(f"ALL DONE ({total:.1f} min)")
    print("="*60)
    for f_name in sorted(os.listdir(RESULTS_DIR)):
        print(f"  {f_name} ({os.path.getsize(os.path.join(RESULTS_DIR, f_name))} bytes)")
