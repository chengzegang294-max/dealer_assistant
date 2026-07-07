# n02_wider_history_validation_eurusd_m5_from_m1_runtime_notes v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录主 `EURUSD/M1` canonical bars 聚合到 `EURUSD/M5` 之后的 wider history validation 运行口径。

## 当前边界

- 不写回：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - 主 `M1` 行为链下的 sample/card/summary
- 当前只落：
  - `n02_real_input_eurusd_m5_from_m1_main_v1.csv`
  - `n02_real_input_eurusd_m5_from_m1_main_report_v1.json`
  - `n02_proof_of_mapping_output_eurusd_m5_from_m1_main_v1.csv`
  - `n02_ib_proof_of_mapping_output_eurusd_m5_from_m1_main_v1.csv`
  - `n02_wider_history_validation_eurusd_m5_from_m1_summary_v1.md`
  - `n02_wider_history_validation_eurusd_m5_from_m1_summary_v1.json`
- 当前不推进：
  - `failed breakout`
  - `retest`
  - `reject`
  - `day type`

## 当前怎么用（v1）

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

## 推荐复现命令

- `python real_input_samples\n02_aggregate_bars_to_m5_v1.py`
- `python real_input_samples\n02_proof_of_mapping_v2.py --input real_input_samples\n02_real_input_eurusd_m5_from_m1_main_v1.csv --output real_input_samples\n02_proof_of_mapping_output_eurusd_m5_from_m1_main_v1.csv`
- `python real_input_samples\n02_ib_proof_of_mapping_v1.py --session-input london=real_input_samples\n02_real_input_eurusd_m5_from_m1_main_v1.csv --session-input new_york=real_input_samples\n02_real_input_eurusd_m5_from_m1_main_v1.csv --symbol EURUSD --timeframe M5 --skip-partial-days --output real_input_samples\n02_ib_proof_of_mapping_output_eurusd_m5_from_m1_main_v1.csv`
- `python n02_wider_history_validation_eurusd_m5_from_m1_build_v1.py`

## 2026-07-04 fresh-run 结果

- M5 聚合：
  - `input_rows_filtered=99500`
  - `bucket_groups_total=19929`
  - `bucket_groups_dropped_partial=89`
  - `output_rows=19840`
- OR proof：
  - `rows=165`
  - `rows_or_defined=138`
  - `first_break_up=82`
  - `first_break_down=56`
  - `first_break_none=27`
- IB proof：
  - `ib_proof_of_mapping_rows=138`
- 当前结论：
  - 主 `EURUSD/M1` 样本聚合成 `EURUSD/M5` 后，已能跑通更宽历史窗下的 OR/IB proof。
  - 当前验证层只说明 `wider EURUSD/M5 history` 可跑性，不写回主 `M1` runtime。
