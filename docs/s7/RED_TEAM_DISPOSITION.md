# Red-team dispositions (wave 7, C2)

Two independent critics in fresh context reviewed design R2 (`docs/s7/PIPELINE_DESIGN_R2.md`, commit `de09536`): a validity critic (`docs/s7/parts/critic-C1-validity/FINDINGS.md`, V1 to V14; 0 BLOCKING, 12 MAJOR, 2 MINOR) and a claims critic (`docs/s7/parts/critic-C1-claims/FINDINGS.md`, K1 to K23; 3 BLOCKING, 14 MAJOR, 6 MINOR). Each finding was resolved inside the operator sign-off of wave 7; none required changing a signed-off decision (margin rule, $k$ rule, $n$, primary set, both readings, LiveCodeBench release, GPU, claim scope, disclosure). The frozen design is `docs/s7/PIPELINE_DESIGN_FROZEN.md`; its section 0 lists the changes F1 to F22 with the findings each resolves.

Dispositions: **Accepted** (the critic's fix applied as proposed), **Modified** (resolved by a different fix, with the reason), or **Verified** (the orchestrator checked the critic's evidence against the source before acting).

## BLOCKING

| ID | Finding | Disposition | Where resolved |
|---|---|---|---|
| K1 | Outcome templates overreach (generic readout names, unrestricted "code", "matches", shared-information claim) | Accepted. Population prefix, defined readout names ("Yes/No readout", "zero-shot numeric readout", "probe"), "is equivalent within the 0.03 margin to", and the caveat that equal $W$ does not show shared information | FROZEN 1.8 rules 3, 4, 7 and the D1 sentence (F1) |
| K2 | $\phi_t$ mixes format change (V1 to V2) with training | Accepted. Pre-registered split into a format step and a training step at $(r,d,l)=(1,1,1)$ in both orders; the paper name is "readout change (format and training)" unless the training step alone qualifies; V1 imputation tie share reported beside $G_0$ | FROZEN 1.4, 1.8 (F2); also resolves V5 |
| K3 | The ".02 tie" credited to [2610.31820] is not in the paper | Verified and accepted. The saved full text has no tie statement; txt:1115 reads a .02 difference as a lead, and txt:118 concerns external versus self estimators. Rewritten as this design's reading of Table 3, removed as a margin anchor, and named "the Table 3 pattern" | FROZEN 1.6 reason 1, 2.4 check, K5 (F3) |

## MAJOR and MINOR, claims critic

| ID | Disposition | Where resolved |
|---|---|---|
| K4 | Accepted. Naming requires a simultaneous interval excluding zero and $\lvert\phi\rvert \ge \delta$; $r$ never named in the discrimination budget; intervals condition on fold-seed-0 fits | 1.8 rule 1; 1.3 |
| K5 | Accepted. Share defined as $\phi_v/(R-G_0)$ only when signs agree; sign-conditional wording; "sum with $G_0$ to"; unit change at $\phi_d$ marked; no causal verbs | 1.8 rule 6 |
| K6 | Accepted. Operational names in paper text; scale confounds (Gemma 4 architecture, Olmo 3 versus 3.1 version) stated | 1.4 "Names in paper text" |
| K7 | Accepted. Mirrored capacity and recipe caveats for D2 and D3, quoting $R$ at ranks 1, 4, 16 and the MLP probe | 1.8 D2, D3 |
| K8 | Modified. Per-model sentence reports counts within, above, and below the margin and the audited per-model power; heterogeneity sentence fires when $\hat{\tau} > \delta$. Per-model power under the R2 rule is computed in the pilot rerun of the audit at the measured pass-count histograms (13), not in this wave, because it depends on those histograms | 1.8 rule 5; 13 |
| K9 | Accepted. Levels are descriptive where deviations predict a shift; the Ribeiro level check is descriptive (planning half-width about 0.064 at 121 tasks near 0.85) | 2.1, 2.2 |
| K10 | Accepted. A named tie fails when its paired interval lies entirely outside the tie width; tie widths labeled as design choices; K5 aligned | 2.1, 2.3, 2.4, K5 |
| K11 | Accepted. gpt-oss prefilled final channel fixed now (reasoning on is a labeled sensitivity); one outcome per reading; no inference about the paper's protocol; one verb per paper with check counts | 2.1, 2.3, 2.4 |
| K12 | Accepted. Truncation- and extraction-excluded diagnostics; descriptive levels; the Campos clause no longer makes any primary term model-specific; "explains" struck | 2.1, 2.3, 2.4, K5 |
| K13 | Accepted. One named discrepancy per paper with its corresponding term, no predicted sign; LiveCodeBench cells written $(r,t,d)$; DIFFERENTIAL row 17 reworded to "beside the budget" | 2.1, 2.3, 2.4; `research/positioning/w7/DIFFERENTIAL_R2.md` |
| K14 | Verified and accepted. FitMBPP 28.1 percent (below Random 64.5) is in the Qwen row at `2512.07404v3.txt:1182-1211`; listed, the check restricted to FitHE, the positional reading flagged | 2.2 |
| K15 | Accepted. "Claims of novelty" list mapped to DIFFERENTIAL rows 13, 15, 16; rows 2, 3, 5, 8, 9 not claimed; DIFFERENTIAL budget column corrected for rows 3, 4, 13. The suspicion about A codes from keyword searches is recorded as an open caveat in the DIFFERENTIAL notes, not re-coded in this wave | 1.8; DIFFERENTIAL_R2 notes |
| K16 | Accepted. Title rules and a new title naming the measured object, population, and model set | title; 1.8 |
| K17 | Accepted. Inline power caveats; re-partitioning limit; driver 1 corrected to the R2 rule; planning half-widths for reconciliation checks; "inconclusive" is not evidence of a gap | 1.8; 2.1; 9 |
| K18 | Accepted. "The field already reads differences of this size as ties" removed; reason 2 marked as pooled units | 1.6 |
| K19 | Accepted. "Trained with the same execution labels and folds" | 1.8 |
| K20 | Accepted. "Stated confidence" reserved for the concept; "Yes/No readout" in outcome sentences | 1.8 rule 4 |
| K21 | Accepted. 2609.33290's comparison is described, not called a confound | 1.5 |
| K22 | Verified and accepted. `TMLR_RUBRIC.md:58` requires a first-page footnote and gives no wording | 14.1 |
| K23 | Accepted. Pivot framed on TMLR acceptance criteria; certifications not targeted; analogs not called reproductions | 13 K6 |

## Validity critic

| ID | Disposition | Where resolved |
|---|---|---|
| V1 | Accepted (the critic's first option). Recipe selected per (fold seed, outer fold) from that partition's own inner split; mapping recorded. Budget recomputed: seed refits now include selection adapters (refit row 15.7 to 51.1 GPU-hours at $k=10$) | 7.4; 12 (F10, F22) |
| V2 | Accepted. Step count transferred by epoch fraction with the cosine schedule set to that length; K4 retry is learning rate $10^{-3}$ and 4 epochs, outside the original grid | 7.4; 13 K4 |
| V3 | Accepted as proposed. Failed $S^T$ kept and flagged in $\bar{R}$; sensitivity without flagged models; decisions reached only through flagged models stated | 13 K4 |
| V4 | Accepted (the first option). Game at fold seed 0 labeled $R^{(0)}$; decision on $\bar{R}$; both shown with $\bar{R}-R^{(0)}$. The costlier option (seed-averaging all $t=1$ cells) is not adopted, to stay inside the budget | 1.4 (F8) |
| V5 | Accepted (split option). Same change as K2; V1 stays the primary zero-shot readout for $G_0$ | 1.4 |
| V6 | Accepted. "Expected near zero, and not interpreted" removed; $r \times t$ index and $S^T$ pooled AUROC with and without the map reported; order dependence called mechanical; in-sample-map sensitivity already in 7.3 | 1.3 |
| V7 | Accepted. Float32 Yes/No logits stored as log-odds; fixed per-tokenizer variant rule; within-problem tie rates for every readout in $R$ | 7.12 |
| V8 | Accepted. Span and $p_3$ defined by template; per-architecture test in the padded training layout and the scoring engine, with a $10^{-3}$ tolerance and a positive control; the R-Tuning-style full adapter as a negative control | 7.12; R1 |
| V9 | Accepted. Ladder starts at $P_3$; MLP probe sensitivity on all six primary models; the false "inner cross-validation for both" sentence corrected, with a single-split probe sensitivity; interval-based capacity rule | 7.4, 7.11 |
| V10 | Accepted. The currency stays the mean mixed count (sign-off). Before the freeze, a $\mu$ and $\kappa$ sweep at $n=542$, a heterogeneous-count scenario (one model near 60 mixed), and a $\rho_e$ stress were run (`docs/s7/power/POWER_R2.md`, "Red-team follow-up"). They raised the thresholds before any data: $T_{10}$ from 140 to 185 and $T_{20}$ from 90 to 125 (larger bracketed crossing plus 10 percent; verified at minimum power 0.940 and 0.946). One model at about 60 mixed gives minimum power 0.915 to 0.917; $\rho_e = 0.2$ gives 0.931 to 0.944. The pilot reports per-model mixed and pair counts and reruns the audit at the measured histograms | 9; 13 |
| V11 | Accepted. Unpaired cross contrast, the probe's own shift, and $d=1$ on problems mixed in both sets; one fresh set per suite-specific adapter; probe read with the same V2 turn; DIFFERENTIAL row 13 recoded as a conditional contrast | 1.5; DIFFERENTIAL_R2 |
| V12 | Accepted (both options). Analysis code hashed before any T1 output is opened; T1 $\Gamma$ cells sealed by hash until the full-run analysis code is frozen; later code changes logged in `docs/DEVIATIONS.md` | 13 |
| V13 | Accepted: (a) undefined replicates dropped and counted, with a reporting rule (9); (b) $t_{12}=1.782$ in the widening; minimum power at $\delta=0.03$ is 0.971 to 0.979 at $k=10$, and at $\delta=0.02$ 0.662 to 0.685, so the margin rule still gives 0.03 (9); (c) all-V2 sensitivity when K3 switches formats (K3); (d) the recipe-reuse cut removed from K7; (e) Brier and calibration sign convention (8); (f) selection-score reuse in the isotonic map stated, with a splits-2-to-4 sensitivity (7.3) | 7.3, 8, 9, 13 |
| V14 | Accepted: (a) cache key extended (6); (b) canonicalized deduplication and a near-duplicate report for agreement inputs (4); (c) near-duplicate problems grouped into one fold (4); (d) LiveCodeBench analog wording aligned with the 80 percent label split (4); (e) LiveCodeBench adapters train on four folds, budget corrected (12) | 4, 6, 12 |

## Strongest rejection argument

The claims critic's strongest TMLR rejection argument (that the central test compares two supervised classifiers and says little about stated confidence as the field uses the term) is answered within the sign-off by K1, K2, K3, and K13 together: the outcome sentences name the Yes/No readout and never generalize to stated confidence; $\phi_t$ is split so that format and training are separated; the 2610.31820 target is the Table 3 pattern, not a claimed tie; and each paper has one named discrepancy. The residual objection, modest significance, is one TMLR asks reviewers not to weigh. No BLOCKING finding remains open, so the design is frozen.
