## BASIC_INFO
- title: ORDER FLOW Trading Setups
- author: Trader Dale
- material_type: 交易技术教材/教程
- domain_tags: [order flow, trading setups, delta, absorption, liquidity, footprint, volume profile, institutional activity, cumulative delta]
- file_scope: ORDER FLOW Trading Setups (Trader Dale) (Z-Library).pdf
- source_file_size_mb: 18.98
- retain_mode: RETAINED_EXCERPTS
- current_repo_role: SECONDARY_STRUCTURED_NOTE

## MATERIAL_POSITIONING
- what_this_book_is: 一本面向日内交易者的订单流可视化工具使用指南，核心讲解如何通过 Footprint、Delta、Volume Profile 等微观结构元素识别机构活动痕迹，并围绕这些痕迹构建交易决策框架。作者强调订单流数据优于 DOM 的"噪音过滤"价值——只展示实际成交的订单（而非未成交的挂单），且以图形化方式降低读取难度。
- why_in_f2: 本书为 F2 资料库中"订单流交易的具体观察对象与识别技术"模块。它定义了多种可在量化特征工程中被概念化的微观模式：HVN、Volume Cluster、Imbalance、Stacked Imbalance、Unfinished Business、Trades Filter、Cumulative Delta Divergence 等。这些模式虽在书中被包装为交易设置，但其底层定义与识别逻辑可直接映射为订单流特征工程中的候选因子。
- not_a_strategy_book_because: 本书确实包含大量具体交易设置（入场、出场、止损、时间框架选择），但它们的真正价值不在于可直接复制的策略规则，而在于揭示了订单流图表中"哪些微观结构对象需要被观察"。我们保留这些对象的定义与识别机制，而非具体的交易规则。因此本书在 F2 中的角色是概念库与数据源目录，而非可直接部署的量化策略手册。
- relation_to_order_flow_microstructure: 直接对应。书中所有观察对象（Footprint、Bid/Ask 逐笔分布、Delta、HVN、Volume Cluster、Absorption、Limit Order 签名、Imbalance 等）均为订单流微观结构的核心元素。作者反复强调的是"跟随机构"——即通过成交量分布识别大资金的建仓/防御/撤退痕迹。
- data_footprint_required: 严格要求交易所级逐笔数据（tick-by-tick with aggressor flag），或至少带 Bid/Ask 分离的成交数据。作者明确区分 Futures（中心化、可区分 Bid/Ask）与 Forex（去中心化、通常仅 Total Volume）的数据质量差异，并指出 Order Flow 的效力高度依赖于能否区分 Bid 与 Ask 的成交量。DOM 的 Level 2 数据对本书并非必需，但 L1 的 Bid/Ask 分离成交数据是底线。

## CONTENT_STRUCTURE
- 章节1: 订单流基础架构与数据要求（平台选择、Futures vs Forex、数据 feed、CQG）
- 章节2: 市场参与者分类与 Footprint 读取逻辑（Passive vs Active、Bid/Ask 双重视角、Green/Red Cells）
- 章节3: 核心订单流对象定义（HVN、Delta、Cumulative Delta、Volume Clusters、Imbalances、Stacked Imbalances、Unfinished Business、Trades Filter）
- 章节4: 主交易设置（基于 Volume Clusters、Multiple Nodes、Trades Filter、Stacked Imbalances、Unfinished Business 的识别框架）——保留对象定义，剥离具体入场规则
- 章节5: 确认机制（Big Limit Orders、Absorption、Aggressive Orders + Delta、Cumulative Delta Divergence）——保留确认对象的定义与识别逻辑
- 章节6: Volume Profile 与订单流整合（Volume Profile 形状、Volume Accumulation、Trend Setup、Rejection Setup）——保留 Volume Profile 作为订单流宏观背景的角色定义
- 章节7: 交易管理（Take Profit / Stop Loss / Trailing）——保留基于 Volume/Order Flow 对象的逻辑原理，不保留具体规则

## RETAINED_EXCERPTS

- excerpt_id: 1
  source_hint: "Page 20-21, Passive vs Active Market Participants"
  quote: "Passive market participants are traders who enter their trade with a limit (pending) order. They do not chase the market. Active market participants are traders who enter their trades with market orders. If you open a LONG position with a market order, it will appear on the ASK side of the footprint (on the right). If you open a SHORT position with a market order, it will appear on the BID side (on the left)."
  why_kept: 定义了 Footprint 中 Bid/Ask 数字的双重含义——同一数字既可能是被动一方的建仓，也可能是主动一方的建仓。这是理解订单流所有后续模式的基础。
  quant_link: "Bid/Ask volume decomposition is a prerequisite for all footprint-based features."

- excerpt_id: 2
  source_hint: "Page 25, Green/Red Cells"
  quote: "The cell is GREEN if the number on the Ask is larger than the number on the Bid. It is RED when the Bid is larger than the Ask. Usually (not always), the bullish footprints are primarily green and the bearish footprints are primarily red. However, this is not always true, and there is much more to it."
  why_kept: 明确 Green/Red Cell 的机械定义与局限——它是 Ask vs Bid 的体积比较，而非直接等于"买方强/卖方强"，因为每个数字都包含被动和主动两种成分。
  quant_link: "Green/Red ratio can be computed from tick-by-tick data with aggressor flag, but interpretation requires additional microstructure context."

- excerpt_id: 3
  source_hint: "Page 25-26, High Volume Nodes (HVN)"
  quote: "Possibly, the most important place in any footprint is the High Volume Node. It represents the place where the heaviest volumes were traded, a place where the institutions were the most active. It is marked by a black outline. If there are more Heavy Volume Nodes at the same price, in two or more consecutive footprints, then my software will make it in yellow. Price levels like these represent Support/Resistance zones."
  why_kept: HVN 是逐笔级别的成交量密度标记，其"连续性"（多个 footprint 在同一价格出现 HVN）被赋予更高的结构意义（黄色高亮）。这是机构活动痕迹的逐笔级识别单元。
  quant_link: "HVN detection requires per-bar volume-at-price distribution; Multiple HVN requires cross-bar price-level alignment."

- excerpt_id: 4
  source_hint: "Page 26-27, Delta"
  quote: "It is GREEN (positive) when more volume is executed at the Ask. It is RED (negative) when more volume is executed at the Bid. If there is a rotation, then you cannot rely on this as much. The reason is that in a rotation, big institutions usually enter their trades both with market and pending orders. They combine these two types of orders in an effort to mask their true intentions."
  why_kept: Delta 的机械定义（Ask - Bid）与关键局限：在盘整/旋转行情中不可靠，因为机构会混合使用市价单与限价单来隐藏意图。这直接定义了 Delta 的"适用市场状态边界"。
  quant_link: "Delta = AskVol - BidVol per footprint; validity boundary is trending markets, not rotations."

- excerpt_id: 5
  source_hint: "Page 27-28, Price and Delta Divergence"
  quote: "A bullish footprint with a negative Delta tells you this: The price is rising, but Sellers are entering their Shorts and they are stronger than the Buyers. A bearish footprint with a positive Delta tells you this: The price is falling, but Buyers are entering their Longs and they are stronger than the sellers. Both those scenarios represent a warning that a price reversal might happen (price reverses to follow Delta)."
  why_kept: 定义了 Price-Delta Divergence 的微观结构含义——价格方向与主动力量方向背离，被视为潜在反转预警。这是订单流中最经典的反转信号概念之一。
  quant_link: "Price-Delta divergence requires footprint-level Delta series and price direction alignment."

- excerpt_id: 6
  source_hint: "Page 34, Volume Clusters"
  quote: "When there is an area that is way darker than the surrounding areas, it marks a place where the BIG trading institutions and their algorithms were most likely actively trading. Those are critical areas to keep track of as they often represent strong Support and Resistance zones."
  why_kept: Volume Cluster 的定义——基于"颜色深浅"（即成交量密度）的视觉识别，标记机构算法的活跃区域。这是从"逐笔成交密度"到"支撑阻力区域"的概念映射。
  quant_link: "Volume Cluster detection = local volume density anomaly in volume-at-price matrix."

- excerpt_id: 7
  source_hint: "Page 35-36, Imbalances"
  quote: "An Imbalance is when Buyers are way more aggressive than Sellers or when Sellers are more aggressive than Buyers. If Buyers are way more aggressive (Ask is 300% or larger than the Bid), then the number on the Ask is printed in BLUE. If Sellers are more aggressive (Bid is 300% or larger than the Ask), then the number on the Bid is printed in BLUE. Bid x Ask Order Flow is compared diagonally."
  why_kept: 定义了 Imbalance 的精确量化阈值（300%）与比较方式（对角线比较）。这是 Footprint 中识别"主动力量极端失衡"的硬性标准。
  quant_link: "Imbalance threshold = 300% diagonal ratio; requires per-cell Bid/Ask decomposition."

- excerpt_id: 8
  source_hint: "Page 36-37, Stacked Imbalances"
  quote: "Stacked Imbalances are three or more cells with imbalances on top of each other. Stacked Imbalances are a sign that one side of the market (Buyers or Sellers) is dominating and in control. Those Buyers or Sellers are really strong, aggressive, and determined to push the price their way."
  why_kept: Stacked Imbalance 的定义与行为含义——多个连续价格层级的失衡叠加，意味着单边力量的持续主导，被视为强支撑/阻力区域。
  quant_link: "Stacked Imbalance = 3+ consecutive price-level cells each satisfying 300% imbalance threshold; requires full footprint matrix."

- excerpt_id: 9
  source_hint: "Page 37-38, Unfinished Business"
  quote: "Unfinished Business represents a market imperfection. A properly formed high needs to have 0 contracts traded at the Bid, and a properly formed Low needs to have 0 contracts traded on the Ask. When the market turns from a new low or high without this happening, it is called Unfinished Business (or a Failed Auction). It is an imperfection that the market tends to fix. The price has a tendency to revisit such places and 'finish the business.'"
  why_kept: 定义了 Failed Auction / Unfinished Business 的微观结构条件——反转发生时未满足"高点 Bid 为零"或"低点 Ask 为零"的拍卖完美性条件。这是 Market Profile 概念在订单流中的映射。
  quant_link: "Unfinished Business = reversal bar where extreme price tick still has non-zero opposing-side volume; requires per-tick volume data within footprint."

- excerpt_id: 10
  source_hint: "Page 40-41, Trades Filter"
  quote: "This unique feature filters out all the noise from the market and leaves only the biggest trades (trades of the BIG guys we want to track). Institutions prefer to enter their trading positions using Iceberg orders. But when there is not much time, and the institutions need to get into their trade quickly, they don't have the luxury of Iceberg orders and they need to enter their trades using bigger position sizes. Those larger orders are the ones we track with the Trades Filter."
  why_kept: Trades Filter 的本质——识别机构在"时间紧迫"时无法使用 Iceberg 拆分而暴露的大单痕迹。这是从"逐笔成交大小过滤"到"机构紧急活动检测"的概念映射。
  quant_link: "Trades Filter = large-lot threshold filter on individual executed trades; proxy for institutional urgency."

- excerpt_id: 11
  source_hint: "Page 41-42, Cumulative Delta"
  quote: "The Cumulative Delta prints the difference between the Bid and Ask. You can think of it this way: Cumulative Delta identifies the difference between Buyers and Sellers. If there are more aggressive Buyers jumping in, then the Cumulative Delta is rising. If there are more aggressive Sellers than Buyers, then it is falling. It is best to watch the Cumulative Delta around strong Support and Resistance zones."
  why_kept: Cumulative Delta 的累积定义与使用场景——作为日内主动力量净值的累积度量，在关键价格区域观察其方向性变化。
  quant_link: "Cumulative Delta = cumulative sum of (Ask - Bid) per footprint from session start; reset daily."

- excerpt_id: 12
  source_hint: "Page 42, Cumulative Delta Divergence Example"
  quote: "The price is heading downwards, but the Cumulative Delta is going up. This tells me that even though the price is going down, there are Buyers entering Long and the price will most likely reverse and turn upwards. It is best to look for price x Delta divergences around Support and Resistance zones."
  why_kept: 定义了 Price-Cumulative Delta Divergence 的读取逻辑——价格下行但累积主动力量向上，暗示底部反转。强调在支撑/阻力区域使用。
  quant_link: "Cumulative Delta Divergence = price direction vs cumulative delta direction mismatch at S/R zones."

- excerpt_id: 13
  source_hint: "Page 80-81, Big Limit Orders (Confirmation Setup)"
  quote: "Passive traders who wait for the price to come to them use Limit orders. A Limit order is more suitable because they get filled for the price THEY want. The Limit Confirmation Strategy is quite simple. First, you identify a significant S/R zone. Then you wait and look for somebody big to jump in a trade there. To get a Resistance zone confirmed, you need to see a Limit Sell order appear. To get a Support zone confirmed, you need to see a Limit Buy order appear."
  why_kept: Big Limit Orders 确认机制的定义——在关键区域识别"异常大"的被动限价单痕迹。注意：书中对"异常大"的定义是"与近期同 instrument 平均 cell volume 相比显著偏大"，且因 instrument 和 session 而异。
  quant_link: "Big Limit Order detection = outlier volume cell at Bid (Limit Buy) or Ask (Limit Sell) in footprint; requires per-cell volume and instrument/session-specific baseline."

- excerpt_id: 14
  source_hint: "Page 86-87, Absorption (Confirmation Setup)"
  quote: "Sellers are pushing the price downwards using aggressive Market Sell orders. But then strong Buyers appear, and they absorb all the selling pressure—all the selling momentum. They buy everything the Sellers are selling. The price does not drop anymore, and heavy volumes start to appear. Those heavy volumes appear on the BID (aggressive Sellers) and ASK (aggressive Buyers). So, when you see huge volumes traded on the Bid and Ask (both!) around some S/R zone, then it is most likely the Absorption taking place."
  why_kept: Absorption 的定义——双向巨量同时出现，意味着一方完全吸收了另一方的动量。关键特征：Bid 和 Ask 同时出现"异常大"成交量，价格停止移动。这是 Stopping Volume 的订单流等价概念。
  quant_link: "Absorption = simultaneous high volume on both Bid and Ask at same price level with price stall; requires bid/ask volume decomposition."

- excerpt_id: 15
  source_hint: "Page 91-93, Aggressive Orders and Delta (Confirmation Setup)"
  quote: "Aggressive Buyers show on Ask and aggressive Sellers show on Bid. If the price entered a Resistance zone, you want to see aggressive Sell orders (way larger volumes on the Bid than the Ask). If the price reached Support, you want to see aggressive Buy orders (way larger volumes on the Ask as compared to the Bid). If Bid grows bigger than Ask or the other way around, it will also show on the Delta."
  why_kept: Aggressive Orders 确认的定义——在关键区域观察单一方向主动力量的突然放大。Delta 作为快速聚合指标的角色：当主动力量开始介入时，Delta 会相应变色。
  quant_link: "Aggressive Order signature = single-sided volume spike at support/resistance; Delta captures this as footprint-level Ask-Bid differential."

- excerpt_id: 16
  source_hint: "Page 94, Confirmation Combination (Bonus)"
  quote: "The best scenario you can ask for is when there is a combination of two confirmations. The first confirmation you will see is either a Limit order or Absorption. The confirmation that comes after is the Aggressive orders confirmation. This basically means that some large passive market participant was waiting for the S/R to get hit. Then this big guy jumped in, which caused a snowball effect and more people started to join in, this time more aggressively."
  why_kept: 定义了订单流确认信号的序列逻辑——先被动（限价单/吸收），后主动（市价单），形成"雪球效应"。这是订单流中微观结构事件序列的典型案例。
  quant_link: "Sequence pattern: passive absorption signature -> aggressive momentum signature; requires temporal ordering of footprint-level events."

- excerpt_id: 17
  source_hint: "Page 98, Cumulative Delta vs Delta Definition"
  quote: "Delta = Ask – Bid. Simply put, Delta is the difference between Buyers and Sellers in each footprint. Cumulative Delta is a sum of all Deltas since the beginning of the day. For example, if the 1st footprint has Delta = 30, the 2nd footprint has Delta = 100, and the 3rd footprint has Delta = -50, then by the time the 3rd footprint finishes printing, the Cumulative Delta will be +80 (30+100-50)."
  why_kept: 精确数学定义：Delta = Ask - Bid（逐 footprint），Cumulative Delta = sum(Delta) from session start（逐日重置）。
  quant_link: "Delta = Ask - Bid per footprint; Cumulative Delta = cumulative sum from session open; daily reset."

- excerpt_id: 18
  source_hint: "Page 110-111, Trailing with Imbalance"
  quote: "To trail your Long position, you want to see aggressive Buyers. The easiest way is to look for Imbalances. When you are Long, you want to see Buying Imbalances. If the price continues to move rapidly and it creates an Imbalance on the way, then you can trail your position some more. Imbalance = Sign of aggressive Buyers/Sellers."
  why_kept: Imbalance 作为"主动力量持续性"标志的定义——在趋势延续过程中出现 Imbalance，意味着单边主动力量仍在持续介入，可作为动量持续性代理。
  quant_link: "Imbalance as momentum continuation proxy = presence of 300%+ diagonal ratio during directional price movement."

- excerpt_id: 19
  source_hint: "Page 114-115, Stop Loss with Order Flow (Low Volume Area)"
  quote: "Low volume area means placing your SL in a low volume area, which is located behind a heavy volume area. The reason behind this is that heavy volume areas work as zones of Support/Resistance. The price should not go past them. If it does go past a heavy volume area, then it is a sign of strong market momentum and there is no reason for staying in a trade that would go against that momentum."
  why_kept: Low Volume Area 作为动量突破信号的定义——当价格穿越高成交量区域进入低成交量区域，意味着原有支撑/阻力失效，动量足够强大以突破机构密集区。这是 Volume Profile 概念在订单流中的映射。
  quant_link: "Low volume area breakout = price penetrating heavy volume node into low volume zone; requires volume-at-price profile."

- excerpt_id: 20
  source_hint: "Page 122-124, Volume Profile Definition and Role"
  quote: "Volume Profile is a trading indicator that shows Volume at Price. It helps to identify where the big financial institutions put their money and helps to reveal their intentions. Volume Profile shows volume at price. Standard volume indicators only show WHEN there were big volumes traded. This tells you nothing about essential price levels (Support/Resistance zones)."
  why_kept: Volume Profile 的核心定义——Volume at Price 而非 Volume at Time。它揭示了机构在"哪些价格"投入资金的痕迹，这是所有订单流分析的大背景。
  quant_link: "Volume Profile = volume-at-price histogram; requires tick-level or aggregated volume data per price level."

- excerpt_id: 21
  source_hint: "Page 124-128, Volume Profile Shapes"
  quote: "D-Shaped Profile: temporary balance, institutions building positions. P-Shaped Profile: uptrend, aggressive buyers pushing price up, then rotation with heavy volume. b-Shaped Profile: exact opposite of P, downtrend. Thin Profile: strong trend, not much time for building positions, only small Volume Clusters created."
  why_kept: Volume Profile 四种形态的定义与行为含义——D（平衡/建仓）、P（上涨后盘整）、b（下跌后盘整）、Thin（强趋势/小集群）。这些形态为订单流观察提供了宏观市场状态分类。
  quant_link: "Volume Profile shape classification = D/P/b/Thin based on volume-at-price distribution skewness and kurtosis."

- excerpt_id: 22
  source_hint: "Page 128, Why Care about Volumes and Big Institutions"
  quote: "There is a straightforward reason why we need to know what the big financial institutions are doing. The reason is that they dominate, move, and manipulate the markets. It is they who decide where the price will go, not you or I."
  why_kept: 本书的底层世界观——成交量是机构意图的代理，订单流的目的是跟踪这些机构。这定义了所有订单流特征的理论基础：成交量异常 = 机构活动痕迹。
  quant_link: "Institutional activity proxy = volume anomalies at price levels; requires volume-profile baseline per instrument."

- excerpt_id: 23
  source_hint: "Page 130-131, Volume Accumulation Setup Logic"
  quote: "Big trading institutions first need to enter their huge trading positions before manipulating the market into a new trend. They enter their huge positions in a rotation. This is the only place where they can accumulate such large volume without being seen and without their intentions being recognised."
  why_kept: Volume Accumulation 的微观结构逻辑——机构在"盘整/旋转"中建仓，因为趋势中无法隐蔽大额成交。这定义了"高成交量区域在盘整中 = 机构建仓"的核心概念。
  quant_link: "Volume Accumulation = high volume within rotation range; interpreted as institutional position-building before directional move."

- excerpt_id: 24
  source_hint: "Page 131-132, Two Factors Driving Price from S/R"
  quote: "Reason #1: Strong Buyers/Sellers who were accumulating their positions are likely to defend their positions. Reason #2: Nobody wants to risk a fight with strong and aggressive Buyers/Sellers. When Sellers approach the strong rotation where aggressive Buyers accumulated, the Sellers stop and close their positions. When Sellers close their Shorts, they buy, which helps drive the price upwards."
  why_kept: 定义了高成交量区域作为支撑/阻力生效的"双因素机制"——(1) 原有持仓方的防御性买入/卖出；(2) 反向交易方的撤退性平仓。这两个因素在订单流中体现为同一方向的主动力量叠加。
  quant_link: "Dual-factor S/R mechanism = defending orders + counterparty closing orders; both manifest as same-direction aggressive volume."

- excerpt_id: 25
  source_hint: "Page 136-137, Trend Setup Logic"
  quote: "There is not much time for accumulating big trading positions when there is a trend. Sometimes, the trend movement halts for a bit and some new and relatively big volumes get accumulated. Those volumes show as a little 'bump' on the otherwise thin Volume Profile. Those 'bumps' are called Volume Clusters."
  why_kept: Volume Cluster in Trend 的定义——强趋势中短暂停顿形成的小成交量凸起，被视为机构在趋势中"边走边建"的痕迹。这区分了"盘整中的大量积累"与"趋势中的小量集群"两种场景。
  quant_link: "Volume Cluster in trend = local volume bump within thin volume profile; distinct from accumulation in rotation."

- excerpt_id: 26
  source_hint: "Page 140-141, Rejection Setup Logic"
  quote: "When there is a strong price reversal, we get the information that one side of the market became very aggressive and strongly rejected some price level. When this happens, I am interested in how the volumes were distributed within the rejection. The place with the heaviest volumes marks the place where the counterparty was the most aggressive—the place where the biggest fight was."
  why_kept: Rejection 的订单流含义——强烈反转区域中的成交量最重处 = 双方最激烈博弈的价格。这是"反转区域成交量分布"作为阻力/支撑强度度量的概念。
  quant_link: "Rejection volume distribution = volume-at-price within reversal bar/cluster; heaviest volume level = most aggressive counterparty engagement."

- excerpt_id: 27
  source_hint: "Page 111-112, Trailing Warning Signals"
  quote: "It is best to stop trailing your position when you see a warning signal that says the market momentum may have changed. Those signals are: Limit orders, Absorption, Aggressive orders going against you, or a divergence between Price and Delta. This is especially true if you see any of them appear around a strong level of Support/Resistance or in a heavy volume zone."
  why_kept: 定义了订单流中"动量反转警告"的四类微观结构信号——Limit Orders、Absorption、Aggressive Orders（反向）、Price-Delta Divergence。这些信号在关键区域出现时被视为动量可能终止的标记。
  quant_link: "Momentum reversal warnings = limit order signature + absorption + aggressive reverse orders + price-delta divergence; all require footprint-level bid/ask decomposition."

- excerpt_id: 28
  source_hint: "Page 16-17, Futures vs Forex Data Quality"
  quote: "Futures: Is centralized, which means that everybody sees the same price and volumes. Most importantly, Futures allow us to see how much volume was traded on the Bid as well as the Ask. Forex: Is decentralized, which means that only people who use the same data feed provider see the same price and volumes. The main disadvantage is that Forex providers are unable to distinguish Bid and Ask (or if they do, they do it very badly). So, the best you can get is Total volume."
  why_kept: 数据质量边界定义——订单流的核心效力依赖于 Bid/Ask 分离的成交量数据；Forex 的"Total Volume"只能支持部分功能（Volume Cluster、HVN），无法支持 Delta、Imbalance、Cumulative Delta 等核心特征。
  quant_link: "Data quality boundary: Bid/Ask split = required for Delta/Imbalance/Cumulative Delta; Total Volume = sufficient only for volume cluster and HVN."

- excerpt_id: 29
  source_hint: "Page 33-34, Volume Clusters Visual Definition"
  quote: "When there is an area that is way darker than the surrounding areas, it marks a place where the BIG trading institutions and their algorithms were most likely actively trading. Those darker and lighter shades are also used on the Bid x Ask visualization. The heavier the volumes the darker the color."
  why_kept: Volume Cluster 的可视化定义——通过"颜色深浅"在 footprint 中标记成交量密度。这是从原始成交数据到人类可读视觉信号的转换机制，其底层为 volume-at-price 的密度计算。
  quant_link: "Volume Cluster visualization = heatmap of volume-at-price within footprint; darker = higher volume density."

- excerpt_id: 30
  source_hint: "Page 156, Glossary - Iceberg Order"
  quote: "When a big trading institution enters a position, they sometimes don't enter it all at once with one order. Instead, their algorithms split the order into many small orders. For example, instead of entering 10 contracts, they enter 1+1+1… They do this super quick."
  why_kept: Iceberg Order 的定义——机构拆分大单以隐藏真实意图。书中指出 Trades Filter 无法捕获 Iceberg（因为拆分后每单都小于阈值），只能捕获"来不及拆分"的大单。这定义了 Trades Filter 的探测边界。
  quant_link: "Iceberg Order = algorithmic order splitting into small sequential trades; Trades Filter detects only un-split large orders."

- excerpt_id: 31
  source_hint: "Page 156-157, Glossary - Imbalance Diagonal Comparison"
  quote: "Imbalance: If Ask is 300% or more than Bid, then it is a Buying Imbalance. If Bid is 300% or more than Ask, then it is a Selling Imbalance. Note that Bid and Ask are compared diagonally from left to right!"
  why_kept: 再次确认 Imbalance 的精确计算方式——对角线比较（左上到右下），300% 阈值。这是 footprint 矩阵中失衡计算的核心几何规则。
  quant_link: "Diagonal comparison = upper-left Bid vs lower-right Ask cell pair; 300% ratio threshold."

- excerpt_id: 32
  source_hint: "Page 10-11, Why Order Flow vs DOM"
  quote: "DOM was just full of noise and too hard to read. I knew there was a lot of useful info there, but I needed something to help me read that crazy matrix. The big advantage of using the Order Flow is that it prints orders that matter—orders that actually got filled. Order Flow also prints those orders in a way that is much easier to read as well as backtest."
  why_kept: Order Flow 相对于 DOM 的优势定义——过滤未成交挂单噪音，只显示实际成交；图形化降低读取难度；可回测（因为基于成交历史而非瞬时的挂单快照）。
  quant_link: "Order Flow advantage over DOM = executed orders only, not pending; historically backtestable because based on trade tape, not L2 snapshot."

- excerpt_id: 33
  source_hint: "Page 23, Bigger Perspective on Bid/Ask Coloring"
  quote: "When volumes appear on BID, they can be both aggressive Sellers or passive Buyers. And when volumes appear on the ASK, they can be both aggressive Buyers or passive Sellers! If somebody tells you that 'green' means Buyers and 'red' means Sellers, they are telling you a half-truth."
  why_kept: 对 Green/Red 颜色解读的彻底否定——颜色只是 Ask vs Bid 的体积比，不代表"买方/卖方"。这是订单流分析中最根本的误读陷阱。
  quant_link: "Color interpretation trap: Green = Ask > Bid, not 'Buyers'; Red = Bid > Ask, not 'Sellers'. Each cell contains both active and passive participants."

- excerpt_id: 34
  source_hint: "Page 40, Trades Filter Threshold Calibration"
  quote: "You can set the Filter anyway you like. I personally prefer to set it in a way that only the most significant trading orders show. This means that on EUR Futures I have the Trades Filter set to 25. This means it only shows executed trades that were 25+ contracts. A rule of thumb here is to set it to a number that gives you around 5–10 trading signals per day."
  why_kept: Trades Filter 的阈值校准逻辑——按 instrument、session、信号频率来设定。书中给出 EUR Futures 的参考值（25 lots）和 ES 的参考值（300+），强调阈值不是通用的，而是需要 per-instrument calibration。
  quant_link: "Trades Filter threshold = instrument-specific, session-specific; target ~5-10 signals per day; ES ~300, 6E ~25."

- excerpt_id: 35
  source_hint: "Page 71-72, Unfinished Business as Magnet"
  quote: "The main thing to remember about Unfinished Business is that it works like a magnet. The price is drawn towards it, and if it comes close, it is likely to move through it. If you are in a profitable trade and the price is moving towards Unfinished Business, you might remain in your position a little bit longer until the price tests the Unfinished Business."
  why_kept: Unfinished Business 的"磁力"隐喻定义——市场不完美性具有价格回拉的倾向。这定义了 Failed Auction 作为"价格吸引子"的概念角色。
  quant_link: "Unfinished Business magnet effect = failed auction price level attracting future price revisit; behavioral mechanism = market imperfection correction."

- excerpt_id: 36
  source_hint: "Page 87, Absorption Volume Definition"
  quote: "An 'unusually large' or 'huge' volume would be volume way above this average. It is also hard to provide an exact definition of the term 'unusually large volumes' as they are different for every trading instrument and trading session. A simple technique you can use is to look at recent Order Flow footprints and determine an average cell volume."
  why_kept: Absorption 中"异常大成交量"的定义方式——相对于近期同 instrument、同 session 的"平均 cell volume"的异常值。这强调了所有成交量"异常"的基准都是相对的、instrument-dependent 的。
  quant_link: "Absorption volume baseline = rolling average of per-cell volume per instrument per session; outlier = way above average."

- excerpt_id: 37
  source_hint: "Page 25, Footprint Definition"
  quote: "The Order Flow does not show standard candles, but it shows FOOTPRINTS. A footprint shows not only Open, High, Low, Close as standard candles do, but it also shows orders that got traded within that candle. Orders are placed on Bid or on Ask."
  why_kept: Footprint 的基础定义——在标准 OHLC 之上增加了逐笔级别的 Bid/Ask 成交分布。这是订单流可视化的原子单元。
  quant_link: "Footprint = OHLC + per-price-level Bid/Ask volume decomposition within bar."

- excerpt_id: 38
  source_hint: "Page 70, Unfinished Business Formal Condition"
  quote: "A properly formed high needs to have 0 contracts traded at the Bid, and a properly formed Low needs to have 0 contracts traded on the Ask. When the market turns from a new low or high without this happening (Bid AND Ask are both more than 0), it is called an Unfinished Business (or a Failed Auction)."
  why_kept: 再次确认 Unfinished Business 的精确条件：反转时极端价格点上的对侧成交量非零。即：高点反转时，高点价格仍有 Bid 成交；低点反转时，低点价格仍有 Ask 成交。
  quant_link: "Failed Auction condition: high reversal with Bid>0 at high tick, or low reversal with Ask>0 at low tick."

- excerpt_id: 39
  source_hint: "Page 26, Delta Reliability in Rotations"
  quote: "In a rotation, big institutions usually enter their trades both with market and pending orders. They combine these two types of orders in an effort to mask their true intentions."
  why_kept: 机构在旋转/盘整中混合使用市价单和限价单以隐藏意图——这是 Delta 在旋转市中不可靠的根本原因，也是所有订单流指标都需要"市场状态上下文"的典型例证。
  quant_link: "Delta reliability boundary: invalid in rotations because institutions mix market and limit orders to mask intent."

- excerpt_id: 40
  source_hint: "Page 45-46, Volume Cluster Logic (Two Factors)"
  quote: "Two factors drove the price upwards from the Volume Cluster: #1 factor: Buyers defending their Long Position; #2 factor: Sellers quitting or closing out their Short Position. We can't really tell which of these factors played a bigger role (because both Buyers and Sellers used Buy Market Orders—the same orders)."
  why_kept: 再次确认 Volume Cluster 反弹的双因素机制——防御性买入与空头回补的叠加。关键洞察：订单流无法区分这两种力量（因为它们都使用 Buy Market Orders），只能观测到"向上的主动力量总量"。
  quant_link: "Volume Cluster reaction = sum of defending longs + short covering; both appear as Buy Market Orders, indistinguishable in footprint."

## CORE_CONCEPTS

- concept_name: Footprint (Bid x Ask Cell)
  definition_from_text: "A box that represents a standard price 'candle' with the Bid and Ask values displayed. It shows not only Open, High, Low, Close, but also orders that got traded within that candle, placed on Bid or on Ask."
  behavioral_mechanism: "将单根 K 线内的逐笔成交按价格层级分解为 Bid（左）和 Ask（右）两个维度，每个价格层级显示在该层级成交的合约数量。通过颜色深浅（Volume Clusters）或颜色编码（Green/Red）提供成交量密度的视觉提示。"
  data_objects_involved: "per-bar volume-at-price matrix with Bid/Ask split; diagonal cell pairs for imbalance comparison"
  quant_boundary: "最小数据单元是单根 K 线内的逐笔成交分布；需要 Bid/Ask 分离的成交数据。对于仅提供 Total Volume 的市场（如 Forex），Footprint 退化为只有总成交量的 heatmap，无法计算 Delta 和 Imbalance。"

- concept_name: High Volume Node (HVN)
  definition_from_text: "A black outline in every footprint pointing to the price where the heaviest volumes got traded (within that footprint). It represents the place where the institutions were the most active."
  behavioral_mechanism: "在每根 footprint 内识别成交量最大的价格层级。如果连续两根或多根 footprint 的 HVN 出现在同一价格，则升级为黄色高亮的 Multiple Node，被视为更强的支撑/阻力区域。"
  data_objects_involved: "per-footprint volume-at-price distribution; maximum volume price level per bar; cross-bar price-level alignment"
  quant_boundary: "HVN 需要 per-bar 的 volume-at-price 数据。Multiple HVN 需要跨 bar 的价格层级比对，对价格粒度敏感（相同 price level 的定义取决于 instrument 的 tick size）。"

- concept_name: Delta (Per Footprint)
  definition_from_text: "Delta = Ask – Bid. It is GREEN (positive) when more volume is executed at the Ask. It is RED (negative) when more volume is executed at the Bid. It shows whether there were stronger Buyers or Sellers in that footprint."
  behavioral_mechanism: "计算单根 footprint 内主动买方（Ask 成交）与主动卖方（Bid 成交）的净差值。正值表示主动买方占优，负值表示主动卖方占优。在趋势市中通常与价格方向一致；在旋转市中因机构混合订单类型而可靠性下降。"
  data_objects_involved: "per-footprint Ask volume, Bid volume; Delta = Ask - Bid"
  quant_boundary: "需要逐笔级别的 Bid/Ask 分离数据。无法从 OHLCV 或 Total Volume 推断。在旋转/盘整市中的可靠性显著低于趋势市。"

- concept_name: Cumulative Delta
  definition_from_text: "Cumulative Delta is a sum of all Deltas since the beginning of the day. Its calculation starts every day anew. For example, if the 1st footprint has Delta = 30, the 2nd = 100, and the 3rd = -50, then the Cumulative Delta by the 3rd footprint is +80."
  behavioral_mechanism: "将日内所有 footprint 的 Delta 累加，形成一条日内主动力量净值的累积曲线。用于观察日内主动买方或卖方的总体优势。Price-Cumulative Delta Divergence 被视为价格与主动力量方向背离的潜在反转信号。"
  data_objects_involved: "session-level cumulative sum of per-footprint Delta; reset at session open"
  quant_boundary: "需要连续的 footprint-level Delta 序列。对 session 起始时间的定义敏感（不同交易所/ instrument 的开盘时间不同）。日内累加意味着它对隔夜跳空敏感。"

- concept_name: Order Flow Imbalance (Diagonal)
  definition_from_text: "An Imbalance is when Buyers are way more aggressive than Sellers or vice versa. If Ask is 300% or more than Bid (diagonal comparison), it is a Buying Imbalance (blue). If Bid is 300% or more than Ask, it is a Selling Imbalance (blue)."
  behavioral_mechanism: "在 footprint 矩阵中，将相邻层级的 Bid 与 Ask 进行对角线比较（左上 Bid 对右下 Ask）。当一侧成交量达到另一侧的 300% 或以上时，标记为失衡。这表示在该价格区间，一方主动力量极端占优。"
  data_objects_involved: "per-cell Bid and Ask volumes; diagonal cell pairs; ratio calculation with 300% threshold"
  quant_boundary: "需要完整的 footprint 矩阵（每根 bar 内的每个价格层级都有 Bid/Ask 分解）。对角线比较的几何规则需要精确定义（相邻 cell pair 的对应关系）。阈值（300%）为作者默认值，理论上可调整，但其物理含义是"极端失衡"的代理。"

- concept_name: Stacked Imbalance
  definition_from_text: "Stacked Imbalances are three or more cells with imbalances on top of each other. They represent strong Support/Resistance zones. It is a sign that one side of the market is dominating and in control."
  behavioral_mechanism: "当连续三个或更多价格层级都出现同一方向的 Imbalance 时，形成 Stacked Imbalance。这意味着从低到高（或高到低）的连续价格区间都遭受同一方向的极端主动力量，被视为强趋势中的机构持续介入痕迹。"
  data_objects_involved: "consecutive price-level cells each satisfying 300% imbalance; minimum 3 cells stacked; direction consistency"
  quant_boundary: "需要完整的 footprint 矩阵和精确的 price level 序列。对 instrument 的 tick size 和 footprint 的 bar size 敏感——更大的 bar 或更小的 tick size 更容易产生 Stacked Imbalance。"

- concept_name: Volume Cluster
  definition_from_text: "An area in a chart where heavy volumes were traded. Often appears in a trend or in a Rejection. When there is an area that is way darker than the surrounding areas, it marks a place where the BIG trading institutions and their algorithms were most likely actively trading."
  behavioral_mechanism: "通过 footprint 内颜色深浅（或 Volume Profile 中的厚度）识别成交量密度异常高的区域。被视为机构建仓或激烈博弈的痕迹。后续价格回到 Volume Cluster 时，可能触发防御性反应（原有持仓方防守 + 反向交易方撤退）。"
  data_objects_involved: "volume-at-price density; visual heatmap or histogram; local maxima in volume distribution"
  quant_boundary: "Volume Cluster 可以从 Total Volume 数据中识别（不需要 Bid/Ask 分离）。但其在 Order Flow 中的行为解释（防守/撤退机制）需要 Bid/Ask 数据来确认。对 instrument 和 session 的平均成交量基准敏感。"

- concept_name: Unfinished Business (Failed Auction)
  definition_from_text: "A market imperfection. When the market went one way then turned the other way without having the high/low formed properly. A properly formed high needs to have 0 contracts traded at the Bid, and a properly formed Low needs to have 0 contracts traded on the Ask."
  behavioral_mechanism: "拍卖理论在订单流中的映射：完美的顶部需要最高价格处没有 Bid 成交（即没有主动卖方在顶部卖出），完美的底部需要最低价格处没有 Ask 成交（即没有主动买方在底部买入）。当反转发生时这些条件未满足，意味着市场'不完美'，未来有回拉修正的倾向。"
  data_objects_involved: "extreme tick volume within footprint; high tick Bid volume, low tick Ask volume; reversal detection"
  quant_boundary: "需要 footprint 内最高/最低价格层级的 Bid/Ask 分解数据。'0 contracts' 是理论定义，实际实现中可能需要一个 epsilon 阈值（因为真正的零成交极少）。"

- concept_name: Trades Filter (Big Orders / Iceberg Proxy)
  definition_from_text: "A feature that filters out all the noise and leaves only the biggest trades. It shows executed trades that were X+ contracts with ONE order. Institutions prefer Iceberg orders, but when there is not much time, they enter with bigger position sizes. Those larger orders are the ones we track."
  behavioral_mechanism: "通过设定单笔成交合约数阈值，过滤掉小单噪音，只显示大单成交。书中承认这无法捕获 Iceberg（因为拆分后每单都小于阈值），只能捕获机构在紧急情况下无法拆分的大单。"
  data_objects_involved: "individual trade size (lot/contracts); threshold filter; per-instrument calibration"
  quant_boundary: "需要逐笔成交的 exact trade size 数据。阈值需要 per-instrument、per-session 校准（书中给出 6E ~25 lots, ES ~300 lots 作为参考）。无法检测 Iceberg 的累积效应。"

- concept_name: Absorption (Stopping Volume)
  definition_from_text: "Sellers are pushing the price downwards with aggressive Market Sell orders. But then strong Buyers appear, and they absorb all the selling pressure. They buy everything the Sellers are selling. The price does not drop anymore, and heavy volumes appear on both BID and ASK."
  behavioral_mechanism: "当双向同时出现极端成交量而价格停止移动时，意味着一方的动量被另一方完全吸收。这是趋势暂停/反转的微观结构信号。关键特征是 Bid 和 Ask 同时出现'异常大'成交量，且价格停滞。"
  data_objects_involved: "simultaneous high volume on Bid and Ask at same price level; price stall / narrow range; bid/ask volume decomposition"
  quant_boundary: "需要 Bid/Ask 分离数据和价格停滞检测。'异常大'的基准是相对于近期同 instrument 的平均 cell volume。吸收可能发生在单一 footprint 内，也可能跨多个 footprint。"

- concept_name: Big Limit Orders (Passive Signature)
  definition_from_text: "Passive traders who wait for the price to come to them use Limit orders. A Limit order is more suitable because they get filled for the price THEY want. To get a Resistance zone confirmed, you need to see a Limit Sell order appear. To get a Support zone confirmed, you need to see a Limit Buy order appear."
  behavioral_mechanism: "在关键支撑/阻力区域，识别 footprint 中异常大的被动限价单成交痕迹。注意：在 footprint 中，Limit Buy 出现在 Bid 侧，Limit Sell 出现在 Ask 侧——这与市价单的位置相同。因此'Big Limit Order'的识别依赖于成交量异常而非订单类型直接识别。"
  data_objects_involved: "outlier volume cell at Bid (interpreted as Limit Buy) or Ask (interpreted as Limit Sell) around S/R zone; instrument/session-specific baseline"
  quant_boundary: "Order Flow 数据无法直接区分 Limit Order 和 Market Order 的成交。Big Limit Order 的识别是基于'在关键区域出现极端成交量'的推断，而非直接观测。需要与其他确认信号（如后续价格反应）结合。"

- concept_name: Aggressive Orders (Market Order Signature)
  definition_from_text: "Aggressive Buyers show on Ask and aggressive Sellers show on Bid. If the price entered a Resistance zone and you see big volumes starting to appear on Bid, then it is confirmation that aggressive Sellers are jumping in."
  behavioral_mechanism: "在关键区域识别单一方向主动力量的突然放大。与 Absorption 不同，Aggressive Orders 是单向的（只在 Bid 或只在 Ask 出现极端成交量），且通常伴随着价格沿该方向移动。"
  data_objects_involved: "single-sided volume spike at S/R zone; footprint-level Delta confirmation; bid/ask decomposition"
  quant_boundary: "需要 Bid/Ask 分离数据。'Big' 的定义是相对于近期同 instrument 的平均 cell volume。单向极端成交量可能同时包含主动力量和部分被动力量，无法 100% 区分。"

- concept_name: Price-Delta Divergence
  definition_from_text: "A bullish footprint with a negative Delta tells you: The price is rising, but Sellers are entering their Shorts and they are stronger than the Buyers. A bearish footprint with a positive Delta tells you: The price is falling, but Buyers are entering their Longs and they are stronger than the sellers."
  behavioral_mechanism: "价格方向与 footprint 级别的主动力量净方向相反。被视为潜在反转信号，因为价格可能'追随'主动力量方向而修正。在趋势市中尤为显著，因为趋势市中 Delta 通常与价格方向一致。"
  data_objects_involved: "price direction per footprint; per-footprint Delta sign; cross-footprint divergence detection"
  quant_boundary: "需要 footprint-level Delta 数据和价格方向。在旋转市中 Delta 本身可靠性低，因此 Price-Delta Divergence 在旋转市中的意义也相应降低。"

- concept_name: Volume Profile (Volume at Price)
  definition_from_text: "Volume Profile is a trading indicator that shows Volume at Price. It helps to identify where the big financial institutions put their money and helps to reveal their intentions. Standard volume indicators only show WHEN there were big volumes traded."
  behavioral_mechanism: "将一段时间内的成交量按价格分布绘制为水平直方图。厚重区域表示机构在该价格区间有大量交易活动，被视为支撑/阻力区域。与 Order Flow 的微观视角形成互补——Volume Profile 提供宏观背景，Order Flow 提供微观确认。"
  data_objects_involved: "volume-at-price histogram over a lookback period; local maxima (HVN) and minima (LVN); profile shapes (D, P, b, Thin)"
  quant_boundary: "Volume Profile 可以从 tick 数据或聚合数据构建。对 lookback period 的选择敏感（书中推荐 intraday 30-minute 或 1-hour）。Profile 形状的分类需要统计方法（偏度、峰度）。"

- concept_name: Iceberg Orders
  definition_from_text: "When a big trading institution enters a position, they sometimes don't enter it all at once with one order. Instead, their algorithms split the order into many small orders. For example, instead of entering 10 contracts, they enter 1+1+1… They do this super quick."
  behavioral_mechanism: "机构通过算法将大单拆分为多个小单，以隐藏真实交易量。订单流中无法直接观测 Iceberg 的拆分逻辑，只能通过 Trades Filter 的'漏网之鱼'（即来不及拆分的大单）或 Volume Cluster 的累积成交量来间接推断。"
  data_objects_involved: "sequence of small trades in rapid succession; volume accumulation patterns; trades filter threshold misses"
  quant_boundary: "Iceberg 的拆分逻辑是机构内部算法，不体现在公开数据中。Trades Filter 只能检测未拆分的大单。Volume Cluster 可以检测累积效果，但无法区分是 Iceberg 还是多个独立小单。"

- concept_name: Liquidity Sweeps / Liquidity Grabs (Implied in Unfinished Business & Stop Runs)
  definition_from_text: "书中未使用 'Liquidity Sweeps' 或 'Liquidity Grabs' 的精确术语，但 Unfinished Business 的机制与之高度相关：当价格形成极端后快速反转，且极端点的对侧成交量非零，意味着价格'扫过'了该区域的流动性但未完全耗尽，未来需要回归测试。"
  behavioral_mechanism: "价格快速穿越某区域后反转，留下未完成的拍卖过程。这隐含了流动性被部分'扫取'但未完全清除，导致未来价格被吸引回该区域。Stop Runs 在书中表现为'价格快速突破关键区域后反转'的订单流模式。"
  data_objects_involved: "rapid price excursion to extreme; reversal with non-zero opposing volume at extreme; Unfinished Business detection"
  quant_boundary: "需要极端价格点的 Bid/Ask 分解和快速反转检测。'Sweep' 的持续时间定义（几根 footprint）对识别敏感。"

- concept_name: Bid/Ask Pressure (DOM Pressure Proxy)
  definition_from_text: "书中避免使用 DOM 的'挂单'概念，强调 Order Flow 只看'已成交'订单。但 Bid/Ask Pressure 通过 Delta、Imbalance、Stacked Imbalance 和 Aggressive Orders 等元素被间接定义——即主动力量在 Bid 或 Ask 侧的累积压力。"
  behavioral_mechanism: "通过 footprint 级别的 Delta 方向、Imbalance 方向、Stacked Imbalance 的连续性和 Aggressive Orders 的单边放大来综合判断当前主动力量在哪一侧施压。"
  data_objects_involved: "Delta sign and magnitude; imbalance direction; stacked imbalance direction; aggressive order side"
  quant_boundary: "DOM Pressure 传统上需要 L2 挂单数据；本书中的 Bid/Ask Pressure 完全基于成交数据（L1 with aggressor flag），是 DOM Pressure 的成交侧代理。"

- concept_name: Exhaustion / Trapped Traders (Implied)
  definition_from_text: "书中未直接使用 'Exhaustion' 或 'Trapped Traders' 术语，但 Price-Delta Divergence 和 Absorption 的机制隐含了这一概念：当价格继续向某一方向移动但主动力量已转向（Divergence），或当极端成交量出现但价格停滞（Absorption），意味着最后一波推动者可能已耗尽，反向交易者可能被套。"
  behavioral_mechanism: "Price-Delta Divergence 显示'价格继续但力量已尽'；Absorption 显示'力量被完全吸收'。两者都是动量耗尽和潜在反向交易者被套的微观结构信号。"
  data_objects_involved: "price-delta divergence; absorption signature; volume climax at extreme price levels"
  quant_boundary: "Exhaustion 的识别是推断性的，需要多个订单流元素的组合（Divergence + Absorption + Volume Cluster），而非单一指标。"

- concept_name: Breakout / False Breakout (Order Flow Angle)
  definition_from_text: "书中未直接使用 'Breakout' 或 'False Breakout' 术语，但 Unfinished Business 和 Low Volume Area Stop Loss 机制隐含了订单流对突破的解读：当价格突破高成交量区域进入低成交量区域，意味着突破有效（动量足够）；反之，若价格'突破'高成交量区域但 Bid/Ask 数据显示机构在反向积极介入，则可能是假突破。"
  behavioral_mechanism: "订单流中的突破有效性取决于突破过程中主动力量的方向一致性。Volume Profile 中的 Thin Profile（强趋势）对应持续突破；Unfinished Business 对应'未完成的突破'可能回归。"
  data_objects_involved: "volume profile shape; penetration through HVN into LVN; bid/ask direction during breakout; unfinished business at breakout extreme"
  quant_boundary: "需要 Volume Profile 的 HVN/LVN 边界和突破过程中的 Bid/Ask 分解数据。突破时间框架（几根 footprint）的定义敏感。"

- concept_name: Institutional Activity Signatures
  definition_from_text: "书中反复强调的核心主题是'跟踪机构'。具体的机构活动签名包括：Volume Cluster（机构算法活跃区）、Multiple HVN（机构持续在同一价格交易）、Trades Filter 大单（机构紧急大单）、Stacked Imbalance（机构持续单向施压）、Volume Accumulation（机构在旋转中建仓）。"
  behavioral_mechanism: "机构活动通过成交量异常在订单流中留下痕迹。这些痕迹的共同特征是：成交量密度远高于周围区域、同一价格跨时间重复出现、单向主动力量持续主导、大单紧急暴露。"
  data_objects_involved: "volume density outliers; cross-time price-level alignment; directional imbalance persistence; large trade size outliers"
  quant_boundary: "所有机构活动签名都是'代理'（proxy）而非直接观测。机构可能使用 Iceberg 拆分、多个账户、算法伪装等手段隐藏真实意图。订单流只能检测'无法完全隐藏'的成交量痕迹。"

- concept_name: Volume Climax / Volume Spike (Heatmap Visual)
  definition_from_text: "书中使用'dark grey areas'和'heavier volumes'来描述 Volume Clusters。当某区域颜色远深于周围，即标记为 Volume Cluster。Trades Filter 中红色/绿色高亮的大单也被视为极端成交量事件。"
  behavioral_mechanism: "通过视觉深浅（heatmap）或阈值过滤识别成交量密度异常。Volume Climax 在订单流中表现为 footprint 内某一价格层级的成交量显著高于该 bar 内其他层级，或显著高于近期同 instrument 的平均 cell volume。"
  data_objects_involved: "per-cell volume; heatmap color intensity; statistical outlier detection against rolling baseline"
  quant_boundary: "Volume Climax 可以从 Total Volume 数据中识别，但其行为解释（机构活动 vs 噪音）需要 Bid/Ask 数据来增强。对 instrument 的成交量基准和 session 时间敏感。"

- concept_name: Reversal Patterns in Order Flow
  definition_from_text: "书中定义了多种订单流反转信号：Price-Delta Divergence（价格与主动力量背离）、Cumulative Delta Divergence（价格与累积主动力量背离）、Absorption（双向巨量吸收）、Aggressive Orders at S/R（关键区域反向主动力量介入）、Unfinished Business（市场不完美吸引回归）。"
  behavioral_mechanism: "订单流中的反转不是单一信号，而是多个微观结构元素的组合：主动力量方向与价格方向背离、动量被完全吸收、机构在关键区域反向介入、拍卖过程未完美完成。这些信号在支撑/阻力区域出现时被视为更高可信度的反转预警。"
  data_objects_involved: "delta divergence; cumulative delta divergence; absorption signature; aggressive order at S/R; unfinished business at extreme"
  quant_boundary: "所有反转信号都是概率性的，书中明确警告'不存在魔法'。反转信号需要与宏观结构（Volume Profile、关键价格区域）结合使用，而非孤立使用。"

## QUANTIZATION_TABLE

| concept | raw_rule_from_text | observable_proxy | data_needed | quant_status | implementation_hint | notes |
|---|---|---|---|---|---|---|
| Delta (per footprint) | Delta = Ask - Bid per bar; positive = more Ask, negative = more Bid | AskVol - BidVol per aggregation bar | tick-by-tick with aggressor flag (or exchange-level L1 with Bid/Ask split) | needs_extra_data | Compute per-bar Ask-Bid differential; requires precise aggressor side assignment per trade | 旋转市中可靠性低；机构混合订单类型会掩盖意图 |
| Cumulative Delta | Sum of all Deltas since session start; reset daily | Cumulative sum of per-bar Delta | tick-by-tick with aggressor flag; session start time definition | needs_extra_data | Daily-reset cumulative sum; watch for divergence vs price at S/R zones | 对 session 开盘时间敏感；隔夜跳空需特殊处理 |
| Price-Delta Divergence | Bullish bar with negative Delta, or bearish bar with positive Delta | Sign(bar_return) != Sign(Delta) | tick-by-tick with aggressor flag; per-bar Delta series | needs_extra_data | Compare price direction and Delta sign per footprint; more significant at S/R | 旋转市中意义降低；需结合 S/R 上下文 |
| Order Flow Imbalance | Ask >= 300% of Bid (diagonal) = Buying Imbalance; Bid >= 300% of Ask = Selling Imbalance | Per-cell diagonal ratio >= 3.0 | footprint chart with per-bar bid/ask delta matrix | needs_extra_data | Diagonal comparison: cell[i].Bid vs cell[i+1].Ask (or reverse); requires full footprint matrix | 阈值 300% 为作者默认值；cell 定义依赖 tick size 和 bar size |
| Stacked Imbalance | 3+ consecutive cells with imbalance in same direction | 3+ consecutive price levels each satisfying imbalance threshold | footprint chart with per-bar bid/ask delta matrix | needs_extra_data | Detect consecutive price-level imbalances; direction must be consistent | 对 bar size 和 tick size 敏感；更大 bar 或更小 tick 更容易触发 |
| Volume Cluster | Area way darker than surrounding = heavy volume; institutional activity | Local maxima in volume-at-price distribution | volume-at-price (can be Total Volume) | proxy_quantizable_now | Heatmap or histogram of volume-at-price; detect local density outliers | 可以从 Total Volume 构建；但行为解释需要 Bid/Ask 增强 |
| High Volume Node (HVN) | Price level with heaviest volume within one footprint | Max(volume-at-price) per bar | volume-at-price per bar | proxy_quantizable_now | Per-bar argmax of volume-at-price; black outline equivalent = local max | 需要 per-bar 的 volume-at-price 数据；可基于 Total Volume |
| Multiple HVN | 2+ consecutive footprints with HVN at same price | Cross-bar alignment of per-bar HVN price level | volume-at-price per bar; tick-level price alignment | needs_extra_data | Check if HVN price levels match across consecutive bars; requires tick size precision | 对价格粒度（tick size）和 bar size 敏感 |
| Trades Filter | Show only trades > X lots (e.g., 25 for 6E, 300 for ES) | Per-trade size threshold filter | tick-by-tick trade size data (exact lots per trade) | needs_extra_data | Filter individual trades by lot size; threshold per-instrument calibration | 无法检测 Iceberg（拆分后每单都小）；只能捕获未拆分大单 |
| Unfinished Business (Failed Auction) | High reversal: Bid=0 at high tick; Low reversal: Ask=0 at low tick | Reversal bar where extreme tick has non-zero opposing volume | tick-by-tick with per-tick bid/ask; footprint with per-price-level bid/ask | needs_extra_data | Detect reversal at bar extreme; check if opposing side volume at extreme tick is > 0 | 理论定义为 0；实际可能需要 epsilon 阈值；真正的零成交极少 |
| Absorption (Stopping Volume) | Huge volumes on BOTH Bid and Ask; price stops moving | Simultaneous high Bid and Ask volume with price stall / narrow range | tick-by-tick with aggressor flag; per-cell bid/ask volume | needs_extra_data | Detect Bid and Ask outliers at same price level; confirm with price range compression | "异常大"需要 rolling baseline 校准；可能跨多根 bar |
| Big Limit Orders (Passive Signature) | Unusually large volume on Bid (Limit Buy) or Ask (Limit Sell) at S/R | Outlier volume cell at S/R zone; interpreted as passive | tick-by-tick with aggressor flag; per-cell bid/ask volume | needs_extra_data | Volume outlier detection at S/R; note: cannot truly distinguish limit from market fill | 无法直接区分 Limit vs Market；是基于位置+大小的推断 |
| Aggressive Orders (Active Signature) | Large volumes on Bid (Sellers) or Ask (Buyers) at S/R; Delta confirms | Single-sided volume spike at S/R zone with Delta in same direction | tick-by-tick with aggressor flag; per-cell bid/ask volume | needs_extra_data | Single-sided outlier at S/R; Delta sign confirmation; requires instrument baseline | 同样无法 100% 区分 active vs passive；是推断性代理 |
| Volume Profile (Volume at Price) | Volume histogram at price; D/P/b/Thin shapes | Volume-at-price histogram over lookback period | tick-level or aggregated volume data per price level | proxy_quantizable_now | Build histogram: volume per price level over N bars; classify shapes by skewness/kurtosis | 可从聚合数据构建；lookback period 选择敏感 |
| Volume Accumulation | Heavy volume in rotation = institutions building positions | High volume within sideways range (rotation) | volume-at-price; range detection | proxy_quantizable_now | Detect rotation period; compute volume profile within range; identify HVN | 行为解释（建仓 vs 出货）需要 Bid/Ask 增强；仅从 Volume Profile 无法区分方向 |
| Iceberg Orders | Institutions split large orders into many small ones (e.g., 1+1+1...) | Not directly observable; proxy via rapid sequence of small trades at same price | tick-by-tick with exact trade sequence and timestamps | future_bucket | Sequence analysis: rapid small trades at same price level; but false positive rate high | 无法可靠检测；只能作为间接推断；算法拆分逻辑不透明 |
| DOM Pressure (Bid/Ask Pressure) | Delta direction + Imbalance direction + Stacked Imbalance direction | Composite indicator of net aggressive pressure | tick-by-tick with aggressor flag; full footprint matrix | needs_extra_data | Combine Delta, Imbalance, Stacked Imbalance into a directional pressure label (do not collapse into a single-number scalar) | 本书中的 DOM Pressure 完全基于成交数据，非 L2 挂单数据 |
| Exhaustion / Trapped Traders | Price-Delta Divergence + Absorption = momentum exhaustion | Divergence + absorption + volume climax at extreme | tick-by-tick with aggressor flag; full footprint matrix | needs_extra_data | Multi-signal composite: divergence + absorption + high volume at extreme price | 推断性较强；书中未明确命名为 Exhaustion；是概念映射 |
| Breakout Validity (Order Flow Angle) | Price penetrates heavy volume into low volume = strong momentum | Penetration of HVN into LVN; bid/ask direction aligned with breakout | tick-by-tick with aggressor flag; volume profile HVN/LVN | needs_extra_data | Identify HVN/LVN boundaries; monitor bid/ask during penetration; check alignment | 需要 Volume Profile 和 footprint 数据的组合；时间框架敏感 |
| Stop Runs (Implied) | Rapid price move through S/R with reversal; Unfinished Business left | Fast move through level + reversal + non-zero opposing volume at extreme | tick-by-tick with aggressor flag; per-tick bid/ask | needs_extra_data | Detect rapid excursion through S/R; check for reversal and unfinished business within N bars | 书中未明确命名；从 Unfinished Business + Rejection 机制映射 |
| Footprint Green/Red Cell | Green = Ask > Bid; Red = Bid > Ask; NOT Buyers vs Sellers | Per-cell color = sign(Ask - Bid) | per-cell bid/ask volume | needs_extra_data | Simple per-cell comparison; color heatmap of footprint matrix | 作者明确警告：颜色不等于买方/卖方力量；是半真半假的解读 |
| Glossary - Risk Reward Ratio (RRR) | Potential gain vs potential loss; e.g., SL=10, TP=20, RRR=2 | Ratio of TP distance to SL distance | price levels only | shell_only | Purely price-based; not an order flow concept; included for completeness as it appears in text | 本书中的 RRR 是通用交易概念，非订单流特有；与微观结构无关 |
| Volume Profile Trend Setup | Little "bump" (Volume Cluster) in thin trend profile = support/resistance | Local volume bump within thin volume profile | volume-at-price per trend segment | proxy_quantizable_now | Segment volume profile by trend; detect local bumps; compare to overall thinness | 区分"趋势中的集群"与"盘整中的积累"需要趋势检测前置 |
| Volume Profile Rejection Setup | Heaviest volumes within rejection = biggest fight zone | Volume-at-price within rejection bar/cluster; identify max volume level | volume-at-price; rejection bar detection | proxy_quantizable_now | Define rejection bar (strong reversal candle); compute volume profile within it; argmax | Rejection 的 bar 定义需要 price action 规则；可与 Volume Profile 独立使用 |
| Cumulative Delta Divergence (Confirmation) | Price heading up while Cumulative Delta heading down at S/R | Price direction vs cumulative delta direction mismatch at S/R zone | tick-by-tick with aggressor flag; cumulative delta per session; S/R zone definition | needs_extra_data | Monitor cumulative delta slope vs price slope at S/R; divergence = confirmation | 需明确 S/R 区域边界；1-minute 粒度常用于监测 |
| Confirmation Sequence (Passive -> Active) | Limit order or Absorption first, then Aggressive orders follow | Temporal sequence: absorption/limit signature followed by aggressive signature | tick-by-tick with aggressor flag; timestamped footprint sequence | needs_extra_data | Event sequence detection: passive absorption at T, then aggressive orders at T+N | "雪球效应"的序列逻辑；需要时间戳和事件顺序检测；N 的定义不明确 |
| Unfinished Business Magnet Effect | Price drawn to unfinished business level; likely to move through it | Price revisit to failed auction level within lookback period | tick-by-tick with per-tick bid/ask; unfinished business detection | needs_extra_data | Track detected unfinished business levels; measure revisit rate and penetration rate | 作者明确警告：不一定立即测试；可能长期远离；非确定性规则 |
| Low Volume Area (Stop Loss Logic) | Place SL behind heavy volume into low volume; if penetrated, momentum is strong | Penetration of HVN into LVN = momentum continuation signal | volume-at-price; HVN/LVN detection | proxy_quantizable_now | Identify HVN and adjacent LVN; if price moves through HVN into LVN, signal strong momentum | 作为动量突破/止损逻辑的量化代理；仅需 Volume Profile 数据 |

## FORMULAS_AND_ALGOS

- Delta (per footprint): `Delta = Ask - Bid` (per bar/footprint)
- Cumulative Delta: `CumulativeDelta(t) = Σ(Delta(i))` from session start i=0 to t; reset at each session open
- Imbalance threshold (diagonal): `Buying Imbalance = Ask_cell >= 3 * Bid_cell_diagonal` ; `Selling Imbalance = Bid_cell >= 3 * Ask_cell_diagonal`
- Stacked Imbalance: `Count_imbalance_cells >= 3` in consecutive price levels, same direction
- HVN: `HVN_price = argmax(volume-at-price)` within a single footprint
- Multiple HVN: `HVN_price(t) == HVN_price(t-1)` for 2+ consecutive footprints
- Unfinished Business (high reversal): `high_tick_Bid > 0` at bar extreme when reversal occurs
- Unfinished Business (low reversal): `low_tick_Ask > 0` at bar extreme when reversal occurs
- Trades Filter threshold (examples): `EUR Futures (6E) ~ 25 lots`; `ES (S&P 500 futures) ~ 300 lots`; target ~5-10 signals/day
- Volume Cluster detection: `volume-at-price > local_mean + K * local_std` (author uses visual heatmap; K not specified)
- Absorption volume baseline: `average_cell_volume = mean(recent_cell_volumes)`; outlier = `cell_volume >> average_cell_volume` on BOTH Bid and Ask
- RRR: `RRR = TakeProfit / StopLoss` (in pips; not an order flow concept)
- Fixed SL guidance: `SL ~ 10-20% of average daily volatility` (measured by ATR)
- Volume Profile shape classification (implied): D = balanced; P = uptrend + rotation; b = downtrend + rotation; Thin = strong trend, low volume accumulation
- Volume Profile Setup lookback: `30 Minute` recommended for intraday; `15 Minute` or `1 Hour` acceptable; do not go past 1 Hour

## NOT_QUANT_YET

1. **Iceberg Order Detection**: 作者明确承认 Iceberg 的拆分逻辑不可观测。Trades Filter 只能捕获未拆分的大单，Volume Cluster 只能检测累积效果。任何试图"量化检测 Iceberg"的尝试都面临根本性数据限制——拆分后的 trades 与正常小单在数据层面不可区分。
2. **Big Limit Order vs Market Order Distinction**: Footprint 数据无法直接区分成交来自 Limit Order 还是 Market Order。作者将大成交量 cell "推断"为 Limit Order 或 Aggressive Order，但这种推断是基于场景（在 S/R 区域、价格停滞 vs 移动）的贝叶斯式推断，而非直接观测。量化实现中无法 100% 区分。
3. **"Magnet Effect" of Unfinished Business**: 作者明确警告 Unfinished Business 并非 Holy Grail，价格可能长期远离且不测试。其"磁力"是行为金融学隐喻，缺乏可量化的预测边界（多久内测试？多大概率测试？）。
4. **Volume Cluster Color Depth Calibration**: 作者使用视觉颜色深浅来识别 Volume Cluster，但未提供跨 instrument 的客观阈值。颜色的"深浅"依赖于软件渲染逻辑和 instrument 的成交量分布，缺乏统一的统计标准化方法。
5. **Absorption Duration**: 吸收过程的"持续时间"（需要多少分钟/多少根 footprint 才能确认）未明确定义。作者说"it can take a few minutes"，但没有给出可量化的确认标准。
6. **Confirmation Sequence Timing (Snowball Effect)**: 书中描述了"先被动确认、后主动确认"的理想序列，但未定义两个事件之间的最大允许时间间隔。量化实现中需要自行设定 N-bar 窗口，这会影响检测率与误报率。
7. **Institutional Intent Inference**: 所有订单流模式（Volume Cluster = 机构建仓、Multiple HVN = 机构持续交易、Stacked Imbalance = 机构施压）都是基于成交量异常的"意图推断"。这些推断无法通过订单流数据本身验证——我们无法知道某个 Volume Cluster 确实是机构建仓还是散户的随机聚集。
8. **Instrument-Specific Threshold Transferability**: Trades Filter 的阈值（6E=25, ES=300）是作者的经验值，缺乏系统性的 per-instrument calibration 方法。不同 instrument、不同 session、不同波动率环境下的最优阈值需要大量样本外测试，书中未提供方法论。
9. **Delta Reliability in Rotations**: 作者指出 Delta 在旋转市中不可靠，因为机构混合使用市价单和限价单，但"旋转市"的定义本身就不是订单流数据能直接观测的——需要外部趋势检测工具来定义市场状态。
10. **Volume Profile Shape Classification**: D/P/b/Thin 的分类是作者基于视觉观察的定性分类，缺乏可量化的统计边界（偏度/峰度的阈值）。自动化分类这些形状需要额外的统计方法。
11. **Forex Data Quality Gap**: 书中明确承认 Forex 数据无法区分 Bid/Ask，这意味着所有基于 Delta、Imbalance、Cumulative Delta、Unfinished Business 的模式在 Forex 中完全失效。只有 Volume Cluster 和 HVN 可以勉强使用，但效力大减。

## NEXT_ACTION

1. **搭建订单流数据基础设施**：获取带 aggressor flag 的逐笔数据（如 CQG、Rithmic、CME 的 MDP），确认 Bid/Ask 分离能力。优先选择 Futures 市场（如 6E、ES），避免 Forex 的数据质量限制。
2. **构建 Footprint 矩阵解析器**：将 tick-by-tick 数据按 bar（如 30-minute、5-minute）聚合为 volume-at-price 矩阵，每个价格层级分别统计 Bid 和 Ask 成交量。这是所有后续特征的基础数据结构。
3. **实现 HVN 与 Multiple HVN 检测**：在每根 bar 的 volume-at-price 分布中识别 argmax（HVN），跨 bar 比对 HVN 价格层级以检测 Multiple HVN（2+ 连续 bar 的 HVN 对齐）。
4. **实现 Delta 与 Cumulative Delta 计算**：`Delta = Ask - Bid per bar`; `Cumulative Delta = session cumulative sum`。添加 session 起始时间管理和每日重置逻辑。标记 Price-Delta Divergence 事件。
5. **实现 Imbalance 与 Stacked Imbalance 检测**：对角线比较 footprint 矩阵中的相邻 cell pair（Bid_i vs Ask_{i+1} 或反向），设定 300% 阈值（可参数化）。检测连续 3+ 个 price level 的同一方向失衡以标记 Stacked Imbalance。
6. **实现 Unfinished Business 检测**：在反转 bar 中检查 extreme tick 的对侧成交量：若 high reversal 且 high_tick_Bid > 0，或 low reversal 且 low_tick_Ask > 0，则标记为 Failed Auction。需定义"反转"的检测规则（如后续 N 根 bar 价格反向移动）。
7. **实现 Trades Filter 大单检测**：对逐笔数据按 lot size 过滤（per-instrument 校准阈值）。分析 6E/ES 等常见 instrument 的 lot size 分布以确定合理阈值。记录检测到的异常大单的时间戳、价格、大小。
8. **实现 Volume Cluster 密度检测**：基于 volume-at-price 的 heatmap，使用局部统计方法（如局部均值 + K 倍标准差）识别 Volume Cluster。可与 Volume Profile 的 HVN 结合，作为支撑/阻力区域的候选生成器。
9. **探索 Volume Profile 形状自动分类**：基于日内 volume-at-price 分布的统计特征（均值、偏度、峰度、四分位距）对 D/P/b/Thin 形状进行自动化分类。这需要大量历史数据训练分类器。
10. **设计订单流特征的"市场状态边界"标注系统**：根据外部趋势检测（如 ADX、移动平均线状态）标注每根 bar 处于 trend/rotation，然后分别统计 Delta、Imbalance、Absorption 等特征在不同市场状态下的分布差异，验证作者的可靠性边界声明。
11. **整合确认信号的序列检测框架**：将 Big Limit Orders（大单 cell）、Absorption（双向巨量）、Aggressive Orders（单向巨量 + Delta 确认）和 Cumulative Delta Divergence 作为独立事件流，实现多事件序列检测（如 Absorption 后 N 根 bar 内出现 Aggressive Orders）。
12. **建立 per-instrument 的成交量基准库**：为每个 instrument 和每个主要 session（US、EU、Asia）建立 rolling average cell volume 和 lot size distribution 的基准，以支持 Trades Filter、Absorption、Big Limit Orders 的异常检测。

