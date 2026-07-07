# Probe Batch 01 Provenance Noteboard

## 目的

- 这份文件不是替代执行卡或产物索引，而是把“当前这批里每个核心文件是谁、怎么来的、现在干什么”一次写清。
- 它用于避免后续看到 `csv / log / report / py / ini` 时，只知道文件名，不知道用途和来源。

## 当前批次范围

- 批次：`batch_01_volty_xbreaking`
- 对象：
  - `Volty`
  - `XBreaking`
- 平台：
  - `MT4`
  - `MT5`

## 当前规则

- `fresh_run`
  - 当前终端重新跑出并回收到新仓库的证据
- `historical_recovered`
  - 旧仓库里已存在，后回收到新仓库的证据
- `weak_evidence`
  - 文件已找到，但不能直接证明目标 probe 已跑通
- `pending`
  - 该类证据当前还没有

## Volty

### Generator

- 文件：`12_tooling_runtime_archive\batch_02_mt_indicator_family\MT4Probe_Volty.mq4`
  - 类型：`GENERATOR`
  - producer：`MT4Probe_Volty`
  - 生成对象：`Volty probe csv`
  - 默认输出：`MT4_probe_Volty_<SYMBOL>_<TF>_<STAMP>.csv`
  - 当前作用：`Volty` 的 `MT4` probe 入口
  - 关键参数：`DumpSeries / DumpModeStart / DumpModeEnd`（默认关闭；开启后追加 series 行）
  - 当前状态：`known_generator`

- 文件：`12_tooling_runtime_archive\batch_02_mt_indicator_family\VoltyChannel_Stop_v2_1M.mq4`
  - 类型：`GENERATOR`
  - producer：`VoltyChannel_Stop_v2_1M`
  - 生成对象：被 `MT4Probe_Volty` 调用的指标输出
  - 当前作用：`Volty` 指标本体
  - 当前状态：`known_generator`

- 文件：`12_tooling_runtime_archive\batch_02_mt_indicator_family\mt4probe_volty_portable.ini`
  - 类型：`GENERATOR`
  - producer：`MT4 strategy tester ini`
  - 当前作用：旧测试参数参考，不是新仓库默认执行稿
  - 当前状态：`archive_reference_only`

- 文件：`MT4Probe_Volty_dumpseries_0_6.ini`
  - 类型：`GENERATOR`
  - producer：`batch_01 runtime template`
  - 生成对象：`Volty DumpSeries fresh-run`
  - 当前作用：把 `DumpSeries=1 / DumpModeStart=0 / DumpModeEnd=6` 固定成可复制的 tester 参数模板
  - 当前状态：`batch_local_rerun_ready`

- 文件：`mt4probe_volty_dumpseries_portable.ini`
  - 类型：`GENERATOR`
  - producer：`batch_01 runtime template`
  - 生成对象：`MT4 portable tester launch`
  - 当前作用：把 `EURUSD / H1 / Open prices only / 2025.01.01 -> 2025.01.15` 固定成批次内启动模板
  - 当前状态：`batch_local_rerun_ready`

- 文件：`fill_mt4_eurusd_h1_history_v1.py`
  - 类型：`GENERATOR`
  - producer：`batch_01 history patch helper`
  - 生成对象：`legacy MT4 EURUSD/H1 history backfill`
  - 当前作用：把 `VTMarkets-Live 2\EURUSD-VIP60.hst` 的缺失 bar 合并进旧实例 `EURUSD60.hst`，并删除旧 `EURUSD60_0.fxt`
  - 当前状态：`batch_local_history_patch_ready`

- 文件：`run_volty_dumpseries_gui_once.ps1`
  - 类型：`GENERATOR`
  - producer：`batch_01 gui automation helper`
  - 生成对象：`Volty DumpSeries best-effort GUI rerun`
  - 当前作用：自动注入本批参数模板、拉起 MT4 便携实例、触发 tester、等待新产物并恢复默认配置
  - 当前状态：`batch_local_gui_rerun_ready`

### Artifact

- 文件：`artifacts\volty\csv\MT4_probe_Volty_EURUSD_H4_20250102_000000.csv`
  - 类型：`ARTIFACT`
  - source_path：`旧仓库\12_工具运行时_TOOLING_RUNTIME\03_MT4便携探针实例\tester\files\MT4_probe_Volty_EURUSD_H4_20250102_000000.csv`
  - repo_path：`artifacts\volty\csv\MT4_probe_Volty_EURUSD_H4_20250102_000000.csv`
  - producer：`MT4Probe_Volty.mq4`
  - scope：`Volty / EURUSD / H4`
  - evidence_mode：`historical_recovered`
  - status：`recovered_and_verified`
  - current_role：`历史硬证据`
  - 备注：当前已确认 `mode 1/4/5/6/7` 非空，且 `status=DONE`

- 文件：`artifacts\volty\tester_report\mt4probe_volty_portable.htm`
  - 类型：`ARTIFACT`
  - source_path：`旧仓库\12_工具运行时_TOOLING_RUNTIME\03_MT4便携探针实例\tester\files\mt4probe_volty_portable.htm`
  - repo_path：`artifacts\volty\tester_report\mt4probe_volty_portable.htm`
  - producer：`MT4 strategy tester`
  - scope：`Volty / EURUSD / H4`
  - evidence_mode：`historical_recovered`
  - status：`recovered`
  - current_role：`历史辅助证据`
  - 备注：能证明旧测试器曾输出报告，但当前未补明确 journal/log

- 文件：`artifacts\volty\csv\MT4_probe_Volty_EURUSD_H1_20250102_000000_20260701T035759.csv`
  - 类型：`ARTIFACT`
  - source_path：`旧仓库\12_工具运行时_TOOLING_RUNTIME\03_MT4便携探针实例\tester\files\MT4_probe_Volty_EURUSD_H1_20250102_000000.csv`
  - repo_path：`artifacts\volty\csv\MT4_probe_Volty_EURUSD_H1_20250102_000000_20260701T035759.csv`
  - producer：`MT4Probe_Volty.mq4`
  - scope：`Volty / EURUSD / H1 / DumpSeries=1`
  - evidence_mode：`fresh_run`
  - status：`recovered_and_verified`
  - current_role：`当前硬证据`
  - 备注：当前已确认 `series_row_count = 350`，`DumpSeries / DumpModeStart / DumpModeEnd` 已真实生效

- 文件：`artifacts\volty\tester_report\mt4probe_volty_dumpseries_portable_20260701T035759.htm`
  - 类型：`ARTIFACT`
  - source_path：`旧仓库\12_工具运行时_TOOLING_RUNTIME\03_MT4便携探针实例\tester\files\mt4probe_volty_dumpseries_portable.htm`
  - repo_path：`artifacts\volty\tester_report\mt4probe_volty_dumpseries_portable_20260701T035759.htm`
  - producer：`MT4 strategy tester`
  - scope：`Volty / EURUSD / H1 / DumpSeries=1`
  - evidence_mode：`fresh_run`
  - status：`recovered`
  - current_role：`当前辅助证据`
  - 备注：报告参数区已明确记录 `DumpSeries=true; DumpModeStart=0; DumpModeEnd=6;`

- 文件：`artifacts\volty\log\20260701_20260701T035759.log`
  - 类型：`ARTIFACT`
  - source_path：`旧仓库\12_工具运行时_TOOLING_RUNTIME\03_MT4便携探针实例\tester\logs\20260701.log`
  - repo_path：`artifacts\volty\log\20260701_20260701T035759.log`
  - producer：`MT4 strategy tester`
  - scope：`Volty / EURUSD / H1 / DumpSeries=1`
  - evidence_mode：`fresh_run`
  - status：`recovered`
  - current_role：`当前日志硬佐证`
  - 备注：已明确记录第一次 `no history data` 与第二次 `DumpSeries=1` 成功写出 `DONE file`

- 文件：`artifacts\volty\history_patch\fill_mt4_eurusd_h1_history_latest.json`
  - 类型：`ARTIFACT`
  - source_path：`fill_mt4_eurusd_h1_history_v1.py`
  - repo_path：`artifacts\volty\history_patch\fill_mt4_eurusd_h1_history_latest.json`
  - producer：`fill_mt4_eurusd_h1_history_v1.py`
  - scope：`legacy MT4 EURUSD/H1 history patch`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`补历史数据摘要`
  - 备注：记录了 source/target/backup/fxt 删除和窗口内 bar 数变化

## XBreaking

### Generator

- 文件：`12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreakingProbe.mq5`
  - 类型：`GENERATOR`
  - producer：`XBreakingProbe`
  - 生成对象：`XBreaking probe csv`
  - 当前作用：`XBreaking` 的 `MT5` probe 入口
  - 当前状态：`known_generator`

- 文件：`12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreaking.ex5`
  - 类型：`GENERATOR`
  - producer：`XBreaking`
  - 生成对象：被 `XBreakingProbe` 调用的指标输出
  - 当前作用：`XBreaking` 指标本体
  - 当前状态：`known_binary_indicator`

- 文件：`12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreakingProbe.ini`
  - 类型：`GENERATOR`
  - producer：`MT5 strategy tester ini`
  - 当前作用：`XBreakingProbe` 的 `MT5 tester` 参考模板
  - 当前状态：`repo_local_relative_report_ready`
  - 备注：`Report=` 已改为终端内相对 `tester\files\xbreaking_probe_portable.htm`，不再默认依赖旧仓库 `backtest_out`

- 文件：`12_tooling_runtime_archive\batch_02_mt_indicator_family\MT4Probe_XBreaking.ini`
  - 类型：`GENERATOR`
  - producer：`MT4 strategy tester ini`
  - 当前作用：`MT4IndicatorProbe + XBreaking` 的补充验证模板
  - 当前状态：`repo_local_relative_report_ready`
  - 备注：`TestExpert=Probe\MT4IndicatorProbe`，`TestReport=` 已改为终端内相对 `tester\files\mt4probe_xbreaking_portable`

- 文件：`12_tooling_runtime_archive\batch_02_mt_indicator_family\MT5SymbolDumpProbe.mq5`
  - 类型：`GENERATOR`
  - producer：`MT5SymbolDumpProbe`
  - 生成对象：`MarketWatch / AllSymbols symbol list`
  - 当前作用：在 `MT5 strategy tester` 中导出 `SymbolsTotal/SymbolName` 的真实品种清单，用于 broker alias 探测与跨环境对照
  - 当前状态：`known_generator`

- 文件：`12_tooling_runtime_archive\batch_02_mt_indicator_family\MT5SymbolDumpProbe.ex5`
  - 类型：`GENERATOR`
  - producer：`MT5SymbolDumpProbe`
  - 生成对象：`MarketWatch / AllSymbols symbol list`
  - 当前作用：`MT5SymbolDumpProbe.mq5` 的编译产物
  - 当前状态：`known_binary_expert`

- 文件：`run_mt5_symbol_dump_once.ps1`
  - 类型：`GENERATOR`
  - producer：`batch_01 mt5 symbol export helper`
  - 生成对象：`environment_snapshots/mt5_symbols_*`
  - 当前作用：按 `EnvironmentSelector` 在目标 MT5 环境运行 `MT5SymbolDumpProbe.ex5`，并把导出结果回收进 `environment_snapshots`
  - 当前状态：`batch_local_environment_snapshot_ready`

- 文件：`run_xbreaking_probe_once.ps1`
  - 类型：`GENERATOR`
  - producer：`batch_01 MT5 rerun helper`
  - 生成对象：`XBreaking fresh-run + validation_matrix archive`
  - 当前作用：部署 `XBreakingProbe.ex5 / XBreaking.ex5`、生成 `runtime .set + runtime .ini`、通过 `ExpertParameters=` 执行 `MT5 /config`、等待并归档新 `csv / report / log`
  - 当前状态：`batch_local_matrix_rerun_ready`
  - 备注：当前已实测打通 `EURUSD / H4 / IndicatorTf=H4`，且 `run_summary.json` 已绑定 `install_root / data_root / server / login / access_server`，并支持 `DataRootOverride` 与 `EnvironmentInventoryJson + EnvironmentSelector`；并修复了 strict mode 下 `data_root_override` 场景打印 `inventory_*` 字段导致的属性缺失错误

- 文件：`run_xbreaking_validation_matrix.ps1`
  - 类型：`GENERATOR`
  - producer：`batch_01 matrix runner`
  - 生成对象：`XBreaking validation_matrix multi-run`
  - 当前作用：按 `Symbols x Periods` 组合循环调用 `run_xbreaking_probe_once.ps1` 并生成多个 `validation_matrix\<ArchiveTag>\` 归档
  - 当前状态：`batch_local_matrix_runner_ready`

- 文件：`probe_mt_environment_inventory.ps1`
  - 类型：`GENERATOR`
  - producer：`batch_01 environment inventory helper`
  - 生成对象：`MetaQuotes runtime inventory snapshot`
  - 当前作用：扫描 `MetaQuotes\Terminal\*\origin.txt`、`Config\common.ini` 与最新 terminal log，输出 `platform / origin_path / login / server / access_server`
  - 当前状态：`batch_local_environment_inventory_ready`
  - 备注：当前快照已额外输出 `environment_label`，可直接作为 rerun 入口的环境选择键

- 文件：`probe_artifact_ingest_v1.py`
  - 类型：`GENERATOR`
  - producer：`batch_01 artifact ingest helper`
  - 生成对象：`batch artifacts + validation_matrix archive copies + ingest manifest + validation matrix index`
  - 当前作用：扫描 `MetaQuotes / portable terminal` 候选目录并回收 `csv / report / log`，必要时生成 log excerpt、`validation_matrix\<tag>\ingest_manifest.json` 与 `validation_matrix_index_latest.json`
  - 当前状态：`batch_local_ingest_and_provenance_ready`
  - 备注：当前已支持 `--archive-tag` 把回收记录写成 `source_path / repo_path / matched_keywords / excerpt_path` 闭环说明，并支持 `--write-validation-matrix-index` 与 `--backfill-ingest-manifest-from-archive`
  - 备注_2：当前已支持 `--backfill-missing-ingest-manifests` 批量补齐缺失的历史 `ingest_manifest.json`（均标记为 `historical_recovered`）

- 文件：`normalize_purchased_csv_contract_v1.py`
  - 类型：`GENERATOR`
  - producer：`batch_01 purchased csv contract normalizer`
  - 生成对象：`legacy purchased csv preview contract archive`
  - 当前作用：把 `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\` 根目录已购 `csv` 标准化成 `bar_time / symbol / timeframe / open / high / low / close / tick_volume / source_path / source_row_number / contract_version` 最小输入层
  - 当前状态：`batch_local_preview_contract_ready`
  - 备注：当前已实测 `xauusd_1h.csv / nas100_1h.csv / usoil_1h.csv`，其中 `usoil_1h.csv` 会按 broker alias 归一到 `XTIUSD`

### Artifact

- 文件：`artifacts\xbreaking\csv\XBreaking_probe_EURUSD_H1_20250101_220500.csv`
  - 类型：`ARTIFACT`
  - source_path：`本机终端目录（已脱敏）/XBreaking_probe_EURUSD_H1_20250101_220500.csv`
  - repo_path：`artifacts\xbreaking\csv\XBreaking_probe_EURUSD_H1_20250101_220500.csv`
  - producer：`XBreakingProbe.mq5`
  - scope：`XBreaking / EURUSD / H1`
  - evidence_mode：`historical_recovered`
  - status：`recovered_and_verified`
  - current_role：`历史硬证据`
  - 备注：已确认 `handle=10`、`init_err=0`，当前主要用于和本轮 fresh-run 对账

- 文件：`artifacts\xbreaking\csv\XBreaking_probe_EURUSD_H1_20250102_000030.csv`
  - 类型：`ARTIFACT`
  - source_path：`%APPDATA%\MetaQuotes\Terminal\Common\Files\XBreaking_probe_EURUSD_H1_20250102_000030.csv`
  - repo_path：`artifacts\xbreaking\csv\XBreaking_probe_EURUSD_H1_20250102_000030.csv`
  - producer：`XBreakingProbe.mq5`
  - scope：`XBreaking / EURUSD / H1`
  - evidence_mode：`fresh_run`
  - status：`recovered_and_verified`
  - current_role：`当前硬证据`
  - 备注：当前已确认 `buffer0_only`，且 `status=DONE`

- 文件：`artifacts\xbreaking\log\20260609__excerpt.txt`
  - 类型：`ARTIFACT`
  - source_path：`本机终端日志（已脱敏）`
  - repo_path：`artifacts\xbreaking\log\20260609__excerpt.txt`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`possible_xbreaking_related`
  - evidence_mode：`weak_evidence`
  - status：`derived_excerpt`
  - current_role：`日志摘录`
  - 备注：仅是辅助阅读文件，不构成独立硬证据

- 文件：`artifacts\xbreaking\log\20260609.log`
  - 类型：`ARTIFACT`
  - source_path：`本机终端日志（已脱敏）`
  - repo_path：`artifacts\xbreaking\log\20260609.log`
  - producer：`MT5 terminal`
  - scope：`possible_xbreaking_related`
  - evidence_mode：`weak_evidence`
  - status：`recovered`
  - current_role：`日志回收`
  - 备注：当前摘录内容主要为迁移日志片段，未检出 `XBreaking / XBreakingProbe / tester` 关键词，不能作为强相关 tester journal

- 文件：`artifacts\xbreaking\log\20260701.log`
  - 类型：`ARTIFACT`
  - source_path：`%APPDATA%\MetaQuotes\Terminal\<instance_id>\logs\20260701.log`
  - repo_path：`artifacts\xbreaking\log\20260701.log`
  - producer：`MT5 terminal`
  - scope：`XBreaking / EURUSD / H1`
  - evidence_mode：`fresh_run`
  - status：`recovered`
  - current_role：`终端级启动佐证`
  - 备注：当前已明确记录 `automatical testing started` 与 `last test passed with result "successfully finished"`

- 文件：`artifacts\xbreaking\log\20260701_20260701T041405.log`
  - 类型：`ARTIFACT`
  - source_path：`%APPDATA%\MetaQuotes\Terminal\<instance_id>\Tester\logs\20260701.log`
  - repo_path：`artifacts\xbreaking\log\20260701_20260701T041405.log`
  - producer：`MT5 strategy tester`
  - scope：`XBreaking / EURUSD / H1`
  - evidence_mode：`fresh_run`
  - status：`recovered`
  - current_role：`当前日志硬佐证`
  - 备注：已明确记录 `testing of Experts\XBreakingProbe.ex5`、`program file added: \Indicators\XBreaking.ex5` 与 `XBreakingProbe: DONE`

- 文件：`artifacts\xbreaking\tester_report\xbreaking_probe_portable.htm`
  - 类型：`ARTIFACT`
  - source_path：`%APPDATA%\MetaQuotes\Terminal\<instance_id>\xbreaking_probe_portable.htm`
  - repo_path：`artifacts\xbreaking\tester_report\xbreaking_probe_portable.htm`
  - producer：`MT5 strategy tester`
  - scope：`XBreaking / EURUSD / H1`
  - evidence_mode：`fresh_run`
  - status：`recovered`
  - current_role：`当前辅助证据`
  - 备注：参数区已明确记录 `InpIndicatorName=XBreaking`、`InpIndicatorTf=16385`、`InpBarsToProbe=200`

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_20260701_setmode\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_20260701_setmode\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURUSD / H4 / IndicatorTf=H4`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`validation matrix run index`
  - 备注：绑定 `runtime_set_write_mode=written`、源 `csv / report / terminal log / tester log` 与归档路径

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_20260701_setmode\csv\XBreaking_probe_EURUSD_H4_20250102_000030.csv`
  - 类型：`ARTIFACT`
  - source_path：`%APPDATA%\MetaQuotes\Terminal\Common\Files\XBreaking_probe_EURUSD_H4_20250102_000030.csv`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_20260701_setmode\csv\XBreaking_probe_EURUSD_H4_20250102_000030.csv`
  - producer：`XBreakingProbe.mq5`
  - scope：`XBreaking / EURUSD / H4`
  - evidence_mode：`fresh_run`
  - status：`recovered_and_verified`
  - current_role：`跨场景 buffer 语义复核硬证据`
  - 备注：当前已确认 `chart_tf=PERIOD_H4`、`indicator_tf=PERIOD_H4`、`status=DONE`，且访问形态仍为 `buffer0_only`

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_hard_20260701T1426\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_hard_20260701T1426\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURUSD / H4 / inventory_selector`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`selection_mode hard evidence`
  - 备注：`environment_selection_mode=inventory_selector`，且 `environment_inventory_*` 字段齐全，归档已包含 `csv / report / terminal log / tester log`

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_hard_20260701T1426\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_hard_20260701T1426\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / EURUSD / H4`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕（不伪装原始 source），并记录 repo 内归档文件清单

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_override_hard_20260701T1426\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_override_hard_20260701T1426\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURUSD / H4 / data_root_override`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`selection_mode hard evidence`
  - 备注：`environment_selection_mode=data_root_override`，归档已包含 `csv / report / terminal log / tester log`

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_override_hard_20260701T1426\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_override_hard_20260701T1426\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / EURUSD / H4`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕（不伪装原始 source），并记录 repo 内归档文件清单

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_feb_20260701T1615\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_feb_20260701T1615\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURUSD / H4 / inventory_selector / window=2025.02.03-2025.02.10`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`date_window robustness evidence`
  - 备注：在更远日期窗下复跑，`selection_mode=inventory_selector` 字段齐全，归档已包含 `csv / report / terminal log / tester log`

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_feb_20260701T1615\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_feb_20260701T1615\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / EURUSD / H4`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕（不伪装原始 source），并记录 repo 内归档文件清单

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_longwin_20260702T0038\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_longwin_20260702T0038\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURUSD / H4 / inventory_selector / window=2024.12.01-2025.03.01`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`long_window robustness evidence`
  - 备注：跨月长窗口复跑，`selection_mode=inventory_selector` 字段齐全，归档已包含 `csv / report / terminal log / tester log`

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_longwin_20260702T0038\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_longwin_20260702T0038\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / EURUSD / H4`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 `run_summary` 可追溯 source 与 `1` 条 repo-only backup log

- 文件：`artifacts\xbreaking\validation_matrix\usdjpy_h1_envselect_longwin_20260702T0041\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdjpy_h1_envselect_longwin_20260702T0041\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / USDJPY / H1 / inventory_selector / window=2024.12.01-2025.03.01`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`long_window robustness evidence`
  - 备注：跨月长窗口复跑，`selection_mode=inventory_selector` 字段齐全，归档已包含 `csv / report / terminal log / tester log`

- 文件：`artifacts\xbreaking\validation_matrix\usdjpy_h1_envselect_longwin_20260702T0041\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdjpy_h1_envselect_longwin_20260702T0041\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / USDJPY / H1`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 `run_summary` 可追溯 source 与 `1` 条 repo-only backup log

- 文件：`artifacts\xbreaking\validation_matrix\xauusd_h4_envselect_longwin_20260702T0044\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\xauusd_h4_envselect_longwin_20260702T0044\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / XAUUSD / H4 / inventory_selector / window=2024.12.01-2025.03.01`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`long_window robustness evidence`
  - 备注：跨月长窗口复跑，`selection_mode=inventory_selector` 字段齐全，归档已包含 `csv / report / terminal log / tester log`

- 文件：`artifacts\xbreaking\validation_matrix\xauusd_h4_envselect_longwin_20260702T0044\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\xauusd_h4_envselect_longwin_20260702T0044\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / XAUUSD / H4`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 `run_summary` 可追溯 source 与 `1` 条 repo-only backup log

- 文件：`artifacts\xbreaking\validation_matrix\us30_h4_envselect_longwin_20260702T0054\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\us30_h4_envselect_longwin_20260702T0054\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / US30 / H4 / inventory_selector / window=2024.12.01-2025.03.01`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`long_window robustness evidence`
  - 备注：跨月长窗口复跑，`selection_mode=inventory_selector` 字段齐全，归档已包含 `csv / report / terminal log / tester log`

- 文件：`artifacts\xbreaking\validation_matrix\us30_h4_envselect_longwin_20260702T0054\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\us30_h4_envselect_longwin_20260702T0054\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / US30 / H4`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 `run_summary` 可追溯 source 与 `1` 条 repo-only backup log

- 文件：`artifacts\xbreaking\validation_matrix\us30_h4_tmgm_longwin_20260702T0137\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\us30_h4_tmgm_longwin_20260702T0137\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / US30 / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成跨月长窗口复跑，`selection_mode=inventory_selector`、`environment_label` 与 `inventory_match_field` 字段齐全

- 文件：`artifacts\xbreaking\validation_matrix\us30_h4_tmgm_longwin_20260702T0137\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\us30_h4_tmgm_longwin_20260702T0137\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / US30 / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 `run_summary` 可追溯 source 与 `1` 条 repo-only backup log

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_tmgm_longwin_20260702T0143\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_tmgm_longwin_20260702T0143\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURUSD / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment forex hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 EURUSD/H4 跨月长窗口复跑，证明跨环境结论已从股指样本扩展到外汇主对

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_tmgm_longwin_20260702T0143\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_tmgm_longwin_20260702T0143\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / EURUSD / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment forex ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 `run_summary` 可追溯 source 与 `1` 条 repo-only backup log

- 文件：`artifacts\xbreaking\validation_matrix\usdjpy_h1_tmgm_longwin_20260702T0145\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdjpy_h1_tmgm_longwin_20260702T0145\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / USDJPY / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment jpy hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 USDJPY/H1 跨月长窗口复跑，证明跨环境结论已扩展到日系 H1 样本

- 文件：`artifacts\xbreaking\validation_matrix\usdjpy_h1_tmgm_longwin_20260702T0145\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdjpy_h1_tmgm_longwin_20260702T0145\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / USDJPY / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment jpy ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 `run_summary` 可追溯 source 与 `1` 条 repo-only backup log

- 文件：`artifacts\xbreaking\validation_matrix\gbpusd_h4_tmgm_longwin_20260702T0147\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbpusd_h4_tmgm_longwin_20260702T0147\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / GBPUSD / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment gbp hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 GBPUSD/H4 跨月长窗口复跑，证明跨环境结论已扩展到英镑 H4 样本

- 文件：`artifacts\xbreaking\validation_matrix\gbpusd_h4_tmgm_longwin_20260702T0147\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbpusd_h4_tmgm_longwin_20260702T0147\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / GBPUSD / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment gbp ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 `run_summary` 可追溯 source 与 `1` 条 repo-only backup log

- 文件：`artifacts\xbreaking\validation_matrix\xauusd_h4_tmgm_longwin_20260702T0152\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\xauusd_h4_tmgm_longwin_20260702T0152\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / XAUUSD / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment gold hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 XAUUSD/H4 跨月长窗口复跑，证明跨环境结论已从外汇与股指进一步扩展到黄金 H4 样本

- 文件：`artifacts\xbreaking\validation_matrix\xauusd_h4_tmgm_longwin_20260702T0152\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\xauusd_h4_tmgm_longwin_20260702T0152\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / XAUUSD / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment gold ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 `run_summary` 可追溯 source 与 `1` 条 repo-only backup log

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h1_tmgm_longwin_20260702T0202\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h1_tmgm_longwin_20260702T0202\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURUSD / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment forex h1 hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 EURUSD/H1 跨月长窗口复跑，证明跨环境结论已从主对 H4 继续扩展到主对 H1 样本

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h1_tmgm_longwin_20260702T0202\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h1_tmgm_longwin_20260702T0202\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / EURUSD / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment forex h1 ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 `run_summary` 可追溯 source 与 `1` 条 repo-only backup log

- 文件：`artifacts\xbreaking\validation_matrix\usdjpy_h4_tmgm_longwin_20260702T0210\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdjpy_h4_tmgm_longwin_20260702T0210\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / USDJPY / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment jpy h4 hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 USDJPY/H4 跨月长窗口复跑，证明跨环境结论已从日系 H1 继续扩展到日系 H4 样本

- 文件：`artifacts\xbreaking\validation_matrix\usdjpy_h4_tmgm_longwin_20260702T0210\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdjpy_h4_tmgm_longwin_20260702T0210\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / USDJPY / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment jpy h4 ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 `run_summary` 可追溯 source 与 `1` 条 repo-only backup log

- 文件：`artifacts\xbreaking\validation_matrix\us30_h1_tmgm_longwin_20260702T0222\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\us30_h1_tmgm_longwin_20260702T0222\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / US30 / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment index h1 hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 US30/H1 跨月长窗口复跑，证明跨环境结论已从股指 H4 继续扩展到股指 H1 样本

- 文件：`artifacts\xbreaking\validation_matrix\us30_h1_tmgm_longwin_20260702T0222\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\us30_h1_tmgm_longwin_20260702T0222\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / US30 / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment index h1 ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 `run_summary` 可追溯 source 与 `1` 条 repo-only backup log

- 文件：`PURCHASED_MARKET_DATA_INVENTORY.md`
  - 类型：`INDEX_NOTE`
  - source_path：`12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\VTMarkets-Live 2\*.hst` + `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\*.csv|*.xls|*.xlsx`
  - repo_path：`PURCHASED_MARKET_DATA_INVENTORY.md`
  - producer：`manual inventory synthesis from legacy runtime history`
  - scope：`purchased market data / forex + metals + indices + macro / legacy HST + data-root CSV/XLSX`
  - evidence_mode：`historical_recovered`
  - status：`written`
  - current_role：`已购历史数据清单入口`
  - 备注：当前固定了“你买过的数据”在仓库中的识别规则：一条证据链是 `VTMarkets-Live 2` 下的 `VIP*.hst` 与同目录股指 `.hst`，另一条证据链是 `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\` 根目录本层的已购 `CSV/XLSX`；`EURUSD-VIP60.hst` 已被工程链实际消费，`_xau_test_1h.csv` 已被用户明确确认为旧仓已购数据样本

- 文件：`artifacts\xbreaking\validation_matrix\xauusd_h1_tmgm_longwin_20260702T0234\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\xauusd_h1_tmgm_longwin_20260702T0234\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / XAUUSD / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment gold h1 hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 XAUUSD/H1 跨月长窗口复跑，证明跨环境结论已从黄金 H4 继续扩展到黄金 H1 样本

- 文件：`artifacts\xbreaking\validation_matrix\xauusd_h1_tmgm_longwin_20260702T0234\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\xauusd_h1_tmgm_longwin_20260702T0234\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / XAUUSD / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment gold h1 ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 `run_summary` 可追溯 source 与 `1` 条 repo-only backup log

- 文件：`artifacts\xbreaking\validation_matrix\gbpusd_h1_tmgm_longwin_20260702T0250\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbpusd_h1_tmgm_longwin_20260702T0250\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / GBPUSD / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment gbp h1 hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 GBPUSD/H1 跨月长窗口复跑，证明跨环境结论已从英镑 H4 继续扩展到英镑 H1 样本

- 文件：`artifacts\xbreaking\validation_matrix\gbpusd_h1_tmgm_longwin_20260702T0250\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbpusd_h1_tmgm_longwin_20260702T0250\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / GBPUSD / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment gbp h1 ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 `run_summary` 可追溯 source 与 `1` 条 repo-only backup log

- 文件：`artifacts\xbreaking\validation_matrix\xagusd_h1_tmgm_longwin_20260702T0302\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\xagusd_h1_tmgm_longwin_20260702T0302\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / XAGUSD / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment silver h1 hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 XAGUSD/H1 跨月长窗口复跑，证明跨环境结论已从黄金扩展到白银 H1 样本

- 文件：`artifacts\xbreaking\validation_matrix\xagusd_h1_tmgm_longwin_20260702T0302\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\xagusd_h1_tmgm_longwin_20260702T0302\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / XAGUSD / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment silver h1 ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 `run_summary` 可追溯 source 与 `1` 条 repo-only backup log

- 文件：`artifacts\xbreaking\validation_matrix\xagusd_h4_tmgm_longwin_20260702T0315\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\xagusd_h4_tmgm_longwin_20260702T0315\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / XAGUSD / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment silver h4 hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 XAGUSD/H4 跨月长窗口复跑，证明跨环境结论已从白银 H1 继续扩展到白银 H4 样本

- 文件：`artifacts\xbreaking\validation_matrix\xagusd_h4_tmgm_longwin_20260702T0315\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\xagusd_h4_tmgm_longwin_20260702T0315\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / XAGUSD / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment silver h4 ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 `run_summary` 可追溯 source 与 `1` 条 repo-only backup log

- 文件：`artifacts\xbreaking\validation_matrix\nas100_h1_tmgm_longwin_20260702T0332\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\nas100_h1_tmgm_longwin_20260702T0332\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / NAS100 / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment nas100 h1 hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 NAS100/H1 跨月长窗口复跑，证明跨环境结论已扩展到新的股指样本，并为 `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\nas100_1h.csv` 提供主线字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\nas100_h1_tmgm_longwin_20260702T0332\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\nas100_h1_tmgm_longwin_20260702T0332\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / NAS100 / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment nas100 h1 ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 `run_summary` 可追溯 source 与 `1` 条 repo-only backup log

- 文件：`artifacts\xbreaking\validation_matrix\nas100_h4_tmgm_longwin_20260702T0346\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\nas100_h4_tmgm_longwin_20260702T0346\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / NAS100 / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment nas100 h4 hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 NAS100/H4 跨月长窗口复跑，证明跨环境结论已从股指 H1 继续扩展到同品种 H4 样本，并为 `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\nas100_1h.csv` 提供更稳的主线字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\nas100_h4_tmgm_longwin_20260702T0346\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\nas100_h4_tmgm_longwin_20260702T0346\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / NAS100 / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment nas100 h4 ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 `run_summary` 可追溯 source 与 `1` 条 repo-only backup log

- 文件：`artifacts\xbreaking\validation_matrix\usoil_h1_tmgm_longwin_20260702T0400\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\usoil_h1_tmgm_longwin_20260702T0400\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / USOIL / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`commodity alias failure evidence`
  - 备注：本次仅形成 runtime/log 证据，未形成新 `csv/report`；TMGM 第二环境 tester 日志明确显示 `symbol USOIL not exist`，当前应将原油商品主线 symbol 切换到 `XTIUSD`

- 文件：`artifacts\xbreaking\validation_matrix\usoil_h1_tmgm_longwin_20260702T0400\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\usoil_h1_tmgm_longwin_20260702T0400\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / USOIL / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`commodity alias failure provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前 manifest 仅记录 runtime/log 等失败运行证据，不应视为有效商品硬样本

- 文件：`artifacts\xbreaking\validation_matrix\xtiusd_h1_tmgm_longwin_20260702T0406\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\xtiusd_h1_tmgm_longwin_20260702T0406\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / XTIUSD / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment oil alias h1 hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 XTIUSD/H1 跨月长窗口复跑，作为 TMGM 环境下原油商品的可用 broker symbol，并为 `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\usoil_1h.csv` 与 `xtiusd_1h.csv` 提供字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\xtiusd_h1_tmgm_longwin_20260702T0406\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\xtiusd_h1_tmgm_longwin_20260702T0406\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / XTIUSD / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment oil alias h1 ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 source-backed 运行产物与 `1` 条 repo-only backup log

- 文件：`artifacts\xbreaking\validation_matrix\xtiusd_h4_tmgm_longwin_20260702T0418\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\xtiusd_h4_tmgm_longwin_20260702T0418\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / XTIUSD / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment oil alias h4 hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `XTIUSD/H4` 跨月长窗口复跑，证明原油商品 broker alias 结论已从 `H1` 扩展到 `H4`；该样本曾作为 `recommended_cross_environment_seed_archive_tag`

- 文件：`artifacts\xbreaking\validation_matrix\xtiusd_h4_tmgm_longwin_20260702T0418\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\xtiusd_h4_tmgm_longwin_20260702T0418\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / XTIUSD / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment oil alias h4 ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕；当前记录显示 `5` 条 source-backed 运行产物与 `1` 条 repo-only backup log，属于 `mixed_provenance`

- 文件：`artifacts\purchased_csv_contract_preview\p1_contract_preview_20260702T0428\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`normalize_purchased_csv_contract_v1.py`
  - repo_path：`artifacts\purchased_csv_contract_preview\p1_contract_preview_20260702T0428\run_summary.json`
  - producer：`normalize_purchased_csv_contract_v1.py`
  - scope：`legacy purchased csv preview contract / xauusd_1h + nas100_1h + usoil_1h`
  - evidence_mode：`historical_recovered`
  - status：`written`
  - current_role：`已购 CSV 标准化预览索引`
  - 备注：当前首份预览归档已写出 `3` 个样本；`xauusd_1h.csv` 为 `60969` 行、`nas100_1h.csv` 为 `68961` 行、`usoil_1h.csv` 为 `13933` 行，且原油样本已按 broker alias 归一到 `symbol = XTIUSD`

- 文件：`artifacts\purchased_csv_contract_preview\p1_contract_preview_20260702T0428\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`normalize_purchased_csv_contract_v1.py`
  - repo_path：`artifacts\purchased_csv_contract_preview\p1_contract_preview_20260702T0428\ingest_manifest.json`
  - producer：`normalize_purchased_csv_contract_v1.py`
  - scope：`legacy purchased csv preview contract provenance`
  - evidence_mode：`historical_recovered`
  - status：`written`
  - current_role：`已购 CSV 标准化溯源留痕`
  - 备注：当前 manifest 已把 `xauusd_1h.csv / nas100_1h.csv / usoil_1h.csv` 与对应 normalized 输出一一绑定，明确标记为 `normalized from legacy purchased csv into preview contract`

- 文件：`artifacts\purchased_csv_contract_preview\p1_contract_preview_20260702T0702\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`normalize_purchased_csv_contract_v1.py`
  - repo_path：`artifacts\purchased_csv_contract_preview\p1_contract_preview_20260702T0702\run_summary.json`
  - producer：`normalize_purchased_csv_contract_v1.py`
  - scope：`legacy purchased csv preview contract / p1 expanded`
  - evidence_mode：`historical_recovered`
  - status：`written`
  - current_role：`已购 CSV 标准化预览索引（扩容）`
  - 备注：当前扩容预览归档已写出 `10` 个样本（`eurusd_1h / gbpusd_1h / usdjpy_1h / xauusd_1h / xagusd_1h / _xau_test_1h / US30_1h / nas100_1h / usoil_1h / xtiusd_1h`）；其中 `usoil_1h.csv` 仍按 broker alias 归一到 `symbol = XTIUSD`

- 文件：`artifacts\purchased_csv_contract_preview\p1_contract_preview_20260702T0702\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`normalize_purchased_csv_contract_v1.py`
  - repo_path：`artifacts\purchased_csv_contract_preview\p1_contract_preview_20260702T0702\ingest_manifest.json`
  - producer：`normalize_purchased_csv_contract_v1.py`
  - scope：`legacy purchased csv preview contract provenance / p1 expanded`
  - evidence_mode：`historical_recovered`
  - status：`written`
  - current_role：`已购 CSV 标准化溯源留痕（扩容）`
  - 备注：当前 manifest 已把 `10` 个源 `csv` 与对应 normalized 输出一一绑定，明确标记为 `normalized from legacy purchased csv into preview contract`

- 文件：`artifacts\purchased_csv_contract_preview\p1_contract_preview_20260702T1730\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`normalize_purchased_csv_contract_v1.py`
  - repo_path：`artifacts\purchased_csv_contract_preview\p1_contract_preview_20260702T1730\run_summary.json`
  - producer：`normalize_purchased_csv_contract_v1.py`
  - scope：`legacy purchased csv preview contract / p1_core preset`
  - evidence_mode：`historical_recovered`
  - status：`written`
  - current_role：`已购 CSV 标准化预览索引（预设入口）`
  - 备注：当前归档由 `--preset p1_core` 直接生成 `10` 个 P1 核心样本；其中 `_xau_test_1h.csv` 已显式归一到 `symbol = XAUUSD`，避免旧文件名被误判为 `_XAU_TEST`

- 文件：`artifacts\purchased_csv_contract_preview\p1_contract_preview_20260702T1730\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`normalize_purchased_csv_contract_v1.py`
  - repo_path：`artifacts\purchased_csv_contract_preview\p1_contract_preview_20260702T1730\ingest_manifest.json`
  - producer：`normalize_purchased_csv_contract_v1.py`
  - scope：`legacy purchased csv preview contract provenance / p1_core preset`
  - evidence_mode：`historical_recovered`
  - status：`written`
  - current_role：`已购 CSV 标准化溯源留痕（预设入口）`
  - 备注：当前 manifest 已把 `p1_core` 预设展开的 `10` 个源 `csv` 与 normalized 输出逐条绑定，属于可重复调用的批量标准化入口

- 文件：`artifacts\purchased_csv_contract_preview\p2_contract_preview_20260703T1115\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`normalize_purchased_csv_contract_v1.py`
  - repo_path：`artifacts\purchased_csv_contract_preview\p2_contract_preview_20260703T1115\run_summary.json`
  - producer：`normalize_purchased_csv_contract_v1.py`
  - scope：`legacy purchased csv preview contract / p2_ohlc_all preset`
  - evidence_mode：`historical_recovered`
  - status：`written`
  - current_role：`已购 CSV 标准化预览索引（P2 批量入口）`
  - 备注：当前归档由 `--preset p2_ohlc_all` 直接生成 `23` 个 P2 OHLC 样本，并且在标准化层完成 broker alias 对齐：`UKOIL_1h.csv -> XBRUSD`、`dollaridxusd_1h.csv -> USIDX`、`GER30_1h.csv -> GER40`

- 文件：`artifacts\purchased_csv_contract_preview\p2_contract_preview_20260703T1115\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`normalize_purchased_csv_contract_v1.py`
  - repo_path：`artifacts\purchased_csv_contract_preview\p2_contract_preview_20260703T1115\ingest_manifest.json`
  - producer：`normalize_purchased_csv_contract_v1.py`
  - scope：`legacy purchased csv preview contract provenance / p2_ohlc_all preset`
  - evidence_mode：`historical_recovered`
  - status：`written`
  - current_role：`已购 CSV 标准化溯源留痕（P2 批量入口）`
  - 备注：当前 manifest 已把 `23` 个源 `csv` 与 normalized 输出逐条绑定，统一标记为 `historical_recovered`

- 文件：`artifacts\purchased_csv_contract_preview\purchased_csv_contract_preview_index_latest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`purchased_csv_contract_preview_index_v1.py`
  - repo_path：`artifacts\purchased_csv_contract_preview\purchased_csv_contract_preview_index_latest.json`
  - producer：`purchased_csv_contract_preview_index_v1.py`
  - scope：`purchased_csv_contract_preview archive index / latest pointer`
  - evidence_mode：`index_refresh`
  - status：`written`
  - current_role：`已购 CSV 标准化预览索引（latest）`
  - 备注：当前索引已汇总 `4` 份 contract preview 归档，并将 latest 切到 `p2_contract_preview_20260703T1115`

- 文件：`acceptance_snapshots\purchased_csv_contract_preview_acceptance_latest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`purchased_csv_contract_preview_acceptance_v1.py`
  - repo_path：`acceptance_snapshots\purchased_csv_contract_preview_acceptance_latest.json`
  - producer：`purchased_csv_contract_preview_acceptance_v1.py`
  - scope：`purchased_csv_contract_preview archive acceptance / latest snapshot`
  - evidence_mode：`acceptance_refresh`
  - status：`written`
  - current_role：`已购 CSV 标准化预览验收快照`
  - 备注：当前验收已对 `purchased_csv_contract_preview` 下所有归档完成结构检查，`next_actions=[]`

- 文件：`artifacts\xbreaking\validation_matrix\ukoil_h1_tmgm_longwin_20260702T1918\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\ukoil_h1_tmgm_longwin_20260702T1918\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / UKOIL / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`oil alias failure evidence`
  - 备注：当前第二环境实跑只生成 `terminal/tester log + runtime_config`，未生成新的 `csv/report`；tester journal 已明确记录 `symbol UKOIL not exist`，因此该 symbol 在 TMGM broker 下不能直接作为商品主线

- 文件：`artifacts\xbreaking\validation_matrix\ukoil_h1_tmgm_longwin_20260702T1918\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\ukoil_h1_tmgm_longwin_20260702T1918\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / UKOIL / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`oil alias failure ingest provenance`
  - 备注：当前 manifest 只包含 `log + runtime_config` 共 `4` 条记录，其中 `3` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\us500_h1_tmgm_longwin_20260702T1925\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\us500_h1_tmgm_longwin_20260702T1925\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / US500 / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment index hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `US500/H1` 跨月长窗口复跑，为旧仓 `us500_1h.csv` 提供直接对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\us500_h1_tmgm_longwin_20260702T1925\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\us500_h1_tmgm_longwin_20260702T1925\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / US500 / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment index h1 ingest provenance`
  - 备注：当前 manifest 包含 `csv / report / log / runtime_config` 共 `6` 条记录，其中 `5` 条为 source-backed fresh-run 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\us500_h4_tmgm_longwin_20260702T1926\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\us500_h4_tmgm_longwin_20260702T1926\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / US500 / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment index hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `US500/H4` 跨月长窗口复跑；该样本曾作为 `recommended_cross_environment_seed_archive_tag`

- 文件：`artifacts\xbreaking\validation_matrix\us500_h4_tmgm_longwin_20260702T1926\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\us500_h4_tmgm_longwin_20260702T1926\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / US500 / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment index h4 ingest provenance`
  - 备注：当前 manifest 包含 `csv / report / log / runtime_config` 共 `6` 条记录，其中 `5` 条为 source-backed fresh-run 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\ger40_h1_tmgm_longwin_20260702T1932\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\ger40_h1_tmgm_longwin_20260702T1932\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / GER40 / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment index hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `GER40/H1` 跨月长窗口复跑，为旧仓 `ger40_1h.csv` 提供直接对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\ger40_h1_tmgm_longwin_20260702T1932\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\ger40_h1_tmgm_longwin_20260702T1932\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / GER40 / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment index h1 ingest provenance`
  - 备注：当前 manifest 包含 `csv / report / log / runtime_config` 共 `6` 条记录，其中 `5` 条为 source-backed fresh-run 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\ger40_h4_tmgm_longwin_20260702T1933\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\ger40_h4_tmgm_longwin_20260702T1933\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / GER40 / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment index hard evidence`
  - 备注：当前已在第二套 MT5 环境 `TradeMaxGlobal-Demo__60088394` 下完成 `GER40/H4` 跨月长窗口复跑，并成为当前 `recommended_cross_environment_seed_archive_tag`

- 文件：`artifacts\xbreaking\validation_matrix\ger40_h4_tmgm_longwin_20260702T1933\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\ger40_h4_tmgm_longwin_20260702T1933\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / GER40 / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`cross_environment index h4 ingest provenance`
  - 备注：当前 manifest 包含 `csv / report / log / runtime_config` 共 `6` 条记录，其中 `5` 条为 source-backed fresh-run 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\ger30_h1_tmgm_longwin_20260702T1942\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\ger30_h1_tmgm_longwin_20260702T1942\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / GER30 / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`index alias failure evidence`
  - 备注：当前第二环境实跑只生成 `terminal/tester log + runtime_config`，未生成新的 `csv/report`；tester journal 已明确记录 `symbol GER30 not exist`，因此旧仓 `GER30_1h.csv` 不能继续直接映射为 `GER30` tester symbol

- 文件：`artifacts\xbreaking\validation_matrix\ger30_h1_tmgm_longwin_20260702T1942\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\ger30_h1_tmgm_longwin_20260702T1942\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / GER30 / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`index alias failure ingest provenance`
  - 备注：当前 manifest 只包含 `log + runtime_config` 共 `4` 条记录，其中 `3` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\xcuusd_h1_tmgm_longwin_20260702T1950\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\xcuusd_h1_tmgm_longwin_20260702T1950\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / XCUUSD / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`commodity alias failure evidence`
  - 备注：当前第二环境实跑只生成 `terminal/tester log + runtime_config`，未生成新的 `csv/report`；tester journal 已明确记录 `symbol XCUUSD not exist`，因此旧仓 `XCUUSD_1h.csv` 不能继续直接映射为 `XCUUSD` tester symbol

- 文件：`artifacts\xbreaking\validation_matrix\xcuusd_h1_tmgm_longwin_20260702T1950\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\xcuusd_h1_tmgm_longwin_20260702T1950\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / XCUUSD / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`commodity alias failure ingest provenance`
  - 备注：当前 manifest 只包含 `log + runtime_config` 共 `4` 条记录，其中 `3` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\dollaridxusd_h1_tmgm_longwin_20260702T1959\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\dollaridxusd_h1_tmgm_longwin_20260702T1959\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / DOLLARIDXUSD / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`macro alias failure evidence`
  - 备注：当前第二环境实跑只生成 `terminal/tester log + runtime_config`，未生成新的 `csv/report`；tester journal 已明确记录 `symbol DOLLARIDXUSD not exist`，因此旧仓 `dollaridxusd_1h.csv` 不能继续直接映射为 `DOLLARIDXUSD` tester symbol

- 文件：`artifacts\xbreaking\validation_matrix\dollaridxusd_h1_tmgm_longwin_20260702T1959\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\dollaridxusd_h1_tmgm_longwin_20260702T1959\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / DOLLARIDXUSD / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`macro alias failure ingest provenance`
  - 备注：当前 manifest 只包含 `log + runtime_config` 共 `4` 条记录，其中 `3` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\audusd_h1_tmgm_longwin_20260702T2022\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\audusd_h1_tmgm_longwin_20260702T2022\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / AUDUSD / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，为旧仓 `audusd_1h.csv` 提供新的主线字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\audusd_h1_tmgm_longwin_20260702T2022\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\audusd_h1_tmgm_longwin_20260702T2022\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / AUDUSD / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\audusd_h4_tmgm_longwin_20260702T2024\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\audusd_h4_tmgm_longwin_20260702T2024\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / AUDUSD / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，并因完整性与溯源质量上升而接替为当前 `recommended_cross_environment_seed`

- 文件：`artifacts\xbreaking\validation_matrix\audusd_h4_tmgm_longwin_20260702T2024\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\audusd_h4_tmgm_longwin_20260702T2024\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / AUDUSD / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\usdchf_h1_tmgm_longwin_20260702T2034\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdchf_h1_tmgm_longwin_20260702T2034\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / USDCHF / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，为旧仓 `usdchf_1h.csv` 提供新的主线字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\usdchf_h1_tmgm_longwin_20260702T2034\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdchf_h1_tmgm_longwin_20260702T2034\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / USDCHF / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\usdchf_h4_tmgm_longwin_20260702T2035\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdchf_h4_tmgm_longwin_20260702T2035\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / USDCHF / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，并因完整性与溯源质量上升而接替为当前 `recommended_cross_environment_seed`

- 文件：`artifacts\xbreaking\validation_matrix\usdchf_h4_tmgm_longwin_20260702T2035\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdchf_h4_tmgm_longwin_20260702T2035\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / USDCHF / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\usdcad_h1_tmgm_longwin_20260702T2110\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdcad_h1_tmgm_longwin_20260702T2110\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / USDCAD / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，为旧仓 `usdcad_1h.csv` 提供新的主线字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\usdcad_h1_tmgm_longwin_20260702T2110\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdcad_h1_tmgm_longwin_20260702T2110\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / USDCAD / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\usdcad_h4_tmgm_longwin_20260702T2111\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdcad_h4_tmgm_longwin_20260702T2111\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / USDCAD / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，并因完整性与溯源质量上升而接替为当前 `recommended_cross_environment_seed`

- 文件：`artifacts\xbreaking\validation_matrix\usdcad_h4_tmgm_longwin_20260702T2111\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdcad_h4_tmgm_longwin_20260702T2111\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / USDCAD / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\nzdusd_h1_tmgm_longwin_20260702T2128\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\nzdusd_h1_tmgm_longwin_20260702T2128\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / NZDUSD / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，为旧仓 `nzdusd_1h.csv` 提供新的主线字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\nzdusd_h1_tmgm_longwin_20260702T2128\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\nzdusd_h1_tmgm_longwin_20260702T2128\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / NZDUSD / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\nzdusd_h4_tmgm_longwin_20260702T2129\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\nzdusd_h4_tmgm_longwin_20260702T2129\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / NZDUSD / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，并因完整性与溯源质量上升而接替为当前 `recommended_cross_environment_seed`

- 文件：`artifacts\xbreaking\validation_matrix\nzdusd_h4_tmgm_longwin_20260702T2129\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\nzdusd_h4_tmgm_longwin_20260702T2129\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / NZDUSD / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\eurjpy_h1_tmgm_longwin_20260702T2144\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurjpy_h1_tmgm_longwin_20260702T2144\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURJPY / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，为旧仓 `eurjpy_1h.csv` 提供新的主线字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\eurjpy_h1_tmgm_longwin_20260702T2144\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurjpy_h1_tmgm_longwin_20260702T2144\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / EURJPY / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\eurjpy_h4_tmgm_longwin_20260702T2145\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurjpy_h4_tmgm_longwin_20260702T2145\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURJPY / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，并因完整性与溯源质量上升而接替为当前 `recommended_cross_environment_seed`

- 文件：`artifacts\xbreaking\validation_matrix\eurjpy_h4_tmgm_longwin_20260702T2145\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurjpy_h4_tmgm_longwin_20260702T2145\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / EURJPY / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\gbpjpy_h1_tmgm_longwin_20260702T2203\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbpjpy_h1_tmgm_longwin_20260702T2203\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / GBPJPY / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，为旧仓 `gbpjpy_1h.csv` 提供新的主线字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\gbpjpy_h1_tmgm_longwin_20260702T2203\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbpjpy_h1_tmgm_longwin_20260702T2203\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / GBPJPY / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\gbpjpy_h4_tmgm_longwin_20260702T2204\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbpjpy_h4_tmgm_longwin_20260702T2204\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / GBPJPY / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，并因完整性与溯源质量上升而接替为当前 `recommended_cross_environment_seed`

- 文件：`artifacts\xbreaking\validation_matrix\gbpjpy_h4_tmgm_longwin_20260702T2204\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbpjpy_h4_tmgm_longwin_20260702T2204\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / GBPJPY / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\eurgbp_h1_tmgm_longwin_20260702T2220\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurgbp_h1_tmgm_longwin_20260702T2220\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURGBP / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，为旧仓 `EURGBP_1h.csv` 提供新的主线字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\eurgbp_h1_tmgm_longwin_20260702T2220\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurgbp_h1_tmgm_longwin_20260702T2220\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / EURGBP / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\eurgbp_h4_tmgm_longwin_20260702T2221\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurgbp_h4_tmgm_longwin_20260702T2221\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURGBP / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，并因完整性与溯源质量上升而接替为当前 `recommended_cross_environment_seed`

- 文件：`artifacts\xbreaking\validation_matrix\eurgbp_h4_tmgm_longwin_20260702T2221\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurgbp_h4_tmgm_longwin_20260702T2221\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / EURGBP / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\chfjpy_h1_tmgm_longwin_20260702T2233\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\chfjpy_h1_tmgm_longwin_20260702T2233\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / CHFJPY / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，为旧仓 `CHFJPY_1h.csv` 提供新的主线字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\chfjpy_h1_tmgm_longwin_20260702T2233\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\chfjpy_h1_tmgm_longwin_20260702T2233\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / CHFJPY / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\chfjpy_h4_tmgm_longwin_20260702T2234\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\chfjpy_h4_tmgm_longwin_20260702T2234\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / CHFJPY / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，并因完整性与溯源质量上升而接替为当前 `recommended_cross_environment_seed`

- 文件：`artifacts\xbreaking\validation_matrix\chfjpy_h4_tmgm_longwin_20260702T2234\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\chfjpy_h4_tmgm_longwin_20260702T2234\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / CHFJPY / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\eurchf_h1_tmgm_longwin_20260702T2247\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurchf_h1_tmgm_longwin_20260702T2247\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURCHF / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，为旧仓 `EURCHF_1h.csv` 提供新的主线字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\eurchf_h1_tmgm_longwin_20260702T2247\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurchf_h1_tmgm_longwin_20260702T2247\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / EURCHF / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\eurchf_h4_tmgm_longwin_20260702T2248\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurchf_h4_tmgm_longwin_20260702T2248\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURCHF / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，并因完整性与溯源质量上升而接替为当前 `recommended_cross_environment_seed`

- 文件：`artifacts\xbreaking\validation_matrix\eurchf_h4_tmgm_longwin_20260702T2248\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurchf_h4_tmgm_longwin_20260702T2248\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / EURCHF / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\audnzd_h1_tmgm_longwin_20260702T2310\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\audnzd_h1_tmgm_longwin_20260702T2310\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / AUDNZD / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，为旧仓 `AUDNZD_1h.csv` 提供新的主线字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\audnzd_h1_tmgm_longwin_20260702T2310\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\audnzd_h1_tmgm_longwin_20260702T2310\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / AUDNZD / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\audnzd_h4_tmgm_longwin_20260702T2311\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\audnzd_h4_tmgm_longwin_20260702T2311\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / AUDNZD / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，并因完整性与溯源质量上升而接替为当前 `recommended_cross_environment_seed`

- 文件：`artifacts\xbreaking\validation_matrix\audnzd_h4_tmgm_longwin_20260702T2311\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\audnzd_h4_tmgm_longwin_20260702T2311\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / AUDNZD / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\cadjpy_h1_tmgm_longwin_20260702T2331\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\cadjpy_h1_tmgm_longwin_20260702T2331\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / CADJPY / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，为旧仓 `CADJPY_1h.csv` 提供新的主线字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\cadjpy_h1_tmgm_longwin_20260702T2331\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\cadjpy_h1_tmgm_longwin_20260702T2331\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / CADJPY / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\cadjpy_h4_tmgm_longwin_20260702T2332\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\cadjpy_h4_tmgm_longwin_20260702T2332\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / CADJPY / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，并因完整性与溯源质量上升而接替为当前 `recommended_cross_environment_seed`

- 文件：`artifacts\xbreaking\validation_matrix\cadjpy_h4_tmgm_longwin_20260702T2332\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\cadjpy_h4_tmgm_longwin_20260702T2332\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / CADJPY / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\euraud_h1_tmgm_longwin_20260702T2353\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\euraud_h1_tmgm_longwin_20260702T2353\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURAUD / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，为旧仓 `EURAUD_1h.csv` 提供新的主线字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\euraud_h1_tmgm_longwin_20260702T2353\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\euraud_h1_tmgm_longwin_20260702T2353\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / EURAUD / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\euraud_h4_tmgm_longwin_20260702T2354\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\euraud_h4_tmgm_longwin_20260702T2354\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURAUD / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，并因完整性与溯源质量上升而接替为当前 `recommended_cross_environment_seed`

- 文件：`artifacts\xbreaking\validation_matrix\euraud_h4_tmgm_longwin_20260702T2354\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\euraud_h4_tmgm_longwin_20260702T2354\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / EURAUD / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\gbpchf_h1_tmgm_longwin_20260703T0007\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbpchf_h1_tmgm_longwin_20260703T0007\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / GBPCHF / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，为旧仓 `GBPCHF_1h.csv` 提供新的主线字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\gbpchf_h1_tmgm_longwin_20260703T0007\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbpchf_h1_tmgm_longwin_20260703T0007\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / GBPCHF / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\gbpchf_h4_tmgm_longwin_20260703T0008\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbpchf_h4_tmgm_longwin_20260703T0008\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / GBPCHF / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，并因完整性与溯源质量上升而接替为当前 `recommended_cross_environment_seed`

- 文件：`artifacts\xbreaking\validation_matrix\gbpchf_h4_tmgm_longwin_20260703T0008\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbpchf_h4_tmgm_longwin_20260703T0008\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / GBPCHF / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\eurnzd_h1_tmgm_longwin_20260703T0027\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurnzd_h1_tmgm_longwin_20260703T0027\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURNZD / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，为旧仓 `EURNZD_1h.csv` 提供新的主线字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\eurnzd_h1_tmgm_longwin_20260703T0027\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurnzd_h1_tmgm_longwin_20260703T0027\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / EURNZD / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\eurnzd_h4_tmgm_longwin_20260703T0028\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurnzd_h4_tmgm_longwin_20260703T0028\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURNZD / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，并因完整性与溯源质量上升而接替为当前 `recommended_cross_environment_seed`

- 文件：`artifacts\xbreaking\validation_matrix\eurnzd_h4_tmgm_longwin_20260703T0028\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurnzd_h4_tmgm_longwin_20260703T0028\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / EURNZD / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\audjpy_h1_tmgm_longwin_20260703T0038\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\audjpy_h1_tmgm_longwin_20260703T0038\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / AUDJPY / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，为旧仓 `AUDJPY_1h.csv` 提供新的主线字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\audjpy_h1_tmgm_longwin_20260703T0038\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\audjpy_h1_tmgm_longwin_20260703T0038\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / AUDJPY / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\audjpy_h4_tmgm_longwin_20260703T0039\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\audjpy_h4_tmgm_longwin_20260703T0039\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / AUDJPY / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，并因完整性与溯源质量上升而接替为当前 `recommended_cross_environment_seed`

- 文件：`artifacts\xbreaking\validation_matrix\audjpy_h4_tmgm_longwin_20260703T0039\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\audjpy_h4_tmgm_longwin_20260703T0039\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / AUDJPY / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\nzdjpy_h1_tmgm_longwin_20260703T0115\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\nzdjpy_h1_tmgm_longwin_20260703T0115\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / NZDJPY / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，为旧仓 `NZDJPY_1h.csv` 提供新的主线字段对照锚点

- 文件：`artifacts\xbreaking\validation_matrix\nzdjpy_h1_tmgm_longwin_20260703T0115\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\nzdjpy_h1_tmgm_longwin_20260703T0115\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / NZDJPY / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\nzdjpy_h4_tmgm_longwin_20260703T0116\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\nzdjpy_h4_tmgm_longwin_20260703T0116\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / NZDJPY / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，并因完整性与溯源质量上升而接替为当前 `recommended_cross_environment_seed`

- 文件：`artifacts\xbreaking\validation_matrix\nzdjpy_h4_tmgm_longwin_20260703T0116\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\nzdjpy_h4_tmgm_longwin_20260703T0116\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / NZDJPY / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\gbridxgbp_h1_tmgm_longwin_20260703T0125\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbridxgbp_h1_tmgm_longwin_20260703T0125\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / GBRIDXGBP / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`index alias failure evidence`
  - 备注：当前归档仅生成 `terminal log / tester log / runtime_config`，tester 日志已明确记录 `symbol GBRIDXGBP not exist` 与 `cannot select symbol in market watch`，因此该旧命名当前不能直接作为 TMGM tester symbol

- 文件：`artifacts\xbreaking\validation_matrix\gbridxgbp_h1_tmgm_longwin_20260703T0125\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbridxgbp_h1_tmgm_longwin_20260703T0125\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / GBRIDXGBP / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `4` 条记录，其中 `3` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；由于未产出 `csv / report`，本归档当前仅作为 alias failure evidence 与后续 broker alias 探测入口

- 文件：`artifacts\xbreaking\validation_matrix\xbrusd_h1_tmgm_longwin_20260703T0159\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\xbrusd_h1_tmgm_longwin_20260703T0159\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / XBRUSD / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，用于把旧仓 `UKOIL_1h.csv` 从旧命名失败证据推进到 `XBRUSD` Brent alias 对照链

- 文件：`artifacts\xbreaking\validation_matrix\xbrusd_h1_tmgm_longwin_20260703T0159\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\xbrusd_h1_tmgm_longwin_20260703T0159\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / XBRUSD / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\xbrusd_h4_tmgm_longwin_20260703T0200\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\xbrusd_h4_tmgm_longwin_20260703T0200\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / XBRUSD / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，并因完整性与 Brent alias 代表性提升而接替为当前 `recommended_cross_environment_seed`

- 文件：`artifacts\xbreaking\validation_matrix\xbrusd_h4_tmgm_longwin_20260703T0200\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\xbrusd_h4_tmgm_longwin_20260703T0200\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / XBRUSD / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\coppercmdusd_h1_tmgm_longwin_20260703T0216\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\coppercmdusd_h1_tmgm_longwin_20260703T0216\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / COPPERCMDUSD / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`candidate alias failure evidence`
  - 备注：当前归档仅生成 `terminal log / tester log / runtime_config`；原始 MT5 日志已明确记录 `symbol COPPERCMDUSD not exist`，因此该候选 alias 当前不能用于把旧仓 `XCUUSD_1h.csv` 收敛到 TMGM tester 主线

- 文件：`artifacts\xbreaking\validation_matrix\coppercmdusd_h1_tmgm_longwin_20260703T0216\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\coppercmdusd_h1_tmgm_longwin_20260703T0216\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / COPPERCMDUSD / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `4` 条记录，其中 `3` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；由于未产出 `csv / report`，本归档当前仅作为 `XCUUSD` 候选 alias failure evidence

- 文件：`artifacts\xbreaking\validation_matrix\usdx_h1_tmgm_longwin_20260703T0222\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdx_h1_tmgm_longwin_20260703T0222\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / USDX / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`candidate alias failure evidence`
  - 备注：当前归档仅生成 `terminal log / tester log / runtime_config`；原始 MT5 日志已明确记录 `symbol USDX not exist`，因此该候选 alias 当前不能用于把旧仓 `dollaridxusd_1h.csv` 收敛到 TMGM tester 主线

- 文件：`artifacts\xbreaking\validation_matrix\usdx_h1_tmgm_longwin_20260703T0222\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdx_h1_tmgm_longwin_20260703T0222\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / USDX / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `4` 条记录，其中 `3` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；由于未产出 `csv / report`，本归档当前仅作为 `DOLLARIDXUSD` 候选 alias failure evidence

- 文件：`artifacts\xbreaking\validation_matrix\dxy_h1_tmgm_longwin_20260703T0226\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\dxy_h1_tmgm_longwin_20260703T0226\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / DXY / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`candidate alias failure evidence`
  - 备注：当前归档仅生成 `terminal log / tester log / runtime_config`；原始 MT5 日志已明确记录 `symbol DXY not exist`，因此该候选 alias 当前也不能用于把旧仓 `dollaridxusd_1h.csv` 收敛到 TMGM tester 主线

- 文件：`artifacts\xbreaking\validation_matrix\dxy_h1_tmgm_longwin_20260703T0226\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\dxy_h1_tmgm_longwin_20260703T0226\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / DXY / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `4` 条记录，其中 `3` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；由于未产出 `csv / report`，本归档当前仅作为 `DOLLARIDXUSD` 候选 alias failure evidence

- 文件：`artifacts\xbreaking\validation_matrix\usidx_h1_tmgm_longwin_20260703T0247\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\usidx_h1_tmgm_longwin_20260703T0247\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / USIDX / H1 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，用于把旧仓 `dollaridxusd_1h.csv` 从旧命名失败与候选 alias 失败证据推进到 `USIDX` 美元指数别名对照链

- 文件：`artifacts\xbreaking\validation_matrix\usidx_h1_tmgm_longwin_20260703T0247\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\usidx_h1_tmgm_longwin_20260703T0247\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / USIDX / H1 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\usidx_h4_tmgm_longwin_20260703T0248\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\usidx_h4_tmgm_longwin_20260703T0248\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / USIDX / H4 / inventory_selector / window=2024.12.01-2025.03.01 / environment=TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`cross_environment hard evidence`
  - 备注：当前第二环境实跑已完整生成 `csv / report / terminal log / tester log / runtime_config`，并因完整性与美元指数 alias 代表性提升而接替为当前 `recommended_cross_environment_seed`

- 文件：`artifacts\xbreaking\validation_matrix\usidx_h4_tmgm_longwin_20260703T0248\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\usidx_h4_tmgm_longwin_20260703T0248\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / USIDX / H4 / TradeMaxGlobal-Demo__60088394`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：当前 manifest 共 `6` 条记录，其中 `5` 条为 `fresh_run_index` source-backed 记录、`1` 条为 repo 内 backup log；属于 `mixed_provenance`

- 文件：`artifacts\xbreaking\validation_matrix\gbpusd_h4_envselect_hard_20260701T1535\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbpusd_h4_envselect_hard_20260701T1535\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / GBPUSD / H4 / inventory_selector`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`selection_mode hard evidence`
  - 备注：`environment_selection_mode=inventory_selector`，且 `environment_inventory_*` 字段齐全，归档已包含 `csv / report / terminal log / tester log`

- 文件：`artifacts\xbreaking\validation_matrix\gbpusd_h4_envselect_hard_20260701T1535\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbpusd_h4_envselect_hard_20260701T1535\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / GBPUSD / H4`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕（不伪装原始 source），并记录 repo 内归档文件清单

- 文件：`artifacts\xbreaking\validation_matrix\gbpusd_h4_override_hard_20260701T1535\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbpusd_h4_override_hard_20260701T1535\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / GBPUSD / H4 / data_root_override`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`selection_mode hard evidence`
  - 备注：`environment_selection_mode=data_root_override`，归档已包含 `csv / report / terminal log / tester log`

- 文件：`artifacts\xbreaking\validation_matrix\gbpusd_h4_override_hard_20260701T1535\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbpusd_h4_override_hard_20260701T1535\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / GBPUSD / H4`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕（不伪装原始 source），并记录 repo 内归档文件清单

- 文件：`artifacts\xbreaking\validation_matrix\usdjpy_h1_envselect_hard_20260701T1608\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdjpy_h1_envselect_hard_20260701T1608\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / USDJPY / H1 / inventory_selector`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`selection_mode hard evidence`
  - 备注：`environment_selection_mode=inventory_selector`，且 `environment_inventory_*` 字段齐全，归档已包含 `csv / report / terminal log / tester log`

- 文件：`artifacts\xbreaking\validation_matrix\usdjpy_h1_envselect_hard_20260701T1608\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdjpy_h1_envselect_hard_20260701T1608\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / USDJPY / H1`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕（不伪装原始 source），并记录 repo 内归档文件清单

- 文件：`artifacts\xbreaking\validation_matrix\usdjpy_h1_override_hard_20260701T1608\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdjpy_h1_override_hard_20260701T1608\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / USDJPY / H1 / data_root_override`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`selection_mode hard evidence`
  - 备注：`environment_selection_mode=data_root_override`，归档已包含 `csv / report / terminal log / tester log`

- 文件：`artifacts\xbreaking\validation_matrix\usdjpy_h1_override_hard_20260701T1608\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdjpy_h1_override_hard_20260701T1608\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / USDJPY / H1`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕（不伪装原始 source），并记录 repo 内归档文件清单

- 文件：`artifacts\xbreaking\validation_matrix\usdjpy_h1_envselect_feb_20260701T1625\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdjpy_h1_envselect_feb_20260701T1625\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / USDJPY / H1 / inventory_selector / window=2025.02.03-2025.02.10`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`date_window robustness evidence`
  - 备注：在更远日期窗下复跑，`selection_mode=inventory_selector` 字段齐全，归档已包含 `csv / report / terminal log / tester log`

- 文件：`artifacts\xbreaking\validation_matrix\usdjpy_h1_envselect_feb_20260701T1625\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdjpy_h1_envselect_feb_20260701T1625\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / USDJPY / H1`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`archive ingest provenance`
  - 备注：由 `--backfill-ingest-manifest-from-archive` 补齐回收留痕（不伪装原始 source），并记录 repo 内归档文件清单

- 文件：`artifacts\xbreaking\validation_matrix\gbpusd_h4_20260701T\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbpusd_h4_20260701T\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / GBPUSD / H4 / IndicatorTf=H4`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`validation matrix run index`
  - 备注：绑定 `runtime_set_write_mode=written`、源 `csv / report / terminal log / tester log` 与归档路径

- 文件：`artifacts\xbreaking\validation_matrix\gbpusd_h4_20260701T\csv\XBreaking_probe_GBPUSD_H4_20250102_000000.csv`
  - 类型：`ARTIFACT`
  - source_path：`%APPDATA%\MetaQuotes\Terminal\Common\Files\XBreaking_probe_GBPUSD_H4_20250102_000000.csv`
  - repo_path：`artifacts\xbreaking\validation_matrix\gbpusd_h4_20260701T\csv\XBreaking_probe_GBPUSD_H4_20250102_000000.csv`
  - producer：`XBreakingProbe.mq5`
  - scope：`XBreaking / GBPUSD / H4`
  - evidence_mode：`fresh_run`
  - status：`recovered_and_verified`
  - current_role：`跨场景 buffer 语义复核硬证据`
  - 备注：当前已确认 `chart_tf=PERIOD_H4`、`indicator_tf=PERIOD_H4`、`status=DONE`，且访问形态仍为 `buffer0_only`

- 文件：`artifacts\xbreaking\validation_matrix\usdjpy_h4_20260701T\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdjpy_h4_20260701T\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / USDJPY / H4 / IndicatorTf=H4`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`validation matrix run index`
  - 备注：绑定 `runtime_set_write_mode=written`、源 `csv / report / terminal log / tester log` 与归档路径

- 文件：`artifacts\xbreaking\validation_matrix\usdjpy_h4_20260701T\csv\XBreaking_probe_USDJPY_H4_20250102_000000.csv`
  - 类型：`ARTIFACT`
  - source_path：`%APPDATA%\MetaQuotes\Terminal\Common\Files\XBreaking_probe_USDJPY_H4_20250102_000000.csv`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdjpy_h4_20260701T\csv\XBreaking_probe_USDJPY_H4_20250102_000000.csv`
  - producer：`XBreakingProbe.mq5`
  - scope：`XBreaking / USDJPY / H4`
  - evidence_mode：`fresh_run`
  - status：`recovered_and_verified`
  - current_role：`跨场景 buffer 语义复核硬证据`
  - 备注：当前已确认 `chart_tf=PERIOD_H4`、`indicator_tf=PERIOD_H4`、`status=DONE`，且访问形态仍为 `buffer0_only`

- 文件：`artifacts\xbreaking\validation_matrix\usdjpy_h1_20260701T\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdjpy_h1_20260701T\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / USDJPY / H1 / IndicatorTf=H1`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`validation matrix run index`
  - 备注：绑定 `runtime_set_write_mode=written`、源 `csv / report / terminal log / tester log` 与归档路径

- 文件：`artifacts\xbreaking\validation_matrix\usdjpy_h1_20260701T\csv\XBreaking_probe_USDJPY_H1_20250102_000000.csv`
  - 类型：`ARTIFACT`
  - source_path：`%APPDATA%\MetaQuotes\Terminal\Common\Files\XBreaking_probe_USDJPY_H1_20250102_000000.csv`
  - repo_path：`artifacts\xbreaking\validation_matrix\usdjpy_h1_20260701T\csv\XBreaking_probe_USDJPY_H1_20250102_000000.csv`
  - producer：`XBreakingProbe.mq5`
  - scope：`XBreaking / USDJPY / H1`
  - evidence_mode：`fresh_run`
  - status：`recovered_and_verified`
  - current_role：`跨场景 buffer 语义复核硬证据`
  - 备注：当前已确认 `chart_tf=PERIOD_H1`、`indicator_tf=PERIOD_H1`、`status=DONE`，且访问形态仍为 `buffer0_only`

- 文件：`artifacts\xbreaking\validation_matrix\xauusd_h4_20260701T\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\xauusd_h4_20260701T\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / XAUUSD / H4 / IndicatorTf=H4`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`validation matrix run index`
  - 备注：绑定 `runtime_set_write_mode=written`、源 `csv / report / terminal log / tester log` 与归档路径

- 文件：`artifacts\xbreaking\validation_matrix\xauusd_h4_20260701T\csv\XBreaking_probe_XAUUSD_H4_20250102_010000.csv`
  - 类型：`ARTIFACT`
  - source_path：`%APPDATA%\MetaQuotes\Terminal\Common\Files\XBreaking_probe_XAUUSD_H4_20250102_010000.csv`
  - repo_path：`artifacts\xbreaking\validation_matrix\xauusd_h4_20260701T\csv\XBreaking_probe_XAUUSD_H4_20250102_010000.csv`
  - producer：`XBreakingProbe.mq5`
  - scope：`XBreaking / XAUUSD / H4`
  - evidence_mode：`fresh_run`
  - status：`recovered_and_verified`
  - current_role：`异质品种 buffer 语义复核硬证据`
  - 备注：当前已确认 `chart_tf=PERIOD_H4`、`indicator_tf=PERIOD_H4`、`status=DONE`，且访问形态仍为 `buffer0_only`

- 文件：`artifacts\xbreaking\validation_matrix\us30_h4_20260701T\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\us30_h4_20260701T\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / US30 / H4 / IndicatorTf=H4`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`validation matrix run index`
  - 备注：绑定 `runtime_set_write_mode=written`、源 `csv / report / terminal log / tester log` 与归档路径

- 文件：`artifacts\xbreaking\validation_matrix\us30_h4_20260701T\csv\XBreaking_probe_US30_H4_20250102_010000.csv`
  - 类型：`ARTIFACT`
  - source_path：`%APPDATA%\MetaQuotes\Terminal\Common\Files\XBreaking_probe_US30_H4_20250102_010000.csv`
  - repo_path：`artifacts\xbreaking\validation_matrix\us30_h4_20260701T\csv\XBreaking_probe_US30_H4_20250102_010000.csv`
  - producer：`XBreakingProbe.mq5`
  - scope：`XBreaking / US30 / H4`
  - evidence_mode：`fresh_run`
  - status：`recovered_and_verified`
  - current_role：`异质品种 buffer 语义复核硬证据`
  - 备注：当前已确认 `chart_tf=PERIOD_H4`、`indicator_tf=PERIOD_H4`、`status=DONE`，且访问形态仍为 `buffer0_only`

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_jan0310_20260701T124339_window_a\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_validation_matrix.ps1 -> run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_jan0310_20260701T124339_window_a\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURUSD / H4 / 2025.01.03~2025.01.10`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`日期窗口稳定性 run index`
  - 备注：绑定 `WindowTag=jan03_10`、`runtime_set_write_mode=written` 与源 `csv / report / terminal log / tester log`

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_jan0310_20260701T124339_window_a\csv\XBreaking_probe_EURUSD_H4_20250103_000000.csv`
  - 类型：`ARTIFACT`
  - source_path：`%APPDATA%\MetaQuotes\Terminal\Common\Files\XBreaking_probe_EURUSD_H4_20250103_000000.csv`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_jan0310_20260701T124339_window_a\csv\XBreaking_probe_EURUSD_H4_20250103_000000.csv`
  - producer：`XBreakingProbe.mq5`
  - scope：`XBreaking / EURUSD / H4 / 2025.01.03~2025.01.10`
  - evidence_mode：`fresh_run`
  - status：`recovered_and_verified`
  - current_role：`日期窗口稳定性硬证据`
  - 备注：当前已确认 `chart_tf=PERIOD_H4`、`indicator_tf=PERIOD_H4`、`status=DONE`，且访问形态仍为 `buffer0_only`

- 文件：`artifacts\xbreaking\validation_matrix\xauusd_h4_jan0310_20260701T124339_window_a\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_validation_matrix.ps1 -> run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\xauusd_h4_jan0310_20260701T124339_window_a\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / XAUUSD / H4 / 2025.01.03~2025.01.10`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`日期窗口稳定性 run index`
  - 备注：绑定 `WindowTag=jan03_10`、`runtime_set_write_mode=written` 与源 `csv / report / terminal log / tester log`

- 文件：`artifacts\xbreaking\validation_matrix\xauusd_h4_jan0310_20260701T124339_window_a\csv\XBreaking_probe_XAUUSD_H4_20250103_010000.csv`
  - 类型：`ARTIFACT`
  - source_path：`%APPDATA%\MetaQuotes\Terminal\Common\Files\XBreaking_probe_XAUUSD_H4_20250103_010000.csv`
  - repo_path：`artifacts\xbreaking\validation_matrix\xauusd_h4_jan0310_20260701T124339_window_a\csv\XBreaking_probe_XAUUSD_H4_20250103_010000.csv`
  - producer：`XBreakingProbe.mq5`
  - scope：`XBreaking / XAUUSD / H4 / 2025.01.03~2025.01.10`
  - evidence_mode：`fresh_run`
  - status：`recovered_and_verified`
  - current_role：`日期窗口稳定性硬证据`
  - 备注：当前已确认 `chart_tf=PERIOD_H4`、`indicator_tf=PERIOD_H4`、`status=DONE`，且访问形态仍为 `buffer0_only`

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_jan0714_20260701T124459_window_b\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_validation_matrix.ps1 -> run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_jan0714_20260701T124459_window_b\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURUSD / H4 / 2025.01.07~2025.01.14`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`日期窗口稳定性 run index`
  - 备注：绑定 `WindowTag=jan07_14`、`runtime_set_write_mode=written` 与源 `csv / report / terminal log / tester log`

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_jan0714_20260701T124459_window_b\csv\XBreaking_probe_EURUSD_H4_20250107_000000.csv`
  - 类型：`ARTIFACT`
  - source_path：`%APPDATA%\MetaQuotes\Terminal\Common\Files\XBreaking_probe_EURUSD_H4_20250107_000000.csv`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_jan0714_20260701T124459_window_b\csv\XBreaking_probe_EURUSD_H4_20250107_000000.csv`
  - producer：`XBreakingProbe.mq5`
  - scope：`XBreaking / EURUSD / H4 / 2025.01.07~2025.01.14`
  - evidence_mode：`fresh_run`
  - status：`recovered_and_verified`
  - current_role：`日期窗口稳定性硬证据`
  - 备注：当前已确认 `chart_tf=PERIOD_H4`、`indicator_tf=PERIOD_H4`、`status=DONE`，且访问形态仍为 `buffer0_only`

- 文件：`artifacts\xbreaking\validation_matrix\xauusd_h4_jan0714_20260701T124459_window_b\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_validation_matrix.ps1 -> run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\xauusd_h4_jan0714_20260701T124459_window_b\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / XAUUSD / H4 / 2025.01.07~2025.01.14`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`日期窗口稳定性 run index`
  - 备注：绑定 `WindowTag=jan07_14`、`runtime_set_write_mode=written` 与源 `csv / report / terminal log / tester log`

- 文件：`artifacts\xbreaking\validation_matrix\xauusd_h4_jan0714_20260701T124459_window_b\csv\XBreaking_probe_XAUUSD_H4_20250107_010000.csv`
  - 类型：`ARTIFACT`
  - source_path：`%APPDATA%\MetaQuotes\Terminal\Common\Files\XBreaking_probe_XAUUSD_H4_20250107_010000.csv`
  - repo_path：`artifacts\xbreaking\validation_matrix\xauusd_h4_jan0714_20260701T124459_window_b\csv\XBreaking_probe_XAUUSD_H4_20250107_010000.csv`
  - producer：`XBreakingProbe.mq5`
  - scope：`XBreaking / XAUUSD / H4 / 2025.01.07~2025.01.14`
  - evidence_mode：`fresh_run`
  - status：`recovered_and_verified`
  - current_role：`日期窗口稳定性硬证据`
  - 备注：当前已确认 `chart_tf=PERIOD_H4`、`indicator_tf=PERIOD_H4`、`status=DONE`，且访问形态仍为 `buffer0_only`

- 文件：`environment_snapshots\mt_environment_inventory_latest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_mt_environment_inventory.ps1`
  - repo_path：`environment_snapshots\mt_environment_inventory_latest.json`
  - producer：`probe_mt_environment_inventory.ps1`
  - scope：`Local MetaQuotes runtime inventory`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`当前环境盘点快照`
  - 备注：当前确认 `1` 套 `MT4` 与 `2` 套 `MT5`；`MT5` 环境为 `ICMarketsSC-Demo / 52886989 / HK-Demo` 与 `TradeMaxGlobal-Demo / 60088394`，并已写出 `environment_label=ICMarketsSC-Demo__52886989` 与 `TradeMaxGlobal-Demo__60088394`

- 文件：`environment_snapshots\mt5_symbols_marketwatch__TradeMaxGlobal-Demo__60088394__20250101_000000__55.txt`
  - 类型：`ARTIFACT`
  - source_path：`%APPDATA%\\MetaQuotes\\Terminal\\Common\\Files\\mt5_symbols_marketwatch__TradeMaxGlobal-Demo__60088394__20250101_000000__55.txt`
  - repo_path：`environment_snapshots\mt5_symbols_marketwatch__TradeMaxGlobal-Demo__60088394__20250101_000000__55.txt`
  - producer：`MT5SymbolDumpProbe.ex5`
  - scope：`MT5 Symbols / TradeMaxGlobal-Demo__60088394 / MarketWatch`
  - evidence_mode：`fresh_run`
  - status：`recovered_and_verified`
  - current_role：`broker symbol list snapshot`

- 文件：`environment_snapshots\mt5_symbols_all__TradeMaxGlobal-Demo__60088394__20250101_000000__55.txt`
  - 类型：`ARTIFACT`
  - source_path：`%APPDATA%\\MetaQuotes\\Terminal\\Common\\Files\\mt5_symbols_all__TradeMaxGlobal-Demo__60088394__20250101_000000__55.txt`
  - repo_path：`environment_snapshots\mt5_symbols_all__TradeMaxGlobal-Demo__60088394__20250101_000000__55.txt`
  - producer：`MT5SymbolDumpProbe.ex5`
  - scope：`MT5 Symbols / TradeMaxGlobal-Demo__60088394 / AllSymbols`
  - evidence_mode：`fresh_run`
  - status：`recovered_and_verified`
  - current_role：`broker symbol list snapshot`

- 文件：`environment_snapshots\mt5_symbols_marketwatch__ICMarketsSC-Demo__52886989__20250101_000000__56.txt`
  - 类型：`ARTIFACT`
  - source_path：`%APPDATA%\\MetaQuotes\\Terminal\\Common\\Files\\mt5_symbols_marketwatch__ICMarketsSC-Demo__52886989__20250101_000000__56.txt`
  - repo_path：`environment_snapshots\mt5_symbols_marketwatch__ICMarketsSC-Demo__52886989__20250101_000000__56.txt`
  - producer：`MT5SymbolDumpProbe.ex5`
  - scope：`MT5 Symbols / ICMarketsSC-Demo__52886989 / MarketWatch`
  - evidence_mode：`fresh_run`
  - status：`recovered_and_verified`
  - current_role：`broker symbol list snapshot`

- 文件：`environment_snapshots\mt5_symbols_all__ICMarketsSC-Demo__52886989__20250101_000000__56.txt`
  - 类型：`ARTIFACT`
  - source_path：`%APPDATA%\\MetaQuotes\\Terminal\\Common\\Files\\mt5_symbols_all__ICMarketsSC-Demo__52886989__20250101_000000__56.txt`
  - repo_path：`environment_snapshots\mt5_symbols_all__ICMarketsSC-Demo__52886989__20250101_000000__56.txt`
  - producer：`MT5SymbolDumpProbe.ex5`
  - scope：`MT5 Symbols / ICMarketsSC-Demo__52886989 / AllSymbols`
  - evidence_mode：`fresh_run`
  - status：`recovered_and_verified`
  - current_role：`broker symbol list snapshot`

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h1_envmeta_20260701T\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h1_envmeta_20260701T\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURUSD / H1 / environment metadata snapshot`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`环境元数据绑定示例`
  - 备注：当前已确认 `run_summary.json` 包含 `install_root / data_root / server / login / access_server / environment_label`

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_overridecheck_20260701T\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_overridecheck_20260701T\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURUSD / H4 / DataRootOverride smoke check`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`显式 data root 选择能力硬证据`
  - 备注：当前已确认通过 `DataRootOverride` 指向 `AC48B16F101CC6359ADC4B870ED6B744` 时，fresh-run 与归档链仍可正常工作

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_20260701T1305\run_summary.json`
  - 类型：`INDEX_NOTE`
  - source_path：`run_xbreaking_probe_once.ps1`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_20260701T1305\run_summary.json`
  - producer：`run_xbreaking_probe_once.ps1`
  - scope：`XBreaking / EURUSD / H4 / environment inventory selector smoke check`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`环境快照选环境能力硬证据`
  - 备注：当前已确认通过 `EnvironmentInventoryJson + EnvironmentSelector=ICMarketsSC-Demo__52886989` 命中 inventory 后，fresh-run、归档与 `run_summary.environment.selection_mode=inventory_selector` 均正常工作

- 文件：`artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_20260701T1305\ingest_manifest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\eurusd_h4_envselect_20260701T1305\ingest_manifest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / EURUSD / H4 / validation_matrix archive ingest trace`
  - evidence_mode：`fresh_run`
  - status：`written`
  - current_role：`archive-tag 回收留痕索引`
  - 备注：当前已记录 `csv / report / tester log` 的 `source_path / repo_path / copied_at / matched_keywords / excerpt_path`，用于补齐 run-time 归档后的回收链说明

- 文件：`artifacts\xbreaking\validation_matrix\validation_matrix_index_latest.json`
  - 类型：`INDEX_NOTE`
  - source_path：`probe_artifact_ingest_v1.py`
  - repo_path：`artifacts\xbreaking\validation_matrix\validation_matrix_index_latest.json`
  - producer：`probe_artifact_ingest_v1.py`
  - scope：`XBreaking / validation_matrix batch overview`
  - evidence_mode：`fresh_run_index`
  - status：`written`
  - current_role：`validation_matrix 批次级总览索引`
  - 备注：当前会汇总各 archive 的 `symbol / chart_period / indicator_period / environment_label / selection_mode / manifest_record_count`，用于替代逐目录人工盘点；并已反映失败遗留空 archive `eurusd_h4_jan0310_20260701T124043_window_a` 已被清理
  - 备注_2：若旧 `run_summary.json` 缺 `environment` 字段，总览索引会从 `run_summary.files.*.source` 提取 `MetaQuotes\\Terminal\\<hash>` 并结合 `environment_snapshots\\mt_environment_inventory_latest.json` 推断环境字段，标记 `environment_inferred=true`
  - 备注_3：总览索引会统计 `selection_mode_missing_count` 并列出 `selection_mode_missing_archive_tags`（最多 30 个），用于暴露“环境选择方式信息缺口”

## 当前默认入口

- 执行入口：
  - `BATCH_01_EXECUTION_CARD.md`
- 产物索引：
  - `BATCH_01_ARTIFACT_INDEX_TEMPLATE.md`
- 运行说明：
  - `MT4_MT5_FIRST_RUN_PLAYBOOK.md`
- 备注总表：
  - `BATCH_01_PROVENANCE_NOTEBOARD.md`

## 当前缺口

- `Volty`
  - 当前批次级 fresh-run 证据已闭环，剩余工作转向字段升级与迁移固化
- `XBreaking`
  - 当前批次级 fresh-run 与跨环境硬证据已闭环，剩余工作转向 buffer 语义字段升级与旧仓已购 CSV 接线
- `Purchased CSV`
  - 当前预览标准化归档已落地，剩余工作转向扩大输入覆盖并接入新仓消费者

## 一句话记忆

- 以后看这批文件，不要只看文件名；先看这张备注总表，确认“它是谁、怎么来的、现在干什么、证据算不算硬”。
