# Cross-locus comparisons

Step 6 of the wave 4 run (vault tag code-llm-confidence-positioning-d82d00). Inputs are the committed positions of the six step 5 interim notes.

## Tension 1: decompose the gap, or first test whether a controlled gap exists

- **Locus L2-residual** ([[interim-report-l2-residual-post-training-reasoning-format-on-code]]) commits: the residual after Ribeiro is NARROW as a factorial decomposition (tuning stage by readout, reasoning toggle by readout) of where the probe-verbal gap opens on code, about 65% confidence.
- **Locus probe-confound** ([[interim-report-probe-advantage-real-or-difficulty-confound-on-code]]) commits: the uncontrolled "probe beats own readout" claim is OCCUPIED, and the controlled gap (supervision-matched readouts, input-only baselines, within-problem scoring) is probably at most about 0.05 within-problem AUROC, about 65% confidence.
- **The cross-locus dynamic:** this is a dependency, not a factual conflict. Locus L2-residual's decomposition presumes a gap worth locating; locus probe-confound's evidence (Campos 0.620 vs 0.629 and Miglani 0.677 vs 0.703 within problem) predicts that the controlled gap may be near zero, in which case the decomposition would partition noise. Both investigators rate their position at medium confidence and both name the same deciding experiment: a same-sample, within-problem comparison on code with a trained own-readout.
- **How the draft should engage this:** the L2 spine must be ordered as "controlled test first, decomposition conditional on a measurable controlled gap"; the draft must say explicitly that a null controlled result is itself the finding and is publishable under TMLR's evidence criterion.

## Tension 2: two independent routes to the same decisive control (pivot A14)

- **Locus L2-residual** commits: the residual cannot carry a paper without a trained-verbal arm and an isotonic-verbal control, because Probe-SD (AUROC .825 to .928 vs probe .948) and RLCR show training closes most of the gap in NLP, and no code study reports AUROC after training stated confidence (CLEAN (provisional)).
- **Locus probe-confound** commits: Ribeiro's probe is fitted while its verbal readout is zero-shot, and Liu et al. show the winner flips on 2 of 3 datasets when supervision is matched.
- **The cross-locus dynamic:** convergence from different mechanisms. One locus reaches the trained-readout control from the post-training literature (pivot A14), the other from the supervision asymmetry in the occupant's design. Both name it as unrun on code, and both list it under "what would change my mind."
- **How the draft should engage this:** the recommendation should make a supervision-matched own-readout arm (trained verbal head or logit-feature head on the same execution labels) a required component, and should flag pivot criterion 3 as open, not triggered.

## Tension 3: the label and difficulty controls that L1 needs are the same controls L2 and L3 need

- **Locus L1-estimator** ([[interim-report-l1-estimator-and-label-oracle-sensitivity-with-contamination-cont]]) commits: the L1 comparison is OCCUPIED (union); the defensible L1 contribution is a three-control sensitivity protocol (estimator set, base versus augmented-test oracle, per-model release split), about 60% confidence.
- **Locus probe-confound** commits: pooled AUROC is about 99% between-problem at function-level scale; report within and between separately.
- **Locus L3-routing** ([[interim-report-l3-confidence-routed-execution-and-update-after-failure]]) commits: a gate beats random only when within-pool rank correlation clears about 0.3 to 0.55 and mean pass rate exceeds about 0.1 (Give-Up), so the replay must stratify by pass rate.
- **The cross-locus dynamic:** convergence. Three loci independently require the same measurement hygiene: label-oracle swaps (L1), within-problem scoring (L2), and pass-rate stratification (L3) all control for what the label and the problem, not the readout, contribute. Label flips under augmented tests would also move L2 and L3 numbers, so L1's protocol is the foundation the other claims stand on, not a separate contribution.
- **How the draft should engage this:** present L1's protocol as the measurement layer of one paper whose findings are L2's controlled test and L3's replay, rather than as a standalone benchmark contribution (which is OCCUPIED (union)).

## Tension 4: F is OCCUPIED, yet its quantities are what L1 and L2 must report

- **Locus F-metrology** ([[interim-report-f-metrology-residual-quantity]]) commits: F is OCCUPIED as a framing; every proposed quantity maps onto Yates, Murphy, grouping loss, or meta-I, about 75% confidence.
- **Locus L1-estimator** and **locus L2-residual** both prescribe reporting calibration and discrimination separately (Brier skill with reliability, AUROC, recalibration controls).
- **The cross-locus dynamic:** complication. F fails as a contribution but survives as a reporting discipline: the "readout bias" and "resolution against an internal reference" that F would name are exactly the Murphy and Yates terms L1 and L2 already need. The measurement-instrument framing is therefore "used" (psychometric and measurement-validity vocabulary is occupied, 2610.25846, 2603.14893) and not "contested" in fetched work.
- **How the draft should engage this:** state that the framing is used, adopt its vocabulary as exposition only, and do not claim novelty for it.

## Tension 5: whether downstream utility (L3) and localization (L4) can stand without a strong signal

- **Locus L3-routing** commits: routing by elicited verbal or probe confidence is NARROW and an honest negative is publishable; update-after-failing-test is CLEAN (provisional), 45 to 55% confidence.
- **Locus L4-localization** ([[interim-report-l4-localization-occupancy-and-targeted-repair]]) commits: line-level localization is OCCUPIED (Gros and Devanbu); per-test-group and targeted repair are NARROW; keep v4_dprc out of the paper, about 70% confidence.
- **Locus probe-confound** predicts within-problem AUROC around 0.6 to 0.7 for the best readouts on code.
- **The cross-locus dynamic:** special case. L3's routing gain is bounded by the readout quality locus probe-confound estimates; in the hard stratum (pass rate below 0.1) Give-Up predicts that every gate fails. L4 adds a new label unit and an unrun pipeline without adding a calibration claim.
- **How the draft should engage this:** rank L3 as a secondary analysis on the same generations (offline replay with random and label-sorted oracle arms) and the update-after-failure test as a small, hedged probe; rank L4 last and recommend that v4_dprc stay out of the strongest version.

## Calibration notes

| Locus | Investigator confidence | Shared "would change my mind" condition |
|---|---|---|
| L2-residual | medium (about 65%) | a code study training stated confidence on execution labels and reporting AUROC |
| probe-confound | medium (about 65%) on gap size; high (about 85%) that the controlled test is unrun | same as above, plus a within-problem probe margin above 0.05 with a CI excluding zero |
| L3-routing | medium (55 to 65%) routing; medium-low (45 to 55%) update | a code paper routing by elicited confidence with random and oracle arms |
| L1-estimator | medium (about 60%) | a code paper ranking families under original versus EvalPlus tests |
| F-metrology | medium-high (about 75%) | a readout-error quantity not a function of probe score, verbal score, and outcome |
| L4-localization | medium (about 70%) | a work scoring per-test confidence against failing-test identity |

The trained-own-readout experiment on code is named by two loci and is the main open question; every CLEAN (provisional) verdict in these notes shares the same instrument gaps (arXiv full-text search failed, OpenAlex budget exhausted, Semantic Scholar keyword search and arXiv export rate-limited).

## Step 8 updates (corpus-critic gap fill)

- **Tension 2 strengthened toward the A14 threat.** CREDO (arXiv 2609.34857, Table 1, concurrent) trains stated confidence on code with execution labels: in-domain AUROC 0.850 against 0.690 for the untrained Qwen3-8B base and 0.815 for RLCR. It has no probe arm. Trained stated confidence on code is now NARROW, not CLEAN (provisional); the residual is the same-sample probe comparison. The draft must treat a trained own-readout arm as required, and must say the gap may close.
- **Tension 1 adjusted.** No citer of 2512.07404, 2608.08266, or 2606.14530 runs a supervision-matched control (adversarial screen returned no overturning source). Campos et al. Table V shows the about-0.05 within-problem margin holds for Qwen3-Coder under language shift but not for gpt-oss in distribution (trained methods 0.69 to 0.78 within problem), so the predicted small controlled gap is model-dependent; confidence in "at most about 0.05" drops to medium-low.
- **Adversarial searches with no overturning source** (cc-2, cc-3): L3 routing by elicited confidence (stays NARROW), update after a failing test (stays CLEAN (provisional), with Resist-and-Update citers unscreened after HTTP 429), release-date contamination effect on calibration, and label independence and test insufficiency. These positions gain confidence, within the stated instrument gaps.
