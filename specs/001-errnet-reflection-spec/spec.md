# Feature Specification: ERRNet 单图反射去除课程实验规格

**Feature Branch**: `001-errnet-reflection-spec`

**Created**: 2026-05-24

**Status**: Approved

**Input**: User description: "根据 /inspire/hdd/global_user/yanjunchi-24040/dyh/数字图像处理/DIP26_ERRNet_实验指导.md 创建功能规格说明。请生成一份清晰的规格说明，包括：目标、非目标、假设、边界情况，以及可测试的验收标准。"

## Scope *(mandatory)*

**Goal**: 将实验指导转化为一份可用于后续计划、任务拆分和验收的 ERRNet 单图反射去除课程项目规格。

**Background**: 当前实验指导包含环境、数据、baseline、改进算法、评价指标和交付要求，但需要整理成边界清晰、可验证、便于后续实施的规格说明。

**In Scope**: 为 DIP26 ERRNet 课程项目定义可规划的功能规格，覆盖环境和数据准备、baseline 训练与测试、指定 benchmark 与自采图像评估、改进算法实验、结果记录、论文/PPT 所需证据整理和交付清单。改进算法允许在现有 ERRNet 训练路径上做最小、局部、默认兼容的损失权重实验。

**Out of Scope**: 本规格不进行大范围模型架构重写，不新增并行训练/评估系统，不新增数据集下载源，不提交课程论文、模型权重或 PPT，不改变课程截止时间、提交邮箱和评分标准。除已授权的局部损失权重实验外，其他网络结构、数据 loader、数据增强、metric 定义、依赖变更或多卡/分布式训练适配均不在当前范围内。

**Existing Behavior to Preserve**: 保持现有 ERRNet 仓库结构、已有训练/测试入口、数据目录约定、预训练权重路径、结果输出约定、评价指标含义和课程实验指导中的提交要求不变。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 复现 ERRNet Baseline (Priority: P1)

作为课程项目学生，我需要按照实验指导准备环境、数据和预训练权重，并运行 ERRNet baseline 的测试流程，以便获得可作为后续改进对比的基准结果。

**Why this priority**: baseline 是所有改进实验、论文结果和课程验收的基础；没有 baseline，无法判断改进方法是否有效。

**Independent Test**: 使用已准备的数据和权重完成至少一个指定 benchmark 的 baseline 测试，并生成对应结果目录、输出图像和指标记录。

**Acceptance Scenarios**:

1. **Given** ERRNet 仓库、预训练权重和 processed data 已就绪，**When** 学生运行任一指定 benchmark 的 baseline 测试，**Then** 系统生成输入、输出和可记录的定量指标结果。
2. **Given** 学生使用 CPU 或 GPU 环境，**When** 学生按环境选择对应运行方式，**Then** baseline 推理流程可完成，且论文记录中说明硬件和依赖环境。

---

### User Story 2 - 评估指定数据集和自采图像 (Priority: P2)

作为课程项目学生，我需要在 CEILNet Table 2、real20、SIR2 子集、sir2_withgt 和 5 张自采图像上评估模型，以便形成覆盖合成、真实和自采场景的实验结果。

**Why this priority**: 多数据集评估决定实验充分性，并直接支撑论文中的定量表格和定性可视化分析。

**Independent Test**: 对每个指定 benchmark 记录 PSNR、SSIM、NCC、LMSE；对无 ground truth 的自采图像记录定性输出，并说明无法计算全参考指标的原因。

**Acceptance Scenarios**:

1. **Given** 指定 benchmark 已处理为可测试数据，**When** 学生对每个 benchmark 运行评估，**Then** 每个数据集都有方法输出、指标记录和可追溯的实验设置。
2. **Given** 自采 5 张反射图像没有无反射参考图像，**When** 学生报告自采图像结果，**Then** 报告以定性可视化为主，并明确说明不能计算全参考指标的限制。

---

### User Story 3 - 设计并验证改进算法 (Priority: P3)

作为课程项目学生，我需要在 baseline 基础上实现一个改进算法，并在相同或明确说明差异的数据、指标和实验设置下进行对比，以便证明改进是否有效。

**Why this priority**: 改进算法完成度是课程项目评分的核心部分，但应建立在可复现 baseline 和评估流程之上。

**Independent Test**: 改进方法可完成推理或训练后推理，并能与 baseline 在至少一组指定数据和自采图像上进行定性、定量或合理说明的对比。

**Acceptance Scenarios**:

1. **Given** baseline 结果已经记录，**When** 学生运行改进方法评估，**Then** 论文可展示同一数据集上的 baseline 与改进方法对比。
2. **Given** 当前规格仅授权局部损失权重实验，**When** 改进方法需要改变网络结构、数据 loader、数据增强、metric 或后处理，**Then** 必须先更新规格、计划和任务后再实施。

---

### User Story 4 - 完成课程交付材料 (Priority: P4)

作为课程项目小组，我需要整理论文、代码仓库链接、模型权重链接和项目汇报材料，以便按课程要求完成提交。

**Why this priority**: 课程验收依赖完整交付物和可复现实验记录。

**Independent Test**: 使用提交清单检查论文、代码链接、权重链接、汇报材料、成员贡献和提交邮件信息是否齐全。

**Acceptance Scenarios**:

1. **Given** 实验结果和分析已经完成，**When** 小组准备最终提交，**Then** 交付清单能追踪论文所需的背景、方法、实验、样例分析、结论和成员贡献证据。
2. **Given** 截止时间为 2026-06-16 17:00，**When** 小组提交课程论文，**Then** 邮件主题、收件人和附件内容符合实验指导要求。

### Edge Cases

- 数据目录或预训练权重缺失时，规格要求先验证数据准备状态，并在实验记录中标明缺失项和处理结果。
- Pascal VOC 实际 processed 数量与 PPT 中数量不一致时，实验报告以当前仓库脚本输出为准，并说明差异。
- 自采图像没有 ground truth 时，只做定性分析；若要报告 PSNR、SSIM、NCC、LMSE，必须额外准备参考图像或合成有真值的数据。
- GPU 显存不足时，允许降低输入尺寸、减小 batch size 或使用 CPU 推理，但必须记录性能和时间影响。
- 复现实验指标与 README 参考指标不同步时，以本组实际运行结果为准，并记录依赖版本、硬件、数据处理和随机性等可能原因。
- 外部开源数据集被用于训练或测试时，必须记录来源、使用原因和使用方式，且不得替代课程指定数据集评估。
- 指标计算出现 NaN、inf、尺寸不一致或缺少 ground truth 时，必须记录该样本或数据集的 metric 状态、裁剪/对齐策略和不可计算原因。
- 若后续需要修改数据 loader、resize/crop/augmentation 或 metric 实现，必须先补充对应规格、计划和 smoke test；当前默认方案不修改这些路径。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 规格 MUST 明确课程实验目标：理解单图反射去除任务、复现 ERRNet baseline、设计改进算法、完成指定数据和自采图像评估，并形成课程交付材料。
- **FR-002**: 规格 MUST 要求学生记录实验环境，包括操作系统、Python 版本、深度学习依赖版本、CUDA 或 CPU 环境、GPU 型号和代码 commit id。
- **FR-003**: 规格 MUST 要求验证数据和权重准备状态，包括预训练权重、raw data、processed data、指定 benchmark 和 5 张自采图像。
- **FR-004**: 规格 MUST 要求 baseline 在至少一个指定 benchmark 上可运行，并逐步扩展到 CEILNet Table 2、real20、objects、postcard、wild 和 sir2_withgt。
- **FR-005**: 规格 MUST 要求对有 ground truth 的测试集报告 PSNR、SSIM、NCC 和 LMSE，并保留对应方法输出或结果路径。
- **FR-006**: 规格 MUST 要求对 5 张自采图像输出可视化结果；若没有 ground truth，报告 MUST 明确标注该部分为定性分析。
- **FR-007**: 规格 MUST 要求改进算法与 baseline 使用可比较的数据划分、评价指标和实验记录；任何差异 MUST 在论文中说明。
- **FR-008**: 规格 MUST 要求改进方法的范围保持局部化，优先复用现有 ERRNet 模块、训练流程、测试入口、数据准备脚本和评价指标。
- **FR-009**: 规格 MUST 要求避免无关重构和不必要依赖；新增依赖、额外数据集或显著计算开销 MUST 有明确原因和验证影响说明。
- **FR-010**: 规格 MUST 要求记录训练和评估过程，包括实验名、数据集、初始权重、epoch、batch size、学习率、loss 设置和训练时间。
- **FR-011**: 规格 MUST 要求实验记录和交付清单映射论文所需证据，包括背景综述、baseline 方法、改进方法、实验设置、定量结果、定性结果、失败案例、局限性、结论和成员贡献。
- **FR-012**: 规格 MUST 要求最终交付清单追踪课程论文、可运行代码仓库链接、模型权重下载链接、项目汇报 PPT、指定时间和邮件格式的完成状态或缺失原因；本规格不负责实际撰写、上传或发送这些外部交付物。
- **FR-013**: 规格 MUST 要求评估记录说明 metric 输入语义，包括输出/目标图像对齐方式、裁剪策略、像素范围、ground truth 条件、mask/有效像素定义、NaN/inf 处理和不可计算原因。
- **FR-014**: 规格 MUST 要求任何改进方法的新增参数默认保持 baseline 行为，并验证旧 checkpoint 仍可加载和推理。
- **FR-015**: 规格 MUST 要求改进方法在 5 张自采图像上生成输出并与 baseline 做定性对比；若无法运行，必须记录阻塞原因和剩余风险。

### Key Entities *(include if feature involves data)*

- **实验项目**: 围绕 ERRNet 单图反射去除的课程项目，包含 baseline 复现、改进算法、评估和交付材料。
- **数据集**: 包括 Pascal VOC、Berkeley real89、CEILNet Table 2、real20、SIR2 Objects、SIR2 Postcard、SIR2 Wild、sir2_withgt 和 5 张自采图像。
- **模型方法**: 包括 ERRNet baseline、aligned training 结果、unaligned finetuning 结果和学生设计的改进方法。
- **评价结果**: 包括 PSNR、SSIM、NCC、LMSE、输入图像、输出图像、ground truth、局部放大图、误差图和失败案例说明。
- **交付物**: 包括课程论文、代码仓库链接、模型权重链接、汇报 PPT、可选课堂展示报告和小组成员贡献说明。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 学生能够在 30 分钟内根据规格确认本地环境、权重、raw data、processed data 和自采图像是否满足实验前置条件。
- **SC-002**: 至少 6 个指定 benchmark 中的评估结果能够形成完整记录，每条记录包含方法名、数据集名、4 个指标或不可计算原因。
- **SC-003**: 5 张自采图像均有输入图、baseline 输出和改进方法输出的定性对比材料；若缺少改进方法输出，必须记录原因和剩余风险。
- **SC-004**: 改进方法与 baseline 至少在 1 个指定 benchmark 和自采图像上完成可解释对比，且对比结论能追溯到实验记录。
- **SC-005**: 交付清单或论文证据映射覆盖建议结构中的 5 个主要部分，并索引至少 1 个成功案例、1 个失败案例和每位成员贡献说明。
- **SC-006**: 最终提交清单中课程论文、代码仓库链接、模型权重链接和项目汇报 PPT 均被标记为完成或给出明确缺失原因。

## Assumptions

- 项目类型为 2D 图像复原 ML 仓库，主要入口为 ERRNet 的数据准备、训练和测试流程。
- 现有 ERRNet 仓库位于 `ERRNet` 目录，并保留课程指导中描述的分支、数据目录、权重路径和结果输出约定。
- 当前规格授权后续实现一个默认兼容、局部化的结构损失权重实验；若改为网络结构、数据 loader、数据增强或后处理方向，需要先更新规格和计划。
- 自采 5 张图片默认没有 ground truth，因此默认只用于定性分析；定量评价需要额外参考图像。
- 默认验证边界是 CPU import/CPU 推理和单卡 CUDA 环境；多卡或分布式运行只记录现有行为，不作为本 ERRNet PJ 规格的验收要求。
- 参考指标用于对照，不作为强制精确复现阈值；论文应报告本组实际运行结果。
- 主要风险包括环境依赖差异、GPU 资源不足、数据路径不一致、训练耗时较长、随机性导致指标波动，以及自采图像无法计算全参考指标。
## Verification Plan *(mandatory)*

- 审阅规格，确认所有用户故事均有独立测试方式和验收场景。
- 检查功能需求，确认每条需求可通过实验记录、输出文件、结果表、论文内容或提交清单验证。
- 检查成功标准，确认每条标准包含可计数、可观察或可明确判定的结果。
- 在后续计划阶段，将本规格映射为最小化实施任务：环境核验、baseline 评估、改进方法、结果记录、论文/交付清单。
- 若进入实现阶段，使用实验指导中的指定命令和结果路径验证 baseline、custom 图像和改进方法输出。

## Artifact Synchronization *(mandatory)*

- **Tests**: Update required - 后续任务应包含 baseline 评估、指标记录和自采图像可视化检查；本规格阶段仅生成质量清单。
- **Documentation**: Update required - 本规格来源于 `DIP26_ERRNet_实验指导.md`，后续计划和任务应保持与该指导一致。
- **Configuration/Scripts**: Update if required - 局部结构损失实验可修改训练 options 和损失组合；默认行为、旧命令和旧 checkpoint 必须保持兼容。训练/测试入口、数据准备脚本、metric 实现和 loader 默认不变。
- **Dependencies**: No new dependencies - 当前规格不要求新增依赖；任何后续新增依赖必须说明原因、收益和验证影响。
