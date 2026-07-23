# A5 G5 Covariance Body Run Preflight Checklist v1

## 用途

- 把 `covariance_model_id` 的 `first fresh-run 入口前检查` 固定成可复跑清单。
- 当前只检查：
  - runtime 参数边界是否仍与冻结口径一致
  - success / failure latest 输入装配是否齐备
  - success / failure template-level smoke-run 结果是否齐备
- 当前不等于：
  - 协方差矩阵本体 fresh-run 已完成
  - 风险模型已 ready

## 当前检查对象

- `covariance_bodyrun_runtime_params_template_v1.json`
- `artifacts/covariance_bodyrun_input/covariance_bodyrun_input_success_latest.json`
- `artifacts/covariance_bodyrun_input/covariance_bodyrun_input_failure_latest.json`
- `artifacts/covariance_bodyrun/covariance_bodyrun_success_latest.json`
- `artifacts/covariance_bodyrun/covariance_bodyrun_failure_latest.json`

## 必过项

- 必过 1：
  - `candidate_model_family = benchmark_relative_sample_covariance`
- 必过 2：
  - `benchmark_id != ""`
- 必过 3：
  - `asset_universe_id != ""`
- 必过 4：
  - `returns_window_spec.lookback_days > 0`
- 必过 5：
  - `returns_window_spec.frequency != ""`
- 必过 6：
  - success input assembly latest 与 runtime params 一致
- 必过 7：
  - failure input assembly latest 仍保持 `invalid_benchmark_context`
- 必过 8：
  - success / failure prep smoke-run 都保持 `validation_passed = true`
- 必过 9：
  - `notes` 仍明确标注：
    - `not_ready__do_not_claim_body_matrix_run_completed`

## 最小命令入口

- `python 02_runtime/a5_g5_covariance_bodyrun/run_covariance_bodyrun_preflight_v1.py --runtime-params-json 02_runtime/a5_g5_covariance_bodyrun/covariance_bodyrun_runtime_params_template_v1.json --success-assembly-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_input/covariance_bodyrun_input_success_latest.json --failure-assembly-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_input/covariance_bodyrun_input_failure_latest.json --success-prep-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun/covariance_bodyrun_success_latest.json --failure-prep-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun/covariance_bodyrun_failure_latest.json --output-json 02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_preflight/covariance_bodyrun_preflight_latest.json`

## 当前裁决

- 当前 preflight 只服务于：
  - `benchmark_relative_sample_covariance`
- 当前通过后，下一手才允许推进到：
  - `first fresh-run execution prep`
- 当前即使 preflight 通过，也仍不能写成：
  - `fresh-run completed`
  - `risk model ready`

## 回链

- `runtime_execution_card_v1.md`
- `runtime_provenance_note_v1.md`
- `../../00_entry/全库资料整理收口__20260713/A5_covariance_model_id_first_fresh_run入口准备页__20260716.md`
