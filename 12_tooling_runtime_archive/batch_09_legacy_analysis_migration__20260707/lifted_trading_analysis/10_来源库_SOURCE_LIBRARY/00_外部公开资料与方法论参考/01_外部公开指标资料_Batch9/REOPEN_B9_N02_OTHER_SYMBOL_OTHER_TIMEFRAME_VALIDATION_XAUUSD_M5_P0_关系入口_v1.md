# REOPEN_B9_N02 OTHER_SYMBOL_OTHER_TIMEFRAME_VALIDATION_XAUUSD_M5_P0 关系入口 v1

## 作用

- 对 `XAUUSD/M5 jobs` 做最小 OR/IB 口径验证。
- 当前只验证 `other symbol + other timeframe` 可跑性，不写回主 `EURUSD/M1` runtime，不升级成 `failed breakout / retest / reject / day type`。

## 当前边界（写死）

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `EURUSD/M1` 主行为链下的 sample/card/summary
- 当前只新增：
  - `XAUUSD/M5 jobs` 的 canonical bars / OR proof / IB proof / validation summary

## 当前真值组成（v1）

- `entry_md`：`REOPEN_B9_N02_OTHER_SYMBOL_OTHER_TIMEFRAME_VALIDATION_XAUUSD_M5_P0_关系入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_other_symbol_other_timeframe_validation_xauusd_m5_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_other_symbol_other_timeframe_validation_xauusd_m5_acceptance_v1.md`
- `ingest_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_mt5_export_ingest_v1.py`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_other_symbol_other_timeframe_validation_xauusd_m5_build_v1.py`
- `bars_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_real_input_xauusd_m5_jobs_v1.csv`
- `or_proof_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_output_xauusd_m5_jobs_v1.csv`
- `ib_proof_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_ib_proof_of_mapping_output_xauusd_m5_jobs_v1.csv`
- `summary_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_other_symbol_other_timeframe_validation_xauusd_m5_summary_v1.md`
- `summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_other_symbol_other_timeframe_validation_xauusd_m5_summary_v1.json`

## 最小验收（关系开题级）

- validation summary 必须显式记录：
  - `bars_rows`
  - `or_rows`
  - `or_defined_rows`
  - `ib_rows`
  - `ib_defined_rows`
- 所有输出都必须显式保留：
  - `writes_main_m1_runtime=false`
  - `is_validation_only=true`

## 2026-07-05 fresh-run

- 运行入口：
  - `python real_input_samples\n02_mt5_export_ingest_v1.py --input 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\jobs\xauusd_m5.csv --symbol XAUUSD --timeframe M5 --source-timezone UTC --dest real_input_samples\n02_real_input_xauusd_m5_jobs_v1.csv`
  - `python real_input_samples\n02_proof_of_mapping_v2.py --input real_input_samples\n02_real_input_xauusd_m5_jobs_v1.csv --output real_input_samples\n02_proof_of_mapping_output_xauusd_m5_jobs_v1.csv`
  - `python real_input_samples\n02_ib_proof_of_mapping_v1.py --input real_input_samples\n02_real_input_xauusd_m5_jobs_v1.csv --symbol XAUUSD --timeframe M5 --skip-partial-days --output real_input_samples\n02_ib_proof_of_mapping_output_xauusd_m5_jobs_v1.csv`
  - `python n02_other_symbol_other_timeframe_validation_xauusd_m5_build_v1.py`
- 关键统计：
  - `bars_rows=70880`
  - `or_rows=601`
  - `or_defined_rows=516`
  - `ib_rows=516`
  - `ib_defined_rows=516`
- 当前裁决：
  - `XAUUSD/M5 jobs` 已能独立跑通最小 OR/IB validation。
  - 当前验证层只说明 `other symbol + other timeframe` 可跑性，不把 `XAUUSD/M5` 混入主 `EURUSD/M1` 行为链。

## provenance 说明

- 当前 `source_timezone=UTC` 沿用 `mt_exports_drop` 同家族导出的既有 N02 口径。
- 当前 ingest / proof fresh-run 仍按旧仓 runtime 路径实跑。
- 本目录及同名产物承担新仓镜像回填与主线索引职责。

## 下一步最顺动作

- 若继续沿同一条线推进，优先补：
  - 第二个外汇 symbol 的同口径输入样本
