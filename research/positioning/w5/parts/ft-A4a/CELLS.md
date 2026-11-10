# Wave 5, Part A4a: cell verdicts for L1 Q5 (sub-part), Q10, Q13

Run 2026-11-10. Queries and raw records: `QUERIES.md`. Verdict vocabulary as in `research/positioning/w4/VERDICTS.md`. W4 gaps named below: G-FT (arXiv full-text search), G-OA (OpenAlex full text partial), G-S2 (Semantic Scholar search 429), G-AX (arXiv export 429).

**Instrument change since W4.** The arXiv full-text instrument (search.arxiv.org) answered 30 of 30 queries with HTTP 200 and returned body-text snippets (table captions, appendices, limitation sections). G-FT is therefore closed for these three cells. G-AX is not relevant here because the export API was not used. G-OA still holds (partial full-text coverage, though all 10 queries returned HTTP 200). G-S2 still holds for Q5 and Q10 (six 429s each); for Q13 one query returned HTTP 200 on the fourth attempt.

## L1 Q5 sub-part: estimator set (equal-mass, debiased, smooth ECE) changes the ranking of confidence methods on code

**Verdict: stays CLEAN (provisional).** G-FT is now closed; G-OA (partial) and G-S2 (429) remain.

New evidence. All of it is adjacent; none of it occupies the cell.
- Afrin and Shihab 2609.27954 (LLM-judge recalibration; HumanEval is one of eight domains, Table 1). They use equal-mass ECE as a secondary metric and state that "debiased and smoothed ECE variants were not computed and are listed in Appendix K as not run" (Section 2.3; Appendix K, "Not run, and therefore claimed nowhere: ... debiased/smoothed ECE variants"). This is explicit body-text confirmation of the gap.
- CREDO 2609.34857 (HumanEval+, LiveCodeBench v5 and v6). Table 1 ECE uses "the standard ten equal-width bins"; equal-mass bins appear only in the reliability diagrams (Appendix C.5, B.3). There is no estimator comparison.
- MARGIN 2605.22949: ECE "uses ten equal-width bins" (Section 6.3). Its band-count grid varies the calibrator's bands, not the ECE estimator (Section 7.6, Parameter Sensitivity).
- NeuroSym-Cal (W4 full text): it uses one estimator, "the unbiased estimator with M = 10 bins" (Section 4.3).
- 2606.30814 (vault note): calibration rankings of models reverse under accuracy control, with an APPS graded-correctness appendix for two Qwen models (appendix, Table 11). That is a ranking change across models caused by accuracy alignment, not across confidence methods caused by the estimator.
- 2608.20569 (HumanEval and MBPP among 11 benchmarks) scores with equal-mass ECE only. 2606.07822 (ACUTE) compares ECE and smECE but uses no code task (no code benchmark in the full text).

Remaining gaps: G-S2 (S5-1 failed); G-OA partial.

## L1 Q10: test insufficiency (original versus augmented tests) changes calibration or rankings

**Verdict: moves from CLEAN (provisional) to NARROW.**

Occupant (concurrent; dossier `dossiers/2605.22949.md`):
- MARGIN (Armstrong, 2605.22949, v1 2026-05-21) uses HumanEval to HumanEval+ and MBPP to MBPP+ as "same-task hardening" transitions. "HumanEval+ and MBPP+ use expanded tests from EvalPlus on the original candidate programs. These two hardening checks change the correctness criterion for previously seen tasks" (Section 6.1, Table 1).
- It reports post-hardening ECE of raw verbal confidence of 8.57 and 17.96, against 3.57 and 3.07 for MARGIN (Table 3).
- It states that "All five comparisons on each of the two same-task hardening checks are inconclusive" (Section 7.1). So MARGIN measures calibration under an augmented-test oracle swap on fixed generations.

**Residual.** No work found measures, on matched cohorts and identical generations, whether swapping original tests for EvalPlus tests changes calibration and discrimination (ECE, AUROC) across several confidence families, or whether it reorders confidence methods. MARGIN covers one family (verbal stated confidence). It compares online recalibrators, not readouts, and it reports no matched original-test calibration figure for the same nine-model cohort.

Closest work on each side:
- MARGIN: oracle swap, calibration, verbal only.
- EvalPlus 2305.01210: oracle swap, accuracy and model ranking only ("test insufficiency can lead to mis-ranking", abstract snippet A10-06).
- Liu et al. 2609.25938 (W4): oracle sets risk, text-to-SQL.

Adjacent, read in full and not occupying:
- 2609.01106 requires passing both EvalPlus base and plus tests (Section 2), with no swap.
- 2610.18583 reports HumanEval+ and MBPP+ as accuracy only; its ECE is on math (Table 2, Table 6).
- 2609.13890 uses HumanEval+ for router calibration, not readout calibration.
- 2610.05472 (survey, Section 3.3) restates that EvalPlus "can change rankings", which refers to accuracy.

Remaining gaps: G-S2 (S10-1 failed); G-OA partial. Forward citations of MARGIN were not screened.

## L1 Q13: contamination (pre- versus post-cutoff) changes calibration or discrimination of confidence readouts on code

**Verdict: stays CLEAN (provisional).** G-FT is now closed and S2 passed one query; G-OA remains partial.

New or reconfirmed evidence. All of it is adjacent.
- Tuerlings and Valdenegro-Toro (vault note, Section 3.1) evaluate all six models "on the same window from 2024-09-19 to 2025-04-30". They cite Li and Flanigan for the pre- versus post-cutoff accuracy gap but do not measure calibration on pre-cutoff problems. The DataCite record of the companion dataset (10.5281/zenodo.22881716) lists only the 365-problem window.
- NeuroSym-Cal (W4 full text, Section 4.1) reports "the held-out subset per model" and treats the whole window "as a harder-than-training testbed rather than a universally OOD set". It gives no pre- versus post-cutoff contrast.
- Klassert 2609.13975 (W4 dossier, Section 4.1) explicitly forgoes "strict contamination control".
- 2609.01106 lists contamination as a limitation (Section 11, Limitations: "A contamination-resistant, time-split ... benchmark would strengthen external validity").
- The W4 lead 10.1109/tse.2026.3713834 resolves via Crossref to Dong et al., "Generalization or Memorization". Its arXiv full text (2402.15938) detects contamination from output distributions and reports pass@1. It contains no calibration or confidence-correctness metric (no "calibrat", "ECE", or "AUROC" in the text).
- BlockBench (OpenReview ijm5JWbyQM, abstract) contrasts pre- and post-cutoff accuracy for smart-contract vulnerability detection, with no calibration.

Remaining gaps:
- G-OA is partial.
- The TSE version of Dong et al. was not read (IEEE is off the allowlist), so only the arXiv text is checked.
- 2606.20502 (vulnerability-detection calibration with a temporal split) was snippet-screened only. It is a classification task, not execution-graded generation.
