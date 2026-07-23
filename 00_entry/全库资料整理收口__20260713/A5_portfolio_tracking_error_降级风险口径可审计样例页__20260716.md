# A5 portfolio_tracking_error 降级风险口径可审计样例页

更新时间：2026-07-18

## 用途

- 把 `portfolio_tracking_error` 当前第三缺口正式压成一页。
- 这页不宣布：
  - `portfolio_tracking_error output_passed`
  - `covariance_model_id ready`
- 这页只负责：
  - 冻结降级风险口径下 success / failure 两类可审计样例应该长什么样
  - 写清哪些字段必须保留
  - 说明补完这页后，下一手为何应切到单点升级判断

## 当前结论

- 当前 `portfolio_tracking_error` 仍只能写成：
  - `pass_conditions_drafted__not_output_passed`
- 但当前已经不是：
  - 只有 benchmark 口径与 covariance 输入层，没有可审计样例
- 当前可以正式写成：
  - `降级风险口径可审计样例已冻结`
- 因此当前最顺下一手不再是：
  - 继续补同层条件说明
- 而是：
  - 起 `portfolio_tracking_error` 单点升级判断包

## 一、success 样例最小结构

- success 样例至少必须带：
  - `portfolio_tracking_error`
  - `benchmark_id`
  - `target_weight_status = verified_with_degraded_risk__upstream_min_integration_verified__not_output_passed`
  - `covariance_model_id_status = ready_judgement_conditional__downstream_still_locked`
  - `risk_mode = degraded_risk_handling`
  - `benchmark_mode = true`
  - `tracking_error_limit`
  - `degrade_flags`
  - `audit_note`
- success 样例最关键的可审计断言是：
  - 输出明确来自降级风险口径
  - 没有假装正式风险模型已闭合
  - 没有引用未声明的正式协方差实现字段

## 二、failure 样例最小结构

- failure 样例至少必须带：
  - `portfolio_tracking_error = null`
  - `benchmark_id`
  - `risk_mode = degraded_risk_handling`
  - `benchmark_mode = true`
  - `degrade_flags`
  - `abort_reason`
  - `audit_note`
- failure 样例最关键的可审计断言是：
  - 失败原因必须可命名
  - 失败原因必须与输入缺口或边界触发器一致
  - 不得把 failure 写成“模型暂时没算出来”这类不可追溯表述

## 三、当前推荐的 success 样例口径

- 当前 success 样例允许写成：
  - `portfolio_tracking_error` 已生成最小可审计数值
  - `risk_mode = degraded_risk_handling`
  - `degrade_flags` 已显式展开
  - `covariance_model_id` 仅作为命名输入层存在
- 当前 success 样例不得写成：
  - 正式风险引擎输出
  - 正式协方差矩阵闭合结果

## 四、当前推荐的 failure 样例口径

- 当前 failure 样例推荐触发器至少覆盖：
  - 缺少 `benchmark_id`
  - 缺少 `tracking_error_limit`
  - 缺少 `covariance_model_id`
  - `target_weight` 状态回退到不可消费层
- 当前 failure 样例建议使用的最小 `abort_reason` 家族是：
  - `missing_benchmark_id`
  - `missing_tracking_error_limit`
  - `missing_covariance_model_id`
  - `upstream_target_weight_not_consumable`

## 五、当前必过清单

- 必过 1：
  - success 样例显式带 `risk_mode = degraded_risk_handling`
- 必过 2：
  - success 样例显式带 `degrade_flags`
- 必过 3：
  - success 样例没有把 `covariance_model_id` 写成 `ready`
- 必过 4：
  - failure 样例显式带 `abort_reason`
- 必过 5：
  - failure 样例的 `abort_reason` 可以和输入缺口逐条回链

## 六、越界即停清单

- 一旦出现以下任一条，当前 `portfolio_tracking_error` 升级判断不得继续外推：
  - success 样例隐含正式协方差矩阵已落地
  - success 样例依赖未声明风险预算逻辑
  - failure 样例没有明确 `abort_reason`
  - 输出文字把当前样例写成 `output_passed`

## 七、主负责人裁决

- 当前不做：
  - tracking error 正式通过裁决
  - runtime 风险引擎实现
- 当前正式裁决是：
  - `portfolio_tracking_error` 的三项最小缺口已全部推进到可判断层
  - 当前最顺下一手已切到：
    - `portfolio_tracking_error` 单点升级判断
- 原因：
  - benchmark 风险输出最小正式口径已冻结
  - `covariance_model_id` 最小输入层已冻结
  - 降级风险口径 success / failure 可审计样例已冻结

## 八、一句话口径

- 当前 `portfolio_tracking_error` 已不再只停在“条件可命名”，
  而是已补到：
  - `三项最小缺口均到可判断层`
- 但当前仍未到：
  - `output_passed`

## 八点五、2026-07-18 执行验证复位

- 本轮已新增真实 runtime 入口：
  - `02_runtime/a5_g5_portfolio_tracking_error_validation/`
- 本轮已实际执行：
  - success generation
  - failure generation
- 本轮复跑确认：
  - `portfolio_tracking_error = 0.005948`
  - `within_limit = true`
  - `observed_abort_reason = missing_tracking_error_limit`
- 这次执行新增证明的是：
  - success 样例显式风险输出已进入 hard 证据层
  - failure 样例 `abort_reason` 已进入可复现层
- 这次执行不新增宣称：
  - `output_passed`
  - `benchmark 风险输出 ready`

## 回链

- `A5_portfolio_tracking_error_最小通过条件页__20260716.md`
- `A5_portfolio_tracking_error_benchmark风险输出最小正式口径页__20260716.md`
- `A5_portfolio_tracking_error_covariance最小输入层页__20260716.md`
- `A5_portfolio_tracking_error_actual_generation_execution页__20260718.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
- `A5_G5_输出升格证据总表__20260716.tsv`
