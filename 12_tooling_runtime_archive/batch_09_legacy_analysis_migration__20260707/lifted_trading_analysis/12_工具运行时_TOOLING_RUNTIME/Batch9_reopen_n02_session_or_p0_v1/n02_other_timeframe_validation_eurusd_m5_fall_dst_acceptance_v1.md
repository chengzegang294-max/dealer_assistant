# n02_other_timeframe_validation_eurusd_m5_fall_dst_acceptance v1

## 目的

- 记录 `REOPEN_B9_N02_OTHER_TIMEFRAME_VALIDATION_EURUSD_M5_FALL_DST_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `n02_dst_london_fall_20251023_20251028_bars.csv`
  - `n02_dst_newyork_fall_20251031_20251104_bars.csv`
- 生成脚本：
  - `real_input_samples\n02_expand_real_input_with_dst_v1.py`
  - `real_input_samples\n02_proof_of_mapping_v2.py`
  - `real_input_samples\n02_ib_proof_of_mapping_v1.py`
  - `n02_other_timeframe_validation_eurusd_m5_fall_dst_build_v1.py`
- 输出：
  - `n02_real_input_eurusd_m5_fall_dst_v1.csv`
  - `n02_real_input_eurusd_m5_fall_dst_report_v1.json`
  - `n02_proof_of_mapping_output_eurusd_m5_fall_dst_v1.csv`
  - `n02_ib_proof_of_mapping_output_eurusd_m5_fall_dst_v1.csv`
  - `n02_other_timeframe_validation_eurusd_m5_fall_dst_summary_v1.md`
  - `n02_other_timeframe_validation_eurusd_m5_fall_dst_summary_v1.json`

## 2026-07-04 fresh-run 验收

- 本轮结果：
  - `bars_rows=1440`
  - `or_rows=15`
  - `or_defined_rows=10`
  - `ib_rows=10`
  - `ib_defined_rows=10`
- 当前结论：
  - `EURUSD/M5` 秋季 DST 样本已能独立跑通 OR/IB proof。
  - 当前验证层只说明 `other timeframe` 可跑性，不写回主 `M1` runtime。
  - 当前仍不升级成 `failed breakout / retest / reject / day type`。

## 关键统计

- `or_defined_ratio=10/15`
- `ib_defined_ratio=10/10`
- `or_first_break_direction_counts={"down": 3, "none": 5, "up": 7}`
- `or_first_break_mode_counts={"close": 7, "none": 5, "wick": 3}`

## 当前不通过项

- 当前还没有其它 symbol 的同口径输入样本。
