# Implementation Plan: ERRNet 单图反射去除课程实验

**Branch**: `001-errnet-reflection-spec` | **Date**: 2026-05-24 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-errnet-reflection-spec/spec.md`

## Summary

为 DIP26 ERRNet 课程项目建立一个最小可行、可复现实验实施方案：先复用现有 ERRNet 数据准备、训练、测试、指标和结果输出流程完成 baseline 复现，再以局部损失权重调整作为默认改进实验方向，最后形成实验记录、结果对比、论文/PPT 证据映射和课程交付清单。不新增并行评估系统，不重写模型架构，不改变已有命令默认行为。

## 1. 实现思路概述

1. 固定现有 ERRNet 仓库作为唯一实验执行入口，优先使用 `README_DIP26.md`、`test_errnet.py`、`train_errnet.py`、`train_errnet_unaligned.py`、`util/index.py` 和现有数据目录。
2. 先完成环境、权重、数据和自采图片的只读核验，生成可追溯实验记录。
3. 使用现有 `test_errnet.py` 跑 baseline benchmark 和 `custom` 自采图像，记录 PSNR、SSIM、NCC、LMSE 或不可计算原因。
4. 默认改进方向选择结构约束损失实验：复用 `models/losses.py` 中已有 `GradientLoss` 和 `MultipleLoss`，只在必要时将权重参数化，保持默认值与当前行为兼容。
5. 改进实验通过新的实验名、现有训练入口和现有测试入口产出结果，与 baseline 共享数据划分和评价指标。
6. 汇总论文/PPT 需要的环境、训练设置、定量表格、定性图像、失败案例、局限性和提交清单；实际论文/PPT 成稿、上传和邮件发送不属于本实施计划。

## Technical Context

**Language/Version**: Python 3.10 for the course environment; existing ERRNet code is Python.

**Primary Dependencies**: Existing ERRNet dependencies in `ERRNet/requirements.txt`, PyTorch/TorchVision/Torchaudio per course guide, OpenCV/skimage/visdom/tensorboardX as already used by the repository.

**Storage**: Local filesystem datasets, checkpoints, results, and documentation files. No database.

**Testing**: Reproducible command runs, metric table inspection, visual output inspection, and static documentation review. No new automated test framework is required for the planning scope.

**Target Platform**: Linux workstation or server with CPU mode and optional single-card CUDA GPU; CPU inference remains supported through existing `--gpu_ids -1` behavior. Multi-card or distributed training is not a current acceptance target.

**Project Type**: ML repository with CLI-style scripts for data preparation, training, inference, and evaluation.

**Performance Goals**: Baseline and improved experiments should be runnable within course-resource expectations; the default improvement must avoid large additional GPU demand beyond baseline-scale training or inference.

**Constraints**: Keep modifications local, preserve current behavior by default, avoid unrelated refactors, avoid new dependencies, do not modify loader/metric semantics by default, and document any non-default compute or data assumptions.

**Scale/Scope**: One course project covering 6 benchmark evaluation targets, 5 custom images, one baseline, one improved method, and final report artifacts.

## 2. 优先检查的代码区域

- `ERRNet/README_DIP26.md`: course-specific runbook and baseline reference.
- `DIP26_ERRNet_实验指导.md`: authoritative course requirements, deadline, datasets, metrics, and report structure.
- `ERRNet/test_errnet.py`: benchmark/custom inference and evaluation entrypoint.
- `ERRNet/train_errnet.py`: aligned-data baseline training entrypoint.
- `ERRNet/train_errnet_unaligned.py`: unaligned finetuning entrypoint.
- `ERRNet/models/losses.py`: existing pixel, gradient, VGG, contextual, and GAN loss helpers.
- `ERRNet/models/errnet_model.py`: loss aggregation and current train/eval/test behavior.
- `ERRNet/options/errnet/train_options.py`: training options and candidate place for optional loss weights.
- `ERRNet/util/index.py`: PSNR, SSIM, NCC, LMSE metric implementation.
- `ERRNet/datasets/prepare_train_data.py` and `ERRNet/datasets/prepare_test_data.py`: processed data generation.
- `5pictures/`: custom images used for qualitative evaluation.
- `specs/001-errnet-reflection-spec/`: generated planning, checklist, task, and quickstart artifacts.

## 3. 按模块划分的拟修改内容

### Documentation And Experiment Records

Potentially changed:
- `specs/001-errnet-reflection-spec/quickstart.md`: concrete execution and validation path.
- `specs/001-errnet-reflection-spec/tasks.md`: implementation task list.
- `ERRNet/README_DIP26.md`: update only if implementation changes commands or report guidance.
- Optional future docs under `ERRNet/experiments/` or `ERRNet/results_summary.md`: record environment, dataset counts, run commands, metrics, visual result paths, and submission checklist.

Not changed:
- Course deadline, submission email, grading percentages, external dataset URLs, or paper structure requirements from the guide.

### Baseline Evaluation

Potentially changed:
- No code changes expected for baseline evaluation.
- Optional future experiment record files may reference outputs under `ERRNet/results/`.

Not changed:
- `ERRNet/test_errnet.py` command behavior, dataset keys, result directory defaults, metric definitions, checkpoint loading, and custom image behavior.

### Improved Method

Potentially changed only if the implementation phase proceeds beyond documentation:
- `ERRNet/options/errnet/train_options.py`: add optional loss weight arguments with defaults matching current behavior.
- `ERRNet/models/losses.py`: reuse or minimally parameterize existing `GradientLoss` composition.
- `ERRNet/models/errnet_model.py`: report any new loss term in `get_current_errors()` only when enabled.
- Optional script or note under `ERRNet/experiments/`: store exact improved run command and comparison table.

Not changed unless explicitly approved later:
- Network architecture in `ERRNet/models/arch.py` or `ERRNet/models/networks.py`.
- Data loader semantics in `ERRNet/data/` and `ERRNet/datasets/`.
- Metric implementation in `ERRNet/util/index.py`.
- Pretrained baseline weights and raw/processed datasets.
- Multi-card or distributed training adaptation; current validation records CPU and single-card behavior only.

### Delivery Artifacts

Potentially changed:
- Documentation/checklist files that track paper sections, repository link, model weight link, PPT status, contribution statement, and known limitations.

Not changed:
- Actual course paper, PPT, and uploaded model links are outside this repository plan unless a later request asks to create them.

## 4. 集成点

- Data preparation integrates through `ERRNet/datasets/prepare_test_data.py` and `ERRNet/datasets/prepare_train_data.py`.
- Baseline and improved benchmark evaluation integrate through `ERRNet/test_errnet.py --dataset <key>`.
- Custom image qualitative evaluation integrates through `ERRNet/test_errnet.py --dataset custom --input_dir ../5pictures`.
- Baseline aligned training integrates through `ERRNet/train_errnet.py`.
- Unaligned finetuning integrates through `ERRNet/train_errnet_unaligned.py`.
- Metrics integrate through `ERRNet/util/index.py` and existing `Engine.eval()` aggregation.
- Experiment naming integrates with existing `--name` and `checkpoints/{experiment_name}` / `results/{dataset_name}` conventions.
- Agent runtime guidance integrates through `AGENTS.md`, which points to this plan.

## 5. 验证策略

1. Static validation:
   - Confirm all planned documents exist under `specs/001-errnet-reflection-spec/`.
   - Confirm no unresolved clarification markers or template placeholders remain in spec, plan, research, data-model, contracts, quickstart, checklists, and tasks.
   - Run `git diff --check` on changed planning, checklist, contract, quickstart, and task files.
2. Baseline readiness validation:
   - Confirm `ERRNet/checkpoints/errnet/errnet_060_00463920.pt` exists.
   - Confirm processed benchmark directories and `5pictures/p1.jpg` through `p5.jpg` exist.
   - Record current dirty worktree state and identify allowed edit paths before modifying files.
3. Baseline execution validation:
   - Run at least one small benchmark or CPU smoke command when resources allow.
   - For full validation, run all six benchmark keys and record PSNR/SSIM/NCC/LMSE.
   - Run custom image inference and inspect that each image has an output folder with input and output image.
   - Record metric semantics: prediction/target alignment, crop policy for size mismatch, pixel value range, ground-truth requirement, mask or valid-pixel policy, and NaN/inf or invalid-result handling.
4. Improved method validation:
   - Confirm default configuration reproduces current loss behavior.
   - Run CPU import and optional GPU forward/backward smoke checks for changed loss/options paths, including tensor shape, dtype, and device notes.
   - Verify the old baseline checkpoint loads and runs inference with default options after code changes.
   - Run a short debug training or inference smoke check before long training.
   - Compare baseline and improved outputs on at least one benchmark and all five custom images, or record blockers.
5. Delivery validation:
   - Confirm report table includes environment, command, dataset, method, metrics, and qualitative paths.
   - Confirm custom images without ground truth are marked qualitative unless references are provided.
   - Confirm final submission checklist covers paper, code link, weight link, PPT, contribution statement, and deadline.

## 6. 风险 / 未知项 / 假设

- Assumption: The feature is approved as a course experiment implementation workflow, not a request to immediately redesign ERRNet.
- Assumption: Default improved direction may be structural loss weighting because it is local, uses existing code, and preserves architecture.
- Risk: Long training may exceed available GPU time. Mitigation: require smoke/debug validation and record full-training feasibility separately.
- Risk: Dependency and CUDA versions may shift metric values. Mitigation: record exact environment and use actual measured results in the paper.
- Risk: Custom images lack ground truth. Mitigation: treat them as qualitative unless paired references are created.
- Risk: Existing repo is already dirty. Mitigation: edit only feature planning artifacts and later explicitly scoped implementation files.
- Risk: Metric values can become invalid if prediction/target alignment, image range, valid-pixel policy, or invalid values differ. Mitigation: record metric semantics and sanity-check NaN/inf status before reporting.
- Assumption: This spec covers the ERRNet PJ task and evidence preparation only; final paper/PPT authoring, upload links, and submission email are tracked but not produced unless a later request explicitly expands scope.
- Risk: Optional loss parameters could break pretrained checkpoint inference. Mitigation: defaults must preserve current behavior and old checkpoint load/inference must be verified.
- Assumption: CPU and single-card CUDA checks are sufficient for this ERRNet PJ scope; multi-card behavior is out of scope unless explicitly requested later.
- Compatibility: Defaults for any future option changes must preserve current baseline behavior.
- Compatibility: Existing dataset keys, result folders, checkpoint paths, and metric names must remain stable.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Scope Control**: PASS. The spec now authorizes a local loss-weight improvement path while keeping large network rewrites, loader changes, metric changes, and new systems out of scope.
- **Existing Contracts**: PASS. Existing script names, CLI flags, dataset keys, metric names, result directories, and checkpoint conventions remain unchanged.
- **Reuse First**: PASS. The plan reuses `test_errnet.py`, training scripts, `GradientLoss`, `MultipleLoss`, `Engine`, data preparation scripts, and existing metrics.
- **Verification Path**: PASS. Static checks, data readiness checks, smoke runs, full benchmark runs, custom image visual inspection, and delivery checklist review are defined.
- **Assumptions And Risks**: PASS. Compute, dependency, dirty worktree, custom-image ground truth, and default improvement assumptions are recorded.
- **Synchronized Artifacts**: PASS. Documentation, plan, checklist, tasks, quickstart, contracts, and optional future experiment records are included.
- **Dependency Discipline**: PASS. No new dependency is planned.
- **Completion Evidence**: PASS. Final implementation must summarize changed files, commands run, outputs, and residual risks.

## Project Structure

### Documentation (this feature)

```text
specs/001-errnet-reflection-spec/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── errnet-cli-contract.md
├── checklists/
│   ├── requirements.md
│   └── pre-implementation.md
└── tasks.md
```

### Source Code (repository root)

```text
ERRNet/
├── README_DIP26.md
├── test_errnet.py
├── train_errnet.py
├── train_errnet_unaligned.py
├── options/
│   └── errnet/
│       └── train_options.py
├── models/
│   ├── errnet_model.py
│   └── losses.py
├── datasets/
│   ├── prepare_test_data.py
│   └── prepare_train_data.py
├── util/
│   └── index.py
├── checkpoints/
├── datasets/
│   ├── raw_data/
│   └── processed_data/
└── results/

5pictures/
├── p1.jpg
├── p2.jpg
├── p3.jpg
├── p4.jpg
└── p5.jpg
```

**Structure Decision**: Use the existing ML repository layout. Planning artifacts live in `specs/001-errnet-reflection-spec/`; executable experiments continue to run inside `ERRNet/`. No new app, package, service, or parallel evaluation framework is introduced.

## Complexity Tracking

No constitution violations are planned.
