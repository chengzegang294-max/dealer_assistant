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
- `t02_fund_flow_scan/`
  - `t02_fund_flow_scan_summary_latest.json`
  - `t02_trigger_detail_latest.tsv`
  - `t02_symbol_trigger_counts_latest.tsv`
  - `t02_regime_trigger_counts_latest.tsv`
  - 当前口径：
    - 模板级 smoke-run
    - 输入行数：`1`
    - 触发数：`0`

## 当前回链

- runtime 执行卡：
  - `02_runtime/ashare_p0_first_round_validation/runtime_execution_card_v1.md`
- repo 级产出落点说明：
  - `00_entry/A股_P0_离线验证产出落点说明__20260712.md`
