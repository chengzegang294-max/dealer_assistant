# A5 covariance_model_id first fresh-run 执行页

更新时间：2026-07-18

## 用途

- 在 `first fresh-run preflight` 已通过后，
  把 `benchmark_relative_sample_covariance` 的第一手真实执行正式收口到一页。
- 这页记录的是：
  - 仓内既有日线资产如何被吸收到执行输入
  - first fresh-run 跑出了什么
  - 当前为什么仍然 `not_ready`
- 这页不负责：
  - 宣称唯一实现模型已定稿
  - 宣称风险模型已 ready
  - 展开多家族并跑

## 当前结论

- 当前 `covariance_model_id` 已完成：
  - `benchmark_relative_sample_covariance` 的 first fresh-run
  - `CSI300` benchmark 原始收益序列抓取
  - `asset_returns / benchmark_returns / active_returns` 三类输入产物
  - `20 x 20` 协方差矩阵 first fresh-run
- 当前正式状态可推进到：
  - `first_fresh_run_completed__not_ready`
- 当前还不是：
  - `risk_model_ready`
  - `unique_model_frozen`
  - `three_outputs_unblocked`

## 一、本轮实际消费的仓内资产

- 资产日线底表：
  - `02_runtime/ashare_p0_first_round_validation/data/t02_sources/daily_tushare/t02_daily_tushare_batch__sample20_q2__20260401_20260630.csv`
- 样本 universe：
  - `02_runtime/ashare_p0_first_round_validation/data/t02_multi_symbol_sample_v3.csv`
- benchmark 原始序列抓取入口：
  - `02_runtime/a5_g5_covariance_bodyrun/fetch_covariance_benchmark_series_v1.py`
- benchmark latest：
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_benchmark_series/covariance_benchmark_series__000300_SH__20260401_20260630.csv`

## 二、本轮新增执行物

- `GENERATOR`
  - `02_runtime/a5_g5_covariance_bodyrun/fetch_covariance_benchmark_series_v1.py`
  - `02_runtime/a5_g5_covariance_bodyrun/build_covariance_returns_input_v1.py`
  - `02_runtime/a5_g5_covariance_bodyrun/run_covariance_bodyrun_fresh_v1.py`
- `ARTIFACT`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_benchmark_series/covariance_benchmark_series__000300_SH__20260401_20260630.csv`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_returns_input/asset_returns_panel_latest.csv`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_returns_input/benchmark_returns_series_latest.csv`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_returns_input/active_returns_panel_latest.csv`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_fresh/covariance_matrix_latest.csv`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_fresh/covariance_bodyrun_fresh_latest.json`

## 三、本轮 first fresh-run 结果

- 候选家族：
  - `benchmark_relative_sample_covariance`
- `benchmark_id`：
  - `CSI300`
- `asset_universe_id`：
  - `a5_top_liquid_20`
- `lookback_days`：
  - `60`
- 实际覆盖：
  - `60` 个交易日
  - `20` 个标的
- 结果摘要：
  - `matrix_shape = [20, 20]`
  - `diagonal_positive = true`
  - `is_psd = true`
  - `min_eigenvalue = 2.0584972694271718e-05`
- 正式 `covariance_model_id`：
  - `benchmark_relative_sample_covariance__CSI300__lookback60__a5_top_liquid_20__v1`

## 四、为什么这次不再属于“需要外部回包”

- 本轮已确认：
  - 先前所谓“first fresh-run 外部输入包缺失”，
    实际上是没有把仓内已有 `Tushare + daily_tushare + sample20 universe` 资产重新吸收到当前 runtime 线。
- 当前仓内已经足以生成：
  - `benchmark_returns_series`
  - `asset_returns_panel`
  - `active_returns_panel`
- 因此本轮正式解除：
  - `需要外部回包`

## 五、为什么当前仍然 not_ready

- 当前已经证明的是：
  - 单家族
  - 单窗口
  - 第一手真实协方差矩阵可生成
- 当前还没证明的是：
  - 更长窗口或相邻窗口的稳定性
  - shrinkage / factor-implied 是否仍需保留为候选
  - 是否足以冻结唯一实现模型
- 所以当前只能写成：
  - `first_fresh_run_completed__not_ready`

## 六、主负责人裁决

- 当前先做什么：
  - 正式承认 first fresh-run 已完成
  - 把旧的“外部输入包边界”改写为“仓内资产已吸收并解除”
  - 把下一手推进到唯一模型收敛前的最小稳定性检查
- 当前暂缓什么：
  - 多家族并跑
  - shrinkage 参数扫描
  - 直接把 `covariance_model_id` 写成 ready

## 七、一句话口径

- 当前 `covariance_model_id` 已不再停在 `preflight only`，
  而是已推进到：
  - `first_fresh_run_completed__not_ready`

## 七点五、2026-07-18 执行验证复跑

- 本轮已按现有 latest 输入再次执行：
  - `run_covariance_bodyrun_fresh_v1.py`
- 本轮复跑确认：
  - `status = success`
  - `fresh_run_passed = true`
  - `matrix_shape = [20, 20]`
  - `diagonal_positive = true`
  - `is_psd = true`
- 这次复跑新增证明的是：
  - 当前 runtime 线不是历史孤例
  - 在仓内现有 `runtime_params + active_returns latest` 下仍可直接复现
- 这次复跑不新增宣称：
  - `risk_model_ready`
  - `unique_model_frozen`
  - 任何高于 `first_fresh_run_completed__not_ready` 的状态名

## 回链

- `A5_covariance_model_id_first_fresh_run入口准备页__20260716.md`
- `A5_covariance_model_id_first_fresh_run前检查页__20260716.md`
- `A5_covariance_model_id_first_fresh_run外部输入包清单页__20260716.md`
- `A5_covariance_model_id_最小稳定性检查准备页__20260716.md`
- `A5_covariance_model_id_最小稳定性检查执行页__20260716.md`
- `A5_covariance_model_id_本体实跑最小准备页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
