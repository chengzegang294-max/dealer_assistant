# A5 Cursor 同步包 · 直播间 Raw 补洞对接 Trae

更新时间：2026-08-12  
工作仓：**只用** `d:\Stock\dealer_assistant`  
目的：把「补 A+B 缺洞 Raw → 再盯梢」正式交给 Trae / 下一任助手，避免再建房文件夹或改微信金十。

---

## 1. Trae 接手时只读这 4 份（按序）

1. **本同步包**（你在读）  
2. **执行令（主流程）**  
   [A5_直播间A加B_Raw补洞执行令__20260812.md](file:///d:/Stock/dealer_assistant/02_runtime/info_live_room_sampling/batch_08_rooms_backfill__20260812/A5_直播间A加B_Raw补洞执行令__20260812.md)  
3. **中转篮 + 清单**  
   [batch_08 README](file:///d:/Stock/dealer_assistant/02_runtime/info_live_room_sampling/batch_08_rooms_backfill__20260812/README.md)  
   [CHECKLIST.md](file:///d:/Stock/dealer_assistant/02_runtime/info_live_room_sampling/batch_08_rooms_backfill__20260812/CHECKLIST.md)  
4. **正史柜说明（诚实自动化边界）**  
   [rooms/README.md](file:///d:/Stock/dealer_assistant/02_runtime/info_live_room_sampling/rooms/README.md)  

交接总览（回填用）：  
[A5_新仓交接总记录__20260809.md](file:///d:/Stock/dealer_assistant/00_entry/A5_新仓交接总记录__20260809.md)

---

## 2. 用户当前意图（冻结）

- **阶段 1（现在）：** 补齐 A+B 缺洞 Raw，再谈 NOTES/盯梢  
- **阶段 2：** 仅当 24 房 Raw 全 >0 后，才开 `midday_watch`  
- **不用**新建每房文件夹；只用 `rooms/` + 中转篮  
- **微信金十停线**；出站导出必须用户浏览器登录  

---

## 3. Trae / Cursor 职责切分

| 角色 | 做 | 不做 |
|------|----|------|
| 用户 | 登录 mx2025、按房点历史、贴 JS、JSON 丢中转篮 | 手建 rooms 子文件夹体系 |
| Trae/Cursor | 收到「今日 Raw 已入档」→ migrate + sentinel；勾清单/回填交接；导出失败时只记缺口 | 声称全自动抓站；搬 C/D 进 rooms；微信 Cookie；未补洞就开盯梢全库任务 |

---

## 4. 口令（可直接粘）

### 用户导出后

```text
今日直播间 Raw 已入档。
中转路径：d:\Stock\dealer_assistant\02_runtime\info_live_room_sampling\batch_08_rooms_backfill__20260812\00_raw
请 migrate --apply + 刷新 SENTINEL_INDEX，回报各房 Raw 数。
```

### Trae 项目命令

设置里可再建：`/live-backfill`（正文见 `.trae/TRAE_COMMANDS_BACKUP__20260810.md` 命令 5）

### 开工

```text
按 A5_直播间A加B_Raw补洞执行令 帮我推进补洞。
当前先盯 A 缺 7 房；我不说完成不要开 midday_watch。
```

---

## 5. 最小命令（AI 侧）

```powershell
cd d:\Stock\dealer_assistant\20_tools_workspace\batch_09_rooms_archive_tools
python migrate_raw_from_batch05_and_batch07_to_rooms_v1.py --batch-dir "d:\Stock\dealer_assistant\02_runtime\info_live_room_sampling\batch_08_rooms_backfill__20260812\00_raw" --apply
python sentinel_update_rooms_index_v1.py --rooms-root "d:\Stock\dealer_assistant\02_runtime\info_live_room_sampling\rooms"
```

---

## 6. 一句话同步（可转 Trae）

> 直播间补洞阶段 1 已正式落新仓：中转篮 batch_08_rooms_backfill__20260812、执行令、CHECKLIST、rooms 24 房正史柜已齐。用户从 A「复盘哥」起在独立浏览器导 JSON 丢 00_raw；丢完报「今日 Raw 已入档」做 migrate+sentinel。未补齐前禁止盯梢主线扩张、禁止微信金十、禁止另建房目录。

### 追加 · 2026-08-12 夜间 B 桶本批（已吸收 raw）

正式回报：  
[A5_B桶本批吸收回报__20260812.md](file:///d:/Stock/dealer_assistant/02_runtime/info_live_room_sampling/batch_08_rooms_backfill__20260812/A5_B桶本批吸收回报__20260812.md)

| B 房本批 | 条数 | stop |
|----------|------|------|
| 游资胖大叔 | 374 | scroll_end |
| 潜伏王者 | 370 | scroll_end |
| 擒龙小师姐 | 272 | scroll_end |
| 独家竞价低吸 | 250 | scroll_end |

### 追加 · night2（28 文件 · 2026-08-12 03:55）

正式回报：  
[A5_AB本批吸收回报__20260812_night2.md](file:///d:/Stock/dealer_assistant/02_runtime/info_live_room_sampling/batch_08_rooms_backfill__20260812/A5_AB本批吸收回报__20260812_night2.md)

- 28/28 copy + migrate；覆盖 **13 房**（A：先知、机构电话…；B：天机/k神/周期女王/格兰/小锦鲤/核心逻辑社/梦幻一步/新生代/龙头/机构研报/小作文嗅嗅 等）  
- 全部 **raw 入柜**；**SENTINEL 已刷**；NOTES 未做  
- 机构电话 / 机构研报：本批有有效条数，**解除「禁止入 raw」**；引用跳过 0 条文件  
- 24 房 SENTINEL **Raw 文件数均 >0**，阶段 1 补洞从索引看可收口  

B 早前批次回报仍有效：`A5_B桶本批吸收回报__20260812.md`  
