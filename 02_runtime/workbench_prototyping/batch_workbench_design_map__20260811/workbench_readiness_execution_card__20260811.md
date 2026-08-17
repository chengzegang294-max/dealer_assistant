# 工作台 READINESS 执行卡 · 2026-08-11

> 数据源：`design_field_mapping__20260811.tsv` · 6区块 × 62字段 · 整体就绪度 **64%**

---

## 一、6 区块总览

| 区块 | 字段数 | 已就绪 | 就绪率 | 就绪度条 |
|------|--------|--------|--------|----------|
| ① 盘前方向卡 preopen | 15 | 9 | **60%** | ████████████░░░░░░░░░░ |
| ② 盘中确认卡 intraday | 7 | 1 | **14%** | ███░░░░░░░░░░░░░░░░░░░ |
| ③ 盘后复盘卡 afterclose | 9 | 3 | **33%** | ███████░░░░░░░░░░░░░░░ |
| ④ 连板天梯 stock_row | 17 | 16.5 | **97%** | ████████████████████▌░ |
| ⑤ 行业板块 sector_row | 7 | 7 | **100%** | ██████████████████████ |
| ⑥ 直播间 rooms | 7 | 3 | **43%** | ████████▋░░░░░░░░░░░░░ |
| **合计** | **62** | **39.5** | **64%** | █████████████▌░░░░░░░░ |

---

## 二、各区块详情

### ① 盘前方向卡 / preopen · 60%

**已就绪字段（9/15）：**
- `trade_date` / 交易日
- `最高板 / T1 / 市场高度`
- `P_ge2 / ≥2板数 / 连板梯队`
- `总连板池 / totalStocks`
- `梯队分布(5板x2/3板x2/2板x9/1板x86)`
- `ladder_yesterday_fact / 连板结构摘要`
- `sector_snapshot_ref / 行业快照路径`
- `行业Top5 / 主力净额前5板块`
- `p1_auction_ref / P1竞价段引用`

**待补字段（6/15）：**
- `bias_preopen` / 今日偏强偏弱 — 待补(人工)
- `watch_sectors` / 该盯板块 — 待补(人工，可参考sector前5)
- `watch_symbols` / 该盯标的 — 待补(人工，可参考天梯高标)
- `live_room_note` / 直播间方向摘要 — 待补(需导出Raw，A桶9房 NOTES.今日要点)
- `情绪标签` — 待补(半可推导，pauseRatio/连板扩张)
- `one_liner` / 盘前一句话 — 待补(人工)

**下一步最小操作命令：**
```powershell
# 命令1：列出昨日 ladder json 快照，确认连板摘要可用
Get-ChildItem "D:\Stock\trading_assistant\02_runtime\quicktiny_capture\ladder_daily_snapshots" -Filter "ladder_day_min__*.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 3 Name,LastWriteTime

# 命令2：列出最近 sector 快照 + P1 竞价段 md 路径
Get-ChildItem "D:\Stock\trading_assistant\02_runtime\quicktiny_capture\sector_daily_snapshots" -Filter "sector_capital_flow_snapshot__*.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 FullName
Get-ChildItem "D:\Stock\trading_assistant\02_runtime\shortline_funding_gap" -Recurse -Filter "p1_day__*.md" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 FullName
```

---

### ② 盘中确认卡 / intraday · 14%

**已就绪字段（1/7）：**
- `trade_date` / 交易日

**待补字段（6/7）：**
- `confirm_10_00` / 10:00资金确认 — 待补(人工+P1盘中段)
- `confirm_13_30` / 13:30资金确认 — 待补(人工+P1盘中段)
- `confirm_14_30` / 14:30确认 — 待补(人工，可选)
- `still_watch` / 仍值得盯 — 待补(人工+天梯盘中变化)
- `live_turn_note` / 直播间转折解释 — 待补(需导出Raw，B桶15房 NOTES.盘中转折)
- `one_liner` / 盘中一句话 — 待补(人工)

**下一步最小操作命令：**
```powershell
# 命令1：打开最新 P1 日记录，定位 10:00 / 13:30 段关键字
Get-ChildItem "D:\Stock\trading_assistant\02_runtime\shortline_funding_gap" -Recurse -Filter "p1_day__*.md" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { Select-String -Path $_.FullName -Pattern "10:00|13:30|14:30" }

# 命令2：列出 B 桶片段房原始 json，准备盘中转折抽取
Get-ChildItem "D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms" -Recurse -Filter "*.json" | Select-Object -First 10 DirectoryName,Name
```

---

### ③ 盘后复盘卡 / afterclose · 33%

**已就绪字段（3/9）：**
- `trade_date` / 交易日
- `ladder_result_fact` / 当日连板结果
- `sector_eod_ref` / 当日行业快照

**待补字段（6/9）：**
- `judge_ok` / 判断对不对 — 待补(人工回看)
- `most_useful` / 最有用信息来源 — 待补(人工回看)
- `most_useless` / 最没用 — 待补(人工回看)
- `keep_to_longterm` / 沉长期库 — 待补(人工+NOTES.值得沉)
- `p1_incremental_value` / P1增量价值 — 待补(人工回看P1)
- `one_liner` / 盘后一句话 — 待补(人工)

**下一步最小操作命令：**
```powershell
# 命令1：确认当日 ladder + sector 快照已就绪
Get-ChildItem "D:\Stock\trading_assistant\02_runtime\quicktiny_capture\ladder_daily_snapshots" -Filter "ladder_day__20260811.json" -ErrorAction SilentlyContinue | Select-Object Name,Length
Get-ChildItem "D:\Stock\trading_assistant\02_runtime\quicktiny_capture\sector_daily_snapshots" -Filter "sector_capital_flow_snapshot__20260811.json" -ErrorAction SilentlyContinue | Select-Object Name,Length

# 命令2：跨房搜索"值得沉淀"标记，为长期库收口做准备
Get-ChildItem "D:\Stock\trading_assistant\02_runtime\info_live_room_sampling" -Recurse -Filter "*.md" | Select-String -Pattern "值得沉淀|长期|沉" -List | Select-Object Path
```

---

### ④ 连板天梯 / stock_row · 97%

**已就绪字段（16/17 完整 + 1 部分就绪）：**
- ✅ `name` / 股票名称
- ✅ `code` / 代码
- ✅ `level / continue_num` / 连板数
- ✅ `high_days` / N天N板
- ✅ `change_rate` / 涨跌幅%
- ✅ `industry` / 行业
- ✅ `primary_theme` / 主线题材
- ✅ `kpl_theme_tags` / 题材标签
- ✅ `tradeAmount` / 成交额
- ✅ `actual_turnover_rate` / 真实换手率
- ✅ `limit_up_suc_rate` / 封单率
- ✅ `limitAmount` / 封单额
- ✅ `limit_up_type` / 板型
- ✅ `first_limit_up_time_text` / 首封时间
- ✅ `reason_type` / 连板原因
- ✅ `auto_position / tags` / 总龙头/一字龙定位
- ⚠️ `risk` / 风险(炸板率/开板次数) — 部分就绪(缺个股炸板 open_num 明细)

**待补字段（0.5/17）：**
- 个股级炸板率补全（当前仅有日级 pauseRatio，缺 `stocks[].open_num`）

**下一步最小操作命令：**
```powershell
# 命令1：把 batch_150 NOTES 设计稿搬到 workbench 参考目录(作为连板人工裁决锚点)
Copy-Item "D:\Stock\dealer_assistant\.trae\commands\工作台事实预填.md" "D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_workbench_design_map__20260811\__ref_ladder_prefill_notes.md" -Force

# 命令2：校验最新 ladder json 中 open_num 字段是否存在（确认 risk 缺口）
Get-ChildItem "D:\Stock\trading_assistant\02_runtime\quicktiny_capture\ladder_daily_snapshots" -Filter "ladder_day__*.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { Get-Content $_.FullName -Raw | Select-String "open_num" | Select-Object -First 3 }
```

---

### ⑤ 行业板块 / sector_row · 100%

**已就绪字段（7/7）：**
- ✅ `sectorName` / 板块名称
- ✅ `mainNetAmount` / 主力净流入额
- ✅ `bigOrderNetAmount` / 大单净额
- ✅ `strength` / 板块强度
- ✅ `pctChg` / 涨跌幅%
- ✅ `memberCount` / 成分股数
- ✅ `relativeInflow` / 相对流入比

**待补字段：无**

**下一步最小操作命令：**
```powershell
# 命令1：取最新 sector 快照 Top5 主力净流入，直接喂给盘前卡 watch_sectors
Get-ChildItem "D:\Stock\trading_assistant\02_runtime\quicktiny_capture\sector_daily_snapshots" -Filter "sector_capital_flow_snapshot__*.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { Write-Host "=== Top5 板块参考: ==="; (Get-Content $_.FullName -Raw | ConvertFrom-Json).data.rows | Select-Object -First 5 sectorName,mainNetAmount | Format-Table -AutoSize }
```

---

### ⑥ 直播间 / rooms · 43%

**已就绪字段（3/7，均为 rooms_index 层）：**
- ✅ `房名(24房完整名单)` — SENTINEL_INDEX.md
- ✅ `A桶(9房) / Tier1 方向房` — SENTINEL 分桶=A
- ✅ `B桶(15房) / Tier2 片段房` — SENTINEL 分桶=B

**待补字段（4/7，均为 room_NOTES 层）：**
- `今日要点 / 人话摘要` — 待补(需✅吸收，24房各 NOTES.md 今日要点段)
- `提到的标的/金股池` — 待补(需✅吸收)
- `次日方向/风险提示` — 待补(需✅吸收)
- `P1建议 / 策略建议` — 待补(无固定合同，全文搜索"建议"/"关注")

**下一步最小操作命令：**
```powershell
# 命令1：列出 A 桶 9 房（方向房），输出每日盯房清单（A9）
Write-Host "=== A桶9房 · 每日盯房清单 ==="; $priority = @("复盘哥","k神","天机","浮光","先知","周期女王","上海老梁","兄安","七龙珠"); Get-ChildItem "D:\Stock\trading_assistant\02_runtime\info_live_room_sampling\batch_05__20260803_20260805_priority_room_history_rerun\00_raw\priority_rooms" -Directory | Where-Object { $priority -contains $_.Name } | Select-Object Name,@{N="LastJson";E={(Get-ChildItem $_.FullName -Filter "*.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 1).Name}} | Format-Table -AutoSize

# 命令2：跨房抽取 NOTES 中"今日要点/金股/风险提示"关键字（先定位 md）
Get-ChildItem "D:\Stock\trading_assistant\02_runtime\info_live_room_sampling" -Recurse -Include "NOTES*.md","*吸收*.md" -ErrorAction SilentlyContinue | Select-Object -First 10 FullName
```

---

## 三、三档人工动作建议

### ⏱️ 5 分钟档（立刻做，≤5min）
1. 跑「行业板块 命令1」，把 Top5 板块名直接抄进 `盘前卡 > watch_sectors` 判断格
2. 跑「连板天梯 命令1」，把 NOTES 设计稿搬过来，随时对照裁决
3. 跑「直播间 命令1」，把 A9 房清单钉在工作台侧栏

### ⏱️ 10 分钟档（盘前做，≤10min）
1. 跑「盘前方向卡 命令1+2」，确认 ladder / sector / P1 三源路径都在，再人工填 `bias_preopen`（偏强/偏弱）
2. 跑「连板天梯 命令2」，确认 risk 缺口（open_num），若缺则在卡上标注"风险字段仅日级"
3. 人工填 `watch_symbols`（参考天梯最高3只） + `情绪标签`（参考 pauseRatio + 连板池较昨日增减）

### ⏱️ 30 分钟档（盘中/盘后做，≤30min）
1. **盘中段**：跑「盘中确认卡 命令1」，按 10:00 / 13:30 两个时点读 P1 段，填 `confirm_10_00` + `confirm_13_30`，14:30 可选
2. **直播间 Raw 导出**：跑「盘中确认卡 命令2」+「直播间 命令2」，把 B 桶片段房的转折段 / A9 房今日要点抽成纯文本，填 `live_room_note` + `live_turn_note`
3. **盘后段**：跑「盘后复盘卡 命令1+2」，对照当日 ladder/行业快照，填 `judge_ok` + `most_useful/useless` + 三句 `one_liner`

---

*生成时间：2026-08-11 · 设计锚点：`design_field_mapping__20260811.tsv:1-63`*
