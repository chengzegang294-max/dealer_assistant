# A5 covariance_model_id 本体实跑输入装配页

更新时间：2026-07-16

## 用途

- 在 `candidate_model_family_frozen__not_ready` 与 template-level smoke-run 完成后，
  把下一手收缩到“第一手最小本体实跑输入装配”。
- 这页不做真正实跑。
- 这页只负责：
  - 冻结第一手要拼哪些输入
  - 写清先从哪条主候选装配
  - 写清哪些输入缺失会直接中止

## 当前结论

- 当前 `covariance_model_id` 已完成：
  - 候选模型家族冻结
  - success / failure template-level smoke-run
  - success / failure latest 输入装配
  - first fresh-run returns 输入构建
  - first fresh-run execution
- 当前最顺下一手不是：
  - 再扩候选家族
  - 直接开始多家族并跑
- 当前最顺下一手是：
  - 围绕已产出的输入包转入稳定性检查与唯一模型收敛准备

## 一、第一手输入包范围

- 当前第一手只装配：
  - `benchmark_relative_sample_covariance`
- 当前先不装配：
  - `shrinkage_structured_covariance`
  - `factor_implied_covariance`

## 二、必须字段

- 必须 1：
  - `portfolio_date`
- 必须 2：
  - `benchmark_id`
- 必须 3：
  - `asset_universe_id`
- 必须 4：
  - `returns_window_spec.lookback_days`
- 必须 5：
  - `returns_window_spec.frequency`
- 必须 6：
  - `tracking_error_limit`
- 必须 7：
  - `active_risk_aversion`

## 三、推荐最小默认值

- `benchmark_id`：
  - `CSI300`
- `asset_universe_id`：
  - `a5_top_liquid_20`
- `returns_window_spec.lookback_days`：
  - `60`
- `returns_window_spec.frequency`：
  - `1d`

## 四、直接中止条件

- 一旦出现以下任一条，当前输入装配必须中止：
  - `benchmark_id` 为空
  - `returns_window_spec` 缺失
  - `asset_universe_id` 为空
  - `lookback_days <= 0`

## 五、当前先做什么

- 当前先做：
  - 基于仓内 Tushare daily 资产生成 returns 输入 latest
  - 把输入装配正式吸收到 first fresh-run 执行页
- 当前暂缓：
  - PSD 修正
  - shrinkage 参数比较

## 六、一句话口径

- 当前 `covariance_model_id` 的输入装配已不再停在模板层，
  下一手已切到：
  - `first_fresh_run_completed__not_ready`

## 回链

- `A5_covariance_model_id_候选模型家族冻结页__20260716.md`
- `A5_covariance_model_id_本体实跑最小准备页__20260716.md`
- `A5_covariance_model_id_first_fresh_run执行页__20260716.md`
- `02_runtime/a5_g5_covariance_bodyrun/runtime_execution_card_v1.md`
