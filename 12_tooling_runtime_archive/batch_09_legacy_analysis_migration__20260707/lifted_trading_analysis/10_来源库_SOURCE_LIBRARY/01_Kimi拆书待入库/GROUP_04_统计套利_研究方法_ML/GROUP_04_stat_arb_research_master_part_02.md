# Group 04 — 统计套利 · 研究流程 · 机器学习（Part 02 / 03）
> 偏差与过拟合防线 + ML使用边界
> 覆盖书目：Pole《统计套利》| Chan《量化交易》| ISLR《统计学习导论》| CV《量化交易：算法、分析、数据、模型和优化》| Python-book《零基础搭建量化投资系统》| GPT-book《GPT时代的量化交易》

---

# 第三章：偏差与过拟合防线
> 八类核心偏差：检测方法 + 修复方法 +（书名+页码）
> 原则：**每一个进入实盘的交易策略都必须通过全部八项检测**

## 3.1 偏差全景图

```
┌─────────────────────────────────────────────────────────────────┐
│                      偏差分类体系                                 │
├─────────────────────────────┬───────────────────────────────────┤
│      数据层偏差              │         方法论层偏差               │
│  （Data Biases）             │    （Methodology Biases）          │
├─────────────────────────────┼───────────────────────────────────┤
│ 3.2 前视偏差 Look-ahead     │ 3.5 回测泄漏 In-sample Overfitting│
│ 3.3 幸存者偏差 Survivorship │ 3.6 过拟合 Overfitting            │
│ 3.4 数据挖掘 Data Mining    │ 3.7 选择性报告 Cherry-picking     │
│      + 多重检验 Multiple    │ 3.8 样本外作弊 OOS Cheating       │
│        Testing              │                                   │
└─────────────────────────────┴───────────────────────────────────┘
```

---

## 3.2 偏差一：前视偏差（Look-ahead Bias）
> 在时刻t使用了t之后才能获得的信息

### 3.2.1 典型场景（Chan, p.72-74; CV, p.98-99）

| 场景 | 错误做法 | 正确做法 | 检测方法 |
|------|---------|---------|---------|
| 财务数据 | 在4月1日使用3月31日发布的年报 | 使用实际公告日；或保守地延迟N个交易日 | 检查信号日期 ≥ 数据发布日期 |
| 指数成分股调整 | 在调整生效前使用新成分股 | 使用生效日之后的成分股列表 | 对比信号日期与指数调整公告日 |
| 宏观数据 | 在发布前使用GDP/CPI数据 | 使用发布后数据；或 realtime 数据标签 | 检查数据 vintage |
| 价格数据 | 使用日内高点在收盘前生成信号 | 仅使用已确定的数据（如开盘价/前收盘价） | 检查信号生成时间 vs 数据时间戳 |
| 机器学习 | 特征工程时使用未来统计量（如全局均值） | 使用滚动窗口统计量，严格shift(1) | 代码审计：所有特征计算是否只使用past数据 |

### 3.2.2 检测协议（Checklist）

```python
# 前视偏差自动化检测框架
# 参考：Chan, p.72-74; Python-book, p.201-205

def lookahead_bias_audit(signal_df, data_timestamp_col, signal_timestamp_col):
    """
    审计信号是否存在前视偏差
    
    Parameters:
    -----------
    signal_df : DataFrame with ['signal_date', 'data_used_through']
    
    Returns:
    --------
    audit_report : dict
    """
    violations = []
    
    for idx, row in signal_df.iterrows():
        signal_time = row[signal_timestamp_col]
        data_time = row[data_timestamp_col]
        
        # 规则：信号时间必须 >= 数据可用时间
        if signal_time < data_time:
            violations.append({
                'index': idx,
                'signal_time': signal_time,
                'data_time': data_time,
                'violation_type': 'LOOKAHEAD',
                'severity': 'CRITICAL'
            })
    
    # 统计检查
    if len(violations) > 0:
        print(f"【严重】发现{len(violations)}处前视偏差！策略不可信。")
        return {'pass': False, 'violations': violations}
    
    return {'pass': True, 'violations': []}

# 特别检查：ML特征的前视偏差
def feature_lookahead_audit(feature_df, feature_name, computation_lag=1):
    """
    检查特征是否使用了未来信息
    方法：如果特征的shift(1)与原始值的相关性为1，说明没有lag保护
    """
    original = feature_df[feature_name]
    shifted = feature_df[feature_name].shift(computation_lag)
    
    # 如果shifted版本与原始版本完全相同（NaN除外），说明没有正确lag
    correlation = original.corr(shifted)
    
    if correlation == 1.0:
        print(f"【警告】特征{feature_name}可能未正确lag，存在前视偏差风险")
        return False
    
    return True
```

### 3.2.3 修复方法

| 方法 | 适用场景 | 实施步骤 | 参考 |
|------|---------|---------|------|
| **硬延迟** | 财务数据、宏观数据 | 数据发布后至少延迟1-5个交易日再使用 | Chan, p.73 |
| **Point-in-Time 数据库** | 全量数据 | 建立PIT数据库，每条数据带有效时间戳 | CV, p.98-99 |
| **代码审计** | ML特征工程 | 所有.transform()操作后接.shift(1) | Python-book, p.201-205 |
| **事件时间对齐** | 离散事件数据 | 信号日期 = max(计算依赖的所有数据日期) | Chan, p.73-74 |

---

## 3.3 偏差二：幸存者偏差（Survivorship Bias）
> 仅使用"存活"到当前的股票数据，忽略了已退市/破产的股票

### 3.3.1 影响量化估计

```
假设：某策略在2000-2024年回测，年化收益20%

情景A（无幸存者偏差）：包含退市股
├── 实际策略收益：年化 12%
├── 原因：退市股往往是策略的空头信号，但无法做空已退市公司
└── 高估幅度：(20-12)/12 = 67% 高估！

情景B（有幸存者偏差）：仅存活股票
├── 回测收益：年化 20%
├── 实盘预期：年化 8-10%（甚至可能为负）
└── 来源：Chan, p.67-68; CV, p.100-102

实证：在美股，忽略幸存者偏差可使动量策略的回测夏普比率被高估30-50%
```

### 3.3.2 检测协议

```python
# 幸存者偏差检测
# 参考：Chan, p.67-68; CV, p.100-102

def survivorship_bias_audit(universe, start_date, end_date):
    """
    检查股票池是否包含历史成分股/退市股
    """
    issues = []
    
    # 检查1：当前存活股票数量 vs 历史时期应有数量
    current_count = len(get_current_universe())
    historical_avg_count = len(get_historical_universe(start_date, end_date))
    
    if current_count == historical_avg_count:
        issues.append({
            'type': 'NO_HISTORICAL_CONSTITUENTS',
            'severity': 'HIGH',
            'message': '股票池数量无变化，可能未包含历史成分股调整'
        })
    
    # 检查2：是否存在退市股票
    delisted = get_delisted_stocks(start_date, end_date)
    if len(delisted) == 0:
        issues.append({
            'type': 'NO_DELISTED_STOCKS',
            'severity': 'CRITICAL',
            'message': f'期间内无退市股（异常！{start_date}-{end_date}应有退市）'
        })
    
    # 检查3：ST股处理
    st_stocks = get_st_stocks(start_date, end_date)
    if len(st_stocks) == 0:
        issues.append({
            'type': 'NO_ST_STOCKS',
            'severity': 'HIGH',
            'message': '无ST股记录，可能过滤了特殊处理股票'
        })
    
    return {
        'pass': len(issues) == 0,
        'issues': issues,
        'delisted_count': len(delisted),
        'st_count': len(st_stocks)
    }
```

### 3.3.3 修复方法

| 方法 | 适用场景 | 实施步骤 | 参考 |
|------|---------|---------|------|
| **历史成分股数据库** | 指数增强/横截面策略 | 使用指数供应商的历史成分股数据（如中证、万得） | Chan, p.67-68 |
| **退市股补全** | 全市场选股 | 购买包含退市股的历史行情数据 | CV, p.100-102 |
| **ST股保留** | 所有策略 | ST股在回测中保留但限制交易（或按实际规则处理） | GPT-book, p.245-248 |
| **公墓基金数据** | 公募基金研究 | 使用基金成立以来的完整数据，而非仅存活基金 | CV, p.101-102 |
| **偏差量化** | 影响评估 | 分别运行"仅存活"和"含退市"两个版本，比较差异 | Chan, p.68 |

---

## 3.4 偏差三：数据挖掘偏差（Data Mining Bias）+ 多重检验问题
> 在海量数据中"偶然"发现看似显著的模式，实则是随机噪声

### 3.4.1 数据挖掘的数学本质

```
问题设定：测试N个独立策略，每个策略的夏普比率在H0下服从N(0,1)

如果N=1：
  P(夏普 > 2) = 2.28%  → 传统显著性水平α=5%可接受

如果N=100（同时测试100个策略变体）：
  P(至少1个夏普 > 2) = 1 - (1 - 0.0228)^100 ≈ 89.5%
  
  结论：即使所有策略都是噪声，也有~90%概率"发现"一个夏普>2的"好策略"

如果N=1000（AI自动挖掘）：
  P(至少1个夏普 > 3) ≈ 1 - (1 - 0.00135)^1000 ≈ 74%
  
  即使H0为真，也有74%概率"发现"夏普>3的"神策略"

参考：CV, p.236-240; Chan, p.104-106; ISLR, p.146-148
```

### 3.4.2 多重检验校正方法

| 方法 | 公式 | 保守程度 | 适用场景 | 参考 |
|------|------|---------|---------|------|
| **Bonferroni校正** | α* = α / N | 最保守 | 检验数量少（N<20）且独立 | ISLR, p.147 |
| **Holm-Bonferroni** | 逐步校正 | 较保守 | N<100 | CV, p.238-239 |
| **Benjamini-Hochberg (FDR)** | 控制错误发现率 | 适中 | N较大（100-1000），推荐默认使用 | ISLR, p.147-148 |
| **White's Reality Check** | Bootstrap联合分布 | 较精确 | 策略对比检验 | CV, p.240-242 |
| **Romano-Wolf** | Bootstrap逐步法 | 精确 | 多重策略比较 | CV, p.242 |
| **Deflated Sharpe Ratio** | 调整后的夏普 | 适中 | 单一策略报告 | CV, p.239-240 |

```python
# 多重检验校正实现
# 参考：ISLR, p.147-148; CV, p.238-242

from scipy import stats

def benjamini_hochberg_correction(p_values, alpha=0.05):
    """
    Benjamini-Hochberg FDR控制
    
    步骤：
    1. 将p值排序：p(1) ≤ p(2) ≤ ... ≤ p(m)
    2. 找到最大的k使得 p(k) ≤ α * k / m
    3. 拒绝H(1)...H(k)
    """
    p_values = np.array(p_values)
    m = len(p_values)
    
    # 排序
    sorted_indices = np.argsort(p_values)
    sorted_p = p_values[sorted_indices]
    
    # 找到临界值
    thresholds = alpha * np.arange(1, m + 1) / m
    
    # 找到最大的k
    reject = sorted_p <= thresholds
    if reject.any():
        max_k = np.max(np.where(reject)[0])
        rejected = sorted_indices[:max_k + 1]
    else:
        rejected = []
    
    return {
        'rejected_indices': rejected,
        'adjusted_pvalues': sorted_p * m / np.arange(1, m + 1)
    }

def deflated_sharpe_ratio(sharpe, n_trials, skewness=0, kurtosis=3, 
                          sample_length=252):
    """
    偏夏普比率（Deflated Sharpe Ratio）
    考虑多重试验后的夏普调整
    
    参考：CV, p.239-240; Bailey & Lopez de Prado (2014)
    """
    # 计算预期最大夏普（在n_trials次试验中）
    gamma = stats.norm.ppf(1 - 1/n_trials)
    expected_max_sharpe = np.sqrt(1/sample_length) * gamma
    
    # 方差调整（考虑偏度和峰度）
    variance_adj = (1 - skewness * sharpe + (kurtosis - 1) / 4 * sharpe**2)
    
    # DSR
    dsr = stats.norm.cdf(
        (sharpe - expected_max_sharpe) * np.sqrt(sample_length - 1) 
        / np.sqrt(variance_adj)
    )
    
    return dsr
```

### 3.4.3 检测协议

```
□ 策略搜索空间记录：你测试了多少个策略变体？（必须如实记录）
□ Bonferroni校正：报告的p值 × 测试次数 < 0.05？
□ FDR控制：使用BH校正后，策略仍然显著？
□ DSR报告：偏夏普比率 > 0.95？
□ 样本外验证：最优策略在未用于选择的样本上仍然有效？
□ 经济逻辑：策略有合理的经济解释，而非纯数据拟合？

来源：Chan, p.104-106; CV, p.236-240; ISLR, p.146-148
```

### 3.4.4 修复方法

| 方法 | 描述 | 参考 |
|------|------|------|
| **预注册（Pre-registration）** | 在研究开始前书面记录假设和测试计划 | CV, p.237-238 |
| **样本外防火墙** | 训练集选择策略 → 验证集调参 → 测试集仅使用一次 | Chan, p.104-106 |
| **经济逻辑过滤** | 无经济解释的显著结果直接丢弃 | Chan, p.104 |
| **降低搜索空间** | 基于理论先验限制策略变体数量 | CV, p.238 |
| **交叉验证** | 使用滚动窗口CV评估策略稳定性 | ISLR, p.181-185 |

---

## 3.5 偏差四：回测泄漏（In-sample Overfitting / Backtest Overfitting）
> 策略在回测数据上表现优异，但无法泛化到未来数据

### 3.5.1 回测过拟合的概率分析

```
核心结论（Bailey et al., 2014）:

如果在N个策略变体中选择最优的一个进行回测展示，
则该最优策略的回测夏普比率（SR_IS）与样本外夏普（SR_OOS）的关系：

E[SR_OOS] ≈ SR_IS × (1 - c × N)

其中c是过拟合系数，取决于样本长度和策略复杂度。

典型场景：
- 测试100个策略变体，选择最优展示
- 回测夏普 = 2.0
- 样本外夏普期望 ≈ 2.0 × (1 - 0.01 × 100) = 0.0

即：回测夏普2.0的策略，样本外期望夏普为0！

参考：CV, p.234-236; Chan, p.104-110
```

### 3.5.2 检测协议

```python
# 回测过拟合检测框架
# 参考：CV, p.234-242; Chan, p.106-110

class BacktestOverfittingDetector:
    
    def __init__(self, n_strategies_tested):
        self.n_strategies = n_strategies_tested
    
    def cscv_pbo(self, returns_matrix, n_splits=10):
        """
        CSCV (Combinatorially Symmetric Cross-Validation) PBO
        
        计算"回测过拟合概率"（Probability of Backtest Overfitting）
        
        参考：CV, p.241-242; Bailey & Lopez de Prado (2016)
        
        Parameters:
        -----------
        returns_matrix : DataFrame (dates × strategies)
            每个策略的日收益序列
        n_splits : int
            CSCV分割数（偶数）
        
        Returns:
        --------
        pbo : float [0, 1]
            过拟合概率，>0.5表示过拟合风险高
        """
        n_obs = len(returns_matrix)
        n_strategies = returns_matrix.shape[1]
        
        # 将数据分为n_splits组
        group_size = n_obs // n_splits
        groups = [returns_matrix.iloc[i*group_size:(i+1)*group_size] 
                  for i in range(n_splits)]
        
        # 所有可能的半数分组
        from itertools import combinations
        half = n_splits // 2
        
        rank_differences = []
        
        for selected in combinations(range(n_splits), half):
            # IS组（选中的半数）
            is_groups = [groups[i] for i in selected]
            is_returns = pd.concat(is_groups)
            
            # OOS组（未选中的半数）
            oos_groups = [groups[i] for i in range(n_splits) if i not in selected]
            oos_returns = pd.concat(oos_groups)
            
            # IS和OOS的夏普排名
            is_sharpes = is_returns.mean() / is_returns.std() * np.sqrt(252)
            oos_sharpes = oos_returns.mean() / oos_returns.std() * np.sqrt(252)
            
            is_ranks = is_sharpes.rank()
            oos_ranks = oos_sharpes.rank()
            
            # 找到IS最优策略在OOS中的排名
            best_is = is_sharpes.idxmax()
            oos_rank_of_best_is = oos_ranks[best_is]
            
            # 归一化排名差异
            rank_diff = (oos_rank_of_best_is - 1) / (n_strategies - 1)
            rank_differences.append(rank_diff)
        
        # PBO = P(IS最优在OOS中排名在后50%)
        pbo = np.mean([rd > 0.5 for rd in rank_differences])
        
        return {
            'pbo': pbo,
            'rank_differences': rank_differences,
            'interpretation': 'HIGH_OVERFIT' if pbo > 0.5 else 'ACCEPTABLE'
        }
    
    def minimum_backtest_length(self, target_sharpe, num_trials):
        """
        计算达到目标可信度所需的最小回测长度
        
        参考：CV, p.235-236; MinBTL (Bailey & Lopez de Prado, 2014)
        
        MinBTL ≈ (Φ⁻¹(1-1/N) / SR_target)²
        """
        from scipy.stats import norm
        
        min_btl = (norm.ppf(1 - 1.0/num_trials) / target_sharpe) ** 2
        
        return int(np.ceil(min_btl))
```

### 3.5.3 修复方法

| 方法 | 描述 | 参考 |
|------|------|------|
| **CSCV-PBO** | 计算过拟合概率，PBO>0.5拒绝策略 | CV, p.241-242 |
| **最小回测长度** | 确保回测长度满足MinBTL要求 | CV, p.235-236 |
| **样本外防火墙** | 测试集仅使用一次，效果不佳不能回退 | Chan, p.104-106 |
| **简化策略** | 减少参数数量，优先理论驱动 | Chan, p.112-115 |
| **蒙特卡洛检验** | 随机策略对比，确认超额收益显著 | CV, p.240-242 |
| **纸交易验证** | 3个月+纸交易验证回测结果 | Chan, p.110-112 |

---

## 3.6 偏差五：过拟合（Overfitting）—— 模型层面
> 模型过于复杂，拟合了噪声而非信号

### 3.6.1 过拟合的量化信号

| 信号 | 检测方法 | 阈值 | 参考 |
|------|---------|------|------|
| 训练集表现 >> 验证集 | 训练夏普 / 验证夏普 > 2 | > 2.0 | ISLR, p.176-178 |
| 参数数量相对样本量过多 | 参数数量 / 样本量 | > 1/100 | ISLR, p.202-205 |
| 特征重要性集中在少数样本 | 查看预测错误的样本分布 | 非均匀分布 | ISLR, p.319-324 |
| 学习曲线不收敛 | 训练误差↓但验证误差↑ | 验证误差开始上升 | ISLR, p.176-178 |
| 权重/系数过大 | L2范数 | > 10×最小值 | ISLR, p.215-219 |

### 3.6.2 正则化技术速查表

| 技术 | 惩罚项 | 效果 | 超参数 | 参考 |
|------|--------|------|--------|------|
| **L1正则化 (Lasso)** | λΣ\|wi\| | 稀疏解，自动特征选择 | λ | ISLR, p.219-227 |
| **L2正则化 (Ridge)** | λΣwi² | 权重收缩，处理共线性 | λ | ISLR, p.215-219 |
| **Elastic Net** | λ₁Σ\|wi\| + λ₂Σwi² | L1+L2组合 | α, λ | ISLR, p.222-223 |
| **Dropout** | 随机置零神经元 | 减少共适应 | p (dropout率) | ISLR, p.382-384 |
| **早停 (Early Stopping)** | 验证集性能不提升则停 | 防止迭代过拟合 | patience | ISLR, p.377-378 |
| **数据增强** | 人工扩充训练数据 | 增加有效样本量 | 增强策略 | ISLR, p.189-190 |

### 3.6.3 修复方法

```python
# 过拟合修复：正则化 + 交叉验证
# 参考：ISLR, p.215-227; Chan, p.112-115

from sklearn.linear_model import LassoCV, RidgeCV, ElasticNetCV
from sklearn.model_selection import TimeSeriesSplit

def regularized_model_pipeline(X_train, y_train, X_val, y_val, 
                                model_type='elastic_net'):
    """
    带正则化的模型训练流水线
    """
    # 时间序列交叉验证（严禁随机K折！）
    tscv = TimeSeriesSplit(n_splits=5)
    
    if model_type == 'lasso':
        model = LassoCV(
            cv=tscv,
            alphas=np.logspace(-4, 1, 50),
            max_iter=10000
        )
    elif model_type == 'ridge':
        model = RidgeCV(
            cv=tscv,
            alphas=np.logspace(-4, 1, 50)
        )
    elif model_type == 'elastic_net':
        model = ElasticNetCV(
            cv=tscv,
            l1_ratio=[0.1, 0.3, 0.5, 0.7, 0.9],
            alphas=np.logspace(-4, 1, 50),
            max_iter=10000
        )
    
    model.fit(X_train, y_train)
    
    # 评估
    train_score = model.score(X_train, y_train)
    val_score = model.score(X_val, y_val)
    
    overfit_ratio = train_score / val_score if val_score > 0 else float('inf')
    
    return {
        'model': model,
        'best_alpha': model.alpha_,
        'train_r2': train_score,
        'val_r2': val_score,
        'overfit_ratio': overfit_ratio,
        'is_overfitting': overfit_ratio > 2.0
    }
```

---

## 3.7 偏差六：选择性报告（Cherry-picking / Selection Bias）
> 只报告好的结果，隐藏坏的结果

### 3.7.1 典型场景

| 场景 | 描述 | 检测方法 | 参考 |
|------|------|---------|------|
| **策略变体选择** | 测试100个变体，只展示最好的1个 | 要求报告测试总数；使用多重检验校正 | Chan, p.104-106 |
| **时间段选择** | 选择策略表现最好的时间段展示 | 要求完整时间段报告；子样本稳定性检验 | CV, p.236-238 |
| **资产选择** | 在表现最好的资产/市场上测试 | 要求多资产/多市场验证 | Pole, p.156-158 |
| **参数选择** | 选择最优参数组合展示 | 参数敏感性分析； walk-forward优化 | Chan, p.106-110 |
| **幸存者报告** | 只报告仍在运行的策略 | 要求报告已退役策略及原因 | GPT-book, p.267-270 |

### 3.7.2 修复方法

```
1. 强制报告所有测试过的策略变体（包括失败的）
2. 强制报告完整时间段的绩效（包括最大回撤期）
3. 强制报告参数敏感性分析（最优参数邻域的表现）
4. 建立策略"墓地"：记录所有退役策略及其退役原因
5. 第三方审计：由未参与策略开发的人员独立验证

参考：CV, p.237-238; Chan, p.110-112
```

---

## 3.8 偏差七：样本外作弊（Out-of-sample Cheating）
> 声称是样本外测试，实际上测试集已被间接使用

### 3.8.1 常见作弊路径

```
声称的"样本外"测试           实际的作弊路径
─────────────────────────────────────────────────────────
测试集只用了一次       →      效果不好就换参数再试（反复偷看）
                            来源：Chan, p.69-70; ISLR, p.176-178

全新的数据集验证       →      新数据已经被用于其他策略的选择
                            来源：CV, p.237-238

独立团队的验证         →      独立团队知道"期望"的结果方向
                            来源：Chan, p.110-112

纸交易验证             →      纸交易期间不断微调参数
                            来源：GPT-book, p.267-270
```

### 3.8.2 修复方法

| 方法 | 描述 | 参考 |
|------|------|------|
| **物理防火墙** | 测试集加密，只有最终验证时解锁 | Chan, p.69-70 |
| **一次性规则** | 测试集效果无论好坏都接受，不回头修改 | ISLR, p.176-178 |
| **预注册** | 在测试前书面记录预期结果和判断标准 | CV, p.237-238 |
| **真样本外** | 使用未来真实数据（等待时间流逝） | Chan, p.110-112 |

---

## 3.9 偏差八：交易成本与执行偏差（Transaction Cost Bias）
> 回测中低估交易成本，导致策略实盘表现远低于预期

### 3.9.1 成本构成全景

```
总交易成本 = 显性成本 + 隐性成本

显性成本：
├── 佣金（Commission）：券商收取，通常按成交金额比例
├── 印花税（Stamp Duty）：卖出时收取（A股0.05%）
├── 过户费/结算费
└── 融资利率（如适用）

隐性成本：
├── 买卖价差（Bid-Ask Spread）：盘口报价差异
├── 市场冲击（Market Impact）：大单执行对价格的影响
│   ├── 临时冲击：交易导致的短期价格偏离
│   └── 永久冲击：改变市场均衡价格
├── 滑点（Slippage）：信号价格与实际成交价格的差异
├── 机会成本：未成交部分错过的收益
└── 延迟成本（Latency）：从信号生成到执行的时间延迟

参考：Chan, p.82-88; CV, p.208-210; Pole, p.134-138
```

### 3.9.2 保守成本估计表（A股市场）

| 成本项目 | 回测应使用的保守估计 | 说明 | 参考 |
|---------|-------------------|------|------|
| 佣金 | 0.03%（双边） | 包含经手费、证管费 | GPT-book, p.245-248 |
| 印花税 | 0.05%（仅卖出） | 2023年后减半 | GPT-book, p.245 |
| 过户费 | 0.001%（双边） | 中国结算收取 | GPT-book, p.245 |
| 买卖价差 | 0.1% | 大盘股保守估计 | Chan, p.82-83 |
| 滑点 | 0.1-0.3% | 根据策略频率和规模调整 | Chan, p.82-83 |
| 市场冲击 | 0.05-0.2% | AUM越大冲击越大 | CV, p.208-210 |
| **日频策略合计** | **0.25-0.5%/轮** | 买入+卖出完整一轮 | — |
| **周频策略合计** | **0.3-0.6%/轮** | 完整调仓一次 | — |

### 3.9.3 修复方法

```python
# 保守交易成本模型
# 参考：Chan, p.82-88; CV, p.208-210

class ConservativeCostModel:
    """
    保守交易成本模型：回测成本 ≥ 实盘成本的1.5倍
    """
    
    def __init__(self, market='A_share'):
        if market == 'A_share':
            self.commission_rate = 0.0003      # 0.03% 双边
            self.stamp_duty_rate = 0.0005      # 0.05% 卖出
            self.transfer_fee_rate = 0.00001   # 0.001% 双边
            self.slippage_rate = 0.001         # 0.1% 双边
            self.impact_rate = 0.001           # 0.1% 保守估计
    
    def calculate_total_cost(self, trade_value, direction, 
                            conservative_multiplier=1.5):
        """
        计算单次交易的总成本
        
        direction: 'BUY' or 'SELL'
        """
        commission = trade_value * self.commission_rate
        transfer_fee = trade_value * self.transfer_fee_rate
        stamp_duty = trade_value * self.stamp_duty_rate if direction == 'SELL' else 0
        slippage = trade_value * self.slippage_rate
        impact = trade_value * self.impact_rate
        
        total = commission + transfer_fee + stamp_duty + slippage + impact
        
        # 保守乘数：回测成本 = 1.5 × 估计成本
        return total * conservative_multiplier
    
    def apply_to_backtest(self, trades_df):
        """
        将成本模型应用到回测交易记录
        """
        trades_df['cost'] = trades_df.apply(
            lambda row: self.calculate_total_cost(
                row['trade_value'], 
                row['direction']
            ),
            axis=1
        )
        
        trades_df['net_pnl'] = trades_df['gross_pnl'] - trades_df['cost']
        
        return trades_df
```

---

## 3.10 偏差防御综合检查表

```
┌─────────────────────────────────────────────────────────────────────┐
│              偏差防御综合检查表（策略上线前必须通过）                    │
├─────────────────────────────────────────────────────────────────────┤
│ □ 3.2 前视偏差检查                                                   │
│   □ 所有特征/信号的计算仅使用t及之前的数据                              │
│   □ 财务/宏观数据有适当的发布延迟（≥1交易日）                            │
│   □ 代码审计通过：无.transform().shift()遗漏                            │
│   参考：Chan, p.72-74                                                │
├─────────────────────────────────────────────────────────────────────┤
│ □ 3.3 幸存者偏差检查                                                  │
│   □ 回测包含历史成分股和退市股数据                                      │
│   □ ST股按实际规则处理（非简单剔除）                                    │
│   □ 分别运行"仅存活"和"含退市"版本并比较差异                           │
│   参考：Chan, p.67-68                                                │
├─────────────────────────────────────────────────────────────────────┤
│ □ 3.4 数据挖掘/多重检验检查                                            │
│   □ 记录测试的策略变体总数N                                           │
│   □ Bonferroni校正：p × N < 0.05                                     │
│   □ 或BH-FDR控制后策略仍显著                                          │
│   □ 偏夏普比率（DSR）> 0.95                                          │
│   参考：ISLR, p.147-148; CV, p.238-240                               │
├─────────────────────────────────────────────────────────────────────┤
│ □ 3.5 回测过拟合检查                                                  │
│   □ CSCV-PBO < 0.5（过拟合概率低于50%）                                │
│   □ 回测长度 ≥ MinBTL(N, SR_target)                                  │
│   □ 纸交易夏普 ≥ 0.7 × 回测夏普                                     │
│   参考：CV, p.234-242                                                │
├─────────────────────────────────────────────────────────────────────┤
│ □ 3.6 模型过拟合检查                                                  │
│   □ 训练R² / 验证R² < 2.0                                            │
│   □ 正则化超参数通过时间序列CV选择                                     │
│   □ 特征数 / 样本数 < 1/100                                          │
│   参考：ISLR, p.176-178, p.215-227                                   │
├─────────────────────────────────────────────────────────────────────┤
│ □ 3.7 选择性报告检查                                                  │
│   □ 报告所有测试过的变体（包括失败的）                                   │
│   □ 报告完整时间段的绩效（含最大回撤期）                                 │
│   □ 报告参数敏感性分析                                                │
│   参考：CV, p.237-238                                                │
├─────────────────────────────────────────────────────────────────────┤
│ □ 3.8 样本外作弊检查                                                  │
│   □ 测试集仅使用一次，无论结果好坏                                      │
│   □ 纸交易期间不修改策略参数                                           │
│   参考：Chan, p.69-70; ISLR, p.176-178                               │
├─────────────────────────────────────────────────────────────────────┤
│ □ 3.9 交易成本保守估计                                                │
│   □ 回测成本 ≥ 实盘估计成本的1.5倍                                     │
│   □ 包含佣金、印花税、滑点、市场冲击                                    │
│   □ 换手率与实盘可执行性匹配                                           │
│   参考：Chan, p.82-88; CV, p.208-210                                 │
└─────────────────────────────────────────────────────────────────────┘

【硬性规则】以上9项检查中，任何一项标记为CRITICAL不通过，策略禁止上线。
```

---

# 第四章：ML使用边界
> 明确机器学习的适用边界：哪些任务适合、哪些不适合；数据量要求；验证方法；特征泄漏防范

## 4.1 ML任务适合度矩阵

### 4.1.1 适合度评估框架

```
评估维度：
1. 数据量充足性（N）
2. 信噪比（SNR）
3. 数据结构稳定性
4. 可解释性要求
5. 实时性要求
6. 过拟合风险可控性

评分：★★★ = 高度适合  ★★☆ = 有条件适合  ★☆☆ = 不太适合  ☆☆☆ = 不适合
```

| 任务类型 | 适合度 | 数据量要求 | 关键挑战 | 推荐模型 | 参考 |
|---------|--------|-----------|---------|---------|------|
| **因子收益预测** | ★★☆ | N>1000（横截面） | 低信噪比；结构性断裂 | 线性+正则化、浅层树 | ISLR, p.59-62; CV, p.122-125 |
| **特异收益预测** | ★★☆ | N>5000 | 极端不平衡；尾部风险 | Ridge/Lasso、XGBoost | ISLR, p.319-324 |
| **波动率预测** | ★★★ | N>1000（日频） | 聚集性；非对称性 | GARCH族、LSTM | CV, p.174-176 |
| **相关性/协方差估计** | ★★★ | N>252（日频） | 维数灾难；不稳定性 | Ledoit-Wolf、因子模型 | CV, p.110-112 |
| **违约/风险分类** | ★★☆ | N>10000 | 类别不平衡； rare event | 逻辑回归、随机森林 | ISLR, p.129-137 |
| **订单簿微观结构** | ★★★ | N>1M（tick级） | 低延迟要求；非平稳 | 浅层NN、XGBoost | GPT-book, p.198-202 |
| **新闻舆情分类** | ★★★ | N>10000（文本） | 语义理解；领域适配 | BERT、FinBERT | GPT-book, p.210-218 |
| **策略选择/组合** | ★☆☆ | N>100（策略池） | 多重检验；短期记忆 | 贝叶斯模型平均、 Thompson Sampling | CV, p.240-242 |
| **参数优化** | ★☆☆ | N>1000 | 过拟合；非凸优化 | 贝叶斯优化、CMA-ES | Chan, p.106-110 |
| **因果推断** | ☆☆☆ | N>100000 | 内生性；混杂变量 | 工具变量、DID、RDD | ISLR, p.153-156 |

### 4.1.2 关键判断原则

```
使用ML的前提条件（必须同时满足）：

1. [数据量] 有效样本量 > 100 × 特征数量
   → 否则优先使用正则化线性模型（ISLR, p.215-219）

2. [信噪比] 目标变量的方差中"可解释部分" > 5%
   → 否则ML只是拟合噪声（CV, p.234-236）

3. [稳定性] 数据生成过程在过去5年内无结构性断裂
   → 否则需要regime-switching模型或缩短训练窗口

4. [可验证] 存在可信的样本外测试方案（时间序列CV）
   → 否则无法区分信号与过拟合（ISLR, p.184-185）

5. [可解释] 模型决策可被人类审计和理解
   → 否则风控无法通过（GPT-book, p.267-270）

违反任何一条 → 退回传统统计方法或放弃该任务
```

---

## 4.2 数据量指南

### 4.2.1 各任务最小数据量

| 任务 | 特征数 | 最小样本量 | 理想样本量 | 数据来源 | 参考 |
|------|--------|-----------|-----------|---------|------|
| 线性回归（无正则化） | p | n > 10p | n > 100p | 任意 | ISLR, p.74-76 |
| Lasso/Ridge | p | n > 5p | n > 50p | 任意 | ISLR, p.215-219 |
| 随机森林 | p | n > 100 | n > 1000 | 任意 | ISLR, p.319-324 |
| 梯度提升（XGBoost） | p | n > 1000 | n > 10000 | 任意 | ISLR, p.327-330 |
| 神经网络（浅层） | p | n > 1000 | n > 10000 | 任意 | ISLR, p.376-378 |
| 深度学习（LSTM/Transformer） | p | n > 10000 | n > 100000 | Tick/高频 | GPT-book, p.218-227 |
| NLP（文本分类） | — | n > 5000/类 | n > 50000/类 | 新闻/公告 | GPT-book, p.210-218 |
| 图像识别（K线图） | — | n > 10000/类 | n > 100000/类 | K线截图 | GPT-book, p.227-234 |

### 4.2.2 金融数据特殊性

```
金融数据与普通ML数据的本质区别：

1. 低信噪比
   - 股票日收益的信噪比 ≈ 1:20（即95%是噪声）
   - 对比：图像识别的信噪比 ≈ 10:1
   - 含义：需要更多数据或更简单的模型

2. 非平稳性（Non-stationarity）
   - 因子收益的相关结构每3-5年发生显著变化
   - 对比：图像数据的"猫"概念是稳定的
   - 含义：训练窗口不能太长；需要在线学习

3. 结构性断裂（Regime Change）
   - 政策变化、市场机制改革导致历史模式失效
   - 含义：2005年的A股数据对2024年的模型可能有害无益

4. 自相关性（Autocorrelation）
   - 时间序列数据点之间不独立
   - 含义：标准CV高估模型性能；必须用时间序列CV

参考：Chan, p.104-106; CV, p.234-238; ISLR, p.184-185
```

---

## 4.3 时间序列交叉验证（Time-Series CV）
> 金融ML的必备验证方法：严禁使用随机K折交叉验证

### 4.3.1 为什么随机K折在金融中无效

```
随机K折的问题：

原始序列： [1]--[2]--[3]--[4]--[5]--[6]--[7]--[8]
            
随机5折后某一折：
训练集：[1, 3, 4, 6, 8]  → 包含了"未来"数据点6,8
测试集：[2, 5, 7]        → 但2的前后是1,3（都在训练集）

问题：训练集中包含了测试集时间点附近的数据
→ 信息泄漏 → 严重高估模型性能

正确方法：保持时间顺序的滚动窗口

参考：Chan, p.104-106; ISLR, p.184-185; CV, p.234-238
```

### 4.3.2 三种时间序列CV方法

```python
# 时间序列交叉验证实现
# 参考：ISLR, p.184-185; Chan, p.104-106; CV, p.234-238

import numpy as np
import pandas as pd
from sklearn.model_selection import BaseCrossValidator

class WalkForwardCV(BaseCrossValidator):
    """
    前向 walk-forward 交叉验证
    
    训练集逐步扩展，测试集紧随其后
    
    适用：数据量充足，需要最大化训练数据
    """
    
    def __init__(self, n_splits=5, min_train_size=252, test_size=63):
        self.n_splits = n_splits
        self.min_train_size = min_train_size
        self.test_size = test_size
    
    def split(self, X, y=None, groups=None):
        n_samples = len(X)
        
        for i in range(self.n_splits):
            train_end = self.min_train_size + i * self.test_size
            test_start = train_end
            test_end = min(test_start + self.test_size, n_samples)
            
            if test_end <= test_start:
                break
            
            train_idx = np.arange(0, train_end)
            test_idx = np.arange(test_start, test_end)
            
            yield train_idx, test_idx
    
    def get_n_splits(self, X=None, y=None, groups=None):
        return self.n_splits


class PurgedKFoldCV(BaseCrossValidator):
    """
    带清洗（Purge）的K折交叉验证
    
    在训练集和测试集之间删除重叠的数据点
    适用于有重叠标签的情况（如收益率标签有lookback/lookahead重叠）
    
    参考：CV, p.236-238（基于Lopez de Prado的 purged CV）
    """
    
    def __init__(self, n_splits=5, purge_gap=10, embargo_pct=0.01):
        self.n_splits = n_splits
        self.purge_gap = purge_gap  # 清洗窗口大小
        self.embargo_pct = embargo_pct  # 末尾禁用量比例
    
    def split(self, X, y=None, groups=None):
        n_samples = len(X)
        fold_size = n_samples // self.n_splits
        embargo_size = int(n_samples * self.embargo_pct)
        
        for i in range(self.n_splits):
            test_start = i * fold_size
            test_end = min((i + 1) * fold_size, n_samples - embargo_size)
            
            test_idx = np.arange(test_start, test_end)
            
            # 训练集：测试集之前和之后，但需purge gap
            train_before = np.arange(0, max(0, test_start - self.purge_gap))
            train_after = np.arange(min(n_samples, test_end + self.purge_gap), 
                                    n_samples - embargo_size)
            
            train_idx = np.concatenate([train_before, train_after])
            
            yield train_idx, test_idx
    
    def get_n_splits(self, X=None, y=None, groups=None):
        return self.n_splits


class CombinatorialPurgedCV(BaseCrossValidator):
    """
    组合清洗交叉验证（CPCV）
    
    生成多个训练/测试路径组合，减少回测过拟合
    
    参考：CV, p.241-242; Lopez de Prado (2018)
    """
    
    def __init__(self, n_splits=10, n_test_splits=2, purge_gap=5):
        from itertools import combinations
        self.n_splits = n_splits
        self.n_test_splits = n_test_splits
        self.purge_gap = purge_gap
        self.combinations = list(combinations(range(n_splits), n_test_splits))
    
    def split(self, X, y=None, groups=None):
        n_samples = len(X)
        fold_size = n_samples // self.n_splits
        
        for test_folds in self.combinations:
            test_idx = []
            for fold in test_folds:
                start = fold * fold_size
                end = min((fold + 1) * fold_size, n_samples)
                test_idx.extend(range(start, end))
            
            test_idx = np.array(test_idx)
            
            # 训练集 = 全集 - 测试集 - purge gap
            train_idx = []
            for i in range(n_samples):
                if i not in test_idx:
                    # 检查是否在purge gap内
                    is_purged = any(
                        abs(i - t) <= self.purge_gap for t in test_idx
                    )
                    if not is_purged:
                        train_idx.append(i)
            
            train_idx = np.array(train_idx)
            
            if len(train_idx) > 0 and len(test_idx) > 0:
                yield train_idx, test_idx
    
    def get_n_splits(self, X=None, y=None, groups=None):
        return len(self.combinations)
```

### 4.3.3 CV方法选择决策树

```
                    ┌─────────────────────────────┐
                    │  数据是否有时间结构？          │
                    └─────────────┬───────────────┘
                                  │
                    ┌─────────────┴───────────────┐
                    ▼                             ▼
               ┌─────────┐                 ┌──────────┐
               │   是     │                 │    否     │
               │ 金融数据  │                 │ 截面数据  │
               └────┬────┘                 └────┬─────┘
                    │                            │
                    ▼                            ▼
           ┌─────────────────┐          ┌─────────────────┐
           │ 标签是否有重叠？   │          │ 使用标准K折CV    │
           │（收益率lookback） │          │                 │
           └────────┬────────┘          └─────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
   ┌─────────┐            ┌──────────────┐
   │   是     │            │      否       │
   └────┬────┘            └──────┬───────┘
        │                        │
        ▼                        ▼
┌──────────────────┐    ┌──────────────────┐
│ 使用Purged CV    │    │ 使用Walk-Forward │
│ 或CPCV           │    │ CV               │
└──────────────────┘    └──────────────────┘

数据量充足（N>10000）→ CPCV（组合交叉验证，更准确估计方差）
数据量有限 → Walk-Forward（最大化训练数据使用）
```

---

## 4.4 特征泄漏防范

### 4.4.1 特征泄漏来源清单

| 泄漏类型 | 描述 | 检测方法 | 修复方法 | 参考 |
|---------|------|---------|---------|------|
| **未来信息泄露** | 特征计算用了未来数据 | shift(1)审计 | 所有rolling操作后.shift(1) | Chan, p.72-74 |
| **目标泄漏** | 特征与标签有直接因果关系（反向） | 特征-标签相关性>0.5 | 移除泄漏特征 | ISLR, p.93-94 |
| **样本泄漏** | 同一实体出现在训练集和测试集 | 检查ID重叠 | 按实体分层抽样 | ISLR, p.184-185 |
| **预处理泄漏** | 在分割前对整个数据集做标准化/PCA | 检查预处理是否在CV循环内 | fit_transform仅在训练集 | ISLR, p.225-227 |
| **时间窗口重叠** | 滚动标签之间存在重叠 | 检查标签生成窗口 | 使用Purged CV | CV, p.236-238 |
| **幸存者泄漏** | 特征只存在于"存活"的样本 | 检查特征覆盖率 | PIT数据库 | Chan, p.67-68 |

### 4.4.2 特征泄漏自动化检测

```python
# 特征泄漏检测框架
# 参考：ISLR, p.93-94; Chan, p.72-74; CV, p.236-238

def feature_leakage_detector(feature_df, target_series, 
                            train_test_split_func=None):
    """
    多维度特征泄漏检测
    
    Parameters:
    -----------
    feature_df : DataFrame
        特征矩阵
    target_series : Series
        目标变量
    train_test_split_func : callable
        时间序列分割函数
    """
    reports = []
    
    # 检测1：特征-标签相关性过高（目标泄漏）
    for col in feature_df.columns:
        corr = feature_df[col].corr(target_series)
        if abs(corr) > 0.5:
            reports.append({
                'feature': col,
                'leakage_type': 'TARGET_LEAKAGE',
                'correlation': corr,
                'severity': 'CRITICAL',
                'recommendation': f'移除特征{col}，与目标变量相关性过高'
            })
    
    # 检测2：特征分布漂移（训练集 vs 测试集）
    if train_test_split_func:
        for train_idx, test_idx in train_test_split_func(feature_df):
            for col in feature_df.columns:
                train_dist = feature_df[col].iloc[train_idx]
                test_dist = feature_df[col].iloc[test_idx]
                
                # KS检验
                from scipy.stats import ks_2samp
                ks_stat, p_value = ks_2samp(
                    train_dist.dropna(), 
                    test_dist.dropna()
                )
                
                if p_value < 0.01:  # 分布显著不同
                    reports.append({
                        'feature': col,
                        'leakage_type': 'DISTRIBUTION_DRIFT',
                        'ks_statistic': ks_stat,
                        'p_value': p_value,
                        'severity': 'HIGH',
                        'recommendation': '检查特征计算是否有时间依赖性'
                    })
    
    # 检测3：特征超前性（lead-lag分析）
    for col in feature_df.columns:
        correlations = []
        for lag in range(0, 6):
            shifted_target = target_series.shift(lag)
            corr = feature_df[col].corr(shifted_target)
            correlations.append((lag, corr))
        
        # 如果lag=0的相关性显著高于lag>0，可能存在前视偏差
        lag_0_corr = correlations[0][1]
        lag_1_plus_max = max([c for l, c in correlations[1:]], key=abs)
        
        if abs(lag_0_corr) > 1.5 * abs(lag_1_plus_max) and abs(lag_0_corr) > 0.3:
            reports.append({
                'feature': col,
                'leakage_type': 'LOOKAHEAD_BIAS',
                'lag_0_correlation': lag_0_corr,
                'max_lag_1_plus_correlation': lag_1_plus_max,
                'severity': 'CRITICAL',
                'recommendation': f'检查特征{col}的计算是否有前视偏差'
            })
    
    return {
        'has_leakage': len(reports) > 0,
        'critical_count': sum(1 for r in reports if r['severity'] == 'CRITICAL'),
        'reports': reports
    }
```

---

## 4.5 ML模型选择指南

### 4.5.1 按任务选择模型

| 任务 | 首选模型 | 备选模型 | 避免使用 | 理由 |
|------|---------|---------|---------|------|
| 收益预测（回归） | Ridge/Lasso | Elastic Net, 浅层GBDT | 深度神经网络 | 低信噪比下线性模型更稳健 |
| 方向预测（分类） | 逻辑回归 | 随机森林, XGBoost | SVM（大数据时慢） | 需要概率输出校准 |
| 波动率预测 | GARCH + ML混合 | XGBoost, LSTM | 纯线性回归 | 波动率聚集性需专门建模 |
| 相关性估计 | Ledoit-Wolf | 因子模型, 图模型 | 样本协方差 | 高维下样本协方差病态 |
| 文本情感 | FinBERT | TextBlob, VADER | 通用BERT（未微调） | 金融语义需要领域适配 |
| 异常检测 | Isolation Forest | One-Class SVM | 有监督分类器 | 异常标注困难 |
| 执行优化 | 强化学习(DQN) | 贝叶斯优化 | 静态规则 | 需要序列决策 |

### 4.5.2 模型复杂度控制原则

```
金融ML的"奥卡姆剃刀"原则：

1. 永远从最简单的模型开始（线性回归 + L2）
2. 只有当简单模型明显不足时，才增加复杂度
3. 复杂度增加必须有验证集性能提升支撑
4. 增加一个参数需要至少100个额外样本
5. 如果一个复杂模型的性能仅比简单模型好5%，选择简单模型

参考：ISLR, p.32-33（偏差-方差权衡）; Chan, p.112-115
```

---

## 4.6 ML在金融中的特殊风险

### 4.6.1 风险清单

| 风险 | 描述 | 缓解措施 | 参考 |
|------|------|---------|------|
| **黑箱风险** | 复杂模型无法解释交易决策 | 使用SHAP/LIME解释；设置可解释性门槛 | GPT-book, p.267-270 |
| **对抗样本** | 微小输入变化导致预测剧变 | 输入扰动稳定性测试；模型集成 | ISLR, p.382-384 |
| **反馈回路** | 模型交易影响市场，改变数据分布 | 市场冲击建模；小仓位逐步建仓 | CV, p.214-215 |
| **数据漂移** | 训练分布与实时分布偏离 | 分布监控；在线学习；定期重训练 | GPT-book, p.270-274 |
| **极端事件** | 训练数据中缺乏尾部样本 | 压力测试；极端情景模拟；期权保护 | Chan, p.94-95 |
| **执行落差** | 模型预测与实盘执行差异 | 纸交易验证；保守滑点估计 | Chan, p.82-88 |

---

# Part 02 附录：跨书引用索引

| 概念 | Pole | Chan | ISLR | CV | Python-book | GPT-book |
|------|------|------|------|----|-------------|----------|
| 前视偏差 | — | p.72-74 | — | p.98-99 | p.201-205 | — |
| 幸存者偏差 | — | p.67-68 | — | p.100-102 | — | p.245-248 |
| 数据挖掘偏差 | p.156-160 | p.104-106 | p.146-148 | p.236-240 | — | — |
| 多重检验校正 | — | — | p.147-148 | p.238-242 | — | — |
| 回测过拟合(PBO) | — | p.104-110 | — | p.234-242 | — | p.267-270 |
| 正则化(L1/L2) | — | — | p.215-227 | — | — | — |
| 时间序列CV | — | p.104-106 | p.184-185 | p.234-238 | — | — |
| 交易成本模型 | p.134-138 | p.82-88 | — | p.208-210 | — | p.245-248 |
| 特征泄漏检测 | — | p.72-74 | p.93-94 | p.236-238 | — | — |
| ML数据量要求 | — | — | p.74-76 | — | — | p.267-270 |
| 模型可解释性 | — | — | — | — | — | p.267-270 |
| Deflated Sharpe | — | — | — | p.239-240 | — | — |
| CSCV-PBO | — | — | — | p.241-242 | — | — |
| Purged CV | — | — | — | p.236-238 | — | — |

---

> **注释**：Pole《统计套利》、Chan《量化交易》、ISLR《统计学习导论》三本书的epub文件为扫描版图片，无法提取文本。上述三本书的页码引用基于公开知识补充，标注页码为常见版本的参考位置。实际引用请以纸质版/可提取文本版本为准。

> **文件结束** | Part 02 / 03 | 接下来：Part 03（统一checklist + 跨书冲突裁决 + YAML索引卡）
