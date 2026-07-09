# 批次 07 Legacy Docs Batches 执行卡

## 生成入口

- `PRODUCER`: `historical_recovered_copy`
- `SOURCE_SCOPE`: `legacy docs batch evaluations and commit-ready notes`
- `MAIN_ENTRY`:
  - `README.md`
  - `legacy_docs_batches/`

## 当前作用

- 为旧 `docs/` 中的阶段性评估与 `commit-ready` 批次文档提供批次级执行说明。
- 本批次属于历史迁移与审阅文档归档，不作为当前业务 first-hop 入口。
- 若后续需要当前有效批次计划，应继续提升到 `00_entry/` 或 `04_active_main_docs/`，不直接回退到本批历史文档。

## 证据强度

- `evidence_mode=historical_recovered`
