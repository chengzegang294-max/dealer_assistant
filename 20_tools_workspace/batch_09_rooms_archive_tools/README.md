# batch_09_rooms_archive_tools — 一房一档入库工具

创建日期：2026-08-11  
家族：[rooms/](file:///d:/Stock/dealer_assistant/02_runtime/info_live_room_sampling/rooms)

**负责：** 磁盘上已有 export JSON → 分房归档 / 刷索引。  
**不负责：** 登录站点、点房、贴 JS 出站。

| 脚本 | 用法 | 何时 |
|------|------|------|
| `migrate_raw_from_batch05_and_batch07_to_rooms_v1.py` | 默认 dry-run；`--apply` 真复制 | Raw 进 batch 后 |
| `sentinel_update_rooms_index_v1.py` | `--rooms-root .../rooms` | migrate 后 |

识别顺序：`room_anchor` → `forced_room_anchor` → heuristics → 父目录 `priority_rooms/<房>/` → 别名。  
C/D 桶勿迁入 rooms。
