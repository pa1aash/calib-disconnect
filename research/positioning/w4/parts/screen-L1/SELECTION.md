# L1 screening selection

Screened on title and abstract (first 400 characters only) from `candidates-L1.tsv`. Questions (Q) refer to L1 in `docs/s3/POSITIONING_BRIEF_R1.md` section 2. A dash means the TSV has no identifier.

## 1. Selected papers

| rank | rating | arXiv | DOI | OpenReview | year | title | Q | reason |
|---|---|---|---|---|---|---|---|---|
| 1 | CLOSE | 2512.07404 | https://doi.org/10.1145/3744916.3787846 | - | 2026 | On LLMs' Internal Representation of Code Correctness | 1, 2 | Hidden-state direction versus likelihood and verbal readouts on code; known occupant, check breadth and metrics |
| 2 | CLOSE | 2402.02047 | https://doi.org/10.1109/icse55347.2025.00040 | VDZkSSpa_b | 2025 | Calibration and Correctness of Language Models for Code | 1, 5, 6 | Code calibration with execution labels and recalibration; likely metric and rescaling coverage |
| 3 | CLOSE | - | https://doi.org/10.18653/2026.uncertainlp-main.21 | - | 2026 | Verbalized Uncertainty in Coding LLMs: A Contamination-Aware Study of Confidence Calibration | 1, 3, 4, 12, 13 | Six coding models, 365 LiveCodeBench problems, contamination-aware; direct hit on release-date control for calibration |
| 4 | CLOSE | 2609.13975 | https://doi.org/10.48550/arxiv.2609.13975 | - | 2026 | Introspective Uncertainty Estimation for LLM-Based Code Generation | 1, 2 | Hidden-state uncertainty versus correctness; thesis, may compare several families |
| 5 | CLOSE | 2608.14659 | https://doi.org/10.48550/arxiv.2608.14659 | - | 2026 | When Uncertainty Isn't Enough: An Empirical Study of Self-Correction in Code Generation | 1, 2 | Five uncertainty methods (token entropy, verbalized, P(True)) on code; multi-family comparison |
| 6 | CLOSE | 2606.09577 | https://doi.org/10.48550/arxiv.2606.09577 | - | 2026 | Code Is More Than Text: Uncertainty Estimation for Code Generation | 1, 2, 7 | Code-specific UE methods versus NL-inherited ones; possible multi-family benchmark |
| 7 | CLOSE | 2610.11300 | https://doi.org/10.48550/arxiv.2610.11300 | - | 2026 | Characterizing Overconfident Failure in LLM-Based Code Generation | 1, 5 | Model-derived uncertainty versus execution failure; overconfidence characterization |
| 8 | CLOSE | 2502.11620 | https://doi.org/10.48550/arxiv.2502.11620 | - | 2025 | Assessing Correctness in LLM-Based Code Generation via Uncertainty Estimation | 7, 8 | Semantic entropy and mutual information adapted to code with equivalence check |
| 9 | CLOSE | 2605.28500 | https://doi.org/10.18653/2026.emnlp-main.8 | - | 2026 | Functional Entropy: Predicting Functional Correctness in LLM-Generated Code with Uncertainty Quantification | 1, 7, 8 | Systematic UQ transfer to code; functional-equivalence entropy |
| 10 | CLOSE | 2605.09023 | https://doi.org/10.48550/arxiv.2605.09023 | - | 2026 | Using Semantic Distance to Estimate Uncertainty in LLM-Based Code Generation | 7, 8 | Compares sample-based estimator design choices for code |
| 11 | CLOSE | 2506.11021 | https://doi.org/10.48550/arxiv.2506.11021 | - | 2025 | Eliminating Hallucination-Induced Errors in LLM Code Generation with Functional Clustering | 7, 8 | Functional clustering on executed outputs giving a confidence score |
| 12 | CLOSE | 2604.06485 | https://doi.org/10.48550/arxiv.2604.06485 | - | 2026 | Inference-Time Code Selection via Symbolic Equivalence Partitioning | 7, 8 | Symbolic-equivalence agreement among samples without hidden tests |
| 13 | CLOSE | 2603.27098 | https://doi.org/10.48550/arxiv.2603.27098 | - | 2026 | Ensemble-Based Uncertainty Estimation for Code Correctness Estimation | 1, 7 | Consistency of semantics or execution behaviors across samples, no oracle |
| 14 | CLOSE | 2607.12273 | https://doi.org/10.1145/3832276 | - | 2026 | Code-MUE: Measuring Code LLMs' Uncertainty through Execution-Based Semantic Interaction Graphs | 7, 8 | Execution-based sample-agreement uncertainty for code |
| 15 | CLOSE | 2512.08810 | https://doi.org/10.48550/arxiv.2512.08810 | - | 2025 | Multicalibration for LLM-based Code Generation | 11 | Subgroup calibration (complexity, length, language) on code; Campos et al. lead |
| 16 | CLOSE | - | https://doi.org/10.18653/v1/2026.findings-acl.305 | - | 2026 | NeuroSym-Cal: Bridging the Reasoning-Execution Gap in Code Generation via Hierarchical Calibration | 1, 7 | Calibration for CoT code generation; critiques self-consistency, symbolic component |
| 17 | RELATED | 2602.07080 | - | - | 2026 | CodeCircuit: Toward Inferring LLM-Generated Code Correctness via Attribution Graphs | 1, 12 | White-box correctness readout against unit-test or judge approaches |
| 18 | RELATED | 2605.12201 | https://doi.org/10.48550/arxiv.2605.12201 | - | 2026 | Uncertainty Quantification for LLM-based Code Generation | 5, 6 | Conformal prediction sets for code; extends PAC sets, selective-risk side |
| 19 | RELATED | 2508.16131 | https://doi.org/10.1007/s10515-026-00683-0 | - | 2026 | The fools are certain; the wise are doubtful: Exploring LLM confidence in code completion | 1, 5 | Token-probability calibration for code completion |
| 20 | RELATED | 2609.12489 | https://doi.org/10.18653/2026.findings-emnlp.1715 | - | 2026 | Confidence-Gated Transductive Test Generation for Code Reranking | 7 | Model-written-test agreement used as confidence |
| 21 | RELATED | 2608.04439 | https://doi.org/10.48550/arxiv.2608.04439 | - | 2026 | ExeCRE: Execution-Consistency Guided Reliability Estimation for Self-Correcting Code Generation | 7 | Execution-consistency reliability without hidden tests |
| 22 | RELATED | 2411.08254 | https://doi.org/10.1109/tse.2026.3664287 | - | 2026 | Toward Automated Validation of Language Model Synthesized Test Cases Using Semantic Entropy | 8 | Semantic entropy applied to generated tests |
| 23 | RELATED | - | https://doi.org/10.18653/v1/2026.gem-main.55 | - | 2026 | Semantic vs. Structural Signals: Log-Probability and LLM-as-a-Judge for Reference-Free Code Evaluation | 12 | Judge score versus log-probability for code; label source unclear |
| 24 | RELATED | 2305.01210 | https://doi.org/10.52202/075280-0943 | - | 2023 | Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation | 9, 10 | EvalPlus augmented tests; foundation for test-insufficiency labels |
| 25 | RELATED | 2603.00520 | https://doi.org/10.48550/arxiv.2603.00520 | - | 2026 | SWE-ABS: Adversarial Benchmark Strengthening Exposes Inflated Success Rates on Test-based Benchmark | 10 | Weak test suites inflate success; accuracy side of Q10 |
| 26 | RELATED | 2404.04689 | https://doi.org/10.48550/arxiv.2404.04689 | - | 2024 | Multicalibration for Confidence Scoring in LLMs | 11 | General-NLP multicalibration baseline |
| 27 | RELATED | 2302.09664 | https://doi.org/10.48550/arxiv.2302.09664 | VD-AYtP0dve | 2023 | Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation | 8 | Semantic entropy origin; comparison side for code adaptation |
| 28 | RELATED | 2309.12236 | https://doi.org/10.3929/ethz-b-000714260 | - | 2023 | Smooth ECE: Principled Reliability Diagrams via Kernel Smoothing | 5 | Binning-free estimator and diagram foundation |
| 29 | RELATED | 2405.15709 | https://doi.org/10.52202/079017-2677 | - | 2024 | Information-theoretic Generalization Analysis for Expected Calibration Error | 5 | Bias of equal-width versus equal-mass binned ECE |
| 30 | RELATED | - | https://doi.org/10.5281/zenodo.22881716 | - | 2026 | Verbalized Uncertainty in Coding LLMs: A Contamination-Aware Confidence Calibration Dataset | 3, 13 | Data record of rank 3; confirms models, labels, and elicitation strategies |

## 2. MISSING LEADS

Seed leads from the brief not found in the TSV (no identifiers supplied):

1. Spiess et al., ICSE 2025, under the brief's title: search "Calibration of LLM Code Generation" (the TSV has rank 2 under a different title; confirm they are one work).
2. Campos et al., multicalibration for code: possibly rank 15; confirm authors from the fetched record.
3. AlphaCode clustering: search "Competition-Level Code Generation with AlphaCode".
4. Search "Teaching models to express their uncertainty in words" (lin2022teaching).
5. Search "PAC Prediction Sets for Large Language Models of Code".
6. Search "UQ4CT" (legacy references.bib lines 273-279).
7. Search "self-consistency distillation" (legacy references.bib lines 265-271).
8. Execution-based MBR and dual agreement: search "Natural Language to Code Translation with Execution" and "CodeT: Code Generation with Generated Tests".
9. Release-date benchmark: search "LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code".
10. 2025 to 2026 benchmarks or surveys of code-model calibration: no specific title in the brief; rerun the search facet.

## 3. Counts

Rows screened: 423; CLOSE: 16; RELATED: 14; rejected: 393.
