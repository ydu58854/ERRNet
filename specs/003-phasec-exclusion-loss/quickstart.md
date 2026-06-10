# Quickstart: Phase C Exclusion-Loss Experiment

Run commands from the repository root unless a command starts with `cd ERRNet`.

## 1. Static Checks

```bash
cd ERRNet
python -m py_compile \
  options/errnet/train_options.py \
  models/losses.py \
  models/errnet_model.py
```

## 2. Tensor Smoke

```bash
cd ERRNet
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 python - <<'PY'
import torch
from models.losses import ExclusionLoss

torch.manual_seed(2018)
criterion = ExclusionLoss()
input_tensor = torch.rand(2, 3, 16, 16, requires_grad=False)
output_tensor = torch.rand(2, 3, 16, 16, requires_grad=True)
loss = criterion(output_tensor, input_tensor)
loss.backward()
print("loss", float(loss))
print("finite_loss", bool(torch.isfinite(loss)))
print("finite_grad", bool(torch.isfinite(output_tensor.grad).all()))
PY
```

Expected result: finite non-negative loss and finite gradients.

## 3. Option Check

```bash
cd ERRNet
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
  python train_errnet.py --help | rg "lambda_exclusion"
```

Expected result: help output contains `--lambda_exclusion`.

## 4. Bounded Phase C Smoke Training

```bash
cd ERRNet
RUN_ID=20260529_phaseC_exclusion_smoke
LOG="experiments/run-logs/phaseC_exclusion_smoke_${RUN_ID}.log"
STATUS="experiments/run-logs/phaseC_exclusion_smoke_${RUN_ID}.status"
mkdir -p experiments/run-logs
set +e
timeout --kill-after=20s 180s \
  conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
    python train_errnet.py \
      --name errnet_phaseC_exclusion_smoke \
      --hyper \
      --lambda_exclusion 0.001 \
      --nEpochs 1 \
      --max_dataset_size 2 \
      --nThreads 0 \
      --display_id 0 \
      --save_iter_freq 1 \
  >"${LOG}" 2>&1
status=$?
set -e
printf '%s\n' "$status" > "${STATUS}"
tail -n 40 "${LOG}"
```

Expected result: status `0`, finite `Excl` values, and a saved latest
checkpoint.

## 5. Checkpoint Load Smoke

```bash
cd ERRNet
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
  python test_errnet.py \
    --name errnet_phaseC_exclusion_smoke_load \
    --dataset custom \
    --input_dir ../5pictures \
    --max_long_edge 256 \
    --save_subdir phaseC_exclusion_smoke_load \
    -r \
    --icnn_path checkpoints/errnet_phaseC_exclusion_smoke/errnet_latest.pt \
    --hyper \
    --nThreads 0
```

Expected result: command exits `0` and generates five custom outputs.

## 6. Longer Candidate Evaluation

After a longer Phase C checkpoint exists, evaluate the same six benchmarks as
prior evidence:

```bash
cd ERRNet
for dataset in ceilnet_table2 real20 postcard objects wild sir2_withgt; do
  conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
    python test_errnet.py \
      --name "errnet_phaseC_exclusion_lam0001_${dataset}" \
      --dataset "$dataset" \
      --save_subdir "phaseC_exclusion_lam0001_${dataset}" \
      -r \
      --icnn_path checkpoints/errnet_phaseC_exclusion_lam0001/errnet_060_*.pt \
      --hyper \
      --nThreads 0
done
```

Use exact checkpoint filenames after training completes; do not rely on a glob
in final recorded commands.

## Decision Rule

- Report Phase C as improved only if the six benchmark comparison supports it.
- Report Phase C as mixed if only dataset-specific or custom-image gains appear.
- Reject a checkpoint if tensor scans or metrics show NaN/Inf.
- Do not claim custom-image metrics without paired ground truth.
