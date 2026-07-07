# n02_ib_or_beyond_multi_session_persistence_card v1

## 作用

- 把 `beyond multi-session persistence` 观察固定成独立说明卡。
- 当前不表达：`failed breakout / retest / reject / day type`。

## 2026-07-04 fresh-run

- 总行数：`2`
- status 分布：`{"second_next_session_first_30m_all_closes_beyond_prior_ib": 2}`
- direction 分布：`{"down": 1, "up": 1}`
- mode 分布：`{"close": 1, "wick": 1}`
- `second_next_session_first_30m_bar_count_30_rows`：`2`
- `second_next_session_first_bar_expected_side_rows`：`2`

## Session 分布

- `new_york`: `{"rows": 2, "status_second_next_session_first_30m_all_closes_beyond_prior_ib": 2}`

## 当前裁决

- `beyond multi-session persistence` 当前只说明：第二个同类 session 首 30 分钟是否整体仍在前一日 `IB` 外侧。
- 当前 `2/2` 行满足持续外侧，`0/2` 行不满足，`0/2` 行缺第二个同类 session 数据。
- 后续若继续推进，应从满足持续外侧的样本再拆第三个同类 session persistence，不直接改名成 `failed breakout`。
