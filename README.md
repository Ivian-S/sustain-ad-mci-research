# SuStaIn × AD/MCI Research

> 基于 SuStaIn 的阿尔茨海默病（AD）早期脑结构/网络异常及认知变化研究工作区。
>
> Research workspace for SuStaIn-based AD/MCI subtype–stage modeling and longitudinal cognitive outcome analysis.

**当前状态：开题前的文献调研与研究方案设计；尚未确定最终论文题目、数据条件或算法创新。**

## 项目目的

本仓库用于持续整理研究思路、文献证据、技术决策、代码和可复现实验记录。导师提出的核心方向是：围绕临床前期 AD 和轻度认知障碍（MCI）人群，探索脑结构/网络异常模式与临床认知变化之间的关系，并评估其在早期风险识别中的价值。

注意：**SuStaIn 推断的潜在疾病阶段不等于真实经过的时间**；如果要研究未来认知下降或事件先后，需要纵向随访数据。MCI 也不等同于生物学定义的 AD。

## 研究记录入口

| 文件 | 用途 |
| --- | --- |
| [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) | 长期项目背景、目标、已确定事实、待确认事项、决策日志 |
| [LITERATURE_MATRIX.md](LITERATURE_MATRIX.md) | 关键文献索引、阅读证据、方法对比、潜在研究空白 |
| [EXPERIMENT_LOG.md](EXPERIMENT_LOG.md) | 实验计划与可复现实验记录；尚未开展的实验不得填写成既成结果 |

## 当前拟议研究链条（非最终方案）

1. 对结构 MRI 形态学指标进行质量控制和标准化。
2. 使用 SuStaIn 进行脑异常模式的亚型与潜在阶段推断。
3. **在数据允许时**，评估脑网络指标提供的增量价值。
4. **在存在有效纵向随访时**，研究亚型/阶段概率与认知下降的预测关系。
5. 与合理基线比较，检查稳定性、数据泄漏及跨队列泛化。

研究内容、模型与评价指标均须依据文献调研、数据可用性及导师意见逐步确定。

## 文件与数据管理

- Git 跟踪：代码、环境配置样例、公开文献的引用信息、脱敏且允许发布的汇总结果、研究笔记。
- **不上传**：原始 MRI/PET/临床记录、患者级表格、个人身份信息、访问凭据、受限制数据集、未经授权公开的论文 PDF。
- 数据放在被 `.gitignore` 排除的目录，例如 `data/`、`datasets/`；这只是防误传的第一层保护，提交前仍须人工检查。
- 研究决策写入 `PROJECT_CONTEXT.md`，文献证据写入 `LITERATURE_MATRIX.md`，实验事实写入 `EXPERIMENT_LOG.md`。
- 尚未选定代码许可证；在取得导师/实验室许可之前，仓库建议保持 **Private**。

## 使用原则

所有算法结果必须有对应的数据版本、运行参数和代码版本；研究假设与已经得到的实验结果要明确区分。不要将 AI 生成的文字、文献摘要或实验结论未经核查直接作为学术事实。

<!-- BEGIN SUSTAIN_HANDOFF:README_STATUS -->
## 研究现状（2026-10-30 更新）

**暂定硕士论文题目：**《基于 SuStaIn 的 AD/MCI 脑结构网络与认知功能联合演变建模研究》（尚待导师确认）。目标是使用 T1/FreeSurfer 形态特征和个体 MSN 网络特征，研究 SuStaIn 亚型/阶段与基线、后续认知量表的联系。项目优先追求可复现、工作量可控、满足毕业要求的研究成果。

**项目阶段：**已完成 ADNI 的 V1–V4 初步数据审计与研究选题论证，正在准备开题报告。**尚未完成**真实 SuStaIn/网络模型训练、影像 QC 后的最终队列确认或任何可声称为实验结果的模型性能。

### 文档导航（新 AI 建议按此顺序阅读）

1. [`docs/AI_HANDOFF.md`](docs/AI_HANDOFF.md)：跨会话 AI 最重要的项目事实和待办入口。
2. [`docs/TOPIC_DECISION.md`](docs/TOPIC_DECISION.md)：暂定题目、备选题、创新边界、与相近论文对比。
3. [`docs/DATA_AUDIT_SUMMARY.md`](docs/DATA_AUDIT_SUMMARY.md)：四轮 ADNI 数据审计结果、统计口径与局限。
4. [`docs/PROPOSAL_BRIEF.md`](docs/PROPOSAL_BRIEF.md)：下一阶段开题报告研究目标、技术路线、实验计划。
5. [`docs/PROJECT_CONTEXT.md`](docs/PROJECT_CONTEXT.md)、[`docs/LITERATURE_MATRIX.md`](docs/LITERATURE_MATRIX.md)、[`docs/EXPERIMENT_LOG.md`](docs/EXPERIMENT_LOG.md)：持续维护的项目状态、文献矩阵及日志。
6. [`docs/SuStaIn_AD_MCI_Research_Justification_v1.1.md`](docs/SuStaIn_AD_MCI_Research_Justification_v1.1.md)：此前详细选题论证。

### 当前数据与开发环境

- Linux GPU 服务器，4×RTX 3090、48 CPU 线程；`scripts/` 当前存放数据审计脚本，`src/`、`configs/` 的正式模型尚待实现。
- 临床数据来自 **ADNI**，本地 `data/all.xlsx`（**受访问协议约束，不能提交 Git**）；MRI/PET 影像在独立的 SMB 共享，通过只读挂载访问。私有路径单独记录于 Git 忽略的 `docs/LOCAL_ENV_PRIVATE.md`。
- V3 实际日期匹配候选：T1 元数据＋诊断＋认知 **1,830 人**，其中 MCI **765**、CU **788**；V4 不完整磁盘扫描在 `processed_data` 发现 **821 个 FreeSurfer 成套 `.stats` 目录、444 个不同 PTID**，尚需具体的 MRI 访视匹配与影像质量复核。
- 建议 M1 形态、M2 形态＋MSN 网络、M3 形态＋基线认知、M4 三者联合 SuStaIn，对独立后续认知变化进行纵向验证；切勿将 SuStaIn 横断面推断事件解释成真实因果时间。

### 下一步

请先查看 [`docs/PROPOSAL_BRIEF.md`](docs/PROPOSAL_BRIEF.md) 并获取学校开题模板；与导师确认 T1/FreeSurfer 形态相似性网络能否满足“脑结构网络”定义、以及算法创新要求。实验上优先小样本定向匹配与影像 QC，随后复现官方 [pySuStaIn](https://github.com/ucl-pond/pySuStaIn)；不要为增加技术复杂度而盲目加入 DTI/多模态深度学习。

**安全提醒：**不要提交 `data/`、原始影像、MRI 个人级索引、凭据、`results/data_audit/` 或 `docs/LOCAL_ENV_PRIVATE.md`。如准备公开仓库，请再次人工检查 Git 已暂存内容和历史提交记录。
<!-- END SUSTAIN_HANDOFF:README_STATUS -->
