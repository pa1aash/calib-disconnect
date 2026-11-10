# L3 screening selection (verification utility)

Screened on title and abstract only (first 400 characters). Question numbers refer to the L3 list in section 2 of docs/s3/POSITIONING_BRIEF_R1.md. A blank cell means the TSV has no value.

| rank | rating | arXiv id | DOI | OpenReview id | year | title | questions | reason |
|---|---|---|---|---|---|---|---|---|
| 1 | CLOSE | 2608.14659 | https://doi.org/10.48550/arxiv.2608.14659 | | 2026 | When Uncertainty Isn't Enough: An Empirical Study of Self-Correction in Code Generation | 1, 2, 7 | Tests five uncertainty methods, including verbalized confidence, as triggers for selective self-correction in code. |
| 2 | CLOSE | 2611.06372 | https://doi.org/10.48550/arxiv.2611.06372 | | 2026 | Give Up to Get More: Priors, Not Policies, Govern Test-Time Compute Allocation | 1, 4 | Compares allocation rules with oracle gain on math, code, and proof samples. |
| 3 | CLOSE | 2610.30284 | https://doi.org/10.48550/arxiv.2610.30284 | | 2026 | SWE-VERIFIER: Selective Verification for Cost-Efficient Coding Agents | 1, 3, 4, 6 | Decides when to spend verification on coding-agent actions; may report cost against always-verify and random. |
| 4 | CLOSE | 2506.10056 | | | 2025 | Pareto Optimal Code Generation | 4 | Trades accuracy against verification compute for generate-then-rank code. |
| 5 | CLOSE | 2607.00053 | https://doi.org/10.48550/arxiv.2607.00053 | | 2026 | SWE-Router: Routing in Multi-turn Agentic Software Engineering Tasks | 1, 5, 6 | Routing for SWE agents, possibly with oracle comparison. |
| 6 | CLOSE | 2603.25764 | | | 2026 | Confident and Wrong: Silent Semantic Failures in Coding Agents | 3, 6, 7 | Trustworthiness versus completion in SWE-bench Verified trajectories. |
| 7 | CLOSE | 2605.17029 | https://doi.org/10.48550/arxiv.2605.17029 | | 2026 | Task Abstention for Large Language Models in Code Generation | 3 | Abstention for code generation, likely with risk-coverage style reporting. |
| 8 | CLOSE | 2605.19369 | | | 2026 | When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions | 3 | Correctness estimation plus abstention for code models. |
| 9 | CLOSE | 2505.13553 | https://doi.org/10.48550/arxiv.2505.13553 | | 2025 | Towards Functional Correctness of Code Models with Selective Generation | 3 | Selective generation with risk control for code. |
| 10 | CLOSE | 2502.11620 | https://doi.org/10.48550/arxiv.2502.11620 | | 2025 | Assessing Correctness in LLM-Based Code Generation via Uncertainty Estimation | 3 | Uncertainty as a correctness proxy for generated code; may report selective curves. |
| 11 | CLOSE | 2606.09577 | https://doi.org/10.48550/arxiv.2606.09577 | | 2026 | Code Is More Than Text: Uncertainty Estimation for Code Generation | 3 | Code-specific UE aimed at selective prediction and agentic decisions. |
| 12 | CLOSE | 2609.12489 | https://doi.org/10.18653/2026.findings-emnlp.1715 | | 2026 | Confidence-Gated Transductive Test Generation for Code Reranking | 4 | Confidence gates when expensive test generation is invoked. |
| 13 | CLOSE | 2606.31511 | https://doi.org/10.48550/arxiv.2606.31511 | | 2026 | Falsification, Not Exposure: An Internally Preregistered Placebo-Controlled Decomposition of Self-Repair Feedback in Frozen Small Code Models | 2, 7 | Separates the value of failing-test feedback from re-exposure in self-repair; the repair side of question 7. |
| 14 | RELATED | 2604.07036 | https://doi.org/10.48550/arxiv.2604.07036 | | 2026 | ReDAct: Uncertainty-Aware Deferral for LLM Agents | 5, 6 | Uncertainty-based deferral for agents; general-agent comparison side. |
| 15 | RELATED | 2605.26849 | https://doi.org/10.48550/arxiv.2605.26849 | | 2026 | Uncertainty-Aware Budget Allocation for Adaptive Test-Time Reasoning | 1, 4 | Uncertainty-driven sampling-budget allocation; reasoning, not code. |
| 16 | RELATED | 2602.07670 | | | 2026 | Surprisal-Guided Selection: Compute-Optimal Test-Time Strategies for Execution-Grounded Code Generation | 1, 4 | Compute-optimal selection with an execution evaluator; kernel-optimization domain. |
| 17 | RELATED | 2610.05170 | | | 2026 | Verification Trap: Understanding Test-Time Selection Failures under False Premises in Code Generation | 4, 7 | Verifier-visible evidence failure modes in code selection. |
| 18 | RELATED | 2412.19513 | https://doi.org/10.18653/v1/2025.acl-long.203 | | 2025 | Confidence v.s. Critique: A Decomposition of Self-Correction Capability for LLMs | 2, 7 | Confidence role in self-correction; general NLP baseline. |
| 19 | RELATED | 2306.09896 | https://doi.org/10.48550/arxiv.2306.09896 | | 2023 | Is Self-Repair a Silver Bullet for Code Generation? | 2, 7 | Seed lead; repair outcome with feedback, no confidence tracking expected. |
| 20 | RELATED | 2304.05128 | https://doi.org/10.48550/arxiv.2304.05128 | | 2023 | Teaching Large Language Models to Self-Debug | 2, 7 | Foundation for execution-feedback repair. |
| 21 | RELATED | 2512.01457 | https://doi.org/10.48550/arxiv.2512.01457 | | 2025 | Zero-Overhead Introspection for Adaptive Test-Time Compute | 1 | Introspective success prediction to set effort; general baseline. |
| 22 | RELATED | 2503.00031 | https://doi.org/10.48550/arxiv.2503.00031 | | 2025 | Efficient Test-Time Scaling via Self-Calibration | 1 | Confidence-driven sample allocation in general tasks. |
| 23 | RELATED | 2305.11860 | https://doi.org/10.18653/v1/2023.emnlp-main.761 | | 2023 | Let's Sample Step by Step: Adaptive-Consistency for Efficient Reasoning and Coding with LLMs | 1, 4 | Agreement-driven budget allocation including coding. |
| 24 | RELATED | 2410.10347 | https://doi.org/10.48550/arxiv.2410.10347 | | 2024 | A Unified Approach to Routing and Cascading for LLMs | 5 | Routing and cascade framework; oracle comparison baseline. |
| 25 | RELATED | 2502.09054 | https://doi.org/10.48550/arxiv.2502.09054 | | 2025 | Cost-Saving LLM Cascades with Early Abstention | 5 | Cascades with abstention; general baseline. |
| 26 | RELATED | 2208.02814 | https://doi.org/10.48550/arxiv.2208.02814 | | 2022 | Conformal Risk Control | 3 | Seed foundation for risk control in selective prediction. |
| 27 | RELATED | 2503.10512 | https://doi.org/10.48550/arxiv.2503.10512 | | 2025 | Conformal Prediction Sets for Deep Generative Models via Reduction to Conformal Regression | 3 | Prediction sets for sampled code with an admissibility function. |
| 28 | RELATED | 2611.02318 | https://doi.org/10.48550/arxiv.2611.02318 | | 2026 | A Capitulation Direction Emerges With Scale and Is Causally Load-Bearing Where Validation Is Strong | 7 | Belief revision under pushback; comparison side for update versus spurious feedback. |
| 29 | RELATED | 2607.12985 | https://doi.org/10.48550/arxiv.2607.12985 | | 2026 | Resist and Update: Counterfactual Report Coordinates for Incentive-Compatible LLMs | 7 | Separates updating on licensed evidence from caving to pressure. |
| 30 | RELATED | 2302.08468 | https://doi.org/10.48550/arxiv.2302.08468 | YzRqIr03Ih | 2023 | LEVER: Learning to Verify Language-to-Code Generation with Execution | 4 | Learned verifier using execution results; baseline for verifier value. |

## MISSING LEADS

Seed leads from the brief not found in the TSV (search title words):

1. "Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation" (Kuhn et al., 2023)
2. "Detecting hallucinations in large language models using semantic entropy" (Farquhar et al., Nature 2024)
3. "Self-Consistency Improves Chain of Thought Reasoning in Language Models"
4. "PAC Prediction Sets for Large Language Models of Code"
5. "conformal prediction abstention code generation" (A32, beyond PAC sets; no title known)
6. "selective prediction verifier routing coding agents" (search facet; no title known)

## COUNTS

Rows screened: 354; CLOSE: 13; RELATED: 17; rejected: 324.
