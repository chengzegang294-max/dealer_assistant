# S 分桶摘要

目录根：

- `D:\Stock\cut_file\S`

## 当前角色

- `S桶` 当前不是“仓库内已独立资料库”，而是：
  - 外部源文件树
  - 仓库内索引 / 摘要 / 去重证据
- 因此当前不能进入“整盘删除 `D:\Stock\cut_file`”窗口。

## 现状统计

### 1) 外部实际文件树（2026-06-22 复核）

- 实际总文件数：`868`
- 扩展名分布：
  - `.pdf`：`610`
  - `.md`：`44`
  - `.doc`：`3`
  - `.docx`：`7`
  - `.epub`：`114`
  - `.opf`：`45`
  - `.jpg`：`44`
  - `.original_epub`：`1`

### 2) 顶层桶规模（按实际文件树）

- `01_集合竞价教程`：`49` 文件，约 `5.55 MB`
- `02_游资悟道交割单`：`341` 文件，约 `2251.01 MB`
- `03_券商研报`：`477` 文件，约 `2360.69 MB`
- `04_待归类`：`1` 文件，约 `37.14 MB`

### 3) 当前仓库内索引覆盖

- `S_BUCKET_INDEX__2026-06-17.tsv` 已于 `2026-06-22` 重新生成并补齐到 `868` 条
- 当前已与外部实际文件树对齐：
  - `.pdf`：`610`
  - `.md`：`44`
  - `.doc`：`3`
  - `.docx`：`7`
  - `.epub`：`114`
  - `.opf`：`45`
  - `.jpg`：`44`
  - `.original_epub`：`1`
- 旧口径里的 `620 -> 868` manifest 缺口已关闭

### 4) 已有去重证据

- `S_DUP_DELETE_LIST__same_hash__2026-06-17.tsv` 已记录 `200` 条同 hash 重复拷贝删除行
- 对应释放体量约 `1251.41 MB`
- 这说明 `S桶` 之前已经做过“完全重复件”收缩，但还没有完成“独立化”

## 券商研报二级桶

- `01_高频微观`：`98`
- `02_指数增强`：`16`
- `03_机器学习`：`112`
- `04_多因子`：`181`
- `05_其他`：`70`

## 历史追溯层

- 本节只保留 `S桶` 进入当前主线前的前置完成状态、旧边界与来源沿革。
- 本节不承担默认入口说明；当前默认入口以 `当前合同层` 为准。

1. `S桶` 的“全量 manifest”已补齐：
   - 仓库内索引现在已是外部实际文件树的完整镜像
   - 后续 staging / 删源判断不再漏掉 `.epub / .opf / .jpg` 等对象
2. `S桶` 仍未完成“全量仓库内自有真值副本”：
   - 当前 `01_集合竞价教程` 已完成最小 staging proof
  - 当前 `03_券商研报` 已完成“代表作层”前五十二批 proof：前八批按四主题各 `2` 份推进，`v9-v40` 改为 `2 + 3 + 3` 配额，`v41` 因机器学习池仅剩 `1` 个对象而收缩为 `2 + 1 + 3`，`v42-v49` 已切到 `高频微观=2 / 多因子=6` 两主题模式，`v50-v52` 因高频微观源池耗尽改为纯多因子续推，累计 `408` 份
  - `post-v52` 默认规则已固定为：`STOP_AT_FILLED__NO_AUTO_EXPANSION`
  - `05_其他` 当前继续留在 `future bucket`，不自动重开 proof
  - 只有在新增来源进入 inventory、或用户显式要求开 `05_其他` 试点时，才重开下一轮
   - `02_游资悟道交割单 / 03_券商研报` 其余主体 / `04_待归类` 仍主要依赖 `D:\Stock\cut_file\S`
3. `S桶` 仍需要继续沿主线优先级推进：
   - 当前不追求一次性全量进仓
   - 仍要避免把 `03_券商研报` 的 `477` 份全文搬进仓库
4. `S桶` 当前已开始预备“功能层”：
   - 新增 `S_BUCKET_功能归类最小框架_v1.md`
   - 当前口径不是改物理目录，而是在来源层之上新增功能映射层

## 当前合同层

- 本节统一镜像 `00 / 01 / 03` 的合同写法。
- 本层只收：`当前生效入口 / 包级角色 / 固定顺序 / 扩展附注`
- 默认阅读顺序固定为：
  - `repo 默认入口`
  - `repo 真值文件`
  - `repo 回帖副本`
  - `外部 PDF 读取目录`
  - `外部目录角色`
5. `Kimi` 第一轮对象卡批次已回收：
   - 包级角色：文件名初筛包；用于挂接首轮草稿与基础真值映射
   - 固定顺序：`包级角色 -> repo 默认入口 -> repo 真值文件 -> repo 回帖副本 -> 外部目录 -> 附注`
   - repo 默认入口：`S_BUCKET_SUMMARY__2026-06-17.md`
   - repo 真值文件：`S_BUCKET_KIMI_batch1_prompt_v1.txt`、`S_BUCKET_功能映射表_v1.tsv`
   - repo 回帖副本：`99_回收与外部回帖_IMPORTS/S_BUCKET_functional_cards_batch1_v15_v16__draft__imported_2026-06-24.md`
   - 外部 PDF 读取目录：`D:\Stock\cut_file\data\__KIMI_batches\S_BUCKET_functional_cards_batch1_v15_v16`
   - 外部目录角色：仅作为 PDF 读取位置，不作为默认入口
   - 扩展字段附注：`decision=filename_only_draft；review_status=DRAFT_ONLY__NEEDS_TEXT_READ；boundary=not_body_text_truth`
6. `batch1` 当前已启动优先对象精读包：
   - 包级角色：正文优先精读包；用于锁定可读对象与稳定真值
   - 固定顺序：`包级角色 -> repo 默认入口 -> repo 真值文件 -> repo 回帖副本 -> 外部目录 -> 附注`
   - repo 默认入口：`S_BUCKET_SUMMARY__2026-06-17.md`
   - repo 真值文件：`S_BUCKET_KIMI_batch1_priority_read_prompt_v1.txt`、`S_BUCKET_功能映射表_v1.tsv`
   - repo 回帖副本：`99_回收与外部回帖_IMPORTS/S_BUCKET_batch1_priority_read_v1__text_review__imported_2026-06-24.md`
   - 外部 PDF 读取目录：`D:\Stock\cut_file\data\__KIMI_batches\S_BUCKET_batch1_priority_read_v1`
   - 外部目录角色：仅作为 PDF 读取位置，不作为默认入口
-   - 扩展字段附注：`durable_truth=S_BUCKET_功能映射表_v1.tsv+imported_reply_md；objects=SBKT_F006/F014/F002/F007/F004；result=5_of_5_ok|0_need_ocr；review_status=TEXT_EVIDENCE_IMPORTED__NO_OCR；ranking=SBKT_F014>SBKT_F006>SBKT_F002>SBKT_F007>SBKT_F004`
7. `batch1` 当前已启动第二轮正文精读包：
   - 包级角色：正文收缩验证包；用于做代表因子与共线性收缩
   - 固定顺序：`包级角色 -> repo 默认入口 -> repo 真值文件 -> repo 回帖副本 -> 外部目录 -> 附注`
   - repo 默认入口：`S_BUCKET_batch1_round2_focus_README_v1.md`
   - repo 真值文件：`S_BUCKET_batch1_round2_focus_manifest_v1.tsv`、`S_BUCKET_KIMI_batch1_round2_focus_prompt_v1.txt`、`S_BUCKET_KIMI_batch1_round2_direct_message_v2.txt`、`S_BUCKET_功能映射表_v1.tsv`
   - repo 回帖副本：`99_回收与外部回帖_IMPORTS/S_BUCKET_batch1_round2_focus_v1__text_review__imported_2026-06-24.md`
   - 外部 PDF 读取目录：`D:\Stock\cut_file\data\__KIMI_batches\S_BUCKET_batch1_round2_focus_v1`
   - 外部目录角色：仅作为 PDF 读取位置，不作为默认入口
   - 扩展字段附注：`objects=SBKT_F014/F006/F002；focus=representative_shrink/correlation_shrink/recent_decay_check；result=F014->mfd_sellord+mfd_volinflowrate_open_m|F006->id2_std_3m+hml_r_std_5m|F002->空头/多空；boundary=F014/F006_two_factor_set_from_perf_and_correlation_shrink|F002_failure_reason_still_limited_to_reversal_volatility_correlation`
8. `batch1` 第三轮功能核心对象卡包当前已在 repo 内准备完成：
   - 包级角色：功能核心固化包；用于把收缩结论压成对象核心卡
   - 固定顺序：`包级角色 -> repo 默认入口 -> repo 真值文件 -> repo 回帖副本 -> 外部目录 -> 附注`
   - repo 默认入口：`S_BUCKET_batch1_round3_function_core_README_v1.md`
   - repo 真值文件：`S_BUCKET_batch1_round3_function_core_manifest_v1.tsv`、`S_BUCKET_KIMI_batch1_round3_function_core_prompt_v1.txt`、`S_BUCKET_KIMI_batch1_round3_function_core_direct_message_v1.txt`、`S_BUCKET_功能映射表_v1.tsv`
   - repo 回帖副本：当前结果已直接并回本文档与 `S_BUCKET_功能映射表_v1.tsv`，暂无单独 imported reply
   - 外部 PDF 读取目录：`D:\Stock\cut_file\data\__KIMI_batches\S_BUCKET_batch1_round3_function_core_v1`
   - 外部目录角色：仅作为 PDF 读取位置，不作为默认入口
   - 扩展字段附注：`goal=function_core_cards_for_SBKT_F014/F006/F002；state=external_pdf_copied_and_direct_message_sent；result=SBKT_F014/F006->ENTER_FUNCTION_CORE_WITH_BOUNDARY|SBKT_F002->KEEP_AS_LIMITED_CANDIDATE；ranking=SBKT_F014>SBKT_F006>SBKT_F002；fallback=long_only_keep_SBKT_F014+SBKT_F006`

## 独立化方案

- 本节只说明 `S桶` 的独立化边界、分层方案与 future bucket，不替代上面的 `当前合同层`。
- 若出现入口判断冲突，优先遵循 `当前合同层`，再回看本节解释为什么仍保留部分外部依赖。

### 目标定义

- `S桶` 独立化不等于“一次性把 868 个文件全部搬进仓库”
- 当前更稳的定义是先完成三件事：
  1. 有全量 manifest
  2. 有仓库内可直接使用的最小自有子集
  3. 有明确的“哪些仍依赖外部源、哪些已可脱离 cut_file”的边界

### 分层方案

1. `manifest 层`
   - 已完成：`S桶` 现已具备覆盖实际 `868` 文件的全量清单
   - 这条前置门槛已经通过
2. `最小可用层`
   - 第一优先独立对象 `01_集合竞价教程` 已完成最小 staging proof
   - proof 结果：`49` 条已复制到仓库内 `S_BUCKET__staging\01_集合竞价教程`
   - proof 文件：`S_BUCKET_stage_proof__01_集合竞价教程__v1.tsv`
3. `代表作层`
   - `03_券商研报` 不做 `477` 份全文搬运
  - 已完成前五十二批代表作 proof：`高频微观=98`、`指数增强=16`、`机器学习=113`、`多因子=181`，累计 `408` 份
   - 第一批代表作清单：`S_BUCKET_report_representatives_v1.tsv`
   - 第一批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v1.tsv`
   - 第二批代表作清单：`S_BUCKET_report_representatives_v2.tsv`
   - 第二批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v2.tsv`
   - 第三批代表作清单：`S_BUCKET_report_representatives_v3.tsv`
   - 第三批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v3.tsv`
   - 第四批代表作清单：`S_BUCKET_report_representatives_v4.tsv`
   - 第四批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v4.tsv`
   - 第五批代表作清单：`S_BUCKET_report_representatives_v5.tsv`
   - 第五批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v5.tsv`
   - 第六批代表作清单：`S_BUCKET_report_representatives_v6.tsv`
   - 第六批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v6.tsv`
   - 第七批代表作清单：`S_BUCKET_report_representatives_v7.tsv`
   - 第七批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v7.tsv`
   - 第八批代表作清单：`S_BUCKET_report_representatives_v8.tsv`
   - 第八批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v8.tsv`
   - 第九批代表作清单：`S_BUCKET_report_representatives_v9.tsv`
   - 第九批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v9.tsv`
   - 第十批代表作清单：`S_BUCKET_report_representatives_v10.tsv`
   - 第十批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v10.tsv`
   - 第十一批代表作清单：`S_BUCKET_report_representatives_v11.tsv`
   - 第十一批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v11.tsv`
   - 第十二批代表作清单：`S_BUCKET_report_representatives_v12.tsv`
   - 第十二批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v12.tsv`
   - 第十三批代表作清单：`S_BUCKET_report_representatives_v13.tsv`
   - 第十三批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v13.tsv`
   - 第十四批代表作清单：`S_BUCKET_report_representatives_v14.tsv`
   - 第十四批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v14.tsv`
   - 第十五批代表作清单：`S_BUCKET_report_representatives_v15.tsv`
   - 第十五批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v15.tsv`
   - 第十六批代表作清单：`S_BUCKET_report_representatives_v16.tsv`
   - 第十六批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v16.tsv`
   - 第十七批代表作清单：`S_BUCKET_report_representatives_v17.tsv`
   - 第十七批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v17.tsv`
   - 第十八批代表作清单：`S_BUCKET_report_representatives_v18.tsv`
   - 第十八批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v18.tsv`
   - 第十九批代表作清单：`S_BUCKET_report_representatives_v19.tsv`
   - 第十九批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v19.tsv`
   - 第二十批代表作清单：`S_BUCKET_report_representatives_v20.tsv`
   - 第二十批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v20.tsv`
   - 第二十一批代表作清单：`S_BUCKET_report_representatives_v21.tsv`
   - 第二十一批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v21.tsv`
   - 第二十二批代表作清单：`S_BUCKET_report_representatives_v22.tsv`
   - 第二十二批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v22.tsv`
   - 第二十三批代表作清单：`S_BUCKET_report_representatives_v23.tsv`
   - 第二十三批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v23.tsv`
   - 第二十四批代表作清单：`S_BUCKET_report_representatives_v24.tsv`
   - 第二十四批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v24.tsv`
   - 第二十五批代表作清单：`S_BUCKET_report_representatives_v25.tsv`
   - 第二十五批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v25.tsv`
   - 第二十六批代表作清单：`S_BUCKET_report_representatives_v26.tsv`
   - 第二十六批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v26.tsv`
   - 第二十七批代表作清单：`S_BUCKET_report_representatives_v27.tsv`
   - 第二十七批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v27.tsv`
   - 第二十八批代表作清单：`S_BUCKET_report_representatives_v28.tsv`
   - 第二十八批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v28.tsv`
   - 第二十九批代表作清单：`S_BUCKET_report_representatives_v29.tsv`
   - 第二十九批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v29.tsv`
   - 第三十批代表作清单：`S_BUCKET_report_representatives_v30.tsv`
   - 第三十批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v30.tsv`
   - 第三十一批代表作清单：`S_BUCKET_report_representatives_v31.tsv`
   - 第三十一批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v31.tsv`
   - 第三十二批代表作清单：`S_BUCKET_report_representatives_v32.tsv`
   - 第三十二批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v32.tsv`
   - 第三十三批代表作清单：`S_BUCKET_report_representatives_v33.tsv`
   - 第三十三批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v33.tsv`
  - 第三十四批代表作清单：`S_BUCKET_report_representatives_v34.tsv`
  - 第三十四批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v34.tsv`
  - 第三十五批代表作清单：`S_BUCKET_report_representatives_v35.tsv`
  - 第三十五批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v35.tsv`
  - 第三十六批代表作清单：`S_BUCKET_report_representatives_v36.tsv`
  - 第三十六批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v36.tsv`
  - 第三十七批代表作清单：`S_BUCKET_report_representatives_v37.tsv`
  - 第三十七批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v37.tsv`
  - 第三十八批代表作清单：`S_BUCKET_report_representatives_v38.tsv`
  - 第三十八批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v38.tsv`
  - 第三十九批代表作清单：`S_BUCKET_report_representatives_v39.tsv`
  - 第三十九批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v39.tsv`
  - 第四十批代表作清单：`S_BUCKET_report_representatives_v40.tsv`
  - 第四十批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v40.tsv`
  - 第四十一批代表作清单：`S_BUCKET_report_representatives_v41.tsv`
  - 第四十一批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v41.tsv`
  - 第四十二批代表作清单：`S_BUCKET_report_representatives_v42.tsv`
  - 第四十二批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v42.tsv`
  - 第四十三批代表作清单：`S_BUCKET_report_representatives_v43.tsv`
  - 第四十三批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v43.tsv`
  - 第四十四批代表作清单：`S_BUCKET_report_representatives_v44.tsv`
  - 第四十四批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v44.tsv`
  - 第四十五批代表作清单：`S_BUCKET_report_representatives_v45.tsv`
  - 第四十五批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v45.tsv`
  - 第四十六批代表作清单：`S_BUCKET_report_representatives_v46.tsv`
  - 第四十六批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v46.tsv`
  - 第四十七批代表作清单：`S_BUCKET_report_representatives_v47.tsv`
  - 第四十七批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v47.tsv`
  - 第四十八批代表作清单：`S_BUCKET_report_representatives_v48.tsv`
  - 第四十八批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v48.tsv`
  - 第四十九批代表作清单：`S_BUCKET_report_representatives_v49.tsv`
  - 第四十九批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v49.tsv`
  - 第五十批代表作清单：`S_BUCKET_report_representatives_v50.tsv`
  - 第五十批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v50.tsv`
  - 第五十一批代表作清单：`S_BUCKET_report_representatives_v51.tsv`
  - 第五十一批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v51.tsv`
  - 第五十二批代表作清单：`S_BUCKET_report_representatives_v52.tsv`
  - 第五十二批 proof 文件：`S_BUCKET_stage_proof__03_券商研报__representatives_v52.tsv`
  - 注意：`02_指数增强` 已在既定代表作口径下耗尽；`03_机器学习` 已在 `v41` 用完最后 `1` 个对象；`01_高频微观` 已在 `v49` 用完最后 `2` 个对象；`04_多因子` 也已在 `v52` 收满最后 `2` 个对象；因此当前四个代表作目标桶均已完成 proof，后续不再沿旧配额继续扩批
4. `功能映射预备层`
   - 当前已新增：`S_BUCKET_功能归类最小框架_v1.md`
   - 当前裁决：保留来源目录作为真值层，不直接改物理目录
  - 当前下一步：保持 `03_券商研报` 停在已收满状态，不再沿旧配额推进；如需新一轮，只能显式改开 `05_其他 / future bucket` 试点；并把 `round3 function core` 的固化结果继续并回功能层对象卡
  - source control backlog 已完成三分类台账：`docs/SOURCE_CONTROL_BACKLOG_TRIAGE__2026-06-23.md`
5. `Kimi 批次执行层`
   - repo 默认入口：`S_BUCKET_SUMMARY__2026-06-17.md`
   - repo 真值文件：`S_BUCKET_KIMI_batch1_prompt_v1.txt`、`S_BUCKET_功能映射表_v1.tsv`
   - repo 回帖副本：`99_回收与外部回帖_IMPORTS/S_BUCKET_functional_cards_batch1_v15_v16__draft__imported_2026-06-24.md`
   - 外部 PDF 读取目录：`D:\Stock\cut_file\data\__KIMI_batches\S_BUCKET_functional_cards_batch1_v15_v16`
   - 外部目录角色：仅作为 PDF 读取位置，不作为默认入口
   - 当前回收状态：`16/16` 已导入，状态为 `IMPORTED__FILENAME_ONLY_DRAFT`
   - 当前审核状态：`DRAFT_ONLY__NEEDS_TEXT_READ`
6. `Kimi 正文精读层`
   - repo 默认入口：`S_BUCKET_SUMMARY__2026-06-17.md`
   - repo 真值文件：`S_BUCKET_KIMI_batch1_priority_read_prompt_v1.txt`、`S_BUCKET_功能映射表_v1.tsv`
   - repo 回帖副本：`99_回收与外部回帖_IMPORTS/S_BUCKET_batch1_priority_read_v1__text_review__imported_2026-06-24.md`
   - 外部 PDF 读取目录：`D:\Stock\cut_file\data\__KIMI_batches\S_BUCKET_batch1_priority_read_v1`
   - 外部目录角色：仅作为 PDF 读取位置，不作为默认入口
   - 当前 durable truth：`S_BUCKET_功能映射表_v1.tsv` + `99_回收与外部回帖_IMPORTS/S_BUCKET_batch1_priority_read_v1__text_review__imported_2026-06-24.md`
   - 当前回执结果：`5/5 OK`，`0 NEED_OCR`
   - 当前首轮正文优先对象：`SBKT_F014 / F006 / F002 / F007 / F004`
7. `Kimi 第二轮精读层`
   - repo 默认入口：`S_BUCKET_batch1_round2_focus_README_v1.md`
   - repo 真值文件：`S_BUCKET_batch1_round2_focus_manifest_v1.tsv`、`S_BUCKET_KIMI_batch1_round2_focus_prompt_v1.txt`、`S_BUCKET_功能映射表_v1.tsv`
   - repo 回帖副本：`99_回收与外部回帖_IMPORTS/S_BUCKET_batch1_round2_focus_v1__text_review__imported_2026-06-24.md`
   - 外部 PDF 读取目录：`D:\Stock\cut_file\data\__KIMI_batches\S_BUCKET_batch1_round2_focus_v1`
   - 外部目录角色：仅作为 PDF 读取位置，不作为默认入口
   - 当前对象：`SBKT_F014 / F006 / F002`
   - 当前目标：从正文证据层继续收缩到“代表因子 / 最小组合 / 失效边界”
   - 当前已完成正文收缩回收：`SBKT_F014 / F006` 已进入“最小组合候选”层，`SBKT_F002` 已进入“限制用途边界”层
   - 当前审核口径：`IMPORTED__ROUND2_REDUCTION_OK / TEXT_EVIDENCE_IMPORTED__ROUND2_REDUCED`
8. `Kimi 第三轮功能核心层`
   - repo 默认入口：`S_BUCKET_batch1_round3_function_core_README_v1.md`
   - repo 真值文件：`S_BUCKET_batch1_round3_function_core_manifest_v1.tsv`、`S_BUCKET_KIMI_batch1_round3_function_core_prompt_v1.txt`、`S_BUCKET_KIMI_batch1_round3_function_core_direct_message_v1.txt`、`S_BUCKET_功能映射表_v1.tsv`
   - repo 回帖副本：当前结果已直接并回本文档与 `S_BUCKET_功能映射表_v1.tsv`，暂无单独 imported reply
   - 外部 PDF 读取目录：`D:\Stock\cut_file\data\__KIMI_batches\S_BUCKET_batch1_round3_function_core_v1`
   - 外部目录角色：仅作为 PDF 读取位置，不作为默认入口
   - 当前回收口径：结果已写回本文档与 `S_BUCKET_功能映射表_v1.tsv`
9. `外部保留层`
   - `02_游资悟道交割单` 中的 `.epub / .opf / .jpg / .original_epub` 当前继续保留在外部
   - 在没有明确主线用途前，不进入仓库内 staging

10. `统一入口合同模板`
   - 当前统一模板：`docs/playbooks/PLAYBOOK_滚动模板.md` -> `S_BUCKET_ENTRY_CONTRACT__REPO_FIRST`
   - 当前要求字段顺序固定为：
     - `repo 默认入口`
     - `repo 真值文件`
     - `repo 回帖副本`
     - `外部 PDF 读取目录`
     - `外部目录角色`

### 四分流

- `已吸收 / 最先独立`
  - `01_集合竞价教程`
- `可重开`
  - `03_券商研报` 的第三十五批代表作扩展批次
  - `03_券商研报` 已回收对象卡的第二轮正文级补读回帖
- `future bucket`
  - `02_游资悟道交割单` 的 `pdf/docx` 子集
  - `03_券商研报` 的 `05_其他`
- `仅来源库保留`
  - `02_游资悟道交割单` 的 `.epub / .opf / .jpg / .original_epub`
  - `04_待归类` 在人工确认前暂不进仓

## 当前建议推进顺序

1. 已完成 `S桶` 全量 manifest 补齐：`620 -> 868`。
2. 已完成 `01_集合竞价教程` 最小 staging proof，形成第一批仓库内自有入口。
3. 已完成 `03_券商研报` 前五十二批主题代表作 proof，累计 `408` 份，不做 `477` 份全量进仓。
4. `v9-v40` 为三主题扩批，`v41` 为 `2 + 1 + 3` 过渡批次，`v42-v49` 为 `高频微观=2 / 多因子=6` 两主题模式，`v50-v52` 因高频微观耗尽改为纯多因子续推；当前四个代表作目标桶已全部收满。
5. `post-v52` 默认裁决是：停在已收满状态，不自动继续扩批；`05_其他` 继续留在 `future bucket`，只有在新增来源入库或显式试点决策下才重开。
5. 已新增“功能映射预备层”，当前先做对象卡和功能标签，不改来源目录真值结构。
6. 已完成 `Kimi batch1` 回收：`v15-v16` 的 `16` 张对象卡已并回功能映射表，其中 `5` 张已升级为正文证据层。
7. `batch1` 第一轮优先对象精读已完成：`5/5` 可读、`0` 个需要 OCR。
8. `batch1` 第二轮正文精读包已准备就绪，当前聚焦 `SBKT_F014 / F006 / F002` 的收缩与边界澄清。
9. 第二轮已收到成功回帖并完成仓库内回收：`SBKT_F014 / F006` 已形成 `2` 因子最小集合候选，`SBKT_F002` 已确认只保留 `空头 / 多空` 用途；后续若继续，应以这轮收缩结果作为功能层新起点。

## 独立化完成前的禁止事项

- 不把 `S桶` 当前索引误写成“已独立”
- 不把“manifest 已补齐”误写成“整桶已独立”
- 不把 `03_券商研报` 全量 `477` 份直接搬进仓库
- 不在 `02_游资悟道交割单` 的 `epub/jpg/opf` 还没定用途前做大批量入仓

## 当前验收口径

- 当前若删除 `D:\Stock\cut_file\S`：
  - `GROUP_08` 相关研究 `pdf` 仍可用
  - `S桶` 中 `01_集合竞价教程` 这 `49` 条 proof 子集仍可用
- `S桶` 中 `03_券商研报` 的前五十二批 `408` 份代表作 proof 仍可用
  - `02_游资悟道交割单 / 03_券商研报` 其余主体 / `04_待归类` 仍不可视为安全
- 因而当前正式口径固定为：
  - `GROUP_08`：`日常可脱离 cut_file`
  - `S桶`：`PARTIAL_PROOF_ONLY`

## 配套清单

- `S_BUCKET_INDEX__2026-06-17.tsv`
- `S_DUP_REPORT__sha256__2026-06-17.tsv`
- `S_DUP_DELETE_LIST__same_hash__2026-06-17.tsv`
- `S_BUCKET_report_representatives_v1.tsv`
- `S_BUCKET_report_representatives_v2.tsv`
- `S_BUCKET_report_representatives_v3.tsv`
- `S_BUCKET_report_representatives_v4.tsv`
- `S_BUCKET_report_representatives_v5.tsv`
- `S_BUCKET_report_representatives_v6.tsv`
- `S_BUCKET_report_representatives_v7.tsv`
- `S_BUCKET_report_representatives_v8.tsv`
- `S_BUCKET_report_representatives_v9.tsv`
- `S_BUCKET_report_representatives_v10.tsv`
- `S_BUCKET_report_representatives_v11.tsv`
- `S_BUCKET_report_representatives_v12.tsv`
- `S_BUCKET_report_representatives_v13.tsv`
- `S_BUCKET_report_representatives_v14.tsv`
- `S_BUCKET_report_representatives_v15.tsv`
- `S_BUCKET_report_representatives_v16.tsv`
- `S_BUCKET_report_representatives_v17.tsv`
- `S_BUCKET_report_representatives_v18.tsv`
- `S_BUCKET_report_representatives_v19.tsv`
- `S_BUCKET_report_representatives_v20.tsv`
- `S_BUCKET_report_representatives_v21.tsv`
- `S_BUCKET_report_representatives_v22.tsv`
- `S_BUCKET_report_representatives_v23.tsv`
- `S_BUCKET_report_representatives_v24.tsv`
- `S_BUCKET_report_representatives_v25.tsv`
- `S_BUCKET_report_representatives_v26.tsv`
- `S_BUCKET_report_representatives_v27.tsv`
- `S_BUCKET_report_representatives_v28.tsv`
- `S_BUCKET_report_representatives_v29.tsv`
- `S_BUCKET_report_representatives_v30.tsv`
- `S_BUCKET_report_representatives_v31.tsv`
- `S_BUCKET_report_representatives_v32.tsv`
- `S_BUCKET_report_representatives_v33.tsv`
- `S_BUCKET_report_representatives_v34.tsv`
- `S_BUCKET_report_representatives_v35.tsv`
- `S_BUCKET_report_representatives_v36.tsv`
- `S_BUCKET_report_representatives_v37.tsv`
- `S_BUCKET_report_representatives_v38.tsv`
- `S_BUCKET_report_representatives_v39.tsv`
- `S_BUCKET_report_representatives_v40.tsv`
- `S_BUCKET_report_representatives_v41.tsv`
- `S_BUCKET_report_representatives_v42.tsv`
- `S_BUCKET_report_representatives_v43.tsv`
- `S_BUCKET_report_representatives_v44.tsv`
- `S_BUCKET_report_representatives_v45.tsv`
- `S_BUCKET_report_representatives_v46.tsv`
- `S_BUCKET_report_representatives_v47.tsv`
- `S_BUCKET_report_representatives_v48.tsv`
- `S_BUCKET_report_representatives_v49.tsv`
- `S_BUCKET_batch1_round3_function_core_manifest_v1.tsv`
- `S_BUCKET_KIMI_batch1_round3_function_core_prompt_v1.txt`
- `S_BUCKET_batch1_round3_function_core_README_v1.md`
- `S_BUCKET_KIMI_batch1_round3_function_core_direct_message_v1.txt`
- `S_BUCKET_功能归类最小框架_v1.md`
- `S_BUCKET_功能映射表_v1.tsv`
- `S_BUCKET_KIMI_batch1_prompt_v1.txt`
- `S_BUCKET_KIMI_batch1_priority_read_prompt_v1.txt`
- `S_BUCKET_stage_proof__01_集合竞价教程__v1.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v1.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v2.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v3.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v4.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v5.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v6.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v7.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v8.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v9.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v10.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v11.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v12.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v13.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v14.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v15.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v16.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v17.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v18.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v19.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v20.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v21.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v22.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v23.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v24.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v25.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v26.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v27.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v28.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v29.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v30.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v31.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v32.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v33.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v34.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v35.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v36.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v37.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v38.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v39.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v40.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v41.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v42.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v43.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v44.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v45.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v46.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v47.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v48.tsv`
- `S_BUCKET_stage_proof__03_券商研报__representatives_v49.tsv`
