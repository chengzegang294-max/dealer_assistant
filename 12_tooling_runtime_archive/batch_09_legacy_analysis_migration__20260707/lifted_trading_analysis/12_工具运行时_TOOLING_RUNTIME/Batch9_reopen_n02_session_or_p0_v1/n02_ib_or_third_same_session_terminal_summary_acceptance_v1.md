# n02_ib_or_third_same_session_terminal_summary_acceptance v1

## 目的

- 记录 `REOPEN_B9_N02_IB_OR_THIRD_SAME_SESSION_TERMINAL_SUMMARY_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `n02_ib_or_beyond_third_same_session_persistence_card_summary_v1.json`
  - `n02_ib_or_not_beyond_third_same_session_stability_card_summary_v1.json`
- 生成脚本：
  - `n02_ib_or_third_same_session_terminal_summary_build_v1.py`
- 输出：
  - `n02_ib_or_third_same_session_terminal_summary_v1.md`
  - `n02_ib_or_third_same_session_terminal_summary_v1.json`

## 2026-07-04 fresh-run 验收

- 验收方式：
  - `python n02_ib_or_third_same_session_terminal_summary_build_v1.py`
- 本轮结果：
  - `total_rows=3`
  - `resolved_rows=2`
  - `missing_rows=1`
  - `beyond_status_counts={"third_next_session_first_30m_all_closes_beyond_prior_ib": 2}`
  - `not_beyond_status_counts={"missing_third_next_session_first_30m_data": 1}`
- 当前结论：
  - `third same-session terminal summary` 已完成最小闭环，当前可确认的 `2/3` 行都落在 `beyond persistence` 支。
  - `not_beyond` 当前 `1/3` 行仍缺第三个同类 `session` 数据，只保留 `missing`。
  - 当前仍不升级成 `failed breakout / retest / reject / day type`。

## 关键统计

- `beyond_persistent_rows=2`
- `beyond_failed_rows=0`
- `beyond_missing_rows=0`
- `not_beyond_stable_rows=0`
- `not_beyond_unstable_rows=0`
- `not_beyond_missing_rows=1`

## 当前不通过项

- 当前 terminal summary 还没有扩到 `EURUSD M1 london/new_york` 之外的样本覆盖。
