# L4 screening selection

Candidate L4: per-requirement or per-test-group confidence, localization, targeted repair versus regeneration, self-written test adequacy. Occupancy questions Q1 to Q4 are from R1 section 2 (L4). Source: `candidates-L4.tsv`, screened on title and abstract only. Blank cells mean the TSV has no such identifier.

## 1. Selection

| rank | rating | arXiv id | DOI | OpenReview id | year | title | Q | reason |
|---|---|---|---|---|---|---|---|---|
| 1 | CLOSE | 2512.24560 | https://doi.org/10.48550/arxiv.2512.24560 | | 2025 | Localized Calibrated Uncertainty in Code Language Models | Q4, Q1, Q2 | Localizes where generations misalign with intent via minimal repairing patches and calibrated uncertainty; direct line-level occupant. |
| 2 | CLOSE | 2606.03852 | https://doi.org/10.48550/arxiv.2606.03852 | | 2026 | FLARE: Fine-Grained Diagnostic Feedback for LLM Code Refinement | Q4, Q2 | Diagnostic model tells where to fix the bug in iterative refinement; named seed lead, localization and targeted repair. |
| 3 | CLOSE | 2604.06723 | https://doi.org/10.48550/arxiv.2604.06723 | | 2026 | Fine-grained Approaches for Confidence Calibration of LLMs in Automated Code Revision | Q4 | Fine-grained (per-edit) calibration for code revision; likely the per-edit Platt lead. |
| 4 | CLOSE | 2511.18001 | | | 2025 | Enhancing Automated Program Repair via Faulty Token Localization and Quality-Aware Patch Refinement | Q4, Q2 | Uses internal token signals to find likely-wrong code parts and guide patch refinement. |
| 5 | CLOSE | 2607.05188 | https://doi.org/10.48550/arxiv.2607.05188 | | 2026 | Latent Programming Horizons in Coding Agents | Q4 | Step-level probes decode tests-pass and regression signals; named seed lead. |
| 6 | CLOSE | 2302.07248 | https://doi.org/10.1145/3702320 | | 2024 | Generation Probabilities Are Not Enough: Uncertainty Highlighting in AI Code Completions | Q4 | Token-level uncertainty highlighting of generated code to localize edits; user-facing localization evidence. |
| 7 | CLOSE | 2606.09577 | https://doi.org/10.48550/arxiv.2606.09577 | | 2026 | Code Is More Than Text: Uncertainty Estimation for Code Generation | Q4, Q1 | Code-specific UE; abstract (400 chars) cannot rule out sub-solution granularity, so fetch. |
| 8 | CLOSE | 2604.03922 | https://doi.org/10.48550/arxiv.2604.03922 | | 2026 | ACES: Who Tests the Tests? Leave-One-Out AUC Consistency for Code Generation | Q3 | Models reliability of LLM-generated tests against code correctness; relates test adequacy to correctness. |
| 9 | RELATED | 2402.02047 | https://doi.org/10.1109/icse55347.2025.00040 | VDZkSSpa_b | 2025 | Calibration and Correctness of Language Models for Code | Q4 | Foundation for code calibration; check for line-level or sub-solution calibration. |
| 10 | RELATED | 2609.13975 | https://doi.org/10.48550/arxiv.2609.13975 | | 2026 | Introspective Uncertainty Estimation for LLM-Based Code Generation | Q4 | Hidden-state UE for response-level correctness; comparison side of granularity residual. |
| 11 | RELATED | 2512.08810 | https://doi.org/10.48550/arxiv.2512.08810 | | 2025 | Multicalibration for LLM-based Code Generation | Q1 | Calibration conditioned on problem factors (complexity, length); subgroup comparison side. |
| 12 | RELATED | 2605.12201 | https://doi.org/10.48550/arxiv.2605.12201 | | 2026 | Uncertainty Quantification for LLM-based Code Generation | Q4 | Prediction sets for code beyond PAC sets; structured-output comparison side. |
| 13 | RELATED | 2610.11300 | https://doi.org/10.48550/arxiv.2610.11300 | | 2026 | Characterizing Overconfident Failure in LLM-Based Code Generation | Q1 | Execution-graded overconfidence on code; response-level baseline. |
| 14 | RELATED | 2306.09896 | https://doi.org/10.48550/arxiv.2306.09896 | | 2023 | Is Self-Repair a Silver Bullet for Code Generation? | Q2 | Compares self-repair with resampling; the repair-versus-regeneration baseline. |
| 15 | RELATED | 2410.01215 | https://doi.org/10.1145/3744916.3773255 | | 2026 | From Code to Correctness: Closing the Last Mile of Code Generation with Hierarchical Debugging | Q2, Q4 | Debugging at multiple granularities; targeted repair baseline. |
| 16 | RELATED | 2509.24507 | | | 2025 | SemGuard: Real-Time Semantic Evaluator for Correcting LLM-Generated Code | Q4, Q2 | In-generation semantic error detection and correction; possible sub-solution localization. |
| 17 | RELATED | 2505.07768 | https://doi.org/10.1109/icse55347.2025.00165 | | 2025 | Enhancing Code Generation via Bidirectional Comment-Level Mutual Grounding | Q2, Q4 | Comment-level grounding to help locate and fix errors; fine-granularity repair neighbor. |
| 18 | RELATED | 2607.05721 | https://doi.org/10.48550/arxiv.2607.05721 | | 2026 | SpanUQ: Span-Level Uncertainty Quantification for Large Language Model Generation | Q4 | General-NLP span-level UQ; comparison side of the localization residual. |
| 19 | RELATED | 2411.13343 | | | 2024 | Fact-Level Confidence Calibration and Self-Correction | Q4, Q2 | General-NLP sub-response confidence plus self-correction; closest NLP analogue to per-requirement confidence. |
| 20 | RELATED | 2403.04696 | https://doi.org/10.48550/arxiv.2403.04696 | | 2024 | Fact-Checking the Output of Large Language Models via Token-Level Uncertainty Quantification | Q4 | Token-level claim localization in NLP; comparison side. |
| 21 | RELATED | 2607.03870 | | | 2026 | Evaluating LLM Uncertainty in Long-Form Generation Using Deterministic Ground Truth | Q4 | Evaluates uncertainty at fine granularity against deterministic labels; evaluation-protocol neighbor. |
| 22 | RELATED | 2506.08980 | https://doi.org/10.1145/3808142 | | 2026 | AdaDec: A Uncertainty-Guided Lookahead Decoding Framework for LLM-Based Code Generation | Q4 | Token-level uncertainty in code decoding; token-level signal baseline. |
| 23 | RELATED | 2305.01210 | https://doi.org/10.52202/075280-0943 | | 2023 | Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation | Q3 | EvalPlus: test insufficiency in benchmarks; foundation for test adequacy. |
| 24 | RELATED | 2507.06920 | https://doi.org/10.52202/085713-4591 | | 2025 | Rethinking Verification for LLM Code Generation: From Generation to Testing | Q3 | Test-suite homogeneity and LLM-generated test quality. |
| 25 | RELATED | 2404.10100 | https://doi.org/10.1109/tse.2024.3428972 | | 2024 | LLM-Based Test-Driven Interactive Code Generation: User Study and Empirical Evaluation | Q1, Q3 | TiCoder: tests to clarify intent; test-as-requirement neighbor. |
| 26 | RELATED | 2610.32548 | https://doi.org/10.48550/arxiv.2610.32548 | | 2026 | Beyond Coverage and Mutation: A Blind-Spot Analysis of LLM-Generated Unit Tests | Q3 | Obligation-based adequacy of LLM-written tests; adequacy measure. |
| 27 | RELATED | 2605.23491 | | | 2026 | CoSPlay: Cooperative Self-Play at Test-Time with Self-Generated Code and Unit Test | Q3 | Self-generated tests as verification signal; self-written test use. |
| 28 | RELATED | 2601.03525 | https://doi.org/10.18653/2026.findings-emnlp.1964 | | 2026 | Beyond Binary: Turning Partial Success into Dense Verifiable Rewards for Reinforcement Learning in Code Generation | Q1 | Test-case-level outcomes as dense signal; per-test-group baseline. |
| 29 | RELATED | 2512.15000 | https://doi.org/10.48550/arxiv.2512.15000 | | 2025 | DreamPRM-Code: Function-as-Step Process Reward Model with Label Correction for LLM Coding | Q4 | Process reward model for code at function level; PRM seed lead. |
| 30 | RELATED | 2610.21514 | | | 2026 | Poison Valleys: Diagnosing Path-Dependent Failure in LLM Code Repair | Q1, Q2 | Traces which software obligation failed in repair; per-obligation diagnosis. |

Not selected for lack of slots but worth a second look if a slot frees: 2601.22249 (FunPRM, same PRM seed lead as rank 29), 2607.06503 (probe cascade for agent early abort), 2603.15921 (fault-targeted test generation and repair), CodePRM (Findings of ACL 2025, no arXiv id in TSV, DOI https://doi.org/10.18653/v1/2025.findings-acl.428).

## 2. MISSING LEADS

Seed leads named in R1 or L2_OCCUPANT.md that do not appear in the TSV (search by title words only; no identifiers asserted):

1. Huang et al., line-level internal-state risk for code (cited by Ribeiro et al. 2026): search "line-level" "internal states" "code" "risk" LLM code generation.
2. Bui et al., code-correctness probing: search "Bui" "probing" "code correctness" language model hidden states.
3. Vu et al., code-correctness probing: search "Vu" "probing" "code" "correctness" internal representations.
4. Self-debugging with execution feedback: search "Teaching Large Language Models to Self-Debug".
5. Per-edit Platt recalibration in SE venues (if 2604.06723 is not it): search "Platt scaling" "code edit" "confidence" calibration.
6. Process reward models for code, main-line works: search "process reward model" "code generation" "line-level" OR "step-level" test-time scaling.

## 3. Counts

Rows screened: 277 (rows 2 to 278 of the TSV, header excluded); CLOSE: 8; RELATED: 22; rejected: 247.
