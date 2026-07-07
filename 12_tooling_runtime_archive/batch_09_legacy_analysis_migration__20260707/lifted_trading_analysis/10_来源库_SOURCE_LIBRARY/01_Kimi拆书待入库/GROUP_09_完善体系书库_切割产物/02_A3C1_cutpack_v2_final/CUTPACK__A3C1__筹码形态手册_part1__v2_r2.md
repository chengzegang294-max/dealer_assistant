# BASIC_INFO
- title: 筹码分布典型形态查询手册：一本书把筹码的底细深挖到底（Part 1：基础理论、调整形态与动态转移）
- language: 中文
- source_type: 书籍（EPUB 文本提取；非 calibre 版主源）
- source_quality: 主源 EPUB 正文完整可提取；calibre 版已验证为空壳，PDF 为纯扫描图版，仅用于版面核对。
- extraction_quality: 正文核心段落可提取，案例中的图注存在乱码，需要结合上下文语义推断。关键定义、形态特征、操作要领保留完整。
- topic_cluster: A3-C1 筹码主组（基础定义、成本分布、调整形态、动态转移）
- notes: |
  本 Part 覆盖原书前言及第1-4章（追根溯源、慧眼识珠、趋势为王）。
  主源为 `筹码分布典型形态查询手册：一本书把筹码的底细深挖到底!.epub`（非 calibre 版，main-xhtml 正文可复现）。
  calibre 版已验证为空，原书大量使用 K 线图案例，案例中的图注乱码不影响核心规则提取。
  PDF 仅作复杂图表与页序的版面核对，不作为正文主源。
  作者黄凤祁，2017 年出版，以 A 股日 K 线为主要案例背景。

# MATERIAL_POSITIONING

# SOURCE_AUDIT

| file_name | file_role | text_usability | structure_quality | conflict_status | final_decision | notes |
|---|---|---|---|---|---|---|
| 筹码分布典型形态查询手册：一本书把筹码的底细深挖到底!.epub | main_text_candidate | high | clear | no_material_conflict | use_as_main_text | 当前主源，正文 main-xhtml 可稳定提取。 |
| 同名 calibre 版 EPUB | deprecated_source | none | messy | wrong_book | discard | calibre 版已验证为空壳，不参与正文提取。 |
| 原书扫描版 PDF | pdf_layout_anchor | none | mixed | no_material_conflict | use_for_layout_check_only | 仅作复杂图表与页序核对。 |

当前裁决：

- MAIN_TEXT_SOURCE：`筹码分布典型形态查询手册：一本书把筹码的底细深挖到底!.epub`
- DEPRECATED_SOURCE：`同名 calibre 版 EPUB（空壳）`
- PDF_ASSIST_ROLE：`layout_anchor_only`
- material_type: 技术分析/筹码分布实战手册
- main_use_case: 筹码形态识别、成本区定位、调整阶段筹码变化判断、趋势方向确认
- market_scope: A 股主板、日 K 线级别
- market_scope: A 股主板、日 K 线级别
- expected_value_for_ashare: 中。书中形态语言（单峰/双峰/多峰、筹码发散/集中）可直接映射到 A 股成本分布重建；但大量案例依赖图形目视判断，需工程化近似。
- whether_directly_quantizable: 部分可代理量化。核心概念（集中度、筹码峰、浮筹、获利盘）有指标化基础；调整形态与筹码的映射需要额外几何识别。

# CONTENT_STRUCTURE
- section: 前言与基础定义
  topic: 筹码分布的定义、成本意义、散户与主力成本区分
  why_it_matters: 全书逻辑起点。后续所有形态判断都建立在"筹码=持仓成本"这一定义上。

- section: 第1章 追根溯源
  topic: 筹码与价格成本、散户成本、主力成本、筹码集中度、活跃筹码、吸筹与抛筹
  why_it_matters: 定义了散户筹码（高位、零散、移动快）与主力筹码（低位、集中、移动慢）的对立框架，是后续判断主力意图的基准。

- section: 第2章（案例辅助）
  topic: 深桑达A、华联控股、德赛电池等案例中的 ASR 指标应用
  why_it_matters: 案例层，主要验证第1章理论。因图注乱码，以保留原文规则为主，案例细节降级为辅助。

- section: 第3章 慧眼识珠
  topic: 价格调整期间筹码形态（三角形、菱形、矩形、旗形、楔形）
  why_it_matters: 调整形态是"中继"还是"反转"的判断关键。书中核心贡献是：调整结束后筹码会集中分布于调整区间内，形成可识别的筹码形态。

- section: 第4章 趋势为王
  topic: 动态转移筹码形态（单峰向上发散、单峰向下发散、削峰填谷）
  why_it_matters: 筹码转移方向=趋势方向。单峰发散是趋势延续的信号，削峰填谷是趋势结束或逆转的信号。

# RETAINED_EXCERPTS

- id: R1-001
  section: 前言
  topic: 筹码分布的核心定义
  quote: |
追根溯源：寻找筹码分布背后的秘密 筹码是投资者持仓成本的总体表现。分析筹码分布，可以清晰地发现 投资者的持股价位，在接下来的交易中就能占据非常有利的地位。本章要 研究的是筹码与价格成本，筹码集中度，活跃筹码掘金及吸筹、抛筹与筹 码转移Q 筹码形态体现了全部投资者的持仓成本分布。
  why_it_matters: 全书的基础定义。筹码分布不是成交量，而是持仓成本的统计分布。后续所有量化重建都必须以"成本分布"为语义核心。
  ashare_mapping: 对应 A 股 Level-2 逐笔数据或日线重建的成本分布近似。若只有 OHLCV，可用换手率加权近似重建持仓成本。

- id: R1-002
  section: 前言
  topic: 主力持仓成本与筹码转移
  quote: |
投资者抛售价位的信号，进而在看似公平的股票买卖中占得先机。实 际上，无论股市行情如何，只要我们知晓主力的持仓价位，便可以凭借价 格优势获得交易机会，进而获得盈利。 通常，投资者的持仓成本非常重要，而其中最重要的是主力投资者的 持仓成本。我们确认主力的持仓成本以后，就获得了战胜主力投资者的机 会。不管主力投资者如何洗盘，在没有盈利前他们是不会放手卖出股票的。 我们知道，价格运行趋势有上涨、下跌和双向波动的运行趋势。但是, 不管哪种价格运行趋势，筹码转移和投资者盈利都是必然会出现的情况。 一般看来，价格上涨期间是筹码转移的结果，只要筹码向价格高位转移的 趋势不结束，股价上涨潜力就会很大，持股就能够获得收益。特别是当我 们的持仓成本较低时，能够适应更大空间的价格波动，那么相应的可能盈 利空间也会比较大。类似的事情出现在下跌趋势中，如果股价以单边下跌 的趋势运行，筹码就会向价格低位转移的速度增加，只要筹码转移趋势未 变，股价下跌趋势就不会停止。 既然股价运行趋势是筹码转移的结果，我们就应该提早做出应对策略。 在价格上涨期间，如果我们确认筹码转移趋势即将结束，就应该早一些卖 出股票，避免在高价区被套。最后买入股票的总是亏损
  why_it_matters: 建立了"价格趋势=筹码转移"的因果链。这是后续所有吸筹/派发/洗盘判断的底层逻辑。
  ashare_mapping: 趋势持续性可通过筹码峰移动方向代理。若高位筹码峰增大而低位筹码峰萎缩，对应上升趋势中的主力派发阶段。

- id: R1-003
  section: 第1章
  topic: 散户成本与主力成本的对立框架
  quote: |
处于下跌趋势。股价涨跌与投资者的盈亏状况有最直接的关系，盈 利的投资者会考虑高价抛售股票，亏损的投资者会在价格下跌的时候"割肉减仓”。盈 利投资者持仓成本较低，更能适应价格高强度波动，因为持仓成本低意味着盈利空间 大，投资者买卖都游刃有余。亏损投资者则不同，他们的持仓成本较高，会在价格下 跌期间更为谨慎，甚至会在价格超跌的时候抛售股票，使得股价继续大幅下跌。 鉴于投资者持仓成本对股票买卖的影响很大，我们掌握多数投资者的持仓成本有 助于把握价格运行期间的买卖强度，这对于确认价格趋势也有很大帮助。 实战当中，股票筹码分布可以分为散户成本和主力成本两种分布形态。主力持仓 成本通常比较低，是具有竞争优势的低位筹码分布形态。而散户投资者更喜欢短线交 易股票，因此持仓成本通常比较高，在行情出现波动的时候，散户投资者更可能处于 不利地位。一般浮筹区域的筹码多数为散户投资者买入股票的成本区。而股价波动期 间的追涨杀跌交易通常都是散户投资者买卖股票的结果。 1.1.1筹码分布中的散户成本 追涨杀跌是很常见的交易方式，散户投资者更容易以追涨杀跌的方式交易股票， 这在筹码上表现为大规模移动的筹码形态。由于筹码移动规模较大，筹码移动速度很 快，受价格涨跌影响也会更大。
  why_it_matters: 全书分析框架的二元对立。后续几乎所有筹码形态判断都在区分"散户高位筹码"与"主力低位筹码"。
  ashare_mapping: 浮筹区域（ASR 高位）对应散户成本区；低位密集筹码峰对应主力成本区。可用获利盘比例+筹码集中度做代理区分。

- id: R1-004
  section: 第1章
  topic: 散户筹码特征
  quote: |
影响也会更大。 通常，散户投资者的持仓成本集中分布在不同的价位。价格回升期间，成本集中 在比较高的价位。如果散户投资者追涨资金较大，大量筹码就会集中分布到价格顶部。 量能无法继续放大的时候，追涨后形成的筹码通常不容易获得收益。鉴于散户投资者 的筹码分布比较零散，并且更多分布在价格高位，我们确认价格回升趋势延续的时间, 通常可以从筹码转移的规模发现结果。如果低位筹码转移到价格高位，那么低位主力 的持仓成本转移完毕。接下来的时间里，散户投资者主动价格回升趋势，股价自然容 易见顶回落。 \ 形态特征 散户投资者买卖股票并不一致，有很强的无规则性。从持仓成本来看，散户投资 者的持仓成本可以分布在连续发散的不同价位上。股价脉冲放量上涨的阶段，都是散 户投资者资金流入的时刻。确认散户投资者的持仓成本并不难，只要我们确认移动速 度最快的筹码位置就可以了。 (1)筹码零散分布 散户投资者买卖股票不容易形成一致的买卖效果，反映在筹码形态上表现为零散 分布的特征。不同价位上都会存在高抛和低吸的短线交易者的筹码，这些筹码多数是 散户投资者的持仓筹码。 (2)筹码所在价位较高 通常在价格回升期间，短线交易的特征使得散户投资者的持仓成本较高。不论何 时，
  why_it_matters: 散户筹码的"零散、高位、移动快"三特征，是判断行情顶部的关键。当高位筹码零散分布且移动快时，主力成本已转移完毕。
  ashare_mapping: 可用筹码集中度下降+高位筹码峰离散度上升作为散户主导行情的代理指标。

- id: R1-005
  section: 第1章
  topic: 主力筹码特征
  quote: |
实战当中，股票筹码分布可以分为散户成本和主力成本两种分布形态。主力持仓 成本通常比较低，是具有竞争优势的低位筹码分布形态。而散户投资者更喜欢短线交 易股票，因此持仓成本通常比较高，在行情出现波动的时候，散户投资者更可能处于 不利地位。一般浮筹区域的筹码多数为散户投资者买入股票的成本区。而股价波动期 间的追涨杀跌交易通常都是散户投资者买卖股票的结果。
  why_it_matters: 主力低位筹码是支撑位的核心来源。吸筹阶段完成后，低位筹码峰不消失是拉升的基础。
  ashare_mapping: 低位筹码峰（成本分布的底部密集区）持续时间可作为主力锁仓的代理。结合低换手率+价格横盘，可识别吸筹阶段。

- id: R1-006
  section: 第1章
  topic: 筹码集中度与浮筹指标
  quote: |
②通过浮筹指标ASR运行规律，我们确认C位置为浮筹较大的低位区。随着股价 回升空间加大，D位置的浮筹规模降到最低点，其对应的浮筹规模最小，是价格大涨 以后高位浮筹减少的结果。
  why_it_matters: ASR（浮筹指标）是本书使用最多的辅助指标。ASR 高位=筹码集中在当前价格附近，是突破/跌破的敏感区。
  ashare_mapping: ASR 可直接映射到通达信/同花顺的 ASR 指标（或自定义浮筹比例：当前价上下 10% 区间的筹码占比）。

- id: R1-007
  section: 第1章
  topic: 吸筹阶段筹码转移
  quote: |
吸筹是筹码转移的一种方式，是筹码向资金主力转移的过程。在这个过 程中，我们会发现，大量筹码集中到了主力手中，这也是股价上涨的基础。而在抛售筹 码的过程中，主力又充当了做空主力，大量筹码从主力手中流向散户投资者，这将导 致股价出现下跌趋势。 1.4.1 吸筹阶段筹码转移 主力投资者在吸筹阶段，筹码转移的数量很大，筹码转移趋势也非常明显。如果 我们确认主力放量拉升股价期间大量建仓，我们就可以通过筹码转移的方向来确认主 力投资者的持仓成本，从而指导今后的股票交易。
  why_it_matters: 吸筹的定义性描述。主力吸筹=低位筹码峰规模增大+成交量阶段性放大+价格横盘或缓升。
  ashare_mapping: 吸筹阶段代理：低位筹码峰占比持续提升 + 换手率阶段性高于 100 日均值 + 价格波动率低于历史均值。

- id: R1-008
  section: 第1章
  topic: 抛筹阶段筹码转移
  quote: |
而在抛售筹 码的过程中，主力又充当了做空主力，大量筹码从主力手中流向散户投资者，这将导 致股价出现下跌趋势。
  why_it_matters: 派发阶段的定义。高位筹码峰增大+低位筹码峰萎缩=主力向散户转移。
  ashare_mapping: 派发代理：高位筹码峰占比提升 + 低位筹码峰占比下降 + 换手率放大 + 价格滞涨。

- id: R1-009
  section: 第3章
  topic: 三角形调整与筹码集中
  quote: |
这是因为，股价在三角形调整期间波动强度较大，大量筹码充分换手以后，投 资者的持仓成本逐步集中到三角形调整形态所在的价格区间。从筹码分布来看，三角 形调整结束后筹码分布有自己明显的形态特征，也有自己独到的操作要领。
  why_it_matters: 调整形态的筹码核心规律：调整结束=筹码集中。这是判断调整是否到位的重要依据。
  ashare_mapping: 三角形/矩形等调整区间内的筹码集中度（ASR 或自定义集中度）上升，可作为调整到位的代理。

- id: R1-010
  section: 第3章
  topic: 三角形调整筹码形态特征
  quote: |
(1)筹码呈现三角形形态，筹码三角形的下限在三角形调整形态的下限以上，而 筹码三角形的上限在三角形调整形态的上限以下。 (2)筹码峰的位置与三角形调整形态相关，是调整形态结束时对应的价格区域出 现的筹码形态。 (3)筹码三角形包含了全部筹码的80%以上，是持股投资者的主要持仓成本区, 同时也是我们需要关注的交易区间。
  why_it_matters: 给出了调整形态与筹码形态的几何对应关系。筹码三角形包含 80% 以上筹码，是交易区间的核心。
  ashare_mapping: 需要额外几何识别：提取价格震荡区间的上下轨，计算区间内筹码占比。若占比 > 80%，则对应书中"筹码三角形"。

- id: R1-011
  section: 第3章
  topic: 菱形调整与筹码峰
  quote: |
在菱形调整形态中我们发现，价格波动空间呈现从小到大的趋势，最终波动空间 会不断收窄。在此期间，筹码集中度会不断提升，最终菱形调整结束的时候，筹码峰 所在价位也是菱形形态调整后的价位。
  why_it_matters: 菱形调整的筹码规律：先发散后集中，最终筹码峰位于菱形调整后价位。
  ashare_mapping: 菱形调整的几何识别较复杂，可先简化为"波动率先扩后缩+筹码集中度先降后升"的代理模式。

- id: R1-012
  section: 第4章
  topic: 单峰向上发散与趋势延续
  quote: |
趋势为王：动态转移筹码形态 筹码分布的形态主要是峰形和连续分布，而筹码转移的过程通常是筹 码峰规模增长或萎缩的过程。如果筹码峰已经呈现出集中分布的特征，那 么筹码会表现为发散形态。从集中分布的单峰筹码向发散分布的多峰筹码 转移的时候，便是投资者成本转移的过程。
  why_it_matters: 筹码峰规模变化=趋势动能变化。单峰向上发散是上升趋势确认的经典形态。
  ashare_mapping: 单峰向多峰（向上）发散可用筹码峰的重心上移代理。若筹码分布重心持续上移且集中度下降，对应上升趋势。

- id: R1-013
  section: 第4章
  topic: 单峰持续发散的建仓时机
  quote: |
总结：在量能放大期间，首次确认筹码发散趋势的时候就可以大量建仓了。A位置筹码首先发散到B位置的时候，是有效建仓的最初时机。B位置对应的价格相对较低，我们买入股票后盈利空间会很大。筹码单峰出现以后，价格就已经调整到位，行情加速运行的可能性很大。如果我们确定价格单边运行趋势形成，按照单峰筹码向多峰转换的趋势交易股票，就可以顺势获得较好的调整效果。价格波动速度越快，筹码转移速度也会越快。而想要出现停板的个股，筹码转移可以是脉冲形式的发散效果。形态特征：出现脉冲发散形态的个股，筹码通常表现出以下特征。(1)筹码具备单峰形态。
  why_it_matters: 给出了建仓时机：量能放大+首次确认筹码发散。这是从形态到交易的直接映射。
  ashare_mapping: 交易触发代理：成交量突增（> 100 日均量 1.5x）+ 筹码分布重心上移 + 获利盘比例 > 60%。

- id: R1-014
  section: 第4章
  topic: 削峰填谷与趋势逆转
  quote: |
筹码峰向筹码发散趋势转 移的时候，经常会促成股价单边运行趋势形成。而筹码发散形态向筹码峰 转移过程出现的时候，一般是价格单边趋势开始结束或者即将逆转的时候。
  why_it_matters: 全书最重要的趋势判断规则之一：发散<->集中的转换是趋势转折信号。
  ashare_mapping: 趋势转折代理：筹码集中度从低位回升（发散->集中）+ 价格振幅收窄 + 成交量萎缩。可作为顶部/底部预警。

- id: R1-015
  section: 第4章
  topic: 单峰向下发散与下跌趋势
  quote: |
从集中分布的单峰筹码向发散分布的多峰筹码 转移的时候，便是投资者成本转移的过程。当然，如果筹码已经呈现出发 散状态，那么接下来就会出现筹码由发散向集中转移的趋势Q不同的筹码 转移趋势出现的时候，价格走势也会明显不同。筹码峰向筹码发散趋势转 移的时候，经常会促成股价单边运行趋势形成。而筹码发散形态向筹码峰 转移过程出现的时候，一般是价格单边趋势开始结束或者即将逆转的时候。
  why_it_matters: 下跌趋势的筹码形态：筹码从高位单峰向低位发散，套牢盘扩大。
  ashare_mapping: 下跌代理：筹码分布重心下移 + 高位筹码峰萎缩 + 低位套牢筹码峰增大。

# CORE_CONCEPTS

- concept: 筹码分布
  plain_explanation: 全体投资者持仓成本在价格轴上的分布密度。
  original_basis: "筹码是投资者持仓成本的总体表现"
  ashare_context: 通达信/同花顺等软件提供筹码分布图，基于换手率+价格区间近似重建。A 股可用 Level-2 逐笔数据提升精度。
  quant_relevance: 基础字段。可用价格-成交量加权分布近似持仓成本。

- concept: 成本分布
  plain_explanation: 与筹码分布同义，强调投资者持仓成本的统计分布。
  original_basis: "分析筹码分布，可以清晰地发现投资者的持股价位"
  ashare_context: A 股软件中的成本分布即为此概念。
  quant_relevance: 同筹码分布。

- concept: 筹码峰
  plain_explanation: 筹码分布中密度显著高于周围区间的局部峰值，对应大量投资者持仓成本集中的价位。
  original_basis: "筹码形态体现了全部投资者的持仓成本分布"
  ashare_context: A 股软件中筹码分布图的垂直峰值。
  quant_relevance: 核心字段。峰位置、峰数量、峰高度均可量化。

- concept: 单峰
  plain_explanation: 筹码分布只呈现一个显著主峰，表明投资者成本高度集中。
  original_basis: 全书多处提及，如"单一的筹码峰已经形成"
  ashare_context: 调整结束或主力锁仓的典型形态。
  quant_relevance: 可用集中度指标（如 90% 成本区间宽度）代理。宽度窄=单峰。

- concept: 双峰
  plain_explanation: 筹码分布呈现两个显著峰值，通常对应主力成本区与散户成本区分离。
  original_basis: 书中隐含于"散户成本和主力成本两种分布形态"
  ashare_context: 常见于上涨中继或顶部派发阶段。
  quant_relevance: 需检测多峰结构。可用 KDE 峰检测或局部极大值识别。

- concept: 多峰
  plain_explanation: 筹码分布呈现多个峰值，表明成本分散，投资者分歧大。
  original_basis: "从集中分布的单峰筹码向发散分布的多峰筹码转移"
  ashare_context: 趋势运行中或趋势结束时的典型形态。
  quant_relevance: 多峰数量、峰间距、峰高度比均可量化。

- concept: 筹码集中度
  plain_explanation: 筹码分布的集中程度，通常用 70% 或 90% 成本区间的宽度表示。
  original_basis: "筹码集中度达到非常高的程度时，不仅价格波动空间非常小"
  ashare_context: 通达信等软件提供 90% 和 70% 集中度数据。
  quant_relevance: 直接可用字段。集中度低=单峰；集中度高=发散。

- concept: 套牢盘
  plain_explanation: 持仓成本高于当前价格的筹码比例。
  original_basis: 书中隐含于"亏损的投资者会在价格下跌的时候割肉减仓"
  ashare_context: A 股软件中通常显示为套牢盘比例。
  quant_relevance: 直接可用字段。高位套牢盘=压力位；低位套牢盘=支撑力减弱。

- concept: 获利盘
  plain_explanation: 持仓成本低于当前价格的筹码比例。
  original_basis: "价格处于筹码峰上方的时候，持股的投资者已经获得利润"
  ashare_context: A 股软件中通常显示为获利盘比例。
  quant_relevance: 直接可用字段。获利盘高=抛压潜在增大；获利盘低=抛压轻。

- concept: 主力成本区
  plain_explanation: 主力投资者持仓成本集中的价格区间，通常位于相对低位。
  original_basis: "主力持仓成本通常比较低，是具有竞争优势的低位筹码分布形态"
  ashare_context: 通过低位筹码峰位置+持续时间+低换手率综合识别。
  quant_relevance: 低位筹码峰位置+筹码峰持续时间可作为主力成本区代理。

- concept: 吸筹
  plain_explanation: 主力在低位大量买入股票，筹码从散户向主力转移的过程。
  original_basis: "主力投资者在吸筹阶段，筹码转移的数量很大，筹码转移趋势也非常明显"
  ashare_context: 吸筹阶段价格通常横盘或缓升，低位筹码峰增大。
  quant_relevance: 吸筹代理：低位筹码峰增大 + 换手率阶段性放大 + 价格波动率下降。

- concept: 洗盘
  plain_explanation: 主力通过打压股价，迫使低位获利的散户卖出筹码，从而降低成本区浮筹。
  original_basis: 书中隐含于"不管主力投资者如何洗盘，在没有盈利前他们是不会放手卖出股票的"
  ashare_context: 洗盘时价格回调但低位主力筹码峰不缩小。
  quant_relevance: 洗盘代理：价格回调 + 低位筹码峰稳定 + 换手率萎缩。

- concept: 派发
  plain_explanation: 主力在高位卖出筹码，筹码从主力向散户转移的过程。
  original_basis: "抛售筹码的过程中，主力又充当了做空主力，大量筹码从主力手中流向散户投资者"
  ashare_context: 高位筹码峰增大，低位筹码峰萎缩。
  quant_relevance: 派发代理：高位筹码峰增大 + 低位筹码峰萎缩 + 换手率放大 + 价格滞涨。

- concept: 换手率
  plain_explanation: 筹码转移速度的代理。高换手=筹码迁移快，低换手=筹码锁定好。
  original_basis: 全书多处将换手率与筹码转移关联。
  ashare_context: A 股直接可用字段。
  quant_relevance: 直接可用。

- concept: 成本抬升
  plain_explanation: 筹码分布重心随价格上升而上移。
  original_basis: "筹码向价格高位转移的速度增加"
  ashare_context: 上升趋势中的典型筹码形态。
  quant_relevance: 筹码分布重心（加权平均成本）上移可直接计算。

- concept: 成本下移
  plain_explanation: 筹码分布重心随价格下跌而下移。
  original_basis: "筹码就会向价格低位转移的速度增加"
  ashare_context: 下跌趋势中的典型筹码形态。
  quant_relevance: 筹码分布重心下移可直接计算。

- concept: 压力位
  plain_explanation: 价格上方存在大量套牢筹码的价位，股价回升时难以突破。
  original_basis: "在股价下跌期间，筹码大量存在的价位也是非常典型的压力位"
  ashare_context: A 股中筹码峰上限通常被视作压力位。
  quant_relevance: 筹码峰上限位置可直接作为压力位代理。

- concept: 支撑位
  plain_explanation: 价格下方存在大量获利或成本筹码的价位，股价下跌时难以跌破。
  original_basis: "寻找存在时间较长的筹码峰作为价格上涨期间的支撑位"
  ashare_context: A 股中筹码峰下限或低位密集峰可视为支撑位。
  quant_relevance: 筹码峰下限位置可直接作为支撑位代理。

- concept: 峰谷转换
  plain_explanation: 筹码从集中（峰）到发散（谷）或反向的转换过程，对应趋势转折。
  original_basis: "筹码峰向筹码发散趋势转移...一般是价格单边趋势开始结束或者即将逆转的时候"
  ashare_context: 趋势中继与趋势反转的核心判断。
  quant_relevance: 集中度变化率可作为峰谷转换的代理。

- concept: 量价共振
  plain_explanation: 成交量放大与价格突破/筹码转移同步发生，确认趋势有效性。
  original_basis: 全书多处将放量与筹码突破关联，如"量能放大会推动价格脱离筹码单峰区域"
  ashare_context: A 股中常用放量突破确认趋势。
  quant_relevance: 直接可用：成交量突增 + 价格突破筹码峰。

- concept: 筹码选股
  plain_explanation: 利用筹码形态（低位密集、单峰、高获利盘等）筛选潜在上涨股票。
  original_basis: 全书案例均隐含此逻辑，Part 2 将展开。
  ashare_context: A 股常用选股条件：低位筹码密集 + 获利盘高 + 集中度低。
  quant_relevance: 可直接进入多字段候选池。

# QUANTIZATION_TABLE

- concept: 筹码分布重建
  raw_rule_from_text: "筹码是投资者持仓成本的总体表现"
  observable_proxy: 以日 K 的收盘价/均价为锚点，用换手率加权滚动近似持仓成本分布。
  data_needed: OHLCV、换手率（或成交量+流通盘）
  quant_status: proxy_quantizable_now
  implementation_hint: |
    可用"换手率加权平均成本"近似：
    Cost_t = sum(Price_i * Turnover_i) / sum(Turnover_i)，滚动窗口 60-120 日。
    更精确可用 Amihud 风格或参考通达信筹码分布算法。
  notes: 精确重建需要逐笔数据，日线级别只能做代理。

- concept: 单峰识别
  raw_rule_from_text: "单一的筹码峰已经形成"
  observable_proxy: 90% 成本区间宽度 < 阈值（如 15%），且局部峰数量 = 1。
  data_needed: 筹码分布数据（或重建成本分布）
  quant_status: proxy_quantizable_now
  implementation_hint: |
    计算 90% 成本区间宽度（P90 - P10）。
    若宽度 < 15% 且 KDE 峰检测仅得 1 个显著峰，则标记为单峰。
    阈值需按股票波动率自适应调整。
  notes: 近似定义，标记为 proxy。

- concept: 双峰/主力-散户分离
  raw_rule_from_text: "实战当中，股票筹码分布可以分为散户成本和主力成本两种分布形态"
  observable_proxy: 筹码分布呈现两个显著峰，低位峰对应主力区，高位峰对应散户区。
  data_needed: 筹码分布数据
  quant_status: proxy_quantizable_now
  implementation_hint: |
    KDE 峰检测，若检出 2 个显著峰且峰间距 > 20%，
    且低位峰筹码占比 > 30%、高位峰占比 > 20%，则标记双峰。
    结合获利盘比例区分主力/散户峰。
  notes:  proxy/approximation。峰间距和占比阈值需按市场阶段校准。

- concept: 筹码集中度（ASR 代理）
  raw_rule_from_text: "ASR指标运行规律...筹码集中度达到非常高的程度"
  observable_proxy: 当前价上下 10% 区间内的筹码占比（ASR 定义）。
  data_needed: 筹码分布数据
  quant_status: proxy_quantizable_now
  implementation_hint: |
    ASR = (Price+10% 以下筹码 - Price-10% 以上筹码) / 总筹码。
    或直接使用通达信 ASR 指标。
    ASR > 70% 视为高浮筹/高集中。
  notes: ASR 是标准指标，可直接使用。

- concept: 获利盘比例
  raw_rule_from_text: "价格处于筹码峰上方的时候，持股的投资者已经获得利润"
  observable_proxy: 持仓成本低于当前价的筹码比例。
  data_needed: 筹码分布数据
  quant_status: proxy_quantizable_now
  implementation_hint: 直接取自筹码分布指标。可作为抛压潜在强度的反向代理。
  notes: 直接可用。

- concept: 套牢盘压力
  raw_rule_from_text: "在股价下跌期间，筹码大量存在的价位也是非常典型的压力位"
  observable_proxy: 当前价上方最近的一个显著筹码峰的位置与规模。
  data_needed: 筹码分布数据
  quant_status: proxy_quantizable_now
  implementation_hint: |
    寻找当前价上方最近的局部筹码极大值点（Peak）。
    该 Peak 的筹码量 / 总筹码量 > 20% 时，标记为强压力。
    价格接近该 Peak 时，预警突破难度。
  notes:  proxy/approximation。

- concept: 吸筹阶段代理
  raw_rule_from_text: "主力投资者在吸筹阶段，筹码转移的数量很大...成交量放大的时候，筹码转移规模才会更大"
  observable_proxy: 低位筹码峰占比持续提升 + 换手率放大 + 价格横盘/缓升。
  data_needed: 筹码分布、换手率、价格振幅
  quant_status: proxy_quantizable_now
  implementation_hint: |
    条件1：低位筹码峰（价格底部 20% 区间内）占比连续 20 日上升。
    条件2：换手率 > 100 日均值 1.2x。
    条件3：20 日价格振幅 < 15%。
    三条件同时满足，标记为吸筹代理。
  notes:  proxy/approximation。吸筹可能持续数月，需要足够长窗口。

- concept: 派发阶段代理
  raw_rule_from_text: "大量筹码从主力手中流向散户投资者，这将导致股价出现下跌趋势"
  observable_proxy: 高位筹码峰增大 + 低位筹码峰萎缩 + 价格滞涨 + 换手率放大。
  data_needed: 筹码分布、换手率、价格涨幅
  quant_status: proxy_quantizable_now
  implementation_hint: |
    条件1：高位筹码峰（价格顶部 20% 区间）占比连续 10 日上升。
    条件2：低位筹码峰占比连续 10 日下降。
    条件3：价格 10 日涨幅 < 5% 但换手率 > 100 日均值 1.3x。
    标记为派发代理。
  notes:  proxy/approximation。顶部派发常伴随诱多阳线，需结合假突破规则。

- concept: 洗盘阶段代理
  raw_rule_from_text: "不管主力投资者如何洗盘，在没有盈利前他们是不会放手卖出股票的"
  observable_proxy: 价格回调但低位主力筹码峰不缩小 + 换手率萎缩。
  data_needed: 筹码分布、换手率
  quant_status: proxy_quantizable_now
  implementation_hint: |
    条件1：价格从近期高点回调 5-15%。
    条件2：低位筹码峰占比变化 < -5%（基本稳定）。
    条件3：换手率 < 100 日均值 0.8x。
    标记为洗盘代理。
  notes:  proxy/approximation。洗盘时间通常较短，需要与下跌趋势的"低位筹码萎缩"区分。

- concept: 调整到位代理（三角形/矩形）
  raw_rule_from_text: "股价在三角形调整期间波动强度较大，大量筹码充分换手以后，投资者的持仓成本逐步集中到三角形调整形态所在的价格区间"
  observable_proxy: 价格震荡区间内筹码集中度（ASR）持续上升，最终形成单峰。
  data_needed: 价格、筹码分布、ASR
  quant_status: proxy_quantizable_now
  implementation_hint: |
    识别价格震荡区间（如布林带收口或波动率下降）。
    区间内 ASR 从 < 50% 升至 > 70%。
    同时 90% 成本宽度从宽变窄（如从 30% 缩至 15%）。
    标记为调整到位。
  notes:  proxy/approximation。需与趋势性下跌中的"筹码集中套牢"区分。

- concept: 筹码发散趋势确认
  raw_rule_from_text: "在量能放大期间，首次确认筹码发散趋势的时候就可以大量建仓了"
  observable_proxy: 成交量突增 + 筹码分布重心上移 + 单峰开始向上分裂为多峰。
  data_needed: 成交量、筹码分布
  quant_status: proxy_quantizable_now
  implementation_hint: |
    条件1：成交量 > 100 日均量 1.5x。
    条件2：筹码分布重心（加权平均成本）连续 5 日上移。
    条件3：90% 成本宽度从窄变宽（单峰->发散）。
    标记为筹码发散趋势确认。
  notes:  proxy/approximation。建仓信号需结合其他过滤条件。

- concept: 削峰填谷/趋势逆转预警
  raw_rule_from_text: "筹码发散形态向筹码峰转移过程出现的时候，一般是价格单边趋势开始结束或者即将逆转的时候"
  observable_proxy: 集中度从低位回升（发散->集中）+ 价格振幅收窄 + 成交量萎缩。
  data_needed: 筹码集中度、价格振幅、成交量
  quant_status: proxy_quantizable_now
  implementation_hint: |
    条件1：90% 成本宽度从扩张转为收缩（连续 10 日收窄）。
    条件2：20 日价格振幅 < 10% 且处于历史低位。
    条件3：成交量 < 100 日均量 0.8x。
    标记为趋势可能逆转。
  notes:  proxy/approximation。仅为预警，需等待方向确认（突破/跌破）。

- concept: 多峰结构量化
  raw_rule_from_text: "从集中分布的单峰筹码向发散分布的多峰筹码转移"
  observable_proxy: KDE 峰检测得出显著峰数量 >= 2。
  data_needed: 筹码分布密度数据
  quant_status: needs_extra_data
  implementation_hint: |
    对筹码分布做核密度估计（KDE），设定带宽参数，
    检测局部极大值点作为峰。显著峰定义为峰高度 > 均值 + 1 标准差。
    峰数量 >= 2 时标记为多峰。
  notes: 需要筹码分布密度序列，非简单指标。可归入 future_bucket。

- concept: 调整形态几何识别（三角形/菱形/旗形）
  raw_rule_from_text: "三角形调整有非常明显的三边形态...股价在三角形上限遇阻，而在下跌期间又在三角形下限遇到支撑"
  observable_proxy: 价格震荡区间的上轨、下轨收敛，形成三角形/楔形。
  data_needed: OHLC
  quant_status: future_bucket
  implementation_hint: |
    用线性回归或 Hough 变换识别价格震荡区间的上下轨。
    若上轨斜率 < 0 且下轨斜率 > 0，收敛交点在未来 20-60 日，则标记为三角形。
    菱形更复杂，需先识别扩张后收缩的波动结构。
  notes: 需要专门的几何形态识别模块。后续可与其他结构分析资料对照。

- concept: 主力锁仓比例
  raw_rule_from_text: "筹码集中度达到非常高的程度时...价格波动空间非常小"
  observable_proxy: 90% 成本宽度极窄（如 < 10%）+ 换手率极低（< 1%）。
  data_needed: 筹码集中度、换手率
  quant_status: proxy_quantizable_now
  implementation_hint: |
    90% 成本宽度 < 10% 且 20 日平均换手率 < 1%（小盘股标准需调整）。
    可标记为高度锁仓。Part 2 将细化 30%/15%/10% 锁仓标准。
  notes:  proxy/approximation。锁仓比例与流通盘大小相关，阈值需自适应。

- concept: 筹码峰持续时间
  raw_rule_from_text: "筹码存在时间越长，价格涨跌对筹码转移的影响越小"
  observable_proxy: 某价位附近筹码峰持续存在的天数。
  data_needed: 每日筹码分布序列
  quant_status: needs_extra_data
  implementation_hint: |
    对每日筹码分布做峰检测，追踪同一峰位置（±3% 区间）的连续出现天数。
    持续 > 30 日的峰标记为长期支撑/压力。
  notes: 需要历史筹码分布序列，当前多数软件不直接提供。可自建 future_bucket。

# FORMULAS_AND_ALGOS

- name: 筹码集中度近似
  source_basis: "ASR指标运行规律...筹码集中度达到非常高的程度"
  proxy_formula_or_logic: |
    90% 成本区间宽度 = P90 - P10（筹码分布的 90% 分位价）。
    宽度 < 15% 视为高度集中（单峰），15%-30% 为中等集中，> 30% 为发散。
  required_fields: 筹码分布 90% 成本区间
  caveats: proxy/approximation。不同软件筹码分布算法差异大，需同源比较。

- name: 单峰下限买点
  source_basis: "在筹码峰下限位置对应的价位上...价格不会轻易跌破筹码峰下限"
  proxy_formula_or_logic: |
    价格接近筹码峰下限（如 90% 成本下限）且成交量 < 100 日均量 0.6x 且低位筹码峰稳定。
  required_fields: 价格, 筹码峰下限, 成交量, 100日均量, 低位筹码峰占比
  caveats: proxy/approximation。缩量回踩是惜售信号，但跌破下限需止损。

- name: 单峰突破买点
  source_basis: "价格有效脱离筹码密集区的时候买入"
  proxy_formula_or_logic: |
    价格突破 90% 成本上限 + 成交量 > 100 日均量 1.5x。
  required_fields: 价格, 筹码峰上限, 成交量, 100日均量
  caveats: proxy/approximation。需确认突破非无量诱多。

- name: 吸筹阶段代理
  source_basis: "主力投资者在吸筹阶段，筹码转移的数量很大"
  proxy_formula_or_logic: |
    低位筹码峰占比连续 20 日上升 + 换手率 > 100 日均值 1.2x + 20 日价格振幅 < 15%。
  required_fields: 低位筹码峰占比, 换手率, 价格振幅
  caveats: proxy/approximation。吸筹周期可能长达数月，窗口需灵活。

- name: 派发阶段代理
  source_basis: "大量筹码从主力手中流向散户投资者"
  proxy_formula_or_logic: |
    高位筹码峰占比连续 10 日上升 + 低位筹码峰占比连续 10 日下降 + 换手率 > 100 日均值 1.3x + 10 日涨幅 < 5%。
  required_fields: 高位筹码峰占比, 低位筹码峰占比, 换手率, 价格涨幅
  caveats: proxy/approximation。顶部常伴随诱多阳线，需结合假突破规则。

- name: 调整到位代理
  source_basis: "大量筹码充分换手以后，投资者的持仓成本逐步集中到...价格区间"
  proxy_formula_or_logic: |
    价格震荡区间（20-60日）内振幅收窄 + 区间内 ASR 从 < 50% 升至 > 70% + 90% 成本宽度从 > 25% 缩至 < 15%。
  required_fields: 价格, ASR, 90%成本宽度, 成交量
  caveats: proxy/approximation。需与趋势性下跌中的"筹码集中套牢"区分。

- name: 削峰填谷/趋势逆转预警
  source_basis: "筹码发散形态向筹码峰转移过程出现的时候，一般是价格单边趋势开始结束或者即将逆转的时候"
  proxy_formula_or_logic: |
    90% 成本宽度从扩张转为收缩（连续 10 日收窄）+ 20 日价格振幅 < 10% + 成交量 < 100 日均量 0.8x。
  required_fields: 90%成本宽度, 价格振幅, 成交量
  caveats: proxy/approximation。仅为预警，需等待方向确认（突破/跌破）。

# NOT_QUANT_YET

- concept: 散户情绪与筹码移动的微观关系
  why_not_now: 书中描述散户"追涨杀跌"导致筹码零散高位分布，但缺乏可量化的散户/主力识别标签。只能做代理区分。
  what_extra_data_needed: 需要账户级别持仓数据（交易所席位数据）或资金流向数据（大单/小单拆分）来区分散户与主力。
  whether_it_is_still_valuable: 是。代理框架（低位峰=主力，高位峰=散户）在 A 股已有广泛应用，虽不完美但可用。

- concept: 筹码形态与具体 K 线图的精确对应
  why_not_now: 书中大量案例依赖 K 线图的目视判断（三角形立柱、菱形喇叭口等），需要几何形态识别算法。
  what_extra_data_needed: 需要自动化的价格形态识别模块（三角形/楔形/旗形/矩形检测）。
  whether_it_is_still_valuable: 是。后续可与其他结构分析资料对照。

- concept: 筹码峰的持续时间和"历史支撑"强度
  why_not_now: 书中提到"筹码存在时间越长，价格涨跌对筹码转移的影响越小"，但当前多数数据源只提供当日筹码分布，无历史序列。
  what_extra_data_needed: 需要自建历史筹码分布序列数据库，每日保存筹码分布密度数据。
  whether_it_is_still_valuable: 是。长期筹码峰的支撑/压力效应在 A 股实战中被广泛认可，值得自建数据。

- concept: 洗盘与下跌的精确区分
  why_not_now: 书中仅给出原则性描述（主力未盈利前不卖出），缺乏量化的洗盘 vs 下跌判别规则。
  what_extra_data_needed: 需要更精细的筹码分布追踪（如日度主力持仓比例估算）+ 价格回调深度与时间的统计模型。
  whether_it_is_still_valuable: 是。当前可用低位筹码峰稳定性做代理，但误判率较高。

- concept: 图注乱码导致的案例细节丢失
  why_not_now: OCR 后 K 线图数据（价格、成交量、ASR 数值）存在大量乱码，无法直接提取精确数值。
  what_extra_data_needed: 需要重新获取原书 PDF 的高清图注，或使用更精确的 OCR 工具。
  whether_it_is_still_valuable: 部分案例细节降级，但核心规则文本完整，不影响整体结构提取。

# NEXT_ACTION
- 可直接进入 A 股字段池: |
  ASR（浮筹比例）、获利盘比例、套牢盘比例、90% 成本宽度、70% 成本宽度、筹码分布重心（COG）、换手率。
  这些字段在通达信/同花顺等平台可直接获取或简单计算。

- 先做代理字段: |
  吸筹阶段代理、派发阶段代理、单峰/多峰识别、调整到位检测、筹码发散趋势确认。
  这些可用 OHLCV+筹码分布数据构建，但需标记 proxy/approximation。
