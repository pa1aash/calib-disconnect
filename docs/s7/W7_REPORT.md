# Wave 7 report: operator sign-off applied, design gaps closed, adversarial review, design frozen

Date: 2026-11-10. Scope: design only. No pipeline code, model weights, or model runs. Every number below is a design parameter, a planning assumption, a count from a pinned benchmark file, or a simulation output, with its file.

## 1. Model identifier

The orchestrator ran as `claude-opus-5-5`. Sub-agents: the A1 to A4 records and the B2 power audit (analyst) ran on their configured models; the two C1 critics ran on opus in fresh context.

## 2. Commits and checks

| Commit | Content |
|---|---|
| `799a599` | Part A sub-agent records: third-family evaluation, benchmark pins and post-cutoff counts, design bibliography, differential rows 13 to 17 |
| `fa6b0c7` | Part A synthesis: `docs/s7/BENCHMARK_PINS.md`, `research/positioning/w7/references_design.bib` (19 entries), `research/positioning/w7/DIFFERENTIAL_R2.md` |
| `de09536` | Part B: `docs/s7/PIPELINE_DESIGN_R2.md` with change log C1 to C21, the revised power audit, the GPU-hour budget |
| `fb4de3e` | Red-team records, `docs/s7/RED_TEAM_DISPOSITION.md`, the power follow-up, and the frozen-design budget |
| `e75d219` | Freeze: `docs/s7/PIPELINE_DESIGN_FROZEN.md`, `docs/s7/FROZEN_SHA256.txt`, the freeze check in `tools/hooks/pre-commit`, `docs/DEVIATIONS.md` |
| (this report) | `docs/s7/W7_REPORT.md` and `docs/CONTEXT.md` |

Checks:

- Start state: no unexpected tracked changes; remote HEAD matched local.
- Every commit passed the pre-commit hook (identity, attribution strings, legacy freeze, design freeze, staged gitleaks). One rejection in Part A (seven gitleaks hits on Hugging Face Space names in API JSON and GitHub page tokens in saved HTML, none a secret of this project) was fixed by adding their fingerprints to `.gitleaksignore` with a comment and recommitting; no bypass.
- The design-freeze check was tested in a scratch clone: a modified frozen file is rejected, both for the modification and for the hash mismatch.
- Full-history gitleaks (`gitleaks git --redact` over every commit through `e75d219`): exit 0, no findings.
- Push: after pushing `e75d219`, `origin/main` equals local HEAD (`e75d219`). The commit that adds this report is pushed and verified the same way.

## 3. Model matrix with roles

Third family: **Gemma 4** (Apache-2.0, not gated, base and instruct pairs at 12B and 31B, hidden states accessible, bf16 fits one 96 GB GPU). Gemma 3, Llama 3.x, Mistral and Ministral, IBM Granite, Falcon-H1, DeepSeek-Coder, and EXAONE were evaluated, with reasons, in `docs/s7/parts/models-A1/MODELS_A1.md`. Granite 4.1 8B and 30B is the recorded alternate.

| ID | Role | Model |
|---|---|---|
| P1, P2 | Primary, instruct, thinking off | Qwen3-8B, Qwen3-14B |
| P3, P4 | Primary, instruct | Olmo-3-7B-Instruct, Olmo-3.1-32B-Instruct |
| P5, P6 | Primary, instruct, thinking off | gemma-4-12B-it, gemma-4-31B-it |
| B1 to B6 | Base stratum (bases of P1 to P6) | Qwen3-8B-Base, Qwen3-14B-Base, Olmo-3-1025-7B, Olmo-3-1125-32B, gemma-4-12B, gemma-4-31B |
| S1 | Reasoning toggle (same weights as P1); [2610.31820] reconciliation; generation-shift model | Qwen3-8B, thinking on |
| C1, C2 | Coder-variant stratum (moved from R1 primary); C1 is the [Ribeiro] model | Qwen2.5-Coder-7B-Instruct, -32B-Instruct |
| C3, C4 | Coder base versus instruct | Qwen2.5-Coder-7B, -32B |
| T1, T2 | Post-training trajectory; T1 is the pilot model | Olmo-3-7B-Instruct-SFT, -DPO |
| X1, X2 | [Campos] reconciliation only | Qwen3-Coder-30B-A3B-Instruct, gpt-oss-20b |

Revisions are pinned in section 3.2 of the frozen design.

## 4. Benchmark pins and post-cutoff counts

Source: `docs/s7/BENCHMARK_PINS.md`.

- HumanEval+ v0.1.10 (164 tasks); MBPP+ v0.2.0 (378 tasks) plus the EvalPlus ground-truth patch `fix_v020.py` at `26d6d00` (the June 2024 fixes are not in any release); 542 problems in all. The 21 MBPP+ IDs removed in v0.2.0 are listed. MBPP-sanitized has 427 tasks.
- LiveCodeBench: `release_v6` at Hugging Face commit `0fe84c3`, the newest release as of 2026-11-10 (no newer release in the official repository); 1,055 problems, all with private tests (18 with fewer than 5).
- Post-cutoff counts on release_v6 (`contest_date` after the count date): Olmo 3, 182; Gemma 4, 131; Qwen3, 0 (no clean stratum, a stated limitation; no scraping); gpt-oss-20b, 497; Qwen3-Coder, 0; [Campos] window, 341.
- Downloaded files are cached in a git-ignored folder (`docs/s7/parts/bench-A2/cache/`); hashes are in the manifest.

## 5. Power and $\delta$

Source: `docs/s7/power/POWER_R2.md` (sections on the R2 rule and "Red-team follow-up"). Planning assumptions: $n = 542$, $\kappa = 0.801$, $\mu$ 0.72 (7 to 12B) and 0.80 (14 to 32B), fixed-effects heterogeneity $\tau_R$ 0.02 nominal and 0.04 conservative, refit noise 0.10 trained and 0.05 probe, widening with $t_{12} = 1.782$.

| $k$ | $\delta$ | Minimum power over D1 to D3 (nominal / conservative) |
|---|---|---|
| 10 | 0.02 | 0.685 / 0.662 |
| 10 | 0.03 | 0.979 / 0.971 |
| 20 | 0.02 | 0.858 / 0.848 |
| 20 | 0.03 | 0.994 / 0.990 |

**Rule 1 applied: $\delta = 0.03$**, because power at 0.02 is below 0.90. Caveats carried into the design: doubling the refit noise lowers D1 at $\delta = 0.03$, $k = 10$, to 0.64 to 0.72 (measured on T1 in the pilot); one model at about 60 mixed gives 0.915 to 0.917; $\rho_e = 0.2$ gives 0.931 to 0.944; the simulation fits no readouts, so its widths are lower bounds.

## 6. Pilot threshold

$T_{10} = 185$ and $T_{20} = 125$ mean EvalPlus-mixed problems per model (larger bracketed crossing of 0.90 over the $n$, $\mu$, and $\kappa$ sweeps, plus 10 percent, rounded up to a multiple of 5; verified at minimum power 0.940 and 0.946). They replace R2's 140 and 90, set from the $n$ sweep alone, before any data. If the pilot's mean over P1 to P6 is below 185, $k = 20$ for the full run. The planning expectation is 233 at $k = 10$.

## 7. Compute budget

Source: `docs/s7/budget/budget_frozen.json` (script `budget_r2.py`). One RTX PRO 6000 (96 GB); planning throughputs, not measurements.

| $k$ | GPU-hours | With 25 percent contingency |
|---|---|---|
| 10 | 269.7 | 337.2 |
| 20 | 529.8 | 662.3 |

R2 was 226.8 (283.4) at $k = 10$; the frozen design adds recipe selection under fold seeds 1 and 2 (V1) and four-fold LiveCodeBench adapters (V14e). CPU about 395 hours at $k = 10$. The hourly price is recorded at pilot launch.

## 8. Red-team top findings and dispositions

37 findings: validity 0 BLOCKING, 12 MAJOR, 2 MINOR; claims 3 BLOCKING, 14 MAJOR, 6 MINOR. All resolved inside the sign-off (`docs/s7/RED_TEAM_DISPOSITION.md`); the freeze proceeded.

| Finding | Disposition |
|---|---|
| K1 (BLOCKING) outcome templates overreach | Population prefix, defined readout names, "equivalent within the 0.03 margin", shared-information caveat |
| K2 / V5 (BLOCKING) $\phi_t$ mixes format and training | Pre-registered format step and training step; name "readout change (format and training)" |
| K3 (BLOCKING) the ".02 tie" is not in 2610.31820 | Verified against the saved text (txt:1115 reads .02 as a lead); now "this design's reading of Table 3", removed as a margin anchor |
| V1 recipe selection could see other seeds' test labels | Selection per (fold seed, outer fold); budget recomputed |
| V4 budget identity holds at seed 0, not for $\bar{R}$ | Game residual labeled $R^{(0)}$, shown beside $\bar{R}$ |
| V8 adapter mask test too narrow | Per-architecture test in training layout and scoring engine, tolerance plus positive control |
| V10 $k$ threshold scenario | $\mu$, $\kappa$, heterogeneous-count, and $\rho_e$ stress; thresholds raised to 185 and 125 |
| V12 pilot model previews P3 | Analysis code hashed before T1 outputs are opened; T1 cells sealed |
| K9 to K14 reconciliation rules | Consistent / not consistent / undetermined; descriptive levels; one outcome per reading; gpt-oss prefill fixed; FitMBPP listed |
| K15 / K16 novelty and title | Claims of novelty mapped to differential rows 13, 15, 16; title rules and a new title |

## 9. Frozen hash

`docs/s7/PIPELINE_DESIGN_FROZEN.md` SHA-256 `d83c97c536c984a58ebdc21023f3c19c15e07880f90195f1da76ebec62428c3a`, recorded in `docs/s7/FROZEN_SHA256.txt` and checked by `shasum -a 256 -c`. The pre-commit hook rejects any change to either file.

## 10. Deviations

`docs/DEVIATIONS.md` is created with its rules and an empty table: no deviations recorded. The application of the $k$ rule and any K7 cut will be logged there as pre-registered adjustments.

## 11. [OPERATOR] items, with exact actions

1. **[OPERATOR] Review the frozen design.** Read `docs/s7/PIPELINE_DESIGN_FROZEN.md` section 0 (F1 to F22) and section 17. The sign-off block is recorded as "signed by operator via checkpoint"; if any red-team resolution is unacceptable, it must be recorded as a deviation in `docs/DEVIATIONS.md` before the pilot, since the file itself cannot change.
2. **[OPERATOR] GPU price.** At pilot launch, record the RTX PRO 6000 hourly price (an operator input) so the currency cost is computed from 337.2 / 662.3 GPU-hours with contingency.
3. **[OPERATOR] Threshold change.** The $k$-rule thresholds were raised before freezing (140 to 185, 90 to 125) on red-team finding V10. Confirm this reading of sign-off item 2 ("the count B2 requires for 0.90 power").
4. **[OPERATOR] LiveCodeBench licence.** The problem-text licence is inconsistent (card `cc`, loader and repository MIT; contest-site terms unstated). Only IDs are redistributed; decide whether any text may be released.
5. **[OPERATOR] TMLR disclosure footnote.** Draft at the manuscript stage from the TMLR policy text current at submission (`TMLR_RUBRIC.md:58`).
6. **[OPERATOR] Optional API key.** Put a Semantic Scholar or OpenAlex key in a local, untracked `.env` if fuller literature instruments are wanted.
7. **[OPERATOR] Former GPU host.** Rotate the former host key and host if still live (open since wave 0).
8. **[OPERATOR] Pilot GPU access.** Provide the RTX PRO 6000 host for the pilot wave (T1 end to end, mixed counts for P1 to P6, throughput probes).
