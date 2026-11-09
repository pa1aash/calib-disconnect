#!/usr/bin/env bash
# Turnkey bootstrap for the DPRC pipeline on a fresh Lambda/Hyperstack A100 box.
# Usage:  bash setup_lambda.sh   (run from the repo root or src/v4_dprc)
set -euo pipefail

echo "== DPRC box bootstrap =="
python3 --version

# 1) venv
python3 -m venv ~/dprc_venv
source ~/dprc_venv/bin/activate
pip install --upgrade pip wheel

# 2) core deps. Torch is pinned to what results/v3/harness_info.json recorded (2.11.0+cu130).
#    If the box's CUDA differs, install the matching torch wheel first, THEN the rest.
#    (vLLM pins its own compatible torch; if there's a conflict, install vllm FIRST and let it
#     pull torch, then pip install the remaining packages.)
pip install "torch==2.11.0" --index-url https://download.pytorch.org/whl/cu130 || \
  echo "WARN: pinned torch/cu130 unavailable on this box — install the matching CUDA torch wheel manually, then re-run the rest."

pip install \
  "vllm" \
  "transformers>=4.44" \
  "peft>=0.12" \
  "trl>=0.10" \
  "datasets>=2.20" \
  "accelerate>=0.33" \
  "scikit-learn>=1.4" \
  "numpy>=1.26"

# 3) HF cache on the persistent disk (avoids re-download after a restart — addresses the
#    persistence pain that motivated choosing Lambda/Hyperstack)
export HF_HOME="$HOME/hf_cache"
mkdir -p "$HF_HOME"
echo "export HF_HOME=$HF_HOME" >> ~/.bashrc

# 4) sanity checks
python3 - <<'PY'
import torch, importlib
print("torch:", torch.__version__, "cuda?", torch.cuda.is_available(),
      "| device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU")
for m in ["vllm","transformers","peft","trl","datasets","sklearn","numpy"]:
    importlib.import_module(m); print("ok:", m)
PY

# 5) warm the small dataset caches + run the CPU self-tests to confirm the port works
python3 - <<'PY'
from datasets import load_dataset
load_dataset("openai/openai_humaneval", split="test")
load_dataset("google-research-datasets/mbpp", "sanitized", split="test")
print("HumanEval + MBPP cached.")
PY

echo "== running CPU self-tests =="
for f in metrics pertest_harness grouping serialization conf_block; do
  echo "--- $f ---"; python3 "$f.py" >/dev/null && echo "PASS $f"
done

echo "== bootstrap complete. Next: python3 label_dataset.py --sources mbpp apps taco livecodebench --limit 3000 --model qwen2.5-coder-7b =="
