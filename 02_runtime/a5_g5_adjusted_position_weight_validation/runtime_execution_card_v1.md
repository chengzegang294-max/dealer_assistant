# A5 G5 Adjusted Position Weight Validation Execution Card v1

## 生成入口

- 仓库级正式入口：
  - `00_entry/全库资料整理收口__20260713/A5_adjusted_position_weight_最终融合failure样例页__20260716.md`
  - `00_entry/全库资料整理收口__20260713/A5_adjusted_position_weight_actual_generation_execution页__20260718.md`
- `INDEX_NOTE`:
  - `02_runtime/a5_g5_adjusted_position_weight_validation/README.md`
  - `02_runtime/a5_g5_adjusted_position_weight_validation/artifact_index_v1.tsv`
- `GENERATOR`:
  - `02_runtime/a5_g5_adjusted_position_weight_validation/generate_adjusted_position_weight_v1.py`
  - `02_runtime/a5_g5_adjusted_position_weight_validation/run_covariance_target_weight_pte_apw_same_batch_v1.py`

## 当前范围

- 当前任务：
  - 冻结 success / failure / formula failure 最小输入模板
  - 完成 success / failure / formula failure 真实生成执行
  - 完成 `covariance -> target_weight -> portfolio_tracking_error -> adjusted_position_weight` 同轮串联执行
  - 回填 repo-global 执行页
- 当前输入：
  - `data/adjusted_position_weight_real_input_template_v1.json`
  - `data/adjusted_position_weight_real_input_failure_template_v1.json`
  - `data/adjusted_position_weight_real_input_formula_failure_template_v1.json`
- 当前输出：
  - `artifacts/adjusted_position_weight_validation/` 下的 latest JSON
  - `artifacts/adjusted_position_weight_validation/covariance_target_weight_pte_apw_same_batch_latest.json`

## 推荐运行顺序

1. 运行 success case
2. 运行 failure case
3. 运行 formula failure case
4. 回填 repo-global 执行页
5. 再判断是否还需要更强最终融合证据
6. 沿 same-batch 结果判断是否还需要继续回填 `G5` 主链页

## 当前增强结果

- success latest 当前已确认：
  - `upstream_generation_consumed = true`
  - `target_weight_generation_json` 已实际消费
  - `portfolio_tracking_error_generation_json` 已实际消费
- failure latest 当前已确认：
  - `observed_abort_reason = missing_target_weight_generation_json`
- formula failure latest 当前已确认：
  - `observed_abort_reason = final_size_scalar_below_abort_threshold`
  - 上游 success 产物已先被实际消费
- same-batch latest 当前已确认：
  - `covariance_target_weight_pte_chain_passed = true`
  - `apw_chain_passed = true`
  - 第三段当前已消费本轮 fresh 的 `pte_same_batch_success_latest.json`

## 当前最小命令入口

- success case:
  - `python 02_runtime/a5_g5_adjusted_position_weight_validation/generate_adjusted_position_weight_v1.py --input-json 02_runtime/a5_g5_adjusted_position_weight_validation/data/adjusted_position_weight_real_input_template_v1.json --output-json 02_runtime/a5_g5_adjusted_position_weight_validation/artifacts/adjusted_position_weight_validation/apw_actual_generation_success_latest.json`
- failure case:
  - `python 02_runtime/a5_g5_adjusted_position_weight_validation/generate_adjusted_position_weight_v1.py --input-json 02_runtime/a5_g5_adjusted_position_weight_validation/data/adjusted_position_weight_real_input_failure_template_v1.json --output-json 02_runtime/a5_g5_adjusted_position_weight_validation/artifacts/adjusted_position_weight_validation/apw_actual_generation_failure_latest.json`
- formula failure case:
  - `python 02_runtime/a5_g5_adjusted_position_weight_validation/generate_adjusted_position_weight_v1.py --input-json 02_runtime/a5_g5_adjusted_position_weight_validation/data/adjusted_position_weight_real_input_formula_failure_template_v1.json --output-json 02_runtime/a5_g5_adjusted_position_weight_validation/artifacts/adjusted_position_weight_validation/apw_actual_generation_failure_formula_latest.json`
- covariance -> target_weight -> pte -> apw same-batch:
  - `python 02_runtime/a5_g5_adjusted_position_weight_validation/run_covariance_target_weight_pte_apw_same_batch_v1.py`
