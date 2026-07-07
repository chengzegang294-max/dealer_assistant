# REOPEN_B9_N02 IB OR RETURN_INSIDE_AND_SESSION_CLOSE_SPLIT_P0 关系入口 v1

## 作用

- 把 `post_cross_path observation` 继续推进成两层更明确的下游产物：
  - `return_inside_ib_observed_same_day` 独立说明卡
  - `session_close_beyond_ib / session_close_not_beyond_ib` 二次分桶
- 当前只固定观察与分桶，不升级成 `failed breakout / retest / reject / day type`。

## 当前边界（写死）

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `n02_ib_or_post_cross_path_observation_p0_sample_v1.csv`
- 当前不推进：
  - `failed breakout`
  - `retest`
  - `reject`
  - `day type`

## 当前真值组成（v1）

- `entry_md`：`REOPEN_B9_N02_IB_OR_RETURN_INSIDE_AND_SESSION_CLOSE_SPLIT_P0_关系入口_v1.md`
- `parent_entry_md`：`REOPEN_B9_N02_IB_OR_POST_CROSS_PATH_P0_关系入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_return_inside_and_session_close_split_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_return_inside_and_session_close_split_acceptance_v1.md`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_return_inside_and_session_close_split_p0_build_v1.py`
- `post_cross_observation_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_post_cross_path_observation_p0_sample_v1.csv`
- `return_inside_candidates_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_return_inside_ib_same_day_candidates_p0_sample_v1.csv`
- `return_inside_card_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_return_inside_ib_same_day_card_v1.md`
- `return_inside_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_return_inside_ib_same_day_summary_v1.json`
- `session_close_beyond_candidates_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_session_close_beyond_ib_candidates_p0_sample_v1.csv`
- `session_close_not_beyond_candidates_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_session_close_not_beyond_ib_candidates_p0_sample_v1.csv`
- `session_close_split_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_session_close_beyond_split_p0_summary_v1.json`

## 最小验收（关系开题级）

- `return_inside` 卡必须显式记录：
  - `rows`
  - `session_close_beyond_ib_rows`
  - `session_close_not_beyond_ib_rows`
- `session_close` 二次分桶必须显式记录：
  - `session_close_beyond_ib_rows`
  - `session_close_not_beyond_ib_rows`
  - `by_session`
- 所有输出必须显式保留：
  - `defines_failed_breakout=false`

## 2026-07-03 fresh-run

- 运行入口：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_return_inside_and_session_close_split_p0_build_v1.py`
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
- 当前裁决：
  - `return_inside` 观测已固定成独立说明卡。
  - `session_close_beyond_ib` 与 `session_close_not_beyond_ib` 已完成二次分桶。
  - 当前仍只固定 observation / split，不升级成 `failed breakout`。

## 2026-07-03 session_close_branch_cards child 已开

- 已新增子入口：
  - `REOPEN_B9_N02_IB_OR_SESSION_CLOSE_BRANCH_CARDS_P0_关系入口_v1.md`
- 已新增产物：
  - `n02_ib_or_session_close_beyond_ib_card_v1.md`
  - `n02_ib_or_session_close_beyond_ib_summary_v1.json`
  - `n02_ib_or_session_close_not_beyond_pullback_card_v1.md`
  - `n02_ib_or_session_close_not_beyond_pullback_summary_v1.json`
- 当前最小裁决：
  - `session_close_beyond_ib_rows=9`
  - `session_close_not_beyond_ib_rows=6`
- 当前含义：
  - `session_close_beyond_ib` 已固定成独立说明卡
  - `session_close_not_beyond_ib` 已固定成回落分支说明卡

## 下一步最顺动作

- 若继续沿同一条线推进，优先补：
  - `session_close_beyond_ib=9` 的 continuation / persistence 观察
  - 或 `session_close_not_beyond_ib=6` 的 pullback stability 观察
- 继续保持不做：
  - `failed breakout`
  - `retest / reject`
  - `day type`
