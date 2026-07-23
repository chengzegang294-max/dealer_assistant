# A5 portfolio_tracking_error 风险输出链判断页

更新时间：2026-07-16

## 用途

- 把 `portfolio_tracking_error` 从纯 `future_only` 阻塞项，推进到“风险输出链可判断”层。
- 这页不是跟踪误差实现页。
- 这页也不是在宣布风险输出已正式可用。
- 这页只负责：
  - 冻结当前风险输出链前提
  - 写清 benchmark 模式下的依赖关系
  - 防止过早把风险输出写成已闭合

## 当前结论

- `portfolio_tracking_error` 当前仍不能写成：
  - `formal_output_ready`
- `portfolio_tracking_error` 当前可以写成：
  - `risk_output_chain_defined__not_output_ready`
- 当前最关键的前提是：
  - `benchmark_mode`
  - `covariance_model_id`
  - `target_weight`
- 只要三者之一未闭合：
  - 当前默认不输出正式 `portfolio_tracking_error`

## 一、当前字段状态

- 字段名：
  - `portfolio_tracking_error`
- 所属层：
  - `portfolio_final_outputs`
- 当前来源状态：
  - `future_only`
- 当前角色：
  - `benchmark 风险输出`
- 当前阻塞位置：
  - `G5 / risk_output`

## 二、为什么现在进入判断页

- 原因 1：
  - `covariance_model_id` 已进入实现前口径判断
- 原因 2：
  - `target_weight` 已进入最小生成链判断
- 原因 3：
  - `portfolio_tracking_error` 是 benchmark 模式下的关键验收输出之一，不能一直停在完全无结构状态

## 三、当前最小风险输出链

- 当前允许写成的最小风险输出链是：
  - `benchmark_id`
  - `target_weight`
  - `covariance_model_id`
  - `tracking_error_limit`
  ->
  - `portfolio_tracking_error`

### 解释

- 这条链当前只说明：
  - `portfolio_tracking_error` 至少依赖 benchmark、权重与风险模型
- 这不意味着：
  - 已有正式风险矩阵
  - 已有正式输出数值
  - 当前 benchmark 模式已 fully closed

## 四、当前允许的模式判断

### benchmark_mode

- 若存在：
  - `benchmark_id`
- 则：
  - 允许继续保留 `portfolio_tracking_error` 为目标输出字段
- 但只有在：
  - `target_weight`
  - `covariance_model_id`
  至少都进入实现前可判断层时，才允许讨论它的最小输出链

### nonbenchmark_mode

- 若缺：
  - `benchmark_id`
- 则必须：
  - 切到 `nonbenchmark_mode`
  - 不输出正式 `portfolio_tracking_error`

## 五、当前最小断言

- 断言 1：
  - benchmark 模式下，`portfolio_tracking_error` 才是必须字段
- 断言 2：
  - 若缺 `benchmark_id`
    - 不得伪造 `portfolio_tracking_error`
- 断言 3：
  - 若 `covariance_model_id` 未进入可判断层
    - 不得写成正式风险输出链已闭合
- 断言 4：
  - 若 `target_weight` 仍未闭合
    - `portfolio_tracking_error` 只能保留为：
      - `not_output_ready`

## 六、当前允许写法

- 允许写成：
  - `portfolio_tracking_error 当前风险输出链已定义`
  - `portfolio_tracking_error 当前仍未形成正式输出`
  - `portfolio_tracking_error 当前属于 risk_output_chain_defined__not_output_ready`

## 七、禁止误写

- 禁止写成：
  - `portfolio_tracking_error 已可正式输出`
  - `benchmark 风险输出已闭合`
  - `当前已完成 tracking error 实现`
- 禁止把：
  - 风险输出链定义
  写成：
  - 正式运行结果

## 八、与上游和下游的关系

- 当前这页能解决的是：
  - `portfolio_tracking_error` 不再是纯黑盒 future_only
  - benchmark 模式下的最小风险输出依赖关系已清楚
- 当前这页还没有解决：
  - tracking error 的正式数值输出
  - 风险模型最终选型
  - 优化器或风险引擎实现

## 九、主负责人裁决

- 当前裁决不是：
  - 把 `portfolio_tracking_error` 升格为已闭合输出
- 当前裁决是：
  - 允许它进入：
    - `风险输出链判断层`
  - 当前正确状态应写成：
    - `risk_output_chain_defined__not_output_ready`
- 这一步的价值在于：
  - 让 benchmark 风险输出的依赖关系固定下来
  - 但仍守住“不直接开实现”的边界

## 十、一句话口径

- 当前 `portfolio_tracking_error` 的正确写法是：
  - `risk_output_chain_defined__not_output_ready`

## 回链

- `A_REQ_003_字段映射表__20260715.tsv`
- `A_REQ_003_最小验收口径__20260715.md`
- `A5_covariance_model_id_实现前口径判断页__20260716.md`
- `A5_target_weight_最小生成链判断页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
