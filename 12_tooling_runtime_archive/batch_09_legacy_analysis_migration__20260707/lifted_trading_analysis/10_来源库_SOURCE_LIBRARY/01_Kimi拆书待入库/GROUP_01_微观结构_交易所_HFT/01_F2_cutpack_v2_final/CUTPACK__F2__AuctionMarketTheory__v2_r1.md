# CUTPACK: F2 — Auction Market Theory (Donald L. Jones / CISCO Futures)

## BASIC_INFO
- title: Auction Market Theory
- author: Donald L. Jones / CISCO Futures
- material_type: 交易理论讲义/教材
- domain_tags: [auction market theory, market profile, balance, value discovery, two-sided trade, overlay demand curve, TPO, volatility, reward-risk]
- file_scope: auction-market-theory_compress.pdf
- source_file_size_mb: 0.29
- retain_mode: RETAINED_EXCERPTS
- current_repo_role: SECONDARY_STRUCTURED_NOTE

## MATERIAL_POSITIONING
- what_this_source_is: 一本系统阐述拍卖市场理论（AMT）的教材级讲义，由J.P. Steidlmayer的 Market Profile 概念扩展而来，聚焦于短期非均衡拍卖市场的结构分析。全书分为三部分：理论框架（Part 1）、奖励/风险与交易模型（Part 2）、以及标准与机会度量（Part 3）。
- why_in_f2: F2 是交易理论总纲层。本书提供了拍卖过程、价值发现、接受/拒绝、平衡/失衡循环等底层语言，为 A2（Market Profile / Auction）的日型分类、POC、Value Area、Initial Balance 等具体概念提供理论支点。
- not_a_strategy_book_because: 本书不给出可直接执行的机械策略。它提供的是“规范式”（normative）分析框架——识别当前市场状态（market condition），并为“状态变化”制定策略，而非预测未来价格。Part 2 的 Basic Model 仅作为教学示例，Part 3 的 Potential 和 R/R 是事后评估标准而非实时信号。
- relation_to_order_flow_microstructure: 本书与 order flow 微结构相关但不等同。它使用交易所公开的 volume-price-member type 数据（Liquidity Data Bank / Buy-Sell Report），从会员类型（Locals / Commercials / Public）的净买卖行为推断市场力量，属于中观层面的拍卖分析，而非逐笔订单簿级别的微结构。
- data_footprint_required: 需要日内的 price-volume 或 TPO（Time-Price-Opportunity）数据，最好是 30 分钟级别的 bar 或 TPO 字母图。Overlay Demand Curve 需要多日的 Market Profile 叠加。理想的完整数据包括：TPO 字母图、volume at price、会员分类成交量（CTI1-CTI4）、Buy/Sell 净额报告。

## CONTENT_STRUCTURE

- **Part 1. Auction Market Theory (理论框架)**
  - 与 F2 的核心关联：定义拍卖市场的基本结构。包括 Market Observables（14 条可观察事实）、Market Profile（日内结构）、Overlay Demand Curve（多日叠加，识别市场状态）。
  - 关键章节：Auction Market Structure, Steidlmayer Original Decisions, Market Observables, Structure of a Trading Day, Overlay Demand Curve, Elements of Auction Markets, Volatility, Application: T-bonds on March 23.
- **Part 2. Reward, Risk and Trading Models (奖励/风险与交易模型)**
  - 与 F2 的关联：将 Part 1 的理论状态转化为可操作的前置条件。定义四种市场状态（Balance / Transition to Trend / Trend / Transition to Balance）。提出 Basic Model 作为教学基准，引入 Potential（最大可能盈利）和 Octant（1/8 分布范围作为风险代理）。
  - 关键章节：Initial Conditions, Balance, Transition to Trend, Trend, Basic Model, One Necessary Parameter (entry price), Potential.
- **Part 3. Standards: Potential and Opportunity (标准与机会)**
  - 与 F2 的关联：建立评估市场的绝对标准。Advice Engine Report 作为平衡市场突破候选列表；Potential 作为“理想”基准；Reward/Risk Ratio 作为跨市场比较工具。
  - 关键章节：Advice Engine Report, Select Trades, Reward to Risk Ratio Study, Locating Best Trading Risk.
- **Appendices (附录)**
  - 与 F2 的关联：AMT vs CAPM 对比表明确短期非均衡与长期均衡的本质区别；TA 示例说明为什么价格分析（candlesticks）不如价值分析（Market Profile）可靠；Normal Distribution 附录解释 Value Area 70% 和 Overlay 极限 ±2σ 的统计类比。

## RETAINED_EXCERPTS


**excerpt_id**: AMT-001
source_hint: "Part 1 / Auction Markets (p.3)"
quote: "Auction prices are arrived at by negotiation. Daily price range is determined through negotiation between the traders. As price is negotiated, some prices are accepted by the marketplace and create heavy volume. Rejected prices, the highs and lows, and sometimes opens and closes, are seldom traded and generate little volume. By trading many times throughout a day, accepted prices identify value."
why_kept: 拍卖过程的定义性描述：接受价产生成交量，拒绝价产生极小成交量。这是价值发现的底层机制，连接 order flow 与 price acceptance。
quant_link: "QUANTIZATION_TABLE: accepted_price_volume_proxy, rejected_price_volume_proxy"

**excerpt_id**: AMT-002
source_hint: "Part 1 / Steidlmayer Original Decisions (p.5-6)"
quote: "Markets auction 'too high' and 'too low' in the search for fair prices. Markets accept fair prices with enhanced volume and reject unfair prices by way of low volume. The price range is reached by negotiation among the traders."
why_kept: 价值发现的核心机制：市场通过试探过高/过低价格来寻找公平价格。接受=高量，拒绝=低量。这是 A2 中 value area / POC 的理论来源。
quant_link: "QUANTIZATION_TABLE: fair_price_discovery, value_area_volume_threshold"

**excerpt_id**: AMT-003
source_hint: "Part 1 / Steidlmayer Original Decisions (p.6)"
quote: "Traders/investors seek a fair price. ... He saw that relative value at a price is equal to the sum of the basic units (TPO's) at that price."
why_kept: TPO 作为价值度量的基本单元。Price-over-time = Value。这是将 volume 或 time 转化为价值描述的桥梁。
quant_link: "QUANTIZATION_TABLE: TPO_as_value_proxy"

**excerpt_id**: AMT-004
source_hint: "Part 1 / Market Observables (p.6)"
quote: "Double-sided auction markets see activity by both buyers and sellers. ... Auction markets are not generally equilibrium systems. ... An auction market's structure is continuously evolving, being revalued. ... An auction market is in one of two conditions: balancing or not balancing."
why_kept: 拍卖市场的基本二元性：双边交易、非均衡系统、持续重估、只有两种状态（平衡/非平衡）。这是所有后续状态判断的公理。
quant_link: "QUANTIZATION_TABLE: balance_binary_state, twosided_auction"

**excerpt_id**: AMT-005
source_hint: "Part 1 / Market Observables (p.7)"
quote: "The middle seventy percent of the volume is designated Value by analogy with the +/- one standard deviation of the normal curve. Prices at either end of the 70 percent value region define the Value Area. Prices outside the Value Area are increasingly less significant the further they are from the value region, with the day's highs and lows having the least volume and being least significant."
why_kept: Value Area 的严格定义：70% 成交量类比 ±1σ。高/低价最不被市场重视。这是 A2 中所有 value area 相关策略的基础。
quant_link: "QUANTIZATION_TABLE: value_area_70pct, value_area_extremes_significance"

**excerpt_id**: AMT-006
source_hint: "Part 1 / Market Observables: Accepted Prices (p.8)"
quote: "The price range 6039 to 6050 is heavily traded. A wide range of prices were approved for trading by the participants. These constitute the accepted prices for this day. The graphic is of an accumulating market, one which is cohesive, compact and in which there is good agreement on the location of acceptable price (value)."
why_kept: 接受价的实证描述：大量交易=被批准的价格=累积市场（accumulating）=对价值位置达成一致。与 A2 的 balance day 概念直接对应。
quant_link: "QUANTIZATION_TABLE: accumulating_market_single_distribution"

**excerpt_id**: AMT-007
source_hint: "Part 1 / Market Observables: Rejected Prices (p.8)"
quote: "Prices not accepted by the market generate very light volume. Such prices rarely trade and the trader who wants to do business there has little opportunity to do so. ... The upper three prices and the lower three prices are one-third of the day's trading range but only 3 percent of the volume."
why_kept: 拒绝价的量化证据：高点/低点占 1/3 价格区间但仅占 3% 成交量。这是接受/拒绝的最直观代理变量。
quant_link: "QUANTIZATION_TABLE: rejected_price_volume_ratio"

**excerpt_id**: AMT-008
source_hint: "Part 1 / Market Observables: Accumulation and Distribution (p.8-9)"
quote: "The accumulating market of figure IDO 1 has given way to a distributing, or moving market the next day. ... Volume today is 12,844 compared to the much lower 2,574 of yesterday. This market has moved over $1,000 in one day."
why_kept: 平衡（accumulation）与趋势（distribution/moving）的对比：单日成交量从 2,574 跳到 12,844，同时价格移动 $1,000。展示平衡被打破时的放量特征。
quant_link: "QUANTIZATION_TABLE: balance_vs_trend_volume_expansion"

**excerpt_id**: AMT-009
source_hint: "Part 1 / Market Observables: Day Traders and Swing/Position Traders (p.9)"
quote: "Day traders, by definition, are out of the market by the close. They have no long term effect on the market, since they are holding positions only a fractional part of the day and not at all overnight. ... Longer term demand, the sort that moves markets, comes from those who hold positions past the close. These are the position traders ... Day traders are the opportunists who jump on a move and hold a short time. Position traders have the patience to hold longer term, creating demand."
why_kept: 短期参与者（day traders）与长期参与者（position traders）的区分：前者是机会主义者，后者创造需求并推动市场。这是 timeframe participant 的核心定义。
quant_link: "QUANTIZATION_TABLE: short_vs_long_timeframe_participants"

**excerpt_id**: AMT-010
source_hint: "Part 1 / Market Observables: Members Functions (p.10-11)"
quote: "Class 1 are the Locals or scalpers ... provide liquidity and are most comfortable with balanced markets. Class 2 are the commercials ... the best informed traders on the floor. They too work best in balanced markets. ... Commercials typically do five to fifteen percent of the volume. ... Class 4 clears for us, the public. We, the public, are typically twenty to thirty percent of the day's trading volume."
why_kept: 四类参与者的行为差异：Locals 提供流动性，Commercials 最知情且在平衡市场运作最佳，Public 占 20-30% 成交量。这是理解谁在“接受”或“拒绝”价格的关键。
quant_link: "QUANTIZATION_TABLE: member_type_volume_distribution, commercials_balance_preference"

**excerpt_id**: AMT-011
source_hint: "Part 1 / Market Observables: Markets Cycle (p.11)"
quote: "Markets continually move from balance to testing the balance, to trend, to testing for end of trend and back to balance. The time spent in any one phase may be long or short. There is no valid method of predicting when the phase may change. ... The change from balance to trend can occur in minutes or may take days of testing the balance."
why_kept: 市场循环的完整描述：balance → test → trend → test → balance。强调无法预测阶段变化的时间。这是非预测性策略的理论基础。
quant_link: "QUANTIZATION_TABLE: market_cycle_phases, transition_unpredictable"

**excerpt_id**: AMT-012
source_hint: "Part 1 / Market Profile (p.13-14)"
quote: "Price-over-time, in line with general usage, is designated value. Value maps out a wide area in the mid region of a balanced market. It is inappropriate to say ... that value for the day is 6045. Rather, one would state that the market finds value in the 6050 - 6040 area. It is appropriate to say 'the market rejects prices in the neighborhood of 6054 and 6036'."
why_kept: Value 是区间而非单点。语言上的精确性：说“市场在 6050-6040 区间找到价值”，而非“价值是 6045”。拒绝也是区间概念。
quant_link: "QUANTIZATION_TABLE: value_as_interval_not_point"

**excerpt_id**: AMT-013
source_hint: "Part 1 / Trend Day Profile (p.14)"
quote: "The TPO shape of a short covering rally is that of a capital P. Price runs up, stopping past the point where the excess demand is gone. Then there is a period of backing and filling, forming the loop of the P. ... This behavior has been named the 'P' distribution. ... The P distributions show a time lag of about two hours, the time it takes the market to digest the real demand."
why_kept: 短轧空（short covering rally）的 P 型分布特征：价格冲高后停滞，需求消失后市场需要约两小时消化。这是识别“虚假需求”的具体形态。
quant_link: "QUANTIZATION_TABLE: short_covering_p_shape, demand_digestion_lag"

**excerpt_id**: AMT-014
source_hint: "Part 1 / Overlay Demand Curve (p.15-16)"
quote: "Any auction market may be, at a particular time, (1) in balance (temporary equilibrium), (2) in a trend or (3) in transition between equilibrium and trend. ... Each day is relatively independent of the former day; the coupling from day to day is normally very weak. ... The Overlay converts data from the day timeframe to the longer term required for understanding the over-all market behavior."
why_kept: 市场状态的三种分类：balance / trend / transition。Overlay Demand Curve 的作用是将日度 weak coupling 的数据转化为长期结构。这是 A2 中日型分类需要 Overlay 的原因。
quant_link: "QUANTIZATION_TABLE: market_condition_three_state, overlay_demand_curve"

**excerpt_id**: AMT-015
source_hint: "Part 1 / Overlay Demand Curve and Market Condition (p.17-18)"
quote: "Summing several days of profiles cancels out the noise (rumors, news, etc.) that is a part of each day. The resulting Overlay Demand Curve turns out to contain a deeper level of information. ... a breakout from an Overlay limit is an alert for a change in value. Or, a breakout from balance is an alert of a potential change of market condition from non-directional to directional (trending)."
why_kept: Overlay 的核心功能：抵消日内噪音，提取深层信息。突破 Overlay 极限 = 价值变化警报 = 状态变化警报。这是所有 breakout 策略的底层逻辑。
quant_link: "QUANTIZATION_TABLE: overlay_noise_cancellation, breakout_alert_state_change"

**excerpt_id**: AMT-016
source_hint: "Part 1 / Elements of Auction Markets (p.19-20)"
quote: "Demand fluctuates over the day timeframe. Demand change drives price change. ... Markets accumulate (balance) and distribute (trend). ... Markets cycle (phases are: balance, test, trend, test, balance, etc.) ... Accepted prices define value. Value is price over time. P x T = V x constant. ... Longer timeframe traders move markets by accumulating positions. Public day traders and public long timeframe traders seek trends. Long term trending markets are controlled by long timeframe traders."
why_kept: 拍卖市场的 33 条元素摘录。核心因果链：demand change → price change；accumulation = balance, distribution = trend；长期参与者通过积累头寸推动趋势；公众（短期和长期）都寻求趋势。
quant_link: "QUANTIZATION_TABLE: demand_drives_price, accumulation_distribution_definition, long_timeframe_trend_control"

**excerpt_id**: AMT-017
source_hint: "Part 1 / Volatility (p.21)"
quote: "We define the (AMT) volatility as the average range of the half-hour time periods of a Market Profile. ... The average of the half-hour bars approximates the risk of a trade stop-out from either the long or short side. It is the 'noise' risk. If one sets a risk (stop-loss) smaller than the noise, then the probability is high that simple market fluctuation will cause trade exit. The volatility, then, becomes the minimum risk one should take on a trade."
why_kept: AMT 波动率的定义：半小时 bar 的平均范围 = 噪音风险 = 最小止损风险。低于此噪音的止损会被随机波动触发。这是止损设置的硬性下限。
quant_link: "QUANTIZATION_TABLE: AMT_volatility_definition, noise_risk_minimum_stop"

**excerpt_id**: AMT-018
source_hint: "Part 1 / Volatility Table (p.21-22)"
quote: "Balanced markets (congestion) have low volatility. Trending markets have larger volatilities. ... Large volatility increases rarely precede the start of a trend, although sometimes the general market tenor, as measured by volatilty, rises prior to directional movement. Volatility is more of a coincident indicator, which helps to uncover trend end."
why_kept: 波动率的状态指示功能：低波动 = 平衡/拥堵，高波动 = 趋势。波动率大增很少先于趋势启动，更多是同步指标，帮助识别趋势结束。这是波动率作为 condition confirmation 工具的关键。
quant_link: "QUANTIZATION_TABLE: volatility_balance_trend_correlation, volatility_trend_end_coincident"

**excerpt_id**: AMT-019
source_hint: "Part 1 / Application: T-bonds March 23 (p.22-24)"
quote: "Price above 10706 is an upside breakout. Price below 10528 is a downside breakout. ... Risk on breakout for the swing trader is around $330. Risk on breakout for the day trader is around $160. ... Early congestion followed by massive later congestion on 3/22 is indicative of a market confused about underlying demand. A breakout tomorrow is unlikely because of the congestion picture in the last few hours of 3/22."
why_kept: 理论到策略的完整应用示例：Overlay 极限作为 breakout 触发点，风险分层（swing vs day trader），拥堵（congestion）作为突破可能性的反向指标。展示了 AMT 的“if this, then that”分析范式。
quant_link: "QUANTIZATION_TABLE: breakout_trigger_overlay_limit, congestion_breakout_likelihood"

**excerpt_id**: AMT-020
source_hint: "Part 1 / Short Covering Rally (p.24-25)"
quote: "The net is that the market sees demand over the period in which the members are buying in their shorts. This period is typically an hour or two. During the time the members are net buying, public interest is aroused. The public carries the price on up until they realize demand has evaporated. But this takes time. The market is not efficient."
why_kept: 短轧空的完整机制：会员买入回补→公众被吸引跟进→需求蒸发→市场低效需要约两小时才能消化。解释了为什么 P 型分布会出现“过头”再回落。
quant_link: "QUANTIZATION_TABLE: short_covering_mechanism, market_inefficiency_digestion_time"

**excerpt_id**: AMT-021
source_hint: "Part 1 / Commercial Capping (p.26)"
quote: "Commercial capping: the process where the commercial members (CTI2) sell heavily at the top (or buy heavily at a bottom) to push price back to balance. ... The CTI2 average volume for the day is 6.1 percent of the total. Going down the %CTI2 column we see the first two values of 14.7 and 8.7. Both are substantially larger than the 6.1. ... it appears the commercials capped and drove price well back to the middle."
why_kept: Commercials 在顶部/底部的“封顶”行为：CTI2 成交量占比在极端价格显著高于日均占比时，表明知情交易者在阻止趋势。这是从会员数据识别“接受”或“拒绝”的微观证据。
quant_link: "QUANTIZATION_TABLE: commercial_capping_volume_anomaly, CTI2_extreme_price_ratio"

**excerpt_id**: AMT-022
source_hint: "Part 2 / Initial Conditions / Balance (p.31)"
quote: "Balance is distinguished as a single price - volume distribution of the Overlay Demand Curve with the latest close inside the balance. Balance is a quasi-equilibrium state. End prices (limits) are known, i.e. alerts for end of balance or breakout from the single distribution. ... Risk is defined as a portion of the distribution analogous to one standard deviation (practically, a common approximation is one-eighth of the range of the balance)."
why_kept: Balance 的严格定义：单一分布 + 收盘价在分布内。风险 = 1/8 范围（Octant）。这是 Basic Model 和 Risk 计算的理论基础。
quant_link: "QUANTIZATION_TABLE: balance_single_distribution_criterion, octant_risk_definition"

**excerpt_id**: AMT-023
source_hint: "Part 2 / Transition to Trend & Trend (p.31)"
quote: "A transition from balance moves the market into a dis-equilibrium market condition, one with multiple distributions. A successful transition results in the start of a trend, i.e. a change in value. ... Trending is just price change reflecting changing demand. A trend is a quasi-orderly dis-equilibrium market condition. The path of a trend is generally not smooth, exhibiting runs and pauses."
why_kept: Transition 和 Trend 的定义：transition = 从单一分布到多重分布；trend = 需求变化引起的价格变化，具有 run-pause 结构。解释了为什么趋势日内会有小型平衡（pause）。
quant_link: "QUANTIZATION_TABLE: transition_multiple_distribution, trend_run_pause_structure"

**excerpt_id**: AMT-024
source_hint: "Part 2 / The Basic Model (p.33)"
quote: "Rules for the most elementary form of the breakout day trading Basic Model are: (1) limit trading to balanced markets only; (2) go long on a breakout of 1 tick above the Upper Limit; (3) go short on a breakout of 1 tick below the Lower Limit; (4) use a trailing stop of one Octant; (5) if not stopped out during the day, exit on the exchange close."
why_kept: Basic Model 的完整规则：仅交易平衡市场、突破 1 tick 入场、Octant  trailing stop、收盘离场。这是 AMT 中唯一的“硬规则”示例，用于 Potential 和 R/R 研究。
quant_link: "QUANTIZATION_TABLE: basic_model_breakout_rules, octant_trailing_stop"

**excerpt_id**: AMT-025
source_hint: "Part 3 / Potential (p.35)"
quote: "The best open-trade price is the Potential of that trade. Potential is always positive or zero, while the actual trade may win or lose. Potential measures a trade's maximum possible return. Potential plays a role akin to the index in CAPM. It is a quantity against which the trade's performance can be measured. ... the return - Potential comparison is absolute."
why_kept: Potential 的定义：入场后至收盘前的最大可能价格偏移。作为“理想”基准，用于衡量实际交易模型和交易者的效率。不是预测工具，而是事后评估标准。
quant_link: "QUANTIZATION_TABLE: potential_max_post_entry_excursion, potential_absolute_benchmark"

**excerpt_id**: AMT-026
source_hint: "Part 3 / Reward to Risk Ratio (p.39)"
quote: "The case in Figure IDO 16 uses an unaltered Octant stop. Average reward is 309 ($772) and average risk is 718 ($1795). R/R is 0.43. ... Cutting down the risk by half improves the R/R by a factor of 2 over the normal one Octant risk. ... Increasing the risk by half decreases the R/R by a factor of 50 percent."
why_kept: S&P 23 笔突破交易的实证：100% Octant 时 R/R = 0.43，50% Octant 时 R/R = 1.01，150% Octant 时 R/R = 0.30。证明风险过大或过小都会恶化 R/R，存在最优风险水平。
quant_link: "QUANTIZATION_TABLE: R_R_optimal_risk_level, octant_scaling_study"

**excerpt_id**: AMT-027
source_hint: "Appendix 5 / Value Diagram for a Balanced Market (p.49)"
quote: "There are five different regions on this value diagram. Region 1, above the Overlay upper limit, is up trend territory. Region 2, between the Overlay upper limit and the upper Value Area price is part of the balance but above the previous day's 'resistance'. Inside the Value Area is the profile rotational area. Then Region 4 is Overlay balance and Region 5 is down trend."
why_kept: 五区域价值图：将 Overlay 和 Market Profile 结合为空间策略地图。明确 rotation（Value Area 内）、resistance/support（Overlay 极限与 Value Area 之间）、trend（Overlay 极限外）的区分。
quant_link: "QUANTIZATION_TABLE: five_region_value_diagram, rotational_area_vs_trend_territory"

**excerpt_id**: AMT-028
source_hint: "Appendix 5 / Day Trading Rules (p.49)"
quote: "1) Price moving above 10615 is a breakout and the trader buys bottoms. 2) Price moving below 10507 is a breakout and the trader sells tops. 3) Price moving down through 10615 is sold. 4) Price moving up through 10507 is bought. 5) A long position moving up through 10607 is a confirmation. 6) A short position moving down through 10527 is a confirmation. 7) Price confined between 10607 and 10527 is a no trade."
why_kept: 平衡市场的日内策略规则示例：突破 Overlay 极限 = 趋势方向交易；穿过 Value Area 边界 = 反向/确认信号；Value Area 内 = 不交易。这是从理论到具体规则的映射。
quant_link: "QUANTIZATION_TABLE: balance_day_trading_rules, value_area_no_trade_zone"

**excerpt_id**: AMT-029
source_hint: "Part 1 / AMT Development (p.4)"
quote: "It is an axiom of Auction Market Theory that future prices are not predictable. Current market condition is found from AMT principles. ... A strategy developed subject to the event of change from one market condition to another is non-predictive (normative)."
why_kept: AMT 的核心公理：未来价格不可预测。策略基于“状态变化”而非预测。这是区分 AMT 与技术分析（TA）和 CAPM 的根本立场。
quant_link: "QUANTIZATION_TABLE: non_predictive_normative_strategy, condition_change_trigger"

**excerpt_id**: AMT-030
source_hint: "Part 1 / Market Profile Recap (p.15)"
quote: "Within a trading day, the natural interplay of trading forces generates a price - volume curve similar to the well known bell shape of the normal distribution. The volume per price around the middle prices far outweighs the volume per price farther away."
why_kept: Market Profile 的统计基础：日内交易力量自然产生类正态分布。这是 Value Area 70% 规则的现象学来源。
quant_link: "QUANTIZATION_TABLE: market_profile_quasi_normal_distribution"

## CORE_CONCEPTS


**concept_name**: Auction Process
definition_from_text: "Auction prices are arrived at by negotiation. Each trade has a buyer and a seller. Price is auctioned as high as possible until no one would bid higher, and as low as possible until no one would take less."
behavioral_mechanism: 双边谈判机制。买方竞价、卖方出价，成交价格由双方协商达成。市场通过在高/低价位的低成交量来拒绝极端价格，通过在中等价位的密集交易来接受价值区间。
data_objects_involved: price, volume, time, TPO (Time-Price-Opportunity), buyer/seller negotiation
quant_boundary: 无法直接量化“谈判意愿”，但可以通过 volume at price 和 TPO 频率来代理接受/拒绝程度。

**concept_name**: Two-Sided Trade
definition_from_text: "Double-sided auction markets see activity by both buyers and sellers. ... Each completed trade was negotiated between a buyer and a seller."
behavioral_mechanism: 所有市场均为双边拍卖，不存在单边市场。任何成交价都同时需要买方和卖方。市场通过两端的互动形成价格分布。
data_objects_involved: bid/ask（隐含）, volume, price distribution
quant_boundary: 在 TPO 或成交量数据中不区分买方/卖方主动性（除非有 CTI 分类数据），两端的参与是对称体现的。

**concept_name**: Balance / Imbalance
definition_from_text: "An auction market is in one of two conditions: balancing or not balancing. Balance is distinguished as a single price-volume distribution ... with the latest close inside the balance. ... A trend is a quasi-orderly dis-equilibrium market condition."
behavioral_mechanism: 平衡 = 市场参与者对价值区间达成共识，形成单一类正态分布。失衡 = 需求变化导致价格离开共识区间，形成多重分布或趋势性移动。市场从平衡到失衡的转换不可预测。
data_objects_involved: Overlay Demand Curve (单分布 vs 多分布), Market Profile 形态, 收盘价位置
quant_boundary: 通过 Overlay 是否为单分布、收盘价是否在分布内来判断。Distribution 极限由 ≥3 TPOs 的近似 ±2σ 定义。

**concept_name**: Acceptance / Rejection
definition_from_text: "Some prices are accepted by the marketplace and create heavy volume. Rejected prices, the highs and lows, and sometimes opens and closes, are seldom traded and generate little volume. ... Markets accept fair prices with enhanced volume and reject unfair prices by way of low volume."
behavioral_mechanism: 市场通过成交量表达接受度：高频交易的价格 = 被接受 = 有价值；极少交易的价格 = 被拒绝 = 偏离价值。极端价格（高/低）通常被拒绝。
data_objects_involved: volume at price, TPO count, Value Area (70% 成交量), highs/lows
quant_boundary: 70% 成交量定义 Value Area 边界；边界外价格成交量急剧衰减。可用日内 bar 的成交量分布作为代理。

**concept_name**: Value Discovery
definition_from_text: "Markets auction 'too high' and 'too low' in the search for fair prices. Traders/investors seek a fair price. ... By trading many times throughout a day, accepted prices identify value."
behavioral_mechanism: 市场通过试探性拍卖探索公平价格：出价过高则无人接盘，出价过低则无人抛售，直到找到双方都愿意大量交易的区间。这是一个持续的、非均衡的搜索过程。
data_objects_involved: price range, TPO distribution, volume distribution, Value Area, POC
quant_boundary: 价值由日内（Market Profile）或多日（Overlay）的成交量/时间分布中心定义。价值是区间，不是单点。

**concept_name**: Trade Facilitation
definition_from_text: "The auction market assumption is that frequency of trading at a price measures relative demand. ... at 6050, trading first occurred in the C timeframe, then recurred in F, G, J, K, L timeframes a total of six periods throughout the day. ... there is more demand at 6050 with six events than at 6054 with one event."
behavioral_mechanism: 交易频率（时间维度上的重复出现）是需求/价值的代理。某价格在不同时间段反复出现 = 市场愿意在该价格持续交易 = 该价格被接受。TPO 的重复次数即为“成交机会”的量化。
data_objects_involved: TPO count, half-hour periods, price-time matrix
quant_boundary: TPO 数量直接代理相对需求。在仅有 bar 数据时，可用 price 在多个 bar 内出现来近似 TPO 概念。

**concept_name**: Rotation / Trend / Balance Area
definition_from_text: "Inside the Value Area is the profile rotational area. ... Markets continually move from balance to testing the balance, to trend, to testing for end of trend and back to balance. ... The entire balance range (10615 to 10507) is rotational for the five day period."
behavioral_mechanism: Rotation = 价格在共识区间内来回波动，无方向性。Trend = 价格离开共识区间，需求持续单向推动。Balance Area = 允许旋转的范围。突破 Balance Area = 进入 Trend 状态。
data_objects_involved: Value Area, Overlay limits, Market Profile, Rotation Profile
quant_boundary: Value Area 内 = 旋转区；Overlay 极限内但 Value Area 外 = 平衡但接近突破的测试区；Overlay 极限外 = 趋势区。

**concept_name**: Short Timeframe Participant / Long Timeframe Participant
definition_from_text: "Short timeframe trader holding period is from minutes to hours. Longer timeframe trader holding period is days. ... Longer timeframe traders move markets by accumulating positions. ... Day traders are the opportunists who jump on a move and hold a short time. Position traders have the patience to hold longer term, creating demand."
behavioral_mechanism: 短期参与者（day traders, scalpers）利用日内波动，不隔夜持仓，对长期方向无影响。长期参与者（position/swing traders, institutions）通过持续积累头寸创造需求，推动趋势。公众（public）无论短/长期都倾向于寻求趋势。
data_objects_involved: holding period, position size, overnight exposure, volume by member type (CTI1-CTI4)
quant_boundary: 在本书中，参与者时间框架主要通过 CTI 分类和 Buy/Sell 净额来推断。在 A 股环境中，没有 CTI 数据，需通过持仓变化、资金流向等代理。

## QUANTIZATION_TABLE

| concept | raw_rule_from_text | observable_proxy | data_needed | quant_status | implementation_hint | notes |
|---|---|---|---|---|---|---|
| accepted_price_volume_proxy | 接受价产生大量成交，拒绝价成交量极低 | 日内某价格成交量 / 当日总成交量 > 阈值（如 5%） | 日内 volume at price 或 TPO | proxy_quantizable_now | 用 1-min 或 5-min K 线的成交量分布近似 volume at price | 需要 L2 或至少 volume profile 数据；纯 OHLC 日线无法计算 |
| rejected_price_volume_proxy | 高/低价占 1/3 价格区间但仅占 3% 成交量 | 高/低价附近（如 top 10% 价格区间）的成交量占比 < 阈值 | 日内 volume at price | proxy_quantizable_now | 计算日内成交量分布的尾部占比；或用 TPO 数量在极端价格的稀少性 | 书中以瑞士法郎为例给出 3% 的参考，但阈值应因市场而异 |
| value_area_70pct | 中间 70% 成交量定义为 Value Area，类比 ±1σ | 日内成交量分布的 70% 中心区间 | 日内 volume at price 或 TPO | proxy_quantizable_now | 在 pandas 中对日内 price-volume 分组排序，取累积 70% 的边界 | 无 volume 时可用 TPO（时间）替代；但 TPO 需要 30-min 数据 |
| TPO_as_value_proxy | TPO 数量 = 该价格的基本单元之和，P × T = V × constant | 某价格在不同 30-min 时段出现的次数 | 30-min intraday bars (或更细) | proxy_quantizable_now | 将 30-min bar 的价格轴展平，统计每价格出现的 bar 数 | 15-min 或 5-min bar 可替代 30-min，但“信息消化时间”的假设可能改变 |
| balance_single_distribution_criterion | Balance = Overlay 呈单一分布，收盘价在分布内 | 多日价格分布的峰数（单峰/双峰）+ 最新收盘价是否在 [lower_limit, upper_limit] 内 | 多日 Market Profile 或 TPO 叠加 | needs_extra_data | 用 KDE 或多日 histogram 判断单峰/多峰；Overlay 极限定义为 ≥3 TPOs 的价格 | 需要至少 3-5 个交易日的 Profile 数据 |
| breakout_alert_state_change | 突破 Overlay 极限 = 价值变化警报 = 趋势可能开始 | 价格 > upper_limit 或 < lower_limit | Overlay Demand Curve 的 upper/lower limit | proxy_quantizable_now | 用 N 日滚动成交量分布的 ±2σ 边界作为极限；突破即触发 | 极限可用 1/8 range（Octant）或 ±2σ 定义；需动态更新 |
| octant_risk_definition | 风险 = 1/8 的 Overlay 分布范围（Balance range） | risk = (upper_limit - lower_limit) / 8 | Overlay 的 upper_limit, lower_limit | proxy_quantizable_now | 计算 N 日 overlay 的价格范围，除以 8 作为止损距离 | 书中验证 100% Octant 时 R/R 仅 0.43，50% Octant 时 R/R = 1.01，说明固定 1/8 并非最优 |
| AMT_volatility_definition | 波动率 = 30-min bar 的平均范围 | mean(high_30min - low_30min) across all periods of the day | 30-min intraday bars | proxy_quantizable_now | 取日内所有 30-min bar 的 range，求平均 | 可推广到 15-min 或 1-min，但 30-min 与 TPO 的“信息消化时间”假设一致 |
| noise_risk_minimum_stop | 止损小于噪音波动率时，高概率被随机波动触发 | 止损距离 < AMT_volatility（30-min 平均 range） | 30-min intraday bars + 止损规则 | proxy_quantizable_now | 将 AMT_volatility 作为止损的硬下限；任何小于此值的止损都是“噪音止损” | 这是止损优化的必要条件，而非充分条件 |
| volatility_balance_trend_correlation | 低波动 = 平衡/拥堵；高波动 = 趋势 | 日内 30-min range 的均值 | 30-min intraday bars | proxy_quantizable_now | 将 AMT_volatility 时间序列与 Overlay 状态（balance/trend）做对照 | 波动率增大极少先于趋势启动，更多是同步或滞后确认 |
| market_cycle_phases | 市场循环：balance → test → trend → test → balance | 状态机：单分布 + 收盘价内 → balance；突破极限 → transition；多分布 + 收盘价外 → trend | 多日 Overlay + 日内 Profile | needs_extra_data | 构建状态机：根据每日收盘时的分布形态和收盘价位置判定状态 | 状态转换时间不可预测；状态机本身不提供时间预测 |
| short_covering_p_shape | 短轧空呈 P 型分布：冲高→停滞→消化→回落 | 日内前半段快速上涨，后半段在高位横盘（TPO 在顶部形成“环”），随后回落 | 30-min TPO / Market Profile | needs_extra_data | 识别日内前半段 trend，后半段 balance 的复合形态；可用 profile 字母形状判断 | 需要经验判断，非纯算法。书中的 P 型是命名形态，非量化模板 |
| commercial_capping_volume_anomaly | Commercials 在极端价格成交量占比显著高于日均占比时，在封顶/托底 | CTI2 在 top 3 价格 / CTI2 全天占比 > 1.5x 或 2x | Liquidity Data Bank (CTI1-CTI4) | needs_extra_data | 在 A 股无 CTI 数据，可用大单/超大单在极端价位的占比异常作为代理 | 需要 L2 或逐笔数据中的大单分类；纯 bar 数据无法区分参与者类型 |
| demand_drives_price | 需求变化驱动价格变化 | 成交量变化率（或 TPO 变化率）与价格变化率的领先/滞后关系 | volume at price, TPO, price | proxy_quantizable_now | 计算 volume/TPO 的增量与 price 变化的相关性；但书中强调这是因果陈述，非预测指标 | 统计相关性不等于因果；书中的“需求变化”是理论概念，无直接观测变量 |
| long_timeframe_trend_control | 长期参与者通过积累头寸推动趋势 | 持仓量变化（OI change）或长周期资金流向 | 持仓量（Open Interest）、CFTC COT 等 | needs_extra_data | 在期货市场中用 OI 变化；在 A 股用融资融券余额或北向资金等长周期资金代理 | 书中用 CTI2+CTI4（Commercials+Public）的净买卖作为积累信号；A 股无直接对应 |
| potential_max_post_entry_excursion | Potential = 入场后至收盘前的最大可能价格偏移 | 入场后 intraday 的 max(high) - entry（多头）或 entry - min(low)（空头） | 日内 tick 或 minute 数据 | proxy_quantizable_now | 对历史突破交易，计算入场后至收盘的价格极值偏移；这是事后统计，非实时信号 | Potential 是事后基准，不可用于实时交易决策；用于评估模型效率 |
| R_R_optimal_risk_level | S&P 实证：50% Octant 时 R/R 最佳（1.01），100% Octant 时 0.43，150% Octant 时 0.30 | 不同止损比例下的平均收益 / 平均风险 | 历史交易记录 + 不同止损比例回测 | proxy_quantizable_now | 对历史突破交易回测不同止损比例，绘制 R/R 曲线，寻找峰值区间 | 最优风险比例是市场依赖的，S&P 的结果不能外推至其他市场 |
| five_region_value_diagram | 五区域图：trend 区（Overlay 外）→ 平衡测试区（Overlay 极限与 Value Area 间）→ 旋转区（Value Area 内） | 当前价格相对于昨日/多日 Overlay 极限和 Value Area 的位置 | Overlay limits, Value Area upper/lower | proxy_quantizable_now | 将当前价格映射到五区域之一，输出状态标签 | 区域定义是静态的，基于前一日的 Overlay；日内动态变化需实时更新 |
| balance_day_trading_rules | 平衡市场规则：突破 Overlay 极限 = 趋势方向；穿过 Value Area 边界 = 反向/确认；Value Area 内 = 不交易 | 价格与 Overlay 极限和 Value Area 边界的穿越事件 | 日内 price + 前日 Overlay + 前日 Value Area | proxy_quantizable_now | 用条件触发器实现：价格 > upper_limit → 做多；价格 < lower_limit → 做空；在 VA 内 → 空仓 | 规则是教学示例，非机械系统。实际交易者需要“经验覆盖” |
| non_predictive_normative_strategy | 策略基于状态变化（if this, then that），而非预测未来价格 | 当前状态标签 + 状态变化事件 → 触发策略动作 | 状态机（balance/trend/transition）+ 价格穿越事件 | proxy_quantizable_now | 构建状态机：检测到从 balance 到 breakout → 启动趋势跟踪；检测到 congestion → 启动平衡区间交易 | 状态机不提供“何时变化”的时间预测，只提供“变化后做什么”的动作映射 |
| member_type_volume_distribution | 四类会员（Locals/Commercials/Off-floor/Public）的成交量占比 | 成交量按 CTI1-CTI4 分类 | Liquidity Data Bank | needs_extra_data | 在 A 股可用逐笔中的机构/散户分类（如龙虎榜、大宗交易）作为粗糙代理 | 书中数据来自 CBOT/CME 的 Liquidity Data Bank；A 股无直接等价物 |
| value_as_interval_not_point | 价值是区间，不是单点。拒绝也是区间概念 | Value Area 宽度、Overlay 分布宽度 | 日内/多日 price-volume 分布 | proxy_quantizable_now | 在策略中避免用单点价格作为“价值”，改用区间判断 | 这是概念约束，而非量化规则。它改变了描述市场的方式 |
| transition_multiple_distribution | Transition 从单一分布进入多分布（失衡） | Overlay 的峰数从单峰变为多峰 | 多日 Overlay Demand Curve | needs_extra_data | 用 KDE 峰数检测或分布偏度/峰度变化来识别多分布出现 | 书中用“多分布”是定性判断，无自动算法 |
| demand_digestion_lag | 市场消化真实需求需要约两小时（P 型分布） | 日内从价格极值到 congestion 形成的时间间隔 | 30-min TPO / Market Profile | needs_extra_data | 计算日内 trend phase 到 balance phase 的持续时间，统计分布 | 两小时是经验值（30-min TPO × 4），非普适常数；电子市场可能不同 |

## FORMULAS_AND_ALGOS


**formula_id**: F-001
name: TPO-based Value Area
formula: "Value Area = middle 70% of TPO count (or volume) distribution. Upper = price at 70th percentile from bottom; Lower = price at 30th percentile from bottom."
source_location: "Part 1 / Market Profile Recap (p.15)"
quant_status: proxy_quantizable_now
notes: 类比正态分布的 ±1σ。实际可用 volume 或 TPO 计数实现。

**formula_id**: F-002
name: Overlay Distribution Limits (Approx ±2σ)
formula: "Upper Limit = highest price with ≥3 TPOs in the Overlay. Lower Limit = lowest price with ≥3 TPOs in the Overlay."
source_location: "Part 1 / Overlay Demand Curve (p.18)"
quant_status: proxy_quantizable_now
notes: 3 TPOs 作为 95% 置信水平的近似截断。在正态分布中 ≈ ±2σ。实际可用多日叠加 histogram 的稀疏边界确定。

**formula_id**: F-003
name: AMT Volatility (Half-Hour Range Average)
formula: "VTY = mean( high_i - low_i ) for i = 1..N half-hour periods of the trading day"
source_location: "Part 1 / Volatility (p.21)"
quant_status: proxy_quantizable_now
notes: N 通常 = 12-13（交易时段的 30-min 段数）。可用 15-min 或 1-min 数据类比，但时间尺度会改变噪音含义。

**formula_id**: F-004
name: Octant (Risk Proxy)
formula: "Octant = (Upper_Limit - Lower_Limit) / 8"
source_location: "Part 2 / Balance (p.31)"
quant_status: proxy_quantizable_now
notes: 1/8 的 Balance range 作为 1σ 代理。书中 S&P 实证表明 100% Octant 的 R/R 并非最优，50% Octant 更优。Octant 是教学起点，不是最优风险。

**formula_id**: F-005
name: Potential (Maximum Post-Entry Excursion)
formula: "Potential_long = max(high from entry to close) - entry. Potential_short = entry - min(low from entry to close)."
source_location: "Part 3 / Potential (p.35)"
quant_status: proxy_quantizable_now
notes: 这是事后统计量，用于评估交易模型效率。不是实时交易信号。Basic Model 的 entry 是突破 Overlay 极限 + 1 tick。

**formula_id**: F-006
name: Reward-to-Risk Ratio (R/R)
formula: "R/R = Average_Gain / Average_Risk. Risk can be scaled by Octant percentage (20%, 50%, 100%, 150%, etc.)."
source_location: "Part 3 / Reward to Risk Ratio (p.39-41)"
quant_status: proxy_quantizable_now
notes: 书中对 S&P 23 笔交易进行了 20%-180% Octant 的网格研究。R/R 随风险增加而单调递减（超过最优点后）。

**formula_id**: F-007
name: Commercial Capping Detection (Volume Ratio)
formula: "%CTI2_at_extreme / %CTI2_daily_average > threshold (e.g., 1.5x or 2x)"
source_location: "Part 1 / Commercial Capping (p.26)"
quant_status: needs_extra_data
notes: 书中 CTI2 日均 6.1%，极端价格达 14.7% 和 8.7%。需要 Liquidity Data Bank 或逐笔中的会员分类数据。

**formula_id**: F-008
name: Short Covering Rally Profile (P Distribution)
formula: "定性形态：日内前半段为 trend（价格上涨，TPO 向右上），后半段为 balance（TPO 在高位形成环状）。总时长约 2 小时消化。"
source_location: "Part 1 / Short Covering Rally (p.24-25)"
quant_status: needs_extra_data
notes: 非数值公式。需要 Market Profile 字母图进行形态识别。可量化为：前半段 range 扩展 / 后半段 range 收缩 + 高位 TPO 密集。

**formula_id**: F-009
name: Value Diagram Region Mapping
formula: "Region 1: price > upper_overlay_limit (up trend). Region 2: upper_VA < price < upper_overlay (balance test). Region 3: lower_VA < price < upper_VA (rotation). Region 4: lower_overlay < price < lower_VA (balance test). Region 5: price < lower_overlay (down trend)."
source_location: "Appendix 5 / Value Diagram (p.49)"
quant_status: proxy_quantizable_now
notes: 这是五区域空间映射规则。可直接用前日 Overlay 和 Value Area 边界作为阈值实现。

**formula_id**: F-010
name: Rejected Price Volume Ratio
formula: "Rejected_Volume_Ratio = volume_in_top_3_and_bottom_3_prices / total_day_volume"
source_location: "Part 1 / Market Observables: Rejected Prices (p.8)"
quant_status: proxy_quantizable_now
notes: 书中瑞士法郎示例：高/低 3 个价格占 1/3 区间但仅 3% 成交量。可作为接受/拒绝的代理度量。

## NOT_QUANT_YET


**item_id**: NQY-001
concept: "Excess"
reason: 本书中未使用 "excess" 作为独立术语。最接近的是短轧空中 "price runs up, stopping past the point where the excess demand is gone"，但这里 excess demand 是描述性用语，非理论概念。在 A2（Dalton 的 Market Profile）中 excess 有独立定义，本书不涵盖。
needed_for: 与 A2 的 excess / poor high / poor low 概念衔接

**item_id**: NQY-002
concept: "Initiative Activity / Responsive Activity"
reason: 本书未使用 "initiative" 或 "responsive" 术语。最接近的是 "breakout"（突破 Overlay 极限，类似 initiative）和 Advice Engine 报告中提到的 "Counter-trend (responsive) trades"（p.36），但后者仅是一笔带过，未展开定义。完整的 initiative/responsive 框架需参考 Dalton 的 Mind Over Markets。
needed_for: 与 A2 的 initiative buying / responsive selling 等行为分类衔接

**item_id**: NQY-003
concept: "Auction Facilitation 的实时度量"
reason: 本书用 TPO 重复频率作为相对需求的代理，但无实时算法来度量"当前拍卖是否被促进"。TPO 是事后统计，不能回答"此刻价格是否被接受"。
needed_for: 实时判断价格接受/拒绝，用于日内即时决策

**item_id**: NQY-004
concept: "参与者意图的实时推断"
reason: 本书通过 CTI 分类（Locals/Commercials/Public）和 Buy/Sell 净额推断参与者行为，但这些数据是 EOD 报告。无实时逐笔中的参与者身份数据，无法实时推断 initiative/responsive 的归属。
needed_for: 实时 order flow 分析中的买方/卖方主动性识别

**item_id**: NQY-005
concept: "Information Digestion Time 的自动标定"
reason: 本书假设 30-min 是信息消化的最小时间，P 型分布的消化滞后约 2 小时。但无方法来自动标定不同市场、不同时期的信息消化时间。电子市场可能已改变此时间尺度。
needed_for: 动态 TPO 时间粒度选择，适应不同市场速度

**item_id**: NQY-006
concept: "Overlay 分布极限的自动统计检验"
reason: 书中用 ≥3 TPOs 作为 ±2σ 的近似，但无统计检验来判断 Overlay 是否真的是单分布（正态），还是多分布混合。需要正式的分布检验（如 Bimodality Coefficient, Dip Test）来量化平衡/失衡。
needed_for: 自动识别 balance 状态，减少主观判断

**item_id**: NQY-007
concept: "Trend 内部的 Pause 结构量化"
reason: 书中提到 trend 有 run-pause 结构，但无量化方法来识别 pause 的开始/结束，以及 pause 是 trend continuation 还是 transition to balance。需要形态识别或波动率突变检测。
needed_for: 在趋势中判断何时获利了结或加仓

**item_id**: NQY-008
concept: "跨市场 R/R 的实时排名与选择"
reason: 书中 Advice Engine 和 Select Table 提供 EOD 跨市场 R/R 排名，但无实时方法。Potential 是事后统计量，无法实时计算。
needed_for: 实时多市场扫描，选择最优交易机会

**item_id**: NQY-009
concept: "Failed Breakout 的自动识别与回退机制"
reason: 书中 T-bonds 3/22 案例详细分析了 failed breakout，但依赖分析师经验（识别 short covering rally、congestion 等）。无自动算法来判断 breakout 是 genuine 还是 failed。
needed_for: 自动过滤假突破，减少错误入场

**item_id**: NQY-010
concept: "Market Condition 状态转换的概率模型"
reason: 书中强调状态转换不可预测，但未给出任何概率或持续时间分布。需要历史数据统计 balance 和 trend 的持续时间分布，以及转换触发的条件概率。
needed_for: 为状态机添加概率权重，优化仓位管理

**item_id**: NQY-011
concept: "A 股环境下的 Overlay 与会员数据替代"
reason: 本书所有案例和工具基于 CBOT/CME 的 futures 市场，依赖 TPO、Liquidity Data Bank、CTI 分类。A 股无 TPO 传统、无 CTI 报告、无交易所提供的 volume-price-member 数据。需要找到完整的 A 股代理方案。
needed_for: 将 AMT 框架应用于 A 股量化研究

## NEXT_ACTION


**action_id**: NA-001
task: 建立 A 股 TPO 代理：用 30-min K 线 + 成交量 模拟 Market Profile 的 TPO 和 Value Area 计算
priority: high
rationale: 本书核心工具（TPO、Value Area、Overlay）需要 TPO 数据。A 股无原生 TPO，需用 30-min bar 的 open/high/low/close + volume 来近似。

**action_id**: NA-002
task: 构建 Overlay Demand Curve 的自动化：对 N 日（5/10/15/20）的 30-min 价格分布进行叠加，计算单峰/多峰和分布极限
priority: high
rationale: Overlay 是识别 market condition 的核心。需要程序化实现多日叠加、极限检测、单分布判断。

**action_id**: NA-003
task: 实现 AMT 波动率（30-min bar range 平均）和 Octant（1/8 overlay range）的日度计算
priority: high
rationale: Volatility 是判断 balance/trend 的同步指标，Octant 是 Basic Model 和 R/R 研究的基础。

**action_id**: NA-004
task: 对 A 股指数或期货（如股指期货 IF）进行 Basic Model 回测：平衡市场 + 突破 Overlay 极限 ±1 tick 入场 + Octant 止损 + 收盘离场，计算 Potential 和 R/R
priority: high
rationale: 验证 AMT 框架在 A 股环境中的可行性。书中 S&P 的 R/R 为 0.43（100% Octant），需要测试 A 股是否类似或不同。

**action_id**: NA-005
task: 设计 A 股版本的 commercial capping 代理：用大单/超大单在极端价位的成交量异常占比来推断“知情交易者的拒绝/接受”
priority: medium
rationale: 本书用 CTI2 数据识别 commercial capping。A 股无 CTI，但可用逐笔数据中的大单分类作为粗糙代理。

**action_id**: NA-006
task: 将 AMT 的状态机（Balance / Transition / Trend / Transition）与 A2 的日型分类（Normal / Trend / Non-Trend / Day Type）进行映射
priority: high
rationale: 本书是 A2 的理论基础。需要明确 AMT 的 market condition 如何对应到 A2 的 day type，避免两套语言的混淆。

**action_id**: NA-007
task: 在 A 股数据上测试“接受/拒绝”的 volume 代理：统计日内高/低价区间的成交量占比，验证是否同样呈现“极端价格占 1/3 区间但仅 3% 成交量”的特征
priority: medium
rationale: 本书的核心现象学假设（接受/拒绝的 volume 分布）需要在 A 股中验证。若分布形态不同，则 AMT 的代理变量需要调整。

**action_id**: NA-008
task: 阅读并对比 A2（Market Profile / Auction）的现有 cutpack，明确 AMT 与 A2 的边界：AMT 负责理论语言和状态机，A2 负责日型模板和具体规则
priority: high
rationale: 用户红线要求不要和 A2 混在一起写，但需要明确两者的理论关联。先阅读 A2 现有文件，再定位 AMT 的引用点。

**action_id**: NA-009
task: 实现 P 型分布（short covering rally）的自动化检测：识别日内前半段趋势 + 后半段高位 balance 的复合形态
priority: medium
rationale: P 型是识别虚假需求的具体形态。虽然需要经验判断，但可尝试用波动率/range 的切换模式来量化。

**action_id**: NA-010
task: 对 A 股数据运行不同 Octant 比例（20%-180%）的止损研究，绘制 R/R 曲线，寻找 A 股的最优风险比例
priority: medium
rationale: 书中 S&P 的最优风险约 50% Octant，但不同市场可能不同。A 股需要自己的标定。

**action_id**: NA-011
task: 构建 A 股五区域价值图（Value Diagram）的实时映射：将当前价格映射到 trend / balance-test / rotation / balance-test / trend 五区域之一
priority: medium
rationale: 五区域图是日内策略的空间地图。需要前日 Overlay 和 Value Area 作为阈值，实时输出区域标签。

**action_id**: NA-012
task: 验证 AMT 的"低日度序列相关性"假设在 A 股是否成立：计算 A 股主要指数的日度收益率自相关系数
priority: low
rationale: AMT 的核心公理之一是"markets display little day to day serial correlation"，这是不使用前日数据预测今日的基础。若 A 股相关性不同，则策略框架需调整。
