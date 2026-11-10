# CITING: forward-citation screen, fcs-G4

Retrieval date: 2026-11-10. Sources: Semantic Scholar Graph API (`/citations`, HTTP 200 on all 12 seeds, single page each, no `next`) and OpenAlex (`filter=cites:`). Raw JSON in `raw/` (`s2_<id>_0.json`, `oa_<id>_<page>.json`, `oa_seed_<id>.json`, `fetch_meta.json`, headers carry URL, date, HTTP status).

**Gap (OpenAlex).** OpenAlex returned HTTP 429 (shared free daily budget exhausted) for 2603.18893, 2610.18066, and 2504.03359 after the first nine seeds. No retry could succeed the same day, so their OpenAlex citer lists are not retrieved. For these, counts are Semantic Scholar only. Citer lists are therefore possibly incomplete (instrument gap, not a zero). Seed 2610.18066 shows 0 citers on Semantic Scholar; OpenAlex cited_by_count for it was 0 on the seed record; 2610.25846 shows 0 on both sources.

Tags: CLOSE = could make or partly make a candidate's core claim; RELATED = relevant, not core; UNRELATED. Tags rest on title plus abstract only (abstracts missing for some OpenAlex-only or DOI-only records; those are tagged by title). Bears-on codes are brief question numbers from POSITIONING_BRIEF_R1 section 2. In the vault column: `dedicated` means a note on the paper itself; `mention` means only cited inside another note; `absent` means no grep hit on id or distinctive title words.

## Count summary

| Seed | Title | S2 count | OpenAlex count | Merged distinct | Gap |
|---|---|---|---|---|---|
| 2603.25052 | Closing the Confidence-Faithfulness Gap in Large Language Models | 9 | 13 | 14 | none |
| 2607.08046 | What LLM Forecasters Know but Don't Say | 2 | 3 | 3 | none |
| 2605.09502 | Hidden Error Awareness in Chain-of-Thought Reasoning | 9 | 10 | 12 | none |
| 2607.13753 | Post-Training Shifts Confidence: A Three-Stage Analysis (SFT, RL, OPD) | 1 | 1 | 1 | none |
| 2505.14489 | Reasoning Models Better Express Their Confidence | 86 | 56 | 96 | none |
| 2604.01457 | Wired for Overconfidence | 8 | 8 | 11 | none |
| 2603.25112 | Do LLMs Know What They Know? Metacognitive Efficiency with SDT | 8 | 9 | 12 | none |
| 2603.14893 | LLMs as Signal Detectors | 8 | 11 | 12 | none |
| 2610.25846 | Measurement Validity and Representation Dynamics of Confidence Signals in LLMs | 0 | 0 | 0 | none (zero citers reported; may be new) |
| 2603.18893 | Don't Ask: What Numeric Self-Reports Measure in Language Models | 1 | not retrieved | 1 | OpenAlex 429 |
| 2610.18066 | Uncertainty Evaluation: Bridging Machine Learning and Measurement Science | 0 | not retrieved | 0 | OpenAlex 429; S2 zero |
| 2504.03359 | A metrological framework for uncertainty evaluation in ML classification models | 14 | not retrieved | 14 | OpenAlex 429 |

Note: OpenAlex counts are rows returned with the `select` filter; S2 counts are raw citation edges. Merge was by normalized title; a few DOI-only duplicates with differing titles (for example 2606.15610 appears twice) may remain, so merged counts are upper bounds by a small margin.


## Seed 2603.25052: Closing the Confidence-Faithfulness Gap in Large Language Models

| # | Year | Id | Title | Src | Tag | Bears on | Vault |
|---|---|---|---|---|---|---|---|
| 1 | 2026 | 2610.35694 | Not One Belief: Answer Payloads, Persistence, and Dissociated Confidence Signals in Conversational Question Answering | OA+S2 | CLOSE | L2.1: verbalized, likelihood, frozen probe, P(True) on same transcripts | absent |
| 2 | 2026 | 2606.09876 | Calibrating Overconfidence Without Sacrificing Confidence: Probe-Conditioned Head Intervention for LLMs | OA+S2 | CLOSE | L2.12: probe-conditioned head intervention on stated confidence | mention |
| 3 | 2026 | 2604.24070 | Distilling Self-Consistency into Verbal Confidence: A Pre-Registered Negative Result and Post-Hoc Rescue on Gemma 3 4B | OA+S2 | CLOSE | L2.11/F: gap between internal information and verbal readout; Type-2 AUROC, validity | absent |
| 4 | 2026 | 2605.06673 | Domain-level metacognitive monitoring in frontier LLMs: A 33-model atlas | OA+S2 | CLOSE | F.4: Type-2 AUROC per domain across 33 models | absent |
| 5 | 2026 | 2603.17839 | How do LLMs Compute Verbal Confidence | OA+S2 | CLOSE | L2/F: how verbal confidence is computed internally; reasoning vs non-reasoning | mention |
| 6 | 2026 | 2604.22215 | Verbal Confidence Saturation in 3-9B Open-Weight Instruction-Tuned LLMs: A Pre-Registered Psychometric Validity Screen | OA | CLOSE | F.1: psychometric validity screen of verbal confidence (numeric vs categorical) | absent |
| 7 | 2026 | 2608.06571 | Vision-Language Model Confidence Is Not a Property of the Answer | OA+S2 | RELATED | VLM confidence as non-property of answer | absent |
| 8 | 2026 | 2605.26045 | Confidence and Calibration of Activation Oracles for Reliable Interpretation of Language Model Internals | S2 | RELATED | calibration of activation oracles | absent |
| 9 | 2026 | 2605.09195 | The Geometry of Forgetting: Temporal Knowledge Drift as an Independent Axis in LLM Representations | OA+S2 | RELATED | internal representations vs outdated answers | absent |
| 10 | 2026 | 2604.23333 | Process Supervision of Confidence Margin for Calibrated LLM Reasoning | OA+S2 | RELATED | process supervision of confidence margin | absent |
| 11 | 2026 | 2607.00661 | Faithful by Definition: Emotion Analysis via Natural Semantic Metalanguage Explications | OA | UNRELATED |  |  |
| 12 | 2026 | 10.20944/preprints202604.0078.v1 | Knowing Before Speaking: In-Computation Metacognition Precedes Verbal Confidence in Large Language Models | OA | UNRELATED |  |  |
| 13 | 2026 | 2607.26845 | Thinking Under Uncertainty: Evidence Use and Information-Seeking in Language Models | OA | UNRELATED |  |  |
| 14 | 2026 | none | Towards LLM Reliability: A System Reliability Perspective | OA | UNRELATED |  |  |

## Seed 2607.08046: What LLM Forecasters Know but Don't Say

| # | Year | Id | Title | Src | Tag | Bears on | Vault |
|---|---|---|---|---|---|---|---|
| 1 | 2026 | 2609.22246 | The Corroboration Illusion: When More News Makes LLM Forecasts Less True | OA+S2 | UNRELATED |  |  |
| 2 | 2026 | 2608.23058 | LLM-based Agents for Forecasting and Prediction: Methods, Training, Evaluation, and Applications | OA+S2 | UNRELATED |  |  |
| 3 | 2026 | 10.21203/rs.3.rs-11603009/v1 | Over-Reading the News: How LLM Forecasters Over-Update on Headlines, and What Survives Correcting It | OA | UNRELATED |  |  |

## Seed 2605.09502: Hidden Error Awareness in Chain-of-Thought Reasoning

| # | Year | Id | Title | Src | Tag | Bears on | Vault |
|---|---|---|---|---|---|---|---|
| 1 | 2026 | 2610.22046 | Effectiveness of Hidden-State Probes for Localizing Reasoning Failures | OA+S2 | CLOSE | L2/L4: hidden-state probes for failure type and failing step in reasoning models | absent |
| 2 | 2026 | 2609.01106 | Hints Help But Do They Teach? Evaluating Skills Transfer in Code Generation | OA+S2 | RELATED | code generation, executable eval of hints | absent |
| 3 | 2026 | 2605.26045 | Confidence and Calibration of Activation Oracles for Reliable Interpretation of Language Model Internals | S2 | RELATED | calibration of activation oracles | absent |
| 4 | 2026 | 2611.02574 | RLVR Sharpens the Pencil, Not the Mind | OA+S2 | UNRELATED |  |  |
| 5 | 2026 | 2610.15412 | From Candidate Tokens to Final Outcomes: Decoding Relative Long-Horizon Candidate Value from Reasoning Model Representations | OA+S2 | UNRELATED |  |  |
| 6 | 2026 | 2609.34732 | What Visual Generators Need from Teachers: Rethinking Representation Alignment | OA+S2 | UNRELATED |  |  |
| 7 | 2026 | 2609.03436 | It's the Problem, Not the Path: Budget and Difficulty Confounds in LLM Reasoning Trajectories | OA+S2 | UNRELATED |  |  |
| 8 | 2026 | 2608.20670 | Why2Speak: Faithful Reasoning for Abstaining Action Policies | OA+S2 | UNRELATED |  |  |
| 9 | None | none | The Trace Is Not the State A Counterfactual Test of What Controls Multi-Digit Addition | S2 | UNRELATED |  |  |
| 10 | 2026 | 2609.39263 | Concept Subspaces Compute Beyond the Logit Lens: A Weights-Only Test for Locating Representations Upstream of Readout | OA | UNRELATED |  |  |
| 11 | 2026 | 2610.30882 | Inherited, Not Invented: Tracing the Provenance of Wait in Reasoning Models | OA | UNRELATED |  |  |
| 12 | 2026 | 10.18653/2026.emnlp-main.1846 | Contrastive Neuron Regulation for Chain-of-Thought Reasoning | OA | UNRELATED |  |  |

## Seed 2607.13753: Post-Training Shifts Confidence: A Three-Stage Analysis (SFT, RL, OPD)

| # | Year | Id | Title | Src | Tag | Bears on | Vault |
|---|---|---|---|---|---|---|---|
| 1 | 2026 | 2609.14636 | Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation | OA+S2 | UNRELATED |  |  |

## Seed 2505.14489: Reasoning Models Better Express Their Confidence

| # | Year | Id | Title | Src | Tag | Bears on | Vault |
|---|---|---|---|---|---|---|---|
| 1 | 2026 | 10.1145/3832783.3837465 | Harnessing Uncertainty in Code Language Models: Lessons from Vulnerability Detection | OA+S2 | CLOSE | L1.1/2: uncertainty methods across 8 code LMs; vulnerability detection, not execution labels (abstract only) | absent |
| 2 | 2026 | 2609.34454 | When Words Fall Short: Iterative Synergy Between Verbalized Reasoning and Hidden Features for LLM Confidence Estimation | S2 | CLOSE | L2.1: estimator (probe-like) beats verbalized confidence; QA/reasoning, no code | absent |
| 3 | 2026 | 2606.30814 | When Calibration Rankings Reverse: Accuracy-Controlled Evaluation for Fair Comparison of LLMs | OA+S2 | CLOSE | L1.5/F: calibration rankings confounded by accuracy, ranking reversals | absent |
| 4 | 2026 | 2606.27679 | From Signals to Transfer: A Factorised Study of Probe-Based Uncertainty Estimation in Large Language Models | S2 | CLOSE | L2.5/6: factorised probe-based UE incl. transfer under shift | mention |
| 5 | 2026 | 2606.03969 | Quantifying Faithful Confidence Expression in Large Reasoning Models | OA+S2 | CLOSE | L2/F: faithful calibration, intrinsic vs expressed confidence in reasoning models | absent |
| 6 | 2026 | 2605.27752 | Same Answer, Different Confidence: Protocol Sensitivity in LLM Confidence Calibration | S2 | CLOSE | L2.3: elicitation/protocol as a factor, verbal vs token confidence | dedicated |
| 7 | 2026 | 2604.22271 | How LLMs Detect and Correct Their Own Errors: The Role of Internal Confidence Signals | OA+S2 | CLOSE | L2: internal confidence signals vs error detection | absent |
| 8 | 2026 | 2604.06389 | SELFDOUBT: Uncertainty Quantification for Reasoning LLMs via the Hedge-to-Verify Ratio | OA+S2 | CLOSE | L2.9: reasoning-trace hedging signals vs verbalized confidence | absent |
| 9 | 2026 | 2603.17839 | How do LLMs Compute Verbal Confidence | OA+S2 | CLOSE | L2/F: how verbal confidence is computed internally; reasoning vs non-reasoning | mention |
| 10 | 2026 | 2603.09117 | Decoupling Reasoning and Confidence: Resurrecting Calibration in Reinforcement Learning from Verifiable Rewards | OA+S2 | CLOSE | L2.11: RLVR calibration degeneration and decoupled training | dedicated |
| 11 | 2025 | 2510.10409 | Trace Length is a Simple Uncertainty Signal in Reasoning Models | S2 | CLOSE | L2.9: trace length vs verbalized confidence in reasoning models | mention |
| 12 | 2025 | 2507.16806 | Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty | OA+S2 | CLOSE | L2.11: RL with proper-scoring reward for uncertainty | mention |
| 13 | 2025 | 2504.06564 | Thinking Out Loud: Do Reasoning Models Know When They're Right? | S2 | CLOSE | L2.4/9: distillation of reasoning traces and verbalized confidence | mention |
| 14 | 2025 | 2511.04869 | Trained on Tokens, Calibrated on Concepts: The Emergence of Semantic Calibration in LLMs | OA | CLOSE | L2.4/8: base vs instruct semantic calibration | mention |
| 15 | 2026 | 2606.29490 | Reported Confidence in LLMs Tracks Commitment More Than Correctness | OA | CLOSE | L2/F: verbal confidence tracks commitment, not correctness; formats varied | mention |
| 16 | 2026 | 2609.33290 | Calibration, Not Answer Selection: Distilling Internal Confidence in Reasoning Models | OA | CLOSE | L2.9/10: hidden-state probe vs verbalized confidence in reasoning models, factual QA | dedicated |
| 17 | 2026 | 2610.32144 | Disentangling Question, Response, and Verifier Languages in Multilingual P(True) Self-Evaluation | S2 | RELATED | L2.3: P(True) self-evaluation across languages | absent |
| 18 | 2026 | 2609.26489 | Calibration as a First-Class Criterion in LLM Evaluation | S2 | RELATED | F/L1: calibration as evaluation criterion (position) | absent |
| 19 | 2026 | 2609.00904 | In-Context Neurofeedback: Can LLMs Control Their Internal Representations through Privileged Access? | S2 | RELATED | control of internal representations | absent |
| 20 | 2026 | 2608.16002 | From Sequence to Structure: Relational Uncertainty Propagation for LLM Agents | OA+S2 | RELATED | L3/L4: trajectory-level UQ for agents | absent |
| 21 | 2026 | 2608.09898 | Consilience for Verifier-Free Test-Time Scaling | OA+S2 | RELATED | L3: verifier-free test-time scaling by confidence; coding mentioned | absent |
| 22 | 2026 | 2607.28457 | SVR: Self-Verifying Refinement via Joint Verdict-Confidence Reinforcement Learning for Adaptive Test-Time Compute | S2 | RELATED | L3: confidence-gated adaptive compute | absent |
| 23 | 2026 | 2607.01612 | Scaling with Confidence: Calibrating Confidence of LLMs for Adaptive Test Time Scaling | OA+S2 | RELATED | L3/L2.11: calibrated confidence for adaptive test-time scaling | mention |
| 24 | 2026 | 2604.19444 | Binary Agreement for Efficient Unsupervised Confidence Calibration of Reasoning LLMs | OA+S2 | RELATED | unsupervised calibration of reasoning LLMs | absent |
| 25 | 2026 | 2603.22161 | Causal evidence that language models use confidence to drive behaviour | S2 | RELATED | causal use of confidence for abstention | mention |
| 26 | 2026 | 2603.19118 | How Uncertainty Estimation Scales with Sampling in Reasoning Models | S2 | RELATED | UE scaling with sampling in reasoning models | absent |
| 27 | 2026 | 2603.16728 | The Cost of Reasoning: Chain-of-Thought Induces Overconfidence in Vision-Language Models | OA+S2 | RELATED | CoT overconfidence in VLMs | absent |
| 28 | 2026 | 2601.07767 | Are LLM Decisions Faithful to Verbal Confidence? | OA+S2 | RELATED | decisions faithful to verbal confidence | absent |
| 29 | 2025 | 2510.21049 | Reasoning's Razor: Reasoning Improves Accuracy but Can Hurt Recall at Critical Operating Points in Safety and Hallucination Detection | S2 | RELATED | reasoning vs recall at operating points | absent |
| 30 | 2026 | 2609.07395 | Uncertainty Quantification for LLM Agents: A Taxonomy, an Evaluation Protocol, and an Empirical Study | OA | RELATED | L3.6: UQ for LLM agents taxonomy | absent |
| 31 | 2026 | 2607.03870 | Evaluating LLM Uncertainty in Long-Form Generation Using Deterministic Ground Truth | OA | RELATED | L1/F: deterministic ground-truth for UE evaluation | absent |
| 32 | 2026 | 2610.28658 | CompLit: Scientific Literature Search Benchmarks Must Cover Implicit, Cumulative, and Unmet Needs | S2 | UNRELATED |  |  |
| 33 | 2026 | 2610.11352 | RL-ARC: Calibrating Large Reasoning Models via Reasoning-guided Uncertainty | S2 | UNRELATED |  |  |
| 34 | 2026 | 2610.23933 | VERDICT: Visual Extraction-Result Decoder with Integrated Confidence and Traceable Evidence | S2 | UNRELATED |  |  |
| 35 | 2026 | 2610.01458 | Rethinking Probability-Based Reinforcement Learning From Posterior Concentration | S2 | UNRELATED |  |  |
| 36 | 2026 | 2609.37054 | ACTR: Aligning Thoughts and Responses for Multilingual Safety in Reasoning LLMs | S2 | UNRELATED |  |  |
| 37 | 2026 | 2609.33898 | No Free Efficiency: Revisiting the Trade-off Between Training Efficiency and Model Vulnerability | S2 | UNRELATED |  |  |
| 38 | 2026 | 2609.26550 | JEV-as-a-Judge: Accept When Confident, Escalate When Unsure | S2 | UNRELATED |  |  |
| 39 | 2026 | 2610.00083 | "very likely"Means"uncertain"? How LLMs Diverge from Humans in Linguistic Uncertainty Quantification | S2 | UNRELATED |  |  |
| 40 | 2026 | 10.1038/s41598-026-69576-2 | Mitigating repetition and loops via implicit signal self-tuning for self-correcting inference | S2 | UNRELATED |  |  |
| 41 | 2026 | 2607.26845 | Thinking Under Uncertainty: Evidence Use and Information-Seeking in Language Models | OA+S2 | UNRELATED |  |  |
| 42 | 2026 | 2606.18089 | From Reasoning Traces to Reusable Modules: Understanding Compositional Generalization in Language Model Reasoning | OA+S2 | UNRELATED |  |  |
| 43 | 2026 | 2606.13649 | Operadic consistency: a label-free signal for compositional reasoning failures in LLMs | OA+S2 | UNRELATED |  |  |
| 44 | 2026 | 2605.31220 | Shared Doubt: Zero-shot Cross-Lingual Confidence Estimation for Language Models | OA+S2 | UNRELATED |  |  |
| 45 | 2026 | 2605.08765 | Unlearners Can Lie: Evaluating and Improving Honesty in LLM Unlearning | OA+S2 | UNRELATED |  |  |
| 46 | 2026 | 2605.01428 | Hallucinations Undermine Trust; Metacognition is a Way Forward | OA+S2 | UNRELATED |  |  |
| 47 | 2026 | 2604.22266 | Large Language Models Decide Early and Explain Later | S2 | UNRELATED |  |  |
| 48 | 2026 | 10.1109/ISPP69262.2026.11543003 | Hierarchical Risk Control in Power Grid Emergency RAG via Domain-Specific Counterfactual Probing | S2 | UNRELATED |  |  |
| 49 | 2026 | 2604.05397 | Confidence Should Be Calibrated More Than One Turn Deep | OA+S2 | UNRELATED |  |  |
| 50 | 2026 | 10.1609/aaai.v40i48.42331 | Can You Trust What I Think? Analyzing and Improving Verbalized Uncertainty and Factuality in Reasoning-Based Large Language Models | OA+S2 | UNRELATED |  |  |
| 51 | 2026 | 2603.15653 | Recursive Language Models Meet Uncertainty: The Surprising Effectiveness of Self-Reflective Program Search for Long Context | OA+S2 | UNRELATED |  |  |
| 52 | 2026 | 2603.09985 | The Dunning-Kruger Effect in Large Language Models: An Empirical Study of Confidence Calibration | OA+S2 | UNRELATED |  |  |
| 53 | 2026 | 2601.23163 | Probing the Trajectories of Reasoning Traces in Large Language Models | OA+S2 | UNRELATED |  |  |
| 54 | 2026 | 2601.19245 | Beyond In-Domain Detection: SpikeScore for Cross-Domain Hallucination Detection | S2 | UNRELATED |  |  |
| 55 | 2026 | 2601.17421 | Oops, Wait: Discourse Tokens Matter in Reasoning Model | OA+S2 | UNRELATED |  |  |
| 56 | 2026 | 2601.07806 | The Confidence Trap: Gender Bias and Predictive Certainty in LLMs | OA+S2 | UNRELATED |  |  |
| 57 | 2026 | 2601.07264 | The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents | OA+S2 | UNRELATED |  |  |
| 58 | 2026 | 2601.06786 | EpiCaR: Knowing What You Don't Know Matters for Better Reasoning in LLMs | S2 | UNRELATED |  |  |
| 59 | 2026 | 2601.03154 | Decoupling the Effect of Chain-of-Thought Reasoning: A Human Label Variation Perspective | S2 | UNRELATED |  |  |
| 60 | 2026 | 2601.03093 | ATLAS: Verifier-Guided Adaptive Latent Activation Steering for Efficient LLM Reasoning | S2 | UNRELATED |  |  |
| 61 | 2025 | 2512.20012 | Reliable LLM-Based Edge-Cloud-Expert Cascades for Telecom Knowledge Systems | S2 | UNRELATED |  |  |
| 62 | 2025 | 2512.01725 | Beware of Reasoning Overconfidence: Pitfalls in the Reasoning Process for Multi-solution Tasks | OA+S2 | UNRELATED |  |  |
| 63 | 2025 | 2512.00729 | Superficial Reflection or Genuine Thought? A Fine-Grained Cognitive Analysis of Large Reasoning Models | S2 | UNRELATED |  |  |
| 64 | 2025 | 2511.15921 | Thinking, Faithful and Stable: Mitigating Hallucinations in LLMs | OA+S2 | UNRELATED |  |  |
| 65 | 2025 | 2511.14275 | Let the Model Distribute Its Doubt: Confidence Estimation through Verbalized Probability Distribution | OA+S2 | UNRELATED |  |  |
| 66 | 2025 | 2511.02130 | Re-FORC: Adaptive Reward Prediction for Efficient Chain-of-Thought Reasoning | S2 | UNRELATED |  |  |
| 67 | 2025 | 2510.21067 | The Virtues of Brevity: Avoid Overthinking in Parallel Test-Time Reasoning | S2 | UNRELATED |  |  |
| 68 | 2025 | 2510.19176 | The Zero-Step Thinking: An Empirical Study of Mode Selection as Harder Early Exit in Reasoning Models | OA+S2 | UNRELATED |  |  |
| 69 | 2025 | 2510.18368 | KoSimpleQA: A Korean Factuality Benchmark with an Analysis of Reasoning LLMs | S2 | UNRELATED |  |  |
| 70 | 2025 | 2510.14925 | False Fixed Points: Kantian Feedback, Stable Miscalibration, and Representational Compression in LLMs | S2 | UNRELATED |  |  |
| 71 | 2025 | 2509.24884 | Expanding Computation Spaces of LLMs at Inference Time | OA+S2 | UNRELATED |  |  |
| 72 | 2025 | 2509.23129 | C2GSPG: Confidence-calibrated Group Sequence Policy Gradient towards Self-aware Reasoning | OA+S2 | UNRELATED |  |  |
| 73 | 2025 | 2509.20645 | Anticipatory Evaluation of Language Models: Predicting LLM Benchmark Scores from Descriptions | S2 | UNRELATED |  |  |
| 74 | 2025 | 2507.10587 | Anthropomimetic Uncertainty: What Verbalized Uncertainty in Language Models is Missing | OA+S2 | UNRELATED |  |  |
| 75 | 2025 | 2506.19467 | Can Reasoning Help Large Language Models Capture Human Annotator Disagreement? | OA+S2 | UNRELATED |  |  |
| 76 | 2025 | 2506.19662 | Multimodal large language models and physics visual tasks: comparative analysis of performance and costs | OA+S2 | UNRELATED |  |  |
| 77 | 2025 | 2506.04909 | When Thinking LLMs Lie: Unveiling the Strategic Deception in Representations of Reasoning Models | S2 | UNRELATED |  |  |
| 78 | 2025 | 2506.03723 | Verbalized Confidence Triggers Self-Verification: Emergent Behavior Without Explicit Reasoning Supervision | OA+S2 | UNRELATED |  |  |
| 79 | 2025 | 2505.22660 | Maximizing Confidence Alone Improves Reasoning | OA+S2 | UNRELATED |  |  |
| 80 | 2025 | 2505.22655 | Position: Uncertainty Quantification Needs Reassessment for Large-language Model Agents | S2 | UNRELATED |  |  |
| 81 | 2025 | 2505.19184 | When Two LLMs Debate, Both Think They'll Win | OA+S2 | UNRELATED |  |  |
| 82 | 2026 | 10.18653/v1/2026.acl-long.1365 | LLMs (Almost) Never Abstain Under Medical Uncertainty | S2 | UNRELATED |  |  |
| 83 | 2026 | 10.18653/v1/2026.findings-eacl.263 | Think Just Enough: Leveraging Self-Assessed Confidence for Adaptive Reasoning in Language Models | OA+S2 | UNRELATED |  |  |
| 84 | 2026 | 10.18653/v1/2026.eacl-long.190 | Reasoning's Razor: Reasoning Improves Accuracy but Hurts Recall at Critical Operating Points in Safety and Hallucination Detection | OA+S2 | UNRELATED |  |  |
| 85 | 2026 | 2607.20444 | Confidently Deceptive: How Confidence Amplifies the Risk of LLM Deception | S2 | UNRELATED |  |  |
| 86 | 2025 | 10.1109/OJIM.2025.3592284 | Conversational LLM-Based Decision Support for Defect Classification in AFM Images | OA+S2 | UNRELATED |  |  |
| 87 | 2025 | 2506.19467 | Can Large Language Models Capture Human Annotator Disagreements? | S2 | UNRELATED |  |  |
| 88 | 2025 | 2509.20645 | Look Before you Leap: Estimating LLM Benchmark Scores from Descriptions | S2 | UNRELATED |  |  |
| 89 | None | none | From Reasoning Traces to Reusable Modules: Reinforcement Learning for Compositional Generalization in Language Model Reasoning | S2 | UNRELATED |  |  |
| 90 | None | none | Same Answer, Different Confidence: Protocol Sensitivity in LLM Calibration | S2 | UNRELATED |  |  |
| 91 | None | none | Anticipatory Evaluation of Language Models | S2 | UNRELATED |  |  |
| 92 | 2026 | 10.18653/2026.findings-emnlp.815 | Learning Solvability Boundaries in LLMs: Improving Reasoning, Detecting Unsolvability, and Calibrating Refusal | OA | UNRELATED |  |  |
| 93 | 2026 | 10.18653/2026.findings-emnlp.2412 | LLMs Decide Early and Explain Later: You Can Stop Them Early | OA | UNRELATED |  |  |
| 94 | 2026 | 2602.08145 | Reliable and Responsible Foundation Models: A Comprehensive Survey | OA | UNRELATED |  |  |
| 95 | 2026 | 2608.23663 | Confidently Wrong, Silently So: Auditing Undetectable Failures of a Deployed On-Device Language Model | OA | UNRELATED |  |  |
| 96 | 2026 | 10.18653/v1/2026.acl-long.1136 | PARIF: Pushing the Pareto Frontier of Instruction Following and Reasoning with Curriculum Reinforcement Learning | OA | UNRELATED |  |  |

## Seed 2604.01457: Wired for Overconfidence

| # | Year | Id | Title | Src | Tag | Bears on | Vault |
|---|---|---|---|---|---|---|---|
| 1 | 2026 | 2610.34994 | Why Are LLMs Confidently Wrong? Correcting Overconfident Errors via Causal Head Intervention | OA+S2 | CLOSE | L2.12: causal head intervention on confidence | absent |
| 2 | 2026 | 2610.22046 | Effectiveness of Hidden-State Probes for Localizing Reasoning Failures | OA+S2 | CLOSE | L2/L4: hidden-state probes for failure type and failing step in reasoning models | absent |
| 3 | 2026 | 2606.03969 | Quantifying Faithful Confidence Expression in Large Reasoning Models | OA+S2 | CLOSE | L2/F: faithful calibration, intrinsic vs expressed confidence in reasoning models | absent |
| 4 | 2026 | 2604.24070 | Distilling Self-Consistency into Verbal Confidence: A Pre-Registered Negative Result and Post-Hoc Rescue on Gemma 3 4B | OA+S2 | CLOSE | L2.11/F: gap between internal information and verbal readout; Type-2 AUROC, validity | absent |
| 5 | 2026 | 2604.22215 | Verbal Confidence Saturation in 3-9B Open-Weight Instruction-Tuned LLMs: A Pre-Registered Psychometric Validity Screen | OA | CLOSE | F.1: psychometric validity screen of verbal confidence (numeric vs categorical) | absent |
| 6 | 2026 | 2606.09876 | Calibrating Overconfidence Without Sacrificing Confidence: Probe-Conditioned Head Intervention for LLMs | OA | CLOSE | L2.12: probe-conditioned head intervention on stated confidence | mention |
| 7 | 2026 | 2610.22636 | Measuring Mechanistic Uncertainty in Large Language Models via Causal Robustness | S2 | RELATED | mechanistic uncertainty via causal robustness | absent |
| 8 | 2026 | 2609.33220 | When Do Models Admit They Are Wrong? Failure Disclosure Is Unstable Under Reinforcement Learning | S2 | RELATED | failure disclosure under RL | absent |
| 9 | 2026 | 2605.07806 | Beyond Confidence: Rethinking Self-Assessments for Performance Prediction in LLMs | OA | RELATED | multidimensional self-assessment vs confidence | absent |
| 10 | 2026 | 10.1145/3805696.3846034 | Triaging Defects in Scholarly Result Graphs with Extraction, Evidence, and Consistency Signals | OA+S2 | UNRELATED |  |  |
| 11 | 2024 | 2408.13378 | DrugAgent: Reliable Multi-Agent Integration of Conflicting Biomedical Evidence for Drug-Target Interaction Assessment | S2 | UNRELATED |  |  |

## Seed 2603.25112: Do LLMs Know What They Know? Metacognitive Efficiency with SDT

| # | Year | Id | Title | Src | Tag | Bears on | Vault |
|---|---|---|---|---|---|---|---|
| 1 | 2026 | 2604.17707 | Before You Interpret the Profile: Validity Scaling for LLM Metacognitive Self-Report | OA+S2 | CLOSE | F.1: validity scaling for metacognitive self-report | absent |
| 2 | 2026 | 2604.15702 | The Metacognitive Monitoring Battery: A Cross-Domain Benchmark for LLM Self-Monitoring | OA+S2 | CLOSE | F.1/F.4: psychometric metacognitive monitoring battery | dedicated |
| 3 | 2026 | 2604.08976 | Quantisation Reshapes the Metacognitive Geometry of Language Models | OA | CLOSE | F.4: M-ratio (meta-d') under quantisation | dedicated |
| 4 | 2026 | 2604.22215 | Verbal Confidence Saturation in 3-9B Open-Weight Instruction-Tuned LLMs: A Pre-Registered Psychometric Validity Screen | OA | CLOSE | F.1: psychometric validity screen of verbal confidence (numeric vs categorical) | absent |
| 5 | 2026 | 2605.06673 | Domain-level metacognitive monitoring in frontier LLMs: A 33-model atlas | OA | CLOSE | F.4: Type-2 AUROC per domain across 33 models | absent |
| 6 | 2026 | 2607.11881 | Metacognition in LLMs: Foundations, Progress, and Opportunities | OA+S2 | RELATED | F.4: metacognition survey | absent |
| 7 | 2026 | 2603.29693 | Measuring (some aspects of) the metacognition of AI | S2 | RELATED | F.4: metacognition of AI measurement | mention |
| 8 | 2026 | 2605.14859 | Do Coding Agents Understand Least-Privilege Authorization? | OA+S2 | UNRELATED |  |  |
| 9 | 2026 | 2604.16009 | MEDLEY-BENCH: Benchmarking Behavioural Metacognition and Belief Revision Under Social Pressure in Large Language Models | OA+S2 | UNRELATED |  |  |
| 10 | 2026 | 10.1109/NQComp68334.2026.11497759 | Integrating Neural and Symbolic Paradigms for Reflective Ethical Reasoning and Belief Modeling | S2 | UNRELATED |  |  |
| 11 | 2026 | 2604.16009 | MEDLEY-BENCH: Scale Buys Evaluation but Not Control in AI Metacognition | S2 | UNRELATED |  |  |
| 12 | 2026 | 2604.11011 | K-Way Energy Probes for Metacognition Reduce to Softmax in Discriminative Predictive Coding Networks | OA | UNRELATED |  |  |

## Seed 2603.14893: LLMs as Signal Detectors

| # | Year | Id | Title | Src | Tag | Bears on | Vault |
|---|---|---|---|---|---|---|---|
| 1 | 2026 | 2605.06673 | Domain-level metacognitive monitoring in frontier LLMs: A 33-model atlas | OA+S2 | CLOSE | F.4: Type-2 AUROC per domain across 33 models | absent |
| 2 | 2026 | 2603.25112 | Do LLMs Know What They Know? Measuring Metacognitive Efficiency with Signal Detection Theory | OA+S2 | CLOSE | F.4: seed-level meta-d' LLM work (cites 2603.14893) | absent |
| 3 | 2026 | 2604.15702 | The Metacognitive Monitoring Battery: A Cross-Domain Benchmark for LLM Self-Monitoring | OA | CLOSE | F.1/F.4: psychometric metacognitive monitoring battery | dedicated |
| 4 | 2026 | 2604.17707 | Before You Interpret the Profile: Validity Scaling for LLM Metacognitive Self-Report | OA | CLOSE | F.1: validity scaling for metacognitive self-report | absent |
| 5 | 2026 | 2604.22215 | Verbal Confidence Saturation in 3-9B Open-Weight Instruction-Tuned LLMs: A Pre-Registered Psychometric Validity Screen | OA | CLOSE | F.1: psychometric validity screen of verbal confidence (numeric vs categorical) | absent |
| 6 | 2026 | 2610.15415 | Sensitivity or Criterion? Measuring and Moving When Language Models Act | OA+S2 | RELATED | F: SDT sensitivity vs criterion for agent actions | absent |
| 7 | 2026 | 2607.11881 | Metacognition in LLMs: Foundations, Progress, and Opportunities | OA+S2 | RELATED | F.4: metacognition survey | absent |
| 8 | 2026 | 2606.15610 | LLM Judges Have Dark Current: Stratified Null and Utility Tests for LLM Judge Reliability | OA+S2 | RELATED | F: psychometric reliability of LLM judges | absent |
| 9 | 2026 | 2606.15610 | LLM Judges Have Dark Current: A Psychometric Datasheet for LLM-as-a-Judge Evaluation | S2 | RELATED | F: psychometric reliability of LLM judges | absent |
| 10 | 2026 | 2610.06522 | Anatomy of LLM Sycophancy: What a Flip Rate Hides | OA+S2 | UNRELATED |  |  |
| 11 | 2026 | 2608.16003 | Prior Audit-Repair Context Shifts LLM Verifier Thresholds Toward Leniency | OA+S2 | UNRELATED |  |  |
| 12 | 2026 | 2604.11011 | K-Way Energy Probes for Metacognition Reduce to Softmax in Discriminative Predictive Coding Networks | OA | UNRELATED |  |  |

## Seed 2610.25846: Measurement Validity and Representation Dynamics of Confidence Signals in LLMs

No citing papers returned by either retrieved source.


## Seed 2603.18893: Don't Ask: What Numeric Self-Reports Measure in Language Models

| # | Year | Id | Title | Src | Tag | Bears on | Vault |
|---|---|---|---|---|---|---|---|
| 1 | 2026 | 2608.20569 | Open-Weight Masked Introspection: Measuring What Language Models Can Report About Their Own Computation | S2 | UNRELATED |  |  |

## Seed 2610.18066: Uncertainty Evaluation: Bridging Machine Learning and Measurement Science

No citing papers returned by either retrieved source.


## Seed 2504.03359: A metrological framework for uncertainty evaluation in ML classification models

| # | Year | Id | Title | Src | Tag | Bears on | Vault |
|---|---|---|---|---|---|---|---|
| 1 | 2026 | 2605.03838 | TRACE: A Metrologically-Grounded Engineering Framework for Trustworthy Agentic AI Systems in Operationally Critical Domains | S2 | CLOSE | F.1: GUM/VIM/ISO 17025 metrology vocabulary for agentic AI trust metrics (not confidence elicitation; abstract only) | absent |
| 2 | 2026 | 2602.12975 | Extending confidence calibration to generalised measures of variation | S2 | RELATED | F: VCE calibration metric (ML classifiers) | absent |
| 3 | 2027 | 10.1016/j.measurement.2026.123752 | Uncertainty evaluation and metrological traceability of machine-learning-based measurement systems across domains: a cross-disciplinary critical review of GUM extensions | S2 | UNRELATED |  |  |
| 4 | 2026 | 10.1016/j.measurement.2026.122819 | Physically constrained TCN-CRF cascade framework for hydraulic support state recognition under long-tailed distribution | S2 | UNRELATED |  |  |
| 5 | 2026 | 10.1088/1681-7575/aea165 | Digital precision in metrology: significant figures and trailing zeros as machine readable metadata | S2 | UNRELATED |  |  |
| 6 | 2026 | 10.3390/metrology6030050 | Development of a Metrological Framework Based on Irradiance and Ventilation for the Characterization and Correction of Low-Cost Radiation Shield Errors | S2 | UNRELATED |  |  |
| 7 | 2026 | 10.1088/1681-7575/ae85ff | Digital transformation in ionizing radiation metrology: advances and priorities | S2 | UNRELATED |  |  |
| 8 | 2026 | 10.1109/AI4IM69129.2026.11558218 | Uncertainty Evaluation in classification-based ML measurements: A first step towards a GUM-based methodology | S2 | UNRELATED |  |  |
| 9 | 2026 | 10.1088/2632-2153/ae35ce | U-TraCE: a conformal prediction approach to uncertainty quantification in black-box models | S2 | UNRELATED |  |  |
| 10 | 2025 | 10.1007/s10712-025-09916-5 | A Metrological Framework for Addressing Uncertainty in Satellite and In Situ Earth Environmental Observations | S2 | UNRELATED |  |  |
| 11 | 2025 | 2511.00301 | A systematic evaluation of uncertainty quantification techniques in deep learning: a case study in photoplethysmography signal analysis | S2 | UNRELATED |  |  |
| 12 | 2025 | 2505.18893 | Reality Check: A New Evaluation Ecosystem Is Necessary to Understand AI's Real World Effects | S2 | UNRELATED |  |  |
| 13 | 2025 | 2503.21510 | An uncertainty-aware Bayesian framework for machine learning classification models: A case study in land cover classification | S2 | UNRELATED |  |  |
| 14 | 2026 | 10.1109/TGRS.2025.3649800 | Terrain-Aware Uncertainty Quantification and Cross-Sensor Consistency Analysis of Hyperspectral Surface Reflectance | S2 | UNRELATED |  |  |
