# Feature Specification: Phase C Exclusion-Loss Experiment

**Feature Branch**: `003-phasec-exclusion-loss`

**Created**: 2026-05-29

**Status**: Draft

**Input**: User description: "另开 Phase C/D 的 loss 或数据策略实验"

## Scope *(mandatory)*

**In Scope**:

- Add a default-disabled Phase C exclusion-loss experiment to ERRNet training.
- Expose a user-controlled `lambda_exclusion` option for aligned and unaligned
  training commands.
- Use the existing input image, model output, and `input - output` residual
  proxy to penalize shared transmission/residual gradient structure.
- Provide repeatable smoke checks and benchmark/custom evaluation guidance for
  a small exclusion-loss experiment.
- Record assumptions, risks, commands, and initial verification evidence in the
  experiment documentation.

**Out of Scope**:

- Phase D data strategy changes, including dataset loader changes, synthetic
  image generation changes, crop/resize/augmentation semantics, new datasets,
  or curriculum scheduling changes.
- Network architecture changes, new model outputs, reflection-layer supervision,
  metric implementation changes, and new runtime dependencies.
- Full long training by default during implementation. Long training may be run
  later using the documented commands after the smoke path is verified.

**Existing Behavior to Preserve**:

- Existing commands without `lambda_exclusion` must behave exactly as before.
- Baseline checkpoints, aligned improved checkpoints, Phase B checkpoints, data
  layouts, loader semantics, and benchmark metric definitions must remain
  unchanged.
- Checkpoint format and old checkpoint inference must remain compatible.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Default-Safe Exclusion Option (Priority: P1)

As an experimenter, I want a default-disabled exclusion-loss option so I can
start Phase C without changing prior baseline, aligned, or Phase B experiment
behavior.

**Why this priority**: It is the minimum viable slice. Without a default-safe
option, the project cannot add Phase C while preserving existing evidence.

**Independent Test**: Run option/help, import, and tensor-level loss checks to
confirm the option exists, defaults to zero, and old loss behavior is unchanged
unless the option is enabled.

**Acceptance Scenarios**:

1. **Given** an existing training command without an exclusion option, **When**
   options are parsed, **Then** the exclusion weight is zero and no exclusion
   term is added to the generator loss.
2. **Given** a small tensor batch, **When** exclusion loss is evaluated with a
   positive weight, **Then** the loss is finite, non-negative, differentiable,
   and produces finite gradients.

---

### User Story 2 - Smoke-Run Phase C Training (Priority: P2)

As an experimenter, I want a bounded smoke training command using a small
exclusion weight so I can verify the Phase C path before committing GPU time to
a longer experiment.

**Why this priority**: A smoke run catches integration, logging, checkpoint, and
numerical problems early while keeping resource usage small.

**Independent Test**: Run a short training command with `lambda_exclusion > 0`,
small dataset size, and CPU or single-card CUDA; verify the command exits with
status `0`, logs an `Excl` loss value, and writes a loadable checkpoint.

**Acceptance Scenarios**:

1. **Given** a small training subset and `lambda_exclusion=0.001`, **When** the
   smoke command runs, **Then** it completes without NaN/Inf loss values and
   writes a checkpoint.
2. **Given** the smoke checkpoint, **When** it is loaded by the existing test
   command, **Then** inference completes without changing metric semantics.

---

### User Story 3 - Evaluation Guidance For Longer Phase C Runs (Priority: P3)

As an experimenter preparing the course report, I want clear commands and
success criteria for longer Phase C runs so that future results are comparable
with baseline, aligned improved, and Phase B evidence.

**Why this priority**: It prevents ad hoc long experiments and makes any later
claim traceable to the same six benchmarks and custom-image workflow.

**Independent Test**: Review the generated quickstart and experiment record to
confirm they include the long-run command, six benchmark commands, custom
evaluation command, output naming, status checks, and decision rules.

**Acceptance Scenarios**:

1. **Given** a future Phase C checkpoint, **When** the documented evaluation
   commands are followed, **Then** outputs and logs are named distinctly from
   baseline, aligned, and Phase B artifacts.
2. **Given** future metrics, **When** the decision rules are applied, **Then**
   the report can state whether Phase C is improved, mixed, or rejected without
   overriding benchmark evidence with custom-image-only observations.

### Edge Cases

- `lambda_exclusion=0`: the option must disable the term completely and not
  add a logged `Excl` metric.
- Degenerate or constant tensors: exclusion loss must stay finite and must not
  divide by zero.
- Unaligned samples: the same residual-gradient proxy may be used, but the
  feature must not require paired reflection ground truth.
- Large positive weights: documentation must warn that over-smoothing and
  background-edge suppression are possible risks.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose a training option named `lambda_exclusion`
  with default value `0.0`.
- **FR-002**: System MUST preserve existing training behavior when
  `lambda_exclusion` is omitted or set to `0.0`.
- **FR-003**: System MUST compute exclusion loss from existing tensors only:
  transmission output and `input - output` residual proxy.
- **FR-004**: System MUST keep exclusion loss finite for normal and degenerate
  tensor inputs by avoiding zero-denominator gradient normalization.
- **FR-005**: System MUST add the weighted exclusion term to the generator loss
  only when `lambda_exclusion > 0`.
- **FR-006**: System MUST log the unweighted exclusion loss value in current
  training errors only when the term is active.
- **FR-007**: System MUST not change network architecture, checkpoint schema,
  datasets, loaders, metrics, or dependencies.
- **FR-008**: System MUST document smoke, benchmark, and custom evaluation
  commands for any Phase C exclusion-loss experiment.
- **FR-009**: System MUST document Phase D data strategy as out of scope for
  this feature and require a separate plan before data semantics change.

### Key Entities

- **Exclusion-Loss Option**: User-controlled scalar weight. Default `0.0`
  preserves previous behavior; positive values activate the Phase C term.
- **Residual Proxy**: Existing `input - output` tensor used as a low-cost
  approximation of reflection residual for gradient-correlation penalization.
- **Phase C Run Record**: Evidence entry containing command, status, checkpoint,
  loss health, benchmark/custom outputs, and conclusion.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Existing option/help and syntax checks pass with
  `lambda_exclusion` present and defaulting to `0.0`.
- **SC-002**: A tensor smoke check with positive `lambda_exclusion` returns a
  finite, non-negative loss and finite gradients.
- **SC-003**: A bounded Phase C smoke training run exits with status `0`, logs
  a finite `Excl` value, and writes a loadable checkpoint.
- **SC-004**: Old-checkpoint inference or a benchmark smoke command still runs
  with `lambda_exclusion=0.0`, demonstrating compatibility.
- **SC-005**: Documentation includes repeatable commands and explicit decision
  rules for comparing Phase C against baseline, aligned improved, and Phase B.

## Assumptions

- The existing `errnet` conda environment is available for smoke checks.
- `input - output` is only a residual proxy; it is not treated as ground-truth
  reflection in reporting.
- A small initial weight such as `0.001` is safer than `0.005` or `0.01` for
  smoke validation.
- CPU smoke checks are acceptable for compatibility; longer runs should use the
  existing single-card CUDA path when available.
- Phase D data strategy needs a separate feature because loader and data
  semantics have wider blast radius than a default-disabled loss option.

## Verification Plan *(mandatory)*

- Run Python syntax checks for touched training option, loss, and model files.
- Run a tensor-level exclusion-loss smoke check for finite forward and backward
  values.
- Run training help/options check and confirm `lambda_exclusion` is present.
- Run a bounded training smoke command with a small dataset and positive
  exclusion weight; verify status `0`, finite `Excl` logging, and checkpoint
  creation.
- Run a load/inference smoke using the generated checkpoint or existing
  checkpoint to confirm checkpoint compatibility.
- Run `git diff --check` on changed files.

## Artifact Synchronization *(mandatory)*

- **Tests**: Update required through repeatable smoke commands recorded in
  experiment docs; no new test framework is required.
- **Documentation**: Update required in `ERRNet/README_DIP26.md`,
  `ERRNet/experiments/results-improved.md`, `improvement.md`, and `todo.md`.
- **Configuration/Scripts**: Update required only for existing option/model/loss
  files; no new runner or dataset script should be added.
- **Dependencies**: No new dependencies.
