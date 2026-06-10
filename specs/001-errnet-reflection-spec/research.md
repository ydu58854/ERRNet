# Research: ERRNet 单图反射去除课程实验

## Decision: Use Existing ERRNet Scripts As The Execution Surface

**Rationale**: `test_errnet.py`, `train_errnet.py`, and
`train_errnet_unaligned.py` already cover benchmark evaluation, custom-image
inference, aligned training, and unaligned finetuning. Reusing them preserves
the course guide and avoids a second orchestration layer.

**Alternatives considered**:
- Add a new experiment runner. Rejected because it duplicates existing script
  behavior and expands scope.
- Rewrite data loading or evaluation. Rejected because current dataset keys and
  metrics already match the guide.

## Decision: Treat Custom Images As Qualitative By Default

**Rationale**: The five custom images in `5pictures/` do not include paired
reflection-free ground truth. PSNR, SSIM, NCC, and LMSE require a reference
image, so the default interpretation must be qualitative analysis.

**Alternatives considered**:
- Report full-reference metrics anyway. Rejected because that would be invalid
  without ground truth.
- Require paired custom captures now. Rejected because it expands data
  collection beyond the current feature unless explicitly requested.

## Decision: Default Improved Method Is Local Loss-Weight Experimentation

**Rationale**: `models/losses.py` already contains `GradientLoss` and
`MultipleLoss`, and `ERRNetModel.backward_G()` already aggregates pixel, VGG,
GAN, and contextual losses. Parameterizing or documenting a structural
loss-weight experiment is the smallest viable improvement path that preserves
architecture and avoids new dependencies.

**Alternatives considered**:
- Add a transformer or attention module. Rejected for this plan because it
  changes architecture and raises compute risk.
- Add a new dataset synthesis pipeline. Rejected because it changes data
  assumptions and requires broader validation.
- Add post-processing. Deferred because it may affect output comparability and
  does not exercise the baseline training flow.

## Decision: Preserve Baseline Behavior By Default

**Rationale**: The baseline results and course guide depend on current default
commands. Any future optional argument must default to the current behavior so
existing commands keep working. If loss-option or model-reporting code changes,
the existing `ERRNet/checkpoints/errnet/errnet_060_00463920.pt` checkpoint must
still load and run default inference.

**Alternatives considered**:
- Change default loss weights or training protocol. Rejected because it would
  make baseline reproduction ambiguous.
- Require a new checkpoint format for the improved method. Rejected because it
  would break baseline compatibility and exceed the local-change constraint.

## Decision: Record Metric Semantics Instead Of Changing Metrics

**Rationale**: The current feature needs reproducible evidence, not a new
metric implementation. Reported PSNR, SSIM, NCC, and LMSE values must therefore
record prediction/target alignment, crop policy, pixel range, ground-truth
status, mask or valid-pixel policy, and NaN/inf handling so paper tables are
interpretable without changing `ERRNet/util/index.py`.

**Alternatives considered**:
- Modify metric code to normalize every edge case. Rejected because that would
  alter existing evaluation behavior and require broader regression testing.
- Report metric values without validity notes. Rejected because missing ground
  truth, size mismatch, or invalid values can make scores misleading.

## Decision: Use Documentation And Experiment Records For Delivery Tracking

**Rationale**: The course deliverables include paper, repository link, weight
link, PPT, and contribution statements. For this ERRNet PJ spec, the repository
work should track evidence and readiness in simple documents/checklists rather
than generate final paper/PPT assets or perform external submission actions.

**Alternatives considered**:
- Add a database or tracking tool. Rejected as unnecessary for a single course
  project.
- Store generated binary results in planning artifacts. Rejected because large
  images/checkpoints should remain in result/checkpoint locations or external
  links.
- Generate the final paper/PPT in this implementation plan. Rejected because
  the current spec is limited to ERRNet PJ experiment execution and evidence
  preparation.
