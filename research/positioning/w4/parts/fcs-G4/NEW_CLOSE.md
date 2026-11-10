# NEW_CLOSE: CLOSE citers not in the vault (fcs-G4)

Retrieval date 2026-11-10. Vault check: `grep -ril` on arXiv id and distinctive title words over research/notes. All verdicts are title and abstract level (ABSTRACT-ONLY); none were fetched in full text. 2603.25112 and 2603.14893 are seeds and are excluded as already known.

## Absent from the vault

| arXiv id or DOI | Title | Year | Cites seed | Candidate and component | Reason |
|---|---|---|---|---|---|
| 10.1145/3832783.3837465 | Harnessing Uncertainty in Code Language Models: Lessons from Vulnerability Detection | 2026 | 2505.14489 | L1.1/2 | uncertainty methods across 8 code LMs; vulnerability detection, not execution labels (abstract only) |
| 2604.06389 | SELFDOUBT: Uncertainty Quantification for Reasoning LLMs via the Hedge-to-Verify Ratio | 2026 | 2505.14489 | L2.9 | reasoning-trace hedging signals vs verbalized confidence |
| 2604.17707 | Before You Interpret the Profile: Validity Scaling for LLM Metacognitive Self-Report | 2026 | 2603.25112, 2603.14893 | F.1 | validity scaling for metacognitive self-report |
| 2604.22215 | Verbal Confidence Saturation in 3-9B Open-Weight Instruction-Tuned LLMs: A Pre-Registered Psychometric Validity Screen | 2026 | 2603.25052, 2604.01457, 2603.25112, 2603.14893 | F.1 | psychometric validity screen of verbal confidence (numeric vs categorical) |
| 2604.22271 | How LLMs Detect and Correct Their Own Errors: The Role of Internal Confidence Signals | 2026 | 2505.14489 | L2 | internal confidence signals vs error detection |
| 2604.24070 | Distilling Self-Consistency into Verbal Confidence: A Pre-Registered Negative Result and Post-Hoc Rescue on Gemma 3 4B | 2026 | 2603.25052, 2604.01457 | L2.11/F | gap between internal information and verbal readout; Type-2 AUROC, validity |
| 2605.03838 | TRACE: A Metrologically-Grounded Engineering Framework for Trustworthy Agentic AI Systems in Operationally Critical Domains | 2026 | 2504.03359 | F.1 | GUM/VIM/ISO 17025 metrology vocabulary for agentic AI trust metrics (not confidence elicitation; abstract only) |
| 2605.06673 | Domain-level metacognitive monitoring in frontier LLMs: A 33-model atlas | 2026 | 2603.25052, 2603.25112, 2603.14893 | F.4 | Type-2 AUROC per domain across 33 models |
| 2606.03969 | Quantifying Faithful Confidence Expression in Large Reasoning Models | 2026 | 2505.14489, 2604.01457 | L2/F | faithful calibration, intrinsic vs expressed confidence in reasoning models |
| 2606.30814 | When Calibration Rankings Reverse: Accuracy-Controlled Evaluation for Fair Comparison of LLMs | 2026 | 2505.14489 | L1.5/F | calibration rankings confounded by accuracy, ranking reversals |
| 2609.34454 | When Words Fall Short: Iterative Synergy Between Verbalized Reasoning and Hidden Features for LLM Confidence Estimation | 2026 | 2505.14489 | L2.1 | estimator (probe-like) beats verbalized confidence; QA/reasoning, no code |
| 2610.22046 | Effectiveness of Hidden-State Probes for Localizing Reasoning Failures | 2026 | 2605.09502, 2604.01457 | L2/L4 | hidden-state probes for failure type and failing step in reasoning models |
| 2610.34994 | Why Are LLMs Confidently Wrong? Correcting Overconfident Errors via Causal Head Intervention | 2026 | 2604.01457 | L2.12 | causal head intervention on confidence |
| 2610.35694 | Not One Belief: Answer Payloads, Persistence, and Dissociated Confidence Signals in Conversational Question Answering | 2026 | 2603.25052 | L2.1 | verbalized, likelihood, frozen probe, P(True) on same transcripts |

## Mentioned in other vault notes only (no dedicated note)

| arXiv id | Title | Year | Cites seed | Candidate and component | Reason |
|---|---|---|---|---|---|
| 2504.06564 | Thinking Out Loud: Do Reasoning Models Know When They're Right? | 2025 | 2505.14489 | L2.4/9 | distillation of reasoning traces and verbalized confidence |
| 2507.16806 | Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty | 2025 | 2505.14489 | L2.11 | RL with proper-scoring reward for uncertainty |
| 2510.10409 | Trace Length is a Simple Uncertainty Signal in Reasoning Models | 2025 | 2505.14489 | L2.9 | trace length vs verbalized confidence in reasoning models |
| 2511.04869 | Trained on Tokens, Calibrated on Concepts: The Emergence of Semantic Calibration in LLMs | 2025 | 2505.14489 | L2.4/8 | base vs instruct semantic calibration |
| 2603.17839 | How do LLMs Compute Verbal Confidence | 2026 | 2603.25052, 2505.14489 | L2/F | how verbal confidence is computed internally; reasoning vs non-reasoning |
| 2606.09876 | Calibrating Overconfidence Without Sacrificing Confidence: Probe-Conditioned Head Intervention for LLMs | 2026 | 2603.25052, 2604.01457 | L2.12 | probe-conditioned head intervention on stated confidence |
| 2606.27679 | From Signals to Transfer: A Factorised Study of Probe-Based Uncertainty Estimation in Large Language Models | 2026 | 2505.14489 | L2.5/6 | factorised probe-based UE incl. transfer under shift |
| 2606.29490 | Reported Confidence in LLMs Tracks Commitment More Than Correctness | 2026 | 2505.14489 | L2/F | verbal confidence tracks commitment, not correctness; formats varied |
