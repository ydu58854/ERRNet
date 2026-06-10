# Data Model: ERRNet Improved Retraining Checkpoint

## ImprovedRetrainingRun

**Purpose**: Represents the approved full improved aligned training run.

**Fields**:
- `run_name`: `errnet_improved_retrain_60ep`.
- `training_mode`: non-resumed aligned retraining.
- `epoch_target`: `60`.
- `pixel_loss_weight`: `0.2`.
- `gradient_loss_weight`: `0.4`.
- `command`: exact reproducible command.
- `environment`: OS, Python, dependencies, CUDA/CPU mode, GPU model, seed.
- `start_time`: recorded start timestamp when available.
- `end_time`: recorded end timestamp when available.
- `status`: planned, running, completed, blocked, or failed.
- `log_path`: run log under `ERRNet/experiments/run-logs/` or documented
  equivalent.
- `blocker`: reason and residual risk when status is not completed.

**Relationships**:
- Produces one `ImprovedCheckpoint`.
- Produces zero or more training-time `EvaluationResult` records.
- Feeds one `ImprovedComparisonRecord`.

**Validation Rules**:
- A completed run must show non-resumed start and 60-epoch completion evidence.
- A resumed or smoke-only run cannot satisfy this entity's completed state.
- Loss weights must be exactly `0.2` and `0.4` unless the spec is updated.
- Blocked or failed runs must preserve partial artifacts as non-final evidence.

## ImprovedCheckpoint

**Purpose**: Represents the final model artifact produced by the improved
retraining run.

**Fields**:
- `experiment_name`: `errnet_improved_retrain_60ep`.
- `directory`: `ERRNet/checkpoints/errnet_improved_retrain_60ep/`.
- `checkpoint_file`: final selected loadable checkpoint file.
- `checksum`: checksum for the selected checkpoint file.
- `created_by_run`: linked `ImprovedRetrainingRun`.
- `creation_status`: generated, missing, partial, archived, or blocked.
- `load_status`: unverified, load-verified, failed, or blocked.
- `baseline_preserved`: whether `ERRNet/checkpoints/errnet/errnet_060_00463920.pt`
  remains present and usable.

**Relationships**:
- Belongs to one `ImprovedRetrainingRun`.
- Used by six `BenchmarkEvaluationResult` records and five
  `CustomImageOutput` records.

**Validation Rules**:
- Must not overwrite the baseline checkpoint or smoke-run artifacts.
- If the target directory exists before final training, archive or preserve
  prior contents and record the action.
- Must have a recorded checksum before report-ready status.
- Must load successfully before benchmark/custom evaluation is treated as
  checkpoint evidence.

## BenchmarkEvaluationResult

**Purpose**: Represents one quantitative evaluation row for the improved
checkpoint on a spec1 benchmark dataset.

**Fields**:
- `dataset_key`: one of `ceilnet_table2`, `real20`, `postcard`, `objects`,
  `wild`, `sir2_withgt`.
- `checkpoint`: linked `ImprovedCheckpoint`.
- `command`: exact evaluation command.
- `result_path`: output image directory or file pattern.
- `sample_count`: observed evaluated sample count.
- `psnr`: measured value or unavailable.
- `ssim`: measured value or unavailable.
- `ncc`: measured value or unavailable.
- `lmse`: measured value or unavailable.
- `metric_status`: measured, blocked, or unavailable.
- `nan_inf_status`: none observed, observed, or not checked.
- `alignment_policy`: inherited existing ERRNet eval policy.
- `comparison_to_baseline`: improved, worse, equal, or inconclusive.

**Relationships**:
- Belongs to one `ImprovedCheckpoint`.
- Compared with the matching row in `ERRNet/experiments/results-baseline.md`.

**Validation Rules**:
- All six dataset keys must have a row.
- Metrics must use the same semantics as spec1 baseline evidence.
- Missing metrics require a precise unavailable or blocker reason.
- Worse results are valid evidence but cannot support an improvement claim.

## CustomImageOutput

**Purpose**: Represents one qualitative output for a custom image from
`5pictures/`.

**Fields**:
- `image_name`: `p1.jpg` through `p5.jpg`.
- `input_path`: path under `5pictures/`.
- `checkpoint`: linked `ImprovedCheckpoint`.
- `command`: exact custom evaluation command.
- `output_path`: generated improved output image.
- `ground_truth_status`: unavailable unless references are added later.
- `visual_status`: generated, missing, blocked, or review-needed.
- `comparison_to_baseline`: qualitative note or blocker.

**Relationships**:
- Belongs to one `ImprovedCheckpoint`.
- Feeds `ImprovedComparisonRecord`.

**Validation Rules**:
- All five image names must have output rows or explicit blockers.
- Metrics are not valid unless paired ground truth is added.
- Output paths must be distinct from baseline custom outputs.

## ImprovedComparisonRecord

**Purpose**: Summarizes whether the new checkpoint supports an improvement
claim relative to spec1 baseline evidence.

**Fields**:
- `baseline_reference`: `ERRNet/experiments/results-baseline.md`.
- `improved_checkpoint`: linked `ImprovedCheckpoint`.
- `benchmark_summary`: six-row quantitative comparison.
- `custom_summary`: five-image qualitative comparison.
- `claim_status`: supports improvement, does not support improvement, or
  inconclusive.
- `assumptions`: environment, data, and metric assumptions.
- `risks`: compute, reproducibility, metric, and visual-review risks.

**Relationships**:
- Aggregates six `BenchmarkEvaluationResult` records.
- Aggregates five `CustomImageOutput` records.
- Updates `ERRNet/experiments/results-improved.md`.

**Validation Rules**:
- Must not conflate prior smoke evidence with full retraining evidence.
- Must state actual measured outcome even when worse than baseline.
- Must include residual risks before the checkpoint is considered report-ready.

## CompatibilityEvidence

**Purpose**: Captures proof that any localized code fix did not break existing
behavior.

**Fields**:
- `changed_files`: list of localized files changed, if any.
- `blocker_addressed`: reason the change was necessary.
- `default_preservation_check`: command or inspection proving defaults remain
  compatible.
- `old_checkpoint_inference_check`: command/result for baseline checkpoint
  inference after changes.
- `dependency_status`: no new dependency or documented exception.
- `loader_metric_status`: unchanged, or spec update required.

**Relationships**:
- Required only when implementation touches model, loss, or training-path code.
- Feeds final implementation summary.

**Validation Rules**:
- Must exist for every localized code fix.
- Must verify existing checkpoint inference if model/loss/training code changed.
- Must record no loader or metric semantic change unless a later spec approves
  it.
