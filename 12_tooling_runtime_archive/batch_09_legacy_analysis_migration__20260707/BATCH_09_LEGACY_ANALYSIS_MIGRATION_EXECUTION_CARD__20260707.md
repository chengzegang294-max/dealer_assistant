# Batch 09 Legacy Analysis Migration Execution Card (20260707)

## 生成入口

- `PRODUCER`: `legacy_analysis_migration_tooling`
- `SCOPE`: `legacy analysis inventory + alignment audit + gaps reports`
- `EVIDENCE_MODE`: `historical_recovered`

## 当前作用

- 为旧分析仓库的 lifted 快照与盘点审计产物提供可追溯归档落点。
- 本批次仅作为历史证据与审计留存，不作为当前 repo 的 first-hop 入口。

## 关键产物

- `lifted_trading_analysis/`：lifted 快照目录（含大量来源文档与旧 `.trae`）
- `legacy_analysis_inventory__*.tsv` / `legacy_analysis_inventory__*.summary.json`：盘点结果
- `inventory_compare_src_vs_dst__20260707*.json`：对齐对比
- `gaps_*__20260707.tsv` / `gaps_*__20260707.summary.json`：缺口分析
- `legacy_analysis_ref_rewrite_report__20260707.json`：引用改写报告（若存在）
