# 信息直播间 rooms 家族（一房一档 · 定点闭环）

创建日期：2026-08-11 · 补洞流程对接 2026-08-12  
家族根：`02_runtime/info_live_room_sampling/rooms/`

---

## 当前优先（2026-08-12 纠偏）

**只做两件事，盯梢后置：**

1. 每天人工续导（RESUME，可用 `max_rounds` 主动停）  
2. JSON → 规范 MD（`10_ingest`）  

正式说明：[A5_Cursor同步包_直播间每日续导与JSON转MD__20260812.md](file:///d:/Stock/dealer_assistant/00_entry/A5_Cursor同步包_直播间每日续导与JSON转MD__20260812.md)

机构电话 / 机构研报：**FROZEN_OUT**（不参与每日置顶；跳过自动摘要；只在 SKIP_ROOMS 保留）。  
不要把 Prefill 词频当成已吸收。

- [A5_直播间A加B_Raw补洞执行令__20260812](file:///d:/Stock/dealer_assistant/02_runtime/info_live_room_sampling/batch_08_rooms_backfill__20260812/A5_直播间A加B_Raw补洞执行令__20260812.md)
- [Trae 同步包](file:///d:/Stock/dealer_assistant/00_entry/A5_Cursor同步包_直播间Raw补洞对接Trae__20260812.md)
- 中转篮：`../batch_08_rooms_backfill__20260812/00_raw/`

**不要再建房文件夹；** 本目录 24 房已齐。JSON 先丢中转篮 → migrate 复制进 `*/00_raw/`。  
**阶段 1 未完成前不要开盯梢主线。**

---

## 「能不能自动化」——诚实版

| 段 | 内容 | 自动化（现状） |
|----|------|----------------|
| **L0 出站** | 登录 mx2025 → 进房 → 贴 JS → JSON | **仍要人** |
| **L1～L3 入库** | 分房、索引、草稿、要点确认 | L1 脚本；L2 AI+确认；L3 人拍板 |

工具：`20_tools_workspace/batch_09_rooms_archive_tools/`  
导出 JS：`20_tools_workspace/batch_07_info_live_room_tools/`

**正史只认 `20_absorb/` 且已确认后**；补洞阶段只要求 `00_raw` 有 JSON。

C/D 禁止进本家族。微信金十已停线。  
索引：`SENTINEL_INDEX.md`  
