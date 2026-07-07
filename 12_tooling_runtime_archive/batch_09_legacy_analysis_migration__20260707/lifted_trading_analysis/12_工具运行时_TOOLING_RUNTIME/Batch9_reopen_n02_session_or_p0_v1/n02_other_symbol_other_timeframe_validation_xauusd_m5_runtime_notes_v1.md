# n02_other_symbol_other_timeframe_validation_xauusd_m5_runtime_notes v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `XAUUSD/M5 jobs` 的 other symbol + other timeframe validation 运行口径。

## 当前边界

- 不写回：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - 主 `EURUSD/M1` 行为链下的 sample/card/summary
- 当前只落：
  - `real_input_samples\n02_real_input_xauusd_m5_jobs_v1.csv`
  - `real_input_samples\n02_proof_of_mapping_output_xauusd_m5_jobs_v1.csv`
  - `real_input_samples\n02_ib_proof_of_mapping_output_xauusd_m5_jobs_v1.csv`
  - `n02_other_symbol_other_timeframe_validation_xauusd_m5_summary_v1.md`
  - `n02_other_symbol_other_timeframe_validation_xauusd_m5_summary_v1.json`
- 当前不推进：
  - `failed breakout`
  - `retest`
  - `reject`
  - `day type`

## 当前怎么用（v1）

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

## 推荐复现命令

- `python real_input_samples\n02_mt5_export_ingest_v1.py --input .\data\mt_exports_drop\jobs\xauusd_m5.csv --symbol XAUUSD --timeframe M5 --source-timezone UTC --dest real_input_samples\n02_real_input_xauusd_m5_jobs_v1.csv`
- `python real_input_samples\n02_proof_of_mapping_v2.py --input real_input_samples\n02_real_input_xauusd_m5_jobs_v1.csv --output real_input_samples\n02_proof_of_mapping_output_xauusd_m5_jobs_v1.csv`
- `python real_input_samples\n02_ib_proof_of_mapping_v1.py --input real_input_samples\n02_real_input_xauusd_m5_jobs_v1.csv --symbol XAUUSD --timeframe M5 --skip-partial-days --output real_input_samples\n02_ib_proof_of_mapping_output_xauusd_m5_jobs_v1.csv`
- `python n02_other_symbol_other_timeframe_validation_xauusd_m5_build_v1.py`

## 2026-07-05 fresh-run 结果

- bars：
  - `rows=70880`
  - `first_bar_time_utc=2025-06-12T01:00:00Z`
  - `last_bar_time_utc=2026-06-11T23:55:00Z`
- OR proof：
  - `rows=601`
  - `rows_or_defined=516`
  - `first_break_up=272`
  - `first_break_down=240`
  - `first_break_none=89`
  - `first_break_ambiguous=4`
- IB proof：
  - `ib_proof_of_mapping_rows=516`
- 当前结论：
  - `XAUUSD/M5 jobs` 已能独立跑通最小 OR/IB validation。
  - 当前验证层只说明 `other symbol + other timeframe` 可跑性，不写回主 `EURUSD/M1` runtime。

## provenance 说明

- 当前 `source_timezone=UTC` 沿用 `mt_exports_drop` 同家族导出的既有 N02 口径。
- UTC 复核补充：
  - 已把显式 `UTC` 的 `XAUUSD/M1 tail` 聚合成 `M5`，并与 `XAUUSD/M5 jobs` 做重叠窗口对齐。
  - 对齐结果：`overlap_rows=3758`，`exact_match_rows=0`，当前不能把 `jobs\xauusd_m5.csv` 的 `UTC` 口径升级成独立硬证据。
  - 当前因此保留：`source_timezone=UTC` 仍沿用 `mt_exports_drop` 同家族导出的既有 N02 口径。
- 当前 ingest / proof fresh-run 仍按旧仓 runtime 路径实跑。
- 本目录下同名产物作为镜像回填，用于维持新仓索引与阅读入口一致。
