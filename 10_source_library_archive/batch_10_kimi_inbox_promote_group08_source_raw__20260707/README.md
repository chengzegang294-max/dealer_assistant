# Batch10 Kimi Inbox Promote (GROUP_08 SOURCE_RAW)

## Scope

- 目的：把 `mirror_kimi_inbox_incoming` 中一簇可明确归属的材料，按新仓 canonical 结构迁入 `mirror_kimi_inbox`。
- 口径：迁入的是“归档承接”；后续仍需在 `GROUP_08_*` 的入口卡里完成去重/目录说明/使用边界。

## Source

- incoming root: `10_source_library_archive/batch_09_legacy_source_library_alignment__20260707/mirror_kimi_inbox_incoming`

## Target

- mirror root: `10_source_library_archive/mirror_kimi_inbox`
- 本批次约定的 canonical 迁入前缀：
  - incoming: `GROUP_08_A股量化_数据研究__SOURCE_RAW/`
  - mirror: `GROUP_08_A股量化_数据研究/01_source_raw/`

## Outputs

- promoted manifest: `promote_manifest__20260707.tsv`
- promote report: `promote_report__20260707.json`

