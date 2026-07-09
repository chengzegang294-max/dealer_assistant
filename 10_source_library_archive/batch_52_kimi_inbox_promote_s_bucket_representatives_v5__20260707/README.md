# Batch52 Kimi Inbox Promote (S_BUCKET representatives_v5)

## 用途

- 这批材料把 `S_BUCKET representatives_v5` 从 staging 路径迁入 `mirror_kimi_inbox` 的稳定目标位置。
- 当前只承担来源层承接与归档整理作用，不作为默认阅读入口。

## 当前包含

- `incoming=S_BUCKET__staging/03_券商研报/representatives_v5`
- `target=10_source_library_archive/mirror_kimi_inbox/S_BUCKET__staging/03_券商研报/representatives_v5`

## 当前裁决

- 本批次按 `source_library promote batch` 口径保留。
- 当前作用是把 staging 材料稳定迁入 `mirror_kimi_inbox`，不把本批 README 当作默认阅读入口。
- 默认阅读入口继续看目标目录及其上位索引卡。

## 批次产物

- `promote_manifest__20260707.tsv`
- `promote_report__20260707.json`
