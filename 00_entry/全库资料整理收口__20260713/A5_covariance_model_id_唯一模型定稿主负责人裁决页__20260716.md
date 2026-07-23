# A5 covariance_model_id 唯一模型定稿主负责人裁决页

更新时间：2026-07-16

## 用途

- 在唯一活动实现候选已冻结后，
  对“当前是否已足以写成唯一模型已冻结”给出主负责人正式裁决。
- 这页不是：
  - `risk_model_ready` 宣告页
  - 三段输出解锁页
- 这页只负责：
  - 把状态推进到 `unique_model_frozen__not_ready`
  - 说明为什么当前仍不能写成 `ready`

## 当前结论

- 当前 `covariance_model_id` 已足以从：
  - `sole_implementation_candidate_frozen__not_ready`
  继续推进到：
  - `unique_model_frozen__not_ready`
- 当前唯一模型冻结为：
  - `benchmark_relative_sample_covariance__CSI300__lookback60__a5_top_liquid_20__v1`
- 当前仍不是：
  - `risk_model_ready`
  - `outputs_unblocked`

## 一、为什么这次可以推进

- 原因 1：
  - 当前唯一活动实现候选已经明确到单一命名
- 原因 2：
  - 当前参数边界已经可冻结到：
    - `benchmark_id = CSI300`
    - `asset_universe_id = a5_top_liquid_20`
    - `lookback_days = 60`
    - `frequency = 1d`
    - `tracking_error_limit = 0.06`
    - `active_risk_aversion = 3.0`
- 原因 3：
  - 当前 fallback / observation 触发条件已可书面冻结，
    不再只是口头保留位

## 二、为什么当前仍不能写成 ready

- 当前已冻结的是：
  - 唯一模型
  - 参数边界
  - fallback 最小合同
- 当前仍未冻结的是：
  - `risk_model_ready` 判定页
  - 三段输出如何正式解除 `not_output_passed`
  - 更高一层的 ready 级验收
- 所以当前只能推进到：
  - `unique_model_frozen__not_ready`

## 三、当前保留项

- `shrinkage / structured covariance`：
  - 保留为 `fallback`
- `factor-implied covariance`：
  - 保留为 `observation`
- 当前都不再属于：
  - 当前主实现线

## 四、主负责人裁决

- 当前正式裁决为：
  - 冻结唯一模型状态为：
    - `unique_model_frozen__not_ready`
- 当前正式唯一模型为：
  - `benchmark_relative_sample_covariance__CSI300__lookback60__a5_top_liquid_20__v1`
- 当前下一手切到：
  - `covariance_model_id ready 判断准备`

## 五、一句话口径

- 当前 `covariance_model_id` 已从：
  - `sole_implementation_candidate_frozen__not_ready`
  推进到：
  - `unique_model_frozen__not_ready`

## 回链

- `A5_covariance_model_id_唯一模型最小合同页__20260716.md`
- `A5_covariance_model_id_唯一模型定稿准备页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
