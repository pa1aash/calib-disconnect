"""Central config for the DPRC pipeline. Cross-platform (no hardcoded /home/ubuntu paths).

Override the results/data roots with env vars DPRC_DATA / DPRC_RESULTS on the box.
All experiment knobs are frozen here so they land in the reproducibility checklist (plan GATE-6).
"""
from __future__ import annotations
import os
from pathlib import Path

# ---- roots (env-overridable; default to a v4/ tree next to the existing results/) ----
_here = Path(__file__).resolve()
PROJECT_ROOT = _here.parents[2]                      # .../Calibration Disconnect
DATA_ROOT = Path(os.environ.get("DPRC_DATA", PROJECT_ROOT / "data" / "v4_dprc"))
RESULTS_ROOT = Path(os.environ.get("DPRC_RESULTS", PROJECT_ROOT / "results" / "v4_dprc"))
LABELS_DIR = DATA_ROOT / "labels"                    # per-test labeled datasets (Build #3 output)
ADAPTER_DIR = DATA_ROOT / "adapters"                 # LoRA adapters
for _d in (DATA_ROOT, RESULTS_ROOT, LABELS_DIR, ADAPTER_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# ---- models (HF ids; match the v3 registry) ----
MODELS = {
    "qwen2.5-coder-7b": "Qwen/Qwen2.5-Coder-7B-Instruct",     # PRIMARY (headline)
    "deepseek-coder-6.7b": "deepseek-ai/deepseek-coder-6.7b-instruct",  # cross-model confirmation
}
PRIMARY_MODEL = "qwen2.5-coder-7b"

# ---- sampling (frozen; matches the v3 harness that produced AUROC 0.987) ----
N_SAMPLES = 10                # solutions per problem for confidence targets
N_LABEL_EXTRA = 1            # the (n+1)th independent sample for the unbiased eval label
TEMPERATURE = 0.8
TOP_P = 0.95
MAX_NEW_TOKENS = 512
EXEC_TIMEOUT = 10            # seconds per test (matches v3)

# ---- data pool (plan Phase 1) ----
MIN_TESTS_PER_PROBLEM = 3    # >=3-test filter
POOL_TARGET = 3000           # 2000-4000 problems
POOL_MIX = {                 # TACO = dense per-test spread workhorse; APPS dropped (call-based swamp)
    "mbpp": 0.15, "taco": 0.65, "livecodebench": 0.20,
}
# contamination-controlled eval windows for LiveCodeBench (ISO dates). Set on the box to a window
# that post-dates BOTH models' training cutoffs; keep train/eval windows disjoint.
LCB_TRAIN_WINDOW = (None, "2024-06-30")     # (start, end) used for training pool
LCB_EVAL_WINDOW = ("2024-09-01", None)      # disjoint, later, contamination-controlled — PRIMARY eval

# ---- grouping / DPRC (frozen — pre-registered) ----
GROUPING_LEVEL_L1 = "l1"     # per-test-case (bold headline)
GROUPING_LEVEL_L2 = "l2"     # per-category (safe fallback)

# ---- DPRC training (LoRA; matches exp_final_a100 + DCPO-style recipe) ----
LORA_R = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.05
LORA_TARGETS = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
SFT_EPOCHS = 3
SFT_LR = 2e-5
SFT_BATCH = 1
SFT_GRAD_ACCUM = 16
MAX_SEQ_LEN = 2048
SEED = 42

# ---- gates (pre-registered thresholds) ----
GATE0_MAX_EXEC_WALLCLOCK_DAYS = 2.0
GATE0_MAX_GPU_BUDGET_USD = 375.0
GATE1_MIN_PROBLEMS = 1500
GATE1_MIN_SPREAD_FRAC = 0.20     # >=20% of groups must have an intermediate target in (0.1, 0.9)
GATE2_AUROC_THRESHOLD = 0.65     # pilot per-test (or per-category) AUROC gate
GATE2_AMBER_AUROC = 0.63         # by 07-20: below this AND collapsed -> escalate
PILOT_N_PROBLEMS = 300

# ---- confidence verbalization tokens (structured block the model emits) ----
# The model emits, per requirement group g, a line: "REQ <group_id>: <bucket>"
# mapped to a scalar for scoring. Tokenized-Brier trains on the CONTINUOUS target; these buckets
# are the discrete readout used at inference + for the coarse-tier ablation baseline.
CONF_BUCKETS = {"very_low": 0.1, "low": 0.3, "medium": 0.5, "high": 0.7, "very_high": 0.9}
