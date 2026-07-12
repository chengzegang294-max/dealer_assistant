# AShare P0 First Round Validation Provenance Note v1

更新时间：2026-07-12

## 用途

- 记录本目录当前 `GENERATOR / INDEX_NOTE / ARTIFACT` 的最小追溯关系。
- 防止后续新增脚本和结果后，只看到文件名，看不出谁生成、给谁用、证据强弱如何。

## 当前文件分类

### GENERATOR

- `run_t01_volume_price_scan_v1.py`
  - 当前作用：
    - 扫描日线 OHLCV CSV，输出 `T01` 触发密度摘要
  - 默认输入：
    - `02_runtime/butler_r0_ohlcv_object_cards/data/raw/daily_ohlcv/batch09_promoted/ashare_clean/`
  - 默认产物：
    - `artifacts/t01_volume_price_scan/`
  - 证据强度：
    - `hard`（当前终端新跑结果时）
- `run_t01_industry_distribution_v1.py`
  - 当前作用：
    - 基于 `T01` 标的级触发统计和临时行业映射，输出行业分布摘要
  - 默认输入：
    - `artifacts/t01_volume_price_scan/t01_symbol_trigger_counts_latest.tsv`
    - `02_runtime/butler_r0_ohlcv_object_cards/data/raw/watchlist_inputs/batch09_promoted/structured_inputs/factors_ladder_20260508.csv`
  - 默认产物：
    - `artifacts/t01_industry_distribution/`
  - 证据强度：
    - `hard`（当前终端新跑结果时）
- `run_t02_fund_flow_scan_v1.py`
  - 当前作用：
    - 扫描资金字段 CSV，输出 `T02` 连续主力资金触发摘要
  - 默认输入：
    - 运行时显式传入的资金 CSV
  - 默认产物：
    - `artifacts/t02_fund_flow_scan/`
  - 证据强度：
    - `hard`（当前终端新跑结果时）

### INDEX_NOTE

- `README.md`
- `runtime_execution_card_v1.md`
- `artifact_index_v1.tsv`
- `data/README.md`
- `data/t02_fund_flow_input_contract_v1.csv`
- `reports/*.md`
- `artifacts/README.md`

### ARTIFACT

- 当前尚未默认跟踪真实统计产物。
- 当 runner 首次生成结果后，至少要补：
  - `producer`
  - `scope`
  - `status`
  - `evidence_mode`

## 当前结果与缺口

- 当前已补第一份 `T01` fresh-run 结果：
  - `artifacts/t01_volume_price_scan/t01_volume_price_scan_summary_latest.json`
  - `artifacts/t01_volume_price_scan/t01_trigger_detail_latest.tsv`
  - `artifacts/t01_volume_price_scan/t01_daily_trigger_counts_latest.tsv`
  - `artifacts/t01_volume_price_scan/t01_symbol_trigger_counts_latest.tsv`
- `T01` 当前 smoke-run 口径：
  - 时间窗：`2025-05-08 -> 2026-05-08`
  - 输入目录：`butler_r0_ohlcv_object_cards/data/raw/daily_ohlcv/batch09_promoted/ashare_clean`
  - 当前摘要：`46` 个文件、`520` 条触发、`204` 个触发日、峰值日 `19`
- 当前已补第一份 `T01` 行业分布结果：
  - `artifacts/t01_industry_distribution/t01_industry_distribution_summary_latest.json`
  - `artifacts/t01_industry_distribution/t01_industry_trigger_counts_latest.tsv`
  - `artifacts/t01_industry_distribution/t01_symbol_industry_join_latest.tsv`
  - `artifacts/t01_industry_distribution/t01_unmatched_symbols_latest.tsv`
- `T01` 当前行业映射覆盖：
  - 匹配标的：`17/44`
  - 触发权重覆盖：`181/520`
  - 当前结论：仅适合做临时行业分布观察，不足以作为正式行业统计真值
- `T02` 当前已补统一输入合同模板：
  - `data/t02_fund_flow_input_contract_v1.csv`
- `T02` 还缺首份资金字段输入 CSV
- 还未补统一批次汇总脚本

## 当前回链

- `artifact_index_v1.tsv`
- `runtime_execution_card_v1.md`
- `00_entry/A股_P0_离线验证执行卡__20260712.md`
