# A5 covariance_model_id first fresh-run 入口准备页

更新时间：2026-07-16

## 用途

- 在候选家族冻结、template-level smoke-run 与 first latest 输入装配完成后，
  把下一手正式收缩到 `first fresh-run` 的入口准备。
- 这页不等于已经 fresh-run。
- 这页只负责：
  - 冻结 first fresh-run 入口参数
  - 写清进入前检查项
  - 明确当前仍不能宣称 ready

## 当前结论

- 当前 `covariance_model_id` 已完成：
  - `first_fresh_run_completed__not_ready`
  - success / failure template-level smoke-run
  - success / failure latest 输入装配
  - first fresh-run preflight 已通过
  - `benchmark_relative_sample_covariance` 的 first fresh-run
- 当前最顺下一手是：
  - 这页的入口职责已完成，
    当前主线已继续推进到：
    - `minimum_stability_checked__not_ready`
- 当前还不是：
  - `fresh-run completed`
  - `risk model ready`

## 一、入口参数最小集

- `candidate_model_family`
  - `benchmark_relative_sample_covariance`
- `portfolio_date`
  - `2026-07-16`
- `benchmark_id`
  - `CSI300`
- `asset_universe_id`
  - `a5_top_liquid_20`
- `returns_window_spec.lookback_days`
  - `60`
- `returns_window_spec.frequency`
  - `1d`
- `tracking_error_limit`
  - `0.06`
- `active_risk_aversion`
  - `3.0`

## 二、进入前检查项

- 检查 1：
  - 输入装配 latest 已存在
- 检查 2：
  - candidate family 仍未漂移
- 检查 3：
  - `benchmark_id` 非空
- 检查 4：
  - `lookback_days > 0`
- 检查 5：
  - 仍明确标注：
    - `not_ready`
- 检查 6：
  - 已产出：
    - `covariance_bodyrun_preflight_latest.json`

## 三、当前暂缓项

- 暂缓：
  - 多家族并跑
  - shrinkage 参数扫描
  - factor-implied covariance 入口

## 四、一句话口径

- 当前 `covariance_model_id` 已不再停在入口准备，
  且也已不再停在 first fresh-run 执行，
  而是已推进到：
  - `minimum_stability_checked__not_ready`

## 回链

- `A5_covariance_model_id_本体实跑输入装配页__20260716.md`
- `A5_covariance_model_id_本体实跑最小准备页__20260716.md`
- `A5_covariance_model_id_first_fresh_run前检查页__20260716.md`
- `A5_covariance_model_id_first_fresh_run执行页__20260716.md`
- `A5_covariance_model_id_最小稳定性检查执行页__20260716.md`
- `02_runtime/a5_g5_covariance_bodyrun/runtime_execution_card_v1.md`
