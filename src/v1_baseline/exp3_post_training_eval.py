"""
Experiment 3: Post-Training Calibration Evaluation
Evaluate calibration of DPO-trained and SFT-trained models vs. base model.
"""

import json
import os
import sys
import time
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from datasets import load_dataset
import re
import subprocess
import tempfile

RESULTS_DIR = "/home/ubuntu/dl4c_experiments/results"
MODEL_DIR = "/home/ubuntu/dl4c_experiments/models"
BASE_MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct"
DPO_MODEL = os.path.join(MODEL_DIR, "qwen_confidence_dpo")
SFT_MODEL = os.path.join(MODEL_DIR, "qwen_confidence_sft")

NUM_SAMPLES = 20
TEMPERATURE = 0.8
MAX_NEW_TOKENS = 512


def compute_ece(confidences, accuracies, n_bins=10):
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    bin_data = []
    for i in range(n_bins):
        mask = (confidences >= bin_boundaries[i]) & (confidences < bin_boundaries[i + 1])
        if i == n_bins - 1:
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
    return float(np.mean((confidences - accuracies) ** 2))


def compute_auroc(confidences, accuracies):
    from sklearn.metrics import roc_auc_score
    if len(np.unique(accuracies)) < 2:
        return float('nan')
    return float(roc_auc_score(accuracies, confidences))


def execute_code_safe(code, test_code, timeout=10):
    full_code = code + "\n" + test_code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(full_code)
        f.flush()
        try:
            result = subprocess.run(
                ['python3', f.name], capture_output=True, text=True, timeout=timeout
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, Exception):
            return False
        finally:
            os.unlink(f.name)


def extract_code_from_response(response):
    code_blocks = re.findall(r'```(?:python)?\n?(.*?)```', response, re.DOTALL)
    if code_blocks:
        return code_blocks[0].strip()
    return response.strip()


def extract_verbalized_confidence(response):
    # Look for explicit confidence statements
    response_lower = response.lower()
    
    # Pattern 1: Explicit confidence rating
    match = re.search(r'confidence:\s*(\d)', response)
    if match:
        return int(match.group(1)) / 5.0
    
    # Pattern 2: Our trained confidence phrases
    if "i am confident" in response_lower or "confident this solution is correct" in response_lower:
        return 0.9
    elif "should work for most cases" in response_lower or "please verify" in response_lower:
        return 0.6
    elif "not confident" in response_lower or "may contain bugs" in response_lower or "review carefully" in response_lower:
        return 0.3
    
    # Pattern 3: Numeric
    match = re.search(r'(\d)\s*/\s*5', response)
    if match:
        return int(match.group(1)) / 5.0
    
    return 0.6  # Default


def load_humaneval():
    ds = load_dataset("openai_humaneval", split="test")
    return [{"task_id": item["task_id"], "prompt": item["prompt"],
             "canonical_solution": item["canonical_solution"],
             "test": item["test"], "entry_point": item["entry_point"]} for item in ds]


def load_mbpp():
    ds = load_dataset("google-research-datasets/mbpp", "sanitized", split="test")
    return [{"task_id": f"mbpp_{item['task_id']}", "prompt": item["prompt"],
             "test": "\n".join(item["test_list"]), "code": item["code"]} for item in ds]


def evaluate_model(model, tokenizer, problems, benchmark_name, model_name, is_humaneval=True):
    """Full calibration evaluation on a model."""
    print(f"\n  Evaluating {model_name} on {benchmark_name}...")
    
    results = {
        "model": model_name, "benchmark": benchmark_name,
        "logit_confidences": [], "sampling_confidences": [],
        "verbalized_confidences": [], "correctness": [], "per_problem": [],
    }
    
    for idx, problem in enumerate(problems):
        if idx % 20 == 0:
            print(f"    Problem {idx+1}/{len(problems)}...")
        
        # Prompt with confidence request
        prompt_text = problem["prompt"] if is_humaneval else problem["prompt"]
        messages = [
            {"role": "system", "content": "You are a helpful coding assistant. Before providing your solution, state your confidence level:\n- 'I am confident this solution is correct' for high confidence\n- 'This should work for most cases, but please verify edge cases' for medium confidence\n- 'I am not confident in this solution, it may contain bugs' for low confidence\nThen provide the complete Python solution."},
            {"role": "user", "content": f"Solve this and state your confidence:\n\n{prompt_text}"}
        ]
        
        try:
            text_input = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        except Exception:
            text_input = messages[-1]["content"]
        
        input_ids = tokenizer(text_input, return_tensors="pt", truncation=True, max_length=2048).input_ids.to(model.device)
        
        sample_correct = []
        sample_logit_confs = []
        verbalized_conf = None
        
        for s in range(NUM_SAMPLES):
            with torch.no_grad():
                outputs = model.generate(
                    input_ids, max_new_tokens=MAX_NEW_TOKENS,
                    temperature=TEMPERATURE if s > 0 else 0.1,  # First sample is greedy-ish for verbalized
                    top_p=0.95, do_sample=True,
                    return_dict_in_generate=True, output_scores=True,
                    pad_token_id=tokenizer.pad_token_id,
                )
            
            generated_ids = outputs.sequences[0][input_ids.shape[1]:]
            response = tokenizer.decode(generated_ids, skip_special_tokens=True)
            code = extract_code_from_response(response)
            
            # Logit confidence
            if outputs.scores:
                token_probs = [torch.softmax(score[0], dim=-1).max().item() for score in outputs.scores]
                logit_conf = np.mean(token_probs)
            else:
                logit_conf = 0.5
            
            # Execute
            if is_humaneval:
                full_code = code if problem["prompt"] in code else problem["prompt"] + code
                test_code = problem["test"] + f"\ncheck({problem['entry_point']})"
                is_correct = execute_code_safe(full_code, test_code)
            else:
                is_correct = execute_code_safe(code, problem["test"])
            
            sample_correct.append(is_correct)
            sample_logit_confs.append(logit_conf)
            
            # Extract verbalized confidence from first (low-temp) sample
            if s == 0:
                verbalized_conf = extract_verbalized_confidence(response)
        
        pass_rate = sum(sample_correct) / len(sample_correct)
        mean_logit_conf = np.mean(sample_logit_confs)
        
        results["logit_confidences"].append(mean_logit_conf)
        results["sampling_confidences"].append(pass_rate)
        results["verbalized_confidences"].append(verbalized_conf if verbalized_conf else 0.6)
        results["correctness"].append(float(sample_correct[0]))
        results["per_problem"].append({
            "task_id": problem.get("task_id", f"{benchmark_name}_{idx}"),
            "pass_count": sum(sample_correct),
        })
    
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
        print(f"    {conf_type}: ECE={ece:.4f}, Brier={brier:.4f}, AUROC={auroc:.4f}")
    
    # pass@1 and pass@10
    pass_at_1 = np.mean(results["correctness"])
    from math import comb
    pass_at_10_list = []
    for pr in results["per_problem"]:
        n, c, k = NUM_SAMPLES, pr["pass_count"], 10
        if n - c < k:
            pass_at_10_list.append(1.0)
        else:
            pass_at_10_list.append(1.0 - comb(n - c, k) / comb(n, k))
    pass_at_10 = np.mean(pass_at_10_list)
    results["pass_at_1"] = float(pass_at_1)
    results["pass_at_10"] = float(pass_at_10)
    print(f"    pass@1={pass_at_1:.4f}, pass@10={pass_at_10:.4f}")
    
    return results


def convert_numpy(obj):
    if isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


if __name__ == "__main__":
    print("="*60)
    print("EXPERIMENT 3: Post-Training Calibration Evaluation")
    print("="*60)
    
    humaneval = load_humaneval()
    mbpp = load_mbpp()
    
    all_results = {}
    
    # Evaluate base model
    print("\n--- BASE MODEL ---")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model.eval()
    
    all_results["base_humaneval"] = evaluate_model(model, tokenizer, humaneval, "humaneval", "base", True)
    all_results["base_mbpp"] = evaluate_model(model, tokenizer, mbpp, "mbpp", "base", False)
    del model, tokenizer; torch.cuda.empty_cache()
    
    # Evaluate DPO model
    if os.path.exists(DPO_MODEL):
        print("\n--- DPO MODEL ---")
        tokenizer = AutoTokenizer.from_pretrained(DPO_MODEL, trust_remote_code=True)
        base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
        model = PeftModel.from_pretrained(base_model, DPO_MODEL)
        model.eval()
        
        all_results["dpo_humaneval"] = evaluate_model(model, tokenizer, humaneval, "humaneval", "dpo", True)
        all_results["dpo_mbpp"] = evaluate_model(model, tokenizer, mbpp, "mbpp", "dpo", False)
        del model, base_model, tokenizer; torch.cuda.empty_cache()
    
    # Evaluate SFT model
    if os.path.exists(SFT_MODEL):
        print("\n--- SFT MODEL ---")
        tokenizer = AutoTokenizer.from_pretrained(SFT_MODEL, trust_remote_code=True)
        base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
        model = PeftModel.from_pretrained(base_model, SFT_MODEL)
        model.eval()
        
        all_results["sft_humaneval"] = evaluate_model(model, tokenizer, humaneval, "humaneval", "sft", True)
        all_results["sft_mbpp"] = evaluate_model(model, tokenizer, mbpp, "mbpp", "sft", False)
        del model, base_model, tokenizer; torch.cuda.empty_cache()
    
    # Save all results
    for key, res in all_results.items():
        save_path = os.path.join(RESULTS_DIR, f"exp3_{key}.json")
        with open(save_path, 'w') as f:
            json.dump(res, f, indent=2, default=convert_numpy)
    
    # Summary table
    summary = {}
    for key, res in all_results.items():
        summary[key] = {
            "pass_at_1": res.get("pass_at_1"),
            "pass_at_10": res.get("pass_at_10"),
            "verbalized_ece": res.get("verbalized_ece"),
            "logit_ece": res.get("logit_ece"),
            "sampling_ece": res.get("sampling_ece"),
            "verbalized_auroc": res.get("verbalized_auroc"),
        }
    
    with open(os.path.join(RESULTS_DIR, "experiment3_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "="*60)
    print("EXPERIMENT 3 COMPLETE")
    print("="*60)
    for key, s in summary.items():
        print(f"\n{key}:")
        for m, v in s.items():
            if v is not None:
                print(f"  {m}: {v:.4f}")
