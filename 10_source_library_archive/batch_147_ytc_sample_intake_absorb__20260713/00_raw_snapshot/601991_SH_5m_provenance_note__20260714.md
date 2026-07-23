# 601991_SH_5m Provenance Note

更新时间：2026-07-14

## 文件类型

- `INDEX_NOTE`

## source_path

- `E:\股票历史数据\分钟K线-股票241\2000-2025\按年\5分钟\2024.zip`
- `2024/sh601991.csv`
- 上游下载方式：
  - `百度网盘`
- 淘宝店铺：
  - `INJOY杂货铺`

## repo_path

- `10_source_library_archive/batch_147_ytc_sample_intake_absorb__20260713/00_raw_snapshot/601991_SH_5m.csv`

## producer

- `external_vendor_package_user_downloaded`

## scope

- symbol：
  - `601991.SH`
- timeframe：
  - `5m`
- 窗口：
  - `2024-03-01 09:30:00`
  - `2024-04-10 15:00:00`

## evidence_mode

- `external_vendor_package_snapshot`

## status

- `active`

## 当前作用

- 为 `YTC` 提供真实 `5m` 小样本入口。
- 作为 `601991_SH_60m.csv` 的上游原始窗口样本。

## 处理说明

- 当前文件不是通过 `Tushare` 终端直连拉取生成。
- 当前文件由项目外数据仓中的 `2024/sh601991.csv` 截取目标时间窗后写入本仓。
- 原外部仓由用户手工下载到本地。
- 当前已知来源补充为：
  - 资料主要来自 `百度网盘`
  - 淘宝真实店铺应为 `INJOY杂货铺`
- 当前仍未补：
  - 具体商品标题
  - 百度网盘分享链接或提取页截图

## 字段说明

- 最小接收字段已满足：
  - `trade_date`
  - `open`
  - `high`
  - `low`
  - `close`
  - `volume`
- 额外保留：
  - `amount`
  - `pct_chg`
  - `turnover_rate`
  - `float_share`
  - `total_share`
  - `source_package`
  - `source_entry`

## 备注

- `Tushare stk_mins` 的限频阻塞保留在：
  - `YTC_intraday_provider_rate_limit_blocker__20260713.md`
- 该阻塞说明当前只作为历史失败记录，不再是本轮吸收的唯一来源路径。
