# Differential table, revision 2: the systematics budget against the closest works (wave 7 draft, diff-A4)

Run date 2026-11-10. **Revision 2 (draft).** This revision closes every "not assessed" cell on rows 13 to 17 for Ribeiro, Campos, CREDO, Spiess, NeuroSym, and RLCM by full-text search; per-cell evidence, search terms, and file:line quotes are in `docs/s7/parts/diff-A4/CELLS_R2.md`. All other cells, the evidence table, and the dispositions are copied unchanged from revision 1 (`research/positioning/w6/DIFFERENTIAL_R1.md`), which was revised after the A6 critic (`docs/s6/parts/critic-A6/FINDINGS.md`) and extends `../w5/DIFFERENTIAL.md`, kept unchanged as the wave 5 record.

**What is added:**

- **A "Systematics budget" column.** It records the operator's wave 6 spine as planned in the draft design, `docs/s6/PIPELINE_DESIGN_R1.md` (written in Part B of this wave). These are planned cells, not results.
- **Five new rows (13 to 17).**
- **Three supplementary columns:**
  - MARGIN 2605.22949 (concurrent; label-validity occupant);
  - Kim and Kang 2605.27752 (concurrent; closest general-domain attribution work, A1);
  - 2609.04582 (concurrent; closest internal-versus-expressed decomposition, A1).

**Codes:**

| Code | Meaning |
|---|---|
| P | present |
| Pa | partial |
| A | absent: the full text was read for this control and it was not found |
| n.a. | does not apply |
| not assessed | the full text was not searched for this control (no cell carries this code in revision 2) |

For the budget column, the codes are:

| Code | Meaning |
|---|---|
| T | a toggle that enters the Shapley attribution |
| S | stratum |
| Sens | sensitivity analysis |
| R | required readout or baseline |
| Rec | reconciliation entry |
| Sec | secondary arm |

Rows 1 to 12 keep the wave 5 cells and evidence for the six main columns and RLCM. These are in `../w5/DIFFERENTIAL.md` and `../w5/parts/diff-A6/CELLS.md`.

**Evidence for new cells:**

| Cells | Evidence |
|---|---|
| CaC (2610.31820) | `R2610_31820_PROTOCOL.md` (full extraction) |
| MARGIN | `MARGIN_COVERAGE.md` and `docs/s6/parts/margin-A3/MARGIN.md` (full read, 2,389 lines) |
| 2605.27752 | `docs/s6/parts/occ-A1b/CANDIDATES.md` and `raw/fulltext/2605.27752.html` |
| 2609.04582 | `docs/s6/parts/occ-A1a/CANDIDATES.md` and `raw/ft/2609.04582.txt` |

**Rows 13 to 17 for Ribeiro, Campos, CREDO, Spiess, NeuroSym, and RLCM.** Closed in revision 2 by full-text search (`docs/s7/parts/diff-A4/CELLS_R2.md`). Ribeiro row 13 keeps the critic-verified Pa from revision 1. Cell locations below are line numbers in the full-text files listed in CELLS_R2.md ("txt:").

## Main table

| # | Control | Ribeiro | Campos | CREDO | Spiess | CaC | NeuroSym | RLCM (supp.) | MARGIN (supp.) | 2605.27752 (supp.) | 2609.04582 (supp.) | Systematics budget |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Supervision-matched readouts | A | Pa | Pa | Pa | Pa | A | Pa | Pa (online Platt on stated confidence, TXT:535-539; Spiess precedent) | Pa (isotonic and Platt maps fit for recalibration transfer, App G) | Pa (bias correction and few-shot vs trained probe on the same trials, Table 3) | T (supervision term: zero-shot, isotonic, trained stated readout; all supervised readouts on identical problem-grouped folds) |
| 2 | Trained stated-confidence readout | A | A | P | A | P | A | P | A (Platt rescaling is recalibration, Spiess precedent) | A | n.a. (expressed side is a verdict) | T (LoRA readout active only in the elicitation turn, scored on frozen generations) |
| 3 | Prompt-only baseline | A | P | A | A | Pa | A | A | A | A | Pa (difficulty baseline in the open-generation audit, running text txt:427-429) | T (difficulty term) and R |
| 4 | Code-text-only baseline | Pa | A | A | Pa | Pa | Pa | A | A | n.a. | Pa (lexical baseline 0.76, "text-only bounds", and candidate-only control at 0.500 in the verification design, txt:248, 250, 383; answer-surface features in the generation audit) | T (difficulty term) and R |
| 5 | Within-problem scoring | P | P | A | A | Pa | A | Pa | Pa (pairwise resolution within task in cold start, TXT:567-570; not on hardening rows) | A | Pa (each instance has a gold-YES trial and word-matched gold-NO foils, txt:119, 173, 177; metrics pooled) | T (difficulty term: pooled vs within-problem) |
| 6 | Oracle swap of test suites | A | A | A | Pa | A | A | A | Pa (verbal ECE after the EvalPlus swap on the same programs; no matched original-suite raw values for the cohort, TXT:661-668 vs 690-714) | Pa (correctness rule on QA: default vs exact match, Sec 4.3) | Pa (heuristic vs adjudicated labels, generation audit) | T (label-validity term: original vs EvalPlus) |
| 7 | Release or contamination split | A | A | A | A | A | Pa | A | A | A | A | S (release window relative to each model's cutoff) |
| 8 | Calibration estimator set | A | A | Pa | Pa | A | A | A | A (ten equal-width bins) | P (ECE estimator varied as an axis, App G) | A | Sens |
| 9 | Clustered paired inference | Pa | P | A | A | A | A | A | Pa (problem-cluster bootstrap, pointwise, no multiplicity adjustment, TXT:577-583) | Pa (95 percent intervals, paired bootstrap) | P (cluster bootstrap over structures, 2,000 resamples) | R (problem-clustered paired bootstrap for every term; multiplicity control) |
| 10 | Base versus instruct | A | A | A | A | A | A | A | A | Pa (base checkpoints, App B.3) | Pa (base checkpoints in the Discussion) | S and Sec |
| 11 | Same-weights reasoning on/off | A | Pa | A | A | A | A | A | A | A | Pa (Qwen3-0.6B "+ extended reasoning" 0.902 vs probe 0.898, Table 3, txt:332-367) | S and Sec |
| 12 | Routing replay with random and oracle comparators | Pa | A | Pa | A | Pa | Pa | Pa | Pa (selection in cold start) | A | A | Sec (decision cost of each budget term) |
| 13 | Generation-shift term: a trained readout scored on its own fresh generations vs on frozen generations | Pa (one probe readout scored on other-model candidates, RQ1, and on self-generated candidates, RQ2; dossier-A5/raw/2512.07404v3.txt:1427-1431; not a trained stated readout) | A (own candidates only; generation-state vs judging-pass probe on identical candidates, txt:489-490, 1214-1218) | A (each readout co-trained and scored on its own policy's samples, txt:813, 1383) | A (one greedy generation per problem, txt:408; no trained readout) | A (no contrast; which generations were scored is unresolved, `R2610_31820_PROTOCOL.md`) | A (CCN applied to each model's own K=10 samples; training temperature matched, not contrasted, txt:375-378) | A (probe updated jointly with the policy; Base and GRPO probes fit on their own rollouts, txt:116, 1088-1089) | A (reuses candidates, TXT:1238-1240) | Pa (own vs supplied answers, Sec 4.5 and App I; measures "the level of verbalized confidence, not the gap") | A | T (generation-shift term) |
| 14 | Supervised readouts refit under each label suite | A (one label suite per benchmark; MBPP+ only as a fit source, txt:736-738) | A (one test suite per benchmark, txt:599-601) | A (HumanEval+ is one evaluation set; no refit, txt:431) | Pa (Platt maps reported under test-passing and exact-match criteria, Table IV txt:1099 vs Table A1 txt:1736; criterion swap, not augmented tests) | A (one rule-based grader) | A (canonical test suites only; CCN trained once, txt:358-360) | A (gold-answer match on forced completions only, txt:112-113) | A (state carried across the swap without reset, TXT:468-470) | A | A | R (all supervised readouts retrained per suite) |
| 15 | Joint attribution of a gap between readouts, with intervals | A (zero hits for decompos, attribut, Shapley, ablat) | Pa (probe-vs-confidence lead under language shift, Δ±1.96 SE, txt:1170-1176, 671-681; pooled minus within-problem split, txt:666-667; no joint attribution) | Pa (2 by 2 emission by training-path decomposition, App C.2, txt:1617-1618, 1646; seed 43 only, no intervals, no probe arm) | A (zero hits for decompos, attribut, Shapley, ablat) | A | A (leave-one-out ablation of own modules on one model, no intervals, txt:506-517) | A (2 by 2 ablation of supervision variants within one probe readout, no intervals, txt:365) | A | Pa (one-axis shifts of the verbal-token gap, Table 4; no joint attribution) | Pa (threshold offset vs residual concealment, Table 3) | T (Shapley values over toggles; sequential decompositions as secondary) |
| 16 | Equivalence test of a residual gap against a pre-registered margin | A (superiority tests with Benjamini-Hochberg only, txt:873-874) | A (non-significance read as "statistically level", txt:1184-1185; no equivalence test) | A (mean and standard error over three seeds, txt:440) | A (no inference) | A (no intervals) | A ("margin over IGLB ... is modest", descriptive, txt:415-416) | A ("margin" names the method's reward, txt:121) | A | A | A | R (TOST paired with a superiority test) |
| 17 | Reproduction of other papers' published configurations on shared generations | Pa (RankEF re-trained "following the original paper" and checked against the authors' reported scores, scored on shared candidates, txt:1127-1141; a ranker baseline, no conclusion reconciled) | Pa (LAT re-run with Ribeiro's original stimulus prompt on shared candidates, txt:321-325, 621; Huang et al. claim checked qualitatively, txt:1462-1466; no published number reproduced) | A (RLCR and DCPO retrained under CREDO's own protocol and prompt, txt:435-440) | A (zero hits for reproduc, replicat, re-implement) | A | Pa (IGLB re-implemented with groups "following prior work", txt:396-403; no check against published numbers) | A (baselines retrained with identical shared hyperparameters, txt:135-136) | A | Pa (targeted review of 12 published comparisons, App J; not re-run) | A | Rec (Ribeiro, Campos, and 2610.31820 configurations as points in the budget) |

**Outside the columns.** 2609.33290 (concurrent, non-code) is the clearest instance of the row 13 confound. Its trained, probe-distilled stated readout is scored on the student's own samples, while its probe scores "the original model's sampled answers rather than the student's outputs" (`docs/s6/parts/occ-A1a/raw/ft/2609.33290.txt:571-575, 3448`). The contrast is not isolated there, so the paper would be Pa on row 13. RADAR 2610.22139 would be Pa on row 15: it splits risk into a scalar-recalibration-removable term and residual terms, with no verbal arm.

## What the budget column adds

**Rows 13 to 17.** No assessed column has a P cell on rows 13 to 17. Every cell in the six main columns, RLCM, and the three other supplementary columns is now assessed, so this claim no longer rests on a subset of columns. The partial cells are:

- **Row 13:** Ribeiro (one probe readout on other-model versus self-generated candidates, not a trained stated readout) and 2605.27752 (own versus supplied answers). Every other column scores each readout only on its own policy's generations, or only on frozen ones.
- **Row 14:** Spiess only (Platt maps under test-passing versus exact-match criteria). No column refits a trained readout under original versus augmented test suites.
- **Row 15:** Campos (one-axis shift of the probe-versus-confidence gap with intervals), CREDO (a 2 by 2 emission by training-path decomposition, one seed, no intervals), 2605.27752, and 2609.04582. No column gives a joint attribution of a gap between readouts with intervals.
- **Row 16:** none. No column tests a residual gap for equivalence against a margin; Campos reads non-significance as parity without such a test.
- **Row 17:** Ribeiro (RankEF re-trained under its published configuration and checked against its published scores), Campos (LAT with Ribeiro's original prompt), NeuroSym (IGLB with groups adopted from prior work), and 2605.27752 (a review, not a re-run). None re-runs another paper's readout comparison to reconcile its published conclusion.

Ribeiro row 17 is the cell closest to P. Read literally, the row text ("reproduction of other papers' published configurations on shared generations") is met by its RankEF reproduction. The budget's row 17 is a reconciliation entry: it places other papers' confidence-readout configurations as points in the budget. If the paper states this row as a contribution, its wording should name reconciliation of published readout comparisons, not reproduction in general. The A1 occupancy search (`DECOMPOSITION_OCCUPANCY.md`) found no joint attribution of a probe-versus-stated gap, consistent with row 15.

**Rows 1 to 12.** The wave 5 residual stands: rows 1, 4, 6, 7, 8, 10, 11, and 12 have no P cell in the six main columns. Corrections against the new columns:

- **Row 6, oracle swap:** MARGIN is Pa. The residual is the swap applied across readout families, with matched original-suite values and refit readouts.
- **Row 8, estimator set:** 2605.27752 is P outside code. Estimator choice is therefore a sensitivity analysis and is not claimed as a contribution.
- **Row 9, clustered inference:** 2609.04582 is P outside code. It was already P in Campos on code.

**Concurrency** (A6 F15):

- MARGIN, 2605.27752, and 2609.04582 are concurrent (first posted after 2026-05-10).
- RLCM (arXiv 2604.23333) predates the window.
- 2605.09502 (outside the table) was posted on 2026-05-10 itself, at the boundary.

By the operator rule, concurrent works are cited and differentiated.

## Sentences in the paper that must cite these columns

| Topic of the sentence | Cite |
|---|---|
| Any comparison of a trained readout with a probe on code | 2610.31820, CREDO |
| Within-problem scoring or a prompt-only baseline on code | Campos |
| Probes against stated confidence on code | Ribeiro |
| Augmented tests applied to frozen code generations | MARGIN |
| A readout comparison that moves with measurement choices on fixed answers | 2605.27752 |
| A recalibration-versus-residual split | 2609.04582 and RADAR |
| A trained readout scored on its own generations against a frozen probe | 2609.33290 |

## Disposition of the A6 findings on this file

| Finding | Disposition |
|---|---|
| F6 | Accepted. Ribeiro row 13 is Pa; unsearched cells are "not assessed" |
| F7 | Accepted. 2609.04582 row 5 is Pa |
| F8 | Accepted. Location corrected |
| F9 | Accepted. 2609.04582 row 11 is Pa |
| F10 | Accepted. Row 4 cites the verification controls |
| F11 | Accepted. MARGIN row 1 is Pa and row 2 is A; 2605.27752 row 1 is Pa |
| F12 | Accepted. MARGIN row 6 is Pa |
| F13 | Accepted. MARGIN row 5 is Pa |
| F15 | Accepted. Concurrency statement corrected |
| F21 | Accepted. The design file is named as written in Part B |
