# COLLECTOR_RUNTIME_CONTRACT｜A股 Tushare 日线采集—快照—质量回放闭环

更新时间：2026-09-01

## 1. 输入

采集器固定接收：

- `--snapshot-root`
- `--output-dir`
- `--token-env-var`
- `--run-id`
- `--timezone-name`
- `--post-close-cutoff-local`
- `--reference-time-utc`
- `--page-limit`
- `--max-retries`

`run_id` 必须是安全单段标识：

- 非空
- 不能是 `.` 或 `..`
- 不含 `/`、`\`、盘符、绝对路径或路径遍历成分
- 在读取 Token、发请求、创建目录、写文件前完成校验

固定网络边界：

- 只允许官方 HTTPS origin：`https://api.tushare.pro`
- 不暴露自定义 `api-url`
- 任何 `3xx` 重定向都必须失败

## 2. 采集范围

只允许：

1. `trade_cal(SSE)`
2. `trade_cal(SZSE)`
3. `stock_basic(list_status=L)`
4. `daily`
5. `adj_factor`

## 3. 禁止项

本批不做：

- 实时、分钟、盘中
- 期货、外汇、券商、交易
- BSE 主源
- `qfq/hfq`
- `F016`
- `F026/F030/F031/F032/F034`
- 指标、策略、UI、建议

## 4. Token 纪律

1. Token 只能从 `--token-env-var` 指定的外部环境变量读取
2. 代码、日志、错误、manifest、snapshot、fixture 不得输出 Token 值
3. 本批不执行真实联网烟测

## 5. 快照 envelope

每个原始响应写入：

`<snapshot-root>/<run_id>/raw_pages/<manifest_key>/page_XXXX.json`

最小字段：

- `api_name`
- `capture_time_utc`
- `source_id`
- `request_params_redacted`
- `source_response_text`
- `source_response_sha256`
- `snapshot_file_sha256`
- `row_count`
- `field_list`

供既有 consumer 使用的单数据集输入另写为：

`<snapshot-root>/<run_id>/<manifest_key>.json`

它必须满足：

- `snapshot_role = DERIVED_PAGE_AGGREGATE`
- `source_response_origin = DERIVED_PAGE_AGGREGATE_NOT_VENDOR_RAW`
- 不得被称为供应商原始响应
- 必须保留全部 `page_response_chain`
- `source_response_sha256` 与 raw page 响应 SHA 明确分离

说明：

- 顶层 manifest 中的 `snapshot_file_sha256` 为正式回放使用的 aggregate 文件 SHA
- raw page 文件的实际 file SHA 必须进入 `page_response_chain`
- snapshot 内部同名字段只保留占位说明，避免自哈希悖论
- aggregate snapshot 的 `source_response_sha256` 是派生聚合响应 SHA，不是 vendor raw page SHA

## 6. 不可变性

1. 采用 `<run_id>` 隔离不同采集批次
2. 快照使用排他创建
3. 同一 `run_id` 的重复运行不得覆盖不同内容
4. 重复运行若内容一致，可复用原快照
5. `collector_manifest.json` 与 `collection_report.json` 也按 `<output-dir>/<run_id>/...` 不可覆盖输出
6. `snapshot-root` 与 `output-dir` 必须位于 `dealer_assistant` 仓外
7. `<snapshot-root>/<run_id>` 与 `<output-dir>/<run_id>` resolve 后仍必须位于各自已验证根目录内

## 7. 盘后可用窗口

判定 latest-complete 必须同时依赖：

1. `trade_cal`
2. `timezone-name`
3. `post-close-cutoff-local`
4. `reference-time-utc`

若当前仍在盘后入库窗口内：

- 顶层 `run_status = WAITING_FOR_POST_CLOSE_AVAILABILITY`
- 不得把当日视为空行情
- 不得生成 `SUCCESS manifest`

## 8. 顶层 manifest

顶层 `collector_manifest.json` 至少包含：

- `manifest_name`
- `source_id`
- `run_id`
- `run_status`
- `generated_at_utc`
- `config`
- `latest_complete_trade_date`
- `entries`

## 9. run_status

- `SUCCESS`
- `INCOMPLETE`
- `WAITING_FOR_POST_CLOSE_AVAILABILITY`

只有 `SUCCESS` manifest 允许送入既有离线消费者。

## 10. collection_report.json

机器可读报告至少包含：

- `run_id`
- `source_id`
- `run_status`
- `generated_at_utc`
- `token_env_var`
- `timezone_name`
- `post_close_cutoff_local`
- `reference_time_utc`
- `page_limit`
- `max_retries`
- `api_results`
- `reason_counts`
- `latest_complete_trade_date_by_exchange`

每个 `api_result` 至少包含：

- `status`
- `api_name`
- `scope`
- `page_count`
- `row_count`
- `retry_count`
- `reason_counts`
- `snapshot_path`
- `snapshot_role`
- `page_response_chain`

## 11. consumer 拒收条件

既有离线消费者在以下情况下必须拒收：

1. `run_status != SUCCESS`
2. `run_status` 缺失
3. manifest 缺少正式字段
4. manifest 中任一快照哈希不一致
