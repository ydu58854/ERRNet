# Implementation Plan: Phase C Exclusion-Loss Experiment

**Branch**: `003-phasec-exclusion-loss` | **Date**: 2026-05-29 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/003-phasec-exclusion-loss/spec.md`

## Summary

Open a new Phase C experiment by adding a default-disabled exclusion-loss term
to ERRNet training. The term uses existing tensors only: transmission output
and `input - output` residual proxy. The implementation preserves old behavior
when `--lambda_exclusion` is omitted or `0.0`, adds smoke-level verification,
and documents longer benchmark/custom evaluation commands. Phase D data
strategy remains out of scope for this feature.

## Technical Context

**Language/Version**: Python 3.10 in the existing `errnet` conda environment.

**Primary Dependencies**: Existing ERRNet dependencies only: PyTorch,
TorchVision, OpenCV/skimage, visdom, tensorboardX, and packages already covered
by the repository environment. No new dependencies.

**Storage**: Local filesystem checkpoints, logs, and result images under
`ERRNet/checkpoints/`, `ERRNet/experiments/run-logs/`, and `ERRNet/results/`.

**Testing**: Python syntax checks, option/help checks, tensor forward/backward
smoke, bounded training smoke, checkpoint load/inference smoke, output/log
inspection, and `git diff --check`.

**Target Platform**: Linux workstation/server with the existing `errnet`
environment. CPU is acceptable for tensor and short compatibility checks;
single-card CUDA is preferred for longer training.

**Project Type**: ML repository with CLI-style training and evaluation scripts.

**Performance Goals**: Exclusion loss should add minimal overhead relative to
existing gradient loss and should not block short smoke training. Long-run
quality is measured by the existing six benchmarks and custom-image review.

**Constraints**: Preserve existing defaults, loaders, metrics, architecture,
checkpoint schema, and old checkpoint inference. Do not alter data generation
or Phase D strategy in this feature. Avoid new dependencies and new runner
scripts.

**Scale/Scope**: One default-disabled loss option, one localized loss module,
two training-loss integration points, documentation/evidence updates, and one
bounded smoke training path.

## Constitution Check

*GATE: Passed before Phase 0 research. Re-check after Phase 1 design.*

- **Scope Control**: Smallest viable change is a default-disabled loss option
  and local training integration. Phase D loader/data changes, network changes,
  metrics, and long full training are out of scope.
- **Existing Contracts**: Existing commands without `--lambda_exclusion` keep
  the same loss terms, checkpoints, metrics, and outputs. New command surface is
  additive and default-compatible.
- **Reuse First**: Reuse `TrainOptions`, `ContentLoss`, `compute_gradient`,
  `ERRNetModel.backward_G`, `NetworkWrapper.backward_G`, `Engine`, and existing
  experiment docs/run-log conventions.
- **Verification Path**: Syntax checks, tensor finite forward/backward, option
  presence/default checks, bounded smoke training, checkpoint load/inference
  smoke, and static diff checks.
- **Assumptions And Risks**: `input - output` is a residual proxy, not ground
  truth reflection. Too-large weights can over-smooth background edges.
- **Synchronized Artifacts**: Update spec/plan/tasks, README usage, experiment
  evidence, `improvement.md`, and `todo.md`.
- **Dependency Discipline**: No new dependencies.
- **Completion Evidence**: Final summary must state changed files,
  verification commands/results, assumptions, tradeoffs, and remaining risks.

## Project Structure

### Documentation (this feature)

```text
specs/003-phasec-exclusion-loss/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── errnet-phasec-cli-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
ERRNet/
├── options/errnet/train_options.py
├── models/losses.py
├── models/errnet_model.py
├── README_DIP26.md
└── experiments/results-improved.md

improvement.md
todo.md
AGENTS.md
```

**Structure Decision**: Keep the implementation in the existing ERRNet option,
loss, model, and documentation paths. No new package, runner, dependency,
dataset directory, or metric module is introduced.

## Complexity Tracking

No constitution violations are required.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
