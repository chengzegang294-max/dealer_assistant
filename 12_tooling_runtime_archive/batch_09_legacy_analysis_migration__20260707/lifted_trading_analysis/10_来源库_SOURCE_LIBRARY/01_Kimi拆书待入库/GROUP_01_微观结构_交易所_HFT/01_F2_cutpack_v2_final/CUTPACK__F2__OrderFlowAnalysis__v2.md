## BASIC_INFO
- title: 订单流交易：了解微观市场结构并从中获利（上+下）
- author: Michael Valtos (迈克·威尔托斯)
- material_type: 交易技术教材/订单流教程
- domain_tags: [order flow, footprint, delta, DOM, microstructure, aggressive buying, imbalance, absorption, trapped trader]
- file_scope: 订单流交易 了解微观市场结构并从中获利 —上部分 + —下部分
- source_file_size_mb: 70.05 (上 34.12 + 下 36.89)
- retain_mode: RETAINED_EXCERPTS
- current_repo_role: SECONDARY_STRUCTURED_NOTE

## MATERIAL_POSITIONING
- what_this_book_is: 一本基于订单流（Order Flow）与微观市场结构的交易分析教材，核心是将K线内部按逐笔成交拆解为主动型买单与主动型卖单，通过斜对角对比、Delta计算、失衡检测、堆积识别、吸收判断等手段，读取市场当下的供需力量对比与参与者心理。
- why_in_f2: 本书为F2仓库提供订单流层面的"观察语言层"与"数据对象定义层"，明确定义了aggressive buying/selling、imbalance、stacked imbalance、absorption、trapped trader、delta等可观察对象及其数据需求，是后续任何订单流量化尝试的概念基础。
- not_a_strategy_book_because: 全书以图表模式识别、主观盘感、经验阈值（如比率28、0.699、3:1失衡等）和视觉信号为核心，未提供可编程的入场/出场规则系统；大量依赖"阅读市场"、"感受潮涨潮落"等无法直接编码的描述；作者明确反对将订单流方法简单程序化（"我是交易员，不是IT码农"）。
- relation_to_order_flow_microstructure: 核心教材。直接定义了订单流图表的解读方式（斜对角主动买卖对比）、主动/被动交易者区分、需求/供应失衡、失衡堆积支撑阻力带、吸收区间、被套交易者、大单/微单、POC、Delta/Cumulative Delta、冰山订单、VWAP等概念。这些概念是理解微观市场结构的必要词汇表。
- data_footprint_required: tick-by-tick逐笔成交数据（含aggressor flag判断主动买卖方向）、L2 DOM盘口快照（用于观察冰山订单与被动限价单堆积）、footprint图表（每根K线内部按价格级别的主动买/主动卖量矩阵）、等时图/等价图/等量图的多时间框架数据。

## CONTENT_STRUCTURE
- 名词解释：主动型买方/卖方、被动型买方/卖方、顶部主买比率、底部主卖比率、微单、大单、需求失衡、供应失衡、堆积失衡、被套交易者、Delta、吸收、主动出击、POC等核心概念字典
- 介绍订单流：订单流与传统K线对比、订单流本质不属于技术分析、动态实时观测方法
- 订单流的威力：避免指标滞后性、甄别震荡市场、精确风险衡量、客观交易决策
- 生活中的订单流：供需博弈的类比
- 订单流软件：NinjaTrader8插件、数据提供商要求（精细Tick级数据）
- 理解订单流：机构行为识别、供需博弈、订单流适用范围
- 解读订单流图表：斜对角排布、主动卖单在左/主动买单在右、已成交订单记录规则、蓝色/紫色/黑色着色逻辑
- 价格的重要性：趋势形成过程、趋势健康判断、上涨趋势/下跌趋势终止条件
- 成交量的重要性：传统成交量局限、主动型/被动型成交量分解、牛皮市吸收特征
- Delta的重要性：单K线主动买-主动卖差值、Max/Min Delta、Cumulative Delta、Delta与趋势强度、Delta接近0表示吸收
- POC：K线内部成交量最大价位、POC位置判断（顶部/底部/中部）
- 不同类型的交易者：主动型、被动型、对冲、套利、投机
- 主动型交易者：市价单特征、推动价格运动的核心、与供需不平衡的关系
- 被动型交易者：限价单特征、形成支撑/阻力、机构可能通过限价单隐蔽建仓/派发
- 主动与被动交易者的重要性：趋势形成机制、关键价位订单量分析、成交量下降与趋势终结的复杂性
- 市场失衡：供需比例阈值（250%、300%、400%）、斜对角对比、2.5:1/3:1/4:1比例
- 失衡堆积：连续3个价位失衡构成支撑/阻力带、低风险入场点、止损设置方法、成交量验证要求
- 被套交易者：趋势末端逆势入场者、止损推动新趋势、短线反转信号
- 吸收：筹码交换区间、Delta与总成交额比值低、主动买卖大量出现但价格不动、与盘整的区别（来自市场内部vs外部因素）、突破买入机会
- 主动出击：价值区间突破、机构主导、大额订单推动、响应性行为
- K线图与订单流：传统K线滞后性、K线内部信息缺失、影线部分供需不平衡信号
- 多种搭配图表：等价图、等量图、等时图、多周期框架
- 高频交易：提供流动性、订单流分析应用、抢跑机制
- 机构与算法交易：机构行为识别、成交量暴露行踪、冰山算法、虚出价系统、隐蔽建仓/派发
- VWAP：成交量加权平均价格、机构执行基准、标准差偏离、日内滞后性
- 冰山订单：订单分割、盘口侦测方法、支撑/阻力位有效性、中国市场现状说明
- 阻力位与支撑位：传统技术分析局限、成交量验证、订单流反应判断
- 前期高低点：昨日/前月/一年内高低点、收盘价、止损单触发、突破站稳验证
- 今日高低点：日内局部高低点、夜盘区间、大单/微单在高低点信号、Delta转变
- 长线分析：周线/月线/日线多周期框架、关键价位标注
- 关键数字：20项每日准备清单（年度高低点、月度高低点、昨日/前日数据、夜盘数据、经济事件等）
- 神秘力量：不寻常力量阻止预期走势、经济数据公布前后市场行为
- 订单流在长线交易中的应用：长线趋势中的订单流反转识别
- 交易计划与资金管理：收益风险比、痛苦阈值、时间止损、止损逻辑、避免过度追求完美止盈
- 正确交易操作：基于供需理性分析、避免持仓后二次判断偏差
- 交易心理：连胜目标、空仓纪律、矛盾信号处理
- 高质量交易机会特征：买入/卖出四条件、供需失衡+吸收突破
- 融会贯通：综合信号识别、交易计划步骤（确认→入场→止损→止盈）、胜率与盈亏比
- 订单流应用实例：微单做空、大单反转、失衡+被套交易者、订单流背离（顶/底）、信号组合验证
- 大功告成：练习方法、知识转化为技能、主观性与灵活性

## RETAINED_EXCERPTS

- excerpt_id: EXC001
  source_hint: 名词解释（Page 7）
  quote: "主动型买方：某个价位的主动买单远大于主动卖单，表示有很多主动型买盘在这个价位进场。主动型卖方：某个价位的主动卖单远大于主动买单，表示有很多主动型卖盘在这个价位进场。"
  why_kept: 明确定义了aggressive buying/selling的核心概念，是订单流分析的基础观察对象
  quant_link: aggressive_buying, aggressive_selling, order_flow_footprint

- excerpt_id: EXC002
  source_hint: 名词解释（Page 7-8）
  quote: "需求失衡（过量）：根据拍卖理论，斜对角价位进行对比，某个价位主动买单数量远大于低一档价位的主动卖单数量，表示多头力量强势，本书中比值通常设为3:1。供应失衡（过量）：某个价位主动卖单数量远大于高一档价位的主动买单数量，表示空头力量强势，本书中比值通常设为3:1。"
  why_kept: 定义了imbalance的核心计算方式——斜对角对比，以及阈值设定
  quant_link: imbalance, stacked_imbalance, demand_imbalance, supply_imbalance

- excerpt_id: EXC003
  source_hint: 名词解释（Page 8）
  quote: "堆积失衡现象：表示某个价格区间出现了连续的需求失衡或者供应失衡现象，更能体现这个区间某一方力量的碾压性优势，本书中判定连续三个价位出现失衡现象则构成堆积失衡现象，通常视为形成阻力带或支撑带。"
  why_kept: 定义了stacked imbalance的判定标准（连续3个价位）及其市场意义（支撑/阻力带）
  quant_link: stacked_imbalance, support_resistance_zone

- excerpt_id: EXC004
  source_hint: 名词解释（Page 8）
  quote: "Delta: 按照斜对角对比的原则，K线内部某个价位Delta定义为主动买单量-主动卖单量。在一根K线中的Delta是指主动买单总量减去主动卖单总量。"
  why_kept: 明确定义了Delta的计算方式，是订单流量化中最基础的数值对象
  quant_link: delta, cumulative_delta, per_price_level_delta

- excerpt_id: EXC005
  source_hint: 名词解释（Page 8）
  quote: "吸收：价格原本处于趋势当中，当运行到某个价位出现大量被动型交易者吸收推动趋势运行的主动型交易者的订单，趋势停止，表现为K线Delta值在零值附近波动，成交量放大，趋势停止并在某个价格区间震荡。"
  why_kept: 定义了absorption的核心特征：Delta≈0+成交量放大+趋势停止，是识别吸收区间的关键判据
  quant_link: absorption, delta, volume, range_bound

- excerpt_id: EXC006
  source_hint: 名词解释（Page 8）
  quote: "被套交易者：顶部价位处主动买单成交量显著放大，表示出现大量在上涨趋势的末端买入的交易者，即被套多头交易者。底部价位处主动卖单成交量显著放大，表示出现大量在下跌趋势的末端买入的交易者，即被套空头交易者。"
  why_kept: 定义了trapped trader的识别方法：趋势末端+主动成交量显著放大+价格反向运动
  quant_link: trapped_trader, exhaustion, reversal_signal

- excerpt_id: EXC007
  source_hint: 名词解释（Page 8）
  quote: "微单（Single/small prints): 在一根K线的顶部价位主动买单明显小于低一档价位的主动买单，或者在底部价位的主动卖单明显小于高一档价位的主动卖单，顶底的微小成交，经验比率为大于28。大单（Large prints): 在一根K线的顶部价位主动买单明显大于低一档价位的主动买单，或者在底部价位的主动卖单明显大于高一档价位的主动卖单，顶底的大量成交，经验比率为小于0.699。"
  why_kept: 定义了exhaustion（微单）和block（大单）的量化比率标准，虽然是经验值但提供了具体计算方式
  quant_link: exhaustion, large_prints, small_prints, top_bottom_ratio

- excerpt_id: EXC008
  source_hint: 解读订单流图表（Page 27-28）
  quote: "订单流中的成交量是以对角线的形式排布的，从左至右。K线左侧代表主动卖单的累积成交数量，是主动型卖方的力量体现，右侧是主动买单的累积成交量，是买方的力量体现，通常用这种斜对角对比的方式进行分析。订单流图表只记录已成交的订单数量，也就是主动型买卖单，不记录限价单和未全部成交的订单。"
  why_kept: 定义了footprint chart的基本排布规则与数据边界（只记录已成交主动单，不记录未成交限价单）
  quant_link: footprint_logic, diagonal_comparison, executed_volume_only

- excerpt_id: EXC009
  source_hint: 解读订单流图表（Page 28）
  quote: "订单流并非只是以另一种形式展示成交量和价格，它最大的功能在于分别展现主动型买单和主动型卖单的数量，而不是将它们当成一个整体。而这些信息给订单流足迹上了色——蓝色代表这个价位买单淹没了卖单，紫色代表卖单强势压倒了买单，黑色代表两边处于均衡状态。"
  why_kept: 说明了订单流图表的核心价值在于主动买卖分离，以及着色逻辑
  quant_link: footprint_coloring, bid_ask_separation, market_balance

- excerpt_id: EXC010
  source_hint: Delta的重要性（Page 35-36）
  quote: "Delta被定义为在一根K线内主动买单和主动卖单成交量总和的差值，它是由Tick级别的数据计算而来，我们可以通过它看清谁主导着市场。如果某个时间点Delta很接近0，这就表明当前主动涌入市场的买单和卖单很接近，这个过程通常叫吸收过程，很可能会开启一个新的趋势。"
  why_kept: Delta的数据来源（Tick级）和吸收状态的Delta判据（接近0）
  quant_link: delta, tick_data, absorption_detection

- excerpt_id: EXC011
  source_hint: Delta的重要性（Page 36）
  quote: "如果在标普的迷你期货合约上总成交量为10000，而Delta只有100，这远比在5分钟时间轴上显示的总成交量为1500而Delta为100重要，我们必须意识到我们在用的是什么级别的图表。"
  why_kept: 强调Delta的解读必须结合时间框架与成交量规模，不能孤立看待
  quant_link: delta_normalization, volume_context, timeframe_dependency

- excerpt_id: EXC012
  source_hint: POC（Page 37-38）
  quote: "POC: K线内部的所有价位中买单和卖单成交量总和最大的价位。通过这个功能，我们能够看到哪个点位交易得最激烈，它是在单根K线的顶部、底部，还是停留在中部。大部分时间POC出现在K线的中部，当下跌过程中POC出现在K线相对底部并且收盘在高位时，往往预示着出现了多头力量在推动市场。"
  why_kept: 定义POC并说明其位置判断价值（顶部/底部/中部对应不同市场含义）
  quant_link: poc, volume_profile, price_acceptance

- excerpt_id: EXC013
  source_hint: 主动型交易者（Page 43-44）
  quote: "主动型多头交易者是以市价单买入的交易者；主动型空头交易者是以市价单卖出的交易者。他们的行为被认为是主动，是因为他们按照市场上提供的价格成交，他们已经不想等到价格朝着有利于自己的方向移动一段距离再成交了。"
  why_kept: 从订单类型（市价单vs限价单）定义了主动与被动，是理解订单流行为的基础
  quant_link: aggressive_buying, market_order, initiative

- excerpt_id: EXC014
  source_hint: 被动型交易者（Page 46-47）
  quote: "被动型交易者总是将自己的订单委托在盘口，等着感兴趣的主动型交易者光顾。他们决定在某个特定的点位进入市场，当市场没满足他们要求的时候，他们愿意静静等待。被动型交易者挂的是限价单，而主动型交易者会用市价单与他们进行成交。"
  why_kept: 定义被动交易者及其限价单特征，与主动型交易者形成完整对应
  quant_link: passive_buyer, passive_seller, limit_order, dom

- excerpt_id: EXC015
  source_hint: 被动型交易者（Page 47）
  quote: "被动型交易者通常是机构等主力，他们有左右价格的能力。价格被低估，他们进场收购；价格被高估，他们就开始出货。订单流计算的是主动订单的量，当大量的主动型买单发生在K线顶部或者大量主动型卖单出现在K线底部，这通常预示着被动型交易者在对这个价格提供阻力或支撑，而这些订单大多数情况来自主力。"
  why_kept: 连接被动交易者与机构行为，指出在顶部/底部出现主动成交量放大时，被动方（主力）可能在提供阻力/支撑
  quant_link: passive_institutional, absorption, support_resistance, large_prints

- excerpt_id: EXC016
  source_hint: 市场失衡（Page 51-52）
  quote: "常用的比例阈值通常是250%、300%、400%等。当供需指数显示多方力量强劲，这意味着在这个价格点位，主动买单显著多于主动卖单，它们两者的比值大于供需平衡的阈值。另外，按照拍卖理论，我们拿斜对角线的主动卖单量和主动买单量进行对比，如2.5:1、3:1、4:1的成交量比例。"
  why_kept: 提供了imbalance的比例阈值体系，是量化失衡的基准参数
  quant_link: imbalance_ratio, threshold_setting, auction_theory

- excerpt_id: EXC017
  source_hint: 失衡堆积（Page 53-54）
  quote: "失衡堆积现象的出现对我们有重要意义。当我们看到在出现了连续三个价位以上的供需过度现象时，说明在这个价格区间存在强大的推动力，因此如果价格再次回到这个区间，我们预期相同的推动力会再次出现，它扮演着阻力位和支撑位的角色。"
  why_kept: 明确定义stacked imbalance的连续价位要求（3个以上）及其作为支撑/阻力的逻辑
  quant_link: stacked_imbalance, support_resistance, zone_retest

- excerpt_id: EXC018
  source_hint: 失衡堆积（Page 55）
  quote: "当然如果我们发现图表上出现了堆积区间出现时，也不要高兴得太早，我们还应该观察成交量的大小。如果是价格正处于上涨趋势之中，出现了连续三个价位需求失衡，但是成交量上没有显著的放大，只是主动卖单量相对缩小，我认为这个支撑带可信度并不高，因为它背后没有足够的成交量支撑。"
  why_kept: 强调失衡堆积需要成交量验证，没有成交量放大的堆积可信度低——这是量化时必须纳入的验证条件
  quant_link: stacked_imbalance_validation, volume_confirmation, zone_reliability

- excerpt_id: EXC019
  source_hint: 被套交易者（Page 58-59）
  quote: "如果在接近K线底部出现了供应失衡现象，主动型卖方明显多于买方，但是价格并没有下跌；相反，趋势反转并收盘在高位，这说明被套空头交易者出现了。市场中有句老话：总得有人到了市场底部才交出自己的筹码，而被套空头交易者正是这些到了底部才做空的人。"
  why_kept: 定义了trapped short的识别：底部供应失衡+价格不跌+反收高位，是底部反转信号
  quant_link: trapped_trader, short_squeeze, bottom_reversal

- excerpt_id: EXC020
  source_hint: 被套交易者（Page 59-60）
  quote: "当被套交易者受不了精神的折磨，决定放弃自己亏损的头寸，并且主动型交易者再次积极进入市场，一波新的趋势可能就此开启。传统K线图是无法向我们展示这些被套交易者的存在的。"
  why_kept: 说明trapped trader的止损平仓如何成为新趋势的燃料，以及传统K线无法观测此现象
  quant_link: trapped_trader, stop_loss_cascade, trend_initiation

- excerpt_id: EXC021
  source_hint: 吸收（Page 62-63）
  quote: "市场总是在寻找流动性。这个价格区域使得多空双方能够互相博弈而不至于使价格有太大波动，这个过程叫做吸收。这个价格位置，多空双方都很乐意进行筹码交换，在订单流图表上，主动买方和主动卖方都出现了大量的成交额，而Delta和总成交额的比值却相对较低是这个区间的明显特征。"
  why_kept: 定义absorption的订单流特征：主动买卖大量出现+Delta/总成交额比值低，区别于普通盘整
  quant_link: absorption, delta_volume_ratio, liquidity, range

- excerpt_id: EXC022
  source_hint: 吸收（Page 63-64）
  quote: "吸收现象任何时刻都可能发生。当看到了吸收现象时，我们通常要留意吸收现象之后的价格行为。一波大的趋势总是在吸收现象之后开始，这意味着市场中的买方或者卖方已经建立好了自己的头寸。吸收现象的减弱意味着价格已经可以轻易地在一方力量的带动下启动。"
  why_kept: 说明吸收后的突破是趋势启动信号，吸收减弱意味着一方已建立足够头寸
  quant_link: absorption, range_breakout, position_building, trend_initiation

- excerpt_id: EXC023
  source_hint: 主动出击（Page 65-66）
  quote: "机构交易者主导着趋势，如果在某个价位他们无法达到交易计划的持仓量，则他们对该品种的心理价位会开始发生改变，趋势开始启动，这种现象叫做主动出击。价格在强大的需求下上涨，突破其价值区间，这种现象叫多头主动出击。价格在供应压力下跌破价值区间，这种现象叫空头主动出击。"
  why_kept: 定义initiative（主动出击）的概念及其与价值区间突破的关系
  quant_link: initiative, value_area_breakout, institutional_dominance

- excerpt_id: EXC024
  source_hint: 主动出击（Page 66）
  quote: "当价格开始突破价值区间的时候，观察它的突破行为，大额的成交量预示着机构在主导市场。价值区间突破可以是从上方突破也可以从下方突破，我们需特别关注是否有回应性行为发生，将价格再次带回其原本的价值区间。"
  why_kept: 定义initiative突破需要大额成交量确认，以及responsive（回应性）行为的重要性
  quant_link: initiative, responsive, breakout_volume, value_area

- excerpt_id: EXC025
  source_hint: K线图与订单流（Page 67-68）
  quote: "K线图和柱状图无法展示在一根K线内部到底发生了什么，如果看到一个长阳，并就此判断需求正在涌入市场，这从逻辑上看似无懈可击，但是我们无法知晓这种力量的大小以及他们是否会结束。"
  why_kept: 强调传统K线无法展示K线内部结构，这是订单流存在的根本理由
  quant_link: kline_limitation, intra_bar_structure, footprint_necessity

- excerpt_id: EXC026
  source_hint: K线图与订单流（Page 69-70）
  quote: "在第四根K线内部，2802手主动卖单在3895价位成交，当然Delta值为-473也是卖压出现的信号。所以，即使这是一根阳线，也暗示着卖方的力量大于买方。第五根K线的成交量和第四根K线基本相同的情况下，Delta值进一步减小，价格停止上涨，收了一根上影线。"
  why_kept: 展示具体案例：阳线内部隐藏供应、Delta递减预警、订单流如何提前识别反转
  quant_link: hidden_supply, delta_divergence, bullish_candle_weakness

- excerpt_id: EXC027
  source_hint: K线图与订单流（Page 70）
  quote: "有一种K线走势我很喜欢看到，那就是从订单流上看，K线的影线部分出现供需不平衡，并且影线和K线走势相反，也就是说，如果是阴线，则上影线出现了主动买单多于主动卖单的现象，如果是阳线，那下影线出现了供应失衡堆积现象。"
  why_kept: 描述了一种可识别的订单流模式：影线中的反向失衡，是反转/拒绝信号
  quant_link: wick_imbalance, rejection_pattern, candlestick_internals

- excerpt_id: EXC028
  source_hint: 机构和算法交易（Page 76-78）
  quote: "成交量让他们的所作所为有迹可寻，通过阅读订单流图表，我们可以辨别是否有机构在市场上积极地交易，加入他们行列的人是否越来越多。算法交易从某种角度来说，是一种减小冲击影响的下单方式，简单一点的有冰山算法，复杂的有虚出价系统。"
  why_kept: 指出订单流是识别机构行为的工具，并引入冰山算法/虚出价系统的概念
  quant_link: institutional_footprint, iceberg_order, algorithmic_trading, volume_analysis

- excerpt_id: EXC029
  source_hint: 冰山订单（Page 83-84）
  quote: "冰山订单是投资者玩的一个把戏，用来隐藏投资者的订单。简单点说，冰山订单将订单分割成可以被看到的部分和被隐藏的部分，用于隐藏订单的真实大小。想要侦测冰山订单需要我们关注盘口数据。如果冰山订单隐藏在第一档卖单中，一种侦测冰山的方法是利用高频小额的订单去试探。"
  why_kept: 定义冰山订单及其侦测方法——需要盘口数据（DOM）和高频试探
  quant_link: iceberg_order, dom, order_book_pressure, hidden_liquidity

- excerpt_id: EXC030
  source_hint: 前期高低点（Page 87-88）
  quote: "散户有个根深蒂固的习惯，他们喜欢将止损单放在前期低点再低1〜2个点位，或者前期高点再高1〜2个点位。因此如果价格突破前期低点会触发大量的止损单，而价格没有大幅下跌说明底部出现强大的支撑，存在不同周期下更强大的来自需求力量吸收了这些卖单。"
  why_kept: 描述了liquidity sweep（流动性扫损）机制：止损触发→卖单涌现→被主力吸收→反转
  quant_link: liquidity_sweep, stop_hunt, absorption, key_level_test

- excerpt_id: EXC031
  source_hint: 今日高低点（Page 94-95）
  quote: "当我们观察到顶部出现大单时候，说明有机构交易者进场并愿意满足一切购买者的需求，这种现象通常会在短期内阻止价格的上涨。如果价格之后再次回到该高点，同样没有实现突破，这通常预示着价格疲软，是很好的做空入场点。"
  why_kept: 大单在顶部阻止上涨=供应压倒需求，是locally quantifiable的阻力信号
  quant_link: large_prints, top_rejection, institutional_supply, short_setup

- excerpt_id: EXC032
  source_hint: 今日高低点（Page 96-97）
  quote: "微单在高低点同样重要，特别是当它出现在大单之后。这代表着在高点最后一个多头也放弃了推动价格上涨，或者在低点最后一个坚定的空头也放弃了带动价格下跌。当顶部已经没有更多的买家入场时，上涨趋势会终止并掉头下跌。"
  why_kept: 微单=exhaustion信号，特别是大单之后出现微单，确认力量枯竭
  quant_link: small_prints, exhaustion, trend_termination, follow_through_failure

- excerpt_id: EXC033
  source_hint: 融会贯通（Page 132-133）
  quote: "看到蓝色箭头指向的K线的顶部了吗？这是需求失衡。超过340%的买卖比，在2350处有2834手主动买单量处成交，这些是在上升趋势的最末端才买入的交易者，他们按捺不住自己的情绪，加入到多头的队伍幻想着为这波上涨再加一把力，随后价格下跌过程中出现了供应堆积现象。"
  why_kept: 展示被套多头+需求失衡+供应堆积的复合信号，是顶部反转的典型案例
  quant_link: trapped_trader, demand_imbalance, supply_stacked, composite_signal

- excerpt_id: EXC034
  source_hint: 融会贯通（Page 134-135）
  quote: "我喜欢把入场单放在堆积区域的中部或者接近最后一个价位，紧接着我会将止损单放在堆积区间之外1〜2跳的价位。如果按上图所示，在A点入场如果我们没有做好合理的止盈操作，就会出现价格回踩至止损线，出现小的亏损。"
  why_kept: 提供失衡堆积入场与止损的具体规则（风险1-2跳），这是可量化的风险管理锚点
  quant_link: stacked_imbalance, entry_zone, stop_loss, risk_management

- excerpt_id: EXC035
  source_hint: 订单流应用实例（Page 139-140）
  quote: "我总是在接近顶部或者底部的区域寻找微单，如果价格之前创了新高，当下跌回调再次尝试上涨时，如果顶部出现微单，同时价格无法突破前期高点，说明价格已经上涨乏力，我认为这是绝佳的做空机会。微单的多空成交量比应该至少大于28。"
  why_kept: 微单做空的具体规则：前期高点+回调+微单+无法突破，比率>28
  quant_link: small_prints, high_failure, short_opportunity, ratio_threshold

- excerpt_id: EXC036
  source_hint: 订单流应用实例（Page 140-141）
  quote: "顶部或底部出现大量被动交易者。这种现象叫做大单，它表示顶部的主动买单大于低一档价位的主动买单，或者底部的主动卖单大于高一档价位的主动卖单。对于大单我通常将比例设置为0.699或者更低，理想的状态下应该小于0.5。"
  why_kept: 大单定义与比率阈值，但作者强调还需考虑绝对成交量——无法完全程序化
  quant_link: large_prints, ratio_threshold, absolute_volume, discretion

- excerpt_id: EXC037
  source_hint: 订单流应用实例（Page 142-143）
  quote: "订单流背离。订单流背离和其他的背离现象不太一样，订单流背离的特殊之处在于，我们只能将其当做一个参考，还需要通过别的交易信号进行确认。对于看涨的背离，我们需要走势创造一个相对更低的价格，有正数的Delta值，并且收一根阳线。"
  why_kept: 订单流背离的定义与确认条件，强调不能单独使用——需要多信号验证
  quant_link: delta_divergence, confirmation_required, multi_signal

- excerpt_id: EXC038
  source_hint: 订单流应用实例（Page 143-144）
  quote: "对于大单我通常将比例设置为0.699或者更低，理想的状态下应该小于0.5，这说明顶部的主动买单已经是低一档价位的两倍了。然而，这并不是铁定的，我并不是说只是低于0.5才说明出现大单，我也会考虑在0.5〜0.699之间的比率，并且会将成交量的绝对数值也纳入考虑范畴。"
  why_kept: 作者明确说明这些比率不是铁律，需要结合绝对成交量——这是无法简单编码为硬性规则的原因
  quant_link: ratio_rule, discretion, absolute_volume_context, non_programmable

- excerpt_id: EXC039
  source_hint: 交易计划和资金管理（Page 111-112）
  quote: "合理加仓可以摊平我们的成本价格，将大亏转化为小盈。有一种经常被人们忽略的止损单叫时间止损单，大多数人会用价格止损单来进行止损的操作，如果市场向反方向运动，达到了设定的标准，就平仓止损。而时间止损单是基于时间设置的，一定时间后自动平仓。"
  why_kept: 时间止损概念，在订单流震荡区间中尤为重要，是订单流交易的一个管理工具
  quant_link: time_stop, range_bound, order_flow_management

- excerpt_id: EXC040
  source_hint: 高质量交易机会的特征（Page 130-131）
  quote: "最好的买入情况是市场上涨的过程中出现了需求失衡现象，同时市场突破了之前的吸收区间，价格控制权从空头转移到多头手中，趋势启动。最好的卖出信号是市场上出现了供应失衡，并且跌破了吸收区间，失衡的供应压倒胜过需求。"
  why_kept: 高质量信号的复合条件：失衡+吸收区间突破，控制权转移——是策略化时的核心逻辑框架
  quant_link: high_quality_setup, imbalance, absorption_breakout, control_transfer

- excerpt_id: EXC041
  source_hint: 被动型交易者（Page 47-48）
  quote: "当你看到如下的盘口数据：委买价/委卖价：393.50/393.75 委托量：393.50 500手/393.75 200手。被动型买方在393.50处挂了500手订单，被动型卖方在393.75处挂了200手订单。如果一个挂了10手订单在393.50的投资者无法忍受这种等待，他希望自己的订单立即成交，于是提高了价格，在393.75处买入了10手，他就从被动型买方转变为主动型买方。"
  why_kept: 用具体数字展示DOM盘口结构与主动/被动转化机制，是理解order book pressure的基础
  quant_link: dom, bid_ask_spread, limit_to_market_conversion, order_book_depth

- excerpt_id: EXC042
  source_hint: 介绍订单流（Page 13-14）
  quote: "订单流本质上并不属于任何技术分析流派。技术分析总是在价格走出来后，通过各种图表进行分析预测，它的理论依据是当前的价格反映了所有的市场信息。订单流是一种动态、实时的观测市场演化的分析方法。它的独一无二之处在于，通过市场自身走势，我们能清晰地看见谁在控制着市场。"
  why_kept: 明确区分订单流与传统技术分析，强调订单流的实时性与控制者识别能力
  quant_link: order_flow_vs_ta, real_time, market_control

- excerpt_id: EXC043
  source_hint: 订单流的威力（Page 18-19）
  quote: "订单流帮助我们作出精确的交易抉择。市场健康上涨的时候，赚钱似乎显得很容易，但市场并不总是如你所愿。趋势总是走走停停，甚至掉头。大多数指标都滞后于价格，当市场行为发生变化，你必须尽快适应它。订单流展示的是市场当下发生的一切，因此你可以在机会出现的瞬间抓住它！"
  why_kept: 订单流的核心优势：实时性而非滞后性，捕捉当下发生的市场行为
  quant_link: real_time, lagging_indicator_contrast, immediate_opportunity

- excerpt_id: EXC044
  source_hint: 成交量（Page 33-34）
  quote: "上涨趋势中，主动买单量应该有所增长，这意味着强势的需求横扫了所有价位上挂的卖单。下跌趋势中，主动卖单量应该增长，这意味着卖方正在将自己手中的仓位甩给挂单的买方。而在牛皮市行情下，市场像一块海绵，砸向市场的卖单和买单都被吸收。"
  why_kept: 三种市场状态下的主动成交量特征，是判断趋势健康与震荡的基准
  quant_link: trend_health, aggressive_volume, absorption, market_state

- excerpt_id: EXC045
  source_hint: 理解订单流（Page 24-25）
  quote: "如果深究市场内部结构，其实无非供应和需求，双方博弈造成了价格的涨跌。价格并非由数学公式驱动，只有当供需力量悬殊时，才会产生趋势。指标的滞后性让我们无法在最佳的点位入场以及平仓。"
  why_kept: 重申订单流的核心假设：供需博弈驱动价格，力量悬殊产生趋势
  quant_link: supply_demand, trend_formation, order_flow_premise

- excerpt_id: EXC046
  source_hint: 失衡堆积（Page 54-55）
  quote: "失衡堆积现象的精妙在于它提供了我们一个相对完美的低风险入场点，价格经常会在突破失衡区域后再次回踩该区间，而主动型交易者的再次涌入预示着价格将再次反弹。设置止损点也很简单，只需要将止损单放在失衡堆积区间之外1~2跳的价位即可。"
  why_kept: 失衡堆积的入场逻辑与止损位置，提供了具体可量化的风险管理锚点
  quant_link: stacked_imbalance, entry, stop_loss, risk_reward

- excerpt_id: EXC047
  source_hint: 被套交易者（Page 60-61）
  quote: "直接说被套交易者的449手合约直接导致了市场的反转，这听起来很牵强，更合理的说法是市场情绪在那一刻开始改变，趋势已经无法维持强势了，而被套交易者正是赶在趋势末尾入场的人。"
  why_kept: 作者对trapped trader的审慎表述——不是简单因果关系，而是市场情绪转变的表征
  quant_link: trapped_trader, market_sentiment, correlation_not_causation

- excerpt_id: EXC048
  source_hint: 融会贯通（Page 125-126）
  quote: "订单流交易方法并不是精确的科学理论，我们在交易中仍然要学会灵活变通，紧盯市场形势。成功的交易者都是耐心且自律的，要想成功先练习心态，养成耐心和自律的习惯。"
  why_kept: 作者明确承认订单流不是精确科学，需要主观判断与经验——这是量化时必须正视的边界
  quant_link: discretionary, non_exact_science, experience_boundary

- excerpt_id: EXC049
  source_hint: 融会贯通（Page 122-123）
  quote: "我喜欢那些至少有2:1的盈亏比和不低于50%胜率的交易机会，当然我认为60%左右的胜率是最理想的。"
  why_kept: 作者对交易机会的质量标准，是后续量化系统目标函数的参考
  quant_link: risk_reward, win_rate, opportunity_quality

- excerpt_id: EXC050
  source_hint: VWAP（Page 80-81）
  quote: "VWAP是成交量加权平均价格的缩写，该方法假设市场是有效的，它是衡量交易执行情况的一个基准。VWAP的定义是当前总成交金额与总成交量的比值，VWAP代表了这个时期市场订单的平均成本。"
  why_kept: VWAP的精确定义，是机构执行基准和订单流分析的重要参考线
  quant_link: vwap, execution_benchmark, institutional_reference

- excerpt_id: EXC051
  source_hint: 订单流应用实例（Page 133-134）
  quote: "底部出现了8442手卖单，这个信息犹如一个核弹，因为相比之前价位这个成交量绝对算是巨大的，无疑这是属于主力的行为，有人在这个价格接住了所有抛向市场的卖单，最低档的成交量为26，底部比率为324，远大于我们设定的28，说明所有抛向市场的筹码全部被主力接住。"
  why_kept: 展示大单+微单+被套空头的复合信号实例，具体数值说明判断过程
  quant_link: composite_signal, large_prints, small_prints, trapped_trader, institutional_absorption

- excerpt_id: EXC052
  source_hint: 矛盾信号（Page 128-129）
  quote: "当你基于价格行为入场，但是之后出现了市场反转的信号，可能是支持你入场的原因已经失效了，或者市场另外一方的力量已经形成。相比于反转做空，我更倾向于加仓，因为即使出现了价格下跌的信号，我察觉到C点处接近K线底部出现了大额的成交量，而该价位正是突破价位，说明这个价位涌现出了许多被动型多头投资者，阻止价格下跌。"
  why_kept: 展示矛盾信号处理中的判断逻辑：不机械反转，而是观察支撑位的订单流证据
  quant_link: contradictory_signal, support_validation, add_vs_reverse, discretion

- excerpt_id: EXC053
  source_hint: 介绍订单流（Page 16-17）
  quote: "你不需要有一个应用数学的硕士学位再来学习如何发挥订单流的功效，即使金融学的专家也未必知道答案。订单流仅仅是一个工具，用来帮助投资者作出正确的决策，侦测高低点的强弱，判断卖单和买单的侵略性。"
  why_kept: 作者强调订单流是决策工具而非数学模型，侵略性判断是核心输出
  quant_link: tool_not_model, aggressiveness_assessment, decision_support

- excerpt_id: EXC054
  source_hint: 成交量（Page 34）
  quote: "订单流告诉我们在某个特定的时间框架，某个价位的成交情况。当你继续观察随后的价格走势的时候，你就能决定市场是属于强势还是弱势。传统图表只是将成交量总和与相应的K线一一对应，如果我们在这个基础上，还能看到某根K线内部不同价位的成交量情况，我们就能更加深入市场了。"
  why_kept: 强调订单流的核心能力：时间框架×价位的二维成交量矩阵，而非传统的一维总量
  quant_link: time_price_volume_matrix, intra_bar_detail, depth_of_analysis

- excerpt_id: EXC055
  source_hint: 主动型交易者（Page 44-45）
  quote: "对于每一笔交易，总会出现一个买方一个卖方，一个主动的一个被动的，主动的委托市价单，被动的委托限价单，最终多空双方的交易量是相等的。而供需不平衡表示多方的主动买单量与空方的主动卖单量的比率，当这个比值越过了某个阈值，就造成供需失衡。"
  why_kept: 澄清主动/被动与供需不平衡的关系：每笔交易总量相等，但主动买卖比率可以失衡
  quant_link: active_passive_match, imbalance_ratio, volume_equality_vs_imbalance

## CORE_CONCEPTS

- concept_name: aggressive_buying
  definition_from_text: 以市价单主动买入，按照市场上提供的卖价成交，不愿等待价格回调，希望立刻持有仓位。在订单流图表中表现为某个价位的主动买单远大于主动卖单。
  behavioral_mechanism: 主动型买方涌入市场，吃掉挂单的卖单，推动价格上涨。如果大量主动买单出现在顶部但价格不继续涨，说明遇到被动卖方的阻力。
  data_objects_involved: 主动买单量（aggressive buy volume）、主动卖单量（aggressive sell volume）、市价单成交标记
  quant_boundary: 需要tick-by-tick逐笔数据并区分主动/被动方向。OHLCV分钟K线无法直接观测，仅能粗略代理（成交量放大但不区分方向）。

- concept_name: aggressive_selling
  definition_from_text: 以市价单主动卖出，按照市场上提供的买价成交。在订单流图表中表现为某个价位的主动卖单远大于主动买单。
  behavioral_mechanism: 主动型卖方抛售筹码，与挂单的买方成交，推动价格下跌。底部出现大量主动卖单但价格不跌，说明被动买方（主力）在吸收。
  data_objects_involved: 主动卖单量、主动买单量、市价单成交标记
  quant_boundary: 同aggressive_buying，需要逐笔数据。传统成交量无法区分主动卖与被动卖。

- concept_name: demand_imbalance
  definition_from_text: 根据拍卖理论，斜对角价位对比，某个价位主动买单数量远大于低一档价位的主动卖单数量，表示多头力量强势。本书常用比值3:1（或250%、300%、400%阈值）。
  behavioral_mechanism: 在该价位买方侵略性远超卖方，需求压倒供应，预示价格向上运动或支撑形成。
  data_objects_involved: 每个价格级别的主动买单量、主动卖单量、斜对角对比矩阵
  quant_boundary: 需要footprint级别数据（每K线内按价格级别的主动买卖量）。分钟K线总量无法计算斜对角失衡。

- concept_name: supply_imbalance
  definition_from_text: 斜对角价位对比，某个价位主动卖单数量远大于高一档价位的主动买单数量，表示空头力量强势。常用比值3:1。
  behavioral_mechanism: 在该价位卖方侵略性远超买方，供应压倒需求，预示价格向下运动或阻力形成。
  data_objects_involved: 每个价格级别的主动卖单量、高一档主动买单量
  quant_boundary: 同demand_imbalance，需要逐笔+footprint结构。

- concept_name: stacked_imbalance
  definition_from_text: 连续三个或以上价位出现需求失衡或供应失衡，形成失衡堆积。视为支撑带或阻力带。
  behavioral_mechanism: 在价格区间内某一方力量持续碾压，形成"城墙"效应。价格突破后回踩该区间时，预期原力量会再次出现，提供低风险的入场点。
  data_objects_involved: 连续价格级别的失衡判定序列、失衡方向、K线收盘价相对于堆积区间的位置
  quant_boundary: 需要逐笔+footprint。作者强调还需成交量验证——单纯失衡但无成交量放大则可信度低。需要同时监控Volume与Delta。

- concept_name: delta
  definition_from_text: 在一根K线内主动买单总量减去主动卖单总量的差值。由Tick级别数据计算。单价位Delta为该价位主动买单量-主动卖单量。
  behavioral_mechanism: Delta为正表示多头主导，为负表示空头主导。Delta接近0表示主动买卖力量均衡，可能处于吸收状态。Max/Min Delta表示K线内的力量极值。
  data_objects_involved: Tick级主动买卖量、单K线汇总、Max Delta、Min Delta、Cumulative Delta
  quant_boundary: 严格的Delta需要逐笔数据。可用分钟K线内的大单流向作为粗糙代理，但会丢失Max/Min Delta和价位级别信息。

- concept_name: cumulative_delta
  definition_from_text: 一天内Delta的累积量，显示在图表下方。Cum. Delta/Volume为累积Delta与当天累积总成交量的比值。
  behavioral_mechanism: 反映全天的多空力量净流向。CDV比值可标准化不同成交量规模下的Delta强度。
  data_objects_involved: 逐笔Delta序列、时间聚合、成交量累计
  quant_boundary: 需要逐笔数据。分钟K线可用资金流入流出指标作为概念代理，但精度不足。

- concept_name: absorption
  definition_from_text: 价格原本处于趋势中，运行到某个价位出现大量被动型交易者吸收主动型交易者的订单，趋势停止。K线Delta值在零值附近波动，成交量放大，价格区间震荡。区别于盘整（后者可能由外部因素如节假日、数据公布导致）。
  behavioral_mechanism: 多空双方激烈交换筹码，某一方（通常是机构）在悄悄收集对手盘，等待筹码充足后突破区间。吸收减弱意味着价格可以轻易在一方力量带动下启动。
  data_objects_involved: Delta（接近0）、总成交量（放大）、区间内主动买卖量分布、突破时的成交量与失衡
  quant_boundary: 需要逐笔+Delta计算。分钟K线可用"成交量放大但价格区间收敛"作为粗糙代理，但无法区分是吸收还是外部因素导致的盘整。

- concept_name: trapped_trader
  definition_from_text: 顶部价位处主动买单成交量显著放大，表示大量在上涨末端买入的交易者（被套多头）。底部价位主动卖单显著放大，表示大量在下跌末端做空的交易者（被套空头）。价格反向运动使其被迫平仓。
  behavioral_mechanism: 被套交易者的止损平仓成为新趋势的燃料。顶部被套多头止损→卖出加剧下跌；底部被套空头止损→买入推动上涨。传统K线无法展示此现象。
  data_objects_involved: 顶部/底部主动成交量绝对值、与该K线其他价位对比、趋势末端位置
  quant_boundary: 需要逐笔+footprint。分钟K线可用"顶部放量长上影线"或"底部放量长下影线"作为视觉代理，但无法判断主动/被动构成。

- concept_name: large_prints
  definition_from_text: 在K线顶部价位主动买单明显大于低一档价位的主动买单，或底部主动卖单明显大于高一档价位的主动卖单。经验比率<0.699（理想<0.5）。表示主力在顶/底阻止价格运动。
  behavioral_mechanism: 顶部大单=机构供应阻止上涨；底部大单=机构需求阻止下跌。是绝对成交量与相对比率共同作用的信号。
  data_objects_involved: 顶部/底部相邻两档主动量比率、绝对成交量数值
  quant_boundary: 需要逐笔+footprint。作者明确表示不能仅靠比率，还需考虑绝对成交量大小，无法完全程序化。

- concept_name: small_prints
  definition_from_text: 在K线顶部价位主动买单明显小于低一档价位的主动买单，或底部主动卖单明显小于高一档价位的主动卖单。经验比率>28。表示力量枯竭。
  behavioral_mechanism: 顶部微单=最后一个多头放弃，没有更多买家推动价格；底部微单=最后一个空头放弃。趋势终结信号。大单后出现微单确认力竭。
  data_objects_involved: 顶部/底部相邻两档主动量比率、绝对成交量、前期高点/低点位置
  quant_boundary: 同large_prints，需要逐笔+footprint，且需结合绝对成交量与位置背景。

- concept_name: poc
  definition_from_text: K线内部所有价位中买单和卖单成交量总和最大的价位。是K线内竞争最激烈的点位。
  behavioral_mechanism: POC在K线中部=中性；在顶部+收盘低=看跌（顶部买方被卖方击败）；在底部+收盘高=看涨（底部支撑强劲）。
  data_objects_involved: 每个价位总成交量（主动买+主动卖）、POC位置、收盘价相对POC位置
  quant_boundary: 需要逐笔+价位级成交量。分钟K线可用成交量加权平均价（VWAP of the bar）作为粗糙代理，但非精确等价。

- concept_name: initiative
  definition_from_text: 机构交易者主导趋势，价格突破其价值区间。多头主动出击=价格突破价值区间上沿；空头主动出击=跌破价值区间下沿。需要大额成交量确认。
  behavioral_mechanism: 机构无法满足目标持仓时改变心理价位，用大订单推动价格脱离价值区间。突破后关注是否有回应性行为（responsive）将价格拉回。
  data_objects_involved: 价值区间（通常70%交易量区间）、突破方向、突破成交量、失衡堆积、回踩行为
  quant_boundary: 价值区间可用分钟K线+成交量近似（TPoV近似），但机构意图识别仍需要逐笔数据验证。

- concept_name: responsive
  definition_from_text: 当价格突破价值区间后，另一方将价格带回原价值区间的回应性行为。例如买方在价值区间之下挂限价单等待低价买入，卖方在价值区间之上挂限价单等待高价卖出。
  behavioral_mechanism: 回应性交易者提供反向流动性，可能阻止突破或形成假突破。突破+无回应=趋势延续；突破+强回应=区间延续。
  data_objects_involved: 价值区间边界、突破后价格行为、回踩时的主动/被动成交量、失衡信号
  quant_boundary: 需要逐笔+价值区间定义。分钟K线可近似价值区间，但回应性力量的精确判断需逐笔。

- concept_name: footprint_diagonal_comparison
  definition_from_text: 订单流图表的基本分析原则：K线左侧为主动卖单累积量，右侧为主动买单累积量，按斜对角线方式对比（左下角主动卖 vs 右上角主动买）。
  behavioral_mechanism: 斜对角对比遵循拍卖理论：低价位的主动卖与高价位的主动买对比，判断相邻价格级别的供需传递是否顺畅。
  data_objects_involved: 每根K线内按价格级别的矩阵（左列主动卖、右列主动买）、斜对角元素对比
  quant_boundary: 严格的斜对角矩阵需要逐笔+footprint。任何分钟级代理都会丢失价位级别信息。

- concept_name: order_book_pressure
  definition_from_text: 通过盘口（DOM）观察被动型交易者的限价单分布。被动型买方在低价挂单，被动型卖方在高价挂单。大量被动单聚集在关键价位形成支撑/阻力。
  behavioral_mechanism: 限价单堆积深度决定价格在该价位的受阻程度。冰山订单通过隐藏真实限价单大小来伪装压力。
  data_objects_involved: L2 DOM快照（各价位限价单量）、冰山订单探测、价格触及关键价位的反应
  quant_boundary: 需要L2 DOM实时数据。中国股票Level-1仅提供3秒快照，无法精确探测；期货L2数据更适用。逐笔成交数据无法直接还原DOM，需结合委托簿重建。

- concept_name: liquidity_sweep
  definition_from_text: 价格突破前期高点/低点，触发埋藏在关键价位之外的止损单，形成短暂成交量放大，但随后被反向力量吸收，价格回到原区间。书中描述为"价格突破前期低点触发大量止损单，但价格没有大幅下跌说明底部出现强大支撑"。
  behavioral_mechanism: 主力利用止损单获取流动性（筹码），在触发止损后反向操作。是"stop hunt"的订单流表述。
  data_objects_involved: 前期关键价位、突破时的主动成交量、突破后的价格反应（是否站稳）、吸收信号
  quant_boundary: 需要逐笔+关键价位锚定。分钟K线可识别突破失败形态（如pin bar），但无法确认是止损触发还是普通反转。

- concept_name: exhaustion
  definition_from_text: 趋势末端力量枯竭的信号。在订单流中表现为微单（small prints）：顶部主动买急剧萎缩（比率>28），或底部主动卖急剧萎缩。表示推动趋势的最后一方已放弃。
  behavioral_mechanism: 当顶部/底部没有更多主动交易者跟进，原有趋势失去动力，反转概率增大。大单之后出现微单=确认力竭。
  data_objects_involved: 相邻价位主动量比率、绝对成交量趋势、前期高低点测试次数
  quant_boundary: 需要逐笔+footprint。分钟K线可用"缩量创新高/新低"作为概念代理，但无法区分主动/被动缩量。

- concept_name: absorption_at_bid_ask
  definition_from_text: 在盘口买一/卖一价位出现大量成交但价格不移动，表明该价位的被动单（限价单）正在吸收主动单（市价单）。是吸收现象在微观盘口层面的表现。
  behavioral_mechanism: 当买一/卖一被持续成交但价格不推进，说明该价位存在深厚的隐藏流动性（可能是冰山订单或主力限价单），主动力量被消耗。
  data_objects_involved: DOM买一/卖一挂单量、成交Tick、价格推进速率、逐笔成交中的主动方向
  quant_boundary: 需要L2 DOM + 逐笔撮合数据。Level-1快照无法观测此现象。

- concept_name: iceberg_order_detection
  definition_from_text: 冰山订单将大单分割为可见部分和隐藏部分。侦测方法：以最新卖价小额下单，吃掉卖一后新订单不断涌出，价格无法有效推高，推断该价位存在冰山订单。
  behavioral_mechanism: 机构用冰山订单隐藏真实建仓/派发意图，避免市场跟风。侦测到冰山订单意味着该价位有主力在隐蔽操作。
  data_objects_involved: L2 DOM连续快照、高频小额试探订单、同一价位挂单刷新频率
  quant_boundary: 需要高频L2 DOM + 主动试探能力。普通历史数据无法侦测冰山订单，只能观察其效果（吸收、价格不推进）。

- concept_name: value_area
  definition_from_text: 一天内约70%的交易发生在该区间内，这个区间属于价值区间。是判断价格是否被高估/低估、是否出现initiative/responsive行为的基准。
  behavioral_mechanism: 价格在价值区间内=市场认为价格合理；突破价值区间=某一方用强力改变价格认知；回归价值区间=回应性力量有效。
  data_objects_involved: 日内成交量分布、70%成交量区间边界、价格与价值区间的相对位置
  quant_boundary: 可用分钟K线+成交量近似计算70%成交量区间（TPoV近似），是少数可proxy_quantizable的概念之一，但精确度低于逐笔构建的成交量分布。

## QUANTIZATION_TABLE

| concept | raw_rule_from_text | observable_proxy | data_needed | quant_status | implementation_hint | notes |
|---|---|---|---|---|---|---|
| aggressive_buying | "主动型买方：某个价位主动买单远大于主动卖单" | 单价位主动买量 > 主动卖量×N倍 | tick-by-tick with aggressor flag, per-price-level aggregation | needs_extra_data | 按价格级别汇总逐笔成交，标记主动买/主动卖 | 分钟K线无法区分主动/被动，任何proxy都会丢失方向信息 |
| aggressive_selling | "主动型卖方：某个价位主动卖单远大于主动买单" | 单价位主动卖量 > 主动买量×N倍 | tick-by-tick with aggressor flag, per-price-level aggregation | needs_extra_data | 同上，方向取反 | 同上 |
| demand_imbalance | "斜对角对比，主动买单远大于低一档主动卖单，通常3:1" | 某价位主动买 / 低一档主动卖 ≥ 3 | tick-by-tick with aggressor flag, footprint matrix per bar | needs_extra_data | 构建每根K线内价格×主动买卖矩阵，取斜对角元素计算比率 | 分钟K线总量无法计算斜对角，因为缺少价位级别拆分 |
| supply_imbalance | "斜对角对比，主动卖单远大于高一档主动买单，通常3:1" | 某价位主动卖 / 高一档主动买 ≥ 3 | tick-by-tick with aggressor flag, footprint matrix per bar | needs_extra_data | 同上，方向取反 | 同上 |
| stacked_imbalance | "连续三个价位出现失衡则构成堆积" | 连续3+个价位满足失衡条件 | tick-by-tick with aggressor flag, footprint matrix, imbalance detection | needs_extra_data | 先做单价位失衡检测，再扫描连续序列；需同时验证成交量放大 | 作者强调无成交量放大的堆积可信度低，需Volume作为第二验证维度 |
| delta | "一根K线内主动买单总量-主动卖单总量" | 单K线内大单净流入代理 | tick-by-tick with aggressor flag, bar-level aggregation | needs_extra_data | 逐笔汇总Delta；Max/Min Delta需实时追踪K线内极值 | 可用分钟级资金流入流出作为概念代理，但丢失Max/Min与价位信息 |
| cumulative_delta | "一天内Delta的累积量" | 日内累计大单净流入 | tick-by-tick with aggressor flag, session-level accumulation | needs_extra_data | 从开盘起逐笔累加Delta；CDV需同时累加成交量 | 分钟K线可用累积主力资金作为代理，但口径不同 |
| absorption | "Delta接近0，成交量放大，趋势停止，区间震荡" | 成交量放大但价格区间收敛，RSI中性 | tick-by-tick with aggressor flag, Delta calculation, volume per bar | needs_extra_data | 严格吸收需Delta≈0+Volume↑；可设Delta/Volume比率阈值 | 分钟K线可用"放量横盘"代理，但无法区分吸收 vs 外部因素盘整 |
| trapped_trader_long | "顶部主动买单显著放大，价格不上涨，开始下跌" | 顶部放量长上影线 | tick-by-tick with aggressor flag, top-of-bar volume profile | needs_extra_data | 检测K线顶部价位主动买绝对值是否异常放大，对比该K线其他价位 | 分钟K线proxy仅为视觉模式，无法确认主动买构成 |
| trapped_trader_short | "底部主动卖单显著放大，价格不下跌，开始上涨" | 底部放量长下影线 | tick-by-tick with aggressor flag, bottom-of-bar volume profile | needs_extra_data | 检测K线底部价位主动卖绝对值是否异常放大 | 同上 |
| large_prints | "顶部主动买/低一档主动买 < 0.699，且绝对成交量大" | 顶部相邻价位成交量比率异常 | tick-by-tick with aggressor flag, top-two-level ratio | needs_extra_data | 计算顶部两档主动买比率；作者要求同时考察绝对成交量 | 比率规则硬编码会失效，需结合成交量阈值过滤 |
| small_prints | "顶部主动买/低一档主动买 > 28，力量枯竭" | 顶部相邻价位成交量比率极大 | tick-by-tick with aggressor flag, top-two-level ratio | needs_extra_data | 计算顶部两档主动买比率；需确认前期高点测试背景 | 绝对成交量过低时的比率>28无意义，需设最小成交量阈值 |
| poc | "K线内成交量总和最大的价位" | 单K线成交量加权平均价（VWAP of bar） | tick-by-tick with volume per price level | needs_extra_data | 逐笔按价位汇总成交量，取最大者；追踪POC位置与收盘价关系 | bar VWAP是粗糙代理，但非精确等价，尤其当分布偏斜时 |
| initiative_breakout | "价格突破价值区间，伴随大额成交量" | 价格突破70%成交量区间+成交量放大 | tick-by-tick with aggressor flag, volume profile, value area | needs_extra_data | 先计算价值区间（70%成交量），再检测突破时的主动成交量与失衡 | 价值区间可用分钟K线近似，但突破力度验证需逐笔 |
| responsive_reaction | "突破后被拉回价值区间" | 突破失败，价格回到区间 | tick-by-tick with aggressor flag, post-breakout price action | needs_extra_data | 检测突破后N根K线内的主动买卖方向是否反转 | 分钟K线可识别突破失败形态，但无法确认"回应性"力量构成 |
| order_book_pressure | "被动型交易者在盘口挂单形成支撑/阻力" | 买一/卖一挂单深度 | L2 DOM snapshot, limit order book depth | needs_extra_data | 监控关键价位L2挂单量变化，探测冰山订单需高频试探 | 中国Level-1为3秒快照，无法精确；期货L2更适用 |
| liquidity_sweep | "突破前期低点触发止损，但价格不继续跌" | 假突破/穿刺后快速收回 | tick-by-tick with aggressor flag, key level breakout test | needs_extra_data | 识别关键价位突破时的成交量 spike + 迅速反向 + 失衡信号 | 分钟K线可用pin bar/穿刺形态代理，但无法确认止损触发 |
| exhaustion_top | "顶部微单，没有更多买家" | 缩量创新高 | tick-by-tick with aggressor flag, top-level volume ratio | needs_extra_data | 检测顶部主动买与相邻档位比率>28，且绝对成交量显著下降 | 分钟K线proxy为缩量创新高，但无法区分主动/被动缩量 |
| exhaustion_bottom | "底部微单，没有更多卖家" | 缩量创新低 | tick-by-tick with aggressor flag, bottom-level volume ratio | needs_extra_data | 检测底部主动卖与相邻档位比率>28，且绝对成交量显著下降 | 同上 |
| absorption_at_bid | "买一价位大量成交但价格不推进" | 买一成交量大但价格横盘 | tick-by-tick with aggressor flag, L2 DOM, price tick-by-tick | needs_extra_data | 需DOM显示买一挂单持续被吃掉且价格不跌，推断有隐藏买盘 | 无DOM数据时无法观测，只能从事后footprint推断 |
| absorption_at_ask | "卖一价位大量成交但价格不推进" | 卖一成交量大但价格横盘 | tick-by-tick with aggressor flag, L2 DOM, price tick-by-tick | needs_extra_data | 需DOM显示卖一挂单持续被吃掉且价格不涨，推断有隐藏卖盘 | 同上 |
| footprint_diagonal | "K线左侧主动卖，右侧主动买，斜对角对比" | 无精确代理，丢失结构 | tick-by-tick with aggressor flag, per-price-level matrix | needs_extra_data | 按价格级别构建[主动卖|主动买]矩阵，实施斜对角比率计算 | 任何非footprint数据都无法还原此结构，无可靠proxy |
| delta_divergence | "价格创新低，Delta为正且收阳线；或价格创新高，Delta为负且收阴线" | 价格与资金流入方向背离 | tick-by-tick with aggressor flag, bar-level Delta, OHLC | needs_extra_data | 计算单K线Delta与价格方向是否相反，同时要求收盘价确认 | 分钟K线可用资金流入与价格背离作为代理，但需收盘确认 |
| value_area | "一天内70%交易发生在该区间" | 日内成交量分布70%区间 | minute-level OHLCV, volume profile approximation | proxy_quantizable_now | 用分钟K线构建日内成交量分布，取70%成交量所在价格区间 | 这是少数可用分钟K线+成交量较好代理的概念，但精度低于逐笔构建 |
| vwap | "总成交金额/总成交量" | 标准VWAP | minute-level OHLCV, turnover & volume | proxy_quantizable_now | 逐分钟累计成交金额与成交量，滚动计算VWAP；标准差轨需价格序列 | 标准VWAP可用分钟数据精确计算，但书中强调机构算法可能分时段执行 |
| key_level_test | "价格接近前期高低点、昨日高低点、月度高低点时的反应" | 价格触及关键价位+成交量反应 | tick-by-tick with aggressor flag, volume at key level | needs_extra_data | 在关键价位附近检测主动成交量与失衡信号，判断接受或拒绝 | 关键价位本身可分钟线标注，但"反应"的量化需逐笔 |
| iceberg_detection | "高频小额试探，卖一被吃掉后新订单不断涌出" | 同一价位反复出现大额成交后刷新挂单 | L2 DOM high-frequency snapshot, micro-probe orders | needs_extra_data | 需要实时DOM + 主动下单试探能力；历史数据无法直接侦测 | 属于实时交易操作而非历史回测量化，回测中只能观察冰山效果（吸收） |
| stop_loss_cascade | "被套交易者止损平仓推动新趋势" | 突破关键价位后加速+随后反转 | tick-by-tick with aggressor flag, key level breakout, post-breakout volume | needs_extra_data | 检测突破关键价位后的主动成交量 spike 与随后的反向主动成交量 | 无法从公开数据区分"止损单"与普通市价单，只能推断 |
| institutional_footprint | "通过成交量识别机构积极交易" | 异常大单的连续出现 | tick-by-tick with aggressor flag, large order filter, volume clustering | needs_extra_data | 过滤异常大成交量价位，检测是否伴随失衡、吸收、隐蔽区间特征 | 机构定义模糊，任何量化代理都是推断而非确认 |

## FORMULAS_AND_ALGOS

- formula_id: F001
  name: Delta（单K线）
  formula: Delta = Σ(主动买单量) - Σ(主动卖单量)，在该K线时间区间内按逐笔成交计算
  data_requirement: tick-by-tick逐笔数据，每条成交记录需标记主动买（market buy）或主动卖（market sell）方向
  proxy_or_real: 严格Delta需要逐笔数据。分钟级proxy可用大单净流入作为方向代理，但丢失K线内Max/Min Delta和价位级别信息。
  notes: 书中定义Delta为"由Tick级别数据计算而来"，并强调Max/Min Delta的极值意义。任何不基于逐笔的Delta计算都是近似。

- formula_id: F002
  name: 需求失衡比率（斜对角）
  formula: 需求失衡比率 = 价位P主动买单量 / 价位(P-1)主动卖单量；当比率 ≥ 3.0（或250%/300%/400%阈值）时判定为需求失衡
  data_requirement: footprint级别矩阵——每根K线内每个价格级别分别统计主动买总量和主动卖总量
  proxy_or_real: 需要逐笔+aggressor flag。无精确proxy，分钟K线总量无法还原价位级别斜对角对比。
  notes: 书中使用3:1作为常用阈值，但指出可用2.5:1、4:1等。阈值本身可调整，但结构必须基于footprint矩阵。

- formula_id: F003
  name: 供应失衡比率（斜对角）
  formula: 供应失衡比率 = 价位P主动卖单量 / 价位(P+1)主动买单量；当比率 ≥ 3.0时判定为供应失衡
  data_requirement: 同F002，footprint矩阵
  proxy_or_real: 同F002，需要逐笔+aggressor flag
  notes: 同F002，斜对角结构不可还原。

- formula_id: F004
  name: 失衡堆积检测
  formula: 若连续3个或以上价格级别均满足需求失衡（或供应失衡），则构成需求堆积（或供应堆积）
  data_requirement: 逐价位失衡判定结果序列
  proxy_or_real: 需要逐笔+footprint。分钟K线无法代理，因为缺少价位级别拆分。
  notes: 书中强调堆积需成交量验证——"如果成交量上没有显著放大，只是主动卖单量相对缩小，支撑带可信度并不高"。堆积检测需同时监控总成交量与Delta。

- formula_id: F005
  name: 大单（Large Prints）顶部比率
  formula: 顶部大单比率 = 顶部价位主动买单量 / 顶部次低价位主动买单量；当比率 < 0.699（理想<0.5）时视为顶部大单
  data_requirement: K线顶部两个相邻价格级别的主动买单量
  proxy_or_real: 需要逐笔+footprint。作者明确指出需同时考虑绝对成交量——"如果比率是0.2，但成交量是1:5，很难令人信服"。
  notes: 此规则不能硬编码为程序，因为绝对成交量的"令人信服"标准是主观经验。可作为启发式规则，但需保留人工审查或自适应阈值。

- formula_id: F006
  name: 微单（Small Prints）顶部比率
  formula: 顶部微单比率 = 顶部价位主动买单量 / 顶部次低价位主动买单量；当比率 > 28时视为顶部微单
  data_requirement: K线顶部两个相邻价格级别的主动买单量
  proxy_or_real: 需要逐笔+footprint。绝对成交量过低时比率>28无意义，需设最小成交量阈值过滤。
  notes: 书中阈值28为经验值。微单信号在"前期高点测试失败"背景下更强，需位置过滤。

- formula_id: F007
  name: 吸收区间识别（最小代理）
  formula: 吸收区间 = {连续N根K线满足：|Delta| < ε × Volume，且Volume > Volume_mean，且价格区间宽度 < threshold}
  data_requirement: 逐笔Delta、单K线总成交量、K线价格区间
  proxy_or_real: 需要逐笔计算Delta。分钟级proxy可用"成交量放大+价格区间收窄+RSI中性"作为粗略代理，但无法区分吸收与外部因素盘整。
  notes: 书中区分吸收与盘整的关键是"主动买方和主动卖方都大量出现"（Delta≈0+Volume↑），而外部因素导致的盘整成交量不一定放大。此区分需要逐笔数据。

- formula_id: F008
  name: VWAP（成交量加权平均价）
  formula: VWAP = Σ(成交金额) / Σ(成交量)，从交易日开始逐笔或逐分钟累计
  data_requirement: 逐笔或逐分钟的成交价格与成交量（成交金额=价格×成交量）
  proxy_or_real: 可用分钟K线精确计算。书中VWAP标准差轨需要价格序列标准差。
  notes: 这是书中少数可用常规分钟数据较好计算的概念。但书中提醒"VWAP算法不一定真正接近市场VWAP指标"，且机构可能分时段执行算法（如仅在现货开盘1小时内执行）。

- formula_id: F009
  name: 价值区间（70%成交量区间）
  formula: 将日内所有成交按价格级别排序，从成交量最大的价位向两侧扩展，直到累计成交量达到日内总成交量的70%，所得区间即为价值区间
  data_requirement: 日内每个价格级别的成交量分布
  proxy_or_real: 可用分钟K线近似构建日内成交量分布（TPoV近似），精度低于逐笔但可用。
  notes: 书中定义价值区间为"一天内70%的交易发生在该区间内"。是判断initiative/responsive和主动出击的基准线。

- formula_id: F010
  name: Cumulative Delta / Volume 比率（CDV）
  formula: CDV = Cumulative Delta / Cumulative Volume，显示日内主动买卖力量的净方向强度
  data_requirement: 逐笔Delta累计、逐笔成交量累计
  proxy_or_real: 需要逐笔数据。分钟级可用累积大单净流入/总成交量作为概念代理。
  notes: 书中用CDV标准化不同成交量规模下的Delta强度。是少数可直接计算的比率指标。

- formula_id: F011
  name: POC（Point of Control）定位
  formula: POC = argmax_price(主动买单量 + 主动卖单量)，在单K线内寻找成交量最大价位
  data_requirement: 单K线内每个价格级别的总成交量（主动买+主动卖）
  proxy_or_real: 需要逐笔+价位级汇总。分钟K线可用bar VWAP作为粗糙代理，但POC与VWAP在偏斜分布时不等价。
  notes: 书中强调POC位置（顶部/底部/中部）与收盘价的相对关系是判断信号，而非POC绝对值本身。

- formula_id: F012
  name: 订单流背离（最小定义）
  formula: 看涨背离 = 价格创相对新低 AND 单K线Delta > 0 AND 收盘价 > 开盘价；看跌背离 = 价格创相对新高 AND 单K线Delta < 0 AND 收盘价 < 开盘价
  data_requirement: 逐笔Delta、K线OHLC
  proxy_or_real: 需要逐笔Delta。分钟K线可用价格新低+资金流入为正作为代理，但缺少Delta精确度与开盘收盘方向。
  notes: 书中强调背离"只能当做一个参考，还需要通过别的交易信号进行确认"，且加入收盘开盘关系是为了过滤吸收导致的错误信号。

## NOT_QUANT_YET

1. **微单的"力量枯竭"隐喻**：书中将微单描述为"最后一个多头也放弃了推动价格上涨"，这是典型的行为金融学隐喻，无法直接映射为可稳定计算的规则。比率>28只是经验阈值，但"力量枯竭"本身没有可量化的物理对应。

2. **主力意图揣测**：全书反复出现"机构在隐蔽吸筹"、"主力在这个价位提供支撑"、"有人在这个价格接住了所有抛向市场的卖单"等判断。这些判断基于成交量模式的推断，而非对机构身份的确认。在公开数据中，无法区分"主力"与"普通大户"的订单流特征。

3. **吸收与盘整的主观区分**：书中承认盘整"可能来自市场外部因素（美联储决策、节假日、非农数据）"，而吸收是"市场内部价格行为"。这种区分需要知道外部事件日程并做主观判断，无稳定量化边界。

4. **经验比率阈值的普适性**：28（微单）、0.699（大单）、3:1（失衡）等比率被作者称为"经验比率"，在不同市场（股指期货、螺纹、股票）和不同时间框架下，这些阈值的有效性未经过统计验证。直接硬编码会导致过拟合。

5. **"最小压力点"的主观判断**：作者提出寻找"最小压力点"（用最小可能损失博取最大上涨空间），这是一个交易哲学概念，而非可计算的点位。其具体实现依赖盘感与经验。

6. **情绪与恐慌的量化**：被套交易者的"精神折磨"、"被迫放弃头寸"、"恐慌"等描述是心理层面的机制，无法从订单流数据中直接观测。数据只能显示止损平仓的成交量结果，无法确认其心理动因。

7. **冰山订单的实时侦测**：书中描述的冰山订单侦测方法需要"利用高频小额订单去试探"——这是一种主动交易操作，而非历史回测可实现的量化规则。在回测中只能观察冰山订单的被动效果（吸收、价格不推进），无法主动确认冰山存在。

8. **价值区间的动态性**：书中说价值区间"选择和你交易的时点有密切联系，并不是一成不变的"。这意味着价值区间不是一个静态算法可以一劳永逸定义的，需要根据上下文动态调整。

9. **"神秘力量"的不确定来源**：书中描述当预期走势未发生时的"不寻常力量"，这种力量可能来自任意市场参与者的任意决策，无先验识别方法。只能事后从订单流异常中推断，无法事前预测。

10. **矛盾信号的主观权衡**：当出现矛盾信号时，作者选择"加仓"而非"反转"，依据是"C点底部出现大额成交量"提供支撑。这种权衡依赖多信号的综合判断与经验，没有优先级的固定算法。

11. **大单/微单的绝对成交量"令人信服"标准**：作者明确说"我也会将成交量的绝对数值也纳入考虑范畴"，但从未给出绝对数值的具体阈值。这个标准是语境依赖的，无法全局量化。

12. **订单流交易的"灵活性"**：作者反复强调"订单流交易方法并不是精确的科学理论，我们在交易中仍然要学会灵活变通"。这直接声明了该方法无法被完全编码为固定规则系统。

## NEXT_ACTION

1. **明确数据需求边界**：在F2仓库中建立"订单流数据层级"文档，明确区分Level-1（3秒快照）、Level-2（DOM）、Tick-by-tick（含aggressor flag）三档数据各自能支持哪些概念的可观测性。本书中绝大多数概念需要第三档。

2. **整理中国期货市场Tick数据可用性**：调研中国四大期货交易所（中金所、上期所、大商所、郑商所）的Tick数据是否提供aggressor flag（主动买/主动卖方向标记）。若无此标记，则书中核心概念（Delta、失衡、大单/微单）均无法直接复现，需设计方向推断代理算法。

3. **设计footprint矩阵的最小数据规格**：为后续可能的量化实现，定义footprint chart的最小数据规格：每根K线需包含[价格级别, 主动买成交量, 主动卖成交量, 总成交量]矩阵，以及K线级别的Delta、Max Delta、Min Delta、POC位置。

4. **建立"proxy_quantizable" vs "needs_extra_data" vs "shell_only"的判定清单**：将本书中所有概念按此三档分类，作为F2仓库中"数据可用性→概念可观测性"的映射表，避免在数据不足时强行量化。

5. **保留作者的经验阈值作为超参数框架**：将28、0.699、3:1、70%价值区间等经验阈值记录为可调超参数，而非固定常数。任何后续量化实现应将这些阈值作为需优化或自适应的参数，而非硬编码。

6. **区分"实时交易操作"与"历史回测规则"**：将书中涉及主动试探（如冰山订单侦测）的内容标记为"实时交易专用"，与可回测的被动观察规则（如失衡检测、Delta背离）分开归档。避免将不可回测的操作混入历史策略。

7. **识别本书未覆盖但用户要求的概念**：用户要求提取的"unfinished auction"（未完成拍卖）在本书中未明确出现。需在F2中标注此概念不在本书范围内，并注明如需补充需参考其他订单流资料（如Market Profile或Jigsaw Trading文献）。

8. **建立"复合信号"的记录模板**：书中大量交易决策基于2-3个信号同时出现（如大单+被套交易者+需求失衡）。设计一个复合信号记录模板，用于后续量化时评估多信号组合的信噪比，而非单独优化单个信号。

9. **评估VWAP与价值区间的分钟级代理可行性**：对本书中少数可用分钟K线较好代理的概念（VWAP、价值区间），设计分钟级实现方案，并明确标注其近似误差与适用边界，作为"数据降级"时的 fallback。

10. **标记订单流与量化系统的接口层**：明确本书内容在F2中的角色：它提供的是"可观察对象定义"与"数据需求规格"，而非可直接部署的策略模块。任何策略化尝试需要额外一层"信号编码+参数优化+回测验证"的工作。

11. **保留作者对程序化的明确态度**：在F2中记录作者原话"我是厮杀在市场中的交易员，不是IT码农"，作为后续量化工作时的警示——本书方法的主观性和经验性意味着直接程序化可能面临根本性的信噪比损失。

12. **建立订单流概念与常规技术指标的隔离墙**：确保本书中的订单流概念（Delta、失衡、堆积）在后续量化中不会被强行"翻译"为RSI、MACD、均线等传统指标的组合。书中明确反对这种翻译，订单流是独立的观察维度。

