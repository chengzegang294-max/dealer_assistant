# AG Pro ATR Compression Map 手动网页摘录

更新时间：2026-07-14

## 文件类型

- `ARTIFACT`

## 原路径

- `https://www.tradingview.com/script/nCbbDHVD-AG-Pro-ATR-Compression-Map-AGPro-Series/`
- `https://www.tradingview.com/u/AGProLabs/#published-scripts`
- `https://www.sorafutures.com/archives/42281`

## 新路径

- `batch_146/00_raw_snapshot/AG_Pro_ATR_Compression_Map__manual_web_capture__20260713.md`

## 生成入口

- `manual_webpage_capture`

## 适用对象

- `Batch9 N01 AG Pro`

## 当前作用

- 补强 `AG Pro ATR Compression Map` 的原作者页正文、参数位与四因子说明。
- 为压缩质量分阶段口径提供可追溯页面证据。

## 证据强度

- `manual_webpage_capture`

## 状态

- `active`

## 边界说明

- 当前主来源已经升级为 `TradingView` 原始开源脚本页。
- `sorafutures` 当前只保留为次级补充页，不再作为主来源。
- 因而当前已可作为：
  - `definition_page`
  - `regime_interpretation`
  - 一部分 `parameter_panel`
- 当前不冒充：
  - 核心源码硬证据

## 网页正文摘录

- 页面头部：
  - `OPEN-SOURCE SCRIPT`
  - `AG Pro ATR Compression Map [AGPro Series]`
  - `Source code`
  - `View in Pine Editor・709 lines`
- 作者归属：
  - `AGPro Series`
  - `AGProLabs` 作者页自述：`Public AGPro Series + advanced invite-only workflows`
- 页面说明：
  - `chart-first compression analysis tool designed to evaluate how organized a low-volatility phase is and how structurally developed that contraction has become`
  - `It does not attempt to forecast direction, guarantee expansion, or replace execution planning and risk management.`
- 四个组成因子：
  - `ATR contraction`
  - `Range tightness`
  - `Noise evaluation`
  - `Containment structure`
- 分数与阶段：
  - `normalized compression score`
  - `Loose`
  - `Building`
  - `Tight`
  - `Mature`
- 关键输入项：
  - `ATR Length`
  - `Baseline Length`
  - `Range Window`
  - `Noise Window`
  - `Containment Window`
  - `Compression Threshold`
  - `Mature Threshold`
- mini panel 字段：
  - `ATR state`
  - `range state`
  - `noise condition`
  - `containment quality`
  - `overall compression score`
  - `active state`
  - `current compression window length`
- 告警语义：
  - `Compression Active`
  - `Compression Mature`
  - `Compression State Change`

## 源码页可见摘录

- 源码可见性：
  - `Source code`
  - `View in Pine Editor・709 lines`
- 源码首屏可见行：
  - `// ATR Compression Map [AGPro Series]`
  - `// Author  : AGProLabs | AGPro Series`
  - `// Version : 2.1`
  - `//@version=6`
  - `indicator("ATR Compression Map [AGPro Series]",`
  - `shorttitle = "AG Pro ATR",`
  - `overlay = true,`
  - `max_labels_count = 220,`
  - `max_lines_count = 220,`
  - `max_boxes_count = 120)`
- 分组与输入区块首屏可见词：
  - `Inputs`
  - `Core Engine`
  - `Scoring`
  - `Compression Pocket`
  - `Visuals`
  - `Panel`
  - `Alerts`
  - `ATR Length`

## 当前可确认的最小计算口径

- `compression_score`
  - 范围 `0-100`
- 四个子维度：
  - `atr_contraction`
  - `range_tightness`
  - `noise_level`
  - `containment_quality`
- 当前阶段枚举：
  - `Loose`
  - `Building`
  - `Tight`
  - `Mature`
- 当前输入窗口骨架：
  - `atr_length`
  - `baseline_length`
  - `range_window`
  - `noise_window`
  - `containment_window`
- 当前阈值骨架：
  - `compression_threshold`
  - `mature_threshold`

## 对 N01 的当前可用价值

- 可补：
  - `definition_page`
  - `regime_interpretation`
  - `parameter_panel`
  - 一部分 `source_code_snippet`
  - 压缩质量四因子与四阶段枚举
- 当前仍缺：
  - 四因子的更完整源码公式
  - 子分数权重与具体阈值的源码证据
  - 更完整 Pine 源码正文

## 缺口

- 仍需后续补：
  - 更完整 Pine 源码正文
  - 参数面板截图或更细默认值证据
