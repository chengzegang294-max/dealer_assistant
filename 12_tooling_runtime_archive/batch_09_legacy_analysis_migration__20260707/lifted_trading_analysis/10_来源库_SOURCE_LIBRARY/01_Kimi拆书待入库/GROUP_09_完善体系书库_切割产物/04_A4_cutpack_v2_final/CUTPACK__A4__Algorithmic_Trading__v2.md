### MATERIAL_CARD
- title: Algorithmic Trading
- author_or_source: Ernest P. Chan
- material_type: 书
- domain_tags: [算法交易, 均值回归, 动量策略, 配对交易, 回测陷阱, 风险管理, 凯利公式]
- file_scope: 全书 225 页（Chapter 1-8 + 附录）

### ROUTING_DECISION
- current_repo_role: data_engineering_guard / state_template_shell
- is_worth_deep_cut_now: yes
- deep_cut_priority: P1
- reason: 本书侧重具体策略类别（均值回归、动量、配对交易、新闻驱动）和回测执行一体化。比 Quantitative Trading 更偏策略实现，适合直接转化为 strategy_evaluation_shell 和 execution_guard。

### CONTENT_CLUSTERS
- cluster_name: 回测与执行基础
  what_it_is: 回测的重要性、统计显著性（假设检验、蒙特卡洛）、何时不应回测、平台选择（编程能力、资产类别支持、复杂事件处理）。
  keep_level: 高
  repo_mapping: data_engineering_guard
- cluster_name: 回测常见陷阱
  what_it_is: 前视偏差、数据迁就偏差、股票拆分/分红调整、幸存者偏差、主价/合并价差异、外汇报价场所依赖、卖空限制、期货连续合约、收盘价/结算价差异。
  keep_level: 高
  repo_mapping: data_engineering_guard
- cluster_name: 均值回归基础
  what_it_is: 均值回归的自然现象类比、ADF 检验、Hurst 指数、方差比率检验、半衰期、线性均值回归策略。平稳性检验是均值回归策略的前提。
  keep_level: 高
  repo_mapping: state_template_shell / data_engineering_guard
- cluster_name: 协整与配对交易
  what_it_is: 协整 ADF 检验（CADF）、Johansen 检验、价格价差/对数价差/比率、线性组合上的均值回归交易。股票对、ETF 对、外汇交叉汇率、期货跨期套利的实现细节。
  keep_level: 高
  repo_mapping: state_template_shell
- cluster_name: 均值回归策略实现
  what_it_is: 布林带、逐步建仓（scaling-in）、卡尔曼滤波作为动态线性回归（估计对冲比率和平价）、卡尔曼滤波作为做市模型。数据错误对均值回归策略的致命影响。
  keep_level: 中
  repo_mapping: state_template_shell
- cluster_name: 股票与 ETF 均值回归
  what_it_is: 短期/季节性均值回归、指数套利（股票 vs 期货/ETF）、截面均值回归（横截面排序）。卖空限制对股票配对的影响。ETF 配对和三元组优于股票配对。
  keep_level: 中
  repo_mapping: state_template_shell
- cluster_name: 外汇与期货均值回归
  what_it_is: 期货展期收益（roll returns）、现货收益与展期收益分离、正向/反向市场（contango/backwardation）、期货跨期套利、波动率期货 vs 股指期货。外汇交叉汇率的协整与点值标准化。
  keep_level: 中
  repo_mapping: state_template_shell
- cluster_name: 日间动量策略
  what_it_is: 动量的四大成因：展期收益持续性、信息扩散慢、基金强制买卖、高频操纵。时间序列动量与截面动量。期货（跨期、跨品种）和股票动量策略。长期动量持有导致的统计显著性下降和危机后表现不佳。
  keep_level: 中
  repo_mapping: state_template_shell
- cluster_name: 日内动量策略
  what_it_is: 触发止损导致的动量（突破策略）、开盘跳空、盘中支撑/阻力位突破、新闻事件（盈利公告、分析师推荐）、宏观新闻、杠杆 ETF 每日再平衡、开盘/收盘竞价失衡。日内动量不受长期动量弱点影响。
  keep_level: 中
  repo_mapping: state_template_shell
- cluster_name: 新闻驱动动量
  what_it_is: 新闻情绪作为基本面因子、盈利公告后漂移（PEAD）、跨资产类别信息扩散（如期货领先股票）、延迟反应（隔夜跳空、开盘缺口）。
  keep_level: 低
  repo_mapping: source_library_only
- cluster_name: 风险管理
  what_it_is: 最优杠杆（凯利公式、历史增长率优化）、最大回撤与最优杠杆、固定比例投资组合保险（CPPI）、止损的困境、风险指标（VIX、信用利差等）。半凯利下注。基于模拟收益优化预期增长率。
  keep_level: 高
  repo_mapping: data_engineering_guard / state_template_shell

### QUANTIZATION_TABLE
| concept | type | minimal_definition | observable_proxy | min_data_requirement | confirmation_timing | quant_status | repo_target | leakage_risk | notes |
|---|---|---|---|---|---|---|---|---|---|
| ADF Test for Stationarity | risk_guard | 检验价格序列是否存在单位根，即是否平稳 | ADF 检验统计量 < 临界值（如 1%）则拒绝单位根假设；或报告 p-value | OHLCV | 回测筛选阶段 | proxy_quantizable_now | data_engineering_guard | low | 需区分时间序列 ADF 与配对价差的 CADF |
| Hurst Exponent | state | 衡量时间序列的长期记忆性：H < 0.5 均值回归，H = 0.5 随机游走，H > 0.5 趋势 | R/S 分析或 AR(1) 回归估计 H；或在滚动窗口上估计 | OHLCV | 回测筛选阶段 | proxy_quantizable_now | state_template_shell | low | 对样本长度敏感；短期窗口估计方差大 |
| Variance Ratio Test | risk_guard | 检验收益率序列是否服从随机游走（方差比率 = 1） | VR(k) = Var(r_t^{(k)})/(k * Var(r_t))；若 VR < 1 则存在均值回归 | OHLCV | 回测筛选阶段 | proxy_quantizable_now | data_engineering_guard | low | 需选择适当的聚合周期 k |
| Half-Life of Mean Reversion | feature | 价格偏离均值后恢复至一半所需的时间（以周期计） | 对扩散方程 dz_t = -theta(z_t - mu)dt + sigma dW_t 的 theta 估计；半衰期 = ln(2)/theta | OHLCV | 回测筛选阶段 | proxy_quantizable_now | state_template_shell | low | 半衰期过长（如 > 1 年）则策略不可交易 |
| Cointegrated ADF (CADF) | risk_guard | 检验两个价格序列的线性组合是否平稳 | 回归 spread = P_1 - h * P_2 的残差 ADF 检验；或使用 Engle-Granger 两步法 | OHLCV | 回测筛选阶段 | proxy_quantizable_now | state_template_shell | low | 需估计对冲比率 h；在滚动窗口上重新估计 |
| Johansen Cointegration Test | risk_guard | 检验多资产系统中协整关系的秩（多变量） | Johansen 迹检验统计量；最大特征值检验；协整秩 r > 0 则存在协整 | OHLCV | 回测筛选阶段 | proxy_quantizable_now | state_template_shell | low | 适用于三元组或更多资产的配对交易 |
| Roll Returns / Contango Signal | feature | 期货展期收益（近月 vs 远月价差）的符号和持续性 | 连续合约的滚动收益率 = (P_{near} - P_{far})/P_{near}；符号持续性检验 | OHLCV futures | 每月换月时 | proxy_quantizable_now | state_template_shell | med | 不同商品/股指的展期结构差异大；需逐个品种验证 |
| Intraday Momentum Breakout | execution_rule | 突破支撑/阻力位或触发止损后的动量延续 | 开盘跳空幅度、前日高点/低点突破、日内 VWAP 偏离度；信号触发后持仓至收盘 | OHLCV intraday | 日内信号触发时 | needs_extra_data | state_template_shell | med | 需要分钟级数据；A 股 T+1 限制下日内平仓受限 |
| PEAD (Post-Earnings Announcement Drift) | feature | 盈利公告后的价格漂移方向与幅度 | 公告后 1-60 天累计异常收益 vs 预期 EPS 偏离； drift 方向与超预期符号一致 | OHLCV + earnings | 每季度财报季 | proxy_quantizable_now | object_definition_shell | high | A 股业绩预告制度与美股不同；需适配公告时点 |
| Leveraged ETF Rebalancing Momentum | feature | 杠杆 ETF 每日再平衡对标的资产产生的日内动量 | 杠杆 ETF 目标倍数（2x/3x）与标的日收益率方向；再平衡交易量估计 | OHLCV + ETF holdings | 每日开盘 | proxy_quantizable_now | state_template_shell | low | 主要适用于美股杠杆 ETF；A 股缺乏杠杆 ETF |
| Kelly Optimal Leverage | execution_rule | 基于历史收益率均值与方差最大化长期复合增长率的最优杠杆 | f* = (mu - r)/sigma^2；半凯利 f = f*/2；或通过模拟收益优化预期增长率 | OHLCV | 回测后 | proxy_quantizable_now | state_template_shell | high | A 股两融上限约 2x；Kelly 建议可能超出监管限制 |
| Maximum Drawdown Constraint | risk_guard | 最大回撤与最优杠杆之间的权衡：高杠杆导致高 MDD | 在历史数据上模拟不同杠杆下的 MDD 分布；设定 MDD 上限反推最大杠杆 | OHLCV | 回测后 | proxy_quantizable_now | data_engineering_guard | low | 需考虑路径依赖：相同均值方差的不同序列 MDD 可能差异很大 |
| CPPI (Constant Proportion Portfolio Insurance) | execution_rule | 在风险资产和无风险资产之间动态分配，保证最低净值 | m_t = max(0, m * (V_t - F_t)/V_t)，其中 F_t 为 floor，m 为乘数 | OHLCV | 实时 | shell_only | state_template_shell | med | 跳空风险可能导致 CPPI 在极端情况下无法保 floor |
| News Sentiment Momentum | feature | 新闻/情绪对价格的动量影响 | 新闻事件时间戳后 1-60 分钟收益率方向与情绪得分符号；RavenPack 或 Recorded Future 数据 | OHLCV + news | 事件触发时 | needs_extra_data | source_library_only | high | 中文新闻情绪需单独构建词典；A 股信息扩散速度快 |

### RETAINED_EXCERPTS
- excerpt_id: EX-01
  source_hint: Chapter 1: Backtesting and Automated Execution / Importance
  quote: >
    If one blithely goes ahead and backtests a strategy without taking care to avoid these pitfalls, the backtesting will be useless. Or worse—it will be misleading and may cause significant financial losses. Since backtesting typically involves the computation of an expected return and other statistical measures of the performance of a strategy, it is reasonable to question the statistical significance of these numbers. We will discuss various ways of estimating statistical significance using the methodologies of hypothesis testing and Monte Carlo simulations. In general, the more round trip trades there are in the backtest, the higher will be the statistical significance. But even if a backtest is done correctly without pitfalls and with high statistical significance, it doesn’t necessarily mean that it is predictive of future returns. Regime shifts can spoil everything, and a few important historical examples will be highlighted.
  why_kept: 回测核心警示：即使回测无误且统计显著，也不等于对未来有预测力；regime 切换会毁掉一切。保留作为回测模块的定性约束。
  quant_link: Statistical Significance of Backtesting

- excerpt_id: EX-02
  source_hint: Chapter 1: Common Pitfalls / Data-Snooping
  quote: >
    Data-Snooping Bias and the Beauty of Linearity: The more strategies we test on the same data, the more likely we are to find a profitable strategy that is actually just a fluke. The fact that a strategy has a linear response to some parameter does not mean that it is not overfit. In fact, linear strategies are often the most overfit because they are the simplest to optimize.
  why_kept: 数据迁就偏差：测试策略越多，越可能找到伪盈利策略。线性策略因最简单反而最易过拟合。保留作为策略筛选的数量约束。
  quant_link: Data-Snooping Bias

- excerpt_id: EX-03
  source_hint: Chapter 2: The Basics of Mean Reversion / Stationarity
  quote: >
    Is mean reversion also prevalent in financial price series? If so, our lives as traders would be very simple and profitable! All we need to do is to buy low (when the price is below the mean), wait for reversion to the mean price, and then sell at this higher price, all day long. Alas, most price series are not mean reverting, but are geometric random walks. The returns, not the prices, are the ones that usually randomly distribute around a mean of zero. Unfortunately, we cannot trade on the mean reversion of returns. Those few price series that are found to be mean reverting are called stationary, and in this chapter we will describe the statistical tests (ADF test and the Hurst exponent and Variance Ratio test) for stationarity.
  why_kept: 均值回归的核心前提：价格序列必须平稳，而收益率序列虽围绕均值分布但无法交易。保留作为均值回归策略筛选的理论基础。
  quant_link: ADF Test for Stationarity / Hurst Exponent / Variance Ratio Test

- excerpt_id: EX-04
  source_hint: Chapter 2: Cointegration / CADF
  quote: >
    The basic idea in forming a stationary portfolio of foreign currencies is very similar to the trading of pairs of stocks: we need to find two or more price series that form a stationary portfolio, or equivalently, two or more price series that are cointegrated. We can use the CADF test or the Johansen test to determine cointegration. For two price series, the CADF test is usually sufficient; for three or more price series, the Johansen test is more appropriate.
  why_kept: 协整检验的选择标准：两序列用 CADF，三序列及以上用 Johansen。保留作为配对交易对象筛选的硬性规则。
  quant_link: Cointegrated ADF (CADF) / Johansen Cointegration Test

- excerpt_id: EX-05
  source_hint: Chapter 3: Implementing Mean Reversion / Bollinger Bands
  quote: >
    In practice, though, we should remember that we don’t necessarily need true stationarity or cointegration in order to implement a successful mean reversion strategy: If we are clever, we can capture short-term or seasonal mean reversion, and liquidate our positions before the prices go to their next equilibrium level. Conversely, not all stationary series will lead to great profits—not if their half-life for mean reversion is 10 years long.
  why_kept: 均值回归策略的实践洞察：不必追求绝对平稳，可捕捉短期/季节性均值回归；但半衰期过长（如10年）的平稳序列也无交易价值。保留作为策略时间尺度筛选的依据。
  quant_link: Half-Life of Mean Reversion

- excerpt_id: EX-06
  source_hint: Chapter 4: Mean Reversion of Stocks and ETFs / Short-term
  quote: >
    In the short term, most stocks exhibit mean-reverting properties under normal circumstances. (Normal circumstance means there isn’t any news on the stock, a topic that is taken up in Chapter 7.) This is despite the fact that stock prices follow geometric random walks over the long term. We will build a strategy to exploit this short-term, or seasonal, mean reversion.
  why_kept: 短期均值回归的隐含条件：无新闻冲击的“正常”环境下股票短期呈均值回归。保留作为 regime 检测与新闻过滤的定性输入。
  quant_link: Intraday Momentum Breakout / News Sentiment Momentum

- excerpt_id: EX-07
  source_hint: Chapter 6: Interday Momentum Strategies / Causes
  quote: >
    There are four main causes of momentum: 1. For futures, the persistence of roll returns, especially of their signs. 2. The slow diffusion, analysis, and acceptance of new information. 3. The forced sales or purchases of assets of various type of funds. 4. Market manipulation by high-frequency traders.
  why_kept: 动量的四大成因：展期收益、信息扩散、基金强制交易、高频操纵。保留作为动量策略分类与归因的框架。
  quant_link: Roll Returns / Contango Signal / PEAD / Leveraged ETF Rebalancing Momentum

- excerpt_id: EX-08
  source_hint: Chapter 6: Interday Momentum / Weakness
  quote: >
    The reason for this distinction is that many interday momentum strategies suffer from a recently discovered weakness, while intraday momentum strategies are less affected by it. I will highlight this weakness in this chapter, and also discuss the very different profit potentials of time series momentum and cross-sectional momentum.
  why_kept: 日间动量 vs 日内动量的关键区别：日间动量存在近期发现的弱点（长期持有导致统计显著性下降和危机后表现不佳），而日内动量受影响较小。保留作为时间尺度选择的依据。
  quant_link: Intraday Momentum Breakout

- excerpt_id: EX-09
  source_hint: Chapter 7: Intraday Momentum / Breakout
  quote: >
    There is an additional cause of momentum that is mainly applicable to the short time frame: the triggering of stops. Such triggers often lead to the so-called breakout strategies. We will see one example that involves an entry at the market open, and another one that involves intraday entry at various support or resistance levels.
  why_kept: 日内动量的特殊成因：止损触发导致的动量（突破策略）。开盘跳空和盘中支撑/阻力突破是典型触发场景。保留作为日内动量信号的定性来源。
  quant_link: Intraday Momentum Breakout

- excerpt_id: EX-10
  source_hint: Chapter 8: Risk Management / Kelly
  quote: >
    It is easy to say that we need to be prudent when using leverage, but much harder to decide what constitutes a prudent, or optimal, leverage for a particular strategy or portfolio because, obviously, if we set leverage to zero, we will suffer no risks but will generate no returns, either. To some portfolio managers, especially those who are managing their own money and answerable to no one but themselves, the sole goal of trading is the maximization of long-term equity growth. The Kelly formula is the mathematical solution to this optimization problem.
  why_kept: 凯利公式的优化目标：最大化长期权益增长。对于自负盈亏的交易者，这是唯一目标。保留作为最优杠杆决策的理论基础。
  quant_link: Kelly Optimal Leverage / Maximum Drawdown Constraint

- excerpt_id: EX-11
  source_hint: Chapter 8: Risk Management / Stop Loss
  quote: >
    One obvious way of accomplishing this is the use of stop loss, but it is often problematic. The other way is constant proportion portfolio insurance, which tries to maximize the upside of the account in addition to preventing large drawdowns. Both will be discussed here. Finally, it may be wise to avoid trading altogether during times when the risk of loss is high. We will investigate whether the use of certain leading indicators of risk is an effective loss-avoidance technique.
  why_kept: 风险管理的三大支柱：止损（但有问题）、CPPI（保 floor 同时追求上行）、风险回避（使用领先指标）。保留作为风险管理模块的定性框架。
  quant_link: CPPI / Maximum Drawdown Constraint

### FORMULAS_AND_ALGOS

**1. ADF Test for Stationarity (Chapter 2)**
公式：ADF 检验统计量，若小于临界值（如 1% 显著性水平）则拒绝单位根假设，序列平稳。Hurst 指数 H 通过 R/S 分析或 AR(1) 回归估计：H < 0.5 均值回归，H = 0.5 随机游走，H > 0.5 趋势。方差比率检验 VR(k) = Var(r^{(k)})/(k * Var(r))，若 VR < 1 则存在均值回归。
- 适用：均值回归策略的对象筛选
- 失效条件：检验窗口选择不当；A 股政策突变导致非平稳性假设本身不成立

**2. Half-Life of Mean Reversion (Chapter 2)**
公式：对扩散方程 dz_t = -theta(z_t - mu)dt + sigma dW_t 估计 theta；半衰期 = ln(2)/theta。若半衰期过长（如超过一年），则策略不具备实际交易价值。
- 适用：评估均值回归策略的可交易时间尺度
- 失效条件：theta 估计对样本长度敏感；在滚动窗口上需定期重估计

**3. Cointegrated ADF Test (Chapter 2)**
公式：对价格序列 P_1, P_2 做回归 P_1 = alpha + h * P_2 + epsilon；对残差 epsilon 做 ADF 检验。若拒绝单位根，则两序列协整。对冲比率 h 在滚动窗口上重新估计。
- 适用：两资产配对交易（股票对、ETF 对、外汇对）
- 失效条件：若 h 长期不滚动更新，regime 切换后对冲比率失效；A 股停牌导致窗口缺失

**4. Johansen Cointegration Test (Chapter 2)**
公式：多资产系统的协整秩检验。迹检验统计量 lambda_trace = -T * ln(1 - lambda_i)；最大特征值检验 lambda_max = -T * ln(1 - lambda_{r+1})。协整秩 r > 0 则存在协整关系。
- 适用：三资产及以上配对交易（如 ETF 三元组）
- 失效条件：A 股停牌导致面板不平衡；需处理缺失值

**5. Roll Returns / Contango Signal (Chapter 5)**
公式：滚动收益率 = (P_{near} - P_{far}) / P_{near}。若滚动收益率持续为正（backwardation），则多头展期收益；若持续为负（contango），则空头展期收益。符号持续性检验可判断时间序列动量。
- 适用：期货时间序列动量和跨期套利
- 失效条件：不同品种的展期结构差异大；需逐个品种验证；换月时点选择影响计算

**6. Kelly Optimal Leverage (Chapter 8)**
公式：f* = (mu - r) / sigma^2，其中 mu 为策略预期年化收益率，r 为无风险利率，sigma^2 为年化收益率方差。半凯利下注 f = f* / 2。也可通过模拟历史收益率序列优化预期增长率。
- 适用：确定最优杠杆或资金分配比例
- 失效条件：A 股两融杠杆上限约 2x，Kelly 建议可能超出监管限制；需截断

**7. CPPI (Constant Proportion Portfolio Insurance) (Chapter 8)**
公式：风险资产配置比例 m_t = max(0, m * (V_t - F_t) / V_t)，其中 V_t 为当前组合价值，F_t 为 floor 价值，m 为乘数。无风险资产分配比例为 1 - m_t。乘数 m 越大，追求上行越积极，但保 floor 能力越弱。
- 适用：保 floor 同时追求上行的动态资产配置
- 失效条件：极端跳空可能导致 CPPI 在再平衡前跌破 floor；A 股涨跌停可能提供部分保护但流动性枯竭时失效

### NOT_QUANT_YET
1. **新闻情绪动量（News Sentiment）** - 需要 RavenPack/Recorded Future 等付费数据或自建中文新闻情绪词典；A 股信息扩散速度快，套利窗口极短；标 needs_extra_data。
2. **杠杆 ETF 再平衡动量** - 主要适用于美股 2x/3x ETF；A 股缺乏杠杆 ETF；标 source_library_only。
3. **高频日内止损触发动量** - 需要 tick/Level-2 数据识别止损触发链；A 股 T+1 限制下日内策略受限；标 needs_extra_data。
4. **跨资产类别信息扩散（期货领先股票）** - 需要多资产类别同步数据与精确时间戳；A 股期货与现货的领先滞后关系需单独验证；标 future_bucket。

### NEXT_ACTION
1. 生成 stationarity_screener 模块：输入 OHLCV，输出 ADF/Hurst/VR 检验结果和半衰期，标记可交易的均值回归对象。
2. 生成 cointegration_pair_selector 模块：输入多资产价格序列，输出 CADF/Johansen 协整检验结果、对冲比率、半衰期，筛选配对交易候选。
3. 生成 momentum_cause_classifier 模块：输入期货展期收益、新闻事件、ETF 再平衡数据，分类动量成因并匹配对应策略。
4. 生成 kelly_cppi_allocator 模块：输入策略历史收益和当前组合价值，输出 Kelly 最优杠杆、半凯利建议、CPPI 动态权重。
5. 生成 backtest_pitfall_guard 模块：输入回测参数和数据源，检查前视偏差、幸存者偏差、分红/拆分调整、主价/合并价差异、卖空限制。
6. 补全 A 股期货连续合约数据（如 Wind、同花顺 iFinD），支撑展期收益和跨期套利计算。
7. 继续切割 Successful Algorithmic Trading (Halls-Moore) 和 Advances in Financial Machine Learning (López de Prado)。
