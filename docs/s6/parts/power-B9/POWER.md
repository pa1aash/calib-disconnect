# B9 power simulation (wave 6 Part B): systematics budget

Status: design-stage planning arithmetic under stated assumptions. These are simulation assumptions, not results. No number here comes from model outputs or from the study data.

Files: `power_sim.py` (numpy only, deterministic seeds), `power_sim.json` (assumptions, calibration, full grid, delta sensitivity, Shapley CI widths, recommendation). Baseline `docs/s6/power/w5-baseline/` was read and not edited.

## Command log

| Step | Command | Exit | Output |
|---|---|---|---|
| Smoke test | `python3 -I docs/s6/parts/power-B9/power_sim.py --quick` | 0 | wrote a quick JSON (5 s), deleted afterward |
| Full run | `python3 -I docs/s6/parts/power-B9/power_sim.py` | 0 | `power_sim.json`, runtime 1412 s (23.5 min wall, 8 worker processes, machine heavily loaded by other jobs) |

Versions: numpy 2.4.4, Python 3 (version string in the JSON). Base seed 20261110; each grid cell uses `SeedSequence([seed, stream, cell index])`, so results do not depend on process scheduling. Bootstrap B = 400; 200 replicates for decision probabilities; 60 replicates for Shapley CI widths.

## Design as implemented

- Scores: s_P = d_P y + 0.8 z + e_P; s_S = d_S y + 0.3 z + e_S; corr(e) = 0.5; stated score rounded to 11 bins; z is the standardized logit of p ~ Beta(0.6, 0.5), shared across models. Probe within AUROC 0.72 (before heterogeneity); zero-shot stated d0 gives realized within AUROC 0.60 after rounding (calibration block: 0.5998 to 0.6027).
- Trained stated separation d1 is calibrated per (k, true R) so the population residual R (all toggles on, including cross-fit isotonic) equals the scenario value; achieved values match to 4 decimals (calibration block, 30000 problems).
- Weak suite: 8 percent of failing samples (in expectation) become false passes, concentrated at mid-range p (Gaussian weight, SD 0.15 around 0.5).
- Toggles RECAL, TRAIN, DIFF, LABEL give 16 cells. Shapley is exact; both sequential orders are reported in the JSON.
- Multi-model: per-model, per-problem probe shocks (SD 0.05 AUROC units), independent across models; bootstrap resamples problems jointly across models.
- Decisions at delta: equivalence if the 5th percentile of R exceeds -delta and the 95th is below delta; superiority if the 5th percentile exceeds delta; else inconclusive.

Full assumption list: the `ASSUMPTIONS` dict, copied into the JSON.

## Recommendation (M = 9, delta = 0.03)

Rule: smallest k*n with P(equivalence | R = 0) >= 0.80 and P(superiority | R = 0.06) >= 0.80.

- Smallest qualifying cell in the grid: k = 8, n = 542 (P(equivalence | R=0) = 1.00, P(superiority | R=0.06) = 1.00). That is the grid floor for both k and n, so the true minimum may be lower; the grid did not probe below it.
- Main setting k = 10, n = 542 also qualifies (1.00 and 1.00), as do all 9 grid cells at M = 9. The recommendation is k = 10 with n = 542 (all problems available) for margin; moving to n = 1600 buys little at M = 9 and is not needed for these two checks.
- The decision is not the binding limit at M = 9. The binding limit is the boundary region: at true R = 0.03 (equal to delta), P(inconclusive) is 0.87 to 0.90 at every n, by construction. At delta 0.02 and true R = 0.015, P(equivalence) is 0.40 at n = 542 and 0.76 at n = 1600 (k = 10, M = 9).

Caution on optimism at M = 9: in this simulation outcomes are independent across models given p_i and the shocks are independent across models, so the mean over 9 models has a much narrower interval than it would if models share problem-level error. The baseline shared the shocks across models. If real shocks are shared, M = 9 behaves closer to the M = 1 rows below. Treat M = 9 power as an upper bound under these assumptions.

## Per-model power (M = 1, k = 10, delta 0.03)

| n | P(equiv, R=0) | P(sup, R=0.06) | P(LB>0, R=0.015) | P(sup, R=0.05) |
|---|---|---|---|---|
| 542 | 0.67 | 0.865 | 0.34 | 0.585 |
| 900 | 0.895 | 0.94 | 0.485 | 0.83 |
| 1600 | 1.00 | 0.995 | 0.74 | 0.895 |

(The third column is P(lower bound > 0) at R = 0.015, from the `p_lower_bound_gt_0` field.) Per-model equivalence at R = 0 reaches 0.80 only near n = 900 at k = 10 (0.895; 0.795 at k = 8, n = 900). At n = 542, k = 16 gives 0.925 for M = 1. Superiority at R = 0.06 passes 0.80 at every M = 1 cell with k >= 8 and n >= 542 (0.84 at the worst, k = 8, n = 542).

## Delta sensitivity (M = 9, k = 10)

| n | R true | delta 0.02: eq / sup | delta 0.03: eq / sup | delta 0.05: eq / sup |
|---|---|---|---|---|
| 542 | 0 | 1.00 / 0 | 1.00 / 0 | 1.00 / 0 |
| 542 | 0.06 | 0 / 1.00 | 0 / 1.00 | 0 / 0.84 |
| 1600 | 0 | 1.00 / 0 | 1.00 / 0 | 1.00 / 0 |
| 1600 | 0.06 | 0 / 1.00 | 0 / 1.00 | 0 / 0.99 |

Intermediate true R values are in the JSON. A true R equal to delta is always mostly inconclusive.

## Shapley terms and CI widths (M = 9, k = 10; mean over 60 replicates)

Mean 95 percent CI half-width in AUROC units, with mean point value (true R = 0 / true R = 0.06 for the point values; half-widths were within 0.0005 across the two R values, so they are shown for R = 0 only).

| Term | Point (R=0 / R=0.06) | Half-width n=542 | Half-width n=1600 |
|---|---|---|---|
| G0 (raw gap) | 0.1648 / 0.1647 | 0.0051 | 0.0030 |
| R | 0.0004 / 0.0601 | 0.0073 | 0.0043 |
| Shapley RECAL | 0.0017 / 0.0017 | 0.0009 | 0.0003 |
| Shapley TRAIN | -0.1012 / -0.0481 | 0.0017 | 0.0010 |
| Shapley DIFF | -0.0692 / -0.0653 | 0.0063 | 0.0037 |
| Shapley LABEL | 0.0042 / 0.0071 | 0.0027 | 0.0015 |

Point values at n = 1600 are within 0.0011 of these. The point values depend on the assumed loadings (a_P = 0.8, a_S = 0.3) and the false-pass fraction; they show how the decomposition is estimated, not what it will be. The DIFF term has the widest interval because pooled-versus-within AUROC both enter. Order dependence is large for TRAIN and DIFF (for example at R = 0, TRAIN is -0.0919 sequentially forward, -0.1139 reversed, -0.1012 Shapley), which is why Shapley is the primary decomposition.

Mean number of mixed problems per model (both a pass and a fail under the true label): 360.9 of 542 and 1070.0 of 1600 at k = 10 (R = 0; R = 0.06 gives 363.5 and 1068.5). Across the grid it ranges from about 340 (k = 8, n = 542) to 1187 (k = 16, n = 1600).

## Limits

Monte Carlo SE of a probability near 0.8 is about 0.028 at 200 replicates. B = 400 bootstrap draws (study: 10000) slightly widens percentile tails relative to the study. Calibration targets are population values; realized R at a single draw varies, as the replicates show. Probabilities of exactly 1.00 or 0 mean "not observed in 200 replicates", not certainty. The quick-mode smoke file was deleted; the log of the full run was folded into this file.
