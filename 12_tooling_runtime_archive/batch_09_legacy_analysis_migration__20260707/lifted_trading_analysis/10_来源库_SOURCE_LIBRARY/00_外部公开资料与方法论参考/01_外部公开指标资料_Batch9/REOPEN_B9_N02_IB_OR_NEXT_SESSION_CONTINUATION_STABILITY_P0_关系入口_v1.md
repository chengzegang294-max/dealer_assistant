# REOPEN_B9_N02 IB OR NEXT_SESSION_CONTINUATION_STABILITY_P0 关系入口 v1

## 作用

- 把 `session_close_beyond_ib` 分支继续推进到“下一同类 session 首 30 分钟 continuation 观察”。
- 把 `session_close_not_beyond_ib` 分支继续推进到“下一同类 session 首 30 分钟 pullback stability 观察”。
- 当前只表达下一同类 session 首 30 分钟相对前一日 `IB` 同侧边界的位置关系，不升级成 `failed breakout / retest / reject / day type`。

## 当前边界（写死）

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `n02_ib_or_session_close_beyond_ib_candidates_p0_sample_v1.csv`
  - `n02_ib_or_session_close_not_beyond_ib_candidates_p0_sample_v1.csv`
- 当前只新增：
  - `beyond continuation` 观察样本与摘要
  - `not_beyond pullback stability` 观察样本与摘要

## 当前真值组成（v1）

- `entry_md`：`REOPEN_B9_N02_IB_OR_NEXT_SESSION_CONTINUATION_STABILITY_P0_关系入口_v1.md`
- `parent_entry_md`：`REOPEN_B9_N02_IB_OR_SESSION_CLOSE_BRANCH_CARDS_P0_关系入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_next_session_continuation_stability_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_next_session_continuation_stability_acceptance_v1.md`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_beyond_continuation_and_not_beyond_stability_p0_build_v1.py`
- `session_close_beyond_candidates_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_session_close_beyond_ib_candidates_p0_sample_v1.csv`
- `session_close_not_beyond_candidates_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_session_close_not_beyond_ib_candidates_p0_sample_v1.csv`
- `post_cross_observation_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_post_cross_path_observation_p0_sample_v1.csv`
- `bars_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_first_real_input_bars_v1.csv`
- `beyond_continuation_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_beyond_continuation_observation_p0_sample_v1.csv`
- `beyond_continuation_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_beyond_continuation_observation_p0_summary_v1.json`
- `not_beyond_stability_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_not_beyond_pullback_stability_observation_p0_sample_v1.csv`
- `not_beyond_stability_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_not_beyond_pullback_stability_observation_p0_summary_v1.json`

## 最小验收（关系开题级）

- `beyond continuation` 必须显式记录：
  - `missing_next_session_first_30m_data`
  - `next_session_first_30m_all_closes_beyond_prior_ib`
  - `next_session_first_30m_not_all_closes_beyond_prior_ib`
- `not_beyond pullback stability` 必须显式记录：
  - `missing_next_session_first_30m_data`
  - `next_session_first_30m_all_closes_inside_prior_ib`
  - `next_session_first_30m_not_all_closes_inside_prior_ib`
- 所有输出都必须显式保留：
  - `defines_failed_breakout=false`

## 2026-07-03 fresh-run

- 运行入口：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_beyond_continuation_and_not_beyond_stability_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_beyond_continuation_observation_p0_sample_v1.csv`
  - `n02_ib_or_beyond_continuation_observation_p0_summary_v1.json`
  - `n02_ib_or_not_beyond_pullback_stability_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_pullback_stability_observation_p0_summary_v1.json`
- 关键统计：
  - `beyond_rows=9`
  - `beyond_status_counts={"missing_next_session_first_30m_data": 2, "next_session_first_30m_all_closes_beyond_prior_ib": 2, "next_session_first_30m_not_all_closes_beyond_prior_ib": 5}`
  - `not_beyond_rows=6`
  - `not_beyond_status_counts={"missing_next_session_first_30m_data": 2, "next_session_first_30m_all_closes_inside_prior_ib": 2, "next_session_first_30m_not_all_closes_inside_prior_ib": 2}`
- 当前裁决：
  - `beyond continuation` 当前只有 `2/9` 行在下一同类 session 首 30 分钟持续位于前一日 `IB` 外侧。
  - `not_beyond pullback stability` 当前有 `2/6` 行在下一同类 session 首 30 分钟稳定保持在前一日 `IB` 内侧。
  - 两支各有 `2` 行因为缺下一同类 session 数据而保留为 `missing`。
  - 当前仍只做观察层，不升级成 `failed breakout`。

## 2026-07-04 next_session_branch_cards child 已开

- 已新增子入口：
  - `REOPEN_B9_N02_IB_OR_NEXT_SESSION_BRANCH_CARDS_P0_关系入口_v1.md`
- 已新增产物：
  - `n02_ib_or_beyond_continuation_card_v1.md`
  - `n02_ib_or_beyond_continuation_card_summary_v1.json`
  - `n02_ib_or_not_beyond_stability_card_v1.md`
  - `n02_ib_or_not_beyond_stability_card_summary_v1.json`
- 当前最小裁决：
  - `beyond continuation 2/9` 已固定成独立说明卡
  - `not_beyond stability 2/6` 已固定成独立说明卡
- 当前含义：
  - 下一同类 `session` 的 continuation / stability 观察已升级成 branch card
  - 当前仍只写 card，不升级成 `failed breakout`

## 2026-07-04 multi_session_persistence_stability child 已开

- 已新增子入口：
  - `REOPEN_B9_N02_IB_OR_MULTI_SESSION_PERSISTENCE_STABILITY_P0_关系入口_v1.md`
- 已新增产物：
  - `n02_ib_or_beyond_multi_session_persistence_observation_p0_sample_v1.csv`
  - `n02_ib_or_beyond_multi_session_persistence_observation_p0_summary_v1.json`
  - `n02_ib_or_not_beyond_multi_session_stability_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_multi_session_stability_observation_p0_summary_v1.json`
- 当前最小裁决：
  - `beyond continuation 2/9` 进入第二个同类 `session` 后，当前 `2/2` 行继续外侧
  - `not_beyond stability 2/6` 进入第二个同类 `session` 后，当前 `1/2` 行继续内侧
- 当前含义：
  - continuation / stability 已继续推进到 multi-session observation
  - 当前仍只写 observation，不升级成 `failed breakout`

## 2026-07-04 multi_session_branch_cards child 已开

- 已新增子入口：
  - `REOPEN_B9_N02_IB_OR_MULTI_SESSION_BRANCH_CARDS_P0_关系入口_v1.md`
- 已新增产物：
  - `n02_ib_or_beyond_multi_session_persistence_card_v1.md`
  - `n02_ib_or_beyond_multi_session_persistence_card_summary_v1.json`
  - `n02_ib_or_not_beyond_multi_session_stability_card_v1.md`
  - `n02_ib_or_not_beyond_multi_session_stability_card_summary_v1.json`
- 当前最小裁决：
  - `beyond multi-session persistence card=2/2`
  - `not_beyond multi-session stability card=1/2`
- 当前含义：
  - continuation / stability 已继续推进到 multi-session branch cards
  - 当前仍只写 branch card，不升级成 `failed breakout`

## 下一步最顺动作

- 若继续沿同一条线推进，优先补：
  - `beyond third same-session persistence` observation
  - 或 `not_beyond third same-session stability` observation
