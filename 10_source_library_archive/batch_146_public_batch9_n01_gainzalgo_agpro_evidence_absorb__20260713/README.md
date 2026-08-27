# Batch 146 Batch9 N01 GainzAlgo AGPro Evidence Absorb

更新时间：2026-07-15

## 批次目标

- 为 `Batch9 N01 GainzAlgo / AG Pro` 补齐“定义/源码/证据位”，用于波动环境解释层与后续重开线。
- 当前阶段只做资料整理，不把它接入默认执行链。

## 已知上游入口

- 来源库 Batch9 入口：
  - `file:///D:/Stock/trading_assistant/10_source_library_archive//_raw_snapshot_batch09//10_%E6%9D%A5%E6%BA%90%E5%BA%93_SOURCE_LIBRARY//00_%E5%A4%96%E9%83%A8%E5%85%AC%E5%BC%80%E8%B5%84%E6%96%99%E4%B8%8E%E6%96%B9%E6%B3%95%E8%AE%BA%E5%8F%82%E8%80%83//01_%E5%A4%96%E9%83%A8%E5%85%AC%E5%BC%80%E6%8C%87%E6%A0%87%E8%B5%84%E6%96%99_Batch9//README.md`
- Batch9 四分流裁决：
  - `10_source_library_archive/_raw_snapshot_batch09/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/Batch9_批次收口与四分流_v1.md`
- 手动补采网页清单：
  - `10_source_library_archive/_raw_snapshot_batch09/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/Batch9_待用户手动补网页清单_v1.md`

## 当前产物

- `manifest_v1.tsv`
- `provenance.md`
- `N01_EVIDENCE_GAP_STATUS_v1.tsv`
- `BATCH_146_EXECUTION_CARD.md`
- `BATCH_146_ARTIFACT_INDEX_v1.md`
- `00_raw_snapshot/Volatility_Regimes__GainzAlgo__historical_recovered_excerpt.md`
- `00_raw_snapshot/AG_Pro_ATR_Compression_Map__historical_recovered_excerpt.md`
- `00_raw_snapshot/Volatility_Regimes__GainzAlgo__manual_web_capture__20260713.md`
- `00_raw_snapshot/AG_Pro_ATR_Compression_Map__manual_web_capture__20260713.md`
- `00_raw_snapshot/n01_formula_snippets.md`
- `00_raw_snapshot/N01_source_code_and_parameter_defaults_bundle__20260714.md`
- `00_raw_snapshot/N01_parameter_dictionary_v1.tsv`
- `00_raw_snapshot/N01_source_logic_excerpt_bundle__20260714.md`
- `00_raw_snapshot/AGPro_family_invite_only_access_note__20260715.md`

## 默认阅读顺序

- 1. 先看本 README
- 2. 再看 `N01_EVIDENCE_GAP_STATUS_v1.tsv`
- 3. 最后回到 Batch9 上游入口补证据与回链

## 当前边界

- 当前批次只负责证据补强与回链，不负责：
  - 字段实现
  - runtime 接线
  - 回测与执行

## 当前进展

- 当前批次已从：
  - `历史回收摘录`
  - `GainzAlgo / AG Pro 原作者页详细网页正文`
  继续推进到：
  - `GainzAlgo / AG Pro` 源码首屏、参数默认值证据包、参数字典表、源码逻辑摘录包、更长连续源码窗口与结构化公式摘录页
  - `AGPro` 家族 invite-only 访问边界与 `Source code disabled` 说明页
- 当前更准确口径是：
  - 已能把 `ATR / baseline / atr_ratio / regime / ATR Bands / Stop / TP / Position Size` 与 `compression_score / 四因子 / 四阶段 / key inputs / mini panel 字段 / 源码首屏 / 参数默认值 / 参数字典 / 源码逻辑摘录 / 更长连续源码窗口 / invite-only access-state` 收成半硬到近硬证据
  - 但仍缺更完整 Pine 源码正文、参数截图与 AG Pro 精确公式硬证据；当前也已能解释一部分源码缺口来自 invite-only 页面边界
