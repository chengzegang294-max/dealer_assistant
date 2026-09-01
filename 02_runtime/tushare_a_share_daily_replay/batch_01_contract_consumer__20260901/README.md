# batch_01_contract_consumer__20260901

更新时间：2026-09-01
状态：离线回放骨架已落盘
仓库：`d:\Stock\dealer_assistant`

## 这批是干什么的

给 `Tushare A股日线研究主源` 的新仓正式合同，配一套**本地只读回放骨架**：

1. 外部 snapshot manifest 示例
2. 输出目录骨架说明
3. 与工具脚本的最小使用约定

这批只负责“怎么把外部证据包读进来并回放”，不内置任何真实旧仓快照。

## 目录

| 路径 | 用途 |
|------|------|
| `examples/external_snapshot_manifest__example.json` | 外部 manifest 示例 |
| `INPUT_OUTPUT_CONTRACT__20260901.md` | 输入输出与质量闸门合同 |
| `artifact_index.json` | 本批骨架清单 |

## 怎么用

1. 准备外部快照目录，例如用户自己提供的 `stock_basic / trade_cal / daily / adj_factor` 快照目录
2. 参照 `examples/external_snapshot_manifest__example.json` 生成真实 manifest
3. 用工具脚本执行回放：

```powershell
python "D:\Stock\dealer_assistant\20_tools_workspace\batch_16_tushare_daily_replay_tools\tushare_daily_replay_consumer.py" `
  --manifest "D:\path\to\external_snapshot_manifest.json" `
  --snapshot-root "D:\path\to\external_snapshots" `
  --output-dir "D:\path\to\replay_output"
```

## 输出约定

成功输出：

- `normalized_daily_output.tsv`
- `exclusion_register.tsv`
- `replay_validation_report.md`
- `summary.json`
- `data_quality_report.json`

失败输出：

- `replay_validation_report.md`
- `summary.json`
- `data_quality_report.json`

## 质量闸门

阻断性失败：

- 主键重复
- 关键字段缺失
- 日线无法联到 active `stock_basic`
- `SSE/SZSE` 日期不是 latest-complete trading day
- 数值字段无法解析或不是有限数值

行级排除：

- `OHLC` 关系不合法
- `vol/amount < 0`
- `pct_chg` 复算超出容差
- `change` 复算超出容差
- `adj_factor <= 0`

详见：
[INPUT_OUTPUT_CONTRACT__20260901.md](file:///D:/Stock/dealer_assistant/02_runtime/tushare_a_share_daily_replay/batch_01_contract_consumer__20260901/INPUT_OUTPUT_CONTRACT__20260901.md#L1-L176)

## 一句话

运行时批次里只放回放骨架和示例，不落真实外部证据包。
