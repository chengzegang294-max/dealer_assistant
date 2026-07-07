# n02_gbpusd_m15_slice_or_break_only_same_day_session_close_acceptance v1

## 目的

- 记录 `REOPEN_B9_N02_GBPUSD_M15_SLICE_OR_BREAK_ONLY_SAME_DAY_SESSION_CLOSE_P0` 的最小验收结果。

## 本次验收对象

- 脚本：
  - `n02_ib_or_or_break_only_same_day_session_close_split_p0_build_v1.py`
- 产物：
  - `n02_ib_or_or_break_only_return_inside_or_same_day_candidates_p0_sample_gbpusd_m15_slice_v1.csv`
  - `n02_ib_or_or_break_only_session_close_beyond_or_candidates_p0_sample_gbpusd_m15_slice_v1.csv`
  - `n02_ib_or_or_break_only_session_close_not_beyond_or_candidates_p0_sample_gbpusd_m15_slice_v1.csv`
  - `n02_ib_or_or_break_only_same_day_session_close_split_p0_summary_gbpusd_m15_slice_v1.json`
  - `n02_ib_or_or_break_only_session_close_beyond_or_card_gbpusd_m15_slice_v1.md`
  - `n02_ib_or_or_break_only_session_close_not_beyond_or_card_gbpusd_m15_slice_v1.md`

## 2026-07-06 fresh-run 验收

- `or_break_only_rows=325`
- `return_inside_or_observed_same_day_rows=312`
- `session_close_beyond_or_rows=168`
- `session_close_not_beyond_or_rows=157`
- `london_rows=167`
- `new_york_rows=158`
- `session_close_beyond_or_direction_counts={"down":96,"up":72}`
- `session_close_not_beyond_or_direction_counts={"down":76,"up":81}`

## 当前结论

- 已确认 `GBPUSD/M15 slice` 的 `or_break_only` 分支可以独立落到 same-day session close 分流。
- 已确认这层不依赖主 runtime 持久化，不污染 `EURUSD/M1` 主链。
- 已确认这层仍不把任何结果改写成 `failed breakout / retest / reject / day type`。

## 当前不通过项

- 当前仍未做：
  - `session_close_beyond_or` 之后的 multi-session 延展
  - `session_close_not_beyond_or` 的 pullback stability 进一步分层
  - 任意 `failed breakout` 定义
