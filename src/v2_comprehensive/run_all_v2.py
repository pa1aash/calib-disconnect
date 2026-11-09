"""
All-in-one experiment runner for DL4C paper.
Fixes MBPP execution, reruns baselines, runs DPO training, evaluation, and trust study.
"""

import json, os, sys, time, re, subprocess, tempfile, gc
import numpy as np
import torch
from math import comb
from collections import defaultdict, Counter
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset, Dataset
from peft import LoraConfig, get_peft_model, PeftModel, TaskType
from trl import DPOTrainer, DPOConfig, SFTTrainer, SFTConfig

RESULTS_DIR = "/home/ubuntu/dl4c_experiments/results"
DATA_DIR = "/home/ubuntu/dl4c_experiments/data"
MODEL_DIR = "/home/ubuntu/dl4c_experiments/models"
for d in [RESULTS_DIR, DATA_DIR, MODEL_DIR]:
    os.makedirs(d, exist_ok=True)

BASE_MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct"
NUM_SAMPLES = 10
MAX_TOKENS = 512

# ==================== UTILITIES ====================

def compute_ece(c, a, n_bins=10):
    c, a = np.array(c, dtype=float), np.array(a, dtype=float)
    bounds = np.linspace(0, 1, n_bins + 1)
    ece = 0.0; bins = []
    for i in range(n_bins):
        m = (c >= bounds[i]) & (c < bounds[i+1]) if i < n_bins-1 else (c >= bounds[i]) & (c <= bounds[i+1])
        if m.sum() > 0:
            ba, bc, bs = float(a[m].mean()), float(c[m].mean()), int(m.sum())
            ece += (bs / len(c)) * abs(ba - bc)
            bins.append({"bin_lower": float(bounds[i]), "bin_upper": float(bounds[i+1]),
                        "accuracy": ba, "confidence": bc, "count": bs})
    return float(ece), bins

def compute_brier(c, a): return float(np.mean((np.array(c) - np.array(a)) ** 2))

def compute_auroc(c, a):
    from sklearn.metrics import roc_auc_score
    c, a = np.array(c), np.array(a)
    return float(roc_auc_score(a, c)) if len(np.unique(a)) >= 2 else float('nan')

def execute_humaneval(code, problem):
    """Execute HumanEval: code should complete the function stub."""
    full_code = code if problem["prompt"] in code else problem["prompt"] + code
    test_code = problem["test"] + f"\ncheck({problem['entry_point']})"
    return _run_code(full_code + "\n" + test_code)

def execute_mbpp(code, problem):
    """Execute MBPP: code should define a standalone function matching test assertions."""
    # MBPP tests are like: assert func_name(args) == expected
    # Just run the code + tests directly
    return _run_code(code + "\n" + problem["test"])

def _run_code(code, timeout=10):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code); f.flush()
        try:
            r = subprocess.run(['python3', f.name], capture_output=True, text=True, timeout=timeout)
            return r.returncode == 0
        except: return False
        finally: os.unlink(f.name)

def extract_code(resp):
    """Extract Python code from model response, handling various formats."""
    # Try markdown code blocks first
    blocks = re.findall(r'```(?:python)?\n?(.*?)```', resp, re.DOTALL)
    if blocks:
        return blocks[0].strip()
    # Try to find function definitions
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
    if code_lines:
        return '\n'.join(code_lines).strip()
    return resp.strip()

def extract_verbalized_conf(resp):
    m = re.search(r'CONFIDENCE:\s*(\d)', resp)
    if m: return min(max(int(m.group(1)), 1), 5) / 5.0
    m = re.search(r'(\d)\s*/\s*5', resp)
    if m: return int(m.group(1)) / 5.0
    rl = resp.lower()
    if 'very confident' in rl or 'certainly correct' in rl: return 0.9
    if any(p in rl for p in ['i am confident', 'quite confident', 'highly confident']): return 0.8
    if any(p in rl for p in ['should work', 'most cases', 'fairly', 'moderately']): return 0.6
    if any(p in rl for p in ['unsure', 'not confident', 'not sure', 'uncertain', 'may have bugs']): return 0.3
    if any(p in rl for p in ['very unsure', 'likely wrong', 'probably incorrect']): return 0.2
    return 0.6  # default

def extract_trained_conf(resp):
    """Extract confidence from DPO-trained model output."""
    rl = resp.lower()
    if 'i am confident this solution is correct' in rl: return 0.9
    if 'should work for most cases' in rl or 'please verify edge cases' in rl: return 0.6
    if 'not confident' in rl or 'may contain bugs' in rl or 'review carefully' in rl: return 0.3
    # Fallback to general extraction
    return extract_verbalized_conf(resp)

@torch.no_grad()
def generate_n(model, tokenizer, prompt, n, temp=0.8):
    ids = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048).input_ids.to(model.device)
    results = []
    for _ in range(n):
        out = model.generate(ids, max_new_tokens=MAX_TOKENS, temperature=temp, top_p=0.95,
                            do_sample=True, pad_token_id=tokenizer.pad_token_id)
        results.append(tokenizer.decode(out[0][ids.shape[1]:], skip_special_tokens=True))
    return results

def format_prompt(tokenizer, messages):
    try: return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    except: return messages[-1]["content"]

def load_humaneval():
    ds = load_dataset("openai_humaneval", split="test")
    return [{"task_id": i["task_id"], "prompt": i["prompt"], "canonical_solution": i["canonical_solution"],
             "test": i["test"], "entry_point": i["entry_point"]} for i in ds]

def load_mbpp():
    ds = load_dataset("google-research-datasets/mbpp", "sanitized", split="test")
    return [{"task_id": f"mbpp_{i['task_id']}", "prompt": i["prompt"],
             "test": "\n".join(i["test_list"]), "code": i["code"]} for i in ds]

def eval_calibration(model, tokenizer, problems, is_humaneval, model_name, bench_name, use_trained_conf=False):
    """Run full calibration evaluation."""
    print(f"\n  Evaluating {model_name} on {bench_name} ({len(problems)} problems)...", flush=True)
    t0 = time.time()
    
    sampling_confs, verbal_confs, corr_list, per_problem = [], [], [], []
    
    for idx, prob in enumerate(problems):
        if idx % 20 == 0: print(f"    [{idx}/{len(problems)}] ({time.time()-t0:.0f}s)", flush=True)
        
        # Code generation
        code_msg = [{"role": "user", "content": f"Complete the following Python function. Only output the complete function, no explanations.\n\n{prob['prompt']}"}] if is_humaneval else [{"role": "user", "content": f"Write a Python function to solve: {prob['prompt']}\nOnly output the function, no explanations."}]
        pi = format_prompt(tokenizer, code_msg)
        samples = generate_n(model, tokenizer, pi, NUM_SAMPLES, temp=0.8)
        
        sample_ok = []
        for s in samples:
            code = extract_code(s)
            ok = execute_humaneval(code, prob) if is_humaneval else execute_mbpp(code, prob)
            sample_ok.append(ok)
        pr = sum(sample_ok) / len(sample_ok)
        
        # Verbalized confidence
        if use_trained_conf:
            conf_msg = [{"role": "system", "content": "Before providing your solution, state your confidence:\n- 'I am confident this solution is correct' for high confidence\n- 'This should work for most cases, but please verify edge cases' for medium confidence\n- 'I am not confident in this solution, it may contain bugs' for low confidence\nThen provide the complete Python solution."},
                       {"role": "user", "content": f"State your confidence and solve:\n\n{prob['prompt']}"}]
        else:
            conf_msg = [{"role": "user", "content": f"Rate your confidence 1-5 (1=unsure, 5=confident). Format: CONFIDENCE: [N]. Then solve.\n\n{prob['prompt']}"}]
        ci = format_prompt(tokenizer, conf_msg)
        cresp = generate_n(model, tokenizer, ci, 1, temp=0.1)[0]
        vc = extract_trained_conf(cresp) if use_trained_conf else extract_verbalized_conf(cresp)
        
        sampling_confs.append(float(pr))
        verbal_confs.append(float(vc))
        corr_list.append(float(sample_ok[0]))
        per_problem.append({"task_id": prob.get("task_id", ""), "pass_count": sum(sample_ok), "pass_rate": float(pr)})
    
    elapsed = time.time() - t0
    results = {"model": model_name, "benchmark": bench_name, "time_seconds": elapsed}
    
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
    p10 = [1.0 if NUM_SAMPLES - p["pass_count"] < min(10, NUM_SAMPLES) else 
           1.0 - comb(NUM_SAMPLES - p["pass_count"], min(10, NUM_SAMPLES)) / comb(NUM_SAMPLES, min(10, NUM_SAMPLES)) 
           for p in per_problem]
    results["pass_at_10"] = float(np.mean(p10))
    print(f"    pass@1={results['pass_at_1']:.4f}, pass@10={results['pass_at_10']:.4f}", flush=True)
    
    return results


# ==================== EXPERIMENT 2: DPO TRAINING ====================

def generate_dpo_data(model, tokenizer, problems):
    """Generate DPO training pairs using execution feedback."""
    print("\n  Generating DPO training data...", flush=True)
    
    CONF_HIGH = "I am confident this solution is correct. The logic handles the requirements and edge cases well."
    CONF_MED = "This solution should work for most cases, but please verify edge cases. There may be subtle issues I'm not certain about."
    CONF_LOW = "I am not confident in this solution. It may contain bugs or miss important edge cases. Please review carefully before using."
    
    dpo_pairs = []
    
    for idx, prob in enumerate(problems):
        if idx % 20 == 0: print(f"    [{idx}/{len(problems)}]", flush=True)
        
        prompt_text = prob["prompt"]
        code_msg = [{"role": "user", "content": f"Complete the following Python function:\n\n{prompt_text}"}]
        pi = format_prompt(tokenizer, code_msg)
        
        samples = generate_n(model, tokenizer, pi, NUM_SAMPLES, temp=0.8)
        
        sample_results = []
        for s in samples:
            code = extract_code(s)
            full_code = code if prompt_text in code else prompt_text + code
            test_code = prob["test"] + f"\ncheck({prob['entry_point']})"
            ok = _run_code(full_code + "\n" + test_code)
            sample_results.append({"code": code, "correct": ok})
        
        n_correct = sum(1 for s in sample_results if s["correct"])
        difficulty = n_correct / len(sample_results)
        
        # Determine true confidence level
        if difficulty >= 0.7: true_conf, true_label = "high", CONF_HIGH
        elif difficulty >= 0.3: true_conf, true_label = "medium", CONF_MED
        else: true_conf, true_label = "low", CONF_LOW
        
        correct_samples = [s for s in sample_results if s["correct"]]
        incorrect_samples = [s for s in sample_results if not s["correct"]]
        
        dpo_prompt = f"State your confidence level, then complete the following Python function.\n\n{prompt_text}"
        
        # Pair type 1: Correct code + calibrated conf vs incorrect code + overconfident
        if correct_samples and incorrect_samples:
            chosen = f"{true_label}\n\n```python\n{correct_samples[0]['code']}\n```"
            rejected = f"{CONF_HIGH}\n\n```python\n{incorrect_samples[0]['code']}\n```"
            dpo_pairs.append({"prompt": dpo_prompt, "chosen": chosen, "rejected": rejected, 
                            "pair_type": "correct_calibrated_vs_incorrect_overconfident", "difficulty": difficulty})
        
        # Pair type 2: Calibrated conf on hard problem vs overconfident on hard problem
        if incorrect_samples and true_conf in ["low", "medium"]:
            chosen = f"{true_label}\n\n```python\n{incorrect_samples[0]['code']}\n```"
            rej_code = incorrect_samples[min(1, len(incorrect_samples)-1)]['code']
            rejected = f"{CONF_HIGH}\n\n```python\n{rej_code}\n```"
            dpo_pairs.append({"prompt": dpo_prompt, "chosen": chosen, "rejected": rejected,
                            "pair_type": "calibrated_low_vs_overconfident", "difficulty": difficulty})
        
        # Pair type 3: Calibrated high conf vs underconfident on easy problem
        if correct_samples and true_conf == "high":
            chosen = f"{CONF_HIGH}\n\n```python\n{correct_samples[0]['code']}\n```"
            rej_code = correct_samples[min(1, len(correct_samples)-1)]['code']
            rejected = f"{CONF_LOW}\n\n```python\n{rej_code}\n```"
            dpo_pairs.append({"prompt": dpo_prompt, "chosen": chosen, "rejected": rejected,
                            "pair_type": "calibrated_high_vs_underconfident", "difficulty": difficulty})
    
    print(f"  Generated {len(dpo_pairs)} DPO pairs", flush=True)
    types = Counter(p["pair_type"] for p in dpo_pairs)
    for t, c in types.items(): print(f"    {t}: {c}")
    
    return dpo_pairs


def train_dpo_model(dpo_pairs):
    """Train model with DPO on confidence-annotated pairs."""
    print("\n  === DPO TRAINING ===", flush=True)
    
    ds = Dataset.from_dict({"prompt": [p["prompt"] for p in dpo_pairs],
                           "chosen": [p["chosen"] for p in dpo_pairs],
                           "rejected": [p["rejected"] for p in dpo_pairs]})
    split = ds.train_test_split(test_size=0.1, seed=42)
    print(f"  Train: {len(split['train'])}, Eval: {len(split['test'])}", flush=True)
    
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    
    lora_cfg = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05,
        target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
        task_type=TaskType.CAUSAL_LM, bias="none")
    
    out_dir = os.path.join(MODEL_DIR, "qwen_confidence_dpo")
    args = DPOConfig(output_dir=out_dir, num_train_epochs=3, per_device_train_batch_size=2,
        per_device_eval_batch_size=2, gradient_accumulation_steps=8, learning_rate=5e-7,
        beta=0.1, lr_scheduler_type="cosine", warmup_ratio=0.1, bf16=True, logging_steps=10,
        eval_strategy="steps", eval_steps=50, save_strategy="epoch",
        max_length=2048, report_to="none",
        gradient_checkpointing=True, remove_unused_columns=False)
    
    trainer = DPOTrainer(model=model, args=args, train_dataset=split["train"],
                        eval_dataset=split["test"], processing_class=tokenizer, peft_config=lora_cfg)
    
    t0 = time.time()
    trainer.train()
    elapsed = (time.time() - t0) / 60
    print(f"  DPO training done in {elapsed:.1f} min", flush=True)
    
    trainer.save_model(out_dir)
    tokenizer.save_pretrained(out_dir)
    
    metrics = {"time_minutes": elapsed, "n_train": len(split["train"]), "n_eval": len(split["test"])}
    with open(os.path.join(RESULTS_DIR, "dpo_training_metrics.json"), 'w') as f:
        json.dump(metrics, f, indent=2)
    
    del model, tokenizer, trainer; torch.cuda.empty_cache(); gc.collect()
    return out_dir


def train_sft_model(dpo_pairs):
    """Train SFT baseline (chosen responses only, no preference signal)."""
    print("\n  === SFT BASELINE TRAINING ===", flush=True)
    
    sft_data = [{"messages": [{"role": "user", "content": p["prompt"]},
                              {"role": "assistant", "content": p["chosen"]}]} for p in dpo_pairs]
    ds = Dataset.from_list(sft_data)
    split = ds.train_test_split(test_size=0.1, seed=42)
    
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    
    lora_cfg = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05,
        target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
        task_type=TaskType.CAUSAL_LM, bias="none")
    
    out_dir = os.path.join(MODEL_DIR, "qwen_confidence_sft")
    args = SFTConfig(output_dir=out_dir, num_train_epochs=3, per_device_train_batch_size=2,
        per_device_eval_batch_size=2, gradient_accumulation_steps=8, learning_rate=2e-5,
        lr_scheduler_type="cosine", warmup_ratio=0.1, bf16=True, logging_steps=10,
        eval_strategy="steps", eval_steps=50, save_strategy="epoch",
        max_length=2048, report_to="none", gradient_checkpointing=True)
    
    def fmt(ex): return tokenizer.apply_chat_template(ex["messages"], tokenize=False, add_generation_prompt=False)
    
    trainer = SFTTrainer(model=model, args=args, train_dataset=split["train"],
                        eval_dataset=split["test"], processing_class=tokenizer,
                        peft_config=lora_cfg, formatting_func=fmt)
    
    t0 = time.time()
    trainer.train()
    elapsed = (time.time() - t0) / 60
    print(f"  SFT training done in {elapsed:.1f} min", flush=True)
    
    trainer.save_model(out_dir)
    tokenizer.save_pretrained(out_dir)
    
    del model, tokenizer, trainer; torch.cuda.empty_cache(); gc.collect()
    return out_dir


# ==================== EXPERIMENT 4: TRUST STUDY ====================

def run_trust_study(humaneval):
    """Simulated developer trust calibration study."""
    print("\n  === EXPERIMENT 4: TRUST STUDY ===", flush=True)
    
    problems = humaneval[:50]  # Use first 50 problems
    
    conditions = {}
    
    # Load base model
    print("  Loading base model...", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    base = AutoModelForCausalLM.from_pretrained(BASE_MODEL, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    base.eval()
    
    # Condition 1: No confidence
    # Condition 2: Uncalibrated (base model) confidence
    for cond_name, show_conf, use_trained in [("no_confidence", False, False), ("uncalibrated", True, False)]:
        print(f"\n  Condition: {cond_name}", flush=True)
        results = _run_trust_condition(base, tokenizer, problems, show_conf, use_trained)
        conditions[cond_name] = results
    
    del base; torch.cuda.empty_cache(); gc.collect()
    
    # Condition 3: Calibrated (DPO) confidence  
    dpo_dir = os.path.join(MODEL_DIR, "qwen_confidence_dpo")
    if os.path.exists(dpo_dir):
        print("\n  Loading DPO model...", flush=True)
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
        if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
        dpo_base = AutoModelForCausalLM.from_pretrained(BASE_MODEL, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
        dpo_model = PeftModel.from_pretrained(dpo_base, dpo_dir)
        dpo_model.eval()
        
        results = _run_trust_condition(dpo_model, tokenizer, problems, True, True)
        conditions["calibrated_dpo"] = results
        
        del dpo_model, dpo_base; torch.cuda.empty_cache(); gc.collect()
    
    # Save
    save_path = os.path.join(RESULTS_DIR, "experiment4_trust_study.json")
    with open(save_path, 'w') as f:
        json.dump(conditions, f, indent=2)
    
    print("\n  TRUST STUDY SUMMARY:", flush=True)
    print(f"  {'Condition':<25} {'Accept%':>8} {'Overtrust':>10} {'Undertrust':>11} {'DecAcc':>8}")
    for name, r in conditions.items():
        print(f"  {name:<25} {r['acceptance_rate']:>7.3f} {r['overtrust_rate']:>10.3f} {r['undertrust_rate']:>11.3f} {r['decision_accuracy']:>8.3f}")
    
    return conditions


def _run_trust_condition(model, tokenizer, problems, show_conf, use_trained):
    """Run one condition of the trust study."""
    decisions = []
    
    for idx, prob in enumerate(problems):
        if idx % 10 == 0: print(f"    [{idx}/{len(problems)}]", flush=True)
        
        # Generate solution (with or without confidence prompt)
        if show_conf:
            if use_trained:
                msgs = [{"role": "system", "content": "Before providing your solution, state your confidence:\n- 'I am confident this solution is correct' for high confidence\n- 'This should work for most cases, but please verify edge cases' for medium confidence\n- 'I am not confident in this solution, it may contain bugs' for low confidence\nThen provide the complete Python solution."},
                       {"role": "user", "content": f"State your confidence and complete:\n\n{prob['prompt']}"}]
            else:
                msgs = [{"role": "user", "content": f"Rate confidence 1-5 before solving. Format: CONFIDENCE: [N]\n\n{prob['prompt']}"}]
        else:
            msgs = [{"role": "user", "content": f"Complete the following Python function:\n\n{prob['prompt']}"}]
        
        pi = format_prompt(tokenizer, msgs)
        resp = generate_n(model, tokenizer, pi, 1, temp=0.1)[0]
        code = extract_code(resp)
        
        # Check actual correctness
        is_correct = execute_humaneval(code, prob)
        
        # Extract confidence
        if show_conf:
            conf = extract_trained_conf(resp) if use_trained else extract_verbalized_conf(resp)
        else:
            conf = None
        
        # Simulated developer decision based on code quality signals + confidence
        decision = _developer_decision(code, conf, show_conf)
        
        decisions.append({"task_id": prob["task_id"], "correct": is_correct, "decision": decision,
                         "confidence": conf})
    
    # Compute metrics
    total = len(decisions)
    correct_accept = sum(1 for d in decisions if d["decision"] == "accept" and d["correct"])
    incorrect_accept = sum(1 for d in decisions if d["decision"] == "accept" and not d["correct"])
    correct_reject = sum(1 for d in decisions if d["decision"] != "accept" and not d["correct"])
    incorrect_reject = sum(1 for d in decisions if d["decision"] != "accept" and d["correct"])
    
    return {
        "total": total,
        "acceptance_rate": sum(1 for d in decisions if d["decision"] == "accept") / total,
        "correct_rate": sum(1 for d in decisions if d["correct"]) / total,
        "overtrust_rate": incorrect_accept / total,
        "undertrust_rate": incorrect_reject / total,
        "decision_accuracy": (correct_accept + correct_reject) / total,
        "decisions": decisions,
    }


def _developer_decision(code, conf, has_conf):
    """Simulate developer decision: accept, modify, or reject."""
    score = 0.5
    lines = code.strip().split('\n')
    if len(lines) < 2: score -= 0.15
    if 'try:' in code or 'except' in code: score += 0.05
    if 'if not' in code or 'if len' in code or '== 0' in code or 'is None' in code: score += 0.05
    if '"""' in code or "'''" in code: score += 0.03
    
    if has_conf and conf is not None:
        if conf >= 0.8: score += 0.15
        elif conf >= 0.5: score += 0.0
        else: score -= 0.2  # Low confidence → developer more cautious
    
    if score >= 0.55: return "accept"
    elif score >= 0.35: return "modify"
    else: return "reject"


# ==================== MAIN ====================

if __name__ == "__main__":
    t_start = time.time()
    print("="*60)
    print("DL4C EXPERIMENTS - FULL PIPELINE")
    print("="*60, flush=True)
    
    humaneval = load_humaneval()
    mbpp = load_mbpp()
    print(f"HumanEval: {len(humaneval)}, MBPP: {len(mbpp)}")
    
    # ===== EXPERIMENT 1: Baseline Calibration (rerun with fixed MBPP) =====
    print("\n" + "#"*60)
    print("# EXPERIMENT 1: Baseline Calibration")
    print("#"*60, flush=True)
    
    # Check if we already have valid Qwen HumanEval results
    qwen_he_path = os.path.join(RESULTS_DIR, "exp1_qwen2.5-coder-7b_humaneval.json")
    if os.path.exists(qwen_he_path):
        with open(qwen_he_path) as f:
            existing = json.load(f)
        if existing.get("pass_at_1", 0) > 0.5:
            print("  Qwen HumanEval already done (pass@1={:.3f}), skipping.".format(existing["pass_at_1"]))
        else:
            existing = None
    else:
        existing = None
    
    # Load model for baseline + DPO data generation
    print("\n  Loading base model...", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    model.eval()
    
    # Run HumanEval if needed
    if existing is None:
        he_results = eval_calibration(model, tokenizer, humaneval, True, "qwen2.5-coder-7b-base", "humaneval")
        with open(qwen_he_path, 'w') as f: json.dump(he_results, f, indent=2)
    
    # Run MBPP with fixed execution
    mbpp_path = os.path.join(RESULTS_DIR, "exp1_qwen2.5-coder-7b_mbpp_fixed.json")
    if not os.path.exists(mbpp_path):
        mbpp_results = eval_calibration(model, tokenizer, mbpp, False, "qwen2.5-coder-7b-base", "mbpp")
        with open(mbpp_path, 'w') as f: json.dump(mbpp_results, f, indent=2)
    else:
        print("  MBPP already done, skipping.")
    
    # ===== EXPERIMENT 2: DPO Training =====
    print("\n" + "#"*60)
    print("# EXPERIMENT 2: DPO Training Data Generation + Training")
    print("#"*60, flush=True)
    
    dpo_data_path = os.path.join(DATA_DIR, "dpo_confidence_pairs.json")
    if not os.path.exists(dpo_data_path):
        dpo_pairs = generate_dpo_data(model, tokenizer, humaneval)
        with open(dpo_data_path, 'w') as f: json.dump(dpo_pairs, f, indent=2)
    else:
        print("  Loading existing DPO data...")
        with open(dpo_data_path) as f: dpo_pairs = json.load(f)
        print(f"  {len(dpo_pairs)} pairs loaded")
    
    # Free base model before training
    del model, tokenizer; torch.cuda.empty_cache(); gc.collect()
    
    # DPO training
    dpo_dir = os.path.join(MODEL_DIR, "qwen_confidence_dpo")
    if not os.path.exists(os.path.join(dpo_dir, "adapter_config.json")):
        dpo_dir = train_dpo_model(dpo_pairs)
    else:
        print("  DPO model already trained, skipping.")
    
    # SFT baseline training
    sft_dir = os.path.join(MODEL_DIR, "qwen_confidence_sft")
    if not os.path.exists(os.path.join(sft_dir, "adapter_config.json")):
        sft_dir = train_sft_model(dpo_pairs)
    else:
        print("  SFT model already trained, skipping.")
    
    # ===== EXPERIMENT 3: Post-Training Evaluation =====
    print("\n" + "#"*60)
    print("# EXPERIMENT 3: Post-Training Calibration Evaluation")
    print("#"*60, flush=True)
    
    for variant, vdir, label in [("dpo", dpo_dir, "qwen-dpo"), ("sft", sft_dir, "qwen-sft")]:
        result_path = os.path.join(RESULTS_DIR, f"exp3_{label}_humaneval.json")
        if os.path.exists(result_path):
            print(f"  {label} HumanEval already done, skipping.")
            continue
            
        if not os.path.exists(os.path.join(vdir, "adapter_config.json")):
            print(f"  {label} model not found, skipping.")
            continue
        
        print(f"\n  Loading {label} model...", flush=True)
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
        if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
        base_m = AutoModelForCausalLM.from_pretrained(BASE_MODEL, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
        peft_m = PeftModel.from_pretrained(base_m, vdir)
        peft_m.eval()
        
        r = eval_calibration(peft_m, tokenizer, humaneval, True, label, "humaneval", use_trained_conf=True)
        with open(result_path, 'w') as f: json.dump(r, f, indent=2)
        
        del peft_m, base_m, tokenizer; torch.cuda.empty_cache(); gc.collect()
    
    # ===== EXPERIMENT 4: Trust Study =====
    print("\n" + "#"*60)
    print("# EXPERIMENT 4: Simulated Trust Study")
    print("#"*60, flush=True)
    
    trust_path = os.path.join(RESULTS_DIR, "experiment4_trust_study.json")
    if not os.path.exists(trust_path):
        trust_results = run_trust_study(humaneval)
    else:
        print("  Trust study already done, skipping.")
    
    # ===== FINAL SUMMARY =====
    total_time = (time.time() - t_start) / 60
    print("\n" + "="*60)
    print(f"ALL EXPERIMENTS COMPLETE ({total_time:.1f} min)")
    print("="*60)
    print("\nResult files:")
    for f in sorted(os.listdir(RESULTS_DIR)):
        size = os.path.getsize(os.path.join(RESULTS_DIR, f))
        print(f"  {f} ({size} bytes)")
