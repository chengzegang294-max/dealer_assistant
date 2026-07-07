# n02_ib_or_multi_session_persistence_stability_acceptance v1

## 目的

- 记录 `REOPEN_B9_N02_IB_OR_MULTI_SESSION_PERSISTENCE_STABILITY_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `n02_ib_or_beyond_continuation_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_pullback_stability_observation_p0_sample_v1.csv`
  - `real_input_samples\n02_first_real_input_bars_v1.csv`
- 生成脚本：
  - `n02_ib_or_multi_session_persistence_and_stability_p0_build_v1.py`
- 输出：
  - `n02_ib_or_beyond_multi_session_persistence_observation_p0_sample_v1.csv`
  - `n02_ib_or_beyond_multi_session_persistence_observation_p0_summary_v1.json`
  - `n02_ib_or_not_beyond_multi_session_stability_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_multi_session_stability_observation_p0_summary_v1.json`

## 2026-07-04 fresh-run 验收

- 验收方式：
  - `python n02_ib_or_multi_session_persistence_and_stability_p0_build_v1.py`
- 本轮结果：
  - `beyond_rows=2`
  - `beyond_status_counts={"second_next_session_first_30m_all_closes_beyond_prior_ib": 2}`
  - `not_beyond_rows=2`
  - `not_beyond_status_counts={"second_next_session_first_30m_all_closes_inside_prior_ib": 1, "second_next_session_first_30m_not_all_closes_inside_prior_ib": 1}`
- 当前结论：
  - `beyond multi-session persistence` 已完成最小 fresh-run 闭环，当前 `2/2` 行持续外侧。
  - `not_beyond multi-session stability` 已完成最小 fresh-run 闭环，当前 `1/2` 行稳定内侧、`1/2` 行失稳。
  - 当前仍不升级成 `failed breakout / retest / reject / day type`。

## 2026-07-04 child 推进结果

- 已完成：
  - `beyond multi-session persistence card` fresh-run
  - `not_beyond multi-session stability card` fresh-run
- child 结果：
  - `beyond_status_counts={"second_next_session_first_30m_all_closes_beyond_prior_ib": 2}`
  - `not_beyond_status_counts={"second_next_session_first_30m_all_closes_inside_prior_ib": 1, "second_next_session_first_30m_not_all_closes_inside_prior_ib": 1}`
- 当前含义：
  - multi-session 两支的默认下一步已不再停留在 card 待做
  - 当前下一步已切到 `third same-session persistence / stability observation`

## 关键统计

- `beyond_second_next_all_closes_beyond_prior_ib=2`
- `beyond_second_next_not_all_closes_beyond_prior_ib=0`
- `beyond_second_next_missing=0`
- `not_beyond_second_next_all_closes_inside_prior_ib=1`
- `not_beyond_second_next_not_all_closes_inside_prior_ib=1`
- `not_beyond_second_next_missing=0`

## 当前不通过项

- 当前还没有把 `beyond multi-session persistence` 推进到第三个同类 `session` observation。
- 当前还没有把 `not_beyond multi-session stability` 推进到第三个同类 `session` observation。
