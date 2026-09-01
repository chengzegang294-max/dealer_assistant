# batch_16_tushare_daily_replay_tools

更新时间：2026-09-01
状态：可运行的离线只读合同消费者 + 质量闸门
仓库：`d:\Stock\dealer_assistant`

## 这批是干什么的

把 `Tushare A股日线研究主源` 的正式 addendum，落成一个**离线、只读、合同驱动**的最小消费者：

1. 从用户显式提供的外部 manifest + snapshot root 读取外部快照
2. 先校验 `source_response_sha256` 与 `snapshot_file_sha256`
3. 再按 `stock_basic.exchange + list_status='L'` 收口正式范围
4. 输出标准化 raw 日线数据、排除登记、回放报告、summary JSON 和 `data_quality_report.json`

本批明确不做：

- 不联网
- 不读 Token
- 不连 Tushare API
- 不做分钟、日内、即时更新、执行或券商功能
- 不算 `qfq/hfq`
- 不输出 `F016`
- 不实施 `F026/F030/F031/F032/F034`

## 目录

| 路径 | 用途 |
|------|------|
| `tushare_daily_replay_consumer.py` | 主 CLI 与离线消费者实现 |
| `tests/test_tushare_daily_replay_consumer.py` | 合成 fixture 测试 |

## 输入与输出合同

固定输入：

1. `--manifest`
2. `--snapshot-root`
3. `--output-dir`

成功产物：

- `normalized_daily_output.tsv`
- `exclusion_register.tsv`
- `replay_validation_report.md`
- `summary.json`
- `data_quality_report.json`

失败产物：

- `replay_validation_report.md`
- `summary.json`
- `data_quality_report.json`

质量报告计数口径：

- `excluded_row_count`：全部排除行
- `out_of_scope_exclusion_row_count`：范围外排除
- `quality_exclusion_row_count`：质量失败导致的排除
- `quality_failed_row_count`：质量失败行数
- `blocking_failure_count`：阻断性失败计数

其中：

- `BSE_EXCLUDED_BY_FORMAL_SCOPE`
- `EXCHANGE_OUT_OF_FORMAL_SCOPE`

只计入 `out_of_scope_exclusion_row_count`，不计入 `quality_failed_row_count`。

阻断项包括：

- `stock_basic / daily / adj_factor` 主键重复
- `daily / adj_factor` 关键字段缺失
- `daily` 无法联到 active `stock_basic`
- `daily` 只联到 `stock_basic.list_status != 'L'`，并记为 `DAILY_MATCHED_STOCK_BASIC_NOT_ACTIVE_L`
- `SSE/SZSE` 日线日期不是 latest-complete trading day
- 数值字段无法解析或不是有限数值
- raw daily 必填字段缺失

只要命中阻断项，就不能产生 `SUCCESS` 的标准化输出。

行级质量检查：

- `OHLC` 关系
- `vol/amount >= 0`
- `pct_chg = change / pre_close * 100`
- `change = close - pre_close`
- `adj_factor > 0`

固定容差：

- `pct_chg_abs_tolerance = 0.05`
- `change_abs_tolerance = 0.011`

## 怎么跑

```powershell
python "D:\Stock\dealer_assistant\20_tools_workspace\batch_16_tushare_daily_replay_tools\tushare_daily_replay_consumer.py" `
  --manifest "D:\path\to\external_snapshot_manifest.json" `
  --snapshot-root "D:\path\to\external_snapshots" `
  --output-dir "D:\path\to\replay_output"
```

成功时输出：

- `normalized_daily_output.tsv`
- `exclusion_register.tsv`
- `replay_validation_report.md`
- `summary.json`
- `data_quality_report.json`

失败时只写：

- `replay_validation_report.md`
- `summary.json`
- `data_quality_report.json`

且不会生成“通过”标准化输出。

## 测试

```powershell
python -m unittest "D:\Stock\dealer_assistant\20_tools_workspace\batch_16_tushare_daily_replay_tools\tests\test_tushare_daily_replay_consumer.py" -v
```

## 正式依据

- [Tushare A股日线研究主源与字段映射合同](file:///D:/Stock/dealer_assistant/00_entry/全库资料整理收口__20260713/A5_TushareA股日线研究主源与字段映射合同__20260901.md#L1-L222)
- [TA-04 正式冻结定义](file:///D:/Stock/dealer_assistant/00_entry/全库资料整理收口__20260713/A5_A股技术分析术语公式与字段语义裁决合同__20260831.md#L46-L125)
- [新仓交接总记录](file:///D:/Stock/dealer_assistant/00_entry/A5_新仓交接总记录__20260809.md#L737-L753)
- [批次输入输出合同](file:///D:/Stock/dealer_assistant/02_runtime/tushare_a_share_daily_replay/batch_01_contract_consumer__20260901/INPUT_OUTPUT_CONTRACT__20260901.md#L1-L176)

## 一句话

这是一个把外部 Tushare 证据包读进来、先验哈希、再按正式范围回放的最小合同消费者，不替代理论合同，也不碰实时和执行。
