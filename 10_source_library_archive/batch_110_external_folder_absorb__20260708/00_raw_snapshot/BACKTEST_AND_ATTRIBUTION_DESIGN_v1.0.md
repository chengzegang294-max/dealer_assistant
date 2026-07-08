# 回测稳健性与绩效归因设计参考 v1.0

> **文档编号**: REF-BACKTEST-v1.0
> **创建日期**: 2026-07-07
> **依赖文档**: `EXTERNAL_STRATEGY_RAW_MATERIAL_v3.0.md` + `BACKTEST_FRAMEWORK_DESIGN_v1.0.md` + `BACKTEST_REPORT_TEMPLATE_v1.0.md`
> **用途**: 将第四批外部搜索的启发（日历效应/事件驱动/过拟合检测/绩效归因）转化为回测框架和报告模块的可落地方案。
> **原则**: 回测不是"证明策略好"，而是"证明策略不坏"。

---

## 1. 核心问题：回测的诚实性

> "回测表现亮眼的策略往往在实盘中折戟沉沙，核心原因之一便是过拟合。"

我们的系统在设计回测框架时，必须遵循**"诚实回测"原则**：
- 不美化结果（不隐藏交易成本、不忽略滑点）
- 不盲目相信历史（过拟合检测是强制环节）
- 不只看最终收益（归因分解才能知道"为什么赚钱"）

---

## 2. v1.0 增强（回测框架核心）

### 2.1 增强一：日历效应日历（MACRO_ENVIRONMENT_SCORER）

**问题**: 现有 `MACRO_ENVIRONMENT_SCORER` 只有五维度（利率/汇率/流动性/风险偏好/政策），缺少"时间维度"的季节性信息。

**外部启发**: A股显著的日历效应（春季躁动/四月决断/五穷六绝/黑周四/春节效应），虽然传统规律在弱化，但仍可作为"软性预警"。

**设计方案**:

```python
# 新增模块：SEASONAL_CALENDAR（季节日历）
# 不新增对象卡，而是作为 MACRO_ENVIRONMENT_SCORER 的子模块

class SeasonalCalendar:
    """
    季节日历：标记当前日期附近的传统风险/机会窗口
    注意：日历效应是概率参考，不是确定性信号，只作为"软性调整"
    """
    
    CALENDAR_EVENTS = {
        # 月份效应
        "spring_rally": {
            "months": [1, 2, 3],
            "bias": "positive",           # 传统偏强
            "confidence": 0.6,            # 置信度（近年弱化）
            "note": "春季躁动，流动性宽松+政策预期",
        },
        "april_decision": {
            "months": [4],
            "bias": "volatile",           # 分化加剧
            "confidence": 0.7,
            "note": "四月决断，业绩验证期，警惕暴雷",
        },
        "summer_lull": {
            "months": [5, 6],
            "bias": "negative",           # 传统偏弱
            "confidence": 0.5,            # 近年弱化最明显
            "note": "五穷六绝，年中流动性收紧",
        },
        "july_rebound": {
            "months": [7],
            "bias": "positive",
            "confidence": 0.5,
            "note": "七翻身，流动性改善",
        },
        "year_end_defense": {
            "months": [12],
            "bias": "defensive",          # 防御板块占优
            "confidence": 0.6,
            "note": "年末机构调仓，蓝筹稳健",
        },
        
        # 假日效应
        "spring_festival": {
            "pre_days": 5,                # 节前5天
            "post_days": 15,              # 节后15天
            "bias": "positive",
            "confidence": 0.65,
            "note": "春节效应，避险资金回流+节后流动性宽松",
        },
        "dragon_boat": {
            "post_days": 7,
            "bias": "negative",
            "confidence": 0.55,
            "note": "端午劫，年中资金面紧张",
        },
        
        # 星期效应
        "monday_effect": {
            "weekday": 0,                 # 周一
            "bias": "positive",
            "confidence": 0.5,            # 近年弱化
            "note": "红周一，周末消息释放+情绪修复",
        },
        "thursday_effect": {
            "weekday": 3,                 # 周四
            "bias": "negative",
            "confidence": 0.45,           # 近年弱化最明显
            "note": "黑周四，T+1规避周末风险",
        },
        
        # 财报季效应
        "earnings_season_q1": {
            "months": [4],                # 一季报截止
            "bias": "volatile",
            "confidence": 0.7,
            "note": "一季报密集披露，基本面主导",
        },
        "earnings_season_h1": {
            "months": [7, 8],             # 中报
            "bias": "volatile",
            "confidence": 0.7,
            "note": "中报披露期",
        },
        "earnings_season_q3": {
            "months": [10],               # 三季报
            "bias": "volatile",
            "confidence": 0.7,
            "note": "三季报披露期",
        },
        "earnings_season_annual": {
            "months": [1, 2],             # 年报预告
            "bias": "volatile",
            "confidence": 0.7,
            "note": "年报预告期，业绩雷高发",
        },
    }
    
    def get_current_bias(self, date):
        """
        获取当前日期的季节性偏差
        返回: {"bias": str, "confidence": float, "notes": list}
        """
        biases = []
        total_confidence = 0
        
        for event_name, event in self.CALENDAR_EVENTS.items():
            if self._is_active(date, event):
                biases.append(event["bias"])
                total_confidence += event["confidence"]
        
        # 合并多个效应的偏差
        if not biases:
            return {"bias": "neutral", "confidence": 0, "notes": []}
        
        # 简单投票：多数效应的偏向
        from collections import Counter
        bias_counts = Counter(biases)
        dominant_bias = bias_counts.most_common(1)[0][0]
        avg_confidence = total_confidence / len(biases)
        
        return {
            "bias": dominant_bias,
            "confidence": min(avg_confidence, 0.7),  # 上限0.7（日历效应不可过度信赖）
            "notes": [f"{name}: {event['note']}" for name, event in self.CALENDAR_EVENTS.items() 
                      if self._is_active(date, event)],
        }

# 对 PERIOD_QUEEN 的影响
def adjust_regime_by_calendar(pq_state, calendar_bias, calendar_confidence):
    """
    根据日历效应调整 regime_state 参数
    """
    adjustments = {}
    
    if calendar_bias == "negative" and calendar_confidence > 0.5:
        # 传统弱势窗口：提高门槛，降低仓位
        adjustments["entry_min_votes"] = pq_state.entry_min_votes + 1
        adjustments["position_max_size"] = max(0, pq_state.position_max_size - 0.1)
        adjustments["calendar_note"] = f"传统弱势窗口（置信度{calendar_confidence:.0%}），系统更谨慎"
        
    elif calendar_bias == "positive" and calendar_confidence > 0.5:
        # 传统强势窗口：略微降低门槛（但不盲目追涨）
        adjustments["entry_min_votes"] = max(2, pq_state.entry_min_votes - 1)
        adjustments["calendar_note"] = f"传统强势窗口（置信度{calendar_confidence:.0%}），系统更积极"
        
    elif calendar_bias == "volatile":
        # 波动窗口：提高门槛，强调风控
        adjustments["entry_min_votes"] = pq_state.entry_min_votes + 1
        adjustments["van_tharp_max_risk"] = pq_state.van_tharp_max_risk * 0.8  # 更严格
        adjustments["calendar_note"] = "业绩披露期/波动窗口，风控收紧"
    
    return adjustments

# 对 A5 选股层的影响
def adjust_a5_weights_by_calendar(a5_weights, month):
    """
    根据月份调整A5选股维度权重
    """
    seasonal_adjustments = {
        # 春季（1-3月）：成长板块权重增加
        (1, 2, 3): {"growth_weight": +0.1, "value_weight": -0.05},
        # 年末（12月）：防御板块权重增加
        (12,): {"value_weight": +0.1, "growth_weight": -0.05},
        # 4月：业绩确定性权重增加
        (4,): {"profitability_weight": +0.1},
    }
    
    for months, adj in seasonal_adjustments.items():
        if month in months:
            for key, delta in adj.items():
                a5_weights[key] = a5_weights.get(key, 0) + delta
    
    return a5_weights
```

**数据需求**: 仅需日期信息。`proxy_quantizable_now`（纯规则）。

---

### 2.2 增强二：事件驱动排雷（A5 选股层）

**问题**: 现有 `A5` 排雷机制只有7项（大股东质押/法律诉讼/商誉暴雷等），缺少事件驱动的风险预警（限售股解禁、高送转陷阱）。

**外部启发**: 事件驱动研究——限售股解禁、高送转、盈利不及预期都是显著的风险事件。

**设计方案**:

```python
# A5 排雷机制增强（新增排雷项）
a5_event_driven_red_flags = {
    # 新增排雷项1：限售股解禁预警
    "lockup_expiry_30d": {
        "description": "未来30日内有限售股解禁",
        "risk": "解禁后原始股东可能减持，造成抛压",
        "severity": "HIGH",  # 直接排除
        "data_source": "Wind 限售股解禁数据",
    },
    "lockup_expiry_90d_large": {
        "description": "未来90日内解禁占总股本>10%",
        "risk": "大规模解禁可能导致长期股价承压",
        "severity": "HIGH",
        "data_source": "Wind 限售股解禁数据",
    },
    
    # 新增排雷项2：高送转陷阱
    "high_transfer_ratio": {
        "description": "送转比例>10送10（即每10股送转>10股）",
        "risk": "高送转通常是数字游戏，缺乏基本面支撑，容易成为出货工具",
        "severity": "MEDIUM",  # 警告但不直接排除
        "additional_check": "若同时大股东减持 → 升级为HIGH",
    },
    "high_transfer_no_profit_growth": {
        "description": "高送转但净利润增速<10%",
        "risk": "送转后EPS被严重摊薄，缺乏业绩支撑的填权不可能",
        "severity": "HIGH",
    },
    
    # 新增排雷项3：盈利不及预期
    "earnings_miss": {
        "description": "最新季报实际盈利 < 一致预期（或预告下限）",
        "risk": "业绩miss通常导致股价下跌",
        "severity": "MEDIUM",
    },
    "earnings_guidance_down": {
        "description": "公司下调全年业绩指引",
        "risk": "基本面恶化信号",
        "severity": "HIGH",
    },
    
    # 新增排雷项4：分红异常
    "dividend_cut": {
        "description": "分红率较上年度显著下降（>50%）",
        "risk": "现金流恶化或盈利下滑",
        "severity": "MEDIUM",
    },
    "dividend_yield_trap": {
        "description": "股息率>8%但净利润增速<0%",
        "risk": "高股息不可持续，可能是周期顶点",
        "severity": "HIGH",
    },
}

# 事件日历（融入 MACRO_ENVIRONMENT_SCORER）
class EventCalendar:
    """
    事件日历：标记未来确定的事件窗口
    """
    
    UPCOMING_EVENTS = {
        "earnings_season_q1": {"month": 4, "day_range": (1, 30), "type": "earnings"},
        "earnings_season_h1": {"month": 7, "day_range": (1, 31), "type": "earnings"},
        "earnings_season_q3": {"month": 10, "day_range": (1, 31), "type": "earnings"},
        "earnings_pre_annual": {"month": 1, "day_range": (1, 31), "type": "earnings"},
        "spring_festival": {"type": "holiday", "variable_date": True},  # 农历春节
        "two_sessions": {"month": 3, "day_range": (1, 15), "type": "policy"},  # 两会
    }
    
    def get_event_risk_level(self, date, symbol):
        """
        获取某股票在某日期的事件风险等级
        """
        risk_level = "LOW"
        notes = []
        
        # 检查是否在财报季
        if self._is_earnings_season(date):
            # 检查该股票是否即将披露财报
            if self._has_earnings_announcement_soon(symbol, date):
                risk_level = "MEDIUM"
                notes.append("即将披露财报，业绩不确定性增加")
        
        # 检查限售股解禁
        lockup_info = self._get_lockup_expiry(symbol, date)
        if lockup_info and lockup_info["days_to_expiry"] <= 30:
            risk_level = "HIGH"
            notes.append(f"未来{lockup_info['days_to_expiry']}天有限售股解禁")
        
        return risk_level, notes
```

**数据需求**: 限售股解禁数据、财报披露日程、高送转公告。Wind 已有部分。标记为 `needs_extra_data`（但核心数据可用）。

---

### 2.3 增强三：回测稳健性验证模块（核心）

**问题**: 现有 `BACKTEST_FRAMEWORK_DESIGN_v1.0.md` 定义了回测引擎，但缺少**强制性的稳健性验证流程**。没有验证的回测结果是不可信的。

**外部启发**: 过拟合检测是"交易系统优化的核心环节"，Walk-Forward是"检验策略稳健性的黄金标准"。

**设计方案**:

```python
# 回测框架新增模块：validation/
# 每个对象卡/策略组合在上线前必须通过以下验证

class ValidationSuite:
    """
    回测稳健性验证套件
    原则：不通过验证 = 不允许上线
    """
    
    VALIDATION_STAGES = [
        "economic_logic",       # 经济逻辑检验
        "out_of_sample",        # 样本外测试
        "parameter_sensitivity", # 参数敏感性
        "walk_forward",         # Walk-Forward分析
        "monte_carlo",          # 蒙特卡洛模拟
    ]
    
    def __init__(self, strategy, data, benchmark):
        self.strategy = strategy
        self.data = data
        self.benchmark = benchmark
        self.results = {}
    
    def run_full_validation(self):
        """
        运行完整验证流程
        返回: {"passed": bool, "stage_results": dict, "recommendation": str}
        """
        for stage in self.VALIDATION_STAGES:
            result = getattr(self, f"_{stage}")()
            self.results[stage] = result
            
            if not result["passed"]:
                return {
                    "passed": False,
                    "failed_stage": stage,
                    "stage_results": self.results,
                    "recommendation": result["recommendation"],
                }
        
        return {
            "passed": True,
            "stage_results": self.results,
            "recommendation": "通过全部验证，可以上线",
        }

# 1. 经济逻辑检验
class EconomicLogicTest:
    """
    检查策略是否有明确的市场理论支撑
    """
    
    CHECKLIST = [
        "策略逻辑是否基于可解释的市场规律？（如趋势延续、均值回归）",
        "信号生成是否有明确的因果关系？（而非纯统计相关性）",
        "参数设置是否有经济学直觉？（如20日均线对应一个月交易周期）",
        "策略是否只在特定市场条件下有效？（是否有状态切换机制）",
    ]
    
    def test(self, strategy):
        score = 0
        for item in self.CHECKLIST:
            if strategy.can_explain(item):
                score += 1
        
        passed = score >= 3  # 至少3/4通过
        return {"passed": passed, "score": score, "max": len(self.CHECKLIST)}

# 2. 样本外测试
class OutOfSampleTester:
    """
    训练集优化参数，测试集验证
    """
    
    def __init__(self, train_ratio=0.7):
        self.train_ratio = train_ratio
    
    def test(self, strategy, data):
        # 划分训练集/测试集
        split_idx = int(len(data) * self.train_ratio)
        train_data = data[:split_idx]
        test_data = data[split_idx:]
        
        # 训练集优化参数
        optimized_params = strategy.optimize(train_data)
        
        # 测试集验证（不改参数）
        test_result = strategy.run(test_data, optimized_params)
        train_result = strategy.run(train_data, optimized_params)
        
        # 判断标准：测试集夏普/回撤与训练集差异<20%
        sharpe_ratio_diff = abs(test_result.sharpe - train_result.sharpe) / train_result.sharpe
        max_drawdown_diff = abs(test_result.max_drawdown - train_result.max_drawdown) / abs(train_result.max_drawdown)
        
        passed = sharpe_ratio_diff < 0.2 and max_drawdown_diff < 0.2
        
        return {
            "passed": passed,
            "train_sharpe": train_result.sharpe,
            "test_sharpe": test_result.sharpe,
            "sharpe_diff": sharpe_ratio_diff,
            "train_drawdown": train_result.max_drawdown,
            "test_drawdown": test_result.max_drawdown,
            "drawdown_diff": max_drawdown_diff,
        }

# 3. 参数敏感性测试
class ParameterSensitivityAnalyzer:
    """
    检查策略是否依赖"尖峰"参数
    """
    
    def test(self, strategy, data, param_ranges, n_grid=5):
        """
        参数网格扫描
        """
        results = []
        
        for param_name, (min_val, max_val) in param_ranges.items():
            values = np.linspace(min_val, max_val, n_grid)
            param_results = []
            
            for val in values:
                test_params = strategy.default_params.copy()
                test_params[param_name] = val
                result = strategy.run(data, test_params)
                param_results.append({"param": val, "sharpe": result.sharpe, "drawdown": result.max_drawdown})
            
            # 判断：性能波动<20%
            sharpe_values = [r["sharpe"] for r in param_results]
            sharpe_cv = np.std(sharpe_values) / np.mean(sharpe_values)  # 变异系数
            
            results.append({
                "param": param_name,
                "sharpe_cv": sharpe_cv,
                "stable": sharpe_cv < 0.2,
                "grid_results": param_results,
            })
        
        all_stable = all(r["stable"] for r in results)
        
        return {"passed": all_stable, "param_results": results}

# 4. Walk-Forward 分析
class WalkForwardAnalyzer:
    """
    滚动窗口验证，最贴近实盘逻辑
    """
    
    def __init__(self, n_windows=10, optimization_window=252, validation_window=63):
        """
        n_windows: 滚动窗口数
        optimization_window: 优化窗口（约1年交易日）
        validation_window: 验证窗口（约1季度）
        """
        self.n_windows = n_windows
        self.opt_window = optimization_window
        self.val_window = validation_window
    
    def test(self, strategy, data):
        window_results = []
        
        for i in range(self.n_windows):
            start = i * self.val_window
            opt_end = start + self.opt_window
            val_end = opt_end + self.val_window
            
            if val_end > len(data):
                break
            
            opt_data = data[start:opt_end]
            val_data = data[opt_end:val_end]
            
            # 优化
            params = strategy.optimize(opt_data)
            # 验证
            result = strategy.run(val_data, params)
            
            window_results.append(result)
        
        # 判断：各窗口表现一致性高
        sharpe_values = [r.sharpe for r in window_results]
        sharpe_cv = np.std(sharpe_values) / np.mean(sharpe_values)
        
        passed = sharpe_cv < 0.3 and all(r.sharpe > 0.5 for r in window_results)
        
        return {
            "passed": passed,
            "n_windows": len(window_results),
            "sharpe_mean": np.mean(sharpe_values),
            "sharpe_std": np.std(sharpe_values),
            "sharpe_cv": sharpe_cv,
            "window_results": window_results,
        }

# 5. 蒙特卡洛模拟
class MonteCarloSimulator:
    """
    随机打乱历史路径，评估策略鲁棒性
    """
    
    def __init__(self, n_simulations=1000):
        self.n_simulations = n_simulations
    
    def test(self, strategy, data):
        final_pnls = []
        
        for _ in range(self.n_simulations):
            # 方法1：随机打乱日收益率顺序
            shuffled_returns = data["returns"].sample(frac=1, replace=False).reset_index(drop=True)
            
            # 重建价格序列
            shuffled_data = self._rebuild_prices_from_returns(shuffled_returns)
            
            # 运行策略
            result = strategy.run(shuffled_data)
            final_pnls.append(result.total_pnl)
        
        # 判断：95%路径盈利
        pnl_percentiles = np.percentile(final_pnls, [5, 50, 95])
        p95_profit = pnl_percentiles[0] > 0  # 第5百分位>0（95%盈利）
        
        passed = p95_profit
        
        return {
            "passed": passed,
            "n_simulations": self.n_simulations,
            "pnl_median": pnl_percentiles[1],
            "pnl_p5": pnl_percentiles[0],
            "pnl_p95": pnl_percentiles[2],
            "profit_ratio": sum(1 for p in final_pnls if p > 0) / len(final_pnls),
        }
```

**对编程AI的指令**: 在 `src/backtest_engine/validation/` 目录下实现上述5个验证类。每个对象卡在 `src/backtest_engine/objects/` 中必须实现 `optimize()` 和 `explain()` 方法，以支持验证流程。

---

## 3. v1.1 增强（绩效归因模块）

### 3.1 Brinson 绩效归因

**问题**: 现有 `BACKTEST_REPORT_TEMPLATE_v1.0.md` 只有基础指标（收益/回撤/夏普），缺少**归因分解**——不知道"为什么赚钱/亏钱"。

**设计方案**:

```python
# 新增模块：src/backtest_engine/attribution/

class BrinsonAttribution:
    """
    Brinson 绩效归因模型
    将组合超额收益分解为：配置收益 + 选股收益 + 交互收益
    """
    
    def __init__(self, portfolio_weights, benchmark_weights, portfolio_returns, benchmark_returns):
        """
        portfolio_weights: dict {industry: weight}
        benchmark_weights: dict {industry: weight}
        portfolio_returns: dict {industry: return}
        benchmark_returns: dict {industry: return}
        """
        self.w_p = portfolio_weights
        self.w_b = benchmark_weights
        self.r_p = portfolio_returns
        self.r_b = benchmark_returns
    
    def calculate(self):
        """
        BHB形式：
        超额收益 = 配置收益 + 选股收益 + 交互收益
        """
        industries = set(self.w_p.keys()) | set(self.w_b.keys())
        
        allocation_effect = 0
        selection_effect = 0
        interaction_effect = 0
        
        for ind in industries:
            w_p = self.w_p.get(ind, 0)
            w_b = self.w_b.get(ind, 0)
            r_p = self.r_p.get(ind, 0)
            r_b = self.r_b.get(ind, 0)
            
            allocation_effect += (w_p - w_b) * r_b
            selection_effect += w_b * (r_p - r_b)
            interaction_effect += (w_p - w_b) * (r_p - r_b)
        
        return {
            "allocation_effect": allocation_effect,
            "selection_effect": selection_effect,
            "interaction_effect": interaction_effect,
            "total_excess": allocation_effect + selection_effect + interaction_effect,
        }

# 对A股的适配
class AShareBrinsonAttribution(BrinsonAttribution):
    """
    A股版Brinson归因
    行业分类：申万或中信一级行业
    基准：沪深300/中证500/中证1000
    """
    
    INDUSTRY_CLASSIFICATION = "sw_level1"  # 申万一级行业
    BENCHMARK_OPTIONS = {
        "large_cap": "000300.SH",    # 沪深300
        "mid_cap": "000905.SH",      # 中证500
        "small_cap": "000852.SH",    # 中证1000
    }
    
    def __init__(self, portfolio, benchmark_name="large_cap"):
        self.portfolio = portfolio
        self.benchmark_code = self.BENCHMARK_OPTIONS[benchmark_name]
        
        # 获取行业权重和收益（从Wind或本地数据）
        self.w_p, self.r_p = self._get_portfolio_industry_data(portfolio)
        self.w_b, self.r_b = self._get_benchmark_industry_data(self.benchmark_code)
        
        super().__init__(self.w_p, self.w_b, self.r_p, self.r_b)
    
    def _get_portfolio_industry_data(self, portfolio):
        """计算组合的行业权重和收益"""
        industry_weights = {}
        industry_returns = {}
        
        for stock in portfolio.holdings:
            industry = stock.industry  # 申万行业
            weight = stock.weight
            stock_return = stock.period_return
            
            industry_weights[industry] = industry_weights.get(industry, 0) + weight
            industry_returns[industry] = industry_returns.get(industry, 0) + weight * stock_return
        
        # 加权平均收益
        for ind in industry_returns:
            if industry_weights[ind] > 0:
                industry_returns[ind] /= industry_weights[ind]
        
        return industry_weights, industry_returns

# 三层归因报告结构
class AttributionReport:
    """
    三层归因报告
    """
    
    def generate(self, portfolio, benchmark):
        report = {
            "level_1_brinson": BrinsonAttribution(portfolio, benchmark).calculate(),
            "level_2_factor": self._factor_attribution(portfolio, benchmark),
            "level_3_decomposition": self._return_decomposition(portfolio),
        }
        return report
    
    def _factor_attribution(self, portfolio, benchmark):
        """
        第二层：多因子归因
        （v1.2实现，v1.1可跳过）
        """
        pass
    
    def _return_decomposition(self, portfolio):
        """
        第三层：收益分解
        总收益 = 交易收益 + 选股收益 + 择时收益 + 基准收益 + 交易成本
        """
        return {
            "trading_pnl": portfolio.trading_pnl,
            "selection_pnl": portfolio.selection_pnl,
            "timing_pnl": portfolio.timing_pnl,
            "benchmark_pnl": portfolio.benchmark_pnl,
            "transaction_cost": portfolio.transaction_cost,
        }
```

**数据需求**: 行业分类数据（申万/中信）、基准指数行业权重数据。Wind 已有。`proxy_quantizable_now`。

---

## 4. 回测报告模板增强

### 4.1 三级报告结构（与已有文档整合）

```
回测报告（BACKTEST_REPORT_TEMPLATE_v1.0.md 增强）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
一级报告（单因子/单对象卡）
  ├─ 基础指标：年化收益、最大回撤、夏普、胜率、盈亏比
  ├─ 稳健性验证：样本外测试、Walk-Forward、参数敏感性（新增）
  └─ 推荐结论：通过/不通过/有条件通过

二级报告（策略组合）
  ├─ 基础指标：组合收益、组合回撤、组合夏普
  ├─ 稳健性验证：蒙特卡洛模拟（新增）
  ├─ Brinson归因：配置收益、选股收益、交互收益（新增）
  └─ 策略协同度：各对象卡信号相关性分析

三级报告（系统级）
  ├─ 全系统基础指标
  ├─ 三层归因报告（Brinson + 多因子 + 收益分解）（新增）
  ├─ 制度模式对比：不同 regime 下的策略表现差异
  ├─ 日历效应分析：各季节/事件窗口的表现（新增）
  └─ 策略衰减监测：近期表现vs历史表现（新增）
```

---

## 5. 对编程 AI 的指令

### 5.1 v1.0 新增任务（第四批）

1. **实现季节日历模块** (`src/backtest_engine/calendar/seasonal_calendar.py`):
   - 输入：日期
   - 输出：`bias`, `confidence`, `notes`
   - 与 `MACRO_ENVIRONMENT_SCORER` 和 `PERIOD_QUEEN` 联动

2. **增强 A5 排雷机制** (`src/data_pipeline/fundamental/a5_red_flags.py`):
   - 新增限售股解禁预警、高送转陷阱、盈利miss检测
   - 数据接口：预留Wind限售解禁/财报数据接口

3. **实现回测验证套件** (`src/backtest_engine/validation/`):
   - `EconomicLogicTest`（经济逻辑检验）
   - `OutOfSampleTester`（样本外测试）
   - `ParameterSensitivityAnalyzer`（参数敏感性）
   - `WalkForwardAnalyzer`（Walk-Forward分析）
   - 每个对象卡必须实现 `optimize()` 和 `explain()` 方法

4. **增强回测报告模板** (`src/backtest_engine/reporting/`):
   - 单因子报告增加稳健性验证章节
   - 策略组合报告增加Brinson归因章节

### 5.2 v1.1 新增任务（第四批）

5. **实现蒙特卡洛模拟** (`src/backtest_engine/validation/monte_carlo.py`):
   - 随机打乱日收益率序列，重建价格，运行策略
   - 1000次模拟，输出盈利比例、置信区间

6. **实现 Brinson 归因** (`src/backtest_engine/attribution/brinson.py`):
   - 输入：组合持仓 + 基准
   - 输出：配置收益、选股收益、交互收益
   - 使用申万一级行业分类

7. **实现策略衰减监测** (`src/backtest_engine/monitoring/strategy_decay.py`):
   - 对比近期表现（最近3个月）与历史表现
   - 当近期表现显著低于历史均值时，触发预警

---

## 6. 与全部四批搜索的整合

四批搜索覆盖了量化交易的完整生命周期：

```
四批搜索覆盖图
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第一批：框架与基础策略（vnpy/Backtrader/Qlib/Lean）
        → 系统架构选择、数据管道设计、模块划分

第二批：具体策略与系统（多因子/趋势/均值回归/打板）
        → ADX过滤、动态阈值、交易量确认、组合风控、均值回归

第三批：微观结构与情绪（集合竞价/尾盘/情绪/板块轮动）
        → 缺口统计、竞价成交量、尾盘异动、恐惧贪婪指数、行业动量

第四批：日历效应与回测质量（日历/事件/过拟合/归因）
        → 季节日历、事件排雷、样本外测试、WF分析、蒙特卡洛、Brinson归因

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
全部四批 = 一个完整的量化系统设计方案
```

---

> 文件：BACKTEST_AND_ATTRIBUTION_DESIGN_v1.0.md
> 生产者：Kimi（基于第四批搜索+现有架构融合）
> 用途：回测稳健性与绩效归因的可落地方案
> 与v1.0/v2.0关系：v1.0覆盖策略增强；v2.0覆盖微观结构/情绪；本文覆盖回测质量/归因
> 关联文件：
>   - `EXTERNAL_STRATEGY_RAW_MATERIAL_v3.0.md`（第四批原始资料）
>   - `BACKTEST_FRAMEWORK_DESIGN_v1.0.md`（回测框架）
>   - `BACKTEST_REPORT_TEMPLATE_v1.0.md`（报告模板）
>   - `MACRO_ENVIRONMENT_SCORER_v1.0.md`（宏观评分）
>   - `A5_FUNDAMENTAL_INTEGRATION_v1.0.md`（A5选股层）
