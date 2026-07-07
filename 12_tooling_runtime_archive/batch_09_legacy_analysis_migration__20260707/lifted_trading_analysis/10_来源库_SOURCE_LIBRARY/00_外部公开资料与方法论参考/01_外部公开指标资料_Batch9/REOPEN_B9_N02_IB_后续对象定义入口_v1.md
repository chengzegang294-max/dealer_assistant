# REOPEN_B9_N02 IB 后续对象定义入口 v1

## 作用

- 把 `IB` 从 `GROUP_06 -> N02` 的“对象候选清单”继续推进到更明确的后续对象入口。
- 当前目标不是把 `IB` 塞进 `N02 P0`，而是先固定：
  - 进入条件
  - 最小输入
  - 最小输出
  - 与现有 `N02 P0` 的依赖关系
  - 后续验收边界

## 当前定位

- 层级：
  - `N02` 后续对象层
- 当前角色：
  - `next_object_entry`
- 不是：
  - 当前 `N02 P0` 字段
  - 当前已真实实现对象
  - 当前硬门控

## 为什么先从 IB 开

- `IB` 是 `GROUP_06` 里最贴近当前 `N02 sessions / open-range / time-window context` 的对象。
- 它与当前已做的 `OR` 有天然连续性：
  - 都依赖 session 边界
  - 都依赖分钟级或可重建的 session 内价格区间
  - 都属于“先做上下文对象，再谈后续行为标签”
- 相比 `VA / POC / Day Type`：
  - `IB` 的输入更轻
  - 工程歧义更低
  - 更适合成为 `N02` 的第一个对象入口

## 上游依赖

- 来自当前 `N02 P0` 的已具备前置：
  - `symbol`
  - `timeframe`
  - `bar_time_utc`
  - `session_id`
  - `session_timezone`
  - `session_local_date`
  - `session_start_utc`
  - `session_end_utc`
  - `opening_range_start_utc`
  - `opening_range_end_utc`
- 当前最重要的依赖判断：
  - `IB` 不应脱离 session binding 单独定义
  - `IB` 应建立在已冻结的 `session_id + session_timezone + local_date` 之上

## 最小输入

- 分钟级或可重建分钟级的 session 内 OHLCV
- `session_id`
- `session_timezone`
- `session_local_date`
- `ib_window_minutes`
  - v1 建议先固定为 `60`
- 可选但推荐：
  - `opening_range_minutes`
  - 用于后续比较 `OR vs IB`

## 最小输出

- `ib_start_utc`
- `ib_end_utc`
- `ib_high`
- `ib_low`
- `ib_range`
- `ib_mid`

## 建议的派生输出（先占位，不进 v1 最小合同）

- `ib_position_close`
  - 收盘位于 `IB` 的相对位置
- `ib_extension_multiple`
  - 当日总波幅相对 `IB range` 的倍数
- `ib_break_state`
  - `inside / above / below / two_sided`
- `ib_retest_flag`
  - 是否发生回测
- `ib_reject_flag`
  - 是否发生回测后拒绝

## 与 OR 的关系

- 当前更稳的口径：
  - `OR` 继续留在 `N02 P0`
  - `IB` 作为 `N02` 后续对象层
- 二者关系不写成：
  - `OR == IB`
- 当前更合适的写法是：
  - `OR` 是当前 P0 已落地的 session/opening-range 上下文
  - `IB` 是下一个自然扩展对象
  - 后续可讨论：
    - `OR inside IB`
    - `IB vs OR width`
    - `first break relative to OR/IB`
  - 但这些不提前进入当前 P0

## 2026-07-03 关系层推进更新

- `IB_OBJECT_P0` 之后的第一条关系子链已新开：
  - `REOPEN_B9_N02_IB_OR_RELATION_P0_关系入口_v1.md`
- 当前已完成的最小关系裁决：
  - `relation_rows_written=138`
  - `missing_or_match_rows=0`
  - `or_inside_ib_ratio=1.0`
- 当前含义：
  - `OR inside IB` 已从“可讨论”升级为“当前样本可复现观测”
  - 但仍不升级为策略门控或 `acceptance`

## 2026-07-03 first_break relative 更新

- `first_break relative to IB/OR` 已继续新开：
  - `REOPEN_B9_N02_IB_OR_FIRST_BREAK_RELATIVE_P0_关系入口_v1.md`
- 当前最小裁决：
  - `shared_edge_break_rows=14`
  - `gap_remaining_rows=124`
  - `requires_break_price_rows=124`
- 当前含义：
  - 只有 shared-edge 行可确认 `OR 首破 == IB 同侧首破`
  - 其余大多数行仍需 `break price`，不允许假确认

## 2026-07-03 break_bar evidence 更新

- 已继续新开：
  - `REOPEN_B9_N02_IB_OR_BREAK_BAR_EVIDENCE_P0_关系入口_v1.md`
- 当前最小裁决：
  - `ib_same_side_cross_confirmed_rows=15`
  - `ib_same_side_not_crossed_rows=123`
  - `direction_mode_mismatch_rows=1`
- 当前含义：
  - `break price` 缺口已用 bar-level 证据补齐
  - 下一步应转向 confirmed cross / not crossed 的结果分流，而不是继续停在“还缺价位”

## 2026-07-03 cross outcome split 更新

- 已继续新开：
  - `REOPEN_B9_N02_IB_OR_CROSS_OUTCOME_SPLIT_P0_关系入口_v1.md`
- 当前最小裁决：
  - `confirmed_cross_rows=15`
  - `or_break_only_rows=123`
  - `outcome_shell_rows=15`
- 当前含义：
  - `confirmed cross` 与 `OR break only` 已完成分桶
  - `confirmed cross` 已有独立 `outcome_shell`，但仍未进入 `failed breakout`

## 2026-07-03 post_cross_path 更新

- 已继续新开：
  - `REOPEN_B9_N02_IB_OR_POST_CROSS_PATH_P0_关系入口_v1.md`
- 当前最小裁决：
  - `return_inside_ib_observed_same_day_rows=15`
  - `session_close_beyond_ib_rows=9`
  - `or_break_only_rows=123`
- 当前含义：
  - `confirmed_cross` 已补到同日本地日内观察层
  - `OR break only` 已补到独立说明卡
  - 当前仍只做 observation / card，不进入 `failed breakout`

## 2026-07-03 return_inside / session_close split 更新

- 已继续新开：
  - `REOPEN_B9_N02_IB_OR_RETURN_INSIDE_AND_SESSION_CLOSE_SPLIT_P0_关系入口_v1.md`
- 当前最小裁决：
  - `return_inside_rows=15`
  - `session_close_beyond_ib_rows=9`
  - `session_close_not_beyond_ib_rows=6`
- 当前含义：
  - `return_inside` 已固定成独立说明卡
  - `session_close` 已完成 beyond / not_beyond 二次分桶
  - 当前仍只做 observation / split，不进入 `failed breakout`

## 2026-07-03 session_close branch cards 更新

- 已继续新开：
  - `REOPEN_B9_N02_IB_OR_SESSION_CLOSE_BRANCH_CARDS_P0_关系入口_v1.md`
- 当前最小裁决：
  - `session_close_beyond_ib_rows=9`
  - `session_close_not_beyond_ib_rows=6`
- 当前含义：
  - `session_close_beyond_ib` 已固定成独立说明卡
  - `session_close_not_beyond_ib` 已固定成回落分支说明卡
  - 当前仍只做 branch card，不进入 `failed breakout`

## 2026-07-03 next session continuation / stability 更新

- 已继续新开：
  - `REOPEN_B9_N02_IB_OR_NEXT_SESSION_CONTINUATION_STABILITY_P0_关系入口_v1.md`
- 当前最小裁决：
  - `beyond_all_closes_beyond_prior_ib=2/9`
  - `not_beyond_all_closes_inside_prior_ib=2/6`
  - `beyond_missing=2/9`
  - `not_beyond_missing=2/6`
- 当前含义：
  - `session_close_beyond_ib` 已推进到下一同类 session 首 30 分钟 continuation 观察
  - `session_close_not_beyond_ib` 已推进到下一同类 session 首 30 分钟 pullback stability 观察
  - 当前仍只做 observation，不进入 `failed breakout`

## 2026-07-04 next session branch cards 更新

- 已继续新开：
  - `REOPEN_B9_N02_IB_OR_NEXT_SESSION_BRANCH_CARDS_P0_关系入口_v1.md`
- 当前最小裁决：
  - `beyond continuation 2/9` 已固定成独立说明卡
  - `not_beyond stability 2/6` 已固定成独立说明卡
- 当前含义：
  - next-session continuation / stability 已从 observation 升级到 branch card
  - 当前仍只做 branch card，不进入 `failed breakout`

## 2026-07-04 multi-session persistence / stability 更新

- 已继续新开：
  - `REOPEN_B9_N02_IB_OR_MULTI_SESSION_PERSISTENCE_STABILITY_P0_关系入口_v1.md`
- 当前最小裁决：
  - `beyond_multi_session_persistence_rows=2`
  - `beyond_multi_session_persistence_all_closes_beyond_prior_ib=2`
  - `not_beyond_multi_session_stability_rows=2`
  - `not_beyond_multi_session_stability_all_closes_inside_prior_ib=1`
- 当前含义：
  - `beyond continuation` 已继续推进到第二个同类 `session` 的 persistence observation
  - `not_beyond stability` 已继续推进到第二个同类 `session` 的 stability observation
  - 当前仍只做 observation，不进入 `failed breakout`

## 2026-07-04 multi-session branch cards 更新

- 已继续新开：
  - `REOPEN_B9_N02_IB_OR_MULTI_SESSION_BRANCH_CARDS_P0_关系入口_v1.md`
- 当前最小裁决：
  - `beyond_multi_session_persistence_card_rows=2`
  - `beyond_multi_session_persistence_card_all_closes_beyond_prior_ib=2`
  - `not_beyond_multi_session_stability_card_rows=2`
  - `not_beyond_multi_session_stability_card_all_closes_inside_prior_ib=1`
- 当前含义：
  - `beyond multi-session persistence` 已固定成独立 branch card
  - `not_beyond multi-session stability` 已固定成独立 branch card
  - 当前仍只做 branch card，不进入 `failed breakout`

## 2026-07-04 third same-session persistence / stability 更新

- 已继续新开：
  - `REOPEN_B9_N02_IB_OR_THIRD_SAME_SESSION_PERSISTENCE_STABILITY_P0_关系入口_v1.md`
- 当前最小裁决：
  - `beyond_third_same_session_persistence_rows=2`
  - `beyond_third_same_session_persistence_all_closes_beyond_prior_ib=2`
  - `not_beyond_third_same_session_stability_rows=1`
  - `not_beyond_third_same_session_stability_missing_rows=1`
- 当前含义：
  - `beyond third same-session persistence` 已继续推进到 observation
  - `not_beyond third same-session stability` 已继续推进到 observation，并明确记录缺数据
  - 当前仍只做 observation，不进入 `failed breakout`

## 最小验收定义

- 有一份对象合同草案：
  - 输入/输出/窗口定义明确
- 有一份可复现 proof-of-mapping：
  - 至少 1 个 `session_id`
  - 至少 1 个 `symbol`
  - 至少 1 个分钟级样本
- 有一份当前角色裁决：
  - `DIAG_ONLY_OBJECT_CANDIDATE`
  - 或更明确的 `next_object_entry`
- 不得提前宣称：
  - `IB acceptance`
  - `IB failed breakout`
  - `day type`
  - `IB 已真实接入主线`

## 当前 gaps

- `IB` 的具体窗口是否对所有 session 一律固定为首 `60` 分钟，当前仍应先保持保守写法。
- 当前还没有把 `IB` 与 `OR first_break_mode` 做联合验证。
- 当前不应把 `IB retest / reject` 直接提升为规则或门控。

## 是否值得新开 REOPEN_B9_N02_IB_OBJECT_P0（门槛判断）

- 已具备：
  - `IB proof-of-mapping`（三件套 + 可复现输出）
  - `IB contract notes`
  - `IB runtime notes`（写死“不污染 N02 P0”）
- 仍缺的最小两项（补齐即可开题）：
  - `IB runtime CSV contract`（独立于 `N02 P0`）：`n02_ib_fields_runtime_v1.csv`
  - `IB append 脚本`：`n02_ib_runtime_append_from_proof_v1.py`

## 当前裁决（更新）

- 门槛已满足：可以新开 `REOPEN_B9_N02_IB_OBJECT_P0` 作为 reopen 子项入口。
- 仍保持边界：
  - `IB` 不写回 `n02_p0_fields_runtime_v2.csv`
  - `IB acceptance / failed breakout / day type` 不进入本轮开题

## 与来源的衔接

- 来源锚点：
  - `01_Kimi拆书待入库\GROUP_06_to_N02_对象候选清单_v1.md`
- 当前承接方式：
  - 从“候选对象清单”升级到“对象定义入口”
- 后续若继续推进：
  - `IB proof-of-mapping`
  - `IB contract notes`
  - `IB runtime notes`
  - `IB runtime CSV contract + append`
  - 再进入 `REOPEN_B9_N02_IB_OBJECT_P0`

## 当前裁决

- `IB` 已不再只是 `GROUP_06 -> N02` 的泛候选。
- 当前应把它固定为：
  - `N02` 后续对象层第一入口
  - `OR` 之后最自然的对象扩展位
- 同时继续保持边界：
  - 不反向污染当前 `N02 P0`
  - 不提前宣称实现完成

## 下一步

- 若继续推进同一条线，优先顺序应为：
  - 先补 `IB proof-of-mapping`（只做对象映射证据，不写入 `n02_p0_fields_runtime_v2.csv`）
  - 再补 `IB contract notes`
  - 再补 `IB runtime notes`
  - 再补 `IB runtime CSV contract + append`
  - 再新开 `REOPEN_B9_N02_IB_OBJECT_P0`
- 在此之前，`VA / POC / Day Type` 继续保持在 `IB` 之后，不抢先开题。

## 如何用（v1）

- 目的：把 `IB window=60min` 的最小输出在真实 bars 样本上跑通，形成可复现的 proof 产物。
- 使用方式：
  - 脚本：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_ib_proof_of_mapping_v1.py`
  - 输入：
    - 主样本：`...real_input_samples\n02_first_real_input_bars_v1.csv`
    - 可选补样本（按 session 定向补覆盖）：`n02_dst_london_spring_20260327_20260331_bars.csv`、`n02_dst_newyork_spring_20260306_20260310_bars.csv`
  - 配置：`...real_input_samples\n02_or_proof_config_v1.json`（复用 session timezone + open_local）
  - 输出：`...real_input_samples\n02_ib_proof_of_mapping_output_v1.csv`
  - 推荐命令（按 session 定向采样 + 跳过边界残缺日）：
    - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_ib_proof_of_mapping_v1.py --session-input london=n02_first_real_input_bars_v1.csv --session-input london=n02_dst_london_spring_20260327_20260331_bars.csv --session-input new_york=n02_first_real_input_bars_v1.csv --session-input new_york=n02_dst_newyork_spring_20260306_20260310_bars.csv --symbol EURUSD --timeframe M1 --skip-partial-days`
  - 合同说明：`n02_ib_contract_notes_v1.md`
  - runtime notes：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_runtime_notes_v1.md`
  - runtime CSV：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_fields_runtime_v1.csv`
  - runtime append：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_runtime_append_from_proof_v1.py`
- 验收口径（最小）：
  - 输出至少包含 `london/new_york` 两个 session 的 1 个本地日期行
  - 每行都能给出：`ib_start_utc/ib_end_utc/ib_high/ib_low/ib_range/ib_mid`
  - 仍保持边界：这份 proof 不反向污染当前 `N02 P0` 合约与 runtime 主 CSV
