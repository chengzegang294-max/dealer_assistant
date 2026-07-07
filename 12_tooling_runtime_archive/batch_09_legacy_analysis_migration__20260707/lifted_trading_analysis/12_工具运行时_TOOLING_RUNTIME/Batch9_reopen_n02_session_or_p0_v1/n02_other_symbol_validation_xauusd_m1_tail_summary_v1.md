# n02_other_symbol_validation_xauusd_m1_tail_summary v1

## 作用

- 对 `XAUUSD / M1 / tail sample` 做最小 OR/IB 口径验证。
- 当前只验证 `other symbol` 可跑性，不写回主 `EURUSD/M1` runtime，不升级成行为标签。

## 2026-07-05 fresh-run

- bars 行数：`20000`
- bars 时间范围：`2026-04-07T03:35:00Z` -> `2026-04-27T14:54:00Z`
- OR proof 行数：`37`
- OR defined：`30` / `37`
- OR first_break_direction：`{"down": 17, "none": 7, "up": 13}`
- OR first_break_mode：`{"close": 19, "none": 7, "wick": 11}`
- IB proof 行数：`30`
- IB defined：`30` / `30`

## 当前裁决

- `XAUUSD/M1` tail 样本已能独立跑通 OR/IB proof。
- OR proof 当前 `30/37` 行已定义，`7/37` 行未定义；IB proof 当前 `30/30` 行已定义。
- 当前验证层只说明 `other symbol` 可跑性，不把 `XAUUSD` 混入主 `EURUSD/M1` 行为链。
