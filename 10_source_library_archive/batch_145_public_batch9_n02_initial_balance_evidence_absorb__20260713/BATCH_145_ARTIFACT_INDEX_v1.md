# Batch 145 Artifact Index v1

更新时间：2026-07-15

## 当前批次产物

| 文件类型 | 原路径/来源 | 新路径 | 生成入口 | 适用对象 | 当前作用 | 证据强度 | 状态 | 缺口 |
|---|---|---|---|---|---|---|---|---|
| `INDEX_NOTE` | `batch_145/README.md` | `batch_145/README.md` | `manual_batch_setup` | `Batch9 N02 Initial Balance` | 批次入口 | `hard` | `active` | 无 |
| `INDEX_NOTE` | `batch_145/provenance.md` | `batch_145/provenance.md` | `manual_batch_setup` | `Batch9 N02 Initial Balance` | 来源追溯说明 | `hard` | `active` | 无 |
| `INDEX_NOTE` | `batch_145/N02_EVIDENCE_GAP_STATUS_v1.tsv` | `batch_145/N02_EVIDENCE_GAP_STATUS_v1.tsv` | `manual_batch_setup` | `Batch9 N02 Initial Balance` | 证据缺口清单 | `hard` | `active` | 需实际证据文件 |
| `ARTIFACT` | `Initial_Balance_Breakout__page_excerpt.md` 历史回收 | `batch_145/00_raw_snapshot/Initial_Balance_Breakout__historical_recovered_excerpt.md` | `historical_recovered_excerpt` | `Batch9 N02 Initial Balance` | 定义页与原文证据 | `historical_recovered` | `active` | 仍缺网页全文/截图 |
| `ARTIFACT` | `Initial_Balance_Breakout__historical_recovered_excerpt.md` | `batch_145/00_raw_snapshot/Initial_Balance_Breakout__historical_recovered_excerpt.md` | `historical_recovered_excerpt` | `Batch9 N02 Initial Balance` | `2 periods outside IB` 原文段 | `historical_recovered` | `active` | 仍缺更完整上下文截图 |
| `ARTIFACT` | `https://toslc.thinkorswim.com/center/reference/Tech-Indicators/strategies/E-K/FirstHourBreakout.html` | `batch_145/00_raw_snapshot/FirstHourBreakout__manual_web_capture__20260713.md` | `manual_webpage_capture` | `Batch9 N02 Initial Balance` | 首小时区间注册与 breakout 时间窗网页证据 | `weak_evidence` | `active` | 是相邻平台页，不是 IB 原始命名页 |
| `ARTIFACT` | `https://futuresindicators.com/learn/initial-balance-basics + https://www.investing.com/analysis/how-to-trade-the-initial-balance-like-a-pro-200678607` | `batch_145/00_raw_snapshot/Initial_Balance__manual_web_capture__20260714.md` | `manual_webpage_capture` | `Batch9 N02 Initial Balance` | 直接使用 `Initial Balance / IB High / IB Low / range extension / failed breakout` 术语的同主题网页证据 | `manual_webpage_capture` | `active` | 已补同主题定义页，仍缺源码段或图例 |
| `ARTIFACT` | `Initial_Balance_Breakout__historical_recovered_excerpt.md + FirstHourBreakout__manual_web_capture__20260713.md` | `batch_145/00_raw_snapshot/ib_formula_or_chart_example.md` | `manual_excerpt_capture` | `Batch9 N02 Initial Balance` | IB 最小公式、acceptance 与失败模式结构化摘录 | `weak_evidence` | `active` | 已有半硬证据页，仍需源码段或图例 |
| `ARTIFACT` | `https://www.shadowtrader.net/glossary/acceptance/ + https://www.aspenres.com/documents/aspengraphics4.0/Using_Market_Profile.htm + https://www.trevortrades.com/initial-balance` | `batch_145/N02_EVIDENCE_GAP_STATUS_v1.tsv` | `external_evidence_linkage` | `Batch9 N02 Initial Balance` | `two TPO periods` acceptance 定义、`range extension` 标准定义与 `Contained 0.6%` 统计线索 | `linked_external_evidence` | `active` | 已锁定外部强证据，但尚未单独落图例/统计页 |
| `ARTIFACT` | `ShadowTrader + Aspen + TrevorTrades quote capture` | `batch_145/00_raw_snapshot/N02_acceptance_extension_statistics_quote_bundle__20260714.md` | `manual_quote_bundle_capture` | `Batch9 N02 Initial Balance` | acceptance、range extension 与 breakout 统计的正式引文证据包 | `strong_quote_bundle` | `active` | 已正式归档引文包，仍缺图例/源码硬证据 |
| `ARTIFACT` | `FuturesIndicators + Noesis + WindoTrader + ShadowTrader + ATAS + CBOT handbook mirror + Mind Over Markets page read + Market Profile Basics scan` | `batch_145/00_raw_snapshot/N02_chart_and_teaching_figure_bundle__20260714.md` | `manual_chart_caption_capture` | `Batch9 N02 Initial Balance` | 教材级图例、caption、经典 `IB = A + B` glossary 图例、`CBOT handbook` 原始体系线索与教材扫描页级入口证据包 | `strong_chart_bundle` | `active` | 已补图示型证据、经典 glossary 线索与教材扫描页入口，仍缺更完整原始教材图示或源码实现层 |

## 当前说明

- 这个批次已从“只有历史回收摘录”推进到“历史回收 + 相邻平台页 + 同主题 Initial Balance 页 + 结构化公式摘录页 + acceptance/extension/statistics 强证据引文包 + 教材级图例证据包 + 经典 glossary 图例/handbook 线索 + 教材扫描页级入口”。
- 当前仍不冒充已经拿到源码级证据。
