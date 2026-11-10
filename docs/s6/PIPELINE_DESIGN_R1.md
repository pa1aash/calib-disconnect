# Pipeline design R1 (draft, pre-registration candidate): a systematics budget for the calibration disconnect in code language models

Status: DRAFT R1, wave 6, 2026-11-10. It revises R0 (`docs/s6/PIPELINE_DESIGN_R0.md`, kept unchanged) after three Part B critics; every change is traced in `docs/s6/CRITIQUE_DISPOSITION.md`. It is not frozen and not hashed. No pipeline code, run, or manuscript text exists. Every number in this file is a design parameter, a published value quoted from a saved full text (with location), or a planning assumption labeled as such. None is a result.

Inputs: the operator decisions of wave 6; `research/positioning/w6/` (Part A); `docs/s2/METHOD_INVENTORY.md`; `docs/s2/venue/TMLR_RUBRIC.md`; `paper/STYLE.md`; the Part B fact records in `docs/s6/parts/models-B3/`, `docs/s6/parts/bench-B4/`, and `docs/s6/parts/power-B9/`; the power files in `docs/s6/power/`; and the critic records in `docs/s6/parts/critic-B-method/`, `critic-B-tmlr/`, and `critic-B-budget/`.

**Citation rule for this file.** The rule covers every sentence that overlaps prior or concurrent work:

| Work | Short form |
|---|---|
| Ribeiro et al., arXiv 2512.07404, ICSE 2026 | [Ribeiro] |
| Campos, Klassert, and Ulges, arXiv 2611.07876 | [Campos] |
| Wu and Ji, arXiv 2610.31820 | [2610.31820] |

The same rule applies to the adjacent works found in Part A:

| Work | Where it must be cited in the paper |
|---|---|
| MARGIN 2605.22949 | the label-validity toggle (augmented tests on the same generations) |
| Kim and Kang 2605.27752 | the framing: a readout comparison that moves with measurement choices on fixed answers; the estimator set |
| 2609.04582 | the recalibration-versus-residual split; nested probe selection; clustered inference |
| RADAR 2610.22139 | the recalibration-versus-residual split |
| 2609.33290 | the generation-shift term (a trained readout scored on its own samples against a probe on the original samples) |
| CREDO 2609.34857 | the trained stated readout on code |
| 2610.25846 and 2605.09502 | prompt-only or text-surface baselines and within-problem difficulty controls outside code |
| 2610.27455 | hidden-state gain over output-side feature blocks (block-removal attribution) |
| Miglani et al. 2609.36783 | within-problem AUROC of a probe against token likelihood on code |

The measurement-instrument and error-budget language is exposition only and is never claimed as novel.

## 1. Estimands and hypotheses

### 1.1 Objects

- **Models.** $m \in \mathcal{M}$ (section 3).
- **Problems.** $i \in \mathcal{I}$, with benchmark populations defined in section 4.
- **Frozen generations.** For each model and problem, $k$ samples $c_{mij}$, $j = 1..k$. They are generated once (section 5), hashed, and never regenerated. Every readout except the generation-shift arm is computed on these same strings.
- **Labels.** $y^{O}_{mij}$ under the original test suite and $y^{E}_{mij}$ under the EvalPlus suite (section 6).
- **Readouts.** Each readout maps a sample to a score in [0, 1] (section 7):
  - $P$: the hidden-state probe (the selected member of a pre-specified linear probe family, section 7.1);
  - $S$: the stated-confidence readout, whose form depends on the supervision level.

### 1.2 The gap function and the raw gap $G_0$

A scoring configuration is a vector $x = (r, t, d, l) \in \{0, 1\}^4$ of four toggles, each switched from its uncontrolled level (0) to its controlled level (1):

| Toggle | Term | 0 (uncontrolled) | 1 (controlled) |
|---|---|---|---|
| $r$ | supervision, recalibration | stated readout used as elicited | stated readout passed through an isotonic map fit on training-fold data only (section 7.3) |
| $t$ | supervision, training | zero-shot stated readout | trained stated readout (LoRA adapter active only in the elicitation turn, fit on the same labels and folds as the probe; section 7.4; compare [2610.31820] and CREDO 2609.34857) |
| $d$ | difficulty | pooled scoring | within-problem scoring |
| $l$ | label validity | original test suite (labels for fitting and scoring) | EvalPlus suite (all supervised readouts refit; compare MARGIN 2605.22949, which re-scores frozen programs under EvalPlus for verbalized confidence only) |

When $t = 1$ and $r = 1$, the isotonic map is fit on scores of the trained readout that were produced for training-fold samples by adapters that did not see those samples (inner cross-fitting, section 7.3). No test-fold score or label enters any map.

**Gap function.** For a metric $\mathrm{M}$, the gap at configuration $x$ is

$$\Gamma_{\mathrm{M}}(x) = \mathrm{M}_d\big(P^{(l)}, y^{(l)}\big) - \mathrm{M}_d\big(S^{(r,t,l)}, y^{(l)}\big),$$

on the frozen generations, where $\mathrm{M}_d$ is the pooled version of the metric when $d = 0$ and the within-problem version when $d = 1$ (section 8). Positive values mean the probe is ahead.

**Primary metric.** Discrimination: pooled AUROC at $d = 0$ and pair-weighted within-problem AUROC $W$ at $d = 1$. The same budget is reported for Brier score and the calibration estimators as secondary metrics. For these, $d = 1$ means the problem-demeaned version defined in section 8.

**Ties created by recalibration.** For discrimination metrics, a recalibrated score is ranked by the pair (isotonic value, pre-map score), lexicographically. The isotonic step function therefore never creates ties that the pre-map score did not have. Without this rule, the step function would merge the samples of a problem into ties and pull $W$ of $S$ toward 0.5 while the probe is untouched, which biases $R$ upward (methodologist F1). Tie rates with and without the rule are reported, and the no-tie-break variant is a sensitivity analysis.

**Raw gap.** $G_0 = \Gamma(0, 0, 0, 0)$: probe against zero-shot numeric verbal confidence, pooled AUROC, original tests, frozen generations. Comparisons of this kind on code are reported in three works, each in its own configuration:

- pooled probe against zero-shot verbalized confidence in [2610.31820] Table 3;
- probe against reflective token readouts in [Ribeiro], scored within task as selection accuracy;
- probe against P(Yes) in [Campos], pooled and within problem.

$G_0$ is this design's analog on its own generations, not a published value. Each paper's own configuration is reproduced separately as a reconciliation entry (section 2).

**Residual gap.** $R = \Gamma(1, 1, 1, 1)$: probe against the trained, isotonic-recalibrated stated readout, within-problem AUROC, EvalPlus labels, identical frozen generations.

**Pooled residual.** $R_{\text{pool}} = \Gamma(1, 1, 0, 1)$: the same comparison scored pooled. Because $G_0$ is pooled and $R$ is within-problem, $R$ alone cannot say whether the probe's pooled advantage survives supervision and relabeling. $R_{\text{pool}}$ answers that and is reported as a pre-specified secondary statistic with the same three decisions (section 1.6). [Campos] already shows on code that pooled AUROC overstates candidate-level discrimination (Sec VI-C c, `2611.07876.txt:556-566`); the budget makes that difference one of its terms, $\phi_d$.

### 1.3 Toggles, strata, and sensitivity analyses

| Term | Role | Definition |
|---|---|---|
| Recalibration ($r$) | toggle | isotonic map (section 7.3) |
| Training ($t$) | toggle | trained stated readout (section 7.4) |
| Difficulty ($d$) | toggle | pooled vs within-problem scoring |
| Difficulty baselines | reported beside $d$ (not a toggle) | prompt-only probe and code-text-only classifier (sections 7.9, 7.10), fit on the same folds. They report how much of the pooled AUROC of $P$ and $S$ is reachable without the sample ([Campos] on code; 2610.25846 and 2605.09502 outside code) |
| Diagnostic split of $d$ | reported beside $\phi_d$ | pooled AUROC restricted to mixed problems, and fold-averaged pooled AUROC, so that $\phi_d$ can be read as (restriction to mixed problems) plus (within-problem conditioning) plus (cross-fold pooling) |
| Label validity ($l$) | toggle | original vs EvalPlus suites, with refitting |
| Diagnostic split of $l$ | reported beside $\phi_l$ | at the full configuration, the change from refitting on EvalPlus labels while scoring on original labels, then the change from scoring on EvalPlus labels; and $W$ on the problems mixed under both suites, so that relabeling is separated from the change in the mixed set |
| Generation shift ($g$) | conditional contrast, outside the attribution | $\Delta\Gamma_g$ (section 1.5) |
| Contamination | stratum | problem release date relative to the model's stated cutoff (section 4) |
| Model family and scale | strata | section 3 |
| Base vs instruct, reasoning on/off | strata and secondary arms | section 10 |
| Calibration estimator | sensitivity analysis | section 8 (compare 2605.27752, which varies the estimator as an axis) |
| Zero-shot elicitation format | sensitivity analysis | the budget is recomputed with the second verbal format (P(Yes), section 7.2) as the zero-shot readout |
| Probe family | sensitivity analysis | $R$ against each member of the probe family separately (section 7.1) |
| Adapter capacity | sensitivity analysis | $R$ at LoRA ranks 1, 4, and 16, and a LoRA-plus-linear-head control (section 7.11) |

**The isotonic toggle in the discrimination budget.** With the lexicographic rule, a monotone map leaves the within-problem ranking of a problem's samples unchanged (all samples of a problem lie in one fold and get one map). So $r$ is a null player for $W$ by construction, and on pooled AUROC it moves the gap only through fold-to-fold differences between the fitted maps. Its Shapley value on discrimination is reported, expected near zero, and not interpreted.

On the Brier and calibration budgets, $r$ is the term that separates a recalibration-removable gap from a residual. That is the split made by RADAR 2610.22139 for risk and by 2609.04582 for a probe-versus-answer gap. The budget applies it to the probe-versus-stated gap and does not claim it as a new decomposition. On the problem-demeaned Brier analog, isotonic is expected to do little, because demeaning removes the level shift it corrects; $r$ is read on the pooled calibration budget.

### 1.4 Attribution

**What the attribution is.** An accounting identity over scoring configurations. Each term says how much the measured gap moves when one scoring choice changes, averaged over the settings of the others. It is not a causal effect of a property of the model, and the paper says so where the budget is first shown.

**Primary: Shapley values.** Over the four toggles $N = \{r, t, d, l\}$:

$$\phi_v = \sum_{S \subseteq N \setminus \{v\}} \frac{|S|!\,(|N| - |S| - 1)!}{|N|!}\,\big[\Gamma(S \cup \{v\}) - \Gamma(S)\big],$$

where $\Gamma(S)$ is the gap with the toggles in $S$ at level 1 and the rest at level 0.

- **Efficiency.** $G_0 + \sum_v \phi_v = R$. The budget reads: raw gap, plus the four terms (each expected to be negative when a control narrows the gap), equals the residual.
- **Cells.** All 16 cells of $\Gamma$ are computed on the same frozen generations, the same problem set (section 4: problems valid under both suites), and the same bootstrap resamples. Every cell is a well-defined scoring configuration, so the game is defined at every coalition. None of the four toggles changes the generations.
- **Non-commutation.** The toggles do not commute in effect. For example, $l$ changes which samples are positive, and that changes what $d$ removes. Shapley values split each interaction equally among its members. The pairwise interaction indices (Shapley interaction index, order 2) for the six pairs are therefore reported in the main text, beside the terms (Table 2).

**Secondary: sequential decompositions.** Two canonical orders are reported:

- labels first $(l, d, t, r)$: fix the labels, then the scoring, then the readout;
- readout first $(r, t, d, l)$.

The labels-first order follows the logic of measurement: a gap is first measured against valid labels and at the right granularity, and the readout is changed last. The spread between the two orders, beside the Shapley value, shows how order-dependent each term is. (The B9 power script names these orders differently; its `seq_fwd` is the readout-first order. The paper uses only the names above.)

### 1.5 Generation-shift contrast

The generation-shift contrast is defined for one trained readout, the [2610.31820]-style categorical readout $S^R$, whose adapter is active in generation as well as in the readout. The confound it measures is the one in 2609.33290, where a trained stated readout is scored on the student's own samples while the probe scores the original model's samples (`research/positioning/w6/DIFFERENTIAL_R1.md`, note under the table).

Two generation sets are scored, each by both readouts, so each comparison is paired:

- **fresh ($g = 1$):** $k_g = 10$ samples per problem generated with the adapter active, executed under both suites (reading A of `research/positioning/w6/R2610_31820_PROTOCOL.md`); the probe is read on these samples by a base-weights forward pass;
- **frozen ($g = 0$):** the frozen generations, with $S^R$ teacher-forced (reading B).

$$\Delta\Gamma_g = \big[\mathrm{M}_d(P) - \mathrm{M}_d(S^R)\big]_{g=0} - \big[\mathrm{M}_d(P) - \mathrm{M}_d(S^R)\big]_{g=1},$$

computed at $r = 0$ for $d \in \{0, 1\}$ and $l \in \{0, 1\}$. It is the part of a probe-versus-trained-readout difference that comes from scoring on different generations. With it, the pass rate, the number of mixed problems, and the extraction-failure rate of each generation set are reported, because the fresh set changes all three.

**Why it is outside the attribution.** The residual is defined on identical generations, and $g$ is undefined when $t = 0$ (a zero-shot readout does not change the generator). The R0 five-player game is dropped: its $t \times g$ split was not interpretable (methodologist F15, TMLR F17).

**Readout-format contrast.** $S^R$ at $g = 0$ is compared with this design's trained readout $S^T$, both on frozen generations, and the difference is reported in the reconciliation table.

### 1.6 Primary test and the margin $\delta$

**Primary statistic.** $\bar{R} = |\mathcal{M}_{\mathrm{primary}}|^{-1} \sum_m R_m$, the mean residual over the six primary models (section 3), on the label-validity population (section 4). All decisions come from one problem-clustered paired bootstrap (section 9).

**Three mutually exclusive decisions**, at $\alpha = 0.05$ each, with $(L, U)$ the 90 percent interval (two-sided, so each bound is a one-sided 95 percent bound):

| Decision | Hypothesis rejected | Reached when |
|---|---|---|
| D1, equivalence (TOST) | $\lvert\bar{R}\rvert \ge \delta$ | $-\delta < L$ and $U < \delta$ |
| D2, probe ahead by more than the margin | $\bar{R} \le \delta$ | $L > \delta$ |
| D3, stated readout ahead by more than the margin | $\bar{R} \ge -\delta$ | $U < -\delta$ |

At most one can be reached. If none is, the result is reported as inconclusive, with the interval. The conventional bounds ($\bar{R} > 0$, $\bar{R} < 0$) are reported beside them and labeled secondary. The interval used for the decisions includes the refit-variance component (section 9).

**The margin: $\delta = 0.03$ in pair-weighted within-problem AUROC.** It is a substantive choice, not a power choice. The power analysis shows that the design could also decide at 0.02 (section 9), so decidability does not single out 0.03. The reasons:

1. **The field already reads differences of this size as ties.** [2610.31820] calls its trained readout and its probe comparable at pooled differences up to .02 (Table 3). Miglani et al. (2609.36783, Table 1) report within-problem differences of .004 and .026 between a probe and token likelihood on code, as point estimates, without significance claims (`research/positioning/w6/CLOSED_ITEMS.md`). A margin of .03 classifies all of these as within the margin. The pooled anchor is in a different unit from $W$, and it is used only as the field's reading of a tie, not as a calibration of $W$.
2. **The published pooled advantages are an order of magnitude larger.** The probe-over-zero-shot-verbalized gaps on code in [2610.31820] Table 3 are .20 to .31 (Qwen3-8B .88 - .60 and .84 - .61; Nemotron .89 - .58 and .80 - .60).
3. **Published within-problem values on code are spread far wider than the margin.** [Campos] Table V reports within-problem AUROC from .514 to .781 across readouts and models in distribution (for example, Qwen3-Coder: judging-pass probe .553, code-token probe .620; gpt-oss: .772 and .781), and states that trained methods reach within-problem AUROC of 0.69 to 0.78 only for gpt-oss in distribution (`2611.07876.txt:565-566`). A difference under .03 is small against that spread.

The R0 anchor ".627 against .629" came from the language-shift setting of [Campos] and is withdrawn as a within-distribution anchor (methodologist F11, TMLR F6).

**Sensitivity.** The decisions are also reported at $\delta \in \{0.02, 0.05\}$. The margin is fixed at sign-off and is not changed after the pilot, and the pilot does not see any $\Gamma$ cell of a primary model (section 13).

**Pooled residual.** $R_{\text{pool}}$ gets the same three decisions at a pooled-AUROC margin of 0.03, labeled secondary. The pooled tie width of [2610.31820] (.02) is inside it.

### 1.7 Hypotheses

- **H1 (primary).** D1, equivalence: $|\bar{R}| < \delta$.
- **H2 (primary).** D2, probe ahead: $\bar{R} > \delta$.
- **H2' (primary).** D3, stated readout ahead: $\bar{R} < -\delta$.
- **H3 (secondary, descriptive).** The sign and interval of each Shapley term and each pairwise interaction on the primary metric. No directional hypothesis is stated for any term, and the pilot is not used to choose signs. The model-pooled terms carry simultaneous (Bonferroni) intervals so that the four can be read together; they are still descriptive.
- **H4 (secondary).** The budget is computed separately in each stratum (contamination, family, scale, base vs instruct, reasoning on/off), with the stratum-by-term table, labeled unadjusted (section 9).

### 1.8 Contribution statement for each outcome

The paper keeps exactly one of these, with the numbers filled from generated macros. Two template rules: a term is named in the sentence only if its simultaneous interval excludes zero; and the sentence names the model set as it is ("six open instruct models from three families: four Qwen and two Olmo"), never "open models" in general.

- **D1, equivalence.** "On frozen, execution-labeled code from six open instruct models (four Qwen, two Olmo), a trained stated readout matches a hidden-state probe within problems: after training the stated readout on the probe's labels, scoring within problems, and relabeling with EvalPlus, the within-problem gap lies within 0.03 AUROC of zero. The pooled gap of [G0] AUROC is attributed, with problem-clustered intervals, to [named terms]." It is followed by the pooled-residual result in one sentence, and by the capacity caveat: the trained readout is a low-rank adapter that reads the code through attention, so equivalence shows that supervised stated confidence can express what the probe reads, not that zero-shot stated confidence does.
- **D2, probe ahead.** "On frozen, execution-labeled code from six open instruct models (four Qwen, two Olmo), a hidden-state probe ranks a problem's samples better than a stated readout trained on the same labels, by more than 0.03 within-problem AUROC, after EvalPlus relabeling. The pooled gap of [G0] AUROC is attributed, with problem-clustered intervals, to [named terms] and this residual."
- **D3, stated readout ahead.** "On frozen, execution-labeled code from six open instruct models (four Qwen, two Olmo), a stated readout trained on the probe's labels ranks a problem's samples better than the probe, by more than 0.03 within-problem AUROC, after EvalPlus relabeling. The pooled gap of [G0] AUROC in favor of the probe is reversed by [named terms]."
- **Inconclusive.** "On frozen, execution-labeled code from six open instruct models (four Qwen, two Olmo), [named terms] account for [share] of the pooled probe-over-stated gap of [G0] AUROC, and the within-problem residual lies in [lo, hi] AUROC, which neither establishes nor excludes a gap of 0.03."

Each of these sentences that contrasts pooled with within-problem scoring cites [Campos]; each that involves a trained stated readout cites [2610.31820] and CREDO 2609.34857; each that involves EvalPlus relabeling of frozen samples cites MARGIN 2605.22949.

Each is followed in the paper by the reconciliation sentence: "On this design's generations, analogs of the configurations of [Ribeiro], [Campos], and [2610.31820] [reproduce / do not reproduce / are undetermined against] their published patterns, and each is placed at the budget cell it shares, where one exists (Table [R])."

## 2. Reconciliation targets

### 2.1 Common reporting

For each target, the reconciliation table has one row per published comparison. Each row gives:

- the published value, quoted from the saved full text with its location;
- the value reproduced on this design's frozen generations, with its 95 percent problem-clustered interval;
- the deviations from the published protocol;
- the shared budget cell: the cell of this design's lattice that the analog shares with the budget, if any, or "none" when the analog's readout or metric is outside the lattice (TMLR F2).

Each entry is an analog on this design's generations of a published configuration, not the published experiment: models, data, and metrics differ as listed under each target.

**Outcome of each check: one of three.**

1. **Reproduced.** Both hold:
   - *Pattern.* Each published ordering that the check names holds with a paired 95 percent interval that excludes zero, and each published tie holds with a paired interval inside the published tie width.
   - *Level.* The reproduced 95 percent interval lies inside the published value plus or minus a pre-stated tolerance of 0.05 in the published unit (an equivalence-style check, so a wide interval cannot count as a reproduction).
2. **Not reproduced.** A named ordering is reversed with an interval that excludes zero, or the reproduced interval lies entirely outside the published value plus or minus the tolerance.
3. **Undetermined.** Neither of the above. The interval is reported, and the entry is not counted as a reproduction (methodologist F19, TMLR F10).

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
- **Check.**
  - Pattern: LAT above Random and LAT above Reflective T/F, each with a paired interval that excludes zero. These are the two large published gaps (20.6 and 58.7 points). The LAT-minus-Intrinsic difference (4.9 points) is reported descriptively, because 121 problems give little power for it.
  - Level: the LAT and Intrinsic values against 85.1 and 80.2.
  - Recorded oddity: the published Reflective formats rank below Random (24.8 and 26.4 against 64.5), so ranking by them selects failing samples more often than chance. The reproduction reports whether this holds; it is not part of the check.
- **Shared budget cell.** None for pass@rank-1. The same samples scored by $W$ give the cell $(r, t, d, l) = (0, 0, 1, 0)$ with the V2 format, reported beside it.

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
  - Release window: [Campos] uses problems released October 2024 to May 2025, but release_v6 ends in April 2025 (section 4). The May 2025 problems are not available, and the analog uses October 2024 to April 2025.
- **Check.** The prompt-only probe's within-problem AUROC is 0.5 by construction (its score is constant within a problem), so it is not a check (methodologist F18, TMLR F10). The check is:
  - pooled AUROC of the prompt-only probe within 0.03 of the code-token probe for Qwen3-Coder (published .891 against .895);
  - for gpt-oss, the prompt-only pooled AUROC below the code-token probe, with a paired interval that excludes zero (published .720 against .864);
  - within-problem AUROC of the code-token probe above 0.5 for both models, with intervals that exclude 0.5;
  - for Qwen3-Coder, the judging-pass probe below the code-token probe within problem (published .553 against .620), paired.
- **Shared budget cell.** The code-token probe is this design's $P$; the P(Yes) readout is the V2 zero-shot readout. The within-problem comparison of the two is the cell $(0, 0, 1, 0)$ of the V2 sensitivity chain on LiveCodeBench.

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
  - R-Tuning-style readout: trained per section 7.5 and scored under reading A (its own fresh generations, $k_g = 4$ per problem as in the paper) and reading B (frozen generations).
  - Probe and metrics: the same-label probe, read on the same generation set as the readout it is compared with (a base-weights forward pass over the fresh samples under reading A), so both readings are paired comparisons. Pooled AUROC, 15-bin equal-width ECE, and Brier.
- **Deviations to record:**
  - The public checkpoint is used instead of the PPO checkpoints.
  - TACO, CodeContests, and Codeforces are not used.
  - The probe layer is chosen by this design's nested procedure (unstated in the paper).
  - R-Tuning hyperparameters are this design's (unstated for Sec 4 of the paper).
  - Labels come from execution.
  - Nemotron-Cascade-8B is reproduced only if section 3 admits it.
- **Check.** Three parts:
  - pooled AUROC of the R-Tuning-style readout within 0.02 of the probe, as the paper's tie, under each reading separately;
  - zero-shot verbalized below both, with paired intervals that exclude zero;
  - levels within the tolerance of the published LiveCodeBench values.

  The comparison is reported under both readings. Whichever reading reproduces the published tie is evidence about the paper's unstated protocol, and the design reports it as such and not as a fact about the paper.
- **Shared budget cell.** Under reading B, the R-Tuning-style readout against the probe at pooled scoring and original labels is the cell $(0, 1, 0, 0)$ with $S^R$ in place of $S^T$ (the readout-format contrast of section 1.5). Under reading A there is no shared cell, because the generations differ.

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

**Family balance (TMLR F13).** Four of the six come from one developer (Qwen2.5-Coder and Qwen3), and two from Olmo 3. Every result is also reported per family, and the outcome sentences name the set as it is (section 1.8). Replacing one Qwen family with a third developer's non-gated, Apache-2.0 instruct pair at 7B to 32B would balance the set; no such pair with released base checkpoints was verified in B3 (Llama and Gemma are gated). This is an operator item.

**Pilot model.** The pilot (section 13) runs on Olmo-3-7B-Instruct-SFT, a trajectory checkpoint outside the primary set, so that no $\Gamma$ cell of a primary model is computed before sign-off (methodologist F14).

**Strata and arms.**

- The base stratum pairs each primary model with its base.
- The reasoning toggle is Qwen3-8B with thinking on, against the same weights with thinking off. The card's mode-specific sampling recommendations are recorded but not used, because all frozen generations use temperature 1.0 and top-p 1.0 (section 5).
- The post-training trajectory is Olmo-3-1025-7B, then -Instruct-SFT, -Instruct-DPO, and -Instruct.

**Generation-shift model.** Qwen/Qwen3-8B is the generation-shift model:

- with thinking off for the budget's $\Delta\Gamma_g$ ($k_g = 10$, label-validity population);
- with thinking on, on LiveCodeBench, for the [2610.31820] reconciliation ($k_g = 4$, the paper's count).

**Hardware.** One GPU with 96 GB of memory. The GPU model and its price are not fixed in this design; they are an operator item, and the throughput assumptions of section 12 are checked against the pilot on that GPU (budget F1).

**Precision.**

- Every model runs at bf16. No model needs FP8.
- gpt-oss-20b ships MXFP4 MoE weights. It is run in its native format, recorded as a deviation from bf16.

**Alternates if a model must be swapped (risk R6):**

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

**Licence.** MIT for HumanEval, CC-BY-4.0 for MBPP (its Hugging Face card, `docs/s6/parts/bench-B4/BENCHMARKS.md`), and Apache-2.0 for EvalPlus. The LiveCodeBench licence is inconsistent ("cc" in the card, MIT in the loader), and its problems are collected from contest sites whose terms are not recorded in B4. Both are gaps, checked before any release of samples or labels; until then, LiveCodeBench problem text is not redistributed, only problem IDs (TMLR F14).

**Populations.**

- **Label-validity population (primary).** HumanEval+ and MBPP+ together, 542 problems, minus any problem whose reference solution fails either suite (section 6). Every remaining problem is valid under both suites, so all 16 cells of $\Gamma$ are defined on one problem set and stay paired across cells (methodologist F8). The primary test (section 1.6) is stated on this population. Every supervised readout of the 16-cell game is fit on this population only (methodologist F3).
- **LiveCodeBench population.** 1,055 problems, one suite family. On it, the budget has three toggles ($r$, $t$, $d$), with readouts fit on LiveCodeBench folds only. The label toggle is replaced by a label-validity analog: public example tests against the full official suite. It is reported separately, labeled as an analog, and shown in its own figure panel (section 16). LiveCodeBench readouts are fit for the six primary models only.

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
- HumanEval and MBPP have no per-problem dates and predate every model, so the label-validity population is pre-cutoff for all models (risk R7).
- The per-model counts of post-cutoff problems are computed from the pinned dataset before the pilot. They are not estimated here.

**Held-out agreement inputs, disjoint from the label suites.**

- **HumanEval and MBPP.** New inputs are generated per problem with EvalPlus's type-aware mutation generator (`TypedMutGen`), seeded by the base inputs, with a fixed seed. The LLM-based generator is not used, so no API model is needed.
  - Inputs are filtered by the problem's contract.
  - Any input equal to a base or plus input is deduplicated away.
  - Each problem is capped at 50 inputs.
  - The full EvalPlus suite stays intact as the label suite.
- **LiveCodeBench.** A fixed SHA-256 hash of each private test's input string selects 20 percent of the private tests as agreement inputs.
  - Labels use the public tests plus the remaining 80 percent. The deviation from the official suite is recorded.
  - A sensitivity analysis labels on the full official suite. In that analysis the agreement readout is not computed, because its inputs would be label inputs (methodologist F20).
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
- **Samples per problem.** $k = 10$ (section 9). The generation-shift arm on the label-validity population draws $k_g = 10$ fresh samples per problem, so that the fresh and frozen sets differ only in the generator (methodologist F15). The [2610.31820] reconciliation on LiveCodeBench draws $k_g = 4$, the paper's own count.
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
    - $p_2$, the last code token (probe). For a sample with an extraction failure, $p_2$ is the last generated token before the end-of-turn token (methodologist F21);
    - $p_3$, the last token of the elicitation turn (pre-answer state; judging-pass probe for [Campos]);
  - the V2 Yes/No logits at $p_3$.
  - **Candidate layers:** depth fractions {0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0} of the decoder stack, rounded down, plus the mean-pooled code-token state at the same layers, for the probe-position sensitivity analysis.
  - **What V1 adds:** one short greedy decode from the same prefix with the V1 turn. The prefix KV cache is reused.
  - **Storage:** bfloat16 hidden states (the native dtype; float16 can overflow on large residual-stream activations), sharded per model (budget F13).
- **Extra generation pass for the generation-shift term.** Part A could not resolve which generations [2610.31820] scored (`research/positioning/w6/R2610_31820_PROTOCOL.md`). So the extra pass runs:
  - on the generation-shift model (section 3);
  - with the R-Tuning-style adapter active in generation;
  - drawing $k_g$ fresh samples per test-fold problem, per fold, with the adapter of that fold and suite;
  - executing each fresh sample under both suites;
  - scoring each by its own confidence-token probability (reading A), and reading the probe on it by one base-weights forward pass.

  Reading B uses the frozen generations and needs no extra generation. If the operator rules that only one reading is needed, the extra pass is dropped and $\Delta\Gamma_g$ is not estimated.

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
- **Reference-solution check (HumanEval and MBPP).**
  - The canonical solution of every problem is executed under every suite before any sample is labeled.
  - A problem whose reference fails a suite is excluded from analyses that use that suite and listed with the reason. It is not silently repaired.
  - The share of excluded problems is reported per suite.
- **LiveCodeBench has no canonical solutions**, so no reference check is possible there (budget F10). The official evaluator's tests are taken as given, and this is a stated limitation of the LiveCodeBench analyses. Problems that no sample of any model passes under the public tests, and problems whose public and full-suite labels disagree for every passing sample, are listed.
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

- **Folds.** Five problem-grouped folds, assigned by SHA-256 of (fold seed, problem ID) modulo 5, so the same problems fall in the same fold for every model and readout. Every supervised readout is fit on four folds and scored on the fifth (cross-fitting). The out-of-fold scores form the analysis set.
- **Fold seeds.** Fold seed 0 is the primary partition for every readout, the LoRA readouts included. Fold seeds 1 and 2 give two more partitions, used for the refit-variance estimate (section 9): all non-LoRA readouts are refit on them for every model, and the LoRA readouts on them for the refit sub-study models (methodologist F12).
- **Inner split.** Inside each outer training set, an inner problem-grouped split assigns each of the four training folds in turn as inner validation (inner 4-fold cross-validation). Every selection uses it.
- **Label suites.** Every supervised readout is refit under each label suite.
- **No test-fold information in fitting.** Layer and position choice, regularization strength, the LoRA learning rate and step count, isotonic maps, imputation values, and retry decisions use only training-fold problems.
- **Populations.** The label-validity population and LiveCodeBench are fit separately; no readout of one is trained on the other (methodologist F3).

### 7.1 Hidden-state probe ($P$)

- **Model.** $P(c) = \sigma(w^\top \tilde{h}(c) + b)$, an L2-regularized logistic regression on a standardized feature vector $\tilde{h}$. Standardization uses training-fold means and variances.
- **Probe family** (methodologist F2, TMLR F3). Three feature sets, all from the single forward pass (section 5):
  - $P_{2}$: one layer's state at $p_2$, the last code token (the configuration of [Ribeiro], [Campos], and [2610.31820]);
  - $P_{3}$: one layer's state at $p_3$, the last token of the elicitation turn, which is the state from which the trained stated readout answers;
  - $P_{\text{multi}}$: the states of all seven candidate layers at $p_2$, concatenated, reduced by PCA to 512 dimensions fit on training folds.
- **Nested selection.** The member of the family, the layer (for $P_2$ and $P_3$, seven candidates), and $C \in \{10^{-3}, 10^{-2}, 10^{-1}, 1, 10\}$ are chosen inside each outer training set by inner 4-fold problem-grouped cross-validation, minimizing log loss. $P$ is the selected readout, so the residual is measured against the strongest linear probe in the family, chosen without test-fold information. Each member is also reported separately (section 1.3). This removes the layer-selection optimism found in Miglani et al. (2609.36783, which selects on the same out-of-fold scores) and follows the nested procedure of 2609.04582.
- **Class balance.** None. The readout is a probability on the natural base rate.

### 7.2 Zero-shot verbal confidence (two formats)

- **V1.** The integer $N$ parsed by the regular expression `Confidence:\s*(\d{1,3})`, clipped to [0, 100], divided by 100.
  - An unparsed answer is missing. It is never set to a default value (METHOD_INVENTORY 6.8 records the legacy default of 0.6).
  - In the primary analysis, missing values are imputed with the training-fold median of parsed values for that model, and flagged. Imputed samples tie with each other, which pulls the readout's AUROC toward 0.5 (TMLR F16). This is intended: an answer that cannot be parsed carries no ranking information, and the cost is charged to the zero-shot readout. The share of pairs tied by imputation is reported.
  - A sensitivity analysis drops them.
  - The parse rate is reported.
- **V2.** $P(\text{Yes}) / (P(\text{Yes}) + P(\text{No}))$, read from the logits at $p_3$ as in section 5. It is never missing.
- **Role.** V1 is the zero-shot readout in the primary chain. V2 is the zero-shot readout in the sensitivity chain and the reconciliation readout for [Campos] and [Ribeiro].

### 7.3 Isotonic-recalibrated verbal confidence

- **Fit.** For a stated readout $S$, an isotonic regression of $y$ on $S$ is fit on training-fold samples and applied out of fold.
  - For the zero-shot readouts, the training-fold scores need no fitting, so the map is fit on them directly.
  - For the trained readout $S^T$, the training-fold scores must come from adapters that did not see those samples. The map is fit on the inner-cross-fitted scores: for each inner split, the adapter trained with the selected recipe on three training folds scores the fourth. These adapters exist anyway for recipe selection (section 7.4). The map is then applied to the test-fold scores of the adapter fit on all four training folds (methodologist F4). The small mismatch between three-fold and four-fold adapters is stated, and on the refit sub-study models the map is also fit on the four-fold adapter's in-sample scores as a sensitivity analysis.
- **Ranking ties.** For discrimination metrics, ties of the isotonic map are broken by the pre-map score (section 1.2).
- **Boundaries.** `out_of_bounds = clip`. A single-class training set falls back to the training base rate (METHOD_INVENTORY 6.5).

### 7.4 Trained stated-confidence readout ($t = 1$)

- **Adapter.**
  - LoRA with rank 16, alpha 32, dropout 0.05, no bias, on all attention and MLP projections.
  - It is active only on tokens of the elicitation turn: the LoRA output is multiplied by a 0/1 position mask that is 1 on the V2 elicitation-turn tokens and the answer position.
  - The generation prompt and the frozen code are therefore encoded by the base weights, and their KV cache is identical to the base model's.
- **Readout.** $S^T(c) = P_{\theta + \Delta}(\text{Yes}) / (P_{\theta+\Delta}(\text{Yes}) + P_{\theta+\Delta}(\text{No}))$ at the answer position, the V2 format.
- **Loss.** Binary cross-entropy between $S^T$ and the label (a proper scoring rule, as for the probe).
- **Training.**
  - Data: every training-fold sample of the population being fit, unweighted.
  - Optimizer: AdamW, cosine schedule, 5 percent warmup, effective batch 64 sequences, up to 2 epochs.
  - **Recipe selection** (methodologist F6, TMLR F8): learning rate in $\{5 \times 10^{-5}, 10^{-4}, 3 \times 10^{-4}\}$ and the step count, both chosen by inner cross-validation log loss on the label-validity population under the EvalPlus suite, evaluated every 20 steps. With about 4,336 training sequences per outer fold, one epoch is about 68 steps, so the R0 check every 200 steps would never have fired. The selected recipe is reused for the original suite, for LiveCodeBench, and for the model's base and trajectory checkpoints. For Qwen3-8B with thinking on, the recipe of the same weights with thinking off is reused.
- **Runs.** One adapter per (model, outer fold, label suite) with the selected recipe, plus the inner-split adapters of recipe selection.
- **Supervision match.** The probe and the trained readout see the same samples, labels, folds, and loss, and both have their hyperparameters selected by inner cross-validation. They still differ in capacity: the probe is a linear map on frozen states, and the adapter is a low-rank update of the network in the elicitation turn that reads the code through attention. Section 7.11 measures how much that difference matters, and section 1.8 states it in every outcome sentence. This is the design's version of the comparison in [2610.31820] (a trained readout against a same-label probe on code) and of CREDO 2609.34857 (a trained stated readout on code, without a probe).

### 7.5 The [2610.31820]-style trained readout

- **Adapter.** Same LoRA settings and selected recipe as 7.4, but active on all positions, as in R-Tuning, which fine-tunes the policy ([2610.31820] Sec 4.1). It is fit on the label-validity population for $\Delta\Gamma_g$ and on LiveCodeBench for the reconciliation.
- **Training.** Supervised fine-tuning on training-fold frozen samples. Each training sequence is the generation prompt, the frozen code, and the suffix "I am sure" if the sample passes the active suite or "I am unsure" if it fails. The loss is next-token cross-entropy on the assistant tokens: the code and the suffix.
- **Readout.** $P(\text{sure}) / (P(\text{sure}) + P(\text{unsure}))$ at the token after "I am".
- **Scoring.**
  - Reading A ($g = 1$): generate $k_g$ fresh samples per test-fold problem with the adapter active ($k_g = 10$ on the label-validity population, 4 on LiveCodeBench), execute them, and score each from its own suffix position. The probe is read on the same fresh samples.
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

### 7.11 Capacity controls for the trained readout

The trained readout has more capacity than a linear probe (methodologist F2, TMLR F3). Two controls, on the label-validity population under the EvalPlus suite, fold seed 0:

- **Capacity ladder.** $S^T$ at LoRA ranks 1 and 4 (alpha twice the rank), beside the primary rank 16, on Qwen2.5-Coder-7B-Instruct and Qwen3-14B. $R$ is reported at each rank. If $R$ moves by more than $\delta$ across ranks, the outcome sentence says that the residual depends on the readout's capacity.
- **LoRA plus linear head.** The same masked adapter, but the score is a logistic head on the $p_3$ state of the adapted network, trained jointly, instead of the Yes/No token probabilities. On the same two models. The difference between this control and $S^T$ isolates the cost of reading the answer through the verbal tokens from the cost of the adapter's capacity. It is reported as a contrast, not as a stated readout.

## 8. Metrics

**Discrimination.**

- **Pooled AUROC.** Over all samples of the population (Mann-Whitney, ties counted as one half).
- **Pooled AUPRC.** For the positive class "pass", with the base rate printed beside it. The "fail" class AUPRC is also reported, because routing targets failures.
- **Pair-weighted within-problem AUROC.**

  $$W = \frac{\sum_i \sum_{a \in \mathcal{P}_i} \sum_{b \in \mathcal{F}_i} \big(\mathbb{1}[s_a > s_b] + \tfrac{1}{2}\mathbb{1}[s_a = s_b]\big)}{\sum_i |\mathcal{P}_i|\,|\mathcal{F}_i|},$$

  where $\mathcal{P}_i$ and $\mathcal{F}_i$ are the passing and failing samples of problem $i$. All-pass and all-fail problems have $|\mathcal{P}_i|\,|\mathcal{F}_i| = 0$ and drop out. Their number, and the number of mixed problems, are reported for every model, suite, and stratum.
  - $W$ weights problems by their number of pass-fail pairs. It is the probability that a random passing sample outranks a random failing sample of the same problem, with pairs drawn uniformly.
  - **Secondary:** the problem-averaged version $W_{\text{avg}}$ (each mixed problem weighted equally), the definition used by Miglani et al. (2609.36783).
  - **Effect of the label switch.** Switching from the original to the EvalPlus suite changes which problems are mixed. $W$ is computed on each suite's own mixed set, as its definition requires. Beside it, $W$ on the problems mixed under both suites is reported, with the counts of problems that enter or leave the mixed set, so that $\phi_l$ can be split into relabeling and population change (TMLR F12).
  - **Diagnostics for $d$.** Pooled AUROC restricted to mixed problems, and the mean over folds of the per-fold pooled AUROC, are reported beside each pooled value (methodologist F9).

**Brier score and its decomposition.**

- $\mathrm{BS} = \frac{1}{n}\sum (s - y)^2$, with the Murphy decomposition into reliability, resolution, and uncertainty, estimated with 15 equal-mass bins.
- The problem-demeaned Brier analog for $d = 1$ uses $s - \bar{s}_i$ and $y - \bar{y}_i$ within mixed problems. It is reported as a secondary within-problem calibration measure.

**Calibration estimator set** (sensitivity analysis, compare 2605.27752 App G):

- debiased equal-mass binned ECE (15 bins, with the debiasing correction of Kumar, Liang, and Ma 2019);
- the binning-free smooth ECE (Blasiok and Nakkiran 2023, with its default kernel bandwidth rule);
- KS calibration error (Gupta et al. 2021, binning-free).

Equal-width 15-bin ECE is computed only for the [2610.31820] reconciliation. Equal-width 10-bin ECE is computed only for comparison with MARGIN. The bibliography entries for the three estimator papers must be fetched before the manuscript cites them (section 14, risk R4).

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
- **Cost.** Per-problem pass-fail pair counts and per-problem rank sums are precomputed once per readout, so each resample is a weighted sum over problems.

**What the bootstrap conditions on.** Fitted readouts are not refit inside resamples, so the bootstrap conditions on the out-of-fold scores of fold seed 0. Refit variance is added explicitly (methodologist F12, risk R9):

- **Non-LoRA readouts.** Refit under fold seeds 1 and 2 for every model.
- **LoRA readouts.** A refit sub-study on two primary models (Qwen2.5-Coder-7B-Instruct and Qwen3-14B): $S^T$ and its isotonic map are refit under fold seeds 1 and 2 (new partition and new adapter initialization), under the EvalPlus suite.
- **Combination rule, fixed now.** Let $s^2_{\text{refit}}$ be the between-seed variance of $\bar{R}$, computed from the three seeds with the LoRA readouts of the non-sub-study models held at seed 0 and their share of the variance scaled up by the ratio of the number of primary models to the number of sub-study models. The decision interval is the percentile interval widened symmetrically about its center to half-width $\sqrt{h^2 + (z\,s_{\text{refit}})^2}$, where $h$ is the bootstrap half-width and $z = 1.645$. The unwidened interval is reported beside it. Point estimates stay at seed 0.

**Shapley intervals.** In each resample, all 16 cells of $\Gamma$ are computed and the four $\phi_v$ are taken. The interval of each term is the percentile interval of its resampled values. The sequential decompositions and the interaction indices get intervals the same way.

**Multiplicity.**

- **Primary decisions.** One family of three mutually exclusive decisions on $\bar{R}$; at most one can be reached, so no adjustment.
- **Secondary per-model residual decisions.** Holm adjustment across the six primary models, for each decision.
- **Shapley terms (descriptive, H3).** Model-pooled terms carry simultaneous Bonferroni intervals (98.75 percent, four terms), with 95 percent intervals beside them. Per-model and per-stratum terms are at 95 percent, labeled unadjusted.
- **$R_{\text{pool}}$.** Secondary, at its own margin, unadjusted, labeled as such.
- **Reconciliation entries.** Each is a separate pre-stated check; no adjustment is applied, and the table says so.

**Scope of the interval.** The primary interval is conditional on the six named models. Models are not a sampled population, and between-model spread is reported per model and per family.

**Power.** The wave 5 simulation was copied (not moved; the scratch originals stay in place) to `docs/s6/power/w5-baseline/`. Its adaptation to the three decisions and the Shapley terms is `docs/s6/power/power_sim.py` (B9, results in `docs/s6/power/POWER.md` and `power_sim.json`). A wrapper, `docs/s6/power/power_shared_shock.py`, reruns the decision at $M = 6$ with gap shocks shared across models (results in `docs/s6/power/SHARED_SHOCK.md` and `power_shared_shock.json`).

**Planning assumptions** (labeled, to be replaced by pilot estimates): probe within-problem AUROC 0.72 nominal (0.714 realized in the simulation); zero-shot stated within-problem AUROC 0.60; between-problem gap heterogeneity; per-problem pass rates from Beta(0.6, 0.5). The simulation fits no readouts and does not refit per suite, and the stated score is pre-binned, so its interval widths are lower bounds (methodologist F13). The pass-rate distribution may be optimistic for strong models on HumanEval and MBPP (TMLR F7); the pilot measures the mixed-problem count, and K2 acts on it.

**Choice: $k = 10$ samples per problem, $n = 542$ problems** (the whole label-validity population, before reference exclusions). LiveCodeBench release_v6 adds 1,055 problems for its own 3-toggle budget.

**Results at the chosen setting** (100 replicates per cell, so each probability carries Monte Carlo error up to about 0.05):

| Setting | P(D1 equivalence \| $R = 0$) | P(D2 probe ahead \| $R = 0.06$) | Source |
|---|---|---|---|
| $M = 6$, independent shocks | 1.00 | 1.00 | `power_shared_shock.json`, rho 0 |
| $M = 6$, shocks shared across models (rho 0.5; rho 1) | 1.00; 1.00 | 1.00; 1.00 | same file |
| $M = 1$ (per model), independent shocks | 0.66 | 0.83 | same file |
| $M = 9$ (B9 grid) | 1.00 | 1.00 | `power_sim.json` |

- **Interval width.** Mean 90 percent half-width of $\bar{R}$ at $M = 6$ is about 0.008, whatever rho. The problem-clustered bootstrap resamples the same problems for all models, so shared problem-level variance is already inside the interval.
- **Margin grid** ($M = 6$, $R = 0$, P(D1)): 0.29 to 0.44 at $\delta = 0.01$; 0.80 to 0.92 at 0.015; 0.96 to 1.00 at 0.02; 1.00 at 0.03 and 0.05. The design could decide at 0.02, so the margin is justified on substantive grounds (section 1.6).
- **Boundary.** At true $R = \delta$, P(inconclusive) is about 0.9 by construction, and that outcome is reportable.
- **Third decision.** P(D3) is 0.00 in every simulated cell, as expected with true $R \ge 0$.
- **Per model.** Per-model equivalence reaches 0.80 only near $n = 900$ (B9). Per-model decisions are secondary and may be underpowered for equivalence, as stated in advance.
- **Mixed problems.** About 361 of 542 per model at $k = 10$ under the planning assumptions (B9), which sets the effective sample of $W$.
- **Shapley half-widths** (95 percent, $M = 9$, $n = 542$, B9): $G_0$ 0.0051, difficulty term 0.0063, $R$ 0.0073. At $M = 6$ they are expected to be somewhat wider; the pilot-based rerun reports them at $M = 6$.

**Pilot rerun.** After the pilot, the simulation is rerun with the pilot's measured mixed count and within-problem AUROC of the zero-shot readout (no primary-model $\Gamma$ cell is used). Only $k$ may change as a result (section 13).

## 10. Secondary arms

- **Base vs instruct.** Every family with a base and instruct pair enters as a stratum, on the label-validity population only. The full budget (all 16 cells) is computed per model, and the stratum contrast is the difference in each Shapley term between instruct and base, with a paired interval (same problems).
  - Base models need a completion-style generation prompt. The elicitation turns for base models use a plain-text dialogue frame, frozen and hashed like the chat prompts.
  - The zero-shot verbal readouts of base models are expected to parse less often. Parse rates are reported, and the V2 chain is primary for base models if the V1 parse rate falls below 80 percent. That threshold is fixed now.
- **Same-weights reasoning toggle.** The reasoning-toggle model (section 3) is generated twice on the same problems, thinking off and thinking on. Each condition has its own frozen generations, labels, and full budget. The stratum contrast is per term.
- **Intermediate post-training checkpoints.** If section 3 admits a family with released SFT, preference-tuned, and final checkpoints, the budget is computed at each stage, as a descriptive trajectory.
- **Offline routing replay.** It measures the decision cost of each budget term. Two decision problems are replayed on the frozen generations and their labels:
  1. **Best-of-$k$ selection per problem** (within-problem use). The sample with the highest confidence is selected. The value is the selected pass rate. The comparators are:
     - random selection (the mean pass rate);
     - oracle selection (pass@$k$, 1 if any sample passes);
     - regret, defined as oracle minus selected.
  2. **Global verification triage** (pooled use; a separate figure panel from best-of-$k$, section 16). Samples are sorted by confidence, and the lowest-confidence fraction $b \in \{0.05, 0.1, 0.2, 0.3, 0.5\}$ is sent to execution. The value is the share of all failing samples that the budget catches. The comparators are:
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
| 2.5 | Hardware and software | One 96 GB GPU (model fixed at sign-off); pinned versions of CUDA, PyTorch, vLLM, transformers, PEFT, scikit-learn, and EvalPlus, recorded in the run manifest | Legacy recorded only partly |
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
| 4.9 | Extra generations | None for the primary analysis: label, readouts, and agreement all use the same $k$ samples. The single extra pass is the generation-shift arm ($k_g = 10$; 4 for the [2610.31820] reconciliation) | Fixes the legacy "different generations" problem (METHOD_INVENTORY headline 3) |
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
| 6.5 | Post-hoc calibration | Isotonic only, cross-fitted on problem folds, with inner cross-fitting for the trained readout and ranking ties broken by the pre-map score (7.3); Platt as a sensitivity analysis | Legacy used unshuffled-by-problem KFold |
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
| 8.6 | Intervals for recalibrated scores | Conditional on cross-fitted maps; refit variance added by the fixed rule of section 9 | |
| 9.1 to 9.15 | SFT and DPO pipeline | Replaced by the trained readouts of 7.4 and 7.5; no preference training; no tier sentences | The legacy SFT data overlapped the evaluation set |
| 10 | Random seeds | Generation seeded per sample; folds by hash of (fold seed, problem ID), seed 0 primary and seeds 1 and 2 for refit variance; bootstrap and model fitting seeded and recorded | Legacy generation was unseeded |
| 11 | `src/v4_dprc` | Out of scope (operator decision) | |

## 12. Compute and cost budget

All throughput values are planning assumptions for one 96 GB GPU at bf16. They are not measurements, they have no cited source, and the GPU model is not yet fixed (section 3). The prefill rates imply roughly 230 to 250 TFLOP/s sustained (budget F1), which is plausible only on a current data-center GPU; the pilot measures them on the actual GPU. Prices are not given in this design, so the budget is in GPU-hours and CPU-hours only. Problem counts and model conditions come from sections 3 and 4; $k = 10$ (section 9).

R1 recomputes every row after the Part B critics. The changes from R0 are: supervised readouts are fit per population (section 7); the trained readout gets a learning-rate selection and inner adapters for its isotonic map; base and trajectory checkpoints run on the label-validity population only; LiveCodeBench readouts are fit on three folds with the fourth calibrating; the generation-shift arm uses $k_g = 10$ and reads the probe on fresh samples; capacity controls and a second refit model are added; and the pilot covers a 32B model and the thinking-on length.

### 12.1 Assumptions

| Quantity | Assumed value |
|---|---|
| Problems | label-validity 542; LiveCodeBench 1,055 |
| Samples, primary instruct model | (542 + 1,055) x 10 = 15,970 |
| Samples, base or trajectory checkpoint | 542 x 10 = 5,420 |
| Mean generated tokens, non-reasoning instruct | 332 per sample (200 on HumanEval and MBPP, 400 on LiveCodeBench; weighted by problem counts) |
| Mean generated tokens, base models | 400 (completion prompts with stop strings) |
| Mean generated tokens, thinking on | 6,000 (cap 16,384); unsourced, measured in the pilot; each +1,000 tokens adds about 7 GPU-hours (12.3) |
| Mean tokens per teacher-forced sequence | 900 non-reasoning (prompt, code, elicitation); 6,900 thinking on; 7,000 for the LiveCodeBench thinking-on reconciliation |
| vLLM decode throughput, batched, prefix caching on | 8B 4,000 tok/s; 14B 2,500; 32B dense 1,000; 30B-A3B MoE 3,000; gpt-oss-20b 3,000 |
| Teacher-forced prefill with hidden-state capture | 8B 15,000 tok/s; 14B 8,000; 32B 3,500; MoE 10,000 |
| LoRA elicitation-only training (no-grad prefix, gradient only on elicitation tokens) | 0.77 of prefill throughput: 8B 11,500 tok/s; 14B 6,150; 32B 2,700 |
| LoRA full-sequence training (R-Tuning-style) | 8B 5,000 tok/s |
| Adapter-active generation in vLLM | 0.7 of base decode throughput (8B 2,800 tok/s) |
| LoRA scoring and validation overhead | 20 percent on elicitation-only training (R0: 10 percent; budget F3); 10 percent on full-sequence training |

**Training tokens per outer fold** (one epoch, 900 tokens per sequence):

| Item | Arithmetic | Tokens |
|---|---|---|
| Final adapter, label-validity, one suite | 0.8 x 5,420 x 900 | 3.90M |
| Inner adapter (three training folds), label-validity, one suite | 0.6 x 5,420 x 900 | 2.93M |
| LiveCodeBench adapter (three training folds), one suite | 0.6 x 10,550 x 900 | 5.70M |
| Learning-rate selection (three rates, EvalPlus suite, inner adapters) | 3 x 2.93M | 8.78M |

Per primary instruct model, per outer fold: selection 8.78M (its selected-rate adapter is the EvalPlus inner adapter) + original-suite inner adapter 2.93M + two final adapters 7.80M + two LiveCodeBench adapters 11.39M = 30.9M; over 5 folds, 154.5M.
Per base or trajectory checkpoint (recipe reused): two final adapters 7.80M + two inner adapters 5.85M = 13.66M per fold; 68.3M over 5 folds.

### 12.2 Per-stage GPU-hours

| Stage | Arithmetic | Conditions | GPU-hours |
|---|---|---|---|
| Generation, instruct 7-8B | 15,970 x 332 = 5.30M / 4,000 = 0.37 h | 3 | 1.10 |
| Generation, instruct 14B | 5.30M / 2,500 | 1 | 0.59 |
| Generation, instruct 32B | 5.30M / 1,000 = 1.47 h | 2 | 2.94 |
| Generation, Olmo SFT and DPO (label-validity only) | 5,420 x 200 = 1.08M / 4,000 = 0.075 h | 2 | 0.15 |
| Generation, base (label-validity only) | 5,420 x 400 = 2.17M: 7-8B 0.15 h; 14B 0.24 h; 32B 0.60 h | 3 + 1 + 2 | 1.89 |
| Generation, Qwen3-8B thinking on | 15,970 x 6,000 = 95.8M / 4,000 | 1 | 6.65 |
| Generation, [Campos] models (LiveCodeBench only, 10,550 samples) | Coder-30B-A3B: 10,550 x 400 = 4.22M / 3,000 = 0.39 h; gpt-oss-20b at 1,500 tok: 15.8M / 3,000 = 1.47 h | 2 | 1.86 |
| Forward pass, instruct | 15,970 x 900 = 14.4M: 8B 0.27 h; 14B 0.50 h; 32B 1.14 h | 3 + 1 + 2 | 3.58 |
| Forward pass, base and Olmo stages | 5,420 x 900 = 4.88M: 7-8B 0.09 h; 14B 0.17 h; 32B 0.39 h | 5 + 1 + 2 | 1.40 |
| Forward pass, thinking on | 15,970 x 6,900 = 110M / 15,000 | 1 | 2.04 |
| Forward pass, [Campos] models | Coder: 10,550 x 1,000 / 10,000 = 0.29 h; gpt-oss at 2,500 tok: 0.73 h | 2 | 1.02 |
| V1 greedy decode (8 tokens per sample) | allowance; R0's 1.0 h assumed a cached-prefix engine, and without one it could reach about 10 h (budget F5) | 17 | 5.0 |
| Trained stated readout, instruct 7-8B | 154.5M / 11,500 = 3.73 h x 1.2 | 3 | 13.4 |
| Trained stated readout, instruct 14B | 154.5M / 6,150 = 6.98 h x 1.2 | 1 | 8.4 |
| Trained stated readout, instruct 32B | 154.5M / 2,700 = 15.9 h x 1.2 | 2 | 38.1 |
| Trained stated readout, base and Olmo stages 7-8B | 68.3M / 11,500 = 1.65 h x 1.2 | 5 | 9.9 |
| Trained stated readout, base 14B | 68.3M / 6,150 = 3.08 h x 1.2 | 1 | 3.7 |
| Trained stated readout, base 32B | 68.3M / 2,700 = 7.03 h x 1.2 | 2 | 16.9 |
| Trained stated readout, thinking on (label-validity, recipe reused) | per fold: final 2 x 0.8 x 5,420 x 6,900 = 59.8M + inner 2 x 0.6 x 5,420 x 6,900 = 44.9M; 5 folds = 523.6M / 11,500 = 12.6 h x 1.2 | 1 | 15.2 |
| Capacity controls (7.11) | per model: ranks 1 and 4 and the linear-head control, 3 x 5 x 3.90M = 58.5M; Qwen2.5-Coder-7B-I 58.5M / 11,500 x 1.2 = 1.70 h; Qwen3-14B 58.5M / 6,150 x 1.2 = 3.17 h | 2 | 4.9 |
| LoRA refit sub-study (9) | per model, 2 fold seeds x (final 19.5M + inner 14.6M) = 68.3M; 7B 1.98 h; 14B 3.70 h | 2 | 5.7 |
| Generation shift, Qwen3-8B thinking off, label-validity | R-Tuning training 2 suites x 5 x 3.90M = 39.0M / 5,000 = 2.17 h x 1.1 = 2.38 h; fresh generation 542 x 10 x 200 x 2 suites = 2.17M / 2,800 = 0.22 h; two forward passes on fresh samples (probe and readout) 2 x 10,840 x 900 = 19.5M / 15,000 = 0.36 h; reading B 2 x 5,420 x 900 = 9.76M / 15,000 = 0.18 h | 1 | 3.1 |
| Generation shift, thinking on, LiveCodeBench ([2610.31820] reconciliation) | training 5 x 0.8 x 10,550 x 7,000 = 295.4M / 5,000 = 16.4 h x 1.1 = 18.1 h; fresh 1,055 x 4 x 6,000 = 25.3M / 2,800 = 2.51 h; two forward passes on fresh 2 x 4,220 x 7,000 = 59.1M / 15,000 = 1.09 h; reading B 10,550 x 7,000 = 73.9M / 15,000 = 1.37 h (missing in R0, budget F3) | 1 | 23.1 |
| Pilot (section 13) | Olmo-3-7B-Instruct-SFT end to end with debugging, 4.0 h; 32B throughput probe (Qwen2.5-Coder-32B-Instruct: 50 problems x 10 samples, forward pass, 200 LoRA steps; outputs timed, not analyzed), 1.5 h; thinking-on length probe (Qwen3-8B, 100 problems x 2 samples), 0.5 h | 1 | 6.0 |
| **Total** | | | **176.6** |
| With 25 percent contingency | | | **220.8** |

**Contingency.** 25 percent, up from R0's 20 percent, because three of the largest rows (thinking on, 32B LoRA, LiveCodeBench reconciliation) rest on unmeasured token lengths and throughputs, and failed or restarted jobs are not otherwise budgeted (budget F9). The budget critic's independent correction of R0 was about 185 h before contingency (`docs/s6/parts/critic-B-budget/FINDINGS.md`); R1's 176.6 h differs because R1 also restructures the fits.

### 12.3 Sensitivity of the total

- **Thinking-on length.** Each +1,000 mean thinking tokens adds about 7.0 h: generation 1.1, forward 0.3, thinking-on trained readout 2.2, reconciliation training 2.6, fresh generation and scoring 0.8.
- **$k = 8$.** Saves about 20 percent of generation, forward, and trained-readout hours: about 0.2 x (15.2 + 8.0 + 105.6) = 25.8 h. B9 shows $k = 8$, $n = 542$ also qualifies for both primary decisions at $M = 9$. $k = 10$ is kept for margin on the mixed-problem count, which is the highest-likelihood risk (R2); $k = 8$ is the second-to-last cut under K7.

### 12.4 CPU and storage

All CPU figures are planning assumptions, measured in the pilot (budget F4, F11).

- **Execution.** About 191,000 samples (instruct 95,820; thinking on 15,970; base 32,520; Olmo stages 10,840; [Campos] models 21,100; fresh generation-shift samples 15,060), each under 1.5 suites on average. At 2 CPU-seconds per sample per suite and a 30 percent cache hit rate: 191,000 x 1.5 x 2 x 0.7 = 401,000 CPU-s, about 112 CPU-hours.
- **Agreement inputs.** Up to 50 inputs per HumanEval or MBPP problem and the 20 percent LiveCodeBench split: about 100 CPU-hours.
- **Probe fits.** Per (condition, population, suite, fold seed, outer fold): 15 feature sets x 5 values of $C$ x 4 inner folds = 300 fits plus one final fit; with prompt-only probes and the code-text classifier, about 270,000 logistic fits in total, at about 2 CPU-seconds each: about 150 CPU-hours.
- **Bootstrap.** Precomputed per-problem sums make each resample a weighted sum; about 10 CPU-hours for all metrics and cells.
- **Total CPU.** About 370 CPU-hours, about 12 hours of wall-clock on 32 cores.
- **Hidden-state storage.** 28 vectors per sample (7 layers at 3 positions, plus 7 mean-pooled), bfloat16. With the actual hidden sizes, the budget critic computes 62.4 GB for the R0 conditions; the fresh generation-shift samples add about 3.4 GB. About 66 GB in total, sharded per model.
- **Model weights.** About 544 GB of bf16 weights across all repositories (budget F13). The GPU host needs about 1 TB of disk, or downloads models in sequence.

### 12.5 Cost-minimizing choices

- **One pass per sample.** Generation once. Then one teacher-forced pass for log-probabilities, hidden states at all candidate layers and positions, and the V2 readout. V1 adds only an 8-token greedy decode from the cached prefix.
- **Samples reused across methods.** All readouts, baselines, labels, agreement, clustering, the routing replay, and both reconciliation entries on the same model read the same frozen generations. The only exception is the generation-shift arm, which is by definition fresh.
- **Execution cache keyed by normalized code hash** (section 6). Shared across samples, models, suites, and the agreement runs.
- **vLLM prefix caching.** The $k$ samples of a problem share the prompt prefix. The V1 decode shares the prefix of the teacher-forced pass.
- **Elicitation-only LoRA trained on a no-grad prefix.** Gradients flow only through elicitation tokens, which keeps the trained readout near prefill cost.
- **Recipe selected once per model,** on one suite, and reused for the other suite, LiveCodeBench, and the model's base and trajectory checkpoints.
- **Base and trajectory checkpoints on the label-validity population only;** LiveCodeBench adapters only for the six primary models.
- **Resumable per-model shards.** Every stage writes per-model, per-benchmark shards with content hashes. A restart skips completed shards. The run manifest lists every shard hash.
- **A pilot before the full matrix** that measures the three most uncertain rows (section 13).
- **No API-model arms.** No claim in section 1 requires one. EvalPlus's LLM-based input generator is not used (section 4).

## 13. Kill and pivot criteria

**The pilot.** It runs before sign-off is used for anything else, and it is fixed now:

- **End to end** on Olmo-3-7B-Instruct-SFT, a checkpoint outside the primary set, on the label-validity population with $k = 10$: generation, labels, the forward pass, all readouts including the trained readout with recipe selection, and the full analysis code. It yields parse rates, mixed counts, extraction-failure rates, reference exclusions, tie rates, timing, and the unit test of risk R1.
- **Throughput probes** on Qwen2.5-Coder-32B-Instruct (generation, forward pass, and 200 LoRA steps) and on Qwen3-8B with thinking on (mean thinking length). Their outputs are timed and not analyzed.
- **What the pilot does not do.** It computes no $\Gamma$ cell of a primary model (methodologist F14). Its own $\Gamma$ cells exist, because it runs the analysis code, but they are a different model's, are reported in the paper as the pilot, and are not used to choose anything but $k$.

These criteria are fixed before the pilot runs. The kill criteria use IDs K1 to K7; the risks of section 14 use R1 to R16 (budget F7).

| ID | Trigger | Action |
|---|---|---|
| K1 | Reference-solution failures exclude more than 5 percent of the problems of a HumanEval or MBPP suite | Stop. Fix the harness or the suite version. Do not proceed until the excluded share is at most 5 percent or the operator accepts the list |
| K2 | Fewer mixed problems per model than section 9 assumes, by more than 25 percent, in the pilot | Raise $k$ (to at most 16) within the compute cap of K7, after rerunning the power simulation with the pilot's mixed count. The primary population, $\delta$, and the decisions do not change (methodologist F14). Adding LiveCodeBench to the primary population is not available after sign-off |
| K3 | The V1 parse rate is below 80 percent for an instruct model | Switch that model's primary chain to V2 (fixed rule, section 10). If V2 is degenerate (one value for every sample) on more than half the primary models, the zero-shot stated readout is uninformative. $G_0$ is then reported as such, and the contribution reverts to the budget of the trained readout against the probe |
| K4 | The trained readout ($t = 1$) fails to train: inner-validation log loss no better than the training base rate for every learning rate of the selection grid, on a majority of outer folds | Retry the selection once with 2 epochs, fixed now. The decision uses inner-validation loss only, never test-fold loss, and the probe gets the matching retry of its own selection if it also fails (methodologist F5). If the trained readout still fails, report it. The supervision term is then bounded by the isotonic readout, and the primary test is reported with that limitation |
| K5 | A reconciliation check is "not reproduced" or "undetermined" (section 2) | Report it (section 2.1). It does not stop the study, because the budget is defined on this design's generations. If [2610.31820]'s tie fails under both readings, the paper reports that the published tie is not reproduced on public checkpoints, and the generation-shift contrast is reported without the claim that it explains the published tie. If [Campos]'s prompt-only pattern fails, the difficulty term is reported as model-specific |
| K6 | Concurrent work posted before submission occupies the joint attribution (a full text attributing the probe-versus-stated gap to two or more of the four terms on shared generations) | Re-run the Part A occupancy check before the manuscript is drafted. If it is occupied, the contribution becomes the reproduction and reconciliation on code, under the TMLR Reproducibility certification criteria (`docs/s2/venue/TMLR_RUBRIC.md` section 3). This is the pivot |
| K7 | The compute estimate after the pilot exceeds the budget with contingency (220.8 GPU-hours, section 12) | Cut, in this order, until the estimate fits: (1) the Olmo SFT and DPO stages, about 4.5 h; (2) LiveCodeBench trained readouts for the two 32B instruct models, about 14.1 h; (3) the base 32B pair, about 18.9 h; (4) the thinking-on stratum's original-suite trained readouts, about 7.6 h ($\phi_l$ not estimated for that stratum); (5) recipe selection for the 32B models, replaced by their family's smaller instruct model's recipe, about 10.8 h; (6) $k = 8$ for every condition, about 25.8 h. Together about 81.7 h. The primary set, the primary population, and the reconciliation models are never cut. Beyond these, the operator decides (budget F7) |

## 14. Risk register

| ID | Risk | Likelihood | Effect | Mitigation |
|---|---|---|---|---|
| R1 | The LoRA readout active only in the elicitation turn needs a custom position mask; a bug would leak code-token adaptation | medium | the supervision term is wrong | Unit test: with the mask, the KV cache of the prompt and code is bit-identical to the base model's; checked in the pilot |
| R2 | Too few mixed problems on HumanEval and MBPP for strong models (most problems all-pass) | high for 32B-class instruct models | $W$ rests on few problems | Report mixed counts; K2; primary pooling over models; $k = 10$ rather than 8 |
| R3 | EvalPlus flips are rare for some models, so $\phi_l$ is near zero by construction | medium | label term is uninformative for those models | Report the flip table; the term is still estimated, with its interval |
| R4 | Estimator citations (debiased ECE, smooth ECE, KS) are not yet fetched records | certain | bibliography rule | Fetch the records before drafting |
| R5 | The [2610.31820] protocol is unrecoverable (unreleased checkpoints, unstated generations) | certain | reproduction is approximate | Both readings run; deviations listed; claims about the paper limited to its text |
| R6 | Gated model cards or licences restrict use | medium | model swap | Section 3 lists alternatives |
| R7 | Test-time contamination of HumanEval and MBPP for all models | certain | the label-validity population is all pre-cutoff | The contamination stratum uses LiveCodeBench windows. The primary test is stated for the pre-cutoff population, and the stratum result is reported separately |
| R8 | Sandbox escapes or resource exhaustion from generated code | low | host damage | Container limits, no network, unprivileged user, tmpfs |
| R9 | Refit variance of LoRA readouts is larger than the bootstrap variance | medium | the decisions are anticonservative | Refit sub-study on two models; its variance widens the decision interval by a fixed rule (section 9) |
| R10 | Non-commuting toggles make Shapley values hard to read | certain | interpretation | Interaction indices in the main text; both sequential orders; diagnostic splits of $\phi_d$ and $\phi_l$ |
| R11 | A failed reconciliation is read as a flaw of this design | medium | reviewer doubt | Deviations stated before running; failure is reported as a finding (K5) |
| R12 | Storage (66 GB of hidden states, about 544 GB of weights) exceeds the GPU host's disk | low | pipeline stall | Per-model shards; sequential model downloads; size in section 12 |
| R13 | The trained readout's capacity, not its stated form, drives equivalence | high | an equivalence result is over-read | Probe family (7.1), capacity ladder and linear-head control (7.11), and the capacity caveat in every outcome sentence (1.8) |
| R14 | Four of six primary models come from one developer | certain | limited generality | Per-family results; outcome sentences name the set; operator item on a third family (section 3) |
| R15 | Double-blind and supplement limits: the TMLR supplement is capped at 100 MB, below the size of the hidden states | certain | release plan | Section 14.1 |
| R16 | LiveCodeBench has no canonical solutions, so its tests cannot be checked against a reference | certain | LiveCodeBench labels are taken as given | Stated limitation; listed problem anomalies (section 6) |

### 14.1 Release, anonymization, and disclosure

- **Submission supplement (anonymized, under 100 MB).** Pipeline code, frozen prompt files with hashes, the run manifest, problem IDs, labels, out-of-fold scores of every readout, and the `analysis/` JSON from which every number and figure is generated. No hidden states and no model weights.
- **Hidden states and adapters.** Released after acceptance from a non-anonymous host; at submission, their hashes are in the manifest.
- **Anonymization.** No author names, institution, repository URL, or host identifiers in the PDF, supplement, or linked artifacts (`docs/s2/venue/TMLR_RUBRIC.md`).
- **LLM-use footnote.** TMLR requires disclosure of LLM-tool use in a first-page footnote. Its wording is an open operator item (`docs/CONTEXT.md`).
- **LiveCodeBench text.** Problem statements are not redistributed until the licence gap of section 4 is closed; only IDs are.

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
| hidden-state probe | $P$ | the logistic-regression probe selected by inner cross-validation from the probe family | "internal confidence" |
| probe family | $P_2, P_3, P_{\text{multi}}$ | one layer at the last code token; one layer at the end of the elicitation turn; all seven layers at the last code token | |
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
| pooled residual | $R_{\text{pool}}$ | $\Gamma(1,1,0,1)$ | |
| decision | D1, D2, D3 | equivalence; probe ahead by more than $\delta$; stated readout ahead by more than $\delta$ | "significant" (unqualified) |
| budget term | $\phi_v$ | the Shapley value of toggle $v$; an accounting term, not a causal effect | "contribution", "effect", "explains" (unqualified) |
| systematics budget | | the decomposition $G_0 + \sum_v \phi_v = R$ with intervals | "error budget" (exposition only) |
| generation-shift contrast | $\Delta\Gamma_g$ | the probe-minus-trained-readout gap on frozen generations minus the same gap on the readout's own fresh generations | "distribution shift", "generation-shift term" |
| analog | | this design's version, on its own generations, of a published configuration | "replication" |
| shared budget cell | | the cell of the 16-cell lattice that a reconciliation analog shares with the budget, if any | |
| margin | $\delta$ | the pre-registered equivalence margin, 0.03 in $W$ | "threshold" |
| contamination stratum | | pre-cutoff vs post-cutoff release window per model | "leakage" |
| routing replay | | the offline replay of selection and triage decisions from out-of-fold scores | "deployment" |
| regret | | oracle value minus achieved value in the routing replay | |

## 16. Figure plan

Every figure is generated from `analysis/` JSON. It follows `paper/STYLE.md` rules 14 and 15: one style, no in-figure annotations, captions of at most three sentences, each figure necessary. The main body targets at most 12 pages (TMLR review time rises above that, `docs/s2/venue/TMLR_RUBRIC.md`); everything marked "appendix" stays there (TMLR F15).

| ID | Content | Claim it supports | Place |
|---|---|---|---|
| Figure 1 (hero) | The budget for the label-validity population. One row per primary model and a model-pooled row. Each row shows $G_0$, the four Shapley terms, and $R$ as points with 95 percent intervals (simultaneous intervals on the pooled row) on one horizontal axis in within-problem-or-pooled AUROC units, with a shaded band at $\pm\delta$ around zero in the $R$ column. Dots, not a waterfall, because a waterfall implies an order of terms that Shapley values do not have | D1, D2, or D3, and the term-by-term attribution (H3) | main |
| Figure 2 | Reconciliation: each published configuration of [Ribeiro], [Campos], and [2610.31820] as a point (published value) beside its analog (interval), one panel per paper on its own published unit, with the three outcomes marked by marker shape | Section 2 | main |
| Figure 3 | Strata, two panels: (a) the 4-toggle budget by stratum on the label-validity population (family, scale, base vs instruct, reasoning on/off); (b) the 3-toggle LiveCodeBench budget by contamination window, labeled as the analog. The two budgets are never on one axis | H4 | main |
| Figure 4 | Routing replay, two panels: (a) best-of-$k$ selected pass rate by configuration as bars, with random and oracle lines; (b) verification triage, regret against budget fraction, for routing by $P$ and by $S$ at the uncontrolled and controlled configurations | Decision cost of the terms | main |
| Table 1 | Model and benchmark matrix with revisions, cutoffs, problem counts, mixed counts | Setup | main |
| Table 2 | The 16-cell gap function for the pooled set, with intervals, and the six pairwise interaction indices | Shapley inputs and non-commutation (TMLR F18) | main |
| Table 3 | Primary decisions: $\bar{R}$ with the unwidened and widened 90 percent intervals, D1 to D3, the $\delta$ sensitivity, $R_{\text{pool}}$, and $R$ against each probe-family member and adapter rank | D1, D2, or D3 | main |
| Table 4 | Reconciliation table (section 2.1), with the shared-budget-cell column | Section 2 | main |
| Table 5 | Generation-shift contrast: $P$ and $S^R$ on fresh and frozen generations, $\Delta\Gamma_g$, pass rates, mixed counts (replaces the R0 Figure 3, TMLR F15) | Section 1.5 | main |
| Table 6 | All readouts and baselines in pooled AUROC, $W$, AUPRC, Brier, and the three calibration estimators, per model | Completeness | appendix |
| Table 7 | Label flips, extraction failures, reference exclusions, and tie rates per model and suite | Sections 6 and 1.2 | appendix |
| Table 8 | Diagnostic splits of $\phi_d$ and $\phi_l$; both sequential orders | Section 1.3 | appendix |

## 17. Operator sign-off

Not signed. This draft is not frozen or hashed. Sign-off freezes the design for the pilot.

```
Design version:                 R__
Margin delta (W):               ______
k and problem counts:           ______
Primary model set:              ______
Third model family (yes/no):    ______
Readings for 2610.31820:        [ ] both  [ ] A only  [ ] B only
LiveCodeBench contamination for
  Qwen3 and Qwen3-Coder:        [ ] accept gap  [ ] add a source
GPU model:                      ______
Approved by:                    ____________________
Date:                           ____________________
Design SHA-256 at freeze:       ____________________
```
