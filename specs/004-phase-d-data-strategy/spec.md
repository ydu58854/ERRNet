# Feature Specification: Phase D Data Strategy Experiment

**Feature Branch**: `004-phase-d-data-strategy`

**Created**: 2026-05-30

**Status**: Implemented MVP

**Input**: User description: "若 Phase C 30epoch 仍不成功，则进入计划下一步，另开 Phase D 数据策略实验"; follow-up "转入phaseD，制定计划并实施"

## Scope *(mandatory)*

**In Scope**:

- Plan and execute an MVP Phase D experiment focused on ERRNet training data strategy after the
  Phase C `lambda_exclusion=0.001` 30epoch candidate failed to reach baseline or
  aligned epoch-60 quality.
- Define a small, reversible candidate matrix for synthetic reflection
  parameters and curriculum staging.
- Identify the exact data semantics that may change: blur sigma range, gamma
  range, reflection strength/opacity, optional color perturbation, and staged
  training order. Implement only the first single-variable gamma candidate for
  this MVP.
- Define and apply validation samples, benchmark alignment, logging, output
  naming, rollback rules, and decision criteria before accepting any Phase D
  training result.
- Keep Phase D implementation default-disabled or isolated so existing
  baseline, aligned, Phase B, and Phase C evidence remains reproducible.

**Out of Scope**:

- No data loader, dataset file, augmentation, crop/resize, model, loss, metric,
  checkpoint schema, or training script behavior is changed. The implemented
  option preset only forwards explicit gamma values to the existing synthetic
  data path.
- No full 60/80 epoch training is launched for a Phase D candidate until a
  10/20epoch screen shows a strong signal.
- No new external dataset or dependency is introduced.
- No custom-image full-reference metrics are claimed without paired ground
  truth.

**Existing Behavior to Preserve**:

- Existing `train_errnet.py`, `train_errnet_unaligned.py`, and `test_errnet.py`
  commands must remain valid.
- Existing processed benchmark directories, metric definitions, and result
  image conventions must remain unchanged.
- Existing experiment records for baseline, aligned improved, Phase B, and
  Phase C must remain comparable and must not be overwritten.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Define Safe Phase D Candidate Matrix (Priority: P1)

As an experimenter, I want a bounded Phase D data-strategy matrix so I can test
whether synthetic reflection distribution changes are worth implementing.

**Why this priority**: It prevents ad hoc loader edits and keeps the first data
strategy step small enough to verify and roll back.

**Independent Test**: Review the spec/plan/research documents and confirm that
each candidate names the data semantic being changed, the expected effect, the
risk, and the stop condition. Parse options to confirm `none` preserves old
defaults and `gamma_1p1_1p5` applies only `low_gamma=1.1/high_gamma=1.5`.

**Acceptance Scenarios**:

1. **Given** the Phase C 30epoch result is below baseline/aligned-60, **When**
   Phase D planning is reviewed, **Then** the next candidates are data strategy
   candidates rather than more Phase C long training.
2. **Given** a candidate changes synthetic reflection generation, **When** the
   candidate is listed, **Then** it includes the parameter range, target
   datasets, risk, and rollback rule.
3. **Given** the default training command omits `--phase_d_candidate`, **When**
   options are parsed, **Then** old synthetic gamma defaults remain `1.3/1.3`.

---

### User Story 2 - Preserve Benchmark Comparability (Priority: P2)

As an experimenter preparing the report, I want Phase D evaluation to use the
same benchmark and custom workflow so any improvement claim remains comparable.

**Why this priority**: Phase D changes data semantics, so evaluation must remain
strictly aligned with prior evidence to avoid untraceable gains.

**Independent Test**: Check quickstart and tasks for the same six benchmark
datasets, custom output handling, tensor scan, output counts, and log anomaly
scan; verify the first candidate has all status files at `0`.

**Acceptance Scenarios**:

1. **Given** a Phase D checkpoint exists, **When** evaluation commands are
   run, **Then** they use `ceilnet_table2`, `real20`, `postcard`, `objects`,
   `wild`, and `sir2_withgt`.
2. **Given** Phase D custom outputs are generated, **When** results are
   reported, **Then** they are treated as qualitative only unless paired ground
   truth is available.

---

### User Story 3 - Define Implementation Guardrails (Priority: P3)

As a maintainer, I want explicit guardrails before data code changes so the
next implementation can be limited, reversible, and easy to verify.

**Why this priority**: Loader and data-generation semantics have wider blast
radius than a loss flag and need clear boundaries before editing code.

**Independent Test**: Confirm the plan and tasks name the exact files to
inspect or potentially change, require smoke verification before training, and
state that default behavior is preserved unless Phase D options are enabled.

**Acceptance Scenarios**:

1. **Given** the next implementation starts, **When** source changes are made,
   **Then** they are limited to documented data-strategy hooks and docs.
2. **Given** a Phase D candidate fails smoke or tensor checks, **When** recovery
   is attempted, **Then** it can be reverted by disabling Phase D parameters or
   using the old default data path.

### Edge Cases

- Phase D candidates may improve `objects/postcard/sir2_withgt` while
  degrading `real20/wild`; decision rules must handle mixed results.
- Small epoch screening may not predict mature 60epoch behavior; screening is
  only a filter for whether to run a longer candidate.
- A technically healthy candidate can still be rejected if equal-weight
  benchmark averages broadly regress.
- Changing random synthetic parameters may reduce reproducibility; every run
  must record seed, command, data parameters, status, checkpoint, and metrics.
- Any loader failure, empty dataset, non-finite tensor, or benchmark status
  failure must stop the candidate before long training.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The plan MUST identify candidate Phase D data strategy changes
  before implementation modifies data semantics.
- **FR-002**: The implementation MUST preserve existing default training and
  evaluation behavior unless a Phase D option is explicitly enabled.
- **FR-003**: The plan MUST define at least three bounded candidates covering
  gamma range, blur sigma range, and curriculum staging.
- **FR-004**: The feature MUST include validation checks for dataset availability,
  sample decoding, synthetic-pair smoke generation, tensor finite health, six
  benchmark metrics, custom qualitative outputs, output counts, and log anomaly
  scans.
- **FR-005**: The plan MUST define rollback behavior for each data-strategy
  change.
- **FR-006**: The plan MUST document success criteria relative to baseline,
  aligned improved epoch 60, and Phase C epoch 30.
- **FR-007**: The feature MUST not introduce new dependencies or external
  datasets.
- **FR-008**: The feature MUST update `AGENTS.md`, `improvement.md`, `todo.md`,
  README usage notes, and experiment results with Phase C 30epoch conclusions
  and Phase D screening status.

### Key Entities

- **Data Strategy Candidate**: A named bounded change to synthetic reflection
  generation or training schedule, with parameter range, rationale, risk, and
  rollback.
- **Screening Run**: A short Phase D training/evaluation run, typically 10 or
  20 epochs, used only to decide whether longer training is justified.
- **Benchmark Alignment Record**: Evidence tying a Phase D checkpoint to the
  same six benchmark datasets, metric implementation, output counts, and custom
  qualitative workflow used by prior phases.
- **Rollback Rule**: The documented way to return to default data behavior when
  a candidate fails.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Phase D spec, plan, research, data model, quickstart, and tasks
  exist under `specs/004-phase-d-data-strategy/`.
- **SC-002**: The Phase D plan names exact candidate parameters and exact
  verification commands, and the first implementation preserves old defaults.
- **SC-003**: The task list contains independently testable steps for candidate
  design, smoke verification, benchmark evaluation, and documentation.
- **SC-004**: `AGENTS.md` points to the Phase D plan, and `todo.md` records that
  Phase C long training has stopped after epoch 30.
- **SC-005**: Static documentation checks (`git diff --check` and placeholder
  scan) pass for changed planning artifacts.
- **SC-006**: The first Phase D screening candidate has training, tensor scan,
  six benchmark, custom inference, output count, and anomaly scan evidence.

## Assumptions

- The existing `errnet` conda environment and benchmark data remain available.
- Phase D implementation reuses existing data modules and command patterns
  rather than adding new dependencies.
- Short screening runs are acceptable for deciding whether a candidate deserves
  longer training, but not sufficient for a final improvement claim.
- Phase C `lambda=0.001` should not be extended further unless new evidence
  changes the decision threshold.

## Verification Plan *(mandatory)*

- Run `git diff --check` on Phase C result updates, Phase D specs, and planning
  docs.
- Scan Phase D docs for unresolved template placeholders or unresolved
  clarification markers.
- Verify `.specify/feature.json` and `AGENTS.md` point to
  `specs/004-phase-d-data-strategy/plan.md`.
- Run dataset availability and smoke-generation checks listed in `quickstart.md`
  before training a candidate.

## Artifact Synchronization *(mandatory)*

- **Tests**: Repeatable smoke and benchmark verification commands are required
  for implemented candidates.
- **Documentation**: Update required in Phase D specs plus `improvement.md`,
  `todo.md`, `AGENTS.md`, and `ERRNet/experiments/results-improved.md`.
- **Configuration/Scripts**: No new scripts or configuration. CLI behavior adds
  a default-compatible optional preset.
- **Dependencies**: No new dependencies.
