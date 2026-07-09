# Batch97 Kimi Inbox Duplicate Target Fill

## 用途

- 这批材料用于把 `sha256` 已存在于 `mirror` 其他路径的 `59` 条记录，补齐到审计要求的 `proposed target` 路径。
- 当前只承担来源层补位与审计对齐作用，不作为默认阅读入口。

## 当前包含

- `source=duplicate_keep_mirror_review__20260707.tsv`
- `rule=COPY_EXISTING_MIRROR_TO_PROPOSED_TARGET__KEEP_BOTH_PATHS`
- `goal=对 mirror 既有内容补齐 proposed target 路径`

## 当前裁决

- 本批次按 `source_library fill batch` 口径保留。
- 当前作用是补齐审计所需目标落点，不把本批 README 当作默认阅读入口。
- 默认阅读入口继续看 `mirror_kimi_inbox` 实体目录与上位索引材料。

## 批次产物

- `fill_manifest__20260707.tsv`
- `fill_report__20260707.json`
