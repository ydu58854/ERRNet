#!/usr/bin/env bash
set -euo pipefail
cd /inspire/hdd/global_user/yanjunchi-24040/dyh/数字图像处理/ERRNet
RUN_ID=20260528_phaseB_full_resume_bg
EXP=errnet_phaseB_full_improved_ctx_vgg_retry
LOG="experiments/run-logs/phaseB_full_train_improved_ctx_vgg_retry_${RUN_ID}.log"
STATUS="experiments/run-logs/phaseB_full_train_improved_ctx_vgg_retry_${RUN_ID}.status"
{
  echo "[train-bg] ${EXP}"
  echo "[resume-bg] latest checkpoint in checkpoints/${EXP}"
  echo "[run] ${RUN_ID}"
  date '+[start] %F %T %z'
} >> "${LOG}"
set +e
conda run --no-capture-output -n errnet \
  env PYTHONNOUSERSITE=1 TORCH_HOME="$(pwd)/../.torch" CUDA_VISIBLE_DEVICES=0 \
  python train_errnet_unaligned.py \
    --name "${EXP}" \
    --hyper \
    -r \
    --unaligned_loss ctx_vgg \
    --gpu_ids 0 \
    --nThreads 0 \
    --display_id 0 \
    --save_iter_freq 500 \
    --no-verbose \
    --no-log \
    --no_html \
  >> "${LOG}" 2>&1
status=$?
set -e
echo "${status}" > "${STATUS}"
date '+[end] %F %T %z' >> "${LOG}"
exit "${status}"
