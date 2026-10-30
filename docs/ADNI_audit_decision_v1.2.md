# SuStaIn / AD-MCI 项目：ADNI 数据审计判读与选题决策备忘录（V1.2）

日期：2026-10-29

## 1. 当前已验证的信息

输入：`07_schema_v2.json`、`08_cohort_v2.json`（完整扫描 12,758 条数据记录、955 列）；此前 `command_out.txt` 中的 SMB 文件审计（由于时间/条目限制均不完整）。以下人数均为审计工具计算的不同受试者数，不是已经确认的完整实验队列。

| 项目 | 受试者数 | 注释 |
|---|---:|---|
| 注册表 RID/PTID 一一对应 | 3,221 | 各来源身份关联依据 |
| T1 影像元数据 | 3,237 | 不代表原始影像或分割结果可读 |
| T1 可经注册表映射到 RID | 3,221 | 仅身份级关联 |
| MMSE 有效评分 | 2,890 | 其中 1,925 名至少两个不同访视 |
| ADAS-Cog13 有效评分 | 2,294 | 其中 1,807 名至少两个不同访视 |
| CDR-SB 有效评分 | 2,886 | 其中 1,916 名至少两个不同访视 |
| MoCA 有效评分 | 1,028 | 其中 596 名至少两个不同访视 |
| ADNI_MEM 有效评分 | 2,075 | 其中 1,732 名至少两个不同访视 |
| DXSUM 有诊断记录 | 1,840 | 需进一步进行阶段编码及访视时间匹配 |
| UC Berkeley amyloid 来源 | 1,302 | 其中 1,285 名存在未解码状态标签 |
| T1 身份匹配 + 至少两次 MMSE 访视 | 1,925 | 尚未检查是否有可读 MRI、病理和基线访视 |

来自此前 SMB 文件审计：`processed_data` 已扫描到 `aseg.stats` 288 个；`recon_all_new` 已扫描到 `aseg.stats` 350 个。两者扫描不完整，可能包含重叠、失败或复扫。**不可相加为独立研究人数**。

## 2. 审计中发现的关键误判风险

1. `MMSE` 和 `CDRSB` 的 `VISCODE2=bl` 受试者数为 0，但存在大量 `sc`、`m12`、`m24` 记录。不能仅因 `bl` 缺失断言没有基线数据。应依据 MRI 扫描日期和量表实际测量日期匹配；临床诊断基线优先遵循 ADNI 对正式基线的定义。
2. `DXSUM` 严格 `VISCODE2=bl` 只得到 MCI=70、CU=96、Dementia=21（总计 187）。这是**当前选取方式下的数值**，不是所有可能用于基线分析的受试者人数。
3. Amyloid 状态 1,285 名受试者的数值/标签尚未经字典解码，因此 `explicit A+ = 0` 不能解读为没有 Aβ 阳性病例。不同示踪剂 SUVR 值不可直接混合。
4. 10,859 行包含至少两项 RID，其中未发现 RID 不一致；12,726 行同时有多个 PTID，其中 1 行存在不一致，需要本地核查。同行字段不等于同一次访视。
5. `PTID_T1` 与认知访视名称的字符串匹配数为 0 不能解读为无交集；T1 的长访视描述和临床 `VISCODE2` 格式不同。应按身份和实际检查日期关联。
6. UC Berkeley PET 结果中的 `*_VOLUME_UCBERKELEY` 是 PET 分析体系里的区域体积相关输出，不应未经数据源确认就当作独立的 T1 MRI 形态指标。

## 3. 选题建议（暂定）

**首选（条件成立时）**：《基于 SuStaIn 的 AD/MCI 脑结构网络与认知功能联合演变建模研究》。

学位论文方法主线：
- M1：T1 MRI 形态指标输入 Z-score SuStaIn；
- M2：加入从个体 T1 影像构建的结构相似性网络指标；
- M3：加入基线认知量表，研究联合的潜在异常事件序列；
- 验证：独立认知指标及（如有）实际随访认知变化。预测任务需进行受试者级划分，并加入基线认知单独预测对照。

**保底**：如日期配对和有效随访不足，重点研究 M1、M2 与独立认知关联，M3 为探索实验。任何不包含脑网络的降级方案需先取得导师认可。

## 4. 下一步必须完成的审核

运行 `adni_match_audit_v3.py` 对本地 `all.xlsx` 做以下检查：

- PTID ↔ RID 一一对应，影像 T1 的实际 Study Date、Image ID 非空；
- DXSUM 对应 EXAMDATE，按 ADNI 当前与历史阶段规则生成临床分类；
- 基线认知评分按实际访视日期与 T1 扫描日期匹配（默认 ±90 天）；
- 诊断按 MRI 周边 ±180 天匹配，Amyloid 状态仅统计字段覆盖、不自动解读数值标签；
- 按每名受试者最早满足条件的 T1 检查统计 CU、MCI、Dementia 各组规模，及至少 6 个月、约 12/24 个月随访覆盖；
- 数据审计最终还需将 T1 Image ID 与共享盘中的真实 NIfTI 或 DICOM 及 FreeSurfer/QC 成果关联。**目前这一步尚未实现**。

运行（在项目根目录）：

```bash
python3 scripts/adni_match_audit_v3.py \
  --xlsx data/all.xlsx \
  --out results/data_audit/09_matched_feasibility_v3.json
```

可选的测试：增加 `--max-rows 500` 并使用另一个输出文件；该结果应标记不完整。输入数据始终保留在服务器，审计程序只输出汇总计数（对小于 5 的计数抑制显示）。

## 5. 决策门槛（仅供规划，非统计学标准）

- 若实际可匹配 T1 + 诊断 + 至少一种基线认知评分的人群充足（建议先检查 MCI、CU、Aβ 状态分层），将 M1/M2/M3 作为论文主体；
- 若还存在足够 12/24 月随访，增加纵向预测或变化斜率分析，先从简单基线做起；
- 若可匹配 MRI 受试者多但 FreeSurfer 合格结果有限，优先重新处理入选研究队列中的 T1，而非全部影像；
- 若 Aβ 阳性筛选后样本少，不得把所有 MCI 都称作 AD 生物标志物确诊人群，需重写研究对象表述。

## 6. 权威资料

- ADNI 诊断数据说明：https://adni.loni.usc.edu/quick-start-guide-asset/diagnostic.html
- ADNI 各阶段编码问答：https://adni.loni.usc.edu/support/experts-knowledge-base/question/?QID=1756
- ADNI VISCODE2 与真实日期：https://adni.loni.usc.edu/support/experts-knowledge-base/question/?QID=2126
- ADNI PET 结果说明：https://adni.loni.usc.edu/quick-start-guide-asset/pet.html
- ADNI MRI 质量与数值结果：https://adni.loni.usc.edu/data-samples/adni-data/neuroimaging/mri/

隐私：原始 `all.xlsx`、影像、个体级表格、身份索引仅在经授权的服务器上使用；公开项目不得提交原始 ADNI 受控数据或密钥。
