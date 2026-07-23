# A5 covariance_model_id 唯一模型最小合同页

更新时间：2026-07-16

## 用途

- 在 `sole_implementation_candidate_frozen__not_ready` 后，
  把当前唯一模型定稿所依赖的最小合同正式冻结成一页。
- 这页不是：
  - `risk_model_ready` 宣告页
  - 多家族对比讨论页
- 这页只负责：
  - 冻结当前唯一模型命名
  - 冻结当前参数边界
  - 冻结当前 fallback / observation 触发条件

## 当前结论

- 当前唯一模型最小合同冻结为：
  - `benchmark_relative_sample_covariance__CSI300__lookback60__a5_top_liquid_20__v1`
- 当前唯一模型口径只覆盖：
  - `benchmark_id = CSI300`
  - `asset_universe_id = a5_top_liquid_20`
  - `lookback_days = 60`
  - `frequency = 1d`
  - `tracking_error_limit = 0.06`
  - `active_risk_aversion = 3.0`
- 当前仍不是：
  - `risk_model_ready`
  - `outputs_unblocked`

## 一、唯一模型正式命名

- 当前正式 `covariance_model_id`：
  - `benchmark_relative_sample_covariance__CSI300__lookback60__a5_top_liquid_20__v1`
- 生成入口回指：
  - `02_runtime/a5_g5_covariance_bodyrun/run_covariance_bodyrun_fresh_v1.py`
- latest 证据回指：
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_fresh/covariance_bodyrun_fresh_latest.json`

## 二、参数边界最小合同

- 当前固定不改：
  - `candidate_model_family = benchmark_relative_sample_covariance`
  - `benchmark_id = CSI300`
  - `asset_universe_id = a5_top_liquid_20`
  - `returns_window_spec.lookback_days = 60`
  - `returns_window_spec.frequency = 1d`
  - `tracking_error_limit = 0.06`
  - `active_risk_aversion = 3.0`
- 当前运行结果最小验收：
  - `matrix_shape = [20, 20]`
  - `asset_count = 20`
  - `effective_trade_dates = 60`
  - `diagonal_positive = true`
  - `is_psd = true`
  - `min_eigenvalue >= 0` 或近似非负

## 三、稳定性边界最小合同

- 当前至少要求：
  - current / adjacent 两窗口都能跑通
  - `stability_check_passed = true`
  - `relative_trace_gap <= 0.60`
- 当前已满足：
  - `relative_trace_gap = 0.3521095040180391`
  - `scale_gap_within_guardrail = true`
- 当前不把以下内容写入最小合同：
  - 更长窗口多段扫描
  - shrinkage 参数寻优
  - factor model 参数定稿

## 四、fallback / observation 触发条件

### 重开 `shrinkage / structured covariance`

- 若出现以下任一情况，则允许从 fallback 位重开：
  - `is_psd = false`
  - `diagonal_positive = false`
  - `effective_trade_dates < 60`
  - `asset_count != 20`
  - `relative_trace_gap > 0.60`
  - 相邻窗口稳定性检查失败

### 重开 `factor-implied covariance`

- 只有在以下条件出现时才值得重开观察位：
  - 组合层明确新增“解释性/降维”硬要求
  - 当前 sample covariance 与 shrinkage fallback 都无法满足主线稳定性需要
- 当前未出现上述条件，因此：
  - `factor-implied covariance` 继续只保留观察位

## 五、当前允许写法

- 允许写成：
  - `唯一模型最小合同已冻结`
  - `unique_model_frozen__not_ready`
  - `benchmark_relative_sample_covariance` 已是当前唯一模型
- 禁止写成：
  - `risk_model_ready`
  - `正式风险模型已通过`
  - `三段输出已解锁`

## 六、主负责人裁决

- 当前正式裁决为：
  - 把当前唯一模型最小合同冻结到文档层
  - 把其它家族正式降格为：
    - `fallback`
    - `observation`
- 当前下一手切到：
  - `covariance_model_id ready 判断准备`

## 七、一句话口径

- 当前 `covariance_model_id` 已完成：
  - `唯一模型最小合同冻结`
- 但当前仍停在：
  - `unique_model_frozen__not_ready`

## 回链

- `A5_covariance_model_id_唯一模型收敛主负责人裁决页__20260716.md`
- `A5_covariance_model_id_唯一模型定稿准备页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
