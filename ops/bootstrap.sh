#!/usr/bin/env bash
# Pod bootstrap: GPU check, uv, locked environment, Hugging Face access check, sequential model
# download at pinned revisions. Idempotent: completed steps leave marker files under $OPS_STATE_DIR.
#
#   bash ops/bootstrap.sh [--plan pilot] [--dry-run]
#
# Environment (names only; values are never printed):
#   HF_TOKEN          optional Hugging Face token, read from the environment or the untracked .env
#   HF_HOME           model cache root (default /workspace/hf-cache)
#   OPS_STATE_DIR     pod-local marker directory (default /workspace/ops-state)
#   UV_VERSION        pinned uv version (default 0.11.6)
#   ALLOW_OTHER_GPU   set to 1 to continue on a GPU that is not an RTX PRO 6000
set -euo pipefail

PLAN="pilot"
DRY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --plan) PLAN="${2:?--plan needs a value}"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    -h|--help) sed -n '2,15p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 64 ;;
  esac
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export HF_HOME="${HF_HOME:-/workspace/hf-cache}"
STATE_DIR="${OPS_STATE_DIR:-/workspace/ops-state}"
UV_VERSION="${UV_VERSION:-0.11.6}"
PLAN_FILE="$REPO_ROOT/ops/plans/$PLAN.json"

say() { echo "[bootstrap] $*"; }
# act "<description>" cmd args...: print the action; execute it unless --dry-run.
act() {
  local desc="$1"; shift
  if [ "$DRY" = 1 ]; then say "[dry-run] $desc"; return 0; fi
  say "$desc"
  "$@"
}
marker() { echo "$STATE_DIR/$1.done"; }
# step <name> "<description>" cmd...: skip if its marker exists; write the marker after success.
step() {
  local name="$1" desc="$2"; shift 2
  if [ "$DRY" = 1 ]; then
    say "[dry-run] step $name: $desc (skipped if $(marker "$name") exists)"; return 0
  fi
  if [ -f "$(marker "$name")" ]; then say "skip step $name (done)"; return 0; fi
  say "step $name: $desc"
  "$@"
  mkdir -p "$STATE_DIR"
  date -u +%Y-%m-%dT%H:%M:%SZ > "$(marker "$name")"
}

[ -f "$PLAN_FILE" ] || { echo "unknown plan: $PLAN (no $PLAN_FILE)" >&2; exit 64; }
say "plan=$PLAN repo=$REPO_ROOT HF_HOME=$HF_HOME state=$STATE_DIR dry_run=$DRY"
if [ -n "${HF_TOKEN:-}" ]; then say "HF_TOKEN: set"; else say "HF_TOKEN: not set"; fi
export HF_TOKEN="${HF_TOKEN:-}"
[ -n "$HF_TOKEN" ] || unset HF_TOKEN

# 1. GPU check (always run when executing; cheap)
if [ "$DRY" = 1 ]; then
  say "[dry-run] check: nvidia-smi --query-gpu=name must contain 'RTX PRO 6000' (override: ALLOW_OTHER_GPU=1)"
else
  if ! command -v nvidia-smi >/dev/null 2>&1; then
    if [ "${ALLOW_OTHER_GPU:-0}" = 1 ]; then say "warning: nvidia-smi not found; continuing (ALLOW_OTHER_GPU=1)"
    else echo "nvidia-smi not found. This bootstrap is for the GPU pod. Set ALLOW_OTHER_GPU=1 to override." >&2; exit 3; fi
  else
    GPU_NAME="$(nvidia-smi --query-gpu=name --format=csv,noheader | head -n 1)"
    say "GPU: $GPU_NAME"
    case "$GPU_NAME" in
      *"RTX PRO 6000"*) ;;
      *) if [ "${ALLOW_OTHER_GPU:-0}" = 1 ]; then say "warning: not an RTX PRO 6000; continuing (ALLOW_OTHER_GPU=1)"
         else echo "Expected an NVIDIA RTX PRO 6000, found: $GPU_NAME. Stop the pod and pick the right GPU type, or set ALLOW_OTHER_GPU=1." >&2; exit 3; fi ;;
    esac
  fi
fi

# 2. uv at a pinned version
install_uv() {
  curl -LsSf "https://astral.sh/uv/${UV_VERSION}/install.sh" | sh
}
if [ "$DRY" = 1 ]; then
  say "[dry-run] step uv: install uv ${UV_VERSION} via https://astral.sh/uv/${UV_VERSION}/install.sh if 'uv' is missing"
elif ! command -v uv >/dev/null 2>&1; then
  step uv "install uv ${UV_VERSION}" install_uv
  export PATH="$HOME/.local/bin:$PATH"
else
  say "uv present: $(uv --version)"
fi

# 3. locked environment
cd "$REPO_ROOT"
step sync "uv sync --group pod --frozen (from uv.lock)" uv sync --group pod --frozen

# 4. model cache directory and access check
act "mkdir -p $HF_HOME $STATE_DIR" mkdir -p "$HF_HOME" "$STATE_DIR"
LOGS_DIR="$REPO_ROOT/runs/${RUN_ID:-$PLAN}/logs"

if [ "$DRY" = 1 ]; then
  say "[dry-run] step access: uv run python -m ops.hf_access check --plan $PLAN (fails fast, naming the model and the action needed)"
  uv_models="$(python3 -c "import json,sys; c=json.load(open(sys.argv[1]))['config']['models']; print(' '.join(m for m in c if m not in ('SMOKE','MOCK')))" "$PLAN_FILE" 2>/dev/null || echo '(unreadable)')"
  say "[dry-run] models the plan lists: $uv_models"
  say "[dry-run] step models: for each model, in sequence: free-disk check, download at the pinned revision, marker under $STATE_DIR"
else
  step "access-$PLAN" "Hugging Face access check for plan $PLAN" uv run python -m ops.hf_access check --plan "$PLAN"
  # 5. sequential download; the python side skips completed models and checks free disk before each
  say "downloading models for plan $PLAN in sequence"
  uv run python -m ops.hf_access fetch --plan "$PLAN" --hf-home "$HF_HOME" --state-dir "$STATE_DIR" --logs-dir "$LOGS_DIR"
fi
say "done"
