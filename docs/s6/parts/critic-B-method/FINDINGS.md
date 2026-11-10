# Critic B (methodologist, opus): findings on PIPELINE_DESIGN_R0.md

Saved by the orchestrator from the critic's returned text (the critic's own write was blocked). 24 findings: 3 blockers, 12 major, 9 minor.

## Blockers

- **F1 (1.2, 1.3, 7.3 "Tie-break. None."; mechanism verified).** R is computed after isotonic recalibration. S^T is continuous; isotonic maps it to a few steps, so samples of one problem become ties and W of S is pulled toward 0.5. The probe is never recalibrated, so R is biased upward. The power simulation hides this because it rounds the stated score to 11 bins before isotonic (power_sim.py:39-40, 108). Fix: compute R at r = 0 for AUROC, or rank by (iso(S), S), or recalibrate P too; report tie rates.
- **F2 (7.1, 7.4, 1.8).** The probe is linear on one vector; S^T is a rank-16 LoRA attending to every token at every layer. Matching labels, folds, and loss does not match capacity, so H1 would overclaim. Fix: stronger probes on captured data (a p3 probe, multi-layer or attention-pooled probe); test R against the strongest; add a LoRA plus linear-head control.
- **F3 (12.2; verified).** The original-suite adapter trains on 0.8 x 15,970 samples (including LCB); the EvalPlus adapter on 0.8 x 5,420. phi_l also changes training population and volume. Fix: fit the 16-cell game on the 542-problem population only.

## Major

- **F4 (verified).** Isotonic fit on S^T's out-of-fold scores leaks test-fold labels (stacking leak). Fix: nested cross-fitting.
- **F5 (K4, verified).** Retry trigger uses test-fold log loss and only S^T gets a retry. Fix: inner-validation loss, or fix the recipe on the pilot.
- **F6 (verified).** The probe selects among 35 configurations by inner CV; S^T has a fixed recipe. At about 68 optimizer steps (4,336 / 64), early stopping checked every 200 steps never fires. Fix: a small inner-CV grid for S^T.
- **F7.** The label toggle refits P but only rescores the zero-shot readout. Fix: split into fitting labels and scoring labels.
- **F8.** Per-suite exclusions and suite-specific mixed sets break pairing across cells. Fix: intersection of problems valid under both suites.
- **F9.** phi_d mixes the switch to mixed problems only, within-problem conditioning, and artifacts of pooling out-of-fold scores of five separately fit models. Fix: also report pooled AUROC on mixed problems only and fold-averaged pooled AUROC.
- **F10.** No decision region for R below minus delta. Fix: a minimum-effect inferiority hypothesis.
- **F11 (verified).** delta justification fails: point 2 (smallest decidable margin) contradicted by POWER.md (delta 0.02 gives 1.00/1.00); point 3 omits Campos "trained methods reach higher within-problem AUROCs of 0.69-0.78 only for gpt-oss in distribution" (2611.07876.txt:565-566); point 1 carries a pooled tie width into a within-problem metric.
- **F12.** Folds are a fixed hash, so "three fold seeds" is undefined; P averaged over three partitions while S^T uses one; LoRA refit variance from 3 seeds on one model combined with a percentile interval by an unstated rule.
- **F13.** The power simulation has no fitting, no refit per suite, and a pre-binned S; its half-widths are lower bounds.
- **F14.** The pilot can reveal one model's Gamma cells, including R, before freeze; K2 lets the primary population change after the pilot.
- **F15.** Delta_g mixes base rate and k = 4 vs 10 with the readout effect; the probe is never scored on fresh generations; the five-player game does not say whether t = 1 means S^T or S^R.

## Minor

- **F16.** Line 91 says raw gap "minus the four terms" equals the residual; the formula gives G0 + sum phi = R.
- **F17.** Forward and reverse orders swapped relative to power_sim.py.
- **F18.** Campos within-problem criterion [0.45, 0.55] for the prompt-only probe cannot fail (W = 0.5 by construction).
- **F19.** Reconciliation tolerance and tie criteria ambiguous; the Ribeiro ordering test likely underpowered.
- **F20.** The full-suite LCB sensitivity labels on the 20 percent agreement inputs.
- **F21.** Extraction failures are easy negatives for every readout; position p2 undefined for them.
- **F22.** Isotonic does little to the problem-demeaned Brier.
- **F23.** H3 called descriptive but gets "confirmatory" Bonferroni intervals.
- **F24.** The H1 sentence names every term even if its interval includes zero.

Not checked by the critic: Campos's in-distribution P(Yes) within-problem value; Miglani Table 1 values quoted in 1.6.
