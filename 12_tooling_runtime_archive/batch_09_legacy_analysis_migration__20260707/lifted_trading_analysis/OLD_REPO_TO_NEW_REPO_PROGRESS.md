# Old Repo To New Repo Progress

更新时间：2026-07-03

ARCHIVE_ONLY: 本文件仅用于历史迁移进度回溯；旧根路径只保留为历史锚点，不作为当前默认入口或可复制执行命令

## 这份文件是干嘛的

- 这份文件站在旧仓库 `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis` 的视角，记录：
  - 哪些内容已经平移到新仓库 `D:\Stock\trading_assistant`
  - 哪些内容只是部分平移
  - 哪些内容当前还没动
- 这不是按文件数量精确计算的百分比，而是按“迁移阶段状态”看的进度条。

## 总体状态

- 旧仓库角色：
  - 继续保留为历史大仓库、旧路径锚点、历史证据保留层
- 新仓库角色：
  - 未来主工作根
  - 只接收已筛选、已说明、已定责的内容

## 当前新主线

- 当前新主线不是“先全量吃透，再考虑迁移”，而是：
  - 一边继续全量吃透旧仓库
  - 一边继续把值得长期维护的内容迁入新仓库
  - 一边趁这轮把旧主文档中的重复结论和冗余过程压掉
- 当前规划锚点：
  - `00_entry\MAINLINE_FULL_INGEST_AND_MIGRATION_PLAN__2026-06-26.md`
- 当前并行重点：
  - 旧主文档第二轮清理已完成，`12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_trading_analysis/00/01/02/03/关于日活` 已切到兼容入口与最小历史锚点口径
  - `04_active_main_docs\batch_01_selected` 已稳定承接 `00/01/02/03/关于日活/PLAYBOOK/ashare_daily_ops`，正文级镜像同步也已完成
  - `20_tools_workspace` 已形成 `batch_01~06` 的可维护批次，`PY-04 = tk_r6~r8` 三组手工表工具已正式迁入
  - `12_tooling_runtime_archive` 已形成 `batch_01~03`，`batch_02_mt_indicator_family` 已继续扩到 `MT5SymbolDumpProbe.mq5/.ex5` 这类可复用导出探针
  - `10_source_library_archive` 已形成 `mirror_kimi_inbox`、`raw_assets\S` 与 `batch_01_youzi_truth_anchors` 三层承接，说明来源库已不再只是“空壳规划”
  - 2026-07-03 已重新实扫旧仓库：总文件 `15226`，其中 `csv=11093`、`md=1366`、`pdf=532`、`py=260`、`ps1=62`、`mq4=53`、`ex4=52`；一级目录仍以 `backtest_out=10862`、`10_来源库_SOURCE_LIBRARY=2188`、`12_工具运行时_TOOLING_RUNTIME=1488` 为主
  - 每批同步旧库进度板、旧库任务板、新库镜像说明，并把“剩余批次/退出条件”继续写硬
- 当前主线任务：
  - 旧仓迁移有限批次已归零，当前只保留维护态同步
  - 继续维持 `S_BUCKET` 的 `13` 个锚点与 `A/F` 第二阶段状态表的 repo-first 真值入口
  - 删源、树外目录处理与显式批准动作都留在 `OLD_REPO_FROZEN_MAINTENANCE_ONLY` 之后
  - 每轮只在需要时同步任务板 / 进度板 / `MAINLINE`，不再把已完成批次重写成未完成

## 总体进度条

- 总体迁移状态：`[#######---] 约 68%`
- 说明：
  - 已把新仓库骨架、主入口、首批活跃对象、首批归档层、主文档镜像层、`.trae` 可见集、`tools` 的 `R6/R7/R8` 代表批次，以及 `MT` 工程化主线搭起来
  - 但来源库正文大头、旧主文档第二轮正文级镜像、旧 `tools` 长尾和高风险根脚本、旧 `TOOLING_RUNTIME` 非最小工程集仍未整批迁完

## 已平移到新库

### 1. 新仓库基础骨架

- 进度：`[##########] 100%`
- 状态：`DONE`
- 已完成：
  - `00_entry`
  - `01_active_objects`
  - `02_runtime`
  - `03_docs`
  - `04_active_main_docs`
  - `10_source_library_archive`
  - `11_frozen_summaries_archive`
  - `12_tooling_runtime_archive`
  - `20_tools_workspace`
  - `21_trae_system_archive`

### 2. DY-R1 / KD_MTF_P0 活跃对象

- 进度：`[##########] 100%`
- 状态：`DONE`
- 已完成：
  - 对象层
  - runtime 层
  - docs 层
  - proof builder
  - `--target-bar-time`
  - `--persist`

### 3. 根目录主文档首批

- 进度：`[##########] 100%`
- 状态：`DONE`
- 已平移：
  - `00_主线检索索引.md`
  - `01_阶段一_项目记录_过去与落地.md`
  - `02_阶段二_工作方向_想法库.md`
  - `03_阶段二_当下计划_执行清单.md`
  - `关于日活.md`
  - `PLAYBOOK_滚动模板.md`
  - `ashare_daily_ops.md`

### 4. `.trae` 首批与第二批

- 进度：`[########--] 80%`
- 状态：`DONE_FOR_VISIBLE_SET__RECOVERY_AND_PROMPT_SYNCED`
- 已平移：
  - `recover_01/02/03`
  - `recover_about`
  - `p0-exec-evidence-officer_PROMPT.md`
- 已补新仓库副本：
  - `artifact-provenance-note-guard-cn`

### 5. 工具脚本首批与第二批

- 进度：`[########--] 85%`
- 状态：`IN_PROGRESS__SELECTED_BATCHES_SYNCED`
- 已平移：
  - `generate_p0_subset.py`
  - `relocate_path_prefix.py`
  - `slice_csv_tail_v1.py`
  - `tk_manual_append_rows.py`
  - `group08` 主流水线 `6` 个脚本
  - `tk_r6_make_manual_sheet.py` / `tk_r6_summarize_manual_sheet.py`
  - `tk_r7_make_manual_sheet.py` / `tk_r7_summarize_manual_sheet.py`
  - `tk_r8_make_manual_sheet.py` / `tk_r8_summarize_manual_sheet.py`

### 6. 工具运行时首批与第二批

- 进度：`[########--] 85%`
- 状态：`IN_PROGRESS__MT_AND_TEMPLATE_BATCHES_SYNCED`
- 已平移：
  - `cross_line_frozen` 顶层最小冻结链
  - `MT 指标家族最小工程集`
  - `Volty / XBreaking` 运行时批次包
  - `MT4` 便携探针最小模板批次
  - `MT5SymbolDumpProbe.mq5` / `MT5SymbolDumpProbe.ex5` 及其编译日志

## 部分平移

### 7. 冻结总结层

- 进度：`[#####-----] 50%`
- 状态：`PARTIAL`
- 已完成：
  - 首批总结锚点已迁入新仓库
- 还没完成：
  - 不是整层都迁了
  - 仍有大量旧冻结材料只留在旧仓库

### 8. 来源库

- 进度：`[###-------] 35%`
- 状态：`PARTIAL__MIRROR_AND_RAW_ASSETS_READY`
- 已完成：
  - 新仓库已建 `10_source_library_archive`
  - 已写迁移规则、任务板和批次流程
  - 已形成 `mirror_kimi_inbox` 的稳定入口层
  - 已形成 `raw_assets\S` 的 repo 内承接层
  - 已形成 `batch_01_youzi_truth_anchors` 的首批真值锚点批次
- 还没完成：
  - 还没有真正大批量把来源库正文主体迁入新仓库
  - `A* / F*` 的大体量原件仍主要留在外部重资产层
  - 当前仍以“先扫清作用、再决定是否迁入”为主，不做整包复制

### 9. 旧仓库 skill 副本策略

- 进度：`[####------] 40%`
- 状态：`PARTIAL__VISIBLE_SET_AND_PROMPTS_SYNCED`
- 已完成：
  - `artifact-provenance-note-guard-cn` 已在新仓库建副本
  - `recover_01/02/03/about` 已在 `21_trae_system_archive\batch_01_selected` 承接
  - `p0-exec-evidence-officer_PROMPT.md` 已在 `21_trae_system_archive\batch_02_selected` 承接
- 还没完成：
  - `dev-guardrails`
  - `rolling-playbook-cn`
  - `mt-indicator-engineering-cn`

### 10. 旧 tools / py 全场扫库

- 进度：`[########--] 85%`
- 状态：`IN_PROGRESS`
- 已完成：
  - 已建立新仓库任务板：
    - `trading_assistant\00_entry\OLD_REPO_FILE_SWEEP_TASKBOARD.md`
  - 已完成 `PY-03 / PY-04` 首轮细扫：
    - `trading_assistant\00_entry\OLD_REPO_FILE_SWEEP_PY03_PY04_NOTES.md`
  - 已完成 `PY-03` 首批正式平移：
    - `trading_assistant\20_tools_workspace\batch_03_general_ingest_tools\s_bucketize.py`
    - `trading_assistant\20_tools_workspace\batch_03_general_ingest_tools\ingest_ashare_txt_to_md.py`
    - `trading_assistant\20_tools_workspace\batch_03_general_ingest_tools\kimi_cutpack_manifest.py`
    - 批次备注：`trading_assistant\20_tools_workspace\batch_03_general_ingest_tools\BATCH_03_TOOL_NOTES.md`
  - 已完成 `PY-04` 的 `R6` 首批正式平移：
    - `trading_assistant\20_tools_workspace\batch_04_tk_r6_manual_sheet_tools\tk_r6_make_manual_sheet.py`
    - `trading_assistant\20_tools_workspace\batch_04_tk_r6_manual_sheet_tools\tk_r6_summarize_manual_sheet.py`
    - 批次备注：`trading_assistant\20_tools_workspace\batch_04_tk_r6_manual_sheet_tools\BATCH_04_TOOL_NOTES.md`
  - 已完成 `PY-04` 的 `R7` 首批正式平移：
    - `trading_assistant\20_tools_workspace\batch_05_tk_r7_manual_sheet_tools\tk_r7_make_manual_sheet.py`
    - `trading_assistant\20_tools_workspace\batch_05_tk_r7_manual_sheet_tools\tk_r7_summarize_manual_sheet.py`
    - 批次备注：`trading_assistant\20_tools_workspace\batch_05_tk_r7_manual_sheet_tools\BATCH_05_TOOL_NOTES.md`
  - 已完成 `PY-04` 的 `R8` 首批正式平移：
    - `trading_assistant\20_tools_workspace\batch_06_tk_r8_manual_sheet_tools\tk_r8_make_manual_sheet.py`
    - `trading_assistant\20_tools_workspace\batch_06_tk_r8_manual_sheet_tools\tk_r8_summarize_manual_sheet.py`
    - 批次备注：`trading_assistant\20_tools_workspace\batch_06_tk_r8_manual_sheet_tools\BATCH_06_TOOL_NOTES.md`
- 当前已明确优先迁入候选：
  - `PY-03` 其余通用整理工具与后续低耦合脚本
  - 需要先补作用卡再决定去留的高风险根脚本

### 10A. 旧主文档清理

- 进度：`[##########] 100%`
- 状态：`DONE_FOR_COMPAT_ENTRY_AND_MIRROR_SYNC`
- 当前未完成主线：
  - `NONE`
- 已完成：
  - 已建立旧仓库主文档清理任务板：
    - `OLD_MAIN_DOC_CLEANUP_TASKBOARD.md`
  - 已把 `00/01/02/03/关于日活` 补入首轮“当前合同层”短块
  - 已把“旧仓库全量吃透做到哪里”统一压成：至少推进到 `Batch 36`
  - 已把 `cut_file` 的 `S` 主战场进一步拆成 repo 内状态表：
    - `trading_assistant\00_entry\S_BUCKET_REPO_STATE_TABLE__2026-06-26.md`
  - 已开始明确 `S桶` 的源文件子集：`stage proof` 源文件已在 repo 的 `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\S_BUCKET__staging\`（`49+408=457` files），`cut_file` 角色收缩为未入仓主体原件与读取位
  - 已把 `02_游资悟道交割单` 从外部重资产层继续拆成：
    - `YZ-A = 退学炒股心法三件套`
    - `YZ-B = 赵老哥 / 著名刺客 单体风格锚点组`
  - 已把 `YZ-A / YZ-B` 的主题簇对照结论压短回写到新库 `S_BUCKET_02` 顶层段落（不并旧卡号）
  - 已把 `cut_file A* / F*` 的“外部只留重资产、repo 内有稳定入口的不回外部当默认入口”口径补进退场计划
  - 已把 `12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_trading_analysis/00/01/02/03` 收成兼容入口与最小历史锚点
  - 已把 `04_active_main_docs/batch_01_selected/00/01/02/03/关于日活` 的正文级镜像同步收口
  - 已把迁移进度板 / 清理任务板 / `MAINLINE` 收成 `remaining_batches_count=0 / remaining_actions_count=0`
  - 已把 `01` 的 `Batch 16-18 / 19-23 / 24-35 / 36` 压成组级事实结论，并同步到 `04_active_main_docs/batch_01_selected/01`
  - 已把旧库 `00/01/02` 与镜像 `00/01/02` 的当前默认阅读顺序、边界短块和导航结构继续写硬；其中 `00` 已把 `NFTRADEZ / S_BUCKET` 压成短导航块，`01` 已把 `Batch 8 / 9A-15` 的重复中间停点压回组级追溯事实，并把 `GROUP_08` 后的 `Kimi / S桶` 长段压成 `独立化边界 / batch1 四包 / NFTRADEZ 双包 / backlog 与 GROUP_08 锚点` 四组事实块
  - 已把 `F1 / F2 / A2 / A5` 补成 `A* / F*` 第一版第二阶段分区状态表草案，并把 `A3 / A4 / A1` 补到“组级入口/组级边界/组级下一刀 + 是否细拆判定”短表
  - 已继续加厚 `YZ-A` 的旧冻结层同主题证据表（等待/停手/风险与仓位上限/回撤触发/系统性风险应对/弱势禁忌不交易等行号证据增强），使主题簇级对照更可对账
  - 已在新仓库来源库层建立首批批次壳：
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\README.md`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\youzi_truth_anchor_manifest_v1.tsv`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_A_MIN_EXCERPT_EXECUTION_BOARD__2026-06-26.md`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_A01_MIN_EXCERPTS__2026-06-26.md`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_A02_MIN_EXCERPTS__2026-06-26.md`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_A03_MIN_EXCERPTS__2026-06-26.md`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_A_TO_OLD_MXX_MAPPING_CHECK__2026-06-26.md`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_A_THEME_CLUSTER_MAPPING__2026-06-26.tsv`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_A_OLD_FROZEN_THEME_EVIDENCE__2026-06-26.tsv`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_A_TO_OLD_FROZEN_THEME_ALIGNMENT_CHECK__2026-06-26.md`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_B_MIN_READ_PLAN__2026-06-26.md`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_B01_MIN_EXCERPTS__2026-06-26.md`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_B02_MIN_EXCERPTS__2026-06-26.md`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_B03_MIN_EXCERPTS__2026-06-26.md`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_B04_MIN_EXCERPTS__2026-06-26.md`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_B_GROUP_SUMMARY__2026-06-26.md`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_B_THEME_CLUSTER_MAPPING__2026-06-26.tsv`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_B_OLD_FROZEN_THEME_EVIDENCE__2026-06-26.tsv`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_B_TO_OLD_FROZEN_THEME_ALIGNMENT_CHECK__2026-06-26.md`
  - 已完成 `YZ-A01/A02/A03` 与旧冻结层 `Mxx` 的显式映射检查：
    - 当前结论：`NO_EXPLICIT_MAPPING_FOUND_YET`
    - 当前继续保留 `YZ-A` 为对象级真值锚点，不强行并卡号
  - 已把 `YZ-A` 的主题簇映射与旧冻结层同主题证据表落盘（仍不并旧卡号）：
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_A_THEME_CLUSTER_MAPPING__2026-06-26.tsv`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_A_OLD_FROZEN_THEME_EVIDENCE__2026-06-26.tsv`
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_A_TO_OLD_FROZEN_THEME_ALIGNMENT_CHECK__2026-06-26.md`
  - 已把 `YZ-B03 = 著名刺客语录` 推进到首批真实摘录卡：
    - 当前已落 `4` 条最小摘录
    - `YZ-B` 不再只是候选阅读计划
  - 已把 `YZ-B01 = A股题材炒作的本质（赵老哥著）` 推进到首批真实摘录卡：
    - 当前已从 `epub` 落 `4` 条最小摘录
  - 已把 `YZ-B02 = 【赵老哥】悟道心法` 推进到首批真实摘录卡：
    - 当前已从 `pdf` 落 `4` 条最小摘录
  - 已把 `YZ-B04 = 著名刺客新生代游资著名刺客手法揭秘 PDF文章` 推进到首批真实摘录卡：
    - 当前已从 `pdf` 落 `4` 条最小摘录
  - `YZ-B` 当前已具备四张对象级真值锚点：`YZ-B01 / YZ-B02 / YZ-B03 / YZ-B04`
  - 已把 `YZ-B` 的主题簇映射证据落盘：
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_B_THEME_CLUSTER_MAPPING__2026-06-26.tsv`
  - 已把 `YZ-B` 每簇旧冻结层同主题证据表落盘（仍不并旧卡号）：
    - `trading_assistant\10_source_library_archive\batch_01_youzi_truth_anchors\YZ_B_OLD_FROZEN_THEME_EVIDENCE__2026-06-26.tsv`
- 当前目标：
  - 把 `00/01/02/03/关于日活` 压成“当前合同层 + 历史追溯层 + 已完成批次索引 + 下一步”
  - 再继续压掉错误、冗余、被后续覆盖的旧过程段
  - 同时把 `cut_file` 退场路线从主线说明升级成专门执行卡
  - `YZ-A/YZ-B` 的主题簇对照证据链已落盘，下一刀继续压 `03/关于日活` 顶层重复段，并把 `YZ-A` 对照结论也压成“可复用旧事实”回写到 `S_BUCKET_02`

## 当前没动或继续留旧仓库

### 11. 根目录高风险脚本

- 进度：`[----------] 0%`
- 状态：`KEEP_OLD_FROZEN`
- 当前不动：
  - `backtest_p0.py`
  - `mt5_exit_assistant.py`
  - `ashare_preprocess.py`
- 原因：
  - 风险高
  - 默认行为复杂
  - 需要先补作用卡和边界说明

### 12. TK-R1 ~ TK-R4 审计家族

- 进度：`[----------] 0%`
- 状态：`KEEP_OLD_FROZEN`
- 当前不动：
  - `tk_r1_*`
  - `tk_r2_*`
  - `tk_r3_*`
  - `tk_r4_*`
- 原因：
  - 强绑定旧 `backtest_out`
  - 强绑定旧 `backtest_p0`
  - 现在不是新仓库最优先承接对象

### 13. Batch9 reopen / pv_corr / rsj 家族

- 进度：`[##--------] 20%`
- 状态：`OLD_REPO_FROZEN_MAINTENANCE_ONLY__WITH_P0_TRIAGE_IN_PROGRESS`
- 当前状态：
  - 旧库侧默认动作已切到“维护态抽查”：只保留 `ARCHIVE_ONLY` 入口壳与可复核清单
  - 新仓侧已承接关键结论与入口回指：主线合同层以 `04_active_main_docs/batch_01_selected/00_主线检索索引.md` 为准
  - 后续只做：逐份人工过眼尚未抽到的 archive 壳，继续压平残留“可续跑/默认入口”话术

## 已经明确“不简单复制”的规则

- 看到旧文件，不直接复制
- 先判断：
  - 作用是否明确
  - 来源是否明确
  - 当前还会不会维护
  - 该放新仓库哪里
- 当前统一处理动作只有四种：
  - `COPY_WITH_NOTE`
  - `NEW_IN_NEW_REPO`
  - `MOVE_LATER_AFTER_REF_CHECK`
  - `KEEP_OLD_FROZEN`

## 当前下一步

- 下一刀不是继续泛泛扫，而是：
  - 先继续压旧主文档的当前合同层与历史追溯层边界，仍按 `01 -> 02 -> 00` 推进
  - 同时把 `cut_file` 三阶段退场路线继续写进新旧仓库入口和任务板，并维持 `F1/F2/A2/A5` 独立块 + `A3/A4/A1` 轻量子组状态
  - 同时把 `S_BUCKET` 最小回迁批次草案固定为 `13` 个锚点，并继续把 `YZ-A / YZ-B` 保持为对象级真值锚点
  - 同时把迁移文件改成“剩余批次数 + 剩余动作数 + 退出条件”可直接读取的有限收口口径
  - 每完成一批，就同步回写旧仓库进度板、旧库任务板和新仓库入口

## 迁移有限计数

- `legacy_migration_current_state_v1=IN_PROGRESS__FINITE_COUNTERS_ACTIVE`
- `legacy_migration_remaining_batches=old_main_docs_round2_tail|active_main_docs_body_sync_tail|source_library_stage2_minimal_return_batch|tools_long_tail_and_high_risk_role_cards`
- `legacy_migration_remaining_batches_count=4`
- `legacy_migration_remaining_actions=complete_active_main_docs_body_sync|stabilize_s_bucket_13_anchor_return_batch|keep_A_F_stage2_tables_in_sync`
- `legacy_migration_remaining_actions_count=3`
- `legacy_migration_exit_criteria=remaining_batches_count=0_and_remaining_actions_count=0=>OLD_REPO_FROZEN_MAINTENANCE_ONLY`
- `legacy_migration_batch_notes_v1=old_main_docs_round2_tail=legacy_01_02_00_second_round_prune|active_main_docs_body_sync_tail=batch_01_selected_body_level_sync|source_library_stage2_minimal_return_batch=s_bucket_13_anchor_plus_A_F_stage2_tables|tools_long_tail_and_high_risk_role_cards=py03_tail_plus_backtest_p0_mt5_exit_assistant_ashare_preprocess`

## 一句话记忆

- 旧仓库不是要一下子搬空；当前策略是：先把新仓库搭成可长期维护的主工作根，再按作用清晰度分批平移旧仓库内容。
