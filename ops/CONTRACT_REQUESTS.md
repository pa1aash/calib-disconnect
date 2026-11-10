# Contract requests from B6 (ops)

None of these block the ops tests. Each needs an orchestrator decision.

1. Stage behavior for per-job configs. The runner calls each stage once per job with a RunConfig
   restricted to one model (`models=(m,)`), one benchmark (or, for a population scope, the plan's
   label-validity benchmarks), and `stages=(stage,)`. `cfg.extra` carries `job_id`, `gen_set`, `scope`
   (a benchmark or "label_validity"), and `job_kind` ("normal" or "timing"). Stages should read
   `cfg.extra["gen_set"]` as the generation-set name (layout `_gs` form).
2. Timing-only probes (pilot, design section 13). Jobs of kind "timing" use `gen_set = "timing"` and set
   `cfg.extra["timing_only"] = True` and `cfg.extra["probe"]` (`forward_pass_50_problems`,
   `lora_200_steps_50_problems`, `thinking_length_100_problems_x2`) with `problem_limit`, `lora_max_steps`,
   and `k` overrides. The stage must write the probe's own input (it must not read or write the frozen
   generation set), record wall-clock timings in `StageReport.metrics`, and list outputs under the
   "timing" generation set. Which benchmark the probes use (HumanEval+ here) is my choice; the design does
   not say.
3. Done-marker and manifest ownership. The runner writes `config/run_config.json` if absent and adds it to
   the manifest (producer `ops.runner:write_run_config`); stages must not overwrite it. The runner adds any
   declared output that the stage did not add itself. `design_sha256` is read from the first token of
   `docs/s7/FROZEN_SHA256.txt`, `lock_sha256` from `uv.lock`.
4. `.gitignore` (not mine to edit). Suggested ignores: `runs/*/logs/`, `runs/*/state/` (progress heartbeat
   and done markers are pod-local operational files; `Manifest.unlisted` already ignores both). The local
   pod ID file lives under `scratch/ops/` (already excluded through `.git/info/exclude`).
5. Package registration. `ops` is not importable from the current editable install until the next
   `uv sync` by the orchestrator (pyproject already lists `ops*`). `python -m ops` and the tests work from the
   repo root now (the tests add the repo root to `sys.path`).
6. Operator confirmations before the first real launch (see README): the RunPod GPU type ID string, the
   container image or template ID, and the REST request field names.
7. Fresh generation-shift jobs in the `full` plan carry `extra["fresh"]` entries with `adapter_path`
   `adapters/<model>/<adapter_id>` (relative to the run root, my placeholder). Stages should resolve it
   against the run layout. The plan orders them after the model's frozen readouts.
