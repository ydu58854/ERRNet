# Tasks: Phase D Data Strategy Experiment

**Input**: Design documents from `/specs/004-phase-d-data-strategy/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Planning tasks include static verification. Future implementation
tasks include dataset smoke, tensor scan, benchmark evaluation, output counts,
and log anomaly checks.

**Organization**: Tasks are grouped by user story so candidate design can be
reviewed before any loader or synthetic-data implementation changes.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Close Phase C decision and prepare Phase D planning artifacts.

- [x] T001 Record Phase C epoch-30 training, tensor scan, benchmark, custom recovery, and decision in `ERRNet/experiments/results-improved.md`
- [x] T002 [P] Update Phase C/Phase D current status in `improvement.md`
- [x] T003 [P] Update TODO-007C and TODO-007D status in `todo.md`
- [x] T004 Set current Spec Kit feature pointer in `.specify/feature.json`
- [x] T005 Update current feature plan pointer in `AGENTS.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define data-strategy boundaries before implementation.

- [x] T006 [P] Write Phase D scope, scenarios, requirements, and verification plan in `specs/004-phase-d-data-strategy/spec.md`
- [x] T007 [P] Write Phase D decisions in `specs/004-phase-d-data-strategy/research.md`
- [x] T008 [P] Write Phase D candidate and run entities in `specs/004-phase-d-data-strategy/data-model.md`
- [x] T009 [P] Write Phase D candidate/evaluation contract in `specs/004-phase-d-data-strategy/contracts/phase-d-data-strategy-contract.md`
- [x] T010 [P] Write Phase D quickstart in `specs/004-phase-d-data-strategy/quickstart.md`

**Checkpoint**: Phase D planning is reviewable without source changes.

---

## Phase 3: User Story 1 - Define Safe Phase D Candidate Matrix (Priority: P1) MVP

**Goal**: Provide bounded data-strategy candidates with risks and rollback.

**Independent Test**: Review `research.md`, `data-model.md`, and contract to
confirm each candidate is explicit and reversible.

### Verification for User Story 1

- [x] T011 [P] [US1] Run touchpoint search from `specs/004-phase-d-data-strategy/quickstart.md` and record relevant files before implementation
- [x] T012 [P] [US1] Confirm candidates in `specs/004-phase-d-data-strategy/contracts/phase-d-data-strategy-contract.md` have parameter values, purpose, and rollback expectations

### Implementation for User Story 1

- [x] T013 [US1] Add default-compatible Phase D data option surface in the smallest existing option file identified by T011
- [x] T014 [US1] Add Phase D synthetic parameter application in the smallest existing data path identified by T011
- [x] T015 [US1] Document the exact candidate command and rollback command in `ERRNet/experiments/results-improved.md`

**Checkpoint**: A single Phase D candidate can be enabled without changing old defaults.

---

## Phase 4: User Story 2 - Preserve Benchmark Comparability (Priority: P2)

**Goal**: Verify every Phase D screening run uses prior benchmark/custom workflow.

**Independent Test**: Run dataset availability, short screening, tensor scan,
six benchmark evaluations, custom inference, output count checks, and anomaly
scan for one candidate.

### Verification for User Story 2

- [x] T016 [P] [US2] Run dataset availability check from `specs/004-phase-d-data-strategy/quickstart.md`
- [x] T017 [US2] Run synthetic sample smoke from `specs/004-phase-d-data-strategy/quickstart.md`
- [x] T018 [US2] Run a 10epoch Phase D screening command for the first candidate and save status/log under `ERRNet/experiments/run-logs/`
- [x] T019 [US2] Run checkpoint tensor scan and record SHA256/nonfinite count in `ERRNet/experiments/results-improved.md`
- [x] T020 [US2] Run six benchmark evaluations for the Phase D checkpoint and save status/logs under `ERRNet/experiments/run-logs/`
- [x] T021 [US2] Run custom inference with `--dataset custom --input_dir ../5pictures` and save outputs under a distinct `ERRNet/results/phaseD_*_custom/` directory
- [x] T022 [US2] Check benchmark/custom output counts and log anomaly scan for Phase D logs

### Implementation for User Story 2

- [x] T023 [US2] Record Phase D screening metrics, output counts, and decision in `ERRNet/experiments/results-improved.md`
- [x] T024 [US2] Update `improvement.md` and `todo.md` with the Phase D screening result and next action

**Checkpoint**: One Phase D candidate has comparable evidence.

---

## Phase 5: User Story 3 - Define Implementation Guardrails (Priority: P3)

**Goal**: Keep future Phase D source changes localized, reversible, and documented.

**Independent Test**: Run static checks and review docs to confirm no unrelated
source, dataset, metric, or dependency changes were introduced.

### Verification for User Story 3

- [x] T025 [P] [US3] Run `git diff --check` for Phase C result updates and Phase D planning docs
- [x] T026 [P] [US3] Scan Phase D docs for template placeholders and unresolved clarification markers

### Implementation for User Story 3

- [x] T027 [US3] Summarize Phase D assumptions, risks, and verification gates in `specs/004-phase-d-data-strategy/plan.md`

**Checkpoint**: Planning is complete and implementation remains gated.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and handoff.

- [x] T028 Run `git diff --check` from repository root for all changed planning files
- [x] T029 Confirm `AGENTS.md` and `.specify/feature.json` both point to `specs/004-phase-d-data-strategy/`
- [x] T030 Summarize Phase C final status, Phase D generated artifacts, verification results, assumptions, and residual risks

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Story 1 (P1)**: Depends on Foundational completion
- **User Story 2 (P2)**: Depends on a candidate implementation from User Story 1
- **User Story 3 (P3)**: Can verify planning after Foundational, and must be
  re-run after future source changes
- **Polish**: Depends on selected user stories being complete

### Parallel Opportunities

- T002 and T003 can run in parallel.
- T006 through T010 can run in parallel because they write distinct files.
- T011 and T012 can run in parallel before implementation.
- T016 can run before training, while T017-T022 are sequential for a candidate.
- T025 and T026 can run in parallel for planning verification.

## Implementation Strategy

### MVP First

1. Complete Phase 1 and Phase 2 planning.
2. Implement only one default-compatible candidate from User Story 1 (`gamma_1p1_1p5`).
3. Run synthetic sample smoke before any training.
4. Stop if default behavior changes or smoke fails.

### Incremental Delivery

1. Add one candidate and verify it with a 10epoch screening run.
2. Evaluate all six benchmarks and custom images.
3. Decide whether to expand to another candidate, run a 20epoch screen, or stop.
4. Only after a strong screening signal, consider a longer candidate. The
   `gamma_1p1_1p5` screen did not meet this bar, so it is stopped at 10 epochs.

### Guardrails

- Do not edit benchmark metrics.
- Do not overwrite prior result directories.
- Do not add dependencies.
- Do not report custom images as full-reference metrics.
- Keep rollback to the old default data path explicit.
