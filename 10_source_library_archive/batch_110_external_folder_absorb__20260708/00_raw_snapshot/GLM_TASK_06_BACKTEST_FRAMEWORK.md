# GLM 任务指令 06：回测框架设计与全流程验证

> 制作人：Kimi（任务分发）
> 目标：GLM 设计一个可运行的回测框架原型，将缠论 + TK 外汇体系串联测试
> 前置条件：
>   - 缠论对象卡：CHZL_FX/BI/ZS/BC/BSD（公式已冻结）
>   - TK 对象卡：TK-IB/DB/CB + R6/R7/R8（阈值已冻结）
>   - KD MTF P0：6字段已冻结
>   - MTS 测试集：EURUSD H4（20根K线，覆盖分型→笔→中枢→背驰→买卖点）
> 输出要求：Python 伪代码 + 框架架构图 + 回测报告模板 + 测试断言

---

## 任务概述

现在缠论和 TK 的核心对象都已工程化（伪代码 + 字段冻结），下一步是设计一个**回测框架**，把这些对象串起来验证：

1. 缠论公式是否正确（分型 → 笔 → 中枢 → 背驰 → 买卖点）
2. TK 信号是否有效（IB/DB/CB + R6/R7/R8 过滤）
3. 两者互锁后的融合信号是否比单一信号更好
4. 与 KD MTF P0 的联合决策是否降低了噪音

---

## 第一部分：回测框架架构设计

### 1.1 框架选型建议

请 GLM 从以下架构中选一种并说明理由：

| 架构 | 优点 | 缺点 | 适合场景 |
|------|------|------|---------|
| **Event-Driven**（事件驱动） | 逐K线处理，接近实盘 | 慢，代码复杂 | 高精度验证 |
| **Vectorized**（向量化） | 快，适合参数扫描 | 无法处理动态状态（如中枢的实时扩展） | 初步筛选 |
| **Hybrid**（混合） | 向量化计算指标 + 事件驱动处理信号 | 实现复杂 | 推荐采用 |

**推荐：Hybrid 架构**
- 向量化层：一次性计算所有技术指标（KD MTF、MACD、AO、Volty）
- 事件驱动层：逐K线处理缠论结构（分型、笔、中枢的状态机）和 TK 信号（IB/DB/CB 的实时检测）
- 决策层：每根K线结束时，综合所有对象的输出，生成 `lock_signal`

### 1.2 模块划分

```python
# 框架模块结构
backtest_framework/
├── data_loader.py          # 加载 OHLC + 计算基础指标（KD, MACD, AO, ATR）
├── chzl_engine.py          # 缠论引擎：FX → BI → ZS → BC → BSD
├── tk_engine.py            # TK 引擎：IB/DB/CB + R6/R7/R8
├── kd_mtf_engine.py        # KD MTF P0：6字段计算
├── fusion_layer.py         # 融合层：互锁规则 + lock_signal 生成
├── portfolio.py            # 仓位管理：固定金额风险（Van Tharp 风格）
├── performance.py          # 绩效统计：胜率、盈亏比、最大回撤、夏普
└── report_generator.py     # 报告生成：HTML/Markdown 回测报告
```

### 1.3 核心流程伪代码

```python
FUNCTION RunBacktest(config):
    # 1. 加载数据
    bars = LoadData(config.symbol, config.timeframe, config.start_date, config.end_date)
    
    # 2. 向量化计算基础指标（一次性）
    kd_data = CalculateKDMTF(bars, config.kd_params)      # KD MTF P0
    macd_data = CalculateMACD(bars, config.macd_params)     # CHZL_BC 用
    ao_data = CalculateAO(bars, config.ao_params)           # TK_R7 用
    atr_data = CalculateATR(bars, 14)                     # TK_R8 / Volty 用
    
    # 3. 初始化引擎状态
    chzl_state = InitializeCHZLState()    # 空的分型/笔/中枢列表
    tk_state = InitializeTKState()        # 空的 IB/DB/CB 列表
    portfolio = InitializePortfolio(config.initial_capital, config.risk_per_trade)
    
    # 4. 逐K线事件循环（事件驱动层）
    FOR i, bar IN enumerate(bars):
        # 4.1 更新缠论结构（增量计算）
        chzl_state = UpdateCHZL(chzl_state, bar, macd_data[i])
        # 输出：fx_list, bi_list, zs_list, bc_flag, bsd_type
        
        # 4.2 更新 TK 信号（增量计算）
        tk_state = UpdateTK(tk_state, bar, atr_data[i], ao_data[i])
        # 输出：ib_list, db_signals, cb_signals, r6_status, r7_flag, r8_pass
        
        # 4.3 融合决策
        lock_signal = GenerateLockSignal(
            kd_data[i],           # KD MTF P0 当前状态
            chzl_state,           # 缠论当前状态
            tk_state              # TK 当前状态
        )
        
        # 4.4 执行交易
        IF lock_signal IN ['PERFECT_LONG', 'PERFECT_SHORT']:
            trade = ExecuteTrade(portfolio, bar, lock_signal, config.risk_per_trade)
            portfolio.trades.append(trade)
        
        # 4.5 更新持仓（止损/止盈/信号失效）
        portfolio = UpdatePositions(portfolio, bar, chzl_state, tk_state)
    
    # 5. 生成报告
    report = GenerateReport(portfolio, bars)
    RETURN report
```

---

## 第二部分：测试用例设计

### 2.1 单元测试（每个对象独立验证）

请 GLM 为每个对象设计 3-5 个单元测试用例：

```python
# 示例：CHZL_FX 单元测试
TEST_CASE_1:
    input: [3根K线，中间高点最高，低点也最高] → 预期：top_fractal
TEST_CASE_2:
    input: [5根K线，连续包含关系] → 预期：合并后只剩3根，识别1个分型
TEST_CASE_3:
    input: [2根K线，不足3根] → 预期：none

# 示例：TK-IB 单元测试
TEST_CASE_1:
    input: [当前K线 high=10, low=5, 前一根 high=12, low=4] → 预期：is_ib=True
TEST_CASE_2:
    input: [当前K线 high=13, low=5, 前一根 high=12, low=4] → 预期：is_ib=False (high突破)
TEST_CASE_3:
    input: [当前K线 high=11, low=3, 前一根 high=12, low=4] → 预期：INVALID_TOUCH_LOW
```

### 2.2 集成测试（对象组合验证）

```python
# 集成测试 1：缠论完整链
TEST_CASE:
    input: EURUSD H4 模拟数据（MTS 测试集）
    steps:
        1. 确认 T12 出现 BOT_FX
        2. 确认 T12 形成向下笔 Bi_3
        3. 确认 T11 形成中枢 ZS（ZG=1.095, ZD=1.092）
        4. 确认 T12 触发 BOT_DIVERGENCE（MACD面积缩小）
        5. 确认 BSD = 2Buy（类三买）
    assert: lock_signal == 'PERFECT_LONG' (假设 KD 金叉)

# 集成测试 2：TK + 缠论互锁
TEST_CASE:
    input: TK-CB 做多触发 + CHZL_BC = divergence_top
    steps:
        1. TK-CB 触发做多
        2. 缠论背驰显示顶部
    assert: lock_signal == 'REDUCE_POSITION' (不是 PERFECT_LONG)

# 集成测试 3：噪音过滤
TEST_CASE:
    input: KD alignment = conflict + CHZL_ZS = EXTENDING
    steps:
        1. KD 多周期冲突
        2. 价格在中枢内部震荡
    assert: lock_signal == 'NOISE_IGNORE'
```

### 2.3 回测测试（完整历史数据）

```python
# 回测配置模板
CONFIG:
    symbol: "EURUSD"
    timeframe: "H4"
    start_date: "2024-01-01"
    end_date: "2024-12-31"
    initial_capital: 10000
    risk_per_trade: 0.02  # 2% 固定风险
    
    # 参数网格（用于后续优化）
    kd_params: {week: 9, day: 9, h4: 9}
    macd_params: {fast: 12, slow: 26, signal: 9}
    ao_params: {fast: 5, slow: 34}
    atr_period: 14
    
# 回测断言
ASSERT:
    - total_return > 0  # 必须正收益
    - win_rate >= 0.35  # 最低胜率（TK系统 RR>1:1.5 时 35% 即可盈利）
    - max_drawdown < 0.20  # 最大回撤 < 20%
    - profit_factor > 1.5  # 盈亏比 > 1.5
    - sharpe_ratio > 1.0   # 夏普 > 1.0
```

---

## 第三部分：回测报告模板

请 GLM 设计一份 Markdown 格式的回测报告模板，包含：

```markdown
# 回测报告：缠论 + TK 融合策略

## 1. 测试配置
- 资产：EURUSD H4
- 时间：2024-01-01 ~ 2024-12-31
- 初始资金：$10,000
- 风险/单：2%

## 2. 绩效指标
| 指标 | 数值 | 阈值 | 状态 |
|------|------|------|------|
| 总收益率 | 15.3% | > 0% | ✅ |
| 胜率 | 42.1% | ≥ 35% | ✅ |
| 盈亏比 | 1.78 | > 1.5 | ✅ |
| 最大回撤 | 12.4% | < 20% | ✅ |
| 夏普比率 | 1.34 | > 1.0 | ✅ |
| 交易次数 | 156 | - | - |
| 平均持仓时间 | 18.5 hours | - | - |

## 3. 分对象统计
- CHZL_BSD 触发次数：89（其中 1Buy 23次，2Buy 34次，3Buy 32次）
- TK-CB 触发次数：67（与 CHZL_BSD 重叠 45次，独立 22次）
- KD MTF 过滤掉的噪音：41次（lock_signal = NOISE_IGNORE）
- R6 增强 TP3 概率：28次（其中 18次成功到达 TP3）
- R7 预警风险：12次（其中 5次避免了大亏损）
- R8 过滤掉的无效入场：19次

## 4. 失效分析
- 最大单笔亏损：-$198（原因：R7 预警未触发，背驰失败）
- 连续亏损最大次数：5次（2024-03-15 ~ 2024-03-22，震荡市）
- 缠论失效场景：中枢延伸过久，没有形成 BSD
- TK 失效场景：1分钟数据加载不足，XBreaking 无信号

## 5. 参数敏感度分析
- KD 周期从 (9,9,9) 改为 (12,12,12)：胜率下降 3%，但盈亏比上升 0.2
- MACD 参数 (12,26,9) vs (8,17,9)：后者更敏感，假背驰增加
- ATR 倍数从 0.5 改为 1.0：入场次数减少 15%，但胜率提升 5%

## 6. 结论与下一步
- 当前策略通过所有回测阈值，可以进入模拟盘测试
- 建议优化：R6 的 threshold 从 0.236 调整到 0.382 可能过滤更多假信号
- 建议补充：增加币圈 7x24h 的非交易时段过滤（RSJ 优化）
```

---

## 第四部分：约束与建议

1. **框架语言**：Python 伪代码（不要写完整的 backtrader/zipline 集成代码）
2. **数据接口**：假设输入是 pandas DataFrame（columns: open, high, low, close, volume）
3. **状态管理**：缠论的中枢和笔是**有状态**的（不能向量化），必须用事件驱动处理
4. **TK 信号**：XBreaking 的 1H 以下排障逻辑必须在数据加载阶段处理
5. **性能基准**：向量化层应在 1 秒内处理 10,000 根 K 线；事件驱动层应在 1 秒内处理 1,000 根 K 线

---

## 输出文件命名建议

`GLM_TASK_06_BACKTEST_FRAMEWORK_v1.0.md`

请按上述4个部分组织文档，包含：
1. 框架架构图（用文字/表格描述）
2. 每个模块的输入输出接口定义
3. 完整的单元测试 + 集成测试用例（可直接给程序员实现）
4. 回测报告模板（Markdown 格式）
