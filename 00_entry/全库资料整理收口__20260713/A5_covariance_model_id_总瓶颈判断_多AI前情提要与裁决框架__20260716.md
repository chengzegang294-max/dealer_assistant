# A5 covariance_model_id 总瓶颈判断 多AI前情提要与裁决框架

更新时间：2026-07-16

## TASK

- 讨论：在 `target_weight / portfolio_tracking_error / adjusted_position_weight` 三段输出都已分别推进到 `verified` 或 `frozen` 的 not_output_passed 状态后，`covariance_model_id` 是否已足以进入下一档总瓶颈判断结论。

## BACKGROUND

- 当前 `covariance_model_id` 已推进到：
  - `future_only_but_under_judgement`
- 已完成：
  - `A5_covariance_model_id_实现前口径判断页__20260716.md`
- 当前下游状态为：
  - `target_weight = verified_with_degraded_risk__not_output_passed`
  - `portfolio_tracking_error = pass_conditions_frozen__not_output_passed`
  - `adjusted_position_weight = pass_conditions_frozen__not_output_passed`

## KNOWN_CONSTRAINTS

- 当前仍不能误写成：
  - `covariance_model_id ready`
  - `协方差模型已闭合`
  - `正式风险模型已完成`
- 当前仍未具备：
  - 协方差矩阵本体实跑
  - 唯一实现模型定稿

## DISCUSSION_SCOPE

- 本轮允许讨论：
  - 当前是否足以把总瓶颈判断从 `future_only_but_under_judgement` 继续推进一档
  - 如果仍不足，唯一剩余缺口是什么
  - 如果足够，当前最稳正式结论应写到哪
- 本轮不要展开：
  - 是否已经 ready
  - runtime 实现
  - 回测
  - G6 粒度扩展

## FREE_GUESS_RANGE

- 允许你合理判断：
  - 三段输出已前推一档这件事，是否足以反向压实 `covariance_model_id` 的候选模型家族冻结
  - 当前更稳的命名应偏保守、平衡还是激进
- 若缺证据必须写：
  - `NEED_EVIDENCE`

## EXPECTED_OUTPUT

- 请至少给出：
  - `保守 / 平衡 / 激进` 三种判断写法
- 对每种写法说明：
  - 适用条件
  - 好处
  - 风险
  - 是否会制造 ready 幻觉
- 最后给出你最推荐的方案与当前最小下一步
