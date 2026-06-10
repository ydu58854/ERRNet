# Tasks: Phase C Exclusion-Loss Experiment

**Input**: Design documents from `/specs/003-phasec-exclusion-loss/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Include repeatable smoke and static verification for every meaningful change.

**Organization**: Tasks are grouped by user story so the default-safe option can be implemented and verified before longer experiment guidance is used.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm scope and existing patterns before code changes

- [x] T001 Review existing loss/option/model training paths in `ERRNet/models/losses.py`, `ERRNet/options/errnet/train_options.py`, and `ERRNet/models/errnet_model.py`
- [x] T002 [P] Record Phase C scope and Phase D out-of-scope constraint in `specs/003-phasec-exclusion-loss/plan.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define the loss behavior and command contract shared by all stories

- [x] T003 [P] Document CLI contract for `--lambda_exclusion` in `specs/003-phasec-exclusion-loss/contracts/errnet-phasec-cli-contract.md`
- [x] T004 [P] Document tensor smoke and training smoke commands in `specs/003-phasec-exclusion-loss/quickstart.md`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Default-Safe Exclusion Option (Priority: P1) MVP

**Goal**: Add a default-disabled exclusion-loss option without changing existing training behavior.

**Independent Test**: Syntax checks, option presence/default check, and tensor finite forward/backward smoke.

### Verification for User Story 1

- [x] T005 [P] [US1] Run `python -m py_compile` for `ERRNet/options/errnet/train_options.py`, `ERRNet/models/losses.py`, and `ERRNet/models/errnet_model.py`
- [x] T006 [P] [US1] Run a tensor forward/backward smoke for `ExclusionLoss` from `ERRNet/models/losses.py`
- [x] T007 [P] [US1] Run `python train_errnet.py --help` and confirm `--lambda_exclusion` appears

### Implementation for User Story 1

- [x] T008 [US1] Add `--lambda_exclusion` default `0.0` to `ERRNet/options/errnet/train_options.py`
- [x] T009 [US1] Implement finite `ExclusionLoss` in `ERRNet/models/losses.py`
- [x] T010 [US1] Integrate active exclusion loss into `ERRNet/models/errnet_model.py` for `ERRNetModel.backward_G`
- [x] T011 [US1] Integrate active exclusion loss into `ERRNet/models/errnet_model.py` for `NetworkWrapper.backward_G`

**Checkpoint**: User Story 1 is default-safe and tensor-verified

---

## Phase 4: User Story 2 - Smoke-Run Phase C Training (Priority: P2)

**Goal**: Verify the new loss path in a bounded training run with finite logging and checkpoint creation.

**Independent Test**: Run the bounded smoke command from `quickstart.md`, inspect `Excl` logs, and load the generated checkpoint.

### Verification for User Story 2

- [x] T012 [US2] Run bounded Phase C smoke training from `specs/003-phasec-exclusion-loss/quickstart.md`
- [x] T013 [US2] Verify the smoke log under `ERRNet/experiments/run-logs/` contains finite `Excl` values and no NaN/Inf errors
- [x] T014 [US2] Run checkpoint load/custom inference smoke using `ERRNet/test_errnet.py`

### Implementation for User Story 2

- [x] T015 [US2] Record smoke command, status, checkpoint path, and evidence in `ERRNet/experiments/results-improved.md`

**Checkpoint**: User Story 2 proves the Phase C path can train and load

---

## Phase 5: User Story 3 - Evaluation Guidance For Longer Phase C Runs (Priority: P3)

**Goal**: Make future longer Phase C experiments reproducible and comparable.

**Independent Test**: Review docs for long-run command, six benchmark commands, custom evaluation, naming, and decision rules.

### Verification for User Story 3

- [x] T016 [P] [US3] Run documentation stale-language scan for Phase C/D status in `improvement.md`, `todo.md`, and `ERRNet/experiments/results-improved.md`
- [x] T017 [P] [US3] Run `git diff --check` for changed files

### Implementation for User Story 3

- [x] T018 [US3] Add Phase C usage notes to `ERRNet/README_DIP26.md`
- [x] T019 [US3] Update `improvement.md` with Phase C opened status and Phase D deferred status
- [x] T020 [US3] Update `todo.md` with Phase C smoke/long-run next steps
- [x] T021 [US3] Update `ERRNet/experiments/results-improved.md` with Phase C experiment section and decision rules

**Checkpoint**: User Story 3 provides reproducible guidance for future longer runs

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and handoff

- [x] T022 Run `git diff --check` from repository root and inside `ERRNet/` for touched paths
- [x] T023 Summarize changed files, verification results, assumptions, tradeoffs, and residual risks in `ERRNet/experiments/results-improved.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Story 1 (P1)**: Depends on Foundational completion and blocks smoke training
- **User Story 2 (P2)**: Depends on User Story 1
- **User Story 3 (P3)**: Can update docs after User Story 1, but final evidence depends on User Story 2
- **Polish**: Depends on selected user stories being complete

### Parallel Opportunities

- T002, T003, and T004 are documentation-only and can be done in parallel.
- T005, T006, and T007 can run independently after implementation.
- T016 and T017 can run in parallel after documentation updates.

## Implementation Strategy

### MVP First

1. Complete Setup and Foundational documentation.
2. Implement User Story 1 only.
3. Run syntax, option, and tensor verification.
4. Stop if default-safe behavior or finite tensor behavior fails.

### Incremental Delivery

1. Add User Story 2 bounded smoke training after MVP passes.
2. Add User Story 3 documentation and long-run guidance after smoke evidence is available.
3. Start any long Phase C training only after smoke status and checkpoint load evidence are recorded.
