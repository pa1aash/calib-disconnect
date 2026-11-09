#!/bin/bash
# Deploy and run V3 experiments on GH200 GPU
# Usage: bash deploy_v3.sh <IP_ADDRESS>
# Example: bash deploy_v3.sh [REDACTED-IP]

set -e

IP="${1:-[REDACTED-IP]}"
KEY="/tmp/[REDACTED-KEYFILE]"
USER="ubuntu"
REMOTE_DIR="/home/ubuntu/dl4c_experiments"

echo "=== Deploying V3 experiments to ${USER}@${IP} ==="

# 1. Copy experiment script
echo "Copying experiment script..."
scp -o StrictHostKeyChecking=no -i "$KEY" \
    "exp_v3_multimodel.py" \
    "${USER}@${IP}:${REMOTE_DIR}/"

# 2. Install any missing deps
echo "Installing dependencies..."
ssh -o StrictHostKeyChecking=no -i "$KEY" "${USER}@${IP}" << 'SETUP'
set -e
pip install -q scikit-learn datasets transformers peft accelerate torch
mkdir -p /home/ubuntu/dl4c_experiments/results_v3
echo "Dependencies installed."
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv
python3 -c "import torch; print(f'PyTorch {torch.__version__}, CUDA: {torch.cuda.is_available()}, Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"none\"}')"
SETUP

# 3. Launch experiment in background (disconnect-safe)
echo "Launching experiments (nohup)..."
ssh -o StrictHostKeyChecking=no -i "$KEY" "${USER}@${IP}" << 'RUN'
cd /home/ubuntu/dl4c_experiments
# Kill any existing run
pkill -f exp_v3_multimodel.py 2>/dev/null || true
sleep 1
PYTHONUNBUFFERED=1 nohup python3 -u exp_v3_multimodel.py > v3_log.txt 2>&1 &
echo "PID: $!"
echo "Experiments launched. Monitor with: tail -f v3_log.txt"
RUN

echo ""
echo "=== Deployment complete ==="
echo "Monitor: ssh -i $KEY ${USER}@${IP} 'tail -f ${REMOTE_DIR}/v3_log.txt'"
echo "Results: ssh -i $KEY ${USER}@${IP} 'ls -la ${REMOTE_DIR}/results_v3/'"
