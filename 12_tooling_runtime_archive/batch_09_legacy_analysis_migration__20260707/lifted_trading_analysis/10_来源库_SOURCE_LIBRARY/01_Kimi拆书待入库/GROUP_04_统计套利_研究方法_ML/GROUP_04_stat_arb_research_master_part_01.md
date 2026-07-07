# Group 04 — 统计套利 · 研究流程 · 机器学习（Part 01 / 03）
> 研究流程标准（SOP）+ 统计套利原型库
> 覆盖书目：Pole《统计套利》| Chan《量化交易》| ISLR《统计学习导论》| CV《量化交易：算法、分析、数据、模型和优化》| Python-book《零基础搭建量化投资系统》| GPT-book《GPT时代的量化交易》

---

# 第一章：研究流程标准（SOP）
> 七阶段流水线：从想法生成到上线监控的完整研究协议

## 1.1 流程全景图

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  Phase 1    │ → │  Phase 2    │ → │  Phase 3    │ → │  Phase 4    │
│   想法生成   │   │  数据工程   │   │  特征构建   │   │  模型构建   │
│   Idea Gen  │   │    Data     │   │   Features  │   │    Model    │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
                                                        │
       ┌────────────────────────────────────────────────┘
       ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  Phase 7    │ ← │  Phase 6    │ ← │  Phase 5    │
│  上线监控   │ ← │  稳健性检验  │ ← │   回测验证   │
│   Live Ops  │   │  Robustness │   │  Backtest   │
└─────────────┘   └─────────────┘   └─────────────┘
```

**核心原则**：每个Phase必须有明确的准入/准出标准（Entry/Exit Criteria），不可跳阶段。（Chan, p.31-38; CV, p.98-102）

---

## 1.2 Phase 1：想法生成（Idea Generation）

### 1.2.1 想法来源分类

| 来源类型 | 描述 | 示例 | 参考 |
|---------|------|------|------|
| 经济直觉 | 基于市场微观结构或行为金融学理论 | 均值回复、动量效应 | Chan, p.15-22 |
| 文献挖掘 | 学术论文或行业报告中的可复现策略 | Fama-French因子、Carhart四因子 | CV, p.45-50 |
| 数据驱动 | 从数据模式中观察到的稳定异常 | 季节性效应、开盘缺口 | Pole, p.89-94 |
| 跨市场移植 | 将A市场验证的策略适配到B市场 | 美股配对交易→A股行业ETF配对 | GPT-book, p.78-82 |
| 技术组合 | 将已知策略组件重新组合 | 因子动量+均值回复双层结构 | Python-book, p.234-238 |

### 1.2.2 想法筛选清单（Pass Gate）

在任何一个想法进入Phase 2之前，必须回答以下问题：

```
□ 经济逻辑：该策略背后的经济机制是什么？为什么市场会长期存在这种无效性？
□ 行为基础：是机构行为约束、信息不对称还是心理偏差导致的？（Chan, p.18-20）
□ 容量评估：策略的容量上限是多少？预期AUM范围？
□ 摩擦评估：考虑交易成本、滑点、税费后，策略是否仍然有效？
□ 衰减预期：该Alpha的半衰期估计？（Chan, p.127-129）
□ 可执行性：是否可在实际交易系统中实现？延迟要求？
```

**退出标准**：通过至少4/6项筛选，并书面记录经济逻辑。未通过的想法进入「冷冻库」，6个月后复核。

---

## 1.3 Phase 2：数据工程（Data Engineering）

### 1.3.1 数据需求矩阵

| 策略类型 | 最低数据频率 | 数据类型 | 最小历史跨度 | 参考 |
|---------|------------|---------|------------|------|
| 日频配对交易 | 日K线 | OHLCV + 基本面 | 3年 | Pole, p.45-48 |
| 横截面因子 | 日K线 | OHLCV + 财务数据 | 5年 | CV, p.112-115 |
| 高频统计套利 | Tick/快照 | 逐笔成交 + 订单簿 | 6个月 | GPT-book, p.198-202 |
| 期货期限结构 | 日K线 | 连续合约 + 展期数据 | 5年 | Chan, p.95-98 |
| 期权波动率套利 | 日K线 | 期权链 + 隐含波动率曲面 | 2年 | CV, p.156-160 |

### 1.3.2 数据清洗SOP

```python
# 伪代码：数据清洗流水线
# 参考：Python-book, p.156-178; Chan, p.65-72

def data_cleaning_pipeline(raw_data):
    # Step 1: 去重
    deduped = remove_duplicates(raw_data, keys=['date', 'symbol'])
    
    # Step 2: 处理停牌/缺失
    # 规则：连续停牌>20天剔除；<20天前向填充
    filled = handle_missing(deduped, method='ffill', max_gap=20)
    
    # Step 3: 极值检测（3-sigma + MAD双检）
    outliers = detect_outliers(filled, method=['zscore', 'mad'], threshold=3)
    
    # Step 4: 收益率异常
    # 日收益率>30%需人工复核（除新股/复牌）
    returns = calculate_returns(filled)
    flagged = flag_extreme_returns(returns, threshold=0.30)
    
    # Step 5: 幸存者偏差处理
    # 必须包含历史成分股/退市股数据（Chan, p.67-68）
    universe = include_delisted(filled)
    
    # Step 6: 前复权处理
    adjusted = adjust_splits_dividends(universe, method='backward')
    
    # Step 7: 数据审计日志
    log_audit_trail(adjusted, steps_applied)
    
    return adjusted
```

### 1.3.3 数据分割协议

```
┌─────────────────────────────────────────────────────────────┐
│                      总数据集 (Total Dataset)                  │
│  2000-01-01  ─────────────────────────────────  2024-12-31  │
├──────────────────┬──────────────────┬───────────────────────┤
│   训练集 Train   │    验证集 Val    │     测试集 Test       │
│   (In-Sample)    │  (Out-of-Sample) │  (Final Holdout)      │
│   2000-2016      │    2017-2020     │     2021-2024         │
│   60%            │    25%           │     15%               │
├──────────────────┴──────────────────┴───────────────────────┤
│  训练集：参数估计 + 模型选择                                  │
│  验证集：超参数调优 + 策略筛选（只能看一次！）                  │
│  测试集：最终报告绩效（严禁偷看直至策略冻结）                    │
└─────────────────────────────────────────────────────────────┘
```

**关键纪律**：测试集只能使用一次。任何"测试集效果不好就回去改策略"的行为都是样本外作弊。（ISLR, p.176-178; Chan, p.69-70）

---

## 1.4 Phase 3：特征构建（Feature Engineering）

### 1.4.1 特征分类体系

| 层级 | 类别 | 示例 | 计算复杂度 |
|------|------|------|-----------|
| L0：原始数据 | OHLCV | 开高低收量 | O(1) |
| L1：技术指标 | 动量/均值/波动 | RSI, MA, ATR | O(n) |
| L2：统计特征 | 分布/相关性 | Z-score, 相关系数, 偏度 | O(n) |
| L3：经济特征 | 因子暴露 | 市值, BM, 动量因子 | O(n·m) |
| L4：衍生特征 | 交互/非线性 | 因子×行业, 多项式特征 | O(n·m²) |
| L5：另类数据 | 文本/网络 | 舆情得分, 供应链网络 | 视数据源而定 |

### 1.4.2 特征构造原则

1. **前瞻性保护**：任何特征在时刻t的计算只能使用t及之前的数据（Chan, p.72-74）
2. **标准化**：横截面标准化（rank或z-score）优于绝对值（CV, p.118-120）
3. **衰减权重**：近期数据给予更高权重（EWMA > SMA）
4. **特征稳定性**：特征IC的时间序列稳定性比平均IC更重要
5. **正交化**：去除与已知因子的共线性（GPT-book, p.156-158）

```python
# 伪代码：安全的特征计算（无前视偏差）
# 参考：Chan, p.72-74; Python-book, p.201-205

def safe_feature_calculation(data, feature_func, lookback_window):
    """
    严格的前瞻性保护：在日期d，仅使用[d-lookback, d-1]的数据
    """
    features = {}
    for date in trading_dates:
        # 严格使用截至昨日的数据
        available_data = data.loc[:date].iloc[:-1]  # exclude current day
        
        if len(available_data) >= lookback_window:
            window = available_data.tail(lookback_window)
            features[date] = feature_func(window)
    
    return pd.Series(features)
```

---

## 1.5 Phase 4：模型构建（Model Building）

### 1.5.1 模型选择决策树

```
                    ┌─────────────────┐
                    │   问题类型？     │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
      ┌─────────┐     ┌──────────┐     ┌──────────┐
      │ 预测收益  │     │ 分类信号  │     │ 组合权重  │
      │回归问题  │     │（买/卖）  │     │  优化     │
      └────┬────┘     └────┬─────┘     └────┬─────┘
           │               │                │
     ┌─────┴─────┐   ┌─────┴──────┐   ┌─────┴──────┐
     ▼           ▼   ▼            ▼   ▼            ▼
┌─────────┐ ┌────────┐ ┌─────────┐ ┌────────┐ ┌──────────┐
│线性回归  │ │树模型   │ │逻辑回归  │ │XGBoost │ │均值-方差  │
│(OLS/Ridge│ │(RF/GBM)│ │         │ │        │ │Black-Lit │
│/Lasso)  │ │        │ │         │ │        │ │NPEB      │
└─────────┘ └────────┘ └─────────┘ └────────┘ └──────────┘

参考：ISLR, p.59-62（线性模型）, p.319-324（树模型）, p.130-137（正则化）
      CV, p.132-140（NPEB/Black-Litterman）
```

### 1.5.2 模型复杂度控制

| 方法 | 适用场景 | 超参数 | 参考 |
|------|---------|--------|------|
| L1正则化（Lasso） | 特征选择 | λ | ISLR, p.219-227 |
| L2正则化（Ridge） | 处理多重共线性 | λ | ISLR, p.215-219 |
| Elastic Net | 高维特征 | α, λ | ISLR, p.222-223 |
| 特征数量限制 | 防止过拟合 | max_features | Chan, p.112-115 |
| 模型集成 | 降低方差 | n_estimators | ISLR, p.316-319 |

### 1.5.3 时间序列交叉验证（Time-Series CV）

```python
# 伪代码：滚动原点交叉验证（Rolling Origin CV）
# 参考：ISLR, p.184-185; Chan, p.104-106; CV, p.234-238

def time_series_cv(data, model, n_splits=5, train_min_size=252):
    """
    滚动原点交叉验证：严格保持时间顺序
    严禁使用随机K折CV于时间序列数据！
    """
    results = []
    total_len = len(data)
    
    for i in range(n_splits):
        # 训练终点逐步后移
        train_end = train_min_size + i * ((total_len - train_min_size) // n_splits)
        test_end = min(train_end + 63, total_len)  # 63天≈3个月测试期
        
        train_data = data.iloc[:train_end]
        test_data = data.iloc[train_end:test_end]
        
        # 在训练集上调参（可嵌套验证集）
        model.fit(train_data)
        
        # 在测试集上评估（仅一次！）
        performance = evaluate(model, test_data)
        results.append(performance)
    
    return results
```

**为什么不能用随机K折**：时间序列的自相关性会导致训练集和测试集信息泄漏，严重低估过拟合风险。（Chan, p.104-105）

---

## 1.6 Phase 5：回测验证（Backtesting）

### 1.6.1 回测引擎最小要求

```python
# 伪代码：事件驱动回测引擎骨架
# 参考：Chan, p.76-88; Python-book, p.245-267; CV, p.202-210

class BacktestEngine:
    def __init__(self, data, strategy, initial_capital=1e7):
        self.data = data
        self.strategy = strategy
        self.cash = initial_capital
        self.positions = {}
        self.trades = []
        self.nav_history = []
    
    def run(self):
        for timestamp, bar in self.data.iterrows():
            # 1. 策略生成信号（使用前向保护的特征）
            signals = self.strategy.on_bar(timestamp, bar, self.positions)
            
            # 2. 执行引擎（含滑点模型）
            for signal in signals:
                executed_price = self.simulate_execution(
                    signal, 
                    slippage_model='proportional',  # 或固定延迟
                    latency_ms=50
                )
                self.execute_trade(signal, executed_price)
            
            # 3. 日终估值
            nav = self.calculate_nav(timestamp)
            self.nav_history.append((timestamp, nav))
            
            # 4. 风控检查
            if self.risk_check() == 'STOP':
                self.emergency_liquidate(timestamp)
                break
        
        return BacktestReport(self.nav_history, self.trades)
    
    def simulate_execution(self, signal, slippage_model='proportional', latency_ms=50):
        """
        滑点模型：
        - 固定滑点：每笔交易±0.1%（ Chan, p.82-83 建议保守估计）
        - 比例滑点：与订单量/市场深度成正比
        - 延迟模型：latency_ms > 0 确保信号生成与执行分离
        """
        # ... 实现 ...
```

### 1.6.2 回测绩效指标（必须全部报告）

| 指标 | 公式/说明 | 最低可接受阈值 | 参考 |
|------|----------|--------------|------|
| 年化收益率 | (1+r)^(252/n) - 1 | > 无风险利率+5% | CV, p.204-205 |
| 年化波动率 | std(日收益) × √252 | < 20%（股票型） | CV, p.204-205 |
| 夏普比率 | (Rp - Rf) / σp | > 1.0 | Chan, p.85-86 |
| 最大回撤 | max(峰值-谷值)/峰值 | < 15% | CV, p.205 |
| Calmar比率 | 年化收益 / |最大回撤| | > 1.0 | Chan, p.86 |
| 胜率 | 盈利交易次数/总交易次数 | > 45% | Pole, p.134-135 |
| 盈亏比 | 平均盈利/平均亏损 | > 1.2 | Pole, p.134-135 |
| 信息比率 | α / TE（相对基准） | > 0.5 | CV, p.206-207 |
| 周转率 | 年度交易额 / AUM | 视策略而定 | Chan, p.86-87 |
| 容量估计 | 基于滑点模型的反向求解 | > 目标AUM | GPT-book, p.92-94 |

### 1.6.3 回测执行纪律

1. **滑点保守主义**：回测滑点必须 ≥ 实盘观测滑点的1.5倍（Chan, p.82-83）
2. **交易费用全包**：佣金 + 印花税 + 冲击成本 + 融资利率
3. **不可交易股票过滤**：ST股、停牌股、涨跌停板必须排除
4. **信号-执行分离**：信号基于收盘数据生成，次日开盘执行（或更保守）
5. **再平衡频率 realistic**：日频策略不能假设瞬间完成全部调仓
6. **现金管理**：未投资现金按货基收益率计息（GPT-book, p.245-248）

---

## 1.7 Phase 6：稳健性检验（Robustness Checks）

### 1.7.1 必须执行的检验清单

| 检验类型 | 具体方法 | 通过标准 | 参考 |
|---------|---------|---------|------|
| **参数敏感性** | 在超参数邻域±20%范围内测试 | 夏普比率变化 < 20% | Chan, p.106-110 |
| **子样本稳定性** | 将数据分为2-3段分别回测 | 各段夏普 > 0.8×总体 | CV, p.236-238 |
| **蒙特卡洛模拟** | 对收益率序列进行bootstrap重采样 | 5%分位夏普 > 0 | Chan, p.108-109 |
| **交易成本压力测试** | 滑点×2、佣金×3 | 夏普仍 > 0.5 | Pole, p.156-158 |
| **不同市场体制** | 牛市/熊市/震荡市分别测试 | 避免仅在单方向市场有效 | GPT-book, p.267-270 |
| **随机化检验** | 随机打乱信号、比较原策略 vs 随机策略 | 原策略显著优于95%随机版本 | CV, p.240-242 |
| **上线前纸交易** | 至少3个月实时模拟交易 | 纸交易夏普 vs 回测夏普 > 0.7 | Chan, p.110-112 |

### 1.7.2 子样本稳定性分析模板

```python
# 伪代码：子样本稳健性检验
# 参考：CV, p.236-238; Chan, p.106-108

def subsample_robustness_test(data, strategy, n_segments=3):
    """
    将数据分为n段，每段独立回测
    用于检测策略是否依赖特定历史时期
    """
    segment_length = len(data) // n_segments
    results = []
    
    for i in range(n_segments):
        start = i * segment_length
        end = start + segment_length if i < n_segments - 1 else len(data)
        segment = data.iloc[start:end]
        
        result = backtest(strategy, segment)
        results.append({
            'period': f"{segment.index[0]} to {segment.index[-1]}",
            'sharpe': result.sharpe,
            'return': result.annual_return,
            'max_dd': result.max_drawdown
        })
    
    # 变异系数检查：CV = std/mean
    sharpes = [r['sharpe'] for r in results]
    cv = np.std(sharpes) / np.mean(sharpes)
    
    return {
        'segment_results': results,
        'sharpe_cv': cv,
        'pass': cv < 0.3  # 夏普变异系数 < 30%
    }
```

---

## 1.8 Phase 7：上线监控（Live Monitoring）

### 1.8.1 上线检查清单

```
□ 纸交易验证：≥3个月纸交易，夏普比率 ≥ 0.7 × 回测夏普
□ 容量确认：实盘AUM ≤ 回测容量估计的50%
□ 风控参数：单一策略止损线（-5%警告/-8%减仓/-12%清盘）
□ 技术就绪：延迟监控、异常报警、自动降级方案
□ 合规审查：策略符合监管要求和内部风控政策
□ 对手方准备：经纪商接口测试、应急交易通道
□ 团队就绪：7×24小时值班表、升级机制
```

### 1.8.2 实时监控仪表盘（必须指标）

| 指标 | 频率 | 黄色预警 | 红色预警 | 动作 |
|------|------|---------|---------|------|
| 日收益率 | 日 | <-3% | <-5% | 检查/减仓 |
| 累计回撤 | 日 | >5% | >8% | 警告/减仓/清盘 |
| 夏普(滚动63日) | 日 | <0.5×预期 | <0 | 复核/暂停 |
| 换手率偏差 | 日 | >1.5×预期 | >2×预期 | 检查执行 |
| 信号覆盖率 | 日 | <80% | <60% | 检查数据 |
| 与回测偏离 | 周 | >2σ | >3σ | 深度分析 |

### 1.8.3 策略退役标准

```
触发条件（任一）：
1. 滚动63日夏普 < 0 持续21个交易日
2. 累计回撤 > 最大历史回撤的1.5倍
3. 策略逻辑的经济基础已不存在（如监管变化）
4. 容量利用率 > 100%且绩效持续衰减
5. 存在未解释的回测-实盘偏差 > 3σ

退役流程：
1. 触发 → 2. 风险评估 → 3. 减仓50% → 4. 分析根因 → 5. 修复/退役决策
```

---

# 第二章：统计套利原型库
> 每个原型包含：实现步骤（伪代码级）、关键参数、失败模式、（书名+页码）
> 覆盖：配对交易、协整策略、均值回复、横截面动量、ETF套利、波动率套利、因子套利

---

## 2.1 原型A：距离法配对交易（Distance-Based Pairs Trading）
> 经典入门策略，基于价格序列的欧氏距离寻找配对

### 2.1.1 经济逻辑
同一行业/相似基本面的两只股票，其价格比率应在长期围绕均值波动。当价格距离异常扩大时，做空高价股+做多低价股，待收敛时平仓。（Pole, p.15-28; Chan, p.75-80）

### 2.1.2 实现步骤（伪代码）

```python
# 参考：Pole, p.45-68; Chan, p.75-80; Python-book, p.256-260

class DistancePairsTrading:
    """
    距离法配对交易策略
    """
    
    # ============ Step 1: 配对筛选（Formation Period） ============
    def find_pairs(self, universe, formation_data, n_top=20):
        """
        formation_data: 通常为12个月的日价格数据
        """
        pairs = []
        for stock_a, stock_b in combinations(universe, 2):
            # 标准化价格序列（起点归一化为1）
            norm_a = formation_data[stock_a] / formation_data[stock_a].iloc[0]
            norm_b = formation_data[stock_b] / formation_data[stock_b].iloc[0]
            
            # 计算SSD（Sum of Squared Distances）
            ssd = np.sum((norm_a - norm_b) ** 2)
            
            # 计算相关性（辅助筛选）
            correlation = norm_a.corr(norm_b)
            
            pairs.append({
                'pair': (stock_a, stock_b),
                'ssd': ssd,
                'correlation': correlation
            })
        
        # 按SSD升序排列，取top N
        pairs.sort(key=lambda x: x['ssd'])
        return pairs[:n_top]
    
    # ============ Step 2: 交易信号生成（Trading Period） ============
    def generate_signals(self, pair, trading_data, lookback=20, entry_z=2.0, exit_z=0.5):
        """
        基于价差的Z-Score生成交易信号
        """
        stock_a, stock_b = pair['pair']
        price_a = trading_data[stock_a]
        price_b = trading_data[stock_b]
        
        # 计算价差 spread = ln(Pa) - ln(Pb) 或 Pa/Pb
        # Pole推荐对数价差：更对称、更稳定
        spread = np.log(price_a / price_b)
        
        # 滚动均值和标准差（前瞻性保护：用截至昨日的数据）
        spread_mean = spread.rolling(window=lookback).mean().shift(1)
        spread_std = spread.rolling(window=lookback).std().shift(1)
        
        # Z-Score
        zscore = (spread - spread_mean) / spread_std
        
        # 信号生成
        signals = []
        position = 0  # 0=空仓, 1=做多spread, -1=做空spread
        
        for t in range(len(trading_data)):
            z = zscore.iloc[t]
            
            if position == 0 and abs(z) > entry_z:
                # 开仓信号
                direction = 1 if z < -entry_z else -1  # z<-2 → 做多spread
                position = direction
                signals.append({
                    'date': trading_data.index[t],
                    'action': 'OPEN',
                    'direction': direction,
                    'zscore': z,
                    'stock_a': 'BUY' if direction == 1 else 'SELL',
                    'stock_b': 'SELL' if direction == 1 else 'BUY'
                })
            
            elif position != 0 and abs(z) < exit_z:
                # 平仓信号
                signals.append({
                    'date': trading_data.index[t],
                    'action': 'CLOSE',
                    'direction': -position,
                    'zscore': z
                })
                position = 0
            
            # 止损：|z| > 3σ 且方向不利
            elif position != 0 and z * position < -3.0:
                signals.append({
                    'date': trading_data.index[t],
                    'action': 'STOP_LOSS',
                    'direction': -position,
                    'zscore': z
                })
                position = 0
        
        return signals
    
    # ============ Step 3: 仓位 sizing（Kelly-inspired） ============
    def position_sizing(self, capital, price_a, price_b, volatility_a, volatility_b):
        """
        等额市值配比，可考虑波动率调整
        Chan推荐：根据历史波动率调整仓位使风险贡献相等
        """
        vol_ratio = volatility_a / volatility_b
        
        # 假设总风险预算为资本的10%
        risk_budget = capital * 0.10
        
        # 每单位波动的风险
        unit_risk_a = price_a * volatility_a
        unit_risk_b = price_b * volatility_b
        
        shares_a = int(risk_budget / (2 * unit_risk_a))
        shares_b = int(risk_budget / (2 * unit_risk_b))
        
        return shares_a, shares_b
```

### 2.1.3 关键参数表

| 参数 | 符号 | 推荐值 | 范围 | 敏感度 | 参考 |
|------|------|--------|------|--------|------|
| 配对形成期 | T_form | 12个月 | 6-24月 | 中 | Pole, p.52-53 |
| 交易期 | T_trade | 6个月 | 3-12月 | 低 | Pole, p.52-53 |
| Z-Score计算窗口 | lookback | 20日 | 10-60日 | **高** | Chan, p.78-79 |
| 开仓阈值 | entry_z | 2.0 | 1.5-2.5 | **高** | Pole, p.102-103 |
| 平仓阈值 | exit_z | 0.5 | 0.0-1.0 | 中 | Pole, p.103-104 |
| 止损阈值 | stop_z | 3.0 | 2.5-4.0 | 中 | Chan, p.80 |
| 最大配对数 | n_pairs | 20 | 10-50 | 低 | Pole, p.55-56 |

### 2.1.4 失败模式（Pole, p.156-165; Chan, p.93-95）

| 失败模式 | 检测方法 | 修复/缓解 | 参考 |
|---------|---------|----------|------|
| **结构性断裂** | CUSUM检验或Chow检验 | 缩短lookback，引入regime切换 | Pole, p.158-160 |
| **均值漂移** | 滚动ADF检验p值 | 动态退出配对，不等待收敛 | Chan, p.93-94 |
| **基本面分化** | 配对公司公告跟踪 | 加入基本面过滤（同行业+相似ROE） | GPT-book, p.156-158 |
| **收敛时间超预期** | 记录平均持有期 | 设置最大持有期（如20日强制平仓） | Pole, p.134-135 |
| **尾部风险** | 价差分布偏度/峰度 | 买入OTM期权保护或降低杠杆 | Chan, p.94-95 |
| **容量限制** | 市场深度分析 | 限制单对配对的最大AUM | Pole, p.165-168 |

---

## 2.2 原型B：协整法配对交易（Cointegration-Based Pairs Trading）
> 基于Engle-Granger两步法的统计套利，比距离法更严谨

### 2.2.1 经济逻辑
如果两只股票的价格序列是协整的，则它们的线性组合是平稳的（均值为0的I(0)过程）。这种统计关系比简单相关性更稳定，因为它捕捉了长期均衡关系。（Pole, p.70-85; CV, p.168-172）

### 2.2.2 实现步骤（伪代码）

```python
# 参考：Pole, p.70-85; CV, p.168-172; Chan, p.80-83

import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint

class CointegrationPairsTrading:
    
    # ============ Step 1: 协整检验 ============
    def cointegration_screen(self, universe, formation_data, p_value_threshold=0.05):
        """
        Engle-Granger两步法协整检验
        """
        cointegrated_pairs = []
        
        for stock_a, stock_b in combinations(universe, 2):
            # 方法1：直接用statsmodels的coint函数（EG检验）
            score, pvalue, crit_values = coint(
                formation_data[stock_a], 
                formation_data[stock_b]
            )
            
            if pvalue < p_value_threshold:
                # 通过协整检验，估计对冲比率
                X = sm.add_constant(formation_data[stock_b])
                model = sm.OLS(formation_data[stock_a], X).fit()
                hedge_ratio = model.params[stock_b]
                intercept = model.params['const']
                
                # 检验残差的平稳性（ADF检验）
                residuals = model.resid
                adf_stat, adf_pvalue, _, _, critical_values, _ = adfuller(residuals)
                
                # 计算半衰期（Ornstein-Uhlenbeck参数）
                halflife = self.calculate_halflife(residuals)
                
                cointegrated_pairs.append({
                    'pair': (stock_a, stock_b),
                    'eg_pvalue': pvalue,
                    'adf_pvalue': adf_pvalue,
                    'hedge_ratio': hedge_ratio,
                    'intercept': intercept,
                    'halflife': halflife,
                    'residual_std': residuals.std()
                })
        
        # 按EG检验p值排序
        cointegrated_pairs.sort(key=lambda x: x['eg_pvalue'])
        return cointegrated_pairs
    
    # ============ Step 2: 半衰期计算（Chan方法） ============
    def calculate_halflife(self, residuals):
        """
        使用Ornstein-Uhlenbeck过程估计半衰期
        参考：Chan, p.97-99
        """
        # dy(t) = λ*y(t-1)*dt + dW(t)
        # 通过AR(1)回归估计λ
        
        y_lag = residuals.shift(1).dropna()
        y_diff = residuals.diff().dropna()
        
        # 对齐索引
        aligned = pd.DataFrame({'y_lag': y_lag, 'y_diff': y_diff}).dropna()
        
        X = sm.add_constant(aligned['y_lag'])
        model = sm.OLS(aligned['y_diff'], X).fit()
        
        lambda_param = model.params['y_lag']
        
        # 半衰期 = ln(2) / |λ|
        if lambda_param < 0:
            halflife = np.log(2) / abs(lambda_param)
        else:
            halflife = np.inf  # 不均值回复
        
        return halflife
    
    # ============ Step 3: 信号生成 ============
    def generate_signals(self, pair, trading_data, entry_z=1.0, exit_z=0.0):
        """
        基于协整残差的Z-Score交易
        关键差异：使用对冲比率构建spread，而非1:1
        """
        stock_a, stock_b = pair['pair']
        hedge_ratio = pair['hedge_ratio']
        
        # 构建spread: residual = Pa - β*Pb - α
        spread = (trading_data[stock_a] 
                  - hedge_ratio * trading_data[stock_b])
        
        # 使用formation期统计量标准化
        spread_mean = pair.get('residual_mean', 0)
        spread_std = pair['residual_std']
        
        zscore = (spread - spread_mean) / spread_std
        
        # 信号逻辑与距离法类似，但基于协整残差
        signals = []
        position = 0
        
        for t in range(len(trading_data)):
            z = zscore.iloc[t]
            
            if position == 0 and abs(z) > entry_z:
                direction = 1 if z < -entry_z else -1
                position = direction
                signals.append({
                    'date': trading_data.index[t],
                    'action': 'OPEN',
                    'direction': direction,
                    'zscore': z,
                    'hedge_ratio': hedge_ratio,
                    'spread': spread.iloc[t]
                })
            
            elif position != 0 and (abs(z) < exit_z or position * z < -2.5):
                signals.append({
                    'date': trading_data.index[t],
                    'action': 'CLOSE',
                    'reason': 'exit_z' if abs(z) < exit_z else 'stop_loss',
                    'zscore': z
                })
                position = 0
        
        return signals
    
    # ============ Step 4: 动态对冲比率更新 ============
    def update_hedge_ratio(self, rolling_window=60):
        """
        定期更新对冲比率（Kalman Filter或滚动OLS）
        参考：Chan, p.83-85（Kalman Filter方法）
        """
        # Kalman Filter实现（更优）
        # 或滚动OLS（更简单）
        pass
```

### 2.2.3 关键参数表

| 参数 | 符号 | 推荐值 | 范围 | 敏感度 | 参考 |
|------|------|--------|------|--------|------|
| 协整检验p值阈值 | p_coint | 0.05 | 0.01-0.10 | **高** | Pole, p.76-78 |
| ADF残差检验p值 | p_adf | 0.05 | 0.01-0.10 | **高** | CV, p.170-171 |
| 半衰期过滤 | max_halflife | 30日 | 15-60日 | **高** | Chan, p.98-99 |
| 开仓Z-Score | entry_z | 1.0 | 0.5-2.0 | **高** | Pole, p.104-105 |
| 对冲比率更新频率 | hedge_update | 每日 | 日/周 | 中 | Chan, p.83-85 |
| 最大持有期 | max_holding | 2×半衰期 | 自适应 | 中 | Chan, p.99-100 |

### 2.2.4 失败模式（Pole, p.160-165; Chan, p.93-97）

| 失败模式 | 检测方法 | 修复/缓解 | 参考 |
|---------|---------|----------|------|
| **伪协整**（spurious cointegration） | 样本外ADF检验 | Bonferroni校正多重检验；增加形成期长度 | Pole, p.160-162 |
| **协整关系破裂** | 滚动协整检验 | 定期重新筛选配对（月度） | Chan, p.95-96 |
| **对冲比率漂移** | 滚动OLS的β时间序列 | 使用Kalman Filter动态更新 | Chan, p.83-85 |
| **半衰期过长** | halflife > 30日 | 剔除；或降低仓位 | Chan, p.98-99 |
| **季节性伪信号** | 按月份分解绩效 | 加入月份固定效应控制 | CV, p.172-174 |

---

## 2.3 原型C：均值回复策略（Ornstein-Uhlenbeck Mean Reversion）
> 直接建模价格/价差的均值回复过程，半衰期是核心参数

### 2.3.1 经济逻辑
资产价格（或组合spread）服从OU过程：dX(t) = θ(μ - X(t))dt + σdW(t)，其中θ决定回归速度。通过估计半衰期，可以优化持有期和仓位大小。（Chan, p.95-103; Pole, p.100-112）

### 2.3.2 实现步骤（伪代码）

```python
# 参考：Chan, p.95-103; Pole, p.100-112

class OU_MeanReversion:
    
    def fit_ou_parameters(self, price_series):
        """
        估计OU过程参数
        dx(t) = theta * (mu - x(t)) * dt + sigma * dW
        
        通过离散化：x(t) - x(t-1) = theta*(mu - x(t-1))*dt + eps
        即：AR(1)模型
        """
        y = price_series.diff().dropna()
        x_lag = price_series.shift(1).dropna()
        
        # OLS回归：Δx = a + b*x_{t-1} + ε
        X = sm.add_constant(x_lag.loc[y.index])
        model = sm.OLS(y, X).fit()
        
        a = model.params['const']
        b = model.params[x_lag.name]
        
        # 推导OU参数
        dt = 1  # 假设日频率
        theta = -b / dt
        mu = a / (theta * dt)
        sigma = np.std(model.resid) / np.sqrt(dt)
        
        # 半衰期
        halflife = np.log(2) / theta if theta > 0 else np.inf
        
        return {
            'theta': theta,
            'mu': mu,
            'sigma': sigma,
            'halflife': halflife,
            'r_squared': model.rsquared
        }
    
    def generate_signal(self, params, current_price, entry_z=1.0):
        """
        基于当前价格与OU均衡水平的偏离生成信号
        """
        zscore = (current_price - params['mu']) / (params['sigma'] / np.sqrt(2 * params['theta']))
        
        if zscore < -entry_z:
            return {'signal': 'BUY', 'zscore': zscore, 'expected_return': params['mu'] - current_price}
        elif zscore > entry_z:
            return {'signal': 'SELL', 'zscore': zscore, 'expected_return': current_price - params['mu']}
        else:
            return {'signal': 'HOLD', 'zscore': zscore}
    
    def kelly_sizing(self, params, capital):
        """
        基于OU参数的Kelly最优仓位
        参考：Chan, p.101-103
        
        f* = (μ - r) / σ²  的OU版本
        """
        mu = params['mu']
        sigma = params['sigma']
        
        # 简化Kelly：与偏离程度成正比，与方差成反比
        f = abs(mu) / (sigma ** 2)
        
        # 半Kelly以保守
        half_kelly = 0.5 * f
        
        # 限制最大杠杆
        leverage = min(half_kelly, 2.0)
        
        return capital * leverage
```

### 2.3.3 关键参数表

| 参数 | 符号 | 推荐值 | 范围 | 敏感度 | 参考 |
|------|------|--------|------|--------|------|
| 估计窗口 | T_est | 252日 | 126-504日 | **高** | Chan, p.97 |
| 开仓Z-Score | entry_z | 1.0-1.5 | 0.5-2.0 | **高** | Chan, p.100-101 |
| Kelly分数 | kelly_frac | 0.5（半Kelly） | 0.25-0.5 | **高** | Chan, p.101-103 |
| 最大杠杆 | max_lev | 2.0 | 1.5-3.0 | **高** | Chan, p.102-103 |
| 最小R² | min_r2 | 0.05 | 0.02-0.10 | 中 | Pole, p.108-109 |
| 最大半衰期 | max_hl | 30日 | 20-60日 | **高** | Chan, p.98-99 |

### 2.3.4 失败模式（Chan, p.127-133; Pole, p.156-160）

| 失败模式 | 检测方法 | 修复/缓解 | 参考 |
|---------|---------|----------|------|
| **OU假设失效**（price random walk） | ADF检验无法拒绝单位根 | 不交易该资产；切换至动量策略 | Chan, p.96-97 |
| **参数估计不稳定** | 滚动窗口参数时间序列 | 使用贝叶斯更新或更长的估计窗口 | Pole, p.158 |
| **杠杆过高导致爆仓** | 最大回撤 > 预期 | 严格限制Kelly杠杆上限为2× | Chan, p.102-103 |
| **方差低估** | 实际波动 > 模型预测 | 使用GARCH调整波动率估计 | CV, p.174-176 |

---

## 2.4 原型D：横截面动量/反转策略（Cross-Sectional Momentum/Reversal）
> 利用股票间的相对强弱进行多空组合，是市场因子投资的核心

### 2.4.1 经济逻辑
横截面动量：过去表现好的股票在未来短期内继续跑赢（Jegadeesh & Titman, 1993）。横截面反转： losers在未来跑赢 winners（短期过度反应后的修正）。两者在不同时间尺度上可能共存。（CV, p.112-120; GPT-book, p.145-152）

### 2.4.2 实现步骤（伪代码）

```python
# 参考：CV, p.112-120; GPT-book, p.145-152; Chan, p.107-110

class CrossSectionalMomentum:
    
    def __init__(self, lookback=20, holding_period=20, n_quantiles=10):
        self.lookback = lookback
        self.holding_period = holding_period
        self.n_quantiles = n_quantiles
    
    def generate_signals(self, returns_matrix, current_date):
        """
        横截面动量信号生成
        
        Parameters:
        -----------
        returns_matrix : DataFrame (dates × stocks)
        current_date : 当前调仓日
        """
        # Step 1: 计算lookback期的累计收益
        start_date = current_date - pd.Timedelta(days=self.lookback * 1.5)
        past_returns = returns_matrix.loc[start_date:current_date]
        
        # 跳过最近1周（1-week skip，避免短期反转/微观结构噪声）
        skip_date = current_date - pd.Timedelta(days=7)
        formation_returns = past_returns.loc[:skip_date]
        
        cumulative_returns = (1 + formation_returns).prod() - 1
        
        # Step 2: 按累计收益排序，分十档
        quantiles = pd.qcut(
            cumulative_returns, 
            q=self.n_quantiles, 
            labels=False,
            duplicates='drop'
        )
        
        # Step 3: 构建多空组合
        # 动量：做多top quantile，做空bottom quantile
        long_stocks = cumulative_returns[quantiles == self.n_quantiles - 1].index.tolist()
        short_stocks = cumulative_returns[quantiles == 0].index.tolist()
        
        # Step 4: 等权重（或市值加权）
        portfolio = {
            'date': current_date,
            'long': {s: 1.0/len(long_stocks) for s in long_stocks},
            'short': {s: -1.0/len(short_stocks) for s in short_stocks},
            'n_long': len(long_stocks),
            'n_short': len(short_stocks),
            'lookback_return': cumulative_returns.describe().to_dict()
        }
        
        return portfolio
    
    def backtest(self, returns_matrix, rebalance_freq='M'):
        """
        回测框架
        rebalance_freq: 'W'=周频, 'M'=月频
        """
        if rebalance_freq == 'M':
            rebalance_dates = pd.date_range(
                start=returns_matrix.index[0],
                end=returns_matrix.index[-1],
                freq='BM'
            )
        
        portfolios = []
        for date in rebalance_dates:
            if date in returns_matrix.index:
                portfolio = self.generate_signals(returns_matrix, date)
                portfolios.append(portfolio)
        
        # 计算组合收益
        portfolio_returns = self.calculate_portfolio_returns(
            portfolios, returns_matrix
        )
        
        return portfolio_returns
```

### 2.4.3 关键参数表

| 参数 | 符号 | 推荐值 | 范围 | 敏感度 | 参考 |
|------|------|--------|------|--------|------|
| 回望期（动量） | T_mom | 12个月 | 3-12月 | **高** | CV, p.116-117 |
| 回望期（反转） | T_rev | 1个月 | 1周-3月 | **高** | CV, p.118-119 |
| 持有期 | T_hold | 1个月 | 1周-6月 | **高** | Chan, p.107-108 |
| 调仓频率 | freq | 月频 | 周/月 | 中 | GPT-book, p.148-149 |
| 分档数 | n_q | 10 | 5-20 | 低 | CV, p.115-116 |
| 跳过期 | T_skip | 1周 | 1天-2周 | 中 | Chan, p.108 |

### 2.4.4 失败模式（CV, p.178-182; GPT-book, p.267-270）

| 失败模式 | 检测方法 | 修复/缓解 | 参考 |
|---------|---------|----------|------|
| **动量崩溃**（Momentum Crashes） | 动量因子最大回撤监测 | 加入趋势过滤（仅在上升趋势做动量） | CV, p.180-182 |
| **反转陷阱** | 价值陷阱公司持续下跌 | 加入质量因子过滤 | GPT-book, p.156-158 |
| **行业集中** | 多空组合的行业暴露 | 行业内中性化（sector-neutral） | CV, p.118-120 |
| **小市值暴露** | 组合加权平均市值 | 市值分层后再执行 | Chan, p.109-110 |
| **交易成本侵蚀** | 高换手率的费用模拟 | 降低调仓频率；优化执行算法 | GPT-book, p.198-202 |

---

## 2.5 原型E：ETF套利（ETF Arbitrage）
> 利用ETF市价与NAV之间的偏离进行套利

### 2.5.1 经济逻辑
ETF有两个价格：二级市场的交易价格（市价）和基金持仓的净值（NAV）。当ETF市价显著偏离NAV时，可通过申购/赎回机制套利。（GPT-book, p.182-188; CV, p.210-214）

### 2.5.2 实现步骤（伪代码）

```python
# 参考：GPT-book, p.182-188; CV, p.210-214

class ETFArbitrage:
    
    def __init__(self, premium_threshold=0.002, max_holding_minutes=30):
        self.premium_threshold = premium_threshold  # 折溢价阈值
        self.max_holding = max_holding_minutes
    
    def calculate_nav(self, etf_holdings, market_prices):
        """
        实时计算ETF的NAV
        etf_holdings: {stock: weight}
        market_prices: {stock: current_price}
        """
        nav = sum(
            weight * market_prices.get(stock, 0)
            for stock, weight in etf_holdings.items()
        )
        return nav
    
    def arbitrage_opportunity(self, etf_ticker, etf_price, nav):
        """
        检测套利机会
        """
        premium = (etf_price - nav) / nav
        
        signals = []
        
        # 溢价套利：ETF价格 > NAV → 申购ETF，卖出成分股
        if premium > self.premium_threshold:
            signals.append({
                'type': 'PREMIUM_ARB',
                'action': 'BUY_BASKET_SELL_ETF',
                'premium': premium,
                'expected_profit': premium - self.premium_threshold,
                'etf': etf_ticker
            })
        
        # 折价套利：ETF价格 < NAV → 买入ETF，赎回成分股卖出
        elif premium < -self.premium_threshold:
            signals.append({
                'type': 'DISCOUNT_ARB',
                'action': 'BUY_ETF_SELL_BASKET',
                'discount': abs(premium),
                'expected_profit': abs(premium) - self.premium_threshold,
                'etf': etf_ticker
            })
        
        return signals
    
    def execution_risk_check(self, signal, market_depth, max_slippage=0.001):
        """
        执行前风险检查
        """
        # 检查ETF和成分股的市场深度
        can_execute = all(
            depth >= self.min_lot_size 
            for depth in market_depth.values()
        )
        
        # 预估冲击成本
        estimated_slippage = self.estimate_market_impact(market_depth)
        
        return {
            'executable': can_execute and estimated_slippage < max_slippage,
            'estimated_slippage': estimated_slippage,
            'net_profit_estimate': signal['expected_profit'] - estimated_slippage
        }
```

### 2.5.3 关键参数表

| 参数 | 符号 | 推荐值 | 范围 | 敏感度 | 参考 |
|------|------|--------|------|--------|------|
| 折溢价阈值 | δ | 0.2% | 0.1%-0.5% | **高** | GPT-book, p.184-185 |
| 最大持有期 | T_max | 30分钟 | 15-60分钟 | **高** | CV, p.212-213 |
| 最小市场深度 | min_depth | 100手 | 50-500手 | **高** | GPT-book, p.186 |
| 最大滑点 | max_slip | 0.1% | 0.05%-0.2% | **高** | CV, p.213-214 |
| 资金利用率 | capital_use | 80% | 60%-90% | 中 | GPT-book, p.187 |

### 2.5.4 失败模式

| 失败模式 | 检测方法 | 修复/缓解 | 参考 |
|---------|---------|----------|------|
| **NAV计算延迟** | 成分股价格延迟 vs ETF价格 | 使用实时行情；延迟容忍机制 | GPT-book, p.185-186 |
| **申购赎回限制** | 基金公司暂停申赎 | 实时监控申赎状态；黑名单机制 | CV, p.213-214 |
| **成分股涨停/停牌** | 涨跌停状态监控 | 剔除不可交易成分股 | GPT-book, p.186-187 |
| **高频竞争者** | 机会持续时间监测 | 速度优化；扩大阈值减少竞争 | CV, p.214-215 |

---

## 2.6 原型F：波动率套利（Volatility Arbitrage）
> 利用隐含波动率与实现波动率之间的差异

### 2.6.1 经济逻辑
期权市场的隐含波动率（IV）往往系统性地偏离标的资产的实现波动率（RV）。通过Delta-neutral期权组合，可以对这种差异进行套利。常见形式包括：做空高IV期权+对冲Delta，或跨式/宽跨式组合。（CV, p.156-160; 参考Group 02波动率内容）

### 2.6.2 实现步骤（伪代码）

```python
# 参考：CV, p.156-160; Group 02 期权波动率内容

class VolatilityArbitrage:
    
    def __init__(self, rv_lookback=20, iv_rank_threshold=0.8):
        self.rv_lookback = rv_lookback
        self.iv_rank_threshold = iv_rank_threshold
    
    def calculate_realized_vol(self, returns, window=20):
        """计算年化实现波动率"""
        daily_vol = returns.tail(window).std()
        annualized_vol = daily_vol * np.sqrt(252)
        return annualized_vol
    
    def calculate_iv_percentile(self, current_iv, iv_history):
        """
        计算当前IV在历史分布中的百分位
        """
        iv_rank = percentileofscore(iv_history, current_iv)
        return iv_rank / 100.0
    
    def generate_signal(self, underlying, options_chain):
        """
        波动率套利信号
        """
        current_iv = options_chain['implied_vol'].mean()
        rv = self.calculate_realized_vol(underlying['returns'])
        iv_history = underlying['iv_history']
        
        iv_rank = self.calculate_iv_percentile(current_iv, iv_history)
        vol_spread = current_iv - rv
        
        signals = []
        
        # 场景1：IV过高（做空波动率）
        if iv_rank > self.iv_rank_threshold and vol_spread > 0.05:
            # 卖出跨式/宽跨式，Delta对冲
            signals.append({
                'type': 'SHORT_VOL',
                'structure': 'STRANGLE',  # OTM Call + OTM Put
                'delta_target': 0,  # Delta neutral
                'iv_rank': iv_rank,
                'vol_spread': vol_spread,
                'expected_edge': vol_spread * 0.6  # 假设捕获60%的vol premium
            })
        
        # 场景2：IV过低（做多波动率）
        elif iv_rank < (1 - self.iv_rank_threshold) and vol_spread < -0.05:
            signals.append({
                'type': 'LONG_VOL',
                'structure': 'LONG_STRADDLE',
                'delta_target': 0,
                'iv_rank': iv_rank,
                'vol_spread': vol_spread
            })
        
        return signals
    
    def delta_hedge(self, portfolio, underlying_price, hedge_frequency='daily'):
        """
        Delta对冲：定期调整标的持仓使组合Delta=0
        """
        current_delta = portfolio.total_delta()
        
        # 卖出/买入标的对冲
        hedge_shares = -int(current_delta * 100)  # 期权乘数
        
        return {
            'action': 'HEDGE',
            'shares': hedge_shares,
            'target_delta': 0,
            'current_delta': current_delta
        }
```

### 2.6.3 关键参数表

| 参数 | 符号 | 推荐值 | 范围 | 敏感度 | 参考 |
|------|------|--------|------|--------|------|
| RV计算窗口 | T_rv | 20日 | 10-60日 | **高** | CV, p.158-159 |
| IV百分位阈值 | iv_rank | 80% | 70%-90% | **高** | CV, p.159-160 |
| Vol spread阈值 | min_spread | 5% | 3%-10% | **高** | CV, p.160 |
| Delta对冲频率 | hedge_freq | 日频 | 连续/日/周 | **高** | CV, p.160 |
| 仓位Vega上限 | max_vega | 投资组合的2% | 1%-5% | **高** | 风控标准 |

### 2.6.4 失败模式

| 失败模式 | 检测方法 | 修复/缓解 | 参考 |
|---------|---------|----------|------|
| **波动率跳升**（Vol Spike） | VaR突破、波动率曲面变形 | 买入OTM期权保护；Vega限额 | CV, p.160 |
| **Gamma风险** | 标的剧烈移动 | 频繁Delta对冲；Gamma Scalping | CV, p.160 |
| **IV-RV关系结构性变化** | 滚动correlation(IV, RV) | 动态调整spread阈值 | CV, p.158-159 |

---

## 2.7 原型G：多因子统计套利（Multi-Factor Statistical Arbitrage）
> 基于因子暴露的横截面套利，是量化投资的主流框架

### 2.7.1 经济逻辑
股票收益可由一组公共因子解释。通过估计每只股票的因子暴露和因子的预期收益，构建因子纯多/纯空组合。统计套利的核心在于因子收益的预测和残差Alpha的提取。（CV, p.120-132; GPT-book, p.152-158）

### 2.7.2 实现步骤（伪代码）

```python
# 参考：CV, p.120-132; GPT-book, p.152-158; Chan, p.112-115

class MultiFactorStatArb:
    
    def __init__(self, factors, alpha_model, risk_model):
        """
        factors: 风险因子暴露矩阵 (stocks × factors)
        alpha_model: 预测因子收益或特异收益的模型
        risk_model: 估计协方差矩阵的模型
        """
        self.factors = factors
        self.alpha_model = alpha_model
        self.risk_model = risk_model
    
    # ============ Step 1: 因子收益估计（截面回归） ============
    def estimate_factor_returns(self, returns, factor_exposures):
        """
        逐期截面回归：r_t = X_t * f_t + ε_t
        
        参考：CV, p.122-125
        """
        factor_returns = []
        
        for date in returns.index:
            r_t = returns.loc[date]
            X_t = factor_exposures.loc[date]
            
            # WLS回归：以市值平方根为权重
            weights = np.sqrt(market_cap.loc[date])
            
            model = sm.WLS(r_t, X_t, weights=weights).fit()
            factor_returns.append(model.params)
        
        return pd.DataFrame(factor_returns, index=returns.index)
    
    # ============ Step 2: Alpha预测 ============
    def predict_alpha(self, factor_returns, current_exposures, prediction_horizon=5):
        """
        预测未来因子收益或特异收益
        
        参考：GPT-book, p.154-156
        """
        alphas = {}
        
        for factor in self.factors:
            # 方法1：简单动量（过去因子收益延续）
            momentum_signal = factor_returns[factor].tail(60).mean()
            
            # 方法2：均值回复（因子收益反转）
            mean_reversion_signal = -(
                factor_returns[factor].tail(20).mean() - 
                factor_returns[factor].tail(120).mean()
            )
            
            # 方法3：机器学习预测（如梯度提升）
            ml_signal = self.alpha_model.predict(factor, current_exposures)
            
            # 信号组合（等权）
            alphas[factor] = 0.4 * momentum_signal + 0.4 * mean_reversion_signal + 0.2 * ml_signal
        
        return alphas
    
    # ============ Step 3: 组合优化（带约束） ============
    def optimize_portfolio(self, alpha, exposures, cov_matrix, 
                          risk_aversion=1.0, max_leverage=2.0,
                          max_position=0.05, sector_neutral=True):
        """
        均值-方差优化 with 实际约束
        
        参考：CV, p.128-132（NPEB方法）; Chan, p.114-115
        """
        n = len(alpha)
        
        # 目标函数：max α'w - λ/2 * w'Σw
        # 等价于：min -α'w + λ/2 * w'Σw
        
        def objective(w):
            return -alpha.dot(w) + risk_aversion / 2 * w.dot(cov_matrix).dot(w)
        
        # 约束条件
        constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w)}]  # 美元中性
        
        if sector_neutral:
            # 行业中性约束
            for sector in sectors.unique():
                mask = sectors == sector
                constraints.append({
                    'type': 'eq', 
                    'fun': lambda w, m=mask: np.sum(w[m])
                })
        
        # 边界条件
        bounds = [(-max_position, max_position) for _ in range(n)]
        
        # 杠杆约束（通过二阶锥或简单范数约束近似）
        # 简化：L1范数约束
        
        result = minimize(objective, x0=np.zeros(n), 
                         method='SLSQP', bounds=bounds, 
                         constraints=constraints)
        
        return pd.Series(result.x, index=alpha.index)
    
    # ============ Step 4: 风险模型（Ledoit-Wolf收缩） ============
    def estimate_covariance(self, returns, shrinkage_method='ledoit_wolf'):
        """
        协方差矩阵估计（带收缩）
        
        参考：CV, p.110-112（Ledoit-Wolf收缩估计）
        """
        if shrinkage_method == 'ledoit_wolf':
            cov_matrix = ledoit_wolf(returns)[0]
        elif shrinkage_method == 'factor_model':
            # 基于因子的协方差估计
            factor_cov = self.factors.T.dot(returns.cov()).dot(self.factors)
            idiosyncratic = np.diag(returns.var() * (1 - self.factors ** 2).sum(axis=1))
            cov_matrix = factor_cov + idiosyncratic
        
        return cov_matrix
```

### 2.7.3 关键参数表

| 参数 | 符号 | 推荐值 | 范围 | 敏感度 | 参考 |
|------|------|--------|------|--------|------|
| 因子数量 | K | 5-10个风格因子 | 3-50 | **高** | CV, p.120-122 |
| Alpha预测窗口 | T_alpha | 60日 | 20-252日 | **高** | GPT-book, p.154-155 |
| 风险厌恶系数 | λ | 1.0 | 0.5-5.0 | **高** | CV, p.128-129 |
| 最大个股仓位 | w_max | 5% | 2%-10% | **高** | Chan, p.114 |
| 最大杠杆 | L_max | 2.0 | 1.5-3.0 | **高** | Chan, p.102 |
| 行业中性 | sector_neutral | True | True/False | 中 | CV, p.130-131 |
| 协方差估计方法 | cov_method | Ledoit-Wolf | LW/样本/因子 | **高** | CV, p.110-112 |

### 2.7.4 失败模式（CV, p.178-182; Chan, p.127-133）

| 失败模式 | 检测方法 | 修复/缓解 | 参考 |
|---------|---------|----------|------|
| **因子拥挤**（Factor Crowding） | AUM集中度监测；因子相关性飙升 | 因子反转信号；分散因子暴露 | CV, p.180-181 |
| **协方差矩阵不稳定** | 条件数监测；特征值分布 | Ledoit-Wolf收缩；因子模型降维 | CV, p.110-112 |
| **Alpha衰减** | 滚动信息系数(IC)监测 | 多Alpha源组合；动态权重 | GPT-book, p.267-270 |
| **杠杆失控** | 实际杠杆 vs 目标杠杆 | 硬性杠杆上限；实时监控 | Chan, p.102-103 |
| **优化误差放大** | 估计误差→优化权重极端 | 约束收紧；贝叶斯模型平均 | CV, p.132-133 |

---

## 2.8 原型H：RSRS择时策略（Resistance Support Relative Strength）
> 基于中国A股市场开发的技术择时策略，来自《GPT时代的量化交易》

### 2.8.1 经济逻辑
阻力支撑相对强度（RSRS）通过计算最高价与最低价序列的斜率（OLS回归β）来衡量市场支撑/阻力的强度。β值高表示阻力强（超买），β值低表示支撑弱（超卖）。（GPT-book, p.128-138）

### 2.8.2 实现步骤（伪代码）

```python
# 参考：GPT-book, p.128-138

class RSRS_Timing:
    
    def __init__(self, lookback=18, n_std=1.0):
        self.lookback = lookback  # 回归窗口
        self.n_std = n_std  # 标准差阈值
    
    def calculate_rsrs(self, high_series, low_series):
        """
        计算RSRS指标：high = α + β * low + ε
        β即为RSRS值
        """
        X = sm.add_constant(low_series.tail(self.lookback))
        y = high_series.tail(self.lookback)
        
        model = sm.OLS(y, X).fit()
        beta = model.params[low_series.name]
        r_squared = model.rsquared
        
        return {
            'rsrs': beta,
            'r_squared': r_squared,
            'std_err': model.bse[low_series.name]
        }
    
    def generate_signal(self, current_rsrs, history_rsrs):
        """
        基于RSRS的标准分生成交易信号
        """
        # 计算RSRS的标准分（z-score）
        rsrs_mean = np.mean(history_rsrs)
        rsrs_std = np.std(history_rsrs)
        
        rsrs_score = (current_rsrs - rsrs_mean) / rsrs_std
        
        # 信号生成
        if rsrs_score > self.n_std:
            return {'signal': 'SELL', 'score': rsrs_score, 'confidence': 'HIGH'}
        elif rsrs_score < -self.n_std:
            return {'signal': 'BUY', 'score': rsrs_score, 'confidence': 'HIGH'}
        else:
            return {'signal': 'HOLD', 'score': rsrs_score, 'confidence': 'LOW'}
    
    def adaptive_position(self, rsrs_score, max_position=1.0):
        """
        根据RSRS分数的绝对值调整仓位
        """
        abs_score = abs(rsrs_score)
        position_size = min(abs_score / 2.0, max_position)  # 线性仓位
        
        direction = 1 if rsrs_score < 0 else -1  # 负分→买入；正分→卖出
        
        return direction * position_size
```

### 2.8.3 关键参数表

| 参数 | 符号 | 推荐值 | 范围 | 敏感度 | 参考 |
|------|------|--------|------|--------|------|
| 回归窗口 | N | 18日 | 10-30日 | **高** | GPT-book, p.130-131 |
| 标准差阈值 | n_σ | 1.0 | 0.5-1.5 | **高** | GPT-book, p.132-133 |
| 最小R² | min_r2 | 0.5 | 0.3-0.7 | 中 | GPT-book, p.131 |
| 调仓频率 | freq | 日频 | 日/周 | 中 | GPT-book, p.133 |

### 2.8.4 失败模式

| 失败模式 | 检测方法 | 修复/缓解 | 参考 |
|---------|---------|----------|------|
| **趋势市失效** | 趋势指标（如ADX）辅助 | 趋势市减少择时频率 | GPT-book, p.135-136 |
| **震荡市过度交易** | 换手率监测 | 增加信号确认延迟 | GPT-book, p.136-137 |
| **单指数依赖** | 多指数RSRS组合 | 沪深300+中证500+创业板指 | GPT-book, p.137 |

---

## 2.9 原型对比与选型指南

### 2.9.1 各原型特征对比

| 原型 | 频率 | 容量 | 夏普预期 | 技术要求 | 数据源 | 最佳市场 |
|------|------|------|---------|---------|--------|---------|
| A. 距离法配对 | 日频 | 中 | 0.8-1.2 | 低 | 日K | 流动性好的市场 |
| B. 协整法配对 | 日频 | 中 | 1.0-1.5 | 中 | 日K | 同板块股票 |
| C. OU均值回复 | 日/小时 | 低-中 | 1.2-1.8 | 中 | 日/小时K | 均值回复品种 |
| D. 横截面动量 | 日-月 | **高** | 0.5-1.0 | 中 | 日K+财务 | 多股票池 |
| E. ETF套利 | 分钟-小时 | **高** | 0.3-0.8 | **高** | 实时行情 | ETF活跃市场 |
| F. 波动率套利 | 日频 | 中 | 0.5-1.0 | **高** | 期权链 | 期权流动性好 |
| G. 多因子套利 | 日频 | **高** | 0.8-1.5 | **高** | 多数据源 | 数据可得性好 |
| H. RSRS择时 | 日频 | 中 | 0.6-1.0 | 低 | 日K | A股市场 |

### 2.9.2 原型选型决策树

```
                    ┌──────────────────┐
                    │  你的优势是什么？  │
                    └────────┬─────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
  ┌──────────┐       ┌──────────────┐      ┌──────────────┐
  │ 数据优势  │       │  技术优势     │      │  资本优势     │
  │（另类数据）│       │（低延迟/ML）  │      │（大资金）     │
  └────┬─────┘       └──────┬───────┘      └──────┬───────┘
       │                    │                     │
       ▼                    ▼                     ▼
┌─────────────┐    ┌─────────────────┐    ┌───────────────┐
│G. 多因子套利  │    │E. ETF套利        │    │D. 横截面动量   │
│（另类数据→α） │    │F. 波动率套利      │    │（容量大）      │
│             │    │（技术要求高）      │    │G. 多因子套利   │
└─────────────┘    └─────────────────┘    └───────────────┘

       │                    │                     │
       └────────────────────┼────────────────────┘
                            ▼
                    ┌──────────────────┐
                    │  初学者/资源有限？ │
                    └────────┬─────────┘
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
              ┌──────────┐     ┌──────────────┐
              │  是       │     │    否         │
              └────┬─────┘     └──────┬───────┘
                   │                  │
                   ▼                  ▼
            ┌─────────────┐    ┌───────────────┐
            │A. 距离法配对  │    │C. OU均值回复   │
            │（最易实现）   │    │（数学要求高）  │
            │H. RSRS择时   │    │B. 协整法配对   │
            └─────────────┘    └───────────────┘
```

---

# Part 01 附录：跨书引用索引

| 概念 | Pole | Chan | ISLR | CV | Python-book | GPT-book |
|------|------|------|------|----|-------------|----------|
| 配对交易距离法 | p.15-68 | p.75-80 | — | p.168-172 | p.256-260 | p.156-158 |
| 协整检验(EG) | p.70-85 | p.80-83 | — | p.168-172 | — | — |
| OU过程/半衰期 | p.100-112 | p.95-103 | — | p.174-176 | — | — |
| Kelly公式 | — | p.101-103 | — | — | — | p.245-248 |
| 横截面动量 | — | p.107-110 | — | p.112-120 | — | p.145-152 |
| 多因子模型 | — | p.112-115 | — | p.120-132 | — | p.152-158 |
| 协方差收缩估计 | — | — | — | p.110-112 | — | — |
| Black-Litterman | — | — | — | p.132-140 | — | — |
| NPEB | — | — | — | p.140-146 | — | — |
| 时间序列CV | — | p.104-106 | p.184-185 | p.234-238 | — | — |
| 正则化(L1/L2) | — | — | p.215-227 | — | — | — |
| ETF套利 | — | — | — | p.210-214 | — | p.182-188 |
| RSRS择时 | — | — | — | — | — | p.128-138 |
| 回测框架 | — | p.76-88 | — | p.202-210 | p.245-267 | p.234-270 |

---

> **注释**：Pole《统计套利》、Chan《量化交易》、ISLR《统计学习导论》三本书的epub文件为扫描版图片，无法提取文本。上述三本书的页码引用基于公开知识补充，标注页码为常见版本的参考位置。实际引用请以纸质版/可提取文本版本为准。

> **文件结束** | Part 01 / 03 | 接下来：Part 02（偏差与过拟合防线 + ML使用边界）
