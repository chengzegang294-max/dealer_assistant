### MATERIAL_CARD
- title: Successful Algorithmic Trading
- author_or_source: Michael L. Halls-Moore
- material_type: 书 / 课程讲义
- domain_tags: [算法交易, Python 回测, 数据管理, 执行系统, 风险管理, 策略开发]
- file_scope: 全书 303 页（Chapter 1-8）

### ROUTING_DECISION
- current_repo_role: DATA_ENGINEERING_GUARD
- is_worth_deep_cut_now: yes
- deep_cut_priority: P1
- reason: 本书是零售量化交易的技术实施手册，覆盖数据存储、清洗、回测、执行全栈。大量内容直接对应 data engineering 与 execution guard，是基础设施层切割的重点素材。

### CONTENT_CLUSTERS
- cluster_name: 算法交易概述
  what_it_is: 定义、优势（历史评估、效率、纪律、统计一致性）、劣势（技术风险、市场变化）。
  keep_level: 中
  repo_mapping: source_library_only
- cluster_name: 数据管理
  what_it_is: Securities Master Database 设计：股票、期权、外汇、期货、债券、衍生品数据统一存储。数据获取、清洗、存储、导出。
  keep_level: 高
  repo_mapping: data_engineering_guard
- cluster_name: 回测系统
  what_it_is: 回测定义、目的、偏差（幸存者偏差、前视偏差、优化偏差）、交易成本建模、性能评估。
  keep_level: 高
  repo_mapping: data_engineering_guard
- cluster_name: 策略实现
  what_it_is: Backtesting 平台选择（TradeStation/MT4/Python/R/C++）、执行能力、Broker 交互、自主控制 vs 外包。
  keep_level: 中
  repo_mapping: state_template_shell
- cluster_name: 策略发现
  what_it_is: 个人偏好、时间约束、频率选择（日内/日终）、数据需求、预算、编程技能、评估标准。
  keep_level: 低
  repo_mapping: source_library_only
- cluster_name: 执行系统
  what_it_is: 自动执行、减少人为干预、sniping 策略、VWAP 执行、与券商 API 交互。
  keep_level: 中
  repo_mapping: state_template_shell
- cluster_name: 风险管理
  what_it_is: Alpha 模型、风险过滤、组合构建、下单、执行监控。心理建设与干预风险。
  keep_level: 中
  repo_mapping: data_engineering_guard
- cluster_name: 高级数据处理
  what_it_is: 市场分类、数据频率（tick/order book）、数据源（免费/商业）、数据清洗与准备。
  keep_level: 高
  repo_mapping: data_engineering_guard

### QUANTIZATION_TABLE
| concept | type | minimal_definition | observable_proxy | min_data_requirement | confirmation_timing | quant_status | repo_target | leakage_risk | notes |
|---|---|---|---|---|---|---|---|---|---|
| Securities Master Schema | object | 全公司统一的金融工具主数据库，存储基本面、价格、交易数据 | 表结构：instrument(symbol, asset_class, exchange), price(open,high,low,close,adj_close,volume), fundamental(eps,dividend) | PIT_fundamental | 每日收盘后更新 | proxy_quantizable_now | data_engineering_guard | low | A 股需处理复权因子、停牌标记、ST 标记、退市标记 |
| Data Cleansing Pipeline | feature | 处理错误价格、缺失值、异常跳点、重复记录的数据清洗流程 | 规则：价格 <= 0 标记为异常；volume = 0 但 price 变化 -> 前复权错误；相邻日收益率 > 50% 标记为跳点 | OHLCV | 每日收盘后 | proxy_quantizable_now | data_engineering_guard | low | A 股需特别处理涨停/跌停导致的一字板（价格不变但 volume 极小） |
| Backtest Equity Curve | state | 策略在历史数据上的权益累积曲线 | equity_t = equity_{t-1} * (1 + r_t)，其中 r_t 为第 t 笔交易收益率（含成本） | OHLCV/session_calendar | 每笔交易闭合后 | proxy_quantizable_now | state_template_shell | low | 必须区分 mark-to-market 与 realized PnL；未平仓头寸需按收盘价估值 |
| Survivorship Bias Ratio | risk_guard | 回测数据库中存活标的占比，衡量幸存者偏差严重程度 | bias_ratio = 当前成分股数 / 历史某一时刻实际可交易股数；越接近 1 偏差越小 | PIT_fundamental | 数据采购时 | proxy_quantizable_now | data_engineering_guard | med | A 股免费数据源（如 tushare pro）的成分股历史需额外购买 |
| Look-Ahead Bias Flag | risk_guard | 回测中使用了未来信息（如未来财报、未来成分股调整） | 审查信号公式中所有输入变量的时间戳；若任一变量的发布时间 > 信号生成时间，则 flag=1 | OHLCV/news_event | 回测开发阶段 | proxy_quantizable_now | data_engineering_guard | high | A 股财报发布日期与报告期末日期不一致，必须使用 publish_date |
| Transaction Cost Model | risk_guard | 将佣金、滑点、市场冲击纳入回测收益计算 | cost_t = commission + slippage + impact；commission = fill_price * volume * rate；slippage 按档位估计 | tick_trade | 回测阶段 | needs_extra_data | state_template_shell | med | A 股印花税为卖出方单边 0.05%，需单独建模 |
| Strategy Sniper Execution | execution_rule | 在特定条件触发时立即下单，不等待人工确认 | 条件：信号生成且风险检查通过 -> 立即发送限价/市价单到 Broker API；超时未确认则报警 | subjective_only | 实时 | shell_only | state_template_shell | high | 偏技术实现与 API 稳定性；不同券商 API 差异大，需抽象层 |
| VWAP Benchmark Cost | risk_guard | 策略成交均价与成交量加权平均价的偏差，衡量执行效率 | VWAP_cost = (avg_fill_price - VWAP) / VWAP * direction；正值表示劣于基准 | tick_trade | 收盘后 | needs_extra_data | state_template_shell | low | A 股可用 level1 分笔汇总近似 VWAP，但机构常用 level2 精确计算 |
| Paper Trading Divergence Alert | risk_guard | 纸面交易与回测的累计收益差异超过阈值时报警 | divergence = |cum_return_paper - cum_return_backtest| / MDD_backtest；若 > 0.3 则触发调查 | OHLCV/session_calendar | 每日收盘后 | proxy_quantizable_now | data_engineering_guard | med | 差异可能来自滑点、心理干预、市场冲击、数据延迟 |
| Alpha Model Signal | feature | 产生原始交易信号的数学模型或规则 | 信号强度 s_t in [-1, +1]，由因子加权或技术指标阈值产生；需经风险过滤后执行 | OHLCV/cross_section | 每日/实时 | proxy_quantizable_now | state_template_shell | low | A 股需考虑 T+1 与涨跌停对信号可执行性的影响 |
| Position Sizing Rule | execution_rule | 根据账户权益、风险限额与信号强度确定下单数量 | size = floor(equity * risk_per_trade / (ATR * price * lot_size))；或 Kelly 比例 | OHLCV | 信号生成后 | proxy_quantizable_now | state_template_shell | low | A 股最小下单 100 股（手），size 必须为整数手 |
| Drawdown Stop Rule | risk_guard | 当权益回撤超过预设阈值时强制减仓或停止交易 | 若 DD_t > max_allowed_dd（如 10%）-> 平掉所有仓位；若连续 N 日亏损 -> 暂停策略 | OHLCV/session_calendar | 实时/收盘 | proxy_quantizable_now | data_engineering_guard | low | A 股跌停时无法平仓；止损价可能无法触发 |
| Tick Data Storage | object | 逐笔成交与报价数据的存储结构 | 表：tick(symbol, timestamp, price, volume, bid, ask, bid_size, ask_size, exchange_code) | tick_trade/level2_orderbook | 实时接收 | needs_extra_data | data_engineering_guard | low | A 股 level2 数据量大，需压缩/分区存储；免费 tick 数据极少 |
| Order Book Imbalance Signal | feature | 买单深度与卖单深度之比，预测短期价格方向 | imbalance = (bid_volume_total - ask_volume_total) / (bid_volume_total + ask_volume_total) | level2_orderbook | 实时 | needs_extra_data | orderflow_future_bucket | high | A 股 level1 仅五档，level2 十档但需付费；十档之外信息缺失 |
| Seasonal/News Event Filter | filter | 在特定日历事件或新闻发布时过滤交易信号 | 事件标记：财报发布日、宏观数据发布日、长假前；若 event_t = 1 则信号强制为 0 | news_event/session_calendar | 每日开盘前 | proxy_quantizable_now | object_definition_shell | med | A 股需维护两会、国庆、春节、北向资金流动等事件日历 |

### RETAINED_EXCERPTS
- excerpt_id: EX-01
  source_hint: Chapter 1: Overview / Definition
  quote: >
    Chapter 1 Introduction to the Book 1.1 Introduction to QuantStart QuantStart was founded in 2010 to help junior quantitative analysts (QAs) ﬁnd jobs in the tough economic climate. Since then QuantStart has evolved to become a substantial resource for quantitative ﬁnance. The ﬁrm now concentrates on algorithmic trading, but also discusses quantitative development, in Python, R and C++. Since its founding QuantStart has helped over two million visitors improve their quantitative ﬁnanceskills. YoucanalwayscontactQuantStartbysendinganemailtosupport@quantstart.com. 1.
  why_kept: 算法交易的定义：无人工干预的预定义规则执行。本书核心方法论：成功来自完全理解实现细节。
  quant_link: Alpha Model Signal

- excerpt_id: EX-02
  source_hint: Chapter 1: Overview / Target Audience
  quote: >
    algorithmic trading. It is designed for those who enjoy self-study and can learn by example. The book is aimed at individuals interested in actual programming and implementation. It is our belief that real success in algorithmic trading comes from fully understanding the implementation details. Professional quantitative traders will also ﬁnd the content useful. Exposure to new libraries and implementation methods may lead to more optimal execution or more accurate backtesting. 1.
  why_kept: 本书面向有基础编程经验的零售交易者和专业量化从业者，强调通过示例学习。
  quant_link: Alpha Model Signal

- excerpt_id: EX-03
  source_hint: Chapter 1: Overview / Python Setup
  quote: >
    Anaconda is bundled with the Spyder Integrated Development Environment (IDE), which providesaPythonsyntax-highlightingtexteditor, anIPythonconsoleforinteractiveworkﬂow/vi- sualisation and an object/variable explorer for debugging. All of the code in the Python sections of this book have been designed to be executed using Anaconda for Python 3.7. However, many seasoned developers prefer to work outside of the Anaconda environment, e.g. by using virtualenv. The code in this book will also happily work in such virtual environments once the necessary libraries have been installed.
  why_kept: Anaconda + Spyder IDE 是推荐开发环境，本书代码针对 Python 3.7 设计，但兼容虚拟环境。
  quant_link: Alpha Model Signal

- excerpt_id: EX-04
  source_hint: Chapter 2: Data / Backtesting Advantage
  quote: >
    this book. Backtesting allows the statistical properties of a strategy to be estimated, providing insight into whether a strategy is likely to be proﬁtable in the future. Eﬃciency Algorithmic trading is substantially more eﬃcient than a discretionary approach. With a fully automated system there is no need for an individual or team to be constantly monitoring the markets for price action or news input. This frees up time for the developer(s) of the trading strategy to carry out more research and thus, depending upon capital constraints, deploy more strategies into a portfolio.
  why_kept: 回测是算法交易最重要的优势：通过历史数据估计策略统计属性，判断未来盈利可能性。
  quant_link: Backtest Equity Curve

- excerpt_id: EX-05
  source_hint: Chapter 2: Data / Efficiency
  quote: >
    Higher Frequencies This is a corollary of the eﬃciency advantage discussed above. Strategies that operate at higher frequencies over many markets become possible in an automated setting. Indeed, some of the most proﬁtable trading strategies operate at the ultra-high frequency domain on limit order book data. These strategies are simply impossible for a human to carry out. 2.1.2 Disadvantages While the advantages of algorithmic trading are numerous there are some disadvantages.
  why_kept: 自动化系统无需持续监控市场，释放时间用于研究，可部署更多策略到组合中。
  quant_link: Backtest Equity Curve

- excerpt_id: EX-06
  source_hint: Chapter 2: Data / Disadvantages
  quote: >
    Within Successful Algorithmic Tradingwe have attempted to demonstrate a wide variety of strategies. The vast majority require minimal mathematical prerequisites. However, if you do possess numerical modelling skills then you will likely ﬁnd it easier to make use of the statistical time series methods present in the Modelling section. Many of the algorithmic methods demon- strated have already been implemented in external Python libraries, which saves a substantial amount of development work.
  why_kept: 算法交易的劣势：技术风险（bug、API 中断）、市场制度变化导致策略失效。
  quant_link: Model Risk Guard

- excerpt_id: EX-07
  source_hint: Chapter 3: Backtesting / Definition
  quote: >
    is a plot of the strategy account size through time. Various statistical measures can then be calculated on this dataset providing quantitative insight into how eﬀective a strategy is. It is these statistical measures that allows quantitative traders to decide whether a historical simulation looks promising enough to motivate further research and potential implementation of a strategy. 3.1.
  why_kept: 回测定义：将策略算法暴露于历史数据流，产生交易信号与权益曲线。统计指标决定策略是否值得进一步研究。
  quant_link: Backtest Equity Curve

- excerpt_id: EX-08
  source_hint: Chapter 3: Backtesting / Biases Overview
  quote: >
    3.2 Backtesting Biases There are many biases that can aﬀect the performance of a backtested strategy. Unfortunately, these biases have a tendency to inﬂate the performance rather than detract from it. Thus you should always consider a backtest to be an idealised upper bound on the actual performance of the strategy. It is almost impossible to eliminate biases from algorithmic trading so it is our job to minimise them as best we can in order to make informed decisions about our algorithmic strategies.
  why_kept: 回测偏差倾向于高估而非低估表现，因此回测应视为实际表现的理想化上界。
  quant_link: Survivorship Bias Ratio

- excerpt_id: EX-09
  source_hint: Chapter 3: Backtesting / Look-Ahead Bias
  quote: >
    3.2.2 Look-Ahead Bias Look-ahead bias is introduced into a backtesting system when future data is accidentally included at a point in the simulation where that data would not have actually been available. If we are running the backtest chronologically and we reach time pointN, then look-ahead bias occurs if data is included for any pointN +k, wherek > 0. Look-ahead bias errors can be incredibly subtle. Here are three examples of how look-ahead bias can be introduced: • Technical Bugs- Arrays/vectors in code often have iterators or index variables.
  why_kept: 前视偏差：在模拟时间点 N 错误地包含未来 N+k 的数据。代码中的数组迭代器和索引是常见漏洞来源。
  quant_link: Look-Ahead Bias Flag

- excerpt_id: EX-10
  source_hint: Chapter 4: Platforms / Programming
  quote: >
    Diﬀerent strategies require diﬀerent software packages. HFT strategies are often written in C/C++. Presently such strategies are often carried out on Graphical Processing Units (GPU) and Field-Programmable Gate Arrays (FPGA). Conversely low-frequency directional equity strategies are easy to implement in tools such as TradeStation due to the “all in one” nature of the software/brokerage. 4.1.1 Programming Custom development of a backtesting language within a ﬁrst-class programming language pro- vides the most ﬂexibility when testing a strategy.
  why_kept: 在一流编程语言中自定义回测语言提供最大灵活性，而 vendor 平台必须对回测方式做假设。
  quant_link: Strategy Sniper Execution

- excerpt_id: EX-11
  source_hint: Chapter 4: Platforms / Research vs Event-Driven
  quote: >
    Despite these executional shortcomings, research environments are heavily used within the professional quantitative environment. They are the “ﬁrst test” for all strategy ideas before promoting them to a more rigourous check within a realistic backtesting environment. 4.1.3 Event-Driven Backtesting Once a strategy has been deemed suitable on a research basis it must be tested in a more realistic fashion. Such realism attempts to account for the majority (if not all) of the issues described in the previous chapter.
  why_kept: 研究工具（MATLAB/R/Python）用于快速验证想法；事件驱动回测用于更真实的执行模拟。
  quant_link: Strategy Sniper Execution

- excerpt_id: EX-12
  source_hint: Chapter 4: Platforms / Latency
  quote: >
    ment during the latency period will not aﬀect the strategy to any great extent. Unfortunately, the same is not true of higher-frequency strategies. At these frequencies latency becomes impor- tant. The ultimate goal is to reduce latency as much as possible in order to minimiseslippage, as discussed in the previous chapter. Decreasing latency involves minimising the “distance” between the algorithmic trading system and the ultimate exchange on which an order is being executed.
  why_kept: 高频策略中延迟至关重要，目标是减少延迟以最小化滑点。降低延迟需要缩短交易系统与交易所之间的距离。
  quant_link: Strategy Sniper Execution

- excerpt_id: EX-13
  source_hint: Chapter 5: Strategy Discovery / Income
  quote: >
    drawdown funds? Income dependence will dictate the frequency of your strategy. More regular income withdrawals will require a higher frequency trading strategy with less volatility (i.e. a higher Sharpe ratio). Finally, do not be deluded by the notion of becoming extremely wealthy in a short space of time! Algo trading is NOT a get-rich-quick scheme- if anything it can be a become-poor- quick scheme. It takes signiﬁcant discipline, research, diligence and patience to be successful at algorithmic trading. It can take months, if not years, to generate consistent proﬁtability. 5.
  why_kept: 收入依赖决定策略频率：更频繁提款需要更高频率、更低波动率（更高 Sharpe）的策略。
  quant_link: Position Sizing Rule

- excerpt_id: EX-14
  source_hint: Chapter 5: Strategy Discovery / Sources
  quote: >
    Financial Markets and Participants The following list details books that outline how capital markets work and describe modern electronic trading. • Financial Times Guide to the Financial Marketsby Glen Arnold[1] - This book is designed for the novice to the ﬁnancial markets. It provides insight into all of the market participants. For our purposes it outlines a list of markets on which we might later trade algorithmically.
  why_kept: 策略来源：学术期刊、预印本、交易博客、论坛、杂志。目标是建立持续产生想法的管道。
  quant_link: Alpha Model Signal

- excerpt_id: EX-15
  source_hint: Chapter 6: Data Storage / Securities Master
  quote: >
    • EODData - http://eoddata.com (requires registration) It is straightforward to manually download historical data for individual securities but it becomes time-consuming if many stocks need to be downloaded daily. Thus an important com- ponent of our securities master will be automatically updating the data set. Another issue islook-back period. How far in the past do we need to go with our data? This will be speciﬁc to the requirements of your trading strategy, but there are certain problems that span all strategies.
  why_kept: Securities Master 是组织级数据库，存储所有资产类别的定价与交易数据，自动更新是关键组件。
  quant_link: Securities Master Schema

- excerpt_id: EX-16
  source_hint: Chapter 6: Data Storage / Look-Back
  quote: >
    6.3.2 Document Stores/NoSQL Document stores/NoSQL databases, while certainly not a new concept, have gained signiﬁcant prominence in recent years due to their use at “web-scale” ﬁrms such as Google, Facebook and Twitter. They diﬀer substantially from RDBMS systems in that there is no concept of table schemas. Instead there arecollections and documents, which are the closest analogies to tables and records, respectively.
  why_kept: 数据回溯期：获取尽可能多的数据，但需注意 regime change（监管环境、波动率、趋势变化）。
  quant_link: Data Cleansing Pipeline

- excerpt_id: EX-17
  source_hint: Chapter 7: Risk / Data Retrieval
  quote: >
    their problems, but they can save a great deal of time. The time-saving usually comes at the expense of performance, however. A popular ORM for Python isSQLAlchemy. It allows you to specify the database schema within Python itself and thus automatically generate theCREATE TABLE code. Since we have speciﬁcally chosen MySQL and are concerned with performance we have opted not to use an ORM for this chapter. Symbol Retrieval Let’s begin by obtaining all of the ticker symbols associated with the Standard & Poor’s list of 500 large-cap stocks, i.e. the S&P500. Of course, this is simply an example.
  why_kept: S&P500 成分股列表可通过 Wikipedia 获取，但成分数量随时间变化。使用 requests + BeautifulSoup 抓取并入库。
  quant_link: Securities Master Schema

- excerpt_id: EX-18
  source_hint: Chapter 8: Processing / Unstructured Data
  quote: >
    7.1.4 Unstructured Data Unstructured data consists ofdocuments such as news articles, blog posts, papers or reports. Analysis of such data can be complicated as it relies onNatural Language Processing(NLP) techniques. One such use of analysing unstructured data is in trying to determine thesentiment context. This can be useful in driving a trading strategy. For instance, by classifying texts as “bullish”, “bearish” or “neutral” a set of trading signals could be generated. The term for this process issentiment analysis.
  why_kept: 非结构化数据（新闻、博客、报告）需 NLP 处理。情感分析可用于生成交易信号（bullish/bearish/neutral）。
  quant_link: Seasonal/News Event Filter

### FORMULAS_AND_ALGOS

**1. Backtest Equity Curve (Chapter 3)**
```
equity_0 = initial_capital
for each trade i in trades:
    pnl_i = direction_i * (exit_price_i - entry_price_i) * size_i - costs_i
    equity_i = equity_{i-1} + pnl_i
cum_return_t = equity_t / equity_0 - 1
```
- 必须包含未平仓头寸的盯市盈亏（mark-to-market）
- 失效条件：未处理分红复权、拆股、停牌导致的价格跳空

**2. Securities Master Schema (Chapter 2/6)**
```
Table: instrument
  symbol VARCHAR(16) PRIMARY KEY
  asset_class ENUM('equity','fx','futures','option','bond')
  exchange VARCHAR(16)
  currency VARCHAR(3)
  sector VARCHAR(32)

Table: daily_price
  symbol VARCHAR(16)
  date DATE
  open, high, low, close DECIMAL(18,4)
  volume BIGINT
  adj_close DECIMAL(18,4)
  PRIMARY KEY (symbol, date)
```
- 必须保留退市股票记录，否则引入幸存者偏差
- 失效条件：若未记录复权因子（split/dividend），则 adj_close 计算错误

**3. Transaction Cost Model (Chapter 3)**
```
total_cost = commission + slippage + market_impact
commission = filled_notional * commission_rate
slippage = |fill_price - signal_price| / signal_price
market_impact = c * sigma * (order_size / ADV)^gamma
A 股额外：stamp_duty = sell_notional * 0.0005 (单边)
```
- 滑点应按流通市值分档：大盘股 < 0.01%，小盘股可达 0.1%+
- 失效条件：涨停/跌停时无法成交，此时成本模型应返回 'no_fill'

**4. Position Sizing (Chapter 7)**
```
size = floor(account_equity * risk_fraction / (ATR_20 * price * lot_size))
where ATR_20 = average true range over 20 days
      risk_fraction = 0.01 (1% per trade)
      lot_size = 100 (A 股最小交易单位)
```
- A 股必须取整手（100 股倍数），size 不能为分数
- 失效条件：若策略信号为空仓但已有持仓，需先处理平仓再计算新 size

### NOT_QUANT_YET
1. **Tick 级订单簿信号** - 需要 level2 逐笔数据；A 股免费数据无此粒度；标 needs_extra_data。
2. **完全自动化无人执行（Sniper）** - 高度依赖券商 API 稳定性与网络延迟；标 shell_only（技术可行但工程风险高）。
3. **外汇/期货多资产 Securities Master** - A 股零售账户通常只能交易股票与场内基金；标 future_bucket。
4. **机器学习驱动的数据清洗** - 使用异常检测模型自动标记坏数据；标 future_bucket（需要标注好的异常样本）。
5. **跨交易所套利（如港股通 vs A 股）** - 需要多交易所数据与跨境执行能力；标 future_bucket。

### NEXT_ACTION
1. 生成 securities_master_schema 对象定义壳：含 instrument、daily_price、corporate_action、dividend 四表。
2. 生成 data_cleansing_pipeline 代码：输入原始 OHLCV，输出清洗后数据 + 异常标记日志。
3. 生成 transaction_cost_model 参数表：A 股分档（主板/创业板/科创板）给出佣金、印花税、滑点估计。
4. 生成 backtest_equity_curve 状态模板：输入交易记录，输出权益曲线、回撤、夏普、最大回撤。
5. 生成 position_sizing_a_share 模块：含整数手取整、涨停可买性判断、跌停可卖性判断。
6. 评估 A 股免费 tick 数据源（如 tushare、akshare、jqdata）的 level1 可用性与存储成本。