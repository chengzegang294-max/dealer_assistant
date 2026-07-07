# 量化选股 研究PDF总摘要 v1 (Part 1/2)

- batch_scope: 量化选股
- source_type: research_pdf
- project_role: A股 future research/data capability
- current_status: 待入库

---

## 2. 本组总体判断

- 本组资料按源目录对账后为 `42` 份 `PDF`（目录名为“40份”，但实际目录文件数为 42），以海通证券金融工程团队出品为主，研究时段集中在2005-2014年
- 内容覆盖四大方向：(1)相关性选股策略系列（全市场+5个行业实证）；(2)事件驱动策略系列（11份，涵盖业绩预告、指数调整、增减持、股权激励、高送转、定增等）；(3)选股因子研究系列（动量反转、尾部相关、Kalman Filter、因子有效性、净换手率）；(4)行业内选股与业绩弹性（钢铁、有色金属）
- 更偏可量化字段层：大量报告提供了明确的因子池、相关性检验方法、打分规则、参数设定和回测结果
- 对当前项目最有价值的方向是：(1)相关性选股框架（因子筛选→打分→组合构建）可直接复用；(2)事件驱动策略中的业绩预告、高送转、定增等事件具有稳定的历史超额收益；(3)净换手率作为新因子具有增量信息价值
- 当前不该直接进硬门控的内容：行业基本面预测（与第2组重复）、过多行业内的专门模型（钢铁/有色金属行业策略对其他行业可复制性差）

---

## 3. 单篇资料卡片区 (S-001 ~ S-021)

---

### 资料卡片 S-001

- `paper_id:` S-001
- `title:` A股全市场选股策略研究
- `group:` 量化选股
- `theme_tags:` 全市场选股、多因子、相关性分析、滚动窗口、因子打分
- `core_problem:` 如何在全市场范围内（跨行业）通过因子相关性分析筛选有效选股因子并构建投资组合
- `method_family:` stock_selection_rule
- `data_requirements:` 全市场个股日度/月度收益数据、基本面因子（ROE/ROA/毛利率/EPS等）、估值因子（PE/PB）、技术指标（MACD）
- `time_granularity:` 月度
- `target_market:` 全A股市场
- `reusable_objects_or_fields:` 备选因子库（盈利/估值/成长/技术指标）、滚动时间窗口相关性分析方法（固定起点扩展法/固定窗口滚动法）、因子排序打分规则、综合得分组合构建法
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 构建与股价变动最相关的因子库，通过历史回溯观察因子与股票收益的相关性，筛选相关性最显著的因子作为选股依据，对因子打分加权后得到股票总得分进行全市场选股。采用两种时间窗口方法（固定起点扩展/固定窗口滚动），发现PB比PE更有效，ROE和ROA要么无效要么负相关，Delta(ROA)和Delta(ROE)呈牛正熊负。2007-2010样本外数据显示超额收益显著，但2008年下跌中期和2010年下跌初期表现较差。
- `selection_style:` multi_factor

---

### 资料卡片 S-002

- `paper_id:` S-002
- `title:` A股上市公司毛利率的均值回归及选股实证
- `group:` 量化选股
- `theme_tags:` 财务因子、毛利率、均值回归、行业选股、盈利能力
- `core_problem:` 研究毛利率在行业内部和行业间的均值回归特性，以及毛利率与涨跌幅的关系
- `method_family:` factor_research
- `data_requirements:` 上市公司季度毛利率数据（剔除ST和异常值）、行业分类数据（海通二级行业）、股票月度/季度涨跌幅数据
- `time_granularity:` 季度
- `target_market:` 全A股市场（剔除金融和ST）
- `reusable_objects_or_fields:` 超额毛利率指标（公司毛利率-行业平均毛利率）、五档分级方法、毛利率与收益正相关的8个行业清单（化工/建材/机械/纺织/食品/医药/信息设备/煤炭）、季报后反转月份特征（造纸T+1月/油气与有色T+2月/医药T+2月第五档）
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 对A股上市公司毛利率进行系统研究：行业内部毛利率不存在均值回归（好公司长期战胜差公司），行业间毛利率以两个季度为周期呈现明显反转。8个行业中毛利率与季度收益高度正相关（化工/建材/机械/纺织/食品/医药/信息设备/煤炭）。极少数行业在季报公布后特定月份出现反转（造纸T+1月、油气与有色T+2月、医药T+2月第五档）。毛利率是比较可靠的财务指标，具有较强延续性。
- `selection_style:` financial_factor

---

### 资料卡片 S-003

- `paper_id:` S-003
- `title:` A股市场特征研究（一）——沪深300样本股尾部相关性观察
- `group:` 量化选股
- `theme_tags:` 尾部相关性、系统性风险、Beta、极端事件、因子研究
- `core_problem:` 研究沪深300样本股与市场指数在极端行情（尾部）时的相关性特征
- `method_family:` risk_model
- `data_requirements:` 沪深300成分股日度/5日/20日收益率数据、市场指数收益率数据
- `time_granularity:` 日度/5日/20日滚动窗口
- `target_market:` 沪深300成分股
- `reusable_objects_or_fields:` 尾部相关系数定义（市场大幅下跌时个股同步下跌的概率）、上尾/下尾相关系数、5日与20日滚动尾部相关系数序列、Hill估计方法
- `can_be_quantized_now:` partial
- `current_role:` future bucket
- `one_paragraph_summary:` 引入尾部相关系数度量个股与市场在极端价格变化时的趋同性。通过向前滚动20日收益率计算不同周期下的尾部相关系数。发现：大部分沪深300样本股与市场的尾部相关系数较高；短期（1日或5日）内个股受市场影响程度有差异，但拉长至20日后尾部相关系数出现显著性差异；市场大幅上涨状态下这一变化更明显。从Beta角度系统性风险类似的个股在尾部行为上风格迥异。
- `selection_style:` unknown

---

### 资料卡片 S-004

- `paper_id:` S-004
- `title:` A股市场特征研究（二）——波段划分新方法及应用展望
- `group:` 量化选股
- `theme_tags:` 波段划分、趋势识别、市场特征、技术分析
- `core_problem:` 如何对A股市场进行更合理的波段划分，以支持后续选股和择时策略
- `method_family:` execution_or_data_tool
- `data_requirements:` 市场指数日度OHLCV数据
- `time_granularity:` 日度
- `target_market:` A股市场指数
- `reusable_objects_or_fields:` 波段划分方法（最小涨跌幅阈值法）、波段识别规则
- `can_be_quantized_now:` partial
- `current_role:` future bucket
- `one_paragraph_summary:` 提出理想的波段划分应具备的特点：每个波段涨跌幅不小于预先指定的幅度（对应不同资金规模的可操作最小波段）。探讨波段划分在选股和择时中的应用展望，但未给出完整的量化策略框架。
- `selection_style:` unknown

---

### 资料卡片 S-005

- `paper_id:` S-005
- `title:` 从极值角度进行选股因子有效性的确认——在换手率上的实证
- `group:` 量化选股
- `theme_tags:` 极值选股、换手率、因子有效性、相关性分析、单调性检验
- `core_problem:` 从极值（而非全样本）角度验证换手率因子的选股有效性
- `method_family:` factor_research
- `data_requirements:` 个股月度换手率数据、月度收益率数据
- `time_granularity:` 月度
- `target_market:` 全A股市场
- `reusable_objects_or_fields:` 极值角度因子检验方法（关注因子取值极端的股票组合收益差异）、换手率因子极值有效性结论
- `can_be_quantized_now:` partial
- `current_role:` future bucket
- `one_paragraph_summary:` 传统因子研究从全样本出发通过相关性和单调性筛选因子，本报告提出从极值角度验证因子有效性。以换手率为实证对象，研究发现从极值角度可以更清晰地识别因子的真实选股能力。为后续系列研究（极值视角下的多因子选股策略）奠定方法论基础。
- `selection_style:` multi_factor

---

### 资料卡片 S-006

- `paper_id:` S-006
- `title:` 分析师荐股能力评定与跟踪
- `group:` 量化选股
- `theme_tags:` 分析师、荐股能力、评价体系、跟踪、另类数据
- `core_problem:` 如何根据分析师过往推荐股票的表现制定分析师评比标准，选出荐股能力优秀的分析师
- `method_family:` factor_research
- `data_requirements:` 分析师个股研究报告、推荐股票后续收益数据
- `time_granularity:` 不定（随报告发布）
- `target_market:` 全A股市场
- `reusable_objects_or_fields:` 分析师荐股能力评分模型、优秀分析师跟踪列表、分析师推荐股票的超额收益评估框架
- `can_be_quantized_now:` no
- `current_role:` 仅来源库保留
- `one_paragraph_summary:` 根据分析师过往推荐股票的表现制定评比标准，选出荐股能力优秀的分析师并跟踪其推荐的个股。发现国内已有卖方分析师评价体系存在不足，需从实际荐股收益出发建立更客观的评价框架。报告提供了评价方法论但未给出完整的可量化执行规则。
- `selection_style:` unknown

---

### 资料卡片 S-007

- `paper_id:` S-007
- `title:` 高估值，你是否师出有名？
- `group:` 量化选股
- `theme_tags:` 估值溢价、基本面、行业研究、盈利拐点、现金流
- `core_problem:` 分析A股和美股市场中行业高估值溢价行情是否伴随基本面改善
- `method_family:` factor_research
- `data_requirements:` 行业估值数据（PE/PB）、行业基本面财务数据（净利润增速、现金流增速）、行业分类数据
- `time_granularity:` 季度
- `target_market:` A股各行业 + 纳斯达克行业
- `reusable_objects_or_fields:` 估值溢价率指标（行业PE/市场平均PE）、盈利拐点识别方法、高估值行业特征总结（A股高估值持续3-4季度，美股不超过3季度）
- `can_be_quantized_now:` no
- `current_role:` 仅来源库保留
- `one_paragraph_summary:` 对比A股与美股（纳斯达克）高估值溢价行业的特征。共性：(1)基本面大幅改善是高溢价的充分条件；(2)基本面状况并非必要条件（军工/互联网等概念驱动行业例外）；(3)估值溢价率总是先行于财报披露。差异：A股高估值行情持续3-4季度，美股仅2季度左右，说明海外成熟市场估值均值回归速度更快。美股高溢价仅在盈利拐点呈现，A股在平稳成长阶段亦延续高溢价。
- `selection_style:` quality_value_growth

---

### 资料卡片 S-008

- `paper_id:` S-008
- `title:` 工欲善其事，必先利其器——选股因子深度解析
- `group:` 量化选股
- `theme_tags:` 选股因子、因子库、Alpha策略、因子分类、深度解析
- `core_problem:` 系统性地解析和分类A股市场中常用的选股因子，为Alpha策略构建提供因子库基础
- `method_family:` factor_research
- `data_requirements:` 个股基本面数据、估值数据、技术指标数据、市值数据
- `time_granularity:` 月度
- `target_market:` 全A股市场
- `reusable_objects_or_fields:` 标准化选股因子分类体系（基本面/估值/成长/技术/市值等）、因子有效性评估框架、Alpha策略因子库构建方法论
- `can_be_quantized_now:` no
- `current_role:` 仅来源库保留
- `one_paragraph_summary:` 随着A股市场衍生品丰富和做空工具多样化，通过选股寻找Alpha获取绝对收益的产品受到越来越多关注。本报告系统性解析Alpha策略中常用的选股因子，从因子定义、计算逻辑、经济含义、历史表现等维度进行深度梳理，为后续多因子选股策略构建提供标准化的因子库基础。报告更偏理论框架和方法论介绍，未提供具体可执行的策略参数。
- `selection_style:` multi_factor

---

### 资料卡片 S-009

- `paper_id:` S-009
- `title:` 极值视角下的多因子选股策略
- `group:` 量化选股
- `theme_tags:` 极值选股、多因子、因子库、因子筛选、因子打分
- `core_problem:` 从极值视角出发构建多因子选股策略，通过因子库构建、因子筛选、因子打分等步骤选股
- `method_family:` stock_selection_rule
- `data_requirements:` 个股月度收益数据、多维度因子数据（基本面/估值/技术/市值等）
- `time_granularity:` 月度
- `target_market:` 全A股市场及行业层面
- `reusable_objects_or_fields:` 极值选股框架（因子库→因子筛选→因子打分→组合构建）、全市场和行业层面的选股模型、近四年样本外跟踪记录
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 延续2010年6月推出的相关性选股策略，通过构建因子库、因子筛选、因子打分等步骤来构建股票组合。经过近四年的样本外跟踪，无论是在全市场还是行业层面，策略组合均表现良好。本报告从极值视角出发对多因子选股进行系统性研究，是相关性选股策略系列的方法论总纲和效果汇总。
- `selection_style:` multi_factor

---

### 资料卡片 S-010

- `paper_id:` S-010
- `title:` 利用分析师盈利预测数据挖掘投资机会
- `group:` 量化选股
- `theme_tags:` 分析师、盈利预测、评级数据、另类数据、选股
- `core_problem:` 考察卖方分析师个股研究报告中的评级和盈利预测数据是否具备有效的投资价值
- `method_family:` factor_research
- `data_requirements:` 卖方分析师个股研究报告评级数据、盈利预测数据（EPS/净利润等）、股票收益率数据
- `time_granularity:` 不定（随报告发布）
- `target_market:` 全A股市场
- `reusable_objects_or_fields:` 分析师评级和盈利预测选股指标构建方法、分析师预测修正信号（预测上调/下调）、定量选股指标（基于评级和预测数据）
- `can_be_quantized_now:` partial
- `current_role:` future bucket
- `one_paragraph_summary:` 考察卖方分析师个股研究报告的投资价值，根据研究报告中的评级和盈利预测数据构建定量选股指标。2006年至今的实证分析表明分析师盈利预测数据具有一定的选股能力，但受限于分析师覆盖范围、预测偏差和数据时效性，更适合作为辅助因子而非独立选股策略。需配合其他因子共同使用以提升稳定性。
- `selection_style:` unknown

---

### 资料卡片 S-011

- `paper_id:` S-011
- `title:` 量化选股之事件驱动策略
- `group:` 量化选股
- `theme_tags:` 事件驱动、系统研究、长期价值型、短期信息驱动型、定增、股权激励
- `core_problem:` 对事件驱动策略进行系统研究，按事件主题与投资风格关系分类
- `method_family:` stock_selection_rule
- `data_requirements:` 事件公告数据（业绩预告/增减持/股权激励/指数调整/定增等）、股票收益率数据
- `time_granularity:` 不定（事件触发）
- `target_market:` 全A股市场
- `reusable_objects_or_fields:` 事件驱动策略分类框架（长期价值型/短期信息驱动型）、事件驱动策略体系总纲
- `can_be_quantized_now:` no
- `current_role:` 仅来源库保留
- `one_paragraph_summary:` 对事件驱动策略进行系统研究，按照事件主题与投资风格的关系分为长期价值型事件（股权激励、大股东增减持等）和短期信息驱动型（业绩预告、ETF股票停牌套利、指数样本股调整等）。本报告为事件驱动策略系列的总纲性介绍，对各子策略的原理进行了概述，但具体参数和执行规则需参考对应专题报告。
- `selection_style:` event_driven

---

### 资料卡片 S-012

- `paper_id:` S-012
- `title:` 如何捕捉短线反弹机会？
- `group:` 量化选股
- `theme_tags:` 短线反弹、反转策略、超跌、量价指标、技术选股
- `core_problem:` 如何利用A股市场显著反转特征，结合量价指标把握股价超跌后的短线反弹机会
- `method_family:` stock_selection_rule
- `data_requirements:` 个股日度/周度收益率数据（相对沪深300超额收益）、成交量数据、技术指标数据
- `time_granularity:` 日度/周度
- `target_market:` 全A股市场
- `reusable_objects_or_fields:` 超跌定义（相对沪深300超额收益跌破10%）、短线反弹选股信号规则、量价配合确认指标
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` A股市场具有显著反转特征，结合量价指标把握股价超跌之后的短线反弹机会。定义超跌为相对沪深300超额收益跌破10%，通过量价配合等技术指标确认反弹信号。策略抓住市场过度反应后的修复行情，具有持仓周期短、换手率较高的特点，适合作为短期交易策略或组合增强模块。
- `selection_style:` momentum

---

### 资料卡片 S-013

- `paper_id:` S-013
- `title:` 商业贸易行业选股策略
- `group:` 量化选股
- `theme_tags:` 行业选股、商业贸易、相关性选股、因子分析
- `core_problem:` 针对商业贸易行业特点构建行业内选股策略
- `method_family:` stock_selection_rule
- `data_requirements:` 商业贸易行业个股财务数据、估值数据、技术指标数据、行业指数数据
- `time_granularity:` 月度
- `target_market:` 商业贸易行业
- `reusable_objects_or_fields:` 商业贸易行业专用因子库、行业内选股模型
- `can_be_quantized_now:` no
- `current_role:` 仅来源库保留
- `one_paragraph_summary:` 随着资本市场发展和企业专业化程度提高，找到适用于所有股票的选股策略非常困难，需要深入到具体行业中寻找最适合该行业的选股策略。本报告针对商业贸易行业构建专门的选股策略，是行业内选股策略研究系列的一部分。由于行业特殊性较强，策略对其他行业的可复制性有限。
- `selection_style:` multi_factor

---

### 资料卡片 S-014

- `paper_id:` S-014
- `title:` 上市公司动量反转以及市值因子的选股识别度
- `group:` 量化选股
- `theme_tags:` 动量、反转、市值因子、选股识别度、因子研究
- `core_problem:` 研究动量反转因子和市值因子在行业内的选股识别度
- `method_family:` factor_research
- `data_requirements:` 个股月度收益率数据、市值数据、行业分类数据
- `time_granularity:` 月度
- `target_market:` 全A股市场
- `reusable_objects_or_fields:` 动量/反转/市值因子的行业内选股识别度评估方法、各因子在不同行业中的有效性对比
- `can_be_quantized_now:` partial
- `current_role:` future bucket
- `one_paragraph_summary:` 延续前期对营业收入增长、毛利率、估值指标的研究方法，对动量反转和市值因子的行业内选股识别度进行系统研究。分析不同行业内部动量、反转和市值因子的选股效果差异，发现因子有效性在不同行业间存在显著分化。市值因子在多数行业中表现稳定，而动量和反转因子的效果受行业特性影响较大。
- `selection_style:` momentum

---

### 资料卡片 S-015

- `paper_id:` S-015
- `title:` 上市公司估值指标的稳定性与选股识别度
- `group:` 量化选股
- `theme_tags:` 估值指标、PE、PB、毛利率、选股识别度、稳定性
- `core_problem:` 研究PE和PB估值指标在行业内部的稳定性以及在不同行业内的选股识别度
- `method_family:` factor_research
- `data_requirements:` 个股PE/PB数据、毛利率数据、行业分类数据、月度收益率数据
- `time_granularity:` 月度
- `target_market:` 全A股市场
- `reusable_objects_or_fields:` PE/PB估值指标的行业内稳定性评估方法、估值指标选股识别度排名（哪些行业PE有效/哪些行业PB有效）、估值与毛利率结合使用的方法
- `can_be_quantized_now:` partial
- `current_role:` future bucket
- `one_paragraph_summary:` 研究PE和PB估值指标在行业内的稳定性和选股识别度。发现PE和PB在各行业中与毛利率类似具有很好的稳定性。估值指标的选股效果在不同行业间差异显著：部分行业PE更有效，部分行业PB更有效。结合前期毛利率研究成果，建议在行业内选股时同时考虑盈利能力和估值水平两个维度。
- `selection_style:` quality_value_growth

---

### 资料卡片 S-016

- `paper_id:` S-016
- `title:` 事件驱动策略之一——业绩预告之一——把握扭亏、预减公告，获取短期超额收益
- `group:` 量化选股
- `theme_tags:` 事件驱动、业绩预告、扭亏、预减、短期超额收益
- `core_problem:` 研究业绩预告公告（扭亏、预减等）公布后对上市公司短期股价的影响，从中寻找投资机会
- `method_family:` stock_selection_rule
- `data_requirements:` 上市公司业绩预告公告数据（预增/预减/首亏/扭亏）、股票日度收益率数据
- `time_granularity:` 日度（事件触发）
- `target_market:` 全A股市场
- `reusable_objects_or_fields:` 四类业绩预告公告分类（预增/预减/首亏/扭亏）、业绩预告事件超额收益计算方法、短期（公告后数日）超额收益统计规律
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 研究业绩预告公告（预增/预减/首亏/扭亏）对短期股价的影响。发现由于信息不对称，部分上市公司超额收益在公告前已反映，但可通过寻找反转指标和业绩预告超预期的股票获取短期超额收益。不同公告类型（扭亏vs预减）的市场反应方向和幅度不同，适合构建差异化的事件驱动组合。
- `selection_style:` event_driven

---

### 资料卡片 S-017

- `paper_id:` S-017
- `title:` 事件驱动策略之二——关注主板预减快报后的短期反弹机会以及中小板盈利公告
- `group:` 量化选股
- `theme_tags:` 事件驱动、业绩快报、预减、反弹、中小板、板块效应
- `core_problem:` 区分主板和中小板，研究业绩快报在不同板块中的不同表现和短期反弹机会
- `method_family:` stock_selection_rule
- `data_requirements:` 主板和中小板业绩快报/预告数据、股票日度收益率数据、反转指标数据
- `time_granularity:` 日度（事件触发）
- `target_market:` 主板 + 中小板
- `reusable_objects_or_fields:` 主板预减快报反弹信号（利空出尽后短期反弹）、中小板盈利公告超额收益规律（预增持有30日胜率65%、超额收益8%）、净利润增长来源分析框架（政府支持/市场利好/竞争力提升三类）
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 中小板对业绩快报及修正公告敏感度明显高于主板。预增和扭亏短期超额收益表现好，首亏和预减发布后超额收益随时间递减。主板股票股价与业绩公告无直接关系，但财季后预减快报存在"利空出尽"反弹机会。反转指标筛选后预增和扭亏表现进一步增强。盈利增长来源影响股价：政府支持/市场利好/竞争力提升类的超额收益确定性更高。全策略指数自2006年以来净值高达10以上。
- `selection_style:` event_driven

---

### 资料卡片 S-018

- `paper_id:` S-018
- `title:` 事件驱动策略之三——指数样本股调整
- `group:` 量化选股
- `theme_tags:` 事件驱动、指数调整、样本股、调入调出、套利
- `core_problem:` 研究指数样本股调整事件中存在的交易机会，特别是关注历史成交量较小的调入调出样本股
- `method_family:` stock_selection_rule
- `data_requirements:` 指数样本股调整公告数据（调入/调出名单）、股票日度收益率数据、成交量数据
- `time_granularity:` 日度（事件触发）
- `target_market:` 被调整指数的成分股
- `reusable_objects_or_fields:` 指数样本股调整事件时间窗口定义、调入/调出股票超额收益统计、历史成交量较小的调入调出股票重点关注名单
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 指数样本股调整带来交易机会：被调入的股票在调整前通常有被动资金流入带来的超额收益，被调出的股票则有被动卖出压力。研究发现历史成交量较小的调入调出样本股的价格效应更为显著（流动性较低导致冲击更大）。策略在调整公告日至生效日之间获取超额收益，是典型的短期事件驱动策略。
- `selection_style:` event_driven

---

### 资料卡片 S-019

- `paper_id:` S-019
- `title:` 事件驱动策略之四——ETF事件套利研究
- `group:` 量化选股
- `theme_tags:` 事件驱动、ETF套利、停牌股票、涨跌停、替代组合
- `core_problem:` 利用ETF一二级市场机制，对停牌或涨跌停无法交易的股票进行事件套利
- `method_family:` execution_or_data_tool
- `data_requirements:` ETF申购赎回清单数据、ETF净值数据、停牌股票信息、涨跌停股票信息
- `time_granularity:` 日度（事件触发）
- `target_market:` ETF及其成分股
- `reusable_objects_or_fields:` ETF事件套利机制（利用ETF成分股停牌/涨跌停时的定价偏差）、替代组合构建方法（用ETF替代无法交易的股票）、套利收益计算方法
- `can_be_quantized_now:` no
- `current_role:` 仅来源库保留
- `one_paragraph_summary:` 股票跌停时很难卖出、涨停时很难买入、停牌时无法交易。利用ETF一二级市场机制，当ETF成分股出现停牌或涨跌停时，ETF净值与成分股实际价值之间产生定价偏差，投资者可通过申购/赎回ETF并同时买卖成分股或相关替代组合进行事件套利。本报告研究ETF事件套利的机制和机会，但策略执行对交易系统和时效性要求极高。
- `selection_style:` event_driven

---

### 资料卡片 S-020

- `paper_id:` S-020
- `title:` 事件驱动策略之五——大股东增减持——关注增持比例较大的事件机会
- `group:` 量化选股
- `theme_tags:` 事件驱动、大股东增减持、增持比例、短期收益、策略指数
- `core_problem:` 研究大股东增减持事件对股价的短期影响，特别是增持比例较大的投资机会
- `method_family:` stock_selection_rule
- `data_requirements:` 大股东增减持公告数据（WIND重要股东二级市场交易明细）、股东类型（公司/高管/个人）、增减持比例、股票收益率数据
- `time_granularity:` 日度（事件触发）
- `target_market:` 全A股市场
- `reusable_objects_or_fields:` 大股东增减持事件信号（增持比例大的超额收益显著）、14日超额收益最大化时间窗口、高管增持vs公司增持区分（高管增持超额收益更显著）、策略指数（5年相对沪深300超额收益470%、累积收益590%、年化36%）
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 研究大股东增减持对股价的短期影响。增持股票组合总能战胜减持组合，相对沪深300超额收益在第14个自然日达到最大后衰减。高管增持组合超额收益比公司增持更显著。增减持变动幅度较大的组合超额收益显著。策略不分牛熊市均有效（2007年极端环境除外）。周度选股策略5年累积收益590%，年化36%，信息比率0.6。
- `selection_style:` event_driven

---

### 资料卡片 S-021

- `paper_id:` S-021
- `title:` 事件驱动策略之六——规避预案陷阱，把握实施收益
- `group:` 量化选股
- `theme_tags:` 事件驱动、股权激励、预案公告、实施公告、行权价
- `core_problem:` 研究股权激励事件对股价的驱动作用，找到最佳参与时点
- `method_family:` stock_selection_rule
- `data_requirements:` 股权激励公告数据（预案/首次实施/行权条件）、激励股票数量、行权价、股票收益率数据
- `time_granularity:` 日度（事件触发）
- `target_market:` 全A股市场（主板+中小板）
- `reusable_objects_or_fields:` 股权激励事件时间线（预案→首次实施→行权）、首次实施公告介入信号（超额收益空间最大）、预案与实施间隔期信号（间隔短后期走势更稳定）、激励占比信号（占总股本比例越高驱动越强）、行权价折溢价信号（折价越多参与价值越大）
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 股权激励事件中，预案公告后难以确定计划是否最终实施（未实施者后期无参与价值），建议将投资时点设在首次实施公告后。实施与预案间隔短的公司后期走势更稳定。激励股票占总股本比例越高对股价驱动越明显（6%-8%区间表现极突出但样本少）。溢价行权需合理溢价空间，折价行权"多多益善"。长持有期低换仓策略（持有9个月）2006年8月以来累积收益1687.4%，年化67.2%，年化超额59.7%。
- `selection_style:` event_driven

---

## 4. 本组可重开候选清单 (Part 1)

---

### 候选 S-C01

- `candidate_id:` S-C01
- `candidate_name:` 相关性选股全市场框架
- `from_paper:` S-001 / S-025（全市场改进）
- `why_it_matters:` 提供了一套完整的从因子库构建到组合形成的系统化选股框架，滚动窗口自动筛选有效因子能适应市场风格变化，是量化选股的核心基础设施
- `minimum_input:` 全市场个股月度因子数据（基本面/估值/技术/市值，24个因子+）、月度收益率数据
- `minimum_output:` 每期有效因子列表、个股综合得分排名、TOP10%/20%组合、超额收益统计
- `current_role:` 可重开

### 候选 S-C02

- `candidate_id:` S-C02
- `candidate_name:` 毛利率行业选股模型
- `from_paper:` S-002
- `why_it_matters:` 毛利率是延续性强的财务指标，行业内无均值回归意味着好公司持续战胜差公司。8个行业中毛利率与收益高度正相关，可直接作为行业选股增强因子
- `minimum_input:` 上市公司季度毛利率数据、行业分类数据、月度/季度收益率数据
- `minimum_output:` 超额毛利率指标（公司-行业均值）、行业内五档分级、正相关行业清单、选股组合收益
- `current_role:` 可重开

### 候选 S-C03

- `candidate_id:` S-C03
- `candidate_name:` 大股东增减持事件驱动策略
- `from_paper:` S-020
- `why_it_matters:` 大股东增减持数据公开可得、信号频率适中、历史超额收益显著（5年累积590%），且不分牛熊市均有效。是事件驱动方向最成熟的策略之一
- `minimum_input:` 大股东增减持公告数据（含股东类型、增减持比例）、股票日度收益率数据
- `minimum_output:` 增持事件信号（关注增持比例大的）、14日持有期超额收益、高管增持/公司增持分类信号
- `current_role:` 可重开

---

## 5. future bucket 清单 (Part 1)

---

- `item:` 分析师荐股能力评价与跟踪系统
- `why_future_only:` 需要完整的分析师报告数据库和长期跟踪体系，数据获取成本高，且分析师覆盖范围和预测质量随时间变化大，难以标准化

- `item:` 分析师盈利预测数据选股
- `why_future_only:` 分析师覆盖范围有限（主要覆盖大盘股），预测存在系统性偏差，更适合作为辅助因子而非独立策略

- `item:` 极值视角下的多因子选股框架完善
- `why_future_only:` S-005和S-009提出了极值选股的方法论框架，但缺乏完整的参数设定和系统性回测，需进一步研究极值因子的组合方式和权重分配

---

## 6. 仅来源库保留清单 (Part 1)

---

- `paper_id:` S-003 / S-004
- `title:` A股市场特征研究（一/二）——尾部相关性观察 / 波段划分新方法
- `reason:` 更偏基础研究性质，未提供可直接执行的选股策略或明确的量化规则，尾部相关系数计算复杂度高，波段划分方法主观性较强

- `paper_id:` S-006
- `title:` 分析师荐股能力评定与跟踪
- `reason:` 方法论介绍为主，未提供完整的可量化执行规则和回测结果

- `paper_id:` S-007
- `title:` 高估值，你是否师出有名？
- `reason:` 行业层面的定性比较研究，未提供可直接用于选股的量化指标或策略规则

- `paper_id:` S-008
- `title:` 工欲善其事，必先利其器——选股因子深度解析
- `reason:` 因子分类和解析的框架性介绍报告，未提供具体可执行的策略参数

- `paper_id:` S-011
- `title:` 量化选股之事件驱动策略
- `reason:` 事件驱动策略系列的总纲介绍，各子策略的具体参数需参考对应专题报告

- `paper_id:` S-013
- `title:` 商业贸易行业选股策略
- `reason:` 单一行业策略，对其他行业可复制性差

- `paper_id:` S-019
- `title:` 事件驱动策略之四——ETF事件套利研究
- `reason:` 策略执行对交易系统和时效性要求极高（需ETF申赎机制配合），与当前项目框架不匹配

---

*Part 1 结束，资料卡片 S-022~S-041 及完整候选清单、去重建议、最终建议见 Part 2。*
