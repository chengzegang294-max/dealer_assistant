# Batch 146 Artifact Index v1

更新时间：2026-07-15

## 当前批次产物

| 文件类型 | 原路径/来源 | 新路径 | 生成入口 | 适用对象 | 当前作用 | 证据强度 | 状态 | 缺口 |
|---|---|---|---|---|---|---|---|---|
| `INDEX_NOTE` | `batch_146/README.md` | `batch_146/README.md` | `manual_batch_setup` | `Batch9 N01 GainzAlgo / AG Pro` | 批次入口 | `hard` | `active` | 无 |
| `INDEX_NOTE` | `batch_146/provenance.md` | `batch_146/provenance.md` | `manual_batch_setup` | `Batch9 N01 GainzAlgo / AG Pro` | 来源追溯说明 | `hard` | `active` | 无 |
| `INDEX_NOTE` | `batch_146/N01_EVIDENCE_GAP_STATUS_v1.tsv` | `batch_146/N01_EVIDENCE_GAP_STATUS_v1.tsv` | `manual_batch_setup` | `Batch9 N01 GainzAlgo / AG Pro` | 证据缺口清单 | `hard` | `active` | 需实际证据文件 |
| `ARTIFACT` | `Volatility_Regimes__GainzAlgo__page_excerpt.md` 历史回收 | `batch_146/00_raw_snapshot/Volatility_Regimes__GainzAlgo__historical_recovered_excerpt.md` | `historical_recovered_excerpt` | `Batch9 N01 GainzAlgo` | 定义页与参数区证据 | `historical_recovered` | `active` | 仍缺原脚本源码页 |
| `ARTIFACT` | `AG_Pro_ATR_Compression_Map__page_excerpt.md` 历史回收 | `batch_146/00_raw_snapshot/AG_Pro_ATR_Compression_Map__historical_recovered_excerpt.md` | `historical_recovered_excerpt` | `Batch9 N01 AG Pro` | 参数面板与状态枚举证据 | `historical_recovered` | `active` | 仍缺核心计算段源码 |
| `ARTIFACT` | `https://www.tradingview.com/script/2z7JVYdK-Volatility-Regimes-GainzAlgo/` | `batch_146/00_raw_snapshot/Volatility_Regimes__GainzAlgo__manual_web_capture__20260713.md` | `manual_webpage_capture` | `Batch9 N01 GainzAlgo` | 原作者页正文、详细 calculation methodology、ATR Bands、Stop/TP/Position Size、源码首屏与 visual inputs 口径 | `manual_webpage_capture` | `active` | 已见源码首屏，但仍缺更完整 Pine 代码段 |
| `ARTIFACT` | `https://www.tradingview.com/script/nCbbDHVD-AG-Pro-ATR-Compression-Map-AGPro-Series/ + https://www.tradingview.com/u/AGProLabs/#published-scripts + https://www.sorafutures.com/archives/42281` | `batch_146/00_raw_snapshot/AG_Pro_ATR_Compression_Map__manual_web_capture__20260713.md` | `manual_webpage_capture` | `Batch9 N01 AG Pro` | 原作者页正文、四因子、compression score、四阶段、key inputs、mini panel 字段与源码首屏 | `manual_webpage_capture` | `active` | 已见源码首屏，但仍缺更完整 Pine 代码段 |
| `ARTIFACT` | `GainzAlgo + AG Pro exact TradingView source capture` | `batch_146/00_raw_snapshot/N01_source_code_and_parameter_defaults_bundle__20260714.md` | `manual_source_capture` | `Batch9 N01 GainzAlgo / AG Pro` | 双原作者页源码首屏、默认值、参数分组与 tooltip 级默认意图证据包 | `near_hard_evidence` | `active` | 已把源码首屏与默认值正式归档，仍缺更完整 Pine 代码段 |
| `ARTIFACT` | `N01 source bundle -> parameter normalization` | `batch_146/00_raw_snapshot/N01_parameter_dictionary_v1.tsv` | `manual_parameter_normalization` | `Batch9 N01 GainzAlgo / AG Pro` | 参数字典表：变量名、界面名、默认值、范围、证据等级 | `near_hard_evidence` | `active` | 已可直接支撑后续对象卡/合同映射，仍缺更完整 Pine 代码段 |
| `ARTIFACT` | `N01 exact TradingView source logic capture` | `batch_146/00_raw_snapshot/N01_source_logic_excerpt_bundle__20260714.md` | `manual_source_capture` | `Batch9 N01 GainzAlgo / AG Pro` | 源码逻辑摘录包：阈值、状态判断、风险/TP、告警与 proof 统计逻辑 | `near_hard_evidence` | `active` | 已进入源码逻辑层，仍缺更完整连续 Pine 代码段 |
| `ARTIFACT` | `https://www.tradingview.com/script/XJmX3p98-Trading-Suite-AGPro-Series/` | `batch_146/00_raw_snapshot/AGPro_family_invite_only_access_note__20260715.md` | `manual_browser_probe` | `Batch9 N01 AG Pro family` | `AGProLabs` invite-only 访问边界、`Source code disabled` 状态与默认值型参数位说明 | `boundary_evidence` | `active` | 已解释一部分源码缺口原因，但不能替代 `AG Pro ATR Compression Map` 核心计算源码 |
| `ARTIFACT` | `GainzAlgo/AG Pro 历史摘录 + 手动网页正文` | `batch_146/00_raw_snapshot/n01_formula_snippets.md` | `manual_excerpt_capture` | `Batch9 N01 GainzAlgo / AG Pro` | ATR ratio、regime 切换、压缩四因子与阈值参考的结构化摘录 | `weak_evidence` | `active` | 已有半硬证据页，仍需更硬源码输入输出 |

## 当前说明

- 这个批次已从“只有历史回收摘录”推进到“历史回收 + GainzAlgo/AG Pro 原作者页详细网页正文 + 源码首屏 + 参数默认值证据包 + 参数字典表 + 源码逻辑摘录包 + 结构化公式摘录页 + AGPro family invite-only 边界证据”。
- 当前仍不冒充已经拿到源码级证据。
