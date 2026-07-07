# n02_wider_history_validation_eurusd_m5_from_m1_summary v1

## 作用

- 对主 `EURUSD/M1` canonical bars 聚合出来的 `EURUSD/M5` 更宽历史窗做 OR/IB 口径验证。
- 当前只验证 `wider history` 可跑性，不写回主 `M1` runtime，不升级成行为标签。

## 2026-07-04 fresh-run

- M5 bars：`19840`
- M5 时间范围：`2026-03-06T17:10:00Z` -> `2026-06-11T23:50:00Z`
- 丢弃不完整 5 分钟桶：`89`
- OR proof：`165` 行，已定义`138/165 `
- OR first_break_direction：`{"down": 56, "none": 27, "up": 82}`
- OR first_break_mode：`{"close": 78, "none": 27, "wick": 60}`
- IB proof：`138` 行，已定义`138/138 `

## 当前裁决

- 主 `EURUSD/M1` 样本聚合成 `EURUSD/M5` 后，已能跑通完整历史窗下的 OR/IB proof。
- 当前 `OR defined=138/165`，`IB defined=138/138`，与主 `M1` runtime 的 session 数量级保持一致。
- 当前验证层只说明 `wider EURUSD/M5 history` 可跑性，不把 `M5` 混入主 `M1` 行为链。
