# A5 target_weight verified_with_degraded_risk 后续升级判断 多AI前情提要与裁决框架

更新时间：2026-07-17

## TASK

- 讨论：在 `target_weight` 已推进到
  `verified_with_degraded_risk__not_output_passed`、
  且 `covariance_model_id` 最小集成验证执行已通过后，
  当前是否足以继续推进到下一档正式升级判断结论。

## BACKGROUND

- 当前 `target_weight` 已完成：
  - `template-level smoke-run`
  - `real-input case validation smoke-run`
  - `actual generation execution`
  - `degraded_risk_handling` 充分性与稳健边界冻结
  - 边界验证清单
  - 主负责人书面验收
  - 升级判断重开回包吸收并正式裁为：
    - `verified_with_degraded_risk__not_output_passed`
- 当前 `covariance_model_id` 又继续完成：
  - ready 判断多AI回包吸收
  - 最小集成验证执行
  - 状态保持：
    - `ready_judgement_conditional__downstream_still_locked`

## KNOWN_CONSTRAINTS

- 当前仍是：
  - `degraded_risk_handling`
- 当前仍未允许写成：
  - `output_passed`
  - `正式优化器 ready`
  - `covariance_model_id ready`
  - `portfolio_tracking_error` / `adjusted_position_weight` 可自动升格
- 当前必须显式保留：
  - `covariance_model_id = ready_judgement_conditional__downstream_still_locked`

## DISCUSSION_SCOPE

- 本轮允许讨论：
  - 当前是否继续保持：
    - `verified_with_degraded_risk__not_output_passed`
  - 或是否值得推进到更高一档、
    但仍保留 `not_output_passed`
  - 如果仍不足，唯一最小剩余缺口是什么
- 本轮不要展开：
  - 是否已经 `output_passed`
  - 回测
  - 信号组合
  - 下游两段输出升格
  - 重开 `covariance_model_id` 的 ready 命名讨论

## FREE_GUESS_RANGE

- 允许你合理判断：
  - `covariance_model_id` 最小集成验证执行通过后，
    是否足以降低 `target_weight` 的上游不确定性
  - `verified_with_degraded_risk__not_output_passed`
    是否仍是最稳状态名
  - 若继续推进一档，最稳写法应长什么样
- 若缺证据必须写：
  - `NEED_EVIDENCE`

## EXPECTED_OUTPUT

- 请至少给出：
  - `保守 / 平衡 / 激进` 三种判断写法
- 对每种写法说明：
  - 适用条件
  - 优点
  - 风险
  - 是否会制造 ready 幻觉
  - `NEED_EVIDENCE`
- 最后给出你最推荐的方案与当前最小下一步
