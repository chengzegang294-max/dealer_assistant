### MATERIAL_CARD
- title: Successful Algorithmic Trading
- author_or_source: Michael L. Halls-Moore
- material_type: 书
- domain_tags: [算法交易入门, 回测, 执行系统, 数据平台, 统计学习, 时间序列分析, 策略优化, 事件驱动引擎]
- file_scope: 全书 303 页（Part I-VI + 附录）

### ROUTING_DECISION
- current_repo_role: data_engineering_guard / state_template_shell
- is_worth_deep_cut_now: yes
- deep_cut_priority: P1
- reason: 本书是 Python 算法交易的实操手册，覆盖数据存储、清洗、回测、执行、统计学习、预测、事件驱动引擎全链路。比 Ernest Chan 的书更偏工程实现和基础设施（Securities Master、事件驱动架构），适合直接转化为 data_engineering_guard 和 execution_shell。

### CONTENT_CLUSTERS
- cluster_name: 算法交易概述与科学方法
  what_it_is: 算法交易的定义（无人工干预的自动执行）、优势（历史评估、纪律性、规模化）、劣势（技术依赖、模型风险、市场变化）。科学方法在交易中的应用：假设→实验→验证→迭代。零售交易者的竞争力来源。
  keep_level: 低
  repo_mapping: source_library_only
- cluster_name: 成功回测
  what_it_is: 回测的定义（将策略算法暴露于历史数据流以产生交易集合）。回测偏差：优化偏差（曲线拟合）、前视偏差、幸存者偏差、认知偏差。交易所问题：订单类型、价格整合、外汇 ECN、卖空限制。交易成本：佣金、滑点、市场冲击。回测 vs 现实的差距。
  keep_level: 高
  repo_mapping: data_engineering_guard
- cluster_name: 自动执行
  what_it_is: 回测平台选择：编程语言（Python、C++、R）、研究工具（数据可视化、统计库）、集成度。执行系统类型：完全自动化、半自动化、人工辅助。事件驱动回测 vs 向量化回测。经纪商接口（Interactive Brokers）。
  keep_level: 中
  repo_mapping: data_engineering_guard
- cluster_name: 策略发现
  what_it_is: 策略想法来源：量化博客、学术论文、交易书籍、独立研究。个人偏好匹配（交易频率、风险偏好、时间投入）。策略评估框架：夏普比率、最大回撤、胜率、盈亏比。历史数据获取：免费源（Yahoo Finance、Quandl）vs 商业源（DTN IQFeed、Bloomberg）。
  keep_level: 中
  repo_mapping: state_template_shell
- cluster_name: 金融数据存储
  what_it_is: Securities Master Database 的设计：存储基本面、价格、交易数据。存储格式：平面文件（CSV/JSON）、文档数据库（NoSQL）、关系数据库（MySQL/PostgreSQL）。EOD 股票数据的 schema 设计：ticker、date、open、high、low、close、volume、adj_close。自动化数据采集和更新。
  keep_level: 高
  repo_mapping: data_engineering_guard
- cluster_name: 金融数据处理
  what_it_is: 市场与工具分类：股票、外汇、商品、固定收益。数据频率：日数据、日内数据、tick 数据、订单簿数据。数据获取：pandas_datareader、Quandl、AlphaVantage。数据清洗：缺失值处理、异常值检测、复权处理（前复权/后复权）、连续期货合约拼接（rollover）。
  keep_level: 高
  repo_mapping: data_engineering_guard
- cluster_name: 统计学习
  what_it_is: 预测与推断的区别。参数化模型（线性回归、逻辑回归）与非参数化模型（KNN、决策树、随机森林）。监督学习（分类/回归）与无监督学习（聚类/降维）。预测准确率评估：混淆矩阵、准确率、精确率、召回率、F1、ROC-AUC。回归评估：MSE、RMSE、MAE、R^2。
  keep_level: 中
  repo_mapping: model_validation_guard
- cluster_name: 时间序列分析
  what_it_is: 均值回归检验：ADF 检验、Hurst 指数、方差比率检验。协整检验：Engle-Granger 两步法、Johansen 检验。预测模型：ARIMA、GARCH、状态空间模型。时间序列特征：自相关、偏自相关、季节性分解。
  keep_level: 中
  repo_mapping: state_template_shell
- cluster_name: 预测与机器学习
  what_it_is: Scikit-Learn 用于金融预测：SVM、随机森林、梯度提升、逻辑回归。特征工程：技术指标（SMA、EMA、RSI、MACD）、统计特征（波动率、偏度、峰度）。预测方向（涨跌分类）vs 预测幅度（收益率回归）。过拟合防范：交叉验证、正则化（L1/L2）、特征选择。网格搜索（Grid Search）与超参数优化。
  keep_level: 中
  repo_mapping: model_validation_guard
- cluster_name: 性能与风险管理
  what_it_is: 交易级、策略级、组合级性能评估。夏普比率、索提诺比率、最大回撤、Calmar 比率、胜率、盈亏比。凯利公式、最优 f、固定比例交易。风险来源：策略风险、组合风险、市场风险、交易对手风险、技术风险。机构级风险管理：压力测试、情景分析、风险价值（VaR）。
  keep_level: 高
  repo_mapping: data_engineering_guard / state_template_shell
- cluster_name: 事件驱动交易引擎
  what_it_is: 事件驱动架构：事件循环（Event Loop）接收事件（市场数据、交易信号、订单确认、定时事件），分发到对应处理器（策略、组合、风险管理、执行）。组件：DataHandler（历史/实时数据）、Strategy（生成信号）、Portfolio（管理持仓和现金）、ExecutionHandler（发送订单）、Backtest（协调事件流）。统计（向量化）回测 vs 事件驱动回测：向量化快但不真实，事件驱动慢但更贴近实际执行。
  keep_level: 高
  repo_mapping: data_engineering_guard / state_template_shell
- cluster_name: 策略实现与优化
  what_it_is: 移动平均线交叉策略（SMA/EMA）。均值回归策略（Bollinger Bands、RSI 均值回归）。动量策略（突破、趋势跟踪）。预测驱动策略（基于 ML 分类器的方向预测）。日内均值回归配对交易。参数优化：网格搜索、随机搜索、贝叶斯优化。过拟合与样本外测试。交易可视化：权益曲线、回撤曲线、收益分布直方图。
  keep_level: 中
  repo_mapping: state_template_shell

### QUANTIZATION_TABLE
| concept | type | minimal_definition | observable_proxy | min_data_requirement | confirmation_timing | quant_status | repo_target | leakage_risk | notes |
|---|---|---|---|---|---|---|---|---|---|
| Backtest Bias Audit | data_guard | 识别回测中存在的优化偏差、前视偏差、幸存者偏差、认知偏差 | 检查清单：1) 是否使用未来信息；2) 是否只使用存活标的；3) 是否反复优化同一数据集；4) 交易决策是否受主观情绪影响 | OHLCV | 回测开发阶段 | proxy_quantizable_now | data_engineering_guard | high | 认知偏差最难量化，需通过交易日志和策略冻结机制控制 |
| Survivorship Bias Flag | data_guard | 历史数据库是否仅包含存活至今的标的 | 对比当前成分股与历史成分股清单；计算缺失率；标记退市/破产标的 | OHLCV | 数据采购阶段 | proxy_quantizable_now | data_engineering_guard | high | A 股退市股数据获取成本高，免费数据源普遍有偏差 |
| Transaction Cost Model | data_guard | 回测中对佣金、滑点、市场冲击的建模 | 佣金 = 固定费率 × 交易额；滑点 = 买卖价差 × 0.5；市场冲击 = 订单量 / 日均成交量 × 价格冲击系数 | OHLCV + tick | 回测阶段 | proxy_quantizable_now | data_engineering_guard | med | A 股佣金率低（万 1-2），但小盘股滑点可能极高 |
| Securities Master Schema | data_guard | 统一存储金融工具元数据、基本面、价格、交易数据的 schema 设计 | EOD 股票表：ticker、date、open、high、low、close、volume、adj_close；外汇表：pair、date、rate；期货表：symbol、expiry、continuous_flag | OHLCV | 数据采购阶段 | proxy_quantizable_now | data_engineering_guard | low | 需支持多资产类别；A 股需处理复权因子、停牌标记、ST 标记 |
| Data Quality Scorecard | data_guard | 评估金融数据质量的维度：完整性、准确性、及时性、一致性 | 缺失率 = 缺失天数 / 总天数；异常率 = 超出 n 倍标准差的收益率比例；延迟 = 数据接收时间 - 交易所时间 | OHLCV | 数据清洗阶段 | proxy_quantizable_now | data_engineering_guard | low | 需逐日监控；A 股停复牌、涨跌停导致数据缺失需特殊处理 |
| Continuous Futures Contract | data_guard | 将近月合约拼接为连续价格序列，处理换月展期 | 展期点选择：按成交量切换或按到期日切换；展期价差调整：加法（价格）或乘法（收益率）调整 | OHLCV futures | 数据清洗阶段 | proxy_quantizable_now | data_engineering_guard | med | 不同展期方法导致不同收益率；需记录展期调整因子 |
| ADF Mean Reversion Test | risk_guard | 检验价格序列是否存在单位根，即是否适合均值回归策略 | ADF 检验统计量 < 临界值（如 5%）则拒绝单位根；或报告 p-value < 0.05 | OHLCV | 策略筛选阶段 | proxy_quantizable_now | state_template_shell | low | 需区分序列 ADF（单序列）和 Engle-Granger（残差 ADF） |
| Hurst Exponent | state | 衡量时间序列的长期记忆性：H < 0.5 均值回归，H = 0.5 随机游走，H > 0.5 趋势 | R/S 分析估计 H；或在滚动窗口上估计；绘制 H 时间序列观察 regime 切换 | OHLCV | 策略筛选阶段 | proxy_quantizable_now | state_template_shell | low | 对样本长度敏感；短期窗口估计方差大；A 股政策突变期 H 可能跳变 |
| Cointegration Test (EG / Johansen) | risk_guard | 检验多资产价格序列的线性组合是否平稳 | Engle-Granger：回归残差 ADF；Johansen：迹检验/最大特征值检验；r > 0 则存在协整 | OHLCV | 策略筛选阶段 | proxy_quantizable_now | state_template_shell | low | A 股停牌导致面板不平衡；需处理缺失值 |
| Sharpe Ratio | risk_guard | 策略超额收益 / 超额收益波动率 | Sharpe = (R_p - R_f) / sigma_p；按日或月收益率计算；年化系数 = sqrt(252) 或 sqrt(12) | OHLCV | 回测完成后 | proxy_quantizable_now | data_engineering_guard | low | 需用无风险利率 R_f 修正；A 股常用 10 年期国债收益率 |
| Maximum Drawdown | risk_guard | 权益曲线从峰值到谷底的最大回撤百分比 | DD_t = (Peak_t - Equity_t) / Peak_t；MDD = max(DD_t)；Time under Water = DD_t > 0 的持续天数 | OHLCV | 回测/实时 | proxy_quantizable_now | data_engineering_guard | low | 需区分日内回撤与收盘回撤；A 股 T+1 限制下日内无法平仓 |
| Sortino Ratio | risk_guard | 策略超额收益 / 下行标准差（仅负收益波动） | Sortino = (R_p - R_f) / sigma_d；sigma_d 为下行偏差标准差 | OHLCV | 回测完成后 | proxy_quantizable_now | data_engineering_guard | low | 比 Sharpe 更适合偏度为负的策略；A 股策略通常偏度为负 |
| Calmar Ratio | risk_guard | 策略年化收益 / 最大回撤 | Calmar = R_p / MDD；用于标准化不同持有期的策略表现 | OHLCV | 回测完成后 | proxy_quantizable_now | data_engineering_guard | low | 若 MDD 被时间拉长，Calmar 会下降；需结合持有期评估 |
| Kelly Optimal f | execution_rule | 基于历史胜率盈亏比的最优资金比例 | f* = (bp - q) / b，其中 b 为平均盈利/平均亏损，p 为胜率，q = 1-p。或简化为 f* = p - (1-p)/b | OHLCV | 回测后 | proxy_quantizable_now | state_template_shell | high | 通常取半 Kelly；A 股不能自由加杠杆，Kelly 用于仓位比例 |
| Fixed Fractional Sizing | execution_rule | 每笔交易固定风险比例（如 1% 账户资金） | 仓位 = 账户资金 × 风险比例 / (止损幅度 × 每股价格) | OHLCV | 实时 | proxy_quantizable_now | state_template_shell | low | 简单直观；但不同策略的最优风险比例不同 |
| Prediction Accuracy Metrics | model_guard | 分类模型预测方向的评估指标 | 混淆矩阵：TP/FP/TN/FN；准确率 = (TP+TN)/(N)；精确率 = TP/(TP+FP)；召回率 = TP/(TP+FN)；F1 = 2 * 精确率 * 召回率 / (精确率 + 召回率) | OHLCV + labels | 模型训练后 | proxy_quantizable_now | model_validation_guard | low | 金融预测中类别不平衡（涨/跌/平）需关注精确率和召回率 |
| ROC-AUC | model_guard | 分类模型区分正负样本的能力 | ROC 曲线：横轴 FP Rate = FP/(FP+TN)，纵轴 TP Rate = TP/(TP+FN)；AUC = ROC 曲线下面积；AUC > 0.5 优于随机猜测 | OHLCV + labels | 模型训练后 | proxy_quantizable_now | model_validation_guard | low | AUC 对类别不平衡不敏感；但金融预测中阈值选择比 AUC 更重要 |
| Overfitting Detection (In-Sample vs OOS) | model_guard | 样本内表现显著优于样本外表现，提示过拟合 | 样本内 Sharpe / 样本外 Sharpe > 2；或样本内准确率 - 样本外准确率 > 阈值（如 10%） | OHLCV | 模型训练后 | proxy_quantizable_now | model_validation_guard | high | 网格搜索超参数优化本身会加剧过拟合；需使用嵌套交叉验证 |
| Grid Search Hyperparameter | model_guard | 在预定义参数网格上穷举所有组合，评估性能 | 参数网格：如 SVM 的 C ∈ [0.1, 1, 10]，gamma ∈ [0.01, 0.1, 1]；每组合做 k-fold CV；选最优参数组合 | OHLCV + labels | 模型训练阶段 | proxy_quantizable_now | model_validation_guard | med | 参数空间爆炸时计算不可行；可用随机搜索或贝叶斯优化替代 |
| Event-Driven Backtest Architecture | execution_rule | 通过事件循环模拟真实交易执行流程的回测系统 | 组件：MarketEvent → DataHandler → Strategy → SignalEvent → Portfolio → OrderEvent → ExecutionHandler → FillEvent → Portfolio。事件按时间顺序处理，模拟延迟和滑点 | OHLCV | 回测阶段 | proxy_quantizable_now | data_engineering_guard | low | 比向量化回测慢但更接近现实；可无缝切换为实盘引擎 |
| Vectorized Backtest | execution_rule | 对整个历史数据一次性计算信号和收益，无逐事件处理 | 信号向量 = f(价格矩阵)；收益向量 = 信号向量.shift(1) × 收益率向量；累计收益 = cumprod(1 + 收益向量) | OHLCV | 回测阶段 | proxy_quantizable_now | data_engineering_guard | low | 速度快但忽略执行细节、滑点、订单填充顺序；仅适合初步筛选 |

### RETAINED_EXCERPTS
- excerpt_id: EX-01
  source_hint: Part I / Chapter 2: What Is Algorithmic Trading / Overview
  quote: >
    Algorithmic trading, as defined here, is the use of an automated system for carrying out trades, which are executed in a pre-determined manner via an algorithm specifically without any human intervention. The latter emphasis is important. Algorithmic strategies are designed prior to the commencement of trading and are executed without discretionary input from human traders. In this book "algorithmic trading" refers to the retail practice of automated, systematic and quantitative trading, which will all be treated as synonyms for the purpose of this text. In the financial industry "algorithmic trading" often refers to a class of execution algorithms (such as Volume Weighted Average Price, VWAP) used to optimise the costs of larger trading orders, rather than automated trading in general.
  why_kept: 算法交易的精确定义：无人工干预的自动执行；策略预先设计、执行中无主观裁量。保留作为概念边界划分的依据。
  quant_link: Event-Driven Backtest Architecture

- excerpt_id: EX-02
  source_hint: Part II / Chapter 3: Successful Backtesting / Why Backtest
  quote: >
    Systematic trading stands apart from other types of investment approaches because we can more reliably provide expectations of future performance from past performance as a consequence of relatively abundant historical data availability. The process by which this is carried out is known as backtesting. Backtesting is carried out by exposing a particular strategy algorithm to a stream of historical financial data, which leads to a set of trading signals and associated portfolio values.
  why_kept: 回测的定义：将策略算法暴露于历史数据流，产生交易信号和组合价值序列。保留作为回测模块的基础定义。
  quant_link: Backtest Bias Audit / Vectorized Backtest

- excerpt_id: EX-03
  source_hint: Part II / Chapter 3: Successful Backtesting / Backtesting Biases
  quote: >
    Optimisation Bias (also known as "curve fitting" or "data-snooping bias") occurs when a strategy is excessively tuned to historical data. This can happen when a trader repeatedly tests a strategy on the same dataset, adjusting parameters until the performance is maximised. Look-Ahead Bias occurs when a strategy uses information that would not have been available at the time of trading. This is often subtle and can arise from incorrectly aligned data timestamps or using future information in signal generation. Survivorship Bias occurs when a strategy is tested on a dataset that only includes securities that have survived to the present day, ignoring those that have been delisted or gone bankrupt.
  why_kept: 三大回测偏差的精确定义：优化偏差（反复调参）、前视偏差（使用未来信息）、幸存者偏差（只使用存活标的）。保留作为回测审计的核心检查项。
  quant_link: Backtest Bias Audit / Survivorship Bias Flag

- excerpt_id: EX-04
  source_hint: Part II / Chapter 3: Successful Backtesting / Transaction Costs
  quote: >
    Commission is the fee charged by a broker for executing a trade. Slippage is the difference between the expected price of a trade and the actual price at which the trade is executed. Market impact is the effect that a trade has on the market price of the security. For small retail traders, market impact is usually negligible, but for large institutional traders, it can be substantial. All three of these costs must be accurately modelled in a backtest to ensure that the strategy is realistic.
  why_kept: 三类交易成本定义：佣金、滑点、市场冲击。保留作为回测成本建模的基础。
  quant_link: Transaction Cost Model

- excerpt_id: EX-05
  source_hint: Part III / Chapter 6: Financial Data Storage / Securities Master
  quote: >
    A securities master is an organisation-wide database that stores fundamental, pricing and transactional data for a variety of financial instruments across asset classes. In algorithmic trading, an accurate and timely securities master is crucial for the performance of a strategy. The securities master must be designed to handle high volumes of data, support multiple data formats, and provide a unified interface for strategy backtesting and execution.
  why_kept: Securities Master 的定义：组织级统一数据库，存储多资产类别的基本面、价格和交易数据。保留作为数据基础设施设计的核心概念。
  quant_link: Securities Master Schema

- excerpt_id: EX-06
  source_hint: Part III / Chapter 7: Processing Financial Data / Cleaning
  quote: >
    Continuous futures contracts are constructed by concatenating individual futures contracts as they approach expiry. The process of concatenation is known as a rollover. There are two main approaches to adjusting the price during a rollover: the "backwards" adjustment (also known as "panama canal" or "price" adjustment) and the "forwards" adjustment (also known as "ratio" or "return" adjustment). In the backwards adjustment, the price difference between the old and new contract is subtracted from all historical prices prior to the rollover date. In the forwards adjustment, the price ratio between the old and new contract is multiplied by all historical prices prior to the rollover date.
  why_kept: 连续期货合约的两种展期调整方法：加法（价格）调整 vs 乘法（收益率）调整。保留作为期货数据清洗的关键技术选择。
  quant_link: Continuous Futures Contract

- excerpt_id: EX-07
  source_hint: Part IV / Chapter 9: Time Series Analysis / Testing Mean Reversion
  quote: >
    The basic idea when trying to ascertain if a time series is mean-reverting is to use a statistical test to see if it differs from the behaviour of a random walk. A random walk is a time series where the next directional movement is completely independent of any past movements - in essence the time series has no memory. If a time series is mean-reverting, it will tend to move back towards its historical mean whenever it deviates significantly from it.
  why_kept: 均值回归检验的核心思想：判断序列是否与随机游走（无记忆）不同。保留作为均值回归策略筛选的理论基础。
  quant_link: ADF Mean Reversion Test / Hurst Exponent

- excerpt_id: EX-08
  source_hint: Part V / Chapter 11: Performance Measurement / Overview
  quote: >
    Performance measurement is an absolutely crucial component of algorithmic trading. Without assessment of performance, along with solid record keeping, it is difficult, if not impossible, to determine if our strategy returns have been due to luck or due to some actual edge over the market. In order to be successful in algorithmic trading it is necessary to be aware of all of the factors that can affect the profitability of trades, and ultimately strategies.
  why_kept: 性能测量的必要性：没有性能评估就无法区分运气与真实优势。保留作为策略评估模块的定性起点。
  quant_link: Sharpe Ratio / Maximum Drawdown / Sortino Ratio / Calmar Ratio

- excerpt_id: EX-09
  source_hint: Part V / Chapter 12: Risk and Money Management / Sources of Risk
  quote: >
    The broad areas of risk that we will consider include Strategy Risk, Portfolio Risk, Market Risk, Counterparty Risk, Technology Risk and Operational Risk. Strategy Risk refers to the possibility that the trading strategy itself is flawed or that market conditions have changed such that the strategy is no longer profitable. Portfolio Risk refers to the risk that the combination of strategies in a portfolio may perform worse than expected due to correlation changes. Market Risk refers to the risk of losses due to market movements. Counterparty Risk refers to the risk that the broker or exchange may default. Technology Risk refers to the risk of software bugs, hardware failures, or network outages. Operational Risk refers to the risk of human error or process failures.
  why_kept: 六大风险类别的定义：策略风险、组合风险、市场风险、交易对手风险、技术风险、操作风险。保留作为风险管理模块的分类框架。
  quant_link: Backtest Bias Audit / Overfitting Detection

- excerpt_id: EX-10
  source_hint: Part VI / Chapter 13: Event-Driven Trading Engine / Event-Driven Software
  quote: >
    A video game has multiple components that interact with each other in a real-time setting at high framerates. This is handled by running the entire set of calculations within an "infinite" loop known as the event-loop or game-loop. At each tick of the game-loop a function is called to receive the latest event, which will have been generated by some corresponding prior action within the game. Depending upon the event type, the event is dispatched to the appropriate handler, which updates the game state and potentially generates new events. Algorithmic trading systems are conceptually identical to video games in this regard.
  why_kept: 事件驱动架构的类比：与视频游戏的事件循环/游戏循环概念相同。保留作为事件驱动交易引擎设计的概念起点。
  quant_link: Event-Driven Backtest Architecture

- excerpt_id: EX-11
  source_hint: Part VI / Chapter 14: Trading Strategy Implementation / Overview
  quote: >
    We will see that our first two attempts at creating a trading strategy on interday data are not altogether successful. It can be challenging to come up with a profitable trading strategy on interday data once transaction costs have been taken into account. The latter is something that many texts on algorithmic trading tend to leave out. However, we will add as many factors as possible to the backtest in order to minimise surprises going forward.
  why_kept: 日间策略的困难：一旦纳入交易成本，日间策略很难盈利。许多教材忽略这一点。保留作为策略评估的诚实基准。
  quant_link: Transaction Cost Model / Overfitting Detection

- excerpt_id: EX-12
  source_hint: Part VI / Chapter 15: Strategy Optimisation / Parameter Optimisation
  quote: >
    In the case of an SVM we have the tuning parameters gamma and C. In a Moving Average Crossover trading strategy we have the parameters for the two lookback windows of the moving average filters. In this chapter we are going to describe optimisation methods to improve the performance of our trading strategies by tuning the parameters in a systematic fashion. For this we will use mechanisms from the statistical field of Model Selection, such as cross-validation and grid search. The literature on model selection and parameter optimisation is vast and most of the methods are somewhat beyond the scope of this book. Here we want to introduce the subject so that you can explore more sophisticated techniques at your own pace.
  why_kept: 参数优化的必要性：任何策略和模型都有调参需求（如 SVM 的 gamma/C、均线策略的窗口）。网格搜索和交叉验证是入门方法。保留作为模型验证模块的基础。
  quant_link: Grid Search Hyperparameter / Overfitting Detection

### FORMULAS_AND_ALGOS

**1. Backtest Bias Checklist (Chapter 3)**
检查清单：1) 优化偏差——是否反复在同一数据集上调参直至性能最大化？2) 前视偏差——信号生成是否使用了未来信息？3) 幸存者偏差——数据库是否包含已退市标的？4) 认知偏差——交易决策是否受情绪影响？
- 每新增一个策略或数据集，必须执行以上检查
- 失效条件：外购数据供应商未明确标注成分股历史、复权时点、换月规则

**2. Transaction Cost Model (Chapter 3)**
公式：佣金 = 固定费率 × 交易额；滑点 = 买卖价差中点 × 0.5（假设市价单以价差另一边成交）；市场冲击 = 订单量 / 日均成交量 × 价格冲击系数。总成本 = 佣金 + 滑点 + 市场冲击。
- 适用：回测阶段对策略进行成本敏感性分析
- 失效条件：A 股小盘股在极端行情下买卖价差可能扩大至数倍；冲击系数需按市值分档校准

**3. Securities Master Schema (Chapter 6)**
定义：EOD 股票表（ticker, date, open, high, low, close, volume, adj_close）；外汇表（pair, date, rate）；期货表（symbol, expiry, continuous_flag, rollover_date）。
- 适用：多资产类别策略的数据统一存储
- 失效条件：A 股需额外处理复权因子（前复权/后复权）、停牌标记、ST 标记、科创板/创业板标识

**4. Continuous Futures Contract (Chapter 7)**
公式：加法调整（ backwards / price 调整）——新合约价格 - 旧合约价格 = 价差 delta；历史价格全部减去 delta。乘法调整（forwards / ratio 调整）——新合约价格 / 旧合约价格 = 比率 ratio；历史价格全部乘以 ratio。
- 适用：期货策略的回测和实盘数据准备
- 失效条件：不同品种的最优展期点不同（按成交量切换 vs 按到期日切换）；需记录调整因子以便收益计算准确

**5. ADF / Hurst / Variance Ratio (Chapter 9)**
公式：ADF 检验——若统计量 < 临界值（如 5%），则拒绝单位根假设，序列平稳。Hurst 指数 H——R/S 分析或 AR(1) 回归估计；H < 0.5 均值回归，H = 0.5 随机游走，H > 0.5 趋势。方差比率 VR(k)——VR(k) = Var(r^{(k)})/(k * Var(r))；若 VR < 1 则均值回归。
- 适用：均值回归策略的对象筛选和 regime 检测
- 失效条件：检验窗口选择不当；A 股政策干预导致非平稳性假设本身不成立

**6. Sharpe / Sortino / Calmar (Chapter 11)**
公式：Sharpe = (R_p - R_f) / sigma_p；Sortino = (R_p - R_f) / sigma_d（sigma_d 为下行标准差）；Calmar = R_p / MDD。年化系数：日收益 × sqrt(252)；月收益 × sqrt(12)。
- 适用：策略和组合的风险调整后收益评估
- 失效条件：收益分布严重偏斜或厚尾时，Sharpe 不能完整描述风险；需结合 Sortino、Calmar、最大回撤

**7. Kelly Optimal f (Chapter 12)**
公式：f* = (bp - q) / b，其中 b 为平均盈利/平均亏损，p 为胜率，q = 1-p。简化版：f* = p - (1-p)/b。半 Kelly：f = f* / 2。固定比例：每笔交易风险 = 账户资金 × 风险比例（如 1%）/ (止损幅度 × 每股价格)。
- 适用：确定单笔交易的资金分配比例
- 失效条件：A 股不能自由加杠杆（两融上限约 2x），Kelly 建议用于仓位比例而非总杠杆；止损幅度需根据波动率动态调整

**8. Prediction Accuracy Metrics (Chapter 10)**
公式：混淆矩阵——TP/FP/TN/FN。准确率 = (TP+TN)/N；精确率 = TP/(TP+FP)；召回率 = TP/(TP+FN)；F1 = 2 * 精确率 * 召回率 / (精确率 + 召回率)。ROC 曲线——横轴 FP Rate，纵轴 TP Rate；AUC = ROC 下面积。
- 适用：机器学习分类器预测涨跌方向的评估
- 失效条件：金融预测中类别严重不平衡（涨/跌/平），准确率高可能仅因预测多数类；需关注精确率、召回率、F1 和 AUC

**9. Event-Driven Backtest Architecture (Chapter 13)**
定义：事件循环按时间顺序处理 MarketEvent → DataHandler → Strategy → SignalEvent → Portfolio → OrderEvent → ExecutionHandler → FillEvent → Portfolio。每个组件仅处理自己关心的事件类型，更新状态后可能生成新事件。
- 适用：模拟真实交易执行的回测系统；可无缝切换为实盘引擎
- 失效条件：事件处理顺序和延迟假设必须与目标交易所匹配；A 股 T+1 结算规则需在 Portfolio 组件中准确建模

**10. Grid Search Hyperparameter (Chapter 15)**
公式：在预定义参数网格上穷举所有组合。如 SVM 的 C ∈ [0.1, 1, 10]，gamma ∈ [0.01, 0.1, 1]；均线策略的短窗口 ∈ [5, 10, 20]，长窗口 ∈ [20, 50, 100]。每组合做 k-fold 交叉验证；选验证性能最优的参数组合。
- 适用：策略和模型的超参数优化
- 失效条件：参数空间爆炸时计算不可行；网格搜索本身会加剧过拟合；需使用嵌套交叉验证或样本外测试集做最终验证

### NOT_QUANT_YET
1. **新闻情绪分析与 Twitter 情感** - 需要独立构建中文新闻情绪词典和实时流处理；A 股信息扩散速度快，套利窗口极短；标 needs_extra_data。
2. **高频事件驱动引擎（秒级/毫秒级）** - 需要 tick/Level-2 数据和交易所直连；本书事件驱动架构为分钟级设计；标 needs_extra_data。
3. **深度学习与神经网络** - 本书未涉及；Scikit-Learn 仅覆盖传统 ML；标 future_bucket。
4. **多资产类别衍生品定价（期权、互换）** - 本书仅涉及股票、期货、外汇；标 source_library_only。
5. **云计算与分布式回测** - 纯基础设施扩展，属于工程实现而非量化对象；标 source_library_only。

### NEXT_ACTION
1. 生成 backtest_bias_auditor 模块：输入策略参数和数据源，输出优化偏差、前视偏差、幸存者偏差、认知偏差标记及修正建议。
2. 生成 securities_master_builder 模块：输入多资产数据，输出统一 schema 的 securities master 数据库，支持 A 股复权、停牌、ST 标记。
3. 生成 futures_rollover_adjuster 模块：输入期货合约序列，输出连续合约（加法/乘法调整），记录展期调整因子。
4. 生成 mean_reversion_screener 模块：输入 OHLCV，输出 ADF/Hurst/VR 检验、半衰期、协整检验结果，筛选可交易对象。
5. 生成 performance_dashboard 模块：输入权益曲线，输出 Sharpe、Sortino、Calmar、最大回撤、水下时间、收益分布直方图。
6. 生成 event_driven_backtest_engine 模块：输入策略逻辑和事件流，输出按事件循环处理的回测结果，支持向量化回测对比。
7. 补全 A 股历史成分股、退市数据、复权因子（如 Wind、CSMAR），消除幸存者偏差。
8. 继续优化和扩展现有策略的样本外测试，避免过拟合。