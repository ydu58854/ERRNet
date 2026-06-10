# Tasks: ERRNet Improved Retraining Checkpoint

**Input**: Design documents from `/specs/002-improved-retraining-checkpoint/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md, checklists/pre-implementation.md

**Tests**: This feature uses reproducible experiment commands, checkpoint identity checks, actual checkpoint load verification, metric records, visual output inspection, compatibility checks, resource-mode evidence, and static documentation checks as verification tasks. No new automated test framework is required.

**Organization**: Tasks are grouped by user story so each story produces an independently reviewable increment. Keep edits local and avoid unrelated cleanup.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it touches different files or only records independent evidence.
- **[Story]**: Maps to the user story in `spec.md`.
- Every task includes exact file paths and completion criteria.

## Phase 1: Setup (Shared Evidence And Readiness)

**Purpose**: Establish the run log and evidence structure before touching training outputs.

- [X] T001 Create a full-retraining section template in `ERRNet/experiments/results-improved.md` with fields for command, environment, non-resume status, epoch target, loss weights, checkpoint path, checksum, logs, and completion status.
- [X] T002 Create benchmark and custom-image result table templates in `ERRNet/experiments/results-improved.md` for six benchmark rows and five custom-image rows.
- [X] T003 [P] Add a feature reference and expected artifact summary to `ERRNet/experiments/README.md` pointing to `specs/002-improved-retraining-checkpoint/plan.md` and `ERRNet/checkpoints/errnet_improved_retrain_60ep/`.
- [X] T004 [P] Record the current implementation-ready checklist status in `specs/002-improved-retraining-checkpoint/checklists/pre-implementation.md` after reviewing all checklist items.
- [X] T005 [P] Create a planned run-log placeholder or naming note in `ERRNet/experiments/results-improved.md` for `ERRNet/experiments/run-logs/improved_retrain_60ep_<date>.log`.

**Checkpoint**: Evidence files can capture every later training, checkpoint, evaluation, and comparison result.

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Confirm data, environment, paths, and compatibility before starting any user story work.

**Critical**: No user story work can begin until this phase is complete.

- [X] T006 Record actual environment, Python/PyTorch/CUDA status, single-card CUDA vs CPU fallback decision, seed, and git status in `ERRNet/experiments/results-improved.md`; if CPU fallback is not exercised, record the reason and residual risk.
- [X] T007 Record processed training data readiness and `5pictures/` custom image readiness in `ERRNet/experiments/results-improved.md`, referencing `ERRNet/datasets/processed_data/` and `5pictures/p1.jpg` through `5pictures/p5.jpg`.
- [X] T008 Verify and record baseline checkpoint preservation in `ERRNet/experiments/results-improved.md` for `ERRNet/checkpoints/errnet/errnet_060_00463920.pt`.
- [X] T009 Inspect `ERRNet/checkpoints/errnet_improved_retrain_60ep/` and record whether it is absent, archived, preserved, or blocked in `ERRNet/experiments/results-improved.md`.
- [X] T010 [P] Review `ERRNet/train_errnet.py`, `ERRNet/engine.py`, and `ERRNet/models/base_model.py` for the non-resumed 60-epoch checkpoint save path and document findings in `ERRNet/experiments/results-improved.md`.
- [X] T011 [P] Review `ERRNet/options/errnet/train_options.py` and `ERRNet/models/losses.py` for `--pixel_loss_weight 0.2` and `--gradient_loss_weight 0.4` support and document findings in `ERRNet/experiments/results-improved.md`.
- [X] T012 [P] Review `ERRNet/test_errnet.py` dataset keys, improved checkpoint command contract, and available CPU fallback flags, then document supported benchmark/custom/load-check commands in `ERRNet/experiments/results-improved.md`.
- [X] T013 Run static planning validation for `specs/002-improved-retraining-checkpoint/spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/errnet-retraining-cli-contract.md`, `quickstart.md`, `checklists/requirements.md`, `checklists/pre-implementation.md`, and `tasks.md`, then record the result in `ERRNet/experiments/results-improved.md`.

**Checkpoint**: Training can start only after environment, data, baseline checkpoint, target directory, command contracts, and planning artifacts are ready.

## Phase 3: User Story 1 - Complete Improved Retraining (Priority: P1) MVP

**Goal**: Produce evidence for a non-resumed 60-epoch improved aligned training run with fixed loss weights.

**Independent Test**: `ERRNet/experiments/results-improved.md` identifies a completed non-resumed 60-epoch run with experiment name `errnet_improved_retrain_60ep`, fixed weights `0.2` and `0.4`, command/log evidence, or a precise blocker.

### Verification for User Story 1

- [X] T014 [US1] Record the exact non-resumed training command in `ERRNet/experiments/results-improved.md` using `ERRNet/train_errnet.py --name errnet_improved_retrain_60ep --hyper --pixel_loss_weight 0.2 --gradient_loss_weight 0.4`.
- [X] T015 [US1] Run or start the full retraining command from `ERRNet/` and capture the run log under `ERRNet/experiments/run-logs/`.
- [X] T016 [US1] Record start time, environment reference, git status, non-resume status, epoch target, and loss weights in `ERRNet/experiments/results-improved.md`.
- [X] T017 [US1] Record training progress and final epoch-60 completion evidence in `ERRNet/experiments/results-improved.md`, or record blocker classification and residual risk if the run cannot complete; if the blocker would require loader, metric, architecture, dependency, or baseline checkpoint changes, stop and record that a spec/plan update is required before code changes.

### Implementation for User Story 1

- [X] T018 [US1] If the full retraining run completes without code changes, record "No code change required" for `ERRNet/train_errnet.py`, `ERRNet/options/errnet/train_options.py`, `ERRNet/models/losses.py`, `ERRNet/engine.py`, and `ERRNet/models/base_model.py` in `ERRNet/experiments/results-improved.md`.
- [X] T019 [US1] If T017 classifies a training-path blocker as in scope, apply the smallest localized fix in `ERRNet/train_errnet.py` and document blocker, rationale, and default-preservation impact in `ERRNet/experiments/results-improved.md`. Completed: SIGINT/SIGTERM handler records an interrupted checkpoint when possible.
- [X] T020 [US1] If T017 classifies a loss-weight blocker as in scope, apply the smallest default-preserving fix in `ERRNet/models/losses.py` or `ERRNet/options/errnet/train_options.py` and document blocker, rationale, and compatibility impact in `ERRNet/experiments/results-improved.md`. Not applicable: no in-scope source-code blocker was found.
- [X] T021 [US1] If T017 classifies a checkpoint-save or epoch-state blocker as in scope, apply the smallest localized fix in `ERRNet/engine.py` or `ERRNet/models/base_model.py` and document blocker, rationale, and compatibility impact in `ERRNet/experiments/results-improved.md`. Completed: checkpoint saves are decoupled from logging, optional iteration saves are supported, and writes are atomic.
- [X] T022 [US1] If any code was changed in T019-T021, run syntax/import compatibility checks for touched files and record results in `ERRNet/experiments/results-improved.md`. Completed: syntax checks, checkpoint generation smoke, and load smoke passed.

**Checkpoint**: User Story 1 is complete when full retraining is completed or a precise blocker is recorded without falsely labeling a partial run as final.

## Phase 4: User Story 2 - Save And Identify New Checkpoint (Priority: P2)

**Goal**: Select and identify the final improved checkpoint artifact without overwriting baseline or smoke artifacts.

**Independent Test**: `ERRNet/experiments/results-improved.md` records the final checkpoint path under `ERRNet/checkpoints/errnet_improved_retrain_60ep/`, checksum, producing run, and baseline preservation status.

### Verification for User Story 2

- [X] T023 [US2] List checkpoint artifacts under `ERRNet/checkpoints/errnet_improved_retrain_60ep/` and record the available files in `ERRNet/experiments/results-improved.md`.
- [X] T024 [US2] Select the final loadable checkpoint file from `ERRNet/checkpoints/errnet_improved_retrain_60ep/` using this policy: prefer an explicit epoch-60 checkpoint; use a latest checkpoint only when the run log proves it corresponds to epoch 60; record filename, mtime, size, and selection rationale in `ERRNet/experiments/results-improved.md`. Completed: selected explicit epoch-60 checkpoint `ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt`, size `346898110`, mtime `2026-05-27 02:42:58 +0800`.
- [X] T025 [US2] Generate and record the checksum for the selected checkpoint in `ERRNet/experiments/results-improved.md`. Completed: SHA256 `9214c1bd66e38350d99c99c02dd2fbceb626b15e50d66c1f3df1bf3a14c7073d`.
- [X] T026 [US2] Record that `ERRNet/checkpoints/errnet/errnet_060_00463920.pt` remains present and distinct from the improved checkpoint in `ERRNet/experiments/results-improved.md`.

### Implementation for User Story 2

- [X] T027 [US2] If `ERRNet/checkpoints/errnet_improved_retrain_60ep/` contained prior artifacts, document the preserve/archive action and final artifact state in `ERRNet/experiments/results-improved.md`. Completed: final artifact list and selected epoch-60 checkpoint state are documented.
- [X] T028 [US2] Run an actual load-verification command through existing `ERRNet/test_errnet.py` using the selected checkpoint via `--icnn_path`, record command/status/log path and resource mode in `ERRNet/experiments/results-improved.md`, and mark load readiness only after the checkpoint is loaded successfully; if the first benchmark evaluation is used as this load check, record that linkage before US3 comparison. Completed: first `ceilnet_table2` benchmark loaded `errnet_060_00470708.pt`, logged `Resume from epoch 60, iteration 470708`, and exited status `0`.
- [X] T029 [US2] If code changed during US1, run old baseline checkpoint inference compatibility and record command/result in `ERRNet/experiments/results-improved.md`. Not applicable: no US1 source code changed; baseline preservation recorded.

**Checkpoint**: User Story 2 is complete when the improved checkpoint has a stable path, checksum, producing-run reference, and compatibility status.

## Phase 5: User Story 3 - Verify Improved Checkpoint Evaluation (Priority: P3)

**Goal**: Evaluate the new checkpoint on all required benchmark and custom-image inputs.

**Independent Test**: `ERRNet/experiments/results-improved.md` contains six benchmark metric rows and five custom-image output rows, each with output paths or blocker notes.

### Verification for User Story 3

- [X] T030 [P] [US3] Record the improved evaluation command for `ceilnet_table2` in `ERRNet/experiments/results-improved.md`.
- [X] T031 [P] [US3] Record the improved evaluation command for `real20` in `ERRNet/experiments/results-improved.md`.
- [X] T032 [P] [US3] Record the improved evaluation command for `postcard` in `ERRNet/experiments/results-improved.md`.
- [X] T033 [P] [US3] Record the improved evaluation command for `objects` in `ERRNet/experiments/results-improved.md`.
- [X] T034 [P] [US3] Record the improved evaluation command for `wild` in `ERRNet/experiments/results-improved.md`.
- [X] T035 [P] [US3] Record the improved evaluation command for `sir2_withgt` in `ERRNet/experiments/results-improved.md`.
- [X] T036 [US3] Run or document the improved `ceilnet_table2` evaluation with the selected checkpoint and record PSNR, SSIM, NCC, LMSE, output path, sample count, and log path in `ERRNet/experiments/results-improved.md`. Completed: PSNR `27.8476`, SSIM `0.9410`, NCC `0.9798`, LMSE `0.0047`, status `0`, output count `100`.
- [X] T037 [US3] Run or document the improved `real20` evaluation with the selected checkpoint and record PSNR, SSIM, NCC, LMSE, output path, sample count, and log path in `ERRNet/experiments/results-improved.md`. Completed: PSNR `23.7577`, SSIM `0.8268`, NCC `0.8935`, LMSE `0.0190`, status `0`, output count `20`.
- [X] T038 [US3] Run or document the improved `postcard` evaluation with the selected checkpoint and record PSNR, SSIM, NCC, LMSE, output path, sample count, and log path in `ERRNet/experiments/results-improved.md`. Completed: PSNR `21.6580`, SSIM `0.8795`, NCC `0.9384`, LMSE `0.0044`, status `0`, output count `179`.
- [X] T039 [US3] Run or document the improved `objects` evaluation with the selected checkpoint and record PSNR, SSIM, NCC, LMSE, output path, sample count, and log path in `ERRNet/experiments/results-improved.md`. Completed: PSNR `24.4328`, SSIM `0.8942`, NCC `0.9820`, LMSE `0.0032`, status `0`, output count `200`.
- [X] T040 [US3] Run or document the improved `wild` evaluation with the selected checkpoint and record PSNR, SSIM, NCC, LMSE, output path, sample count, and log path in `ERRNet/experiments/results-improved.md`. Completed: PSNR `25.1643`, SSIM `0.8864`, NCC `0.9420`, LMSE `0.0069`, status `0`, output count `101`.
- [X] T041 [US3] Run or document the improved `sir2_withgt` evaluation with the selected checkpoint and record PSNR, SSIM, NCC, LMSE, output path, sample count, and log path in `ERRNet/experiments/results-improved.md`. Completed: PSNR `23.5517`, SSIM `0.8871`, NCC `0.9573`, LMSE `0.0044`, status `0`, output count `480`.
- [X] T042 [US3] Record NaN/inf status, metric validity, and same-semantics comparison notes for all six benchmark rows in `ERRNet/experiments/results-improved.md`.
- [X] T043 [US3] Record the custom-image evaluation command for `../5pictures` in `ERRNet/experiments/results-improved.md`.
- [X] T044 [US3] Run or document custom-image evaluation with the selected checkpoint and record output paths for `5pictures/p1.jpg` through `5pictures/p5.jpg` in `ERRNet/experiments/results-improved.md`. Completed: status `0`, log `ERRNet/experiments/run-logs/improved_retrain_60ep_custom_20260527_032534.log`, and five full-retrain custom output PNGs generated under `ERRNet/results/custom_improved_retrain_60ep/`.

### Implementation for User Story 3

- [X] T045 [US3] Add or update the full benchmark results table in `ERRNet/experiments/results-improved.md` with method, dataset, sample count, PSNR, SSIM, NCC, LMSE, metric status, NaN/inf status, output path, and log columns.
- [X] T046 [US3] Add or update the custom-image qualitative table in `ERRNet/experiments/results-improved.md` with image name, input path, improved output path, ground-truth status, visual status, and blocker or review note.
- [X] T047 [US3] If evaluation fails for any benchmark or custom image, record the exact dataset/image blocker and residual risk in `ERRNet/experiments/results-improved.md` without removing the required row.

**Checkpoint**: User Story 3 is complete when every required benchmark/image has measured evidence or an explicit blocker row.

## Phase 6: User Story 4 - Update Project Evidence (Priority: P4)

**Goal**: Summarize full-retraining evidence against spec1 baseline evidence for report readiness.

**Independent Test**: `ERRNet/experiments/results-improved.md` distinguishes full retraining from smoke validation and states whether evidence supports, does not support, or is inconclusive for an improvement claim.

### Verification for User Story 4

- [X] T048 [US4] Compare all six improved benchmark rows against matching baseline rows from `ERRNet/experiments/results-baseline.md` and record comparison outcomes in `ERRNet/experiments/results-improved.md`.
- [X] T049 [US4] Compare all five improved custom-image outputs against baseline custom outputs from `ERRNet/experiments/results-baseline.md` and record qualitative comparison notes in `ERRNet/experiments/results-improved.md`.
- [X] T050 [US4] Record the overall claim status in `ERRNet/experiments/results-improved.md` as supports improvement, does not support improvement, or inconclusive.
- [X] T051 [US4] Record assumptions, compute constraints, compatibility status, and residual risks in `ERRNet/experiments/results-improved.md`.

### Implementation for User Story 4

- [X] T052 [US4] Update `ERRNet/experiments/README.md` with a final feature evidence summary, including new checkpoint path, checksum location, evaluation coverage, and result record link.
- [X] T053 [US4] Update `ERRNet/experiments/delivery-checklist.md` only if the new local checkpoint changes weight-link readiness, report evidence mapping, or remaining blocker status.
- [X] T054 [US4] Update `ERRNet/README_DIP26.md` only if the final implementation changes user-facing retraining or evaluation commands; otherwise record "No README change required" in `ERRNet/experiments/results-improved.md`.

**Checkpoint**: User Story 4 is complete when project evidence is report-ready or blockers are explicit and traceable.

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Validate scope, formatting, synchronization, and final readiness.

- [X] T055 Run `git diff --check -- specs/002-improved-retraining-checkpoint AGENTS.md ERRNet/experiments ERRNet/train_errnet.py ERRNet/options/errnet/train_options.py ERRNet/models/losses.py ERRNet/engine.py ERRNet/models/base_model.py ERRNet/README_DIP26.md` and record result in `ERRNet/experiments/results-improved.md`.
- [X] T056 Scan `specs/002-improved-retraining-checkpoint/` and `ERRNet/experiments/results-improved.md` for unresolved `NEEDS CLARIFICATION`, placeholder text, missing required rows, and stale smoke-only language, then record findings in `ERRNet/experiments/results-improved.md`.
- [X] T057 Review changed files and record any deviations from allowed paths in `ERRNet/experiments/results-improved.md`; do not revert unrelated existing workspace changes.
- [X] T058 If any model, loss, or training-path files changed, verify and record no loader, metric, architecture, dependency, or baseline checkpoint change occurred in `ERRNet/experiments/results-improved.md`.
- [X] T059 Update `specs/002-improved-retraining-checkpoint/tasks.md` task statuses as work is completed and preserve incomplete tasks with blocker notes.
- [X] T060 Summarize final implementation content, commands run, checkpoint checksum, benchmark/custom results, assumptions, and residual risks in `ERRNet/experiments/results-improved.md`.

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Starts immediately and prepares evidence structure.
- **Foundational (Phase 2)**: Depends on Setup; blocks all user stories.
- **US1 Complete Retraining (Phase 3)**: Depends on Foundational and produces the training run evidence.
- **US2 Save Checkpoint (Phase 4)**: Depends on US1 completion or blocker evidence.
- **US3 Evaluate Checkpoint (Phase 5)**: Depends on US2 checkpoint path and actual load-verification status.
- **US4 Update Evidence (Phase 6)**: Depends on US3 benchmark/custom evidence.
- **Polish (Phase 7)**: Runs after desired user stories are complete.

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational; MVP scope.
- **US2 (P2)**: Depends on US1 because it needs training output or blocker status.
- **US3 (P3)**: Depends on US2 because it needs selected checkpoint identity.
- **US4 (P4)**: Depends on US3 because comparison requires evaluation evidence.

### Parallel Opportunities

- T003, T004, and T005 can run in parallel after T001-T002 scope is understood.
- T010, T011, and T012 can run in parallel during Foundational review.
- T030-T035 can be prepared in parallel after US2 identifies the checkpoint.
- T036-T041 benchmark runs can be parallelized only if GPU/CPU resources and output names are isolated.
- T052-T054 can run in parallel after comparison evidence exists because they touch separate documentation files.

## Parallel Example: Foundational Review

```bash
Task: "Review ERRNet/train_errnet.py, ERRNet/engine.py, and ERRNet/models/base_model.py for the non-resumed 60-epoch checkpoint save path and document findings in ERRNet/experiments/results-improved.md"
Task: "Review ERRNet/options/errnet/train_options.py and ERRNet/models/losses.py for --pixel_loss_weight 0.2 and --gradient_loss_weight 0.4 support and document findings in ERRNet/experiments/results-improved.md"
Task: "Review ERRNet/test_errnet.py dataset keys and improved checkpoint command contract, then document supported benchmark/custom commands in ERRNet/experiments/results-improved.md"
```

## Parallel Example: Benchmark Evaluation

```bash
Task: "Run or document the improved ceilnet_table2 evaluation with the selected checkpoint and record metrics in ERRNet/experiments/results-improved.md"
Task: "Run or document the improved real20 evaluation with the selected checkpoint and record metrics in ERRNet/experiments/results-improved.md"
Task: "Run or document the improved postcard evaluation with the selected checkpoint and record metrics in ERRNet/experiments/results-improved.md"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 setup evidence.
2. Complete Phase 2 foundational readiness.
3. Complete Phase 3 non-resumed 60-epoch improved retraining evidence.
4. Stop and validate that the run is full retraining, not smoke or resume-only evidence.

### Incremental Delivery

1. Full retraining evidence.
2. Stable checkpoint identity and checksum.
3. Full benchmark/custom evaluation.
4. Baseline-vs-improved comparison and report-ready evidence.

### Completion Criteria Summary

- Every changed source or documentation file has a direct link to this feature.
- Existing baseline commands, dataset keys, metrics, default loss behavior, resource-mode expectations, and old checkpoint inference remain valid.
- New checkpoint is identified by stable path, checksum, and actual load verification.
- Six benchmark rows and five custom-image rows are recorded or blocked with reasons.
- Final evidence states whether the new checkpoint supports an improvement claim.

## Task Detail Matrix

| Task | Title | Goal | Affected Files / Modules | Dependencies / Order | Completion Criteria |
|------|-------|------|--------------------------|----------------------|---------------------|
| T001 | Full retraining template | Prepare run evidence fields | `ERRNet/experiments/results-improved.md` | First setup task | Fields exist for command, environment, non-resume, epoch target, weights, checkpoint, checksum, logs, status |
| T002 | Evaluation table templates | Prepare benchmark/custom result rows | `ERRNet/experiments/results-improved.md` | After T001 | Six benchmark placeholders and five custom placeholders exist |
| T003 | Evidence index reference | Link feature plan and artifact | `ERRNet/experiments/README.md` | After T001; parallel | Index references current plan and checkpoint directory |
| T004 | Checklist status | Record implementation-readiness review | `specs/002-improved-retraining-checkpoint/checklists/pre-implementation.md` | Parallel setup | Checklist has reviewed statuses or notes |
| T005 | Run-log naming | Establish log naming convention | `ERRNet/experiments/results-improved.md` | Parallel setup | Planned log path/naming note exists |
| T006 | Environment record | Capture reproducibility context | `ERRNet/experiments/results-improved.md` | After setup | Environment, git status, seed, single-card CUDA/CPU fallback decision recorded |
| T007 | Data readiness | Confirm required data/custom images | `ERRNet/experiments/results-improved.md` | Foundational | Processed data and p1-p5 readiness recorded |
| T008 | Baseline checkpoint preservation | Protect old checkpoint | `ERRNet/experiments/results-improved.md`, `ERRNet/checkpoints/errnet/errnet_060_00463920.pt` | Foundational | Baseline path presence recorded |
| T009 | Target directory state | Avoid artifact overwrite | `ERRNet/experiments/results-improved.md`, `ERRNet/checkpoints/errnet_improved_retrain_60ep/` | Before training | Directory state and archive/preserve action recorded |
| T010 | Training save review | Confirm non-resume and save path | `ERRNet/train_errnet.py`, `ERRNet/engine.py`, `ERRNet/models/base_model.py`, `ERRNet/experiments/results-improved.md` | Foundational; parallel | Findings recorded |
| T011 | Loss option review | Confirm fixed weights are supported | `ERRNet/options/errnet/train_options.py`, `ERRNet/models/losses.py`, `ERRNet/experiments/results-improved.md` | Foundational; parallel | Findings recorded |
| T012 | Evaluation contract review | Confirm dataset/custom/load-check commands | `ERRNet/test_errnet.py`, `ERRNet/experiments/results-improved.md` | Foundational; parallel | Commands, dataset keys, and CPU fallback flags recorded |
| T013 | Static planning validation | Check artifacts before execution | `specs/002-improved-retraining-checkpoint/`, `ERRNet/experiments/results-improved.md` | End foundational | Validation result recorded |
| T014 | Training command record | Define exact run command | `ERRNet/experiments/results-improved.md` | US1 start | Command recorded without `--resume` |
| T015 | Full training run | Produce full retraining evidence | `ERRNet/train_errnet.py`, `ERRNet/checkpoints/errnet_improved_retrain_60ep/`, `ERRNet/experiments/run-logs/` | After T014 | Run log captured or blocker recorded |
| T016 | Run metadata | Capture start context | `ERRNet/experiments/results-improved.md` | During T015 | Start metadata recorded |
| T017 | Completion evidence | Prove epoch-60 completion or classify blocker | `ERRNet/experiments/results-improved.md` | After T015 | Completion or blocker classification recorded; out-of-scope blockers stop for spec/plan update |
| T018 | No-code-change record | Document reuse if no blockers | `ERRNet/experiments/results-improved.md` | After T017 | No-code-change status recorded |
| T019 | Training unblocker | Fix proven in-scope training blocker if needed | `ERRNet/train_errnet.py`, `ERRNet/experiments/results-improved.md` | Only if T017 classifies blocker in scope | Minimal fix and rationale recorded |
| T020 | Loss unblocker | Fix proven in-scope loss-weight blocker if needed | `ERRNet/models/losses.py`, `ERRNet/options/errnet/train_options.py`, `ERRNet/experiments/results-improved.md` | Only if T017 classifies blocker in scope | Minimal fix and compatibility impact recorded |
| T021 | Checkpoint unblocker | Fix proven in-scope save/epoch blocker if needed | `ERRNet/engine.py`, `ERRNet/models/base_model.py`, `ERRNet/experiments/results-improved.md` | Only if T017 classifies blocker in scope | Minimal fix and compatibility impact recorded |
| T022 | Code compatibility checks | Verify touched code paths | `ERRNet/experiments/results-improved.md` | Only after code changes | Syntax/import results recorded |
| T023 | Artifact listing | Identify checkpoint files | `ERRNet/checkpoints/errnet_improved_retrain_60ep/`, `ERRNet/experiments/results-improved.md` | After US1 | Available artifacts recorded |
| T024 | Final checkpoint selection | Pick loadable final checkpoint | `ERRNet/experiments/results-improved.md` | After T023 | Epoch-60 selection policy, filename, mtime, size, and rationale recorded |
| T025 | Checksum record | Identify exact artifact | `ERRNet/checkpoints/errnet_improved_retrain_60ep/`, `ERRNet/experiments/results-improved.md` | After T024 | Checksum recorded |
| T026 | Baseline distinction | Ensure checkpoint separation | `ERRNet/checkpoints/errnet/errnet_060_00463920.pt`, `ERRNet/experiments/results-improved.md` | After T025 | Baseline distinctness recorded |
| T027 | Prior artifact handling | Document archive/preserve action | `ERRNet/checkpoints/errnet_improved_retrain_60ep/`, `ERRNet/experiments/results-improved.md` | If directory existed | Action recorded |
| T028 | Load verification | Confirm checkpoint loads through evaluation entrypoint | `ERRNet/test_errnet.py`, `ERRNet/results/`, `ERRNet/experiments/results-improved.md` | After T025 | Actual load command/status/log/resource mode recorded |
| T029 | Old checkpoint compatibility | Verify old checkpoint if code changed | `ERRNet/checkpoints/errnet/errnet_060_00463920.pt`, `ERRNet/experiments/results-improved.md` | Only after code changes | Command/result recorded |
| T030 | CEILNet command record | Prepare `ceilnet_table2` eval command | `ERRNet/experiments/results-improved.md` | After US2 | Command recorded |
| T031 | real20 command record | Prepare `real20` eval command | `ERRNet/experiments/results-improved.md` | After US2 | Command recorded |
| T032 | postcard command record | Prepare `postcard` eval command | `ERRNet/experiments/results-improved.md` | After US2 | Command recorded |
| T033 | objects command record | Prepare `objects` eval command | `ERRNet/experiments/results-improved.md` | After US2 | Command recorded |
| T034 | wild command record | Prepare `wild` eval command | `ERRNet/experiments/results-improved.md` | After US2 | Command recorded |
| T035 | sir2_withgt command record | Prepare `sir2_withgt` eval command | `ERRNet/experiments/results-improved.md` | After US2 | Command recorded |
| T036 | CEILNet benchmark run | Capture `ceilnet_table2` metric row | `ERRNet/test_errnet.py`, `ERRNet/results/`, `ERRNet/experiments/results-improved.md` | After T030 | Metrics/logs/paths recorded |
| T037 | real20 benchmark run | Capture `real20` metric row | `ERRNet/test_errnet.py`, `ERRNet/results/`, `ERRNet/experiments/results-improved.md` | After T031 | Metrics/logs/paths recorded |
| T038 | postcard benchmark run | Capture `postcard` metric row | `ERRNet/test_errnet.py`, `ERRNet/results/`, `ERRNet/experiments/results-improved.md` | After T032 | Metrics/logs/paths recorded |
| T039 | objects benchmark run | Capture `objects` metric row | `ERRNet/test_errnet.py`, `ERRNet/results/`, `ERRNet/experiments/results-improved.md` | After T033 | Metrics/logs/paths recorded |
| T040 | wild benchmark run | Capture `wild` metric row | `ERRNet/test_errnet.py`, `ERRNet/results/`, `ERRNet/experiments/results-improved.md` | After T034 | Metrics/logs/paths recorded |
| T041 | sir2_withgt benchmark run | Capture `sir2_withgt` metric row | `ERRNet/test_errnet.py`, `ERRNet/results/`, `ERRNet/experiments/results-improved.md` | After T035 | Metrics/logs/paths recorded |
| T042 | Metric validity | Record NaN/inf and semantic notes | `ERRNet/experiments/results-improved.md` | After benchmark rows | Validity notes recorded |
| T043 | Custom command record | Prepare custom eval command | `ERRNet/experiments/results-improved.md` | After US2 | Command recorded |
| T044 | Custom outputs | Capture five qualitative outputs | `5pictures/`, `ERRNet/results/`, `ERRNet/experiments/results-improved.md` | After T043 | p1-p5 output paths recorded |
| T045 | Benchmark table | Make metrics reviewable | `ERRNet/experiments/results-improved.md` | After T036-T042 | Full table exists |
| T046 | Custom table | Make qualitative evidence reviewable | `ERRNet/experiments/results-improved.md` | After T044 | Full custom table exists |
| T047 | Evaluation blockers | Preserve failed-row evidence | `ERRNet/experiments/results-improved.md` | As needed | Blockers recorded per row |
| T048 | Benchmark comparison | Compare six metrics to baseline | `ERRNet/experiments/results-baseline.md`, `ERRNet/experiments/results-improved.md` | After US3 | Six comparison outcomes recorded |
| T049 | Custom comparison | Compare five custom outputs | `ERRNet/experiments/results-baseline.md`, `ERRNet/experiments/results-improved.md` | After US3 | Five qualitative notes recorded |
| T050 | Claim status | State improvement claim outcome | `ERRNet/experiments/results-improved.md` | After T048-T049 | Claim status recorded |
| T051 | Risk summary | Record assumptions and residual risks | `ERRNet/experiments/results-improved.md` | After comparison | Risks recorded |
| T052 | Evidence index update | Point index to final evidence | `ERRNet/experiments/README.md` | After US4 evidence | Summary updated |
| T053 | Delivery checklist sync | Update delivery readiness if affected | `ERRNet/experiments/delivery-checklist.md` | Optional after T050 | Checklist updated or no-change reason recorded |
| T054 | README sync | Update user-facing commands if changed | `ERRNet/README_DIP26.md`, `ERRNet/experiments/results-improved.md` | Optional after final commands | README updated or no-change reason recorded |
| T055 | Diff whitespace validation | Catch formatting issues | Listed feature paths | Polish | `git diff --check` result recorded |
| T056 | Placeholder scan | Catch stale planning text | `specs/002-improved-retraining-checkpoint/`, `ERRNet/experiments/results-improved.md` | Polish | Scan result recorded |
| T057 | Scope review | Identify path deviations | Changed files | Polish | Deviations recorded |
| T058 | Compatibility scope review | Confirm no forbidden path changes | Changed source files | Polish, if code changed | Compatibility status recorded |
| T059 | Task status sync | Keep tasks accurate | `specs/002-improved-retraining-checkpoint/tasks.md` | Ongoing/final | Task statuses/blockers updated |
| T060 | Final evidence summary | Close out feature evidence | `ERRNet/experiments/results-improved.md` | Final | Summary includes commands, checksum, metrics, outputs, assumptions, risks |
