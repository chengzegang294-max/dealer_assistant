# n02_ib_or_multi_session_persistence_stability_runtime_notes v1

## 角色

- 本文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `beyond multi-session persistence` 与 `not_beyond multi-session stability` 的第二个同类 `session` 首 30 分钟观察口径。

## 当前边界

- 不写回：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `n02_ib_or_beyond_continuation_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_pullback_stability_observation_p0_sample_v1.csv`
- 当前只落：
  - `n02_ib_or_beyond_multi_session_persistence_observation_p0_sample_v1.csv`
  - `n02_ib_or_beyond_multi_session_persistence_observation_p0_summary_v1.json`
  - `n02_ib_or_not_beyond_multi_session_stability_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_multi_session_stability_observation_p0_summary_v1.json`
- 当前不推进：
  - `failed breakout`
  - `retest`
  - `reject`
  - `day type`

## 当前怎么用（v1）

- 输入：
  - `n02_ib_or_beyond_continuation_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_pullback_stability_observation_p0_sample_v1.csv`
  - `real_input_samples\n02_first_real_input_bars_v1.csv`
  - `real_input_samples\n02_or_proof_config_v1.json`
- 生成脚本：
  - `n02_ib_or_multi_session_persistence_and_stability_p0_build_v1.py`
- 输出：
  - `n02_ib_or_beyond_multi_session_persistence_observation_p0_sample_v1.csv`
  - `n02_ib_or_beyond_multi_session_persistence_observation_p0_summary_v1.json`
  - `n02_ib_or_not_beyond_multi_session_stability_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_multi_session_stability_observation_p0_summary_v1.json`
- 当前字段只表达：
  - 第二个同类 `session` 首 30 分钟是否整体仍在前一日 `IB` 外侧
  - 第二个同类 `session` 首 30 分钟是否整体仍在前一日 `IB` 内侧
  - 当前是否缺第二个同类 `session` 数据

## 推荐复现命令

- `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_or_multi_session_persistence_and_stability_p0_build_v1.py`

## 2026-07-04 fresh-run 结果

- 运行入口：
  - `python n02_ib_or_multi_session_persistence_and_stability_p0_build_v1.py`
- fresh-run 产物：
  - `n02_ib_or_beyond_multi_session_persistence_observation_p0_sample_v1.csv`
  - `n02_ib_or_beyond_multi_session_persistence_observation_p0_summary_v1.json`
  - `n02_ib_or_not_beyond_multi_session_stability_observation_p0_sample_v1.csv`
  - `n02_ib_or_not_beyond_multi_session_stability_observation_p0_summary_v1.json`
- 关键统计：
  - `beyond_rows=2`
  - `beyond_all_closes_beyond_prior_ib_rows=2`
  - `beyond_not_all_closes_beyond_prior_ib_rows=0`
  - `beyond_missing_rows=0`
  - `not_beyond_rows=2`
  - `not_beyond_all_closes_inside_prior_ib_rows=1`
  - `not_beyond_not_all_closes_inside_prior_ib_rows=1`
  - `not_beyond_missing_rows=0`
- 当前结论：
  - `beyond continuation 2/9` 进入第二个同类 `session` 后，当前 `2/2` 行继续保持外侧。
  - `not_beyond stability 2/6` 进入第二个同类 `session` 后，当前 `1/2` 行保持内侧，`1/2` 行已失稳。
  - 当前仍只写 observation，不写 `failed breakout` 定义。

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
  - 主线已从 multi-session observation 推进到 multi-session branch cards
  - 当前仍只写 card，不写 `failed breakout` 定义

## 当前最顺动作

- 若继续推进，优先补：
  - `beyond third same-session persistence` observation
  - `not_beyond third same-session stability` observation
