# Probe Batch 01 Acceptance Check

## 目的

- 这份文件用于证明 `batch_01_volty_xbreaking` 的当前运行时批次不是“只把文件收进来”，而是做过批次级结构与内容校验。

## 校验脚本

- 文件：
  - `probe_batch_acceptance_v1.py`
- 执行命令：
  - `python probe_batch_acceptance_v1.py --json-only`
  - `python probe_batch_acceptance_v1.py --json-only --write-json`
- 最新快照：
  - `acceptance_snapshots\probe_batch_01_acceptance_latest.json`

## 校验范围

- 目录结构：
  - `artifacts\volty\csv`
  - `artifacts\volty\log`
  - `artifacts\volty\tester_report`
  - `artifacts\xbreaking\csv`
  - `artifacts\xbreaking\log`
  - `artifacts\xbreaking\tester_report`
- 内容校验：
  - `Volty` summary 规范化
  - `Volty` series 规范化
  - `XBreaking` probe CSV 基础结构与 buffer 概况

## 本次实测结果

- `Volty`
  - `csv_present`: `true`
  - `csv_files`:
    - `MT4_probe_Volty_EURUSD_H4_20250102_000000.csv`
    - `MT4_probe_Volty_EURUSD_H1_20250102_000000.csv`
    - `MT4_probe_Volty_EURUSD_H1_20250102_000000_20260701T035759.csv`
  - `summary_status_done`: `true`
  - `tester_report_present`: `true`
  - `tester_report_files`:
    - `mt4probe_volty_portable.htm`
    - `mt4probe_volty_dumpseries_portable.htm`
    - `mt4probe_volty_dumpseries_portable_20260701T035759.htm`
  - `log_present`: `true`
  - `log_files`:
    - `20260701.log`
    - `20260701__excerpt.txt`
    - `20260701_20260701T035759.log`
    - `20260701_20260701T035759__excerpt.txt`
  - `current_fresh_run_csv`: `MT4_probe_Volty_EURUSD_H1_20250102_000000_20260701T035759.csv`
  - `series_row_count`: `350`
  - `volty_trend_state`: `up`
- `XBreaking`
  - `csv_present`: `true`
  - `csv_files`:
    - `XBreaking_probe_EURUSD_H1_20250101_220500.csv`
    - `XBreaking_probe_EURUSD_H1_20250102_000030.csv`
  - `current_fresh_run_csv`: `XBreaking_probe_EURUSD_H1_20250102_000030.csv`
  - `status_done`: `true`
  - `handle`: `10`
  - `init_err`: `0`
  - `buffer_activity_profile`: `buffer0_only`
  - `copy_failed_buffers`: `[1, 2, 3, 4, 5, 6, 7]`
  - `tester_report_present`: `true`
  - `tester_report_files`:
    - `xbreaking_probe_portable.htm`
  - `log_present`: `true`
  - `log_files`:
    - `20260609.log`
    - `20260609__excerpt.txt`
    - `20260701.log`
    - `20260701__excerpt.txt`
    - `20260701_20260701T041405.log`
    - `20260701_20260701T041405__excerpt.txt`

## 当前裁决

- 本批已达到：
  - `runtime_dirs_present`
  - `volty_summary_normalization_verified`
  - `volty_series_ready`
  - `xbreaking_probe_csv_verified`
  - `xbreaking_tester_report_present`
  - `batch_01_closed_without_missing_next_actions`

## 缺口解释

- `Volty`
  - 旧实例原始 `EURUSD60.hst` 在 `2021-07 -> 2025-05` 之间存在断层，因此第一次 `DumpSeries` 自动化只生成 report/log，没有生成 `csv`。
  - 当前已通过 `fill_mt4_eurusd_h1_history_v1.py` 把 `VTMarkets-Live 2\EURUSD-VIP60.hst` 的缺失 bar 合并进旧实例 `EURUSD60.hst`，并删除旧 `EURUSD60_0.fxt` 触发重建。
  - 当前 `tester\logs\20260701.log` 已明确记录第二轮 fresh-run 参数：`DumpSeries=1; DumpModeStart=0; DumpModeEnd=6;`。
  - 当前最新 `H1` fresh-run CSV 已包含 `series;...` 行，`normalize-volty-series` 已输出 `series_row_count = 350`，因此 `Volty` 侧的 `series -> field row` 闭环已达成。
- `XBreaking`
  - 当前 `csv` 证明 `handle=10`、`init_err=0`、`buffer0_only` 访问模式成立。
  - 当前已新增一轮 `MT5` fresh-run `csv + tester report + terminal log + tester log`，其中 tester log 明确记录 `XBreakingProbe: DONE`。
  - 当前实测表明 `Report=xbreaking_probe_portable` 时，报告会落在 `MT5 data root` 根目录，而不一定落在 `tester\files`。
  - 当前语义边界已经从 `probe_verified / report_missing` 升级到 `probe_verified / report_present / journal_present`，剩余工作转向 buffer 语义验证，而不是继续补 report。
  - `validation_matrix\` 下的跨场景样本属于额外语义复核证据，本验收脚本当前不把它纳入“批次闭环硬门槛”。

## 当前下一步

- 当前验收脚本已开始输出 `next_actions`，用于把“缺什么证据、下一条跑什么命令”直接固化到 JSON 快照里。
- 当前最新快照 `next_actions = []`，说明这批不再有硬缺口。
- 当前后续优先顺序固定为：
  - `Volty`：继续用 `DumpSeries` 行级证据升级字段定义
  - `XBreaking`：继续做 buffer 语义验证，不再把 report 回收当主阻塞
- 每次新产物入库后，先跑：
  - `python probe_batch_acceptance_v1.py --json-only`
  - 必要时再跑：
    - `python probe_batch_acceptance_v1.py --json-only --write-json`

## 补充搜索结论

- 已额外搜索：
  - `d:\Stock\trading_analysis`
  - `d:\Stock\trading_assistant`
  - `d:\Stock`
- 搜索目标：
  - `xbreaking*.htm / html / gif / csv / log / txt`
  - `20260609_xbreaking_probe_report`
  - `20260609_mt4probe_xbreaking`
- 当前结果：
  - 已确认新的 fresh-run `XBreaking tester report` 实际存在
  - 当前已回收到 `artifacts\xbreaking\tester_report\xbreaking_probe_portable.htm`
  - 当前已额外回收到强相关 `tester log`：`artifacts\xbreaking\log\20260701_20260701T041405.log`
- 当前裁决：
  - `xbreaking_tester_report_present=true`，当前仓内批次证据已闭环

## 入库判断

- 当前这批运行时材料可以保留在新仓，因为：
  - 所有目录结构已固定
  - `Volty / XBreaking` 都已有 fresh-run `csv`
  - `Volty / XBreaking` 都已有对应 `tester report`
  - `Volty / XBreaking` 都已有日志侧佐证，且 `XBreaking` 已补强相关 `tester log`
- 后续任何新产物进入本批前，应先跑一次：
  - `python probe_batch_acceptance_v1.py --json-only`
