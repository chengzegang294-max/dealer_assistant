# 批次 09 Legacy Analysis Migration（20260707）

## 用途

- 这是一批旧仓库分析资产的迁移与对齐审计产物归档包。
- 本批次包含：
  - `lifted_trading_analysis/`：旧分析仓库的 lifted 快照（含大量来源文档与旧 `.trae` 目录快照）
  - `inventory_*` / `gaps_*`：对齐盘点与缺口分析的汇总 TSV/JSON
  - `*_v1.py`：用于生成盘点/对齐/缺口报告的脚本（作为历史证据保留）

## 边界

- 本批次属于 `12_tooling_runtime_archive/` 的历史归档包，不作为日常入口。
- 若后续需要把其中某段内容提升为仓库真值入口，必须按目录合同提升归位到对应层（`00_entry/02_runtime/10_source_library_archive` 等）。

## 入口

- 执行卡：
  - `BATCH_09_LEGACY_ANALYSIS_MIGRATION_EXECUTION_CARD__20260707.md`
- 产物索引：
  - `BATCH_09_LEGACY_ANALYSIS_MIGRATION_ARTIFACT_INDEX__20260707.tsv`
