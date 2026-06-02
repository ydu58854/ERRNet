#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: bash $0 <improved_ctx_vgg|improved_ctx> <gpu_id>"
  exit 2
fi

TAG="$1"
GPU_ID="$2"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ERRNET_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PROJECT_ROOT_DEFAULT="$(cd "${ERRNET_DIR}/.." && pwd)"

PROJECT_ROOT="${PROJECT_ROOT:-${PROJECT_ROOT_DEFAULT}}"
ERRNET_DIR="${ERRNET_DIR_OVERRIDE:-${PROJECT_ROOT}/ERRNet}"
ENV_NAME="${ENV_NAME:-errnet}"
RUN_ID="${RUN_ID:-20260528_phaseB_full}"
TORCH_HOME="${TORCH_HOME:-${PROJECT_ROOT}/.torch}"

case "${TAG}" in
  improved_ctx_vgg)
    EXP="errnet_phaseB_full_improved_ctx_vgg"
    ;;
  improved_ctx)
    EXP="errnet_phaseB_full_improved_ctx"
    ;;
  *)
    echo "Unknown tag: ${TAG}"
    echo "Expected: improved_ctx_vgg or improved_ctx"
    exit 2
    ;;
esac

cd "${ERRNET_DIR}"
mkdir -p experiments/run-logs

CKPT="$(ls -1 "checkpoints/${EXP}"/errnet_080_*.pt 2>/dev/null | sort | tail -n 1)"
if [[ -z "${CKPT}" ]]; then
  echo "[missing] checkpoints/${EXP}/errnet_080_*.pt"
  exit 1
fi

echo "[eval] ${TAG}"
echo "[eval] checkpoint: ${CKPT}"
echo "[eval] GPU ${GPU_ID}, env ${ENV_NAME}, run ${RUN_ID}"

for dataset in ceilnet_table2 real20 postcard objects wild sir2_withgt; do
  log="experiments/run-logs/phaseB_full_eval_${TAG}_${dataset}_${RUN_ID}.log"
  status_file="experiments/run-logs/phaseB_full_eval_${TAG}_${dataset}_${RUN_ID}.status"
  set +e
  conda run --no-capture-output -n "${ENV_NAME}" \
    env PYTHONNOUSERSITE=1 TORCH_HOME="${TORCH_HOME}" CUDA_VISIBLE_DEVICES="${GPU_ID}" \
    python test_errnet.py \
      --name "errnet_phaseB_full_${TAG}_${dataset}" \
      --dataset "${dataset}" \
      --save_subdir "phaseB_full_${TAG}_${dataset}" \
      -r \
      --icnn_path "${CKPT}" \
      --hyper \
      --gpu_ids 0 \
      --nThreads 0 \
    2>&1 | tee "${log}"
  status=${PIPESTATUS[0]}
  set -e
  echo "${status}" > "${status_file}"
  if [[ "${status}" -ne 0 ]]; then
    exit "${status}"
  fi
done

set +e
conda run --no-capture-output -n "${ENV_NAME}" \
  env PYTHONNOUSERSITE=1 TORCH_HOME="${TORCH_HOME}" CUDA_VISIBLE_DEVICES="${GPU_ID}" \
  python test_errnet.py \
    --name "errnet_phaseB_full_${TAG}_custom" \
    --dataset custom \
    --input_dir ../5pictures \
    --max_long_edge 1024 \
    --save_subdir "phaseB_full_${TAG}_custom" \
    -r \
    --icnn_path "${CKPT}" \
    --hyper \
    --gpu_ids 0 \
    --nThreads 0 \
  2>&1 | tee "experiments/run-logs/phaseB_full_custom_${TAG}_${RUN_ID}.log"
status=${PIPESTATUS[0]}
set -e

echo "${status}" > "experiments/run-logs/phaseB_full_custom_${TAG}_${RUN_ID}.status"
exit "${status}"
