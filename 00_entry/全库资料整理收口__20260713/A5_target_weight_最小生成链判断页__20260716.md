# A5 target_weight 最小生成链判断页

更新时间：2026-07-16

## 用途

- 把 `target_weight` 从纯 `future_only` 阻塞项，推进到“最小生成链可判断”层。
- 这页不是优化器实现页。
- 这页也不是在宣布目标权重已可稳定输出。
- 这页只负责：
  - 冻结当前最小生成链
  - 写清前置条件、允许表述与禁止误写
  - 为后续 `adjusted_position_weight` 回溯提供上游框架

## 当前结论

- `target_weight` 当前仍不能写成：
  - `stable_output_ready`
- `target_weight` 当前可以写成：
  - `generation_chain_defined__output_not_closed`
- 当前最小生成链已经足以写清：
  - 上游输入是什么
  - 约束边界是什么
  - 缺什么时必须降级或中止
- 但还不能写成：
  - 已有正式优化器输出

## 一、当前字段状态

- 字段名：
  - `target_weight`
- 所属层：
  - `portfolio_final_outputs`
- 当前来源状态：
  - `future_only`
- 当前角色：
  - `组合目标权重输出`
- 当前阻塞位置：
  - `G5 / optimizer_output`

## 二、为什么现在进入判断页

- 原因 1：
  - `alpha_score` 已完成正式代理合同冻结
- 原因 2：
  - `covariance_model_id` 已进入实现前口径判断
- 原因 3：
  - 若不先定义最小生成链，`adjusted_position_weight` 会一直被动卡死在：
    - `blocked_by_missing_target_weight`

## 三、当前最小生成链

- 当前允许写成的最小生成链是：
  - `alpha_score`
  - `covariance_model_id`
  - `benchmark_id / nonbenchmark_mode`
  - `tracking_error_limit`
  - `active_risk_aversion`
  - `transaction_cost_bps`
  - `weight_lower_bound`
  - `weight_upper_bound`
  - `turnover_limit`
  - `long_only_flag`
  ->
  - `target_weight`

### 解释

- 这条链现在只说明：
  - `target_weight` 不是凭空来的
  - 它至少要消费 alpha、风险、约束与基准模式
- 这不意味着：
  - 求解器已实现
  - 所有参数已定稿
  - 所有输出都能正式跑通

## 四、当前允许的生成模式

### 模式 1：benchmark 约束优化主口径

- 当前定位：
  - `推荐生成模式`
- 含义：
  - 在 `benchmark + tracking_error_limit + constraints` 下生成目标权重
- 前提：
  - `alpha_score` 有正式代理合同
  - `covariance_model_id` 至少进入实现前口径判断

### 模式 2：equal_weight_or_value_weight 降级口径

- 当前定位：
  - `降级生成模式`
- 含义：
  - 当 `covariance_model_id` 仍未闭合时，允许退回：
    - `equal_weight_or_value_weight + risk_overlay`

## 五、当前最小断言

- 断言 1：
  - `target_weight` 必须满足：
    - `weight_lower_bound <= target_weight <= weight_upper_bound`
- 断言 2：
  - `target_weight` 必须能回链到：
    - 上游 alpha / 风险 / 约束输入族
- 断言 3：
  - 若缺 `alpha_score`
    - 必须 `ABORT`
- 断言 4：
  - 若缺 `covariance_model_id`
    - 不得伪装成完整优化器输出
    - 必须降级到：
      - `equal_weight_or_value_weight + risk_overlay`

## 六、当前允许写法

- 允许写成：
  - `target_weight 当前最小生成链已定义`
  - `target_weight 当前仍未闭合正式输出，但上游依赖已可判断`
  - `target_weight 当前属于 generation_chain_defined__output_not_closed`

## 七、禁止误写

- 禁止写成：
  - `target_weight 已可稳定输出`
  - `target_weight 已有正式优化器结果`
  - `adjusted_position_weight 已可正式回溯通过`
- 禁止把：
  - 生成链定义
  写成：
  - 实际可运行结果

## 八、与下游的关系

- 当前这页能解决的是：
  - `target_weight` 不再是纯黑盒 future_only
  - `adjusted_position_weight` 的前置链开始明确
- 当前这页还没有解决：
  - 目标权重的真实数值输出
  - `portfolio_tracking_error` 的正式风险输出
  - 优化器实现

## 九、主负责人裁决

- 当前裁决不是：
  - 直接把 `target_weight` 升格为已闭合输出
- 当前裁决是：
  - 允许它进入：
    - `最小生成链判断层`
  - 当前正确状态应写成：
    - `generation_chain_defined__output_not_closed`
- 这一步的价值在于：
  - 让 `adjusted_position_weight` 的阻塞原因具体化
  - 避免继续把 `target_weight` 当纯黑盒悬空

## 十、一句话口径

- 当前 `target_weight` 的正确写法是：
  - `generation_chain_defined__output_not_closed`

## 回链

- `A_REQ_003_字段映射表__20260715.tsv`
- `A_REQ_003_最小验收口径__20260715.md`
- `A5_covariance_model_id_实现前口径判断页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
- `A5_G5G6_多家AI回收记录与主负责人裁决__20260716.md`
