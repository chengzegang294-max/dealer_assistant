# n02_ib_or_session_close_branch_cards_runtime_notes v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `session_close_beyond_ib` 与 `session_close_not_beyond_ib` 两张分支说明卡的运行口径。

## 当前边界

- 不写回：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `n02_ib_or_post_cross_path_observation_p0_sample_v1.csv`
- 当前只落：
  - `n02_ib_or_session_close_beyond_ib_card_v1.md`
  - `n02_ib_or_session_close_beyond_ib_summary_v1.json`
  - `n02_ib_or_session_close_not_beyond_pullback_card_v1.md`
  - `n02_ib_or_session_close_not_beyond_pullback_summary_v1.json`
- 当前不推进：
  - `failed breakout`
  - `retest`
  - `reject`
  - `day type`

## 当前怎么用（v1）

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
- 当前字段只表达：
  - `session_close_beyond_ib`
  - `session_close_not_beyond_ib`
  - 分支级 `direction / mode / extension bucket`

## 推荐复现命令

- `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_session_close_beyond_and_not_beyond_cards_p0_build_v1.py`

## 2026-07-03 fresh-run 结果

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
  - `session_close_beyond extension_bucket_counts={"0.001_to_0.00299": 5, "ge_0.003": 3, "lt_0.001": 1}`
  - `session_close_not_beyond extension_bucket_counts={"0.001_to_0.00299": 3, "ge_0.003": 1, "lt_0.001": 2}`
- 当前结论：
  - `session_close_beyond_ib` 已固定成独立说明卡。
  - `session_close_not_beyond_ib` 已固定成回落分支说明卡。
  - 当前仍只写 branch card，不写 `failed breakout` 定义。

## 2026-07-03 next_session_continuation_stability child fresh-run

- 运行入口：
  - `python n02_ib_or_beyond_continuation_and_not_beyond_stability_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_beyond_continuation_observation_p0_sample_v1.csv`
  - `n02_ib_or_beyond_continuation_observation_p0_summary_v1.json`
  - `n02_ib_or_not_beyond_pullback_stability_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_pullback_stability_observation_p0_summary_v1.json`
- 关键统计：
  - `beyond_all_closes_beyond_prior_ib=2/9`
  - `beyond_not_all_closes_beyond_prior_ib=5/9`
  - `beyond_missing=2/9`
  - `not_beyond_all_closes_inside_prior_ib=2/6`
  - `not_beyond_not_all_closes_inside_prior_ib=2/6`
  - `not_beyond_missing=2/6`
- 当前结论：
  - 主线已从分支说明卡推进到下一同类 session 首 30 分钟观察
  - 当前仍只写 observation，不写 `failed breakout` 定义

## 当前最顺动作

- 若继续推进，优先补：
  - `beyond continuation 2/9` 的持续外侧说明卡
  - 或 `not_beyond pullback stability 2/6` 的稳定内侧说明卡
