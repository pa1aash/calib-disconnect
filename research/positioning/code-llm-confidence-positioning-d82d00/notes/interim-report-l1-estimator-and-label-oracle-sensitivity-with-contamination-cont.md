---
title: Interim report — l1-estimator-and-label-oracle-sensitivity-with-contamination-control
id: interim-report-l1-estimator-and-label-oracle-sensitivity-with-contamination-cont
tags:
- code-llm-confidence-positioning-d82d00
- locus-l1-estimator-and-label-oracle-sensitivity-with-contamination-control
created: '2026-11-10T08:41:43.426080Z'
status: draft
type: interim
deprecated: false
summary: L1 comparison is OCCUPIED (union); defensible residual is a sensitivity protocol
  (estimator, augmented-test oracle swap, per-model release split); Q3/Q4/Q5 NARROW,
  Q10/Q13 CLEAN (provisional)
---

# Interim report: l1-estimator-and-label-oracle-sensitivity-with-contamination-control

**Locus question:** Whether method rankings change with the calibration estimator, the test-label oracle, and release-date contamination splits; decides L1 (Q3, Q4, Q5, Q6, Q10, Q11, Q13).
**Flavor:** dialectical

## What the corpus already said

The width sweep had both sides but no study that crosses them. Estimator-fragility evidence: [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]]; oracle-fragility evidence: [[certified-against-which-oracleexecution-labels-set-the-reported-riskof-conformal]] and [[is-your-code-generated-by-chatgpt-really-correct-rigorous-evaluation-of-large-la]]. Standard-practice code papers: [[code-is-more-than-text-uncertainty-estimation-for-code-generation]], [[functional-entropy-predicting-functional-correctness-in-llm-generated-code-with]], [[multicalibration-for-llm-based-code-generation]], [[240202047-calibration-and-correctness-of-language-models-for-code]] (note body ~950 words, treated as ABSTRACT-LEVEL: no section cites taken from it). Instrument caveat: arXiv full-text search failed, OpenAlex exhausted, S2 keyword search 429; every "no study does X" below is an instrument gap, not a zero.

## What the new sources say

Budget use: 1 new fetch ([[identity-or-prompt-noise-a-calibrated-invariance-audit-of-llm-code-generation]], from the S2 citation screen; not read in depth, not load-bearing, treat as unscreened). Three further S2-surfaced items were already in the vault and were read in full: [[ensemble-based-uncertainty-estimation-for-code-correctness-estimation]], [[using-semantic-distance-to-estimate-uncertainty-in-llm-based-code-generation]], [[towards-functional-correctness-of-code-models-with-selective-generation]]. I also re-read the five corpus occupants in full text.

**Tuerlings and Valdenegro-Toro, UncertaiNLP 2026 (published workshop, pp 328-355) [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]].** Six instruct coders (Qwen2.5-Coder 7B/32B, CodeLlama 7B/34B, DeepSeek-Coder 6.7B/33B), 365 LiveCodeBench v6 problems in one shared window 2024-09-19..2025-04-30 (Sec 3.1), code frozen before elicitation "so ... correctness labels are determined independently of any confidence estimation" (Sec 3.3), three verbal formats (Direct, CoT, Linguistic). Sec 3.5 metrics: ECE with ten equal-width bins, NCE, AUROC, AUACC, PRR, Platt only "as a post-hoc diagnostic" (App E). Table 1: lowest ECE 0.013 (CodeLlama-7B Linguistic) has AUROC 0.491; highest AUROC 0.841 (Qwen-32B Linguistic) has ECE 0.216. Sec 4.3: Linguistic has lowest ECE in 4 of 6 models but 3 of those 4 cells are collapsed; Sec 4.6: 8 of 18 cells collapsed (CodeLlama-7B Linguistic puts 359/365 at confidence 10). Table 2 (PRR): Direct is best for 4 of 6 models. Sec 4.4: parse-repair vs fallback-50 moves CodeLlama-7B CoT ECE 0.680 to 0.445 with AUROC 0.556 to 0.546. This is the only code study in the vault that shows a within-family method ranking change by metric (ECE vs AUROC/PRR). It does not test estimator variants of ECE (equal-mass, debiased, smooth), has one shared window rather than per-model cutoff splits, and no contamination-vs-post-cutoff contrast (no pre-cutoff comparison group, so it cannot say contamination changes calibration). Its own Related Work states "no existing work compares black-box verbalized elicitation strategies across multiple coding-specialized LLMs on a shared temporally filtered window", i.e. it occupies "release-window as calibration control" for the verbal family only.

**Liu et al., arXiv 2609.25938 (preprint, 22 Sep 2026; text-to-SQL) [[certified-against-which-oracleexecution-labels-set-the-reported-riskof-conformal]].** Abstract/Sec 1 (full text read): swapping the shipped database for the distilled multi-instance suite raises conformal held-out risk "2.73 to 10.23 points"; "Every execution-consistency score looks better under the labels of the oracle that built its clusters, in 16 of 16 score-by-checkpoint combinations, while likelihood scores that read no oracle never do"; expert-labeled risk 20.0 and 17.2 points at nominal 0.10; "A consistency score should be evaluated under an oracle that did not build it." This is the strongest oracle-dependence evidence and it names label independence as a design requirement, but it is SQL, four SQL-specialist checkpoints, conformal risk and execution-consistency scores only. It occupies the principle (label independence) in SQL; it does not cover code generation, verbal/probe families, or ranking across families.

**Rathnasuriya and Yang, arXiv 2610.11300 [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]].** HumanEval+, MBPP+ (EvalPlus-strengthened suites) and BigCodeBench, four 7-8B instruct models. Table 3: best token/sampling uncertainty AUC 0.598-0.696. Table 5 (Sec 6): Platt/isotonic cut Brier (e.g., 0.459 to 0.248 for one model) while Brier Skill Score stays ~0.001. This is the only code paper in the vault that separates mapping from information via BSS (answers Q6 for token-level uncertainty). It uses strengthened suites but does not compare base-test vs plus-test labels.

**Selective generation, arXiv 2505.13553 [[towards-functional-correctness-of-code-models-with-selective-generation]].** Sec 5.2.2 "Benefit of Fuzzing": the FDR-CE guarantee tightens and FDR-CE falls "as the number of unit tests for evaluation increases" and labels are fuzz-generated unit tests that "play a role of the true label". This is label-quantity sensitivity of a guarantee, not of a method ranking. Closest code-side partial occupant for Q10, narrow.

**Wei et al. 2603.27098 [[ensemble-based-uncertainty-estimation-for-code-correctness-estimation]] and Semantic-distance 2605.09023 [[using-semantic-distance-to-estimate-uncertainty-in-llm-based-code-generation]].** Both grade on LiveCodeBench official hidden tests (v2; pass rate or pass@1) with generated-test or sample-based estimators; neither reports ECE, a release split, or an oracle swap. They are standard-practice evidence for side B and for Q7/Q8.

**Corpus side B in full text.** [[code-is-more-than-text-uncertainty-estimation-for-code-generation]] (arXiv 2606.09577, Sec on metrics): labels are official hidden-test pass@1, "This distinction is critical, since otherwise the functional signal would be trivially perfect by construction", and "We do not report Brier Score or ECE: post-hoc rank-normalized scores have no meaningful absolute calibration"; it uses self-generated tests as a signal and the official suite as label, so it practices label independence without testing it. [[functional-entropy-predicting-functional-correctness-in-llm-generated-code-with]] (2605.28500): five closed models, LiveCodeBench/MultiPL-E/LiveSQLBench, AUROC primary, ECE and Brier in App; App text: "calibration results are broadly consistent with the AUROC findings", so no estimator-driven reversal reported; its limitation section concedes test-based labels are "an approximation". [[multicalibration-for-llm-based-code-generation]] (2512.08810): token-likelihood only, LiveCodeBench release_v6 used as a leakage-minimizing dataset (whole 1055 problems, May 2023 to Apr 2025), ECE (binned, M bins) and BSS, with group calibrators lifting BSS; labels from benchmark unit tests; no release split. [[251224560-localized-calibrated-uncertainty-in-code-language-models-full-text]] (2512.24560): labels from minimal repair patches verified with hidden tests, ECE flagged as "misleadingly low" under "bucket collapse", BSS preferred; Table 4 shows verbalized BSS -0.72 vs probe 0.29 (line level). [[when-calibration-rankings-reverse-accuracy-controlled-evaluation-for-fair-compar]] (2606.30814, non-code QA): raw ECE gaps correlate with accuracy gaps (rho -0.670, n 40) and reversal rates reach 0-53% (65% under SC candidate-aligned thinking vs non-thinking); that is cross-model ranking, not cross-method ranking, and not code.

## Evidence synthesis

**What is established.** (i) In code, ECE and discrimination decouple and can rank verbal formats oppositely: Tuerlings Table 1 and 2, Sec 4.3, 4.6; collapse-inflated ECE is also flagged by 2512.24560 Sec 3 and 2512.08810 Sec on Brier. (ii) Recalibration can reduce Brier without information gain: 2610.11300 Table 5 (BSS ~0.001). (iii) Test-oracle strength changes absolute pass rates (EvalPlus: -19.3 to -28.9% pass@k, vault abstract-level) and, in SQL, the reported risk and the apparent merit of oracle-built scores (2609.25938). (iv) Execution-graded hidden-suite labels with independent code generation are the code standard (2606.09577, 2603.27098, 2605.28500, 2605.09023).

**What is not established, within the instruments reached.** No fetched code study (a) varies the ECE estimator (equal-mass, debiased, smooth/kernel, reliability intervals) and reports a method-ranking change; (b) recomputes any confidence-method ranking under base vs augmented test labels; (c) contrasts pre-cutoff versus post-cutoff problems for calibration or discrimination; (d) crosses four confidence families (sampling, token, verbal, probe) in one design with these controls. Q13 (contamination changing calibration) remains unanswered by anything fetched. All of (a) to (d) are negatives under failed full-text instruments, so CLEAN (provisional) at best.

### Position A: ECE and single-oracle labels are unstable instruments
Best case: Tuerlings Table 1 (ECE 0.013 at AUROC 0.491), Sec 4.4 (parse policy moves ECE by 0.235 with AUROC flat), Liu et al. 16/16 same-oracle advantage, EvalPlus label shifts, BSS ~0 after Platt (2610.11300). Together these say headline rankings can be artifacts of binning, collapse, and label source. Weakness: each strand is from a different setting (verbal-only code; SQL; token-only code), and none shows a code ranking of methods flipped by oracle.

### Position B: Standard practice (hidden-suite pass, AUROC/ECE, Platt/multicalibration gains) is adequate
Best case: four-plus code studies report concordant rankings across AUROC, ECE and Brier (2605.28500 App: "broadly consistent"), the hidden suite on LiveCodeBench is a strict post-cutoff competitive-programming harness, and independent generation of the code under test (frozen outputs) plus independent self-test signals (2606.09577) already provide label independence in practice. Weakness: nobody tested the claim of adequacy; concordance was reported on closed API models and one benchmark family and without strengthened-test relabeling.

## Committed position

The disagreement is mostly not factual; it is an untested-assumption gap. Side A has real evidence for fragility but each piece lives outside the L1 design space (verbal-only, SQL, token-only), and Side B simply never ran the robustness check. So the comparison itself (four-plus families, execution labels) is OCCUPIED by union, and the defensible L1 contribution is the sensitivity protocol: show, for one fixed set of generations, whether the ranking of sampling, token, verbal, and probe readouts survives (1) four estimators (equal-width ECE, equal-mass ECE, debiased or smooth ECE, Brier skill with reliability intervals, plus AUROC and AURC), (2) base-test versus augmented-test labels (HumanEval+/MBPP+ vs original, a concrete oracle swap analogous to Liu et al.), and (3) a per-model release-date split with a pre-cutoff comparison group. The load-bearing reason: the nearest occupants each hold exactly one of those controls (Tuerlings: window but verbal-only and no oracle swap; Liu: oracle swap but SQL and consistency scores; 2610.11300: strengthened tests and BSS but token-only), and the concrete reason code could differ from SQL is that a code test-suite shortfall gives false-pass labels on plausible-but-wrong programs, which inflates exactly the confidence families that correlate with test-style agreement, as Liu's 16/16 finding predicts for execution-consistency scores.

Provisional verdicts by R1 component (L1 questions this locus decides):
- **Q3 release-date split for calibration (not accuracy):** NARROW. Residual: per-model post-cutoff versus pre-cutoff split applied to non-verbal families (sampling, token, probe) and a contamination contrast, not only a shared window. Closest: Tuerlings 2026 (verbal-only, shared window, UncertaiNLP) on one side; multicalibration 2512.08810 (release_v6 as leakage control, token-likelihood, whole benchmark) on the other.
- **Q4 label independence:** NARROW. Residual: treat label independence as a tested factor (same-oracle versus independent-oracle ranking, with sample-agreement scores built from tests the label uses) for code across families. Closest: Liu 2609.25938 (SQL, states the principle, 16/16) and Tuerlings Sec 3.3 / 2606.09577 (practice it untested). Reason code could differ: tests drive both label and code-side consistency clustering.
- **Q5 estimator sensitivity (ranking changes with estimator):** NARROW, leaning OCCUPIED on the fact (ECE vs AUROC decoupling; Tuerlings Table 1, Sec 4.6) and CLEAN (provisional) on the specific estimators (equal-mass, debiased, smooth, kernel). Residual: estimator variants beyond equal-width ECE versus AUROC. Closest: Tuerlings; 2512.08810 and 2512.24560 for collapse caveats; general-NLP estimator papers (vault 231208589) on the other side.
- **Q6 calibration vs discrimination separation / recalibration control:** OCCUPIED for token-level code (2610.11300 Table 5; 2512.08810 BSS) ; NARROW for the cross-family version.
- **Q10 test insufficiency changing calibration or rankings:** CLEAN (provisional). Closest: EvalPlus 2305.01210 (accuracy only), 2505.13553 Sec 5.2.2 (guarantee tightness vs test count), 2609.25938 (SQL). Gaps: arXiv full text, OpenAlex, S2 keyword all unavailable.
- **Q11 subgroup calibration and ranking effect:** OCCUPIED for token-likelihood (2512.08810); NARROW for ranking change across families.
- **Q13 contamination changing calibration/discrimination:** CLEAN (provisional). Nothing fetched compares pre/post-cutoff calibration. Gaps as above; arXiv metadata queries ti:calibration/contamination/code returned zero relevant records (noise only).

- **Position:** L1 comparison alone is OCCUPIED (union); the defensible L1 contribution is a three-control sensitivity protocol (estimator set, augmented-test relabeling, per-model release split) on identical generations, NARROW on Q3, Q4, Q5 and CLEAN (provisional) on Q10 and Q13.
- **Confidence:** medium (about 60%). Occupancy conclusions rest on full texts of 9 close papers; the negatives rest on partial instruments.
- **Boundary conditions:** holds for code generation with execution labels and for 2022-Nov 2026 literature reachable via vault + metadata search. It does not cover non-fetched concurrent work (arXiv 2611.* items) or OpenReview-only papers.
- **What would change this position:** a code paper showing a family ranking under original versus EvalPlus-strengthened tests (moves Q10 to OCCUPIED); a pre-cutoff versus post-cutoff calibration comparison for code (Q13); a code paper using equal-mass or debiased ECE and reporting rank changes (Q5 to OCCUPIED); or our own pilot showing rankings are invariant to all three controls, which would make the protocol a null result and weaken TMLR interest (still publishable as a robustness finding if narrowly claimed).
- **Evidence weight:** 5 code full texts support fragility pieces in isolation (2609.25938 is SQL), 4 full-text code papers show concordance by default, 2 sources (Spiess note, EvalPlus) abstract-level only, and the contamination-versus-calibration question has zero direct evidence either way.

## Open questions

- Spiess et al. (240202047) full text not in vault; whether its Platt/ECE results vary with estimator or contamination unchecked.
- Whether 2609.22511 (calibrated invariance audit) or post-June-2026 arXiv 2611.* work include oracle swaps; forward citation pages beyond the 3000 S2 offset for LiveCodeBench were rate-limited (HTTP 429 at offset 3000).
- No quantification of how many HumanEval/MBPP labels flip between base and plus suites for confidence-ranking purposes; needs our own pipeline.

## Sources

1. [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]]
2. [[certified-against-which-oracleexecution-labels-set-the-reported-riskof-conformal]]
3. [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]]
4. [[towards-functional-correctness-of-code-models-with-selective-generation]]
5. [[ensemble-based-uncertainty-estimation-for-code-correctness-estimation]]
6. [[using-semantic-distance-to-estimate-uncertainty-in-llm-based-code-generation]]
7. [[code-is-more-than-text-uncertainty-estimation-for-code-generation]]
8. [[functional-entropy-predicting-functional-correctness-in-llm-generated-code-with]]
9. [[multicalibration-for-llm-based-code-generation]]
10. [[251224560-localized-calibrated-uncertainty-in-code-language-models-full-text]]
11. [[when-calibration-rankings-reverse-accuracy-controlled-evaluation-for-fair-compar]]
12. [[is-your-code-generated-by-chatgpt-really-correct-rigorous-evaluation-of-large-la]]
13. [[240202047-calibration-and-correctness-of-language-models-for-code]] (abstract-level)
14. [[identity-or-prompt-noise-a-calibrated-invariance-audit-of-llm-code-generation]] (unscreened)
