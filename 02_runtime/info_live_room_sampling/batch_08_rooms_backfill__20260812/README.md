# batch_08_rooms_backfill__20260812 — A桶9房（2026-08-11交易日）闭市回补执行卡

## 一、结论（先给结果）

**A桶 9 房 8.11 回补导出：8/9 房已就位，先知（A#9）今日未补（漏 1 间）。**

**⚠️ 用户2026-08-12声明撤回2间：机构电话会议纪要+小作文+情报（A#4）/机构研报资讯精选（B#23别名独角兽）机器今日已生成Prefill草稿+人读摘要 2件机器产物已全部撤回删除（00_raw原始JSON保留不碰），后续用户自己重做，盯梢暂扫A#4但不吸收**

SHA 迁移验证（禁止反向覆盖）：**13/13 文件 11 件匹配 + 2 件别名补Copy → 最终 13/13 就位，CONFLICT=0（零反向覆盖）**。

---

## 二、事实依据（1-3-3 格式）

### 2.1 导出源文件清单（13 件，00_raw/）

| # | 文件名 | 房间归属（正式） | 大小 KB | 20260811 前缀导出时间 |
|---|--------|----------------|--------|---------------------|
| 1 | info_live_export__20260811_172830.json | ⚠️ 机构研报资讯精选（独角兽别名·用户2026-08-12说自己重做·机器今日已撤稿） | — | 17:28:30 |
| 2 | info_live_export__20260811_173718.json | ⚠️ 机构研报资讯精选（独角兽别名·用户2026-08-12说自己重做·机器今日已撤稿） | — | 17:37:18 |
| 3 | info_live_incremental_export__20260811_173527.json | ⚠️ 机构电话会议纪要+小作文+情报（A#4·用户2026-08-12说自己重做·Prefill草稿+人读摘要2件今天已删） | 767.4 | 17:35:27 |
| 4 | info_live_incremental_export__20260811_173731.json | ⚠️ 机构研报资讯精选（用户2026-08-12说自己重做·机器今日已撤稿） | <1 | 17:37:31 |
| 5 | info_live_incremental_export__20260811_174434.json | 独家老师5号 | 937.2 | 17:44:34 |
| 6 | info_live_incremental_export__20260811_174816.json | 独家短线老师6号 | 453.5 | 17:48:16 |
| 7 | info_live_incremental_export__20260811_175057.json | 梅森 | 540.4 | 17:50:57 |
| 8 | info_live_incremental_export__20260811_175306.json | 顺势而为 | 280.3 | 17:53:06 |
| 9 | info_live_incremental_export__20260811_175515.json | 混江龙 | 448.8 | 17:55:15 |
| 10 | info_live_incremental_export__20260811_175712.json | 天赢居 | 540.7 | 17:57:12 |
| 11 | info_live_incremental_export__20260811_180810.json | 复盘哥 | 851.9 | 18:08:10 |
| 12 | info_live_incremental_export__20260811_181824.json | 独家老师5号（第二份） | 937.2 | 18:18:24 |
| 13 | info_live_incremental_export__20260811_182502.json | 独家老师5号（第三份） | 1389.7 | 18:25:02 |

### 2.2 A 桶 9 房就位矩阵

| 房间（正式名） | 分桶 # | 今日 20260811 导出是否就位 | 先知漏 YES/NO |
|---|---|---|---|
| 复盘哥 | A1 | ✅ 1 件（18:08:10） | — |
| 独家老师5号 | A2 | ✅ 3 件（17:44 / 18:18 / 18:25） | — |
| 独家短线老师6号 | A3 | ✅ 1 件（17:48:16） | — |
| ⚠️ 机构电话会议纪要+小作文+情报（用户2026-08-12说自己重做·机器今日Prefill+人读摘要已删） | A4 | ✅ 1 件（17:35:27） | — |
| 梅森 | A5 | ✅ 1 件（17:50:57） | — |
| 顺势而为 | A6 | ✅ 1 件（17:53:06） | — |
| 混江龙 | A7 | ✅ 1 件（17:55:15） | — |
| 天赢居 | A8 | ✅ 1 件（17:57:12） | — |
| 先知 | A9 | ❌ **0 件** | YES（漏导出） |

### 2.3 双仓合规 / 禁止反向覆盖

- CONFLICT=0 / SKIP_IDENTICAL=11 / OK_TO_COPY_NOT_EXIST=2（机构研报精选别名漏识别 → 补Copy到位，PostCopy SHA 双匹配）
- 新仓仅写 `02_runtime/info_live_room_sampling/` 家族 + 本 README（正式主线内容）；试验内容零写入

---

## 三、操作 3 步（盯梢与闭环）

```
Step 1（先知补漏 1 分钟）：下次开工打开 quicktiny 导出 先知 8.11 增量 → 放本批 00_raw/ → 执行：
  python migrate_raw_from_batch05_and_batch07_to_rooms_v1.py --apply --batch-dir 02_runtime/info_live_room_sampling/batch_08_rooms_backfill__20260812/00_raw

Step 2（NOTES 事实预填 3 分钟/间 × 8 间，全自动不判）：
  python prefill_A9_rooms_notes_v1.py --trade-date 20260811 --rooms-root 02_runtime/info_live_room_sampling/rooms --apply-draft

Step 3（人工判断回填 10 分钟/间，可选）：
  逐间打开 10_ingest/*_machine_draft.md 抄 NOTES_partial_prefill 进 20_absorb/NOTES.md → 填「已吸收 @ 2026-08-12」
```
