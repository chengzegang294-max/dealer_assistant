# A5 FV gate new evidence type cost sensitivity v0 阶段页

更新时间：2026-07-19

## 用途

- 把 `Cursor` 选定的首个 new evidence type 正式落盘为：
  - `cost_sensitivity_v0`
- 这页不重开：
  - 新信号
  - 新排序
  - 新暴露
  - 新窗口
- 这页只回答：
  - 当前冻结什么
  - 当前唯一允许变什么
  - 当前最小成本带怎么定义

## 一、当前阶段结论

- 当前正式从：
  - `FV_gate_v1_sample_boundary`
- 进入：
  - `FV_gate_new_evidence_type`
  - 首个子阶段：
    - `cost_sensitivity_v0`
- 当前进入原因是：
  - 新样本边界证据已完成
  - 但仍需判断：
    - 当前正向结果对小成本带是否稳定

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
- 当前禁止变化的是：
  - 信号
  - 排序
  - 暴露
  - 窗口

## 三、当前唯一允许变化

- 当前唯一允许变化的是：
  - `one_way_cost_bps`
- 当前预声明小成本带冻结为：
  - `5.0`
  - `15.0`
  - `25.0`
- 当前中位基线仍是：
  - `15.0`

## 四、当前最小输出合同

- 当前至少产出：
  - 三档 scorecard
  - 一张 band summary
- 当前至少对照字段：
  - `net total_return`
  - `holdout net total_return`
  - `net active_total_return`
  - `net max_drawdown`
- 当前标签只允许写成：
  - `cost_band_stable__still_need_evidence`
  - 或
  - `cost_band_fragile__still_need_evidence`

## 五、当前禁止项

- 禁止：
  - 再开第二个 new evidence type
  - 回到同窗微调
  - 回到 breakout
  - 扩完整回测平台
  - 写成 `financial-valid`
  - 写成 `output_passed`

## 六、当前唯一下一手

- 当前唯一下一手是：
  - 用 `v1 sample boundary` 冻结合同
  - 在 `5 / 15 / 25 bps`
    上复跑最小成绩单
  - 然后给出 band summary

## 六点一、2026-07-19 成本带实跑结果

- 本轮已完成：
  - `fv_gate_cost_sensitivity_v0_band_summary_latest.json`
  - `5bps / 15bps / 25bps`
    三档 scorecard
- 当前 band label 为：
  - `cost_band_stable__still_need_evidence`
- 当前 band summary 为：
  - `min_net_total_return = 0.00184768`
  - `max_net_total_return = 0.0020996`
  - `min_holdout_net_total_return = 0.00485478`
  - `max_holdout_net_total_return = 0.00485478`
  - `min_net_active_total_return = 0.03042395`
  - `max_net_active_total_return = 0.03067587`
  - `worst_net_max_drawdown = -0.00983588`
- 当前新增含义是：
  - 在预声明小成本带内，
    `v1 sample boundary` 的正向结果没有塌掉
  - 当前 `degraded_fixed_cost`
    至少在 `5 / 15 / 25 bps`
    范围内呈现：
    - 小带稳定
- 当前但仍不能写成：
  - `financial-valid`
  - `output_passed`

## 六点二、当前阶段完成后的下一手

- 当前 `cost_sensitivity_v0` 阶段已满足完成判据。
- 当前下一手不是：
  - 再扩更宽成本带
  - 直接开冲击模型
- 当前下一手应改写为：
  - 由 `Cursor` 统筹是否进入第二个 `new evidence type` 子阶段
  - 在该统筹结论前，`Trae` 暂不直接开新执行线

## 六点三、2026-07-19 第二个 new evidence type 已吸收并执行

- 本轮已吸收 `Cursor` 的第二个证据类型统筹：
  - `holding_rule_v0`
- 当前已正式进入并完成最小执行：
  - `A5_FV_gate_new_evidence_type_holding_rule_v0阶段页__20260719.md`
  - `fv_gate_holding_rule_v0_summary_latest.json`
- 当前新标签为：
  - `holding_rule_stable__still_need_evidence`
- 当前因此本页的“由 Cursor 统筹是否进入第二个 new evidence type”
  已不再是未执行事项，
  而是：
  - 已完成统筹吸收
  - 已完成第一手实跑
  - 当前下一手应再次交回 `Cursor`
    统筹是否进入第三类 `new evidence type`

## 七、一句话口径

- 当前不是继续换窗，也不是继续调参，而是：`v1_sample_boundary_frozen_contract_under_small_cost_band__cost_band_stable__still_need_evidence`。

## 回链

- `A5_Cursor仓库熟悉度验收与new_evidence_type统筹页__20260719.md`
- `A5_FV_gate_v1_sample_boundary阶段页__20260719.md`
- `02_runtime/a5_g5_financial_validity_gate_v0/fv_gate_v1_sample_boundary_runtime_params_template_v1.json`
