# A5 target_weight 升级判断重开 多AI前情提要与裁决框架

更新时间：2026-07-16

## TASK

- 讨论：在 `actual_generation后` 升级判断已被裁成 `conditional`、且唯一附加条件已补到可判断层后，`target_weight` 是否已足以进入下一档正式升级判断结论。

## BACKGROUND

- 当前 `target_weight` 已推进到：
  - `pass_conditions_frozen__not_output_passed`
- 已完成：
  - 第二轮窄裁决 `no`
  - template-level smoke-run
  - real-input case validation smoke-run
  - actual generation execution
  - 重开升格裁决 `yes`
  - `actual_generation后` 升级判断第二轮 `conditional`
  - `degraded_risk_handling` 充分性与稳健边界页
  - 边界验证清单页
  - 主负责人书面验收页

## KNOWN_CONSTRAINTS

- 当前仍是：
  - `degraded_risk_handling`
- 当前仍未闭合：
  - `covariance_model_id`
- 当前不能误写成：
  - `output_passed`
  - `正式优化器 ready`
  - `covariance_model_id ready`

## DISCUSSION_SCOPE

- 本轮允许讨论：
  - 当前是否足以把升级判断从 `conditional` 继续推进一档
  - 如果仍不足，唯一剩余缺口是什么
  - 如果足够，当前最稳正式结论应写到哪
- 本轮不要展开：
  - 是否已经 `output_passed`
  - 回测与信号组合
  - 下游输出段升格

## FREE_GUESS_RANGE

- 允许你合理判断：
  - 书面验收与边界验证是否已足以消化 `conditional` 的唯一附加条件
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
