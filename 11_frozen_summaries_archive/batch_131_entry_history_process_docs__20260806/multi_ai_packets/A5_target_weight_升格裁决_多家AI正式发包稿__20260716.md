# A5 target_weight 升格裁决 多家AI正式发包稿

你现在参与的是一个多AI讨论，不是自由闲聊。

## TASK

- 讨论 `target_weight` 当前这批首轮补齐证据，是否已经足以支持发起一次新的升格裁决。

## BACKGROUND

- 当前项目主线在：
  - `A5 -> G5 输出升格收口`
- 当前三段输出的正式升格顺序已固定为：
  - `target_weight`
  - `portfolio_tracking_error`
  - `adjusted_position_weight`
- `target_weight` 当前状态为：
  - `pass_conditions_frozen__not_output_passed`
- 当前已经补齐的首轮证据：
  - `constraint_set` 最小正式形式
  - 可审计权重样例
  - 失败样例与 `abort_reason`

## KNOWN_CONSTRAINTS

- 当前不进入 runtime 新开发。
- 当前不允许把任何判断直接写成：
  - `passed`
  - `ready`
  - `implementation_ready`
- 当前 `covariance_model_id` 仍未正式闭合。
- 当前允许的风险口径可包含：
  - `degraded_risk_handling`

## DISCUSSION_SCOPE

- 本轮允许讨论：
  - 这批首轮证据是否足以支持发起一次新的升格裁决
  - 若不足，还差哪一类最小新增证据
  - 当前应继续维持什么状态表述
- 本轮不要展开：
  - 新资料补采
  - `portfolio_tracking_error` 升格
  - `adjusted_position_weight` 升格
  - `G6` 解冻
  - runtime 实现

## FREE_GUESS_RANGE

- 允许你合理推测：
  - 在降级风险口径仍存在时，什么程度的样例可视为“足以支持下一轮升格裁决”
- 若缺证据必须写：
  - `NEED_EVIDENCE: ...`
- 不允许把经验推断写成已验证真值。

## EXPECTED_OUTPUT

- 请至少给出 `2-4` 个不同方案，例如：
  - 保守维持型
  - 证据再补一手型
  - 可开升格裁决型
  - 条件式升格候选型
- 每个方案都必须写：
  - 方案名
  - 核心思路
  - 适用条件
  - 优点
  - 缺点
  - 风险
  - `NEED_EVIDENCE`
- 最后请给出：
  - 你最推荐的方案
  - 为什么不推荐另外几个
  - 当前最小下一步

## OUTPUT CONTRACT

1. 结论摘要
2. 方案对比（至少 2 个）
3. 最推荐方案
4. 当前最小下一步

## 主负责人基线

- 当前默认不直接宣布：
  - `target_weight = output_passed`
- 当前默认先判断：
  - 这批首轮证据是否足够支撑一轮新的升格裁决
- 如果你认为还不够：
  - 必须写清最小还差什么
- 如果你认为已经够：
  - 也只能写成：
    - `可发起升格裁决`
  - 不能直接写成：
    - `已经 passed`
