# Evidence digest — code-llm-calibration-aaai27-eabf3f

High-fidelity index of load-bearing numbers with sources. Drafters: cite these; also read
interim notes, comparisons.md, source-tensions.json for full argument.

### The current paper's own results (grounding — [disconnect-paper-grounding], v3 manuscript)
- Sampling confidence (n=10 pass rate), independent labels: **ECE 0.059, AUROC 0.987** on HumanEval (164). Oracle upper bound the expressed signal targets.
- Log-prob: ECE 0.058 but **AUROC 0.668**; post-hoc isotonic → AUROC 0.587; Platt → 0.386 (ECE improves, AUROC DEGRADES → discrimination failure is fundamental).
- Verbal self-assessment: AUROC **0.519 (τ=0.8) / 0.564 (τ=0.1)**; 67% of problems at max confidence.
- AST proxy: AUROC 0.689, ECE 0.351.
- SFT (274 ex, LoRA r16): verbal ECE −64% BUT mean confidence **0.900 on BOTH easy and hard** subsets → "calibration without discrimination," distribution collapses to one bin.
- Models: Qwen2.5-Coder-7B-Instruct, DeepSeek-Coder-6.7B-Instruct.

### CONSENSUS (assert without hedging)
- Sampling/execution confidence works for code (AUROC ~0.80-0.99): [functional-entropy] 0.87, [fase] 0.74-0.91, [self-improving-consenf] 0.804, [disconnect] 0.987. → NOT a novel headline.
- Log-prob poor for code correctness; post-hoc fixes ECE not discrimination: [spiess], [sharma-david], [multicalibration-for-code].
- Every train-time verbalized-calibration method is QA/math, NOT code: [rewarding-doubt], [beyond-binary-rewards], [conftuner], [lacie], [sayself], [conqord], [uncertainty-distillation], [orce], [jang]. → the gap.

### DCPO — the scalar competitor to beat/position against ([decoupling-reasoning-and-confidence-...], ICML 2026, arXiv 2603.09117)
- Decoded `<conf>` block trained vs hybrid instance+group execution-pass-rate target; **AUROC LCB-v5 0.796, LCB-v6 0.845, HE+ 0.914** (Qwen3-8B), beats joint-reward RLCR on AUROC AND accuracy.
- Prop 4.2: formal gradient-conflict proof for joint accuracy+confidence objectives (names our SFT-collapse mechanism). Ablation: removing instance-level labels degrades ECE 0.128→0.209.
- Full fine-tune, 8×A100 (NOT single-GPU/LoRA).

### Train-time calibration mechanism works + is single-GPU feasible (P2 support)
- [rewarding-doubt] Rewarding Doubt: log-score RL, **Llama-3-8B 4-bit LoRA, single A40**, TriviaQA **AUROC 0.859**, more discriminative than a trained probe. QA only.
- [jang] Verbalized-Confidence-Triggers-Self-Verification: SFT on self-consistency scalar, GSM8K AUROC **50.57→81.25**, single model.
- [conftuner] ConfTuner: provably-proper tokenized Brier, ZERO extra sampling for labels, 7-8B, +14.4% AUROC. QA.
- [beyond-binary-rewards] RLCR: bounded proper scoring rule ⇒ provably accurate+calibrated; BUT unbounded log-score reward-hacks into abstention-collapse (Toy-Arm) → boundedness required.
- [capo] CAPO: discrimination-first (AUC) surrogate; "a predictor assigning identical confidence to correct & incorrect perfectly satisfies calibration yet fails to distinguish them" (≈ our collapse). Single-GPU-class.
- [balancing-classification-...260113284] LoRA r16 decoupled (final-token), **4×A100-40GB, ~500 GPU-hrs / 3 models** → single-GPU LoRA feasibility precedent.

### Novelty defense — the four closest works, each misses one axis (step 8 full-text verified)
- [flare] FLARE (2606.03852): execution + line-level BUT SEPARATE diagnostic model, no AUROC, no "calibrat" (grep-verified). DISTINCT.
- [think-through-uncertainty] CURE (2604.12046): self-report + per-claim + AUROC 0.667 + 3-stage anti-collapse pipeline BUT general long-form, NOISY VeriScore oracle, no code. PARTIAL-method/DISTINCT-domain.
- [atomic-calibration] Atomic Calibration (2410.13246): decompose+calibrate + AUROC BUT analysis/taxonomy (no training), NL-QA, zero "code/test/execution" (grep). PARTIAL-framing.
- Gros & Devanbu "Localized Calibrated Uncertainty in Code LMs" (2512.24560, Dec 2025): calibrated per-LINE/SPAN edit-probability via EXTERNAL probe. DISTINCT axes: spatial not functional; external not self-expressed.
- VeRPO (2601.03525): per-test partial success as CORRECTNESS reward, not confidence. DISTINCT.

### Robustness pillars (answer adversarial threats)
- ECE fragile: [roelofs] ECE_bin biased, equal-width worst; [kim&kang] prob-vs-verbal gap flips sign with conditioning → use AUROC-primary + debiased/adaptive ECE.
- Contamination: [riddell-2024]+[tracer-2026] HumanEval/MBPP surface+semantic contamination → primary eval on LiveCodeBench (time-windowed); [self-improving-consenf] replicates disconnect on LiveCodeBench.
- Mechanism for WHY verbal needs training: [miao&ungar] calibration & verbal-confidence directions ORTHOGONAL in activations, CoT contaminates verbal direction.

### Fallback floor (guaranteed secondary result)
- [cic-260704430] CIC Clopper-Pearson risk-controlled selective generation; QA coverage 0.52-1.00 @ α=0.10; INFEASIBLE @ α=0.05 on weak models (failure mode to pre-register).
- [codereefuser/task-abstention-260517029] 26.5pt precision, ~3.5x coverage vs perplexity.
- [sharma-david] symbolic-execution abstention: **77.8-88% coverage @ ≤0.02% FPR on LiveCodeBench** (ceiling to benchmark).

### Deployment motivation
- [in-ide-calibration-at-scale] 24M dev interactions: Platt post-hoc calibration does NOT align with developer acceptance; 153-dev study prefers CATEGORICAL over numeric signals.
- [copilot-zoominfo] 400+ devs, 33% acceptance, ZERO confidence signal exposed.

### Benchmark test-density (for dense per-test labels; LOW-confidence counts, verify)
- TACO ~50-200 tests/problem; CodeContests+ dense; LiveCodeBench ~17; HumanEval ~7.

### AAAI-27 scope + format ([aaai-27-areas-and-topics], [aaai-27-submission-instructions])
- Primary topic: **ML: Bayesian Learning & Uncertainty Quantification**. Secondary: NLP: Code Generation / Program Synthesis; ML: Evaluation, Benchmarking, Datasets & Analysis.
- 7pg main / 9 max; mandatory reproducibility checklist; deadlines abstract 2026-07-21, paper 2026-07-28, code 07-31; conf Feb 16-23 2027 Montreal.
