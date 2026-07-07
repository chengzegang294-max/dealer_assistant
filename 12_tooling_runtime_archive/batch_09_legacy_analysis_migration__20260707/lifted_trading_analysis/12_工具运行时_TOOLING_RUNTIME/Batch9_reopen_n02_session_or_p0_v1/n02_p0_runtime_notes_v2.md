# n02_p0_runtime_notes v2

## 角色

- 这份文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `REOPEN_B9_N02_SESSION_OR_P0` 在 v2 版本的运行口径与产物边界。

## 当前状态

- v2 用于补齐 v1 中无法落盘的字段级差异：
  - `first_break_mode`
- v2 的 runtime csv：
  - `n02_p0_fields_runtime_v2.csv`

## v2 表头

- 在 v1 的基础上新增：
  - `first_break_mode`

## v2 口径说明

- `first_break_direction`：仍只允许 `up / down / none`
- `first_break_mode`：只允许 `close / wick / none / ambiguous`
- 当前实现为：
  - `close-first + wick-fallback`
  - `dual-break`（同一根 bar 同时上破与下破）记为 `ambiguous`

## 当前不含

- `IB`
- `or_break_high / or_break_low`
- `target_trigger_source`

## 下一步怎么用

- ARCHIVE_ONLY_RUNTIME_MIRROR: 以下步骤只保留为旧 `REOPEN_B9_N02_SESSION_OR_P0` 的历史运行说明，不作为当前默认续跑入口。
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

- 历史主线顺序保持为：`REOPEN_B9_N02_SESSION_OR_P0 -> IB`
- `IB` 当前先只做 proof-of-mapping，不写入 `n02_p0_fields_runtime_v2.csv`
- `IB` 对应入口与验收看：
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\REOPEN_B9_N02_IB_后续对象定义入口_v1.md`
  - `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\REOPEN_B9_N02_IB_OBJECT_P0_对象入口_v1.md`

### N02 P0 真实接入（MT4/MT5 导出 -> runtime v2）

- 先看 drop 目录候选：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_mt5_export_ingest_v1.py --symbol EURUSD --timeframe M1 --source-timezone <SOURCE_TZ> --list-drop`
- 把一份导出 CSV 转成 repo 内 canonical bars：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_mt5_export_ingest_v1.py --latest --symbol EURUSD --timeframe M1 --source-timezone <SOURCE_TZ> --dest 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_first_real_input_bars_v1.csv`
- 基于 canonical bars 生成 N02 P0 proof：
  - `python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_proof_of_mapping_v2.py`
- 把 proof 追加进 runtime v2：
  - dry-run：`python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_p0_runtime_append_from_proof_v2.py`
  - persist：`python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_p0_runtime_append_from_proof_v2.py --persist`
  - 覆盖概况（可选输出 report）：`--report-json <path>`

## 2026-07-03 readiness / dry-run 结果

- drop 探测：
  - `python real_input_samples\n02_mt5_export_ingest_v1.py --symbol EURUSD --timeframe M1 --source-timezone UTC --list-drop`
  - 结果：`drop_dir_exists=true`、`drop_csv_count=5`
  - 当前已发现候选：`eurusd_m1_export.csv`、`single_verify_eurusd_m1.csv`
- 本轮验证链路：
  - ingest：`python real_input_samples\n02_mt5_export_ingest_v1.py --input .\data\mt_exports_drop\single_verify_eurusd_m1.csv --symbol EURUSD --timeframe M1 --source-timezone UTC --dest real_input_samples\n02_real_input_eurusd_m1_20260610_utc_v1.csv`
  - proof：`python real_input_samples\n02_proof_of_mapping_v2.py --input real_input_samples\n02_real_input_eurusd_m1_20260610_utc_v1.csv --output real_input_samples\n02_proof_of_mapping_output__single_verify_20260610_utc_v1.csv`
  - append：`python n02_p0_runtime_append_from_proof_v2.py --proof real_input_samples\n02_proof_of_mapping_output__single_verify_20260610_utc_v1.csv --dest n02_p0_fields_runtime_v2.csv`
- 本轮统计：
  - `ingest rows=1440`
  - `first_bar_time_utc=2026-06-10T00:00:00Z`
  - `last_bar_time_utc=2026-06-11T00:00:00Z`
  - `proof_rows=4`
  - `rows_or_defined=2`
  - `first_break_down=2`
  - `first_break_none=2`
  - `append mode=dry_run`
  - `runtime_rows_before=165`
  - `runtime_rows_after_append=165`
- 当前结论：
  - `N02 P0` 的 ingest -> proof -> append 链已再次验证可执行。
  - 当时仍未对 `eurusd_m1_export.csv` 的 `source_timezone` 做最终确认。

## 2026-07-03 source_timezone 判定 + latest persist

- 判定方法：
  - 选取 `2026-06-10 / 2026-06-11` 的典型 OR 高低值，对比 `eurusd_m1_export.csv` 原始导出里的 30 分钟窗口。
- 对齐结果：
  - `2026-06-10 london 07:00-07:30`：`high=1.15506 low=1.15467`，与 runtime v2 的 london OR 完全一致
  - `2026-06-10 new_york 13:30-14:00`：`high=1.15572 low=1.15503`，与 runtime v2 的 new_york OR 完全一致
  - `2026-06-11 london 07:00-07:30`：`high=1.15473 low=1.15425`，与 runtime v2 的 london OR 完全一致
  - `2026-06-11 new_york 13:30-14:00`：`high=1.15318 low=1.15248`，与 runtime v2 的 new_york OR 完全一致
- 判定结论：
  - `eurusd_m1_export.csv` 的原始时间戳按 `UTC` 解释成立，无需再切到 `Europe/London` 或 broker server time。
- 已执行 latest persist：
  - `python real_input_samples\n02_mt5_export_ingest_v1.py --latest --symbol EURUSD --timeframe M1 --source-timezone UTC --dest real_input_samples\n02_first_real_input_bars_v1.csv`
  - `python real_input_samples\n02_proof_of_mapping_v2.py`
  - `python n02_p0_runtime_append_from_proof_v2.py --persist`
- 本轮统计：
  - `ingest_rows=99500`
  - `first_bar_time_utc=2026-03-06T17:09:00Z`
  - `last_bar_time_utc=2026-06-12T00:00:00Z`
  - `proof_rows=165`
  - `rows_or_defined=138`
  - `runtime_rows_before=165`
  - `runtime_rows_after_append=165`
  - `or_defined_ratio=0.8363636363636363`
  - `london=69/81`
  - `new_york=69/84`
- 当前结论：
  - `N02 P0` 的 `latest + persist` 已完成。
  - 这份 runtime v2 已继续被下游用于 `IB vs OR relation` 关系层 fresh-run。
- 当时默认下一步不再是时区判定，而是进入 `first_break relative to IB/OR` 一类关系扩展，而不是回头重做 `IB_OBJECT_P0`。

## 2026-07-04 expand sample 复核 + EURUSD M5 fall DST validation

- 对 `n02_first_real_input_bars_v1.csv` 的扩样本复核：
  - 使用 `n02_expand_real_input_with_dst_v1.py` 尝试把：
    - `n02_dst_london_spring_20260327_20260331_bars.csv`
    - `n02_dst_newyork_spring_20260306_20260310_bars.csv`
    - `n02_dst_london_fall_20251023_20251028_bars.csv`
    - `n02_dst_newyork_fall_20251031_20251104_bars.csv`
    合并回主 canonical bars
  - 结果：
    - 春季 `M1` 样本与当前主 bars 重合，不产生净新增
    - 秋季两份样本为 `EURUSD/M5`，已过滤，不写入主 `M1` bars
    - 主 canonical bars 最终仍保持 `99500` 行
- 同轮已转做 `EURUSD/M5 fall DST` validation：
  - bars：
    - `real_input_samples\n02_real_input_eurusd_m5_fall_dst_v1.csv`
    - `real_input_samples\n02_real_input_eurusd_m5_fall_dst_report_v1.json`
  - OR proof：
    - `real_input_samples\n02_proof_of_mapping_output_eurusd_m5_fall_dst_v1.csv`
  - IB proof：
    - `real_input_samples\n02_ib_proof_of_mapping_output_eurusd_m5_fall_dst_v1.csv`
  - validation summary：
    - `n02_other_timeframe_validation_eurusd_m5_fall_dst_summary_v1.md`
    - `n02_other_timeframe_validation_eurusd_m5_fall_dst_summary_v1.json`
- 关键统计：
  - `m5_bars_rows=1440`
  - `m5_or_rows=15`
  - `m5_or_defined_rows=10`
  - `m5_ib_rows=10`
  - `m5_ib_defined_rows=10`
- 当前结论：
  - 现有仓内样本下，`expand sample` 对主 `EURUSD/M1` runtime 不产生净新增。
  - `other timeframe validation` 已在 `EURUSD/M5 fall DST` 上跑通最小 OR/IB proof 闭环。
  - 当前仍不把 `M5` 混入主 `M1` runtime。
