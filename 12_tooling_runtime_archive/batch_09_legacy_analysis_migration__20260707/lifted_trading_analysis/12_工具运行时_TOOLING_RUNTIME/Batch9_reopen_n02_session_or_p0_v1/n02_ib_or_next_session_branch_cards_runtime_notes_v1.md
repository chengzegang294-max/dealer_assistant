# n02_ib_or_next_session_branch_cards_runtime_notes v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `beyond continuation card` 与 `not_beyond stability card` 的运行口径。

## 当前边界

- 不写回：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `n02_ib_or_beyond_continuation_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_pullback_stability_observation_p0_sample_v1.csv`
- 当前只落：
  - `n02_ib_or_beyond_continuation_card_v1.md`
  - `n02_ib_or_beyond_continuation_card_summary_v1.json`
  - `n02_ib_or_not_beyond_stability_card_v1.md`
  - `n02_ib_or_not_beyond_stability_card_summary_v1.json`
- 当前不推进：
  - `failed breakout`
  - `retest`
  - `reject`
  - `day type`

## 当前怎么用（v1）

- 输入：
  - `n02_ib_or_beyond_continuation_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_pullback_stability_observation_p0_sample_v1.csv`
- 生成脚本：
  - `n02_ib_or_beyond_continuation_and_not_beyond_stability_cards_p0_build_v1.py`
- 输出：
  - `n02_ib_or_beyond_continuation_card_v1.md`
  - `n02_ib_or_beyond_continuation_card_summary_v1.json`
  - `n02_ib_or_not_beyond_stability_card_v1.md`
  - `n02_ib_or_not_beyond_stability_card_summary_v1.json`
- 当前字段只表达：
  - `beyond continuation` 的 branch card
  - `not_beyond stability` 的 branch card

## 推荐复现命令

- `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_beyond_continuation_and_not_beyond_stability_cards_p0_build_v1.py`

## 2026-07-04 fresh-run 结果

- 运行入口：
  - `python n02_ib_or_beyond_continuation_and_not_beyond_stability_cards_p0_build_v1.py`
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
- 当前结论：
  - `beyond continuation` 已固定成独立说明卡。
  - `not_beyond stability` 已固定成独立说明卡。
  - 当前仍只写 branch card，不写 `failed breakout` 定义。

## 2026-07-04 multi_session_persistence_stability child fresh-run

- 运行入口：
  - `python n02_ib_or_multi_session_persistence_and_stability_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_beyond_multi_session_persistence_observation_p0_sample_v1.csv`
  - `n02_ib_or_beyond_multi_session_persistence_observation_p0_summary_v1.json`
  - `n02_ib_or_not_beyond_multi_session_stability_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_multi_session_stability_observation_p0_summary_v1.json`
- 关键统计：
  - `beyond_rows=2`
  - `not_beyond_rows=2`
  - `beyond_all_closes_beyond_prior_ib_rows=2`
  - `not_beyond_all_closes_inside_prior_ib_rows=1`
- 当前结论：
  - 主线已从 next-session 两张卡继续推进到 multi-session observation
  - 当前仍只写 observation，不写 `failed breakout` 定义

## 2026-07-04 multi_session_branch_cards child fresh-run

- 运行入口：
  - `python n02_ib_or_multi_session_persistence_and_stability_cards_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_beyond_multi_session_persistence_card_v1.md`
  - `n02_ib_or_beyond_multi_session_persistence_card_summary_v1.json`
  - `n02_ib_or_not_beyond_multi_session_stability_card_v1.md`
  - `n02_ib_or_not_beyond_multi_session_stability_card_summary_v1.json`
- 关键统计：
  - `beyond_rows=2`
  - `not_beyond_rows=2`
  - `beyond_all_closes_beyond_prior_ib_rows=2`
  - `not_beyond_all_closes_inside_prior_ib_rows=1`
- 当前结论：
  - 主线已从 multi-session observation 继续推进到 multi-session branch cards
  - 当前仍只写 card，不写 `failed breakout` 定义

## 当前最顺动作

- 若继续推进，优先补：
  - `beyond third same-session persistence` observation
  - 或 `not_beyond third same-session stability` observation
