# n02_second_fx_subhour_terminal_export_insufficient_runtime_notes v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是把 `TradeMaxGlobal-Demo__60088394: terminal export -> n02_mt5_export_ingest_v1` 这一步的真实结果收口成可追溯停点。

## 当前边界

- 当前不写入：
  - `real_input_samples\n02_real_input_gbpusd_m15_v1.csv`
  - 任意 `GBPUSD/M15` ingest / OR proof / IB proof 输出
  - 任意 `failed breakout` 相关定义
- 当前只落：
  - `n02_second_fx_subhour_terminal_export_insufficient_summary_v1.md`
  - `n02_second_fx_subhour_terminal_export_insufficient_summary_v1.json`
- 当前不伪装：
  - `GBPUSD/M15` canonical bars 已生成
  - 当前 terminal export csv 可以直接进入 `n02_mt5_export_ingest_v1.py`

## 当前怎么跑（v1）

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

## 推荐复现命令

- `python n02_second_fx_subhour_terminal_export_insufficient_build_v1.py`

## 2026-07-05 fresh-run 结果

- terminal export 已真实跑通：
  - `process_exited=true`
  - `report_fallback_attempted=true`
  - `runtime_set_write_mode=written`
  - `InpExportTf=15`
  - `tester_chart_tf=PERIOD_M15`
  - `tester_export_tf=PERIOD_M15`
- 但 export 结果仍不足以进 ingest：
  - `tester_bars_generated=96`
  - `csv_row_count=2287`
  - `csv_unique_minute_components=["00"]`
  - `csv_step_minutes_histogram={"60": 2094, "1440": 140, "2940": 15, "4320": 35, "4380": 2}`
  - `observed_subhour_output=false`
  - `do_not_ingest_current_export=true`

## 当前结论

- 当前 `TradeMaxGlobal-Demo__60088394` 的 terminal export 已证明：
  - 路径可跑
  - 归档可收口
  - 但对目标 `GBPUSD/M15` 来说，导出结果仍只出现整点时间戳
- 因此本轮不继续伪造 `GBPUSD/M15` ingest / proof 成功。
- 主线下一步固定为：
  - `build_or_reuse_hcc_reader_then_convert_to_canonical_bars`

## provenance 说明

- 本停点基于真实 `MT5 tester report / terminal log / tester log / runtime_set / export csv` 收口。
- 当前 summary 只声明 `terminal export completed but subhour not observed`，不声明 canonical export 完成。
