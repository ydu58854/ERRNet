#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ERRNET_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PROJECT_ROOT_DEFAULT="$(cd "${ERRNET_DIR}/.." && pwd)"

PROJECT_ROOT="${PROJECT_ROOT:-${PROJECT_ROOT_DEFAULT}}"
ERRNET_DIR="${ERRNET_DIR_OVERRIDE:-${PROJECT_ROOT}/ERRNet}"
ENV_NAME="${ENV_NAME:-errnet}"
RUN_ID="${RUN_ID:-20260528_phaseB_full}"
GPU_ID="${GPU_ID:-0}"
EXP="${EXP:-errnet_phaseB_full_improved_ctx_vgg}"
SRC_CKPT="${SRC_CKPT:-checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt}"
TORCH_HOME="${TORCH_HOME:-${PROJECT_ROOT}/.torch}"

cd "${ERRNET_DIR}"
mkdir -p experiments/run-logs

test -f "${SRC_CKPT}" || { echo "[missing] ${ERRNET_DIR}/${SRC_CKPT}"; exit 1; }
test ! -e "checkpoints/${EXP}" || { echo "[exists] checkpoints/${EXP}; move or rename it before a fresh full run"; exit 1; }

echo "[train] ${EXP}"
echo "[train] GPU ${GPU_ID}, env ${ENV_NAME}, run ${RUN_ID}"

set +e
conda run --no-capture-output -n "${ENV_NAME}" \
  env PYTHONNOUSERSITE=1 TORCH_HOME="${TORCH_HOME}" CUDA_VISIBLE_DEVICES="${GPU_ID}" \
  python train_errnet_unaligned.py \
    --name "${EXP}" \
    --hyper \
    -r \
    --icnn_path "${SRC_CKPT}" \
    --unaligned_loss ctx_vgg \
    --gpu_ids 0 \
    --nThreads 0 \
    --display_id 0 \
    --save_iter_freq 500 \
    --no-verbose \
    --no-log \
    --no_html \
  2>&1 | tee "experiments/run-logs/phaseB_full_train_improved_ctx_vgg_${RUN_ID}.log"
status=${PIPESTATUS[0]}
set -e

echo "${status}" > "experiments/run-logs/phaseB_full_train_improved_ctx_vgg_${RUN_ID}.status"
exit "${status}"
