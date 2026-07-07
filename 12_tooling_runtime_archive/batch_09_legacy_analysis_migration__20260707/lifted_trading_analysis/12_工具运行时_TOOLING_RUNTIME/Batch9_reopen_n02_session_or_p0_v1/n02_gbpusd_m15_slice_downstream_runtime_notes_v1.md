# n02_gbpusd_m15_slice_downstream_runtime_notes v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是把 `GBPUSD/M15 historical recovered` 的下游链收紧成 `slice runtime -> terminal summary + or_break_only same-day session close + beyond_or next-session continuation + beyond_or multi-session persistence` 的可复现闭环。

## 当前边界

- 当前不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - 任意 `failed breakout / retest / reject / day type` 定义
- 当前显式做了：
  - 从 mixed candidate runtime 切出 `GBPUSD/M15 slice`
  - 基于 slice 重跑 `IB object -> relation -> first_break_relative -> break_bar_evidence -> cross split -> post_cross -> next session -> multi-session -> third same-session -> terminal summary`
  - 基于 `or_break_only` 分支补跑 `same-day return_inside_or / session_close_beyond_or / session_close_not_beyond_or`
  - 基于 `or_break_only session_close_beyond_or` 分支补跑 `next same-session first 30m continuation`
  - 基于 `or_break_only beyond_next_session all-closes` 分支补跑 second next-session persistence
- 当前显式不把：
  - `no_break`
  - 缺第二/第三同类 `session` 数据
  混入 `confirmed cross`

## 当前怎么跑（v1）

- slice 生成器：
  - `n02_gbpusd_m15_candidate_slice_build_v1.py`
- 下游汇总生成器：
  - `n02_gbpusd_m15_slice_downstream_summary_build_v1.py`
- 关键已有脚本：
  - `n02_ib_object_p0_build_v1.py`
  - `n02_ib_or_relation_p0_build_v1.py`
  - `n02_ib_or_first_break_relative_p0_build_v1.py`
  - `n02_ib_or_break_bar_evidence_p0_build_v1.py`
  - `n02_ib_or_cross_outcome_split_p0_build_v1.py`
  - `n02_ib_or_post_cross_path_and_or_break_only_card_p0_build_v1.py`
  - `n02_ib_or_or_break_only_same_day_session_close_split_p0_build_v1.py`
  - `n02_ib_or_or_break_only_session_close_beyond_or_next_session_continuation_p0_build_v1.py`
  - `n02_ib_or_or_break_only_session_close_beyond_or_multi_session_persistence_p0_build_v1.py`
  - `n02_ib_or_return_inside_and_session_close_split_p0_build_v1.py`
  - `n02_ib_or_session_close_beyond_and_not_beyond_cards_p0_build_v1.py`
  - `n02_ib_or_beyond_continuation_and_not_beyond_stability_p0_build_v1.py`
  - `n02_ib_or_multi_session_persistence_and_stability_p0_build_v1.py`
  - `n02_ib_or_multi_session_persistence_and_stability_cards_p0_build_v1.py`
  - `n02_ib_or_third_same_session_persistence_and_stability_p0_build_v1.py`
  - `n02_ib_or_third_same_session_persistence_and_stability_cards_p0_build_v1.py`
  - `n02_ib_or_third_same_session_terminal_summary_build_v1.py`

## 2026-07-06 fresh-run 结果

- slice runtime：
  - `or_slice_rows=457`
  - `or_defined_rows=396`
  - `ib_slice_rows=457`
  - `ib_defined_rows=396`
- relation / relative：
  - `relation_rows=396`
  - `first_break_relative_case_counts={"no_break": 23, "or_break_with_ib_same_side_gap_remaining": 325, "shared_edge_break": 48}`
- break / cross：
  - `break_bar_evidence_status_counts={"ib_same_side_cross_confirmed": 48, "no_break_in_upstream_relation": 23, "or_break_bar_found_but_ib_same_side_not_crossed": 325}`
  - `confirmed_cross_rows=48`
  - `or_break_only_rows=325`
  - `no_break_rows=23`
- post-cross / next session：
  - `post_cross_return_inside_ib_observed_same_day_rows=45`
  - `post_cross_session_close_beyond_ib_rows=27`
  - `next_beyond_rows=27`
  - `next_not_beyond_rows=21`
- multi / third same-session：
  - `multi_beyond_rows=13`
  - `multi_not_beyond_rows=14`
  - `third_beyond_rows=2`
  - `third_not_beyond_rows=9`
- terminal：
  - `terminal_total_rows=11`
  - `terminal_resolved_rows=8`
  - `terminal_missing_rows=3`
- or_break_only same-day session close：
  - `or_break_only_return_inside_or_observed_same_day_rows=312`
  - `or_break_only_session_close_beyond_or_rows=168`
  - `or_break_only_session_close_not_beyond_or_rows=157`
- or_break_only beyond_or next-session continuation：
  - `or_break_only_beyond_next_session_rows=168`
  - `or_break_only_beyond_next_session_all_closes_beyond_prior_or_rows=105`
  - `or_break_only_beyond_next_session_not_all_closes_beyond_prior_or_rows=23`
  - `or_break_only_beyond_next_session_missing_rows=40`
- or_break_only beyond_or multi-session persistence：
  - `or_break_only_beyond_multi_session_rows=105`
  - `or_break_only_beyond_multi_session_all_closes_beyond_prior_or_rows=57`
  - `or_break_only_beyond_multi_session_not_all_closes_beyond_prior_or_rows=21`
  - `or_break_only_beyond_multi_session_missing_rows=27`
  - `gate_status=gbpusd_m15_slice_downstream_plus_or_break_only_beyond_multi_session_persistence_done_without_failed_breakout`

## 当前结论

- `GBPUSD/M15 recovered` 的下游链已能在不污染主 runtime 的前提下走到 terminal summary，并把 `or_break_only` 分支推进到 same-day session close、next-session continuation，以及对 next-session all-closes 子集补到 multi-session persistence。
- `no_break` 与缺失后续 session 数据已被显式保留，不再伪装成 break / cross 成功。
- 当前链路固定停在：
  - `gbpusd_m15_slice_downstream_plus_or_break_only_beyond_multi_session_persistence_done_without_failed_breakout`

## provenance 说明

- 这层所有下游产物都基于 `historical_recovered` 的 `GBPUSD/M15` bars 与 slice runtime，而不是 `TMGM terminal fresh export`。
- `n02_ib_or_break_bar_evidence_p0_build_v1.py` 已补 `no_break_in_upstream_relation` 分支，`n02_ib_or_cross_outcome_split_p0_build_v1.py` 已补 `no_break_rows` 分桶，避免把 `no_break` 样本误并入 `or_break_only`。
