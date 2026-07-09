# Batch98 Kimi Inbox Name Collision Target Fill

## 用途

- 这批材料用于把仅 `basename` 冲突但目标路径缺失的 `22` 条记录，保守并存补齐到 `proposed target` 路径。
- 当前只承担来源层补位与审计对齐作用，不作为默认阅读入口。

## 当前包含

- `source=name_collision_manual_review__20260707.tsv`
- `rule=PROMOTE_INCOMING_TO_PROPOSED_TARGET__KEEP_EXISTING_BASENAME_VARIANTS`
- `goal=不覆盖 mirror 中既有同名异内容文件，补齐缺失的 proposed target 路径`

## 当前裁决

- 本批次按 `source_library fill batch` 口径保留。
- 当前作用是处理名称冲突下的保守补位，不把本批 README 当作默认阅读入口。
- 默认阅读入口继续看 `mirror_kimi_inbox` 实体目录与上位索引材料。

## 批次产物

- `fill_manifest__20260707.tsv`
- `fill_report__20260707.json`
