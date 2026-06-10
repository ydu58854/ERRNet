# Contract: ERRNet Improved Retraining Commands

This contract documents the command surface for the approved improved
retraining checkpoint feature. It preserves existing ERRNet script names,
dataset keys, checkpoint format, and metric semantics.

## Full Improved Aligned Retraining

**Command shape**:

```bash
python train_errnet.py \
  --name errnet_improved_retrain_60ep \
  --hyper \
  --pixel_loss_weight 0.2 \
  --gradient_loss_weight 0.4
```

**Working directory**: `ERRNet/`

**Required properties**:
- Non-resumed start: do not pass `-r` or `--resume`.
- Experiment name: `errnet_improved_retrain_60ep`.
- Completion target: existing aligned 60-epoch training protocol.
- Checkpoint output directory:
  `ERRNet/checkpoints/errnet_improved_retrain_60ep/`.
- Baseline checkpoint path must remain unchanged:
  `ERRNet/checkpoints/errnet/errnet_060_00463920.pt`.

**Expected evidence**:
- Exact command and environment record.
- Run log with start/end or completion evidence.
- Final selected checkpoint path.
- Checksum for the final selected checkpoint.
- Note if the target checkpoint directory existed before the run and how it was
  preserved or archived.

## Checkpoint Identity Verification

**Command shape**:

```bash
sha256sum checkpoints/errnet_improved_retrain_60ep/<checkpoint-file>.pt
```

**Working directory**: `ERRNet/`

**Expected evidence**:
- Checksum recorded next to the final checkpoint path.
- Checkpoint is distinct from `checkpoints/errnet/errnet_060_00463920.pt`.
- Checkpoint can be supplied to `test_errnet.py` via `--icnn_path`.
- Final checkpoint selection records filename, mtime, size, and rationale.
- Prefer an explicit epoch-60 checkpoint; use a latest checkpoint only when the
  run log proves it corresponds to epoch 60.

## Checkpoint Load Verification

**Command shape**:

```bash
python test_errnet.py \
  --name errnet_improved_retrain_60ep_loadcheck \
  --dataset ceilnet_table2 \
  -r \
  --icnn_path checkpoints/errnet_improved_retrain_60ep/<checkpoint-file>.pt \
  --hyper \
  --nThreads 0
```

**CPU fallback variant**:

```bash
python test_errnet.py \
  --name errnet_improved_retrain_60ep_loadcheck_cpu \
  --dataset ceilnet_table2 \
  -r \
  --gpu_ids -1 \
  --icnn_path checkpoints/errnet_improved_retrain_60ep/<checkpoint-file>.pt \
  --hyper \
  --nThreads 0
```

**Expected evidence**:
- Command, status, log path, output path, and resource mode are recorded.
- The checkpoint is not marked load-verified until this command or the first
  benchmark evaluation successfully loads it.
- If this command is reused as the first benchmark row, the evidence record
  states that linkage before comparison.

## Improved Benchmark Evaluation

**Command shape**:

```bash
python test_errnet.py \
  --name errnet_improved_retrain_60ep_<dataset_key> \
  --dataset <dataset_key> \
  -r \
  --icnn_path checkpoints/errnet_improved_retrain_60ep/<checkpoint-file>.pt \
  --hyper
```

**Supported dataset keys**:
- `ceilnet_table2`
- `real20`
- `postcard`
- `objects`
- `wild`
- `sir2_withgt`

**Optional resource control**:

```bash
python test_errnet.py \
  --name errnet_improved_retrain_60ep_<dataset_key> \
  --dataset <dataset_key> \
  -r \
  --gpu_ids -1 \
  --icnn_path checkpoints/errnet_improved_retrain_60ep/<checkpoint-file>.pt \
  --hyper \
  --nThreads 0
```

**Expected evidence**:
- Metrics: PSNR, SSIM, NCC, LMSE or a precise unavailable reason for each
  dataset.
- Output path under the existing `ERRNet/results/` convention.
- NaN/inf status and metric semantic notes aligned with spec1 baseline.
- Comparison with the matching baseline row.

## Improved Custom Image Evaluation

**Command shape**:

```bash
python test_errnet.py \
  --name errnet_improved_retrain_60ep_custom \
  --dataset custom \
  --input_dir ../5pictures \
  --max_long_edge 1024 \
  --save_subdir custom_improved_retrain_60ep \
  -r \
  --icnn_path checkpoints/errnet_improved_retrain_60ep/<checkpoint-file>.pt \
  --hyper
```

**Working directory**: `ERRNet/`

**Expected evidence**:
- Output rows for `p1.jpg` through `p5.jpg`.
- Each row records input path, output path, ground-truth status, and qualitative
  comparison note.
- No full-reference metric claim unless paired ground truth is added later.

## Compatibility Requirements

- Existing baseline command surfaces must remain valid.
- Existing default loss behavior must remain compatible.
- If localized model, loss, or training-path code changes are made, run a
  default old-checkpoint inference check after the change.
- Dataset keys, metric names, loader behavior, metric implementation, and
  checkpoint format must not change in this feature.
- New dependencies are not allowed for this feature.
