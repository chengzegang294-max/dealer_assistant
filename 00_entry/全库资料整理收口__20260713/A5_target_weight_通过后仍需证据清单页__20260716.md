# A5 target_weight 通过后仍需证据清单页

更新时间：2026-07-16

## 用途

- 把 `target_weight` 从“最小通过条件已冻结”继续推进到“若要升格为 `output_passed`，还缺哪些新增证据”。
- 这页不新增实现。
- 这页只负责：
  - 写清升级门槛
  - 写清哪些证据是硬门槛
  - 写清哪些不足时只能继续保留 `not_output_passed`

## 当前结论

- `target_weight` 当前已经到：
  - `pass_conditions_frozen__not_output_passed`
- `target_weight` 当前还没到：
  - `output_passed`
- 当前最准确口径应写成：
  - `通过条件已冻结，第一手升格证据已补齐，但验证运行证据仍未齐`

## 一、升级为 `output_passed` 的最小硬证据

- 证据 1：
  - `alpha_score` 输入接口必须可回溯
  - 至少要能明确：
    - `signal_vector`
    - 或 `ranked_scores`
  - 不允许：
    - 未命名代理量直接入权重生成链
- 证据 2：
  - `constraint_set` 必须完整到可验收
  - 至少覆盖：
    - `weight_lower_bound`
    - `weight_upper_bound`
    - `long_only_flag`
    - `turnover_limit`
  - 若缺任一项：
    - 不得升格
- 证据 3：
  - `target_weight` 输出 schema 必须有可审计样例
  - 至少要能证明：
    - 权重非空
    - 单项权重在边界内
    - 权重和可回溯
    - `degrade_flags / abort_reason` 可显式带出
- 证据 4：
  - 风险口径必须明确写成哪一种：
    - `formalized_risk_model`
    - 或 `degraded_risk_handling`
  - 不允许：
    - 风险口径悬空
    - 写成“默认已有正式协方差模型”

## 二、可接受但不等于通过的中间状态

- 状态 A：
  - `covariance_model_id` 仍未 formalize
  - 但已明确只走：
    - `equal_weight_or_value_weight + risk_overlay`
  - 当前结论：
    - 允许继续保留 `pass_conditions_frozen`
    - 不允许升级为 `output_passed`
- 状态 B：
  - `constraint_set` 已大体存在
  - 但仍缺最小可验收样例
  - 当前结论：
    - 允许继续保留 `not_output_passed`
- 状态 C：
  - 输出 schema 已定义
  - 但没有可审计样例或失败样例
  - 当前结论：
    - 仍不得升格

## 三、当前最缺的证据

- 已经补齐的不是：
  - `constraint_set` 最小正式形式
  - 可审计权重样例
  - 失败样例与 `abort_reason`
- 当前真正剩下的缺口是：
  - `explicit validation run`
- 最小还差：
  - 成功验证记录
  - 失败验证记录与 `abort_reason` 路径一致性
  - 主负责人把 `no` 与最小缺口书面写死

## 四、禁止误写

- 禁止把：
  - `通过条件已冻结`
  写成：
  - `已正式通过`
- 禁止把：
  - `允许降级风险口径`
  写成：
  - `正式协方差路线已闭合`
- 禁止把：
  - `有输出 schema`
  写成：
  - `已有正式可消费输出`

## 五、主负责人裁决

- 当前最顺下一步不是：
  - 立刻推进 `portfolio_tracking_error`
  - 立刻推进 `adjusted_position_weight`
- 当前最顺下一步是：
  - 先补 `explicit validation run` 最小缺口
- 原因：
  - 它仍是两个下游输出段的共同上游门槛

## 六、一句话口径

- 当前 `target_weight` 已到：
  - `通过条件已冻结`
- 当前 `target_weight` 仍缺：
  - `显式验证运行记录 + 失败路径一致性`
- 所以当前仍只能写成：
  - `pass_conditions_frozen__not_output_passed`

## 回链

- `A5_target_weight_最小通过条件页__20260716.md`
- `A5_G5_输出通过条件_多家AI回收记录与主负责人裁决__20260716.md`
- `A5_target_weight_最小缺口补齐页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
