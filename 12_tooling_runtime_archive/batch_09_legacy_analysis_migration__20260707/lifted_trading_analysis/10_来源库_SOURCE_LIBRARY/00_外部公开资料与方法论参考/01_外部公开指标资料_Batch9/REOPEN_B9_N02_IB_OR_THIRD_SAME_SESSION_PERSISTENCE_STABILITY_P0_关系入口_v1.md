# REOPEN_B9_N02 IB OR THIRD_SAME_SESSION_PERSISTENCE_STABILITY_P0 关系入口 v1

## 作用

- 把 `beyond multi-session persistence` 的成功样本继续推进到第三个同类 `session` 首 30 分钟的 `third same-session persistence` 观察。
- 把 `not_beyond multi-session stability` 的成功样本继续推进到第三个同类 `session` 首 30 分钟的 `third same-session stability` 观察。
- 当前只表达第三个同类 `session` 首 30 分钟相对前一日 `IB` 同侧边界的位置关系，不升级成 `failed breakout / retest / reject / day type`。

## 当前边界（写死）

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `n02_ib_or_beyond_multi_session_persistence_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_multi_session_stability_observation_p0_sample_v1.csv`
- 当前只新增：
  - `beyond third same-session persistence` 观察样本与摘要
  - `not_beyond third same-session stability` 观察样本与摘要

## 当前真值组成（v1）

- `entry_md`：`REOPEN_B9_N02_IB_OR_THIRD_SAME_SESSION_PERSISTENCE_STABILITY_P0_关系入口_v1.md`
- `parent_entry_md`：`REOPEN_B9_N02_IB_OR_MULTI_SESSION_BRANCH_CARDS_P0_关系入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_third_same_session_persistence_stability_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_third_same_session_persistence_stability_acceptance_v1.md`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_third_same_session_persistence_and_stability_p0_build_v1.py`
- `beyond_multi_session_observation_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_beyond_multi_session_persistence_observation_p0_sample_v1.csv`
- `not_beyond_multi_session_observation_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_not_beyond_multi_session_stability_observation_p0_sample_v1.csv`
- `bars_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_first_real_input_bars_v1.csv`
- `beyond_third_same_session_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_beyond_third_same_session_persistence_observation_p0_sample_v1.csv`
- `beyond_third_same_session_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_beyond_third_same_session_persistence_observation_p0_summary_v1.json`
- `not_beyond_third_same_session_csv`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_not_beyond_third_same_session_stability_observation_p0_sample_v1.csv`
- `not_beyond_third_same_session_summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_not_beyond_third_same_session_stability_observation_p0_summary_v1.json`

## 最小验收（关系开题级）

- `beyond third same-session persistence` 必须显式记录：
  - `third_next_session_first_30m_all_closes_beyond_prior_ib`
  - `third_next_session_first_30m_not_all_closes_beyond_prior_ib`
  - `missing_third_next_session_first_30m_data`
- `not_beyond third same-session stability` 必须显式记录：
  - `third_next_session_first_30m_all_closes_inside_prior_ib`
  - `third_next_session_first_30m_not_all_closes_inside_prior_ib`
  - `missing_third_next_session_first_30m_data`
- 所有输出都必须显式保留：
  - `defines_failed_breakout=false`

## 2026-07-04 fresh-run

- 运行入口：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_third_same_session_persistence_and_stability_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_beyond_third_same_session_persistence_observation_p0_sample_v1.csv`
  - `n02_ib_or_beyond_third_same_session_persistence_observation_p0_summary_v1.json`
  - `n02_ib_or_not_beyond_third_same_session_stability_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_third_same_session_stability_observation_p0_summary_v1.json`
- 关键统计：
  - `beyond_rows=2`
  - `beyond_status_counts={"third_next_session_first_30m_all_closes_beyond_prior_ib": 2}`
  - `not_beyond_rows=1`
  - `not_beyond_status_counts={"missing_third_next_session_first_30m_data": 1}`
- 当前裁决：
  - `beyond multi-session persistence 2/2` 里进入第三个同类 `session` 观察的 `2/2` 行，当前都保持了 `third same-session persistence`。
  - `not_beyond multi-session stability 1/2` 里进入第三个同类 `session` 观察的 `1/1` 行，当前缺第三个同类 `session` 数据。
  - 当前仍只做观察层，不升级成 `failed breakout`。

## 2026-07-04 third_same_session_branch_cards child 已开

- 已新增子入口：
  - `REOPEN_B9_N02_IB_OR_THIRD_SAME_SESSION_BRANCH_CARDS_P0_关系入口_v1.md`
- 已新增产物：
  - `n02_ib_or_beyond_third_same_session_persistence_card_v1.md`
  - `n02_ib_or_beyond_third_same_session_persistence_card_summary_v1.json`
  - `n02_ib_or_not_beyond_third_same_session_stability_card_v1.md`
  - `n02_ib_or_not_beyond_third_same_session_stability_card_summary_v1.json`
- 当前最小裁决：
  - `beyond third same-session persistence card=2/2`
  - `not_beyond third same-session stability card=missing 1/1`
- 当前含义：
  - third same-session observation 已继续固化成 branch card
  - 当前仍只写 branch card，不升级成 `failed breakout`

## 2026-07-04 third_same_session_terminal_summary child 已开

- 已新增子入口：
  - `REOPEN_B9_N02_IB_OR_THIRD_SAME_SESSION_TERMINAL_SUMMARY_P0_关系入口_v1.md`
- 已新增产物：
  - `n02_ib_or_third_same_session_terminal_summary_v1.md`
  - `n02_ib_or_third_same_session_terminal_summary_v1.json`
- 当前最小裁决：
  - `total_rows=3`
  - `resolved_rows=2`
  - `missing_rows=1`
- 当前含义：
  - third same-session observation 已继续收口到 terminal summary
  - 当前仍只写 observation/card/terminal summary，不升级成 `failed breakout`

## 下一步最顺动作

- 若继续沿同一条线推进，优先补：
  - 扩大 `EURUSD M1 london/new_york` 之外的样本覆盖
  - 或并行扩到其它 symbol / timeframe 的同口径验证
