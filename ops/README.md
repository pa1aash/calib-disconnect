# ops: pod operations (B6)

Bootstrap, job runner, sync, cost guard, RunPod client, and dry run. Every command that would call an
API or create cost is a dry run unless `--execute` is passed. A dry run prints each action and calls
nothing. Run everything through `uv run python -m ops ...` from the repo root.

## Environment variable names

| Name | Used by | Notes |
|---|---|---|
| `RUNPOD_API_KEY` | launch, stop, guard | API key. Env var or the untracked `.env` at the repo root. |
| `HF_TOKEN` | bootstrap, hf_access, launch | Hugging Face token. Passed to the pod by name (`--env-names`, default `HF_TOKEN`). |
| `POD_SSH_HOST`, `POD_SSH_PORT`, `POD_SSH_KEY` | sync, guard `--remote` | From the pod's connect panel. Printed only as first 4 characters plus `...`. |
| `POD_SSH_USER`, `POD_REMOTE_ROOT` | sync | Defaults `root`, `/workspace/calib-disconnect`. |
| `RUNPOD_GPU_TYPE_ID`, `RUNPOD_IMAGE`, `RUNPOD_API_BASE` | launch | Optional overrides (see below). |
| `HF_HOME`, `OPS_STATE_DIR` | bootstrap (pod) | Defaults `/workspace/hf-cache`, `/workspace/ops-state`. |
| `ALLOW_OTHER_GPU` | bootstrap (pod) | `1` skips the RTX PRO 6000 name check. |
| `OPS_LOCAL_STATE` | operator machine | Where the pod ID is kept (default `scratch/ops/pod.json`, untracked). |

Secrets are never written to a file, log, or fixture. Printed secrets, pod IDs, hosts, and key paths are
shown as at most 4 characters plus `...`.

## GPU and template choice (needs operator confirmation)

The design budgets one NVIDIA RTX PRO 6000 (96 GB). The GPU type ID string used by default is
`NVIDIA RTX PRO 6000 Blackwell Server Edition`. **This string is not verified**: confirm the exact name in
the RunPod console and set `RUNPOD_GPU_TYPE_ID` or `--gpu-type-id`. No image tag is assumed; give
`--image` (or `RUNPOD_IMAGE`) or `--template-id`; use an image with CUDA 13 drivers and `git`, `curl`,
`rsync`, and SSH. The REST field names in `runpod_api.py` were written from memory of the RunPod REST
reference and were not checked against a live API; review the dry-run request once first.
Disk: the pilot plan downloads roughly 240 GB of bf16 weights (my estimate from parameter counts, not measured; T1, P1 to P6; S1 reuses P1 files), so use
`--volume-gb 400` (default) or more. The full matrix needs about 715 GB, or sequential downloads.

## Operator flow

1. Look at the jobs: `uv run python -m ops plan --plan pilot`.
2. Pilot dry run (one command, calls nothing):
   `uv run python -m ops launch --plan pilot --hourly-price-usd <price> --price-source "<where you read it>" --image <image>`
3. Real launch (creates the pod, appends the row to `runs/COST_LEDGER.csv`, saves the pod ID locally):
   `uv run python -m ops launch --plan pilot --hourly-price-usd <price> --price-source "<where you read it>" --image <image> --execute`
   The launch refuses without a price and a price source. It prints the pod-side commands.
4. On the pod, copy or clone the repo to `/workspace/calib-disconnect`, then:
   `bash ops/bootstrap.sh --plan pilot` (use `--dry-run` first). It checks the GPU, installs a pinned uv,
   runs `uv sync --group pod --frozen`, checks Hugging Face access for every model of the plan at its pinned
   revision (gated, missing, or absent revisions fail fast naming the model and the action), then downloads
   models one at a time with a free-disk check before each. Re-running skips finished steps.
5. On the pod, run the plan and the guard:
   `uv run python -m ops run --plan pilot --execute --keep-going` and
   `uv run python -m ops guard --run-id pilot --launched-at <UTC from the launch output> --execute`
   (the guard can instead run on your machine with `--remote`). The guard stops the pod when the queue is
   empty (after `--empty-grace-seconds`, default 900, so you can sync), when no progress line was written for
   `--stall-minutes` (default 45), or at `--gpu-hour-cap` (default 7.5 = 6.0 pilot GPU-hours plus 25 percent).
6. Sync and verify before the pod stops (or restart it):
   `uv run python -m ops sync --run-id pilot --skip-large --execute`
   (`--skip-large` leaves hidden-state shards, adapters, and sqlite caches on the pod; they are reported as
   missing on purpose). A tarball works too: `--tarball run.tar.gz`. Exit code 1 means a hash mismatch, 2 an
   unexpected missing file, 3 a failed pull.
7. Stop and close the ledger row: `uv run python -m ops stop --execute` (add `--terminate` to delete the
   pod). If the guard stopped the pod on the pod itself, run `uv run python -m ops ledger complete --pod-id <id> --reason <reason>` locally.
   `uv run python -m ops ledger summary` totals GPU-hours and cost.

## Sandbox

The pilot sandbox is `bwrap`. To use a container instead, pass `--container-image name@sha256:...` to `launch` and `run`; it sets `sandbox="container"` and `extra["container_image"]`.

## Plans

`smoke` (local, 6 jobs), `pilot` (40 jobs), `pilot-mixed-only` (25 jobs), `full` (stub listing, refused by `run` and `launch`).
Job IDs look like `generate.P1.mbpp_plus.frozen` and name the done markers in `runs/<run_id>/state/`.
Local smoke: `uv run python -m ops run --plan smoke --execute`.

## Resuming

`run` skips a job whose done marker exists and whose recorded outputs still match the manifest hashes. The
manifest is saved after every job. Without `--keep-going` the first failure stops the run; with it, the failed
model's remaining jobs are skipped, other models continue, and analysis is skipped.
