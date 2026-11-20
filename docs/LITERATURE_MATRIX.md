# LITERATURE_MATRIX — 实验阶段文献入口

依据 2026-11-10 开题报告参考文献及既有文献矩阵整理。此处为索引与研究边界，不表示已逐篇复现或重新核验全文。具体样本数、效应量、公式、图表编号须回到论文原文确认。

| 论文 | 入口 | 与本课题关系 |
|---|---|---|
| Jack et al., 2024 | https://doi.org/10.1002/alz.13859 | AD 生物学定义与临床分期区别 |
| Seidlitz et al., 2018 | https://doi.org/10.1016/j.neuron.2017.11.039 | 个体 MSN 原理；原始多模态特征不等于 T1-only |
| Young et al., 2018 | https://doi.org/10.1038/s41467-018-05892-0 | SuStaIn 原始分型分期及事件推断 |
| Aksman et al., 2021 | https://doi.org/10.1016/j.softx.2021.100811 | pySuStaIn 实现与复现 |
| Vogel et al., 2021 | https://doi.org/10.1038/s41591-021-01309-6 | Tau 病理演变异质性 |
| Kim et al., 2024 | https://doi.org/10.1038/s42003-024-05787-5 | 不同认知障碍的皮层变薄模式 |
| Baumeister et al., 2024 | https://doi.org/10.1093/brain/awae118 | 形态 SuStaIn、认知变化与跨队列验证 |
| Tandon et al., 2025 | https://doi.org/10.3390/ijms26125514 | 解剖分期与 MCI 临床进展 |
| Cai et al., 2023 | https://doi.org/10.1111/cns.14384 | 个体形态网络方法综述 |
| Xu et al., 2024 | https://doi.org/10.1093/cercor/bhad450 | MCI 个体形态网络拓扑 |
| Xiao et al., 2024 | https://doi.org/10.3389/fnins.2024.1366761 | 单受试者灰质网络与认知、萎缩 |
| Wei et al., 2025 | https://doi.org/10.1186/s13195-025-01752-4 | 个体结构协方差网络与 MCI 异质性，方法不等同 MSN |
| Gao & Hu, 2026 | https://doi.org/10.1162/NETN.a.553 | T1 MSN/MIND 的可靠性与年龄敏感性 |
| Estarellas et al., 2024 | https://doi.org/10.1093/braincomms/fcae219 | 含认知的多模态 SuStaIn 与缺失数据 |
| Berman et al., 2026 | https://papers.miccai.org/miccai-2026-sat/MLCN_2026_032.html | T1 结构相似性网络与萎缩共同输入；核查网络定义差异 |
| Mao et al., 2026 | https://doi.org/10.1016/j.neuroimage.2026.122215 | A+ AD 萎缩亚型与纵向 MMSE；注意研究人群与模型内解释/预测区别 |
| Tandon et al., 2024 | https://proceedings.mlr.press/v248/tandon24a.html | s-SuStaIn，备查效率方法，非核心路线 |

代码入口：https://github.com/ucl-pond/pySuStaIn

## 研究边界与阅读优先级

- E1：先读 Young、Aksman 与官方示例，核实事件定义、PVD、交叉验证及新受试者推断方式。
- E2：先读 Seidlitz、Cai、Gao & Hu，核实 T1-only 特征集合、相似度和网络可靠性；结合 Xu、Xiao、Wei 辨析不同个体网络定义。
- E3：重点比较 Estarellas 和 Berman。认知输入和网络输入分别已有先例，不能将特征拼接本身称为新算法。
- E4：重点读 Baumeister、Kim、Mao、Tandon 2025。纵向关联与样本外预测、外部验证分别需要不同证据；Mao 预后分析的模型内比较不能直接等同留出测试。
- 本研究拟贡献：特定 T1-MSN 的有效增量、共同队列 M1–M4 对照、联合异常模式以及后续认知观测验证。效果待实测；阴性结果同样报告。
- 若后续确有算法原创性硬性要求，与导师确认后另立可消融模块，不自行扩大任务。

## 精读记录模板

论文与 DOI / 阅读日期及状态 / 实际数据和纳排 / 特征与预处理 / 模型及参数 / 结局时点 / 数据划分及泄漏检查 / 真实结果及图表页码 / 局限 / 对本研究的启示与区别 / 官方代码版本与许可。

引用正式文献前核对元数据和原文；未经授权不提交 PDF。提交报告的部分正文引文编号与文末表存在错位风险，后续撰写论文时以 DOI 和正式出版信息重新核对，不将其当作实验参数依据。
