# n02_other_symbol_other_timeframe_validation_xauusd_m5_summary v1

## 作用

- 对 `XAUUSD / M5 / jobs sample` 做最小 OR/IB 口径验证。
- 当前只验证 `other symbol + other timeframe` 可跑性，不写回主 `EURUSD/M1` runtime，不升级成行为标签。

## 2026-07-05 fresh-run

- bars 行数：`70880`
- bars 时间范围：`2025-06-12T01:00:00Z` -> `2026-06-11T23:55:00Z`
- OR proof 行数：`601`
- OR defined：`516` / `601`
- OR first_break_direction：`{"down": 240, "none": 89, "up": 272}`
- OR first_break_mode：`{"ambiguous": 4, "close": 280, "none": 85, "wick": 232}`
- IB proof 行数：`516`
- IB defined：`516` / `516`

## 当前裁决

- `XAUUSD/M5` jobs 样本已能独立跑通 OR/IB proof。
- OR proof 当前 `516/601` 行已定义，`89/601` 行未定义；IB proof 当前 `516/516` 行已定义。
- 当前验证层只说明 `other symbol + other timeframe` 可跑性，不把 `XAUUSD/M5` 混入主 `EURUSD/M1` 行为链。
