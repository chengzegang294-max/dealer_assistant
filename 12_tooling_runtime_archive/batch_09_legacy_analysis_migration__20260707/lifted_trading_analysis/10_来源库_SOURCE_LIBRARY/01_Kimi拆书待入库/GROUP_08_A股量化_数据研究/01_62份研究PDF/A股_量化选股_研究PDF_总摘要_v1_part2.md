# 量化选股 研究PDF总摘要 v1 (Part 2/2)

- batch_scope: 量化选股（续）
- source_type: research_pdf
- project_role: A股 future research/data capability
- current_status: 待入库

---

## 3. 单篇资料卡片区 (S-022 ~ S-041)

---

### 资料卡片 S-022

- `paper_id:` S-022
- `title:` 事件驱动策略之七——高送转行情下的事件性投资机会
- `group:` 量化选股
- `theme_tags:` 事件驱动、高送转、送红股、资本公积金转增、命中率
- `core_problem:` 研究高送转（大比例送红股或资本公积金转增股本）事件对股价的驱动效应
- `method_family:` stock_selection_rule
- `data_requirements:` 高送转预案/实施公告数据（送转比例）、股价数据、基本面数据（每股资本公积金/未分配利润/股价等）
- `time_granularity:` 日度（事件触发）
- `target_market:` 全A股市场
- `reusable_objects_or_fields:` 高送转预测指标（每股资本公积金高/未分配利润高/股价高/总股本小）、高送转事件时间窗口收益统计、2011年高送转预测命中率已达90%
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 高送转是大比例送红股或资本公积金转增股本的行为，表明公司对业绩增长的信心。预案公告后至股权登记日之间通常存在显著超额收益。通过每股资本公积金、未分配利润、股价、总股本等指标可提前预测高送转概率，2011年预测命中率已达90%。策略在每年年报和半年报披露期集中布局，是典型的季节性事件驱动策略。
- `selection_style:` event_driven

---

### 资料卡片 S-023

- `paper_id:` S-023
- `title:` 事件驱动策略之九——股权激励续篇
- `group:` 量化选股
- `theme_tags:` 事件驱动、股权激励、行权条件、窗口期、超额收益递减
- `core_problem:` 对股权激励整个投资周期进行系统研究，寻找不同阶段的最佳参与时点
- `method_family:` stock_selection_rule
- `data_requirements:` 股权激励全周期公告数据（预案/首次实施/行权/解锁）、行权条件细则、业绩基准设置、股票收益率数据
- `time_granularity:` 日度（事件触发）
- `target_market:` 全A股市场
- `reusable_objects_or_fields:` 股权激励全周期时间线（预案→股东大会通过→首次实施→行权/解锁）、不同窗口期超额收益统计、行权条件影响（条件苛刻者后期表现更好）、超额收益边际递减规律
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 对股权激励整个投资周期进行系统研究：预案→股东大会通过→首次实施→行权/解锁各阶段均有不同超额收益特征。行权条件苛刻（业绩基准要求高）的公司后期股价表现更好。首次实施公告是最佳介入时点（与S-021一致）。超额收益存在边际递减效应，同一事件后期参与价值降低。需关注激励对象、激励比例、行权价折溢价等细节对收益的调节作用。
- `selection_style:` event_driven

---

### 资料卡片 S-024

- `paper_id:` S-024
- `title:` 事件驱动策略之十一——事件驱动组合止损机制设计
- `group:` 量化选股
- `theme_tags:` 事件驱动、止损机制、回撤控制、大小盘风格切换、系统性风险
- `core_problem:` 设计事件驱动策略组合的止损机制，应对大小盘风格切换时的集体回撤
- `method_family:` risk_model
- `data_requirements:` 事件驱动策略组合日度净值数据、中证500/中小板指数数据、风格指数相对强弱数据
- `time_granularity:` 日度
- `target_market:` 事件驱动策略组合
- `reusable_objects_or_fields:` 事件驱动策略回撤与风格切换的关联规律、策略间相关性变动预警信号、止损触发条件（相关性异常升高+风格指数走弱）
- `can_be_quantized_now:` partial
- `current_role:` future bucket
- `one_paragraph_summary:` 事件驱动策略多数具有偏中小盘的风格特征，当市场发生大小盘风格切换时总会集体经历较大回撤。通过跟踪事件驱动策略之间的相关性变动可以形成有效的回撤止损信号——策略间相关性异常升高预示系统性风险积聚，配合风格指数走弱信号可触发组合止损。本报告为止损机制设计报告，需结合具体事件策略组合使用。
- `selection_style:` event_driven

---

### 资料卡片 S-025

- `paper_id:` S-025
- `title:` 事件驱动策略之十二——重要股东持股结构变化蕴含的信息分析
- `group:` 量化选股
- `theme_tags:` 事件驱动、股东持股结构、大股东、机构投资者、持股变化
- `core_problem:` 利用大股东和机构投资者持股变化信息探寻与未来股价走势的关系
- `method_family:` stock_selection_rule
- `data_requirements:` 上市公司股东持股结构数据（大股东/机构投资者持股变动）、股票收益率数据
- `time_granularity:` 季度（随季报披露）
- `target_market:` 全A股市场
- `reusable_objects_or_fields:` 大股东增持信号（持股比例提升的积极信号）、机构投资者增持信号（基金/保险/QFII等）、股东持股集中度变化指标、持股结构变化与未来收益的相关性统计
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 上市公司股东持股变化反映其对公司未来发展的预期。大股东增持通常预示积极信号，机构投资者增持则代表专业投资者看好。通过分析大股东和机构持股者的持股变化信息，可以发掘与未来股价走势的正相关关系。策略在季报披露后根据最新持股结构变化调整组合，是季度频率的基本面事件驱动策略。
- `selection_style:` event_driven

---

### 资料卡片 S-026

- `paper_id:` S-026
- `title:` 事件驱动策略之十三——定增事件投资——甄别市场，把握买点
- `group:` 量化选股
- `theme_tags:` 事件驱动、定向增发、定增、解禁、折价率、市场甄别
- `core_problem:` 研究定向增发事件的投资机会，特别是增发类股票即将解禁前的超额收益机会
- `method_family:` stock_selection_rule
- `data_requirements:` 定向增发公告数据（预案/发行/解禁时间点）、定增价格、折价率、股票收益率数据
- `time_granularity:` 日度（事件触发）
- `target_market:` 全A股市场
- `reusable_objects_or_fields:` 定增事件时间线（预案→发行→解禁）、解禁前超额收益机会（提前60日布局）、折价率信号（折价大的参与价值高）、市场状态甄别（牛市参与定增收益更高）
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 定向增发事件中，增发类股票即将解禁前存在超额收益机会（股价启动不会太过提前，临近解禁时参与）。提前60日布局效果较好。折价率大的定增参与价值更高。需甄别市场状态——牛市中定增收益更高，熊市中需谨慎。策略关注解禁日期并提前布局，是典型的日历驱动型事件策略。
- `selection_style:` event_driven

---

### 资料卡片 S-027

- `paper_id:` S-027
- `title:` 现金流量市值比因子的极值效应
- `group:` 量化选股
- `theme_tags:` 极值选股、现金流市值比、财务因子、因子有效性
- `core_problem:` 从极值角度验证现金流量市值比因子的选股有效性
- `method_family:` factor_research
- `data_requirements:` 个股经营活动现金流数据、市值数据、月度收益率数据
- `time_granularity:` 月度
- `target_market:` 全A股市场
- `reusable_objects_or_fields:` 现金流量市值比因子（经营现金流/市值）极值选股效果、极值因子有效性评估方法
- `can_be_quantized_now:` partial
- `current_role:` future bucket
- `one_paragraph_summary:` 延续因子极值选股研究系列，从极值角度验证现金流量市值比因子的有效性。相比全样本分析，极值视角下因子选股效果更显著。经营现金流/市值比率极端值（最高/最低）的股票组合收益差异明显，高现金流市值比股票具有显著超额收益。可与S-005（换手率极值）、S-009（极值多因子框架）结合构建多因子极值选股组合。
- `selection_style:` financial_factor

---

### 资料卡片 S-028

- `paper_id:` S-028
- `title:` 相关性选股策略——全市场选股方法改进
- `group:` 量化选股
- `theme_tags:` 相关性选股、全市场、因子扩充、短样本、长样本
- `core_problem:` 对全市场相关性选股策略进行改进，扩充因子库并优化选股方法
- `method_family:` stock_selection_rule
- `data_requirements:` 全市场个股月度因子数据（24个因子：基本面/规模/估值/技术面）、月度收益率数据
- `time_granularity:` 月度
- `target_market:` 全A股市场
- `reusable_objects_or_fields:` 24因子基础库（盈利/资产运营/偿债/规模/估值PE PB/技术换手率和动量反转/MACD等）、短样本策略（新因子筛选规则：相关性高+显著性高）、长样本策略（最大窗口5年）、PB优于PE的结论、超额收益被反转现象驱动而非动量的结论
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 沿用6月份全市场相关性选股策略，将因子池从12个扩充至24个（覆盖基本面/规模/估值/技术面）。短样本策略倾向于通过非基本面因子选股，近期表现优异（基本面因子贡献度随时间减弱）。长样本策略控制最大窗口5年，表现逊于短样本。关键发现：PB比PE更有效；超额收益多被反转现象驱动而非动量；换手率与收益负相关（换手越高收益越差）；09年后小盘股强于大盘股。
- `selection_style:` multi_factor

---

### 资料卡片 S-029

- `paper_id:` S-029
- `title:` 相关性选股策略——在房地产行业上的实证
- `group:` 量化选股
- `theme_tags:` 相关性选股、房地产行业、行业专用因子、资本结构
- `core_problem:` 将相关性选股策略应用于房地产行业，加入反映行业特点的专用指标
- `method_family:` stock_selection_rule
- `data_requirements:` 房地产行业个股财务数据、估值数据、技术指标数据、资本结构指标（流动比率/预收账款/营业收入等）、行业指数数据
- `time_granularity:` 月度
- `target_market:` 房地产行业
- `reusable_objects_or_fields:` 房地产行业专用因子库（剔除费用变量和成交量变化率，加入资本结构指标如流动比率/预收账款/营业收入）、短样本和长样本两种策略在房地产行业的表现对比
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 将相关性选股策略应用于房地产行业，加入了反映行业特点的专用指标（资本结构类指标如流动比率、预收账款/营业收入等）。长短样本策略均获得显著超额收益，短样本波动大但累计净值更高，长样本稳定但收益率较低。发现策略表现受市场风格影响——样本期前2年因子过多可能因市场风格复杂，风格清晰后超额收益显著。短样本选中指标：1/3/6个月反转、ROA、EPS、净利润率、每股净资产、流动比率、DIFF、换手率、PE、市值。
- `selection_style:` multi_factor

---

### 资料卡片 S-030

- `paper_id:` S-030
- `title:` 相关性选股策略——在纺织服装行业上的实证
- `group:` 量化选股
- `theme_tags:` 相关性选股、纺织服装行业、行业选股
- `core_problem:` 将相关性选股策略应用于纺织服装行业
- `method_family:` stock_selection_rule
- `data_requirements:` 纺织服装行业个股因子数据、行业指数数据
- `time_granularity:` 月度
- `target_market:` 纺织服装行业
- `reusable_objects_or_fields:` 纺织服装行业相关性选股模型参数（显著性水平要求、样本窗口长度24个月）
- `can_be_quantized_now:` no
- `current_role:` 仅来源库保留
- `one_paragraph_summary:` 将相关性选股策略应用于纺织服装行业，沿用与其他行业相同的选股模型框架。研究方法与前述行业实证一致：2003年12月至2010年12月数据，24个月滚动窗口，Pearson相关性检验筛选显著因子，样本外排序打分取TOP10%/20%。策略在纺织服装行业取得较好超额收益，但方法论与S-028/S-029高度重复。
- `selection_style:` multi_factor

---

### 资料卡片 S-031

- `paper_id:` S-031
- `title:` 相关性选股策略——在公用事业行业上的实证以及选股因子权重的再讨论
- `group:` 量化选股
- `theme_tags:` 相关性选股、公用事业行业、因子权重、大类指标平衡
- `core_problem:` 在公用事业行业验证相关性选股策略，并讨论不同因子权重设置方法对策略效果的影响
- `method_family:` stock_selection_rule
- `data_requirements:` 公用事业行业个股因子数据（25个因子分9大类）、行业指数数据
- `time_granularity:` 月度
- `target_market:` 公用事业行业
- `reusable_objects_or_fields:` 25因子9大类分类体系（盈利能力/偿债能力/估值/市值/动量/成长性/技术指标/换手率/资产运营）、因子权重平衡方法（大类指标等权重vs原始指标等权重对比）、无显著因子时两种处理方法（持有上期组合vs持有市场指数，前者优于后者）
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 在公用事业行业验证相关性选股策略，25个因子分9大类。探讨因子权重设置：大类指标等权重 vs 原始指标等权重。发现在5个已实证行业中，平衡各大类权重反而削弱了策略表现（原始等权重更优）。TOP10%组合累积净值达行业指数2.06倍。无显著因子时持有上期组合（方法一）优于持有市场指数（方法二）。2011年2月末短样本选股指标：总市值/流通市值/1月换手率/3月换手率。
- `selection_style:` multi_factor

---

### 资料卡片 S-032

- `paper_id:` S-032
- `title:` 相关性选股策略——在化学工业行业上的实证
- `group:` 量化选股
- `theme_tags:` 相关性选股、化学工业、行业选股
- `core_problem:` 将相关性选股策略应用于化学工业行业
- `method_family:` stock_selection_rule
- `data_requirements:` 化学工业行业个股因子数据、行业指数数据
- `time_granularity:` 月度
- `target_market:` 化学工业行业
- `reusable_objects_or_fields:` 化工行业相关性选股参数（显著性水平0.01、样本窗口24个月）、10只和20只股票组合对比结论
- `can_be_quantized_now:` no
- `current_role:` 仅来源库保留
- `one_paragraph_summary:` 将相关性选股策略应用于化学工业行业。2003年12月至2011年9月数据，24个月滚动窗口，显著性水平0.01。10只股票组合表现更好，最终净值为行业指数2.83倍，20只组合夏普值与10只不相上下但累积收益略低。等权重加权超额收益下降明显。9月末选股指标：Delta(ROA)/Delta(ROE)/Delta(净利率)/Delta(EPS)/主营收入增长率/资产负债率/1月换手率/MACD。方法论与S-028~S-031高度重复。
- `selection_style:` multi_factor

---

### 资料卡片 S-033

- `paper_id:` S-033
- `title:` 相关性选股策略——在有色金属行业上的实证
- `group:` 量化选股
- `theme_tags:` 相关性选股、有色金属行业、行业选股
- `core_problem:` 将相关性选股策略应用于有色金属行业
- `method_family:` stock_selection_rule
- `data_requirements:` 有色金属行业个股因子数据、行业指数数据
- `time_granularity:` 月度
- `target_market:` 有色金属行业
- `reusable_objects_or_fields:` 有色金属行业相关性选股模型
- `can_be_quantized_now:` no
- `current_role:` 仅来源库保留
- `one_paragraph_summary:` 将相关性选股策略应用于有色金属行业。方法论与前述行业实证完全一致：通过因子与股票超额收益历史相关性的度量筛选显著因子，在行业内选股。策略在有色金属行业获得较好超额收益。研究方法和因子池与全市场及其他行业实证高度一致，属于同一方法论的横向扩展。
- `selection_style:` multi_factor

---

### 资料卡片 S-034

- `paper_id:` S-034
- `title:` 行业内股票业绩弹性分析——在钢铁行业上的实证
- `group:` 量化选股
- `theme_tags:` 业绩弹性、钢铁行业、成本要素、产成品价格、弹性系数、选股增强
- `core_problem:` 分析行业内公司对于上下游各类成本、产成品价格波动的业绩弹性系数，为行业内选股提供新参考指标
- `method_family:` stock_selection_rule
- `data_requirements:` 钢铁行业个股主营业务构成数据、15种产成品价格数据、8大类成本要素价格数据（铁精粉/铁矿石运费等）、季度利润数据
- `time_granularity:` 月度（价格更新）/ 季度（利润验证）
- `target_market:` 钢铁行业
- `reusable_objects_or_fields:` 业绩弹性系数计算方法（产品价格变动→公司业绩变动的敏感度）、15种产成品+8大类成本要素因子库、弹性因子与传统因子（财务/估值/技术）结合框架、弹性极值应用（价格大幅波动时弹性选股能力充分体现）
- `can_be_quantized_now:` partial
- `current_role:` future bucket
- `one_paragraph_summary:` 针对钢铁行业，分析各公司对上下游成本/产成品价格波动的业绩弹性系数。汇总15种产成品、8大类成本要素，通过相关性确认产品相关输入成本和输出价格指标，主成分分析与回归分析结合提取弹性系数。弹性因子月度胜率65%、月度战胜均值0.85%。与传统因子结合后超额收益提升、最大回撤缩小50%以上（5只股票）、组合稳定性显著提升。2011年12月铁精粉/运费大幅下跌时组合胜率100%、超额收益2.42%。
- `selection_style:` financial_factor

---

### 资料卡片 S-035

- `paper_id:` S-035
- `title:` 行业内选股策略——钢铁行业
- `group:` 量化选股
- `theme_tags:` 行业内选股、钢铁行业、自上而下、强势弱势阶段、打分模型
- `core_problem:` 构建钢铁行业内的选股策略，区分行业强势和弱势阶段的不同显著指标
- `method_family:` stock_selection_rule
- `data_requirements:` 钢铁行业个股财务数据、估值数据、技术指标数据、行业指数数据
- `time_granularity:` 月度
- `target_market:` 钢铁行业
- `reusable_objects_or_fields:` 钢铁行业强势/弱势阶段划分方法、强势阶段显著指标（短期业绩变动/市场预测估值/反转特性）、弱势阶段显著指标（市净率/市销率为主，PE失效）、综合选股模型（市销率/预估PE/预估PB/6个月涨幅，样本内保留50%个股）
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 构建钢铁行业自上而下选股策略：回顾2006-2008年钢铁板块4个强势和弱势阶段，运用财务/情绪/技术指标对涨幅序列进行解释。强势阶段个股表现受短期业绩变动、市场预测估值和反转特性影响；弱势阶段市净率和市销率成为主要显著指标（"牛市看PE、熊市看PB"）。综合选股模型使用市销率、预估市盈率、预估市净率、6个月涨幅。样本外（2008.10-2009.12）50%样本内选股累计涨幅188%，同期钢铁指数107%，年化Sharp比率190%。
- `selection_style:` multi_factor

---

### 资料卡片 S-036

- `paper_id:` S-036
- `title:` 行业内选股策略——有色金属行业
- `group:` 量化选股
- `theme_tags:` 行业内选股、有色金属、强势弱势阶段、打分模型、重组预期
- `core_problem:` 构建有色金属行业内的选股策略，考虑行业市值偏小和重组预期影响
- `method_family:` stock_selection_rule
- `data_requirements:` 有色金属行业个股财务数据、估值数据、技术指标数据、行业指数数据
- `time_granularity:` 月度
- `target_market:` 有色金属行业
- `reusable_objects_or_fields:` 有色金属行业强势/弱势阶段显著指标、综合选股模型（下一年预估PE/预估PB/3个月涨幅，样本内保留50%个股）、重组预期对行业选股的影响分析
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 构建有色金属行业自上而下选股策略。有色金属市值偏小，个股表现受重组预期影响大（宏观经济上升周期中资源定价差异导致重组价值可能远大于现有业务价值）。卖方分析师保守预测完全不能反映重组预期，导致有重组预期和无重组预期公司业绩可比性弱。综合选股模型使用下一年预估PE、预估PB、3个月涨幅。样本外（2008.10-2010.2）50%选股累计涨幅296%，同期有色指数194%，年化Sharp比率66%。
- `selection_style:` multi_factor

---

### 资料卡片 S-037

- `paper_id:` S-037
- `title:` 选股因子研究系列（一）——弱者终有逆袭日，强势几无持续时——A股市场的动量反转效应研究
- `group:` 量化选股
- `theme_tags:` 动量、反转、因子研究、A股特征、月度效应、过度反应
- `core_problem:` 系统研究A股市场动量/反转效应的存在性和特征
- `method_family:` factor_research
- `data_requirements:` 个股月度收益率数据、市场指数收益率数据
- `time_granularity:` 月度
- `target_market:` 全A股市场
- `reusable_objects_or_fields:` A股反转效应强于动量的实证结论（弱者逆袭/强势不持续）、月度动量/反转规律（特定月份动量强/其他月份反转强）、动量反转因子构建方法
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 系统研究A股市场动量/反转效应。核心结论：A股市场反转效应显著强于动量效应——"弱者终有逆袭日，强势几无持续时"。股价对信息的过度反应或反应不足为历史收益率选股策略提供了操作空间。研究不同持有期/观察期参数下的动量和反转效果，发现A股市场在特定月份动量效应较强，其他多数月份反转效应占主导。该研究为动量/反转因子的参数设定提供了实证基础。
- `selection_style:` momentum

---

### 资料卡片 S-038

- `paper_id:` S-038
- `title:` 选股因子研究系列（二）——因子模型的尾部相关性研究
- `group:` 量化选股
- `theme_tags:` 尾部相关性、因子模型、极端事件、Hill估计、风险分散
- `core_problem:` 引入尾部相关系数度量个股与市场在极端价格变化时的趋同性
- `method_family:` risk_model
- `data_requirements:` 个股日度/5日/20日收益率数据、市场指数收益率数据
- `time_granularity:` 日度/5日/20日滚动窗口
- `target_market:` 沪深300成分股
- `reusable_objects_or_fields:` 尾部相关系数定义与估计方法（Hill估计）、因子模型框架下的尾部相关系数显式解、上下尾相关系数时间序列、极端下跌状态下低尾部相关性组合风险更小
- `can_be_quantized_now:` partial
- `current_role:` future bucket
- `one_paragraph_summary:` 引入尾部相关系数度量个股与市场在极端行情下的趋同性。在因子模型框架下，利用Hill估计获得尾部相关系数简洁表达式。数据模拟表明估计具备稳健有效性质。实证发现：大部分沪深300样本股与市场尾部相关系数较高；Beta类似的个股在尾部行为上风格迥异；极端下跌状态下低尾部相关性组合风险几乎一致小于高尾部相关性组合，夏普比率和最大回撤表现更优。
- `selection_style:` unknown

---

### 资料卡片 S-039

- `paper_id:` S-039
- `title:` 选股因子研究系列（三）——从Spearman相关系数出发研究因子有效性——Kalman Filter模型在因子选择中的应用
- `group:` 量化选股
- `theme_tags:` Spearman相关系数、Kalman Filter、因子选择、动态跟踪、时变有效性
- `core_problem:` 如何动态跟踪因子有效性的时变特征，及时把握市场风格变化
- `method_family:` factor_research
- `data_requirements:` 沪深300成分股月度因子数据、月度收益率数据
- `time_granularity:` 月度
- `target_market:` 沪深300成分股
- `reusable_objects_or_fields:` 截面Spearman相关系数（度量因子与收益的相关关系）、马尔科夫链Kalman Filter模型（动态跟踪因子有效性时变序列）、p值选取法对比基准、因子有效性动态跟踪框架
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 以截面Spearman相关系数描述因子与股票收益的相关关系，用马尔科夫链Kalman Filter模型对因子Spearman相关系数时间序列建模，动态跟踪因子有效性变化。解决传统方法痛点：短历史数据噪音多/长历史数据滞后性。Kalman Filter通过状态空间模型平衡估计精度和时效性。实证表明该模型比传统p值选取法更能及时捕捉因子有效性变化，基于该模型的股票组合历史表现优于p值选取法。
- `selection_style:` multi_factor

---

### 资料卡片 S-040

- `paper_id:` S-040
- `title:` 选股因子研究系列（四）——多因子选股模型的有效与失效
- `group:` 量化选股
- `theme_tags:` 因子有效性、强弱指数、尾部相关、线性相关、分组检验
- `core_problem:` 探索因子对收益率的预测能力与表现形态，解决传统线性统计方法筛选因子的困境
- `method_family:` factor_research
- `data_requirements:` 沪深300成分股月度因子数据（28个常用因子）、月度收益率数据
- `time_granularity:` 月度
- `target_market:` 沪深300成分股
- `reusable_objects_or_fields:` 因子有效性强弱指数（最大平均收益出现在因子极端值区间的概率）、10组分组检验方法、尾部相关系数vs线性相关系数对比、因子有效性动态评估框架
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `one_paragraph_summary:` 传统线性相关系数很难有效筛选对收益率有较强鉴别能力的因子（28个因子中仅少数相关系数>0.1）。提出因子有效性强弱指数：按因子大小分10组，统计最大平均收益出现在极端值组别的概率。实证发现平均收益率最高的组合更易出现在因子取值的两端（最大/最小组别），概率显著高于其他组。尾部相关系数具有不同于线性相关性的独特信息，是评估因子有效性的补充工具。
- `selection_style:` multi_factor

---

### 资料卡片 S-041

- `paper_id:` S-041
- `title:` 选股因子研究系列（五）——寻找股价驱动新因子之净换手率
- `group:` 量化选股
- `theme_tags:` 净换手率、新因子、Level-2数据、主动买卖单、多空力量
- `core_problem:` 从上交所Level-2逐笔成交数据中提炼"净换手率"新因子，跟踪市场多空力量对比
- `method_family:` factor_research
- `data_requirements:` 上交所Level-2逐笔成交数据（主动买卖单判别）、个股日度换手率数据、收益率数据
- `time_granularity:` 日度
- `target_market:` 上交所上市股票
- `reusable_objects_or_fields:` 净换手率定义（基于主动买卖单的方向性换手率）、主动买卖单判别方法（从市场微观角度结合量价信息反推投资者买卖偏好）、净换手率因子选股效果
- `can_be_quantized_now:` partial
- `current_role:` 可重开
- `one_paragraph_summary:` 传统成交量和换手率是绝对值、不带方向性。从上交所Level-2逐笔成交数据出发，结合量价信息反推投资者买卖偏好，构建"净换手率"指标（带方向性的换手率）跟踪市场多空力量对比。净换手率能识别分批逐步建仓的隐藏性买单，相比传统换手率具有增量信息价值。实证表明净换手率作为新因子在选股中具有显著有效性，可纳入多因子选股模型作为补充因子。
- `selection_style:` multi_factor

---

## 4. 本组可重开候选清单 (Part 2 补充)

---

### 候选 S-C04

- `candidate_id:` S-C04
- `candidate_name:` 相关性选股策略全市场框架（含6个行业实证）
- `from_paper:` S-028 ~ S-033
- `why_it_matters:` 提供了一套从因子库构建→滚动相关性筛选→打分→组合形成的完整选股流水线，24因子覆盖基本面/估值/技术/市值多维度，已验证6个行业的适用性，是量化选股的核心基础设施
- `minimum_input:` 个股月度因子数据（24个因子）、月度收益率数据、行业分类数据
- `minimum_output:` 每期有效因子列表、个股综合得分排名、TOP10%/20%组合、超额收益统计
- `current_role:` 可重开

### 候选 S-C05

- `candidate_id:` S-C05
- `candidate_name:` 事件驱动策略组合（业绩预告+高送转+定增+股权激励+增减持）
- `from_paper:` S-016~S-018 / S-022 / S-023 / S-026
- `why_it_matters:` 事件驱动策略来源多样、信号互补、与量价因子低相关，是组合 diversification 的重要来源。各子策略均有明确的事件时间窗口和超额收益统计
- `minimum_input:` 上市公司事件公告数据（业绩预告/高送转/定增/股权激励/增减持）、股票日度收益率数据
- `minimum_output:` 各事件类型信号列表、事件窗口超额收益、组合持仓、止损触发条件（参考S-024）
- `current_role:` 可重开

### 候选 S-C06

- `candidate_id:` S-C06
- `candidate_name:` Kalman Filter动态因子选择模型
- `from_paper:` S-039
- `why_it_matters:` 市场风格不断变化，传统静态因子筛选无法及时适应。Kalman Filter通过状态空间模型动态跟踪因子有效性，比p值法更能及时捕捉因子有效性变化，是多因子模型的"智能开关"
- `minimum_input:` 沪深300成分股月度因子数据、月度收益率数据
- `minimum_output:` 各因子Spearman相关系数时间序列、Kalman Filter估计的因子有效性状态、每期有效因子列表、基于动态因子的组合收益
- `current_role:` 可重开

---

## 5. future bucket 清单 (Part 2 补充)

---

- `item:` 事件驱动组合止损机制设计（S-024）
- `why_future_only:` 需要具体的事件驱动策略组合作为应用对象，止损触发条件（策略间相关性异常+风格指数走弱）需要配合实际组合验证，单独实施价值有限

- `item:` 钢铁行业业绩弹性因子向其他行业的推广
- `why_future_only:` 钢铁行业弹性分析依赖于15种产成品和8大类成本要素的价格数据，其他行业的产品结构和成本要素完全不同，需逐个行业重新构建弹性分析框架

- `item:` 尾部相关系数在组合风险管理中的应用
- `why_future_only:` S-003和S-038提供了尾部相关系数的计算方法，但将其融入日常组合风险管理需要完整的系统支持和大量计算资源，与当前框架不匹配

- `item:` 净换手率因子的全市场推广
- `why_future_only:` 净换手率依赖上交所Level-2逐笔数据，数据获取成本高，且目前仅验证了上交所股票，深交所股票需单独验证

---

## 6. 仅来源库保留清单 (Part 2 补充)

---

- `paper_id:` S-030 / S-032 / S-033
- `title:` 相关性选股策略——纺织服装/化学工业/有色金属行业实证
- `reason:` 与S-028（全市场改进）和S-029（房地产）方法论高度重复，均为同一方法的横向行业扩展，因子池和选股流程完全一致。保留S-028和S-029作为代表即可

- `paper_id:` S-034
- `title:` 行业内股票业绩弹性分析——在钢铁行业上的实证
- `reason:` 依赖大量行业专用价格数据（15种产成品+8类成本要素），向其他行业推广成本高，更适合作为行业研究模块而非通用选股框架

- `paper_id:` S-035 / S-036
- `title:` 行业内选股策略——钢铁行业/有色金属行业
- `reason:` 方法论与S-028~S-033的相关性选股策略存在重叠，但更侧重行业内自上而下的风格判断（强势/弱势阶段）。策略对单个行业的依赖性强，向其他行业复制的成本高

- `paper_id:` S-038
- `title:` 选股因子研究系列（二）——因子模型的尾部相关性研究
- `reason:` 尾部相关系数计算复杂（需Hill估计、厚尾分布假设），更偏风险管理研究而非选股策略，实际应用的系统支持要求高

---

## 7. 本组去重与合并建议

---

- **方法论完全一致（相关性选股系列）：** S-028（全市场改进）→ S-029（房地产）→ S-030（纺织服装）→ S-031（公用事业）→ S-032（化学工业）→ S-033（有色金属）六份报告方法论完全一致（因子池→Pearson相关性检验→滚动窗口→打分→组合），仅目标行业不同。可合并为"相关性选股策略"一个来源主题，保留S-028作为核心参考（因子最全、方法改进最完整），S-031作为因子权重讨论的补充
- **方法论完全一致（行业内选股系列）：** S-035（钢铁）和S-036（有色金属）方法论一致（行业强弱势阶段划分→单因素回归→综合打分模型），仅目标行业不同。可合并为"行业内选股策略"一个来源主题
- **事件驱动策略系列可合并为子主题：**
  - 业绩预告子主题：S-016（扭亏预减）+ S-017（主板预减+中小板盈利）
  - 股权激励子主题：S-021（首次实施收益）+ S-023（全周期窗口期）
  - 其他独立事件：S-018（指数调整）、S-020（大股东增减持）、S-022（高送转）、S-025（股东持股结构）、S-026（定增）
- **因子研究系列相互独立但可互补：** S-037（动量反转）+ S-039（Kalman Filter动态跟踪）+ S-040（因子有效与失效）+ S-041（净换手率新因子）四份报告从不同角度研究因子，可合并为"因子研究方法论"主题
- **S-003与S-038内容关联：** S-003（沪深300尾部相关性观察）和S-038（因子模型尾部相关性研究）均涉及尾部相关性，但S-003更偏实证观察，S-038更偏理论模型，可相互参照

---

## 8. 对项目的最终建议

---

- **最值得保留的方向：**
  1. 优先重开 S-C04（相关性选股全市场框架）——方法论最完整、因子覆盖最广、已在6个行业验证，是量化选股的核心基础设施。仅需月度因子数据即可运行
  2. 同步推进 S-C05（事件驱动策略组合）——与量价因子低相关，来源多样（业绩预告/高送转/定增/股权激励/增减持），是组合 diversification 的关键模块
  3. 关注 S-C06（Kalman Filter动态因子选择）——解决因子失效问题的"智能开关"，可作为相关性选股框架的因子筛选层升级
- **最不值得继续深切的内容：**
  1. 行业专用选股策略系列（S-030/S-032/S-033/S-035/S-036等）——方法论重复，对其他行业可复制性差
  2. 尾部相关性风险管理（S-003/S-038）——计算复杂度高，与当前选股框架匹配度低
  3. 业绩弹性分析（S-034）——数据门槛极高（需行业专用价格数据），推广成本高
- **下一步行动：**
  1. 先用最新数据（2020-2025）复现S-028的相关性选股框架，验证24因子在当前市场的有效性，特别关注基本面因子是否仍然有效（原始报告指出09年后基本面因子贡献减弱）
  2. 同步整理事件驱动数据源（业绩预告/高送转/定增/股权激励/增减持公告），建立事件日历和信号触发机制
  3. 评估Kalman Filter模块的开发成本，决定是作为一期还是二期功能实现
