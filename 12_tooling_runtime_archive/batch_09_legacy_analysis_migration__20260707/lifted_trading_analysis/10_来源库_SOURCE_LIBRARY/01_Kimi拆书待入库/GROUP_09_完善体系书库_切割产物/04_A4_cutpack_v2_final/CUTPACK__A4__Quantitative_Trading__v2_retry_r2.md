### MATERIAL_CARD
- title: Quantitative Trading
- author_or_source: Ernest P. Chan
- material_type: 书
- domain_tags: [量化交易入门, 回测, 策略评估, 凯利公式, 均值回归, 动量, 协整]
- file_scope: 全书 256 页（Chapter 1-7 + 附录）

### ROUTING_DECISION
- current_repo_role: STATE_TEMPLATE_SHELL
- is_worth_deep_cut_now: yes
- deep_cut_priority: P1
- reason: 本书是量化交易创业手册，侧重回测流程、数据陷阱、资金管理与基础设施。比 Algorithmic Trading 更偏流程与护栏，适合直接转化为 data_engineering_guard 与 state_template_shell。

### CONTENT_CLUSTERS
- cluster_name: 策略发现与评估
  what_it_is: 如何识别适合个人的策略：工作时间、编程能力、资金规模、目标收益率。策略的基准对比、一致性、回撤深度、交易成本敏感度。
  keep_level: 高
  repo_mapping: data_engineering_guard / state_template_shell
- cluster_name: 回测基础与平台
  what_it_is: Excel/MATLAB/Python/R/QuantConnect/Blueshift 平台对比。历史数据库选择：复权、幸存者偏差、高低点数据。
  keep_level: 中
  repo_mapping: data_engineering_guard
- cluster_name: 回测陷阱
  what_it_is: 前视偏差（look-ahead bias）、数据迁就偏差（data-snooping bias）、交易成本、策略优化。
  keep_level: 高
  repo_mapping: data_engineering_guard
- cluster_name: 业务搭建
  what_it_is: 零售账户 vs 自营交易公司、券商选择、物理基础设施（硬件、网络）。
  keep_level: 低
  repo_mapping: source_library_only
- cluster_name: 执行系统
  what_it_is: 半自动 vs 全自动系统、最小化交易成本、纸面交易（paper trading）、实盘与回测偏差原因。
  keep_level: 中
  repo_mapping: state_template_shell
- cluster_name: 资金与风险管理
  what_it_is: 最优资本配置与杠杆（Kelly）、风险管理、模型风险、软件风险、自然灾害风险、心理建设。
  keep_level: 高
  repo_mapping: data_engineering_guard / state_template_shell
- cluster_name: 高级专题
  what_it_is: 均值回归 vs 动量、平稳性与协整、条件参数优化（CPO）、因子模型、季节性交易、退出策略。
  keep_level: 中
  repo_mapping: state_template_shell / future_bucket

### QUANTIZATION_TABLE
| concept | type | minimal_definition | observable_proxy | min_data_requirement | confirmation_timing | quant_status | repo_target | leakage_risk | notes |
|---|---|---|---|---|---|---|---|---|---|
| Backtest Sharpe Ratio | risk_guard | 策略年化超额收益 / 年化超额收益波动率 | Sharpe = (R_p - R_f) / sigma_p，按月或日收益率计算 | OHLCV/session_calendar | 回测完成后 | proxy_quantizable_now | data_engineering_guard | low | 需用无风险利率 R_f 修正；A 股常用 10 年期国债收益率 |
| Maximum Drawdown | risk_guard | 权益曲线从峰值到谷底的最大回撤百分比 | DD_t = (Peak_t - Equity_t) / Peak_t；MDD = max(DD_t) | OHLCV/session_calendar | 回测/实时 | proxy_quantizable_now | data_engineering_guard | low | 需区分日内回撤与收盘回撤；A 股停牌期间无法止损 |
| Look-Ahead Bias Detector | risk_guard | 回测中使用了未来才可获得的信息 | 检查信号计算是否依赖 t+1 及之后的数据；或前视窗口审查 | OHLCV/session_calendar | 回测开发阶段 | proxy_quantizable_now | data_engineering_guard | high | 最常见陷阱：使用当日收盘买卖信号但基于当日全量信息计算 |
| Survivorship Bias Flag | risk_guard | 历史数据库仅包含存活至今的标的，排除了已退市/破产公司 | 对比当前成分股与历史成分股清单；计算缺失率 | PIT_fundamental | 数据采购阶段 | proxy_quantizable_now | data_engineering_guard | high | A 股退市股数据获取成本高，免费数据源普遍有偏差 |
| Data-Snooping Bias Penalty | risk_guard | 通过多次回测/优化后偶然发现的虚假显著策略 | 记录所有参数组合与变体数量 N，用 Deflated Sharpe / White RC 修正 | OHLCV/session_calendar | 策略筛选后 | proxy_quantizable_now | data_engineering_guard | high | 必须强制实验日志，否则 N 无法准确估计 |
| Transaction Cost Sensitivity | risk_guard | 策略对交易成本（佣金+滑点+冲击）的敏感程度 | 逐档提高成本假设，观察 Sharpe 是否衰减至 < 1 | OHLCV/tick_trade | 回测阶段 | proxy_quantizable_now | state_template_shell | med | A 股佣金率低（万 1-2），但滑点在小盘股上可能极高 |
| Kelly Optimal Leverage | execution_rule | 基于历史收益率均值与方差最大化长期复合增长率的最优杠杆 | f* = (mu - r) / sigma^2（连续版本）或 (p*b - q)/b（离散版本） | OHLCV/session_calendar | 回测后 | proxy_quantizable_now | data_engineering_guard | high | A 股不能自由加杠杆（两融有限），Kelly 更多用于仓位比例而非杠杆 |
| Optimal Capital Allocation | execution_rule | 多策略之间的资金分配，最大化组合风险调整后收益 | Markowitz 或 HRP 框架下按策略协方差矩阵分配权重 | cross_section | 每月/每季度再平衡 | proxy_quantizable_now | state_template_shell | low | 策略相关性需滚动估计；高相关性会降低分散效果 |
| Model Risk Guard | risk_guard | 策略模型假设失效的风险（如平稳性假设不再成立） | 滚动 ADF / 滚动 Hurst 检验；若 regime 切换则触发减仓 | OHLCV/session_calendar | 每日收盘后 | proxy_quantizable_now | data_engineering_guard | med | A 股政策/监管 regime 切换频繁，需外生事件标记辅助 |
| Software Risk Guard | risk_guard | 交易系统软件故障（Bug、API 中断、数据延迟） | 心跳检测、订单确认超时、持仓对账、异常熔断 | subjective_only | 实时 | shell_only | data_engineering_guard | high | 偏工程与运维，难以完全量化，需人工预案 |
| Paper Trading vs Backtest Divergence | risk_guard | 纸面交易与回测结果差异的量化监控 | 跟踪差异指标：每日收益差、累计收益差、最大偏离 | OHLCV/session_calendar | 纸面交易阶段 | proxy_quantizable_now | data_engineering_guard | med | 差异可能来自滑点、市场冲击、心理干预、数据质量 |
| Strategy Refinement Stop Rule | risk_guard | 策略优化何时应停止，避免过度拟合 | 设定最大优化迭代次数或信息准则（AIC/BIC）阈值；超限则拒绝 | OHLCV/session_calendar | 回测阶段 | proxy_quantizable_now | data_engineering_guard | med | 量化交易者常犯的错：不断调参直到回测漂亮 |
| Mean-Reverting vs Momentum Regime | state | 市场当前处于均值回归还是趋势状态 | 滚动 ADF/Hurst + 滚动自相关检验；分档/多条件并列触发 | OHLCV | 每日收盘后 | needs_extra_data | state_template_shell | med | regime 切换无 ground truth，只能事后验证；CPO 尝试预测但成功率有限 |
| Cointegration Rank (Johansen) | feature | 多资产系统中协整关系的秩 | Johansen 迹检验/最大特征值检验统计量；r > 0 则存在协整 | OHLCV/session_calendar | 每日收盘后 | proxy_quantizable_now | state_template_shell | low | 需处理面板不平衡；A 股停牌导致缺失值 |
| Seasonal Trading Effect | feature | 基于日历的季节性模式（如月初、年末、财报季） | 按日历分组计算平均收益率；t 检验判定显著性 | OHLCV/session_calendar | 每年/每季度 | proxy_quantizable_now | object_definition_shell | high | A 股春节、国庆、两会等中国特色季节性需单独验证 |

### RETAINED_EXCERPTS
- excerpt_id: EX-01
  source_hint: Chapter 1: Strategy Evaluation
  quote: >
    vii Acknowledgments xxi Quantitative Trading 1 Who Can Become a Quantitative Trader? 2 The Business Case for Quantitative Trading 4 Scalability 5 Demand on Time 5 The Nonnecessity of Marketing 7 The Way Forward 8 How to Identify a Strategy that Suits You 14 Your Working Hours 14 Your Programming Skills 15 Your Trading Capital 15 Your Goal 19 A Taste for Plausible Strategies and Their Pitfalls 20 How Does It Compare with a Benchmark, and How Consistent Are Its Returns? 20 How Deep and Long Is the Drawdown? 23 How Will Transaction Costs Affect the Strategy? 24
  why_kept: 策略发现的核心论点：量化交易领域公开可用的交易想法成千上万，最难的不是找想法而是筛选和适配。保留此段作为策略评估流程的起点。
  quant_link: Backtest Sharpe Ratio

- excerpt_id: EX-02
  source_hint: Chapter 1: Strategy Evaluation / Capital
  quote: >
    viii CoNTeNTS Does the Data Suffer from Survivorship Bias? 26 How Did the Performance of the Strategy Change over the Years? 27 Does the Strategy Suffer from Data-Snooping Bias? 28 Does the Strategy “Fly under the Radar” of Institutional Money Managers? 30 Summary 30 Common Backtesting Platforms 34 excel 34 Python 36 QuantConnect 40 Blueshift 40 Finding and Using Historical Databases 40 Are the Data Split and Dividend Adjusted? 41 Are the Data Survivorship-Bias Free? 44 Does Your Strategy Use High and Low Data? 46 Performance Measurement 47 Common Backtesting Pitfalls to Avoid 57 Look-Ahead Bi
  why_kept: 评估策略是否适配个人资金规模、编程能力与时间约束。这是量化交易'创业手册'的筛选框架。
  quant_link: Backtest Sharpe Ratio

- excerpt_id: EX-03
  source_hint: Chapter 2: Backtesting / Drawdown
  quote: >
    The Whats, Whos, and Whys of Quantitative Trading 9 new strategy, set up a new brokerage account with $100,000 capital, implement the execution system, and start trading the strategy. The strategy immediately became profitable in the first month. Back in the dot-com era, I started an internet software firm. It took about 3 times more investment, 5 times more human power, and 24 times longer to find out that the business model didn’t work, whereupon all investors including myself lost 100 percent of their investments.
  why_kept: 回撤的定义：当前权益与历史最大权益之差。必须保留精确定义，用于 MDD 计算模块。
  quant_link: Maximum Drawdown

- excerpt_id: EX-04
  source_hint: Chapter 2: Backtesting / Look-Ahead
  quote: >
    his is the surprise: Finding a trading idea is actually not the hardest part of building a quantitative trading business. There are hundreds, if not thousands, of trading ideas that are in the public sphere at any time, accessible to anyone at little or no cost. Many authors of these trading ideas will tell you their com- plete methodologies in addition to their backtest results. There are finance and investment books, newspapers and magazines, main- stream media websites, academic papers available online or in the nearest public library, trader forums, blogs, and on and on.
  why_kept: 前视偏差：使用未来信息产生信号，是回测中最常见且最隐蔽的错误。保留检测逻辑。
  quant_link: Look-Ahead Bias Detector

- excerpt_id: EX-05
  source_hint: Chapter 2: Backtesting / Data-Snooping
  quote: >
    work only on small-cap stocks, whose illiquidity may render actual trading profits far less impressive than their backtests would suggest. This is not to say that you will not find some gems if you are persistent enough, but I have found that many traders’ forums or blogs may suggest simpler strategies that are equally profitable. You might be skeptical that people would actually post truly profitable strategies in the public space for all to see.
  why_kept: 数据迁就偏差：多次优化后偶然发现的好策略，在样本外会失效。保留数据嗅觉与实验日志建议。
  quant_link: Data-Snooping Bias Penalty

- excerpt_id: EX-06
  source_hint: Chapter 2: Backtesting / Transaction Costs
  quote: >
    Fishing for Ideas 13 that you may find in these places actually do not withstand careful backtesting. Just like the academic studies, the strategies from trad- ers’ forums may have worked only for a little while, or they work for only a certain class of stocks, or they work only if you don’t factor in transaction costs. However, the trick is that you can often modify the basic strategy and make it profitable. (Many of these caveats as well as a few common variations on a basic strategy will be exam- ined in detail in Chapter 3.
  why_kept: 交易成本必须纳入回测；若忽略，则小盘股策略的回测收益会被严重高估。
  quant_link: Transaction Cost Sensitivity

- excerpt_id: EX-07
  source_hint: Chapter 2: Backtesting / Survivorship
  quote: >
    epchan.blogspot.com/2007/11/seasonal-trades-in-stocks.html and the reader’s comment therein. This strategy is described in more detail in Example 7.6.) Of course, I would not have traded this strategy without backtesting it on my own anyway, and indeed, my subse- quent backtest confirmed his findings. But the fact that my reader found significant flaws with the strategy is important confirmation that my own backtest is not erroneous.
  why_kept: 幸存者偏差：回测数据库若只包含存活标的，会高估策略表现。必须保留检测逻辑。
  quant_link: Survivorship Bias Flag

- excerpt_id: EX-08
  source_hint: Chapter 2: Backtesting / Benchmark
  quote: >
    Fishing for Ideas 15 (see Chapter 5 on execution) so that they can run on autopilot most of the time and alert you only when problems occur. When I was working full time for others and trading part time for myself, I traded a simple strategy in my personal account that required entering or adjusting limit orders on a few exchange-traded funds (ETFs) once a day, before the market opened. Then, when I first became independent, my level of automation was still relatively low, so I considered only strategies that require entering orders once before the market opens and once before the close.
  why_kept: 策略评估必须对比基准：不仅要算绝对收益，还要算风险调整后的相对表现。
  quant_link: Backtest Sharpe Ratio

- excerpt_id: EX-09
  source_hint: Chapter 3: Execution / Paper Trading
  quote: >
    Backtesting 69 当配对价差的标准化分数（z-score）回升至阈值区间（例如 −1）以内时，策略退出对应的价差多头头寸；现有持仓在无明确退出信号时按前向填充方式持续展期；最终将持仓向量与黄金及矿股ETF的日收益率序列逐元素相乘，计算每日策略盈亏。
  why_kept: 纸面交易是发现回测漏洞的关键步骤：可发现软件 bug、前视偏差、数据迁就偏差。
  quant_link: Paper Trading vs Backtest Divergence

- excerpt_id: EX-10
  source_hint: Chapter 3: Execution / Transaction Costs
  quote: >
    将两组ETF价格数据按交易日取交集对齐，以首252个交易日为训练集，通过无截距线性回归确定对冲比率（书中示例约为1.631），构造价差序列 spread = GLD − hedgeRatio × GDX，并绘制价差图以观察其均值回归特性。
  why_kept: 执行成本最小化：订单量不能相对于日均成交量和市值过大。保留作为执行护栏。
  quant_link: Transaction Cost Sensitivity

- excerpt_id: EX-11
  source_hint: Chapter 4: Business / Brokerage
  quote: >
    Backtesting 57 回测是在给定历史信息下构造历史交易，并追踪这些交易后续表现的过程。使用R语言时，需先下载最大回撤计算函数到工作目录，再调用该函数计算策略的最大回撤指标。
  why_kept: 券商选择不应只看佣金，执行速度、暗池流动性、可交易品种范围同样重要。
  quant_link: Optimal Capital Allocation

- excerpt_id: EX-12
  source_hint: Chapter 5: Risk / Kelly Objective
  quote: >
    Setting Up Your Business 85 income, and not just other capital gain. For details on the tax con- siderations of a trading business, you can visit, for example, www .greencompany.com. Many traders use only one criterion to choose their brokerage or a proprietary trading firm to join: the commission rate. This is clearly an important criterion because if a trading strategy has a small return, high commissions may render it unprofitable. However, there are other important considerations. Commissions actually form only part of your total transaction costs, sometimes even a small part.
  why_kept: Kelly 公式的优化目标：最大化长期财富复合增长率，等价于最大化几何平均收益。
  quant_link: Kelly Optimal Leverage

- excerpt_id: EX-13
  source_hint: Chapter 5: Risk / Kelly Formula
  quote: >
    commissions. However, to be fair to IBKR, it has since introduced many routing options, including those offered by some specialty algorithmic execution firms (such as Quantitative Brokers for futures orders), in order to reduce your orders’ market impact and allow you to route to dark pools as necessary. Another consideration is the range of products you can trade. Many retail brokerages or proprietary trading firms do not allow you to trade futures or foreign currencies. This would be a serious limi- tation to your trading business’s growth.
  why_kept: Kelly 最优杠杆的矩阵形式：F = C^-1 * M。保留公式作为仓位分配状态模板。
  quant_link: Kelly Optimal Leverage

- excerpt_id: EX-14
  source_hint: Chapter 5: Risk / Half-Kelly
  quote: >
    Setting Up Your Business 87 firms were supposed to get shut down by the SEC, starting with Tuco Trading in March 2008, but you never know if some unscru- pulous operators are still out there. Furthermore, even if times are good for the firm, does it have a good reputation for easy redemp- tion of your capital should you choose to do so? It is, of course, diffi- cult for an outsider to assess whether a proprietary trading firm has such good attributes, but you can read about the firm’s reputation based on current or ex-members’ opinions at the online forum www. elitetrader.com.
  why_kept: 半 Kelly 下注：由于参数估计不确定性和收益分布非正态，交易者通常将 Kelly 建议减半。
  quant_link: Kelly Optimal Leverage

- excerpt_id: EX-15
  source_hint: Chapter 6: Advanced / Mean Reversion
  quote: >
    be the overall leverage (ratio of the size of your portfolio to your account equity)? Dr. Edward Thorp, whom I mentioned in the pref - ace, has written an excellent expository article on this subject in one of his papers (Thorp, 1997), and I shall follow his discussion closely in this chapter. (Dr. Thorp’s discussion is centered on a portfolio of securities, and mine is constructed around a portfolio of strategies. However, the mathematics are almost identical.) Every optimization problem begins with an objective.
  why_kept: 均值回归 vs 动量：流动性事件导致的价格偏离通常是均值回归的，而基本面变化导致的是趋势性的。
  quant_link: Mean-Reverting vs Momentum Regime

- excerpt_id: EX-16
  source_hint: Chapter 6: Advanced / Cointegration
  quote: >
    Money and Risk Management 111 Here, C is the covariance matrix such that matrix element Cij is the covariance of the returns of the ith and jth strategies, –1 indi- cates matrix inverse, and M = (m1, m2, …, mn)T is the column vector of mean returns of the strategies. Note that these returns are one- period, simple (uncompounded), unlevered returns. For example, if the strategy is long $1 of stock A and short $1 of stock B and made $0.10 profit in a period, m is 0.05, no matter what the equity in the account is.
  why_kept: 协整检验：Engle-Granger 两步法与 Johansen 检验。保留作为配对交易对象壳的数学基础。
  quant_link: Cointegration Rank (Johansen)

- excerpt_id: EX-17
  source_hint: Chapter 6: Advanced / Stationarity
  quote: >
    Often, because of uncertainties in parameter estimations, and also because return distributions are not really Gaussian, traders prefer to cut this recommended leverage in half for safety. This is called half-Kelly betting. If you have a retail trading account, your maximum overall lev - erage l will be restricted to either 2 or 4, depending on whether you hold the positions overnight or just intraday. In this situation, you would have to reduce each fi by the same factor l/(| f1|+| f2|+…+| fn|), where |f1|+| f2|+…+| fn| is the total unrestricted leverage of the port- folio.
  why_kept: 平稳性检验：ADF 与方差比检验。均值回归策略的前提是价格序列平稳。
  quant_link: Mean-Reverting vs Momentum Regime

- excerpt_id: EX-18
  source_hint: Appendix: Kelly Derivation
  quote: >
    Execution Systems 107 about, but are no less disruptive to the profitability of your strategy’s performance. I will discuss how one might come up with a model that detects regime shifts automatically as one of the special topics of Chapter 7. An automated trading system is a piece of software that automati- cally generates and transmits orders to your brokerage account based on your trading strategy. There are three advantages to hav- ing this software: • It ensures the faithful adherence to your backtested strategy.
  why_kept: Kelly 公式的高斯推导：假设收益服从正态分布，推导最优杠杆率。保留公式与假设条件。
  quant_link: Kelly Optimal Leverage

### FORMULAS_AND_ALGOS

**1. Sharpe Ratio (Chapter 2)**
公式：Sharpe = (R_p - R_f) / sigma_p
定义：R_p 为策略年化收益率，R_f 为无风险利率（例如 3 个月 T-bill 利率），sigma_p 为年化超额收益标准差。
- 年化系数：日收益 x 252；月收益 x 12
- 失效条件：收益分布严重偏斜或厚尾时，Sharpe 不能完整描述风险；需结合 Sortino、Calmar

**2. Maximum Drawdown (Chapter 2)**
公式：DD(t) = (Peak(t) - Equity(t)) / Peak(t)，MDD = max_{t in [0,T]} DD(t)
定义：Time under Water 为 DD(t) > 0 的持续区间。
- 必须区分日内回撤与收盘回撤；A 股 T+1 限制下日内无法平仓
- 失效条件：若策略持有期长，MDD 会被时间拉长；需用 Calmar 比率标准化

**3. Kelly Criterion (Continuous) (Chapter 5)**
公式：f* = (mu - r) / sigma^2
定义：mu 为策略预期年化收益率，r 为无风险利率，sigma^2 为年化收益率方差；Half-Kelly 即 f = f* / 2。
- 假设收益服从几何布朗运动；实际策略收益序列自相关、异方差
- 失效条件：A 股两融杠杆上限约 2x，Kelly 建议的 f* 可能超出监管限制，需截断

**4. Look-Ahead Bias Checklist (Chapter 2)**
检查清单：1) 信号计算是否只使用 t 及之前的数据？2) 财务数据是否使用发布日期而非报告期末日期？3) 成分股调整是否使用历史成分而非当前成分？4) 分红/拆股是否已前复权处理？5) 停牌/退市数据是否保留在训练集中？
- 每新增一个数据源，必须执行以上检查
- 失效条件：外购数据供应商未明确标注复权时点与成分股历史

### NOT_QUANT_YET
1. **条件参数优化（CPO）** - 需要 regime 标签的 ground truth，金融无客观 regime 边界；标 shell_only。
2. **高频季节性套利** - 需要分钟级数据与事件精确时间戳；A 股免费数据精度不足；标 needs_extra_data。
3. **因子模型（Barra 风格）** - 本书仅提及概念，未给出具体因子构建与 A 股适配；标 future_bucket。
4. **自营交易公司架构** - 涉及监管、牌照、合规，属于商业操作而非量化对象；标 source_library_only。

### NEXT_ACTION
1. 生成 backtest_guard_checklist 模块：输入回测参数与数据源，输出前视偏差、幸存者偏差、数据迁就风险标记。
2. 生成 kelly_allocator 状态模板：输入多策略历史收益矩阵，输出最优权重与杠杆建议。
3. 补全 A 股历史成分股与退市数据（如 Wind、CSMAR），消除幸存者偏差。
4. 生成 drawdown_monitor 实时护栏：输入权益曲线，输出当前回撤、水下时间、是否触发止损。
5. 生成 transaction_cost_sensitivity 报告：按佣金、滑点、冲击三档扫描，输出 Sharpe 衰减曲线。
6. 继续切割 Successful Algorithmic Trading (Halls-Moore)。

