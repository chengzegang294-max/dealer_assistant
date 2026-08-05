# A5 target_weight 升格裁决 actual_generation后 多AI前情提要与裁决框架

更新时间：2026-07-16

## TASK

- 讨论：在 `actual generation execution` 已完成、且重开升格裁决资格已获批准后，`target_weight` 是否已足以进入更进一步的升级判断。

## BACKGROUND

- 当前 `target_weight` 已完成：
  - template-level smoke-run
  - real-input case validation smoke-run
  - actual generation execution
  - 重开升格裁决多AI回包吸收
- 当前主负责人已裁定：
  - `yes，足以重开升格裁决`
- 当前尚未裁定的是：
  - 在 `degraded_risk_handling` 与 `covariance_model_id` 未闭合边界下，`target_weight` 是否具备更进一步的升级资格

## KNOWN_CONSTRAINTS

- 当前仍处于：
  - `degraded_risk_handling`
- 当前不能误写成：
  - `output_passed`
  - `正式优化器 ready`
  - `covariance_model_id ready`

## DISCUSSION_SCOPE

- 本轮允许讨论：
  - 当前新增证据在升级判断层面的价值
  - `degraded_risk_handling` 的边界是否足以支撑更进一步判断
  - `covariance_model_id` 未闭合是否仍然构成硬门槛
- 本轮不要展开：
  - 大范围回测
  - 新信号组合讨论
  - 下游字段跟升

## FREE_GUESS_RANGE

- 允许合理推测：
  - 降级风险处理边界在当前阶段的可接受性
  - 升级判断与最终 `output_passed` 之间的最小分隔线
- 若缺证据必须写：
  - `NEED_EVIDENCE`

## EXPECTED_OUTPUT

- 每个模型至少给出：
  - `yes / no / conditional`
- 并写清：
  - 一句话原因
  - 若为 `no / conditional`，唯一最小剩余缺口
  - 当前绝不能误写成什么
