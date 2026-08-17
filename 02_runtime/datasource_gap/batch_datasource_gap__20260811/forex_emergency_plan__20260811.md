# 外汇应急方案 v1.0 __20260811

> 状态：🔴全断（无任何结构化外汇K线/快照）
> 目标：30天内从0到「主力6品种日线稳定+3品种M5可探」
> 产出目录：`02_runtime/quicktiny_capture/forex_daily_snapshots/` 与 `02_runtime/info_live_room_sampling/rooms/金十财经直播间/`

---

## 方案一：金十直播间锚点（低成本先跑通信号流）

在 `info_live_room_sampling/rooms/` 新建「金十财经直播间」子目录，结构与现有24房一致（00_raw / 10_ingest / 20_absorb）。每日 08:30 亚洲盘前、15:30 欧洲盘前、20:30 美洲盘前共3个时点，进入金十数据(jin10.com)直播间手动导出 HTML→JSON，或对直播页关键卡片（财经日历、重磅数据、名家点评、异动提醒）截图 OCR 成「锚点JSON」，字段包含：时间戳、品种(EURUSD/XAUUSD 等)、事件类型(数据公布/讲话/突发事件)、影响方向(多/空)、原文摘要、置信度。第一周只要求日均3条有效锚点即可，不求全，先形成每日不落空的节律。

## 方案二：东方财富PC截图OCR（先拿可视化保真价）

每交易日 08:00/12:00/20:00 三次，用 Windows 截图快捷键或 Python `mss`/`PIL` 对东方财富 PC 端「外汇中心」(quote.eastmoney.com/center/gridlist.html#forex) 全屏固定坐标截一张 PNG，存到 `00_raw_screenshot/forex_eastmoney/`。再用 Tesseract（中文包+英文包）对截图中 6 个主力品种（EURUSD、GBPUSD、USDJPY、USDCNY、XAUUSD、XAGUSD）的现价、涨跌额、涨跌幅、最高、最低 5 列做表格 OCR，输出到 `forex_snapshot_oce__YYYYMMDD_HHMM.tsv`。OCR 不准的字段先用空值，连续跑7天后取众数补置信度，先保真拿到可回溯的价量原始证据，后续再上 API 替换。

## 方案三：免费API akshare / efinance 批量日线（30天内建成主力底仓）

写独立脚本 `20_tools_workspace/batch_12_forex_daily_seed/seed_forex_akshare_v1.py`，先用 `akshare.currency_hist(symbol="EURUSD", period="daily")` 对主力 12 品种（EURUSD/GBPUSD/USDJPY/AUDUSD/USDCAD/NZDUSD/USDCNY/USDHKD/XAUUSD/XAGUSD/UKOIL/USOIL）批量拉取最近 3 年日线，每条输出标准化 OHLCV 5 列 + 成交额(如有)，落地到 `02_runtime/quicktiny_capture/forex_daily_snapshots/forex_daily__{symbol}__YYYYMMDD.tsv`，另附 meta.json 写清抓取时的 akshare 版本号与调用参数。每周末用 `efinance.stock.get_quote_history()` 做一次交叉核验，两条来源相差超过 0.3% 的交易日标记 flag 人工复核。此方案一旦跑通即沉淀历史回测底仓，后续再迭代分时级别。

---

## 优先级与里程碑

| 周次 | 方案 | 里程碑 |
|------|------|--------|
| W1(8/11-8/17) | 一+二 | 金十房间建完，首周3锚点/日；OCR脚本跑通首版，6品种截图3次/日 |
| W2(8/18-8/24) | 三 | akshare 12品种3年日线全部落地，完成首轮 efinance 交叉对账 |
| W3(8/25-8/31) | 一二三合 | 三套方案产物互相校验，选出 2 套稳定方案作为正式链路，第3套留作备用 |
