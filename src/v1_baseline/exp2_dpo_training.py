"""
Experiment 2: Confidence-Aware DPO Training
1. Generate training data from APPS problems with execution-based confidence labels
2. Train Qwen2.5-Coder-7B-Instruct with DPO on confidence-annotated pairs
"""

import json
import os
import sys
import time
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from datasets import load_dataset, Dataset
from peft import LoraConfig, get_peft_model, TaskType
from trl import DPOTrainer, DPOConfig
import re
import subprocess
import tempfile
from collections import defaultdict

RESULTS_DIR = "/home/ubuntu/dl4c_experiments/results"
DATA_DIR = "/home/ubuntu/dl4c_experiments/data"
MODEL_DIR = "/home/ubuntu/dl4c_experiments/models"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

BASE_MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct"
NUM_SAMPLES_PER_PROBLEM = 20
TEMPERATURE = 0.8
MAX_NEW_TOKENS = 512

# Confidence labels based on empirical pass rate
CONFIDENCE_LABELS = {
    "high": "I am confident this solution is correct. The logic handles the requirements and edge cases well.",
    "medium": "This solution should work for most cases, but please verify edge cases. There may be subtle issues I'm not certain about.",
    "low": "I am not confident in this solution. It may contain bugs or miss important edge cases. Please review carefully before using.",
}

OVERCONFIDENT_LABELS = {
    "high_on_hard": "I am confident this solution is correct. The logic handles the requirements and edge cases well.",
    "medium_on_hard": "This solution should work for most cases, but please verify edge cases.",
}

UNDERCONFIDENT_LABELS = {
    "low_on_easy": "I am not confident in this solution. It may contain bugs or miss important edge cases.",
    "medium_on_easy": "This solution should work for most cases, but please verify edge cases.",
}


def execute_code_safe(code, test_inputs=None, timeout=10):
    """Execute Python code safely with timeout."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
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


def extract_code_from_response(response):
    """Extract Python code from model response."""
    code_blocks = re.findall(r'```(?:python)?\n?(.*?)```', response, re.DOTALL)
    if code_blocks:
        return code_blocks[0].strip()
    return response.strip()


def generate_dpo_data():
    """Generate DPO training pairs from APPS dataset."""
    print("Loading APPS dataset...")
    # Use APPS introductory level for feasibility
    ds = load_dataset("codeparrot/apps", split="train", trust_remote_code=True)
    
    # Filter for introductory difficulty problems with test cases
    problems = []
    for item in ds:
        if item.get("difficulty") == "introductory" and item.get("input_output"):
            try:
                io = json.loads(item["input_output"])
                if "inputs" in io and "outputs" in io and len(io["inputs"]) >= 2:
                    problems.append({
                        "question": item["question"],
                        "solutions": item.get("solutions", ""),
                        "input_output": io,
                    })
            except (json.JSONDecodeError, KeyError):
                continue
        if len(problems) >= 500:  # Cap at 500 problems for data generation
            break
    
    print(f"Found {len(problems)} suitable problems")
    
    # Load model for generation
    print(f"Loading {BASE_MODEL}...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model.eval()
    
    dpo_pairs = []
    
    for idx, problem in enumerate(problems):
        if idx % 20 == 0:
            print(f"  Problem {idx+1}/{len(problems)}...")
        
        question = problem["question"]
        io = problem["input_output"]
        
        # Generate samples
        messages = [
            {"role": "system", "content": "You are a helpful coding assistant. Write a complete Python solution for the given problem. Read input from stdin and write output to stdout."},
            {"role": "user", "content": f"Solve the following programming problem:\n\n{question}"}
        ]
        
        try:
            text_input = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        except Exception:
            text_input = messages[-1]["content"]
        
        input_ids = tokenizer(text_input, return_tensors="pt", truncation=True, max_length=2048).input_ids.to(model.device)
        
        sample_results = []
        for s in range(NUM_SAMPLES_PER_PROBLEM):
            with torch.no_grad():
                outputs = model.generate(
                    input_ids,
                    max_new_tokens=MAX_NEW_TOKENS,
                    temperature=TEMPERATURE,
                    top_p=0.95,
                    do_sample=True,
                    pad_token_id=tokenizer.pad_token_id,
                )
            
            generated_ids = outputs[0][input_ids.shape[1]:]
            response = tokenizer.decode(generated_ids, skip_special_tokens=True)
            code = extract_code_from_response(response)
            
            # Test against IO pairs
            correct_count = 0
            total_tests = min(len(io["inputs"]), 3)  # Test on up to 3 IO pairs
            for t in range(total_tests):
                test_code = code + f"\n# Redirect stdin\nimport sys\nfrom io import StringIO\nsys.stdin = StringIO({repr(io['inputs'][t])})\n"
                # Check if output matches
                full_test = f"""
import sys
from io import StringIO

_input = {repr(io['inputs'][t])}
_expected = {repr(io['outputs'][t]).strip()}

sys.stdin = StringIO(_input)

# Capture stdout
from io import StringIO as SIO
_old_stdout = sys.stdout
sys.stdout = _captured = SIO()

try:
{chr(10).join('    ' + line for line in code.split(chr(10)))}
except:
    pass

sys.stdout = _old_stdout
_actual = _captured.getvalue().strip()
_expected_clean = _expected.strip()

if _actual == _expected_clean:
    sys.exit(0)
else:
    sys.exit(1)
"""
                is_correct = execute_code_safe(full_test, timeout=5)
                if is_correct:
                    correct_count += 1
            
            pass_rate = correct_count / total_tests if total_tests > 0 else 0
            sample_results.append({
                "code": code,
                "response": response,
                "pass_rate": pass_rate,
                "fully_correct": pass_rate == 1.0,
            })
        
        # Compute empirical difficulty
        fully_correct_count = sum(1 for s in sample_results if s["fully_correct"])
        empirical_difficulty = fully_correct_count / len(sample_results)
        
        # Assign ground-truth confidence category
        if empirical_difficulty >= 0.7:
            true_confidence = "high"
        elif empirical_difficulty >= 0.3:
            true_confidence = "medium"
        else:
            true_confidence = "low"
        
        # Create DPO pairs
        # Find one correct and one incorrect sample (or closest)
        correct_samples = [s for s in sample_results if s["fully_correct"]]
        incorrect_samples = [s for s in sample_results if not s["fully_correct"]]
        
        if not correct_samples and not incorrect_samples:
            continue
        
        # Pair 1: Calibrated chosen vs. overconfident rejected
        if incorrect_samples and true_confidence in ["low", "medium"]:
            # Chosen: incorrect solution with honest low confidence
            chosen_sample = incorrect_samples[0]
            chosen_response = f"{CONFIDENCE_LABELS[true_confidence]}\n\n```python\n{chosen_sample['code']}\n```"
            
            # Rejected: incorrect solution with falsely high confidence
            rejected_sample = incorrect_samples[min(1, len(incorrect_samples)-1)]
            rejected_response = f"{CONFIDENCE_LABELS['high']}\n\n```python\n{rejected_sample['code']}\n```"
            
            dpo_pairs.append({
                "prompt": f"Solve the following programming problem. First state your confidence level, then provide the solution.\n\n{question}",
                "chosen": chosen_response,
                "rejected": rejected_response,
                "true_confidence": true_confidence,
                "empirical_difficulty": empirical_difficulty,
                "pair_type": "overconfident_rejected",
            })
        
        # Pair 2: Calibrated chosen vs. underconfident rejected  
        if correct_samples and true_confidence in ["high", "medium"]:
            # Chosen: correct solution with honest high confidence
            chosen_sample = correct_samples[0]
            chosen_response = f"{CONFIDENCE_LABELS[true_confidence]}\n\n```python\n{chosen_sample['code']}\n```"
            
            # Rejected: correct solution with falsely low confidence
            rejected_sample = correct_samples[min(1, len(correct_samples)-1)]
            rejected_response = f"{CONFIDENCE_LABELS['low']}\n\n```python\n{rejected_sample['code']}\n```"
            
            dpo_pairs.append({
                "prompt": f"Solve the following programming problem. First state your confidence level, then provide the solution.\n\n{question}",
                "chosen": chosen_response,
                "rejected": rejected_response,
                "true_confidence": true_confidence,
                "empirical_difficulty": empirical_difficulty,
                "pair_type": "underconfident_rejected",
            })
        
        # Pair 3: Correct+calibrated chosen vs. incorrect+overconfident rejected
        if correct_samples and incorrect_samples:
            chosen_sample = correct_samples[0]
            chosen_conf = "high" if empirical_difficulty >= 0.7 else "medium"
            chosen_response = f"{CONFIDENCE_LABELS[chosen_conf]}\n\n```python\n{chosen_sample['code']}\n```"
            
            rejected_sample = incorrect_samples[0]
            rejected_response = f"{CONFIDENCE_LABELS['high']}\n\n```python\n{rejected_sample['code']}\n```"
            
            dpo_pairs.append({
                "prompt": f"Solve the following programming problem. First state your confidence level, then provide the solution.\n\n{question}",
                "chosen": chosen_response,
                "rejected": rejected_response,
                "true_confidence": true_confidence,
                "empirical_difficulty": empirical_difficulty,
                "pair_type": "correct_calibrated_vs_incorrect_overconfident",
            })
    
    print(f"\nGenerated {len(dpo_pairs)} DPO pairs")
    
    # Save data
    data_path = os.path.join(DATA_DIR, "dpo_confidence_pairs.json")
    with open(data_path, 'w') as f:
        json.dump(dpo_pairs, f, indent=2)
    print(f"Saved to {data_path}")
    
    # Free model
    del model
    del tokenizer
    torch.cuda.empty_cache()
    
    return dpo_pairs


def train_dpo(dpo_pairs):
    """Train model with DPO on confidence-annotated pairs."""
    print(f"\n{'='*60}")
    print("DPO TRAINING")
    print(f"{'='*60}")
    
    # Prepare dataset
    train_data = {
        "prompt": [p["prompt"] for p in dpo_pairs],
        "chosen": [p["chosen"] for p in dpo_pairs],
        "rejected": [p["rejected"] for p in dpo_pairs],
    }
    dataset = Dataset.from_dict(train_data)
    
    # Split 90/10
    split = dataset.train_test_split(test_size=0.1, seed=42)
    train_dataset = split["train"]
    eval_dataset = split["test"]
    
    print(f"Train: {len(train_dataset)}, Eval: {len(eval_dataset)}")
    
    # Load model
    print(f"Loading {BASE_MODEL}...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # LoRA config
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        task_type=TaskType.CAUSAL_LM,
        bias="none",
    )
    
    # DPO config
    output_dir = os.path.join(MODEL_DIR, "qwen_confidence_dpo")
    
    training_args = DPOConfig(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=2,
        per_device_eval_batch_size=2,
        gradient_accumulation_steps=8,
        learning_rate=5e-7,
        beta=0.1,
        lr_scheduler_type="cosine",
        warmup_ratio=0.1,
        bf16=True,
        logging_steps=10,
        eval_strategy="steps",
        eval_steps=50,
        save_strategy="steps",
        save_steps=100,
        max_length=2048,
        max_prompt_length=1024,
        report_to="none",
        gradient_checkpointing=True,
        remove_unused_columns=False,
    )
    
    # DPO Trainer
    trainer = DPOTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        processing_class=tokenizer,
        peft_config=lora_config,
    )
    
    print("Starting DPO training...")
    start_time = time.time()
    trainer.train()
    train_time = time.time() - start_time
    print(f"Training completed in {train_time/60:.1f} minutes")
    
    # Save model
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Model saved to {output_dir}")
    
    # Save training metrics
    train_metrics = {
        "training_time_minutes": train_time / 60,
        "num_train_pairs": len(train_dataset),
        "num_eval_pairs": len(eval_dataset),
        "final_train_loss": trainer.state.log_history[-1].get("loss", None) if trainer.state.log_history else None,
    }
    with open(os.path.join(RESULTS_DIR, "dpo_training_metrics.json"), 'w') as f:
        json.dump(train_metrics, f, indent=2)
    
    # Free memory
    del model
    del tokenizer
    del trainer
    torch.cuda.empty_cache()
    
    return output_dir


def train_sft_baseline(dpo_pairs):
    """Train SFT baseline (only on chosen responses, no preference signal)."""
    from trl import SFTTrainer, SFTConfig
    
    print(f"\n{'='*60}")
    print("SFT BASELINE TRAINING")
    print(f"{'='*60}")
    
    # Prepare dataset - just prompt + chosen response
    sft_data = []
    for p in dpo_pairs:
        sft_data.append({
            "messages": [
                {"role": "user", "content": p["prompt"]},
                {"role": "assistant", "content": p["chosen"]},
            ]
        })
    
    dataset = Dataset.from_list(sft_data)
    split = dataset.train_test_split(test_size=0.1, seed=42)
    
    print(f"Train: {len(split['train'])}, Eval: {len(split['test'])}")
    
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        task_type=TaskType.CAUSAL_LM,
        bias="none",
    )
    
    output_dir = os.path.join(MODEL_DIR, "qwen_confidence_sft")
    
    training_args = SFTConfig(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=2,
        per_device_eval_batch_size=2,
        gradient_accumulation_steps=8,
        learning_rate=2e-5,
        lr_scheduler_type="cosine",
        warmup_ratio=0.1,
        bf16=True,
        logging_steps=10,
        eval_strategy="steps",
        eval_steps=50,
        save_strategy="steps",
        save_steps=100,
        max_seq_length=2048,
        report_to="none",
        gradient_checkpointing=True,
    )
    
    def formatting_func(example):
        return tokenizer.apply_chat_template(example["messages"], tokenize=False, add_generation_prompt=False)
    
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=split["train"],
        eval_dataset=split["test"],
        processing_class=tokenizer,
        peft_config=lora_config,
        formatting_func=formatting_func,
    )
    
    print("Starting SFT training...")
    start_time = time.time()
    trainer.train()
    train_time = time.time() - start_time
    print(f"SFT training completed in {train_time/60:.1f} minutes")
    
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"SFT model saved to {output_dir}")
    
    del model, tokenizer, trainer
    torch.cuda.empty_cache()
    
    return output_dir


if __name__ == "__main__":
    # Step 1: Generate DPO data
    data_path = os.path.join(DATA_DIR, "dpo_confidence_pairs.json")
    if os.path.exists(data_path):
        print(f"Loading existing DPO data from {data_path}...")
        with open(data_path) as f:
            dpo_pairs = json.load(f)
    else:
        dpo_pairs = generate_dpo_data()
    
    print(f"\nTotal DPO pairs: {len(dpo_pairs)}")
    pair_types = defaultdict(int)
    for p in dpo_pairs:
        pair_types[p["pair_type"]] += 1
    print("Pair type distribution:")
    for pt, count in pair_types.items():
        print(f"  {pt}: {count}")
    
    # Step 2: DPO training
    dpo_model_dir = train_dpo(dpo_pairs)
    
    # Step 3: SFT baseline
    sft_model_dir = train_sft_baseline(dpo_pairs)
    
    print("\n" + "="*60)
    print("EXPERIMENT 2 COMPLETE")
    print(f"DPO model: {dpo_model_dir}")
    print(f"SFT model: {sft_model_dir}")
    print("="*60)
