# A5 G5 Portfolio Tracking Error Validation Execution Card v1

## 生成入口

- 仓库级正式入口：
  - `00_entry/全库资料整理收口__20260713/A5_portfolio_tracking_error_降级风险口径可审计样例页__20260716.md`
  - `00_entry/全库资料整理收口__20260713/A5_portfolio_tracking_error_actual_generation_execution页__20260718.md`
- `INDEX_NOTE`:
  - `02_runtime/a5_g5_portfolio_tracking_error_validation/README.md`
  - `02_runtime/a5_g5_portfolio_tracking_error_validation/artifact_index_v1.tsv`
- `GENERATOR`:
  - `02_runtime/a5_g5_portfolio_tracking_error_validation/generate_portfolio_tracking_error_v1.py`
  - `02_runtime/a5_g5_portfolio_tracking_error_validation/run_covariance_target_weight_pte_same_batch_v1.py`

## 当前范围

- 当前任务：
  - 冻结 success / failure 最小输入模板
  - 完成 success / failure 真实生成执行
  - 完成 `covariance -> target_weight -> portfolio_tracking_error` 同轮串联执行
  - 回填 repo-global 执行页
- 当前输入：
  - `data/portfolio_tracking_error_real_input_template_v1.json`
  - `data/portfolio_tracking_error_real_input_failure_template_v1.json`
- 当前输出：
  - `artifacts/portfolio_tracking_error_validation/` 下的 latest JSON
  - `artifacts/portfolio_tracking_error_validation/covariance_target_weight_pte_same_batch_latest.json`

## 当前作用

- 把 repo-global 的样例口径接到实际 runtime 入口。
- 让 `portfolio_tracking_error` 的 success / failure 证据不再只停在文档层。
- 当前只验证：
  - 显式风险输出是否可生成
  - `covariance_matrix_latest.csv` 是否被实际消费
  - `abort_reason` 是否一致
- 当前不验证：
  - 正式风险模型
  - 正式 tracking error 实现
  - 输出升格通过

## 推荐运行顺序

1. 运行 success case
2. 运行 failure case
3. 回填 repo-global 执行页
4. 再决定是否继续补 portfolio_tracking_error 的更强执行证据
5. 沿 same-batch 结果判断是否继续顺接到 `adjusted_position_weight`

## 当前增强结果

- success latest 当前已确认：
  - `calculation_method = active_weight_covariance_quadratic_proxy`
  - `covariance_matrix_consumed = true`
- failure latest 当前已确认：
  - `observed_abort_reason = missing_covariance_matrix_csv`
- same-batch latest 当前已确认：
  - `covariance_target_weight_chain_passed = true`
  - `pte_chain_passed = true`
  - `same_batch_generated_weight_count = 3`

## 当前最小命令入口

- success case:
  - `python 02_runtime/a5_g5_portfolio_tracking_error_validation/generate_portfolio_tracking_error_v1.py --input-json 02_runtime/a5_g5_portfolio_tracking_error_validation/data/portfolio_tracking_error_real_input_template_v1.json --output-json 02_runtime/a5_g5_portfolio_tracking_error_validation/artifacts/portfolio_tracking_error_validation/pte_actual_generation_success_latest.json`
- failure case:
  - `python 02_runtime/a5_g5_portfolio_tracking_error_validation/generate_portfolio_tracking_error_v1.py --input-json 02_runtime/a5_g5_portfolio_tracking_error_validation/data/portfolio_tracking_error_real_input_failure_template_v1.json --output-json 02_runtime/a5_g5_portfolio_tracking_error_validation/artifacts/portfolio_tracking_error_validation/pte_actual_generation_failure_latest.json`
- covariance -> target_weight -> pte same-batch:
  - `python 02_runtime/a5_g5_portfolio_tracking_error_validation/run_covariance_target_weight_pte_same_batch_v1.py`

## 当前产物边界

- `data/`:
  - 放模板，不放运行结果
- `artifacts/`:
  - 放真实运行结果
- 当前不把 runtime 结果直接写成：
  - `output_passed`
