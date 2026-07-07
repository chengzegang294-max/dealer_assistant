# n02_second_fx_symbol_input_gate_gbpusd_h1_runtime_notes v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `GBPUSD/H1` 的 second FX symbol input gate 运行口径。

## 当前边界

- 不写回：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - 主 `EURUSD/M1` 行为链下的 sample/card/summary
- 当前只落：
  - `real_input_samples\n02_real_input_gbpusd_h1_v1.csv`
  - `real_input_samples\n02_ib_proof_of_mapping_output_gbpusd_h1_v1.csv`
  - `n02_second_fx_symbol_input_gate_gbpusd_h1_summary_v1.md`
  - `n02_second_fx_symbol_input_gate_gbpusd_h1_summary_v1.json`
- 当前不推进：
  - `failed breakout`
  - `retest`
  - `reject`
  - `day type`
- 当前也不把：
  - `GBPUSD/H1`
  - 强行写成 `30m OR validation` 成功样本

## 当前怎么用（v1）

- 输入：
  - `TRADING_ANALYSIS_DATA_ROOT\gbpusd_1h.csv`（默认：`.\data\gbpusd_1h.csv`）
- 参考 inventory：
  - `TRADING_ANALYSIS_DATA_ROOT\*_1h.csv`
- 生成脚本：
  - `real_input_samples\n02_mt5_export_ingest_v1.py`
  - `real_input_samples\n02_ib_proof_of_mapping_v1.py`
  - `n02_second_fx_symbol_input_gate_gbpusd_h1_build_v1.py`
- 输出：
  - `real_input_samples\n02_real_input_gbpusd_h1_v1.csv`
  - `real_input_samples\n02_ib_proof_of_mapping_output_gbpusd_h1_v1.csv`
  - `n02_second_fx_symbol_input_gate_gbpusd_h1_summary_v1.md`
  - `n02_second_fx_symbol_input_gate_gbpusd_h1_summary_v1.json`

## 推荐复现命令

- `python real_input_samples\n02_mt5_export_ingest_v1.py --input .\data\gbpusd_1h.csv --symbol GBPUSD --timeframe H1 --source-timezone UTC --dest real_input_samples\n02_real_input_gbpusd_h1_v1.csv`
- `python real_input_samples\n02_ib_proof_of_mapping_v1.py --input real_input_samples\n02_real_input_gbpusd_h1_v1.csv --symbol GBPUSD --timeframe H1 --skip-partial-days --output real_input_samples\n02_ib_proof_of_mapping_output_gbpusd_h1_v1.csv`
- `python real_input_samples\n02_proof_of_mapping_v2.py --input real_input_samples\n02_real_input_gbpusd_h1_v1.csv --output real_input_samples\n02_proof_of_mapping_output_gbpusd_h1_v1.csv`
- `python n02_second_fx_symbol_input_gate_gbpusd_h1_build_v1.py`

## 2026-07-05 fresh-run 结果

- inventory：
  - 已在 `TRADING_ANALYSIS_DATA_ROOT\*_1h.csv` 发现多组 `FX H1` 原始样本。
  - 当前首个第二 FX 样本固定为：`GBPUSD/H1`
- bars：
  - `rows=64897`
  - `first_bar_time_utc=2016-01-03T22:00:00Z`
  - `last_bar_time_utc=2026-06-10T00:00:00Z`
  - `timezone_heuristic=first_bar_utc_like_sunday_reopen`
- IB proof：
  - `ib_proof_of_mapping_rows=5414`
- OR gate：
  - 已观察到：`ValueError: max() iterable argument is empty`
  - 当前 `H1=60m`，而 `n02_or_proof_config_v1.json` 中两组 `opening_range_window_minutes=30`
  - 当前因此判定：`GBPUSD/H1` 不满足现有 `30m OR` 粒度要求

## 当前结论

- 第二个 FX 原始输入已经存在，当前不再是“无样本”状态。
- `GBPUSD/H1` 可完成 ingest 与 IB proof，但当前只收口为 `input gate`，不写成 OR validation 成功。

## provenance 说明

- 当前 `source_timezone=UTC` 采用周日 `22:00Z` 外汇重开型时间轴作为启发式口径。
- 当前 ingest / IB proof fresh-run 仍按旧仓 runtime 路径实跑。
- 本目录下同名 summary 承担新仓镜像回填与主线索引职责。
