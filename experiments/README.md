# ERRNet Experiment Records

This directory stores reproducibility evidence for the DIP26 ERRNet single
image reflection removal project. It is intentionally documentation-only unless
a later task records paths to generated outputs.

## Scope

- Feature: ERRNet 2D RGB single-image reflection removal course project.
- Current implementation boundary: reuse existing ERRNet scripts and add only
  local, default-compatible loss-weight options when improvement work starts.
- Out of scope: final paper/PPT authoring, external upload, submission email,
  new datasets, loader/metric semantic changes, architecture rewrites, and
  multi-card or distributed training adaptation.

## Record Index

| Record | Purpose | Completion Rule |
| --- | --- | --- |
| `environment.md` | OS, Python, dependency, CUDA/CPU, GPU, and commit record | Actual values or blocker notes are recorded |
| `datasets.md` | Raw data, processed data, checkpoint, benchmark, and custom image readiness | Paths, observed counts, and missing items are recorded |
| `results-baseline.md` | Baseline commands, metrics, outputs, and custom image evidence | Commands, result paths, metrics or blockers, and metric semantics are recorded |
| `results-improved.md` | Improved-method configuration, compatibility, smoke runs, full-retraining start validation, and comparison | Default compatibility, checkpoint compatibility, command evidence, and blockers are recorded |
| `report-materials.md` | Interim paper/PPT material pool, slide skeleton, and custom figure checklist | Current evidence is organized as reusable material without claiming final submission results |
| `delivery-checklist.md` | Course delivery readiness and paper/PPT evidence mapping | Each deliverable is complete, blocked, missing, or linked to evidence |

## Required Fields

Experiment runs must include:
- run name
- method
- dataset
- command
- environment reference
- parameters
- output path
- status: `planned`, `completed`, `blocked`, or `skipped`
- notes and residual risk when not completed

Evaluation results must include:
- method and dataset
- metric status: `measured`, `not applicable`, or `blocked`
- PSNR, SSIM, NCC, and LMSE when valid
- prediction/target alignment policy
- crop policy
- pixel range
- ground-truth status
- mask or valid-pixel policy
- NaN/inf status
- visual paths and interpretation

## Completion Rules

- Do not report custom images as full-reference metrics unless paired ground
  truth is available.
- Do not report a partial retraining attempt as a final improved checkpoint.
- Do not edit loader, resize/crop/augmentation, or metric implementation paths
  without first updating `spec.md`, `plan.md`, and `tasks.md`.
- Any new optional training argument must default to current baseline behavior.
- Existing ERRNet commands, dataset keys, metric names, and checkpoint paths
  must remain valid.
- Final completion requires changed files, commands run, verification results,
  assumptions, and residual risks to be summarized in this file.

## Command Contracts

Reviewed in T009 from `ERRNet/test_errnet.py`.

### Benchmark Evaluation

```bash
cd ERRNet
python test_errnet.py --name errnet --dataset <dataset_key> -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper
```

Supported benchmark dataset keys:
- `ceilnet_table2`
- `real20`
- `postcard`
- `objects`
- `wild`
- `sir2_withgt`

Default data root: `./datasets/processed_data`

Default output root: `./results`

Dataset key to output subdirectory:
- `ceilnet_table2` -> `CEILNet_table2`
- `real20` -> `real20`
- `postcard` -> `postcard`
- `objects` -> `objects`
- `wild` -> `wild`
- `sir2_withgt` -> `sir2_withgt`

Optional CPU mode uses the existing base option:

```bash
python test_errnet.py --name errnet_cpu --dataset <dataset_key> -r --gpu_ids -1 --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper
```

### Custom Image Evaluation

```bash
cd ERRNet
python test_errnet.py --name errnet --dataset custom --input_dir ../5pictures --max_long_edge 1024 -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper
```

Custom images are loaded through the existing `RealDataset` path and saved under
`ERRNet/results/custom/` unless `--result_dir` or `--save_subdir` is changed.
This feature does not change dataset keys, loader behavior, metric names, or
result directory defaults.

## Static Validation Log

T011 completed on 2026-05-24:
- `git diff --check -- ERRNet/experiments specs/001-errnet-reflection-spec/... .gitignore` passed.
- Placeholder scan found no unresolved implementation placeholders in planning
  artifacts. The only `NEEDS CLARIFICATION` hit is the completed checklist item
  text in `checklists/requirements.md`.

## Dirty Worktree And Scope Log

T012 completed on 2026-05-24 before editing ERRNet implementation files.

Observed dirty worktree includes pre-existing Spec Kit, AGENTS, ERRNet,
dataset, guide, and generated artifact changes. These are treated as existing
workspace state and are not reverted.

Allowed edit paths for this feature:
- `.gitignore`
- `ERRNet/experiments/`
- `ERRNet/options/errnet/train_options.py`
- `ERRNet/models/losses.py`
- `ERRNet/models/errnet_model.py` only if reporting needs it
- `ERRNet/README_DIP26.md` only if command guidance changes
- `specs/001-errnet-reflection-spec/tasks.md`

Guarded paths:
- `ERRNet/data/`
- `ERRNet/datasets/`
- `ERRNet/util/index.py`
- `ERRNet/models/arch.py` or `ERRNet/models/networks.py`
- raw data, processed data, checkpoints, final paper/PPT assets

If any guarded path becomes necessary, stop and update spec, plan, and tasks
before editing.

## Blocker Rerun Summary

Environment-related blockers were rerun on 2026-05-25 in the documented
`errnet` conda environment.

### Rerun Evidence

- Six benchmark evaluations completed with status `0`:
  - `ceilnet_table2`: PSNR `27.8766`, SSIM `0.9407`, NCC `0.9808`, LMSE `0.0048`
  - `real20`: PSNR `23.5531`, SSIM `0.8285`, NCC `0.8877`, LMSE `0.0201`
  - `postcard`: PSNR `22.0710`, SSIM `0.8773`, NCC `0.9463`, LMSE `0.0044`
  - `objects`: PSNR `24.8530`, SSIM `0.8980`, NCC `0.9817`, LMSE `0.0029`
  - `wild`: PSNR `25.1761`, SSIM `0.8861`, NCC `0.9359`, LMSE `0.0083`
  - `sir2_withgt`: PSNR `23.8836`, SSIM `0.8878`, NCC `0.9589`, LMSE `0.0046`
- CPU fallback completed on `ceilnet_table2` with status `0` and metrics:
  PSNR `27.8767`, SSIM `0.9407`, NCC `0.9808`, LMSE `0.0048`.
- Custom baseline inference generated five outputs under
  `ERRNet/results/custom_baseline/`.
- Improved-option custom inference generated five outputs under
  `ERRNet/results/custom_improved_default_weights/`.
- Improved loss-weight smoke completed with status `0`; it loaded the existing
  checkpoint and evaluated CEILNet, but did not perform new long training
  because the resumed checkpoint was already at epoch 60.
- Loss tensor smoke completed on CPU with input shape `(2, 3, 16, 16)`, dtype
  `torch.float32`, finite loss, and default weights `0.2` / `0.4`.

### Rerun Logs

Logs are stored under `ERRNet/experiments/run-logs/`:
- `baseline_ceilnet_table2_20260525.log`
- `baseline_real20_20260525.log`
- `baseline_postcard_20260525.log`
- `baseline_objects_20260525.log`
- `baseline_wild_20260525.log`
- `baseline_sir2_withgt_20260525.log`
- `cpu_fallback_ceilnet_table2_20260525.log`
- `custom_baseline_20260525.log`
- `custom_improved_default_weights_20260525.log`
- `improved_loss_weight_smoke_20260525.log`
- `loss_tensor_smoke_20260525.log`

## Final Implementation Summary

T045 completed on 2026-05-24.

### Modified Files

- `.gitignore`: added minimal Python/common ignore patterns required by Spec
  Kit setup verification.
- `ERRNet/options/errnet/train_options.py`: added
  `--pixel_loss_weight` and `--gradient_loss_weight` with defaults `0.2` and
  `0.4`.
- `ERRNet/models/losses.py`: parameterized the existing aligned
  `MultipleLoss([nn.MSELoss(), GradientLoss()], ...)` weights through the new
  options while preserving default behavior.
- `ERRNet/README_DIP26.md`: documented the optional local loss-weight
  experiment command.
- `ERRNet/experiments/*.md`: recorded environment, dataset readiness,
  baseline/improved commands, rerun results, metric semantics, and delivery
  status.
- `specs/001-errnet-reflection-spec/tasks.md`: marked completed tasks after
  recording implementation and verification evidence.

`ERRNet/models/errnet_model.py` was reviewed but not changed because current
error reporting already exposes the combined `IPixel` scalar.

### Behavior Change

Default ERRNet training remains compatible with the previous behavior. When no
new options are passed, the aligned pixel loss still uses MSE weight `0.2` and
GradientLoss weight `0.4`.

The only new behavior is opt-in:

```bash
python train_errnet.py --name errnet_loss_weight_smoke --hyper --pixel_loss_weight 0.2 --gradient_loss_weight 0.4
```

Changing those two values adjusts the existing aligned pixel-loss weighting. No
model architecture, checkpoint schema, dataset loader, metric implementation,
training config, inference config, dependency, or multi-card path
was changed.

## Full Retraining Checkpoint Feature

Feature reference: `specs/002-improved-retraining-checkpoint/plan.md`

Expected artifact:
`ERRNet/checkpoints/errnet_improved_retrain_60ep/`.

Implementation evidence is recorded in `results-improved.md` under
"Full Retraining Checkpoint Result". The improved run produced an explicit
epoch-60 checkpoint:
`ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt`.
The selected checkpoint checksum, metadata, load-verification evidence, six
benchmark commands, output counts, logs, and metrics are recorded there.
TODO-002 benchmark evaluation is complete; full-retrain custom-image
qualitative outputs for p1-p5 are also generated under
`ERRNet/results/custom_improved_retrain_60ep/`.

The baseline checkpoint remains available at
`ERRNet/checkpoints/errnet/errnet_060_00463920.pt`.

### Verification Results

- `python -m py_compile ERRNet/options/errnet/train_options.py ERRNet/options/errnet/base_options.py ERRNet/options/base_option.py ERRNet/models/losses.py ERRNet/models/errnet_model.py` passed.
- Static source check confirmed both new CLI options exist and
  `losses.py` falls back to defaults `0.2` and `0.4`.
- `git diff --check -- ERRNet/experiments ERRNet/options/errnet/train_options.py ERRNet/models/losses.py ERRNet/models/errnet_model.py ERRNet/README_DIP26.md specs/001-errnet-reflection-spec/... .gitignore` passed.
- Baseline, CPU fallback, old-checkpoint compatibility, custom-image inference,
  and improved smoke commands were rerun successfully in the `errnet`
  environment on 2026-05-25. Metrics, output counts, and log paths are recorded
  in `results-baseline.md` and `results-improved.md`.

### Scope Review

Feature-introduced changes are limited to the approved experiment records,
approved ERRNet option/loss files, README command guidance, `.gitignore`, and
the current feature task file. The broader top-level dirty worktree contains
pre-existing Spec Kit, AGENTS, dataset, guide, and generated artifact changes;
those were not reverted or edited as part of implementation cleanup.

### Assumptions And Risks

- Assumption: the approved improved method is the ERRNet PJ local
  structural-loss weighting experiment only.
- Assumption: the documented `errnet` conda environment or packed archive is the
  reproducible runtime for this workspace.
- Risk: full improved-method retraining was not performed; current improved
  evidence proves option/checkpoint/runtime compatibility, not a trained quality
  improvement.
- Risk: custom-image outputs are generated but still require human visual review
  for success/failure case selection.
- Risk: final repository link, external model-weight link, group contribution
  text, paper, PPT, and submission email remain external delivery work.
