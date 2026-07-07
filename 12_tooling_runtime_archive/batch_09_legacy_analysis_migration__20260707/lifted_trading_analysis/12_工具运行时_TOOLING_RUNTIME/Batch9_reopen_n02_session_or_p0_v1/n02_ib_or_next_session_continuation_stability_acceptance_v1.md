# n02_ib_or_next_session_continuation_stability_acceptance v1

## 目的

- 记录 `REOPEN_B9_N02_IB_OR_NEXT_SESSION_CONTINUATION_STABILITY_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `n02_ib_or_session_close_beyond_ib_candidates_p0_sample_v1.csv`
  - `n02_ib_or_session_close_not_beyond_ib_candidates_p0_sample_v1.csv`
  - `n02_ib_or_post_cross_path_observation_p0_sample_v1.csv`
  - `real_input_samples\n02_first_real_input_bars_v1.csv`
  - `real_input_samples\n02_or_proof_config_v1.json`
- 生成脚本：
  - `n02_ib_or_beyond_continuation_and_not_beyond_stability_p0_build_v1.py`
- 输出：
  - `n02_ib_or_beyond_continuation_observation_p0_sample_v1.csv`
  - `n02_ib_or_beyond_continuation_observation_p0_summary_v1.json`
  - `n02_ib_or_not_beyond_pullback_stability_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_pullback_stability_observation_p0_summary_v1.json`

## 2026-07-03 fresh-run 验收

- 验收方式：
  - `python n02_ib_or_beyond_continuation_and_not_beyond_stability_p0_build_v1.py`
- 本轮结果：
  - `beyond_rows=9`
  - `beyond_status_counts={"missing_next_session_first_30m_data": 2, "next_session_first_30m_all_closes_beyond_prior_ib": 2, "next_session_first_30m_not_all_closes_beyond_prior_ib": 5}`
  - `not_beyond_rows=6`
  - `not_beyond_status_counts={"missing_next_session_first_30m_data": 2, "next_session_first_30m_all_closes_inside_prior_ib": 2, "next_session_first_30m_not_all_closes_inside_prior_ib": 2}`
- 当前结论：
  - `beyond continuation` 与 `not_beyond pullback stability` 都已形成最小观察闭环。
  - 当前可以明确区分：
    - 持续外侧 / 稳定内侧
    - 非持续 / 非稳定
    - 缺下一同类 session 数据
  - 当前仍不升级成 `failed breakout / retest / reject / day type`。

## 关键统计

- `beyond_all_closes_beyond_prior_ib=2`
- `beyond_not_all_closes_beyond_prior_ib=5`
- `beyond_missing=2`
- `not_beyond_all_closes_inside_prior_ib=2`
- `not_beyond_not_all_closes_inside_prior_ib=2`
- `not_beyond_missing=2`

## 当前不通过项

- 当前还没有把 `beyond continuation 2/9` 固定成独立说明卡。
- 当前还没有把 `not_beyond pullback stability 2/6` 固定成独立说明卡。
