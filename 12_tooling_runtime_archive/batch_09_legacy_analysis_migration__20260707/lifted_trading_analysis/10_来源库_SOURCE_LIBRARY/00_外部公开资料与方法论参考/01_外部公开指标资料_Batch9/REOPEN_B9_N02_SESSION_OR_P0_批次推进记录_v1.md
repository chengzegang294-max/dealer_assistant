# REOPEN_B9_N02_SESSION_OR_P0 批次推进记录 v1

## 作用

- 这份文档专门记录 `Batch9` 第一项重开是怎样一步步从“来源收集”推进到“可实施”的。
- 它不是字段定义文档，也不是运行说明，而是给主线回看时用的推进索引。

## 推进链路

### 第 1 步：类型裁决

- 在 `Batch9` 开题阶段，先把外部指标类型拆成：
  - `N01`
  - `N02`
  - `N03`
  - `N04/N05/N06`
- 其中 `N02 sessions / open-range / time-window context` 被裁定为立即收集类型。

### 第 2 步：公开来源收集

- 已收：
  - `opening_range_breakout__joveteo.pine`
  - `README__joveteo_orb.md`
  - `USER_GUIDE__joveteo_orb.md`
  - `Initial_Balance_Breakout__page_excerpt.md`
- 结论：
  - `N02` 是三类里当前证据最稳、最适合先重开的一组。

### 第 3 步：字段合同化

- 已形成：
  - `N02_字段草案_v1.md`
  - `N02_P0_字段落盘草案_v1.md`
  - `Batch9_P0_统一字段_CSV草案_v1.csv`
- 结论：
  - `N02` 已具备最小 `P0` 字段合同。

### 第 4 步：批次收口与四分流

- 已新增：
  - `Batch9_批次收口与四分流_v1.md`
- 裁决：
  - `REOPEN_B9_N02_SESSION_OR_P0`
  - 进入 Batch9 首批量化重开优先项

### 第 5 步：最小实施草案

- 已新增：
  - `REOPEN_B9_N02_SESSION_OR_P0_最小实施草案_v1.md`
- 固定内容：
  - 第一版只做 `12` 个 `N02 P0` 字段
  - 不混入 `IB / acceptance / failed breakout`
  - 不做硬门控

### 第 6 步：第一版输出证据

- 已新增：
  - `n02_p0_field_sample_v1.csv`
  - `n02_p0_field_header_v1.txt`
  - `n02_p0_contract_notes_v1.md`
- 结论：
  - 已从“只有草案”推进到“已有表头、空值、默认值、枚举样本证据”。

### 第 7 步：真实输出路径草案

- 已新增：
  - `REOPEN_B9_N02_SESSION_OR_P0_真实字段输出路径草案_v1.md`
- 结论：
  - 下一阶段真实运行产物应落到哪里、叫什么、各自承担什么角色，已经固定。

### 第 8 步：工具运行时空壳落地

- 已新增目录：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\`
- 已新增：
  - `n02_p0_fields_runtime_v1.csv`
  - `n02_p0_fields_runtime_header_v1.txt`
  - `n02_p0_runtime_notes_v1.md`
  - `n02_p0_runtime_gaps_v1.md`
- 结论：
  - `REOPEN_B9_N02_SESSION_OR_P0` 已正式跨过来源库阶段，进入工具运行时阶段。

### 第 9 步：占位样本行与追加协议

- 已新增：
  - `n02_p0_runtime_append_protocol_v1.md`
- 已推进：
  - `n02_p0_fields_runtime_v1.csv` 中写入 `1` 行明确标识的占位样本行
- 结论：
  - 运行时目录不再只是空壳
  - 已固定“先删或覆盖占位行，再写第一批真实数据”的最小执行顺序

### 第 10 步：stub 的 dry-run / persist 验证

- 已继续推进：
  - `n02_p0_runtime_append_stub_v1.py`
- 已验证：
  - 默认 `dry-run` 只打印示例行，不写回 CSV
  - 可选 `--persist` 会先清理 placeholder 与旧示例行，再只保留 `1` 条示例行写回
- 当前结果：
  - `n02_p0_fields_runtime_v1.csv` 里的 placeholder 已被示例行替换
  - 但这条示例行仍不是“真实 runtime 数据”

### 第 11 步：session binding 从示例默认值推进到批次冻结口径

- 已推进：
  - `session_id = london`
    - 已从单个示例上下文升级为 `project_contract_default`
  - `session_timezone = Europe/London`
    - 已与 `london` 一起升级为 v1 冻结 binding
  - 已新增：
    - `session_binding_registry`
      - `london -> Europe/London`
      - `new_york -> America/New_York`
- 依据：
  - `REOPEN_B9_N02_SESSION_OR_P0_最小实施草案_v1.md`
  - `n02_p0_field_sample_v1.csv`
- 当前结果：
  - `N02` 不再只是“单条示例 session 默认值”
  - 而是已有最小可复用 session binding 表

### 第 12 步：session binding 再补 DST / 日历边界

- 已推进：
  - `session_binding_registry` 中的每个 session 继续补了：
    - `calendar_basis`
    - `dst_handling`
- 当前要求：
  - `london` 按 `Europe/London` 本地日期解释 session 日历
  - `new_york` 按 `America/New_York` 本地日期解释 session 日历
  - DST 必须由时区规则推导，不能手写固定 UTC 偏移
- 当前结果：
  - `N02` 的 session binding 已不只是“名称映射”
  - 而是进一步具备最小时区与日历审计边界

### 第 13 步：真实接入前 session calendar / DST 验收清单落地

- 已新增：
  - `n02_p0_runtime_session_calendar_dst_checklist_v1.md`
- 当前作用：
  - 在第一份真实 runtime 数据接入前，固定 session / timezone / local date / DST 的最小验收顺序
- 当前结果：
  - `N02` 已不只是“binding 冻结”
  - 还具备了真实接入前的固定 checklist

### 第 14 步：真实数据接入前最小输入映射草案

- 已新增：
  - `n02_p0_real_input_mapping_draft_v1.md`
- 当前作用：
  - 固定 `bar_time/open/high/low/close + session binding registry` 如何映射到当前 N02 P0 输出字段
- 当前结果：
  - `N02` 已具备真实接入前的输入映射草案
  - 后续第一份真实数据可以直接按草案做 proof-of-mapping

## 当前状态

- 当前角色：`in_progress`
- 当前准确描述：
  - 已完成类型裁决
  - 已完成来源收集
  - 已完成字段合同化
  - 已完成第一版样本证据
  - 已完成真实输出路径草案
  - 已完成工具运行时空壳
  - 已完成占位样本行与追加协议
  - 已完成 stub 的 dry-run / persist 示例行验证
  - 已完成 session binding 冻结口径升级
  - 已完成 DST / 日历边界补充
  - 已完成真实接入前 session calendar / DST 验收清单
  - 已完成真实数据接入前最小输入映射草案
- 当前还没完成：
  - 基于“项目外 MT4/MT5 导出 CSV”的接入复现（`n02_mt5_export_ingest_v1.py`）
  - `IB acceptance / failed breakout`（仍不在本 reopen 主线的第一段范围）

## 当前怎么用（主线入口）

- 想知道这条 reopen 主线做到哪：只看本文档 `推进链路/当前状态/下一步`
- 想看当前已落盘的 `N02 P0` runtime 口径与文件：看 `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_p0_runtime_notes_v2.md`
- 想继续推进 `IB`（不污染 `N02 P0`）：看 `REOPEN_B9_N02_IB_后续对象定义入口_v1.md`，先跑 `IB proof-of-mapping`
  - `IB contract notes`：`n02_ib_contract_notes_v1.md`
  - `IB runtime notes`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_runtime_notes_v1.md`
  - `IB runtime CSV`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_fields_runtime_v1.csv`
  - `IB reopen 子项入口`：`REOPEN_B9_N02_IB_OBJECT_P0_对象入口_v1.md`
  - `IB vs OR relation 入口`：`REOPEN_B9_N02_IB_OR_RELATION_P0_关系入口_v1.md`
  - `IB vs OR first_break relative 入口`：`REOPEN_B9_N02_IB_OR_FIRST_BREAK_RELATIVE_P0_关系入口_v1.md`
  - `IB vs OR break_bar evidence 入口`：`REOPEN_B9_N02_IB_OR_BREAK_BAR_EVIDENCE_P0_关系入口_v1.md`
  - `IB vs OR cross outcome split 入口`：`REOPEN_B9_N02_IB_OR_CROSS_OUTCOME_SPLIT_P0_关系入口_v1.md`
  - `IB vs OR post_cross_path 入口`：`REOPEN_B9_N02_IB_OR_POST_CROSS_PATH_P0_关系入口_v1.md`
  - `IB vs OR return_inside/session_close split 入口`：`REOPEN_B9_N02_IB_OR_RETURN_INSIDE_AND_SESSION_CLOSE_SPLIT_P0_关系入口_v1.md`
  - `IB vs OR session_close branch cards 入口`：`REOPEN_B9_N02_IB_OR_SESSION_CLOSE_BRANCH_CARDS_P0_关系入口_v1.md`
  - `IB vs OR next session continuation/stability 入口`：`REOPEN_B9_N02_IB_OR_NEXT_SESSION_CONTINUATION_STABILITY_P0_关系入口_v1.md`
  - `IB vs OR next session branch cards 入口`：`REOPEN_B9_N02_IB_OR_NEXT_SESSION_BRANCH_CARDS_P0_关系入口_v1.md`
  - `IB vs OR multi-session persistence/stability 入口`：`REOPEN_B9_N02_IB_OR_MULTI_SESSION_PERSISTENCE_STABILITY_P0_关系入口_v1.md`
  - `IB vs OR multi-session branch cards 入口`：`REOPEN_B9_N02_IB_OR_MULTI_SESSION_BRANCH_CARDS_P0_关系入口_v1.md`
  - `IB vs OR third same-session persistence/stability 入口`：`REOPEN_B9_N02_IB_OR_THIRD_SAME_SESSION_PERSISTENCE_STABILITY_P0_关系入口_v1.md`
  - `IB vs OR third same-session branch cards 入口`：`REOPEN_B9_N02_IB_OR_THIRD_SAME_SESSION_BRANCH_CARDS_P0_关系入口_v1.md`
  - `IB vs OR third same-session terminal summary 入口`：`REOPEN_B9_N02_IB_OR_THIRD_SAME_SESSION_TERMINAL_SUMMARY_P0_关系入口_v1.md`
  - `N02 other timeframe validation 入口`：`REOPEN_B9_N02_OTHER_TIMEFRAME_VALIDATION_EURUSD_M5_FALL_DST_P0_关系入口_v1.md`
  - `N02 wider history validation 入口`：`REOPEN_B9_N02_WIDER_HISTORY_VALIDATION_EURUSD_M5_FROM_M1_P0_关系入口_v1.md`
  - `N02 other symbol validation 入口`：`REOPEN_B9_N02_OTHER_SYMBOL_VALIDATION_XAUUSD_M1_TAIL_P0_关系入口_v1.md`
  - `N02 other symbol + other timeframe validation 入口`：`REOPEN_B9_N02_OTHER_SYMBOL_OTHER_TIMEFRAME_VALIDATION_XAUUSD_M5_P0_关系入口_v1.md`
  - `N02 second FX symbol input gate 入口`：`REOPEN_B9_N02_SECOND_FX_SYMBOL_INPUT_GATE_GBPUSD_H1_P0_关系入口_v1.md`
  - `IB vs OR relation runtime notes`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_relation_runtime_notes_v1.md`
  - `IB vs OR relation acceptance`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_relation_acceptance_v1.md`
  - 推荐命令（按 session 定向采样 + 跳过边界残缺日）：
    - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_ib_proof_of_mapping_v1.py --session-input london=n02_first_real_input_bars_v1.csv --session-input london=n02_dst_london_spring_20260327_20260331_bars.csv --session-input new_york=n02_first_real_input_bars_v1.csv --session-input new_york=n02_dst_newyork_spring_20260306_20260310_bars.csv --symbol EURUSD --timeframe M1 --skip-partial-days`

## 为什么先做 N02

- `N02` 是环境锚点层，不是复杂策略层。
- 它对后续 `N01 / N03 / IB` 都有共用价值。
- 它比 `N03` 更少重绘与审计歧义。
- 它比直接重开 `IB` 更容易先形成稳定字段底座。

## 对主线的意义

- `Batch9` 现在已经不只是“收网页资料”。
- `REOPEN_B9_N02_SESSION_OR_P0` 证明：
  - Batch9 可以像前几批一样，先收口，再选首批重开项，再逐步形成实现证据。

## 最近推进

- `2026-07-04 third same-session terminal summary` 已继续推进到：
  - `other timeframe validation (EURUSD M5 fall DST)` fresh-run
  - `wider history validation (EURUSD M5 from main M1)` fresh-run
  - `other symbol validation (XAUUSD M1 tail)` fresh-run
  - `other symbol + other timeframe validation (XAUUSD M5 jobs)` fresh-run
  - `second FX symbol input gate (GBPUSD H1)` fresh-run
  - `second FX sub-hour input gate` fresh-run
  - `second FX sub-hour input acquisition` fresh-run
  - `second FX sub-hour input cache recovery ready` fresh-run
  - `second FX sub-hour terminal export insufficient` fresh-run
- 已新增入口：
  - `REOPEN_B9_N02_IB_OR_THIRD_SAME_SESSION_PERSISTENCE_STABILITY_P0_关系入口_v1.md`
  - `REOPEN_B9_N02_IB_OR_THIRD_SAME_SESSION_BRANCH_CARDS_P0_关系入口_v1.md`
  - `REOPEN_B9_N02_IB_OR_THIRD_SAME_SESSION_TERMINAL_SUMMARY_P0_关系入口_v1.md`
  - `REOPEN_B9_N02_WIDER_HISTORY_VALIDATION_EURUSD_M5_FROM_M1_P0_关系入口_v1.md`
  - `REOPEN_B9_N02_OTHER_SYMBOL_VALIDATION_XAUUSD_M1_TAIL_P0_关系入口_v1.md`
  - `REOPEN_B9_N02_OTHER_SYMBOL_OTHER_TIMEFRAME_VALIDATION_XAUUSD_M5_P0_关系入口_v1.md`
  - `REOPEN_B9_N02_SECOND_FX_SYMBOL_INPUT_GATE_GBPUSD_H1_P0_关系入口_v1.md`
  - `REOPEN_B9_N02_SECOND_FX_SUBHOUR_INPUT_GATE_P0_关系入口_v1.md`
  - `REOPEN_B9_N02_SECOND_FX_SUBHOUR_INPUT_ACQUISITION_P0_关系入口_v1.md`
  - `REOPEN_B9_N02_SECOND_FX_SUBHOUR_INPUT_CACHE_RECOVERY_READY_P0_关系入口_v1.md`
  - `REOPEN_B9_N02_SECOND_FX_SUBHOUR_TERMINAL_EXPORT_INSUFFICIENT_P0_关系入口_v1.md`
- 已新增生成脚本：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_third_same_session_persistence_and_stability_p0_build_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_third_same_session_persistence_and_stability_cards_p0_build_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_third_same_session_terminal_summary_build_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_expand_real_input_with_dst_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_other_timeframe_validation_eurusd_m5_fall_dst_build_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_aggregate_bars_to_m5_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_wider_history_validation_eurusd_m5_from_m1_build_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_other_symbol_validation_xauusd_m1_tail_build_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_other_symbol_other_timeframe_validation_xauusd_m5_build_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_symbol_input_gate_gbpusd_h1_build_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_gate_build_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_acquisition_build_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_cache_recovery_ready_build_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_terminal_export_insufficient_build_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_historical_recovery_gbpusd_m15_build_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_gbpusd_m15_candidate_slice_build_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_gbpusd_m15_slice_downstream_summary_build_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_or_break_only_same_day_session_close_split_p0_build_v1.py`
- 已新增产物：
  - `n02_ib_or_beyond_third_same_session_persistence_observation_p0_sample_v1.csv`
  - `n02_ib_or_beyond_third_same_session_persistence_observation_p0_summary_v1.json`
  - `n02_ib_or_not_beyond_third_same_session_stability_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_third_same_session_stability_observation_p0_summary_v1.json`
  - `n02_ib_or_beyond_third_same_session_persistence_card_v1.md`
  - `n02_ib_or_beyond_third_same_session_persistence_card_summary_v1.json`
  - `n02_ib_or_not_beyond_third_same_session_stability_card_v1.md`
  - `n02_ib_or_not_beyond_third_same_session_stability_card_summary_v1.json`
  - `n02_ib_or_third_same_session_terminal_summary_v1.md`
  - `n02_ib_or_third_same_session_terminal_summary_v1.json`
  - `real_input_samples\n02_real_input_eurusd_m5_fall_dst_v1.csv`
  - `real_input_samples\n02_real_input_eurusd_m5_fall_dst_report_v1.json`
  - `real_input_samples\n02_proof_of_mapping_output_eurusd_m5_fall_dst_v1.csv`
  - `real_input_samples\n02_ib_proof_of_mapping_output_eurusd_m5_fall_dst_v1.csv`
  - `n02_other_timeframe_validation_eurusd_m5_fall_dst_summary_v1.md`
  - `n02_other_timeframe_validation_eurusd_m5_fall_dst_summary_v1.json`
  - `real_input_samples\n02_real_input_eurusd_m5_from_m1_main_v1.csv`
  - `real_input_samples\n02_real_input_eurusd_m5_from_m1_main_report_v1.json`
  - `real_input_samples\n02_proof_of_mapping_output_eurusd_m5_from_m1_main_v1.csv`
  - `real_input_samples\n02_ib_proof_of_mapping_output_eurusd_m5_from_m1_main_v1.csv`
  - `n02_wider_history_validation_eurusd_m5_from_m1_summary_v1.md`
  - `n02_wider_history_validation_eurusd_m5_from_m1_summary_v1.json`
  - `real_input_samples\n02_real_input_xauusd_m1_tail_v1.csv`
  - `real_input_samples\n02_proof_of_mapping_output_xauusd_m1_tail_v1.csv`
  - `real_input_samples\n02_ib_proof_of_mapping_output_xauusd_m1_tail_v1.csv`
  - `n02_other_symbol_validation_xauusd_m1_tail_summary_v1.md`
  - `n02_other_symbol_validation_xauusd_m1_tail_summary_v1.json`
  - `real_input_samples\n02_real_input_xauusd_m5_jobs_v1.csv`
  - `real_input_samples\n02_proof_of_mapping_output_xauusd_m5_jobs_v1.csv`
  - `real_input_samples\n02_ib_proof_of_mapping_output_xauusd_m5_jobs_v1.csv`
  - `n02_other_symbol_other_timeframe_validation_xauusd_m5_summary_v1.md`
  - `n02_other_symbol_other_timeframe_validation_xauusd_m5_summary_v1.json`
  - `real_input_samples\n02_real_input_gbpusd_h1_v1.csv`
  - `real_input_samples\n02_ib_proof_of_mapping_output_gbpusd_h1_v1.csv`
  - `n02_second_fx_symbol_input_gate_gbpusd_h1_summary_v1.md`
  - `n02_second_fx_symbol_input_gate_gbpusd_h1_summary_v1.json`
  - `n02_second_fx_subhour_input_gate_summary_v1.md`
  - `n02_second_fx_subhour_input_gate_summary_v1.json`
  - `n02_second_fx_subhour_input_acquisition_summary_v1.md`
  - `n02_second_fx_subhour_input_acquisition_summary_v1.json`
  - `n02_second_fx_subhour_input_cache_recovery_ready_summary_v1.md`
  - `n02_second_fx_subhour_input_cache_recovery_ready_summary_v1.json`
  - `n02_second_fx_subhour_terminal_export_insufficient_summary_v1.md`
  - `n02_second_fx_subhour_terminal_export_insufficient_summary_v1.json`
  - `real_input_samples\n02_real_input_gbpusd_m15_v1.csv`
  - `real_input_samples\n02_real_input_gbpusd_m15_report_v1.json`
  - `real_input_samples\n02_proof_of_mapping_output_gbpusd_m15_v1.csv`
  - `real_input_samples\n02_ib_proof_of_mapping_output_gbpusd_m15_v1.csv`
  - `n02_second_fx_subhour_historical_recovery_gbpusd_m15_summary_v1.md`
  - `n02_second_fx_subhour_historical_recovery_gbpusd_m15_summary_v1.json`
  - `n02_p0_fields_runtime_gbpusd_m15_slice_v1.csv`
  - `n02_ib_fields_runtime_gbpusd_m15_slice_v1.csv`
  - `n02_gbpusd_m15_candidate_slice_summary_v1.json`
  - `n02_gbpusd_m15_slice_downstream_summary_v1.md`
  - `n02_gbpusd_m15_slice_downstream_summary_v1.json`
  - `n02_ib_or_third_same_session_terminal_summary_gbpusd_m15_slice_v1.md`
  - `n02_ib_or_third_same_session_terminal_summary_gbpusd_m15_slice_v1.json`
  - `n02_ib_or_or_break_only_same_day_session_close_split_p0_summary_gbpusd_m15_slice_v1.json`
  - `n02_ib_or_or_break_only_session_close_beyond_or_card_gbpusd_m15_slice_v1.md`
  - `n02_ib_or_or_break_only_session_close_beyond_or_summary_gbpusd_m15_slice_v1.json`
  - `n02_ib_or_or_break_only_session_close_not_beyond_or_card_gbpusd_m15_slice_v1.md`
  - `n02_ib_or_or_break_only_session_close_not_beyond_or_summary_gbpusd_m15_slice_v1.json`
- 当前结果：
  - `beyond third same-session persistence=2/2`
  - `not_beyond third same-session stability missing=1/1`
  - `terminal_summary resolved=2/3, missing=1/3`
  - `m5_validation or_defined=10/15, ib_defined=10/10`
  - `m5_wider_history bars=19840, or_defined=138/165, ib_defined=138/138`
  - `xauusd_m1_validation bars=20000, or_defined=30/37, ib_defined=30/30`
  - `xauusd_m5_validation bars=70880, or_defined=516/601, ib_defined=516/516`
  - `gbpusd_h1_input_gate fx_h1_symbols=19, bars=64897, ib_defined=5412/5414, or_gate=blocked_by_timeframe_granularity`
  - `second_fx_subhour_input_gate fx_subhour_file_count=11, fx_subhour_symbols=["EURUSD"], second_fx_subhour_symbol_count=0, gate=blocked_by_missing_second_fx_subhour_input`
  - `second_fx_subhour_input_acquisition data_subhour=11, mt4_subhour=8, combined_second_fx_subhour=0, higher_tf_only=["GBPUSD","USDCHF","USDJPY"], recommended_target=GBPUSD/M15`
  - `second_fx_subhour_input_cache_recovery_ready repo_drop_gbpusd_m15=0, mt5_hcc=6, ticks_dat=true, probe_csv=4, repo_log_matches=10, recovery_status=cache_recovery_ready_without_canonical_export`
  - `second_fx_subhour_terminal_export_insufficient process_exited=true, requested_symbol_timeframe=GBPUSD/M15, input_export_tf=15, tester_bars_generated=96, csv_row_count=2287, csv_minute_components=["00"], observed_subhour_output=false`
  - `second_fx_subhour_historical_recovery_gbpusd_m15 bars=19032, minute_components=["00","15","30","45"], or_defined=396/457, ib_defined=396/457, gate=historical_recovered_second_fx_subhour_ready`
  - `gbpusd_m15_slice_runtime or=457/396, ib=457/396`
  - `gbpusd_m15_slice_first_break_relative case_counts={"no_break":23,"or_break_with_ib_same_side_gap_remaining":325,"shared_edge_break":48}`
  - `gbpusd_m15_slice_cross_split confirmed=48, or_break_only=325, no_break=23`
  - `gbpusd_m15_slice_terminal total=11, resolved=8, missing=3`
  - `gbpusd_m15_slice_or_break_only_same_day_session_close return_inside_or=312, close_beyond_or=168, close_not_beyond_or=157`
  - `gbpusd_m15_slice_or_break_only_beyond_next_session all_closes=105, not_all=23, missing=40`
  - `gbpusd_m15_slice_or_break_only_beyond_multi_session all_closes=57, not_all=21, missing=27`
  - `gbpusd_m15_slice_gate=gbpusd_m15_slice_downstream_plus_or_break_only_beyond_multi_session_persistence_done_without_failed_breakout`
- 当前边界：
  - 仍只写 observation/card/terminal summary/validation，不升级成 `failed breakout`
  - `XAUUSD/M5 jobs` 当前 `source_timezone=UTC` 仍沿用 `mt_exports_drop` 家族口径，未升级成独立价窗硬证据
  - `GBPUSD/H1` 当前只收口为 `input gate`，不强写成 `30m OR` validation 成功
  - `second FX sub-hour` 当前只收口为 `input gate`，不伪装成已存在第二个 FX sub-hour validation 样本
  - `second FX sub-hour acquisition` 当前只收口为已知源盘点，不伪装成已完成外部导出或历史回收
  - `second FX sub-hour cache recovery ready` 当前只收口为 `MT5 cache + log + drop gap` 的真实盘点，不伪装成已完成 `GBPUSD/M15 canonical export`
  - `second FX sub-hour terminal export insufficient` 当前只收口为 terminal export 已跑通但仍只见整点 bars，不伪装成已完成 `GBPUSD/M15 ingest`
  - `second FX sub-hour historical recovery GBPUSD/M15` 当前只收口为 `historical_recovered canonical bars + OR/IB proof`，不冒充成 `TMGM terminal fresh export`
  - `GBPUSD/M15 slice downstream` 当前只收口为 `historical_recovered -> slice runtime -> terminal summary + or_break_only same-day session close`，不污染主 runtime，不升级成 `failed breakout`
  - `GBPUSD/M15 slice or_break_only beyond multi-session persistence` 当前只收口为 `session_close_beyond_or -> next same-session first 30m -> second next-session first 30m` 观察，不升级成 `failed breakout`

## 下一步

- 若继续推进同一条线，下一步应是：
  - 保持 `gbpusd_m15_slice_downstream_plus_or_break_only_beyond_multi_session_persistence_done_without_failed_breakout`
  - 仅在确有需要时再扩 `or_break_only beyond multi-session all-closes` 分支
- 若暂时不接代码，也应保持：
  - `N02` 作为已完成的环境锚点层继续稳定
  - `IB` 及其 relation 继续作为 `N02` 的第一顺位下游
- 与 `01_Kimi拆书待入库\GROUP_06` 的新衔接：
  - 当前已补：
    - `GROUP_06_to_N02_对象候选清单_v1.md`
    - `REOPEN_B9_N02_IB_后续对象定义入口_v1.md`
  - 当前把 `GROUP_06` 中最贴近 `N02` 的对象收敛为：
    - 第一优先：`IB`
    - 第二优先：`VA / POC`
    - 第三优先：`Balance vs Imbalance / Day Type`
  - 当前又进一步把：
    - `IB`
    从“候选对象”推进成了“更明确的后续对象定义入口”
  - 当前写法固定为：
    - `OR` 继续留在 `N02 P0`
    - `IB` 作为 `N02` 后续对象层第一入口
    - 仍不把 `IB` 反向塞回当前 `N02 P0`
  - 处理原则仍保持：
    - 这些对象先作为 `N02` 后续对象候选层
    - 不反向污染当前 `N02 P0` 合约

### 真实接入最小复现命令（v1）

- 先检查 drop 目录里可用的导出 CSV：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_mt5_export_ingest_v1.py --symbol EURUSD --timeframe M1 --source-timezone <SOURCE_TZ> --list-drop`
- 再 ingest 进 repo 内 canonical bars（可选：`--latest` 直接取 drop 目录最新文件）：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_mt5_export_ingest_v1.py --latest --symbol EURUSD --timeframe M1 --source-timezone <SOURCE_TZ> --dest 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_first_real_input_bars_v1.csv`
- 跑 N02 P0 proof：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py`
- append 到 runtime v2：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_p0_runtime_append_from_proof_v2.py --persist`
