# Quickstart: ERRNet 单图反射去除课程实验

## 1. Confirm Feature Context

```bash
cat .specify/feature.json
sed -n '1,220p' specs/001-errnet-reflection-spec/spec.md
sed -n '1,260p' specs/001-errnet-reflection-spec/plan.md
```

Expected:
- `feature_directory` points to `specs/001-errnet-reflection-spec`.
- Plan scope preserves existing ERRNet behavior and names concrete files.

## 2. Confirm Data And Weight Readiness

```bash
test -f ERRNet/checkpoints/errnet/errnet_060_00463920.pt
test -d ERRNet/datasets/processed_data
test -f 5pictures/p1.jpg
test -f 5pictures/p2.jpg
test -f 5pictures/p3.jpg
test -f 5pictures/p4.jpg
test -f 5pictures/p5.jpg
```

If processed data is missing, run from `ERRNet/`:

```bash
python datasets/prepare_test_data.py
python datasets/prepare_train_data.py
```

## 3. Record Environment

Run from `ERRNet/`:

```bash
git rev-parse HEAD
python --version
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

Record OS, Python, dependency versions, CUDA/CPU mode, GPU model, and commit id
in the experiment notes.

## 4. Baseline Smoke Evaluation

Run from `ERRNet/`:

```bash
python test_errnet.py --name errnet --dataset ceilnet_table2 -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper
```

CPU fallback:

```bash
python test_errnet.py --name errnet_cpu --dataset ceilnet_table2 -r --gpu_ids -1 --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper
```

Expected:
- Metrics are printed.
- Results are saved under `ERRNet/results/CEILNet_table2/`.

Record metric semantics before using a score in the paper:
- prediction/target alignment and any crop policy
- pixel value range
- ground-truth availability
- mask or valid-pixel policy
- NaN/inf status or blocked reason

## 5. Full Benchmark Evaluation

Run from `ERRNet/`:

```bash
for d in ceilnet_table2 real20 postcard objects wild sir2_withgt; do
  python test_errnet.py --name errnet --dataset "$d" -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper
done
```

Record PSNR, SSIM, NCC, and LMSE for each dataset when available. Each row
must also include metric status, valid ground-truth status, crop/alignment note,
mask or valid-pixel policy, and NaN/inf status.

## 6. Custom Image Evaluation

Run from `ERRNet/`:

```bash
python test_errnet.py --name errnet --dataset custom --input_dir ../5pictures --max_long_edge 1024 -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper
```

Expected:
- Results are saved under `ERRNet/results/custom/`.
- Each of the five custom images has input and output images.
- Report this section as qualitative unless ground truth references are added.

## 7. Improved Method Smoke Path

Before long training, use the future improved experiment name and a short/debug
run where practical. The default planned improvement is a local structural-loss
weight experiment that must preserve baseline defaults.

Expected:
- Existing baseline commands still work unchanged.
- Existing `checkpoints/errnet/errnet_060_00463920.pt` loads and runs default
  inference after any code changes.
- Improved command uses a distinct experiment name.
- Any new option has a documented default and verification impact.
- Changed loss/options/model paths have a CPU import or option-parse smoke
  record with tensor shape, dtype, and device notes.
- Improved outputs exist for `p1.jpg` through `p5.jpg`, or each blocker is
  recorded.

## 8. Final Evidence Checklist

Before claiming completion, collect:
- Environment record.
- Dataset readiness record.
- Baseline benchmark metric table.
- Custom image qualitative output paths.
- Improved-method metric and visual comparison.
- Failure cases and limitations.
- Paper/PPT evidence mapping, code link, weight link, and member contribution
  status. Final paper/PPT authoring, upload, and email submission are outside
  this ERRNet PJ implementation unless requested separately.
