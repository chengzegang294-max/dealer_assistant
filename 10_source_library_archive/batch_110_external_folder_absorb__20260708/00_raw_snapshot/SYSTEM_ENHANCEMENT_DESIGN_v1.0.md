# 系统增强设计参考 v1.0 — A股制度/算法执行/组合优化/Barra因子/可视化

> **文档类型**：系统设计规格书（可给编程 AI 参考实现）
> **版本**：v1.0 | 最后更新：2026-07-07
> **状态**：✅ 可编码 | 优先级：P1（部分模块为P0增强）
> **前置依赖**：
>   - `EXTERNAL_STRATEGY_RAW_MATERIAL_v6.0.md`（原始资料）
>   - `LIVE_TRADING_SYSTEM_DESIGN_v1.0.md`（实盘系统）
>   - `BACKTEST_FRAMEWORK_DESIGN_v1.0.md`（回测框架）
>   - `RISK_ARCHITECTURE_P0_R_v1.0.md`（风控架构）

---

## 一、概述

本文档基于第七批外部搜索（ABCDE五个方向），为投资管家系统提供**五个维度的增强设计**。这些增强不是核心架构变更，而是对现有系统的补充和细化。

```
五大增强维度：

A. A股特殊交易制度 → 风控门控细化 + 回测撮合规则完善
B. 算法交易执行   → 订单拆分策略 + 执行层增强
C. 组合优化       → 权重分配模块（投票后→执行前）
D. Barra因子体系  → 数据预处理流水线 + 因子评估
E. 可视化监控     → 控制台面板组件 + 监控联动机制
```

---

## 二、A. A股特殊交易制度 → 风控门控与回测撮合

### 2.1 涨跌幅规则库（2026年7月最新）

```python
# src/backtest_engine/types.py 或 src/config/market_rules.py

from enum import Enum
from dataclasses import dataclass

class MarketSegment(Enum):
    """A股市场板块分类。"""
    MAIN_BOARD_SH = "主板_沪"      # ±10%
    MAIN_BOARD_SZ = "主板_深"      # ±10%
    STAR_MARKET = "科创板"          # ±20%
    CHINEXT = "创业板"              # ±20%
    BSE = "北交所"                  # ±30%
    ST_MAIN = "ST主板"              # ±10%（2026年7月新规）
    STAR_ST = "ST科创/创业"         # ±20%
    DELISTING_SZ_MAIN = "退市整理_深主板"   # 首日无限制，后续10%
    DELISTING_SZ_CY = "退市整理_深创业"     # 首日无限制，后续20%
    DELISTING_SH = "退市整理_沪"            # 首日无限制，后续按原板块
    NEW_STOCK_MAIN = "新股_主板"    # 前5日无限制
    NEW_STOCK_STAR = "新股_科创"   # 前5日无限制
    NEW_STOCK_BSE = "新股_北交"    # 首日无限制

@dataclass(frozen=True)
class PriceLimitRule:
    """涨跌停规则定义。"""
    segment: MarketSegment
    upper_limit_pct: float       # 涨停幅度
    lower_limit_pct: float       # 跌停幅度
    new_stock_days_no_limit: int # 新股无限制天数
    st_limit_pct: float          # ST股限制（如有差异）
    min_order_unit: int          # 最小申报单位
    increment_unit: int          # 递增单位

# 规则库
PRICE_LIMIT_RULES = {
    MarketSegment.MAIN_BOARD_SH: PriceLimitRule(
        segment=MarketSegment.MAIN_BOARD_SH,
        upper_limit_pct=0.10,
        lower_limit_pct=-0.10,
        new_stock_days_no_limit=5,
        st_limit_pct=0.10,       # ⚠️ 2026年7月新规：从0.05放宽到0.10
        min_order_unit=100,
        increment_unit=100,
    ),
    MarketSegment.STAR_MARKET: PriceLimitRule(
        segment=MarketSegment.STAR_MARKET,
        upper_limit_pct=0.20,
        lower_limit_pct=-0.20,
        new_stock_days_no_limit=5,
        st_limit_pct=0.20,
        min_order_unit=200,      # 科创板200股起
        increment_unit=1,        # 超过200股以1股递增
    ),
    MarketSegment.BSE: PriceLimitRule(
        segment=MarketSegment.BSE,
        upper_limit_pct=0.30,
        lower_limit_pct=-0.30,
        new_stock_days_no_limit=1,  # 北交所首日无限制
        st_limit_pct=0.30,
        min_order_unit=100,
        increment_unit=1,        # 北交所1股递增
    ),
    # ... 其他板块
}
```

### 2.2 涨跌停保护风控检查

```python
# src/trading_engine/execution/risk_gate.py

class RiskGate:
    def _check_price_limit(self, order: Order, market_data: MarketSnapshot) -> CheckResult:
        """
        涨跌停保护：
        - 涨停价不卖（卖单价格 ≤ 涨停价）
        - 跌停价不买（买单价格 ≥ 跌停价）
        - 已涨停股票不可买入（除非有卖盘）
        - 已跌停股票不可卖出（除非有买盘）
        """
        rule = self._get_price_limit_rule(order.symbol)
        
        # 计算涨停价和跌停价
        if market_data.last_close > 0:
            upper_price = market_data.last_close * (1 + rule.upper_limit_pct)
            lower_price = market_data.last_close * (1 + rule.lower_limit_pct)
        else:
            # 新股前5日无涨跌幅限制
            return CheckResult(True, "新股无涨跌幅限制")
        
        if order.direction == Direction.LONG:
            # 买入：价格不能高于涨停价
            if order.limit_price > upper_price:
                return CheckResult(False, f"PRICE_LIMIT_UPPER: 买入价{order.limit_price} > 涨停价{upper_price}")
            # 已涨停检查：如果最新价 == 涨停价且卖盘极少
            if abs(market_data.last_price - upper_price) < 0.01 and market_data.ask1_volume < 100:
                return CheckResult(False, "PRICE_LIMIT_HIT_UPPER: 已涨停，买入可能无法成交")
        
        elif order.direction == Direction.SHORT:
            # 卖出：价格不能低于跌停价
            if order.limit_price < lower_price:
                return CheckResult(False, f"PRICE_LIMIT_LOWER: 卖出价{order.limit_price} < 跌停价{lower_price}")
            # 已跌停检查
            if abs(market_data.last_price - lower_price) < 0.01 and market_data.bid1_volume < 100:
                return CheckResult(False, "PRICE_LIMIT_HIT_LOWER: 已跌停，卖出可能无法成交")
        
        return CheckResult(True, "OK")
    
    def _check_order_unit(self, order: Order) -> CheckResult:
        """检查申报单位合规性。"""
        rule = self._get_price_limit_rule(order.symbol)
        
        if order.quantity < rule.min_order_unit:
            return CheckResult(False, f"MIN_ORDER_UNIT: 数量{order.quantity} < 最小单位{rule.min_order_unit}")
        
        if order.quantity > rule.min_order_unit:
            remainder = (order.quantity - rule.min_order_unit) % rule.increment_unit
            if remainder != 0:
                return CheckResult(False, 
                    f"INCREMENT_UNIT: 数量{order.quantity}不符合递增单位{rule.increment_unit}"
                )
        
        return CheckResult(True, "OK")
```

### 2.3 回测撮合规则细化

```python
# src/backtest_engine/execution/mock_broker.py

class AShareMatchingEngine:
    """
    A股回测撮合引擎，严格遵循T+1和涨跌停规则。
    
    撮合规则：
    1. T+1：当日买入不可卖出
    2. 价格优先、时间优先
    3. 集合竞价：9:15-9:25（9:20后不可撤单）
    4. 收盘集合竞价：14:57-15:00（不可撤单）
    5. 涨跌停：超出范围的订单成为"废单"
    6. 新股前N日无涨跌幅限制（按板块）
    """
    
    def match_order(self, order: Order, bar: Bar, rule: PriceLimitRule) -> FillResult:
        """
        撮合单笔订单。
        
        返回：
        - FILLED：完全成交
        - PARTIAL_FILLED：部分成交
        - REJECTED：废单（价格超限、数量不合规等）
        - PENDING：挂单中（限价单未触价）
        """
        # 1. 检查是否废单
        if not self._is_valid_order(order, bar, rule):
            return FillResult(status=OrderState.REJECTED, filled_qty=0)
        
        # 2. 市价单/限价单撮合
        if order.order_type == OrderType.MARKET:
            # 市价单：按对手方最优价成交
            fill_price = bar.open if order.direction == Direction.LONG else bar.close
        else:
            # 限价单：检查是否触价
            if order.direction == Direction.LONG and order.limit_price >= bar.low:
                fill_price = min(order.limit_price, bar.high)
            elif order.direction == Direction.SHORT and order.limit_price <= bar.high:
                fill_price = max(order.limit_price, bar.low)
            else:
                return FillResult(status=OrderState.PENDING, filled_qty=0)
        
        # 3. 应用滑点
        fill_price = self._apply_slippage(fill_price, order, bar, rule)
        
        # 4. 应用流动性限制（大额订单可能部分成交）
        max_fillable = self._calculate_max_fillable(order, bar)
        filled_qty = min(order.quantity, max_fillable)
        
        if filled_qty < order.quantity:
            return FillResult(
                status=OrderState.PARTIAL_FILLED,
                filled_qty=filled_qty,
                fill_price=fill_price,
            )
        
        return FillResult(
            status=OrderState.FILLED,
            filled_qty=filled_qty,
            fill_price=fill_price,
        )
```

---

## 三、B. 算法交易执行 → 订单拆分策略

### 3.1 算法执行模块设计

```python
# src/trading_engine/execution/algo_executor.py

from abc import ABC, abstractmethod
from enum import Enum

class AlgoType(Enum):
    """算法交易类型。"""
    TWAP = "twap"           # 时间加权平均价格
    VWAP = "vwap"           # 成交量加权平均价格
    POV = "pov"             # 成交量百分比
    ICEBERG = "iceberg"     # 冰山订单
    SIMPLE = "simple"       # 简单直接执行（默认）

class AlgoExecutor(ABC):
    """算法执行器基类。"""
    
    @abstractmethod
    def split_order(self, parent_order: Order, market_data: MarketData) -> list[ChildOrder]:
        """将父订单拆分为子订单。"""
        pass
    
    @abstractmethod
    def next_child(self, executed_children: list[ChildOrder]) -> ChildOrder | None:
        """决定下一笔子订单。"""
        pass

class TWAPExecutor(AlgoExecutor):
    """
    TWAP：时间加权平均价格。
    
    将交易时间均匀分割，每个分割点提交等量的子订单。
    优点：简单、稳定、不需要成交量预测。
    适用：流动性较低的市场，或需要稳定执行节奏的场景。
    """
    
    def __init__(self, num_slices: int = 10, time_window_minutes: int = 30):
        self.num_slices = num_slices
        self.time_window = time_window_minutes
        self.interval = time_window_minutes / num_slices
    
    def split_order(self, parent_order: Order, market_data: MarketData) -> list[ChildOrder]:
        qty_per_slice = parent_order.quantity // self.num_slices
        remainder = parent_order.quantity % self.num_slices
        
        children = []
        for i in range(self.num_slices):
            qty = qty_per_slice + (1 if i < remainder else 0)
            children.append(ChildOrder(
                parent_id=parent_order.id,
                symbol=parent_order.symbol,
                quantity=qty,
                direction=parent_order.direction,
                trigger_time=self._calculate_trigger_time(i),
            ))
        return children

class VWAPExecutor(AlgoExecutor):
    """
    VWAP：成交量加权平均价格。
    
    按历史成交量分布比例分配子订单数量。
    优点：执行价格贴近市场均价，降低市场冲击。
    适用：流动性好的大盘股，追求市场均价。
    """
    
    def __init__(self, lookback_days: int = 20, num_slices: int = 10):
        self.lookback_days = lookback_days
        self.num_slices = num_slices
    
    def split_order(self, parent_order: Order, market_data: MarketData) -> list[ChildOrder]:
        # 获取历史成交量分布（按时间段）
        volume_profile = self._get_historical_volume_profile(
            parent_order.symbol, 
            self.lookback_days
        )
        
        # 按成交量比例分配
        total_volume = sum(volume_profile)
        children = []
        remaining = parent_order.quantity
        
        for i, vol in enumerate(volume_profile):
            ratio = vol / total_volume
            qty = int(parent_order.quantity * ratio)
            qty = min(qty, remaining)  # 不超过剩余数量
            remaining -= qty
            
            children.append(ChildOrder(
                parent_id=parent_order.id,
                symbol=parent_order.symbol,
                quantity=qty,
                direction=parent_order.direction,
                trigger_time=self._calculate_trigger_time(i),
            ))
        
        # 将剩余数量加到最后一个子订单
        if remaining > 0 and children:
            children[-1].quantity += remaining
        
        return children

class IcebergExecutor(AlgoExecutor):
    """
    冰山订单：隐藏大额交易意图。
    
    只显示部分数量于订单簿，成交后自动补充。
    优点：隐蔽性强、减少滑点、防止抢跑。
    适用：需要隐藏真实交易规模的大额交易。
    """
    
    def __init__(self, 
                 display_qty: int = 1000,    # 每次显示的数量
                 min_display_pct: float = 0.02,  # 最小显示比例（2%）
                 max_display_pct: float = 0.08): # 最大显示比例（8%）
        self.display_qty = display_qty
        self.min_display_pct = min_display_pct
        self.max_display_pct = max_display_pct
    
    def split_order(self, parent_order: Order, market_data: MarketData) -> list[ChildOrder]:
        """
        动态调整显示量：
        - 薄市场（流动性差）：显示量小（1%-3%）
        - 深度市场（流动性好）：显示量大（5%-8%）
        """
        # 根据市场深度调整显示比例
        market_depth = market_data.ask1_volume + market_data.bid1_volume
        if market_depth < 10000:
            display_pct = self.min_display_pct
        elif market_depth > 100000:
            display_pct = self.max_display_pct
        else:
            display_pct = self.min_display_pct + (market_depth - 10000) / 90000 * (self.max_display_pct - self.min_display_pct)
        
        display_qty = max(self.display_qty, int(parent_order.quantity * display_pct))
        
        children = []
        remaining = parent_order.quantity
        
        while remaining > 0:
            qty = min(display_qty, remaining)
            children.append(ChildOrder(
                parent_id=parent_order.id,
                symbol=parent_order.symbol,
                quantity=qty,
                direction=parent_order.direction,
                display_qty=qty,  # 显示数量 = 实际数量（冰山效果）
            ))
            remaining -= qty
        
        return children
```

### 3.2 与现有执行层的集成

```python
# src/trading_engine/execution/router.py

class OrderRouter:
    """增强版订单路由：支持算法交易拆分。"""
    
    def __init__(self, broker: BrokerInterface, config: RouterConfig):
        self.broker = broker
        self.config = config
        self.algo_executors: dict[AlgoType, AlgoExecutor] = {
            AlgoType.TWAP: TWAPExecutor(),
            AlgoType.VWAP: VWAPExecutor(),
            AlgoType.ICEBERG: IcebergExecutor(),
        }
    
    def route(self, order: Order) -> OrderResult:
        """
        路由订单：
        1. 判断是否需要算法拆分（大额订单）
        2. 选择算法类型
        3. 拆分为子订单
        4. 逐笔提交
        """
        # 判断是否需要算法执行
        algo_type = self._select_algo(order)
        
        if algo_type == AlgoType.SIMPLE:
            # 小额订单直接执行
            return self.broker.submit(order)
        
        # 大额订单使用算法拆分
        executor = self.algo_executors[algo_type]
        children = executor.split_order(order, self._get_market_data(order.symbol))
        
        # 提交第一笔子订单
        result = self.broker.submit(children[0])
        
        # 启动定时器，后续子订单按计划提交
        self._schedule_remaining_children(children[1:], executor)
        
        return result
    
    def _select_algo(self, order: Order) -> AlgoType:
        """根据订单特征选择算法类型。"""
        account_value = self.account.get_total_value()
        order_value_pct = order.target_value / account_value
        
        # 超过10%资金 → VWAP
        if order_value_pct > 0.10:
            return AlgoType.VWAP
        
        # 超过5%资金 → TWAP
        if order_value_pct > 0.05:
            return AlgoType.TWAP
        
        # 需要隐藏意图 → 冰山
        if order.hide_intent:
            return AlgoType.ICEBERG
        
        return AlgoType.SIMPLE
```

---

## 四、C. 组合优化 → 权重分配模块

### 4.1 模块定位

```
现有流程：
对象卡信号 → 投票 → 风控门控 → [权重分配] → 订单生成 → 执行

权重分配模块在风控门控之后、订单生成之前，负责：
- 将多个信号整合为最优持仓权重
- 考虑组合整体风险（分散化）
- 控制集中度（单标的≤20%，单行业≤30%）
```

### 4.2 权重分配器设计

```python
# src/backtest_engine/weights/portfolio_optimizer.py

from abc import ABC, abstractmethod
import numpy as np
from scipy.optimize import minimize

class WeightAllocator(ABC):
    """权重分配器基类。"""
    
    @abstractmethod
    def allocate(self, 
                 signals: list[Signal], 
                 current_weights: dict[str, float],
                 cov_matrix: np.ndarray,
                 ) -> dict[str, float]:
        """
        输入：对象卡信号 + 当前权重 + 协方差矩阵
        输出：目标权重（各标的占总资金比例）
        """
        pass

class EqualWeightAllocator(WeightAllocator):
    """等权重分配：最简单、最稳健。"""
    
    def allocate(self, signals, current_weights, cov_matrix):
        n = len(signals)
        return {s.symbol: 1.0 / n for s in signals}

class RiskParityAllocator(WeightAllocator):
    """
    风险平价：每个资产对组合风险的贡献相等。
    
    公式：wi ∝ 1/σi（单资产波动率的倒数）
    优点：不依赖预期收益估计，权重稳定。
    """
    
    def allocate(self, signals, current_weights, cov_matrix):
        # 从协方差矩阵提取方差
        variances = np.diag(cov_matrix)
        inv_vol = 1.0 / np.sqrt(variances)
        weights = inv_vol / inv_vol.sum()
        return {s.symbol: w for s, w in zip(signals, weights)}

class MinVarianceAllocator(WeightAllocator):
    """
    最小方差组合：在给定约束下最小化组合波动率。
    
    优化问题：
    min wᵀΣw
    s.t. Σwi = 1, wi ≥ 0
    
    解析解：w* = Σ⁻¹·1 / (1ᵀ·Σ⁻¹·1)
    """
    
    def allocate(self, signals, current_weights, cov_matrix):
        n = len(signals)
        
        # 目标函数：组合方差
        def portfolio_variance(w):
            return w.T @ cov_matrix @ w
        
        # 约束：权重和为1，权重≥0
        constraints = [
            {"type": "eq", "fun": lambda w: np.sum(w) - 1.0},
        ]
        bounds = [(0.0, 0.20) for _ in range(n)]  # 单标的最大20%
        
        # 初始猜测：等权重
        w0 = np.ones(n) / n
        
        # 优化
        result = minimize(
            portfolio_variance,
            w0,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )
        
        return {s.symbol: w for s, w in zip(signals, result.x)}

class KellyAllocator(WeightAllocator):
    """
    凯利公式权重分配：根据各信号的历史表现分配。
    
    已在 OBJECT_CARD_KELLY_P0_R 中定义，此处作为组合层面的整合。
    """
    
    def allocate(self, signals, current_weights, cov_matrix):
        # 使用各对象卡的历史胜率、盈亏比计算凯利分数
        kelly_fractions = {}
        for signal in signals:
            kf = self._calculate_kelly_fraction(signal.object_id)
            kelly_fractions[signal.symbol] = kf
        
        # 归一化到总权重
        total_kf = sum(kelly_fractions.values())
        if total_kf == 0:
            return EqualWeightAllocator().allocate(signals, current_weights, cov_matrix)
        
        # 应用"半凯利"保守原则
        weights = {sym: kf / total_kf * 0.5 for sym, kf in kelly_fractions.items()}
        return weights
```

### 4.3 组合层面的约束

```python
# src/backtest_engine/weights/constraints.py

class PortfolioConstraints:
    """
    组合层面的硬约束（在权重分配后强制执行）。
    
    约束清单：
    1. 单标的 ≤ 20%
    2. 单一行业 ≤ 30%
    3. 总仓位 ≤ 100%（纯多头）
    4. 现金 ≥ 5%（留作缓冲）
    """
    
    MAX_SINGLE_POSITION = 0.20
    MAX_SINGLE_INDUSTRY = 0.30
    MIN_CASH_PCT = 0.05
    
    def apply(self, weights: dict[str, float], 
              industry_map: dict[str, str]) -> dict[str, float]:
        """应用约束，返回调整后的权重。"""
        
        # 1. 单标的上限
        weights = {sym: min(w, self.MAX_SINGLE_POSITION) for sym, w in weights.items()}
        
        # 2. 行业上限
        industry_weights = {}
        for sym, w in weights.items():
            industry = industry_map.get(sym, "其他")
            industry_weights[industry] = industry_weights.get(industry, 0) + w
        
        for industry, iw in industry_weights.items():
            if iw > self.MAX_SINGLE_INDUSTRY:
                # 按比例缩减该行业所有标的权重
                scale = self.MAX_SINGLE_INDUSTRY / iw
                for sym, w in weights.items():
                    if industry_map.get(sym) == industry:
                        weights[sym] *= scale
        
        # 3. 归一化（总权重 = 1 - MIN_CASH_PCT）
        total = sum(weights.values())
        target_total = 1.0 - self.MIN_CASH_PCT
        if total > 0:
            weights = {sym: w / total * target_total for sym, w in weights.items()}
        
        return weights
```

---

## 五、D. Barra因子体系 → 数据预处理流水线

### 5.1 因子数据预处理流水线

```python
# src/data_pipeline/factor_preprocessing.py

import polars as pl
import numpy as np
from scipy import stats

class FactorPreprocessor:
    """
    因子数据预处理四步法（Barra标准）。
    
    Step 1: 去极值（Outlier Removal）
    Step 2: 标准化（Standardization）
    Step 3: 正交化（Orthogonalization）
    Step 4: 中性化（Neutralization）
    """
    
    def __init__(self, method_outlier: str = "MAD", method_std: str = "zscore"):
        self.method_outlier = method_outlier
        self.method_std = method_std
    
    def process(self, 
                df: pl.DataFrame, 
                factor_cols: list[str],
                market_cap_col: str = "market_cap",
                industry_col: str = "industry") -> pl.DataFrame:
        """执行完整的预处理流水线。"""
        
        # Step 1: 去极值
        df = self.remove_outliers(df, factor_cols)
        
        # Step 2: 标准化
        df = self.standardize(df, factor_cols)
        
        # Step 3: 正交化（可选，用于多因子组合）
        # df = self.orthogonalize(df, factor_cols)
        
        # Step 4: 中性化
        df = self.neutralize(df, factor_cols, market_cap_col, industry_col)
        
        return df
    
    def remove_outliers(self, df: pl.DataFrame, factor_cols: list[str]) -> pl.DataFrame:
        """
        去极值：MAD法（中位数绝对偏差）。
        
        MAD = median(|xi - median(x)|)
        有效范围：[median - 3*1.4826*MAD, median + 3*1.4826*MAD]
        """
        for col in factor_cols:
            median = df[col].median()
            mad = (df[col] - median).abs().median()
            lower = median - 3 * 1.4826 * mad
            upper = median + 3 * 1.4826 * mad
            df = df.with_columns(
                pl.col(col).clip(lower, upper).alias(col)
            )
        return df
    
    def standardize(self, df: pl.DataFrame, factor_cols: list[str]) -> pl.DataFrame:
        """
        标准化：Z-Score。
        
        z = (x - μ) / σ
        """
        for col in factor_cols:
            mean = df[col].mean()
            std = df[col].std()
            if std > 0:
                df = df.with_columns(
                    ((pl.col(col) - mean) / std).alias(col)
                )
        return df
    
    def orthogonalize(self, df: pl.DataFrame, factor_cols: list[str]) -> pl.DataFrame:
        """
        正交化：消除因子间相关性。
        
        方法：对称正交（特征值分解）
        S = U · diag(D^(-0.5)) · Uᵀ
        """
        # 提取因子矩阵
        factor_matrix = df.select(factor_cols).to_numpy()
        
        # 计算协方差矩阵
        cov = np.cov(factor_matrix.T)
        
        # 特征值分解
        D, U = np.linalg.eig(cov)
        
        # 构造过渡矩阵
        d = np.diag(D ** (-0.5))
        S = U @ d @ U.T
        
        # 正交化
        orthogonal = factor_matrix @ S
        
        # 更新DataFrame
        for i, col in enumerate(factor_cols):
            df = df.with_columns(pl.Series(col, orthogonal[:, i]))
        
        return df
    
    def neutralize(self, 
                   df: pl.DataFrame, 
                   factor_cols: list[str],
                   market_cap_col: str,
                   industry_col: str) -> pl.DataFrame:
        """
        中性化：消除市值和行业影响。
        
        方法：对市值对数 + 行业哑变量做线性回归，取残差。
        """
        import statsmodels.api as sm
        
        # 准备回归变量
        df = df.with_columns(
            pl.col(market_cap_col).log().alias("log_market_cap")
        )
        
        # 行业哑变量
        industries = df[industry_col].unique().to_list()
        
        for col in factor_cols:
            y = df[col].to_numpy()
            
            # 构建X矩阵：市值对数 + 行业哑变量
            X_data = {"log_cap": df["log_market_cap"].to_numpy()}
            for ind in industries[:-1]:  # 去掉一个避免多重共线性
                X_data[f"ind_{ind}"] = (df[industry_col] == ind).cast(pl.Int32).to_numpy()
            
            X = sm.add_constant(pd.DataFrame(X_data))
            
            # 回归
            model = sm.OLS(y, X).fit()
            residuals = model.resid
            
            # 用残差替代原因子值
            df = df.with_columns(pl.Series(col, residuals))
        
        return df
```

### 5.2 因子评估指标

```python
# src/backtest_engine/performance/factor_analysis.py

class FactorAnalyzer:
    """
    因子分析：评估因子的预测能力和稳定性。
    """
    
    def rank_ic(self, factor_values: pl.Series, future_returns: pl.Series) -> float:
        """
        Rank IC：因子排名与未来收益排名的相关系数。
        
        IC = corr(rank(factor), rank(future_return))
        
        |IC| > 0.03：因子有一定预测能力
        |IC| > 0.05：因子预测能力较强
        """
        from scipy.stats import spearmanr
        
        ic, pvalue = spearmanr(factor_values, future_returns)
        return ic
    
    def ic_ir(self, ic_series: pl.Series) -> float:
        """
        IC_IR = mean(IC) / std(IC)
        
        衡量因子预测能力的稳定性。
        IC_IR > 0.5：因子稳定有效
        """
        return ic_series.mean() / ic_series.std()
    
    def factor_return(self, 
                      factor_values: pl.Series,
                      returns: pl.Series,
                      n_groups: int = 5) -> dict:
        """
        因子分组收益：将股票按因子值分为N组，计算多空收益。
        
        返回：
        - top_group_return: 最高分组收益
        - bottom_group_return: 最低分组收益
        - long_short_return: 多空收益（最高 - 最低）
        """
        # 按因子值分组
        df = pl.DataFrame({
            "factor": factor_values,
            "return": returns,
        }).with_columns(
            pl.col("factor").qcut(n_groups, labels=False).alias("group")
        )
        
        group_returns = df.group_by("group").agg(
            pl.col("return").mean().alias("avg_return")
        ).sort("group")
        
        top = group_returns.filter(pl.col("group") == n_groups - 1)["avg_return"][0]
        bottom = group_returns.filter(pl.col("group") == 0)["avg_return"][0]
        
        return {
            "top_group_return": top,
            "bottom_group_return": bottom,
            "long_short_return": top - bottom,
        }
```

---

## 六、E. 可视化与监控面板 → 控制台增强

### 6.1 控制台面板组件设计

```python
# src/console/panels.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class PanelConfig:
    """面板配置。"""
    name: str
    refresh_interval: int  # 秒
    alert_thresholds: dict[str, tuple[float, float]]  # 指标 -> (预警值, 熔断值)

class MonitoringDashboard:
    """
    监控仪表盘：五层监控体系的可视化实现。
    
    面板布局（终端/ANSI）：
    
    ┌─────────────────────────────────────────────────────────────┐
    │  [首辅] PeriodQueen: BULL          [次辅] TrendFollowing   │
    ├─────────────────────────────────────────────────────────────┤
    │  实时P&L: +2.34% (+12,450元)      日回撤: -0.5%           │
    │  总资产: 1,023,450元              可用资金: 97,500元       │
    ├─────────────────────────────────────────────────────────────┤
    │  [持仓热力图]                                                │
    │  科技: ████████░░ 18%   消费: ████░░░░░░ 8%              │
    │  医药: ██████░░░░ 12%   金融: █████░░░░░ 10%             │
    ├─────────────────────────────────────────────────────────────┤
    │  [风险雷达] 5个维度                                          │
    │  集中度: ●●●○○ 3/5   流动性: ●●●●○ 4/5                    │
    │  波动率: ●●●●● 5/5   相关性: ●●○○○ 2/5                    │
    ├─────────────────────────────────────────────────────────────┤
    │  [活跃信号] 最近5笔                                          │
    │  14:32 CHZL_BSD 买入 000001.SZ 1000股 @10.50               │
    │  14:28 VP       卖出 000002.SZ  500股 @25.30               │
    ├─────────────────────────────────────────────────────────────┤
    │  [告警] ⚠️ 波动率突破阈值 (15% → 18%)                       │
    └─────────────────────────────────────────────────────────────┘
    """
    
    def __init__(self, account: AccountManager, risk_engine: RiskEngine):
        self.account = account
        self.risk = risk_engine
        self.panels = self._init_panels()
    
    def _init_panels(self) -> list[PanelConfig]:
        return [
            PanelConfig("pnl_summary", 5, {
                "daily_pnl": (-0.03, -0.05),
                "drawdown": (0.03, 0.05),
            }),
            PanelConfig("position_heatmap", 30, {
                "single_position": (0.18, 0.25),
                "industry_concentration": (0.25, 0.35),
            }),
            PanelConfig("risk_radar", 10, {
                "portfolio_volatility": (0.15, 0.20),
                "beta": (1.2, 1.5),
            }),
            PanelConfig("signal_log", 5, {}),
            PanelConfig("alert_banner", 1, {}),
        ]
    
    def render(self) -> str:
        """渲染完整仪表盘。"""
        lines = []
        lines.append(self._render_governance_header())
        lines.append(self._render_pnl_summary())
        lines.append(self._render_position_heatmap())
        lines.append(self._render_risk_radar())
        lines.append(self._render_signal_log())
        lines.append(self._render_alert_banner())
        return "\n".join(lines)
    
    def _render_pnl_summary(self) -> str:
        """P&L摘要面板。"""
        pnl = self.account.daily_pnl
        pnl_pct = self.account.daily_pnl_pct
        dd = self.account.get_daily_drawdown()
        total = self.account.get_total_value()
        cash = self.account.cash
        
        color = "\033[32m" if pnl >= 0 else "\033[31m"  # 绿/红
        reset = "\033[0m"
        
        return f"""
┌─────────────────────────────────────────────────────────────┐
│  实时P&L: {color}{pnl_pct:+.2%} ({pnl:+,.0f}元){reset}    日回撤: {dd:.2%}           │
│  总资产: {total:,.0f}元              可用资金: {cash:,.0f}元       │
└─────────────────────────────────────────────────────────────┘"""
    
    def _render_position_heatmap(self) -> str:
        """持仓热力图面板。"""
        positions = self.account.get_positions_by_industry()
        max_pct = max(positions.values()) if positions else 1
        
        lines = ["┌─────────────────────────────────────────────────────────────┐"]
        lines.append("│  [持仓热力图]                                                │")
        
        for industry, pct in sorted(positions.items(), key=lambda x: -x[1]):
            bar_len = int(pct / max_pct * 10)
            bar = "█" * bar_len + "░" * (10 - bar_len)
            lines.append(f"│  {industry:6s}: {bar} {pct:.1f}%                           │")
        
        lines.append("└─────────────────────────────────────────────────────────────┘")
        return "\n".join(lines)
    
    def _render_risk_radar(self) -> str:
        """风险雷达图面板（简化版）。"""
        metrics = self.risk.get_portfolio_risk_metrics()
        
        radar = {
            "集中度": min(metrics["concentration"] / 0.30 * 5, 5),
            "流动性": min(metrics["liquidity"] / 1.0 * 5, 5),
            "波动率": min(metrics["volatility"] / 0.20 * 5, 5),
            "相关性": min(metrics["correlation"] / 0.80 * 5, 5),
            "杠杆": min(metrics["leverage"] / 1.0 * 5, 5),
        }
        
        lines = ["┌─────────────────────────────────────────────────────────────┐"]
        lines.append("│  [风险雷达] 5个维度                                          │")
        
        for name, score in radar.items():
            filled = int(score)
            empty = 5 - filled
            dots = "●" * filled + "○" * empty
            lines.append(f"│  {name:6s}: {dots} {score:.1f}/5                         │")
        
        lines.append("└─────────────────────────────────────────────────────────────┘")
        return "\n".join(lines)
    
    def _render_alert_banner(self) -> str:
        """告警横幅。"""
        alerts = self.risk.get_active_alerts()
        if not alerts:
            return ""
        
        lines = ["┌─────────────────────────────────────────────────────────────┐"]
        for alert in alerts[:3]:  # 最多显示3条
            icon = "🚨" if alert.level == "CRITICAL" else "⚠️"
            lines.append(f"│  {icon} {alert.message:52s}  │")
        lines.append("└─────────────────────────────────────────────────────────────┘")
        return "\n".join(lines)
```

### 6.2 联动机制

```python
# src/console/interaction.py

class PanelInteraction:
    """
    面板联动机制：
    
    1. 点击"持仓热力图"中某行业 → 主图表显示该行业成分股
    2. 点击"风险雷达"中某维度 → 显示该风险项的详细分解
    3. 某标的波动率突破阈值 → 热力图中该标的红闪
    4. 回撤超过5% → P&L面板红色警示
    """
    
    def __init__(self, dashboard: MonitoringDashboard):
        self.dashboard = dashboard
        self.selected_industry: Optional[str] = None
        self.selected_symbol: Optional[str] = None
    
    def on_industry_click(self, industry: str):
        """点击行业热力图。"""
        self.selected_industry = industry
        # 联动：更新持仓列表，只显示该行业股票
        self.dashboard.refresh_position_table(industry_filter=industry)
    
    def on_risk_dimension_click(self, dimension: str):
        """点击风险雷达维度。"""
        # 联动：显示该风险维度的详细分析
        details = self.dashboard.risk.get_risk_detail(dimension)
        self.dashboard.show_detail_panel(details)
    
    def on_threshold_breach(self, metric: str, value: float, threshold: float):
        """阈值突破事件。"""
        # 联动：对应面板高亮/闪烁
        if metric == "drawdown" and value > threshold:
            self.dashboard.flash_panel("pnl_summary", color="red")
        elif metric.startswith("volatility"):
            self.dashboard.flash_cell("position_heatmap", metric, color="red")
```

---

## 七、模块优先级与实现顺序

| 模块 | 优先级 | 依赖 | 说明 |
|------|--------|------|------|
| A股交易规则库 | **P0** | 无 | 风控门控的基础，必须优先实现 |
| 涨跌停保护 | **P0** | 规则库 | 防止废单和无效交易 |
| 回测撮合细化 | **P0** | 规则库 | 确保回测贴近真实 |
| TWAP/VWAP拆分 | P1 | 执行层 | 大额订单优化 |
| 权重分配器 | P1 | 投票+风控 | 组合层面的优化 |
| 因子预处理 | P1 | 数据管道 | 选股层增强 |
| 监控面板组件 | P1 | 控制台 | 用户体验 |
| 冰山订单 | P2 | 执行层 | 高级功能 |
| 面板联动 | P2 | 监控面板 | 交互增强 |

---

## 八、相关文档交叉引用

| 文档 | 关系 | 引用章节 |
|------|------|----------|
| `EXTERNAL_STRATEGY_RAW_MATERIAL_v6.0.md` | 原始资料 | 全部 |
| `LIVE_TRADING_SYSTEM_DESIGN_v1.0.md` | 实盘系统 | 执行层、风控门控 |
| `BACKTEST_FRAMEWORK_DESIGN_v1.0.md` | 回测框架 | 撮合机制 |
| `RISK_ARCHITECTURE_P0_R_v1.0.md` | 风控架构 | Van Tharp、Kelly、VolTarget |
| `MASTER_PROGRAMMING_INSTRUCTION_v1.0.md` | 编程规范 | polars、pytest |
| `EMPEROR_CONSOLE_UI_v1.0.md` | 控制台设计 | 面板布局 |
| `PROGRAMMING_AI_ULTIMATE_TASK_PACKAGE_v1.0.md` | 编码指南 | Phase 1-4 |

---

> 文件：SYSTEM_ENHANCEMENT_DESIGN_v1.0.md
> 生产者：Kimi（基于第七批搜索资料 + 现有系统架构整合）
> 用途：五大方向增强设计参考，可直接给编程 AI 实现
> 状态：✅ 可编码 | 优先级：P1
