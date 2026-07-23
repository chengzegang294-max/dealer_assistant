# A5 portfolio_tracking_error actual generation execution 页

更新时间：2026-07-18

## 用途

- 把 `portfolio_tracking_error` 的最小 actual generation execution 正式收口到 repo-global。
- 这页不直接宣布：
  - `output_passed`
  - `benchmark 风险输出 ready`
- 这页只回答：
  - 显式风险输出是否真的生成过
  - success / failure 两条路径是否都有 hard 证据
  - 当前执行线能写到哪

## 当前结论

- 当前 `portfolio_tracking_error` 仍只能写成：
  - `pass_conditions_frozen__not_output_passed`
- 但当前已经不是：
  - 只停在样例口径冻结
- 当前已经推进到：
  - `actual generation execution completed`
- 因此当前最顺下一手不再是：
  - 继续补 `portfolio_tracking_error` 的最小 runtime 入口
- 而是：
  - 再决定是否继续补更强的风险输出执行证据

## 一、success 生成执行

- 输入：
  - `portfolio_tracking_error_real_input_template_v1.json`
- 产物：
  - `pte_actual_generation_success_latest.json`
- 当前可确认：
  - `generation_executed = true`
  - `portfolio_tracking_error = 0.00012553`
  - `tracking_error_limit = 0.03`
  - `within_limit = true`
  - `calculation_method = active_weight_covariance_quadratic_proxy`
  - `covariance_matrix_consumed = true`
  - `overlap_symbol_count = 3`

## 二、failure 生成执行

- 输入：
  - `portfolio_tracking_error_real_input_failure_template_v1.json`
- 产物：
  - `pte_actual_generation_failure_latest.json`
- 当前可确认：
  - `generation_executed = false`
  - `observed_abort_reason = missing_covariance_matrix_csv`

## 三、这轮完成后当前能写到哪

- 允许写成：
  - `portfolio_tracking_error` 已具备最小 actual generation execution 证据
  - success / failure 两条路径都有 hard 产物
  - 显式风险输出与 `abort_reason` 已进入可复现层
  - success 样例已实际消费 `covariance_matrix_latest.csv`
- 仍不能写成：
  - `output_passed`
  - `benchmark 风险输出 ready`
  - `covariance_model_id ready`

## 四、主负责人裁决

- 当前选：
  - 把 `actual generation execution` 视为已完成的最小新增执行证据
- 为什么选这个：
  - 因为 success / failure 两条路径都已具备 hard 产物
  - 且 success 样例已经不再只是口头样例，而是脚本生成并实际消费协方差矩阵的显式风险输出
- 为什么不直接写成 `output_passed`：
  - 当前仍是 `degraded_risk_handling`
  - 当前仍是降级链执行，不是正式风险引擎闭合
- 当前先做什么：
  - 把串联执行主线继续切到 `adjusted_position_weight`

## 五、一句话口径

- 当前 `portfolio_tracking_error` 已从“样例冻结”继续推进到：
  - `actual generation execution completed`
- 但当前仍未到：
  - `output_passed`

## 六、2026-07-18 更强执行证据

- 本轮已把 success 计算从：
  - `half_l1_active_weight_proxy`
  升到：
  - `active_weight_covariance_quadratic_proxy`
- 本轮已显式消费：
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_fresh/covariance_matrix_latest.csv`
- 这意味着当前 `portfolio_tracking_error` 已不再只是 benchmark 权重差 proxy，
  而是已开始实际消费上游风险矩阵产物

## 七、2026-07-18 同轮串联批次执行

- 本轮已新增同轮 hard 汇总产物：
  - `02_runtime/a5_g5_portfolio_tracking_error_validation/artifacts/portfolio_tracking_error_validation/covariance_target_weight_pte_same_batch_latest.json`
- 当前批次已确认：
  - `covariance_target_weight_chain_passed = true`
  - `pte_chain_passed = true`
  - `same_batch_generated_weight_count = 3`
- 当前 success 已进一步确认：
  - `portfolio_tracking_error` 使用的 `target_weight_entries`
    来自本轮 fresh 的
    `tw_actual_generation_success_latest.json`
  - 不再只是静态模板抄写权重
- 当前 failure 已进一步确认：
  - 即便 `target_weight generated_weights` 已同轮注入，
    仍会在 `covariance_matrix_csv` 缺失处按合同中止
- 这次批次执行新增证明的是：
  - `portfolio_tracking_error` 已具备
    `covariance -> target_weight -> portfolio_tracking_error`
    的同轮串联消费证据
  - 上游 `target_weight actual generation` 当前已被下游风险输出实际消费
- 这次批次执行仍不新增宣称：
  - `output_passed`
  - `benchmark 风险输出 ready`
  - `covariance_model_id ready`

## 八、2026-07-18 same-batch 下游继续消费

- 本轮又已确认：
  - `pte_same_batch_success_latest.json`
    已被 `adjusted_position_weight` 的 same-batch success / formula failure 两条路径实际消费
- 这意味着第二段当前不只具备：
  - `covariance -> target_weight -> portfolio_tracking_error`
    的 same-batch 证据
- 还具备：
  - 被第三段 same-batch 继续向下消费的证据
- 但这仍不新增宣称：
  - `output_passed`
  - `portfolio_tracking_error ready`

## 回链

- `A5_portfolio_tracking_error_降级风险口径可审计样例页__20260716.md`
- `02_runtime/a5_g5_portfolio_tracking_error_validation/README.md`
- `02_runtime/a5_g5_portfolio_tracking_error_validation/runtime_execution_card_v1.md`
