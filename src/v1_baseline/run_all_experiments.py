"""
Master experiment runner for DL4C paper.
Runs all 4 experiments sequentially with proper logging.
"""

import json
import os
import sys
import time

RESULTS_DIR = "/home/ubuntu/dl4c_experiments/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def run_with_logging(script_name, description):
    """Run a script and log timing."""
    print(f"\n{'='*70}")
    print(f"RUNNING: {description}")
    print(f"Script: {script_name}")
    print(f"{'='*70}")
    
    start = time.time()
    
    # Import and run
    import importlib.util
    spec = importlib.util.spec_from_file_location("module", f"/home/ubuntu/dl4c_experiments/{script_name}")
    module = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(module)
        elapsed = time.time() - start
        print(f"\n>>> {description} completed in {elapsed/60:.1f} minutes")
        return {"status": "success", "time_minutes": elapsed/60}
    except Exception as e:
        elapsed = time.time() - start
        print(f"\n>>> {description} FAILED after {elapsed/60:.1f} minutes: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "failed", "time_minutes": elapsed/60, "error": str(e)}


if __name__ == "__main__":
    overall_start = time.time()
    
    log = {}
    
    # Experiment 1: Baseline Calibration
    log["exp1"] = run_with_logging("exp1_baseline_calibration.py", "Experiment 1: Baseline Calibration Measurement")
    
    # Experiment 2: DPO Training
    log["exp2"] = run_with_logging("exp2_dpo_training.py", "Experiment 2: Confidence-Aware DPO Training")
    
    # Experiment 3: Post-Training Evaluation
    log["exp3"] = run_with_logging("exp3_post_training_eval.py", "Experiment 3: Post-Training Calibration Evaluation")
    
    # Experiment 4: Trust Study
    log["exp4"] = run_with_logging("exp4_trust_study.py", "Experiment 4: Simulated Trust Calibration Study")
    
    overall_time = (time.time() - overall_start) / 60
    log["total_time_minutes"] = overall_time
    
    with open(os.path.join(RESULTS_DIR, "experiment_log.json"), 'w') as f:
        json.dump(log, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"ALL EXPERIMENTS COMPLETE")
    print(f"Total time: {overall_time:.1f} minutes")
    print(f"{'='*70}")
    for exp, info in log.items():
        if isinstance(info, dict):
            print(f"  {exp}: {info.get('status', 'N/A')} ({info.get('time_minutes', 0):.1f} min)")
