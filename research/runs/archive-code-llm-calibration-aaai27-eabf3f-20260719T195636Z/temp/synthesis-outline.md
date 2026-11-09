# Synthesis outline

## Executive summary
The committed answer first: write the structured per-test/per-requirement self-expressed confidence
paper for code, as a risk-stratified three-tier method; headline = per-test failure-localization
AUROC ~0.75-0.85 (no incumbent); guaranteed floor + DCPO-positioned scalar underneath; single-GPU
LoRA feasible; AAAI-27 primary topic ML: Bayesian Learning & UQ; flag the ~10-day AAAI-27 clock and
the ICLR-27 pivot.

## 1. The Research Frontier in Code-LLM Confidence and Calibration
The two-channel split: internal/execution confidence for code is near-perfect (0.987) and now
consensus; the expressed channel fails. The open frontier is COMMUNICATION.

## 2. Caveats, Holes, and Open Problems at the Frontier
Expressed confidence for code unoccupied except DCPO scalar; metric fragility (ECE) + contamination
(→LiveCodeBench); the structured/per-test cell is empty; every train-time method is QA/math.

## 3. Where the Current Calibration-Disconnect Paper Falls Short of Main-Track
Diagnostic/negative, single benchmark, its one intervention (SFT) is a documented collapse; needs a
prescriptive methodological turn to clear main-track novelty.

## 4. Candidate Directions, Scored on Novelty and Confidence
Scored table: structured-per-test (novelty high) vs scalar (occupied by DCPO) vs complexity-routing
(secondary) vs selective-utility (safe floor); the composed three-tier paper wins both axes.

## 5. The One Paper: Committed Recommendation
The structured per-test self-expressed confidence method; decoupled masked-gradient LoRA + bounded
Brier vs continuous per-test targets; risk-stratified three tiers.

## 6. Headline Claim and the Exact Experiment That Produces It
Per-test AUROC ~0.75-0.85 (pilot-set) localizing which requirement fails; scalar replication vs DCPO;
risk-coverage utility. The concrete training + eval protocol.

## 7. Why the Headline Will Likely Land: Feasibility on Single-GPU 7B Compute
Three proven ingredients (verbalized-RL 0.85-0.86 QA; DCPO scalar code; CURE 0.667 on noisier oracle
→ execution oracle should exceed); free labels; ~15-75 GPU-hrs; single A100/GH200.

## 8. Supporting Results, Failure Mode, and Pre-Registered Fallback
Ablations (joint-vs-decoupled, continuous-vs-tiered); pre-registered fallback (if per-test AUROC<~0.70
→ floor 70-90% coverage @ ≤2-5% err + scalar); the de-scope ladder + Day-2/3 gate + 10-day calendar
+ AAAI-vs-ICLR pivot.

## 9. Novelty Defense Against the Closest Prior Work
The four-axis wedge; distinguish DCPO/FLARE/CURE/Atomic/Gros&Devanbu/VeRPO; HONEST scoop caveat
(UT-Dallas under-review) + contemporaneous-work norms.

## 10. AAAI-27 Topic Alignment: Primary and Secondary Keywords
Primary: ML: Bayesian Learning & Uncertainty Quantification. Secondary: NLP: Code Generation /
Program Synthesis; ML: Evaluation, Benchmarking, Datasets & Analysis. Method=primary, code=secondary;
7pg format + reproducibility checklist; timeline box.

## 11. The Shortlist: 5-10 Load-Bearing Papers
DCPO, Rewarding Doubt, ConfTuner/RLCR, CURE, FLARE, Gros&Devanbu, Spiess, DCPO-vs-RLCM, Sharma&David
— each with one-line contribution + the hole it leaves that this paper fills.

## Sources
Inline [N] + deduplicated Sources list with titles + URLs.
