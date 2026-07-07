# Batch98 Kimi Inbox Name Collision Target Fill

## Scope

- source: `name_collision_manual_review__20260707.tsv`
- rule: `PROMOTE_INCOMING_TO_PROPOSED_TARGET__KEEP_EXISTING_BASENAME_VARIANTS`
- goal: 对仅 basename 冲突但目标路径缺失的 22 条记录，保守并存补齐到 proposed target 路径，不覆盖 mirror 中既有同名异内容文件

## Outputs

- fill manifest: `fill_manifest__20260707.tsv`
- fill report: `fill_report__20260707.json`
