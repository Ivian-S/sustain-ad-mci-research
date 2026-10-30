# SuStaIn 与 AD/MCI 早期进展预测研究选题论证

**版本：** v1.1 ｜ **日期：** 2026-10-27 ｜ **用途：** 硕士开题前选题论证

> **核心立场** 以导师要求的“SuStaIn＋脑结构网络特征＋认知量表”为必需闭环，优先选择可在现有 ADNI T1 影像基础上复现、可扩展、可按数据条件降级的方案。概率耦合与复杂网络模型不是毕业的前置条件。

适用阶段：计算机技术硕士学位论文开题前选题论证 / 与导师讨论。
研究范围：临床前期 AD（须有生物标志物证据）、AD 相关 MCI；无该证据时使用“AD 风险相关认知障碍”或“MCI”表述。
文献核验时间：2026 年 10 月 27 日；本文件是**重点文献导向的选题论证**，不等于系统综述或已完成实验报告。
证据标识：下文 [序号] 可在文末查阅原文。实验性能、有效样本量和创新效果均尚未经过本课题实测。
# 0. 执行摘要
> **选题判断** **可做，但不建议使用“SuStaIn 分型 + 认知相关性分析”作为唯一创新。** 已有研究做过 MRI 分型分期、与认知下降的关联、MCI 转化预测，以及脑结构相似性网络和影像联合 SuStaIn [3–9]。

## 0.1 推荐题目与备选题目
| 优先级 | 拟定题目 | 适用条件／评价 |
| --- | --- | --- |
| A · 首选 | 基于 SuStaIn 的 AD/MCI 脑结构网络异常分型与认知功能变化研究 | T1 与认知量表配对即可启动；纵向数据充分则拓展为变化预测；更符合尽快毕业的目标 |
| B · 强化预测 | 融合结构相似性网络与 SuStaIn 的 MCI 认知功能下降预测研究 | 需 T1、基线与后续认知量表、足够纵向 MCI 样本；更聚焦预测 |
| C · 高难度 | 融合 DTI 结构连接与 SuStaIn 的 AD/MCI 脑网络损伤演变及认知预测研究 | 需可配对 DTI/T1、梯度信息、白质纤维追踪和纵向认知；不宜先做 |
| D · 应急降级 | 基于 SuStaIn 的 MCI 脑形态异常分期及认知功能预测研究 | 仅需形态 ROI 与量表，但不直接满足导师的“脑结构网络”关键词，须事先征得同意 |

## 0.1A 题目难度、创新度与可行性评分（毕业优先）
这里的 1—5 分是项目规划用的主观相对评分，不是论文质量或真实成功概率；难度分越高越难，创新度越高表示相对现有文献可拓展空间越大，可行性越高表示在已知数据条件下越容易完成。可行性以 T1_nii 等确有有效影像及可获取认知表为前提，尚未审计真实受试者交集。
| 方案 | 实现难度 | 预期创新度 | 条件可行性 | 决策建议 |
| --- | --- | --- | --- | --- |
| A 网络分型＋认知变化 | 3.5/5 | 2/5 | 4/5 | 首选；完成必做闭环后再增量改进 |
| B 网络＋纵向预测 | 4/5 | 3/5 | 3/5 | 纵向量表有效样本足够时升级 |
| C DTI 连接网络 | 5/5 | 3/5 | 2/5 | 仅在 DTI 完整且导师明确要求时进行 |
| D 仅 T1 形态分期 | 2/5 | 1.5/5 | 4.5/5 | 技术保底，需导师允许不强调网络 |
### A 的最小工作量与数据要求
需要：基线 T1 NIfTI、可生成个体结构相似性网络的灰质图、脑区体积或厚度、认知量表与临床分组、正常对照用于参照标准化。必做实验为 T1 形态 vs T1 形态＋网络特征的 SuStaIn 比较、亚型—阶段图、基线量表关联、患者级交叉验证和稳健性分析；如果存在纵向量表，再做后续认知下降预测。核心风险是网络构建成本及与已有 Berman 2026 工作的重复，因此必须把认知结局和特征贡献验证写清楚。
### B 的价值与门槛
在 A 基础上增加真实随访时间与预测终点（例如 12／24 月 ADAS13 或 CDR-SB），比较人口学＋基线认知、原始 T1 特征、SSN 特征、SuStaIn 硬分期与可选后验统计量。主要增量是规范的受试者级留出预测，而不是将预测改进写成既成事实。若纵向人数太少，不能硬写“认知轨迹预测”。
### C 为什么暂不推荐
DTI 网络是白质纤维连接组，与 T1 形态相似性网络并不等价。需要 bvec/bval、eddy/motion/畸变校正、束流追踪与跨站点一致性评估，T1/DTI/量表三者交集可能很小；并不是因为服务器显卡不足，而是处理链和有效样本风险高。
### D 的角色
若 T1 网络提取失败，可先完成传统形态 SuStaIn 与认知分析，形成可交付的基线成果。但因缺少“脑结构网络特征”，正式改题前应与导师沟通。现阶段没有理由优先退到 D。
### 选题决策
先用 A 作为与导师讨论的暂定题目，不立即把复杂概率模型写进题目。等 ADNI 影像与临床审计出有效样本漏斗后，若 MCI 具有充分的基线与纵向量表，则可升级为 B。评分应随数据事实更新。
## 0.2 三个可验证的核心研究问题（按任务优先级）
- H1（必做）：T1 脑结构相似性网络与脑区形态特征联合输入 SuStaIn 后，是否得到可复现的亚型、分期与异常事件模式？与纯形态模型的差异是否稳定？
- H2（必做）：不同亚型与阶段能否解释基线认知量表差异；有随访时，其对于未来量表的预测是否有额外价值？须控制年龄、性别、教育、基线认知和站点效应。
- H3（可选）：在纵向样本充分时，使用 SuStaIn 亚型—阶段后验概率而不是硬标签，能否改善预测稳定性或预测区间校准？任何改善都需未见受试者上的测试证据。
这些都属于研究假设；不要求全部得到正结果。A 路线可以先完成 H1＋H2，再决定是否投入 H3。
## 0.3 开题决定条件
1. 最重要：实验室是否还存有 ADNI 临床／认知 CSV（例如 ADNIMERGE、诊断汇总、ADAS/MMSE/CDR、FreeSurfer 形态统计表）？这决定我们能否把影像与临床量表配对。只需回复有／没有／尚未查到。
# 1. 医学概念与研究边界
## 1.1 AD、临床前期 AD、MCI 并非同义词
认知正常（CN/CU）指没有达到临床认知损害标准；MCI 指认知功能下降但未满足痴呆诊断标准。AD 指由特定疾病生物学过程支持的诊断。临床前期 AD 要求认知未明显受损但已存在合格的 AD 生物标志物证据，不能仅凭 MRI 萎缩、年龄或低分认知测试判定。2024 年修订标准体现了疾病生物学与临床表型的区别 [13]。
研究对象宜分层：① Aβ 阳性且临床认知正常（真正的临床前期 AD，可选）；② Aβ 阳性 MCI（优先目标）；③ 全部 MCI（更现实，但必须注明病因异质性）；④ 健康对照／适当参照人群（用于标准化和建模）。
## 1.2 三组数据的不同含义
- **脑形态（morphometry）：** 海马体积、内嗅皮层厚度、脑区灰质体积、皮层厚度。可能受颅内容积、年龄、性别、扫描协议影响。
- **结构相似性网络（SSN）：** 对同一个人的不同脑区灰质形态分布计算相似性，从而形成网络。它不直接等于白质纤维解剖连接；不能将其解释为神经纤维真实断裂 [9]。
- **纵向认知／临床结果：** MMSE（通常分数越低越差）、ADAS-Cog13 / CDR-SB（通常越高越差）、临床转化事件及随访时间。不同量表必须分开分析或明确定义变换。
SuStaIn 的“stage”是潜在疾病异常事件次序，不是以月／年为单位的真实时钟；事件的前后顺序不能单凭横断面 SuStaIn 推断证明真实时间先后 [1,6,9]。
# 2. 核心论文精读：已有工作究竟做到哪里
下列“方法与结论”依据出版商论文页面、可访问全文和会议开放论文核验；对未完整获取的方法细节保持保留。引用中的 n 为原论文研究样本，不能直接推断为本课题可用的完整纵向样本。
## 2.1 Young 等（2018）：SuStaIn 算法原点 [1]
**问题与方法：** 传统聚类忽略疾病阶段，单一进展模型忽略不同亚型。SuStaIn 联合估计受试者的病程亚型与潜在阶段，利用疾病标志物异常事件序列及其似然建模。原文对 793 名 ADNI 参与者（其中 524 为 MCI 或 AD）分析并开展 1.5T 影像复现。
**关键产出：** 每个受试者的亚型和阶段后验分布、亚型特异异常顺序、交叉验证选择亚型数、PVD 可视化。
**对我们：** 基线模型及概念必须复现。但“直接用 SuStaIn 得到多种疾病模式”已不是新贡献。尤其不能把阶段数当成等间隔真实时间。
## 2.2 Estarellas 等（2024）：多模态缺失值 SuStaIn [3]
**问题与方法：** 传统 SuStaIn 要求完整指标，限制 MRI/PET/CSF/认知的联合分析。作者改进缺失值处理，在 789 名 ADNI 受试者中使用 MRI、PET、CSF 与部分认知测试建模，识别多模态疾病亚型并分析与临床特征的关联。
**已覆盖：** “影像 + 临床行为指标联合分型”并非空白。对该论文需要重点核实哪些认知评分参与了 SuStaIn 输入，哪些用于外部结果，以免我们的评价循环验证。
**我们的差异：** 主实验坚持“基线脑影像建分型；未来未见的认知评分评估预测”，避免把同一个随访结果放进无监督模型及预测标签两边。
## 2.3 Kim（2024）与 Baumeister（2024）：纵向认知关联已有先例 [5,6]
Kim 等用 1,338 名参与者的数据研究 AD 型与血管性认知障碍的皮层变薄模式；SuStaIn 得出的亚型表现出不同的纵向认知衰退特征。Baumeister 等在 DELCODE 813 人的临床记忆门诊队列上构建萎缩亚型，分析基线认知、疾病标志物与长期临床／认知结局，并进行跨队列相关验证。
**重复风险：** “发现不同亚型的认知下降速度不同”“采用线性混合效应模型做亚型与认知关联”不能作为新算法创新。
**待突破：** 将新受试者的完整后验概率转为未来某个时点的**前瞻预测分布**，提供严格的留出测试评估、预测区间可靠性和相对合理临床基线的净增益。
## 2.4 Tandon（2024, 2025）：MCI 转化与解剖分期预测 [4,7]
2024 年 s-SuStaIn 以更大规模脑标志物进行快速分型分期，研究 MCI 进展风险；2025 年作者使用 118 个解剖特征，在 504 名认知正常者与 346 名 AD 患者上建立模型，再于 808 名 MCI 受试者中研究临床进展。论文报告的 Cox 模型 C-index 为 0.73，对比传统模型的 0.62。
**重复风险：** MCI 转化风险与阶段显著相关已经被证明。我们不能把该研究的 0.73 当作本课题目标值，也不能在不同数据划分或结局定义下直接对比数字。
**可做差异：** 关注指定时间点的连续认知值 + 校准区间，必要时把转化作为次要结局；尽可能复现与 2025 工作相近的风险基线。
## 2.5 Berman 等（2026）：网络改变先于萎缩的 SuStaIn 研究 [9]
**问题与方法：** 使用 1,699 名 ADNI 参与者的 T1 MRI，构建个体脑结构相似性网络；把网络全局／局部拓扑量与脑区体积组合用于 SuStaIn。论文报告部分 Typical 亚型中网络相关异常事件排在海马或杏仁核萎缩事件之前。
**重要解释：** 这是模型推断的异常事件顺序，不是独立纵向实验确认“网络损伤在真实时间上提前发生”。结构相似性网络与扩散 MRI 白质连接组并不相同；网络指标可能非单调，违反简单 z-score 事件顺序的部分前提。
**我们的差异：** 不以复现先后顺序为主要创新，而检验网络指标对 24 月认知结局的**额外预测信息**，以及事件排序与临床预测增益是否在抽样扰动下稳定。若无 T1 原始影像，该支线直接舍弃。
## 2.6 Mao 等（2026）：已核对上传的 NeuroImage 全文 [10]
研究对象与数据：来自北京协和医院的 484 名经 Aβ PET 或 CSF 支持的 Aβ 阳性临床 AD 患者，另有 384 名独立认知正常对照；基线 MMSE 中位数为 15，不能当作“临床前期 AD/MCI”队列。患者影像为 T1 MRI，预处理分割后汇总成 17 个复合 ROI，进行 ICV 归一化和按对照年龄组的 Z-score 标准化（正文第 2—4 页）。
SuStaIn 方法：仅将基线 MRI 的 17 个形态 Z-score 输入模型，采用异常阈值 1/2/3、50 次随机起点、100000 次 MCMC、1—5 个亚型的五折交叉验证，以 CVIC 和留折似然决定亚型数；所得四个亚型分别为 Typical、Parietal-predominant、Limbic-predominant 与 Hippocampal-sparing。Bhattacharyya 稳定性系数约 0.93（正文第 3—5 页）。
样本数量必须分清：484 为 SuStaIn 全部建模患者；226 名患者的 741 次 MMSE 记录进入纵向认知分析；45 名患者的 134 次 MMSE 记录构成 CSF／血浆／海马体积等预后模型的共同完整案例比较。不要把“484 人”直接写成预测验证样本量（正文第 4、8 页）。
关键结果：SuStaIn stage 与基线 MMSE 负相关，Spearman ρ=-0.56。Parietal-predominant 亚型 MMSE 下降较快；亚型与时间交互 p=0.042，相较 Hippocampal-sparing 的斜率差为 -1.14（Tukey 调整后 p=0.021）。ADL 的亚型×时间交互不显著（p=0.27）。45 人的模型比较中 SuStaIn 取得最高模型内 marginal R²=0.579，但作者明确承认这不是独立测试集上的预测优势证据（正文第 8—9 页）。
与本课题的差异：本文没有把“新患者预测的患者级留出泛化”作为核心验证，也没有将 T1 个体结构相似性网络引入 SuStaIn；其研究对象主要是临床症状已明显的 Aβ+ AD，而我们优先定位 ADNI 的 MCI／认知较早期子群。我们需要真正做出 T1 网络特征输入、形态 vs 网络对照、认知量表关联，有纵向数据时做留出预测，而不是重复“分出四种亚型”。
图表阅读提示：第 5 页图 1 为亚型事件序列 PVD；标注的 55/18/14/13% 是模型后验平均亚型比例，不同于按最大后验硬分配得到的 314/60/49/61 人（约 64.9/12.4/10.1/12.6%）。第 8 页图 5 是线性混合效应轨迹，图 6 是 45 人模型内解释度比较，不可当作外部预测结果。
代码与补充材料：作者公开仓库 https://github.com/qiuyuyue2022/Spatiotemporal-Subtypes-in-Pure-AD ，包含 ROI Z-score、SuStaIn Notebook 与后处理。仓库公开不等于其 484 人原始数据公开；论文声明原始 MRI 和临床数据受隐私限制。复现精确 17 ROI 组合仍需核对在线 Supplementary Table S1；若难以获取，可请导师或作者补充。
## 2.7 Li 等（2026）：个体化动力系统预测 [11]
作者利用 MRI/PET 与个体脑网络构建动态模型，在 1,891 名 ADNI 参与者中对 AD 病理与认知指标演变开展预测。它不是 SuStaIn，但已经展示“脑网络 + 多模态数据 + 认知轨迹个体化预测”的竞争方向。
**边界：** 我们的潜在价值是少模态、早期临床子群、分型可解释性以及预测校准，而不是声称首次做“网络到认知轨迹”的连接。
# 3. 研究竞争矩阵与可论证空白
| 工作 | 已有贡献 | 与本题直接重合 | 拟检验的区别 |
| --- | --- | --- | --- |
| Young 2018 [1] | 亚型 + 阶段联合推断 | 分型、异常顺序 | 面向独立未来认知的概率预测 |
| Estarellas 2024 [3] | 多模态 + 缺失处理 | 纳入临床指标 | 坚持未来结局独立、防循环验证 |
| Kim / Baumeister 2024 [5,6] | 纵向认知关联 | 亚型和认知下降 | 预测误差、区间、患者级留出 |
| Tandon 2024/25 [4,7] | 大特征分期与转化风险 | MCI 转化预测 | 连续轨迹 + 不确定性与校准 |
| Berman 2026 [9] | T1 SSN + SuStaIn | 网络—萎缩序列 | 测试网络的临床增量价值与稳健性 |
| Mao 2026 [10] | Aβ+ AD 亚型与 MMSE 预后 | AD 预后关联／比较 | 严谨外推、概率耦合、缺失处理 |
| Li 2026 [11] | 图动力模型预测认知 | 个体认知轨迹 | 低模态条件下的可解释与校准 |

## 3.1 真正需要回答的科学／工程问题
1. **增量信息：** 在强基线（年龄、教育、基线认知和原始 MRI）下，亚型–阶段的软后验到底还增加多少可预测信息？
2. **统计不确定性：** 患者不同亚型、不同阶段均可能合理时，硬标签是否造成不稳定的个体预测？后验加权能否改善预测区间校准？
3. **模型稳健性：** 早期 AD/MCI 影像差异微弱、样本不平衡、扫描站点混杂时，SuStaIn 序列与预测结果能否跨折／跨队列复现？
4. **网络价值（条件性）：** 从同一份 T1 构建的 SSN 与脑区体积高度关联，其额外信息是否真实存在？
**注意新颖性判断：** “使用 p(亚型, 阶段) 加权”本身可能只是已有概率推断的自然应用。若最终只有这一项代码修改，方法创新可能偏弱。开题前应补查 mixture-of-experts、probabilistic SuStaIn prognosis、survival mixture、posterior predictive AD 相关论文，并由导师确认足够的学位论文算法深度。
# 4. 推荐技术方案：可逐步升级的模型
## 4.0 先完成“网络＋SuStaIn＋认知量表”的最小研究闭环
第一步：以 T1_nii 为优先影像，做质量控制、脑区分割与灰质图预处理；由同一受试者的脑区灰质分布建立个体结构相似性网络（SSN），提取全局效率、局部效率、小世界性等候选网络指标。网络是灰质形态统计相似性，不代表 DTI 纤维束的真实物理连接。
第二步：分别用 ①脑区形态指标，②脑区形态＋SSN 网络指标建立 Z-score SuStaIn。比较亚型数、CVIC、PVD、阶段分布、跨折稳定性，做网络指标方向性与单调性检查。勿将大量高度相关图指标无筛选全部喂入 SuStaIn。
第三步：将亚型、阶段与 MMSE／ADAS13／CDR-SB 的基线分数关联，调整常见混杂因素。若有纵向量表，则优先完成真实留出个体的 12／24 月认知值预测；若无充分纵向量表，报告横断面关系，不声称预测了真实衰退轨迹。
第四步：使用网络指标消融、替换脑区数量、模型种子／折稳定性、强基线对照形成能够支撑硕士论文的实验体系。只有这些完成后才投入 SuStaIn 概率耦合、DTI 连接组或复杂深度学习。
创新性定位：本路线相对 Berman 2026 的算法架构不新，贡献预期在早期 MCI 队列的脑结构网络—临床量表联合验证、特征增益及稳健性分析。若导师明确要求算法结构创新，可再加入有依据的后验加权预测或网络特征稳定性选择模块。

## 4.1 任务定义与防泄漏的信息边界
对于受试者 i：基线形态学指标 xᵢ，基线协变量 cᵢ（年龄、性别、教育、诊断、ICV、站点等按可用性选取），可用的基线认知 yᵢ(0)；随访结果为 yᵢ(tⱼ)，其中 tⱼ 是距离基线的真实月数。主研究使用基线数据预测 12/24/36 月认知，不在预测时利用未来 MRI、未来诊断或未来认知。
先在训练集的基线 MRI 上拟合 SuStaIn，并仅以训练所得参数给验证／测试个体推断 qᵢ(k,s)=P(K=k,S=s | xᵢ)。严禁对全体受试者先进行 SuStaIn 拟合或预处理，再划分训练和测试。
## 4.2 [Optional] 主模型：概率耦合的纵向认知预测
> **核心公式（概念设计）** **p(yᵢ(t)|xᵢ,cᵢ,yᵢ(0)) = ΣₖΣₛ qᵢ(k,s) · pθ(yᵢ(t)|k,s,cᵢ,yᵢ(0),t)**。其中 q 为 SuStaIn 基线后验；pθ 是亚型/阶段条件下的认知轨迹预测分布。可从带正则化的线性混合模型、层次回归或时间样条开始，不应直接上大规模神经网络。

输出既包括点估计（如预测均值与 24 月认知变化），也包括预测区间。预测区间需同时考虑后验混合与观测残差；模型后验概率不是自动等于未来认知预测的置信区间。可采用严格的训练/校准划分或交叉拟合进行后验校准。
阶段 0 与异常早期不稳定的问题，可通过阶段归一化、后验期望阶段、亚型共享参数、样条平滑及层级收缩控制复杂度。需要防止在样本少时为每一个 (k,s) 独立训练模型导致严重过拟合。
## 4.3 完成导向的对照模型阶梯
| 级别 | 模型 | 目的／是否必做 |
| --- | --- | --- |
| M0 | 年龄、性别、教育＋基线认知 | 必做：临床强基线；仅在预测任务中有基线认知才使用 |
| M1 | M0＋T1 脑区形态特征 | 必做：MRI 形态是否有增量价值 |
| M2 | M0＋SSN 网络特征 | 必做：网络单独的解释或预测价值 |
| M3 | M0＋脑区形态＋SSN（不使用 SuStaIn） | 必做：检验分型分期相比原始特征有何作用 |
| M4 | M0＋形态 SuStaIn 硬分期／亚型 | 必做：纯形态 SuStaIn 基线 |
| M5 | M0＋形态＋SSN SuStaIn 硬分期／亚型 | 必做：直接回答三个关键词的组合是否有价值 |
| M6 | M5＋亚型—阶段后验概率或校准 | 视纵向人数与导师要求选做：增强方法贡献 |
## 4.4 [Optional] 核心创新应如何写进开题
拟创新点 1（主）：研究 SuStaIn 亚型—阶段**联合后验驱动**的认知轨迹分布预测框架，比较硬标签与完整后验在连续随访预测中的误差及稳定性；引入共享参数/层次正则控制高维阶段组合的过拟合。
拟创新点 2（主或加强）：考虑亚型与阶段不确定性传播、认知随访噪声及数据缺失的**区间估计与概率校准**，从点预测扩展到可靠的个体风险表达。
拟创新点 3（条件）：评估 MRI 结构相似性网络指标在脑形态指标之外的独立信息贡献，比较单一脑形态模型与结构+网络模型，并检查网络指标的单调性假设。
上面均应写成“拟研究／拟验证”，不要写“首次提出”“显著提高”“已证实网络先于萎缩”等未经证实断言。
# 5. 数据来源、最低要求与样本设计
| 资源／优先级 | 可用内容及用途 | 现实障碍 |
| --- | --- | --- |
| ADNI / 高 | MRI 区域表、原始 T1、临床量表、Aβ/Tau、纵向诊断；主研究首选 | 需申请访问；模态/时间点交集变小；站点差异 |
| TADPOLE / 高 | ADNI 派生的时序 ROI、临床表格；最适合快速方法原型 | 需遵守 ADNI 权限；与 ADNI 不是独立外部队列 |
| 实验室数据 / 待核实 | 可能提供额外人群／本地外部验证 | 知情同意、伦理许可、字段一致性、随访损失 |
| OASIS-3 / 中高 | 不同来源的 MRI 与临床随访；可做外部适用性检验 | 需申请；标志物和量表可比性不一定充分 |

官方入口：ADNI https://adni.loni.usc.edu/data-samples/adni-data/；TADPOLE https://tadpole.grand-challenge.org/Data/；OASIS-3 https://sites.wustl.edu/oasisbrains/home/oasis-3/。ADNI 使用协议、申请规则以及引用要求须遵守 [14–16]。
## 5.0 实验室 ADNI 数据库存与真正的数据缺口（2026-10-27 更新）
目前你确认实验室存在 amyloid_dcm、amyloid_nii、DTI_dcm、DTI_nii、FMRI_dcm、FMRI_nii、T1_dcm、T1_nii、tau_dcm、tau_nii。这说明存储了五类影像及不同文件表示，但无法据此确定各模态的受试者数、质量、随访时间、Aβ 阳性标签、临床评分或同一人多模态交集。DICOM 与 NIfTI 同时存在不等于两份独立样本。
| 目录 | 数据含义 | 在本课题中的优先级 |
| --- | --- | --- |
| T1_nii／T1_dcm | 结构 T1 MRI；脑区形态、个体 SSN 主要来源 | 必需；先检查有效 3D T1、扫描日期与 QC |
| amyloid_nii／dcm | Aβ PET；支持 Aβ 生物学分层，须匹配受试者与示踪剂 | 推荐用于限定 Aβ+ MCI，第二阶段接入 |
| tau_nii／dcm | Tau PET；病理分期与外部机制佐证 | 可选，不是入门必需 |
| DTI_nii／dcm | 扩散影像；白质结构连接可能需要 bvec/bval | 升级时使用，须完整梯度和 QC |
| FMRI_nii／dcm | 功能 MRI，可形成功能连接网络 | 非本课题所说结构网络，暂缓 |
最优先的待查资料不是额外影像，而是 ADNI 受试者级临床／量表 CSV：如 ADNIMERGE、诊断汇总 DXSUM、ADAS/MMSE/CDR 评分及人口学记录，若不在本地，可由获授权的 ADNI IDA 账户下载。ADNI 官方说明影像与临床表可通过 RID/PTID、VISCODE2、EXAMDATE、IMAGEUID 等字段关联，但实际连接必须核对扫描日期与访视窗口，不能只靠文件名或 VISCODE 拼接。
建议形成四级样本漏斗：① T1 受试者数；② 加入可匹配诊断、年龄、性别和基线量表的人数；③ 再加入 ≥1 次真实随访量表的人数与随访月份；④ 若使用 Aβ+ MCI，再加入该子群人数。另分别列出 T1＋DTI、T1＋PET 的交集数，并检查不同 ADNI 阶段／扫描站点的偏倚。
时间对齐建议：确定受试者的基线 T1 日期，再按预先声明的窗口选取基线临床测量（例如 ±90 天，作为初步候选而非固定规则）；预测时间按真实日期差计算，不把不同月份 VISCODE 混为等间隔观测。同一受试者的多次影像和认知记录必须始终留在同一数据划分侧。T1 网络特征从基线影像生成，不接触随访评分。
注意 ADNI1/GO/2/3/4 之间扫描场强、序列和设备存在显著差异，网络特征的标准化、ComBat 等任何依赖总体分布的处理都应限于训练数据拟合。优先利用 ADNI 已提供的 FreeSurfer 形态统计表做快速模型原型，再用现有 T1_nii 独立构建网络；这样不必先对整个库重新分割。
官方核验入口：ADNI Data https://adni.loni.usc.edu/data-samples/adni-data/；Clinical Assessments https://adni.loni.usc.edu/data-samples/adni-data/clinical-assessments/；MRI Numeric Outputs https://adni.loni.usc.edu/data-samples/adni-data/neuroimaging/mri/mri-numerical-data-sets/；ADNI FAQ https://adni.loni.usc.edu/help-faqs/faqs/ 。

## 5.1 需要向实验室确认的“数据能力表”
| 字段组 | 必须问的问题 | 决定什么 |
| --- | --- | --- |
| 受试者级 ID | 是否能关联基线 MRI 与多个随访？是否有去重 ID？ | 纵向预测和患者级划分 |
| MRI | 只有 FreeSurfer ROI 表，还是有原始 T1/DICOM？ | 能否做 SSN 网络 |
| 临床 | 是否有 ADAS13、MMSE、CDR-SB？随访月数与缺失率？ | 主终点及预测窗口 |
| AD 生物标志物 | 有无 Aβ/Tau PET、CSF、适用血液标志物？ | 能否严格称“临床前期 AD” |
| 诊断与事件 | MCI/AD 诊断时间、转化、末次随访？ | 事件预测与删失处理 |
| 扫描与人口学 | 年龄、性别、教育、ICV、扫描站点／批次？ | 标准化和混杂控制 |
| 许可 | 有无科研伦理/共享限制/对外公开政策？ | 论文可用性与 GitHub 合规 |

## 5.2 推荐的人群定义与主要结果
**主要预测人群：** 基线为 MCI 且具有基线 MRI 与至少一个目标时间窗附近的后续认知测量者；有 Aβ 状态时主分析优先 Aβ+ MCI，全部 MCI 作为敏感性分析。严格意义上的临床前期 AD（Aβ+ CU）独立分析，避免与广义 MCI 混为一谈。
**主要终点：** 24 月 ADAS-Cog13（优先），若缺少则使用 CDR-SB 或 MMSE，按数据可获得性固定一种为主终点。12 和 36 月结果作为次要终点。若目标窗无精确 24 月值，优先使用“以实际随访月份入模”的纵向混合模型，并明确固定时间点外推规则，不能随意挑选最接近结果而忽略时间误差。
**转化结局：** 仅在有明确转化日期、充分事件数量及删失信息时开展 MCI→AD 痴呆时间到事件分析；否则不作为主贡献。
**样本规模：** 当前未知，不填虚假数字。先形成 CN、MCI、AD、Aβ+ 子群、12/24/36 月有效配对人数和转化事件人数的样本漏斗图；复杂模型的自由参数与有效样本相匹配，并使用模拟／学习曲线确认可行性。
## 5.3 分层交付与失败降级：确保毕业方向可执行
第 1 档（不可省）：确认合法访问权限与临床表 → 构建受试者级基线 T1／认知表 → MRI 形态／SSN 指标质量控制 → 两套 SuStaIn → 与基线认知关系＋跨折稳健性 → 完成实验图、方法、结果和讨论。
第 2 档（优先提升）：同人随访认知足够时，加入实际月份预测、强基线对照、MAE／RMSE 和 Bootstrap 置信区间；此时可使用“预测”作为主要结论，并考虑题目 B。
第 3 档（可不做）：Aβ+ 生物学亚组、SuStaIn 后验加权及预测区间、DTI 白质连接组、复杂图神经网络、多队列外部验证。此类工作仅应在基础闭环已完成、数据与导师要求允许的情况下增加。
判断规则：若没有任何能够和 T1 匹配的认知量表，当前数据不足以满足导师三关键词，必须优先补齐临床表；若有一次认知量表但无随访，限于认知关联，不写真实时间预测；若网络特征无稳定可靠性，应报告失败并考虑更稳健的指标，但不能把结构相似性网络宣传成物理神经连接。

# 6. 可直接执行的实验协议（E0–E7）
| 编号 | 实验任务 | 比较／输出 | 成功或退出标准 |
| --- | --- | --- | --- |
| E0 | 数据审计与预注册协议 | 漏斗图、时间分布、缺失热图、字段字典 | 数据可合法使用且支持至少一项纵向终点 |
| E1 | 官方 pySuStaIn 复现 | 模拟数据→真实 ROI；PVD、后验、CV 亚型数 | 运行可复现；亚型/阶段非随机崩溃 |
| E2 | 基础纵向预测 | M0/M1/硬标签 M2；MAE、RMSE | 强基线建立且患者级留出 |
| E3 | 概率耦合预测 | M2 对 M3/M4；配对误差、校准 | 差异/区间有可信统计估计 |
| E4 | 风险预测（条件） | 24–36 月转化 C-index、时间 AUC、校准 | 足够事件与删失资料，避免数据泄漏 |
| E5 | SSN 增量（条件） | M3/M4 与 M5；网络单调性、稳定性 | 原始 T1 可得，增益对脑形态有条件独立性 |
| E6 | 稳健性与消融 | 软/硬、删基线认知、删协变量、样本扰动 | 报告改进与失败边界 |
| E7 | 外部验证（条件） | 固定模型转移另一队列；域偏移评估 | 独立受试者/来源且量表定义可对齐 |

## 6.1 强制执行的训练／测试规范
1. **先按受试者 ID 分割。** 多次随访、不同数据表、同一人的不同 ADNI/TADPOLE 记录一律在同一侧。若外部 OASIS-3，有时受试者可能跨项目出现，也须检查重复。
2. **所有数据依赖式预处理在训练折内拟合。** 年龄/性别/ICV 去偏、均值/方差标准化、异常阈值、缺失值填补、特征选择、SSN 图阈值确定及 SuStaIn 拟合不得提前看测试集。
3. **SuStaIn 只接收当时已知的信息。** 主实验用基线 MRI；可在预测器中使用同一时点的基线认知，但不能将未来认知作为 SuStaIn 输入再预测它。
4. **避免重用同一测试集调参。** 使用患者级训练/验证/最终测试或嵌套交叉验证；校准集与最终测试集分开。多个超参数与亚型数在训练环节确定。
5. **先固定主要终点与评价。** 主 MAE（24 月认知）及训练集/测试集配对 ΔMAE；次 RMSE、轨迹斜率误差、区间覆盖率与宽度、预测校准。转化时用删失适配指标，不直接把 Cox C-index 与分类 AUC 混用。
6. **不确定性统计：** 受试者级 Bootstrap 置信区间，多个随机种子／数据折；对罕见临床子群报告误差与区间而非只呈现总体平均。
## 6.2 推荐输出图表及其回答的问题
- **图 1：** 数据入组与随访漏斗图——是否真的有可用纵向样本？
- **图 2：** 各亚型 PVD／异常事件稳定性——脑结构模式是否可重复？
- **图 3：** SuStaIn 亚型–阶段后验热力图——早期患者的分型不确定性是否明显？
- **图 4：** 观测与预测认知轨迹、分型分期分层——模型究竟预测了什么？
- **图 5：** M0–M5 主要模型配对预测误差与 95% 置信区间——改进是否有实际意义？
- **图 6：** 预测区间覆盖率 vs 区间宽度、风险校准图——预测可靠性如何？
- **图 7（条件）：** 网络图指标加入前后预测增益与事件顺序扰动——网络信息是否真实有用？
# 7. 风险清单与预先定义的转向策略
| 风险 | 可能出现的事实 | 不影响毕业推进的应对 |
| --- | --- | --- |
| R1 纵向不足 | 只有单次 MRI + 单次认知 | 改为亚型分期与横断面关联；另用 ADNI/TADPOLE 做纵向主实验 |
| R2 无原始 MRI | 实验室只有 ROI 统计表 | 放弃 SSN，保留脑形态 SuStaIn 主研究 |
| R3 无 Aβ/Tau | 只有 MCI/CN/AD 临床分组 | 研究表述改为认知障碍风险，不宣称“临床前期 AD” |
| R4 模型无增益 | 软后验未胜过基线认知+MRI | 开展何种情况有效的误差/校准研究；不夸大，必要时换方法 |
| R5 后验太分散 | 亚型不稳定、阶段难辨 | 强正则、减少指标或亚型数、交叉验证；报告不确定性 |
| R6 缺失非随机 | 高风险人群更易失访 | 失访敏感性分析、混合模型、可行时逆概率加权 |
| R7 站点域偏移 | 外部队列性能下降 | 队列内外对照、训练内调整；明确外部域差异 |
| R8 文献重复 | 概率模型思想已有更接近工作 | 将贡献收窄到具体算法机制、可靠性/复现或改题，不虚构首创 |

**最低可毕业主线（旧版表述，以 V1.1 的 A 方案为准）：** 基线 ROI MRI + 有效纵向认知 → pySuStaIn → 强临床基线 + MRI 基线 → 软后验/层次轨迹方法 → 误差与校准消融 → 可复现论文。SSN 与 MCI 生存分析是增强模块，不应阻塞主线。
# 8. 软件、服务器与复现工程
## 8.1 开源起点
| 项目 | 用途 | 官方链接 |
| --- | --- | --- |
| pySuStaIn | 正式基线、模拟数据和概率输出 | https://github.com/ucl-pond/pySuStaIn |
| s-SuStaIn | 大特征数量时的可扩展基线 | https://github.com/pathology-dynamics/s-SuStaIn |
| FastSurfer（可选） | 原始 T1 的脑区分割／皮层测量 | https://github.com/Deep-MI/FastSurfer |
| NetworkX / nilearn | SSN 网络统计／脑区图谱处理 | https://networkx.org/ / https://nilearn.github.io/ |

SuStaIn 主要是 CPU 数值推断，48 线程 CPU 对交叉验证、Bootstrap、多初始化适用；4×3090 可用于原始 T1 预处理与可选深度学习，但不是 SuStaIn 主模型的必要条件。不应为了“用满显卡”而加入图神经网络。
## 8.2 GitHub 工程结构（建议）
`docs/`：proposal、literature、data_dictionary；`src/sustain/`：模型适配与训练内预处理；`src/prediction/`：基线与概率轨迹；`configs/`：固定数据与模型配置；`experiments/`：评估脚本；`results/`：可分享的汇总图表；`tests/`：泄漏/输入输出测试；`PROJECT_CONTEXT.md` 与 `EXPERIMENT_LOG.md`：决策记录与实验追踪。
严禁向公开仓库上传任何受数据使用协议、个人隐私或实验室伦理限制的原始数据、访问令牌、标识符以及可能重新识别个人的记录。所有科研实验要保存配置、随机种子、版本信息和匿名的聚合结果。
# 9. 可执行时间路线与阶段门槛
| 阶段 | 工作内容 | 完成判据 |
| --- | --- | --- |
| 阶段 1：选题核准 | 向导师确认算法深度、数据概况、终点；细读竞争论文 | 定题目 A/B/C 与“必做 vs 可选”研究边界 |
| 阶段 2：模型入门 | 阅读 Young/pySuStaIn 论文，跑模拟示例，产出 PVD | 能解释每个输入、后验、stage 与 PVD |
| 阶段 3：数据审计 | 申请 ADNI/TADPOLE；输出字段字典和纵向样本漏斗 | 确认主终点、入组标准、训练/测试方案 |
| 阶段 4：基线复现 | 完成 E1–E2 和 24 月指标；记录依赖和种子 | 有可复现的无泄漏临床与 MRI 基线 |
| 阶段 5：拟创新实验 | 完成 E3、可靠性消融，决定 E4/E5/E7 | 有证据支持或否定拟创新假设 |
| 阶段 6：论文与答辩 | 统计与可视化、论文写作、导师反馈 | 方法/数据/结果和代码完全对应 |

以上按阶段安排，不虚构开题日期。建议阶段 1–3 与开题文稿并行；一旦拿到具体学校模板即可将本论证按“背景—现状—关键问题—方法—可行性”映射到开题。
# 10. 当前必须确认的问题与最近行动
1. 最重要：实验室是否还存有 ADNI 临床／认知 CSV（例如 ADNIMERGE、诊断汇总、ADAS/MMSE/CDR、FreeSurfer 形态统计表）？这决定我们能否把影像与临床量表配对。只需回复有／没有／尚未查到。
2. 是否可以在 Linux 服务器的十个影像目录共同父目录运行只读的文件库存脚本？建议先输出文件类型计数与临床 CSV 文件名，不分享任何影像原件或受试者记录。
3. 导师口中的“脑结构网络”如果尚未细分，建议带题目 A 和 B 向导师确认：能否接受 T1 个体结构相似性网络作为结构网络，还是必须用 DTI 连接组。
4. 学位论文是否对“必须改进 SuStaIn 核心算法”有明确要求？若没有，则先完成可解释特征构建、脑网络增量实验和临床结局验证，再论证算法增强。
5. 开题报告模板和截止时间可在得到导师反馈后再确定，不阻碍我们立即进行 ADNI 数据审计与 pySuStaIn 官方示例复现。
建议交付顺序：第一步生成实验室影像与临床 CSV 库存报告；第二步构建一份脱敏的受试者交集统计表；第三步选择题目 A 或 B；第四步固定数据划分和评价方案，开始 T1 ROI＋SSN 的最小复现。
# 附录 A. 优先精读与原文获取清单
建议按“方法原点 → 纵向认知竞争 → 网络竞争 → 最新国内研究”的顺序。标注“有可访问全文”表示已找到出版商开放网页或会议全文入口；“补全文”表示目前仍建议获取 PDF 以核对细节。
[1] Young AL et al. Uncovering the heterogeneity and temporal complexity of neurodegenerative diseases with Subtype and Stage Inference. Nature Communications. 2018;9:4273. DOI:10.1038/s41467-018-05892-0.  https://www.nature.com/articles/s41467-018-05892-0  （开放全文；必读）

[2] Aksman LM et al. pySuStaIn: A Python implementation of the Subtype and Stage Inference algorithm. SoftwareX. 2021;16:100811. DOI:10.1016/j.softx.2021.100811.  https://github.com/ucl-pond/pySuStaIn  （源码与文档；必复现）

[3] Estarellas M et al. Multimodal subtypes identified in ADNI participants by missing-data-enabled subtype and stage inference. Brain Communications. 2024;6:fcae219. DOI:10.1093/braincomms/fcae219.  https://pmc.ncbi.nlm.nih.gov/articles/PMC11259979/  （开放全文；必读）

[4] Tandon R, Lah JJ, Mitchell CS. s-SuStaIn: Scaling subtype and stage inference via simultaneous clustering of subjects and biomarkers. PMLR. 2024;248:461–476.  https://proceedings.mlr.press/v248/tandon24a.html  （PDF 开放；方法对照）

[5] Kim J et al. Distinct spatiotemporal patterns of cortical thinning in Alzheimer’s disease-type cognitive impairment and subcortical vascular cognitive impairment. Communications Biology. 2024;7:198. DOI:10.1038/s42003-024-05787-5.  https://www.nature.com/articles/s42003-024-05787-5  （开放全文；纵向关联）

[6] Baumeister H et al. A generalizable data-driven model of atrophy heterogeneity and progression in memory clinic settings. Brain. 2024;147:2400–2413. DOI:10.1093/brain/awae118.  https://academic.oup.com/brain/article/147/7/2400/7657064  （开放论文页面／PMC；必读）

[7] Tandon R, Mei Y, Lah JJ, Mitchell CS. Comprehensive Anatomical Staging Predicts Clinical Progression in Mild Cognitive Impairment: A Data-Driven Approach. International Journal of Molecular Sciences. 2025;26:5514. DOI:10.3390/ijms26125514.  https://pmc.ncbi.nlm.nih.gov/articles/PMC12193007/  （开放全文；直接竞争）

[8] Prevot et al. How reproducible are data-driven subtypes of Alzheimer’s disease atrophy? Journal of Alzheimer’s Disease. 2026. DOI:10.1177/13872877251415019.  https://doi.org/10.1177/13872877251415019  （稳定性补充阅读）

[9] Berman B et al. Network Alterations Precede Atrophy in Alzheimer’s Disease Progression Subtypes. MICCAI 2026 MLCN Satellite.  https://papers.miccai.org/miccai-2026-sat/paper/MLCN_2026_032.pdf  （会议开放 PDF；网络必读）

[10] Mao C et al. Spatiotemporal atrophy subtypes in Alzheimer’s disease: Neurodegenerative-vascular associations and potential prognostic value. NeuroImage. 2026;340:122215. DOI:10.1016/j.neuroimage.2026.122215.  https://doi.org/10.1016/j.neuroimage.2026.122215  （已获得完整 PDF，已核验方法、样本量与局限）

[11] Li C, Mao Y, Liu X, Hao W. Data-driven modeling of spatiotemporal dynamics using multimodal imaging data. PLOS Computational Biology. 2026;22:e1014751. DOI:10.1371/journal.pcbi.1014751.  https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014751  （开放全文；广义进展预测竞品）

[12] de Jonge S et al. Disease Progression and Subtype Modeling for Combined Discrete and Continuous Input Data. 2026. arXiv:2602.22018.  https://arxiv.org/abs/2602.22018  （预印本；方法扩展）

[13] Jack CR Jr et al. Revised criteria for diagnosis and staging of Alzheimer’s disease: Alzheimer’s Association Workgroup. Alzheimer’s & Dementia. 2024. DOI:10.1002/alz.13859.  https://doi.org/10.1002/alz.13859  （医学定义与生物标志物）

[14] ADNI Official. Researcher data access and data use agreement.  https://support.adni4.org/hc/en-us/articles/31090030057236-I-am-a-researcher-how-do-I-access-ADNI-research-data-or-samples  （数据申请官方说明）

[15] TADPOLE Challenge. Data access and D1–D4 definitions.  https://tadpole.grand-challenge.org/Data/  （数据结构及获取方法）

[16] OASIS. OASIS-3 longitudinal neuroimaging resource.  https://sites.wustl.edu/oasisbrains/home/oasis-3/  （外部验证候选）

[17] ADNI Official. MRI numerical outputs and FreeSurfer morphometry. https://adni.loni.usc.edu/data-samples/adni-data/neuroimaging/mri/mri-numerical-data-sets/
[18] ADNI Official. Clinical Assessments: ADAS-Cog13, MMSE, CDR and MoCA availability. https://adni.loni.usc.edu/data-samples/adni-data/clinical-assessments/
[19] Qiu et al. Public analysis code companion to Mao et al. 2026. https://github.com/qiuyuyue2022/Spatiotemporal-Subtypes-in-Pure-AD
[20] ADNI Official. FAQ on data dictionary, clinical downloads and image/assessment linking. https://adni.loni.usc.edu/help-faqs/faqs/
[21] Berman B et al. Network Alterations Precede Atrophy in Alzheimer’s Disease Progression Subtypes. MICCAI Satellite 2026, Methods, pp. 2–4. https://papers.miccai.org/miccai-2026-sat/paper/MLCN_2026_032.pdf

# 附录 B. 文献阅读任务卡与下一次交流的输入
建议每篇核心论文的固定阅读卡：① 原问题和临床人群；② 训练/验证/测试人数；③ MRI 类型与脑区分割方式；④ 是否把认知输入 SuStaIn；⑤ 结果是否真正纵向、使用哪些测量时点；⑥ 性能及置信区间；⑦ 代码与下载入口；⑧ 可被我们独立验证的不足。
代码与补充材料：作者公开仓库 https://github.com/qiuyuyue2022/Spatiotemporal-Subtypes-in-Pure-AD ，包含 ROI Z-score、SuStaIn Notebook 与后处理。仓库公开不等于其 484 人原始数据公开；论文声明原始 MRI 和临床数据受隐私限制。复现精确 17 ROI 组合仍需核对在线 Supplementary Table S1；若难以获取，可请导师或作者补充。
