# n02_second_fx_subhour_terminal_export_insufficient_acceptance v1

## 目的

- 记录 `REOPEN_B9_N02_SECOND_FX_SUBHOUR_TERMINAL_EXPORT_INSUFFICIENT_P0` 的最小验收结论。

## 本次验收对象

- 生成器：
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\MT5BarExportProbe.mq5`
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\MT5BarExportProbe.ini`
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\run_mt5_bar_export_once.ps1`
  - `n02_second_fx_subhour_terminal_export_insufficient_build_v1.py`
- 实跑归档：
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\mt5_bar_export\fix2_gbpusd_m15_short_tmgm_20260705T1737`
- 输出：
  - `n02_second_fx_subhour_terminal_export_insufficient_summary_v1.md`
  - `n02_second_fx_subhour_terminal_export_insufficient_summary_v1.json`

## 2026-07-05 fresh-run 验收

- 本轮结果：
  - `process_exited=true`
  - `requested_symbol_timeframe=GBPUSD/M15`
  - `input_export_tf_value=15`
  - `tester_chart_tf=PERIOD_M15`
  - `tester_export_tf=PERIOD_M15`
  - `tester_bars_generated=96`
  - `csv_row_count=2287`
  - `csv_unique_minute_components=["00"]`
  - `observed_subhour_output=false`
  - `do_not_ingest_current_export=true`
  - `status=terminal_export_completed_but_subhour_not_observed`
- 当前结论：
  - 已确认 terminal export 链路本身可跑通，且 provenance 归档完整。
  - 已确认当前导出的 `GBPUSD/M15` csv 仍只包含整点时间戳，不能当作 `sub-hour` canonical input。
  - 因此当前不进入 `n02_mt5_export_ingest_v1.py`，主线从 `terminal export -> ingest` 收紧为：
    - `build_or_reuse_hcc_reader_then_convert_to_canonical_bars`

## 当前不通过项

- 当前缺口固定为：
  - `GBPUSD/M15 canonical export csv with true sub-hour timestamps`
  - `GBPUSD/M15 ingest output`
  - `GBPUSD/M15 proof output`
