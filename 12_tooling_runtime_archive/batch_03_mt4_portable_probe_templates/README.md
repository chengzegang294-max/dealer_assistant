# MT4 Portable Probe Templates Batch 03

## 用途

- 这里放从旧 `03_MT4便携探针实例` 抽出来的最小可复用文本配置模板。
- 目标是减少当前 `Volty / probe` 主线对旧便携终端目录的直接依赖。

## 当前包含

- `mt4probe_volty_portable.template.ini`
- `smoke_moving_average_portable.template.ini`

## 来源

- 历史来源目录：
  - `旧仓库\12_工具运行时_TOOLING_RUNTIME\03_MT4便携探针实例\config\00_text_recovered_batch1\`
- 参考文件：
  - `README_batch1.md`
  - `mt4probe_volty_portable.ini`
  - `smoke_moving_average_portable.ini`

## 当前裁决

- 这里的 `.template.ini` 属于 `GENERATOR / ARCHIVE_TEMPLATE`。
- 它们可作为新仓执行前的参考模板，但不是“已经验证无差异的终端快照”。
- `servers.ini / terminal.ini` 保留在旧仓冻结层，不迁入这里作为默认入口。

## 使用方式

- 手工复制模板后，按你的终端目录和当前实验目标补充必要字段。
- `TestReport` 优先保持终端内相对路径口径。
- 实跑产物回收根仍以：
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\...`

## 缺口

- 这里不包含真实账号态、服务器态和窗口态配置。
- 若后续需要 `MT5 portable` 模板，应单开新批次，不混入本批。

## 备注入口

- `BATCH_03_MT4_PORTABLE_PROBE_TEMPLATES_EXECUTION_CARD__20260709.md`
- `BATCH_03_MT4_PORTABLE_PROBE_TEMPLATES_ARTIFACT_INDEX__20260709.tsv`
