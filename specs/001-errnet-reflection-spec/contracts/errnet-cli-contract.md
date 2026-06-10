# Contract: ERRNet Experiment Commands

This contract documents the command surfaces the implementation plan relies on.
It preserves existing ERRNet script names, dataset keys, paths, and result
semantics.

## Data Preparation

### Prepare Test Data

**Command shape**:

```bash
python datasets/prepare_test_data.py
```

**Working directory**: `ERRNet/`

**Preconditions**:
- Raw data exists under `ERRNet/datasets/raw_data/`.

**Expected evidence**:
- Processed benchmark directories exist under `ERRNet/datasets/processed_data/`.

### Prepare Training Data

**Command shape**:

```bash
python datasets/prepare_train_data.py
```

**Working directory**: `ERRNet/`

**Preconditions**:
- Raw Pascal VOC and real89 data exist under `ERRNet/datasets/raw_data/`.

**Expected evidence**:
- Processed training directories exist under `ERRNet/datasets/processed_data/`.

## Baseline Benchmark Evaluation

**Command shape**:

```bash
python test_errnet.py --name errnet --dataset <dataset_key> -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper
```

**Supported dataset keys**:
- `ceilnet_table2`
- `real20`
- `postcard`
- `objects`
- `wild`
- `sir2_withgt`

**Optional CPU mode**:

```bash
python test_errnet.py --name errnet_cpu --dataset <dataset_key> -r --gpu_ids -1 --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper
```

**Expected evidence**:
- Result directory under `ERRNet/results/`.
- Metrics printed for datasets with ground truth.
- Saved input/output/target images where the current script supports them.
- Metric evidence records must state prediction/target alignment, crop policy,
  pixel range, ground-truth status, mask or valid-pixel policy, and NaN/inf
  status before scores are used in the paper.

## Custom Image Evaluation

**Command shape**:

```bash
python test_errnet.py --name errnet --dataset custom --input_dir ../5pictures -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper
```

**Optional memory control**:

```bash
python test_errnet.py --name errnet --dataset custom --input_dir ../5pictures --max_long_edge 1024 -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper
```

**Expected evidence**:
- One output folder per custom image under `ERRNet/results/custom/`.
- `m_input.png` and method output image for each custom image.
- Metrics are not expected unless paired ground truth is provided separately.
- Qualitative records must cover `p1.jpg` through `p5.jpg`, or document the
  blocker for each missing output.

## Aligned Training

**Command shape**:

```bash
python train_errnet.py --name <experiment_name> --hyper
```

**Optional CPU mode**:

```bash
python train_errnet.py --name <experiment_name> --hyper --gpu_ids -1
```

**Expected evidence**:
- Checkpoints under `ERRNet/checkpoints/<experiment_name>/`.
- Training log or recorded command/environment in experiment records.
- If optional loss-weight arguments are added, their defaults must match the
  current baseline loss behavior.

## Unaligned Finetuning

**Command shape**:

```bash
python train_errnet_unaligned.py --name <experiment_name> --hyper -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --unaligned_loss vgg
```

**Expected evidence**:
- Finetuned checkpoints under `ERRNet/checkpoints/<experiment_name>/`.
- Recorded loss setting and initial checkpoint path.

## Compatibility Requirements

- Existing commands must remain valid.
- Existing default dataset keys must not be renamed.
- Existing metric names `PSNR`, `SSIM`, `NCC`, and `LMSE` must remain stable.
- Existing baseline checkpoint path must remain usable.
- The existing `ERRNet/checkpoints/errnet/errnet_060_00463920.pt` checkpoint
  must load and run default inference after any loss-option or model reporting
  change.
- Changed loss or model paths must have a CPU import/options smoke record with
  tensor shape, dtype, and device notes.
- New optional arguments, if added later, must default to current behavior.
- Data loader, resize/crop/augmentation, and metric implementation semantics
  must not change unless spec, plan, and tasks are updated first.
- Multi-card or distributed training behavior is not an acceptance target for
  this ERRNet PJ feature; record existing behavior if encountered.
- Final paper/PPT authoring, artifact upload, and submission email are not part
  of this command contract; this feature only records evidence and readiness.
