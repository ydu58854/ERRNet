#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

GPU_CTX_VGG="${GPU_CTX_VGG:-0}"
GPU_CTX="${GPU_CTX:-1}"

echo "[shared-disk] eval improved + ctx_vgg on GPU ${GPU_CTX_VGG}"
bash "${SCRIPT_DIR}/20_eval_phaseB_full_one.sh" improved_ctx_vgg "${GPU_CTX_VGG}" &
pid_ctx_vgg=$!

echo "[shared-disk] eval improved + ctx on GPU ${GPU_CTX}"
bash "${SCRIPT_DIR}/20_eval_phaseB_full_one.sh" improved_ctx "${GPU_CTX}" &
pid_ctx=$!

set +e
wait "${pid_ctx_vgg}"
status_ctx_vgg=$?
wait "${pid_ctx}"
status_ctx=$?
set -e

echo "[shared-disk] eval ctx_vgg status: ${status_ctx_vgg}"
echo "[shared-disk] eval ctx status: ${status_ctx}"

if [[ "${status_ctx_vgg}" -ne 0 || "${status_ctx}" -ne 0 ]]; then
  exit 1
fi

echo "[shared-disk] both evaluations completed"
