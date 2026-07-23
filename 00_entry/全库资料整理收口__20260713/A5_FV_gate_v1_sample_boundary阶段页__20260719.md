# A5 FV gate v1 sample boundary 阶段页

更新时间：2026-07-19

## 用途

- 把 `Cursor` 对下一阶段的规划正式落盘为：
  - `FV_gate_v1_sample_boundary`
- 这页不重跑：
  - 同窗微调
  - `scalar`
  - `rank-decay`
- 这页只回答：
  - 为什么现在进入 `v1`
  - `v1` 冻结什么
  - `v1` 允许变什么
  - 当前唯一下一手是什么

## 一、当前阶段切换结论

- 当前正式从：
  - `FV gate v0 current_best tuning_frozen`
- 切到：
  - `FV_gate_v1_sample_boundary`
- 当前切换原因是：
  - `v0` 已完成最小回测入口、A/B、过滤失败、risk-lite、rank-decay+risk-lite、`current_best` 冻结与 `tuning_frozen`
  - 同窗继续微调已无新增证据类型价值

## 二、当前冻结四元组

- 当前冻结为：
  - `signal_hypothesis_id = trend_pullback_confirmation_v1`
  - `filter_layer_id = none`
  - `weight_logic_id = filtered_alpha_rank_to_target_weight_rank_decay_v2`
  - `final_size_scalar = 0.5`
- 当前一并冻结：
  - 成本口径：
    - `degraded_fixed_cost`
  - holdout 规则形态：
    - `last_n_trade_days`
    - `holdout_trade_days = 15`

## 三、当前唯一允许变化的边界

- 当前允许变化的不是：
  - 信号
  - 过滤器
  - 排序逻辑
  - 暴露缩放
- 当前唯一允许变化的是：
  - 样本时间窗切到：
    - `adjacent window`
  - 对应 OHLCV / benchmark / covariance fresh 输入切到相邻窗

## 四、当前已确认输入

- 当前仓内已存在：
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/raw_daily/t02_daily_tushare_batch__sample20_adjacent60__20251215_20260331.csv`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/benchmark/covariance_benchmark_series__000300_SH__20251215_20260331.csv`
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_adjacent_window/fresh/covariance_bodyrun_fresh_adjacent_latest.json`
- 这意味着当前：
  - 不触发 `缺外部输入停`
  - 可以直接进入相邻窗复跑

## 五、当前唯一下一手

- 当前唯一下一手是：
  - 用 `current_best` 冻结合同在相邻窗口复跑一张最小成绩单
  - 并与 `v0 current_best` 做字段对照
- 当前至少要对照：
  - `holdout net total_return`
  - `net total_return`
  - `net active_total_return`
  - `net max_drawdown`

## 五点一、2026-07-19 相邻窗复跑结果

- 本轮已完成：
  - `fv_gate_v1_sample_boundary_scorecard_latest.json`
- 当前相邻窗结果为：
  - `net total_return = 0.00197364`
  - `holdout net total_return = 0.00485478`
  - `net active_total_return = 0.03054991`
  - `net max_drawdown = -0.00983588`
- 相比 `v0 current_best`：
  - `net total_return`：
    - `-0.00947495 -> 0.00197364`
  - `holdout net total_return`：
    - `-0.00291711 -> 0.00485478`
  - `net active_total_return`：
    - `-0.12843922 -> 0.03054991`
  - `net max_drawdown`：
    - `-0.01794461 -> -0.00983588`
- 当前新增含义是：
  - `current_best` 冻结合同在新样本边界上没有崩塌
  - 且相邻窗对照给出了方向性更强的正向结果
- 当前最准确标签应写成：
  - `sample_boundary_reproduced__still_need_evidence`
- 当前仍不能写成：
  - `financial-valid`
  - `output_passed`

## 六、当前禁止项

- 禁止：
  - 同窗继续调 `final_size_scalar`
  - 同窗继续调 `rank-decay`
  - 解冻 `tuning_frozen`
  - 切回 `breakout`
  - 扩新信号池
  - 铺完整回测平台
  - 写成 `financial-valid`
  - 写成 `output_passed`

## 七、停点与等待条件

- 当前仅在以下情况停：
  - 相邻窗输入不可对齐
  - runtime 合同断裂
  - 权限或破坏性操作
  - 硬分歧
- 当前阶段完成判据是：
  - 相邻窗成绩单已落盘
  - 与 `v0 current_best` 对照已写清
  - 标签已写清

## 七点一、当前阶段已完成后的下一手

- 当前 `v1 sample boundary` 阶段已满足完成判据。
- 当前下一手不是：
  - 再开第二个相邻窗复跑
  - 回到同窗微调
- 当前下一手应切到：
  - 由 `Cursor` 统筹判断是否进入：
    - `new evidence type` 子阶段
  - 在该统筹结论前，`Trae` 暂不直接开新执行线

## 八、一句话口径

- 当前不是继续调 `v0`，而是：`current_best_frozen_contract_replayed_on_adjacent_window__sample_boundary_reproduced__still_need_evidence`。

## 回链

- `A5_FV_gate_v0_当前最佳最小口径冻结页__20260719.md`
- `A5_FV_gate_v0_current_best后续推进主负责人裁决页__20260719.md`
- `A5_Cursor主导_FV_gate下一阶段规划讨论包__20260719.md`
- `02_runtime/a5_g5_financial_validity_gate_v0/fv_gate_v1_sample_boundary_runtime_params_template_v1.json`
