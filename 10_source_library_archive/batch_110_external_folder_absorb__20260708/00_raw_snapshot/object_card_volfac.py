# VOLFAC_P0_A — Volatility Factor 对象卡 Python 实现
# 文件名: object_card_volfac.py
# 状态: ✅ 可编码完成（proxy_quantizable_now）
# 数据需求: 日收盘价（60日）+ 可选5分钟数据
# A股落地: 直接可用

"""
波动率因子（Volatility Factor）对象卡实现

功能层: P0_A（选股层 / 过滤器）
来源: 华泰证券《多因子系列 6：单因子测试之波动率类因子》
SBKT_F006 固化结论: 8个波动率因子 → 收缩为 id2_std_3m + hml_r_std_5m

标准输出字段:
    object_id, signal_type, signal_strength, confidence,
    lock_status, filter_action, risk_action, size_scalar
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, List, Dict, Any


# ---------------------------------------------------------------------------
# 枚举定义
# ---------------------------------------------------------------------------

class VolRegime(Enum):
    LOW_VOL = "LOW_VOL"
    NORMAL_VOL = "NORMAL_VOL"
    HIGH_VOL = "HIGH_VOL"
    EXTREME_VOL = "EXTREME_VOL"


class VolTrend(Enum):
    EXPANDING = "EXPANDING"
    CONTRACTING = "CONTRACTING"
    STABLE = "STABLE"


class FilterAction(Enum):
    PASS = "PASS"
    REDUCE_WEIGHT = "REDUCE_WEIGHT"
    EXCLUDE = "EXCLUDE"
    INCREASE_WEIGHT = "INCREASE_WEIGHT"


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
class VolFacRawInput:
    """VOLFAC 原始数据输入"""
    close_60d: List[float]           # 最近60日收盘价（必需）
    close_5m: Optional[List[float]] = None   # 可选：5分钟收盘价
    high_5m: Optional[List[float]] = None    # 可选：5分钟最高价
    low_5m: Optional[List[float]] = None     # 可选：5分钟最低价
    historical_vol_1y: Optional[List[float]] = None  # 过去1年的id2_std_3m滚动值（用于分位）


@dataclass(frozen=True)
class VolFacInternal:
    """VOLFAC 内部计算结果"""
    id2_std_3m: float
    annualized_vol: float
    vol_percentile: float
    vol_regime: VolRegime
    vol_trend: VolTrend
    hml_r_std_5m: Optional[float]
    r8_qualify: bool


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
    # 扩展字段（各对象卡特有）
    internal: Dict[str, Any] = field(default_factory=dict)
    notes: str = ""


# ---------------------------------------------------------------------------
# 核心计算类
# ---------------------------------------------------------------------------

class VolatilityFactor:
    """
    波动率因子对象卡实现
    
    使用示例:
        >>> vf = VolatilityFactor()
        >>> raw = VolFacRawInput(close_60d=[...], historical_vol_1y=[...])
        >>> result = vf.calculate(raw, strategy_type='swing')
        >>> print(result.filter_action, result.size_scalar)
    """

    OBJECT_ID = "VOLFAC_P0_A"
    MIN_DAYS_FOR_RELIABLE = 40    # 最少40日数据才可靠
    TOTAL_DAYS_FOR_STD = 60       # 计算标准差所需日数
    HML_5M_THRESHOLD = 0.05       # 5分钟波动率阈值（暂停日内）
    PERCENTILE_LOW = 20.0
    PERCENTILE_HIGH = 80.0
    PERCENTILE_EXTREME = 95.0
    TREND_SLOPE_THRESHOLD = 0.001
    TREND_LOOKBACK = 5            # 趋势判断回看期数

    def __init__(self):
        self._last_regimes: List[VolRegime] = []  # 用于锁定状态判断

    # ------------------------------------------------------------------
    # 主入口
    # ------------------------------------------------------------------

    def calculate(
        self,
        raw: VolFacRawInput,
        strategy_type: str = "swing",
        market_cap: Optional[float] = None,  # 市值（亿），用于分层
    ) -> ObjectCardOutput:
        """
        计算波动率因子并输出标准对象卡格式
        
        Args:
            raw: 原始输入数据
            strategy_type: 'swing' | 'day_trade' | 'trend'
            market_cap: 市值（亿元），用于小盘股特殊处理
        
        Returns:
            ObjectCardOutput: 统一输出格式
        """
        # 1. 数据完整性检查
        confidence = self._compute_confidence(raw)
        
        # 2. 核心因子计算
        internal = self._compute_internal(raw, confidence)
        
        # 3. 更新历史状态（用于锁定判断）
        self._last_regimes.append(internal.vol_regime)
        if len(self._last_regimes) > self.TREND_LOOKBACK:
            self._last_regimes.pop(0)
        
        # 4. 信号强度映射
        signal_strength = self._map_signal_strength(internal)
        
        # 5. 锁定状态
        lock_status = self._compute_lock_status()
        
        # 6. 过滤动作
        filter_action = self._compute_filter_action(internal, strategy_type)
        
        # 7. 风险动作
        risk_action = self._compute_risk_action(internal, strategy_type)
        
        # 8. 仓位缩放（市值分层）
        size_scalar = self._compute_size_scalar(internal, market_cap)
        
        # 9. 组装标准输出
        return ObjectCardOutput(
            object_id=self.OBJECT_ID,
            signal_type="FILTER",
            signal_strength=signal_strength,
            confidence=confidence,
            lock_status=lock_status.value,
            filter_action=filter_action.value,
            risk_action=risk_action.value,
            size_scalar=size_scalar,
            internal={
                "id2_std_3m": round(internal.id2_std_3m, 6),
                "annualized_vol": round(internal.annualized_vol, 4),
                "vol_percentile": round(internal.vol_percentile, 2),
                "vol_regime": internal.vol_regime.value,
                "vol_trend": internal.vol_trend.value,
                "hml_r_std_5m": round(internal.hml_r_std_5m, 6) if internal.hml_r_std_5m else None,
                "r8_qualify": internal.r8_qualify,
            },
            notes=self._generate_notes(internal, confidence),
        )

    # ------------------------------------------------------------------
    # 内部计算方法
    # ------------------------------------------------------------------

    def _compute_confidence(self, raw: VolFacRawInput) -> float:
        """数据完整性 → 置信度"""
        n = len(raw.close_60d)
        if n >= self.TOTAL_DAYS_FOR_STD:
            return 1.0
        elif n >= self.MIN_DAYS_FOR_RELIABLE:
            return 0.7
        elif n >= 20:
            return 0.3
        else:
            return 0.0

    def _compute_internal(self, raw: VolFacRawInput, confidence: float) -> VolFacInternal:
        """计算所有内部因子字段"""
        close = np.array(raw.close_60d, dtype=float)
        
        # 1. id2_std_3m: 对数收益率标准差
        if len(close) >= 2:
            log_returns = np.log(close[1:] / close[:-1])
            id2_std_3m = float(np.std(log_returns, ddof=1))
        else:
            id2_std_3m = 0.0
        
        # 2. 年化波动率
        annualized_vol = id2_std_3m * np.sqrt(252)
        
        # 3. 历史分位
        vol_percentile = self._compute_percentile(id2_std_3m, raw.historical_vol_1y)
        
        # 4. 波动率状态
        vol_regime = self._classify_regime(vol_percentile)
        
        # 5. 波动率趋势
        vol_trend = self._classify_trend(raw.historical_vol_1y)
        
        # 6. 5分钟高频波动率（可选）
        hml_r_std_5m = self._compute_hml_5m(raw)
        
        # 7. R8 日内资格
        r8_qualify = True
        if hml_r_std_5m is not None and hml_r_std_5m > self.HML_5M_THRESHOLD:
            r8_qualify = False
        
        return VolFacInternal(
            id2_std_3m=id2_std_3m,
            annualized_vol=annualized_vol,
            vol_percentile=vol_percentile,
            vol_regime=vol_regime,
            vol_trend=vol_trend,
            hml_r_std_5m=hml_r_std_5m,
            r8_qualify=r8_qualify,
        )

    def _compute_percentile(
        self,
        current_vol: float,
        historical: Optional[List[float]],
    ) -> float:
        """计算当前波动率在过去1年中的分位"""
        if not historical or len(historical) < 60:
            return 50.0  # 数据不足，默认中位
        hist = np.array(historical, dtype=float)
        return float(np.mean(hist < current_vol) * 100)

    def _classify_regime(self, percentile: float) -> VolRegime:
        if percentile >= self.PERCENTILE_EXTREME:
            return VolRegime.EXTREME_VOL
        elif percentile >= self.PERCENTILE_HIGH:
            return VolRegime.HIGH_VOL
        elif percentile <= self.PERCENTILE_LOW:
            return VolRegime.LOW_VOL
        else:
            return VolRegime.NORMAL_VOL

    def _classify_trend(self, historical: Optional[List[float]]) -> VolTrend:
        """基于最近5期波动率值判断趋势"""
        if not historical or len(historical) < self.TREND_LOOKBACK:
            return VolTrend.STABLE
        recent = np.array(historical[-self.TREND_LOOKBACK:], dtype=float)
        if len(recent) < 2:
            return VolTrend.STABLE
        slope = float(np.polyfit(range(len(recent)), recent, 1)[0])
        if slope > self.TREND_SLOPE_THRESHOLD:
            return VolTrend.EXPANDING
        elif slope < -self.TREND_SLOPE_THRESHOLD:
            return VolTrend.CONTRACTING
        else:
            return VolTrend.STABLE

    def _compute_hml_5m(self, raw: VolFacRawInput) -> Optional[float]:
        """计算5分钟已实现波动率（需Level-2数据）"""
        if raw.close_5m is None or len(raw.close_5m) < 2:
            return None
        close_5m = np.array(raw.close_5m, dtype=float)
        log_returns = np.log(close_5m[1:] / close_5m[:-1])
        # 48个5分钟/日 * 252交易日 = 年化系数
        return float(np.std(log_returns, ddof=1) * np.sqrt(48 * 252))

    def _map_signal_strength(self, internal: VolFacInternal) -> int:
        """映射到 -2~+2 信号强度"""
        regime = internal.vol_regime
        trend = internal.vol_trend
        
        if regime == VolRegime.EXTREME_VOL:
            return -2
        elif regime == VolRegime.HIGH_VOL:
            return -1
        elif regime == VolRegime.LOW_VOL:
            if trend == VolTrend.EXPANDING:
                return 0  # 低波动但正在扩大，保持观察
            else:
                return +1  # 低波动稳定/收缩，可增仓
        else:  # NORMAL_VOL
            return 0

    def _compute_lock_status(self) -> LockStatus:
        """连续3期同状态则锁定"""
        if len(self._last_regimes) < 3:
            return LockStatus.UNLOCKED
        last3 = self._last_regimes[-3:]
        if all(r == last3[0] for r in last3):
            return LockStatus.LOCKED
        return LockStatus.UNLOCKED

    def _compute_filter_action(
        self,
        internal: VolFacInternal,
        strategy_type: str,
    ) -> FilterAction:
        """根据策略类型和波动率状态决定过滤动作"""
        regime = internal.vol_regime
        trend = internal.vol_trend
        
        if strategy_type == "swing":
            if regime == VolRegime.EXTREME_VOL:
                return FilterAction.EXCLUDE
            elif regime == VolRegime.HIGH_VOL:
                return FilterAction.REDUCE_WEIGHT
            elif regime == VolRegime.LOW_VOL and trend != VolTrend.EXPANDING:
                return FilterAction.INCREASE_WEIGHT
        
        elif strategy_type == "day_trade":
            if regime == VolRegime.EXTREME_VOL:
                return FilterAction.EXCLUDE
        
        elif strategy_type == "trend":
            if regime == VolRegime.LOW_VOL and trend == VolTrend.STABLE:
                return FilterAction.INCREASE_WEIGHT
            elif regime == VolRegime.HIGH_VOL:
                return FilterAction.REDUCE_WEIGHT
        
        return FilterAction.PASS

    def _compute_risk_action(
        self,
        internal: VolFacInternal,
        strategy_type: str,
    ) -> RiskAction:
        """风险动作判断"""
        if strategy_type == "day_trade" and not internal.r8_qualify:
            return RiskAction.HALT_DAY_TRADE
        if internal.vol_regime == VolRegime.EXTREME_VOL:
            return RiskAction.REDUCE_POSITION
        return RiskAction.NONE

    def _compute_size_scalar(
        self,
        internal: VolFacInternal,
        market_cap: Optional[float],
    ) -> float:
        """
        仓位缩放系数
        小盘股（<50亿）天然波动率高，目标波动率应调高
        """
        regime = internal.vol_regime
        trend = internal.vol_trend
        
        # 基础映射
        if regime == VolRegime.EXTREME_VOL:
            base = 0.2
        elif regime == VolRegime.HIGH_VOL:
            base = 0.5
        elif regime == VolRegime.LOW_VOL:
            if trend == VolTrend.EXPANDING:
                base = 0.8
            else:
                base = 1.2
        else:  # NORMAL
            base = 1.0
        
        # 小盘股调整：小盘股target_vol更高，size_scalar可适当上调
        if market_cap is not None and market_cap < 50:
            # 小盘股波动率天然高，若已处于正常/低波动，说明相对其同类更稳定
            if regime in (VolRegime.NORMAL_VOL, VolRegime.LOW_VOL):
                base = min(base * 1.2, 2.0)
        
        return round(base, 2)

    def _generate_notes(self, internal: VolFacInternal, confidence: float) -> str:
        parts = []
        if confidence < 1.0:
            parts.append(f"数据完整度{confidence:.0%}，结果可靠性受限")
        if internal.hml_r_std_5m is None:
            parts.append("5分钟数据缺失，hml_r_std_5m未计算")
        if internal.vol_regime == VolRegime.EXTREME_VOL:
            parts.append("极端波动率状态，建议剔除或大幅降仓")
        return "; ".join(parts) if parts else ""


# ---------------------------------------------------------------------------
# 与 VolTarget 的互锁接口
# ---------------------------------------------------------------------------

class VolFacVolTargetBridge:
    """
    VOLFAC → VOLTARGET 互锁桥接
    
    VOLFAC 是 VOLTARGET 的核心输入参数来源
    """

    @staticmethod
    def to_voltarget_input(obj_out: ObjectCardOutput) -> Dict[str, Any]:
        """
        将 VOLFAC 输出转换为 VOLTARGET 输入
        
        Returns:
            dict: {
                'vt_current_vol': float,      # 当前年化波动率
                'vt_vol_regime': str,         # 波动率状态
                'vt_vol_trend': str,          # 波动率趋势
                'vt_size_scalar': float,      # 仓位缩放（来自VOLFAC）
            }
        """
        internal = obj_out.internal
        return {
            "vt_current_vol": internal.get("annualized_vol", 0.0),
            "vt_vol_regime": internal.get("vol_regime", "NORMAL_VOL"),
            "vt_vol_trend": internal.get("vol_trend", "STABLE"),
            "vt_size_scalar": obj_out.size_scalar,
        }


# ---------------------------------------------------------------------------
# 快速测试
# ---------------------------------------------------------------------------

def _quick_test():
    """内部快速验证"""
    np.random.seed(42)
    
    # 生成模拟60日收盘价
    returns = np.random.normal(0.001, 0.02, 60)
    close_60d = [10.0]
    for r in returns:
        close_60d.append(close_60d[-1] * (1 + r))
    close_60d = close_60d[1:]
    
    # 生成模拟1年历史波动率（用于分位）
    hist_vol = list(np.random.normal(0.025, 0.008, 250))
    
    vf = VolatilityFactor()
    raw = VolFacRawInput(
        close_60d=close_60d,
        historical_vol_1y=hist_vol,
    )
    
    result = vf.calculate(raw, strategy_type="swing", market_cap=30)
    
    print("=" * 60)
    print("VOLFAC 对象卡测试输出")
    print("=" * 60)
    for k, v in result.__dict__.items():
        print(f"  {k}: {v}")
    
    # 验证 VolTarget 桥接
    bridge = VolFacVolTargetBridge()
    vt_input = bridge.to_voltarget_input(result)
    print("\n→ VOLTARGET 桥接输入:")
    for k, v in vt_input.items():
        print(f"  {k}: {v}")
    
    # 边界测试：数据不足
    print("\n" + "=" * 60)
    print("边界测试：仅20日数据")
    print("=" * 60)
    raw_short = VolFacRawInput(close_60d=close_60d[:20])
    result_short = vf.calculate(raw_short, strategy_type="swing")
    print(f"  confidence: {result_short.confidence}")
    print(f"  signal_strength: {result_short.signal_strength}")
    print(f"  notes: {result_short.notes}")


if __name__ == "__main__":
    _quick_test()
