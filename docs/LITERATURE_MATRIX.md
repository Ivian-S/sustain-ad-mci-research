# LITERATURE_MATRIX — 文献索引与证据矩阵

> 目标：区分**文献实际结论**、**我们的解释**和**待验证的创新设想**。  
> 本表初始条目只代表阅读优先级，**不表示已经完整精读或核验每项研究结论**。

## 1. 核心文献候选

| ID | 年份/作者 | 主题 | 入口 | 阅读状态 | 重点待核实 |
| --- | --- | --- | --- | --- | --- |
| P01 | Young et al., 2018 | SuStaIn 原始方法 | [Nature Communications](https://www.nature.com/articles/s41467-018-05892-0) | 待读 | 模型假设、事件序列、分型/分期、验证方式 |
| P02 | Estarellas et al., 2024 | 缺失数据与多模态 SuStaIn | [DOI](https://doi.org/10.1093/braincomms/fcae219) | 待读 | 融合模态、认知变量是否进入建模、信息泄漏防控 |
| P03 | Tandon et al., 2024 | s-SuStaIn 与高效分期 | [PMLR](https://proceedings.mlr.press/v248/tandon24a.html) | 待读 | 核心算法、复杂度、预测任务及可复现性 |
| P04 | 2025，待核对作者 | 高维解剖分期与认知轨迹 | [文章页面](https://www.mdpi.com/1422-0067/26/12/5514) | 待读 | 与拟议预测方法的重合之处 |
| P05 | Berman et al., 2026（待核对著录） | 脑网络异常与脑萎缩的 SuStaIn 建模 | [会议论文页面](https://papers.miccai.org/miccai-2026-sat/MLCN_2026_032.html) | 待读 | SSN 网络定义、事件顺序、纵向验证和局限 |

注：作者、题目、年份、样本量、指标与 DOI 等，精读时以正式论文全文核验后更新；不要直接将本表当作参考文献终稿。

## 2. 每篇论文统一记录模板

### Px — [题目待填]

- **完整引文 / DOI / 发表版本**：
- **文献状态**：未读 / 略读 / 精读 / 已复现
- **研究问题 / 关键假设**：
- **数据来源、受试者数量和纳排标准**：
- **输入模态与具体特征**：
- **是否使用纵向数据？如何使用？**：
- **模型方法及明确的新贡献**：
- **对照算法与评价指标**：
- **结果（原文数值、表格/图号、置信区间）**：
- **作者承认的限制与我们的额外质疑**：
- **对我们选题的启示 / 潜在重合**：
- **已核验证据位置（页码/图/表/代码行）**：
- **复现仓库 / 许可 / 版本（如有）**：
- **阅读日期 / 阅读者**：

## 3. 对选题的竞争性检查

对于每个拟创新点，务必回答：

1. 是否已有工作使用相同的数据模态、亚型/阶段特征和认知预测目标？
2. 与“对 SuStaIn 硬标签做回归”相比，拟议方法具有何种可量化的方法差异？
3. 是否存在独立数据、患者级划分或外部验证？是否有使用认知量表参与分型后再预测相同评分的风险？
4. 研究结论是横断面事件次序、真实纵向关联，还是因果机制？不可混用。

## 4. 检索与引用规范

优先使用论文出版社页面、PubMed、会议/期刊官网、作者正式预印本和官方代码仓库。记录检索日期、搜索式和版本；参考文献最终统一采用学校要求格式。论文 PDF 可以保存在本地受控目录，但不要未经授权提交到 GitHub。

<!-- BEGIN SUSTAIN_HANDOFF:LITERATURE_MATRIX -->
## 2026-10-30 更新：直接竞争研究与创新边界

> 下列论文是真实可查询的先例。其数据、模型与结论不能被写作本课题的原创成果。详细方法比较见 `docs/TOPIC_DECISION.md`，原始选题论证见 `docs/SuStaIn_AD_MCI_Research_Justification_v1.1.md`。

| 论文 | 文献及来源 | 与课题的直接关系 | 必须避免的重复/我们的拟议切入 |
|---|---|---|---|
| Young et al. 2018 | [Nature Communications, SuStaIn 原始论文](https://www.nature.com/articles/s41467-018-05892-0) | 提出亚型/阶段联合推断与潜在事件顺序 | 使用 pySuStaIn 复现，不能宣称提出 SuStaIn |
| Estarellas et al. 2024 | [Brain Communications, fcae219](https://pmc.ncbi.nlm.nih.gov/articles/PMC11259979/) | ADNI 789 人，MRI＋PET＋CSF＋认知联合 SuStaIn，含 Cognitive 亚型 | **认知加入 SuStaIn 已有人做**；我们拟在 MSN 网络增量、受控对照和未来结果验证上区分 |
| Baumeister et al. 2024 | [Brain, awae118](https://academic.oup.com/brain/article/147/7/2400/7657064) | MRI SuStaIn、早期人群、纵向认知和跨队列泛化 | **纵向认知外部验证已存在**；不能宣称首创 |
| Kim et al. 2024 | [Communications Biology](https://www.nature.com/articles/s42003-024-05787-5) | 皮层变薄模式与认知相关性 | 不能仅以脑形态＋认知相关证明独创新意 |
| Tandon et al. 2025 | [IJMS, 118 ROI／MCI 进展](https://pmc.ncbi.nlm.nih.gov/articles/PMC12193007/) | 解剖学分期与 MCI 进展风险，基线较强 | **MCI 风险预测非首创** |
| Berman et al. 2026 | [MICCAI MLCN, Network Alterations Precede Atrophy](https://papers.miccai.org/miccai-2026-sat/MLCN_2026_032.html) | ADNI 1,699 人，T1 结构网络指标与萎缩指标共同输入 SuStaIn | **脑网络加入 SuStaIn 已有人做**；强调脑网络＋基线认知的增量/交互和独立纵向结果，而非简单重复网络先于萎缩 |
| Mao et al. 2026 | [NeuroImage 340:122215](https://doi.org/10.1016/j.neuroimage.2026.122215) | A+ AD 484 人、17 ROI、四亚型，226 人纵向 MMSE；45 人的预后模型比较属模型内解释度 | 与较晚临床 AD 人群区分，做早期 CU/MCI 与网络联合；预测时使用严格留出测试 |
| Seidlitz et al. 2018 | [Neuron, Morphometric Similarity Networks](https://doi.org/10.1016/j.neuron.2017.11.039) | 个体 MRI 多形态特征构建 MSN 的方法基础 | MSN 不是新发明，需明确数学实现、网络拓扑指标和可靠性 |
| Aksman et al. 2021 | [SoftwareX pySuStaIn 100811](https://doi.org/10.1016/j.softx.2021.100811) | 可复现官方 Python SuStaIn 工具 | 优先复现官方教程及 Z-score SuStaIn |

**本课题创新强度初评：**直接拼接脑形态、网络、认知属于有限创新的方法组合。通过 M1（形态）、M2（形态＋网络）、M3（形态＋认知）、M4（三者）在同一受试者子集上比较，并用独立未来认知变化与稳健性实验证实增量价值，才可形成可检验的主要研究贡献。是否满足学院算法创新要求仍待导师确认。不要预设 M4 性能一定提高。
<!-- END SUSTAIN_HANDOFF:LITERATURE_MATRIX -->
