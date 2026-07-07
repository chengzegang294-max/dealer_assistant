# REOPEN_B9_N02 WIDER_HISTORY_VALIDATION_EURUSD_M5_FROM_M1_P0 关系入口 v1

## 作用

- 对主 `EURUSD/M1` canonical bars 聚合出来的 `EURUSD/M5` 更宽历史窗做 OR/IB 口径验证。
- 当前只验证 `wider history` 可跑性，不写回主 `M1` runtime，不升级成 `failed breakout / retest / reject / day type`。

## 当前边界（写死）

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `M1` 主行为链下的 sample/card/summary
- 当前只新增：
  - `EURUSD/M5 from main M1` 聚合样本 / proof / summary

## 当前真值组成（v1）

- `entry_md`：`REOPEN_B9_N02_WIDER_HISTORY_VALIDATION_EURUSD_M5_FROM_M1_P0_关系入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_wider_history_validation_eurusd_m5_from_m1_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_wider_history_validation_eurusd_m5_from_m1_acceptance_v1.md`
- `aggregate_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_aggregate_bars_to_m5_v1.py`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_wider_history_validation_eurusd_m5_from_m1_build_v1.py`
- `bars_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_real_input_eurusd_m5_from_m1_main_v1.csv`
- `bars_report_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_real_input_eurusd_m5_from_m1_main_report_v1.json`
- `or_proof_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_output_eurusd_m5_from_m1_main_v1.csv`
- `ib_proof_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_ib_proof_of_mapping_output_eurusd_m5_from_m1_main_v1.csv`
- `summary_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_wider_history_validation_eurusd_m5_from_m1_summary_v1.md`
- `summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_wider_history_validation_eurusd_m5_from_m1_summary_v1.json`

## 最小验收（关系开题级）

- validation summary 必须显式记录：
  - `m5_bars_rows`
  - `m5_bucket_groups_dropped_partial`
  - `or_rows`
  - `or_defined_rows`
  - `ib_rows`
  - `ib_defined_rows`
- 所有输出都必须显式保留：
  - `writes_main_m1_runtime=false`
  - `is_validation_only=true`

## 2026-07-04 fresh-run

- 运行入口：
  - `python n02_aggregate_bars_to_m5_v1.py`
  - `python n02_proof_of_mapping_v2.py --input n02_real_input_eurusd_m5_from_m1_main_v1.csv --output n02_proof_of_mapping_output_eurusd_m5_from_m1_main_v1.csv`
  - `python n02_ib_proof_of_mapping_v1.py --session-input london=n02_real_input_eurusd_m5_from_m1_main_v1.csv --session-input new_york=n02_real_input_eurusd_m5_from_m1_main_v1.csv --symbol EURUSD --timeframe M5 --skip-partial-days --output n02_ib_proof_of_mapping_output_eurusd_m5_from_m1_main_v1.csv`
  - `python n02_wider_history_validation_eurusd_m5_from_m1_build_v1.py`
- 关键统计：
  - `m5_bars_rows=19840`
  - `m5_bucket_groups_dropped_partial=89`
  - `or_rows=165`
  - `or_defined_rows=138`
  - `ib_rows=138`
  - `ib_defined_rows=138`
- 当前裁决：
  - 主 `EURUSD/M1` 样本聚合成 `EURUSD/M5` 后，已能跑通更宽历史窗下的 OR/IB proof。
  - 当前验证层只说明 `wider EURUSD/M5 history` 可跑性，不把 `M5` 混入主 `M1` 行为链。

## 下一步最顺动作

- 若继续沿同一条线推进，优先补：
  - 其它 symbol 的同口径输入样本
