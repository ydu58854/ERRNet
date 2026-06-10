# CLI Contract: Phase C Exclusion-Loss Experiment

## Training Option

### `--lambda_exclusion`

| Property | Contract |
| --- | --- |
| Type | `float` |
| Default | `0.0` |
| Scope | Training commands only |
| Active condition | Greater than `0` |
| Disabled behavior | No exclusion term is added; no `Excl` training error is logged |
| Active behavior | Add `lambda_exclusion * exclusion_loss` to generator loss and log unweighted `Excl` |

## Supported Commands

### Aligned Phase C smoke

```bash
cd ERRNet
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
  python train_errnet.py \
    --name errnet_phaseC_exclusion_smoke \
    --hyper \
    --lambda_exclusion 0.001 \
    --nEpochs 1 \
    --max_dataset_size 2 \
    --nThreads 0 \
    --display_id 0 \
    --save_iter_freq 1
```

### Aligned Phase C longer candidate

```bash
cd ERRNet
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
  python train_errnet.py \
    --name errnet_phaseC_exclusion_lam0001 \
    --hyper \
    --lambda_exclusion 0.001 \
    --pixel_loss_weight 0.2 \
    --gradient_loss_weight 0.4 \
    --save_iter_freq 500
```

### Unaligned Phase C candidate from best Phase B quick-screen source

```bash
cd ERRNet
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
  python train_errnet_unaligned.py \
    --name errnet_phaseC_exclusion_unaligned_lam0001 \
    --hyper \
    -r \
    --icnn_path checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt \
    --unaligned_loss ctx_vgg \
    --lambda_exclusion 0.001 \
    --save_iter_freq 500 \
    --nThreads 0 \
    --display_id 0
```

## Evaluation Contract

Use the existing `test_errnet.py` command shape and the same six benchmark
dataset keys:

```text
ceilnet_table2
real20
postcard
objects
wild
sir2_withgt
```

Outputs must use distinct save subdirectories such as:

```text
phaseC_exclusion_lam0001_<dataset>
phaseC_exclusion_lam0001_custom
```

## Compatibility Contract

- Existing commands that omit `--lambda_exclusion` must continue to run.
- Existing checkpoints must load without requiring the new option.
- No dataset key, metric name, checkpoint field, or result image convention may
  be changed by this feature.
