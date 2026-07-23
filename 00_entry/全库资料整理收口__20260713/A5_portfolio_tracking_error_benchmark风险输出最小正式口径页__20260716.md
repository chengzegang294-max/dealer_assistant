# A5 portfolio_tracking_error benchmark 风险输出最小正式口径页

更新时间：2026-07-16

## 用途

- 把 `portfolio_tracking_error` 当前最值钱的缺口先压成一页。
- 这页不宣布：
  - 已有正式 tracking error 输出值
  - 风险模型已 ready
- 这页只负责：
  - 冻结 benchmark 风险输出当前最小正式口径
  - 说明降级风险模式下允许写到哪
  - 给后续 `covariance_model_id` 与样例页留下统一入口

## 当前结论

- 当前 `portfolio_tracking_error` 仍不能写成：
  - `output_passed`
- 当前可以先正式写成：
  - benchmark 风险输出最小正式口径已冻结
- 当前最小口径只要求：
  - 存在 `benchmark_id`
  - 存在 `target_weight`
  - 存在可命名风险口径来源
  - 存在 `tracking_error_limit`

## 一、最小输入口径

- 输入 1：
  - `benchmark_id`
- 输入 2：
  - `target_weight`
  - 当前允许其状态为：
    - `verified_with_degraded_risk__upstream_min_integration_verified__not_output_passed`
- 输入 3：
  - 风险口径来源：
    - `degraded_risk_handling`
    - 或 `covariance_model_id under_judgement`
- 输入 4：
  - `tracking_error_limit`

## 二、最小输出口径

- 输出必须至少带：
  - `portfolio_tracking_error`
  - `risk_mode`
  - `benchmark_mode = true`
  - `degrade_flags`
  - 若失败则带：
    - `abort_reason`

## 三、当前允许写法

- 允许写成：
  - 当前已具备 `benchmark` 风险输出最小正式口径
  - 当前风险输出仍处于降级模式约束下
  - 当前 tracking error 仍未通过正式输出升格

## 四、当前禁止误写

- 禁止写成：
  - `benchmark 风险输出已 ready`
  - `covariance_model_id 已正式闭合`
  - `portfolio_tracking_error 已可正式消费`

## 五、当前先做什么

- 当前先做：
  - 以这页为入口，后续再补：
    - `covariance_model_id` 最小输入层
- 当前该页补完后的下一手是：
  - `降级风险口径可审计样例`
- 当前暂缓：
  - 直接发起 `portfolio_tracking_error` 升格裁决

## 六、一句话口径

- 当前 `portfolio_tracking_error` 的最小正式推进不是数值闭合，
  而是先冻结：
  - `benchmark 风险输出最小正式口径`
