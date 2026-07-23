# A5 G5 Financial Validity Gate v0 Runtime

## 用途

- 为 `A5 -> G5` 提供独立的 `financial validity gate v0` 最小 runtime 入口骨架。
- 当前只承接：
  - `contract-first minimal backtest entry`
  - 最小成绩单产物
  - 最小失败回退记录
- 当前不承接：
  - 完整回测平台
  - 稳健性全家桶
  - 多市场并行

## 当前已锁定输入

- same-batch APW 入口：
  - `02_runtime/a5_g5_adjusted_position_weight_validation/artifacts/adjusted_position_weight_validation/covariance_target_weight_pte_apw_same_batch_latest.json`
- 资产 OHLCV：
  - `02_runtime/ashare_p0_first_round_validation/data/t02_sources/daily_tushare/t02_daily_tushare_batch__sample20_q2__20260401_20260630.csv`
- benchmark series：
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_benchmark_series/covariance_benchmark_series__000300_SH__20260401_20260630.csv`
- benchmark returns：
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_returns_input/benchmark_returns_series_latest.csv`
- active returns：
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_returns_input/active_returns_panel_latest.csv`
- covariance fresh：
  - `02_runtime/a5_g5_covariance_bodyrun/artifacts/covariance_bodyrun_fresh/covariance_bodyrun_fresh_latest.json`

## 当前计划输出

- `artifacts/fv_gate_v0/`
  - 最小成绩单 JSON
  - 最小成绩单 CSV 或 TSV
  - 失败回退 latest JSON

## 当前已生成

- `artifacts/fv_gate_v0/fv_gate_v0_scorecard_latest.json`
- `artifacts/fv_gate_v0/fv_gate_v0_scorecard_latest.tsv`
- `fv_gate_v0_runtime_params_round2_template_v1.json`
- `fv_gate_v0_runtime_params_round2_breakout_template_v1.json`
- `fv_gate_v0_runtime_params_round3_trend_filter_template_v1.json`
- `fv_gate_v0_runtime_params_round3_trend_risklite_template_v1.json`
- `fv_gate_v0_runtime_params_round4_rankdecay_risklite_template_v1.json`
- `fv_gate_v0_runtime_params_current_best_template_v1.json`
- `fv_gate_v1_sample_boundary_runtime_params_template_v1.json`
- `fv_gate_cost_sensitivity_v0_band_template_v1.json`
- `fv_gate_holding_rule_v0_probe_template_v1.json`
- `fv_gate_v2_third_window_runtime_params_template_v1.json`
- `artifacts/fv_gate_v0/fv_gate_v0_round2_scorecard_latest.json`
- `artifacts/fv_gate_v0/fv_gate_v0_round2_breakout_scorecard_latest.json`
- `artifacts/fv_gate_v0/fv_gate_v0_round3_risklite_scorecard_latest.json`
- `artifacts/fv_gate_v0/fv_gate_v0_round4_rankdecay_risklite_scorecard_latest.json`
- `artifacts/fv_gate_v0/fv_gate_v0_current_best_scorecard_latest.json`
- `artifacts/fv_gate_v1_sample_boundary/fv_gate_v1_sample_boundary_scorecard_latest.json`
- `artifacts/fv_gate_cost_sensitivity_v0/fv_gate_cost_sensitivity_v0_band_summary_latest.json`
- `artifacts/fv_gate_holding_rule_v0/fv_gate_holding_rule_v0_summary_latest.json`
- `artifacts/fv_gate_window_consistency_v0/fv_gate_window_consistency_v0_summary_latest.json`
- `artifacts/fv_gate_v2_third_window/fv_gate_v2_third_window_scorecard_latest.json`
- `artifacts/fv_gate_v2_third_window/fv_gate_v2_third_window_summary_latest.json`
- `artifacts/fv_gate_active_underperformance_v0/fv_gate_active_underperformance_v0_summary_latest.json`

## 当前冻结范围

- `holdout` 必须作为回测内规则存在。
- 成本口径当前只允许：
  - `degraded_fixed_cost`
- 当前通过只允许写成：
  - `FV_gate_v0_evidence_produced`
- 当前禁止写成：
  - `financial-valid`
  - `output_passed`
  - `ready to deploy`

## 当前下一手

- 基于首轮成绩单，继续留在 `FV gate` 内调整最小信号组合 / 评价卡。
- 第二轮参数挂点已冻结：
  - `signal_hypothesis_id`
  - `filter_layer_id`
  - `evaluation_card_id`
  - `baseline_scorecard_json`
- 当前真实对照结果已显示：
  - `trend_pullback_confirmation_v1` 优于首轮 proxy 与 breakout 对照
  - 但仍属于 `improved_but_still_negative`
- 当前第三轮又显示：
  - 更严过滤层会把样本筛空
  - risk-lite 缩仓会继续改善收益、holdout 与回撤
- 当前第四轮又显示：
  - 弱名次降权 + 更轻仓位 比第三轮 risk-lite 继续改善
  - 当前可冻结为最佳最小口径
- 当前 `current_best` 独立复跑又显示：
  - 最佳最小口径已具备稳定基线形态
  - 后续继续应与 `current_best` 比较，不再直接依附某一轮次命名
- 当前 `v1 sample boundary` 又显示：
  - `current_best` 冻结合同在相邻窗上完成正向复验
  - 已形成 `sample_boundary_reproduced` 型新证据
  - 但仍必须保留 `still_need_evidence`
- 当前 `cost_sensitivity_v0` 又显示：
  - `v1 sample boundary` 冻结合同在 `5 / 15 / 25 bps` 小成本带内保持正向
  - 已形成 `cost_band_stable` 型新证据
  - 但仍必须保留 `still_need_evidence`
- 当前 `holding_rule_v0` 又显示：
  - 在相同 `v1 sample boundary + 15bps`
    冻结合同下，
    `fixed_period_rebalance_v0`
    的 `20 trade days`
    最小再平衡场景仍保持：
    - `net total_return > 0`
    - `holdout net total_return > 0`
    - `net active_total_return > 0`
  - 相比静态持有基线，收益略有收缩但未翻负
  - 已形成 `holding_rule_stable` 型第二类新证据
  - 但仍必须保留 `still_need_evidence`
- 当前 `window_consistency_v0` 又显示：
  - 同一冻结合同在：
    - `v0 current_best window`
    - `v1 adjacent window`
    上出现：
    - 收益主字段符号分歧
  - 当前更准确的新增停点不是：
    - `cross_window_consistency_passed`
  - 而是：
    - `cross_window_sign_divergence__still_need_evidence`
  - 因而当前下一手不再默认扩第三类 `new evidence type`
  - 而应先交回 `Cursor`
    统筹：
    - 是否补第三日历窗
    - 或停在当前 `still_need_evidence`
- 当前 `v2 third window` 又显示：
  - 失败候选
    `20250701 -> 20250930`
    已因
    `688981.SH`
    缺行被放弃
  - 实跑成功的第三窗为：
    - `20250909 -> 20251212`
  - `net total_return`
    与
    `holdout net total_return`
    形成：
    - `2 positive / 1 negative`
      的多数恢复
  - 但
    `net active_total_return`
    形成：
    - `1 positive / 2 negative`
      的多数偏负
  - 因此当前三窗只能写成：
    - `cross_window_return_sign_majority_positive__active_sign_majority_negative__still_need_evidence`
  - 当前不继续默认抓第四窗，
    而是再次交回 `Cursor`
    统筹更窄解释层
- 当前 `active_underperformance_v0` 又显示：
  - 当前并未新增任何 runtime
    或新回测
  - 只是把三窗之后最核心的张力正式点名为：
    - `active underperformance`
  - 当前解释层结论仍保持：
    - `cross_window_return_sign_majority_positive__active_sign_majority_negative__still_need_evidence`
  - 当前解释层完成后可先停在：
    - `still_need_evidence`
- 当前不回退否定工程链。
- 当前不扩成完整回测平台。

## 回链

- `00_entry/全库资料整理收口__20260713/A5_financial_validity_gate最小入口与通过标准页__20260719.md`
- `00_entry/全库资料整理收口__20260713/A5_execution_validation到financial_validity_gate阶段切换页__20260718.md`
- `02_runtime/a5_g5_min_chain_validation/artifacts/a5_g5_same_batch_boundary_audit_latest.json`
