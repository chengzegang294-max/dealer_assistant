# A5 target_weight 输出闭合判断页

更新时间：2026-07-16

## 用途

- 把 `target_weight` 从“最小生成链已定义”继续推进到“输出闭合判断层”。
- 这页不是优化器实现页。
- 这页也不是在宣布 `target_weight` 已 ready。
- 这页只负责：
  - 判断当前为什么还不能宣布目标权重输出闭合
  - 固定当前最小闭合条件
  - 给后续 `portfolio_tracking_error` 与 `adjusted_position_weight` 提供明确上游口径

## 当前结论

- `target_weight` 当前仍不能写成：
  - `output_closed`
- `target_weight` 当前可以写成：
  - `output_closure_under_judgement__not_closed`
- 当前最小生成链已经具备：
  - `alpha`
  - `risk_model`
  - `constraints`
  - `benchmark_mode`
- 但当前仍缺：
  - 明确可消费的风险模型口径
  - 正式输出级别的求解口径
  - 与降级模式之间的边界冻结

## 一、当前字段状态

- 字段名：
  - `target_weight`
- 所属层：
  - `portfolio_final_outputs`
- 当前来源状态：
  - `generation_chain_defined__output_not_closed`
- 当前角色：
  - `组合目标权重输出`
- 当前阶段定位：
  - `输出闭合判断层`

## 二、为什么现在进入输出闭合判断

- 原因 1：
  - `G5` 当前已经被正式裁定为：
    - `chain_defined__output_closure_not_passed`
- 原因 2：
  - `target_weight` 是当前第一优先输出对象
- 原因 3：
  - 它直接卡住：
    - `portfolio_tracking_error`
    - `adjusted_position_weight`

## 三、当前最小闭合条件

- 条件 1：
  - `alpha_score` 必须保持：
    - `contract_frozen_proxy`
  - 且不得漂移为未定义代理输入
- 条件 2：
  - `covariance_model_id` 至少要维持：
    - `ready_judgement_conditional__downstream_still_locked`
  - 且唯一模型与 fallback 合同不能失真
- 条件 3：
  - 必须明确当前输出到底走：
    - `benchmark 约束优化主口径`
    - 或 `equal_weight_or_value_weight + risk_overlay` 降级口径
- 条件 4：
  - 权重边界、换手限制、long_only 等约束不能只存在于口头描述

## 四、为什么当前仍不能判闭合

- 原因 1：
  - `covariance_model_id` 还没进入正式可实现输入层
- 原因 2：
  - 当前只定义了生成链，没有定义“何时算输出通过”
- 原因 3：
  - 降级模式虽然存在，但还不能被误写成完整优化器输出
- 因此当前不能写成：
  - `target_weight 已可稳定输出`
  - `target_weight 已通过输出闭合`

## 五、当前允许写法

- 允许写成：
  - `target_weight 当前已进入输出闭合判断层`
  - `target_weight 当前仍未通过输出闭合`
  - `target_weight 当前属于 output_closure_under_judgement__not_closed`

## 六、禁止误写

- 禁止写成：
  - `target_weight 已 ready`
  - `target_weight 已有正式优化器输出`
  - `portfolio_tracking_error 已可正式输出`
  - `adjusted_position_weight 已可正式运行`
- 禁止把：
  - 当前输出闭合判断
  写成：
  - 当前已经形成正式输出结果

## 七、与下游的关系

- 当前这页能解决的是：
  - `target_weight` 已不再只是“生成链已定义”
  - 而是进入了“为什么还不能闭合输出”的判断层
- 当前这页还没有解决：
  - `portfolio_tracking_error` 的输出闭合
  - `adjusted_position_weight` 的最终输出闭合
  - 优化器实现

## 八、主负责人裁决

- 当前裁决不是：
  - 把 `target_weight` 直接升格为 ready
- 当前裁决是：
  - 允许它进入：
    - `输出闭合判断层`
  - 当前正确状态应写成：
    - `output_closure_under_judgement__not_closed`
- 这一步的价值在于：
  - `G5` 的第一优先输出对象已经不再悬空
  - 后续 `portfolio_tracking_error` 与 `adjusted_position_weight` 都能围绕同一上游口径继续判断

## 九、一句话口径

- 当前 `target_weight` 的正确写法是：
  - `output_closure_under_judgement__not_closed`

## 回链

- `A5_target_weight_最小生成链判断页__20260716.md`
- `A5_G5_输出闭合判断页__20260716.md`
- `A5_covariance_model_id_实现前口径判断页__20260716.md`
- `A5_portfolio_tracking_error_风险输出链判断页__20260716.md`
- `A5_adjusted_position_weight_回溯闭合判断页__20260716.md`
