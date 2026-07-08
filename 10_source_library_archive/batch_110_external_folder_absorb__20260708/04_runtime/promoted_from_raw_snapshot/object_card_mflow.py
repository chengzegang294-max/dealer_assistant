# MFLOW_P0_A — 资金流向因子（Money Flow）对象卡 Python 实现
# 文件名: object_card_mflow.py
# 状态: proxy_quantizable_now（需 Wind 资金流向数据，A 股已普及）
# A 股落地: 直接可用（支持真实数据 + OHLCV 模拟降级）

"""
资金流向因子对象卡实现

功能层: P0_A（选股层 / 过滤器）
来源: 华泰证券《多因子系列 7：单因子测试之资金流向因子》
SBKT_F014 固化结论: 50 个因子 → 收缩为 2 个核心因子

标准输出字段:
    object_id, signal_type, signal_strength, confidence,
    lock_status, filter_action, risk_action, size_scalar
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any


# ---------------------------------------------------------------------------
# 枚举定义
# ---------------------------------------------------------------------------

class MFlowSignal(Enum):
    NONE = "NONE"
    MAIN_FORCE_OUT = "MAIN_FORCE_OUT"
    MAIN_FORCE_IN = "MAIN_FORCE_IN"
    OPEN_RUSH_BUY = "OPEN_RUSH_BUY"
    OPEN_DUMP_SELL = "OPEN_DUMP_SELL"
    DIVERGENCE_WARN = "DIVERGENCE_WARN"


class FilterAction(Enum):
    PASS = "PASS"
    ENHANCE = "ENHANCE"
    DOWNGRADE = "DOWNGRADE"
    BLOCK = "BLOCK"
    REVERSE = "REVERSE"


class RiskAction(Enum):
    NONE = "NONE"
    HALT_DAY_TRADE = "HALT_DAY_TRADE"
    REDUCE_POSITION = "REDUCE_POSITION"


class LockStatus(Enum):
    UNLOCKED = "UNLOCKED"
    LOCKED = "LOCKED"


# ---------------------------------------------------------------------------
# 数据类
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MFlowRealInput:
    """真实资金流向数据（Wind / 同花顺 Level-1）"""
    mfd_sellord: Optional[float] = None          # 主力流出单数
    mfd_buyord: Optional[float] = None           # 主力流入单数
    mfd_volinflowrate_open_m: Optional[float] = None  # 开盘主力净流入率
    total_volume: Optional[int] = None           # 当日总成交量
    large_sell_amount: Optional[float] = None    # 大单卖出金额（>100万）
    large_buy_amount: Optional[float] = None     # 大单买入金额（>100万）
    total_amount: Optional[float] = None         # 当日总成交额


@dataclass(frozen=True)
class MFlowSimulatedInput:
    """OHLCV 模拟输入（无真实资金流向数据时使用）"""
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
    prev_close: Optional[float] = None           # 昨收（用于判断早盘意图）
    volume_5d_avg: Optional[float] = None        # 5日平均成交量
    close_20d: Optional[List[float]] = None      # 近20日收盘价（用于背离判断）


@dataclass(frozen=True)
class MFlowInternal:
    """MFLOW 内部计算结果"""
    sellord_ratio: float          # 主力流出单数占比
    inflow_ratio: float           # 净流入占比
    open_intent: str              # 早盘意图
    divergence_score: float       # 背离评分 0.0-1.0
    net_inflow: float             # 净流入金额
    data_mode: str                # 'real' 或 'simulated'


@dataclass(frozen=True)
class ObjectCardOutput:
    """对象卡统一输出接口（所有对象卡必须实现）"""
    object_id: str
    signal_type: str
    signal_strength: int          # -2 ~ +2
    confidence: float             # 0.0 ~ 1.0
    lock_status: str
    filter_action: str
    risk_action: str
    size_scalar: float            # 0.0 ~ 2.0
    internal: Dict[str, Any] = field(default_factory=dict)
    notes: str = ""


# ---------------------------------------------------------------------------
# 核心计算类
# ---------------------------------------------------------------------------

class MoneyFlowFactor:
    """
    资金流向因子对象卡实现

    使用示例（真实数据）:
        >>> mflow = MoneyFlowFactor()
        >>> real = MFlowRealInput(mfd_sellord=300, mfd_buyord=700, ...)
        >>> result = mflow.calculate(real_data=real)

    使用示例（OHLCV 模拟）:
        >>> sim = MFlowSimulatedInput(open=10.0, high=10.5, low=9.8, close=10.2, volume=50000)
        >>> result = mflow.calculate(simulated_data=sim)
    """

    OBJECT_ID = "MFLOW_P0_A"
    SELLORD_OUT_THRESHOLD = 0.60   # 主力流出占比阈值
    SELLORD_IN_THRESHOLD = 0.30    # 主力吸筹占比阈值
    INFLOW_RATIO_THRESHOLD = 0.05  # 净流入率显著阈值
    OPEN_STRONG_BUY = 0.10         # 早盘抢筹阈值
    OPEN_MODERATE_BUY = 0.05
    OPEN_MODERATE_SELL = -0.05
    OPEN_STRONG_SELL = -0.10
    DIVERGENCE_THRESHOLD = 0.70    # 背离警告阈值

    def __init__(self):
        self._last_signals: List[str] = []  # 用于锁定状态判断
        self._TREND_LOOKBACK = 3

    # ------------------------------------------------------------------
    # 主入口
    # ------------------------------------------------------------------

    def calculate(
        self,
        real_data: Optional[MFlowRealInput] = None,
        simulated_data: Optional[MFlowSimulatedInput] = None,
        kd_signal: Optional[str] = None,
        price_action: Optional[Dict[str, Any]] = None,
    ) -> ObjectCardOutput:
        """
        计算资金流向因子并输出标准对象卡格式

        Args:
            real_data: 真实资金流向数据（优先使用）
            simulated_data: OHLCV 模拟数据（无真实数据时使用）
            kd_signal: 可选 KD MTF 当前信号（如 'PERFECT_LONG'）
            price_action: 可选价格行为（如 {'is_breakout': True}）

        Returns:
            ObjectCardOutput: 统一输出格式
        """
        if real_data is not None and self._has_real_data(real_data):
            internal = self._compute_from_real(real_data)
            confidence = 1.0
        elif simulated_data is not None:
            internal = self._compute_from_simulated(simulated_data)
            confidence = 0.6  # 模拟数据置信度降级
        else:
            # 无任何数据 → 返回空信号
            return ObjectCardOutput(
                object_id=self.OBJECT_ID,
                signal_type=MFlowSignal.NONE.value,
                signal_strength=0,
                confidence=0.0,
                lock_status=LockStatus.UNLOCKED.value,
                filter_action=FilterAction.PASS.value,
                risk_action=RiskAction.NONE.value,
                size_scalar=1.0,
                internal={"data_mode": "none", "error": "no data provided"},
                notes="未提供任何输入数据，信号不可用",
            )

        # 更新历史信号（用于锁定判断）
        # 基于 open_intent 判断锁定
        self._last_signals.append(internal.open_intent)
        if len(self._last_signals) > self._TREND_LOOKBACK:
            self._last_signals.pop(0)

        # 信号生成
        signal_type, signal_strength, filter_action = self._generate_signal(
            internal, kd_signal, price_action
        )

        # 锁定状态
        lock_status = self._compute_lock_status(internal)

        # 风险动作
        risk_action = self._compute_risk_action(internal, signal_type)

        # 仓位缩放
        size_scalar = self._compute_size_scalar(internal, signal_type)

        return ObjectCardOutput(
            object_id=self.OBJECT_ID,
            signal_type=signal_type.value if isinstance(signal_type, Enum) else signal_type,
            signal_strength=signal_strength,
            confidence=confidence,
            lock_status=lock_status.value,
            filter_action=filter_action.value if isinstance(filter_action, Enum) else filter_action,
            risk_action=risk_action.value if isinstance(risk_action, Enum) else risk_action,
            size_scalar=size_scalar,
            internal={
                "sellord_ratio": round(internal.sellord_ratio, 4),
                "inflow_ratio": round(internal.inflow_ratio, 4),
                "open_intent": internal.open_intent,
                "divergence_score": round(internal.divergence_score, 4),
                "net_inflow": round(internal.net_inflow, 2),
                "data_mode": internal.data_mode,
            },
            notes=self._generate_notes(internal, confidence),
        )

    # ------------------------------------------------------------------
    # 内部计算方法
    # ------------------------------------------------------------------

    def _has_real_data(self, real: MFlowRealInput) -> bool:
        """检查是否具备足够真实数据进行计算"""
        return (
            real.mfd_sellord is not None
            and real.mfd_buyord is not None
            and real.total_amount is not None
            and real.total_amount > 0
        )

    def _compute_from_real(self, real: MFlowRealInput) -> MFlowInternal:
        """基于真实资金流向数据计算"""
        # 1. 主力流出单数占比
        total_ord = real.mfd_sellord + real.mfd_buyord
        sellord_ratio = real.mfd_sellord / total_ord if total_ord > 0 else 0.5

        # 2. 净流入与净流入率
        net_inflow = (real.large_buy_amount or 0.0) - (real.large_sell_amount or 0.0)
        inflow_ratio = net_inflow / real.total_amount if real.total_amount > 0 else 0.0

        # 3. 早盘意图
        open_rate = real.mfd_volinflowrate_open_m or 0.0
        open_intent = self._classify_open_intent(open_rate)

        # 4. 背离评分（简化：仅基于净流入率符号）
        divergence_score = 0.0

        return MFlowInternal(
            sellord_ratio=sellord_ratio,
            inflow_ratio=inflow_ratio,
            open_intent=open_intent,
            divergence_score=divergence_score,
            net_inflow=net_inflow,
            data_mode="real",
        )

    def _compute_from_simulated(self, sim: MFlowSimulatedInput) -> MFlowInternal:
        """
        基于 OHLCV 模拟主力行为

        核心假设：
        - 放量上涨且 K 线实体大 → 主力流入
        - 放量下跌且 K 线实体大 → 主力流出
        - 缩量回调（小阴线 / 十字星） → 主力吸筹（洗盘）
        - 放量滞涨（大成交量但小实体） → 主力派发
        """
        # 价格变化率
        price_change = (sim.close_price - sim.open_price) / sim.open_price if sim.open_price != 0 else 0.0
        body_ratio = abs(sim.close_price - sim.open_price) / (sim.high_price - sim.low_price) if (sim.high_price - sim.low_price) > 0 else 0.0

        # 成交量相对 5 日均量的比率
        vol_ratio = sim.volume / sim.volume_5d_avg if sim.volume_5d_avg and sim.volume_5d_avg > 0 else 1.0

        # 模拟主力流出单数占比
        # 放量下跌 → sellord_ratio 高；缩量上涨 → sellord_ratio 低
        if price_change < -0.02 and vol_ratio > 1.3:
            sellord_ratio = 0.65  # 主力出逃
        elif price_change > 0.02 and vol_ratio > 1.3:
            sellord_ratio = 0.30  # 主力拉抬（买入单主导）
        elif abs(price_change) < 0.005 and vol_ratio > 1.5:
            sellord_ratio = 0.55  # 放量滞涨，疑似对倒/派发
        elif price_change < 0 and vol_ratio < 0.7:
            sellord_ratio = 0.40  # 缩量回调，主力未出逃
        else:
            sellord_ratio = 0.50  # 中性

        # 模拟净流入率
        if price_change > 0.02 and vol_ratio > 1.2:
            inflow_ratio = 0.08
        elif price_change < -0.02 and vol_ratio > 1.2:
            inflow_ratio = -0.08
        elif abs(price_change) < 0.005 and vol_ratio > 1.5:
            inflow_ratio = -0.03  # 放量滞涨，净流出
        elif price_change < 0 and vol_ratio < 0.7:
            inflow_ratio = 0.02   # 缩量回调，资金未流出
        else:
            inflow_ratio = 0.0

        # 模拟早盘意图（基于昨收跳空）
        open_intent = "NEUTRAL"
        if sim.prev_close and sim.prev_close > 0:
            gap = (sim.open_price - sim.prev_close) / sim.prev_close
            open_intent = self._classify_open_intent(gap)

        # 背离评分（价格 vs 模拟资金流向）
        divergence_score = 0.0
        if sim.close_20d and len(sim.close_20d) >= 2:
            price_high = max(sim.close_20d)
            price_low = min(sim.close_20d)
            if sim.close_price >= price_high * 0.99 and inflow_ratio < 0:
                divergence_score = min(1.0, abs(inflow_ratio) * 10 + 0.3)
            elif sim.close_price <= price_low * 1.01 and inflow_ratio > 0:
                divergence_score = min(1.0, inflow_ratio * 10 + 0.3)

        return MFlowInternal(
            sellord_ratio=sellord_ratio,
            inflow_ratio=inflow_ratio,
            open_intent=open_intent,
            divergence_score=divergence_score,
            net_inflow=inflow_ratio * sim.volume * sim.close_price,  # 近似
            data_mode="simulated",
        )

    def _classify_open_intent(self, open_rate: float) -> str:
        """分类早盘意图"""
        if open_rate > self.OPEN_STRONG_BUY:
            return "STRONG_BUY"
        elif open_rate > self.OPEN_MODERATE_BUY:
            return "MODERATE_BUY"
        elif open_rate > self.OPEN_MODERATE_SELL:
            return "NEUTRAL"
        elif open_rate > self.OPEN_STRONG_SELL:
            return "MODERATE_SELL"
        else:
            return "STRONG_SELL"

    def _generate_signal(
        self,
        internal: MFlowInternal,
        kd_signal: Optional[str],
        price_action: Optional[Dict[str, Any]],
    ) -> tuple[MFlowSignal, int, FilterAction]:
        """
        生成资金流向信号

        返回: (signal_type, signal_strength, filter_action)
        """
        sellord_ratio = internal.sellord_ratio
        inflow_ratio = internal.inflow_ratio
        divergence = internal.divergence_score
        is_breakout = price_action.get("is_breakout", False) if price_action else False

        # 1. 主力大幅出逃（危险信号）→ BLOCK
        if sellord_ratio > self.SELLORD_OUT_THRESHOLD and inflow_ratio < -self.INFLOW_RATIO_THRESHOLD:
            return MFlowSignal.MAIN_FORCE_OUT, -2, FilterAction.BLOCK

        # 2. 主力吸筹（增强信号）→ ENHANCE
        if sellord_ratio < self.SELLORD_IN_THRESHOLD and inflow_ratio > self.INFLOW_RATIO_THRESHOLD:
            return MFlowSignal.MAIN_FORCE_IN, +2, FilterAction.ENHANCE

        # 3. 早盘抢筹 + 价格突破 → ENHANCE
        if internal.open_intent == "STRONG_BUY" and is_breakout:
            return MFlowSignal.OPEN_RUSH_BUY, +1, FilterAction.ENHANCE

        # 4. 早盘抛售 → DOWNGRADE
        if internal.open_intent == "STRONG_SELL":
            return MFlowSignal.OPEN_DUMP_SELL, -1, FilterAction.DOWNGRADE

        # 5. 背离警告
        if divergence > self.DIVERGENCE_THRESHOLD:
            if kd_signal and "LONG" in kd_signal and inflow_ratio < 0:
                return MFlowSignal.DIVERGENCE_WARN, -1, FilterAction.DOWNGRADE

        return MFlowSignal.NONE, 0, FilterAction.PASS

    def _compute_lock_status(self, internal: MFlowInternal) -> LockStatus:
        """连续 3 期同向早盘意图则锁定"""
        if len(self._last_signals) < self._TREND_LOOKBACK:
            return LockStatus.UNLOCKED
        last3 = self._last_signals[-self._TREND_LOOKBACK:]
        # 全是 STRONG_BUY 或全是 STRONG_SELL
        if all(s == "STRONG_BUY" for s in last3):
            return LockStatus.LOCKED
        if all(s == "STRONG_SELL" for s in last3):
            return LockStatus.LOCKED
        return LockStatus.UNLOCKED

    def _compute_risk_action(self, internal: MFlowInternal, signal_type: MFlowSignal) -> RiskAction:
        """风险动作判断"""
        if signal_type == MFlowSignal.MAIN_FORCE_OUT:
            return RiskAction.REDUCE_POSITION
        if signal_type == MFlowSignal.OPEN_DUMP_SELL:
            return RiskAction.HALT_DAY_TRADE
        return RiskAction.NONE

    def _compute_size_scalar(self, internal: MFlowInternal, signal_type: MFlowSignal) -> float:
        """仓位缩放"""
        if signal_type == MFlowSignal.MAIN_FORCE_IN:
            return 1.3
        elif signal_type == MFlowSignal.OPEN_RUSH_BUY:
            return 1.2
        elif signal_type == MFlowSignal.MAIN_FORCE_OUT:
            return 0.0  # 纯多头下阻断
        elif signal_type == MFlowSignal.DIVERGENCE_WARN:
            return 0.5
        elif signal_type == MFlowSignal.OPEN_DUMP_SELL:
            return 0.3
        return 1.0

    def _generate_notes(self, internal: MFlowInternal, confidence: float) -> str:
        parts = []
        if internal.data_mode == "simulated":
            parts.append("使用 OHLCV 模拟资金流向，置信度降级")
        if confidence < 1.0:
            parts.append(f"数据完整度{confidence:.0%}")
        if internal.open_intent in ("STRONG_BUY", "STRONG_SELL"):
            parts.append(f"早盘意图: {internal.open_intent}")
        if internal.divergence_score > 0.5:
            parts.append(f"资金流向背离评分: {internal.divergence_score:.2f}")
        return "; ".join(parts) if parts else ""


# ---------------------------------------------------------------------------
# 快速测试
# ---------------------------------------------------------------------------

def _quick_test():
    """内部快速验证 — 至少覆盖 3 个场景"""
    mflow = MoneyFlowFactor()

    print("=" * 60)
    print("MFLOW_P0_A 对象卡测试输出")
    print("=" * 60)

    # --- 场景 1: 真实数据 - 主力大幅流入 ---
    print("\n【场景 1】真实数据 - 主力吸筹（买入增强）")
    real_in = MFlowRealInput(
        mfd_sellord=200,
        mfd_buyord=800,
        mfd_volinflowrate_open_m=0.12,
        total_volume=100000,
        large_sell_amount=5000000,
        large_buy_amount=15000000,
        total_amount=20000000,
    )
    r1 = mflow.calculate(real_data=real_in, kd_signal="PERFECT_LONG")
    _print_result(r1)

    # --- 场景 2: 真实数据 - 主力大幅流出 ---
    print("\n【场景 2】真实数据 - 主力出逃（阻断买入）")
    real_out = MFlowRealInput(
        mfd_sellord=750,
        mfd_buyord=250,
        mfd_volinflowrate_open_m=-0.08,
        total_volume=200000,
        large_sell_amount=20000000,
        large_buy_amount=5000000,
        total_amount=25000000,
    )
    r2 = mflow.calculate(real_data=real_out, kd_signal="PERFECT_LONG")
    _print_result(r2)

    # --- 场景 3: OHLCV 模拟 - 放量上涨突破 ---
    print("\n【场景 3】OHLCV 模拟 - 放量突破（主力流入模拟）")
    sim_breakout = MFlowSimulatedInput(
        open_price=10.0,
        high_price=10.8,
        low_price=9.9,
        close_price=10.6,
        volume=150000,
        prev_close=9.8,
        volume_5d_avg=80000,
        close_20d=[9.5, 9.6, 9.7, 9.8, 9.9, 10.0, 10.1, 10.2, 10.3, 10.4],
    )
    r3 = mflow.calculate(simulated_data=sim_breakout, kd_signal="PERFECT_LONG",
                         price_action={"is_breakout": True})
    _print_result(r3)

    # --- 场景 4: OHLCV 模拟 - 放量滞涨（派发） ---
    print("\n【场景 4】OHLCV 模拟 - 放量滞涨（派发模拟）")
    sim_dist = MFlowSimulatedInput(
        open_price=10.0,
        high_price=10.15,
        low_price=9.95,
        close_price=10.02,
        volume=200000,
        prev_close=10.0,
        volume_5d_avg=90000,
        close_20d=[9.0 + i * 0.05 for i in range(20)],
    )
    r4 = mflow.calculate(simulated_data=sim_dist)
    _print_result(r4)

    # --- 场景 5: 数据缺失 ---
    print("\n【场景 5】无任何输入数据")
    r5 = mflow.calculate()
    _print_result(r5)


def _print_result(result: ObjectCardOutput) -> None:
    for k, v in result.__dict__.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    _quick_test()
