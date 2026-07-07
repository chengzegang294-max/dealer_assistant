## BASIC_INFO
- title: Trading and Exchanges: Market Microstructure for Practitioners
- author: Larry Harris
- material_type: 教材/专著
- domain_tags: [market microstructure, trading mechanisms, liquidity, execution, market design]
- file_scope: Trading and Exchanges (Larry Harris).pdf
- source_file_size_mb: 11.37
- retain_mode: RETAINED_EXCERPTS
- current_repo_role: SECONDARY_STRUCTURED_NOTE

## MATERIAL_POSITIONING
- what_this_book_is: 一本系统介绍市场微观结构、交易机制与流动性供给的学术专著，涵盖订单类型、市场结构、参与者分类、交易成本与市场监管等核心主题。
- why_in_f2: 为 F2 建立市场微观结构的基础对象框架——包括参与者（dealer/broker/trader/investor）、订单（limit/market/stop）、市场结构（order-driven/quote-driven/hybrid）、流动性维度（spread/depth/resiliency）、交易成本（adverse selection/price impact/execution cost）以及价格发现机制。后续 A2、F1、订单流、盘口、执行质量评估均以本书定义为语义基准。
- not_a_strategy_book_because: 本书不给出可直接交易的策略或信号，而是描述市场运作机制、参与者行为与市场设计原理，属于机制与定义层面的基础教材。
- relation_to_order_flow_microstructure: 本书定义了订单簿、价差、深度、弹性、逆向选择等对象，这些概念是订单流分析与盘口解读的语义前提；没有本书的定义，后续订单流研究将缺乏统一的术语与测量边界。
- data_footprint_required: 需要 tick-by-tick 成交数据、Level-2 订单簿深度、order book 快照、逐笔委托与撤单记录，方能真实测量 spread、depth、impact、resiliency；仅凭 OHLCV 无法还原这些微观结构对象。

## CONTENT_STRUCTURE
- Part I: The Structure of Trading (Ch 1-7)
  - Ch 1 Introduction: 全书概览，市场结构、订单、参与者、流动性等核心概念总览。
  - Ch 2 Trading Stories: 通过具体交易场景引入市场运作逻辑。
  - Ch 3 The Trading Industry: 买方（buy side）与卖方（sell side）的划分，交易所、经纪商、做市商的角色。
  - Ch 4 Orders and Order Properties: 订单类型（market/limit/stop/hidden/iceberg）及其属性，流动性提供与流动性索取。
  - Ch 5 Market Structures: 市场结构分类——quote-driven、order-driven、hybrid，call auction 与 continuous trading 的对比。
  - Ch 6 Order-Driven Markets: 订单簿撮合机制、价格优先与时间优先、 discriminatory pricing 与 uniform pricing。
  - Ch 7 Brokers: 经纪商职能、佣金结构、智能订单路由（SOR）与最佳执行义务。
- Part II: The Benefits of Trade (Ch 8-12)
  - Ch 8 Why People Trade: 交易动机——对冲、投机、流动性需求、投资组合再平衡。
  - Ch 9 Good Markets: 市场质量（market quality）的维度——流动性、价格发现效率、公平性、低交易成本。
  - Ch 10 Informed Traders and Market Efficiency: 信息交易者（informed traders）的类型，价格发现过程，市场有效性。
  - Ch 11 Order Anticipators: 订单预判者（front-running、quote matching）的行为与影响。
  - Ch 12 Bluffers and Market Manipulation: 市场操纵（manipulation）类型、虚报订单（spoofing）、幌骗与监管。
- Part III: Liquidity Suppliers (Ch 13-18)
  - Ch 13 Dealers: 做市商（dealer）的库存管理、库存风险（inventory risk）、买卖价差来源。
  - Ch 14 Bid/Ask Spreads: 价差的构成——订单处理成本、库存成本、逆向选择（adverse selection）成本。
  - Ch 15 Block Traders: 大宗交易（block trades）的撮合机制、 upstairs market、对价格的影响。
  - Ch 16 Value Traders: 价值交易者作为最终流动性供给者的角色。
  - Ch 17 Arbitrageurs: 套利者作为信息交易者与流动性供给者的双重角色。
  - Ch 18 Buy-Side Traders: 买方交易者的执行策略、TWAP/VWAP/Implementation Shortfall 等算法交易框架。
- Part IV: Origins of Liquidity and Volatility (Ch 19-22)
  - Ch 19 Liquidity: 流动性的三维定义——宽度（width/tightness）、深度（depth）、弹性（resiliency）。
  - Ch 20 Volatility: 波动率的来源与信息到达、交易频率的关系。
  - Ch 21 Liquidity and Transaction Cost Measurement: 有效价差（effective spread）、已实现价差（realized spread）、价格影响（price impact）的测量方法。
  - Ch 22 Performance Evaluation and Prediction: 执行绩效评估、交易成本预测模型。
- Part V: Market Structures (Ch 23-27)
  - Ch 23 Index and Portfolio Markets: 指数与组合市场的交易机制、程序交易（program trading）。
  - Ch 24 Specialists: 纽约证券交易所专家（specialist）的职能与义务。
  - Ch 25 Internalization/Preferencing/Crossing: 订单内部化、优先匹配、交叉网络（crossing networks）对价格发现的影响。
  - Ch 26 Competition Within and Among Markets: 市场间竞争、市场分割（fragmentation）与整合。
  - Ch 27 Floor Versus Automated Trading Systems: 场内交易与自动交易系统的对比。
- Part VI: Bubbles, Crashes, and Market Regulation (Ch 28-29)
  - Ch 28 Bubbles, Crashes, and Circuit Breakers: 市场崩溃机制、熔断制度（circuit breakers）的设计与效果。
  - Ch 29 Insider Trading: 内幕交易（insider trading）的定义、监管与执法。

## RETAINED_EXCERPTS
- excerpt_id: E001
  source_hint: Ch 1 / Introduction
  quote: "Market structure consists of the trading rules, the physical layout, the information presentation systems, and the communication systems that traders use to arrange trades."
  why_kept: 定义市场结构的核心对象，为后续所有微观结构分析提供语义基准。
  quant_link: 市场结构决定可观测数据类型（order book vs. quote stream vs. trade tape）

- excerpt_id: E002
  source_hint: Ch 3 / The Trading Industry
  quote: "Liquidity is the ability to trade when you want to trade. Traders on the sell side supply liquidity. Traders on the buy side demand liquidity."
  why_kept: 流动性的基础定义与供需划分，是订单流分析中'流动性提供者/索取者'分类的理论来源。
  quant_link:  liquidity = f(order_book_depth, spread, resiliency)

- excerpt_id: E003
  source_hint: Ch 4 / Orders and Order Properties
  quote: "A market order is an instruction to trade at the best price currently available. A limit order is an instruction to trade at the best price available, but only if it is no worse than the limit price specified by the trader."
  why_kept: 明确区分市场订单与限价订单的定义，是订单分类与流动性归因的基础。
  quant_link:  market orders 消耗流动性；limit orders 提供流动性

- excerpt_id: E004
  source_hint: Ch 4 / Orders and Order Properties
  quote: "A stop order is an instruction to submit a market order if the price reaches or passes a stop price specified by the trader. Stop orders are often called stop-loss orders because traders use them to stop their losses."
  why_kept: 止损订单的定义及其触发机制，与波动率突破和订单簿压力释放有关。
  quant_link:  stop order 触发会产生集中流动性需求

- excerpt_id: E005
  source_hint: Ch 5 / Market Structures
  quote: "In quote-driven markets, dealers quote the prices at which they will buy and sell. Traders who want to trade with dealers must trade at those prices. In order-driven markets, traders submit orders to a central order book. The orders are arranged by price and time, and trades occur when orders match."
  why_kept: 两种基本市场结构的定义对比，决定数据观测方式（报价流 vs. 订单簿）。
  quant_link:  quote-driven → quote/transaction data; order-driven → order book + transaction data

- excerpt_id: E006
  source_hint: Ch 5 / Market Structures
  quote: "Hybrid markets mix characteristics of quote-driven, order-driven, and brokered markets. For example, although the New York Stock Exchange is essentially an order-driven market, it also uses a dealer— the specialist— to provide liquidity when the order book is empty."
  why_kept: 混合市场的定义，说明现代交易所（NYSE、Nasdaq）多为 hybrid 结构。
  quant_link:  hybrid markets 需要同时观察 dealer quote + order book + cross trades

- excerpt_id: E007
  source_hint: Ch 5 / Market Structures
  quote: "In continuous trading, traders can attempt to arrange their trades whenever the market is open. In call markets, all traders trade at the same time and price when the market is called."
  why_kept: 连续交易与集合竞价的对比，决定价格形成机制与可观测成交模式。
  quant_link:  call auction → single price, batch; continuous → sequential, price-time priority

- excerpt_id: E008
  source_hint: Ch 5 / Market Structures
  quote: "The two types of trading sessions are continuous trading sessions and call market sessions. In continuous trading, traders can attempt to arrange their trades whenever the market is open. In call markets, all traders trade at the same time and price when the market is called."
  why_kept: 交易时段类型定义，涉及开盘/收盘集合竞价与连续交易时段的切换。
  quant_link:  open/close auction vs. continuous session 需要区分建模

- excerpt_id: E009
  source_hint: Ch 6 / Order-Driven Markets
  quote: "Continuous rule-based order matching systems use the discriminatory pricing rule to price their trades. The rule is the same discriminatory pricing rule that oral auctions use. (Both are examples of two-sided auctions.)"
  why_kept: 连续竞价市场的定价规则——歧视性定价（discriminatory pricing），即撮合价格等于订单价格。
  quant_link:  discriminatory pricing → trade price = order limit price; uniform pricing → single clearing price

- excerpt_id: E010
  source_hint: Ch 7 / Brokers
  quote: "Brokers arrange trades for their clients. Unlike dealers, they do not trade for their own accounts. They are agents who find the best prices for their clients and who ensure that trades settle properly."
  why_kept: 经纪商与做市商的本质区分——agent vs. principal，影响委托执行数据的归因。
  quant_link:  broker data = agency trades; dealer data = principal trades + inventory changes

- excerpt_id: E011
  source_hint: Ch 10 / Informed Traders and Market Efficiency
  quote: "Informed traders trade on information that other traders do not yet have. They predict future price changes by analyzing fundamental data, technical patterns, or order flow. When they trade, their orders reveal their information to the market, and prices move toward their estimates of value."
  why_kept: 信息交易者的定义及其对价格发现的影响，是逆向选择与价格冲击的理论基础。
  quant_link:  informed trading intensity ∝ price impact per trade; adverse selection cost ∝ informed fraction

- excerpt_id: E012
  source_hint: Ch 10 / Informed Traders and Market Efficiency
  quote: "Uninformed traders trade for reasons other than information about future prices. They may trade to hedge risks, to obtain liquidity, to rebalance portfolios, or to meet margin calls. Their trades do not predict future price changes."
  why_kept: 非信息交易者的定义，与噪声交易、流动性交易同质，是价差中库存成本部分的理论基础。
  quant_link:  uninformed flow → mean-reverting inventory; informed flow → trending price impact

- excerpt_id: E013
  source_hint: Ch 12 / Bluffers and Market Manipulation
  quote: "Bluffers are traders who try to manipulate prices to profit from their distortions. They may submit false orders to create the impression of demand or supply, or they may trade to move prices in directions that benefit their other positions."
  why_kept: 市场操纵者（bluffers）的定义与行为模式，涉及幌骗、拉高出货等。
  quant_link:  manipulation detection → order cancellation rate, trade-to-order ratio, volume-synchronized price pattern

- excerpt_id: E014
  source_hint: Ch 13 / Dealers
  quote: "Dealers buy and sell for their own accounts. They profit from the spread between their bid and ask prices. They also manage their inventory positions to avoid losses from adverse price changes."
  why_kept: 做市商（dealer）的核心定义与盈利模式，是价差与库存风险分析的对象。
  quant_link:  dealer inventory ∝ net position; spread = f(inventory risk + adverse selection + order processing)

- excerpt_id: E015
  source_hint: Ch 14 / Bid/Ask Spreads
  quote: "The bid/ask spread is the difference between the highest price at which a dealer is willing to buy (the bid) and the lowest price at which a dealer is willing to sell (the ask). The spread is the cost of immediacy. It compensates dealers for the costs of providing liquidity."
  why_kept: 买卖价差的定义与经济学解释——即时性的成本、做市商提供流动性的补偿。
  quant_link:  spread = ask - bid; relative spread = (ask-bid)/mid; effective spread = 2|trade_price - mid|

- excerpt_id: E016
  source_hint: Ch 14 / Bid/Ask Spreads
  quote: "Dealers recover their losses to informed speculators by widening the spread between the bid and ask prices at which they will buy and sell. Uninformed traders therefore pay more for their trades when dealers lose a lot to informed traders. In effect, uninformed traders lose to well-informed traders through the intermediation of the dealer."
  why_kept: 逆向选择（adverse selection）如何通过价差传导：非信息交易者通过价差补贴信息交易者。
  quant_link:  adverse selection component of spread = expected loss to informed traders = f(information asymmetry)

- excerpt_id: E017
  source_hint: Ch 14 / Bid/Ask Spreads
  quote: "Adverse selection risk is the risk that a trader on the other side of a trade knows more about the value of the instrument than the dealer does. When dealers trade with informed traders, they lose money on average."
  why_kept: 逆向选择风险的定义，是做市商定价与价差设计的核心约束。
  quant_link:  adverse selection spread = (P_informed × Loss_to_informed) / (P_informed + P_uninformed)

- excerpt_id: E018
  source_hint: Ch 14 / Bid/Ask Spreads
  quote: "Inventory risk is the risk that the price of a security will change before the dealer can unload an unwanted inventory position. Dealers who hold large inventories are exposed to price changes that may cause them losses."
  why_kept: 库存风险的定义，是价差中库存成本部分的理论基础。
  quant_link:  inventory risk ∝ position_size × price_volatility; inventory cost component = f(inventory holding period)

- excerpt_id: E019
  source_hint: Ch 15 / Block Traders
  quote: "Block traders arrange large trades that would disrupt the market if they were submitted directly to the exchange. They find counterparties in the upstairs market, negotiate prices, and arrange for the exchange to clear the trade."
  why_kept: 大宗交易（block trading）的定义与 upstairs market 机制，对价格冲击的规避。
  quant_link:  block trade impact = f(trade_size, market_depth, information_content); upstairs market = bilateral negotiation

- excerpt_id: E020
  source_hint: Ch 19 / Liquidity
  quote: "Liquidity has three dimensions: tightness, depth, and resiliency. Tightness refers to the cost of trading. Depth refers to the size of a trade that can be arranged at a given cost. Resiliency refers to the speed at which prices recover from a random shock."
  why_kept: 流动性的三维定义（宽度/深度/弹性），是流动性测量的核心框架。
  quant_link:  tightness = spread; depth = order_book_size at best bid/ask; resiliency = recovery speed after shock

- excerpt_id: E021
  source_hint: Ch 21 / Liquidity and Transaction Cost Measurement
  quote: "The effective spread is twice the difference between the trade price and the midpoint of the quoted bid and ask prices at the time of the trade. The realized spread is the difference between the trade price and the midpoint of the quoted bid and ask prices some time after the trade."
  why_kept: 有效价差与已实现价差的定义，是测量交易成本与逆向选择的标准方法。
  quant_link:  effective spread = 2|price - mid|; realized spread = 2|price - mid_post|; adverse selection = effective - realized

- excerpt_id: E022
  source_hint: Ch 21 / Liquidity and Transaction Cost Measurement
  quote: "Price impact is the change in price that results from a trade. It measures the permanent effect of a trade on the market price. The temporary effect is the difference between the trade price and the midpoint before the trade."
  why_kept: 价格冲击（price impact）的定义——永久性 vs. 暂时性效应的区分。
  quant_link:  temporary impact = effective spread/2; permanent impact = price_change after trade; total impact = temporary + permanent

- excerpt_id: E023
  source_hint: Ch 21 / Liquidity and Transaction Cost Measurement
  quote: "Transaction costs include the bid/ask spread, brokerage commissions, price impact, and the opportunity cost of failing to complete a trade. Execution costs are the costs of arranging a trade, excluding the opportunity cost of failing to trade."
  why_kept: 交易成本与执行成本的定义及包含范围，是绩效评估的边界设定。
  quant_link:  transaction cost = spread + commission + impact + opportunity cost; execution cost = spread + commission + impact

- excerpt_id: E024
  source_hint: Ch 9 / Good Markets
  quote: "Market quality is the extent to which a market satisfies the needs of traders. Good markets are liquid, fair, and efficient. They have low transaction costs, prices that reflect fundamental values, and rules that prevent manipulation and fraud."
  why_kept: 市场质量（market quality）的定义与维度，是评估市场设计的综合框架。
  quant_link:  market quality = f(liquidity, price_discovery_efficiency, fairness, transaction_cost, transparency)

- excerpt_id: E025
  source_hint: Ch 10 / Informed Traders and Market Efficiency
  quote: "Price discovery is the process by which markets determine the prices of securities. Informed traders contribute to price discovery by trading on their information and causing prices to move toward their estimates of value."
  why_kept: 价格发现（price discovery）的定义与信息交易者的角色。
  quant_link:  price discovery efficiency = |price - fundamental_value|; speed = time for price to reflect new information

- excerpt_id: E026
  source_hint: Ch 20 / Volatility
  quote: "Volatility is the rate at which prices change. It is a measure of uncertainty about the value of a security. High volatility indicates that traders disagree about values or that new information is arriving quickly."
  why_kept: 波动率的定义及其与信息到达和交易者分歧的关系。
  quant_link:  volatility = std(returns) or realized variance; information flow ∝ volatility^2

- excerpt_id: E027
  source_hint: Ch 6 / Order-Driven Markets
  quote: "In a continuous trading market, the order book contains all standing orders that have not yet been filled. When a new order arrives, the matching system checks whether it can be filled against standing orders. If it can, a trade occurs. If not, the new order is added to the book."
  why_kept: 连续竞价市场订单簿的运作机制，是盘口与订单流分析的直接描述。
  quant_link:  order book state = {bid_levels, ask_levels, volume, time_priority}; matching engine = price-time priority

- excerpt_id: E028
  source_hint: Ch 5 / Market Structures
  quote: "In an oral auction, traders call out their bids and offers, and other traders respond. In an electronic auction, traders enter their orders into a computer system, which matches them according to the rules of the auction."
  why_kept: 拍卖市场的基本机制， oral vs. electronic，涉及价格形成规则。
  quant_link:  auction type → pricing rule (discriminatory vs. uniform); clearing mechanism

- excerpt_id: E029
  source_hint: Ch 11 / Order Anticipators
  quote: "Order anticipators are traders who try to profit by guessing the trading intentions of other traders. They include front runners, who trade ahead of large orders, and quote matchers, who place orders to match the quotes of other traders."
  why_kept: 订单预判者的定义，涉及订单流预测与前置交易（front-running）的检测。
  quant_link:  front-running detection = trade sequence before large block; quote matching = order placement pattern

- excerpt_id: E030
  source_hint: Ch 25 / Internalization
  quote: "Internalization is the practice of filling a client's order against the broker's own inventory rather than sending it to the market. Preferencing is the practice of directing orders to a particular dealer in exchange for payments."
  why_kept: 订单内部化与优先匹配的定义，涉及市场分割与最佳执行问题。
  quant_link:  internalization → trade not reported to exchange; payment for order flow → price improvement or conflict of interest

## CORE_CONCEPTS
- concept_name: market structure
  definition_from_text: Market structure consists of the trading rules, the physical layout, the information presentation systems, and the communication systems that traders use to arrange trades. (Ch 1)
  behavioral_mechanism:  determines which orders are valid, how they are presented, how they are matched, and what information is revealed to whom. Different structures produce different liquidity, transparency, and price discovery outcomes.
  data_objects_involved: order types, trading rules, matching engine, disclosure rules, physical/electronic infrastructure
  quant_boundary: order book snapshots, trade tape, quote streams, regulatory filing data

- concept_name: dealer
  definition_from_text: A dealer is a trader who buys and sells for his own account, expecting to profit from the bid/ask spread and from favorable price changes in his inventory. (Ch 13)
  behavioral_mechanism: Dealers provide immediacy by standing ready to trade. They set bid and ask prices based on inventory risk and adverse selection. When inventory deviates from target, they adjust prices to induce trades that restore balance.
  data_objects_involved: bid price, ask price, inventory position, target inventory, spread, quote duration
  quant_boundary: quote data (bid/ask/size), inventory changes, position reports

- concept_name: broker
  definition_from_text: A broker is an agent who arranges trades for clients. Brokers do not trade for their own accounts. They find counterparties, negotiate terms, and ensure settlement. (Ch 7)
  behavioral_mechanism: Brokers reduce search costs and provide agency services. They may offer smart order routing (SOR) to obtain best execution across multiple venues. They also may internalize orders or accept payment for order flow.
  data_objects_involved: commission, order routing, best execution, client order, agency relationship
  quant_boundary: order routing records, execution quality reports, 606 reports (US)

- concept_name: informed trader
  definition_from_text: An informed trader is a trader who possesses information about future price changes that other traders do not yet have. (Ch 10)
  behavioral_mechanism: Informed traders trade in the direction of their information. Their orders cause permanent price impacts because they move prices toward their estimates of fundamental value. Dealers lose to them on average, so spreads widen to compensate.
  data_objects_involved: information signal, trade direction, position size, holding horizon, permanent price impact
  quant_boundary: trade data with aggressor side, post-trade price drift, news timestamps

- concept_name: uninformed trader
  definition_from_text: An uninformed trader trades for reasons unrelated to information about future prices—such as hedging, liquidity needs, portfolio rebalancing, or margin calls. (Ch 10)
  behavioral_mechanism: Uninformed traders do not predict future price changes. Their trades create temporary price impacts that revert. They pay the spread and effectively subsidize liquidity providers through the adverse selection component of the spread.
  data_objects_involved: hedge ratio, liquidity shock, portfolio weights, margin status, trade direction
  quant_boundary: fund flow data, ETF creation/redemption baskets, index rebalancing schedules

- concept_name: liquidity trader
  definition_from_text: A liquidity trader is a trader who needs to trade to obtain cash or to invest cash, but does not have information about future prices. Often treated as a subset of uninformed traders. (Ch 10, implicit)
  behavioral_mechanism: Liquidity traders demand immediacy and are willing to pay the spread. Their urgency determines their price sensitivity and choice between market orders and limit orders.
  data_objects_involved: urgency, trade size, price sensitivity, order type choice, time horizon
  quant_boundary: order type mix (market vs. limit), time-of-day patterns, withdrawal/deposit correlations

- concept_name: limit order
  definition_from_text: A limit order is an instruction to trade at the best price available, but only if it is no worse than the limit price specified by the trader. (Ch 4)
  behavioral_mechanism: Limit orders provide liquidity by adding visible or hidden depth to the order book. They expose the submitter to adverse selection risk (the free trading option problem) and non-execution risk. They are executed via price-time priority in most order-driven markets.
  data_objects_involved: limit price, quantity, side, time-in-force, hidden flag, iceberg flag, priority
  quant_boundary: order book messages (add/modify/cancel), fill events, queue position data

- concept_name: market order
  definition_from_text: A market order is an instruction to trade at the best price currently available. (Ch 4)
  behavioral_mechanism: Market orders demand immediacy and consume liquidity. They are filled against the best available limit orders or dealer quotes. They carry price uncertainty (no guarantee of execution price) but no non-execution risk.
  data_objects_involved: quantity, side, execution price, slippage, fill time, venue
  quant_boundary: trade records with aggressor flag, best bid/ask at execution time, slippage relative to mid

- concept_name: stop order
  definition_from_text: A stop order is an instruction to submit a market order if the price reaches or passes a stop price specified by the trader. (Ch 4)
  behavioral_mechanism: Stop orders are dormant until triggered. When triggered, they become market orders and demand liquidity. They can accelerate price movements if many stop orders cluster at similar prices, creating gaps or cascades.
  data_objects_involved: stop price, trigger direction, triggered order type (market/limit), cluster density
  quant_boundary: order book depth near stop clusters, trigger events, post-trigger price paths

- concept_name: order-driven market
  definition_from_text: An order-driven market is a market in which traders submit orders to a central order book, and trades occur when orders match according to the rules of the market. (Ch 5, Ch 6)
  behavioral_mechanism: Order-driven markets use price-time priority or other matching rules. Liquidity is provided by limit orders. Transparency is high because the order book is visible. Examples include most modern electronic exchanges.
  data_objects_involved: order book, matching engine, price priority, time priority, limit order, visible depth
  quant_boundary: Level-2 order book data, market-by-order (MBO) feeds, matching engine rules

- concept_name: quote-driven market
  definition_from_text: A quote-driven market is a market in which dealers quote bid and ask prices at which they will trade, and traders who want to trade must trade at those prices. (Ch 5)
  behavioral_mechanism: Quote-driven markets rely on dealer capital to provide liquidity. Traders see quotes but not the full order book. Spreads are set by dealers based on inventory risk and adverse selection. Examples include NASDAQ (historically) and OTC markets.
  data_objects_involved: dealer quote, bid, ask, spread, quote size, quote duration, inventory
  quant_boundary: quote feeds (Level-1), dealer position data, TRACE/MSRB transaction reports

- concept_name: hybrid market
  definition_from_text: A hybrid market mixes characteristics of quote-driven, order-driven, and brokered markets. (Ch 5)
  behavioral_mechanism: Hybrid markets combine a visible limit order book with dealer quotes and sometimes crossing networks or upstairs brokers. The NYSE is the classic example: a specialist/dealer provides liquidity alongside the order book.
  data_objects_involved: order book, dealer quote, crossing network, specialist role, upstairs market
  quant_boundary: consolidated tape, order book + dealer quotes + dark pool prints

- concept_name: spread / bid-ask spread
  definition_from_text: The bid/ask spread is the difference between the highest price a dealer is willing to buy (bid) and the lowest price a dealer is willing to sell (ask). It is the cost of immediacy. (Ch 14)
  behavioral_mechanism: The spread compensates dealers for three costs: order processing, inventory holding, and adverse selection. The adverse selection component is the loss dealers expect to incur when trading with informed traders. In order-driven markets, the spread is the gap between the best bid and best ask in the order book.
  data_objects_involved: bid, ask, midpoint, quoted spread, effective spread, realized spread, spread components
  quant_boundary: quote data, trade data, post-trade price data (for realized spread)

- concept_name: depth
  definition_from_text: Depth is the size of a trade that can be arranged at a given cost. It is measured in units available at a given price of liquidity. (Ch 19)
  behavioral_mechanism: Depth reflects the cumulative size of standing orders at each price level. It determines how much a large trade will move the price. Shallow depth implies high price impact for large orders.
  data_objects_involved: bid/ask depth, cumulative depth, depth profile, depth at price levels
  quant_boundary: Level-2 order book (bid/ask size at each level), full order book snapshots

- concept_name: liquidity
  definition_from_text: Liquidity is the ability to trade when you want to trade. (Ch 3, Ch 19)
  behavioral_mechanism: Liquidity has three dimensions: tightness (width/spread), depth (size available), and resiliency (speed of recovery after a shock). Markets with high liquidity allow large trades with minimal price impact and fast recovery.
  data_objects_involved: tightness, depth, resiliency, trading volume, turnover, price impact per unit volume
  quant_boundary: order book depth, spread, resiliency metrics, volume, turnover ratio

- concept_name: resiliency
  definition_from_text: Resiliency is the speed at which prices recover from a random shock. It measures how quickly a market returns to its normal state after a large trade or information event. (Ch 19)
  behavioral_mechanism: Resiliency depends on the speed with which new limit orders arrive to replenish the book and the speed with which arbitrageurs and value traders respond to price deviations. Low resiliency markets have persistent price impacts.
  data_objects_involved: recovery time, post-trade price path, order book replenishment rate, autocorrelation of returns
  quant_boundary: tick data, order book event timestamps, post-trade price trajectory

- concept_name: inventory risk
  definition_from_text: Inventory risk is the risk that the price of a security will change before the dealer can unload an unwanted inventory position. (Ch 14)
  behavioral_mechanism: Dealers manage inventory risk by adjusting quotes to induce trades that restore their target inventory. High inventory risk leads to wider spreads and more aggressive quote revisions. Inventory risk is distinct from adverse selection risk because it does not depend on the counterparty's information.
  data_objects_involved: inventory position, target inventory, price volatility, holding period, inventory cost
  quant_boundary: dealer inventory data, quote revision frequency, inventory-target deviation

- concept_name: adverse selection
  definition_from_text: Adverse selection is the risk that a trader on the other side of a trade knows more about the value of the instrument than the dealer does. (Ch 14)
  behavioral_mechanism: Adverse selection arises from information asymmetry. When dealers trade with informed traders, they lose on average. They recover these losses by widening the spread, which imposes a tax on uninformed traders. In order-driven markets, limit order submitters face adverse selection when their orders are picked off by informed traders.
  data_objects_involved: informed trader probability, pricing error, expected loss, spread component, information asymmetry
  quant_boundary: effective spread vs. realized spread decomposition, post-trade price drift, VPIN (volume-synchronized probability of informed trading)

- concept_name: price impact
  definition_from_text: Price impact is the change in price that results from a trade. It measures the permanent effect of a trade on the market price. (Ch 21)
  behavioral_mechanism: Price impact has a temporary component (execution cost) and a permanent component (information effect). The temporary component is due to liquidity demand; the permanent component is due to the information revealed by the trade. In aggregate, price impact is a function of trade size, information content, and market depth.
  data_objects_involved: trade size, mid-price before/after, temporary impact, permanent impact, information content
  quant_boundary: tick data with trade direction, post-trade price trajectory, market depth at execution time

- concept_name: execution cost / transaction cost
  definition_from_text: Transaction costs include the bid/ask spread, brokerage commissions, price impact, and the opportunity cost of failing to complete a trade. Execution costs are the costs of arranging a trade, excluding the opportunity cost of failing to trade. (Ch 21)
  behavioral_mechanism: Execution cost is measured by effective spread (relative to mid) or implementation shortfall (relative to arrival price). It decomposes into spread cost, delay cost, and market impact. Transaction cost adds missed-trade opportunity cost and commission.
  data_objects_involved: effective spread, implementation shortfall, delay cost, market impact, commission, opportunity cost
  quant_boundary: trade data, quote data at order entry time, benchmark price (arrival price, VWAP)

- concept_name: market quality
  definition_from_text: Market quality is the extent to which a market satisfies the needs of traders. Good markets are liquid, fair, and efficient. (Ch 9)
  behavioral_mechanism: Market quality is a multidimensional concept involving liquidity (tightness, depth, resiliency), price discovery efficiency (speed and accuracy of price adjustment to information), fairness (equal treatment of orders), and transparency (availability of pre-trade and post-trade information).
  data_objects_involved: liquidity, price discovery efficiency, fairness, transparency, transaction cost, volatility
  quant_boundary: composite market quality indices, transaction cost metrics, price discovery metrics, market structure data

- concept_name: price discovery
  definition_from_text: Price discovery is the process by which markets determine the prices of securities. Informed traders contribute to price discovery by trading on their information and causing prices to move toward their estimates of value. (Ch 10)
  behavioral_mechanism: Price discovery efficiency is measured by how quickly and accurately prices reflect fundamental information. In efficient markets, prices are close to values and changes are unpredictable. The speed of price discovery depends on the presence of informed traders, transparency rules, and market structure.
  data_objects_involved: price deviation from fundamental value, information arrival rate, price adjustment speed, return predictability
  quant_boundary: high-frequency price data, news timestamps, fundamental value proxies, variance ratio tests

- concept_name: manipulation
  definition_from_text: Manipulation is the practice of trading or placing orders to deceive other traders about the demand for or supply of a security, or to move prices in a direction that benefits the manipulator. (Ch 12)
  behavioral_mechanism: Types include bluffing (spoofing), wash trading, cornering, and front-running. Manipulators distort price discovery and impose costs on legitimate traders. Detection relies on identifying patterns that are inconsistent with legitimate trading motives.
  data_objects_involved: order cancellation rate, trade-to-order ratio, price deviation, volume pattern, account linkage
  quant_boundary: order-level audit trail, message data (add/modify/cancel), account and position records

- concept_name: regulation
  definition_from_text: Regulation consists of the rules and oversight that govern trading to ensure fair, orderly, and transparent markets. (Ch 28, Ch 29)
  behavioral_mechanism: Regulatory objectives include preventing manipulation, insider trading, and systemic risk; ensuring disclosure; and protecting investors. Regulations affect market structure, trading costs, and the distribution of information among traders.
  data_objects_involved: rules, disclosure requirements, surveillance, enforcement, circuit breakers, insider trading prohibitions
  quant_boundary: regulatory filings, rule changes, enforcement actions, market structure evolution data

- concept_name: auction
  definition_from_text: An auction is a market mechanism in which traders submit bids and offers, and trades are arranged according to a pricing rule. (Ch 5, Ch 6)
  behavioral_mechanism: Auctions can be single-price (uniform pricing) or discriminatory. Call auctions collect orders over a period and clear at a single price. Continuous auctions match orders sequentially. Oral auctions involve face-to-face bidding; electronic auctions use centralized order matching.
  data_objects_involved: bids, offers, pricing rule, clearing price, uniform pricing, discriminatory pricing, order aggregation
  quant_boundary: auction parameters, order submission schedules, clearing price, volume at clearing

- concept_name: continuous trading
  definition_from_text: Continuous trading is a trading session in which traders can attempt to arrange their trades whenever the market is open. Trades occur sequentially as orders arrive and match against standing orders. (Ch 5)
  behavioral_mechanism: Continuous trading provides immediacy but may fragment liquidity if order arrival is lumpy. Prices are determined by the order book state at each moment. Most equity markets operate continuous trading during regular hours.
  data_objects_involved: order arrival rate, matching frequency, price path, order book state evolution
  quant_boundary: tick-by-tick trade and order book data, event timestamps, queue position changes

- concept_name: call auction
  definition_from_text: A call auction is a trading session in which all traders trade at the same time and at a single price when the market is called. Orders are collected during a batching period and matched at a clearing price that maximizes volume. (Ch 5)
  behavioral_mechanism: Call auctions concentrate liquidity and reduce price manipulation. They are used for market opens and closes, and for thinly traded securities. The single price eliminates the bid-ask spread at the clearing moment.
  data_objects_involved: order collection period, batching, clearing price, volume maximization, single price
  quant_boundary: call auction orders, indicative price, uncrossing volume, final clearing price

- concept_name: volatility
  definition_from_text: Volatility is the rate at which prices change. It is a measure of uncertainty about the value of a security. High volatility indicates that traders disagree about values or that new information is arriving quickly. (Ch 20)
  behavioral_mechanism: Volatility is both a cause and a consequence of trading activity. It affects liquidity because dealers and limit order traders demand higher compensation for bearing risk in volatile markets. It also affects the value of trading options and the probability of stop order triggering.
  data_objects_involved: return standard deviation, realized variance, implied volatility, intraday range, GARCH parameters
  quant_boundary: OHLCV, high-frequency returns, option implied volatility, realized variance estimators

- concept_name: information asymmetry
  definition_from_text: Information asymmetry exists when some traders know more about the value of a security than others. It is the source of adverse selection and the primary determinant of the bid-ask spread. (Ch 10, Ch 14)
  behavioral_mechanism: Information asymmetry drives informed trading, which in turn causes permanent price impacts and widens spreads. The degree of asymmetry varies by stock, by time (e.g., around earnings announcements), and by market structure (e.g., pre-trade transparency).
  data_objects_involved: private information, public information, information arrival rate, informed trading intensity, spread
  quant_boundary: news data, earnings announcement calendars, insider trading records, VPIN, PIN models

- concept_name: trade size
  definition_from_text: Trade size is the number of units traded in a transaction. Large trades have greater price impact than small trades because they exhaust more of the available liquidity. (Ch 15, Ch 21)
  behavioral_mechanism: Trade size interacts with market depth to determine price impact. In block trading markets, large orders are negotiated upstairs to avoid disrupting the public market. In order-driven markets, large orders may be sliced into smaller pieces (icebergs) to minimize impact.
  data_objects_involved: quantity, notional value, block threshold, iceberg size, participation rate
  quant_boundary: trade size distribution, block trade flags, iceberg order detection, volume profile

## QUANTIZATION_TABLE
| concept | raw_rule_from_text | observable_proxy | data_needed | quant_status | implementation_hint | notes |
|---|---|---|---|---|---|---|
| market structure | Market structure = trading rules + physical layout + information systems + communication systems | venue identifier + trading session type + order type availability | market structure reference data (MIC, segment, session schedule, supported order types) | shell_only | Map venue MIC to structure type (order-driven/quote-driven/hybrid/auction); use as categorical variable in execution analysis. | No direct numerical proxy; structure is a categorical classification that determines what data to collect and how to interpret it. |
| dealer | Dealer buys/sells for own account, profits from spread + inventory changes; sets bid/ask based on inventory risk and adverse selection | quote presence (bid/ask) + quote size + inventory changes in principal trades | dealer quote feed (Level-1 with size), dealer transaction reports (TRACE/MSRB), inventory snapshots | needs_extra_data | Identify dealer-initiated quotes vs. customer orders; track inventory position deviation from target; requires dealer identity in data. | Without dealer identity tagging, cannot distinguish dealer principal trades from agency trades in consolidated tape. |
| broker | Broker arranges trades for clients, does not trade for own account; provides SOR and best execution | agency trade volume + routing destination + commission rate | order routing records (605/606 reports), execution quality reports, venue-by-venue fill data | needs_extra_data | Use SEC 606 routing reports to map broker routing behavior; best execution measurement requires arrival price vs. execution price comparison. | Broker function is operational; quantifiable only through execution quality and routing data, not through market price data alone. |
| informed trader | Informed trader has superior information about future price changes; trades cause permanent price impact | permanent price impact after trade; post-trade price drift; trade direction correlation with subsequent returns | tick-by-tick trade data with aggressor side + post-trade price trajectory (e.g., 5-min/30-min/close returns) | needs_extra_data | Measure permanent impact as price change from pre-trade mid to post-trade mid (e.g., 30-min later); if impact persists and does not revert, trade likely contained information. | PIN/VPIN models estimate informed trading probability; but these require full order-level data or volume bucket classification. |
| uninformed trader | Uninformed trader trades for hedging/liquidity/rebalancing; trades do not predict future price changes | temporary price impact that reverts; trade direction uncorrelated with subsequent returns; order flow autocorrelation | tick-by-tick trade data with direction + post-trade reversion analysis + fund flow data | needs_extra_data | Measure temporary impact as difference between effective spread and realized spread; if post-trade price reverts to pre-trade mid, impact was temporary (liquidity-driven). | Distinguishing informed vs. uninformed at trade level is impossible without post-trade price path or external information event data. |
| liquidity trader | Liquidity trader needs to trade for cash/investment needs, no price-predictive information; subset of uninformed traders | order type mix (market vs. limit) + time-of-day concentration + correlation with cash flow events | order-level data with order type + time stamps + account-type classification (retail/institutional) | needs_extra_data | Classify orders by urgency: market orders and marketable limit orders indicate liquidity demand; non-marketable limit orders indicate liquidity supply. | 'Liquidity trader' is a behavioral classification; observable only through order type choice and timing, not directly through price data. |
| limit order | Limit order = instruction to trade at best price available, but not worse than limit price; provides liquidity | order book depth at each price level; visible bid/ask size; queue length; fill rate | Level-2 order book (bid/ask size at N levels), full order book messages (MBO), queue position data | needs_extra_data | Measure limit order fill probability, time-to-fill, and adverse selection cost (pick-off risk) using order book event data; compare limit price to post-trade mid. | OHLCV completely loses limit order information; need order book snapshots or message-level data. |
| market order | Market order = instruction to trade at best price currently available; consumes liquidity; no price guarantee | trade price relative to best quote at submission time; slippage; fill rate | tick data with trade records + best bid/ask at submission time + aggressor flag | needs_extra_data | Compute slippage = |trade price - mid at submission|; measure immediate price impact as change in mid after trade; fill rate = filled quantity / ordered quantity. | In OHLCV, market orders are indistinguishable from limit orders; need trade-by-trade data with direction and quote context. |
| stop order | Stop order = instruction to submit market order if price reaches stop price; often called stop-loss | trigger events at stop clusters; post-trigger price path; cascade detection | order book depth near stop price levels + trade data with stop-trigger flags + price gap events | needs_extra_data | Detect stop cascades by monitoring order book depth exhaustion at clustered price levels; measure post-trigger volatility and gap size. | Stop orders are often invisible in public data until triggered; need broker order book or internal flow data. |
| order-driven market | Order-driven market: traders submit orders to central order book; trades occur when orders match by price-time priority | order book depth profile; price-time priority matching; visible bid-ask spread from order book | Level-2 order book data (MBO preferred); matching engine rules; order addition/modification/cancel messages | needs_extra_data | Model order book as discrete price levels with quantities; simulate matching engine to predict trade price and slippage for hypothetical orders. | Order-driven market mechanics are inherently unobservable without order book data; OHLCV only shows trade outcomes, not the book state. |
| quote-driven market | Quote-driven market: dealers quote bid/ask; traders must trade at dealer prices; liquidity from dealer capital | dealer quote stream (bid/ask/size); quote revision frequency; dealer inventory snapshots | dealer quote feed (Level-1 with size), inventory data, transaction reports tagged by dealer/customer | needs_extra_data | Track quote half-life, spread decomposition (order processing + inventory + adverse selection), and inventory mean-reversion speed using dealer-level data. | Quote-driven markets require dealer identity and inventory data; consolidated tape alone insufficient. |
| hybrid market | Hybrid market mixes quote-driven, order-driven, and brokered characteristics; e.g., NYSE with specialist + order book | consolidated view: order book + dealer quotes + crossing/dark pool prints; multi-venue execution distribution | consolidated market data (CTS/UTP), SIP feeds, order book data from primary exchange, dark pool ATS prints | needs_extra_data | Reconstruct multi-venue liquidity map: visible book + dealer quote + dark pool liquidity; measure fragmentation index and venue-level fill rates. | Hybrid market quantification requires stitching together data from multiple venues and mechanisms; SIP alone insufficient. |
| spread / bid-ask spread | Spread = ask - bid; cost of immediacy; compensates dealer for order processing, inventory risk, and adverse selection | quoted spread (ask-bid); effective spread (2*abs(trade_price - mid)); realized spread (2*abs(trade_price - mid_post)); relative spread | quote data (best bid/ask) + trade data (price, direction) + post-trade price data (mid at T+5min/T+30min) | needs_extra_data | Decompose spread: effective spread - realized spread = adverse selection component; realized spread = dealer gross profit; effective spread = total execution cost. | Can approximate quoted spread from OHLC if intraday high/low approximates bid/ask extremes, but this is a very noisy proxy. |
| depth | Depth = size of trade that can be arranged at a given cost; measured in units available at a given price of liquidity | cumulative bid/ask size at 1, 5, 10 ticks from best; depth profile; depth asymmetry (bid/ask imbalance) | Level-2 order book (bid/ask size at each level); full order book snapshots; depth-of-market (DOM) data | needs_extra_data | Compute depth-to-trade ratio = cumulative depth / average trade size; measure depth exhaustion events and their correlation with price moves. | Depth is fundamentally an order book object; cannot be inferred from trade prices alone. |
| liquidity | Liquidity = ability to trade when you want to trade; three dimensions: tightness, depth, resiliency | composite liquidity proxy: 1/spread × depth × resiliency_speed; Amihud illiquidity ratio; price impact per dollar volume | spread data + depth data + volume data + price impact data; for Amihud: daily OHLCV + absolute return | needs_extra_data | Amihud ratio = |return| / dollar_volume uses OHLCV only but is a coarse proxy; true liquidity requires spread + depth + resiliency simultaneously. | Amihud is proxy_quantizable_now with OHLCV, but it is a very noisy, low-frequency proxy that misses depth and resiliency entirely. |
| resiliency | Resiliency = speed at which prices recover from a random shock; market returns to normal state after large trade | post-trade price recovery half-life; autocorrelation decay of returns after shock; order book replenishment time | tick data with post-trade price path + order book event timestamps (add/cancel orders after trade) | needs_extra_data | Fit exponential decay to price deviation from pre-trade trend after large trades; measure time to return within 1 spread of pre-trade mid. | Resiliency requires observing the post-trade price path and the order book replenishment process; impossible with OHLCV. |
| inventory risk | Inventory risk = risk that price changes before dealer can unload unwanted inventory position | inventory position deviation from target; quote revision frequency; quote skew (bid/ask adjustment) | dealer inventory snapshots + quote history + position data | needs_extra_data | Regress quote mid change on inventory deviation; inventory risk component of spread = inventory_cost × expected_holding_period. | Inventory data is proprietary to dealers; public data only allows indirect inference via quote dynamics. |
| adverse selection | Adverse selection = risk that counterparty knows more than dealer; dealers lose to informed traders on average | effective spread minus realized spread; post-trade price drift; VPIN (volume-synchronized probability of informed trading) | tick-by-tick trade + quote data + post-trade price; for VPIN: bucketed volume + buy/sell volume classification | needs_extra_data | Standard decomposition: adverse selection cost = effective_spread - realized_spread; compute using trade-by-trade data with 5-30 min post-trade mid. | VPIN requires classifying trade direction (buy/sell) in volume buckets; needs tick data or accurate trade-direction algorithm. |
| price impact | Price impact = change in price resulting from a trade; has temporary (liquidity) and permanent (information) components | temporary impact = effective_spread/2; permanent impact = price change from pre-trade to T+30min mid; total impact = temporary + permanent | tick-by-tick trade data (price, direction, size) + quote data (pre-trade mid) + post-trade price trajectory | needs_extra_data | For each trade: temporary_impact = |trade_price - pre_trade_mid|; permanent_impact = |post_trade_mid - pre_trade_mid|; total_impact = |trade_price - post_trade_mid|. | Price impact requires observing the trade price, the pre-trade mid, and the post-trade mid; impossible with OHLCV. |
| execution cost / transaction cost | Execution cost = spread + commission + price impact; Transaction cost = execution cost + opportunity cost of failing to trade | effective spread + commission rate + market impact; implementation shortfall = (execution_price - benchmark_price) / benchmark_price | trade data + quote data at entry time + commission schedule + benchmark price (arrival price, VWAP, closing price) | needs_extra_data | Implementation shortfall = (fill_price - arrival_price)/arrival_price × fill_rate + opportunity_cost × (1 - fill_rate); requires order entry timestamp and arrival price. | Execution cost measurement requires knowing the order submission price/time and the benchmark; not available in OHLCV. |
| market quality | Market quality = extent to which market satisfies trader needs; dimensions: liquidity, price discovery, fairness, transparency, low cost | multi-metric dashboard: liquidity metrics + price discovery metrics + cost metrics + volatility metrics (no single scalar) | multi-source data: spread/depth/resiliency + price discovery metrics + transaction cost metrics + market structure data | needs_extra_data | Build a dashboard-style multi-metric view; normalize each metric separately; avoid collapsing into one weighted scalar. | Market quality is a meta-concept; no single observable proxy exists. Requires stitching multiple microstructure metrics. |
| price discovery | Price discovery = process by which markets determine security prices; informed traders cause prices to move toward fundamental value | price deviation from fundamental value; speed of price adjustment after news; variance ratio (random walk test); return predictability after events | high-frequency price data + news timestamps + fundamental value proxies (analyst consensus, NAV, futures price) | needs_extra_data | Event study: measure price drift and convergence speed after news; variance ratio test: compare short-horizon to long-horizon return variance; information share model for multi-market price discovery. | Price discovery requires a benchmark for fundamental value, which is never directly observable; must be proxied. |
| manipulation | Manipulation = trading or placing orders to deceive others about demand/supply, or to move prices for profit | order cancellation rate; trade-to-order ratio; volume-synchronized price patterns; account concentration; spoofing detection | order-level audit trail (add/modify/cancel with account IDs) + trade data + position data + account linkage graph | needs_extra_data | Spoofing detection: flag accounts with high cancellation rate (>90%) and large order-to-trade ratio; layering detection: analyze order book depth manipulation patterns. | Manipulation detection requires order-level message data with account identifiers; impossible with anonymous trade tape. |
| regulation | Regulation = rules and oversight governing trading to ensure fair, orderly, and transparent markets | regulatory event dummy variables (circuit breaker activation, short-sale ban, tick-size change); market structure change dates | regulatory filing data, rule change announcements, circuit breaker trigger logs, tick-size pilot data | shell_only | Use difference-in-differences or event-study framework to measure causal effect of regulatory changes on liquidity, volatility, or price discovery; regulation itself is not a tradable variable but a structural shock. | Regulation is a categorical/policy variable; quantifiable only as a treatment in causal inference, not as a continuous market signal. |
| auction | Auction = market mechanism where traders submit bids/offers and trades are arranged by pricing rule; call vs. continuous | clearing price; volume at clearing; order imbalance pre-clearing; indicative price path during call phase | call auction order data (indicative prices, uncrossing volume, order book at clearing) + continuous auction trade data | needs_extra_data | For call auctions: model supply/demand curves from order book; predict clearing price as intersection; measure order imbalance and its correlation with post-open price drift. | Auction mechanics require order book data during the auction phase; indicative prices and order imbalances are often not publicly disseminated in full detail. |
| continuous trading | Continuous trading = trading session where traders can attempt to trade whenever market is open; trades occur sequentially | trade arrival rate; inter-trade duration; order book update frequency; price path continuity; queue position dynamics | tick-by-tick trade and order book data with millisecond timestamps; queue position data; event rate metrics | needs_extra_data | Model trade arrival as a point process (e.g., Hawkes process) with self-excitation; measure order book imbalance and its predictive power for next trade direction. | Continuous trading quantification requires high-frequency event data; OHLCV collapses all intraday activity into four points. |
| call auction | Call auction = trading session where all traders trade at same time and single price when market is called; orders batched | uncrossing volume; clearing price deviation from previous close; order imbalance; pre-open price discovery accuracy | call auction parameters (indicative price, volume, imbalance, final price) + pre-auction order book + post-auction trades | needs_extra_data | Measure price discovery efficiency at open/close as |clearing_price - fundamental_value_proxy|; compare call auction volatility to continuous session volatility. | Call auction data requires exchange-specific auction feeds; many consolidated feeds do not include indicative auction data. |
| volatility | Volatility = rate at which prices change; measure of uncertainty about security value; high when traders disagree or information arrives fast | realized variance (sum of squared returns); GARCH conditional volatility; implied volatility from options; intraday range (high-low) | OHLCV for realized variance and range; options data for implied volatility; high-frequency returns for realized variance | proxy_quantizable_now | Realized variance can be computed from OHLCV (lower frequency) or tick data (higher accuracy); intraday range is a robust volatility proxy when tick data is unavailable; GARCH/EGARCH models fit on daily returns. | Volatility is one of the few concepts in this book that can be adequately proxied with OHLCV alone, though tick data improves precision. |
| information asymmetry | Information asymmetry = some traders know more about value than others; source of adverse selection and spread | VPIN; PIN; probability of informed trading; earnings surprise dispersion; analyst forecast dispersion; insider trading intensity | volume bucket data + trade direction classification (buy/sell) for VPIN; option volume for PIN; earnings/news data for event-based measures | needs_extra_data | VPIN = standard deviation of volume-bucket trade imbalance over rolling window; requires classifying each trade as buyer-initiated or seller-initiated using tick rule or Lee-Ready algorithm. | Information asymmetry is latent; all proxies (VPIN, PIN, spread decomposition) require assumptions about trade direction or information event timing. |
| trade size | Trade size = number of units traded in a transaction; large trades have greater price impact due to liquidity exhaustion | trade size distribution; average trade size; block trade flags; participation rate; volume profile by price level | trade data with size field; block trade thresholds (e.g., 10,000 shares); volume-at-price (volume profile) from order book | needs_extra_data | Measure Kyle's lambda (price impact per unit volume) via regression: Δprice = λ × volume + noise; requires tick data with trade size and direction; block trades require upstairs market negotiation data. | Trade size is observable in tick data, but its impact on price depends on contemporaneous market depth, which is not in trade tape alone. |

## FORMULAS_AND_ALGOS
- **Quoted Spread**
  - Formula: `Quoted_Spread = Ask_Price - Bid_Price`
  - Relative: `Relative_Spread = (Ask_Price - Bid_Price) / Mid_Price`
  - Source: Ch 14; proxy: can approximate from intraday high/low or quote snapshots.

- **Effective Spread**
  - Formula: `Effective_Spread = 2 × |Trade_Price - Mid_Price_at_Trade_Time|`
  - For buyer-initiated: `2 × (Trade_Price - Mid_Price)`; for seller-initiated: `2 × (Mid_Price - Trade_Price)`
  - Source: Ch 21; proxy: requires trade price and contemporaneous quote midpoint.

- **Realized Spread**
  - Formula: `Realized_Spread = 2 × |Trade_Price - Mid_Price_at_T+Δt|`
  - Common Δt = 5 minutes or 30 minutes; proxy for dealer gross profit.
  - Source: Ch 21; proxy: requires post-trade price data.

- **Adverse Selection Component of Spread**
  - Formula: `Adverse_Selection_Cost = Effective_Spread - Realized_Spread`
  - Interpretation: if positive, dealers lose to informed traders on average and uninformed traders pay via spread.
  - Source: Ch 14; proxy: requires both effective and realized spread data.

- **Implementation Shortfall (Perold)**
  - Formula: `IS = (Execution_Price - Arrival_Price) / Arrival_Price × Fill_Rate + Opportunity_Cost × (1 - Fill_Rate)`
  - Arrival price = mid at order submission time; opportunity cost = missed price movement.
  - Source: Ch 22 (implied); proxy: requires order submission timestamp and benchmark price.

- **Amihud Illiquidity Ratio**
  - Formula: `Amihud = |Daily_Return| / (Dollar_Volume)`
  - Daily proxy using OHLCV; measures price impact per dollar of volume.
  - Source: Ch 19/21 (implied); proxy: **proxy_quantizable_now** with daily data but very noisy.

- **Kyle's Lambda (Price Impact Coefficient)**
  - Formula: `ΔP = λ × Q + ε`, where Q = signed trade size (positive for buy, negative for sell)
  - Estimation: OLS regression of price change on signed order flow over short intervals.
  - Source: Kyle (1985) referenced implicitly; proxy: requires tick data with trade direction and size.

- **Liquidity Dimensions Composite (Approximation, Non-scalar)**
  - Formula: `L ≈ 1 / Spread × Depth × Resiliency_Speed` (conceptual, not from text)
  - Harris defines three dimensions but does not provide a closed-form scalar aggregation.
  - Status: **proxy/approximation** — any single-number aggregation is normative and must be user-defined, not a direct formula from text.

## NOT_QUANT_YET
1. **Resiliency as a scalar metric**: Harris defines resiliency as recovery speed after a shock, but does not specify the exact measurement window or the recovery benchmark. Different shocks (large trade vs. news event) have different recovery dynamics. Need a standardized event definition and a half-life estimation method.
2. **Dealer inventory risk without dealer data**: The inventory risk component of the spread depends on the dealer's actual inventory position, which is proprietary. Public data only allows indirect inference via quote skew, but quote skew can also reflect adverse selection. Disentangling the two requires dealer-level data or structural assumptions.
3. **Information asymmetry magnitude**: Harris describes information asymmetry as the source of adverse selection, but provides no operational formula for its magnitude. PIN and VPIN are later models (Easley et al., 2012) that require strong distributional assumptions and are not directly derived from this text. Need a validated proxy for private information arrival rate.
4. **Hybrid market fragmentation**: Hybrid markets combine order-driven, quote-driven, and brokered mechanisms. Quantifying the relative contribution of each mechanism to a single trade requires venue-level tagging and order-type classification that is often not available in consolidated tapes. Need a multi-venue data merge with mechanism labels.
5. **Market quality dashboard (non-scalar)**: Harris defines market quality as a multidimensional concept (liquidity, fairness, efficiency, transparency) but does not provide a weighting scheme or aggregation formula. Any single-number aggregation is normative and requires practitioner/regulatory judgment on dimension weights.
6. **Price discovery speed vs. accuracy**: The text distinguishes price discovery as a process but does not separate speed (how fast prices react) from accuracy (how close prices are to fundamental value). Fundamental value is unobservable, so accuracy requires a proxy (e.g., post-earnings consensus), introducing model risk.
7. **Manipulation detection at scale**: Harris describes manipulation types (bluffing, spoofing, wash trading) but does not provide a statistical detection algorithm. Operational detection requires order-level audit trails with account identifiers, which are not publicly available. Regulatory surveillance systems have proprietary rules.
8. **Stop order cascade dynamics**: Stop orders are dormant until triggered; their clustering and cascade effects are highly nonlinear. Without access to broker order books or stop order placement data, their effect can only be inferred ex-post from price gaps and volume spikes, which have multiple causes.
9. **Call auction price formation**: Harris describes call auctions but does not model the supply/demand curve intersection or the effect of order imbalance on clearing price. Continuous-time order book modeling does not directly apply to batch auctions. Need auction-specific order data and a discrete clearing model.
10. **Broker best execution quality**: Best execution is a legal standard, not a numerical metric. Harris discusses broker duties but does not provide a formula for best execution measurement. Implementation shortfall is the closest proxy, but it requires knowing the order arrival price and the broker's routing decision timing, which is often private.
11. **Regulatory impact causal identification**: Regulations (circuit breakers, short-sale bans, tick-size changes) are policy shocks. Identifying their causal effect on market quality requires an exogenous variation design (e.g., regression discontinuity, difference-in-differences) and a valid control group, not just a time-series correlation.
12. **Trade size impact with iceberg orders**: Large orders may be split into iceberg slices, making observed trade size a biased measure of true intent. Without iceberg detection (which requires order-level data showing repeated same-size orders at same price), trade-size-based impact models underestimate true size.

## NEXT_ACTION
1. **Acquire tick/Level-2 data for at least one equity market** (e.g., A-share tick data or US equities via Polygon/IEX) to begin measuring effective spread, realized spread, and adverse selection component as defined in Ch 14/21.
2. **Build a trade-direction classifier** (Lee-Ready or tick rule) for tick data so that signed order flow can be used for Kyle's lambda estimation and VPIN computation.
3. **Construct an order-book snapshot parser** that reconstructs bid/ask depth at multiple levels from Level-2 data, enabling direct measurement of depth, depth asymmetry, and resiliency.
4. **Map venue MIC codes to market structure categories** (order-driven/quote-driven/hybrid/auction) to create a structural reference table that can be joined with execution data.
5. **Implement an effective-vs-realized spread decomposition pipeline** for a sample of stocks, computing the adverse selection component and inventory cost component at daily or weekly frequency.
6. **Collect earnings announcement calendars and news timestamps** to conduct event studies measuring price discovery speed and information asymmetry spikes around corporate events.
7. **Build a stop-cluster detection module** that identifies price levels with thin depth and high historical trade concentration, as proxy locations for dormant stop orders.
8. **Develop a call auction phase analyzer** for open/close auction data (indicative prices, uncrossing volume, imbalance) to model clearing price prediction and post-open drift.
9. **Create a broker routing quality dashboard** using 605/606 execution quality reports to map broker routing behavior and venue-level fill rates.
10. **Design a manipulation-pattern scanner** for order-level data (if available) that flags high cancellation rates, trade-to-order ratio anomalies, and layering patterns consistent with spoofing.
11. **Build a dealer inventory proxy model** using quote skew and quote revision dynamics as observable proxies for inventory position, validated against any available dealer transaction data.
12. **Integrate the objects from this book into a unified microstructure schema** that links participants, orders, market structures, liquidity dimensions, and transaction costs into a queryable knowledge graph for downstream A2/F1 use.

