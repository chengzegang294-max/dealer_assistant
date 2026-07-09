# 批次 01 Cross Line Frozen 执行卡

## 生成入口

- `PRODUCER`: `historical_recovered_copy`
- `SOURCE_SCOPE`: `cross_line_frozen minimal set`
- `MAIN_ENTRY`:
  - `cross_line_frozen_min_set/cross_line_frozen_current_manifest_v1.md`

## 当前作用

- 为 `cross_line_frozen` 顶层最小冻结链提供批次级执行说明。
- 本批次属于历史运行时锚点归档，不作为当前业务 first-hop 入口。
- 更长链的运行时材料继续通过 `legacy_file_map` 追溯，不回流到默认入口层。

## 证据强度

- `evidence_mode=historical_recovered`
