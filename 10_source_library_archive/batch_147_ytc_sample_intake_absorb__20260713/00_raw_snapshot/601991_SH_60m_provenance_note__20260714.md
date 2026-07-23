# 601991_SH_60m Provenance Note

更新时间：2026-07-14

## 文件类型

- `INDEX_NOTE`

## source_path

- 上游文件：
  - `10_source_library_archive/batch_147_ytc_sample_intake_absorb__20260713/00_raw_snapshot/601991_SH_5m.csv`
- 上游外部包来源：
  - `E:\股票历史数据\分钟K线-股票241\2000-2025\按年\5分钟\2024.zip`
- 上游包内条目：
  - `2024/sh601991.csv`
- 上游下载方式：
  - `百度网盘`
- 淘宝店铺：
  - `INJOY杂货铺`

## repo_path

- `10_source_library_archive/batch_147_ytc_sample_intake_absorb__20260713/00_raw_snapshot/601991_SH_60m.csv`

## producer

- `local_aggregation_from_external_5m_snapshot`

## scope

- symbol：
  - `601991.SH`
- timeframe：
  - `60m`
- 窗口：
  - `2024-03-01 10:30:00`
  - `2024-04-10 15:00:00`

## evidence_mode

- `derived_from_external_vendor_5m_snapshot`

## status

- `active`

## 当前作用

- 为 `YTC` 提供真实 `60m` 小样本入口。
- 连接现有 `daily+weekly` 最小运行锚点与分钟级样本验证链。

## 聚合说明

- 由 `601991_SH_5m.csv` 本地聚合得到。
- session bucket 规则：
  - `10:30:00`
  - `11:30:00`
  - `14:00:00`
  - `15:00:00`
- 聚合模式：
  - `aggregate_5m_to_60m_session_buckets_v1`

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
  - `source_trade_date`
  - `derived_from`
  - `derivation_mode`
  - `source_vendor_code`

## 备注

- 当前 `60m` 文件不伪装成外部包直接提供的原生 `60m` 文件。
- provenance 明确保留：
  - 上游 `5m` 文件
  - 外部 zip 包路径
  - 聚合模式
- 当前已知来源补充为：
  - 资料主要来自 `百度网盘`
  - 淘宝真实店铺应为 `INJOY杂货铺`
