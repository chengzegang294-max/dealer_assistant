CUTPACK__A2__Harris__TradingAndExchanges__v2_r1.md

---

# BASIC_INFO

| 字段 | 内容 |
|------|------|
| **书名** | Trading and Exchanges: Market Microstructure for Practitioners |
| **作者** | Larry Harris |
| **出版社** | Oxford University Press, 2003 |
| **语言** | English |
| **A2 组定位** | 市场微观结构 / 交易机制 / 流动性与成本基础 |
| **CUTPACK 版本** | v2_r1 |
| **对应原始文件** | Trading and Exchanges (Larry Harris).pdf |
| **处理人** | Kimi |
| **处理日期** | 2025-06-17 |
| **主文本来源** | PDF 文字层提取：`extracted_TradingAndExchanges.txt`（约 1.6M 字符） |
| **交叉校对** | none（当前无 EPUB 可用） |
| **PDF 角色** | `main_text_source` |
| **关键说明** | 本 CUTPACK 基于 PDF 文字层提取结果构建，而非 EPUB/OCR 整理。原文为英文教科书，核心关注市场微观结构（订单、市场结构、流动性、交易成本、波动性、交易利润）。A股适配时需考虑订单驱动市场与做市商市场的差异，以及T+1/涨跌停等制度差异。 |

---

# MATERIAL_POSITIONING

## 在 A2 组中的角色

- **A2-4**：Trading and Exchanges 是 A2 组“市场微观结构”模块的**底层机制说明书**。它解释的是“市场如何运作”——订单如何传递、价格如何形成、流动性从何而来、交易成本如何构成。
- **与 MP/Dalton 体系的关系**：MP 和 Dalton 的书关注“如何在已知的市场结构中交易”，而 Harris 的书关注“市场结构本身如何设计”。前者是战术层，后者是机制层。理解 Harris 有助于理解为什么 MP 中的某些现象会出现（如大单冲击成本、开盘跳空、流动性枯竭）。
- **与 A股策略的关系**：A股是订单驱动市场（连续竞价+集合竞价），Harris 书中讨论的做市商、 specialists、ECN 等结构在 A股不直接存在。但订单属性（限价、市价、止损）、流动性原理、交易成本分解、信息优势等概念完全适用。

## 适用范围与限制

- **适用**：理解订单类型、流动性度量、交易成本估算、市场结构比较、订单簿分析。
- **不适用**：直接的交易信号系统、纯技术分析、MP 结构识别。本书没有日内形态或趋势判断框架。
- **A股适配**：A股为订单驱动连续竞价+集合竞价，无做市商。书中关于 bid/ask spread 的分析需转化为 A股 的买卖五档/十档价差分析。书中关于 dealers 的分析可映射至 A股 的“提供流动性的大单交易者/机构”概念。

---

# RETAINED_EXCERPTS

以下摘录为从原文提取的**显式规则原文**，按章节归类。

## Excerpt 1：市场微观结构的定义—— Chapter 1

> "Market microstructure is the branch of financial economics that investigates trading and the organization of markets."
>
> —— Chapter 1, Introduction.

> "Trading is a search problem. Buyers must find sellers, and sellers must find buyers. Every trader wants to trade at a good price."
>
> —— Chapter 1, Section 1.4.

**保留原因**：市场微观结构的定义和交易的本质是理解后续所有概念的起点。

---

## Excerpt 2：交易质量五要素—— Chapter 1

> "The primary objectives of this book are to understand the origins of the following characteristics of market quality: Liquidity, Transaction costs, Informative prices, Volatility, Trading profits."
>
> —— Chapter 1, Section 1.2.

> "Liquidity: Traders and regulators often talk about liquidity, but they are rarely careful about what they mean."
>
> —— Chapter 1, Section 1.2.

> "Transaction costs: Traders must effectively manage their transaction costs to trade successfully."
>
> —— Chapter 1, Section 1.2.

> "Volatility: Traders care about volatility because it can have a significant impact on their wealth."
>
> —— Chapter 1, Section 1.2.

> "Trading profits: Trading is a zero-sum game in which some traders win and others lose."
>
> —— Chapter 1, Section 1.2.

**保留原因**：五要素框架是全书的核心结构，也是任何交易策略设计时必须考虑的底层变量。

---

## Excerpt 3：订单类型—— Chapter 4

> "A limit order instructs the broker to buy at the best price possible, but in no event to pay more than a limit price that Jennifer specifies."
>
> —— Chapter 4, Orders and Order Properties.

> "A market order instructs the broker to fill the order quickly, at the best price available."
>
> —— Chapter 4, Orders and Order Properties.

**保留原因**：订单类型是交易者与市场交互的基本语言。限价单 vs 市价单的选择直接决定了交易成本和执行概率。

---

## Excerpt 4：交易商与经纪商—— Chapter 1/3

> "Dealers and brokers help people trade. Dealers trade with their clients when their clients want to trade. The prices at which a dealer will buy and sell are the dealer's bid and ask prices."
>
> —— Chapter 1, Section 1.4.

> "Brokers are agents who arrange trades for their clients. They help their clients find traders who are willing to trade with them. They profit by charging commissions."
>
> —— Chapter 1, Section 1.4.

**保留原因**：交易商（dealer）与经纪商（broker）的区分是理解市场流动性来源和交易成本结构的基础。

---

## Excerpt 5：价差与信息交易者—— Chapter 1

> "Dealers recover their losses to informed speculators by widening the spread between the bid and ask prices at which they will buy and sell."
>
> —— Chapter 1, Section 1.4.

> "Uninformed traders therefore pay more for their trades when dealers lose a lot to informed traders. In effect, uninformed traders lose to well-informed traders through the intermediation of dealers."
>
> —— Chapter 1, Section 1.4.

**保留原因**：价差的形成机制与信息优势的关系是微观结构的核心洞察。A股中虽无做市商，但大单交易者/机构的“信息优势”同样会反映在买卖价差和冲击成本中。

---

## Excerpt 6：市场结构—— Chapter 1/5

> "Market structure consists of the trading rules, the physical layout, the information presentation systems, and the information communication systems of a market."
>
> —— Chapter 1, Section 1.5.

> "Market structure determines what traders can do and what they can know. It therefore affects trader strategies, the power relationships among different types of traders, and ultimately trader profitability."
>
> —— Chapter 1, Section 1.5.

**保留原因**：市场结构决定了参与者的博弈规则。A股的 T+1、涨跌停、集合竞价等规则都是“市场结构”的一部分。

---

## Excerpt 7：外部性—— Chapter 1

> "The most important externality in market microstructure is the order flow externality. Traders who offer to trade give other traders valuable options to trade for which the offerers are not compensated."
>
> —— Chapter 1, Section 1.5.

**保留原因**：订单流外部性是理解流动性聚集效应（为什么交易者集中在某些市场/时段）的核心概念。

---

## Excerpt 8：耐心与价格—— Chapter 1

> "Patient traders obtain better prices than impatient traders do because they are willing to search longer and harder to arrange their trades at favorable terms."
>
> —— Chapter 1, Section 1.4.

**保留原因**：耐心与价格的关系是交易成本管理的核心原则。在 A股中，限价单的耐心挂单 vs 市价单的急迫执行，直接体现了这一原则。

---

## Excerpt 9：交易是零和博弈—— Chapter 1

> "Trading is a zero-sum game when gains and losses are measured relative to the market average. On average, well-informed speculators and bluffers win, and poorly informed traders and foolish traders lose."
>
> —— Chapter 1, Section 1.4.

**保留原因**：交易的零和性质是理解“谁赚谁的钱”的基础。信息优势是唯一的可持续利润来源。

---

# CORE_CONCEPTS_AND_RULES

## 概念 1：订单类型与属性

source_basis：Chapter 4, Orders and Order Properties.

核心规则：
1. **市价单（Market Order）**：要求立即以最优价格成交。执行确定性高，但价格不确定性高。适用于需要立即成交的场景。
2. **限价单（Limit Order）**：指定最高买入价或最低卖出价，不保证成交。价格确定性高，但执行不确定性高。适用于对价格敏感、可等待的场景。
3. **止损单（Stop Order）**：当价格达到触发价时转为市价单。用于限制损失或保护利润。
4. **止损限价单（Stop-Limit Order）**：当价格达到触发价时转为限价单。结合了止损和限价的特性。

条件阈值：
- 市价单：成交概率 ≈ 100%，价格冲击成本取决于市场深度。
- 限价单：成交概率取决于限价与当前市场价格的距离。距离越远，成交概率越低，但价格越优。
- 止损单：触发后等同于市价单，价格冲击取决于触发时的市场流动性。

所需数据：订单簿深度（买卖档位）、实时报价、历史成交数据。
caveats：A股中市价单在涨跌停板时可能无法成交（无对手盘）。限价单在涨停板时无法买入，在跌停板时无法卖出。止损单在 A股 中较少直接使用，需通过条件单/算法交易实现。
quant_status：`proxy_quantizable_now` — 订单类型可直接映射到 A股 的委托类型。

---

## 概念 2：市场结构分类

source_basis：Chapter 5, Market Structures.

核心规则：
1. **订单驱动市场（Order-Driven Market）**：交易者直接提交订单到中央订单簿，由撮合引擎按价格优先、时间优先原则匹配。典型例子：A股、NYSE、NASDAQ（部分）。
2. **报价驱动市场（Quote-Driven Market）**：交易者与做市商（Dealer）交易，做市商报出 bid/ask 价格。典型例子：NASDAQ（传统）、外汇市场。
3. **混合市场（Hybrid Market）**：同时包含订单驱动和报价驱动机制。典型例子：NYSE（ Specialists + 订单簿）、现代 NASDAQ。
4. **集合竞价市场（Call Market）**：在特定时间点收集所有订单，然后统一撮合出一个清算价格。典型例子：A股 开盘/收盘集合竞价、交叉盘（Crossing Networks）。

条件阈值：
- 订单驱动市场：透明度最高，价格发现效率取决于订单簿深度。
- 报价驱动市场：流动性由做市商提供，买卖价差是主要交易成本。
- 混合市场：兼具两者优点，但结构更复杂。

所需数据：市场规则说明、交易所撮合机制文档、订单簿数据。
caveats：A股 为纯订单驱动市场（连续竞价+集合竞价），无做市商制度。但科创板/创业板的盘后定价交易、以及大宗交易平台的协议转让，可视为集合竞价/协商交易的变体。新三板有部分做市商制度。
quant_status：`proxy_quantizable_now` — 市场结构为已知规则，可直接分类。

---

## 概念 3：流动性三维度

source_basis：Chapter 19, Liquidity.

核心规则：
1. **紧度（Tightness）**：买卖价差的大小。价差越小，市场越紧。
2. **深度（Depth）**：在不影响价格的前提下可交易的数量。深度越大，大单冲击越小。
3. **弹性（Resiliency）**：价格受冲击后恢复原状的速度。弹性越高，市场越稳定。

条件阈值：
- 紧度：买卖价差 < 0.1% 为紧，0.1%-0.5% 为中等，> 0.5% 为松。
- 深度：订单簿前 5 档累计成交量 / 日均成交量 > 1% 为深，< 0.1% 为浅。
- 弹性：价格偏离后 1 分钟内恢复 50% 为弹性高，5 分钟未恢复为弹性低。

所需数据：Level2 订单簿（买卖档位）、逐笔成交数据。
caveats：A股 标准行情只提供买卖 5 档（部分 Level2 提供 10 档），深度计算受限。弹性需要逐笔数据或高频快照。
quant_status：`proxy_quantizable_now` — 买卖价差可直接计算；深度可用 5 档/10 档近似；弹性需高频数据。

---

## 概念 4：交易成本分解

source_basis：Chapter 21, Liquidity and Transaction Cost Measurement.

核心规则：
交易成本 = 显性成本 + 隐性成本
1. **显性成本**：佣金、税费、交易所费用等。可直接计算。
2. **隐性成本**：
   - 买卖价差（Bid-Ask Spread）：买入价与卖出价之差。
   - 市场冲击成本（Market Impact）：大单交易导致的价格不利移动。
   - 延迟成本（Delay Cost）：从决策到执行期间价格的不利移动。
   - 机会成本（Opportunity Cost）：因未成交或部分成交而错失的价格。

条件阈值：
- 买卖价差：可用当前 best bid/ask 直接计算。
- 市场冲击：可用交易前后价格变化估算。例如，买入后价格上升 > 0.5% 视为高冲击。
- 延迟成本：决策价与实际成交价之差。
- 机会成本：未成交部分按后续价格移动的潜在收益/损失计算。

所需数据：成交明细、订单簿快照、决策时间记录。
caveats：A股 中佣金已很低（万 1-3），显性成本占比小。隐性成本（尤其是冲击成本和延迟成本）是主要交易成本。对于散户，冲击成本通常可忽略；对于机构，冲击成本是核心考量。
quant_status：`proxy_quantizable_now` — 买卖价差直接可算；冲击成本可用前后价格变化近似；延迟成本和机会成本需交易记录。

---

## 概念 5：信息优势与价格发现

source_basis：Chapter 10, Informed Traders and Market Efficiency; Chapter 1, Section 1.4.

核心规则：
1. **信息交易者（Informed Traders）**：拥有关于未来价格的信息优势，通过交易使价格向其信息指示的方向移动。
2. **价格发现（Price Discovery）**：价格通过交易逐步反映基本面信息的过程。信息交易者是推动价格发现的主要力量。
3. **信息不对称（Information Asymmetry）**：信息交易者从不知情交易者（Uninformed Traders）处获利。不知情交易者通过价差和冲击成本间接向信息交易者支付。

条件阈值：
- 信息优势难以直接量化，但可通过以下代理指标近似：
  - 大单流向与后续价格移动的相关性（> 0.3 为显著）。
  - 异常成交量（> 2 倍平均）与后续价格移动的相关性。
  - 订单簿深度的不对称性（买单深度 vs 卖单深度比例 > 1.5 或 < 0.67）。

所需数据：逐笔成交明细（含订单方向）、订单簿深度、Level2 数据。
caveats：A股 中“信息交易者”可能包括内幕信息持有者、拥有研究优势的机构、以及拥有数据处理优势的高频交易者。直接识别信息交易者是不可能的，只能通过统计代理推断。
quant_status：`needs_extra_data` — 需要 Level2/逐笔数据才能有效估计信息优势。

---

## 概念 6：波动性来源

source_basis：Chapter 20, Volatility.

核心规则：
1. **信息驱动的波动（Information-Driven Volatility）**：新信息到达导致价格重新定价。
2. **交易驱动的波动（Trading-Driven Volatility）**：交易行为本身（如大单冲击、止损连锁触发）导致的短期波动。
3. **波动性集聚（Volatility Clustering）**：高波动时段倾向于聚集出现，低波动时段同样聚集。

条件阈值：
- 信息驱动波动：通常在公告/新闻发布时急剧上升，可用事件研究法识别。
- 交易驱动波动：可用成交量-波动关系识别。成交量突增但无信息事件 → 交易驱动。
- 波动集聚：GARCH 模型可捕捉。高波动后倾向于继续高波动。

所需数据：分钟/日 K 线、新闻事件时间、成交量。
caveats：A股 中涨跌停制度会抑制日内波动，但可能导致次日跳空波动（波动性转移）。GARCH 模型在 A股 中适用，但需考虑涨跌停的截断效应。
quant_status：`proxy_quantizable_now` — 波动率可用标准 GARCH/RV 计算，但需调整涨跌停影响。

---

## 概念 7：订单簿分析与订单流不平衡

source_basis：Chapter 6, Order-Driven Markets; Chapter 1, Section 1.5.

核心规则：
1. **订单簿深度（Order Book Depth）**：各价格档位的挂单数量。深度越大，流动性越好。
2. **订单流不平衡（Order Flow Imbalance）**：买单总量与卖单总量之差。正不平衡 → 买盘压力 → 价格上升压力；负不平衡 → 卖盘压力 → 价格下降压力。
3. **订单簿倾斜（Book Skew）**：买单深度与卖单深度的比率。倾斜度 > 1.5 → 买盘占优；< 0.67 → 卖盘占优。

条件阈值：
- 订单流不平衡：可用前 N 档买单总量 - 卖单总量计算。标准化后（除以总量）> 0.2 为显著买盘压力，< -0.2 为显著卖盘压力。
- 订单簿倾斜：前 5 档买单总量 / 前 5 档卖单总量。

所需数据：Level2 订单簿快照（买卖 5/10 档）。
caveats：A股 中 Level2 数据可用但需付费。标准行情只提供 5 档，深度计算受限。订单簿倾斜是短期信号（分钟级），长期有效性有限。
quant_status：`proxy_quantizable_now` — 需 Level2 数据，但 5 档/10 档足够计算基础代理。

---

# QUANTIZATION_TABLE

| # | concept | raw_rule_from_text | observable_proxy | data_needed | timeframe_hint | quant_status | implementation_hint | notes |
|---|---------|-------------------|------------------|-------------|----------------|--------------|---------------------|-------|
| 1 | **订单类型识别** | 市价单立即成交、限价单指定价格、止损单触发后转市价 | 订单委托类型字段 | 交易委托数据 | 即时 | `proxy_quantizable_now` | 直接读取委托类型字段 | A股 无原生止损单，需通过条件单实现 |
| 2 | **买卖价差** | 买入价与卖出价之差 | `(best_ask - best_bid) / mid_price` | Level1 报价 | 实时 | `proxy_quantizable_now` | 直接计算 best bid/ask 价差 | 涨跌停时价差可能为 0 或极大 |
| 3 | **订单簿深度** | 各价格档位的挂单数量 | 前 5/10 档买单总量 vs 卖单总量 | Level2 订单簿 | 实时 | `proxy_quantizable_now` | 累加各档位挂单量 | 5 档深度有限，10 档更准 |
| 4 | **订单流不平衡** | 买单总量与卖单总量之差 | `(bid_volume - ask_volume) / total_volume` | Level2 订单簿 | 分钟级 | `proxy_quantizable_now` | 快照时刻计算前 N 档 imbalance | 短期信号，分钟级有效 |
| 5 | **市场冲击成本** | 大单交易导致的价格不利移动 | `(price_after - price_before) / price_before` 按成交量加权 | 逐笔成交 + 订单簿 | 交易时刻 | `needs_extra_data` | 需知道订单大小和前后价格 | 机构交易核心成本 |
| 6 | **延迟成本** | 决策到执行期间价格的不利移动 | `decision_price - execution_price` | 交易记录 + 行情 | 交易时刻 | `proxy_quantizable_now` | 需记录决策时间和价格 | 算法交易/被动执行的核心考量 |
| 7 | **波动率 (Realized Volatility)** | 价格变动的标准差 | `sqrt(sum(log_returns^2))` | OHLCV | 日/分钟级 | `proxy_quantizable_now` | 标准 RV 计算 | GARCH 可预测，但 A股 涨跌停需调整 |
| 8 | **信息交易者代理** | 信息交易者从不知情交易者处获利 | 大单流向与后续收益的相关性 | 逐笔成交 + Level2 | 日/分钟级 | `needs_extra_data` | 需识别大单方向和后续价格移动 | 统计代理，非直接识别 |
| 9 | **市场结构分类** | 订单驱动、报价驱动、混合、集合竞价 | 交易所规则映射 | 市场规则文档 | 静态 | `proxy_quantizable_now` | 按交易所规则直接分类 | A股 为订单驱动+集合竞价 |
| 10 | **交易驱动波动识别** | 交易行为本身导致的短期波动 | 成交量突增但无信息事件 → 交易驱动 | 成交量 + 新闻事件 | 分钟级 | `proxy_quantizable_now` | 对比成交量异常与新闻时间窗口 | 与信息驱动波动区分 |
| 11 | **订单簿倾斜** | 买单深度与卖单深度的比率 | `bid_depth_5 / ask_depth_5` | Level2 订单簿 | 实时 | `proxy_quantizable_now` | 前 5 档深度比 | 短期方向压力信号 |
| 12 | **零和博弈结构** | 交易是零和博弈，信息优势者获利 | 收益分布分析：赢家/输家比例 | 逐笔成交/账户数据 | 长期 | `needs_extra_data` | 需账户级别的盈亏数据 | 散户整体为负和博弈（因交易成本） |
| 13 | **集合竞价价格发现** | 集合竞价时统一撮合出清算价格 | 集合竞价成交量/开盘价 vs 前日收盘价 | 集合竞价明细 | 日级别（开盘/收盘） | `proxy_quantizable_now` | A股 9:15-9:25 虚拟匹配价序列 | 开盘价决定机制 |
| 14 | **流动性外部性** | 交易者提供流动性给其他交易者 | 订单簿挂单总量 vs 成交量比率 | Level2 订单簿 | 实时 | `proxy_quantizable_now` | 挂单量/成交量比率 | 流动性提供者 vs 消耗者识别 |
| 15 | **交易成本综合度量** | 显性+隐性成本综合 | `execution_cost = (execution_price - benchmark) / benchmark` | 成交明细 + 基准价格 | 交易时刻 | `proxy_quantizable_now` | 基准可用 VWAP/前收盘价/决策价 | 机构交易绩效核心指标 |

---

# NOT_QUANT_YET

| # | concept | why_not_now | what_extra_data_is_needed | whether_it_is_still_valuable |
|---|---------|-------------|---------------------------|------------------------------|
| 1 | **精确的市场冲击模型** | 需要知道每笔订单的大小、时间和前后价格，A股标准数据不包含订单归属 | 逐笔成交明细（含订单号/账户类型） | 是。机构交易的核心成本模型。 |
| 2 | **做市商库存动态** | A股无做市商，但科创板/北交所部分引入。传统 A股数据不包含做市商库存 | 做市商报价序列和库存数据 | 是。对于引入做市商制度的市场。 |
| 3 | **跨市场交易成本比较** | 需要多市场的同步订单簿和成交数据 | 跨市场 Level2 数据 | 是。对于跨市场套利/最优执行策略。 |
| 4 | **订单簿全深度重建** | A股标准只提供 5 档，Level2 提供 10 档。全深度需要交易所内部数据 | 交易所全深度订单簿数据 | 是。对于高频交易策略。 |
| 5 | **精确的信息优势度量** | 需要知道每笔交易的主动/被动方向和交易者类型（机构/散户） | 逐笔成交 + 账户分类数据 | 是。是预测短期价格移动的核心变量。 |
| 6 | **波动率的微观结构分解** | 需要将波动分解为信息成分和交易成分，需要同步新闻事件数据 | 新闻事件时间戳 + 分钟级波动 | 是。对于事件驱动策略。 |
| 7 | **最优执行策略（Algo Trading）** | 需要完整的历史订单簿和成交路径数据来训练/回测 | 历史 Level2 数据 + 完整订单执行记录 | 是。对于机构算法交易。 |
| 8 | **市场操纵检测（Bluffing）** | 需要识别虚假订单/幌骗（spoofing），需要订单生命周期数据 | 订单簿快照 + 订单取消/修改记录 | 是。对于监管和反操纵策略。 |

---

# NEXT_ACTION

## 可直接进入A2字段池的对象（proxy_quantizable_now，本周实施）

1. `bid_ask_spread` (买卖价差) → `(best_ask - best_bid) / mid_price`
2. `order_book_depth_5` (订单簿5档深度) → 前5档买单/卖单累计量
3. `order_flow_imbalance` (订单流不平衡) → `(bid_vol - ask_vol) / total_vol`
4. `realized_volatility` (实现波动率) → 日内/日 log return 标准差
5. `trading_volume_anomaly` (成交量异常) → 当日成交量 vs 20日均量
6. `market_structure_type` (市场结构类型) → 静态规则映射（A股=订单驱动+集合竞价）
7. `call_auction_price` (集合竞价价格) → 9:15-9:25 虚拟匹配价/开盘价
8. `transaction_cost_proxy` (交易成本代理) → 买卖价差 + 佣金率
9. `book_skew` (订单簿倾斜) → `bid_depth_5 / ask_depth_5`
10. `liquidity_proxy` (流动性代理) → 挂单量/成交量比率

## 适合先做代理版本（proxy_quantizable_now，2周内实施）

1. **市场冲击成本估算** → 大单成交前后的价格变化
2. **延迟成本估算** → 决策价 vs 成交价（需交易记录）
3. **集合竞价价格发现效率** → 开盘价 vs 前收盘价的偏离度 + 集合竞价成交量
4. **交易驱动波动识别** → 成交量异常 + 无新闻事件
5. **信息交易者代理** → 大单流向与后续 1-5 分钟收益的相关性
6. **订单簿压力指数** → 综合订单流不平衡 + 订单簿倾斜 + 大单分布

## 先放future bucket（needs_extra_data，1月+）

1. **精确市场冲击模型** → 需逐笔成交明细（含订单归属）
2. **做市商库存动态** → 需做市商制度引入后的数据
3. **跨市场最优执行** → 需多市场 Level2 数据
4. **订单簿全深度重建** → 需交易所内部全深度数据
5. **精确信息优势度量** → 需账户分类 + 逐笔数据
6. **波动率微观结构分解** → 需新闻事件时间戳 + 高频数据
7. **最优执行算法** → 需历史 Level2 + 完整订单执行记录
8. **市场操纵检测** → 需订单生命周期数据（挂撤改）

## 可作为后续策略设计依据的Excerpt

- **Excerpt 1**（交易是搜索问题）→ 流动性需求策略的前提
- **Excerpt 2**（五要素框架）→ 策略设计时必须考虑的底层变量
- **Excerpt 3**（订单类型）→ 执行策略的基础
- **Excerpt 4**（交易商/经纪商）→ 理解流动性来源
- **Excerpt 5**（价差与信息交易者）→ 理解冲击成本和价差扩大机制
- **Excerpt 6**（市场结构）→ A股规则适配的基准
- **Excerpt 7**（外部性）→ 流动性聚集效应的解释
- **Excerpt 8**（耐心与价格）→ 执行策略的定价原则
- **Excerpt 9**（零和博弈）→ 策略竞争优势的本质

---

*End of CUTPACK*
*File: CUTPACK__A2__Harris__TradingAndExchanges__v2_r1.md*
