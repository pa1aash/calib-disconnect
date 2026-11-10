# Critic C1 (claims) findings: PIPELINE_DESIGN_R2

Wave 7, step C1. Fresh-context red-team critic (opus) that read only `docs/s7/PIPELINE_DESIGN_R2.md`, `docs/s7/power/POWER_R2.md`, `research/positioning/w7/DIFFERENTIAL_R2.md`, and `docs/s2/venue/TMLR_RUBRIC.md`, plus three cited full texts to check specific claims. The critic declined to write this file under its own operating rules; the orchestrator saved the returned text here, condensed, with no change of substance. Line numbers refer to R2 as committed in `de09536`.

**Count:** BLOCKING 3, MAJOR 14, MINOR 6.

## BLOCKING

**K1. The outcome templates claim more than the evidence covers.**
- **Location:** §1.8.
- **Problem:**
  - Generic names such as "a trained stated readout", "a hidden-state probe", and "supervised stated confidence" stand for one specific rank-16 elicitation-masked LoRA Yes/No readout and one selected linear-probe family.
  - "Code" is unrestricted, although the population is pre-cutoff HumanEval+ and MBPP+ sampled at temperature 1.0 with thinking off.
  - R7's "pre-cutoff" scope does not appear in any template.
  - "Can express what the probe reads" claims shared information, which equal W does not show.
  - "Matches" is stronger than equivalence within ±0.03.
- **Fix:** add a population prefix, use defined readout names, write "is equivalent within the 0.03 margin to", and caveat that equal within-problem AUROC does not show shared information.

**K2. The training term φ_t mixes a format change, parse failures, and training.**
- **Location:** §1.2, §7.2, §7.4.
- **Problem:** in the primary chain, t moves the readout from V1 (a decoded integer with median-imputed ties) to S^T (a V2 Yes/No logit ratio with a LoRA adapter). φ_t is likely the largest term (−0.107 in T6, a planning value).
- **Fix:**
  - Pre-register a diagnostic split: (V1 zero-shot → V2 zero-shot) plus (V2 zero-shot → V2 trained).
  - Call the term "readout change (format and training)" unless the training part alone excludes zero.
  - Report the share of pairs tied by V1 imputation next to G0.

**K3. The ".02 tie" credited to [2610.31820] does not appear in the paper (checked).**
- **Location:** lines 186, 194, 364, and 1050 (K5).
- **Evidence:** no tie statement exists in `research/positioning/w5/parts/ft-A4b/raw/ft/2610.31820.txt`. At txt:1115 the paper reads a .02 difference as a lead ("ahead of R-Tuning by 0.02 to 0.13"). The "comparable discrimination ... within 0.05" passage (txt:118) concerns external versus self estimators.
- **Fix:**
  - Rewrite as the design's own reading of Table 3 (differences of at most .02 in all four cells, with no tie stated by the paper).
  - Drop it as a margin anchor.
  - Say "Table 3 pattern" instead of "the paper's tie".

## MAJOR

**K4. Rule 1 would name null or negligible terms.**
- **Evidence:** T6 gives phi_RECAL 0.0019 ± 0.0009, which excludes zero.
- **Fix:**
  - Name a term only if its simultaneous interval excludes zero and its absolute value is at least δ.
  - Never name r in the discrimination budget.
  - State that term intervals condition on the fold-seed-0 fits.

**K5. "Share", "reversed by", and "probe-over-stated" assume signs and mix units.**
- **Problem:** the sign of G0 is not pre-registered, and "share" is undefined when terms have mixed signs. G0 is pooled AUROC while R is W. "Reversed by" is causal language.
- **Fix:**
  - Define share as φ_v/(R − G0), used only when every named term has the sign of R − G0.
  - Make the templates conditional on the sign of G0.
  - Write "sum with G0 to".
  - Mark the unit change at φ_d.

**K6. Term and stratum names carry interpretations the accounting cannot support.**
- **Problem:**
  - "Difficulty", "label validity", "supervision", and "contamination stratum" are interpretive names.
  - Scale contrasts are confounded with architecture (Gemma) and with version (Olmo 3 versus 3.1).
- **Fix:**
  - Use operational names in paper text: scoring level, label suite, and release window relative to the stated cutoff.
  - State the confounds.

**K7. Only D1 carries a capacity or recipe caveat.**
- **Problem:** D2 is consistent with an under-fit adapter or a narrow recipe grid. D3 is consistent with the adapter's extra capacity.
- **Fix:** add mirrored caveats that quote R at ranks 1, 4, and 16.

**K8. Under true equivalence, the per-model sentence will read as a failure.**
- **Evidence:** per-model D1 power is about 0.01 to 0.05, so about 0 of 6 intervals fall within the margin even when every R_m = 0. The heterogeneity sentence rarely fires.
- **Fix:**
  - Add the audited per-model power.
  - Report how many intervals exclude the margin in each direction.
  - Trigger the heterogeneity sentence when τ̂ > δ.
  - Run M = 1 power under the R2 rule.

**K9. "Reproduced" cannot happen for [Ribeiro].**
- **Arithmetic:** 121 tasks give a 95 percent half-width of about 0.064 at 0.85, which cannot fit in a 0.10 window. The rule is asymmetric.
- **Also:** "0.05 in the published unit" means 0.05 points for percentages.
- **Fix:** use per-target tolerances in proportion units, or make the level check descriptive where deviations predict a shift. Redefine the level check.

**K10. A tie cannot be classed "not reproduced", and the tie widths are the design's own.**
- **Fix:**
  - Add "a named tie fails when its paired interval lies entirely outside the tie width".
  - Label the tie widths as design choices.
  - Align K5 with this rule.

**K11. The reconciliation leaves room for choices made after seeing outcomes.**
- **Problem:**
  - The gpt-oss prefill is applied "only if the reproduction needs it".
  - Two readings give two chances to reproduce.
  - The inference about the paper's protocol is not licensed.
  - No combination rule exists across readings, models, and checks.
- **Fix:**
  - Fix the prefilled final channel now, with reasoning-on as a labeled sensitivity analysis.
  - Report one outcome per reading.
  - Drop the protocol inference.
  - Use one verb per paper, with per-check counts.

**K12. Analogs can pass or fail for reasons unrelated to the published claims.**
- **Problem:**
  - Level misses are expected from the PPO checkpoints and the LCB window.
  - Truncation-labeled samples are easy negatives.
  - A Campos failure on X1 and X2 cannot make the primary difficulty term "model-specific".
  - K5's "explains" is causal language.
- **Fix:**
  - Make the level checks descriptive where deviations predict a shift.
  - Add diagnostics that exclude truncation and extraction failures.
  - Reword the Campos clause.
  - Strike "explains".

**K13. The "shared budget cell" is nearly always empty, and no reconciled disagreement is named.**
- **Fix:**
  - Name the discrepancy and the term for each paper pair, without predicting a sign.
  - Reword DIFFERENTIAL row 17 as "beside the budget".
  - Write the LiveCodeBench cells as (r,t,d).

**K14. The published [Ribeiro] values are a selective subset.**
- **Evidence:** the Qwen row includes LAT FitMBPP at 28.1 percent, below Random (`2512.07404v3.txt:1182-1211`). The column assignment is positional.
- **Fix:** list FitMBPP, restrict the check to the FitHE analog, and flag the positional reading.

**K15. No novelty list is frozen, and the differential's budget column is out of date.**
- **Problem:**
  - Rows where another work is P must not be claimed: rows 2, 3, 5, 8, and 9.
  - Row 15 must read "joint attribution, with intervals, of a probe-versus-stated gap on code".
  - Row 16 (TOST) is standard practice.
  - Rows 3, 4, and 13 are coded "T", but the design does not attribute them.
  - Suspicion, not verified: A codes from keyword searches against a "full read" definition.
- **Fix:** add a "Claims of novelty" subsection mapped to the differential rows, and regenerate the budget column from R2.

**K16. The title claims more than the design supports.**
- **Problem:** "... the calibration disconnect in code language models" generalizes beyond the six models, the primary metric is discrimination, and the glossary bans "disconnect" as a measured quantity.
- **Fix:** add title rules.

**K17. The power caveats are only partly carried into the design.**
- **Problem:**
  - "At least 0.97" has no inline refit-noise caveat.
  - The re-partitioning limit is omitted.
  - The driver 1 comparison mixes rules.
  - R_pool, the naming rule, and the reconciliation checks have no power analysis.
  - τ_R comes from pooled AUROC and is applied to W.
- **Fix:**
  - Qualify the power figures.
  - Add the re-partitioning limit.
  - Correct driver 1.
  - Give planning half-widths for the reconciliation checks.
  - State that "inconclusive" is not evidence of a gap.

## MINOR

- **K18.** "The field already reads differences of this size as ties" rests on K3 and on point estimates. Reason 2 mixes units. Tone both down.
- **K19.** "Trained on the probe's labels" suggests distillation. Say "the same execution labels and folds".
- **K20.** "Stated" is used for token-probability readouts. Define it once and say "Yes/No readout" in the outcome sentences.
- **K21.** "The confound it measures is the one in 2609.33290" calls another paper's comparison a confound.
- **K22.** "TMLR's exact disclosure wording": the rubric gives a requirement (a first-page footnote, TMLR_RUBRIC.md:58), not wording.
- **K23.** K6 pivots "under the TMLR Reproducibility certification criteria". Certifications are awarded after acceptance, and analogs are not reproductions. Frame the pivot against the acceptance criteria.

## Strongest TMLR rejection argument (critic's text, condensed)

"The central test compares two supervised classifiers fit on the same labels: a linear probe on frozen states, and a LoRA adapter that attends to every state and is read through Yes/No logits. Equivalence or a stated lead is expected and says nothing about stated confidence as the field uses the term. The budget adds little:
- r is null by construction;
- d swaps the metric, and Campos already showed its effect;
- t changes format, capacity, and training at once;
- l is expected near zero.

The reconciliation shares no primary cell, and one target (the 2610.31820 tie) is not a published claim."

**Partial rebuttals in the design:**
- the probe family includes P3;
- the capacity ladder and the linear-head control address capacity;
- the V2 chain and the diagnostic splits address format and the d and l terms;
- pre-registration supports correctness.

**Not rebutted:** K2, K3, K13, and K1. The minimal fix, all inside the sign-off, is:
- the φ_t split;
- the template rewording;
- the 2610.31820 correction;
- one named discrepancy per paper.

The remaining objection would then be modest significance, which TMLR asks reviewers not to penalize.
