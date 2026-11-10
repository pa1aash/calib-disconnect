# A1b: decomposition-occupancy search (titles and abstracts)

Run date 2026-11-10. Instruments: Semantic Scholar `paper/search/bulk` (year=2023-2026, fields title,year,externalIds,abstract,publicationDate; one page, up to 1000 records) and OpenAlex works `search` (filter publication_year:2023-2026, per-page 100, relevance order, first page only). No API keys. No HTTP 429 occurred on either instrument (backoff code was armed but not used). Candidate abstracts were cross-checked with export.arxiv.org `id_list`; full texts were read from arxiv.org/html/<id>. Raw JSON is in `raw/` (one file per query id), arXiv abstracts in `raw/arxiv_abs.xml`, and full-text HTML in `raw/fulltext/`.

Notes on the record:
- The per-run log files `raw/_log_s2.json` and `raw/_log_oa.json` for batch 1 were overwritten by batch 2 (now `_log_s2b.json`, `_log_oab.json`). The counts below are recomputed from the saved raw JSON; the HTTP 200 for every batch-1 query was printed to stdout at run time.
- OpenAlex `search` does not apply the boolean as a strict filter (counts in the thousands), so only the first 100 records by relevance were screened; OpenAlex zeros or misses are not evidence of absence. S2 bulk counts are the instrument totals.
- Recall check against the known set: 7 of 8 surfaced (2512.07404 S29; 2611.07876 O17, O19, S32; 2609.34857 O01; 2610.31820 O03; 2605.22949 O08, O15; 2609.36783 S11; 2402.02047 by title in O04, O11, O15, O19). 2610.34654 did not surface in any query.
- Screening: all records were filtered by regex (LLM term, confidence term, and either a probe-or-token-versus-verbal pattern or a decomposition/attribution term plus a nuisance-term pattern); 159 survived plus the batch-2 lists, and titles and abstracts were read by hand.

## Query log

| id | instrument | query | count | HTTP |
|---|---|---|---|---|
| S01 | S2 bulk | `("verbalized confidence" \| "expressed confidence" \| "stated confidence" \| "verbal confidence") + (probe \| probing \| "internal confidence" \| "token probability" \| logit) + (gap \| discrepancy \| mismatch \| disconnect \| misalignment)` | 15 (15 returned) | 200 |
| S02 | S2 bulk | `"internal confidence" + ("verbalized" \| "expressed" \| "stated")` | 27 (27 returned) | 200 |
| S03 | S2 bulk | `(probe \| probing) + "verbalized confidence" + calibration` | 7 (7 returned) | 200 |
| S04 | S2 bulk | `("know more than" \| "knowing" ) + ("say" \| "tell") + confidence + "language model"` | 3 (3 returned) | 200 |
| S05 | S2 bulk | `"verbalized" + (logit \| "token probability" \| "sequence probability") + calibration + (compare \| comparison \| versus)` | 8 (8 returned) | 200 |
| S06 | S2 bulk | `decomposition + calibration + ("language model" \| LLM) + confidence` | 52 (52 returned) | 200 |
| S07 | S2 bulk | `"error budget" + (calibration \| uncertainty \| confidence)` | 223 (223 returned) | 200 |
| S08 | S2 bulk | `"variance decomposition" + (calibration \| "uncertainty estimation" \| "confidence estimation")` | 42 (42 returned) | 200 |
| S09 | S2 bulk | `Shapley + (calibration \| "uncertainty quantification" \| "confidence estimation") + ("language model" \| LLM)` | 11 (11 returned) | 200 |
| S10 | S2 bulk | `"systematics" + (calibration \| uncertainty) + ("language model" \| LLM)` | 1221 (1000 returned) | 200 |
| S11 | S2 bulk | `(reproduce \| reproducibility \| replication \| reconcile \| reconciliation) + ("confidence estimation" \| "uncertainty estimation" \| "uncertainty quantification" \| calibration) + ("language models" \| LLMs)` | 425 (425 returned) | 200 |
| S12 | S2 bulk | `("label noise" \| "noisy labels" \| "label validity" \| "label quality") + (calibration \| "uncertainty quantification" \| "confidence estimation") + (LLM \| "language model")` | 13 (13 returned) | 200 |
| S13 | S2 bulk | `("test suite" \| "test cases" \| "unit tests") + (calibration \| "confidence estimation" \| "uncertainty") + "code generation"` | 12 (12 returned) | 200 |
| S14 | S2 bulk | `("within-question" \| "per-question" \| "within-prompt" \| "per-prompt") + (calibration \| AUROC \| "uncertainty")` | 67 (67 returned) | 200 |
| S15 | S2 bulk | `("prompt-only" \| "question-only" \| "input-only" \| "query-only") + (confidence \| correctness \| uncertainty) + (LLM \| "language model")` | 91 (91 returned) | 200 |
| S16 | S2 bulk | `(difficulty \| "question difficulty") + (confound \| confounder \| confounding) + (uncertainty \| confidence \| calibration) + (LLM \| "language model")` | 5 (5 returned) | 200 |
| S17 | S2 bulk | `("Platt scaling" \| "temperature scaling" \| recalibration) + ("verbalized confidence" \| "verbalized uncertainty")` | 9 (9 returned) | 200 |
| S18 | S2 bulk | `("own generations" \| "self-generated" \| "on-policy" \| "off-policy") + (probe \| probing) + (correctness \| hallucination \| truthfulness \| confidence)` | 181 (181 returned) | 200 |
| S19 | S2 bulk | `("distribution shift" \| "generalization") + ("truthfulness probe" \| "correctness probe" \| "hallucination probe" \| "probing classifier") + LLM` | 3 (3 returned) | 200 |
| S20 | S2 bulk | `(pitfalls \| "evaluation flaws" \| "spurious" \| confounders) + ("uncertainty quantification" \| "uncertainty estimation") + (LLM \| "language models") + evaluation` | 5 (5 returned) | 200 |
| S21 | S2 bulk | `("confidence estimation" \| calibration \| "uncertainty") + "code" + (execution \| "functional correctness") + (LLM \| "language model")` | 143 (143 returned) | 200 |
| S22 | S2 bulk | `introspection + (verbalized \| "self-report" \| "self-reported") + (internal \| probe) + confidence` | 1 (1 returned) | 200 |
| S23 | S2 bulk | `(metacognition \| metacognitive) + (probe \| "internal states") + (verbalized \| "self-reported") + confidence` | 7 (7 returned) | 200 |
| S24 | S2 bulk | `"calibration gap" + ("language model" \| LLM)` | 22 (22 returned) | 200 |
| S25 | S2 bulk | `(attribution \| attribute) + ("calibration error" \| miscalibration \| overconfidence) + (LLM \| "language model") + sources` | 8 (8 returned) | 200 |
| S26 | S2 bulk | `("supervised probe" \| "trained probe" \| "linear probe") + ("zero-shot" \| "training-free") + (uncertainty \| confidence) + (LLM \| "language model")` | 5 (5 returned) | 200 |
| S27 | S2 bulk | `("frozen generations" \| "fixed generations" \| "shared generations" \| "same generations") + (confidence \| uncertainty)` | 13 (13 returned) | 200 |
| S28 | S2 bulk | `("benchmark" \| "unified") + ("confidence estimation" \| "uncertainty quantification") + (LLM \| "language model") + (inconsistent \| inconsistencies \| "conflicting")` | 25 (25 returned) | 200 |
| S29 | S2 bulk | `("code generation" \| "code LLMs" \| "code language models") + (probe \| probing \| "internal representation" \| "hidden states") + correctness` | 44 (44 returned) | 200 |
| S30 | S2 bulk | `("code language models" \| "code LLMs" \| "LLMs for code") + (calibration \| "confidence estimation")` | 42 (42 returned) | 200 |
| S31 | S2 bulk | `("knowing-saying" \| "cannot say so" \| "say what they know" \| "know when they are wrong")` | 19 (19 returned) | 200 |
| S32 | S2 bulk | `(probe \| "hidden states") + ("verbalized" \| "self-reported" \| "stated") + AUROC + correctness` | 25 (25 returned) | 200 |
| S33 | S2 bulk | `("propagation gap" \| "metacognitive gap" \| "readout gap" \| "confidence gap" \| "introspection gap") + (LLM \| "language model")` | 19 (19 returned) | 200 |
| S34 | S2 bulk | `("variance partitioning" \| "variance partition" \| "ANOVA") + (confidence \| calibration \| uncertainty) + (LLM \| "language model")` | 30 (30 returned) | 200 |
| S35 | S2 bulk | `("multiverse" \| "specification curve" \| "researcher degrees of freedom" \| "measurement choices") + (calibration \| uncertainty \| confidence) + (LLM \| "language model")` | 4 (4 returned) | 200 |
| O01 | OpenAlex | `"verbalized confidence" AND (probe OR "internal confidence" OR "token probability") AND (gap OR discrepancy OR mismatch)` | 531 (100 returned) | 200 |
| O02 | OpenAlex | `"internal confidence" AND ("verbalized confidence" OR "expressed confidence" OR "stated confidence")` | 175 (100 returned) | 200 |
| O03 | OpenAlex | `probing AND "verbalized confidence" AND calibration` | 411 (100 returned) | 200 |
| O04 | OpenAlex | `"verbalized" AND "token probability" AND calibration AND "language model"` | 566 (100 returned) | 200 |
| O05 | OpenAlex | `"error budget" AND (calibration OR uncertainty) AND "language model"` | 445 (100 returned) | 200 |
| O06 | OpenAlex | `"variance decomposition" AND (calibration OR "uncertainty estimation") AND "language model"` | 554 (100 returned) | 200 |
| O07 | OpenAlex | `Shapley AND (calibration OR "uncertainty quantification") AND "language model"` | 3377 (100 returned) | 200 |
| O08 | OpenAlex | `decomposition AND calibration AND "verbalized confidence"` | 384 (100 returned) | 200 |
| O09 | OpenAlex | `reproducibility AND ("uncertainty quantification" OR "confidence estimation") AND "large language models"` | 5766 (100 returned) | 200 |
| O10 | OpenAlex | `"label noise" AND calibration AND "large language model"` | 1505 (100 returned) | 200 |
| O11 | OpenAlex | `"test suite" AND (calibration OR confidence) AND "code generation"` | 2012 (100 returned) | 200 |
| O12 | OpenAlex | `("per-question" OR "within-question") AND (calibration OR AUROC) AND "language model"` | 2110 (100 returned) | 200 |
| O13 | OpenAlex | `("prompt-only" OR "question-only") AND (confidence OR correctness) AND "language model"` | 6885 (100 returned) | 200 |
| O14 | OpenAlex | `difficulty AND confound AND (uncertainty OR calibration) AND "language model"` | 7481 (100 returned) | 200 |
| O15 | OpenAlex | `(recalibration OR "Platt scaling" OR "temperature scaling") AND "verbalized confidence"` | 263 (100 returned) | 200 |
| O16 | OpenAlex | `("self-generated" OR "on-policy" OR "off-policy") AND probe AND (hallucination OR correctness)` | 91666 (100 returned) | 200 |
| O17 | OpenAlex | `("truthfulness probe" OR "correctness probe" OR "hallucination probe") AND generalization` | 139 (100 returned) | 200 |
| O18 | OpenAlex | `pitfalls AND "uncertainty quantification" AND "language models"` | 930 (100 returned) | 200 |
| O19 | OpenAlex | `"confidence estimation" AND "code generation" AND execution` | 209 (100 returned) | 200 |
| O20 | OpenAlex | `introspection AND "verbalized" AND confidence AND "language model"` | 258 (100 returned) | 200 |
| O21 | OpenAlex | `metacognitive AND probe AND confidence AND "language model"` | 1600 (100 returned) | 200 |
| O22 | OpenAlex | `"calibration gap" AND "language model"` | 473 (100 returned) | 200 |
| O23 | OpenAlex | `"linear probe" AND "zero-shot" AND uncertainty AND "language model"` | 1137 (100 returned) | 200 |
| O24 | OpenAlex | `"uncertainty quantification" AND "large language models" AND (inconsistent OR conflicting) AND benchmark` | 4318 (100 returned) | 200 |
| O25 | OpenAlex | `"expressed confidence" AND "internal" AND "language model"` | 827 (100 returned) | 200 |
| O26 | OpenAlex | `"knowing-saying gap"` | 3 (3 returned) | 200 |
| O27 | OpenAlex | `"propagation gap" AND confidence AND "language model"` | 10 (10 returned) | 200 |
| O28 | OpenAlex | `"code" AND probe AND "verbalized confidence"` | 317 (100 returned) | 200 |
| O29 | OpenAlex | `"variance partitioning" AND "verbal confidence"` | 2 (2 returned) | 200 |
| O30 | OpenAlex | `"multiverse analysis" AND (calibration OR uncertainty) AND "language model"` | 119 (100 returned) | 200 |

Supporting lookups: export.arxiv.org `id_list` for 14 candidate ids (HTTP 200); arxiv.org/html for 10 ids (all HTTP 200).

## Candidate table

Terms: SUP = supervision (zero-shot vs recalibrated vs trained readout), DIF = difficulty (pooled vs within-question, prompt-only baseline), LAB = label validity (test-suite strength, label noise), GEN = generation shift (own vs frozen or supplied generations), DEC = explicit decomposition, attribution, or variance partition. "Shared gens" = whether the compared readouts are scored on the same answers.

| id | title | date | readouts compared | terms varied | shared gens | access | section cites |
|---|---|---|---|---|---|---|---|
| 2605.27752 | Same Answer, Different Confidence: Protocol Sensitivity in LLM Confidence Calibration (v4 title: "...in Measuring LLM Confidence") | 2026-05-26 (v4 2026-10-23) | verbalized vs token probability (no probe) | DEC (shift of the verbal-token gap attributed by axis: scoring context, correctness rule, token aggregation, ECE estimator); SUP partly (isotonic and Platt recalibration within context and transfer across contexts); LAB partly (correctness rule, exact match vs default); GEN partly (own vs supplied answers); also a targeted review of 12 published verbal-vs-token comparisons. No DIF term, no probe | Yes ("we fix each answer, its verbalized confidence, and its correctness label") | FULL TEXT | Abstract; Sec. 3.5 Metrics; Sec. 4.1 Context Shift; Sec. 4.2 Prompt Ablation; Sec. 4.4 Comparing the Axes (Table 4); Sec. 4.5 Supplied Answers; App. G "Calibration transfer"; App. I "Own versus supplied"; App. J Review of Published Comparisons |
| 2606.29490 | Reported Confidence in LLMs Tracks Commitment More Than Correctness | 2026-06-28 | verbalized vs Platt/temperature-calibrated log-prob vs activation probes | DEC (two-way ANOVA partial eta-squared, correctness vs decision; residualisation of VC on Cal-LP, correctness, and item difficulty); SUP fixed (Cal-LP calibrated on Phase 0, not varied as a term); DIF as a residualisation covariate | Yes within model (Phase 1 answers) | FULL TEXT | "Residualisation analysis"; "ANOVA and partial eta^2" (Methods); "Calibration of log-probability confidence"; Supplemental Table 7 |
| 2610.22139 | Are You Sure Your LLM Is Sure? Repairing and Auditing Confidence (RADAR) | 2026-10-15 | likelihood and fixed-choice scores, correctness probes (as repair anchors); no verbalized arm evaluated | DEC (squared-risk split into outcome noise, hidden information, mapping error, pooling gap); SUP (label-isotonic vs probe-anchored isotonic); distribution shift by difficulty, task, subject | Yes ("fixed realized answers") | FULL TEXT | Abstract; Sec. 3 (Theorem 3.1); Sec. 3.2 PAIC; Sec. 4.2; App. B.3 |
| 2610.25846 | Measurement Validity and Representation Dynamics of Confidence Signals in LLMs | 2026-10-19 | verbalized vs hidden-state probe vs semantic entropy | DIF (prompt-only TF-IDF baseline matches probe in 9 of 11 retrieval cells); verbal template instability; ECE vs resolution. No SUP, LAB, GEN, or gap decomposition | Yes ("re-ran the probe stages over the same generations") | FULL TEXT | Sec. 1; Sec. 4.1; Sec. 4.2; Sec. 6.1 ECE Equivalence Fallacy; Sec. 8 |
| 2608.28382 | When Linguistic and Internal Confidence Diverge in LLMs | 2026-08-28 | linguistic (verbalized) vs logit confidence; vs semantic entropy for generation | DEC-like (regression of alignment on score-distribution properties and model metadata); DIF (association higher on easier items, task-level); prompt design. No probe, no SUP, LAB, GEN | Not stated in text searched | FULL TEXT | Sec. 3.1 to 3.3; Sec. 5.2; Sec. 5.5; Sec. 6.1 Regression Modeling |
| 2605.09502 | Hidden Error Awareness in Chain-of-Thought Reasoning | 2026-05-10 | hidden-state probe vs verbalized confidence vs text-surface classifier | DIF (within-problem difficulty control, Table 3; text-surface baseline 0.59 vs probe 0.95). No SUP, LAB, GEN, DEC | Yes (same traces) | FULL TEXT | "Comparison with baselines"; "Difficulty control" (Table 3); Sec. 4.2 Textual indistinguishability |
| 2608.07528 | The Knowing-Saying Gap: When Probes See Errors that Confidence Misses | 2026-07-21 | linear probe vs structured verbal confidence | DIF (contrastive matched clean/corrupted design controls difficulty). No SUP, LAB, GEN, DEC | Yes (frozen models, matched pairs) | FULL TEXT | Sec. 4.1; Sec. 4.2 Contrastive probing design; Sec. 4.7 |
| 2607.22034 | Small VLMs Know When They Are Wrong But Cannot Say So | 2026-07-24 | stated vs mean token probability | SUP partly (post-hoc temperature scaling, negative result). No DIF, LAB, GEN, DEC | Yes (same predictions) | FULL TEXT | Sec. 2.2; Sec. 4.6; Sec. 4.7 |
| 2603.17839 | How do LLMs Compute Verbal Confidence | 2026-03-18 | verbal confidence vs token log-prob vs cached activations | DEC (variance partitioning of verbal confidence beyond log-probs). No SUP (no temperature scaling, App. B), DIF, LAB, GEN | Yes | FULL TEXT | Sec. 2.6 Decoding Confidence Information; App. B |
| 2608.08266 | On the Robustness of LLMs' Internal Representation of Code Correctness | 2026-08-08 | internal correctness direction (follow-up to 2512.07404) | Reproduces 2512.07404 and varies extraction configuration and data (fault-isolated pairs); test suite noted as proxy (no LAB variation). Not a probe-vs-stated gap | n/a | FULL TEXT | Sec. III-C; Sec. IV (RQ1); Sec. V (RQ2) |
| Propagation Gap (Zenodo 10.5281/zenodo.19122015) | The Propagation Gap: Hidden-State Reliability Signals Do Not Reach Language Model Outputs | 2026-03-20 | hidden-state probe vs logit features vs verbalized | Probe-minus-output AUROC gap (0.18 to 0.19); surface-form controls (DIF-like). Decomposition not stated in abstract | Unknown | ABSTRACT-ONLY (no arXiv copy found; Zenodo not on allowlist) | n/a |
| PT-CSFT (Zenodo 10.5281/zenodo.20436840) | Making LLMs Say What They Know: Probe-Targeted Fine-Tuning for Verbal Confidence Calibration | 2026 | probe vs verbal (SFT closes gap) | SUP (trained verbal readout targeted at probe). No decomposition in abstract | Unknown | ABSTRACT-ONLY | n/a |
| 2604.24070 | Distilling Self-Consistency into Verbal Confidence (Gemma 3 4B) | 2026-04-27 | verbal vs logit entropy vs self-consistency | SUP (CSFT trained verbal readout) | Unknown | ABSTRACT-ONLY | n/a |
| 2609.20541 | An Analysis of Training-Free Self-Reported Confidence in Language Models | 2026-09-17 | verbalized vs P(True) vs sample agreement | LAB (benchmark-error audit), re-elicitation on fixed answers | Yes per abstract | ABSTRACT-ONLY | n/a |
| Verbalized Uncertainty in Coding LLMs (UncertaiNLP 2026, 10.18653/2026.uncertainlp-main.21) | A Contamination-Aware Study of Confidence Calibration | 2026 | verbalized only (three elicitations), code | Frozen code generations; no internal readout | Yes (frozen generations) | ABSTRACT-ONLY | n/a |

Also screened and judged not relevant to a gap decomposition (abstract only): 2512.11998 DCA, 2408.09773, 2405.16282, 2604.01457, 2505.23854, 2609.34454, 2610.27566, 2610.03894, 2608.14659, 2609.13975, 2607.08456, 2609.16933, 2608.08791, 2604.17714, 2605.09844, 2606.22179, "The Impact of Off-Policy Training Data on Probe Generalisation" (Findings ACL 2026; GEN for probes, no verbal arm). No title or abstract matched "error budget", "systematics budget", or Shapley attribution applied to LLM calibration or uncertainty evaluation.

## Verdict

No paper found decomposes the probe-versus-stated-confidence gap into supervision, difficulty, label-validity, and generation-shift terms on shared generations (stop case not triggered, title and abstract level). The closest occupant is 2605.27752: on fixed answers it attributes the token-versus-verbalized gap to protocol axes (context, correctness rule, aggregation, estimator), with recalibration transfer, own-versus-supplied answers, and a review of published comparisons. It has no probe and no difficulty term.
