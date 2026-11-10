# Forward-citation screen, group G3 (L3 routing/abstention, L4 localization)

Retrieved 2026-11-10 from api.semanticscholar.org (citations endpoint, limit 100, no `next` on any seed) and api.openalex.org (cites filter, cursor paging). Raw JSON in `raw/`. Tags: CLOSE, RELATED, UNRELATED, by title and abstract only (no full text). Merged by title and arXiv id.

**Gaps and cautions.** No HTTP errors or backoff gaps occurred on any call. Seeds posted in 2026-09 to 2026-11 (2609.12489, 2610.30284, 2611.06372) and others show zero citers; this reflects index lag at both sources, so zero is an instrument limit, not evidence of no citers. OpenAlex returns no abstracts for most records (inverted index absent), so OpenAlex-only items are screened by title.

Seed titles come from export.arxiv.org (`raw/arxiv_seed_titles.xml`).

## 2610.30284: SWE-VERIFIER: Selective Verification for Cost-Efficient Coding Agents (L3)

- Semantic Scholar citations: 0
- OpenAlex citations (cites filter): 0
- Merged distinct: 0
- Retrieval date: 2026-11-10
- Gap: none (index lag possible for recent seeds)

No citing papers returned.

## 2611.06372: Give Up to Get More: Priors, Not Policies, Govern Test-Time Compute Allocation (L3)

- Semantic Scholar citations: 0
- OpenAlex citations (cites filter): 0
- Merged distinct: 0
- Retrieval date: 2026-11-10
- Gap: none (index lag possible for recent seeds)

No citing papers returned.

## 2506.10056: Pareto Optimal Code Generation (L3)

- Semantic Scholar citations: 0
- OpenAlex citations (cites filter): 1
- Merged distinct: 1
- Retrieval date: 2026-11-10
- Gap: none (index lag possible for recent seeds)

| arXiv id / DOI | Title | Year | Source | Tag | Reason | In vault |
|---|---|---|---|---|---|---|
| 2604.01411 | Test-Time Scaling Makes Overtraining Compute-Optimal | 2026 | OpenAlex only (no S2 record; abstract not retrieved) | UNRELATED | Title only screen; scaling-law paper, no code confidence claim; ABSTRACT-NOT-RETRIEVED | no |

## 2605.17029: Task Abstention for Large Language Models in Code Generation (L3)

- Semantic Scholar citations: 0
- OpenAlex citations (cites filter): 0
- Merged distinct: 0
- Retrieval date: 2026-11-10
- Gap: none (index lag possible for recent seeds)

No citing papers returned.

## 2605.19369: When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions (L3)

- Semantic Scholar citations: 2
- OpenAlex citations (cites filter): 0
- Merged distinct: 2
- Retrieval date: 2026-11-10
- Gap: none (index lag possible for recent seeds)

| arXiv id / DOI | Title | Year | Source | Tag | Reason | In vault |
|---|---|---|---|---|---|---|
| 2610.21248 | Beyond Confidence: Rethinking Uncertainty Calibration in Deep Code Models | 2026 | S2 | RELATED | Selective prediction and calibration for discriminative code models (defect prediction, vulnerability detection), not generated-code execution correctness; bears on L3 Q3 and F | partial: appears only in research/notes/ravishka-rathnasuriya-publications.md, no own note |
| 2610.11300 | Characterizing Overconfident Failure in LLM-Based Code Generation | 2026 | S2 | CLOSE | Token-level and program-level confidence vs execution correctness on four code models, three benchmarks, selective generation, instruct-tuning effect, latent probe hint; bears on L1 and L2 | yes |

## 2608.14659: When Uncertainty Isn't Enough: An Empirical Study of Self-Correction in Code Generation (L3)

- Semantic Scholar citations: 2
- OpenAlex citations (cites filter): 0
- Merged distinct: 2
- Retrieval date: 2026-11-10
- Gap: none (index lag possible for recent seeds)

| arXiv id / DOI | Title | Year | Source | Tag | Reason | In vault |
|---|---|---|---|---|---|---|
| 2611.07876 | Which Signals of Code Correctness Survive Distribution Shift? Hidden-State and Causal Predictors of Program and Verdict Correctness | 2026 | S2 | CLOSE | Execution-free correctness predictors (output probabilities, samples, hidden states) under distribution shift, routing judgments to costly verification; bears on L2 and L3 | yes |
| 2610.11300 | Characterizing Overconfident Failure in LLM-Based Code Generation | 2026 | S2 | CLOSE | As above; also cites seed on self-correction/uncertainty; bears on L1, L2 | yes |

## 2609.12489: Confidence-Gated Transductive Test Generation for Code Reranking (L3)

- Semantic Scholar citations: 0
- OpenAlex citations (cites filter): 0
- Merged distinct: 0
- Retrieval date: 2026-11-10
- Gap: none (index lag possible for recent seeds)

No citing papers returned.

## 2512.24560: Localized Calibrated Uncertainty in Code Language Models (L4)

- Semantic Scholar citations: 4
- OpenAlex citations (cites filter): 3
- Merged distinct: 4
- Retrieval date: 2026-11-10
- Gap: none (index lag possible for recent seeds)

| arXiv id / DOI | Title | Year | Source | Tag | Reason | In vault |
|---|---|---|---|---|---|---|
| 2611.07876 | Which Signals of Code Correctness Survive Distribution Shift? Hidden-State and Causal Predictors of Program and Verdict Correctness | 2026 | S2 | CLOSE | Hidden-state predictors of program correctness; L2 component probe-vs-readout | yes |
| 2608.08266 | On the Robustness of LLMs' Internal Representation of Code Correctness | 2026 | S2 and OpenAlex | CLOSE | Robustness of hidden-state correctness probes for code; L2 probe-beats-verbal | yes |
| 2607.12273 | Code-MUE: Measuring Code LLMs' Uncertainty through Execution-Based Semantic Interaction Graphs | 2026 | S2 and OpenAlex (DOI 10.1145/3832276) | CLOSE | Execution-based uncertainty for code LLMs; L1 sampled-confidence family | yes |
| 2607.05188 | Latent Programming Horizons in Coding Agents | 2026 | S2 and OpenAlex | CLOSE | Step-level probes on agent residual streams for program properties; L4 component (step-level localization) and L2 | yes |

## 2606.03852: FLARE: Fine-Grained Diagnostic Feedback for LLM Code Refinement (L4)

- Semantic Scholar citations: 1
- OpenAlex citations (cites filter): 1
- Merged distinct: 1
- Retrieval date: 2026-11-10
- Gap: none (index lag possible for recent seeds)

| arXiv id / DOI | Title | Year | Source | Tag | Reason | In vault |
|---|---|---|---|---|---|---|
| 2607.07663 | Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops | 2026 | S2 and OpenAlex | RELATED | Survey of 1,250 self-improvement papers; mentions refinement, no confidence-as-claim | n/a (not CLOSE) |

## 2604.06723: Fine-grained Approaches for Confidence Calibration of LLMs in Automated Code Revision (L4)

- Semantic Scholar citations: 0
- OpenAlex citations (cites filter): 0
- Merged distinct: 0
- Retrieval date: 2026-11-10
- Gap: none (index lag possible for recent seeds)

No citing papers returned.

## Totals

Distinct citing papers across all ten seeds: 8 (2611.07876, 2610.11300, 2608.08266, 2607.12273, 2607.05188, 2610.21248, 2607.07663, 2604.01411). CLOSE: 5 (2611.07876, 2610.11300, 2608.08266, 2607.12273, 2607.05188). All five CLOSE papers are already in the vault (note filenames checked by grep of research/notes).
