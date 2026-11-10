# MARGIN (arXiv 2605.22949): what made L1 Q10 NARROW, and what the systematics budget adds

Wave 6, task A3. Run date 2026-11-10. Text basis: FULL TEXT, arXiv v4 (2026-10-08, single author), saved at `../w5/parts/ft-A4a/raw/ft/2605.22949.txt`, read in full (2,389 lines). The sub-agent inventory with all quotes and line numbers is `../../../docs/s6/parts/margin-A3/MARGIN.md`; `TXT:N` below refers to the saved text. The v1 date (2026-05-21) comes from the W5 dossier and is not printed in the v4 text.

## What MARGIN covers (the reason for NARROW)

**What it does.** MARGIN re-scores the same candidate programs under EvalPlus tests: "expanded tests from EvalPlus on the original candidate programs" (TXT:447-449). In its own words, "These tests reuse the original candidate programs rather than eliciting new answers" (TXT:1238-1240). That is an oracle swap on frozen generations, which is the L1 Q10 control.

**Scope of the oracle swap:**

- **Readout:** one confidence family, verbalized 0 to 100 at temperature zero (TXT:1256-1257).
- **Cohort:** nine cloud models (TXT:520, TXT:523, Table 8).
- **Tasks:** HE 164 to HE+ 163; MBPP 257 to MBPP+ 224 (TXT:518-524).
- **Metric:** ten-bin equal-width ECE, pooled over responders (TXT:549-561).
- **Results (Table 3, TXT:661-668):**
  - HE to HE+: raw ECE 8.57, MARGIN 3.57.
  - MBPP to MBPP+: raw ECE 17.96, MARGIN 3.07.
- **Intervals:** paired problem-cluster bootstrap with 10,000 draws, "pointwise without multiplicity adjustment" (TXT:577-583).

**What it does not do.** It reports no raw ECE and no AUROC on the original tests for the same nine-model cohort. The nearest original-test raw values (12.80 and 17.51, TXT:698-714) come from a different 18-model cold-start pool and are not compared. MARGIN therefore shows calibration after a relabel. It does not measure how test insufficiency changes calibration or ranking.

**Also absent** (searched across the full text):

- probe, hidden-state, logit, and token-probability readouts (TXT:61-62, TXT:110-112);
- an isotonic baseline;
- prompt-only and code-text-only baselines;
- within-problem scoring on the hardening rows (pairwise resolution appears only in cold-start coordination, TXT:567-570);
- a release or contamination split;
- difficulty strata;
- clustering on model or family.

The only trained stated readout is online Platt scaling (TXT:535-539). It is updated online and carries its state across the swap without a reset (TXT:468-470), so no readout is refit under each suite.

## What the systematics budget adds beyond MARGIN

1. **A probe-versus-stated gap.** The budget defines that gap as the estimand, on frozen self-generated code. MARGIN has no internal readout.
2. **Label validity as an attributed term.** All readouts are rescored and every supervised readout is refit under each suite. Both suites are reported on matched raw calibration and discrimination for the same cohort. MARGIN has only the post-swap calibration of one family.
3. **Supervision and difficulty terms.** The budget toggles zero-shot, isotonic, and trained stated readouts, and contrasts pooled with within-problem scoring, with prompt-only and code-text-only baselines. None appears in MARGIN.
4. **Generation shift.** The budget scores a trained readout on its own fresh generations. MARGIN reuses candidates only.
5. **Attribution with clustered uncertainty.** Shapley terms get problem-clustered paired intervals and multiplicity control. MARGIN's intervals are pointwise.
6. **Strata.** Contamination (release window relative to cutoff) and model family and scale become explicit strata. MARGIN pools models and calls its cloud and local split "descriptive" (TXT:1107-1109).

**Sentence that must cite MARGIN in the paper.** Any sentence that says augmented tests are applied to the same generations to measure stated-confidence calibration must cite it. The budget's own label-validity term is differentiated by points 2 and 5.

**Citations for points 1 to 4** (A6 F22). These rows describe what MARGIN lacks, and each control exists elsewhere:

| Point | Control | Cite |
|---|---|---|
| 1 | Probe against stated confidence on code | Ribeiro 2512.07404 |
| 3 | Within-problem scoring and a prompt-only baseline on code | Campos 2611.07876 |
| 3 | Trained stated readouts against a probe | 2610.31820 (on code), 2609.33290 (outside code), and CREDO 2609.34857 (trained stated readout on code) |
| 4 | Generation confound in a trained arm | 2609.33290 |

## Flag (resolved after A6 F19)

**First draft.** The sub-agent compared Table 9's 1,467 (HE to HE+) and 2,016 (MBPP to MBPP+) usable target records against the summed source-phase columns of Table 8, which gave 1,320 and 2,142. That flag is withdrawn: the source-phase columns are the wrong denominator.

**Resolution.** The counts reconcile as 9 x 163 = 1,467 and 9 x 224 = 2,016: nine cloud models times the target task counts (TXT:476-477).
