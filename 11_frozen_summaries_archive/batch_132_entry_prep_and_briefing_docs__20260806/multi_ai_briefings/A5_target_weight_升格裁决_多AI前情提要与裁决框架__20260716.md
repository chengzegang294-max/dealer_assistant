# A5 target_weight 升格裁决 多AI前情提要与裁决框架

更新时间：2026-07-16

## TASK

- 讨论 `target_weight` 当前这批首轮补齐证据，是否已经足以支持发起一次新的升格裁决。

## BACKGROUND

- 当前主线在：
  - `A5 -> G5 输出升格收口`
- 当前正式升格顺序已固定为：
  - `target_weight`
  - `portfolio_tracking_error`
  - `adjusted_position_weight`
- `target_weight` 当前状态为：
  - `pass_conditions_frozen__not_output_passed`
- 已新增第一手执行物：
  - `A5_target_weight_升格证据补齐页__20260716.md`
- 当前已补的首轮证据包括：
  - `constraint_set` 最小正式形式
  - 可审计权重样例
  - 失败样例与 `abort_reason`

## KNOWN_CONSTRAINTS

- 当前不进入 runtime 新开发。
- 当前不把任何组合层输出误写成：
  - `passed`
  - `ready`
  - `implementation_ready`
- 当前 `covariance_model_id` 仍未正式闭合。
- 当前允许的风险口径仍可包含：
  - `degraded_risk_handling`

## DISCUSSION_SCOPE

- 本轮允许讨论：
  - 当前首轮补齐证据是否足以支撑一次新的升格裁决
  - 若不够，还差哪一类最小新增证据
  - 是否应继续停在 `pass_conditions_frozen__not_output_passed`
  - 还是允许升级到更接近 passed 的判断层
- 本轮不要展开：
  - 新资料补采
  - `portfolio_tracking_error` 升格
  - `adjusted_position_weight` 升格
  - `G6` 解冻
  - runtime 实现

## FREE_GUESS_RANGE

- 允许合理推测：
  - 在当前降级风险口径下，什么程度的样例可视为“足以支持下一轮裁决”
- 若缺证据必须写：
  - `NEED_EVIDENCE`
- 不允许把：
  - 经验判断
  写成：
  - 已验证真值

## EXPECTED_OUTPUT

- 请至少给出 `2-4` 个方案，例如：
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

## 主负责人基线

- 当前默认不直接宣布：
  - `target_weight = output_passed`
- 当前默认先判断：
  - 这批首轮证据是否足够支撑一轮新的升格裁决
- 如果答案是否定：
  - 必须写清最小还差什么
- 如果答案是肯定：
  - 也只能写成：
    - `可发起升格裁决`
  - 不能直接写成：
    - `已经 passed`

## 回链

- `A5_target_weight_通过后仍需证据清单页__20260716.md`
- `A5_target_weight_升格证据补齐页__20260716.md`
- `A5_G5_输出升格证据总表__20260716.tsv`
- `A5_G5_输出升格顺序裁决页__20260716.md`
