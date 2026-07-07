extract_status: success

---

# MATERIAL_CARD

| field | value |
|-------|-------|
| title | 量化交易之路——用Python做股票量化分析 (Part4: 第9-11章+附录) |
| author_or_source | 作者：阿布 |
| material_type | 技术书籍（Python量化交易机器学习+附录） |
| domain_tags | 量化交易, Python, 机器学习, sklearn, 回测度量, 相关性分析, 技术指标, 环境部署 |
| file_scope | 第9章（度量与优化）+ 第10章（机器学习·猪老三）+ 第11章（机器学习·abu）+ 附录A/B/C |
| source_file_size_mb | ~50MB（PDF文字版） |
| retain_mode | EXCERPT_RETAIN |

---

# ROUTING_DECISION

| field | value |
|-------|-------|
| current_repo_role | A_SHARES_DATA_ENGINEERING_GUARD |
| quantizable_now_ratio_estimate | 70% |
| needs_extra_data_ratio_estimate | 30% |
| biggest_leakage_risks | 1) 书中机器学习示例基于构造的"猪老三世界"股价，非真实市场规律；2) 第10章结论明确"预测股价涨跌不可能"，但第11章Ump模块通过概率拦截仍有价值；3) A股环境部署需切换数据源和缓存格式；4) 附录A的abu版本可能与当前Git版本不一致；5) 相关性/技术指标需适配A股数据频率 |

---

# CONTENT_CLUSTERS

## 1. 回测度量与基础指标
- what_it_is: 策略收益、年化收益、胜率、盈亏比、夏普比率、信息比率、阿尔法、贝塔、最大回撤、资金利用率等核心度量指标
- keep_level: 高
- repo_mapping: A_SHARES_DATA_ENGINEERING_GUARD / 绩效归因模块
- evidence_status: 来自原文

## 2. Grid Search参数优化
- what_it_is: 对买入/卖出因子参数进行排列组合，使用WrsmScorer综合评分寻找最优参数
- keep_level: 高
- repo_mapping: A_SHARES_DATA_ENGINEERING_GUARD / 参数优化模块
- evidence_status: 来自原文

## 3. 资金限制与满仓乘数
- what_it_is: 全市场回测中资金不足导致成交比例低，通过满仓乘数使策略与基准可比
- keep_level: 高
- repo_mapping: A_SHARES_DATA_ENGINEERING_GUARD / 资金管理模块
- evidence_status: 来自原文

## 4. 中文自动生成交易策略
- what_it_is: gen_buy_from_chinese()通过中文描述生成Python策略代码
- keep_level: 中
- repo_mapping: A_SHARES_DATA_ENGINEERING_GUARD / 策略生成器
- evidence_status: 来自原文

## 5. 机器学习基础（分类/回归/聚类）
- what_it_is: 使用sklearn进行股价涨跌预测：线性回归、多项式回归、AdaBoost、RandomForest、SVM、逻辑回归、KMeans
- keep_level: 高
- repo_mapping: A_SHARES_FEATURE_POOL / 机器学习模块
- evidence_status: 来自原文

## 6. 特征工程与模型评估
- what_it_is: 特征标准化、交叉验证、混淆矩阵、ROC曲线、学习曲线、特征重要度、RFE特征筛选
- keep_level: 高
- repo_mapping: A_SHARES_FEATURE_POOL / 特征工程
- evidence_status: 来自原文

## 7. abuML封装与回测特征生成
- what_it_is: AbuML封装sklearn API，回测时自动生成deg_ang、price_rank、wave_score等特征
- keep_level: 高
- repo_mapping: A_SHARES_DATA_ENGINEERING_GUARD / 特征自动生成
- evidence_status: 来自原文

## 8. Ump裁判模块（主裁）
- what_it_is: 使用GMM对回测交易进行无监督聚类，识别失败概率>65%的分类簇并拦截新交易
- keep_level: 高
- repo_mapping: A_SHARES_DATA_ENGINEERING_GUARD / 机器学习风控
- evidence_status: 来自原文

## 9. Ump裁判模块（边裁）
- what_it_is: 基于训练集top win/top loss边缘数据，通过pairwise_distances相似度匹配对新交易投票拦截
- keep_level: 高
- repo_mapping: A_SHARES_DATA_ENGINEERING_GUARD / 非均衡风控
- evidence_status: 来自原文

## 10. 深度学习K线图预测
- what_it_is: 使用K线快照图片训练深度学习模型分类交易盈亏，书中结论为"现阶段基本不可用于实盘"
- keep_level: 中
- repo_mapping: A_SHARES_FEATURE_POOL / 深度学习实验
- evidence_status: 来自原文

## 11. 附录A：量化环境部署
- what_it_is: Anaconda/conda/pip环境管理，abu量化系统安装，A股/港股/美股市场切换
- keep_level: 中
- repo_mapping: A_SHARES_DATA_ENGINEERING_GUARD / 基础设施
- evidence_status: 来自原文

## 12. 附录B：相关性分析
- what_it_is: 皮尔逊相关系数、斯皮尔曼秩相关系数、相关与协整选股策略
- keep_level: 中
- repo_mapping: A_SHARES_FEATURE_POOL / 统计工具
- evidence_status: 来自原文

## 13. 附录C：统计分析及技术指标
- what_it_is: 跳空缺口统计、时间加权jump_line、BOLL/MACD/MA技术指标可视化
- keep_level: 中
- repo_mapping: A_SHARES_FEATURE_POOL / 技术分析
- evidence_status: 来自原文

---

# QUANTIZATION_TABLE

| concept | type | minimal_definition | observable_proxy | min_data_requirement | confirmation_timing | quant_status | repo_target | leakage_risk | notes |
|---------|------|-------------------|------------------|---------------------|---------------------|--------------|-------------|--------------|-------|
| 策略收益 | 度量 | (Pend-Pstart)/Pstart*100% | 最终资产/初始资产 | 每日资产 | 回测后 | proxy_quantizable_now | 绩效归因 | 未考虑资金规模 | 大资金需冲击成本调整 |
| 策略年化收益 | 度量 | ((1+P)^(252/n)-1)*100% | 策略收益与天数 | 收益+天数 | 回测后 | proxy_quantizable_now | 绩效归因 | 复利假设 | A股用250天 |
| 胜率 | 度量 | 盈利次数/总交易次数 | order.result统计 | 交易记录 | 回测后 | proxy_quantizable_now | 绩效归因 | 样本外偏差 | 需交叉验证 |
| 盈亏比 | 度量 | 盈利总和/亏损总和 | order.profit | 交易记录 | 回测后 | proxy_quantizable_now | 绩效归因 | 极端值扭曲 | 结合胜率使用 |
| 夏普比率 | 度量 | (年化收益-无风险利率)/波动率 | cum_returns/volatility | 日收益率 | 回测后 | proxy_quantizable_now | 绩效归因 | 分布敏感 | 与基准对比 |
| 信息比率 | 度量 | (策略年化-基准年化)/跟踪误差 | 超额收益/标准差 | 策略+基准日收益 | 回测后 | needs_extra_data | 绩效归因 | 基准选择 | 风格匹配基准 |
| 阿尔法/贝塔 | 度量 | 超额收益/市场敏感度 | 回归系数 | 策略+基准日收益 | 回测后 | needs_extra_data | 绩效归因 | 市场结构变化 | 需滚动计算 |
| 最大回撤 | 度量 | 峰值到谷底最大亏损 | capital_blance | 资金曲线 | 回测后 | proxy_quantizable_now | 绩效归因 | 未来可能更大 | 关注持续时间 |
| 满仓乘数 | 调整 | algorithm_returns * (1/stocks_rate) | 持仓比例倒数 | 持仓比例 | 回测后 | proxy_quantizable_now | 绩效归因 | 虚拟调整 | 无法真实提高收益 |
| Grid Search | 优化 | 参数排列组合+评分排序 | 参数组合数*评分 | 多组回测结果 | 参数优化 | proxy_quantizable_now | 参数优化 | 过拟合 | 需交叉验证 |
| WrsmScorer | 评分 | 胜率/收益/夏普/回撤加权 | 0-1标准化排序 | 回测度量 | 参数优化 | proxy_quantizable_now | 评分模型 | 权重主观 | 可自定义权重 |
| 线性回归预测 | ML | sklearn.LinearRegression.fit(X,y) | RMSE | 特征+标签 | 训练后 | proxy_quantizable_now | ML模块 | 线性假设 | 可用多项式扩展 |
| 随机森林预测 | ML | RandomForestRegressor/Classifier | RMSE/Accuracy | 特征+标签 | 训练后 | proxy_quantizable_now | ML模块 | 过拟合 | n_estimators调参 |
| AdaBoost预测 | ML | AdaBoostRegressor | RMSE | 特征+标签 | 训练后 | proxy_quantizable_now | ML模块 | 对异常值敏感 | 需迭代次数控制 |
| SVM分类 | ML | SVC(kernel='rbf') | Accuracy | 特征+标签 | 训练后 | proxy_quantizable_now | ML模块 | 核函数选择 | rbf适用于非线性 |
| 逻辑回归分类 | ML | LogisticRegression | Accuracy | 特征+标签 | 训练后 | proxy_quantizable_now | ML模块 | 线性边界 | 需正则化参数调优 |
| KMeans聚类 | ML | KMeans(n_clusters=2) | 簇内方差 | 特征 | 训练后 | proxy_quantizable_now | ML模块 | 簇数预设 | 可用轮廓系数评估 |
| PCA降维 | ML | PCA(n_components=2) | 方差保留率 | 特征 | 训练后 | proxy_quantizable_now | ML模块 | 信息损失 | 可视化常用 |
| 特征重要度 | ML | feature_importances_ | 特征排序 | 训练后模型 | 训练后 | proxy_quantizable_now | 特征工程 | 模型依赖 | 不同模型结果不同 |
| RFE特征筛选 | ML | RFE(estimator) | ranking/support | 特征+标签 | 训练后 | proxy_quantizable_now | 特征工程 | 递归耗时 | 适合特征数中等 |
| GMM主裁聚类 | ML | GMM(component).fit(X) | 分类簇失败率 | 交易特征 | 训练后 | needs_extra_data | 风控模块 | 簇数选择 | 默认40-85 |
| 角度主裁拦截 | ML | deg_ang21/42/60/252 GMM聚类 | 失败率>65%簇 | 回测特征 | 训练后 | needs_extra_data | 风控模块 | 特征有限 | 可扩展更多特征 |
| 跳空主裁拦截 | ML | jump_up/down_power GMM聚类 | 失败率>65%簇 | 回测特征 | 训练后 | needs_extra_data | 风控模块 | 异常值敏感 | 结合价格验证 |
| 价格主裁拦截 | ML | price_rank60/90/120/252 GMM聚类 | 失败率>65%簇 | 回测特征 | 训练后 | needs_extra_data | 风控模块 | 突破信号固有 | 需长周期验证 |
| 波动主裁拦截 | ML | wave_score1/2/3 GMM聚类 | 失败率>65%簇 | 回测特征 | 训练后 | needs_extra_data | 风控模块 | 高波动偏差 | 结合跳空验证 |
| 全局最优筛选 | 优化 | brute(min_func) | 最优参数[lps,lms,lrs] | 分类簇统计 | 训练后 | proxy_quantizable_now | 风控模块 | 局部最优 | 可用更优算法 |
| 边裁相似度匹配 | ML | pairwise_distances+np.corrcoef | 相似度>0.91 | 训练集+新交易 | 预测时 | needs_extra_data | 风控模块 | 阈值敏感 | 多阈值级联 |
| 边裁非均衡投票 | ML | top_win/loss cnt * 0.618 > 对方 | 投票结果 | 相似交易rk | 预测时 | needs_extra_data | 风控模块 | 比例主观 | K_EDGE_JUDGE_RATE |
| 皮尔逊相关系数 | 统计 | Cov(X,Y)/Std(X)Std(Y) | np.corrcoef | 两序列 | 计算时 | proxy_quantizable_now | 统计工具 | 线性相关 | 对非线性失效 |
| 斯皮尔曼秩相关 | 统计 | rank(X)与rank(Y)相关 | stats.spearmanr | 两序列 | 计算时 | proxy_quantizable_now | 统计工具 | 单调相关 | 对异常值稳健 |
| 协整选股 | 统计 | 序列差值围绕均值波动 | coint_similar() | 两序列 | 计算时 | needs_extra_data | 统计套利 | 样本期选择 | 适合配对交易 |
| 跳空缺口统计 | 技术 | calc_jump()可视化 | jump_power | K线数据 | 计算时 | proxy_quantizable_now | 技术分析 | 阈值固定 | 建议时间加权 |
| 时间加权缺口 | 技术 | calc_jump_line_weight(sw) | 加权jump_power | K线数据 | 计算时 | proxy_quantizable_now | 技术分析 | 权重分配 | sw=(0.5,0.5) |
| BOLL指标 | 技术 | 布林带中轨+上下轨 | 价格位置 | K线数据 | 计算时 | proxy_quantizable_now | 技术分析 | 滞后性 | 结合其他指标 |
| MACD指标 | 技术 | DIF-DEA柱状图 | 金叉死叉 | K线数据 | 计算时 | proxy_quantizable_now | 技术分析 | 滞后性 | 需参数调优 |
| MA均线 | 技术 | 多周期移动平均 | 均线交叉 | K线数据 | 计算时 | proxy_quantizable_now | 技术分析 | 滞后性 | 常用10/20/30/60/90/120 |
| 市场切换 | 配置 | g_market_target=CN/HK/US | 佣金/交易日/股数 | 市场规则 | 配置时 | proxy_quantizable_now | 基础设施 | 规则变化 | 需持续关注 |
| 数据缓存 | 配置 | E_DATA_CACHE_HDF5/CSV/MONGODB | 读写速度 | 硬件环境 | 配置时 | proxy_quantizable_now | 基础设施 | 硬件依赖 | 固态硬盘用HDF5 |
| 强制本地缓存 | 配置 | E_DATA_FETCH_FORCE_LOCAL | 数据一致性 | 历史数据 | 回测时 | proxy_quantizable_now | 基础设施 | 数据陈旧 | 定期更新 |
| 全市场数据更新 | 配置 | abu.run_kl_update() | 更新进度 | 全市场symbol | 维护时 | proxy_quantizable_now | 基础设施 | 耗时 | 多线程/进程优化 |


---

# RETAINED_EXCERPTS

### EXCERPT_P4_01
- **source_hint**: 第9章 - 度量基础概念
- **quote**: `策略收益(P) = (Pend - Pstart) / Pstart * 100%。Pend=统计周期内最后股票和现金的总价值，Pstart=统计周期内最初股票和现金的总价值。策略年化收益 = ((1+P)^(252/n)-1)*100%，P=策略收益，n=策略执行天数。注：252是美股交易一年内天数，如果是a股则为250天。胜率：统计周期内所有投资盈利次数/统计周期内所有交易次数；盈亏比：统计周期内所有投资盈利单的盈利之和/统计周期内所有亏损单的亏损之和；平均获利期望：统计周期内所有投资盈利单的平均获利比例；平均亏损期望：统计周期内所有投资亏损单的平均亏损比例。`
- **why_kept**: 所有核心度量指标的标准定义，含A股250天修正
- **quant_link**: 绩效度量

### EXCERPT_P4_02
- **source_hint**: 第9章 - 度量输出示例
- **quote**: `买入后卖出的交易数量：67 胜率：55.22% 平均获利期望：14.11% 平均亏损期望：-7.7% 盈亏比：2.3543 策略收益：50.44% 基准收益：15.66% 策略年化收益：25.22% 基准年化收益：7.83% 策略买入成交比例：80.0% 策略共执行504个交易日`
- **why_kept**: 完整回测度量输出示例，所有关键指标数值
- **quant_link**: 绩效度量

### EXCERPT_P4_03
- **source_hint**: 第9章 - 夏普与波动率
- **quote**: `夏普比率 = (Rp - Rf) / σp。Rp=策略年化收益率，Rf=无风险利率（默认0），σp=策略收益波动率。信息比率 = (Rp - Rm) / σf。Rp=策略年化收益率，Rm=基准年化收益率，σf=策略与基准日收益差值的年化标准差。Alpha = α = Rp - [Rf + βp*(Rm-Rf)]。Beta = βp = Cov(Dp,Dm)/Var(Dm)。`
- **why_kept**: 夏普比率、信息比率、阿尔法、贝塔的数学定义
- **quant_link**: 风险指标

### EXCERPT_P4_04
- **source_hint**: 第9章 - 月度收益目标警示
- **quote**: `print('平均每月目标收益5%，一年总收益{}'.format(0.05*12)) print('100万本金，年收益60%，20年复利总收益{}'.format(round(1000000*(1+0.60)**20))) 输出：平均每月目标收益5%，一年总收益0.6。100万本金，年收益60%，20年复利总收益12089258196.0。`
- **why_kept**: 收益目标警示案例：月收益5%看似不高，但20年复利达120亿，说明高预期收益不现实
- **quant_link**: 收益预期

### EXCERPT_P4_05
- **source_hint**: 第9章 - Grid Search参数范围
- **quote**: `stop_win_range = np.arange(2.0, 4.5, 0.5) stop_loss_range = np.arange(0.5, 2, 0.5) sell_atr_nstop_factor_grid = {'class': [AbuFactorAtrNStop], 'stop_loss_n': stop_loss_range, 'stop_win_n': stop_win_range} close_atr_range = np.arange(1.0, 4.0, 0.5) pre_atr_range = np.arange(1.0, 3.5, 0.5)`
- **why_kept**: 卖出因子参数Grid Search范围定义示例
- **quant_link**: 参数优化

### EXCERPT_P4_06
- **source_hint**: 第9章 - Grid Search执行
- **quote**: `grid_search = GridSearch(read_cash, choice_symbols, buy_factors_product=buy_factors_product, sell_factors_product=sell_factors_product) scores, score_tuple_array = grid_search.fit(n_jobs=-1) print('组合因子参数数量{}'.format(len(buy_factors_product)*len(sell_factors_product))) print('最终评分结果数量{}'.format(len(scores))) 输出：组合因子参数数量1431，最终评分结果数量1431`
- **why_kept**: GridSearch执行及参数组合数量验证，1431种组合全遍历
- **quant_link**: 参数优化

### EXCERPT_P4_07
- **source_hint**: 第9章 - 最优参数结果
- **quote**: `best_score_tuple_grid = grid_search.best_score_tuple_grid AbuMetricsBase.show_general(best_score_tuple_grid.orders_pd, best_score_tuple_grid.action_pd, best_score_tuple_grid.capital, best_score_tuple_grid.benchmark) 买入后卖出的交易数量：38 胜率：60.53% 平均获利期望：13.45% 平均亏损期望：-6.06% 盈亏比：3.2382 策略收益：31.58% 基准收益：15.66% 策略年化收益：15.79% 基准年化收益：7.83% 策略买入成交比例：100.0%`
- **why_kept**: Grid Search最优参数结果展示，胜率60.53%、盈亏比3.24
- **quant_link**: 参数优化

### EXCERPT_P4_08
- **source_hint**: 第9章 - 评分机制核心
- **quote**: `class AbuBaseScorer: for ind, score_tuple in enumerate(self.score_tuple_array): metrics = AbuMetricsBase(score_tuple.orders_pd, score_tuple.action_pd, score_tuple.capital, score_tuple.benchmark) metrics.fit_metrics() self.score_dict[ind] = self.select_score_func(metrics) score_pd = pd.DataFrame(self.score_dict).T score_pd.columns = self.columns_name score_ls = np.linspace(0, 1, score_pd.shape[0]) for cn in self.columns_name: score = score_ls[(score_pd[cn].rank().values - 1).astype(int)] score_pd['score_' + cn] = score score_pd['score'] = scores.apply(lambda s: (s*self.weights).sum(), axis=1)`
- **why_kept**: 评分核心逻辑：每项度量排序后0-1标准化，再按权重求和
- **quant_link**: 评分模型

### EXCERPT_P4_09
- **source_hint**: 第9章 - 不同权重评分
- **quote**: `scorer = WrsmScorer(score_tuple_array, weights=[0,1,0,0]) # 只考虑投资回报 best_score_tuple_grid = score_tuple_array[scorer_returns_max.index[-1]] AbuMetricsBase.show_general(...) 买入后卖出的交易数量：67 胜率：55.22% 平均获利期望：14.11% 平均亏损期望：-7.7% 盈亏比：2.3543 策略收益：50.44% 基准收益：15.66% 策略年化收益：25.22%`
- **why_kept**: 只考虑收益权重时最优结果为50.44%收益，与默认权重31.58%对比
- **quant_link**: 评分模型

### EXCERPT_P4_10
- **source_hint**: 第9章 - 资金限制影响
- **quote**: `read_cash = 2000000 abupy.beta.atr.g_atr_pos_base = 0.0015 abu_result_tuple, _ = abu.run_loop_back(read_cash, buy_factors, sell_factors, stock_pickers, choice_symbols=None, n_folds=5) abu_result_tuple.action_pd.deal.value_counts() False 109671 True 54635 策略买入成交比例：32.57% 策略资金利用率比例：86.31%`
- **why_kept**: 全市场回测资金不足导致仅1/3成交，资金利用率86%
- **quant_link**: 资金管理

### EXCERPT_P4_11
- **source_hint**: 第9章 - 满仓乘数解决方案
- **quote**: `self.stocks_full_rate_factor = 1 if self.enable_stocks_full_rate_factor: stocks_full_rate = (self.capital.capital_pd.stocks_blance / self.capital.capital_pd.capital_blance) stocks_full_rate[stocks_full_rate == 0] = 1 self.stocks_full_rate_factor = (1 / stocks_full_rate) self.algorithm_returns = np.round(self.capital.capital_pd['capital_blance'].pct_change(), 3) * self.stocks_full_rate_factor`
- **why_kept**: 满仓乘数实现：使策略收益曲线与基准同量级可比
- **quant_link**: 度量调整

### EXCERPT_P4_12
- **source_hint**: 第9章 - 中文策略生成
- **quote**: `init_self_code = {'类名称': 'AbuChineseGen', '类变量': [('连续下跌买入阀值天数', {'默认': 3}), ('计数连续下跌的天数', {'默认': 0})]} fit_day_code = ['如果|今天.收盘<昨天.收盘|计数连续下跌的天数+=1', '否则：计数连续下跌的天数=0', '如果|计数连续下跌的天数>=连续下跌买入阀值天数|买入&计数连续下跌的天数=0'] gen_code = abu.gen_buy_from_chinese(init_self_code, fit_day_code) 输出：class AbuChineseGen(AbuFactorBuyBase): def __init__(self, **kwargs): self.a = 3; self.b = 0; self.factor_name = '{}:{}:{}'.format(self.__class__.__name__, self.a, self.b) def fit_day(self, today): ... if b < d: self.b += 1 else: self.b = 0 if self.b >= self.a: order = self.make_buy_order(day_ind); self.b = 0; return order return None`
- **why_kept**: 中文描述自动生成Python策略代码的完整流程
- **quant_link**: 策略生成

### EXCERPT_P4_13
- **source_hint**: 第10章 - 机器学习基础概念
- **quote**: `机器学习按应用场景分为3类：有监督机器学习(Supervised learning)；无监督机器学习(Unsupervised learning)；强化学习(Reinforcement learning)。给定数据集和对应的标签X-y，训练模型，预测输出，这是有监督机器学习。不关心有没有标签y，只是挖掘数据集X的一些内在规律，这是无监督机器学习。在固定的场景下，机器在环境(Environment)中学习到策略(Strategy)，按策略选择一个动作(Action)，目标是让对应的回报(Reward)最大，这是强化学习。`
- **why_kept**: 机器学习三大分类的清晰定义
- **quant_link**: 机器学习基础

### EXCERPT_P4_14
- **source_hint**: 第10章 - 猪老三世界股价生成
- **quote**: `def gen_another_word_price_rule(yesterday_close, yesterday_volume, bf_yesterday_close, bf_yesterday_volume, today_volume, date_week): price_change = yesterday_close - bf_yesterday_close; volume_change = yesterday_volume - bf_yesterday_volume sign = 1.0 if price_change * volume_change > 0 else -1.0 gen_noise = today_volume > np.max([yesterday_volume, bf_yesterday_volume]) if gen_noise and date_week == 4: sign = -1.0 elif gen_noise and date_week == 0: sign = 1.0 price_base = abs(price_change); price_factor = np.mean([today_volume/yesterday_volume, today_volume/bf_yesterday_volume]) if abs(price_base * price_factor) < yesterday_close * 0.10: today_price = yesterday_close + sign * price_base * price_factor else: today_price = yesterday_close + sign * yesterday_close * 0.10 return today_price`
- **why_kept**: 构造"猪老三世界"股价的规则函数，量价一致则涨否则跌，周五噪音下跌周一噪音上涨
- **quant_link**: 走势生成

### EXCERPT_P4_15
- **source_hint**: 第10章 - 特征工程
- **quote**: `kl_another_word['feature_price_change'] = kl_another_word['yesterday_close'] - kl_another_word['bf_yesterday_close'] kl_another_word['feature_volume_Change'] = kl_another_word['yesterday_volume'] - kl_another_word['bf_yesterday_volume'] kl_another_word['feature_sign'] = np.sign(kl_another_word['feature_price_change'] * kl_another_word['feature_volume_Change']) kl_another_word['feature_date_week'] = kl_another_word['date_week'] kl_another_word['feature_volume_noise'] = kl_another_word['yesterday_volume'] * kl_another_word['bf_yesterday_volume'] kl_another_word['feature_price_noise'] = kl_another_word['yesterday_close'] * kl_another_word['bf_yesterday_close']`
- **why_kept**: 猪老三特征工程：价格差、成交量差、涨跌符号、周几、噪音特征
- **quant_link**: 特征工程

### EXCERPT_P4_16
- **source_hint**: 第10章 - 线性回归预测
- **quote**: `from sklearn.linear_model import LinearRegression from sklearn import cross_validation def regress_process(estimator, train_x, train_y_regress, test_x, test_y_regress): estimator.fit(train_x, train_y_regress) test_y_prdict_regress = estimator.predict(test_x) plt.plot(test_y_regress.cumsum()); plt.plot(test_y_prdict_regress.cumsum()) scores = cross_validation.cross_val_score(estimator, train_x, train_y_regress, cv=10, scoring='mean_squared_error') mean_sc = np.mean(np.sqrt(-scores)); print('RMSE:' + str(mean_sc)) estimator = LinearRegression() regress_process(estimator, train_x, train_y_regress, test_x, test_y_regress) 输出：RMSE: 0.0260964344834`
- **why_kept**: 线性回归预测股价涨跌幅度，RMSE=0.026，交叉验证
- **quant_link**: 回归预测

### EXCERPT_P4_17
- **source_hint**: 第10章 - 多项式回归与集成学习
- **quote**: `from sklearn.pipeline import make_pipeline from sklearn.preprocessing import PolynomialFeatures estimator = make_pipeline(PolynomialFeatures(degree=3), LinearRegression()) regress_process(estimator, train_x, train_y_regress, test_x, test_y_regress) 输出：RMSE: 0.0242783959238 from sklearn.ensemble import AdaBoostRegressor estimator = AdaBoostRegressor(n_estimators=100) regress_process(...) 输出：RMSE: 0.0236202304171 from sklearn.ensemble import RandomForestRegressor estimator = RandomForestRegressor(n_estimators=100) regress_process(...) 输出：RMSE: 0.0195852583561`
- **why_kept**: 多项式回归、AdaBoost、RandomForest对比，RMSE逐步降低
- **quant_link**: 集成学习

### EXCERPT_P4_18
- **source_hint**: 第10章 - 分类预测
- **quote**: `from sklearn.linear_model import LogisticRegression from sklearn import metrics def classification_process(estimator, train_x, train_y_classification, test_x, test_y_classification): estimator.fit(train_x, train_y_classification) test_y_prdict_classification = estimator.predict(test_x) print("{} accuracy= {:.2f}".format(estimator.__class__.__name__, metrics.accuracy_score(test_y_classification, test_y_prdict_classification))) scores = cross_validation.cross_val_score(estimator, train_x, train_y_classification, cv=10, scoring='accuracy') print('cross validation accuracy mean: {:.2f}'.format(np.mean(scores))) estimator = LogisticRegression(C=1.0, penalty='l1', tol=1e-6) 输出：LogisticRegression accuracy= 0.93 cross validation accuracy mean: 0.92`
- **why_kept**: 逻辑回归分类预测涨跌，准确率93%，交叉验证92%
- **quant_link**: 分类预测

### EXCERPT_P4_19
- **source_hint**: 第10章 - SVM与RandomForest分类
- **quote**: `from sklearn.svm import SVC estimator = SVC(kernel='rbf') classification_process(estimator, train_x, train_y_classification, test_x, test_y_classification) 输出：SVC accuracy= 0.94 cross validation accuracy mean: 0.92 from sklearn.ensemble import RandomForestClassifier estimator = RandomForestClassifier(n_estimators=100) classification_process(...) 输出：RandomForestClassifier accuracy= 0.93 cross validation accuracy mean: 0.92`
- **why_kept**: SVM和RandomForest分类对比，准确率均约93%
- **quant_link**: 分类预测

### EXCERPT_P4_20
- **source_hint**: 第10章 - 混淆矩阵
- **quote**: `def confusion_matrix_with_report(test_y, predictions): confusion_matrix = metrics.confusion_matrix(test_y, predictions) print("Predicted"); print("| 0 | 1 |"); print("|-----|-----|"); print("0 | %3d | %3d |" % (confusion_matrix[0,0], confusion_matrix[0,1])) print("Actual |-----|-----|"); print("1 | %3d | %3d |" % (confusion_matrix[1,0], confusion_matrix[1,1])) print(metrics.classification_report(test_y, predictions)) 输出：0 | 903 | 73 | 1 | 84 | 948 | precision recall f1-score support 0 0.91 0.93 0.92 976 1 0.93 0.92 0.92 1032`
- **why_kept**: 混淆矩阵及classification_report展示，假阳假阴约10%
- **quant_link**: 模型评估

### EXCERPT_P4_21
- **source_hint**: 第10章 - 特征重要度
- **quote**: `def importances_coef_pd(estimator): if hasattr(estimator, 'feature_importances_'): return pd.DataFrame({'feature': list(pig_three_feature.columns[1:]), 'importance': estimator.feature_importances_}).sort_values('importance') estimator = RandomForestClassifier(n_estimators=100) estimator.fit(train_x, train_y_classification) importances_coef_pd(estimator) 输出：feature importance feature_price_noise 0.052230 feature_volume_noise 0.053481 feature_price_change 0.094741 feature_volume_Change 0.094907 feature_date_week 0.095468 feature_sign 0.609173`
- **why_kept**: RandomForest特征重要度排序，sign特征最重要(0.609)，噪音特征最小
- **quant_link**: 特征工程

### EXCERPT_P4_22
- **source_hint**: 第10章 - RFE特征筛选
- **quote**: `from sklearn.feature_selection import RFE def feature_selection(estimator, x, y): selector = RFE(estimator) selector.fit(x, y) print('RFE selection') print(pd.DataFrame({'support': selector.support_, 'ranking': selector.ranking_}, index=pig_three_feature.columns[1:])) feature_selection(estimator, train_x, train_y_classification) 输出：feature_price_change 1 True feature_volume_Change 1 True feature_sign 1 True feature_date_week 2 False feature_volume_noise 3 False feature_price_noise 4 False`
- **why_kept**: RFE特征筛选结果：价格变化、成交量变化、涨跌符号保留，周几和噪音特征剔除
- **quant_link**: 特征工程

### EXCERPT_P4_23
- **source_hint**: 第10章 - KMeans聚类提高正确率
- **quote**: `pig_three_kmean_feature = kl_another_word_feature_test pig_three_kmean_feature['y'] = test_y_classification pig_three_kmean_feature['y_prdict'] = test_y_prdict_classification pig_three_kmean_feature['y_same'] = np.where(pig_three_kmean_feature['y'] == pig_three_kmean_feature['y_prdict'], 1, 0) x_kmean = pig_three_kmean_feature.values kmean = KMeans(n_clusters=2) kmean.fit(x_kmean) pig_three_kmean_feature['cluster'] = kmean.predict(x_kmean) pig_three_kmean_feature['feature_date_week'] = kl_another_word_feature_test['feature_date_week'] pd.crosstab(pig_three_kmean_feature.feature_date_week, pig_three_kmean_feature.cluster) 输出：cluster 0 1 feature_date_week 0 77 18 1 103 0 2 104 0 3 100 0 4 85 15`
- **why_kept**: KMeans聚类发现周一和周五预测失败率最高，可通过降低这两天交易频率提高战绩
- **quant_link**: 聚类分析

### EXCERPT_P4_24
- **source_hint**: 第10章 - abuML封装
- **quote**: `from abupy import AbuML ml = AbuML(train_x, train_y_classification, pig_three_feature) ml.estimator.random_forest_classifier() ml.cross_val_accuracy_score() 输出：accuracy mean: 0.91883391499 ml.feature_selection() 输出：feature_price_change 1 True feature_volume_Change 1 True feature_sign 1 True feature_date_week 2 False feature_volume_noise 3 False feature_price_noise 4 False`
- **why_kept**: abuML封装sklearn API，一行代码完成交叉验证和特征筛选
- **quant_link**: 机器学习封装

### EXCERPT_P4_25
- **source_hint**: 第10章 - 回测特征生成
- **quote**: `def make_buy_order_ml_feature(self, day_ind): ml_feature_dict = {} ml_feature_dict.update(ABuMLFeature.calc_price_rank_feature(self.kl_pd, self.pre_kl_pd, day_ind)) ml_feature_dict.update(ABuMLFeature.calc_deg_feature(self.kl_pd, self.pre_kl_pd, day_ind)) ml_feature_dict.update(ABuMLFeature.calc_wave_feature(self.kl_pd, self.pre_kl_pd, day_ind)) ml_feature_dict.update(ABuMLFeature.calc_atr_feature(self.kl_pd, self.pre_kl_pd, day_ind)) ml_feature_dict.update(ABuMLFeature.calc_jump_feature(self.kl_pd, self.pre_kl_pd, day_ind)) if ABuEnv.g_enable_take_kl_snapshot: ml_feature_dict.update(ABuMLFeature.take_kl_snapshot(self.kl_pd, self.pre_kl_pd, day_ind)) return ml_feature_dict`
- **why_kept**: 回测中自动生成机器学习特征：价格位置、角度、波动、ATR、跳空、快照
- **quant_link**: 特征自动生成

### EXCERPT_P4_26
- **source_hint**: 第10章 - 训练测试集切分
- **quote**: `def market_train_test_split(choice_symbols): market_symbols, test_symbols = ABuSymbol.market_train_test_split(market_symbols=choice_symbols) ABuFileUtil.dump_pickle(test_symbols, K_MARKET_TEST_FN) ABuFileUtil.dump_pickle(market_symbols, K_MARKET_TRAIN_FN) return market_symbols abupy.env.g_enable_ml_feature = True abupy.env.g_enable_train_test_split = True abu_result_tuple, kl_pd_manger = abu.run_loop_back(read_cash, buy_factors, sell_factors, stock_pickers, choice_symbols=None, n_folds=5) 买入后卖出的交易数量：80261 胜率：44.2% 策略收益：58.05% 基准收益：77.87%`
- **why_kept**: 回测中自动切分训练/测试集(9:1)，生成机器学习特征，全市场回测结果
- **quant_link**: 数据切分

### EXCERPT_P4_27
- **source_hint**: 第10章 - 深度学习结论
- **quote**: `将abupy.env.g_enable_take_kl_snapshot开关打开后，将在每一个买入单子成交后，生成买入股票时的K线快照在本地。如果通过大量的策略回测，生成大量买入时刻交易快照图片，通过回测结果将图片分成两组，即结果盈利的交易快照图片为一组，亏损的交易快照图片为另一组，将两组图片输入深度学习模型进行训练。结论：现阶段基本不可用于实盘。使用K线图进行深度学习的稳定性不够好；训练拟合度不容易把握，很容易过拟合。`
- **why_kept**: 深度学习K线图预测交易盈亏的实验结论：现阶段不可用于实盘
- **quant_link**: 深度学习

### EXCERPT_P4_28
- **source_hint**: 第10章 - 预测市场的混沌
- **quote**: `量化交易更倾向于投机范畴，预测肯定了确定性，概率优势不需要肯定确定性。虽然笔者认为对市场无法做到确定性预测，但是股票市场也并不是杂乱无章的，由于市场参与者的非理性行为（有效市场假说不成立），通过历史数据发现规律，一定可以获得一些概率上的优势。预测和混沌之间存在着一种状态，这种状态可以使用概率来描述，即通过算法来找到这些概率的分布，预测市场的混沌。`
- **why_kept**: 核心投资哲学：量化获取概率优势而非预测确定性，市场存在可被利用的非理性
- **quant_link**: 投资哲学

### EXCERPT_P4_29
- **source_hint**: 第11章 - 搜索引擎与量化类比
- **quote**: `量化交易和搜索引擎结果的利弊中最相似之处有两点：1) 对搜索引擎（量化策略）失败结果的人工分析，注重分析失败的结果以及是否存在改进方案；2) 机器学习技术在搜索引擎（量化策略）上的改进，必须赋予宏观上合理的解释。`
- **why_kept**: Ump模块设计哲学：分析失败交易+机器学习改进需有宏观解释
- **quant_link**: 风控设计

### EXCERPT_P4_30
- **source_hint**: 第11章 - Ump裁判模块架构
- **quote**: `ump将策略回测交易结果作为训练集进行模式识别，特别针对失败的交易识别模式寻找规律，通过非均衡技术进一步寻找概率上的优势，通过构建多个裁判员的方式构建裁判（主裁、边裁）机制，来对新的交易进行识别，当新的交易失败的风险大于一定的概率的时候，放弃这次交易。`
- **why_kept**: Ump模块核心架构说明：主裁+边裁机制，对失败交易模式识别
- **quant_link**: 风控架构

### EXCERPT_P4_31
- **source_hint**: 第11章 - 主裁GMM实现
- **quote**: `K_DEFAULT_NCS_RANG = slice(40, 85) def fit(self, p_ncs=None, threshold=0.65, show=True): ncs = p_ncs if ncs is None: ncs = np.arange(K_DEFAULT_NCS_RANG.start, K_DEFAULT_NCS_RANG.stop) df = copy.deepcopy(self.fiter().df); df['ind'] = np.arange(0, df.shape[0]); rts = {} for component in ncs: clf = GMM(component, n_iter=500, random_state=3).fit(self.fiter().x) cluster = clf.predict(self.fiter().x); df['cluster'] = cluster xt = pd.crosstab(df['cluster'], df['result']) xt = xt[xt.sum(axis=1) > 5] xt_pct = xt.div(xt.sum(1).astype(float), axis=0) if len(xt_pct[xt_pct[0] > threshold].index) > 0: rts[component] = (clf, xt_pct[xt_pct[0] > threshold].index) self.rts = rts`
- **why_kept**: 主裁核心：GMM聚类40-85个分类，识别失败率>65%的簇保存为拦截器
- **quant_link**: 主裁实现

### EXCERPT_P4_32
- **source_hint**: 第11章 - 角度主裁特征
- **quote**: `class AbuUmpMainDeg(AbuUmpMainBase): class UmpDegFiter(AbuMLPd): @ump_main_make_xy def make_xy(self, **kwarg): regex = 'result|{}'.format('|'.join(ABuMLFeature.get_deg_feature_keys())) deg_df = self.order_has_ret.filter(regex=regex) return deg_df def get_predict_col(self): return ABuMLFeature.get_deg_feature_keys() 表11-1：result deg_ang21 deg_ang42 deg_ang60 deg_ang252 2011-09-21 0 3.438 5.130 5.880 -3.677 2011-09-21 0 9.718 6.871 5.542 16.172`
- **why_kept**: 角度主裁使用21/42/60/252日拟合角度作为特征
- **quant_link**: 角度主裁

### EXCERPT_P4_33
- **source_hint**: 第11章 - 全局最优筛选
- **quote**: `def brust_min(self): cprs = self.cprs bnds = ((round(cprs['lps'].min(), 2), 0, 0.5), (round(cprs['lms'].min(), 2), 0, 0.01), (round(cprs['lrs'].min(), 2), round(cprs['lrs'].max(), 2), 0.1)) brust_result = sco.brute(self.min_func_improved, bnds, finish=None) return brust_result def min_func(self, lpmr): llps = cprs[(cprs['lps'] <= lpmr[0]) & (cprs['lms'] <= lpmr[1]) & (cprs['lrs'] >= lpmr[2])] nts_pd = pd.DataFrame() for nk in llps.index: nts_pd = nts_pd.append(nts[nk]) nts_pd = nts_pd.drop_duplicates(subset='ind', keep='last) num = nts_pd.shape[0]; loss_rate = nts_pd.result.value_counts()[0] / nts_pd.result.value_counts().sum() win_rate = 1 - loss_rate improved = (num / self.fiter.order_has_ret.shape[0]) * (loss_rate - win_rate) return np.array([improved, num])`
- **why_kept**: 全局最优筛选分类簇：获利和<=-1.29、平均获利<=-0.01、失败率>=0.65
- **quant_link**: 全局最优

### EXCERPT_P4_34
- **source_hint**: 第11章 - 主裁拦截效果
- **quote**: `def predict(self, x, need_hit_cnt=1): dump_clf_with_ind = AbuUmpMainBase.dump_clf_manager.get_ump(self) count_hit = 0 for clf, ind in dump_clf_with_ind.values(): ss = clf.predict(x) if ss == ind: count_hit += 1 if need_hit_cnt == count_hit: return 1 return 0 order_has_result['ump_deg'] = order_has_result.apply(apply_ml_features_ump, axis=1, args=(ump_deg, 2,)) 四个裁判整体拦截正确率68.3% 角度裁判拦截正确率73.83% 跳空裁判拦截正确率60.87% 波动裁判拦截正确率59.17% 价格裁判拦截正确率62.50%`
- **why_kept**: 主裁predict机制：命中need_hit_cnt个分类簇才拦截，整体正确率68.3%
- **quant_link**: 主裁验证

### EXCERPT_P4_35
- **source_hint**: 第11章 - 开启主裁拦截回测
- **quote**: `abupy.env.g_enable_ump_main_deg_block = True abupy.env.g_enable_ump_main_jump_block = True abupy.env.g_enable_ump_main_price_block = True abupy.env.g_enable_ump_main_wave_block = True abu_result_tuple_test_ump, _ = abu.run_loop_back(read_cash, buy_factors, sell_factors, stock_pickers, choice_symbols=None, n_folds=5) metric_ump = AbuMetricsBase(*abu_result_tuple_test_ump) metric_ump.fit_metrics() metric_ump.plot_order_returns_cmp(only_info=True) 买入后卖出的交易数量：8637 胜率：43.58% 盈亏比：1.1875 所有交易收益比例和：57.4217 对比未开启：8882笔，胜率43.14%，盈亏比1.1605，收益比例和48.3401`
- **why_kept**: 开启4个主裁拦截后，交易数减少245笔，胜率+0.44%，盈亏比+0.027，收益比例和+9.08
- **quant_link**: 主裁效果

### EXCERPT_P4_36
- **source_hint**: 第11章 - 边裁原理
- **quote**: `K_CG_TOP_RATE = 0.236 def fit(self): self.fiter.df['p_rk_cg'] = self.fiter.df['profit_cg'].rank() win_top = len(self.fiter.df['profit_cg']) - len(self.fiter.df['profit_cg']) * K_CG_TOP_RATE loss_top = len(self.fiter.df['profit_cg']) * K_CG_TOP_RATE self.fiter.df['rk'] = EEdgeType.E_EEdge_NORMAL.value self.fiter.df['rk'] = np.where(self.fiter.df['p_rk_cg'] > win_top, EEdgeType.E_STORE_TOP_WIN.value, self.fiter.df['rk']) self.fiter.df['rk'] = np.where(self.fiter.df['p_rk_cg'] < loss_top, EEdgeType.E_EEdge_TOP_LOSS.value, self.fiter.df['rk'])`
- **why_kept**: 边裁原理：将交易按获利比例排序，top 23.6%标记为win_top，bottom 23.6%标记为loss_top
- **quant_link**: 边裁原理

### EXCERPT_P4_37
- **source_hint**: 第11章 - 边裁预测核心
- **quote**: `K_N_TOP_SEED = 100 K_DISTANCE_THRESHOLD = 0.668 K_SIMILAR_THRESHOLD = 0.91 K_EDGE_JUDGE_RATE = 0.618 def predict(self, **kwargs): x = np.array([kwargs[col] for col in dump_clf['fiter_df'].columns[2:2+2]]) x = x.reshape(1, -1) con_x = np.concatenate((x, dump_clf['fiter_x']), axis=0) x_scale_param = self.scaler.fit(con_x); con_x = self.scaler.fit_transform(con_x, x_scale_param) distances_cx = pairwise_distances(con_x[0].reshape(1, -1), con_x[1:], metric='euclidean') if distances_cx.min() > K_DISTANCE_THRESHOLD: return EEdgeType.E_EEdge_NORMAL distances_sort = distances_cx.argsort()[:K_N_TOP_SEED] similar_cx = {arg: similar_func(con_x[0], con_x[arg+1]) for arg in distances_sort} similar_sorted = sorted(zip(similar_cx.values(), similar_cx.keys()))[::-1] similar_filters = filter(lambda sm: sm[0] > K_SIMILAR_THRESHOLD, similar_sorted)`
- **why_kept**: 边裁预测：距离阈值0.668->前100种子->相似度阈值0.91->投票
- **quant_link**: 边裁实现

### EXCERPT_P4_38
- **source_hint**: 第11章 - 边裁验证
- **quote**: `四个边裁拦截交易总数2379，拦截率26.78% 角度边裁拦截正确率61.73%，拦截交易数量776 跳空裁判拦截正确率62.83%，拦截交易数量374 波动裁判拦截正确率60.6%，拦截交易数量846 价格裁判拦截正确率60.00%，拦截交易数量865 开启主裁+边裁后：买入后卖出的交易数量：6988 胜率：44.12% 盈亏比：1.2196 所有交易收益比例和：55.9924`
- **why_kept**: 边裁拦截2379笔(26.78%)，正确率60-63%，主裁+边裁后胜率44.12%最佳
- **quant_link**: 边裁效果

### EXCERPT_P4_39
- **source_hint**: 附录A - A股回测
- **quote**: `from abupy import EMarketTargetType abupy.env.g_market_target = EMarketTargetType.E_MARKET_TARGET_CN read_cash = 8000000 abupy.beta.atr.g_atr_pos_base = 0.0015 abu_result_tuple, _ = abu.run_loop_back(read_cash, buy_factors, sell_factors, stock_pickers, choice_symbols=None, n_folds=5) 买入后卖出的交易数量：56685 胜率：46.75% 平均获利期望：14.88% 平均亏损期望：-8.25% 盈亏比：1.8294 策略收益：59.66% 基准收益：51.2% 策略年化收益：11.93% 基准年化收益：10.24% 策略买入成交比例：39.98% 策略资金利用率比例：75.5%`
- **why_kept**: A股全市场5年回测结果：策略收益59.66%，跑赢基准51.2%
- **quant_link**: A股回测

### EXCERPT_P4_40
- **source_hint**: 附录A - A股佣金计算
- **quote**: `def calc_commision_cn(trade_cnt, buy_price): cost = trade_cnt * buy_price tax = cost * 0.0003 # 印花税0.3‰ commision = cost * 0.00025 # 佣金0.25‰ commision = commision if commision > 5 else 5 commision += tax return commision def calc_commision_hk(trade_cnt, buy_price): cost = trade_cnt * buy_price tax = cost * 0.001 # 印花税1‰ commision = cost * 0.002 # 佣金2‰ commision += tax return commision`
- **why_kept**: A股和港股佣金计算公式，A股包含印花税0.3‰+佣金0.25‰，最低5元
- **quant_link**: A股交易规则

### EXCERPT_P4_41
- **source_hint**: 附录A - 数据缓存
- **quote**: `class EDataCacheType(Enum): E_DATA_CACHE_HDF5 = 0 # 读取及写入最快但非固态硬盘写入慢，存贮空间需要大 E_DATA_CACHE_CSV = 1 # 读取及写入最慢但非固态硬盘写入速度还可以，存贮空间需要较小 E_DATA_CACHE_MONGODB = 2 # 读取及写入速度一般，存贮空间需要较大 abupy.env.g_data_cache_type = EDataCacheType.E_DATA_CACHE_HDF5`
- **why_kept**: 三种数据缓存格式对比及选择建议
- **quant_link**: 基础设施

### EXCERPT_P4_42
- **source_hint**: 附录B - 皮尔逊相关系数
- **quote**: `r = Cov(X,Y) / Std(X)Std(Y)。Cov是协方差，Std是标准差。两个序列的协方差计算：Cov(X,Y) = sum((xi-ux)(yi-uy)) / (N-1)。相关系数>0说明正关系，<0说明负关系，随机序列趋于0。arr1 = np.random.rand(10000); arr2 = np.random.rand(10000) corr = np.cov(arr1, arr2) / (np.std(arr1)*np.std(arr2)) corr[0,1] 输出：-0.000561... np.corrcoef(arr1, arr2)[0,1] 输出：-0.006709...`
- **why_kept**: 皮尔逊相关系数数学定义及NumPy实现，随机序列趋于0验证
- **quant_link**: 统计工具

### EXCERPT_P4_43
- **source_hint**: 附录B - 斯皮尔曼秩相关
- **quote**: `斯皮尔曼秩相关系数针对非线性相关的相关性计算，即非线性的单调函数。在计算斯皮尔曼秩相关系数时，不使用原始序列，而是使用序列的秩。demo_list = (1, 2, 10, 100, 2, 1000) 原始序列：[1, 2, 10, 100, 2, 1000] 序列的秩：[1.0, 2.5, 4.0, 5.0, 2.5, 6.0] stats.spearmanr(arr1, arr2) 输出：SpearmanrResult(correlation=0.83056392883363928, pvalue=0.0)`
- **why_kept**: 斯皮尔曼秩相关定义及示例，对非线性单调关系有效
- **quant_link**: 统计工具

### EXCERPT_P4_44
- **source_hint**: 附录B - 协整选股
- **quote**: `ABuTLSimilar.coint_similar('usTSLA') 综合利用相关和协整的特征返回查询的股票是否有统计套利的交易机会，从整个市场中首先通过相关性分析筛选出与查询股票最相关的前100只股票作为种子，然后从这100个种子中通过与查询股票协整程度的计算来度量查询股票是否存在统计套利机会。触及最下方的线及以下时可以考虑买入股票，触及最上方线及以上的情况需考虑卖出股票。`
- **why_kept**: 协整选股策略：相关+协整，适合统计套利配对交易
- **quant_link**: 统计套利

### EXCERPT_P4_45
- **source_hint**: 附录C - 跳空缺口统计
- **quote**: `from abupy import tl jumps = tl.jump.calc_jump(tsla_df) tl.jump.calc_jump_line_weight(tsla_df, sw=(0.5, 0.5)) 缺口最大的意义在于存在很强的支撑或者阻力。calc_jump_line_weight()根据时间权重重新计算jump_power，一年前有个jump_power=2的缺口，根据时间线性加权的结果可能只有0.8了，但昨天的缺口jump_power还是2。使用time加权原因：越远的记忆越淡忘；新交易者没有之前记忆。`
- **why_kept**: 跳空缺口统计及时间加权计算，支撑阻力位识别
- **quant_link**: 技术分析

### EXCERPT_P4_46
- **source_hint**: 附录C - 技术指标可视化
- **quote**: `from abupy import nd nd.macd.plot_macd_from_order(sample_order, date_ext=252) nd.boll.plot_boll_from_order(has_result.ix[100], date_ext=252) nd.ma.plot_ma_from_order(has_result.ix[100], date_ext=252, time_period=[10, 20, 30, 60, 90, 120]) 技术指标滞后性这个特点，反而在可视化人工分析中可以更直观地发现问题。分析时同样要注意不能以偏概全，过分拟合交易行为。`
- **why_kept**: MACD、BOLL、MA均线指标结合买卖点可视化，强调滞后性用于人工分析
- **quant_link**: 技术分析

---

# FORMULAS_AND_ALGOS

## 核心度量指标公式
```
策略收益(P) = (Pend - Pstart) / Pstart * 100%
策略年化收益 = ((1+P)^(252/n)-1)*100%  # A股用250天
胜率 = 盈利次数 / 总交易次数
盈亏比 = 盈利总和 / 亏损总和
夏普比率 = (Rp - Rf) / σp
信息比率 = (Rp - Rm) / σf
Alpha = Rp - [Rf + β*(Rm-Rf)]
Beta = Cov(Dp, Dm) / Var(Dm)
最大回撤 = max(峰值 - 谷底) / 峰值
```

## Grid Search参数组合
```python
# 卖出因子参数网格
stop_win_range = np.arange(2.0, 4.5, 0.5)
stop_loss_range = np.arange(0.5, 2, 0.5)
sell_atr_nstop_factor_grid = {
    'class': [AbuFactorAtrNStop],
    'stop_loss_n': stop_loss_range,
    'stop_win_n': stop_win_range
}
close_atr_range = np.arange(1.0, 4.0, 0.5)
pre_atr_range = np.arange(1.0, 3.5, 0.5)

# 买入因子参数网格
buy_bk_factor_grid1 = {'class': [AbuFactorBuyBreak], 'xd': [42]}
buy_bk_factor_grid2 = {'class': [AbuFactorBuyBreak], 'xd': [60]}
buy_factors_product = ABuGridHelper.gen_factor_grid(
    ABuGridHelper.K_GEN_FACTOR_PARM_BUY,
    [buy_bk_factor_grid1, buy_bk_factor_grid2])
# 共3种组合：只42d、只60d、同时使用42d+60d
```

## WrsmScorer评分逻辑
```python
class WrsmScorer(AbuBaseScorer):
    def init_self_begin(self, *arg, **kwargs):
        self.select_score_func = lambda metrics: [
            metrics.win_rate,           # 胜率
            metrics.algorithm_period_returns,  # 收益
            metrics.algorithm_sharpe,   # 夏普
            metrics.max_drawdown        # 最大回撤
        ]
        self.columns_name = ['win_rate', 'returns', 'sharpe', 'max_drawdown']
        self.weights_cnt = 4
# 每项度量排序后0-1标准化，再按权重(默认等权重)求和
```

## 满仓乘数调整
```python
self.cash_utilization = 1 - (cash_blance / capital_blance).mean()
stocks_full_rate = (stocks_blance / capital_blance)
stocks_full_rate[stocks_full_rate == 0] = 1
self.stocks_full_rate_factor = (1 / stocks_full_rate)
# 调整收益：algorithm_returns * stocks_full_rate_factor
```

## GMM主裁核心
```python
K_DEFAULT_NCS_RANG = slice(40, 85)
def fit(self, p_ncs=None, threshold=0.65, show=True):
    ncs = np.arange(K_DEFAULT_NCS_RANG.start, K_DEFAULT_NCS_RANG.stop)
    for component in ncs:
        clf = GMM(component, n_iter=500, random_state=3).fit(self.fiter().x)
        cluster = clf.predict(self.fiter().x)
        xt = pd.crosstab(df['cluster'], df['result'])
        xt = xt[xt.sum(axis=1) > 5]  # 簇数量>5
        xt_pct = xt.div(xt.sum(1).astype(float), axis=0)
        if len(xt_pct[xt_pct[0] > threshold].index) > 0:
            rts[component] = (clf, xt_pct[xt_pct[0] > threshold].index)
    # 保存失败概率>65%的簇
```

## 全局最优筛选分类簇
```python
# 最优参数：lps<=-1.29, lms<=-0.01, lrs>=0.65
llps = cprs[(cprs['lps'] <= brust_min[0]) & 
            (cprs['lms'] <= brust_min[1]) & 
            (cprs['lrs'] >= brust_min[2])]
# 筛选后：101 rows -> 41 rows
# 训练集中生效拦截的数量：2084
# 拦截的交易中正确拦截比例：0.6627
# 拦截生效后可提升比例：0.0084
```

## 主裁预测拦截
```python
def predict(self, x, need_hit_cnt=1):
    count_hit = 0
    for clf, ind in dump_clf_with_ind.values():
        ss = clf.predict(x)
        if ss == ind:
            count_hit += 1
        if need_hit_cnt == count_hit:
            return 1  # 拦截
    return 0  # 不拦截
# 四个裁判整体拦截正确率68.3%
```

## 边裁非均衡投票
```python
K_N_TOP_SEED = 100
K_DISTANCE_THRESHOLD = 0.668
K_SIMILAR_THRESHOLD = 0.91
K_EDGE_JUDGE_RATE = 0.618

# 步骤：
# 1. pairwise_distances计算距离（欧氏距离）
# 2. 最小距离>0.668则判定normal
# 3. 取前100个最近种子
# 4. np.corrcoef相似度>0.91的保留
# 5. 相似交易的rk投票：-1=loss_top, 1=win_top
# 6. top_win * 0.618 > top_loss 则win，反之loss
```

## 皮尔逊相关系数
```python
arr1 = np.random.rand(10000)
arr2 = np.random.rand(10000)
corr = np.cov(arr1, arr2) / (np.std(arr1) * np.std(arr2))
# 取非对角线元素：corr[0,1]
np.corrcoef(arr1, arr2)[0,1]  # 封装函数
```

## 斯皮尔曼秩相关
```python
import scipy.stats as stats
demo_list = (1, 2, 10, 100, 2, 1000)
# 原始序列：[1, 2, 10, 100, 2, 1000]
# 序列的秩：[1.0, 2.5, 4.0, 5.0, 2.5, 6.0]
stats.spearmanr(arr1, arr2)
# 对非线性单调关系有效，对序列平移稳健
```

## A股佣金计算
```python
def calc_commision_cn(trade_cnt, buy_price):
    cost = trade_cnt * buy_price
    tax = cost * 0.0003        # 印花税0.3‰
    commision = cost * 0.00025  # 佣金0.25‰
    commision = commision if commision > 5 else 5  # 最低5元
    commision += tax
    return commision
```

---

# NOT_QUANT_YET

1. **A股实时行情接入**：书中回测使用本地缓存或沙盒数据，实盘需要实时行情API。需要extra_data：A股Level-1/Level-2行情接口、逐笔成交数据。

2. **美股到A股策略迁移**：书中示例基于美股T+0、无涨跌停，A股T+1+10%涨跌停需要策略逻辑调整。需要extra_data：A股历史涨跌停数据、T+1对策略收益影响的量化分析。

3. **机器学习特征扩展**：书中使用的角度/跳空/价格rank/波动等特征仅8个，A股实战可能需要更多特征（如北向资金、融资融券、订单簿不平衡等）。需要extra_data：另类数据源接入。

4. **Ump模块A股训练数据**：第11章Ump裁判基于美股训练，A股需要重新训练。需要extra_data：A股历史回测交易数据（含特征）、A股-specific失败交易模式。

5. **深度学习K线图数据**：书中结论为不可实盘，但如要探索需大量标注K线图。需要extra_data：A股K线图快照数据集、GPU计算资源、图像预处理pipeline。

6. **非固态硬盘数据性能**：A股全市场5000只股票数据量大，HDF5在非固态硬盘写入慢。需要extra_data：存储硬件性能基准、CSV/MongoDB替代方案对比。

7. **多进程并行效率**：全市场回测并行效率受GIL/进程通信限制。需要extra_data：C++核心模块、向量化计算方案、Spark分布式部署方案。

8. **参数过拟合跨市场验证**：Grid Search最优参数在美股有效，A股需独立验证。需要extra_data：A股不同时间段（牛市/熊市/震荡）数据、跨市场参数稳定性测试。

9. **冲击成本与流动性建模**：A股小盘股流动性差，大资金策略需考虑冲击成本。需要extra_data：A股订单簿数据、市场深度数据、VWAP执行算法。

10. **监管规则变化**：A股交易规则（如印花税调整、停牌规则）变化影响策略。需要extra_data：历史规则变化时间线、规则变化对策略影响的量化分析。

11. **策略同质化风险**：书中突破策略信号明显，多人使用会导致信号失效。需要extra_data：策略拥挤度指标、市场参与者行为数据。

12. **协整配对交易A股验证**：附录B的协整选股策略需A股配对验证。需要extra_data：A股行业分类数据、历史配对交易回测结果。

---

# NEXT_ACTION

1. **A股环境切换验证**：设置`abupy.env.g_market_target = EMarketTargetType.E_MARKET_TARGET_CN`，获取`ABuSymbolPd.make_kl_df('601398')`验证A股数据结构，对比美股字段一致性。

2. **A股佣金计算单元测试**：编写`calc_commision_cn`的单元测试，验证印花税0.3‰+佣金0.25‰+最低5元的边界条件（如1手4.75元股票，佣金=4.75*100*0.00025=0.11875<5，应按5元收取）。

3. **A股全市场回测基线**：使用`choice_symbols=None`在A股运行`run_loop_back`，5年历史数据，记录基准收益（沪深300）、买入成交比例、资金利用率，与书中美股结果对比。

4. **Grid Search A股参数优化**：在A股8只股票池上运行`GridSearch`，生成买入因子（42d/60d）和卖出因子（ATR止盈止损/暴跌保护/保护盈利）的1431种组合，使用`WrsmScorer`寻找最优参数。

5. **机器学习特征A股生成**：开启`g_enable_ml_feature=True`，在A股回测中自动生成`deg_ang21/42/60/252`、`price_rank60/90/120/252`、`wave_score1/2/3`、`jump_up/down_power`等特征。

6. **Ump角度主裁A股训练**：使用A股回测生成的交易特征训练`AbuUmpMainDeg`，设置`threshold=0.65`，运行`fit()`识别失败率>65%的分类簇，使用`brust_min()`全局最优筛选，保存`dump_clf()`。

7. **Ump边裁A股训练**：训练`AbuUmpEdgeDeg`、`AbuUmpEdgePrice`、`AbuUmpEdgeWave`、`AbuUmpEdgeFull`四个边裁，在A股测试集上验证拦截正确率（目标>60%）。

8. **开启Ump拦截A股回测**：同时开启`g_enable_ump_main_deg_block=True`和`g_enable_ump_edge_deg_block=True`，对比未开启/仅主裁/主裁+边裁三种模式的胜率、盈亏比、收益比例和。

9. **跳空缺口A股统计**：使用`tl.jump.calc_jump()`和`tl.jump.calc_jump_line_weight()`对A股指数（如沪深300）统计跳空缺口，识别强支撑阻力位，设计突破/反转策略。

10. **相关性选股策略A股验证**：使用`ABuTLSimilar.coint_similar()`在A股寻找协整配对（如银行股配对），验证统计套利空间，对比书中美股TSLA结果。

11. **技术指标可视化A股**：使用`nd.macd.plot_macd_from_order()`、`nd.boll.plot_boll_from_order()`、`nd.ma.plot_ma_from_order()`对A股典型交易进行可视化，人工分析买卖点合理性。

12. **数据缓存性能优化**：测试A股全市场数据在HDF5/CSV/MongoDB三种缓存格式下的读写速度，根据硬盘类型（固态/非固态）选择最优方案，设置`g_data_cache_type`。
