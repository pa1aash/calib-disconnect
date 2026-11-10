# Disposition of the Part B critiques of PIPELINE_DESIGN_R0 (wave 6)

Run date 2026-11-10. Three critics reviewed `PIPELINE_DESIGN_R0.md` in parallel:

| Critic | Model | Findings | Record |
|---|---|---|---|
| Methodologist (leakage, Shapley, within-problem estimator, supervision asymmetries) | opus | 24 (3 blockers, 12 major, 9 minor) | `parts/critic-B-method/FINDINGS.md` |
| TMLR reviewer (rubric and the two acceptance criteria) | opus | 21 (5 blockers, 8 major, 8 minor) | `parts/critic-B-tmlr/FINDINGS.md` |
| Budget and feasibility | sonnet | 14 (no blocker, 9 major, 5 minor) | `parts/critic-B-budget/FINDINGS.md` |

Each critic's own write was blocked by the harness; the orchestrator saved the returned text to the record files. The revision is `PIPELINE_DESIGN_R1.md`. R0 is kept unchanged.

**Totals.** 59 findings: 49 accepted, 10 modified, 0 rejected. Where two critics raised the same point, both IDs are listed in one row.

**Codes.** A = accepted as proposed; M = modified (the problem is accepted, the fix differs, reason given); R = rejected (reason given).

## Blockers

| Finding | Disposition | What R1 does | Where |
|---|---|---|---|
| Method F1 (isotonic ties bias $R$ upward) | A | Recalibrated scores are ranked by (isotonic value, pre-map score), so the map creates no ties; $r$ is a null player for $W$; tie rates and the no-tie-break variant are reported | 1.2, 1.3, 7.3 |
| Method F2, TMLR F3 (trained readout has more capacity than a linear probe) | M | Accepted problem. Fix: a probe family ($P_2$, $P_3$ at the pre-answer state, multi-layer $P_{\text{multi}}$) selected by inner cross-validation, so $R$ is against the strongest linear probe; a capacity ladder (ranks 1, 4, 16) and a LoRA-plus-linear-head control on two models; a capacity caveat in every outcome sentence. Not adopted: an attention-pooled probe, because it needs states at every code token, which the single forward pass does not store (the storage would grow about 300-fold) | 1.8, 7.1, 7.11, R13 |
| Method F3 (label toggle changes training population and volume) | A | Every readout of the 16-cell game is fit on the 542-problem population only; LiveCodeBench readouts are fit separately | 4, 7 |
| TMLR F1 (pooled $G_0$ against within-problem $R$; "accounted for" overclaims) | A | Added $R_{\text{pool}} = \Gamma(1,1,0,1)$ with the same three decisions (secondary); outcome sentences rewritten to say where the probe's advantage remains; [Campos] cited for pooled versus within-problem | 1.2, 1.6, 1.8 |
| TMLR F2 (reconciliation entries are not points of this budget) | A | Entries are called analogs; the reconciliation sentence is rewritten; a "shared budget cell" column is added | 1.8, 2.1 to 2.4, 15 |
| TMLR F4, Method F10 (no decision for the stated readout ahead) | A | Three mutually exclusive decisions D1 to D3, each with its own sentence | 1.6, 1.7, 1.8 |
| TMLR F5, Method F11 (power does not single out 0.03; anchors mixed) | A | The decidability argument is deleted; the power grid is extended to $\delta$ 0.01 and 0.015 at $M = 6$ (`power/SHARED_SHOCK.md`); $\delta = 0.03$ is kept on substantive grounds (field tie readings, published pooled gaps, the spread of published within-problem values), and the language-shift anchor is withdrawn | 1.6, 9 |

## Major

| Finding | Disposition | What R1 does | Where |
|---|---|---|---|
| Method F4 (stacking leak in isotonic on the trained readout) | A | Nested cross-fitting: the map is fit on inner-cross-fitted scores of adapters that did not see the samples | 1.2, 7.3 |
| Method F5 (K4 retry uses test-fold loss) | A | K4 uses inner-validation loss only; the probe gets a matching retry | 13 |
| Method F6, TMLR F8 (probe tuned, adapter fixed; early stopping inert) | M | Accepted problem. Fix: learning rate in three values and step count chosen by inner cross-validation, evaluated every 20 steps. Selected once per model on one suite and reused elsewhere, which keeps the cost at about 8.8M tokens per fold instead of a grid per suite and population. The epoch count stays at one (two only on a K4 retry) | 7.4, 12 |
| Method F7 (label toggle refits $P$ but only rescores zero-shot $S$) | M | Accepted as a diagnostic, not a game change: at the full configuration, $\phi_l$ is split into refitting on EvalPlus labels and scoring on them. A zero-shot readout has nothing to refit, so the asymmetry is inherent to $t = 0$ and is stated | 1.3 |
| Method F8 (exclusions break pairing) | A | The primary population is the problems valid under both suites | 4 |
| Method F9 ($\phi_d$ mixes three things) | A | Pooled AUROC on mixed problems only and fold-averaged pooled AUROC reported beside each pooled value | 1.3, 8 |
| Method F12 (fold seeds undefined; refit-variance rule unstated) | A | Folds hashed with a fold seed; seed 0 primary for all readouts; seeds 1 and 2 for non-LoRA readouts on every model and for LoRA readouts on two models; a fixed widening rule | 7, 9 |
| Method F13 (power simulation widths are lower bounds) | A | Stated, with a pilot-based rerun | 9 |
| Method F14 (pilot can reveal $R$; K2 can change the population) | A | Pilot on a checkpoint outside the primary set; K2 may change only $k$ | 3, 13 |
| Method F15, TMLR F17 (generation-shift term confounded; five-player game unclear) | A | $k_g = 10$; the probe is read on the fresh samples; the contrast is a gap difference $\Delta\Gamma_g$; pass rates and mixed counts reported; the five-player game is dropped. TMLR F17's thinking-on point: the thinking-on reconciliation already exists and is now named in 3 | 1.5, 3, 5, 7.5 |
| TMLR F6 (anchor units; Campos values) | A | Merged into the margin rewrite; Campos lines 565-566 verified by the orchestrator in the saved text | 1.6 |
| TMLR F7 (saturated populations; optimistic pass-rate model) | A | Stated as a planning limitation; the pilot measures the mixed count; K2 raises $k$; R2 rated high | 9, 13, 14 |
| TMLR F9 (missing citations) | A | A citation table for all adjacent works, including 2610.27455 and Miglani; citations placed in the toggle table, 1.5, and 7.4. 2610.25846 and 2605.09502 were checked against `research/positioning/w6/DECOMPOSITION_OCCUPANCY.md` | header, 1.2, 1.3, 1.5, 7.4 |
| TMLR F10, Method F18, F19 (weak reconciliation checks) | A | Three outcomes (reproduced, not reproduced, undetermined) with an equivalence-style level check; the Campos within-problem criterion that cannot fail is removed and replaced; Ribeiro tests only its two large gaps and records the Reflective-below-Random oddity; reading A is paired; the Campos May 2025 window is a listed deviation | 2 |
| TMLR F11, Method F16 (efficiency sign) | A | $G_0 + \sum_v \phi_v = R$ stated in prose and glossary | 1.4 |
| TMLR F12 (label toggle changes the mixed set) | A | $W$ on problems mixed under both suites reported beside $\phi_l$, with counts entering and leaving | 1.3, 8 |
| TMLR F13 (generality beyond six models, four Qwen) | M | Accepted problem. Fix: sentences name the set exactly, results are reported per family, and a third family is an operator item. No swap is made now, because B3 verified no non-gated, Apache-2.0 alternative family with base checkpoints at 7B to 32B | 1.8, 3, R14 |
| Budget F1 (hardware and prices not given) | M | The GPU model is an operator item on the sign-off block; prices are not given because none is in a fetched record; the implied TFLOP/s is stated | 3, 12, 17 |
| Budget F2 (thinking-on length unsourced) | A | Labeled unsourced; measured in the pilot; sensitivity of +7.0 h per +1,000 tokens | 12.1, 12.3, 13 |
| Budget F3 (LoRA scoring short; reading B missing) | A | Overhead raised to 20 percent; reading-B scoring added | 12.2 |
| Budget F4 (probe fits and bootstrap without CPU budget) | A | About 150 CPU-hours for fits and 10 for the bootstrap | 12.4 |
| Budget F6 (LiveCodeBench label-analog refits omitted) | A | LiveCodeBench adapters for both label sets are budgeted for the six primary models | 12.1, 12.2 |
| Budget F7 (K7 cuts too small, remove primary models; ID collision) | A | Six cuts totaling about 81.7 h, none touching the primary set, population, or reconciliation models; risks renamed R1 to R16 | 13, 14 |
| Budget F8 (pilot misses 67 percent of cost) | A | The pilot adds a 32B throughput probe and a thinking-on length probe | 12.2, 13 |
| Budget F10 (no reference check possible on LiveCodeBench) | A | Stated; anomalies listed; R16 | 6, 14 |

## Minor

| Finding | Disposition | What R1 does | Where |
|---|---|---|---|
| Method F17 (order names swapped relative to the script) | A | Orders renamed "labels first" and "readout first", with the script's names mapped | 1.4 |
| Method F20 (full-suite sensitivity labels on agreement inputs) | A | The agreement readout is not computed in that sensitivity | 4 |
| Method F21 (extraction failures; $p_2$ undefined) | M | $p_2$ is defined for them. They stay labeled incorrect in the primary analysis (a deployed system fails on them), and the exclusion sensitivity is already pre-registered | 5, 6 |
| Method F22 (isotonic and demeaned Brier) | A | Stated; $r$ is read on the pooled calibration budget | 1.3 |
| Method F23 (descriptive H3 with "confirmatory" intervals) | A | Called simultaneous intervals; H3 stays descriptive | 1.7, 9 |
| Method F24 (sentence names terms whose interval includes zero) | A | Template rule: only terms whose simultaneous interval excludes zero are named | 1.8 |
| TMLR F14 (licences) | A | MBPP CC-BY-4.0 from B4; LiveCodeBench contest terms recorded as a gap; only IDs redistributed | 4, 14.1 |
| TMLR F15 (figure plan) | A | Dots instead of a waterfall; generation shift is a table; strata split into two panels; routing split into two panels; 12-page main-body target | 16 |
| TMLR F16 (median imputation ties) | M | Kept by design: an unparsable answer carries no ranking information, and the cost is charged to the zero-shot readout. The tie share is reported, and the drop-missing sensitivity stays | 7.2 |
| TMLR F18 (causal reading; interactions in an appendix) | A | Attribution stated as an accounting identity; interaction indices in main-text Table 2; glossary bans "explains" | 1.4, 15, 16 |
| TMLR F19 (LLM footnote; release; supplement cap) | A | Release, anonymization, and disclosure plan | 14.1 |
| TMLR F20 (Part A files cite R1 while R0 was reviewed) | A | No change needed: R1 now exists, which is the file the Part A records name | none |
| TMLR F21 (M = 9 quoted for an M = 6 design; replicates; 0.71 vs 0.72) | A | $M = 6$ results from the shared-shock run (which includes rho 0); Monte Carlo error stated; 0.72 nominal and 0.714 realized | 9 |
| Budget F5 (V1 allowance) | A | Raised to 5.0 h with the reason | 12.2 |
| Budget F9 (cost-minimizing claim; contingency) | A | $k = 8$ saving computed (25.8 h) and placed as a K7 cut; contingency raised to 25 percent with its reason | 12.2, 12.3, 13 |
| Budget F11 (execution-cost inputs unsupported) | A | Labeled as planning assumptions, measured in the pilot; sample count recomputed | 12.4 |
| Budget F12 (generation-shift row double counts fresh samples) | M | The R0 thinking-off row generated per suite because each suite has its own adapter, which is not a double count; the row was recomputed anyway for $k_g = 10$ and the extra forward pass | 12.2 |
| Budget F13 (weights cache; float16) | A | About 544 GB of weights and a 1 TB disk requirement; hidden states stored as bfloat16 | 5, 12.4 |
| Budget F14 (early stopping inert) | A | Evaluated every 20 steps (merged with Method F6) | 7.4 |

## Net effect on the budget and the decisions

- **GPU-hours.** 132.4 (R0) to 176.6 before contingency; 158.9 to 220.8 with contingency (now 25 percent).
- **Decisions.** Two primary decisions in R0, three in R1, plus $R_{\text{pool}}$ as a secondary statistic.
- **Margin.** $\delta = 0.03$ unchanged, with a new justification.
- **Power.** $k = 10$ and $n = 542$ unchanged.
