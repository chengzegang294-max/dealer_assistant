# A5 portfolio_tracking_error frozen 后续升级判断 多AI前情提要与裁决框架

更新时间：2026-07-17

## TASK

- 讨论：在 `portfolio_tracking_error` 已推进到
  `pass_conditions_frozen__not_output_passed`
  且上游 `target_weight` 已推进到
  `verified_with_degraded_risk__upstream_min_integration_verified__not_output_passed`
  后，
  当前是否已足以让 `portfolio_tracking_error` 再推进一档正式升级判断结论。

## BACKGROUND

- 当前 `portfolio_tracking_error` 已完成：
  - `benchmark` 风险输出最小正式口径页
  - `covariance_model_id` 最小输入层页
  - `降级风险口径可审计样例页`
  - 单点升级判断回包吸收并正式裁为：
    - `pass_conditions_frozen__not_output_passed`
- 当前 `target_weight` 已继续正式推进到：
  - `verified_with_degraded_risk__upstream_min_integration_verified__not_output_passed`
- 当前 `covariance_model_id` 仍保持：
  - `ready_judgement_conditional__downstream_still_locked`
- 上一轮混合回包存在：
  - 旧题
  - 串题
  - 泛化票
  - 不答题票

## KNOWN_CONSTRAINTS

- 当前仍是：
  - `risk_mode = degraded_risk_handling`
- 当前仍不能写成：
  - `output_passed`
  - `benchmark 风险输出 ready`
  - `covariance_model_id ready`
  - `adjusted_position_weight` 自动解锁
- 当前必须显式保留：
  - `covariance_model_id = ready_judgement_conditional__downstream_still_locked`

## DISCUSSION_SCOPE

- 本轮允许讨论：
  - `portfolio_tracking_error` 是否继续维持：
    - `pass_conditions_frozen__not_output_passed`
  - 或是否已足以再推进一档
  - 若仍不足，唯一最小剩余缺口是什么
- 本轮不要展开：
  - 回到 `drafted -> frozen` 旧题
  - `target_weight` 是否还要再改状态
  - `adjusted_position_weight`
  - 回测
  - 最终组合实现

## FREE_GUESS_RANGE

- 允许你合理判断：
  - 新的 `target_weight` 上游状态是否已降低 `portfolio_tracking_error` 的不确定性
  - `frozen` 之后是否值得再前推一档
- 若缺证据必须写：
  - `NEED_EVIDENCE`

## EXPECTED_OUTPUT

- 你只能在三种结论里选一个：
  - `yes`
  - `no`
  - `conditional`
- 并严格按固定合同输出：
  - 结论
  - 一句话原因
  - 唯一最小剩余缺口 / 唯一附加条件
  - 禁止误写提醒
  - 若为 `yes` 的唯一焦点
