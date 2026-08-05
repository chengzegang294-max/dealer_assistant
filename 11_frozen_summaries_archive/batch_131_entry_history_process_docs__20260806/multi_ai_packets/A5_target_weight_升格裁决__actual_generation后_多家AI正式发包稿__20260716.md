# A5 target_weight 升格裁决 actual_generation后 多家AI正式发包稿

你现在参与的是一个多AI讨论，不是自由闲聊。

## TASK

- 讨论：在 `actual generation execution` 已完成、且重开升格裁决资格已获批准后，`target_weight` 是否已足以进入更进一步的升级判断。

## BACKGROUND

- 当前 `target_weight` 已完成：
  - template-level smoke-run
  - real-input case validation smoke-run
  - actual generation execution
- 当前主负责人已裁定：
  - `yes，足以重开升格裁决`
- 但当前仍未裁定：
  - `degraded_risk_handling` 与 `covariance_model_id` 未闭合边界下，是否足以进入更进一步升级判断

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
  - `degraded_risk_handling` 是否足以支撑更进一步判断
  - `covariance_model_id` 未闭合是否仍是硬门槛
- 本轮不要展开：
  - 是否直接宣布 `output_passed`
  - 回测与信号组合
  - 下游字段升格

## FREE_GUESS_RANGE

- 允许你合理判断：
  - 升级判断与最终通过之间的最小边界
- 若缺证据必须写：
  - `NEED_EVIDENCE`

## OUTPUT CONTRACT

1. 结论：
   - 只能写 `yes / no / conditional`
2. 一句话原因：
   - 只写最核心原因
3. 若为 `no / conditional`：
   - 写出唯一最小剩余缺口
4. 禁止误写提醒：
   - 当前为什么仍不能写成 `output_passed`
5. 若为 `yes`：
   - 写出升级判断时最该看的唯一焦点
