extract_status: success

---

# MATERIAL_CARD

| field | value |
|-------|-------|
| title | 量化交易之路——用Python做股票量化分析 (Part3: 第7-8章) |
| author_or_source | 作者：阿布 |
| material_type | 技术书籍（Python量化交易系统开发） |
| domain_tags | 量化交易, Python, 回测系统, 择时, 选股, 凯利公式, ATR, 仓位管理 |
| file_scope | 第7章（量化系统入门）+ 第8章（量化系统开发） |
| source_file_size_mb | ~50MB（PDF文字版） |
| retain_mode | EXCERPT_RETAIN |

---

# ROUTING_DECISION

| field | value |
|-------|-------|
| current_repo_role | A_SHARES_DATA_ENGINEERING_GUARD |
| quantizable_now_ratio_estimate | 75% |
| needs_extra_data_ratio_estimate | 25% |
| biggest_leakage_risks | 1) 书中示例基于美股(usTSLA等)，A股需切换市场参数；2) abu框架开源版本与书中教学版本有差异；3) 部分因子只有教学演示价值，无实战盈利能力；4) 滑点/佣金模型需按A股规则重配 |

---

# CONTENT_CLUSTERS

## 1. 趋势跟踪与均值回复策略入门
- what_it_is: 通过"三只小猪"故事讲解两种截然相反的量化策略模型，以及凯利公式仓位控制
- keep_level: 高
- repo_mapping: A_SHARES_DATA_ENGINEERING_GUARD / 策略回测框架设计
- evidence_status: 来自原文

## 2. 凯利公式与仓位管理
- what_it_is: 标准凯利公式f=Pwin-Ploss及修正版f=Ploss/(收益期望/亏损期望)的Python实现
- keep_level: 高
- repo_mapping: A_SHARES_DATA_ENGINEERING_GUARD / 仓位管理模块
- evidence_status: 来自原文

## 3. abu量化系统择时模块（买入因子）
- what_it_is: AbuFactorBuyBreak N日趋势突破买入因子的实现及多因子并行配置
- keep_level: 高
- repo_mapping: A_SHARES_DATA_ENGINEERING_GUARD / 择时引擎
- evidence_status: 来自原文

## 4. abu量化系统卖出因子（止盈止损）
- what_it_is: AbuFactorAtrNStop、AbuFactorPreAtrNStop、AbuFactorCloseAtrNStop三类卖出因子
- keep_level: 高
- repo_mapping: A_SHARES_DATA_ENGINEERING_GUARD / 风控模块
- evidence_status: 来自原文

## 5. 滑点策略与订单执行
- what_it_is: AbuSlippageBuyMean默认均价买入及自定义滑点类AbuSlippageBuyMean2
- keep_level: 中
- repo_mapping: A_SHARES_DATA_ENGINEERING_GUARD / 交易执行层
- evidence_status: 来自原文

## 6. 多股票择时与并行加速
- what_it_is: ABuPickTimeExecute.do_symbols_with_same_factors()及多进程并行回测
- keep_level: 中
- repo_mapping: A_SHARES_DATA_ENGINEERING_GUARD / 分布式回测
- evidence_status: 来自原文

## 7. 选股因子与角度选股
- what_it_is: AbuPickRegressAngMinMax基于线性拟合角度的选股因子实现
- keep_level: 高
- repo_mapping: A_SHARES_FEATURE_POOL / 选股模块
- evidence_status: 来自原文

## 8. 自定义仓位管理（Kelly/ATR）
- what_it_is: AbuKellyPosition基于胜率和盈亏期望的仓位管理，以及AbuAtrPosition默认ATR仓位
- keep_level: 高
- repo_mapping: A_SHARES_DATA_ENGINEERING_GUARD / 资金管理
- evidence_status: 来自原文

## 9. 中文自动生成交易策略
- what_it_is: gen_buy_from_chinese()通过中文描述生成Python策略代码的元编程技术
- keep_level: 中
- repo_mapping: A_SHARES_DATA_ENGINEERING_GUARD / 策略生成器
- evidence_status: 来自原文

## 10. 回测结果度量与可视化
- what_it_is: AbuMetricsBase对回测结果进行胜率、盈亏比、夏普比率、最大回撤等度量
- keep_level: 高
- repo_mapping: A_SHARES_DATA_ENGINEERING_GUARD / 绩效归因
- evidence_status: 来自原文

---

# QUANTIZATION_TABLE

| concept | type | minimal_definition | observable_proxy | min_data_requirement | confirmation_timing | quant_status | repo_target | leakage_risk | notes |
|---------|------|-------------------|------------------|---------------------|---------------------|--------------|-------------|--------------|-------|
| 凯利公式仓位 | 公式 | f = Pwin - Ploss / (收益期望/亏损期望) | 每次买入仓位比例 | 历史交易胜率/盈亏数据 | 策略回测后 | proxy_quantizable_now | 资金管理模块 | 参数过拟合风险 | 需按实际策略调整 |
| N日趋势突破 | 买入信号 | 收盘价达到xd天内最高价格 | price == rolling_max(xd) | N日K线数据 | 每日收盘后 | proxy_quantizable_now | 择时引擎 | 信号趋同化 | 书中示例为教学演示 |
| ATR止盈止损 | 卖出信号 | profit > stop_win_n * ATR 或 profit < -stop_loss_n * ATR | ATR(14)+ATR(21) | 日内high/low/close | 每日收盘后 | proxy_quantizable_now | 风控模块 | 参数敏感 | 需Grid Search优化 |
| 暴跌保护止损 | 卖出信号 | preClose - close > atr21 * pre_atr_n | 前收盘价与今日收盘价差 | 日内数据 | 盘中实时监控 | proxy_quantizable_now | 风控模块 | 极端行情下可能失效 | 适合非高频个人投资者 |
| 保护盈利止盈 | 卖出信号 | max_close - close > atr21 * close_atr_n | 买入后最高价与当前价差 | 日内数据 | 每日收盘后 | proxy_quantizable_now | 风控模块 | 可能过早止盈 | 需结合趋势强度判断 |
| 线性拟合角度选股 | 选股因子 | 计算股票前期走势线性拟合角度，筛选角度范围 | regress_deg(close, window) | 选股周期数据(默认252天) | 回测前选股阶段 | proxy_quantizable_now | 选股模块 | 仅反映线性趋势 | 可扩展为非线性拟合 |
| 价格范围选股 | 选股因子 | 选股周期内收盘价最大/最小值满足阈值 | close.max() < max and close.min() > min | 选股周期数据 | 回测前选股阶段 | proxy_quantizable_now | 选股模块 | 固定阈值不适应市场变化 | 建议动态阈值 |
| 滑点过滤 | 执行策略 | 开盘下跌超过阈值则放弃买单 | open/preClose < (1 - g_open_down_rate) | 当日开盘数据 | 开盘瞬间 | proxy_quantizable_now | 交易执行层 | 阈值需按市场调整 | 默认0.07适合美股 |
| 多进程并行回测 | 工程优化 | 将target_symbols切割为n_process个子序列并行择时 | CPU利用率/子进程数 | 全市场股票池 | 策略开发阶段 | proxy_quantizable_now | 分布式回测 | 进程间通信开销 | 可扩展为Spark分布式 |
| 中文策略生成 | 元编程 | 解析中文描述的语法树生成Python策略代码 | 自然语言到代码的转换准确率 | 策略模板库 | 策略开发阶段 | future_bucket | 策略生成器 | 复杂策略难以描述 | 适合简单快速验证 |
| 策略胜率 | 度量指标 | 盈利次数/总交易次数 | order.result统计 | 历史交易记录 | 回测完成后 | proxy_quantizable_now | 绩效归因 | 样本外可能偏差 | 需交叉验证 |
| 盈亏比 | 度量指标 | 盈利总和/亏损总和 | order.profit统计 | 历史交易记录 | 回测完成后 | proxy_quantizable_now | 绩效归因 | 极端盈利会扭曲 | 结合胜率使用 |
| 夏普比率 | 度量指标 | (年化收益-无风险利率)/收益波动率 | cum_returns / annual_volatility | 策略日收益率序列 | 回测完成后 | proxy_quantizable_now | 绩效归因 | 对收益分布敏感 | 需与基准对比 |
| 最大回撤 | 度量指标 | 峰值到谷底的最大亏损比例 | capital_blance峰值与谷底差 | 资金曲线 | 回测完成后 | proxy_quantizable_now | 绩效归因 | 未来回撤可能更大 | 需关注回撤持续时间 |
| 资金利用率 | 度量指标 | 1 - (cash_blance/capital_blance).mean() | 每日现金余额 | 资金流水 | 回测完成后 | proxy_quantizable_now | 绩效归因 | 满仓乘数可能失真 | 需与基准同量级对比 |
| 买入成交比例 | 度量指标 | 实际成交买单数/发出买单信号数 | action_pd.deal.value_counts() | 交易行为记录 | 回测完成后 | proxy_quantizable_now | 绩效归因 | 资金不足导致 | 需调整g_atr_pos_base |
| 策略收益 | 度量指标 | (Pend-Pstart)/Pstart * 100% | 最终资产/初始资产 | 每日资产记录 | 回测完成后 | proxy_quantizable_now | 绩效归因 | 未考虑资金规模 | 大资金需考虑冲击成本 |
| 策略年化收益 | 度量指标 | ((1+P)^(252/n)-1)*100% | 策略收益与执行天数 | 策略收益和执行天数 | 回测完成后 | proxy_quantizable_now | 绩效归因 | 复利假设可能不成立 | A股用250天 |
| 信息比率 | 度量指标 | (策略年化收益-基准年化收益)/跟踪误差 | 超额收益/标准差 | 策略与基准日收益差 | 回测完成后 | needs_extra_data | 绩效归因 | 需基准指数选择合理 | 基准需与策略风格匹配 |
| 阿尔法/贝塔 | 度量指标 | Alpha=策略超额收益，Beta=市场敏感度 | 回归系数 | 策略与基准日收益 | 回测完成后 | needs_extra_data | 绩效归因 | 市场结构变化时失效 | 需滚动计算 |
| 满仓乘数 | 调整方法 | algorithm_returns * stocks_full_rate_factor | 使策略随时满仓的虚拟收益 | 持仓比例 | 回测完成后 | proxy_quantizable_now | 绩效归因 | 仅虚拟调整 | 无法真实提高收益 |


---

# RETAINED_EXCERPTS

### EXCERPT_P3_01
- **source_hint**: 第7章 - 三只小猪故事
- **quote**: `7.2.3 三只小猪股票投资的故事。猪妈妈有三个孩子，一个叫猪老大，一个叫猪老二，还有一个叫猪老三。猪妈妈说："我发现股票里有条规律，连续下跌3天的股票，在第4天差不多全是上涨，而且一般一涨就连续上涨3天，你们只要抓住这个规律就能盈利了！" 猪妈妈把凯利公式的使用方法告诉了猪老二和猪老三。J=Pwin-Ploss(b=1)。连续下跌3天，第4天及之后上涨的概率为80%，所以：Pwin=0.8, Ploss=1-0.8=0.2, J=Pwin-Ploss=0.6。利用凯利公式计算保持每次买入仓位的60%为可以控制风险。修正的凯利公式：f = Pwin - Ploss/(收益期望值/亏损期望值)。期望收益：0.05*3=0.15。期望亏损：0.5（系统性灾难概率20%，股价下跌50%）。f = 0.8 - 0.2/(0.15/0.5) = 0.13。经过修正的凯利公式计算保持每次买入仓位的13%为可最大程度控制风险。`
- **why_kept**: 核心仓位管理寓言，凯利公式教学案例，包含标准版和修正版公式及计算过程
- **quant_link**: 仓位管理

### EXCERPT_P3_02
- **source_hint**: 第7章 - 股票走势生成代码
- **quote**: `def gen_stock_price_array2(): price_array = np.concatenate((price_array1, np.ones(trade_day) * price_array1[-1]), axis=0) for ind in np.arange(len(price_array1) - 1, len(price_array) - 1): last4 = price_array[ind - 3:ind + 1] if len(last4) == 4 and last4[-1] > last4[-2] and last4[-2] > last4[-3] and last4[-3] > last4[-4]: win = np.random.binomial(1, 0.45) elif len(last4) == 4 and last4[-1] < last4[-2] and last4[-2] < last4[-3] and last4[-3] < last4[-4]: win = np.random.binomial(1, 0.8) else: win = price_array[ind] > price_array[ind - 1] if win: price_array[ind + 1] = (1 + 0.05) * price_array[ind] else: price_array[ind + 1] = (1 - 0.05) * price_array[ind] return price_array`
- **why_kept**: 马尔可夫假设下的股票走势模拟代码，包含连续涨跌规则和价格变动逻辑
- **quant_link**: 走势生成

### EXCERPT_P3_03
- **source_hint**: 第7章 - 交易执行函数
- **quote**: `def execute_trade(cash, buy_rate): commission = 5 # 手续费 stock_cnt = 0 # 持有股票数 keep_day = 0 # 持股天数 capital = [] # 资产结果序列 for ind in np.arange(352, len(price_array3) - 1): if stock_cnt > 0: keep_day += 1 if stock_cnt > 0 and keep_day == 3: cash += price_array3[ind] * stock_cnt cash -= commission if cash <= 0: capital.append(0); print('爆仓了！'); break keep_day = 0; stock_cnt = 0 lasts = price_array3[ind - 4 : ind + 1] if stock_cnt == 0 and len(last5) == 5 and last5[1] > last5[0] and last5[-1] < last5[-2] and last5[-2] < last5[-3] and last5[-3] < last5[-4]: cash -= commission; buy_cash = cash * buy_rate; cash -= buy_cash; stock_cnt += buy_cash / price_array3[ind] if stock_cnt < 1: capital.append(0); print('爆仓了！'); break keep_day = 0 capital.append(cash + (stock_cnt * price_array3[ind])) return capital`
- **why_kept**: 三只小猪交易策略的完整Python实现，含买入条件、持股天数、卖出逻辑、爆仓判断
- **quant_link**: 交易执行

### EXCERPT_P3_04
- **source_hint**: 第7章 - 交易结果
- **quote**: `猪老大buy_rate=1.0每次全仓买入，结果爆仓了，最终全部输光！虽然最高资产曾经达到过49757元。猪老二buy_rate=0.6，最终资产为7665！最高资产曾经达到过26832元。猪老三buy_rate=0.13，最终资产为11472元！盈利了！最高资产曾经达到过13280元。`
- **why_kept**: 三只小猪不同仓位的最终对比结果，直观展示仓位管理的重要性
- **quant_link**: 仓位管理

### EXCERPT_P3_05
- **source_hint**: 第8章 - 买入因子AbuFactorBuyBreak
- **quote**: `class AbuFactorBuyBreak(AbuFactorBuyBase): def __init__(self, **kwargs): self.xd = kwargs['xd'] # 突破参数，比如20,30,40天突破 self.skip_days = 0 self.factor_name = '{}:{}'.format(self.__class__.__name__, self.xd) def fit_day(self, today): day_ind = int(today.key) if day_ind < self.xd - 1 or day_ind >= self.kl_pd.shape[0] - 1: return None if self.skip_days > 0: self.skip_days -= 1; return None if today.close == self.kl_pd.close[day_ind - self.xd + 1:day_ind + 1].max(): self.skip_days = self.xd; return self.make_buy_order(day_ind) return None`
- **why_kept**: N日趋势突破买入因子核心实现，含xd参数、skip_days防重复买入机制
- **quant_link**: 买入因子

### EXCERPT_P3_06
- **source_hint**: 第8章 - 买入因子配置
- **quote**: `buy_factors = [{'xd': 60, 'class': AbuFactorBuyBreak}, {'xd': 42, 'class': AbuFactorBuyBreak}] benchmark = AbuBenchmark()`
- **why_kept**: 买入因子字典配置方式，展示多因子并行生效机制
- **quant_link**: 因子配置

### EXCERPT_P3_07
- **source_hint**: 第8章 - 时间驱动核心
- **quote**: `def day_task(self, today): for buy_factor in self.buy_factors: order = buy_factor.fit_day(today) if order and order.order_deal: self.orders.append(order) for sell_factor in self.sell_factors: sell_factor.fit_day(today, self.orders) def task_loop(self, today): day_cnt = today.key if day_cnt % 5 == 0: self._week_task(today) if day_cnt % 20 == 0: self._month_task(today) self._day_task(today) def fit(self, *args, **kwargs): self.kl_pd.apply(self.task_loop, axis=1)`
- **why_kept**: abu量化系统时间驱动核心代码，日/周/月任务调度机制
- **quant_link**: 择时引擎

### EXCERPT_P3_08
- **source_hint**: 第8章 - 卖出因子AbuFactorSellBreak
- **quote**: `class AbuFactorSellBreak(AbuFactorSellBase): def __init__(self, **kwargs): self.xd = kwargs['xd'] self.sell_type_extra = '{}:{}'.format(self.__class__.__name__, self.xd) @skip_last_day def fit_day(self, today, orders): day_ind = int(today.key) if today.close == self.kl_pd.close[day_ind - self.xd + 1:day_ind + 1].min(): for order in orders: order.fit_sell_order(day_ind, self)`
- **why_kept**: N日向下突破卖出因子实现，与买入因子对称
- **quant_link**: 卖出因子

### EXCERPT_P3_09
- **source_hint**: 第8章 - ATR止盈止损
- **quote**: `class AbuFactorAtrNStop(AbuFactorSellBase): def __init__(self, **kwargs): if 'stop_loss_n' in kwargs: self.stop_loss_n = kwargs['stop_loss_n'] if 'stop_win_n' in kwargs: self.stop_win_n = kwargs['stop_win_n'] @skip_last_day def fit_day(self, today, orders): for order in orders: profit = today.close - order.buy_price stop_base = today.atr21 + today.atr14 if hasattr(self, 'stop_win_n') and profit > 0 and profit > self.stop_win_n * stop_base: self.sell_type_extra = self.sell_type_extra_win; order.fit_sell_order(int(today.key), self) if hasattr(self, 'stop_loss_n') and profit < 0 and profit < -self.stop_loss_n * stop_base: self.sell_type_extra = self.sell_type_extra_loss; order.fit_sell_order(int(today.key), self)`
- **why_kept**: ATR倍数止盈止损核心实现，使用atr21+atr14作为stop_base
- **quant_link**: 止盈止损

### EXCERPT_P3_10
- **source_hint**: 第8章 - 暴跌保护止损
- **quote**: `g_default_pre_atr_n = 1.5 class AbuFactorPreAtrNStop(AbuFactorSellBase): def __init__(self, **kwargs): self.pre_atr_n = g_default_pre_atr_n if 'pre_atr_n' in kwargs: self.pre_atr_n = kwargs['pre_atr_n'] @skip_last_day def fit_day(self, today, orders): for order in orders: if today.preClose - today.close > today.atr21 * self.pre_atr_n: order.fit_sell_order(int(today.key), self)`
- **why_kept**: 暴跌保护止损：今日收盘价与昨日收盘价之差大于ATR*pre_atr_n时卖出
- **quant_link**: 风控

### EXCERPT_P3_11
- **source_hint**: 第8章 - 保护盈利止盈
- **quote**: `class AbuFactorCloseAtrNStop(AbuFactorSellBase): def __init__(self, **kwargs): self.close_atr_n = K_DEFAULT_CLOSE_ATR_N if 'close_atr_n' in kwargs: self.close_atr_n = kwargs['close_atr_n'] @skip_last_day def fit_day(self, today, orders): day_ind = int(today.key) for order in orders: mask_date = self.kl_pd['date'] == order.buy_date start_ind = int(self.kl_pd[mask_date]['key'].values) end_ind = day_ind + 1 max_close = self.kl_pd.iloc[start_ind:end_ind, :].close.max() if max_close - order.buy_price > today['atr21'] and max_close - today.close > today['atr21'] * self.close_atr_n: order.fit_sell_order(day_ind, self)`
- **why_kept**: 保护盈利止盈：买入后有盈利且从最高价回撤超过ATR*close_atr_n时卖出
- **quant_link**: 止盈

### EXCERPT_P3_12
- **source_hint**: 第8章 - 滑点策略
- **quote**: `g_open_down_rate = 0.07 class AbuSlippageBuyMean(AbuSlippageBuyBase): def fit_price(self): if (self.kl_pd_buy.open / self.kl_pd_buy.preClose) < (1 - g_open_down_rate): return np.inf # 开盘下跌超过阈值，单子失效 self.buy_price = np.mean([self.kl_pd_buy['high'], self.kl_pd_buy['low']]) return self.buy_price`
- **why_kept**: 默认均价滑点策略，开盘下跌超过7%则放弃买单
- **quant_link**: 滑点

### EXCERPT_P3_13
- **source_hint**: 第8章 - 因子中滑点类配置
- **quote**: `class AbuFactorBuyBase(six.with_metaclass(ABCMeta, ABuParamBaseClass)): def __init__(self, capital, kl_pd, **kwargs): self.kl_pd = kl_pd; self.capital = capital self.slippage_class = kwargs['slippage'] if 'slippage' in kwargs else AbuSlippageBuyMean self.position_class = kwargs['position'] if 'position' in kwargs else AbuAtrPosition if 'win_rate' in kwargs: self.win_rate = kwargs['win_rate'] if 'gains_mean' in kwargs: self.gains_mean = kwargs['gains_mean'] if 'losses_mean' in kwargs: self.losses_mean = kwargs['losses_mean']`
- **why_kept**: 买入因子基类中滑点类、仓位管理类、胜率/盈亏期望的初始化
- **quant_link**: 执行配置

### EXCERPT_P3_14
- **source_hint**: 第8章 - 多股票择时
- **quote**: `choice_symbols = ['usTSLA','usNOAH','usSFUN','usBIDU','usAAPL', 'usGOOG','usWUBA','usVIPS'] capital = AbuCapital(1000000, benchmark) orders_pd, action_pd, all_fit_symbols_cnt = ABuPickTimeExecute.do_symbols_with_same_factors(choice_symbols, benchmark, buy_factors, sell_factors, capital, show=False)`
- **why_kept**: 多只股票使用相同因子进行择时回测的调用方式
- **quant_link**: 多股回测

### EXCERPT_P3_15
- **source_hint**: 第8章 - 交易结果表
- **quote**: `orders_pd[:10].filter(['Symbol','buy Price','buy Cnt','buyFactor','buy Pos','Sell Date','sell type extra','Sell Type','profit']) Symbol buy Price buy Cnt buyFactor buy Pos Sell Date sell type extra Sell Type profit usAAPL 105.010 1904 AbuFactorBuyBreak:60 AbuAtrPosition 20141202 AbuFactorPreAtrNStop:pre_atr=1.0 win 17592.96 usBIDU 223.680 781 AbuFactorBuyBreak:42 AbuAtrPosition 20141202 AbuFactorPreAtrNStop:pre_atr=1.0 win 9473.53 usNOAH 16.010 9217 AbuFactorBuyBreak:42 AbuAtrPosition 20141208 AbuFactorAtrNStop:stop_win=3.0 win 74104.68`
- **why_kept**: orders_pd交易结果表示例，展示交易详情和卖出因子生效情况
- **quant_link**: 交易记录

### EXCERPT_P3_16
- **source_hint**: 第8章 - Kelly仓位管理
- **quote**: `class AbuKellyPosition(AbuPositionBase): def fit_position(self, factor_object): if not hasattr(factor_object, 'win_rate'): raise RuntimeError('AbuKellyPosition need factor object has win_rate') win_rate = factor_object.win_rate; loss_rate = 1 - win_rate gains_mean = factor_object.gains_mean; losses_mean = factor_object.losses_mean kelly_pos = win_rate - loss_rate / (gains_mean / losses_mean) kelly_pos = g_pos_max if kelly_pos > g_pos_max else kelly_pos return self.read_cash * kelly_pos / self.bp`
- **why_kept**: AbuKellyPosition基于胜率和盈亏期望的仓位管理核心实现
- **quant_link**: 仓位管理

### EXCERPT_P3_17
- **source_hint**: 第8章 - 不同因子配置
- **quote**: `target_symbols = ['usSFUN','usNOAH'] buy_factors_sfun = [{'xd': 42, 'class': AbuFactorBuyBreak}] sell_factors_sfun = [{'xd': 60, 'class': AbuFactorSellBreak}] buy_factors_noah = [{'xd': 21, 'class': AbuFactorBuyBreak}] sell_factors_noah = [{'xd': 42, 'class': AbuFactorSellBreak}] factor_dict = dict() factor_dict['usSFUN'] = {'buy_factors': buy_factors_sfun, 'sell_factors': sell_factors_sfun} factor_dict['usNOAH'] = {'buy_factors': buy_factors_noah, 'sell_factors': sell_factors_noah}`
- **why_kept**: 不同股票使用不同买入/卖出因子的配置示例
- **quant_link**: 因子配置

### EXCERPT_P3_18
- **source_hint**: 第8章 - 并行回测
- **quote**: `class AbuPickTimeMaster(object): @classmethod def do_symbols_with_same_factors_process(cls, target_symbols, benchmark, buy_factors, sell_factors, capital, kl_pd_manger=None, n_process_kl=64, n_process_pick_time=8): kl_pd_manger.batch_get_pick_time_kl_pd(target_symbols, n_process=n_process_kl) process_symbols = split_k_market(n_process_pick_time, market_symbols=target_symbols) parallel = Parallel(n_jobs=n_process_pick_time, verbose=0, pre_dispatch='2*n_jobs') out = parallel(delayed(do_symbols_with_same_factors)(choice_symbols, benchmark, buy_factors, sell_factors, capital, apply_capital=False, kl_pd_manger=kl_pd_manger) for choice_symbols in process_symbols)`
- **why_kept**: 多进程并行回测架构，将股票池切分后并行择时再合并结果
- **quant_link**: 性能优化

### EXCERPT_P3_19
- **source_hint**: 第8章 - 角度选股因子
- **quote**: `class AbuPickRegressAngMinMax(AbuPickStockBase): def __init__(self, **kwargs): self.threshold_ang_min = -np.inf if 'threshold_ang_min' in kwargs: self.threshold_ang_min = kwargs['threshold_ang_min'] self.threshold_ang_max = np.inf if 'threshold_ang_max' in kwargs: self.threshold_ang_max = kwargs['threshold_ang_max'] @reversed_result def fit_pick(self, kl_pd, target_symbol): ang = ABuRegUtil.calc_regress_deg(kl_pd.close, show=False) if self.threshold_ang_min < ang < self.threshold_ang_max: return True return False`
- **why_kept**: 基于线性拟合角度的选股因子，支持最小/最大角度阈值及结果反转
- **quant_link**: 选股因子

### EXCERPT_P3_20
- **source_hint**: 第8章 - 角度计算
- **quote**: `def calc_regress_deg(y_arr, show=True): x = np.arange(0, len(y_arr)) zoom_factor = x.max() / y_arr.max() y_arr = zoom_factor * y_arr x = sm.add_constant(x) model = regression.linear_model.OLS(y_arr, x).fit() rad = model.params[1] deg = np.rad2deg(rad) if show: intercept = model.params[0] reg_y_fit = x * rad + intercept; plt.plot(x, y_arr); plt.plot(x, reg_y_fit); plt.title('deg='+str(deg)); plt.show() return deg`
- **why_kept**: 线性拟合角度计算完整实现，使用OLS回归后将弧度转为角度
- **quant_link**: 特征计算

### EXCERPT_P3_21
- **source_hint**: 第8章 - 选股执行
- **quote**: `def do_pick_stock_work(choice_symbols, benchmark, capital, stock_pickers): kl_pd_manger = AbuKLManger(benchmark, capital) stock_pick = AbuPickStockWorker(capital, benchmark, kl_pd_manger, choice_symbols=choice_symbols, stock_pickers=stock_pickers) stock_pick.fit() return stock_pick.choice_symbols`
- **why_kept**: 选股操作封装函数，展示AbuPickStockWorker的使用流程
- **quant_link**: 选股执行

### EXCERPT_P3_22
- **source_hint**: 第8章 - 价格选股因子
- **quote**: `class AbuPickStockPriceMinMax(AbuPickStockBase): def __init__(self, **kwargs): self.threshold_price_min = np.inf if 'threshold_price_min' in kwargs: self.threshold_price_min = kwargs['threshold_price_min'] self.threshold_price_max = np.inf if 'threshold_price_max' in kwargs: self.threshold_price_max = kwargs['threshold_price_max'] @reversed_result def fit_pick(self, kl_pd, target_symbol): if kl_pd.close.max() < self.threshold_price_max and kl_pd.close.min() > self.threshold_price_min: return True return False`
- **why_kept**: 基于价格范围的选股因子，筛选周期内最高价/最低价满足阈值的股票
- **quant_link**: 选股因子

### EXCERPT_P3_23
- **source_hint**: 第9章 - 中文策略生成
- **quote**: `init_self_code = {'类名称': 'AbuChineseGen', '类变量': [('连续下跌买入阀值天数', {'默认': 3}), ('计数连续下跌的天数', {'默认': 0})]} fit_day_code = list() fit_day_code.extend(['如果|今天.收盘<昨天.收盘|计数连续下跌的天数+=1', '否则：计数连续下跌的天数=0']) fit_day_code.extend(['如果|计数连续下跌的天数>=连续下跌买入阀值天数|买入&计数连续下跌的天数=0']) gen_code = abu.gen_buy_from_chinese(init_self_code, fit_day_code)`
- **why_kept**: 通过中文描述生成交易策略代码的元编程技术示例
- **quant_link**: 策略生成

### EXCERPT_P3_24
- **source_hint**: 第9章 - 回测主函数
- **quote**: `def run_loop_back(read_cash, buy_factors, sell_factors, stock_picks=None, choice_symbols=None, n_folds=2, n_process_kl=16, n_process_pick=8): benchmark = AbuBenchmark(n_folds=n_folds) capital = AbuCapital(read_cash, benchmark) choice_symbols = AbuPickStockMaster.do_pick_stock_with_process(capital, benchmark, stock_picks, choice_symbols=choice_symbols, n_process_pick_stock=n_process_pick) if choice_symbols is None or len(choice_symbols) == 0: return None, None kl_pd_manger = AbuKLManger(benchmark, capital) kl_pd_manger.batch_get_pick_time_kl_pd(choice_symbols, n_process=n_process_kl) orders_pd, action_pd, all_fit_symbols_cnt = AbuPickTimeMaster.do_symbols_with_same_factors_process(choice_symbols, benchmark, buy_factors, sell_factors, capital, kl_pd_manger=kl_pd_manger, n_process_kl=n_process_kl, n_process_pick_time=n_process_pick) abu_result_tuple = namedtuple('abu_result', ('orders_pd', 'action_pd', 'capital', 'benchmark')) return abu_result_tuple(orders_pd, action_pd, capital, benchmark), kl_pd_manger`
- **why_kept**: run_loop_back完整封装：选股->获取K线->择时->返回结果元组
- **quant_link**: 回测框架

### EXCERPT_P3_25
- **source_hint**: 第9章 - 度量统计
- **quote**: `def metrics_base_stats(self): self.benchmark_returns = np.round(self.benchmark.kl_pd.close.pct_change(), 3) self.algorithm_returns = np.round(self.capital.capital_pd['capital_blance'].pct_change(), 3) self.algorithm_cum_returns = stats.cum_returns(self.algorithm_returns) self.benchmark_cum_returns = stats.cum_returns(self.benchmark_returns) self.algorithm_period_returns = self.algorithm_cum_returns[-1] self.benchmark_period_returns = self.benchmark_cum_returns[-1] self.num_trading_days = len(self.benchmark_returns) self.algorithm_annualized_returns = (252 / self.num_trading_days) * self.algorithm_period_returns self.benchmark_annualized_returns = (252 / self.num_trading_days) * self.benchmark_period_returns`
- **why_kept**: AbuMetricsBase核心统计：收益、累计收益、年化收益、交易天数计算
- **quant_link**: 绩效度量

### EXCERPT_P3_26
- **source_hint**: 第9章 - 夏普等风险指标
- **quote**: `self.benchmark_volatility = stats.annual_volatility(self.benchmark_returns) self.algorithm_volatility = stats.annual_volatility(self.algorithm_returns) self.benchmark_sharpe = stats.sharpe_ratio(self.benchmark_returns) self.algorithm_sharpe = stats.sharpe_ratio(self.algorithm_returns) self.information = stats.information_ratio(self.algorithm_returns.values, self.benchmark_returns.values) self.alpha, self.beta = stats.alpha_beta_aligned(self.algorithm_returns.values, self.benchmark_returns.values) self.max_drawdown = stats.max_drawdown(self.algorithm_returns.values)`
- **why_kept**: 波动率、夏普比率、信息比率、阿尔法贝塔、最大回撤的计算
- **quant_link**: 风险指标

### EXCERPT_P3_27
- **source_hint**: 第9章 - 网格搜索
- **quote**: `class GridSearch: def __init__(self, read_cash, choice_symbols, buy_factors_product, sell_factors_product, stock_pickers_product=None): self.read_cash = read_cash; self.choice_symbols = choice_symbols self.buy_factors_product = buy_factors_product; self.sell_factors_product = sell_factors_product self.stock_pickers_product = stock_pickers_product def fit(self, score_class=WrsmScorer, n_jobs=-1): score_tuple_array = [] parallel = Parallel(n_jobs=n_jobs, verbose=0, pre_dispatch='2*n_jobs') out_abu_score_tuple = parallel(delayed(grid_mul_func)(self.read_cash, self.benchmark, buy_factors, sell_factors, stock_pickers, self.choice_symbols, pass_kl_pd_manger) for stock_pickers in self.stock_pickers_product for buy_factors in self.buy_factors_product for sell_factors in self.sell_factors_product) scores = make_scorer(score_tuple_array, score_class, weights=self.score_weights) self.best_score_tuple_grid = score_tuple_array[scores.index[-1]] return scores, score_tuple_array`
- **why_kept**: GridSearch对买入/卖出/选股因子参数进行排列组合寻优
- **quant_link**: 参数优化

### EXCERPT_P3_28
- **source_hint**: 第9章 - 评分机制
- **quote**: `class WrsmScorer(AbuBaseScorer): def init_self_begin(self, *arg, **kwargs): self.select_score_func = lambda metrics: [metrics.win_rate, metrics.algorithm_period_returns, metrics.algorithm_sharpe, metrics.max_drawdown] self.columns_name = ['win_rate', 'returns', 'sharpe', 'max_drawdown'] self.weights_cnt = len(self.columns_name)`
- **why_kept**: 默认评分类：胜率/收益/夏普/回撤四项等权重评分，每项排序后0-1标准化
- **quant_link**: 评分模型

### EXCERPT_P3_29
- **source_hint**: 第9章 - 资金限制度量
- **quote**: `abu_result_tuple.action_pd.deal.value_counts() False 109671 True 54635 metrics = AbuMetricsBase(*abu_result_tuple) metrics.fit_metrics() metrics.plot_returns_cmp(only_show_returns=True) 买入后卖出的交易数量：80743 胜率：44.24% 平均获利期望：10.0% 平均亏损期望：-6.17% 盈亏比：1.186 策略收益：48.36% 基准收益：77.87% 策略买入成交比例：32.57% 策略资金利用率比例：86.31%`
- **why_kept**: 全市场回测资金限制导致约1/3单子成交，策略收益未跑赢基准
- **quant_link**: 资金管理

### EXCERPT_P3_30
- **source_hint**: 第9章 - 满仓乘数
- **quote**: `self.cash_utilization = 1 - (self.capital.capital_pd.cash_blance / self.capital.capital_pd.capital_blance).mean() self.stocks_full_rate_factor = 1 if self.enable_stocks_full_rate_factor: stocks_full_rate = (self.capital.capital_pd.stocks_blance / self.capital.capital_pd.capital_blance) stocks_full_rate[stocks_full_rate == 0] = 1 self.stocks_full_rate_factor = (1 / stocks_full_rate) self.algorithm_returns = np.round(self.capital.capital_pd['capital_blance'].pct_change(), 3) * self.stocks_full_rate_factor`
- **why_kept**: 满仓乘数实现：通过持仓比例倒数虚拟调整收益，使策略与基准可比
- **quant_link**: 度量调整

### EXCERPT_P3_31
- **source_hint**: 第9章 - 结果保存
- **quote**: `abu.store_abu_result_tuple(abu_result_tuple, n_folds=5)`
- **why_kept**: 回测结果本地序列化保存，使用pickle存储
- **quant_link**: 数据持久化

### EXCERPT_P3_32
- **source_hint**: 第8章 - 本章小结
- **quote**: `择时与选股操作是交易系统中的两大重点，它们之间的关系是相辅相成的。比如你实现了一个选股策略，选取股价在过去一年内在5元上下波动的股票，在美股中很多机构确实有规定5元以下的股票不能买入，所以很多机构会选择在5元进行救市。比如美国爆发经济危机时美国银行的股价就是在5元左右被托住，这样后续使用的择时策略就应该是属于趋势突破类型的择时策略，只有将选股和择时配合好，并且彻底理解你的策略，最终才能有好的结果。`
- **why_kept**: 核心投资理念：选股与择时相辅相成，必须理解策略本质
- **quant_link**: 策略设计

---

# FORMULAS_AND_ALGOS

## 凯利公式（标准版）
```
f = Pwin - Ploss
其中：
Pwin = 连续下跌3天后第4天上涨概率 = 0.8
Ploss = 1 - 0.8 = 0.2
f = 0.8 - 0.2 = 0.6 （每次买入60%仓位）
```

## 修正凯利公式（考虑期望收益/亏损）
```
f = Pwin - Ploss / (收益期望值/亏损期望值)
收益期望值 = 0.05 * 3 = 0.15 （期待三天上涨，每天5%）
亏损期望值 = 0.5 （系统性灾难概率20%，股价下跌50%）
f = 0.8 - 0.2 / (0.15/0.5) = 0.8 - 0.2/0.3 = 0.13 （每次买入13%仓位）
```

## 马尔可夫股票走势生成（Phase 2）
```python
def gen_stock_price_array2():
    price_array = np.concatenate(
        (price_array1, np.ones(trade_day) * price_array1[-1]), axis=0)
    for ind in np.arange(len(price_array1) - 1, len(price_array) - 1):
        last4 = price_array[ind - 3:ind + 1]
        if len(last4) == 4 and last4[-1] > last4[-2] and last4[-2] > last4[-3] and last4[-3] > last4[-4]:
            # 连续上涨3天，第4天及之后天下跌的概率为55%
            win = np.random.binomial(1, 0.45)
        elif len(last4) == 4 and last4[-1] < last4[-2] and last4[-2] < last4[-3] and last4[-3] < last4[-4]:
            # 连续下跌3天，第4天及之后天上涨的概率为80%
            win = np.random.binomial(1, 0.8)
        else:
            # 涨跌只与前一天的涨跌相关
            win = price_array[ind] > price_array[ind - 1]
        if win:
            price_array[ind + 1] = (1 + 0.05) * price_array[ind]
        else:
            price_array[ind + 1] = (1 - 0.05) * price_array[ind]
    return price_array
```

## 买入因子AbuFactorBuyBreak核心逻辑
```python
class AbuFactorBuyBreak(AbuFactorBuyBase):
    def __init__(self, **kwargs):
        self.xd = kwargs['xd']  # 突破参数，如20,30,40天突破
        self.skip_days = 0
        self.factor_name = '{}:{}'.format(self.__class__.__name__, self.xd)
    
    def fit_day(self, today):
        day_ind = int(today.key)
        if day_ind < self.xd - 1 or day_ind >= self.kl_pd.shape[0] - 1:
            return None
        if self.skip_days > 0:
            self.skip_days -= 1
            return None
        # 今天的收盘价格达到xd天内最高价格则符合条件
        if today.close == self.kl_pd.close[day_ind - self.xd + 1:day_ind + 1].max():
            self.skip_days = self.xd  # xd天内再次创新高也不买
            return self.make_buy_order(day_ind)
        return None
```

## 卖出因子AbuFactorAtrNStop核心逻辑
```python
class AbuFactorAtrNStop(AbuFactorSellBase):
    def __init__(self, **kwargs):
        if 'stop_loss_n' in kwargs:
            self.stop_loss_n = kwargs['stop_loss_n']
        if 'stop_win_n' in kwargs:
            self.stop_win_n = kwargs['stop_win_n']
    
    def fit_day(self, today, orders):
        for order in orders:
            profit = today.close - order.buy_price
            stop_base = today.atr21 + today.atr14
            if hasattr(self, 'stop_win_n') and profit > 0 and profit > self.stop_win_n * stop_base:
                self.sell_type_extra = self.sell_type_extra_win
                order.fit_sell_order(int(today.key), self)
            if hasattr(self, 'stop_loss_n') and profit < 0 and profit < -self.stop_loss_n * stop_base:
                self.sell_type_extra = self.sell_type_extra_loss
                order.fit_sell_order(int(today.key), self)
```

## 角度选股因子AbuPickRegressAngMinMax
```python
class AbuPickRegressAngMinMax(AbuPickStockBase):
    def __init__(self, **kwargs):
        self.threshold_ang_min = -np.inf
        if 'threshold_ang_min' in kwargs:
            self.threshold_ang_min = kwargs['threshold_ang_min']
        self.threshold_ang_max = np.inf
        if 'threshold_ang_max' in kwargs:
            self.threshold_ang_max = kwargs['threshold_ang_max']
    
    @reversed_result
    def fit_pick(self, kl_pd, target_symbol):
        ang = ABuRegUtil.calc_regress_deg(kl_pd.close, show=False)
        if self.threshold_ang_min < ang < self.threshold_ang_max:
            return True
        return False
```

## 线性拟合角度计算
```python
def calc_regress_deg(y_arr, show=True):
    x = np.arange(0, len(y_arr))
    zoom_factor = x.max() / y_arr.max()
    y_arr = zoom_factor * y_arr
    x = sm.add_constant(x)
    model = regression.linear_model.OLS(y_arr, x).fit()
    rad = model.params[1]
    deg = np.rad2deg(rad)
    return deg
```

## 滑点买入策略
```python
g_open_down_rate = 0.07
class AbuSlippageBuyMean(AbuSlippageBuyBase):
    def fit_price(self):
        if (self.kl_pd_buy.open / self.kl_pd_buy.preClose) < (1 - g_open_down_rate):
            return np.inf  # 开盘下跌超过阈值，单子失效
        self.buy_price = np.mean([self.kl_pd_buy['high'], self.kl_pd_buy['low']])
        return self.buy_price
```

## 时间驱动回测核心
```python
def day_task(self, today):
    for buy_factor in self.buy_factors:
        order = buy_factor.fit_day(today)
        if order and order.order_deal:
            self.orders.append(order)
    for sell_factor in self.sell_factors:
        sell_factor.fit_day(today, self.orders)

def task_loop(self, today):
    day_cnt = today.key
    if day_cnt % 5 == 0:
        self._week_task(today)
    if day_cnt % 20 == 0:
        self._month_task(today)
    self._day_task(today)

def fit(self, *args, **kwargs):
    self.kl_pd.apply(self.task_loop, axis=1)
```

---

# NOT_QUANT_YET

1. **A股市场交易规则适配**：书中示例使用美股市场（usTSLA等），A股需要切换EMarketTargetType.E_MARKET_TARGET_CN，并调整佣金计算（印花税+佣金）、最小买入股数（100的整数倍）、一年交易日（250天）。需要extra_data：A股历史交易数据、A股佣金规则表。

2. **实盘数据接入**：书中回测使用沙盒数据或本地缓存，实盘需要实时行情接入。需要extra_data：A股实时行情API、Level-2数据权限。

3. **特征工程扩展**：书中使用的角度、跳空、价格rank等特征较为简单，实际A股策略可能需要更多特征（如资金流向、龙虎榜、研报情感等）。需要extra_data：另类数据源。

4. **参数过拟合风险**：书中Grid Search寻找最优参数的方法在特定历史数据上可能过拟合，需要更严格的交叉验证（股票相关性分组验证）。需要extra_data：更多历史数据、不同市场环境数据。

5. **冲击成本与流动性**：全市场回测中大量交易无法成交（买入成交比例仅32-39%），实盘大资金需要考虑冲击成本。需要extra_data：订单簿数据、逐笔成交数据。

6. **T+1交易制度**：A股T+1制度限制当日买入后卖出，与书中假设的T+0（美股）不同。需要extra_data：A股交易制度约束规则。

7. **涨跌停限制**：A股10%涨跌停（科创板/创业板20%）会影响突破策略有效性。需要extra_data：涨跌停历史数据、开盘集合竞价数据。

8. **退市风险与ST股票**：书中未涉及A股特有的退市风险、ST股票交易限制。需要extra_data：A股股票状态表、风险警示股票列表。

9. **策略性能优化**：Python多进程回测全市场耗时较长，需要更高效实现（C++核心/向量化计算）。需要extra_data：性能基准测试数据。

10. **非固态硬盘数据缓存**：书中提到HDF5在非固态硬盘写入慢，需要调整缓存格式。需要extra_data：存储硬件性能数据。

11. **中文策略生成复杂度**：书中中文策略生成仅适合简单策略，复杂策略难以描述。需要extra_data：自然语言处理模型、策略模板库扩展。

12. **机器学习裁判泛化能力**：Ump模块基于GMM分类，在新市场环境下可能失效。需要extra_data：A股历史交易特征、更多训练数据。

---

# NEXT_ACTION

1. 实现A股市场切换：设置`abupy.env.g_market_target = EMarketTargetType.E_MARKET_TARGET_CN`，并验证A股佣金计算函数`calc_commision_cn`的印花税+佣金逻辑。

2. 接入A股历史数据源：使用`ABuSymbolPd.make_kl_df()`获取A股股票数据（如'601398'工商银行），验证数据结构（open/high/low/close/volume）与美股一致。

3. 构建A股突破策略回测：将买入因子`AbuFactorBuyBreak`的xd参数设置为42/60，卖出因子使用`AbuFactorAtrNStop`，在A股8只股票池上运行`run_loop_back`并对比美股结果。

4. 实现角度选股因子A股验证：使用`AbuPickRegressAngMinMax`在A股股票池上选股，对比`threshold_ang_min=0`时筛选结果，分析A股趋势特征与美股差异。

5. 调整仓位管理基数：针对A股全市场股票数量（约5000只），设置`abupy.beta.atr.g_atr_pos_base = 0.0015`，确保买入成交比例>30%且资金利用率>70%。

6. 开发Grid Search参数优化：使用`ABuGridHelper.gen_factor_grid()`生成买入/卖出因子参数排列组合，在A股数据上运行`GridSearch`寻找最优参数组合。

7. 实现中文策略生成器验证：使用`abu.gen_buy_from_chinese()`输入中文描述"连续下跌5天买入"，生成策略代码并在A股上回测验证胜率。

8. 部署多进程并行回测：使用`AbuPickTimeMaster.do_symbols_with_same_factors_process(n_process_kl=64, n_process_pick_time=8)`对A股500只股票并行回测，对比串行效率。

9. 设计A股-specific卖出因子：针对A股T+1制度，开发"次日开盘止损"卖出因子，替换或补充`AbuFactorPreAtrNStop`的盘中暴跌保护逻辑。

10. 验证满仓乘数度量：在A股全市场回测中对比`enable_stocks_full_rate_factor=True/False`的策略收益差异，确保与基准（沪深300）可比。

11. 编写A股回测基准对比：使用`AbuMetricsBase.plot_returns_cmp()`对比策略收益与沪深300指数收益，计算Alpha、Beta、信息比率等度量指标。

12. 保存回测结果复用：使用`abu.store_abu_result_tuple()`将A股回测结果序列化，便于后续机器学习Ump模块训练使用。
