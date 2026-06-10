# Tasks: ERRNet 单图反射去除课程实验

**Input**: Design documents from `/specs/001-errnet-reflection-spec/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: This feature uses reproducible experiment commands, metric records, visual inspection, and static documentation checks as verification tasks.

**Organization**: Tasks are grouped by user story so each story produces an independently reviewable experiment increment. Keep changes local and avoid unrelated cleanup.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it touches different files and does not depend on incomplete tasks
- **[Story]**: Maps to the user story in `spec.md`
- Every task includes exact file paths and completion criteria

## Phase 1: Setup (Shared Documentation And Evidence Structure)

**Purpose**: Establish shared experiment records before running or changing anything.

- [X] T001 Create `ERRNet/experiments/README.md` with the experiment record structure, required fields, and completion criteria from `specs/001-errnet-reflection-spec/data-model.md`
- [X] T002 Create `ERRNet/experiments/environment.md` template for OS, Python, dependency versions, CUDA/CPU mode, GPU model, and Git commit id
- [X] T003 Create `ERRNet/experiments/datasets.md` template listing raw data, processed data, pretrained weight, benchmark datasets, counts, and `5pictures/` readiness
- [X] T004 Create `ERRNet/experiments/results-baseline.md` template for baseline commands, metric tables, output paths, and blocked/skipped run notes
- [X] T005 Create `ERRNet/experiments/results-improved.md` template for improved-method commands, metric comparison, qualitative paths, and interpretation notes
- [X] T006 Create `ERRNet/experiments/delivery-checklist.md` for paper, code link, weight link, PPT, contribution statement, deadline, and submission status

**Checkpoint**: Shared experiment documentation exists and can capture evidence for every later story.

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Confirm the implementation can proceed without changing existing ERRNet behavior.

- [X] T007 Populate `ERRNet/experiments/environment.md` with actual environment and commit information using the quickstart commands from `specs/001-errnet-reflection-spec/quickstart.md`
- [X] T008 Populate `ERRNet/experiments/datasets.md` with observed paths and counts for `ERRNet/checkpoints/errnet/errnet_060_00463920.pt`, `ERRNet/datasets/raw_data/`, `ERRNet/datasets/processed_data/`, and `5pictures/`
- [X] T009 [P] Review `ERRNet/test_errnet.py` and document supported benchmark/custom command contracts in `ERRNet/experiments/README.md` without changing code
- [X] T010 [P] Review `ERRNet/models/losses.py`, `ERRNet/models/errnet_model.py`, and `ERRNet/options/errnet/train_options.py` to confirm the local loss-weight improvement path and note exact planned touchpoints in `ERRNet/experiments/results-improved.md`
- [X] T011 Run static documentation validation for `specs/001-errnet-reflection-spec/spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/errnet-cli-contract.md`, `quickstart.md`, `checklists/pre-implementation.md`, and `tasks.md`, then record the result in `ERRNet/experiments/README.md`
- [X] T012 Record current dirty worktree state and allowed edit paths in `ERRNet/experiments/README.md` before modifying ERRNet files

**Checkpoint**: Environment, datasets, command contracts, and improvement touchpoints are documented before story implementation starts.

## Phase 3: User Story 1 - 复现 ERRNet Baseline (Priority: P1) MVP

**Goal**: Produce baseline evidence from existing ERRNet commands.

**Independent Test**: At least one benchmark baseline run has a recorded command, environment, result path, and PSNR/SSIM/NCC/LMSE or blocker note.

### Verification for User Story 1

- [X] T013 [US1] Run or document the exact baseline smoke command for `ceilnet_table2` in `ERRNet/experiments/results-baseline.md`
- [X] T014 [US1] Record the baseline smoke output metrics and output path for `ceilnet_table2` in `ERRNet/experiments/results-baseline.md`
- [X] T015 [US1] Record CPU fallback feasibility or blocker notes for the `--gpu_ids -1` baseline command in `ERRNet/experiments/results-baseline.md`

### Implementation for User Story 1

- [X] T016 [US1] Add a baseline reproduction section to `ERRNet/experiments/results-baseline.md` with command, checkpoint path, dataset key, environment reference, metrics, output path, and completion status
- [X] T017 [US1] Add metric semantics notes to `ERRNet/experiments/results-baseline.md` covering prediction/target alignment, crop policy, pixel range, ground-truth requirement, mask or valid-pixel policy, and NaN/inf handling
- [X] T018 [US1] Update `ERRNet/README_DIP26.md` only if the baseline evidence reveals stale command or path guidance; otherwise record "No change required" in `ERRNet/experiments/results-baseline.md`

**Checkpoint**: Baseline MVP can be reviewed independently from `ERRNet/experiments/results-baseline.md`.

## Phase 4: User Story 2 - 评估指定数据集和自采图像 (Priority: P2)

**Goal**: Complete benchmark and custom-image evaluation evidence.

**Independent Test**: All six benchmark rows and five custom-image qualitative rows are recorded with metric values, output paths, or explicit unavailable/blocker reasons.

### Verification for User Story 2

- [X] T019 [US2] Record benchmark commands for `ceilnet_table2`, `real20`, `postcard`, `objects`, `wild`, and `sir2_withgt` in `ERRNet/experiments/results-baseline.md`
- [X] T020 [US2] Record PSNR, SSIM, NCC, and LMSE values or blocked reasons for all six benchmark datasets in `ERRNet/experiments/results-baseline.md`
- [X] T021 [US2] Record NaN/inf status, valid ground-truth status, mask or valid-pixel policy, and crop/alignment notes for each benchmark row in `ERRNet/experiments/results-baseline.md`
- [X] T022 [US2] Record the custom-image command and output path expectations for `../5pictures` in `ERRNet/experiments/results-baseline.md`
- [X] T023 [US2] Inspect or document output folders for `5pictures/p1.jpg` through `5pictures/p5.jpg` in `ERRNet/experiments/results-baseline.md`

### Implementation for User Story 2

- [X] T024 [US2] Add a full benchmark results table to `ERRNet/experiments/results-baseline.md` with method, dataset, PSNR, SSIM, NCC, LMSE, metric status, command, and output path columns
- [X] T025 [US2] Add a custom-image qualitative table to `ERRNet/experiments/results-baseline.md` with image name, input path, output path, visual notes, and ground-truth status
- [X] T026 [US2] Add a limitations note to `ERRNet/experiments/results-baseline.md` explaining why custom images are qualitative unless ground truth is provided

**Checkpoint**: Benchmark and custom-image baseline evidence can support the paper's experiment section.

## Phase 5: User Story 3 - 设计并验证改进算法 (Priority: P3)

**Goal**: Implement and document a local, compatible improved-method experiment.

**Independent Test**: Improved method has a distinct experiment name, preserves baseline defaults, passes a smoke run or documented blocker, and records comparison evidence against baseline.

### Implementation for User Story 3

- [X] T027 [US3] Confirm current default loss composition in `ERRNet/models/losses.py` and record the baseline default in `ERRNet/experiments/results-improved.md`
- [X] T028 [US3] If any loader, resize/crop/augmentation, or metric implementation change becomes necessary, stop and update `specs/001-errnet-reflection-spec/spec.md`, `plan.md`, and `tasks.md` before editing ERRNet code
- [X] T029 [US3] Add optional loss-weight arguments with baseline-compatible defaults in `ERRNet/options/errnet/train_options.py`
- [X] T030 [US3] Parameterize existing `MultipleLoss` usage in `ERRNet/models/losses.py` so default weights preserve current behavior and optional weights enable the structural-loss experiment
- [X] T031 [US3] Update `ERRNet/models/errnet_model.py` only if needed to expose the improved loss term in current error reporting without changing default training behavior

### Verification for User Story 3

- [X] T032 [US3] After code changes, run a CPU import and option-parse smoke check for `ERRNet/options/errnet/train_options.py`, `ERRNet/models/losses.py`, and `ERRNet/models/errnet_model.py`, then record shape/dtype/device notes in `ERRNet/experiments/results-improved.md`
- [X] T033 [US3] After code changes, verify the existing `ERRNet/checkpoints/errnet/errnet_060_00463920.pt` checkpoint loads and runs default inference, then record the command/result in `ERRNet/experiments/results-improved.md`
- [X] T034 [US3] Run or document an improved-method smoke command with a distinct experiment name and record outputs in `ERRNet/experiments/results-improved.md`
- [X] T035 [US3] Run or document improved-method custom image inference for `5pictures/p1.jpg` through `5pictures/p5.jpg` and record output paths in `ERRNet/experiments/results-improved.md`
- [X] T036 [US3] Compare improved and baseline evidence on at least one benchmark and all five custom images, or document blockers in `ERRNet/experiments/results-improved.md`
- [X] T037 [US3] Document the improved-method motivation, changed options, run command, default compatibility, old-checkpoint compatibility, tensor shape/dtype/device notes, and extra compute notes in `ERRNet/experiments/results-improved.md`
- [X] T038 [US3] Update `ERRNet/README_DIP26.md` with improved-method usage only if new command-line options are added; otherwise record "No README change required" in `ERRNet/experiments/results-improved.md`

**Checkpoint**: Improved method is local, compatible by default, and backed by recorded smoke/comparison evidence.

## Phase 6: User Story 4 - 完成课程交付材料 (Priority: P4)

**Goal**: Prepare final submission readiness evidence.

**Independent Test**: Delivery checklist clearly states complete, blocked, or missing status for paper, repository link, model weight link, PPT, contribution statement, and submission instructions.

### Verification for User Story 4

- [X] T039 [US4] Review `ERRNet/experiments/results-baseline.md` and `ERRNet/experiments/results-improved.md` for paper-ready metrics, qualitative examples, failure cases, metric semantics, checkpoint compatibility, and limitations
- [X] T040 [US4] Review `ERRNet/experiments/delivery-checklist.md` for paper, code link, weight link, PPT, member contributions, deadline, and email subject completeness

### Implementation for User Story 4

- [X] T041 [US4] Fill `ERRNet/experiments/delivery-checklist.md` with current status, links or missing reasons, and final submission notes
- [X] T042 [US4] Add a paper/PPT evidence mapping in `ERRNet/experiments/delivery-checklist.md` linking background, method, experiment, sample analysis, conclusion, and contribution sections to available evidence files without generating final paper or PPT assets

**Checkpoint**: Course delivery readiness is documented even if some external artifacts remain blocked.

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Validate that the work stayed scoped and evidence-backed.

- [X] T043 Run `git diff --check -- ERRNet/experiments ERRNet/options/errnet/train_options.py ERRNet/models/losses.py ERRNet/models/errnet_model.py ERRNet/README_DIP26.md specs/001-errnet-reflection-spec/spec.md specs/001-errnet-reflection-spec/plan.md specs/001-errnet-reflection-spec/research.md specs/001-errnet-reflection-spec/data-model.md specs/001-errnet-reflection-spec/contracts/errnet-cli-contract.md specs/001-errnet-reflection-spec/quickstart.md specs/001-errnet-reflection-spec/checklists/pre-implementation.md specs/001-errnet-reflection-spec/tasks.md`
- [X] T044 Review changed files and report any unrelated edits outside `ERRNet/experiments/`, explicitly approved ERRNet implementation files, and `specs/001-errnet-reflection-spec/`; only remove edits introduced by this feature
- [X] T045 Summarize implementation content, commands run, verification results, assumptions, and residual risks in `ERRNet/experiments/README.md`

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Starts immediately and creates shared evidence files.
- **Foundational (Phase 2)**: Depends on Setup; blocks all user story work.
- **US1 Baseline MVP (Phase 3)**: Depends on Foundational.
- **US2 Full Evaluation (Phase 4)**: Depends on US1 because it extends baseline evidence.
- **US3 Improved Method (Phase 5)**: Depends on US1 for baseline comparison; can overlap with US2 after baseline smoke evidence exists.
- **US4 Delivery (Phase 6)**: Depends on US1-US3 evidence, but checklist structure can be filled incrementally.
- **Polish (Phase 7)**: Runs after desired user stories are complete.

### User Story Dependencies

- **US1**: No dependency beyond foundational readiness; recommended MVP.
- **US2**: Depends on US1 baseline smoke command and evidence structure.
- **US3**: Depends on US1 baseline evidence, metric semantics, and foundational touchpoint review.
- **US4**: Depends on the evidence available from US1-US3.

### Parallel Opportunities

- T009 and T010 can run in parallel after setup.
- US2 benchmark and custom-image documentation tasks can be split across datasets/images after T017.
- US3 option/loss/model tasks should be sequential because they touch related training behavior and checkpoint compatibility.
- US4 review tasks can run in parallel after evidence files exist.

## Parallel Example: Foundational Review

```bash
Task: "Review ERRNet/test_errnet.py and document command contracts in ERRNet/experiments/README.md"
Task: "Review ERRNet/models/losses.py, ERRNet/models/errnet_model.py, and ERRNet/options/errnet/train_options.py and document touchpoints in ERRNet/experiments/results-improved.md"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 setup files.
2. Complete Phase 2 readiness checks.
3. Complete Phase 3 baseline smoke evidence.
4. Stop and validate that baseline evidence is reproducible and paper-ready.

### Incremental Delivery

1. Baseline MVP evidence.
2. Full benchmark and custom-image baseline evidence.
3. Local improved-method experiment and comparison.
4. Delivery checklist and paper evidence mapping.

### Completion Criteria Summary

- Every changed file has a direct link to the feature.
- Existing ERRNet commands remain valid.
- Any optional improved-method code preserves default behavior.
- Verification results and residual risks are recorded before claiming completion.

## Task Detail Matrix

| Task | Title | Goal | Affected Files / Modules | Dependencies / Order | Completion Criteria |
|------|-------|------|--------------------------|----------------------|---------------------|
| T001 | Experiment record index | Define the evidence structure for all experiment records | `ERRNet/experiments/README.md` | First setup task | File lists record types, required fields, and completion rules |
| T002 | Environment template | Capture reproducibility environment fields | `ERRNet/experiments/environment.md` | After T001 | Template includes OS, Python, dependencies, CUDA/CPU, GPU, commit id |
| T003 | Dataset readiness template | Capture data and weight readiness | `ERRNet/experiments/datasets.md` | After T001 | Template covers raw/processed data, weights, benchmark counts, custom images |
| T004 | Baseline results template | Prepare baseline command and metric recording | `ERRNet/experiments/results-baseline.md` | After T001 | Template includes command, metrics, output path, status, blocker fields |
| T005 | Improved results template | Prepare improved-method comparison recording | `ERRNet/experiments/results-improved.md` | After T001 | Template includes motivation, command, metrics, qualitative paths, risks |
| T006 | Delivery checklist | Track course submission readiness | `ERRNet/experiments/delivery-checklist.md` | After T001 | Checklist includes paper, code link, weight link, PPT, contributions, deadline |
| T007 | Populate environment | Record actual runtime environment | `ERRNet/experiments/environment.md` | After T002 | Actual environment and commit values are recorded or blockers stated |
| T008 | Populate datasets | Record actual data, weight, and custom image readiness | `ERRNet/experiments/datasets.md` | After T003 | Paths, counts, and missing/blocker notes are recorded |
| T009 | Document test command contract | Confirm benchmark/custom entrypoint without code changes | `ERRNet/test_errnet.py`, `ERRNet/experiments/README.md` | After T001; parallel with T010 | Supported dataset keys and custom-image behavior are documented |
| T010 | Document improvement touchpoints | Identify minimal loss-weight implementation surface | `ERRNet/models/losses.py`, `ERRNet/models/errnet_model.py`, `ERRNet/options/errnet/train_options.py`, `ERRNet/experiments/results-improved.md` | After T005; parallel with T009 | Exact candidate files and "no architecture rewrite" boundary are recorded |
| T011 | Static planning validation | Confirm planning artifacts are clean before implementation | `specs/001-errnet-reflection-spec/spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/errnet-cli-contract.md`, `quickstart.md`, `checklists/pre-implementation.md`, `tasks.md`, `ERRNet/experiments/README.md` | After T001-T010 | Validation command/result and residual issues are recorded |
| T012 | Dirty worktree record | Preserve scope control before editing ERRNet files | `ERRNet/experiments/README.md` | After T007-T011 | Current dirty state and allowed edit paths are recorded |
| T013 | Baseline smoke command | Establish the first reproducible baseline run | `ERRNet/experiments/results-baseline.md` | After T007-T012 | Exact `ceilnet_table2` command is recorded or blocker stated |
| T014 | Baseline smoke metrics | Capture smoke-run outputs | `ERRNet/experiments/results-baseline.md` | After T013 | Metrics and output path are recorded or blocker stated |
| T015 | CPU fallback note | Capture CPU-mode feasibility | `ERRNet/experiments/results-baseline.md` | After T013 | CPU fallback result, feasibility, or blocker is recorded |
| T016 | Baseline reproduction section | Make US1 evidence reviewable | `ERRNet/experiments/results-baseline.md` | After T013-T015 | Section includes command, checkpoint, dataset, environment, metrics, output path, status |
| T017 | Baseline metric semantics | Prevent invalid metric interpretation | `ERRNet/experiments/results-baseline.md` | After T014 | Prediction/target alignment, crop policy, pixel range, GT requirement, mask or valid-pixel policy, and NaN/inf handling are recorded |
| T018 | Baseline README sync | Update stale guidance only if evidence proves it | `ERRNet/README_DIP26.md`, `ERRNet/experiments/results-baseline.md` | After T016-T017 | README updated or "No change required" recorded |
| T019 | Full benchmark commands | Record all benchmark evaluation commands | `ERRNet/experiments/results-baseline.md` | After US1 baseline smoke | Six dataset commands are recorded |
| T020 | Full benchmark metrics | Capture benchmark quantitative results | `ERRNet/experiments/results-baseline.md` | After T019 and each run | PSNR/SSIM/NCC/LMSE or blocked reason recorded for all six datasets |
| T021 | Benchmark metric sanity | Record metric validity per benchmark row | `ERRNet/experiments/results-baseline.md` | After T020 | NaN/inf status, valid GT status, mask or valid-pixel policy, and crop/alignment notes are recorded for each row |
| T022 | Custom command | Record custom-image evaluation path | `ERRNet/experiments/results-baseline.md` | After US1 baseline smoke | Custom command and expected output paths are recorded |
| T023 | Custom output evidence | Capture five-image qualitative evidence | `5pictures/`, `ERRNet/results/custom/`, `ERRNet/experiments/results-baseline.md` | After T022 | p1-p5 output folder status and notes are recorded |
| T024 | Benchmark results table | Make full quantitative evidence paper-ready | `ERRNet/experiments/results-baseline.md` | After T019-T021 | Table includes method, dataset, metrics, metric status, command, and output path |
| T025 | Custom qualitative table | Make custom image evidence paper-ready | `ERRNet/experiments/results-baseline.md` | After T022-T023 | Table includes image, input, output, visual notes, and ground-truth status |
| T026 | Custom metric limitation | Prevent invalid full-reference metric claims | `ERRNet/experiments/results-baseline.md` | After T025 | Limitation note explains qualitative-only status unless GT exists |
| T027 | Default loss record | Preserve current baseline loss behavior | `ERRNet/models/losses.py`, `ERRNet/experiments/results-improved.md` | After T010 | Current default composition and weights are recorded |
| T028 | Loader and metric guard | Prevent unapproved data or metric semantic changes | `specs/001-errnet-reflection-spec/spec.md`, `plan.md`, `tasks.md` | Before any loader/metric/augmentation edit | Work stops and planning docs are updated before such code is changed |
| T029 | Add loss options | Expose optional loss weights safely | `ERRNet/options/errnet/train_options.py` | After T027-T028 | New options default to current behavior and are documented in help text |
| T030 | Parameterize loss composition | Enable structural-loss experiment without a new loss stack | `ERRNet/models/losses.py` | After T029 | Existing default weights preserved; optional weights influence existing `MultipleLoss` use |
| T031 | Report improved loss term | Surface new loss evidence only if needed | `ERRNet/models/errnet_model.py` | After T030 | Error reporting changes are optional and default-safe |
| T032 | CPU import and option smoke | Verify changed loss/option paths are importable and shape-safe | `ERRNet/options/errnet/train_options.py`, `ERRNet/models/losses.py`, `ERRNet/models/errnet_model.py`, `ERRNet/experiments/results-improved.md` | After T029-T031 | CPU import, option parse, tensor shape, dtype, and device notes are recorded |
| T033 | Old checkpoint compatibility | Verify default inference still works with the existing checkpoint | `ERRNet/checkpoints/errnet/errnet_060_00463920.pt`, `ERRNet/experiments/results-improved.md` | After T032 | Existing checkpoint load/default inference command and result are recorded |
| T034 | Improved smoke run | Establish improved-method evidence | `ERRNet/experiments/results-improved.md`, `ERRNet/checkpoints/`, `ERRNet/results/` | After T032-T033 | Distinct experiment name, command, output path, and status recorded |
| T035 | Improved custom output | Capture improved outputs for five custom images | `5pictures/`, `ERRNet/results/`, `ERRNet/experiments/results-improved.md` | After T034 | Output paths for p1-p5 are recorded or blockers stated |
| T036 | Improved comparison | Compare improved method with baseline | `ERRNet/experiments/results-improved.md`, `ERRNet/experiments/results-baseline.md` | After T024-T035 | At least one benchmark and all five custom-image comparisons are recorded, or blockers are stated |
| T037 | Document improved method | Make improved experiment reproducible | `ERRNet/experiments/results-improved.md` | After T028-T035 | Motivation, options, command, default compatibility, old-checkpoint compatibility, tensor notes, and compute notes recorded |
| T038 | Improved README sync | Update user-facing commands only if new options exist | `ERRNet/README_DIP26.md`, `ERRNet/experiments/results-improved.md` | After T037 | README updated or "No README change required" recorded |
| T039 | Paper evidence review | Confirm experiment evidence is paper-ready | `ERRNet/experiments/results-baseline.md`, `ERRNet/experiments/results-improved.md` | After US1-US3 evidence | Metrics, qualitative examples, failures, metric semantics, checkpoint compatibility, and limitations reviewed |
| T040 | Delivery checklist review | Confirm submission checklist coverage | `ERRNet/experiments/delivery-checklist.md` | After T006 and available evidence | Required deliverable fields are present |
| T041 | Fill delivery checklist | Record current delivery status | `ERRNet/experiments/delivery-checklist.md` | After T040 | Links, missing reasons, and final notes filled |
| T042 | Paper/PPT evidence mapping | Tie paper and PPT sections to available evidence without generating final assets | `ERRNet/experiments/delivery-checklist.md` | After T039-T041 | Background/method/experiment/analysis/conclusion/contribution mapping exists and final paper/PPT generation remains out of scope |
| T043 | Diff whitespace validation | Catch formatting issues in changed files | `ERRNet/experiments/`, `ERRNet/options/errnet/train_options.py`, `ERRNet/models/losses.py`, `ERRNet/models/errnet_model.py`, `ERRNet/README_DIP26.md`, `specs/001-errnet-reflection-spec/` | After implementation tasks | `git diff --check` passes or issues are recorded |
| T044 | Scope review | Report unrelated existing edits and clean only feature-introduced unrelated edits | Changed feature files | After T043 | Changed files are limited to approved paths or exceptions are justified |
| T045 | Final evidence summary | Provide completion evidence and residual risks | `ERRNet/experiments/README.md` | Final task | Summary states changes, commands, verification results, assumptions, and risks |
