# Batch 120 Tools Workspace Absorb

## 用途

- 吸收 `20_tools_workspace` 中不再适合继续停留在合同外工作区、但仍需要保留来源形态的材料。
- 当前批次先收 `session_clip` 这类会话级临时粘贴快照，不把它误判成运行时正式输入。

## 入口

- `INDEX_NOTE`:
  - 当前文件
  - `manifest_v1.tsv`
  - `01_index/promotion_map_v1.tsv`
  - `00_raw_snapshot/session_clip/README.md`

## 当前范围

- `00_raw_snapshot/session_clip/`

## 当前结构

- `00_raw_snapshot/session_clip/`
  - 回收的 session clip 原样快照
- `01_index/promotion_map_v1.tsv`
  - 批次级最小回指与入口映射
- `manifest_v1.tsv`
  - 批次级最小清单

## 证据口径

- 本批材料属于 `historical_recovered`
- 当前作用是保留历史排查现场，不作为默认入口真源

## 当前裁决

- 当前批次保留在 `10_source_library_archive` 是合理的：
  - 它已经不适合继续放在 `20_tools_workspace`
  - 但也不应被提升到 `00_entry / 02_runtime / 04_active_main_docs`
- 默认阅读顺序：
  - 先看当前批次 README
  - 再进 `00_raw_snapshot/session_clip/README.md`
  - 最后才看具体快照文件
