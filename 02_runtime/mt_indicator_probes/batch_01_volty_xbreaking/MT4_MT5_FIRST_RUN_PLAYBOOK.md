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
- 作用：
  - 扫描本机 `MetaQuotes` 终端目录中的候选 `csv / report / log`
  - 把最新匹配文件复制到当前批次的 `artifacts`
  - 对 `log` 会先按家族默认关键词过滤，不再把所有 `*.log` 都当候选
  - 还支持按文件名关键词、尾部行数限制和摘录落盘

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
python "02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py" --family xbreaking --kind csv --copy-latest
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
python "02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\probe_artifact_ingest_v1.py" --family xbreaking --kind log --copy-latest --log-filename-keyword 20260609 --log-keyword DONE --log-tail-lines 300
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
3. 在 `MT4 Strategy Tester` 里设置
   - `Expert`: `Probe\MT4Probe_Volty`
   - `Symbol`: 建议先 `EURUSD`
   - `Period`: 建议先 `H1`
   - `Model`: `Open prices only`
   - 时间范围：建议先沿用 `2025.01.01` 到 `2025.01.15`
4. 跑完后回收产物
   - `csv`：找 `MT4_probe_Volty_<SYMBOL>_<TF>_<STAMP>.csv`
   - `log`：导出或复制 tester/journal 关键日志
   - `tester report`：导出 `.htm` 或截图也可，但优先 `.htm`
5. 复制回新仓库
   - 手工复制，或用 `probe_artifact_ingest_v1.py`
   - `csv` -> `artifacts\volty\csv`
   - `log` -> `artifacts\volty\log`
   - `tester report` -> `artifacts\volty\tester_report`

## XBreaking 首次实跑

1. 准备 `MT5` 指标与 probe 文件
   - 从 `12_tooling_runtime_archive\batch_02_mt_indicator_family\` 取：
     - `XBreaking.ex5`
     - `XBreakingProbe.ex5`
2. 放入 `MT5` 终端
   - `XBreakingProbe.ex5` 放到 `MQL5\Experts\`
   - `XBreaking.ex5` 放到 `MQL5\Indicators\`
3. 在 `MT5 Strategy Tester` 里设置
   - `Expert`: `XBreakingProbe`
   - `Symbol`: 建议先 `EURUSD`
   - `Period`: 建议先 `H1`
   - 时间范围：建议先沿用 `2025.01.01` 到 `2025.01.15`
   - `UseLocal`: 开启本地历史
4. 跑完后回收产物
   - `csv`：找 `XBreaking_probe_<SYMBOL>_<TF>_<STAMP>.csv`
   - `log`：导出 tester journal 或 terminal journal
   - `tester report`：导出 `.htm`
5. 复制回新仓库
   - 手工复制，或用 `probe_artifact_ingest_v1.py`
   - `csv` -> `artifacts\xbreaking\csv`
   - `log` -> `artifacts\xbreaking\log`
   - `tester report` -> `artifacts\xbreaking\tester_report`

## 旧 ini 的使用方式

- `mt4probe_volty_portable.ini`
  - 当前只能作为参数范围参考，不直接当新仓库默认执行稿。
- `XBreakingProbe.ini`
  - 当前只能作为 `MT5 tester` 字段参考，不直接复用旧 `Report=` 老路径。
- `MT4Probe_XBreaking.ini`
  - 当前指向旧仓库路径，而且对象也不是本批主线，不纳入本批默认执行口径。

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
