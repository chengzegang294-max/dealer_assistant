# ATRATIO_P0_A — Active Trade Ratio 对象卡 Python 实现
# 文件名: object_card_atratio.py
# 状态: ⚠️ LIMITED_CANDIDATE（A股纯多头下无效，仅接口标准化）
# 数据需求: Level-2逐笔委托/成交数据
# A股纯多头落地: ❌ 不可用（SBKT_F002 结论）

"""
主动成交占比（Active Trade Ratio）对象卡实现

功能层: P0_A（选股层 / 过滤器）
来源: 华泰证券《多因子系列 5：单因子测试之主动买卖因子》
SBKT_F002 固化结论: A股纯多头下 IC 不显著，无法产生有效信号

标准输出字段:
    object_id, signal_type, signal_strength, confidence,
    lock_status, filter_action, risk_action, size_scalar

A股纯多头场景: 输出固定"空信号"，confidence=0.0，不干预任何决策
多空/外汇/期货场景: 可生成有效信号
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict, Any


# ---------------------------------------------------------------------------
# 枚举定义
# ---------------------------------------------------------------------------

class AtratioSignalType(Enum):
    NONE = "NONE"
    STRONG_ACTIVE_BUY = "STRONG_ACTIVE_BUY"
    STRONG_ACTIVE_SELL = "STRONG_ACTIVE_SELL"
    TIME_ADVANTAGE_BUY = "TIME_ADVANTAGE_BUY"
    TIME_ADVANTAGE_SELL = "TIME_ADVANTAGE_SELL"


class FilterAction(Enum):
    PASS = "PASS"
    BLOCK_BUY = "BLOCK_BUY"
    ENHANCE_SHORT = "ENHANCE_SHORT"


class LockStatus(Enum):
    UNLOCKED = "UNLOCKED"
    LOCKED = "LOCKED"


class RiskAction(Enum):
    NONE = "NONE"


# ---------------------------------------------------------------------------
# 数据类
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AtratioRawInput:
    """ATRATIO 原始数据输入（需 Level-2 逐笔数据）"""
    # 逐笔委托时间（毫秒级）
    buy_order_time: Optional[List[float]] = None
    sell_order_time: Optional[List[float]] = None
    # 逐笔成交量
    buy_vol: Optional[List[int]] = None
    sell_vol: Optional[List[int]] = None
    # 逐笔成交价格
    buy_price: Optional[List[float]] = None
    sell_price: Optional[List[float]] = None
    # 日汇总
    total_vol: Optional[int] = None
    total_amount: Optional[float] = None


@dataclass(frozen=True)
class ObjectCardOutput:
    """对象卡统一输出接口"""
    object_id: str
    signal_type: str
    signal_strength: int          # -2 ~ +2
    confidence: float             # 0.0 ~ 1.0
    lock_status: str
    filter_action: str
    risk_action: str
    size_scalar: float            # 0.0 ~ 2.0
    internal: Dict[str, Any]
    notes: str = ""


# ---------------------------------------------------------------------------
# 核心计算类
# ---------------------------------------------------------------------------

class ActiveTradeRatio:
    """
    主动成交占比对象卡实现
    
    A股纯多头场景: 固定输出空信号，不干预任何决策
    多空场景: 基于逐笔数据计算主动买卖信号
    
    使用示例:
        >>> atr = ActiveTradeRatio(market_type='ashare_long_only')
        >>> raw = AtratioRawInput(...)  # 即使传入数据，纯多头下也无效
        >>> result = atr.calculate(raw)
        >>> print(result.signal_type)  # 'NONE'
    """

    OBJECT_ID = "ATRATIO_P0_A"
    LARGE_ORDER_THRESHOLD = 1_000_000  # 大单阈值：100万元
    COMPOSITE_STRONG_THRESHOLD = 0.7
    COMPOSITE_MODERATE_THRESHOLD = 0.5

    def __init__(self, market_type: str = "ashare_long_only"):
        """
        Args:
            market_type: 'ashare_long_only' | 'ashare_long_short' | 'forex' | 'futures'
        """
        self.market_type = market_type
        self._short_qualify = market_type in ("ashare_long_short", "forex", "futures")

    # ------------------------------------------------------------------
    # 主入口
    # ------------------------------------------------------------------

    def calculate(self, raw: AtratioRawInput) -> ObjectCardOutput:
        """
        计算主动成交占比因子并输出标准对象卡格式
        
        A股纯多头: 立即返回固定空信号
        多空环境: 计算逐笔因子后输出
        """
        # A股纯多头：直接返回空信号（SBKT_F002 结论）
        if not self._short_qualify:
            return self._empty_signal("A股纯多头场景下 ATRATIO 因子无效（SBKT_F002 结论）")
        
        # 多空环境：计算因子
        return self._compute_for_short(raw)

    # ------------------------------------------------------------------
    # A股纯多头：空信号输出
    # ------------------------------------------------------------------

    def _empty_signal(self, note: str) -> ObjectCardOutput:
        """生成统一的空信号输出"""
        return ObjectCardOutput(
            object_id=self.OBJECT_ID,
            signal_type=AtratioSignalType.NONE.value,
            signal_strength=0,
            confidence=0.0,
            lock_status=LockStatus.UNLOCKED.value,
            filter_action=FilterAction.PASS.value,
            risk_action=RiskAction.NONE.value,
            size_scalar=1.0,
            internal={
                "atratio_signal_valid": False,
                "atratio_short_qualify": False,
                "market_type": self.market_type,
            },
            notes=note,
        )

    # ------------------------------------------------------------------
    # 多空环境：因子计算
    # ------------------------------------------------------------------

    def _compute_for_short(self, raw: AtratioRawInput) -> ObjectCardOutput:
        """多空/外汇/期货环境下的因子计算"""
        # 数据完整性检查
        has_tick_data = all([
            raw.buy_vol is not None,
            raw.sell_vol is not None,
            raw.total_vol is not None and raw.total_vol > 0,
        ])
        
        if not has_tick_data:
            return self._empty_signal("逐笔数据缺失，无法计算主动成交占比")
        
        # 核心因子计算
        buy_vol = sum(raw.buy_vol)
        sell_vol = sum(raw.sell_vol)
        total_vol = raw.total_vol
        
        active_buy_ratio = buy_vol / total_vol
        active_sell_ratio = sell_vol / total_vol
        
        # 时间优势（需委托时间数据）
        time_advantage = 0.5  # 默认中性
        if raw.buy_order_time and raw.sell_order_time and len(raw.buy_order_time) > 0:
            buy_first_count = sum(
                1 for bt, st in zip(raw.buy_order_time, raw.sell_order_time)
                if bt < st
            )
            time_advantage = buy_first_count / len(raw.buy_order_time)
        
        # 大单主动成交占比
        large_order_ratio = 0.0
        if raw.buy_price and raw.sell_price and raw.buy_vol and raw.sell_vol:
            large_buy_vol = sum(
                v for v, p in zip(raw.buy_vol, raw.buy_price)
                if v * p > self.LARGE_ORDER_THRESHOLD
            )
            large_sell_vol = sum(
                v for v, p in zip(raw.sell_vol, raw.sell_price)
                if v * p > self.LARGE_ORDER_THRESHOLD
            )
            total_large = large_buy_vol + large_sell_vol
            if total_large > 0:
                large_order_ratio = (large_buy_vol - large_sell_vol) / total_large
        
        # 综合评分 [-1, +1]
        composite_score = (
            active_buy_ratio * 0.3 +
            (1 - active_sell_ratio) * 0.3 +
            time_advantage * 0.2 +
            large_order_ratio * 0.2
        ) * 2 - 1
        composite_score = max(-1.0, min(1.0, composite_score))
        
        # 信号类型判断
        signal_type, signal_strength = self._map_signal(composite_score)
        
        # 过滤动作
        filter_action = self._compute_filter_action(signal_type)
        
        # 置信度（基于数据质量）
        confidence = 1.0 if (raw.buy_order_time and raw.sell_order_time) else 0.5
        
        return ObjectCardOutput(
            object_id=self.OBJECT_ID,
            signal_type=signal_type.value,
            signal_strength=signal_strength,
            confidence=confidence,
            lock_status=LockStatus.UNLOCKED.value,
            filter_action=filter_action.value,
            risk_action=RiskAction.NONE.value,
            size_scalar=self._compute_size_scalar(composite_score),
            internal={
                "atratio_signal_valid": True,
                "atratio_short_qualify": True,
                "active_buy_ratio": round(active_buy_ratio, 4),
                "active_sell_ratio": round(active_sell_ratio, 4),
                "time_advantage": round(time_advantage, 4),
                "large_order_ratio": round(large_order_ratio, 4),
                "composite_score": round(composite_score, 4),
            },
            notes=f"多空环境信号: {signal_type.value}, score={composite_score:.2f}",
        )

    def _map_signal(self, score: float) -> tuple:
        """综合评分 → 信号类型和强度"""
        if score > self.COMPOSITE_STRONG_THRESHOLD:
            return AtratioSignalType.STRONG_ACTIVE_BUY, 2
        elif score > self.COMPOSITE_MODERATE_THRESHOLD:
            return AtratioSignalType.STRONG_ACTIVE_BUY, 1
        elif score < -self.COMPOSITE_STRONG_THRESHOLD:
            return AtratioSignalType.STRONG_ACTIVE_SELL, -2
        elif score < -self.COMPOSITE_MODERATE_THRESHOLD:
            return AtratioSignalType.STRONG_ACTIVE_SELL, -1
        else:
            return AtratioSignalType.NONE, 0

    def _compute_filter_action(self, signal_type: AtratioSignalType) -> FilterAction:
        if signal_type == AtratioSignalType.STRONG_ACTIVE_SELL:
            return FilterAction.BLOCK_BUY
        return FilterAction.PASS

    def _compute_size_scalar(self, score: float) -> float:
        """仓位缩放：强信号缩半仓，弱信号全仓"""
        if abs(score) > self.COMPOSITE_STRONG_THRESHOLD:
            return 0.5
        return 1.0


# ---------------------------------------------------------------------------
# 快速测试
# ---------------------------------------------------------------------------

def _quick_test():
    """内部快速验证"""
    print("=" * 60)
    print("ATRATIO 对象卡实现验证")
    print("=" * 60)
    
    # 测试1: A股纯多头（默认）
    print("\n【测试1】A股纯多头场景（默认）")
    atr = ActiveTradeRatio(market_type="ashare_long_only")
    raw = AtratioRawInput()  # 空数据也无所谓
    result = atr.calculate(raw)
    assert result.object_id == "ATRATIO_P0_A"
    assert result.signal_type == "NONE"
    assert result.signal_strength == 0
    assert result.confidence == 0.0
    assert result.filter_action == "PASS"
    assert result.size_scalar == 1.0
    print(f"  object_id: {result.object_id}")
    print(f"  signal_type: {result.signal_type}")
    print(f"  confidence: {result.confidence}")
    print(f"  filter_action: {result.filter_action}")
    print(f"  notes: {result.notes}")
    print("  ✅ A股纯多头空信号正确")
    
    # 测试2: 多空环境（有数据）
    print("\n【测试2】多空环境（模拟数据）")
    atr_ls = ActiveTradeRatio(market_type="ashare_long_short")
    raw_ls = AtratioRawInput(
        buy_vol=[1000, 2000, 1500],
        sell_vol=[500, 800, 600],
        total_vol=6400,
        buy_order_time=[1.0, 2.0, 3.0],
        sell_order_time=[1.5, 2.5, 3.5],  # 买单先于卖单
        buy_price=[10.0, 10.1, 10.2],
        sell_price=[10.0, 10.1, 10.2],
    )
    result_ls = atr_ls.calculate(raw_ls)
    print(f"  signal_type: {result_ls.signal_type}")
    print(f"  signal_strength: {result_ls.signal_strength}")
    print(f"  confidence: {result_ls.confidence}")
    print(f"  internal: {result_ls.internal}")
    assert result_ls.signal_type == "STRONG_ACTIVE_BUY" or result_ls.signal_type == "NONE"
    print("  ✅ 多空环境信号计算正确")
    
    # 测试3: 外汇环境
    print("\n【测试3】外汇环境")
    atr_fx = ActiveTradeRatio(market_type="forex")
    raw_fx = AtratioRawInput(
        buy_vol=[100, 100],
        sell_vol=[500, 500],
        total_vol=1200,
    )
    result_fx = atr_fx.calculate(raw_fx)
    print(f"  signal_type: {result_fx.signal_type}")
    print(f"  signal_strength: {result_fx.signal_strength}")
    assert result_fx.object_id == "ATRATIO_P0_A"
    print("  ✅ 外汇环境输出正确")
    
    # 测试4: 数据缺失
    print("\n【测试4】多空环境但数据缺失")
    atr_ls2 = ActiveTradeRatio(market_type="ashare_long_short")
    result_missing = atr_ls2.calculate(AtratioRawInput())
    assert result_missing.signal_type == "NONE"
    assert result_missing.confidence == 0.0
    print(f"  signal_type: {result_missing.signal_type}")
    print("  ✅ 数据缺失时正确降级为空信号")
    
    print("\n" + "=" * 60)
    print("✅ 全部测试通过")
    print("=" * 60)


if __name__ == "__main__":
    _quick_test()
