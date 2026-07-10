# N02 IB OR 仅 OR 突破收盘超出 OR 多会话延续说明卡 GBPUSD M15 切片 v1

## 作用

- 把 `or_break_only beyond_or` 的 multi-session persistence 固定成独立说明卡。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-06 fresh-run

- 总行数：`105`
- status 分布：`{"missing_second_next_session_first_30m_data": 27, "second_next_session_first_30m_all_closes_beyond_prior_or": 57, "second_next_session_first_30m_not_all_closes_beyond_prior_or": 21}`
- direction 分布：`{"down": 55, "up": 50}`
- mode 分布：`{"close": 50, "wick": 55}`
- `second_next_session_first_30m_full_window_rows`：`78`
- `second_next_session_first_bar_expected_side_rows`：`57`

## Session 分布

- `london`: `{"rows": 61, "status_second_next_session_first_30m_not_all_closes_beyond_prior_or": 14, "status_missing_second_next_session_first_30m_data": 17, "status_second_next_session_first_30m_all_closes_beyond_prior_or": 30}`
- `new_york`: `{"rows": 44, "status_second_next_session_first_30m_all_closes_beyond_prior_or": 27, "status_missing_second_next_session_first_30m_data": 10, "status_second_next_session_first_30m_not_all_closes_beyond_prior_or": 7}`

## 当前裁决

- 当前只说明：对 next-session `all closes beyond prior OR` 的样本，第二个 next-session 首 30 分钟是否仍全体 close 在 prior `OR` 外侧同方向。
- 当前 `57/105` 行满足持续外侧，`21/105` 行不满足，`27/105` 行缺第二个 next-session 数据。
- 后续若继续推进，应只从满足持续外侧的样本再拆 persistence，不直接改名成 `failed breakout`。
