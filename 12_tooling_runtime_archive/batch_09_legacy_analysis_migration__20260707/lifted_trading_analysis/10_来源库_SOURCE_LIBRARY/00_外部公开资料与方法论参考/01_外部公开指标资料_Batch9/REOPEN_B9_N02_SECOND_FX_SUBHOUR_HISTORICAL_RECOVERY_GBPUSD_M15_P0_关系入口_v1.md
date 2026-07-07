# REOPEN_B9_N02_SECOND_FX_SUBHOUR_HISTORICAL_RECOVERY_GBPUSD_M15_P0 关系入口 v1

## 作用

- 对 `GBPUSD/M15 historical recovered` 做关系入口级收口。
- 当前专门记录：`terminal export insufficient` 之后，旧仓 `VTMarkets-Live 2\GBPUSD-VIP15.hst` 已能提供第二个 FX sub-hour canonical bars 与 OR / IB proof。

## 当前边界（写死）

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - 任意 `failed breakout` 相关定义
- 当前不把：
  - `historical_recovered` 结果
  冒充成 `TradeMaxGlobal-Demo__60088394` terminal fresh export 修复成功

## 当前真值组成（v1）

- `entry_md`：`REOPEN_B9_N02_SECOND_FX_SUBHOUR_HISTORICAL_RECOVERY_GBPUSD_M15_P0_关系入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_historical_recovery_gbpusd_m15_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_historical_recovery_gbpusd_m15_acceptance_v1.md`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_historical_recovery_gbpusd_m15_build_v1.py`
- `ingest_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_mt4_hst_ingest_v1.py`
- `summary_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_historical_recovery_gbpusd_m15_summary_v1.md`
- `summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_historical_recovery_gbpusd_m15_summary_v1.json`

## 最小验收（关系开题级）

- historical recovered summary 必须显式记录：
  - `source_hst`
  - `bars_record_count`
  - `bars_unique_minute_components`
  - `bars_step_minutes_histogram`
  - `or_rows`
  - `or_defined_rows`
  - `ib_rows`
  - `ib_defined_rows`
  - `gate_status`
- 所有输出都必须显式保留：
  - `writes_main_m1_runtime=false`
  - `historical_recovered=true`
  - `declares_terminal_fresh_export=false`

## 2026-07-05 fresh-run

- 运行入口：
  - `python real_input_samples\n02_mt4_hst_ingest_v1.py --symbol GBPUSD --timeframe M15`
  - `python n02_second_fx_subhour_historical_recovery_gbpusd_m15_build_v1.py`
- 关键统计：
  - `source_hst=VTMarkets-Live 2\GBPUSD-VIP15.hst`
  - `bars_record_count=19032`
  - `bars_unique_minute_components=["00","15","30","45"]`
  - `bars_step_minutes_histogram={"15": 18991, "45": 1, "2895": 37, "2955": 2}`
  - `or_rows=457`
  - `or_defined_rows=396`
  - `ib_rows=457`
  - `ib_defined_rows=396`
  - `gate_status=historical_recovered_second_fx_subhour_ready`
- 当前裁决：
  - 当前 `GBPUSD/M15` 已成功由旧仓 `HST` 历史资产恢复成 canonical bars，并跑通 OR / IB proof。
  - 主线下一步固定为：
    - `recovered_gbpusd_m15_downstream_without_failed_breakout`

## provenance 说明

- 当前关系入口以 `HST historical source / ingest report / canonical bars / OR proof / IB proof / validation summary` 共同收口。
- 本目录及同名产物承担新仓镜像回填与主线索引职责。
