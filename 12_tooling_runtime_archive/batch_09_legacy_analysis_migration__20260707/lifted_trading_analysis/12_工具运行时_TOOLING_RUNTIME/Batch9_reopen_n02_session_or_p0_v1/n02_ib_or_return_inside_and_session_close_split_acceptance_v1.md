# N02 IB OR 回到区间内与收盘分桶验收 v1

## 目的

- 记录 `REOPEN_B9_N02_IB_OR_RETURN_INSIDE_AND_SESSION_CLOSE_SPLIT_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `n02_ib_or_post_cross_path_observation_p0_sample_v1.csv`
- 生成脚本：
  - `n02_ib_or_return_inside_and_session_close_split_p0_build_v1.py`
- 输出：
  - `n02_ib_or_return_inside_ib_same_day_candidates_p0_sample_v1.csv`
  - `n02_ib_or_return_inside_ib_same_day_card_v1.md`
  - `n02_ib_or_return_inside_ib_same_day_summary_v1.json`
  - `n02_ib_or_session_close_beyond_ib_candidates_p0_sample_v1.csv`
  - `n02_ib_or_session_close_not_beyond_ib_candidates_p0_sample_v1.csv`
  - `n02_ib_or_session_close_beyond_split_p0_summary_v1.json`

## 2026-07-03 fresh-run 验收

- 验收方式：
  - `python n02_ib_or_return_inside_and_session_close_split_p0_build_v1.py`
- 本轮结果：
  - `return_inside_rows=15`
  - `session_close_beyond_ib_rows=9`
  - `session_close_not_beyond_ib_rows=6`
  - `session_close_beyond_ib_ratio=0.6`
  - `london return_inside_rows=2 / beyond_rows=0 / not_beyond_rows=2`
  - `new_york return_inside_rows=13 / beyond_rows=9 / not_beyond_rows=4`
- 当前结论：
  - `return_inside` 说明卡已落盘。
  - `session_close` beyond / not_beyond 二次分桶已落盘。
  - 当前仍只把这层当 observation / split，不升级成 `failed breakout`。

## 关键统计

- `return_inside_rows=15`
- `session_close_beyond_ib_rows=9`
- `session_close_not_beyond_ib_rows=6`
- `session_close_beyond_ib_ratio=0.6`
- `london_beyond_rows=0`
- `newyork_beyond_rows=9`

## 当前不通过项

- 当前还没有把 `session_close_beyond_ib=9` 固定成独立说明卡。
- 当前还没有把 `session_close_not_beyond_ib=6` 固定成回落分支说明。
- 当前仍不进入 `failed breakout / retest / reject / day type`。
