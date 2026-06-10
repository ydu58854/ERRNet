# Implementation Plan: Phase D Data Strategy Experiment

**Branch**: `004-phase-d-data-strategy` | **Date**: 2026-05-30 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/004-phase-d-data-strategy/spec.md`

## Summary

Phase C `lambda_exclusion=0.001` reached epoch 30 with finite checkpoints and
successful benchmark/custom evaluation, but its averages stayed below baseline
and aligned improved epoch 60. Phase D therefore defines a separate data
strategy experiment with bounded candidates, verification gates, rollback
rules, and evaluation alignment. Per the follow-up request to implement Phase D,
the first MVP candidate `gamma_1p1_1p5` has been implemented as a
default-compatible option and screened for 10 epochs.

## Technical Context

**Language/Version**: Python 3.10 in the existing `errnet` conda environment for
implementation and verification checks.

**Primary Dependencies**: Existing ERRNet dependencies only: PyTorch,
TorchVision, OpenCV/skimage, visdom, tensorboardX, and packages already covered
by the repository environment. No new dependencies.

**Storage**: Existing local filesystem checkpoints, logs, and result images
under `ERRNet/checkpoints/`, `ERRNet/experiments/run-logs/`, and
`ERRNet/results/`.

**Testing**: Documentation validation plus implementation checks for the first
candidate: dataset availability, synthetic sample smoke, syntax checks, option
default checks, tensor finite checks, 10epoch screening, six benchmark
evaluations, custom qualitative outputs, output counts, and anomaly scans.

**Target Platform**: Linux workstation/server with the existing `errnet`
environment. Single-card CUDA is expected for short/long training; CPU may be
used for static and dataset inspection.

**Project Type**: ML repository with CLI-style training and evaluation scripts.

**Performance Goals**: Screening runs should stay bounded at 10 or 20 epochs
before any full 60epoch candidate. Data changes must not add avoidable per-sample
overhead beyond existing synthetic generation.

**Constraints**: Preserve existing defaults, benchmark metrics, result naming
patterns, checkpoint compatibility, and prior experiment evidence. Any data
semantic change must be enabled explicitly and must have a rollback path.

**Scale/Scope**: MVP implementation only. The completed source change adds one
default-compatible data-strategy hook and one candidate preset. Other matrix
candidates remain deferred until separately selected and smoke-verified.

## Constitution Check

*GATE: Passed before Phase 0 research. Re-check after Phase 1 design.*

- **Scope Control**: Smallest viable implementation is one explicit candidate
  preset in the existing options path. No model, metric, dataset file, external
  dependency, benchmark script, or checkpoint schema changes are included.
- **Existing Contracts**: Existing training/evaluation commands, loaders,
  metrics, checkpoints, and results remain valid because `--phase_d_candidate
  none` is the default.
- **Reuse First**: Implementation reuses existing
  `ERRNet/data/reflect_dataset.py`/`ERRNet/data/transforms.py` synthetic gamma
  controls, option patterns, run-log conventions, and benchmark/custom
  evaluation commands.
- **Verification Path**: Verification includes `git diff --check`, placeholder
  scans, feature pointer checks, syntax checks, option/default checks, synthetic
  sample smoke, 10epoch training, tensor scan, six benchmark evaluations,
  custom inference, output counts, and anomaly scans.
- **Assumptions And Risks**: Small epoch screening may not predict full
  convergence. Data strategy can improve one dataset group while hurting
  another. Synthetic distribution changes must remain reversible.
- **Synchronized Artifacts**: Update Phase C result evidence, Phase D screening
  evidence, `improvement.md`, `todo.md`, `AGENTS.md`, README usage notes, and
  Phase D spec artifacts together.
- **Dependency Discipline**: No new dependencies.
- **Completion Evidence**: Final report must include Phase C 30epoch result,
  Phase D code/doc artifact paths, screening verification results, assumptions,
  and residual risks.

## Project Structure

### Documentation (this feature)

```text
specs/004-phase-d-data-strategy/
├── spec.md
├── checklists/
│   └── requirements.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── phase-d-data-strategy-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
ERRNet/
├── data/reflect_dataset.py         # inspected/reused; no source edit
├── data/transforms.py              # inspected/reused; no source edit
├── options/errnet/base_options.py  # option postprocess hook
├── options/errnet/train_options.py # Phase D candidate preset
├── train_errnet.py                # future command compatibility check only
└── experiments/results-improved.md

AGENTS.md
improvement.md
todo.md
```

**Structure Decision**: The implementation stays in existing ERRNet option
paths and reuses existing data-generation parameters. It avoids new packages,
datasets, metrics, runner scripts, loader rewrites, and checkpoint schema
changes.

## Complexity Tracking

No constitution violations are required.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
