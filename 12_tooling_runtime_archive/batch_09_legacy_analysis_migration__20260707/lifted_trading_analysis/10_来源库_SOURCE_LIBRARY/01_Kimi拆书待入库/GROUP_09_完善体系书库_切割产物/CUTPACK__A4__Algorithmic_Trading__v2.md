### MATERIAL_CARD
- title: Algorithmic Trading
- author_or_source: Ernest P. Chan
- material_type: 书
- domain_tags: [均值回归, 动量, 协整配对, 执行优化, 凯利公式, 市场冲击]
- file_scope: 全书 225 页（Chapter 1–8）

### ROUTING_DECISION
- current_repo_role: STATE_TEMPLATE_SHELL
- is_worth_deep_cut_now: yes
- deep_cut_priority: P0
- reason: 本书直接提供均值回归与动量策略的完整实现范式（ADF、Hurst、方差比、Johansen、Kalman），以及执行与风险模块。这些是可立即部署的状态模板。

### CONTENT_CLUSTERS
- cluster_name: 均值回归策略
  what_it_is: ADF、Hurst 指数、方差比检验、Bollinger Bands、Half-life 估计。用于判断序列平稳性与建仓阈值。
  keep_level: 高
  repo_mapping: state_template_shell / object_definition_shell
- cluster_name: 动量策略
  what_it_is: 时间序列动量与横截面动量、移动平均突破、日内动量。
  keep_level: 高
  repo_mapping: state_template_shell
- cluster_name: 配对交易与协整
  what_it_is: Engle-Granger 与 Johansen 检验、Kalman 滤波动态对冲比率、ETF 与股票配对。
  keep_level: 高
  repo_mapping: state_template_shell
- cluster_name: 执行优化
  what_it_is: 市场冲击模型、滑点估计、VWAP/TWAP 对比、限价单与市价单选择。
  keep_level: 中
  repo_mapping: state_template_shell
- cluster_name: 风险管理
  what_it_is: Kelly 公式最优杠杆、最大回撤控制、止损与止盈逻辑。
  keep_level: 高
  repo_mapping: data_engineering_guard / state_template_shell
- cluster_name: 回测陷阱
  what_it_is: 前视偏差、幸存者偏差、数据迁就偏差、交易成本敏感性。
  keep_level: 高
  repo_mapping: data_engineering_guard

### QUANTIZATION_TABLE
| concept | type | minimal_definition | observable_proxy | min_data_requirement | confirmation_timing | quant_status | repo_target | leakage_risk | notes |
|---|---|---|---|---|---|---|---|---|---|
| ADF Test on Spread | filter | 对价差序列进行增广迪基-富勒检验，H0 为单位根（非平稳） | ADF 统计量 < 临界值（1%）→ 拒绝 H0，判定平稳/可均值回归 | OHLCV/session_calendar | 滚动窗口更新后 | proxy_quantizable_now | state_template_shell | low | 窗口长度需覆盖至少 20 个 half-life 周期 |
| Hurst Exponent | feature | H = 0.5 为随机游走；H < 0.5 为均值回归；H > 0.5 为趋势 | Rescaled Range (R/S) 分析估计 H；或使用 rolling 方差比 | OHLCV | 每日收盘后 | proxy_quantizable_now | state_template_shell | low | 短样本估计方差大，建议至少 100 个观测点 |
| Variance Ratio Test | feature | 检验 k 期收益方差是否为单期方差的 k 倍，判断随机游走 | VR(k) = Var(r_t^k) / (k×Var(r_t^1))；偏离 1 则拒绝随机游走 | OHLCV | 每日收盘后 | proxy_quantizable_now | state_template_shell | low | 需用异方差稳健标准误修正 |
| Half-Life of Mean Reversion | feature | Ornstein-Uhlenbeck 过程中序列回归线性趋势所需时间 | 对 Δy_t = λy_{t-1} + μ + ε_t 回归，half-life = -ln(2)/λ | OHLCV | 每日收盘后 | proxy_quantizable_now | state_template_shell | low | λ 为负时才有意义；若 λ>0 则发散，不适合均值回归 |
| Bollinger Bands Entry | execution_rule | 价格触及下轨（μ - kσ）做多，触及上轨（μ + kσ）做空 | rolling z-score = (price - rolling_mean) / rolling_std；|z| > k 触发 | OHLCV | 实时或收盘 | proxy_quantizable_now | state_template_shell | med | k 通常取 1~2；需考虑跳空导致的 z-score 突变 |
| Johansen Cointegration Test | filter | 多变量协整检验，判定多个资产是否存在长期均衡关系 | 最大特征值统计量 > 临界值 → 存在 r 个协整向量 | OHLCV/session_calendar | 每日收盘后 | proxy_quantizable_now | state_template_shell | low | A 股多因子配对需处理停牌导致的不平衡面板 |
| Kalman Filter Hedge Ratio | object | 动态估计配对资产的时变对冲比率与价差 | 状态空间模型：观测方程为 spread = y - βx；卡尔曼增益更新 β_t | OHLCV | 实时更新 | proxy_quantizable_now | state_template_shell | med | 需调协方差矩阵 Q、R；Q 过大导致 β 过于敏感 |
| Kelly Criterion Leverage | execution_rule | 根据策略历史胜率与赔率计算最优杠杆率，最大化长期财富增长率 | f* = (p×b - q) / b，其中 p 为胜率，b 为赔率（平均盈利/平均亏损） | OHLCV/session_calendar | 回测后/滚动窗口 | proxy_quantizable_now | data_engineering_guard | high | 半凯利（Half-Kelly）更稳健；需假设收益分布稳定 |
| Market Impact Model | risk_guard | 大额订单对市场价格造成的临时性与永久性冲击 | impact = c × σ × (order_size / ADV)^γ，ADV 为日均成交额 | OHLCV/PIT_fundamental | 下单前 | needs_extra_data | state_template_shell | med | A 股需知道 ADV 与日内波动率 σ；机构单需拆分 |
| Slippage Estimate | risk_guard | 下单价与实际成交价之间的偏差，包含滑点与部分成交 | slippage = (fill_price - signal_price) / signal_price，按历史成交分布估计 | tick_trade | 回测/实时 | needs_extra_data | state_template_shell | med | A 股 level1 五档只能近似；level2 更准但需付费 |
| Stop Loss / Profit Target | execution_rule | 固定金额或百分比止损/止盈；或基于波动率（ATR）的动态止损 | 触发价 = entry_price × (1 ± s) 或 entry_price ± k×ATR | OHLCV | 实时 | proxy_quantizable_now | state_template_shell | low | 需考虑涨停/跌停导致无法成交；A 股有涨跌幅限制 |
| Moving Average Breakout | filter | 短期均线突破长期均线产生动量信号 | MA_short(t) > MA_long(t) 且前一时刻 < → 多头信号 | OHLCV | 实时/收盘 | proxy_quantizable_now | state_template_shell | low | 滞后严重；需结合波动率过滤震荡市 |
| Intraday Momentum | state | 日内开盘后趋势延续或反转模式 | 开盘后 30min 收益率方向预测当日收盘方向 | OHLCV/session_calendar | 盘中 | proxy_quantizable_now | state_template_shell | med | A 股需考虑上午/下午开盘时段不同流动性特征 |
| VWAP Execution Benchmark | risk_guard | 以成交量加权平均价为执行基准，衡量策略执行效率 | VWAP = Σ(price_i × volume_i) / Σ volume_i；对比策略成交均价 | tick_trade | 收盘后 | needs_extra_data | state_template_shell | low | A 股可用 level1 分笔汇总近似 VWAP，但精度有限 |
| Data-Snooping Bias Guard | risk_guard | 通过多次优化/筛选后策略的虚假夏普比率 | 记录所有尝试过的参数组合与策略变体，用于 Deflated Sharpe 修正 | OHLCV/session_calendar | 回测完成后 | proxy_quantizable_now | data_engineering_guard | high | 必须强制记录所有失败实验，否则 N 低估 |

### RETAINED_EXCERPTS
- excerpt_id: EX-01
  source_hint: Chapter 2: Mean Reversion
  quote: >
    d we will lay out standard techniques for trading each category of strategies, and equally important, the fundamental reasons why a strategy should work. The emphasis throughout is on simple and linear strategies, as an antidote to the overfi tting and data-snooping biases that often plague complex strategies. In the mean-reverting camp, we will discuss the multiple statistical tech- niques (augmented Dickey-Fuller [ADF] test, Hurst exponent, Variance Ra- tio test, half-life) for detecting “time
  why_kept: ADF 检验是均值回归策略的门槛条件；必须保留检验逻辑与临界值判定。
  quant_link: ADF Test on Spread

- excerpt_id: EX-02
  source_hint: Chapter 2: Mean Reversion
  quote: >
    s for trading each category of strategies, and equally important, the fundamental reasons why a strategy should work. The emphasis throughout is on simple and linear strategies, as an antidote to the overfi tting and data-snooping biases that often plague complex strategies. In the mean-reverting camp, we will discuss the multiple statistical tech- niques (augmented Dickey-Fuller [ADF] test, Hurst exponent, Variance Ra- tio test, half-life) for detecting “time series” mean reversion or stationar
  why_kept: Hurst 指数是判断序列记忆性的核心指标；H<0.5 才适合均值回归策略。
  quant_link: Hurst Exponent

- excerpt_id: EX-03
  source_hint: Chapter 2: Mean Reversion
  quote: >
    ns. (One should not confuse mean reversion of returns with anti-serial-correlation of returns, which we can defi nitely trade on. But anti-serial-correlation of returns is the same as the mean reversion of prices.) Those few price series that are found to be mean reverting are called stationary, and in this chapter we will describe the statistical tests (ADF test and the Hurst exponent and Variance Ratio test) for stationarity. There are not too many prefabricated --- PAGE 58 --- 40 ALGORITHMIC
  why_kept: 方差比检验直接验证随机游走假设；比 ADF 更直观。
  quant_link: Variance Ratio Test

- excerpt_id: EX-04
  source_hint: Chapter 2/3: Bollinger Bands
  quote: >
    cribed a simple linear mean reversion strategy that sim- ply “scales” into an asset in proportion to its price’s deviation from the mean. It is not a very practical strategy due to the constant infi nitesimal rebalancing and the demand of unlimited buying power. In this chapter, we discuss a more practical, but still simple, mean reversion strategy— --- PAGE 82 --- 64 ALGORITHMIC TRADING the Bollinger bands. W e describe variations of this technique, including the pros and cons of using multiple
  why_kept: Bollinger Band 是均值回归策略最常用的进场触发器；必须保留 z-score 计算公式。
  quant_link: Bollinger Bands Entry

- excerpt_id: EX-05
  source_hint: Chapter 4: Pairs Trading
  quote: >
    -snooping biases that often plague complex strategies. In the mean-reverting camp, we will discuss the multiple statistical tech- niques (augmented Dickey-Fuller [ADF] test, Hurst exponent, Variance Ra- tio test, half-life) for detecting “time series” mean reversion or stationarity, and for detecting cointegration of a portfolio of instruments (cointegrated augmented Dickey Fuller [CADF] test, Johansen test). Beyond the mechani- cal application of these statistical tests to time series, we striv
  why_kept: Johansen 检验是多资产配对的基础；保留特征值统计量与协整向量解释。
  quant_link: Johansen Cointegration Test

- excerpt_id: EX-06
  source_hint: Chapter 4: Pairs Trading / Dynamic Hedge
  quote: >
    to be constant. In fact, volatility is usually not constant, which means that p will not be constant either. In this circumstance, scaling-in is likely to result in a better realized Sharpe ratio if not profi ts. Another way to put it is that even though you will fi nd that scaling-in is never op- timal in-sample, you may well fi nd that it outperforms the all-in method out-of-sample. ■ Kalman Filter as Dynamic Linear Regression For a pair of truly cointegrating price series, determination of t
  why_kept: Kalman 滤波给出动态对冲比率；比静态 OLS 回归更适合非平稳协整关系。
  quant_link: Kalman Filter Hedge Ratio

- excerpt_id: EX-07
  source_hint: Chapter 6: Risk Management
  quote: >
    n Wiley & Sons, 2010. Snider, Connan Andrew , and Thomas Y oule. “Does the LIBOR Refl ect Banks’ Borrowing Costs?” 2010. Available at SSRN: http://papers .ssrn.com/sol3/papers.cfm?abstract_id=1569603. Sorensen, Bent E. Course notes on Economics. University of Houston, 2005. Available at www .uh.edu/~bsorense/coint.pdf. “The Wacky W orld of Gold.” The Economist, June 2011. Thorp, Edward. “The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market,” 1997. Available at www .EdwardOThorp
  why_kept: Kelly 公式直接给出最优杠杆；是风险管理层最重要的量化依据。
  quant_link: Kelly Criterion Leverage

- excerpt_id: EX-08
  source_hint: Chapter 5: Execution
  quote: >
    s to its mean before taking profi ts. The advantage of being able to exit whenever the price reverts by a small increment is that even if the price series is not really stationary and therefore never really reverts to its mean, we can still be profi table by constantly realizing small profi ts. An added ben- efi t is that if you are trading large sizes, scaling-in and -out will reduce the market impact of the entry and exit trades. If we want to implement scaling- in using Bollinger bands, we ca
  why_kept: 市场冲击模型决定大单拆分与执行路径；删除源文件后无法重建。
  quant_link: Market Impact Model

- excerpt_id: EX-09
  source_hint: Chapter 5/7: Backtesting / Execution
  quote: >
    acktesting a stock pair–trading strategy using either trade or quote prices is not very realistic unless you trade only 100 shares or if you include a substantial transaction cost. The same phenomenon leads to diffi culties in live execution also. If we were to submit market orders for both sides after a trading signal was triggered by the NBBO prices, we could have suff ered a substantial slippage. W e are forced to send limit orders for one side (or for both sides with small fractions of an or
  why_kept: 滑点是回测与实盘差异的主要来源；必须保留估计方法。
  quant_link: Slippage Estimate

- excerpt_id: EX-10
  source_hint: Chapter 6: Risk Management
  quote: >
    ey management in my previous book, which was built on the Kelly formula—a formula that determines the optimal lever- age and capital allocation while balancing returns versus risks. I once again cover risk and money management here, still based on the Kelly formula, but tempered with my practical experience in risk management involving black swans, constant proportion portfolio insurance, and stop losses. (U.S. Supreme Court Justice Robert H. Jackson could have been talking about the application
  why_kept: 止损/止盈逻辑是策略风险护栏的直接组成部分。
  quant_link: Stop Loss / Profit Target

- excerpt_id: EX-11
  source_hint: Chapter 3/7: Momentum
  quote: >
    8 7 6 5 4 3 2 1 --- PAGE 7 --- T o my parents, Hung Yip and Ching, and my partner, Ben --- PAGE 9 --- vii CONTENTS Preface ix CHAPTER 1 Backtesting and Automated Execution 1 CHAPTER 2 The Basics of Mean Reversion 39 CHAPTER 3 Implementing Mean Reversion Strategies 63 CHAPTER 4 Mean Reversion of Stocks and ETFs 87 CHAPTER 5 Mean Reversion of Currencies and Futures 107 CHAPTER 6 Interday Momentum Strategies 133 CHAPTER 7 Intraday Momentum Strategies 155 CHAPTER 8 Risk Management 169 Conclusion 18
  why_kept: 动量与均值回归是两种对立 regime；必须保留判断 regime 的素材。
  quant_link: Moving Average Breakout

- excerpt_id: EX-12
  source_hint: Chapter 2: Mean Reversion
  quote: >
    2. Stocks. 3. Exchange traded funds. 4. Algorithms. 5. Program trading (Securities) I. Title. HG4529.C443 2013 332.63’2042—dc23 2013008380 Printed in the United States of America. 10 9 8 7 6 5 4 3 2 1 --- PAGE 7 --- T o my parents, Hung Yip and Ching, and my partner, Ben --- PAGE 9 --- vii CONTENTS Preface ix CHAPTER 1 Backtesting and Automated Execution 1 CHAPTER 2 The Basics of Mean Reversion 39 CHAPTER 3 Implementing Mean Reversion Strategies 63 CHAPTER 4 Mean Reversion of Stocks and ETFs 87
  why_kept: 均值回归的定义与数学基础（OU 过程）必须保留。
  quant_link: Half-Life of Mean Reversion

### FORMULAS_AND_ALGOS

**1. ADF Test Statistic (Chapter 2)**
```
Δy_t = α + βt + γy_{t-1} + Σ_{i=1}^{p} δ_i Δy_{t-i} + ε_t
H0: γ = 0 (unit root, non-stationary)
H1: γ < 0 (stationary)
Test statistic = γ_hat / SE(γ_hat)
Compare with MacKinnon critical values (1%, 5%, 10%)
```
- p: lag order selected by AIC/BIC on Δy_t
- 失效条件：小样本下检验功效低；结构突变存在时 ADF 易误接受 H0

**2. Half-Life of Ornstein-Uhlenbeck (Chapter 2)**
```
Δy_t = λ y_{t-1} + μ + ε_t
half-life = -ln(2) / λ
If λ > 0: mean-fleeing (discard strategy)
If λ < 0: mean-reverting; expect to hold for ~half-life periods
```
- λ 估计有偏，小样本下需用 Vasicek MLE 修正
- 失效条件：对数价格序列若含漂移项 μ，需先去除趋势再估计 λ

**3. Kalman Filter State-Space (Chapter 4)**
```
State equation:   β_t = β_{t-1} + w_t,   w_t ~ N(0, Q)
Observation:      y_t = β_t x_t + α_t + ε_t,   ε_t ~ N(0, R)
Prediction:      β_{t|t-1} = β_{t-1|t-1}
                 P_{t|t-1} = P_{t-1|t-1} + Q
Kalman Gain:     K_t = P_{t|t-1} x_t / (x_t^2 P_{t|t-1} + R)
Update:          β_{t|t} = β_{t|t-1} + K_t (y_t - x_t β_{t|t-1})
                 P_{t|t} = (1 - K_t x_t) P_{t|t-1}
```
- Q: 过程噪声协方差；R: 观测噪声协方差；需网格搜索或 EM 估计
- 失效条件：Q 过大导致 β_t 过度波动；Q 过小则响应滞后

**4. Kelly Criterion (Chapter 6)**
```
f* = (p × b - q) / b
where p = win rate, q = 1-p, b = average win / average loss
Optimal leverage L = f* / max_drawdown_limit (if fractional Kelly)
Half-Kelly: f = f* / 2
```
- 假设收益分布不变；实际金融序列存在 regime 切换，需滚动估计 p, b
- 失效条件：若序列存在厚尾，Kelly 会低估破产概率；需加入 CVaR 约束

**5. Market Impact (Chapter 5)**
```
Temporary impact: I_temp = c1 × σ × (X / ADV)^0.6
Permanent impact: I_perm = c2 × σ × (X / ADV)^0.9
Total cost ≈ I_temp + I_perm + spread/2
where X = order size, ADV = average daily volume, σ = daily volatility
```
- c1, c2 为经验常数（Almgren-Chriss 模型）
- 失效条件：A 股涨跌停板下冲击非线性；小盘股 ADV 低导致分母失效

### NOT_QUANT_YET
1. **高频日内市场微观结构套利** — 需要逐笔成交与委托簿数据，A 股无公开免费数据源；标 needs_extra_data。
2. **跨品种统计套利（期货/外汇）** — A 股个股期货有限（仅股指期货），个股期权流动性不足；标 future_bucket。
3. **订单流 toxicity 指标（VPIN）** — 同本书未覆盖，但需 level2；标 future_bucket。
4. **机器学习动态 regime 识别（CPO）** — 需要 regime 标签的 ground truth，金融无客观划分；标 shell_only。
5. **完全自动化无人值守交易** — 涉及券商 API 稳定性、风控熔断、自然灾害；标 shell_only（技术可行但监管/操作风险高）。

### NEXT_ACTION
1. 生成 `adf_mean_reversion_filter` 对象壳：输入价格序列，输出 ADF 统计量、half-life、是否通过检验。
2. 生成 `kalman_pairs_hedge` 状态模板：输入双资产价格序列，输出动态 β_t、spread 序列、Z-score。
3. 生成 `kelly_leverage_guard` 模块：输入历史盈亏序列，输出 Kelly f*、Half-Kelly 建议杠杆、最大允许回撤。
4. 补全 A 股 ADV（日均成交额）与日内波动率数据，用于市场冲击模型校准。
5. 生成 `slippage_model` 参数表：按股票流通市值分档，给出滑点估计区间（level1 近似）。
6. 继续切割 Quantitative Trading (E. Chan) 与 Successful Algorithmic Trading (Halls-Moore)。