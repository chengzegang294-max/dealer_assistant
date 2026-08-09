# sector_daily_snapshots

## 用途

- 只累积 `sector-capital-flow/snapshot` **当日**快照
- 不碰历史日回补

## 脚本

```powershell
python "d:\Stock\dealer_assistant\20_tools_workspace\batch_08_quicktiny_capture_tools\capture_sector_snapshot_daily_v1.py" `
  --input-json "<当日原始 json>" `
  --output-dir "d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\sector_daily_snapshots" `
  --trade-date YYYYMMDD
```

## 已有样例

- `sector_capital_flow_snapshot__20260807.*`（脚手架冒烟样例）
