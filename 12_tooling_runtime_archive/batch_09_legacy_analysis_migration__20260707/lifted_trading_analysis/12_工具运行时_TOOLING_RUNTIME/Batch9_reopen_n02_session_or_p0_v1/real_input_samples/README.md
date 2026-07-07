# N02 real_input_samples

## 目的

- 作为 `REOPEN_B9_N02_SESSION_OR_P0` 在真实接入前的第一份可跑通输入样本。
- 重点是“输入字段形态 + 时间戳口径 + session 归属”，不是宣称已经完成真实接入。

## 文件

- `n02_first_real_input_bars_v1.csv`
  - 字段：`symbol,timeframe,bar_time,open,high,low,close`
  - `bar_time`：UTC，ISO8601（示例：`2026-06-12T07:00:00Z`）
  - 该样本包含两段：
    - `london`（06 月为 BST，`08:00 local == 07:00Z`）
    - `new_york`（06 月为 EDT，`09:30 local == 13:30Z`）
- `n02_mt5_export_ingest_v1.py`
  - 把 MT5 导出的 CSV 转成上述标准 bars CSV
  - 默认会覆盖写入 `n02_first_real_input_bars_v1.csv`，并自动备份旧文件（`.bak_YYYYmmddTHHMMSSZ`）
- `n02_mt4_hst_ingest_v1.py`
  - 把 MT4 `HST` 历史文件直接转成上述标准 bars CSV
  - 当前用于：
    - `12_tooling_runtime_archive\batch_05_legacy_mt4_probe_assets__20260706\03_MT4便携探针实例\history\VTMarkets-Live 2\GBPUSD-VIP15.hst -> n02_real_input_gbpusd_m15_v1.csv`
    - 同步产出 `n02_real_input_gbpusd_m15_report_v1.json`
- `n02_expand_real_input_with_dst_v1.py`
  - 把多份 canonical bars 去重合并成一份输出 CSV
  - 当前用于：
    - 复核 `EURUSD/M1` 主样本是否还能被 DST 补充样本扩容
    - 生成独立的 `EURUSD/M5 fall DST` validation bars
- `n02_aggregate_bars_to_m5_v1.py`
  - 把主 `EURUSD/M1` canonical bars 聚合成 `EURUSD/M5` bars
  - 当前用于：
    - 生成 `EURUSD/M5 from main M1` wider history validation bars
    - 保持 `M5` 验证链独立，不回写主 `M1` runtime
- `n02_or_proof_config_v1.json`
  - OR proof 的 session 定义（时区 + 本地开盘时刻 + OR 窗口）
- `n02_proof_of_mapping_v1.py`
  - 基于 bars + config 输出第一轮 OR proof 结果（不写入 runtime 主 CSV）
- `n02_ib_proof_of_mapping_v1.py`
  - 基于 bars + config 输出第一轮 IB proof 结果（不写入 runtime 主 CSV）
- `n02_real_input_eurusd_m5_fall_dst_v1.csv`
  - `EURUSD/M5` 秋季 DST validation bars
- `n02_real_input_eurusd_m5_fall_dst_report_v1.json`
  - 上述 validation bars 的合并报告
- `n02_proof_of_mapping_output_eurusd_m5_fall_dst_v1.csv`
  - `EURUSD/M5` 秋季 DST validation 的 OR proof 输出
- `n02_ib_proof_of_mapping_output_eurusd_m5_fall_dst_v1.csv`
  - `EURUSD/M5` 秋季 DST validation 的 IB proof 输出
- `n02_real_input_eurusd_m5_from_m1_main_v1.csv`
  - 主 `EURUSD/M1` 聚合出来的 `EURUSD/M5` wider history validation bars
- `n02_real_input_eurusd_m5_from_m1_main_report_v1.json`
  - 上述聚合 bars 的分桶与丢弃统计
- `n02_proof_of_mapping_output_eurusd_m5_from_m1_main_v1.csv`
  - `EURUSD/M5 from main M1` wider history validation 的 OR proof 输出
- `n02_ib_proof_of_mapping_output_eurusd_m5_from_m1_main_v1.csv`
  - `EURUSD/M5 from main M1` wider history validation 的 IB proof 输出
- `n02_real_input_xauusd_m1_tail_v1.csv`
  - `XAUUSD/M1` other symbol validation 的 canonical bars
- `n02_proof_of_mapping_output_xauusd_m1_tail_v1.csv`
  - `XAUUSD/M1 tail` other symbol validation 的 OR proof 输出
- `n02_ib_proof_of_mapping_output_xauusd_m1_tail_v1.csv`
  - `XAUUSD/M1 tail` other symbol validation 的 IB proof 输出
- `n02_real_input_xauusd_m5_jobs_v1.csv`
  - `XAUUSD/M5 jobs` other symbol + other timeframe validation 的 canonical bars
- `n02_proof_of_mapping_output_xauusd_m5_jobs_v1.csv`
  - `XAUUSD/M5 jobs` other symbol + other timeframe validation 的 OR proof 输出
- `n02_ib_proof_of_mapping_output_xauusd_m5_jobs_v1.csv`
  - `XAUUSD/M5 jobs` other symbol + other timeframe validation 的 IB proof 输出
- `n02_real_input_xauusd_m5_from_m1_tail_v1.csv`
  - 显式 `UTC` 的 `XAUUSD/M1 tail` 聚合出来的 `M5` diagnostic bars，用于和 `XAUUSD/M5 jobs` 做重叠窗口对齐
- `n02_real_input_xauusd_m5_from_m1_tail_report_v1.json`
  - 上述 diagnostic 聚合 bars 的分桶统计
- `n02_real_input_gbpusd_h1_v1.csv`
  - `GBPUSD/H1` second FX symbol input gate 的 canonical bars
- `n02_ib_proof_of_mapping_output_gbpusd_h1_v1.csv`
  - `GBPUSD/H1` second FX symbol input gate 的 IB proof 输出
- `n02_real_input_gbpusd_m15_v1.csv`
  - `GBPUSD/M15` second FX sub-hour historical recovered 的 canonical bars
- `n02_real_input_gbpusd_m15_report_v1.json`
  - 上述 `GBPUSD/M15` recovered bars 的 ingest report
- `n02_proof_of_mapping_output_gbpusd_m15_v1.csv`
  - `GBPUSD/M15` second FX sub-hour historical recovered 的 OR proof 输出
- `n02_ib_proof_of_mapping_output_gbpusd_m15_v1.csv`
  - `GBPUSD/M15` second FX sub-hour historical recovered 的 IB proof 输出

## 如何用这份样本校验映射

- 先过一遍 checklist：
  - `n02_p0_runtime_session_calendar_dst_checklist_v1.md`
- 再对照映射草案：
  - `n02_p0_real_input_mapping_draft_v1.md`
- 最终目标是把这份 bars 输入与 `session_binding_registry` 一起，映射到 `n02_p0_fields_runtime_v1.csv` 的字段落盘口径。

## 升级为“真正真实接入”的条件

- 以 MT5/broker 导出的 bar 数据替换本样本，并满足：
  - session 本地开盘时刻与 DST 解释无歧义
  - `session_id/session_timezone` 来自 registry，而不是手填

## MT5 导出 -> 替换样本（建议流程）

1. 从 MT5 导出 bars CSV（Date/Time/Open/High/Low/Close）
2. 运行导入脚本把它转成标准 bars：

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_mt5_export_ingest_v1.py --input "D:\path\to\mt5_export.csv" --symbol EURUSD --timeframe M1 --source-timezone Europe/London
```

如果你不想自己管路径，推荐把导出文件先放到：

- `.\data\mt_exports_drop\`
  - 以 `TRADING_ANALYSIS_DATA_ROOT` 为根（默认：`.\data`），推荐投递区：`.\data\mt_exports_drop\`

若不确定导出时间属于哪个时区，先用 dry-run 观察首尾时间再决定 `--source-timezone`：

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_mt5_export_ingest_v1.py --input "D:\path\to\mt5_export.csv" --symbol EURUSD --timeframe M1 --source-timezone Europe/London --dry-run
```

3. 跑第一轮 OR proof（输出到 `n02_proof_of_mapping_output_v1.csv`）：

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v1.py
```

4. 跑第一轮 IB proof（输出到 `n02_ib_proof_of_mapping_output_v1.csv`）：

```powershell
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_ib_proof_of_mapping_v1.py
```
