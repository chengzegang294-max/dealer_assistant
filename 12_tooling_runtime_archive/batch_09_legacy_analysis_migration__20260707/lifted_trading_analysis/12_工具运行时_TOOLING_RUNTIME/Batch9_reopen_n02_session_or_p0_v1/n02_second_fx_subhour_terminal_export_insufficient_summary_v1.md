# N02 第二 FX 次小时终端导出不足总览 v1

## 目的

- 对 `TradeMaxGlobal-Demo__60088394` 的 `GBPUSD/M15 terminal export` 做真实结果收口。
- 明确当前 terminal export 是否已经足够进入 `n02_mt5_export_ingest_v1.py`。

## 2026-07-05 fresh-run 结论

- `status`: `terminal_export_completed_but_subhour_not_observed`
- `environment_label`: `TradeMaxGlobal-Demo__60088394`
- `requested_symbol_timeframe`: `GBPUSD/M15`
- `process_exited`: `true`
- `report_fallback_attempted`: `true`
- `input_export_tf_value`: `15`
- `tester_chart_tf`: `PERIOD_M15`
- `tester_export_tf`: `PERIOD_M15`
- `tester_bars_generated`: `96`
- `csv_row_count`: `2287`
- `csv_latest_bar_time_utc`: `2024-01-05T23:00:00Z`
- `csv_earliest_bar_time_utc`: `2023-01-02T00:00:00Z`
- `csv_step_minutes_histogram`: `{"60": 2094, "1440": 140, "2940": 15, "4320": 35, "4380": 2}`
- `csv_unique_minute_components`: `["00"]`
- `observed_subhour_output`: `false`
- `do_not_ingest_current_export`: `true`

## 当前裁决

- 当前 terminal export 已真实跑通，并已归档 `csv / tester_log / terminal_log / report / runtime_set / runtime_ini`。
- 但导出的 `GBPUSD/M15` csv 仍只出现整点时间戳，未观察到 `:15/:30/:45` 子小时时间点。
- 因此当前不能把该 csv 直接送入 `n02_mt5_export_ingest_v1.py` 作为 `GBPUSD/M15` canonical bars。
- 主线下一步从 `terminal export -> ingest` 收紧为：`build_or_reuse_hcc_reader_then_convert_to_canonical_bars`。

## provenance

- `archive_root`: `D:\Stock\trading_assistant\02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\mt5_bar_export\fix2_gbpusd_m15_short_tmgm_20260705T1737`
- `run_summary_json`: `D:\Stock\trading_assistant\02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\mt5_bar_export\fix2_gbpusd_m15_short_tmgm_20260705T1737\run_summary.json`
- `tester_log`: `D:\Stock\trading_assistant\02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\mt5_bar_export\fix2_gbpusd_m15_short_tmgm_20260705T1737\log\20260705.log`
- `mq5`: `D:\Stock\trading_assistant\12_tooling_runtime_archive\batch_02_mt_indicator_family\MT5BarExportProbe.mq5`
- `run_ps1`: `D:\Stock\trading_assistant\02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\run_mt5_bar_export_once.ps1`
