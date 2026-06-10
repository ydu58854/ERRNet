# Feature Specification: ERRNet Improved Retraining Checkpoint

**Feature Branch**: `002-improved-retraining-checkpoint`

**Created**: 2026-05-26

**Status**: Draft

**Input**: User description: "根据spec1的结果，进行完整 improved retraining，并保存新的 checkpoint。"

## Scope *(mandatory)*

**Goal**: Complete the improved ERRNet retraining phase that follows the spec1 baseline and improved-option smoke results, then produce a new checkpoint that can be used for reproducible benchmark and custom-image comparison.

**Background**: Spec1 established the ERRNet course experiment workflow, verified baseline benchmark/custom-image evaluation, added default-compatible improved loss-weight options, and recorded that a smoke run did not perform full retraining or create a newly trained improved checkpoint. This feature closes that gap by defining the required complete improved retraining outcome and checkpoint evidence.

**In Scope**: Execute and document a full improved retraining run using the approved spec1 improvement direction, save a distinct new improved checkpoint, record the training configuration and completion evidence, verify the checkpoint can be loaded for evaluation, and update experiment records so the new checkpoint can be compared against the spec1 baseline on benchmark and custom-image inputs. If full retraining exposes a blocker, localized model, loss, or training-path changes are in scope only when they directly unblock the approved run and preserve existing defaults.

**Out of Scope**: This feature does not redesign the ERRNet architecture, introduce a new improvement family, change dataset preparation, alter metric definitions, add new dependencies, replace the baseline checkpoint, rewrite existing evaluation behavior, create final paper/PPT deliverables, upload model files externally, or send the course submission email.

**Existing Behavior to Preserve**: Baseline evaluation results, existing dataset keys, current metric meanings, default-compatible improved options from spec1, pretrained baseline checkpoint usage, existing output naming conventions, and CPU/single-card compatibility expectations must remain unchanged unless a later approved specification expands scope.

## Clarifications

### Session 2026-05-26

- Q: What completion rule defines full improved retraining for this feature? → A: Full 60-epoch improved aligned retraining from a non-resumed start, using the approved spec1 loss-weight configuration, then save the resulting checkpoint.
- Q: Which improved loss-weight configuration should the full retraining use? → A: Use spec1 default-compatible weights: pixel loss 0.2 and gradient loss 0.4.
- Q: What canonical identity should the new improved checkpoint use? → A: Use experiment name `errnet_improved_retrain_60ep`; final checkpoint must be under `ERRNet/checkpoints/errnet_improved_retrain_60ep/` with recorded checksum.
- Q: What evaluation coverage is required for the new checkpoint? → A: Full comparison on all six spec1 benchmarks plus all five custom images.
- Q: What code/module responsibility boundary applies if full retraining reveals blockers? → A: Allow localized model/loss/training code changes if full retraining reveals blockers, while preserving existing defaults.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Complete Improved Retraining (Priority: P1)

As a project participant, I need to run the approved improved training configuration to completion so the project has a genuinely retrained improved model rather than only an option-parsing or inference smoke result.

**Why this priority**: The current spec1 result explicitly records that full improved retraining was not performed. Without a completed run, the project cannot claim an improved trained model or provide a new checkpoint for downstream comparison.

**Independent Test**: Review the improved training record and confirm it contains a completed non-resumed 60-epoch aligned training status, fixed improved weights of pixel loss 0.2 and gradient loss 0.4, distinct experiment identity, training settings, start/end evidence, and a saved improved checkpoint produced after the run.

**Acceptance Scenarios**:

1. **Given** spec1 baseline and improved-option smoke evidence exists, **When** the improved retraining is completed, **Then** the experiment record identifies a non-resumed 60-epoch aligned training run as complete and distinguishes it from smoke-only or resumed checkpoint-only runs.
2. **Given** the approved improved configuration uses pixel loss weight 0.2 and gradient loss weight 0.4, **When** the run finishes, **Then** the record captures the training settings, duration or completion timestamp, source checkpoint if any, and any deviations from spec1 assumptions.

---

### User Story 2 - Save And Identify New Checkpoint (Priority: P2)

As a project participant, I need the retraining output saved as a distinct checkpoint so later evaluation, reporting, and sharing can reference the exact improved model artifact.

**Why this priority**: A new checkpoint is the concrete artifact that separates this feature from spec1 smoke validation and enables reproducible comparison.

**Independent Test**: Inspect the checkpoint evidence and confirm the saved artifact has a stable path, run name, creation evidence, and checksum record without overwriting the baseline checkpoint.

**Acceptance Scenarios**:

1. **Given** improved retraining completes, **When** the checkpoint is saved, **Then** the artifact is stored under `ERRNet/checkpoints/errnet_improved_retrain_60ep/` and the baseline checkpoint remains available unchanged.
2. **Given** the saved checkpoint is recorded, **When** another contributor reviews the records, **Then** they can identify which training run produced it and how to use it for evaluation.

---

### User Story 3 - Verify Improved Checkpoint Evaluation (Priority: P3)

As a project participant, I need to verify that the new improved checkpoint can run through the established evaluation workflow so the project can compare it with the spec1 baseline on benchmark and custom images.

**Why this priority**: A checkpoint that cannot be loaded or evaluated is not useful for the course report or for future reproduction.

**Independent Test**: Use the saved improved checkpoint for all six spec1 benchmark evaluations and the five custom images, then record output paths, metrics when valid, qualitative status, and any blockers.

**Acceptance Scenarios**:

1. **Given** a saved improved checkpoint exists, **When** it is evaluated on the six spec1 benchmarks with ground truth, **Then** each benchmark result record includes PSNR, SSIM, NCC, LMSE or a precise reason the metrics are unavailable.
2. **Given** the five custom images from spec1 exist, **When** the improved checkpoint is evaluated on them, **Then** each image has a recorded improved output path and qualitative-only status unless ground truth is added.

---

### User Story 4 - Update Project Evidence (Priority: P4)

As a project participant, I need the improved retraining evidence summarized alongside baseline evidence so the final project materials can make clear, traceable claims about the new checkpoint.

**Why this priority**: The training artifact must be tied to evidence before it can support the course report, PPT, or external model link.

**Independent Test**: Review the experiment records and confirm they include the new checkpoint path, training run status, evaluation status, comparison notes, assumptions, and residual risks.

**Acceptance Scenarios**:

1. **Given** improved retraining and evaluation evidence exists, **When** records are updated, **Then** the baseline and improved checkpoint comparison is visible in one place with no ambiguity between smoke and full retraining.
2. **Given** full retraining cannot complete because of compute or data blockers, **When** records are updated, **Then** the blocker, partial artifact status, and remaining risk are explicitly stated.

### Edge Cases

- If retraining stops before completion, the feature must not label the checkpoint as final; records must distinguish partial, latest, and completed artifacts.
- If no new checkpoint is produced, the feature is incomplete unless the record explains the blocker and preserves all prior baseline artifacts unchanged.
- If the improved checkpoint has worse metrics than baseline, the artifact may still be valid, but the comparison record must avoid claiming quality improvement and must report the measured outcome.
- If GPU resources are insufficient, the run may use the smallest project-acceptable fallback only if the record states the compute limitation and the resulting comparability risk.
- If evaluation produces NaN, inf, missing metrics, or missing custom outputs, the record must identify the affected dataset or image and the reason.
- If `ERRNet/checkpoints/errnet_improved_retrain_60ep/` already exists, the feature must preserve or archive the prior contents before producing the new final checkpoint and must record the action taken.
- If training resumes from a prior partial run, that resumed run must not satisfy this feature's full-retraining completion rule; the record may keep it only as supplemental evidence.
- If localized model, loss, or training-path changes are needed to unblock full retraining, the feature must document the blocker, changed responsibility area, default-behavior preservation check, and verification impact before claiming completion.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The feature MUST use the improved method direction approved in spec1 with pixel loss weight 0.2 and gradient loss weight 0.4, and MUST identify this selected improved training configuration in the experiment record.
- **FR-002**: The feature MUST record a complete non-resumed 60-epoch improved aligned retraining run, including experiment identity, initialization choice, key training settings, completion status, and completion evidence.
- **FR-003**: The feature MUST save the new improved checkpoint under experiment identity `errnet_improved_retrain_60ep` without overwriting the spec1 baseline checkpoint or smoke-run artifacts.
- **FR-004**: The feature MUST record stable checkpoint identification details, including path under `ERRNet/checkpoints/errnet_improved_retrain_60ep/`, producing run, creation status, and checksum evidence.
- **FR-005**: The feature MUST verify that the new checkpoint can be loaded for evaluation before it is considered ready for comparison.
- **FR-006**: The feature MUST evaluate the new checkpoint on all six spec1 ground-truth benchmarks and record PSNR, SSIM, NCC, LMSE or a precise reason metrics are unavailable for each benchmark.
- **FR-007**: The feature MUST generate or verify improved outputs for all five custom images from spec1 and record qualitative output paths.
- **FR-008**: The feature MUST compare the new checkpoint against the spec1 baseline evidence using the same metric meanings and clearly state whether results support, do not support, or are insufficient for an improvement claim.
- **FR-009**: The feature MUST preserve baseline default behavior and existing evaluation conventions unless a later approved specification authorizes a change.
- **FR-010**: The feature MUST keep changes local to retraining configuration, checkpoint/evidence recording, directly required verification artifacts, and localized model, loss, or training-path fixes that are necessary to unblock full retraining.
- **FR-011**: The feature MUST record any training interruption, resource limitation, data issue, or evaluation anomaly with residual risk before claiming completion.
- **FR-012**: The feature MUST update project evidence so final report preparation can distinguish spec1 smoke validation from this full improved retraining checkpoint.
- **FR-013**: Any localized model, loss, or training-path fix MUST preserve existing defaults, avoid loader and metric semantic changes, and include a repeatable compatibility verification.

### Key Entities *(include if feature involves data)*

- **Improved Retraining Run**: A completed training attempt for the approved improved method; includes experiment identity, configuration summary, source state, completion evidence, and status.
- **Improved Checkpoint**: The saved model artifact produced by the improved retraining run under `ERRNet/checkpoints/errnet_improved_retrain_60ep/`; includes path, producing run, creation evidence, checksum, and readiness status.
- **Baseline Evidence**: The spec1 benchmark/custom-image results and pretrained checkpoint reference used as the comparison point.
- **Evaluation Result**: Benchmark metrics and custom-image outputs generated from the improved checkpoint, with metric validity and qualitative limitations recorded.
- **Experiment Record**: The documentation tying training, checkpoint, evaluation, comparison, assumptions, and risks together for reproducibility.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: One distinct non-resumed 60-epoch improved aligned retraining run is recorded with completion status, experiment identity, pixel loss weight 0.2, gradient loss weight 0.4, key settings, and completion evidence.
- **SC-002**: One new improved checkpoint is saved under `ERRNet/checkpoints/errnet_improved_retrain_60ep/` and identifiable by path plus checksum evidence.
- **SC-003**: The new checkpoint is load-verified and evaluated on all six spec1 ground-truth benchmarks with four metric values or explicit unavailable reasons for each benchmark.
- **SC-004**: All five spec1 custom images have recorded improved output paths or explicit blocker notes.
- **SC-005**: The improved-vs-baseline comparison record states the outcome for all six spec1 benchmarks and all five custom images without conflating smoke validation with full retraining.
- **SC-006**: The feature evidence lists all known assumptions, resource constraints, and residual risks before the checkpoint is considered ready for report use.

## Assumptions

- The approved improved direction remains the local loss-weight experiment established in spec1, fixed for this feature at pixel loss weight 0.2 and gradient loss weight 0.4; a different method or weight pair would require a new or updated specification.
- The relevant baseline evidence is the spec1 benchmark/custom-image record and the original ERRNet baseline checkpoint.
- Full retraining means a non-resumed 60-epoch improved aligned training run for the selected configuration that saves a checkpoint intended for evaluation, not a resumed checkpoint-only pass, option parse, smoke test, or inference-only run.
- Custom images still lack ground truth by default, so they remain qualitative unless paired references are added later.
- Available compute is expected to support at least one complete improved training run; if not, the blocker and comparability risk must be recorded.
- No new dependencies are expected. Existing environment and data preparation assumptions from spec1 remain in force.
- The main risk is training time or GPU availability preventing completion; the main tradeoff is preserving a small local improvement scope rather than attempting a larger architecture change.
- Localized model, loss, or training-path fixes are allowed only as unblockers for full retraining; broader redesign, loader changes, metric changes, and new dependencies remain out of scope.

## Verification Plan *(mandatory)*

- Confirm the feature directory contains this specification and a completed quality checklist with no unresolved clarification markers.
- Confirm the improved retraining record identifies a completed non-resumed 60-epoch aligned training run with pixel loss weight 0.2 and gradient loss weight 0.4, rather than a resumed checkpoint-only or smoke-only result.
- Confirm the new checkpoint exists under `ERRNet/checkpoints/errnet_improved_retrain_60ep/`, is distinct from the baseline checkpoint, and has path plus checksum evidence recorded.
- Confirm the new checkpoint can be loaded for evaluation.
- Confirm all six spec1 benchmark results include PSNR, SSIM, NCC, LMSE or precise unavailable reasons using the same metric meanings as spec1.
- Confirm all five custom images have improved output paths or explicit blocker notes.
- Confirm comparison notes state whether the improved checkpoint supports an improvement claim, fails to improve, or is inconclusive.
- If localized model, loss, or training-path changes were made, confirm defaults still preserve spec1 behavior and existing checkpoint evaluation remains compatible.
- Run static formatting checks on changed specification and evidence files before reporting completion.

## Artifact Synchronization *(mandatory)*

- **Tests**: Update required - verification must include checkpoint load/evaluation evidence and custom-image output checks.
- **Documentation**: Update required - improved retraining results, checkpoint identity, comparison notes, assumptions, and risks must be recorded.
- **Configuration/Scripts**: Update if required - directly required retraining configuration changes and localized model, loss, or training-path fixes are in scope only when they unblock full retraining, and defaults must preserve spec1 behavior.
- **Dependencies**: No new dependencies - any proposed dependency would require a separate reason, benefit, and verification impact.
