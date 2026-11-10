# Pipeline design R0 (draft, pre-registration candidate): a systematics budget for the calibration disconnect in code language models

Status: DRAFT R0, wave 6, 2026-11-10. It is not frozen and not hashed. No pipeline code, run, or manuscript text exists. Every number in this file is a design parameter, a published value quoted from a saved full text (with location), or a planning assumption labeled as such. None is a result.

Inputs: the operator decisions of wave 6; `research/positioning/w6/` (Part A); `docs/s2/METHOD_INVENTORY.md`; `docs/s2/venue/TMLR_RUBRIC.md`; `paper/STYLE.md`; and the Part B fact records in `docs/s6/parts/models-B3/`, `docs/s6/parts/bench-B4/`, and `docs/s6/parts/power-B9/`.

**Citation rule for this file.** The rule covers every sentence that overlaps prior or concurrent work:

| Work | Short form |
|---|---|
| Ribeiro et al., arXiv 2512.07404, ICSE 2026 | [Ribeiro] |
| Campos, Klassert, and Ulges, arXiv 2611.07876 | [Campos] |
| Wu and Ji, arXiv 2610.31820 | [2610.31820] |

The same rule applies to the Part A adjacent works: MARGIN 2605.22949, Kim and Kang 2605.27752, 2609.04582, RADAR 2610.22139, 2609.33290, and CREDO 2609.34857.

The measurement-instrument and error-budget language is exposition only and is never claimed as novel.

## 1. Estimands and hypotheses

### 1.1 Objects

- **Models.** $m \in \mathcal{M}$ (section 3).
- **Problems.** $i \in \mathcal{I}$, with benchmark populations defined in section 4.
- **Frozen generations.** For each model and problem, $k$ samples $c_{mij}$, $j = 1..k$. They are generated once (section 5), hashed, and never regenerated. Every readout except the generation-shift arm is computed on these same strings.
- **Labels.** $y^{O}_{mij}$ under the original test suite and $y^{E}_{mij}$ under the EvalPlus suite (section 6).
- **Readouts.** Each readout maps a sample to a score in [0, 1] (section 7):
  - $P$: the hidden-state probe;
  - $S$: the stated-confidence readout, whose form depends on the supervision level.

### 1.2 The gap function and the raw gap $G_0$

A scoring configuration is a vector $x = (r, t, d, l) \in \{0, 1\}^4$ of four toggles, each switched from its uncontrolled level (0) to its controlled level (1):

| Toggle | Term | 0 (uncontrolled) | 1 (controlled) |
|---|---|---|---|
| $r$ | supervision, recalibration | stated readout used as elicited | stated readout passed through an isotonic map fit on training folds |
| $t$ | supervision, training | zero-shot stated readout | trained stated readout (LoRA adapter active only in the elicitation turn, fit on the same labels and folds as the probe) |
| $d$ | difficulty | pooled scoring | within-problem scoring |
| $l$ | label validity | original test suite (labels for fitting and scoring) | EvalPlus suite (all supervised readouts refit) |

When $t = 1$ and $r = 1$, the isotonic map is fit on top of the trained readout's out-of-fold scores.

**Gap function.** For a metric $\mathrm{M}$, the gap at configuration $x$ is

$$\Gamma_{\mathrm{M}}(x) = \mathrm{M}_d\big(P^{(l)}, y^{(l)}\big) - \mathrm{M}_d\big(S^{(r,t,l)}, y^{(l)}\big),$$

on the frozen generations, where $\mathrm{M}_d$ is the pooled version of the metric when $d = 0$ and the within-problem version when $d = 1$ (section 8).

**Primary metric.** Discrimination: pooled AUROC at $d = 0$ and pair-weighted within-problem AUROC $W$ at $d = 1$. The same budget is reported for Brier score and the calibration estimators as secondary metrics. For these, $d = 1$ means the problem-demeaned version defined in section 8.

**Raw gap.** $G_0 = \Gamma(0, 0, 0, 0)$: probe against zero-shot numeric verbal confidence, pooled AUROC, original tests, frozen generations. This is the configuration in which "probes beat stated confidence on code" has been reported:

- pooled probe against zero-shot verbalized confidence in [2610.31820] Table 3;
- probe against reflective token readouts in [Ribeiro], scored within task as selection accuracy;
- probe against P(Yes) in [Campos], pooled and within problem.

Each paper's exact configuration is reproduced separately as a reconciliation entry (section 2).

**Residual gap.** $R = \Gamma(1, 1, 1, 1)$: probe against the trained, isotonic-recalibrated stated readout, within-problem AUROC, EvalPlus labels, identical frozen generations.

### 1.3 Toggles, strata, and sensitivity analyses

| Term | Role | Definition |
|---|---|---|
| Recalibration ($r$) | toggle | isotonic map (section 7.3) |
| Training ($t$) | toggle | trained stated readout (section 7.4) |
| Difficulty ($d$) | toggle | pooled vs within-problem scoring |
| Difficulty baselines | reported beside $d$ (not a toggle) | prompt-only probe and code-text-only classifier (sections 7.9, 7.10), fit on the same folds. They report how much of the pooled AUROC of $P$ and $S$ is reachable without the sample, which is the difficulty component of pooled scoring |
| Label validity ($l$) | toggle | original vs EvalPlus suites, with refitting |
| Generation shift ($g$) | conditional term, outside the primary attribution | $\Delta_g$ (section 1.5) |
| Contamination | stratum | problem release date relative to the model's stated cutoff (section 4) |
| Model family and scale | strata | section 3 |
| Base vs instruct, reasoning on/off | strata and secondary arms | section 10 |
| Calibration estimator | sensitivity analysis | section 8 |
| Zero-shot elicitation format | sensitivity analysis | the budget is recomputed with the second verbal format (P(Yes), section 7.2) as the zero-shot readout |
| Probe token position | sensitivity analysis | mean-pooled code tokens instead of the last code token |

**Why the isotonic toggle is in the budget although it cannot change AUROC.** A monotone map preserves ranking, so in the primary metric $r$ moves AUROC only through ties created by the isotonic step function and through fold-to-fold differences in the fitted map. Its Shapley value on AUROC is therefore expected near zero, and the design reports it rather than dropping it.

On the Brier and calibration budgets, $r$ is the term that separates a recalibration-removable gap from a residual. That is the split made by RADAR 2610.22139 for risk and by 2609.04582 for a probe-versus-answer gap. The budget applies it to the probe-versus-stated gap and does not claim it as a new decomposition.

### 1.4 Attribution

**Primary: Shapley values.** Over the four toggles $N = \{r, t, d, l\}$:

$$\phi_v = \sum_{S \subseteq N \setminus \{v\}} \frac{|S|!\,(|N| - |S| - 1)!}{|N|!}\,\big[\Gamma(S \cup \{v\}) - \Gamma(S)\big],$$

where $\Gamma(S)$ is the gap with the toggles in $S$ at level 1 and the rest at level 0.

- **Efficiency.** $\sum_v \phi_v = R - G_0$, so the budget reads: raw gap, minus the four terms, equals the residual.
- **Cells.** All 16 cells of $\Gamma$ are computed on the same frozen generations and the same bootstrap resamples. Every cell is a well-defined scoring configuration, so the game is defined at every coalition. None of the four toggles changes the generations.
- **Non-commutation.** The toggles do not commute in effect. For example, $l$ changes which samples are positive, and that changes what $d$ removes. Shapley values split each interaction equally among its members. The design therefore also reports the pairwise interaction indices (Shapley interaction index, order 2) for the six pairs.

**Secondary: sequential decompositions.** Two canonical orders are reported:

- forward $(l, d, t, r)$: fix the labels, then the scoring, then the readout;
- reverse $(r, t, d, l)$.

The forward order follows the logic of measurement: a gap is first measured against valid labels and at the right granularity, and the readout is changed last. The spread between the two orders, beside the Shapley value, shows how order-dependent each term is.

### 1.5 Generation-shift term

The generation-shift term is defined for one trained readout, the [2610.31820]-style categorical readout. Its fine-tuning adapter is active in the generation turn as well as in the readout. Two scores are computed for it (section 7.5):

- $S^{g=1}$: scored on its own fresh generations, with fresh execution labels (reading A of `research/positioning/w6/R2610_31820_PROTOCOL.md`);
- $S^{g=0}$: teacher-forced on the frozen generations (reading B).

$$\Delta_g = \mathrm{M}_d\big(S^{g=0}\big) - \mathrm{M}_d\big(S^{g=1}\big),$$

computed at $r = 0$, $t = 1$, for $d \in \{0, 1\}$ and $l \in \{0, 1\}$. $\Delta_g$ is the part of an apparent probe-versus-trained-readout difference that comes from scoring the two readouts on different generations.

**Why it is outside the primary attribution.**

- The residual is defined on identical generations.
- $g$ is undefined when $t = 0$ (a zero-shot readout does not change the generator).

**Secondary five-player game.** A five-player Shapley attribution with $g$ as a null player when $t = 0$ is reported as a secondary analysis. Its interpretation caveat is stated with it: the $t \times g$ interaction is split equally between the two terms.

**Comparison of readout formats.** The [2610.31820]-style categorical readout at $g = 0$ is also compared with this design's trained readout at $t = 1$, both on frozen generations. The difference is reported as a readout-format contrast in the reconciliation table.

### 1.6 Primary test and the margin $\delta$

**Primary statistic.** $\bar{R} = |\mathcal{M}_{\mathrm{primary}}|^{-1} \sum_m R_m$, the mean residual over the primary model set (section 3), on the label-validity population (HumanEval and MBPP problems with EvalPlus suites, section 4). Both tests below are computed from one problem-clustered paired bootstrap (section 9).

**Test 1, equivalence (TOST).** $H_0: |\bar{R}| \ge \delta$ against $H_1: |\bar{R}| < \delta$. Rejected at $\alpha = 0.05$ when the 90 percent percentile interval lies inside $(-\delta, \delta)$.

**Test 2, minimum-effect superiority.** $H_0: \bar{R} \le \delta$ against $H_1: \bar{R} > \delta$. Rejected at $\alpha = 0.05$ when the one-sided 95 percent lower bound exceeds $\delta$. The conventional superiority bound ($\bar{R} > 0$) is reported beside it and labeled secondary.

**Exclusivity.** The two primary decisions cannot both be reached. If neither is reached, the result is reported as inconclusive, with the interval.

**The margin: $\delta = 0.03$ in pair-weighted within-problem AUROC.** Justification:

1. **It is wider than the published ties.** [2610.31820] treats differences up to .02 pooled AUROC between its trained readout and its probe as a tie (Table 3). Miglani et al. (2609.36783, Table 1) report within-problem differences of .004 and .026 on code without significance claims (`research/positioning/w6/CLOSED_ITEMS.md`). A margin of .03 is above all of these, so a residual the field already reads as a tie counts as equivalence.
2. **It is the smallest margin the design can decide.** Under the planning assumptions of section 9 (pending B9), .03 is the smallest margin at which the pooled test reaches 80 percent power for both decisions with the available problem count. A smaller margin would make the null outcome undecidable, which removes the point of an equivalence design.
3. **It sits between the published within-problem ties and the published pooled advantages.**
   - **Pooled advantages.** The probe-over-zero-shot-verbalized gaps on code in [2610.31820] Table 3 are .20 to .31 (Qwen3-8B .88 - .60 and .84 - .61; Nemotron .89 - .58 and .80 - .60).
   - **Within-problem ties.** [Campos] reports a code-token probe at .627 against P(Yes) confidence at .629 under language shift (Sec VI-C c, Table V).
   - **Consequence.** A margin of .03 classifies the published within-problem comparisons as ties and the published pooled gaps as far outside it.

**Sensitivity.** The decisions are also reported at $\delta \in \{0.02, 0.05\}$. The margin is fixed at sign-off and not changed after the pilot. The pilot may only change $k$ and the problem count (section 13).

### 1.7 Hypotheses

- **H1 (primary).** Equivalence: $|\bar{R}| < \delta$.
- **H2 (primary, mutually exclusive with H1).** Minimum-effect superiority: $\bar{R} > \delta$.
- **H3 (secondary, descriptive).** The sign and interval of each Shapley term on the primary metric. The design states no directional hypothesis for any term. The pilot is not used to choose signs.
- **H4 (secondary).** The budget is computed separately in each stratum (contamination, family, scale, base vs instruct, reasoning on/off), with the stratum-by-term table and multiplicity control (section 9).

### 1.8 Contribution statement for each outcome

The paper keeps exactly one of these, with the numbers filled from generated macros.

- **Equivalence (H1).** "On frozen, execution-labeled code from [N] open models, the published advantage of hidden-state probes over stated confidence (raw gap [G0] pooled AUROC) is accounted for by supervision, difficulty, and label validity: after a trained stated readout, within-problem scoring, and EvalPlus relabeling, the residual lies within 0.03 within-problem AUROC of zero, and a budget attributes the raw gap to each term with problem-clustered intervals."
- **Superiority (H2).** "On frozen, execution-labeled code from [N] open models, a residual of more than 0.03 within-problem AUROC separates hidden-state probes from stated confidence after a trained stated readout, within-problem scoring, and EvalPlus relabeling, so the probe holds correctness information that supervised stated confidence does not express on identical generations; a budget attributes the rest of the raw gap to each term."
- **Inconclusive.** "On frozen, execution-labeled code from [N] open models, supervision, difficulty, and label validity account for [share] of the raw probe-over-stated gap, and the residual lies in [lo, hi] within-problem AUROC, which neither establishes nor excludes a gap of 0.03."

Each sentence is followed in the paper by the reconciliation sentence: "The configurations of [Ribeiro], [Campos], and [2610.31820] are points of this budget, and each reproduces [or: fails to reproduce] on the same generations (Table [R])."

## 2. Reconciliation targets

### 2.1 Common reporting

For each target, the reconciliation table has one row per published comparison. Each row gives:

- the published value, quoted from the saved full text with its location;
- the value reproduced on this design's frozen generations, with its 95 percent problem-clustered interval;
- the deviations from the published protocol;
- the cell of the budget lattice that the configuration occupies.

**What counts as a reproduction:** both of these hold.

1. **Qualitative.** The published ordering of the readouts holds, with a paired interval that excludes zero, or the published tie holds, with an interval inside the published tie width.
2. **Quantitative.** The published point value lies inside the reproduced 95 percent interval widened by a pre-stated tolerance of 0.05 in the published unit. The tolerance absorbs unavoidable deviations (sections 2.2 to 2.4).

**How a failure is reported.**

- A failed reproduction is a result. It is reported in the same table with the same prominence, never omitted or moved to an appendix alone.
- Each failure gets a short deviation analysis: which deviation is the likeliest cause, tested where the design allows. Examples: the language subset for [Campos], or the PPO checkpoint for [2610.31820].
- Section 13 states what a failure changes.

### 2.2 [Ribeiro] RQ2: self-ranking on HumanEval

- **Published configuration** (`research/positioning/w5/parts/dossier-A5/raw/2512.07404v3.txt`; Sec 5.1.1 to 5.1.3; Table 5):

| Element | Published value |
|---|---|
| Model | Qwen2.5-Coder-7B-Instruct (also Mistral-7B-Instruct-v0.3, CodeLlama-7B-Instruct, OpenCoder-8B-Instruct) |
| Tasks | 121 HumanEval test tasks (TestHE), same split as RQ1 |
| Samples | 10 per task at temperature 1.0 |
| Readouts | LAT direction fit on FitHE, layer chosen on ValHE; Intrinsic (length-normalized likelihood); Reflective Regular and T/F (token probability of a verbal answer); Random |
| Metric | pass@rank-1, the share of tasks whose top-ranked sample passes the tests, within task |

- **Published values for Qwen** (Table 5, pass@rank-1):

| Readout | pass@rank-1 |
|---|---|
| Random | 64.5% |
| Intrinsic | 80.2% |
| Reflective Regular | 24.8% |
| Reflective T/F | 26.4% |
| LAT FitHE | 85.1% |
| LAT FitSyn | 85.1% |
| RankEF | 81.0% |

- **Reproduced here.**
  - Model, readouts, and metric: Qwen2.5-Coder-7B-Instruct with the LAT direction, the length-normalized likelihood, and the two reflective formats, scored by pass@rank-1 on this design's frozen HumanEval generations.
  - Fitting data: fit on problems outside TestHE, with this design's labels.
  - Additional points: the same frozen generations are also scored with this design's probe ($P$) and trained readout. Ribeiro's configuration thereby becomes a point at $d = 1$ (within-task use), $t = 0$, $l = 0$, with a different metric.
- **Deviations to record:**
  - The task split is rebuilt from the paper's description, because the list of 121 tasks is not in the saved text. The deviation is listed if it cannot be matched.
  - The fit set uses this design's folds.
  - RankEF is not reproduced, because it needs a separate trained ranker. Its published value is shown as published.
  - Labels follow this design's harness (section 6).
- **Success criterion.** Two parts:
  - the ordering LAT > Intrinsic > Random > Reflective holds with paired intervals;
  - the LAT and Intrinsic values fall within the tolerance of 85.1 and 80.2.

### 2.3 [Campos]: probe, prompt-only probe, and judging pass on LiveCodeBench

- **Published configuration** (`research/positioning/w4/parts/fetcher-l2/raw/2611.07876.txt`; Sec V-A to V-C; Table V):

| Element | Published value |
|---|---|
| Models | Qwen3-Coder-30B-A3B-Instruct and gpt-oss-20b |
| Problems | 454 LiveCodeBench release_v6 problems released October 2024 to May 2025, in Python, C++, and Java |
| Samples | 10 candidates at temperature 1 |
| Splits | by problem, 60/20/20, three partitions |
| Probe | logistic regression on one layer, 512 candidates per class |
| Readouts | last code token; last prompt token (prompt-only); the probe on the judging pass; P(Yes) confidence |
| Metrics | pooled and within-problem AUROC |
| Inference | paired problem-clustered bootstrap with 2,000 resamples |

- **Published values** (Table V, program target, in distribution, mean over three languages; pooled / within):

| Readout | Qwen3-Coder-30B | gpt-oss-20b |
|---|---|---|
| Judging pass | .886 / .553 | .851 / .772 |
| Generation, last code token | .895 / .620 | .864 / .781 |
| Generation, last prompt token | .891 / .514 | .720 / .524 |

- **Reproduced here.**
  - Models and population: both models on this design's LiveCodeBench Python problems from the same release window.
  - Readouts: this design's probe at the last code token, the prompt-only probe at the last prompt token, a probe on the judging pass (the elicitation turn of format V2), and P(Yes).
  - Scoring: pooled and within problem.
  - Splits: Campos's three 60/20/20 partitions are reconstructed by problem with a fixed seed, in addition to this design's five folds.
- **Deviations to record:**
  - Python only. The published values average three languages, and Python-only values are not separately printed in Table V. The quantitative criterion is therefore applied to the pattern, not to the level.
  - gpt-oss is run with the final channel prefilled, as Campos does (Sec V-A a), only if the reproduction needs it. Otherwise it runs with reasoning on, as a stratum.
- **Success criterion.** Three parts:
  - pooled AUROC of the prompt-only probe within 0.03 of the code-token probe for Qwen3-Coder;
  - within-problem AUROC of the prompt-only probe inside [0.45, 0.55];
  - the gpt-oss prompt-only pooled AUROC below its code-token probe, with a paired interval that excludes zero.

### 2.4 [2610.31820]: trained categorical readout against a same-label probe

- **Published configuration** (`research/positioning/w6/R2610_31820_PROTOCOL.md`):

| Element | Published value |
|---|---|
| Models | Qwen3-8B and Nemotron-Cascade-8B, each PPO-trained by the authors (checkpoints not released), thinking on |
| Code splits | in distribution: held-out TACO, CodeContests, and Codeforces problems; out of distribution: LiveCodeBench, Easy to Hard, no window stated |
| Samples | four per prompt at temperature 1.0, top-p 1.0, 16,384 response tokens |
| Grading | rule-based, truncation counted as incorrect |
| R-Tuning | the policy fine-tuned to append "I am sure" or "I am unsure", scored by confidence-token probability |
| Probe | linear, on the last-token activations, "with the same labeled data" |
| Metrics | pooled AUROC, 15-bin ECE, Brier; no intervals |

- **Published values** (Table 3, code AUROC, in distribution / LiveCodeBench):

| Readout | Qwen3-8B | Nemotron-Cascade-8B |
|---|---|---|
| Verbalized | .60 / .61 | .58 / .60 |
| R-Tuning | .86 / .85 | .89 / .79 |
| Probe | .88 / .84 | .89 / .80 |

- **Reproduced here.**
  - Model and decoding: public Qwen/Qwen3-8B with thinking on, temperature 1.0, top-p 1.0, and the response cap of the reasoning stratum (section 5).
  - Population: this design's LiveCodeBench problems (the out-of-distribution analog) and HumanEval and MBPP.
  - R-Tuning-style readout: trained per section 7.5 and scored under reading A (its own fresh generations, $g = 1$) and reading B (frozen generations, $g = 0$).
  - Probe and metrics: the same-label probe on frozen generations, with pooled AUROC, 15-bin equal-width ECE, and Brier.
- **Deviations to record:**
  - The public checkpoint is used instead of the PPO checkpoints.
  - TACO, CodeContests, and Codeforces are not used.
  - The probe layer is chosen by this design's nested procedure (unstated in the paper).
  - R-Tuning hyperparameters are this design's (unstated for Sec 4 of the paper).
  - Labels come from execution.
  - Nemotron-Cascade-8B is reproduced only if section 3 admits it.
- **Success criterion.** Three parts:
  - pooled AUROC of the R-Tuning-style readout under reading A within 0.02 of the probe, as the paper's tie;
  - zero-shot verbalized below both, with paired intervals that exclude zero;
  - levels within the tolerance of the published LiveCodeBench values.

  The comparison is reported under both readings. Whichever reading reproduces the published tie is evidence about the paper's unstated protocol, and the design reports it as such and not as a fact about the paper.

## 3. Models

All facts come from `docs/s6/parts/models-B3/MODELS.md` (repository API JSON and model cards saved in its `raw/`, retrieved 2026-11-10). Every model is non-gated and Apache-2.0, so hidden states are available through forward hooks. Revisions are the `main` SHA at retrieval and are pinned. Sizes are bf16 weights at 2 bytes per parameter.

### 3.1 Families and requirements

**Qwen2.5-Coder 7B and 32B, base and instruct:**

- the code-specialist family;
- 7B-Instruct is the [Ribeiro] model.

**Qwen3 8B and 14B, base and post-trained:**

- the general family;
- Qwen3-8B with thinking on is the [2610.31820] model;
- the thinking mode switches on identical weights through `enable_thinking`.

**Olmo 3, 7B and 32B base:**

- the fully open family;
- the stated cutoff is "Dec. 2024";
- SFT, DPO, and final checkpoints are released.

**Two [Campos] models, used for reconciliation only:**

- Qwen3-Coder-30B-A3B-Instruct;
- gpt-oss-20b.

**Requirement check:**

| Requirement | Met by |
|---|---|
| Three open families at two scales | Qwen2.5-Coder, Qwen3, Olmo 3 |
| Base and instruct pairs | all three families |
| One same-weights reasoning toggle | Qwen3-8B; Qwen3-14B is available as a second scale |
| Released intermediate checkpoints | Olmo 3 7B |
| Hidden-state access | all models (open weights) |
| Fits one 96 GB GPU at bf16 | largest is Qwen2.5-Coder-32B at 65.5 GB |

### 3.2 Matrix

| Role | Repository ID | Revision (main) | Params | bf16 GB | Licence | Stated cutoff (quoted source) or upper bound |
|---|---|---|---|---|---|---|
| Primary, instruct | Qwen/Qwen2.5-Coder-7B-Instruct | c03e6d358207e414f1eca0bb1891e29f1db0e242 | 7.62B | 15.2 | Apache-2.0 | code data from GitHub repositories "created before February 2024" (arXiv 2409.12186 Sec 3.1.1); full corpus not stated; repository created 2024-09-17 (upper bound) |
| Primary, instruct | Qwen/Qwen2.5-Coder-32B-Instruct | 381fc969f78efac66bc87ff7ddeadb7e73c218a7 | 32.76B | 65.5 | Apache-2.0 | as above; repository created 2024-11-06 (upper bound) |
| Primary, instruct (thinking off) | Qwen/Qwen3-8B | b968826d9c46dd6066d109eabc6255188de91218 | 8.19B | 16.4 | Apache-2.0 | not stated (card, arXiv 2505.09388); repository created 2025-04-27 (upper bound) |
| Primary, instruct (thinking off) | Qwen/Qwen3-14B | 40c069824f4251a91eefaf281ebe4c544efd3e18 | 14.77B | 29.5 | Apache-2.0 | not stated; created 2025-04-27 (upper bound) |
| Primary, instruct | allenai/Olmo-3-7B-Instruct | 6e5971d9eba42665f5bd5a0fcf047f299ce1dccc | 7.30B | 14.6 | Apache-2.0 | "Date cutoff: Dec. 2024." (card; arXiv 2512.13961 Sec 3.4.1) |
| Primary, instruct | allenai/Olmo-3.1-32B-Instruct | ac0587e4a7744a551c059d8cd17ba220bc940dae | 32.23B | 64.5 | Apache-2.0 | as above |
| Base stratum | Qwen/Qwen2.5-Coder-7B | 0396a76181e127dfc13e5c5ec48a8cee09938b02 | 7.62B | 15.2 | Apache-2.0 | as for 7B-Instruct; created 2024-09-16 |
| Base stratum | Qwen/Qwen2.5-Coder-32B | 2e12b5f7bc878d424d222e224ed40aee564ec45f | 32.76B | 65.5 | Apache-2.0 | created 2024-11-08 |
| Base stratum | Qwen/Qwen3-8B-Base | 49e3418fbbbca6ecbdf9608b4d22e5a407081db4 | 8.19B | 16.4 | Apache-2.0 | not stated; created 2025-04-28 |
| Base stratum | Qwen/Qwen3-14B-Base | 0b0bd3732e2c374d483664439ea334928b65f304 | 14.77B | 29.5 | Apache-2.0 | not stated; created 2025-04-28 |
| Base stratum | allenai/Olmo-3-1025-7B | a81bae42db3975be1671e27b9c9a56da1a9f980f | 7.30B | 14.6 | Apache-2.0 | Dec. 2024 |
| Base stratum | allenai/Olmo-3-1125-32B | c2b61dae89a1ad10e4ad5653d0e46b590902607b | 32.23B | 64.5 | Apache-2.0 | Dec. 2024 |
| Reasoning toggle (same weights as Qwen/Qwen3-8B) | Qwen/Qwen3-8B, thinking on | b968826d9c46dd6066d109eabc6255188de91218 | 8.19B | 16.4 | Apache-2.0 | as for Qwen3-8B |
| Post-training trajectory | allenai/Olmo-3-7B-Instruct-SFT | e1452fc572d51966ff4aaeb25118b891eb93e549 | 7.30B | 14.6 | Apache-2.0 | Dec. 2024 |
| Post-training trajectory | allenai/Olmo-3-7B-Instruct-DPO | b33130b7de49f0c2553b5c2b3bc8409ff3e627d1 | 7.30B | 14.6 | Apache-2.0 | Dec. 2024 |
| Reconciliation ([Campos]) | Qwen/Qwen3-Coder-30B-A3B-Instruct | b2cff646eb4bb1d68355c01b18ae02e7cf42d120 | 30.53B total, 3.3B active | 61.1 | Apache-2.0 | not stated; created 2025-07-31 (upper bound); non-thinking only |
| Reconciliation ([Campos]) | openai/gpt-oss-20b | 6cee5e81ee83917806bbde320786a8fb61efebee | 21B (card) | 42.0 | Apache-2.0 | "knowledge cutoff of June 2024" (arXiv 2508.10925 Sec 2.4); reasoning effort low/medium/high, no off switch stated |

**Primary model set.** $\mathcal{M}_{\mathrm{primary}}$ is the six instruct models: two per family, at two scales. The primary statistic $\bar{R}$ averages over these six.

**Strata and arms.**

- The base stratum pairs each primary model with its base.
- The reasoning toggle is Qwen3-8B with thinking on, against the same weights with thinking off. The card's mode-specific sampling recommendations are recorded but not used, because all frozen generations use temperature 1.0 and top-p 1.0 (section 5).
- The post-training trajectory is Olmo-3-1025-7B, then -Instruct-SFT, -Instruct-DPO, and -Instruct.

**Generation-shift model.** Qwen/Qwen3-8B is the generation-shift model:

- with thinking off for the budget's $\Delta_g$;
- with thinking on, on LiveCodeBench, for the [2610.31820] reconciliation.

**Precision.**

- Every model runs at bf16. No model needs FP8.
- gpt-oss-20b ships MXFP4 MoE weights. It is run in its native format, recorded as a deviation from bf16.

**Alternates if a model must be swapped (risk K6):**

- the OLMo 2 7B and 13B chains (Dec 2023 cutoff);
- deepseek-coder-6.7b base and instruct (code cutoff Feb 2023).

Llama-3.1-8B and gemma-3-12b are gated, and their cards could not be read.

**Cutoff gaps.** Qwen cutoffs are not stated in any card or technical report. Repository creation dates are used as upper bounds on the cutoff, labeled as such. A problem released after the upper bound is post-cutoff for certain. A problem released before it is classified "pre or unknown".

## 4. Benchmarks

All facts come from `docs/s6/parts/bench-B4/BENCHMARKS.md` (sources saved in its `raw/`, retrieved 2026-11-10).

| Benchmark | Version pinned | Problems | Release | Suites | Role |
|---|---|---|---|---|---|
| HumanEval | `openai/openai_humaneval` | 164 | 2021-07-07 (arXiv v1) | original tests (EvalPlus base inputs) | label-validity population |
| HumanEval+ | EvalPlus v0.1.10 (2024-05-01; HF tag v0.1.10, sha d32357c) | 164 | 2024-05-01 | base plus plus inputs (paper: about 764 tests per task on average) | EvalPlus suite for HumanEval |
| MBPP+ | EvalPlus v0.2.0 (2024-04-17; HF tag 9a36f31) | 378 (399 in v0.1.0; 21 removed for wrong original tests) | MBPP 2021-08-16 (arXiv v1); MBPP+ built from MBPP-sanitized | original MBPP tests (base inputs) and base plus plus inputs | label-validity population |
| LiveCodeBench code_generation_lite | release_v6 (= release_latest; 2025-04-21) | 1,055 (contest dates May 2023 to Apr 2025) | per-problem `contest_date` | public and private tests (official evaluator) | contamination stratum; [Campos] and [2610.31820] reconciliation |

**Licence.** MIT for HumanEval and Apache-2.0 for EvalPlus. The LiveCodeBench licence is inconsistent ("cc" in the card, MIT in the loader); it is recorded as a gap and checked before release.

**Populations.**

- **Label-validity population (primary).** HumanEval+ and MBPP+ together, 542 problems. Every problem has both suites, so all 16 cells of $\Gamma$ are defined. The primary test (section 1.6) is stated on this population.
- **LiveCodeBench population.** 1,055 problems, one suite family. On it, the budget has three toggles ($r$, $t$, $d$). The label toggle is replaced by a label-validity analog: public example tests against the full official suite. It is reported separately and labeled as an analog.

**Contamination windows.** For each model, the LiveCodeBench problems are classified by `contest_date` against the model's stated cutoff or its upper bound:

| Model group | Bound | Post-cutoff window |
|---|---|---|
| Olmo 3 | stated Dec 2024 | January to April 2025 |
| Qwen2.5-Coder 7B | creation 2024-09-16 | after mid-September 2024 |
| Qwen2.5-Coder 32B | creation 2024-11-08 | after early November 2024 |
| gpt-oss-20b | stated June 2024 | July 2024 onward |
| Qwen3 | upper bound late April 2025 | none; every v6 problem predates the bound |
| Qwen3-Coder | upper bound 2025-07-31 | none |

- For Qwen3 and Qwen3-Coder the stratum is not estimable on release_v6. This is an operator item: either accept the gap or add a newer problem source (no LiveCodeBench release after v6 exists as of 2026-11-10).
- HumanEval and MBPP have no per-problem dates and predate every model, so the label-validity population is pre-cutoff for all models (risk K7).
- The per-model counts of post-cutoff problems are computed from the pinned dataset before the pilot. They are not estimated here.

**Held-out agreement inputs, disjoint from the label suites.**

- **HumanEval and MBPP.** New inputs are generated per problem with EvalPlus's type-aware mutation generator (`TypedMutGen`), seeded by the base inputs, with a fixed seed. The LLM-based generator is not used, so no API model is needed.
  - Inputs are filtered by the problem's contract.
  - Any input equal to a base or plus input is deduplicated away.
  - Each problem is capped at 50 inputs.
  - The full EvalPlus suite stays intact as the label suite.
- **LiveCodeBench.** A fixed SHA-256 hash of each private test's input string selects 20 percent of the private tests as agreement inputs.
  - Labels use the public tests plus the remaining 80 percent. The deviation from the official suite is recorded.
  - A sensitivity analysis labels on the full official suite.
  - Agreement never uses the public tests, because they appear in the prompt.

**Gaps carried from B4:**

- the 21 MBPP+ task IDs removed in v0.2.0;
- whether the June 2024 EvalPlus ground-truth fixes (tasks 459, 102, 559) are in the v0.2.0 asset;
- the contents of HumanEval+ v0.1.10;
- whether every LiveCodeBench problem has private tests;
- the day-level date bounds of each LiveCodeBench release;
- the 426 versus 427 count of MBPP-sanitized.

All are resolved from the pinned files before the pilot. None changes the design.

## 5. Generation

- **Decoding.**
  - Temperature 1.0 and top-p 1.0 for all frozen generations. This matches all three reconciliation targets: [Ribeiro] Sec 5.1.1, [Campos] Sec V-A c, and [2610.31820] App C. It also gives the sample diversity that within-problem scoring needs.
  - No top-k and no repetition penalty.
  - Stop at end of turn.
- **Samples per problem.** $k$ is set by section 9 (planning value 10). The [2610.31820]-style generation-shift arm draws $k_g = 4$ fresh samples per problem, the paper's own count.
- **Maximum new tokens.**
  - 1,024 for non-reasoning generation.
  - 16,384 for the reasoning stratum, matching [2610.31820] App C.
  - Truncated outputs are labeled incorrect, as in [2610.31820], and counted separately (section 6).
- **Prompts.** All prompts are frozen text files, each with a SHA-256 hash recorded in the run manifest. The chat template of each model is pinned by repository revision and hashed as rendered.
  - **Generation prompt, one per benchmark family.** Function-completion benchmarks (HumanEval, MBPP) get the signature and docstring, with an instruction to return one fenced Python block. LiveCodeBench gets the problem statement and the starter code or I/O specification. The two prompts differ only in the problem payload.
  - **Elicitation format V1 (numeric).** A second user turn after the frozen assistant code:

    > Rate the probability, from 0 to 100, that the code above passes all hidden tests. Answer with one line: Confidence: N

    The answer is decoded greedily, up to 8 tokens.
  - **Elicitation format V2 (categorical).** A second user turn:

    > Does the code above pass all hidden tests? Answer Yes or No.

    The readout is $P(\text{Yes}) / (P(\text{Yes}) + P(\text{No}))$ at the first answer position, summing the case and leading-space variants of each token. This is the readout class of [Campos] (P(Yes)) and of the [Ribeiro] reflective T/F format.
  - **Reasoning models.** In the reasoning-on stratum, both elicitation turns run with thinking off, so that the readout position is fixed. A thinking-on elicitation is a sensitivity analysis on the reasoning toggle model only.
- **Seeds.** Each sample's sampler seed is the first 8 bytes of SHA-256 over (model ID, revision, benchmark, problem ID, sample index), so any single sample can be regenerated. vLLM's per-request seed is used, and the engine version is pinned.
- **Single forward pass per sample.** After generation, one teacher-forced pass over [generation prompt, frozen code, V2 elicitation turn] records three things:
  - the log-probability of every code token (section 7.6);
  - hidden states at the candidate layers, at three positions:
    - $p_1$, the last prompt token before the code (prompt-only probe);
    - $p_2$, the last code token (probe);
    - $p_3$, the last token of the elicitation turn (pre-answer state; judging-pass probe for [Campos]);
  - the V2 Yes/No logits at $p_3$.
  - **Candidate layers:** depth fractions {0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0} of the decoder stack, rounded down, plus the mean-pooled code-token state at the same layers, for the probe-position sensitivity analysis.
  - **What V1 adds:** one short greedy decode from the same prefix with the V1 turn. The prefix KV cache is reused.
  - **Storage:** float16 hidden states, sharded per model.
- **Extra generation pass for the generation-shift term.** Part A could not resolve which generations [2610.31820] scored (`research/positioning/w6/R2610_31820_PROTOCOL.md`). So the extra pass runs:
  - on the generation-shift model (section 3);
  - with the R-Tuning-style adapter active in generation;
  - drawing $k_g = 4$ fresh samples per test-fold problem, per fold, per label suite;
  - executing each fresh sample under both suites;
  - scoring each by its own confidence-token probability (reading A).

  Reading B uses the frozen generations and needs no extra generation. If the operator rules that only one reading is needed, the extra pass is dropped and $\Delta_g$ is not estimated.

## 6. Labels

- **Pass protocol.**
  - A sample passes a suite if every test in the suite passes within its time limit, the process exits normally, and no test raises.
  - HumanEval and MBPP use the EvalPlus evaluator at a pinned version. The original suite is the base inputs; the EvalPlus suite is the base plus the plus inputs.
  - The evaluator's per-test time limit rule (a factor times the reference solution's runtime, with a floor) is recorded at the pinned version.
  - LiveCodeBench uses its official evaluator at a pinned commit, with its time limits.
- **Sandbox.** Each execution runs in a fresh, unprivileged container with:
  - no network;
  - a read-only filesystem except a tmpfs work directory;
  - CPU-time and memory limits (2 GB);
  - a process-count limit;
  - an interpreter pinned by path, never taken from PATH (METHOD_INVENTORY 5.1).

  Wall-clock timeout per test is the evaluator's rule. A whole-program cap of 60 s catches hangs.
- **Reference-solution check.**
  - The canonical solution of every problem is executed under every suite before any sample is labeled.
  - A problem whose reference fails a suite is excluded from analyses that use that suite and listed with the reason. It is not silently repaired.
  - The share of excluded problems is reported per suite.
- **Extraction failures.** Recorded separately from execution failures, with codes:
  - no fenced block, and the fallback extraction (first `def` or `class` line) also fails;
  - syntax error;
  - missing entry point;
  - empty output;
  - truncation at the token cap.

  An extraction failure is labeled incorrect in the primary analysis, because a deployed system would fail on it. A sensitivity analysis excludes these samples. Rates are reported per model, benchmark, and suite.
- **Both suites.** Every sample has $y^O$ and $y^E$ where both suites exist. The flip table (pass to fail, fail to pass) is reported per model. Fail-to-pass flips can only come from flaky tests or changed time limits; each is investigated and listed.
- **Execution cache.**
  - **Key:** SHA-256 of (normalized code, suite ID, evaluator version, problem ID). The normalized code is the `ast.unparse` of the parsed module, or the raw text if parsing fails.
  - **Value:** pass, failure code, per-test outcomes, runtime.
  - **Reuse:** identical programs across samples and models reuse results.
  - **Flakiness check:** a 1 percent random audit re-executes cached entries, and any mismatch is logged.

## 7. Readouts and baselines

**Common protocol for every supervised readout.**

- **Folds.** Five problem-grouped folds, assigned by SHA-256 of the problem ID modulo 5, so the same problems fall in the same fold for every model. Every supervised readout is fit on four folds and scored on the fifth (cross-fitting). The out-of-fold scores form the analysis set.
- **Label suites.** Every supervised readout is refit under each label suite.
- **No test-fold information in fitting.** Layer choice, regularization strength, isotonic maps, imputation values, and early stopping use only training-fold problems. The validation needed for selection is an inner problem-grouped split of the four training folds.
- **Fold-seed repeats.** Three fold seeds for all readouts except the LoRA readouts (section 9 explains the refit-variance sub-study).

### 7.1 Hidden-state probe ($P$)

- **Model.** $P(c) = \sigma(w^\top \tilde{h}_\ell(c) + b)$, an L2-regularized logistic regression on the standardized hidden state $\tilde{h}_\ell$ at position $p_2$ and layer $\ell$. Standardization uses training-fold means and variances.
- **Nested selection.** Layer $\ell$ (seven candidates) and $C \in \{10^{-3}, 10^{-2}, 10^{-1}, 1, 10\}$ are chosen inside each outer training set by inner 4-fold problem-grouped cross-validation, minimizing log loss. This removes the layer-selection optimism found in Miglani et al. (2609.36783, which selects on the same out-of-fold scores) and follows the nested procedure of 2609.04582.
- **Class balance.** None. The readout is a probability on the natural base rate.

### 7.2 Zero-shot verbal confidence (two formats)

- **V1.** The integer $N$ parsed by the regular expression `Confidence:\s*(\d{1,3})`, clipped to [0, 100], divided by 100.
  - An unparsed answer is missing. It is never set to a default value (METHOD_INVENTORY 6.8 records the legacy default of 0.6).
  - In the primary analysis, missing values are imputed with the training-fold median of parsed values for that model, and flagged.
  - A sensitivity analysis drops them.
  - The parse rate is reported.
- **V2.** $P(\text{Yes}) / (P(\text{Yes}) + P(\text{No}))$, read from the logits at $p_3$ as in section 5. It is never missing.
- **Role.** V1 is the zero-shot readout in the primary chain. V2 is the zero-shot readout in the sensitivity chain and the reconciliation readout for [Campos] and [Ribeiro].

### 7.3 Isotonic-recalibrated verbal confidence

- **Fit.** For a stated readout $S$, an isotonic regression of $y$ on $S$ is fit on training-fold samples and applied out of fold.
- **Tie-break.** None.
- **Boundaries.** `out_of_bounds = clip`. A single-class training set falls back to the training base rate (METHOD_INVENTORY 6.5).

### 7.4 Trained stated-confidence readout ($t = 1$)

- **Adapter.**
  - LoRA with rank 16, alpha 32, dropout 0.05, no bias, on all attention and MLP projections.
  - It is active only on tokens of the elicitation turn: the LoRA output is multiplied by a 0/1 position mask that is 1 on the V2 elicitation-turn tokens and the answer position.
  - The generation prompt and the frozen code are therefore encoded by the base weights, and their KV cache is identical to the base model's.
- **Readout.** $S^T(c) = P_{\theta + \Delta}(\text{Yes}) / (P_{\theta+\Delta}(\text{Yes}) + P_{\theta+\Delta}(\text{No}))$ at the answer position, the V2 format.
- **Loss.** Binary cross-entropy between $S^T$ and the label (a proper scoring rule, as for the probe).
- **Training.**
  - Data: every training-fold sample, unweighted.
  - Optimizer: 1 epoch, AdamW, learning rate $10^{-4}$, cosine schedule, 5 percent warmup.
  - Effective batch: 64 sequences.
  - Early stopping on the inner validation split (log loss), checked every 200 steps.
- **Runs.** One adapter per (model, fold, label suite).
- **Supervision match.** The probe and the trained readout see the same samples, labels, folds, and loss. They differ in what is trained (a linear map on one frozen state, against a low-rank update of the network in the elicitation turn) and in where the answer is read.

### 7.5 The [2610.31820]-style trained readout

- **Adapter.** Same LoRA settings as 7.4, but active on all positions, as in R-Tuning, which fine-tunes the policy ([2610.31820] Sec 4.1).
- **Training.** Supervised fine-tuning on training-fold frozen samples. Each training sequence is the generation prompt, the frozen code, and the suffix "I am sure" if the sample passes the active suite or "I am unsure" if it fails. The loss is next-token cross-entropy on the assistant tokens: the code and the suffix.
- **Readout.** $P(\text{sure}) / (P(\text{sure}) + P(\text{unsure}))$ at the token after "I am".
- **Scoring.**
  - Reading A ($g = 1$): generate $k_g = 4$ fresh samples per test-fold problem with the adapter active, execute them, and score each from its own suffix position.
  - Reading B ($g = 0$): teacher-force the frozen test-fold samples followed by "I am", and score the same position.
- **Accuracy check.** The adapter's pass rate on fresh samples is reported against the base model's. [2610.31820] reports that R-Tuning lowers accuracy on 15 of 16 settings (Sec 4.2).

### 7.6 Token-likelihood variants

From the single forward pass, over the code tokens only (excluding the fence and end-of-turn tokens):

- the geometric-mean token probability, $\exp\big(\tfrac{1}{L}\sum \log p\big)$ (METHOD_INVENTORY 6.3 fixes this name and formula);
- the minimum token log-probability, $\min \log p$, transformed by $\exp$;
- the total log-probability $\sum \log p$ (length-confounded, reported as a baseline of length);
- the [Ribeiro] "Intrinsic" length-normalized likelihood, which is the geometric mean, used for the reconciliation.

All are unsupervised. Isotonic versions are reported for calibration only.

### 7.7 Sampling agreement on disjoint tests

**Definitions.**

- **Input set.** For problem $i$, let $X_i$ be the held-out agreement inputs (section 4), disjoint from every input of the label suites.
- **Behavior signature.** Each sample is executed on $X_i$ in the same sandbox. Its signature is the tuple of (output value or exception type, per input), with outputs compared by canonical `repr` after normalization of floats to 9 significant digits.
- **Readout.** $A(c_{ij}) = \frac{1}{k-1}\sum_{j' \neq j} \mathbb{1}[\text{sig}(c_{ij}) = \text{sig}(c_{ij'})]$.
- **Problem-level variant.** The largest-cluster share.

**Properties.**

- Agreement needs no expected outputs, so it uses no label information.
- Because $X_i$ is disjoint from the label inputs, a sample's agreement is not computed from the tests that define its label.
- It is unsupervised.

### 7.8 Semantic (AST) clustering

- **Normalization.** Each sample is parsed, identifiers are alpha-renamed by first occurrence (functions, arguments, locals), docstrings and comments are removed, and the result is dumped with `ast.dump`. Unparseable samples form singleton clusters.
- **Readout.** The size of the sample's cluster divided by $k$. The legacy formula $\max(0, 1 - (K-1)/9)$ is retired (METHOD_INVENTORY 6.6).

### 7.9 Prompt-only probe

- **Model.** The same model class and nested selection as $P$, on the hidden state at $p_1$ (the last prompt token, before any code).
- **Scores.** Constant within a problem, so its within-problem AUROC is 0.5 by construction. Its pooled AUROC measures how much of a readout's pooled discrimination is problem difficulty. This is the baseline [Campos] reports in Table V.

### 7.10 Code-text-only classifier

- **Required version.**
  - Features: character 3- to 5-gram TF-IDF (sublinear term frequency, minimum document frequency 3, fit on training folds) of the extracted code.
  - Model: L2 logistic regression, with $C$ chosen by inner grouped cross-validation.
- **Optional second version.** A frozen embedding from a code encoder that is not among the studied models (repository to be verified before sign-off), with logistic regression.
- **Purpose.** It reads only the code string, with no model internals. It measures how much correctness is visible in the surface text, the role of the text-only estimators in [2610.31820] Sec 2, Table 1.

## 8. Metrics

**Discrimination.**

- **Pooled AUROC.** Over all samples of the population (Mann-Whitney, ties counted as one half).
- **Pooled AUPRC.** For the positive class "pass", with the base rate printed beside it. The "fail" class AUPRC is also reported, because routing targets failures.
- **Pair-weighted within-problem AUROC.**

  $$W = \frac{\sum_i \sum_{a \in \mathcal{P}_i} \sum_{b \in \mathcal{F}_i} \big(\mathbb{1}[s_a > s_b] + \tfrac{1}{2}\mathbb{1}[s_a = s_b]\big)}{\sum_i |\mathcal{P}_i|\,|\mathcal{F}_i|},$$

  where $\mathcal{P}_i$ and $\mathcal{F}_i$ are the passing and failing samples of problem $i$. All-pass and all-fail problems have $|\mathcal{P}_i|\,|\mathcal{F}_i| = 0$ and drop out. Their number, and the number of mixed problems, are reported for every model, suite, and stratum.
  - $W$ weights problems by their number of pass-fail pairs. It is the probability that a random passing sample outranks a random failing sample of the same problem, with pairs drawn uniformly.
  - **Secondary:** the problem-averaged version $W_{\text{avg}}$ (each mixed problem weighted equally), the definition used by Miglani et al. (2609.36783).
  - **Effect of the label switch.** Switching from the original to the EvalPlus suite changes which problems are mixed. $W$ is computed on each suite's own mixed set, and the overlap is reported.

**Brier score and its decomposition.**

- $\mathrm{BS} = \frac{1}{n}\sum (s - y)^2$, with the Murphy decomposition into reliability, resolution, and uncertainty, estimated with 15 equal-mass bins.
- The problem-demeaned Brier analog for $d = 1$ uses $s - \bar{s}_i$ and $y - \bar{y}_i$ within mixed problems. It is reported as a secondary within-problem calibration measure.

**Calibration estimator set** (sensitivity analysis, compare 2605.27752 App G):

- debiased equal-mass binned ECE (15 bins, with the debiasing correction of Kumar, Liang, and Ma 2019);
- the binning-free smooth ECE (Blasiok and Nakkiran 2023, with its default kernel bandwidth rule);
- KS calibration error (Gupta et al. 2021, binning-free).

Equal-width 15-bin ECE is computed only for the [2610.31820] reconciliation. Equal-width 10-bin ECE is computed only for comparison with MARGIN. The bibliography entries for the three estimator papers must be fetched before the manuscript cites them (section 14, risk K4).

**Legacy TACE is retired.** The legacy implementation (METHOD_INVENTORY 7.4) has three faults:

- it uses $\lfloor\sqrt{n}\rfloor$ equal-count bins;
- it drops bins whose gap is under 0.01 instead of applying the stated minimum-count rule;
- it weights by bin share without dividing by the number of bins kept.

It therefore matches neither its own text nor a published estimator, and it has no debiasing. The debiased equal-mass ECE replaces it.

## 9. Inference and power

**Bootstrap.**

- **Resampling unit.** One problem-clustered paired bootstrap with $B = 10{,}000$ resamples. Each resample draws problems with replacement from the population, jointly across all models, readouts, suites, and toggle cells, so every comparison is paired.
- **Intervals.** Percentile intervals. The bias-corrected and accelerated interval is a sensitivity analysis for the primary statistic.
- **Shared seed.** A single fixed seed for all metrics (METHOD_INVENTORY 8.5).

**What the bootstrap conditions on.** Fitted readouts are not refit inside resamples. The bootstrap therefore conditions on the out-of-fold scores. Two additions cover refit variance:

- the three fold-seed repeats of every non-LoRA readout, with the primary statistic averaged over seeds;
- a LoRA refit sub-study on one model: three seeds of every LoRA adapter at $l = 1$. The between-seed variance of $\bar{R}$ is added to the bootstrap variance for the TOST decision (normal approximation for that component), and this is stated with the result.

**Shapley intervals.** In each resample, all 16 cells of $\Gamma$ are computed and the four $\phi_v$ are taken. The interval of each term is the percentile interval of its resampled values. The sequential decompositions and the interaction indices get intervals the same way.

**Multiplicity.**

- **Primary test.** One test on the model-pooled residual; no adjustment.
- **Secondary per-model residual tests.** Holm adjustment across the models of the primary set, for each of the two decisions.
- **Shapley terms.**
  - Model-pooled budget: Bonferroni-adjusted intervals (98.75 percent, four terms) are the confirmatory intervals; 95 percent intervals are shown beside them.
  - Per-model and per-stratum budgets: descriptive, at 95 percent, labeled unadjusted.
- **Reconciliation entries.** Each is a separate pre-stated check; no adjustment is applied, and the table says so.

**Power.** The wave 5 simulation was copied (not moved; the scratch originals stay in place) to `docs/s6/power/w5-baseline/`. Its adaptation to the residual-gap TOST and the Shapley terms is `docs/s6/power/power_sim.py` (B9). Results are in `docs/s6/power/POWER.md` and `power_sim.json`; the shared-shock sensitivity is `docs/s6/power/SHARED_SHOCK.md`. All values are planning arithmetic under labeled assumptions (pooled probe within-problem AUROC 0.71, zero-shot stated 0.60, between-problem gap heterogeneity, $\delta = 0.03$), to be replaced by pilot estimates.

- **Chosen $k = 10$ samples per problem, $n = 542$ problems** (HE+ 164 plus MBPP+ 378, the whole label-validity population). LCB release_v6 adds 1,055 problems for its own 3-toggle budget.
- **Primary decision at $M = 6$, $k = 10$, $n = 542$:** P(equivalence | $R = 0$) = 1.00 and P(superiority | $R = 0.06$) = 1.00 in the B9 grid at $M = 9$, and the same at $M = 6$ in the shared-shock run (both $\rho = 0.5$ and $\rho = 1$; mean 90 percent half-width about 0.008).
- **Boundary.** At true $R = \delta$, P(inconclusive) is about 0.9 by construction. That outcome is reportable as "inconclusive at $\delta$".
- **Per model ($M = 1$):** P(equivalence | $R = 0$) = 0.67 and P(superiority | $R = 0.06$) = 0.865 at $n = 542$. Per-model equivalence reaches 0.80 only near $n = 900$. Per-model tests are therefore secondary and may be underpowered for equivalence; this is stated in advance.
- **Mixed problems** (at least one pass and one fail): about 361 of 542 per model at $k = 10$, which sets the effective sample of the within-problem metric.
- **Shapley half-widths** (95 percent, $M = 9$, $n = 542$): $G_0$ 0.0051, difficulty term 0.0063, $R$ 0.0073.
- **Scope of the interval.** The primary interval is conditional on the six named models. Models are not a sampled population, and between-model spread is reported per model.

## 10. Secondary arms

- **Base vs instruct.** Every family with a base and instruct pair enters as a stratum. The full budget (all 16 cells) is computed per model, and the stratum contrast is the difference in each Shapley term between instruct and base, with a paired interval (same problems).
  - Base models need a completion-style generation prompt. The elicitation turns for base models use a plain-text dialogue frame, frozen and hashed like the chat prompts.
  - The zero-shot verbal readouts of base models are expected to parse less often. Parse rates are reported, and the V2 chain is primary for base models if the V1 parse rate falls below 80 percent. That threshold is fixed now.
- **Same-weights reasoning toggle.** The reasoning-toggle model (section 3) is generated twice on the same problems, thinking off and thinking on. Each condition has its own frozen generations, labels, and full budget. The stratum contrast is per term.
- **Intermediate post-training checkpoints.** If section 3 admits a family with released SFT, preference-tuned, and final checkpoints, the budget is computed at each stage, as a descriptive trajectory.
- **Offline routing replay.** It measures the decision cost of each budget term. Two decision problems are replayed on the frozen generations and their labels:
  1. **Best-of-$k$ selection per problem** (within-problem use). The sample with the highest confidence is selected. The value is the selected pass rate. The comparators are:
     - random selection (the mean pass rate);
     - oracle selection (pass@$k$, 1 if any sample passes);
     - regret, defined as oracle minus selected.
  2. **Global verification triage** (pooled use). Samples are sorted by confidence, and the lowest-confidence fraction $b \in \{0.05, 0.1, 0.2, 0.3, 0.5\}$ is sent to execution. The value is the share of all failing samples that the budget catches. The comparators are:
     - random triage (catches the fraction $b$ of failures in expectation);
     - oracle triage (catches $\min(1, bn/n_{\text{fail}})$);
     - regret, defined as oracle minus achieved.

  **Decision cost of a term $v$.** The Shapley value of $v$ in the game whose payoff is the regret gap between routing by $P$ and routing by $S$, computed over the same 16 cells. The same toggles are used; $d$ selects which decision problem scores the cell. Random and oracle regrets are reported as anchors.
  - The replay uses the out-of-fold scores, so no readout sees the label of the sample it routes.
  - This replay is the routing analysis of the earlier positioning work. It is now attached to the budget. [Ribeiro], [2610.31820], CREDO, and NeuroSym-Cal each report a partial version (`research/positioning/w6/DIFFERENTIAL_R1.md` row 12), and the paper cites them.

## 11. Method decisions

One row per METHOD_INVENTORY element. Neither legacy version binds. "Adopted" is this design's definition.

| Row | Element | Adopted definition | Reason |
|---|---|---|---|
| 1.1 | HumanEval source and size | `openai/openai_humaneval` at a pinned dataset revision; 164 problems; the EvalPlus HumanEval+ release is the label-validity population (section 4) | One source, pinned |
| 1.2 | MBPP source and size | The MBPP problems covered by EvalPlus MBPP+ at its pinned version (section 4) | Needed for the EvalPlus suite |
| 1.3 | Fields read from MBPP | Problem text and signature as packaged by EvalPlus; original tests = EvalPlus base inputs | Matches the label suite |
| 1.4 | Subset for sweeps | No sweep subset; every analysis uses the full population | Removes the undocumented first-80 subset |
| 1.5 | Which problems | All problems, listed by ID in the manifest | Same |
| 1.6 | Data for trained readouts | The study's own training-fold samples only | Supervision matching and no leakage |
| 1.7 | Held-out evaluation | Problem-grouped cross-fitting; no example-level split | The legacy example-level split leaked problems |
| 1.8 | Easy and hard subsets | Replaced by the contamination stratum and per-problem pass-rate deciles, reported descriptively | Difficulty enters as the $d$ toggle |
| 1.9 | Other subsets | None | |
| 2.1 to 2.2 | Models | Section 3 | |
| 2.3 | Revision | Every model pinned by repository revision SHA (section 3) | Legacy had none |
| 2.4 | Precision and loading | bf16 weights and activations by default; FP8 only where section 3 requires it, recorded per model; `trust_remote_code` only where the model card requires it, recorded | Reproducibility |
| 2.5 | Hardware and software | One 96 GB GPU; pinned versions of CUDA, PyTorch, vLLM, transformers, PEFT, scikit-learn, and EvalPlus, recorded in the run manifest | Legacy recorded only partly |
| 2.6 | Base of the trained adapters | The model being read; one adapter per (model, fold, suite) | Supervision matching |
| 3.1 to 3.2 | Generation prompts | Section 5, frozen and hashed | Legacy text and code differed |
| 3.3 | Verbal numeric prompt | V1, section 5; a separate elicitation turn after the frozen code; scale 0 to 100 | Legacy asked for a rating before the solution, in the same response |
| 3.4 to 3.5 | Critique and chain-of-thought verbal prompts | Not used; the reasoning stratum covers thinking | Two formats suffice |
| 3.6 | Verbal at a second temperature | Not used; V1 is greedy | Removes a sampled readout |
| 3.7 | Chat template and system turn | The model's own chat template at its pinned revision, no system turn except where the card requires one, rendered and hashed | |
| 3.8 to 3.12 | SFT prompts | Replaced by sections 7.4 and 7.5 | The legacy SFT pipeline is not reused |
| 4.1 | Temperature for frozen samples | 1.0 | Matches the three reconciliation targets |
| 4.2 | Temperature for verbal elicitation | Greedy for V1; V2 is read from logits | Deterministic readouts |
| 4.3 | top-p | 1.0 | |
| 4.4 | Max new tokens | 1,024 non-reasoning; 16,384 reasoning | Section 5 |
| 4.5 | Prompt truncation | None; a prompt longer than the context window is excluded and listed | Legacy silently truncated at 2,048 |
| 4.6 | Stop sequences | End of turn only | |
| 4.7 | Other decoding settings | Seeded per sample (section 5); no top-k; no penalties | Legacy was unseeded |
| 4.8 | Samples per problem | $k$ from section 9 | Power |
| 4.9 | Extra generations | None for the primary analysis: label, readouts, and agreement all use the same $k$ samples. The single extra pass is the generation-shift arm | Fixes the legacy "different generations" problem (METHOD_INVENTORY headline 3) |
| 4.10 | Sweep grids | No temperature or $n$ sweep | Out of scope |
| 4.11 | pass@k | Unbiased estimator $1 - \binom{n-c}{k}/\binom{n}{k}$, reported descriptively | |
| 5.1 | Isolation | Container sandbox, section 6 | Legacy had no isolation beyond a subprocess |
| 5.2 | Timeout scope | Per test, evaluator rule, plus a 60 s program cap | Legacy text said per test; the code timed out per script |
| 5.3 | Pass criterion | Every test passes, normal exit | |
| 5.4 | Which generation carries the label | Each sample carries its own label; no independent label draw | Same-sample readouts and labels |
| 5.5 | Labels for trained readouts | Same as 5.4 | |
| 5.6 | Program assembly | The EvalPlus or LiveCodeBench evaluator's own assembly | |
| 5.7 | Code extraction | First fenced Python block; fallback from the first `def` or `class` line; failures coded (section 6) | Stated, not silent |
| 5.8 | MBPP signature handling | EvalPlus entry point; no renaming repair | Legacy repair changed labels |
| 5.9 | Failed generations | Recorded as a failure code; never an empty string scored silently | |
| 5.10 | Variant harnesses | One harness | |
| 6.1 | Methods | Section 7 | |
| 6.2 | Sampling confidence | Sampling agreement on disjoint inputs (7.7). The legacy execution pass rate on the label tests is retired, because it is computed from the labels | Leakage |
| 6.3 | Log-probability confidence | Geometric-mean token probability (7.6), named as such | Legacy text said sigmoid, code used exp |
| 6.4 | Logit-style variants | Minimum and total log-probability (7.6) | |
| 6.5 | Post-hoc calibration | Isotonic only, cross-fitted on problem folds (7.3); Platt as a sensitivity analysis | Legacy used unshuffled-by-problem KFold |
| 6.6 | AST clustering | Alpha-renamed AST cluster share (7.8) | Legacy formula differed from its text |
| 6.7 | Verbal scale mapping | 0 to 100 divided by 100 | |
| 6.8 | Verbal parsing | Regular expression of 7.2; missing values flagged and imputed from training folds; never a constant default | Legacy defaulted to 0.6 silently |
| 6.9 | Critique and chain-of-thought extraction | Not used | |
| 6.10 | Verbal at a second temperature | Not used | |
| 6.11 | SFT verbal readout | Replaced by the trained readouts of 7.4 and 7.5 | |
| 7.1 | ECE bins | Equal-width bins only for reconciliation; primary estimators in section 8 | |
| 7.2 | Equal-width vs equal-mass | Equal-mass for the debiased ECE and the Brier decomposition | |
| 7.3 | Brier | Mean squared error with Murphy decomposition | |
| 7.4 | TACE | Retired (section 8) | |
| 7.5 | Number of metrics | Section 8 | |
| 7.6 | AUROC | Mann-Whitney with ties at one half; pooled and within-problem | |
| 7.7 | Undefined AUROC | Reported as undefined with the reason (one class); never imputed | |
| 7.8 | Stored point value | Point estimates on the full data; bootstrap means are never reported as point estimates | Legacy stored bootstrap means |
| 7.9 | Thresholds | None; all metrics use continuous scores, except the routing replay's budget fractions | |
| 8.1 | Resample count | $B = 10{,}000$ | |
| 8.2 | Resampling unit | Problems, clustered and paired across everything | |
| 8.3 | Interval type | Percentile; bias-corrected and accelerated as a sensitivity analysis | |
| 8.4 | Dropped replicates | A replicate in which a metric is undefined (for example, no mixed problems) is kept and counted, and the metric's interval is reported with the count of undefined replicates | Legacy dropped them silently |
| 8.5 | Seed and resample sharing | One seed; the same resamples for every metric | |
| 8.6 | Intervals for recalibrated scores | Conditional on cross-fitted maps; fold-seed repeats (section 9) | |
| 9.1 to 9.15 | SFT and DPO pipeline | Replaced by the trained readouts of 7.4 and 7.5; no preference training; no tier sentences | The legacy SFT data overlapped the evaluation set |
| 10 | Random seeds | Generation seeded per sample; folds by problem-ID hash; bootstrap and model fitting seeded and recorded | Legacy generation was unseeded |
| 11 | `src/v4_dprc` | Out of scope (operator decision) | |

## 12. Compute and cost budget

All throughput values are planning assumptions for one 96 GB GPU at bf16. They are not measurements. The pilot measures them, and K7 applies if the measured total exceeds this budget by more than 50 percent. Problem counts and model conditions come from sections 3 and 4; $k = 10$ is the planning value of section 9.

### 12.1 Assumptions

| Quantity | Assumed value |
|---|---|
| Problems per budget model | 542 (label-validity) + 1,055 (LiveCodeBench) = 1,597 |
| Samples per budget model | 1,597 x 10 = 15,970 |
| Mean generated tokens, non-reasoning instruct | 332 per sample (200 on HumanEval and MBPP, 400 on LiveCodeBench; weighted by problem counts) |
| Mean generated tokens, base models | 400 (completion prompts with stop strings) |
| Mean generated tokens, thinking on | 6,000 (cap 16,384) |
| Mean tokens per teacher-forced sequence | 900 non-reasoning (prompt, code, elicitation); 6,900 thinking on |
| vLLM decode throughput, batched, prefix caching on | 8B 4,000 tok/s; 14B 2,500; 32B dense 1,000; 30B-A3B MoE 3,000; gpt-oss-20b 3,000 |
| Teacher-forced prefill with hidden-state capture | 8B 15,000 tok/s; 14B 8,000; 32B 3,500; MoE 10,000 |
| LoRA elicitation-only training (no-grad prefix, gradient only on elicitation tokens) | 0.77 of prefill throughput: 8B 11,500 tok/s; 14B 6,150; 32B 2,700 |
| LoRA full-sequence training (R-Tuning-style) | 8B 5,000 tok/s |
| Adapter-active generation in vLLM | 0.7 of base decode throughput |

### 12.2 Per-stage GPU-hours

Each row gives the arithmetic: tokens divided by throughput.

| Stage | Per condition | Conditions | GPU-hours |
|---|---|---|---|
| Generation, 7-8B instruct | 15,970 x 332 = 5.30M tok / 4,000 = 0.37 h | 3 (Qwen2.5-Coder-7B-I, Qwen3-8B off, Olmo-3-7B-I) + 2 (Olmo SFT, DPO) | 1.84 |
| Generation, 14B instruct | 5.30M / 2,500 = 0.59 h | 1 | 0.59 |
| Generation, 32B instruct | 5.30M / 1,000 = 1.47 h | 2 | 2.94 |
| Generation, base 7-8B | 15,970 x 400 = 6.39M / 4,000 = 0.44 h | 3 | 1.33 |
| Generation, base 14B | 6.39M / 2,500 = 0.71 h | 1 | 0.71 |
| Generation, base 32B | 6.39M / 1,000 = 1.77 h | 2 | 3.55 |
| Generation, Qwen3-8B thinking on | 15,970 x 6,000 = 95.8M / 4,000 = 6.65 h | 1 | 6.65 |
| Generation, [Campos] models (LiveCodeBench only, 10,550 samples) | Coder-30B-A3B: 10,550 x 400 = 4.22M / 3,000 = 0.39 h; gpt-oss-20b at 1,500 tok: 15.8M / 3,000 = 1.47 h | 2 | 1.86 |
| Forward pass (logprobs, hidden states, V2), non-reasoning | 15,970 x 900 = 14.4M tok: 8B 0.27 h; 14B 0.50 h; 32B 1.14 h | 6 at 7-8B (3 instruct + 3 base) + 2 Olmo stages, 2 at 14B, 4 at 32B | 8 x 0.27 + 2 x 0.50 + 4 x 1.14 = 7.72 |
| Forward pass, thinking on | 15,970 x 6,900 = 110M / 15,000 = 2.04 h | 1 | 2.04 |
| Forward pass, [Campos] models | Coder: 10,550 x 1,000 / 10,000 = 0.29 h; gpt-oss at 2,500 tok per sequence: 0.73 h | 2 | 1.02 |
| V1 greedy decode (8 tokens, cached prefix) | under 0.1 h | 17 | 1.0 (allowance) |
| Trained stated readout, 7-8B | per fold: original suite 0.8 x 15,970 x 900 = 11.5M / 11,500 = 0.28 h; EvalPlus suite 0.8 x 5,420 x 900 = 3.9M / 11,500 = 0.09 h; 5 folds = 1.85 h, plus 10 percent for validation and scoring = 2.0 h | 8 (3 instruct, 3 base, 2 Olmo stages) | 16.0 |
| Trained stated readout, 14B | 1.85 x (11,500 / 6,150) x 1.1 = 3.8 h | 2 | 7.6 |
| Trained stated readout, 32B | 1.85 x (11,500 / 2,700) x 1.1 = 8.7 h | 4 | 34.8 |
| Trained stated readout, thinking on | per fold: 0.8 x 15,970 x 6,900 / 11,500 = 2.13 h + 0.8 x 5,420 x 6,900 / 11,500 = 0.72 h; 5 folds = 14.3 h | 1 | 14.3 |
| Generation-shift arm, thinking off (Qwen3-8B) | training per fold 11.5M / 5,000 = 0.64 h + 3.9M / 5,000 = 0.22 h; 5 folds = 4.3 h. Fresh generation 1,597 x 4 x 332 x 2 suites = 4.2M / 2,800 = 0.42 h. Forward on fresh 0.2 h | 1 | 4.9 |
| Generation-shift arm, thinking on, LiveCodeBench only ([2610.31820] reconciliation) | training per fold 0.8 x 10,550 x 7,000 = 59M / 5,000 = 3.3 h; 5 folds = 16.4 h. Fresh 1,055 x 4 x 6,000 = 25.3M / 2,800 = 2.5 h. Forward 0.55 h | 1 | 19.5 |
| LoRA refit sub-study (Qwen2.5-Coder-7B-Instruct, 2 extra seeds, EvalPlus suite) | 2 x 5 x 0.1 h | 1 | 1.0 |
| Pilot (one 7B model, label-validity population, end to end, with debugging) | | 1 | 3.0 |
| **Total** | | | **132.4** |
| With 20 percent contingency | | | **158.9** |

The 32B LoRA rows dominate (34.8 h). If K7 applies, the cuts in the order of section 13 save:

1. The Olmo SFT and DPO stages: 0.74 + 0.54 + 4.0 = about 5.3 h.
2. One second-scale pair: about 9.9 h for the Qwen3-14B pair, or 1.47 + 1.77 + 2.28 + 17.4 = about 22.9 h for a 32B pair.

### 12.3 CPU and storage

- **Execution (CPU).** About 290,000 samples (budget models, [Campos] models, and fresh generation-shift samples), each under 1.5 suites on average. EvalPlus stops a sample at its first failing input. Planning assumptions: 2 CPU-seconds per sample per suite, and a 30 percent cache hit rate from duplicate programs. That gives 290,000 x 1.5 x 2 x 0.7 = 609,000 CPU-s, about 170 CPU-hours: about 5.3 h of wall-clock on 32 cores. Agreement inputs (up to 50 per problem) add about 100 CPU-hours.
- **Hidden-state storage.** 28 vectors per sample: 7 layers at 3 positions, plus 7 mean-pooled. At hidden size 4,096 in float16 that is 229 KB per sample, or 3.7 GB per 8B condition. The total is under 100 GB for all conditions, sharded per model.

### 12.4 Cost-minimizing choices

- **One pass per sample.** Generation once. Then one teacher-forced pass for log-probabilities, hidden states at all candidate layers and positions, and the V2 readout. V1 adds only an 8-token greedy decode from the cached prefix.
- **Samples reused across methods.** All readouts, baselines, labels, agreement, clustering, the routing replay, and both reconciliation entries on the same model read the same frozen generations. The only exception is the generation-shift arm, which is by definition fresh.
- **Execution cache keyed by normalized code hash** (section 6). Shared across samples, models, suites, and the agreement runs.
- **vLLM prefix caching.** The $k$ samples of a problem share the prompt prefix. The V1 decode shares the prefix of the teacher-forced pass.
- **Elicitation-only LoRA trained on a no-grad prefix.** Gradients flow only through elicitation tokens, which keeps the trained readout near prefill cost.
- **Resumable per-model shards.** Every stage writes per-model, per-benchmark shards with content hashes. A restart skips completed shards. The run manifest lists every shard hash.
- **A pilot before the full matrix** (section 13).
- **No API-model arms.** No claim in section 1 requires one. EvalPlus's LLM-based input generator is not used (section 4).

## 13. Kill and pivot criteria

The pilot (section 12) runs one model of the primary set on the label-validity population with $k$ samples, end to end. These criteria are fixed before it runs.

| ID | Trigger | Action |
|---|---|---|
| K1 | Reference-solution failures exclude more than 5 percent of the problems of a suite | Stop. Fix the harness or the suite version. Do not proceed until the excluded share is at most 5 percent or the operator accepts the list |
| K2 | Fewer mixed problems per model than section 9 assumes, by more than 25 percent, on the primary population | Raise $k$ up to the compute cap of section 12, or add LiveCodeBench problems to the primary population with a label-validity analog (public vs full tests), as an operator decision. $\delta$ does not change |
| K3 | The V1 parse rate is below 80 percent for an instruct model | Switch that model's primary chain to V2 (fixed rule, section 10). If V2 is degenerate (one value for every sample) on more than half the primary models, the zero-shot stated readout is uninformative. G0 is then reported as such, and the contribution reverts to the budget of the trained readout against the probe |
| K4 | The trained readout ($t = 1$) fails to train: out-of-fold log loss no better than the training base rate on a majority of folds | Retry once with learning rate $3 \times 10^{-4}$ and 2 epochs, both fixed now. If it still fails, report it. The supervision term is then bounded by the isotonic readout, and the primary test is reported with that limitation |
| K5 | A reconciliation target fails to reproduce (section 2) | Report it (section 2.1). It does not stop the study, because the budget is defined on this design's generations. If [2610.31820]'s tie fails under both readings, the paper reports that the published tie is not reproduced on public checkpoints, and the generation-shift term is reported without the claim that it explains the published tie. If [Campos]'s prompt-only pattern fails, the difficulty term is reported as model-specific |
| K6 | Concurrent work posted before submission occupies the joint attribution (a full text attributing the probe-versus-stated gap to two or more of the four terms on shared generations) | Re-run the Part A occupancy check before the manuscript is drafted. If it is occupied, the contribution becomes the reproduction and reconciliation on code, under the TMLR Reproducibility certification criteria (`docs/s2/venue/TMLR_RUBRIC.md` section 3). This is the pivot |
| K7 | The compute estimate after the pilot exceeds the section 12 budget by more than 50 percent | Drop strata in this order: the intermediate-checkpoint trajectory, the second scale of one family, the reasoning-on condition's second label suite. The primary set and the reconciliation models are never dropped |

## 14. Risk register

| ID | Risk | Likelihood | Effect | Mitigation |
|---|---|---|---|---|
| K1 | The LoRA readout active only in the elicitation turn needs a custom position mask; a bug would leak code-token adaptation | medium | the supervision term is wrong | Unit test: with the mask, the KV cache of the prompt and code is bit-identical to the base model's; checked in the pilot |
| K2 | Too few mixed problems on HumanEval for strong models (most problems all-pass) | high for 32B-class instruct models | $W$ rests on few problems | Report mixed counts; K2 rule; primary pooling over models |
| K3 | EvalPlus flips are rare for some models, so $\phi_l$ is near zero by construction | medium | label term is uninformative for those models | Report the flip table; the term is still estimated, with its interval |
| K4 | Estimator citations (debiased ECE, smooth ECE, KS) are not yet fetched records | certain | bibliography rule | Fetch the records before drafting |
| K5 | The [2610.31820] protocol is unrecoverable (unreleased checkpoints, unstated generations) | certain | reproduction is approximate | Both readings run; deviations listed; claims about the paper limited to its text |
| K6 | Gated model cards or licences restrict use | medium | model swap | Section 3 lists alternatives |
| K7 | Test-time contamination of HumanEval and MBPP for all models | certain | the label-validity population is all pre-cutoff | The contamination stratum uses LiveCodeBench windows. The primary test is stated for the pre-cutoff population, and the stratum result is reported separately |
| K8 | Sandbox escapes or resource exhaustion from generated code | low | host damage | Container limits, no network, unprivileged user, tmpfs |
| K9 | Refit variance of LoRA readouts is larger than the bootstrap variance | medium | TOST is anticonservative | Refit sub-study, and its variance added to the decision (section 9) |
| K10 | Non-commuting toggles make Shapley values hard to read | certain | interpretation | Interaction indices and both sequential orders are reported |
| K11 | A failed reconciliation is read as a flaw of this design | medium | reviewer doubt | Deviations stated before running; failure is reported as a finding (K5) |
| K12 | Hidden-state storage exceeds local disk | low | pipeline stall | Seven layers, three positions, float16, per-model shards; size in section 12 |

## 15. Terminology

The glossary is copied into the glossary of `paper/STYLE.md`.

| Term | Symbol | Definition | Do not use |
|---|---|---|---|
| frozen generations | $c_{mij}$ | the $k$ samples per problem per model, generated once at temperature 1.0 and reused by every readout | "responses", "completions" (as a defined term) |
| sample | $j$ | one frozen generation of one problem | "candidate" (except when quoting [Campos]), "attempt" |
| problem | $i$ | one benchmark task | "task" (except when quoting [Ribeiro]), "question" |
| original suite | $O$ | the benchmark's own tests (EvalPlus base inputs for HumanEval and MBPP) | "base tests" |
| EvalPlus suite | $E$ | the original suite plus EvalPlus's added inputs | "augmented tests", "HumanEval+ tests" (except as the dataset name) |
| label | $y^{O}, y^{E}$ | 1 if the sample passes every test of the suite | "correctness score" |
| readout | | a function from a sample to a confidence score in [0, 1] | "signal", "method" |
| hidden-state probe | $P$ | logistic regression on one layer's hidden state at the last code token | "internal confidence" |
| stated confidence | $S$ | a readout the model produces in an elicitation turn about its frozen sample (V1 or V2, zero-shot or trained) | "verbal confidence" (except "verbal format V1"), "expressed confidence" |
| zero-shot stated readout | $S^Z$ | stated confidence with no training | |
| trained stated readout | $S^T$ | stated confidence read through a LoRA adapter active only in the elicitation turn, fit on the probe's labels and folds | "fine-tuned verbal" |
| R-Tuning-style readout | $S^R$ | the [2610.31820]-style categorical readout with the adapter active in generation | |
| prompt-only probe | | the probe read at the last prompt token, before any code | "input-only probe" |
| code-text-only classifier | | a classifier on the code string alone | "text-only probe" |
| sampling agreement | $A$ | share of the other samples with the same behavior signature on held-out inputs | "consistency", "self-consistency" (except when quoting) |
| pooled AUROC | | AUROC over all samples of the population | |
| within-problem AUROC | $W$ | pair-weighted AUROC over pass-fail pairs inside problems | "per-problem AUROC" |
| mixed problem | | a problem with at least one passing and one failing sample under the active suite | |
| toggle | $r, t, d, l$ | a binary change of scoring setup from uncontrolled (0) to controlled (1) | "ablation", "factor" |
| scoring configuration | $x$ | a vector of toggle levels | |
| gap function | $\Gamma(x)$ | probe metric minus stated metric at configuration $x$ | |
| raw gap | $G_0$ | $\Gamma(0,0,0,0)$ | "disconnect" (as a measured quantity) |
| residual gap | $R$, $\bar{R}$ | $\Gamma(1,1,1,1)$; its mean over the primary models | |
| budget term | $\phi_v$ | the Shapley value of toggle $v$ | "contribution", "effect" (unqualified) |
| systematics budget | | the decomposition $G_0 + \sum_v \phi_v = R$ with intervals | "error budget" (exposition only) |
| generation-shift term | $\Delta_g$ | the difference in a trained readout's metric between frozen and fresh generations | "distribution shift" |
| margin | $\delta$ | the pre-registered equivalence margin, 0.03 in $W$ | "threshold" |
| contamination stratum | | pre-cutoff vs post-cutoff release window per model | "leakage" |
| routing replay | | the offline replay of selection and triage decisions from out-of-fold scores | "deployment" |
| regret | | oracle value minus achieved value in the routing replay | |

## 16. Figure plan

Every figure is generated from `analysis/` JSON. It follows `paper/STYLE.md` rules 14 and 15: one style, no in-figure annotations, captions of at most three sentences, each figure necessary.

| ID | Content | Claim it supports |
|---|---|---|
| Figure 1 (hero) | The budget: for each primary model and the model-pooled row, a horizontal waterfall from $G_0$ through $\phi_l$, $\phi_d$, $\phi_t$, $\phi_r$ to $R$, with 95 percent intervals on every bar and a shaded band at $\pm\delta$ around zero at the residual | The primary result (H1 or H2) and the term-by-term attribution (H3) |
| Figure 2 | Reconciliation: each published configuration of [Ribeiro], [Campos], and [2610.31820] as a point (published value) beside its reproduction (interval), on the axis of its own published unit, grouped by paper | Section 2 reproductions |
| Figure 3 | Generation shift: the R-Tuning-style readout's pooled and within-problem AUROC under reading A and reading B, beside the probe, for the generation-shift model | $\Delta_g$ and the [2610.31820] reading question |
| Figure 4 | Strata: Shapley terms by stratum (contamination, family, scale, base vs instruct, reasoning on/off), one panel per term | H4 |
| Figure 5 | Routing replay: regret against budget fraction for routing by $P$ and by $S$ at the uncontrolled and controlled configurations, with random and oracle anchors | Decision cost of each term |
| Table 1 | Model and benchmark matrix with revisions, cutoffs, problem counts, mixed counts | Setup |
| Table 2 | The 16-cell gap function for the pooled set, with intervals | Shapley inputs (transparency) |
| Table 3 | Primary test: $\bar{R}$, 90 and 95 percent intervals, both decisions, and the $\delta$ sensitivity | H1 or H2 |
| Table 4 | Reconciliation table (section 2.1) | Section 2 |
| Table 5 | All readouts and baselines in pooled AUROC, $W$, AUPRC, Brier, and the three calibration estimators, per model (appendix) | Completeness |
| Table 6 | Label flips and extraction failures per model and suite (appendix) | Section 6 |

## 17. Operator sign-off

Not signed. This draft is not frozen or hashed. Sign-off freezes the design for the pilot.

```
Design version:            R__
Margin delta (W):          ______
k and problem counts:      ______
Primary model set:         ______
Readings for 2610.31820:   [ ] both  [ ] A only  [ ] B only
Approved by:               ____________________
Date:                      ____________________
Design SHA-256 at freeze:  ____________________
```
