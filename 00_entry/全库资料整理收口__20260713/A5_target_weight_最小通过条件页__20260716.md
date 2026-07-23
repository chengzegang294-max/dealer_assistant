# A5 target_weight 最小通过条件页

更新时间：2026-07-16

## 用途

- 把 `target_weight` 从“输出闭合判断层”进一步推进到“最小通过条件已冻结”。
- 这页不是在宣布 `target_weight` 已通过。
- 这页只负责：
  - 冻结最小输入条件
  - 冻结最小输出条件
  - 冻结降级与中止条件
  - 冻结禁止性表述

## 当前结论

- `target_weight` 当前不能写成：
  - `output_passed`
  - `ready`
- `target_weight` 当前可以写成：
  - `pass_conditions_frozen__not_output_passed`
- 当前这一步的含义是：
  - 通过条件已冻结
  - 但是否真正通过仍待后续证据与上游口径支撑

## 一、最小输入条件

- 条件 1：
  - `alpha_score` 必须存在明确输入接口
  - 当前允许：
    - `signal_vector`
    - `ranked_scores`
  - 当前不允许：
    - 未命名的口头代理量
- 条件 2：
  - `constraint_set` 必须最少包含：
    - `weight_lower_bound`
    - `weight_upper_bound`
    - `long_only_flag`
    - `turnover_limit`
- 条件 3：
  - `benchmark_mode` 必须显式声明：
    - `benchmark_mode`
    - 或 `nonbenchmark_mode`
- 条件 4：
  - `covariance_model_id` 当前若未 formalize
    - 只允许写成：
      - `使用降级风险口径`
    - 不允许写成：
      - `正式风险模型已闭合`

## 二、最小输出条件

- 条件 1：
  - `target_weight` 输出必须有明确 schema
- 条件 2：
  - 输出值必须满足：
    - 权重非空
    - 单项权重位于边界内
    - 权重和可回溯
- 条件 3：
  - 若当前输出走降级模式
    - 必须显式带：
      - `degrade_flags`
- 条件 4：
  - 若不可解
    - 必须显式写：
      - `abort_reason`

## 三、降级与中止条件

- 场景 1：
  - `covariance_model_id` 未 formalize
  - 当前允许：
    - `equal_weight_or_value_weight + risk_overlay`
  - 当前不允许：
    - 伪装成正式优化器输出
- 场景 2：
  - `alpha_score` 接口不清
  - 当前结论：
    - `中止`
- 场景 3：
  - 最小约束集合不完整
  - 当前结论：
    - `继续保留 not_closed`

## 四、禁止性表述

- 禁止写成：
  - `target_weight 已可稳定输出`
  - `target_weight 已正式通过`
  - `portfolio_tracking_error 可随之通过`
  - `adjusted_position_weight 可随之通过`
- 禁止把：
  - `pass_conditions_frozen`
  写成：
  - `output_passed`

## 五、主负责人裁决

- 当前裁决是：
  - 先冻结 `target_weight` 的最小通过条件
- 当前不裁决：
  - `portfolio_tracking_error` 通过
  - `adjusted_position_weight` 通过
- 当前正确状态应写成：
  - `pass_conditions_frozen__not_output_passed`

## 六、一句话口径

- 当前 `target_weight` 已到：
  - `最小通过条件已冻结`
- 但仍未到：
  - `正式输出已通过`

## 回链

- `A5_target_weight_输出闭合判断页__20260716.md`
- `A5_G5_输出通过条件_多家AI回收记录与主负责人裁决__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
