# N02 IB OR 第三同会话终端总览 v1

## 作用

- 把 `third same-session` 两支 branch card 汇总成 terminal summary。
- 当前只收口 `beyond persistence` 与 `not_beyond stability` 到第三个同类 `session` 的 terminal state，不升级成 `failed breakout / retest / reject / day type`。

## 2026-07-04 fresh-run

- `total_rows`：`3`
- `resolved_rows`：`2`
- `missing_rows`：`1`
- `beyond_rows`：`2`
- `beyond_status_counts`：`{"third_next_session_first_30m_all_closes_beyond_prior_ib": 2}`
- `not_beyond_rows`：`1`
- `not_beyond_status_counts`：`{"missing_third_next_session_first_30m_data": 1}`

## 当前裁决

- `beyond third same-session persistence` 当前 `2/2` 行保持外侧，没有出现第三同类 `session` 首 30 分钟失守样本。
- `not_beyond third same-session stability` 当前 `1/1` 行缺第三同类 `session` 数据，因此这支只保留为 `missing`，不升级成失稳或失败突破。
- 这层 terminal summary 当前只给出链路收口：`beyond` 支持续外侧、`not_beyond` 支当前数据不足。
- 当前仍不把任何一支改写成 `failed breakout`。
