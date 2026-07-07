# n02_ib_or_session_close_branch_cards_acceptance v1

## 目的

- 记录 `REOPEN_B9_N02_IB_OR_SESSION_CLOSE_BRANCH_CARDS_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `n02_ib_or_session_close_beyond_ib_candidates_p0_sample_v1.csv`
  - `n02_ib_or_session_close_not_beyond_ib_candidates_p0_sample_v1.csv`
- 生成脚本：
  - `n02_ib_or_session_close_beyond_and_not_beyond_cards_p0_build_v1.py`
- 输出：
  - `n02_ib_or_session_close_beyond_ib_card_v1.md`
  - `n02_ib_or_session_close_beyond_ib_summary_v1.json`
  - `n02_ib_or_session_close_not_beyond_pullback_card_v1.md`
  - `n02_ib_or_session_close_not_beyond_pullback_summary_v1.json`

## 2026-07-03 fresh-run 验收

- 验收方式：
  - `python n02_ib_or_session_close_beyond_and_not_beyond_cards_p0_build_v1.py`
- 本轮结果：
  - `session_close_beyond_ib_rows=9`
  - `session_close_not_beyond_ib_rows=6`
  - `session_close_beyond direction_counts={"down": 4, "up": 5}`
  - `session_close_not_beyond direction_counts={"down": 2, "up": 4}`
  - `session_close_beyond extension_bucket_counts={"0.001_to_0.00299": 5, "ge_0.003": 3, "lt_0.001": 1}`
  - `session_close_not_beyond extension_bucket_counts={"0.001_to_0.00299": 3, "ge_0.003": 1, "lt_0.001": 2}`
- 当前结论：
  - 两支都已完成独立 branch card + summary 闭环。
  - `session_close_beyond_ib` 当前全部位于 `new_york`。
  - `session_close_not_beyond_ib` 当前覆盖 `london + new_york`。
  - 当前仍不升级成 `failed breakout / retest / reject / day type`。

## 关键统计

- `session_close_beyond_ib_rows=9`
- `session_close_not_beyond_ib_rows=6`
- `session_close_beyond_newyork_rows=9`
- `session_close_not_beyond_london_rows=2`
- `session_close_not_beyond_newyork_rows=4`

## 当前不通过项

- 当前还没有为 `session_close_beyond_ib=9` 补 continuation / persistence 观察。
- 当前还没有为 `session_close_not_beyond_ib=6` 补 pullback stability 观察。
