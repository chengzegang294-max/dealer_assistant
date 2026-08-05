# Batch 131 Entry History Process Docs

更新时间：2026-08-06

## 1. 批次作用

- 本批次用于承接 `00_entry/全库资料整理收口__20260713` 中第一批“历史过程稿”迁档。
- 本轮已完成第一批真实迁档，不再停留在预留目标态。

## 2. 来源路径

- 源目录：
  - [00_entry/全库资料整理收口__20260713](file:///d:/Stock/trading_assistant/00_entry/全库资料整理收口__20260713)

## 3. 第一批拟迁档对象族

1. `A5_Cursor同步包_*`
2. `A5_Cursor编码向任务包_*`
3. `A5_Cursor发起多AI_*`
4. `A5_Cursor主导_*讨论包`
5. `*_多家AI正式发包稿__*`
6. `*_OpenWebUI纯文本发包稿__*`
7. `*_超窄纯文本正式发包稿__*`
8. `*_多家AI回收记录模板__*`
9. `*_超窄纯文本回收记录模板__*`
10. `*走查记录*`

## 4. 本轮已迁入结果

- `cursor_packs/`：15 份
- `multi_ai_packets/`：68 份
- `walkthrough_records/`：11 份
- 合计：94 份

对应关系清单：

- [migration_manifest.tsv](file:///d:/Stock/trading_assistant/11_frozen_summaries_archive/batch_131_entry_history_process_docs__20260806/migration_manifest.tsv)

## 5. 当前状态

- 状态：`first_batch_migrated`
- 当前动作：已按文档族完成首批迁档，并在源目录回填回指说明
- 下一手：继续判断是否要迁第二批“过程稿但仍留在入口层”的对象

## 6. 迁档原则

- 迁档对象必须是“过程追溯稿”，不能误搬当前主线入口
- 源目录仍承担历史索引作用时，不直接整体挪空
- 迁档后必须保留：
  - 批次 README
  - 迁档对象族说明
  - 原路径与新路径对应关系

## 7. 子目录说明

- [cursor_packs](file:///d:/Stock/trading_assistant/11_frozen_summaries_archive/batch_131_entry_history_process_docs__20260806/cursor_packs)
  - `Cursor` 同步包、编码向任务包、主导讨论包
- [multi_ai_packets](file:///d:/Stock/trading_assistant/11_frozen_summaries_archive/batch_131_entry_history_process_docs__20260806/multi_ai_packets)
  - 多 AI 正式发包稿、回收模板、OpenWebUI/超窄纯文本发包稿
- [walkthrough_records](file:///d:/Stock/trading_assistant/11_frozen_summaries_archive/batch_131_entry_history_process_docs__20260806/walkthrough_records)
  - 走查记录类过程稿

## 8. 主负责人裁决

- 第一批真实迁档已完成。
- 当前不做第二批大范围搬运，先让入口层稳定下来再继续分层。
