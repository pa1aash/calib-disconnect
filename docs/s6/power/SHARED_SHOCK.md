# Shared-shock sensitivity of the primary decision (wave 6, orchestrator)

Script: `power_shared_shock.py` (imports the B9 `power_sim.py` unchanged). Output: `power_shared_shock.json`. Runtime under 20 s; 100 replicates and B = 400 per cell, so probabilities carry Monte Carlo error of up to about 0.05.

**Why.** In the B9 design each model draws its own per-problem gap shock, which treats models as independent and can make the model-pooled residual look more precise than it is (B9 POWER.md caveat). Here the shock is `sqrt(rho) * shared + sqrt(1 - rho) * own`, with the shared part common to all models on a problem. All other B9 assumptions are unchanged (k = 10, n = 542, delta = 0.03, 90 percent two-sided interval).

Rows at rho = 0 reproduce the B9 independent-shock design at M = 6 (B9 itself reported M = 9 and M = 1). Revision after the Part B critics (TMLR F5 and F21, methodologist F11): the run now covers rho = 0, adds the delta grid, and reports the third decision (stated readout ahead of the probe by more than delta). All values below are from `power_shared_shock.json`.

| rho | M | true R | mean 90% CI | P(equivalence) | P(superiority) | P(inconclusive) |
|---|---|---|---|---|---|---|
| 0.5 | 6 | 0.00 | [-0.0077, 0.0082] | 1.00 | 0.00 | 0.00 |
| 0.5 | 6 | 0.03 | [0.0225, 0.0385] | 0.02 | 0.05 | 0.93 |
| 0.5 | 6 | 0.06 | [0.0514, 0.0677] | 0.00 | 1.00 | 0.00 |
| 0.5 | 1 | 0.00 | [-0.0188, 0.0181] | 0.64 | 0.00 | 0.36 |
| 0.5 | 1 | 0.06 | [0.0410, 0.0790] | 0.00 | 0.86 | 0.14 |
| 1.0 | 6 | 0.00 | [-0.0087, 0.0079] | 1.00 | 0.00 | 0.00 |
| 1.0 | 6 | 0.03 | [0.0200, 0.0369] | 0.07 | 0.01 | 0.92 |
| 1.0 | 6 | 0.06 | [0.0515, 0.0682] | 0.00 | 1.00 | 0.00 |
| 1.0 | 1 | 0.00 | [-0.0196, 0.0176] | 0.57 | 0.00 | 0.43 |
| 1.0 | 1 | 0.06 | [0.0433, 0.0812] | 0.00 | 0.87 | 0.13 |

(M = 1 rows at R = 0.03 and all rho = 0 rows are in the JSON.)

**Delta grid, M = 6, true R = 0, P(equivalence):**

| rho | delta 0.01 | 0.015 | 0.02 | 0.03 | 0.05 |
|---|---|---|---|---|---|
| 0.0 | 0.44 | 0.92 | 1.00 | 1.00 | 1.00 |
| 0.5 | 0.29 | 0.83 | 0.97 | 1.00 | 1.00 |
| 1.0 | 0.32 | 0.80 | 0.96 | 1.00 | 1.00 |

**Delta grid, M = 6, true R = 0.06, P(probe superiority):** 1.00 at delta 0.01 to 0.03 for every rho; 0.57 to 0.65 at delta 0.05.

**Third decision.** P(stated readout ahead by more than delta) is 0.00 in every cell, as expected with true R >= 0.

**Consequence for the margin.** Under these assumptions the design can decide equivalence at delta 0.02 (P at least 0.96) and reaches about 0.8 at 0.015. Decidability therefore does not single out 0.03. The margin must be justified on substantive grounds (design R1 section 1.6).

**Reading.** Sharing the gap shock across models barely widens the pooled interval at M = 6 (half-width about 0.008, the same as at rho = 0). The reason is that the problem-clustered bootstrap resamples the same problems for every model, so problem-level variance, shared or not, is already inside the interval. The decision at R = 0 and R = 0.06 is unchanged at M = 6.

**What this does not cover.** The interval is conditional on the six named models: the estimand is the mean over this fixed set, not over a population of models. Between-model heterogeneity of the true residual is therefore reported per model (with Holm control) and is not a sampling component of the primary interval. This is a scope statement for the paper, not a power issue. The B9 planning assumptions (gap and shock sizes) remain unvalidated until the pilot.
