# BACKTEST_ROBUSTNESS_v1.0.md
# 回测过拟合检测与稳健性验证 — 设计文档

> **搜索批次**：第一批-J | 搜索日期：2026-07-07
> **关键词**：CSCV组合对称交叉验证、回测过拟合检测、Monte Carlo置换检验、策略衰减、最小跟踪误差
> **来源**：华泰证券、Bailey et al. 2017、BigQuant、雪球、SAGE Journal、百度学术
> **核心原则**："回测不是证明策略好，而是证明策略不坏"——用量化方法检测坏策略

---

## 一、过拟合的两层定义

### 1. 训练过拟合（Training Overfitting）
- **领域**：机器学习
- **表现**：训练集表现好，测试集表现差
- **原因**：超参数选择不当、过度训练
- **解决**：合理交叉验证（时序分割，非随机分割）

### 2. 回测过拟合（Backtest Overfitting）
- **领域**：量化策略
- **表现**：回测期表现好，实盘表现差
- **原因**：市场规律变化、对历史噪音过度学习、参数优化过度
- **解决**：CSCV框架、蒙特卡洛模拟、样本外测试

> **关键洞察**：回测过拟合比训练过拟合更隐蔽，因为回测已经"看起来"是样本外测试了——但参数优化过程本身就是对样本内的反复拟合。

---

## 二、核心方法：CSCV（组合对称交叉验证）

### 2.1 原理

来源：Bailey, Borwein, López de Prado, Zhu (2017) 《The Probability of Backtest Overfitting》

**核心思想**：将回测期分为S个等大小块，通过组合不同的训练/测试集块，评估"样本内最优策略在样本外表现如何"。

### 2.2 步骤

1. **分块**：将回测期T分为S等份（S为偶数，如8或10）
2. **组合**：选取S/2份作为训练集（IS），其余S/2份作为测试集（OOS）
3. **优化**：在训练集上找到最优策略（按夏普比率等）
4. **评估**：记录该策略在测试集上的排名
5. **重复**：遍历所有可能的组合（共C(S, S/2)种）
6. **计算PBO**：训练集最优策略在测试集排名落在后50%的概率

### 2.3 输出统计量

| 统计量 | 含义 | 判定标准 |
|--------|------|----------|
| **PBO** | 回测过拟合概率 | **PBO < 50% 可接受**（华泰实证） |
| **性能退化** | 样本内越好→样本外越差的程度 | 负相关越弱越好 |
| **损失概率** | 样本外产生亏损的概率 | 越低越好 |
| **随机占优** | 选择程序是否优于随机选择 | 应优于随机 |

### 2.4 实证结论（华泰证券）

- **多因子选股模型**：PBO大多在15%~50%，相对稳健
- **择时模型**：PBO在50%~90%，极易过拟合
- **关键结论**：择时策略的回测过拟合风险远高于选股策略

> **对我们系统的启示**：PeriodQueen的择时判断（ATTACK/REST等）需要更严格的过拟合检测，因为择时本身就容易过拟合。

---

## 三、辅助方法

### 3.1 Bootstrap重采样

- **方法**：对历史收益率序列进行有放回重采样，构建1000+条"平行世界"收益率路径
- **用途**：评估策略在不同市场路径下的稳健性
- **判断**：如果策略在90%的模拟路径中夏普>1，则认为稳健

### 3.2 Monte Carlo置换检验

- **方法**：随机打乱历史收益率的时间顺序，破坏时间序列相关性
- **用途**：检验策略收益是否显著高于随机序列
- **判断**：p值 < 0.05 说明策略不是运气

### 3.3 Walk-Forward分析（已在BACKTEST_FRAMEWORK中覆盖）

- **方法**：滚动窗口训练→测试，严格按时间顺序
- **用途**：模拟最真实的样本外测试
- **与CSCV的关系**：Walk-Forward是"单一路径"，CSCV是"多路径组合"，两者互补

### 3.4 策略衰减监控（实时监控）

- **方法**：上线后持续跟踪策略表现 vs 回测预期的偏离度
- **指标**：
  - rolling_sharpe(30) vs backtest_sharpe 的偏离
  - 信号命中率月度变化
  - 盈亏比持续下降
- **阈值**：如果rolling_sharpe < 0.5 * backtest_sharpe 持续3个月，触发审查

---

## 四、对现有回测框架的补充建议

### 4.1 强制检测清单（每个策略上线前必须通过）

```
□ CSCV-PBO 检测（PBO < 50%）
□ Bootstrap 显著性检验（p < 0.05）
□ Walk-Forward 验证（至少3个独立窗口）
□ 参数敏感性分析（最优参数附近±20%是否仍稳健）
□ 样本外衰减测试（最近1年表现是否显著退化）
```

### 4.2 对象卡级别的检测要求

| 对象卡 | 必须检测项 | 原因 |
|--------|-----------|------|
| CHZL_BSD | CSCV + 参数敏感性 | 参数多（分型/笔/中枢阈值） |
| BPB | CSCV + 样本外衰减 | 20种形态，容易过度拟合历史 |
| YTC | 样本外衰减 + 时段稳定性 | 微观结构参数敏感 |
| 任何ML模型 | 全部5项 | ML天然过拟合风险 |

### 4.3 回测诚实性升级

在现有"回测不是证明策略好，而是证明策略不坏"原则基础上，增加：

> **"如果一个策略无法通过PBO<50%检测，它就不值得被纳入投票池。"**

---

## 五、技术实现建议

### 5.1 CSCV计算伪代码

```python
def cscv_pbo(returns_matrix, metric_fn=sharpe_ratio):
    """
    returns_matrix: (n_strategies, n_periods) 各策略在各期的收益
    metric_fn: 评价指标函数（如夏普比率）
    """
    S = 8  # 分块数，偶数
    blocks = split_into_blocks(returns_matrix, S)
    
    rankings = []
    for train_indices in combinations(range(S), S//2):
        test_indices = [i for i in range(S) if i not in train_indices]
        
        train_returns = concatenate_blocks(blocks, train_indices)
        test_returns = concatenate_blocks(blocks, test_indices)
        
        # 在训练集上找最优策略
        is_metrics = [metric_fn(r) for r in train_returns]
        best_strategy_idx = argmax(is_metrics)
        
        # 在测试集上排名
        oos_metrics = [metric_fn(r) for r in test_returns]
        oos_rank = rank_of(best_strategy_idx, oos_metrics)
        
        rankings.append(oos_rank)
    
    # PBO = 排名在后50%的频率
    pbo = sum(r > len(rankings)/2 for r in rankings) / len(rankings)
    return pbo
```

### 5.2 集成到现有回测框架

建议在 `BACKTEST_FRAMEWORK_DESIGN_v1.0.md` 的"Phase 3: 回测验证"中增加：

```
阶段3.5: 过拟合检测
├── 输入: 策略参数矩阵 + 回测收益矩阵
├── 输出: PBO值 + 是否通过标记
├── 阈值: PBO < 0.5（宽松）/ PBO < 0.3（严格）
├── 失败处理: 拒绝该策略，记录原因，不进入投票池
└── 依赖: CSCV模块（Python实现，基于NumPy）
```

---

## 六、Kimi取舍总结

### ✅ 必须纳入系统
- **CSCV-PBO检测**：作为策略入池的强制性门槛
- **Bootstrap显著性检验**：作为策略可信度验证
- **Walk-Forward分析**：已在设计中，保持并强化
- **策略衰减监控**：上线后的"持续回测"

### ⚠️ 可选增强
- **Monte Carlo参数扰动**：测试最优参数附近区域的稳健性
- **GAN对抗验证**：生成"平行市场"环境，过于复杂，暂不考虑
- **多策略组合PBO**：计算整个策略组合（而非单策略）的过拟合概率

### ❌ 不纳入
- **纯随机序列检验**：过于基础，不能检测结构化过拟合
- **仅依赖样本外测试**：样本外测试本身也可能被过拟合（因为可能反复调整直到样本外也好看）

---

> 文件：BACKTEST_ROBUSTNESS_v1.0.md
> 生产者：Kimi（搜索+设计）
> 关联：BACKTEST_FRAMEWORK_DESIGN_v1.0.md、BACKTEST_AND_ATTRIBUTION_DESIGN_v1.0.md
> 状态：设计参考，需编程AI实现CSCV模块
