# N02 EURUSD M5 从 M1 聚合的宽历史验证验收 v1

## 目的

- 记录 `REOPEN_B9_N02_WIDER_HISTORY_VALIDATION_EURUSD_M5_FROM_M1_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `n02_first_real_input_bars_v1.csv`
- 生成脚本：
  - `real_input_samples\n02_aggregate_bars_to_m5_v1.py`
  - `real_input_samples\n02_proof_of_mapping_v2.py`
  - `real_input_samples\n02_ib_proof_of_mapping_v1.py`
  - `n02_wider_history_validation_eurusd_m5_from_m1_build_v1.py`
- 输出：
  - `n02_real_input_eurusd_m5_from_m1_main_v1.csv`
  - `n02_real_input_eurusd_m5_from_m1_main_report_v1.json`
  - `n02_proof_of_mapping_output_eurusd_m5_from_m1_main_v1.csv`
  - `n02_ib_proof_of_mapping_output_eurusd_m5_from_m1_main_v1.csv`
  - `n02_wider_history_validation_eurusd_m5_from_m1_summary_v1.md`
  - `n02_wider_history_validation_eurusd_m5_from_m1_summary_v1.json`

## 2026-07-04 fresh-run 验收

- 本轮结果：
  - `m5_bars_rows=19840`
  - `m5_bucket_groups_dropped_partial=89`
  - `or_rows=165`
  - `or_defined_rows=138`
  - `ib_rows=138`
  - `ib_defined_rows=138`
- 当前结论：
  - 主 `EURUSD/M1` 样本聚合成 `EURUSD/M5` 后，已能跑通更宽历史窗下的 OR/IB proof。
  - 当前验证层只说明 `wider EURUSD/M5 history` 可跑性，不写回主 `M1` runtime。
  - 当前仍不升级成 `failed breakout / retest / reject / day type`。

## 关键统计

- `or_defined_ratio=138/165`
- `ib_defined_ratio=138/138`
- `or_first_break_direction_counts={"down": 56, "none": 27, "up": 82}`
- `or_first_break_mode_counts={"close": 78, "none": 27, "wick": 60}`

## 当前不通过项

- 当前还没有第二个外汇 symbol 的同口径输入样本。
