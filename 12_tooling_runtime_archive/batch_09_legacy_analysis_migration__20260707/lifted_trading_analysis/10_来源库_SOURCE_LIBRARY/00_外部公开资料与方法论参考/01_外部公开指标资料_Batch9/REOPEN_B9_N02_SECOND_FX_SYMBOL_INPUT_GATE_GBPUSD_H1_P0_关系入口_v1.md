# REOPEN_B9_N02 SECOND_FX_SYMBOL_INPUT_GATE_GBPUSD_H1_P0 关系入口 v1

## 作用

- 对 `GBPUSD/H1` 做 `second FX symbol input gate` 级验证。
- 当前只确认第二个 FX 原始输入是否存在、是否能 ingest、以及是否满足现有 `30m OR` 粒度要求。

## 当前边界（写死）

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `EURUSD/M1` 主行为链下的 sample/card/summary
- 当前只新增：
  - `GBPUSD/H1` 的 ingest / IB proof / input gate summary
- 当前不把：
  - `GBPUSD/H1`
  - 直接改写成 OR validation 成功样本

## 当前真值组成（v1）

- `entry_md`：`REOPEN_B9_N02_SECOND_FX_SYMBOL_INPUT_GATE_GBPUSD_H1_P0_关系入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_symbol_input_gate_gbpusd_h1_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_symbol_input_gate_gbpusd_h1_acceptance_v1.md`
- `ingest_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_mt5_export_ingest_v1.py`
- `ib_proof_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_ib_proof_of_mapping_v1.py`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_symbol_input_gate_gbpusd_h1_build_v1.py`
- `bars_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_real_input_gbpusd_h1_v1.csv`
- `ib_proof_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_ib_proof_of_mapping_output_gbpusd_h1_v1.csv`
- `summary_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_symbol_input_gate_gbpusd_h1_summary_v1.md`
- `summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_symbol_input_gate_gbpusd_h1_summary_v1.json`

## 最小验收（关系开题级）

- input gate summary 必须显式记录：
  - `fx_h1_symbol_count`
  - `bars_rows`
  - `ib_rows`
  - `ib_defined_rows`
  - `or_gate_status`
- 所有输出都必须显式保留：
  - `writes_main_m1_runtime=false`
  - `is_input_gate_only=true`

## 2026-07-05 fresh-run

- 运行入口：
  - `python real_input_samples\n02_mt5_export_ingest_v1.py --input D:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\gbpusd_1h.csv --symbol GBPUSD --timeframe H1 --source-timezone UTC --dest real_input_samples\n02_real_input_gbpusd_h1_v1.csv`
  - `python real_input_samples\n02_ib_proof_of_mapping_v1.py --input real_input_samples\n02_real_input_gbpusd_h1_v1.csv --symbol GBPUSD --timeframe H1 --skip-partial-days --output real_input_samples\n02_ib_proof_of_mapping_output_gbpusd_h1_v1.csv`
  - `python real_input_samples\n02_proof_of_mapping_v2.py --input real_input_samples\n02_real_input_gbpusd_h1_v1.csv --output real_input_samples\n02_proof_of_mapping_output_gbpusd_h1_v1.csv`
  - `python n02_second_fx_symbol_input_gate_gbpusd_h1_build_v1.py`
- 当前裁决：
  - 第二个 FX 原始输入已经存在，当前首个落地样本固定为 `GBPUSD/H1`。
  - `GBPUSD/H1` 的 ingest 与 IB proof 可跑，但当前 `H1` 粒度不满足现有 `30m OR` 口径。
  - 当前这层只收口为 `input gate`，下一步切到 `second FX sub-hour input validation`。

## provenance 说明

- 当前 `source_timezone=UTC` 采用周日 `22:00Z` 外汇重开型时间轴作为启发式口径。
- 当前 ingest / IB proof fresh-run 仍按旧仓 runtime 路径实跑。
- 本目录及同名产物承担新仓镜像回填与主线索引职责。

## 下一步最顺动作

- 若继续沿同一条线推进，优先补：
  - 第二个 FX 的 `sub-hour` 原始输入样本
