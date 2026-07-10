# N02 IB OR 超出后延续说明卡 v1

## 作用

- 把 `beyond continuation` 观察固定成独立说明卡。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-03 fresh-run

- 总行数：`9`
- status 分布：`{"missing_next_session_first_30m_data": 2, "next_session_first_30m_all_closes_beyond_prior_ib": 2, "next_session_first_30m_not_all_closes_beyond_prior_ib": 5}`
- direction 分布：`{"down": 4, "up": 5}`
- mode 分布：`{"close": 4, "wick": 5}`
- `next_session_first_30m_bar_count_30_rows`：`7`
- `next_session_first_bar_expected_side_rows`：`3`

## Session 分布

- `new_york`: `{"rows": 9, "status_missing_next_session_first_30m_data": 2, "status_next_session_first_30m_all_closes_beyond_prior_ib": 2, "status_next_session_first_30m_not_all_closes_beyond_prior_ib": 5}`

## 当前裁决

- `beyond continuation` 当前只说明：下一同类 session 首 30 分钟是否整体仍在前一日 `IB` 外侧。
- 当前 `2/9` 行满足持续外侧，`5/9` 行不满足，`2/9` 行缺下一同类 session 数据。
- 后续若继续推进，应从满足持续外侧的样本再拆 continuation persistence，不直接改名成 `failed breakout`。
