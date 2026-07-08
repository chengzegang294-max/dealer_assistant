# Promoted From Raw Snapshot

更新时间：2026-07-08

## 目的

- 这里存放从 `00_raw_snapshot/` “提升归位”的运行时资产副本（`.json/.csv/.html`）。
- 原样快照保持不动；本目录用于后续整理为可复现运行时（报告/样本/面板预览）。

## 代码位置

- 从 `00_raw_snapshot/` 提升归位的 `.py` 代码副本已迁到：`03_quantize/promoted_code_from_raw_snapshot/`

## 使用边界

- 本目录文件默认视为“外部/AI产物原样搬运”，只作为参考与改造素材，不等同于 repo 内已验收可跑组件。
- 若要进入主线可跑层（`02_runtime` / `12_tooling_runtime_archive`），必须补齐：
  - 最小输入样本
  - 可复现实跑命令
  - 验收卡（输出字段/行数/关键断言）
