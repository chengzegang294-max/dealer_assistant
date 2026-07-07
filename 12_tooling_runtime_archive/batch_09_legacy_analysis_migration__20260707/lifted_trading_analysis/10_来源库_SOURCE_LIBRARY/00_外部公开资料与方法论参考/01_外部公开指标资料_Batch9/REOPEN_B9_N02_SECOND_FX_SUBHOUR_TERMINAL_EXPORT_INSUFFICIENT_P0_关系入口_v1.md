# REOPEN_B9_N02_SECOND_FX_SUBHOUR_TERMINAL_EXPORT_INSUFFICIENT_P0 关系入口 v1

## 作用

- 对 `TradeMaxGlobal-Demo__60088394` 的 `GBPUSD/M15 terminal export` 做关系入口级收口。
- 当前专门记录“export 已跑通，但结果仍不足以进入 ingest”的真实停点。

## 当前边界（写死）

- 不写入：
  - `real_input_samples\n02_real_input_gbpusd_m15_v1.csv`
  - `n02_proof_of_mapping_output_gbpusd_m15_v1.csv`
  - `n02_ib_proof_of_mapping_output_gbpusd_m15_v1.csv`
  - 任意 `failed breakout` 相关定义
- 当前不把：
  - `MT5_bars_export_GBPUSD_M15_*.csv`
  直接冒充成 `GBPUSD/M15 canonical export`

## 当前真值组成（v1）

- `entry_md`：`REOPEN_B9_N02_SECOND_FX_SUBHOUR_TERMINAL_EXPORT_INSUFFICIENT_P0_关系入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_terminal_export_insufficient_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_terminal_export_insufficient_acceptance_v1.md`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_terminal_export_insufficient_build_v1.py`
- `summary_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_terminal_export_insufficient_summary_v1.md`
- `summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_terminal_export_insufficient_summary_v1.json`

## 最小验收（关系开题级）

- terminal export summary 必须显式记录：
  - `process_exited`
  - `requested_symbol_timeframe`
  - `input_export_tf_value`
  - `tester_chart_tf`
  - `tester_export_tf`
  - `tester_bars_generated`
  - `csv_row_count`
  - `csv_unique_minute_components`
  - `observed_subhour_output`
  - `do_not_ingest_current_export`
  - `preferred_next_step`
- 所有输出都必须显式保留：
  - `writes_main_m1_runtime=false`
  - `is_acquisition_only=true`
  - `declares_canonical_export_done=false`

## 2026-07-05 fresh-run

- 运行入口：
  - `python n02_second_fx_subhour_terminal_export_insufficient_build_v1.py`
- 关键统计：
  - `process_exited=true`
  - `requested_symbol_timeframe=GBPUSD/M15`
  - `input_export_tf_value=15`
  - `tester_chart_tf=PERIOD_M15`
  - `tester_export_tf=PERIOD_M15`
  - `tester_bars_generated=96`
  - `csv_row_count=2287`
  - `csv_unique_minute_components=["00"]`
  - `observed_subhour_output=false`
  - `status=terminal_export_completed_but_subhour_not_observed`
- 当前裁决：
  - terminal export 链路已经真实跑通，但当前导出结果仍不足以进入 ingest。
  - 主线下一步固定为：
    - `build_or_reuse_hcc_reader_then_convert_to_canonical_bars`

## provenance 说明

- 当前关系入口以 `mq5 / ini / ps1 / run_summary / tester_log / terminal_log / export csv` 共同收口。
- 本目录及同名产物承担新仓镜像回填与主线索引职责。
