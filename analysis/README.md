# analysis

Statistics for the frozen design (`docs/s7/PIPELINE_DESIGN_FROZEN.md`, sections 1, 2.1, 8, 9, 10, 13),
computed only from files listed in a run manifest. Derived JSON goes to `analysis/results/<run_id>/`;
each file records the SHA-256 of the run manifest it read and a hash of this code. Every number in the
paper comes from a generated LaTeX macro traced to a file there (`paper/STYLE.md`).

| Module | Contents |
|---|---|
| `ranking.py` | Lexicographic keys of (rank_score, rank_tiebreak); NaN tie-break means none |
| `metrics.py` | Pooled AUROC, W, W_avg, AUPRC (pass and fail), Brier, Murphy decomposition, demeaned Brier, mixed counts, tie rates, d diagnostics, pass@k; `RankStats` fast path for resamples |
| `calibration.py` | Debiased equal-mass ECE, smooth ECE, KS calibration error, equal-width ECE (definitions in the module docstring) |
| `bootstrap.py` | Problem-clustered draws, replicates, percentile intervals with the undefined-replicate rule, BCa |
| `refit.py`, `decisions.py` | Seed averaging, refit widening, D1 to D3, Holm per model, heterogeneity, K4 sensitivity, R_pool |
| `shapley.py` | Shapley values, order-2 interaction indices, sequential orders, the split of the readout-change term |
| `gap.py`, `budget.py` | The 16 cells per model, secondary budgets, diagnostics, per-seed residual; pooled budgets |
| `generation_shift.py`, `routing.py` | Section 1.5 contrasts; section 10 routing replay and decision-cost games |
| `krule.py`, `reconciliation.py`, `recon_checks.py` | Section 13 k rule; section 2.1 outcome rules and verbs; paired check contrasts |
| `stage.py` | `analysis.stage:run`, the only module with file IO; sealing for the pilot |

Tests: `uv run pytest tests/analysis -q`.

Where section 9 (undefined replicates dropped, interval unavailable above 1 percent) and section 11,
row 8.4 ("kept and counted") disagree, section 9 is implemented.
