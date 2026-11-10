# Screening selection, candidate F (measurement-instrument framing)

Source: `candidates-F.tsv` (257 rows). Occupancy questions are F1 to F4 of `docs/s3/POSITIONING_BRIEF_R1.md` section 2. Screening is on title and abstract only (first 400 characters). A blank cell means the TSV has no value.

## 1. Selection table

| Rank | Rating | arXiv | DOI | OpenReview | Year | Title | Questions | Reason |
|---|---|---|---|---|---|---|---|---|
| 1 | CLOSE | 2610.25846 | https://doi.org/10.48550/arxiv.2610.25846 | | 2026 | Measurement Validity and Representation Dynamics of Confidence Signals in Large Language Models | F1, F2 | Pre-registered audit comparing verbalized confidence, hidden-state probe, and sampled agreement under a measurement-validity lens. |
| 2 | CLOSE | 2603.25112 | | | 2026 | Do LLMs Know What They Know? Measuring Metacognitive Efficiency with Signal Detection Theory | F4, F3 | Applies type-2 SDT to LLM confidence, separating type-1 accuracy from type-2 sensitivity. |
| 3 | CLOSE | 2603.14893 | https://doi.org/10.48550/arxiv.2603.14893 | | 2026 | LLMs as Signal Detectors: Sensitivity, Bias, and the Temperature-Criterion Analogy | F2, F4 | Splits calibration into sensitivity and bias; a possible bias/resolution decomposition. |
| 4 | CLOSE | | https://doi.org/10.17605/osf.io/qpk9a | | 2026 | Signal Detection Theory for LLM Calibration | F4, F2 | OSF project applying SDT (d' and response bias c) to calibration metrics. |
| 5 | CLOSE | 2604.08976 | https://doi.org/10.48550/arxiv.2604.08976 | | 2026 | Quantisation Reshapes the Metacognitive Geometry of Language Models | F4 | Reports M-ratio (meta-d' efficiency) for LLMs by domain; direct F4 occupant. |
| 6 | CLOSE | 2512.10451 | https://doi.org/10.48550/arxiv.2512.10451 | | 2025 | Metacognitive Sensitivity for Test-Time Dynamic Model Selection | F4 | Metacognitive sensitivity proposed as a confidence-quality measure for routing. |
| 7 | CLOSE | 2603.18893 | https://doi.org/10.48550/arxiv.2603.18893 | | 2026 | Don't Ask: Understanding What Numeric Self-Reports Measure in Language Models | F1, F2 | Compares numeric self-report with a trained probe of the same internal state; readout-versus-internal-state design. |
| 8 | CLOSE | 2603.15232 | https://doi.org/10.48550/arxiv.2603.15232 | | 2026 | Decomposing Probabilistic Scores: Reliability, Information Loss and Uncertainty | F2, F3 | Decomposition identities that depend on the information level of a predictor; may cover an internal-reference quantity. |
| 9 | CLOSE | 2603.05544 | https://doi.org/10.48550/arxiv.2603.05544 | | 2026 | An intuitive rearranging of the Yates covariance decomposition for probabilistic verification of forecasts with the Brier score | F3 | Rearranges the Yates covariance decomposition into variance mismatch, correlation deficit, and calibration-in-the-large. |
| 10 | CLOSE | 2609.06945 | https://doi.org/10.48550/arxiv.2609.06945 | | 2026 | Brier-UDAM for Paired Prediction-Rule Comparisons: Latent-Risk Interpretation, Observable Contrasts, and Inference | F2, F3 | Separates Brier difference into mean-bias, dispersion, and scale alignment; closest existing bias/resolution-style split. |
| 11 | CLOSE | 2603.29693 | | | 2026 | Measuring (some aspects of) the metacognition of AI | F4, F1 | Metacognition measurement for AI under a measurement-science vocabulary. |
| 12 | CLOSE | | https://doi.org/10.31234/osf.io/8jq4f_v1 | | 2026 | A trade-off between reasoning ability and metacognitive sensitivity in large language models | F4 | Item-level metacognitive sensitivity versus reasoning; bears on F4 and on reasoning-versus-confidence. |
| 13 | RELATED | 2608.14552 | https://doi.org/10.48550/arxiv.2608.14552 | | 2026 | Large Language Models Show Metacognitive Sensitivity in Medical Reasoning | F4 | Metacognitive sensitivity operationalized in LLMs; comparison side for F4. |
| 14 | RELATED | 2609.12439 | https://doi.org/10.48550/arxiv.2609.12439 | | 2026 | Debiasing as a Measurement Intervention: Calibrated Ties and Resolution Loss in LLM-as-a-Judge Evaluation | F1 | Uses "measurement instrument" and "resolution" vocabulary for LLM judges. |
| 15 | RELATED | 2609.14754 | | | 2026 | Calibrating Interpretability Instruments Before Trusting Their Verdicts | F1 | Treats interpretability measurements as instruments needing calibration; vocabulary neighbor for probes. |
| 16 | RELATED | 2604.19809 | https://doi.org/10.48550/arxiv.2604.19809 | | 2026 | MIRROR: A Hierarchical Benchmark for Metacognitive Calibration in Large Language Models | F4, F1 | Metacognitive calibration benchmark with multiple measurement channels. |
| 17 | RELATED | 2604.15702 | | | 2026 | The Metacognitive Monitoring Battery: A Cross-Domain Benchmark for LLM Self-Monitoring | F1, F4 | Psychometric-style battery for monitoring and calibration. |
| 18 | RELATED | 2601.01828 | https://doi.org/10.48550/arxiv.2601.01828 | | 2026 | Emergent Introspective Awareness in Large Language Models | F1 | Self-report versus injected internal state; the readout-versus-internal-state design. |
| 19 | RELATED | 2410.13787 | https://doi.org/10.48550/arxiv.2410.13787 | | 2024 | Looking Inward: Language Models Can Learn About Themselves by Introspection | F1 | Foundation for self-report as readout of internal state. |
| 20 | RELATED | 2507.05587 | https://doi.org/10.48550/arxiv.2507.05587 | | 2025 | Towards Measurement Theory for Artificial Intelligence | F1 | Formal measurement theory for AI evaluation; vocabulary baseline. |
| 21 | RELATED | 2603.00063 | https://doi.org/10.48550/arxiv.2603.00063 | | 2026 | Measuring What AI Systems Might Do: Towards A Measurement Science in AI | F1 | Argues for a measurement science of AI quantities. |
| 22 | RELATED | 2602.15532 | https://doi.org/10.48550/arxiv.2602.15532 | | 2026 | Quantifying construct validity in large language model evaluations | F1 | Construct-validity quantification for LLM evaluations. |
| 23 | RELATED | 2312.08589 | https://doi.org/10.48550/arxiv.2312.08589 | | 2023 | Consistent and Asymptotically Unbiased Estimation of Proper Calibration Errors | F2, F3 | Calibration-plus-refinement decomposition and estimator; the standard decomposition to differ from. |
| 24 | RELATED | 2603.04275 | https://doi.org/10.48550/arxiv.2603.04275 | | 2026 | Statistical Inference for Score Decompositions | F2, F3 | Miscalibration, discrimination, and uncertainty decomposition with inference. |
| 25 | RELATED | 2501.19195 | https://doi.org/10.48550/arxiv.2501.19195 | | 2025 | Rethinking Early Stopping: Refine, Then Calibrate | F2 | Calibration and refinement split of proper losses. |
| 26 | RELATED | 2504.03359 | https://doi.org/10.1088/1681-7575/ae1bae | | 2025 | A metrological framework for uncertainty evaluation in machine learning classification models | F1 | Metrology vocabulary applied to ML classification (not LLM confidence); comparison side. |
| 27 | RELATED | 2610.18066 | https://doi.org/10.48550/arxiv.2610.18066 | | 2026 | Uncertainty Evaluation: Bridging Machine Learning and Measurement Science | F1 | Maps ML uncertainty evaluation onto GUM-style measurement science. |
| 28 | RELATED | 2504.14045 | https://doi.org/10.1177/09637214251391158 | | 2025 | Metacognition and Uncertainty Communication in Humans and Large Language Models | F4 | Overview of LLM metacognition; foundation for F4. |
| 29 | RELATED | 2311.08298 | https://doi.org/10.18653/v1/2024.naacl-long.366 | | 2024 | A Survey of Confidence Estimation and Calibration in Large Language Models | F1, F2 | Survey; checks whether any measurement vocabulary or decomposition appears. |
| 30 | RELATED | 2605.26242 | | | 2026 | Can LLMs Introspect? A Reality Check | F1 | Privileged-access criteria for self-report as readout. |

## 2. MISSING LEADS

Seed leads from the brief for F that do not appear in the TSV. Search by these exact title words.

1. Murphy 1973: "A New Vector Partition of the Probability Score" (Brier score decomposition; pre-2022 foundation).
2. Yates covariance decomposition of the Brier score: search "Yates covariance decomposition Brier score" (original Yates source not in TSV; only the 2026 rearrangement is).
3. Meta-d' literature: "How to measure metacognition" (Fleming and Lau).
4. Meta-d' literature: "Signal detection theory analysis of type 1 and type 2 data: meta-d', response-specific meta-d', and the unequal variance SDT model" (Maniscalco and Lau).
5. Psychometrics of LLMs, construct validity: "Measuring what Matters: Construct Validity in Large Language Model Benchmarks" is in the TSV (2511.04703, not selected as not calibration-specific); no further named lead missing.

No other seed leads for F are named in the brief.

## 3. Counts

Rows screened: 257. CLOSE: 12. RELATED: 18. Rejected: 227.
