# Power audit R2 (wave 7, power-B2): three decisions under heterogeneity, refit noise, and a realistic mixed fraction

Status: design-stage planning arithmetic under stated assumptions. Nothing here is a result; no study data, model output, or primary-model Gamma cell is used. Per-model inputs are ASSUMED (see "Inputs"), not model-card values. Files in `docs/s7/parts/power-B2/`: `power_sim_r2.py` (main), `power_sim_r2_refit_sweep.py` (supplement), `make_tables.py` (tables and thresholds from the JSON), `config_models.json`, `power_r2.json` (assumptions, derivations, grids, all results), `power_r2_refit_sweep.json`, `thresholds_r2.json`, `tables_generated.md`. The wave 6 files in `docs/s6/power/` were read and not edited.


**Two refit rules are reported.** Everything above the section "R2 refit rule rerun" uses the R1 refit rule (3 seeds, LoRA refit on 2 sub-study models, variance scaled by 6/2) and is kept as the R1 record. The section "R2 refit rule rerun" at the end applies the revised rule (repeated cross-fitting of every readout of every model) and is the audit for the margin rule if R2 adopts that rule.

## Headline (R1 refit rule)

1. **Margin rule.** At delta = 0.02 the minimum over D1, D2, D3 of the audited power is at most 0.50 at n = 542 in every heterogeneity setting and both k (T1), and at most 0.55 anywhere on the n sweep up to 900 (T2). The rule gives **delta = 0.03**.
2. **delta = 0.03 itself does not reach 0.90 for D1.** Under the assigned refit noise (relative SD 0.10 for the LoRA readout, 0.05 for the probe) and the widening rule, P(D1 | R = 0) at n = 542 is 0.78 (k = 10) and 0.86 (k = 20) at nominal heterogeneity; D2 and D3 are 0.86 to 0.97. The shortfall is caused by the refit widening, not by sample size: with the widening removed the same cells are 0.96 to 0.99 (T1, "min unwidened"), and with refit noise removed they are 1.00 (T4).
3. **Pilot threshold (mixed problems per model, mean of six), delta = 0.03.** With the assumed refit noise, **no mixed count on the sweep reaches 0.90 on all three decisions** (k = 10: max min-power 0.82 at 387 mixed; k = 20: 0.88 at 461 mixed; T3). The one interpolated crossing (conservative heterogeneity, k = 20, 444 mixed) was not confirmed by a separate-seed run at that size (min power 0.875, 800 replicates). If the refit relative SD is half as large (0.05 LoRA, 0.025 probe): **126 mixed (k = 10) and 71 (k = 20)**; at a quarter: 104 and 61. The analytic mixed count at n = 542 is 233 (k = 10) and 277 (k = 20) under the assumed mu and kappa 0.801 (T8).
4. **Implication for the k rule.** Because the binding limit is refit noise, which does not shrink with n or k, a pilot mixed count cannot restore 0.90 at the nominal refit noise. The pilot should measure the seed-to-seed SD of the trained readout's W (see "Limits"); k = 20 helps by about 0.08 on D1 (T1), not more.

## Command log

| Step | Command (cwd `<repo>`) | Result |
|---|---|---|
| Quick | `python3 -I docs/s7/parts/power-B2/power_sim_r2.py --quick` | 13 s, wrote `power_r2_quick.json` (deleted) |
| Full | `python3 -I docs/s7/parts/power-B2/power_sim_r2.py` | `power_r2.json`, 2163 s wall, 8 worker processes, machine load average above 100 from other jobs |
| Supplement | `python3 -I docs/s7/parts/power-B2/power_sim_r2_refit_sweep.py` | `power_r2_refit_sweep.json`, 420 s |
| Tables | `python3 -I docs/s7/parts/power-B2/make_tables.py` | `tables_generated.md`, `thresholds_r2.json` |

Versions: numpy 2.4.4, scipy 1.17.1. Base seed 20261110; each task uses `SeedSequence([seed, stream, ...])` keyed by heterogeneity setting, kappa, k, n, and world, so results do not depend on scheduling. Random numbers are common across the R* values of a group.

## Procedure (exact)

- **Worlds.** A world is one draw of the six models' parameters from a heterogeneity setting (seed stream 10). 40 worlds x 12 replicates = 480 replicates per decision cell (400 required). Worlds are shared across k, n, and R*. Calibration of the trained separation d1 per model uses 20000 (k = 10) or 10000 (k = 20) problems per model per world, a monotone interpolation (PCHIP) of the population within-AUROC of the stated readout over a separation grid, inverted at W_P minus (R* + u_m).
- **Bootstrap.** B = 500 problem-clustered resamples, shared by all models and by P and S, percentile 5 and 95 (90 percent interval), then widened: half-width sqrt(h^2 + (1.645 s_refit)^2) about the interval center.
- **Refit variance.** Fold seeds 0, 1, 2. Per model and seed, the separation of the probe is multiplied by (1 + e), e ~ N(0, 0.05^2), and the separation of the trained stated readout by (1 + e), e ~ N(0, 0.10^2). Seed 0 is the observed estimate (its perturbation is part of the point estimate); seeds 1 and 2 reuse the same generated data with new perturbations. s_refit^2 = Var(ddof 1, three seeds) of Rbar with the probe refit in all six models and S held at seed 0, plus (6 / 2) x Var(ddof 1, three seeds) of Rbar with the trained readout refit in the two sub-study models only and everything else at seed 0. The sub-study models are the first two in the config (see Inputs).
- **Decisions.** On the widened interval (L, U): D1 if -delta < L and U < delta; D2 if L > delta; D3 if U < -delta. Power = fraction of replicates. Unwidened rates are stored beside them.
- **MC error.** Two SEs are stored per probability: binomial over replicates and the cluster SE over the 40 worlds (SD of world-level rates / sqrt(40)). Tables show the larger. It is at most 0.034 for any D1/D2/D3 cell in T1 and typically 0.01 to 0.03.
- **R values.** R* in {0, 0.02, 0.03, 0.04, 0.06, -0.04, -0.06}. D1 at R* = 0; D2 at +2delta (0.04 or 0.06); D3 at -2delta; P(inconclusive) at R* = delta (0.02 or 0.03).
- **Lexicographic ties.** Per R1 section 1.2, W of the recalibrated readout equals W of the pre-map score, so the isotonic step does not enter R. In the Shapley cells pooled AUROC ranks by (isotonic value, bin).
- **Estimand check.** Mean over replicates of the observed Rbar minus R* is within 0.0003 for k = 10, n = 542, nominal (T-checks in `power_r2.json`, `mean_point` vs `R_true`).

## Assumptions and sources

| Quantity | Value | Source |
|---|---|---|
| Probe within-AUROC mean, zero-shot stated mean, loadings, per-problem separation shift, shock, error correlation, bins | 0.72, 0.60, 0.8 and 0.3, SD 0.3, 0.05 AUROC units, 0.5, 11 | carried from B9 (`docs/s6/power/power_sim.py` lines 28-61); planning assumptions |
| Pass probability | p ~ Beta(mu kappa, (1 - mu) kappa), per model; difficulty correlated across models by a Gaussian copula, correlation 0.7 | copula correlation is an assumption |
| Anchor, Qwen2.5-Coder-7B-Instruct | Random pass@rank-1 at T = 1.0: 0.645 (Table 5, extraction lines 1349-1350); pass@10 ceiling 0.959 (prose, line 1558); pass@1 baseline at T = 0.2: 0.851 (lines 1310, 1335) | `research/positioning/w4/parts/fetcher-l2/raw/2512.07404v3.txt`; 121 HumanEval tasks, 10 samples at T = 1.0 (lines 1235-1237, 1275) |
| Anchor, Mistral-7B-Instruct-v0.3 | Random 0.380 (prose line 1292, Table 5 line 1349); ceiling 0.678 (lines 1308, 1841); pass@1 baseline 0.347 (line 1292) | same file |
| Table 5 column order | Qwen 0.645 sits in the Random column by position in the garbled extraction (Mistral, Qwen, CodeLlama, OpenCoder order); the Mistral value is confirmed by prose, the Qwen value only by position | **verified for Mistral, positional for Qwen** |
| kappa fits | Qwen: 1.835 (ceiling plus or minus 1 binomial SE: 1.414 to 2.633); Mistral: 0.801 (0.616 to 1.034). Fit solves 1 - E[(1-p)^10] = ceiling at the given mu. The ceiling is one realization over 121 tasks, so these are noisy | `power_r2.json` `kappa_analysis` |
| Greedy to T = 1 relation | Not defensible: the two anchors move opposite ways (-20.6 and +3.3 points between the T = 0.2 baseline and T = 1.0 Random), and the baseline is T = 0.2 not greedy. Rule used: mu is the candidate mapping with fewer mixed problems; for mu above 0.5 that is the unshifted value | `power_r2.json` `greedy_to_T1_rule`, function `map_greedy_to_mu` |
| kappa used | 0.801 (primary; the smaller fit gives fewer mixed, since the mixed fraction rises with kappa, T7). 1.835 and 0.40 as sensitivity and stress | rule: fewer mixed |
| 2610.31820 Table 3 code AUROC | Verbalized .60/.61, .58/.60; R-Tuning .86/.85, .89/.79; Probe .88/.84, .89/.80 (ID/OOD; Qwen3-8B then Nemotron-Cascade-8B) | `research/positioning/w5/parts/ft-A4b/raw/ft/2610.31820.txt` (lines 385, 423, 442, 481, 519, 538 of the extraction); `research/positioning/w6/R2610_31820_PROTOCOL.md` line 41 |
| Campos Table V within-problem AUROC, in distribution | Qwen3-Coder-30B: judging pass .553, code token .620, prompt token .514; gpt-oss-20b: .772, .781, .524 | `research/positioning/w4/parts/fetcher-l2/raw/2611.07876.txt` lines 541-558 |

### Heterogeneity SDs and derivations

All SDs are sample SDs (ddof 1) computed in `derive_taus()`.

| SD | nominal | conservative | extreme | Derivation |
|---|---|---|---|---|
| tau_R (residual gap) | 0.02 | 0.04 | 0.06 | nominal: SD of pooled R-Tuning minus probe over 4 cells (-.02, +.01, 0, -.01) = 0.0129, rounded up to 0.02; conservative: SD of the two Campos within-problem gaps judging minus code token (-.067, -.009) = 0.0410; extreme: the larger Campos gap magnitude 0.067, used as an SD (overstatement) |
| tau_P (probe within-AUROC) | 0.04 | 0.08 | 0.114 | nominal: SD of the 4 pooled probe AUROCs = 0.0411 (applied to within AUROC by assumption); extreme: SD of the two Campos code-token within-AUROCs (.620, .781) = 0.1138; conservative: twice nominal |
| tau_0 (zero-shot within-AUROC) | 0.02 | 0.03 | 0.05 | nominal: SD of the 4 pooled verbalized AUROCs = 0.0126, rounded up; others assumed |
| tau_aP, tau_aS (loadings) | 0.22, 0.11 | 0.30, 0.15 | 0.40, 0.20 | tuned so the between-model SD of the raw gap G0 matches the SD of the 4 pooled probe-minus-verbalized gaps (.28, .23, .31, .20) = 0.0493. Population check (T9): nominal 0.0435, conservative 0.0699, extreme 0.0925 |
| tau_f (weak-suite false-pass fraction, mean 0.08) | 0.03 | 0.05 | 0.08 | assumption; no source located |

Fixed effects: R_m = R* + u_m, u_m ~ N(0, tau_R^2), centered to mean zero per world (named-model mean exactly R*). Random effects (sensitivity only): u_m not centered; the decision is still judged against R*.

### Inputs (provisional)

Final primary names per the orchestrator (A1 section 4). No A1 record states HumanEval+/MBPP+ pass@1 or pass@10 at T = 1.0 for them, so mu at T = 1.0 is assumed conservatively high: 0.80 for Qwen3-14B, Olmo-3.1-32B, gemma-4-31B and 0.72 for Qwen3-8B, Olmo-3-7B, gemma-4-12B. R1 names Qwen2.5-Coder-7B-Instruct and Qwen3-14B as the LoRA sub-study; Qwen2.5-Coder-7B is not in the final set, so Qwen3-8B and Qwen3-14B serve as the two sub-study models (assumption; only the count and mu enter). Mixed fraction to mu 0.90 is in T7. Rerun: put greedy values into `config_models.json` and run the same command.

## Results (generated by `make_tables.py` from the JSON)

### T1. Power at n = 542 (widened by the refit rule; SE in parentheses = larger of binomial and cluster-over-worlds SE)

| Heterogeneity | k | delta | mean mixed per model | D1 at R=0 | D2 at R=+2delta | D3 at R=-2delta | min | min unwidened | P(inconclusive) at R=delta | P(D1) at R=delta |
|---|---|---|---|---|---|---|---|---|---|---|
| nominal | 10 | 0.02 | 232.6 | 0.362 (0.022) | 0.704 (0.021) | 0.617 (0.024) | 0.362 | 0.675 | 0.873 | 0.060 |
| nominal | 10 | 0.03 | 232.6 | 0.777 (0.024) | 0.946 (0.011) | 0.858 (0.020) | 0.777 | 0.956 | 0.877 | 0.065 |
| nominal | 20 | 0.02 | 277.1 | 0.454 (0.025) | 0.733 (0.026) | 0.688 (0.027) | 0.454 | 0.865 | 0.842 | 0.075 |
| nominal | 20 | 0.03 | 277.1 | 0.858 (0.019) | 0.971 (0.008) | 0.875 (0.016) | 0.858 | 0.985 | 0.846 | 0.071 |
| conservative | 10 | 0.02 | 233.4 | 0.348 (0.027) | 0.644 (0.034) | 0.613 (0.025) | 0.348 | 0.683 | 0.883 | 0.065 |
| conservative | 10 | 0.03 | 233.4 | 0.767 (0.022) | 0.871 (0.025) | 0.858 (0.018) | 0.767 | 0.944 | 0.865 | 0.083 |
| conservative | 20 | 0.02 | 277.9 | 0.504 (0.025) | 0.721 (0.032) | 0.713 (0.023) | 0.504 | 0.871 | 0.838 | 0.100 |
| conservative | 20 | 0.03 | 277.9 | 0.873 (0.016) | 0.933 (0.018) | 0.912 (0.013) | 0.873 | 0.985 | 0.832 | 0.110 |
| extreme | 10 | 0.02 | 232.6 | 0.356 (0.025) | 0.592 (0.038) | 0.623 (0.025) | 0.356 | 0.690 | 0.827 | 0.117 |
| extreme | 10 | 0.03 | 232.6 | 0.798 (0.022) | 0.812 (0.040) | 0.856 (0.018) | 0.798 | 0.881 | 0.814 | 0.146 |
| extreme | 20 | 0.02 | 277.4 | 0.483 (0.033) | 0.635 (0.043) | 0.715 (0.025) | 0.483 | 0.823 | 0.808 | 0.119 |
| extreme | 20 | 0.03 | 277.4 | 0.831 (0.027) | 0.838 (0.039) | 0.883 (0.017) | 0.831 | 0.921 | 0.754 | 0.173 |

### T2. Sweep over n (mean mixed count per model), widened, kappa 0.80, delta = 0.03 then 0.02: D1 / D2 / D3

| Heterogeneity | k | n | mean mixed | delta 0.03 D1 / D2 / D3 | min | delta 0.02 D1 / D2 / D3 | min |
|---|---|---|---|---|---|---|---|
| nominal | 10 | 100 | 42.9 | 0.198 / 0.625 / 0.537 | 0.198 | 0.000 / 0.392 / 0.315 | 0.000 |
| nominal | 10 | 150 | 64.2 | 0.388 / 0.731 / 0.635 | 0.388 | 0.013 / 0.460 / 0.383 | 0.013 |
| nominal | 10 | 200 | 85.8 | 0.481 / 0.792 / 0.665 | 0.481 | 0.056 / 0.542 / 0.406 | 0.056 |
| nominal | 10 | 250 | 107.5 | 0.629 / 0.842 / 0.773 | 0.629 | 0.135 / 0.537 / 0.508 | 0.135 |
| nominal | 10 | 300 | 129.2 | 0.683 / 0.877 / 0.798 | 0.683 | 0.181 / 0.608 / 0.515 | 0.181 |
| nominal | 10 | 400 | 171.6 | 0.731 / 0.912 / 0.806 | 0.731 | 0.263 / 0.625 / 0.581 | 0.263 |
| nominal | 10 | 542 | 232.6 | 0.777 / 0.946 / 0.858 | 0.777 | 0.362 / 0.704 / 0.617 | 0.362 |
| nominal | 10 | 700 | 300.7 | 0.787 / 0.938 / 0.865 | 0.787 | 0.373 / 0.700 / 0.656 | 0.373 |
| nominal | 10 | 900 | 386.8 | 0.821 / 0.969 / 0.860 | 0.821 | 0.431 / 0.767 / 0.635 | 0.431 |
| nominal | 20 | 100 | 51.4 | 0.537 / 0.825 / 0.729 | 0.537 | 0.083 / 0.556 / 0.465 | 0.083 |
| nominal | 20 | 150 | 76.9 | 0.715 / 0.902 / 0.831 | 0.715 | 0.229 / 0.583 / 0.573 | 0.229 |
| nominal | 20 | 200 | 102.4 | 0.752 / 0.938 / 0.821 | 0.752 | 0.283 / 0.652 / 0.562 | 0.283 |
| nominal | 20 | 250 | 127.9 | 0.765 / 0.946 / 0.808 | 0.765 | 0.302 / 0.713 / 0.535 | 0.302 |
| nominal | 20 | 300 | 153.3 | 0.800 / 0.952 / 0.833 | 0.800 | 0.360 / 0.702 / 0.610 | 0.360 |
| nominal | 20 | 400 | 204.5 | 0.815 / 0.960 / 0.865 | 0.815 | 0.375 / 0.731 / 0.600 | 0.375 |
| nominal | 20 | 542 | 277.1 | 0.858 / 0.971 / 0.875 | 0.858 | 0.454 / 0.733 / 0.688 | 0.454 |
| nominal | 20 | 700 | 358.1 | 0.869 / 0.975 / 0.883 | 0.869 | 0.492 / 0.800 / 0.627 | 0.492 |
| nominal | 20 | 900 | 460.6 | 0.881 / 0.985 / 0.890 | 0.881 | 0.504 / 0.796 / 0.713 | 0.504 |
| conservative | 10 | 100 | 43.0 | 0.221 / 0.558 / 0.579 | 0.221 | 0.000 / 0.365 / 0.333 | 0.000 |
| conservative | 10 | 150 | 64.4 | 0.415 / 0.654 / 0.704 | 0.415 | 0.021 / 0.410 / 0.442 | 0.021 |
| conservative | 10 | 200 | 85.7 | 0.512 / 0.756 / 0.717 | 0.512 | 0.056 / 0.490 / 0.446 | 0.056 |
| conservative | 10 | 250 | 107.3 | 0.596 / 0.783 / 0.767 | 0.596 | 0.142 / 0.498 / 0.550 | 0.142 |
| conservative | 10 | 300 | 129.5 | 0.721 / 0.846 / 0.835 | 0.721 | 0.202 / 0.592 / 0.527 | 0.202 |
| conservative | 10 | 400 | 172.0 | 0.779 / 0.879 / 0.831 | 0.779 | 0.250 / 0.615 / 0.577 | 0.250 |
| conservative | 10 | 542 | 233.4 | 0.767 / 0.871 / 0.858 | 0.767 | 0.348 / 0.644 / 0.613 | 0.348 |
| conservative | 10 | 700 | 301.1 | 0.831 / 0.908 / 0.881 | 0.831 | 0.412 / 0.683 / 0.662 | 0.412 |
| conservative | 10 | 900 | 386.9 | 0.877 / 0.933 / 0.892 | 0.877 | 0.469 / 0.746 / 0.667 | 0.469 |
| conservative | 20 | 100 | 51.2 | 0.548 / 0.750 / 0.746 | 0.548 | 0.092 / 0.487 / 0.535 | 0.092 |
| conservative | 20 | 150 | 76.8 | 0.677 / 0.829 / 0.792 | 0.677 | 0.225 / 0.565 / 0.560 | 0.225 |
| conservative | 20 | 200 | 102.7 | 0.758 / 0.892 / 0.831 | 0.758 | 0.312 / 0.640 / 0.594 | 0.312 |
| conservative | 20 | 250 | 128.4 | 0.802 / 0.892 / 0.858 | 0.802 | 0.338 / 0.690 / 0.619 | 0.338 |
| conservative | 20 | 300 | 153.4 | 0.817 / 0.927 / 0.863 | 0.817 | 0.408 / 0.679 / 0.619 | 0.408 |
| conservative | 20 | 400 | 205.0 | 0.856 / 0.938 / 0.908 | 0.856 | 0.463 / 0.733 / 0.675 | 0.463 |
| conservative | 20 | 542 | 277.9 | 0.873 / 0.933 / 0.912 | 0.873 | 0.504 / 0.721 / 0.713 | 0.504 |
| conservative | 20 | 700 | 358.0 | 0.869 / 0.935 / 0.898 | 0.869 | 0.517 / 0.790 / 0.683 | 0.517 |
| conservative | 20 | 900 | 460.1 | 0.915 / 0.956 / 0.906 | 0.906 | 0.552 / 0.781 / 0.735 | 0.552 |

### T3. Mixed-count thresholds for min-power 0.90 (from thresholds_r2.json)

| Refit noise (rel SD LoRA / probe) | Heterogeneity | k | delta | mean mixed per model at 0.90 | equivalent n |
|---|---|---|---|---|---|
| 0.10 / 0.05 | nominal | 10 | 0.02 | not reached (max min-power 0.431 at the largest n) |
| 0.10 / 0.05 | nominal | 10 | 0.03 | not reached (max min-power 0.821 at the largest n) |
| 0.10 / 0.05 | nominal | 20 | 0.02 | not reached (max min-power 0.504 at the largest n) |
| 0.10 / 0.05 | nominal | 20 | 0.03 | not reached (max min-power 0.881 at the largest n) |
| 0.10 / 0.05 | conservative | 10 | 0.02 | not reached (max min-power 0.469 at the largest n) |
| 0.10 / 0.05 | conservative | 10 | 0.03 | not reached (max min-power 0.877 at the largest n) |
| 0.10 / 0.05 | conservative | 20 | 0.02 | not reached (max min-power 0.552 at the largest n) |
| 0.10 / 0.05 | conservative | 20 | 0.03 | 443.5 | 867.6 |
| 0.05 / 0.025 | nominal | 10 | 0.02 | not reached (max min-power 0.733 at n = 542) |
| 0.05 / 0.025 | nominal | 10 | 0.03 | 126.0 | 292.6 |
| 0.05 / 0.025 | nominal | 20 | 0.02 | 246.6 | 482.4 |
| 0.05 / 0.025 | nominal | 20 | 0.03 | 71.4 | 139.3 |
| 0.025 / 0.0125 | nominal | 10 | 0.02 | not reached (max min-power 0.871 at n = 542) |
| 0.025 / 0.0125 | nominal | 10 | 0.03 | 103.6 | 240.9 |
| 0.025 / 0.0125 | nominal | 20 | 0.02 | 141.6 | 277.0 |
| 0.025 / 0.0125 | nominal | 20 | 0.03 | 60.9 | 118.6 |

Verification runs at an interpolated n (800 replicates, separate seed stream 13):

- conservative_k20_n868: mean mixed 444.6; delta 0.03: D1 0.875, D2 0.941, D3 0.919 (800 replicates)

### T4. Sensitivities and stress tests at n = 542, delta = 0.03 then 0.02 (D1 | D2 | D3 | min; widened)

| Variant | k | mean mixed | delta 0.03 D1 | D2 | D3 | min | delta 0.02 D1 | D2 | D3 | min |
|---|---|---|---|---|---|---|---|---|---|---|
| main (nominal) | 10 | 232.6 | 0.777 | 0.946 | 0.858 | 0.777 | 0.362 | 0.704 | 0.617 | 0.362 |
| main (nominal) | 20 | 277.1 | 0.858 | 0.971 | 0.875 | 0.858 | 0.454 | 0.733 | 0.688 | 0.454 |
| random effects, nominal (sensitivity only) | 10 | 232.6 | 0.688 | 0.863 | 0.833 | 0.688 | 0.275 | 0.590 | 0.654 | 0.275 |
| random effects, nominal (sensitivity only) | 20 | 277.1 | 0.767 | 0.871 | 0.892 | 0.767 | 0.358 | 0.652 | 0.669 | 0.358 |
| random effects, conservative (sensitivity only) | 10 | 233.4 | 0.521 | 0.740 | 0.735 | 0.521 | 0.167 | 0.565 | 0.569 | 0.167 |
| random effects, conservative (sensitivity only) | 20 | 277.9 | 0.592 | 0.746 | 0.790 | 0.592 | 0.250 | 0.596 | 0.623 | 0.250 |
| kappa 1.835 (Qwen anchor) | 10 | 331.2 | 0.829 | 0.973 | 0.863 | 0.829 | 0.440 | 0.746 | 0.662 | 0.440 |
| kappa 1.835 (Qwen anchor) | 20 | 384.7 | 0.879 | 0.977 | 0.890 | 0.879 | 0.502 | 0.794 | 0.688 | 0.502 |
| kappa 0.40 (stress) | 10 | 152.9 | 0.706 | 0.894 | 0.802 | 0.706 | 0.233 | 0.631 | 0.575 | 0.233 |
| kappa 0.40 (stress) | 20 | 185.6 | 0.877 | 0.973 | 0.875 | 0.875 | 0.421 | 0.773 | 0.650 | 0.421 |
| no refit noise | 10 | 232.6 | 1.000 | 1.000 | 1.000 | 1.000 | 0.917 | 0.954 | 0.967 | 0.917 |
| no refit noise | 20 | 277.1 | 1.000 | 1.000 | 1.000 | 1.000 | 0.998 | 1.000 | 0.998 | 0.998 |
| refit noise x0.25 | 10 | 232.6 | 0.998 | 0.998 | 1.000 | 0.998 | 0.871 | 0.933 | 0.929 | 0.871 |
| refit noise x0.25 | 20 | 277.1 | 1.000 | 1.000 | 1.000 | 1.000 | 0.994 | 1.000 | 0.992 | 0.992 |
| refit noise x0.5 | 10 | 232.6 | 0.981 | 0.996 | 0.990 | 0.981 | 0.733 | 0.879 | 0.842 | 0.733 |
| refit noise x0.5 | 20 | 277.1 | 0.998 | 1.000 | 1.000 | 0.998 | 0.921 | 0.975 | 0.942 | 0.921 |
| LoRA refit noise only (probe noise 0) | 10 | 232.6 | 0.838 | 0.969 | 0.856 | 0.838 | 0.438 | 0.758 | 0.654 | 0.438 |
| LoRA refit noise only (probe noise 0) | 20 | 277.1 | 0.902 | 0.981 | 0.908 | 0.902 | 0.585 | 0.823 | 0.721 | 0.585 |
| refit noise x2 | 10 | 232.6 | 0.267 | 0.677 | 0.512 | 0.267 | 0.069 | 0.421 | 0.348 | 0.069 |
| refit noise x2 | 20 | 277.1 | 0.306 | 0.700 | 0.512 | 0.306 | 0.069 | 0.460 | 0.335 | 0.069 |
| problem-level het and shock shared by all models | 10 | 233.2 | 0.773 | 0.940 | 0.802 | 0.773 | 0.283 | 0.690 | 0.560 | 0.283 |
| problem-level het and shock shared by all models | 20 | 277.1 | 0.865 | 0.967 | 0.898 | 0.865 | 0.469 | 0.740 | 0.685 | 0.469 |
| M = 1 (one model, mu 0.80) | 10 | 206.6 | 0.006 | 0.479 | 0.304 | 0.006 | 0.000 | 0.362 | 0.200 | 0.000 |
| M = 1 (one model, mu 0.80) | 20 | 248.2 | 0.052 | 0.583 | 0.350 | 0.052 | 0.000 | 0.433 | 0.237 | 0.000 |

### T5. Interval components at n = 542, nominal, R = 0 (means over replicates)

| k | SD of point estimate | bootstrap half-width h | s_refit probe part | s_refit LoRA part (scaled by 3) | widened half-width |
|---|---|---|---|---|---|
| 10 | 0.0103 | 0.0097 | 0.0038 | 0.0072 | 0.016 |
| 20 | 0.0093 | 0.0066 | 0.0037 | 0.0073 | 0.0143 |

### T6. Shapley terms at M = 6, k = 10, n = 542, true R = 0 (B = 300, 8 worlds x 4 replicates; 95 percent percentile half-widths, no refit widening)

| Heterogeneity | Term | mean point | 95% half-width | between-model SD of per-model point |
|---|---|---|---|---|
| conservative | G0 | 0.172 | 0.0064 | 0.0592 |
| conservative | R | -0.002 | 0.0114 | 0.0308 |
| conservative | phi_RECAL | 0.002 | 0.0009 | 0.0009 |
| conservative | phi_TRAIN | -0.0933 | 0.0026 | 0.0649 |
| conservative | phi_DIFF | -0.086 | 0.0096 | 0.0642 |
| conservative | phi_LABEL | 0.0033 | 0.0036 | 0.0036 |
| nominal | G0 | 0.1854 | 0.0063 | 0.0465 |
| nominal | R | 0.002 | 0.0114 | 0.0191 |
| nominal | phi_RECAL | 0.0019 | 0.0009 | 0.0007 |
| nominal | phi_TRAIN | -0.1067 | 0.0025 | 0.039 |
| nominal | phi_DIFF | -0.0821 | 0.0095 | 0.0404 |
| nominal | phi_LABEL | 0.0035 | 0.0035 | 0.0026 |

### T7. Mixed fraction grid (analytic, 1 - E[p^k] - E[(1-p)^k], p ~ Beta(mu kappa, (1-mu) kappa))


10 samples per problem:

| kappa | mu 0.4 | mu 0.5 | mu 0.55 | mu 0.65 | mu 0.75 | mu 0.8 | mu 0.85 | mu 0.9 | mu 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 0.373 | 0.388 | 0.384 | 0.354 | 0.292 | 0.250 | 0.200 | 0.142 | 0.075 |
| 0.8 | 0.562 | 0.584 | 0.578 | 0.534 | 0.445 | 0.382 | 0.307 | 0.219 | 0.117 |
| 1.1 | 0.650 | 0.674 | 0.668 | 0.619 | 0.519 | 0.448 | 0.361 | 0.259 | 0.139 |
| 1.83 | 0.774 | 0.800 | 0.793 | 0.741 | 0.630 | 0.549 | 0.448 | 0.325 | 0.177 |
| 3.0 | 0.864 | 0.888 | 0.882 | 0.832 | 0.721 | 0.637 | 0.528 | 0.390 | 0.216 |
| 5.0 | 0.923 | 0.943 | 0.938 | 0.896 | 0.795 | 0.713 | 0.602 | 0.453 | 0.257 |

20 samples per problem:

| kappa | mu 0.4 | mu 0.5 | mu 0.55 | mu 0.65 | mu 0.75 | mu 0.8 | mu 0.85 | mu 0.9 | mu 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 0.450 | 0.468 | 0.464 | 0.428 | 0.355 | 0.304 | 0.244 | 0.173 | 0.092 |
| 0.8 | 0.660 | 0.684 | 0.678 | 0.630 | 0.529 | 0.458 | 0.371 | 0.267 | 0.144 |
| 1.1 | 0.750 | 0.775 | 0.769 | 0.718 | 0.611 | 0.533 | 0.435 | 0.316 | 0.172 |
| 1.83 | 0.867 | 0.890 | 0.884 | 0.837 | 0.730 | 0.648 | 0.540 | 0.402 | 0.224 |
| 3.0 | 0.938 | 0.955 | 0.951 | 0.915 | 0.825 | 0.749 | 0.640 | 0.490 | 0.283 |
| 5.0 | 0.976 | 0.986 | 0.984 | 0.962 | 0.897 | 0.833 | 0.734 | 0.581 | 0.349 |

### T8. Mixed fraction per model in the config

| Model | mu | kappa 0.801 k=10 | k=20 | kappa 1.835 k=10 | k=20 | kappa 0.40 k=10 | k=20 |
|---|---|---|---|---|---|---|---|
| Qwen/Qwen3-8B (thinking off) | 0.72 | 0.4771 | 0.5655 | 0.6704 | 0.7703 | 0.314 | 0.3806 |
| Qwen/Qwen3-14B (thinking off) | 0.8 | 0.3827 | 0.4583 | 0.5493 | 0.6487 | 0.2501 | 0.3041 |
| allenai/Olmo-3-7B-Instruct | 0.72 | 0.4771 | 0.5655 | 0.6704 | 0.7703 | 0.314 | 0.3806 |
| allenai/Olmo-3.1-32B-Instruct | 0.8 | 0.3827 | 0.4583 | 0.5493 | 0.6487 | 0.2501 | 0.3041 |
| google/gemma-4-12B-it | 0.72 | 0.4771 | 0.5655 | 0.6704 | 0.7703 | 0.314 | 0.3806 |
| google/gemma-4-31B-it (thinking off) | 0.8 | 0.3827 | 0.4583 | 0.5493 | 0.6487 | 0.2501 | 0.3041 |

Mean mixed count per model at n = 542 (analytic): {"k080_k10": 233.0, "k080_k20": 277.5, "k183_k10": 330.5, "k183_k20": 384.5, "k040_k10": 152.9, "k040_k20": 185.6}

### T9. Heterogeneity check (population level, 30 worlds)

| Setting | mean G0 | between-model SD of G0 | mean W_P | between-model SD of W_P |
|---|---|---|---|---|
| nominal | 0.1713 | 0.0435 | 0.7122 | 0.0364 |
| conservative | 0.1714 | 0.0699 | 0.7132 | 0.0716 |
| extreme | 0.1596 | 0.0925 | 0.7172 | 0.0901 |

## Reading the tables

- **Power table (T1).** At delta = 0.03: nominal heterogeneity, n = 542: k = 10 gives D1 0.777, D2 0.946, D3 0.858; k = 20 gives 0.858, 0.971, 0.875. Conservative and extreme heterogeneity move D1 by at most 0.02 and D2 by up to 0.13 (D2 at extreme, k = 10: 0.812 against 0.946 nominal; conservative 0.871). At delta = 0.02 D1 is 0.35 to 0.50 and the minimum is 0.35 to 0.55. P(inconclusive) at R = delta is 0.83 to 0.88 at both margins (nominal, conservative), the boundary region being unresolvable by construction.
- **Why heterogeneity matters little under fixed effects.** The estimand is the mean over the six named models, and the bootstrap resamples problems jointly, so tau_R enters only through the model-specific sampling noise of each R_m and the size of the perturbation (the trained separation d1 grows when R* is negative, so D3 carries more LoRA noise: s_refit LoRA part 0.0084 at R = -0.06 against 0.0056 at +0.06, T5-type values in the JSON). Random effects (T4) cut D1 to 0.69 / 0.52 (k = 10, nominal / conservative) because the realized mean of the six draws differs from R* by about tau_R / sqrt(6); labeled sensitivity only.
- **delta = 0.02 is out of reach because of the refit rule, not sampling noise.** Mean widened half-width is 0.016 (k = 10) and 0.014 (k = 20) at R = 0 against delta = 0.02, and the observed Rbar itself has SD 0.010 from sampling plus seed-0 perturbation.

## Powers at or near 1.00, and what drives them

Cells at or near 1.00 appear only after an assumption is removed; at the specified settings the widened powers are 0.35 to 0.97. Drivers:

1. **Averaging over six models with independent sampling noise.** Bootstrap half-width h of Rbar is 0.0097 at M = 6; at M = 1 the widened half-width is 0.040 (k = 10) and D1 at delta 0.03 falls to 0.006 (k = 10) and 0.052 (k = 20) (T4, M = 1). In the simulation, outcomes and score noise are independent across models given the difficulty copula (correlation 0.7), so the six estimates average almost like independent draws. The wave 6 value 1.00 came from this and from having no refit noise. Sharing the problem-level separation shift and shock across all models changes D1 at delta 0.03 from 0.777 to 0.773 (k = 10): problem-level sharing is already inside the paired problem bootstrap. What the simulation cannot show is model-level error shared across models beyond the problem bootstrap (for example a common prompt-format effect on the stated readout); M = 1 is the bound for that.
2. **Absence of fitting noise.** With no refit noise (T4) D1/D2/D3 at delta 0.03 are 1.000 for both k, and at delta 0.02 0.92 to 0.97 (k = 10) and 0.998 to 1.000 (k = 20). The wave 6 near-1.00 values are therefore reproduced when the readout is held fixed. Doubling the refit noise (0.20 / 0.10) drops D1 at delta 0.03 to 0.27 (k = 10) and 0.31 (k = 20).
3. **Mixed fraction.** Mean mixed per model is 233 of 542 (k = 10) against 361 in the wave 6 plan (Beta(0.6, 0.5)). With kappa 0.40 (153 mixed) D1 at delta 0.03 falls from 0.777 to 0.706 (k = 10); with kappa 1.835 (331) it rises to 0.829. The mixed fraction acts on h only, so it moves power less than the refit rule does.
4. **The 3-seed variance estimate.** Unwidened versus widened (T1): at delta 0.03, k = 10, the minimum over decisions falls from 0.956 to 0.777. The cost has two parts, the larger interval and the noise in s_refit itself (two degrees of freedom per component); the second is not separated here.
5. **Fixed effects.** D1/D2/D3 are judged against the mean of six named models; the random-effects rows show the loss if models are treated as draws.

## Limits

- The refit relative SD (0.10 LoRA, 0.05 probe) is an assumption; it decides the result. In AUROC units, a 10 percent change of a separation near 0.8 moves a model's W by about 0.02, which is large next to typical seed-to-seed spread of a fitted readout, but no source for that spread was located. At relative SD 0.05 the rule yields D1 0.98 at delta 0.03 (k = 10, n = 542), and at 0.025 / 0.0125 it yields 0.87 at delta 0.02 (T4). The pilot can measure this SD without touching a primary-model Gamma cell, and then the rule is re-evaluated; margins are set before data, so the audit as run says delta = 0.03.
- The primary rows use a single kappa (0.801) for all models and both benchmarks; kappa comes from two 7B models on HumanEval at T = 1.0 (121 tasks) and its ceiling is one realization (kappa range per SE in `kappa_analysis`). mu is assumed, not measured.
- The interpolated thresholds sit on curves with SE 0.01 to 0.03; the one interpolated crossing at the nominal refit noise failed its verification run.
- Sub-study models are placeholders drawn from the primary set.
- Shapley half-widths (T6) are 95 percent bootstrap percentile half-widths at 8 worlds x 4 replicates, B = 300, without refit widening; the R half-width there is therefore the bootstrap part only.
- The simulation fits no readouts, uses pre-binned stated scores, and has one probe per model; interval widths remain lower bounds as in wave 6. Per-model decisions are not simulated except M = 1.
- MC: replicate count 480 per cell (target 400); worlds-level SE accounts for heterogeneity draws. The machine was heavily loaded (load above 100), which affects wall time only.


## R2 refit rule rerun

Script `power_sim_r2_rule2.py` (imports `power_sim_r2.py` unchanged); merge and tables `merge_rule2.py`; raw output `power_r2_rule2.json`, also stored under key `r2_refit_rule` in `power_r2.json` and `thresholds_r2.json`. Runtime 921 s (8 workers, load above 100), command `python3 -I docs/s7/parts/power-B2/power_sim_r2_rule2.py`.

**Rule as implemented.** (a) Every readout of every model, the probe and the trained readout, is fit under fold seeds 0, 1, 2: per model and seed the probe separation is multiplied by (1 + e), e ~ N(0, 0.05^2), and the trained stated separation by (1 + e), e ~ N(0, 0.10^2), on the same generated data. (b) R_m is the mean over seeds of the per-seed R_m; Rbar is the mean over the six models; each bootstrap resample (B = 500, same problem resample for all models, readouts, and seeds) computes the seed-averaged Rbar; the interval is the 5th and 95th percentile. (c) sigma2_m = sample variance (ddof 1) of the three per-seed R_m; s2_refit = (1/3)(1/36) sum_m sigma2_m. (d) Half-width sqrt(h^2 + (1.645 s_refit)^2) about the interval center. No sub-study branch. Everything else (worlds, heterogeneity settings, kappa 0.801, assumed mu, R values, decisions) is as in the R1-rule run. Replicates: 480 per headline cell (40 worlds x 12); 300 per sweep cell (30 x 10; sweep n = 100 to 400, plus the n = 542 headline cell); 480 per verification run (separate seed stream 24). Stress: refit relative SD doubled (0.20 trained, 0.10 probe), run at n = 542 only.

**Why the estimate is more precise.** The point estimate averages three fits, so its refit variance is one third of a single fit, and s_refit pools six models (12 df) instead of two components of 2 df. At n = 542, R = 0, nominal: SD of the point estimate 0.0079 (k = 10) and 0.0061 (k = 20), against 0.0103 and 0.0093 under the R1 rule; widened half-width 0.0124 and 0.0101, against 0.016 and 0.014 (T12 and the R1 T5).

### T11. R2 rule, power at n = 542 (widened; unwidened min in the last-but-one column; SE = larger of binomial and cluster SE)

| Refit noise | Heterogeneity | k | delta | mean mixed | D1 at R=0 | D2 at +2delta | D3 at -2delta | min | min unwidened | P(inconclusive) at R=delta |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.10 / 0.05 (primary) | nominal | 10 | 0.02 | 233.7 | 0.646 (0.024) | 0.846 (0.019) | 0.790 (0.019) | 0.646 | 0.804 | 0.875 |
| 0.10 / 0.05 (primary) | nominal | 10 | 0.03 | 233.7 | 0.973 (0.008) | 0.994 (0.004) | 0.979 (0.007) | 0.973 | 0.994 | 0.875 |
| 0.10 / 0.05 (primary) | nominal | 20 | 0.02 | 278.2 | 0.887 (0.016) | 0.956 (0.010) | 0.925 (0.012) | 0.887 | 0.952 | 0.883 |
| 0.10 / 0.05 (primary) | nominal | 20 | 0.03 | 278.2 | 1.000 (0.000) | 1.000 (0.000) | 0.998 (0.002) | 0.998 | 1.000 | 0.887 |
| 0.10 / 0.05 (primary) | conservative | 10 | 0.02 | 233.0 | 0.669 (0.025) | 0.804 (0.024) | 0.840 (0.018) | 0.669 | 0.812 | 0.873 |
| 0.10 / 0.05 (primary) | conservative | 10 | 0.03 | 233.0 | 0.973 (0.009) | 0.969 (0.011) | 0.981 (0.007) | 0.969 | 0.985 | 0.862 |
| 0.10 / 0.05 (primary) | conservative | 20 | 0.02 | 277.4 | 0.856 (0.019) | 0.944 (0.021) | 0.894 (0.019) | 0.856 | 0.963 | 0.867 |
| 0.10 / 0.05 (primary) | conservative | 20 | 0.03 | 277.4 | 0.994 (0.004) | 0.990 (0.007) | 0.988 (0.006) | 0.988 | 0.996 | 0.854 |
| 0.20 / 0.10 (stress, 2x) | nominal | 10 | 0.02 | 233.7 | 0.125 (0.015) | 0.617 (0.027) | 0.452 (0.029) | 0.125 | 0.621 | 0.902 |
| 0.20 / 0.10 (stress, 2x) | nominal | 10 | 0.03 | 233.7 | 0.644 (0.022) | 0.900 (0.014) | 0.725 (0.020) | 0.644 | 0.933 | 0.882 |
| 0.20 / 0.10 (stress, 2x) | nominal | 20 | 0.02 | 278.2 | 0.256 (0.021) | 0.708 (0.024) | 0.504 (0.025) | 0.256 | 0.840 | 0.902 |
| 0.20 / 0.10 (stress, 2x) | nominal | 20 | 0.03 | 278.2 | 0.812 (0.019) | 0.956 (0.011) | 0.785 (0.019) | 0.785 | 0.973 | 0.890 |
| 0.20 / 0.10 (stress, 2x) | conservative | 10 | 0.02 | 233.0 | 0.181 (0.018) | 0.598 (0.026) | 0.492 (0.025) | 0.181 | 0.671 | 0.882 |
| 0.20 / 0.10 (stress, 2x) | conservative | 10 | 0.03 | 233.0 | 0.723 (0.021) | 0.865 (0.019) | 0.758 (0.021) | 0.723 | 0.931 | 0.857 |
| 0.20 / 0.10 (stress, 2x) | conservative | 20 | 0.02 | 277.4 | 0.258 (0.029) | 0.715 (0.030) | 0.494 (0.026) | 0.258 | 0.810 | 0.869 |
| 0.20 / 0.10 (stress, 2x) | conservative | 20 | 0.03 | 277.4 | 0.771 (0.024) | 0.923 (0.021) | 0.742 (0.021) | 0.742 | 0.954 | 0.873 |

### T12. R2 rule, interval components at n = 542, R = 0 (means over replicates)

| Refit noise | Heterogeneity | k | SD of point estimate | bootstrap half-width h | rms s_refit | widened half-width |
|---|---|---|---|---|---|---|
| primary | nominal | 10 | 0.0079 | 0.0096 | 0.0049 | 0.0124 |
| primary | nominal | 20 | 0.0061 | 0.0065 | 0.0048 | 0.0101 |
| primary | conservative | 10 | 0.0078 | 0.0095 | 0.0047 | 0.0122 |
| primary | conservative | 20 | 0.0065 | 0.0065 | 0.0047 | 0.01 |
| 2x | nominal | 10 | 0.0117 | 0.0095 | 0.0097 | 0.0184 |
| 2x | nominal | 20 | 0.0099 | 0.0065 | 0.0096 | 0.0167 |
| 2x | conservative | 10 | 0.0112 | 0.0095 | 0.0094 | 0.0179 |
| 2x | conservative | 20 | 0.0106 | 0.0064 | 0.0095 | 0.0166 |

### T13. R2 rule, sweep over n (widened; D1 / D2 / D3 and min), then unwidened min

| Heterogeneity | k | n | mean mixed | delta 0.03 D1 / D2 / D3 | min | unwidened min | delta 0.02 D1 / D2 / D3 | min | unwidened min |
|---|---|---|---|---|---|---|---|---|---|
| nominal | 10 | 100 | 43.3 | 0.310 / 0.620 / 0.660 | 0.310 | 0.373 | 0.003 / 0.377 / 0.420 | 0.003 | 0.007 |
| nominal | 10 | 150 | 64.7 | 0.620 / 0.823 / 0.803 | 0.620 | 0.687 | 0.073 / 0.527 / 0.493 | 0.073 | 0.147 |
| nominal | 10 | 200 | 85.9 | 0.750 / 0.850 / 0.890 | 0.750 | 0.833 | 0.177 / 0.550 / 0.570 | 0.177 | 0.317 |
| nominal | 10 | 250 | 107.7 | 0.833 / 0.917 / 0.897 | 0.833 | 0.877 | 0.313 / 0.653 / 0.627 | 0.313 | 0.443 |
| nominal | 10 | 300 | 129.2 | 0.897 / 0.960 / 0.937 | 0.897 | 0.923 | 0.363 / 0.727 / 0.630 | 0.363 | 0.540 |
| nominal | 10 | 400 | 171.3 | 0.963 / 0.987 / 0.970 | 0.963 | 0.977 | 0.513 / 0.780 / 0.700 | 0.513 | 0.657 |
| nominal | 10 | 542 | 233.7 | 0.973 / 0.994 / 0.979 | 0.973 | 0.994 | 0.646 / 0.846 / 0.790 | 0.646 | 0.804 |
| nominal | 20 | 100 | 51.0 | 0.763 / 0.890 / 0.887 | 0.763 | 0.847 | 0.173 / 0.617 / 0.540 | 0.173 | 0.337 |
| nominal | 20 | 150 | 76.6 | 0.863 / 0.940 / 0.930 | 0.863 | 0.923 | 0.430 / 0.750 / 0.667 | 0.430 | 0.577 |
| nominal | 20 | 200 | 102.5 | 0.950 / 0.983 / 0.977 | 0.950 | 0.987 | 0.550 / 0.770 / 0.780 | 0.550 | 0.727 |
| nominal | 20 | 250 | 127.9 | 0.973 / 0.980 / 0.993 | 0.973 | 0.987 | 0.703 / 0.860 / 0.827 | 0.703 | 0.823 |
| nominal | 20 | 300 | 154.1 | 0.983 / 0.997 / 0.980 | 0.980 | 0.993 | 0.727 / 0.893 / 0.827 | 0.727 | 0.873 |
| nominal | 20 | 400 | 205.0 | 0.997 / 0.997 / 0.993 | 0.993 | 0.997 | 0.820 / 0.923 / 0.887 | 0.820 | 0.940 |
| nominal | 20 | 542 | 278.2 | 1.000 / 1.000 / 0.998 | 0.998 | 1.000 | 0.887 / 0.956 / 0.925 | 0.887 | 0.952 |
| conservative | 10 | 100 | 43.4 | 0.373 / 0.617 / 0.690 | 0.373 | 0.430 | 0.000 / 0.347 / 0.427 | 0.000 | 0.013 |
| conservative | 10 | 150 | 64.4 | 0.620 / 0.753 / 0.800 | 0.620 | 0.677 | 0.047 / 0.487 / 0.520 | 0.047 | 0.133 |
| conservative | 10 | 200 | 85.9 | 0.733 / 0.820 / 0.867 | 0.733 | 0.800 | 0.147 / 0.527 / 0.597 | 0.147 | 0.293 |
| conservative | 10 | 250 | 107.2 | 0.807 / 0.897 / 0.863 | 0.807 | 0.883 | 0.290 / 0.653 / 0.597 | 0.290 | 0.433 |
| conservative | 10 | 300 | 128.8 | 0.890 / 0.917 / 0.947 | 0.890 | 0.930 | 0.447 / 0.683 / 0.717 | 0.447 | 0.570 |
| conservative | 10 | 400 | 171.9 | 0.957 / 0.933 / 0.977 | 0.933 | 0.957 | 0.530 / 0.753 / 0.760 | 0.530 | 0.727 |
| conservative | 10 | 542 | 233.0 | 0.973 / 0.969 / 0.981 | 0.969 | 0.985 | 0.669 / 0.804 / 0.840 | 0.669 | 0.812 |
| conservative | 20 | 100 | 51.4 | 0.757 / 0.867 / 0.850 | 0.757 | 0.820 | 0.253 / 0.617 / 0.560 | 0.253 | 0.380 |
| conservative | 20 | 150 | 76.5 | 0.927 / 0.917 / 0.947 | 0.917 | 0.937 | 0.427 / 0.713 / 0.670 | 0.427 | 0.580 |
| conservative | 20 | 200 | 101.9 | 0.947 / 0.940 / 0.963 | 0.940 | 0.947 | 0.543 / 0.777 / 0.727 | 0.543 | 0.677 |
| conservative | 20 | 250 | 128.5 | 0.970 / 0.967 / 0.980 | 0.967 | 0.977 | 0.677 / 0.797 / 0.833 | 0.677 | 0.800 |
| conservative | 20 | 300 | 153.4 | 0.977 / 0.967 / 0.990 | 0.967 | 0.977 | 0.707 / 0.810 / 0.863 | 0.707 | 0.867 |
| conservative | 20 | 400 | 205.4 | 0.993 / 0.983 / 0.997 | 0.983 | 0.990 | 0.837 / 0.920 / 0.870 | 0.837 | 0.943 |
| conservative | 20 | 542 | 277.4 | 0.994 / 0.990 / 0.988 | 0.988 | 0.996 | 0.856 / 0.944 / 0.894 | 0.856 | 0.963 |

### T14. R2 rule, minimum mean mixed count per model for min-power 0.90 (T10 = k 10, T20 = k 20), with verification at the crossing

| Heterogeneity | k | delta | crossing: mean mixed (n) | verification run (separate seeds, 480 replicates): D1 / D2 / D3, min |
|---|---|---|---|---|
| nominal | 10 | 0.02 | no crossing on the available pool (n up to 542): max min-power 0.646 at n = 542 | not run |
| nominal | 10 | 0.03 | 131.1 (304.5) | 0.885 / 0.952 / 0.923, min 0.885 (mixed 131.5) |
| nominal | 20 | 0.02 | no crossing on the available pool (n up to 542): max min-power 0.887 at n = 542 | not run |
| nominal | 20 | 0.03 | 87.6 (171.3) | 0.940 / 0.975 / 0.942, min 0.940 (mixed 88.1) |
| conservative | 10 | 0.02 | no crossing on the available pool (n up to 542): max min-power 0.669 at n = 542 | not run |
| conservative | 10 | 0.03 | 138.8 (323.3) | 0.904 / 0.935 / 0.950, min 0.904 (mixed 139.4) |
| conservative | 20 | 0.02 | no crossing on the available pool (n up to 542): max min-power 0.856 at n = 542 | not run |
| conservative | 20 | 0.03 | 73.8 (144.7) | 0.919 / 0.929 / 0.942, min 0.919 (mixed 74.3) |


### Reading the R2-rule tables

- **Margin rule.** At delta = 0.02 the minimum over D1, D2, D3 is 0.65 (nominal) and 0.67 (conservative) at k = 10, the sample size the design starts with, and 0.89 and 0.86 at k = 20 (T11). The 0.90 condition fails at delta = 0.02, so the rule selects **delta = 0.03**. At delta = 0.03, n = 542, k = 10, all three decisions are at least 0.97 (nominal) and 0.97 (conservative), so delta = 0.03 satisfies the 0.90 condition under the R2 rule (it did not under the R1 rule).
- **Boundary.** P(inconclusive) at R = delta is 0.85 to 0.89 at both margins and both k, by construction.
- **Unwidened versus widened.** At delta = 0.03 the widening costs under 0.03 in the minimum power (0.994 to 0.973 at k = 10, nominal); at delta = 0.02 it costs 0.07 to 0.16 (0.804 to 0.646 at k = 10 nominal).
- **Stress (refit noise doubled).** At delta = 0.03, k = 10, D1 falls to 0.64 (nominal) and 0.72 (conservative), D3 to 0.73 and 0.76, so the 0.90 condition at delta = 0.03 holds only if the true refit relative SD is near the assumed 0.10 or smaller. With k = 20 the stress minimum is 0.785 (nominal) and 0.742 (conservative). The pilot's seed-to-seed spread of the trained readout is what settles this.
- **Near-1.00 values.** D2 and D3 1.000 at delta = 0.03 and k = 20 come from averaging six models with independent sampling noise (bootstrap half-width 0.0065 for the mean against 0.040 for one model, see the R1 section), averaging three seeds, and a mixed count of 278 per model. The stress row removes the third of these assumptions in the direction that matters: doubling the refit SD brings the same cells to 0.74 to 0.96.

### Mixed-count thresholds under the R2 rule (T14)

- **delta = 0.03.** Crossing of 0.90 for all three decisions at **131 mixed problems per model (k = 10, nominal)**, 139 (k = 10, conservative), **88 (k = 20, nominal)**, 74 (k = 20, conservative). Verification runs at the crossing size gave minimum power 0.885 (k = 10, nominal; 131.5 mixed), 0.904 (k = 10, conservative), 0.940 (k = 20, nominal), 0.919 (k = 20, conservative). The k = 10 nominal run is 0.015 below 0.90, within one Monte Carlo SE (about 0.015), so the crossing is confirmed only to that precision; a pilot threshold with margin is about 140 mixed (k = 10) and 90 (k = 20). The analytic mixed count at n = 542 is 233 and 277 under the assumed mu and kappa 0.801, so the expected count exceeds the margin-adjusted floors by a factor of about 1.7 (k = 10: 233 against 140) and 3.1 (k = 20: 277 against 90), if the assumed mu and kappa hold.
- **delta = 0.02.** No crossing exists on the available pool (n up to 542): the maximum minimum-power is 0.646 and 0.669 at k = 10 (nominal, conservative; 233 mixed), 0.887 and 0.856 at k = 20 (278 mixed). Beyond n = 542 was not simulated because the pool has 542 problems; at k = 20 nominal the curve is still rising (0.82 at 205 mixed, 0.887 at 278) so a crossing slightly above 278 mixed is possible but not tested.
- **Effect on the k rule.** The threshold is a mixed-count floor for delta = 0.03: if the pilot's measured count per model is below about 140 at k = 10, raise to k = 20 (floor about 90, and k = 20 raises the count per model by about 19 percent at the same n, from 233 to 277 under the assumed mu and kappa). Keep in mind that the stress run shows the floor is conditional on the refit noise assumed.

### Limits specific to the R2-rule run

- Sweep cells have 300 replicates (SE up to 0.03 near 0.90), below the 400 required only for the headline cells, which have 480.
- Interpolated crossings are linear between sweep points and noisy; the verification table is the check.
- The refit-noise structure (independent relative perturbations per model and seed, same data across seeds) is an assumption; real fold re-partitioning also changes which samples enter each fit, which would add variance not modeled here.
- Kappa, mu, and the heterogeneity SDs are those of the R1-rule run (assumptions above).


## Red-team follow-up

Scripts: `power_sim_r2_redteam.py` (imports `power_sim_r2.py` unchanged; run `python3 -I docs/s7/parts/power-B2/power_sim_r2_redteam.py`, 1637 s), `redteam_fix.py` (corrects and verifies the k = 20 threshold, see RT5), `merge_redteam.py` (stores results under `r2_refit_rule.redteam` in `power_r2.json` and `thresholds_r2.json`, writes the tables). Raw output `power_r2_redteam.json`. All runs use the R2 refit rule, refit relative SD 0.10 trained and 0.05 probe, kappa 0.801 unless a scenario changes it, delta 0.03 unless stated. Headline, heterogeneous-count, rho_e, and verification cells have 480 replicates (40 worlds x 12); sweep and scenario cells have 240 (20 worlds x 12), so their SE is up to about 0.03 near 0.90. Both widening multipliers are applied to the same replicates: z = 1.645 and t_{12, 0.95} = 1.782 (the multiplier on s_refit; the unwidened rate is also shown).

**Scenario construction.** In the mu scenarios all six mu values are shifted by a common offset chosen (analytic, `brentq`) so the mean mixed count at n = 542 hits a target (k = 10: 200, 170, 140, 120, 100; k = 20: 230, 190, 150, 120, 95, 75). Calibration of the trained separation is redone for every scenario. In the kappa scenarios kappa is 0.4, 0.5, 0.6, 0.7 with the assumed mu. For the heterogeneous-count run model 3 (mu 0.80) is moved to mu 0.9528 so it has about 60 mixed problems at k = 10; the other five keep their assumed mu (207 to 259 mixed, mean about 238).

### RT1. Widening multiplier 1.645 versus t = 1.782 (R2 rule, n = 542, 480 replicates; D1 / D2 / D3, min; SE of D1 in the last column)

| Heterogeneity | k | delta | mean mixed | unwidened | z = 1.645 | t = 1.782 | SE (t = 1.782, D1) |
|---|---|---|---|---|---|---|---|
| nominal | 10 | 0.03 | 233.4 | 0.994 / 0.994 / 0.996, min 0.994 | 0.983 / 0.994 / 0.981, min 0.981 | 0.979 / 0.992 / 0.979, min 0.979 | 0.007 |
| nominal | 10 | 0.02 | 233.4 | 0.802 / 0.890 / 0.915, min 0.802 | 0.704 / 0.854 / 0.831, min 0.704 | 0.685 / 0.848 / 0.812, min 0.685 | 0.021 |
| nominal | 20 | 0.03 | 277.6 | 1.000 / 1.000 / 1.000, min 1.000 | 0.994 / 0.998 / 0.996, min 0.994 | 0.994 / 0.998 / 0.994, min 0.994 | 0.004 |
| conservative | 10 | 0.03 | 233.4 | 0.994 / 0.977 / 0.998, min 0.977 | 0.983 / 0.971 / 0.990, min 0.971 | 0.981 / 0.971 / 0.983, min 0.971 | 0.006 |
| conservative | 10 | 0.02 | 233.4 | 0.806 / 0.871 / 0.910, min 0.806 | 0.673 / 0.812 / 0.829, min 0.673 | 0.662 / 0.804 / 0.817, min 0.662 | 0.024 |
| conservative | 20 | 0.03 | 277.6 | 0.998 / 0.992 / 1.000, min 0.992 | 0.996 / 0.990 / 0.996, min 0.990 | 0.994 / 0.990 / 0.996, min 0.990 | 0.004 |

(The k = 20, delta 0.02 cells are also in the JSON: nominal min 0.858 and conservative 0.848 at t = 1.782.)

### RT2. Heterogeneous mixed counts (k = 10, delta 0.03, n = 542, 480 replicates): one model at 60 mixed, five near 207 to 259

| Heterogeneity | mixed per model (six) | unwidened | z = 1.645 | t = 1.782 |
|---|---|---|---|---|
| nominal | [259.3, 207.5, 259.2, 60.0, 259.0, 208.2] | 0.954 / 0.975 / 0.979, min 0.954 | 0.919 / 0.963 / 0.948, min 0.919 | 0.915 / 0.963 / 0.942, min 0.915 |
| conservative | [259.3, 207.5, 259.2, 60.0, 259.0, 208.2] | 0.950 / 0.954 / 0.981, min 0.950 | 0.923 / 0.940 / 0.952, min 0.923 | 0.917 / 0.938 / 0.946, min 0.917 |

### RT3. Residual-error correlation rho_e (delta 0.03, n = 542, 480 replicates; baseline rho_e = 0.5 is in RT1)

| Heterogeneity | k | rho_e | SD of point | bootstrap h | t = 1.782: D1 / D2 / D3, min |
|---|---|---|---|---|---|
| conservative | 10 | 0.2 | 0.0079 | 0.0114 | 0.944 / 0.952 / 0.965, min 0.944 |
| conservative | 10 | 0.8 | 0.0061 | 0.0068 | 1.000 / 0.994 / 0.996, min 0.994 |
| nominal | 10 | 0.2 | 0.0084 | 0.0115 | 0.931 / 0.967 / 0.958, min 0.931 |
| nominal | 10 | 0.8 | 0.0065 | 0.0069 | 1.000 / 1.000 / 0.994, min 0.994 |
| nominal | 20 | 0.2 | 0.0065 | 0.0079 | 0.992 / 1.000 / 0.994, min 0.992 |
| nominal | 20 | 0.8 | 0.0053 | 0.0047 | 1.000 / 1.000 / 0.998, min 0.998 |

### RT4. Min power (t = 1.782, delta 0.03) versus mean mixed count and mean pass-fail pairs per model

n sweep: 240 replicates per point (20 worlds x 12) except the n = 542 point (480). mu and kappa scenarios: n = 542, nominal heterogeneity, 240 replicates, all six models' mu shifted together (offset in `scenario_info`) or kappa changed.

| k | scenario | setting | mean mixed | mean pairs | D1 / D2 / D3 | min |
|---|---|---|---|---|---|---|
| 10 | n_sweep | n = 150 | 64.7 | 1090 | 0.579 / 0.804 / 0.733 | 0.579 |
| 10 | n_sweep | n = 200 | 85.5 | 1440 | 0.725 / 0.842 / 0.854 | 0.725 |
| 10 | n_sweep | n = 250 | 107.9 | 1822 | 0.846 / 0.942 / 0.892 | 0.846 |
| 10 | n_sweep | n = 300 | 128.8 | 2173 | 0.867 / 0.958 / 0.908 | 0.867 |
| 10 | n_sweep | n = 400 | 172.0 | 2900 | 0.967 / 0.983 / 0.975 | 0.967 |
| 10 | n_sweep | n = 542 | 233.4 | 3928 | 0.979 / 0.992 / 0.979 | 0.979 |
| 10 | mu_sweep | mu offset +0.1555 | 100.4 | 1653 | 0.675 / 0.838 / 0.838 | 0.675 |
| 10 | mu_sweep | mu offset +0.1365 | 120.5 | 1987 | 0.762 / 0.863 / 0.871 | 0.762 |
| 10 | mu_sweep | mu offset +0.1164 | 140.2 | 2321 | 0.858 / 0.912 / 0.921 | 0.858 |
| 10 | mu_sweep | mu offset +0.0836 | 170.3 | 2832 | 0.904 / 0.963 / 0.917 | 0.904 |
| 10 | mu_sweep | mu offset +0.0469 | 200.2 | 3347 | 0.929 / 0.971 / 0.975 | 0.929 |
| 10 | mu_sweep | baseline (mu 0.72/0.80, kappa 0.801, n = 542) | 233.4 | 3928 | 0.979 / 0.992 / 0.979 | 0.979 |
| 10 | kappa_sweep | kappa 0.4 | 152.7 | 2515 | 0.904 / 0.954 / 0.946 | 0.904 |
| 10 | kappa_sweep | kappa 0.5 | 177.0 | 2935 | 0.946 / 0.975 / 0.958 | 0.946 |
| 10 | kappa_sweep | kappa 0.6 | 198.2 | 3303 | 0.942 / 0.971 / 0.975 | 0.942 |
| 10 | kappa_sweep | kappa 0.7 | 216.6 | 3626 | 0.950 / 0.983 / 0.979 | 0.950 |
| 10 | kappa_sweep | baseline (mu 0.72/0.80, kappa 0.801, n = 542) | 233.4 | 3928 | 0.979 / 0.992 / 0.979 | 0.979 |
| 20 | n_sweep | n = 150 | 76.6 | 4581 | 0.921 / 0.958 / 0.938 | 0.921 |
| 20 | n_sweep | n = 200 | 102.5 | 6111 | 0.950 / 0.983 / 0.954 | 0.950 |
| 20 | n_sweep | n = 250 | 127.6 | 7620 | 0.975 / 0.992 / 0.971 | 0.971 |
| 20 | n_sweep | n = 300 | 153.5 | 9161 | 0.988 / 0.996 / 0.979 | 0.979 |
| 20 | n_sweep | n = 400 | 204.9 | 12217 | 1.000 / 1.000 / 0.988 | 0.988 |
| 20 | n_sweep | n = 542 | 277.6 | 16570 | 0.994 / 0.998 / 0.994 | 0.994 |
| 20 | mu_sweep | mu offset +0.1896 | 75.2 | 4251 | 0.412 / 0.708 / 0.667 | 0.412 |
| 20 | mu_sweep | mu offset +0.1754 | 95.3 | 5406 | 0.821 / 0.892 / 0.887 | 0.821 |
| 20 | mu_sweep | mu offset +0.1568 | 120.4 | 6871 | 0.950 / 0.975 / 0.963 | 0.950 |
| 20 | mu_sweep | mu offset +0.133 | 150.4 | 8652 | 0.958 / 0.975 / 0.963 | 0.958 |
| 20 | mu_sweep | mu offset +0.0978 | 190.6 | 11074 | 0.988 / 1.000 / 1.000 | 0.988 |
| 20 | mu_sweep | mu offset +0.0576 | 230.7 | 13553 | 0.992 / 1.000 / 1.000 | 0.992 |
| 20 | mu_sweep | baseline (mu 0.72/0.80, kappa 0.801, n = 542) | 277.6 | 16570 | 0.994 / 0.998 / 0.994 | 0.994 |
| 20 | kappa_sweep | kappa 0.4 | 186.0 | 10645 | 1.000 / 1.000 / 0.992 | 0.992 |
| 20 | kappa_sweep | kappa 0.5 | 214.4 | 12431 | 0.996 / 1.000 / 0.992 | 0.992 |
| 20 | kappa_sweep | kappa 0.6 | 238.9 | 13993 | 0.996 / 1.000 / 0.992 | 0.992 |
| 20 | kappa_sweep | kappa 0.7 | 259.9 | 15369 | 1.000 / 1.000 / 0.996 | 0.996 |
| 20 | kappa_sweep | baseline (mu 0.72/0.80, kappa 0.801, n = 542) | 277.6 | 16570 | 0.994 / 0.998 / 0.994 | 0.994 |

### RT5. Thresholds T10 and T20 (delta 0.03, t = 1.782)

| k | bracketed crossings of 0.90 (mean mixed per model) | not bracketed | T (largest bracketed crossing x 1.10, rounded up to 5) | verification run (480 replicates, separate seeds) |
|---|---|---|---|---|
| 10 | {'n_sweep': 143.1, 'mu_sweep': 167.7} | min power >= 0.90 at every kappa tested (mixed 152.7 to 233.4) | **185** | mixed 184.8, pairs 3082: D1 0.94, D2 0.983, D3 0.948, min 0.94 |
| 20 | {'mu_sweep': 110.7} | min power >= 0.90 at every n tested (mixed 76.6 to 277.6); min power >= 0.90 at every kappa tested (mixed 186.0 to 277.6) | **125** | mixed 125.3, pairs 7149: D1 0.946, D2 0.988, D3 0.954, min 0.946 |


### Reading the red-team results

1. **t = 1.782 versus 1.645 (RT1).** The change in power is small. At delta 0.03 the minimum over decisions moves from 0.981 to 0.979 (nominal, k = 10), 0.971 to 0.971 (conservative, k = 10), and 0.994 and 0.990 at k = 20 (unchanged to 0.004). At delta 0.02, k = 10, the minimum moves from 0.704 to 0.685 (nominal) and 0.673 to 0.662 (conservative), still far below 0.90, so the margin rule still selects delta = 0.03. With 1.782 the unwidened-to-widened cost at delta 0.03 is 0.015 (nominal) and 0.006 (conservative) at k = 10.
2. **Heterogeneous counts (RT2).** With one model at 60 mixed and the others at 207 to 259 (mean 209), the six-model decisions are D1 0.915, D2 0.963, D3 0.942 (nominal) and 0.917, 0.938, 0.946 (conservative) at t = 1.782: above 0.90 but 0.06 below the homogeneous cell (233 mixed, min 0.979), limited by D1. The low-count model enters the mean with the same weight as the others and contributes the largest bootstrap variance. A floor on the mean mixed count does not protect against this case; the pilot should report the per-model counts (and pairs) beside the mean.
3. **Residual-error correlation (RT3).** Lower rho_e is worse: at rho_e = 0.2, k = 10, the minimum is 0.931 (nominal) and 0.944 (conservative); at rho_e = 0.8 it is 0.994 for both. The bootstrap half-width h changes from 0.0115 (rho_e 0.2) to 0.0069 (rho_e 0.8) at k = 10, nominal, because the paired difference P minus S loses variance when their errors are positively correlated. At k = 20 the minimum is 0.992 (rho_e 0.2). The primary value 0.5 sits between; the power conclusion at delta 0.03 holds across the range.
4. **Pass rate and pass-fail pairs (RT4).** At the same mean mixed count, high-mu scenarios have fewer pass-fail pairs and lower power than the n sweep. At k = 10, 140 mixed problems give min power 0.858 by shifting mu (2321 pairs per model) and about 0.87 by the n sweep at 129 mixed (2173 pairs, 0.867 at 128.8); the crossing of 0.90 comes at 168 mixed in the mu sweep against 143 in the n sweep. At k = 20, the mu sweep falls from 0.95 at 120 mixed to 0.82 at 95 and 0.41 at 75 mixed (4251 pairs), whereas the n sweep is still 0.92 at 77 mixed (4581 pairs). Power tracks pairs more closely than mixed problems alone, and a low count caused by a high pass rate is the worse case. The kappa sweep (kappa 0.4 to 0.7, mixed 153 to 217 at k = 10; 186 to 260 at k = 20) never fell below 0.90, so it brackets no crossing; kappa at 0.4 is the lowest value tested, as instructed.
5. **Thresholds (RT5).** Take the larger bracketed crossing of the n sweep and the mu sweep, add 10 percent, round up to a multiple of 5: **T10 = 185 mixed problems per model (mean of six), T20 = 125**. Verification runs at these counts (separate seeds, 480 replicates) have minimum power 0.940 (k = 10; 184.8 mixed, 3082 pairs) and 0.946 (k = 20; 125.3 mixed, 7149 pairs). These supersede the R2-rule values of 140 and 90, which came from an n sweep at 1.645 only; the first pass of this run had also set T20 from a kappa-sweep point that was not a bracketed crossing, and that value (205) is superseded (`T_corrected` in the JSON; the original is kept under `T_first_pass_superseded_for_k20`). Against the assumed counts at n = 542 (233 for k = 10, 277 for k = 20) the floors leave factors of 1.3 and 2.2.

### Limits of the red-team run

- Scenario and sweep cells use nominal heterogeneity and 240 replicates; conservative heterogeneity was run only for the headline, heterogeneous-count, and rho_e cells (T10 and T20 are therefore nominal-based; the conservative n-sweep crossings under the R2 rule at z = 1.645 were 139 and 74, versus 131 and 88 nominal, so differences between settings were within 15).
- Crossings are linear interpolations on noisy points (non-monotone in places); the 10 percent margin and the verification runs are the safeguard, not a proof.
- The mu-shift scenarios shift all models together by the same offset; the heterogeneous-count run is the only unequal case, with one model.
- The refit-noise model, kappa, mu, and heterogeneity SDs are the assumptions listed earlier.
