# n02_other_symbol_validation_xauusd_m1_tail_runtime_notes v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `XAUUSD/M1 tail` 的 other symbol validation 运行口径。

## 当前边界

- 不写回：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - 主 `EURUSD/M1` 行为链下的 sample/card/summary
- 当前只落：
  - `real_input_samples\n02_real_input_xauusd_m1_tail_v1.csv`
  - `real_input_samples\n02_proof_of_mapping_output_xauusd_m1_tail_v1.csv`
  - `real_input_samples\n02_ib_proof_of_mapping_output_xauusd_m1_tail_v1.csv`
  - `n02_other_symbol_validation_xauusd_m1_tail_summary_v1.md`
  - `n02_other_symbol_validation_xauusd_m1_tail_summary_v1.json`
- 当前不推进：
  - `failed breakout`
  - `retest`
  - `reject`
  - `day type`

## 当前怎么用（v1）

- 输入：
  - `.\data\mt_exports_drop\xauusd_m1_tail_20000.csv`
- 生成脚本：
  - `real_input_samples\n02_mt5_export_ingest_v1.py`
  - `real_input_samples\n02_proof_of_mapping_v2.py`
  - `real_input_samples\n02_ib_proof_of_mapping_v1.py`
  - `n02_other_symbol_validation_xauusd_m1_tail_build_v1.py`
- 输出：
  - `real_input_samples\n02_real_input_xauusd_m1_tail_v1.csv`
  - `real_input_samples\n02_proof_of_mapping_output_xauusd_m1_tail_v1.csv`
  - `real_input_samples\n02_ib_proof_of_mapping_output_xauusd_m1_tail_v1.csv`
  - `n02_other_symbol_validation_xauusd_m1_tail_summary_v1.md`
  - `n02_other_symbol_validation_xauusd_m1_tail_summary_v1.json`

## 推荐复现命令

- `python real_input_samples\n02_mt5_export_ingest_v1.py --input .\data\mt_exports_drop\xauusd_m1_tail_20000.csv --symbol XAUUSD --timeframe M1 --source-timezone UTC --schema time_only --time-col "Time (UTC)" --dest real_input_samples\n02_real_input_xauusd_m1_tail_v1.csv`
- `python real_input_samples\n02_proof_of_mapping_v2.py --input real_input_samples\n02_real_input_xauusd_m1_tail_v1.csv --output real_input_samples\n02_proof_of_mapping_output_xauusd_m1_tail_v1.csv`
- `python real_input_samples\n02_ib_proof_of_mapping_v1.py --input real_input_samples\n02_real_input_xauusd_m1_tail_v1.csv --symbol XAUUSD --timeframe M1 --skip-partial-days --output real_input_samples\n02_ib_proof_of_mapping_output_xauusd_m1_tail_v1.csv`
- `python n02_other_symbol_validation_xauusd_m1_tail_build_v1.py`

## 2026-07-05 fresh-run 结果

- bars：
  - `rows=20000`
  - `first_bar_time_utc=2026-04-07T03:35:00Z`
  - `last_bar_time_utc=2026-04-27T14:54:00Z`
- OR proof：
  - `rows=37`
  - `rows_or_defined=30`
  - `first_break_up=13`
  - `first_break_down=17`
  - `first_break_none=7`
- IB proof：
  - `ib_proof_of_mapping_rows=30`
- 当前结论：
  - `XAUUSD/M1 tail` 已能独立跑通最小 OR/IB validation。
  - 当前验证层只说明 `other symbol` 可跑性，不写回主 `EURUSD/M1` runtime。

## provenance 说明

- 当前 ingest / proof fresh-run 仍按旧仓 runtime 路径实跑。
- 本目录下同名产物作为镜像回填，用于维持新仓索引与阅读入口一致。
