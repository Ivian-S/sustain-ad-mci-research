# SuStaIn AD/MCI Research

## 研究概况

课题：**基于 SuStaIn 的 AD/MCI 脑结构网络与认知功能联合演变建模**

本项目服务于计算机技术硕士学位论文。用户已确认导师同意 2026-11-10 版开题报告；当前进入实验准备与执行阶段。目标是稳妥、可复现地完成研究，而非追求不必要的算法复杂度。

以获授权的 ADNI 临床 CU/MCI 数据为主，结合 T1 MRI/FreeSurfer 脑区形态、个体形态相似性网络（MSN）及基线认知指标，使用 Z-score SuStaIn 推断潜在亚型、阶段和异常事件顺序，并通过后续认知随访验证。

## 当前进度

- 已完成：选题论证、导师同意开题报告、V1–V4 数据可行性审计。
- 当前任务：E0，精确匹配实体影像、FreeSurfer 和临床访视，并确认 QC 后的有效队列。
- 未完成：正式 M1–M4 训练、MSN 构建、纵向统计验证。尚无模型性能或临床发现。

## 文档入口

| 文档 | 用途 |
|---|---|
| [AI_HANDOFF](docs/AI_HANDOFF.md) | 新 AI 首读；项目状态与协作规范 |
| [EXPERIMENT_PLAN](docs/EXPERIMENT_PLAN.md) | 实验方案、任务与验收 |
| [DATA_AUDIT_SUMMARY](docs/DATA_AUDIT_SUMMARY.md) | 原始 V1–V4 审计证据，历史快照 |
| [EXPERIMENT_LOG](docs/EXPERIMENT_LOG.md) | 实际运行与决策记录 |
| [LITERATURE_MATRIX](docs/LITERATURE_MATRIX.md) | 相关研究与创新边界 |

## 实验路线

E0 数据核验 → E1 pySuStaIn 示例与 M1 基线 → E2 个体 MSN → E3 M2–M4 受控建模 → E4 纵向关联、消融、稳定性验证。

预测与 Aβ 阳性亚组属于条件性扩展，不是必须取得的结果。

## 项目目录

`scripts/`：审计及执行脚本；`src/`、`configs/`：后续模型与配置的建议存放位置（以实际仓库为准）；`docs/`：研究文档。`data/`、`results/` 等受控目录仅在本地服务器使用。

## 复现与数据安全

目前没有经过验证的统一安装或训练命令；待 E1 验证环境后，在实验日志中记录准确命令、依赖版本和代码提交号。禁止上传原始影像、临床明细、受试者索引、凭据及未审查的衍生产物。公开代码及汇总结果须符合数据使用协议与实验室要求。不要把 `.gitignore` 当作数据安全审查的替代品。
