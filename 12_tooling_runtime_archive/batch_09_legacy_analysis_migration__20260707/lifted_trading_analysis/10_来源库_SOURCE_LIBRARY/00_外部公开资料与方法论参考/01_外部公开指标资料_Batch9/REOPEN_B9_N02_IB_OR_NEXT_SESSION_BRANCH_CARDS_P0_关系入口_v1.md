# REOPEN_B9_N02 IB OR NEXT_SESSION_BRANCH_CARDS_P0 关系入口 v1

## 作用

- 把 `beyond continuation` 与 `not_beyond stability` 都固定成独立 branch card。
- 当前只表达下一同类 `session` 首 30 分钟相对前一日 `IB` 的两张说明卡，不升级成 `failed breakout / retest / reject / day type`。

## 当前边界（写死）

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `n02_ib_or_beyond_continuation_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_pullback_stability_observation_p0_sample_v1.csv`
- 当前只新增：
  - `beyond continuation card`
  - `not_beyond stability card`
  - 两张卡各自的 summary

## 当前真值组成（v1）

- `entry_md`：`REOPEN_B9_N02_IB_OR_NEXT_SESSION_BRANCH_CARDS_P0_关系入口_v1.md`
- `parent_entry_md`：`REOPEN_B9_N02_IB_OR_NEXT_SESSION_CONTINUATION_STABILITY_P0_关系入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_next_session_branch_cards_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_next_session_branch_cards_acceptance_v1.md`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_beyond_continuation_and_not_beyond_stability_cards_p0_build_v1.py`
- `beyond_continuation_observation_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_beyond_continuation_observation_p0_sample_v1.csv`
- `not_beyond_stability_observation_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_not_beyond_pullback_stability_observation_p0_sample_v1.csv`
- `beyond_continuation_card_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_beyond_continuation_card_v1.md`
- `beyond_continuation_card_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_beyond_continuation_card_summary_v1.json`
- `not_beyond_stability_card_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_not_beyond_stability_card_v1.md`
- `not_beyond_stability_card_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_not_beyond_stability_card_summary_v1.json`

## 最小验收（关系开题级）

- `beyond continuation card` 必须显式记录：
  - `status_counts`
  - `direction_counts`
  - `mode_counts`
  - `next_session_first_30m_bar_count_30_rows`
- `not_beyond stability card` 必须显式记录：
  - `status_counts`
  - `direction_counts`
  - `mode_counts`
  - `next_session_first_30m_bar_count_30_rows`
- 所有输出必须显式保留：
  - `defines_failed_breakout=false`

## 2026-07-04 fresh-run

- 运行入口：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_beyond_continuation_and_not_beyond_stability_cards_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_beyond_continuation_card_v1.md`
  - `n02_ib_or_beyond_continuation_card_summary_v1.json`
  - `n02_ib_or_not_beyond_stability_card_v1.md`
  - `n02_ib_or_not_beyond_stability_card_summary_v1.json`
- 关键统计：
  - `beyond_rows=9`
  - `beyond_status_counts={"missing_next_session_first_30m_data": 2, "next_session_first_30m_all_closes_beyond_prior_ib": 2, "next_session_first_30m_not_all_closes_beyond_prior_ib": 5}`
  - `not_beyond_rows=6`
  - `not_beyond_status_counts={"missing_next_session_first_30m_data": 2, "next_session_first_30m_all_closes_inside_prior_ib": 2, "next_session_first_30m_not_all_closes_inside_prior_ib": 2}`
- 当前裁决：
  - `beyond continuation card` 已固定成独立说明卡。
  - `not_beyond stability card` 已固定成独立说明卡。
  - 当前仍只写 branch card，不升级成 `failed breakout`。

## 2026-07-04 multi_session_persistence_stability child 已开

- 已新增子入口：
  - `REOPEN_B9_N02_IB_OR_MULTI_SESSION_PERSISTENCE_STABILITY_P0_关系入口_v1.md`
- 已新增产物：
  - `n02_ib_or_beyond_multi_session_persistence_observation_p0_sample_v1.csv`
  - `n02_ib_or_beyond_multi_session_persistence_observation_p0_summary_v1.json`
  - `n02_ib_or_not_beyond_multi_session_stability_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_multi_session_stability_observation_p0_summary_v1.json`
- 当前最小裁决：
  - `beyond multi-session persistence` 当前为 `2/2`
  - `not_beyond multi-session stability` 当前为 `1/2`
- 当前含义：
  - next-session 两张卡已继续推进到第二个同类 `session` 首 30 分钟观察层
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
  - `beyond multi-session persistence card` 当前为 `2/2`
  - `not_beyond multi-session stability card` 当前为 `1/2`
- 当前含义：
  - multi-session observation 已升级成独立 branch card
  - 当前仍只写 branch card，不升级成 `failed breakout`

## 下一步最顺动作

- 若继续沿同一条线推进，优先补：
  - `beyond third same-session persistence` observation
  - 或 `not_beyond third same-session stability` observation
