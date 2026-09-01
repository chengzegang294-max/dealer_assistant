# batch_17_tushare_daily_collection_tools

状态：mock 已覆盖的只读日线采集器骨架

## 目标

提供一个仅面向 `Tushare A股盘后/历史日线研究` 的采集器：

1. 从运行时环境变量读取 Token
2. 采集：
   - `trade_cal(SSE)`
   - `trade_cal(SZSE)`
   - `stock_basic(list_status=L)`
   - `daily`
   - `adj_factor`
3. 把原始响应写入仓外不可变 `snapshot-root`
4. 生成顶层 `collector_manifest.json`
5. 只有 `run_status=SUCCESS` 的 manifest 才允许送入既有离线消费者

## 明确边界

本批不做：

- 实时、分钟、盘中、期货、BSE 主源
- 券商、交易、策略、指标、UI
- `qfq/hfq`
- `F016`
- `F026/F030/F031/F032/F034`
- Token 落盘、展示、异常透传

## Token 与日志

- Token 只能从 `--token-env-var` 指定的环境变量读取
- manifest、report、snapshot、测试断言均不得出现 Token 值
- 实际联网烟测不在本批执行范围内
- 采集目标只能是官方唯一 HTTPS origin：`https://api.tushare.pro`
- 禁止 HTTP 重定向；任何 `3xx` 都必须在携带 Token 前失败

## 原始响应与聚合输入

- 每个分页响应单独写为 `RAW_PAGE_RESPONSE`
- 路径固定为：
  - `<snapshot-root>/<run_id>/raw_pages/<manifest_key>/page_XXXX.json`
- 供离线消费者使用的单数据集输入写为：
  - `<snapshot-root>/<run_id>/<manifest_key>.json`
  - `snapshot_role = DERIVED_PAGE_AGGREGATE`
  - `source_response_origin = DERIVED_PAGE_AGGREGATE_NOT_VENDOR_RAW`
- 聚合快照不是供应商原始响应，必须保留完整 `page_response_chain`
- `reference_time_utc` 只用于 latest-complete 判断
- `capture_time_utc` 必须记录实际分页抓取时间与实际聚合时间
- 聚合快照的 `source_response_sha256` 是派生聚合响应 SHA，不是 vendor raw page SHA

## 不可变快照与输出

- 快照写入：`<snapshot-root>/<run_id>/<manifest_key>.json`
- manifest/report 写入：`<output-dir>/<run_id>/...`
- 使用排他创建，禁止静默覆盖
- 同一 `run_id` 的重复执行只允许复用同内容快照
- 同一 `run_id` 的 manifest/report 也只允许复用同内容
- 顶层 manifest 使用快照文件的实际磁盘 SHA
- `snapshot-root` 与 `output-dir` 都必须位于 `D:\Stock\dealer_assistant` 仓外
- `run_id` 必须是安全单段标识，resolve 后的 run 目录仍必须留在各自已验证根目录内

说明：

- 由于快照文件不能对自身做稳定自哈希嵌入，snapshot 内部 `snapshot_file_sha256` 字段只保留占位说明
- 正式回放与校验以顶层 manifest 的 `snapshot_file_sha256` 为准
- raw page 文件的实际 file SHA 记录在聚合快照与 `collection_report.json` 的 `page_response_chain`

## run_status

- `SUCCESS`
- `INCOMPLETE`
- `WAITING_FOR_POST_CLOSE_AVAILABILITY`

离线消费者会拒绝一切 `run_status != SUCCESS` 的 manifest。

## 测试覆盖

当前 mock 测试覆盖：

- 缺 Token
- 权限错误
- 非官方 URL 拒绝
- 重定向拒绝
- 限流与有限重试
- 分页汇总
- 空响应
- 盘后入库等待
- 重复运行不可覆盖
- 同一 run_id 不同内容失败
- 仓内 snapshot-root/output-dir 拒绝
- 半批失败 `INCOMPLETE`
- SHA/manifest 完整性
- `SUCCESS manifest -> consumer` 端到端
- `INCOMPLETE manifest` 被消费者拒绝
- 缺失 `run_status` 被 consumer 拒绝
- Token 泄漏扫描
