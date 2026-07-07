# n02_second_fx_subhour_historical_recovery_gbpusd_m15_acceptance v1

## 目的

- 记录 `REOPEN_B9_N02_SECOND_FX_SUBHOUR_HISTORICAL_RECOVERY_GBPUSD_M15_P0` 的最小验收结论。

## 本次验收对象

- 历史输入：
  - `12_工具运行时_TOOLING_RUNTIME\VTMarkets-Live 2\GBPUSD-VIP15.hst`
- 生成器：
  - `real_input_samples\n02_mt4_hst_ingest_v1.py`
  - `real_input_samples\n02_proof_of_mapping_v2.py`
  - `real_input_samples\n02_ib_proof_of_mapping_v1.py`
  - `n02_second_fx_subhour_historical_recovery_gbpusd_m15_build_v1.py`
- 输出：
  - `real_input_samples\n02_real_input_gbpusd_m15_v1.csv`
  - `real_input_samples\n02_real_input_gbpusd_m15_report_v1.json`
  - `real_input_samples\n02_proof_of_mapping_output_gbpusd_m15_v1.csv`
  - `real_input_samples\n02_ib_proof_of_mapping_output_gbpusd_m15_v1.csv`
  - `n02_second_fx_subhour_historical_recovery_gbpusd_m15_summary_v1.md`
  - `n02_second_fx_subhour_historical_recovery_gbpusd_m15_summary_v1.json`

## 2026-07-05 fresh-run 验收

- 本轮结果：
  - `bars_record_count=19032`
  - `bars_first_bar_time=2021-06-15T15:30:00Z`
  - `bars_last_bar_time=2022-03-18T23:45:00Z`
  - `bars_unique_minute_components=["00","15","30","45"]`
  - `bars_step_minutes_histogram={"15": 18991, "45": 1, "2895": 37, "2955": 2}`
  - `or_rows=457`
  - `or_defined_rows=396`
  - `ib_rows=457`
  - `ib_defined_rows=396`
  - `status=historical_recovered_second_fx_subhour_ready`
- 当前结论：
  - 已确认 `GBPUSD-VIP15.hst` 可以被直接转成 `GBPUSD/M15` canonical bars。
  - 已确认 recovered `GBPUSD/M15` bars 可以独立跑通 OR / IB proof。
  - 已确认本轮证据属于 `historical_recovered`，不冒充 `TradeMaxGlobal-Demo__60088394` 的 fresh export 修复成功。

## 当前不通过项

- 当前仍未做：
  - `failed breakout` 相关定义
  - `n02_p0_fields_runtime_v2.csv` 主行为链接入
  - 基于这份 recovered `GBPUSD/M15` 的下游关系链扩展
