# Target Weight Actual Generation Execution Summary v1

## 用途

- 记录 `target_weight` 最小 actual generation execution 的 success/failure 两条运行结果。
- 这页不宣布：
  - `output_passed`
- 这页只确认：
  - 最小生成器已实际执行
  - success/failure 路径都有 hard 产物

## 当前结果

- success 产物：
  - `artifacts/target_weight_validation/tw_actual_generation_success_latest.json`
- failure 产物：
  - `artifacts/target_weight_validation/tw_actual_generation_failure_latest.json`
- 生成入口：
  - `generate_target_weight_v1.py`

## success 路径

- 输入：
  - `data/target_weight_real_input_template_v1.json`
- 结果：
  - `generation_executed = true`
  - `weight_count = 3`
  - `within_bounds = true`
  - `allocation_method = alpha_proportional_with_single_name_cap`

## failure 路径

- 输入：
  - `data/target_weight_real_input_failure_template_v1.json`
- 结果：
  - `generation_executed = false`
  - `observed_abort_reason = missing_constraint_set`

## 当前正确写法

- 允许写成：
  - `actual generation execution 已完成`
  - `success / failure 两条生成执行路径都有 hard 产物`
- 不允许写成：
  - `target_weight = output_passed`
  - `正式优化器已 ready`

## 下一手

- 当前下一手不再是：
  - 补生成执行证据
- 当前下一手是：
  - 基于这批新证据重开 `target_weight` 升格裁决
