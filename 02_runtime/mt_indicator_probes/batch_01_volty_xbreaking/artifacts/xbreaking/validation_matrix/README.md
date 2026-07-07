# XBreaking Validation Matrix

## 目的

- 固定存放 `XBreakingProbe` 在不同 `symbol / timeframe` 场景下的 fresh-run 证据，用于复核 `buffer_activity_profile` 是否稳定。

## 目录约定

- 每次运行固定归档到：`<ArchiveTag>\`
- 每个 `ArchiveTag` 目录内固定包含：
  - `csv/`
  - `report/`
  - `log/`
  - `runtime_config/`
  - `run_summary.json`

## 入口

- 单次：
  - `run_xbreaking_probe_once.ps1`
- 批量：
  - `run_xbreaking_validation_matrix.ps1`

