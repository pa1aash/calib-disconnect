"""
Experiment 1: Baseline Calibration Measurement
Measures calibration of code LLMs on HumanEval and MBPP using three confidence methods:
1. Logit-based (mean token probability)
2. Sampling-based (pass@k consistency)
3. Verbalized (model self-reported confidence)
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
import signal
from collections import defaultdict

# ============================================================
# Configuration
# ============================================================

MODELS = {
    "qwen2.5-coder-7b": "Qwen/Qwen2.5-Coder-7B-Instruct",
    "deepseek-coder-v2-lite": "deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct", 
    "codellama-13b": "meta-llama/CodeLlama-13b-Instruct-hf",
}

NUM_SAMPLES = 20
TEMPERATURE = 0.8
MAX_NEW_TOKENS = 512
RESULTS_DIR = "/home/ubuntu/dl4c_experiments/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# Utility Functions
# ============================================================

def compute_ece(confidences, accuracies, n_bins=10):
    """Expected Calibration Error with equal-width bins."""
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    bin_data = []
    for i in range(n_bins):
        mask = (confidences >= bin_boundaries[i]) & (confidences < bin_boundaries[i + 1])
        if i == n_bins - 1:  # include right boundary for last bin
            mask = (confidences >= bin_boundaries[i]) & (confidences <= bin_boundaries[i + 1])
        if mask.sum() > 0:
            bin_acc = accuracies[mask].mean()
            bin_conf = confidences[mask].mean()
            bin_size = mask.sum()
            ece += (bin_size / len(confidences)) * abs(bin_acc - bin_conf)
            bin_data.append({
                "bin_lower": float(bin_boundaries[i]),
                "bin_upper": float(bin_boundaries[i + 1]),
                "accuracy": float(bin_acc),
                "confidence": float(bin_conf),
                "count": int(bin_size)
            })
    return float(ece), bin_data


def compute_brier_score(confidences, accuracies):
    """Brier score: mean squared difference between confidence and outcome."""
    return float(np.mean((confidences - accuracies) ** 2))


def compute_auroc(confidences, accuracies):
    """AUROC for confidence as a classifier of correctness."""
    from sklearn.metrics import roc_auc_score
    if len(np.unique(accuracies)) < 2:
        return float('nan')
    return float(roc_auc_score(accuracies, confidences))


def execute_code_safe(code, test_code, timeout=10):
    """Execute code with test cases in a subprocess with timeout."""
    full_code = code + "\n" + test_code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(full_code)
        f.flush()
        try:
            result = subprocess.run(
                ['python3', f.name],
                capture_output=True, text=True, timeout=timeout
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, Exception):
            return False
        finally:
            os.unlink(f.name)


def load_humaneval():
    """Load HumanEval dataset."""
    ds = load_dataset("openai_humaneval", split="test")
    problems = []
    for item in ds:
        problems.append({
            "task_id": item["task_id"],
            "prompt": item["prompt"],
            "canonical_solution": item["canonical_solution"],
            "test": item["test"],
            "entry_point": item["entry_point"],
        })
    return problems


def load_mbpp():
    """Load MBPP dataset (sanitized subset)."""
    ds = load_dataset("google-research-datasets/mbpp", "sanitized", split="test")
    problems = []
    for item in ds:
        test_code = "\n".join(item["test_list"])
        problems.append({
            "task_id": f"mbpp_{item['task_id']}",
            "prompt": item["prompt"],
            "test": test_code,
            "code": item["code"],
        })
    return problems


def extract_code_from_response(response):
    """Extract Python code from model response."""
    # Try to find code blocks
    code_blocks = re.findall(r'```(?:python)?\n?(.*?)```', response, re.DOTALL)
    if code_blocks:
        return code_blocks[0].strip()
    # If no code blocks, return everything up to first non-code line
    return response.strip()


def format_humaneval_prompt(problem, model_name):
    """Format HumanEval prompt for a model."""
    prompt = problem["prompt"]
    if "qwen" in model_name.lower() or "deepseek" in model_name.lower():
        messages = [
            {"role": "system", "content": "You are a helpful coding assistant. Complete the given Python function. Only output the complete function, no explanations."},
            {"role": "user", "content": f"Complete the following Python function:\n\n{prompt}"}
        ]
    else:  # codellama
        messages = [
            {"role": "user", "content": f"Complete the following Python function. Only output the complete function, no explanations.\n\n{prompt}"}
        ]
    return messages


def format_mbpp_prompt(problem, model_name):
    """Format MBPP prompt for a model."""
    prompt = problem["prompt"]
    if "qwen" in model_name.lower() or "deepseek" in model_name.lower():
        messages = [
            {"role": "system", "content": "You are a helpful coding assistant. Write a Python function to solve the given task. Only output the function, no explanations."},
            {"role": "user", "content": f"Write a Python function to solve the following task:\n{prompt}"}
        ]
    else:
        messages = [
            {"role": "user", "content": f"Write a Python function to solve the following task. Only output the function, no explanations.\n{prompt}"}
        ]
    return messages


def format_confidence_prompt(problem, model_name):
    """Format prompt asking model to rate its confidence before solving."""
    prompt = problem.get("prompt", "")
    if "qwen" in model_name.lower() or "deepseek" in model_name.lower():
        messages = [
            {"role": "system", "content": "You are a helpful coding assistant. Before solving the problem, rate your confidence level from 1-5:\n1 = Very unsure, likely to have bugs\n2 = Somewhat unsure, may have edge case issues\n3 = Moderately confident, should work for most cases\n4 = Quite confident, likely correct\n5 = Very confident, almost certainly correct\nOutput format: CONFIDENCE: [1-5]\nThen provide the solution."},
            {"role": "user", "content": f"Rate your confidence and then solve:\n\n{prompt}"}
        ]
    else:
        messages = [
            {"role": "user", "content": f"Before solving, rate your confidence from 1-5 (1=very unsure, 5=very confident). Format: CONFIDENCE: [1-5]\nThen provide the solution.\n\n{prompt}"}
        ]
    return messages


def extract_verbalized_confidence(response):
    """Extract confidence rating from verbalized response."""
    match = re.search(r'CONFIDENCE:\s*(\d)', response)
    if match:
        conf = int(match.group(1))
        return min(max(conf, 1), 5) / 5.0  # Normalize to [0, 1]
    # Fallback: try to find any digit near "confidence" or "confident"
    match = re.search(r'(\d)\s*/\s*5', response)
    if match:
        return int(match.group(1)) / 5.0
    return 0.6  # Default moderate confidence if can't parse


# ============================================================
# Main Experiment Loop
# ============================================================

def run_experiment(model_key, model_path, problems, benchmark_name, is_humaneval=True):
    """Run calibration experiment for one model on one benchmark."""
    print(f"\n{'='*60}")
    print(f"Model: {model_key} | Benchmark: {benchmark_name}")
    print(f"{'='*60}")
    
    # Load model
    print(f"Loading {model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model.eval()
    
    results = {
        "model": model_key,
        "benchmark": benchmark_name,
        "logit_confidences": [],
        "sampling_confidences": [],
        "verbalized_confidences": [],
        "correctness": [],
        "per_problem": [],
    }
    
    for idx, problem in enumerate(problems):
        if idx % 10 == 0:
            print(f"  Problem {idx+1}/{len(problems)}...")
        
        problem_results = {
            "task_id": problem.get("task_id", f"{benchmark_name}_{idx}"),
            "samples": [],
            "pass_count": 0,
        }
        
        # --- Generate NUM_SAMPLES samples ---
        if is_humaneval:
            messages = format_humaneval_prompt(problem, model_key)
        else:
            messages = format_mbpp_prompt(problem, model_key)
        
        try:
            text_input = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        except Exception:
            text_input = messages[-1]["content"]
        
        input_ids = tokenizer(text_input, return_tensors="pt").input_ids.to(model.device)
        
        sample_correct = []
        sample_logit_confs = []
        
        for s in range(NUM_SAMPLES):
            with torch.no_grad():
                outputs = model.generate(
                    input_ids,
                    max_new_tokens=MAX_NEW_TOKENS,
                    temperature=TEMPERATURE,
                    top_p=0.95,
                    do_sample=True,
                    return_dict_in_generate=True,
                    output_scores=True,
                    pad_token_id=tokenizer.pad_token_id,
                )
            
            generated_ids = outputs.sequences[0][input_ids.shape[1]:]
            response = tokenizer.decode(generated_ids, skip_special_tokens=True)
            code = extract_code_from_response(response)
            
            # Compute logit-based confidence
            if outputs.scores:
                token_probs = []
                for score in outputs.scores:
                    probs = torch.softmax(score[0], dim=-1)
                    max_prob = probs.max().item()
                    token_probs.append(max_prob)
                logit_conf = np.mean(token_probs) if token_probs else 0.5
            else:
                logit_conf = 0.5
            
            # Execute code
            if is_humaneval:
                full_code = code if problem["prompt"] in code else problem["prompt"] + code
                test_code = problem["test"] + f"\ncheck({problem['entry_point']})"
                is_correct = execute_code_safe(full_code, test_code)
            else:
                test_code = problem["test"]
                is_correct = execute_code_safe(code, test_code)
            
            sample_correct.append(is_correct)
            sample_logit_confs.append(logit_conf)
            problem_results["samples"].append({
                "correct": is_correct,
                "logit_conf": logit_conf,
            })
        
        # Sampling-based confidence = fraction of correct samples
        pass_rate = sum(sample_correct) / len(sample_correct)
        problem_results["pass_count"] = sum(sample_correct)
        
        # Mean logit confidence across samples
        mean_logit_conf = np.mean(sample_logit_confs)
        
        # --- Verbalized confidence (separate generation) ---
        if is_humaneval:
            conf_messages = format_confidence_prompt(problem, model_key)
        else:
            conf_messages = format_confidence_prompt(problem, model_key)
        
        try:
            conf_text = tokenizer.apply_chat_template(conf_messages, tokenize=False, add_generation_prompt=True)
        except Exception:
            conf_text = conf_messages[-1]["content"]
        
        conf_input_ids = tokenizer(conf_text, return_tensors="pt").input_ids.to(model.device)
        
        with torch.no_grad():
            conf_outputs = model.generate(
                conf_input_ids,
                max_new_tokens=MAX_NEW_TOKENS,
                temperature=0.1,  # Low temp for consistent confidence rating
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
            )
        
        conf_response = tokenizer.decode(conf_outputs[0][conf_input_ids.shape[1]:], skip_special_tokens=True)
        verbalized_conf = extract_verbalized_confidence(conf_response)
        
        # The "ground truth" for this problem: was the greedy solution correct?
        # Use first sample's correctness as primary, pass_rate as secondary
        is_first_correct = sample_correct[0]
        
        results["logit_confidences"].append(mean_logit_conf)
        results["sampling_confidences"].append(pass_rate)
        results["verbalized_confidences"].append(verbalized_conf)
        results["correctness"].append(float(is_first_correct))
        results["per_problem"].append(problem_results)
    
    # Compute metrics
    for conf_type in ["logit", "sampling", "verbalized"]:
        confs = np.array(results[f"{conf_type}_confidences"])
        accs = np.array(results["correctness"])
        
        ece, bin_data = compute_ece(confs, accs)
        brier = compute_brier_score(confs, accs)
        auroc = compute_auroc(confs, accs)
        
        results[f"{conf_type}_ece"] = ece
        results[f"{conf_type}_brier"] = brier
        results[f"{conf_type}_auroc"] = auroc
        results[f"{conf_type}_bins"] = bin_data
        
        print(f"  {conf_type}: ECE={ece:.4f}, Brier={brier:.4f}, AUROC={auroc:.4f}")
    
    # pass@1 and pass@10
    pass_at_1 = np.mean(results["correctness"])
    pass_at_10_list = []
    for pr in results["per_problem"]:
        # pass@10 = 1 - C(n-c, k) / C(n, k) where n=NUM_SAMPLES, c=pass_count, k=10
        n = NUM_SAMPLES
        c = pr["pass_count"]
        k = min(10, n)
        if n - c < k:
            pass_at_10_list.append(1.0)
        else:
            from math import comb
            pass_at_10_list.append(1.0 - comb(n - c, k) / comb(n, k))
    pass_at_10 = np.mean(pass_at_10_list)
    
    results["pass_at_1"] = float(pass_at_1)
    results["pass_at_10"] = float(pass_at_10)
    print(f"  pass@1={pass_at_1:.4f}, pass@10={pass_at_10:.4f}")
    
    # Save results
    save_path = os.path.join(RESULTS_DIR, f"{model_key}_{benchmark_name}.json")
    # Convert numpy types for JSON serialization
    def convert(obj):
        if isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        return obj
    
    with open(save_path, 'w') as f:
        json.dump(results, f, indent=2, default=convert)
    print(f"  Saved to {save_path}")
    
    # Free memory
    del model
    del tokenizer
    torch.cuda.empty_cache()
    
    return results


if __name__ == "__main__":
    print("="*60)
    print("EXPERIMENT 1: Baseline Calibration Measurement")
    print("="*60)
    
    # Load benchmarks
    print("\nLoading HumanEval...")
    humaneval = load_humaneval()
    print(f"  {len(humaneval)} problems")
    
    print("Loading MBPP (sanitized)...")
    mbpp = load_mbpp()
    print(f"  {len(mbpp)} problems")
    
    all_results = {}
    
    for model_key, model_path in MODELS.items():
        print(f"\n{'#'*60}")
        print(f"# Processing: {model_key}")
        print(f"{'#'*60}")
        
        try:
            he_results = run_experiment(model_key, model_path, humaneval, "humaneval", is_humaneval=True)
            all_results[f"{model_key}_humaneval"] = he_results
        except Exception as e:
            print(f"  ERROR on HumanEval: {e}")
            import traceback
            traceback.print_exc()
        
        try:
            mbpp_results = run_experiment(model_key, model_path, mbpp, "mbpp", is_humaneval=False)
            all_results[f"{model_key}_mbpp"] = mbpp_results
        except Exception as e:
            print(f"  ERROR on MBPP: {e}")
            import traceback
            traceback.print_exc()
    
    # Save summary
    summary = {}
    for key, res in all_results.items():
        summary[key] = {
            "pass_at_1": res.get("pass_at_1"),
            "pass_at_10": res.get("pass_at_10"),
            "logit_ece": res.get("logit_ece"),
            "sampling_ece": res.get("sampling_ece"),
            "verbalized_ece": res.get("verbalized_ece"),
            "logit_auroc": res.get("logit_auroc"),
            "sampling_auroc": res.get("sampling_auroc"),
            "verbalized_auroc": res.get("verbalized_auroc"),
        }
    
    with open(os.path.join(RESULTS_DIR, "experiment1_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "="*60)
    print("EXPERIMENT 1 COMPLETE")
    print("="*60)
    for key, s in summary.items():
        print(f"\n{key}:")
        for metric, val in s.items():
            if val is not None:
                print(f"  {metric}: {val:.4f}")
