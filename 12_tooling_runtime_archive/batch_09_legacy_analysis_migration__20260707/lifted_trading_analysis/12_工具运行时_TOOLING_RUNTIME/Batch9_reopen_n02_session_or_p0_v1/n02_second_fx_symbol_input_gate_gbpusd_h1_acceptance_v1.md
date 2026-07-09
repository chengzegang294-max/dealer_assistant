# N02 GBPUSD H1 第二 FX 品种输入闸口验收 v1

## 目的

- 记录 `REOPEN_B9_N02_SECOND_FX_SYMBOL_INPUT_GATE_GBPUSD_H1_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `TRADING_ANALYSIS_DATA_ROOT\gbpusd_1h.csv`（默认：`.\data\gbpusd_1h.csv`）
- 生成脚本：
  - `real_input_samples\n02_mt5_export_ingest_v1.py`
  - `real_input_samples\n02_ib_proof_of_mapping_v1.py`
  - `n02_second_fx_symbol_input_gate_gbpusd_h1_build_v1.py`
- 观察命令：
  - `real_input_samples\n02_proof_of_mapping_v2.py`
- 输出：
  - `real_input_samples\n02_real_input_gbpusd_h1_v1.csv`
  - `real_input_samples\n02_ib_proof_of_mapping_output_gbpusd_h1_v1.csv`
  - `n02_second_fx_symbol_input_gate_gbpusd_h1_summary_v1.md`
  - `n02_second_fx_symbol_input_gate_gbpusd_h1_summary_v1.json`

## 2026-07-05 fresh-run 验收

- 本轮结果：
  - `fx_h1_symbol_count=19`
  - `bars_rows=64897`
  - `ib_rows=5414`
  - `ib_defined_rows=5412`
  - `or_gate_status=blocked_by_timeframe_granularity`
- 当前结论：
  - 第二个 FX 原始输入已经存在。
  - `GBPUSD/H1` 已能独立跑通 ingest 与 IB proof。
  - 当前 `H1` 粒度不满足现有 `30m OR` 口径，因此这层只收口为 `input gate`。

## 关键统计

- `inventory_second_fx_symbols_excluding_eurusd=["AUDJPY","AUDNZD","AUDUSD","CADJPY","CHFJPY","EURAUD","EURCHF","EURGBP","EURJPY","EURNZD","GBPCHF","GBPJPY","GBPUSD","NZDJPY","NZDUSD","USDCAD","USDCHF","USDJPY"]`
- `bars_first_bar_time_utc=2016-01-03T22:00:00Z`
- `bars_last_bar_time_utc=2026-06-10T00:00:00Z`
- `or_observed_command_failure=ValueError: max() iterable argument is empty`

## 当前不通过项

- 当前缺的不是“第二个 FX 原始样本”，而是满足 `30m OR` 口径的 `second FX sub-hour input`。
