# A5 covariance_model_id first fresh-run 前检查页

更新时间：2026-07-16

## 用途

- 在 `first fresh-run 入口准备` 之后，
  把下一手正式推进到：
  - `first fresh-run 前检查`
- 这页不做真正 fresh-run。
- 这页只负责：
  - 把前检查对象固定成可执行清单
  - 记录 first preflight latest 是否已跑出
  - 明确通过后下一手该进哪一层

## 当前结论

- 当前 `covariance_model_id` 已完成：
  - `first_fresh_run_completed__not_ready`
  - success / failure template-level smoke-run
  - success / failure latest 输入装配
  - first fresh-run preflight 已通过
  - `benchmark_relative_sample_covariance` 的 first fresh-run
- 当前 first preflight 统一只检查：
  - `benchmark_relative_sample_covariance`
- 当前 first preflight 已被真实执行吸收，
  下一手已进一步收缩到：
  - `minimum_stability_checked__not_ready`
- 当前还不是：
  - `fresh-run completed`
  - `risk model ready`

## 一、前检查固定对象

- `runtime_params_template`
  - `02_runtime/a5_g5_covariance_bodyrun/covariance_bodyrun_runtime_params_template_v1.json`
- `success input assembly latest`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_input/covariance_bodyrun_input_success_latest.json`
- `failure input assembly latest`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_input/covariance_bodyrun_input_failure_latest.json`
- `success prep smoke-run latest`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun/covariance_bodyrun_success_latest.json`
- `failure prep smoke-run latest`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun/covariance_bodyrun_failure_latest.json`
- `preflight latest`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_preflight/covariance_bodyrun_preflight_latest.json`

## 二、当前必过项

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
  - failure input assembly latest 仍固定：
    - `abort_reason = invalid_benchmark_context`
- 必过 8：
  - success / failure prep smoke-run 都仍保持：
    - `validation_passed = true`
- 必过 9：
  - 仍明确保留：
    - `not_ready__do_not_claim_body_matrix_run_completed`

## 三、主负责人裁决

- 当前先做什么：
  - 把 preflight 已通过这一层正式吸收到 first fresh-run 执行页
- 当前为什么先做这个：
  - 因为 preflight 已不再是停点，
    当前更值钱的是围绕 first fresh-run 结果做后续稳定性与唯一模型收敛判断
- 当前不做什么：
  - 不直接声称协方差矩阵 fresh-run 已完成
  - 不直接开启多家族并跑
  - 不直接宣称风险模型 ready

## 四、一句话口径

- 当前 `covariance_model_id` 已完成：
  - `first fresh-run preflight`
  - `first fresh-run execution`
- 当前下一手已切到：
  - `最小稳定性检查执行`

## 回链

- `A5_covariance_model_id_first_fresh_run入口准备页__20260716.md`
- `A5_covariance_model_id_first_fresh_run外部输入包清单页__20260716.md`
- `A5_covariance_model_id_first_fresh_run执行页__20260716.md`
- `A5_covariance_model_id_最小稳定性检查执行页__20260716.md`
- `A5_covariance_model_id_本体实跑最小准备页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
- `02_runtime/a5_g5_covariance_bodyrun/covariance_bodyrun_preflight_checklist_v1.md`
