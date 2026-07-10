# N02 IB OR 第三同会话延续稳定性验收 v1

## 目的

- 记录 `REOPEN_B9_N02_IB_OR_THIRD_SAME_SESSION_PERSISTENCE_STABILITY_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `n02_ib_or_beyond_multi_session_persistence_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_multi_session_stability_observation_p0_sample_v1.csv`
  - `real_input_samples\n02_first_real_input_bars_v1.csv`
- 生成脚本：
  - `n02_ib_or_third_same_session_persistence_and_stability_p0_build_v1.py`
- 输出：
  - `n02_ib_or_beyond_third_same_session_persistence_observation_p0_sample_v1.csv`
  - `n02_ib_or_beyond_third_same_session_persistence_observation_p0_summary_v1.json`
  - `n02_ib_or_not_beyond_third_same_session_stability_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_third_same_session_stability_observation_p0_summary_v1.json`

## 2026-07-04 fresh-run 验收

- 验收方式：
  - `python n02_ib_or_third_same_session_persistence_and_stability_p0_build_v1.py`
- 本轮结果：
  - `beyond_rows=2`
  - `beyond_status_counts={"third_next_session_first_30m_all_closes_beyond_prior_ib": 2}`
  - `not_beyond_rows=1`
  - `not_beyond_status_counts={"missing_third_next_session_first_30m_data": 1}`
- 当前结论：
  - `beyond third same-session persistence` 已完成最小 fresh-run 闭环，当前 `2/2` 行持续外侧。
  - `not_beyond third same-session stability` 已完成最小 fresh-run 闭环，当前 `1/1` 行缺第三个同类 `session` 数据。
  - 当前仍不升级成 `failed breakout / retest / reject / day type`。

## 关键统计

- `beyond_third_next_all_closes_beyond_prior_ib=2`
- `beyond_third_next_not_all_closes_beyond_prior_ib=0`
- `beyond_third_next_missing=0`
- `not_beyond_third_next_all_closes_inside_prior_ib=0`
- `not_beyond_third_next_not_all_closes_inside_prior_ib=0`
- `not_beyond_third_next_missing=1`

## 当前不通过项

- 当前 observation 层已经完成，child 已继续推进到 branch card。
- 当前还没有把 `third same-session` 两支继续外推成 terminal summary 或更大样本覆盖。
