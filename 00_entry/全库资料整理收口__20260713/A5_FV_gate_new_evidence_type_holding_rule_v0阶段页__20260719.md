# A5 FV gate new evidence type holding rule v0 阶段页

更新时间：2026-07-19

## 用途

- 把 `Cursor` 选定的第二个 `new evidence type` 正式落盘为：
  - `holding_rule_v0`
- 这页不重开：
  - 新信号
  - 新排序
  - 新暴露
  - 新窗口
  - 新成本带
- 这页只回答：
  - 当前冻结什么
  - 当前唯一允许变化什么
  - `20 trade days` 再平衡与静态持有相比是否仍站得住

## 一、当前阶段结论

- 当前正式从：
  - `FV_gate_new_evidence_type / cost_sensitivity_v0`
- 进入：
  - `FV_gate_new_evidence_type`
  - 第二个子阶段：
    - `holding_rule_v0`
- 当前进入原因是：
  - `sample_boundary` 已完成
  - `cost_sensitivity_v0` 已完成
  - 当前仍缺一类直接打到：
    - `single_entry_static_weight_minimal_backtest`
      假设本身
    的新证据

## 二、当前冻结合同

- 当前冻结不变的是：
  - `signal_hypothesis_id = trend_pullback_confirmation_v1`
  - `filter_layer_id = none`
  - `weight_logic_id = filtered_alpha_rank_to_target_weight_rank_decay_v2`
  - `final_size_scalar = 0.5`
  - 样本边界：
    - `20251215 -> 20260331`
  - benchmark：
    - `CSI300`
  - holdout 规则：
    - `last_n_trade_days`
    - `holdout_trade_days = 15`
  - 成本口径：
    - `degraded_fixed_cost`
    - `one_way_cost_bps = 15.0`
- 当前禁止变化的是：
  - 信号
  - 排序
  - 暴露
  - 窗口
  - 成本

## 三、当前唯一允许变化

- 当前唯一允许变化的是：
  - `holding_rule`
- 当前预声明对照冻结为：
  - 基线：
    - `single_entry_static_weight`
  - 新档：
    - `fixed_period_rebalance_v0`
    - `rebalance_every_trade_days = 20`
- 当前不做：
  - holding rule 网格
  - 多频率 sweep
  - threshold rebalance

## 四、当前最小输出合同

- 当前至少产出：
  - 一张 `20d rebalance` scorecard
  - 一张 baseline vs scenario summary
- 当前至少对照字段：
  - `net total_return`
  - `holdout net total_return`
  - `net active_total_return`
  - `net max_drawdown`
  - `rebalance_turnover_total`
- 当前标签只允许写成：
  - `holding_rule_stable__still_need_evidence`
  - 或
  - `holding_rule_fragile__still_need_evidence`

## 五、当前禁止项

- 禁止：
  - 回到同窗微调
  - 改 `rank-decay`
  - 改 `final_size_scalar`
  - 再扩成本带
  - 直接铺完整回测平台
  - 写成 `financial-valid`
  - 写成 `output_passed`

## 六、当前唯一下一手

- 当前唯一下一手是：
  - 用 `v1 sample boundary + 15bps`
    冻结合同
  - 只开：
    - `fixed_period_rebalance_v0`
    - `rebalance_every_20_trade_days`
  - 与已有静态持有基线直接对照

## 六点一、2026-07-19 holding_rule_v0 实跑结果

- 本轮已完成：
  - `fv_gate_holding_rule_v0_fixed_period_rebalance_v0_20d_scorecard_latest.json`
  - `fv_gate_holding_rule_v0_summary_latest.json`
- 当前 holding rule label 为：
  - `holding_rule_stable__still_need_evidence`
- 当前静态基线为：
  - `net total_return = 0.00197364`
  - `holdout net total_return = 0.00485478`
  - `net active_total_return = 0.03054991`
  - `net max_drawdown = -0.00983588`
- 当前 `20d rebalance` 新档为：
  - `net total_return = 0.00149584`
  - `holdout net total_return = 0.00461705`
  - `net active_total_return = 0.03007211`
  - `net max_drawdown = -0.00966033`
  - `rebalance_turnover_total = 0.00655254`
  - `rebalance_event_count = 3`
- 当前相对基线差值为：
  - `delta_net_total_return = -0.0004778`
  - `delta_holdout_net_total_return = -0.00023773`
  - `delta_net_active_total_return = -0.0004778`
  - `delta_net_max_drawdown = 0.00017555`
- 当前新增含义是：
  - 再平衡版本带来：
    - 略低的收益
    - 略低的 holdout
    - 略低的 active return
  - 但仍保持：
    - `net total_return > 0`
    - `holdout net total_return > 0`
    - `net active_total_return > 0`
  - 且回撤没有恶化，反而略收敛
- 当前因此最准确判断是：
  - 这条冻结合同对单一预声明 holding rule
    不是脆弱翻负
  - 但也不能写成：
    - `financial-valid`
    - `output_passed`

## 六点二、当前阶段完成后的下一手

- 当前 `holding_rule_v0` 阶段已满足最小完成判据。
- 当前下一手不是：
  - 扩更多 rebalance 周期
  - 直接开 threshold rebalance
  - 直接做稳健性全家桶
- 当前下一手应改写为：
  - 再次交回 `Cursor`
  - 统筹是否进入第三类 `new evidence type`
  - 或判断是否先停在当前 `still_need_evidence`

## 七、一句话口径

- 当前不是继续扩成本，也不是继续微调，而是：`v1_sample_boundary_frozen_contract_under_20d_fixed_period_rebalance__holding_rule_stable__still_need_evidence`。

## 回链

- `A5_Cursor主导_FV_gate_second_new_evidence_type讨论包__20260719.md`
- `A5_FV_gate_new_evidence_type_cost_sensitivity_v0阶段页__20260719.md`
- `A5_FV_gate_v1_sample_boundary阶段页__20260719.md`
- `02_runtime/a5_g5_financial_validity_gate_v0/fv_gate_holding_rule_v0_probe_template_v1.json`
