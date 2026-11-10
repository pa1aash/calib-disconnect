# Wave 6 Report: systematics-budget positioning (Part A) and draft pipeline design (Part B)

Date: 2026-11-10.

**Outcome.** Part A ran to completion, and its stop condition did not fire. Part B produced the draft design `docs/s6/PIPELINE_DESIGN_R0.md`, three critics reviewed it, and the revision is `docs/s6/PIPELINE_DESIGN_R1.md`, with every finding traced in `docs/s6/CRITIQUE_DISPOSITION.md`. The design is a DRAFT: it is not frozen or hashed. No pipeline code, run, or manuscript text exists.

**Start-state check: passed.** Tracked files were clean, the branch was `main`, local HEAD equaled origin/main, and both hooks were installed. The untracked stubs in `research/temp/` and `scratch/w5-excluded/` were left untouched.

## 1. Model identifier

- **Orchestrator:** `claude-opus-5-5` (Opus 5.5).
- **Sub-agents:**
  - Part A: occ-A1a, occ-A1b, proto-A2, margin-A3, closed-A4 on the default sub-agent model; critic-A6 on opus.
  - Part B: models-B3, bench-B4, and power-B9 on the default sub-agent model; methodologist and TMLR-reviewer critics on opus; the budget and feasibility critic on sonnet.

## 2. Commits and checks

Every commit was authored and committed as Palaash Gang. Both hooks ran on every commit, and `--no-verify` was never used.

| SHA | Contents |
|---|---|
| `dd6809a` | Part A sub-agent records (occupancy searches, 2610.31820 protocol, MARGIN inventory, closed items, critic findings) |
| `847ee7a` | Part A synthesis (`research/positioning/w6/`), differential revision 1 |
| `53512ff` | Part B sub-agent records (model matrix, benchmark facts, power simulation, design critic findings) |
| `671fa12` | Design R0 and R1, critique dispositions, power files, glossary in `paper/STYLE.md` |
| this commit | This report and `docs/CONTEXT.md` |

**Checks.**

- **gitleaks on staged changes** before each commit: no leaks after triage. Wave 6 added 63 false-positive fingerprints to `.gitleaksignore`: 6 in Part A (model-name lists, Semantic Scholar paper IDs, a pagination token) and 57 in Part B (saved public GitHub and Hugging Face pages: expiring signed image-URL tokens, per-session page HMACs and upload tokens, MBPP+ numeric test data, Space names). None is a project secret.
- **gitleaks on the full history** (about 220 MB): no leaks found.
- **Pre-commit attribution check.** It rejected the first Part B commit, because three saved upstream commit feeds contain third-party co-author trailers. Fix: the three files stay on disk, untracked, listed in `.git/info/exclude`, and documented in `docs/s6/parts/bench-B4/LOCAL_ONLY.md`. Then the commit passed.
- **Remote.** After the push of `671fa12`, remote HEAD equaled local HEAD. The final push of this commit is verified the same way.

**Process notes.**

- Every critic's own write to its record file was blocked by the harness, so the orchestrator saved the returned text to `docs/s6/parts/critic-*/FINDINGS.md`.
- The wave 5 power files were copied, not moved, from `scratch/w5-power/` to `docs/s6/power/w5-baseline/`; moving would delete the originals.

## 3. Part A findings (`research/positioning/w6/`)

- **A1, decomposition occupancy.** Stop condition not triggered; the A6 critic concurs. No full text attributes the probe-versus-stated gap to two or more of supervision, difficulty, label validity, and generation shift on shared generations. The specific estimand is CLEAN (provisional). The broader idea is NARROW: 2605.27752 (one-axis protocol shifts of a token-versus-verbal gap), 2609.04582 (recalibration versus residual, probe versus answer), and RADAR 2610.22139 (risk decomposition). 2609.33290 holds supervision, a difficulty-like control, and an unisolated generation confound.
- **A2, 2610.31820 protocol.** Which generations the R-Tuning readout was scored on is not stated. Two readings fit the text, so the design reproduces both.
- **A3, MARGIN.** MARGIN re-scores the same programs under EvalPlus, for verbalized confidence only, with 10-bin ECE, and reports no matched original-suite values for the same cohort. The count flag resolved as 9 x 163 and 9 x 224.
- **A4, closed items.** Miglani et al. "0.677 versus 0.703" is VERIFIED (within-problem AUC, same attempts, layer chosen without a holdout, no tie averaging). The content of the 2610.34654 bug reports is not specified in the paper; a fixed wording is recorded.
- **A5, differential revision 1.** 17 rows, with supplementary columns for MARGIN, 2605.27752, and 2609.04582 and a "Systematics budget" column. No assessed column has a P cell on rows 13 to 17. Unsearched cells are "not assessed".

## 4. Estimands, margin, and outcome sentences (design R1 section 1)

- **Gap function.** $\Gamma(r, t, d, l)$, probe metric minus stated metric over four toggles: isotonic recalibration, trained stated readout, within-problem scoring, EvalPlus labels. $G_0 = \Gamma(0,0,0,0)$ (pooled AUROC); $R = \Gamma(1,1,1,1)$ (within-problem AUROC $W$); $G_0 + \sum_v \phi_v = R$ with Shapley terms, interaction indices, and two sequential orders. $R_{\text{pool}} = \Gamma(1,1,0,1)$ is a secondary statistic.
- **Generation shift.** A paired contrast $\Delta\Gamma_g$ outside the attribution.
- **Primary statistic.** $\bar{R}$, the mean over six primary instruct models on the label-validity population.
- **Three decisions.** D1 equivalence (TOST), D2 probe ahead by more than $\delta$, D3 stated readout ahead by more than $\delta$; mutually exclusive; otherwise inconclusive.
- **$\delta = 0.03$ in $W$,** justified on substantive grounds (the field's tie readings, the published pooled gaps of .20 to .31, the spread of published within-problem values); sensitivity at 0.02 and 0.05.

**Outcome sentences** (all four are in R1 section 1.8):

- D1: "On frozen, execution-labeled code from six open instruct models (four Qwen, two Olmo), a trained stated readout matches a hidden-state probe within problems: after training the stated readout on the probe's labels, scoring within problems, and relabeling with EvalPlus, the within-problem gap lies within 0.03 AUROC of zero. The pooled gap of [G0] AUROC is attributed, with problem-clustered intervals, to [named terms]." Followed by the capacity caveat.
- D2: "On frozen, execution-labeled code from six open instruct models (four Qwen, two Olmo), a hidden-state probe ranks a problem's samples better than a stated readout trained on the same labels, by more than 0.03 within-problem AUROC, after EvalPlus relabeling. The pooled gap of [G0] AUROC is attributed, with problem-clustered intervals, to [named terms] and this residual."

## 5. Reconciliation (design R1 section 2)

Analogs on this design's generations, each with a "shared budget cell" column and one of three outcomes (reproduced, not reproduced, undetermined):

- **[Ribeiro] RQ2,** Qwen2.5-Coder-7B-Instruct on HumanEval, pass@rank-1: LAT above Random and above Reflective T/F; levels against 85.1 and 80.2.
- **[Campos],** Qwen3-Coder-30B-A3B and gpt-oss-20b on LiveCodeBench (October 2024 to April 2025; May 2025 is outside release_v6): prompt-only pooled pattern, code-token probe within-problem above 0.5, judging-pass below code-token.
- **[2610.31820],** Qwen3-8B thinking on, LiveCodeBench, R-Tuning-style readout against a same-label probe under reading A (fresh) and reading B (frozen), each paired.

## 6. Model and benchmark matrix (design R1 sections 3 and 4)

| Role | Models (all Apache-2.0, non-gated, revisions pinned) |
|---|---|
| Primary instruct (6) | Qwen2.5-Coder-7B-Instruct, Qwen2.5-Coder-32B-Instruct, Qwen3-8B (thinking off), Qwen3-14B (thinking off), Olmo-3-7B-Instruct, Olmo-3.1-32B-Instruct |
| Base stratum (6) | Qwen2.5-Coder-7B and 32B, Qwen3-8B-Base and 14B-Base, Olmo-3-1025-7B, Olmo-3-1125-32B |
| Reasoning toggle | Qwen3-8B, thinking on |
| Trajectory | Olmo-3-7B-Instruct-SFT (also the pilot model) and -DPO |
| Reconciliation only | Qwen3-Coder-30B-A3B-Instruct, gpt-oss-20b |

| Benchmark | Version | Problems | Role |
|---|---|---|---|
| HumanEval / HumanEval+ | openai_humaneval; EvalPlus v0.1.10 | 164 | label-validity population |
| MBPP+ | EvalPlus v0.2.0 | 378 | label-validity population |
| LiveCodeBench | release_v6 | 1,055 (May 2023 to April 2025) | contamination stratum; 3-toggle budget; reconciliation |

## 7. Power (design R1 section 9; `docs/s6/power/`)

- **Choice: $k = 10$ samples per problem, $n = 542$ problems** (label-validity population), plus 1,055 LiveCodeBench problems.
- **At $M = 6$:** P(D1 | $R = 0$) = 1.00 and P(D2 | $R = 0.06$) = 1.00, with independent shocks and with shocks shared across models (rho 0.5 and 1). Mean 90 percent half-width about 0.008.
- **Per model ($M = 1$):** 0.66 and 0.83.
- **Margin grid at $M = 6$:** P(D1 | $R = 0$) is 0.29 to 0.44 at 0.01, 0.80 to 0.92 at 0.015, and 0.96 to 1.00 at 0.02.
- **Caveat.** The simulation fits no readouts, so its widths are lower bounds; 100 replicates per cell.

## 8. Compute total (design R1 section 12)

**176.6 GPU-hours before contingency; 220.8 with 25 percent contingency** (R0: 132.4 and 158.9). About 370 CPU-hours. About 66 GB of hidden states and about 544 GB of model weights. The largest items are the trained stated readouts (105.6 h, of which the two 32B instruct models take 38.1 h) and the [2610.31820] thinking-on reconciliation (23.1 h). Throughputs are unmeasured planning assumptions; the GPU model is not fixed.

## 9. Critics and dispositions (`docs/s6/CRITIQUE_DISPOSITION.md`)

59 findings: 49 accepted, 10 modified, 0 rejected.

| Critic | Findings | Main changes in R1 |
|---|---|---|
| Methodologist (opus) | 24 (3 blockers) | Lexicographic tie-break so isotonic creates no ranking ties; probe family and capacity controls; game fit on the 542-problem population only; nested cross-fitting of the isotonic map; inner-CV recipe for the adapter; third decision; fixed refit-variance rule; pilot outside the primary set |
| TMLR reviewer (opus) | 21 (5 blockers) | $R_{\text{pool}}$; rewritten outcome sentences with the capacity caveat and the exact model set; analogs with a shared-cell column; three-outcome reconciliation; margin justification without the power argument; citation table; figure plan without a waterfall; release and anonymization plan |
| Budget and feasibility (sonnet) | 14 (no blocker) | Recomputed budget; reading-B scoring added; CPU budget; K7 cuts that keep the primary set; pilot covers 32B and thinking-on length; bfloat16 storage; LiveCodeBench has no reference solutions |

Modified rather than accepted as proposed: the capacity fix (no attention-pooled probe, for storage), recipe selection (one suite, reused), the label-toggle split (a diagnostic), family balance (an operator item), hardware and prices, extraction failures, median imputation, and the generation-shift row arithmetic.

## 10. Open decisions

- Whether $\delta = 0.03$ stands, given that the design could decide at 0.02.
- Whether the primary set should gain a third, non-Qwen family.
- Whether both readings of 2610.31820 are needed (reading A costs most of the 23.1 h reconciliation row).
- The contamination stratum for Qwen3 and Qwen3-Coder, which is not estimable on release_v6.
- The B4 gaps to resolve from the pinned files before the pilot (removed MBPP+ IDs, the EvalPlus June 2024 fixes, LiveCodeBench private tests and licence).
- The rows of `research/positioning/w6/DIFFERENTIAL_R1.md` marked "not assessed" for five papers.

## 11. [OPERATOR] items

1. **Review and sign the design.** Read `docs/s6/PIPELINE_DESIGN_R1.md` and `docs/s6/CRITIQUE_DISPOSITION.md`, then fill the section 17 block: margin, $k$ and problem counts, primary model set, third family yes or no, readings for 2610.31820, LiveCodeBench contamination choice, and GPU model. The next wave freezes and hashes the signed version.
2. **Name the GPU and its hourly price,** so the budget can be converted to cost and the throughput assumptions checked.
3. **Decide the Qwen3 and Qwen3-Coder contamination gap:** accept it, or name a newer problem source to add to the allowlist.
4. **Decide the TMLR LLM-use footnote wording** (carried from wave 5).
5. **Optional: a Semantic Scholar or OpenAlex key** in a local, untracked `.env` (carried).
6. **Rotate the former GPU host key and host if still live** (carried from wave 0).
