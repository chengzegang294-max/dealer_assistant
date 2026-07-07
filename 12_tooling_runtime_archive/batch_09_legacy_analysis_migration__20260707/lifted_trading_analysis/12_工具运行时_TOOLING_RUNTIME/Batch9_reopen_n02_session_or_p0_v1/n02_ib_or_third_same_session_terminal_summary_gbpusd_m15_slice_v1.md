# n02_ib_or_third_same_session_terminal_summary v1

## 作用

- 把 `third same-session` 两支 branch card 汇总成 terminal summary。
- 当前只收口 `beyond persistence` 与 `not_beyond stability` 到第三个同类 `session` 的 terminal state，不升级成 `failed breakout / retest / reject / day type`。

## 2026-07-04 fresh-run

- `total_rows`：`11`
- `resolved_rows`：`8`
- `missing_rows`：`3`
- `beyond_rows`：`2`
- `beyond_status_counts`：`{"missing_third_next_session_first_30m_data": 1, "third_next_session_first_30m_all_closes_beyond_prior_ib": 1}`
- `not_beyond_rows`：`9`
- `not_beyond_status_counts`：`{"missing_third_next_session_first_30m_data": 2, "third_next_session_first_30m_all_closes_inside_prior_ib": 6, "third_next_session_first_30m_not_all_closes_inside_prior_ib": 1}`

## 当前裁决

- `beyond third same-session persistence` 当前 `1/2` 行保持外侧，`0/2` 行未保持外侧，`1/2` 行缺第三同类 `session` 数据。
- `not_beyond third same-session stability` 当前 `6/9` 行保持内侧稳定，`1/9` 行失稳，`2/9` 行缺第三同类 `session` 数据。
- 这层 terminal summary 当前只给出链路收口：`beyond` 与 `not_beyond` 两支都停在第三同类 `session` terminal state，不升级为更高层标签。
- 当前仍不把任何一支改写成 `failed breakout`。
