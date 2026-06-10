# Quickstart: ERRNet Improved Retraining Checkpoint

## 1. Confirm Active Feature

```bash
cat .specify/feature.json
sed -n '1,220p' specs/002-improved-retraining-checkpoint/spec.md
sed -n '1,260p' specs/002-improved-retraining-checkpoint/plan.md
```

Expected:
- `feature_directory` points to
  `specs/002-improved-retraining-checkpoint`.
- The plan requires non-resumed 60-epoch aligned retraining.
- The checkpoint identity is `errnet_improved_retrain_60ep`.

## 2. Confirm Environment And Data

Run from repository root:

```bash
test -d ERRNet/datasets/processed_data
test -f ERRNet/checkpoints/errnet/errnet_060_00463920.pt
test -f 5pictures/p1.jpg
test -f 5pictures/p2.jpg
test -f 5pictures/p3.jpg
test -f 5pictures/p4.jpg
test -f 5pictures/p5.jpg
```

Run from `ERRNet/`:

```bash
python --version
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
git rev-parse HEAD
```

Record the environment, GPU/CPU mode, seed, and current dirty worktree state
before training.

## 3. Prepare Checkpoint Directory

Run from repository root:

```bash
test ! -e ERRNet/checkpoints/errnet_improved_retrain_60ep
```

If the directory already exists, preserve or archive it before the final run
and record the action in `ERRNet/experiments/results-improved.md`. Do not
overwrite `ERRNet/checkpoints/errnet/errnet_060_00463920.pt`.

## 4. Run Full Improved Retraining

Run from `ERRNet/`:

```bash
python train_errnet.py \
  --name errnet_improved_retrain_60ep \
  --hyper \
  --pixel_loss_weight 0.2 \
  --gradient_loss_weight 0.4 \
  --save_iter_freq 500
```

Required:
- Do not pass `-r` or `--resume`.
- Let the existing aligned training protocol reach epoch 60.
- Capture stdout/stderr to a run log when practical.
- `--save_iter_freq 500` keeps a loadable `latest` checkpoint available during
  long epochs. The final accepted checkpoint still must come from epoch 60.

Expected:
- Checkpoints are saved under
  `ERRNet/checkpoints/errnet_improved_retrain_60ep/`.
- Run evidence distinguishes this from prior smoke-only results.

## 5. Record Final Checkpoint Identity

Choose the final loadable checkpoint file produced by the 60-epoch run. Prefer
an explicit epoch-60 checkpoint; use a latest checkpoint only when the run log
proves it corresponds to epoch 60. Record filename, mtime, size, and rationale,
then run from `ERRNet/`:

```bash
sha256sum checkpoints/errnet_improved_retrain_60ep/<checkpoint-file>.pt
```

Record:
- checkpoint path
- checksum
- producing run name
- completion status
- any partial or archived artifacts

## 6. Verify Checkpoint Loads

Run one actual evaluation-entrypoint load check before treating the checkpoint
as ready for comparison. From `ERRNet/`, replacing `<checkpoint-file>` with the
selected checkpoint:

```bash
python test_errnet.py \
  --name errnet_improved_retrain_60ep_loadcheck \
  --dataset ceilnet_table2 \
  -r \
  --icnn_path "checkpoints/errnet_improved_retrain_60ep/<checkpoint-file>.pt" \
  --hyper \
  --nThreads 0
```

If GPU is unavailable and CPU fallback is used, add:

```bash
--gpu_ids -1
```

Record the command, status, log path, output path, resource mode, and whether
this load check is also counted as the first benchmark evaluation. If the check
fails, do not proceed to comparison until the blocker is recorded and resolved
or accepted as a blocker.

## 7. Evaluate All Benchmarks

Run from `ERRNet/`, replacing `<checkpoint-file>` with the selected checkpoint:

```bash
for d in ceilnet_table2 real20 postcard objects wild sir2_withgt; do
  python test_errnet.py \
    --name "errnet_improved_retrain_60ep_${d}" \
    --dataset "$d" \
    -r \
    --icnn_path "checkpoints/errnet_improved_retrain_60ep/<checkpoint-file>.pt" \
    --hyper
done
```

Record PSNR, SSIM, NCC, LMSE, output path, sample count, NaN/inf status, and
blocker notes for each dataset.

## 8. Evaluate Custom Images

Run from `ERRNet/`:

```bash
python test_errnet.py \
  --name errnet_improved_retrain_60ep_custom \
  --dataset custom \
  --input_dir ../5pictures \
  --max_long_edge 1024 \
  --save_subdir custom_improved_retrain_60ep \
  -r \
  --icnn_path "checkpoints/errnet_improved_retrain_60ep/<checkpoint-file>.pt" \
  --hyper
```

Expected:
- Outputs exist for `p1.jpg` through `p5.jpg`.
- Custom images remain qualitative unless paired ground truth is added.

## 9. Compatibility Checks

If no code changed:

```bash
git diff --check -- specs/002-improved-retraining-checkpoint ERRNet/experiments AGENTS.md
```

If model, loss, or training-path code changed, also run:

```bash
python -m py_compile train_errnet.py engine.py models/base_model.py models/losses.py options/errnet/train_options.py
python test_errnet.py \
  --name errnet_baseline_compat_after_retrain_plan \
  --dataset ceilnet_table2 \
  -r \
  --icnn_path checkpoints/errnet/errnet_060_00463920.pt \
  --hyper \
  --nThreads 0
```

Record default-preservation evidence and old-checkpoint inference results.

## 10. Scope Boundary For Blockers

If full retraining exposes a blocker, classify it before code changes. Localized
model, loss, or training-path fixes may proceed only when they directly unblock
the approved run and preserve defaults. If the blocker requires loader, metric,
architecture, dependency, or baseline checkpoint changes, stop and update the
spec/plan before implementation.

## 11. Update Evidence

Update `ERRNet/experiments/results-improved.md` with:
- full retraining command and status
- checkpoint path and checksum
- six benchmark metrics or blocker reasons
- five custom-image output paths
- comparison with `ERRNet/experiments/results-baseline.md`
- assumptions, risks, and whether results support an improvement claim
