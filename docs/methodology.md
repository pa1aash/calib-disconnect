# Methodology: Calibrated Confidence Training for Code LLMs

## Research Question & Hypothesis
- **Question**: Can we train code LLMs to produce well-calibrated verbal confidence that correlates with actual code correctness?
- **Hypothesis**: DPO training on confidence-annotated code pairs (where preferred responses have accurate verbal confidence) will reduce ECE while maintaining code quality.
- **Success criteria**: ≥5% absolute ECE reduction; pass@1 within 2% of base model.

## Models
- **Base model**: DeepSeek-Coder-V2-Lite-Instruct (16B) — strong open-source code model, fits in GH200 VRAM
- **Comparison**: CodeLlama-13B-Instruct, Qwen2.5-Coder-7B-Instruct
- All models run in bf16 on GH200 (98GB VRAM)

## Experimental Pipeline

### Experiment 1: Baseline Calibration Measurement
**Goal**: Measure how poorly calibrated existing code LLMs are.
- Run each model on HumanEval (164 problems) and MBPP (500 problems)
- For each problem, generate 20 samples (temperature=0.8)
- Extract confidence via three methods:
  1. **Logit-based**: Mean token-level probability of generated code
  2. **Sampling-based**: pass@k consistency (fraction of 20 samples that pass)
  3. **Verbalized**: Ask model to rate confidence on 1-5 scale before generating code
- Compute ECE (Expected Calibration Error) with 10 bins for each method
- Also compute: Brier score, AUROC (confidence → correctness classification)

### Experiment 2: Confidence-Aware DPO Training
**Goal**: Train the model to produce calibrated verbal confidence.

**Data Generation Pipeline** (automatic, no human annotation):
1. Take coding problems from a training set (APPS, CodeContests subset)
2. For each problem, generate 20 solutions with base model
3. Execute each solution against test cases → binary correctness
4. Compute empirical difficulty (fraction of correct solutions)
5. Create preference pairs:
   - **Chosen**: Solution with verbal confidence matching empirical difficulty
     - If most solutions correct → "I'm confident this solution is correct"
     - If ~half correct → "This approach should work but please verify edge cases"
     - If few correct → "I'm unsure about this solution — it may have bugs, please review carefully"
   - **Rejected**: Solution with miscalibrated confidence
     - Overconfident on hard problems (confident + wrong)
     - Underconfident on easy problems (uncertain + correct)
6. ~5000 preference pairs for DPO training

**DPO Training**:
- Base: DeepSeek-Coder-V2-Lite-Instruct (16B) with LoRA (r=16, alpha=32)
- Learning rate: 5e-7, beta: 0.1, batch size: 4, gradient accumulation: 4
- 3 epochs over the preference dataset
- ~2 hours on GH200

### Experiment 3: Post-Training Calibration Evaluation
**Goal**: Measure calibration improvement after DPO.
- Same evaluation as Experiment 1, but on the DPO-trained model
- Compare ECE, Brier score, AUROC before/after training
- Ablation: DPO vs. SFT-only (just fine-tune on chosen responses)
- Measure code quality: pass@1 and pass@10 to verify no degradation

### Experiment 4: Simulated Trust Calibration Study
**Goal**: Show downstream benefit for human-agent collaboration.
- Create 50 coding scenarios with known correct/incorrect solutions
- For each scenario, present solution + confidence signal (or no signal) to GPT-4 as a simulated developer
- Simulated developer decides: accept, modify, or reject
- Measure:
  - Acceptance rate for correct code (should be high with calibrated confidence)
  - Rejection rate for incorrect code (should be high with calibrated confidence)
  - Overall decision accuracy
- Compare: no confidence vs. uncalibrated confidence vs. calibrated (our method)

## Controls & Validation
- **Positive control**: Perfect oracle confidence (100% when correct, 0% when wrong) — upper bound
- **Negative control**: Random confidence — lower bound
- **Validation**: Hold out 20% of HumanEval for calibration measurement (no overlap with training)
- **Statistical tests**: Paired t-test for ECE comparison, bootstrap CI for all metrics

## Compute Requirements
- **Platform**: Your GH200 GPU ([REDACTED-IP])
- **GPU**: NVIDIA GH200 480GB (98GB VRAM)
- **Estimated time**: 
  - Exp 1 (baseline): ~2 hours (generating 20 samples × 664 problems × 3 models)
  - Exp 2 (DPO training): ~3 hours (data gen + training)
  - Exp 3 (evaluation): ~1 hour
  - Exp 4 (simulated study): ~30 min
  - Total: ~7 hours
- **Cost**: $0 (your own GPU)

## Limitations
- Simulated user study (GPT-4 as proxy) — not real developers
- Limited to Python code generation benchmarks
- LoRA, not full fine-tuning
