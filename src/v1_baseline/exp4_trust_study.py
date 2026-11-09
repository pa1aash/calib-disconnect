"""
Experiment 4: Simulated Trust Calibration Study
Uses GPT-4 as a simulated developer to evaluate whether calibrated confidence
improves decision-making about accepting/rejecting AI-generated code.
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

MAX_NEW_TOKENS = 512


def execute_code_safe(code, test_code, timeout=10):
    full_code = code + "\n" + test_code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(full_code)
        f.flush()
        try:
            result = subprocess.run(['python3', f.name], capture_output=True, text=True, timeout=timeout)
            return result.returncode == 0
        except:
            return False
        finally:
            os.unlink(f.name)


def extract_code_from_response(response):
    code_blocks = re.findall(r'```(?:python)?\n?(.*?)```', response, re.DOTALL)
    if code_blocks:
        return code_blocks[0].strip()
    return response.strip()


def extract_confidence_text(response):
    """Extract the confidence statement from a response."""
    lines = response.strip().split('\n')
    conf_lines = []
    for line in lines[:5]:  # Check first 5 lines
        if any(kw in line.lower() for kw in ['confident', 'confidence', 'unsure', 'verify', 'review', 'bugs']):
            conf_lines.append(line)
    return ' '.join(conf_lines) if conf_lines else ""


def simulated_developer_decision(problem_desc, code, confidence_text, has_confidence):
    """
    Simulate a developer's decision using a rule-based approach.
    Developer sees: problem, code, optional confidence signal.
    Decision: accept (use as-is), modify (use with changes), reject (rewrite).
    
    We use a deterministic rubric based on code characteristics.
    """
    # Simple heuristic "developer" that evaluates code quality signals
    score = 0.5  # Start neutral
    
    # Code length heuristic
    code_lines = code.strip().split('\n')
    if len(code_lines) < 3:
        score -= 0.1  # Too short might be wrong
    elif len(code_lines) > 50:
        score -= 0.05  # Very long code might be overengineered
    
    # Has docstring?
    if '"""' in code or "'''" in code:
        score += 0.05
    
    # Has error handling?
    if 'try:' in code or 'except' in code:
        score += 0.05
    
    # Has edge case checks?
    if 'if not' in code or 'if len' in code or '== 0' in code or 'is None' in code:
        score += 0.05
    
    # Apply confidence signal
    if has_confidence and confidence_text:
        conf_lower = confidence_text.lower()
        if 'not confident' in conf_lower or 'may contain bugs' in conf_lower or 'review carefully' in conf_lower:
            score -= 0.2  # Developer is more cautious
        elif 'confident this solution is correct' in conf_lower or 'i am confident' in conf_lower:
            score += 0.15  # Developer trusts more
        elif 'should work for most cases' in conf_lower or 'verify edge cases' in conf_lower:
            score += 0.0  # Neutral signal
    
    # Decision based on score
    if score >= 0.6:
        return "accept"
    elif score >= 0.4:
        return "modify"
    else:
        return "reject"


def run_trust_study():
    print("="*60)
    print("EXPERIMENT 4: Simulated Trust Calibration Study")
    print("="*60)
    
    # Load HumanEval for test scenarios
    ds = load_dataset("openai_humaneval", split="test")
    problems = [{"task_id": item["task_id"], "prompt": item["prompt"],
                 "test": item["test"], "entry_point": item["entry_point"],
                 "canonical_solution": item["canonical_solution"]} for item in ds]
    
    # Use first 50 problems
    problems = problems[:50]
    
    # Load models
    print("Loading base model...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    print("Loading DPO model...")
    dpo_model = None
    if os.path.exists(DPO_MODEL):
        dpo_base = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
        dpo_model = PeftModel.from_pretrained(dpo_base, DPO_MODEL)
        dpo_model.eval()
    
    base_model.eval()
    
    conditions = {
        "no_confidence": {"model": base_model, "show_confidence": False, "use_conf_prompt": False},
        "uncalibrated_confidence": {"model": base_model, "show_confidence": True, "use_conf_prompt": True},
    }
    if dpo_model:
        conditions["calibrated_confidence"] = {"model": dpo_model, "show_confidence": True, "use_conf_prompt": True}
    
    all_results = {}
    
    for cond_name, cond_config in conditions.items():
        print(f"\n--- Condition: {cond_name} ---")
        model = cond_config["model"]
        
        decisions = []
        correct_accepts = 0
        incorrect_accepts = 0
        correct_rejects = 0
        incorrect_rejects = 0
        total = 0
        
        for idx, problem in enumerate(problems):
            if idx % 10 == 0:
                print(f"  Problem {idx+1}/{len(problems)}...")
            
            # Generate solution
            if cond_config["use_conf_prompt"]:
                messages = [
                    {"role": "system", "content": "You are a helpful coding assistant. Before providing your solution, state your confidence level:\n- 'I am confident this solution is correct' for high confidence\n- 'This should work for most cases, but please verify edge cases' for medium confidence\n- 'I am not confident in this solution, it may contain bugs' for low confidence\nThen provide the complete Python solution."},
                    {"role": "user", "content": f"Complete the following Python function and state your confidence:\n\n{problem['prompt']}"}
                ]
            else:
                messages = [
                    {"role": "system", "content": "You are a helpful coding assistant. Complete the given Python function."},
                    {"role": "user", "content": f"Complete the following Python function:\n\n{problem['prompt']}"}
                ]
            
            try:
                text_input = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            except:
                text_input = messages[-1]["content"]
            
            input_ids = tokenizer(text_input, return_tensors="pt", truncation=True, max_length=2048).input_ids.to(model.device)
            
            with torch.no_grad():
                outputs = model.generate(
                    input_ids, max_new_tokens=MAX_NEW_TOKENS,
                    temperature=0.1, do_sample=True,
                    pad_token_id=tokenizer.pad_token_id,
                )
            
            response = tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True)
            code = extract_code_from_response(response)
            confidence_text = extract_confidence_text(response) if cond_config["show_confidence"] else ""
            
            # Check actual correctness
            full_code = code if problem["prompt"] in code else problem["prompt"] + code
            test_code = problem["test"] + f"\ncheck({problem['entry_point']})"
            is_actually_correct = execute_code_safe(full_code, test_code)
            
            # Simulated developer decision
            decision = simulated_developer_decision(
                problem["prompt"], code, confidence_text, cond_config["show_confidence"]
            )
            
            # Track outcomes
            total += 1
            if decision == "accept" and is_actually_correct:
                correct_accepts += 1
            elif decision == "accept" and not is_actually_correct:
                incorrect_accepts += 1  # Overtrust!
            elif decision in ["reject", "modify"] and not is_actually_correct:
                correct_rejects += 1
            elif decision in ["reject", "modify"] and is_actually_correct:
                incorrect_rejects += 1  # Undertrust!
            
            decisions.append({
                "task_id": problem["task_id"],
                "is_correct": is_actually_correct,
                "decision": decision,
                "confidence_text": confidence_text,
                "has_confidence": cond_config["show_confidence"],
            })
        
        # Compute metrics
        acceptance_rate = sum(1 for d in decisions if d["decision"] == "accept") / total
        correct_rate = sum(1 for d in decisions if d["is_correct"]) / total
        
        # Trust calibration metrics
        overtrust_rate = incorrect_accepts / total  # Accepted but wrong
        undertrust_rate = incorrect_rejects / total  # Rejected but correct
        decision_accuracy = (correct_accepts + correct_rejects) / total
        
        # Appropriate trust: accepted correct + rejected incorrect
        appropriate_trust = (correct_accepts + correct_rejects) / total if total > 0 else 0
        
        cond_results = {
            "condition": cond_name,
            "total": total,
            "acceptance_rate": acceptance_rate,
            "correct_rate": correct_rate,
            "overtrust_rate": overtrust_rate,
            "undertrust_rate": undertrust_rate,
            "decision_accuracy": decision_accuracy,
            "appropriate_trust": appropriate_trust,
            "correct_accepts": correct_accepts,
            "incorrect_accepts": incorrect_accepts,
            "correct_rejects": correct_rejects,
            "incorrect_rejects": incorrect_rejects,
            "decisions": decisions,
        }
        
        all_results[cond_name] = cond_results
        
        print(f"  Acceptance rate: {acceptance_rate:.3f}")
        print(f"  Correct rate: {correct_rate:.3f}")
        print(f"  Overtrust rate: {overtrust_rate:.3f}")
        print(f"  Undertrust rate: {undertrust_rate:.3f}")
        print(f"  Decision accuracy: {decision_accuracy:.3f}")
        print(f"  Appropriate trust: {appropriate_trust:.3f}")
    
    # Save results
    save_path = os.path.join(RESULTS_DIR, "experiment4_trust_study.json")
    with open(save_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {save_path}")
    
    # Summary table
    print("\n" + "="*60)
    print("TRUST CALIBRATION SUMMARY")
    print("="*60)
    print(f"{'Condition':<30} {'Accept%':>8} {'Overtrust':>10} {'Undertrust':>11} {'DecAcc':>8}")
    print("-"*70)
    for cond_name, res in all_results.items():
        print(f"{cond_name:<30} {res['acceptance_rate']:>7.3f} {res['overtrust_rate']:>10.3f} {res['undertrust_rate']:>11.3f} {res['decision_accuracy']:>8.3f}")
    
    # Cleanup
    del base_model
    if dpo_model:
        del dpo_model
    torch.cuda.empty_cache()


if __name__ == "__main__":
    run_trust_study()
