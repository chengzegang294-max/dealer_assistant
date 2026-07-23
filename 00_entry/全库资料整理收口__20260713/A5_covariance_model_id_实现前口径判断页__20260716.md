# A5 covariance_model_id 实现前口径判断页

更新时间：2026-07-16

## 用途

- 把 `covariance_model_id` 从纯 `future_only` 黑盒，推进到“可判断的实现前入口”层。
- 这页不是协方差模型实现页。
- 这页也不是在宣布风险模型已 ready。
- 这页只负责：
  - 判断它是否值得进入实现前口径
  - 冻结当前可接受的最小讨论范围
  - 写清允许表述、禁止误写与下一手条件

## 当前结论

- `covariance_model_id` 当前仍不能写成：
  - `formalizable_now`
- `covariance_model_id` 当前可以写成：
  - `implementation_prep_candidate__not_closed`
- 当前最稳口径不是：
  - 直接决定具体协方差实现
- 当前最稳口径是：
  - 先冻结候选模型家族与最小输入要求
  - 当前已进一步推进到：
    - `candidate_model_family_frozen__not_ready`
    - `unique_model_frozen__not_ready`
    - `ready_judgement_conditional__downstream_still_locked`

## 一、当前字段状态

- 字段名：
  - `covariance_model_id`
- 所属层：
  - `portfolio_policy_inputs`
- 当前来源状态：
  - `future_only`
- 当前角色：
  - `风险模型选择标识`
- 当前阻塞位置：
  - `G5 / risk_model`

## 二、为什么现在进入判断页

- 原因 1：
  - `alpha_score` 已完成第一手正式代理合同冻结
- 原因 2：
  - 多家AI回收的第二共识就是：
    - 下一手应判断 `covariance_model_id` 是否进入实现前口径
- 原因 3：
  - 如果继续把它维持为纯黑盒，`target_weight / portfolio_tracking_error` 会一直无法判断

## 三、当前允许的候选模型家族

### 候选 1：基准相对 + 跟踪误差限制 + 约束优化主口径

- 来源依据：
  - `A_REQ_003_风险模型候选清单__20260715.md`
- 当前定位：
  - `推荐主口径`
- 含义：
  - 协方差模型服务于：
    - `benchmark`
    - `tracking_error_limit`
    - `active_return`
    - `constraint`
  - 这不是在宣布求解器已实现

### 候选 2：等权或市值权重 + 风险缩放降级口径

- 来源依据：
  - `A_REQ_003_风险模型候选清单__20260715.md`
- 当前定位：
  - `降级口径`
- 含义：
  - 若协方差模型不能进入实现前口径，则退回：
    - `equal_weight_or_value_weight + risk_overlay`

### 候选 3：纯均值-方差 / 协方差最优化

- 来源依据：
  - `A_REQ_003_风险模型候选清单__20260715.md`
- 当前定位：
  - `future_model`
- 含义：
  - 当前不作为第一顺位，不进入本轮实现前讨论

## 四、当前最小输入要求

- 当前若要把 `covariance_model_id` 纳入实现前口径，至少需要：
  - `portfolio_date`
  - `benchmark_id` 或明确 `nonbenchmark_mode`
  - `tracking_error_limit`
  - `active_risk_aversion`
  - 一份可声明的风险模型家族标识
- 当前不强行要求：
  - 协方差矩阵本体已实现
  - 历史估计窗口已实跑
  - shrinkage / factor model 参数已最终定稿

## 五、当前允许写法

- 允许写成：
  - `covariance_model_id 已进入实现前口径判断`
  - `covariance_model_id 当前仍未闭合，但已冻结候选模型家族`
  - `covariance_model_id 当前是 candidate_model_family_frozen__not_ready`

## 六、禁止误写

- 禁止写成：
  - `covariance_model_id 已 ready`
  - `协方差模型已闭合`
  - `target_weight 已可稳定生成`
  - `portfolio_tracking_error 已可正式输出`
  - `三段输出已自动解锁`
- 禁止把：
  - 候选模型家族
  写成：
  - `已确定唯一实现模型`
 - 禁止把：
  - `ready_judgement_conditional__downstream_still_locked`
  写成：
  - `risk_model_ready`
  - `ready for all downstream`

## 七、与下游的关系

- 当前这页能解决的是：
  - `covariance_model_id` 不再是纯黑盒
  - `target_weight / portfolio_tracking_error` 的前置条件开始可讨论
- 当前这页还没有解决：
  - 协方差模型最终选型
  - `target_weight` 最小生成链
  - `portfolio_tracking_error` 风险输出链
- 当前即便已推进到：
  - `ready_judgement_conditional__downstream_still_locked`
  也不代表：
  - 下游三段可自动升格

## 八、主负责人裁决

- 当前裁决不是：
  - 直接把 `covariance_model_id` 升格为已闭合输入
- 当前裁决是：
  - 允许它进入：
    - `候选模型家族冻结层`
  - 但状态当前保持：
    - `candidate_model_family_frozen__not_ready`
- 当前新增禁止性条款是：
  - 即便 `covariance_model_id` 已推进到：
    - `ready_judgement_conditional__downstream_still_locked`
  - 也只代表：
    - 风险模型上游判断已进入 conditional 层
  - 不代表：
    - `target_weight`
    - `portfolio_tracking_error`
    - `adjusted_position_weight`
    中任一段可自动解除 `not_output_passed`
- 这一步的价值在于：
  - 让总瓶颈不再只停在“可判断”
  - 但同时继续守住“不直接开实现”的边界

## 九、一句话口径

- 当前 `covariance_model_id` 的正确写法是：
  - `candidate_model_family_frozen__not_ready`

## 回链

- `A_REQ_003_风险模型候选清单__20260715.md`
- `A_REQ_003_最小验收口径__20260715.md`
- `A5_G5G6_多家AI回收记录与主负责人裁决__20260716.md`
- `A5_alpha_score_正式代理合同页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
- `A5_covariance_model_id_总瓶颈判断_多家AI回收记录与主负责人裁决__20260716.md`
- `A5_covariance_model_id_候选模型家族冻结页__20260716.md`
