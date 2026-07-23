# A5 covariance_model_id 本体实跑最小准备页

更新时间：2026-07-16

## 用途

- 在候选模型家族冻结后，
  把下一手收缩到“本体实跑最小准备”。
- 这页不做真正实跑。
- 这页只负责：
  - 说明第一手实跑该跑什么
  - 说明当前不该一次性拉太宽
  - 冻结最小输入、最小输出与失败口径

## 当前结论

- 当前 `covariance_model_id` 已推进到：
  - `first_fresh_run_completed__not_ready`
- 当前最顺下一手不是：
  - 继续扩候选家族
  - 直接宣称实现前 ready
- 当前最顺下一手是：
  - 围绕已跑出的 first fresh-run 继续做最小稳定性检查
  - 并准备唯一模型收敛判断

## 一、第一顺位实跑对象

- 当前第一顺位只选：
  - `benchmark-relative sample covariance`
- 当前不同时并跑：
  - shrinkage
  - factor-implied covariance
- 原因：
  - 先用最窄主候选验证最小输入、最小输出、失败路径
  - 避免在本体实跑前重新扩面

## 二、最小输入

- 最少需要：
  - `portfolio_date`
  - `benchmark_id`
  - `asset_universe_id`
  - `returns_window_spec`
  - `tracking_error_limit`
  - `active_risk_aversion`

## 三、最小输出

- success 至少要带：
  - `covariance_model_id`
  - `candidate_family`
  - `window_spec`
  - `matrix_shape`
  - `diagonal_positive = true/false`
  - `is_psd = true/false`
  - `audit_note`
- failure 至少要带：
  - `covariance_model_id = null`
  - `candidate_family`
  - `abort_reason`
  - `audit_note`

## 四、推荐的最小 abort_reason

- 至少覆盖：
  - `missing_returns_window`
  - `insufficient_asset_history`
  - `matrix_not_psd`
  - `invalid_benchmark_context`

## 五、当前禁止扩写

- 禁止写成：
  - 已完成正式协方差实跑
  - 已完成唯一模型定稿
  - 已可解除三段输出的 not_output_passed

## 六、主负责人裁决

- 当前正式裁决是：
  - 候选家族冻结后，下一手已收缩到：
    - `本体实跑最小准备`
- 当前已完成：
  - `benchmark_relative_sample_covariance` 的 success / failure template-level smoke-run
  - `benchmark_relative_sample_covariance` 的 success / failure latest 输入装配
  - `benchmark_relative_sample_covariance` 的 first fresh-run preflight 已通过
  - `benchmark_relative_sample_covariance` 的 first fresh-run
- 当前暂缓：
  - 多家族并跑
  - 唯一模型定稿
  - ready 宣称

## 七、一句话口径

- 当前 `covariance_model_id` 的下一手已不是转入 first fresh-run execution prep，
  而是：
  - 转入最小稳定性检查与唯一模型收敛准备

## 回链

- `A5_covariance_model_id_候选模型家族冻结页__20260716.md`
- `A5_covariance_model_id_总瓶颈判断准备页__20260716.md`
- `A5_covariance_model_id_本体实跑输入装配页__20260716.md`
- `A5_covariance_model_id_first_fresh_run前检查页__20260716.md`
- `A5_covariance_model_id_first_fresh_run执行页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
