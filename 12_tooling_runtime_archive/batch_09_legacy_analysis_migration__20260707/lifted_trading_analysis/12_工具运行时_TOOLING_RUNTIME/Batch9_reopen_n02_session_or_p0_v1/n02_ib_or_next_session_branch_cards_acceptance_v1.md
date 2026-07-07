# n02_ib_or_next_session_branch_cards_acceptance v1

## 目的

- 记录 `REOPEN_B9_N02_IB_OR_NEXT_SESSION_BRANCH_CARDS_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `n02_ib_or_beyond_continuation_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_pullback_stability_observation_p0_sample_v1.csv`
- 生成脚本：
  - `n02_ib_or_beyond_continuation_and_not_beyond_stability_cards_p0_build_v1.py`
- 输出：
  - `n02_ib_or_beyond_continuation_card_v1.md`
  - `n02_ib_or_beyond_continuation_card_summary_v1.json`
  - `n02_ib_or_not_beyond_stability_card_v1.md`
  - `n02_ib_or_not_beyond_stability_card_summary_v1.json`

## 2026-07-04 fresh-run 验收

- 验收方式：
  - `python n02_ib_or_beyond_continuation_and_not_beyond_stability_cards_p0_build_v1.py`
- 本轮结果：
  - `beyond_rows=9`
  - `beyond_status_counts={"missing_next_session_first_30m_data": 2, "next_session_first_30m_all_closes_beyond_prior_ib": 2, "next_session_first_30m_not_all_closes_beyond_prior_ib": 5}`
  - `not_beyond_rows=6`
  - `not_beyond_status_counts={"missing_next_session_first_30m_data": 2, "next_session_first_30m_all_closes_inside_prior_ib": 2, "next_session_first_30m_not_all_closes_inside_prior_ib": 2}`
- 当前结论：
  - 两张 next-session branch card 已完成独立闭环。
  - `beyond continuation card` 已明确区分持续外侧 / 非持续 / 缺数据。
  - `not_beyond stability card` 已明确区分稳定内侧 / 非稳定 / 缺数据。
  - 当前仍不升级成 `failed breakout / retest / reject / day type`。

## 2026-07-04 child 推进结果

- 已完成：
  - `beyond multi-session persistence` fresh-run
  - `not_beyond multi-session stability` fresh-run
- child 结果：
  - `beyond_status_counts={"second_next_session_first_30m_all_closes_beyond_prior_ib": 2}`
  - `not_beyond_status_counts={"second_next_session_first_30m_all_closes_inside_prior_ib": 1, "second_next_session_first_30m_not_all_closes_inside_prior_ib": 1}`
- 当前含义：
  - next-session 两张卡的默认下一步已不再停留在 extension 待做
  - 当前下一步已切到 `multi-session` 两支的 branch card

## 2026-07-04 grandchild 推进结果

- 已完成：
  - `beyond multi-session persistence card` fresh-run
  - `not_beyond multi-session stability card` fresh-run
- grandchild 结果：
  - `beyond_status_counts={"second_next_session_first_30m_all_closes_beyond_prior_ib": 2}`
  - `not_beyond_status_counts={"second_next_session_first_30m_all_closes_inside_prior_ib": 1, "second_next_session_first_30m_not_all_closes_inside_prior_ib": 1}`
- 当前含义：
  - next-session 两张卡的下游已经继续推进到 multi-session branch cards
  - 当前下一步已切到 `third same-session persistence / stability observation`

## 关键统计

- `beyond_all_closes_beyond_prior_ib=2`
- `beyond_not_all_closes_beyond_prior_ib=5`
- `beyond_missing=2`
- `not_beyond_all_closes_inside_prior_ib=2`
- `not_beyond_not_all_closes_inside_prior_ib=2`
- `not_beyond_missing=2`

## 当前不通过项

- 当前还没有把 `beyond multi-session persistence` 推进到第三个同类 `session` observation。
- 当前还没有把 `not_beyond multi-session stability` 推进到第三个同类 `session` observation。
