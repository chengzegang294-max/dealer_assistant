# A5 covariance_model_id 唯一模型收敛主负责人裁决页

更新时间：2026-07-16

## 用途

- 在 `minimum_stability_checked__not_ready` 后，
  对 `covariance_model_id` 是否已足以继续收敛为“唯一活动实现候选”给出主负责人书面裁决。
- 这页不是：
  - `risk_model_ready` 宣告页
  - 唯一模型最终定稿页
- 这页只负责：
  - 给出当前唯一活动实现候选
  - 说明为什么此时不再继续并跑其它家族
  - 说明为什么当前仍不是 `ready`

## 当前结论

- 当前 `covariance_model_id` 已足以从：
  - `minimum_stability_checked__not_ready`
  继续推进到：
  - `sole_implementation_candidate_frozen__not_ready`
- 当前唯一活动实现候选冻结为：
  - `benchmark_relative_sample_covariance`
- 当前仍不是：
  - `unique_model_frozen`
  - `risk_model_ready`
  - `outputs_unblocked`

## 一、当前为什么选它

- 原因 1：
  - 它是当前唯一已经完成：
    - current 窗口 fresh-run
    - adjacent 窗口 fresh-run
    - 最小稳定性检查
    的家族
- 原因 2：
  - 它与当前 `portfolio_tracking_error` 的 benchmark 风险输出链口径最一致
- 原因 3：
  - 当前所有 runtime、输入装配、fresh-run 与 stability 证据都已围绕：
    - `benchmark_id = CSI300`
    - `asset_universe_id = a5_top_liquid_20`
    - `lookback_days = 60`
    - `frequency = 1d`
    形成闭环

## 二、为什么当前不继续并跑另外两家族

### `shrinkage / structured covariance`

- 当前仍只具备：
  - 结构性备选意义
- 当前不具备：
  - 仓内 first fresh-run
  - 相邻窗口稳定性检查
  - 下游三段输出对其的硬依赖
- 因此当前处理为：
  - `保留为备选 fallback 家族`
  - `不进入当前唯一活动实现线`

### `factor-implied covariance`

- 当前仍只具备：
  - 解释性与维度压缩的观察位意义
- 当前不具备：
  - 仓内 runtime 证据
  - 当前组合层主线的硬前置需求
- 因此当前处理为：
  - `保留为观察位`
  - `不进入当前唯一活动实现线`

## 三、为什么能推进但仍 not_ready

- 当前已证明：
  - 唯一活动实现候选已经足够收缩到单家族
- 当前仍未证明：
  - 该家族已经完成唯一模型定稿
  - 参数边界与 fallback 触发条件已冻结
  - 三段输出已可据此解除 `not_output_passed`
- 所以当前只能推进到：
  - `sole_implementation_candidate_frozen__not_ready`

## 四、主负责人裁决

- 当前正式裁决为：
  - 冻结 `benchmark_relative_sample_covariance` 为：
    - `唯一活动实现候选`
- 当前同时保留：
  - `shrinkage / structured covariance = fallback 备选`
  - `factor-implied covariance = 观察位`
- 当前不再做：
  - 多家族同步并跑
  - 把其它家族继续放在当前主实现线上

## 五、当前先做什么

- 当前先做：
  - 把状态正式回填为：
    - `sole_implementation_candidate_frozen__not_ready`
  - 把下一手切到：
    - `唯一模型定稿准备`

## 六、一句话口径

- 当前 `covariance_model_id` 已完成：
  - `唯一活动实现候选冻结`
- 但当前仍未完成：
  - `唯一模型定稿`
  - `risk_model_ready`

## 回链

- `A5_covariance_model_id_唯一模型收敛准备页__20260716.md`
- `A5_covariance_model_id_最小稳定性检查执行页__20260716.md`
- `A5_covariance_model_id_候选模型家族冻结页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
