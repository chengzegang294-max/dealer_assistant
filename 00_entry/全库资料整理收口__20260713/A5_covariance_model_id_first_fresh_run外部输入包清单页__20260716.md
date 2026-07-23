# A5 covariance_model_id first fresh-run 外部输入包清单页

更新时间：2026-07-16

## 用途

- 在 `first fresh-run preflight` 已通过后，
  记录先前“外部输入包边界”判断为何成立、以及为何已被仓内资产解除。
- 这页只回答：
  - 旧判断为什么会把主线停在外部回包边界
  - 仓内哪些资产实际上足以解除该判断
  - 当前这页为什么只保留为历史边界说明

## 当前结论

- 当前仓内已具备：
  - 候选家族冻结
  - success / failure template-level smoke-run
  - success / failure latest 输入装配
  - first fresh-run preflight 已通过
- 当前仓内已进一步补齐：
  - `CSI300` benchmark 原始收益序列
  - `asset_returns_panel`
  - `benchmark_returns_series`
  - `active_returns_panel`
  - `benchmark_relative_sample_covariance` 的 first fresh-run
- 因此当前主线已不再停在：
  - `需要外部回包`
- 当前需要的不是：
  - 再改状态名
  - 再扩候选家族
  - 伪造 fresh-run 结果
- 当前真正需要的是：
  - 围绕 first fresh-run 结果继续做最小稳定性检查与唯一模型收敛准备

## 一、为什么这里曾属于外部回包边界

- 当前 runtime 目录里已经有的只有：
  - 模板
  - prep smoke-run latest
  - input assembly latest
  - preflight latest
- 当时还没有把以下资产重新接进当前 runtime 线：
  - `t02_daily_tushare_batch__sample20_q2__20260401_20260630.csv`
  - `t02_multi_symbol_sample_v3.csv`
  - `000300.SH` benchmark index daily raw
- 所以当时不能继续假装已经具备：
  - 协方差矩阵本体 fresh-run 输入

## 二、为什么这个边界现在已解除

- 本轮已用仓内 Tushare 资产跑出：
  - `artifacts/covariance_benchmark_series/covariance_benchmark_series__000300_SH__20260401_20260630.csv`
  - `artifacts/covariance_returns_input/asset_returns_panel_latest.csv`
  - `artifacts/covariance_returns_input/benchmark_returns_series_latest.csv`
  - `artifacts/covariance_returns_input/active_returns_panel_latest.csv`
- 因此当前已经具备：
  - 可直接消费的 `active returns panel`
  - 可直接进入协方差矩阵计算的 fresh-run 原始样本

## 三、当前保留下来的元信息口径

- 本轮实际执行统一采用：
  - `candidate_model_family = benchmark_relative_sample_covariance`
  - `portfolio_date = 2026-07-16`
  - `benchmark_id = CSI300`
  - `asset_universe_id = a5_top_liquid_20`
  - `returns_window_spec.lookback_days = 60`
  - `returns_window_spec.frequency = 1d`
- 最少样本要求：
  - 应覆盖最近 `60` 个 `1d` 观察
  - 应能回指到 `a5_top_liquid_20` 的成分集合

## 四、当前这页的定位

- 当前这页不再是：
  - 主线停点
  - 继续向用户索要外部回包的合同
- 当前这页仅保留为：
  - 一次错误边界判断的书面更正页
  - 说明为何已从“需要外部回包”修正为“仓内资产已吸收”

## 五、主负责人裁决

- 当前先做什么：
  - 正式承认旧的外部回包判断已解除
- 当前为什么改写：
  - 因为仓内现有 Tushare 与 daily_tushare 资产已经足以跑出 first fresh-run
- 当前恢复推进的入口已变成：
  - `A5_covariance_model_id_first_fresh_run执行页__20260716.md`

## 六、一句话口径

- 当前这页只保留历史意义；
  真正 first fresh-run 已不再卡在：
  - `外部输入包回包`

## 回链

- `A5_covariance_model_id_first_fresh_run前检查页__20260716.md`
- `A5_covariance_model_id_first_fresh_run入口准备页__20260716.md`
- `A5_covariance_model_id_first_fresh_run执行页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
