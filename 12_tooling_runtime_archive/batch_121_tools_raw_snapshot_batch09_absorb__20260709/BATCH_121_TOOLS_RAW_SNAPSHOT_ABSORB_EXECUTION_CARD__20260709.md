# 批次 121 Tools Raw Snapshot Absorb 执行卡

## 生成入口

- `GENERATOR`: `historical_recovered_archive_absorb_20260709`
- `SOURCE`: `20_tools_workspace/_raw_snapshot_batch09/`

## 当前作用

- 把 `20_tools_workspace/_raw_snapshot_batch09` 从合同外工具工作区整体吸收到 `12_tooling_runtime_archive`。
- 统一保留 `group08_*`、`s_*`、`tk_r*`、通用辅助脚本与 `robocopy` 日志的历史快照形态。
- 用家族索引与裁决台账标清哪些脚本已被新仓活跃批次吸收、哪些只保留为 `archive_only`、哪些只作为历史证据。
