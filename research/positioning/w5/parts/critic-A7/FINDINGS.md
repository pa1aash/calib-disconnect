# A7 critic findings (wave 5, Part A)

Saved by the orchestrator from the critic's returned text, because the harness blocked the critic's own write (same procedure as wave 4, DEVIATIONS.md). The content follows the critic's return, reformatted as markdown. Line numbers refer to the saved full texts in each part's raw/ folder.

**Q2 verdict: UNSEATED as the novelty spine if concurrent works are in scope (operator concurrency decision). NOT UNSEATED if they are ruled out.**

## Summary

- **A14 is met (F1).** 2610.31820 meets pivot A14 as R1 section 6 words it (R1:348, 357-359). R-Tuning is a training method for stated confidence, and it is fit on the same labels as the probe. On code it comes within .02 AUROC of the probe on all four splits (Table 3). A4b's phrase "effectively triggered for a pooled headline" is softer than the rule.
- **Input-only baselines are not residual (F7).** Campos Table V already has a prompt-only probe on code (.891 vs .886).
- **The union boundary (F2).** Together these works cover every Rank 1 control except a trained readout scored within problem. That puts Q1c at the A20 union boundary, so the fallback is Rank 2 as the spine.
- **Effects the agents missed:**
  - L2 Q10 changes (F5).
  - 2610.34654 bears on L4 Q1 (F9).
  - Self-consistency beats the probe on LiveCodeBench (F6).
- **A5 corrections check out, with one addition (F18).** CREDO's untrained base read by digit expectation (Base-d) scores .782, so "0.690 to 0.850" overstates the gain from training.
- **DIFFERENTIAL.md:** five cells are wrong or inconsistent (F11 to F16).
- **Fabrication:** none found (F20).

## Q2 (decisive): does 2610.31820 unseat Rank 1?

**F1. Critical: pivot A14 is triggered, not "near-triggered".**

- **Where:** `ft-A4b/CELLS.md:16, :93`; `dossiers/2610.31820.md:12`; `w4/RECOMMENDATION.md:15-17`.
- **Rule:** R1:357-359 asks only whether "the gap between probe and stated confidence on code is shown to close, in discrimination ... under ... a training method for stated confidence." R1:348 makes L2 unviable as the spine if any such record exists.
- **Evidence, verified in `ft-A4b/raw/ft/2610.31820.txt`:** R-Tuning against the probe on code.
  - Qwen3-8B: .86 vs .88 in distribution (lines 430, 449); .85 vs .84 out of distribution (433, 452).
  - Nemotron: .89 vs .89 in distribution (526, 545); .79 vs .80 out of distribution (529, 548).
  - The probe uses "the same labeled data" (1097). Thinking mode is on (1974).
- **Caveats that do not change the A14 test:**
  - The "different generations" point is inferred from Table 2 (251-262, 1112) and is not stated.
  - The readout is a categorical token, not a numeric statement.
  - Grading is "rule-based" (2021); execution is not stated.
  - Scoring is pooled only, on PPO checkpoints the authors trained.
- **Fix:** mark A14 TRIGGERED (concurrent) and invoke the R1 replacement order, conditional on the concurrency decision.

**F2. Critical: the Rank 1 controls meet the A20 union definition (R1:300-301).**

- **2610.31820:** supervision-matched trained readout against a probe; zero-shot verbal confidence (.58 to .61); 8-sample self-consistency; text-only external estimators on APPS and TACO (100-144).
- **Campos:** prompt-only probe (2611.07876v1.txt:1226-1229, 1261-1281); within-problem scoring of the probe against P(Yes) (196-197, 272); clustered bootstrap (673-676).
- **Ribeiro RQ2:** within-task ranking of the model's own samples.
- **Left:** only a trained readout crossed with within-problem scoring on identical generations.
- **Fix:** L2 Q1c becomes "NARROW, at the A20 boundary".

**F3. Critical: the surviving residual and the sentences that must cite it.**

- **Residual:** on identical, execution-labeled, self-generated code, whether a trained numeric own-readout, zero-shot verbal readouts, sampling readouts, and a probe still differ within problem, with prompt-only and code-text-only baselines fit to the same labels and folds.
- **Status:** this is an analysis inside Rank 2, not a headline. Campos already reports 0.58 to 0.64 within problem for all methods (1202-1204).
- **Sentences that must cite 2610.31820:**
  1. Supervision-matched probe against trained readout on code, including the RECOMMENDATION:29 phrase "how much of the published probe advantage survives".
  2. Text-only or external estimators matching self-estimation on code.
  3. Probe against verbal confidence for thinking-on models on code.
  4. Sampling against probe on LiveCodeBench: self-consistency .89 vs probe .84 for Qwen, and .88 vs .80 for Nemotron (414/452, 510/548).
  5. Confidence-based best-of-N selection or early stopping.
- **Also cite Campos** for the prompt-only baseline.

## Q1: verdict changes

**F4. Minor: L1 Q10 moving to NARROW (MARGIN) is supported.**

- Verified at `2605.22949.txt:447-450, 638-639, 661-667`; v1 is dated 2026-05-21.
- MARGIN reports no raw ECE on the original tests for the same cohort. So it shows calibration under augmented tests, not that test insufficiency changes calibration. Word the residual that way.

**F5. Major: L2 Q10 (W4 VERDICTS:58) changes because of 2610.31820, and every agent missed it.**

- The paper compares a probe with verbal confidence on code, with thinking on, in AUROC, ECE, and Brier (Tables 3 and 9).
- **Fix:** OCCUPIED (concurrent), or NARROW with only a model-swap residual, which fails A21.

**F6. Major: the dossier omits that self-consistency beats the probe out of distribution on code.**

- See F3 item 4.
- Per benchmark, Nemotron on LCB Easy has .83 vs .62 (2549, 2567).
- The paper's sentence "best on seven of eight [OOD] splits" (1116-1117) contradicts its own Table 3: for Nemotron code OOD, self-consistency .88 is above CaC .84 (510, 567). Cite the table, not the sentence.

**F7. Major: the prompt-only baseline is not a residual.**

- Campos Table V: .891 vs .886 for Qwen; .720 vs .851 for gpt-oss.
- **Fix:** remove it from the residual sentences in `ft-A4b/CELLS.md:19`, VERDICTS:50, RECOMMENDATION:59, and DIGEST:20 and :86.

**F8. Minor: the A4b numbers for Q1c and Q11 are correct, with one citation wrong.**

- "Pooled only (Appendix C)" should cite Sec 4.1 (1104).
- The per-difficulty LCB strata in Table 9 are a weak step toward difficulty control and should be mentioned.

**F9. Major: L3 Q2/Q7 moving to NARROW is supported, but an L4 effect was missed.**

- **Support:** 2610.34654 at 468, 476-478, 543, and 1087-1088.
- **Unverified suspicion:** what the "valid bug reports" contain is unspecified (465). Check its appendix Tables 8 and 13 before writing the Rank 3 novelty sentence.
- **Missed L4 effect:** the paper elicits requirement-level stated confidence scored by hidden tests, and that beats whole-patch confidence in Brier (528-529, 541). This narrows L4 Q1 (VERDICTS:88).
- **Wording conflict:** A2's "stays CLEAN (provisional)" refers to 2610.19226 only. Say so, so the two part files do not seem to conflict.

**F10. Minor: other cells checked.** No change to L1 Q1, L2 Q13, A20, A15, or L3 Q1/Q4/Q5.

## Q3: DIFFERENTIAL.md (18 cells checked)

**Correct as coded (verified):**

- Campos: rows 1, 3, 5, 9, and 11.
- CaC: rows 1, 3, 4, 8, and 9.
- CREDO: rows 2 and 9.
- Spiess: rows 1 and 8.
- Ribeiro: row 5.
- NeuroSym: row 8.

**Wrong or inconsistent:**

- **F11, major. CaC row 2 should be present.** R-Tuning is a fine-tuned verbal readout, and CREDO's two-token readout is coded P.
- **F12, major. CaC row 5 should be partial.** It selects among the model's own 8 samples on code (Table 2; Sec 4.3, 1127-1129). That is the same kind of evidence that gives Ribeiro P and RLCM Pa. This breaks DIFFERENTIAL:64.
- **F13, major. "Campos has no stated-confidence readout of any kind" is wrong** (DIFFERENTIAL:64; DIGEST:49; RECOMMENDATION:37). Campos reads P(Yes) following Kadavath, the same kind of readout as Ribeiro's True/False (2512.07404v3.txt:443-447). Reword: "categorical self-judgment, no numeric or trained readout".
- **F14, minor. CREDO row 8 should be Pa** by the Spiess standard: its reliability diagrams use equal-mass bins (2609.34857v1.txt:1993-1996).
- **F15, minor. Row 12 is coded inconsistently.** Ribeiro is A and CaC is Pa; under the row definition both should be A, or both Pa.
- **F16, minor. "Scored on different generations" is an inference, not a stated fact** (DIFFERENTIAL:39, :55). Mark it as inferred.

## Q4: A5 corrections and W4 sentences

**F17. The A5 corrections are verified.**

- **Campos:** .620 is the in-distribution generation probe (1258); .629 is Qwen confidence under shift (1205-1206).
- **Ribeiro:** +29.0 is LAT 56.3 minus True/False 27.3; +28.8 is LAT minus Random 27.5 (941, 971-975). The HumanEval +26.2 is FitSyn 63.0 minus Intrinsic 36.8 (1008-1014).
- **CREDO:** DCPO-d .849 vs CREDO .850; on LCB v6, DCPO-d .896 vs CREDO .887 (617, 627, 2536, 2547).

**F18. Major: a CREDO correction A5 missed.**

- Base-d is .782 (590) and GRPO-d is .833 (599). The "0.690 to 0.850" comparison therefore mixes readout methods.
- Use ".782 (Base-d) to .850; GRPO-d .833; DCPO-d .849".

**F19. Major: W4 sentences that must change.**

- **DIGEST:**
  - :15: the Ribeiro range mixes baselines and fit conditions, and its unit is 1-of-4 selection accuracy, not AUROC.
  - :24: change to ".627 or .540 vs .629 under shift".
  - :20 and :86: input-only baselines (F7).
  - :30: L1 Q10 (F4).
  - :32: L3 (F9).
  - :49: Campos "no verbal" (F13).
  - :50: CREDO (F18).
  - :75: A14 (F1).
  - :88-89: the Rank 1/Rank 2 order (F3).
  - :100-105: the unread leads are now resolved.
- **VERDICTS:**
  - :38 and :43: L1 Q10.
  - :49: Ribeiro wording, plus the sampling result.
  - :50: Q1c residual and the Campos pair.
  - :58: L2 Q10.
  - :59 and :67: CREDO and A14.
  - :77: L3.
  - :88: L4 Q1.
  - :113: new concurrent works.
  - :126 and :130: A14 resolution text and the leads.
- **RECOMMENDATION:**
  - :15-17: A14 and the replacement order.
  - :29: the contribution sentence is now partly answered.
  - :34 and :86: Q10.
  - :37: Campos.
  - :59: input-only baselines.
  - :61: "0.69 to 0.78" comes from Sec VI-C c, not Table V.
  - :72: the trained arm no longer stands at the pooled level.
  - :76: the leads.
  - :103-112: Rank 3 is now NARROW.
  - :151-157: the concurrency section now also covers A14 and L2 Q10.

## Q5: fabrication

**F20. No fabricated number, quotation, or id was found.**

- **Checked:**
  - the 2610.31820 numbers;
  - A2: `text_2610.19226v1_pdf.txt:25, 356, 565, 630-633`;
  - A3: the Spiess Semantic Scholar count of 100, DOI 10.1109/ICSE55347.2025.00040, OpenAlex 96, and 2611.07913 lines 474-544;
  - MARGIN;
  - 2606.00251:580;
  - 2604.16931:73.
- **Not verified:**
  - Miglani "0.677 vs 0.703";
  - the TSE-only text;
  - which generations R-Tuning was scored on;
  - the content of the 2610.34654 bug reports.
- **Process note:** A2 disclosed one request to a host off the allowlist, with the content discarded (VERDICT_EFFECT.md:20). Record it in the wave report.
