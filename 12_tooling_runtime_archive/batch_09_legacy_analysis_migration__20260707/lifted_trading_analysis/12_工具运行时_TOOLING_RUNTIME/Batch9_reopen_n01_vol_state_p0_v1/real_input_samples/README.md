# N01 真实输入样本

- ARCHIVE_ONLY_RUNTIME_MIRROR: 本目录只保留 `REOPEN_B9_N01_VOL_STATE_P0` 的历史真实接入样本说明，不作为当前默认接入入口。
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 目的

- 作为 `REOPEN_B9_N01_VOL_STATE_P0` 在真实接入前的第一份可跑通输入样本。
- 重点是“OHLC 输入形态 + bar_time 口径 + 历史长度是否够计算”，不是宣称已经完成真实接入。

## 文件

- `n01_first_real_input_bars_v1.csv`
  - 字段：`symbol,timeframe,bar_time,open,high,low,close`
  - `bar_time`：UTC，ISO8601（示例：`2026-06-12T06:00:00Z`）
  - 该样本提供 `70` 根 `H1` bar：
    - 足够验证 `atr_value`（>=14）
    - 足够覆盖 `atr_ratio` 的最小历史（当 baseline 定义为 `SMA(ATR, 50)` 时，需要 `14 + 50 - 1 = 63` 根 bar）
    - 不足以验证 `atr_percentile`（>=252）
- `n01_mt5_export_ingest_v1.py`
  - 把 MT5 导出的 CSV 转成上述标准 bars CSV
  - 默认会覆盖写入 `n01_first_real_input_bars_v1.csv`，并自动备份旧文件（`.bak_YYYYmmddTHHMMSSZ`）
- `n01_proof_of_mapping_v1.py`
  - 基于 bars 输出第一轮 ATR proof 结果（不写入 runtime 主 CSV）

## 如何用这份样本校验映射

- 先过一遍 checklist：
  - `n01_p0_runtime_atr_calculation_checklist_v1.md`
- 再对照映射草案：
  - `n01_p0_real_input_mapping_draft_v1.md`

## 升级为“真正真实接入”的条件

- 用 MT5/broker 导出的历史 bar 替换本样本，并满足：
  - `bar_time` 时区口径稳定（统一 UTC）
  - 历史长度覆盖到：
    - `>=252`（才能宣称 percentile 已真实接入）

## MT5 导出 -> 替换样本（历史流程样例）

1. 从 MT5 导出 bars CSV（Date/Time/Open/High/Low/Close）
2. 运行导入脚本把它转成标准 bars：

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input "D:\path\to\mt5_export.csv" --symbol EURUSD --timeframe H1 --source-timezone UTC
```

如果你不想自己管路径，推荐把导出文件先放到：

- `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\mt_exports_drop\`

若不确定导出时间属于哪个时区，先用 dry-run 观察首尾时间再决定 `--source-timezone`：

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_mt5_export_ingest_v1.py --input "D:\path\to\mt5_export.csv" --symbol EURUSD --timeframe H1 --source-timezone UTC --dry-run
```

3. 跑第一轮 ATR proof（输出到 `n01_proof_of_mapping_output_v1.csv`）：

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_proof_of_mapping_v1.py
```

- 上述命令只保留为旧链路追溯样例，不再作为当前默认接入步骤。
