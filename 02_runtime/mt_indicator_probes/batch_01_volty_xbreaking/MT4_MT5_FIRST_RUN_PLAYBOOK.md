# MT4 MT5 First Run Playbook

## 目的

- 这份操作卡用于把 `Volty / XBreaking` 的第一次实际 probe 跑出来，并把产物带回新仓库。
- 当前目标只是收证据，不是改策略，也不是把结果直接变成门控。

## 批次目录

- 当前批次根目录：
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking`
- `Volty` 产物回收目录：
  - `artifacts\volty\csv`
  - `artifacts\volty\log`
  - `artifacts\volty\tester_report`
- `XBreaking` 产物回收目录：
  - `artifacts\xbreaking\csv`
  - `artifacts\xbreaking\log`
  - `artifacts\xbreaking\tester_report`

## 辅助脚本

- 当前批次已补：
  - `probe_artifact_ingest_v1.py`
  - `run_xbreaking_probe_once.ps1`
- 作用：
  - 扫描本机 `MetaQuotes` 终端目录中的候选 `csv / report / log`
  - 把最新匹配文件复制到当前批次的 `artifacts`
  - 对 `log` 会先按家族默认关键词过滤，不再把所有 `*.log` 都当候选
  - 还支持按文件名关键词、尾部行数限制和摘录落盘
  - `run_xbreaking_probe_once.ps1` 会自动部署 `XBreakingProbe.ex5 / XBreaking.ex5`、生成 `runtime .set + runtime .ini`、执行 `MT5 /config` 并等待新 `csv / report / log`

## Volty DumpSeries 快捷模板

- 当前批次已补两份批次内可复制模板：
  - `MT4Probe_Volty_dumpseries_0_6.ini`
    - 作用：`MT4Probe_Volty` 的 expert input 模板
    - 关键参数已写死：`DumpSeries=1`、`DumpModeStart=0`、`DumpModeEnd=6`
    - 建议复制目标：便携终端 `tester\MT4Probe_Volty.ini`
  - `mt4probe_volty_dumpseries_portable.ini`
    - 作用：`MT4 portable` 启动配置模板
    - 当前默认：`EURUSD / H1 / Open prices only / 2025.01.01 -> 2025.01.15`
    - 建议复制目标：便携终端 `config\mt4probe_volty_dumpseries_portable.ini`
- 这两份文件属于本批 `GENERATOR`，当前作用是降低 fresh-run 的手填摩擦，不替代终端实际安装步骤。

## 常用命令

```bash
python "02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py" --family volty --kind csv --list
```

```bash
python "02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py" --family volty --kind csv --copy-latest
```

```bash
python "02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py" --family volty --kind csv --normalize-volty-summary
```

```bash
python "02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py" --family volty --kind csv --normalize-volty-series
```

```bash
python "02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py" --family xbreaking --kind report --list
```

```bash
powershell -ExecutionPolicy Bypass -File "02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\run_xbreaking_probe_once.ps1" -InstallRoot <MT5_INSTALL_ROOT>
```

```bash
python "02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py" --family xbreaking --kind csv --copy-latest
```

```bash
python "02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py" --family xbreaking --kind csv --copy-latest --archive-tag gbpusd_h4_20260701T
```

```bash
python "02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py" --family xbreaking --kind log --list
```

```bash
python "02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py" --family xbreaking --kind log --list --log-keyword XBreakingProbe --log-keyword DONE
```

```bash
python "02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py" --family xbreaking --kind log --list --log-filename-keyword 20260609 --log-keyword DONE --log-tail-lines 300
```

```bash
python "02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py" --family xbreaking --kind log --copy-latest --log-tail-lines 400
```

## Volty 首次实跑

1. 准备 `MT4` 指标与 probe 文件
   - 从 `12_tooling_runtime_archive\batch_02_mt_indicator_family\` 取：
     - `VoltyChannel_Stop_v2_1M.ex4`
     - `MT4Probe_Volty.ex4`
   - 若你的 `MT4Probe_Volty` 代码使用 `Probe\\VoltyChannel_Stop_v2_1M` 名称，则在终端里保持 `Experts\Probe\` 目录结构一致。
2. 放入 `MT4` 终端
   - `MT4Probe_Volty.ex4` 放到 `MQL4\Experts\Probe\`
   - `VoltyChannel_Stop_v2_1M.ex4` 放到 `MQL4\Indicators\Probe\`
   - 若使用本批最短路径：
     - 把 `MT4Probe_Volty_dumpseries_0_6.ini` 复制为终端 `tester\MT4Probe_Volty.ini`
     - 把 `mt4probe_volty_dumpseries_portable.ini` 复制到终端 `config\`
   - 若只想参考旧模板，可再看：
     - `12_tooling_runtime_archive\batch_03_mt4_portable_probe_templates\mt4probe_volty_portable.template.ini`
3. 在 `MT4 Strategy Tester` 里设置
   - 若已复制本批模板，默认就是：
     - `Expert`: `Probe\MT4Probe_Volty`
     - `Symbol`: `EURUSD`
     - `Period`: `H1`
     - `Model`: `Open prices only`
     - 时间范围：`2025.01.01` 到 `2025.01.15`
     - `DumpSeries=1`
     - `DumpModeStart=0`
     - `DumpModeEnd=6`
   - 若手工设置，也保持以上参数不变
4. 跑完后回收产物
   - `csv`：找 `MT4_probe_Volty_<SYMBOL>_<TF>_<STAMP>.csv`
   - `log`：导出或复制 tester/journal 关键日志
   - `tester report`：优先回收 `tester\files\mt4probe_volty_dumpseries_portable.htm`
5. 复制回新仓库
   - 手工复制，或用 `probe_artifact_ingest_v1.py`
   - `csv` -> `artifacts\volty\csv`
   - `log` -> `artifacts\volty\log`
   - `tester report` -> `artifacts\volty\tester_report`
6. 回收后立即验收
   - 先跑：
     - `python 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py --family volty --kind csv --copy-latest`
   - 再跑：
     - `python 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py --family volty --kind csv --normalize-volty-series`
   - 再跑：
     - `python 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_batch_acceptance_v1.py --json-only`

## XBreaking 首次实跑

1. 准备 `MT5` 指标与 probe 文件
   - 从 `12_tooling_runtime_archive\batch_02_mt_indicator_family\` 取：
     - `XBreaking.ex5`
     - `XBreakingProbe.ex5`
2. 放入 `MT5` 终端
   - `XBreakingProbe.ex5` 放到 `MQL5\Experts\`
   - `XBreaking.ex5` 放到 `MQL5\Indicators\`
3. 优先使用批次内自动脚本
   - 直接执行前先显式指定目标安装目录：
     - `powershell -ExecutionPolicy Bypass -File 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\run_xbreaking_probe_once.ps1 -InstallRoot <MT5_INSTALL_ROOT>`
  - 若想先确认当前机器有哪些 `MetaQuotes` 运行环境：
    - `powershell -ExecutionPolicy Bypass -File 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_mt_environment_inventory.ps1 -OutputJson 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\environment_snapshots\mt_environment_inventory_latest.json`
  - 若第二套环境已经出现在清单里，但你想显式锁定某个 data root：
    - `powershell -ExecutionPolicy Bypass -File 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\run_xbreaking_probe_once.ps1 -InstallRoot <MT5_INSTALL_ROOT> -DataRootOverride <MT5_DATA_ROOT> -ChartPeriod H4 -IndicatorPeriod H4 -ReportStem xbreaking_probe_eurusd_h4_overridecheck -ArchiveTag eurusd_h4_overridecheck_20260701T`
  - 若环境清单里已经有目标 `MT5`，想按标签或 hash 直接选：
    - `powershell -ExecutionPolicy Bypass -File 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\run_xbreaking_probe_once.ps1 -EnvironmentInventoryJson 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\environment_snapshots\mt_environment_inventory_latest.json -EnvironmentSelector <MT5_ENVIRONMENT_LABEL_OR_HASH> -ChartPeriod H4 -IndicatorPeriod H4 -ReportStem xbreaking_probe_eurusd_h4_envselect -ArchiveTag eurusd_h4_envselect_20260701T1305`
  - 若想批量跑 validation-matrix（多 symbol/period）：
    - `powershell -ExecutionPolicy Bypass -File 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\run_xbreaking_validation_matrix.ps1 -Symbols GBPUSD -Periods H4 -TagSuffix matrix_sample`
  - 若想批量验证某个指定 data root，也可加：
    - `-DataRootOverride C:\Users\91883\AppData\Roaming\MetaQuotes\Terminal\AC48B16F101CC6359ADC4B870ED6B744`
  - 若想批量验证 inventory 里的目标环境，也可加：
    - `-EnvironmentInventoryJson 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\environment_snapshots\mt_environment_inventory_latest.json -EnvironmentSelector <MT5_ENVIRONMENT_LABEL_OR_HASH>`
  - 若想做“日期窗口稳定性”批量验证并让 tag/readme 更易读：
    - `powershell -ExecutionPolicy Bypass -File 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\run_xbreaking_validation_matrix.ps1 -Symbols EURUSD,XAUUSD -Periods H4 -FromDate 2025.01.03 -ToDate 2025.01.10 -WindowTag jan03_10 -TagSuffix window_a`
    - `powershell -ExecutionPolicy Bypass -File 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\run_xbreaking_validation_matrix.ps1 -Symbols EURUSD,XAUUSD -Periods H4 -FromDate 2025.01.07 -ToDate 2025.01.14 -WindowTag jan07_14 -TagSuffix window_b`
  - 切换非默认场景时可直接带参数，例如：
    - `powershell -ExecutionPolicy Bypass -File 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\run_xbreaking_probe_once.ps1 -ChartPeriod H4 -IndicatorPeriod H4 -ReportStem xbreaking_probe_eurusd_h4 -ArchiveTag eurusd_h4_20260701_setmode`
  - 当前脚本能力：
    - `install_root` 必须显式提供，或由 `EnvironmentSelector` 命中的 `origin_path` 自动解析
    - 通过 `origin.txt` 反查对应 `MT5 data root`
    - 支持参数化 `Symbol / ChartPeriod / IndicatorPeriod / FromDate / ToDate / ReportStem / ArchiveTag`
    - 先生成 `MQL5\Profiles\Tester\XBreakingProbe.runtime.<report_stem>.set`
    - 再在 runtime tester `.ini` 中写入 `ExpertParameters=<that_set_file>`
    - 先尝试绝对 `Report=`，若未出 `.htm`，自动 fallback 为 bare `Report=<report_stem>`
    - 若提供 `ArchiveTag`，会把 `csv / report / terminal log / tester log / runtime ini / runtime set / run_summary.json` 归档到 `artifacts\xbreaking\validation_matrix\<ArchiveTag>\`
    - 归档内的 `run_summary.json` 现已绑定 `install_root / data_root / server / login / access_server`
    - 默认不再回退到任何机器私有 `MT5` 安装目录
    - 若提供 `DataRootOverride`，会直接使用该 data root，不再依赖 `origin.txt` 自动匹配
    - 若提供 `EnvironmentInventoryJson + EnvironmentSelector`，会从环境快照中解析目标 `MT5 data root`，并在 `run_summary.json` 里记录 `selection_mode / inventory_selector / inventory_match_field`
    - 若后续通过 `probe_artifact_ingest_v1.py --archive-tag <tag>` 补拷 `csv / report / log`，归档根目录下还会额外写出 `ingest_manifest.json`
    - 可显式执行 `python 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py --family xbreaking --kind csv --write-validation-matrix-index` 刷新 `validation_matrix_index_latest.json`
    - 若走 `--archive-tag` 回收链，脚本也会自动刷新 `validation_matrix_index_latest.json`
    - `run_xbreaking_validation_matrix.ps1` 当前已兼容 `PowerShell 5`，并支持 `WindowTag` 把日期窗口写进 `report_stem / archive_tag`
4. 若需要手工在 `MT5 Strategy Tester` 里设置
   - `Expert`: `XBreakingProbe`
   - `Symbol`: `EURUSD`
   - `Period`: `H1`
   - 时间范围：`2025.01.01` 到 `2025.01.15`
   - `UseLocal`: 开启本地历史
   - `Report=` 建议优先用 `xbreaking_probe_portable`
5. 跑完后回收产物
   - `csv`：找 `XBreaking_probe_<SYMBOL>_<TF>_<STAMP>.csv`
   - `log`：优先回收 `tester journal`，其次保留 terminal journal
   - `tester report`：找 `xbreaking_probe_portable.htm`
   - 注意：本机当前实测里，report 可能落在 `MT5 data root` 根目录，而不是 `tester\files`
6. 复制回新仓库
   - 手工复制，或用 `probe_artifact_ingest_v1.py`
   - `csv` -> `artifacts\xbreaking\csv`
   - `log` -> `artifacts\xbreaking\log`
   - `tester report` -> `artifacts\xbreaking\tester_report`
7. 回收后立即验收
   - 先跑：
     - `python 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py --family xbreaking --kind csv --copy-latest`
   - 再跑：
     - `python 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py --family xbreaking --kind report --copy-latest`
   - 再跑：
     - `python 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py --family xbreaking --kind log --copy-latest --log-tail-lines 400`
   - 再跑：
     - `python 02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_batch_acceptance_v1.py --json-only`

## 当前 ini 的使用方式

- `mt4probe_volty_portable.ini`
  - 当前采用终端内相对路径口径，可作为 `MT4` 便携探针参考模板。
  - 若需要去账号态的模板，优先看：
    - `12_tooling_runtime_archive\batch_03_mt4_portable_probe_templates\mt4probe_volty_portable.template.ini`
- `XBreakingProbe.ini`
  - 当前已改成终端内相对 `Report=` 路径，不再默认依赖旧仓库 `backtest_out`。
  - 当前本机实测显示，`Report=xbreaking_probe_portable` 比绝对路径更稳定，且报告会落在 `MT5 data root` 根目录。
  - 当前新增约束：自定义 `InpIndicatorTf / InpBarsToProbe / InpMaxBuffers` 时，应通过 `ExpertParameters=<generated .set>` 注入，不再依赖把 `Inp...=` 直接追加进 tester `.ini`。
  - 使用前仍要确认 `XBreakingProbe.ex5` 已放进 `MQL5\Experts\`。
- `MT4Probe_XBreaking.ini`
  - 当前已改成 `Probe\MT4IndicatorProbe` + 终端内相对 `TestReport=` 路径。
  - 使用前仍要确认 `MT4IndicatorProbe.ex4` 和 `XBreaking.ex4` 已放进终端对应 `Probe\` 目录。
  - 当前对象仍以 `MT5 XBreakingProbe` 为主，`MT4Probe_XBreaking.ini` 保留为补充验证入口。

## 回传后我会做什么

1. 回填 `BATCH_01_ARTIFACT_INDEX_TEMPLATE.md` 的真实路径
2. 把 `Volty` 结果写入 `volty_probe_result_intake_v1.md`
3. 把 `XBreaking` 结果写入 `xbreaking_buffer_semantics_log_v1.md`
4. 复核 `volty_xbreaking_field_draft_v1.md` 哪些字段能升级

## 最小回传清单

- `Volty`
  - `1` 份 `csv`
  - `1` 份 `log` 或 journal 摘录
  - `1` 份 `tester report`
- `XBreaking`
  - `1` 份 `csv`
  - `1` 份 `log` 或 journal 摘录
  - `1` 份 `tester report`

## 红线

- 不把没有回收到新仓库的产物，口头记成“已完成”
- 不把 `XBreaking` 任一 buffer 在首轮就写成硬信号
- 不因为旧 `ini` 能跑，就继续把老仓库路径当默认产物路径
