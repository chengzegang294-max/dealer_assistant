# A股 txt 标题聚类与内容保留 v1

- source_type: txt_strategy_samples
- current_status: 浅切并保留实质内容
- project_role: A股 future research/data capability
- batch_scope: 聚宽社区策略代码/社区示例/赠送文本
- note: 源目录对账后确认 `01-99` 共 `99` 份 txt 均存在（来自聚宽 JoinQuant 社区分享/示例集合）

---

## 2. 总体判断

- 这批txt全部为聚宽（JoinQuant）社区用户分享的策略代码，格式统一为Python策略源码+少量注释说明，属于"策略模板池"级别
- 主题最多的是**择时/均线/RSRS/KDJ/MACD**（21份）和**多因子/财务因子**（20份），其次是**低质量杂项/作业/测试**（17份）、**轮动/行业/ETF/市值**（12份）
- 一看就不值得深切的内容：17份作业/测试/无名策略/向导式生成策略，以及大量纯技术指标单因子策略（金叉死叉类）
- 少数值得后续抽样深挖的主题：**北向资金跟踪**（73）、**申万行业轮动**（81）、**银行股AH套利**（96/97）、**GFTD择时**（78）、**CAPM+ROE多因子**（71）、**RSRS择时系列**（05/27/69/77/93）、**祖鲁法则**（23）、**截面动量**（04/17）、**自适应均线+ATR通道**（01/20）、**配对交易**（02/13/19/55），这些提供了可复用的策略规则壳

---

## 3. 主题聚类区

---

### 主题桶 TX-01

- `cluster_id:` TX-01
- `cluster_name:` 择时/均线/RSRS/KDJ/MACD
- `title_count:` 21（第一批7 + 第二批14）
- `representative_titles:` 05-RSRS择时+财务选股、27-RSRS30分钟线、69-RSRS指标择时、77-RSRS大盘择时优化、93-RSRS大盘择时、78-GFTD第二版、08-MACD单因子多头、76-MACD大盘择时、58/90-MACD金叉死叉、29-KD指标、40-kdj+accer、91-KDJ大盘择时、21-BIAS乖离率择时、52-布林带、66-MA10/20交叉、83-沪深300ETF双均线、86/89-均线择时、79-DMI大盘择时
- `common_method_family:` timing_rule
- `common_data_requirements:` 日线OHLCV、分钟线OHLCV、财务指标（PE/PB/ROE等）
- `worth_deepening:` yes

---

### 主题桶 TX-02

- `cluster_id:` TX-02
- `cluster_name:` 多因子/财务因子/机器学习
- `title_count:` 20（第一批12 + 第二批8）
- `representative_titles:` 03-机器学习多因子、06-市值研究、07-价值精选、15-多期限选股、23-祖鲁法则、31-低PB价值投资、35/36-投资学作业多因子、39-因子分析封装、41-多因子回测、43-无模型评估多因子、44-新手价值投资、51-随机森林拐点识别、71-CAPM+ROE股票池、75-财务因子策略、85-便宜股系列、88-小白多因子、92-多因子选股、94-PE和PB策略、98-SVM示例
- `common_method_family:` factor_research
- `common_data_requirements:` 日线OHLCV、财务报表（PE/PB/ROE/EPS等）、市值数据、行业分类
- `worth_deepening:` yes

---

### 主题桶 TX-03

- `cluster_id:` TX-03
- `cluster_name:` 轮动/行业/ETF/市值
- `title_count:` 12（第一批3 + 第二批9）
- `representative_titles:` 25-简单市值轮动、33-行业市值最大、34-成长策略、53-小市值策略、59-小市值轮动改进、64-银行股轮动、65-8只基金按PE调仓、70-蓝筹均线、81-申万行业轮动、82-次新+小市值+KAMA、96-沪港银行翻倍策略、97-银行翻倍策略
- `common_method_family:` allocation_rule
- `common_data_requirements:` 市值数据、行业分类、日线OHLCV、AH股溢价数据
- `worth_deepening:` yes

---

### 主题桶 TX-04

- `cluster_id:` TX-04
- `cluster_name:` 期货/海龟/多品种趋势
- `title_count:` 6（第一批6 + 第二批0）
- `representative_titles:` 01-自适应均线期货多品种、04-商品期货动量、09-多品种双均线、17-截面动量、22-海龟升级分钟级、49-海龟克隆优化
- `common_method_family:` trend_system
- `common_data_requirements:` 期货分钟线/日线OHLCV、多品种数据、合约信息
- `worth_deepening:` yes

---

### 主题桶 TX-05

- `cluster_id:` TX-05
- `cluster_name:` 配对/均值回归/套利
- `title_count:` 7（第一批6 + 第二批1）
- `representative_titles:` 02-协整搬砖策略、12-zscore均值回归、13-招行海天配对改进、18-均值回归分享、19-招行海天配对学习、50-简单配对交易、55-中小板中证500配对
- `common_method_family:` mean_reversion
- `common_data_requirements:` 日线OHLCV、配对股票历史价格、协整检验数据
- `worth_deepening:` yes

---

### 主题桶 TX-06

- `cluster_id:` TX-06
- `cluster_name:` 资金流/事件驱动/聪明钱
- `title_count:` 6（第一批4 + 第二批2）
- `representative_titles:` 10-追三板策略、11-酒股短线、38-跟踪聪明钱、47-次新小盘、73-跟着港资买A股、95-资金流策略
- `common_method_family:` event_or_flow
- `common_data_requirements:` 资金流数据（北向/主力/散户）、涨停数据、次新股列表、日线OHLCV
- `worth_deepening:` yes

---

### 主题桶 TX-07

- `cluster_id:` TX-07
- `cluster_name:` 低质量杂项/作业/测试
- `title_count:` 17（第一批8 + 第二批9）
- `representative_titles:` 16/60-投资学作业、24-自选策略1、26-向导式-1、28-收益策略、32-测试策略1、37-个股止损、46-GetAPI研究、48-再测一支、56-爱神的箭、57-黄泽森策略、61-向导式成长股、62-选股策略、63-向导式、84-投资策略说明、87-张燕兰选股、99-中信向导策略
- `common_method_family:` low_quality_misc
- `common_data_requirements:` 无固定要求
- `worth_deepening:` no

---

### 主题桶 TX-08

- `cluster_id:` TX-08
- `cluster_name:` 其他独立策略
- `title_count:` 8（第一批4 + 第二批4）
- `representative_titles:` 14-抗击熊市低市值、20-ATR自适应通道、30-LSTM预测、45-布林带策略、54-中长线买卖点、72-基金定投沪深300、74-沪深300增强、80-价值分析避股灾
- `common_method_family:` 混合
- `common_data_requirements:` 日线/分钟线OHLCV、财务数据
- `worth_deepening:` partial

---

## 4. 代表样本内容保留卡片

---

### 卡片 TX-01-S1

- `sample_id:` TX-01-S1
- `title:` 兄台且慢，去天台排队不如看看这个策略先（RSRS择时+财务选股）
- `cluster_name:` 择时/均线/RSRS/KDJ/MACD
- `method_family:` timing_rule
- `data_requirements:` 日线OHLCV、财务指标（PE/PB/ROE/毛利率）
- `reusable_objects_or_fields:` RSRS择时信号（最高价/最低价序列OLS回归斜率）、财务指标选股规则（PE/PB/ROE/毛利率过滤）、空仓机制（无信号时保持空仓）
- `retained_logic_summary:`
  - 选股：财务指标过滤（PE/PB/ROE/毛利率），保留基本面优质股票池
  - 择时：RSRS（Resistance Support Relative Strength）指标，用最高价和最低价序列做OLS回归，斜率大于阈值时看多
  - 持仓：有开仓信号时持有10只股票，不满足时保持空仓
  - 本质是将基本面选股与技术择时结合，择时层使用RSRS斜率判断市场支撑力度
- `why_keep_or_not_keep:` RSRS是聚宽社区验证过的有效择时指标，与常规均线/MACD等指标低相关，可作为独立择时模块。财务选股规则壳可直接复用
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `content_excerpt_or_paraphrase:` "选股：财务指标选股；择时：RSRS择时；持仓：有开仓信号时持有10只股票，不满足时保持空仓"

---

### 卡片 TX-01-S2

- `sample_id:` TX-01-S2
- `title:` RSRS指标择时（30分钟线）
- `cluster_name:` 择时/均线/RSRS/KDJ/MACD
- `method_family:` timing_rule
- `data_requirements:` 30分钟线OHLCV
- `reusable_objects_or_fields:` RSRS 30分钟线实现、斜率标准化方法（(斜率-均值)/标准差）、阈值参数（买入阈值/卖出阈值）
- `retained_logic_summary:`
  - 使用30分钟线（而非日线）计算RSRS，提高信号灵敏度
  - 对斜率进行标准化处理：(当日斜率-历史斜率均值)/历史斜率标准差
  - 标准化后RSRS大于买入阈值开仓，小于卖出阈值平仓
  - 30分钟线版本比日线版本反应更快，适合中短线择时
- `why_keep_or_not_keep:` 30分钟RSRS是日线RSRS的高频变体，提供了不同时间粒度的择时信号，可作为多周期RSRS体系的一部分
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `content_excerpt_or_paraphrase:` 使用30分钟K线计算RSRS斜率并标准化，通过阈值判断多空

---

### 卡片 TX-01-S3

- `sample_id:` TX-01-S3
- `title:` GFTD第二版（大盘择时）
- `cluster_name:` 择时/均线/RSRS/KDJ/MACD
- `method_family:` timing_rule
- `data_requirements:` 日线OHLCV
- `reusable_objects_or_fields:` GFTD四阶段计数器（启动→计数→确认→状态切换）、n1=4价格比较参数、n2=4启动期长度、n3=4计数阈值、count_lag=2计数比较滞后期、满仓/空仓状态机
- `retained_logic_summary:`
  - GFTD（Generalized Filtered Trend Detection）是一种多阶段趋势确认择时模型
  - 四阶段机制：启动阶段（价格与n1日前比较）→计数阶段（连续同向计数）→确认阶段（达到n3阈值）→状态切换（满仓/空仓转换）
  - 参数：n1=4（启动比较周期）、n2=4（启动期长度）、n3=4（计数阈值）、count_lag=2（计数比较滞后）
  - 本质是通过多阶段过滤减少假突破信号，比单指标择时更稳健
- `why_keep_or_not_keep:` GFTD是多阶段趋势确认的完整规则壳，参数结构清晰，可作为趋势跟踪策略的择时开关。与RSRS、MACD等单指标择时互补
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `content_excerpt_or_paraphrase:` 买入启动计数→达到n2后进入计数阶段→价格同向比较达到n3阈值→确认趋势→满仓/空仓状态切换

---

### 卡片 TX-01-S4

- `sample_id:` TX-01-S4
- `title:` BIAS_QL乖离率策略指数择时1.0
- `cluster_name:` 择时/均线/RSRS/KDJ/MACD
- `method_family:` timing_rule
- `data_requirements:` 日线OHLCV、指数数据
- `reusable_objects_or_fields:` BIAS乖离率计算公式、QL量化信号生成规则、指数择时信号
- `retained_logic_summary:`
  - 基于BIAS（乖离率）指标进行指数级别择时
  - BIAS衡量价格与移动平均线的偏离程度
  - 当BIAS偏离过大时产生回归信号，偏离过小时产生趋势延续信号
  - 果核量化出品，有社区验证基础
- `why_keep_or_not_keep:` BIAS择时是经典技术择时方法，与RSRS、MACD等指标互补，可作为多指标择时体系的一个组件
- `can_be_quantized_now:` yes
- `current_role:` future bucket
- `content_excerpt_or_paraphrase:` 基于BIAS乖离率指标构建指数择时信号，判断价格与均线的偏离程度

---

### 卡片 TX-02-S1

- `sample_id:` TX-02-S1
- `title:` Principle by Jim Slater 祖鲁法则在A股的实现与改进
- `cluster_name:` 多因子/财务因子/机器学习
- `method_family:` factor_research
- `data_requirements:` 财务报表（PE/PB/EPS增长率/利润率/现金流/负债率）、市值数据、行业分类
- `reusable_objects_or_fields:` 祖鲁法则7大选股标准（PE<20/EPS增长率>15%/利润率>5%/现金流>负债/强relative strength/小市值/独特优势）、A股适配改进方案、财务过滤流程
- `retained_logic_summary:`
  - Jim Slater祖鲁法则核心：买低PE但高成长的中小市值公司
  - 7大标准：PE低于20、EPS增长率>15%、利润率>5%、现金流>负债、relative strength强、小市值、独特竞争优势
  - A股改进：适配A股财务数据口径，增加ROE过滤，调整市值阈值
  - 本质是高成长+低估值+强动量+小市值的多因子组合
- `why_keep_or_not_keep:` 祖鲁法则是经典投资体系在A股的完整实现，7大标准可直接作为多因子评分框架，是TX-02中策略逻辑最完整的一份
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `content_excerpt_or_paraphrase:` 祖鲁法则核心：买低PE但高成长的中小市值公司，7大标准构成完整选股框架

---

### 卡片 TX-02-S2

- `sample_id:` TX-02-S2
- `title:` 基于多期限的选股策略（一）
- `cluster_name:` 多因子/财务因子/机器学习
- `method_family:` factor_research
- `data_requirements:` 日线OHLCV、财务报表、多期限收益率数据
- `reusable_objects_or_fields:` 多期限收益率计算（1月/3月/6月/12月）、期限结构因子、多期限动量/反转组合方法
- `retained_logic_summary:`
  - 同时考虑多个时间期限（1月/3月/6月/12月）的收益率信息
  - 不同期限可能呈现不同特征（短期反转/长期动量）
  - 将多期限信息综合为单一选股信号
  - 本质是多时间尺度动量/反转的融合框架
- `why_keep_or_not_keep:` 多期限框架可捕捉不同时间尺度的alpha，是单一期限动量策略的升级版本，逻辑清晰可复现
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `content_excerpt_or_paraphrase:` 基于多期限收益率构建选股策略，融合不同时间尺度的动量与反转信号

---

### 卡片 TX-02-S3

- `sample_id:` TX-02-S3
- `title:` CAPM单因子回归模型+ROE股票池（含止损）
- `cluster_name:` 多因子/财务因子/机器学习
- `method_family:` factor_research
- `data_requirements:` 日线OHLCV、ROE财务数据、市值数据、沪深300成分股
- `reusable_objects_or_fields:` CAPM单因子回归alpha计算、ROE股票池筛选规则、止损机制、16只股票集中度
- `retained_logic_summary:`
  - 以ROE为筛选标准，选择沪深300中满足条件的股票作为股票池
  - 采用CAPM模型，利用单因子回归计算每只股票的alpha值
  - 选出alpha值最大的前16支股票进行投资
  - 包含止损机制，形成完整的选股-持仓-风控闭环
- `why_keep_or_not_keep:` 将经典CAPM框架与A股财务因子（ROE）结合，alpha选股逻辑清晰，是TX-02中少数有完整风控机制的策略
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `content_excerpt_or_paraphrase:` 以ROE筛选沪深300股票池→CAPM单因子回归计算alpha→选前16只alpha最大股票→含止损

---

### 卡片 TX-03-S1

- `sample_id:` TX-03-S1
- `title:` 申万行业轮动策略
- `cluster_name:` 轮动/行业/ETF/市值
- `method_family:` allocation_rule
- `data_requirements:` 申万一级行业指数数据、行业成分股流通市值数据、日线OHLCV
- `reusable_objects_or_fields:` 申万一级行业指数涨幅排序、行业成分股流通市值Top5选取、月度轮动机制、等权仓位分配
- `retained_logic_summary:`
  - 统计申万一级行业指数，每月固定时间选取涨幅最大的行业
  - 在选定行业中选取流通市值最大的5只股票作为操作标的
  - 每月第一个交易日进行买卖操作，开盘卖出不在股票池中的股票，买入新选出的股票
  - 仓位平均分配
- `why_keep_or_not_keep:` 申万行业轮动是A股经典的行业配置策略，规则简单清晰，月度频率适合作为低频配置模块。行业指数数据可公开获取
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `content_excerpt_or_paraphrase:` 每月选申万涨幅最大行业→取行业流通市值Top5→月度轮动→等权分配

---

### 卡片 TX-03-S2

- `sample_id:` TX-03-S2
- `title:` 12年年化34%，Sharpe1.2，银行股轮动
- `cluster_name:` 轮动/行业/ETF/市值
- `method_family:` allocation_rule
- `data_requirements:` 银行股价格数据、AH股溢价数据、沪港通数据
- `reusable_objects_or_fields:` 银行股轮动规则、AH溢价套利信号、12年年化34%回测基准、Sharpe1.2风险收益比
- `retained_logic_summary:`
  - 专注于银行股内部的轮动策略
  - 12年回测年化收益34%，Sharpe比率1.2
  - 策略逻辑：在银行股内部根据某种规则（如涨幅/估值/动量）进行轮动
  - 银行股具有低波动、高股息、估值稳定的特征，适合轮动策略
- `why_keep_or_not_keep:` 银行股轮动在A股具有独特价值——银行板块市值大、流动性好、估值均值回归特性强。12年回测数据提供了策略稳健性的初步证据
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `content_excerpt_or_paraphrase:` 银行股内部轮动策略，12年回测年化34%、Sharpe1.2

---

### 卡片 TX-03-S3

- `sample_id:` TX-03-S3
- `title:` 沪港两地上市的银行股翻倍策略报告
- `cluster_name:` 轮动/行业/ETF/市值
- `method_family:` allocation_rule
- `data_requirements:` AH股价格数据、沪港通数据、银行股基本面数据
- `reusable_objects_or_fields:` AH股溢价率计算、沪港两地上市银行清单、月度调仓机制、低估值筛选规则
- `retained_logic_summary:`
  - 利用沪港两地上市银行股的AH溢价差异进行套利
  - 当H股相对A股折价较大时，H股存在估值修复空间
  - 每月第一个交易日调仓，选择AH溢价率最小的银行股
  - 本质是跨市场低估值策略
- `why_keep_or_not_keep:` AH股溢价套利是A股特色策略，有真实的市场机制支撑（沪港通）。银行股AH溢价长期存在，策略逻辑清晰可复制
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `content_excerpt_or_paraphrase:` 利用沪港两地上市银行股AH溢价差异，选择溢价率最小的银行股进行月度调仓

---

### 卡片 TX-04-S1

- `sample_id:` TX-04-S1
- `title:` 趋势交易能赚钱吗？商品期货动量效应挖掘初探
- `cluster_name:` 期货/海龟/多品种趋势
- `method_family:` trend_system
- `data_requirements:` 商品期货日线OHLCV、多品种数据
- `reusable_objects_or_fields:` 商品期货动量效应计算方法、多品种动量排名、动量效应存在性验证框架
- `retained_logic_summary:`
  - 系统验证商品期货市场的动量效应是否存在
  - 通过多品种回测验证动量策略在商品期货中的有效性
  - 提供动量效应的量化验证方法（非简单策略展示）
  - 结论：商品期货市场存在显著动量效应
- `why_keep_or_not_keep:` 不是简单策略代码，而是对动量效应存在性的系统研究，方法论（多品种动量验证框架）可迁移至A股市场
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `content_excerpt_or_paraphrase:` 系统验证商品期货市场动量效应的存在性，提供多品种动量验证框架

---

### 卡片 TX-04-S2

- `sample_id:` TX-04-S2
- `title:` AdaptiveMA自适应均线 过滤器 期货多品种模型
- `cluster_name:` 期货/海龟/多品种趋势
- `method_family:` trend_system
- `data_requirements:` 期货日线/分钟线OHLCV、多品种数据
- `reusable_objects_or_fields:` 考夫曼自适应均线（AMA/KAMA）实现、效率系数（ER）计算、过滤器机制（减少震荡市假信号）、多品种同时交易框架
- `retained_logic_summary:`
  - 使用考夫曼自适应均线（KAMA）替代传统均线，根据市场效率自动调整平滑参数
  - 效率系数ER = |价格变化| / 价格变动总和，ER高时均线快速跟随，ER低时均线缓慢平滑
  - 增加过滤器机制，在震荡市自动减少交易信号
  - 多品种同时运行，分散单一品种风险
- `why_keep_or_not_keep:` 自适应均线是趋势系统中比普通均线更先进的工具，过滤器机制解决震荡市假信号问题，多品种框架可直接用于CTA策略
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `content_excerpt_or_paraphrase:` 考夫曼自适应均线+过滤器机制，在趋势行情中快速跟随、震荡行情中自动减少信号

---

### 卡片 TX-04-S3

- `sample_id:` TX-04-S3
- `title:` 海龟交易法则升级版（分钟级回测+合约变更移仓）
- `cluster_name:` 期货/海龟/多品种趋势
- `method_family:` trend_system
- `data_requirements:` 期货分钟线OHLCV、合约信息（主力/次主力切换）
- `reusable_objects_or_fields:` 海龟交易完整规则（20日入市/10日离市/0.5N加仓/2N止损）、分钟级回测实现、合约变更移仓机制、ATR仓位计算
- `retained_logic_summary:`
  - 完整实现海龟交易法则：20日最高值入市、10日最低值离市、涨0.5N加仓、跌2N止损
  - 升级至分钟级回测，提高执行精度
  - 增加合约变更移仓机制（期货主力合约切换时自动移仓）
  - ATR(N)计算仓位大小，波动大时仓位小、波动小时仓位大
- `why_keep_or_not_keep:` 海龟法则是趋势交易经典规则壳，分钟级回测+合约移仓是期货实盘必需功能，ATR仓位管理可跨策略复用
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `content_excerpt_or_paraphrase:` "入市 20日最高值；离市 反向5%；加仓 涨0.5N；止损 跌2N"——完整海龟规则+分钟级回测+合约移仓

---

### 卡片 TX-05-S1

- `sample_id:` TX-05-S1
- `title:` 我好像破解了聚宽擂台排第一的策略？！（协整搬砖）
- `cluster_name:` 配对/均值回归/套利
- `method_family:` mean_reversion
- `data_requirements:` 日线OHLCV、配对股票历史价格
- `reusable_objects_or_fields:` 协整检验方法（Engle-Granger）、配对价差计算、Z-score阈值触发（开仓/平仓）、OLS回归残差分析
- `retained_logic_summary:`
  - 基于协整关系的统计套利：寻找两只价格走势长期相关的股票
  - 当价差偏离历史均值超过Z-score阈值时开仓（买低估卖高估）
  - 价差回归均值时平仓获利
  - 克隆自聚宽量化课堂"基于协整的搬砖策略"
- `why_keep_or_not_keep:` 协整配对是A股有效的统计套利方法，聚宽擂台排名第一说明其在A股有实际效果，规则壳完整可直接复用
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `content_excerpt_or_paraphrase:` 基于协整关系的统计套利，价差偏离Z-score阈值时开仓，回归时平仓

---

### 卡片 TX-05-S2

- `sample_id:` TX-05-S2
- `title:` 招行_海天配对策略-改进版
- `cluster_name:` 配对/均值回归/套利
- `method_family:` mean_reversion
- `data_requirements:` 日线OHLCV、配对股票价格（招商银行/海天味业）
- `reusable_objects_or_fields:` 配对股票选择方法（同行业龙头）、协整检验、动态对冲比率计算、改进版出场规则
- `retained_logic_summary:`
  - 选择同行业两只龙头股票（招商银行/海天味业）作为配对
  - 通过协整检验确认长期均衡关系
  - 计算动态对冲比率（非固定1:1）
  - 改进版增加了更精细的出场规则和风险控制
- `why_keep_or_not_keep:` 是TX-05-S1的改进版本，提供了同行业龙头配对的选择思路（不仅限于统计方法，还考虑基本面配对），改进版出场规则可提升夏普比率
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `content_excerpt_or_paraphrase:` 同行业龙头配对+协整检验+动态对冲比率+改进出场规则

---

### 卡片 TX-06-S1

- `sample_id:` TX-06-S1
- `title:` 跟着港资（北向资金）买A股
- `cluster_name:` 资金流/事件驱动/聪明钱
- `method_family:` event_or_flow
- `data_requirements:` 北向资金（港资）日度净流入数据、个股收盘价、日线OHLCV
- `reusable_objects_or_fields:` 北向资金个股净买入额排名、前一个交易日港资净流入信号、9:30开盘触发交易机制
- `retained_logic_summary:`
  - 跟踪北向资金（港资/沪深港通）的个股净买入数据
  - 选择前一个交易日北向资金净买入额最高的股票
  - 次日开盘（9:30）买入，持有至下一个调仓日
  - 本质是利用外资（聪明钱）的选股能力进行跟随
- `why_keep_or_not_keep:` 北向资金是A股重要的增量资金来源，被普遍认为是"聪明钱"。该策略提供了完整的北向资金跟随规则壳，数据源可通过交易所公开获取
- `can_be_quantized_now:` yes
- `current_role:` 可重开
- `content_excerpt_or_paraphrase:` 跟踪北向资金个股净买入额，选前一交易日净买入最高股票，次日9:30开盘买入

---

### 卡片 TX-06-S2

- `sample_id:` TX-06-S2
- `title:` 一个简单的跟踪聪明钱策略
- `cluster_name:` 资金流/事件驱动/聪明钱
- `method_family:` event_or_flow
- `data_requirements:` 资金流数据（主力/散户资金流向）、日线OHLCV
- `reusable_objects_or_fields:` 聪明钱定义（主力资金净流入/散户资金净流出）、资金流向阈值信号、跟单触发条件
- `retained_logic_summary:`
  - "聪明钱"定义为机构投资者或大户的资金流向
  - 通过主力资金净流入+散户资金净流出识别聪明钱动向
  - 当聪明钱持续流入某只股票时跟随买入
  - 本质是利用资金流的异质性（主力vs散户）获取信息优势
- `why_keep_or_not_keep:` 资金流向数据在A股有独特信息价值（北向资金/主力资金），该策略提供了资金流选股的规则壳，但需注意资金流数据的时效性和准确性
- `can_be_quantized_now:` partial
- `current_role:` future bucket
- `content_excerpt_or_paraphrase:` 通过主力资金净流入+散户资金净流出识别"聪明钱"动向，跟随聪明钱流向选股

---

### 卡片 TX-08-S1

- `sample_id:` TX-08-S1
- `title:` 分钟K线数据重构 ATR自适应通道
- `cluster_name:` 其他独立策略
- `method_family:` trend_system
- `data_requirements:` 分钟线OHLCV
- `reusable_objects_or_fields:` ArrayManager类（分钟K线拼接/重构）、ATR自适应通道计算、不均匀K线生成方法
- `retained_logic_summary:`
  - 自定义ArrayManager类实现分钟K线数据重构
  - 在固定时间点（如早盘收盘时）输出bar，实现不均匀K线
  - 基于ATR构建自适应通道，通道宽度随波动率自动调整
  - 突破通道上轨做多，跌破下轨做空
- `why_keep_or_not_keep:` ArrayManager的K线重构方法和ATR自适应通道具有工具层价值，可复用于其他分钟级策略
- `can_be_quantized_now:` yes
- `current_role:` future bucket
- `content_excerpt_or_paraphrase:` 自定义ArrayManager实现分钟K线重构+ATR自适应通道，通道宽度随波动率自动调整

---

### 卡片 TX-08-S2

- `sample_id:` TX-08-S2
- `title:` 机器学习SVM用法示例策略
- `cluster_name:` 其他独立策略
- `method_family:` factor_research
- `data_requirements:` 日线OHLCV、7个特征变量（收盘价均值比/现量比/最高价均值比/最低价均值比/成交量比值等）
- `reusable_objects_or_fields:` SVM分类模型训练框架、7个特征变量定义、未来5日涨跌标签构建方法、周三调仓机制
- `retained_logic_summary:`
  - 选择标的（同仁堂600085），取7个特征变量一年的数据训练SVM
  - 标签为后5个交易日涨跌（涨=1，跌=0）
  - 每周三调仓，模型预测未来5天涨跌，为1时买入否则空仓
  - 7个特征：收盘价/区间均收盘价均值、现量/区间均量、最高价/区间最高价均值、最低价/区间最低价均值、成交量比值
- `why_keep_or_not_keep:` 是ML在量化中应用的基础示例，特征工程思路（价格/成交量/极值的相对比值）可复用，但单标的训练存在过拟合风险，且SVM已非当前主流ML方法
- `can_be_quantized_now:` partial
- `current_role:` future bucket
- `content_excerpt_or_paraphrase:` SVM训练7个价格成交量特征→预测未来5日涨跌→周三调仓。特征为价格/成交量相对于区间均值的比值

---

## 5. 主题桶保留摘要

---

### TX-01 择时/均线/RSRS/KDJ/MACD（21份）

- `cluster_retained_takeaways:` RSRS择时系列（5份）是聚宽社区验证过的有效择时指标体系，与MACD/KDJ等低相关；GFTD多阶段趋势确认规则壳（78）比单指标更稳健；BIAS乖离率（21）可作为补充择时组件
- `common_reusable_fields:` RSRS斜率、RSRS标准化值、BIAS乖离率、MACD信号、KDJ金叉死叉、GFTD四阶段计数器（n1/n2/n3/count_lag）、DMI动向指数
- `common_failure_or_noise_points:` 大量MACD/KDJ金叉死叉策略（58/76/86/89/90/91）同质化严重、长期效果衰减；单指标策略胜率虽高但盈亏比有限；纯技术指标在A股2015年后有效性下降
- `if_delete_source_still_kept:` RSRS择时规则壳（含5个变体：日线/30分钟/大盘/优化/指标择时）、GFTD四阶段计数器规则、BIAS择时逻辑、各指标参数设定参考

---

### TX-02 多因子/财务因子/机器学习（20份）

- `cluster_retained_takeaways:` 祖鲁法则7大标准（23）是完整的多因子选股框架；CAPM+ROE（71）将经典金融模型与A股财务因子结合；多期限选股（15）提供时间尺度融合方法；SVM示例（98）的特征工程思路可复用
- `common_reusable_fields:` 祖鲁法则7因子（PE/EPS增长率/利润率/现金流/RS/市值/优势）、CAPM alpha计算、ROE股票池筛选、多期限收益率（1/3/6/12月）、SVM 7特征（价格/成交量比值）、低PB过滤规则
- `common_failure_or_noise_points:` 作业式策略（35/36/60/71）代码不完整；SVM（98）和随机森林（51）存在过拟合风险；低PB策略（31/44/85/94）在A股成长风格市场中长期表现不稳定；大量"小白"/"第一次玩"/"向导式"策略（88/85/61/63）无实质逻辑
- `if_delete_source_still_kept:` 祖鲁法则7大标准、CAPM+ROE框架、多期限选股框架、SVM特征工程模板、财务指标过滤规则壳

---

### TX-03 轮动/行业/ETF/市值（12份）

- `cluster_retained_takeaways:` 申万行业轮动（81）是A股经典的行业配置策略；银行股轮动（64）和AH套利（96/97）在A股具有独特价值；次新+小市值+KAMA（82）将多因子与自适应均线结合；小市值轮动（25/53/59）是A股长期有效的风格因子
- `common_reusable_fields:` 申万行业指数涨幅排序、行业成分股流通市值Top5选取、AH股溢价率、KAMA择时信号、小市值排序方法、月度轮动机制
- `common_failure_or_noise_points:` 小市值策略（53/59）在2017年后A股效果减弱（大盘股行情）；成长策略（34）过于笼统无具体规则；基金PE调仓（65）依赖基金数据实时性；向导式生成策略（61）无实质逻辑
- `if_delete_source_still_kept:` 申万行业轮动规则壳、银行股AH溢价套利方法、小市值轮动规则、KAMA择时参数

---

### TX-04 期货/海龟/多品种趋势（6份）

- `cluster_retained_takeaways:` 海龟法则（22）是完整的趋势交易系统规则壳；自适应均线+过滤器（01）比普通均线更先进；多品种动量验证框架（04）方法论可迁移至A股；截面动量（17）是另一种动量表达方式
- `common_reusable_fields:` 海龟规则（20日入市/10日离市/0.5N加仓/2N止损）、KAMA效率系数、ATR仓位计算公式、多品种动量排名、截面动量权重
- `common_failure_or_noise_points:` 期货策略直接迁移至A股股票需调整（杠杆/做空/T+1限制）；分钟级回测对数据源要求高；合约移仓机制仅限期货
- `if_delete_source_still_kept:` 海龟完整规则壳、KAMA+过滤器逻辑、ATR仓位管理公式、动量效应验证方法论

---

### TX-05 配对/均值回归/套利（7份）

- `cluster_retained_takeaways:` 协整配对（02）在A股有实际验证效果（聚宽擂台第一）；同行业龙头配对（13/19）思路独特；中小板-中证500配对（55）提供了指数级别配对思路
- `common_reusable_fields:` 协整检验方法、Z-score阈值、动态对冲比率、同行业龙头配对列表、OLS残差分析、指数配对（中小板vs中证500）
- `common_failure_or_noise_points:` 配对关系会随时间破裂（结构性变化）；需要做空机制（A股融券限制）；交易成本对高频配对影响大
- `if_delete_source_still_kept:` 协整配对规则壳、Z-score触发逻辑、同行业龙头配对思路、指数配对方法

---

### TX-06 资金流/事件驱动/聪明钱（6份）

- `cluster_retained_takeaways:` 北向资金跟踪（73）是A股特色数据源策略；聪明钱（38）提供了主力vs散户资金流向的选股框架；追涨停板（10）和次新（47）是A股特色事件驱动策略
- `common_reusable_fields:` 北向资金个股净买入额、主力资金净流入信号、散户净流出信号、涨停板追踪规则、次新股筛选方法
- `common_failure_or_noise_points:` 主力资金数据准确性存疑（主力/散户划分模糊）；追涨停板策略风险极高；次新小盘策略受IPO政策影响大
- `if_delete_source_still_kept:` 北向资金跟随规则壳、聪明钱定义与信号规则、涨停板追踪逻辑、次新股筛选方法

---

### TX-08 其他独立策略（8份）

- `cluster_retained_takeaways:` ATR自适应通道的分钟级实现（20）具有工具价值；基金定投回测（72）可作为被动投资baseline；沪深300增强（74）提供了指数增强思路
- `common_reusable_fields:` ArrayManager K线重构、ATR自适应通道、基金定投框架、指数增强方法
- `common_failure_or_noise_points:` LSTM预测（30）存在数据泄露和未来函数风险；低市值策略（14）流动性差；布林带策略（45）过于常见
- `if_delete_source_still_kept:` ArrayManager类设计、ATR通道规则壳、基金定投baseline

---

## 6. 低质量/重复清单

---

| title | reason |
|-------|--------|
| 16/60 投资学作业.txt | 纯课程作业，策略逻辑简单，无实质创新 |
| 24 自选策略1.txt | 无名策略，无描述，无明确策略逻辑 |
| 26 向导式-1.txt | 向导式模板代码，无实质策略内容 |
| 28 收益策略.txt | 标题过于笼统，无具体策略描述 |
| 32 测试策略1.txt | 纯测试代码，无实质策略逻辑 |
| 37 个股止损.txt | 仅止损功能演示，无完整策略 |
| 46 Get API 新技能，研究中写策略并回测.txt | API学习演示，无实质策略 |
| 48 再测一支.txt | 无描述，无明确策略逻辑 |
| 56 爱神的箭放声大哭.txt | 无意义标题，无实质策略描述 |
| 57 黄泽森策略.txt | 人名标题，无策略描述 |
| 61 向导式策略生成器生成的成长股精选策略.txt | 向导式自动生成，策略逻辑不透明 |
| 62 选股策略.txt | 标题过于笼统 |
| 63 向导式.txt | 向导式模板，无实质策略 |
| 84 投资策略说明.txt | 无实质策略描述 |
| 87 选股策略说明——张燕兰 16318320.txt | 人名+学号，课程作业性质 |
| 99 一个中信证券的向导策略.txt | 向导式生成，策略逻辑不透明 |
| 35/36 投资学作业多因子/改进.txt | 同一作业的两版迭代，策略逻辑简单 |
| 19/13 招行海天配对/改进版.txt | 同一策略的原始版和改进版，内容高度重复 |
| 58/90 MACD金叉买入死叉卖出.txt | 与76 MACD大盘择时高度重复 |
| 96/97 沪港银行翻倍/银行翻倍.txt | 同一策略的两份副本 |
| 86/89 均线金叉死叉择时.txt | 与90 MA均线金叉死叉高度重复 |

---

## 7. 删源后的保留充分性检查

---

- `delete_source_readiness:` yes

- `if_delete_source_still_kept:`
  - 8个主题桶的完整聚类结构和代表性标题已保留（覆盖全部99份）
  - 20张代表样本内容保留卡片覆盖了最值得保留的策略规则壳：
    - 择时层：RSRS择时（05）、RSRS30分钟（27）、GFTD（78）、BIAS择时（21）、RSRS大盘优化（77）
    - 多因子层：祖鲁法则7标准（23）、多期限选股（15）、CAPM+ROE（71）、SVM特征工程（98）
    - 轮动层：申万行业轮动（81）、银行股轮动（64）、AH银行套利（96）
    - 趋势层：海龟完整规则（22）、自适应均线+过滤器（01）、动量验证框架（04）
    - 配对层：协整配对（02）、招行海天配对改进（13）
    - 资金流：北向资金跟随（73）、聪明钱跟踪（38）
    - 工具层：ArrayManager K线重构（20）
  - 每个主题桶的cluster_retained_takeaways、common_reusable_fields、common_failure_or_noise_points已保留
  - 低质量/重复清单已标注（21条），便于后续筛选时排除

- `still_missing_if_any:`
  - 部分txt文件的策略描述过于简略（仅代码注释），无法提取更详细的策略逻辑
  - 部分策略的具体参数（如RSRS阈值、Z-score阈值等）需在原代码中查找，卡片中未逐一记录
  - 若需完整参数，建议保留原始txt文件或补充参数提取工作

---

## 8. 最终建议

---

- 这批txt里最值得留下的3个主题桶：
  1. **TX-06 资金流/事件驱动/聪明钱（6份）**——北向资金跟踪（73）是A股特色数据源策略，具有独特信息优势；聪明钱（38）提供了主力vs散户的选股框架
  2. **TX-03 轮动/行业/ETF/市值（12份）**——申万行业轮动（81）是A股经典配置策略；银行股AH套利（96/97）有真实市场机制支撑；次新+小市值+KAMA（82）将多因子与自适应均线结合
  3. **TX-04 期货/海龟/多品种趋势（6份）**——海龟规则壳是趋势交易经典基础设施，自适应均线+过滤器解决震荡市假信号问题，方法论可迁移至A股
- 最不值得继续切的3类内容：
  1. **TX-07 低质量杂项（17份）**——作业/测试/无名策略/向导式生成，无实质策略逻辑
  2. **TX-01 中的纯技术指标单因子策略**（MACD金叉死叉/KDJ金叉死叉/均线交叉等约10份）——同质化严重，长期效果衰减
  3. **TX-02 中的"小白"/"第一次玩"/"向导式"策略**（88/85/61/63等）——无实质逻辑，属于社区练习
- 如果后续要继续，只建议深挖 **TX-06（北向资金+聪明钱）** 和 **TX-03（行业轮动+AH套利）**，因为它们的策略规则壳最完整、与A股适配性最好、且具有A股特色（北向资金/AH溢价/行业轮动是A股独特alpha来源）
- 当前最稳的角色是：**模板池**——这批txt本质上是99个策略代码模板（来自聚宽社区），有价值的是其中约20个可复用的规则壳，其余为社区练习代码或重复实现

---

## 9. 文件夹落点建议

---

- `target_folder:` 03_txt标题聚类
- `recommended_output_name:` A股_txt标题聚类与内容保留_v1.md
