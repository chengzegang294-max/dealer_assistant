# batch_02_collection_pipeline__20260901

## 用途

本批是 `A股 Tushare 日线采集 -> 仓外 snapshot-root -> SUCCESS manifest -> 既有离线消费者` 的运行时说明。

它只描述采集与交接，不引入任何技术指标、复权计算、策略或 UI。

## CLI 示例

```powershell
python "D:\Stock\dealer_assistant\20_tools_workspace\batch_17_tushare_daily_collection_tools\tushare_daily_snapshot_collector.py" `
  --snapshot-root "D:\external\tushare_snapshots" `
  --output-dir "D:\external\tushare_collection_runs\run_20260901" `
  --token-env-var "TUSHARE_TOKEN" `
  --run-id "run_20260901" `
  --timezone-name "Asia/Shanghai" `
  --post-close-cutoff-local "18:00" `
  --reference-time-utc "2026-09-01T12:30:00Z"
```

说明：

- 采集器不再接受自定义 `api-url`
- 官方唯一 origin 固定为：`https://api.tushare.pro`
- `run_id` 必须是安全单段标识，不能包含路径成分或盘符
- `--snapshot-root` 与 `--output-dir` 必须位于仓外
- 输出目录实际写入为：`<output-dir>/<run-id>/...`

## 运行结果

- `collector_manifest.json`
- `collection_report.json`
- 仓外不可变 aggregate snapshot files
- 仓外不可变 raw page snapshot files

仅当：

- 四类输入完整
- 快照成功写盘
- `latest-complete` 可判定
- 不在盘后等待窗口内

才会生成 `run_status=SUCCESS` 的 manifest。

## 后续衔接

`collector_manifest.json` 可直接作为既有离线消费者的 `--manifest` 输入，但前提是：

- `run_status = SUCCESS`

否则消费者会拒收。

聚合快照说明：

- manifest 指向的是 `DERIVED_PAGE_AGGREGATE`
- `source_response_origin = DERIVED_PAGE_AGGREGATE_NOT_VENDOR_RAW`
- 它不是供应商原始响应
- 真正的分页原始响应保存在 `raw_pages/` 下
- 聚合快照必须保留完整 `page_response_chain`
- 聚合快照的 `source_response_sha256` 代表派生聚合响应 SHA，不代表 vendor raw page SHA
