# A5 portfolio_tracking_error covariance_model_id 最小输入层页

更新时间：2026-07-16

## 用途

- 把 `portfolio_tracking_error` 当前第二缺口压成正式一页。
- 这页不宣布：
  - `covariance_model_id ready`
  - `portfolio_tracking_error output_passed`
- 这页只负责：
  - 冻结 `portfolio_tracking_error` 对 `covariance_model_id` 的最小输入要求
  - 写清当前允许消费到哪一层
  - 给后续降级风险口径样例页提供统一入口

## 当前结论

- 当前 `portfolio_tracking_error` 仍不能写成：
  - `output_passed`
- 当前可以正式写成：
  - `covariance_model_id` 最小输入层已冻结
- 当前最小输入层的含义不是：
  - 已有正式协方差矩阵实现
- 当前最小输入层的含义是：
  - 已可明确 `portfolio_tracking_error` 在 benchmark 风险输出判断中，至少需要怎样命名和约束 `covariance_model_id`

## 一、为什么现在补这页

- 原因 1：
  - `benchmark` 风险输出最小正式口径已冻结
- 原因 2：
  - 当前第二缺口正是：
    - `covariance_model_id` 最小输入层
- 原因 3：
  - 若这一层继续悬空，后续降级风险样例会失去统一输入边界

## 二、最小输入层组成

- 输入 1：
  - 必须显式存在：
    - `covariance_model_id`
- 输入 2：
  - 它当前允许的状态至少可以是：
    - `candidate_model_family_frozen__not_ready`
    - `unique_model_frozen__not_ready`
    - `ready_judgement_conditional__downstream_still_locked`
- 输入 3：
  - 必须同时绑定：
    - `benchmark_id`
    - `tracking_error_limit`
    - `risk_mode`
- 输入 4：
  - 若当前仍处于降级风险模式，
    - 必须显式保留：
      - `degrade_flags`

## 三、当前允许的最小消费方式

- 允许把 `covariance_model_id` 消费为：
  - 风险模型家族标识
  - 风险口径来源占位
  - benchmark 风险输出判断时的显式输入项
- 当前不要求：
  - 协方差矩阵本体已产出
  - 历史窗口估计已实跑
  - shrinkage 或 factor covariance 参数已定稿

## 四、当前必须守住的边界

- 边界 1：
  - `covariance_model_id` 当前只能证明：
    - 风险模型来源已被命名
  - 不能证明：
    - 风险模型已完全解锁下游
- 边界 2：
  - `portfolio_tracking_error` 当前可引用该输入层继续判断
  - 但不能因此写成：
    - 风险输出已正式可消费
- 边界 3：
  - 若缺少 `benchmark_id` 或 `tracking_error_limit`
  - 则不得把 `covariance_model_id` 单独拔高成充分输入

## 五、当前允许写法

- 允许写成：
  - `portfolio_tracking_error` 已具备 `covariance_model_id` 最小输入层
  - `covariance_model_id` 当前已能作为 benchmark 风险输出判断的命名输入
  - 当前风险模型可以高于 `under_judgement`
    但仍保留：
    - `downstream_still_locked`

## 六、当前禁止误写

- 禁止写成：
  - `covariance_model_id 已 ready`
  - `tracking_error 已具备正式风险模型输入`
  - `portfolio_tracking_error 已可正式消费`
- 禁止把：
  - 最小输入层
  写成：
  - 正式协方差实现已完成

## 七、与前后页的关系

- 这页承接：
  - `A5_portfolio_tracking_error_benchmark风险输出最小正式口径页__20260716.md`
- 这页之后的下一手应是：
  - `降级风险口径可审计样例`
- 这页当前仍没有解决：
  - tracking error 的正式数值输出
  - 风险模型最终选型
  - 组合层实现

## 八、主负责人裁决

- 当前不做：
  - `portfolio_tracking_error` 升格裁决
  - 风险模型实现拍板
- 当前正式裁决是：
  - 允许把 `covariance_model_id` 写到 `portfolio_tracking_error` 的最小输入层
  - 但仍保留：
    - `pass_conditions_drafted__not_output_passed`
  - 且即便上游已推进到：
    - `ready_judgement_conditional__downstream_still_locked`
    也不能把当前页写成：
    - `portfolio_tracking_error output_passed`
- 这一步的价值在于：
  - 第二缺口不再悬空
  - 下一手可以顺滑切到：
    - `降级风险口径可审计样例`

## 九、一句话口径

- 当前 `portfolio_tracking_error` 已补齐第二缺口：
  - `covariance_model_id 最小输入层已冻结`
- 但当前仍未到：
  - `output_passed`

## 回链

- `A5_covariance_model_id_实现前口径判断页__20260716.md`
- `A5_portfolio_tracking_error_最小通过条件页__20260716.md`
- `A5_portfolio_tracking_error_升级判断准备页__20260716.md`
- `A5_portfolio_tracking_error_benchmark风险输出最小正式口径页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
