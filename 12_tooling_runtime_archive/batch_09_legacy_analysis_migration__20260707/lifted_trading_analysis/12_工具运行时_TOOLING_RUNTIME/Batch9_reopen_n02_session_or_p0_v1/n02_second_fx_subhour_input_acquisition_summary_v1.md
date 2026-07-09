# N02 第二 FX 次小时输入采集总览 v1

## Role

- Scan known `data` and `MT4 history` sources for a second FX symbol sub-hour input.
- Keep this layer as acquisition-only evidence, without writing any main runtime fields.

## 2026-07-05 fresh-run

- data_subhour_symbols: `["EURUSD"]`
- data_subhour_timeframes: `["M1", "M5", "M15"]`
- mt4_subhour_symbols: `["EURUSD"]`
- mt4_higher_tf_symbols: `["EURUSD", "GBPUSD", "USDCHF", "USDJPY"]`
- combined_second_fx_subhour_symbols_excluding_eurusd: `[]`
- known_higher_tf_fx_symbols_without_subhour: `["GBPUSD", "USDCHF", "USDJPY"]`
- recommended_target: `GBPUSD/M15`
- acquisition_status: `blocked_by_missing_second_fx_subhour_across_known_sources`

## Current Decision

- Across the currently known `data` and `MT4 history` sources, no second FX sub-hour input was found.
- `EURUSD` still has the only sub-hour raw source; `GBPUSD / USDCHF / USDJPY` currently appear only as higher-timeframe MT4 history files.
- Therefore the next stop remains `second FX sub-hour input acquisition`, now narrowed to `GBPUSD/M15 export or external recovery beyond known sources`.
