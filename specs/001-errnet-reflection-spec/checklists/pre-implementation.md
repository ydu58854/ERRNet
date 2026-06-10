# Pre-Implementation Checklist: ERRNet 单图反射去除课程实验

**Purpose**: Validate implementation readiness before planning moves into task execution
**Created**: 2026-05-24
**Feature**: [spec.md](../spec.md)

## Requirement Completeness

- [x] CHK001 Are the baseline reproduction requirements complete for environment, data, weights, benchmark evaluation, and result recording? [Completeness, Spec §FR-001..FR-005]
- [x] CHK002 Are improved-method requirements complete enough to choose a local implementation without redesigning the ERRNet architecture? [Completeness, Spec §FR-007..FR-009, Plan §3]
- [x] CHK003 Are final delivery tracking requirements complete for paper evidence, code repository link, model weight link, PPT status, and member contribution statement, without requiring this spec to generate final paper/PPT assets? [Completeness, Spec §FR-011..FR-012]
- [x] CHK004 Are data readiness requirements defined for raw data, processed data, pretrained weight, benchmark datasets, and five custom images? [Completeness, Spec §FR-003, Plan §5]

## Requirement Clarity

- [x] CHK005 Is "minimal viable implementation" clarified as reusing existing ERRNet scripts and avoiding a parallel experiment runner? [Clarity, Plan §1]
- [x] CHK006 Is the default improved-method direction clearly bounded to local structural-loss weighting unless later changed explicitly? [Clarity, Plan §1, Plan §3]
- [x] CHK007 Are the boundaries between quantitative benchmark evaluation and qualitative custom-image evaluation unambiguous? [Clarity, Spec §Edge Cases, Research §Custom Images]
- [x] CHK008 Are affected files and directories listed specifically enough for implementation to avoid unrelated edits? [Clarity, Plan §2, Plan §3]

## Non-Goals And Scope Boundaries

- [x] CHK009 Are non-goals explicit for model rewrites, new data sources, course deadline changes, and generation of final paper/PPT assets? [Scope, Spec §Scope]
- [x] CHK010 Are out-of-scope architecture changes distinguished from later optional improved-method changes that would require explicit approval? [Scope, Plan §3]
- [x] CHK011 Are dataset and checkpoint artifacts treated as inputs/outputs rather than files to modify? [Scope, Plan §3, Contract §Compatibility]

## Acceptance Criteria Quality

- [x] CHK012 Are success criteria measurable using counts, artifact presence, metric records, or documented missing reasons? [Measurability, Spec §SC-001..SC-006]
- [x] CHK013 Are baseline and improved-method comparison criteria tied to observable evidence rather than subjective claims? [Acceptance Criteria, Spec §SC-004]
- [x] CHK014 Are custom-image acceptance criteria valid when full-reference metrics are unavailable? [Acceptance Criteria, Spec §SC-003]
- [x] CHK015 Are delivery readiness criteria objective enough to decide whether the course package is complete? [Acceptance Criteria, Spec §SC-006]

## Affected Modules And Integration Points

- [x] CHK016 Are all relevant existing entrypoints identified for data preparation, baseline evaluation, training, finetuning, metrics, and custom-image inference? [Coverage, Plan §2, Plan §4]
- [x] CHK017 Are integration contracts documented for dataset keys, command shapes, result directories, metric names, and checkpoint paths? [Coverage, Contract §Baseline Benchmark Evaluation]
- [x] CHK018 Are planned implementation files limited to `train_options.py`, `losses.py`, `errnet_model.py`, and experiment documentation when improvement work is needed? [Scope, Plan §3]
- [x] CHK019 Are modules that must remain unchanged called out clearly enough to prevent accidental regressions? [Coverage, Plan §3, Contract §Compatibility]

## Compatibility And Regression Risk

- [x] CHK020 Are compatibility requirements explicit that existing commands, defaults, dataset keys, metric names, and checkpoint paths must keep working? [Compatibility, Contract §Compatibility]
- [x] CHK021 Are regression risks identified for metric drift, CUDA/dependency differences, dirty worktree state, and custom-image ground truth limitations? [Risk, Plan §6]
- [x] CHK022 Are future optional arguments required to default to current baseline behavior? [Compatibility, Plan §6]
- [x] CHK023 Are compute-resource limits and long-training risks documented with a mitigation path? [Risk, Plan §6]

## Verification Strategy

- [x] CHK024 Are static validation requirements defined for generated planning artifacts and placeholder-free documents? [Verification, Plan §5]
- [x] CHK025 Are baseline readiness checks defined for pretrained weights, processed data, and custom images? [Verification, Plan §5, Quickstart §2]
- [x] CHK026 Are benchmark and custom-image verification paths defined separately, with qualitative-only handling for missing ground truth? [Verification, Quickstart §4..§6]
- [x] CHK027 Are improved-method validation requirements defined for default compatibility, old-checkpoint compatibility, smoke runs, five custom-image outputs, and comparison evidence? [Verification, Plan §5, Quickstart §7]

## Artifact Synchronization

- [x] CHK028 Are documentation updates identified for plan, quickstart, tasks, contracts, experiment records, and delivery checklist? [Synchronization, Plan §3]
- [x] CHK029 Are configuration or script updates intentionally marked as unnecessary unless the improved method needs optional loss weights? [Synchronization, Plan §3]
- [x] CHK030 Are testing and verification updates represented as experiment commands and evidence records rather than a new test framework? [Synchronization, Spec §Artifact Synchronization]
- [x] CHK031 Are dependency changes explicitly excluded unless a later task documents reason, benefit, and verification impact? [Dependency, Spec §FR-009, Plan §Constitution Check]

## Ambiguities And Assumptions

- [x] CHK032 Are assumptions about project type, current ERRNet paths, custom-image ground truth, and reference metrics documented? [Assumption, Spec §Assumptions]
- [x] CHK033 Is the choice of structural-loss weighting as the default improvement presented as an assumption rather than an irreversible requirement? [Assumption, Plan §6]
- [x] CHK034 Are unresolved choices, such as exact improved loss weights and training duration, deferred to implementation tasks with validation criteria? [Ambiguity, Research §Default Improved Method]

## Metric And Compatibility Readiness

- [x] CHK035 Are metric semantics defined for prediction/target alignment, crop policy, pixel range, ground-truth requirement, mask or valid-pixel policy, NaN/inf handling, and unavailable metrics? [Metric, Spec §FR-013, Plan §5]
- [x] CHK036 Are tensor shape, dtype, and device expectations tied to an import/options smoke check for changed loss or model paths? [Compatibility, Tasks T032]
- [x] CHK037 Is old checkpoint load/default inference compatibility required after any loss-option or model reporting change? [Compatibility, Spec §FR-014, Tasks T033]
- [x] CHK038 Are improved-method outputs required for all five custom images, with blockers recorded if any image cannot run? [Verification, Spec §FR-015, Tasks T035-T036]
- [x] CHK039 Is dirty worktree state captured before implementation, and are allowed edit paths limited to feature planning artifacts, experiment records, and explicitly approved ERRNet files? [Scope, Tasks T012, T044]
- [x] CHK040 Is the runtime compatibility boundary explicit as CPU import/CPU inference plus single-card CUDA, with multi-card or distributed training out of scope? [Compatibility, Spec §Assumptions, Plan §Technical Context]
