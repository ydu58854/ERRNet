#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ERRNET_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PROJECT_ROOT_DEFAULT="$(cd "${ERRNET_DIR}/.." && pwd)"

PROJECT_ROOT="${PROJECT_ROOT:-${PROJECT_ROOT_DEFAULT}}"
ERRNET_DIR="${ERRNET_DIR_OVERRIDE:-${PROJECT_ROOT}/ERRNet}"
RUN_ID="${RUN_ID:-20260528_phaseB_full}"
OUT="${OUT:-phaseB_full_improved_ctx_and_ctx_vgg_${RUN_ID}.tar.gz}"

cd "${ERRNET_DIR}"

echo "[package] writing ${ERRNET_DIR}/${OUT}"

tar -czf "${OUT}" \
  experiments/offline-phaseB-full \
  checkpoints/errnet_phaseB_full_improved_ctx_vgg \
  checkpoints/errnet_phaseB_full_improved_ctx \
  experiments/run-logs/phaseB_full_*_"${RUN_ID}".* \
  results/phaseB_full_improved_ctx_vgg_* \
  results/phaseB_full_improved_ctx_*

sha256sum "${OUT}" > "${OUT}.sha256"
ls -lh "${OUT}" "${OUT}.sha256"
echo "[package] OK"
