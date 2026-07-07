## BASIC_INFO
- title: 订单流鼻祖 Mike 53 个策略（视频转录合集）
- author: Mike (订单流鼻祖)
- material_type: 视频教程转录 / 订单流战术讲义
- domain_tags: [order flow, delta, absorption, imbalance, liquidity, exhaustion, footprint, DOM]
- file_scope: 订单流鼻祖Mike 53个策略（53个视频转录 .md 文件）
- source_file_size_mb: 约 0.8 (合并文本)
- retain_mode: RETAINED_EXCERPTS
- current_repo_role: SECONDARY_STRUCTURED_NOTE

## MATERIAL_POSITIONING
- what_this_source_is: 53个短视频的逐字转录与BibiGPT摘要合集，覆盖订单流微观结构分析中的大量概念与实战语境。内容以口语化讲解为主，穿插具体盘口数据（黄金、ES、国债、原油、铂金等）。
- why_in_f2: 这是F2层中订单流微观结构最直接的观察对象来源。Mike在53个视频中反复演示了Delta、Absorption、Imbalance、Thin Prints、POC、Value Area、Supply/Demand等概念在真实价格行为中的具体识别方式，为后续F1的特征工程提供了概念边界与数据需求验证。
- not_a_strategy_book_because: 视频内容并非系统化的策略手册，而是围绕单个概念或场景的战术演示。没有统一的参数体系、没有完整的进出场链路、没有回测逻辑，大量内容依赖实时DOM/Footprint判读，无法直接转化为可回测规则。
- relation_to_order_flow_microstructure: 资料直接对应订单流微观结构的核心对象——逐笔成交中的主动/被动订单、单根K线内的成交量分布、控制点与价值区域的迁移、流动性稀薄区与缺口。这些对象正是F1订单流特征工程需要提取和量化的目标。
- data_footprint_required: 逐笔成交带Aggressor Flag（区分主动买/主动卖）、L2 DOM深度快照（5档以上）、Footprint图表（每根K线内部各价格级别的Bid/Ask成交量）、单根K线的Max/Min/Close Delta、价值区域与POC计算、Cumulative Delta序列。
- source_quality_note: [视频转录质量中等——存在中英混合、口语重复、BibiGPT摘要添油加醋的情况；核心概念密度高，但需区分Mike原话与摘要加工；可提取性良好，因为大量视频专门围绕单一概念展开]

## CONTENT_STRUCTURE
- 按概念主题重新组织（不按视频编号），主要概念类别如下：
  1. Delta 体系：单根Delta、Cumulative Delta、Delta Divergence（价格-Delta背离）、Internal Delta（Max/Min Delta）、Delta极值与阈值着色、Delta Volume
  2. Imbalance 体系：Buying/Selling Imbalance、Stacked Imbalance、Inverse Volume Imbalance、Imbalance Reversal
  3. Absorption & Exhaustion：筹码吸收、Stopping Volume、Exhaustion Prints、流动性耗竭（Liquidity Tapering Off）
  4. 流动性与缺口：Liquidity Sweep / Liquidity Grab、Thin Prints / Zero Prints、Thin Market、Sunday Gap、Thin Prints as Gaps
  5. 市场结构：Basing Market / Sideways、Double Top / Double Bottom、Breakout / False Breakout / Failed Breakout、High of Day / Low of Day
  6. POC 与价值区域：Point of Control (POC)、Prominent POC、Slingshot POC、Value Area、Engulfing Value Area、Abandoned Value Area、Value Area Gap
  7. 供需与参与者行为：Supply / Demand / Supply Pressure、Passive Buyers/Sellers、Aggressive Buyers/Sellers、Fresh Buying / New Money、Closing vs New Positions、Trapped Trader / Stop Run、Other Time Frame Traders
  8. 市场环境与动能：Market Environment / Flow-Driven Market、Choppy vs Trending、Rotation / Balance / Excess、Strong Aggressive Trading、Order-Flow-Generated Support/Resistance

## RETAINED_EXCERPTS

### 摘录 1: Delta 背离与供应入场
- excerpt_id: F2-Mike-001
- source_hint: Video 13 (Recognizing Supply) / 原文段落
- quote: "So as this market is coming down, right, you do have a supply coming into the market now on this one bar by itself... They're trying to get rid of it for whatever reason. Honestly, the reason doesn't matter. What matters is being able to recognize that, Hey, you know what, there's supply coming into the market and you know they're just happy to absorb whatever aggressive buying is there right?"
- why_kept: 明确定义了"supply coming into the market"的识别逻辑——不是看价格方向，而是看大量被动卖盘在吸收激进买盘，且价格无法上涨。这是Delta-Price Divergence的核心机制描述。
- quant_link: 需要逐笔数据区分主动买 vs 被动卖，以及价格对正Delta的反应函数。

### 摘录 2: 吸收的本质是风险转移
- excerpt_id: F2-Mike-002
- source_hint: Video 11 (Absorption) / 原文段落
- quote: "Okay. So you know, there is a nice, there's a transfer of risk between buyers and sellers going on down here. This is what absorption, in my opinion, really looks like, right? Even though you got, you know, it's not small allish delta."
- why_kept: Mike对Absorption的定义——不是 exhausted/trapped 的同义词，而是"transfer of risk"，伴随成交量放大但Delta不一定极端。这是概念边界的关键原文。
- quant_link: 需要单根K线内部各价位的成交量分布，以及Delta绝对值与总成交量的比例关系。

### 摘录 3: 高正Delta但价格不涨 = 供应压力
- excerpt_id: F2-Mike-003
- source_hint: Video 13 (Recognizing Supply) / 摘要+原文
- quote: "当市场出现高正 Delta（积极买盘）但价格却无法上涨甚至下跌时，这往往意味着存在强大的被动卖盘（Passive Sellers）在吸收买入力量，从而预示着潜在的下跌行情。"
- why_kept: 这是反直觉的Delta解读核心——正Delta不是永远看涨。价格对Delta的"反应"才是信号，而非Delta本身。这是量化中需要构建"价格-Delta响应模型"的概念基础。
- quant_link: 需要bar-level的Close价格变化与Delta符号的联合分布统计。

### 摘录 4: 红K线+正Delta的供应含义
- excerpt_id: F2-Mike-004
- source_hint: Video 15 (Price-Delta Divergence) / 原文段落
- quote: "Generally what that means is supply is coming into the market sort of arrest a move you know, from going higher... So I'm just going to leave you a positive delta of 233. Okay? Obviously the delta volume is going to be positive because you got positive delta. Generally what that means is supply is coming into the market sort of arrest a move you know, from going higher."
- why_kept: 直接定义了红K线（价格下跌）伴随正Delta的机理：供应入场阻止上涨。这是Delta Divergence在Swing High位置的识别逻辑。
- quant_link: 需要Ask Volume vs Bid Volume在单根K线内的分解，以及Delta Volume作为辅助验证指标。

### 摘录 5: 反向成交量失衡的定义
- excerpt_id: F2-Mike-005
- source_hint: Video 17 (Inverse Volume Imbalance) / 原文段落
- quote: "It's a stacked imbalance in the opposite direction... what's happening is the market is going up. But as it's going up, you have strong passive buying coming in again to support a market that is going up, right? And generally, you're going to often see the negative delta on the Green candles, right?"
- why_kept: Inverse Volume Imbalance的定义——与市场趋势方向相反的堆叠失衡，由被动订单吸收主动订单形成。这是Gold等Iceberg Order密集市场的典型特征。
- quant_link: 需要逐笔数据识别Stacked Imbalance，以及价格方向与失衡方向的对比规则。

### 摘录 6: 薄打印与零成交不是自动信号
- excerpt_id: F2-Mike-006
- source_hint: Video 21 (Thin Prints) / 原文段落
- quote: "Just not take know every single zero print inside the bar is an automatic signal, right? You want to you know, work other pieces of order flow like said you're generally going to see some selling imbalances if it's a bearish one or some buying imbalances if it's a bullish one. But more importantly, you know you want to see the market start moving in that direction as well."
- why_kept: Mike明确警告：Thin Prints/Zero Prints不是独立入场信号，需要结合Imbalance和市场方向确认。这是概念边界的关键——避免把单一微观结构信号当成触发器。
- quant_link: 需要Thin Prints位置与后续价格方向的联合统计，以及Imbalance在bar内的空间分布。

### 摘录 7: 堆叠失衡的定义与筛选
- excerpt_id: F2-Mike-007
- source_hint: Video 20 (Stacked Imbalances) / 摘要
- quote: "核心概念定义：堆叠失衡是指三个买入或卖出失衡点垂直堆叠排列，这通常是订单流中捕捉机构资金强力入场的重要视觉信号。"
- why_kept: 堆叠失衡的量化定义——3个及以上失衡点垂直堆叠。这是少数有明确数量阈值的概念。
- quant_link: 需要逐笔成交按价格级别聚合，识别相邻价格级别的 imbalance ratio 超过阈值（如3:1或5:1）的连续出现。

### 摘录 8: 堆叠失衡失效规则
- excerpt_id: F2-Mike-008
- source_hint: Video 20 (Stacked Imbalances) / 摘要
- quote: "如果价格在堆叠失衡出现后的3到5根K线内，未能持续推进反而陷入横盘或触及反向堆叠，那么该信号即被判定为失效。"
- why_kept: 这是关于"信号失效"而非"入场规则"的观察——量化中需要定义confirmation window和invalidation条件。
- quant_link: 需要堆叠失衡事件的时间戳、后续N根K线的价格极值与方向统计。

### 摘录 9: Delta极值与收盘Delta的关系（吸收形态）
- excerpt_id: F2-Mike-009
- source_hint: Video 18 (Max Min Delta) / 摘要
- quote: "利用'Delta 吸收形态'捕捉顶部：如果在波段高点位置出现极高的Max Delta，但收盘Delta却远低于此值甚至转负，这表明市场存在严重的吸收行为（Absorption），通常预示着价格即将见顶回落。"
- why_kept: 定义了Internal Delta的一种关键形态：Max Delta极大但Close Delta背离。这是逐笔数据才能观测的微观结构现象。
- quant_link: 需要单根K线运行过程中的Max Delta、Min Delta、Close Delta三个数值序列。

### 摘录 10: Stopping Volume 与成交量占比
- excerpt_id: F2-Mike-010
- source_hint: Video 19 (Stopping Volume) / 原文段落
- quote: "just these two price levels on the midside alone, right, account for about 21% of the volume of the bar... I like to see you know the heavy volume coming in on the bottom midside like you are seeing here, right? I like to get it you know somewhere around 25%, 30% to be great."
- why_kept: Stopping Volume的量化参考——单个或两个相邻价格级别占据整根K线成交量的25%-30%以上。这是明确的占比阈值。
- quant_link: 需要Footprint数据计算每个价格级别成交量占整根K线总成交量的比例。

### 摘录 11: Stopping Volume 不应迷信Delta
- excerpt_id: F2-Mike-011
- source_hint: Video 19 (Stopping Volume) / 摘要
- quote: "不要过度迷信Delta值，因为在存在'吸纳'（Absorption）的情况下，即便出现强劲的反向力量，由于大额挂单被动吸收了所有的激进单，Delta指标可能会产生误导，此时应更侧重于分析成交量分布而非净值。"
- why_kept: 强调了当存在Absorption时，Delta净值的局限性。量化模型中若仅用bar-level Delta做信号，会在这个场景产生系统性偏差。
- quant_link: 需要比较"Delta-only模型"与"Delta+Volume Distribution模型"在Absorption场景下的信号差异。

### 摘录 12: 大额订单的磁吸效应 vs 阻力陷阱
- excerpt_id: F2-Mike-012
- source_hint: Video 1 (Big Size) / 摘要+原文
- quote: "大单是磁铁而非阻力：不要盲目认为大额订单（Big Size）一定会造成价格反弹，在交易大户眼里，大额流动性通常是吸引资金进场的'磁铁'，如果行情能瞬间消化这些大单，反而预示着后续上涨空间巨大。"
- why_kept: 定义了Big Size在订单流中的双重角色——不是简单的阻力/支撑，而是流动性磁吸点。需要观察价格对大单的"反应"而非大单本身。
- quant_link: 需要DOM快照数据记录大单出现前后的价格速度与成交密度变化。

### 摘录 13: 假突破中的Delta陷阱
- excerpt_id: F2-Mike-013
- source_hint: Video 24 (Strong Aggressive Trading) / 摘要+原文
- quote: "当行情已经走出一波趋势后，突如其来的巨量 Delta 往往是诱多或诱空的陷阱，而非入场的信号。"
- why_kept: 定义了Volume Spike / Delta Spike在趋势末端的风险——不是动能延续，而是陷阱。需要结合"位置"（Swing High/Low）来过滤。
- quant_link: 需要Delta极值与历史分位数的对比，以及价格位置（距离日内高低点的百分比）作为过滤条件。

### 摘录 14: 基底市场与价值区域重叠
- excerpt_id: F2-Mike-014
- source_hint: Video 14 (Basing Market) / 原文段落
- quote: "When I see you know like a market sort of going sideways and a bunch of overlapping value, Aries, one, two, three, four, five, you know almost six here... But again, it's don't fall into the trap that it has to be this number or more."
- why_kept: Basing Market的识别逻辑——多个Value Area重叠（5-6个），但Mike强调没有固定数字。这是概念而非规则。
- quant_link: 需要每根K线的Value Area计算，以及连续N根K线Value Area重叠率的时序统计。

### 摘录 15: 流动性枯竭与POC
- excerpt_id: F2-Mike-015
- source_hint: Video 12 (Order Flow in Context) / 摘要
- quote: "当控制点（POC）出现后，若后续紧跟极度稀薄的成交，通常意味着市场流动性被瞬间'扫除'，这是强劲买卖动能的有力佐证。"
- why_kept: 定义了Liquidity Tapering Off的概念——POC之后出现极度稀薄的成交。这是连接POC与Thin Prints的关键语境。
- quant_link: 需要POC位置与后续若干价格级别的成交量序列，识别"POC后成交量断崖"模式。

### 摘录 16: 双顶的成交量验证
- excerpt_id: F2-Mike-016
- source_hint: Video 42 (Double Tops) / 原文段落
- quote: "This double top right anytime we hit a double top or double bottom right, I've always said watch the volume. Me person I find when I have a double top or double bottom, always keep an eye on the order flow. You know ideally I like to see less order flow."
- why_kept: 双顶/双底不是纯形态概念，而是需要Order Flow验证——第二次触顶时成交量应该减少。这是经典的量化可验证假设。
- quant_link: 需要双顶/双底形态识别 + 两次触顶时的bar-level成交量与Delta对比。

### 摘录 17: 日内低点的看涨价值区域
- excerpt_id: F2-Mike-017
- source_hint: Video 10 (Bullish Order Flow at Low) / 原文段落
- quote: "Then right at the . low of the day here. you've got the bullish value area coming in here right? Right at the low... Then you know got a nice ten point rally off that low. I mean, that's why I use these engulfing value areas, especially if you see them coming in at the highs of the lows of the day."
- why_kept: 定义了Engulfing Value Area在Low of Day位置的语境意义——不是独立的买入信号，而是在已知低风险边界（日内低点）处的确认元素。
- quant_link: 需要Value Area的Engulfing判断逻辑（当前bar VA包含前一bar VA）以及Low of Day位置的标记。

### 摘录 18: 跨周期交易者的识别——背离失效
- excerpt_id: F2-Mike-018
- source_hint: Video 22 (Other Time Frame Traders) / 原文段落
- quote: "potentially is a flow driven market, right? A market that's being driven by the longer term traders, right? I'll say the outside traders, but you know the other time frame traders that have the deeper pockets that are you know moving positions around, necessarily adding or taking off."
- why_kept: Other Time Frame Traders的定义——资金深厚、驱动趋势、使短线背离失效的力量。这是关于市场参与者分层的重要概念。
- quant_link: 需要Cumulative Delta与价格的背离统计，以及背离失效率作为OTF介入的代理指标。

### 摘录 19: 跨周期交易者控制下的市场特征
- excerpt_id: F2-Mike-019
- source_hint: Video 22 (Other Time Frame Traders) / 摘要
- quote: "当市场在低位频繁出现正向Delta（Delta Divergence）却无法推动价格反弹，反而持续创新低时，说明市场的反弹仅为散户或短线获利者的平仓行为，缺乏长线资金（Other Time Frame Traders）的强力承接。"
- why_kept: 区分了"短线反弹"与"趋势驱动"——前者是closing positions，后者需要OTF fresh buying。这是订单流中关于"资金性质"的核心概念。
- quant_link: 需要Delta Divergence事件与后续价格路径的联合分布，区分"有效反转"与"失效背离"。

### 摘录 20: 累积Delta背离
- excerpt_id: F2-Mike-020
- source_hint: Video 52 (Cumulative Delta Divergence) / 原文段落
- quote: "One of the things you should be watching is what's culative delta doing, right? Okay, cumulative delta, -3100, -3800, you know, minus know, 5200 here, -53 hundred. So new lows, you know, minus five, 250, right? That's what you're expecting to see, right?... So okay, you're making those new lows. Delta cumulative delta is still stronger, okay? But you're not getting like those really strong bars coming in... cumulative delta is still negative, but it's starting to gain back."
- why_kept: Cumulative Delta Divergence的定义——价格创新低但Cumulative Delta不再同步创新低，甚至回升。这是多时间尺度上的背离概念。
- quant_link: 需要Cumulative Delta序列与价格序列的滚动相关性/背离检测算法。

### 摘录 21: 停止量能与激进交易的结合
- excerpt_id: F2-Mike-021
- source_hint: Video 19 (Stopping Volume) / 原文段落
- quote: "You got the stopping volume on the red candle at the top with the aggressive selling taking place, stopping volume on the bottom of the Green candle with aggressive buying taking place. As far as delta goes, it's I would sort of I don't want to say overlook the delta in this case because, right, remember, if you're going to have stopping volume here on the bside of a Green candle, you could have positive delta."
- why_kept: Stopping Volume与Aggressive Trading的关系——Stopping Volume是被动挂单，Aggressive Trading是主动攻击。两者结合才能确认反转。Delta在这里可能"骗人"。
- quant_link: 需要区分Stopping Volume（高占比的被动成交）与Aggressive Trading（高Delta的主动成交）的独立识别。

### 摘录 22: 稀薄成交量作为缺口
- excerpt_id: F2-Mike-022
- source_hint: Video 28 (Thin Prints as Gaps) / 摘要
- quote: "在流动性充沛的市场（如E-Mini期货）中，利用交易软件将成交量为0或1的区域标记为'Thin Prints'，这些区域往往揭示了市场的关键缺口。"
- why_kept: 将Thin Prints概念与Gap概念直接关联——在订单流视角下，零成交量区域就是缺口。这是微观结构对经典技术分析的重新解释。
- quant_link: 需要单根K线内部各价格级别的成交量分布，识别零成交/低成交价格级别，并统计其后续被"回补"的概率。

### 摘录 23: 枯竭打印在高低点的定义
- excerpt_id: F2-Mike-023
- source_hint: Video 51 (Exhaustion in Heavily Traded Markets) / 摘要
- quote: "寻找swing高低点：这种'耗竭打印'最有效的应用场景是在波段的高点或低点，而非新闻发布或美联储讲话期间，因为后者本身就会导致流动性撤出，从而产生虚假的低成交量。"
- why_kept: Exhaustion Prints的适用语境——必须在Swing High/Low，而非事件驱动流动性撤出的场景。这是概念的应用边界。
- quant_link: 需要Exhaustion Print事件与Swing High/Low位置的联合标记，以及事件前后成交量对比。

### 摘录 24: 内部Delta与虚假突破
- excerpt_id: F2-Mike-024
- source_hint: Video 18 (Max Min Delta) / 摘要
- quote: "Max/Min Delta 记录了K线运行期间，买盘力量（Max Delta）或卖盘力量（Min Delta）达到过的峰值。这对于识别价格是否存在'虚假突破'或'买方/卖方吸收'至关重要。"
- why_kept: Internal Delta的定义——Max/Min Delta是过程中的极值，Close Delta是结果。三者关系定义了虚假突破和吸收。
- quant_link: 需要tick-level的Delta累积序列，以计算单根K线内的Max Delta、Min Delta、Close Delta。

### 摘录 25: 新鲜买盘 vs 清空订单簿
- excerpt_id: F2-Mike-025
- source_hint: Video 37 (Taking Out the Highs) / 原文段落
- quote: "When up here near this high, right? Again, like I said, you know when we're up here near a high, you want to see how it's being made. Is there . fresh buying?... when you're taking all the highs. I see buying balances come in after the high is made. Okay? To me, that's a bit of a sign of fresh buying as kiable things I like to see."
- why_kept: 区分"突破前高时的两种机制"——清空存量订单簿 vs 新鲜买盘持续进入。这是判断突破真实性的核心概念。
- quant_link: 需要突破前高时的Order Flow序列：突破前的失衡 vs 突破后的失衡，以及两者的持续性统计。

### 摘录 26: 平仓 vs 新建仓位
- excerpt_id: F2-Mike-026
- source_hint: Video 36 (Closing vs New Positions) / 摘要
- quote: "当市场猛烈下跌至低位时，如果伴随巨量成交且后续没有持续的做空动能，这往往暗示着这可能是止损离场的平仓行为，而非大规模的新空头进场。"
- why_kept: 区分Closing Positions（平仓/止损）与New Positions（新开仓）——两者在订单流中的区别是后续动能是否持续。这是关于"成交性质"的重要概念。
- quant_link: 需要巨量成交事件后的后续N根K线Delta方向与成交量趋势统计。

### 摘录 27: 高点供应的识别——大成交量+正Delta+ stagnation
- excerpt_id: F2-Mike-027
- source_hint: Video 31 (Highs Not Being Taken Out) / 原文段落
- quote: "I know there's supply coming in here, right? I have bish order flow coming in here. I've already identified that with the value area with the point of control... someone pops in some supply up here, a decent size offer, the 549, and it's absorbing whatever aggressive buying is taking place. That's what's causing the spire to have a nice positive delta of 223."
- why_kept: 供应压力的具体识别案例——549合约的大单在高位吸收买盘，导致正Delta但价格 stagnation。这是Supply + Absorption + Delta Divergence 的三重概念交集。
- quant_link: 需要特定价格级别的成交量突增检测，以及该价格级别与bar-level Delta的关系建模。

### 摘录 28: 流动性稀薄区的参数因地制宜
- excerpt_id: F2-Mike-028
- source_hint: Video 21 (Thin Prints) / 摘要
- quote: "针对不同市场的流动性，设置'稀薄成交量'的阈值至关重要；例如，E-minis的参数设置完全不适用于原油或YM等波动和成交特征截然不同的品种。"
- why_kept: Thin Prints的阈值不能跨品种通用。这是量化实现中的关键约束——每个品种需要独立的参数校准。
- quant_link: 需要分品种的成交量分布统计，以确定各品种的"稀薄"阈值（如0、1、或更高）。

### 摘录 29: 假突破中的内含K线陷阱
- excerpt_id: F2-Mike-029
- source_hint: Video 2 (Explosive Breakouts) / 摘要
- quote: "在预期行情突破时，如果紧接着出现内含K线（Inside Bar），这往往暗示市场缺乏后续跟进动力，极易形成虚假突破，此时应保持观望。"
- why_kept: Inside Bar在突破语境中的含义——不是中性信号，而是"缺乏跟进动力"的虚假突破预警。这是市场结构概念。
- quant_link: 需要Breakout事件后Inside Bar出现的频率统计，以及该组合与后续反转概率的关系。

### 摘录 30: 周日跳空与低流动性开盘
- excerpt_id: F2-Mike-030
- source_hint: Video 4 (Sunday Night Gaps) / 摘要
- quote: "周日晚间开盘时流动性往往较薄，且容易受到周末新闻的影响产生剧烈波动。此时入场属于'盲操作'，极易被瞬间的大幅涨跌反复扫损，等待15分钟左右让市场消化情绪，数据才会更真实可读。"
- why_kept: Sunday Gap的语境——流动性稀薄导致订单流不可读。这不是可交易的信号，而是应该回避的时段。这是关于"数据质量"的边界定义。
- quant_link: 需要时间序列的流动性指标（如成交量、买卖价差、订单簿深度）来标记"不可读时段"。

### 摘录 31: 双重底的成交量萎缩验证
- excerpt_id: F2-Mike-031
- source_hint: Video 41 (Double Bottoms) / 原文段落
- quote: "Anytime you have a double bottom, watch the volume the second time. First time it's 116, second time it's 25. So even the volumes right above it, 519, 320, 390, 294. So what do you got? Well, the second time you hit that double bottom, so to speak, you got a lot less volume, right? People aren't interested. It's selling it down anymore."
- why_kept: Double Bottom的验证逻辑——第二次触底时成交量显著减少。这是经典的Volume Confirmation概念，在订单流中有直接对应。
- quant_link: 需要Double Bottom形态检测 + 两次触底的成交量对比统计。

### 摘录 32: 趋势日中的价值区域向下演化
- excerpt_id: F2-Mike-032
- source_hint: Video 33 (Weakness After Cash Open) / 摘要
- quote: "当反弹幅度一次比一次弱，且价值区域不断向下演化时，这往往是一个'趋势日'的典型特征。"
- why_kept: Value Area的向下演化作为Trend Day的识别特征。这是将微观结构（Value Area）与宏观市场状态（Trend Day）连接的概念。
- quant_link: 需要Value Area中心点（POC）的时序趋势，以及连续Value Area的向下偏移率统计。

### 摘录 33: 幽灵成交量的流动性扫单本质
- excerpt_id: F2-Mike-033
- source_hint: Video 53 (Heavy Volume Out of Nowhere) / 摘要
- quote: "成交量爆发并不意味着市场会立即反转，必须观察市场是在哪里寻找流动性，以及它是如何通过'扫单'行为清算掉订单簿中的挂单的。"
- why_kept: Heavy Volume的本质不是方向信号，而是Liquidity Sweep——清除订单簿中的挂单。需要观察"扫单后"的价格行为。
- quant_link: 需要Volume Spike事件与订单簿深度变化的联合检测，以及扫单后价格的持续性统计。

### 摘录 34: 市场寻找流动性 vs 流动性枯竭
- excerpt_id: F2-Mike-034
- source_hint: Video 50 (Searching for Liquidity vs Lack of Liquidity) / 摘要
- quote: "在重仓高成交量的市场环境下，如果依然出现薄打印，其代表的市场信号价值远高于低成交量环境。"
- why_kept: Thin Prints的信号强度与总体成交量水平相关——高成交量市场中的薄打印更有统计意义。这是信号质量的相对性概念。
- quant_link: 需要Thin Prints与同期总成交量的比值作为信号强度权重。

### 摘录 35: 失衡反转的地理位置规则
- excerpt_id: F2-Mike-035
- source_hint: Video 21 (Thin Prints) / 原文段落
- quote: "Because when you have a zero print in a bar, internally in . the bar. you will generally see selling a balance right if it's bearish zero print or buying a balance if it's a bullish zero print."
- why_kept: Thin Prints与Imbalance的空间关系——零打印附近通常伴随同方向的失衡，但有效的失衡应该在远离薄打印的位置。这是空间布局概念。
- quant_link: 需要bar内部Thin Prints位置与Imbalance位置的空间距离统计。

### 摘录 36: 突破确认需要持续失衡
- excerpt_id: F2-Mike-036
- source_hint: Video 37 (Taking Out the Highs) / 摘要
- quote: "理想的突破不仅是价格上行，更应在创新高后出现持续的买入不平衡，这代表了市场参与者的积极意愿。"
- why_kept: Breakout Confirmation的订单流定义——不是价格突破，而是突破后的持续失衡。这是概念而非规则。
- quant_link: 需要Breakout事件后N根K线内的Buying Imbalance持续出现率统计。

### 摘录 37: 铂金/黄金市场的订单流特殊性
- excerpt_id: F2-Mike-037
- source_hint: Video 26 (Supply and Demand in Order Flow) / 摘要
- quote: "商品市场（如黄金、原油）相比高杠杆的股指期货更能真实反映订单流，因为其参与者目的性更强，且门槛较高，减少了无效的投机噪音。"
- why_kept: 不同市场的订单流质量差异——商品市场散户噪音少，订单流更"纯净"。这是关于数据质量的市场语境概念。
- quant_link: 不同品种的价格-Delta响应函数可能存在系统性差异，需要分品种建模。

### 摘录 38: 价值区域缺口与趋势延续
- excerpt_id: F2-Mike-038
- source_hint: Video 33 (Weakness After Cash Open) / 摘要
- quote: "当市场未能回测之前的价值区域，形成明显的缺口时，这通常是趋势延续的有力信号，意味着当前的价格变动缺乏买方（或卖方）的有效支撑。"
- why_kept: Value Area Gap的概念——未被回测的价值区域缺口表示趋势延续。这是市场结构概念。
- quant_link: 需要连续Value Area之间的缺口检测，以及缺口被回测的时间与概率统计。

### 摘录 39: 搜索流动性中的算法行为
- excerpt_id: F2-Mike-039
- source_hint: Video 30 (High of Day / Market Searching for Liquidity) / 原文段落
- quote: "If you've watched the dome long enough, you know that you know the offers follow with donwhat. The algorithms do all day. That's that's what they're designed to do, is provide that liquidity. But you don't have that aggressive buying coming in because it's moved down so fast."
- why_kept: 算法在流动性提供中的角色——算法跟随价格提供流动性，但极端快速移动时缺乏主动交易。这是关于市场微观结构参与者行为的描述。
- quant_link: 需要极端价格移动时的订单簿深度变化与主动成交比率统计。

### 摘录 40: 订单流生成的支撑与阻力
- excerpt_id: F2-Mike-040
- source_hint: Video 19 (Stopping Volume) / 摘要
- quote: "通过识别K线顶部或底部的'停止成交量'（Stopping Volume）来精准定义支撑与阻力区域。核心逻辑在于寻找占据K线成交量25%-30%甚至更高比例的成交密集区。"
- why_kept: Order-Flow-Generated Support/Resistance的定义——由Stopping Volume（高占比成交密集区）形成，而非传统价格水平。这是微观结构对支撑阻力的重新定义。
- quant_link: 需要每根K线内部的价格级别成交量占比，以及高占比级别的历史回测支撑/阻力效果统计。

## CORE_CONCEPTS

### 1. Aggressive Buying / Aggressive Selling / Initiative vs Responsive
- **definition_from_text**: 激进的买方/卖方指主动以市价单或主动吃单方式发起交易的一方。Delta的正负即反映Aggressive Buying vs Aggressive Selling的净差。Initiative是主动发起方向的一方，Responsive是在已有价格水平反应的一方（如被动限价单）。
- **behavioral_mechanism**: Aggressive订单推动价格移动；当Aggressive Buyers无法推动价格上涨时，说明Passive Sellers在吸收（Absorption）。Responsive交易者的限价单提供了流动性，使Initiative交易者的攻击被消耗。
- **data_objects_involved**: 逐笔成交的Aggressor Flag（主动买/主动卖/无）、单根K线的Bid/Ask成交量分解、Delta。
- **quant_boundary**: 需要逐笔数据或至少带Aggressor Flag的tick数据。仅用bar-level OHLCV无法区分Aggressive vs Passive。

### 2. Absorption / Stopping Volume / Exhaustion
- **definition_from_text**: Absorption是"transfer of risk between buyers and sellers"——在特定价格区间，大量被动挂单完全吸收主动攻击单，价格停滞。Stopping Volume是K线极端位置出现占整根K线25%-30%以上的成交密集区，标志趋势动能被阻止。Exhaustion Prints是Swing High/Low处出现的极端缩量成交（个位数），标志当前方向动能枯竭。
- **behavioral_mechanism**: Absorption是过程（风险转移），Stopping Volume是现象（成交密集阻止价格），Exhaustion是结果（动能耗尽）。三者相关但不等同——Absorption可能伴随高成交量，Exhaustion伴随极低成交量。
- **data_objects_involved**: Footprint（单根K线内部各价格级别的成交量）、单根K线总成交量、各价格级别成交量占比、Delta（辅助）、Swing High/Low位置。
- **quant_boundary**: Absorption需要Footprint级别数据；Exhaustion Prints可以部分用bar-level成交量突降检测，但最好结合Swing High/Low位置。

### 3. Delta / Cumulative Delta / Delta Divergence / Internal Delta
- **definition_from_text**: Delta是单根K线/时间段内主动买成交量与主动卖成交量的差值。Cumulative Delta是Delta的累积序列。Delta Divergence是价格与Delta方向相反（如价格跌但Delta正，或价格涨但Delta负）。Internal Delta（Max/Min Delta）是单根K线形成过程中Delta达到过的极值。
- **behavioral_mechanism**: Delta反映主动攻击力量的净方向；Delta Divergence揭示被动力量正在吸收主动力量（如负Delta但价格上涨=被动买盘吸收主动卖盘）；Max Delta极大但Close Delta转负=Absorption at highs。
- **data_objects_involved**: 逐笔Aggressor Flag、单根K线内Delta的tick-level累积序列（用于Max/Min/Close）、Cumulative Delta序列。
- **quant_boundary**: Delta Divergence可在bar-level近似，但Internal Delta必须需要tick-level数据。Cumulative Delta需要bar-level Delta的累积，容易实现但需确认Aggressor Flag准确性。

### 4. Imbalance / Stacked Imbalance / Volume Cluster
- **definition_from_text**: Imbalance是单根K线内某一价格级别的买方成交量与卖方成交量出现显著比例偏差（如3:1或5:1）。Stacked Imbalance是3个及以上失衡点垂直堆叠。Volume Cluster是成交密集的价格区域（常由多个失衡或高成交量级别形成）。
- **behavioral_mechanism**: Imbalance代表在特定价格级别一方的力量压倒另一方；Stacked Imbalance代表力量在多个相邻价格级别持续，形成"墙"。
- **data_objects_involved**: Footprint数据（每个价格级别的Bid/Ask成交量）、Imbalance Ratio阈值、Stacked Imbalance的最小连续数量（默认3）。
- **quant_boundary**: 需要Footprint或至少逐笔聚合到价格级别的数据。普通bar-level OHLCV完全无法识别。

### 5. Liquidity Sweep / Liquidity Grab / Thin Prints / Zero Prints
- **definition_from_text**: Liquidity Sweep是价格快速突破关键位以触发止损单和挂单，完成筹码换手。Thin Prints/Zero Prints是单根K线内部成交量为0或1的价格级别，代表流动性真空或"缺口"。
- **behavioral_mechanism**: Sweep是主动清除流动性的行为；Thin Prints是流动性缺失的结果。Thin Prints常被后续价格"回补"（如磁铁效应）。
- **data_objects_involved**: 逐笔成交按价格级别聚合、订单簿深度（用于判断Sweep前后的深度变化）、各品种独立的Thin Prints阈值。
- **quant_boundary**: Thin Prints需要Footprint数据；Liquidity Sweep需要L2 DOM数据或至少tick数据观察价格跳跃与成交量关系。

### 6. Trapped Trader / Stop Run / Stop Hunt
- **definition_from_text**: Trapped Trader是被市场假信号诱导入场后被套牢的交易者。Stop Run是价格快速突破关键位以触发止损单（常伴随大量零打印/薄打印）。Stop Hunt是故意制造假突破以猎杀止损的行为。
- **behavioral_mechanism**: Stop Run的特征是快速价格移动+大量薄打印+后续快速反转。Trapped Trader的位置通常位于Swing High/Low的止损密集区。
- **data_objects_involved**: Swing High/Low位置、价格速度（ticks per second）、薄打印密度、反转后的Delta变化。
- **quant_boundary**: 部分可用bar-level数据近似（价格快速突破后反转），但Stop Run的薄打印特征需要tick/footprint数据。

### 7. POC (Point of Control) / Value Area / Control Point
- **definition_from_text**: POC是单根K线或特定周期内成交量最大的价格水平。Value Area是成交量最集中的区域（通常约70%成交量）。Control Point是市场参与者共识最强的价格位置。
- **behavioral_mechanism**: POC是"价值引力中心"；价格远离POC后常有回测。Prominent POC是特别突出的成交量峰值，形成强支撑/阻力。Value Area的重叠表示Basing Market；Value Area Gap表示趋势延续。
- **data_objects_involved**: 单根K线内部的价格-成交量分布（TPO/Volume Profile）、Value Area百分比阈值（默认70%）、POC识别算法。
- **quant_boundary**: 需要bar内部的Volume Profile数据。分钟K线+tick成交量聚合可以计算POC和Value Area，但精度取决于tick数据的完整性。

### 8. Supply / Demand / Supply Pressure / Fresh Buying
- **definition_from_text**: Supply是 Passive Sellers 以限价单形式提供的大量卖盘；Demand是 Passive Buyers 提供的大量买盘。Supply Pressure是当Aggressive Buying无法推动价格时的上方供应状态。Fresh Buying是价格突破新高后仍有持续的新的主动买盘进入，而非仅仅是空头平仓或止损触发。
- **behavioral_mechanism**: Supply vs Demand通过订单流中的成交量分布和Delta反应来识别——不是看价格方向，而是看主动攻击是否被被动方吸收。Fresh Buying的确认需要突破后的持续Buying Imbalance。
- **data_objects_involved**: Bid/Ask成交量分解、Delta方向与价格方向的联合、突破后的Imbalance持续性、POC/Value Area的 bullish/bearish 分类。
- **quant_boundary**: 需要逐笔分解或Footprint数据。普通bar-level数据只能做粗略代理。

### 9. Double Top / Double Bottom / Basing Market / Sideways
- **definition_from_text**: Double Top/Double Bottom是价格两次冲击同一水平；第二次冲击时订单流应该减弱（成交量、Delta、Imbalance减少）。Basing Market是多个Value Area重叠的横向盘整；Sideways是缺乏明确趋势的来回波动。
- **behavioral_mechanism**: 双顶的第二次触顶若订单流减弱=买方枯竭；双底的第二次触底若订单流减弱=卖方枯竭。Basing Market是多空力量激烈交换的蓄力阶段。
- **data_objects_involved**: 形态识别（价格极值）、两次触顶的成交量/Delta/Imbalance对比、Value Area重叠统计。
- **quant_boundary**: 形态部分可用分钟K线近似；订单流验证部分需要Footprint数据。

### 10. Breakout / False Breakout / Failed Breakout / Breakout Confirmation
- **definition_from_text**: Breakout是价格突破关键位。False Breakout是突破后缺乏后续动能（常伴随Inside Bar、无持续Imbalance、无Fresh Buying）。Breakout Confirmation需要突破后的持续失衡和POC/Value Area的迁移。
- **behavioral_mechanism**: 真突破需要订单流持续支持（Fresh Buying + Stacked Imbalance）；假突破是价格突破了但订单流没有跟上，随后反转。
- **data_objects_involved**: 突破方向、突破后的N根K线Imbalance、Value Area是否被回测、Inside Bar出现、Cumulative Delta是否配合。
- **quant_boundary**: 突破事件可用分钟K线检测；确认/证伪需要后续的bar-level或footprint数据。

### 11. High of Day / Low of Day / Session Highs/Lows
- **definition_from_text**: 日内高点/低点是当日价格极值。这些位置是流动性密集区（止损单、止盈单集中），也是订单流分析的关键语境。Mike反复强调在这些位置观察Value Area、Delta Divergence、Absorption。
- **behavioral_mechanism**: HOD/LOD是"低风险边界"的参考——价格接近这些位置时，订单流信号的质量更高，因为市场结构和流动性背景明确。
- **data_objects_involved**: 日内价格极值、极值附近的订单流特征（Delta、Imbalance、Volume Profile）、时间戳。
- **quant_boundary**: HOD/LOD可用分钟K线计算；附近的订单流分析需要tick/footprint数据。

### 12. Thin Market / Extremely Thin Market / Low Liquidity
- **definition_from_text**: 薄市场（Thin Market）是成交量稀少、参与者少、波动不规律的市场（如铂金、部分农产品）。Extremely Thin Market会出现大量零成交时段，导致订单流信号噪音增加。
- **behavioral_mechanism**: 薄市场中单笔大单影响巨大，但Delta分析的"侵略性"逻辑仍然适用——大单是被吸收还是被突破。薄市场需要更长的K线周期（如5分钟）来聚合信号。
- **data_objects_involved**: 品种成交量基线、买卖价差、订单簿深度、零成交/低成交频率。
- **quant_boundary**: 可用bar-level数据计算流动性指标（成交量、价差、深度）来标记薄市场时段。

### 13. Gap / Sunday Gap / Thin Prints as Gaps
- **definition_from_text**: 周日跳空（Sunday Gap）是周末新闻导致的开盘价格跳空。Thin Prints as Gaps是订单流视角下的缺口——价格快速穿过某些价格级别而几乎没有成交，形成"流动性缺口"。
- **behavioral_mechanism**: 跳空后的订单流常不可读（流动性稀薄），需要等待15-20分钟让市场稳定。Thin Prints作为缺口会被后续价格"回补"。
- **data_objects_involved**: 开盘价格缺口、开盘后订单流可读性指标（成交量恢复速度）、Thin Prints的密度与位置。
- **quant_boundary**: 缺口可用分钟K线检测；订单流可读性需要tick数据或流动性指标。

### 14. Market Environment / Choppy Market / Trending Market / Flow-Driven Market
- **definition_from_text**: 市场分为趋势日（Trending，约30%）和非趋势日（Choppy/Sideways，约70%）。Flow-Driven Market是跨周期交易者（OTF）主导的单边行情。Choppy Market中支撑阻力位被轻易突破，传统技术分析失效。
- **behavioral_mechanism**: 判断市场环境是订单流应用的前提——非趋势日中的失衡和背离信号更容易失效。OTF主导时，短线背离反复失效，应顺势而非逆势。
- **data_objects_involved**: 日内价格波动率、趋势强度指标（如ADX）、Value Area重叠率、背离失效频率、Cumulative Delta与价格的趋势一致性。
- **quant_boundary**: 大部分可用分钟K线数据近似。OTF介入的识别可用Cumulative Delta背离失效率作为代理。

### 15. Rotation / Balance / Excess / Strong Aggressive Trading
- **definition_from_text**: Rotation是价格在两个区域之间来回摆动。Balance是Value Area重叠、多空力量均衡。Excess是价格超出Value Area的极端移动（常伴随Exhaustion Prints）。Strong Aggressive Trading是突然出现的大Delta/大成交量单边攻击。
- **behavioral_mechanism**: Rotation和Balance对应非趋势日；Excess和Strong Aggressive Trading对应趋势启动或结束。Strong Aggressive Trading若发生在趋势末端=陷阱。
- **data_objects_involved**: Value Area的重叠/分离、价格超出Value Area的程度、Delta极值与历史分位数、Volume Spike检测。
- **quant_boundary**: 需要Value Area数据（可由Volume Profile计算）和bar-level Delta/Volume数据。

### 16. Order Flow Generated Support and Resistance
- **definition_from_text**: 由订单流中的Stopping Volume、POC、Stacked Imbalance、Thin Prints等微观结构对象自然形成的支撑/阻力区域，而非传统技术分析中的水平线。
- **behavioral_mechanism**: 这些支撑/阻力是"动态的"——由实际成交行为创造，也会随着成交行为的消失而失效。例如：当POC被测试多次后，若后续成交量无法维持，支撑失效。
- **data_objects_involved**: POC位置、Stacked Imbalance位置、Stopping Volume的成交密集区、Thin Prints的缺口位。
- **quant_boundary**: 需要Footprint或Volume Profile数据来计算这些动态水平。

### 17. Fresh Money / New Money Entering Market
- **definition_from_text**: Fresh Money / New Money指价格突破关键位后，有新的主动资金持续进入（表现为突破后的Buying Imbalance、Positive Delta、价格持续上涨），而非仅仅是平仓或止损触发导致的被动移动。
- **behavioral_mechanism**: 突破后的"Fresh Buying"确认需要观察：突破后的K线是否有Buying Imbalance？价格是否持续远离突破位？Cumulative Delta是否配合？
- **data_objects_involved**: 突破事件后的N根K线Imbalance、Delta、Volume、Value Area迁移方向。
- **quant_boundary**: 需要突破后的多根K线数据，可用bar-level近似但最好有Footprint验证。

### 18. Closing Positions vs New Positions
- **definition_from_text**: Closing Positions是平仓行为（如止损、获利了结），通常在价格极端位置出现巨量成交但后续动能不持续。New Positions是新开仓，表现为突破后的持续失衡和趋势延续。
- **behavioral_mechanism**: 平仓行为的特征是"价格移动但订单流不跟"——巨量成交后Delta不持续、价格回到原区间。新开仓的特征是"价格移动且订单流持续"——Delta持续、Value Area迁移。
- **data_objects_involved**: 巨量成交事件后的Delta趋势、Volume趋势、价格是否回到原区间、Cumulative Delta的变化斜率。
- **quant_boundary**: 可用bar-level数据做事件后分析，但需要明确的"巨量"阈值。

### 19. Heavy Volume Out of Nowhere / Volume Spike / Volume Climax
- **definition_from_text**: 突发天量成交（Heavy Volume Out of Nowhere）是成交量突然远超正常水平的现象。Volume Spike可能是Liquidity Sweep、机构大单、或新闻驱动。Volume Climax是趋势末端的天量，常伴随反转。
- **behavioral_mechanism**: 天量本身不是方向信号——需要看天量是如何形成的（扫单？被动吸收？主动攻击？），以及天量后的价格反应。趋势末端的天量+Delta极值=陷阱。
- **data_objects_involved**: 成交量与移动平均的比值、Delta与成交量的比值、Volume Spike后的价格方向、订单簿深度变化。
- **quant_boundary**: 可用bar-level数据检测Volume Spike，但需要后续多根K线数据验证。

### 20. Cross Timeframe Trader / Other Time Frame
- **definition_from_text**: Other Time Frame Traders（OTF）是资金量大、持仓周期长、驱动整体趋势的大型机构。他们的介入使短线背离反复失效，市场进入Flow-Driven模式。
- **behavioral_mechanism**: OTF的识别信号：连续背离失效、Cumulative Delta与价格持续同向、Value Area单向迁移、反弹缺乏Fresh Buying。OTF介入时应顺势交易，设置更宽止损。
- **data_objects_involved**: Cumulative Delta趋势、背离失效频率、Value Area迁移方向、反弹时的Delta/Imbalance质量。
- **quant_boundary**: 可用bar-level数据（Cumulative Delta、价格趋势、背离失效统计）构建OTF介入的代理指标。

## QUANTIZATION_TABLE

| concept | raw_rule_from_text | observable_proxy | data_needed | quant_status | implementation_hint | notes |
|---|---|---|---|---|---|---|
| Aggressive Buying vs Passive Selling | Delta正=主动买强；但价格不涨时，正Delta反映被动卖盘吸收 | 单根K线Delta符号与价格变化方向的不一致率 | tick-by-tick with aggressor flag | needs_extra_data | 计算每个bar的Delta符号与Close-Close方向的一致性，构建"Absorption概率" | 需要Aggressor Flag，否则无法区分主动/被动 |
| Delta Divergence (红K+正Delta) | 红K线伴随正Delta=供应入场阻止上涨 | bar-level Delta > 0 且 Close < Open | bar-level OHLC + Delta | proxy_quantizable_now | 可用分钟K线+Delta近似，但精准度低于逐笔 | 需要验证Delta数据的Aggressor Flag准确性 |
| Inverse Volume Imbalance | 市场涨但出现负Delta=被动买盘吸收卖压 | 价格方向与Delta方向不一致，且bar内有Buying Imbalance | tick-by-tick with aggressor flag + footprint | needs_extra_data | 需要识别Stacked Imbalance方向与价格趋势的相反性 | Gold等市场常见，因Iceberg Orders多 |
| Stacked Imbalance | 3个及以上失衡点垂直堆叠 | 连续N个价格级别的 imbalance ratio > 阈值 | footprint chart per bar | needs_extra_data | 设置imbalance ratio阈值（如3:1），检测连续3+个价格级别 | 阈值可因品种而异 |
| Stacked Imbalance 失效 | 3-5根K线内未推进或触及反向堆叠=失效 | 堆叠失衡事件后N根K线的价格极值与方向 | bar-level OHLC + 堆叠失衡事件时间 | proxy_quantizable_now | 事件后分析窗口，记录推进率与失效率 | 不是入场规则，是信号质量统计 |
| Absorption | 高成交量+横盘+Delta不大=风险转移 | 成交量 > 均值 且 价格范围小 且 Delta绝对值/Volume < 阈值 | bar-level OHLCV + Delta | proxy_quantizable_now | 可用分钟K线近似，但Mike强调Footprint内部分布更关键 | 分钟K线代理会漏掉内部结构细节 |
| Stopping Volume | K线极端位置占25%-30%成交量的成交密集区 | 单根K线内Top N价格级别成交量占比 | footprint chart per bar | needs_extra_data | 需要Volume Profile或Footprint数据 | 普通K线无法计算 |
| Exhaustion Prints | Swing High/Low处的个位数成交量 | 价格极值附近bar的成交量 < 阈值 | bar-level OHLCV + Swing High/Low标记 | proxy_quantizable_now | 需要区分"事件驱动流动性撤"vs"自然枯竭" | 低流动性市场假信号多 |
| Thin Prints / Zero Prints | 成交量为0或1的价格级别 | bar内各价格级别的成交量 = 0或1 | footprint chart per bar | needs_extra_data | 阈值因品种而异（E-mini可设0-1，其他品种需更高） | 不是独立信号，需结合Imbalance和方向 |
| Thin Prints as Gaps | 零成交量区域=流动性缺口，常被回补 | 零成交价格级别与后续价格回归的概率 | footprint chart per bar + 后续价格路径 | needs_extra_data | 统计Thin Prints被后续价格触碰/穿越的概率 | 是订单流视角的缺口定义 |
| POC (Point of Control) | 单根K线成交量最大的价格水平 | bar内成交量最大价格级别 | footprint / volume profile per bar | needs_extra_data | 可用Volume Profile库从tick数据计算 | 分钟K线无内部数据则无法计算 |
| Value Area | 约70%成交量集中的价格区域 | 按成交量排序累积到70%的价格范围 | footprint / volume profile per bar | needs_extra_data | 标准Market Profile计算 | 可用滚动窗口计算 |
| Value Area Gap | 价值区域未被回测的缺口=趋势延续 | 连续bar的Value Area之间是否有不重叠区间 | volume profile per bar | needs_extra_data | 需要Value Area的上下边界序列 | 可用分钟K线Volume Profile近似 |
| Basing Market | 多个Value Area重叠的横盘 | 连续N根K线Value Area重叠率 > 阈值 | volume profile per bar | needs_extra_data | 需要Value Area的重叠检测算法 | 没有固定数字，需统计分布 |
| Double Top 订单流验证 | 第二次触顶成交量<第一次 | 两次价格极值时的bar-level成交量比值 | bar-level OHLCV + 形态识别 | proxy_quantizable_now | 可用分钟K线检测双顶+成交量萎缩 | 需要形态识别算法 |
| Breakout Confirmation | 突破后持续出现Buying Imbalance | 突破事件后N根K线的Buying Imbalance出现率 | bar-level + footprint | needs_extra_data | 需要突破检测+后续Imbalance统计 | bar-level只能近似 |
| False Breakout (Inside Bar) | 突破后Inside Bar=缺乏跟进 | Breakout事件后第1根K线是否为Inside Bar | bar-level OHLC | proxy_quantizable_now | 事件后条件概率统计 | 简单但有效的bar-level代理 |
| High of Day / Low of Day | 日内极值是订单流关键语境 | 日内滚动极值及其时间戳 | bar-level OHLC | proxy_quantizable_now | 可用分钟K线计算 | 附近订单流分析需要额外数据 |
| Cumulative Delta Divergence | 价格创新低但CumDelta不再创新低 | 价格低点序列与CumDelta低点序列的背离 | bar-level Delta累积序列 | proxy_quantizable_now | 滚动窗口检测CumDelta与价格的背离 | 需要bar-level Delta数据 |
| Internal Delta (Max/Min Delta) | Max Delta极大但Close Delta背离=吸收 | 单根K线MaxDelta - CloseDelta的差值 | tick-by-tick with aggressor flag | needs_extra_data | 需要tick-level Delta累积序列 | 是普通K线完全无法观测的微观结构 |
| Fresh Buying at Highs | 突破新高后仍有Buying Imbalance | 突破后N根K线是否有持续Buying Imbalance | bar-level + footprint | needs_extra_data | 需要区分"突破时失衡"vs"突破后失衡" | 是突破真实性的核心验证 |
| Stop Run | 快速突破+薄打印+快速反转 | 价格速度 > 阈值 且 薄打印密度 > 阈值 且 后续反转 | tick data + footprint | needs_extra_data | 需要价格速度、薄打印、反转三要素的联合检测 | 是经典的订单流陷阱模式 |
| OTF (Other Time Frame) 介入 | 连续背离失效=OTF主导 | 背离事件后价格未反转的概率 | bar-level Delta + 价格 | proxy_quantizable_now | 可用Cumulative Delta背离失效率作为OTF代理 | 是参与者结构推断 |
| Liquidity Sweep | 大单扫单清除订单簿流动性 | 大单成交后的订单簿深度变化 | L2 DOM with 5-level depth | needs_extra_data | 需要DOM快照数据 | 仅用tick数据可部分近似 |
| Heavy Volume Out of Nowhere | 成交量突然远超正常水平 | 成交量 / 滚动均值 > 阈值 | bar-level volume | proxy_quantizable_now | 可用分钟K线Volume Spike检测 | 需要后续验证（是否陷阱） |
| Supply Pressure | 正Delta但价格 stagnation | 正Delta + 价格范围小 + 高成交量 | bar-level OHLCV + Delta | proxy_quantizable_now | 可用分钟K线近似 | 需要确认Aggressor Flag方向 |
| Market Environment (Trending vs Choppy) | 非趋势日约70%，趋势日约30% | 日内ADX、Value Area重叠率、价格波动率 | bar-level OHLCV | proxy_quantizable_now | 多指标并列判定/分档，不合成为单一分数 | 是订单流应用的前提条件 |
| Sunday Gap 不可交易时段 | 开盘后15-20分钟订单流不可读 | 开盘后成交量恢复速度 | bar-level volume + time | proxy_quantizable_now | 标记开盘后成交量 < 阈值的时段 | 是数据质量标记而非信号 |
| Closing vs New Positions | 巨量后无持续动能=平仓；巨量后持续=新开仓 | 巨量事件后N根K线的Delta/Volume趋势 | bar-level OHLCV + Delta | proxy_quantizable_now | 事件后时间序列分析 | 需要"巨量"事件检测 |
| Iceberg Orders (黄金等) | 隐藏大单导致负Delta但价格上涨 | 价格上涨时的负Delta频率 | tick-by-tick with aggressor flag | needs_extra_data | 需要逐笔数据识别Iceberg的成交量痕迹 | 是特定市场的结构性特征 |

## FORMULAS_AND_ALGOS

- **Imbalance Ratio**: 原文中常用 3:1、5:1 等比例作为失衡判断。具体阈值需根据品种调整——E-mini等流动性高的品种可用更高阈值，薄市场可用更低阈值。
- **Stacked Imbalance阈值**: 默认3个连续失衡点。Mike强调没有固定数字，需根据品种和图表类型调整。
- **Thin Prints阈值**: E-mini等市场可设0-1，其他品种需根据成交量分布调整。Mike建议：先用一个品种长期观察，建立直觉，再确定参数。
- **Stopping Volume占比**: 单个或两个相邻价格级别占整根K线成交量的25%-30%以上。
- **Delta极值着色阈值**: 95%分位数作为极端Delta的阈值（青色/洋红色标记）。
- **Max/Min Delta与Close Delta差值**: 当Max Delta极大（如+1000）但Close Delta仅+149或转负时，标志Absorption。
- **Cumulative Delta Divergence检测**: 价格创新低时，Cumulative Delta不再创新低甚至回升。注意区分"恐慌性抛售"（CumDelta剧烈下降）vs"衰竭"（CumDelta趋稳）。
- **Volume Spike阈值**: 成交量达到正常水平的20倍（如Video 2中从1.3万手增至2.9万手）。
- **Exhaustion Prints**: 单个价格级别成交量=1或2，出现在Swing High/Low。注意：需与前一根K线的高成交量形成对比（"量能断崖"）。
- **Value Area重叠检测**: 连续5-6个Value Area重叠视为Basing Market。Mike强调：不要陷入数字陷阱，重点是"密集的横向重叠"而非具体次数。

## NOT_QUANT_YET

1. **Absorption的完整识别**: 需要Footprint级别的"风险转移"过程识别，不仅仅是bar-level的成交量和Delta统计。分钟K线无法区分"高成交量+横盘"是Absorption还是普通整理。
2. **Passive vs Aggressive的精确区分**: 没有Aggressor Flag的逐笔数据时，无法区分主动买和被动卖。这是订单流分析的基石，缺失则大量概念无法准确量化。
3. **DOM快照中的大单磁吸效应**: Video 1中的Big Size分析需要L2 DOM实时深度数据，观察大单出现前后的价格速度和成交密度变化。仅用逐笔成交无法完整捕捉。
4. **Iceberg Orders的识别**: 黄金等市场的Iceberg Orders导致Inverse Volume Imbalance。识别Iceberg需要订单簿的隐藏订单检测算法，仅靠成交数据无法完全实现。
5. **Stop Run的薄打印密度**: Stop Run常伴随大量零打印/薄打印，但薄打印本身在事件驱动场景（如FED讲话）中也有大量出现。区分"Stop Run薄打印"与"事件驱动薄打印"需要语境理解。
6. **Closing vs New Positions的精确区分**: 虽然可以用后续动能做代理，但"平仓"和"新开仓"在订单流中的本质区别是交易者的意图，意图无法从成交数据中直接观测。
7. **OTF (Other Time Frame) 的实时识别**: OTF介入的识别依赖背离失效的统计，但"失效"需要事后确认，实时判断仍存在滞后和误判。
8. **市场环境的实时分类（Trending vs Choppy）**: 原文提到非趋势日占70%，但实时判断市场环境仍是一个统计推断问题，没有单一的订单流指标可以100%准确分类。
9. **Supply/Demand的强度度量**: Mike强调"supply coming in"的识别依赖具体价格级别的成交量分布和POC/Value Area的配合。没有一个统一的数值公式可以度量"Supply Pressure"。
10. **Exhaustion Prints在事件场景的过滤**: Exhaustion Prints在新闻发布期间会大量出现（流动性撤出），但Mike明确说这不是有效信号。区分自然枯竭与事件驱动枯竭需要外部事件时间线。
11. **False Breakout的Inside Bar过滤**: 虽然Inside Bar可以检测，但"突破后Inside Bar"作为假突破的充分条件并不成立——需要结合订单流确认。分钟K线只能提供必要条件的代理。
12. **Fresh Buying的严格验证**: Mike的突破确认需要"突破后的持续Buying Imbalance"，但Imbalance本身需要Footprint数据，且"持续"的定义（N根K线？什么阈值？）需要大量统计校准。

## NEXT_ACTION

1. **获取逐笔带Aggressor Flag的tick数据（如ES、GC、ZN等）**：验证Delta Divergence、Imbalance、Absorption等概念在A股/国内期货的可计算性。这是后续所有订单流量化的前提。
2. **建立Footprint数据的生成pipeline**：从逐笔成交数据聚合为每根K线内部各价格级别的Bid/Ask成交量，以支持POC、Value Area、Stacked Imbalance、Thin Prints的计算。
3. **分品种的Thin Prints阈值统计**：对E-mini、黄金、原油、国债、A股主要品种分别统计成交量分布，确定各品种的"稀薄"阈值（0、1、2、或更高）。
4. **构建Delta Divergence事件库**：标记所有价格方向与Delta方向不一致的bar，统计这些事件后的价格分布（是反转、横盘还是继续原趋势？），区分有效背离与失效背离。
5. **Cumulative Delta背离检测算法开发**：实现滚动窗口内的Cumulative Delta与价格背离检测，区分"恐慌性抛售"（CumDelta剧烈下降）vs"衰竭"（CumDelta趋稳）。
6. **Volume Spike事件后分析**：标记所有成交量突增事件（>滚动均值X倍），统计事件后N根K线的Delta方向、Volume趋势、价格回归率，区分"平仓行为"vs"新开仓行为"。
7. **Stacked Imbalance的自动识别与有效性统计**：实现Footprint级别的Stacked Imbalance检测，记录事件后的推进率、失效率，建立信号质量基准。
8. **POC/Value Area的实时计算与缺口检测**：实现Volume Profile算法，计算每根K线的POC和Value Area，检测Value Area Gap，统计缺口被回测的概率与时间。
9. **Stop Run模式检测原型**：基于价格速度+薄打印密度+Swing High/Low位置，构建Stop Run的检测原型，并与后续反转事件做联合统计。
10. **Double Top/Bottom的订单流验证**：结合形态识别与两次触顶的成交量/Delta/Imbalance对比，建立订单流验证层。
11. **市场状态分类器（Trending vs Choppy）**：基于ADX、Value Area重叠率、背离失效率、Cumulative Delta趋势一致性，构建市场环境分类器，作为订单流信号的前置过滤条件。
12. **A股/国内期货的订单流数据可用性调研**：确认国内L2数据的深度、Aggressor Flag的可用性、以及Footprint/Volume Profile的可计算性。这是决定这些概念能否迁移到A股的关键。
13. **Big Size/Liquidity Sweep的DOM数据需求评估**：评估是否需要L2 DOM快照数据来支持大单磁吸效应和流动性扫单的量化，或仅用tick数据是否足够。
14. **建立"概念-数据需求-实现状态"映射表**：跟踪每个订单流概念的数据依赖和实现进度，确保不将needs_extra_data的概念强行用分钟K线代理。


