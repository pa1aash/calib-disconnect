# Verdicts per candidate and component (wave 4)

Run date 2026-11-10. Definitions are those of `docs/s3/POSITIONING_BRIEF_R1.md` section 4: OCCUPIED, OCCUPIED (union), NARROW (with a one-sentence residual and the closest work on each side), CLEAN, and CLEAN (provisional). Evidence comes from full texts, cited by section or table in the dossiers (`dossiers/`, index in `dossiers/INDEX.md`) and the six depth-investigation notes (`research/notes/interim-report-*.md`, committed positions reconciled in `research/comparisons.md`). Status tags follow A23. "Concurrent" means first posted after 2026-05-10; that window is a proposal for the operator to confirm.

**Instrument gaps that bear on every CLEAN (provisional) verdict below** (`INSTRUMENTS.md`):

- **G-FT:** arXiv full-text search failed validation (searchtype=ft ignored; the full-text host is off the allowlist).
- **G-OA:** OpenAlex full-text search is partial (1 of 2 positives), and the OpenAlex daily budget was exhausted at about 05:05 IST, so later OpenAlex negatives are gaps.
- **G-S2:** Semantic Scholar keyword search returned HTTP 429 throughout; citations and lookups worked, with intermittent 429.
- **G-AX:** the arXiv export API returned HTTP 429 to several step 5 queries.
- **G-OR:** OpenReview forum pages and PDFs are behind a browser challenge; only v1 `notes/search` works.
- **G-FCS:** forward-citation screens of some close occupants were partial (listed per verdict).

No CLEAN verdict in this file is unconditional. Under R1 section 4, every body-text claim is at best CLEAN (provisional) in this wave.

## Summary

| Candidate | Whole-candidate verdict | Strongest surviving residual |
|---|---|---|
| L1 | OCCUPIED (union) for the comparison; NARROW for the protocol | a three-control sensitivity protocol (estimator set, augmented-test oracle swap, per-model release split) on identical generations, including a probe family |
| L2 | OCCUPIED for the uncontrolled headline; NARROW for the controlled and factorial versions | a supervision-matched, within-problem comparison of probe, trained and zero-shot own readouts, and sampling agreement on self-generated code, crossed with base and instruct pairs and a same-weights reasoning toggle |
| L3 | NARROW | routing by elicited verbal or probe confidence against random and label-sorted oracle at matched budget on unmodified execution labels; and stated-confidence update after a shown failing test (CLEAN (provisional)) |
| L4 | NARROW (line level OCCUPIED) | per-test-group confidence as failing-requirement localization; test adequacy versus own confidence (CLEAN (provisional)) |
| F | OCCUPIED as a framing | none as a contribution; vocabulary usable as exposition |

## L1. Execution-graded measurement foundation

| Q | Component | Verdict | Evidence and residual |
|---|---|---|---|
| 1 | Four or more families (sampling, token, stated, probe) against execution labels | **OCCUPIED (union)** | NeuroSym-Cal (Findings ACL 2026; Sec 4.2) covers token, P(True) and self-verification, sampling agreement, and multicalibration, with no probe; Campos et al. 2611.07876 (concurrent; Sec IV, Table II) covers output confidence, sampling (EigenScore), hidden-state probes, and causal localization, with no verbal numeric readout. Together they cover all four families on different problems, which is the A20 union case. The union also holds with published works alone: Ribeiro et al. (probe, verbal, likelihood) plus NeuroSym-Cal (token, verbal, sampling). |
| 2 | Three or more families, two or more scales, three or more benchmarks | **NARROW** | Code-MUE 2607.12273 (concurrent) spans 8 models and 4 benchmarks with one family; NeuroSym-Cal spans 3 models, 2 scales, 3 benchmarks with no probe. Residual: the same breadth with all four families on identical generations. Closest: NeuroSym-Cal and Code-MUE. |
| 3 | Release-date split as a contamination control for calibration | **NARROW** | NeuroSym-Cal holds out a per-model post-cutoff LiveCodeBench subset (Sec 4.1); Tuerlings and Valdenegro-Toro (UncertaiNLP 2026; Sec 3.1) use one shared post-cutoff window, verbal only; 2512.08810 uses release_v6 as a leakage control. Residual: a pre- versus post-cutoff contrast of calibration for all four families, including a probe. |
| 4 | Label independence | **NARROW** | Tuerlings Sec 3.3 freezes code before elicitation; Liu et al. 2609.25938 (concurrent) shows on text-to-SQL that the execution oracle sets the reported risk in 16 of 16 cases. Residual: label independence as a tested factor for code across families (same-oracle versus independent-oracle rankings). Reason code differs: hidden tests drive both the label and test-based agreement scores; 2605.09023 Table 6 shows that fuzz inputs seeded from benchmark tests raise agreement AUROC by 0.014 to 0.087 over seed-free inputs (Critic B). |
| 5 | Ranking changes with the calibration estimator | **NARROW** | ECE and AUROC decouple on code (Tuerlings Table 1: lowest ECE 0.013 with AUROC 0.491). No code study compares equal-mass, debiased, or smooth ECE estimators: CLEAN (provisional) for that sub-part (G-FT, G-OA, G-S2). |
| 6 | Calibration separated from discrimination; recalibration as a control | **OCCUPIED** (token level) / **NARROW** (across families) | 2610.11300 (concurrent; Sec 6, Table 5) applies Platt and isotonic maps to token readouts; Gros and Devanbu 2512.24560 (preprint; Tables 3-4) do so at line level. Residual: recalibration as a control across all four families at program level. |
| 7, 8 | Test-free agreement; semantic entropy with execution or symbolic clustering | **OCCUPIED** | Sharma and David 2502.11620 (symbolic-equivalence clustering), Code-MUE 2607.12273, Functional Entropy 2605.28500, 2605.09023 (semantic distance), 2603.27098 (ensemble semantic entropy). |
| 9 | Benchmarks with release windows used for calibration | **OCCUPIED** | LiveCodeBench windows used for calibration by Tuerlings and NeuroSym-Cal. |
| 10 | Test insufficiency changes calibration or rankings | **CLEAN (provisional)** | Nearest: EvalPlus (accuracy only), 2505.13553 Sec 5.2.2 (guarantee tightness versus test count), 2609.25938 (SQL). Gaps: G-FT, G-OA, G-S2, G-AX. |
| 11 | Subgroup calibration; multicalibration changes rankings | **OCCUPIED** (token likelihood) / **NARROW** (across families) | Campos et al. 2512.08810 (preprint) multicalibrates token likelihood on code. |
| 12 | Self-judgment or judge scores as confidence | **OCCUPIED** | 2610.11300 (LLM judge family), OPENIA 2501.12934 (LLM-as-judge baseline), NeuroSym-Cal (self-verification). |
| 13 | Contamination changes calibration or discrimination | **CLEAN (provisional)** | No fetched work compares pre- and post-cutoff calibration. Gaps: G-FT, G-OA, G-S2, G-AX. |

**Whole L1:** the comparison is OCCUPIED (union); the protocol (Q3, Q4, Q5, Q10, Q13 together, on identical generations with a probe family) is NARROW, with Q10 and Q13 CLEAN (provisional). Closest: NeuroSym-Cal, Tuerlings, 2610.11300, Liu 2609.25938.

## L2. Locating the disconnect

| Q | Component | Verdict | Evidence and residual |
|---|---|---|---|
| 1 | Probe versus stated confidence, token probability, and sampling on the same problems, execution labels, uncontrolled | **OCCUPIED** (probe vs verbal, Ribeiro alone) / **OCCUPIED (union)** (with sampling, Ribeiro plus Campos) | Ribeiro et al. 2512.07404 (ICSE 2026; Sec 4.2.1): LAT probe beats 7-level and True/False verbal and likelihood readouts on 4 instruct models, +13.3 to +29.0 pp (BCB) and +8.7 to +26.2 pp (HE); Campos 2611.07876 adds sampling and AUROC (no verbal numeric). |
| 1c | The same comparison, controlled: supervision-matched own readouts, input-only baselines, within-problem scoring, self-generated samples | **NARROW** | Residual: same-sample comparison of probe, trained own-readout on the same execution labels, prompt-only and candidate-text-only baselines, and verbal numeric and categorical confidence, scored pooled and within problem. Closest: Ribeiro (probe vs zero-shot verbal; correct class is the human reference, incorrect class is other models' failures, Sec 4.1.1) and Campos 2611.07876 (pooled vs within, no verbal). Ribeiro RQ2 (Sec 5.1 to 5.2) already ranks each model's own samples within a task against zero-shot verbal confidence, with few significant differences; it has no trained own-readout and no input-only baseline. The within-problem code comparisons tie: Campos 0.620 vs 0.629; Miglani et al. 2609.36783 0.677 vs 0.703 (interim note, probe-confound locus). |
| 2a | Base versus instruct pairs | **NARROW** | Code side: 2610.11300 Sec 5.5 (token readouts, two pairs, MBPP+: DeepSeekCoder AUC 0.4391 to 0.5654, dAUC +0.1263, CI [0.0447, 0.2089]); Tahimic and Cheng 2510.02917 Sec 5.5 (Gemma-2-2b base and instruct, SAE features, no verbal). NLP side: Miao and Ungar 2603.25052 (probe vs verbal, base and instruct, non-code). Residual: the probe-minus-stated-confidence gap on code for base versus instruct of the same model, on identical generations. This revises the provisional CLEAN of `L2_OCCUPANT.md`. |
| 2b | Reasoning versus non-reasoning | **NARROW** | Campos 2611.07876 prefills gpt-oss-20b so it answers without reasoning (Sec V-A); Barkan et al. 2512.24661 toggles reasoning budgets for in-advance verbal confidence; Open the Oyster 2511.02197 compares DeepSeek-R1 with V3 (different weights), verbal only. Residual: same-weights reasoning on and off with the probe read under reasoning. |
| 3 | Elicitation format as a factor | **OCCUPIED** (within verbal, on code) / **NARROW** (format by readout family) | Tuerlings Table 1 (three verbal formats, code); Ghosh et al. 2610.25846 (cross-format, non-code). Residual: whether the probe-verbal gap depends on format. |
| 4 | Where the gap arises (base, tuning, reasoning) on code | **NARROW** | Closest: Miao and Ungar (gap present in base, NLP) and 2610.11300 (code, token level). |
| 5, 6, 7 | Probes for code correctness; transfer; other white-box readouts | **OCCUPIED** | OPENIA 2501.12934, AutoProbe 2510.02934, 2602.09924, 2606.14530, Klassert thesis 2609.13975, 2611.07876 (distribution shift), 2510.02917 (SAE), 2609.36783 and ACL SRW 2026 (diffusion models). |
| 8 | Calibration across post-training stages with execution labels | **NARROW** (weak residual) | Stage decomposition exists on math only (2607.13753 Table 1). The A21 code reason (anti-aligned base confidence; RLVR on code uses the label's own signal) is a hypothesis, not demonstrated. |
| 9 | Extended reasoning and stated confidence on code | **NARROW** (post-hoc stated) / **CLEAN (provisional)** (trace signals beat the final number, on code) | Open the Oyster and Barkan on the code side; Yoon et al. 2505.14489 and 2510.10409 outside code. Gaps: G-FT, G-OA, G-S2, G-AX. |
| 10 | Probing reasoning models vs stated confidence, reasoning on, code | **NARROW** | RLCM 2604.23333 (probe-read ECE 0.051 vs trained verbal 0.218 on LiveCodeBench, ECE only); Probe-SD 2609.33290 (non-code). |
| 11 | Trained stated confidence on code; effect on discrimination | **NARROW** | CREDO 2609.34857 (concurrent; Table 1) trains stated confidence with execution labels on Qwen3-8B (DeepCoder): in-domain code AUROC 0.850 vs untrained base 0.690, RLCR 0.815; no probe arm. EpiCaR 2601.06786 (Table 4) reports MBPP AUROC 0.538 out of domain. NLP: Probe-SD AUROC .825 to .928 vs probe .948. Residual: trained stated confidence against a probe on the same code generations, in AUROC, within problem. Found by the step 8 gap fill (`parts/cc-1/REPORT.md`); this revises the earlier CLEAN (provisional). |
| 12 | Causal intervention on stated confidence | **NARROW** | Code causal work targets output correctness (2510.02917 Sec 5; 2609.36783 steering null); NLP work targets stated confidence (Miao and Ungar Table 4; Kumaran et al. 2603.17839). |
| 13 | Pooled versus within-problem discrimination | **NARROW** | Campos 2611.07876 reports both for probe and output confidence on two models; 2610.05572 decomposes difficulty for agent probes. Residual: verbal and per-candidate sampling readouts, base and instruct, reasoning on. |

**Pivot criteria (R1 section 6):**

1. **A20 union:** not triggered. No three works together cover probe, stated, and sampling readouts on code with both base-instruct pairs and a reasoning factor; the stated-confidence side and the factor side never meet.
2. **A21 residual:** survives only for the controlled test (Q1c) and the factorial versions (Q2a, Q2b, Q4). A headline "probes beat verbal confidence on code" fails A21.
3. **A14 trained stated confidence closes the gap:** not triggered on code, but the threat is now concrete: CREDO raises code AUROC of stated confidence from 0.690 to 0.850 without a probe comparison. NLP evidence says training closes most of the discrimination gap and recalibration cannot (monotone maps leave AUROC fixed). The strongest version must include a trained own-readout arm.
4. **A15 causal localization on code:** not triggered.

**Whole L2:** NARROW, conditional on the controlled test being the headline.

## L3. Verification utility

| Q | Component | Verdict | Evidence and residual |
|---|---|---|---|
| 1, 4, 5 | Confidence-routed execution or sampling budgets against random and oracle | **NARROW** | Positives use other signals: SWE-Verifier 2610.30284 (trained verifier, no random arm; its "Oracle@3" is best-of-three), Heteroskedastic signals 2606.15841 (logit proxy, random and threshold and oracle arms, MBPP with 10% injected label noise, Table 1), SWE-Router 2607.00053 (beats a random band). Negatives use other budget units: Give-Up 2611.06372 (pass-rate priors), 2608.14659 (regeneration). TRIAGE 2605.13414 (concurrent; full text, Sec 3, Eq. 1 to 3) already normalizes self-directed token-budget allocation on LiveCodeBench between a random-permutation reference and a knapsack oracle, so the comparator design is published. Residual (restated after Critic A): elicited verbal or probe confidence as the gate, execution budget per candidate as the unit, unmodified execution labels, matched-budget random and label-sorted oracle. |
| 2, 7 | Stated confidence updates after a shown failing test; tracks repair; valid versus spurious failures | **CLEAN (provisional)** | Nearest and not occupying: Kaddour et al. 2602.06948 (tests never observed), Barkan Exp. 3, Not-One-Belief 2610.35694 and Resist-and-Update (non-code), Iscan 2606.31511 (no confidence). Gaps: G-FT, G-OA, G-S2, G-AX; forward screens of 2611.06372, 2610.30284, 2608.14659 not run (G-FCS). |
| 3 | Selective prediction with coverage and risk on code | **OCCUPIED** | CodeRefuser 2605.17029 (Table 1, Figs 2-3); 2505.13553; 2605.19369 (selective accuracy over 70% at 80% coverage on MBPP+, Sec 4.1). |
| 6 | Uncertainty or abstention for repository agents | **OCCUPIED** | Kaddour et al. 2602.06948 alone suffices (Critic B); also SWE-Verifier, SWE-Router, and failure prediction for coding agents 2611.08285, 2610.35971, 2610.05572. |

**Whole L3:** NARROW. It is a credible secondary analysis on L1 and L2 generations, not a spine.

## L4. Per-requirement confidence

| Q | Component | Verdict | Evidence and residual |
|---|---|---|---|
| 4 | Line, token, edit, or step localization | **OCCUPIED** | Gros and Devanbu 2512.24560 (preprint; Tables 3-4: Qwen line-level BSS 0.29 probe vs -0.72 verbal; for the Qwen generator the probe reads the generator's own states, and Table 4 compares all four families on the same code at line level, per Critic B, correcting dossier 2512.24560); FLARE 2606.03852 (Table 4); 2607.05188 (agent steps); 2504.14640 (PtTrust, line level). |
| 1 | Per-test-group confidence as failing-requirement localization | **NARROW** | Residual: localization by test group with no patch oracle. Closest: Gros and Devanbu (line) and 2607.05188 (program-version partial correctness). |
| 2 | Targeted repair guided by confidence versus regeneration | **NARROW** (residual shrinks) | FLARE and TokenRepair 2511.18001 (targeted, no matched-budget arm); Olausson 2306.09896 and Iscan 2606.31511 (matched budget, no confidence); 2609.00854 (concurrent, ABSTRACT-ONLY; found by Critic A): spectrum-based localization plus infilling loses to blind resampling at matched attempts with a random-span placebo. Residual: only that localization comes from the model's own per-requirement confidence, and the prior that it wins is now lower. |
| 3 | Adequacy of self-written tests versus own confidence | **CLEAN (provisional)** | 2610.32548 measures adequacy without confidence. Gaps: G-FT, G-OA, G-S2; only 4 forward citers of 2512.24560 screened (G-FCS). |

**Whole L4:** NARROW, and it needs an unrun pipeline (`src/v4_dprc` is frozen legacy code) plus an operator scope decision.

## F. Measurement-instrument framing

| Q | Component | Verdict | Evidence |
|---|---|---|---|
| 1 | Metrology vocabulary for LLM confidence | **OCCUPIED** | Measurement-validity and psychometric vocabulary: Ghosh et al. 2610.25846; 2603.14893; 2604.15702; 2604.22215; 2604.17707. Metrology-proper terms, at conceptual depth: Zabolotnii, Holinko, and Antonenko 2604.26671 (preprint, April 2026; full text, Sec 1 applies VIM and GUM terms such as measurand and traceability to clinical AI; Sec 10 treats stated-confidence calibration error as an instrument's systematic error), found by Critic A; TRACE 2605.03838 uses GUM, VIM, and ISO 17025 vocabulary for agentic AI trust metrics. This revises the earlier CLEAN (provisional) for metrology-proper terms. |
| 2 | Bias, resolution, noise decomposition versus Brier decomposition | **OCCUPIED (union)** | Yates covariance decomposition (Vieira 2603.05544), Charpentier and Fernandes Machado 2603.15232 (reliability, grouping, uncertainty), Ghosh cross-format Spearman 0.126 / -0.069 / 0.247. |
| 3 | A24 residual quantity | **OCCUPIED** (effective) | The only candidate beyond Murphy is a format-by-item variance component, occupied as a statistic in general NLP (Mahaut et al. 2406.13415; Ghosh) with no stated code reason (fails A21). |
| 4 | meta-d' and metacognitive efficiency | **OCCUPIED** | Servajean 2603.29693; Cacioli 2603.25112; 2603.14893. M-ratio is undefined for open-ended generation. |

**Whole F:** OCCUPIED. The framing is **used**, including metrology-proper vocabulary (2604.26671), and is not contested in fetched work.

## Occupant status (A23) for verdict-bearing works

| Work | Status |
|---|---|
| Ribeiro et al. 2512.07404 | published, ICSE 2026 |
| NeuroSym-Cal | published, Findings of ACL 2026 |
| Tuerlings and Valdenegro-Toro | published, UncertaiNLP workshop 2026 |
| Gros and Devanbu 2512.24560 | preprint only (December 2025) |
| Campos et al. 2611.07876; 2610.11300; 2609.25938; 2610.30284; CREDO 2609.34857; 2611.06372; 2606.15841 | concurrent |
| 2510.02917; 2512.08810; 2502.11620; 2505.14489 | preprint only |
| CodeRefuser 2605.17029 | concurrent |
| Code-MUE 2607.12273; 2605.19369 | published (Critic B) |

Verdicts that rest on concurrent works: L1 Q1 (union with 2611.07876), L1 Q4 (2609.25938), L2 Q1 (sampling side), L2 Q2a (2610.11300), L2 Q13, L3 Q1. If the operator rules concurrent works out of scope, L1 Q1 stays OCCUPIED (union) through published works, L2 Q11 returns to CLEAN (provisional) (CREDO is concurrent), L2 Q13 moves toward CLEAN (provisional), and L3 Q3 rests on 2505.13553; no verdict that the recommendation rests on becomes OCCUPIED.

## Challenge resolutions (W4 step 6)

Critic A (`parts/critic-A/CHALLENGES.md`) ran 45 arXiv metadata queries, 11 Semantic Scholar citation lookups, 4 OpenReview and 4 Crossref queries, and 3 full-text reads against the CLEAN and NARROW verdicts. Critic B (`parts/critic-B/CHALLENGES.md`) re-read the full texts of every occupant behind an OCCUPIED verdict. The step 8 gap fill (`parts/cc-1/`, `cc-2/`, `cc-3/` REPORT.md) ran six targeted searches in parallel.

| Verdict | Challenge | Resolution |
|---|---|---|
| L2 Q11 trained stated confidence on code | Critic A and cc-1: CREDO 2609.34857 Table 1 reports code AUROC for trained stated confidence; RLCM 2604.23333 Table 1 sets trained verbal against a probe on LiveCodeBench in ECE | **Accepted.** CLEAN (provisional) to NARROW. Pivot A14 not triggered (no same-sample AUROC comparison with a probe), but closer than first stated. |
| F Q1 metrology-proper vocabulary | Critic A: 2604.26671, full text | **Accepted.** CLEAN (provisional) to OCCUPIED. The framing is "used" including metrology proper. |
| L3 Q1, Q4, Q5 routing | Critic A: TRIAGE 2605.13414, full text | **Accepted as restatement.** Stays NARROW; the residual names the gate and the execution-budget unit, not the comparator design. |
| L4 Q2 targeted repair | Critic A: 2609.00854, abstract only | **Accepted as restatement.** Stays NARROW with a smaller residual. The abstract-only basis is noted. |
| L2 Q1c, Q2a, Q2b; L3 Q2/Q7; L1 Q10, Q13; L4 Q3 | Critic A: new queries found no occupant | **Challenges failed; verdicts stand.** Leads to read before any novelty sentence: 2610.19226 (L3 Q2/Q7, abstract only) and Crossref record 10.1109/tse.2026.3713834 (L1 Q13, title only). LADDER 2610.34737 was later checked in full text (vault note `ladder-diagnosing-domain-level-self-assessment-under-noisy-feedback`, Sec 3): it measures domain-level self-assessment from simulated user feedback (confirm, correct, or unclear) on non-code QA domains, with no executed tests, so it is adjacent and does not occupy L3 Q2/Q7. |
| L2 Q1 label | Critic B: the four-family uncontrolled claim needs Ribeiro plus Campos | **Accepted.** OCCUPIED (probe versus verbal, Ribeiro alone) and OCCUPIED (union) with sampling. |
| L2 Q1c evidence | Critic B: Ribeiro RQ2 ranks own samples within task against verbal | **Accepted.** Added to the evidence; residual unchanged (no trained own-readout, no input-only baseline). |
| L1 Q1 union | Critic B: holds; Draft C: holds with published works alone | **Accepted.** Concurrency no longer affects L1 Q1. |
| L1 Q4 evidence | Critic B: 2605.09023 Table 6 (test-seeded fuzzing raises agreement AUROC by 0.014 to 0.087) | **Accepted.** Added as code-side evidence that label and score share tests. |
| L4 Q4 and dossier 2512.24560 | Critic B: Gros and Devanbu probes read the generator's own states; Table 4 compares four families at line level | **Accepted.** Dossier corrected. |
| L3 Q6 | Critic B: Kaddour 2602.06948 alone suffices | **Accepted.** OCCUPIED (union) to OCCUPIED. |
| Status tags | Critic B: CodeRefuser concurrent; Code-MUE and 2605.19369 published | **Accepted.** |
| Critic B on all OCCUPIED verdicts | No narrower surviving residual found that passes A21 for any OCCUPIED row | **No OCCUPIED verdict changes.** |
| L1 Q3, Q4, Q10, Q13 (cc-3) and L3 routing and update (cc-2) | Targeted adversarial searches | **No overturning source**; verdicts stand within the listed gaps. |
