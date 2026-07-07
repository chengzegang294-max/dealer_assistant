# A2_CUT__Larry_Harris__Trading_and_Exchanges

## 1. MATERIAL_CARD

| 字段 | 内容 |
|------|------|
| **title** | Trading and Exchanges: Market Microstructure for Practitioners |
| **author** | Larry Harris |
| **publisher** | Oxford University Press (2003) |
| **language** | English |
| **pages** | 657 |
| **A2_relevance** | Market microstructure bible; order-driven vs. quote-driven, auction mechanisms, limit order book, liquidity, price discovery, trading costs |
| **contract_used** | CUT_CONTRACT__Kimi_保留型切割_v2 |
| **source_file** | Trading and Exchanges (Larry Harris).pdf |
| **cut_date** | 2025-06-16 |
| **quantizable_now** | order book depth proxy, bid-ask spread, pricing rules, auction surplus, trader surplus, transaction cost decomposition, volatility impact |
| **needs_extra_data** | real-time order book (full depth), dealer inventory, specialist profit, block trade mechanics, exchange-specific rules |
| **a_share_alignment** | A股集合竞价机制（call auction）、连续竞价（continuous auction）、限价订单簿（LOB）、流动性供给、交易成本 |

---

## 2. ROUTING_DECISION

| 决策 | 判定 |
|------|------|
| **保留策略** | 保留拍卖机制、订单簿结构、定价规则、流动性分析；压缩交易所历史/监管细节 |
| **language** | 英文原文保留；专业术语附中文译名 |
| **quantization_path** | `proxy_quantizable_now` for auction mechanics, spread analysis, transaction cost; `future_bucket` for real-time LOB dynamics, dealer behavior |
| **output_form** | RETAINED_EXCERPTS (16+) + FORMULAS_AND_ALGOS + QUANTIZATION_TABLE |
| **A_share_action** | A股集合竞价 = call auction; 连续竞价 = continuous discriminatory auction; 限价订单簿 = LOB; 涨跌停 = price limits + volatility interruption |

---

## 3. CONTENT_CLUSTERS

### Cluster A: Introduction to Trading (Ch.1-2)
- **Trading**: exchanging assets for money or other assets
- **Liquidity**: the ease of trading; supplied by dealers, limit order traders, speculators
- **Market Structure**: rules governing trading; price discovery, liquidity, transaction costs
- **Three Dimensions**: price, time, quantity

### Cluster B: The Trading Industry (Ch.3)
- **Brokers**: agents for traders; arrange trades for commissions
- **Dealers**: principals; trade for their own accounts; provide liquidity
- **Exchanges**: marketplaces; set rules; match orders
- **Specialists / Market Makers**: hybrid broker-dealer roles on exchanges

### Cluster C: Orders and Order Properties (Ch.4)
- **Market Orders**: buy/sell at best available price; demand liquidity
- **Limit Orders**: buy/sell at specified price or better; supply liquidity
- **Stop Orders**: become market orders when price reaches trigger; stop-loss, stop-entry
- **Order Properties**: side, size, price limit, time in force, display options, stop trigger

### Cluster D: Market Structures (Ch.5-6)
- **Call Auction (集合竞价)**: orders accumulate; single clearing price; maximizes total surplus
- **Continuous Auction (连续竞价)**: orders match immediately; discriminatory pricing rule
- **Order-Driven Markets**: traders provide liquidity via limit orders
- **Quote-Driven Markets**: dealers provide liquidity via quotes
- **Hybrid Markets**: combination of order-driven and quote-driven elements
- **Discriminatory Pricing Rule**: trades at different prices based on order precedence
- **Uniform Pricing Rule**: all trades at same price (call auction)

### Cluster E: Brokers, Dealers, and Their Clients (Ch.7-8)
- **Brokerage Services**: order routing, custody, margin, research
- **Dealer Markets**: over-the-counter (OTC); NASDAQ; interdealer brokers
- **Liquidity Suppliers**: who provides it, why, and how they profit
- **Bid-Ask Spread**: compensation for liquidity provision; inventory costs, adverse selection, order processing

### Cluster F: Price Discovery (Ch.10-11)
- **Price Discovery**: process of finding market-clearing price
- **Auctions**: single-price auctions, continuous two-sided auctions, Dutch, English, sealed bid
- **Trader Surplus**: difference between trade price and trader's value
- **Total Surplus**: sum of all buyer and seller surpluses; maximized in call auction
- **Price Efficiency**: prices reflect all available information

### Cluster G: Volatility and Trading Halts (Ch.18)
- **Volatility**: price variation; caused by information flow, trading activity, market structure
- **Trading Halts**: pauses in trading; circuit breakers; price limits
- **Volatility Interruption**: temporary halt to allow information dissemination
- **Price Limits**: maximum daily price movement; can cause liquidity disruption

### Cluster H: Transaction Costs (Ch.19)
- **Transaction Cost Components**: commissions, bid-ask spread, price impact, opportunity cost, delay cost
- **Implementation Shortfall**: difference between decision price and execution price
- **Price Impact**: effect of trading on price; permanent and temporary components
- **Market Impact Models**: linear, square-root, logarithmic models

---

## 4. QUANTIZATION_TABLE

| # | 对象/概念 | 数据源需求 | 可量化标记 | A股近似方案 | 备注 |
|---|----------|-----------|-----------|-------------|------|
| 1 | **Call Auction (集合竞价)** | OHLCV + 集合竞价数据 | `proxy_quantizable_now` | A股 9:15-9:25 集合竞价 = 标准 call auction | 可用集合竞价成交量、匹配价、未成交量 |
| 2 | **Continuous Auction (连续竞价)** | OHLCV + 逐笔 | `proxy_quantizable_now` | A股 9:30-11:30, 13:00-14:57 连续竞价 | 标准连续竞价机制 |
| 3 | **Limit Order Book (LOB)** | Level2 / 逐笔委托 | `needs_extra_data` | A股 Level2 行情 = 10档订单簿 | 需付费终端获取完整数据 |
| 4 | **Bid-Ask Spread** | OHLCV 或 Level1 | `proxy_quantizable_now` | 买一/卖一价差 | 可用分钟K线近似或 Level1 |
| 5 | **Market Depth** | Level2 | `needs_extra_data` | A股 Level2 10档深度 | 需 Level2 数据 |
| 6 | **Discriminatory Pricing Rule** | 逐笔成交 | `proxy_quantizable_now` | 每笔成交按最优对手价撮合 | 所有连续竞价均使用此规则 |
| 7 | **Uniform Pricing Rule** | 集合竞价数据 | `proxy_quantizable_now` | 集合竞价单一成交价 | 标准 call auction 定价规则 |
| 8 | **Trader Surplus** | 逐笔 + 订单簿 | `needs_extra_data` | 难以直接获取；可用成交均价 vs. 决策价近似 | 需要投资者意图数据 |
| 9 | **Total Surplus Maximization** | 集合竞价数据 | `proxy_quantizable_now` | 集合竞价匹配量最大化 | 可用集合竞价匹配成交量衡量 |
| 10 | **Order Precedence** | 逐笔委托 | `needs_extra_data` | 价格优先、时间优先 | 交易所撮合规则已知 |
| 11 | **Price Impact (Permanent)** | OHLCV + 多日线 | `proxy_quantizable_now` | 大单后价格的长期偏移 | 可用事件研究法 |
| 12 | **Price Impact (Temporary)** | OHLCV + 分钟线 | `proxy_quantizable_now` | 大单后价格的短期冲击与恢复 | 分钟级事件研究 |
| 13 | **Implementation Shortfall** | 订单执行数据 | `needs_extra_data` | 需要交易记录（决策价 vs. 执行价） | 仅持仓/交易机构可用 |
| 14 | **Volatility / Trading Halt** | OHLCV | `proxy_quantizable_now` | A股涨跌停板 = 价格限制；盘中临时停牌 = trading halt | 标准规则已知 |
| 15 | **Circuit Breaker** | OHLCV | `proxy_quantizable_now` | A股无美式circuit breaker，但有涨跌停 | 可用日内波动率监控 |
| 16 | **Liquidity Supply/Demand** | Level2 + 逐笔 | `needs_extra_data` | 委托簿深度变化、大单主动/被动方向 | 需 Level2 |
| 17 | **Dealer Inventory** | 券商持仓数据 | `needs_extra_data` | 券商做市持仓（科创板/北交所） | 非公开数据 |
| 18 | **Block Trade Cross** | 大宗交易数据 | `proxy_quantizable_now` | A股大宗交易（盘后定价/协商） | 交易所每日披露 |
| 19 | **Adverse Selection Cost** | Level2 + 逐笔 | `needs_extra_data` | 被大单"穿透"后的价格反向运动 | 需订单簿深度变化 |
| 20 | **Order Flow Toxicity** | 逐笔 | `needs_extra_data` | VPIN (Volume-Synchronized Probability of Informed Trading) | 需逐笔数据计算 |
| 21 | **Stop Order Trigger** | OHLCV + 分钟线 | `proxy_quantizable_now` | 止损触发价 = 触发条件 | 可用分钟K线模拟 |
| 22 | **Time in Force Analysis** | 逐笔委托 | `needs_extra_data` | 订单有效期（IOC/FOK/GTD/GTC） | 需委托级别数据 |
| 23 | **Hidden Order Detection** | 逐笔 | `needs_extra_data** | 冰山订单/隐藏订单 | 需 Level2 逐笔还原 |
| 24 | **Exchange Market Share** | 交易统计 | `proxy_quantizable_now` | 上交所/深交所/北交所成交量占比 | 公开数据 |
| 25 | **Transaction Cost Decomposition** | 交易记录 | `needs_extra_data** | 佣金 + 冲击成本 + 延迟成本 + 机会成本 | 需内部交易数据 |

---

## 5. RETAINED_EXCERPTS

### Excerpt 1: Trading and Liquidity Definition
> "Trading is the process of exchanging assets for money or other assets. Liquidity is the ease of trading. Liquid markets are markets in which traders can quickly buy or sell significant quantities of assets with small transaction costs and little price impact. Liquidity is supplied by dealers, limit order traders, and speculators."

### Excerpt 2: Market Structure Definition
> "Market structure is the set of rules that govern trading. These rules determine who can trade, what can be traded, when trading can occur, where trading takes place, and how prices are determined. The rules affect price discovery, liquidity, and transaction costs."

### Excerpt 3: Order-Driven vs. Quote-Driven
> "Order-driven markets are markets in which traders provide liquidity by submitting limit orders. Quote-driven markets are markets in which dealers provide liquidity by quoting bid and ask prices. Most modern markets are hybrids that combine elements of both order-driven and quote-driven structures."

### Excerpt 4: Call Auction Mechanism
> "In a call auction, orders accumulate until the market calls all orders to trade at a single clearing price. The clearing price is the price that maximizes the total volume traded or the total surplus generated by trading. Call auctions are commonly used to open and close trading sessions and to trade securities that are illiquid."

### Excerpt 5: Continuous Auction and Order Book
> "Continuous auction markets maintain an order book to keep track of standing orders that are waiting to fill. The buy and sell orders are separately sorted by their precedence. The highest-priced bid and the lowest-priced offer are the best bid and the best offer. When a new order arrives, the matching system attempts to arrange a trade between the new order and the order on the opposite side with the highest precedence."

### Excerpt 6: Discriminatory vs. Uniform Pricing
> "Continuous rule-based order matching systems use the discriminatory pricing rule to price their trades. The rule is the same discriminatory pricing rule that oral auctions use. Under the discriminatory pricing rule, large impatient traders prefer to trade because it allows them to trade the first parts of their orders at better prices than the last parts. Under the uniform pricing rule, their entire orders would trade at the same price."

### Excerpt 7: Trader Surplus in Auctions
> "The single price auction maximizes the gains from trading. For a given order flow, no other method of arranging trades can produce a higher total trader surplus than that produced in a single price auction. A comparison of the results from the single price auction example with those from the continuous two-sided auction example confirms that the continuous auction produces a smaller trader surplus when processing the same order flow."

### Excerpt 8: Limit Order Book Structure
> "The limit order book contains all standing limit orders that have not yet been filled. The book is organized by price, with the highest bid and lowest offer displayed at the top. Depth at each price level indicates how many shares are available. The spread between the best bid and best offer is the bid-ask spread."

### Excerpt 9: Bid-Ask Spread Components
> "The bid-ask spread compensates dealers and liquidity suppliers for three costs: order processing costs, inventory holding costs, and adverse selection costs. Order processing costs are the direct costs of doing business. Inventory holding costs arise from the risk of holding positions. Adverse selection costs arise when traders on the other side have better information."

### Excerpt 10: Price Discovery Process
> "Price discovery is the process by which markets determine the prices of assets. In order-driven markets, price discovery occurs through the interaction of buy and sell orders in the limit order book. In quote-driven markets, dealers set prices based on their inventory positions and their expectations about future order flow. In both cases, the discovered price should reflect all available information about the asset's value."

### Excerpt 11: Trading Halts and Price Limits
> "Trading halts are temporary pauses in trading. They are called to allow markets to absorb new information, to prevent panic selling, or to correct order imbalances. Price limits are maximum daily price movements. When a price limit is reached, trading may halt or continue at the limit price. Price limits can cause liquidity disruptions when they prevent prices from reaching market-clearing levels."

### Excerpt 12: Transaction Cost Components
> "Transaction costs consist of commissions, bid-ask spread, price impact, opportunity cost, and delay cost. The bid-ask spread is the cost of trading immediately. Price impact is the effect of your trading on the price. Opportunity cost is the cost of failing to complete a trade. Delay cost is the cost of waiting for a better price."

### Excerpt 13: Implementation Shortfall
> "Implementation shortfall is the difference between the decision price and the final execution price, including all costs. It is the most comprehensive measure of transaction costs because it captures all components: explicit costs (commissions, fees) and implicit costs (spread, impact, delay, opportunity)."

### Excerpt 14: Market Impact Models
> "Market impact can be modeled as a function of order size relative to average daily volume. Common models include: linear impact (impact proportional to order size), square-root impact (impact proportional to square root of order size), and logarithmic impact. The square-root model is most commonly supported by empirical evidence."

### Excerpt 15: Volatility and Market Structure
> "Volatility is the variation of prices over time. It is caused by the arrival of new information, the trading process itself, and the structure of the market. Market structure can affect volatility through the rules governing price changes, the presence of circuit breakers, and the availability of liquidity."

### Excerpt 16: Stop Orders and Market Stability
> "Stop orders are orders that become market orders when the price reaches a specified trigger level. Stop-loss orders are designed to limit losses. However, when many stop orders are triggered simultaneously, they can accelerate price movements and cause cascades. This is why some markets have rules about the placement of stop orders."

### Excerpt 17: Dealer Market Making
> "Dealers profit from trading by buying at the bid and selling at the ask. Their inventory positions fluctuate based on the order flow they receive. When inventories become too large, dealers may adjust their quotes to encourage trades that reduce their positions. This inventory management behavior affects the bid-ask spread and market liquidity."

### Excerpt 18: Order Flow and Information
> "Order flow is informative. The sequence of buy and sell orders reveals information about the asset's value. Informed traders submit orders that move prices toward the true value. Uninformed traders submit orders that provide liquidity but may suffer from adverse selection. The mix of informed and uninformed order flow determines the efficiency of price discovery."

---

## 6. FORMULAS_AND_ALGOS

### Algorithm 1: Call Auction Clearing Price
INPUT: bid_orders = [(price, quantity)], ask_orders = [(price, quantity)]

1. Sort bids descending by price
2. Sort asks ascending by price
3. For each candidate price P (from unique prices in bids and asks):
   total_demand = sum(qty for price, qty in bids where price >= P)
   total_supply = sum(qty for price, qty in asks where price <= P)
   matched_volume = min(total_demand, total_supply)
4. Select P* that maximizes matched_volume
   (If tie, select price that minimizes surplus imbalance)
5. RETURN P* as clearing price, matched_volume
**A股 Proxy**: A股集合竞价机制与此完全一致；可用集合竞价数据验证。

### Algorithm 2: Bid-Ask Spread Decomposition
INPUT: bid, ask, trade_prices, trade_volumes, time_series

spread = ask - bid

# 1. Order Processing Component (fixed)
proc_cost = estimated_fixed_cost_per_trade

# 2. Inventory Holding Component (related to volatility)
inv_cost = 0.5 * price * volatility * sqrt(time_to_liquidate)

# 3. Adverse Selection Component (residual)
# Estimate via price reversal after trades
price_change_after_trade = mid_price_t+1 - mid_price_t
adverse_selection = covariance(price_change_after_trade, trade_direction)

adverse_cost = spread - proc_cost - inv_cost
# Or via regression: spread = alpha + beta1*volatility + beta2*inverse_volume + epsilon
**A股 Proxy**: 可用 Level1/Level2 数据计算 spread 及其时间序列变化。

### Algorithm 3: Transaction Cost Decomposition (Implementation Shortfall)
INPUT: decision_price, execution_price, execution_quantity, 
       commissions, fees, total_order_quantity, market_prices_during_execution

# 1. Explicit Costs
explicit = commissions + fees

# 2. Spread Cost (if market order)
spread_cost = execution_price - mid_price_at_execution

# 3. Price Impact (temporary + permanent)
temporary_impact = execution_price - mid_price_after_execution
permanent_impact = mid_price_after_execution - decision_price

# 4. Delay Cost
delay_cost = decision_price - mid_price_at_start_of_execution

# 5. Opportunity Cost (unfilled portion)
opportunity_cost = (mid_price_at_end - decision_price) * (total_order_quantity - execution_quantity)

total_shortfall = execution_price - decision_price + explicit
# Or decomposed: total = delay + spread + temp_impact + perm_impact + opportunity + explicit
**A股 Proxy**: 需要交易记录；对于市场分析，可用事件研究法近似。

### Algorithm 4: Market Impact Model (Square-Root)
INPUT: order_size, avg_daily_volume, daily_volatility, price

# Almgren-Chriss / square-root model
impact_ratio = order_size / avg_daily_volume

temporary_impact = gamma * daily_volatility * sqrt(impact_ratio) * price
permanent_impact = delta * daily_volatility * impact_ratio * price

# Gamma, delta are market-specific constants (typically gamma ~ 0.5, delta ~ 0.1-0.3)

expected_execution_price = arrival_price + permanent_impact * 0.5 + temporary_impact
**A股 Proxy**: 可用A股历史数据校准 gamma/delta；对大单/机构交易分析有用。

### Algorithm 5: Liquidity Metric (Order Book Based)
INPUT: order_book = [(price, bid_qty, ask_qty)], current_price

# 1. Depth within 1% of mid-price
depth_1pct = sum(bid_qty for price in bids where price >= mid*0.99) + 
             sum(ask_qty for price in asks where price <= mid*1.01)

# 2. Spread tightness
spread_pct = (ask - bid) / mid_price

# 3. Depth imbalance
imbalance = (total_bid_volume - total_ask_volume) / (total_bid_volume + total_ask_volume)

# 4. Composite Liquidity View
liquidity_score = (depth_1pct / avg_depth) * 0.4 + 
                  (1 / spread_pct) * 0.3 + 
                  (1 - abs(imbalance)) * 0.3
**A股 Proxy**: 需 Level2 数据；可用 Level1 近似（买一卖一深度）。

### Algorithm 6: Price Limit Hit Detection (A-Share Style)
INPUT: daily_ohlc, prev_close, limit_pct=0.10 (or 0.20 for ST/STAR)

upper_limit = prev_close * (1 + limit_pct)
lower_limit = prev_close * (1 - limit_pct)

IF high >= upper_limit * 0.999:
    hit_upper_limit = True
    # Check if locked (no trades below limit)
    locked_upper = (low >= upper_limit * 0.999) and (volume < avg_volume * 0.5)
ELIF low <= lower_limit * 1.001:
    hit_lower_limit = True
    locked_lower = (high <= lower_limit * 1.001) and (volume < avg_volume * 0.5)

# Liquidity disruption indicator
liquidity_disrupted = locked_upper OR locked_lower
**A股 Proxy**: 直接适用A股涨跌停制度。

---

## 7. NOT_QUANT_YET

| 对象 | 原因 | 未来数据需求 |
|------|------|-------------|
| **Specialist profit and behavior** | 纽交所 specialist 已大量消亡；A股无直接对应 | 科创板/北交所做市商数据 |
| **Interdealer broker mechanics** | 银行间/券商间撮合机制 | 场外交易数据 |
| **Internalization (internal crossing)** | 券商内部撮合 | 券商内部数据 |
| **Payment for order flow** | 美国市场特有 | 不适用A股 |
| **Front-running detection** | 需订单流序列 | 逐笔委托+成交 |
| **Bluffing and market manipulation** | 需监管案例+订单分析 | 监管披露 + 逐笔数据 |
| **True real-time LOB reconstruction** | 需完整10档+隐藏订单 | Level2 + 逐笔委托 |
| **Dealer quote adjustment dynamics** | 需做市商实时报价调整 | 北交所/科创板做市商数据 |
| **Cross-border arbitrage microstructure** | 需多市场同步数据 | 港股通/沪伦通数据 |
| **Options market microstructure** | 需期权订单簿 | 50ETF/300ETF期权 Level2 |
| **True adverse selection cost per trade** | 需交易后价格走势 | 逐笔 + 高精度时间戳 |
| **VPIN (Order Flow Toxicity)** | 需逐笔方向分类 | 逐笔成交明细 |
| **Hidden / Iceberg Order Detection** | 需订单簿动态分析 | Level2 逐笔还原 |
| **Flash crash post-mortem analysis** | 需毫秒级数据 | 逐笔 + 委托簿 |
| **Regulatory impact assessment** | 需政策变化前后对比 | 监管事件窗口 |

---

## 8. NEXT_ACTION

### 可先做状态壳（proxy_quantizable_now）
1. **Call Auction Analyzer**: A股集合竞价（9:15-9:25）成交量、匹配价、未成交量、委托簿深度分析
2. **Continuous Auction Monitor**: 连续竞价阶段 spread、深度、成交量、波动率实时监控
3. **Bid-Ask Spread Tracker**: 日内 spread 变化追踪，标记 spread 扩大/缩小时段
4. **Price Limit Hit Detector**: 涨跌停触发检测 + 封板/打开判断 + 流动性中断标识
5. **Market Impact Estimator**: 基于 square-root 模型的冲击成本预估（需校准A股参数）
6. **Transaction Cost Decomposer**: 对已知交易记录进行成本分解（如可用模拟交易数据）
7. **Liquidity Metric Calculator**: 基于 Level1/Level2 的流动性多指标刻画（深度+spread+imbalance）
8. **Volatility Regime Classifier**: 日内波动率状态分类（高/中/低）+ 波动率中断检测
9. **Order Precedence Simulator**: 模拟价格优先、时间优先撮合规则的效果
10. **Auction Surplus Proxy**: 用集合竞价匹配成交量/委托量作为 surplus 最大化代理指标

### 先放 future bucket（needs_extra_data）
1. **Full LOB Reconstruction Engine**: 基于 Level2 逐笔委托的完整订单簿重建
2. **Order Flow Toxicity (VPIN) Calculator**: 逐笔数据驱动的知情交易概率
3. **Adverse Selection Cost Per Trade**: 逐笔级别逆向选择成本计量
4. **Hidden Order Detection System**: 冰山订单/隐藏订单识别
5. **Dealer/Market Maker Inventory Tracker**: 做市商库存动态跟踪（科创板/北交所）
6. **Cross-Market Microstructure Linkage**: 现货-期货-ETF 跨市场微观结构联动
7. **Real-Time Manipulation Detection**: 基于订单簿模式的异常检测（幌骗、Layering等）

### 适合和 A股集合竞价/开盘结构对齐的对象
1. **Call Auction ↔ A股 9:15-9:25 集合竞价**: 直接对应；可分析集合竞价成交量、匹配价、未成交量、虚拟匹配参考价变化
2. **Continuous Auction ↔ A股 9:30-11:30, 13:00-14:57**: 直接对应；A股收盘前3分钟（14:57-15:00）也是集合竞价，需注意区分
3. **Opening Price Discovery ↔ A股开盘价形成**: 集合竞价是A股开盘价形成机制；可用 Harris 理论分析开盘价质量
4. **Price Limits ↔ A股涨跌停板**: 10%（20% for ST/STAR）价格限制；Harris 理论中 price limit 的 liquidity disruption 分析直接适用
5. **Trading Halt ↔ A股盘中临时停牌**: 波动率异常或重大信息披露时停牌；可用 Harris 理论分析 halt 的效果
6. **Order Book Depth ↔ A股 Level2 十档行情**: A股 Level2 提供买卖十档深度；可用 Harris 的 depth/liquidity 框架分析
7. **Discriminatory Pricing ↔ A股连续竞价撮合**: 所有连续竞价均采用价格优先+时间优先的歧视性定价；Harris 理论直接适用
8. **Uniform Pricing ↔ A股集合竞价撮合**: 集合竞价单一成交价；Harris 的 call auction surplus 最大化分析直接适用
9. **Market Impact in A-Share ↔ A股大单冲击**: A股机构大单冲击成本可用 Harris 的 square-root 模型预估；需用A股数据校准
10. **Stop Order Cascade ↔ A股止损触发与闪崩**: Harris 提到的 stop order cascade 风险在A股同样存在；可用日内波动率监测预警
11. **Broker Routing ↔ A股券商订单路由**: A股投资者通过券商下单至交易所；Harris 的 broker function 分析适用
12. **Information Arrival ↔ A股信息披露与开盘跳空**: A股非交易时间信息披露导致集合竞价跳空；Harris 的信息到达与 price discovery 分析直接适用

---

*End of CUT for Trading and Exchanges*


