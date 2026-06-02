#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ERRNET_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PROJECT_ROOT_DEFAULT="$(cd "${ERRNET_DIR}/.." && pwd)"

PROJECT_ROOT="${PROJECT_ROOT:-${PROJECT_ROOT_DEFAULT}}"
ERRNET_DIR="${ERRNET_DIR_OVERRIDE:-${PROJECT_ROOT}/ERRNet}"
ENV_NAME="${ENV_NAME:-errnet}"
SRC_CKPT="${SRC_CKPT:-checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt}"
TORCH_HOME="${TORCH_HOME:-${PROJECT_ROOT}/.torch}"

cd "${ERRNET_DIR}"
mkdir -p experiments/run-logs
mkdir -p "${TORCH_HOME}/hub/checkpoints"

echo "[precheck] ERRNet dir: ${ERRNET_DIR}"
echo "[precheck] Conda env: ${ENV_NAME}"
echo "[precheck] TORCH_HOME: ${TORCH_HOME}"

test -f "${SRC_CKPT}" || { echo "[missing] ${ERRNET_DIR}/${SRC_CKPT}"; exit 1; }
test -d datasets/processed_data || { echo "[missing] ${ERRNET_DIR}/datasets/processed_data"; exit 1; }
test -d datasets/raw_data/Dataset/DSLR/unaligned_train250 || { echo "[missing] ${ERRNET_DIR}/datasets/raw_data/Dataset/DSLR/unaligned_train250"; exit 1; }

if [[ ! -f "${TORCH_HOME}/hub/checkpoints/vgg19-dcbb9e9d.pth" ]]; then
  echo "[missing] ${TORCH_HOME}/hub/checkpoints/vgg19-dcbb9e9d.pth"
  echo "Copy vgg19-dcbb9e9d.pth there before running on an offline machine."
  exit 1
fi

conda run --no-capture-output -n "${ENV_NAME}" \
  env PYTHONNOUSERSITE=1 TORCH_HOME="${TORCH_HOME}" python - <<'PY'
import torch
from models.vgg import Vgg19
print("torch", torch.__version__)
print("cuda_available", torch.cuda.is_available())
print("cuda_device_count", torch.cuda.device_count())
_ = Vgg19(requires_grad=False)
print("vgg19_ready", True)
PY

python - <<'PY'
from pathlib import Path
required = [
    Path("datasets/processed_data/VOCdevkit/VOC2012/PNGImages"),
    Path("datasets/processed_data/real_train"),
    Path("datasets/raw_data/Dataset/DSLR/unaligned_train250"),
]
for path in required:
    print(path, "exists=", path.exists())
PY

echo "[precheck] OK"
