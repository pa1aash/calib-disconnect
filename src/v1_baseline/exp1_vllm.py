"""
Experiment 1 (vLLM): Fast Baseline Calibration Measurement
Uses vLLM for batch inference — orders of magnitude faster than HF generate.
"""

import json
import os
import sys
import time
import numpy as np
from datasets import load_dataset
import re
import subprocess
import tempfile
from math import comb
from vllm import LLM, SamplingParams

RESULTS_DIR = "/home/ubuntu/dl4c_experiments/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

MODELS = [
    ("qwen2.5-coder-7b", "Qwen/Qwen2.5-Coder-7B-Instruct"),
    ("deepseek-coder-6.7b", "deepseek-ai/deepseek-coder-6.7b-instruct"),
    ("starcoder2-7b", "bigcode/starcoder2-7b-instruct-v0.1"),
]

NUM_SAMPLES = 10
MAX_TOKENS = 512


def compute_ece(confidences, accuracies, n_bins=10):
    confidences = np.array(confidences)
    accuracies = np.array(accuracies)
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


def compute_brier(c, a):
    return float(np.mean((np.array(c) - np.array(a)) ** 2))


def compute_auroc(c, a):
    from sklearn.metrics import roc_auc_score
    c, a = np.array(c), np.array(a)
    if len(np.unique(a)) < 2:
        return float('nan')
    return float(roc_auc_score(a, c))


def execute_code_safe(code, test_code, timeout=10):
    full_code = code + "\n" + test_code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(full_code)
        f.flush()
        try:
            r = subprocess.run(['python3', f.name], capture_output=True, text=True, timeout=timeout)
            return r.returncode == 0
        except:
            return False
        finally:
            os.unlink(f.name)


def extract_code(response):
    blocks = re.findall(r'```(?:python)?\n?(.*?)```', response, re.DOTALL)
    return blocks[0].strip() if blocks else response.strip()


def extract_verbalized_conf(response):
    m = re.search(r'CONFIDENCE:\s*(\d)', response)
    if m:
        return min(max(int(m.group(1)), 1), 5) / 5.0
    m = re.search(r'(\d)\s*/\s*5', response)
    if m:
        return int(m.group(1)) / 5.0
    rl = response.lower()
    if 'very confident' in rl or 'certainly correct' in rl:
        return 0.9
    if 'confident' in rl and 'not' not in rl:
        return 0.8
    if 'fairly' in rl or 'should work' in rl or 'most cases' in rl:
        return 0.6
    if 'unsure' in rl or 'not confident' in rl or 'not sure' in rl:
        return 0.3
    return 0.6


def load_humaneval():
    ds = load_dataset("openai_humaneval", split="test")
    return [{"task_id": i["task_id"], "prompt": i["prompt"],
             "canonical_solution": i["canonical_solution"],
             "test": i["test"], "entry_point": i["entry_point"]} for i in ds]


def load_mbpp():
    ds = load_dataset("google-research-datasets/mbpp", "sanitized", split="test")
    return [{"task_id": f"mbpp_{i['task_id']}", "prompt": i["prompt"],
             "test": "\n".join(i["test_list"]), "code": i["code"]} for i in ds]


def build_code_prompt(problem, is_humaneval):
    """Build prompt for code generation."""
    if is_humaneval:
        return f"Complete the following Python function. Only output the complete function body, no explanations.\n\n{problem['prompt']}"
    else:
        return f"Write a Python function to solve the following task. Only output the function, no explanations.\n{problem['prompt']}"


def build_confidence_prompt(problem, is_humaneval):
    """Build prompt asking for confidence rating before solving."""
    p = problem["prompt"]
    return f"Before solving, rate your confidence from 1-5 (1=very unsure, 5=very confident). Format: CONFIDENCE: [N]\nThen provide the solution.\n\n{p}"


def run_model(model_key, model_path, humaneval, mbpp):
    print(f"\n{'#'*60}")
    print(f"# Model: {model_key}")
    print(f"{'#'*60}")
    
    # Load model with vLLM
    print(f"Loading {model_path} with vLLM...")
    llm = LLM(
        model=model_path,
        trust_remote_code=True,
        dtype="bfloat16",
        max_model_len=4096,
        gpu_memory_utilization=0.85,
    )
    tokenizer = llm.get_tokenizer()
    
    all_results = {}
    
    for bench_name, problems, is_humaneval in [("humaneval", humaneval, True), ("mbpp", mbpp, False)]:
        print(f"\n  --- {bench_name} ({len(problems)} problems) ---")
        start_time = time.time()
        
        # ============================
        # Phase 1: Generate N samples per problem (for pass@k and sampling confidence)
        # ============================
        print(f"  Phase 1: Generating {NUM_SAMPLES} samples per problem...")
        
        # Build all prompts
        all_prompts = []
        for prob in problems:
            prompt_text = build_code_prompt(prob, is_humaneval)
            # Try chat template
            messages = [{"role": "user", "content": prompt_text}]
            try:
                formatted = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            except:
                formatted = prompt_text
            all_prompts.append(formatted)
        
        # Generate NUM_SAMPLES completions per prompt
        sampling_params = SamplingParams(
            temperature=0.8,
            top_p=0.95,
            max_tokens=MAX_TOKENS,
            n=NUM_SAMPLES,
            logprobs=1,  # Get log probabilities for confidence
        )
        
        outputs = llm.generate(all_prompts, sampling_params)
        
        # Process results
        logit_confidences = []
        sampling_confidences = []
        correctness_list = []
        per_problem_data = []
        
        for prob_idx, (prob, output) in enumerate(zip(problems, outputs)):
            if prob_idx % 50 == 0:
                print(f"    Processing {prob_idx}/{len(problems)}...")
            
            sample_correct = []
            sample_logprobs = []
            
            for completion in output.outputs:
                response = completion.text
                code = extract_code(response)
                
                # Compute logit-based confidence from logprobs
                if completion.logprobs:
                    token_probs = []
                    for lp in completion.logprobs[:50]:  # First 50 tokens
                        if lp:
                            # Get the probability of the chosen token
                            for token_id, logprob_obj in lp.items():
                                token_probs.append(np.exp(logprob_obj.logprob))
                                break
                    mean_prob = np.mean(token_probs) if token_probs else 0.5
                else:
                    mean_prob = 0.5
                
                # Execute code
                if is_humaneval:
                    full_code = code if prob["prompt"] in code else prob["prompt"] + code
                    test_code = prob["test"] + f"\ncheck({prob['entry_point']})"
                else:
                    full_code = code
                    test_code = prob["test"]
                is_correct = execute_code_safe(full_code, test_code)
                
                sample_correct.append(is_correct)
                sample_logprobs.append(mean_prob)
            
            pass_rate = sum(sample_correct) / len(sample_correct)
            mean_logit = np.mean(sample_logprobs)
            
            logit_confidences.append(float(mean_logit))
            sampling_confidences.append(float(pass_rate))
            correctness_list.append(float(sample_correct[0]))
            per_problem_data.append({
                "task_id": prob.get("task_id", f"{bench_name}_{prob_idx}"),
                "pass_count": sum(sample_correct),
                "pass_rate": float(pass_rate),
                "mean_logit_conf": float(mean_logit),
            })
        
        # ============================
        # Phase 2: Get verbalized confidence (single generation per problem)
        # ============================
        print(f"  Phase 2: Getting verbalized confidence...")
        
        conf_prompts = []
        for prob in problems:
            prompt_text = build_confidence_prompt(prob, is_humaneval)
            messages = [{"role": "user", "content": prompt_text}]
            try:
                formatted = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            except:
                formatted = prompt_text
            conf_prompts.append(formatted)
        
        conf_params = SamplingParams(temperature=0.1, max_tokens=MAX_TOKENS, n=1)
        conf_outputs = llm.generate(conf_prompts, conf_params)
        
        verbalized_confidences = []
        for co in conf_outputs:
            resp = co.outputs[0].text
            vc = extract_verbalized_conf(resp)
            verbalized_confidences.append(float(vc))
        
        # ============================
        # Compute metrics
        # ============================
        elapsed = time.time() - start_time
        print(f"  Completed in {elapsed:.1f}s")
        
        results = {
            "model": model_key,
            "benchmark": bench_name,
            "num_problems": len(problems),
            "num_samples": NUM_SAMPLES,
            "time_seconds": elapsed,
        }
        
        for cname, confs in [("logit", logit_confidences), ("sampling", sampling_confidences), ("verbalized", verbalized_confidences)]:
            ece, bins = compute_ece(confs, correctness_list)
            brier = compute_brier(confs, correctness_list)
            auroc = compute_auroc(confs, correctness_list)
            results[f"{cname}_ece"] = ece
            results[f"{cname}_brier"] = brier
            results[f"{cname}_auroc"] = auroc
            results[f"{cname}_bins"] = bins
            results[f"{cname}_confidences"] = confs
            print(f"    {cname}: ECE={ece:.4f}, Brier={brier:.4f}, AUROC={auroc:.4f}")
        
        results["correctness"] = correctness_list
        results["per_problem"] = per_problem_data
        
        # pass@1 and pass@10
        p1 = np.mean(correctness_list)
        p10_list = []
        for pp in per_problem_data:
            n, c = NUM_SAMPLES, pp["pass_count"]
            k = min(10, n)
            if n - c < k:
                p10_list.append(1.0)
            else:
                p10_list.append(1.0 - comb(n - c, k) / comb(n, k))
        p10 = np.mean(p10_list)
        results["pass_at_1"] = float(p1)
        results["pass_at_10"] = float(p10)
        print(f"    pass@1={p1:.4f}, pass@10={p10:.4f}")
        
        # Save
        sp = os.path.join(RESULTS_DIR, f"exp1_{model_key}_{bench_name}.json")
        with open(sp, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"    Saved: {sp}")
        
        all_results[f"{model_key}_{bench_name}"] = results
    
    # Free GPU memory
    del llm
    import gc; gc.collect()
    try:
        import torch; torch.cuda.empty_cache()
    except: pass
    
    return all_results


if __name__ == "__main__":
    print("="*60)
    print("EXPERIMENT 1: Baseline Calibration (vLLM)")
    print("="*60)
    
    humaneval = load_humaneval()
    mbpp = load_mbpp()
    print(f"HumanEval: {len(humaneval)}, MBPP: {len(mbpp)}")
    
    all_results = {}
    
    for model_key, model_path in MODELS:
        try:
            results = run_model(model_key, model_path, humaneval, mbpp)
            all_results.update(results)
        except Exception as e:
            print(f"  ERROR with {model_key}: {e}")
            import traceback; traceback.print_exc()
    
    # Save summary
    summary = {}
    for k, r in all_results.items():
        summary[k] = {m: r.get(m) for m in [
            "pass_at_1", "pass_at_10",
            "logit_ece", "sampling_ece", "verbalized_ece",
            "logit_brier", "sampling_brier", "verbalized_brier",
            "logit_auroc", "sampling_auroc", "verbalized_auroc",
        ]}
    
    with open(os.path.join(RESULTS_DIR, "experiment1_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "="*60)
    print("EXPERIMENT 1 COMPLETE")
    print("="*60)
    for k, s in summary.items():
        print(f"\n{k}:")
        for m, v in s.items():
            if v is not None:
                print(f"  {m}: {v:.4f}")
