# REOPEN_B9_N02 IB OR SESSION_CLOSE_BRANCH_CARDS_P0 关系入口 v1

## 作用

- 把 `session_close_beyond_ib` 与 `session_close_not_beyond_ib` 都固定成独立分支说明卡。
- 当前只表达：
  - 收盘仍在 `IB` 外侧的分支
  - 收盘已回到 `IB` 内侧或边界的回落分支
- 当前不表达：
  - `failed breakout`
  - `retest / reject`
  - `day type`

## 当前边界（写死）

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `n02_ib_or_post_cross_path_observation_p0_sample_v1.csv`
  - `n02_ib_or_session_close_beyond_ib_candidates_p0_sample_v1.csv`
  - `n02_ib_or_session_close_not_beyond_ib_candidates_p0_sample_v1.csv`
- 当前只新增：
  - 分支说明卡
  - 分支摘要

## 当前真值组成（v1）

- `entry_md`：`REOPEN_B9_N02_IB_OR_SESSION_CLOSE_BRANCH_CARDS_P0_关系入口_v1.md`
- `parent_entry_md`：`REOPEN_B9_N02_IB_OR_RETURN_INSIDE_AND_SESSION_CLOSE_SPLIT_P0_关系入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_session_close_branch_cards_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_session_close_branch_cards_acceptance_v1.md`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_session_close_beyond_and_not_beyond_cards_p0_build_v1.py`
- `session_close_beyond_candidates_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_session_close_beyond_ib_candidates_p0_sample_v1.csv`
- `session_close_not_beyond_candidates_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_session_close_not_beyond_ib_candidates_p0_sample_v1.csv`
- `session_close_beyond_card_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_session_close_beyond_ib_card_v1.md`
- `session_close_beyond_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_session_close_beyond_ib_summary_v1.json`
- `session_close_not_beyond_pullback_card_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_session_close_not_beyond_pullback_card_v1.md`
- `session_close_not_beyond_pullback_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_session_close_not_beyond_pullback_summary_v1.json`

## 最小验收（关系开题级）

- `session_close_beyond_ib` 必须有：
  - 独立说明卡
  - 独立摘要
  - `by_session / direction / mode / extension bucket`
- `session_close_not_beyond_ib` 必须有：
  - 独立回落说明卡
  - 独立摘要
  - `by_session / direction / mode / extension bucket`
- 所有输出必须显式保留：
  - `defines_failed_breakout=false`

## 2026-07-03 fresh-run

- 运行入口：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_session_close_beyond_and_not_beyond_cards_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_session_close_beyond_ib_card_v1.md`
  - `n02_ib_or_session_close_beyond_ib_summary_v1.json`
  - `n02_ib_or_session_close_not_beyond_pullback_card_v1.md`
  - `n02_ib_or_session_close_not_beyond_pullback_summary_v1.json`
- 关键统计：
  - `session_close_beyond_ib_rows=9`
  - `session_close_not_beyond_ib_rows=6`
  - `session_close_beyond by_session={"new_york": {"rows": 9, "direction_down": 4, "mode_close": 4, "direction_up": 5, "mode_wick": 5}}`
  - `session_close_not_beyond by_session={"london": {"rows": 2, "direction_up": 2, "mode_wick": 1, "mode_close": 1}, "new_york": {"rows": 4, "direction_up": 2, "mode_wick": 3, "direction_down": 2, "mode_close": 1}}`
- 当前裁决：
  - `session_close_beyond_ib` 已固定成独立说明卡，当前样本全部来自 `new_york`。
  - `session_close_not_beyond_ib` 已固定成回落分支说明卡，当前覆盖 `london + new_york`。
  - 当前仍只写 branch card，不升级成 `failed breakout`。

## 2026-07-03 next_session_continuation_stability child 已开

- 已新增子入口：
  - `REOPEN_B9_N02_IB_OR_NEXT_SESSION_CONTINUATION_STABILITY_P0_关系入口_v1.md`
- 已新增产物：
  - `n02_ib_or_beyond_continuation_observation_p0_sample_v1.csv`
  - `n02_ib_or_beyond_continuation_observation_p0_summary_v1.json`
  - `n02_ib_or_not_beyond_pullback_stability_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_pullback_stability_observation_p0_summary_v1.json`
- 当前最小裁决：
  - `beyond_all_closes_beyond_prior_ib=2/9`
  - `not_beyond_all_closes_inside_prior_ib=2/6`
  - `beyond_missing=2`
  - `not_beyond_missing=2`
- 当前含义：
  - `session_close_beyond_ib` 已进入下一同类 session 首 30 分钟 continuation 观察
  - `session_close_not_beyond_ib` 已进入下一同类 session 首 30 分钟 pullback stability 观察
  - 当前已继续固定成 next-session branch cards

## 下一步最顺动作

- 若继续沿同一条线推进，优先补：
  - `beyond continuation 2/9` 的持续外侧说明卡
  - 或 `not_beyond pullback stability 2/6` 的稳定内侧说明卡
