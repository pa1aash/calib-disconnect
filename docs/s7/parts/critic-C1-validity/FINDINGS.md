# Critic C1 (validity) findings: PIPELINE_DESIGN_R2

Wave 7, step C1. Fresh-context red-team critic (opus) that read only `docs/s7/PIPELINE_DESIGN_R2.md`, `docs/s7/power/POWER_R2.md`, `docs/s7/power/power_sim_r2.py`, `docs/s7/power/power_sim_r2_rule2.py`, `docs/s7/BENCHMARK_PINS.md`, and `research/positioning/w7/DIFFERENTIAL_R2.md`. The critic declined to write this file under its own operating rules. The orchestrator saved the returned text here, lightly reformatted, with no change of substance. "Verified" means the critic confirmed the point against the cited text or script. "Suspicion" means the critic inferred it and did not check it against code or data.

**Count by grade:** BLOCKING 0, MAJOR 12, MINOR 2.

**V1. MAJOR (verified). The trained readout's recipe may leak test-fold labels.**
- **Location:** §7.4 says learning rate and step count are "chosen by the log loss on the first inner split's validation fold (one inner split, three adapters per outer fold)". §12.5 says "Recipe selected once per model". §7.3 says "the fold-seed 1 and 2 refits of $S^T$ fit only the final adapters".
- **Problem:**
  - If one recipe is chosen per model by pooling across the five outer folds, the validation folds behind that choice are test folds of other outer folds.
  - Under fold seeds 1 and 2 the partition changes. Any seed-0 recipe was chosen on labels of problems that are now in seed-1 or seed-2 test folds. The text does not say which seed-0 fold's recipe goes with which seed-1 or seed-2 fold.
  - Both break §7's own rule: "No test-fold information in fitting".
- **Why it matters:** two of the three seeds behind $\bar R$ use a hyperparameter tuned partly on their own test labels. That tilts $S^T$ upward and favors D1 or D3.
- **Fix:** state that the recipe is selected per (fold seed, outer fold), and run the three-adapter selection under seeds 1 and 2 too. The cheaper alternative is a single recipe fixed in advance for all seeds. Either way, record the mapping.

**V2. MAJOR (verified). How the step count moves to the final adapter is not fixed.**
- **Location:** §7.4: the step count is selected on adapters trained on three folds and evaluated every 20 steps. The final adapter trains on four folds with no validation set.
- **Problem:** the rule could keep the absolute step count, keep the epoch fraction, or scale by data size. Each gives a different $S^T$, and the choice can be made after seeing results.
- **Also:** K4's retry is "with 2 epochs", but training is already "up to 2 epochs", so the retry is undefined.
- **Fix:** freeze the transfer rule (for example, keep the selected epoch fraction) and give K4 a different retry setting.

**V3. MAJOR (verified). K4 leaves open what goes into $R$ if the trained readout fails.**
- **Location:** K4: "If the trained readout still fails, report it. The supervision term is then bounded by the isotonic readout, and the primary test is reported with that limitation."
- **Problem:** the text does not say whether a failed $S^T$ still enters $R_m$ and $\bar R$, or is replaced. It also does not say whether "majority of outer folds" is judged per model, or what happens if only some models fail. A failed $S^T$ hands D2 to the probe almost automatically.
- **Fix:** pre-specify all of this. If $S^T$ fails K4 for model $m$, $R_m$ still uses the failed $S^T$, is flagged, and stays in $\bar R$. A second statistic, $\bar R$ without the flagged models, is reported as a sensitivity. A D2 reached only through flagged models is stated as such.

**V4. MAJOR (verified). The budget's efficiency identity fails for the headline residual.**
- **Location:** §1.4 says "$G_0 + \sum_v \phi_v = R$". §9 says "The Shapley cells other than $R$ use fold seed 0", and $R_m$ is "the mean over the three seeds".
- **Problem:** the Shapley terms add up to $R$ at seed 0, but the decision statistic is the seed-averaged $\bar R$. Figure 1's $R$ column and Table 3's $\bar R$ are therefore different numbers.
- **Fix:** run the game at seed 0, label its $R$ as $R^{(0)}$, and show it next to $\bar R$ with $\bar R - R^{(0)}$. A better option, if affordable, is to refit $P$ for all cells and $S^T$ under the original suite under seeds 1 and 2, so the $t=1$ cells can be seed-averaged.

**V5. MAJOR (verified). The training toggle $t$ also switches the answer format (V1 to V2).**
- **Location:** §7.2: "V1 is the zero-shot readout in the primary chain". §7.4: $S^T$ uses "the V2 format".
- **Problem:** $\phi_t$ mixes the change from numeric to Yes/No format with the effect of training.
- **Fix:** split $\phi_t$ into (V1 to V2 zero-shot) plus (V2 zero-shot to V2 trained), or make the V2 chain primary for H3, keeping $G_0$ on V1.

**V6. MAJOR (verified on definitions; magnitude a suspicion). The isotonic toggle $r$ means different things at $t=0$ and $t=1$.**
- **Location:** §1.3 says $r$ is "expected near zero, and not interpreted". §7.3 fits the $S^T$ map on inner adapters' scores and applies it to the final adapter.
- **Verified:**
  - $r$ is an exact null player for $W$.
  - Every coalition is well defined.
  - In the labels-first order, $r$'s sequential term is exactly 0.
- **Problem:**
  - At $t=1$, $r$ is recalibration plus transfer across adapters. It can harmonize score scales across folds on pooled AUROC, so $r \times t$ need not be small.
  - The power simulation cannot test this.
  - On the Brier budget, the three-fold versus four-fold mismatch biases the map.
  - Secondary strata use in-sample maps, so $r$ means a third thing there.
- **Fix:** drop "expected near zero, and not interpreted". Report the $r\times t$ interaction index, and report the pooled AUROC of $S^T$ with and without the map at $t=1$. Report the in-sample-map sensitivity. State that order-dependence for $r$ is mechanical.

**V7. MAJOR (suspicion, mechanism verified). Precision limits can create ties in $S^T$ but not in the probe, biasing $R$ upward.**
- **Location:** §5 and §7.4: $S^T = P(\text{Yes})/(P(\text{Yes})+P(\text{No}))$ from a bf16 model.
- **Problem:** bf16 logits are coarse. A confident trained readout saturates, so a problem's samples tie, which pulls $W(S^T)$ toward 0.5. The float64 probe has no such problem.
- **Fix:** compute the Yes/No logits in float32, store log-odds, and report within-problem tie rates for every readout in $R$. Freeze the per-tokenizer Yes/No variant list.

**V8. MAJOR (verified). The adapter mask's unit test is too narrow, and the masked region is underspecified.**
- **Location:** the R1 test checks that the KV cache of the prompt and code is "bit-identical", in the pilot only, and the pilot model is T1 (Olmo only). §7.4 masks "V2 elicitation-turn tokens and the answer position". §5 defines $p_3$ as "the last token of the elicitation turn".
- **Gaps:**
  - The test covers one architecture.
  - Nothing checks that the mask is nonzero where it should be.
  - Padded or batched layouts are not tested.
  - The scoring engine is not fixed (vLLM LoRA serving has no position mask).
  - "Bit-identical" can fail spuriously across kernels.
  - The masked tokens are undefined: headers, the empty thinking block, and $p_3$.
- **Fix:** fix the token span by template and define $p_3$ as the last prefix token before the answer. Require the test per architecture class, in the padded batch layout, through the engine that computes $S^T$. The test must check (a) code-position states and KV against the base within a stated tolerance and (b) that elicitation positions differ when the adapter is nonzero.

**V9. MAJOR (verified). The probe and the trained readout are not matched in capacity, and the controls do not close the gap.**
- **Location:** §7.1, §7.4, §7.11.
- **Problem:**
  - Even rank 1 across every layer exceeds a linear probe's capacity.
  - Selection is not symmetric: the probe uses inner 4-fold CV, while $S^T$ uses one inner split. §7.4's sentence that both are selected "by inner cross-validation" is false.
  - The probe is chosen by pooled log loss, while the decision metric is $W$.
  - The rule "moves by more than $\delta$" does not say whether it uses point estimates or intervals.
- **Fix:**
  - Name $P_3$ as the rank-0 rung and report the ladder $P_3$, then LoRA plus linear head, then $S^T$ at ranks 1, 4, and 16.
  - Add a probe matched to the adapter's reach (attention pooling or an MLP over code-token states) as a sensitivity.
  - Correct the §7.4 sentence.
  - Make the capacity rule interval-based.

**V10. MAJOR (verified). The power audit's $k$ threshold rests on a scenario that does not match how the pilot will fall short.**
- **Location:** `power_sim_r2_rule2.py` sweeps $n$ at fixed $\mu$ and $\kappa$, while §13 compares the pilot's $\bar m$ with $T_{10}=140$.
- **Problem:**
  - At $n=542$, a low $\bar m$ comes from higher pass rates. High-$\mu$ mixed problems have fewer pass-fail pairs, so the threshold is in the wrong unit for that scenario.
  - $\bar m$ is a mean, so one model at about 60 can hide behind it.
  - There is no $\mu$, $\kappa$, or $\rho_e$ stress under the R2 rule.
  - $T_{10}$ sits 1.2 above the conservative crossing.
- **What matches:** on all other points the script implements the stated rule.
- **Fix:** keep the signed-off currency. Pre-specify a report that reruns the audit at each model's measured pass-count histogram, with per-model mixed and pair counts. Run a $\mu$ sweep at $n=542$ and a $\rho_e$ stress before freezing.

**V11. MAJOR (verified). The generation-shift contrast does not measure the confound it names.**
- **Location:** §1.5; DIFFERENTIAL_R2 row 13 codes the budget "T (generation-shift term)".
- **Problem:**
  - $\Delta\Gamma_g$ includes the probe's own shift.
  - The unpaired confound is never computed.
  - At $d=1$, the two values come from different mixed sets.
  - Which adapter generates the fresh set is unclear.
  - Which probe member and V2 turn are used is unclear.
- **Fix:**
  - Report the unpaired cross contrast and the probe's own shift.
  - Compute $d=1$ also on problems mixed in both sets.
  - Fix one fresh set per suite-specific adapter.
  - Read the probe with the same V2 turn.
  - Correct the row 13 code.

**V12. MAJOR (verified). The pilot model is the direct ancestor of a primary model, and the analysis code is not frozen before the pilot's results are seen.**
- **Location:** §13: T1 runs "all readouts … and the full analysis code".
- **Problem:** T1's cells are a close preview of P3's, so every unfixed choice can be settled with that preview in hand.
- **Fix:** hash the analysis code before the pilot's T1 outputs are opened, and log every later change in DEVIATIONS.md. Alternatively, keep T1's $\Gamma$ cells sealed until the full run is frozen.

**V13. MINOR. Other open analysis choices (garden of forking paths).**
- (a) How undefined replicates enter the percentile interval.
- (b) $z = 1.645$ is used with 12 df ($t_{12} = 1.782$), and equal variances are assumed.
- (c) K3 can mix formats across models.
- (d) K7 cut 6 changes how primary readouts are fit.
- (e) The sign convention for the Brier and calibration budgets.
- (f) The isotonic map is fit on scores that were already used to select the step count.

**V14. MINOR. Leakage edges.**
- (a) The cache key omits the input-set ID, the limits, and the interpreter.
- (b) TypedMutGen inputs can nearly duplicate plus-inputs.
- (c) MBPP near-duplicate tasks are not grouped into the same fold.
- (d) The LiveCodeBench label-analog wording conflicts with the 80 percent label split.
- (e) §12.1 says "three training folds" for LiveCodeBench adapters, but §7 says four.
