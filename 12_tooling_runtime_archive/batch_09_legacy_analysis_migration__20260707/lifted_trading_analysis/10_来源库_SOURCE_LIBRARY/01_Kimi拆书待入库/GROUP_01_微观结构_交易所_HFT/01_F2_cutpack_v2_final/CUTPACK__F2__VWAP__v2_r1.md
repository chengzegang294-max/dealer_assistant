## BASIC_INFO
- title: VWAP: The Insider's Guide To Trading
- author: Trader Dale
- material_type: 交易技术教材/教程
- domain_tags: [VWAP, execution, volume-weighted price, standard deviation bands, institutional trading, anchored VWAP, session VWAP]
- file_scope: VWAP The Insiders Guide To Trading (Trader Dale) (Z-Library).pdf
- source_file_size_mb: 6.63
- retain_mode: RETAINED_EXCERPTS
- current_repo_role: SECONDARY_STRUCTURED_NOTE

## MATERIAL_POSITIONING
- what_this_book_is: 一本面向手工交易者的VWAP与Anchored VWAP实用指南，以图表案例和主观锚定策略为主，包含对机构执行逻辑的简短引证。
- why_in_f2: 提供VWAP定义、计算公式、Citadel等机构对VWAP执行的证词、以及VWAP Bands（标准差带）的入门级描述，可作为后续执行质量与微观结构分析的参考锚点。
- not_a_strategy_book_because: 书中绝大部分内容为“价格回到VWAP即入场”的主观技术形态与止损止盈管理，不含可回测的量化规则、不含算法执行细节、不含标准差带的数学推导。
- relation_to_order_flow_microstructure: 仅通过引用Kenneth Griffin证词点出机构使用VWAP算法切片执行；其余内容属于价格行为与成交量分布的 discretionary trading 范畴，与订单流微观结构教材（如Harris、OHara）不在同一层级。
- data_footprint_required: 如需复现书中图表，需要1-5分钟K线+成交量；如需验证机构执行逻辑，需要券商/交易所的execution log与fill data；如需计算标准差带，需要分钟级成交量加权价格序列。

## CONTENT_STRUCTURE
- 1. Introduction to VWAP — 定义、与SMA/EMA的区别、计算公式与示例
- 2. Why does VWAP work? — 机构订单占比、算法交易、Citadel CEO证词引用
- 3. Where to get VWAP — 平台与指标来源（TradingView等）
- 4. Strategy #1: Reactions to VWAP — 价格回撤VWAP作为支撑/阻力
- 5. Anchoring VWAP — 锚定原理：Day/Week/Year、swing points、trend start、macro news、heavy volume zones、gaps、earnings
- 6. Strategy #2: Reactions to 1st VWAP deviations — VWAP Rotation strategy（横盘）与 VWAP Trend strategy（趋势）
- 7. Confluences with other strategies — 与Price Action、Volume Profile的叠加使用
- 8. Trade entry confirmation — 首次触碰、成功反应后入场、Order Flow confirmation（Absorption、Limit Order、Cumulative Delta divergence）
- 9. Take Profit / Stop Loss placement — 基于VWAP、Price Action、Volume Profile、ATR的退出规则
- 10. Trailing your trade — 随趋势移动止损
- 11. Money management — 单笔风险、仓位计算
- 12. Appendix — 课程推广、软件工具、用户评价

## RETAINED_EXCERPTS

- excerpt_id: R01
  source_hint: Page 8, Introduction to VWAP
  quote: "VWAP, which stands for Value Weighted Average Price, is essentially an average price that takes into account the trading volume. It provides insight into where the average trader placed their orders."
  why_kept: 书中对VWAP的基础定义，直接对应quant_boundary中的volume-weighted average概念。
  quant_link: VWAP核心公式

- excerpt_id: R02
  source_hint: Page 8, Formula section
  quote: "Example #1: Imagine there were 1.000 shares traded at $10, and 5.000 shares traded at $20. SMA = ($10 + $20)/2 = $15. VWAP = (($10 x 1.000) + ($20 x 5.000)) / 6.000 = $18.33"
  why_kept: 包含VWAP的显式计算示例，可直接还原为公式 Σ(Price × Volume) / Σ(Volume)。
  quant_link: VWAP公式推导

- excerpt_id: R03
  source_hint: Page 8-9, SMA vs VWAP comparison
  quote: "Example #2: Imagine there were only 100 shares traded at $5, and 5.000 shares traded at $20. SMA = ($5+$20)/2 = $12.5. VWAP = (($5 x 100) + ($20 x 5.000)) / 5.100 = $19.7"
  why_kept: 极端成交量差异下的SMA与VWAP对比，说明volume-weighting在反映真实平均成交价格时的必要性。
  quant_link: VWAP vs SMA偏差分析

- excerpt_id: R04
  source_hint: Page 9, Why does VWAP work?
  quote: "Fact #1: The majority of trading orders in the financial markets come from large trading institutions. Fact #2: These trading institutions primarily use automated systems or algorithms to execute their trades. Fact #3: What's noteworthy is that many of these automated systems rely on VWAP as part of their trading strategies."
  why_kept: 将VWAP与机构算法执行关联，是全书唯一涉及执行层面的微观结构论述。
  quant_link: Institutional execution / VWAP benchmark

- excerpt_id: R05
  source_hint: Page 10, Kenneth Griffin testimony
  quote: '"Today, virtually all trades executed by institutional investors are in the form of program trades such as volume-weighted average price (VWAP) and other algorithmic trades."'
  why_kept: 来自Citadel CEO的国会证词，是全书关于机构VWAP执行最强有力的外部引用。
  quant_link: VWAP as execution benchmark

- excerpt_id: R06
  source_hint: Page 10, Kenneth Griffin testimony
  quote: '"These VWAP trades are not large trades that you can—it's not like there's 10 million shares to be bought. It is a trade that is sliced into small slices, 100 or 200 shares, and executed over the course of a day, a week, or a month."'
  why_kept: 直接描述VWAP算法执行中的订单切片（order slicing）与时间维度上的分散执行，对应执行成本与市场冲击。
  quant_link: Algorithmic trading to VWAP / Market Impact / Slippage

- excerpt_id: R07
  source_hint: Page 10, Kenneth Griffin testimony
  quote: '"We use VWAP orders to execute on behalf of our hedge fund and have generated exceptional returns for pension plans and for endowments."'
  why_kept: 说明VWAP订单不仅用于执行基准，也被用于为大型机构客户（养老金、捐赠基金）执行。
  quant_link: Institutional execution vs VWAP

- excerpt_id: R08
  source_hint: Page 13, Daily VWAP
  quote: "If you set the VWAP's starting point at the beginning of the trading day, it will reflect the average trader's position since the start of that day. This particular VWAP, anchored at the start of the day, is commonly referred to as the 'Daily VWAP' and is widely used in trading."
  why_kept: 定义Session VWAP（Daily VWAP）的起算点与概念，是后续量化中session-based VWAP计算的基础。
  quant_link: Session VWAP / Daily VWAP

- excerpt_id: R09
  source_hint: Page 16, Start of the Day
  quote: "The VWAP calculation begins at the start of the Asian trading session and concludes at the end of the US trading session."
  why_kept: 明确书中Daily VWAP的计算区间（Asian session start to US session end），对24小时市场（如外汇）的session界定有参考价值。
  quant_link: Session VWAP / Daily VWAP

- excerpt_id: R10
  source_hint: Page 20, Start of the week
  quote: "A VWAP that starts at the beginning of the trading week (at the start of the Asian Session on Monday) is known as the Weekly VWAP."
  why_kept: Weekly VWAP的定义，对应多时间周期VWAP的session划分。
  quant_link: Session VWAP / Weekly VWAP

- excerpt_id: R11
  source_hint: Page 21, Start of the year
  quote: "A VWAP that begins on the first day of the year and ends on the last day is known as the Yearly VWAP. It's one of my top choices for swing trading or long-term trading, and I typically use it on a Daily timeframe."
  why_kept: Yearly VWAP的定义，用于长期交易中的volume-weighted average锚点。
  quant_link: Session VWAP / Yearly VWAP

- excerpt_id: R12
  source_hint: Page 13-14, Anchoring VWAP concept
  quote: "What all these anchoring methods share in common is their placement at crucial points in the market – points where market participants make crucial decisions, where sentiments shift, and the rules of the game change."
  why_kept: Anchored VWAP的核心思想：锚定在市场结构转折点，而非固定时间窗口。这决定了其主观性与不可机械化回测。
  quant_link: Anchored VWAP

- excerpt_id: R13
  source_hint: Page 14, The strategy
  quote: "For a Long trade: If the price is above VWAP (meaning buyers are in control) and it comes back down to VWAP from above, that's when you enter a Long position as the price touches VWAP. For a Short trade: If the price is under VWAP (showing that sellers are in charge) and it comes back up to VWAP from below, that's your signal to enter a Short position as the price touches VWAP."
  why_kept: 书中最基本的VWAP交易逻辑。需保留但需标记为 discretionary / shell_only，因为缺乏客观的“触碰”定义与统计验证。
  quant_link: VWAP as support/resistance（保守处理）

- excerpt_id: R14
  source_hint: Page 47, Strategy #2: Reactions to 1st VWAP deviations
  quote: "VWAP deviations, often referred to as 'bands,' consist of two lines positioned both above and below the VWAP line. These lines move alongside the VWAP and are calculated based on it."
  why_kept: 对VWAP Bands（标准差带）的入门级定义，说明其存在但书中未给出具体数学公式。
  quant_link: Standard Deviation Bands / VWAP Bands

- excerpt_id: R15
  source_hint: Page 48, Distinguishing rotation vs trend
  quote: "If the deviations are moving horizontally, it indicates that the market is in a rotation: When the deviations move vertically, at least one of them, it signals that the market is in a trend."
  why_kept: 将标准差带的几何形态（水平/垂直）用于判断市场状态（rotation vs trend）。这是主观视觉判断，但可作为后续量化中band-angle proxy的参考。
  quant_link: VWAP Bands / Standard Deviation Zones

- excerpt_id: R16
  source_hint: Page 49, The setting
  quote: "I exclusively use the 1st deviations in conjunction with VWAP anchored to specific dates. This means VWAP anchored to the start of a day, week, or year."
  why_kept: 说明书中VWAP Bands的使用范围限制（仅与时间锚定VWAP联用），排除了其他锚定方式下的标准差带应用。
  quant_link: Standard Deviation Bands / VWAP Bands

- excerpt_id: R17
  source_hint: Page 50, VWAP Rotation strategy
  quote: "When the market behaves like this, the price typically stays within the upper and lower 1st deviation lines. The upper 1st deviation acts as a Resistance level, while the lower 1st deviation serves as a Support level."
  why_kept: 标准差带在横盘行情中的主观支撑/阻力用法。需保守标记，因为缺乏统计验证与可量化边界。
  quant_link: Standard Deviation Zones (1σ)

- excerpt_id: R18
  source_hint: Page 54, VWAP Trend strategy
  quote: "For a Long Trade Scenario: Look for the upper deviation to trend upward (moving vertically). Confirm that the price is positioned above the upper Deviation. Enter a Long trade when the price touches the upper deviation from above."
  why_kept: 趋势行情下对1st deviation的另一种主观用法。同样需标记为shell_only，因为“trend upward”缺乏客观度量。
  quant_link: Standard Deviation Zones (1σ)

- excerpt_id: R19
  source_hint: Page 38, Anchoring VWAP to heavy volume zones
  quote: "Heavy volume zones are crucial areas on a chart where large trading institutions have been actively placing many orders. These zones hold significant importance because it's these big players who have the ability to influence and even manipulate the markets."
  why_kept: 将成交量密集区与机构行为关联，为VWAP锚定提供成交量分布逻辑。对应volume-at-price概念。
  quant_link: Volume-at-price distribution around VWAP

- excerpt_id: R20
  source_hint: Page 39, Heavy volume zones and VWAP
  quote: "The trading approach here is to anchor the VWAP at the end of the consolidation zone, right where the trend begins. After that, you trade it as usual, jumping in at the pullbacks."
  why_kept: 将volume profile中的rotation zone与VWAP锚定结合，说明成交量分布如何决定锚定点选择。
  quant_link: Volume-at-price distribution around VWAP

- excerpt_id: R21
  source_hint: Page 82, Order Flow confirmation
  quote: "Order Flow analysis displays all executed orders in the market, allowing you to track the actions of major trading institutions that influence and manipulate markets. You can see where these significant players are placing their large orders."
  why_kept: 提及Order Flow作为机构交易行为的确认工具，与VWAP形成互补验证。
  quant_link: Order Flow / Institutional execution

- excerpt_id: R22
  source_hint: Page 83, Absorption
  quote: "This situation indicates that buyers are aggressively trying to push the price up (visible on the Ask side), but at the same time, sellers are also selling aggressively, as evidenced by the large orders on the Bid side. Essentially, the sellers are absorbing the buying pressure."
  why_kept: Order Flow中的Absorption概念，可作为机构在VWAP附近进行被动成交的微观结构描述。
  quant_link: Slippage / Market Impact

- excerpt_id: R23
  source_hint: Page 84, Limit Order confirmation
  quote: "A significant player was waiting at this Resistance level, and when the price reached it, they initiated a pending Short trade. This type of confirmation is valuable when considering whether to take the trade or not."
  why_kept: 描述机构在VWAP/标准差带附近挂Limit Order的行为，对应微观结构中的被动订单簿策略。
  quant_link: Institutional execution vs VWAP

- excerpt_id: R24
  source_hint: Page 85, Cumulative Delta divergence
  quote: "Cumulative Delta essentially illustrates the difference between bid and ask, which boils down to the distinction between aggressive buyers and sellers. When Cumulative Delta rises, it indicates that aggressive buyers are in control, whereas a decline suggests that aggressive sellers are taking the lead."
  why_kept: Cumulative Delta的定义，可用于与VWAP结合进行aggressive vs passive flow的微观结构分析。
  quant_link: Order Flow / VWAP deviation

- excerpt_id: R25
  source_hint: Page 19, Broken VWAP
  quote: "In simple terms, if the price is above VWAP, it acts as Support. If the price is below VWAP, it becomes a Resistance. This can happen several times in a day!"
  why_kept: VWAP角色切换（支撑变阻力/阻力变支撑）的描述，但需明确这是主观价格行为断言，未经过统计检验。
  quant_link: VWAP hold / VWAP rejection

- excerpt_id: R26
  source_hint: Page 12, Institutional trading logic around VWAP
  quote: "In a hedge fund or a bank, supervisors might instruct traders to 'Short X amount of lots on EUR/USD today, and do it at VWAP or better,' with 'better' meaning a price above VWAP."
  why_kept: 直接引用机构内部的交易指令格式，说明VWAP作为执行基准在buy-side/sell-side中的实际应用语言。
  quant_link: VWAP as execution benchmark

- excerpt_id: R27
  source_hint: Page 32, Macro news anchoring
  quote: "Here's a list of the most crucial news events that are likely to do just that and are ideal for anchoring VWAP: Rate decision and Minimum Bid Rate, FOMC Meeting and Monetary Policy Statement, CPI, GDP, NFP, Unemployment Rate."
  why_kept: 明确可用于VWAP锚定的高影响力宏观事件清单，对事件驱动型VWAP研究有参考意义。
  quant_link: Anchored VWAP / Macro news

- excerpt_id: R28
  source_hint: Page 33, Macro news impact qualification
  quote: "You're looking for macro news that kickstarts action, like a new trend. If the news only makes the price briefly jump up and down before settling back to its previous state, then it wasn't the game-changing news you were seeking."
  why_kept: 对宏观事件影响力的定性筛选标准——必须引发趋势转变而非短暂波动。说明锚定选择的主观判断属性。
  quant_link: Anchored VWAP / Macro news

- excerpt_id: R29
  source_hint: Page 77, Entering a trade at first touch
  quote: "This approach is the riskiest, especially if you solely rely on VWAP setups without any other supporting strategies... I do not recommend trading this way. While it's the easiest, it's also the riskiest."
  why_kept: 作者本人明确警告“首次触碰即入场”是最危险的方式，这支持了“VWAP支撑阻力不是强量化信号”的保守立场。
  quant_link: VWAP as support/resistance（保守处理）

- excerpt_id: R30
  source_hint: Page 78, Entering a trade after a successful reaction
  quote: "For a long trade entry from a VWAP-based support, look for one bullish candle to close ABOVE the Support level. For a short trade, watch for a bearish candle to close below the Resistance level."
  why_kept: 作者推荐的确认式入场方式，但仍然基于主观蜡烛图形态，缺乏可量化的统计阈值。
  quant_link: VWAP as support/resistance（保守处理）

- excerpt_id: R31
  source_hint: Page 96, Stop Loss behind barrier
  quote: "The key rule to remember when setting your Stop Loss is to always position it BEHIND a barrier, which is represented by a Support or Resistance zone. This barrier can be identified through Price Action, VWAP, or Volume Profile analysis."
  why_kept: 书中通用的风险管理框架，将VWAP视为“barrier”之一，但本质是主观技术位而非统计边界。
  quant_link: VWAP as support/resistance（保守处理）

- excerpt_id: R32
  source_hint: Page 98, VWAP-based Stop Loss placement
  quote: "As you can observe, the price eventually moves significantly above the VWAP. In such a case, I recommend searching for other Support levels to move your Stop Loss to because the VWAP is now too far away, and having the Stop Loss behind it would be too distant."
  why_kept: 说明VWAP作为止损屏障的局限：随着价格远离VWAP，其保护作用下降，需切换其他参考位。
  quant_link: VWAP deviation / VWAP hold

- excerpt_id: R33
  source_hint: Page 105, Trailing your trade
  quote: "To trail your trade, continuously adjust your Stop Loss (moving it higher in an uptrend) as the trend develops... always placing your Stop Loss behind a strong Price Action, VWAP, or Volume Profile barrier."
  why_kept: 追踪止损的通用原则，再次强调VWAP被用作动态屏障，但无具体量化调整步长。
  quant_link: VWAP as support/resistance

- excerpt_id: R34
  source_hint: Page 112, Risk per trade
  quote: "Start by backtesting your trading strategy. This will show you how your strategy performed over time. The most crucial thing you'll learn from this is the biggest loss your strategy had in the past, known as the 'drawdown.'"
  why_kept: 作者提及回测作为风险管理的输入，但全书未提供任何可回测的量化规则或数据集。
  quant_link: Money management / Backtesting

- excerpt_id: R35
  source_hint: Page 113, Position sizing
  quote: "It's really important to use the same amount of money for all your trades. For instance, if you decide to risk 2% of your account balance on each trade, make sure you always follow this rule."
  why_kept: 固定比例仓位管理原则，属于通用的资金管理系统，与VWAP本身无直接量化关联。
  quant_link: Money management

- excerpt_id: R36
  source_hint: Page 72, Multiple setups combo
  quote: "When both of these setups highlight the same Support level, it becomes a robust Support zone. In simpler terms, when two strategies agree on a level, it becomes a strong level with a better chance of a successful reaction."
  why_kept: Confluence（多指标共振）逻辑，说明作者依赖多源确认而非单一VWAP信号，进一步降低VWAP独立量化可行性。
  quant_link: Confluence / VWAP as support/resistance

- excerpt_id: R37
  source_hint: Page 40, Example #1 Bitcoin daily chart
  quote: "A rotation where heavy volumes were traded. An uptrend is starting from the rotation. VWAP anchor point."
  why_kept: 图表标注示例，展示Volume Profile与VWAP锚定的结合方式。保留作为可视化案例参考。
  quant_link: Volume-at-price distribution around VWAP

- excerpt_id: R38
  source_hint: Page 26, Example #2 Apple stock daily chart
  quote: "When the price hit the VWAP, it attracted buyers looking for a good price. Their aggressive buying activity helped push the price higher once again."
  why_kept: 对VWAP作为“fair price”吸引aggressive buyers的定性描述，可关联到execution microstructure中的被动订单簿吸引逻辑。
  quant_link: VWAP as execution benchmark

- excerpt_id: R39
  source_hint: Page 28, VWAP anchored to start of the trend
  quote: "Typically, this doesn't lead to significant differences, and the VWAP provides similar Support and Resistance levels. However, if two traders anchor their VWAPs to candles that are too far apart, their VWAP lines may diverge more."
  why_kept: 明确指出Anchored VWAP的主观性：不同交易者选择的锚定点不同，会导致VWAP线 diverge。这是不可量化的核心原因。
  quant_link: Anchored VWAP

- excerpt_id: R40
  source_hint: Page 86, Take Profit placement rule
  quote: "Always exit your trade a bit before it reaches a significant barrier which could prevent the price moving further. These barriers are strong Support or Resistance levels identified through Price Action, VWAP, or Volume Profile analysis."
  why_kept: 通用的止盈原则，将VWAP视为潜在反转屏障。保留作为交易管理中的参考逻辑，但非量化信号。
  quant_link: VWAP as support/resistance

## CORE_CONCEPTS

- concept_name: VWAP (Volume/Value Weighted Average Price)
  definition_from_text: "an average price that takes into account the trading volume... provides insight into where the average trader placed their orders."
  behavioral_mechanism: 通过将每笔成交价格按其成交量加权，反映市场参与者的真实平均持仓成本；区别于SMA/EMA等纯时间序列平均。
  data_objects_involved: 成交价格(Price)、成交量(Volume)、时间戳
  quant_boundary: 可精确计算，但书中未涉及tick-level implementation；日K近似可用OHLCV×Volume估算，分钟级精度需intraday data。

- concept_name: Anchored VWAP
  definition_from_text: "VWAP can be anchored in various ways... placement at crucial points in the market – points where market participants make crucial decisions."
  behavioral_mechanism: 将VWAP的计算起点从固定session起点（如开盘）改为市场结构转折点（swing high/low、macro news、trend start等），从而追踪自该点以来的平均成交位置。
  data_objects_involved: 锚定点选择、成交价格、成交量、时间序列
  quant_boundary: 锚定点的选择高度主观（“two traders might choose different candles”），导致同标的在不同交易者图表上产生 divergent VWAP lines；不可直接作为标准化量化输入。

- concept_name: VWAP Standard Deviation Bands (Deviations)
  definition_from_text: "VWAP deviations, often referred to as 'bands,' consist of two lines positioned both above and below the VWAP line... calculated based on it."
  behavioral_mechanism: 围绕VWAP计算标准差倍数线，形成波动区间；1st deviation的水平/垂直走向被用于主观判断rotation vs trend。
  data_objects_involved: VWAP序列、价格序列、标准差乘数、成交量（是否volume-weighted未明确）
  quant_boundary: 书中未给出标准差带的具体数学公式；未说明是否使用volume-weighted standard deviation；未定义1st/2nd/3rd deviation的乘数；因此无法直接复现。

- concept_name: Session VWAP (Daily / Weekly / Yearly)
  definition_from_text: "Daily VWAP: anchored at the start of the trading day... Weekly VWAP: starts at the beginning of the trading week... Yearly VWAP: begins on the first day of the year."
  behavioral_mechanism: 固定时间窗口内的成交量加权平均，反映该session内市场参与者的平均成本。
  data_objects_involved: Session边界定义、intraday OHLCV数据
  quant_boundary: Daily/Weekly/Yearly VWAP在概念上可精确计算，但书中对session边界（如Asian session start）缺乏严格定义；跨时区品种（forex）需统一时区处理。

- concept_name: Institutional VWAP Execution
  definition_from_text: "virtually all trades executed by institutional investors are in the form of program trades such as volume-weighted average price (VWAP) and other algorithmic trades... sliced into small slices, 100 or 200 shares, executed over the course of a day."
  behavioral_mechanism: 机构使用VWAP算法将大额订单切片分散执行，以最小化市场冲击并接近当日成交量加权平均价格。
  data_objects_involved: 订单簿、成交切片、时间序列、执行日志、市场成交量分布
  quant_boundary: 书中仅引用外部证词，未提供算法细节、切片逻辑、参与率（participation rate）或冲击成本模型；需要execution report和fill data才能验证。

- concept_name: VWAP as Support / Resistance (Fair Price)
  definition_from_text: "VWAP represents the trading position of an average trader, and many market participants use it as a reference point for their trade entries... 'do it at VWAP or better.'"
  behavioral_mechanism: 市场参与者将VWAP视为“公平价格”，当价格回撤至VWAP时，买方/卖方在“公平价”附近重新介入，形成价格反应。
  data_objects_involved: 价格序列、VWAP序列、主观视觉判断
  quant_boundary: 这是全书最主观的内容：无定义“触碰”的精确阈值（价格穿透多少算触碰？），无统计验证（成功率、样本量、不同品种差异），无客观的入场/出场规则；不可直接作为量化信号。

- concept_name: VWAP Deviation / Hold / Rejection
  definition_from_text: "If the price is above VWAP, it acts as Support. If the price is below VWAP, it becomes a Resistance... The price broke through VWAP, turning what used to be a Support into a Resistance."
  behavioral_mechanism: 价格与VWAP的相对位置被用于判断多空主导权；VWAP被突破后角色转换。
  data_objects_involved: 价格序列、VWAP序列、突破方向
  quant_boundary: “突破”缺乏可量化的定义（收盘价突破？影线突破？穿透幅度？），“角色转换”未经统计检验；属于价格行为叙事而非量化规则。

- concept_name: Order Flow Confirmation (Absorption / Limit Order / Cumulative Delta)
  definition_from_text: "Absorption: sellers are absorbing the buying pressure... Limit Order: a huge order on the Ask side... Cumulative Delta: difference between bid and ask."
  behavioral_mechanism: 在VWAP附近使用订单流数据（逐笔成交 footprint、累积差量）确认机构行为与潜在反转。
  data_objects_involved: Tick/逐笔数据、Bid/Ask成交量、Limit Order识别、Cumulative Delta序列
  quant_boundary: 需要Level 2或逐笔数据（footprint chart）；书中仅提供视觉描述，未提供可编程的识别规则（如“huge order”的阈值是多少？）。

## QUANTIZATION_TABLE

| concept | raw_rule_from_text | observable_proxy | data_needed | quant_status | implementation_hint | notes |
|---|---|---|---|---|---|---|
| VWAP (intraday session) | VWAP = Σ(Price × Volume) / Σ(Volume) | 分钟级VWAP数值序列 | 1-min OHLCV with actual volume; session start/end timestamps | needs_extra_data | Use typical price (H+L+C)/3 or close × volume per bar, accumulate from session start. | 书中示例使用单笔价格×股数，实际bar数据需用典型价或VWAP of bar近似。 |
| VWAP (daily approximation) | 同上，但书中未提供日K近似 | 日K VWAP近似值 = Σ(Close × Volume) / Σ(Volume) 在多日内 | Daily OHLCV bars | proxy_quantizable_now | 对日K级别可用Close×Volume近似，但会丢失日内结构。 | 严格来说不是intraday VWAP，但可作为long-term benchmark proxy。 |
| Daily VWAP | 锚定至Asian session start，结束于US session close | 当日0时至当前时刻的累计成交量加权平均 | 1-min OHLCV for forex/24h markets; precise session boundary definition | needs_extra_data | 需先统一时区（如UTC），定义session边界。 | 书中对Asian session start未给出精确时间，需外部定义。 |
| Weekly VWAP | 锚定至Monday Asian session start | 本周累计成交量加权平均 | 1-min OHLCV for the week | needs_extra_data | 周一00:00 UTC起算，逐bar累计。 | 作者偏好在30-min timeframe上使用。 |
| Yearly VWAP | 锚定至1月1日 | 本年度累计成交量加权平均 | Daily OHLCV for the year | needs_extra_data | 1月1日首个bar起算，逐日累计。 | 作者用于swing trading on daily charts。 |
| Anchored VWAP (swing point) | 锚定至“重要高低点” | 自选定高低点以来的累计VWAP | 1-min OHLCV + 高低点识别规则 | needs_extra_data | 高低点识别可用fractal/pivot指标，但锚定选择仍主观。 | 作者明确表示不同交易者可能选不同蜡烛。 |
| Anchored VWAP (macro news) | 锚定至“改变市场情绪的宏观新闻K线” | 自宏观新闻发布bar以来的累计VWAP | 1-min OHLCV + 宏观事件时间戳 | needs_extra_data | 需高影响力事件数据库（FOMC、NFP、CPI等）与精确发布时刻。 | 书中未给出事件影响的自动化判断标准。 |
| Anchored VWAP (trend start) | 锚定至“趋势开始的第一个大K线” | 自趋势起点bar以来的累计VWAP | 1-min OHLCV + 趋势起点检测 | needs_extra_data | 趋势起点可用结构突破（BOS/CHoCH）或动量阈值自动检测，但仍有主观性。 | 作者说“two traders might choose different candles”。 |
| VWAP Standard Deviation Bands (1st) | “bands... calculated based on VWAP” | 1st deviation = VWAP ± k × σ(Price?) | 1-min OHLCV + VWAP序列 | needs_extra_data | 书中未给出公式。假设可用volume-weighted standard deviation of typical price around VWAP，乘数需校准。 | 作者未说明是标准差、ATR、还是其他带宽计算；也未给出乘数。 |
| VWAP Standard Deviation Bands (2nd, 3rd) | 书中仅提及1st deviation，未明确2nd/3rd | VWAP ± 2σ, VWAP ± 3σ（假设） | 同上 | needs_extra_data | 标准差带乘数需通过历史数据校准；书中未提供。 | 标准差带向更高倍数延伸时，样本量要求显著增加。 |
| VWAP as execution benchmark | “do it at VWAP or better” | 实际成交均价 vs VWAP的偏差（slippage） | Full execution report with fill prices and sizes; intraday market VWAP | future_bucket | 需要券商/交易所提供的execution log，计算fill price与session VWAP的差。 | 书中无具体实现，仅引用机构证词。 |
| Institutional VWAP slicing | “sliced into small slices, 100 or 200 shares, executed over the course of a day” | 大单拆分的切片大小、时间分布、参与率 | Full execution report + market volume profile | future_bucket | 需broker的algo execution detail（如VWAP algo的participation rate、schedule）。 | 仅引用Kenneth Griffin证词，无具体算法参数。 |
| Slippage relative to VWAP | 隐含在执行成本讨论中 | 订单均价与同期市场VWAP的差值 | Execution fill data + market tick data | future_bucket | 计算execution shortfall: (fill_price − VWAP) / VWAP。 | 书中未定义slippage的数学表达式。 |
| Market Impact around VWAP | 隐含在机构执行逻辑中 | 大单执行期间价格偏离VWAP的幅度 | Tick-level price + volume + execution timestamps | future_bucket | 需要市场冲击模型（如Almgren-Chriss或Kissell）的输入数据。 | 书中无市场冲击模型。 |
| Volume distribution around VWAP | 提及heavy volume zones与Volume Profile | 在VWAP附近的价格区间内的成交量分布 | Tick or 1-min data with volume + price bins | needs_extra_data | 可用Volume Profile（fixed range）计算VWAP ± X%区间的成交量占比。 | 书中未将Volume Profile直接用于VWAP附近分布的量化。 |
| Price above/below VWAP | “If the price is above VWAP, buyers are in control” | 价格与VWAP的相对位置（+1 above, −1 below） | 1-min OHLCV + VWAP计算 | proxy_quantizable_now | 可构建简单的position proxy: sign(Close − VWAP)。 | 这是最简单的VWAP量化proxy，但书中将其过度解释为多空主导权。 |
| VWAP deviation classification | “If deviations are moving horizontally → rotation; vertically → trend” | 标准差带斜率或角度（band slope） | 1-min VWAP + upper/lower deviation序列 | shell_only | 需定义“水平”与“垂直”的阈值角度（如slope < 0.01 vs > 0.05），书中未提供。 | 作者用肉眼判断，未给出可量化的角度阈值。 |
| VWAP pullback timing | “wait for the price to move away from VWAP, and when it touches it again, enter” | 价格从VWAP偏离后首次回到VWAP的时间间隔 | 1-min OHLCV + VWAP + 偏离阈值 | shell_only | 需定义“move away”和“touches”的精确条件；作者未给出。 | 属于discretionary pattern recognition，无统计验证。 |
| VWAP reaction strength | 描述价格触碰VWAP后的反弹/下跌 | 触碰VWAP后N根bar的收益率或方向持续性 | 1-min OHLCV + VWAP + 触碰事件检测 | shell_only | 可定义触碰事件并统计后续方向，但成功率未经书中验证。 | 作者声称“often acts as Support”但未给出频率数据。 |
| VWAP confluence with Volume Profile | “when two strategies agree on a level, it becomes a strong level” | Volume Profile POC/VAH/VAL与VWAP的接近程度（distance） | 1-min OHLCV + Volume Profile计算 | shell_only | 可量化两指标的距离，但“strong level”的定义仍主观。 | 书中作为视觉确认使用，无统计框架。 |
| Order Flow Absorption at VWAP | “significant volumes on both Bid and Ask... sellers are absorbing the buying pressure” | 在VWAP价位附近的大单双向成交（bid/ask volume spike） | Tick/footprint data with bid/ask volume per level | future_bucket | 需要逐笔或footprint数据，定义Absorption的volume threshold。 | 书中为视觉描述，无可编程阈值。 |
| Cumulative Delta divergence at VWAP | “price is decreasing while Cumulative Delta is on the rise” | 价格与Cumulative Delta的相关系数或方向差 | Tick data + Cumulative Delta calculation | needs_extra_data | Cumulative Delta = Σ(Ask Volume − Bid Volume)；需tick级方向。 | 可在VWAP附近窗口检测divergence，但书中无窗口定义。 |
| VWAP-based Stop Loss distance | “place your Stop Loss behind a barrier” | 价格到VWAP或deviation的距离作为止损幅度 | 1-min OHLCV + VWAP + deviation | shell_only | 可计算距离，但“behind”的精确位置（几个pip？）未定义。 | 止损距离随时间变化，无固定规则。 |
| ATR-based Take Profit (mentioned alongside VWAP) | “10-20% of the average daily volatility” | ATR(200) × 0.1 ~ 0.2 | Daily OHLCV, ATR(200) | proxy_quantizable_now | 直接可用ATR指标计算，但属于通用风险管理，非VWAP专属。 | 作者将其作为VWAP策略的辅助退出方式。 |

## FORMULAS_AND_ALGOS

### VWAP Formula (derived from text examples)
从书中 Example #1 和 Example #2 可还原出标准 VWAP 公式：

公式：VWAP = Σ(Price_i × Volume_i) / Σ(Volume_i)

其中：
- Price_i = 第 i 笔成交的价格（或某根K线的典型价格）
- Volume_i = 第 i 笔（或第 i 根K线）的成交量
- 求和范围 = 从锚定起点到当前时刻的所有成交

书中明确对比：
- SMA = (P1 + P2) / 2 （不考虑成交量）
- VWAP = (P1×V1 + P2×V2) / (V1+V2) （考虑成交量加权）

### Standard Deviation Bands / VWAP Deviations
**重要：书中未提供标准差带的具体数学公式。**

作者仅描述：
- “VWAP deviations, often referred to as 'bands,' consist of two lines positioned both above and below the VWAP line. These lines move alongside the VWAP and are calculated based on it.”
- 使用“1st deviation”（未提及2nd或3rd deviation）
- 通过deviation的走向（水平/垂直）判断rotation vs trend

**合理的补充说明（非书中内容，仅用于边界标注）：**
若需计算标准差带，典型实现为：
公式：Upper Band = VWAP + k × σ
Lower Band = VWAP − k × σ
其中 σ 可以是：
- 价格围绕VWAP的标准差（是否volume-weighted未明确）
- 或典型价格（Typical Price = (H+L+C)/3）的滚动标准差

由于书中未定义k值、σ的计算方式、滚动窗口长度，**标准差带在本文档中标记为 needs_extra_data / shell_only**。

## NOT_QUANT_YET

1. **Anchored VWAP 的锚定点选择是纯粹主观的**。书中承认不同交易者会选择不同的蜡烛作为锚定点，且缺乏自动化规则（如“swing point”无精确定义）。因此无法生成标准化的可回测序列。

2. **VWAP 作为支撑/阻力缺乏统计验证**。书中反复声称 VWAP “often acts as Support/Resistance”，但从未提供成功率、样本量、置信区间、不同品种/时间周期的差异数据。作者本人也警告“first touch”是最危险的方式。

3. **标准差带的计算公式缺失**。作者仅说 bands are “calculated based on VWAP”，未给出标准差、乘数、滚动窗口等任何参数。无法复现。

4. **Order Flow Confirmation（Absorption、Limit Order、Cumulative Delta divergence）缺乏可编程阈值**。例如“huge order”是多大？“divergence”的判定窗口是多长？书中均为视觉描述。

5. **机构 VWAP 算法执行的内部参数未知**。书中仅引用 Kenneth Griffin 的宏观证词（订单切片为100-200股、执行周期为day/week/month），但未涉及：participation rate、schedule strategy、arrival price benchmark、shortfall calculation 等任何执行算法细节。

6. **Slippage 与市场冲击未量化**。书中提到机构使用 VWAP 以最小化冲击，但未给出冲击成本的度量方式（如IS、MI、IMP等），也未提供任何实证数据。

7. **“VWAP or better”的执行语言未扩展**。虽然引用了机构内部指令格式，但无进一步说明：better 的具体容忍区间是多少？如何与broker的 VWAP algo 接口？如何测量执行质量？

8. **Volume-at-price 分布与 VWAP 的交互未量化**。书中使用 Volume Profile 识别 heavy volume zones，但未将成交量分布与 VWAP 附近的成交量集中度进行任何数值分析（如 VWAP 是否落在高成交量节点内、偏离多少等）。

9. **Confluence（多指标共振）无法量化**。作者将 VWAP、Price Action、Volume Profile 的“视觉对齐”视为强信号，但“对齐”的容忍距离（如多少pip内算confluence？）从未定义。

10. **蜡烛图确认规则不可量化**。例如“wait for one bullish candle to close ABOVE the Support”中的“Support”是VWAP线本身还是某个区域？收盘价需高于多少？未定义。

11. **时间周期偏好在书中不一致**。作者提到 intraday 用 5-min 或 30-min，swing 用 Daily，但未给出选择依据或跨周期一致性检验。

12. **回测框架缺失**。作者建议读者“backtesting your trading strategy”，但全书未提供任何可回测的代码逻辑、参数表、历史数据集或性能指标定义。

## NEXT_ACTION

1. **核对 VWAP 与 AVWAP 的精确数学定义**：从微观结构教材（如 Harris《Trading and Exchanges》、OHara《Market Microstructure Theory》）中提取 intraday VWAP 的标准算法实现（包括 tick-level vs bar-level 的偏差处理）。

2. **补全标准差带的数学公式**：从外部来源（如 CME、Bloomberg、或学术文献）获取 VWAP Standard Deviation Bands 的标准定义（通常基于典型价格围绕 VWAP 的 volume-weighted or unweighted standard deviation），明确乘数（1σ, 2σ, 3σ）与滚动窗口。

3. **建立 Session VWAP 的自动计算管线**：为 Daily/Weekly/Yearly VWAP 构建基于 1-min OHLCV 的批处理计算流程，明确 forex（24h）与 equities（有限交易时段）的 session 边界定义。

4. **验证“VWAP 作为支撑/阻力”的统计假设**：如有需要，使用历史 intraday 数据对“价格回撤至 VWAP 后的方向持续性”进行假设检验，但**不将其作为策略信号**，仅用于验证书中主观断言的可靠性。

5. **收集机构 VWAP 执行算法的公开资料**：从券商 white papers（如 Goldman Sachs、Credit Suisse、ITG 的 VWAP algo 文档）或 regulatory filings 中补全：订单切片逻辑、participation rate 模型、arrival price vs VWAP 的 shortfall 计算。

6. **构建 Execution Quality 基准框架**：将 VWAP 作为 benchmark，设计 execution shortfall 指标：
公式：Shortfall = (Execution VWAP − Market VWAP) / Market VWAP
   用于后续 F1 执行质量评估。

7. **获取 Level 2 / Tick 数据以支持 Order Flow 分析**：验证书中 Order Flow confirmation（Absorption、Limit Order、Cumulative Delta）的识别规则，定义可编程的 volume threshold 与 divergence window。

8. **明确 Volume Profile 与 VWAP 的量化接口**：在后续处理 Volume Profile 资料（如 Forthmann 的 Volume Profile 书籍）时，建立 POC/VAH/VAL 与 VWAP 的数值距离指标，用于量化“confluence”程度。

9. **对比 Trader Dale 的 VWAP 与 academic microstructure VWAP 的差异**：本书为 discretionary trading 视角，而 F2 中 Harris、OHara 等资料为 academic microstructure 视角；需对比两者的 VWAP 定义是否一致（如本书开篇将 VWAP 称为 "Value Weighted" 而非标准 "Volume Weighted"）。

10. **评估 Anchored VWAP 的标准化可能性**：研究 TradingView、NinjaTrader 等平台上 Anchored VWAP 的实现方式，判断是否存在行业通行的锚定规则（如 OHLC/4 vs Close 作为 bar 的 VWAP 输入），以及主观锚定点能否通过结构突破（BOS/CHoCH）或事件检测实现半自动化。

11. **为 F1 执行成本分析预留 VWAP 基准接口**：在后续 F1 模块中，如需评估订单执行质量，应将 VWAP 作为核心 benchmark 之一，并预留与券商 execution report 的对接字段。

12. **标记本书中所有 discretionary 策略为“不可量化”并归档**：将 Strategy #1（Reactions to VWAP）、Strategy #2（Reactions to 1st deviations）、所有 stop-loss/take-profit 的 discretionary 规则统一归入 NOT_QUANT_YET，避免后续误将其作为量化信号源使用。

