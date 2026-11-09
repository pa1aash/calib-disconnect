"""
Experiment 3+4: Evaluate SFT model + Trust Study
Handles CUDA errors gracefully.
"""

import json, os, time, re, subprocess, tempfile, gc
import numpy as np
import torch
from math import comb
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from datasets import load_dataset

RESULTS_DIR = "/home/ubuntu/dl4c_experiments/results"
MODEL_DIR = "/home/ubuntu/dl4c_experiments/models"
BASE_MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct"
SFT_MODEL = os.path.join(MODEL_DIR, "qwen_confidence_sft")
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
            bins.append({"bin_lower": float(bounds[i]), "bin_upper": float(bounds[i+1]),
                        "accuracy": ba, "confidence": bc, "count": bs})
    return float(ece), bins

def compute_brier(c, a): return float(np.mean((np.array(c) - np.array(a)) ** 2))

def compute_auroc(c, a):
    from sklearn.metrics import roc_auc_score
    c, a = np.array(c), np.array(a)
    return float(roc_auc_score(a, c)) if len(np.unique(a)) >= 2 else float('nan')

def _run_code(code, timeout=10):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code); f.flush()
        try: return subprocess.run(['python3', f.name], capture_output=True, text=True, timeout=timeout).returncode == 0
        except: return False
        finally: os.unlink(f.name)

def extract_code(resp):
    blocks = re.findall(r'```(?:python)?\n?(.*?)```', resp, re.DOTALL)
    return blocks[0].strip() if blocks else resp.strip()

def extract_conf(resp, trained=False):
    if trained:
        rl = resp.lower()
        if 'i am confident this solution is correct' in rl: return 0.9
        if 'should work for most cases' in rl or 'please verify' in rl: return 0.6
        if 'not confident' in rl or 'may contain bugs' in rl: return 0.3
    m = re.search(r'CONFIDENCE:\s*(\d)', resp)
    if m: return min(max(int(m.group(1)), 1), 5) / 5.0
    rl = resp.lower()
    if 'very confident' in rl: return 0.9
    if 'confident' in rl and 'not' not in rl: return 0.8
    if 'should work' in rl: return 0.6
    if 'unsure' in rl or 'not confident' in rl: return 0.3
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
        except RuntimeError as e:
            print(f"    Generation error: {e}")
            results.append("")
    return results

def fmt(tokenizer, msgs):
    try: return tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    except: return msgs[-1]["content"]

def load_humaneval():
    ds = load_dataset("openai_humaneval", split="test")
    return [{"task_id": i["task_id"], "prompt": i["prompt"], "canonical_solution": i["canonical_solution"],
             "test": i["test"], "entry_point": i["entry_point"]} for i in ds]

if __name__ == "__main__":
    humaneval = load_humaneval()
    
    # ===== Experiment 3: Evaluate SFT model =====
    sft_path = os.path.join(RESULTS_DIR, "exp3_qwen-sft_humaneval.json")
    if not os.path.exists(sft_path):
        print("=== EXPERIMENT 3: SFT Model Evaluation ===", flush=True)
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
        if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
        base_m = AutoModelForCausalLM.from_pretrained(BASE_MODEL, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
        sft_m = PeftModel.from_pretrained(base_m, SFT_MODEL)
        sft_m.eval()
        
        sampling_confs, verbal_confs, corr_list, per_problem = [], [], [], []
        t0 = time.time()
        
        for idx, prob in enumerate(humaneval):
            if idx % 10 == 0: print(f"  [{idx}/{len(humaneval)}] ({time.time()-t0:.0f}s)", flush=True)
            
            # Code generation
            pi = fmt(tokenizer, [{"role": "user", "content": f"Complete the following Python function. Only output the function.\n\n{prob['prompt']}"}])
            samples = gen(sft_m, tokenizer, pi, NUM_SAMPLES, 0.8)
            
            sample_ok = []
            for s in samples:
                code = extract_code(s)
                fc = code if prob["prompt"] in code else prob["prompt"] + code
                tc = prob["test"] + f"\ncheck({prob['entry_point']})"
                sample_ok.append(_run_code(fc + "\n" + tc))
            
            pr = sum(sample_ok) / max(len(sample_ok), 1)
            
            # Confidence
            ci = fmt(tokenizer, [{"role": "system", "content": "Before solving, state your confidence:\n- 'I am confident this solution is correct' for high confidence\n- 'This should work for most cases, but please verify edge cases' for medium\n- 'I am not confident in this solution, it may contain bugs' for low\nThen provide the solution."},
                                 {"role": "user", "content": f"State confidence and solve:\n\n{prob['prompt']}"}])
            cresp = gen(sft_m, tokenizer, ci, 1, 0.1)[0]
            vc = extract_conf(cresp, trained=True)
            
            sampling_confs.append(float(pr))
            verbal_confs.append(float(vc))
            corr_list.append(float(sample_ok[0] if sample_ok else False))
            per_problem.append({"task_id": prob["task_id"], "pass_count": sum(sample_ok), "pass_rate": float(pr)})
        
        results = {"model": "qwen-sft", "benchmark": "humaneval", "time_seconds": time.time()-t0}
        for cn, cv in [("sampling", sampling_confs), ("verbalized", verbal_confs)]:
            ece, bins = compute_ece(cv, corr_list)
            results[f"{cn}_ece"] = ece
            results[f"{cn}_brier"] = compute_brier(cv, corr_list)
            results[f"{cn}_auroc"] = compute_auroc(cv, corr_list)
            results[f"{cn}_bins"] = bins
            results[f"{cn}_confidences"] = cv
            print(f"  {cn}: ECE={ece:.4f}")
        
        results["correctness"] = corr_list
        results["per_problem"] = per_problem
        results["pass_at_1"] = float(np.mean(corr_list))
        results["pass_at_10"] = float(np.mean([1.0 if NUM_SAMPLES-p["pass_count"]<10 else 1.0-comb(NUM_SAMPLES-p["pass_count"],10)/comb(NUM_SAMPLES,10) for p in per_problem]))
        print(f"  pass@1={results['pass_at_1']:.4f}")
        
        with open(sft_path, 'w') as f: json.dump(results, f, indent=2)
        del sft_m, base_m, tokenizer; torch.cuda.empty_cache(); gc.collect()
    else:
        print("SFT eval already done, skipping.")
    
    # ===== Experiment 4: Trust Study =====
    trust_path = os.path.join(RESULTS_DIR, "experiment4_trust_study.json")
    if not os.path.exists(trust_path):
        print("\n=== EXPERIMENT 4: Trust Study ===", flush=True)
        problems = humaneval[:50]
        
        conditions = {}
        
        # Base model conditions
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
        if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
        base_m = AutoModelForCausalLM.from_pretrained(BASE_MODEL, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
        base_m.eval()
        
        for cname, show_c in [("no_confidence", False), ("uncalibrated", True)]:
            print(f"\n  Condition: {cname}", flush=True)
            decisions = []
            for idx, prob in enumerate(problems):
                if idx % 10 == 0: print(f"    [{idx}/{len(problems)}]", flush=True)
                
                if show_c:
                    pi = fmt(tokenizer, [{"role": "user", "content": f"Rate confidence 1-5. Format: CONFIDENCE: [N]. Then solve.\n\n{prob['prompt']}"}])
                else:
                    pi = fmt(tokenizer, [{"role": "user", "content": f"Complete:\n\n{prob['prompt']}"}])
                
                resp = gen(base_m, tokenizer, pi, 1, 0.1)[0]
                code = extract_code(resp)
                fc = code if prob["prompt"] in code else prob["prompt"] + code
                tc = prob["test"] + f"\ncheck({prob['entry_point']})"
                ok = _run_code(fc + "\n" + tc)
                conf = extract_conf(resp) if show_c else None
                
                # Decision
                score = 0.5
                if len(code.strip().split('\n')) < 2: score -= 0.15
                if 'try:' in code: score += 0.05
                if show_c and conf is not None:
                    if conf >= 0.8: score += 0.15
                    elif conf < 0.5: score -= 0.2
                
                dec = "accept" if score >= 0.55 else ("modify" if score >= 0.35 else "reject")
                decisions.append({"task_id": prob["task_id"], "correct": ok, "decision": dec, "confidence": conf})
            
            total = len(decisions)
            ca = sum(1 for d in decisions if d["decision"] == "accept" and d["correct"])
            ia = sum(1 for d in decisions if d["decision"] == "accept" and not d["correct"])
            cr = sum(1 for d in decisions if d["decision"] != "accept" and not d["correct"])
            ir = sum(1 for d in decisions if d["decision"] != "accept" and d["correct"])
            
            conditions[cname] = {
                "total": total, "acceptance_rate": sum(1 for d in decisions if d["decision"]=="accept")/total,
                "correct_rate": sum(1 for d in decisions if d["correct"])/total,
                "overtrust_rate": ia/total, "undertrust_rate": ir/total,
                "decision_accuracy": (ca+cr)/total, "decisions": decisions
            }
            print(f"    Decision accuracy: {(ca+cr)/total:.3f}, Overtrust: {ia/total:.3f}")
        
        del base_m; torch.cuda.empty_cache(); gc.collect()
        
        # SFT model condition
        print("\n  Loading SFT model for calibrated condition...", flush=True)
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
        if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
        sft_base = AutoModelForCausalLM.from_pretrained(BASE_MODEL, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
        sft_m = PeftModel.from_pretrained(sft_base, SFT_MODEL)
        sft_m.eval()
        
        print(f"\n  Condition: calibrated_sft", flush=True)
        decisions = []
        for idx, prob in enumerate(problems):
            if idx % 10 == 0: print(f"    [{idx}/{len(problems)}]", flush=True)
            
            pi = fmt(tokenizer, [{"role": "system", "content": "Before solving, state your confidence:\n- 'I am confident this solution is correct' for high confidence\n- 'This should work for most cases, but please verify edge cases' for medium\n- 'I am not confident in this solution, it may contain bugs' for low\nThen solve."},
                                 {"role": "user", "content": f"State confidence and complete:\n\n{prob['prompt']}"}])
            resp = gen(sft_m, tokenizer, pi, 1, 0.1)[0]
            code = extract_code(resp)
            fc = code if prob["prompt"] in code else prob["prompt"] + code
            tc = prob["test"] + f"\ncheck({prob['entry_point']})"
            ok = _run_code(fc + "\n" + tc)
            conf = extract_conf(resp, trained=True)
            
            score = 0.5
            if len(code.strip().split('\n')) < 2: score -= 0.15
            if 'try:' in code: score += 0.05
            if conf >= 0.8: score += 0.15
            elif conf < 0.5: score -= 0.2
            
            dec = "accept" if score >= 0.55 else ("modify" if score >= 0.35 else "reject")
            decisions.append({"task_id": prob["task_id"], "correct": ok, "decision": dec, "confidence": conf})
        
        total = len(decisions)
        ca = sum(1 for d in decisions if d["decision"] == "accept" and d["correct"])
        ia = sum(1 for d in decisions if d["decision"] == "accept" and not d["correct"])
        cr = sum(1 for d in decisions if d["decision"] != "accept" and not d["correct"])
        ir = sum(1 for d in decisions if d["decision"] != "accept" and d["correct"])
        
        conditions["calibrated_sft"] = {
            "total": total, "acceptance_rate": sum(1 for d in decisions if d["decision"]=="accept")/total,
            "correct_rate": sum(1 for d in decisions if d["correct"])/total,
            "overtrust_rate": ia/total, "undertrust_rate": ir/total,
            "decision_accuracy": (ca+cr)/total, "decisions": decisions
        }
        print(f"    Decision accuracy: {(ca+cr)/total:.3f}, Overtrust: {ia/total:.3f}")
        
        del sft_m, sft_base; torch.cuda.empty_cache(); gc.collect()
        
        with open(trust_path, 'w') as f: json.dump(conditions, f, indent=2)
        
        print("\n  TRUST STUDY SUMMARY:")
        for name, r in conditions.items():
            print(f"    {name}: DecAcc={r['decision_accuracy']:.3f}, Overtrust={r['overtrust_rate']:.3f}")
    else:
        print("Trust study already done, skipping.")
    
    print("\n=== ALL DONE ===")
