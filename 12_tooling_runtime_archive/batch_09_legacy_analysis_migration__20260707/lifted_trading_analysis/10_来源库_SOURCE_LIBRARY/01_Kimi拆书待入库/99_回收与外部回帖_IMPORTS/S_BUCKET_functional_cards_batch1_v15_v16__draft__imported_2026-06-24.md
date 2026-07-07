# S_BUCKET Functional Object Card Drafts — Batch 1 (v15 + v16)

**Template ID:** `S_BUCKET_FUNCTIONAL_OBJECT_CARD__KIMI_BATCH`  
**Batch ID:** `batch1_v15_v16`  
**Source Manifest:** `manifest.tsv`  
**Files in Batch:** 16  
**Evidence Scope:** 仅读取 `manifest.tsv` 与文件名/路径层级。PDF 正文未读取，未进行 OCR 或文本提取。  
**Agent Note:** 所有基于文件名的推断均标注为 `[filename-derived]`；无法确认的内容标注为 `待核`。

---

## 01 高频微观 (4 objects)

---

### SBKT_F001

- **object_id:** SBKT_F001
- **object_name:** 听海外高频交易专家讲解美国的高频交易
- **source_anchor:** `03_券商研报/01_高频微观/20190611-海通证券-金融工程专题报告：听海外高频交易专家讲解美国的高频交易.pdf`
- **function_bucket:** 高频微观 / 执行机制
- **process_layer:** execution / explanation
- **scope_tags:** `[filename-derived]` 美国高频交易、海外专家访谈、执行机制、市场结构
- **maturity_level:** 概念层 / 译介层 — 券商专题报告，转述海外专家观点，未验证是否含可直接落地的 A 股参数
- **role_type:** explanation（更偏向解释海外机制，非直接 alpha 公式）
- **input_requirement:** 待核 — 正文是否列出数据需求、频率、品种未确认
- **output_form:** 待核 — 可能为定性综述、访谈纪要、或含对比表格
- **best_use_case:** 作为理解美国高频交易生态的参考素材；若需迁移至 A 股，需额外验证规则差异
- **cannot_do_yet:** 直接迁移至 A 股执行策略（中美市场结构差异待核）；提取可复用参数（正文未读）；确认是否含滑点/延迟数据
- **combines_with:** 待核
- **overlaps_with:** 待核 — 可能与 SBKT_F009/F010 在高频数据应用方向存在重叠，需正文比对
- **failure_modes:** 把海外经验直接套用到 A 股；把专家观点当作已验证策略
- **evidence_note:** 仅基于文件名推断。PDF 正文未读取。标题含“讲解”，倾向解释型材料。

---

### SBKT_F002

- **object_id:** SBKT_F002
- **object_name:** 分布估计下的主动成交占比（高频因子七）
- **source_anchor:** `03_券商研报/01_高频微观/20200810-长江证券-基础因子研究（十二），高频因子（七）：分布估计下的主动成交占比.pdf`
- **function_bucket:** 高频微观 / alpha 因子
- **process_layer:** alpha / filter
- **scope_tags:** `[filename-derived]` 高频因子、主动成交占比、分布估计、基础因子研究
- **maturity_level:** 可验证层 — 属于系列化因子研究报告（第十二篇），但因子在 A 股是否仍有效需回测确认
- **role_type:** alpha（含因子构造逻辑）
- **input_requirement:** `[filename-derived]` 高频成交数据（分钟/ tick 级别）、买卖方向判别、分布估计方法
- **output_form:** `[filename-derived]` 因子值序列、IC/IR、分层测试、行业中性后的表现
- **best_use_case:** 作为主动成交类高频因子的候选输入；可与资金流向/波动率类因子组合
- **cannot_do_yet:** 直接用于实盘（需确认最新数据下的衰减与过拟合）；因子分布估计的具体参数（核函数/窗口长度）待核
- **combines_with:** 资金流向因子（如 SBKT_F014）、波动率因子（如 SBKT_F006）
- **overlaps_with:** 待核 — 可能与华泰/国盛/广发的同主题高频因子报告重叠
- **failure_modes:** 把历史回测 IC 当作未来收益保证；忽略因子在 2020 年后的失效风险
- **evidence_note:** 文件名明确为因子研究序列第七篇，含“分布估计”与“主动成交占比”，推断为构造型 alpha 因子报告。正文未读取。

---

### SBKT_F009

- **object_id:** SBKT_F009
- **object_name:** 使用高频数据跟踪核心资产的公募基金持仓变化
- **source_anchor:** `03_券商研报/01_高频微观/20210428-海通证券-高频数据应用系列研究（一）：使用高频数据跟踪核心资产的公募基金持仓变化.pdf`
- **function_bucket:** 高频微观 / 资金流向 / 持仓推断
- **process_layer:** alpha / filter
- **scope_tags:** `[filename-derived]` 高频数据、公募基金持仓、核心资产、持仓变化跟踪
- **maturity_level:** 方法层 — 有明确应用场景（跟踪公募持仓），但推断精度与数据频率要求待核
- **role_type:** alpha / filter（通过推断持仓变化生成信号或筛选池）
- **input_requirement:** `[filename-derived]` 高频交易数据（推测为分钟或日内的委托/成交片段）、核心资产成分、公募基金历史持仓披露
- **output_form:** `[filename-derived]` 持仓变化推断指标、偏离度信号、调仓频率估计
- **best_use_case:** 作为观察机构调仓动向的辅助工具；可作为事件驱动或资金流信号的输入
- **cannot_do_yet:** 确认高频数据的具体频率（Level-2/ tick / 分钟）；推断方法的误差率与假阳性率；与官方披露持仓的对照验证
- **combines_with:** 资金流向因子（SBKT_F014）、基金重仓股研究（SBKT_F007）
- **overlaps_with:** 待核 — 与 SBKT_F010（算法交易监测机构动向）可能在“机构动向”主题上重叠
- **failure_modes:** 把高频推断持仓当作真实持仓；忽略公募季报披露与推断之间的时滞误差
- **evidence_note:** 文件名含“高频数据应用系列研究（一）”，推断为方法型应用报告。正文未读取。

---

### SBKT_F010

- **object_id:** SBKT_F010
- **object_name:** 利用高频数据监测机构动向
- **source_anchor:** `03_券商研报/01_高频微观/20210730-国泰君安-算法交易系列二：利用高频数据监测机构动向.pdf`
- **function_bucket:** 高频微观 / 算法交易 / 机构监测
- **process_layer:** execution / filter
- **scope_tags:** `[filename-derived]` 算法交易、高频数据、机构动向、系列报告
- **maturity_level:** 方法层 — 系列化报告（第二篇），但“监测机构动向”的具体准确率待核
- **role_type:** execution / filter（偏执行与监测，非直接定价 alpha）
- **input_requirement:** 待核 — 推测为高频委托/成交数据、算法交易特征识别规则
- **output_form:** 待核 — 可能为机构动向评分、异常交易标记、压力/支撑识别
- **best_use_case:** 作为市场微观结构监测模块；若含可识别的大单拆分/冰山订单特征，可用于执行优化
- **cannot_do_yet:** 具体监测规则与阈值；是否适用于 A 股当前全市场还是仅针对特定板块；与 SBKT_F009 的功能边界划分
- **combines_with:** 待核 — 若含订单流分析，可与 Volume Profile / 订单流模型组合
- **overlaps_with:** 待核 — 与 SBKT_F009 均涉及高频数据+机构行为，需正文比对以确认差异
- **failure_modes:** 把监测到的异常信号直接当作交易信号，不做独立验证；混淆机构调仓与算法拆单
- **evidence_note:** 文件名含“算法交易系列二”与“监测机构动向”，推断为偏向执行与监测的应用报告。正文未读取。

---

## 02 机器学习 (6 objects)

---

### SBKT_F003

- **object_id:** SBKT_F003
- **object_name:** Machine Learning in Finance: From Theory to Practice (Springer, 2020)
- **source_anchor:** `03_券商研报/03_机器学习/Machine Learning in Finance_ From Theory to Practice-Springer (2020).pdf`
- **function_bucket:** 机器学习 / 教材底座
- **process_layer:** explanation / alpha（取决于具体章节）
- **scope_tags:** `[filename-derived]` 机器学习、金融、Springer、教材、理论到实践
- **maturity_level:** 教材层 — 教科书性质，系统性强，但“实践”部分是否直接对应 A 股数据待核
- **role_type:** explanation（底座知识，非单一策略）
- **input_requirement:** 待核 — 教科书通常列出通用数据类型（价格、财报、宏观），但具体章节要求未确认
- **output_form:** 待核 — 可能含模型框架、代码示例、案例数据集结果
- **best_use_case:** 作为团队机器学习方法论的共同底座；可用于提取特征工程、交叉验证、模型评估的通用规范
- **cannot_do_yet:** 直接移植到 A 股实盘（教材通用性强，市场规则差异需本地化）；确认是否含伪代码或真实代码（需去代码块化）；确认理论与实践章节占比
- **combines_with:** 华泰人工智能系列（SBKT_F004/F005/F012/F013）作为理论与本土实践之间的桥梁
- **overlaps_with:** 待核 — 若含深度学习章节，可能与 CNN/RNN 教材（SBKT_F011）重叠
- **failure_modes:** 把教材案例当作可直接复现策略；忽略教材数据与 A 股数据质量差异
- **evidence_note:** 文件名明确为 Springer 2020 年教材，标题为“从理论到实践”。正文未读取。

---

### SBKT_F004

- **object_id:** SBKT_F004
- **object_name:** 再论时序交叉验证对抗过拟合（华泰人工智能系列 16）
- **source_anchor:** `03_券商研报/03_机器学习/华泰人工智能系列16：再论时序交叉验证对抗过拟合.pdf`
- **function_bucket:** 机器学习 / 方法论 / 过拟合控制
- **process_layer:** explanation / risk（过拟合属于模型风险）
- **scope_tags:** `[filename-derived]` 时序交叉验证、过拟合、华泰、系列 16、人工智能选股
- **maturity_level:** 方法层 — 系列化研究，主题为“再论”，暗示已有前序基础，方法本身成熟，但具体参数待核
- **role_type:** explanation / risk（强调方法论与风险控制，非直接 alpha）
- **input_requirement:** `[filename-derived]` 时序数据集、模型训练框架、回测环境
- **output_form:** `[filename-derived]` 交叉验证方案对比、过拟合度量、推荐验证策略
- **best_use_case:** 作为量化选股模型训练流程中的验证层规范；可用于改进现有训练-测试切分方式
- **cannot_do_yet:** 时序交叉验证的具体切分规则（ purge / embargo / 滑动窗口长度）；在 A 股非平稳环境下的失效边界；与 SBKT_F012（数据标注）的方法衔接
- **combines_with:** 华泰系列 28（SBKT_F005，体系概览）、华泰系列 17（SBKT_F012，数据标注）
- **overlaps_with:** 待核 — 与 SBKT_F003 中“交叉验证”章节可能重叠，但深度不同
- **failure_modes:** 把验证方法当作策略收益保证；在训练流程中仅换验证方式而不换模型导致伪稳健
- **evidence_note:** 文件名含“再论”，暗示已有前序讨论。主题为方法论而非因子。正文未读取。

---

### SBKT_F005

- **object_id:** SBKT_F005
- **object_name:** 基于量价的人工智能选股体系概览（华泰人工智能系列 28）
- **source_anchor:** `03_券商研报/03_机器学习/华泰人工智能系列28：基于量价的人工智能选股体系概览.pdf`
- **function_bucket:** 机器学习 / 选股体系
- **process_layer:** alpha
- **scope_tags:** `[filename-derived]` 人工智能选股、量价、体系概览、华泰、系列 28
- **maturity_level:** 体系层 — “概览”意味着框架性总结，可能含多个子模块，但单模块深度待核
- **role_type:** alpha / explanation（框架性 alpha 体系）
- **input_requirement:** `[filename-derived]` 量价数据（OHLCV，推测含分钟或日频）、特征工程、标注数据
- **output_form:** `[filename-derived]` 选股体系框架、子模型结构、组合信号、回测表现
- **best_use_case:** 作为华泰 AI 选股系列的索引级入口；若含完整链路，可作为策略搭建的参照蓝图
- **cannot_do_yet:** 具体特征列表与频率；模型结构（树/神经网络/线性）；是否含端到端代码或仅框架图；组合权重方案
- **combines_with:** 华泰系列 16（SBKT_F004，验证方法）、华泰系列 30（SBKT_F013，因果推断）作为稳健性与去伪层
- **overlaps_with:** 待核 — 与 SBKT_F003（教材）在“量价特征”章节可能重叠；与 SBKT_F012 在“标注”环节可能重叠
- **failure_modes:** 把“概览”当作可直接跑通的完整系统；忽略框架中某些模块需要额外数据（Level-2/NLP）
- **evidence_note:** 文件名含“体系概览”与“系列 28”，推断为框架性总结报告。正文未读取。

---

### SBKT_F011

- **object_id:** SBKT_F011
- **object_name:** Reinforcement Learning for Finance: Solve Problems in Finance with CNN and RNN Using the TensorFlow Library
- **source_anchor:** `03_券商研报/03_机器学习/Reinforcement Learning for Finance_ Solve Problems in Finance with CNN and RNN Using the TensorFlow Library.pdf`
- **function_bucket:** 机器学习 / 强化学习 / 深度学习
- **process_layer:** alpha / explanation
- **scope_tags:** `[filename-derived]` 强化学习、CNN、RNN、TensorFlow、金融、教材/专著
- **maturity_level:** 教材层 — 明确为编程导向教材，含 TensorFlow 实现，但“金融问题”的具体范围待核
- **role_type:** explanation / alpha（含实现代码，但需本地化验证）
- **input_requirement:** 待核 — 推测为时间序列数据、价格/回报序列、状态空间定义、市场模拟环境
- **output_form:** 待核 — 可能为策略网络、价值网络、TensorFlow 代码示例、模拟环境回报曲线
- **best_use_case:** 作为强化学习落地金融的工程参考；若含市场模拟环境，可用于策略原型验证
- **cannot_do_yet:** 直接用于 A 股实盘（RL 样本效率与交易成本未确认）；是否有真实市场回测还是仅限模拟环境；CNN/RNN 的输入频率与特征；是否含伪代码/代码块（需处理）
- **combines_with:** 华泰 AI 系列作为深度学习到本土化的过渡
- **overlaps_with:** 待核 — 与 SBKT_F003 在 CNN/RNN 章节可能重叠；与 SBKT_F005 在“深度学习选股”方向可能重叠
- **failure_modes:** 把模拟环境最优策略直接上线；忽略 RL 在金融中的过拟合与样本外泛化问题；把 TensorFlow 旧版本代码当作当前可用
- **evidence_note:** 文件名明确为教材/专著，含 TensorFlow 与 CNN/RNN。正文未读取。

---

### SBKT_F012

- **object_id:** SBKT_F012
- **object_name:** 人工智能选股数据标注方法实证（华泰人工智能系列 17）
- **source_anchor:** `03_券商研报/03_机器学习/华泰人工智能系列17：人工智能选股数据标注方法实证.pdf`
- **function_bucket:** 机器学习 / 数据工程 / 标注方法
- **process_layer:** alpha / explanation（数据标注是监督学习的前提）
- **scope_tags:** `[filename-derived]` 人工智能选股、数据标注、标注方法、实证、华泰、系列 17
- **maturity_level:** 方法层 — 专项研究“标注方法”，对监督学习流程有直接影响，但最优标注方式是否随市场变化待核
- **role_type:** explanation / alpha（标注方法决定标签质量，间接影响 alpha）
- **input_requirement:** `[filename-derived]` 原始量价/财务数据、不同标注规则（收益率/分类/排序）、标注窗口长度
- **output_form:** `[filename-derived]` 标注方法对比、不同标注下的模型表现差异、推荐标注方案
- **best_use_case:** 作为华泰 AI 选股流程中的数据层规范；可作为团队统一标注标准的参考
- **cannot_do_yet:** 具体标注方案列表（未来收益/未来收益排序/动量/反转等）；最优标注在不同市场阶段的稳定性；与 SBKT_F005（体系概览）中标注模块的衔接方式
- **combines_with:** 华泰系列 16（SBKT_F004，验证）、华泰系列 28（SBKT_F005，体系）
- **overlaps_with:** 待核 — 与 SBKT_F003 中“标签构建”章节可能重叠；与 SBKT_F005 在体系内可能重复
- **failure_modes:** 把单一标注方案当作普适最优；忽略标注泄露（lookahead）风险；在标注时混入未来信息
- **evidence_note:** 文件名明确为“数据标注方法实证”，属于数据工程层研究。正文未读取。

---

### SBKT_F013

- **object_id:** SBKT_F013
- **object_name:** 从关联到逻辑：因果推断初探（华泰人工智能系列 30）
- **source_anchor:** `03_券商研报/03_机器学习/华泰人工智能系列30：从关联到逻辑：因果推断初探.pdf`
- **function_bucket:** 机器学习 / 因果推断 / 方法论
- **process_layer:** explanation / risk（因果推断用于解释模型与识别伪相关）
- **scope_tags:** `[filename-derived]` 因果推断、关联、逻辑、华泰、系列 30、人工智能选股
- **maturity_level:** 概念层 — “初探”意味着早期探索，距离工程化部署可能较远
- **role_type:** explanation（当前更偏向解释与归因，非直接信号生成）
- **input_requirement:** 待核 — 推测为因子/特征数据集、干预变量定义、对照组构造数据
- **output_form:** 待核 — 可能为因果效应估计、后门准则应用、特征去伪结果
- **best_use_case:** 作为团队理解“相关性≠因果性”的参考；若含可操作方法，可用于因子去伪与稳健性检验
- **cannot_do_yet:** 具体因果推断方法（DoWhy/Pearl 框架/工具变量）；在 A 股高维因子中的计算可行性；从“初探”到“可复用模块”的转化路径
- **combines_with:** 多因子系列（SBKT_F006/F014）中因子去伪
- **overlaps_with:** 待核 — 与 SBKT_F003 中“因果推断”章节可能重叠
- **failure_modes:** 把因果推断的初步结论当作交易信号；混淆统计因果与经济学因果；忽略未观测混淆变量
- **evidence_note:** 文件名含“初探”，推断为早期探索性研究。正文未读取。

---

## 03 多因子 (6 objects)

---

### SBKT_F006

- **object_id:** SBKT_F006
- **object_name:** 单因子测试之波动率类因子（华泰多因子系列 6）
- **source_anchor:** `03_券商研报/04_多因子/华泰多因子系列6：单因子测试之波动率类因子.pdf`
- **function_bucket:** 多因子 / 单因子测试 / 波动率
- **process_layer:** alpha / filter
- **scope_tags:** `[filename-derived]` 单因子测试、波动率类因子、华泰、系列 6、多因子
- **maturity_level:** 可验证层 — 华泰多因子系列为标准券商因子研究，通常含完整测试流程，但因子有效性衰减需确认
- **role_type:** alpha / filter（波动率类因子通常用于选股或风险分层）
- **input_requirement:** `[filename-derived]` 个股收益率序列（日频，推测）、波动率计算窗口、行业/市值中性化数据
- **output_form:** `[filename-derived]` 单因子 IC、IR、分层收益、换手率、衰减分析、与常见波动率指标（如 STD、BETA、残差波动率）的细分结果
- **best_use_case:** 作为波动率类因子的候选库输入；可作为多因子模型中风险/alpha 因子的备选
- **cannot_do_yet:** 具体波动率因子定义列表（如已实现波动率/下行波动率/特异波动率）；因子在最新样本外的表现；与 SBKT_F014（资金流向）的互补性验证
- **combines_with:** 华泰多因子系列 7（SBKT_F014，资金流向）、国盛因子择时（SBKT_F015，攻守配置）、广发均值回复（SBKT_F008）
- **overlaps_with:** 待核 — 与广发多因子系列 12/13（SBKT_F008/F016）在波动率/非线性方向可能重叠
- **failure_modes:** 把历史 IC 当作未来收益；忽略波动率因子在极端行情中的尾部风险放大；单因子测试与组合测试脱节
- **evidence_note:** 文件名明确为“单因子测试之波动率类因子”，属于标准券商因子测试报告。正文未读取。

---

### SBKT_F007

- **object_id:** SBKT_F007
- **object_name:** 基金重仓股研究（国盛多因子系列 13）
- **source_anchor:** `03_券商研报/04_多因子/国盛多因子系列13：基金重仓股研究.pdf`
- **function_bucket:** 多因子 / 机构行为 / 选股
- **process_layer:** alpha / filter
- **scope_tags:** `[filename-derived]` 基金重仓股、机构行为、国盛、系列 13、多因子
- **maturity_level:** 方法层 — 主题明确（基金重仓），但因子化方式（持仓复制/跟踪/偏离）待核
- **role_type:** alpha / filter（重仓股可作为选股池或事件信号）
- **input_requirement:** `[filename-derived]` 公募基金季报/半年报重仓股数据、持仓市值、行业分布、调仓频率
- **output_form:** `[filename-derived]` 重仓股因子值、跟踪组合收益、偏离度、主动/被动管理识别
- **best_use_case:** 作为机构跟随策略的候选输入；可作为选股池缩小范围（filter）；结合 SBKT_F009/F010 的高频持仓推断进行交叉验证
- **cannot_do_yet:** 具体因子定义（持仓集中度/超配比例/新增重仓等）；因子在不同市场风格（大盘/小盘）下的稳定性；与 ETF/北向资金的区分
- **combines_with:** 华泰高频持仓跟踪（SBKT_F009）、国泰君安机构动向监测（SBKT_F010）
- **overlaps_with:** 待核 — 与 SBKT_F009 均涉及“持仓/机构”主题，但频率与方法论差异待正文确认
- **failure_modes:** 把重仓股列表当作可直接买入名单（忽略时滞与披露偏差）；把机构抱团当作持续 alpha（忽略反转风险）
- **evidence_note:** 文件名明确为“基金重仓股研究”，属于机构行为+多因子交叉方向。正文未读取。

---

### SBKT_F008

- **object_id:** SBKT_F008
- **object_name:** 从 ICIR 角度探讨风格因子的均值回复性（广发多因子系列 12）
- **source_anchor:** `03_券商研报/04_多因子/广发多因子系列12：从ICIR角度探讨风格因子的均值回复性.pdf`
- **function_bucket:** 多因子 / 风格因子 / 因子择时
- **process_layer:** alpha / risk（均值回复性可用于因子择时或风险预警）
- **scope_tags:** `[filename-derived]` ICIR、风格因子、均值回复、广发、系列 12、多因子
- **maturity_level:** 方法层 — 主题为“均值回复性”，通常涉及时间序列建模，但具体模型与参数待核
- **role_type:** alpha / risk（若用于因子择时，属 alpha；若用于规避因子拥挤，属 risk）
- **input_requirement:** `[filename-derived]` 风格因子收益率序列（日频/月频）、IC/IR 滚动窗口、均值回复时间尺度
- **output_form:** `[filename-derived]` 均值回复半衰期、ICIR 预测值、因子择时信号、风格切换概率
- **best_use_case:** 作为因子择时模块的输入；可用于动态调整风格因子暴露；可验证常见风格因子（市值/价值/动量/质量）的回复周期
- **cannot_do_yet:** 具体风格因子列表；均值回复的计量模型（AR/OU/简单滚动均值）；样本外预测胜率；与 SBKT_F015（攻守因子配置）的互补或冲突
- **combines_with:** 国盛因子择时（SBKT_F015，攻守配置）、华泰单因子测试（SBKT_F006/F014）、广发非线性（SBKT_F016）
- **overlaps_with:** 待核 — 与 SBKT_F015 均涉及“因子择时/配置”，但视角（ICIR 均值回复 vs 风险溢价时钟）不同，需正文确认差异
- **failure_modes:** 把历史均值回复规律当作未来确定性；在回复期未结束时过早反向押注；忽略结构性变化导致的回复规律消失
- **evidence_note:** 文件名明确为“从 ICIR 角度探讨风格因子的均值回复性”，属于因子择时/风格研究。正文未读取。

---

### SBKT_F014

- **object_id:** SBKT_F014
- **object_name:** 单因子测试之资金流向因子（华泰多因子系列 7）
- **source_anchor:** `03_券商研报/04_多因子/华泰多因子系列7：单因子测试之资金流向因子.pdf`
- **function_bucket:** 多因子 / 单因子测试 / 资金流向
- **process_layer:** alpha / filter
- **scope_tags:** `[filename-derived]` 单因子测试、资金流向因子、华泰、系列 7、多因子
- **maturity_level:** 可验证层 — 标准券商因子测试，通常含完整 IC/IR 与分层测试，但资金流向因子在 A 股的有效性衰减需确认
- **role_type:** alpha / filter（资金流向通常用于选股或资金流跟踪）
- **input_requirement:** `[filename-derived]` 日频或更高频成交数据、主动/被动买卖方向判别、资金流计算规则（如超大单/大单/中单/小单划分）
- **output_form:** `[filename-derived]` 单因子 IC、IR、分层收益、资金流向细分指标（如主力净流入/散户净流出）表现
- **best_use_case:** 作为资金流向类因子的候选库输入；可与 SBKT_F002（主动成交占比）进行高频-日频互补
- **cannot_do_yet:** 具体资金流向定义（与 SBKT_F002 的“主动成交占比”关系）；因子在最新样本外表现；与 Level-2 逐笔数据的兼容性
- **combines_with:** 华泰波动率（SBKT_F006）、长江主动成交占比（SBKT_F002）、国盛重仓股（SBKT_F007）
- **overlaps_with:** 待核 — 与 SBKT_F002 均涉及“主动/资金流向”，但频率与定义可能不同；需正文比对
- **failure_modes:** 把资金流方向当作价格方向（忽略主力资金诱多/诱空）；单因子测试与组合测试脱节；忽略 T+1 制度下资金流向的可交易性
- **evidence_note:** 文件名明确为“单因子测试之资金流向因子”，属于标准券商因子测试。正文未读取。

---

### SBKT_F015

- **object_id:** SBKT_F015
- **object_name:** 风险溢价时钟视角下的攻守因子配置（国盛因子择时）
- **source_anchor:** `03_券商研报/04_多因子/国盛因子择时：风险溢价时钟视角下的攻守因子配置.pdf`
- **function_bucket:** 多因子 / 因子择时 / 资产配置
- **process_layer:** alpha / risk（攻守配置属于风险预算与 alpha 的权衡）
- **scope_tags:** `[filename-derived]` 风险溢价时钟、因子择时、攻守配置、国盛、多因子
- **maturity_level:** 方法层 — 有明确框架（风险溢价时钟），但时钟划分方式、切换信号、历史胜率待核
- **role_type:** alpha / risk（偏配置与择时，非单因子选股）
- **input_requirement:** `[filename-derived]` 风险溢价指标（股权风险溢价/信用利差/期限溢价等）、因子收益率历史、市场状态划分数据
- **output_form:** `[filename-derived]` 风险溢价时钟状态、攻守因子配置权重、因子暴露建议、历史回测表现
- **best_use_case:** 作为因子配置层面的宏观-中观桥梁；可用于动态调整价值/成长/防御/进攻因子的权重
- **cannot_do_yet:** 具体风险溢价指标定义与计算；时钟划分数量与边界（几象限？）；切换规则的滞后与胜率；与 SBKT_F008（ICIR 均值回复）的融合方式
- **combines_with:** 广发均值回复（SBKT_F008）、华泰单因子测试（SBKT_F006/F014）、国盛重仓股（SBKT_F007）
- **overlaps_with:** 待核 — 与 SBKT_F008 均涉及“因子择时/配置”，但视角（风险溢价时钟 vs ICIR 均值回复）不同，需正文确认差异
- **failure_modes:** 把风险溢价时钟当作精确择时工具（忽略宏观指标的滞后与噪音）；在时钟边界频繁切换导致高换手率；把历史宏观-因子关系当作恒定规律
- **evidence_note:** 文件名明确为“风险溢价时钟视角下的攻守因子配置”，属于因子择时+宏观配置交叉方向。正文未读取。

---

### SBKT_F016

- **object_id:** SBKT_F016
- **object_name:** 考虑非线性特征的多因子 Alpha 策略（广发多因子系列 13）
- **source_anchor:** `03_券商研报/04_多因子/广发多因子系列13：考虑非线性特征的多因子Alpha策略 .pdf`
- **function_bucket:** 多因子 / 非线性 / Alpha 策略
- **process_layer:** alpha
- **scope_tags:** `[filename-derived]` 非线性特征、多因子、Alpha 策略、广发、系列 13
- **maturity_level:** 策略层 — 明确为“Alpha 策略”，非纯因子测试，但非线性模型的复杂度与过拟合风险待核
- **role_type:** alpha（直接输出策略或组合信号）
- **input_requirement:** `[filename-derived]` 多因子数据（推测为日频因子截面）、非线性模型（如树模型/神经网络/交互项）、组合优化参数
- **output_form:** `[filename-derived]` 非线性 alpha 策略收益、因子交互效应、组合权重、风险调整后收益
- **best_use_case:** 作为线性多因子模型的补充；若非线性部分可解释，可用于提取被线性模型遗漏的因子交互效应
- **cannot_do_yet:** 具体非线性模型类型（GBDT/神经网络/Polynomial features）；非线性部分的解释性与稳定性；过拟合控制方式（是否含时序交叉验证）；与 SBKT_F005（华泰 AI 体系）的关系
- **combines_with:** 华泰多因子系列（SBKT_F006/F014）作为线性基底；华泰 AI 系列（SBKT_F005）作为非线性模型参考；广发均值回复（SBKT_F008）作为风格择时补充
- **overlaps_with:** 待核 — 与 SBKT_F005（华泰 AI 体系概览）在非线性选股方向可能重叠；与 SBKT_F008（均值回复）在因子交互方向可能重叠
- **failure_modes:** 非线性模型过拟合导致样本外崩溃；把训练期非线性收益当作持续 alpha；忽略非线性模型的可交易性与换手率
- **evidence_note:** 文件名明确为“考虑非线性特征的多因子 Alpha 策略”，属于策略层报告。正文未读取。

---

## 本批归纳摘要

- **本批共同主题:**  
  本批 16 个对象全部落在 `03_券商研报` 大桶下，细分至三个子桶：`01_高频微观`（4 个）、`03_机器学习`（6 个）、`04_多因子`（6 个）。共同主题是“券商与教材级别的量化方法论”，涵盖因子构造、机器学习流程、高频数据应用、因子配置四个子域。所有对象均来自 2019–2021 年间的券商研报或 2020 年 Springer 教材，时间跨度集中，但需验证因子衰减与模型时效。

- **本批可复用对象:**  
  `[filename-derived]` 推测可优先进入功能映射表候选的对象：
  - SBKT_F002（长江高频因子-主动成交占比）：因子构造型，若正文含清晰公式与数据要求，可较快进入因子库。
  - SBKT_F006 / SBKT_F014（华泰单因子测试-波动率/资金流向）：标准券商因子测试格式，若含完整 IC/IR 与分层测试，可作为单因子候选库底座。
  - SBKT_F004（华泰 AI 系列 16-时序交叉验证）：方法论通用性强，可作为团队训练流程的验证层规范。
  - SBKT_F007（国盛基金重仓股）：主题明确，输入输出边界较清晰，可作为机构行为 filter。
  
  **注意：** 以上判断均基于文件名推断，需正文读取后确认是否真正可复用。

- **本批仍然只是概念层的对象:**  
  `[filename-derived]` 推测目前仍停留在概念/教材层的对象：
  - SBKT_F001（海通-海外高频交易讲解）：解释型访谈，不含直接可执行策略。
  - SBKT_F003（Springer ML in Finance）：教材性质，通用方法需大量本地化。
  - SBKT_F011（RL for Finance with CNN/RNN）：教材性质，含 TensorFlow 代码但需验证版本与 A 股适用性。
  - SBKT_F013（华泰 AI 系列 30-因果推断初探）：标题含“初探”，推断为早期探索，工程化距离较远。
  - SBKT_F015（国盛-风险溢价时钟）：宏观框架型，需验证时钟划分精度与切换信号胜率。

- **建议优先进入下一轮仓库功能映射表的对象:**  
  `[filename-derived]` 优先级排序（从高到低）：
  1. SBKT_F006 / SBKT_F014（华泰单因子测试-波动率/资金流向）：标准格式，可快速纳入单因子库。
  2. SBKT_F002（长江高频因子-主动成交占比）：因子构造明确，可作为高频因子候选。
  3. SBKT_F007（国盛基金重仓股）：输入数据明确（公募季报），可作为机构行为 filter。
  4. SBKT_F004（华泰 AI 系列 16-时序交叉验证）：方法论通用，可嵌入训练流程。
  5. SBKT_F008（广发-ICIR 均值回复）/ SBKT_F015（国盛-风险溢价时钟）：若正文含可复用参数，可作为因子择时模块候选。
  6. 其余对象建议先完成正文读取与摘录（CUTPACK）后再进入功能映射表。

---

## 质量声明与限制

- **本产出为草稿（draft），非仓库最终 truth。**  
- **所有推断均基于 `manifest.tsv` 与文件名，未读取 PDF 正文。**  
- **每个对象的 `待核` 字段需在后续阅读正文后补全或修正。**  
- **`role_type`（alpha/filter/risk/execution/explanation）为基于文件名的最可能归类，需正文确认。**  
- **若正文与文件名推断冲突，以正文为准，本卡需修订。**  

---

*Generated by: S_BUCKET_FUNCTIONAL_OBJECT_CARD__KIMI_BATCH*  
*Batch: batch1_v15_v16*  
*Objects: 16*  
*Evidence tier: filename + manifest metadata only*
