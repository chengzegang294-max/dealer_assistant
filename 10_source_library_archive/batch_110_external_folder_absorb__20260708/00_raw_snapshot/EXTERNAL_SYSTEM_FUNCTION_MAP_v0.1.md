# 外部交易系统功能层对比表 v0.1

## 说明

- 本表把外部知名交易体系按 **功能层** 拆解，不评价优劣，只记录各体系在不同层用什么方法。
- 功能层定义：
  - **结构层**：判断趋势/方向/状态（用什么定方向）
  - **能量层**：过滤/确认/波动率（用什么说"现在可以交易"）
  - **执行层**：入场触发（用什么说"现在做"）
  - **风控层**：止损/仓位/极端状态（用什么保命）
- 最后一列标注 **与你现有指标的映射**。

---

## 方向1：多周期 + 波动率过滤

### 1. ICT (Inner Circle Trader) — Michael J. Huddleston

| 维度 | 内容 |
|------|------|
| **体系名** | ICT (Inner Circle Trader) |
| **结构层** | Market Structure：Higher High/Low = 多头结构；Lower High/Low = 空头结构。Change of Character (CHoCH) 标记结构翻转。多周期对齐：HTF 定方向，ITF 定结构，LTF 找入场。 |
| **能量层** | Liquidity Engineering：识别流动性池（equal highs/lows, stop hunts），在流动性被清扫后寻找反转。Kill Zone：时间窗口过滤（伦敦 2-5AM EST, 纽约 8-11AM EST）。 |
| **执行层** | Order Block + Fair Value Gap (FVG)：价格回测 Order Block 区域时入场。Optimal Trade Entry (OTE)：用 Fibonacci 0.62-0.79 区做精确入场。 |
| **风控层** | 结构失效点为硬止损（CHoCH 确认点外侧）。Inducement 概念：识别"诱导陷阱"，避免被扫止损。 |
| **适合市场** | 外汇、指数、加密货币、大市值股票 |
| **时间框架** | 日线/4H 定结构，1H/15M 执行 |
| **成熟度** | 社区级（YouTube 免费内容极多，但主观元素强） |
| **与你现有指标映射** | `KD MTF P0` 的 `kd_alignment_tier = s` ↔ HTF/ITF/LTF 结构对齐；`Volty` 的 `tight` ↔ 低波动压缩期（常有突破前奏）；`XBreaking` 占位 ↔ Liquidity Sweep 后的结构突破 |

### 2. Adam Grimes — The Art and Science of Technical Analysis

| 维度 | 内容 |
|------|------|
| **体系名** | Adam Grimes Price Action System |
| **结构层** | 市场结构分析：趋势、震荡、反转三态。用价格行为（高低点结构）而非指标定方向。强调 "market structure first"。 |
| **能量层** | 波动率分析：用 ATR 和波动率百分位判断当前是"正常波动"还是"极端波动"。在极端波动后等待收敛。 |
| **执行层** | 结构突破 + 回测确认：不追突破，等回测结构位后入场。多时间框架精细执行：大周期定方向，小周期等结构。 |
| **风控层** | 结构止损：止损放在结构失效点（前高/前低外侧）。仓位按波动率缩放：高波动 = 小仓位。 |
| **适合市场** | 外汇、期货、股票、加密货币 |
| **时间框架** | 日线/4H 结构，1H/30M 执行 |
| **成熟度** | 半学术级（有书，有量化研究，但执行层面偏主观） |
| **与你现有指标映射** | `KD MTF P0` 的结构判定 ↔ Grimes 的 "market structure first"；`Volty` 的 ATR 通道 ↔ Grimes 的波动率分析；`PV Corr` 的确认/背离 ↔ Grimes 的"量价验证" |

### 3. Andreas Clenow — Following the Trend

| 维度 | 内容 |
|------|------|
| **体系名** | Clenow Trend Following |
| **结构层** | 多资产趋势跟踪：用 100 日/200 日高点突破 + 移动平均斜率确认趋势。跨资产分散，不预测单一市场。 |
| **能量层** | ATR 波动率过滤：用 ATR 计算仓位大小（risk per trade = fixed % / ATR）。波动率越高，仓位越小。Trendless = 不交易。 |
| **执行层** | 突破入场：价格突破 N 日高点 → 做多；突破 N 日低点 → 做空。无"回测等确认"，纯突破触发。 |
| **风控层** | ATR-based 止损：止损 = entry - 2×ATR（多头）。最大回撤控制：portfolio-level drawdown limit。定期再平衡。 |
| **适合市场** | 期货、股票、多资产组合 |
| **时间框架** | 日线为主（月频再平衡） |
| **成熟度** | 学术级（有书，有回测，有论文引用，机构化实现） |
| **与你现有指标映射** | `Volty` 的 `stop_distance_atr` ↔ Clenow 的 ATR 仓位缩放；`RSJ` 的 `risk_on/risk_off` ↔ Clenow 的 trendless 过滤；`KD MTF` 的方向 ↔ Clenow 的 MA 斜率趋势确认 |

### 4. Rob Hoffman — Hoffman System Indicator

| 维度 | 内容 |
|------|------|
| **体系名** | Hoffman System |
| **结构层** | 趋势检测：内置移动平均 + 结构逻辑判断主导方向。多品种多周期同时扫描。 |
| **能量层** | 动量确认：检查买卖压力强度后才发信号。波动率过滤器：自动过滤低成交量/横盘市场。 |
| **执行层** | 箭头信号： buy/sell 箭头直接标在图表上。趋势+动量对齐时才出信号。 |
| **风控层** | 参数可调的止损/止盈。实时警报（弹窗/邮件/推送）。 |
| **适合市场** | 外汇、黄金、指数、加密货币 |
| **时间框架** | M1-MN 全周期，推荐 M15-H4 |
| **成熟度** | 工具级（MT4 指标，社区传播，非公开方法论） |
| **与你现有指标映射** | `KD MTF` 的方向判定 ↔ Hoffman 的 trend detection；`Volty` 的波动率过滤 ↔ Hoffman 的 volatility filter；`XBreaking` 的箭头信号 ↔ Hoffman 的 buy/sell arrows |

---

## 方向2：价量 + 结构突破

### 5. Al Brooks — Price Action Trading

| 维度 | 内容 |
|------|------|
| **体系名** | Al Brooks Price Action |
| **结构层** | 三态框架：Trends / Trading Ranges / Reversals。Always In 偏向：当前市场更可能是多还是空。用 bar-by-bar 分析读结构。 |
| **能量层** | 成交量确认：突破时必须有成交量配合。Bar 质量：大阳线/大阴线 = 强能量；小十字星 = 弱能量/犹豫。 |
| **执行层** | 主要 setup：High 2 / Low 2 Pullback（趋势中的两浪回调）、Breakout Pullback（突破后回测）、Failed Breakout（假突破反转）。Limit order on pullback（不在突破时追，等回测）。 |
| **风控层** | 结构止损：止损放在 pullback low/high 外侧。 scalp 目标小，swing 目标大。部分平仓：先出一部分，余仓追趋势。 |
| **适合市场** | 外汇、期货、股票、加密货币 |
| **时间框架** | 5M-日线（ Brooks 本人用 5M） |
| **成熟度** | 半学术级（三本书极其详细，但主观元素强，无固定参数） |
| **与你现有指标映射** | `KD MTF` 的 `alignment_tier` ↔ Brooks 的 "Always In" 偏向；`XBreaking` 的占位 ↔ Brooks 的 Breakout Pullback / Failed Breakout；`PV Corr` 的 `confirm` ↔ Brooks 的 volume confirmation；`Volty` 的 stop ↔ Brooks 的 结构止损 |

### 6. Lance Beggs (YTC) — YTC Price Action Trader

| 维度 | 内容 |
|------|------|
| **体系名** | YTC Price Action Trader |
| **结构层** | 三周期框架：Higher Timeframe (HTF) 定方向，Trading Timeframe (TF) 找 setup，Lower Timeframe (LF) 精细入场。Support/Resistance Framework：用 S/R 区定义交易框架。 |
| **能量层** | 订单流分析：读" trapped trader "（陷阱交易者）的位置。能量在 S/R 边界处：突破前的犹豫 = 能量积累；突破后的跟进 = 能量释放。 |
| **执行层** | 五类 setup：TST（测试 S/R，预期守住）、BOF（突破失败，反转）、BPB（突破回测，延续）、PB（简单回调）、CPB（复杂回调）。Wholesale entry：在"批发价"入场（早期），不在"零售价"追（晚期）。 |
| **风控层** | T1/T2 目标：T1 是下一级 S/R，T2 是更高级 S/R。初始止损放在 setup 结构外侧。Scatch trade（打平出场）：价格不按预期走时提前退出。 |
| **适合市场** | 外汇、期货（6B GBP/USD 为示例） |
| **时间框架** | 30M/3M/1M（三周期固定） |
| **成熟度** | 社区级（有付费课程，方法论清晰但依赖大量主观判断） |
| **与你现有指标映射** | `KD MTF P0` 的三周期 ↔ YTC 的 HTF/TF/LF；`XBreaking` 的占位 ↔ YTC 的 BOF/BPB 确认点；`Volty` 的通道 ↔ YTC 的 S/R Framework 边界；`RSJ` 的极端 ↔ YTC 的 "exhaustion" 信号 |

### 7. Mentfx — Liquidity + Structure

| 维度 | 内容 |
|------|------|
| **体系名** | Mentfx Structure System |
| **结构层** | Structure Indicator：识别 protected highs/lows，标记结构翻转。Reaccumulation / Redistribution 模型。 |
| **能量层** | Liquidity Clouds：流动性云/池概念，识别大玩家可能扫止损的位置。Rule of 30：多周期对齐规则（当前周期 × 30 = 上级参考周期）。 |
| **执行层** | 结构突破后回测入场：等价格突破结构后回测 Order Block 或 FVG 区域。 |
| **风控层** | 结构失效止损。流动性云外侧为硬边界。 |
| **适合市场** | 外汇、加密货币 |
| **时间框架** | 4H/1H/15M |
| **成熟度** | 社区级（YouTube 内容，有 workbook，偏 ICT 变体） |
| **与你现有指标映射** | `KD MTF` 的结构 ↔ Mentfx 的 Structure Indicator；`XBreaking` 的占位 ↔ Mentfx 的结构突破确认；`Volty` 的 tight ↔ Mentfx 的"结构压缩期" |

---

## 方向3：系统化 / 量化波段

### 8. Meb Faber — GTAA / Ivy Portfolio / Trend Following

| 维度 | 内容 |
|------|------|
| **体系名** | Faber Tactical Asset Allocation |
| **结构层** | 简单 SMA 趋势过滤：价格 > 10 月 SMA = 多头；价格 < 10 月 SMA = 空仓/现金。多资产排名：按 1/3/6/12 月动量排名，选 top N。 |
| **能量层** | 波动率控制：不直接交易高波动资产，而是按波动率缩放仓位。Cash 机制：趋势向下时转现金（BIL），不是做空。 |
| **执行层** | 月频再平衡：每月最后交易日检查信号，收盘价执行。无盘中决策，纯系统化。 |
| **风控层** | 最大回撤控制：历史最大回撤约 -16.8%（vs buy-hold -50.95%）。分散化：5-13 个资产类别，等权或风险平价。 |
| **适合市场** | 股票、债券、REITs、商品、国际股票（ETF） |
| **时间框架** | 月线（月频再平衡） |
| **成熟度** | 学术级（2007 年论文，40 年回测，被广泛引用，有 ETF 产品） |
| **与你现有指标映射** | `KD MTF` 的 week/day 方向 ↔ Faber 的 SMA 趋势过滤；`RSJ` 的 `risk_off` ↔ Faber 的 cash 机制；`Volty` 的 ATR ↔ Faber 的波动率缩放；你的 S_BUCKET 多因子 ↔ Faber 的动量排名 |

### 9. Kris Verma — Statistical Edge + Kelly Criterion

| 维度 | 内容 |
|------|------|
| **体系名** | Kris Verma Systematic Day Trading |
| **结构层** | A+ Setup 定义：Day 2 Short into Resistance（特定形态的概率优势）。统计优势：基于历史数据回测的"优势期"识别。 |
| **能量层** | 波动率状态：等待波动率从压缩到扩张的转换点。Liquidity Traps：识别流动性陷阱后的高概率窗口。 |
| **执行层** | 精确入场：在统计优势窗口内，按预定价格触发。Shorting overextended small-cap：做空过度延伸的小盘股。 |
| **风控层** | Kelly Criterion 仓位管理：按统计优势大小计算最优仓位。Trading Database Template：每单记录，持续回测修正。宽止损 + 结构化交易管理。 |
| **适合市场** | 小盘股、外汇（日内） |
| **时间框架** | 日内（Day 2 setup） |
| **成熟度** | 社区级（ podcast 访谈，个人经验，统计方法但样本量未公开） |
| **与你现有指标映射** | `RSJ` 的 `warm/cold` ↔ Verma 的"优势期/非优势期"；`Volty` 的仓位缩放 ↔ Verma 的 Kelly Criterion；你的 `indicator_audit` 框架 ↔ Verma 的 Trading Database Template |

---

## 方向4：市场轮廓 / 拍卖理论

### 10. Jim Dalton — Market Profile / Auction Market Theory

| 维度 | 内容 |
|------|------|
| **体系名** | Jim Dalton Market Profile |
| **结构层** | Market Profile Structure：TPO 分布图（时间-价格机会），识别 bell curve / skewed / elongated / P-shaped / B-shaped。Day Type：趋势日、震荡日、 neutral day、 double distribution。 |
| **能量层** | Value Area (VA)：70% 交易活动区，是"公平价值"区。POC (Point of Control)：最大成交量/时间的价格，是"磁力点"。HVN/LVN：高/低成交量节点，HVN = 支撑/阻力，LVN = 突破加速器。 |
| **执行层** | 80% Rule：价格进入 VA 并在两个连续 TPO（60分钟）内守住，有 80% 概率走到 VA 另一侧。Initial Balance (IB) 反转：价格延伸出 IB 后返回内部，向 POC 反转概率高。POC Fade：价格远离 POC 后回归。 |
| **风控层** | VAH/VAL 作为动态支撑/阻力：止损放在 VA 外侧。Excess/Tails：长影线 = 拒绝，是反向信号。 |
| **适合市场** | 期货（ES, NQ, CL, GC）、外汇（需 tick volume 代理） |
| **时间框架** | 日级别（30分钟 TPO），也可做 intraday session profile |
| **成熟度** | 半学术级（有经典著作，机构广泛使用，但 TPO 数据需特殊软件） |
| **与你现有指标映射** | 你的 A2 CUTPACK（市场轮廓理论）↔ Dalton 的完整框架；`KD MTF` 的 `week_extreme_zone` ↔ Dalton 的 Value Area 极端；`Volty` 的通道 ↔ Dalton 的 VAH/VAL；`PV Corr` 的 HVN ↔ Volume Profile 的高成交量节点；`XBreaking` 的占位 ↔ 80% Rule 的突破确认 |

---

## 方向5：多周期通用框架

### 11. Multiple Time Frame Trading (通用方法论)

| 维度 | 内容 |
|------|------|
| **体系名** | Multiple Time Frame Confluence |
| **结构层** | 三周期对齐：大周期定方向（日线），中周期定结构（4H），小周期执行（1H/30M）。各周期指标共振时才交易。 |
| **能量层** | Confluence 确认：多个交易基础（S/R, Fib, Trend Line, Pivot, Stochastic, Bollinger, Divergence）在同一方向共振。 |
| **执行层** | 大周期信息 → 小周期精细入场：用更小的止损换取更大的 R:R。 |
| **风控层** | 典型止损 10-20 pips，目标 20-30 pips，R:R 约 1:1.5。 |
| **适合市场** | 外汇（EURUSD 为主） |
| **时间框架** | 日线/4H/1H |
| **成熟度** | 方法论级（通用原则，非特定体系） |
| **与你现有指标映射** | `KD MTF P0` 就是此框架的"Stochastic"组件；`Volty` 的 ATR 可替代 Confluence 中的 ATR；你的完整指标组合可以拼出此框架 |

---

## 总结：外部体系 vs 你现有资产的覆盖缺口

| 功能层 | 外部体系已覆盖 | 你现有资产 | 缺口 |
|--------|---------------|----------|------|
| **结构层** | ICT 多周期结构、Al Brooks 三态、YTC S/R 框架、Dalton Market Profile、Faber SMA 趋势 | `KD MTF P0`（6 字段已冻结） | ✅ 基本覆盖，但缺"日内结构"（IB/VA/POC）字段化 |
| **能量层** | Clenow ATR 仓位、Faber 波动率缩放、Verma 统计优势、Brooks bar 质量 | `Volty`（ATR 通道）、`PV Corr`（价量确认） | ✅ 基本覆盖，但缺"成交量分布"（HVN/LVN）字段化 |
| **执行层** | ICT Order Block/FVG、Brooks H2/L2/BPB、YTC TST/BOF/BPB、Dalton 80% Rule | `XBreaking`（NEED_PROBE） | ❌ 严重不足，XBreaking 未确认，且缺"回测入场"字段化 |
| **风控层** | Clenow ATR 止损、Faber 现金机制/分散、Verma Kelly、YTC scratch trade | `Volty Stop`（动态止损）、`RSJ`（情绪极端） | ✅ 部分覆盖，但缺"portfolio-level drawdown control" |
| **审计层** | Clenow 回测、Verma Trading Database | `indicator_audit`（历史回测产物） | ✅ 已有框架，但缺系统化整合 |

---


## 版本记录

- v0.1 (2026-07-06): 初版，覆盖 11 个外部体系，按功能层拆解
- v0.2 (2026-07-06): 整合 GLM 搜索结果，新增 12 个体系，覆盖经典量价、中文哲学、量化策略、风控专门体系
- 来源：kimi_search_v2 多轮搜索 + 仓库内部已有文件交叉验证 + GLM 补充搜索


## 方向6：经典量价 / 机构行为（GLM 补充）

### 12. Wyckoff Method — Richard D. Wyckoff

| 维度 | 内容 |
|------|------|
| **体系名** | 威科夫方法论 |
| **结构层** | **市场周期与图式**：基于"因果定律"，通过**积累-上涨-派发-下跌**的循环判断大方向。使用**Spring（弹簧）**和**Upthrust（上冲）**作为结构性拐点信号。结合**Composite Man（综合人）**概念，通过价格波动的阶段特征（Automatic Rally, Secondary Test）定位当前处于周期的哪个位置。 |
| **能量层** | **努力与结果**：核心在于**成交量(Volume)**与价格的背离。如果出现巨大的成交量（努力）但价格移动很小（无结果），通常预示反转。使用**Wyckoff Wave**（一种自定义的价格合成指标）配合**Force/Energy**（动力/能量）指标来确认趋势强弱。 |
| **执行层** | **Jump Across the Creek (跳过小溪)** 或 **Back Up to the Edge of the Creek (回踩溪边)**。在确认积累末期（Sign of Strength, SOS）后，在回调至支撑位（Creek）或突破阻力位时入场。通常是右侧交易，等待明确的Spring或SOS信号。 |
| **风控层** | **结构失效止损**：如果Spring失败（价格跌破Spring的低点）或Upthrust被超越，立即判定结构无效并离场。不使用固定百分比止损，而是依据**结构边界**（如交易区间的极值点）设置止损。 |
| **适合市场** | 股票 / 期货 / 外汇 |
| **时间框架** | 日线 / 周线 / 日内（针对VSA变体） |
| **成熟度** | 学术级/经典级（百年历史，大量文献支持） |
| **核心参考来源** | 书籍：《Studies in Tape Reading》/《The Richard D. Wyckoff Method Of Stock Market Science》<br>网站：[StockCharts - Wyckoff](https://school.stockcharts.com/doku.php?id=market_analysis:wyckoff_method) |
| **与你现有指标映射** | `PV Corr` 的价量背离 ↔ Wyckoff 的"努力与结果"；`KD MTF` 的结构 ↔ Wyckoff 的积累/派发周期；`XBreaking` 的占位 ↔ Spring/Upthrust 的突破确认 |

---

### 13. 缠论 — 缠中说禅

| 维度 | 内容 |
|------|------|
| **体系名** | 市场几何动力学 |
| **结构层** | **分型-笔-线段-中枢**：这是完全不同于西方K线形态的独特结构。通过**顶底分型**定义最小单元，连接成**笔**，重叠形成**中枢（盘整区间）**。趋势定义为"没有中枢产生的新高低"，震荡定义为"中枢的延伸"。利用**第三类买卖点（3-Buy/Sell）**确认脱离中枢的趋势启动。 |
| **能量层** | **背驰**：利用**MACD**辅助判断动能衰竭。当价格创新高/新低，但MACD面积（柱状图面积）缩小，即构成背驰。这是缠论的核心能量确认机制，用于判断当前趋势力度的衰减。 |
| **执行层** | **三类买卖点**：<br>1. 第一类点：背驰点（拐点）；<br>2. 第二类点：回抽不破前低/高；<br>3. 第三类点：回抽不进入中枢（最强切入点）。<br>通常采用**分笔成交**或**挂单**方式捕捉精确点位。 |
| **风控层** | **分类讨论与中枢破坏**：严格依据走势类型。例如，对于日线级别的操作，一旦次级别（如30分）走势破坏了当前的结构（如形成反向的中枢或笔），则触发退出机制。强调"当下"的客观应对，而非预测。 |
| **适合市场** | A股 / 期货 / 加密货币（流动性好的品种） |
| **时间框架** | 多级别联立（1分-5分-30分-日线递归） |
| **成熟度** | 社区级/半学术级（逻辑严密，但主要流传于中文圈） |
| **核心参考来源** | 博客：《教你炒股票》108课<br>书籍：《缠中说禅详解》<br>URL：[Blog Original Archive](http://blog.sina.com.cn/chzhshch) |
| **与你现有指标映射** | `KD MTF P0` 的多周期 ↔ 缠论的多级别联立；`KD MTF` 的 `kd_alignment_tier` ↔ 缠论的走势类型分类；`PV Corr` 的背离 ↔ 缠论的背驰；`XBreaking` 的占位 ↔ 第三类买卖点确认 |

---

## 方向7：经典量化策略（GLM 补充）

### 14. Turtle Trading System — Richard Dennis & William Eckhardt

| 维度 | 内容 |
|------|------|
| **体系名** | 海龟交易法则 |
| **结构层** | **唐奇安通道突破**：这是最纯粹的趋势跟踪系统。当价格突破过去 **20日（入局）** 高点时视为上升趋势开始；突破 **10日（离场）** 低点时视为趋势结束。不预测市场状态，只对突破做出反应。系统分为 System 1（入场系统）和 System 2（更灵敏的突破系统）。 |
| **能量层** | **ATR 波动率归一化**：虽然不直接用指标过滤"假突破"，但使用 **ATR (Average True Range)** 来衡量市场的波动能量。单位头寸的大小由 ATR 决定（1 Unit = Account 1% / ATR），确保在高波动市场中减少暴露，低波动中增加暴露。 |
| **执行层** | **突破挂单**：在前一日最高价上方一点设置 Buy Stop，或在最低价下方设置 Sell Stop。一旦触及即进场。不加主观判断，机械执行。 |
| **风控层** | **N倍止损与仓位金字塔**：<br>1. 止损：入场价减去 **2x ATR**。<br>2. 加仓：每盈利 0.5 ATR 加仓一次（最多4个Unit）。<br>3. 限仓：单个市场最大风险不超过账户 2%，高度相关市场总风险不超过 6%。 |
| **适合市场** | 期货 / 外汇 / 趋势性强的加密货币 |
| **时间框架** | 日线 |
| **成熟度** | 半学术级（有完整的历史回测数据公开） |
| **核心参考来源** | 书籍：《Way of the Turtle》(Curtis Faith)<br>Wiki：[Original Turtle Trading Rules](https://www.originalturtles.org/) |
| **与你现有指标映射** | `Volty` 的 ATR 通道 ↔ Turtle 的 ATR 仓位缩放；`Volty Stop` ↔ Turtle 的 2x ATR 止损；`XBreaking` 的占位 ↔ Turtle 的唐奇安通道突破；`KD MTF` 的方向 ↔ Turtle 的趋势确认 |

---

### 15. Dual Momentum (GEM) — Gary Antonacci

| 维度 | 内容 |
|------|------|
| **体系名** | 双动量模型 |
| **结构层** | **绝对动量 + 相对动量的结合**：<br>1. **相对动量**：在风险资产（如美股）之间比较，选最强的（跑赢大盘的）。<br>2. **绝对动量**：将胜出的风险资产与无风险资产（如国债）比较，若风险资产过去12个月回报率为正则持有，否则切换至债券。这解决了传统动量策略在熊市中回撤过大的问题。 |
| **能量层** | **月度收益率截面**：不看复杂的指标，只看过去 **1、3、6、12个月** 的加权复合收益率。这是一种基于时间序列的能量度量，确认资产是否处于正向反馈循环中。 |
| **执行层** | **月度再平衡**：每月最后一天计算信号。如果信号变化（如从股票切到债券），则在下一个交易日开盘执行调仓。属于低频、低成本执行。 |
| **风控层** | **防御性资产配置**：其核心风控就是"离场"。当绝对动量为负时，系统强制持有债券，从而规避了股市崩盘的风险。不需要传统的止损单，而是通过资产类别的切换来实现风控。 |
| **适合市场** | 全球股票 / 债券 / 多资产组合 |
| **时间框架** | 月线 |
| **成熟度** | 学术级（有大量学术论文支撑，如Jegadeesh & Titman） |
| **核心参考来源** | 书籍：《Dual Momentum Investing: An Innovative Strategy for Higher Returns with Lower Risk》<br>论文：[Momentum Factor Research](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3012275) |
| **与你现有指标映射** | 你的 S_BUCKET 多因子 ↔ Dual Momentum 的相对动量排名；`RSJ` 的 `risk_on/risk_off` ↔ Dual Momentum 的绝对动量开关；`KD MTF` 的 week/day 方向 ↔ 相对动量确认 |

---

### 16. Fama-French Multi-Factor Model — Eugene Fama & Kenneth French

| 维度 | 内容 |
|------|------|
| **体系名** | 法玛-弗兰奇多因子模型 |
| **结构层** | **因子暴露**：不预测价格走势，而是根据资产的**统计学特征**进行分类。核心因子包括：<br>1. **Market (Beta)**：市场风险。<br>2. **SMB (Small Minus Big)**：市值因子（小盘股效应）。<br>3. **HML (High Minus Low)**：价值因子（账面市值比）。<br>4. **Momentum (UMD)**：动量因子（后续加入）。 |
| **能量层** | **风险溢价**：这里的"能量"是长期的**预期超额回报**。通过历史回测证明，承担"小市值"或"价值"风险应该获得超过市场平均的回报。能量体现在因子的**Z-Score**（偏离均值程度）上，用于择时（如价值因子极度高估时减配）。 |
| **执行层** | **组合构建与再平衡**：通常按季度或年度进行。剔除流动性差的股票，按因子得分排名，做多排名靠前的（如Top 20% Value Stocks），做空或规避排名靠后的。 |
| **风控层** | **行业中性化与波动率控制**：防止在某些单一行业（如银行）过度集中。限制组合的整体 Beta 接近 1（如果是纯 Alpha 策略则为 0）。利用 **Barra Risk Model** 进行归因分析，控制特异性风险。 |
| **适合市场** | 全球股票市场 / 跨资产 |
| **时间框架** | 月线 / 季度 / 长期持有 |
| **成熟度** | 学术级（诺贝尔奖级别理论，金融学基石） |
| **核心参考来源** | 论文："Common risk factors in the returns on stocks and bonds"<br>数据库：[French Data Library](http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) |
| **与你现有指标映射** | 你的 S_BUCKET 多因子库 ↔ Fama-French 的因子体系；`KD MTF` 的动量确认 ↔ Momentum 因子；`RSJ` 的极端 ↔ 风格因子 Z-Score 偏离 |

---

## 方向8：供需 / 订单流（GLM 补充）

### 17. Supply and Demand (Sam Seiden) — Sam Seiden / Online Trading Academy

| 维度 | 内容 |
|------|------|
| **体系名** | 供需交易法 |
| **结构层** | **机构订单痕迹**：寻找价格图表上的**不平衡 Imbalance**（即剧烈的离开某区域的K线，中间留有缺口或影线极少）。这些区域被称为供应区（Sell Zone）或需求区（Buy Zone）。趋势由更高的高点和更高的低点定义，但在特定的供需区才值得交易。 |
| **能量层** | ** Odds Enhancers (赔率增强器)**：<br>1. 离开该区域的速度越快、K线越剧烈，该区域越强。<br>2. 首次回调至该区域（Fresh level）比第二次有效。<br>3. 必须结合趋势方向（只在趋势的回撤中交易）。 |
| **执行层** | **限价单入场**：在供应区的上限卖出，在下限买入。不等待确认K线（这与ICT不同），假设价格回到该区域会被反弹。或者使用 **Zone Entry + Stop Entry** 结合的方式。 |
| **风控层** | **区域穿越止损**：止损必须设在供需区域的**另一侧**。如果价格强势穿过需求区底部，说明机构的订单已被消耗完毕或失效，必须离场。盈亏比通常要求至少 3:1。 |
| **适合市场** | 股票 / 外汇 / 期货 |
| **时间框架** | 日线 / 4H / 1H |
| **成熟度** | 社区级/商业培训级（OTA proprietary methodology） |
| **核心参考来源** | YouTube：Sam Seiden Channel<br>书籍：《Identify and Profit from Market Turning Points》 |
| **与你现有指标映射** | `PV Corr` 的成交量异常 ↔ Seiden 的 Imbalance；`XBreaking` 的占位 ↔ 供需区突破确认；`KD MTF` 的方向 ↔ 供需区趋势方向 |

---

### 18. Beat The Market Maker (BTMM) — Steve Mauro

| 维度 | 内容 |
|------|------|
| **体系名** | 击败做市商 |
| **结构层** | **算法操纵层级**：认为市场由做市商（MM）通过算法控制。关键结构是 **Premium/Discount Array**（基于前一日的 High/Low/Close 计算出的 20-30个价位水平）。重点关注 **PD Array** (Previous Day), **MSB** (Max Swing Bound), **IB** (Initial Balance)。 |
| **能量层** | **升级与降级**：<br>1. **Upgrade (升级)**：价格在亚洲时段或早盘突破关键阻力，意图扫荡流动性。<br>2. **Downgrade (降级)**：故意压低价格以吸筹。<br>3. 使用 **Deal Range** 和 **Tool Set** 来识别 MM 是在" Accumulation (吸筹)" 还是 "Distribution (派发)"。 |
| **执行层** | **Optimal Trade Entry (OTE)**：类似于 ICT 的 OTE，但更强调在特定的时间段（如 NY Open）和特定的 **Level** 上寻找 **Bullish/Bearish Engulfing (吞没形态)** 作为触发器。非常注重 **Time Based (时间)** 的入场。 |
| **风控层** | **Level 失效**：如果在买入水平出现强烈的 Bearish Engulfing 并击穿该水平的低点，说明逻辑错误。另外，严格限制每日亏损次数（通常建议最多2-3次交易机会）。 |
| **适合市场** | 外汇 (EUR/USD 主要) |
| **时间框架** | 15M / 5M / Tick (日内) |
| **成熟度** | 社区级/导师制 |
| **核心参考来源** | 网站：[BTMM Official](https://beatthemarketmaker.com/)<br>YouTube：Steve Mauro (各类学员整理视频) |
| **与你现有指标映射** | `KD MTF` 的多周期 ↔ BTMM 的 PD Array 时间层级；`XBreaking` 的占位 ↔ BTMM 的 Level 突破确认；`Volty` 的 tight ↔ BTMM 的"升级前压缩" |

---

## 方向9：均线 / 动量工具（GLM 补充）

### 19. GMMA (Guppy Multiple Moving Average) — Daryl Guppy

| 维度 | 内容 |
|------|------|
| **体系名** | 顾比复合移动平均线 |
| **结构层** | **两组均线的分离与聚合**：<br>1. **短期组 (3, 5, 8, 10, 12, 15)**：代表交易者的情绪和投机行为。<br>2. **长期组 (30, 35, 40, 45, 50, 60)**：代表投资者的中长期意向。<br>趋势确立的条件是两组均线**平行发散**且方向一致。 |
| **能量层** | **压缩后的释放**：关注均线组的 **Compression (压缩)**。当长期组和短期组收拢甚至纠缠在一起时，表示市场处于平衡状态，即将发生方向选择。能量来自于这种平衡被打破的瞬间。 |
| **执行层** | **趋势回撤入场**：在上升趋势中，等待价格回落至长期组均线附近并获得支撑（短期组未穿透长期组），或者短期组触碰长期组后再次弹起时入场。 |
| **风控层** | **渗透程度**：如果短期组**渗透进**长期组内部并长时间无法出来，或者长期组开始走平/弯曲，则是趋势结束的风控信号。止损设在长期组下方或趋势反转处。 |
| **适合市场** | 股票 / 期货 / 外汇 |
| **时间框架** | 日线 / 周线 / 4H |
| **成熟度** | 工具级/半学术级（广泛集成于TradingView等软件） |
| **核心参考来源** | 书籍：《Trend Trading》(Daryl Guppy)<br>Investopedia：[GMMA Definition](https://www.investopedia.com/terms/g/gmma.asp) |
| **与你现有指标映射** | `KD MTF` 的三周期对齐 ↔ GMMA 的短期/长期组分离；`Volty` 的压缩期 ↔ GMMA 的 Compression；`XBreaking` 的占位 ↔ GMMA 的发散突破确认 |

---

### 20. Volatility Breakout (Larry Williams) — Larry Williams

| 维度 | 内容 |
|------|------|
| **体系名** | 波动率突破 / 威廉指标 |
| **结构层** | **波动收缩形态**：寻找 **NR4 (Narrowest Range in 4 days)** 或 **ID (Inside Day)**。这意味着市场波动率被压缩到极致，如同弹簧被压紧，预示着即将发生大幅 directional move。 |
| **能量层** | **威廉指标 %R + 成交量**：使用 %R 判断超买超卖区域，但这不是反转信号，而是**强者恒强**的延续信号。配合 **OBV (On Balance Volume)** 确认资金流向是否支持突破。 |
| **执行层** | **Range Breakout**：在 NR4/ID K线的**高点上方**买入，**低点下方**卖出。通常在突破后会有一个**回测原阻力变支撑**的过程（Hook setup），那是最佳的二次入场点。 |
| **风控层** | **波动率止损**：如果突破发生后，价格迅速跌回原波动区间内（假突破），或者未能维持 **Smile/Smirk** 形态（期权隐含波动率形态），则立即止损。也常用 **Chandelier Exit** (吊灯止损) 来追踪趋势。 |
| **适合市场** | 期货 / 股指 / S&P 500 |
| **时间框架** | 日线 / 日内 |
| **成熟度** | 半学术级（多次获得交易冠军，方法公开可回测） |
| **核心参考来源** | 书籍：《Long-Term Secrets to Short-Term Trading》<br>URL：[Larry Williams Official](https://www.larrywilliams.com/) |
| **与你现有指标映射** | `Volty` 的波动率压缩 ↔ Williams 的 NR4/ID；`PV Corr` 的 OBV 方向 ↔ Williams 的成交量确认；`XBreaking` 的占位 ↔ Williams 的 Range Breakout |

---

### 21. LBR (Linda Raschke) — Linda Raschke

| 维度 | 内容 |
|------|------|
| **体系名** | Holy Grail / 波段动量 |
| **结构层** | **ADX 趋势滤波器**：首先要求 **ADX > 30**，确认市场处于强趋势状态（非震荡）。然后结合 **EMA (20)** 作为动态支撑/阻力线。只有在趋势强劲时才寻找交易机会。 |
| **能量层** | **动量震荡指标**：使用 **MACD** 或 **Stochastic** 寻找动量脉冲。特别是在 Holy Grail 策略中，寻找 MACD 柱状图的过度延伸后的回归，或者 Stochastic 在强势区的钝化。 |
| **执行层** | **拉回入场**：经典的 **"Holy Grail" Setup** 是：在上升趋势中，价格拉回至 **EMA(20)** 附近，同时出现 **Doji (十字星)** 或 **小型反转K线**，且 ADX 仍 > 30。这就是"在趋势中捡便宜"的执行点。 |
| **风控层** | **低点/高点穿透**：对于多头，止损设在拉回形成的**摆动低点** 下方；对于空头，设在**摆动高点**上方。如果 ADX 开始掉头向下低于 25，通常意味着趋势结束，提前获利了结。 |
| **适合市场** | 股票 / 期货 / ETFs |
| **时间框架** | 日线 / 60min |
| **成熟度** | 半学术级（职业交易员，有详细规则文档） |
| **核心参考来源** | 书籍：《Street Smarts: High Probability Short-Term Trading Strategies》<br>网站：[LBRGroup](https://lbrgroup.com/) |
| **与你现有指标映射** | `KD MTF` 的动量确认 ↔ LBR 的 ADX 趋势过滤；`Volty` 的通道 ↔ LBR 的 EMA(20) 动态支撑/阻力；`XBreaking` 的占位 ↔ LBR 的拉回确认；`RSJ` 的极端 ↔ ADX 从 >30 掉头的趋势结束信号 |

---

## 方向10：中文特有体系（GLM 补充）

### 22. 冯柳 (弱者体系) — 冯柳 / 高毅资产

| 维度 | 内容 |
|------|------|
| **体系名** | 弱者体系 / 逆向投资 |
| **结构层** | **心逆于势，行顺于势**：不预测市场，只关注市场已经发生的"事实"（如股价大跌、利空出尽）。结构上寻找**"看得见的好（高景气）+ 看得见的坏（短期困境）"**的错杀机会。利用**"赔率优先"**原则，在风险收益比极高的位置介入。 |
| **能量层** | **情绪与常识**：不依赖技术指标，而是利用**市场情绪的极端化**（恐慌性抛售）作为能量触底信号。关注**"人气"**（关注度极低）和**"成交量"**（极度缩量）来确认抛压耗尽。 |
| **执行层** | **左侧交易 + 试错**：在下跌途中分批买入（接飞刀），或者在底部盘整区间高抛低吸降低成本。强调**"满仓、分散、不择时"**的操作风格，通过持仓组合对抗不确定性。 |
| **风控层** | **不止损（个股）/ 止损（逻辑）**：这是该体系最特殊的地方。对于个股，如果不看好可以卖出，但如果是因为市场情绪杀跌，往往不止损反而补仓（前提是基本面逻辑未坏）。真正的风控在于**选股的标准**（避开造假、财务差的公司）和**仓位分散**（单一标的极低仓位）。 |
| **适合市场** | A股 / 股票（需基本面配合） |
| **时间框架** | 周线 / 月线 / 中长线 |
| **成熟度** | 实战大师级（私募大佬，非标准化学术体系） |
| **核心参考来源** | 雪球/博客：冯柳（羊驼）早期发言集<br>文章：《冯柳谈投资：弱者体系与逆向投资的核心》 |
| **与你现有指标映射** | `RSJ` 的 `extreme_low` ↔ 冯柳的"情绪极端化"；`PV Corr` 的极度缩量 ↔ 冯柳的"成交量确认抛压耗尽"；你的 A5 财报估值库 ↔ 冯柳的"选股标准" |

---

## 方向11：风控 / 仓位管理专门体系（GLM 补充）

### 23. Van Tharp Position Sizing — Van Tharp

| 维度 | 内容 |
|------|------|
| **体系名** | 萨普仓位管理模型 |
| **结构层** | **R-Multiple 概念**：将所有交易标准化。初始风险定义为 **1R**。系统的核心不在于胜率，而在于**期望值**。结构上区分 **趋势跟踪型**（低胜率高盈亏比）和 **高胜率型**（高胜率低盈亏比）。 |
| **能量层** | **市场状态热力图**：虽然 Van Tharp 本身是风控大师，但他建议结合 **Market Type (市场类型)**：是温和上涨、剧烈波动还是横盘？根据市场波动能量调整 **Position Sizing (仓位大小)**。 |
| **执行层** | **百分之一模型 / ATR 模型**：<br>1. **% Risk Model**：每笔交易承担总资金的 1%（新手）~ 2%（专家）。<br>2. **Volatility Model**：根据 ATR 决定股数，使得 1 ATR 的波动等于总资金的 1%。 |
| **风控层** | **系统性破产预防**：<br>1. **Drawdown Rule**：当账户回撤达到预设阈值（如 10%），强制将仓位减半（1% -> 0.5%）。<br>2. **Gain Adjustment**：盈利增加时可适当加大仓位（但有限度）。<br>3. **Correlation Control**：不允许在高度相关的资产上同时重仓。 |
| **适合市场** | 所有市场（通用风控层组件） |
| **时间框架** | 适用于任何时间框架 |
| **成熟度** | 学术级/心理学级（交易心理学权威） |
| **核心参考来源** | 书籍：《Trade Your Way to Financial Freedom》、《The Definitive Guide to Position Sizing》<br>URL：[Van Tharp Institute](https://www.vantharp.com/) |
| **与你现有指标映射** | `Volty` 的 ATR ↔ Van Tharp 的 Volatility Model；`RSJ` 的极端 ↔ Van Tharp 的 Drawdown Rule 触发；`indicator_audit` 框架 ↔ Van Tharp 的 R-Multiple 记录系统；`KD MTF` 的 `alignment_tier` ↔ Van Tharp 的 Market Type 分类 |

---

## 更新：外部体系 vs 你现有资产的覆盖缺口（v0.2）

| 功能层 | 外部体系已覆盖（23个） | 你现有资产 | 缺口评估 |
|--------|----------------------|-----------|---------|
| **结构层** | ICT/Grimes/Clenow/Hoffman/Brooks/YTC/Mentfx/Faber/Dalton/Wyckoff/缠论/GMMA/LBR/Seiden/BTMM/冯柳 | `KD MTF P0`（6字段已冻结） | ✅ **基本覆盖**，但缺"日内结构"（IB/VA/POC/中枢/供需区）字段化 |
| **能量层** | Clenow ATR/Faber 波动率/Verma 统计/Brooks bar/YTC 订单流/Dalton VA/POC/Wyckoff 努力结果/缠论背驰/Williams 波动率/LBR 动量/Seiden Odds Enhancers | `Volty`（ATR通道）、`PV Corr`（价量确认） | ✅ **基本覆盖**，但缺"成交量分布"（HVN/LVN）和"缠论背驰"字段化 |
| **执行层** | ICT Order Block/Brooks H2/L2/BPB/YTC TST/BOF/BPB/Dalton 80% Rule/Turtle 突破/Seiden 限价单/BTMM OTE/Williams Range Breakout/LBR 拉回/缠论三类买卖点 | `XBreaking`（NEED_PROBE） | ❌ **严重不足**，执行层方法极多但你只有XBreaking占位 |
| **风控层** | Clenow ATR 止损/Faber 现金分散/Verma Kelly/YTC scratch/Dalton VA 外侧/Wyckoff 结构失效/缠论中枢破坏/Turtle N倍止损/Tharp %Risk/Drawdown Rule | `Volty Stop`（动态止损）、`RSJ`（情绪极端） | ✅ **部分覆盖**，但缺"portfolio-level drawdown control"和"R-Multiple 记录" |
| **审计层** | Clenow 回测/Verma Trading Database/Tharp R-Multiple | `indicator_audit`（历史回测产物） | ✅ **已有框架**，但缺系统化整合 |

---

## 关键新增洞察（v0.2）

### 1. 执行层仍然是最弱环节

即使补充了 12 个新体系，**执行层**仍然是你的最大缺口。外部体系在执行层的方法极其丰富：
- **突破类**：Turtle 唐奇安通道、Williams NR4/ID、BTMM Level 突破
- **回测类**：ICT Order Block、Brooks BPB、YTC BPB、Seiden 供需区、LBR Holy Grail
- **结构确认类**：缠论三类买卖点、Wyckoff Spring/Upthrust、Dalton 80% Rule

而你只有 `XBreaking`（NEED_PROBE）。**建议优先解决 XBreaking 语义，或至少退化为手动执行层**。

### 2. 风控层有了质的飞跃

GLM 补充的 **Van Tharp** 和 **Turtle** 的仓位管理逻辑，可以直接映射到你的现有指标：
- `Volty` 的 ATR → Van Tharp 的 Volatility Model
- `RSJ` 的极端 → Van Tharp 的 Drawdown Rule 触发
- `indicator_audit` → Van Tharp 的 R-Multiple 记录系统

**建议：把 Van Tharp 的仓位管理作为"风控层标准化"的第一候选**。

### 3. 中文体系的独特价值

**缠论**和**冯柳**是西方体系中完全没有的：
- 缠论的"中枢"概念是独特于西方"支撑/阻力"的结构化工具
- 冯柳的"弱者体系"是逆向投资在 A股 的实战落地
- 两者都强调"不预测，只应对"，这与你的 `KD MTF`（只读结构，不预测）的哲学一致

**建议：缠论可以作为"结构层补充"，冯柳可以作为"A股选股层补充"**。

### 4. 量化策略的"总开关"价值

**Dual Momentum** 和 **Fama-French** 虽然不直接用于日内交易，但可以作为"总开关"：
- 当 Dual Momentum 显示风险资产为负时，降低你的波段交易频率
- 当 Fama-French 的 Momentum 因子 Z-Score 极端时，作为 `RSJ` 的宏观验证

---

## 版本记录

- v0.1 (2026-07-06): 初版，覆盖 11 个外部体系，按功能层拆解
- v0.2 (2026-07-06): 整合 GLM 搜索结果，新增 12 个体系（共 23 个），覆盖经典量价、中文哲学、量化策略、风控专门体系
- 来源：kimi_search_v2 多轮搜索 + 仓库内部已有文件交叉验证 + GLM 补充搜索
