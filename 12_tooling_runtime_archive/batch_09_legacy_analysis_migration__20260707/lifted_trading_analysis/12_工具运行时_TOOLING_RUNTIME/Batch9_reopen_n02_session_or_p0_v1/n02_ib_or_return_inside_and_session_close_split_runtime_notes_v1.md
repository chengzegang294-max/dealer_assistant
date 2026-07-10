# N02 IB OR 回到区间内与收盘分桶运行说明 v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `return_inside` 说明卡与 `session_close` 二次分桶的运行口径。

## 当前边界

- 不写回：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `n02_ib_or_post_cross_path_observation_p0_sample_v1.csv`
- 当前只落：
  - `n02_ib_or_return_inside_ib_same_day_candidates_p0_sample_v1.csv`
  - `n02_ib_or_return_inside_ib_same_day_card_v1.md`
  - `n02_ib_or_return_inside_ib_same_day_summary_v1.json`
  - `n02_ib_or_session_close_beyond_ib_candidates_p0_sample_v1.csv`
  - `n02_ib_or_session_close_not_beyond_ib_candidates_p0_sample_v1.csv`
  - `n02_ib_or_session_close_beyond_split_p0_summary_v1.json`
- 当前不推进：
  - `failed breakout`
  - `retest`
  - `reject`
  - `day type`

## 当前怎么用（v1）

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
- 当前字段只表达：
  - `return_inside_ib_observed_same_day`
  - `session_close_beyond_ib`
  - `session_close_not_beyond_ib`

## 推荐复现命令

- `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_return_inside_and_session_close_split_p0_build_v1.py`

## 2026-07-03 fresh-run 结果

- 运行入口：
  - `python n02_ib_or_return_inside_and_session_close_split_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_return_inside_ib_same_day_candidates_p0_sample_v1.csv`
  - `n02_ib_or_return_inside_ib_same_day_card_v1.md`
  - `n02_ib_or_return_inside_ib_same_day_summary_v1.json`
  - `n02_ib_or_session_close_beyond_ib_candidates_p0_sample_v1.csv`
  - `n02_ib_or_session_close_not_beyond_ib_candidates_p0_sample_v1.csv`
  - `n02_ib_or_session_close_beyond_split_p0_summary_v1.json`
- 关键统计：
  - `return_inside_rows=15`
  - `session_close_beyond_ib_rows=9`
  - `session_close_not_beyond_ib_rows=6`
  - `session_close_beyond_ib_ratio=0.6`
  - `london return_inside_rows=2 / beyond_rows=0 / not_beyond_rows=2`
  - `new_york return_inside_rows=13 / beyond_rows=9 / not_beyond_rows=4`
- 当前结论：
  - `return_inside` 已固定成独立说明卡。
  - `session_close` 已完成 beyond / not_beyond 二次分桶。
  - 当前仍只写 observation / split，不写 `failed breakout` 定义。

## 2026-07-03 session_close_branch_cards child fresh-run

- 运行入口：
  - `python n02_ib_or_session_close_beyond_and_not_beyond_cards_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_session_close_beyond_ib_card_v1.md`
  - `n02_ib_or_session_close_beyond_ib_summary_v1.json`
  - `n02_ib_or_session_close_not_beyond_pullback_card_v1.md`
  - `n02_ib_or_session_close_not_beyond_pullback_summary_v1.json`
- 关键统计：
  - `session_close_beyond_ib_rows=9`
  - `session_close_not_beyond_ib_rows=6`
  - `session_close_beyond direction_counts={"down": 4, "up": 5}`
  - `session_close_not_beyond direction_counts={"down": 2, "up": 4}`
- 当前结论：
  - 主线已从 `session_close` 二次分桶推进到两张独立 branch card
  - 当前仍只写 branch card，不写 `failed breakout` 定义

## 当前最顺动作

- 若继续推进，优先补：
  - `session_close_beyond_ib=9` 的 continuation / persistence 观察
  - 或 `session_close_not_beyond_ib=6` 的 pullback stability 观察
- 继续保持不做：
  - `failed breakout`
  - `retest / reject`
  - `day type`
