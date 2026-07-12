# AShare P0 First Round Validation Artifacts

更新时间：2026-07-12

## 用途

- 这里放 A 股 P0 首轮离线验证的统计表、日志、导出表和后续批次归档说明。
- 当前只建立边界说明，不预创建大体量空目录树。

## 计划承接的产物

- `csv`
  - 统计摘要
  - 抽样明细
- `tsv`
  - 汇总对照表
- `log`
  - 运行日志
- `json`
  - 若后续需要结构化摘要，可在本层承接

## 当前规则

- 新跑出的结果优先按批次放在本层。
- 大体量或历史回收结果，必要时同步归档到：
  - `12_tooling_runtime_archive/<validation_batch>/`
- 每批产物至少要写清：
  - `producer`
  - `scope`
  - `status`
  - `evidence_mode`

## 当前已存在产物

- `t01_volume_price_scan/`
  - `t01_volume_price_scan_summary_latest.json`
  - `t01_trigger_detail_latest.tsv`
  - `t01_daily_trigger_counts_latest.tsv`
  - `t01_symbol_trigger_counts_latest.tsv`
  - 当前口径：
    - 时间窗：`2025-05-08 -> 2026-05-08`
    - 结果摘要：`520` 条触发、`204` 个触发日、峰值日 `19`
- `t01_industry_distribution/`
  - `t01_industry_distribution_summary_latest.json`
  - `t01_industry_trigger_counts_latest.tsv`
  - `t01_symbol_industry_join_latest.tsv`
  - `t01_unmatched_symbols_latest.tsv`
  - 当前口径：
    - 行业映射来源：`factors_ladder_20260508.csv`
    - 匹配标的：`17/44`
    - 触发权重覆盖：`181/520`
- `t02_input_audit/`
  - `t02_input_audit_summary_latest.json`
  - `t02_missing_columns_latest.tsv`
  - 当前口径：
    - 模板输入行数：`1`
    - `contract_ready = true`
- `t02_input_prepare/`
  - `t02_input_prepare_summary_latest.json`
  - `t02_fund_flow_input_normalized_latest.csv`
  - 当前口径：
    - `missing_columns = []`
    - 标准化列名链已贯通
- `t02_real_input_build/`
  - `t02_real_input_build_summary_latest.json`
  - `t02_real_input_candidate_latest.csv`
  - 当前口径：
    - latest 跨月真实宽表
    - 输入行数：`1200`
    - join 命中：`northbound=1140/1200`、`regime=1200/1200`、`industry=1200/1200`
- `t02_fund_flow_scan/`
  - `t02_fund_flow_scan_summary_latest.json`
  - `t02_trigger_detail_latest.tsv`
  - `t02_symbol_trigger_counts_latest.tsv`
  - `t02_regime_trigger_counts_latest.tsv`
  - `t02_symbol_regime_trigger_counts_latest.tsv`
  - `t02_sample_expansion_comparison_latest.tsv`
  - `t02_time_window_stability_latest.tsv`
  - 当前口径：
    - latest 跨月真实扫描
    - 输入行数：`1200`
    - 触发数：`493`
    - 触发标的：`20`
- `t02_layer_stability/`
  - `t02_layer_stability_summary_latest.json`
  - `t02_symbol_layer_stability_latest.tsv`
  - `t02_macro_bucket_stability_latest.tsv`
  - `t02_flow_volatility_bucket_stability_latest.tsv`
  - 当前口径：
    - latest 分层稳定性分析
    - 最强宏观层：`金融=49.4%`
    - 最弱宏观层：`成长科技=35.6%`
    - 波动层：`high=45.0%`、`mid=44.7%`、`low=34.1%`
- `t02_local_tuning/`
  - `t02_local_tuning_summary_latest.json`
  - `t02_local_tuning_scenario_comparison_latest.tsv`
  - `t02_local_tuning_recommendation_latest.tsv`
  - 当前口径：
    - latest 局部阈值试算
    - `3% + 连续1日` 被判定为全局过松
    - 当前仅保留 `low_flow_vol` 与 `growth_tech_low_flow_vol` 的 `2.5% + 连续2日` watchlist 候选
- `t02_local_tuning_review/`
  - `t02_local_tuning_review_summary_latest.json`
  - `t02_local_tuning_group_review_latest.tsv`
  - `t02_local_tuning_added_trigger_detail_latest.tsv`
  - 当前口径：
    - latest watchlist 噪声风险复核
    - 新增触发主要集中在 `G03_震荡`
    - `low_flow_vol` 与 `growth_tech_low_flow_vol` 当前仍只保留弱候选地位
- `t02_confirmation_filter/`
  - `t02_confirmation_filter_summary_latest.json`
  - `t02_confirmation_filter_scenario_comparison_latest.tsv`
  - `t02_confirmation_filter_recommendation_latest.tsv`
  - 当前口径：
    - latest watchlist 确认条件过滤试算
    - 首选第一道过滤：`排除 G03_震荡`
    - `北向同向` 当前更适合作为第二层加严条件
- `t02_candidate_branch/`
  - `t02_candidate_branch_summary_latest.json`
  - `t02_candidate_branch_decision_latest.tsv`
  - 当前口径：
    - latest 观察型候选分支裁决
    - `2.5% + 连续2日 + 排除 G03_震荡` 当前仍不升级为 `微调`
    - 当前无可直接接管 baseline 的局部分支

## 当前回链

- runtime 执行卡：
  - `02_runtime/ashare_p0_first_round_validation/runtime_execution_card_v1.md`
- repo 级产出落点说明：
  - `00_entry/A股_P0_离线验证产出落点说明__20260712.md`
