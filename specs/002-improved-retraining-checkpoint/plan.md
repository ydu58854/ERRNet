# Implementation Plan: ERRNet Improved Retraining Checkpoint

**Branch**: `002-improved-retraining-checkpoint` | **Date**: 2026-05-26 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-improved-retraining-checkpoint/spec.md`

## Summary

Complete the spec1 improved-method gap with the smallest reproducible path:
run a non-resumed 60-epoch aligned ERRNet retraining using the already approved
loss-weight configuration, save the resulting checkpoint under
`ERRNet/checkpoints/errnet_improved_retrain_60ep/`, record checksum and run
evidence, then evaluate that checkpoint on all six spec1 benchmark datasets
and all five custom images. The plan reuses the existing ERRNet training,
checkpoint, evaluation, metric, result, and experiment-record conventions.
Localized model, loss, or training-path fixes are allowed only if full
retraining exposes a blocker, and any such fix must preserve existing defaults.

## Technical Context

**Language/Version**: Python 3.10 in the existing ERRNet environment.

**Primary Dependencies**: Existing ERRNet dependencies only: PyTorch,
TorchVision, OpenCV/skimage, visdom, tensorboardX, and packages already covered
by `ERRNet/requirements.txt` or the documented `errnet` environment.

**Storage**: Local filesystem datasets, logs, results, and checkpoints. The
new target checkpoint directory is
`ERRNet/checkpoints/errnet_improved_retrain_60ep/`.

**Testing**: Reproducible training/evaluation commands, checkpoint existence
and checksum checks, command log inspection, metric table inspection, custom
image output inspection, default-compatibility smoke checks if code changes,
and static `git diff --check`.

**Target Platform**: Linux workstation/server with the existing `errnet` conda
environment; single-card CUDA is the expected long-training path. CPU remains
valid for small compatibility checks and inference fallback, not for the
primary 60-epoch training expectation unless GPU is unavailable and the
resource risk is recorded.

**Project Type**: ML repository with CLI-style training and evaluation scripts.

**Performance Goals**: Complete one non-resumed 60-epoch aligned training run
within available course/GPU resources, produce a loadable checkpoint, and run
all six benchmark evaluations plus five custom-image outputs without changing
metric semantics.

**Constraints**: Preserve existing default behavior, dataset keys, metric
definitions, loader semantics, checkpoint format, and baseline checkpoint
availability. Do not add dependencies. Do not create a parallel runner unless
existing scripts cannot complete the approved run and a localized fix is
documented.

**Scale/Scope**: One improved training run, one canonical checkpoint artifact,
six benchmark evaluation rows (`ceilnet_table2`, `real20`, `postcard`,
`objects`, `wild`, `sir2_withgt`), and five qualitative custom-image outputs
from `5pictures/`.

## 1. 实现思路概述

1. Treat spec1 baseline and smoke artifacts as the starting evidence, not as
   sufficient completion for this feature.
2. Use the existing aligned training entrypoint `ERRNet/train_errnet.py` with a
   new experiment name `errnet_improved_retrain_60ep`.
3. Run the training from a non-resumed start for the existing 60-epoch aligned
   protocol, using fixed improved weights `--pixel_loss_weight 0.2` and
   `--gradient_loss_weight 0.4`.
4. Preserve the baseline checkpoint at
   `ERRNet/checkpoints/errnet/errnet_060_00463920.pt`; do not overwrite smoke
   directories such as `ERRNet/checkpoints/errnet_loss_weight_smoke/`.
5. Record command, environment, start/end status, checkpoint path, and checksum
   in `ERRNet/experiments/results-improved.md` or a directly related record.
6. Evaluate the new checkpoint through the existing `ERRNet/test_errnet.py`
   command surface on all six spec1 benchmarks and the five custom images.
7. Compare improved results against spec1 baseline evidence using the same
   metrics and qualitative rules. Worse metrics are valid evidence, but the
   report must not claim improvement unless measured results support it.
8. If full retraining exposes a blocker, make only the smallest localized
   model, loss, or training-path fix needed to unblock the approved run, then
   verify defaults and old checkpoint inference remain compatible.

## 2. 优先检查的代码区域

- `specs/002-improved-retraining-checkpoint/spec.md`: approved scope,
  clarifications, completion rule, and acceptance criteria.
- `ERRNet/train_errnet.py`: aligned training loop, 60-epoch protocol, learning
  rate schedule, fusion ratio schedule, and non-resume behavior.
- `ERRNet/options/errnet/train_options.py`: existing training options,
  `--pixel_loss_weight`, `--gradient_loss_weight`, `--name`, `--resume`, GPU
  settings, and logging options.
- `ERRNet/models/losses.py`: existing `MultipleLoss` and `GradientLoss`
  weighting used by the improved configuration.
- `ERRNet/models/base_model.py`: checkpoint naming and save behavior under
  `checkpoints/{experiment_name}/`.
- `ERRNet/engine.py`: epoch progression, latest checkpoint save, periodic
  epoch checkpoint save, and eval hooks during training.
- `ERRNet/test_errnet.py`: benchmark/custom evaluation entrypoint, dataset
  keys, result directory behavior, and checkpoint loading.
- `ERRNet/util/index.py`: existing PSNR, SSIM, NCC, and LMSE metric semantics;
  review only unless an approved blocker requires otherwise.
- `ERRNet/experiments/results-improved.md`: main evidence record for training,
  checkpoint, evaluation, comparison, blockers, and residual risks.
- `ERRNet/experiments/results-baseline.md`: baseline metrics and output paths
  used for comparison.
- `ERRNet/README_DIP26.md`: update only if implemented commands or usage
  guidance change.

## 3. 按模块划分的拟修改内容

### Planning And Design Artifacts

Changed:
- `specs/002-improved-retraining-checkpoint/plan.md`: this implementation
  plan.
- `specs/002-improved-retraining-checkpoint/research.md`: planning decisions
  and alternatives.
- `specs/002-improved-retraining-checkpoint/data-model.md`: entities and
  validation rules for the improved run, checkpoint, evaluation results, and
  comparison record.
- `specs/002-improved-retraining-checkpoint/contracts/errnet-retraining-cli-contract.md`:
  command contract for full retraining, checkpoint identity, and evaluation.
- `specs/002-improved-retraining-checkpoint/quickstart.md`: repeatable run and
  validation commands.

Not changed:
- Spec1 planning artifacts except as read-only reference.

### Experiment Evidence

Potentially changed during implementation:
- `ERRNet/experiments/results-improved.md`: add full-retraining command,
  status, checkpoint checksum, benchmark metrics, custom output paths,
  comparison notes, blockers, and compatibility evidence.
- `ERRNet/experiments/README.md`: update only if the experiment record index or
  final summary needs to point to the new full-retraining artifact.
- `ERRNet/experiments/delivery-checklist.md`: update only if the new local
  checkpoint changes weight-link readiness or paper/PPT evidence mapping.

Not changed:
- Baseline result values in `ERRNet/experiments/results-baseline.md` except
  optional cross-reference additions; historical baseline evidence must remain
  intact.

### Training And Loss Paths

Expected unchanged:
- `ERRNet/train_errnet.py` should be reused as the aligned training entrypoint.
- `ERRNet/options/errnet/train_options.py` already contains the required loss
  weight options and should remain unchanged unless a blocker is found.
- `ERRNet/models/losses.py` already parameterizes the approved weights and
  should remain unchanged unless a blocker is found.
- `ERRNet/models/base_model.py` and `ERRNet/engine.py` should save checkpoints
  using existing conventions.

Potentially changed only if a blocker is encountered:
- `ERRNet/train_errnet.py`: localized fix for a proven training completion,
  non-resume, logging, or checkpoint-save blocker.
- `ERRNet/options/errnet/train_options.py`: localized option/help/default-safe
  fix if the approved command cannot be expressed or recorded.
- `ERRNet/models/losses.py`: localized default-preserving fix if the approved
  loss weights do not apply as intended during training.
- `ERRNet/models/base_model.py` or `ERRNet/engine.py`: localized fix only if
  checkpoint save identity or completion evidence is broken.

Not changed unless a later spec approves it:
- Network architecture in `ERRNet/models/arch/` and `ERRNet/models/networks.py`.
- Loader, resize, crop, augmentation, and dataset semantics in `ERRNet/data/`
  or `ERRNet/datasets/`.
- Metric implementation in `ERRNet/util/index.py`.
- Baseline checkpoint files and raw/processed datasets.
- New dependencies, external upload tools, final paper/PPT assets, or email
  submission scripts.

### Checkpoints And Results

Generated during implementation:
- `ERRNet/checkpoints/errnet_improved_retrain_60ep/`: canonical improved
  training output directory.
- One final loadable checkpoint in that directory, plus existing ERRNet
  periodic/latest artifacts as produced by current save behavior.
- Evaluation result images under existing `ERRNet/results/<dataset>/` style
  directories, ideally with method names that distinguish the improved
  checkpoint.
- Run logs under `ERRNet/experiments/run-logs/` or an equivalent documented
  experiment log location.

Not changed:
- `ERRNet/checkpoints/errnet/errnet_060_00463920.pt`.
- Existing smoke directories unless explicitly archived to avoid path conflict.

## 4. 集成点

- Training integrates through `ERRNet/train_errnet.py --name
  errnet_improved_retrain_60ep --hyper --pixel_loss_weight 0.2
  --gradient_loss_weight 0.4`.
- Checkpoint identity integrates through existing `--name` and
  `checkpoints/{experiment_name}` conventions.
- Checkpoint verification integrates through filesystem checks and checksum
  recording for files under
  `ERRNet/checkpoints/errnet_improved_retrain_60ep/`.
- Benchmark evaluation integrates through `ERRNet/test_errnet.py --dataset
  <dataset_key> -r --icnn_path <improved_checkpoint> --hyper`.
- Custom-image evaluation integrates through `ERRNet/test_errnet.py --dataset
  custom --input_dir ../5pictures --max_long_edge 1024 -r --icnn_path
  <improved_checkpoint> --hyper`.
- Metric comparison integrates through existing `Engine.eval()` aggregation and
  `ERRNet/util/index.py` metric names.
- Evidence integration uses existing markdown experiment records under
  `ERRNet/experiments/`.
- Agent runtime guidance integrates through `AGENTS.md`, which now points to
  this plan for feature changes.

## 5. 验证策略

1. Static planning validation:
   - Confirm `spec.md`, `plan.md`, `research.md`, `data-model.md`,
     `contracts/errnet-retraining-cli-contract.md`, `quickstart.md`, and
     `checklists/requirements.md` exist under this feature directory.
   - Confirm no unresolved `NEEDS CLARIFICATION`, template placeholders, or
     stale spec1 plan references remain in feature artifacts.
   - Run `git diff --check` on changed planning, contract, quickstart, and
     context files.
2. Pre-training readiness:
   - Confirm processed training data exists under `ERRNet/datasets/processed_data/`.
   - Confirm baseline checkpoint remains present at
     `ERRNet/checkpoints/errnet/errnet_060_00463920.pt`.
   - Confirm `ERRNet/checkpoints/errnet_improved_retrain_60ep/` is absent or
     safely archived before the final run begins.
   - Record exact command, environment, GPU/CPU mode, seed, and current git
     status before training.
3. Full retraining validation:
   - Run non-resumed 60-epoch aligned training with experiment name
     `errnet_improved_retrain_60ep`.
   - Verify the record shows training progressed from the non-resumed start and
     reached the 60-epoch completion point.
   - Verify a new checkpoint exists under the canonical directory and record
     checksum.
   - Select the final checkpoint with an epoch-60-first policy; if only a latest
     checkpoint is selected, tie it to epoch-60 completion evidence from the log.
   - Verify the selected checkpoint actually loads through `test_errnet.py`
     before treating it as ready for comparison.
4. Compatibility validation:
   - If no code changed, record that existing defaults and commands were
     reused.
   - If code changed, run syntax/import checks for touched files and verify
     default old-checkpoint inference still works using
     `ERRNet/checkpoints/errnet/errnet_060_00463920.pt`.
   - Confirm no loader, metric, architecture, dependency, or baseline
     checkpoint change occurred.
   - Record the single-card CUDA or CPU fallback mode used for load/evaluation
     checks, including the reason and residual risk if CPU fallback is not run.
5. Improved checkpoint evaluation:
   - Evaluate the new checkpoint on all six dataset keys:
     `ceilnet_table2`, `real20`, `postcard`, `objects`, `wild`,
     `sir2_withgt`.
   - Record PSNR, SSIM, NCC, LMSE, output paths, metric status, NaN/inf status,
     and blocker notes for each benchmark.
   - Evaluate all five custom images in `5pictures/` and record output paths
     as qualitative evidence.
6. Comparison and evidence validation:
   - Compare improved and baseline results for all six benchmarks and all five
     custom outputs.
   - State whether the new checkpoint supports, fails to support, or is
     inconclusive for an improvement claim.
   - Update experiment records and delivery evidence only where directly
     related to this checkpoint.

## 6. 风险 / 未知项 / 假设

- Assumption: The approved improved method remains the spec1 local loss-weight
  path with pixel loss weight `0.2` and gradient loss weight `0.4`.
- Assumption: A non-resumed 60-epoch aligned training run is feasible in the
  available environment and data layout.
- Assumption: The existing training script's hard-coded `while engine.epoch <
  60` protocol is the authoritative completion rule for this feature.
- Risk: Full training may exceed available GPU time. Mitigation: record start,
  progress, blockers, and residual risk; do not label partial checkpoints as
  final.
- Risk: The approved weights match baseline-compatible defaults, so measured
  gains may be small or absent. Mitigation: report actual metrics without
  overstating improvement.
- Risk: Existing checkpoint directory conflict could overwrite evidence.
  Mitigation: inspect/archive `ERRNet/checkpoints/errnet_improved_retrain_60ep/`
  before the final run and record the action.
- Risk: Existing dirty worktree can make provenance ambiguous. Mitigation:
  record git status and limit implementation edits to approved paths.
- Risk: A training blocker could require an out-of-scope loader, metric,
  architecture, dependency, or baseline checkpoint change. Mitigation: classify
  blockers before code changes and stop for a spec/plan update if the fix is
  outside localized model, loss, or training-path responsibility.
- Compatibility: Baseline commands, dataset keys, result directories, metric
  names, old checkpoint inference, and default loss behavior must remain
  stable.
- Compatibility: Any localized model/loss/training fix must include
  default-preservation evidence and old-checkpoint inference evidence.
- Out-of-scope compatibility: multi-card/distributed behavior, new data
  loaders, new metrics, final paper/PPT authoring, external uploads, and email
  submission.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Scope Control**: PASS. The plan targets one full retraining run, one
  canonical checkpoint, existing evaluation paths, and directly related
  evidence. Broader architecture, loader, metric, dependency, and delivery
  changes remain out of scope.
- **Existing Contracts**: PASS. Existing script names, dataset keys, metric
  names, result conventions, checkpoint format, and baseline checkpoint path
  are preserved.
- **Reuse First**: PASS. The plan reuses `train_errnet.py`, `test_errnet.py`,
  `Engine`, `BaseModel.save`, `TrainOptions`, `MultipleLoss`,
  `GradientLoss`, existing metrics, and `ERRNet/experiments/` records.
- **Verification Path**: PASS. Static checks, pre-training readiness,
  non-resumed 60-epoch completion evidence, checksum verification, full
  benchmark evaluation, custom-image output checks, and compatibility checks
  are defined.
- **Assumptions And Risks**: PASS. Compute feasibility, dirty worktree,
  checkpoint conflict, default-compatible weights, and compatibility risks are
  recorded.
- **Synchronized Artifacts**: PASS. Planning artifacts, command contract,
  quickstart, experiment records, and optional README/delivery evidence sync
  are identified.
- **Dependency Discipline**: PASS. No new dependency is planned.
- **Completion Evidence**: PASS. Implementation completion requires changed
  files, commands, checkpoint checksum, metrics, outputs, assumptions, and
  residual risks before claiming completion.

## Project Structure

### Documentation (this feature)

```text
specs/002-improved-retraining-checkpoint/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── errnet-retraining-cli-contract.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
ERRNet/
├── README_DIP26.md
├── train_errnet.py
├── test_errnet.py
├── engine.py
├── options/
│   └── errnet/
│       └── train_options.py
├── models/
│   ├── base_model.py
│   ├── losses.py
│   └── errnet_model.py
├── util/
│   └── index.py
├── experiments/
│   ├── README.md
│   ├── results-baseline.md
│   ├── results-improved.md
│   └── run-logs/
├── checkpoints/
│   ├── errnet/
│   │   └── errnet_060_00463920.pt
│   └── errnet_improved_retrain_60ep/
└── results/

5pictures/
├── p1.jpg
├── p2.jpg
├── p3.jpg
├── p4.jpg
└── p5.jpg
```

**Structure Decision**: Use the existing ML repository layout. Planning
artifacts live in `specs/002-improved-retraining-checkpoint/`; execution runs
inside `ERRNet/`; evidence is recorded under `ERRNet/experiments/`; generated
checkpoints and result images stay in the existing `ERRNet/checkpoints/` and
`ERRNet/results/` locations. No new app, package, service, runner framework,
or dependency is introduced.

## Complexity Tracking

No constitution violations are planned.

## Post-Design Constitution Re-Check

- **Scope Control**: PASS. Phase 0/1 artifacts keep the work centered on one
  improved retraining run, one checkpoint, and existing evaluation paths.
- **Existing Contracts**: PASS. The command contract preserves current script
  names, dataset keys, metric names, checkpoint format, and baseline checkpoint
  usage.
- **Reuse First**: PASS. Research and quickstart reuse the existing ERRNet
  scripts and experiment record locations.
- **Verification Path**: PASS. Quickstart and contract define repeatable
  training, checksum, benchmark, custom-image, and compatibility checks.
- **Assumptions And Risks**: PASS. Research and plan record compute,
  checkpoint-conflict, dirty-worktree, and compatibility risks.
- **Synchronized Artifacts**: PASS. Data model, contract, quickstart, plan, and
  `AGENTS.md` are aligned with the clarified spec.
- **Dependency Discipline**: PASS. No new dependencies are introduced.
- **Completion Evidence**: PASS. The design requires run logs, checkpoint
  checksum, metric rows, output paths, and residual risk notes before
  completion.
