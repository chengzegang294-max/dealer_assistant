# A5 target_weight 重开升格裁决 多AI前情提要与裁决框架

更新时间：2026-07-16

## TASK

- 讨论：在 `actual generation execution` 已完成后，`target_weight` 是否已足以重开升格裁决。

## BACKGROUND

- `target_weight` 当前仍处于：
  - `pass_conditions_frozen__not_output_passed`
- 已完成：
  - 第一手升格证据补齐
  - 第二轮更窄裁决 `no`
  - template-level smoke-run
  - real-input case validation smoke-run
  - actual generation execution
- 当前新增硬证据是：
  - `tw_actual_generation_success_latest.json`
  - `tw_actual_generation_failure_latest.json`

## KNOWN_CONSTRAINTS

- 当前仍处于：
  - `degraded_risk_handling`
- 当前不能误写成：
  - `output_passed`
  - `正式优化器 ready`
  - `covariance_model_id ready`
- 本轮讨论的是：
  - 是否足以重开升格裁决
- 本轮不是讨论：
  - 是否直接判定 `output_passed`

## DISCUSSION_SCOPE

- 本轮允许讨论：
  - 当前新证据是否足以支持重开升格裁决
  - 若还不足，唯一最小剩余缺口是什么
  - 若足够，重开后的裁决应关注什么
- 本轮不要展开：
  - 大范围优化器理论
  - 新一轮信号组合讨论
  - 下游字段升格顺序

## FREE_GUESS_RANGE

- 允许合理推测：
  - 这批最小生成器证据的裁决价值
  - 重开裁决时最该问的焦点
- 若缺证据必须写：
  - `NEED_EVIDENCE`

## EXPECTED_OUTPUT

- 每个模型必须至少给出：
  - `yes`
  - `no`
  - `conditional`
  三类中的一个
- 并补充：
  - 一句话原因
  - 若为 `no / conditional`，唯一最小剩余缺口
  - 当前绝不能误写成什么

## 主负责人候选裁决方向

- 候选 1：
  - `yes`
  - 当前证据已足以重开升格裁决
- 候选 2：
  - `no`
  - 当前仍不足以重开
- 候选 3：
  - `conditional`
  - 只有在补一个最小新增条件后，才足以重开
