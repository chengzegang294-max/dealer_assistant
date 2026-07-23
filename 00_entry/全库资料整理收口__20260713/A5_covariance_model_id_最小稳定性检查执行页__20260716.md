# A5 covariance_model_id 最小稳定性检查执行页

更新时间：2026-07-18

## 用途

- 在 first fresh-run 已完成后，
  把相邻窗口的最小稳定性检查正式收口到一页。
- 这页记录的是：
  - 相邻窗口怎么取
  - 第二个窗口是否也能跑出同口径协方差矩阵
  - 最小稳定性检查是否通过
- 这页不负责：
  - 宣称 `covariance_model_id ready`
  - 宣称唯一模型已经冻结
  - 直接解除三段输出的 `not_output_passed`

## 当前结论

- 当前 `covariance_model_id` 已完成：
  - `benchmark_relative_sample_covariance` 的 first fresh-run
  - 相邻 `60 x 1d` 窗口的第二手 fresh-run
  - current vs adjacent 两窗口的最小稳定性检查
- 当前正式状态可推进到：
  - `minimum_stability_checked__not_ready`
- 当前还不是：
  - `risk_model_ready`
  - `unique_model_frozen`
  - `outputs_unblocked`

## 一、本轮执行对象

- 候选家族：
  - `benchmark_relative_sample_covariance`
- `benchmark_id`：
  - `CSI300`
- `asset_universe_id`：
  - `a5_top_liquid_20`
- 固定口径：
  - `lookback_days = 60`
  - `frequency = 1d`

## 二、两个比较窗口

- current 窗口：
  - `2026-04-01 -> 2026-06-30`
- adjacent 窗口：
  - `2025-12-26 -> 2026-03-31`
- 相邻窗口原始抓取起点写成：
  - `2025-12-15`
- 原因：
  - `2026-01-02 -> 2026-03-31` 只有 `56` 个交易日，
    不足以覆盖 `lookback = 60`
  - 因此向前补宽到：
    - `2025-12-15 -> 2026-03-31`
  - 再由 builder 自动截出最近 `60` 个公共交易日

## 三、本轮新增执行物

- `GENERATOR`
  - `02_runtime/a5_g5_covariance_bodyrun/run_covariance_stability_check_v1.py`
- `ARTIFACT`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/raw_daily/t02_daily_tushare_batch__sample20_adjacent60__20251215_20260331.csv`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/benchmark/covariance_benchmark_series__000300_SH__20251215_20260331.csv`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/returns/active_returns_panel_adjacent_latest.csv`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/fresh/covariance_matrix_adjacent_latest.csv`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/fresh/covariance_bodyrun_fresh_adjacent_latest.json`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_stability/covariance_stability_check_latest.json`

## 四、最小稳定性检查结果

- 结构层结果：
  - `matrix_shape = [20, 20]`
  - `symbol_count = 20`
  - 两窗口 `effective_trade_dates = 60`
  - 两窗口均：
    - `diagonal_positive = true`
    - `is_psd = true`
- 特征值边界：
  - current `min_eigenvalue = 2.0584972694271718e-05`
  - adjacent `min_eigenvalue = 1.5005948977740515e-05`
- 规模比较：
  - `trace_current = 0.010032149359699299`
  - `trace_adjacent = 0.00649973422442069`
  - `trace_ratio_current_over_adjacent = 1.5434707040799727`
  - `relative_trace_gap = 0.3521095040180391`
- 差异摘要：
  - `relative_fro_diff = 0.8130021798540153`
  - `diag_ratio_mean_current_over_adjacent = 1.9869537110869337`
- 当前判断：
  - `stability_check_passed = true`

## 五、为什么能推进一档但仍 not_ready

- 当前已新增证明：
  - 不是只在单个窗口里偶然跑通一次
  - 至少两个相邻 `60d` 窗口下都能跑出 PSD 协方差矩阵
- 当前仍未证明：
  - 唯一实现模型已经无需保留其它候选
  - 更长样本段下的稳健边界
  - 下游三段输出已可解除 `not_output_passed`
- 所以当前只能推进到：
  - `minimum_stability_checked__not_ready`

## 六、主负责人裁决

- 当前先做什么：
  - 正式承认最小稳定性检查已通过
  - 把状态从 `first_fresh_run_completed__not_ready` 前推到 `minimum_stability_checked__not_ready`
  - 把下一手切到唯一模型收敛准备
- 当前暂缓什么：
  - `ready` 宣称
  - 多家族并跑
  - shrinkage 参数扫描
- 当前继续保留的 `NEED_EVIDENCE`：
  - 唯一实现模型冻结依据
  - 更高一层稳定性或边界检查

## 七、一句话口径

- 当前 `covariance_model_id` 已从：
  - `first_fresh_run_completed__not_ready`
  推进到：
  - `minimum_stability_checked__not_ready`

## 七点五、2026-07-18 执行验证复跑

- 本轮已对相邻窗口 fresh 再次执行：
  - `run_covariance_bodyrun_fresh_v1.py`
- 本轮已对现有 latest 产物再次执行：
  - `run_covariance_stability_check_v1.py`
- 本轮 adjacent fresh 复跑确认：
  - `fresh_run_passed = true`
  - `matrix_shape = [20, 20]`
  - `first_trade_date = 20251226`
  - `last_trade_date = 20260331`
- 本轮复跑确认：
  - `status = success`
  - `stability_check_passed = true`
  - `structural_pass = true`
  - `relative_trace_gap = 0.3521095040180391`
- 这次复跑新增证明的是：
  - 相邻窗口 fresh 不是历史残留产物
  - current / adjacent 两窗口的最小稳定性判断当前仍可复现
  - 现有 stability latest 不是一次性历史产物
- 这次复跑不新增宣称：
  - `risk_model_ready`
  - `outputs_unblocked`
  - 任何高于 `minimum_stability_checked__not_ready` 的状态名

## 回链

- `A5_covariance_model_id_最小稳定性检查准备页__20260716.md`
- `A5_covariance_model_id_first_fresh_run执行页__20260716.md`
- `A5_covariance_model_id_唯一模型收敛准备页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
