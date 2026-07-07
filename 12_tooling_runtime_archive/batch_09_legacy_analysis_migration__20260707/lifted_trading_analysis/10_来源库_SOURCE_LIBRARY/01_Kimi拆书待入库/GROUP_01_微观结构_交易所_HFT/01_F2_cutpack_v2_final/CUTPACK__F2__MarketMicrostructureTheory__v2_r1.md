## BASIC_INFO
- title: Market Microstructure Theory
- author: Maureen O'Hara
- material_type: 学术专著/教材
- domain_tags: [market microstructure, asymmetric information, liquidity, market making, price formation, adverse selection, inventory models, bid-ask spread, strategic trading, order flow]
- file_scope: Market Microstructure Theory (Maureen OHara) .epub / .pdf
- source_file_size_mb: 9.24 (PDF) / 0.31 (EPUB)
- retain_mode: RETAINED_EXCERPTS
- current_repo_role: SECONDARY_STRUCTURED_NOTE

## MATERIAL_POSITIONING
- what_this_book_is: Maureen O'Hara 1995年出版的经典微观结构理论教材，系统梳理了从库存模型（Garman, Stoll, Ho-Stoll）、信息模型（Bagehot, Copeland-Galai, Glosten-Milgrom, Easley-O'Hara）到策略交易者模型（Kyle, Admati-Pfleiderer, Foster-Viswanathan）的完整理论谱系。本书是金融学中市场微观结构理论的奠基性著作之一。
- why_in_f2: F2需要理解"价格如何形成"的理论底座，而不是仅仅知道"价格是什么"。O'Hara提供了信息不对称、交易动机、流动性提供、价差分解、做市行为的机制解释，这些是所有后续盘口/订单流/执行成本研究工程化的前置理论层。
- not_a_strategy_book_because: 本书是纯理论建模，没有任何可回测的交易规则、信号生成逻辑或参数优化。所有模型都是简化到极致的理论抽象（如单期、单资产、风险中性做市商、零库存成本等），与实盘tick数据的复杂性差距极大。
- relation_to_order_flow_microstructure: 本书的理论对象是F2中订单流/盘口研究的理论底座。例如：Glosten-Milgrom的序贯交易模型解释了为什么买卖价差存在；Kyle模型中的λ（市场深度参数）是后续所有订单流价格影响模型的起点；Easley-O'Hara的"信息事件不确定性"是后续VPIN（Volume-synchronized Probability of Informed Trading）等指标的源头。
- data_footprint_required: 需要tick/trade-and-quote (TAQ) 数据、订单簿数据、做市商库存数据、价差分解的面板数据。本书的理论本身不直接产生数据需求，但其验证需要高频微观结构数据。

## CONTENT_STRUCTURE

1. **Chapter 1: Markets and Market Making**
   - F2关联：引入市场微观结构的基本问题——价格如何形成。区分Walrasian拍卖与现实交易机制（NYSE、东京、伦敦）。为后续理论提供市场制度背景。

2. **Chapter 2: Inventory Models**
   - F2关联：Garman的破产模型、Amihud-Mendelson的库存-价格联动、Stoll的价差分解（库存风险+订单处理成本+逆向选择）、Ho-Stoll的多期动态规划。库存理论是价差的"非信息"解释。

3. **Chapter 3: Information-Based Models**
   - F2关联：Bagehot的逆向选择直觉、Copeland-Galai的单期信息模型、Glosten-Milgrom序贯交易模型（贝叶斯学习、鞅性质、价差的信息来源）、Easley-O'Hara的扩展（交易规模、分离/混同均衡、信息事件不确定性）。这是F2最核心的章节。

4. **Chapter 4: Strategic Trader Models I: Informed Traders**
   - F2关联：Kyle的单期拍卖模型（线性均衡、市场深度λ、订单流价格影响）、Kyle连续拍卖模型、多知情交易者的竞争效应（Holden-Subrahmanyam）、交易机制与理性预期均衡的关系。

5. **Chapter 5: Strategic Trader Models II: Uninformed Traders**
   - F2关联：Admati-Pfleiderer的流动性交易者集中交易（clumping）行为、Foster-Viswanathan的跨日模式、Spiegel-Subrahmanyam的套期保值动机。解释成交量与价格波动的时间模式。

6. **Chapter 6: Information and the Price Process**
   - F2关联：Brown-Jennings-McNichols的成交量-价格关系、Diamond-Verrecchia的卖空约束与价格调整、Easley-O'Hara的"无交易即信息"理论。时间本身作为价格调整的信号。

7. **Chapter 7: Market Viability and Stability**
   - F2关联：Glosten的垄断做市商与市场竞争性、Madhavan的集合竞价vs连续竞价、Rock的限价订单簿"逆向选择"问题、Easley-O'Hara的止损订单与市场稳定性。1987年崩盘的机制解释。

8. **Chapter 8: Liquidity and the Relationships Between Markets**
   - F2关联：Grossman-Miller的流动性即时性价格、Pagano的内生流动性与市场规模、Chowdhry-Nanda的多市场竞争与信息揭示、Burdett-O'Hara的大宗交易辛迪加、Seppi的非匿名交易与"不打街"约束。

9. **Chapter 9: Issues in Market Performance**
   - F2关联：市场透明度（Madhavan、Pagano-Roell）、交易者匿名性、市场设计问题。制度层面的微观结构分析。

## RETAINED_EXCERPTS

1. **excerpt_id**: OH_001
   **source_hint**: Chapter 1, p. 5-6 / Demsetz section
   **quote**: "Demsetz began with the simple observation that trade may involve some cost... These implicit costs, referred to as the price of immediacy, arose because, unlike in the Walrasian auction, trading had a time dimension."
   **why_kept**: 定义了"即时性价格"（price of immediacy），这是后续所有流动性成本度量的理论起点。Demsetz模型是价差存在的最基础解释。
   **quant_link**: 价差 = 即时性成本; 可用买卖价差作为代理变量。

2. **excerpt_id**: OH_002
   **source_hint**: Chapter 2, p. 15 / Garman model
   **quote**: "Orders are assumed to be for one unit of the stock... The uncertainty in the model arises from the arrival of the buy and sell orders. These orders are represented as independent stochastic processes, where the arrivals of buy and sell orders are assumed to be Poisson distributed."
   **why_kept**: Garman模型是库存类模型的起点：订单流作为随机过程、做市商的破产/失败问题。奠定了"订单流冲击→库存失衡→价格调整"的逻辑链。
   **quant_link**: 订单到达率λ_a(p), λ_b(p); 泊松过程假设排除了信息驱动的订单流。

3. **excerpt_id**: OH_003
   **source_hint**: Chapter 2, p. 25 / Stoll model
   **quote**: "Stoll focuses on determining the costs the dealer faces in providing dealer services... These costs arise from three sources. First, there are holding costs imposed by the suboptimal portfolio position... Second, there may be order-processing costs... Third, a cost may arise from trading with individuals who know more about the stock than the dealer."
   **why_kept**: Stoll的三重成本分解是价差分解（spread decomposition）的基石：库存成本 + 订单处理成本 + 逆向选择成本。后续所有实证价差分解都源于此。
   **quant_link**: 价差 = 库存成分 + 订单处理成分 + 逆向选择成分。可通过高频数据（如Effective Spread、Realized Spread、Price Impact）进行分解。

4. **excerpt_id**: OH_004
   **source_hint**: Chapter 2, p. 28
   **quote**: "The dealer is compensated for bearing these costs through his trading prices... The linearity of percentage costs in trade size means that the spread increases linearly with trade size. And, as the spread equation does not include inventory as an argument, this spread does not change in response to the dealer's trades."
   **why_kept**: Stoll模型预测：库存影响价差的"位置"（placement），但不影响价差的大小。这是一个可检验的假设，但后续实证发现库存效应在短期更复杂。
   **quant_link**: 价差大小 ~ f(交易规模); 价差位置 ~ f(库存水平)。可用逐笔库存数据检验。

5. **excerpt_id**: OH_005
   **source_hint**: Chapter 2, p. 35-36 / Ho-Stoll
   **quote**: "Ho and Stoll demonstrate three important properties of the dealer's optimal pricing behavior. First, the spread depends on the time horizon of the dealer... Second, this risk adjustment depends on the dealer's coefficient of relative risk aversion, the size of the transaction, and the risk of the stock... Third, the spread is independent of the inventory level."
   **why_kept**: Ho-Stoll多期模型扩展了Stoll的直觉：价差=风险中性价差+风险调整。时间 horizon、风险厌恶、交易规模、股票波动率都进入价差。但"价差独立于库存"这一预测与Stoll一致。
   **quant_link**: 日内价差模式（U型或递减型）可用时间horizon解释；需做市商风险厌恶参数（不可直接观测）。

6. **excerpt_id**: OH_006
   **source_hint**: Chapter 3, p. 53 / Bagehot
   **quote**: "Bagehot's starting point was noting that there is a distinction in the market between market gains and trading gains... This information loss arises because of the presence in the market of traders who have superior information."
   **why_kept**: Bagehot 1971是信息模型的起点。区分了"市场收益"（市场涨跌）和"交易收益"（信息优势）。核心洞见：做市商在与知情者交易时总是亏损，必须从不知情者那里赚回。
   **quant_link**: 不知情者的交易损失 = 知情者的信息租金；可通过交易后价格漂移（post-trade price drift）度量。

7. **excerpt_id**: OH_007
   **source_hint**: Chapter 3, p. 56-57 / Copeland-Galai
   **quote**: "The most important result that emerges from this model is that even with risk neutral, competitive dealers, a spread arises. The size of this spread differs with various market parameters... As long as there is a positive probability that some traders are informed, however, the spread is never zero."
   **why_kept**: Copeland-Galai首次形式化了Bagehot的直觉：信息成本本身就能产生价差，无需库存风险、市场势力或交易费用。价差是逆向选择（adverse selection）的补偿。
   **quant_link**: 价差 ∝ 知情交易者概率; 知情交易比例越高，价差越大。可用VPIN或PIN指标作为知情交易概率的代理。

8. **excerpt_id**: OH_008
   **source_hint**: Chapter 3, p. 60-61 / Glosten-Milgrom
   **quote**: "The specialist in the Glosten-Milgrom model sets prices such that the expected profit on any trade is zero... bid and ask prices are 'regret-free' in the sense that given the trade that actually occurs the market maker believes the price is fair."
   **why_kept**: Glosten-Milgrom的核心机制：零利润竞争、价格等于条件期望（"无悔价格"）、贝叶斯更新。这是序贯交易模型的基准框架。
   **quant_link**: 买卖价 = E[V|交易类型]; 交易后价格更新 = 贝叶斯后验。可用高频交易数据检验价格对买卖方向的响应。

9. **excerpt_id**: OH_009
   **source_hint**: Chapter 3, p. 64
   **quote**: "A second important result of the model is that transaction prices form a Martingale. The stochastic process of prices follows a Martingale with respect to the market maker's information if E[p_{t+1} | I_t] = p_t... This property is important because it suggests a linkage between the price behavior in the model and the concept of market efficiency."
   **why_kept**: Glosten-Milgrom证明：在信息不对称下，交易价格仍然是鞅（半强有效），但一阶差分不再独立（与Roll 1984的负自相关不同）。这改变了价差的实证估计方法。
   **quant_link**: 交易价格一阶差分 ~ 鞅但非i.i.d.; Roll的价差估计量不再适用。需要Glosten-Harris分解。

10. **excerpt_id**: OH_010
    **source_hint**: Chapter 3, p. 65
    **quote**: "Another result that arises from the Glosten and Milgrom model is that under some conditions the adverse selection induced by asymmetric information can cause the market to collapse or shut down... If there are too many informed traders, then the market maker may have to set the spread so large as to preclude any trading at all."
    **why_kept**: 市场崩溃（market collapse）机制：逆向选择太严重→价差太大→不知情者退出→市场关闭。这解释了交易暂停（trading halts）和柠檬市场问题。
    **quant_link**: 市场崩溃阈值 = f(知情者比例, 不知情者弹性); 可用极端市场条件下价差爆炸与成交量枯竭的模式验证。

11. **excerpt_id**: OH_011
    **source_hint**: Chapter 3, p. 66-72 / Easley-O'Hara trade size
    **quote**: "Informed traders are assumed to be risk neutral and trade to maximize their expected profits... trade size induces an adverse selection problem, because at the same price the informed trader always prefers to trade larger quantities."
    **why_kept**: Easley-O'Hara将交易规模引入信息模型：知情者偏好大交易→规模成为信息信号→分离/混同均衡。这是大宗交易（block trades）价格效应的理论基础。
    **quant_link**: 价差随交易规模增加; 大交易后价格恢复（partial recovery）模式。可用交易规模与价格冲击的横截面关系检验。

12. **excerpt_id**: OH_012
    **source_hint**: Chapter 3, p. 71-72 / "existence uncertainty"
    **quote**: "If there is uncertainty over the existence of information, then even an uninformed trade can have information value, because it may signal that no new information exists... A small trade following a block trade thus causes the market maker to revise downward his belief that there is new information."
    **why_kept**: "信息事件不确定性"（existence uncertainty）是Easley-O'Hara的核心贡献。区分了"信息方向"（Direction）和"信息存在"（Existence）。小交易在信息存在不确定性下具有信息内容——它暗示可能没有信息事件。
    **quant_link**: 大宗交易后的小交易导致价格恢复（price recovery）; 这不同于Glosten-Milgrom（无恢复）。可用大宗交易前后的价格路径检验。

13. **excerpt_id**: OH_013
    **source_hint**: Chapter 3, Appendix / Bayesian Learning
    **quote**: "The posteriors converge almost surely to the true value; and the posteriors of a Bayesian observing an independent and identically distributed process over time converge exponentially... So [Pr{V=V|b,s}] converges exponentially at rate -I_q(p) to zero almost surely."
    **why_kept**: 贝叶斯学习 appendix 提供了价格收敛到真实价值的数学基础：熵（entropy）作为信念调整速度的度量。这为"市场效率"提供了过程层面的解释。
    **quant_link**: 价格收敛速度 ~ -I_q(p)（熵率）; 熵率取决于买卖信号概率差异。可用不同市场的价格调整速度比较验证。

14. **excerpt_id**: OH_014
    **source_hint**: Chapter 4, p. 92-93 / Kyle model
    **quote**: "In Kyle's model, the informed trader is a monopolist who receives a signal of the true asset value and submits an order to maximize his expected profit. The market maker receives the total order flow and sets prices efficiently... In equilibrium, the informed trader's optimal strategy is to trade an amount proportional to his signal."
    **why_kept**: Kyle 1984/1985是策略交易模型的起点。线性均衡、市场深度参数λ（价格对订单流的敏感度）、知情者利润与噪声交易方差成正比。这是后续所有订单流价格影响模型的基础。
    **quant_link**: 价格变化 Δp = λ·(订单流); λ = 市场深度的倒数。可用高频数据估计λ（如Amihud非流动性指标或更精细的订单流回归）。

15. **excerpt_id**: OH_015
    **source_hint**: Chapter 4, p. 110-112 / Holden-Subrahmanyam
    **quote**: "With multiple informed traders, λ_n is larger in earlier periods than in the information monopolist case, and it falls rapidly in later periods... As the number of informed traders goes to infinity, all information is revealed in the first trading interval, market depth and the expected quantity of informed trade go to infinity."
    **why_kept**: 多知情交易者的竞争效应：信息揭示加速→市场深度λ在初期更大（价格更敏感）、后期迅速下降。极端情况下（知情者→∞），信息在第一期完全揭示。这连接了微观结构模型与理性预期均衡。
    **quant_link**: 信息事件后的初期λ较高→价格冲击大; 后期λ下降→价格稳定。可用盈余公告等事件前后的订单流价格弹性检验。

16. **excerpt_id**: OH_016
    **source_hint**: Chapter 5, p. 133-136 / Admati-Pfleiderer
    **quote**: "The optimal behavior for an uninformed discretionary trader is determined by solving for the minimum cost trading period in which to transact... it is optimal for the discretionary traders to 'clump' together in an attempt to separate their trades from the ill effects of the informed traders."
    **why_kept**: 不知情者的策略性行为：集中交易（clumping）以降低信息交易的影响。这解释了交易量和波动率的日内模式（U型或集中在开盘/收盘）。
    **quant_link**: 日内成交量模式 = f(不知情者的集中交易决策); 日内λ（价格敏感性）的横截面差异。需要订单流时间戳数据。

17. **excerpt_id**: OH_017
    **source_hint**: Chapter 6, p. 169-176 / Diamond-Verrecchia and Easley-O'Hara on time
    **quote**: "Easley and O'Hara demonstrate that if there is no trade at time t, then the market maker raises the probability he attaches to no information event and lowers the probabilities he attaches to a low signal or a high signal having occurred... the spread narrows following the absence of trade."
    **why_kept**: 无交易（no-trade）本身具有信息内容：在信息存在不确定性下，无交易暗示可能没有信息事件→做市商降低逆向选择风险→收窄价差。这颠覆了"无交易=无信息"的传统假设。
    **quant_link**: 交易间隔时间（inter-trade duration）与价差调整的关系; 无交易区间后的首笔交易价格行为。需要时间戳级别的交易数据。

18. **excerpt_id**: OH_018
    **source_hint**: Chapter 6, p. 176-177 / volume and speed of adjustment
    **quote**: "Volume effects arise in this model because the greater the volume, the less frequent no-trade outcomes are, and thus the more likely it is that new information exists... markets with higher 'normal' trading volume will adjust to information more slowly."
    **why_kept**: 成交量的双重效应：高成交量市场→无交易频率低→信息存在概率高→价格调整更快？不，O'Hara说高成交量市场"调整更慢"（因为无交易的信息信号被稀释）。这是一个反直觉的预测。
    **quant_link**: 成交量水平与价格调整速度的关系; 横截面：高成交量股票的信息吸收速度。需要事件研究与高频数据结合。

19. **excerpt_id**: OH_019
    **source_hint**: Chapter 7, p. 181-187 / Glosten monopolist
    **quote**: "Glosten argues that under some circumstances social welfare may actually be greater when there is a monopolistic, rather than a competitive, specialist... a monopolistic specialist could instead choose a schedule of prices that results in an expected loss on some trades but an expected gain on others."
    **why_kept**: 垄断做市商可能改善社会福利：竞争性做市商每笔交易设零利润价格→大交易（信息风险高）无法定价→市场关闭；垄断者可以跨交易规模补贴（小交易补贴大交易）→维持市场开放。这是市场设计的核心洞见。
    **quant_link**: 垄断vs竞争市场的价差结构差异; 不同规模交易的价格歧视。需要比较不同市场结构（如NYSE specialist vs. Nasdaq dealer）的价差数据。

20. **excerpt_id**: OH_020
    **source_hint**: Chapter 7, p. 193-197 / Rock limit order model
    **quote**: "Rock suggests that one factor alleviating this problem is the inventory exposure of the market maker... Since this allows limit order traders better control of their inventory, for inventory positions close to their desired level, even risk averse traders would be approximately risk neutral."
    **why_kept**: Rock的限价订单簿模型：限价订单面临逆向选择（被"pick off"）→最优策略是不提交限价订单→如果没有做市商的库存风险暴露，限价订单簿不存在。解释了"价差就是簿上的洞"（hole in the book）。
    **quant_link**: 限价订单簿深度与价差的负相关; 订单簿的逆向选择成本度量。需要完整订单簿数据（如LOBS数据）。

21. **excerpt_id**: OH_021
    **source_hint**: Chapter 8, p. 217-222 / Grossman-Miller liquidity
    **quote**: "Grossman and Miller focus on the role of liquidity as the price of immediacy... traders wishing to trade now pay a cost relative to simply waiting to trade next period... The greater the number of speculators willing to provide immediacy, the greater the liquidity of the market."
    **why_kept**: Grossman-Miller将流动性定义为"即时性价格"：投机者承担库存失衡→获得跨期价格变化作为补偿→投机者数量M决定市场流动性。这是流动性的跨期供给理论。
    **quant_link**: 市场深度（如Amihud ILLIQ）与做市商/投机者数量的关系; 波动率与流动性供给成本。可用市场参与者的库存变化数据。

22. **excerpt_id**: OH_022
    **source_hint**: Chapter 8, p. 227-232 / Chowdhry-Nanda multimarket
    **quote**: "Chowdhry and Nanda demonstrate that if traders can observe all trading prices, then the informativeness of prices is given by Ψ = N / [(N+1) + (σ_d^2/σ_u^2)(N-1)]... As the number of markets increases, informativeness also increases."
    **why_kept**: 多市场均衡：知情者在多个市场交易→订单流相关性→信息揭示增加。但小不知情交易者固定在单一市场→他们的存在使信息揭示不完全。这解释了市场分割与信息效率的关系。
    **quant_link**: 多市场交易量分配与价格发现效率; 跨市场价格差异与信息传播速度。需要多市场交易数据（如A股/港股/ADR）。

23. **excerpt_id**: OH_023
    **source_hint**: Chapter 8, p. 234-242 / Seppi block trading
    **quote**: "Seppi demonstrates that there is an equilibrium in which the large trader uses blocks when rebalancing his portfolio and uses the specialist when he is trading on information... the 'no-bagging' constraint is costless for a liquidity trader but is not for an informed trader."
    **why_kept**: Seppi的分离均衡：大宗交易者（非匿名）通过"不打街"（no-bagging-the-street）约束区分流动性交易和信息交易。流动性交易者用大宗交易（无价格效应），信息交易者用专家市场（有价格效应）。
    **quant_link**: 大宗交易价格效应 = 信息交易的信号; 大宗交易后价格恢复 vs 持续漂移。可用大宗交易数据库（如NYSE TAQ中的block trades）检验。

24. **excerpt_id**: OH_024
    **source_hint**: Chapter 9, p. 252-260 / Madhavan transparency
    **quote**: "Madhavan argues that a market maker who reveals his trading prices to the market can set better prices than a market maker who does not. This occurs because informed traders prefer not to trade in such a market since it reduces their informational advantage."
    **why_kept**: 透明度悖论：更多价格信息→知情者信息优势减少→知情者退出→逆向选择降低→价格更好。因此透明度可能改善市场质量，而非仅仅增加竞争。
    **quant_link**: 市场透明度（如报价披露延迟、订单簿披露深度）与价差、市场深度的关系。需要比较不同透明度制度的市场数据。

25. **excerpt_id**: OH_025
    **source_hint**: Chapter 7, p. 205-209 / Gennotte-Leland crash model
    **quote**: "Gennotte and Leland argue that the less observable π(p_0) is, the greater is the volatility of prices... the greatest price volatility arises when traders are ignorant of hedging demands, and this same ignorance can induce jumps in the price process even at relatively small levels of hedging."
    **why_kept**: 1987年崩盘的机制解释：价格保险/对冲需求（如投资组合保险）不可观测→市场参与者误将其解读为信息信号→价格跳跃（crash）。这是"非信息订单流被误解为信息"导致的稳定性危机。
    **quant_link**: 对冲需求（如期权市场gamma、期货基差）的可观测性与现货市场波动率; 价格跳跃频率与订单流类型不确定性。需要衍生品与现货市场联合数据。

## CORE_CONCEPTS

1. **concept_name**: asymmetric information / adverse selection
   **definition_from_text**: "The market maker, who is in the middle of all trades, knows that some traders may have better information than he does. These informed traders buy when they know the stock's current price is too low, they sell when they know it is too high... the market maker knows that when he is trading with an informed trader, he always loses." (Ch.3, p.53)
   **behavioral_mechanism**: 知情者选择交易方向（买/卖）和规模以最大化信息租金；做市商通过贝叶斯更新从订单流中学习，调整价格以补偿逆向选择风险；不知情者因预期损失而减少交易或集中交易以规避信息交易。
   **data_objects_involved**: 交易方向、交易规模、订单簿深度、交易后价格漂移、买卖价差、交易频率、价格序列的鞅性质。
   **quant_boundary**: 知情者比例不可直接观测；需用PIN/VPIN等代理。模型假设知情者是同质的、信息是短命的——与实盘中长期信息、异质信念差距大。

2. **concept_name**: bid-ask spread decomposition
   **definition_from_text**: Stoll: "These costs arise from three sources. First, there are holding costs... Second, there may be order-processing costs... Third, a cost may arise from trading with individuals who know more about the stock than the dealer." (Ch.2, p.25)
   **behavioral_mechanism**: 库存成本→做市商因偏离最优组合而要求补偿；订单处理成本→交易机制的运营费用；逆向选择成本→与知情者交易的预期损失。在竞争中，价差 = 这三种成本之和。
   **data_objects_involved**: 有效价差（effective spread）、实现价差（realized spread）、价格冲击（price impact）、库存变化、交易规模、日内价差模式。
   **quant_boundary**: Stoll的单期模型假设固定"真实价格"和一次清算；Ho-Stoll的多期模型假设有限时间horizon。两者都不允许真实价值随时间变化，这限制了实证适用性。

3. **concept_name**: market depth / Kyle's lambda (λ)
   **definition_from_text**: "In Kyle's model, the market maker sets the price equal to the unconditional expected value plus λ times the order flow... λ is a measure of the market's depth or, more precisely, the reciprocal of market depth." (Ch.4, p.95-96)
   **behavioral_mechanism**: 知情者选择订单规模以平衡信息租金与价格影响；噪声交易提供 camouflage；做市商根据总订单流设定线性价格。λ决定了订单流对价格的影响程度。
   **data_objects_involved**: 订单流、净交易量、价格变化、市场深度（订单簿深度）、知情交易概率、噪声交易方差。
   **quant_boundary**: Kyle模型假设单期、单知情者、线性均衡。多知情者或风险厌恶知情者会改变λ的性质（Subrahmanyam）。线性定价规则在实盘中只是近似。

4. **concept_name**: information revelation through trading / Bayesian learning
   **definition_from_text**: "Glosten and Milgrom demonstrate that over time the preponderance of informed trades on one side of the market results in the market maker eventually learning the informed traders' information, and his prices converge to the expected value of the asset given this information." (Ch.3, p.61)
   **behavioral_mechanism**: 每笔交易传递信号（买=可能好信息，卖=可能坏信息）；做市商用贝叶斯规则更新后验信念；价格序列成为鞅，收敛到真实价值（强有效）。
   **data_objects_involved**: 交易序列、价格序列、买卖方向、交易间隔时间、价格调整速度、熵率（entropy rate）。
   **quant_boundary**: 收敛速度是渐近的（指数收敛），但"多快"取决于熵率——难以在有限样本中精确估计。模型假设交易是i.i.d.的，与实盘中聚集交易、自相关订单流不符。

5. **concept_name**: liquidity provision / immediacy
   **definition_from_text**: "Grossman and Miller focus on the role of liquidity as the price of immediacy... traders wishing to trade now pay a cost relative to simply waiting to trade next period." (Ch.8, p.217)
   **behavioral_mechanism**: 投机者（或做市商）愿意偏离最优组合持有库存→获得跨期价格补偿→库存风险越大→补偿越高→流动性成本越高。投机者数量内生决定市场流动性。
   **data_objects_involved**: 订单簿深度、买卖价差、价格冲击、交易量、持仓量、库存变化、投机者数量、跨期收益率。
   **quant_boundary**: 模型假设无信息摩擦（纯流动性冲击），因此无法解释信息事件期间的流动性枯竭。库存冲击的负序列相关假设（t期的冲击在t+1期被完全抵消）过于简化。

6. **concept_name**: noise trading / liquidity trading
   **definition_from_text**: "The uninformed traders face an interesting problem because, if the informed are profiting on their information, it must be at the uninformeds' expense... the uninformed must trade for reasons other than speculation. A useful construct to achieve this is that of the liquidity trader who trades for reasons exogenous to the model." (Ch.3, p.59)
   **behavioral_mechanism**: 噪声/流动性交易者出于外生原因（如流动性冲击、再平衡需求、套期保值）交易→他们的交易为知情者提供 camouflage→使信息租金可持续。如果没有噪声交易，价格会立即揭示信息，知情者无法盈利。
   **data_objects_involved**: 交易量、订单流方差、价格冲击、交易频率、不知情交易的代理（如散户交易比例、小订单比例）。
   **quant_boundary**: 噪声交易是外生的、无法解释的——这是模型最大的弱点。所有策略模型都假设噪声交易是维持均衡的"黑箱"。后续研究（如Spiegel-Subrahmanyam）尝试将其内生化。

7. **concept_name**: market transparency / information in the order book
   **definition_from_text**: "In Rock's model, traders know not only the complete structure of the book, but the market maker's inventory position as well... To the extent the market maker has private information... he can exert market power on pricing." (Ch.7, p.197)
   **behavioral_mechanism**: 订单簿透明度影响限价订单的逆向选择风险（"被捡便宜"风险）→透明度越低→限价订单越少→价差越大；透明度影响做市商的信息租金和库存管理能力。
   **data_objects_involved**: 订单簿深度、价差、订单簿失衡（order book imbalance）、限价订单取消率、市场深度、价格发现效率。
   **quant_boundary**: 理论对比极端透明/不透明，但实盘中透明度是连续的（部分披露、延迟披露等）。订单簿信息的战略性使用很难用简单模型刻画。

8. **concept_name**: trade size and price impact
   **definition_from_text**: "Informed traders are assumed to be risk neutral and trade to maximize their expected profits... the larger the trade size, the larger is their gain all other things remaining equal. Consequently, trade size induces an adverse selection problem." (Ch.3, p.67)
   **behavioral_mechanism**: 知情者偏好大交易（信息租金规模效应）→规模成为信息信号→做市商对大交易设更宽价差→分离均衡（大交易全是信息交易）或混同均衡（大小交易都含信息）。
   **data_objects_involved**: 交易规模、规模-价格冲击弹性、价差与规模的关系、大宗交易价格、交易后恢复模式。
   **quant_boundary**: 模型假设只有两种规模（大/小），且交易规模是外生的。实盘中规模是连续的、交易者可以拆单（order splitting）——这完全改变了模型的预测。

## QUANTIZATION_TABLE

| concept | raw_rule_from_text | observable_proxy | data_needed | quant_status | implementation_hint | notes |
|---------|-------------------|------------------|-------------|--------------|---------------------|-------|
| bid-ask spread | spread = inventory cost + order processing cost + adverse selection cost (Stoll) | effective spread, quoted spread, realized spread | tick-level TAQ data: quotes, trades, direction | proxy_quantizable_now | 用Glosten-Harris分解：有效价差 = 实现价差 + 价格冲击。实现价差 ≈ 订单处理+库存，价格冲击 ≈ 逆向选择 | 需要trade signing（Lee-Ready算法）区分买卖方向 |
| adverse selection component | informed trading probability × information payoff; spread compensates for expected loss to informed traders | post-trade price drift (15-30 min), permanent price impact | tick TAQ data, event-time alignment | proxy_quantizable_now | 用交易后价格漂移度量逆向选择成本：漂移越大→逆向选择越强 | Roll 1984在存在信息时不适用；需用Glosten-Harris修正 |
| inventory component | spread placement (not size) changes with inventory position; bid/ask both shift with inventory (Stoll, Ho-Stoll) | inventory-adjusted quote changes, inventory position of market maker | dealer inventory data (specialist/regulatory data) or inferred from net order flow | needs_extra_data | 需要逐笔库存数据。NYSE specialist库存数据已不公开，但可用net order flow推断 | 实证中库存效应在短期（分钟级）存在争议，Madhavan-Smidt和Hasbrouck-Sofianos发现证据 |
| order processing cost | fixed cost per trade → decreasing in trade size; U-shaped total cost (Stoll) | fixed component of spread, per-trade fee | brokerage data, exchange fee schedules | proxy_quantizable_now | 交易所费用是公开的固定成本；但不同券商/市场差异大。可用小规模交易的最小价差下限估计 | 在电子市场，订单处理成本趋近于零 |
| Kyle's lambda (λ) | price impact of order flow: Δp = λ·(order flow); λ = market depth^{-1} | Amihud ILLIQ, price impact per unit volume, Kyle's lambda regression | daily or intraday price/volume data | proxy_quantizable_now | 回归：Δp = α + λ·order_flow + ε。日内可用5-15分钟频率估计。Amihud是 coarse proxy | 实盘中λ随时间、事件、股票特征变化剧烈；非线性价格影响更常见 |
| information event probability (α) | probability that new information exists; absence of trade signals no event (Easley-O'Hara) | VPIN, PIN (Probability of Informed Trading), inter-trade duration | tick trade data, volume imbalance, buy/sell classification | proxy_quantizable_now | VPIN = volume-synchronized PIN; 用买卖不平衡和交易量估计信息事件概率。需MLE估计 | Easley-Hvidkjaer-O'Hara 2002 PIN模型需要 buyer-initiated / seller-initiated trade classification |
| price recovery after block trade | if information-event uncertainty exists, small trade after block causes price to partially recover toward prior | block trade price impact, post-block recovery trajectory | block trade records (≥10,000 shares), tick TAQ, time alignment | needs_extra_data | 需要识别block trades和随后的交易序列。NYSE TAQ有block trade标识 | 恢复模式取决于"分离均衡"vs"混同均衡"的假设；需事前判断 |
| entropy rate of convergence | beliefs converge exponentially at rate -I_q(p); I_q(p) is relative entropy | speed of price adjustment to events, half-life of price impact | event-time data, cumulative abnormal return trajectory | shell_only | 熵率是理论概念，无直接观测映射。可用事件研究中的价格调整半衰期作为远代理 | 需要大样本事件才能估计调整速度；不同事件类型差异大 |
| Martingale property of prices | transaction prices form a martingale w.r.t. market maker information; E[p_{t+1} given I_t] = p_t | price change autocorrelation, variance ratio test | tick transaction prices | proxy_quantizable_now | 检验tick价格变化的序列相关：鞅意味着零自相关（一阶差分）。但Glosten-Milgrom预测与Roll 1984的负自相关不同 | 在tick级别，由于bid-ask bounce，价格变化通常负自相关。需要区分"bounce"和"信息效应" |
| no-trade as information signal | absence of trade raises probability of no information event; spread narrows after no-trade | inter-trade duration, spread change after no-trade intervals | time-stamped quote data (millisecond or second level) | needs_extra_data | 需要精确的时间戳数据来识别无交易区间和随后的价差变化。传统TAQ秒级数据可能不够精确 | 该预测与Diamond-Verrecchia的"无交易=坏信息"相反，取决于模型假设（卖空约束vs信息事件不确定性） |
| market collapse threshold | if too many informed traders, spread → ∞, market shuts down | spread explosion during crises, volume collapse, trading halts | extreme market condition data (e.g., 1987 crash, 2008 flash crash) | shell_only | 理论阈值是参数化的（知情者比例），但实盘中无法直接观测该比例。交易暂停是多重因素结果 | 理论预测"无交易可清价格"，但实盘中市场通常以 circuit breakers 或交易暂停应对 |
| monopolist vs competitive spread | monopolist can cross-subsidize trades across sizes; competitive dealer cannot → market may fail | spread structure by trade size in different market structures (NYSE vs NASDAQ) | market structure comparison, trade size-stratified spread data | needs_extra_data | 需要比较不同市场结构（垄断做市商 vs 竞争性做市商）的价差-规模关系。历史数据有变化（如NYSE specialist system已改变） | 随着电子交易和maker-taker费用，传统垄断/竞争二分法已不适用 |
| clumping of liquidity trades | discretionary traders concentrate in periods with higher uninformed volume to minimize λ | intraday volume patterns, U-shaped volume curve, variance of returns by time-of-day | intraday volume and return data, tick-level TAQ | proxy_quantizable_now | 检验日内成交量和λ（价格敏感性）的日内模式。Admati-Pfleiderer预测集中交易时段λ更低 | 日内模式也可用开盘/收盘的信息事件（如隔夜信息）解释，不完全等同于clumping行为 |
| limit order adverse selection (Rock) | limit order traders face adverse selection because market maker can condition on size, they cannot → book is a "hole" | bid-ask spread as "hole in the book", limit order execution probability and post-execution price drift | full limit order book data (LOB), order-level data with execution and cancellation | needs_extra_data | 需要完整订单簿数据（如NASDAQ ITCH, CME Market Depth）才能识别"被捡便宜"的限价订单 | 现代电子市场允许冰山订单和动态重设，部分缓解了Rock的问题 |
| sunshine trading benefit | preannouncement of liquidity trades reduces variance, improves liquidity trader welfare | impact of pre-trade transparency (iceberg orders, indicative interest) on spread and depth | market with varying transparency rules, or event studies of disclosure changes | shell_only | "sunshine trading"在现实中很少见；现代对应物是 iceberg orders 或暗池（dark pools）的预披露 | 现代市场的趋势是减少透明度（暗池兴起），与理论预测的益处相反，说明其他因素（如信息隐藏）更重要 |
| portfolio insurance / hedging-induced crash | unobservable hedging demands misinterpreted as information → price jumps | gamma of options market, futures basis, spot market volatility, order flow classification | joint spot-derivatives data, option order flow, portfolio rebalancing data | needs_extra_data | 需要识别"非信息对冲需求"的订单流。可用期权市场gamma和delta对冲流作为代理 | 1987年崩盘后 portfolio insurance 减少；现代对应物是风险平价基金的再平衡或ETF套利流 |
| call market vs continuous market stability | call market batches orders → averages out information effects → may avoid market failure | call auction opening price vs continuous trading prices, opening volatility vs intraday volatility | market with both call and continuous phases (e.g., Tokyo, Euronext, some Chinese markets) | proxy_quantizable_now | 比较集合竞价阶段与连续交易阶段的价差、价格发现效率、波动率。集合竞价通常有更小的逆向选择问题 | 集合竞价的信息效率可能较低（Madhavan），存在权衡：稳定性 vs 速度 |
| multimarket information revelation | informed trades across N markets → prices more informative; but small traders fixed → prevents full revelation | price discovery contribution by market, cross-market price correlation, information share (Hasbrouck) | multi-market trade data for same security (e.g., A-share/H-share, primary listing/dark pool) | needs_extra_data | 需要多市场交易数据。Hasbrouck信息份额方法可分解各市场的价格发现贡献 | 多市场竞争导致"奶油层剥离"（cream-skimming）问题，暗池吸引不知情流，留下信息流在交易所 |
| block trade no-bagging equilibrium | block traders use non-anonymity + "no-bagging" constraint to separate liquidity from informed trades | block trade price impact relative to round-lot sequence, post-block price path | block trade data with identification of liquidity vs informed motive (hard) | needs_extra_data | 需要识别大宗交易者的身份和动机（通常非公开）。可用后续交易行为（是否继续交易）推断 |  upstairs market 的"非匿名性"是核心，但在现代暗池和ATS中，匿名性是常态，Seppi的分离机制可能失效 |

## FORMULAS_AND_ALGOS

### 1. Stoll 价差分解（百分比成本）

公式：C_i(Q_i) = (z / W_0) * [σ_i * Q_p * ρ_i * σ_i * Q_i + 0.5 * σ_i^2 * Q_i^2]

(P* - P_b) / P* = c_i(Q_i^s)  [ask类似]
(P_a - P_b) / P* = c_i(Q_i^s) - c_i(Q_i^b) = (z / W_0) * σ_i^2 * |Q_i|
- **代理标注**: 这是单期、风险厌恶的闭式解。实盘中：
  - 库存成本可用交易后实现价差（realized spread）代理，但需控制库存风险暴露（需要做市商持仓数据）。
  - 交易规模|Q_i|的线性关系假设只在单笔交易中成立；实盘拆单会改变此关系。
  - 风险厌恶系数z和财富W_0不可观测。

### 2. Glosten-Milgrom 贝叶斯定价

公式：a_1 = E[V | B_1] = V̄ * Pr{V=V̄ | B_1} + V * Pr{V=V | B_1}
b_1 = E[V | S_1] = V̄ * Pr{V=V̄ | S_1} + V * Pr{V=V | S_1}

Pr{V=V̄ | S_1} = [Pr{V=V̄} * Pr{S_1 | V=V̄}] / [Pr{V=V̄} * Pr{S_1 | V=V̄} + Pr{V=V} * Pr{S_1 | V=V}]
- **proxy/approximation**: 模型假设二值信息（高/低），实盘是连续信息空间。贝叶斯更新只在结构化的离散模型中可精确计算。实盘中的"近似"：用价格对买卖方向的响应系数作为"学习速度"的代理，但这不是贝叶斯更新本身。

### 3. Kyle 线性均衡（单期）

公式：Δx = β(v - p_{n-1})  [informed trader's optimal order]
Δp_n = λ(Δx_n + Δu_n)  [market maker's pricing rule]

β = 1 / (2λ) = σ_u / σ_v  [equilibrium]
λ = σ_v / (2σ_u)  [market depth parameter]

E[π | v] = (v - p_0)^2 / (4λ) = (v - p_0)^2 * σ_u / (2σ_v)
- **proxy/approximation**: 线性均衡假设是简化的。实盘中的λ估计：
  - 可用日内订单流回归：Δp = α + λ·signed_volume + ε
  - 但λ随时间变化（如Holden-Subrahmanyam预测日内λ递减），单期估计只是平均λ。
  - σ_u（噪声交易方差）和σ_v（信息方差）不可直接观测，需用收益方差和订单流方差代理。

### 4. Easley-O'Hara 分离均衡价格（大交易）

公式：V̄_{S_2} = [V̄ * x_1(1-αμ) + V̄ * αμ] / [x_1(1-αμ) + αμ(1-δ)]

S_2 / S_1 ≥ 1 + αμδ / [x_1(1-αμ)]  [separating condition for sells]
- **proxy/approximation**: 分离/混同均衡取决于相对规模阈值。实盘中：
  - 交易规模是连续的，非离散的S_1/S_2。
  - 条件涉及α（信息事件概率）、μ（知情者比例）、δ（信息方向概率）、x_1（不知情大交易比例）——全部不可观测。
  - 只能检验横截面预测：价差-规模关系是否为分段线性（大交易有更宽的价差）。

### 5. Holden-Subrahmanyam 多知情者极限

公式：lim_{N→∞} Σ_{n'} = 0, lim_{N→∞} λ_{n'} = 0  [for last auction before any τ]
lim_{M→∞} Σ_1 = 0, lim_{M→∞} E_0[Δx_1 | v] = ∞, lim_{M→∞} λ_1 = 0, lim_{M→∞} p_1 = v
- **proxy/approximation**: 这是渐近结果，描述"很多交易"和"很多知情者"的极限。实盘中：
  - 不可直接检验，但可检验定性预测：信息事件后初期的λ（价格敏感性）更高。
  - 盈余公告等事件中，预期公告后的初期订单流价格弹性更大。

### 6. Grossman-Miller 流动性价格（两期）

公式：i = (M / (1 + M)) * (r - 1)  [speculator inventory in period 1]
r = p_2 / p_1  [return to speculator]
r = (σ_ε^2 / (1 + M)) * (variance-related term)  [approximate]
- **proxy/approximation**: 投机者数量M内生，但进入成本c外生。实盘中：
  - 无法直接数"投机者"，可用做市商数量或高频交易者数量代理。
  - 价格跨期变化r取决于流动性冲击的序列相关性，但模型假设完美负相关（ unrealistic）。
  - Amihud ILLIQ 是该理论的粗粒度代理：|return| / volume 作为即时性价格。

## NOT_QUANT_YET

1. **信息事件概率（α）的实时估计**：虽然PIN/VPIN模型提供了知情交易概率的估计，但"信息事件是否发生"是一个二值不可观测变量。现有模型用MLE从交易序列推断，但假设了固定的交易到达率，与实盘中聚集交易（trade clustering）和信息驱动的到达率变化不符。需要允许信息事件内生的交易到达率模型。

2. **做市商库存的实时观测**：Stoll、Ho-Stoll、Amihud-Mendelson的库存-价格联动理论依赖于库存数据。但在现代分散的电子市场中，单个做市商的库存几乎不可观测（除非是特定监管数据）。"库存"从集中式 specialist book 变为分散的多个高频交易商的库存。需要新的聚合库存代理变量。

3. **限价订单簿的逆向选择成本量化**：Rock模型指出限价订单面临"被捡便宜"（picked off）风险，但实盘中冰山订单、动态重设、订单簿分层使得这种逆向选择难以用简单模型刻画。需要允许订单簿动态策略的复杂模型，目前还没有广泛接受的实证度量。

4. **非信息性订单流与信息性订单流的实时区分**：Gennotte-Leland的崩盘模型强调对冲需求（非信息）被误读为信息信号。但实盘中实时区分"对冲/再平衡流"和"信息驱动流"几乎不可能，除非有订单级别的动机数据（通常不可获得）。

5. **市场崩溃阈值的结构性估计**：Glosten-Milgrom预测"太多知情者→市场关闭"，但实证中市场关闭（交易暂停）是多重因素（流动性枯竭、技术故障、监管干预）的结果。没有一个清晰的统计阈值来识别"信息驱动的市场关闭"。

6. **跨市场信息份额的动态分解**：Chowdhry-Nanda模型预测多市场中的信息揭示，但Hasbrouck的信息份额方法假设价格服从向量误差修正模型（VECM），这是线性近似。在高频非线性动态、跳跃、市场摩擦下，信息份额的估计可能不稳定。

7. **透明度对信息优势的内生影响**：Madhavan的理论预测透明度可能改善市场质量，但实盘中暗池（dark pools）和冰山订单的兴起似乎表明市场参与者偏好减少透明度。需要同时考虑信息隐藏需求和流动性需求的权衡模型。

8. **大宗交易的分离均衡检验**：Seppi的"no-bagging"均衡要求区分大宗交易者的流动性动机和信息动机，但现代市场中大宗交易通常通过暗池或内部化（internalization）处理，"非匿名性"和"不打街约束"难以观测。

9. **时间作为信息信号的利用**：Diamond-Verrecchia和Easley-O'Hara的"无交易=信息"理论需要毫秒级的时间戳和精确的无交易区间识别。但现代连续电子市场中，无交易区间很短（<1秒），订单簿变化本身可能包含信息，传统"交易/无交易"二元划分过于简化。

10. **策略性交易者的动态博弈均衡**：Kyle、Admati-Pfleiderer、Foster-Viswanathan的模型要求线性均衡或特定策略集，但实盘中策略可能是非线性的、混合的、学习的。目前还没有从高频数据中识别"策略集"的统计方法。

11. **日内价差模式的时间horizon解释**：Ho-Stoll预测价差随时间horizon递减，但实证中的U型日内价差也可用开盘/收盘的信息集中效应解释。两者在统计上难以区分，需要外生的时间horizon变化（如交易时间延长或缩短）作为自然实验。

12. **多期库存模型的实证对应**：Garman的破产模型、Amihud-Mendelson的半马尔可夫库存过程都是多期动态模型，但实证中通常只能观测到离散时间间隔的库存快照。需要连续时间模型与离散观测数据的匹配方法。

## NEXT_ACTION

1. **提取Glosten-Milgrom和Easley-O'Hara的核心公式作为独立数学卡片**：将贝叶斯更新规则、分离均衡条件、信息事件不确定性模型写成独立的数学参考卡片，方便后续VPIN/PIN类指标的实现时查阅。

2. **构建Kyle模型与订单流回归的桥梁文档**：将Kyle的λ、深度、知情者策略映射到实证的Amihud ILLIQ、订单流回归、价格冲击模型。需要明确：哪些Kyle预测可以检验，哪些因模型简化而失效。

3. **整理Stoll价差分解的实证实现路径**：收集Glosten-Harris 1988、Huang-Stoll 1997等后续实证论文的方法，形成"如何从TAQ数据计算有效价差、实现价差、永久/暂时价格冲击"的操作指南。

4. **标注"不可量化"理论对象的后验检查清单**：对于entropy rate、market collapse threshold、no-bagging equilibrium等shell_only概念，在F2中保留一个"理论提示列表"，当有新的数据可用（如监管数据、订单簿数据）时重新评估可量化性。

5. **连接Hasbrouck的价格发现文献与本书的信息模型**：Hasbrouck的"信息份额"（Information Share）和"成分份额"（Component Share）方法是对Chowdhry-Nanda多市场信息揭示的实证对应。需要补充这部分文献作为F2的后续阅读。

6. **收集现代市场结构变迁对本书理论的挑战**：由于本书写于1995年（电子交易、高频交易、暗池兴起之前），需要补充：
   - 高频做市商的库存管理（与Stoll/Ho-Stoll的不同）
   - 暗池中的非匿名性（与Seppi block trading的对应）
   - 订单簿高频动态（与Rock limit order model的扩展）
   - 现代透明度的多层次结构（与Madhavan/Pagano-Roell的对比）

7. **建立"信息事件"的实证识别方法**：从Easley-O'Hara的信息事件不确定性出发，整理：
   - 盈余公告、宏观经济数据发布、公司新闻等可识别事件的价格-成交量模式
   - 不可识别事件（如渐进信息流入）的统计检测方法（如anomaly detection、regime switching）
   - 将PIN/VPIN估计与这些事件对齐，检验信息事件概率的准确性

8. **编制"市场微观结构理论→可量化假设→数据需求"映射表**：对于本书中的每一个核心模型（Garman、Stoll、Glosten-Milgrom、Kyle、Easley-O'Hara、Grossman-Miller、Admati-Pfleiderer、Chowdhry-Nanda等），明确：
   - 理论预测的可检验假设
   - 所需的最低数据粒度
   - 现有公开数据（如CRSP、TAQ、LOBSTER）是否足够
   - 如果不能，需要购买或申请什么数据

9. **连接本书与F2中其他材料的层级关系**：明确本书在F2知识图谱中的位置：
   - 上游：经济学基础（博弈论、信息经济学、贝叶斯学习）
   - 同层：其他微观结构教材（如Trading and Exchanges、Market Liquidity）
   - 下游：实证方法（Hasbrouck empirical market microstructure、O'Hara的Market Microstructure in Practice）、交易执行策略（最优执行、VWAP/TWAP、市场冲击模型）
   - 应用层：盘口策略、事件驱动策略、高频交易基础设施

10. **编制"从本书到实盘信号"的警告清单**：对于每一个理论概念，标注：
    - 哪些理论假设在实盘中被系统性违反（如知情者同质、信息短命、零库存成本）
    - 这些违反如何改变理论预测的方向或大小
    - 哪些理论预测在实证中已被拒绝（如库存不影响价差大小）
    - 哪些预测仍有实证支持（如价差与逆向选择的正相关）

11. **补充后续关键文献（1995-2024）**：本书只到1995年，需要补充：
    - Glosten 1994（电子限价订单簿的开创性模型）
    - Parlour 1998（订单提交策略的动态模型）
    - Foucault 1999（订单簿中的等待成本与价差）
    - Roşu 2009（动态限价订单簿模型）
    - Easley, López de Prado, O'Hara 2012（VPIN）
    - Menkveld 2016（高频交易与做市）
    - 这些文献作为"本书的后续发展"记录在F2中

12. **为F2的"价差分解"和"订单流价格影响"工程模块提供理论注释**：当F2后续开发具体的回测模块或信号生成器时，从本书提取的理论约束应作为前置条件：
    - 任何声称"利用逆向选择"的策略必须明确其信息优势来源（否则等于声称自己是知情者）
    - 任何"做市"策略必须明确其库存风险管理和成本补偿机制
    - 任何"订单流毒性"（toxic flow）检测必须连接到Easley-O'Hara的信息事件框架
    - 任何"大宗交易"策略必须考虑分离/混同均衡条件

