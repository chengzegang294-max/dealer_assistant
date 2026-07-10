# N02 IB OR 未超出稳定性说明卡 v1

## 作用

- 把 `not_beyond pullback stability` 观察固定成独立说明卡。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-03 fresh-run

- 总行数：`6`
- status 分布：`{"missing_next_session_first_30m_data": 2, "next_session_first_30m_all_closes_inside_prior_ib": 2, "next_session_first_30m_not_all_closes_inside_prior_ib": 2}`
- direction 分布：`{"down": 2, "up": 4}`
- mode 分布：`{"close": 2, "wick": 4}`
- `next_session_first_30m_bar_count_30_rows`：`4`
- `next_session_first_bar_expected_side_rows`：`2`

## Session 分布

- `london`: `{"rows": 2, "status_next_session_first_30m_all_closes_inside_prior_ib": 2}`
- `new_york`: `{"rows": 4, "status_missing_next_session_first_30m_data": 2, "status_next_session_first_30m_not_all_closes_inside_prior_ib": 2}`

## 当前裁决

- `not_beyond stability` 当前只说明：下一同类 session 首 30 分钟是否整体仍在前一日 `IB` 内侧或边界。
- 当前 `2/6` 行满足稳定内侧，`2/6` 行不满足，`2/6` 行缺下一同类 session 数据。
- 后续若继续推进，应从满足稳定内侧的样本再拆 stability persistence，不直接改名成 `failed breakout`。
