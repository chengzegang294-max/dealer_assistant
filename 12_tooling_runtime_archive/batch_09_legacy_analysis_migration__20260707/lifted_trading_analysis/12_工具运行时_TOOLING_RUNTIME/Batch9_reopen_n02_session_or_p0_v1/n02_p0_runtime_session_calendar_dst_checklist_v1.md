# n02_p0_runtime_session_calendar_dst_checklist v1

ARCHIVE_ONLY: 本文件属于旧库运行时快照；若复制执行命令，路径必须以仓库根目录为基准改写为 `.\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\...`，禁止依赖 `d:\Stock\trading_analysis`

## 目的

- 给 `REOPEN_B9_N02_SESSION_OR_P0` 第一份真实 runtime 数据接入前提供固定验收清单。
- 防止把 session 名称、timezone、交易日本地日期、DST 偏移混成同一个概念。

## 当前冻结 binding

- `london -> Europe/London`
- `new_york -> America/New_York`

## 接入前必须逐项确认

### 1. session 命中检查

- 本次写入的 `session_id` 必须命中 `session_binding_registry`。
- 若出现未登记 session：
  - 不直接落到 `v1`
  - 先补 registry 和来源说明

### 2. timezone 一致性检查

- `session_id = london` 时：
  - `session_timezone` 必须为 `Europe/London`
- `session_id = new_york` 时：
  - `session_timezone` 必须为 `America/New_York`
- 不允许手工写入与 registry 不一致的 timezone

### 3. 本地日期解释检查

- session 划分必须按 registry 中 timezone 的本地日期解释。
- 不允许直接用 UTC 日期代替 session 本地交易日。
- 跨日边界时，必须先确认 bar 的本地日期再归属 session。

### 4. DST 检查

- DST 必须由时区规则自动推导。
- 不允许手工写死：
  - `Europe/London = UTC+0`
  - `America/New_York = UTC-5`
- 春秋令时切换周，必须抽 1-2 个时间点做人工复核。

### 5. opening range 窗口检查

- `opening_range_window_minutes` 当前保持 `30`。
- 计算 OR 时，窗口起点必须从 session 本地开盘时刻推导。
- 不允许用固定 UTC 时刻替代本地开盘时刻。

### 6. 最小抽查样本

- 至少抽查：
  - `london` 1 条正常日样本
  - `new_york` 1 条正常日样本
  - DST 切换附近样本至少 1 组
- 每条抽查至少记录：
  - `bar_time`
  - `session_id`
  - `session_timezone`
  - 本地日期解释
  - OR 是否已定义

## 当前已补首批 DST 抽查证据

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v1.py --debug-dst-sample --dst-start 2026-03-25 --dst-end 2026-04-05
```

- `london`：`2026-03-29` 起出现 `+0100`，且 `or_end_utc` 从 `08:30Z` 切换为 `07:30Z`
- `new_york`：该窗口内保持 `-0400`，`or_end_utc = 14:00Z`（符合时区规则推导）

## 当前已扩大 DST 抽查窗口（新增 2 段）

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --debug-dst-sample --dst-start 2026-03-05 --dst-end 2026-03-15
```

- `new_york`：`2026-03-08` 起从 `-0500` 切换到 `-0400`，`or_end_utc` 从 `15:00Z` 切换为 `14:00Z`
- `london`：该窗口内保持 `+0000`，`or_end_utc = 08:30Z`

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --debug-dst-sample --dst-start 2026-10-20 --dst-end 2026-11-05
```

- `london`：`2026-10-25` 起从 `+0100` 切换到 `+0000`，`or_end_utc` 从 `07:30Z` 切换为 `08:30Z`
- `new_york`：`2026-11-01` 起从 `-0400` 切换到 `-0500`，`or_end_utc` 从 `14:00Z` 切换为 `15:00Z`

## 当前已补“DST 切换周 + OR anchor 一致性”证据

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --debug-dst-sample --dst-start 2026-03-27 --dst-end 2026-04-02
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --debug-dst-sample --dst-start 2026-10-23 --dst-end 2026-10-28
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --debug-dst-sample --dst-start 2026-03-06 --dst-end 2026-03-10
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --debug-dst-sample --dst-start 2026-10-30 --dst-end 2026-11-03
```

- `london`（2026-03-29 起进入 `+0100`）：
  - `or_start_utc` 从 `08:00Z` 跳变为 `07:00Z`
  - `or_end_utc` 从 `08:30Z` 跳变为 `07:30Z`
- `london`（2026-10-25 起回到 `+0000`）：
  - `or_start_utc` 从 `07:00Z` 跳变为 `08:00Z`
  - `or_end_utc` 从 `07:30Z` 跳变为 `08:30Z`
- `new_york`（2026-03-08 起进入 `-0400`）：
  - `or_start_utc` 从 `14:30Z` 跳变为 `13:30Z`
  - `or_end_utc` 从 `15:00Z` 跳变为 `14:00Z`
- `new_york`（2026-11-01 起回到 `-0500`）：
  - `or_start_utc` 从 `13:30Z` 跳变为 `14:30Z`
  - `or_end_utc` 从 `14:00Z` 跳变为 `15:00Z`

## 当前已补“DST 切换周 + 真实 bars 的 OR anchor 对齐”证据（春季 + 秋季）

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol EURUSD --timeframe M1 --start 2026-03-27T00:00:00 --end 2026-03-31T00:00:00 --out .\data\mt_exports_drop\dst_windows\london_spring_20260327_20260331\eurusd_m1.csv
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_mt5_export_ingest_v1.py --input .\data\mt_exports_drop\dst_windows\london_spring_20260327_20260331\eurusd_m1.csv --symbol EURUSD --timeframe M1 --source-timezone UTC --dest .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_dst_london_spring_20260327_20260331_bars.csv
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --input .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_dst_london_spring_20260327_20260331_bars.csv --debug-bars-binning --utc-start 2026-03-27T06:50:00Z --utc-end 2026-03-30T09:10:00Z --bars-binning-limit-lines 5
```

- `london`：真实 bars 覆盖 DST 切换前后两个交易日，且 OR anchor（UTC）按时区规则发生跳变：
  - `bars_or_anchor_by_local_date={"2026-03-27":["2026-03-27T08:00:00Z","2026-03-27T08:30:00Z"],"2026-03-30":["2026-03-30T07:00:00Z","2026-03-30T07:30:00Z"]}`

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol EURUSD --timeframe M1 --start 2026-03-06T00:00:00 --end 2026-03-10T00:00:00 --out .\data\mt_exports_drop\dst_windows\ny_spring_20260306_20260310\eurusd_m1.csv
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_mt5_export_ingest_v1.py --input .\data\mt_exports_drop\dst_windows\ny_spring_20260306_20260310\eurusd_m1.csv --symbol EURUSD --timeframe M1 --source-timezone UTC --dest .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_dst_newyork_spring_20260306_20260310_bars.csv
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --input .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_dst_newyork_spring_20260306_20260310_bars.csv --debug-bars-binning --utc-start 2026-03-06T19:13:00Z --utc-end 2026-03-10T00:00:00Z --bars-binning-limit-lines 5
```

- `new_york`：真实 bars 覆盖 DST 切换前后本地交易日，且 OR anchor（UTC）按时区规则发生跳变：
  - `bars_or_anchor_by_local_date={"2026-03-06":["2026-03-06T14:30:00Z","2026-03-06T15:00:00Z"],"2026-03-08":["2026-03-08T13:30:00Z","2026-03-08T14:00:00Z"],"2026-03-09":["2026-03-09T13:30:00Z","2026-03-09T14:00:00Z"]}`

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol EURUSD --timeframe M1 --start 2025-10-23T00:00:00 --end 2025-10-28T00:00:00 --out .\data\mt_exports_drop\dst_windows\london_fall_20251023_20251028\eurusd_m1.csv
```

- `M1`：该窗口内 M1 历史不可用（返回了区间外的单根最新 bar，脚本已改为严格校验区间并报错）。

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol EURUSD --timeframe M5 --start 2025-10-23T00:00:00 --end 2025-10-28T00:00:00 --out .\data\mt_exports_drop\dst_windows\london_fall_20251023_20251028\eurusd_m5.csv
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_mt5_export_ingest_v1.py --input .\data\mt_exports_drop\dst_windows\london_fall_20251023_20251028\eurusd_m5.csv --symbol EURUSD --timeframe M5 --source-timezone UTC --dest .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_dst_london_fall_20251023_20251028_bars.csv
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --input .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_dst_london_fall_20251023_20251028_bars.csv --debug-bars-binning --utc-start 2025-10-24T06:50:00Z --utc-end 2025-10-27T09:10:00Z --bars-binning-limit-lines 5
```

- `london`：秋季回切前后两个交易日（周末无交易 bar），OR anchor（UTC）按时区规则发生跳变：
  - `bars_or_anchor_by_local_date={"2025-10-24":["2025-10-24T07:00:00Z","2025-10-24T07:30:00Z"],"2025-10-27":["2025-10-27T08:00:00Z","2025-10-27T08:30:00Z"]}`

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --input .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_dst_london_fall_20251023_20251028_bars.csv --debug-bars-binning --utc-start 2025-10-24T06:55:00Z --utc-end 2025-10-24T07:35:00Z --bars-binning-limit-lines 5
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --input .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_dst_london_fall_20251023_20251028_bars.csv --debug-bars-binning --utc-start 2025-10-27T07:55:00Z --utc-end 2025-10-27T08:35:00Z --bars-binning-limit-lines 5
```

- `london`：OR window 命中数验证（M5 + 30min => 6 bars）：
  - `bars_or_hits_by_local_date={"2025-10-24": 6}`
  - `bars_or_hits_by_local_date={"2025-10-27": 6}`

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\mt5_export_bars.py --symbol EURUSD --timeframe M5 --start 2025-10-31T00:00:00 --end 2025-11-04T00:00:00 --out .\data\mt_exports_drop\dst_windows\ny_fall_20251031_20251104\eurusd_m5.csv
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_mt5_export_ingest_v1.py --input .\data\mt_exports_drop\dst_windows\ny_fall_20251031_20251104\eurusd_m5.csv --symbol EURUSD --timeframe M5 --source-timezone UTC --dest .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_dst_newyork_fall_20251031_20251104_bars.csv
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --input .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_dst_newyork_fall_20251031_20251104_bars.csv --debug-bars-binning --utc-start 2025-10-31T13:20:00Z --utc-end 2025-11-03T16:10:00Z --bars-binning-limit-lines 5
```

- `new_york`：秋季回切前后两个交易日（周末无交易 bar），OR anchor（UTC）按时区规则发生跳变：
  - `bars_or_anchor_by_local_date={"2025-10-31":["2025-10-31T13:30:00Z","2025-10-31T14:00:00Z"],"2025-11-02":["2025-11-02T14:30:00Z","2025-11-02T15:00:00Z"],"2025-11-03":["2025-11-03T14:30:00Z","2025-11-03T15:00:00Z"]}`

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --input .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_dst_newyork_fall_20251031_20251104_bars.csv --debug-bars-binning --utc-start 2025-10-31T13:25:00Z --utc-end 2025-10-31T14:05:00Z --bars-binning-limit-lines 5
```

- `new_york`：OR window 命中数验证（M5 + 30min => 6 bars）：
  - `bars_or_hits_by_local_date={"2025-10-31": 6}`

## 当前已补 overlap（本地时间重复/缺失）抽查证据

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --debug-overlap-sample --utc-start 2026-11-01T04:00:00Z --utc-end 2026-11-01T09:00:00Z --utc-step-minutes 30
```

- `new_york`：出现本地时钟重复：
  - `2026-11-01T01:00:00` 重复（`-0400` 与 `-0500` 两段）
  - `2026-11-01T01:30:00` 重复（`-0400` 与 `-0500` 两段）
- 结论：从 `UTC -> local` 的映射在 fall-back 日存在本地时间重复，但本脚本以 `dt_utc` 为唯一时间轴，不会发生丢 bar；本地日期归属需严格依赖 timezone 推导。

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --debug-overlap-sample --utc-start 2026-03-08T06:00:00Z --utc-end 2026-03-08T10:00:00Z --utc-step-minutes 30
```

- `new_york`：出现本地时钟缺失跳跃（`01:30 -> 03:00`），且 offset 从 `-0500` 切换到 `-0400`
- 结论：spring-forward 日存在本地时间缺失，但 `UTC -> local` 映射仍单调可用；session 划分必须按本地日期解释，不得使用固定 UTC 偏移。

## 当前已补“交易日本地日期归属”抽查证据

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --debug-local-date-binning --utc-start 2026-11-01T03:00:00Z --utc-end 2026-11-01T07:00:00Z --utc-step-minutes 30
```

- `new_york`：在 `2026-11-01T04:00Z` 本地时间跨日（`23:xx -> 00:00`），local_date 从 `2026-10-31` 切换为 `2026-11-01`；随后出现 `01:00/01:30` 重复但 local_date 保持 `2026-11-01`

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --debug-local-date-binning --utc-start 2026-03-08T03:00:00Z --utc-end 2026-03-08T07:00:00Z --utc-step-minutes 30
```

- `new_york`：在 `2026-03-08T05:00Z` 本地时间跨日（`23:xx -> 00:00`），local_date 从 `2026-03-07` 切换为 `2026-03-08`；后续 spring-forward 跳跃不影响 local_date 归属

## 当前已补“真实 bars 分桶”抽查证据（by_local_date + OR window）

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --debug-bars-binning --utc-start 2026-06-01T03:50:00Z --utc-end 2026-06-01T04:10:00Z --bars-binning-limit-lines 40
```

- `new_york`：同一段真实 bars 内出现本地跨日切换：
  - `bars_transition utc=2026-06-01T04:00:00Z local=2026-06-01T00:00:00-0400 date=2026-05-31->2026-06-01`
  - `bars_local_date_bins={"2026-05-31": 10, "2026-06-01": 11}`

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --debug-bars-binning --utc-start 2026-06-01T22:50:00Z --utc-end 2026-06-01T23:10:00Z --bars-binning-limit-lines 40
```

- `london`：同一段真实 bars 内出现本地跨日切换：
  - `bars_transition utc=2026-06-01T23:00:00Z local=2026-06-02T00:00:00+0100 date=2026-06-01->2026-06-02`
  - `bars_local_date_bins={"2026-06-01": 10, "2026-06-02": 11}`

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --debug-bars-binning --utc-start 2026-06-01T06:55:00Z --utc-end 2026-06-01T07:35:00Z --bars-binning-limit-lines 20
```

- `london`：OR window 命中数验证（M1 + 30min）：
  - `bars_or_hits_by_local_date={"2026-06-01": 30}`

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --debug-bars-binning --utc-start 2026-06-01T13:25:00Z --utc-end 2026-06-01T14:05:00Z --bars-binning-limit-lines 20
```

- `new_york`：OR window 命中数验证（M1 + 30min）：
  - `bars_or_hits_by_local_date={"2026-06-01": 30}`

## 当前已补 OR 边界语义验证（[start,end) 与 post_or>=end）

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --debug-bars-binning --utc-start 2026-06-01T06:59:00Z --utc-end 2026-06-01T07:31:00Z --bars-binning-limit-lines 80
```

- `london`：`07:00Z`（本地 `08:00`）开始 `in_or=1`；到 `07:29Z` 仍 `in_or=1`；`07:30Z`（本地 `08:30`）开始 `in_or=0` 且 `post_or=1`

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py --debug-bars-binning --utc-start 2026-06-01T13:29:00Z --utc-end 2026-06-01T14:01:00Z --bars-binning-limit-lines 80
```

- `new_york`：`13:30Z`（本地 `09:30`）开始 `in_or=1`；到 `13:59Z` 仍 `in_or=1`；`14:00Z`（本地 `10:00`）开始 `in_or=0` 且 `post_or=1`

## 不通过时怎么处理

- 若 session 与 timezone 不一致：
  - 不写入真实数据
- 若 DST 解释不清：
  - 先保留 `v1` 示例行状态
  - 不宣称已真实接入
- 若需要新增 session：
  - 先补 registry
  - 再补 notes / append protocol
  - 必要时新开版本
