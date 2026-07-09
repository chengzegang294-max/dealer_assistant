# N02 EURUSD M5 秋季 DST 跨周期验证运行说明 v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `EURUSD / M5 / fall DST` 的 other timeframe validation 运行口径。

## 当前边界

- 不写回：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - 主 `EURUSD/M1` 行为链下的任何 sample/card/summary
- 当前只落：
  - `n02_real_input_eurusd_m5_fall_dst_v1.csv`
  - `n02_real_input_eurusd_m5_fall_dst_report_v1.json`
  - `n02_proof_of_mapping_output_eurusd_m5_fall_dst_v1.csv`
  - `n02_ib_proof_of_mapping_output_eurusd_m5_fall_dst_v1.csv`
  - `n02_other_timeframe_validation_eurusd_m5_fall_dst_summary_v1.md`
  - `n02_other_timeframe_validation_eurusd_m5_fall_dst_summary_v1.json`
- 当前不推进：
  - `failed breakout`
  - `retest`
  - `reject`
  - `day type`

## 当前怎么用（v1）

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

## 推荐复现命令

- `python real_input_samples\n02_expand_real_input_with_dst_v1.py --input real_input_samples\n02_dst_london_fall_20251023_20251028_bars.csv --input real_input_samples\n02_dst_newyork_fall_20251031_20251104_bars.csv --output real_input_samples\n02_real_input_eurusd_m5_fall_dst_v1.csv --report-json real_input_samples\n02_real_input_eurusd_m5_fall_dst_report_v1.json`
- `python real_input_samples\n02_proof_of_mapping_v2.py --input real_input_samples\n02_real_input_eurusd_m5_fall_dst_v1.csv --output real_input_samples\n02_proof_of_mapping_output_eurusd_m5_fall_dst_v1.csv`
- `python real_input_samples\n02_ib_proof_of_mapping_v1.py --session-input london=real_input_samples\n02_real_input_eurusd_m5_fall_dst_v1.csv --session-input new_york=real_input_samples\n02_real_input_eurusd_m5_fall_dst_v1.csv --symbol EURUSD --timeframe M5 --skip-partial-days --output real_input_samples\n02_ib_proof_of_mapping_output_eurusd_m5_fall_dst_v1.csv`
- `python n02_other_timeframe_validation_eurusd_m5_fall_dst_build_v1.py`

## 2026-07-04 fresh-run 结果

- bars 合并：
  - `output_rows=1440`
  - `output_first_bar_time=2025-10-23T00:00:00Z`
  - `output_last_bar_time=2025-11-03T23:55:00Z`
- OR proof：
  - `rows=15`
  - `rows_or_defined=10`
  - `first_break_up=6`
  - `first_break_down=4`
  - `first_break_none=5`
- IB proof：
  - `ib_proof_of_mapping_rows=10`
- 当前结论：
  - `EURUSD/M5` 秋季 DST 样本已能独立跑通 OR/IB proof。
  - 当前验证层只说明 `other timeframe` 可跑性，不写回主 `M1` runtime。
