# n02_other_timeframe_validation_eurusd_m5_fall_dst_summary v1

## 作用

- 对 `EURUSD / M5 / fall DST sample` 做最小 OR/IB 口径验证。
- 当前只验证 `other timeframe` 可跑性，不写回主 `M1` runtime，不升级成行为标签。

## 2026-07-04 fresh-run

- bars 行数：`1440`
- bars 时间范围：`2025-10-23T00:00:00Z` -> `2025-11-03T23:55:00Z`
- OR proof 行数：`15`
- OR defined：`10` / `15`
- OR first_break_direction：`{"down": 4, "none": 5, "up": 6}`
- OR first_break_mode：`{"close": 7, "none": 5, "wick": 3}`
- IB proof 行数：`10`
- IB defined：`10` / `10`

## 当前裁决

- `EURUSD/M5` 秋季 DST 样本已能独立跑通 OR/IB proof。
- OR proof 当前 `10/15` 行已定义，`5/15` 行未定义；IB proof 当前 `10/10` 行已定义。
- 当前验证层只说明 `other timeframe` 可跑性，不把 `M5` 混入主 `M1` 行为链。
