# N02 XAUUSD M5 其他品种跨周期验证验收 v1

## 目的

- 记录 `REOPEN_B9_N02_OTHER_SYMBOL_OTHER_TIMEFRAME_VALIDATION_XAUUSD_M5_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `.\data\mt_exports_drop\jobs\xauusd_m5.csv`
- 生成脚本：
  - `real_input_samples\n02_mt5_export_ingest_v1.py`
  - `real_input_samples\n02_proof_of_mapping_v2.py`
  - `real_input_samples\n02_ib_proof_of_mapping_v1.py`
  - `n02_other_symbol_other_timeframe_validation_xauusd_m5_build_v1.py`
- 输出：
  - `real_input_samples\n02_real_input_xauusd_m5_jobs_v1.csv`
  - `real_input_samples\n02_proof_of_mapping_output_xauusd_m5_jobs_v1.csv`
  - `real_input_samples\n02_ib_proof_of_mapping_output_xauusd_m5_jobs_v1.csv`
  - `n02_other_symbol_other_timeframe_validation_xauusd_m5_summary_v1.md`
  - `n02_other_symbol_other_timeframe_validation_xauusd_m5_summary_v1.json`

## 2026-07-05 fresh-run 验收

- 本轮结果：
  - `bars_rows=70880`
  - `or_rows=601`
  - `or_defined_rows=516`
  - `ib_rows=516`
  - `ib_defined_rows=516`
- 当前结论：
  - `XAUUSD/M5 jobs` 已能独立跑通最小 OR/IB validation。
  - 当前验证层只说明 `other symbol + other timeframe` 可跑性，不写回主 `EURUSD/M1` runtime。
  - 当前仍不升级成 `failed breakout / retest / reject / day type`。

## 关键统计

- `or_defined_ratio=516/601`
- `ib_defined_ratio=516/516`
- `or_first_break_direction_counts={"down": 240, "none": 89, "up": 272}`
- `or_first_break_mode_counts={"ambiguous": 4, "close": 280, "none": 85, "wick": 232}`

## 当前不通过项

- 已对显式 `UTC` 的 `XAUUSD/M1 tail` 聚合 `M5` 后做重叠窗口对齐：
  - `overlap_rows=3758`
  - `exact_match_rows=0`
  - 当前仍不能把 `jobs\xauusd_m5.csv` 的 `UTC` 口径升级成独立硬证据。
