# A5 G5 min chain execution 页

更新时间：2026-07-18

## 用途

- 把 `G5` 三段输出的最小串联执行正式收口到 repo-global。
- 这页不直接宣布：
  - `output_passed`
  - `G5 implementation ready`
- 这页只回答：
  - 三段当前是否已经能顺序执行
  - success 链最后跑到哪
  - failure 链最先停在哪

## 当前结论

- 当前 `G5` 已经不是：
  - 只有分段执行证据
- 当前已经推进到：
  - `minimum chained execution completed`
- 当前 success 链已完成：
  - `target_weight -> portfolio_tracking_error -> adjusted_position_weight`
- 当前 failure 链已确认两条：
  - 会在 `portfolio_tracking_error` 的协方差输入缺失处中止
  - 也会在 `adjusted_position_weight` 的最终融合阈值处按合同中止

## 一、success 链结果

- 产物：
  - `a5_g5_min_chain_success_latest.json`
- 当前可确认：
  - `chain_completed = true`
  - `final_step = adjusted_position_weight`
  - `final_status = success`
- success 链中实际发生的是：
  - `target_weight` 生成成功
  - `portfolio_tracking_error` 实际消费 `covariance_matrix_latest.csv`
  - `adjusted_position_weight` 实际消费前两段真实产物

## 二、`pte_failure` 链结果

- 产物：
  - `a5_g5_min_chain_pte_failure_latest.json`
- 当前可确认：
  - `chain_completed = false`
  - `final_step = portfolio_tracking_error`
  - `observed_abort_reason = missing_covariance_matrix_csv`
- 这说明当前链级 failure 不是“无定义失败”，而是：
  - 上游 `target_weight` 成功后
  - 在 `portfolio_tracking_error` 协方差输入缺失处按合同中止

## 三、`apw_failure` 链结果

- 产物：
  - `a5_g5_min_chain_apw_failure_latest.json`
- 当前可确认：
  - `chain_completed = false`
  - `final_step = adjusted_position_weight`
  - `observed_abort_reason = final_size_scalar_below_abort_threshold`
- 这说明当前第三段 failure 也不是“黑盒失败”，而是：
  - 上游 `target_weight` success 已先完成
  - `portfolio_tracking_error` success 已先完成
  - 最后在 `adjusted_position_weight` 的公式阈值处按合同中止

## 四、这轮完成后当前能写到哪

- 允许写成：
  - `G5` 已具备最小串联执行证据
  - `G5` 三段已开始形成真实上下游消费
  - `G5` 当前已有 success / `pte_failure` / `apw_failure` 三条链级 hard 产物
- 且当前又新增：
  - 第三段 same-batch success 已消费本轮 fresh 的 `pte_same_batch_success_latest.json`
  - 因而当前三段已具备从 `covariance` 一路下探到 `adjusted_position_weight` 的同轮串联消费证据
  - 且链级 boundary audit 已确认三段 frozen 边界当前都已 `runtime_backed = true`
  - 且 `adjusted_position_weight` 的解除 `not_output_passed` 正式边界已由运行事实补裁冻结
- 仍不能写成：
  - `output_passed`
  - `G5 implementation ready`
  - `正式组合输出已闭合`

## 五、主负责人裁决

- 当前选：
  - 把 `minimum chained execution completed + 双 failure 停点合同化` 视为本轮最值钱新增证据
- 为什么选这个：
  - 因为它把三段从“各自可跑”推进到了“能顺序串起来跑”
  - 且 failure 已不再只有一个停点，而是被压到两个明确合同停点
- 为什么不直接写成 `output_passed`：
  - 当前仍是最小降级链
  - 当前仍缺更强执行证据与总闭合判断
- 当前先做什么：
  - 回到 `covariance_model_id -> target_weight validation` 这条最短执行主线
  - 继续补更强显式运行记录与失败路径一致性

## 六、一句话口径

- 当前 `G5` 已从“分段 execution completed”继续推进到：
  - `minimum chained execution completed`
- 且当前链级 failure 已明确覆盖到：
  - `portfolio_tracking_error`
  - `adjusted_position_weight`
- 但当前仍未到：
  - `output_passed`

## 回链

- `A5_G5主链闭合状态页__20260716.md`
- `A5_G5_输出闭合判断页__20260716.md`
- `A5_target_weight_actual_generation_execution页__20260716.md`
- `A5_portfolio_tracking_error_actual_generation_execution页__20260718.md`
- `A5_adjusted_position_weight_actual_generation_execution页__20260718.md`
- `A5_adjusted_position_weight解除not_output_passed正式边界_运行事实补裁页__20260723.md`
- `02_runtime/a5_g5_min_chain_validation/README.md`
