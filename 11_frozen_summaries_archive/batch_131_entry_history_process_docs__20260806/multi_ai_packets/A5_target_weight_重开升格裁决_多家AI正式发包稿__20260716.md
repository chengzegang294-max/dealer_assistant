# A5 target_weight 重开升格裁决 多家AI正式发包稿

你现在参与的是一个多AI讨论，不是自由闲聊。

## TASK

- 讨论：在 `actual generation execution` 已完成后，`target_weight` 是否已足以重开升格裁决。

## BACKGROUND

- 当前项目已把 `target_weight` 推进到：
  - `pass_conditions_frozen__not_output_passed`
- 已完成的关键证据包括：
  - 第一手升格证据补齐
  - 第二轮更窄裁决 `no`
  - template-level smoke-run
  - real-input case validation smoke-run
  - actual generation execution
- 最新新增硬证据包括：
  - success generation execution 结果
  - failure generation execution 结果

## KNOWN_CONSTRAINTS

- 当前仍是：
  - `degraded_risk_handling`
- 当前不能误写成：
  - `output_passed`
  - `正式优化器 ready`
  - `covariance_model_id ready`

## DISCUSSION_SCOPE

- 本轮允许讨论：
  - 当前是否足以重开升格裁决
  - 如果不足，唯一最小剩余缺口是什么
  - 如果足够，重开后的裁决焦点应是什么
- 本轮不要展开：
  - 是否直接判定 `output_passed`
  - 下游字段是否跟着升格
  - 大范围交易逻辑或回测讨论

## FREE_GUESS_RANGE

- 允许你合理判断：
  - 这批 actual generation execution 证据的裁决价值
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
   - 写出重开升格裁决时最该看的唯一焦点
