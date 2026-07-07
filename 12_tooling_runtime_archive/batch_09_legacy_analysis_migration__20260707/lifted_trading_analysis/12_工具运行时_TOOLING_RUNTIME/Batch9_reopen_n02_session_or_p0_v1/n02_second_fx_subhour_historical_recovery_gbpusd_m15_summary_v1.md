# n02_second_fx_subhour_historical_recovery_gbpusd_m15_summary v1

## 作用

- 对 `GBPUSD/M15` 做 `historical_recovered` 级恢复验证。
- 当前专门记录：`terminal export` 已被证明不足，但旧仓 `VTMarkets-Live 2\GBPUSD-VIP15.hst` 已能直接转成 canonical bars 并跑通 OR / IB proof。

## 2026-07-05 fresh-run

- source_hst: `D:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\VTMarkets-Live 2\GBPUSD-VIP15.hst`
- bars_record_count: `19032`
- bars_time_range: `2021-06-15T15:30:00Z` -> `2022-03-18T23:45:00Z`
- bars_unique_minute_components: `["00", "15", "30", "45"]`
- bars_step_minutes_histogram: `{"15": 18991, "45": 1, "2895": 37, "2955": 2}`
- OR proof rows: `457`
- OR defined: `396` / `457`
- OR first_break_direction: `{"down": 199, "none": 84, "up": 174}`
- OR first_break_mode: `{"ambiguous": 22, "close": 203, "none": 62, "wick": 170}`
- IB proof rows: `457`
- IB defined: `396` / `457`
- gate_status: `historical_recovered_second_fx_subhour_ready`

## 当前裁决

- 当前 `GBPUSD/M15` 已不再卡在 `hcc reader` fallback，因为仓内现成 `HST reader` 已足够把 `GBPUSD-VIP15.hst` 转成 canonical bars。
- 这一层证据强度是 `historical_recovered`，不是 `TradeMaxGlobal-Demo__60088394` terminal fresh export。
- 当前 recovered `GBPUSD/M15` bars 已能独立跑通 OR / IB proof，可作为 `Batch9 N02` 第二个 FX sub-hour 输入继续向下游推进。
