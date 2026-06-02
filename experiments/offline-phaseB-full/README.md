# Offline Phase B Full Training Scripts

Purpose: run full default unaligned finetuning for the two current clear
candidates:

- `improved + ctx_vgg`
- `improved + ctx`

These scripts are intended for an offline training machine. They do not use
`--max_dataset_size 100` and do not use `--debug`.

## Required Files On The Offline Machine

Run from a copied project tree containing:

```text
ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt
ERRNet/datasets/processed_data/
ERRNet/datasets/raw_data/Dataset/DSLR/unaligned_train250/
5pictures/p1.jpg ... p5.jpg
```

Also ensure VGG19 weights are already cached in the shared project cache:

```text
<PROJECT_ROOT>/.torch/hub/checkpoints/vgg19-dcbb9e9d.pth
```

## Environment Variables

Defaults:

```bash
ENV_NAME=errnet
RUN_ID=20260528_phaseB_full
PROJECT_ROOT=<parent directory of ERRNet>
TORCH_HOME=<PROJECT_ROOT>/.torch
```

Override examples:

```bash
export PROJECT_ROOT=/path/to/数字图像处理
export ENV_NAME=ERRNet
export RUN_ID=20260528_phaseB_full
```

## Run Order

Precheck:

```bash
bash ERRNet/experiments/offline-phaseB-full/00_precheck.sh
```

Two-GPU parallel training:

```bash
GPU_ID=0 bash ERRNet/experiments/offline-phaseB-full/10_train_improved_ctx_vgg_full.sh
GPU_ID=1 bash ERRNet/experiments/offline-phaseB-full/11_train_improved_ctx_full.sh
```

Single-GPU sequential training:

```bash
GPU_ID=0 bash ERRNet/experiments/offline-phaseB-full/10_train_improved_ctx_vgg_full.sh
GPU_ID=0 bash ERRNet/experiments/offline-phaseB-full/11_train_improved_ctx_full.sh
```

Evaluation after both trainings complete:

```bash
GPU_ID=0 bash ERRNet/experiments/offline-phaseB-full/20_eval_phaseB_full_one.sh improved_ctx_vgg 0
GPU_ID=1 bash ERRNet/experiments/offline-phaseB-full/20_eval_phaseB_full_one.sh improved_ctx 1
```

On one GPU:

```bash
bash ERRNet/experiments/offline-phaseB-full/20_eval_phaseB_full_one.sh improved_ctx_vgg 0
bash ERRNet/experiments/offline-phaseB-full/20_eval_phaseB_full_one.sh improved_ctx 0
```

Package artifacts:

```bash
bash ERRNet/experiments/offline-phaseB-full/30_package_phaseB_full.sh
```

Return these files:

```text
ERRNet/phaseB_full_improved_ctx_and_ctx_vgg_20260528_phaseB_full.tar.gz
ERRNet/phaseB_full_improved_ctx_and_ctx_vgg_20260528_phaseB_full.tar.gz.sha256
```

## Output Convention

Checkpoints:

```text
ERRNet/checkpoints/errnet_phaseB_full_improved_ctx_vgg/
ERRNet/checkpoints/errnet_phaseB_full_improved_ctx/
```

Logs:

```text
ERRNet/experiments/run-logs/phaseB_full_*_20260528_phaseB_full.log
ERRNet/experiments/run-logs/phaseB_full_*_20260528_phaseB_full.status
```

Results:

```text
ERRNet/results/phaseB_full_improved_ctx_vgg_<dataset>/
ERRNet/results/phaseB_full_improved_ctx_<dataset>/
ERRNet/results/phaseB_full_improved_ctx_vgg_custom/
ERRNet/results/phaseB_full_improved_ctx_custom/
```
