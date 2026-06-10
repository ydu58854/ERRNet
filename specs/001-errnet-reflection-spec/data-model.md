# Data Model: ERRNet 单图反射去除课程实验

## ExperimentProject

**Purpose**: Represents the overall DIP26 ERRNet course project.

**Fields**:
- `title`: ERRNet single image reflection removal experiment.
- `deadline`: `2026-06-16 17:00`.
- `submission_email`: course submission address from the guide.
- `branch_or_commit`: Git reference used for experiments.
- `members`: group members and contribution notes.

**Relationships**:
- Has many `Dataset`.
- Has many `ExperimentRun`.
- Has many `EvaluationResult`.
- Has one `DeliveryPackage`.

**Validation Rules**:
- Deadline, submission target, and contribution statement must be documented.
- Code reference must be recorded before final reporting.

## Dataset

**Purpose**: Represents a training, benchmark, or custom-image dataset.

**Fields**:
- `name`: Pascal VOC, real89, CEILNet Table 2, real20, objects, postcard,
  wild, sir2_withgt, or custom five images.
- `raw_path`: source directory or archive location when applicable.
- `processed_path`: processed directory used by ERRNet when applicable.
- `count`: expected or observed sample count.
- `has_ground_truth`: whether full-reference metrics are valid.
- `image_semantics`: single-image reflection removal input/output.
- `usage`: training, finetuning, benchmark evaluation, or qualitative analysis.

**Relationships**:
- Used by one or more `ExperimentRun`.
- Produces one or more `EvaluationResult`.

**Validation Rules**:
- Benchmark datasets used for metrics must have ground truth.
- Custom images without references must be marked qualitative.
- Count discrepancies must be explained in experiment records.
- Resize, crop, augmentation, loader, or mask semantics must not change unless
  spec, plan, and tasks are updated first.

## ModelMethod

**Purpose**: Represents a method being evaluated.

**Fields**:
- `name`: baseline or improved method name.
- `checkpoint_path`: local checkpoint or external weight link.
- `change_summary`: baseline, loss-weight improvement, or other explicitly
  approved change.
- `default_compatibility`: whether current defaults preserve baseline behavior.
- `checkpoint_compatibility`: whether the existing ERRNet checkpoint can load
  and run default inference after changes.
- `compute_notes`: resource requirements and training/inference assumptions.

**Relationships**:
- Used by one or more `ExperimentRun`.
- Compared in one or more `EvaluationResult`.

**Validation Rules**:
- Baseline method must preserve existing ERRNet behavior.
- Improved method must document how it differs from baseline.
- Optional improved-method parameters must default to current baseline behavior.
- Existing pretrained checkpoints must remain usable for default inference.
- New dependencies or extra datasets must have a stated reason.

## ExperimentRun

**Purpose**: Represents one reproducible training, finetuning, benchmark, or
custom-image run.

**Fields**:
- `run_name`: value mapped to existing ERRNet experiment naming.
- `method`: linked `ModelMethod`.
- `dataset`: linked `Dataset`.
- `command`: reproducible command or run description.
- `environment`: OS, Python, dependency versions, CUDA/CPU, GPU model.
- `parameters`: epoch, batch size, learning rate, loss settings, seed.
- `tensor_notes`: expected input/output tensor shape, dtype, and device for
  changed loss or model paths when applicable.
- `output_path`: checkpoint or results directory.
- `status`: planned, completed, blocked, or skipped.
- `notes`: known differences, limitations, or failure observations.

**Relationships**:
- Produces zero or more `EvaluationResult`.
- Provides evidence for `DeliveryPackage`.

**Validation Rules**:
- Completed runs must include command, environment, output path, and status.
- Blocked or skipped runs must include the blocker and residual risk.
- Changed loss or model code must have an import/options smoke record that
  includes shape, dtype, and device notes.

## EvaluationResult

**Purpose**: Represents quantitative or qualitative evidence for a method on a
dataset.

**Fields**:
- `method`: linked `ModelMethod`.
- `dataset`: linked `Dataset`.
- `metrics`: PSNR, SSIM, NCC, LMSE when valid.
- `metric_status`: measured, not applicable, or blocked.
- `ground_truth_status`: available, unavailable, mismatched, or invalid.
- `alignment_policy`: how prediction and target images are aligned before
  metric calculation.
- `crop_policy`: whether output/target images are cropped or rejected on size
  mismatch.
- `pixel_range`: expected numeric range for metric inputs.
- `valid_pixel_policy`: whether all finite image pixels are used or an explicit
  mask is applied.
- `invalid_value_status`: NaN/inf check result and handling decision.
- `visual_paths`: input, output, ground truth, crop, error map, or comparison
  images.
- `interpretation`: concise finding, limitation, or failure-case note.

**Relationships**:
- Belongs to an `ExperimentRun`.
- Feeds course paper/PPT evidence mapping.

**Validation Rules**:
- Full-reference metrics require `has_ground_truth = true`.
- Qualitative-only results must explicitly state why metrics are unavailable.
- Reported metrics must state alignment, crop, pixel range, ground-truth,
  valid-pixel, and invalid-value handling.
- NaN/inf, missing ground truth, or size mismatch must produce `blocked` or
  `not applicable` metric status rather than an unqualified score.
- Comparisons must identify both baseline and improved method evidence.
- Improved-method qualitative comparison must include all five custom images or
  a blocker for each missing output.

## DeliveryPackage

**Purpose**: Tracks ERRNet PJ evidence and final course submission readiness.

**Fields**:
- `paper_status`: draft, reviewed, final, or missing.
- `paper_evidence_mapping`: links from paper sections to experiment records.
- `code_repo_link`: URL or local status.
- `weight_link`: URL or local status.
- `ppt_status`: draft, reviewed, final, or missing.
- `ppt_evidence_mapping`: links from slide sections to experiment records.
- `member_contributions`: completed or missing.
- `submission_status`: not sent, sent, or blocked.

**Relationships**:
- Summarizes all `ExperimentRun` and `EvaluationResult` evidence.

**Validation Rules**:
- Final package must include paper, code link, weight link, PPT, and
  contribution statement or a documented missing reason.
- Submission must use the deadline and email format from the course guide.
- This ERRNet PJ feature tracks evidence and readiness; final paper/PPT authoring
  and external upload/submission are out of scope unless separately requested.
