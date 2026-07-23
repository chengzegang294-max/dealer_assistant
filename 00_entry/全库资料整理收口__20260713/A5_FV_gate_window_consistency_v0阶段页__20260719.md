# A5 FV gate window consistency v0 阶段页

更新时间：2026-07-19

## 用途

- 把 `Cursor` 本轮新统筹正式落盘为：
  - `FV_gate_window_consistency_v0`
- 这页不重开：
  - 第三类 `new evidence type`
  - 冲击模型
  - 稳健性全家桶
  - 同窗微调
- 这页只回答：
  - 为什么现在先做跨窗一致性收口
  - 当前对照冻结什么
  - 当前结果到底是“一致”还是“分歧”
  - 当前完成后下一手是什么

## 一、当前阶段结论

- 当前正式从：
  - `FV_gate_new_evidence_type / holding_rule_v0`
- 进入：
  - `FV_gate_window_consistency_v0`
- 当前进入原因是：
  - `sample_boundary_v1`
    已证明：
    - 相邻窗存在一张正向成绩单
  - `cost_sensitivity_v0`
    与 `holding_rule_v0`
    已继续证明：
    - 在该正向窗口下，
      小成本带与单一预声明持有规则都未把结果打回负区
  - 但当前仍缺：
    - 同一冻结合同在两个时间窗上的正式对照收口
  - 因而当前最值钱的一手不是再开第三类新证据，
    而是先把：
    - `v0 current_best window`
    - `v1 adjacent window`
    的符号分歧正式写清

## 二、当前冻结对照合同

- 当前冻结不变的是：
  - `signal_hypothesis_id = trend_pullback_confirmation_v1`
  - `filter_layer_id = none`
  - `weight_logic_id = filtered_alpha_rank_to_target_weight_rank_decay_v2`
  - `final_size_scalar = 0.5`
  - `cost_model = degraded_fixed_cost`
  - `one_way_cost_bps = 15.0`
  - `holdout_rule = last_n_trade_days`
  - `holdout_trade_days = 15`
- 当前唯一允许变化的是：
  - 样本时间窗
- 当前对照冻结为：
  - `v0 current_best window = 20260401 -> 20260630`
  - `v1 adjacent window = 20251215 -> 20260331`
- 当前禁止变化的是：
  - 信号
  - 过滤
  - 排序
  - 暴露
  - 成本
  - 持有规则

## 三、当前最小输出合同

- 当前至少产出：
  - 一张跨窗对照 summary
  - 一张跨窗对照 tsv
- 当前至少对照字段：
  - `net total_return`
  - `holdout net total_return`
  - `net active_total_return`
  - `net max_drawdown`
- 当前标签只允许写成：
  - `cross_window_sign_divergence__still_need_evidence`
  - 或
  - `cross_window_stable__still_need_evidence`
- 当前这一轮更准确要避免误写为：
  - `window_consistency_passed`
  - `financial-valid`
  - `output_passed`

## 四、当前禁止项

- 禁止：
  - 把相邻窗正向结果直接偷换成跨窗一致
  - 在 `window_consistency_v0`
    里继续调 `final_size_scalar`
  - 在 `window_consistency_v0`
    里继续调 `rank-decay`
  - 直接开第三类 `new evidence type`
  - 直接开第三日历窗数据抓取
  - 直接开冲击模型
  - 直接开稳健性全家桶

## 五、当前唯一下一手

- 当前唯一下一手是：
  - 只用既有两张正式 scorecard
  - 把：
    - `fv_gate_v0_current_best_scorecard_latest.json`
    - `fv_gate_v1_sample_boundary_scorecard_latest.json`
    做正式跨窗字段对照
  - 然后给出：
    - 是否同符号
    - 是否已足以继续开第三类新证据

## 五点一、2026-07-19 window_consistency_v0 对照结果

- 本轮已完成：
  - `fv_gate_window_consistency_v0_summary_latest.json`
  - `fv_gate_window_consistency_v0_summary_latest.tsv`
- 当前 window consistency label 为：
  - `cross_window_sign_divergence__still_need_evidence`
- 当前 `v0 current_best window` 为：
  - `net total_return = -0.00947495`
  - `holdout net total_return = -0.00291711`
  - `net active_total_return = -0.12843922`
  - `net max_drawdown = -0.01794461`
- 当前 `v1 adjacent window` 为：
  - `net total_return = 0.00197364`
  - `holdout net total_return = 0.00485478`
  - `net active_total_return = 0.03054991`
  - `net max_drawdown = -0.00983588`
- 当前 `adjacent - current_best` 差值为：
  - `delta_net_total_return = 0.01144859`
  - `delta_holdout_net_total_return = 0.00777189`
  - `delta_net_active_total_return = 0.15898913`
  - `delta_net_max_drawdown = 0.00810873`
- 当前新增含义是：
  - 同一冻结合同在两个窗口上没有保持同符号
  - `v0 current_best window`
    的核心收益字段为负
  - `v1 adjacent window`
    的核心收益字段为正
  - 因而当前最诚实的结论不是：
    - `cross_window_stable`
  - 而是：
    - 已出现正式的跨窗符号分歧
- 当前因此更准确的判断是：
  - `sample boundary reproduced`
    依然成立，
    因为相邻窗正向复验是真实证据
  - 但该证据现在又被补上了：
    - `cross_window_sign_divergence`
      这一层新停点
  - 因此整体仍必须保留：
    - `still_need_evidence`

## 五点二、当前阶段完成后的下一手

- 当前 `window_consistency_v0`
  阶段已满足最小完成判据。
- 当前下一手不是：
  - 立刻进入第三类 `new evidence type`
  - 立刻抓第三日历窗
  - 立刻做冲击模型
  - 立刻做稳健性全家桶
- 当前下一手应改写为：
  - 再次交回 `Cursor`
  - 统筹二选一：
    - 补第三日历窗数据，
      继续验证 `cross_window_sign_divergence`
      是偶发还是持续
    - 或正式停在当前
      `still_need_evidence`
      不再默认扩线

## 五点三、2026-07-19 后续方向多AI讨论包已备

- 本轮已新增：
  - `A5_FV_gate_window_consistency_v0后续方向_多AI前情提要与裁决框架__20260719.md`
  - `A5_FV_gate_window_consistency_v0后续方向_多家AI正式发包稿__20260719.md`
  - `A5_FV_gate_window_consistency_v0后续方向_多家AI回收记录模板__20260719.md`
- 当前用途是：
  - 让 `GPT / DeepSeek / Kimi / GLM / Qwen`
    围绕：
    - 第三日历窗
    - 先停在当前
    - 更窄替代动作
    给出保守 / 平衡 / 激进三种方案
- 当前 `Trae` 下一手不是：
  - 直接替代多家 AI 拍板
- 当前 `Trae` 下一手是：
  - 等待多家 AI 回包
  - 然后做主负责人吸收与正式裁决

## 五点四、2026-07-19 多家AI回包已吸收并转入第三窗准备

- 本轮已新增：
  - `A5_FV_gate_window_consistency_v0后续方向_多家AI回收记录与主负责人裁决__20260719.md`
  - `A5_FV_gate_v2_third_window准备页__20260719.md`
- 当前主负责人正式裁决是：
  - 不直接停在当前
  - 不把环境归因页改写成新主线
  - 进入：
    - `FV_gate_v2_third_window_preparation`
- 当前第三窗冻结为：
  - `20250701 -> 20250930`
- 当前又已确认：
  - 仓内 runtime 现成输入只覆盖：
    - `20251215 -> 20260331`
    - `20260401 -> 20260630`
  - 尚未发现第三窗对应：
    - 日线 csv
    - benchmark csv
    - covariance fresh json
- 当前下一手因此改写为：
  - 先补第三窗输入装配
  - 输入未到位前，
    停在：
    - `input_gated`
    这一合法停点

## 五点五、2026-07-19 第三窗准备已闭合并完成实跑

- 本轮已新增：
  - `A5_FV_gate_v2_third_window阶段页__20260719.md`
  - `fv_gate_v2_third_window_scorecard_latest.json`
  - `fv_gate_v2_third_window_summary_latest.json`
- 当前第三窗原候选：
  - `20250701 -> 20250930`
  已因：
  - `688981.SH`
    在
    `20250901 -> 20250908`
    缺行
    而放弃
- 当前正式采用并实跑成功的第三窗为：
  - `20250909 -> 20251212`
- 当前三窗正式标签更新为：
  - `cross_window_return_sign_majority_positive__active_sign_majority_negative__still_need_evidence`
- 当前下一手因此再次改写为：
  - 不继续默认抓第四窗
  - 由 `Cursor`
    统筹是否围绕：
    - `active underperformance`
      开更窄解释层
    - 或切回新的
      `new evidence type`

## 六、一句话口径

- 当前不是“跨窗一致性已成立”，而是：`current_best_frozen_contract_after_sample_boundary_reproduced_and_two_new_evidence_checks__cross_window_sign_divergence__still_need_evidence`。

## 回链

- `A5_FV_gate_new_evidence_type_holding_rule_v0阶段页__20260719.md`
- `A5_FV_gate_new_evidence_type_cost_sensitivity_v0阶段页__20260719.md`
- `A5_FV_gate_v1_sample_boundary阶段页__20260719.md`
- `02_runtime/a5_g5_financial_validity_gate_v0/artifacts/fv_gate_v0/fv_gate_v0_current_best_scorecard_latest.json`
- `02_runtime/a5_g5_financial_validity_gate_v0/artifacts/fv_gate_v1_sample_boundary/fv_gate_v1_sample_boundary_scorecard_latest.json`
