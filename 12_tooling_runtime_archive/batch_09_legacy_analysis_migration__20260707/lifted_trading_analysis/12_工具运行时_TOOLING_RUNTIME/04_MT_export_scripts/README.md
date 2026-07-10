# MT4/MT5 Bars CSV 一键导出说明

## 你遇到的卡点

- 你一直在跑 ingest 脚本，但投递区 `data\mt_exports_drop\` 里没有任何 CSV。
- 这说明“导出这一步”并没有真正产出文件（或产出到未知位置）。

## 这个目录提供什么

- `ExportBarsToCsv_v1.mq4`
- `ExportBarsToCsv_v1.mq5`
- `ExportBarsToCsv_UTC_v1.mq4`
- `ExportBarsToCsv_UTC_v1.mq5`

它们会把指定品种与周期的 bars 写成 CSV，输出到：

- `%APPDATA%\MetaQuotes\Terminal\Common\Files\`

也就是你机器上这个目录：

- `C:\Users\91883\AppData\Roaming\MetaQuotes\Terminal\Common\Files\`

## 用法（最小动作）

1. 在 MT4/MT5 打开 `File -> Open Data Folder`
2. 把脚本复制进去：
   - MT4：复制到 `MQL4\Scripts\`
   - MT5：复制到 `MQL5\Scripts\`
3. 在终端里运行脚本（Scripts 里双击）

推荐优先跑 UTC 版本（减少时区歧义）：

- `ExportBarsToCsv_UTC_v1.mq4` / `ExportBarsToCsv_UTC_v1.mq5`
4. 运行前参数改成：
   - `InpSymbol = EURUSD`
   - `InpTimeframe = PERIOD_M1`（给 N02）
   - `InpFileName = eurusd_m1_export.csv`
   - `InpFileName = eurusd_m1_export_utc.csv`
5. 再跑一次（给 N01）：
   - `InpTimeframe = PERIOD_H1`
   - `InpFileName = eurusd_h1_export.csv`
   - `InpFileName = eurusd_h1_export_utc.csv`


## 把 Common\\Files 的导出文件复制到投递区（推荐）

```powershell
Copy-Item -LiteralPath "C:\Users\91883\AppData\Roaming\MetaQuotes\Terminal\Common\Files\eurusd_m1_export_utc.csv" -Destination "12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop" -Force
Copy-Item -LiteralPath "C:\Users\91883\AppData\Roaming\MetaQuotes\Terminal\Common\Files\eurusd_h1_export_utc.csv" -Destination "12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop" -Force
Get-ChildItem -LiteralPath "12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop" -File | Select-Object Name,Length,LastWriteTime
```

之后就可以继续跑我们的 ingest + proof-of-mapping 了。
