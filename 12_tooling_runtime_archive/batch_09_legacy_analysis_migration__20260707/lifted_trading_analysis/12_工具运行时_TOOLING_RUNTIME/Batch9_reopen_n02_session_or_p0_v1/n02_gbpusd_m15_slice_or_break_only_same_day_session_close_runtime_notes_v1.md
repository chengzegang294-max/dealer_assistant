# n02_gbpusd_m15_slice_or_break_only_same_day_session_close_runtime_notes v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是把 `GBPUSD/M15 slice -> or_break_only -> same-day session close` 这条新支线固定成可追溯闭环。

## 当前边界

- 当前输入只来自：
  - `n02_ib_or_or_break_only_candidates_p0_sample_gbpusd_m15_slice_v1.csv`
  - `real_input_samples\n02_real_input_gbpusd_m15_v1.csv`
- 当前只观察：
  - `return_inside_or_observed_same_day`
  - `session_close_beyond_or`
  - `session_close_not_beyond_or`
- 当前不定义：
  - `failed breakout`
  - `retest / reject / day type`
  - 更高层 continuation / persistence

## 当前怎么跑（v1）

- 生成脚本：
  - `n02_ib_or_or_break_only_same_day_session_close_split_p0_build_v1.py`
- 关键产物：
  - `n02_ib_or_or_break_only_return_inside_or_same_day_candidates_p0_sample_gbpusd_m15_slice_v1.csv`
  - `n02_ib_or_or_break_only_session_close_beyond_or_candidates_p0_sample_gbpusd_m15_slice_v1.csv`
  - `n02_ib_or_or_break_only_session_close_not_beyond_or_candidates_p0_sample_gbpusd_m15_slice_v1.csv`
  - `n02_ib_or_or_break_only_same_day_session_close_split_p0_summary_gbpusd_m15_slice_v1.json`
  - `n02_ib_or_or_break_only_session_close_beyond_or_card_gbpusd_m15_slice_v1.md`
  - `n02_ib_or_or_break_only_session_close_beyond_or_summary_gbpusd_m15_slice_v1.json`
  - `n02_ib_or_or_break_only_session_close_not_beyond_or_card_gbpusd_m15_slice_v1.md`
  - `n02_ib_or_or_break_only_session_close_not_beyond_or_summary_gbpusd_m15_slice_v1.json`

## 2026-07-06 fresh-run 结果

- `or_break_only_rows=325`
- `return_inside_or_observed_same_day_rows=312`
- `session_close_beyond_or_rows=168`
- `session_close_not_beyond_or_rows=157`
- `by_session={"london":{"rows":167,"return_inside_or_rows":165,"session_close_beyond_or_rows":88,"session_close_not_beyond_or_rows":79},"new_york":{"rows":158,"return_inside_or_rows":147,"session_close_beyond_or_rows":80,"session_close_not_beyond_or_rows":78}}`
- `session_close_beyond_or_direction_counts={"down":96,"up":72}`
- `session_close_not_beyond_or_direction_counts={"down":76,"up":81}`

## 当前结论

- `or_break_only` 分支已经不再只有 gap bucket 说明卡，现已推进到 same-day `session close` 分流。
- 其中 `session_close_beyond_or` 已继续补到下一同类 session 首 30 分钟 continuation 观察。
- 当前主线可明确区分：
  - 首破后同日收盘仍在 OR 外侧
  - 首破后同日收盘回到 OR 内侧或边界
- 这层结果仍然只属于 `without_failed_breakout`。
