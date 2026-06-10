# Research: Phase D Data Strategy Experiment

## Decision 1: Stop Phase C Long-Training Expansion

**Decision**: Do not extend the current `lambda_exclusion=0.001` Phase C run
beyond the bounded epoch-30 recovery segment.

**Rationale**: The epoch-30 checkpoint is technically healthy but still below
baseline and aligned improved epoch 60 on equal-weight averages. It improves
over epoch 20 but not enough to justify another long segment before exploring a
different hypothesis.

**Alternatives considered**:

- Continue Phase C to 40/60 epochs. Rejected because the epoch-30 gap to
  baseline/aligned-60 remains large and TODO-007C defined epoch 30 as the stop
  gate for switching to Phase D.
- Increase `lambda_exclusion`. Rejected for now because the current weight did
  not show mature quality signal and larger weights increase over-smoothing
  risk without addressing data distribution mismatch.

## Decision 2: Start With Synthetic Parameter Screening

**Decision**: Phase D should first screen small, explicit changes to synthetic
reflection parameters: gamma range, blur sigma range, and reflection
strength/opacity.

**Rationale**: Current evidence shows dataset-dependent behavior. Synthetic-like
and real datasets respond differently, suggesting the training distribution may
not match the benchmark reflection distribution. Parameter screening is smaller
than new datasets or architecture changes.

**Alternatives considered**:

- Add external datasets. Rejected because source, license, preprocessing, and
  storage questions would expand scope.
- Replace the loader wholesale. Rejected because it would break comparability
  and make rollback harder.

## Decision 3: Use Curriculum Only After Single-Parameter Smoke

**Decision**: Treat curriculum staging as a second-level candidate after
single-parameter smoke checks confirm the data hook is controllable and stable.

**Rationale**: Curriculum changes affect training schedule and data semantics at
the same time. It is better to first verify that synthetic parameter controls
produce valid samples and stable short training.

**Alternatives considered**:

- Start with curriculum immediately. Rejected because it makes attribution
  unclear if results change.
- Ignore curriculum. Rejected because the improvement notes identify staged weak
  to strong reflection training as a plausible way to reduce synthetic-to-real
  gap.

## Decision 4: Preserve Evaluation Alignment

**Decision**: Every Phase D candidate must use the same six benchmark datasets,
tensor scan, custom qualitative workflow, output counts, and log anomaly scan as
Phase C.

**Rationale**: Phase D changes data semantics; strict evaluation alignment is
needed to make comparisons defensible.

**Alternatives considered**:

- Evaluate only affected datasets such as `objects/postcard/sir2_withgt`.
  Rejected because improvements there may hide regressions on `real20/wild`.
- Use custom images as the main evidence. Rejected because custom images lack
  paired ground truth.

## Decision 5: Require Default-Compatible Rollback

**Decision**: Future implementation must preserve the old data path by default
and make Phase D behavior explicitly selectable or isolated.

**Rationale**: Existing experiment evidence depends on current data semantics.
Default-compatible rollback protects reproducibility and keeps failures easy to
recover from.

**Alternatives considered**:

- Edit constants in place without an option. Rejected because it makes old and
  new runs hard to reproduce side by side.
