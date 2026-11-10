# Critic A challenges (wave 4, step 6)

Run 2026-11-10 (UTC timestamps in `raw/queries.log`). Target: every CLEAN, CLEAN (provisional), and NARROW verdict in `research/positioning/w4/VERDICTS.md`, prioritized as briefed. All queries are new phrasings, not repeats of `QUERIES.md` or `research/corpus-critic-gaps.json`. The cc-1, cc-2, and cc-3 REPORT.md files were read before writing; their results are not re-run here.

Instruments: export.arxiv.org metadata search (`abs:`, `ti:`, `au:`), Semantic Scholar citation lookups, OpenReview v1 `notes/search`, Crossref `query.bibliographic`, arXiv PDF plus pdftotext for full texts. Headless curl, desktop user agent, no email, 3 s spacing, backoff 4 to 40 s (no 429 occurred). Raw responses are in `raw/` (arXiv `a*.xml`, Semantic Scholar `s2c_*.json`, OpenReview `o*.json`, Crossref `c*.json`, full-text extracts `ft_*.txt`). No client IP appears in any raw file (pattern-checked).

Totals: 45 arXiv metadata queries, 11 Semantic Scholar citation lookups (one 404), 4 OpenReview, 4 Crossref, 3 full-text reads (2603.06604, 2605.13414, 2604.26671).

Instrument notes that apply to every entry:

- **OpenAlex not called** (daily budget exhausted; gap G-OA persists).
- arXiv full-text search unavailable (G-FT); every arXiv negative below is title-and-abstract only.
- OpenReview v1 search ORs the terms and returned mostly pre-2024 records; its four queries (`o01` to `o04`, 50 records each) yielded nothing relevant, which is instrument behavior, not evidence of absence.
- Crossref rows (`c01` to `c04`, 25 each; the log column shows 0 because the logger read the wrong JSON key) were screened by title.
- The Tuerlings DOI (10.18653/v1/2026.uncertainlp-main.21) returned 404 on Semantic Scholar; cc-3 found the record under 10.18653/2026.uncertainlp-main.21 with 0 citers.
- Semantic Scholar citer lists for seeds posted after 2026-09 are subject to indexing lag (NeuroSym-Cal, Probe-SD 2609.33290, and 2610.32548 returned 0).

---

## L2 Q11: trained stated confidence on code; effect on discrimination (VERDICTS: CLEAN (provisional))

Queries:

| Instrument | Query | HTTP | Hits |
|---|---|---|---|
| arXiv | abs "confidence" AND "code" AND "reward" AND "calibration" AND "LiveCodeBench" (a01) | 200 | 0 |
| arXiv | abs "Brier" AND "reward" AND "coding" (a02) | 200 | 2 (RLCR 2507.16806; PRDO 2609.38850, MMLU-Pro only) |
| arXiv | abs "express" AND "confidence" AND "fine-tuning" AND "programming" (a03) | 200 | 1, off-topic |
| arXiv | ti "confidence" AND abs "code" AND "trained" AND "unit tests" AND "AUROC" (a04) | 200 | 0 |
| arXiv | abs "self-assessment" AND "coding" AND "calibration" (a05) | 200 | 10, none code-trained |
| arXiv | abs "confidence" AND "RLVR" AND "code" AND "calibration" (a40) | 200 | 3, includes CREDO 2609.34857 |
| arXiv | abs "confidence" AND "probe" AND "fine-tuned" AND "code" AND "verbal" (a42) | 200 | 0 |
| S2 | citations of RLCM 2604.23333 | 200 | 4 (SVR 2607.28457 math; CalibSFT 2609.32470 math and general; Conformal Thinking; 2610.12933) |
| S2 | citations of Probe-SD 2609.33290 | 200 | 0 (lag likely) |
| S2 | citations of CREDO 2609.34857 | 200 | 2 (2610.39927 multi-agent; PRDO 2609.38850) |
| S2 | citations of Barkan 2512.24661 | 200 | 16; 2603.06604 checked in full text (below) |
| OpenReview | "verbalized confidence training code generation execution" (o01) | 200 | 50 returned, none relevant |
| Crossref | "training verbalized confidence code generation calibration" (c03) | 200 | 25, none code-trained (LoVeC, ADVICE are long-form or QA) |

Strongest counter-evidence:

1. **CREDO, arXiv 2609.34857** (concurrent, posted 2026-09), retrieved independently here (a40); cc-1 read the full text: Table 1 reports in-domain code AUROC for trained stated confidence (CREDO 0.850, RLCR 0.815, base 0.690 on DeepCoder, Qwen3-8B). This already occupies "trained stated confidence on code, discrimination reported". No probe arm.
2. **RLCM, arXiv 2604.23333** (COLM 2026 per vault note; vault full text, Table 1): an RLCR-trained verbal arm, trained on math, evaluated on LiveCodeBench at ECE 0.218 against a trained probe readout at 0.051. Only ECE and PCE are reported for code, with no AUROC (the "confidence discrimination" dimension named in Sec 4.1 is not tabulated for LiveCodeBench). So this is a trained-verbal-versus-probe contrast on code, calibration only, with labels the model was not trained on.
3. 2603.06604 ("Know When You're Wrong", FULL TEXT read): SFT raises confidence AUROC from 0.806 to 0.879 on Qwen3-4B, but its seven tasks are BoolQ, CommonsenseQA, HellaSwag, AG News, GSM8K, TriviaQA, and self-evaluation variants (Appendix C). No code. Not an occupant.

**Proposed verdict: NARROW** (agreeing with cc-1). Residual: a trained own-readout and a probe on the same code generations and execution labels, with discrimination reported for both. Closest on each side: CREDO (trained verbal, AUROC, no probe) and RLCM (trained verbal versus probe, ECE only, out-of-domain code). Note that RLCM puts a trained-verbal-versus-probe comparison on code on record, so pivot criterion 3 is closer than VERDICTS states: on calibration the probe wins (0.051 vs 0.218); on discrimination nothing is reported. The recommendation must cite RLCM in L2 Q10 and Q11, not only Q10.

---

## L2 Q1c: controlled probe test (VERDICTS: NARROW)

Queries:

| Instrument | Query | HTTP | Hits |
|---|---|---|---|
| arXiv | abs "probe" AND "code" AND "correctness" AND "difficulty" AND "hidden" (a06) | 200 | 1, off-topic (2605.15454) |
| arXiv | abs "internal states" AND "program" AND "verbalized" (a07) | 200 | 0 |
| arXiv | au Devanbu AND abs "confidence" (a08) | 200 | 5, all known (2512.07404, 2402.02047, 2404.19318, 2510.22614) |
| arXiv | au Spiess AND abs "code" (a09) | 200 | 9, no new probe study |
| arXiv | abs "probe" AND "self-generated" AND "code" AND "confidence" (a39) | 200 | 0 |
| arXiv | abs "probe" AND "baseline" AND "code correctness" (a41) | 200 | 4, all known (2510.02934, 2502.13966, 2606.14530, 2608.14659) |
| OpenReview | "base versus instruct probe verbal confidence code" (o03) | 200 | 50 returned, none relevant |

cc-1 already screened the 14 Semantic Scholar citers of 2512.07404 and the citers of 2608.08266 and 2606.14530; not repeated.

**Challenge failed.** No fetched work runs the supervision-matched, input-only-baseline, within-problem comparison. One sharpening from cc-1 is relevant to the VERDICTS wording: 2611.07876 (Table V, Sec V-C) shows trained methods reaching 0.69 to 0.78 within problem for gpt-oss in distribution, so the "ties at about 0.05" premise holds only for some model and shift conditions. NARROW stands. Gaps: G-FT, G-OA, G-S2 keyword.

---

## L2 Q2a: base versus instruct (VERDICTS: NARROW)

Queries:

| Instrument | Query | HTTP | Hits |
|---|---|---|---|
| arXiv | abs "base" AND "instruct" AND "code" AND "calibration" AND "confidence" (a10) | 200 | 5, none code (DualStake, medical VQA, distillation) |
| arXiv | abs "instruction tuning" AND "probe" AND "correctness" AND "code" (a36) | 200 | 8; one new (2610.20683, syntax circuits, not confidence) |
| S2 | citations of Open the Oyster 2511.02197 | 200 | 2 (2608.22938 Verilog reranking; 2604.16320), neither base versus instruct |

**Challenge failed.** No work measures the probe-minus-stated gap on code across a base and instruct pair. NARROW stands. Gaps: G-FT, G-OA, G-S2 keyword.

---

## L2 Q2b: reasoning versus non-reasoning (VERDICTS: NARROW)

Queries:

| Instrument | Query | HTTP | Hits |
|---|---|---|---|
| arXiv | abs "thinking mode" AND "confidence" AND "calibration" (a11) | 200 | 1, medical |
| arXiv | abs "reasoning" AND "hidden states" AND "verbalized confidence" AND "code" (a12) | 200 | 1 (2512.22245, LLM judges) |
| arXiv | abs "thinking" AND "non-thinking" AND "confidence" (a37) | 200 | 9; relevant known item 2606.30814 (thinking versus non-thinking calibration under accuracy control, in vault) |
| arXiv | abs "reasoning budget" AND "calibration" AND "code" (a38) | 200 | 1 (2607.26865, edge agents) |

Nearest new item: **TRIAGE, arXiv 2605.13414** (concurrent, v1 2026-05-13, v2 2026-11-07; FULL TEXT read). It evaluates models with reasoning enabled and disabled (`enable_thinking`, thinking budget 0, Appendix Table 1 notes) on LiveCodeBench among other sets, but its readout is a prospective allocation plan, not stated confidence or a probe. It does not occupy.

**Challenge failed.** No same-weights reasoning on and off comparison with a probe read under reasoning, on code. NARROW stands. Gaps: G-FT, G-OA, G-S2 keyword.

---

## L3 Q1, Q4, Q5: confidence-routed budgets against random and oracle (VERDICTS: NARROW)

Queries:

| Instrument | Query | HTTP | Hits |
|---|---|---|---|
| arXiv | abs "confidence" AND "random baseline" AND "code" AND "budget" (a13) | 200 | 0 |
| arXiv | abs "uncertainty-aware" AND "test-time scaling" AND "code" (a14) | 200 | 0 |
| arXiv | abs "probe" AND "compute allocation" (a15) | 200 | 7, none code routing |
| arXiv | abs "when to verify" OR "whether to execute" AND "code" (a16) | 200 | 72, noisy (OR precedence), none relevant |
| S2 | citations of SWE-Router 2607.00053 | 200 | 19; screened by title and abstract: StopLoss 2610.25525, Scout 2611.09028, ORACLE 2607.22465, and routing papers; none gates execution budget by elicited verbal or probe confidence with random and label-sorted oracle arms |
| S2 | citations of Kaddour 2602.06948 | 200 | 7, none |

Strongest counter-evidence:

1. **TRIAGE, arXiv 2605.13414** (concurrent; FULL TEXT, Sec 3, Eq. 1 to 3, Appendix Table 13). The model commits a plan that selects, orders, and allocates a token budget across a pool including LiveCodeBench. The plan is scored against measured outcomes as triage efficiency, normalized between a random-permutation reference (10^3 permutations) and a knapsack oracle built from each model's own measured solvability and cost. This is the random-to-oracle comparator design on code, but the gate is a self-written plan, not an elicited confidence score or probe, the budget is generation tokens, not execution, and there is no matched-budget per-item routing.
2. **StopLoss, arXiv 2610.25525** (concurrent, ABSTRACT-ONLY): a trained external monitor aborts SWE agent runs likely to fail, compared with six LLM judges. External monitor, no random or oracle arm stated in the abstract.

**Challenge failed; NARROW stands.** TRIAGE should be added as the closest occupant on the comparator side. It shows that random-to-oracle normalization of self-directed budget allocation on code is published, so the residual must name the gate (elicited verbal or probe confidence) and the unit (execution budget per candidate), not the comparator design. Gaps: G-FT, G-OA, G-S2 keyword; S2 citer lists for 2611.06372 and 2610.30284 are empty because of lag (cc-2).

---

## L3 Q2, Q7: stated confidence update after a shown failing test (VERDICTS: CLEAN (provisional))

Queries:

| Instrument | Query | HTTP | Hits |
|---|---|---|---|
| arXiv | abs "confidence" AND "failing test" (a17) | 200 | 3, fault localization only |
| arXiv | abs "overconfidence" AND "debugging" AND "feedback" (a18) | 200 | 0 |
| arXiv | abs "belief revision" AND "code" AND "language model" (a19) | 200 | 4, none |
| arXiv | abs "metacognition" AND "execution" AND "code" (a20) | 200 | 8; TRIAGE 2605.13414 (prospective, before feedback by design), 2606.20661 (tool-use self-awareness), none post-failure |
| S2 | citations of Barkan 2512.24661 | 200 | 16; LADDER 2610.34737 (self-assessment under noisy feedback, ABSTRACT-ONLY, non-code domains per abstract) is the nearest |
| S2 | citations of Iscan 2606.31511 | 200 | 5; 2609.00854 (placebo-controlled repair, no confidence) |
| OpenReview | "confidence after test feedback code repair calibration" (o02) | 200 | 50 returned, none relevant |

Nearest: **LADDER, arXiv 2610.34737** (in vault by id, ABSTRACT-ONLY here): models' self-assessment under unreliable interaction feedback. It is the closest analogue to the spurious-failure arm, but the abstract names no code or test-execution setting and no per-item confidence revision. **2610.19226** (Agentic Self-Awareness, ABSTRACT-ONLY) probes "responses to a single challenge" of stated feasibility on Terminal-Bench, which is a reconsideration probe in a coding-adjacent harness but concerns task feasibility, not confidence after a failing test.

**Challenge failed.** CLEAN (provisional) stands, with LADDER and 2610.19226 added as near neighbors to read in full before any novelty claim. Gaps: G-FT, G-OA, G-S2 keyword; Resist-and-Update citers remain unrun (cc-2, 429).

---

## L1 Q10: test insufficiency changes calibration or rankings (VERDICTS: CLEAN (provisional))

Queries:

| Instrument | Query | HTTP | Hits |
|---|---|---|---|
| arXiv | abs "label noise" AND "code generation" AND "uncertainty" (a21) | 200 | 0 |
| arXiv | abs "test suite" AND "confidence" AND "calibration" AND "code" (a22) | 200 | 0 |
| arXiv | abs "MBPP+" AND "calibration" (a23) | 200 | 14, none compares base versus plus suites for confidence |
| arXiv | abs "incomplete tests" AND "code" AND "LLM" (a43) | 200 | 5, repair and equivalence only |

**Challenge failed.** cc-3 independently confirms that 2610.11300 uses strengthened suites only and SWE-ABS ranks agents, not estimators. CLEAN (provisional) stands. Gaps: G-FT, G-OA, G-S2 keyword.

---

## L1 Q13: contamination changes calibration or discrimination (VERDICTS: CLEAN (provisional))

Queries:

| Instrument | Query | HTTP | Hits |
|---|---|---|---|
| arXiv | abs "memorized" AND "calibration" AND "language models" AND "confidence" (a24) | 200 | 8; 2609.02899 (contamination and leaderboard order, accuracy), none calibration |
| arXiv | abs "knowledge cutoff" AND "confidence" AND "calibration" (a25) | 200 | 0 |
| arXiv | abs "contamination" AND "uncertainty estimation" (a26) | 200 | 21, off-topic |
| arXiv | abs "contaminated" AND "overconfidence" (a44) | 200 | 3, off-topic |
| Crossref | "data contamination calibration confidence code language models" (c02) | 200 | 25; two titles worth a later look, both outside code confidence: 10.1016/j.ijmedinf.2026.106291 ("Calibration or contamination?", clinical) and 10.1109/tse.2026.3713834 (contamination in code generation, TSE 2026; title only, accuracy framing by title) |

**Challenge failed.** CLEAN (provisional) stands. The TSE 2026 record is a title-only lead (not fetched; Crossref record only) and should be checked for any confidence analysis before the novelty claim is written. Gaps: G-FT, G-OA, G-S2 keyword.

---

## L4 Q3: adequacy of self-written tests versus own confidence (VERDICTS: CLEAN (provisional))

Queries:

| Instrument | Query | HTTP | Hits |
|---|---|---|---|
| arXiv | abs "generated tests" AND "confidence" AND "own" AND "code" (a27) | 200 | 1, off-topic |
| arXiv | abs "test generation" AND "mutation score" AND "self" AND "correctness" AND "LLM" (a28) | 200 | 1 (SPARC, C test generation, no confidence) |
| arXiv | abs "test adequacy" AND "LLM" AND "confidence" (a45) | 200 | 1 (Clotho 2509.17314, known: input-side adequacy) |
| S2 | citations of 2610.32548 | 200 | 0 (lag likely) |
| Crossref | "self-generated unit tests confidence language model code correctness" (c04) | 200 | 25; nearest by title 10.1145/3832204 (misguidance of buggy code in LLM-generated tests), no confidence by title |

**Challenge failed.** CLEAN (provisional) stands. Gaps: G-FT, G-OA, G-S2 keyword, G-FCS (2610.32548 has no indexed citers).

---

## L4 Q2: targeted repair guided by confidence versus regeneration (VERDICTS: NARROW; incidental)

Found via S2 citations of 2606.31511: **arXiv 2609.00854**, "Does Fault Localization Beat a Fresh Attempt? A Placebo-Controlled Study of Test-Guided Code Repair" (concurrent, 2026-09; ABSTRACT-ONLY). Spectrum-based localization plus infilling loses to blind resampling at matched attempt count (3:40, p = 3.0 x 10^-9) across three 26-32B models and three benchmarks, with a random-span placebo. No confidence signal guides the edit.

**Challenge failed; NARROW stands but the residual narrows.** Matched-budget targeted repair versus regeneration with a placebo span is now published for test-guided localization, with a negative result. The remaining residual is only that the localization comes from the model's own per-requirement confidence. This also raises the prior that such a variant loses. Add 2609.00854 as the closest occupant on the matched-budget side (replacing or joining Olausson and Iscan).

---

## F Q1: metrology-proper terms applied to LLM confidence (VERDICTS: CLEAN (provisional))

Queries:

| Instrument | Query | HTTP | Hits |
|---|---|---|---|
| arXiv | abs "measurand" AND "language model" (a30) | 200 | 0 |
| arXiv | abs "metrology" AND "large language models" (a31) | 200 | 4 (TRACE 2605.03838, known; 2601.21678 Allan deviation on text embeddings, not confidence) |
| arXiv | abs "traceability" AND "measurement uncertainty" AND "machine learning" AND "calibration" (a32) | 200 | 1, 2020, cyber-physical |
| arXiv | abs "Expression of Uncertainty in Measurement" AND "language model" (a33) | 200 | 0 |
| arXiv | abs "measurement instrument" AND "confidence" AND "LLM" (a34) | 200 | 3, none |
| arXiv | abs "metrological" AND "evaluation" AND "AI" (a35) | 200 | 9; 2604.26671 (below); 2407.16711 "Benchmarks as Microscopes: A Call for Model Metrology" (2024, benchmarks, not confidence); 1911.01875 "Metrology for AI" (2019, outside window, benchmarks) |
| OpenReview | "metrology measurand language model confidence" (o04) | 200 | 50 returned, none |
| Crossref | "metrology measurand large language model confidence uncertainty" (c01) | 200 | 25, none applying VIM or GUM to LLM confidence |

Strongest counter-evidence: **arXiv 2604.26671**, Zabolotnii, Holinko, and Antonenko, "From Black-Box Confidence to Measurable Trust in Clinical AI: A Framework for Evidence, Supervision, and Staged Autonomy" (preprint only, v1 2026-04-29, cs.CL; FULL TEXT read, `raw/ft_2604.26671.txt`).

- Section 1 states that "The International Vocabulary of Metrology (VIM) defines measurand, measurement uncertainty, and metrological traceability" and that "these concepts apply directly to clinical AI". It invokes the GUM for uncertainty propagation through a multi-stage chain.
- Section 10 defines Calibration Error as "deviation between the model's stated confidence and its actual accuracy" and calls it "a direct analog of the systematic error of a measuring instrument" requiring recalibration. Section 11 maps evaluation to calibration against reference standards per GUM and ISO 17025.
- It is a conceptual position paper with no experiments, no code, and no internal-reference readout. It was previously visible only as a mention inside the TRACE note and was never screened.

**Proposed verdict: OCCUPIED for the vocabulary claim, at conceptual depth.** F Q1 becomes OCCUPIED for metrology-proper terms (VIM, measurand, GUM, traceability) applied to LLM stated-confidence calibration error. A residual would be only an operationalized, empirical measurand-readout decomposition, which is F Q2 and Q3 territory, already OCCUPIED (union) and OCCUPIED (effective). Whole F stays OCCUPIED and the framing is "used", now including metrology proper. Exposition that uses this vocabulary must cite 2604.26671 (and TRACE 2605.03838).

---

## Verdicts not challenged (budget)

L1 Q2, Q3, Q4, Q5 (estimator sub-part), Q6, Q11; L2 Q3, Q4, Q8, Q9, Q10, Q12, Q13; L4 Q1. cc-3 covered L1 Q3 and Q4. These were not attacked with new queries in this pass.

## Summary of proposed changes

| Verdict | VERDICTS | Proposed | Basis |
|---|---|---|---|
| L2 Q11 | CLEAN (provisional) | NARROW | CREDO 2609.34857 Table 1 (code AUROC, trained verbal); RLCM 2604.23333 Table 1 (trained verbal versus probe on LiveCodeBench, ECE only) |
| F Q1 (metrology-proper) | CLEAN (provisional) | OCCUPIED (conceptual) | 2604.26671 Sec 1, Sec 10, FULL TEXT |
| L3 Q1, Q4, Q5 | NARROW | NARROW, residual restated | TRIAGE 2605.13414 random-to-oracle normalization on LiveCodeBench, FULL TEXT |
| L4 Q2 | NARROW | NARROW, residual shrinks | 2609.00854 placebo-controlled matched-budget localization versus resampling, ABSTRACT-ONLY |
| L2 Q1c, Q2a, Q2b; L3 Q2/Q7; L1 Q10, Q13; L4 Q3 | as listed | challenge failed | queries above; gaps G-FT, G-OA, G-S2 keyword |
