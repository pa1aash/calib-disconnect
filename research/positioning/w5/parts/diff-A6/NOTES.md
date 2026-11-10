# Notes on the A6 differential table

Run date 2026-11-10. Basis: `CELLS.md` (six full texts; NeuroSym-Cal from the wave 4 local full text, no arXiv version found).

## Clean residual: controls that no column implements as defined

No column is **present** on eight of the twelve controls:

| # | Control | Best cell(s) among the six | Why it falls short |
|---|---|---|---|
| 1 | Supervision-matched readouts | Pa: Campos, CREDO, Spiess, RLCM | Campos matches splits for trained readouts only; CREDO and RLCM train each readout with its own policy; Spiess applies only Platt scaling |
| 4 | Code-text-only baseline | Pa: Ribeiro (RankEF), Spiess (length), NeuroSym (metadata features) | none is a classifier on candidate code text fit to the study's own labels |
| 6 | Oracle swap of test suites | Pa: Spiess (exact match versus tests) | no paper contrasts original with augmented tests on the same generations |
| 7 | Release or contamination split | Pa: NeuroSym (per-model post-cutoff subset defined) | no pre- versus post-cutoff result is reported |
| 8 | Calibration estimator set | Pa: Spiess (quantile-bin plots beside equal-width ECE) | every paper reports one ECE estimator |
| 10 | Base versus instruct | none (all A) | no paired base and instruct checkpoints in any column |
| 11 | Same-weights reasoning on/off | Pa: Campos (one gpt-oss check, confidence readout only) | no toggle across all readouts |
| 12 | Routing replay with random and oracle comparators | Pa: CREDO, NeuroSym (abstention), RLCM (math early exit, oracle voting) | no replay on code with both random and oracle comparators |

**Strictly empty row (absent in all six columns): row 10, base versus instruct.**

Controls covered by at least one column (not residual):

- Row 2, trained stated confidence: CREDO and RLCM (P).
- Row 3, prompt-only baseline: Campos (P, Table V last-prompt-token probe).
- Row 5, within-problem scoring: Ribeiro and Campos (P).
- Row 9, clustered paired inference: Campos (P, problem-clustered paired bootstrap).

## Combination finding

No single column holds more than three P cells (Campos: rows 3, 5, and 9). The rows that cover trained stated confidence (CREDO, RLCM) are disjoint from the rows that cover within-problem scoring, prompt-only baselines, and clustered inference (Campos, Ribeiro). No column pairs a probe with a trained stated-confidence readout on code under matched supervision: RLCM comes closest, but its code evaluation is out of domain and its readouts come from different policies.

## Caveats

- The residual holds for these six papers only. Wave 4 lists other occupants that may cover some rows: TRIAGE 2605.13414 (random and oracle routing normalization), 2606.15841 (random, threshold, and oracle routing), 2610.11300 (base versus instruct on token readouts), Miao and Ungar 2603.25052 (base versus instruct, non-code), and Tuerlings and Valdenegro-Toro (shared post-cutoff window). See `research/positioning/w4/DIGEST.md`. Those papers were not read in this pass.
- NeuroSym-Cal was read from the wave 4 PDF extraction (`research/positioning/w4/parts/dossier-D4/raw/neurosym.txt`); no new ACL Anthology request was made.
- CREDO's "Base" and RLCM's "Base" are pre-RL checkpoints, not pretrained-only models. Row 10 is coded A for both for that reason.
- Ribeiro's significance test (GEE) is coded Pa because the clustering unit is not stated in the text.
