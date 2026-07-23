# A5 portfolio_tracking_error 输出闭合判断页

更新时间：2026-07-16

## 用途

- 把 `portfolio_tracking_error` 从“风险输出链已定义”继续推进到“输出闭合判断层”。
- 这页不是风险引擎实现页。
- 这页也不是在宣布 `portfolio_tracking_error` 已 ready。
- 这页只负责：
  - 判断当前为什么还不能宣布跟踪误差输出闭合
  - 固定当前最小闭合条件
  - 为后续组合层最终输出判断提供统一 benchmark 风险口径

## 当前结论

- `portfolio_tracking_error` 当前仍不能写成：
  - `output_closed`
- `portfolio_tracking_error` 当前可以写成：
  - `output_closure_under_judgement__not_closed`
- 当前最小风险输出链已经具备：
  - `benchmark_id`
  - `target_weight`
  - `covariance_model_id`
  - `tracking_error_limit`
- 但当前仍缺：
  - 明确可消费的风险模型输出口径
  - benchmark 模式下的正式输出通过条件
  - 与 nonbenchmark 降级口径之间的边界冻结

## 一、当前字段状态

- 字段名：
  - `portfolio_tracking_error`
- 所属层：
  - `portfolio_final_outputs`
- 当前来源状态：
  - `risk_output_chain_defined__not_output_ready`
- 当前角色：
  - `benchmark 风险输出`
- 当前阶段定位：
  - `输出闭合判断层`

## 二、为什么现在进入输出闭合判断

- 原因 1：
  - `target_weight` 已进入：
    - `output_closure_under_judgement__not_closed`
- 原因 2：
  - `portfolio_tracking_error` 已不再只是“风险输出链已定义”
- 原因 3：
  - 它是 `benchmark_mode` 下的关键输出字段，不能长期停在只有链没有闭合判断的状态

## 三、当前最小闭合条件

- 条件 1：
  - 必须存在：
    - `benchmark_id`
  - 否则必须切到：
    - `nonbenchmark_mode`
- 条件 2：
  - `target_weight` 至少要维持：
    - `output_closure_under_judgement__not_closed`
  - 且不得退回为未定义上游输出
- 条件 3：
  - `covariance_model_id` 至少要维持：
    - `ready_judgement_conditional__downstream_still_locked`
  - 且唯一模型与 fallback 合同不能漂移
- 条件 4：
  - `tracking_error_limit` 不能只是名字存在，必须作为 risk budget 约束被显式保留

## 四、为什么当前仍不能判闭合

- 原因 1：
  - `covariance_model_id` 虽已高于实现前判断层，
    但当前仍保留：
    - `downstream_still_locked`
- 原因 2：
  - `target_weight` 也还没通过输出闭合
- 原因 3：
  - 当前只定义了风险输出链，没有定义“何时算 tracking error 输出通过”
- 原因 4：
  - 若切到 `nonbenchmark_mode`，当前就不应再伪造 `portfolio_tracking_error`
- 因此当前不能写成：
  - `portfolio_tracking_error 已可正式输出`
  - `benchmark 风险输出已闭合`

## 五、当前允许写法

- 允许写成：
  - `portfolio_tracking_error 当前已进入输出闭合判断层`
  - `portfolio_tracking_error 当前仍未通过输出闭合`
  - `portfolio_tracking_error 当前属于 output_closure_under_judgement__not_closed`

## 六、禁止误写

- 禁止写成：
  - `portfolio_tracking_error 已 ready`
  - `benchmark 风险输出已 ready`
  - `组合层风险输出已完成实现`
  - `adjusted_position_weight 已可直接消费 tracking_error`
- 禁止把：
  - 当前输出闭合判断
  写成：
  - 当前已经形成正式风险输出结果

## 七、与上游和下游的关系

- 当前这页能解决的是：
  - `portfolio_tracking_error` 已不再只是“风险输出链已定义”
  - 而是进入了“为什么还不能闭合输出”的判断层
- 当前这页还没有解决：
  - tracking error 的正式数值输出
  - 风险模型最终选型
  - 最终组合实现

## 八、主负责人裁决

- 当前裁决不是：
  - 把 `portfolio_tracking_error` 直接升格为 ready
- 当前裁决是：
  - 允许它进入：
    - `输出闭合判断层`
  - 当前正确状态应写成：
    - `output_closure_under_judgement__not_closed`
- 这一步的价值在于：
  - `G5` 的第二个输出对象不再悬空
  - 后续最终融合输出将能围绕更稳定的 benchmark 风险口径继续判断

## 九、一句话口径

- 当前 `portfolio_tracking_error` 的正确写法是：
  - `output_closure_under_judgement__not_closed`

## 回链

- `A5_portfolio_tracking_error_风险输出链判断页__20260716.md`
- `A5_target_weight_输出闭合判断页__20260716.md`
- `A5_G5_输出闭合判断页__20260716.md`
- `A5_covariance_model_id_实现前口径判断页__20260716.md`
- `A5_adjusted_position_weight_回溯闭合判断页__20260716.md`
