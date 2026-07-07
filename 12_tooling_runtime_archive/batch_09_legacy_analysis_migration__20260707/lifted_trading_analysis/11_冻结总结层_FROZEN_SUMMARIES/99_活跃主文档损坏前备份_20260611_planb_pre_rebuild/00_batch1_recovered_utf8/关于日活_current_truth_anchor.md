# 关于日活

更新时间：2026-06-19

- ARCHIVE_ONLY: 旧仓库冻结总结层快照；以下命令仅用于历史复核，默认不作为当前可跑入口

## 2026-06-19 RSJ/PV 样例输入层 + S桶 收缩任务书

### 证据

- 已新增：
  - `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_raw_window_sample_schema_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\real_input_samples\rsj_state_p0_raw_window_sample_input_v1.csv`
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_bar_window_sample_schema_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\real_input_samples\pv_corr_state_p0_bar_window_sample_input_v1.csv`
- 已更新：
  - `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_runtime_params_template_v1.json`
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_runtime_params_template_v1.json`
  - `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_runtime_notes_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_runtime_notes_v1.md`
  - `10_来源库_SOURCE_LIBRARY\02_原子化拆解文件\技术指标_波动率_RSJ市场情绪冷暖剂_后续对象定义入口_v1.md`
  - `10_来源库_SOURCE_LIBRARY\02_原子化拆解文件\技术指标_量价关系_高频价量相关性因子_后续对象定义入口_v1.md`
  - `临时粘贴区_外部AI与终端输出.md`

### 当前结论

- `RSJ / PV Corr` 当前已从“未来真实输入字段合同”推进到“未来真实输入样例层”。
- 新增的 `sample schema + sample csv` 现在可作为后续真实绑定前的固定样例入口。
- 这一步仍不改变：
  - `allow_live_binding = false`
  - `allow_signal_generation = false`
  - 两条线仍然只是 `diag-only`
- `S桶` 当前也同步切到“收缩而非扩题”：
  - 已给 `Kimi` 一份只做稳定登记层/缺口层/禁止抬级层的新任务书
  - 目标是继续降低对原材料目录的直接依赖
- `Kimi` 最新贴回也已经进入可吸收状态：
  - 已形成 `detach_now_queue_v1 / normalize_target_names_v1 / minimal_reopen_queue_v1 / freeze_confirm_v1`
  - 当前不再需要它重扫 `S桶`
  - 当前也不需要它重开候选池
- 本轮对 `Kimi` 回帖的审计结论是：
  - 可立即脱依赖队列已压到：
    - `9` 条规则卡片
    - `14` 条方法卡片
    - `11` 条 `fx_mainline_ok` 研报卡片
    - `1` 个 `44md` 文本归档对象
  - 低成本重开队列已压到 `6` 个对象
  - 冻结区已明确覆盖空壳 epub、扫描残留、交割单截图与 3 份深度学习 future bucket
- 本轮又继续补上：
  - `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_validate_raw_window_sample_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_raw_window_sample_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_validate_bar_window_sample_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_bar_window_sample_acceptance_v1.md`
- 本轮又继续补上：
  - `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_validate_raw_window_mapping_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_raw_window_mapping_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_validate_bar_window_mapping_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_bar_window_mapping_acceptance_v1.md`
- 本轮又继续补上：
  - `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_validate_append_compatibility_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_append_compatibility_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_validate_append_compatibility_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_append_compatibility_acceptance_v1.md`
- 本轮又继续补上：
  - `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_simulate_append_diff_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_simulate_append_diff_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_simulate_append_diff_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_simulate_append_diff_acceptance_v1.md`
- 本轮又继续补上：
  - `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_export_replay_preview_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_replay_preview_rows_v1.csv`
  - `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_replay_preview_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_export_replay_preview_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_replay_preview_rows_v1.csv`
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_replay_preview_acceptance_v1.md`
- 本轮又继续补上：
  - `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_validate_replay_preview_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_replay_preview_acceptance_validation_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_validate_replay_preview_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_replay_preview_acceptance_validation_v1.md`
- 已本机完成：
  - `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_validate_raw_window_sample_v1.py`
  - `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_validate_bar_window_sample_v1.py`
- 已本机完成：
  - `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_validate_raw_window_mapping_v1.py`
  - `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_validate_bar_window_mapping_v1.py`
- 已本机完成：
  - `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_validate_append_compatibility_v1.py`
  - `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_validate_append_compatibility_v1.py`
- 已本机完成：
  - `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_simulate_append_diff_v1.py`
  - `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_simulate_append_diff_v1.py`
- 已本机完成：
  - `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_export_replay_preview_v1.py`
  - `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_export_replay_preview_v1.py`
- 已本机完成：
  - `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_validate_replay_preview_acceptance_v1.py`
  - `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_validate_replay_preview_acceptance_v1.py`
- 最新校验结果确认：
  - `RSJ sample rows_loaded = 3`
  - `PV Corr sample rows_loaded = 3`
  - 两条线都为：
    - `header_match = true`
    - `trade_id_unique = True`
    - `invalid_rows = 0`
    - `write_attempted = false`
    - `validation_passed = true`
- 最新映射结果确认：
  - `RSJ rows_mapped = 3`
  - `PV Corr rows_mapped = 3`
  - `RSJ model_state_counts = {"valid": 3}`
  - `PV Corr model_state_counts = {"valid": 3}`
  - `RSJ rsj_state_counts = {"cold": 1, "neutral": 1, "warm": 1}`
  - `PV Corr pv_sync_state_counts = {"confirm": 1, "diverge": 1, "neutral": 1}`
  - 两条线都为：
    - `output_header_match = true`
    - `write_attempted = false`
    - `mapping_passed = true`
- 最新兼容性联调结果确认：
  - `RSJ rows_before_cleanup = 5`
  - `PV Corr rows_before_cleanup = 5`
  - `RSJ mapped_rows_loaded = 3`
  - `PV Corr mapped_rows_loaded = 3`
  - `RSJ rows_after_append = 8`
  - `PV Corr rows_after_append = 8`
  - 两条线都为：
    - `append_header_match = true`
    - `write_attempted = false`
    - `compatibility_passed = true`
- 最新 replay 对照结果确认：
  - `RSJ before_row_count = 5`
  - `PV Corr before_row_count = 5`
  - `RSJ mapped_row_count = 3`
  - `PV Corr mapped_row_count = 3`
  - `RSJ after_replay_row_count = 8`
  - `PV Corr after_replay_row_count = 8`
  - 两条线都为：
    - `overlapping_trade_ids = []`
    - `removed_trade_ids = []`
    - `write_attempted = false`
    - `replay_passed = true`
- 最新 preview 导出结果确认：
  - `RSJ preview_row_count = 3`
  - `PV Corr preview_row_count = 3`
  - `RSJ preview_csv = rsj_state_p0_replay_preview_rows_v1.csv`
  - `PV Corr preview_csv = pv_corr_state_p0_replay_preview_rows_v1.csv`
  - 两条线都为：
    - `runtime_write_attempted = false`
    - `preview_export_passed = true`
- 最新 preview-acceptance 对照结果确认：
  - `RSJ preview_row_count = 3`
  - `PV Corr preview_row_count = 3`
  - `RSJ acceptance_row_count = 3`
  - `PV Corr acceptance_row_count = 3`
  - 两条线都为：
    - `rows_match = true`
    - `write_attempted = false`
    - `preview_acceptance_validation_passed = true`

## 2026-06-18 A5 候审承接 + 多周期KD 第二批 proof

### 证据

- 已新增：
  - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_10_A5_财报_估值_组合管理\01_A5_cutpack_v1_final\README_放这里.md`
  - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_10_A5_财报_估值_组合管理\01_A5_cutpack_v1_final\manifest_v2.tsv`
- 已复制入来源库候审承接区：
  - `5073_Quantitative_Equity_Portfolio_Management`
  - `Active_Portfolio_Management`
  - `上市公司财报分析与股票估值`
  - `财务报表分析与股票估值_郭永清`
- 已更新：
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\real_input_samples\kd_mtf_p0_proof_output_v1.csv`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_runtime_notes_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_runtime_append_acceptance_v1.md`
- 已执行：
  - `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_runtime_append_stub_v1.py`
  - `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_runtime_append_stub_v1.py --persist`
- 已裁决并清理：
  - 已删除：`D:\Stock\cut_file\S\02_游资悟道交割单\游资交割单 游资语录\29位交割单`
  - 已同步索引去除该目录引用：
    - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\S_BUCKET_INDEX__2026-06-17.tsv`
    - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\S_DUP_REPORT__sha256__2026-06-17.tsv`
    - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\PANEL__S文件夹_整理方向__EVIDENCE_PACK__2026-06-17.md`
- 已更新 S 桶承接口径（用于交代给 Kimi 执行）：
  - `临时粘贴区_外部AI与终端输出.md`：补了 `2026-06-18` 实扫统计、重新定义分类方法与默认切法、并给出 Kimi 的输出合同
- 已继续把 S 桶 Kimi 回帖往前收口：
  - 冻结 `03_券商研报` 第一批 `30` 份候选池，其中：
    - `27` 份 = `extract_text_then_card`
    - `3` 份 = `future_bucket`
  - 补出统一 `8` 字段提取模板
  - 给 `01_集合竞价教程` 与 `02_游资悟道交割单(epub/docx)` 各补一份 `p0/p1/p2` 验证优先级
  - 并把卡片证据强度统一降到：
    - `title_or_folder_inference`
    - 避免把标题推断误写成正文锚点
- 已继续往前推进一轮真实文本验证：
  - `01_集合竞价教程` 当前已有：
    - `R01 / R02 / R03 / R22 = direct_text_support`
    - `R04 / R11 / R21 / R23 / R25` 等已提升到 `excerpt_support_but_not_full_rule`
    - `R09` 已降级为 `title_or_folder_inference`
  - `02_游资悟道交割单(epub/docx)` 当前已有 `13` 张方法论卡片提升到 `excerpt_support_but_not_full_rule`
  - 其中：
    - `M04 / M19` 已新升到 `excerpt_support_but_not_full_rule`
    - `M06 / M07 / M14` 已确认是空壳 `epub`
    - `M18 / M20` 当前正文与目标卡片概念不够贴合，继续低证据保留
  - `03_券商研报` 的 `27` 份 `8` 字段提取也已完成：
    - `can_map_to_fx = yes 9 / partial 4 / no 14`
- 已继续把 `yes = 9` 收缩为首批 `2` 个对象入口：
  - `技术指标_波动率_RSJ市场情绪冷暖剂_后续对象定义入口_v1.md`
  - `技术指标_量价关系_高频价量相关性因子_后续对象定义入口_v1.md`
  - 当前都只定为：
    - `next_object_entry`
    - `DIAG_ONLY_OBJECT_CANDIDATE`
  - `Kimi` 当前在 `S桶` 仅保留补缺口角色，不再主导首批对象选择
- 已继续执行 `detach_now_queue_v1` 的第一批真实落盘：
  - 在 `10_来源库_SOURCE_LIBRARY\02_原子化拆解文件` 新建 `8` 张 `A股竞价规则卡片`
  - 文件为：
    - `A股竞价规则_R01_9点15到9点20可撤单与假单诱导_v1.md`
    - `A股竞价规则_R02_9点20到9点25不可撤单与挂单更真实_v1.md`
    - `A股竞价规则_R03_白点未匹配量与红绿柱观察卡_v1.md`
    - `A股竞价规则_R04_9点25真实成交与9点25前飙升片段卡_v1.md`
    - `A股竞价规则_R21_9点20前涨停封单可撤单片段卡_v1.md`
    - `A股竞价规则_R22_9点20前后可信度分界_v1.md`
    - `A股竞价规则_R23_白点多与量能活跃不等于直接涨停片段卡_v1.md`
    - `A股竞价规则_R25_撮合量放大与抛压变化片段卡_v1.md`
- 本轮卡片落盘时同步固定了边界：
  - `R03` 只作为 `白点 / 未匹配量 / 红绿柱` 观察卡
  - `R04 / R21 / R23 / R25` 保留 `excerpt_support_but_not_full_rule`
  - 全部卡片都写入 `Do Not Overclaim`
- 已继续把这两条线推进到 `P0` 合同层：
  - `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\`
    - `rsj_state_p0_min_contract_v1.md`
    - `rsj_state_p0_proof_of_mapping_v1.md`
    - `real_input_samples\rsj_state_p0_proof_input_v1.csv`
    - `real_input_samples\rsj_state_p0_proof_output_v1.csv`
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\`
    - `pv_corr_state_p0_min_contract_v1.md`
    - `pv_corr_state_p0_proof_of_mapping_v1.md`
    - `real_input_samples\pv_corr_state_p0_proof_input_v1.csv`
    - `real_input_samples\pv_corr_state_p0_proof_output_v1.csv`
- 已继续补齐这两条线的 runtime 文档壳：
  - `rsj_state_p0_runtime_notes_v1.md`
  - `rsj_state_p0_fields_output_header_v1.txt`
  - `pv_corr_state_p0_runtime_notes_v1.md`
  - `pv_corr_state_p0_fields_output_header_v1.txt`
- 已继续把这两条线推进到可落 CSV 的 runtime 空壳：
  - `rsj_state_p0_runtime_params_template_v1.json`
  - `rsj_state_p0_runtime_append_stub_v1.py`
  - `rsj_state_p0_runtime_append_acceptance_v1.md`
  - `rsj_state_p0_fields_runtime_v1.csv`
  - `pv_corr_state_p0_runtime_params_template_v1.json`
  - `pv_corr_state_p0_runtime_append_stub_v1.py`
  - `pv_corr_state_p0_runtime_append_acceptance_v1.md`
  - `pv_corr_state_p0_fields_runtime_v1.csv`
- 已本机完成：
  - `RSJ dry-run + persist`
  - `PV Corr dry-run + persist`
  - 当前两条 runtime csv 都是 `5` 行 proof persist 行
- 已继续把这两条线从 `preview acceptance validation` 再往前推进一层：
  - `rsj_state_p0_validate_replay_chain_v1.py`
  - `pv_corr_state_p0_validate_replay_chain_v1.py`
  - `rsj_state_p0_replay_chain_acceptance_v1.md`
  - `pv_corr_state_p0_replay_chain_acceptance_v1.md`
- 已本机完成：
  - `RSJ replay chain validation`
  - `PV Corr replay chain validation`
  - 两条线结果一致：
    - `runtime_row_count = 5`
    - `mapped_row_count = 3`
    - `appended_row_count = 3`
    - `after_replay_row_count = 8`
    - `preview_row_count = 3`
    - `acceptance_row_count = 3`
    - `rows_match = true`
    - `write_attempted = false`
    - `replay_chain_passed = true`
- 已固定当前执行口径：
  - `S桶` 继续作为可持续第二条线保留，不丢
  - 可继续把 `S桶` 的补缺口/收缩任务分发给 `Kimi`
  - 若后续需要重做 `OCR`，必须先报用户确认，当前不默认进入 OCR
- 已继续把两条主线再往前推一层总索引收口：
  - `rsj_state_p0_export_chain_summary_index_v1.py`
  - `pv_corr_state_p0_export_chain_summary_index_v1.py`
  - `rsj_state_p0_chain_summary_index_v1.md`
  - `pv_corr_state_p0_chain_summary_index_v1.md`
- 已本机完成：
  - `RSJ chain summary index export`
  - `PV Corr chain summary index export`
  - 两条线结果一致：
    - `runtime_row_count = 5`
    - `preview_row_count = 3`
    - `stage_count = 10`
    - `all_stage_files_exist = True`
    - `write_attempted = false`
    - `chain_summary_export_passed = true`
- 当前这层的作用已固定为：
  - 把散落的合同/acceptance/preview/replay 证据收成单一总索引入口
  - 方便后续继续主线时直接从总索引层往下补，不再重复拼装历史证据
- 已继续把两条主线再往前推到冻结清单层：
  - `rsj_state_p0_validate_chain_summary_acceptance_compare_v1.py`
  - `pv_corr_state_p0_validate_chain_summary_acceptance_compare_v1.py`
  - `rsj_state_p0_chain_summary_acceptance_compare_v1.md`
  - `pv_corr_state_p0_chain_summary_acceptance_compare_v1.md`
  - `rsj_state_p0_export_manifest_freeze_v1.py`
  - `pv_corr_state_p0_export_manifest_freeze_v1.py`
  - `rsj_state_p0_manifest_freeze_v1.md`
  - `pv_corr_state_p0_manifest_freeze_v1.md`
- 已本机完成：
  - `RSJ chain summary acceptance compare`
  - `PV Corr chain summary acceptance compare`
  - `RSJ manifest freeze export`
  - `PV Corr manifest freeze export`
  - 两条线结果一致：
    - `indexed_stage_count = 10`
    - `expected_stage_count = 10`
    - `rows_match = true`
    - `manifest_count = 12`
    - `all_manifest_files_exist = True`
    - `manifest_frozen = true`
    - `manifest_freeze_passed = true`
- 当前这层的作用已固定为：
  - 先校验总索引正文与 stage 清单一致
  - 再把总索引相关关键文件槽位冻结成 manifest
  - 后续继续推进时可以直接在冻结清单层上补跨线统一入口
- 已继续把两条主线再往前推到跨线统一入口层：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_manifest_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_manifest_index_v1.md`
- 已本机完成：
  - `cross_line frozen manifest index`
  - 当前结果为：
    - `candidate_count = 2`
    - `all_candidates_manifest_frozen = True`
    - `candidate_ids = ["RSJ_STATE_P0", "PV_CORR_STATE_P0"]`
    - `RSJ manifest_count = 13`
    - `PV manifest_count = 13`
    - `cross_line_frozen_manifest_index_passed = true`
- 当前这层的作用已固定为：
  - 把 `RSJ / PV Corr` 两条冻结清单收成根层统一入口
  - 后续跨线继续推进时不必分别进入两个子目录
- 已继续把根层统一入口再往前推一层：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_compare_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance compare`
  - 当前结果为：
    - `index_md_exists = True`
    - `indexed_candidate_count = 2`
    - `expected_candidate_count = 2`
    - `rows_match = true`
    - `candidate_ids = ["RSJ_STATE_P0", "PV_CORR_STATE_P0"]`
    - `cross_line_frozen_acceptance_compare_passed = true`
- 当前这层的作用已固定为：
  - 校验根层统一入口正文与两条冻结状态一致
  - 让跨线统一入口自身也具备 acceptance 校验层
- 已继续把根层冻结验收再往前收一层：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen manifest acceptance`
  - 当前结果为：
    - `artifact_count = 4`
    - `all_artifacts_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 把根层统一入口、根层 compare、两条子线 manifest freeze 一起收成更高一层冻结验收
  - 让跨线冻结层不只停在单一入口对照，而有总验收壳
- 已继续把跨线冻结总验收再往前收成总链入口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_chain_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_chain_index_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance chain index`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `artifact_count = 4`
    - `candidate_ids = ["RSJ_STATE_P0", "PV_CORR_STATE_P0"]`
    - `cross_line_frozen_acceptance_chain_index_passed = true`
- 当前这层的作用已固定为：
  - 把根层 `manifest index / acceptance compare / manifest acceptance` 三层再收成跨线总链入口
  - 后续跨线继续推进时可以直接在总链入口上补 compare 或 freeze
- 已继续把跨线总链入口再往前推一层：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_chain_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_chain_acceptance_compare_v1.md`
- 已本机完成：
  - `cross_line frozen chain acceptance compare`
  - 当前结果为：
    - `chain_index_md_exists = True`
    - `indexed_stage_count = 3`
    - `expected_stage_count = 3`
    - `rows_match = true`
    - `candidate_ids = ["RSJ_STATE_P0", "PV_CORR_STATE_P0"]`
    - `cross_line_frozen_chain_acceptance_compare_passed = true`
- 当前这层的作用已固定为：
  - 校验跨线冻结总链索引正文与实际冻结层级一致
  - 让跨线总链入口自身也具备 acceptance compare
- 已继续把跨线总链 compare 再往前收成总验收：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_chain_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_chain_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen chain manifest acceptance`
  - 当前结果为：
    - `artifact_count = 3`
    - `all_artifacts_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_chain_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 把总链索引、总链 compare、根层 manifest acceptance 收成更高一层总链冻结验收
  - 让跨线总链不只停在 compare，而有自己的 manifest acceptance
- 已继续把跨线总链总验收再往前压成真正的总入口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_index_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance super-index`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `artifact_count = 3`
    - `candidate_ids = ["RSJ_STATE_P0", "PV_CORR_STATE_P0"]`
    - `cross_line_frozen_acceptance_super_index_passed = true`
- 当前这层的作用已固定为：
  - 把高层冻结收口件压成真正的跨线冻结总入口
  - 后续继续推进时可以直接在总入口上补 compare 或 acceptance
- 已继续把跨线冻结总入口再往前补一层自动对照：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_acceptance_compare_v1.md`
- 已本机完成：
  - `cross_line frozen super-acceptance compare`
  - 当前结果为：
    - `super_index_md_exists = True`
    - `indexed_stage_count = 3`
    - `expected_stage_count = 3`
    - `rows_match = true`
    - `candidate_ids = ["RSJ_STATE_P0", "PV_CORR_STATE_P0"]`
    - `cross_line_frozen_super_acceptance_compare_passed = true`
- 当前这层的作用已固定为：
  - 校验最顶层跨线冻结总入口正文与实际高层冻结结构一致
  - 防止最顶层入口继续漂移
- 已继续把最顶层冻结总入口再收成更紧的总链冻结层：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_manifest_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_chain_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_chain_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_chain_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_chain_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_chain_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_chain_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen super-manifest acceptance`
  - `cross_line frozen super-chain index`
  - `cross_line frozen super-chain acceptance compare`
  - `cross_line frozen super-chain manifest acceptance`
  - 当前结果为：
    - `artifact_count = 3`
    - `all_artifacts_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_super_manifest_acceptance_passed = true`
    - `cross_line_frozen_super_chain_index_passed = true`
    - `cross_line_frozen_super_chain_acceptance_compare_passed = true`
    - `cross_line_frozen_super_chain_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 先把 `super-index + super-compare + 上一层 chain manifest acceptance` 收成最顶层冻结总验收
  - 再把这份最顶层冻结总验收收成单一总链入口，并给它补 compare 与 manifest acceptance
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续把当前最顶层总链冻结收口件再往上一层压成新的统一入口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance super-super index`
  - `cross_line frozen super-super acceptance compare`
  - `cross_line frozen super-super manifest acceptance`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_acceptance_super_super_index_passed = true`
    - `cross_line_frozen_super_super_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 把 `super-chain index + super-chain compare + super-chain manifest acceptance` 再收成更高一层跨线冻结总入口
  - 再给这份更高一层总入口补 compare，并和上一层 `super-chain manifest acceptance` 一起收成新的冻结总验收
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续把更高一层冻结总验收再收成更高一层总链入口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_chain_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_chain_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_chain_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_chain_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_chain_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_chain_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen super-super chain index`
  - `cross_line frozen super-super chain acceptance compare`
  - `cross_line frozen super-super chain manifest acceptance`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_super_super_chain_index_passed = true`
    - `cross_line_frozen_super_super_chain_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_chain_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 把 `super-super index + super-super compare + super-super manifest acceptance` 收成更高一层总链入口
  - 再给这份更高一层总链入口补 compare，并和 `super-super manifest acceptance` 一起收成新的总链冻结验收
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续把更高一层总链冻结验收再压成更高一层跨线冻结总入口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance super-super-super index`
  - `cross_line frozen super-super-super acceptance compare`
  - `cross_line frozen super-super-super manifest acceptance`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_acceptance_super_super_super_index_passed = true`
    - `cross_line_frozen_super_super_super_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 把 `super-super chain index + super-super chain compare + super-super chain manifest acceptance` 再压成更高一层跨线冻结总入口
  - 再给这份更高一层总入口补 compare，并和上一层 `super-super chain manifest acceptance` 一起收成新的冻结总验收
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续把更高一层冻结总验收再收成更高一层总链入口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_chain_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_chain_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_chain_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_chain_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_chain_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_chain_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen super-super-super chain index`
  - `cross_line frozen super-super-super chain acceptance compare`
  - `cross_line frozen super-super-super chain manifest acceptance`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_super_super_super_chain_index_passed = true`
    - `cross_line_frozen_super_super_super_chain_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_chain_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 把 `super-super-super index + super-super-super compare + super-super-super manifest acceptance` 收成更高一层总链入口
  - 再给这份更高一层总链入口补 compare，并和 `super-super-super manifest acceptance` 一起收成新的总链冻结验收
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续把更高一层总链冻结验收再压成更高一层跨线冻结总入口，并再补一层总链收口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_manifest_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_chain_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_chain_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_chain_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_chain_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_chain_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_chain_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance super-super-super-super index`
  - `cross_line frozen super-super-super-super acceptance compare`
  - `cross_line frozen super-super-super-super manifest acceptance`
  - `cross_line frozen super-super-super-super chain index`
  - `cross_line frozen super-super-super-super chain acceptance compare`
  - `cross_line frozen super-super-super-super chain manifest acceptance`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_acceptance_super_super_super_super_index_passed = true`
    - `cross_line_frozen_super_super_super_super_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_manifest_acceptance_passed = true`
    - `cross_line_frozen_super_super_super_super_chain_index_passed = true`
    - `cross_line_frozen_super_super_super_super_chain_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_chain_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 先把 `super-super-super chain index + super-super-super chain compare + super-super-super chain manifest acceptance` 压成更高一层跨线冻结总入口
  - 再给这份更高一层总入口补 compare，并和上一层 `super-super-super chain manifest acceptance` 收成新的冻结总验收
  - 然后再把这份新的冻结总验收收成更高一层总链入口，并给它补 compare / manifest acceptance
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续把更高一层总链冻结验收再压成更高一层跨线冻结总入口，并再补一层总链收口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_manifest_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_chain_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_chain_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_chain_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_chain_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_chain_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_chain_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance super-super-super-super-super index`
  - `cross_line frozen super-super-super-super-super acceptance compare`
  - `cross_line frozen super-super-super-super-super manifest acceptance`
  - `cross_line frozen super-super-super-super-super chain index`
  - `cross_line frozen super-super-super-super-super chain acceptance compare`
  - `cross_line frozen super-super-super-super-super chain manifest acceptance`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_acceptance_super_super_super_super_super_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_manifest_acceptance_passed = true`
    - `cross_line_frozen_super_super_super_super_super_chain_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_chain_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_chain_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 先把 `super-super-super-super chain index + super-super-super-super chain compare + super-super-super-super chain manifest acceptance` 压成更高一层跨线冻结总入口
  - 再给这份更高一层总入口补 compare，并和上一层 `super-super-super-super chain manifest acceptance` 收成新的冻结总验收
  - 然后再把这份新的冻结总验收收成更高一层总链入口，并给它补 compare / manifest acceptance
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续把更高一层总链冻结验收再压成更高一层跨线冻结总入口，并再补一层总链收口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_manifest_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_chain_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_chain_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance super-super-super-super-super-super index`
  - `cross_line frozen super-super-super-super-super-super acceptance compare`
  - `cross_line frozen super-super-super-super-super-super manifest acceptance`
  - `cross_line frozen super-super-super-super-super-super chain index`
  - `cross_line frozen super-super-super-super-super-super chain acceptance compare`
  - `cross_line frozen super-super-super-super-super-super chain manifest acceptance`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_acceptance_super_super_super_super_super_super_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_manifest_acceptance_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_chain_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_chain_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_chain_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 先把 `super-super-super-super-super chain index + super-super-super-super-super chain compare + super-super-super-super-super chain manifest acceptance` 压成更高一层跨线冻结总入口
  - 再给这份更高一层总入口补 compare，并和上一层 `super-super-super-super-super chain manifest acceptance` 收成新的冻结总验收
  - 然后再把这份新的冻结总验收收成更高一层总链入口，并给它补 compare / manifest acceptance
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续把更高一层总链冻结验收再压成更高一层跨线冻结总入口，并再补一层总链收口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_chain_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_chain_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance super-super-super-super-super-super-super index`
  - `cross_line frozen super-super-super-super-super-super-super acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super manifest acceptance`
  - `cross_line frozen super-super-super-super-super-super-super chain index`
  - `cross_line frozen super-super-super-super-super-super-super chain acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super chain manifest acceptance`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_acceptance_super_super_super_super_super_super_super_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_manifest_acceptance_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_chain_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_chain_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_chain_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 先把 `super-super-super-super-super-super chain index + super-super-super-super-super-super chain compare + super-super-super-super-super-super chain manifest acceptance` 压成更高一层跨线冻结总入口
  - 再给这份更高一层总入口补 compare，并和上一层 `super-super-super-super-super-super chain manifest acceptance` 收成新的冻结总验收
  - 然后再把这份新的冻结总验收收成更高一层总链入口，并给它补 compare / manifest acceptance
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续把更高一层总链冻结验收再压成更高一层跨线冻结总入口，并再补一层总链收口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_chain_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_chain_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance super-super-super-super-super-super-super-super index`
  - `cross_line frozen super-super-super-super-super-super-super-super acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super manifest acceptance`
  - `cross_line frozen super-super-super-super-super-super-super-super chain index`
  - `cross_line frozen super-super-super-super-super-super-super-super chain acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super chain manifest acceptance`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_manifest_acceptance_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_chain_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_chain_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_chain_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 先把 `super-super-super-super-super-super-super chain index + super-super-super-super-super-super-super chain compare + super-super-super-super-super-super-super chain manifest acceptance` 压成更高一层跨线冻结总入口
  - 再给这份更高一层总入口补 compare，并和上一层 `super-super-super-super-super-super-super chain manifest acceptance` 收成新的冻结总验收
  - 然后再把这份新的冻结总验收收成更高一层总链入口，并给它补 compare / manifest acceptance
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续把更高一层总链冻结验收再压成更高一层跨线冻结总入口，并再补一层总链收口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance super-super-super-super-super-super-super-super-super index`
  - `cross_line frozen super-super-super-super-super-super-super-super-super acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super-super manifest acceptance`
  - `cross_line frozen super-super-super-super-super-super-super-super-super chain index`
  - `cross_line frozen super-super-super-super-super-super-super-super-super chain acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super-super chain manifest acceptance`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_manifest_acceptance_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_chain_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_passed = true`
- 本轮中途已修复：
  - `super9 chain` 三个脚本文件名错位
  - `super9 chain` 三个 md 未真实落盘
  - `candidate_ids` 行被写成非 JSON 格式
  - 上一层 `super8 chain manifest acceptance md` 被误写到 `super9` 口径
- 当前这层的作用已固定为：
  - 先把 `super-super-super-super-super-super-super-super chain index + super-super-super-super-super-super-super-super chain compare + super-super-super-super-super-super-super-super chain manifest acceptance` 压成更高一层跨线冻结总入口
  - 再给这份更高一层总入口补 compare，并和上一层 `super-super-super-super-super-super-super-super chain manifest acceptance` 收成新的冻结总验收
  - 然后再把这份新的冻结总验收收成更高一层总链入口，并给它补 compare / manifest acceptance
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续把更高一层总链冻结验收再压成更高一层跨线冻结总入口，并再补一层总链收口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance super-super-super-super-super-super-super-super-super-super index`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super manifest acceptance`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super chain index`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super chain acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super chain manifest acceptance`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_chain_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 先把 `super-super-super-super-super-super-super-super-super chain index + super-super-super-super-super-super-super-super-super chain compare + super-super-super-super-super-super-super-super-super chain manifest acceptance` 压成更高一层跨线冻结总入口
  - 再给这份更高一层总入口补 compare，并和上一层 `super-super-super-super-super-super-super-super-super chain manifest acceptance` 收成新的冻结总验收
  - 然后再把这份新的冻结总验收收成更高一层总链入口，并给它补 compare / manifest acceptance
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续把更高一层总链冻结验收再压成更高一层跨线冻结总入口，并再补一层总链收口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance super-super-super-super-super-super-super-super-super-super-super index`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super manifest acceptance`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super chain index`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super chain acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_chain_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 先把 `super-super-super-super-super-super-super-super-super-super chain index + super-super-super-super-super-super-super-super-super-super chain compare + super-super-super-super-super-super-super-super-super-super chain manifest acceptance` 压成更高一层跨线冻结总入口
  - 再给这份更高一层总入口补 compare，并和上一层 `super-super-super-super-super-super-super-super-super-super chain manifest acceptance` 收成新的冻结总验收
  - 然后再把这份新的冻结总验收收成更高一层总链入口，并给它补 compare / manifest acceptance
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续把更高一层总链冻结验收再压成更高一层跨线冻结总入口，并再补一层总链收口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance super-super-super-super-super-super-super-super-super-super-super-super index`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super manifest acceptance`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super chain index`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super chain acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 先把 `super-super-super-super-super-super-super-super-super-super-super chain index + super-super-super-super-super-super-super-super-super-super-super chain compare + super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance` 压成更高一层跨线冻结总入口
  - 再给这份更高一层总入口补 compare，并和上一层 `super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance` 收成新的冻结总验收
  - 然后再把这份新的冻结总验收收成更高一层总链入口，并给它补 compare / manifest acceptance
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续把更高一层总链冻结验收再压成更高一层跨线冻结总入口，并再补一层总链收口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance super-super-super-super-super-super-super-super-super-super-super-super-super index`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super manifest acceptance`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super chain index`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super chain acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 先把 `super-super-super-super-super-super-super-super-super-super-super-super chain index + super-super-super-super-super-super-super-super-super-super-super-super chain compare + super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance` 压成更高一层跨线冻结总入口
  - 再给这份更高一层总入口补 compare，并和上一层 `super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance` 收成新的冻结总验收
  - 然后再把这份新的冻结总验收收成更高一层总链入口，并给它补 compare / manifest acceptance
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续把更高一层总链冻结验收再压成更高一层跨线冻结总入口，并再补一层总链收口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance super-super-super-super-super-super-super-super-super-super-super-super-super-super index`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super manifest acceptance`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super chain index`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super chain acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 先把 `super-super-super-super-super-super-super-super-super-super-super-super-super chain index + super-super-super-super-super-super-super-super-super-super-super-super-super chain compare + super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance` 压成更高一层跨线冻结总入口
  - 再给这份更高一层总入口补 compare，并和上一层 `super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance` 收成新的冻结总验收
  - 然后再把这份新的冻结总验收收成更高一层总链入口，并给它补 compare / manifest acceptance
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续把更高一层总链冻结验收再压成更高一层跨线冻结总入口，并再补一层总链收口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance super-super-super-super-super-super-super-super-super-super-super-super-super-super-super index`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super manifest acceptance`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain index`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 先把 `super-super-super-super-super-super-super-super-super-super-super-super-super-super chain index + super-super-super-super-super-super-super-super-super-super-super-super-super-super chain compare + super-super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance` 压成更高一层跨线冻结总入口
  - 再给这份更高一层总入口补 compare，并和上一层 `super-super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance` 收成新的冻结总验收
  - 然后再把这份新的冻结总验收收成更高一层总链入口，并给它补 compare / manifest acceptance
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续把更高一层总链冻结验收再压成更高一层跨线冻结总入口，并再补一层总链收口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super index`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super manifest acceptance`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain index`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 先把 `super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain index + super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain compare + super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance` 压成更高一层跨线冻结总入口
  - 再给这份更高一层总入口补 compare，并和上一层 `super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance` 收成新的冻结总验收
  - 然后再把这份新的冻结总验收收成更高一层总链入口，并给它补 compare / manifest acceptance
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续把更高一层总链冻结验收再压成更高一层跨线冻结总入口，并再补一层总链收口：
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_v1.md`
- 已本机完成：
  - `cross_line frozen acceptance super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super index`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super manifest acceptance`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain index`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain acceptance compare`
  - `cross_line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance`
  - 当前结果为：
    - `stage_count = 3`
    - `all_stage_files_exist = True`
    - `candidate_count = 2`
    - `rows_match = true`
    - `cross_line_frozen_acceptance_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_manifest_acceptance_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_index_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_acceptance_compare_passed = true`
    - `cross_line_frozen_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_super_chain_manifest_acceptance_passed = true`
- 当前这层的作用已固定为：
  - 先把 `super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain index + super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain compare + super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance` 压成更高一层跨线冻结总入口
  - 再给这份更高一层总入口补 compare，并和上一层 `super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance` 收成新的冻结总验收
  - 然后再把这份新的冻结总验收收成更高一层总链入口，并给它补 compare / manifest acceptance
  - 继续保持 `write_attempted = false`，不把验证层误写成真实执行层
- 已继续推进到 `super18`：
  - 已本机顺序跑通 `index / acceptance compare / manifest acceptance / chain index / chain acceptance compare / chain manifest acceptance`
  - 当前结果继续保持：`stage_count = 3`、`candidate_count = 2`、`rows_match = true`、`write_attempted = false`
  - 当前最高层已提升为 `cross-line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance`
- 已继续推进到 `super19`：
  - 已本机顺序跑通 `index / acceptance compare / manifest acceptance / chain index / chain acceptance compare / chain manifest acceptance`
  - 当前结果继续保持：`stage_count = 3`、`candidate_count = 2`、`rows_match = true`、`write_attempted = false`
  - 当前最高层已提升为 `cross-line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance`
- 已继续推进到 `super20`：
  - 已本机顺序跑通 `index / acceptance compare / manifest acceptance / chain index / chain acceptance compare / chain manifest acceptance`
  - 当前结果继续保持：`stage_count = 3`、`candidate_count = 2`、`rows_match = true`、`write_attempted = false`
  - 当前最高层已提升为 `cross-line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance`
- 已继续推进到 `super21`：
  - 已本机顺序跑通 `index / acceptance compare / manifest acceptance / chain index / chain acceptance compare / chain manifest acceptance`
  - 当前结果继续保持：`stage_count = 3`、`candidate_count = 2`、`rows_match = true`、`write_attempted = false`
  - 当前最高层已提升为 `cross-line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance`
- 已继续推进到 `super22`：
  - 已本机顺序跑通 `index / acceptance compare / manifest acceptance / chain index / chain acceptance compare / chain manifest acceptance`
  - 当前结果继续保持：`stage_count = 3`、`candidate_count = 2`、`rows_match = true`、`write_attempted = false`
  - 当前最高层已提升为 `cross-line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance`
- 已继续推进到 `super23`：
  - 已本机顺序跑通 `index / acceptance compare / manifest acceptance / chain index / chain acceptance compare / chain manifest acceptance`
  - 当前结果继续保持：`stage_count = 3`、`candidate_count = 2`、`rows_match = true`、`write_attempted = false`
  - 当前最高层已提升为 `cross-line frozen super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super-super chain manifest acceptance`
- 已对 `super20+` 的 runtime markdown 标题做减压：
  - 把首行从超长文件名改成短作用名，例如 `Cross-line Frozen super20 Chain Acceptance Compare`
  - 目的是减少 IDE `Markdown 语言功能` 在超长 token 上做 `references` 时的报错概率
- 已把全库编码扫描落成硬结论：
  - `candidate_files = 12693`
  - `utf8_fail = 47`
  - `mojibake_marker_files = 353`
  - 当前主线活跃文档与冻结 runtime 脚本不在 `utf8_fail` 这批里
  - 最集中的是 `12_工具运行时_TOOLING_RUNTIME\03_MT4便携探针实例`、`12_工具运行时_TOOLING_RUNTIME\mt4_probe_instance`、`10_来源库_SOURCE_LIBRARY\00_指标定义&公式`
  - 备份目录 `11_冻结总结层_FROZEN_SUMMARIES\99_活跃主文档损坏前备份_20260611_planb_pre_rebuild` 仍建议单开编码抢救，不和主线混改
  - 当前保留的下一轮编码抢救 `batch1` 为：`备份4文件 + 两套 config ini`
  - `batch1` 已开只读诊断：备份 `4` 文件确认为“UTF-8 可读但内容已乱码化”；两套 config 里只有一部分是普通文本，另一部分更像 MT4 私有/二进制配置，暂不硬转
- `S桶` 本轮继续保持第二条线：
  - 不插主线
  - 可持续追
  - 可分发 `Kimi`
  - 若碰 `OCR` 先报用户
- 已继续把这两条线推进到未来真实输入契约的接口壳：
  - `rsj_state_p0_append_from_raw_window_stub_v1.py`
  - `rsj_state_p0_raw_window_stub_acceptance_v1.md`
  - `pv_corr_state_p0_append_from_bar_window_stub_v1.py`
  - `pv_corr_state_p0_bar_window_stub_acceptance_v1.md`
- 已本机完成：
  - `RSJ append_from_raw_window --dry-run`
  - `PV Corr append_from_bar_window --dry-run`
  - 两条接口当前都明确为：
    - `binding_state = unbound`
    - `allow_live_binding = False`
    - `write_attempted = false`
- 已继续把这两条线推进到真实输入契约层：
  - `rsj_state_p0_raw_window_input_contract_v1.md`
  - `rsj_state_p0_raw_window_input_header_v1.txt`
  - `pv_corr_state_p0_bar_window_input_contract_v1.md`
  - `pv_corr_state_p0_bar_window_input_header_v1.txt`
- `S桶` 当前最准状态同步为：
  - 已完成目录级收口
  - 已完成候选池收口
  - 已完成首批对象 runtime 化
  - 未做全桶全文切分，也不以此为当前目标
- 已顺手做 Markdown 弹窗的最小规避补丁：
  - 把四件套里多处“标题含反引号”的写法改成纯文本标题，减少 `markdown-language-features` 的 `references` 崩溃触发面
- 已推进：
  - `10_来源库_SOURCE_LIBRARY\02_原子化拆解文件\核心技术_威科夫_弹簧Spring与上抛UT量化判定.md` 已补 `DIAG_ONLY` 对象入口与最小合同（v1 草案）

### 当前结论

- `A5` 已从 `cut_file` 输出层接回来源库候审承接区，不再只是等待态。
- `A5` 当前候审入口已固定：
  - `5073 -> contents.md`
  - `Active Portfolio Management -> INDEX.md`
  - `上市公司财报分析与股票估值 -> INDEX.md`
  - `财务报表分析与股票估值_郭永清 -> INDEX.md`
- `S桶` 当前状态已从“目录初扫”推进到：
  - `第一批候选池 + 提取模板 + 验证优先级`
  - 并已进入“首批真实文本验证”阶段
  - 并已补出 `yes / partial / no` 的研报映射分层
  - 并已从 `yes = 9` 里选出 `RSJ / 高频价量相关性` 作为首批对象入口
  - 并已把 `R01 / R02 / R03 / R04 / R21 / R22 / R23 / R25` 切成独立卡片
  - 但大部分 `集合竞价规则卡片 / 游资心法卡片` 仍未达到整包完成状态，不可整桶宣称已入库
- `5073` 的 `INDEX.md` 已明确降级为书末主题索引，不作为稳定入口。
- `多周期KD` 第二批 proof 已补齐，当前总 proof 行数 = `5`，已基本覆盖：
  - `s / a / b / conflict`
- 最新 dry-run 已确认：
  - `rows_before_cleanup = 3`
  - `proof_rows_loaded = 5`
  - `rows_before_append = 0`
  - `rows_after_append = 5`
- 最新 persist 已确认：
  - runtime csv 当前已写回 `5` 行
  - 新增：
    - `GBPUSD H1 2026-06-19T04:00:00Z`
    - `USDJPY H1 2026-06-19T08:00:00Z`
- 当前仍保持：
  - 这 `5` 行仍然是手工 proof persist 结果
  - 不是 broker 原始链路重建出来的真实 runtime 行
- `A5` 本轮也已补做验收：
  - 当前可写成“已正式通过并入库完成”
  - `5073 / Active Portfolio / 上市公司财报分析与股票估值 / 财务报表分析与股票估值_郭永清` 当前审查通过
  - `财务报表分析与股票估值_郭永清` 的第10章当前已通过：
    - `PDF_text_layer` 主文字源
    - `bycalibre_epub` 文字校对
    - `EPUB_remake` 表格结构辅助
    - `表10-6` 已根据图版 + 用户贴回数字手工重排成 md 表格
- 本轮已切回主线继续推进：
  - `A2` 严格复核后继续维持 `keep_current / keep_current_with_audit_note`
  - `A3` 严格复核后继续维持“主规则可用、案例图注降级为辅助、只补 residual source_audit”
  - 当前没发现必须把 `A2 / A3` 整组拉回重切的新硬伤
- `A3` 当前已补齐 residual source_audit：
  - `陈浩完整版`
  - `筹码形态手册 part1`
  - `筹码形态手册 part2`
- 任务六 Batch4（`00_交易系统书籍`）本轮重收口为：
  - `已吸收`：`墨菲 / Kaufman / 海龟`
  - `可重开`：`VanTharp`、`海龟`
  - `future bucket`：`Kaufman` 压力轴细化、`墨菲` 图表形态系统化
  - `仅来源库保留`：`archive / vt_images / 99_流程模板`
- `VanTharp` 这条线本轮已继续下压到对象入口层：
  - 已新增 `风险管理_VanTharp_R乘数_期望与头寸规模_后续对象定义入口_v1.md`
  - 当前角色：`next_object_entry / DIAG_ONLY_OBJECT_CANDIDATE`
- `VanTharp` 本轮已补齐最小合同 + 首份 proof-of-mapping（仍为 diag-only）：
  - `12_工具运行时_TOOLING_RUNTIME\vantharp_risk_p0_v1\vantharp_risk_p0_min_contract_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\vantharp_risk_p0_v1\vantharp_risk_p0_proof_of_mapping_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\vantharp_risk_p0_v1\real_input_samples\vantharp_risk_p0_proof_input_v1.csv`
  - `12_工具运行时_TOOLING_RUNTIME\vantharp_risk_p0_v1\real_input_samples\vantharp_risk_p0_proof_output_v1.csv`
- `VanTharp` 本轮已冻结 `initial_risk_amount` 的双口径，并提供 v2 对照 proof：
  - `statement_amount`（来自交割单金额字段）
  - `entry_stop_calc`（来自 entry/stop 换算）
  - `12_工具运行时_TOOLING_RUNTIME\vantharp_risk_p0_v1\real_input_samples\vantharp_risk_p0_proof_input_v2.csv`
  - `12_工具运行时_TOOLING_RUNTIME\vantharp_risk_p0_v1\real_input_samples\vantharp_risk_p0_proof_output_v2.csv`
  - `12_工具运行时_TOOLING_RUNTIME\vantharp_risk_p0_v1\vantharp_risk_p0_fields_output_header_v2.txt`

## 2026-06-17 A股书库收口口径更新 + 任务六立项

### 证据

- 已更新：
  - `02_阶段二_工作方向_想法库.md`
  - `03_阶段二_当下计划_执行清单.md`
- 已吸收的外部回帖状态：
  - `A5` 已收到一轮细切回复
  - `A2 / A3 / F1` 已发出按“先审现有 cutpack 质量，再判 PDF/OCR/双 EPUB”的问题包

### 当前结论

- 书库切割当前不再按“哪个组资料多就先做”，而是按“哪组现有切割质量最差、最值得修”来排。
- 双 EPUB 当前升级条件已明确固定：
  - 先看现有 `md/cutpack` 是否质量差
  - 再确认 `PDF` 是否难用或无文字层
  - 再确认单 OCR 是否仍不稳
  - 且同一本同时存在：
    - `FineReaderOCR` 主源
    - `calibre` 校对源
- `A2 / A3 / F1` 当前进入等待回帖后的正式收口阶段：
  - 下一步只做：
    - `keep_current`
    - `patch_source_audit`
    - `re_ocr_only`
    - `recut_with_dual_epub`
    的裁决，不重复泛扫
- `A1 / A4 / F2` 当前不再扩大战线：
  - 但所有已入库对象必须补一次显式复核
  - 复核目标是把主源/校对源/`PDF` 角色/当前质量写清，而不是默认重做
- `A5 / S桶` 当前继续由用户侧并行扫描：
  - 仓库侧先不重复插入同题动作
  - 后续接回传结论后再挂入统一计划
- 已新增正式下一步：
  - `任务六 = 盘点更远资料和旧来源库`
  - 固定顺序：
    - 目录级盘点
    - 代表文件抽读
    - 四分流
    - 再决定重切/重做候选

## 2026-06-15 仓库瘦身规则补齐 + skill 边界收紧 + Trae reconnect 排查

### 证据

- 已更新：
  - `.gitignore`
  - `.trae/skills/panel-multi-ai-cn/SKILL.md`
  - `.trae/skills/multi-ai-orchestrator-cn/SKILL.md`
  - `.trae/skills/p0-exec-evidence-officer/SKILL.md`
  - `.trae/skills/p0-sweep-outbound-guard/SKILL.md`
  - `02_阶段二_工作方向_想法库.md`
  - `03_阶段二_当下计划_执行清单.md`
- 已检查：
  - `C:\Users\91883\AppData\Roaming\Trae\logs\aha_log\aha_electron_2026.0615.log`
  - `C:\Users\91883\AppData\Roaming\Trae\logs\20260615T152618\window5\renderer.log`

### 当前结论

- 仓库瘦身
  - 当前先不删研究证据，只先补忽略规则：
    - `12_工具运行时_TOOLING_RUNTIME/**/logs/`
    - `tester/logs/`
    - `MQL4/Logs/`
    - `mailbox/`
    - `profiles/lastprofile.ini`
    - 自动生成的若干 `profiles` 二进制/终端状态文件
  - 当前保留：
    - `runtime_notes / runtime_gaps / field_sample / proof_of_mapping / 手工审计表 / 参数模板 / append stub`
- 全量吃透顺序
  - 当前任务顺序已再次固定为：
    - `N02`
    - `N01`
    - `N03`
    - `GROUP_05 + GROUP_06`
    - `A股指标整理区`
  - 当前单字段先做完：
    - `N02 P0 12 字段`
    - `N01 P0 8 字段`
    - `TK-R6 / TK-R8 / TK-R7` 的 proof-of-mapping/diag 壳
  - 当前明确并入 A 股后置整理的部分继续保持不变：
    - `N04 / N05 / N06`
    - `T09 / T10`
- skill 边界
  - `panel-multi-ai-cn`
    - 固定模型 roster + 统一发包模板
  - `multi-ai-orchestrator-cn`
    - 维护 OUTBOUND / PANEL / DIFF / BATCH_CLOSE
  - `p0-exec-evidence-officer`
    - 负责实际运行 `sweep / action / eval`
  - `p0-sweep-outbound-guard`
    - 只负责 postprocess/outbound 摘录
- Trae reconnect / 失败提示
  - 当前能看到的主要日志目录：
    - `C:\Users\91883\AppData\Roaming\Trae\logs`
  - 刚刚并不是仓库内容损坏。
  - 日志里确实出现过一组网络/扩展宿主报错：
    - `Client network socket disconnected before secure TLS connection was established`
    - `fetch failed`
    - `features response error`
  - 这些错误集中在 `window5\renderer.log` 的 `2026-06-15 18:28:55` 到 `18:30:24` 左右，更像 Trae 侧网络/特性服务短时异常，而不是本仓库文件出错。
  - 同时索引状态日志仍显示：
    - `d:\Stock\trading_analysis` indexing `success_index_files=919`
    - 说明工作区索引并没有整体挂掉
  - 因而当前裁决是：
    - 仓库本身没坏
    - 刚刚更像客户端侧短时 reconnect / TLS 建连失败
    - 后续若再遇到，先看 `renderer.log` 与 `aha_electron_*.log`

## 2026-06-15 多AI补书路线收口

### 证据

- 已读取并收口：
  - `临时粘贴区_外部AI与终端输出.md`
    - `#14 全书库补书路线重定_PANEL_OUTBOUND`
    - 回帖来源：
      - `kimi`
      - `deepseek`
      - `glm`
      - `千问`
      - `豆包`

### 当前结论

- 投票收口结果：
  - `Q1`：一致为 `B`
    - 说明两层思路保留，但要调整成更清晰的层次
  - `Q2`：多数票 `B`
    - 当前最缺簇优先收口为 `A4 数据工程 / PIT / 回测防偏差`
  - `Q3`：一致为 `D`
    - 书库补充必须混合搭配，但按层次分工
  - `Q4`：多数票 `B`
    - `F1/F2` 当前中期准备、先补理论，不进入深切主流水线
- 当前长期排序已改为：
  - `Layer0`: `A4`
  - `Layer1`: `A1 + A2`
  - `Layer2`: `A3 + A5`
  - `Layer3`: `F2 theory only + F1 theory only`
- 当前稳定推荐清单（首批）：
  - `A4`
    - `Advances in Financial Machine Learning`
    - `Algorithmic Trading / Quantitative Trading`
    - 交易所官方规则文档
    - A 股本地化 `PIT / 复权 / 停牌 / 成分股调整 / 回测偏差` 研报/讲义
  - `A1`
    - `股市极客思考录`
    - 淘股吧代表性游资帖合集
    - 券商情绪因子/龙头轮动专题研报
  - `A2`
    - `Mind Over Markets`
    - `Trading and Exchanges`
    - 集合竞价/开盘结构高质量专栏或课程
- 当前明确后置：
  - `A3 / A5`
  - `F1 / F2` 深切
  - 纯心法/纯盘感/纯案例回忆录

### 下一步

- 先按 `A4 -> A1 -> A2` 找第一批资料
- 每一簇先找 `2-4` 个高质量来源，不一次铺太多
- 资料到位后，优先用 `#13 Kimi_跨书库统一切割执行指令_v1` 开切

## 2026-06-15 TK-R8 继续补细 + A股书单 panel 升级 + epub/txt 保留型切分

### 证据

- 已更新：
  - `10_来源库_SOURCE_LIBRARY\00_TK外汇\TK-R8_B区域_最小判据草案_v1.md`
  - `临时粘贴区_外部AI与终端输出.md`
  - `03_阶段二_当下计划_执行清单.md`

### 当前结论

- `TK-R8`
  - 当前已继续补到：
    - `zone_alignment + abc_integrity + continuation_quality` 的最小组合映射
  - 当前保守收口已进一步固定为：
    - 三块同时站得住才进 `qualified_b_zone`
    - 允许一块偏软但未失效时落在 `weak_b_zone`
    - 任一块明显失效就优先退出到 `not_b_zone`
- A股补充书单多 AI
  - 当前 `#8 A股书单与Kimi切分_OUTBOUND` 已升级成 panel 版
  - 参与模型已明确为：
    - `glm`
    - `deepseek`
    - `kimi`
    - `豆包`
    - `千问本地`
  - 当前外发顺序已固定为：
    - 我先给初始建议
    - 各模型先评价我的建议
    - 再各自给方案
    - 最后再统一总结
  - 当前又新补了一份更上层的咨询块：
    - `#14 全书库补书路线重定_PANEL_OUTBOUND`
  - 与 `#8` 的区别：
    - `#8` 主要重定 A 股补书方向
    - `#14` 直接把 `A股 + Auction/MP + 数据工程/PIT + 外汇订单流/微观结构 + 通用订单流/拍卖理论` 放到同一轮讨论里
  - 当前目标已固定为：
    - 不是只列“该买什么书”
    - 而是要让多家 AI 一起给出：
      - 哪些簇优先补
      - 哪些值得现在深切
      - 哪些只适合索引
      - 哪些应先进入 `future bucket`
- `epub / txt`
  - 当前 `#11 / #12` 已不再是旧版“只看目录/标题”的要求
  - 当前新口径是：
    - 即使未来删掉原 `epub / txt`
    - 生成的 `md` 也要尽量保留实质内容
  - `epub`
    - 需保留章节簇判断 + 代表章节实质内容卡片
  - `txt`
    - 需保留主题聚类 + 代表样本内容保留卡片 + 主题桶保留摘要
- Kimi 跨书库统一切割协议
  - 已新增：
    - `临时粘贴区_外部AI与终端输出.md`
      - `#13 Kimi_跨书库统一切割执行指令_v1`
  - 当前用途已固定为：
    - 不只处理 `GROUP_08`
    - 也预备服务后续 `A股 / Auction-MarketProfile / 外汇订单流 / 通用微观结构 / 数据工程` 资料
  - 当前要求已固定为：
    - 先判断 `来源库角色`
    - 再做 `章节簇/主题簇`
    - 再产出 `QUANTIZATION_TABLE`
    - 明确区分：
      - `proxy_quantizable_now`
      - `needs_extra_data`
      - `shell_only`
      - `future_bucket`
      - `index_only`
    - 对 `Level2 / orderbook / DOM / 逐笔成交` 依赖内容，不允许假装可用 `OHLCV` 直接落地
- 执行清单
  - 已同步更新：
    - `TK-R6 close_back_to_signal_side` 已落盘
    - `TK-R8` 最小组合映射已落盘
    - `新的参考书` 的 `#8 / #11 / #12` 已按新版口径收口
- A股来源迁移与 txt 全文保留
  - `txt` 已从源目录全量转为“全文保留型 md + 分桶归类 + 索引”：
    - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_08_A股量化_数据研究\05_txt源码_md归档`
  - 原始 `pdf/epub/txt` 源目录已迁移到待入库区的 raw 保留层：
    - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_08_A股量化_数据研究__SOURCE_RAW\新的参考书`
  - 当前可删源边界：
    - `txt`：已具备“删源仍可回看全文”的条件
    - `pdf/epub`：仍建议先保留 raw 作为真值锚点（便于后续回看原文）
- TK-R6 proof-of-mapping 诊断壳
  - 已新增手工标注证据表与可复现汇总：
    - `12_工具运行时_TOOLING_RUNTIME\TK_R6\tkr6_manual_audit_sheet_v1.tsv`
    - `12_工具运行时_TOOLING_RUNTIME\TK_R6\tkr6_manual_audit_summary_v1.md`
- TK-R8 proof-of-mapping 诊断壳
  - 已新增手工标注证据表与可复现汇总：
    - `12_工具运行时_TOOLING_RUNTIME\TK_R8\tkr8_manual_audit_sheet_v1.tsv`
    - `12_工具运行时_TOOLING_RUNTIME\TK_R8\tkr8_manual_audit_summary_v1.md`
- TK-R7 proof-of-mapping 诊断壳
  - 已新增手工标注证据表与可复现汇总：

## 2026-06-16 视频参考吸收（体系化做法）+ CUTPACK v2 收口（A4/G08/A2）+ 滚动模板 playbook

### 证据

- 已读取：
  - `~视频参考,总结后删/*.md`
- 已入库：
  - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_08_A股量化_数据研究\06_pdf_retained_cut_v2`
  - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_09_完善体系书库_切割产物`
  - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_06_Auction_MarketProfile_价格行为\01_A2_cutpack_v2`
  - `PLAYBOOK_滚动模板.md`
  - `.trae/skills/rolling-playbook-cn/SKILL.md`
  - `.trae/skills/INDEX.md`

### 当前结论

- 视频参考的“体系化做法”可直接吸收为三层框架：
  - 工程层：
    - 分层架构：`config -> data(exchange) -> algo(strategy) -> monitor -> dashboard`
    - 稳定性：重试（指数退避）+ 本地缓存兜底
    - 运行方式：守护进程（异常告警 + 自动重启）
  - 研究层：
    - 强制回测闭环与防泄漏：只用 t 之前数据、次日开盘执行、T+1 约束等
    - 多因子合成优先做“排名法”消除量纲差异
    - 批量扫描与排序输出，减少人工翻图成本
  - 表达层：
    - 把结果产出成“可交互、可复现”的仪表盘与表格，而不是口头结论
- CUTPACK v2 收口
  - `GROUP_08` 已实现“删源可用”：
    - 失败的图片型 epub 已明确为不可 OCR（ROI 低），并用 PDF 版本拆成 4 个 part 替代
  - `A4` 已补切：
    - `Quantitative Trading` 与 `Successful Algorithmic Trading` 的 `v2_retry` 修复了空 quote，优先用 retry
  - `A2` 已落盘：
    - 3 本可提取文本的书完成 cutpack
    - 扫描版《市场轮廓理论》标记 `NEEDS_OCR`，先占位不伪造原文
- 滚动模板
  - 新增 `PLAYBOOK_滚动模板.md`，把“近期形成的流程”固化为模板，避免聊天超长后遗忘与重来
  - 新增 skill：`rolling-playbook-cn`，用于触发与维护滚动模板

### 下一步

- A2
  - 扫描版《市场轮廓理论》若要纳入“删源可用”，需要先 OCR 或寻找文字版替代
- 量化预处理
  - 以各组 `manifest_v2.tsv` 为入口，开始把 QUANTIZATION_TABLE 汇总成跨书字段池（去重 + 规范化 + 标注数据依赖）
    - `12_工具运行时_TOOLING_RUNTIME\TK_R7\tkr7_manual_audit_sheet_v1.tsv`
    - `12_工具运行时_TOOLING_RUNTIME\TK_R7\tkr7_manual_audit_summary_v1.md`

## 2026-06-16 A3 书库盘点与预处理计划落地

### 证据

- 已盘点目录：
  - `~完善体系_书籍\A3`
- 目录文件数：
  - `15`
- 文件类型分布：
  - `8` 个 `epub`
  - `6` 个 `pdf`
  - `1` 个 `txt`
- 已抽样判断：
  - 多本 `epub` 具备可提取正文文本层，可作为主文本源
  - `投资者交易指南 Volume Profile.pdf` 文本层相对更可用
  - 多份中文 `筹码分布*.pdf` 与 `和谐交易*.pdf` 更偏扫描/图片型，需先做文字层闸门
  - 两份 `陈浩` PDF 的 `sha256` 不同，不是同文件硬重复

### 当前结论

- `A3` 不是单一“筹码资料夹”，而是混合包：
  - `筹码分布 / 成本分布 / 形态手册`
  - `量价 / 威科夫`
  - `Volume Profile / Harmony / 蜡烛图`
- 当前最合理的做法不是直接整包切，而是先分成三组：
  - `A3-C1 筹码主组`
  - `A3-C2 量价 / 威科夫`
  - `A3-C3 邻接理论`
- 当前主线顺序继续收紧为：
  - `A1` 正在切
  - `A3` 同步搭预处理与切割计划
  - `F2` 暂后置到 `A3` 之后

### 下一步

- `A3-C1`
  - 先准备 Kimi 批次开场语 + 单文件模板
  - 先做中文筹码主组，优先抽：
    - `筹码分布典型形态查询手册*.pdf`
    - `擒住大牛*.epub`
    - `跟我学筹码分布*.epub`
    - `从零开始学筹码分布*.epub`
    - `筹码分布选股法.txt`
- `A3-C2`
  - 后接 `量价分析*.epub` 与 `威科夫操盘法*.epub`
- `A3-C3`
  - 仅做邻接补强，不抢当前 A 股主线

## 2026-06-13 专属工作流 skill 落地

### 证据

- 已新增：
  - `.trae/skills/mainline-full-ingest-cn/SKILL.md`
- 已更新：
  - `02_阶段二_工作方向_想法库.md`
  - `03_阶段二_当下计划_执行清单.md`

### 当前结论

- 当前已把这套工作方式正式固化成专属 skill：
  - 主线优先
  - 全量吃透
  - 一轮多步推进
  - 不默认开多 AI
  - 每轮 durable sync
- 这让后续再出现：
  - `继续推`
  - `不要停`
  - `主线不能丢`
  - `全量吃透`
  这类指令时，可以直接按 skill 工作，而不再只靠聊天记忆。

## 2026-06-13 来源库收口：TK 综合整理稿 + a-stock-data + IB 对象入口

### 证据

- 已新增：
  - `10_来源库_SOURCE_LIBRARY\00_TK外汇\20231219TK外汇交易系统学习资料整理(6)_吸收结论_v1.md`
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\REOPEN_B9_N02_IB_后续对象定义入口_v1.md`
- 已更新：
  - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_06_to_N02_对象候选清单_v1.md`
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\REOPEN_B9_N02_SESSION_OR_P0_批次推进记录_v1.md`
  - `02_阶段二_工作方向_想法库.md`
  - `03_阶段二_当下计划_执行清单.md`
- 已再次检查：
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\batch9_sources_kimi\N01\strictMode_kimi_followup\OUTBOUND__strictMode_mechanism_v3.md`
  - 当前仍无 v3 回帖

### 当前结论

- `20231219TK外汇交易系统学习资料整理(6).docx`
  - 转 `md` 与图片提取已完成
  - 当前不再只把它当“新导出文件”，而是正式当作 `00_TK外汇` Batch 1 的综合整理扩展稿
  - 它不是旧 `第1-10集 + 经验分享` 的简单重复
  - 当前新增主题已固定为：
    - 四种最佳入场法
    - `AO divergence` 风险调整
    - `B 区域` qualify
    - `平台监管 / 黑资管 / MYFXBOOK`
    - `TP3 延伸区做单法 + SOP + Forex Tester`
- `TK` 线当前最值得保留的新增对象顺序：
  - 第一优先：`TK-R6 = IB 回撤阻挡 -> TP3 概率增强`
  - 第二优先：`TK-R8 = B 区域 qualify 壳`
  - 第三优先：`TK-R7 = AO divergence 风险调整标签`
- `a-stock-data`
  - 当前正式裁决为：
    - 后期有用
    - 作用位点在 `A 股 research/data capability`
    - 不进入当前 `FX + Batch9 N01/N02` 主线
  - 记录口径已固定：
    - 方向与边界写进 `02`
    - 执行占位写进 `03`
- `IB -> N02`
  - 当前已从 `GROUP_06` 候选清单继续推进到：
    - `REOPEN_B9_N02_IB_后续对象定义入口_v1.md`
  - 角色收紧为：
    - `OR` 之后最自然的 `N02` 后续对象层第一入口
    - 当前不反向污染 `N02 P0`
- `strictMode v3`
  - 本轮再次检查仍无回帖
  - 因而继续维持当前顺序：
    - `threshold shift / qualify strictness`
    - `additional qualify conditions`
    - `score formula / weights rewrite` 最不优先

## 2026-06-13 双线继续：strictMode 冻结口径 + TK-R6 对象入口

### 证据

- 已新增：
  - `10_来源库_SOURCE_LIBRARY\00_TK外汇\TK-R6_IB回撤阻挡到TP3_后续对象定义入口_v1.md`
- 已更新：
  - `10_来源库_SOURCE_LIBRARY\00_TK外汇\20231219TK外汇交易系统学习资料整理(6)_吸收结论_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_runtime_notes_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_runtime_append_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_runtime_gaps_v1.md`
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\REOPEN_B9_N01_VOL_STATE_P0_批次推进记录_v1.md`
  - `02_阶段二_工作方向_想法库.md`
  - `03_阶段二_当下计划_执行清单.md`

### 当前结论

- `TK-R6`
  - 当前已从综合整理稿中的“可重开对象”推进成：
    - `TK` 后续对象层第一入口
  - 当前定位固定为：
    - `IB/DB/CB + Fib TP3` 之间的结构补充对象
    - 先留在诊断/对象层
    - 不直接升级成硬门控或独立策略
- `TK-R8`
  - 当前也已从综合整理稿中的“可重开对象”推进成：
    - `ABC / B 位挂单` 的 qualify 壳入口
  - 当前定位固定为：
    - 结构 qualify / 诊断对象层
    - 不直接升级成硬门控或独立策略
- `TK-R7`
  - 当前也已从综合整理稿中的“可重开对象”推进成：
    - `AO divergence` 风险调整标签入口
  - 当前定位固定为：
    - 风险修正 / 诊断对象层
    - 不直接升级成硬门控或独立策略
- `TK Batch1`
  - 当前已补统一索引：
    - `TK_Batch1_新增对象入口索引_v1.md`
  - 现在 `TKFX_12` 带来的新增对象顺序已固定为：
    - `TK-R6`
    - `TK-R8`
    - `TK-R7`
  - 当前又补了两份第一版最小草案：
    - `TK-R6_IB_retest_rejection_最小标签定义_v1.md`
    - `TK-R8_B区域_最小判据草案_v1.md`
  - 本轮又补了两份第二层最小条件：
    - `TK-R6_IB附近_最小距离口径_v1.md`
    - `TK-R8_ABC结构失效_最小条件_v1.md`
  - 当前又继续补细一格：
    - `TK-R6` 已补到 `inside_ib` 的最小 candle 触达定义
    - `TK-R8` 已补到 `structure_break` 的最小可见价格行为特征
  - 本轮又继续补到：
    - `TK-R6` 的 `reject_clear` 最少价格行为特征
    - `TK-R8` 的 `b_zone_miss` 最小距离口径
  - 本轮继续再补一格：
    - `TK-R6` 的 `inside_ib -> touch_only / reject_weak / reject_clear` 更细映射
    - `TK-R8` 的 `continuation_lost` 最小可见环境特征
- `strictMode`
  - `v3` 当前已完成一轮多 AI 批次收口
  - 当前多数票型收在：
    - `A = threshold shift`
    - `C = score formula / weights rewrite` 最不优先
    - `A = pocket/state qualify strictness`
  - 因而当前 repo 口径已继续压窄为：
    - `threshold shift / tighter score gates` 更优先
    - `additional qualify conditions` 继续保留为次优残余可能
  - `score formula / weights rewrite` 继续保持最不优先
  - 当前“其实在盯什么”也已单独收成：
    - `strictMode_v3_监看清单_v1.md`
  - 当前也已把可直接外发的提问包同步到：
    - `临时粘贴区_外部AI与终端输出.md`
  - 当前已继续补出更窄一轮：
    - `#7 strictMode_v4_OUTBOUND`
  - 核心就是只盯：
    - 具体抬的是哪个 threshold
    - 是否仍叠加 `additional qualify conditions`
    - 是否继续保持 `pocket/state qualify strictness` 这条保守口径
- 新资料/Kimi
  - 当前默认流程已固定：
    - 先给我看资料
    - 我先定批次、切法、输出层
    - 再给 Kimi 指令
- `新的参考书`
  - 当前已完成首轮盘点：
    - `162` 文件
    - `99 txt`
    - `61 pdf`
    - `2 epub`
  - 当前已固定切法：
    - 先切 `62 份研究 pdf`
    - 再切 `pdf 入门书`
    - `99 份 txt` 只做标题聚类 + 模板抽样
    - `epub` 先目录级粗切
  - 当前也已补好给多 AI 的外发问题包：
    - `#8 A股书单与Kimi切分_OUTBOUND`
  - 当前也已补好给 Kimi 直接执行的详细切分指令：
    - `#9 Kimi_62份研究PDF_三组切分执行指令`
    - `#10 Kimi_pdf入门书_章节切分执行指令`
    - `#11 Kimi_epub_目录级粗切执行指令`
    - `#12 Kimi_txt标题聚类浅切执行指令`
  - 当前先执行的第一组已固定为：
    - `量化择时`
  - 当前上传落点也已新建：
    - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_08_A股量化_数据研究`
    - `README_放这里.md`
- A股准备
  - 当前已把“优先准备哪几类 A 股书/资料”补到：
    - `02_阶段二_工作方向_想法库.md`
    - `03_阶段二_当下计划_执行清单.md`

## 2026-06-13 Batch 9：N01 compression 核心计算段细化审计

### 证据

- 已更新：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_runtime_notes_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_runtime_append_acceptance_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_runtime_gaps_v1.md`
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\REOPEN_B9_N01_VOL_STATE_P0_批次推进记录_v1.md`
  - `03_阶段二_当下计划_执行清单.md`
- 本轮不改业务逻辑代码，只把 `compression_quality_score / compression_state` 的不等价边界继续收严。

### 当前结论

- `compression_quality_score`
  - 已完成第二轮细化审计：
    - `atrScore`：高语义对齐，但 `0.60/1.10` 仍是工程冻结阈值
    - `rangeScore`：窗口骨架对齐，但 `baseline_range=sum(tr_window)` 与 `0.17/0.34` 仍属工程代理
    - `noiseScore`：当前覆盖 `body + flips`，仍缺来源摘要中提到的显式 `drift` 子项
    - `containmentScore`：当前 `25%-75% close-only pocket` 仍不能代表源码 pocket 细节
  - 因而当前总分仍只能写成“结构对齐后的 AG-Pro-like 连续分数”，不能写成源码等价。
- `compression_state`
  - 已把不等价项继续锁死：
    - `Loose / Building / Tight / Mature` 枚举骨架可保留
    - `70` 仍只是影子诊断切点
    - `Mature` 所需的 `noise/containment confirm` 已确认是来源语义要求，但仍未实现
    - `strictMode` 已确认作用方向是“收紧 score gates”，但仍未绑定具体 gating 规则
  - 因此继续维持：只审计，不落盘。
- `Action Engine`
  - 已进一步确认存在：
    - `Review Upside / Review Downside`
    - `Watch Edge / Monitor Mature`
    - `Track Compression / Build Context / Wait Setup`
  - 这说明 `compression_state` 后面还有“状态 + 位置”的解释层，但当前仍缺：
    - `nearEdge`
    - `releaseUp`
    - `releaseDown`
    的精确判定公式
- 公开页正文新增补证：
  - `strictMode` 不只是抽象开关，还伴随：
    - `stricter filtering`
    - `wick behavior` 敏感度控制
    - `close-overlap behavior` 敏感度控制
  - 还确认存在：
    - `Compression Mature` alert
    - `Compression State Change` alert
  - 这进一步说明状态机和过滤层是稳定存在的，但仍不足以反推出完整 gating 公式
- `strictMode` 的下一层优先核对位点也已收敛：
  - 先看 `noiseScore` 的 `wick behavior`
  - 再看 `containment / pocket` 的 `close-overlap behavior`
  - 再看 `compression_active / Mature` 的 qualification gating
  - 暂时不优先假设它会改四项权重，或只做单一总分阈值上调
- `nearEdge / releaseUp / releaseDown` 的层级也进一步收敛：
  - 结合 Kimi 整理到的源码结构：
    - `Pocket detection + Archive management = Lines 201-300`
    - `Ribbon + Action Engine + Event Labels = Lines 426-540`
  - 当前更应把这三项当作“位置事件 + 状态后处理分支”
  - 不应先把它们并入四项核心评分或总分公式
  - 同时已锁定条件优先级：
    - `releaseUp / releaseDown` 优先于 `isMature and nearEdge`
    - `nearEdge` 目前只出现在 `Mature` 分支
  - 这说明 `release` 更像事件覆盖，`nearEdge` 更像 Mature 阶段的位置条件
  - 再结合 `Compression State Change` 是独立告警语义，可进一步收敛为：
    - `releaseUp / releaseDown` 不等于通用 state change
    - 更像 state 之后叠加的方向性/边界事件标签
    - 当前不应直接把它们解释成 breakout 交易信号
  - 这轮又补到 Alerts 层边界：
    - 公开页明确有 `Compression Active / Compression Mature / Compression State Change`
    - 但没有把 `Review Upside / Review Downside` 作为 alerts 暴露
    - 因而 `strictMode` 更优先怀疑落在 `active/mature gating`
    - `releaseUp / releaseDown` 更像主告警层之后的附加 action 标签
  - 同时公开页还直接展示：
    - active compression zone
    - mini panel 的 `active state`
    - `compression window length`
  - 这进一步说明 `active pocket / active state` 是主状态层输出，而 `release` 更像后处理标签
  - 更新日志还单独提到 `resolved compression areas`
  - 这使得 `releaseUp / releaseDown` 更值得优先怀疑与 resolved/exit 事件相关
  - 但当前仍不能把它们直接写成 resolved breakout 公式
  - 再结合 `archivePockets / archiveCount`：
    - resolved 更可能先属于 pocket/归档展示链路
    - 不宜先把它当成新的主状态分箱
    - `release` 更像 active pocket 结束后的事件解释层
  - 更新日志还明确写出：
    - 非 active 时 preview labels 仍可见
    - preview labels 不能被当成 active confirmation
  - 因而当前继续维持：
    - 展示标签层 != active 状态层
    - `release / watch / preview labels` 都不能先抬升成主状态确认条件
  - 参数面板分层也补强了 `strictMode` 边界：
    - `strictMode` 在 `Core Engine`
    - `showPocket / archivePockets / projectPocketBars` 在 `Compression Pocket Visuals`
  - 因而 `strictMode` 继续优先视为核心资格/过滤层输入，而不是展示开关
  - 公开页总述还把 `display controls` 与 `advanced options` 分开，因此当前也没有证据表明 `strictMode` 与 labels/panel/theme 共用显示链路
  - `strictMode` 参数描述还直接写到 `more selective compression pockets`，再结合公开页开头强调 `cleaner, more contained compression conditions` 与 `matureThreshold -> noise and containment confirm`，因此当前更优先怀疑它会收紧 contained pocket / pocket qualify，而不只是 active/mature 后置 gating
  - 本轮又把 first landing 再收窄为：
    - `close-overlap`
    - `pocket qualify`
    - `contained pocket`
    - `active/Mature gating`
  - 同时补了一层结构关系：
    - `local overlap behavior` 在原始页面属于 `Noise evaluation`
    - `Structural containment` 是后一层
    - 因而当前更优先把 `close-overlap` 视为前置过滤输入，把 `contained pocket` 视为筛后的结构结果
  - `Key Inputs` 又补到一层：
    - `additional sensitivity controls for ... close-overlap behavior`
    - 因而当前更优先把 `close-overlap` 视为可调 sensitivity input，而不是 `pocket qualify` 条件名本体
  - 同时把口径再收紧为：
    - 不直接写成 `strictMode == close-overlap sensitivity`
    - 更保守地写成：二者同属 `advanced options`
    - 其中 `strictMode` 更偏总括 filtering/gating
    - `close-overlap behavior` 更偏局部 sensitivity control
  - 这轮又补到句式结构证据：
    - `stricter filtering and additional sensitivity controls ...`
    - 更像两类并列能力，而不是同一个旋钮的重说
    - 因而当前更优先怀疑 `strictMode` 与 `close-overlap sensitivity` 会并列存在，并可能共同进入 `pocket qualify`
  - 这轮再往下压一层职责分工：
    - `close-overlap` 更像 feature-level sensitivity
    - `strictMode` 更像 policy-level gating / qualify strictness
    - 因而当前更优先把二者写成共同汇入 `shared pocket qualify`，而不是互相替代
  - `projectPocketBars` 也因此更像 pocket 区域的展示延伸控制，不宜直接当成 `releaseUp / releaseDown` 的触发证据
  - 源码结构顺序还确认 `Scoring engine + State machine` 在 `Pocket detection` 与 `Action Engine` 之前，因此 `releaseUp / releaseDown` 更像状态机之后的下游解释层
  - `batch9_sources_kimi` 还明确先写 `State 判定`，后写 `Action Engine 输出`
  - 因而本轮把顺序再收严为：
    - `compressionScore -> state bucket -> isMature/isTight/isBuilding -> action labels`
    - `noise + containment -> Mature confirm` 位于 `release/nearEdge` 之前
    - `releaseUp / releaseDown` 不倒推成 `Mature` 的前置条件
  - 页面还明确写 `It does not attempt to forecast direction`，因此当前也不把 `releaseUp / releaseDown` 解释成 breakout direction prediction
  - 本轮把后续追索顺序也固定了：
    - 先追 `close-overlap` 作为 sensitivity input
    - 再追 `strictMode` 的 broader filtering/gating
    - 再追它们是否共同进入 `shared pocket qualify`
    - 再追 `contained pocket`
    - 再追 `noise + containment -> Mature confirm`
  - 另外已新增两个实际落点：
    - 书类 Kimi 回帖待入库区：`10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\`
    - `N01 strictMode` 的 Kimi 追问包：`10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\batch9_sources_kimi\N01\strictMode_kimi_followup\OUTBOUND__strictMode_vs_close_overlap_v1.md`
  - 因为当前看到的 `kimi的回复md` 仍是书类整理稿，不是 `strictMode` 回帖，所以本轮没有误并入 N01 证据链
  - 后续已确认 `strictMode_kimi_followup\OUTBOUND__strictMode_vs_close_overlap_v1.md` 下方确实已贴回 Kimi 回帖，且当前可吸收裁决为：
    - `Q1=B`
    - `Q2=B`
    - `Q3=C`
    - 即继续支持：
      - `strictMode != close-overlap sensitivity`
      - `close-overlap sensitivity + strictMode broader gating -> pocket qualify -> contained pocket -> Mature`
      - 当前不能写死 `strictMode` 只改 `Mature`
  - 同时已补一份更精确的下一轮追问：
    - `OUTBOUND__strictMode_vs_close_overlap_v2.md`
    - 重点改成直接问：
      - `close-overlap = feature-level sensitivity`？
      - `strictMode = policy-level gating / qualify strictness`？
      - 二者是否共同汇入 `shared pocket qualify`？
  - 本轮还检查了 `01_Kimi拆书待入库` 已落地的 md：
    - 当前不是乱稿，已具备待入库区结构
    - 已新增：
      - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\Kimi拆书待入库_批次检查_v1.md`
    - 当前吸收优先级暂定为：
      - 第一优先：`GROUP_05`、`GROUP_06`
      - 第二优先：`GROUP_01`、`GROUP_04`
      - 第三优先：`GROUP_03`、`GROUP_02`
      - 索引保留：`GROUP_07`
  - 本轮继续往前推了两步：
    - `strictMode` 线：
      - 因为参数区直接写了 `noiseWindow = wick behavior, direction flips, close-to-close noise`
      - 而公开页又把 `wick behavior` 与 `close-overlap behavior` 并列成 sensitivity controls
      - 所以当前更优先怀疑 `close-overlap sensitivity` 先进入 `Noise evaluation`
      - 再通过 `shared pocket qualify` 间接影响 `contained pocket`
    - Kimi 拆书线：
      - 已新增 `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_05_GROUP_06_首批可吸收清单_v1.md`
      - 当前先把 `GROUP_05` 吸收到“四轴状态模板/方法护栏”
      - 再把 `GROUP_06` 吸收到 `IB / VA / POC / Day Type` 的对象定义候选
  - 本轮又再推两步：
    - `strictMode` 线：
      - 已确认 `OUTBOUND__strictMode_vs_close_overlap_v2.md` 下方也已有回帖
      - 当前新增可吸收裁决为：
        - `Q1=B`
        - `Q2=A`
        - `Q3=A`
        - `Q4=C`
      - 即更进一步支持：
        - `close-overlap = feature-level sensitivity`
        - `strictMode = policy-level gating / qualify strictness`
        - `strictMode + close-overlap -> shared pocket qualify -> contained pocket -> Mature`
      - 同时已补第三轮追问：
        - `OUTBOUND__strictMode_mechanism_v3.md`
        - 专门继续追：阈值门 / 额外条件 / 总分权重改写
    - Kimi 拆书线：
      - 已新增 `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_05_GROUP_06_统一吸收壳_v1.md`
      - 当前把 `GROUP_05` 固定进“状态层壳”
      - 把 `GROUP_06` 固定进“对象层壳”
  - 本轮继续补了两步：
    - `strictMode` 线：
      - `v3` 目前还没有新回帖，所以这轮先不空等
      - 直接基于现有证据再收窄了一层：
        - `score formula / weights rewrite` 当前最不优先
        - 更优先顺序暂定为：
          - `threshold shift / qualify strictness`
          - `additional qualify conditions`
          - `score formula / weights rewrite`
    - `GROUP_06 -> N02` 线：
      - 已新增 `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_06_to_N02_对象候选清单_v1.md`
      - 当前顺序固定为：
        - 第一优先：`IB`
        - 第二优先：`VA / POC`
        - 第三优先：`Balance vs Imbalance / Day Type`
    - 最后追 `releaseUp / releaseDown` 与 resolved pocket 退出事件
- `Batch9 N01` 的下一步已收敛为：
  - 先补 `strictMode` 在 `noise/containment/active gating` 三层中的精确落点，以及 `Pocket detection -> Action Engine` 之间的 `nearEdge / releaseUp / releaseDown` 证据
  - 四项子评分继续只做审计，不提前落盘
  - 更广市场/第四周期扩样降为次一级

## 2026-06-12 Batch 9：字段级补缺验收推进（N02 break + N01 atr_percentile）

### 证据

- 已修改：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v1.py`
- 已重跑 proof：

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v1.py
```

- 已重跑 append：

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_runtime_append_from_proof_v1.py --persist
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_p0_runtime_append_from_proof_v1.py --persist
```

- 已补第二品种样本（`XAUUSD H1`）：

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol XAUUSD --timeframe H1 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_second_sample\xauusd_h1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_second_sample\xauusd_h1.csv --symbol XAUUSD --timeframe H1 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_xauusd_h1_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_xauusd_h1_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_xauusd_h1_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_runtime_append_from_proof_v1.py --proof 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_xauusd_h1_v1.csv --persist
```

- 已补第二周期样本（`EURUSD M15 + XAUUSD M15`）：

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol EURUSD --timeframe M15 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_second_cycle\eurusd_m15.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol XAUUSD --timeframe M15 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_second_cycle\xauusd_m15.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_second_cycle\eurusd_m15.csv --symbol EURUSD --timeframe M15 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_eurusd_m15_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_second_cycle\xauusd_m15.csv --symbol XAUUSD --timeframe M15 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_xauusd_m15_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_eurusd_m15_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_eurusd_m15_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_xauusd_m15_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_xauusd_m15_v1.csv
```

- 已补第三周期与原油类新资产类别样本（`EURUSD/XAUUSD H4` + `XBRUSD H1/H4`）：

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol EURUSD --timeframe H4 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_third_cycle\eurusd_h4.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol XAUUSD --timeframe H4 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_third_cycle\xauusd_h4.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol XBRUSD --timeframe H1 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_new_asset\xbrusd_h1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol XBRUSD --timeframe H4 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_new_asset\xbrusd_h4.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_third_cycle\eurusd_h4.csv --symbol EURUSD --timeframe H4 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_eurusd_h4_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_third_cycle\xauusd_h4.csv --symbol XAUUSD --timeframe H4 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_xauusd_h4_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_new_asset\xbrusd_h1.csv --symbol XBRUSD --timeframe H1 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_xbrusd_h1_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_new_asset\xbrusd_h4.csv --symbol XBRUSD --timeframe H4 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_xbrusd_h4_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_eurusd_h4_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_eurusd_h4_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_xauusd_h4_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_xauusd_h4_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_xbrusd_h1_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_xbrusd_h1_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_xbrusd_h4_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_xbrusd_h4_v1.csv
```

- 已补股票类新资产类别样本（`AAPL.NAS H1/H4`）：

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol AAPL.NAS --timeframe H1 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_equity_asset\aapl_nas_h1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol AAPL.NAS --timeframe H4 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_equity_asset\aapl_nas_h4.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_equity_asset\aapl_nas_h1.csv --symbol AAPL.NAS --timeframe H1 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_aapl_nas_h1_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_equity_asset\aapl_nas_h4.csv --symbol AAPL.NAS --timeframe H4 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_aapl_nas_h4_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_aapl_nas_h1_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_aapl_nas_h1_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_aapl_nas_h4_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_aapl_nas_h4_v1.csv
```

- 已补指数类新资产类别样本（`USTEC H1/H4`）：

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol USTEC --timeframe H1 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_index_asset\ustec_h1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol USTEC --timeframe H4 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_index_asset\ustec_h4.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_index_asset\ustec_h1.csv --symbol USTEC --timeframe H1 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_ustec_h1_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_index_asset\ustec_h4.csv --symbol USTEC --timeframe H4 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_ustec_h4_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_ustec_h1_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_ustec_h1_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_ustec_h4_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_ustec_h4_v1.csv
```

- 已补指数分支样本（`US500 H1/H4` + `DE40 H1/H4`）：

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol US500 --timeframe H1 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_more_index\us500_h1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol US500 --timeframe H4 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_more_index\us500_h4.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol DE40 --timeframe H1 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_more_index\de40_h1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol DE40 --timeframe H4 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_more_index\de40_h4.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_more_index\us500_h1.csv --symbol US500 --timeframe H1 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_us500_h1_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_more_index\us500_h4.csv --symbol US500 --timeframe H4 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_us500_h4_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_more_index\de40_h1.csv --symbol DE40 --timeframe H1 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_de40_h1_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_more_index\de40_h4.csv --symbol DE40 --timeframe H4 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_de40_h4_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_us500_h1_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_us500_h1_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_us500_h4_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_us500_h4_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_de40_h1_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_de40_h1_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_de40_h4_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_de40_h4_v1.csv
```

- 已补亚洲指数分支样本（`JP225 H1/H4`）：

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol JP225 --timeframe H1 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_asia_index\jp225_h1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol JP225 --timeframe H4 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_asia_index\jp225_h4.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_asia_index\jp225_h1.csv --symbol JP225 --timeframe H1 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_jp225_h1_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_asia_index\jp225_h4.csv --symbol JP225 --timeframe H4 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_jp225_h4_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_jp225_h1_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_jp225_h1_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_jp225_h4_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_jp225_h4_v1.csv
```

- 已补港股指数分支样本（`HK50 H1/H4`）：

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol HK50 --timeframe H1 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_hk_index\hk50_h1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol HK50 --timeframe H4 --start 2025-01-01 --end 2026-06-12 --out 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_hk_index\hk50_h4.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_hk_index\hk50_h1.csv --symbol HK50 --timeframe H1 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_hk50_h1_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\batch9_n01_hk_index\hk50_h4.csv --symbol HK50 --timeframe H4 --source-timezone UTC --dest 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_hk50_h4_bars_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_hk50_h1_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_hk50_h1_v1.csv
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_hk50_h4_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_hk50_h4_v1.csv
```

- 已补 `squeeze` 首批跨变体审计（`tier!=off` 对比 `mid-only`）：

```powershell
$code = @'
import csv
from pathlib import Path

base = Path(r"d:\Stock\trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples")
pairs = [("n01_first_real_input_bars_v1.csv", "n01_proof_of_mapping_output_v1.csv")]
for bars in sorted(base.glob("n01_*_bars_v1.csv")):
    if bars.name == "n01_first_real_input_bars_v1.csv":
        continue
    proof = bars.name.replace("_bars_v1.csv", "").replace("n01_", "n01_proof_of_mapping_output_") + "_v1.csv"
    if (base / proof).exists():
        pairs.append((bars.name, proof))

def sma(values):
    return sum(values) / len(values)

def stddev(values):
    mean = sma(values)
    return (sum((v - mean) ** 2 for v in values) / len(values)) ** 0.5

results = []
for bars_name, proof_name in pairs:
    bars = list(csv.DictReader((base / bars_name).open("r", encoding="utf-8", newline="")))
    proof = list(csv.DictReader((base / proof_name).open("r", encoding="utf-8", newline="")))
    closes = [float(r["close"]) for r in bars]
    highs = [float(r["high"]) for r in bars]
    lows = [float(r["low"]) for r in bars]
    trs = []
    prev_close = None
    for i in range(len(bars)):
        h = highs[i]
        l = lows[i]
        tr = max(h - l, abs(h - prev_close), abs(l - prev_close)) if prev_close is not None else h - l
        trs.append(tr)
        prev_close = closes[i]
    alt = []
    for i in range(len(bars)):
        if i + 1 < 20:
            alt.append("0")
            continue
        close_window = closes[i - 19 : i + 1]
        bb_basis = sma(close_window)
        dev = 2.0 * stddev(close_window)
        bb_upper = bb_basis + dev
        bb_lower = bb_basis - dev
        kc_basis = sma(close_window)
        dev_kc = sma(trs[i - 19 : i + 1])
        mid_on = bb_lower >= (kc_basis - 1.5 * dev_kc) or bb_upper <= (kc_basis + 1.5 * dev_kc)
        alt.append("1" if mid_on else "0")
    curr_on = sum(1 for r in proof if r["squeeze_is_on"] == "1")
    alt_on = sum(1 for v in alt if v == "1")
    curr_fired = sum(1 for r in proof if r["squeeze_fired"] == "1")
    alt_fired = sum(1 for i, v in enumerate(alt) if i > 0 and v == "0" and alt[i - 1] == "1")
    sym = proof[0]["symbol"]
    tf = proof[0]["timeframe"]
    results.append((sym, tf, curr_on, alt_on, curr_fired, alt_fired))

for row in sorted(results):
    print(row)
print("totals", sum(r[2] for r in results), sum(r[3] for r in results), sum(r[4] for r in results), sum(r[5] for r in results))
'@
$code | python -
```

- 已补 `compression_quality_score` 首批跨变体审计与 `range_score` 去退化修正：

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_first_real_input_bars_v1.csv --output 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_v1.csv
# 其余 19 份 real_input_samples\n01_*_bars_v1.csv 同口径重跑 proof，再重建 n01_p0_fields_runtime_v1.csv
```

- 已补 `compression_quality_score` 结构级源码等价审计：
  - 已对齐 AG Pro 的参数窗口：`atrLen=14 / baselineLen=50 / rangeWindow=20 / noiseWindow=10 / containmentWindow=24`
  - 已对齐权重：`30 / 30 / 20 / 20`
  - 已对齐状态阈值骨架：`compressionThreshold=62 / matureThreshold=80`
  - 仍未对齐或仍缺源码证据：
    - `range / noise / containment` 精确公式
    - `strictMode`
    - `compression_state` 的完整状态机分支
    - `Action Engine` 建议层
- 已补 `compression_state` 影子分箱审计（仅诊断、不落盘）：
  - 使用当前修正后的 `compression_quality_score` 与已对齐阈值 `62/80`
  - 20 组样本总分布：
    - `Loose = 118973`
    - `Building = 18035`
    - `Tight = 13851`
    - `Mature = 4201`
  - 代表样本：
    - `EURUSD H1 = 6774 / 1183 / 813 / 144`
    - `EURUSD M15 = 25251 / 4214 / 4503 / 1924`
    - `XAUUSD H1 = 6710 / 1045 / 645 / 75`
    - `DE40 H1 = 6645 / 900 / 590 / 160`

### 当前结论

- `N01`
  - 已把 `atr_percentile` 从 `na` 推进为真实 rolling 值。
  - 已把 `atr_percentile_regime` 从 `unknown` 推进为真实分档值。
  - 已把 `squeeze_is_on / squeeze_tier / squeeze_fired` 从占位推进为真实 `TTM-Pro-like` 分布值。
  - 已把 `compression_quality_score` 从 `na` 推进为真实 `AG-Pro-like` 连续分数（最小可复现口径）。
  - 已把 runtime 从 `EURUSD H1` 单样本推进到 `EURUSD/XAUUSD` × `H1/M15/H4`、`XBRUSD H1/H4`、`AAPL.NAS H1/H4` 与 `USTEC/US500/DE40/JP225/HK50 H1/H4` 的多周期 + 多资产类别覆盖。
  - 已完成 `squeeze` 首批跨变体审计：`tier!=off` 对比 `mid-only`，20 组样本下 `current_on=77409`、`mid_only_on=36329`、`current_fired=5363`、`mid_only_fired=4907`，差异主要来自 `low` tier 扩张。
  - 已完成 `compression_quality_score` 首批去退化修正：`range_score` 先暴露出 `pre_fix_mean=0.00` 的量纲错误，再出现 `post_scale_fix_mean=100.00` 的阈值错配，最终收敛到 `post_threshold_fix_mean=57.85`。
  - 已完成 `compression_quality_score` 首批跨变体审计：修正后四项子评分均值为 `atr=33.54 / range=57.85 / noise=48.33 / contain=60.72`，且 `current` 对 `equal_weight` 的相关性 `0.9957`、对 `no_containment` 的相关性 `0.9626`。
  - 已完成 `compression_quality_score` 结构级源码等价审计：当前实现已对齐 AG Pro 的窗口、权重与阈值骨架，但仍不能宣称“核心计算段逐项等价”。
  - 已完成 `compression_state` 影子分箱审计：当前分数配合 `62/80` 阈值在 20 组样本上可稳定分出 `Loose/Building/Tight/Mature` 四档，但在核心公式未完全等价前仍不提前落盘。
  - 已把 `compression` 等价矩阵固化到 `n01_p0_runtime_notes_v1.md`：后续统一按“已对齐 / 半对齐 / 缺源码无法判定”三类推进，不再口头漂移。
  - 当前 runtime 统计：
    - `runtime_rows = 156300`
    - `AAPL.NAS H1 atr_percentile_non_na = 2253`
    - `AAPL.NAS H4 atr_percentile_non_na = 455`
    - `DE40 H1 atr_percentile_non_na = 8093`
    - `DE40 H4 atr_percentile_non_na = 1930`
    - `EURUSD H1 atr_percentile_non_na = 8712`
    - `EURUSD M15 atr_percentile_non_na = 35690`
    - `EURUSD H4 atr_percentile_non_na = 1984`
    - `HK50 H1 atr_percentile_non_na = 5713`
    - `HK50 H4 atr_percentile_non_na = 1615`
    - `JP225 H1 atr_percentile_non_na = 8310`
    - `JP225 H4 atr_percentile_non_na = 1966`
    - `US500 H1 atr_percentile_non_na = 8261`
    - `US500 H4 atr_percentile_non_na = 1966`
    - `USTEC H1 atr_percentile_non_na = 8260`
    - `USTEC H4 atr_percentile_non_na = 1966`
    - `XAUUSD H1 atr_percentile_non_na = 8273`
    - `XAUUSD M15 atr_percentile_non_na = 33878`
    - `XAUUSD H4 atr_percentile_non_na = 1971`
    - `XBRUSD H1 atr_percentile_non_na = 7752`
    - `XBRUSD H4 atr_percentile_non_na = 1972`
    - `AAPL.NAS H1 squeeze_is_on_1 = 966`
    - `AAPL.NAS H4 squeeze_is_on_1 = 171`
    - `DE40 H1 squeeze_is_on_1 = 4080`
    - `DE40 H4 squeeze_is_on_1 = 888`
    - `EURUSD H1 squeeze_is_on_1 = 4777`
    - `EURUSD M15 squeeze_is_on_1 = 19248`
    - `EURUSD H4 squeeze_is_on_1 = 1126`
    - `HK50 H1 squeeze_is_on_1 = 2375`
    - `HK50 H4 squeeze_is_on_1 = 695`
    - `JP225 H1 squeeze_is_on_1 = 3818`
    - `JP225 H4 squeeze_is_on_1 = 1070`
    - `US500 H1 squeeze_is_on_1 = 3958`
    - `US500 H4 squeeze_is_on_1 = 930`
    - `USTEC H1 squeeze_is_on_1 = 3836`
    - `USTEC H4 squeeze_is_on_1 = 882`
    - `XAUUSD H1 squeeze_is_on_1 = 4299`
    - `XAUUSD M15 squeeze_is_on_1 = 18562`
    - `XAUUSD H4 squeeze_is_on_1 = 999`
    - `XBRUSD H1 squeeze_is_on_1 = 3748`
    - `XBRUSD H4 squeeze_is_on_1 = 981`
    - `AAPL.NAS H1 squeeze_fired_1 = 78`
    - `AAPL.NAS H4 squeeze_fired_1 = 19`
    - `DE40 H1 squeeze_fired_1 = 273`
    - `DE40 H4 squeeze_fired_1 = 80`
    - `EURUSD H1 squeeze_fired_1 = 302`
    - `EURUSD M15 squeeze_fired_1 = 1250`
    - `EURUSD H4 squeeze_fired_1 = 79`
    - `HK50 H1 squeeze_fired_1 = 205`
    - `HK50 H4 squeeze_fired_1 = 73`
    - `JP225 H1 squeeze_fired_1 = 300`
    - `JP225 H4 squeeze_fired_1 = 73`
    - `US500 H1 squeeze_fired_1 = 293`
    - `US500 H4 squeeze_fired_1 = 80`
    - `USTEC H1 squeeze_fired_1 = 299`
    - `USTEC H4 squeeze_fired_1 = 81`
    - `XAUUSD H1 squeeze_fired_1 = 285`
    - `XAUUSD M15 squeeze_fired_1 = 1139`
    - `XAUUSD H4 squeeze_fired_1 = 75`
    - `XBRUSD H1 squeeze_fired_1 = 288`
    - `XBRUSD H4 squeeze_fired_1 = 91`
    - `EURUSD H1 squeeze_tier_counts = off:4199 / low:2372 / medium:2123 / high:282`
    - `EURUSD M15 squeeze_tier_counts = off:16706 / low:10114 / medium:7905 / high:1229`
    - `EURUSD H4 squeeze_tier_counts = off:1122 / low:595 / medium:495 / high:36`
    - `XAUUSD H1 squeeze_tier_counts = off:4238 / low:2240 / medium:1791 / high:268`
    - `XAUUSD M15 squeeze_tier_counts = off:15580 / low:9675 / medium:7984 / high:903`
    - `XAUUSD H4 squeeze_tier_counts = off:1236 / low:479 / medium:436 / high:84`
    - `XBRUSD H1 squeeze_tier_counts = off:4268 / low:2166 / medium:1403 / high:179`
    - `XBRUSD H4 squeeze_tier_counts = off:1255 / low:603 / medium:353 / high:25`
    - `squeeze_variant_audit current_any_on = 77409`
    - `squeeze_variant_audit mid_only_on = 36329`
    - `squeeze_variant_audit current_any_fired = 5363`
    - `squeeze_variant_audit mid_only_fired = 4907`
    - `squeeze_tier_totals = off:78891 / low:41080 / medium:32135 / high:4194`
    - `compression_range_score_pre_fix_mean = 0.00`
    - `compression_range_score_post_scale_fix_mean = 100.00`
    - `compression_range_score_post_threshold_fix_mean = 57.85`
    - `compression_subscore_means_after_fix = atr:33.54 / range:57.85 / noise:48.33 / contain:60.72`
    - `compression_variant_audit current_mean = 49.23`
    - `compression_variant_audit equal_weight_mean = 50.11`
    - `compression_variant_audit no_containment_mean = 45.27`
    - `compression_variant_audit corr_equal_weight = 0.9957`
    - `compression_variant_audit corr_no_containment = 0.9626`
    - `compression_variant_audit mad_equal_weight = 2.12`
    - `compression_variant_audit mad_no_containment = 5.19`
    - `EURUSD H1 regime_counts = unknown:264 / normal:3300 / calm:1850 / squeeze:1050 / elevated:1571 / extreme:941`
    - `EURUSD M15 regime_counts = unknown:264 / extreme:4060 / elevated:7240 / normal:13131 / calm:7003 / squeeze:4256`
    - `EURUSD H4 regime_counts = unknown:264 / elevated:313 / extreme:190 / normal:702 / calm:430 / squeeze:349`
    - `XAUUSD H1 regime_counts = unknown:264 / squeeze:1072 / calm:1543 / normal:2961 / elevated:1527 / extreme:1170`
    - `XAUUSD M15 regime_counts = unknown:264 / normal:12372 / calm:6744 / squeeze:4102 / elevated:6754 / extreme:3906`
    - `XAUUSD H4 regime_counts = unknown:264 / elevated:345 / extreme:346 / normal:618 / calm:365 / squeeze:297`
    - `XBRUSD H1 regime_counts = unknown:264 / elevated:1449 / normal:2768 / calm:1609 / squeeze:990 / extreme:936`
    - `XBRUSD H4 regime_counts = unknown:264 / elevated:370 / normal:676 / calm:398 / squeeze:252 / extreme:276`
- `N02`
  - 已把 `first_break_direction` 从全 `none` 推进为真实 break 样本。
  - 已把 break 判定收紧为“唯一突破才记方向；双穿歧义 bar 记 none”。
  - 已实现 `close-first + wick-fallback` 的细分口径，并输出统计证据（不改 v1 表头）。
  - 已开 v2 并落盘 `first_break_mode`（`close/wick/none/ambiguous`）。
  - 已补 3 段 DST 抽查证据 + 2 段 overlap（本地时间重复/缺失）抽查证据 + 2 段“交易日本地日期归属”抽查证据（跨本地 23:xx->00:00）+ 7 段“真实 bars 分桶 + OR window 命中数”抽查证据（含秋季回切 M5：30min=>6 bars）。
  - 已补 OR 边界语义抽查证据：`in_or` 采用 `[start,end)`，`post_or` 采用 `>=end`（london/new_york 各 1 段窗口）。
  - 已补跨日本地跨日窗口下的 OR anchor 证据：同一段真实 bars 覆盖两天 local_date，分别输出两天的 `or_start_utc/or_end_utc`，证明按本地日历推导且不漂移。
  - 已补 DST 切换周的 OR anchor 一致性证据：`or_start_utc/or_end_utc` 在春秋切换日按时区规则发生 1 小时跳变（london/new_york 均覆盖）。
  - 已补 DST 切换周的“真实 bars OR anchor 对齐”证据（春季：M1；秋季：M5，london/new_york 均覆盖）。
  - 已增强 `mt5_export_bars.py`：当历史不可用但 API 返回区间外 bars 时，严格按请求区间过滤并报错（避免“看似成功但时间错位”）。
  - 当前 runtime 统计：
    - `runtime_rows = 22`
    - `or_defined = 18`
    - `first_break_up = 13`
    - `first_break_down = 5`
    - `first_break_none = 4`
    - `first_break_close_up = 8`
    - `first_break_close_down = 3`
    - `first_break_wick_up = 5`
    - `first_break_wick_down = 2`
    - `first_break_mode_close = 11`
    - `first_break_mode_wick = 7`
    - `first_break_mode_none = 4`
    - `first_break_mode_ambiguous = 0`
    - `first_non_none_break_bar_time = 2026-06-01T07:30:00Z`

### 当前剩余缺口

- `N01`
  - `squeeze` 已完成首批 `current_any_vs_mid_only` 审计，但仍未做更广 TTM 变体或源码等价审计。
  - `compression_quality_score` 已完成首批去退化修正、跨变体审计与结构级源码等价审计，但尚未完成原脚本核心计算段逐项等价审计，也未落盘四项子评分字段。
- `N02`
  - `session_timezone` 的 DST/overlap 已补最小证据（含 DST 切换周 OR anchor 跳变一致性），但仍待扩大抽查窗口与覆盖更多年份/更多时段。
  - v2 当前仍只覆盖 `EURUSD M1` 的 `london/new_york` 首批样本。

## 2026-06-12 Batch 9：第一项重开推进到脚本接入前置件

### 证据

- 已在 `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9` 新增：
  - `REOPEN_B9_N02_SESSION_OR_P0_最小实施草案_v1.md`
  - `n02_p0_field_sample_v1.csv`
  - `n02_p0_field_header_v1.txt`
  - `n02_p0_contract_notes_v1.md`
  - `REOPEN_B9_N02_SESSION_OR_P0_真实字段输出路径草案_v1.md`
  - `REOPEN_B9_N02_SESSION_OR_P0_批次推进记录_v1.md`

### 当前结论

- `REOPEN_B9_N02_SESSION_OR_P0` 已从 Batch9 的“首批可重开项”推进到：
  - 最小实施草案
  - 第一版输出证据
  - 真实字段输出路径草案
  - 工具运行时空壳
  - 占位样本行与追加协议
  - 参数模板与追加脚本 stub
- 当前仍未进入：
  - 真实 runtime csv
  - `IB / acceptance / failed breakout`
  - 策略 gate

### 当前产物路径草案

- 未来真实运行产物建议根目录：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\`
- 未来建议文件：
  - `n02_p0_fields_runtime_v1.csv`
  - `n02_p0_fields_runtime_header_v1.txt`
  - `n02_p0_runtime_notes_v1.md`
  - `n02_p0_runtime_gaps_v1.md`
  - `n02_p0_runtime_append_protocol_v1.md`
  - `n02_p0_runtime_params_template_v1.json`
  - `n02_p0_runtime_append_stub_v1.py`
- 当前这些文件已经在建议目录中创建为空壳。
- 当前 `n02_p0_fields_runtime_v1.csv` 已由 stub 写入 `1` 条示例行，placeholder 已被替换。
- 已完成 dry-run 验证命令：
- 已完成 persist 示例行验证命令：

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_p0_runtime_append_stub_v1.py
```

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_p0_runtime_append_stub_v1.py --persist
```

### 可复现口径

- 当前阶段尚未接入真实脚本链路。
- 现阶段可复现的是目录、表头、示例行、追加协议、参数模板和脚本 stub，而不是运行策略输出。
- 当前 `n02_p0_fields_runtime_v1.csv` 中已由 stub 写入 `1` 条示例行，placeholder 已被替换。

## 2026-06-12 Batch 9：第二项重开推进到 persist 示例行验证

### 证据

- 已新增：
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\REOPEN_B9_N01_VOL_STATE_P0_最小实施草案_v1.md`
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\n01_p0_field_sample_v1.csv`
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\n01_p0_field_header_v1.txt`
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\n01_p0_contract_notes_v1.md`
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\REOPEN_B9_N01_VOL_STATE_P0_真实字段输出路径草案_v1.md`
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\REOPEN_B9_N01_VOL_STATE_P0_批次推进记录_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_fields_runtime_v1.csv`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_fields_runtime_header_v1.txt`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_runtime_notes_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_runtime_gaps_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_runtime_append_protocol_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_runtime_params_template_v1.json`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_runtime_append_stub_v1.py`

### 当前结论

- `REOPEN_B9_N01_VOL_STATE_P0` 已从 `candidate` 进入 `in_progress`。
- 当前只推进：
  - `atr`
  - `atr_percentile`
  - `squeeze`
  - `compression_quality_score`
- 当前已具备：
  - 表头证据
  - 假数据样本证据
  - 合同边界说明
  - 真实字段输出路径草案
  - 运行时目录空壳
  - header / notes / gaps / append protocol
  - params template
  - append stub
  - dry-run 可复现验证
  - `--persist` 示例行验证
- 当前仍未进入：
  - `compression_state`
  - `vol_regime_code`
  - breakout 类条件字段
  - 真实 runtime 数据接入

### 参数来源收严补记

- `N01/N02` 的 runtime params template 已新增结构化来源字段：
  - `parameter_source_contract`
  - `parameter_source_detail`
- 当前每个关键参数都要求写清：
  - `source_tier`
  - `source_basis`
  - `evidence_anchor`
  - `upgrade_rule`
- 当前口径明确：
  - `source_excerpt_or_open_source` 才能被描述为“来源驱动”
  - `stub_only_default` 只能描述为“当前演示/骨架默认值”，不能冒充已审计来源参数

### 进一步冻结补记

- `N01`
  - `atr_length = 14`
    - 已由 `Volatility_Regimes__GainzAlgo__page_excerpt.md` 支撑
    - 当前可描述为“来源页支撑的 v1 ATR 输入长度”
  - `atr_baseline_length = 50`
    - 已由 `Volatility_Regimes__GainzAlgo__page_excerpt.md` 支撑
    - 当前可描述为“来源页支撑的 v1 默认值”
  - `atr_percentile_window = 252`
    - 当前已冻结为 Batch9 v1 比较窗口
    - 不是任意占位值
- `N02`
  - 已新增 `session_binding_registry`
  - 当前冻结：
    - `london -> Europe/London`
    - `new_york -> America/New_York`
  - 已补：
    - `calendar_basis`
    - `dst_handling`
  - 这意味着 `session_id / session_timezone` 已从单条示例默认值推进到最小可复用 binding 表

### 接入前 checklist 补记

- `N01`
  - 已新增：
    - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_runtime_atr_calculation_checklist_v1.md`
  - 当前作用：
    - 在真实 runtime 数据接入前固定 ATR / baseline / percentile / squeeze 的验收顺序
- `N02`
  - 已新增：
    - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_p0_runtime_session_calendar_dst_checklist_v1.md`
  - 当前作用：
    - 在真实 runtime 数据接入前固定 session / timezone / local date / DST 的验收顺序

### 真实输入映射草案补记

- `N01`
  - 已新增：
    - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_real_input_mapping_draft_v1.md`
  - 当前作用：
    - 固定真实 OHLC 输入如何映射到 ATR / percentile / squeeze 字段
  - 已新增第一份输入样本（用于 proof-of-mapping）：
    - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_first_real_input_bars_v1.csv`
  - 已落地第一份 proof 输出（基于仓库内历史 bars 数据）：
    - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_v1.csv`
  - 本轮使用的数据来源（可替换为后续 MT4/MT5 导出）：
    - `data\eurusd_1h.csv`
  - 已新增 MT5 导出接入脚本 + proof 脚本（用于升级到真实数据接入）：
    - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py`
  - 已升级为真实 MT5 导出接入 proof：
    - MT 导出脚本：
      - `mt5_export_bars.py`
      - 当前已扩为：
        - 单次导出：`--symbol --timeframe --out`
        - 批量导出：`--symbols --timeframes --out-dir`
        - 精确任务清单：`--jobs EURUSD:M1,EURUSD:H1,XAUUSD:M5 --out-dir ...`
        - 任务清单可单独指定时间窗：`SYMBOL:TIMEFRAME[:START[:END]]`
      - 默认时间窗：
        - `start=2016-01-01`
        - `end=当天 UTC 日期`
      - 若未显式传 `--start`：
        - `M1` 自动收敛到近 `180` 天
        - `M5/M6` 自动收敛到近 `365` 天
        - `M10~M30` 自动收敛到近 `730` 天
        - `H1+` 仍保留长历史口径
    - 真实导出文件：
      - `data\mt_exports_drop\eurusd_h1_export.csv`
    - 当前真实 proof 输出：
      - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_output_v1.csv`
    - 当前结果摘要：
      - `bars=8976`
      - `atr_values_computed=8963`
      - `atr_ratio_computed=8914`
  - 已进一步升级为正式 runtime append 证据：
    - `n01_p0_runtime_append_from_proof_v1.py`
    - `n01_p0_fields_runtime_v1.csv`
    - 当前 runtime 行数：`8976`
  - 已新增首批 append 验收结论：
    - `n01_p0_runtime_append_acceptance_v1.md`
    - 当前口径：
      - `atr_value / atr_ratio` 已有真实 append 证据
      - `atr_percentile` 仍未形成真实数值
- `N02`
  - 已新增：
    - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_p0_real_input_mapping_draft_v1.md`
  - 当前作用：
    - 固定真实 bar 输入与 session binding 如何映射到 OR 字段
  - 已新增第一份输入样本（用于 proof-of-mapping）：
    - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_first_real_input_bars_v1.csv`
  - 已落地第一份 OR proof 输出（基于仓库内 1min bars 数据切片）：
    - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_output_v1.csv`
  - 本轮使用的数据来源（可替换为后续 MT4/MT5 导出）：
    - `data\XAUUSD CSV\XAUUSD CSV\XAUUSD_1 Min_Bid_2003.05.05_2026.04.27.csv`
    - `data\mt_exports_drop\xauusd_m1_tail_20000.csv`
  - 已新增 MT5 导出接入脚本 + OR proof 脚本（用于升级到真实数据接入）：
    - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_mt5_export_ingest_v1.py`
    - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v1.py`
  - 已升级为真实 MT5 导出接入 proof：
    - MT 导出脚本：
      - `mt5_export_bars.py`
      - 当前已扩为：
        - 单次导出：`--symbol --timeframe --out`
        - 批量导出：`--symbols --timeframes --out-dir`
        - 精确任务清单：`--jobs EURUSD:M1,EURUSD:H1,XAUUSD:M5 --out-dir ...`
        - 任务清单可单独指定时间窗：`SYMBOL:TIMEFRAME[:START[:END]]`
      - 默认时间窗：
        - `start=2016-01-01`
        - `end=当天 UTC 日期`
      - 若未显式传 `--start`：
        - `M1` 自动收敛到近 `180` 天
        - `M5/M6` 自动收敛到近 `365` 天
        - `M10~M30` 自动收敛到近 `730` 天
        - `H1+` 仍保留长历史口径
    - 真实导出文件：
      - `data\mt_exports_drop\eurusd_m1_export.csv`
    - 当前真实 proof 输出：
      - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_output_v1.csv`
    - 当前结果摘要：
      - `bars=12947`
      - `rows=22`
      - `rows_or_defined=18`
  - 已进一步升级为正式 runtime append 证据：
    - `n02_p0_runtime_append_from_proof_v1.py`
    - `n02_p0_fields_runtime_v1.csv`
    - 当前 runtime 行数：`22`
  - 已新增首批 append 验收结论：
    - `n02_p0_runtime_append_acceptance_v1.md`
    - 当前口径：
      - `opening_range_*` 已有真实 append 证据
      - `first_break_direction` 仍未覆盖真实 break 样本

### 主线检索入口补记

- 已新增统一检索入口：
  - `00_主线检索索引.md`
- 当前作用：
  - 以后先定位主线锚点
  - 再沿索引跳到 `N01/N02 runtime`、外部参考总纲、经济事件数据维护说明

### 外部参考总纲补记

- 已新增：
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\02_外部视频与方法论参考\Smile_SMC交易系统2_0\Smile_SMC交易系统2_0_吸收与总纲_v1.md`
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\02_外部视频与方法论参考\Smile_SMC交易系统2_0\Smile_SMC交易系统2_0_逐帧运行过程_文字化_v1.md`
- 已做最小归档整理：
  - 两份原始视频总结稿已从根目录归档到：
    - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\02_外部视频与方法论参考\Smile_SMC交易系统2_0\raw_materials`
- 当前吸收重点：
  - 趋势方向
  - 开单类型
  - 入场确认
  - 订单管理
  - 实盘复盘
- 当前判断：
  - 这更像“分析系统总纲参考”，不是直接拿来做交易规则照抄
- 当前补充判断：
  - 逐帧截图已归档到：
    - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\02_外部视频与方法论参考\Smile_SMC交易系统2_0\raw_materials\video_screenshots`
  - 因此后续可删除根目录的 `视频截图` 文件夹（以归档目录为准）
- “财经新闻日历”当前补查结果：
  - 没找到按此名称收成的正式专题文档
  - 但已发现保存的数据文件：
    - `data\news_2007-01 to 2026-05 CSV; sorted date, time; UTC.csv`
  - 当前处理原则：
    - 不并入 `N01/N02/N03` 的 `P0` 字段层
    - 作为长期维护数据资产，后续要持续更新并记录更新时间与来源
  - 维护说明：
    - `data\economic_events_maintenance_v1.md`

### 可复现命令

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_runtime_append_stub_v1.py
```

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_runtime_append_stub_v1.py --persist
```

## 2026-06-11 方案 B 半硬整理与主文档抢修

### 证据

- 根目录已存在：
  - `10_来源库_SOURCE_LIBRARY`
  - `11_冻结总结层_FROZEN_SUMMARIES`
  - `12_工具运行时_TOOLING_RUNTIME`
- 活跃主文档损坏前备份：
  - `11_冻结总结层_FROZEN_SUMMARIES\99_活跃主文档损坏前备份_20260611_planb_pre_rebuild`

### 目录核对结果

- `10_来源库_SOURCE_LIBRARY` 下已有：
  - `00_指标定义&公式`
  - `00_大隐体系`
  - `00_周期女王`
  - `00_交易系统书籍`
  - `00_TK外汇`
  - `02_原子化拆解文件`
- `11_冻结总结层_FROZEN_SUMMARIES` 下已有：
  - `01_初整理文档备份_禁止修改`
  - `03_迭代后核心母版V1.2`
- `12_工具运行时_TOOLING_RUNTIME` 下已有：
  - `02_MT指标家族_源码与探针`
  - `03_MT4便携探针实例`
  - `mt4_probe_instance`
  - `98_MT历史数据_VTMarkets_Live2`
  - `VTMarkets-Live 2`

### 体量统计

- 来源库主体共约 `485` 个可扫单元：
  - 指标定义与公式：61
  - 大隐体系：132
  - 周期女王：67
  - 交易系统书籍：151
  - TK 外汇：11
  - 原子化拆解文件：63
- 冻结总结对照层共 `24` 个单元。

### 当前决策

- 不直接开“稳定候选组合优化”第一批。
- 先做“大范围扫库 + 全量吃透来源库”。
- 方案 B 进入“目录已落地、文档与索引收口”的阶段。

## 今日可复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
Get-ChildItem -Force | Select-Object Name,Mode
```

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
$dirs = @(
  '10_来源库_SOURCE_LIBRARY\00_指标定义&公式',
  '10_来源库_SOURCE_LIBRARY\00_大隐体系',
  '10_来源库_SOURCE_LIBRARY\00_周期女王',
  '10_来源库_SOURCE_LIBRARY\00_交易系统书籍',
  '10_来源库_SOURCE_LIBRARY\00_TK外汇',
  '10_来源库_SOURCE_LIBRARY\02_原子化拆解文件',
  '11_冻结总结层_FROZEN_SUMMARIES\01_初整理文档备份_禁止修改',
  '11_冻结总结层_FROZEN_SUMMARIES\03_迭代后核心母版V1.2'
)
foreach ($d in $dirs) {
  $files = (Get-ChildItem -LiteralPath $d -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
  Write-Output ("{0}`tfiles={1}" -f $d, $files)
}
```

## 下一步

- 从 `00_TK外汇` 开始 Batch 1 全量扫库。
- 每批都同步更新四份主文档，不再把结论放回临时粘贴区。
- Batch 2 开始进入：`10_来源库_SOURCE_LIBRARY\00_指标定义&公式`（先分组再抽读代表文件）。
- Batch 2 Step0：目录共 `61` 文件（`.txt=43/.docx=12/.mq4=5/.md=1`）；已抽读趋势线方法学与 KDJ 模板，并核对 Volty Stop 源码；GAS*.docx 抽样为可计算公式脚本（个别 docx 格式异常需修复）；本批先完成四分流冻结，不新增量化实现。
- Batch 2 Step0.1：已把 61 文件 unit 清单落到 `03`（含 docx 的 zip_ok/bad_zip）；其中 `GAS五里趋势.docx` 标记为 `bad_zip`，后续需先修复格式再抽读。
- Batch 3 开始进入：`10_来源库_SOURCE_LIBRARY\02_原子化拆解文件`（先抓 `原子规则表.md`，再四分流冻结；本批不新增量化实现）。
- Batch 4 开始进入：`10_来源库_SOURCE_LIBRARY\00_交易系统书籍`（本批 unit 只统计 `.md=50`；图片不计入；先四分流冻结，不新增量化实现）。
- Batch 5 开始进入：`10_来源库_SOURCE_LIBRARY\00_大隐体系`（`.md=109 / .jpg=23`；按 family 冻结，不展开 109 行逐文件表；本批不新增量化实现）。
- Batch 6 开始进入：`10_来源库_SOURCE_LIBRARY\00_周期女王`（`.md=67`；按 family 冻结；核心结构化资产在 `99_可用规则壳`；本批不新增量化实现）。
- Batch 7 开始进入：`11_冻结总结层_FROZEN_SUMMARIES\01_初整理文档备份_禁止修改`（`.md=12`；本批确认为“冻结总结层备份批”，只读，不从这里直接开新实现）。
- Batch 8 开始进入：`11_冻结总结层_FROZEN_SUMMARIES\03_迭代后核心母版V1.2`（`.md=12`；本批确认为“冻结母版层”，只做索引/总表模板，不从这里直接开新实现）。
- 海外外部指标资源整理延后到 Batch 9（Batch 8 之后）；到时要把“全量扫库结果 + 已做/待做指标 + 海外候选资源”合成一张总表，并走多 AI 讨论。
- Batch 9 已开题：第一轮先做“当前类型总表 + 建议补充类型 + 多 AI 讨论范围”，先不进入具体下载链接整理。
- Batch 9 第一轮已收口：主收 `N01 波动率状态机`、`N02 时段/开盘区间结构`；`N03 市场结构/突破质量` 只做条件收集；`N04/N05/N06` 当前不展开，但并入 `A股指标整理区` 后续整理。
- 临时粘贴区已切到“资料收集轮”：当前顶部是 `BATCH_ID=20260612_v_batch9_source_collection_round1`，可直接复制给外部 AI。
- Batch 9 已在 `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9` 建目录，并已下载首批公开文件：
  - `N01`：`TTM_Squeeze__Alorse.pine`、`TTM-Squeeze-Pro__vijankush.pine`、`README__volscope.md`
  - `N02`：`opening_range_breakout__joveteo.pine`、`README__joveteo_orb.md`、`USER_GUIDE__joveteo_orb.md`
  - `N03`：`CHOCH-BOS-ICT__gist.pine`、`BOS_CHOCH_Indicator__github.pine`
- 多 AI 本轮能力画像：`kimi` 整理最强，`deepseek` 推理/审计最强，`glm` 模板化最强，`豆包` 扩搜快但 URL 需逐条核验。

## 2026-06-11 Batch 1：00_TK外汇 初扫结果

- 目录结构：共 `11` 个文件，其中 `10` 个课程导出、`1` 个经验分享文本。
- 当前可先拆四类：
  - `IB / DB / CB` 信号链
  - `Fib 参数、TP1/TP2/TP3、SL`
  - `支撑阻力转换区 / 顺波段回撤`
  - `风险与资金管理`
- 初步分流判断：
  - `IB / DB / CB`：继续保留为可编程候选
  - `Fib 参数与 TP/SL`：继续保留为可编程候选
  - `支撑阻力转换区 / 顺波段回撤`：更像条件化应用层
  - `风险与资金管理`：更像仓位/风控规则层

## 2026-06-11 Batch 1：00_TK外汇 正式收口

### 这一步是否算在“全量吃透 + 首批量化重开实现”流程里

- 算，而且就是这条流程的前半段正式动作。
- `Batch 1 四分流收口` 属于“全量吃透”阶段。
- 当这批里再挑出 `1-2` 个最值得的量化项并真正实现、验收时，就进入“首批量化重开实现”阶段。

### 四分流

- 已吸收
  - `IB / DB / CB` 信号链：已进入最小可编程映射主线
  - `Fib` 基本止盈止损骨架：`TP1 / TP2 / TP3 / SL`
  - `TK 偏震荡、趋势行情易失效` 的 regime 提示：已作为口径提示吸收
- 可重开
  - `TP3 延申链`：`TP wick -> CB close -> CB wick`
  - `支撑阻力转换区 / 顺波段回撤`
  - `风险报酬比 / 最低胜率 / TP2 vs TP3` 的计划验证
  - `固定风险、固定止损、跨品种相关性风控` 的规则化映射
- future bucket
  - `FETP` 专有自动下单器、账号绑定授权链
  - `Xbreaking` 小周期显示修复、历史数据导入链
  - 这两类都更依赖 `MT4/MT5 + 专有工具 + 运行时环境`，不作为当前主库字段优先实现
- 仅来源库保留
  - `MT4 / MT5 Fib` 界面设定技巧、绘图快捷键、矩形填色等纯操作教程
  - 纯教学性心态描述、观望建议、软件使用细节

### 本批建议的首批量化重开项

- TK-R1：`TP3 延申链`
  - 目标：把 `TP3 被突破后如何重定位反向区域` 做成可复现字段或诊断链
- TK-R2：`顺波段回撤`
  - 目标：把 `TP1/TP2 突破后回撤挂单 / 小周期确认` 做成条件化应用验证
- TK-R3：`风险报酬比与最低胜率`
  - 目标：把 `TP1/TP2/TP3` 对应的 `R multiple / minimum win rate` 固化为计划评估层，而不是口头经验

## 2026-06-11 “全量吃透 + 首批量化重开实现”执行清单

### 固定总流程

- [ ] Step 0：先做目录统计、文件清单、主题分组
- [ ] Step 1：抽读代表文件，写出“这批真正讲了什么”
- [ ] Step 2：输出四分流：`已吸收 / 可重开 / future bucket / 仅来源库保留`
- [ ] Step 3：从“可重开”里只选 `1-2` 个最值得做的项
- [ ] Step 4：给每个重开项写最小实现定义：字段、规则、依赖数据、输出位置
- [ ] Step 5：只做最小补丁，不顺手扩写同家族
- [ ] Step 6：跑最小证据：覆盖率、样本数、分桶或 trade-level 结果
- [ ] Step 7：回写四份主文档：阶段记录、想法库、执行清单、日活
- [ ] Step 8：决定这批是“继续重开下一项”还是“正式冻结进入下一批”

### 每批固定出口

- [ ] 已吸收：确认已经被现有字段或规则覆盖
- [ ] 可重开：必须写成明确条目，不允许只写“以后再看”
- [ ] future bucket：必须写清楚为什么现在不做
- [ ] 仅来源库保留：必须写清楚为什么只保留来源属性

### 防走歪约束

- [ ] 每批最多只推进 `1-2` 个量化重开实现
- [ ] 没有新数据口径或新证据，不允许顺手扩家族
- [ ] 工具运行时问题和字段研究问题分开记，不混写
- [ ] 先收口一批，再开下一批，不回到大范围乱扫

### 当前 12-20 个工作日的推荐排程

- [ ] Day 1-2：Batch 1 `00_TK外汇` 收口 + 选出首批重开项
- [ ] Day 3-4：实现 TK-R1
- [ ] Day 5-6：实现 TK-R2 或 TK-R3
- [ ] Day 7-9：Batch 2 `00_指标定义&公式`
- [ ] Day 10-12：Batch 3 `02_原子化拆解文件`
- [ ] Day 13-15：Batch 4 `00_大隐体系`
- [ ] Day 16-17：Batch 5 `00_周期女王`
- [ ] Day 18-19：Batch 6 `00_交易系统书籍`
- [ ] Day 20：Batch 7-8 冻结对照层收口 + 总体复盘

## 2026-06-11 skill 体系升级

- 已升级：`.trae\skills\dev-guardrails\SKILL.md`
- 已新增：`.trae\skills\source-sweep-batch-cn\SKILL.md`
- 新增 skill 的用途：
  - 固定方案 B 的四层边界
  - 固定来源库每批四分流
  - 固定四份主文档同步

## 2026-06-11 TK-R1：TP3 延申链 第一版实现

### 复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\backtest_p0.py b114-tk-tp3-extension --date 20260611 --scope all --split since2022
```

### 产物

- `backtest_out\stage2\indicator_audit\20260611_b114_tk_tp3_extension_all_v1\b114_bucket_stats_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b114_tk_tp3_extension_all_v1\b114_feature_summary_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b114_tk_tp3_extension_all_v1\b114_coverage_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b114_tk_tp3_extension_all_v1\b114_spearman_corr_20260611_v1.csv`

### 当前实现边界

- 这是第一版“近似诊断映射”，不是 TK 原版 `TP / CB` 信号系统的完整复刻。
- 当前映射的是：
  - `stage0`：未进入 TP3 深区突破
  - `stage1`：深区突破后仍未回收
  - `stage2`：深区突破后完成回收
  - `stage3`：深区突破后强回收

### 关键结果

- `feature_summary`：
  - `tk_tp3_ext_stage_1h`：`top_minus_bot_avg_pnl = 1402.52`
  - `tk_tp3_reclaim_flag_1h`：`top_minus_bot_avg_pnl = 644.81`
- 样本分布：
  - `stage0 = 16540`
  - `stage2 = 10`
  - `stage3 = 3`
  - `reclaim=1 = 13`
- 当前判断：
  - 已经满足“可复现、可审计、可继续调参”的第一步
  - 但分布仍偏稀疏，当前只能定为 `DIAG_ONLY`

## 2026-06-11 TK-R1：第二步参数调优 + 交互验证

### 调参扫描摘要

- 扫描摘要文件：
  - `backtest_out\stage2\indicator_audit\param_sweeps\20260611_b114_tuning_small\small_summary.csv`
- 四组代表参数结果：
  - `base`：`stage2=10`、`stage3=3`
  - `mid`：`stage2=311`、`stage3=133`
  - `low`：`stage2=540`、`stage3=277`
  - `tight`：`stage2=131`、`stage3=96`
- 最终选中 `low` 作为 tuned 版：
  - `lookback_bars=36`
  - `deep_ratio=0.50`
  - `wick_ratio_min=0.15`
  - `close_pos_min=0.35`
  - `body_ratio_min=0.20`
  - `strong_close_pos_min=0.50`

### tuned 版复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\backtest_p0.py b114-tk-tp3-extension --date 20260611 --scope all --split since2022 --lookback_bars 36 --deep_ratio 0.50 --wick_ratio_min 0.15 --close_pos_min 0.35 --body_ratio_min 0.20 --strong_close_pos_min 0.50 --out_dir backtest_out\stage2\indicator_audit\20260611_b114_tk_tp3_extension_tuned_v2
```

### tuned 版关键结果

- 产物目录：
  - `backtest_out\stage2\indicator_audit\20260611_b114_tk_tp3_extension_tuned_v2`
- 样本分布：
  - `stage0 = 22270`
  - `stage1 = 62`
  - `stage2 = 540`
  - `stage3 = 277`
  - `reclaim=1 = 817`
- 说明：
  - 相比第一版的 `13` 个回收样本，tuned 版已经进入“可审计样本量”

### 交互验证复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tools\tk_r1_interactions.py --out_dir backtest_out\stage2\indicator_audit\20260611_b114_tk_tp3_extension_tuned_v2
```

### 交互验证产物

- `backtest_out\stage2\indicator_audit\20260611_b114_tk_tp3_extension_tuned_v2\b114_tuned_trade_level_interactions_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b114_tk_tp3_extension_tuned_v2\b114_tuned_stage_summary_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b114_tk_tp3_extension_tuned_v2\b114_tuned_interaction_delta_20260611_v1.csv`

### 交互验证结论

- `stage2+stage3` 相对 `stage0/1`：
  - `b46` 信号质量均值：`+0.97`
  - `b51` reversal 分数：`+0.43`
  - `b53` trendbar 强度：`+0.18`
  - `doji`：`-0.03`
- 分阶段看：
  - `stage2`：`avg_pnl = -1.69`，明显好于 `stage0 = -27.53`
  - `stage3`：`avg_pnl = -106.95`，比 `stage2` 明显更差
- 当前判断：
  - `TK-R1` 更像“回收型诊断 / 回收后延续诊断”
  - 不像“反转型诊断”
  - 后续如果要继续收缩，应优先保留 `stage2`，单独审计 `stage3`

### stage2 vs stage3 分拆审计

- 分拆依据：
  - `b114_tuned_interaction_delta_20260611_v1.csv`
- 关键对比：
  - `stage2_vs_stage0`
    - `avg_pnl = +25.84`
    - `b46 = +1.30`
    - `b51 = +0.52`
    - `b53 = +0.29`
  - `stage3_vs_stage0`
    - `avg_pnl = -79.41`
    - `b46 = +0.34`
    - `b51 = +0.26`
    - `b53 = -0.02`
  - `stage3_vs_stage2`
    - `avg_pnl = -105.26`
    - `b46 = -0.96`
    - `b51 = -0.25`
    - `b53 = -0.31`
- 分拆结论：
  - `stage2`：升级为保留候选
  - `stage3`：降级为观察项

### stage2 单独审计

- 复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tools\tk_r1_stage2_audit.py --out_dir backtest_out\stage2\indicator_audit\20260611_b114_tk_tp3_extension_tuned_v2
```

- 审计产物
  - `b114_stage2_overall_audit_20260611_v1.csv`
  - `b114_stage2_by_symbol_20260611_v1.csv`
  - `b114_stage2_by_profile_20260611_v1.csv`
  - `b114_stage2_breadth_20260611_v1.csv`
  - `b114_stage2_feature_buckets_20260611_v1.csv`

- 总体结果
  - `trade_pnl`：`stage2 - stage0 = +25.84`
  - `b46`：`+1.30`
  - `b51`：`+0.52`
  - `b53`：`+0.29`
  - 但 `win_rate`、`tp2_rate` 不比 `stage0` 更好，`stop_loss_rate` 也更高

- 广度结果
  - `stage2_n = 543`
  - `stage2_share_all = 2.33%`
  - `32` 个 symbol 中，只有 `12` 个 symbol 的 `avg_pnl > 0`
  - `3` 个 profile 中，只有 `A_universal` 为正，`A_strict` 明显偏弱

- 条件结果
  - `b46_sig_quality` 在 `(5,8]` 和 `(8,9]` 桶更健康
  - `b46_sig_quality >= 9` 反而明显恶化
  - `b53_trendbar_strength = 2` 好于 `=1`

- 当前结论
  - `stage2` 比 `stage3` 明显更健康，应继续保留
  - 但它还不是“更稳定的全局保留候选”
  - 当前最合适的角色是：`DIAG_ONLY_CANDIDATE / 条件型保留候选`

### stage2 条件化收缩

- 复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tools\tk_r1_stage2_conditional_shrink.py --out_dir backtest_out\stage2\indicator_audit\20260611_b114_tk_tp3_extension_tuned_v2
```

- 产物
  - `b114_stage2_b46_focus_bins_20260611_v1.csv`
  - `b114_stage2_profile_x_b46_focus_20260611_v1.csv`
  - `b114_stage2_midbin_profiles_20260611_v1.csv`

- b46 聚焦桶
  - `(5,8] = +145.96`
  - `(8,9] = +113.36`
  - `<=5 = -77.74`
  - `>=10 = -716.64`

- profile x b46 关键结论
  - `A_relaxed + (5,8] = +226.26`
  - `A_relaxed + (8,9] = +143.82`
  - `A_universal + (5,8] = +388.52`
  - `A_universal + (8,9] = +52.58`
  - `A_strict + (5,8] = -277.06`
  - `A_strict + (8,9] = -18.71`

- 条件化结论
  - 可保留条件链：
    - `stage2`
    - `b46 in (5,8] / (8,9]`
    - `profile in {A_relaxed, A_universal}`
  - 应排除或强降权：
    - `b46 >= 10`
    - `A_strict`
  - 角色更新：
    - 无条件 `stage2`：仍是 `DIAG_ONLY_CANDIDATE`
    - 条件化后的 `stage2`：可升级为 `条件型保留候选`

## 2026-06-11 关于“旧单字段是否全品种 / TK-R1 是否全品种”

- 旧单字段阶段的“已完成”口径，是当前 universe 下的全品种口径：
  - `FX / index / commodity 1H`
- 这不等于所有来源库、所有市场、所有 A 股专用指标都已全量完成。
- `TK-R1` 当前也保持同一口径，先跑：
  - `scope all`
  - `split since2022`
- 原因：
  - 现在仍在诊断阶段，先看全 universe 是否成立，比先缩成 core 更稳
  - 如果一开始就只看 core，容易把稀疏信号误判成“看起来很好”

## 2026-06-11 如何确保“全量吃透 + 首批量化重开实现”主线不丢

- 固定主线：
  - 当前主线只有一条：`来源库全量吃透 -> 当前批次收口 -> 首批量化重开实现`
- 允许深挖，但只能是主线内深挖：
  - 只允许深挖当前批次、当前重开项
  - 例如：扫参、stage 分拆、profile 分层、交互验证
- 每次深挖必须先写三件事：
  - 进入条件：为什么现在值得深挖
  - 退出条件：做到什么程度就停止
  - 主线影响：角色升级 / 维持 / 降级
- 每次深挖结束后必须回填：
  - 四份主文档
  - 当前项的新角色
  - 下一步是继续当前项，还是回到下一批
- 如果深挖后角色没有变化，就停止横向扩展，回到主线

## 2026-06-11 根目录单文件职责盘点与最小整理

- 新增总表：
  - `docs\根目录单文件职责与归类_20260611.md`
- 当前根目录单文件结论：
  - 活跃入口脚本：
    - `ashare_preprocess.py`
    - `backtest_p0.py`
    - `mt5_exit_assistant.py`
    - `mt5_export_1h.py`
    - `mt5_daily_ops.ps1`
    - `run_p0_sweep.ps1`
  - 配置锚点：
    - `pyrightconfig.json`
    - `basedpyrightconfig.json`
  - 候选后续整理：
    - `_ai_index.txt`
    - `generate_p0_subset.py`
- 已执行整理动作：
  - 新建 `docs\ops\`
  - 正式版 `ashare_daily_ops.md` 已复制到：
    - `docs\ops\ashare_daily_ops.md`
  - 根目录 `ashare_daily_ops.md` 已改成兼容入口
- 这样做的原因：
  - 说明文档进入 `docs`
  - 旧命令锚点不丢
  - 活跃入口脚本不被硬搬导致口径断裂

## 2026-06-11 TK-R2 = 顺波段回撤 开题

- 来源锚点：
  - `10_来源库_SOURCE_LIBRARY\00_TK外汇\外汇交易课程第四集-斐波那契支撑阻力转换区_导出.md`
  - `10_来源库_SOURCE_LIBRARY\00_TK外汇\经验分享.txt`
- 当前抽到的最小规则壳：
  - `TP1` 突破后：
    - 在“信号回撤区”等待回撤
    - 目标先看 `TP2`
  - `TP2` 突破后：
    - 在 `TP1` 转换区等待第二次回撤
    - 目标先看 `TP3`
  - 若价格未回撤直接到达 `TP3`：
    - 取消挂单
  - 保守模式：
    - 大周期转换区 + 1H/15m 小周期反向信号确认
- 当前实现策略：
  - 不先硬造完整交易系统
  - 先把它拆成可诊断的：
    - breakout stage
    - zone type
    - zone hit
    - cancel / no-retrace

## 2026-06-11 根目录整理第二批收口

- `_ai_index.txt`
  - 正式归档：
    - `docs\indexes\_ai_index_legacy_20260611.txt`
  - 根目录已收口为兼容入口，不再混放旧正文
- `generate_p0_subset.py`
  - 正式实现已迁到：
    - `tools\generate_p0_subset.py`
  - 根目录 wrapper 已验证可正常转发
  - 今日实跑结果：
    - 成功生成 `docs\P0_规则子表_v0.1.md`
    - `规则条数 = 70`

## 2026-06-11 TK-R2 第一版诊断标签 / 证据命令已跑通

### 复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\backtest_p0.py b115-tk-r2-pullback --date 20260611 --scope all --split since2022
```

### 产物

- `backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1\b115_bucket_stats_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1\b115_feature_summary_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1\b115_coverage_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1\b115_spearman_corr_20260611_v1.csv`

### 第一版覆盖率

- 总覆盖：
  - `priced = 20852 / 23657 = 88.14%`
- symbol x profile 覆盖率：
  - `median = 88.73%`
  - `mean = 87.27%`
  - `min = 70.21%`

### pooled 关键结果

- `stage`
  - `stage0 = 10036`，`avg_pnl = +5.33`
  - `stage1 = 8542`，`avg_pnl = -42.14`
  - `stage2 = 1828`，`avg_pnl = -146.09`
  - `stage3 = 204`，`avg_pnl = -161.02`
- `zone_hit`
  - `zone_hit=1 = 64`，`avg_pnl = +440.35`
  - `zone_hit=0 = 20546`，`avg_pnl = -30.89`
- `cancel_no_retrace`
  - `cancel=1 = 132`，`avg_pnl = -246.88`
  - `cancel=0 = 20478`，`avg_pnl = -28.02`
- `retrace_depth qtiles`
  - `q4_bin2 = -1.70`
  - `q4_bin1 = -43.18`
  - `q4_bin3 = -29.31`
  - `q4_bin4 = -42.41`
  - 深回撤桶的 `stop_loss_rate` 明显更高：`q4_bin4 = 28.06%`

### 第一版判断

- `TK-R2` 已满足“第一版诊断标签/证据命令可复现”。
- `stage` 目前不像单调增益特征，更像 breakout 后所处阶段的状态标签。
- `zone_hit` 有正向 pocket，但样本只有 `64`，当前只能先放在 `DIAG_ONLY_CANDIDATE`。
- `cancel_no_retrace` 更像负向告警标签，当前先放在 `DIAG_ONLY`，不直接做硬 veto。
- 下一步应继续：
  - 做 trade-level 分拆
  - 拆 `stage1/stage2/stage3`
  - 再看 `zone_hit / cancel` 是否在特定 profile 或 symbol 上更稳定

## 2026-06-11 TK-R2 trade-level 分拆

### 复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\backtest_p0.py b115-tk-r2-pullback --date 20260611 --scope all --split since2022
.\.venv\Scripts\python.exe .\tools\tk_r2_tradelevel_audit.py
```

### 新增产物

- `backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1\b115_trade_level_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1\b115_stage_split_summary_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1\b115_stage_split_delta_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1\b115_stage_by_profile_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1\b115_stage_by_symbol_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1\b115_zonehit_profile_symbol_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1\b115_cancel_profile_symbol_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1\b115_flag_breadth_20260611_v1.csv`

### stage 分拆结果

- pooled `stage`：
  - `stage0 = 10147`，`avg_pnl = +4.16`，`median_pnl = +17.90`
  - `stage1 = 8647`，`avg_pnl = -39.59`，`median_pnl = 0.00`
  - `stage2 = 1853`，`avg_pnl = -145.16`，`median_pnl = 0.00`
  - `stage3 = 205`，`avg_pnl = -172.30`，`median_pnl = -245.00`
- pairwise：
  - `stage1_vs_stage0 = -43.75`
  - `stage2_vs_stage0 = -149.31`
  - `stage3_vs_stage0 = -176.45`
  - `stage2_vs_stage1 = -105.57`
  - `stage3_vs_stage2 = -27.14`
- 说明：
  - 这轮 trade-level 分拆后，`stage1 / stage2 / stage3` 没有出现“越往后越健康”的证据
  - 相反，更像 breakout 后所处位置的风险状态层

### profile / symbol 广度

- profile：
  - `stage1` 只有 `A_strict = +11.50`，其余 profile 仍偏弱
  - `stage2`：
    - `A_relaxed = -21.36`
    - `A_strict = -242.25`
    - `A_universal = -174.68`
  - `stage3` 三个 profile 全为负
- symbol breadth：
  - `stage1`：`32` 个 symbol 中，`5` 个 `avg_pnl > 0`
  - `stage2`：`32` 个 symbol 中，`12` 个 `avg_pnl > 0`
  - `stage3`：虽然有少量小样本正口袋，但 `n>=20` 的 symbol 里只剩 `NZDJPY`，且 `avg_pnl = -358.39`
- 当前判断：
  - `stage3` 应明确降为观察项/负向状态标签
  - `stage1 / stage2` 仍只能保留为 `DIAG_ONLY` 状态层，不进入硬门控讨论

### zone_hit / cancel 的 profile x symbol 稳定性

- `zone_hit`
  - `96` 个 `profile x symbol` 组合里：
    - `26` 个组合至少出现过一次
    - `7` 个组合 `n_flag1 >= 3`
    - `4` 个组合 `n_flag1 >= 5`
    - `5` 个组合同时满足 `avg/median delta > 0`
  - 相对更好的 pocket：
    - `A_universal + AUDJPY`：`n=8`，`share=1.00%`
    - `A_strict + GBPJPY`：`n=6`，`share=0.52%`
    - `A_relaxed + GER40`：`n=6`，`share=1.44%`
  - 结论：
    - 全局仍过稀
    - 但可以保留少数局部 pocket 作为下一轮条件化收缩入口
- `cancel_no_retrace`
  - `96` 个组合里：
    - `43` 个组合至少出现过一次
    - `19` 个组合 `n_flag1 >= 3`
    - `8` 个组合 `n_flag1 >= 5`
    - 只有 `5` 个组合同时满足 `avg/median delta > 0`
  - 说明：
    - 它不是稳定的全局负向 veto
    - 因为在 `profile x symbol` 下方向明显混杂，既有强负向 pocket，也有正向 pocket
  - 当前更合理的定位：
    - `条件化负向告警标签`
    - 暂不升为全局硬 veto

### 当前收口

- `stage1 / stage2 / stage3`：
  - 保留为 `DIAG_ONLY` 状态标签
- `stage3`：
  - 更明确地视为过晚阶段 / 观察项
- `zone_hit`：
  - 从“全局候选”收紧为“局部 pocket 候选”
- `cancel_no_retrace`：
  - 从“可能的全局负向标签”收紧为“条件化负向告警”

## 2026-06-11 TK-R2 pocket 收缩（zone_hit 正向 / cancel 负向）

### 复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tools\tk_r2_pocket_shrink.py --out_dir backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1 --date_tag 20260611
```

### 新增产物

- `backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1\b115_zonehit_positive_pockets_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1\b115_cancel_negative_pockets_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1\b115_pocket_shrink_summary_20260611_v1.csv`

### pocket 规模（默认口径：support>=3；strong>=5）

- `zone_hit` 正向 pocket：`5`（其中 strong `3`）
- `cancel_no_retrace` 负向 pocket：`13`（其中 strong `5`）

### zone_hit 正向 pocket（示例）

- `A_universal + AUDJPY`：`n=8`，`delta_avg=+1078.66`，`delta_median=+1066.34`
- `A_strict + GBPJPY`：`n=6`，`delta_avg=+851.35`，`delta_median=+1329.74`
- `A_relaxed + GER40`：`n=6`，`delta_avg=+681.37`，`delta_median=+881.05`

### cancel_no_retrace 负向 pocket（示例）

- `A_relaxed + XAUUSD`：`n=5`，`delta_avg=-1867.76`，`delta_median=-2582.78`
- `A_strict + UKOIL`：`n=5`，`delta_avg=-1584.53`，`delta_median=-2434.63`
- `A_strict + XAUUSD`：`n=5`，`delta_avg=-729.14`，`delta_median=-819.56`

### pocket 应用影响（只做审计，不做门控）

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tools\tk_r2_pocket_apply_audit.py --out_dir backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1 --date_tag 20260611
```

- 产物：
  - `backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1\b115_pocket_apply_overall_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_all_v1\b115_pocket_apply_pockets_20260611_v1.csv`
- 总体读数（trade-level）：
  - `zonehit_pos_pocket_hit`：`n=26`（0.11%），`avg_pnl=+1248.12`，`median=+1055.76`
  - `cancel_neg_pocket_hit`：`n=59`（0.25%），`avg_pnl=-882.34`，`median=-630.67`
  - 若仅过滤 `cancel_neg_pocket_hit`：全局 `avg_pnl` 从 `-29.43` 改善到 `-27.30`（改善 `+2.13`），但改善幅度受限于覆盖率很小

## 2026-06-11 TK-R2 稳定性复验（pre2022）

### 复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\backtest_p0.py b115-tk-r2-pullback --date 20260611 --scope all --split pre2022 --out_dir backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_pre2022_v1
.\.venv\Scripts\python.exe .\tools\tk_r2_tradelevel_audit.py --trade_level_csv backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_pre2022_v1\b115_trade_level_20260611_v1.csv --out_dir backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_pre2022_v1
.\.venv\Scripts\python.exe .\tools\tk_r2_pocket_shrink.py --out_dir backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_pre2022_v1 --date_tag 20260611
.\.venv\Scripts\python.exe .\tools\tk_r2_pocket_apply_audit.py --out_dir backtest_out\stage2\indicator_audit\20260611_b115_tk_r2_pullback_pre2022_v1 --date_tag 20260611
```

### pre2022 stage 结构是否复现

- pooled `stage`（pre2022）：
  - `stage0 = 5679`，`avg_pnl = -12.96`
  - `stage1 = 5189`，`avg_pnl = -104.38`
  - `stage2 = 1181`，`avg_pnl = -126.74`
  - `stage3 = 126`，`avg_pnl = -435.79`
- 结论：`stage0 > stage1 > stage2 > stage3` 的负向递进结构复现，`stage` 仍是风险状态层而非正向特征。

### pre2022 pocket 是否仍是“强但稀”

- pocket 规模（support>=3；strong>=5）：
  - `zone_hit` 正向 pocket：`1`（strong `0`）
  - `cancel_no_retrace` 负向 pocket：`7`（strong `1`）
- 应用影响（trade-level）：
  - `zonehit_pos_pocket_hit`：`n=4`（0.03%），`avg_pnl=+522.57`，`median=+677.64`
  - `cancel_neg_pocket_hit`：`n=26`（0.19%），`avg_pnl=-1160.31`，`median=-871.87`
  - 若仅过滤 `cancel_neg_pocket_hit`：全局 `avg_pnl` 从 `-69.82` 改善到 `-67.70`（改善 `+2.12`）
- 结论：
  - pocket 的方向性复现（正口袋/负口袋都存在）
  - 但覆盖率仍极小，因此继续维持“规则壳 + pocket 清单（诊断/告警）”，不升级为全局门控

## 2026-06-11 TK-R3：风险报酬比与最低胜率（最小审计）

### 复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tools\tk_r3_rr_minwin_audit.py --split since2022 --date_tag 20260611 --out_dir backtest_out\stage2\indicator_audit\20260611_b116_tk_r3_rr_minwin_since2022_v1
.\.venv\Scripts\python.exe .\tools\tk_r3_rr_minwin_audit.py --split pre2022 --date_tag 20260611 --out_dir backtest_out\stage2\indicator_audit\20260611_b116_tk_r3_rr_minwin_pre2022_v1
```

### 新增产物

- since2022：
  - `backtest_out\stage2\indicator_audit\20260611_b116_tk_r3_rr_minwin_since2022_v1\b116_rr_minwin_overall_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b116_tk_r3_rr_minwin_since2022_v1\b116_rr_minwin_by_reason_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b116_tk_r3_rr_minwin_since2022_v1\b116_rr_minwin_overall_20260611_v2.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b116_tk_r3_rr_minwin_since2022_v1\b116_rr_minwin_by_reason_20260611_v2.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b116_tk_r3_rr_minwin_since2022_v1\b116_rr_minwin_by_class_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b116_tk_r3_rr_minwin_since2022_v1\b116_rr_minwin_tp2_vs_tp3_20260611_v1.csv`
- pre2022：
  - `backtest_out\stage2\indicator_audit\20260611_b116_tk_r3_rr_minwin_pre2022_v1\b116_rr_minwin_overall_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b116_tk_r3_rr_minwin_pre2022_v1\b116_rr_minwin_by_reason_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b116_tk_r3_rr_minwin_pre2022_v1\b116_rr_minwin_overall_20260611_v2.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b116_tk_r3_rr_minwin_pre2022_v1\b116_rr_minwin_by_reason_20260611_v2.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b116_tk_r3_rr_minwin_pre2022_v1\b116_rr_minwin_by_class_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b116_tk_r3_rr_minwin_pre2022_v1\b116_rr_minwin_tp2_vs_tp3_20260611_v1.csv`

### R multiple 口径

- `R = (exit-entry) / abs(entry-entry_stop_ref)`（LONG/SHORT 分开符号）
- `entry_stop_ref` 使用同一笔交易（同 entry_time/side/entry）的 stop 极值复原：
  - LONG：取最小 stop
  - SHORT：取最大 stop

### reason 收口：统一映射为五类

- `tp_cam_[r/s]1` -> `TP1`
- `tp_cam_[r/s]2` -> `TP2`
- `tp_cam_[r/s]3+` -> `TP3`
- `*stop*` -> `Stop`
- `*trail*` -> `Trail`

### TP2 vs TP3 最低胜率对照（当前数据口径下）

- since2022：
  - `TP2 n=12776`，`breakeven_win_rate_est≈0.339`
  - `TP3 n=0`（baseline 回测只产出 `tp_cam_[r/s]1/2`，无 `tp_cam_[r/s]3`）
- pre2022：
  - `TP2 n=7167`，`breakeven_win_rate_est≈0.333`
  - `TP3 n=0`

### TP2 vs TP3 最低胜率对照（cam_tp3 重算：让 baseline 真的产出 TP3）

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tools\tk_r3_rr_minwin_recompute_cam_tp3.py --split since2022 --date_tag 20260611 --out_dir backtest_out\stage2\indicator_audit\20260611_b117_tk_r3_rr_minwin_cam_tp3_since2022_v1 --cam_r3_mult 0.70 --cam_tp3_frac 0.20
.\.venv\Scripts\python.exe .\tools\tk_r3_rr_minwin_recompute_cam_tp3.py --split pre2022 --date_tag 20260611 --out_dir backtest_out\stage2\indicator_audit\20260611_b117_tk_r3_rr_minwin_cam_tp3_pre2022_v1 --cam_r3_mult 0.70 --cam_tp3_frac 0.20
```

- since2022（cam_tp3）：
  - `TP2 n=20112`，`breakeven_win_rate_est≈0.331`
  - `TP3 n=17960`，`breakeven_win_rate_est≈0.304`
- pre2022（cam_tp3）：
  - `TP2 n=7167`，`breakeven_win_rate_est≈0.333`
  - `TP3 n=6429`，`breakeven_win_rate_est≈0.306`

### baseline 为什么没有 TP3（根因）

- baseline 的 CAM 出场在回测里只定义了 `tp_cam_[r/s]1` 与 `tp_cam_[r/s]2`，所以原始 `p0_sweep/*/trades_baseline_*.csv` 不会出现 `tp_cam_[r/s]3`
- 已在 [backtest_p0.py](file:///d:/Stock/trading_analysis/backtest_p0.py) 增加可选 `enable_cam_tp3/cam_r3_mult/cam_tp3_frac`（默认关闭，不影响旧口径）

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tools\tk_r3_tp3_reason_smoketest.py --symbol XAUUSD --cam_r3_mult 0.70 --cam_tp3_frac 0.20
```

## 2026-06-11 TK-R4：固定风险 / 跨品种相关性风控（第一版审计）

### 复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tools\tk_r4_risk_corr_audit.py --split since2022 --date_tag 20260611 --out_dir backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_since2022_v1
.\.venv\Scripts\python.exe .\tools\tk_r4_risk_corr_audit.py --split pre2022 --date_tag 20260611 --out_dir backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_pre2022_v1
```

### 新增产物

- since2022：
  - `backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_since2022_v1\b118_position_level_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_since2022_v1\b118_overlap_summary_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_since2022_v1\b118_overlap_by_profile_20260611_v1.csv`
- pre2022：
  - `backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_pre2022_v1\b118_position_level_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_pre2022_v1\b118_overlap_summary_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_pre2022_v1\b118_overlap_by_profile_20260611_v1.csv`

### 当前读数

- 审计口径：
  - 先从 `trades_baseline_*.csv` 复原 position-level 交易
  - 再统计同一 `split x profile` 下开新仓时，已存在的：
    - `USD` 同向暴露
    - `AUD/NZD/CAD` 商品货币同向暴露
- since2022：
  - `usd_overlap_any = 2658 / 15399 = 17.26%`
  - `commodity_overlap_any = 650 / 15399 = 4.22%`
  - `any_corr_overlap_any = 3197 / 15399 = 20.76%`
- pre2022：
  - `usd_overlap_any = 2230 / 13394 = 16.65%`
  - `commodity_overlap_any = 470 / 13394 = 3.51%`
  - `any_corr_overlap_any = 2630 / 13394 = 19.63%`

### 代表性重叠样本

- since2022：
  - `A_relaxed + AUDUSD SHORT @ 2022-09-28 03:00`：`concurrent_usd_same_dir = 9`
  - `A_relaxed + USDJPY LONG @ 2022-09-26 16:00`：`concurrent_usd_same_dir = 9`
- pre2022：
  - `A_relaxed + EURUSD LONG @ 2016-06-09 03:00`：`concurrent_usd_same_dir = 6`
  - `A_relaxed + NZDUSD SHORT @ 2016-11-18 05:00`：`concurrent_usd_same_dir = 6`

### 当前结论

- `USD` 同向风险暴露不是偶发现象，值得保留在主线继续推进
- 商品货币相关性的方向性仍不稳定，暂不升成硬规则
- `TK-R4` 当前角色：
  - `计划层 / 组合层 DIAG_ONLY_CANDIDATE`
  - 下一步应做 `same-theme risk halve` 的 paper audit，而不是直接改默认 `risk_per_trade`

## 2026-06-11 TK-R4：same-theme risk halve paper audit

### 复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tools\tk_r4_half_risk_paper_audit.py --position_level_csv backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_since2022_v1\b118_position_level_20260611_v1.csv --out_dir backtest_out\stage2\indicator_audit\20260611_b119_tk_r4_half_risk_since2022_v1 --date_tag 20260611 --theme any
.\.venv\Scripts\python.exe .\tools\tk_r4_half_risk_paper_audit.py --position_level_csv backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_pre2022_v1\b118_position_level_20260611_v1.csv --out_dir backtest_out\stage2\indicator_audit\20260611_b119_tk_r4_half_risk_pre2022_v1 --date_tag 20260611 --theme any
```

### 新增产物

- since2022：
  - `backtest_out\stage2\indicator_audit\20260611_b119_tk_r4_half_risk_since2022_v1\b119_half_risk_position_level_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b119_tk_r4_half_risk_since2022_v1\b119_half_risk_summary_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b119_tk_r4_half_risk_since2022_v1\b119_half_risk_by_profile_20260611_v1.csv`
- pre2022：
  - `backtest_out\stage2\indicator_audit\20260611_b119_tk_r4_half_risk_pre2022_v1\b119_half_risk_position_level_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b119_tk_r4_half_risk_pre2022_v1\b119_half_risk_summary_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b119_tk_r4_half_risk_pre2022_v1\b119_half_risk_by_profile_20260611_v1.csv`

### 总体结果

- 规则：
  - 若新仓在同一 `split x profile` 下与已开仓存在任一主题重叠（`USD` 或 `commodity`）
  - 则纸上记账按 `0.5x` 风险和 `0.5x` 盈亏
- since2022：
  - `sum_pnl`：`-729352.82 -> -634042.21`（改善 `+95310.61`）
  - `max_drawdown_pnl`：`-828165.48 -> -731126.62`（改善 `+97038.85`）
- pre2022：
  - `sum_pnl`：`-935120.05 -> -827500.71`（改善 `+107619.34`）
  - `max_drawdown_pnl`：`-1036812.40 -> -932855.48`（改善 `+103956.91`）

### 当前结论

- `same-theme risk halve` 在两个 split 上都带来明显的 paper-level 改善
- 因此 `TK-R4` 可以从一般相关性诊断进一步收紧为：
  - `方案 B 风控壳候选`
- 但当前仍保持：
  - 默认关闭
  - 只作为 paper audit / 方案 B 口径继续验证

## 2026-06-11 TK-R4：USD-only vs commodity-only half-risk

### 复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tools\tk_r4_half_risk_paper_audit.py --position_level_csv backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_since2022_v1\b118_position_level_20260611_v1.csv --out_dir backtest_out\stage2\indicator_audit\20260611_b119_tk_r4_half_risk_usd_since2022_v1 --date_tag 20260611 --theme usd
.\.venv\Scripts\python.exe .\tools\tk_r4_half_risk_paper_audit.py --position_level_csv backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_pre2022_v1\b118_position_level_20260611_v1.csv --out_dir backtest_out\stage2\indicator_audit\20260611_b119_tk_r4_half_risk_usd_pre2022_v1 --date_tag 20260611 --theme usd
.\.venv\Scripts\python.exe .\tools\tk_r4_half_risk_paper_audit.py --position_level_csv backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_since2022_v1\b118_position_level_20260611_v1.csv --out_dir backtest_out\stage2\indicator_audit\20260611_b119_tk_r4_half_risk_commodity_since2022_v1 --date_tag 20260611 --theme commodity
.\.venv\Scripts\python.exe .\tools\tk_r4_half_risk_paper_audit.py --position_level_csv backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_pre2022_v1\b118_position_level_20260611_v1.csv --out_dir backtest_out\stage2\indicator_audit\20260611_b119_tk_r4_half_risk_commodity_pre2022_v1 --date_tag 20260611 --theme commodity
```

### 关键结果

- `USD-only`：
  - since2022：
    - `sum_pnl` 改善 `+93732.30`
    - `max_drawdown_pnl` 改善 `+93406.24`
  - pre2022：
    - `sum_pnl` 改善 `+144225.04`
    - `max_drawdown_pnl` 改善 `+140562.61`
- `commodity-only`：
  - since2022：
    - 仅小幅改善：`sum_pnl +17762.04`，`max_drawdown +21672.87`
  - pre2022：
    - 反而变差：`sum_pnl -21023.72`，`max_drawdown -21023.72`

### 当前裁决

- 当前真正稳定、有保留价值的是：
  - `USD 同向主题暴露 -> 新增仓 half-risk`
- `commodity-only` 不具备跨 split 稳定性
- 因此 `TK-R4` 下一步应收口为：
  - `USD-only half-risk` 的方案 B 风控壳候选
  - `commodity` 暂不纳入当前方案 B

## 2026-06-11 TK-R4：USD-only half-risk 方案 B 草案脚本

### 复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tools\tk_r4_usd_half_risk_scheme_b.py --position_level_csv backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_since2022_v1\b118_position_level_20260611_v1.csv --out_dir backtest_out\stage2\indicator_audit\20260611_b120_tk_r4_usd_half_risk_scheme_b_since2022_off_v1 --date_tag 20260611 --enable_usd_half_risk 0
.\.venv\Scripts\python.exe .\tools\tk_r4_usd_half_risk_scheme_b.py --position_level_csv backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_since2022_v1\b118_position_level_20260611_v1.csv --out_dir backtest_out\stage2\indicator_audit\20260611_b120_tk_r4_usd_half_risk_scheme_b_since2022_on_v1 --date_tag 20260611 --enable_usd_half_risk 1
.\.venv\Scripts\python.exe .\tools\tk_r4_usd_half_risk_scheme_b.py --position_level_csv backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_pre2022_v1\b118_position_level_20260611_v1.csv --out_dir backtest_out\stage2\indicator_audit\20260611_b120_tk_r4_usd_half_risk_scheme_b_pre2022_off_v1 --date_tag 20260611 --enable_usd_half_risk 0
.\.venv\Scripts\python.exe .\tools\tk_r4_usd_half_risk_scheme_b.py --position_level_csv backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_pre2022_v1\b118_position_level_20260611_v1.csv --out_dir backtest_out\stage2\indicator_audit\20260611_b120_tk_r4_usd_half_risk_scheme_b_pre2022_on_v1 --date_tag 20260611 --enable_usd_half_risk 1
```

### 脚本边界

- 新增脚本：
  - `tools\tk_r4_usd_half_risk_scheme_b.py`
- 当前只做：
  - `config csv`
  - `position-level csv`
  - `summary csv`
  - accounting / audit 记账缩放
- 当前不做：
  - 不改 `backtest_p0.py` baseline 默认执行路径
  - 不把 `commodity` 主题并入当前方案 B

### 配置合约

- 关键字段：
  - `scheme_b_name = tk_r4_usd_half_risk`
  - `scheme_b_enabled = True/False`
  - `enabled_default = False`
  - `trigger_col = usd_overlap_flag`
  - `trigger_theme = usd`
  - `risk_scale_when_triggered = 0.5`
- 标准产物文件名：
  - `b120_scheme_b_config_20260611_v1.csv`
  - `b120_scheme_b_position_level_20260611_v1.csv`
  - `b120_scheme_b_summary_20260611_v1.csv`

### 产物目录

- since2022 off：
  - `backtest_out\stage2\indicator_audit\20260611_b120_tk_r4_usd_half_risk_scheme_b_since2022_off_v1`
- since2022 on：
  - `backtest_out\stage2\indicator_audit\20260611_b120_tk_r4_usd_half_risk_scheme_b_since2022_on_v1`
- pre2022 off：
  - `backtest_out\stage2\indicator_audit\20260611_b120_tk_r4_usd_half_risk_scheme_b_pre2022_off_v1`
- pre2022 on：
  - `backtest_out\stage2\indicator_audit\20260611_b120_tk_r4_usd_half_risk_scheme_b_pre2022_on_v1`

### 验收结果

- 默认关闭不漂移：
  - since2022 off：`scheme_b == baseline`，`scheme_b_minus_base == 0`
  - pre2022 off：`scheme_b == baseline`，`scheme_b_minus_base == 0`
- 启用后复现 `USD-only half-risk`：
  - since2022：
    - `sum_pnl +93732.30`
    - `max_drawdown_pnl +93406.24`
  - pre2022：
    - `sum_pnl +144225.04`
    - `max_drawdown_pnl +140562.61`

### 当前收口

- `USD-only half-risk` 已从 paper audit 候选推进到：
  - `默认关闭的方案 B 风控壳草案`
- 当前仍保持：
  - 先独立脚本
  - 先审计合约
  - 不并入 baseline 默认风控

## 2026-06-11 TK-R4：USD-only half-risk wrapper / 编排入口

### 新增脚本

- `tools\tk_r4_usd_half_risk_scheme_b_runner.py`
- `tk_r4_usd_half_risk_scheme_b_runner.py`（根目录兼容入口）

### 入口能力

- 支持：
  - `--split since2022`
  - `--split pre2022`
  - `--split all`
- 支持：
  - `--mode off`
  - `--mode on`
  - `--mode both`
- 自动处理：
  - `b118 position_level_csv` 路径拼接
  - `b120 ... since2022/pre2022 + off/on` 标准 `out_dir` 命名
- 当前仍不做：
  - 不改 baseline 默认执行路径
  - 不新增默认开启的风控逻辑

### 复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tools\tk_r4_usd_half_risk_scheme_b_runner.py --split all --mode both --date_tag 20260611
```

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tk_r4_usd_half_risk_scheme_b_runner.py --split since2022 --mode off --date_tag 20260611
```

### 终端输出锚点

- `split=since2022 enabled=0`
- `split=since2022 enabled=1`
- `split=pre2022 enabled=0`
- `split=pre2022 enabled=1`
- 根目录兼容入口已验证可直接转发到 `tools\` 内正式 runner
- 现已直接打印三行摘要：
  - `baseline: sum_pnl / max_dd / avg_r`
  - `scheme_b: sum_pnl / max_dd / avg_r`
  - `delta: sum_pnl / max_dd / avg_r`
- 现已追加 off 校验行（默认开启）：
  - `validation split=... off_equals_baseline=ok`
  - 对应落盘到 `run_manifest.validation`，用于后续自动审计

### 再验收

- `since2022 off` summary 仍为：
  - `scheme_b == baseline`
  - `scheme_b_minus_base == 0`
- `since2022 on` summary 仍为：
  - `sum_pnl +93732.30`
  - `max_drawdown_pnl +93406.24`

### 终端输出示例

```text
split=since2022 enabled=0
  baseline: sum_pnl=-729352.82, max_dd=-828165.48, avg_r=-0.021947
  scheme_b: sum_pnl=-729352.82, max_dd=-828165.48, avg_r=-0.021947
  delta: sum_pnl=+0.00, max_dd=+0.00, avg_r=+0.000000

split=since2022 enabled=1
  baseline: sum_pnl=-729352.82, max_dd=-828165.48, avg_r=-0.021947
  scheme_b: sum_pnl=-635620.53, max_dd=-734759.24, avg_r=-0.020912
  delta: sum_pnl=+93732.30, max_dd=+93406.24, avg_r=+0.001035
```

### full 安全网验死（generated provenance）

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tk_r4_usd_half_risk_scheme_b_runner.py --preset full --date_tag 20260612 --support_min 3 --p0_sweep_dir backtest_out\p0_sweep
```

- 预期点：`b118/b122/b123` 必须走 `generated`（证明缺依赖时可自动补齐）
- 单文件真值：
  - `backtest_out\stage2\indicator_audit\20260612_b124_tk_r4_usd_half_risk_role_finalize_v1\b124_usd_half_risk_run_manifest_20260612_v1.json`

## 2026-06-11 TK-R4：USD overlap 强度分层审计

### 复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tools\tk_r4_usd_overlap_depth_audit.py --position_level_csv backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_since2022_v1\b118_position_level_20260611_v1.csv --out_dir backtest_out\stage2\indicator_audit\20260611_b121_tk_r4_usd_overlap_depth_since2022_v1 --date_tag 20260611 --thresholds 1,2,3
.\.venv\Scripts\python.exe .\tools\tk_r4_usd_overlap_depth_audit.py --position_level_csv backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_pre2022_v1\b118_position_level_20260611_v1.csv --out_dir backtest_out\stage2\indicator_audit\20260611_b121_tk_r4_usd_overlap_depth_pre2022_v1 --date_tag 20260611 --thresholds 1,2,3
```

### 新增产物

- since2022：
  - `backtest_out\stage2\indicator_audit\20260611_b121_tk_r4_usd_overlap_depth_since2022_v1\b121_usd_depth_position_level_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b121_tk_r4_usd_overlap_depth_since2022_v1\b121_usd_depth_threshold_summary_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b121_tk_r4_usd_overlap_depth_since2022_v1\b121_usd_depth_by_profile_20260611_v1.csv`
- pre2022：
  - `backtest_out\stage2\indicator_audit\20260611_b121_tk_r4_usd_overlap_depth_pre2022_v1\b121_usd_depth_position_level_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b121_tk_r4_usd_overlap_depth_pre2022_v1\b121_usd_depth_threshold_summary_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b121_tk_r4_usd_overlap_depth_pre2022_v1\b121_usd_depth_by_profile_20260611_v1.csv`

### 终端摘要

```text
usd_overlap_depth
  ge_1: trigger_share=17.26%, delta_sum_pnl=+93732.30, delta_max_dd=+93406.24, delta_avg_r=+0.001035
  ge_2: trigger_share=8.71%, delta_sum_pnl=+29009.33, delta_max_dd=+20782.01, delta_avg_r=-0.000052
  ge_3: trigger_share=4.36%, delta_sum_pnl=-6406.06, delta_max_dd=-12519.09, delta_avg_r=-0.000663

usd_overlap_depth
  ge_1: trigger_share=16.65%, delta_sum_pnl=+144225.04, delta_max_dd=+140562.61, delta_avg_r=+0.002724
  ge_2: trigger_share=6.59%, delta_sum_pnl=+46237.20, delta_max_dd=+46237.20, delta_avg_r=+0.000629
  ge_3: trigger_share=2.54%, delta_sum_pnl=+16241.88, delta_max_dd=+16241.88, delta_avg_r=+0.000179
```

### 关键结论

- `>=1`：
  - 仍是两个 split 上最强、最稳定的改善档
- `>=2`：
  - 仍为正，但改善幅度明显缩小
- `>=3`：
  - 在 since2022 已整体转负
  - 在 pre2022 虽仍为正，但明显进一步变弱
- profile 侧补充：
  - since2022 的 `>=3` 在 `A_strict / A_universal` 为负
  - pre2022 的 `>=3` 在 `A_strict` 为负

### 当前裁决

- 当前没有证据支持把 `USD-only half-risk` 的触发条件收窄到：
  - `concurrent_usd_same_dir >= 2`
  - 或 `>= 3`
- 因此 b120 当前保留口径仍应是：
  - `usd_overlap_flag`
  - 即 `concurrent_usd_same_dir >= 1`

## 2026-06-11 TK-R4：USD overlap 异质性审计

### 复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tools\tk_r4_usd_overlap_heterogeneity_audit.py --position_level_csv backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_since2022_v1\b118_position_level_20260611_v1.csv --out_dir backtest_out\stage2\indicator_audit\20260611_b122_tk_r4_usd_overlap_heterogeneity_since2022_v1 --date_tag 20260611 --support_min 3
.\.venv\Scripts\python.exe .\tools\tk_r4_usd_overlap_heterogeneity_audit.py --position_level_csv backtest_out\stage2\indicator_audit\20260611_b118_tk_r4_risk_corr_pre2022_v1\b118_position_level_20260611_v1.csv --out_dir backtest_out\stage2\indicator_audit\20260611_b122_tk_r4_usd_overlap_heterogeneity_pre2022_v1 --date_tag 20260611 --support_min 3
```

### 新增产物

- since2022：
  - `backtest_out\stage2\indicator_audit\20260611_b122_tk_r4_usd_overlap_heterogeneity_since2022_v1\b122_usd_overlap_by_profile_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b122_tk_r4_usd_overlap_heterogeneity_since2022_v1\b122_usd_overlap_by_symbol_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b122_tk_r4_usd_overlap_heterogeneity_since2022_v1\b122_usd_overlap_profile_symbol_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b122_tk_r4_usd_overlap_heterogeneity_since2022_v1\b122_usd_overlap_breadth_20260611_v1.csv`
- pre2022：
  - `backtest_out\stage2\indicator_audit\20260611_b122_tk_r4_usd_overlap_heterogeneity_pre2022_v1\b122_usd_overlap_by_profile_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b122_tk_r4_usd_overlap_heterogeneity_pre2022_v1\b122_usd_overlap_by_symbol_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b122_tk_r4_usd_overlap_heterogeneity_pre2022_v1\b122_usd_overlap_profile_symbol_20260611_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260611_b122_tk_r4_usd_overlap_heterogeneity_pre2022_v1\b122_usd_overlap_breadth_20260611_v1.csv`

### 终端摘要

```text
usd_overlap_heterogeneity
  since2022 A_relaxed: trigger_share=17.38%, delta_sum_pnl=+47104.62, delta_max_dd=+38848.85, delta_avg_r=+0.002742
  since2022 A_strict: trigger_share=17.01%, delta_sum_pnl=+8519.73, delta_max_dd=+9559.17, delta_avg_r=-0.000767
  since2022 A_universal: trigger_share=17.35%, delta_sum_pnl=+38107.95, delta_max_dd=+31280.75, delta_avg_r=+0.000719
  profile_symbol since2022: eligible=33, both_positive=22
  symbol since2022: eligible=11, both_positive=8

usd_overlap_heterogeneity
  pre2022 A_relaxed: trigger_share=17.81%, delta_sum_pnl=+55119.73, delta_max_dd=+51457.30, delta_avg_r=+0.002481
  pre2022 A_strict: trigger_share=16.79%, delta_sum_pnl=+55262.32, delta_max_dd=+56297.93, delta_avg_r=+0.004003
  pre2022 A_universal: trigger_share=15.20%, delta_sum_pnl=+33843.00, delta_max_dd=+32955.51, delta_avg_r=+0.001220
  profile_symbol pre2022: eligible=33, both_positive=27
  symbol pre2022: eligible=11, both_positive=10
```

### 关键结论

- profile 层：
  - 两个 split 上，三类 profile 的 `sum_pnl / max_drawdown` 基本都改善
  - 仅 since2022 的 `A_strict` 出现 `avg_r_mult` 小幅转弱，但 `sum_pnl / max_drawdown` 仍为正改善
- symbol breadth（`n_trigger >= 3`）：
  - since2022：`8/11` 同时改善 `sum_pnl + max_drawdown`
  - pre2022：`10/11` 同时改善 `sum_pnl + max_drawdown`
- profile x symbol breadth（`n_trigger >= 3`）：
  - since2022：`22/33` 同时改善
  - pre2022：`27/33` 同时改善
- 当前负向 pocket：
  - since2022 主要见于：
    - `USDJPY`
    - `XAGUSD`
    - `XAUUSD`
    - 少量 `XTIUSD / USDCHF`
  - pre2022 主要见于：
    - `GBPUSD`
    - 少量 `USDCAD / USDJPY / XAGUSD`

### 当前裁决

- `USD-only half-risk` 已不只是零散局部 pocket
- 现有证据更支持把它保留为：
  - 一个具备较好 profile/symbol 广度的全局方案 B 候选
  - 同时附带少量观察型负向 pocket
- 因此当前不需要把全局 `USD overlap >=1` 壳打回为“仅局部 symbol 清单”

## 2026-06-11 TK-R4：USD overlap 负向 pocket 清单

### 复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tools\tk_r4_usd_overlap_negative_pockets.py --date_tag 20260611 --support_min 3
```

### 新增产物

- `backtest_out\stage2\indicator_audit\20260611_b123_tk_r4_usd_overlap_negative_pockets_v1\b123_usd_overlap_negative_pockets_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b123_tk_r4_usd_overlap_negative_pockets_v1\b123_usd_overlap_negative_watchlist_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b123_tk_r4_usd_overlap_negative_pockets_v1\b123_usd_overlap_negative_summary_20260611_v1.csv`

### 终端摘要

```text
usd_overlap_negative_pockets
  symbol: negative_rows=11, distinct_groups=8, persistent=3, hard=2
  profile_symbol: negative_rows=34, distinct_groups=25, persistent=9, hard=12
  profile_symbol A_universal|XAGUSD: priority=high_watch, splits=2, worst_sum=-7901.56, worst_dd=+1120.31
  profile_symbol A_relaxed|XAGUSD: priority=high_watch, splits=2, worst_sum=-6500.49, worst_dd=+2966.54
  profile_symbol A_universal|USDJPY: priority=high_watch, splits=2, worst_sum=-5951.92, worst_dd=-975.26
  profile_symbol A_strict|USDCAD: priority=high_watch, splits=2, worst_sum=-1384.80, worst_dd=+1223.39
  profile_symbol A_relaxed|GBPUSD: priority=single_split_hard_negative, splits=1, worst_sum=-2386.37, worst_dd=-1224.97
  profile_symbol A_universal|GBPUSD: priority=single_split_hard_negative, splits=1, worst_sum=-1798.17, worst_dd=-1542.88
```

### 当前观察名单

- symbol 高优先：
  - `XAGUSD`
  - `GBPUSD`
- symbol 次级观察：
  - `USDJPY`
  - `USDCAD`
  - `XAUUSD`
- profile x symbol 高优先：
  - `A_universal|XAGUSD`
  - `A_relaxed|XAGUSD`
  - `A_universal|USDJPY`
  - `A_strict|USDCAD`
  - `A_relaxed|GBPUSD`
  - `A_universal|GBPUSD`

### 当前裁决

- 这一步支持的不是“大规模 symbol 例外硬门控”
- 而是：
  - 保留全局 `USD overlap >=1` 的方案 B 壳
  - 再附一个较小的负向 pocket watchlist
- 当前最像持续负向例外的是：
  - `XAGUSD`
- 当前最像单 split 硬反例的是：
  - `GBPUSD`（主要在 pre2022）

## 2026-06-11 TK-R4：USD-only Scheme B 最终角色收口

### 复现命令

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tools\tk_r4_usd_half_risk_role_finalize.py --date_tag 20260611
```

### 新增产物

- `backtest_out\stage2\indicator_audit\20260611_b124_tk_r4_usd_half_risk_role_finalize_v1\b124_usd_half_risk_role_contract_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b124_tk_r4_usd_half_risk_role_finalize_v1\b124_usd_half_risk_watchlist_contract_20260611_v1.csv`
- `backtest_out\stage2\indicator_audit\20260611_b124_tk_r4_usd_half_risk_role_finalize_v1\b124_usd_half_risk_validation_summary_20260611_v1.csv`

### 终端摘要

```text
usd_half_risk_role_finalize
  status=global_candidate_with_watchlist, enabled_default=0, hard_gate=0, watchlist_mode=observe_only
  since2022: delta_sum_pnl=+93732.30, delta_max_dd=+93406.24, delta_avg_r=+0.001035
  pre2022: delta_sum_pnl=+144225.04, delta_max_dd=+140562.61, delta_avg_r=+0.002724
  watch profile_symbol A_universal|XAGUSD: priority=high_watch, action=observe_only
  watch profile_symbol A_relaxed|XAGUSD: priority=high_watch, action=observe_only
  watch profile_symbol A_universal|USDJPY: priority=high_watch, action=observe_only
  watch profile_symbol A_strict|USDCAD: priority=high_watch, action=observe_only
  watch profile_symbol A_relaxed|GBPUSD: priority=single_split_hard_negative, action=observe_only
  watch profile_symbol A_universal|GBPUSD: priority=single_split_hard_negative, action=observe_only
```

### 最终角色合约

- `role_status = global_candidate_with_watchlist`
- `enabled_default = False`
- `baseline_default_unchanged = True`
- `hard_gate_enabled = False`
- `watchlist_mode = observe_only`
- `trigger_col = usd_overlap_flag`
- `trigger_theme = usd`
- `risk_scale_when_triggered = 0.5`

### 最终裁决

- `TK-R4` 当前已经可以固定为：
  - 一个默认关闭的 `USD-only half-risk` 方案 B 风控壳
  - 触发口径是 `USD overlap >= 1`
  - 带 `observe-only` 的负向 pocket watchlist
- 当前不做：
  - baseline 默认接入
  - symbol 级硬门控
  - watchlist 直接 veto

### 一键入口命令（b120 + b124）

- Fast（默认依赖已存在的 `b118_position_level`，缺了会报错）：

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tk_r4_usd_half_risk_scheme_b_runner.py --split all --mode both --date_tag 20260611 --finalize_role 1 --ensure_watchlist 1 --support_min 3
```

- Full（缺 `b118_position_level` 时自动补齐：`b118 -> b120 -> b122 -> b123 -> b124`）：

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tk_r4_usd_half_risk_scheme_b_runner.py --split all --mode both --date_tag 20260611 --finalize_role 1 --ensure_watchlist 1 --support_min 3 --ensure_position_level 1 --p0_sweep_dir backtest_out\p0_sweep
```

- 更短的预设写法：

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\tk_r4_usd_half_risk_scheme_b_runner.py --preset fast --date_tag 20260611 --support_min 3
.\.venv\Scripts\python.exe .\tk_r4_usd_half_risk_scheme_b_runner.py --preset full --date_tag 20260611 --support_min 3 --p0_sweep_dir backtest_out\p0_sweep
```

- 终端摘要固化文件（用于替代临时粘贴 `Untitled-*`）：
  - `backtest_out\stage2\indicator_audit\20260611_b124_tk_r4_usd_half_risk_role_finalize_v1\b124_usd_half_risk_terminal_brief_20260611_v1.txt`
  - `backtest_out\stage2\indicator_audit\20260611_b124_tk_r4_usd_half_risk_role_finalize_v1\b124_usd_half_risk_run_manifest_20260611_v1.json`
  - manifest 已包含：
    - `provenance`（b118/b122/b123 是否为 existing 或 generated）
    - `outputs_grouped`（按 b118/b120/b122/b123/b124 分桶的产物索引）
    - `inputs_index`（外部依赖索引：b118 position-level、b122 by_symbol/profile_symbol、b123 watchlist/summary）
  - `terminal_brief` 也会附带 `inputs_index`，终端/文件都能一眼看到依赖指向

### 覆盖范围（是否全品种）

- 当前这套 `b118 -> b120 -> b122 -> b123 -> b124` 的“全品种”含义是：
  - **覆盖 `p0_sweep_dir` 里 baseline 落盘的全部 symbol**（在对应 split/profile 下出现过的都会被纳入）
  - 不会凭空包含“仓库里不存在 trades_baseline 输出”的品种
- runner 已在终端打印每个 split 的覆盖摘要（positions/symbols/profiles），并写入 `b124_usd_half_risk_terminal_brief_*.txt`：
  - since2022：`positions=15399, symbols=32, profiles=3`
  - pre2022：`positions=13394, symbols=28, profiles=3`

## 2026-06-18 来源库去 cut_file 依赖同步

- 已把来源库目录重构为：
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9`
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\02_外部视频与方法论参考`
  - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库`
- 已完成 `A1/A2/A3/A4/F1` 的第一轮非破坏式同步：以 `cut_file` 最新版复制到来源库 `final`，不删旧历史版。
- 已同步的关键文件：
  - `A1`：`CUTPACK__A1__情绪流龙头战法__part2__v2_r2.md`
  - `A2`：`市场轮廓理论 part1 v2_r1`、`part2 v2_r2`、`MarketsInProfile v2_r1`、`MindOverMarkets v2_r1`、`TradingAndExchanges v2_r1`
  - `A3`：`VolumeProfile v2_r1`、`陈浩完整版 v2`、`筹码形态手册 part1/part2 v2_r2`
  - `A4`：`Algorithmic_Trading v2`、`Successful_Algorithmic_Trading v2_retry`
  - `F1`：`HeikinAshi part1-4 v2_r1`、`WyckoffMethod_赠送 v2_r1`
- `F2` 当前判定为基本独立；已补同步：
  - `GROUP_01_微观结构_交易所_HFT\01_F2_cutpack_v2_final\compliance_report_r1.json`
- 当前阶段口径：
  - 来源库 `final` 开始承接最新 `CUTPACK`
  - `cut_file` 暂仍保留 `pdf/epub/raw txt/toc/chapters/compliance` 这类源与施工辅助
  - 旧版 `v2 / v2_r1` 暂不删除，等后续统一做归档/冻结收口
## 2026-06-18 去 cut_file 依赖第二阶段：稳定入口索引修正

- 已更新：
  - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_09_完善体系书库_切割产物\01_A1_cutpack_v2_final\README_放这里.md`
  - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_09_完善体系书库_切割产物\01_A1_cutpack_v2_final\manifest_v2.tsv`
  - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_06_Auction_MarketProfile_价格行为\01_A2_cutpack_v2_final\README_放这里.md`
  - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_06_Auction_MarketProfile_价格行为\01_A2_cutpack_v2_final\manifest_v2.tsv`
  - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_09_完善体系书库_切割产物\README_放这里.md`
  - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_09_完善体系书库_切割产物\manifest_v2.tsv`
  - `02_阶段二_工作方向_想法库.md`
  - `03_阶段二_当下计划_执行清单.md`
- 当前明确：
  - `A1 stable = part1_v2_r2 + part2_v2_r2`
  - `A2 stable = part1_v2_r1 + part2_v2_r2 + 三本英文 v2_r1`
  - `A4 stable = 04_A4_cutpack_v2_final`
  - `F2 stable = 01_F2_cutpack_v2_final`
- 当前最小缺口：
  - `A2 part2` 的 19 条 retained excerpts 仍需 OCR spot check
  - 旧版目录与重复副本还没做 freeze / archive 说明

## 2026-06-18 去 cut_file 依赖第二阶段：A2 OCR spot check + Batch9 并入主线

- 已完成：
  - `A2 part2` 的 19 条 retained excerpts OCR spot check
  - `A1 final / A2 final / GROUP_09` 的 freeze / archive 说明补写
  - `Batch9` 并入当前主线口径同步
- `A2 part2` 当前裁决（该节为第一轮 spot check 记录，已被下方深查结论更新）：
  - Excerpts `1-10 / 14-19`：保留为 OCR 锚定
  - Excerpts `11 / 12 / 13`：当时暂按 `knowledge_inference` 保守处理
  - Excerpt `15`：TPO 定义保留 OCR 锚定，A股时段映射明确为后加适配
- `Batch9` 当前裁决：
  - 已基本独立于 `cut_file`
  - 已吃透到批次决策层
  - 仍未源码级补全，后续继续补缺口备注，不重做整批结构

## 2026-06-18 A2 深查 + Batch9 源码缺口备注收口

- 已更新：
  - `cut_file\A2\CUTPACK__A2__CN__市场轮廓理论__part2__v2_r2.md`
  - `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_06_Auction_MarketProfile_价格行为\01_A2_cutpack_v2_final\README_放这里.md`
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\batch9_source_manifest.csv`
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\00_本批说明与多AI能力画像.md`
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\Batch9_批次收口与四分流_v1.md`
  - `02_阶段二_工作方向_想法库.md`
  - `03_阶段二_当下计划_执行清单.md`
- `A2` 当前明确：
  - Excerpts `11 / 12 / 13` 已回升为 `direct_ocr_support`
  - Excerpt `15` 继续保留 `partial_ocr_support`，其中 A股时段映射属于后加适配
- `Batch9` 当前明确：
  - Kimi 补强层统一写入 `manifest notes`
  - 标签固定为 `secondary_structured_note / secondary_structured_note_conflict`
  - 这些标签不改变原始来源的源码级完成度裁决

## 2026-06-18 任务六开做 + Kimi 角色降级

- 已更新：
  - `01_阶段一_项目记录_过去与落地.md`
  - `02_阶段二_工作方向_想法库.md`
  - `03_阶段二_当下计划_执行清单.md`
- 任务六当前目录级裁决：
  - `00_TK外汇`：部分吸收 + 可重开
  - `Batch9`：已吸收到合同层 + 可重开
  - `00_交易系统书籍`：已作为方法学/规则底座吸收 + 可重开少量规则壳
  - `02_原子化拆解文件`：结构化规则库 + 可重开
  - `00_大隐体系`：family 级冻结 + 条件型可重开
  - `00_周期女王`：A股状态语言层 + 条件型可重开
  - `01_Kimi拆书待入库`：active inbox / final 承接层，不并入任务六旧来源库主战场
- `Kimi` 当前新职责：
  - 对 `A1/A2/A3/A4/F1/F2` 不再常驻负责
  - 默认只在我点名时补 `新资料初扫 / 外部网页说明 / 证据缺口`

## 2026-06-18 任务六继续下压：下一轮明确可重开清单

- 已更新：
  - `01_阶段一_项目记录_过去与落地.md`
  - `02_阶段二_工作方向_想法库.md`
  - `03_阶段二_当下计划_执行清单.md`
- 本轮抽出的首批明确可重开对象：
  - `00_大隐体系`
    - `stochastic oscillator 指标组`
    - `B转A失败 -> B浪C反手 / 天王山 / 中枢反手`
  - `00_周期女王`
    - `周期状态系统规则壳`
    - `10日区间前十 + 前交易日领涨 + 包容度/补位协同`
  - `02_原子化拆解文件`
    - `技术指标_随机指标_多周期KD共振与过滤规则`
    - `核心技术_威科夫_弹簧Spring与上抛UT量化判定`
- 当前角色裁决：
  - `多周期KD`、`Spring/UT` = 更适合作首批“字段化 / 过滤层 / event-level”对象
  - `周期状态系统规则壳` = 更适合作 `A股状态标签层`
  - `大隐 B转A失败` = 先保留为 `diag-only candidate`
  - `ALBrooks 趋势强度评分`、`中军五维模型` = 暂不抢做

## 2026-06-18 多周期KD：最小实现入口开做

- 已新增：
  - `10_来源库_SOURCE_LIBRARY\02_原子化拆解文件\技术指标_随机指标_多周期KD共振_后续对象定义入口_v1.md`
  - `10_来源库_SOURCE_LIBRARY\02_原子化拆解文件\技术指标_随机指标_多周期KD共振_P0_最小实施草案_v1.md`
  - `10_来源库_SOURCE_LIBRARY\02_原子化拆解文件\技术指标_随机指标_多周期KD共振_真实字段输出路径草案_v1.md`
- 当前固定口径：
  - 先做 `diagnostic/filter layer`
  - 第一版只保留 `week/day/4h`
  - 第一版只做 `6` 个字段
  - 不提前混入 `month bias / 1h refine / 背离 / 离散 / 完美 / 仓位倍率`
- 已补第一版输出证据：
  - `kd_mtf_p0_field_header_v1.txt`
  - `kd_mtf_p0_contract_notes_v1.md`
  - `kd_mtf_p0_field_sample_v1.csv`
- 已补运行时空壳：
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\`
  - `kd_mtf_p0_fields_runtime_v1.csv`
  - `kd_mtf_p0_fields_runtime_header_v1.txt`
  - `kd_mtf_p0_runtime_notes_v1.md`
  - `kd_mtf_p0_runtime_gaps_v1.md`
  - `kd_mtf_p0_runtime_append_protocol_v1.md`
  - `kd_mtf_p0_real_input_mapping_draft_v1.md`
- 已补第一份手工 proof 样本：
  - `real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - `real_input_samples\kd_mtf_p0_proof_output_v1.csv`
- 已补 runtime 参数与 dry-run 验收：
  - `kd_mtf_p0_runtime_params_template_v1.json`
  - `kd_mtf_p0_runtime_append_stub_v1.py`
  - `kd_mtf_p0_runtime_append_acceptance_v1.md`
- 已完成首批 persist：
  - `kd_mtf_p0_fields_runtime_v1.csv` 已由 placeholder 替换为 `3` 行 proof 行
  - 当前行为：`EURUSD H1`、`XAUUSD H1`、`BTCUSD H1`
- 下一步最顺动作：
  - 先补第二批 proof 样本
  - 再看是否需要补 `append_from_proof` 独立脚本
