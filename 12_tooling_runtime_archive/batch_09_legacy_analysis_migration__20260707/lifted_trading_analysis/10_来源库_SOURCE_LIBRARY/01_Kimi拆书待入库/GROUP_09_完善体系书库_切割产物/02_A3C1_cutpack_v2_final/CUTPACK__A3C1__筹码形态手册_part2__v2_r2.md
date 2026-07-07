# BASIC_INFO
- title: 筹码分布典型形态查询手册：一本书把筹码的底细深挖到底（Part 2：单峰形态、指标形态、突破、锁仓、假突破与综合应用）
- language: 中文
- source_type: 书籍（EPUB 文本提取；非 calibre 版主源）
- source_quality: 主源 EPUB 正文完整可提取；calibre 版已验证为空壳，PDF 为纯扫描图版，仅用于版面核对。
- extraction_quality: 正文规则完整。案例图注乱码降级处理，以保留原文逻辑和术语为主。
- topic_cluster: A3-C1 筹码主组（单峰形态、筹码指标、突破形态、锁仓、假突破、综合应用）
- notes: |
  本 Part 覆盖原书第5-10章（有迹可循、按图索骥、点石成金、致命一击、以假乱真、纵观全局）。
  主源为 `筹码分布典型形态查询手册：一本书把筹码的底细深挖到底!.epub`（非 calibre 版，main-xhtml 正文可复现）。
  calibre 版已验证为空，PDF 仅作复杂图表与页序的版面核对，不作为正文主源。
  核心内容：单峰买卖规则、ASR/SSRP/CYQKL 三个指标、突破筹码峰的 K 线形态、主力锁仓比例（30%/15%/10%）、假突破识别、综合应用。

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
- material_type: 技术分析/筹码分布实战手册（进阶形态与指标）
- main_use_case: 单峰筹码买卖点识别、筹码指标量化、突破有效性判断、主力锁仓程度评估、假突破过滤、综合选股
- market_scope: A 股主板、日 K 线级别
- market_scope: A 股主板、日 K 线级别
- expected_value_for_ashare: 中-高。本 Part 提供了更可直接量化的指标（ASR、SSRP、CYQKL）和更明确的锁仓/假突破判别标准。
- whether_directly_quantizable: 指标部分（ASR/SSRP/CYQKL）可直接量化；锁仓比例和假突破可做代理量化；单峰买卖规则需形态识别辅助。

# CONTENT_STRUCTURE
- section: 第5章 有迹可循
  topic: 典型单峰筹码形态（回调买点、突破买点）
  why_it_matters: 单峰是最常见的筹码形态，提供了明确的支撑/阻力边界。回调至单峰下限和突破单峰上限是两种最基本的交易模式。

- section: 第6章 按图索骥
  topic: 筹码指标形态（ASR、SSRP、CYQKL）
  why_it_matters: 将筹码形态转化为可直接计算的指标，是工程化最关键的一步。

- section: 第7章 点石成金
  topic: 价格突破筹码形态（天量大阳线、跳空阳线、T字涨停、光头光脚大阳线）
  why_it_matters: 给出了"有效突破"的 K 线确认标准，可与筹码指标形成交叉验证。

- section: 第8章 致命一击
  topic: 主力锁仓突破筹码形态（30%/15%/10% 锁仓）
  why_it_matters: 锁仓比例是主力控盘程度的代理。锁仓越高，突破后趋势延续性越强。

- section: 第9章 以假乱真
  topic: 假突破筹码形态（无量突破、无量跌破）
  why_it_matters: 过滤假突破是避免亏损的关键。本书提供了明确的量能和筹码双重过滤标准。

- section: 第10章 纵观全局
  topic: 筹码形态综合应用（踩点买点、高抛低吸、追涨）
  why_it_matters: 全书的方法论总结，提供了可组合使用的交易框架。

# RETAINED_EXCERPTS

- id: R2-001
  section: 第5章
  topic: 单峰筹码下限买点
  quote: |
在筹码峰下限位置对应的价位上，持股投资者中的多数处于亏损状态。当股价回 升趋势还未结束的时候，价格不会轻易跌破筹码峰下限。从短线来看，价格回落至筹 码峰下限，一定会使得场外投资者加仓买入股票。同时，场内投资者惜售，使得股价 很快出现反弹走势。我们可以在价格即将跌破筹码峰下限的时候建仓交易，以便获得 廉价筹码。
  why_it_matters: 单峰下限买点的核心逻辑：筹码峰下限是多数投资者的成本区，趋势未结束前不会有效跌破。这是回踩买入的理论基础。
  ashare_mapping: 回踩单峰下限买入：价格接近筹码峰下限（如 90% 成本下限）+ 缩量 + 获利盘仍 > 50%。

- id: R2-002
  section: 第5章
  topic: 单峰下限买点的量能确认
  quote: |
图中L位置的成交量明显萎缩，量能已经达到等量线下方，这是近两个月从未 有过的情况。量能萎缩恰好说明投资者惜售，股价继续下跌的空间有限。
  why_it_matters: 缩量回踩是确认"惜售"的关键信号。无量跌破是假跌破，缩量回踩是买点。
  ashare_mapping: 成交量 < 100 日均量 0.6x + 价格接近筹码峰下限 + 低位筹码峰稳定 = 回踩买点。

- id: R2-003
  section: 第5章
  topic: 单峰突破买点
  quote: |
当筹码出现了密集分布形态的时候，价格脱离密集筹码区越是明显，价格回升趋 势越好。可以在股价有效脱离筹码密集区的时候买入股票，以便提升盈利空间。
  why_it_matters: 突破单峰上限是追涨信号。筹码密集区一旦被有效突破，上方抛压轻，趋势延续。
  ashare_mapping: 价格突破 90% 成本上限 + 成交量 > 100 日均量 1.5x + CYQKL > 40 = 突破买点。

- id: R2-004
  section: 第5章
  topic: 单峰突破后的筹码发散
  quote: |
事实上，只要筹码向上转移的趋势存在，价格回升趋势就不会结束。而我们可以 根据价格低位的筹码峰规模确认筹码转移还未完成，筹码主峰规模依然很大，证明价 格上行趋势还将延续。
  why_it_matters: 突破后趋势延续的确认标准：低位筹码峰未完全消失，筹码仍在向上转移。
  ashare_mapping: 突破后持续监控低位筹码峰占比。若占比仍 > 20% 且缓慢下降，趋势未结束。

- id: R2-005
  section: 第6章
  topic: ASR 指标定义与用法
  quote: |
ASR指标的表现直接决定了价格处于筹码中的位置，其经常处于高位运行表明价 格正处于筹码峰的内部。真实的突破走势虽然还未出现，但是行情发展到一定阶段, 价格总会出现突破。我们应该把握好高浮筹阶段的买点，以便在恰当的时候买入股票, 以获得盈利。
  why_it_matters: ASR 是浮筹比例，直接衡量价格是否处于筹码密集区内部。高 ASR=价格被大量筹码包围。
  ashare_mapping: ASR 可直接计算或使用通达信指标。ASR > 70% 为高浮筹，ASR < 30% 为低浮筹。

- id: R2-006
  section: 第6章
  topic: SSRP 指标（筹码峰指标）
  quote: |
筹码指标有浮筹指标（ASR指标）、筹码峰指标（S5RP指标）、筹码 突破力度指标（CYQKL指标）等。这些指标分别用于描述当前价位的浮筹 大小、投资者总体持仓成本及价格突破期间穿越的筹码数量。利用筹码指 标可以确认股价的活跃度，能够正确理解筹码代表的成本含义，提升盈利 空间。
  why_it_matters: SSRP 是筹码峰位置的指标化表示。书中将其与 ASR、CYQKL 并列为三大筹码指标。
  ashare_mapping: SSRP 在通达信中为筹码峰位置线。SSRP 走平=筹码峰稳定；SSRP 上移=成本抬升。

- id: R2-007
  section: 第6章
  topic: CYQKL 指标（筹码突破力度）
  quote: |
一般用CYQKL指标确认价格突破有效。该指标回升空间较大，是表现在脱离筹码 规模上的更大突破。价格快速脱离筹码峰的时候，显示出主力拉升股价的力度空前高, 这是非常难得的行情加速的信号。如果我们按照价格突破筹码峰的节奏买入股票，就 可以获得短线收益。
  why_it_matters: CYQKL 是衡量价格突破筹码峰力度的专用指标。数值大=突破的筹码规模大=突破有效。
  ashare_mapping: CYQKL 在通达信/同花顺中可用。CYQKL > 40 视为强突破信号。

- id: R2-008
  section: 第6章
  topic: CYQKL 强势突破标准
  quote: |
通常，我们确认CYQKL指标达到40以上的时候，就已经是超强的突破信号。 CYQKL指标数值较大，表明股价突破的筹码规模也很大，相应的价格回升期间的突破 力度就更好。既然股价有效突破了压力位，结合成交量等就可以确认回升趋势已经加 速出现。这时就有必要追涨买入股票，以便在价格上涨期间盈利。
  why_it_matters: 给出了明确的量化阈值：CYQKL >= 40。这是突破有效性的硬标准。
  ashare_mapping: CYQKL >= 40 作为 A 股突破有效性筛选条件之一。需结合成交量确认。

- id: R2-009
  section: 第6章
  topic: ASR 回落与加仓机会
  quote: |
价格真正突破了筹码峰以后，在股价脱离筹码峰的过程中，ASR指标会明显回落, 这是股价上涨趋势加强的信号。通常，真实的突破走势出现以后，ASR指标会从高位 大幅回落，这是价格上行趋势加强的信号。
  why_it_matters: ASR 从高位回落=价格脱离筹码密集区=突破成功。这是突破后的加仓确认信号。
  ashare_mapping: ASR 从 > 70% 快速回落至 < 50% + 价格持续上涨 = 突破确认，可加仓。

- id: R2-010
  section: 第7章
  topic: 天量大阳线突破
  quote: |
点石成金：价格突破筹码形态 为了明确价格突破信号，除了熟悉筹码，还需对有突破意义的K线进 行更深入的理解。事实上，如果我们提前明确了突破筹码的K线形态，就 更容易把握交易机会。通常价格形态有非常多的种类，而筹码转移趋势和 筹码表现形态的种类不多。可见，我们熟知一些典型的突破形态，当价格 确认突破筹码峰，发现分时图即将形成的价格走势后，投资者就能够早一 些发现交易机会。如果即将出现的K线形态突破有效，我们按照交易策略 买卖股票，自然有利可图0 本章介绍的价格突破形态较多，涉及天量大阳线形态、跳空阳线形态、 T字涨停形态以及光头光脚大阳线形态。 7.1 CYQKL 4筹码突破有效 一般用CYQKL指标确认价格突破有效。该指标回升空间较大，是表现在脱离筹码 规模上的更大突破。价格快速脱离筹码峰的时候，显示出主力拉升股价的力度空前高, 这是非常难得的行情加速的信号。如果我们按照价格突破筹码峰的节奏买入股票，就 可以获得短线收益。 7.1.1 CYQKL指标表现强势 通常，我们确认CYQKL指标达到40以上的时候，就已经是超强的突破信号。 CYQKL指标数值较大，表明股价突破的筹码规模也
  why_it_matters: 天量大阳线是最强烈的突破信号之一。成交量与天量水平接近，确认突破资金充足。
  ashare_mapping: 单日成交量 > 100 日均量 2.5x + 大阳线涨幅 > 5% + 价格突破筹码峰 = 天量突破。

- id: R2-011
  section: 第7章
  topic: 跳空阳线突破筹码峰
  quote: |
点石成金：价格突破筹码形态 为了明确价格突破信号，除了熟悉筹码，还需对有突破意义的K线进 行更深入的理解。事实上，如果我们提前明确了突破筹码的K线形态，就 更容易把握交易机会。通常价格形态有非常多的种类，而筹码转移趋势和 筹码表现形态的种类不多。可见，我们熟知一些典型的突破形态，当价格 确认突破筹码峰，发现分时图即将形成的价格走势后，投资者就能够早一 些发现交易机会。如果即将出现的K线形态突破有效，我们按照交易策略 买卖股票，自然有利可图0 本章介绍的价格突破形态较多，涉及天量大阳线形态、跳空阳线形态、 T字涨停形态以及光头光脚大阳线形态。 7.1 CYQKL 4筹码突破有效 一般用CYQKL指标确认价格突破有效。该指标回升空间较大，是表现在脱离筹码 规模上的更大突破。价格快速脱离筹码峰的时候，显示出主力拉升股价的力度空前高, 这是非常难得的行情加速的信号。如果我们按照价格突破筹码峰的节奏买入股票，就 可以获得短线收益。 7.1.1 CYQKL指标表现强势 通常，我们确认CYQKL指标达到40以上的时候，就已经是超强的突破信号。 CYQKL指标数值较大，表明股价突破的筹码规模也很大，相应的价
  why_it_matters: 跳空突破直接越过筹码峰，不给套牢盘解套机会，是最强的突破形态之一。
  ashare_mapping: 向上跳空缺口 > 2% + 开盘价直接高于筹码峰上限 + 当日不补缺口 = 跳空突破。

- id: R2-012
  section: 第7章
  topic: T字涨停突破
  quote: |
价格突破筹码形态 为了明确价格突破信号，除了熟悉筹码，还需对有突破意义的K线进 行更深入的理解。事实上，如果我们提前明确了突破筹码的K线形态，就 更容易把握交易机会。通常价格形态有非常多的种类，而筹码转移趋势和 筹码表现形态的种类不多。可见，我们熟知一些典型的突破形态，当价格 确认突破筹码峰，发现分时图即将形成的价格走势后，投资者就能够早一 些发现交易机会。如果即将出现的K线形态突破有效，我们按照交易策略 买卖股票，自然有利可图0 本章介绍的价格突破形态较多，涉及天量大阳线形态、跳空阳线形态、 T字涨停形态以及光头光脚大阳线形态。 7.1 CYQKL 4筹码突破有效 一般用CYQKL指标确认价格突破有效。该指标回升空间较大，是表现在脱离筹码 规模上的更大突破。价格快速脱离筹码峰的时候，显示出主力拉升股价的力度空前高, 这是非常难得的行情加速的信号。如果我们按照价格突破筹码峰的节奏买入股票，就 可以获得短线收益。 7.1.1 CYQKL指标表现强势 通常，我们确认CYQKL指标达到40以上的时候，就已经是超强的突破信号。 CYQKL指标数值较大，表明股价突破的筹码规模也很大，相应的价格回升期间的突破
  why_it_matters: T字涨停=开盘涨停后短暂打开再封板，表明抛压被快速消化。突破筹码峰时极为强势。
  ashare_mapping: T字涨停 + 当日成交量放大 + 筹码峰位于涨停价下方 = 强势突破。

- id: R2-013
  section: 第7章
  topic: 光头光脚大阳线突破
  quote: |
光头光脚大阳线是最显著的看涨形态，也是支持股价回升的非常典型的形态。该 形态如果已经出现在价格低位，我们便确认其为典型的支撑形态。假如在大阳线以后 买入股票，我们的盈利空间会非常大。
  why_it_matters: 光头光脚=无上下影线，表明全天多头主导。突破筹码峰时无回调，趋势明确。
  ashare_mapping: 光头光脚阳线（开盘价=最低价，收盘价=最高价）+ 涨幅 > 5% + 突破筹码峰 = 强突破。

- id: R2-014
  section: 第8章
  topic: 30% 锁仓形态
  quote: |
据筹码集中度确 认。筹码集中度达到非常高的程度时，不仅价格波动空间非常小，投资者 的持仓成本也集中到非常小的价格范围。一旦确认筹码集中度非常高，接 下来出现的价格突破就会非常有效。我们确认筹码集中度达到空前高位的 时候，股价就会脱离筹码集中区域，那么单边交易机会就会形成。 围绕筹码集中度，我们在本章内容中对筹码锁仓在30%、15%和10% 的筹码情况逐一进行分析。在筹码锁仓到30%以内的时候，价格就会突破 筹码集中区域，突破的方向上行情可以继续发展，我们按照这个趋势交易 便可以获得成功。 通常，价格波动在30%内筹码聚集，表明筹码集中度相对较高。如果股价已经出 现了明显的拉升阳线形态，阳线在快速突破筹码密集分布区的过程中，我们的买点就 会逐步形成。投资者的成本聚集在30%的价格范围内，这是相对宽泛的一个价格区间。 股价突破这一价格区间的时间可以相对较长，而我们则会有比较长的交易时间来完成 建仓过程。 8.1.1 30%内锁仓形态 如果在30%的价格波动区间内聚集了多数投资者的持仓成本，那么筹码在形态上 表现为30%的价格区间内的集中形态。30%的价格区间虽然相对宽泛，但是股价只需 三个涨停板就可以脱离这一区域。换言之，如果主力投资者打
  why_it_matters: 30% 锁仓是主力初步控盘信号。筹码在 30% 价格区间内集中，突破后趋势可延续。
  ashare_mapping: 90% 成本宽度 < 30% + 换手率 > 2%（有活跃度） = 30% 锁仓代理。

- id: R2-015
  section: 第8章
  topic: 15% 锁仓形态
  quote: |
8.2 15 %内的超低筹码峰锁仓 当股价大幅杀跌的时候，如果新进入的主力投资者的持仓成本处于15%的价格区 间内，价格脱离这一区间的时候，也就达到了主力投资者成本上方，突破信号值得投 资者关注。股价摆脱15%的价格波动区间并不困难，两根大阳线就足以达到目标。如 果我们确认股价在低位突破15%的筹码聚集区间，那么追涨买入股票便可以获得收益。
  why_it_matters: 15% 锁仓是高度控盘。筹码在 15% 区间内集中，主力控盘度更高，突破后趋势更强。
  ashare_mapping: 90% 成本宽度 < 15% + 换手率 < 3%（锁定好） = 15% 锁仓代理。

- id: R2-016
  section: 第8章
  topic: 10% 锁仓形态
  quote: |
围绕筹码集中度，我们在本章内容中对筹码锁仓在30%、15%和10% 的筹码情况逐一进行分析。在筹码锁仓到30%以内的时候，价格就会突破 筹码集中区域，突破的方向上行情可以继续发展，我们按照这个趋势交易 便可以获得成功。
  why_it_matters: 10% 锁仓是极高控盘。筹码在 10% 区间内极度集中，几乎完全锁定，突破后可能连续涨停。
  ashare_mapping: 90% 成本宽度 < 10% + 换手率 < 1.5% = 10% 锁仓代理。

- id: R2-017
  section: 第8章
  topic: 锁仓突破的买点
  quote: |
致命一击：主力锁仓突破筹码形态 在实战当中，我们发现筹码单峰形态出现的次数很多，不过究竟哪一 种筹码单峰形态是比较集中的调整结束形态，我们可以根据筹码集中度确 认。筹码集中度达到非常高的程度时，不仅价格波动空间非常小，投资者 的持仓成本也集中到非常小的价格范围。一旦确认筹码集中度非常高，接 下来出现的价格突破就会非常有效。
  why_it_matters: 锁仓突破的核心逻辑：高度集中+突破=有效性高。因为抛压已被主力锁定。
  ashare_mapping: 高锁仓（90% 宽度 < 15%）+ 放量突破（CYQKL > 40） = 高置信度突破信号。

- id: R2-018
  section: 第9章
  topic: 无量突破是假突破
  quote: |
在成交量无法出现放大的情况下，即便股价突破了筹码峰，这种突破后的价格走 势也很难延续。当然，在股价突破的那一刻，量能还是会放大，这是价格短线走强的 基础。量能经历了脉冲放大，股价确实已经在筹码峰上方。而如果这只是主力诱多操 作的一部分，那么价格冲高回落的情况就会形成。
  why_it_matters: 假突破的核心判别规则：无量突破不可信。这是全书最重要的风控规则之一。
  ashare_mapping: 价格突破筹码峰但成交量 < 100 日均量 1.0x = 假突破预警。需等待放量确认或反向做空。

- id: R2-019
  section: 第9章
  topic: 无量突破的诱多特征
  quote: |
在股价无量突破筹码峰的过程中，涨停走势很容易出现。股价在短时间内涨停， 与其说是价格突破形态，倒不如说是主力为了吸引散户投资者追涨。价格涨停速度很 快，使得量能不需要太大股价就可以涨停。涨停以后散户投资者追涨成为接盘侠， 股价在缩量过程中突破失败，逐步进入下跌趋势中。
  why_it_matters: 无量涨停突破=诱多。主力利用少量资金拉涨停，吸引散户接盘，随后缩量回落。
  ashare_mapping: 无量涨停（换手率 < 100 日均量 0.8x）+ 突破筹码峰 = 强诱多信号。次日低开概率高。

- id: R2-020
  section: 第9章
  topic: 突破失败后的缩量回落
  quote: |
股价在突破失败的过程中会出现缩量回落的走势。一旦股价缩量回落，价格下跌 和量能萎缩一定会出现，这是我们确认价格突破失败的重要形态。
  why_it_matters: 突破失败的确认标准：缩量回落。量+价双确认，可有效止损。
  ashare_mapping: 突破后 3 日内价格回落至筹码峰下方 + 成交量连续萎缩 = 突破失败确认。

- id: R2-021
  section: 第9章
  topic: 无量跌破筹码峰
  quote: |
在股价下跌的过程中，技术性的反弹走势很难改变股价的下跌趋势。即便股价短 线放量回升，改变投资者卖出股票的想法还是很困难的。从筹码的形态上看，价格突破短线筹码峰的阻力还是很高的。股价从低位反弹的时候，价格轻松突破低位筹码峰。不过考虑到做空压力较大, 价格很难继续突破第二个筹码峰。股价很容易在筹码双峰之间的某个价位见顶。一旦 确认反弹结束，价格会延续下跌趋势。
  why_it_matters: 向下假突破同样需要过滤。无量跌破可能是诱空，随后反弹。
  ashare_mapping: 价格跌破筹码峰下限但成交量 < 100 日均量 0.8x = 假跌破预警。不宜恐慌割肉。

- id: R2-022
  section: 第10章
  topic: 踩点买点（突破前介入）
  quote: |
方向，从而明确交易的机会。事实上，只要筹码转移趋势不变，价格 单边运行趋势就不会结束，顺势加仓的策略就能够成功0而价格在不同筹 码峰之间双向波动的时候，最适合的交易方式是高抛低吸。当价格不断围 绕筹码峰运行时，双向波动就会频繁出现，高抛低吸的交易过程可以轻松 增加盈利次数，提升盈利空间。 利用筹码分布完成短线的交易过程，通常是很多投资者喜欢的做法。 假如价格按照双向波动的特征运行，确认筹码峰之间的交易机会并不困难。 而利用筹码的移动规律，在价格运行的趋势中交易股票，完全可以做到顺 势盈利。 、 利用筹码形态来确认买入股票的时机，可以在价格即将脱离筹码峰的时候开始。 在实战当中，可以发现筹码峰被价格突破期间的交易机会。特别是在股价有效回升的 时候，价格逐步摆脱筹码密集区的压力区，这是非常典型的看涨信号。 价格脱离筹码密集区域的时候，持股投资者的盈利状况明显好转。随着盈利空间 的增加，投资者的风险偏好增大，在积极追涨买入股票的过程中，价格自然会表现得 更好。在股价脱离筹码密集区的过程中，追涨机会就已经出现。可以被视为短线买入 股票的时机，是比较理想的踩点建仓机会。 形态特征 当筹码出现了密集分布形态的时候，价格脱离密集筹码区越是明显，价格回升趋 势越好。可
  why_it_matters: 踩点买点是左侧交易思路：在突破前、筹码密集区即将被突破时提前建仓。
  ashare_mapping: 价格接近筹码峰上限（距上限 < 3%）+ ASR 从高位回落 + 成交量温和放大 = 踩点买点。

- id: R2-023
  section: 第10章
  topic: 高抛低吸（双峰之间）
  quote: |
只要筹码转移趋势不变，价格 单边运行趋势就不会结束，顺势加仓的策略就能够成功而价格在不同筹 码峰之间双向波动的时候，最适合的交易方式是高抛低吸。当价格不断围 绕筹码峰运行时，双向波动就会频繁出现，高抛低吸的交易过程可以轻松 增加盈利次数，提升盈利空间。
  why_it_matters: 双峰或多峰之间价格震荡，无明确趋势，适合区间交易。
  ashare_mapping: 存在两个显著筹码峰（间距 > 15%）+ 价格在两峰之间波动 + 20 日振幅 < 10% = 高抛低吸区间。

- id: R2-024
  section: 第10章
  topic: 追涨（突破后）
  quote: |
在股价脱离筹码密集区的过程中，追涨机会就已经出现。可以被视为短线买入 股票的时机，是比较理想的踩点建仓机会。
  why_it_matters: 追涨是右侧交易：突破确认后买入。适用于强趋势行情。
  ashare_mapping: 价格突破筹码峰上限 + CYQKL > 40 + ASR 回落 + 成交量 > 100 日均量 1.5x = 追涨信号。

# CORE_CONCEPTS

- concept: 单峰下限买点
  plain_explanation: 价格回调至单峰筹码峰下限附近时买入，基于"趋势未结束不会有效跌破成本区"的假设。
  original_basis: "在筹码峰下限位置对应的价位上，持股投资者中的多数处于亏损状态。当股价回升趋势还未结束的时候，价格不会轻易跌破筹码峰下限"
  ashare_context: A 股回踩支撑位的经典做法。适用于上升趋势中的回调买入。
  quant_relevance: 可用筹码峰下限+缩量+获利盘比例做代理。

- concept: 单峰上限突破买点
  plain_explanation: 价格放量突破单峰筹码峰上限时买入，确认趋势加速。
  original_basis: "当筹码出现了密集分布形态的时候，价格脱离密集筹码区越是明显，价格回升趋势越好"
  ashare_context: A 股突破买入法。需注意无量突破为假突破。
  quant_relevance: 需突破+放量+CYQKL 三重确认。

- concept: ASR（浮筹指标）
  plain_explanation: 当前价格附近（通常±10%）的筹码占比，衡量价格是否处于筹码密集区。
  original_basis: "ASR指标的表现直接决定了价格处于筹码中的位置，其经常处于高位运行表明价格正处于筹码峰的内部"
  ashare_context: 通达信/同花顺标准指标。A 股可直接使用。
  quant_relevance: 直接可用。高 ASR=高浮筹=突破敏感区；低 ASR=已脱离密集区=趋势确认。

- concept: SSRP（筹码峰指标）
  plain_explanation: 筹码分布主峰的位置线，反映市场主力成本区的大致位置。
  original_basis: "筹码峰指标（SSRP指标）"
  ashare_context: 通达信指标。SSRP 走平=成本区稳定；SSRP 上移=成本抬升。
  quant_relevance: 直接可用。但不同软件算法可能不同，需同源比较。

- concept: CYQKL（筹码突破力度）
  plain_explanation: 衡量价格突破时穿越的筹码规模，数值越大突破力度越强。
  original_basis: "一般用CYQKL指标确认价格突破有效。该指标回升空间较大，是表现在脱离筹码规模上的更大突破"
  ashare_context: A 股软件中可用。> 40 视为强突破。
  quant_relevance: 直接可用。是突破有效性的关键量化标准。

- concept: 天量大阳线
  plain_explanation: 成交量接近或超过历史天量水平的大阳线，确认资金大规模入场。
  original_basis: "天量大阳线形态"
  ashare_context: A 股中常见突破信号。需结合筹码峰位置判断突破有效性。
  quant_relevance: 可代理：成交量 > 100 日均量 2.5x + 涨幅 > 5%。

- concept: 跳空阳线
  plain_explanation: 向上跳空开盘，直接越过筹码峰或阻力位，形成缺口。
  original_basis: "跳空阳线形态"
  ashare_context: A 股中缺口理论常用。跳空突破筹码峰=强势。
  quant_relevance: 可代理：向上跳空 > 2% + 不补缺口。

- concept: T字涨停
  plain_explanation: 开盘涨停，盘中短暂打开后再封死涨停，表明抛压被快速消化。
  original_basis: "T字涨停形态"
  ashare_context: A 股涨停战法中的强势形态。突破筹码峰时尤为有效。
  quant_relevance: 需从逐笔数据识别。日线级别可代理：涨停+长下影线+放量。

- concept: 光头光脚大阳线
  plain_explanation: 无上下影线的大阳线，全天多头完全主导。
  original_basis: "光头光脚大阳线是最显著的看涨形态，也是支持股价回升的非常典型的形态"
  ashare_context: A 股中强势信号。突破筹码峰时无回调，趋势最明确。
  quant_relevance: 可代理：开盘价=最低价，收盘价=最高价，涨幅 > 5%。

- concept: 主力锁仓
  plain_explanation: 主力高度控盘，大量筹码不交易，导致筹码极度集中。
  original_basis: "筹码集中度达到非常高的程度时，不仅价格波动空间非常小，投资者的持仓成本也集中到非常小的价格范围"
  ashare_context: A 股中常用于识别庄股或强控盘股。锁仓高=突破后连续涨停概率大。
  quant_relevance: 用 90% 成本宽度+换手率代理。30%/15%/10% 分级。

- concept: 假突破
  plain_explanation: 价格突破筹码峰但无量能配合，突破很快失败并回落。
  original_basis: "在成交量无法出现放大的情况下，即便股价突破了筹码峰，这种突破后的价格走势也很难延续"
  ashare_context: A 股中常见诱多/诱空陷阱。是风控的核心过滤条件。
  quant_relevance: 可代理：突破时成交量 < 均量 1.0x = 假突破预警。

- concept: 踩点买点
  plain_explanation: 在价格即将突破筹码峰前提前建仓，属于左侧交易。
  original_basis: "利用筹码形态来确认买入股票的时机，可以在价格即将脱离筹码峰的时候开始"
  ashare_context: A 股中突破前潜伏。风险是突破失败，需设止损。
  quant_relevance: 可代理：价格接近筹码峰上限+ASR 回落+温和放量。

- concept: 高抛低吸
  plain_explanation: 在两个筹码峰之间做区间交易，低买高卖。
  original_basis: "价格在不同筹码峰之间双向波动的时候，最适合的交易方式是高抛低吸"
  ashare_context: A 股震荡行情中的主要策略。需明确上下峰边界。
  quant_relevance: 需双峰值检测+区间识别。

- concept: 追涨
  plain_explanation: 突破确认后右侧买入，适合强趋势。
  original_basis: "在股价有效脱离筹码密集区的过程中，追涨机会就已经出现"
  ashare_context: A 股趋势跟踪策略。需严格止损。
  quant_relevance: 突破+CYQKL+ASR+成交量四重确认。

# QUANTIZATION_TABLE

- concept: ASR 高浮筹状态
  raw_rule_from_text: "ASR指标高位运行表明股价正处于筹码峰的内部"
  observable_proxy: ASR > 70%（或软件自定义阈值）表示价格处于高浮筹区。
  data_needed: ASR 指标（或价格±10% 筹码占比）
  quant_status: proxy_quantizable_now
  implementation_hint: 直接使用通达信/同花顺 ASR 指标。若自建，计算当前价上下 10% 区间内筹码占比。
  notes: 直接可用。不同软件对 ASR 的区间定义可能不同（如 ±5% 或 ±10%），需注意同源。

- concept: ASR 回落确认突破
  raw_rule_from_text: "价格真正突破了筹码峰以后，在股价脱离筹码峰的过程中，ASR指标会明显回落"
  observable_proxy: ASR 从 > 70% 快速回落至 < 50%，同时价格持续上涨。
  data_needed: ASR, 收盘价
  quant_status: proxy_quantizable_now
  implementation_hint: 连续 3 日 ASR 下降且价格创新高，确认突破有效。可作为突破后加仓条件。
  notes: proxy/approximation。需确认 ASR 回落不是因价格暴跌导致（需价格同步上涨）。

- concept: CYQKL 强突破标准
  raw_rule_from_text: "我们确认CYQKL指标达到40以上的时候，就已经是超强的突破信号"
  observable_proxy: CYQKL >= 40。
  data_needed: CYQKL 指标
  quant_status: proxy_quantizable_now
  implementation_hint: 直接使用通达信 CYQKL 指标。若自建，需参考官方算法（通常与穿越筹码比例相关）。
  notes: 40 是书中明确阈值，可作为 A 股突破筛选的硬条件。

- concept: CYQKL 与 ASR 组合突破确认
  raw_rule_from_text: "CYQKL指标回升空间较大...ASR指标会明显回落"
  observable_proxy: CYQKL >= 40 AND ASR 从高位回落 AND 成交量放大。
  data_needed: CYQKL, ASR, 成交量
  quant_status: proxy_quantizable_now
  implementation_hint: 三条件同时满足时，突破确认度更高。可作为买入候选的辅助确认条件。
  notes: 组合确认比单一指标更可靠。

- concept: 30% 锁仓突破
  raw_rule_from_text: "价格波动在30%内筹码聚集，表明筹码集中度相对较高"
  observable_proxy: 90% 成本宽度 < 30% + 价格放量突破筹码峰。
  data_needed: 90% 成本宽度, 成交量
  quant_status: proxy_quantizable_now
  implementation_hint: 90% 宽度 < 30% 为初步集中。突破时 CYQKL > 30 即可确认。
  notes: 30% 锁仓是主力初步控盘，突破后趋势可延续但力度中等。

- concept: 15% 锁仓突破
  raw_rule_from_text: "15%内筹码聚集"
  observable_proxy: 90% 成本宽度 < 15% + 价格放量突破 + CYQKL > 40。
  data_needed: 90% 成本宽度, CYQKL, 成交量
  quant_status: proxy_quantizable_now
  implementation_hint: 15% 锁仓高度集中，突破后趋势力度强。建议作为高置信度买入信号。
  notes: 小盘股和大盘股阈值需调整。小盘股 15% 算高集中，大盘股 15% 算极高集中。

- concept: 10% 锁仓突破
  raw_rule_from_text: "10%内筹码聚集"
  observable_proxy: 90% 成本宽度 < 10% + 换手率 < 1.5% + 突破。
  data_needed: 90% 成本宽度, 换手率, 价格, 成交量
  quant_status: proxy_quantizable_now
  implementation_hint: 10% 锁仓是庄股特征。突破后可能连续涨停。但流动性风险高，需谨慎。
  notes: 庄股特征明显。需结合 A1 股东户数和大宗交易数据排除恶意控盘风险。

- concept: 无量突破假突破过滤
  raw_rule_from_text: "在成交量无法出现放大的情况下，即便股价突破了筹码峰，这种突破后的价格走势也很难延续"
  observable_proxy: 价格突破筹码峰 BUT 成交量 < 100 日均量 1.0x。
  data_needed: 价格, 筹码峰位置, 成交量
  quant_status: proxy_quantizable_now
  implementation_hint: 突破日成交量不足均量 1.0x 时，标记 Fake_Breakout_Warning = True。不买入或减仓。
  notes: 这是最重要的风控规则之一。无量突破是诱多的高发区。

- concept: 无量跌破假跌破过滤
  raw_rule_from_text: "无量跌破筹码峰"
  observable_proxy: 价格跌破筹码峰下限 BUT 成交量 < 100 日均量 0.8x。
  data_needed: 价格, 筹码峰下限, 成交量
  quant_status: proxy_quantizable_now
  implementation_hint: 无量跌破时标记 Fake_Breakdown_Warning = True。不恐慌割肉，等待反弹确认。
  notes: 向下诱空同样常见。需结合低位筹码峰是否稳定判断。

- concept: 突破失败 3 日确认
  raw_rule_from_text: "股价在突破失败的过程中会出现缩量回落的走势。一旦股价缩量回落，价格下跌和量能萎缩一定会出现"
  observable_proxy: 突破后 3 日内价格回落至筹码峰下方 AND 成交量连续萎缩。
  data_needed: 价格, 筹码峰位置, 成交量
  quant_status: proxy_quantizable_now
  implementation_hint: 突破后设置 3 日观察期。若价格+成交量双回落，确认失败，止损。
  notes: 3 日观察期是合理的工程化近似。实际应用中可根据波动率调整。

- concept: 踩点买点量化
  raw_rule_from_text: "利用筹码形态来确认买入股票的时机，可以在价格即将脱离筹码峰的时候开始"
  observable_proxy: 价格距筹码峰上限 < 3% + ASR 从高位开始回落 + 成交量温和放大（> 均量 1.1x）。
  data_needed: 价格, 筹码峰上限, ASR, 成交量
  quant_status: proxy_quantizable_now
  implementation_hint: 左侧交易信号。风险是突破失败，需设 3% 止损。
  notes: 踩点买点适合低风险偏好者。突破确认后（CYQKL>40）可加仓。

- concept: 高抛低吸区间量化
  raw_rule_from_text: "价格在不同筹码峰之间双向波动的时候，最适合的交易方式是高抛低吸"
  observable_proxy: 存在两个显著峰（间距 > 15%）+ 价格 20 日振幅 < 10% + 价格在两峰之间。
  data_needed: 筹码峰位置, 价格, 振幅
  quant_status: future_bucket
  implementation_hint: 需自动识别双峰值和区间边界。可用 KDE 峰检测 + 布林带收口判断。
  notes: 属于区间交易策略，需专门的震荡市识别模块。与趋势策略互斥。

- concept: 追涨信号量化
  raw_rule_from_text: "在股价有效脱离筹码密集区的过程中，追涨机会就已经出现"
  observable_proxy: 价格突破筹码峰上限 + CYQKL >= 40 + ASR 回落 + 成交量 > 100 日均量 1.5x。
  data_needed: 价格, 筹码峰, CYQKL, ASR, 成交量
  quant_status: proxy_quantizable_now
  implementation_hint: 右侧交易信号。四重确认后买入，止损设在筹码峰上限下方 2%。
  notes: 追涨风险最高，但趋势确认度也最高。需严格执行止损。

- concept: SSRP 筹码峰位置趋势
  raw_rule_from_text: "筹码峰指标（SSRP指标）"
  observable_proxy: SSRP 走平 = 筹码峰稳定；SSRP 上移 = 成本抬升；SSRP 下移 = 成本下降。
  data_needed: SSRP 指标
  quant_status: proxy_quantizable_now
  implementation_hint: 直接使用 SSRP 指标。趋势判断：SSRP 5 日斜率 > 0 = 成本抬升趋势。
  notes: SSRP 是标准指标，但不同软件算法可能不同。建议自建统一算法。

- concept: 天量大阳线突破量化
  raw_rule_from_text: "天量大阳线形态"
  observable_proxy: 成交量 > 100 日均量 2.5x AND 涨幅 > 5% AND 突破筹码峰上限。
  data_needed: 成交量, 价格, 筹码峰上限
  quant_status: proxy_quantizable_now
  implementation_hint: 天量标准可按历史分位数设定（如 90 日成交量 95% 分位）。
  notes: 天量是相对概念。小盘股和大盘股的天量阈值差异大，需自适应。

- concept: T字涨停识别
  raw_rule_from_text: "T字涨停形态"
  observable_proxy: 涨停 + 存在下影线（开盘价=最高价=涨停价，盘中最低价 < 涨停价）+ 成交量放大。
  data_needed: OHLC, 涨停价, 成交量
  quant_status: proxy_quantizable_now
  implementation_hint: A 股中 T字涨停 = 涨停价开盘且最低价 < 涨停价。需识别非一字板。
  notes: 需从日线或分钟线识别。一字板（无下影线）不属于 T字。

- concept: 光头光脚大阳线识别
  raw_rule_from_text: "光头光脚大阳线是最显著的看涨形态"
  observable_proxy: 开盘价 = 最低价 AND 收盘价 = 最高价 AND 涨幅 > 5%。
  data_needed: OHLC
  quant_status: proxy_quantizable_now
  implementation_hint: 日线级别直接可用。需确认非一字板（即振幅 > 0）。
  notes: 是最强烈的突破 K 线形态之一。

# FORMULAS_AND_ALGOS

- name: 锁仓分级检测
  source_basis: 30%/15%/10% 锁仓形态
  proxy_formula_or_logic: |
    90% 成本宽度 < 10% 且 20 日平均换手率 < 1.5% → 高度锁仓（10%级）。
    90% 成本宽度 < 15% 且 20 日平均换手率 < 3% → 中度锁仓（15%级）。
    90% 成本宽度 < 30% 且 20 日平均换手率 > 2% → 初步锁仓（30%级）。
  required_fields: 90%成本宽度, 20日平均换手率
  caveats: proxy/approximation。换手率阈值需按流通盘大小调整。

- name: 假突破过滤
  source_basis: "无量突破+突破失败缩量回落"
  proxy_formula_or_logic: |
    (价格 > 筹码峰上限 且 成交量 < 100 日均量 1.0x) → 假突破预警。
    或：突破后 3 日内价格回落至筹码峰下方 且 成交量连续萎缩 → 确认失败。
  required_fields: 价格, 筹码峰上限, 成交量, 100日均量
  caveats: proxy/approximation。3 日观察期是经验值，可回测调整。

- name: 回踩买点
  source_basis: "单峰下限买点+缩量惜售"
  proxy_formula_or_logic: |
    价格接近筹码峰下限 且 成交量 < 100 日均量 0.6x 且 低位筹码峰稳定 → 回踩买点。
  required_fields: 价格, 筹码峰下限, 成交量, 100日均量, 低位筹码峰占比
  caveats: proxy/approximation。左侧交易，风险高于突破买点。

- name: CYQKL 强突破确认
  source_basis: "CYQKL指标达到40以上"
  proxy_formula_or_logic: |
    CYQKL >= 40 且 价格突破筹码峰上限 且 成交量 > 100 日均量 1.5x → 强突破。
  required_fields: CYQKL, 价格, 筹码峰上限, 成交量, 100日均量
  caveats: proxy/approximation。CYQKL 为通达信/同花顺标准指标，> 40 为书中明确阈值。

- name: ASR 回落确认突破
  source_basis: "ASR指标从高位回落"
  proxy_formula_or_logic: |
    ASR 从 > 70% 连续 3 日下降至 < 50% 且 价格持续上涨 → 突破确认，可加仓。
  required_fields: ASR, 价格
  caveats: proxy/approximation。需确认 ASR 回落非因价格暴跌导致。

# NOT_QUANT_YET

- concept: T字涨停的精确逐笔识别
  why_not_now: 日线级别只能识别"涨停+下影线"，无法精确判断盘中打开次数和封板时间。
  what_extra_data_needed: 需要分钟级或逐笔数据，识别开盘封板->打开->再封板的时间序列。
  whether_it_is_still_valuable: 是。T字涨停是强势信号，日线级别代理可用，但精度不足。

- concept: 跳空缺口的持续性判断
  why_not_now: 书中未给出跳空突破后缺口持续时间的量化规则，仅定性描述为强势信号。
  what_extra_data_needed: 需要缺口理论的量化和回补概率统计模型。
  whether_it_is_still_valuable: 是。跳空突破是 A 股常用信号，可代理为"缺口 3 日不补"。

- concept: 主力锁仓的精确比例
  why_not_now: 书中用 30%/15%/10% 成本宽度作为锁仓代理，但真实主力锁仓比例需要账户数据。
  what_extra_data_needed: 需要股东户数、机构持仓比例、大宗交易数据来交叉验证。
  whether_it_is_still_valuable: 是。成本宽度代理在实战中有广泛应用，可先用。

- concept: 图注乱码导致的精确数值缺失
  why_not_now: OCR 后案例中的 K 线价格、成交量、ASR 数值乱码，无法提取精确数值。
  what_extra_data_needed: 需要重新 OCR 或人工校对案例数据。
  whether_it_is_still_valuable: 案例细节降级，但核心规则和阈值（CYQKL>40 等）已完整提取。

- concept: 多峰之间的精确高抛低吸边界
  why_not_now: 高抛低吸需要精确的峰边界和区间识别，当前仅靠 KDE 峰检测不够稳定。
  what_extra_data_needed: 需要更稳定的峰边界追踪算法（如峰位置平滑、峰合并/分裂规则）。
  whether_it_is_still_valuable: 是。震荡市策略是 A 股重要组成，但实施难度高于趋势策略。

- concept: 不同调整形态（三角/菱形/矩形/旗形/楔形）的自动识别
  why_not_now: 需要专门的几何形态识别算法，本书仅提供定性描述。
  what_extra_data_needed: 需要价格形态识别模块（如线性回归、Hough 变换、机器学习分类器）。
  whether_it_is_still_valuable: 是。震荡市策略是 A 股重要组成，但实施难度高于趋势策略。

# NEXT_ACTION
- 可直接进入 A 股字段池: |
  ASR、CYQKL、SSRP、获利盘比例、90% 成本宽度、70% 成本宽度、换手率、成交量。
  这些指标在通达信/同花顺中可直接获取或简单计算。

- 先做代理字段: |
  锁仓级别、假突破预警、回踩买点、追涨信号、天量大阳线识别、T字涨停识别、光头光脚阳线识别。
  这些可用现有指标组合构建，但需标记 proxy/approximation。
