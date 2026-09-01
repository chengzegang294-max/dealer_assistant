# INPUT_OUTPUT_CONTRACT｜A股日线离线回放质量闸门与批次输入输出合同

更新时间：2026-09-01

## 1. 输入

运行入口固定为：

```powershell
python "D:\Stock\dealer_assistant\20_tools_workspace\batch_16_tushare_daily_replay_tools\tushare_daily_replay_consumer.py" `
  --manifest "D:\path\to\external_snapshot_manifest.json" `
  --snapshot-root "D:\path\to\external_snapshots" `
  --output-dir "D:\path\to\replay_output"
```

输入物只允许来自用户显式指定的外部目录：

1. `--manifest`
   - 外部 manifest JSON
   - 必须显式提供
2. `--snapshot-root`
   - 外部快照根目录
   - manifest 内 `snapshot_path` 必须相对该根目录
3. `--output-dir`
   - 用户显式指定的外部输出目录或系统临时目录

## 2. manifest 最小字段

每条 manifest entry 至少包含：

- `manifest_key`
- `source_id`
- `snapshot_path`
- `api_name`
- `capture_time_utc`
- `source_response_sha256`
- `snapshot_file_sha256`
- `row_count`
- `field_list`
- `scope`
- `status`

顶层 manifest 还必须显式包含：

- `run_status = SUCCESS`

必需 `manifest_key`：

- `stock_basic_active`
- `trade_cal_sse`
- `trade_cal_szse`
- `daily_all_market`
- `adj_factor_all_market`

## 3. 成功产物

当且仅当阻断性校验全部通过时，才写出：

1. `normalized_daily_output.tsv`
2. `exclusion_register.tsv`
3. `replay_validation_report.md`
4. `summary.json`
5. `data_quality_report.json`

## 4. 失败产物

若任一阻断项失败：

1. `normalized_daily_output.tsv` 不得写出
2. `exclusion_register.tsv` 不得写出成功版
3. 只允许写：
   - `replay_validation_report.md`
   - `summary.json`
   - `data_quality_report.json`

## 4.1 质量报告计数口径

`data_quality_report.json` 固定区分：

- `excluded_row_count`
- `out_of_scope_exclusion_row_count`
- `quality_exclusion_row_count`
- `quality_failed_row_count`
- `blocking_failure_count`

口径冻结：

1. `BSE_EXCLUDED_BY_FORMAL_SCOPE`
2. `EXCHANGE_OUT_OF_FORMAL_SCOPE`

只计入 `out_of_scope_exclusion_row_count`。

以下才计入 `quality_failed_row_count` 与 `quality_exclusion_row_count`：

1. `OHLC` 关系失败
2. `vol / amount` 负值
3. `pct_chg` 超容差
4. `change` 超容差
5. `adj_factor` 缺失或非正

## 5. 每条输出的 provenance

成功进入标准化输出或排除登记的每行，至少保留：

- `source_id`
- `ts_code`
- `trade_date`
- `capture_time_utc`
- `source_response_sha256`
- `snapshot_file_sha256`
- `snapshot_role`
- `source_response_origin`
- `scope`
- `freshness_status`
- `replay_status`
- `exclusion_reason`
- `exchange`
- `list_status`
- `market`

raw 标准化输出另外保留：

- `open`
- `high`
- `low`
- `close`
- `pre_close`
- `change`
- `pct_chg`
- `vol`
- `amount`
- `adj_factor`

其中 provenance 口径冻结如下：

- `source_response_sha256`
  - 在派生聚合模式下，表示 `DERIVED_PAGE_AGGREGATE` 的聚合响应 SHA
  - 不是 vendor raw page response SHA
- vendor 原始分页响应必须沿 aggregate snapshot 内的 `page_response_chain / derived_from_page_responses` 回查
- 不得把聚合 SHA 表述为 vendor raw SHA

## 6. 阻断项

以下任一项失败，必须令本次回放失败：

1. `stock_basic ts_code` 重复
2. `daily (ts_code, trade_date)` 重复
3. `adj_factor (ts_code, trade_date)` 重复
4. `daily` 或 `adj_factor` 关键字段缺失
5. `daily` 与 active `stock_basic` 无法联结
6. `daily` 只联到 `stock_basic.list_status != 'L'`，记为 `DAILY_MATCHED_STOCK_BASIC_NOT_ACTIVE_L`
7. `SSE/SZSE` 日线日期与 `latest-complete trading day` 不一致
8. 数值字段无法解析为有限数值
9. raw daily 必填字段缺失

## 7. 行级质量检查

对进入正式 `SSE/SZSE active scope` 的每一行，执行：

1. `high >= max(open, close, low)`
2. `low <= min(open, close, high)`
3. `vol >= 0`
4. `amount >= 0`
5. `pct_chg` 复算：
   - `change / pre_close * 100`
   - 容差：`0.05`
6. `change` 复算：
   - `close - pre_close`
   - 容差：`0.011`
7. `adj_factor > 0`

这些检查失败时：

- 行进入 `exclusion_register.tsv`
- 不进入 `normalized_daily_output.tsv`
- 失败原因写入 `exclusion_reason`
- 机器可读统计写入 `data_quality_report.json`

## 8. data_quality_report.json

必须包含：

- `run_status`
- `quality_gate_version`
- `checks`
- `sample_row_count`
- `passed_row_count`
- `excluded_row_count`
- `out_of_scope_exclusion_row_count`
- `quality_exclusion_row_count`
- `quality_failed_row_count`
- `blocking_failure_count`
- `exclusion_reason_counts`
- `blocking_reason_counts`
- `tolerances`
- `formula_version`
- `error`

其中每个 `check` 至少有：

- `check_name`
- `check_type`
- `status`
- `sample_row_count`
- `failed_row_count`
- `reason_counts`
- `tolerance`
- `formula_version`

## 9. 明确不做

本批次不做：

- `qfq/hfq` 计算
- `F016 turnover_rate`
- `F026/F030/F031/F032/F034` 实施
- 任何指标、策略、UI、交易建议
- 任何日内、分钟、即时更新、券商或交易功能
