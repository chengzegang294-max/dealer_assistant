# T01 量价阈值触发密度结果页 stub v1

## 对应验证项

- `T01`
- `V01`

## 当前预留结构

- 验证范围：
  - 时间窗：`2025-05-08 -> 2026-05-08`
  - 输入目录：`02_runtime/butler_r0_ohlcv_object_cards/data/raw/daily_ohlcv/batch09_promoted/ashare_clean/`
  - 覆盖文件数：`46`
- 输入口径：
  - `20日均量 1.8 倍 + 当日涨跌幅绝对值 > 4.5%`
- 核心结果：
  - 触发总量：`520`
  - 触发日：`204`
  - 日均触发数：`2.549`
  - 峰值日触发数：`19`
  - 触发标的数：`44`
- 抽样观察：
  - 当前头部高频触发标的包括：
    - `300209.SZ`
    - `603278.SH`
    - `603399.SH`
  - 仍需后续结合持仓相关性与行业分布做二次复核
- 结论判断：
  - 当前先记为 `微调候选`
- 下一步动作：
  - 补行业分布与持仓相关占比
  - 复核峰值日 `19` 是否过吵
  - 决定是否需要调阈值或加过滤

## 当前产物

- `artifacts/t01_volume_price_scan/t01_volume_price_scan_summary_latest.json`
- `artifacts/t01_volume_price_scan/t01_trigger_detail_latest.tsv`
- `artifacts/t01_volume_price_scan/t01_daily_trigger_counts_latest.tsv`
- `artifacts/t01_volume_price_scan/t01_symbol_trigger_counts_latest.tsv`

## 回链

- 输出模板：
  - `00_entry/A股_P0_离线验证输出模板__20260712.md`
- 结论门槛：
  - `00_entry/A股_P0_离线验证结论门槛__20260712.md`
