# Research: ERRNet Improved Retraining Checkpoint

## Decision: Reuse Existing Aligned Training As The Full Retraining Surface

**Rationale**: `ERRNet/train_errnet.py` already implements the aligned ERRNet
training protocol, including the 60-epoch loop, learning-rate schedule,
fusion-ratio adjustment, logging, and checkpoint saves. Reusing it is the
smallest path to a genuine retrained checkpoint and avoids a parallel training
system.

**Alternatives considered**:
- Add a new retraining runner. Rejected because it duplicates existing
  behavior and increases scope.
- Use `train_errnet_unaligned.py` for this feature. Rejected because the spec
  clarifies non-resumed 60-epoch aligned retraining.
- Treat the previous smoke run as sufficient. Rejected because spec1 recorded
  that no full retraining occurred.

## Decision: Use Fixed Spec1 Loss Weights For The Approved Improved Run

**Rationale**: The clarified spec fixes the improved configuration at pixel
loss weight `0.2` and gradient loss weight `0.4`. These options already exist,
were smoke-verified in spec1, and preserve default-compatible behavior.

**Alternatives considered**:
- Tune new weights during this feature. Rejected because it would turn the
  checkpoint feature into a hyperparameter search.
- Change default weights. Rejected because baseline compatibility must remain
  stable.

## Decision: Use `errnet_improved_retrain_60ep` As Canonical Experiment Identity

**Rationale**: A fixed experiment name maps directly to the existing
`checkpoints/{experiment_name}` convention, makes the final artifact easy to
verify, and avoids conflating the final checkpoint with prior smoke outputs.

**Alternatives considered**:
- Date-stamped names. Rejected because they make downstream tasks and report
  references less stable.
- Any distinct name. Rejected because it weakens acceptance checks.

## Decision: Evaluate The New Checkpoint On All Spec1 Benchmarks And Custom Images

**Rationale**: Spec1 already established six benchmark rows and five custom
images as the comparison surface. Reusing the same surface gives a fair
baseline-vs-improved comparison and prevents an under-validated checkpoint from
being treated as report-ready.

**Alternatives considered**:
- Evaluate only `ceilnet_table2`. Rejected because it is not enough for the
  course comparison scope.
- Make the remaining five benchmarks optional. Rejected because the clarified
  acceptance criteria require full comparison.

## Decision: Record Checksum And Completion Evidence For The Final Checkpoint

**Rationale**: The checkpoint is the core artifact. A stable path plus checksum
allows later report writing, sharing, or task handoff to refer to the exact
model rather than an ambiguous latest file.

**Alternatives considered**:
- Record only the directory. Rejected because directories may contain multiple
  epoch/latest artifacts.
- Record only command logs. Rejected because logs do not uniquely identify the
  model file.

## Decision: Allow Localized Code Fixes Only As Training Blocker Unblockers

**Rationale**: The clarified spec permits localized model, loss, or
training-path changes if full retraining exposes blockers, while preserving
defaults. This keeps the implementation practical without opening the door to
architecture, loader, metric, or dependency changes.

**Alternatives considered**:
- Documentation/artifact-only work. Rejected because a real 60-epoch run may
  expose code blockers that must be fixed.
- Broad model redesign. Rejected because it conflicts with minimal scope and
  would invalidate existing comparison assumptions.

## Decision: Keep Metric And Loader Semantics Read-Only

**Rationale**: The feature is about producing and validating a new checkpoint,
not redefining evaluation. Existing metric and loader semantics were already
used for spec1 baseline evidence, so preserving them keeps comparison valid.

**Alternatives considered**:
- Improve metric handling during this feature. Rejected because it changes the
  comparison contract and requires broader regression tests.
- Change dataset preparation or augmentation. Rejected because it would make
  the new checkpoint harder to compare with spec1 baseline evidence.
