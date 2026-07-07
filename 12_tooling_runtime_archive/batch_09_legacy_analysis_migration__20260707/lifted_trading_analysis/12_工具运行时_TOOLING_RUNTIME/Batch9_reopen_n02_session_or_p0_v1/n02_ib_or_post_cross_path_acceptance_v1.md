# n02_ib_or_post_cross_path_acceptance v1

## 目的

- 记录 `REOPEN_B9_N02_IB_OR_POST_CROSS_PATH_P0` 的最小验收结论。

## 本次验收对象

- 输入：
  - `n02_ib_or_confirmed_cross_candidates_p0_sample_v1.csv`
  - `n02_ib_or_confirmed_cross_outcome_shell_p0_sample_v1.csv`
  - `n02_ib_or_or_break_only_candidates_p0_sample_v1.csv`
  - `real_input_samples\n02_first_real_input_bars_v1.csv`
- 生成脚本：
  - `n02_ib_or_post_cross_path_and_or_break_only_card_p0_build_v1.py`
- 输出：
  - `n02_ib_or_post_cross_path_observation_p0_sample_v1.csv`
  - `n02_ib_or_post_cross_path_observation_p0_summary_v1.json`
  - `n02_ib_or_or_break_only_branch_card_v1.md`
  - `n02_ib_or_or_break_only_branch_summary_v1.json`

## 2026-07-03 fresh-run 验收

- 验收方式：
  - `python n02_ib_or_post_cross_path_and_or_break_only_card_p0_build_v1.py`
- 本轮结果：
  - `post_cross_rows=15`
  - `return_inside_ib_observed_same_day_rows=15`
  - `session_close_beyond_ib_rows=9`
  - `or_break_only_rows=123`
  - `or_break_only_gap_bucket_counts={"0.00010_to_0.00049": 64, "ge_0.00050": 30, "lt_0.00010": 29}`
- 当前结论：
  - `confirmed_cross` 分支已拿到同日 post-cross 观察样本。
  - `OR break only` 分支已拿到独立说明卡与摘要。
  - 当前观察到 `15/15` 行都回到 `IB` 边界内侧，但仍只存为 observation，不升级成 `failed breakout`。

## 关键统计

- `post_cross_rows=15`
- `return_inside_ib_observed_same_day=15`
- `session_close_beyond_ib=9`
- `or_break_only_rows=123`
- `gap_bucket_0.00010_to_0.00049=64`
- `gap_bucket_ge_0.00050=30`
- `gap_bucket_lt_0.00010=29`

## 当前不通过项

- 当前还没有把 `return_inside_ib_observed_same_day` 提升为对象级定义。
- 当前还没有把 `session_close_beyond_ib` 做二次分桶。
- 当前仍不进入 `failed breakout / retest / reject / day type`。
