# Improved Method Results

## Status

- Status: `implemented; checkpoint save blocker fixed; epoch-60 checkpoint completed; TODO-002 benchmark evaluation completed; Phase A checkpoint-selection diagnostics completed; Phase B quick-screen unaligned finetuning completed; TODO-006 compact paper/PPT tables completed; Phase B full improved+ctx_vgg epoch-70 evaluation completed; Phase B full fixed epoch-80 evaluations completed; Phase C exclusion-loss smoke completed; Phase C lambda=0.001 10epoch evaluation completed; TODO-003 custom visual review completed`
- Default improved direction: local structural-loss weighting
- Environment reference: `environment.md`
- Baseline comparison reference: `results-baseline.md`
- Full retraining feature: `specs/002-improved-retraining-checkpoint/plan.md`

## Motivation

The approved ERRNet PJ improvement is a local structural-loss weighting
experiment. It exposes the existing aligned pixel-loss MSE and GradientLoss
weights as command-line options so experiments can shift emphasis between
pixel fidelity and edge/structure consistency without changing the network,
loader, metric implementation, data preprocessing, or checkpoint format.

## Baseline Loss Record

| Field | Value |
| --- | --- |
| Current pixel loss | `MultipleLoss([nn.MSELoss(), GradientLoss()], [0.2, 0.4])` |
| Current VGG weight | `lambda_vgg = 0.1` |
| Current GAN weight | `lambda_gan = 0.01` |
| Default compatibility target | New options preserve the values above by default |
| T027 status | completed; confirmed from `ERRNet/models/losses.py` |

## Implemented Touchpoints

| File | Change | Scope Guard |
| --- | --- | --- |
| `ERRNet/options/errnet/train_options.py` | Add optional pixel/gradient loss weights with baseline-compatible defaults | No loader, metric, architecture, or dependency change |
| `ERRNet/models/losses.py` | Parameterize existing `MultipleLoss` weights | Preserve default behavior |
| `ERRNet/models/errnet_model.py` | No change needed | Current reporting already consumes the combined `IPixel` scalar |

## Touchpoint Audit

Reviewed in T010:
- `ERRNet/models/losses.py` defined the aligned pixel loss as
  `MultipleLoss([nn.MSELoss(), GradientLoss()], [0.2, 0.4])` inside
  `init_loss(opt, tensor)`.
- `ERRNet/options/errnet/train_options.py` exposed GAN/VGG loss weights but did
  not expose pixel or gradient weights before this feature.
- `ERRNet/models/errnet_model.py` consumes `loss_dic['t_pixel']` as a single
  scalar `IPixel` term; a separate reporting change was not needed.
- No loader, resize/crop/augmentation, metric implementation, network
  architecture, dependency, or multi-card change was required.
- T028 guard status: no loader, resize/crop/augmentation, or metric
  implementation change was made.

## Option / Import Smoke

| Check | Command / Method | Status | Result / Notes |
| --- | --- | --- | --- |
| Option syntax | `python -m py_compile ERRNet/options/errnet/train_options.py ERRNet/options/errnet/base_options.py ERRNet/options/base_option.py` | completed | passed |
| Loss/model syntax | `python -m py_compile ERRNet/models/losses.py ERRNet/models/errnet_model.py` | completed | passed |
| Option presence | source check for `--pixel_loss_weight` and `--gradient_loss_weight` | completed | both options present |
| Loss weight fallback | source check for `getattr(opt, ..., default)` | completed | defaults preserve `0.2` and `0.4` |
| Runtime import/options smoke | `conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 python train_errnet.py --name errnet_loss_weight_smoke --hyper --pixel_loss_weight 0.2 --gradient_loss_weight 0.4 -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --nThreads 0` | completed | status `0`; log `improved_loss_weight_smoke_20260525.log` |
| Tensor shape/dtype/device | CPU tensor loss smoke in `errnet` env | completed | input shape `(2, 3, 16, 16)`, dtype `torch.float32`, device `cpu`, finite loss, status `0`; log `loss_tensor_smoke_20260525.log` |

## Old Checkpoint Compatibility

| Field | Value |
| --- | --- |
| Checkpoint | `ERRNet/checkpoints/errnet/errnet_060_00463920.pt` |
| Default inference command | `conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 python test_errnet.py --name errnet_cpu_fallback_20260525 --dataset ceilnet_table2 -r --gpu_ids -1 --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper --nThreads 0` |
| Status | completed |
| Result | Existing checkpoint loaded and ran 100/100 CEILNet samples on CPU fallback |
| Metrics | `LMSE 0.0048`, `NCC 0.9808`, `PSNR 27.8767`, `SSIM 0.9407` |
| Log | `ERRNet/experiments/run-logs/cpu_fallback_ceilnet_table2_20260525.log`, status `0` |

## Improved Smoke Run

| Field | Value |
| --- | --- |
| Experiment name | `errnet_loss_weight_smoke` |
| Command | `conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 python train_errnet.py --name errnet_loss_weight_smoke --hyper --pixel_loss_weight 0.2 --gradient_loss_weight 0.4 -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --nThreads 0` |
| Status | completed |
| Output path | `ERRNet/checkpoints/errnet_loss_weight_smoke/` |
| Result | Training entrypoint parsed the new options, loaded the old checkpoint, evaluated CEILNet 100/100, and exited with status `0` |
| Metrics | `LMSE 0.0048`, `NCC 0.9808`, `PSNR 27.8770`, `SSIM 0.9407` |
| Notes | The checkpoint was already at epoch 60, so this smoke did not perform additional training or save a new improved model checkpoint |

## Improved Custom Outputs

Command:

```bash
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 python test_errnet.py --name errnet_custom_improved_default_weights --dataset custom --input_dir ../5pictures --max_long_edge 1024 --save_subdir custom_improved_default_weights -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper --pixel_loss_weight 0.2 --gradient_loss_weight 0.4 --nThreads 0
```

| Image | Input Path | Baseline Output | Improved-Option Output | Status / Notes |
| --- | --- | --- | --- | --- |
| p1 | `5pictures/p1.jpg` | `ERRNet/results/custom_baseline/p1/errnet_custom_baseline.png` | `ERRNet/results/custom_improved_default_weights/p1/errnet_custom_improved_default_weights.png` | completed; qualitative only |
| p2 | `5pictures/p2.jpg` | `ERRNet/results/custom_baseline/p2/errnet_custom_baseline.png` | `ERRNet/results/custom_improved_default_weights/p2/errnet_custom_improved_default_weights.png` | completed; qualitative only |
| p3 | `5pictures/p3.jpg` | `ERRNet/results/custom_baseline/p3/errnet_custom_baseline.png` | `ERRNet/results/custom_improved_default_weights/p3/errnet_custom_improved_default_weights.png` | completed; qualitative only |
| p4 | `5pictures/p4.jpg` | `ERRNet/results/custom_baseline/p4/errnet_custom_baseline.png` | `ERRNet/results/custom_improved_default_weights/p4/errnet_custom_improved_default_weights.png` | completed; qualitative only |
| p5 | `5pictures/p5.jpg` | `ERRNet/results/custom_baseline/p5/errnet_custom_baseline.png` | `ERRNet/results/custom_improved_default_weights/p5/errnet_custom_improved_default_weights.png` | completed; qualitative only |

Log: `ERRNet/experiments/run-logs/custom_improved_default_weights_20260525.log`, status `0`.

## Comparison Evidence

| Dataset / Image | Baseline Evidence | Improved Evidence | Interpretation | Status |
| --- | --- | --- | --- | --- |
| CEILNet benchmark | `PSNR 27.8766`, `SSIM 0.9407`, log `baseline_ceilnet_table2_20260525.log` | `PSNR 27.8770`, `SSIM 0.9407`, log `improved_loss_weight_smoke_20260525.log` | Runtime compatibility confirmed with default-compatible weights; no quality-improvement claim because no new training occurred | completed |
| p1 | `custom_baseline/p1/errnet_custom_baseline.png` | `custom_improved_default_weights/p1/errnet_custom_improved_default_weights.png` | Both outputs generated; qualitative visual review completed in TODO-003 section | completed |
| p2 | `custom_baseline/p2/errnet_custom_baseline.png` | `custom_improved_default_weights/p2/errnet_custom_improved_default_weights.png` | Both outputs generated; qualitative visual review completed in TODO-003 section | completed |
| p3 | `custom_baseline/p3/errnet_custom_baseline.png` | `custom_improved_default_weights/p3/errnet_custom_improved_default_weights.png` | Both outputs generated; qualitative visual review completed in TODO-003 section | completed |
| p4 | `custom_baseline/p4/errnet_custom_baseline.png` | `custom_improved_default_weights/p4/errnet_custom_improved_default_weights.png` | Both outputs generated; qualitative visual review completed in TODO-003 section | completed |
| p5 | `custom_baseline/p5/errnet_custom_baseline.png` | `custom_improved_default_weights/p5/errnet_custom_improved_default_weights.png` | Both outputs generated; qualitative visual review completed in TODO-003 section | completed |

## Full Retraining Checkpoint Result

This section records the implementation evidence for
`specs/002-improved-retraining-checkpoint/`. It is separate from the earlier
improved-option smoke evidence above because the spec requires a new 60 epoch
checkpoint and checkpoint-dependent evaluation evidence.

### Run Summary

| Field | Value |
| --- | --- |
| Experiment name | `errnet_improved_retrain_60ep` |
| Working directory | `ERRNet/` |
| Required command | `conda run -n ERRNet python train_errnet.py --name errnet_improved_retrain_60ep --hyper --pixel_loss_weight 0.2 --gradient_loss_weight 0.4 --save_iter_freq 500` |
| Planned log | `ERRNet/experiments/run-logs/improved_retrain_60ep_20260526.log` naming pattern |
| Actual start-validation log | `ERRNet/experiments/run-logs/improved_retrain_60ep_attempt_20260526.log` |
| Long-run window | First start-validation began `2026-05-26T19:08:50+08:00`; final epoch-60 checkpoint mtime `2026-05-27T02:42:58+08:00` |
| Completion status | `completed` - explicit epoch-60 checkpoint exists and was selected for evaluation |
| Final checkpoint | `ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt` |
| Training note | The canonical run reached epoch 60 after resuming its own in-progress checkpoint state; final evidence uses the explicit epoch-60 file, not an interim `latest` checkpoint |
| Residual risk | Course/report claims must use the measured benchmark rows below; results are mixed and do not support a blanket quality-improvement claim |

The final `opt.txt` and start-validation records confirm the run configuration:

| Option | Observed Value |
| --- | --- |
| `name` | `errnet_improved_retrain_60ep` |
| `hyper` | `True` |
| `pixel_loss_weight` | `0.2` |
| `gradient_loss_weight` | `0.4` |
| `nEpochs` | `60` |
| `resume` | `True` in the final `opt.txt` because the long run was resumed from its own partial checkpoint after interruption; the initial start-validation command was recorded without `-r` |
| `resume_epoch` | `None` |
| `gpu_ids` | `[0]` |
| `seed` | `2018` |
| `save_iter_freq` | `500` for the fixed full-run command; default `0` preserves original epoch-only behavior |

### Environment And Data Readiness

| Check | Status | Evidence / Notes |
| --- | --- | --- |
| Python environment | completed | `/opt/conda/envs/ERRNet/bin/python` |
| Required packages | completed | `pip install -r ERRNet/requirements.txt` in the existing `ERRNet` environment; this synchronized already-declared dependencies and did not modify source or training config files |
| PyTorch/CUDA | completed | `torch` present; CUDA available; one `NVIDIA GeForce RTX 4090` device |
| VGG19 weights | completed | `Vgg19(requires_grad=False)` loaded after caching `vgg19-dcbb9e9d.pth` |
| CPU fallback | not exercised for final checkpoint | Final benchmark evaluation used single-card CUDA; prior baseline CPU fallback remains recorded in `results-baseline.md` |
| Training data | completed | `VOC2012_224_train_png.txt` has `15287` entries; synthetic train length `7643`; real train length `89`; fused epoch length `7732`; estimated full run `463920` iterations |
| Benchmark data | completed | Required processed datasets are present: `testdata_CEILNET_table2`, `real20`, `postcard`, `objects`, `wild`, `sir2_withgt` |
| Custom images | completed | `5pictures/p1.jpg` through `5pictures/p5.jpg` are present |
| Baseline checkpoint | completed | `ERRNet/checkpoints/errnet/errnet_060_00463920.pt`, size `346772498` bytes, SHA256 `96146622142fe7c515f260024018704a4b0bba4f3940e84cfe9451e408a9b567` |
| Git/worktree scope | completed | Worktree was already dirty before this implementation; current implementation edits are limited to experiment/spec evidence and generated run artifacts |

### Static Implementation Review

| Area | Finding | Status |
| --- | --- | --- |
| `ERRNet/train_errnet.py` | Uses `./datasets/processed_data`, constructs synthetic/real `FusionDataset`, disables GAN before epoch 20, and loops while `engine.epoch < 60` | compatible |
| `ERRNet/engine.py` | Creates `checkpoints/<name>/`; saves epoch checkpoints every `save_epoch_freq=10`, saves `latest` after each completed epoch, and now supports optional iteration-based `latest` saves | fixed |
| `ERRNet/models/base_model.py` | Saves `.pt` files through a `.tmp` file and `os.replace` so interrupted writes do not overwrite the last complete checkpoint | fixed |
| `ERRNet/options/errnet/train_options.py` | Exposes `--pixel_loss_weight` default `0.2`, `--gradient_loss_weight` default `0.4`, and `--save_iter_freq` default `0` | fixed |
| `ERRNet/models/losses.py` | Builds the aligned pixel term as `MultipleLoss([nn.MSELoss(), GradientLoss()], [pixel_loss_weight, gradient_loss_weight])` | compatible |
| `ERRNet/test_errnet.py` | Supports benchmark keys `ceilnet_table2`, `real20`, `postcard`, `objects`, `wild`, `sir2_withgt` and `custom` input evaluation with `--icnn_path` | compatible |
| Source changes in this pass | Localized training/checkpoint save fix only: `train_errnet.py`, `engine.py`, `models/base_model.py`, `options/errnet/train_options.py` | compatible |

### Checkpoint Identity

| Artifact | Status | Evidence |
| --- | --- | --- |
| Target directory | present | `ERRNet/checkpoints/errnet_improved_retrain_60ep/` |
| `opt.txt` | present | `925` bytes; records the final run options, including `nEpochs=60`, `pixel_loss_weight=0.2`, `gradient_loss_weight=0.4`, `save_iter_freq=500` |
| `loss_log.txt` | present | `375` bytes; training session headers were written during the long run/resume attempts |
| Periodic checkpoints | present | `errnet_010_00077320.pt`, `errnet_020_00161428.pt`, `errnet_030_00238748.pt`, `errnet_040_00316068.pt`, `errnet_050_00393388.pt`, `errnet_060_00470708.pt` |
| Selected final checkpoint | completed | `ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt`; explicit epoch-60 file preferred over `errnet_latest.pt` |
| Selected checkpoint metadata | completed | size `346898110` bytes; mtime `2026-05-27 02:42:58.083785947 +0800`; checkpoint load metadata `epoch=60` |
| New checkpoint checksum | completed | SHA256 `9214c1bd66e38350d99c99c02dd2fbceb626b15e50d66c1f3df1bf3a14c7073d` |
| `errnet_latest.pt` comparison | recorded | size `346894086` bytes; mtime `2026-05-27 02:42:59.963954006 +0800`; SHA256 `6051a2701731a66cc516bacd01e5141df1d4017ebad623220c55a0fc8ca5db35`; checkpoint load metadata `epoch=60` |
| Actual load verification | completed | First TODO-002 benchmark evaluation loaded the selected checkpoint; `ceilnet_table2` log line `Resume from epoch 60, iteration 470708`; status `0` |
| Baseline preservation | completed | Baseline checkpoint remains present and distinct under `ERRNet/checkpoints/errnet/` |

### Evaluation Commands And Measured Results

TODO-002 benchmark evaluation used the selected explicit epoch-60 checkpoint
from `ERRNet/`:

```bash
CKPT=checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt
RUN_TS=20260527_0245
```

Benchmark evaluation command pattern:

```bash
for d in ceilnet_table2 real20 postcard objects wild sir2_withgt; do
  conda run --no-capture-output -n ERRNet python test_errnet.py \
    --name "errnet_improved_retrain_60ep_${d}" \
    --dataset "$d" \
    --save_subdir "improved_retrain_60ep_${d}" \
    -r \
    --icnn_path "$CKPT" \
    --hyper \
    --nThreads 0 \
    2>&1 | tee "experiments/run-logs/improved_retrain_60ep_eval_${d}_${RUN_TS}.log"
  echo "${PIPESTATUS[0]}" > "experiments/run-logs/improved_retrain_60ep_eval_${d}_${RUN_TS}.status"
done
```

Benchmark command, log, and output map:

| Dataset | Samples | Command | Log | Output Path |
| --- | ---: | --- | --- | --- |
| `ceilnet_table2` | 100 | `conda run --no-capture-output -n ERRNet python test_errnet.py --name errnet_improved_retrain_60ep_ceilnet_table2 --dataset ceilnet_table2 --save_subdir improved_retrain_60ep_ceilnet_table2 -r --icnn_path checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt --hyper --nThreads 0` | `ERRNet/experiments/run-logs/improved_retrain_60ep_eval_ceilnet_table2_20260527_0245.log` | `ERRNet/results/improved_retrain_60ep_ceilnet_table2/*/errnet_improved_retrain_60ep_ceilnet_table2.png` |
| `real20` | 20 | `conda run --no-capture-output -n ERRNet python test_errnet.py --name errnet_improved_retrain_60ep_real20 --dataset real20 --save_subdir improved_retrain_60ep_real20 -r --icnn_path checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt --hyper --nThreads 0` | `ERRNet/experiments/run-logs/improved_retrain_60ep_eval_real20_20260527_0245.log` | `ERRNet/results/improved_retrain_60ep_real20/*/errnet_improved_retrain_60ep_real20.png` |
| `postcard` | 179 | `conda run --no-capture-output -n ERRNet python test_errnet.py --name errnet_improved_retrain_60ep_postcard --dataset postcard --save_subdir improved_retrain_60ep_postcard -r --icnn_path checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt --hyper --nThreads 0` | `ERRNet/experiments/run-logs/improved_retrain_60ep_eval_postcard_20260527_0245.log` | `ERRNet/results/improved_retrain_60ep_postcard/*/errnet_improved_retrain_60ep_postcard.png` |
| `objects` | 200 | `conda run --no-capture-output -n ERRNet python test_errnet.py --name errnet_improved_retrain_60ep_objects --dataset objects --save_subdir improved_retrain_60ep_objects -r --icnn_path checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt --hyper --nThreads 0` | `ERRNet/experiments/run-logs/improved_retrain_60ep_eval_objects_20260527_0245.log` | `ERRNet/results/improved_retrain_60ep_objects/*/errnet_improved_retrain_60ep_objects.png` |
| `wild` | 101 | `conda run --no-capture-output -n ERRNet python test_errnet.py --name errnet_improved_retrain_60ep_wild --dataset wild --save_subdir improved_retrain_60ep_wild -r --icnn_path checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt --hyper --nThreads 0` | `ERRNet/experiments/run-logs/improved_retrain_60ep_eval_wild_20260527_0245.log` | `ERRNet/results/improved_retrain_60ep_wild/*/errnet_improved_retrain_60ep_wild.png` |
| `sir2_withgt` | 480 | `conda run --no-capture-output -n ERRNet python test_errnet.py --name errnet_improved_retrain_60ep_sir2_withgt --dataset sir2_withgt --save_subdir improved_retrain_60ep_sir2_withgt -r --icnn_path checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt --hyper --nThreads 0` | `ERRNet/experiments/run-logs/improved_retrain_60ep_eval_sir2_withgt_20260527_0245.log` | `ERRNet/results/improved_retrain_60ep_sir2_withgt/*/errnet_improved_retrain_60ep_sir2_withgt.png` |

Benchmark result table:

| Method | Dataset | Samples | Output Count | PSNR | SSIM | NCC | LMSE | Metric Status | NaN/inf | Log | Blocker |
| --- | --- | ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| ERRNet improved retrain | `ceilnet_table2` | 100 | 100 | 27.8476 | 0.9410 | 0.9798 | 0.0047 | measured, status `0` | none observed | `ERRNet/experiments/run-logs/improved_retrain_60ep_eval_ceilnet_table2_20260527_0245.log` | none |
| ERRNet improved retrain | `real20` | 20 | 20 | 23.7577 | 0.8268 | 0.8935 | 0.0190 | measured, status `0` | none observed | `ERRNet/experiments/run-logs/improved_retrain_60ep_eval_real20_20260527_0245.log` | none |
| ERRNet improved retrain | `postcard` | 179 | 179 | 21.6580 | 0.8795 | 0.9384 | 0.0044 | measured, status `0` | none observed | `ERRNet/experiments/run-logs/improved_retrain_60ep_eval_postcard_20260527_0245.log` | none |
| ERRNet improved retrain | `objects` | 200 | 200 | 24.4328 | 0.8942 | 0.9820 | 0.0032 | measured, status `0` | none observed | `ERRNet/experiments/run-logs/improved_retrain_60ep_eval_objects_20260527_0245.log` | none |
| ERRNet improved retrain | `wild` | 101 | 101 | 25.1643 | 0.8864 | 0.9420 | 0.0069 | measured, status `0` | none observed | `ERRNet/experiments/run-logs/improved_retrain_60ep_eval_wild_20260527_0245.log` | none |
| ERRNet improved retrain | `sir2_withgt` | 480 | 480 | 23.5517 | 0.8871 | 0.9573 | 0.0044 | measured, status `0` | none observed | `ERRNet/experiments/run-logs/improved_retrain_60ep_eval_sir2_withgt_20260527_0245.log` | none |

NaN/inf status is recorded as `none observed` because all six commands exited
with status `0`, emitted finite final metric rows, and produced the expected
per-dataset output counts.

Custom-image evaluation with the selected checkpoint was run as T044. It is
qualitative because the custom images do not include paired ground truth.

```bash
conda run --no-capture-output -n ERRNet python test_errnet.py \
  --name errnet_improved_retrain_60ep_custom \
  --dataset custom \
  --input_dir ../5pictures \
  --max_long_edge 1024 \
  --save_subdir custom_improved_retrain_60ep \
  -r \
  --icnn_path "$CKPT" \
  --hyper \
  --nThreads 0 \
  2>&1 | tee "experiments/run-logs/improved_retrain_60ep_custom_20260527_032534.log"
```

| Image | Input Path | Improved Retrain Output | GT Status | Visual Status | Blocker / Review Note |
| --- | --- | --- | --- | --- | --- |
| p1 | `5pictures/p1.jpg` | `ERRNet/results/custom_improved_retrain_60ep/p1/errnet_improved_retrain_60ep_custom.png` | unavailable | reviewed; see TODO-003 section | status `0`; PNG opens, size `768x1024`; log `improved_retrain_60ep_custom_20260527_032534.log` |
| p2 | `5pictures/p2.jpg` | `ERRNet/results/custom_improved_retrain_60ep/p2/errnet_improved_retrain_60ep_custom.png` | unavailable | reviewed; see TODO-003 section | status `0`; PNG opens, size `768x1024`; log `improved_retrain_60ep_custom_20260527_032534.log` |
| p3 | `5pictures/p3.jpg` | `ERRNet/results/custom_improved_retrain_60ep/p3/errnet_improved_retrain_60ep_custom.png` | unavailable | reviewed; see TODO-003 section | status `0`; PNG opens, size `1024x768`; log `improved_retrain_60ep_custom_20260527_032534.log` |
| p4 | `5pictures/p4.jpg` | `ERRNet/results/custom_improved_retrain_60ep/p4/errnet_improved_retrain_60ep_custom.png` | unavailable | reviewed; see TODO-003 section | status `0`; PNG opens, size `768x1024`; log `improved_retrain_60ep_custom_20260527_032534.log` |
| p5 | `5pictures/p5.jpg` | `ERRNet/results/custom_improved_retrain_60ep/p5/errnet_improved_retrain_60ep_custom.png` | unavailable | reviewed; see TODO-003 section | status `0`; PNG opens, size `772x1024`; log `improved_retrain_60ep_custom_20260527_032534.log` |

### Comparison And Claim Status

| Dataset / Image | Baseline Evidence | Full-Retrain Improved Evidence | Delta / Interpretation |
| --- | --- | --- | --- |
| `ceilnet_table2` | PSNR 27.8766, SSIM 0.9407, NCC 0.9808, LMSE 0.0048 | PSNR 27.8476, SSIM 0.9410, NCC 0.9798, LMSE 0.0047 | PSNR -0.0290, SSIM +0.0003, NCC -0.0010, LMSE -0.0001; mixed |
| `real20` | PSNR 23.5531, SSIM 0.8285, NCC 0.8877, LMSE 0.0201 | PSNR 23.7577, SSIM 0.8268, NCC 0.8935, LMSE 0.0190 | PSNR +0.2046, SSIM -0.0017, NCC +0.0058, LMSE -0.0011; mostly improved except SSIM |
| `postcard` | PSNR 22.0710, SSIM 0.8773, NCC 0.9463, LMSE 0.0044 | PSNR 21.6580, SSIM 0.8795, NCC 0.9384, LMSE 0.0044 | PSNR -0.4130, SSIM +0.0022, NCC -0.0079, LMSE 0.0000; mixed |
| `objects` | PSNR 24.8530, SSIM 0.8980, NCC 0.9817, LMSE 0.0029 | PSNR 24.4328, SSIM 0.8942, NCC 0.9820, LMSE 0.0032 | PSNR -0.4202, SSIM -0.0038, NCC +0.0003, LMSE +0.0003; mostly worse |
| `wild` | PSNR 25.1761, SSIM 0.8861, NCC 0.9359, LMSE 0.0083 | PSNR 25.1643, SSIM 0.8864, NCC 0.9420, LMSE 0.0069 | PSNR -0.0118, SSIM +0.0003, NCC +0.0061, LMSE -0.0014; mixed, structure metrics improved |
| `sir2_withgt` | PSNR 23.8836, SSIM 0.8878, NCC 0.9589, LMSE 0.0046 | PSNR 23.5517, SSIM 0.8871, NCC 0.9573, LMSE 0.0044 | PSNR -0.3319, SSIM -0.0007, NCC -0.0016, LMSE -0.0002; mixed |
| p1-p5 | baseline and improved-option smoke outputs exist | full-retrain custom outputs generated | qualitative visual review completed; success/failure selections recorded in TODO-003 section |

Overall claim status: `inconclusive`. The full retrained checkpoint is
loadable and evaluated on all six TODO-002 benchmarks, but the metrics are
mixed: PSNR drops on four datasets, while some SSIM/NCC/LMSE values improve on
selected datasets. The report can cite the measured tradeoff, but should not
claim a broad quality improvement.

### Phase A Checkpoint Selection Diagnostics

Phase A from `improvement.md` was run on 2026-05-27 to test whether the current
result is mainly caused by selecting epoch 60 poorly. No training or source
change was made for this diagnostic pass. The same six benchmark keys, metric
implementation, data root, hypercolumn setting, and single-card CUDA path were
used for every checkpoint.

Command pattern:

```bash
cd ERRNet
RUN_TS=20260527_phaseA
for spec in \
  10:errnet_010_00077320.pt \
  20:errnet_020_00161428.pt \
  30:errnet_030_00238748.pt \
  40:errnet_040_00316068.pt \
  50:errnet_050_00393388.pt \
  60:errnet_060_00470708.pt
do
  ep=${spec%%:*}
  file=${spec#*:}
  ckpt="checkpoints/errnet_improved_retrain_60ep/${file}"
  for d in ceilnet_table2 real20 postcard objects wild sir2_withgt; do
    conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
      python test_errnet.py \
        --name "errnet_phaseA_ep${ep}_${d}" \
        --dataset "$d" \
        --save_subdir "phaseA_ep${ep}_${d}" \
        -r \
        --icnn_path "$ckpt" \
        --hyper \
        --nThreads 0 \
        > "experiments/run-logs/phaseA_ep${ep}_${d}_${RUN_TS}.log" 2>&1
    printf '%s\n' "$?" \
      > "experiments/run-logs/phaseA_ep${ep}_${d}_${RUN_TS}.status"
  done
done
```

Checkpoint identities:

| Epoch | Checkpoint | SHA256 |
| ---: | --- | --- |
| 10 | `ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_010_00077320.pt` | `ed667850889e8d7093ae1a3a122eab3e6f228e346f9da764546caa8955ad109d` |
| 20 | `ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_020_00161428.pt` | `7632b7c45c6ae20d1f31952aa563baafc28f49da0976187aed82461b02a5163b` |
| 30 | `ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_030_00238748.pt` | `d573446574da3ed903346c2e4e67e02fbe1d57dfce75c53e327411f2623835a1` |
| 40 | `ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_040_00316068.pt` | `1566bca90da4a1e5dfec54a40779c17cea12f9d8076a380d2b3755fe18401492` |
| 50 | `ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_050_00393388.pt` | `a05f3f746edb0a22757a4307e8a3a3e64897ee3f16c0cef7724b2e90d7a3c1de` |
| 60 | `ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt` | `9214c1bd66e38350d99c99c02dd2fbceb626b15e50d66c1f3df1bf3a14c7073d` |

Full benchmark table:

| Epoch | Dataset | Samples | Output Count | PSNR | SSIM | NCC | LMSE | Status |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 10 | `ceilnet_table2` | 100 | 100 | 22.7529 | 0.8889 | 0.9481 | 0.0089 | `0` |
| 10 | `real20` | 20 | 20 | 20.4004 | 0.7603 | 0.8456 | 0.0247 | `0` |
| 10 | `postcard` | 179 | 179 | 15.5341 | 0.8104 | 0.8826 | 0.0063 | `0` |
| 10 | `objects` | 200 | 200 | 19.4252 | 0.8655 | 0.9476 | 0.0060 | `0` |
| 10 | `wild` | 101 | 101 | 21.7612 | 0.8757 | 0.9144 | 0.0076 | `0` |
| 10 | `sir2_withgt` | 480 | 480 | 18.4657 | 0.8471 | 0.9164 | 0.0065 | `0` |
| 20 | `ceilnet_table2` | 100 | 100 | 25.1093 | 0.9117 | 0.9659 | 0.0065 | `0` |
| 20 | `real20` | 20 | 20 | 22.0746 | 0.7945 | 0.8712 | 0.0235 | `0` |
| 20 | `postcard` | 179 | 179 | 18.8396 | 0.8489 | 0.9028 | 0.0066 | `0` |
| 20 | `objects` | 200 | 200 | 22.8770 | 0.8945 | 0.9736 | 0.0039 | `0` |
| 20 | `wild` | 101 | 101 | 24.3790 | 0.9034 | 0.9391 | 0.0069 | `0` |
| 20 | `sir2_withgt` | 480 | 480 | 21.6874 | 0.8794 | 0.9399 | 0.0055 | `0` |
| 30 | `ceilnet_table2` | 100 | 100 | 25.6214 | 0.9246 | 0.9696 | 0.0060 | `0` |
| 30 | `real20` | 20 | 20 | 22.3558 | 0.8087 | 0.8834 | 0.0215 | `0` |
| 30 | `postcard` | 179 | 179 | 19.9815 | 0.8530 | 0.9217 | 0.0060 | `0` |
| 30 | `objects` | 200 | 200 | 24.3926 | 0.9007 | 0.9786 | 0.0034 | `0` |
| 30 | `wild` | 101 | 101 | 24.2443 | 0.8771 | 0.9380 | 0.0078 | `0` |
| 30 | `sir2_withgt` | 480 | 480 | 22.7164 | 0.8780 | 0.9489 | 0.0053 | `0` |
| 40 | `ceilnet_table2` | 100 | 100 | 25.8712 | 0.9293 | 0.9748 | 0.0063 | `0` |
| 40 | `real20` | 20 | 20 | 23.1693 | 0.8218 | 0.8896 | 0.0213 | `0` |
| 40 | `postcard` | 179 | 179 | 20.5121 | 0.8692 | 0.9385 | 0.0050 | `0` |
| 40 | `objects` | 200 | 200 | 24.4395 | 0.9044 | 0.9797 | 0.0029 | `0` |
| 40 | `wild` | 101 | 101 | 24.4557 | 0.8736 | 0.9369 | 0.0082 | `0` |
| 40 | `sir2_withgt` | 480 | 480 | 22.9783 | 0.8848 | 0.9553 | 0.0048 | `0` |
| 50 | `ceilnet_table2` | 100 | 100 | 26.5043 | 0.9324 | 0.9759 | 0.0050 | `0` |
| 50 | `real20` | 20 | 20 | 23.6714 | 0.8279 | 0.8944 | 0.0193 | `0` |
| 50 | `postcard` | 179 | 179 | 21.0422 | 0.8728 | 0.9308 | 0.0045 | `0` |
| 50 | `objects` | 200 | 200 | 24.5034 | 0.8978 | 0.9817 | 0.0032 | `0` |
| 50 | `wild` | 101 | 101 | 24.1528 | 0.8697 | 0.9327 | 0.0088 | `0` |
| 50 | `sir2_withgt` | 480 | 480 | 23.1389 | 0.8826 | 0.9524 | 0.0049 | `0` |
| 60 | `ceilnet_table2` | 100 | 100 | 27.8490 | 0.9410 | 0.9798 | 0.0047 | `0` |
| 60 | `real20` | 20 | 20 | 23.7578 | 0.8268 | 0.8935 | 0.0190 | `0` |
| 60 | `postcard` | 179 | 179 | 21.6585 | 0.8795 | 0.9384 | 0.0044 | `0` |
| 60 | `objects` | 200 | 200 | 24.4318 | 0.8942 | 0.9820 | 0.0032 | `0` |
| 60 | `wild` | 101 | 101 | 25.1631 | 0.8864 | 0.9420 | 0.0069 | `0` |
| 60 | `sir2_withgt` | 480 | 480 | 23.5517 | 0.8871 | 0.9573 | 0.0044 | `0` |

Aggregate and selection table:

| Epoch | Avg PSNR | Avg SSIM | Avg NCC | Avg LMSE | PSNR wins vs ep60 | SSIM wins vs ep60 | NCC wins vs ep60 | LMSE wins vs ep60 | Datasets with >=2 metrics better than ep60 | Datasets with >=2 metrics better than baseline |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 19.7233 | 0.8413 | 0.9091 | 0.0100 | 0 | 0 | 0 | 0 | 0 | 0 |
| 20 | 22.4945 | 0.8721 | 0.9321 | 0.0088 | 0 | 2 | 0 | 0 | 0 | 1 |
| 30 | 23.2187 | 0.8737 | 0.9400 | 0.0083 | 0 | 1 | 0 | 0 | 0 | 1 |
| 40 | 23.5710 | 0.8805 | 0.9458 | 0.0081 | 1 | 1 | 1 | 1 | 1 | 1 |
| 50 | 23.8355 | 0.8805 | 0.9446 | 0.0076 | 1 | 2 | 1 | 0 | 2 | 1 |
| 60 | 24.4020 | 0.8858 | 0.9488 | 0.0071 | 0 | 0 | 0 | 0 | 0 | 3 |

Per-dataset best metric check:

| Dataset | Best PSNR | Best SSIM | Best NCC | Best LMSE |
| --- | --- | --- | --- | --- |
| `ceilnet_table2` | ep60 `27.8490` | ep60 `0.9410` | ep60 `0.9798` | ep60 `0.0047` |
| `real20` | ep60 `23.7578` | ep50 `0.8279` | ep50 `0.8944` | ep60 `0.0190` |
| `postcard` | ep60 `21.6585` | ep60 `0.8795` | ep40 `0.9385` | ep60 `0.0044` |
| `objects` | ep50 `24.5034` | ep40 `0.9044` | ep60 `0.9820` | ep40 `0.0029` |
| `wild` | ep60 `25.1631` | ep20 `0.9034` | ep60 `0.9420` | ep20 `0.0069` |
| `sir2_withgt` | ep60 `23.5517` | ep60 `0.8871` | ep60 `0.9573` | ep60 `0.0044` |

Phase A decision:

- Selected checkpoint remains epoch 60:
  `ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt`.
- Epoch 60 has the best equal-weight average PSNR, SSIM, NCC, and LMSE across
  the six benchmarks.
- No middle checkpoint satisfies the Phase A adoption rules from
  `improvement.md`: none has average PSNR higher than epoch 60; none is
  consistently better on `objects`/`postcard`/`sir2_withgt`; none reaches
  `4/6` datasets with at least two metrics better than baseline.
- Epoch 40 and epoch 50 are useful diagnostic references for isolated metrics:
  epoch 40 is best for `objects` SSIM/LMSE and `postcard` NCC; epoch 50 is best
  for `real20` SSIM/NCC and `objects` PSNR. These isolated wins do not offset
  epoch 60's stronger aggregate behavior.
- Conclusion: the current difficulty is not explained by poor epoch-60
  checkpoint selection alone. Epoch 60 is the best or most balanced checkpoint
  within the existing aligned retraining run, but it still does not support a
  blanket improvement claim over the baseline.

Phase A verification:

| Check | Status | Evidence |
| --- | --- | --- |
| Run completion | passed | 36 `phaseA_*_20260527_phaseA.status` files; all contain `0` |
| Metric extraction | passed | 36 logs contain finite final PSNR/SSIM/NCC/LMSE rows |
| Output counts | passed | Each `ERRNet/results/phaseA_epXX_<dataset>/` output count matches the expected sample count: 100, 20, 179, 200, 101, or 480 |
| NaN/inf scan | passed | `rg -i --pcre2 '(^|[^a-z])(nan|inf)([^a-z]|$)' ERRNet/experiments/run-logs/phaseA_*_20260527_phaseA.log` returned no matches |
| Scope guard | passed | No model, training, loader, metric, dataset, or checkpoint file was changed for Phase A; only evaluation logs/results and documentation were generated |

### Phase B Quick-Screen Unaligned Finetuning

Phase B from `improvement.md` was run on 2026-05-27 to verify ERRNet's
misaligned real-data path with the existing `train_errnet_unaligned.py`
entrypoint. This is a quick-screen matrix, not a full default-data training
claim: to keep the six-run matrix tractable, `--max_dataset_size 100` was used.
The real unaligned path remained enabled with all `250` blended files and
`250` transmission files under `datasets/raw_data/Dataset/DSLR/unaligned_train250`;
the fusion dataset reported `389 [50, 250, 89]` samples with ratio
`[0.25, 0.5, 0.25]`. The `50` synthetic samples are a consequence of the
current `CEILDataset` split behavior under this cap.

Training command pattern:

```bash
cd ERRNet
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
  python train_errnet_unaligned.py \
    --name "errnet_phaseB_quick_${origin}_${loss}" \
    --hyper \
    -r \
    --icnn_path "$ckpt" \
    --unaligned_loss "$loss" \
    --max_dataset_size 100 \
    --nThreads 0 \
    --display_id 0 \
    --save_iter_freq 500 \
    --no-verbose \
    --no-log \
    --no_html
```

Evaluation command pattern:

```bash
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
  python test_errnet.py \
    --name "errnet_phaseB_quick_${origin}_${loss}_${dataset}" \
    --dataset "$dataset" \
    --save_subdir "phaseB_quick_${origin}_${loss}_${dataset}" \
    -r \
    --icnn_path "$phaseb_ckpt" \
    --hyper \
    --nThreads 0
```

Source checkpoints:

| Source | Checkpoint | SHA256 |
| --- | --- | --- |
| `baseline` | `ERRNet/checkpoints/errnet/errnet_060_00463920.pt` | `96146622142fe7c515f260024018704a4b0bba4f3940e84cfe9451e408a9b567` |
| `improved` | `ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt` | `9214c1bd66e38350d99c99c02dd2fbceb626b15e50d66c1f3df1bf3a14c7073d` |

Phase B checkpoint identities:

| Source | `unaligned_loss` | Checkpoint | Epoch / Iterations | SHA256 |
| --- | --- | --- | --- | --- |
| `baseline` | `vgg` | `ERRNet/checkpoints/errnet_phaseB_quick_baseline_vgg/errnet_080_00471700.pt` | `80 / 471700` | `0f7a93437d51ed5928acfb593225a6bba7d5153123aedcc400f9beb5a1e55479` |
| `baseline` | `ctx` | `ERRNet/checkpoints/errnet_phaseB_quick_baseline_ctx/errnet_080_00471700.pt` | `80 / 471700` | `1e6da3c0336d6f05db32103e18adbf96b59eb2ca55b5ee7676fa174580f0e121` |
| `baseline` | `ctx_vgg` | `ERRNet/checkpoints/errnet_phaseB_quick_baseline_ctx_vgg/errnet_080_00471700.pt` | `80 / 471700` | `39095107fd91bc45df98c397bf3a12cf82213b1cac92aa792b8bd1ce0d26ffa9` |
| `improved` | `vgg` | `ERRNet/checkpoints/errnet_phaseB_quick_improved_vgg/errnet_080_00478488.pt` | `80 / 478488` | `f6bee61355c322d052bcc2823c66531eaa63e9f1d6e11f77485c44f5d77421cc` |
| `improved` | `ctx` | `ERRNet/checkpoints/errnet_phaseB_quick_improved_ctx/errnet_080_00478488.pt` | `80 / 478488` | `4e9ddcc7aa2e2b59db133af90775109e1e238209d18098bbaaf7cde6ea2eda12` |
| `improved` | `ctx_vgg` | `ERRNet/checkpoints/errnet_phaseB_quick_improved_ctx_vgg/errnet_080_00478488.pt` | `80 / 478488` | `e411b97856399eb8b009b0d2f67240aec2749290c6a7171450c1bd81d88849ea` |

Equal-weight average across the six benchmark datasets:

| Source | Loss | Avg PSNR | Delta PSNR vs Source | Avg SSIM | Delta SSIM | Avg NCC | Delta NCC | Avg LMSE | Delta LMSE |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `vgg` | 24.3251 | -0.2438 | 0.8832 | -0.0032 | 0.9477 | -0.0008 | 0.0075 | +0.0000 |
| `baseline` | `ctx` | 24.3954 | -0.1735 | 0.8834 | -0.0030 | 0.9474 | -0.0012 | 0.0077 | +0.0002 |
| `baseline` | `ctx_vgg` | 24.2022 | -0.3667 | 0.8834 | -0.0030 | 0.9467 | -0.0019 | 0.0077 | +0.0001 |
| `improved` | `vgg` | 24.0962 | -0.3058 | 0.8815 | -0.0043 | 0.9439 | -0.0049 | 0.0076 | +0.0005 |
| `improved` | `ctx` | 24.2992 | -0.1028 | 0.8854 | -0.0004 | 0.9445 | -0.0043 | 0.0072 | +0.0001 |
| `improved` | `ctx_vgg` | 24.3502 | -0.0518 | 0.8868 | +0.0010 | 0.9469 | -0.0020 | 0.0069 | -0.0002 |

TODO-006 paper/PPT compact tables:

These tables compress the 36 benchmark rows into report-ready evidence.
All deltas are measured against the corresponding source checkpoint
(`baseline` or aligned `improved`), and lower LMSE is better. This remains a
quick-screen result because the training used `--max_dataset_size 100`, not the
full default unaligned training schedule.

Recommended compact average table:

| Start checkpoint | Loss | Avg PSNR | ΔPSNR | Avg SSIM | ΔSSIM | Avg NCC | ΔNCC | Avg LMSE | ΔLMSE | PPT note |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `baseline` | `vgg` | 24.3251 | -0.2438 | 0.8832 | -0.0032 | 0.9477 | -0.0008 | 0.0075 | +0.0000 | baseline-source LMSE best/tie |
| `baseline` | `ctx` | 24.3954 | -0.1735 | 0.8834 | -0.0030 | 0.9474 | -0.0012 | 0.0077 | +0.0002 | baseline-source PSNR best |
| `baseline` | `ctx_vgg` | 24.2022 | -0.3667 | 0.8834 | -0.0030 | 0.9467 | -0.0019 | 0.0077 | +0.0001 | no average win |
| `improved` | `vgg` | 24.0962 | -0.3058 | 0.8815 | -0.0043 | 0.9439 | -0.0049 | 0.0076 | +0.0005 | no average win |
| `improved` | `ctx` | 24.2992 | -0.1028 | 0.8854 | -0.0004 | 0.9445 | -0.0043 | 0.0072 | +0.0001 | strong `wild` signal |
| `improved` | `ctx_vgg` | 24.3502 | -0.0518 | 0.8868 | +0.0010 | 0.9469 | -0.0020 | 0.0069 | -0.0002 | best quick-screen candidate |

Source-level best loss summary:

| Start checkpoint | Best Avg PSNR | Best Avg SSIM | Best Avg NCC | Best Avg LMSE | Suggested wording |
| --- | --- | --- | --- | --- | --- |
| `baseline` | `ctx` 24.3954 | `ctx`/`ctx_vgg` 0.8834 | `vgg` 0.9477 | `vgg` 0.0075 | Baseline-source finetuning did not beat the original baseline on average. |
| `improved` | `ctx_vgg` 24.3502 | `ctx_vgg` 0.8868 | `ctx_vgg` 0.9469 | `ctx_vgg` 0.0069 | `improved + ctx_vgg` is the best compact candidate, mainly from SSIM/LMSE. |

`wild` dataset highlight:

| Start checkpoint | Loss | PSNR | ΔPSNR | SSIM | ΔSSIM | NCC | ΔNCC | LMSE | ΔLMSE | Takeaway |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `baseline` | `vgg` | 24.7370 | -0.4391 | 0.8921 | +0.0060 | 0.9362 | +0.0003 | 0.0071 | -0.0012 | structure/LMSE improves, PSNR drops |
| `baseline` | `ctx` | 25.1734 | -0.0027 | 0.8946 | +0.0085 | 0.9440 | +0.0081 | 0.0083 | +0.0000 | strongest baseline-source `wild` balance |
| `baseline` | `ctx_vgg` | 24.4337 | -0.7424 | 0.8870 | +0.0009 | 0.9334 | -0.0025 | 0.0088 | +0.0005 | not preferred |
| `improved` | `vgg` | 24.8432 | -0.3211 | 0.8881 | +0.0017 | 0.9402 | -0.0018 | 0.0069 | +0.0000 | limited gain |
| `improved` | `ctx` | 25.4125 | +0.2482 | 0.9061 | +0.0197 | 0.9497 | +0.0077 | 0.0049 | -0.0020 | all four metrics improve |
| `improved` | `ctx_vgg` | 25.2924 | +0.1281 | 0.9080 | +0.0216 | 0.9521 | +0.0101 | 0.0047 | -0.0022 | best structure/LMSE signal |

`ceilnet_table2` limitation for slides:

| Start checkpoint | Best quick-screen loss on `ceilnet_table2` by PSNR | PSNR | ΔPSNR | SSIM | ΔSSIM | NCC | ΔNCC | LMSE | ΔLMSE | Slide takeaway |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `baseline` | `ctx_vgg` | 27.3318 | -0.5448 | 0.9362 | -0.0045 | 0.9772 | -0.0036 | 0.0050 | +0.0002 | even the best loss drops PSNR/SSIM/NCC |
| `improved` | `ctx_vgg` | 27.2098 | -0.6378 | 0.9360 | -0.0050 | 0.9767 | -0.0031 | 0.0050 | +0.0003 | quick-screen has a clear synthetic-table risk |

Paper/PPT wording:

```text
Phase B quick-screen used the original ERRNet unaligned finetuning path with
a capped synthetic subset (`--max_dataset_size 100`, fusion dataset
389 [50, 250, 89]). The compact six-run matrix selected improved + ctx_vgg:
it had the smallest average PSNR drop, the only positive average SSIM delta,
and the best average LMSE. The strongest positive signal appeared on wild,
where improved + ctx and improved + ctx_vgg improved all four metrics. However,
ceilnet_table2 consistently degraded, so this evidence supports a candidate
screening result rather than a broad full-reference improvement claim.
```

Full benchmark table:

| Source | Loss | Dataset | Samples | Output Count | PSNR | SSIM | NCC | LMSE | Delta PSNR vs Source | Delta SSIM | Delta NCC | Delta LMSE |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `vgg` | `ceilnet_table2` | 100 | 100 | 27.2393 | 0.9355 | 0.9777 | 0.0048 | -0.6373 | -0.0052 | -0.0031 | +0.0000 |
| `baseline` | `vgg` | `real20` | 20 | 20 | 23.7692 | 0.8282 | 0.8933 | 0.0203 | +0.2161 | -0.0003 | +0.0056 | +0.0002 |
| `baseline` | `vgg` | `postcard` | 179 | 179 | 22.2904 | 0.8654 | 0.9410 | 0.0050 | +0.2194 | -0.0119 | -0.0053 | +0.0006 |
| `baseline` | `vgg` | `objects` | 200 | 200 | 24.2803 | 0.8948 | 0.9814 | 0.0032 | -0.5727 | -0.0032 | -0.0003 | +0.0003 |
| `baseline` | `vgg` | `wild` | 101 | 101 | 24.7370 | 0.8921 | 0.9362 | 0.0071 | -0.4391 | +0.0060 | +0.0003 | -0.0012 |
| `baseline` | `vgg` | `sir2_withgt` | 480 | 480 | 23.6343 | 0.8833 | 0.9568 | 0.0047 | -0.2493 | -0.0045 | -0.0021 | +0.0001 |
| `baseline` | `ctx` | `ceilnet_table2` | 100 | 100 | 27.2830 | 0.9364 | 0.9775 | 0.0049 | -0.5936 | -0.0043 | -0.0033 | +0.0001 |
| `baseline` | `ctx` | `real20` | 20 | 20 | 23.4039 | 0.8301 | 0.8922 | 0.0197 | -0.1492 | +0.0016 | +0.0045 | -0.0004 |
| `baseline` | `ctx` | `postcard` | 179 | 179 | 22.1296 | 0.8602 | 0.9329 | 0.0055 | +0.0586 | -0.0171 | -0.0134 | +0.0011 |
| `baseline` | `ctx` | `objects` | 200 | 200 | 24.5879 | 0.8964 | 0.9819 | 0.0029 | -0.2651 | -0.0016 | +0.0002 | +0.0000 |
| `baseline` | `ctx` | `wild` | 101 | 101 | 25.1734 | 0.8946 | 0.9440 | 0.0083 | -0.0027 | +0.0085 | +0.0081 | +0.0000 |
| `baseline` | `ctx` | `sir2_withgt` | 480 | 480 | 23.7943 | 0.8825 | 0.9556 | 0.0050 | -0.0893 | -0.0053 | -0.0033 | +0.0004 |
| `baseline` | `ctx_vgg` | `ceilnet_table2` | 100 | 100 | 27.3318 | 0.9362 | 0.9772 | 0.0050 | -0.5448 | -0.0045 | -0.0036 | +0.0002 |
| `baseline` | `ctx_vgg` | `real20` | 20 | 20 | 23.3947 | 0.8301 | 0.8940 | 0.0196 | -0.1584 | +0.0016 | +0.0063 | -0.0005 |
| `baseline` | `ctx_vgg` | `postcard` | 179 | 179 | 22.2977 | 0.8685 | 0.9371 | 0.0047 | +0.2267 | -0.0088 | -0.0092 | +0.0003 |
| `baseline` | `ctx_vgg` | `objects` | 200 | 200 | 24.2111 | 0.8949 | 0.9829 | 0.0030 | -0.6419 | -0.0031 | +0.0012 | +0.0001 |
| `baseline` | `ctx_vgg` | `wild` | 101 | 101 | 24.4337 | 0.8870 | 0.9334 | 0.0088 | -0.7424 | +0.0009 | -0.0025 | +0.0005 |
| `baseline` | `ctx_vgg` | `sir2_withgt` | 480 | 480 | 23.5444 | 0.8834 | 0.9554 | 0.0048 | -0.3392 | -0.0044 | -0.0035 | +0.0002 |
| `improved` | `vgg` | `ceilnet_table2` | 100 | 100 | 27.0257 | 0.9361 | 0.9769 | 0.0052 | -0.8219 | -0.0049 | -0.0029 | +0.0005 |
| `improved` | `vgg` | `real20` | 20 | 20 | 23.3427 | 0.8213 | 0.8863 | 0.0203 | -0.4150 | -0.0055 | -0.0072 | +0.0013 |
| `improved` | `vgg` | `postcard` | 179 | 179 | 21.3137 | 0.8598 | 0.9275 | 0.0055 | -0.3443 | -0.0197 | -0.0109 | +0.0011 |
| `improved` | `vgg` | `objects` | 200 | 200 | 24.6185 | 0.9009 | 0.9804 | 0.0030 | +0.1857 | +0.0067 | -0.0016 | -0.0002 |
| `improved` | `vgg` | `wild` | 101 | 101 | 24.8432 | 0.8881 | 0.9402 | 0.0069 | -0.3211 | +0.0017 | -0.0018 | +0.0000 |
| `improved` | `vgg` | `sir2_withgt` | 480 | 480 | 23.4333 | 0.8829 | 0.9522 | 0.0047 | -0.1184 | -0.0042 | -0.0051 | +0.0003 |
| `improved` | `ctx` | `ceilnet_table2` | 100 | 100 | 27.1910 | 0.9362 | 0.9773 | 0.0050 | -0.6566 | -0.0048 | -0.0025 | +0.0003 |
| `improved` | `ctx` | `real20` | 20 | 20 | 23.3186 | 0.8245 | 0.8859 | 0.0203 | -0.4391 | -0.0023 | -0.0076 | +0.0013 |
| `improved` | `ctx` | `postcard` | 179 | 179 | 21.6022 | 0.8618 | 0.9202 | 0.0055 | -0.0558 | -0.0177 | -0.0182 | +0.0011 |
| `improved` | `ctx` | `objects` | 200 | 200 | 24.6125 | 0.8979 | 0.9820 | 0.0029 | +0.1797 | +0.0037 | +0.0000 | -0.0003 |
| `improved` | `ctx` | `wild` | 101 | 101 | 25.4125 | 0.9061 | 0.9497 | 0.0049 | +0.2482 | +0.0197 | +0.0077 | -0.0020 |
| `improved` | `ctx` | `sir2_withgt` | 480 | 480 | 23.6583 | 0.8862 | 0.9521 | 0.0043 | +0.1066 | -0.0009 | -0.0052 | -0.0001 |
| `improved` | `ctx_vgg` | `ceilnet_table2` | 100 | 100 | 27.2098 | 0.9360 | 0.9767 | 0.0050 | -0.6378 | -0.0050 | -0.0031 | +0.0003 |
| `improved` | `ctx_vgg` | `real20` | 20 | 20 | 23.2890 | 0.8227 | 0.8879 | 0.0197 | -0.4687 | -0.0041 | -0.0056 | +0.0007 |
| `improved` | `ctx_vgg` | `postcard` | 179 | 179 | 22.0188 | 0.8683 | 0.9268 | 0.0051 | +0.3608 | -0.0112 | -0.0116 | +0.0007 |
| `improved` | `ctx_vgg` | `objects` | 200 | 200 | 24.5353 | 0.8971 | 0.9825 | 0.0030 | +0.1025 | +0.0029 | +0.0005 | -0.0002 |
| `improved` | `ctx_vgg` | `wild` | 101 | 101 | 25.2924 | 0.9080 | 0.9521 | 0.0047 | +0.1281 | +0.0216 | +0.0101 | -0.0022 |
| `improved` | `ctx_vgg` | `sir2_withgt` | 480 | 480 | 23.7562 | 0.8887 | 0.9553 | 0.0041 | +0.2045 | +0.0016 | -0.0020 | -0.0003 |

Best Phase B quick-screen loss by PSNR:

| Source | `ceilnet_table2` | `real20` | `postcard` | `objects` | `wild` | `sir2_withgt` |
| --- | --- | --- | --- | --- | --- | --- |
| `baseline` | `ctx_vgg` | `vgg` | `ctx_vgg` | `ctx` | `ctx` | `ctx` |
| `improved` | `ctx_vgg` | `vgg` | `ctx_vgg` | `vgg` | `ctx` | `ctx_vgg` |

Custom-image qualitative outputs:

| Source | Loss | Output Directory | Output Count | Log |
| --- | --- | --- | ---: | --- |
| `baseline` | `vgg` | `ERRNet/results/phaseB_quick_baseline_vgg_custom/` | 5 | `ERRNet/experiments/run-logs/phaseB_quick_custom_baseline_vgg_20260527_phaseB_quick.log` |
| `baseline` | `ctx` | `ERRNet/results/phaseB_quick_baseline_ctx_custom/` | 5 | `ERRNet/experiments/run-logs/phaseB_quick_custom_baseline_ctx_20260527_phaseB_quick.log` |
| `baseline` | `ctx_vgg` | `ERRNet/results/phaseB_quick_baseline_ctx_vgg_custom/` | 5 | `ERRNet/experiments/run-logs/phaseB_quick_custom_baseline_ctx_vgg_20260527_phaseB_quick.log` |
| `improved` | `vgg` | `ERRNet/results/phaseB_quick_improved_vgg_custom/` | 5 | `ERRNet/experiments/run-logs/phaseB_quick_custom_improved_vgg_20260527_phaseB_quick.log` |
| `improved` | `ctx` | `ERRNet/results/phaseB_quick_improved_ctx_custom/` | 5 | `ERRNet/experiments/run-logs/phaseB_quick_custom_improved_ctx_20260527_phaseB_quick.log` |
| `improved` | `ctx_vgg` | `ERRNet/results/phaseB_quick_improved_ctx_vgg_custom/` | 5 | `ERRNet/experiments/run-logs/phaseB_quick_custom_improved_ctx_vgg_20260527_phaseB_quick.log` |

Phase B quick-screen decision:

- The best average result in this quick-screen matrix is `improved + ctx_vgg`:
  it has the smallest average PSNR drop from its source checkpoint
  (`-0.0518`), the only positive average SSIM delta (`+0.0010`), and the best
  average LMSE (`0.0069`, delta `-0.0002`).
- From the baseline source, `ctx` has the best average PSNR, while `vgg` has
  the lowest average LMSE tie. None of the baseline-source quick-screen runs
  improves the equal-weight average PSNR/SSIM/NCC over the baseline source.
- The most consistent positive signal is on `wild`, especially from the
  improved source with `ctx` or `ctx_vgg`: both improve PSNR, SSIM, NCC, and
  LMSE relative to the aligned improved checkpoint.
- `ceilnet_table2` consistently drops after unaligned quick-screen finetuning.
  This is expected risk for a real-data finetuning path and prevents a broad
  full-reference improvement claim.
- These results are useful screening evidence for the ERRNet paper path, but
  they are not a final full-training claim. A report should call this
  `Phase B quick-screen` unless the full default unaligned matrix is later run.

Phase B verification:

| Check | Status | Evidence |
| --- | --- | --- |
| Training completion | passed | 6 `phaseB_quick_train_*_20260527_phaseB_quick.status` files; all contain `0` |
| Checkpoint metadata | passed | Six selected checkpoints load with `epoch=80`; baseline-source iterations `471700`, improved-source iterations `478488` |
| Benchmark completion | passed | 36 `phaseB_quick_eval_*_20260527_phaseB_quick.status` files; all contain `0` |
| Metric extraction | passed | 36 logs contain finite final PSNR/SSIM/NCC/LMSE rows |
| Output counts | passed | All benchmark output counts match expected samples: 100, 20, 179, 200, 101, or 480 |
| Custom outputs | passed | 6 custom runs completed with status `0`; each generated five outputs for `5pictures/p1.jpg` through `p5.jpg` |
| Scope guard | passed | No model, loader, metric, architecture, dataset, or source code was changed for Phase B; only checkpoints, evaluation outputs, logs, and documentation were generated |

### Phase B Full Default-Data `improved + ctx_vgg`

The full default-data unaligned finetuning candidate `improved + ctx_vgg` was
tested on 2026-05-28. It starts from
`ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt` and
does not use the quick-screen `--max_dataset_size 100` cap.

Checkpoint health:

| Checkpoint | Epoch / Iteration | SHA256 | Tensor Scan | Decision |
| --- | --- | --- | --- | --- |
| `ERRNet/checkpoints/errnet_phaseB_full_improved_ctx_vgg/errnet_070_00550528.pt` | `70 / 550528` | `a8d31b4fd7e9626ffeaa40b57a7d79f6d1007ac1b818a3a374f081e6b1e762d0` | `0 / 164` scanned floating tensors contain non-finite values | selected for evaluation |
| `ERRNet/checkpoints/errnet_phaseB_full_improved_ctx_vgg/errnet_080_00630348.pt` | `80 / 630348` | `f955f4a894a5b8730a894efa4e6a1f55773560eeea00b28040d3083ecdd77917` | `164 / 164` scanned floating tensors contain non-finite values | rejected |
| `ERRNet/checkpoints/errnet_phaseB_full_improved_ctx_vgg/errnet_latest.pt` | `80 / 630348` | `c9de4974dbeb9c88149722a461271aa2d044c0d27881b3af685d34223902bbc3` | `164 / 164` scanned floating tensors contain non-finite values | rejected |

The first epoch-80 evaluation attempt produced NaN metrics on
`ceilnet_table2` and `real20`, with
`RuntimeWarning: invalid value encountered in cast` in
`ERRNet/models/errnet_model.py`. The test script can still exit `0` on NaN
metrics, so the epoch-80/latest checkpoint is not usable evidence.

Epoch-70 benchmark results:

| Dataset | Samples / Model Outputs | PSNR | SSIM | NCC | LMSE |
| --- | ---: | ---: | ---: | ---: | ---: |
| `ceilnet_table2` | 100 | 26.2052 | 0.9290 | 0.9728 | 0.0059 |
| `real20` | 20 | 23.2336 | 0.8169 | 0.8911 | 0.0208 |
| `postcard` | 179 | 22.5143 | 0.8724 | 0.9392 | 0.0051 |
| `objects` | 200 | 24.7004 | 0.8988 | 0.9810 | 0.0034 |
| `wild` | 101 | 25.0299 | 0.9047 | 0.9494 | 0.0053 |
| `sir2_withgt` | 480 | 23.9545 | 0.8902 | 0.9588 | 0.0044 |
| **Equal-weight average** | - | **24.2730** | **0.8853** | **0.9487** | **0.0075** |

Average deltas:

| Reference | ΔPSNR | ΔSSIM | ΔNCC | ΔLMSE |
| --- | ---: | ---: | ---: | ---: |
| Baseline checkpoint | -0.2959 | -0.0011 | +0.0002 | -0.0000 |
| Aligned improved epoch 60 | -0.1290 | -0.0005 | -0.0001 | +0.0004 |

Interpretation:

- Full default-data `improved + ctx_vgg` did not strengthen the broad
  improvement claim. The usable epoch-70 checkpoint has lower average PSNR and
  SSIM than both baseline and aligned improved epoch 60.
- The best signal remains dataset-specific: `wild` improves SSIM, NCC, and
  LMSE relative to both references, while `sir2_withgt` improves PSNR and SSIM.
- `ceilnet_table2` and `real20` regress strongly, so this full run should be
  reported as unstable/mixed rather than as a final improvement.
- This result is retained as historical unstable-run evidence. The repaired
  `improved + ctx_vgg_fixed` continuation and the rerun `improved + ctx_fixed`
  full candidate are recorded in the follow-up fixed epoch-80 section below.

Full-run verification:

| Check | Status | Evidence |
| --- | --- | --- |
| Epoch-70 benchmark completion | passed | Six `phaseB_full_eval_improved_ctx_vgg_ep70_*_20260528_phaseB_full_ep70.status` files contain `0` |
| Metric extraction | passed | Six epoch-70 logs contain finite final PSNR/SSIM/NCC/LMSE rows |
| Output counts | passed | Model output counts match expected samples: `100`, `20`, `179`, `200`, `101`, `480`; total PNG counts include saved inputs/labels |
| Custom output | passed | `ERRNet/results/phaseB_full_improved_ctx_vgg_ep70_custom/` contains five model outputs for `p1` through `p5`; image integrity check opened 10 PNGs including saved inputs |
| Checkpoint rejection | passed | Epoch-80/latest tensor scan and NaN metric logs justify rejecting final/latest full checkpoint |
| Follow-up fixed candidates | completed later | See the `Phase B Full Fixed Epoch-80 Candidates` section for repaired `ctx_vgg_fixed` and rerun `ctx_fixed` evidence |
| Scope guard | passed | No model, loader, metric, architecture, dataset, or source code was changed for this evaluation |

### Phase B Full Fixed Epoch-80 Candidates

After the CX stability fix, the repaired full default-data runs completed on
2026-05-29. Both runs use full unaligned finetuning without the quick-screen
`--max_dataset_size 100` cap. `ctx_vgg_fixed` resumes the last healthy original
`ctx_vgg` epoch-70 checkpoint; `ctx_fixed` reruns the second full candidate from
the aligned improved epoch-60 checkpoint.

Checkpoint health:

| Candidate | Checkpoint | Epoch / Iteration | SHA256 | Tensor Scan | Decision |
| --- | --- | ---: | --- | --- | --- |
| `improved + ctx_vgg_fixed` | `ERRNet/checkpoints/errnet_phaseB_full_improved_ctx_vgg_fixed/errnet_080_00632892.pt` | `80 / 632892` | `e6548656158bae2ecfb5b5266f65478f53bf75099f189810227a6db21ec10b29` | `656` tensors / `86671568` elements scanned; `0` non-finite | selected for evaluation |
| `improved + ctx_fixed` | `ERRNet/checkpoints/errnet_phaseB_full_improved_ctx_fixed/errnet_080_00630348.pt` | `80 / 630348` | `8336989c5ad655b8387f2c264878a7c0dd766f838c721263a353ce5a5bbe3013` | `656` tensors / `86671568` elements scanned; `0` non-finite | selected for evaluation |

Run evidence:

| Candidate | Training Log | Tensor Scan Log | Evaluation Logs | Custom Outputs | Status |
| --- | --- | --- | --- | --- | --- |
| `improved + ctx_vgg_fixed` | `ERRNet/experiments/run-logs/phaseB_full_train_improved_ctx_vgg_fixed_20260529_resume2_tmux.log` | `ERRNet/experiments/run-logs/phaseB_full_tensor_scan_improved_ctx_vgg_fixed_20260529_phaseB_full_fixed.log` | `ERRNet/experiments/run-logs/phaseB_full_eval_improved_ctx_vgg_fixed_<dataset>_20260529_phaseB_full_fixed.log` | `ERRNet/results/phaseB_full_improved_ctx_vgg_fixed_custom/` | train, tensor scan, six benchmarks, and custom all status `0` |
| `improved + ctx_fixed` | `ERRNet/experiments/run-logs/phaseB_full_train_improved_ctx_fixed_20260529_resume_tmux.log` | `ERRNet/experiments/run-logs/phaseB_full_tensor_scan_improved_ctx_fixed_20260529_phaseB_full_fixed.log` | `ERRNet/experiments/run-logs/phaseB_full_eval_improved_ctx_fixed_<dataset>_20260529_phaseB_full_fixed.log` | `ERRNet/results/phaseB_full_improved_ctx_fixed_custom/` | train, tensor scan, six benchmarks, and custom all status `0` |

Benchmark results:

| Candidate | Dataset | Samples / Model Outputs | PSNR | SSIM | NCC | LMSE |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `improved + ctx_vgg_fixed` | `ceilnet_table2` | 100 | 27.0464 | 0.9350 | 0.9760 | 0.0051 |
| `improved + ctx_vgg_fixed` | `real20` | 20 | 23.3249 | 0.8166 | 0.8946 | 0.0204 |
| `improved + ctx_vgg_fixed` | `postcard` | 179 | 22.3702 | 0.8680 | 0.9341 | 0.0050 |
| `improved + ctx_vgg_fixed` | `objects` | 200 | 24.4260 | 0.8933 | 0.9826 | 0.0036 |
| `improved + ctx_vgg_fixed` | `wild` | 101 | 23.8224 | 0.8947 | 0.9482 | 0.0055 |
| `improved + ctx_vgg_fixed` | `sir2_withgt` | 480 | 23.5324 | 0.8841 | 0.9573 | 0.0045 |
| **`improved + ctx_vgg_fixed` average** | - | - | **24.0870** | **0.8820** | **0.9488** | **0.0074** |
| `improved + ctx_fixed` | `ceilnet_table2` | 100 | 27.1630 | 0.9359 | 0.9761 | 0.0049 |
| `improved + ctx_fixed` | `real20` | 20 | 23.0743 | 0.8144 | 0.8893 | 0.0204 |
| `improved + ctx_fixed` | `postcard` | 179 | 22.2167 | 0.8637 | 0.9273 | 0.0055 |
| `improved + ctx_fixed` | `objects` | 200 | 24.4627 | 0.8936 | 0.9830 | 0.0034 |
| `improved + ctx_fixed` | `wild` | 101 | 23.7641 | 0.8907 | 0.9455 | 0.0058 |
| `improved + ctx_fixed` | `sir2_withgt` | 480 | 23.4781 | 0.8819 | 0.9543 | 0.0047 |
| **`improved + ctx_fixed` average** | - | - | **24.0265** | **0.8800** | **0.9459** | **0.0075** |

Average deltas:

| Candidate | Reference | ΔPSNR | ΔSSIM | ΔNCC | ΔLMSE |
| --- | --- | ---: | ---: | ---: | ---: |
| `improved + ctx_vgg_fixed` | Baseline checkpoint | -0.4819 | -0.0044 | +0.0002 | -0.0002 |
| `improved + ctx_vgg_fixed` | Aligned improved epoch 60 | -0.3150 | -0.0039 | +0.0000 | +0.0003 |
| `improved + ctx_fixed` | Baseline checkpoint | -0.5424 | -0.0064 | -0.0026 | -0.0001 |
| `improved + ctx_fixed` | Aligned improved epoch 60 | -0.3755 | -0.0058 | -0.0029 | +0.0003 |

Interpretation:

- The CX stability fix solved the previous non-finite checkpoint failure for
  this continuation: both epoch-80 checkpoints are finite and all evaluation
  status files are `0`.
- The fixed full default-data results are still mixed. Neither candidate
  improves the equal-weight PSNR/SSIM average over the baseline or aligned
  improved epoch-60 checkpoint.
- `improved + ctx_vgg_fixed` is the better of the two fixed full candidates by
  average PSNR/SSIM/NCC/LMSE, but it remains below the quick-screen candidate and
  below the baseline/aligned improved averages on PSNR and SSIM.
- The strongest positive dataset-specific signal is still partial: `wild`
  improves SSIM/NCC/LMSE against baseline, and `postcard` improves PSNR against
  baseline, but the result is not broad enough for an overall improvement claim.

Fixed-run verification:

| Check | Status | Evidence |
| --- | --- | --- |
| Training completion | passed | Training logs save epoch 80 checkpoints and end with `status=0`; both `.status` files contain `0` |
| Checkpoint tensor scan | passed | Both tensor scan logs report `nonfinite_tensors: 0`, `nonfinite_elements: 0`, and `result: finite` |
| Benchmark completion | passed | Twelve benchmark `.status` files contain `0`; logs contain finite final PSNR/SSIM/NCC/LMSE rows |
| Output counts | passed | Model output counts match expected samples: `100`, `20`, `179`, `200`, `101`, `480` for both candidates |
| Custom outputs | passed | Both custom runs completed with status `0` and generated five model outputs |
| Log anomaly scan | passed | No `Traceback`, `RuntimeError`, `Killed`, or `invalid value` lines were found in the fixed-run tensor/evaluation logs |
| Scope guard | passed | No model, loader, metric, architecture, dataset, or source code was changed for this evaluation pass |

### Phase C Exclusion-Loss Smoke

Phase C opens a new default-disabled loss experiment. It adds
`--lambda_exclusion`, default `0.0`, and uses `input - output` as a residual
proxy for a transmission/residual gradient exclusion penalty. Phase D data
strategy remains out of scope for this feature.

Implementation scope:

| File | Change | Scope Guard |
| --- | --- | --- |
| `ERRNet/options/errnet/train_options.py` | Add `--lambda_exclusion`, default `0.0` | Existing commands omit it and preserve behavior |
| `ERRNet/models/losses.py` | Add finite `ExclusionLoss` using normalized absolute gradients | No new dependency or tensor input |
| `ERRNet/models/errnet_model.py` | Add weighted `Excl` term only when `lambda_exclusion > 0` | No architecture, loader, metric, or checkpoint schema change |
| `ERRNet/train_errnet.py` | Use existing `--nEpochs` value in the training loop | Default remains `60`; enables bounded smoke runs |

Smoke evidence:

| Check | Status | Evidence |
| --- | --- | --- |
| Syntax check | passed | `conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 python -m py_compile options/errnet/train_options.py models/losses.py models/errnet_model.py` |
| Option/default check | passed | `train_errnet.py --help` includes `--lambda_exclusion`; parser default is `0.0` |
| Tensor finite check | passed | `ExclusionLoss` returned finite random-tensor loss `2.3723862171173096`, finite gradients, and constant-tensor loss `0.0` |
| Bounded training smoke | passed | `ERRNet/experiments/run-logs/phaseC_exclusion_smoke_20260529_phaseC_exclusion_smoke_n1.status` contains `0`; log records finite `Excl` values |
| Smoke checkpoint | passed | `ERRNet/checkpoints/errnet_phaseC_exclusion_smoke/errnet_latest.pt`, epoch `1`, iterations `90`, SHA256 `c9a24c43994c0beb708b6ed781e987edc80f13b9aadea4474be840d29609cc26` |
| Checkpoint load/custom inference | passed | `ERRNet/experiments/run-logs/phaseC_exclusion_smoke_load_20260529_phaseC_exclusion_smoke_load.status` contains `0`; `ERRNet/results/phaseC_exclusion_smoke_load/` contains five model outputs |
| Baseline checkpoint compatibility | passed | `ERRNet/experiments/run-logs/phaseC_baseline_compat_20260529_phaseC_baseline_compat.status` contains `0`; old baseline checkpoint generated five custom outputs with default `lambda_exclusion=0.0` |
| Log anomaly scan | passed | No `Traceback`, `RuntimeError`, `Killed`, `invalid value`, `nan`, or `inf` lines found in Phase C smoke/load logs |

Decision:

- Phase C code path is open and smoke-verified.
- This smoke checkpoint is not quality evidence and must not be used for an
  improvement claim.
- The first longer Phase C run used `lambda_exclusion=0.001` for 10 epochs; the
  result is recorded below.
- Phase D data strategy still needs a separate feature plan before modifying
  dataset generation, loader, crop/resize, augmentation, or curriculum
  semantics.

### Phase C Lambda 0.001 10-Epoch Candidate

The requested Phase C candidate was trained with:

```bash
cd ERRNet
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
  python train_errnet.py \
    --name errnet_phaseC_exclusion_lam0001_10ep \
    --hyper \
    --lambda_exclusion 0.001 \
    --nEpochs 10 \
    --save_iter_freq 500 \
    --nThreads 0 \
    --display_id 0
```

Training completed with status `0` at `2026-05-30T00:27:18+08:00`. The selected
checkpoint is
`ERRNet/checkpoints/errnet_phaseC_exclusion_lam0001_10ep/errnet_010_00077320.pt`,
epoch `10`, iteration `77320`, SHA256
`defce620d09eba1f33a494382fd431696129c17f5f0f53728bbfb3acd94aea28`.
Tensor scan checked `122` floating tensors / `18953379` floating elements and
found `0` non-finite elements.

Benchmark results:

| Dataset | Samples | PSNR | SSIM | NCC | LMSE | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `ceilnet_table2` | 100 | 22.9187 | 0.8913 | 0.9514 | 0.0082 | `0` |
| `real20` | 20 | 21.3720 | 0.7877 | 0.8588 | 0.0225 | `0` |
| `postcard` | 179 | 17.2603 | 0.8370 | 0.9059 | 0.0052 | `0` |
| `objects` | 200 | 22.1991 | 0.8899 | 0.9706 | 0.0039 | `0` |
| `wild` | 101 | 23.8841 | 0.8996 | 0.9402 | 0.0053 | `0` |
| `sir2_withgt` | 480 | 20.7118 | 0.8722 | 0.9401 | 0.0047 | `0` |
| **Average** | - | **21.3910** | **0.8630** | **0.9278** | **0.0083** | - |

Comparison:

| Reference | Avg PSNR | Avg SSIM | Avg NCC | Avg LMSE |
| --- | ---: | ---: | ---: | ---: |
| Phase C `lambda=0.001`, epoch 10 | 21.3910 | 0.8630 | 0.9278 | 0.0083 |
| Aligned improved epoch 10 | 19.7233 | 0.8413 | 0.9091 | 0.0100 |
| Aligned improved epoch 60 | 24.4020 | 0.8858 | 0.9488 | 0.0071 |
| Baseline | 24.5689 | 0.8864 | 0.9486 | 0.0075 |

Verification:

| Check | Status | Evidence |
| --- | --- | --- |
| Training completion | passed | `ERRNet/experiments/run-logs/phaseC_exclusion_lam0001_10ep_20260529_phaseC_lam0001_10ep_tmux.status` contains `0`; training log ends at epoch `10`, iteration `77320` |
| Checkpoint tensor scan | passed | `ERRNet/experiments/run-logs/phaseC_tensor_scan_lam0001_10ep_20260530_phaseC_eval.log` reports `result: finite` |
| Benchmark completion | passed | Six `phaseC_eval_lam0001_10ep_*_20260530_phaseC_eval.status` files contain `0` |
| Custom output | passed | `ERRNet/experiments/run-logs/phaseC_custom_lam0001_10ep_20260530_phaseC_eval.status` contains `0`; `ERRNet/results/phaseC_lam0001_10ep_custom/` contains five model outputs plus copied inputs |
| Log anomaly scan | passed | No `Traceback`, `RuntimeError`, `Killed`, `invalid value`, `nan`, or `inf` matches in the Phase C 10epoch train/eval logs |

Decision:

- Technical result: training, checkpoint health, benchmark evaluation, and
  custom inference all succeeded.
- Quality result: the 10epoch candidate is not reportable as an improvement
  because its equal-weight average is still clearly below baseline and aligned
  improved epoch 60.
- Diagnostic result: the candidate is better than the aligned improved epoch 10
  checkpoint across all six datasets and all four averaged metrics, so this is
  not an implementation crash or non-finite failure. The likely cause is that
  10 epochs are too early for a mature checkpoint.
- Recovery action: continue from epoch 10 to epoch 20 using the same checkpoint
  directory and optimizer state with `-r --resume_epoch 10 --nEpochs 20`, then
  repeat tensor scan and benchmark evaluation before considering any longer
  run.

### Phase C Lambda 0.001 20-Epoch Recovery Candidate

The 10epoch candidate was continued in the same checkpoint directory with:

```bash
cd ERRNet
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
  python train_errnet.py \
    --name errnet_phaseC_exclusion_lam0001_10ep \
    --hyper \
    --lambda_exclusion 0.001 \
    --nEpochs 20 \
    -r \
    --resume_epoch 10 \
    --save_iter_freq 500 \
    --nThreads 0 \
    --display_id 0
```

Training completed with status `0` at `2026-05-30T03:03:34+08:00` and saved
`ERRNet/checkpoints/errnet_phaseC_exclusion_lam0001_10ep/errnet_020_00154640.pt`.
The checkpoint SHA256 is
`85b2d5e412fe232a3d923a7d76c60c2964c0c963746430e049996b5cc2b866c6`;
tensor scan checked `488` floating tensors / `56860259` floating elements and
found `0` non-finite elements.

Benchmark results:

| Dataset | Samples | PSNR | SSIM | NCC | LMSE | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `ceilnet_table2` | 100 | 24.8605 | 0.9085 | 0.9641 | 0.0063 | `0` |
| `real20` | 20 | 21.8367 | 0.7980 | 0.8579 | 0.0224 | `0` |
| `postcard` | 179 | 19.9198 | 0.8627 | 0.9252 | 0.0050 | `0` |
| `objects` | 200 | 23.4647 | 0.8853 | 0.9763 | 0.0036 | `0` |
| `wild` | 101 | 24.7432 | 0.9006 | 0.9382 | 0.0055 | `0` |
| `sir2_withgt` | 480 | 22.4118 | 0.8801 | 0.9492 | 0.0045 | `0` |
| **Average** | - | **22.8728** | **0.8725** | **0.9352** | **0.0079** | - |

Comparison:

| Reference | Avg PSNR | Avg SSIM | Avg NCC | Avg LMSE |
| --- | ---: | ---: | ---: | ---: |
| Phase C `lambda=0.001`, epoch 20 | 22.8728 | 0.8725 | 0.9352 | 0.0079 |
| Phase C `lambda=0.001`, epoch 10 | 21.3910 | 0.8630 | 0.9278 | 0.0083 |
| Aligned improved epoch 20 | 22.4945 | 0.8721 | 0.9321 | 0.0088 |
| Aligned improved epoch 60 | 24.4020 | 0.8858 | 0.9488 | 0.0071 |
| Baseline | 24.5689 | 0.8864 | 0.9486 | 0.0075 |

Verification:

| Check | Status | Evidence |
| --- | --- | --- |
| Training completion | passed | `ERRNet/experiments/run-logs/phaseC_exclusion_lam0001_resume20_20260530_phaseC_resume20.status` contains `0`; training log ends at epoch `20`, iteration `154640` |
| Checkpoint tensor scan | passed | `ERRNet/experiments/run-logs/phaseC_tensor_scan_lam0001_20ep_20260530_phaseC_resume20.log` reports `result=finite` |
| Benchmark completion | passed | Six `phaseC_eval_lam0001_20ep_*_20260530_phaseC_resume20.status` files contain `0` |
| Custom output | passed | `ERRNet/experiments/run-logs/phaseC_custom_lam0001_20ep_20260530_phaseC_resume20.status` contains `0`; `ERRNet/results/phaseC_lam0001_20ep_custom/` contains five model outputs plus copied inputs |
| Output counts | passed | Benchmark result directories contain `300`, `60`, `537`, `600`, `303`, and `1440` PNG files respectively, matching input/target/output triplets |
| Log anomaly scan | passed | No `Traceback`, `RuntimeError`, `Killed`, `CUDA out of memory`, `invalid value`, `nan`, or `inf` matches in the Phase C 20epoch train/tensor/eval/custom logs |

Decision:

- Technical result: the recovery run succeeded, the checkpoint is finite, and
  all benchmark/custom evaluation commands completed with status `0`.
- Quality result: epoch 20 is still below baseline and aligned improved epoch
  60, so it is not reportable as an overall quality improvement.
- Diagnostic result: epoch 20 improves over Phase C epoch 10 and is also above
  aligned improved epoch 20 on equal-weight PSNR/SSIM/NCC/LMSE, so the
  exclusion path still has a plausible training-progress signal.
- Next action: continue one more bounded segment from epoch 20 to epoch 30
  before deciding whether to stop Phase C and open a separate Phase D data
  strategy plan.

### Phase C Lambda 0.001 30-Epoch Recovery Candidate

The 20epoch candidate was continued in the same checkpoint directory with:

```bash
cd ERRNet
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
  python train_errnet.py \
    --name errnet_phaseC_exclusion_lam0001_10ep \
    --hyper \
    --lambda_exclusion 0.001 \
    --nEpochs 30 \
    -r \
    --resume_epoch 20 \
    --save_iter_freq 500 \
    --nThreads 0 \
    --display_id 0
```

Training completed with status `0` at `2026-05-30T05:49:21+08:00` and saved
`ERRNet/checkpoints/errnet_phaseC_exclusion_lam0001_10ep/errnet_030_00231960.pt`.
The checkpoint SHA256 is
`00784ad9323bb923426f1386bd92a8c8b8222b25cbe7497990049a0b9ce56bdb`;
tensor scan checked `656` floating tensors / `86671568` floating elements and
found `0` non-finite elements.

Benchmark results:

| Dataset | Samples | PSNR | SSIM | NCC | LMSE | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `ceilnet_table2` | 100 | 24.9263 | 0.9180 | 0.9659 | 0.0060 | `0` |
| `real20` | 20 | 22.1640 | 0.8122 | 0.8692 | 0.0212 | `0` |
| `postcard` | 179 | 20.7850 | 0.8635 | 0.9228 | 0.0055 | `0` |
| `objects` | 200 | 24.2010 | 0.8919 | 0.9778 | 0.0032 | `0` |
| `wild` | 101 | 24.5555 | 0.8966 | 0.9339 | 0.0071 | `0` |
| `sir2_withgt` | 480 | 23.0017 | 0.8823 | 0.9480 | 0.0049 | `0` |
| **Average** | - | **23.2722** | **0.8774** | **0.9363** | **0.0080** | - |

Comparison:

| Reference | Avg PSNR | Avg SSIM | Avg NCC | Avg LMSE |
| --- | ---: | ---: | ---: | ---: |
| Phase C `lambda=0.001`, epoch 30 | 23.2722 | 0.8774 | 0.9363 | 0.0080 |
| Phase C `lambda=0.001`, epoch 20 | 22.8728 | 0.8725 | 0.9352 | 0.0079 |
| Aligned improved epoch 30 | 23.2187 | 0.8737 | 0.9400 | 0.0083 |
| Aligned improved epoch 60 | 24.4020 | 0.8858 | 0.9488 | 0.0071 |
| Baseline | 24.5689 | 0.8864 | 0.9486 | 0.0075 |

Verification:

| Check | Status | Evidence |
| --- | --- | --- |
| Training completion | passed | `ERRNet/experiments/run-logs/phaseC_exclusion_lam0001_resume30_20260530_phaseC_resume30.status` contains `0`; training log ends at epoch `30`, iteration `231960` |
| Checkpoint tensor scan | passed | `ERRNet/experiments/run-logs/phaseC_tensor_scan_lam0001_30ep_20260530_phaseC_resume30.log` reports `result=finite` |
| Benchmark completion | passed | Six `phaseC_eval_lam0001_30ep_*_20260530_phaseC_resume30.status` files contain `0` |
| Custom recovery | passed | Initial custom command failed with status `2` because `--dataset custom` was omitted; retry `phaseC_custom_lam0001_30ep_20260530_phaseC_resume30.retry1.status` contains `0` |
| Output counts | passed | Benchmark result directories contain `300`, `60`, `537`, `600`, `303`, and `1440` PNG files respectively; custom output contains `10` PNG files |
| Log anomaly scan | passed | No `Traceback`, `RuntimeError`, `Killed`, `CUDA out of memory`, `invalid value`, `nan`, or `inf` matches in the successful Phase C 30epoch train/tensor/eval/custom logs |

Decision:

- Technical result: the epoch 30 recovery completed successfully, produced a
  finite checkpoint, and all benchmark/custom evaluations completed after the
  one corrected custom retry.
- Quality result: epoch 30 is still below baseline and aligned improved epoch
  60 on equal-weight average PSNR/SSIM/NCC/LMSE, so it is not reportable as an
  overall improvement.
- Diagnostic result: epoch 30 is only slightly above aligned improved epoch 30
  on PSNR/SSIM/LMSE and lower on NCC. It continues the Phase C training trend
  but does not close the gap to the mature baseline/aligned-60 references.
- Next action: stop Phase C long-training expansion for `lambda_exclusion=0.001`
  and open a separate Phase D data strategy plan before changing synthetic data,
  loader semantics, augmentation, or curriculum.

### Phase D Gamma 1.1-1.5 10-Epoch Screening Candidate

Phase D implemented the first bounded data-strategy candidate from
`specs/004-phase-d-data-strategy/`: `gamma_1p1_1p5`. The candidate changes only
the synthetic gamma range by setting `low_gamma=1.1` and `high_gamma=1.5`; all
other synthetic parameters remain at their existing defaults.

Implementation scope:

| File | Change | Scope Guard |
| --- | --- | --- |
| `ERRNet/options/errnet/train_options.py` | Add `--phase_d_candidate` with choices `none` and `gamma_1p1_1p5` | Default `none` preserves existing synthetic parameters |
| `ERRNet/options/errnet/base_options.py` | Call optional option postprocessing before printing/saving options | Existing parsers are unchanged unless they define `postprocess_options` |

Run command:

```bash
cd ERRNet
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
  python train_errnet.py \
    --name errnet_phaseD_gamma_1p1_1p5_10ep \
    --phase_d_candidate gamma_1p1_1p5 \
    --hyper \
    --nEpochs 10 \
    --save_iter_freq 500 \
    --nThreads 0 \
    --display_id 0
```

Rollback command: omit `--phase_d_candidate` or pass `--phase_d_candidate none`.
That restores the old synthetic defaults, including `low_gamma=1.3` and
`high_gamma=1.3`.

Training completed with status `0`. The selected checkpoint is
`ERRNet/checkpoints/errnet_phaseD_gamma_1p1_1p5_10ep/errnet_010_00077320.pt`,
epoch `10`, iteration `77320`, SHA256
`9bcde49447c1196b0cec458022f79d007a9a3e3fe153a81b559ca6474a540db4`.
Tensor scan checked `488` floating tensors / `56860259` floating elements and
found `0` non-finite elements.

Benchmark results:

| Dataset | Samples | PSNR | SSIM | NCC | LMSE | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `ceilnet_table2` | 100 | 23.0222 | 0.8928 | 0.9526 | 0.0081 | `0` |
| `real20` | 20 | 21.5040 | 0.7939 | 0.8751 | 0.0216 | `0` |
| `postcard` | 179 | 17.7712 | 0.8461 | 0.9159 | 0.0052 | `0` |
| `objects` | 200 | 22.4072 | 0.8922 | 0.9723 | 0.0038 | `0` |
| `wild` | 101 | 24.1263 | 0.9007 | 0.9408 | 0.0055 | `0` |
| `sir2_withgt` | 480 | 21.0401 | 0.8768 | 0.9447 | 0.0047 | `0` |
| **Average** | - | **21.6452** | **0.8671** | **0.9336** | **0.0081** | - |

Comparison:

| Reference | Avg PSNR | Avg SSIM | Avg NCC | Avg LMSE |
| --- | ---: | ---: | ---: | ---: |
| Phase D `gamma_1p1_1p5`, epoch 10 | 21.6452 | 0.8671 | 0.9336 | 0.0081 |
| Phase C `lambda=0.001`, epoch 30 | 23.2722 | 0.8774 | 0.9363 | 0.0080 |
| Aligned improved epoch 60 | 24.4020 | 0.8858 | 0.9488 | 0.0071 |
| Baseline | 24.5689 | 0.8864 | 0.9486 | 0.0075 |

Verification:

| Check | Status | Evidence |
| --- | --- | --- |
| Syntax check | passed | `python -m py_compile options/errnet/base_options.py options/errnet/train_options.py data/reflect_dataset.py data/transforms.py train_errnet.py` |
| Option/default check | passed | Default parse keeps `phase_d_candidate=none`, `low_gamma=1.3`, `high_gamma=1.3`; candidate parse sets `low_gamma=1.1`, `high_gamma=1.5` |
| Synthetic sample smoke | passed | `FusionDataset` loaded one training sample with `input`, `real`, `target_r`, `target_t`, and `unaligned` tensors at `(3, 224, 224)` |
| Training completion | passed | `ERRNet/experiments/run-logs/phaseD_gamma_1p1_1p5_10ep_20260530_phaseD_gamma_1p1_1p5_10ep.status` contains `0` |
| Checkpoint tensor scan | passed | `ERRNet/experiments/run-logs/phaseD_tensor_scan_gamma_1p1_1p5_10ep_20260530_phaseD_gamma_1p1_1p5_eval.log` reports `result=finite` |
| Benchmark completion | passed | Six `phaseD_eval_gamma_1p1_1p5_10ep_*_20260530_phaseD_gamma_1p1_1p5_eval.status` files contain `0` |
| Custom inference | passed | `ERRNet/experiments/run-logs/phaseD_custom_gamma_1p1_1p5_10ep_20260530_phaseD_gamma_1p1_1p5_eval.status` contains `0` |
| Output counts | passed | Benchmark result directories contain `300`, `60`, `537`, `600`, `303`, and `1440` PNG files respectively; custom output contains `10` PNG files |
| Log anomaly scan | passed | No `Traceback`, `RuntimeError`, `Killed`, `CUDA out of memory`, `invalid value`, `nan`, or `inf` matches in successful Phase D logs |

Decision:

- Technical result: the default-compatible Phase D data hook works, the
  `gamma_1p1_1p5` checkpoint is finite, and all benchmark/custom evaluations
  completed.
- Quality result: the candidate broadly underperforms Phase C epoch 30,
  aligned improved epoch 60, and baseline on equal-weight average metrics. It
  is rejected as a long-run or reportable improvement candidate.
- Attribution result: only the gamma range changed, so this is useful evidence
  that mild gamma variation alone does not close the current synthetic-to-real
  gap.
- Next action: do not extend `gamma_1p1_1p5` to 20/60 epochs. If more Phase D
  exploration is needed, start a separate single-variable sigma candidate or
  stop and consolidate the existing report evidence.

### TODO-003 Custom Visual Review

This section records the requested human-style visual scores for the custom
images in `5pictures/`. The custom images have no paired reflection-free ground
truth, so these scores are qualitative only and must not be reported as
full-reference metrics.

Review evidence generated on 2026-05-28:

| Evidence | Path |
| --- | --- |
| Priority comparison sheets | `ERRNet/experiments/visual-review/custom_p1_comparison.png` through `custom_p5_comparison.png` |
| All-method review sheets | `ERRNet/experiments/visual-review/custom_p1_all_methods.png` through `custom_p5_all_methods.png` |

Scoring rubric: `5` = strong reflection/highlight suppression with natural
detail preservation; `4` = useful suppression with minor artifacts or detail
loss; `3` = usable but only marginally different from input/baseline; `2` =
limited reflection removal or visible quality tradeoff; `1` = clearly worse or
artifact-heavy.

Priority comparison from `todo.md`:

| Image | Baseline Score | Full-Retrain Score | Phase B `improved + ctx_vgg` Score | Selected For Display | Human-Style Review Note |
| --- | ---: | ---: | ---: | --- | --- |
| p1 | 3.0 | 3.0 | 3.0 | no strong winner | Glass-door reflections and interior/window details remain similar across all three outputs; no visible improvement should be claimed. |
| p2 | 2.5 | 2.5 | 3.0 | weak candidate only | Curved-window reflections and branch-like structures are mostly retained. Phase B is slightly cleaner but the improvement is marginal. |
| p3 | 2.0 | 2.0 | 2.0 | failure / limitation | The reflected trees, road, and orange glass reflections remain almost unchanged; methods mostly preserve the reflected facade content. |
| p4 | 3.0 | 3.0 | 3.5 | usable mixed case | Phase B gives the clearest outdoor scene and stronger contrast, but the door/window reflection marks remain visible. |
| p5 | 3.5 | 2.5 | 4.0 | success case | Phase B `improved + ctx_vgg` gives the cleanest large glass facade by suppressing repeated reflection texture; full retrain introduces a darker smear/uneven patch near the upper glass area. |

All-method score matrix:

| Method | p1 | p2 | p3 | p4 | p5 | Avg | Qualitative Summary |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Baseline | 3.0 | 2.5 | 2.0 | 3.0 | 3.5 | 2.8 | Stable and natural, but mostly weak reflection removal. |
| Improved option default weights | 3.0 | 2.5 | 2.0 | 3.0 | 3.5 | 2.8 | Visually matches baseline, as expected from default-compatible inference. |
| Full retrain aligned epoch 60 | 3.0 | 2.5 | 2.0 | 3.0 | 2.5 | 2.6 | No clear custom-image benefit; p5 shows an obvious local artifact/uneven patch. |
| Phase B baseline + vgg | 3.0 | 2.5 | 2.0 | 3.0 | 3.5 | 2.8 | Similar to baseline with slight facade cleanup on p5. |
| Phase B baseline + ctx | 3.0 | 3.0 | 2.0 | 3.0 | 3.5 | 2.9 | Slightly cleaner on p2, otherwise close to baseline. |
| Phase B baseline + ctx_vgg | 3.0 | 3.0 | 2.0 | 3.0 | 3.5 | 2.9 | Similar to baseline + ctx; no broad visual win. |
| Phase B improved + vgg | 3.0 | 2.5 | 2.0 | 3.0 | 3.5 | 2.8 | Stable but not visibly better than baseline. |
| Phase B improved + ctx | 3.0 | 3.0 | 2.0 | 3.5 | 4.0 | 3.1 | Best or tied-best on p4/p5; still limited on p1-p3. |
| Phase B improved + ctx_vgg | 3.0 | 3.0 | 2.0 | 3.5 | 4.0 | 3.1 | Best qualitative candidate, matching the Phase B metric-screen conclusion; still not a full default-training claim. |

Selected qualitative cases for paper/PPT:

| Case Type | Image | Recommended Output | Reason |
| --- | --- | --- | --- |
| Success | p5 | `ERRNet/results/phaseB_quick_improved_ctx_vgg_custom/p5/errnet_phaseB_quick_improved_ctx_vgg_custom.png` | Cleans large-pane reflection texture better than baseline/full retrain while preserving the building outline reasonably well. |
| Mixed / usable | p4 | `ERRNet/results/phaseB_quick_improved_ctx_vgg_custom/p4/errnet_phaseB_quick_improved_ctx_vgg_custom.png` | Outdoor transmission appears clearer, but window/door reflection marks remain. |
| Failure / limitation | p3 | `ERRNet/results/phaseB_quick_improved_ctx_vgg_custom/p3/errnet_phaseB_quick_improved_ctx_vgg_custom.png` | Reflection-like facade content remains; no method removes the reflected trees/road convincingly. |
| Full-retrain limitation | p5 | `ERRNet/results/custom_improved_retrain_60ep/p5/errnet_improved_retrain_60ep_custom.png` | Shows why aligned full retrain should not be claimed as visually superior on custom images. |

TODO-003 decision:

- Completed: all five custom images were visually reviewed across baseline,
  improved-option, full-retrain, and six Phase B quick-screen outputs.
- Best qualitative candidate: Phase B `improved + ctx_vgg`, tied with
  Phase B `improved + ctx` in average human-style score.
- Main limitation: p1-p3 do not show reliable reflection removal; apparent
  improvements are small or absent.
- Reporting constraint: use these scores as qualitative evidence only. They do
  not override the six benchmark metric tables and do not justify claiming
  broad improvement over baseline.

### Commands Run For This Feature

| Purpose | Command | Status |
| --- | --- | --- |
| Dependency readiness | `conda run -n ERRNet python -m pip install -r ERRNet/requirements.txt` | completed |
| Syntax check | `conda run -n ERRNet python -m py_compile train_errnet.py test_errnet.py engine.py models/losses.py models/errnet_model.py models/base_model.py options/base_option.py options/errnet/base_options.py options/errnet/train_options.py data/reflect_dataset.py` | passed |
| Training help/options | `conda run -n ERRNet python train_errnet.py --help` | passed after requirements sync |
| Evaluation help/options | `conda run -n ERRNet python test_errnet.py --dataset ceilnet_table2 --help` | passed |
| Loss tensor smoke | CPU tensor invocation of `MultipleLoss([nn.MSELoss(), GradientLoss()], [0.2, 0.4])` | finite loss |
| Data readiness | Dataloader construction/count and sample tensor inspection | passed |
| VGG readiness | `Vgg19(requires_grad=False)` | passed |
| Full command start-validation | `timeout --kill-after=20s 120s conda run -n ERRNet python train_errnet.py --name errnet_improved_retrain_60ep --hyper --pixel_loss_weight 0.2 --gradient_loss_weight 0.4` | timeout status `124`; no checkpoint |
| Checkpoint interrupt smoke | `timeout --kill-after=20s 60s conda run -n ERRNet python train_errnet.py --name errnet_ckpt_interrupt_smoke_20260526 --hyper --pixel_loss_weight 0.2 --gradient_loss_weight 0.4 --max_dataset_size 2 --nThreads 0 --display_id 0` | produced loadable `errnet_interrupted.pt` and `errnet_latest.pt`; log `ckpt_interrupt_smoke_20260526.log` |
| Checkpoint load smoke | `conda run -n ERRNet python test_errnet.py --name errnet_ckpt_interrupt_load_smoke_20260526 --dataset custom --input_dir ../5pictures --max_long_edge 256 --save_subdir ckpt_interrupt_load_smoke_20260526 -r --icnn_path checkpoints/errnet_ckpt_interrupt_smoke_20260526/errnet_interrupted.pt --hyper --nThreads 0` | status `0`; generated 5 custom outputs plus inputs; log `ckpt_interrupt_load_smoke_20260526.log` |
| Iteration-save smoke | `timeout --kill-after=20s 180s conda run -n ERRNet python train_errnet.py --name errnet_ckpt_iter_smoke_20260526 --hyper --pixel_loss_weight 0.2 --gradient_loss_weight 0.4 --max_dataset_size 2 --nThreads 0 --display_id 0 --save_iter_freq 1` | produced loadable `errnet_latest.pt`; checkpoint state `epoch=1`, `iterations=157`; SHA256 `24ea81d3994869e0f75de60bd01357b5299e99aef0e62d1b6b6fe3cf726a6b19`; log `ckpt_iter_save_smoke_20260526.log` |
| Final checkpoint checksum | `sha256sum ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_latest.pt ERRNet/checkpoints/errnet/errnet_060_00463920.pt` | passed; selected final SHA256 `9214c1bd66e38350d99c99c02dd2fbceb626b15e50d66c1f3df1bf3a14c7073d`; baseline SHA256 unchanged |
| Final checkpoint metadata | `conda run --no-capture-output -n ERRNet python - <<'PY' ... torch.load(..., map_location='cpu') ... PY` | selected final checkpoint and `errnet_latest.pt` both reported checkpoint metadata `epoch=60` |
| TODO-002 benchmark evaluations | six `test_errnet.py` commands using `--icnn_path checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt` and `RUN_TS=20260527_0245` | all six status files contain `0`; metrics and output counts are recorded above |
| TODO-002 output count check | `find ERRNet/results/improved_retrain_60ep_<dataset> -name "errnet_improved_retrain_60ep_<dataset>.png" | wc -l` | expected counts matched: 100, 20, 179, 200, 101, 480 |
| T044 custom evaluation | `conda run --no-capture-output -n ERRNet python test_errnet.py --name errnet_improved_retrain_60ep_custom --dataset custom --input_dir ../5pictures --max_long_edge 1024 --save_subdir custom_improved_retrain_60ep -r --icnn_path checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt --hyper --nThreads 0` | status `0`; log `ERRNet/experiments/run-logs/improved_retrain_60ep_custom_20260527_032534.log`; generated p1-p5 outputs |
| T044 image integrity check | `PIL.Image.open` and NumPy summary for five custom output PNGs | all five outputs opened successfully, RGB mode, non-empty pixel ranges |
| Phase A checkpoint diagnostics | 36 `test_errnet.py` evaluations for epochs `10/20/30/40/50/60` over all six benchmark datasets, with `RUN_TS=20260527_phaseA` | all status files contain `0`; epoch 60 selected as current best/balanced checkpoint |
| Phase B quick-screen training | Six `train_errnet_unaligned.py` runs from baseline/improved checkpoints with `--unaligned_loss` in `vgg`, `ctx`, `ctx_vgg`, `--max_dataset_size 100`, and `RUN_TS=20260527_phaseB_quick` | all six status files contain `0`; six epoch-80 checkpoints recorded above |
| Phase B quick-screen benchmarks | 36 `test_errnet.py` evaluations over all six benchmark datasets for the six Phase B checkpoints | all 36 status files contain `0`; metrics and output counts are recorded above |
| Phase B custom evaluation | Six `test_errnet.py --dataset custom --input_dir ../5pictures` runs for the Phase B checkpoints | all six status files contain `0`; each generated five qualitative outputs |
| Phase B full checkpoint health | `torch.load` tensor scan over `ERRNet/checkpoints/errnet_phaseB_full_improved_ctx_vgg/errnet_070_00550528.pt`, `errnet_080_00630348.pt`, and `errnet_latest.pt` | epoch 70 selected; epoch 80/latest rejected because all scanned floating tensors contain non-finite values |
| Phase B full `improved + ctx_vgg` benchmarks | Six `test_errnet.py` evaluations using `errnet_070_00550528.pt` and `RUN_ID=20260528_phaseB_full_ep70` | all six status files contain `0`; finite metrics are recorded in the full-run table |
| Phase B full `improved + ctx_vgg` custom evaluation | `test_errnet.py --dataset custom --input_dir ../5pictures --max_long_edge 1024` using `errnet_070_00550528.pt` | status `0`; five model outputs generated under `ERRNet/results/phaseB_full_improved_ctx_vgg_ep70_custom/` |
| Historical Phase B full `improved + ctx` candidate search | `find` over current workspace and parent project tree plus log/status inspection | no full checkpoint found in the earlier failed run; superseded by the fixed epoch-80 rerun below |
| Phase B full fixed checkpoint health | Tensor scan over `errnet_phaseB_full_improved_ctx_vgg_fixed/errnet_080_00632892.pt` and `errnet_phaseB_full_improved_ctx_fixed/errnet_080_00630348.pt` with `RUN_ID=20260529_phaseB_full_fixed` | both scans report `0` non-finite tensors/elements and `result: finite` |
| Phase B full fixed benchmarks | Twelve `test_errnet.py` evaluations over six datasets for `improved_ctx_vgg_fixed` and `improved_ctx_fixed` | all twelve status files contain `0`; finite metrics and matching output counts are recorded in the fixed epoch-80 table |
| Phase B full fixed custom evaluation | Two `test_errnet.py --dataset custom --input_dir ../5pictures --max_long_edge 1024` runs for the fixed full checkpoints | both status files contain `0`; each generated five custom outputs |
| Phase C exclusion-loss syntax/tensor smoke | `py_compile`, option/default checks, and `ExclusionLoss` random/constant tensor forward-backward checks in the `errnet` env | passed; positive loss and gradients finite, constant tensor loss finite |
| Phase C exclusion-loss bounded training smoke | `train_errnet.py --name errnet_phaseC_exclusion_smoke --lambda_exclusion 0.001 --nEpochs 1 --max_dataset_size 2 --save_iter_freq 1` | status `0`; finite `Excl` values logged; checkpoint epoch `1`, iterations `90` |
| Phase C smoke checkpoint load/custom inference | `test_errnet.py --dataset custom --input_dir ../5pictures --max_long_edge 256 --icnn_path checkpoints/errnet_phaseC_exclusion_smoke/errnet_latest.pt` | status `0`; generated five custom outputs under `ERRNet/results/phaseC_exclusion_smoke_load/` |
| TODO-003 visual review sheets | `python - <<'PY' ... PIL contact-sheet generation ... PY` over custom input/baseline/full-retrain/Phase B outputs | generated 10 review sheets under `ERRNet/experiments/visual-review/`; all opened for visual scoring |

### Final Notes For Feature 002

- Localized checkpoint-save code was changed in this implementation pass.
- No loader, metric, architecture, dataset, baseline checkpoint, or training
  configuration file was changed.
- Existing baseline behavior and baseline checkpoint were preserved.
- `ERRNet/README_DIP26.md` and the quickstart now document `--save_iter_freq`
  for long aligned runs.
- The generated smoke checkpoints proved checkpoint generation was unblocked.
  The final improved evidence now uses
  `ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt`.
- TODO-002 benchmark evaluation is complete for all six datasets. T044
  full-retrain custom-image outputs are generated, and TODO-003 visual scoring
  selected p5 as a success case and p3 as a failure/limitation case.
- Phase A checkpoint-selection diagnostics are complete. Intermediate
  checkpoints do not explain the current mixed result; epoch 60 remains the
  selected checkpoint for the current aligned retraining run.
- Phase B quick-screen unaligned finetuning is complete. The strongest
  screening result is `improved + ctx_vgg`, especially on SSIM/LMSE and `wild`;
  however the run used a capped synthetic subset and does not justify a full
  default-training improvement claim.
- Phase B full default-data `improved + ctx_vgg` testing is complete for the
  last healthy checkpoint, epoch 70. The epoch-80/latest full checkpoint is
  rejected due to NaN/Inf weights and NaN benchmark metrics. Epoch 70 is mixed
  and does not improve the equal-weight average over baseline or aligned
  improved epoch 60.
- After the CX stability fix, both repaired full epoch-80 candidates completed:
  `improved + ctx_vgg_fixed` and `improved + ctx_fixed`. Their checkpoints are
  finite and all six benchmark plus custom evaluations completed, but both
  remain mixed and do not improve the equal-weight PSNR/SSIM average over
  baseline or aligned improved epoch 60.
- Phase C exclusion-loss experimentation is open. The default-disabled
  `--lambda_exclusion` path is smoke-verified, including finite tensor
  forward/backward behavior, one bounded training run, and smoke checkpoint
  custom inference. No quality claim is made from this smoke checkpoint.

### Final Validation

| Check | Status | Result |
| --- | --- | --- |
| `git diff --check` | passed | Checked feature specs, AGENTS, experiment docs, and guarded ERRNet source/readme paths |
| Placeholder/stale-language scan | completed | Remaining angle-bracket placeholders in `contracts/` and `quickstart.md` are intentional command variables; `NEEDS CLARIFICATION` appears only as checklist/task text |
| Out-of-scope domain-language scan | passed | No obsolete cross-domain wording was found in the current feature docs or experiment docs |
| Scope review | passed | Source edits are limited to checkpoint-save/training option paths plus related documentation/evidence |
| Source compatibility review | passed | No loader, metric, architecture, dataset, dependency, or baseline checkpoint source path changed |
| Final feature state | benchmark and custom outputs completed | Checkpoint generation is fixed and verified; final epoch-60 checkpoint exists, six benchmark evaluations completed, five custom full-retrain outputs generated, the original full default-data `improved + ctx_vgg` epoch-70 fallback has been evaluated, and both repaired full epoch-80 candidates have completed health checks, six benchmarks, and custom outputs |

## Compute Notes

- Full improved retraining produced an explicit epoch-60 checkpoint:
  `ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt`.
- CPU and single-card CUDA are the current compatibility boundary.
- Added options:
  - `--pixel_loss_weight`, default `0.2`
  - `--gradient_loss_weight`, default `0.4`
  - `--lambda_exclusion`, default `0.0`
- `--save_iter_freq`, default `0`, optionally saves `latest` during long
  epochs without changing the default epoch-only save cadence.
- The implementation changes scalar weights passed into existing
  `MultipleLoss` and checkpoint save timing/atomicity only; it does not change
  tensor shapes, dtype, device placement, dataloaders, metrics, model
  architecture, or checkpoint schema.
- `ERRNet/README_DIP26.md` documents the optional loss-weight and long-run
  checkpoint commands.
- Inference with the pretrained checkpoint and default-compatible loss weights
  is not a trained improved model; it only verifies option compatibility and
  output generation.
