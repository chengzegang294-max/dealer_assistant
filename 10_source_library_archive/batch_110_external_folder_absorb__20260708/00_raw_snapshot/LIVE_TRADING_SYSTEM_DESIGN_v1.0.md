# 实盘交易系统设计 v1.0

> **文档类型**：系统设计规格书（可直接给编程 AI 实现）
> **版本**：v1.0 | 最后更新：2026-07-07
> **状态**：✅ 可编码 | 优先级：P0（与回测引擎同等）
> **前置依赖**：
>   - `BACKTEST_FRAMEWORK_DESIGN_v1.0.md`（回测引擎设计）
>   - `RISK_ARCHITECTURE_P0_R_v1.0.md`（风控架构）
>   - `MING_CABINET_HYBRID_ARCHITECTURE_v1.0.md`（治理架构）
>   - `EXTERNAL_STRATEGY_RAW_MATERIAL_v4.0.md`（实盘技术参考资料）

---

## 一、系统概述

### 1.1 设计目标

本系统是一个**面向 A 股个人投资者的量化实盘交易系统**，与现有回测引擎共享同一套信号生成和策略逻辑，但在执行层区分"回测模式"与"实盘模式"。

**核心原则**：
- **回测与实盘统一代码**：同一套信号生成、投票、风控逻辑，仅在最后执行环节替换为模拟成交或真实成交
- **回测诚实性优先**：回测阶段即引入滑点、延迟、流动性影响，避免回测表现与实盘脱节
- **风控前置**：任何订单在离开系统前必须经过独立风控 gate 检查
- **最小可行**：在 Windows 单机部署下运行，不追求机构级高频设施，但保证日频/分钟频策略的可靠执行

### 1.2 系统范围

```
✅ 包含：信号生成（对象卡）→ 投票 → 风控 → 订单生成 → 风控前置 → 券商接口 → 成交确认 → 实时监控 → 灾难恢复
✅ 包含：回测诚实性参数（滑点/延迟/流动性）
✅ 包含：订单生命周期管理（状态机）
✅ 包含：实时账户 P&L 与持仓管理
✅ 包含：运行时风控守护（熔断/告警）
✅ 包含：监控与日志体系
❌ 不包含：高频优化（FPGA/内核旁路/托管机房）
❌ 不包含：机构级合规报送
❌ 不包含：FIX 协议自行实现（使用券商封装 API）
```

### 1.3 运行模式

系统支持三种运行模式，通过治理架构（皇帝控制台）切换：

| 模式 | 执行层行为 | 数据源 | 用途 |
|------|-----------|--------|------|
| **BACKTEST** | 模拟成交（历史数据回放） | 历史 OHLCV | 策略验证、参数优化 |
| **PAPER** | 模拟成交（实时行情，真实订单不发送） | 实时行情 | 上线前验证、策略预热 |
| **LIVE** | 真实成交（通过券商 API 发送订单） | 实时行情 + 券商接口 | 实盘交易 |

> **模式切换保护**：从 BACKTEST → PAPER 或 LIVE 需要皇帝控制台（用户）手动确认，并记录审计日志。

---

## 二、系统架构（全链路）

### 2.1 端到端数据流

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    实盘交易系统全链路                                  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │  数据管道    │ → │  对象卡引擎  │ → │  投票与策略  │ → │  信号缓冲区  │          │
│  │  DataPipe   │    │  ObjEngine  │    │  VoteEngine │    │ SignalBuffer│          │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘          │
│        │                  │                  │                  │                    │
│        │  实时/历史行情    │  对象卡信号      │  策略组合      │  待执行信号队列      │
│        │  OHLCV/Level-2  │  CHZL/VP/BPB... │  TrendFollowing│  (延迟+去重)        │
│        │                │                  │  /Breakout...  │                    │
│        ▼                ▼                  ▼                  ▼                    │
│  ┌─────────────────────────────────────────────────────────────────────────┐        │
│  │                         风控层 (Risk Engine)                             │        │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────┐  │        │
│  │  │ 仓位管理     │ → │ 凯利公式     │ → │ 波动率目标   │ → │ 风控门控  │  │        │
│  │  │ Van Tharp   │    │ Kelly       │    │ VolTarget   │    │ RiskGate │  │        │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └──────────┘  │        │
│  └─────────────────────────────────────────────────────────────────────────┘        │
│                              │                                                      │
│                              ▼                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────┐        │
│  │                      执行层 (Execution Engine)                           │        │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────┐  │        │
│  │  │ 信号→订单   │ → │ 风控前置     │ → │ 订单路由     │ → │ 订单状态机│  │        │
│  │  │ 转换器      │    │ PreRisk     │    │ Router      │    │ Lifecycle │  │        │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └──────────┘  │        │
│  └─────────────────────────────────────────────────────────────────────────┘        │
│                              │                                                      │
│                              ▼                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────┐        │
│  │                      接口层 (Broker Interface)                           │        │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                │        │
│  │  │ 统一接口抽象 │ → │ 模拟实现     │ → │ 券商实现     │                │        │
│  │  │ BrokerAPI   │    │ MockBroker  │    │ QMTBroker   │                │        │
│  │  │             │    │ /PaperBroker│    │ /PtradeBroker│               │        │
│  │  └─────────────┘    └─────────────┘    └─────────────┘                │        │
│  └─────────────────────────────────────────────────────────────────────────┘        │
│                              │                                                      │
│                              ▼                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────┐        │
│  │                      监控层 (Monitoring & Alerting)                      │        │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────┐  │        │
│  │  │ 实时 P&L    │ → │ 订单监控     │ → │ 策略监控     │ → │ 告警通知  │  │        │
│  │  │ AccountMgr  │    │ OrderMonitor│    │ StratMonitor│    │ Alert     │  │        │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └──────────┘  │        │
│  └─────────────────────────────────────────────────────────────────────────┘        │
│                              │                                                      │
│                              ▼                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────┐        │
│  │                      持久层 (Persistence & Recovery)                     │        │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                  │        │
│  │  │ 交易日志     │ → │ 持仓快照     │ → │ 灾难恢复     │                  │        │
│  │  │ TradeLog    │    │ PortfolioSnap│    │ Recovery    │                  │        │
│  │  └─────────────┘    └─────────────┘    └─────────────┘                  │        │
│  └─────────────────────────────────────────────────────────────────────────┘        │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 模块职责表

| 模块 | Python 类 | 职责 | 对应文档 |
|------|-----------|------|----------|
| 信号缓冲区 | `SignalBuffer` | 缓存对象卡输出信号，去重、延迟、排序 | 本文档 §3.1 |
| 风控门控 | `RiskGate` | 前置风控检查（金额/时间/标的/账户状态） | 本文档 §3.2 |
| 订单转换器 | `SignalToOrderConverter` | 将信号转换为目标订单（order_target / order_value / limit_order） | 本文档 §3.3 |
| 风控前置 | `PreTradeRisk` | 独立执行的风控检查（速率/回撤/集中度） | 本文档 §3.4 |
| 订单路由 | `OrderRouter` | 选择券商接口、分配订单、处理报盘 | 本文档 §3.5 |
| 订单状态机 | `OrderLifecycleManager` | 维护订单状态机、处理在途订单、同步券商状态 | 本文档 §3.6 |
| 统一接口 | `BrokerInterface` | 抽象类，定义统一接口 | 本文档 §4.1 |
| 模拟实现 | `MockBroker` / `PaperBroker` | 回测/模拟模式下的模拟成交 | 本文档 §4.2 |
| 券商实现 | `QMTBroker` / `PtradeBroker` | 真实券商 API 对接 | 本文档 §4.3 |
| 实时账户 | `AccountManager` | 实时资金、持仓、P&L 计算 | 本文档 §5.1 |
| 监控告警 | `MonitoringSystem` | 五层监控、阈值检查、告警通知 | 本文档 §5.2 |
| 持久化 | `PersistenceManager` | 交易日志、持仓快照、灾难恢复 | 本文档 §6.1 |

---

## 三、执行层详细设计

### 3.1 信号缓冲区（SignalBuffer）

**问题**：对象卡可能在同一时刻产生多个信号（不同周期、不同标的），需要缓冲和协调。

```python
class SignalBuffer:
    """
    信号缓冲区：暂存对象卡输出，处理后送入执行层。
    
    功能：
    1. 去重：同一标的同一方向信号在 N 分钟内只保留一次
    2. 延迟：将信号延迟 D 秒（模拟从信号生成到执行的真实延迟）
    3. 排序：按优先级（信号强度 × 确定性评分）排序
    4. 聚合：多个对象卡对同一标的的信号可聚合（取平均或最高）
    """
    
    def __init__(self, 
                 dedup_window: timedelta = timedelta(minutes=5),
                 execution_delay: float = 0.0,  # 秒，BACKTEST=0, PAPER=1, LIVE=3
                 ):
        self.buffer: deque[Signal] = deque()
        self.dedup_window = dedup_window
        self.execution_delay = execution_delay
        self._last_signal_time: dict[str, datetime] = {}  # symbol -> last_time
    
    def add(self, signal: Signal) -> bool:
        """添加信号到缓冲区。若触发去重，返回 False。"""
        key = f"{signal.symbol}_{signal.direction}"
        now = datetime.now()
        if key in self._last_signal_time:
            if now - self._last_signal_time[key] < self.dedup_window:
                return False  # 去重
        self._last_signal_time[key] = now
        
        # 添加延迟执行时间
        signal.execute_at = now + timedelta(seconds=self.execution_delay)
        self.buffer.append(signal)
        return True
    
    def get_executable(self) -> list[Signal]:
        """获取所有到达执行时间的信号。"""
        now = datetime.now()
        executable = []
        while self.buffer and self.buffer[0].execute_at <= now:
            executable.append(self.buffer.popleft())
        # 按优先级排序（信号强度 × 置信度）
        executable.sort(key=lambda s: s.strength * s.confidence, reverse=True)
        return executable
```

**与回测引擎的关系**：回测引擎中 `SignalBuffer` 的 `execution_delay` 设为 0（或按回测诚实性参数设置），直接在同一回合处理。

### 3.2 风控门控（RiskGate）

**位置**：在信号转换为订单之前，最后一道轻量检查。

```python
class RiskGate:
    """
    轻量级风控门控：快速检查，不阻塞主路径。
    若检查失败，信号被丢弃或降级，记录原因。
    """
    
    CHECKS = [
        "trading_hours",      # 是否在交易时间（9:30-11:30, 13:00-15:00）
        "price_limit",        # 涨跌停保护（涨停不卖、跌停不买）
        "suspension",         # 停牌/退市检查
        "whitelist",          # 标的白名单
        "max_position",       # 单标的最大持仓比例
        "max_daily_orders",   # 单日最大订单数
    ]
    
    def check(self, signal: Signal, account: AccountState) -> RiskGateResult:
        """返回 (passed: bool, action: str, reason: str)"""
        # 快速检查链，任一失败即返回
        ...
```

**检查项详表**：

| 检查项 | 规则 | 失败动作 | 日志级别 |
|--------|------|----------|----------|
| 交易时间 | 9:30-11:30, 13:00-15:00 | 丢弃信号 | INFO |
| 涨跌停 | 涨停不卖、跌停不买 | 丢弃信号 | WARNING |
| 停牌 | 标的是否处于停牌 | 丢弃信号 | WARNING |
| 白名单 | 标的是否在允许列表 | 丢弃信号 | ERROR |
| 最大持仓 | 单标的 ≤ 总资金 20% | 降级为减仓信号 | WARNING |
| 日订单上限 | 单日 ≤ 100 笔 | 丢弃信号 | ERROR |
| 账户状态 | 资金/持仓是否正常 | 暂停交易 | CRITICAL |

### 3.3 信号→订单转换器（SignalToOrderConverter）

**将对象卡信号转换为具体的交易指令**：

```python
class SignalToOrderConverter:
    """
    将对象卡输出信号转换为券商 API 可接受的订单格式。
    
    支持三种订单类型：
    - TARGET_VALUE: 调整持仓市值到目标值（适合再平衡）
    - TARGET_AMOUNT: 调整持仓数量到目标值（适合精确数量）
    - LIMIT_ORDER: 限价单（适合特定价格）
    """
    
    def convert(self, 
                signal: Signal, 
                account: AccountState,
                order_type: OrderType = OrderType.TARGET_VALUE) -> Order:
        """信号 → 订单"""
        
        # 计算目标仓位
        target_size = self._calculate_target_size(signal, account)
        
        # 根据当前持仓计算 delta
        current = account.get_position(signal.symbol)
        delta = target_size - current.shares
        
        if order_type == OrderType.TARGET_VALUE:
            # 计算目标市值
            target_value = target_size * signal.price
            return Order(
                symbol=signal.symbol,
                order_type=OrderType.TARGET_VALUE,
                target_value=target_value,
                direction=signal.direction,  # LONG/SHORT/EXIT
                trigger_price=signal.price,
                stop_loss=signal.stop_loss,
                reason=signal.reason,
                source_object=signal.object_id,
            )
        ...
    
    def _calculate_target_size(self, signal: Signal, account: AccountState) -> int:
        """根据凯利公式 + 波动率目标 + 风险门控计算目标仓位。"""
        # 1. 凯利公式建议仓位
        kelly_size = kelly_fraction(signal.win_rate, signal.win_loss_ratio) * account.total_value
        # 2. 波动率目标调整
        vol_adj = volatility_target_adjustment(signal.volatility, target_vol=0.15)
        # 3. 取整到 100 股（A股）
        raw_size = int(kelly_size * vol_adj / signal.price)
        return (raw_size // 100) * 100
```

### 3.4 风控前置（PreTradeRisk）

**独立执行的风控检查，比 RiskGate 更严格**：

```python
class PreTradeRisk:
    """
    风控前置：在订单发送到券商前进行深度检查。
    
    设计原则：
    - 独立执行（asyncio 任务或线程池），不阻塞主路径
    - 所有检查通过才允许订单离开系统
    - 检查失败记录详细原因，触发告警
    
    检查项：
    1. 订单速率限制：每分钟 ≤ 20 笔（防止信号风暴）
    2. 单笔金额限制：单笔 ≤ 总资金 10%
    3. 累计金额限制：单日累计 ≤ 总资金 50%
    4. 回撤熔断：日回撤 > 5% 暂停当日交易
    5. 集中度限制：单一行业 ≤ 30%
    6. 资金可用检查：确保账户有足够资金/持仓
    """
    
    def __init__(self, account: AccountManager, config: RiskConfig):
        self.account = account
        self.config = config
        self._order_history: deque[Order] = deque(maxlen=1000)
        self._daily_stats = DailyTradingStats()
    
    async def validate(self, order: Order) -> PreTradeResult:
        """异步风控检查。返回 (allowed, reason, adjusted_order)。"""
        checks = [
            self._check_rate_limit(order),
            self._check_single_order_size(order),
            self._check_daily_cumulative(order),
            self._check_drawdown_circuit(order),
            self._check_concentration(order),
            self._check_account_funds(order),
        ]
        
        for check in checks:
            result = await check
            if not result.passed:
                return PreTradeResult(False, result.reason, None)
        
        # 可能调整订单（如减小数量）
        adjusted = self._adjust_order(order)
        return PreTradeResult(True, "OK", adjusted)
    
    def _check_drawdown_circuit(self, order: Order) -> CheckResult:
        """回撤熔断检查。"""
        dd = self.account.get_daily_drawdown()
        if dd > self.config.max_daily_drawdown:
            return CheckResult(False, f"DRAWDOWN_CIRCUIT: daily drawdown {dd:.2%} > limit {self.config.max_daily_drawdown:.2%}")
        return CheckResult(True, "")
```

**风控配置参数**（默认值）：

```python
@dataclass
class RiskConfig:
    # 订单速率
    max_orders_per_minute: int = 20
    max_orders_per_day: int = 100
    
    # 金额限制
    max_single_order_pct: float = 0.10  # 单笔 ≤ 10%
    max_daily_cumulative_pct: float = 0.50  # 单日累计 ≤ 50%
    max_position_per_symbol_pct: float = 0.20  # 单标的 ≤ 20%
    max_industry_concentration_pct: float = 0.30  # 单行业 ≤ 30%
    
    # 熔断阈值
    max_daily_drawdown: float = 0.05  # 日回撤 > 5% 熔断
    max_single_loss_pct: float = 0.02  # 单笔亏损 > 2% 告警
    
    # 时间窗口
    trading_start: time = time(9, 30)
    trading_end: time = time(15, 0)
    no_trade_window_before_close: timedelta = timedelta(minutes=3)  # 收盘前3分钟不新开仓
```

### 3.5 订单路由（OrderRouter）

**简单路由（个人量化场景）**：

```python
class OrderRouter:
    """
    订单路由：选择对应的券商接口，处理订单发送。
    
    个人量化场景下路由逻辑简单：
    - 上海市场 → 上海柜台
    - 深圳市场 → 深圳柜台
    - 无复杂智能路由（不需要算法交易拆单）
    
    但保留扩展点：若未来需要 VWAP 拆单，可在路由层增加。
    """
    
    def __init__(self, broker: BrokerInterface):
        self.broker = broker
    
    def route(self, order: Order) -> OrderResult:
        """路由订单到券商接口。"""
        # 简单路由：所有订单通过同一接口
        # 未来扩展：大额订单 → VWAP 拆单器
        return self.broker.submit(order)
    
    def cancel(self, order_id: str) -> CancelResult:
        """发送撤单请求。"""
        return self.broker.cancel(order_id)
```

### 3.6 订单状态机（OrderLifecycleManager）

**核心模块：订单从发起到最终确认的全生命周期管理。**

```python
from enum import Enum, auto

class OrderState(Enum):
    """订单状态机。"""
    PENDING = auto()           # 已创建，未发送
    SUBMITTING = auto()        # 正在提交到券商
    SUBMITTED = auto()         # 券商已确认接收
    PARTIAL_FILLED = auto()    # 部分成交
    FILLED = auto()            # 全部成交
    CANCELING = auto()         # 正在撤单
    CANCELLED = auto()         # 已撤单
    REJECTED = auto()          # 被券商拒绝（废单）
    EXPIRED = auto()           # 订单过期（如未成交的限价单）
    ERROR = auto()             # 系统错误

class OrderLifecycleManager:
    """
    订单生命周期管理器：跟踪所有在途订单，维护状态机。
    
    关键设计：
    1. 唯一标识：订单 UUID + 券商返回的 order_id
    2. 状态转换：显式定义合法转换，非法转换触发告警
    3. 同步机制：定期从券商查询订单状态（补偿 6 秒时滞）
    4. 超时处理：SUBMITTED 超过 30 秒未成交 → 自动撤单
    """
    
    # 合法状态转换
    VALID_TRANSITIONS = {
        OrderState.PENDING: {OrderState.SUBMITTING, OrderState.CANCELLED, OrderState.ERROR},
        OrderState.SUBMITTING: {OrderState.SUBMITTED, OrderState.REJECTED, OrderState.ERROR},
        OrderState.SUBMITTED: {OrderState.PARTIAL_FILLED, OrderState.FILLED, OrderState.CANCELING, OrderState.EXPIRED},
        OrderState.PARTIAL_FILLED: {OrderState.FILLED, OrderState.CANCELING},
        OrderState.CANCELING: {OrderState.CANCELLED, OrderState.FILLED},  # 撤单过程中可能成交
    }
    
    def __init__(self, broker: BrokerInterface, sync_interval: int = 5):
        self.broker = broker
        self.sync_interval = sync_interval  # 秒，定期同步频率
        self._orders: dict[str, OrderRecord] = {}  # order_id -> OrderRecord
        self._pending_sync: set[str] = set()  # 需要同步的订单
    
    def create_order(self, order: Order) -> str:
        """创建订单，返回订单 ID。"""
        order_id = str(uuid.uuid4())
        record = OrderRecord(
            order_id=order_id,
            order=order,
            state=OrderState.PENDING,
            created_at=datetime.now(),
            filled_quantity=0,
            avg_fill_price=0.0,
        )
        self._orders[order_id] = record
        return order_id
    
    def submit(self, order_id: str) -> OrderResult:
        """提交订单到券商。"""
        record = self._orders[order_id]
        self._transition(order_id, OrderState.SUBMITTING)
        
        result = self.broker.submit(record.order)
        if result.success:
            record.broker_order_id = result.broker_order_id
            self._transition(order_id, OrderState.SUBMITTED)
            # 启动超时检查
            asyncio.create_task(self._timeout_check(order_id, timeout=30))
        else:
            self._transition(order_id, OrderState.REJECTED)
        return result
    
    def _transition(self, order_id: str, new_state: OrderState):
        """执行状态转换。非法转换触发告警。"""
        record = self._orders[order_id]
        old_state = record.state
        
        if new_state not in self.VALID_TRANSITIONS.get(old_state, set()):
            self._alert_illegal_transition(order_id, old_state, new_state)
            return
        
        record.state = new_state
        record.state_history.append((datetime.now(), old_state, new_state))
        logger.info(f"Order {order_id}: {old_state.name} -> {new_state.name}")
    
    async def _sync_with_broker(self):
        """定期与券商同步订单状态（补偿时滞）。"""
        for order_id in list(self._pending_sync):
            record = self._orders[order_id]
            broker_status = self.broker.query_order(record.broker_order_id)
            self._update_from_broker(order_id, broker_status)
    
    async def _timeout_check(self, order_id: str, timeout: int):
        """超时检查：若订单长期未成交，自动撤单。"""
        await asyncio.sleep(timeout)
        record = self._orders.get(order_id)
        if record and record.state in (OrderState.SUBMITTED, OrderState.PARTIAL_FILLED):
            logger.warning(f"Order {order_id} timeout, auto-canceling")
            await self.cancel(order_id)
```

**状态转换图**：

```
                    ┌──────────┐
                    │  PENDING │
                    └────┬─────┘
                         │ submit()
                         ▼
                   ┌────────────┐
              ┌───→│ SUBMITTING │←────────────────────────┐
              │    └─────┬──────┘                          │
              │          │ broker confirms                   │
         cancel│          ▼                                 │
              │    ┌────────────┐       ┌──────────────┐   │
              └───→│  SUBMITTED │──────→│ PARTIAL_FILLED│───┘
                   └─────┬──────┘       └──────┬───────┘
                         │ fill                    │ fill
                         ▼                         ▼
                   ┌────────────┐              ┌────────┐
                   │   FILLED   │              │ FILLED │
                   └────────────┘              └────────┘
                         │
                    ┌────┴────┐
                    │ CANCELING│
                    └────┬────┘
                         │
                    ┌────┴────┐
                    │CANCELLED│
                    └─────────┘
                    
  REJECTED / EXPIRED / ERROR（异常终止状态）
```

---

## 四、券商接口层

### 4.1 统一接口抽象（BrokerInterface）

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Order:
    """统一订单格式（与券商无关）。"""
    symbol: str
    order_type: OrderType  # TARGET_VALUE / TARGET_AMOUNT / LIMIT
    direction: Direction    # LONG / SHORT / EXIT
    target_value: float = 0.0   # 目标市值（TARGET_VALUE 用）
    target_amount: int = 0     # 目标数量（TARGET_AMOUNT 用）
    limit_price: float = 0.0   # 限价（LIMIT 用）
    stop_loss: float = 0.0     # 止损价
    take_profit: float = 0.0   # 止盈价
    reason: str = ""           # 订单原因（来自哪个对象卡）
    source_object: str = ""    # 来源对象卡 ID

@dataclass
class OrderResult:
    """订单提交结果。"""
    success: bool
    order_id: str = ""           # 系统订单 ID
    broker_order_id: str = ""   # 券商订单 ID
    error_message: str = ""

@dataclass
class OrderStatus:
    """订单状态查询结果。"""
    broker_order_id: str
    state: OrderState
    filled_quantity: int
    avg_fill_price: float
    remaining_quantity: int
    commission: float
    update_time: datetime

class BrokerInterface(ABC):
    """券商接口抽象基类。所有具体券商实现必须继承此类。"""
    
    @abstractmethod
    def connect(self) -> bool:
        """连接券商系统。"""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """断开连接。"""
        pass
    
    @abstractmethod
    def submit(self, order: Order) -> OrderResult:
        """提交订单。"""
        pass
    
    @abstractmethod
    def cancel(self, broker_order_id: str) -> CancelResult:
        """撤单。"""
        pass
    
    @abstractmethod
    def query_order(self, broker_order_id: str) -> OrderStatus:
        """查询订单状态。"""
        pass
    
    @abstractmethod
    def query_account(self) -> AccountState:
        """查询账户状态。"""
        pass
    
    @abstractmethod
    def query_positions(self) -> list[Position]:
        """查询持仓。"""
        pass
    
    @abstractmethod
    def get_market_snapshot(self, symbol: str) -> MarketSnapshot:
        """获取行情快照。"""
        pass
```

### 4.2 模拟实现（MockBroker / PaperBroker）

```python
class MockBroker(BrokerInterface):
    """
    模拟券商：用于回测模式。
    
    成交规则：
    - 使用历史数据的下一根 K 线开盘价或收盘价成交
    - 支持滑点建模
    - 支持延迟模拟
    - 不考虑流动性（假设无冲击成本）
    """
    
    def __init__(self, price_source: PriceSource, slippage: float = 0.001):
        self.price_source = price_source
        self.slippage = slippage
    
    def submit(self, order: Order) -> OrderResult:
        # 立即成交（回测场景）
        price = self.price_source.get_price(order.symbol)
        adjusted_price = price * (1 + self.slippage * random.choice([-1, 1]))
        return OrderResult(success=True, filled_price=adjusted_price)

class PaperBroker(BrokerInterface):
    """
    模拟券商：用于 PAPER 模式（模拟盘）。
    
    与 MockBroker 的区别：
    - 使用实时行情数据
    - 订单发送但不真正提交到交易所（或提交到券商模拟环境）
    - 成交模拟更真实：使用行情快照，考虑买卖盘
    """
    
    def __init__(self, real_time_quote: QuoteSource):
        self.quote = real_time_quote
    
    def submit(self, order: Order) -> OrderResult:
        # 获取实时行情快照
        snapshot = self.quote.get_snapshot(order.symbol)
        # 模拟成交：买按卖一价，卖按买一价
        if order.direction == Direction.LONG:
            fill_price = snapshot.ask1
        else:
            fill_price = snapshot.bid1
        return OrderResult(success=True, filled_price=fill_price)
```

### 4.3 真实券商实现（QMTBroker / PtradeBroker）

```python
class PtradeBroker(BrokerInterface):
    """
    Ptrade 券商接口实现（恒生出品）。
    
    关键约束（来自 Ptrade API 文档）：
    - 股票委托取整 100 股，可转债取整 10 张
    - limit_price 不填时默认用行情快照最新价
    - 持仓同步有 6 秒时滞
    - 需配合在途订单管理（防止重复下单）
    """
    
    def __init__(self, api_client):
        self.api = api_client
        self._order_cache: dict[str, str] = {}  # order_id -> broker_order_id
    
    def submit(self, order: Order) -> OrderResult:
        # 调用 Ptrade API
        if order.order_type == OrderType.TARGET_VALUE:
            broker_id = self.api.order_target_value(
                order.symbol, 
                order.target_value,
                limit_price=order.limit_price or None
            )
        elif order.order_type == OrderType.TARGET_AMOUNT:
            broker_id = self.api.order_target(
                order.symbol,
                order.target_amount,
                limit_price=order.limit_price or None
            )
        ...
        return OrderResult(success=True, broker_order_id=broker_id)
    
    def query_order(self, broker_order_id: str) -> OrderStatus:
        # 查询 Ptrade 订单状态
        raw = self.api.get_order(broker_order_id)
        return self._parse_order_status(raw)
    
    def query_positions(self) -> list[Position]:
        # 查询持仓（注意 6 秒时滞）
        raw = self.api.get_positions()
        return [self._parse_position(p) for p in raw]
    
    def _parse_order_status(self, raw) -> OrderStatus:
        # 映射 Ptrade 状态到统一状态
        state_map = {
            "待报": OrderState.PENDING,
            "已报": OrderState.SUBMITTED,
            "部成": OrderState.PARTIAL_FILLED,
            "已成": OrderState.FILLED,
            "已撤": OrderState.CANCELLED,
            "废单": OrderState.REJECTED,
        }
        return OrderStatus(
            state=state_map.get(raw.status, OrderState.ERROR),
            filled_quantity=raw.filled_volume,
            avg_fill_price=raw.avg_price,
            ...
        )
```

**券商接口映射表**：

| 统一接口 | Ptrade API | QMT API | 模拟实现 |
|----------|-----------|---------|----------|
| `submit` | `order_target` / `order_target_value` | `send_order` | 立即成交 |
| `cancel` | `cancel_order` | `cancel_order` | 立即成功 |
| `query_order` | `get_order` | `query_order` | 返回缓存状态 |
| `query_account` | `get_trading_util` | `get_stock_asset` | 返回初始配置 |
| `query_positions` | `get_positions` | `get_positions` | 返回空持仓 |
| `get_snapshot` | `get_current_data` | `get_stock_quote` | 从数据源读取 |

---

## 五、账户与监控层

### 5.1 实时账户管理（AccountManager）

```python
class AccountManager:
    """
    实时账户管理：跟踪资金、持仓、P&L。
    
    数据来源：
    - 初始状态：从券商查询
    - 增量更新：从订单成交回报
    - 定时同步：每 N 秒从券商查询一次（补偿时滞）
    
    计算方式：
    - 成本：移动平均成本法（T 日实时）
    - P&L：浮动盈亏 + 已实现盈亏 - 交易费用
    - 回撤：从当日最高 P&L 计算
    """
    
    def __init__(self, broker: BrokerInterface):
        self.broker = broker
        self.cash: float = 0.0
        self.positions: dict[str, Position] = {}  # symbol -> Position
        self.trade_log: list[TradeRecord] = []
        self.daily_high_pnl: float = 0.0
        self.daily_pnl: float = 0.0
    
    def update_from_fill(self, fill: FillRecord):
        """从成交回报更新账户。"""
        # 更新持仓（移动平均成本法）
        pos = self.positions.get(fill.symbol)
        if pos:
            total_cost = pos.cost_basis * pos.shares + fill.price * fill.quantity
            total_shares = pos.shares + fill.quantity
            pos.cost_basis = total_cost / total_shares
            pos.shares += fill.quantity
        else:
            self.positions[fill.symbol] = Position(
                symbol=fill.symbol,
                shares=fill.quantity,
                cost_basis=fill.price,
            )
        
        # 更新现金
        self.cash -= fill.price * fill.quantity + fill.commission
        
        # 记录交易
        self.trade_log.append(fill)
        
        # 更新 P&L
        self._update_pnl()
    
    def get_daily_drawdown(self) -> float:
        """计算日回撤。"""
        if self.daily_high_pnl <= 0:
            return 0.0
        return (self.daily_high_pnl - self.daily_pnl) / self.daily_high_pnl
    
    def get_total_value(self) -> float:
        """总资产 = 现金 + 持仓市值。"""
        position_value = sum(
            pos.shares * self._get_last_price(sym) 
            for sym, pos in self.positions.items()
        )
        return self.cash + position_value
    
    async def sync_from_broker(self):
        """从券商同步账户状态（定期补偿时滞）。"""
        account = self.broker.query_account()
        positions = self.broker.query_positions()
        self.cash = account.available_cash
        self.positions = {p.symbol: p for p in positions}
```

### 5.2 监控与告警（MonitoringSystem）

```python
class MonitoringSystem:
    """
    五层监控体系：
    
    Layer 1: 基础设施（CPU/内存/磁盘）
    Layer 2: 应用（进程/日志/接口延迟）
    Layer 3: 交易（订单成功率/成交率/废单率）
    Layer 4: 业务（PnL/回撤/持仓）
    Layer 5: 合规（交易频率/异常行为）
    """
    
    ALERT_THRESHOLDS = {
        # 资金
        "daily_pnl_drawdown": (0.03, 0.05, "CRITICAL"),  # 预警/熔断
        "single_loss_pct": (0.01, 0.02, "WARNING"),
        
        # 执行
        "order_fail_rate": (0.01, 0.05, "ERROR"),
        "reject_rate": (0.005, 0.02, "ERROR"),
        
        # 技术
        "signal_delay_ms": (500, 2000, "WARNING"),
        "quote_delay_ms": (1000, 5000, "CRITICAL"),
        
        # 系统
        "cpu_usage": (0.80, 0.95, "WARNING"),
        "memory_usage": (0.85, 0.95, "ERROR"),
    }
    
    def __init__(self, account: AccountManager, order_mgr: OrderLifecycleManager):
        self.account = account
        self.order_mgr = order_mgr
        self.alert_history: deque[Alert] = deque(maxlen=1000)
    
    async def run(self, interval: int = 5):
        """监控主循环，每 interval 秒检查一次。"""
        while True:
            await asyncio.sleep(interval)
            self._check_fundamental()
            self._check_execution()
            self._check_business()
            self._check_system()
    
    def _check_business(self):
        """检查业务层指标。"""
        dd = self.account.get_daily_drawdown()
        warn, circuit, level = self.ALERT_THRESHOLDS["daily_pnl_drawdown"]
        
        if dd > circuit:
            self._alert(f"DRAWDOWN_CIRCUIT: {dd:.2%}", level="CRITICAL", action="HALT_TRADING")
        elif dd > warn:
            self._alert(f"DRAWDOWN_WARNING: {dd:.2%}", level="WARNING", action="NOTIFY")
    
    def _check_execution(self):
        """检查执行层指标。"""
        stats = self.order_mgr.get_statistics()
        fail_rate = stats.failed / max(stats.total, 1)
        
        if fail_rate > self.ALERT_THRESHOLDS["order_fail_rate"][1]:
            self._alert(f"HIGH_FAIL_RATE: {fail_rate:.2%}", level="ERROR", action="CHECK_BROKER")
    
    def _alert(self, message: str, level: str, action: str):
        """发送告警。"""
        alert = Alert(
            timestamp=datetime.now(),
            level=level,
            message=message,
            action=action,
        )
        self.alert_history.append(alert)
        
        # 通知方式：日志 + 控制台 + 可选邮件/微信
        logger.log(getattr(logging, level), message)
        if level in ("CRITICAL", "ERROR"):
            self._send_immediate_notification(alert)
    
    def _send_immediate_notification(self, alert: Alert):
        """紧急通知（弹窗/声音/邮件）。"""
        # Windows 弹窗
        if os.name == 'nt':
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, alert.message, f"交易告警 [{alert.level}]", 0x10)
```

**监控指标详表**：

| 层级 | 指标 | 预警阈值 | 熔断阈值 | 告警动作 |
|------|------|----------|----------|----------|
| L1 系统 | CPU 使用率 | 80% | 95% | 通知 |
| L1 系统 | 内存使用率 | 85% | 95% | 通知 |
| L2 应用 | 信号延迟 | 500ms | 2000ms | 检查数据源 |
| L2 应用 | 行情延迟 | 1000ms | 5000ms | 切换数据源 |
| L3 交易 | 订单失败率 | 1% | 5% | 检查券商接口 |
| L3 交易 | 废单率 | 0.5% | 2% | 检查参数 |
| L3 交易 | 撤单率 | 10% | 20% | 检查策略 |
| L4 业务 | 日 PnL 回撤 | 3% | 5% | 暂停交易 |
| L4 业务 | 单笔亏损 | 1% | 2% | 通知 |
| L4 业务 | 持仓集中度 | 25% | 35% | 减仓 |
| L5 合规 | 日交易次数 | 80 笔 | 100 笔 | 通知 |

---

## 六、回测诚实性参数

### 6.1 参数包设计

```python
@dataclass
class BacktestHonestyParams:
    """
    回测诚实性参数包：在回测阶段引入实盘摩擦，使回测结果更接近真实。
    
    来源：
    - 滑点：0.05%~0.2%（按流动性调整）
    - 延迟：50~100ms（从信号生成到执行）
    - 流动性：大额订单用 VWAP 拆分（> 1分钟平均成交额 10%）
    """
    
    # 滑点设置
    slippage_fixed: float = 0.0       # 固定滑点（元），0=不使用
    slippage_pct: float = 0.001       # 滑点比例（默认 0.1%）
    slippage_model: str = "random"    # random / fixed / adaptive
    
    # 按流动性调整滑点（A股）
    slippage_tiers: dict[str, float] = field(default_factory=lambda: {
        "large_cap": 0.0005,    # 大盘蓝筹：0.05%
        "mid_cap": 0.001,       # 中盘：0.1%
        "small_cap": 0.002,     # 小盘：0.2%
        "micro_cap": 0.003,     # 微盘：0.3%
    })
    
    # 延迟设置
    signal_delay_ms: float = 0.0      # 信号延迟（ms），BACKTEST=0, PAPER=1000, LIVE=3000
    
    # 流动性影响
    vwap_threshold_pct: float = 0.10   # 超过 1分钟成交额 10% 触发 VWAP 拆分
    vwap_time_window: int = 5         # VWAP 拆分到 5 分钟内执行
    
    # 交易成本
    commission_rate: float = 0.00025  # 佣金率（万 2.5）
    stamp_tax_rate: float = 0.001      # 印花税（卖时千 1）
    transfer_fee_rate: float = 0.00002 # 过户费（十万分之 2）
    min_commission: float = 5.0        # 最低佣金 5 元
```

### 6.2 回测 vs 实盘差异对照表

| 差异项 | 回测假设 | 实盘现实 | 诚实性修正 |
|--------|----------|----------|------------|
| 成交价 | 按 K 线 Close | 买卖盘实际撮合 | 滑点建模 + 买卖价 |
| 执行速度 | 同一 K 线内立即成交 | 几十到几百毫秒延迟 | 延迟补偿 |
| 流动性 | 假设无冲击成本 | 大额订单影响价格 | VWAP 拆分阈值 |
| 交易费用 | 简化或忽略 | 佣金+印花税+过户费 | 完整费用模型 |
| 订单失败 | 假设 100% 成功 | 废单/拒绝/超时 | 模拟失败率 |
| 停牌/涨跌停 | 简化处理 | 真实交易限制 | 完整风控门控 |
| 资金同步 | 假设实时同步 | 6 秒时滞 | 异步同步机制 |

---

## 七、灾难恢复与持久化

### 7.1 持久化机制

```python
class PersistenceManager:
    """
    持久化管理：确保交易数据不丢失，支持灾难恢复。
    
    持久化内容：
    1. 交易日志：每笔订单的完整生命周期（写前日志 WAL）
    2. 持仓快照：定时保存当前持仓和资金
    3. 策略状态：对象卡内部状态（如 CHZL 的笔段缓存）
    4. 配置快照：当前运行配置和参数
    
    写入策略：
    - 交易日志：同步写入（每次状态变更立即写磁盘）
    - 持仓快照：异步写入（每 30 秒一次）
    - 策略状态：仅在关闭时写入
    """
    
    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.wal_file = open(log_dir / "trade.wal", "a")
    
    def log_trade(self, record: TradeRecord):
        """同步写入交易日志（WAL）。"""
        line = json.dumps(record.to_dict(), default=str) + "\n"
        self.wal_file.write(line)
        self.wal_file.flush()
        os.fsync(self.wal_file.fileno())  # 强制刷盘
    
    def save_snapshot(self, account: AccountManager, timestamp: datetime = None):
        """保存持仓快照。"""
        snapshot = {
            "timestamp": (timestamp or datetime.now()).isoformat(),
            "cash": account.cash,
            "positions": {sym: pos.to_dict() for sym, pos in account.positions.items()},
            "daily_pnl": account.daily_pnl,
            "daily_high_pnl": account.daily_high_pnl,
        }
        path = self.log_dir / f"snapshot_{datetime.now():%Y%m%d_%H%M%S}.json"
        with open(path, "w") as f:
            json.dump(snapshot, f, indent=2)
    
    def recover(self) -> RecoveryState:
        """从 WAL 和快照恢复状态。"""
        # 1. 读取最新快照
        # 2. 从快照时间点后读取 WAL，重放所有事件
        # 3. 重建账户状态
        pass
```

### 7.2 灾难恢复策略

| 场景 | 恢复目标 | 恢复方式 | 预计时间 |
|------|----------|----------|----------|
| 策略进程崩溃 | 重启后恢复交易 | 从 WAL + 快照重建 | < 30 秒 |
| 系统断电 | 不丢失已成交数据 | WAL 已刷盘 | 重启后自动恢复 |
| 券商接口断开 | 恢复连接后恢复 | 重连 + 状态同步 | 取决于券商 |
| 网络中断 | 恢复后检查订单状态 | 查询所有在途订单 | 手动确认 |
| 策略异常（无限下单） | 停止交易 | 风控熔断 + 手动干预 | 立即 |

### 7.3 进程守护设计

```python
class TradingDaemon:
    """
    交易守护进程：确保策略进程持续运行，崩溃后自动重启。
    
    Windows 下的实现：
    - 使用 Windows Service 或计划任务
    - 或简单方案：独立 watchdog 脚本，每 10 秒检查主进程
    
    重启策略：
    - 首次崩溃：立即重启（可能是偶发错误）
    - 5 分钟内第二次崩溃：延迟 60 秒重启（避免错误循环）
    - 第三次崩溃：停止自动重启，发送告警等待人工干预
    """
    
    MAX_RESTARTS = 3
    RESTART_WINDOW = 300  # 秒
    
    def watch(self):
        restart_count = 0
        last_restart = 0
        
        while True:
            process = subprocess.Popen(["python", "-m", "trading_engine.main"])
            process.wait()
            
            if process.returncode != 0:
                # 非正常退出
                now = time.time()
                if now - last_restart < self.RESTART_WINDOW:
                    restart_count += 1
                else:
                    restart_count = 1
                
                if restart_count > self.MAX_RESTARTS:
                    self._alert("CRITICAL: Max restarts exceeded, manual intervention required")
                    break
                
                delay = 0 if restart_count == 1 else 60
                self._alert(f"Process crashed, restarting in {delay}s (attempt {restart_count})")
                time.sleep(delay)
                last_restart = now
```

---

## 八、与现有系统的集成

### 8.1 与回测引擎的关系

```
回测引擎（BACKTEST_FRAMEWORK_DESIGN_v1.0.md）
  ├─ 数据管道（共享）
  ├─ 对象卡引擎（共享）
  ├─ 投票机制（共享）
  ├─ 风控层（共享）
  └─ 执行层（替换为模拟实现）
       ├─ SignalBuffer（执行延迟=0）
       ├─ RiskGate（完整检查）
       ├─ SignalToOrderConverter（同实盘）
       ├─ PreTradeRisk（同实盘）
       ├─ OrderRouter（MockBroker）
       ├─ OrderLifecycleManager（简化状态机）
       └─ 无需 AccountManager（回测引擎已有账户跟踪）

实盘引擎（本文档）
  ├─ 数据管道（共享，但切换为实时数据源）
  ├─ 对象卡引擎（共享，同一代码）
  ├─ 投票机制（共享，同一代码）
  ├─ 风控层（共享，但增加实时账户状态）
  └─ 执行层（真实实现）
       ├─ SignalBuffer（执行延迟 > 0）
       ├─ RiskGate（完整检查）
       ├─ SignalToOrderConverter（同回测）
       ├─ PreTradeRisk（完整风控守护）
       ├─ OrderRouter（PtradeBroker/QMTBroker）
       ├─ OrderLifecycleManager（完整状态机 + 同步）
       ├─ AccountManager（实时资金持仓）
       ├─ MonitoringSystem（五层监控）
       └─ PersistenceManager（WAL + 快照）
```

**关键设计：信号层与执行层解耦**

```python
class TradingEngine:
    """总控引擎，整合回测与实盘。"""
    
    def __init__(self, mode: TradingMode, config: EngineConfig):
        self.mode = mode
        self.data_pipe = DataPipeline(config.data)
        self.obj_engine = ObjectCardEngine(config.objects)
        self.vote_engine = VoteEngine(config.vote)
        self.risk_engine = RiskEngine(config.risk)
        
        # 执行层根据模式切换
        if mode == TradingMode.BACKTEST:
            self.execution = BacktestExecution(config.backtest)
        elif mode == TradingMode.PAPER:
            self.execution = LiveExecution(config.live, PaperBroker())
        elif mode == TradingMode.LIVE:
            self.execution = LiveExecution(config.live, PtradeBroker())
    
    def run(self):
        """主循环：数据 → 对象卡 → 投票 → 风控 → 执行。"""
        for bar in self.data_pipe.stream():
            signals = self.obj_engine.process(bar)
            approved = self.vote_engine.vote(signals)
            filtered = self.risk_engine.filter(approved)
            self.execution.execute(filtered)
```

### 8.2 与治理架构的集成

```python
# 在治理引擎（governance_architecture.py）中增加交易模式控制
class GovernanceEngine:
    def __init__(self):
        ...
        self.trading_mode = TradingMode.PAPER  # 默认模拟盘
    
    def switch_mode(self, new_mode: TradingMode):
        """
        模式切换需经皇帝（用户）确认，记录起居注（审计日志）。
        BACKTEST → PAPER: 直接切换
        PAPER → LIVE: 需确认 + 账户检查 + 风险提醒
        LIVE → PAPER: 直接切换（一键清仓）
        """
        if new_mode == TradingMode.LIVE and self.trading_mode != TradingMode.LIVE:
            self._require_emperor_confirmation(
                "切换到实盘模式",
                "当前为模拟盘，切换到实盘将产生真实交易。请确认账户资金和风险设置。"
            )
        self.audit.log_mode_switch(self.trading_mode, new_mode)
        self.trading_mode = new_mode
```

---

## 九、文件路径约定

```
D:\Stock\trading_assistant\  （用户代码仓库）
  └─ src/
      └─ trading_engine/
          ├─ __init__.py
          ├─ main.py                    # 入口
          ├─ config.py                  # 配置管理
          ├─ engine.py                  # TradingEngine 总控
          ├─ modes.py                   # 运行模式枚举
          ├─ data_pipeline/             # 数据管道（与回测共享）
          ├─ object_cards/              # 对象卡（与回测共享）
          ├─ voting/                    # 投票机制（与回测共享）
          ├─ risk/                      # 风控层（与回测共享）
          ├─ execution/                 # 执行层（实盘核心）
          │   ├─ __init__.py
          │   ├─ signal_buffer.py       # 信号缓冲区
          │   ├─ risk_gate.py           # 风控门控
          │   ├─ converter.py           # 信号→订单转换
          │   ├─ pre_trade_risk.py      # 风控前置
          │   ├─ router.py              # 订单路由
          │   ├─ lifecycle.py           # 订单状态机
          │   ├─ backtest_exec.py       # 回测执行器
          │   └─ live_exec.py           # 实盘执行器
          ├─ broker/                    # 券商接口层
          │   ├─ __init__.py
          │   ├─ interface.py           # BrokerInterface 抽象
          │   ├─ mock.py                # MockBroker / PaperBroker
          │   ├─ ptrade.py              # PtradeBroker
          │   └─ qmt.py                 # QMTBroker
          ├─ account/                   # 账户与监控
          │   ├─ __init__.py
          │   ├─ manager.py             # AccountManager
          │   ├─ monitoring.py          # MonitoringSystem
          │   └─ alerts.py              # 告警通知
          ├─ persistence/               # 持久化与恢复
          │   ├─ __init__.py
          │   ├─ wal.py                 # 写前日志
          │   ├─ snapshot.py            # 快照管理
          │   └─ recovery.py            # 灾难恢复
          └─ governance_integration.py  # 与治理架构的集成
```

---

## 十、实现优先级（P0 → P1 → P2）

| 优先级 | 模块 | 说明 |
|--------|------|------|
| **P0** | `BrokerInterface` + `MockBroker` | 先实现抽象接口和模拟回测，这是所有上层的基础 |
| **P0** | `OrderLifecycleManager` | 状态机是实盘核心，必须优先实现 |
| **P0** | `AccountManager`（简化版） | 回测和模拟盘需要 |
| **P0** | `BacktestHonestyParams` | 回测诚实性参数，确保回测有价值 |
| **P1** | `RiskGate` + `PreTradeRisk` | 风控门控和前置检查 |
| **P1** | `SignalBuffer` + `Converter` | 信号缓冲和订单转换 |
| **P1** | `MonitoringSystem`（简化） | 基本监控和日志 |
| **P1** | `PersistenceManager`（WAL） | 交易日志持久化 |
| **P2** | `PtradeBroker` / `QMTBroker` | 真实券商接口（需要实际账户） |
| **P2** | `MonitoringSystem`（完整） | 五层监控 + 告警通知 |
| **P2** | `TradingDaemon` | 进程守护和自动重启 |
| **P2** | `PaperBroker` | 模拟盘模式 |

---

## 十一、相关文档交叉引用

| 文档 | 关系 | 引用章节 |
|------|------|----------|
| `BACKTEST_FRAMEWORK_DESIGN_v1.0.md` | 回测引擎设计 | 执行层接口、Pipeline 设计 |
| `RISK_ARCHITECTURE_P0_R_v1.0.md` | 风控架构 | Van Tharp / Kelly / VolTarget 参数 |
| `MING_CABINET_HYBRID_ARCHITECTURE_v1.0.md` | 治理架构 | 模式切换、审计日志 |
| `EXTERNAL_STRATEGY_RAW_MATERIAL_v4.0.md` | 参考资料 | 券商 API、滑点、延迟 |
| `MASTER_PROGRAMMING_INSTRUCTION_v1.0.md` | 编程规范 | 接口命名、polars 优先、pytest |
| `OBJECT_CARD_*.md` | 信号源 | 对象卡输出格式 |
| `VOTE_DECISION_TABLE_P0_E_v1.0.md` | 投票机制 | 信号进入执行层的前置条件 |

---

> 文件：LIVE_TRADING_SYSTEM_DESIGN_v1.0.md
> 生产者：Kimi（基于第五批搜索资料 + 现有系统架构整合）
> 用途：实盘交易系统的完整设计规格书，可直接给编程 AI 实现
> 状态：✅ 可编码 | 优先级：P0
