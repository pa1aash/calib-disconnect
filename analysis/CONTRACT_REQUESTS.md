# Contract requests from analysis (B5)

All four earlier requests were decided by the orchestrator on 2026-11-10 and are implemented:

1. Manifest saving after sealing: the stage saves the manifest (kept).
2. Results outside the run root: listed with SHA-256 in `analysis/results/<run_id>/INDEX.json`.
3. Fresh sets ("fresh:SR_<suite>_seed<s>_fold<f>", merged per suite) and the reconciliation check
   mapping: wired in `analysis/stage.py` and `analysis/recon_checks.py`.
4. Mixed NaN and finite tie-breaks within one readout: `ranking.lex_keys` raises ValueError.

Open: the readout path scheme (`RunLayout.scores`) has no generation-set component, so fresh-set
scores written by `pipeline.readouts` under the same path as frozen scores would overwrite them. The
stage reads every parquet file under `readouts/` and keys rows by their `generation_set` column, so
any distinct file name works; a path rule for fresh scores should be fixed in the contract.
