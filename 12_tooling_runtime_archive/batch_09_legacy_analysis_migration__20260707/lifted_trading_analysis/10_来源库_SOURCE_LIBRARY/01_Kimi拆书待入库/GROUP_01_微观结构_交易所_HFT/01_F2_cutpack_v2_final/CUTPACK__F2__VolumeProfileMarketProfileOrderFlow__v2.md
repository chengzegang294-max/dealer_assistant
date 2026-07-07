## BASIC_INFO
- title: Volume Profile, Market Profile, Order Flow: Next Generation of Daytrading
- author: Johannes Forthmann
- material_type: 交易技术教材/教程
- domain_tags: [volume profile, market profile, order flow, footprint, TPO, POC, VWAP, delta, cumulative delta, absorption, imbalance, HVN, LVN, initial balance, value area, bid-ask volume, OTF, day structure]
- file_scope: Volume Profile, Market Profile, Order Flow Next Generation of Daytrading (Forthmann, Johannes) (Z-Library).pdf
- source_file_size_mb: 4.04
- retain_mode: RETAINED_EXCERPTS
- current_repo_role: SECONDARY_STRUCTURED_NOTE

## MATERIAL_POSITIONING
- what_this_book_is: 一本面向日内交易者的实用教材，将 Volume Profile（成交量分布）、Market Profile / TPO（市场轮廓）、Order Flow / Footprint / Delta（订单流分析）三合一，用于在日内时间框架中识别大型机构交易者（OTF）的踪迹、定位流动性密集区与关键反转点，并据此制定低风险的入场与持仓计划。
- why_in_f2: 本书定义了后续 A2 / F1 中成交量分布特征工程与订单流微观结构所需的核心可观察对象：POC、VA、HVN/LVN、TPO 结构、Initial Balance、Delta Divergence、Absorption、Stacked Imbalance 等。这些概念在量化语境下需要转化为 intraday volume-at-price、时间-价格矩阵、逐笔买卖方向等数据对象，因此必须作为结构化笔记保留原始文本定义与边界条件。
- not_a_strategy_book_because: 作者反复强调本书不是一套可像指标一样直接套用的系统（p.9, p.156）。全书以案例驱动，强调“contextual thinking”和“拼图式”分析，没有给出固定的入场参数、仓位公式或回测规则。任何将书中描述直接转化为机械信号的尝试都会与作者意图相违。
- relation_to_order_flow_microstructure: 本书直接涉及订单簿微观结构（DOM、limit orders vs. market orders、iceberg orders、spoofing），但作者明确表示 DOM 容易被操纵，更偏好使用 Footprint + Delta + Cumulative Delta 作为过滤工具（p.64-66, p.80-82）。因此，书中关于订单流的描述处于“从订单簿形态到可聚合统计量”的过渡地带，对量化实现具有直接参考价值。
- data_footprint_required: 需要 Level 1（Top of Book）或 Level 2（market depth）原始期货交易所数据；作者特别指出 Forex 是去中心化市场，缺乏精确成交量数据，不建议用于订单流分析（p.15, p.62-63）。对于量化实现，这意味着需要 intraday tick/aggregate 数据，以及 bid-ask 方向标识。

## CONTENT_STRUCTURE
- 1. Introduction: 本书写作背景，批判传统技术分析，提出 Profile + Order Flow 观察法的必要性
- 2. The Advantages of Futures: 期货 vs. 股票/外汇，保证金机制，流动性要求，数据透明度
- 3. The Market Participants: 机构交易者（OTF）与零售交易者的区分，OTF 的建仓与操纵方式
- 4. Market Profile - A Brief Overview: TPO（Time Price Opportunity）基础，Initial Balance（IB），Range Extension，Single Prints / Tails，日型结构（D profile, trend day）
- 5. What is a Volume Profile?: 成交量分布图定义，VPOC（Point of Control），Naked POC，High Volume Areas，Thin Profiles / Low Volume Nodes
- 6. Value Area: 70% 规则，VAH / VAL，Value Area 突破与回归，隔夜参考意义
- 7. Forms and Shapes of Profiles: P profile, b profile, D profile, Double Distribution 的形态意义与上下文依赖
- 8. How to display the Profiles?: Fixed profiles（前日/24h/周 profile）与 Flexible profiles（日内动态 profile）的使用场景与区别
- 9. Bounce Backs: Type 1（简单支撑/阻力回弹）, Type 2（气球效应 / 回弹至 imbalance 区）, Type 3（气球破裂 / 方向反转）
- 10. General Set ups: Accumulation and Follow-up（积累与跟进），Reversals（强/弱反转），Strong/Weak Highs and Lows
- 11. Hardware, Software and Data Feed: Atas / Sierrachart / NinjaTrader 等，Level 1 vs Level 2 data feed，数据成本与必要性
- 12. Order Flow Analysis:
  - 12.1 DOM / Order Book: limit orders, market orders, spoofing, iceberg orders, Smart Tape
  - 12.2 Footprints: Footprint Chart 内部结构，lift the ask / hit the bid，Stacked Imbalance，POC of single candles
  - 12.3 Delta: Delta 定义与表示，Absorption（吸收），Delta Divergence，Cumulative Delta，Variants（领先/滞后/混合形态），Delta Numbers and Profiles
- 13. The Preparation: 盘前准备流程，VIX 检查，经济日历，屏幕布局，隔夜参考点
- 14. Liquidity and Volatility: 流动性与波动率的配对关系，VIX 阈值（18 以上机会增加，36 以上应离场），混乱市场识别
- 15. Characteristics of Individual Trading Instruments: E-Mini, Dax, Bund, EURUSD, JPY, Gold, Oil, Hang Seng, Nikkei 的各自流动性与行为差异
- 16. More on Market Profile: Opening Phases（Open Drive, Open Rejection Reverse, Acceptance, Rejection of Value Area），MPOC vs VPOC 分歧， tails 长度与 OTF 强度
- 17. Filtering the Ledge: Ross Hook, Ledge（直接/hanging），用 Flexible VP 过滤趋势中的中继结构，P profile 在趋势中的意义
- 18. Broadening Tops: 宽幅顶部（Schabacker）作为流动性枯竭的警告信号，假突破与后续回调
- 19. Complete Examples: Yen, E-Mini S&P, FDAX, Bund, Crude Oil, Gold, Broadening Top + Ledge, EURUSD, Weekly Profiles 的完整案例分析
- 20. Summary: 方法论的总结，强调无系统、无预测、只确认
- 21-25. Bonus Chapters: Fake Moves（Backfire, SHS, Squeeze, Trend Line, Breakout），Trend 定义（Dunnigan），Trade & Risk Management，Short Term Trading Example

## RETAINED_EXCERPTS

- excerpt_id: F2_VP_001
  source_hint: "Page 19-20, Market Profile - A Brief Overview"
  quote: "The market profile is also known as TPO and combines time, volume and price. TPO is an abbreviation for Time Price Opportunity. It has a bell-shaped structure. The traditional approach extends over one trading day. 30 minute time periods are shown here in letter form on a vertical plane."
  why_kept: 明确定义 TPO 的三要素（time, volume, price）及其传统表示方式（30-min 字母块），是后续 Market Profile 数据结构化的基础。
  quant_link: TPO 时间-价格矩阵需要 intraday 30-min bracket 或更小粒度的 presence-at-price 数据；日 K 无法还原。

- excerpt_id: F2_VP_002
  source_hint: "Page 20, Initial Balance"
  quote: "The letters A and B represent the first two first 30 minute periods of the institutional trading day. This period is also known as the initial balance."
  why_kept: 定义 Initial Balance（IB）为开盘后前两个 30-min 周期（A, B），是 Market Profile 日结构分析的核心起点。
  quant_link: IB 的自动识别需要交易所官方会话时间或用户自定义的 institutional trading hours；分钟级价格范围聚合即可计算 IB Range。

- excerpt_id: F2_VP_003
  source_hint: "Page 20, Range Extension"
  quote: "Any extension of the Initial Balance up or down is called Range Extension."
  why_kept: Range Extension 是判断趋势日 vs 平衡日的关键机制，直接关联日型分类。
  quant_link: 可量化：在 IB 结束后，价格突破 IBH/IBL 即构成 Range Extension；需 intraday 分钟数据。

- excerpt_id: F2_VP_004
  source_hint: "Page 20, Single Prints / Tails"
  quote: "To speak of a tail, you should see at least two single-column rows at the edges of a market profile. In this case you see a 'buying tail' with three single-column rows, which led to an upward movement in the last trading phase."
  why_kept: 定义 Tails（单字母行）的数量阈值（至少 2 个），表示 OTF 在极端价格区间的激进介入，是 Market Profile 的微观结构信号。
  quant_link: 需要完整的 TPO 矩阵（30-min brackets × price levels）来检测单字母行；日 K 无法计算。

- excerpt_id: F2_VP_005
  source_hint: "Page 21, Trend Day Profile Structure"
  quote: "Trend days should never have more than four parallel rows or blocks of letters during the course of the day. They have a narrow and long (high) day profile. There are multiple range extensions in the same direction."
  why_kept: 给出趋势日的 TPO 形态规则（≤4 并行行，窄而高），是日型分类的量化判据之一。
  quant_link: 需要日内 TPO 矩阵计算每行（price level）的并行字母块数；日内分钟数据可代理。

- excerpt_id: F2_VP_006
  source_hint: "Page 22, Volume Profile Definition"
  quote: "The price level at which the largest number of transactions took place is called Point of Control (VPOC). This price is considered to be fair. Otherwise, most transactions would not take place there."
  why_kept: 定义 VPOC 为给定时期内成交量最大的价格水平，并赋予其“公允价格”的行为解释。
  quant_link: 可量化：对价格轴聚合成交量取 argmax；需 intraday volume-at-price（1-min 或 5-min 聚合）。

- excerpt_id: F2_VP_007
  source_hint: "Page 22, POC Shift"
  quote: "A rising or falling Point of Control (VPOC), on the other hand, reflects a change in the market situation. If it changes, a higher or lower price is accepted."
  why_kept: POC 位移（POC Shift）被作者视为 OTF 意图变化的关键信号，贯穿全书（如 p.45-50）。
  quant_link: 可追踪 Flex VP 的 POC 随时间变化序列；需动态滚动聚合窗口。

- excerpt_id: F2_VP_008
  source_hint: "Page 25, Naked POC"
  quote: "The most important point of a past period is the so-called Naked POC. This is a point of control that was not touched the following day. This point attracts particular attention."
  why_kept: Naked POC 是后续交易日中未被触及的历史 POC，被作者视为强吸引力参考点。
  quant_link: 可通过历史 intraday volume-at-price 序列计算每日 POC，再检测后续是否触及；日 K 的日高/日低无法精确判定是否触及 intraday POC。

- excerpt_id: F2_VP_009
  source_hint: "Page 27, Thin Profiles and Low Volume Nodes"
  quote: "Thin Profiles are zones where the price is proceeding particularly fast. These always occur when OTF buyers or sellers are operating aggressively. Strong indentations are called low volume nodes. These are often located on the edge of high volume areas and can be starting points for reversals."
  why_kept: 定义 Low Volume Node（LVN）为成交量分布中的“凹陷”区，价格穿过速度快，与 HVN 形成对比；是 Volume Profile 的微观结构概念。
  quant_link: 需要 volume-at-price 序列检测局部极小值（凹陷）；需 intraday 分钟数据。

- excerpt_id: F2_VP_010
  source_hint: "Page 28, Value Area 70% Rule"
  quote: "The Value Area is the centerpiece of the volume profile. It characterizes the area in which 70% of the total trading activities of a selected period have taken place."
  why_kept: 明确 VA 的 70% 规则——覆盖总成交量 70% 的价格区间；是 Volume Profile 的核心统计边界。
  quant_link: 可量化：对 volume-at-price 分布按成交量从大到小排序，累积至 70% 的成交量对应价格区间的上下界即为 VAH/VAL；标准做法，可计算。

- excerpt_id: F2_VP_011
  source_hint: "Page 29, Value Area Opening Test"
  quote: "Did the market open above/below yesterday's Value Area today? Did it stay there after the opening phase or did it fall back into the value area of the previous day?"
  why_kept: VA 的突破/回归测试是日内方向判断的上下文规则之一，被作者用于开盘场景分析。
  quant_link: 需前日 VAH/VAL 与当日开盘价/开盘后分钟级价格序列比较；可计算。

- excerpt_id: F2_VP_012
  source_hint: "Page 31, P Profile"
  quote: "P profiles are theoretically associated with a bullish scenario. However, if the market has already gone through a long upward phase, P profiles can signal a reversal. As a result, P profiles have their greatest significance when they appear at the beginning of a trend."
  why_kept: P profile 的形态意义高度依赖上下文（趋势起点 vs 趋势末端），体现了作者“形态必须结合语境”的方法论。
  quant_link: P profile 的形态识别需要完整的 volume-at-price 或 TPO 矩阵分布；在量化中可作为分布偏态/峰度的代理，但需人工上下文判断。

- excerpt_id: F2_VP_013
  source_hint: "Page 32, D Profile and Double Distribution"
  quote: "A D profile is a sideways day, in many cases also an 'inside day', whose entire price range lies within the fluctuation range of the previous day. The market is 'in balance'. Double Distribution Profiles occur relatively frequently. ... Initially the price spent some time in one zone. Then there is a sudden rejection in form of an imbalance before a new strongly traded price zone is formed."
  why_kept: D profile（平衡）与 Double Distribution（双分布）是 Market Profile / Volume Profile 的两种基本日型结构；Double Distribution 意味着市场方向可能发生切换。
  quant_link: D profile 识别可通过日内价格范围与成交量分布集中度；Double Distribution 需要检测 volume-at-price 的多峰结构（bimodal）。

- excerpt_id: F2_VP_014
  source_hint: "Page 34, Fixed vs Flexible Profiles"
  quote: "Volume profiles of this type are called fixed volume profiles. I use them to get a basic overview of the last 3 days and possibly get some good reference points for the current session. All further analysis is done with flexible profiles."
  why_kept: Fixed VP（固定窗口：前日/24h/周）与 Flexible VP（动态窗口：日内实时调整）的区分是本书方法论的核心组织原则。
  quant_link: Fixed VP 对应历史 volume-at-price 聚合；Flexible VP 对应滚动窗口聚合，需支持动态边界调整。

- excerpt_id: F2_VP_015
  source_hint: "Page 45, POC Shift in Trend"
  quote: "When a trend begins, the value area should follow the POC, not the POC of the value area as in sideways phases. Different laws apply there."
  why_kept: 作者在趋势 vs 横盘阶段对 POC 与 VA 的相对运动关系给出区分性规则：趋势中 VA 跟随 POC，横盘中 POC 在 VA 内部旋转。
  quant_link: 可量化追踪 VA 中心与 POC 的偏离方向及速度，作为趋势/横盘的代理指标之一。

- excerpt_id: F2_VP_016
  source_hint: "Page 54, Type 2 Bounce Back (Balloon Effect)"
  quote: "The author of market profile classic 'Mind over Markets' compares this situation with a balloon inflated. When it is squeezed, it bounces back quickly... Group B has now made a partial profit by bringing the price back a good distance. However, they do not want to risk a fight with group A and liquidate their position just before reaching the starting point of the Imbalance Zone."
  why_kept: Type 2 回弹描述了两个 OTF 群体（A 和 B）在 volume profile 上的博弈边界——回弹常在 imbalance 区边缘停止；这是理解 Volume Profile 作为博弈地图的关键隐喻。
  quant_link: 需要识别 HVN 区（Group A 建仓区）与相邻 LVN 区（imbalance）的边界，结合回测价格位置；需 intraday volume-at-price。

- excerpt_id: F2_VP_017
  source_hint: "Page 64, Order Flow Subdivision"
  quote: "The order flow analysis is an important enhancement of the volume profile analysis. It can be sub-divided into three main areas: DOM (= Depth of Market), Footprint Chart, Delta."
  why_kept: 作者明确将订单流分析分为 DOM、Footprint、Delta 三大区域，构成后续章节结构的基础。
  quant_link: DOM 需要 Level 2 订单簿数据；Footprint 需要逐笔/聚合 bid-ask 成交量；Delta 需要 market order 方向标识。

- excerpt_id: F2_VP_018
  source_hint: "Page 65, Market Orders Move Price"
  quote: "The price always increases when a market buy order meets the closest sell limit order (right) and the number of contracts is greater than the number of contracts offered there. In this case, this is called 'lift the ask'. The price always falls when a market sell order meets the closest buy limit order (left) and the number of contracts to be sold is greater than the limit order on the buyer's side (closest). In this case, the term 'hit the bid' is used."
  why_kept: 定义 lift the ask / hit the bid 作为价格变动的微观机制，是 Footprint 和 Delta 计算方向的根本来源。
  quant_link: 需要逐笔成交数据（tick data）带 bid/ask 标识，或至少聚合级别的 bid volume / ask volume per price level。

- excerpt_id: F2_VP_019
  source_hint: "Page 70-71, Footprint Chart and Imbalance"
  quote: "Footprint Charts can be read diagonally from top right to bottom left in a falling market. In this case you can see a red number on the next lower floor. This number is only displayed by the Order Flow software if the number of sell market orders is at least twice as high as the limit orders on the buyer's side (hit the bid)."
  why_kept: 定义 Footprint imbalance 的判定条件：market order 数量至少为对面 limit order 的两倍（作者使用的默认乘数）。
  quant_link: 需要 per-candle / per-price-level 的 bid volume vs ask volume 聚合；乘数可参数化，但原始数据需带方向。

- excerpt_id: F2_VP_020
  source_hint: "Page 72, Stacked Imbalance"
  quote: "A 'stacked imbalance' (stacked order) occurs when several imbalances are lined up on one side. This can only happen if big players act aggressively via market orders. ... These are then visible in the form of a green chain on the right side for OTF buyers (lift the ask) and a red chain on the left side (hit the bid)."
  why_kept: Stacked Imbalance 是作者视为 OTF 激进介入的最强 Footprint 信号之一，贯穿全书案例。
  quant_link: 需要在连续多个 price levels（或 candles）上检测同方向 imbalance；需要 intraday bid-ask volume per level。

- excerpt_id: F2_VP_021
  source_hint: "Page 78, Delta Definition"
  quote: "Delta represents the difference between contracts bought and sold during a selected time period and can be displayed in an order flow software in various ways."
  why_kept: Delta 的数学定义：选定时间周期内买入合约与卖出合约的差值；是订单流分析的核心统计量。
  quant_link: Delta = Ask Volume − Bid Volume（或反之，取决于符号约定）；需要 intraday bid-ask tagged volume；可计算。

- excerpt_id: F2_VP_022
  source_hint: "Page 78-79, Delta Divergence"
  quote: "However, it is precisely these turning points that become interesting for a day trader, because this is where deception often takes place. From this point of view, it is especially the deviations that should be considered. On the following chart the Delta Histogram shows strong positive deltas. The price should rise, but it falls."
  why_kept: Delta Divergence（价格与 Delta 方向背离）是作者识别 Absorption / 操纵 / 反转的关键工具。
  quant_link: 可计算：价格创新高而 Delta 未创新高（或反之）即构成 divergence；需 intraday Delta 序列。

- excerpt_id: F2_VP_023
  source_hint: "Page 80-81, Absorption and Iceberg Orders"
  quote: "Iceberg Orders are split OTF orders. ... If the limit orders are hit, they are automatically converted into market orders. As a result no price changes will occur. All market orders of the opposing side are 'absorbed' by iceberg orders. ... Absorption often is easier to localize with a summed (cumulated) delta curve."
  why_kept: Absorption 的定义：OTF 的 iceberg limit orders 吸收对手方的 market orders，导致价格不随 Delta 方向移动；是本书订单流分析的精髓。
  quant_link: 需要检测 Cumulative Delta 与价格的背离（Delta 持续下降但价格横盘/微涨），并伴随 Footprint 中大单被“消化”的特征；需要 Level 2 或至少 Top-of-Book 的逐笔数据。

- excerpt_id: F2_VP_024
  source_hint: "Page 86-87, Delta Variants (Leading / Lagging / Mixed)"
  quote: "It is often the price that anticipates the start of decisive movements, not Delta as many traders assume. ... Approx. 20 min. after the opening, Delta made a new high, but the price not. This means a clear absorption. The Opening high got rejected! After that, Delta fell, but the price rose slightly (direct divergence)."
  why_kept: 作者分类了 Delta 与价格关系的多种变体：Delta 领先、价格领先、混合形态；对量化建模的时序关系具有直接参考价值。
  quant_link: 需要高频 Delta 与价格序列的 lead-lag 分析；需 intraday 1-min 或更细粒度数据。

- excerpt_id: F2_VP_025
  source_hint: "Page 92, Delta Profiles and Rejection"
  quote: "At the top you can see an extremely high number of executed buy market orders. But the price immediately closes significantly lower. This is a rejection in combination with absorption. All breakout traders were trapped here."
  why_kept: Delta Profile（将 Delta 以 volume profile 方式呈现）与 Rejection + Absorption 的组合是作者用于确认假突破的利器。
  quant_link: 可将 Delta 按 price level 聚合为 Delta Profile，检测某价格区大量单向 Delta 但价格反向收盘；需 intraday bid-ask volume per price level。

- excerpt_id: F2_VP_026
  source_hint: "Page 109, Opening Phases Classification"
  quote: "Open Drive: The market opens above yesterday's range and immediately continues in the same direction... Open Rejection Reverse: The market opens outside yesterday's range, is rejected and immediately shoots in the opposite direction... Acceptance: The market opens outside yesterday's value area, but remains within yesterday's range..."
  why_kept: Market Profile 传统开盘类型分类（Open Drive, Open Rejection Reverse, Acceptance, Rejection of Value Area）被作者保留但提醒“不应机械套用”。
  quant_link: 可基于前日 range/VA 与当日开盘价格和前 30-min 走势自动分类；需分钟级数据与前日聚合统计。

- excerpt_id: F2_VP_027
  source_hint: "Page 111, MPOC vs VPOC Divergence"
  quote: "In case of an imminent breakout, VPOC and MPOC should be identical. If they are not, then the probability increases that the POC of the market profile will be targeted again by market makers to call stops."
  why_kept: MPOC（Market Profile POC = 停留时间最长点）与 VPOC（成交量最大点）不一致时，假突破概率上升；是双 profile 验证的关键规则。
  quant_link: 需同时计算 TPO 矩阵的 time-at-price 峰值和 volume-at-price 峰值；两者不一致可作为警告信号。

- excerpt_id: F2_VP_028
  source_hint: "Page 117-118, Ledge and Ross Hook"
  quote: "Ross Hooks are called the temporary end points of a trend section... Ledges are parallel mini-congestion zones that form in strong trend sections when the trend comes to a break. ... With Ledges you should distinguish 2 types. With direct ledges, there is no real hook... Hanging ledges are the better ones, because they can only be created after a hook has become clearly visible."
  why_kept: Ledge 与 Ross Hook 是作者用于趋势中继过滤的图表结构概念；结合 Flexible VP 使用。
  quant_link: Ledge 和 Hook 是价格结构概念，需通过价格极值序列和平行通道检测；Volume Profile 的 POC 位移用于确认突破方向。

- excerpt_id: F2_VP_029
  source_hint: "Page 119-120, P Profile in Ledge Filter"
  quote: "If in a strong intraday trend you see a Ross Hook followed by a trailing Ledge plus P profile (b profile in an uptrend), then there is a high probability that the trend has resumed before the Hook is taken out. A starting point is always a drop below the Flex VP POC."
  why_kept: Ledge + P Profile + POC 下破是作者给出的强趋势中继入场条件组合；体现了多维度确认的方法论。
  quant_link: 需同时检测价格结构（ledge）、volume profile 形态（P profile 识别）、POC 动态位移；属于多条件触发，非单信号。

- excerpt_id: F2_VP_030
  source_hint: "Page 122-123, Broadening Top Definition"
  quote: "Broadening tops are classic patterns which ... characterise situations in which large market participants are beginning to leave the market or have already done so. ... They are characterised by five diverging oscillations... A retracement follows afterwards, which in most cases makes up 40 - 60% of the last downswing."
  why_kept: Broadening Top 作为流动性枯竭的宏观警告信号，被作者与 Volume Profile 的 POC 延伸结合使用。
  quant_link: Broadening Top 为价格形态（5 个扩散摆动），可通过价格序列检测；但其量化意义更多在于与 VP 参考区结合后的上下文判断。

- excerpt_id: F2_VP_031
  source_hint: "Page 158, VWAP Mention"
  quote: "Recently, other terms such as VWAP and Heat map have been making the rounds. I don't use them, because they either generalize too much (VWAP)..."
  why_kept: 作者明确排除 VWAP，认为其过度泛化；对量化实现具有反向参考价值——如果构建类似工具，需避免将 VWAP 作为通用支撑/阻力使用。
  quant_link: VWAP 公式本身可计算，但作者质疑其在日内方向判断中的行为解释力；若纳入量化系统，需附加上下文过滤。

- excerpt_id: F2_VP_032
  source_hint: "Page 198-199, Take Profit and Low Volume Zones"
  quote: "Low Volume Zones (Thin Profiles) are therefore the zones of accelerated movement. After passing through these zones the momentum will automatically decrease. A take profit order should be placed there."
  why_kept: LVN 作为动量减速区，被作者用于止盈位定位；体现 Volume Profile 在风险管理中的应用。
  quant_link: 通过历史/当前 volume-at-price 识别 LVN 区，作为潜在目标位；需 intraday volume-at-price。

- excerpt_id: F2_VP_033
  source_hint: "Page 100-101, Follow Through and Time"
  quote: "This brings us to the most important factor of every price action. This will be addressed even more often in this book: Follow Through. ... The purpose of VP and order flow analysis is not guessing nor following any trends, assumptions or 'gut feelings', but to enter the market as soon as possible after OTF's have done so."
  why_kept: Follow Through 是作者强调的核心概念——入场后必须有即时动量确认；否则应离场。这是非机械化的风险管理哲学。
  quant_link: Follow Through 可近似为入场后 N 根 candles 的动量/价格位移统计；但作者将其作为语境判断，非固定阈值。

- excerpt_id: F2_VP_034
  source_hint: "Page 62-63, Data Feed Requirements"
  quote: "For the VP and Order Flow analysis you need either Level 2 or Level 1 Top of the Book Data - Feed from the original futures exchanges in the USA, Europe or Asia. ... Level 1 Top of the book data provides all recently executed market orders with price and time. They are sufficient for the examples shown in this book."
  why_kept: 明确数据要求：Level 1（Top of Book，含成交价格与时间）即可支持书中案例；Level 2 含 market depth 更好。这是量化实现的数据边界定义。
  quant_link: 需要原始期货交易所的 tick/Top-of-Book 数据； Forex 无精确数据，不适合。

- excerpt_id: F2_VP_035
  source_hint: "Page 16, OTF Definition"
  quote: "Throughout this book, institutional traders are referred to as 'other time frame traders' (OTF traders) because their expectation horizon is at a higher time level than day trading. ... The large market participants addressed here dispose of massive financial resources, which they constantly use in the markets for specific purposes."
  why_kept: OTF（Other Time Frame）是本书的隐性核心概念——所有 Profile 和 Order Flow 分析的最终目的都是识别 OTF 的活动痕迹。
  quant_link: OTF 本身不可直接观测，但通过 Volume Profile 的 HVN 聚集、Footprint 的 Stacked Imbalance、Delta Divergence 可间接推断其存在和方向。

- excerpt_id: F2_VP_036
  source_hint: "Page 40-41, MP and VP Combined"
  quote: "Both profiles usually do not show any major external deviations. It is more the different points of control that can sometimes provide essential information. ... The market profile shows the time a trading instrument remains at different price levels."
  why_kept: 作者强调 Market Profile 与 Volume Profile 的互补性：VP 看成交量聚集，MP 看时间停留；两者 POC 差异本身即信息。
  quant_link: 需同时维护 time-at-price（TPO）和 volume-at-price（VP）两个矩阵；双 POC 差异可作为特征变量。

- excerpt_id: F2_VP_037
  source_hint: "Page 96-97, VIX Thresholds"
  quote: "My experience in recent years shows that the probability of profitable price movements on the stock markets increases considerably when the Vix Index reaches values above 18. Above a limit of 36, one should no longer enter the market because the Fear Factor becomes too large."
  why_kept: 作者给出经验性的 VIX 阈值（18 和 36）作为波动率过滤条件；可直接作为量化环境过滤器。
  quant_link: VIX 数据公开可获取；可设为策略的波动率环境开关（proxy_quantizable_now）。

- excerpt_id: F2_VP_038
  source_hint: "Page 10-11, Market Profile Renaissance"
  quote: "The market profile related to the volume profile has been known for over 40 years. ... However, the progressive development of chart software has led to a renaissance of two central principles of this form of analysis in particular. By integrating them into a chart, market profile analysis can give traders a quick overview of who is in control of the market."
  why_kept: 说明 Market Profile 的老方法（80 年代理论）部分失效，但 IB 和 POC 等核心原则在当代软件中仍有价值；提醒量化实现时不能机械套用旧日型分类。
  quant_link: 需关注软件可实现的实时 TPO/VP 聚合，而非手写字母图；传统日型分类可作为启发式框架，但需动态适配。

- excerpt_id: F2_VP_039
  source_hint: "Page 57-58, Strong Highs and Lows / Take Out Early Morning Stops"
  quote: "An aggressive reversal offers a day trader the best chances if it takes place at important reference points. On the following chart you can see a strong high and a strong low in the E-Mini. In my apprenticeship we always practiced this on the E-mini. It was called 'Take out early morning stops'."
  why_kept: 强高低点与开盘止损清扫（Take out early morning stops）是作者反复出现的交易场景；本质是识别流动性陷阱后的反转。
  quant_link: 强高低点可由开盘后价格极值 + 成交量/订单流确认来检测；属于事件驱动型机会，非连续信号。

- excerpt_id: F2_VP_040
  source_hint: "Page 60, Unfinished Auction / Weak High"
  quote: "Another form of a weak high or low is called an unfinished auction and looks similar or identical to the weak high shown here. In this situation no clear high or low is formed because two extreme points are at the same price level. ... If no clear buyer or seller can be determined at a price auction, the probability increases that this stalemate situation will be solved by crossing the highs or lows again."
  why_kept: Unfinished Auction（未完成的拍卖）是 Market Profile 中识别弱反转/犹豫状态的概念，被作者用于过滤假突破。
  quant_link: 需检测价格极值的重复测试（equal highs/lows）及对应成交量/订单流是否确认方向；需 intraday 数据。

## CORE_CONCEPTS

- concept_name: Volume Profile (VP)
  definition_from_text: "The horizontal representation of volume by means of a histogram in the main chart is called a volume profile." (p.24) 价格轴上的成交量水平直方图，显示在给定时期内各价格水平上成交的合约数量。
  behavioral_mechanism: 价格倾向于回到成交量最大的区域（POC），因为该价格被认为是“公允价格”；如果 POC 发生位移，说明大型参与者接受了新的价格水平；薄区域（LVN）代表快速通过区，阻力小。
  data_objects_involved: volume-at-price aggregation per period, POC, VAH, VAL, HVN, LVN, Naked POC
  quant_boundary: 需要 intraday 分钟级成交量按价格聚合；日 K 的日高/日低/成交量无法还原价格级别的成交量分布。

- concept_name: Market Profile / TPO (Time Price Opportunity)
  definition_from_text: "TPO is an abbreviation for Time Price Opportunity. It has a bell-shaped structure. ... 30 minute time periods are shown here in letter form on a vertical plane." (p.19) 以 30 分钟时间块（字母）标记价格停留时间的垂直分布图。
  behavioral_mechanism: 价格在某水平停留时间越长，该水平对买卖双方越“公允”；单字母行（Single Prints / Tails）表示 OTF 在极端价格上的激进介入；Initial Balance 的宽度决定当日趋势概率。
  data_objects_involved: TPO matrix (time brackets × price levels), Initial Balance (IB), Range Extension, Tails, MPOC, D profile / P profile / b profile day types
  quant_boundary: 需要 intraday 时间-价格矩阵（30-min 或更小 bracket）；日 K 数据完全无法还原 TPO 结构。

- concept_name: Point of Control (POC / VPOC / MPOC)
  definition_from_text: "The price level at which the largest number of transactions took place is called Point of Control (VPOC)." (p.22) / "The market profile ... the widest point of the profile. This is where the price had spent the longest time." (p.21)
  behavioral_mechanism: POC 是“公允价格”的代理；Naked POC（次日未被触及）具有磁吸效应；MPOC 与 VPOC 不一致时，假突破概率增加。
  data_objects_involved: volume-at-price peak (VPOC), time-at-price peak (MPOC), Naked POC status
  quant_boundary: VPOC 可通过分钟级 volume-at-price 取 argmax；MPOC 需要 TPO 矩阵；两者可分别计算。

- concept_name: Value Area (VA) / VAH / VAL
  definition_from_text: "The Value Area is the centerpiece of the volume profile. It characterizes the area in which 70% of the total trading activities of a selected period have taken place." (p.28)
  behavioral_mechanism: VA 是机构交易者接受的价格区间；开盘价在 VA 外且停留，则新价格被接受；回归 VA 表示方向不确定。
  data_objects_involved: volume-at-price distribution, cumulative volume percentage, VAH, VAL
  quant_boundary: 标准计算：按成交量从大到小排序价格，累积至 70% 的边界；可精确计算，但需 intraday volume-at-price。

- concept_name: High Volume Node (HVN) / Low Volume Node (LVN)
  definition_from_text: "Pronounced volume clusters are called high volume areas." (p.24) / "Strong indentations are called low volume nodes. These are often located on the edge of high volume areas and can be starting points for reversals." (p.27)
  behavioral_mechanism: HVN 是大型参与者建仓区，价格回归时可能被“防守”；LVN 是快速通过区，动量在此加速，突破后常成为止盈目标。
  data_objects_involved: volume-at-price histogram, local maxima (HVN), local minima (LVN)
  quant_boundary: 可通过 price-level 成交量分布的局部极值检测；需 intraday 分钟级聚合。

- concept_name: Initial Balance (IB) and Initial Balance Range
  definition_from_text: "The letters A and B represent the first two first 30 minute periods of the institutional trading day. This period is also known as the initial balance." (p.20) / "The closer the Initial Balance (AB) at the beginning of a day compared to previous days, the higher the probability of an intraday trend." (p.21)
  behavioral_mechanism: IB 窄 → 当日趋势概率高；IB 宽 → 当日可能平衡；IB 突破（Range Extension）方向预示日内主导方向。
  data_objects_involved: first 30-60 min price range, IBH, IBL, comparison with previous days' IB
  quant_boundary: 需要明确的 institutional trading hours 起点；分钟级价格范围可计算。

- concept_name: Order Flow / Footprint Chart
  definition_from_text: "Footprint Charts, as the name suggests, show the tracks of institutional traders (OTF traders). With this order flow tool it is possible to determine if and when these have actually entered the market and when they switch." (p.70)
  behavioral_mechanism: Footprint 将每根蜡烛内部拆分为 Bid 和 Ask 成交量矩阵，通过 lift the ask / hit the bid 的不平衡揭示 OTF 的激进方向。
  data_objects_involved: bid volume per price level, ask volume per price level, imbalance multiplier, stacked imbalance, per-candle POC
  quant_boundary: 需要逐笔或聚合 bid-ask volume per price level；普通 K 线数据（仅 OHLCV）完全无法构建 Footprint。

- concept_name: Delta / Cumulative Delta
  definition_from_text: "Delta represents the difference between contracts bought and sold during a selected time period." (p.78) / "Cumulated delta curve" (p.81)
  behavioral_mechanism: Delta 正值 = 主动买入占优；负值 = 主动卖出占优；Cumulative Delta 的累积趋势与价格的背离（Absorption）揭示 OTF 的隐蔽建仓。
  data_objects_involved: per-period bid/ask volume, delta histogram, cumulative delta curve, zero line crossings
  quant_boundary: Delta 可直接从 bid-ask tagged volume 计算；Cumulative Delta 是时间序列累加；需 intraday 数据。

- concept_name: Imbalance / Stacked Imbalance
  definition_from_text: "A 'stacked imbalance' (stacked order) occurs when several imbalances are lined up on one side. This can only happen if big players act aggressively via market orders." (p.72)
  behavioral_mechanism: 单个 imbalance 可能是噪音；连续多个 price levels 出现同方向 imbalance（stacked）说明 OTF 通过 market orders 大力推动方向。
  data_objects_involved: bid-ask volume per level, imbalance ratio (e.g., ≥2x), consecutive stacked levels
  quant_boundary: 需要 per-level bid-ask volume；stacked 检测需跨多个相邻 price levels 的连续性判断。

- concept_name: Absorption / Exhaustion
  definition_from_text: "All market orders of the opposing side are 'absorbed' by iceberg orders. ... This can take place in any time frame." (p.81) / "Absorption is the most common form of market manipulation. It often takes place in connection with iceberg orders." (p.80)
  behavioral_mechanism: OTF 通过拆分 limit orders（iceberg）吸收对手方的 market orders，使价格不按 Delta 方向移动；一旦 iceberg 耗尽，价格会向 Delta 方向爆发。
  data_objects_involved: cumulative delta divergence, price stability despite large delta, footprint large numbers at single price levels, iceberg order resolution
  quant_boundary: Absorption 无法直接从 Level 1 数据识别 icebergs，但可通过 Delta-Price divergence 间接推断；需要 Level 2 或 Smart Tape 类工具才能更接近直接检测。

- concept_name: Opening Type / Day Type
  definition_from_text: "Open Drive: The market opens above yesterday's range and immediately continues... Open Rejection Reverse: The market opens outside yesterday's range, is rejected and immediately shoots in the opposite direction... Acceptance: The market opens outside yesterday's value area, but remains within yesterday's range..." (p.109)
  behavioral_mechanism: 开盘类型决定了当日早期方向结构和概率；但作者提醒不应机械套用旧理论，需结合整体语境。
  data_objects_involved: open price, previous day range, previous day VA, first 30-min price action direction
  quant_boundary: 可基于前日 VA/range 和当日开盘/前 30-min 走势自动分类；属于规则型分类器，可计算。

- concept_name: Market Structure / Trend / Balance
  definition_from_text: "A D profile is a sideways day, in many cases also an 'inside day', whose entire price range lies within the fluctuation range of the previous day. The market is 'in balance'." (p.32) / "Every major trend begins with micro inflection points." (p.18)
  behavioral_mechanism: 平衡（ sideways / D profile / accumulation）是趋势之间的建仓阶段；OTF 在平衡区隐蔽建仓，突破后产生趋势；作者用 Flexible VP 跟踪日内平衡区的 POC 位移来识别趋势重启。
  data_objects_involved: intraday range, volume profile shape (D/P/b/double distribution), POC shift, VA shift, follow through
  quant_boundary: 平衡/趋势的判定依赖形态识别和上下文，无单一阈值；可用价格范围、成交量分布集中度、POC 位移速度作为代理变量。

- concept_name: Bid-Ask Volume / Volume Delta per Candle
  definition_from_text: "The construction of a candle of a footprint chart should always be completed before considering a trading decision. ... In the main chart you can see again the black windows with POC's of the single candles." (p.76-91)
  behavioral_mechanism: 每根蜡烛的 POC 方向（上升/下降）和 Delta 数字（正/负）共同构成微方向确认；作者强调不要仅凭单根蜡烛的 imbalance 交易，而需等待 pullback 和 POC 方向一致。
  data_objects_involved: per-candle delta number, per-candle POC, per-candle bid-ask volume matrix
  quant_boundary: 需要 Footprint 级别的 bid-ask 聚合；普通 OHLCV 数据无法还原。

- concept_name: OTF (Other Time Frame) Traders
  definition_from_text: "Institutional traders are referred to as 'other time frame traders' (OTF traders) because their expectation horizon is at a higher time level than day trading." (p.16)
  behavioral_mechanism: OTF 是市场的真正方向设定者；他们通过 limit orders 隐蔽建仓，然后通过 market orders 推动价格；VP / MP / Order Flow 的最终目的都是识别 OTF 的踪迹。
  data_objects_involved: HVN accumulation, stacked imbalance, absorption, delta divergence, tails, POC shift
  quant_boundary: OTF 本身不可直接观测，是上述多个微观结构信号的联合推断对象；量化上需设计多信号融合模型而非单变量。

## QUANTIZATION_TABLE

| concept | raw_rule_from_text | observable_proxy | data_needed | quant_status | implementation_hint | notes |
|---|---|---|---|---|---|---|
| Volume Profile (VP) | 给定时期内各价格水平的成交量水平直方图 | 每个价格桶的累计成交量 | intraday volume-at-price aggregation (1-min or 5-min buckets) | proxy_quantizable_now | 可用分钟 K 的成交量按价格近似分配，但会丢失同一分钟内多价格成交量分布 | 日 K 成交量无法还原价格级别分布；分钟级是唯一可行起点 |
| Point of Control (VPOC) | 成交量最大的价格水平 | argmax(volume-at-price) | intraday volume-at-price (1-min or 5-min) | proxy_quantizable_now | 分钟 K 的成交量全部归入该分钟收盘价或典型价，取 argmax；精度有限 | 精确 VPOC 需 tick 级成交量，但分钟级可代理 |
| Naked POC | 次日未被触及的历史 POC | 当日价格区间未触及前日 POC | intraday price range + historical VPOC series | proxy_quantizable_now | 比较当日价格区间 [Low, High] 与前日 POC；需确认是否触及 | 前日 POC 来自 VP，故需先计算 VPOC |
| Value Area (VA) | 覆盖 70% 总成交量的价格区间 | 按成交量排序后累积至 70% 的边界 | intraday volume-at-price (1-min or 5-min) | proxy_quantizable_now | 标准算法：从成交量峰值向两侧扩展，累积至 70% | 分钟级聚合足够；算法成熟 |
| Value Area High (VAH) / Low (VAL) | VA 的上下边界 | VA 区间的 max / min 价格 | intraday volume-at-price (1-min or 5-min) | proxy_quantizable_now | 同 VA 计算 | 可作为支撑/阻力量化参考，但作者反对机械使用 |
| High Volume Node (HVN) | 成交量分布中的显著峰值 | volume-at-price 的局部最大值 | intraday volume-at-price (1-min or 5-min) | proxy_quantizable_now | 使用局部峰值检测或设定成交量阈值；窗口大小影响结果 | 需避免噪声峰值，建议平滑处理 |
| Low Volume Node (LVN) | 成交量分布中的显著凹陷 | volume-at-price 的局部最小值 | intraday volume-at-price (1-min or 5-min) | proxy_quantizable_now | 局部最小值检测；相邻 HVN 之间常见 LVN | 动量加速区；作者用于止盈定位 |
| Market Profile / TPO | 30-min 时间块在价格轴上的字母分布 | 每个时间 bracket 内价格访问过的价格集合 | TPO matrix with 30-min time brackets (or smaller) | needs_extra_data | 需要专门的时间-价格矩阵数据结构；普通 OHLCV 无法直接生成 | 若用 30-min K 的 OHLC 可近似，但会丢失 TPO 的字母行/单字母结构 |
| Initial Balance (IB) | 开盘后前两个 30-min 周期的价格范围 | 开盘后前 30/60 分钟的 High-Low 范围 | intraday minute data with official session open time | proxy_quantizable_now | 需明确交易所开盘时间（如 9:00 CET for Eurex）；取开盘后 N 分钟范围 | 不同市场 IB 时间不同；作者提示可调整 |
| Initial Balance Range (IBR) | IB 的宽度 | IBH - IBL | intraday minute data | proxy_quantizable_now | 直接计算 | 窄 IB 预示高趋势概率；可量化比较历史 IB 宽度分布 |
| Range Extension | IB 后价格突破 IBH/IBL | 价格超出 IB 范围的次数和方向 | intraday minute data + IB boundaries | proxy_quantizable_now | 在 IB 结束后检测价格突破 IBH/IBL | 多次同方向 Range Extension = 趋势日特征 |
| TPO Single Prints / Tails | 边缘单字母行（至少 2 个） | 某 price level 仅出现 1 个时间 bracket | TPO matrix with 30-min brackets | needs_extra_data | 必须完整 TPO 矩阵；无法从 OHLCV 还原 | 日 K 完全无法计算 |
| Market Profile POC (MPOC) | 停留时间最长的价格水平 | argmax(time-at-price) | TPO matrix with 30-min brackets | needs_extra_data | 需完整时间-价格矩阵 | MPOC 与 VPOC 不一致 = 假突破警告 |
| P Profile / b Profile / D Profile | 成交量/时间分布的形态 | 分布的偏态、峰度、单/双峰 | volume-at-price or TPO matrix | needs_extra_data | 可用分布形态统计量（skewness, kurtosis, bimodality）代理；但上下文判断难自动化 | 作者强调形态意义高度依赖语境；不宜硬编码规则 |
| Double Distribution | 分布呈现两个明显峰值 | volume-at-price 的双峰检测 | intraday volume-at-price (1-min or 5-min) | proxy_quantizable_now | 使用峰值检测算法（如 find_peaks）检测多峰结构 | 出现双分布后需关注后续方向选择 |
| Order Flow / DOM | 订单簿深度与最近成交 | 未直接给出可计算的聚合规则 | Level 2 market depth (limit orders + executions) | needs_extra_data | 需要实时订单簿数据；DOM 主要用于观察速度和大单 | 作者警告 DOM 易受 spoofing 操纵 |
| Footprint Chart | 每根蜡烛内部的 Bid/Ask 成交量矩阵 | 每根蜡烛内每个价格级别的 bid volume 和 ask volume | tick-by-tick bid/ask volume per price level (or 1-min aggregation) | needs_extra_data | 需要逐笔成交带方向标识；普通 OHLCV 无法构建 | 是订单流分析的核心可视化工具 |
| Imbalance (Footprint) | 某价格级别 market order 数量 ≥ 2x 对面 limit order | bid/ask volume ratio ≥ 2 (adjustable) | tick-by-tick bid/ask volume per price level | needs_extra_data | 需要 per-level bid/ask volume；比率可参数化 | 乘数可调整；作者建议按市场实验 |
| Stacked Imbalance | 连续多个 price levels 同方向 imbalance | 相邻 price levels 同时满足 imbalance 条件 | tick-by-tick bid/ask volume per price level | needs_extra_data | 跨价格级别的连续性检测 | 作者视为最强 OTF 信号之一 |
| Delta (per period) | 选定周期内买入合约与卖出合约之差 | Ask Volume − Bid Volume | tick-by-tick bid/ask volume or 1-min aggregated bid/ask volume | needs_extra_data | 需要从交易所获取带方向的成交量；国内数据需特别处理 | 可用分钟级 bid/ask 估算，但精度有限 |
| Cumulative Delta | Delta 的累积和 | cumsum(delta) | time series of delta per period | needs_extra_data | 基于 Delta 序列累加；需先解决 Delta 数据问题 | 是检测 Absorption 的核心工具 |
| Delta Divergence | 价格与 Delta 方向背离 | 价格新高 + Delta 未新高（或反之） | intraday price + delta series | needs_extra_data | 需要同时有价格序列和 Delta 序列；检测 lead-lag 或背离 | 作者强调这是识别操纵和反转的关键 |
| Absorption | OTF iceberg limit orders 吸收对手方 market orders | 价格稳定但 Delta 大幅单向累积 | cumulative delta + price stability | needs_extra_data | 需要 Cumulative Delta 与价格的背离检测；直接识别 iceberg 需 Level 2 | 本书订单流精髓；量化实现需间接推断 |
| Delta Profile | 将 Delta 按价格级别聚合为分布 | 每个价格级别的净 Delta（正/负） | tick-by-tick bid/ask volume per price level | needs_extra_data | 类似 Footprint，但按 Delta 聚合而非独立 bid/ask | 用于检测某价格区的单向力量陷阱 |
| Speed of Tape | 订单流速度变化 | 单位时间内成交笔数/合约数加速 | tick-by-tick execution data or 1-min volume spikes | needs_extra_data | 可用成交量 spike 作为代理；但作者用专门功能检测 | 可作为预警系统，非必需 |
| Big Trades | 大单成交警报 | 超过阈值的市场订单成交 | tick-by-tick execution data with volume | needs_extra_data | 检测单笔成交超过合约数阈值 | 作者用作辅助确认，非核心信号 |
| VWAP | 成交量加权平均价格 | 标准 VWAP 公式 | intraday price × volume per period | proxy_quantizable_now | 标准计算，但作者明确不使用 VWAP，认为其过度泛化 | 若纳入量化系统，需附加上下文过滤；不能单独作为支撑/阻力 |
| Standard Deviation Bands (VWAP) | 未在书中系统讨论 | 未明确给出 | 未明确 | shell_only | 作者未使用标准差带；若需实现，可用 VWAP ± n×std | 仅提及 VWAP 存在，未展开 |
| Opening Type Classification | 基于前日范围/VA 与当日开盘的对比分类 | 开盘价相对前日 VA/Range 的位置 + 前 30-min 方向 | intraday open + previous day VAH/VAL/Range + first 30-min price action | proxy_quantizable_now | 规则型分类器：Open Drive / Open Rejection Reverse / Acceptance 等 | 作者提醒不应机械套用，但规则本身可计算 |
| Day Type (Trend / Balance) | 日内价格范围与成交量分布形态 | 日价格范围 vs 前日范围，分布集中度 | intraday range + volume profile shape | proxy_quantizable_now | 日内范围窄而高 = 趋势；范围在昨日内部且分布钟形 = 平衡 | 分类需结合多个条件，不宜单一阈值 |
| Trend Definition (Dunnigan) | 上升底/穿透两顶 | 连续 higher lows + 突破前两个高点 | daily/intraday OHLC | proxy_quantizable_now | 可用价格序列检测；但作者用于上下文理解，非机械信号 | 属于传统技术分析的简化规则 |
| VIX Threshold | VIX > 18 机会增加；VIX > 36 应离场 | CBOE Volatility Index 实时值 | VIX daily / intraday data | proxy_quantizable_now | 公开数据；可直接作为环境过滤器 | 作者经验阈值，可作为策略开关 |
| Liquidity-Volatility Pair | 波动率过高 → 流动性枯竭 → 市场混乱 | 日内蜡烛结构（长影线、十字星、锯齿状） | intraday candle structure (OHLC) | proxy_quantizable_now | 通过蜡烛形态统计（长影线比例、重叠度）代理流动性状况 | 作者定性描述，可尝试量化 |
| POC Shift (Flexible VP) | 趋势中 POC 持续向趋势方向移动 | 滚动窗口内 POC 的序列变化 | intraday volume-at-price in rolling window | proxy_quantizable_now | 对滚动窗口（如从趋势起点到当前）计算 VP 并追踪 POC 位移 | 作者核心趋势确认方法之一 |
| Follow Through | 入场后动量应立即确认 | 入场后 N 根 candles 的价格位移/动量 | intraday minute data | proxy_quantizable_now | 可用入场后 3-5 根 candles 的位移统计代理；但作者强调语境判断 | 作者视为最重要的非机械概念；可作为辅助过滤 |

## FORMULAS_AND_ALGOS

- **Value Area 70% 规则**：对给定时期的 volume-at-price 分布，按成交量从大到小排序价格水平，从峰值向两侧扩展，直到累积成交量达到该时期总成交量的 70%。此时覆盖的价格区间即为 Value Area，上界为 VAH，下界为 VAL。（p.28）
- **POC 计算**：argmax(volume-at-price) —— 在给定时期内，成交量最大的价格水平即为 Point of Control（VPOC）。对于 Market Profile，argmax(time-at-price) 即为 MPOC。（p.21-22）
- **Delta 计算**：Delta = Ask Volume − Bid Volume（或相反，取决于符号约定）。作者使用 Delta 的正值表示主动买入占优，负值表示主动卖出占优。（p.78）
- **Cumulative Delta**：cumsum(Δt) 从选定起点开始的累加和。用于检测 Absorption：当 cum delta 持续下降但价格横盘或微涨时，推断存在 iceberg buy limit orders  absorbing sell market orders。（p.80-82）
- **Footprint Imbalance 阈值**：作者默认使用 market order 数量至少为对面 limit order 数量两倍（≥2x）作为 imbalance 的显示条件；该乘数可调整。（p.71）
- **Initial Balance Range (IBR)**：IBH − IBL，其中 IBH = 开盘后前 30/60 分钟最高价，IBL = 最低价。窄 IB（相对历史分布）预示高趋势概率。（p.20-21）
- **VIX 环境阈值**：VIX > 18 时，盈利价格运动概率显著增加；VIX > 36 时，不应再入场（"Fear Factor too large"）。（p.96）
- **Broadening Top 回撤幅度**：从 point 5 的下跌突破 point 4 后，回撤通常达到 point 4 到 point 5 价格波动的 40%–60%。（p.123）
- **Take Profit 初始规则**：初学者建议将止盈目标设为初始风险的 3 倍；有经验的交易者可将止盈置于前方 Low Volume Zone（薄区）。（p.198-199）
- **Stop Loss 定位原则**：作者反对使用 ATR 等滞后指标计算止损；建议将止损设在 entry 附近的 POC 级别之外（"just above / below the price level of the POC located near the entry point"），并设置时间止损（如 3 根蜡烛后无 follow through 即离场）。（p.201-202）

## NOT_QUANT_YET

1. **Contextual Thinking / Puzzle Assembly**：作者反复强调“分析是拼图”，必须结合多个时间框架、多个工具和整体语境。这种综合判断无法通过单一公式或固定规则量化，需要多源信息融合框架（如 LLM-based 或 rule-based expert system），目前不在标准量化管线中。
2. **OTF Presence Inference**：虽然 HVN、Stacked Imbalance、Absorption 等可作为 OTF 的代理信号，但“OTF 是否在场”本质是一个隐变量推断问题，缺乏 ground truth。作者的所有结论都是后验解释，无法通过历史数据直接验证 OTF 行为。
3. **Absorption 的直接检测**：作者描述 iceberg orders 通过 limit orders 吸收 market orders，导致价格不移动。但 iceberg orders 在 Level 2 中也难以直接识别（只有 Smart Tape 等工具尝试破解），在标准 tick 数据中几乎不可观测。Delta-Price divergence 只能间接推断，无法直接测量 absorption 强度。
4. **P / b / D Profile 的上下文意义**：作者明确指出 P profile 在趋势起点看涨、在趋势末端看跌；D profile 是平衡但可能孕育突破。这种形态-语境的映射依赖人工判断，缺乏可编程的客观阈值。
5. **Follow Through 的语境判断**：作者将 Follow Through 视为“最重要的因素”，但从未给出固定的时间或位移阈值。它是一个“感觉”和“即时确认”概念，难以编码为固定规则而不导致过度拟合。
6. **Fake Moves 的意图识别**：Backfire、SHS Fake、Squeeze 等模式的核心是识别“谁在输钱”，即市场 maker 的意图。这需要对流动性陷阱和订单簿动态的深层理解，目前无法通过价格/成交量序列自动分类。
7. **Speed of Tape 与 Big Trades**：作者使用这些作为早期预警，但明确说明它们是“非必需的”。这些功能依赖软件内部的实时执行流分析，标准历史数据无法还原其精确行为。
8. **Ledge / Ross Hook 的精确检测**：虽然 Ledge 是平行迷你盘整区，但其识别依赖人工画线（“connecting two absolute highs or lows”）和主观判断（4-8 根蜡烛）。自动化的通道检测算法会产生大量假阳性，需要 Volume Profile 的 POC 位移作为确认过滤器。
9. **Unfinished Auction / Weak Highs and Lows**：这些概念涉及“未完成的拍卖”和“犹豫状态”，需要检测价格极值的重复测试及对应订单流的缺乏确认。虽然价格部分可检测，但“犹豫”的订单流确认需要 Footprint 数据。
10. **Market Profile 传统日型分类的机械失效**：作者多次提醒“older theories should not be taken too closely, especially today”（p.19）。传统日型（trend day, normal day, neutral day 等）的分类在当代市场已部分失效，不宜直接作为量化特征输入。
11. **Instrument-Specific Behavior**：Dax 的“optioned”特性、Gold 的季节性合约流动性、Oil 的库存新闻前 insider 行为等，属于作者的经验知识，缺乏可复用的数据源或通用规则。
12. **DOM / Order Book Manipulation (Spoofing)**：作者警告 DOM 易被 spoofing 和 fake limit orders 操纵，因此 DOM 数据本身不适合作为稳定的量化输入。识别 spoofing 需要模式识别而非简单统计。

## NEXT_ACTION

1. **建立 Volume Profile 基础数据结构**：在量化框架中实现 intraday volume-at-price 聚合模块（1-min 或 5-min buckets），支持固定窗口（Fixed VP：前日/24h/周）和滚动窗口（Flexible VP：日内动态）两种模式。这是本书所有 VP 相关量化分析的基础设施。
2. **实现标准 VP 统计量计算**：基于 volume-at-price 聚合，实现 VPOC、VA（70% 规则）、VAH、VAL、HVN（局部峰值）、LVN（局部谷值）的标准算法。验证分钟级聚合与专业软件（如 Atas）结果的近似一致性。
3. **获取 bid-ask tagged intraday 数据**：评估并采购/接入带买卖方向的逐笔或分钟级期货数据（如 CME/欧交所 Top-of-Book 或 Level 2）。这是实现 Delta、Footprint、Imbalance、Absorption 等订单流概念的必要前提；若无法获取，则需明确标注为“不可量化”。
4. **设计 Delta 与 Cumulative Delta 计算管线**：一旦获得 bid-ask 数据，实现 per-period Delta（Ask − Bid）和 Cumulative Delta 的实时/历史计算。重点验证 Delta-Price Divergence 的检测逻辑（价格新高/新低但 Delta 未确认）。
5. **构建 TPO 矩阵原型**：实现 30-min bracket（或 15-min / 1-hour）的时间-价格矩阵，支持 Initial Balance（A/B period）自动提取、Range Extension 检测、Single Prints / Tails 计数。作为 Market Profile 数字化的最小可行产品。
6. **开发双 POC 差异信号（MPOC vs VPOC）**：在同时支持 TPO 和 VP 的框架中，比较 MPOC 与 VPOC 的位置差异。当两者不一致时，输出警告信号（作者认为此时假突破概率增加）。
7. **实现 VA 开盘测试规则**：自动比较当日开盘价与前一交易日 VAH/VAL 的关系，并追踪开盘后前 30-60 分钟的价格是否停留在 VA 外（Acceptance）或回归 VA 内（Rejection）。作为 Opening Type 分类器的子模块。
8. **评估 Stacked Imbalance 的近似检测**：若无法获取完整 Footprint 数据，研究是否可用分钟级 bid-ask 成交量不平衡的连续检测作为 Stacked Imbalance 的粗糙代理。明确近似误差和适用边界。
9. **建立 VIX 环境过滤器**：将 VIX 实时/日数据接入策略环境，实现作者建议的阈值规则（VIX > 18 允许入场，VIX > 36 禁止入场）。作为全局风险开关。
10. **记录 Instrument-Specific 边界文档**：针对本书涉及的每个品种（E-Mini, Dax, Bund, EURUSD, JPY, Gold, Oil, Hang Seng, Nikkei），整理其作者提到的特殊行为（流动性时段、合约切换、假突破频率、Delta 可靠性等），形成量化实现的约束清单。
11. **设计 Follow Through 代理指标**：虽然作者拒绝固定阈值，但可尝试用入场后 N 个周期的位移/动量/ATR 倍数作为 Follow Through 的量化代理，并记录其与传统止损的对比表现。明确标注这是“代理”而非原文概念。
12. **组织跨资料关联（F2 → A2/F1）**：将本书中提取的 quantizable 概念（POC, VA, HVN, LVN, Delta Divergence, Absorption Proxy）与 A2（订单流特征工程）和 F1（成交量分布策略）的工作项对接，确保数据结构一致、术语统一、避免重复开发。

