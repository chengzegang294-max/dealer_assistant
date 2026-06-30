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

- 文件：`artifacts\volty\log\`
  - 类型：`ARTIFACT`
  - evidence_mode：`pending`
  - status：`not_found_yet`
  - current_role：`缺口`
  - 备注：本机终端目录暂未发现明确 `Volty tester log / journal`

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
  - 当前作用：旧测试参数与理论报告路径参考
  - 当前状态：`archive_reference_only`

### Artifact

- 文件：`artifacts\xbreaking\csv\XBreaking_probe_EURUSD_H1_20250101_220500.csv`
  - 类型：`ARTIFACT`
  - source_path：`本机终端目录（已脱敏）/XBreaking_probe_EURUSD_H1_20250101_220500.csv`
  - repo_path：`artifacts\xbreaking\csv\XBreaking_probe_EURUSD_H1_20250101_220500.csv`
  - producer：`XBreakingProbe.mq5`
  - scope：`XBreaking / EURUSD / H1`
  - evidence_mode：`fresh_run`
  - status：`recovered_and_verified`
  - current_role：`当前硬证据`
  - 备注：已确认 `handle=10`、`init_err=0`

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

- 文件：`artifacts\xbreaking\tester_report\`
  - 类型：`ARTIFACT`
  - evidence_mode：`pending`
  - status：`not_found_yet`
  - current_role：`缺口`
  - 备注：`XBreakingProbe.ini` 指向过理论报告路径，但当前仓库中未找到实际报告文件

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
  - 缺明确 `tester log / journal`
  - 缺一次本机终端重新跑出的 `fresh_run csv`
- `XBreaking`
  - 缺明确 `tester report`
  - 缺强相关 `tester log / journal`

## 一句话记忆

- 以后看这批文件，不要只看文件名；先看这张备注总表，确认“它是谁、怎么来的、现在干什么、证据算不算硬”。
