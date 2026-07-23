# Batch 145 Batch9 N02 Initial Balance Evidence Absorb

更新时间：2026-07-15

## 批次目标

- 为 `Batch9 N02 Initial Balance` 补齐“定义/源码/证据位”，让后续重开线有可追溯入口。
- 当前阶段只做资料整理，不把它接入默认执行链。

## 已知上游入口

- 来源库 Batch9 入口：
  - `10_source_library_archive/_raw_snapshot_batch09/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/README.md`
- Batch9 四分流裁决：
  - `10_source_library_archive/_raw_snapshot_batch09/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/Batch9_批次收口与四分流_v1.md`
- 手动补采网页清单：
  - `10_source_library_archive/_raw_snapshot_batch09/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/Batch9_待用户手动补网页清单_v1.md`

## 当前产物

- `manifest_v1.tsv`
- `provenance.md`
- `N02_EVIDENCE_GAP_STATUS_v1.tsv`
- `BATCH_145_EXECUTION_CARD.md`
- `BATCH_145_ARTIFACT_INDEX_v1.md`
- `00_raw_snapshot/Initial_Balance_Breakout__historical_recovered_excerpt.md`
- `00_raw_snapshot/FirstHourBreakout__manual_web_capture__20260713.md`
- `00_raw_snapshot/Initial_Balance__manual_web_capture__20260714.md`
- `00_raw_snapshot/ib_formula_or_chart_example.md`
- `00_raw_snapshot/N02_acceptance_extension_statistics_quote_bundle__20260714.md`
- `00_raw_snapshot/N02_chart_and_teaching_figure_bundle__20260714.md`

## 默认阅读顺序

- 1. 先看本 README
- 2. 再看 `N02_EVIDENCE_GAP_STATUS_v1.tsv`
- 3. 最后回到 Batch9 上游入口补证据与回链

## 当前边界

- 当前批次只负责证据补强与回链，不负责：
  - 字段实现
  - runtime 接线
  - 回测与执行

## 当前进展

- 当前批次已从：
  - `历史回收摘录`
  - `相邻平台网页正文`
  - `同主题 Initial Balance 页`
  继续推进到：
  - `IB 最小公式/acceptance/failed breakout` 的结构化摘录页
  - `acceptance / range extension / statistics` 的外部强证据引文包
  - `chart / figure / caption` 的教材级图例证据包
  - 更贴近经典 `Market Profile` 的 `IB = A + B` glossary 图例与 `CBOT handbook` 原始体系线索
  - 更贴近经典 `Market Profile` 的 `IB = A + B` glossary 图例、`CBOT handbook` 原始体系线索与教材扫描页级入口
  - 已有同主题定义页、半硬证据页、外部强证据引文包、教材级图例证据包，以及更贴近经典 `Market Profile` 的原始 glossary 图例线索
  - 已有同主题定义页、半硬证据页、外部强证据引文包、教材级图例证据包，以及更贴近经典 `Market Profile` 的原始 glossary 图例线索与教材扫描页级入口
  - 但仍缺更完整原始教材扫描图示与源码硬证据
