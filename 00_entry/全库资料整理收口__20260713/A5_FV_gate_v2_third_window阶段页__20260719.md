# A5 FV gate v2 third window 阶段页

更新时间：2026-07-19

## 一、当前阶段用途

- 本阶段用于：
  - 在不改 frozen contract
    的前提下，
    补第三个非重叠时间窗
  - 对
    `v0 current_best`
    与
    `v1 adjacent window`
    形成三窗对照
- 本阶段不允许写成：
  - `financial-valid`
  - `output_passed`
  - `cross_window_consistency_passed`

## 二、当前冻结合同

- 当前冻结不变的是：
  - `signal_hypothesis_id = trend_pullback_confirmation_v1`
  - `filter_layer_id = none`
  - `weight_logic_id = filtered_alpha_rank_to_target_weight_rank_decay_v2`
  - `final_size_scalar = 0.5`
  - `cost_model = degraded_fixed_cost`
  - `one_way_cost_bps = 15.0`
  - `holdout_trade_days = 15`
- 当前唯一允许变化的是：
  - 时间窗输入

## 三、候选窗与裁决

- 候选 A：
  - `20250701 -> 20250930`
- 候选 A 未采用原因：
  - `688981.SH`
    在
    `20250901 -> 20250908`
    期间缺行，
    导致 full-universe
    完整性检查失败
- 当前正式采用候选 B：
  - `20250909 -> 20251212`
- 当前采用理由：
  - 与：
    - `20260401 -> 20260630`
    - `20251215 -> 20260331`
    都不重叠
  - 距离失败候选最近
  - 可完整形成：
    - `60`
      个有效 trade dates
  - covariance fresh
    与 FV gate scorecard
    均已实跑成功

## 四、2026-07-19 第三窗实跑结果

- 当前第三窗 scorecard 为：
  - `fv_gate_v2_third_window_scorecard_latest.json`
- 当前第三窗窗口为：
  - `20250909 -> 20251212`
- 当前第三窗核心结果为：
  - `net total_return = 0.00740809`
  - `holdout net total_return = 0.00072619`
  - `net active_total_return = -0.0179673`
  - `net max_drawdown = -0.00699902`

## 五、三窗对照结果

- 当前三窗分别为：
  - `v0 current_best`
    - `20260401 -> 20260630`
  - `v1 adjacent`
    - `20251215 -> 20260331`
  - `v2 third`
    - `20250909 -> 20251212`
- 当前三窗标签应写成：
  - `cross_window_return_sign_majority_positive__active_sign_majority_negative__still_need_evidence`
- 当前多数观察为：
  - `net total_return`
    - `2 positive / 1 negative`
  - `holdout net total_return`
    - `2 positive / 1 negative`
  - `net active_total_return`
    - `1 positive / 2 negative`
  - `net max_drawdown`
    - `v2` 最好
    - `v1` 其次
    - `v0` 最差

## 六、主负责人裁决

- 当前最准确结论不是：
  - 跨窗一致性通过
  - 金融有效
  - 输出已通过
- 当前最准确结论是：
  - 绝对收益与 holdout
    已出现：
    - `2 正 1 负`
      的多数恢复
  - 但 active return
    仍呈：
    - `2 负 1 正`
      的多数偏负
  - 因此当前只能写成：
    - `still_need_evidence`
- 当前不再继续默认抓第四窗
- 当前下一手应改写为：
  - 暂停继续扩时间窗
  - 由 `Cursor`
    统筹是否进入：
    - active underperformance
      的更窄解释层
    - 或回到新的
      `new evidence type`
      统筹

## 七、正式产物

- `02_runtime/a5_g5_financial_validity_gate_v0/fv_gate_v2_third_window_runtime_params_template_v1.json`
- `02_runtime/a5_g5_financial_validity_gate_v0/artifacts/fv_gate_v2_third_window/fv_gate_v2_third_window_scorecard_latest.json`
- `02_runtime/a5_g5_financial_validity_gate_v0/artifacts/fv_gate_v2_third_window/fv_gate_v2_third_window_summary_latest.json`
- `02_runtime/a5_g5_financial_validity_gate_v0/artifacts/fv_gate_v2_third_window/fv_gate_v2_third_window_summary_latest.tsv`

## 八、一句话口径

- 当前最准确写法是：`third_window_replay_completed__return_sign_majority_positive_but_active_sign_majority_negative__still_need_evidence`。

## 九、2026-07-19 第三窗之后解释层已落地

- 当前已按 `Cursor`
  裁决正式新增：
  - `A5_FV_gate_active_underperformance_v0解释层页__20260719.md`
  - `fv_gate_active_underperformance_v0_summary_latest.json`
- 当前解释层只做：
  - 把
    `active_sign_majority_negative`
    正式点名
- 当前解释层不做：
  - 新 runtime
  - 新回测
  - 新 evidence type
- 当前第三窗之后的口径因此改写为：
  - `active underperformance`
    已被正式写出
  - 但状态仍保持：
    - `still_need_evidence`
