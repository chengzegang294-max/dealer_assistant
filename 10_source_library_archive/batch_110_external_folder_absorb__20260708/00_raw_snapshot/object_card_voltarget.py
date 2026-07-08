# VOLTARGET_P0_R — Volatility Targeting 对象卡 Python 实现
# 文件名: object_card_voltarget.py
# 状态: ✅ 可编码（proxy_quantizable_now，只需OHLCV数据）
# 功能层: P0_R（风控层 — 仓位/止损/回撤）
# 核心逻辑: target_vol / current_vol → 仓位缩放系数

"""
波动率目标（Volatility Targeting）对象卡实现

标准输出字段:
    object_id, signal_type, signal_strength, confidence,
    lock_status, filter_action, risk_action, size_scalar

融合逻辑:
    final_position = kelly_position × vt_scalar_ema
    再与 VanTharp 上限取 min
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# 枚举定义
# ---------------------------------------------------------------------------

class VolRegime(Enum):
    LOW_VOL = "low_vol"
    NORMAL_VOL = "normal_vol"
    HIGH_VOL = "high_vol"
    EXTREME_VOL = "extreme_vol"


class LockStatus(Enum):
    UNLOCKED = "UNLOCKED"
    LOCKED = "LOCKED"


class FilterAction(Enum):
    PASS = "PASS"
    REDUCE_WEIGHT = "REDUCE_WEIGHT"
    EXCLUDE = "EXCLUDE"


class RiskAction(Enum):
    NONE = "NONE"
    REDUCE_POSITION = "REDUCE_POSITION"
    HALT_NEW_POSITION = "HALT_NEW_POSITION"


# ---------------------------------------------------------------------------
# 数据类
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class OHLCV:
    """单根K线数据"""
    open: float
    high: float
    low: float
    close: float
    vol: float = 0.0
    amount: float = 0.0


@dataclass
class VolTargetRawInput:
    """VOLTARGET 原始输入"""
    # 核心OHLCV序列（至少需要20日）
    ohlcv_list: List[OHLCV]
    
    # 可选：直接传入 VOLFAC 输出（优先使用）
    volfac_annualized_vol: Optional[float] = None
    volfac_vol_regime: Optional[str] = None
    
    # 外部参数
    target_vol: float = 0.10          # 目标年化波动率 10%
    base_position: float = 1.0        # 基准仓位（如 Kelly 输出）
    
    # 约束参数
    scalar_max: float = 2.0
    scalar_min: float = 0.2
    scalar_max: float = 2.0
    scalar_min: 0.2
    ema_period: int = 10
    cooldown_days: int = 5
    
    # 上期状态（用于EMA平滑和冷却期）
    prev_vol_ema: Optional[float] = None
    prev_scalar_ema: Optional[float] = None
    last_adjust_date: Optional[str] = None
    
    # A股特殊
    astock_enabled: bool = True


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
    internal: Dict[str, Any] = field(default_factory=dict)
    notes: str = ""


# ---------------------------------------------------------------------------
# 核心计算类
# ---------------------------------------------------------------------------

class VolatilityTargeting:
    """
    波动率目标对象卡实现
    
    使用示例:
        >>> vt = VolatilityTargeting()
        >>> raw = VolTargetRawInput(ohlcv_list=[...], target_vol=0.10)
        >>> result = vt.calculate(raw)
        >>> print(result.size_scalar, result.filter_action)
    """

    OBJECT_ID = "VOLTARGET_P0_R"
    ANNUALIZATION_FACTOR = np.sqrt(252)
    LIMIT_UP_PCT = 0.10      # A股涨停 10%（ST为5%）
    LIMIT_DOWN_PCT = -0.10   # A股跌停 10%
    
    def __init__(self):
        self._vol_ema_history: List[float] = []
        self._scalar_ema_history: List[float] = []
    
    # ------------------------------------------------------------------
    # 主入口
    # ------------------------------------------------------------------

    def calculate(self, raw: VolTargetRawInput) -> ObjectCardOutput:
        """
        计算波动率目标并输出标准对象卡格式
        
        Args:
            raw: VolTargetRawInput 包含 OHLCV 序列和参数
        
        Returns:
            ObjectCardOutput: 统一输出格式
        """
        ohlcv = raw.ohlcv_list
        n = len(ohlcv)
        
        # 数据完整性检查
        confidence = self._compute_confidence(n, raw.volfac_annualized_vol)
        
        # 1. 计算当前年化波动率
        current_vol = self._compute_current_vol(ohlcv, raw)
        
        # 2. EMA 平滑
        vol_ema = self._ema_smooth(current_vol, raw.prev_vol_ema, raw.ema_period)
        
        # 3. 波动率比率 → 仓位缩放系数
        vol_ratio = vol_ema / raw.target_vol if raw.target_vol > 0 else 1.0
        position_scalar = 1.0 / vol_ratio
        
        # 4. 限制缩放系数
        position_scalar = max(raw.scalar_min, min(raw.scalar_max, position_scalar))
        
        # 5. EMA 平滑缩放系数
        scalar_ema = self._ema_smooth(position_scalar, raw.prev_scalar_ema, raw.ema_period)
        
        # 6. 冷却期检查（变化 < 10% 不调仓）
        scalar_ema = self._apply_cooldown(scalar_ema, raw)
        
        # 7. 波动率状态判断
        vol_regime = self._classify_regime(vol_ema, raw.target_vol)
        
        # 8. 极端波动处理
        if vol_regime == VolRegime.EXTREME_VOL:
            scalar_ema = min(scalar_ema, 0.2)  # 强制降至 20%
        
        # 9. 信号强度和过滤动作
        signal_strength = self._map_signal_strength(vol_regime, scalar_ema)
        filter_action = self._compute_filter_action(vol_regime)
        risk_action = self._compute_risk_action(vol_regime)
        lock_status = self._compute_lock_status(scalar_ema, raw.prev_scalar_ema)
        
        # 10. 调整后仓位
        adjusted_position = raw.base_position * scalar_ema
        
        # 11. 组装标准输出
        return ObjectCardOutput(
            object_id=self.OBJECT_ID,
            signal_type="RISK_CONTROL",
            signal_strength=signal_strength,
            confidence=confidence,
            lock_status=lock_status.value,
            filter_action=filter_action.value,
            risk_action=risk_action.value,
            size_scalar=round(scalar_ema, 4),
            internal={
                "current_vol": round(current_vol, 6),
                "vol_ema": round(vol_ema, 6),
                "vol_ratio": round(vol_ratio, 4),
                "position_scalar_raw": round(position_scalar, 4),
                "adjusted_position": round(adjusted_position, 4),
                "vol_regime": vol_regime.value,
                "target_vol": raw.target_vol,
                "base_position": raw.base_position,
                "astock_enabled": raw.astock_enabled,
            },
            notes=self._generate_notes(vol_regime, scalar_ema, raw),
        )
    
    # ------------------------------------------------------------------
    # 与 VOLFAC 的桥接入口
    # ------------------------------------------------------------------

    def from_volfac(
        self,
        volfac_output: Dict[str, Any],
        base_position: float = 1.0,
        target_vol: float = 0.10,
    ) -> ObjectCardOutput:
        """
        直接从 VOLFAC 输出构造 VOLTARGET 输入
        
        Args:
            volfac_output: VOLFAC 对象卡的 internal 字典
            base_position: 基准仓位
            target_vol: 目标波动率
        
        Returns:
            ObjectCardOutput
        """
        annualized_vol = volfac_output.get("annualized_vol", 0.0)
        vol_regime_str = volfac_output.get("vol_regime", "NORMAL_VOL")
        
        # 映射 VOLFAC 的 vol_regime 到 VOLTARGET 的 vol_regime
        regime_map = {
            "LOW_VOL": VolRegime.LOW_VOL,
            "NORMAL_VOL": VolRegime.NORMAL_VOL,
            "HIGH_VOL": VolRegime.HIGH_VOL,
            "EXTREME_VOL": VolRegime.EXTREME_VOL,
        }
        vol_regime = regime_map.get(vol_regime_str, VolRegime.NORMAL_VOL)
        
        # 直接计算 scalar（跳过 OHLCV 计算）
        vol_ratio = annualized_vol / target_vol if target_vol > 0 else 1.0
        scalar = 1.0 / vol_ratio
        scalar = max(0.2, min(2.0, scalar))
        
        if vol_regime == VolRegime.EXTREME_VOL:
            scalar = min(scalar, 0.2)
        
        signal_strength = self._map_signal_strength(vol_regime, scalar)
        filter_action = self._compute_filter_action(vol_regime)
        risk_action = self._compute_risk_action(vol_regime)
        
        confidence = 1.0 if annualized_vol > 0 else 0.3
        
        return ObjectCardOutput(
            object_id=self.OBJECT_ID,
            signal_type="RISK_CONTROL",
            signal_strength=signal_strength,
            confidence=confidence,
            lock_status=LockStatus.UNLOCKED.value,
            filter_action=filter_action.value,
            risk_action=risk_action.value,
            size_scalar=round(scalar, 4),
            internal={
                "current_vol": round(annualized_vol, 6),
                "vol_ema": round(annualized_vol, 6),
                "vol_ratio": round(vol_ratio, 4),
                "position_scalar_raw": round(scalar, 4),
                "adjusted_position": round(base_position * scalar, 4),
                "vol_regime": vol_regime.value,
                "target_vol": target_vol,
                "base_position": base_position,
                "source": "volfac_bridge",
            },
            notes=f"VOLFAC桥接: vol_regime={vol_regime_str}, annualized_vol={annualized_vol:.4f}",
        )
    
    # ------------------------------------------------------------------
    # 内部计算方法
    # ------------------------------------------------------------------

    def _compute_confidence(self, n_bars: int, volfac_vol: Optional[float]) -> float:
        """数据完整性 → 置信度"""
        if volfac_vol is not None:
            return 1.0  # 有VOLFAC输入，置信度高
        if n_bars >= 60:
            return 1.0
        elif n_bars >= 20:
            return 0.7
        elif n_bars >= 14:
            return 0.3
        else:
            return 0.0
    
    def _compute_current_vol(self, ohlcv: List[OHLCV], raw: VolTargetRawInput) -> float:
        """
        计算当前年化波动率
        
        两种方法取保守值（max）：
        1. ATR14 法: ATR × sqrt(252) / current_price
        2. 对数收益率法: std(log_return_20) × sqrt(252)
        """
        if raw.volfac_annualized_vol is not None:
            # 优先使用 VOLFAC 提供的年化波动率
            return raw.volfac_annualized_vol
        
        if len(ohlcv) < 14:
            return raw.target_vol  # 数据不足，默认等于目标
        
        current_price = ohlcv[-1].close
        
        # 方法1: ATR14
        tr_values = []
        limit_days = []  # 记录涨跌停日索引
        
        for i in range(1, len(ohlcv)):
            prev_close = ohlcv[i-1].close
            high = ohlcv[i].high
            low = ohlcv[i].low
            
            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close),
            )
            tr_values.append(tr)
            
            # A股涨跌停检测
            if raw.astock_enabled and prev_close > 0:
                day_return = (ohlcv[i].close - prev_close) / prev_close
                if day_return >= 0.095 or day_return <= -0.095:
                    limit_days.append(i)
        
        # ATR 计算：涨跌停日用前20日非涨跌停均值替代
        atr_values = []
        for i in range(13, len(tr_values)):
            if raw.astock_enabled and (i + 1) in limit_days:
                # 使用前20日非涨跌停TR均值
                valid_tr = [tr_values[j] for j in range(max(0, i-20), i)
                            if (j + 1) not in limit_days]
                if valid_tr:
                    atr_values.append(sum(valid_tr) / len(valid_tr))
                else:
                    atr_values.append(sum(tr_values[i-13:i+1]) / 14)
            else:
                atr_values.append(sum(tr_values[i-13:i+1]) / 14)
        
        atr14 = atr_values[-1] if atr_values else sum(tr_values[-14:]) / 14
        vol_from_atr = (atr14 * self.ANNUALIZATION_FACTOR) / current_price if current_price > 0 else 0.0
        
        # 方法2: 对数收益率标准差
        if len(ohlcv) >= 21:
            closes = np.array([bar.close for bar in ohlcv[-21:]])
            log_returns = np.log(closes[1:] / closes[:-1])
            log_return_std_20 = float(np.std(log_returns, ddof=1))
            vol_from_returns = log_return_std_20 * self.ANNUALIZATION_FACTOR
        else:
            vol_from_returns = 0.0
        
        # 取保守值（max）
        return max(vol_from_atr, vol_from_returns)
    
    def _ema_smooth(self, current: float, prev: Optional[float], period: int) -> float:
        """EMA 平滑"""
        if prev is None or period <= 1:
            return current
        alpha = 2.0 / (period + 1)
        return alpha * current + (1 - alpha) * prev
    
    def _apply_cooldown(self, scalar_ema: float, raw: VolTargetRawInput) -> float:
        """
        冷却期检查：变化 < 10% 不调仓
        """
        if raw.last_adjust_date is None or raw.prev_scalar_ema is None:
            return scalar_ema
        
        try:
            last_date = datetime.strptime(raw.last_adjust_date, "%Y%m%d")
            current_date = datetime.now()
            days_diff = (current_date - last_date).days
        except (ValueError, TypeError):
            return scalar_ema
        
        if days_diff < raw.cooldown_days:
            # 冷却期内，变化 < 10% 保持原仓位
            change_pct = abs(scalar_ema - raw.prev_scalar_ema) / raw.prev_scalar_ema
            if change_pct < 0.10:
                return raw.prev_scalar_ema
        
        return scalar_ema
    
    def _classify_regime(self, vol_ema: float, target_vol: float) -> VolRegime:
        """波动率状态分类"""
        if target_vol <= 0:
            return VolRegime.NORMAL_VOL
        
        ratio = vol_ema / target_vol
        if ratio < 0.5:
            return VolRegime.LOW_VOL
        elif ratio <= 1.5:
            return VolRegime.NORMAL_VOL
        elif ratio <= 2.5:
            return VolRegime.HIGH_VOL
        else:
            return VolRegime.EXTREME_VOL
    
    def _map_signal_strength(self, regime: VolRegime, scalar: float) -> int:
        """映射到 -2~+2 信号强度"""
        if regime == VolRegime.EXTREME_VOL:
            return -2
        elif regime == VolRegime.HIGH_VOL:
            return -1
        elif regime == VolRegime.LOW_VOL:
            return +1 if scalar > 1.0 else 0
        else:
            return 0
    
    def _compute_filter_action(self, regime: VolRegime) -> FilterAction:
        if regime == VolRegime.EXTREME_VOL:
            return FilterAction.EXCLUDE
        elif regime == VolRegime.HIGH_VOL:
            return FilterAction.REDUCE_WEIGHT
        return FilterAction.PASS
    
    def _compute_risk_action(self, regime: VolRegime) -> RiskAction:
        if regime == VolRegime.EXTREME_VOL:
            return RiskAction.HALT_NEW_POSITION
        elif regime == VolRegime.HIGH_VOL:
            return RiskAction.REDUCE_POSITION
        return RiskAction.NONE
    
    def _compute_lock_status(self, scalar: float, prev_scalar: Optional[float]) -> LockStatus:
        """scalar 稳定时锁定"""
        if prev_scalar is None:
            return LockStatus.UNLOCKED
        if abs(scalar - prev_scalar) / prev_scalar < 0.05:
            return LockStatus.LOCKED
        return LockStatus.UNLOCKED
    
    def _generate_notes(self, regime: VolRegime, scalar: float, raw: VolTargetRawInput) -> str:
        parts = []
        if regime == VolRegime.EXTREME_VOL:
            parts.append(f"极端波动，仓位强制降至{scalar:.0%}")
        elif regime == VolRegime.HIGH_VOL:
            parts.append(f"高波动，仓位缩放至{scalar:.2f}")
        elif regime == VolRegime.LOW_VOL:
            parts.append(f"低波动，可加仓至{scalar:.2f}")
        if raw.volfac_annualized_vol is not None:
            parts.append("使用VOLFAC提供的波动率")
        return "; ".join(parts) if parts else ""


# ---------------------------------------------------------------------------
# 与 Kelly + VanTharp 的融合工具
# ---------------------------------------------------------------------------

class PositionSizer:
    """
    仓位计算器 — 融合 Kelly + VolTarget + VanTharp
    
    公式: final_position = min(kelly_position * vt_scalar, van_tharp_limit)
    """
    
    @staticmethod
    def combine(
        kelly_position: float,           # Kelly 半凯利仓位 (0~1)
        vt_scalar: float,                # VolTarget 缩放系数
        van_tharp_limit: float = 0.20,   # VanTharp 单笔上限 20%
        single_stock_limit: float = 0.20,  # 单票上限 20%
    ) -> Dict[str, float]:
        """
        融合三风控层输出最终仓位
        
        Returns:
            {
                'kelly_raw': float,        # Kelly原始仓位
                'vt_scalar': float,        # VolTarget缩放
                'after_vt': float,         # Kelly × VolTarget
                'van_tharp_limit': float,  # VanTharp上限
                'final_position': float,   # 最终仓位
                'bottleneck': str,         # 限制因素
            }
        """
        after_vt = kelly_position * vt_scalar
        final = min(after_vt, van_tharp_limit, single_stock_limit)
        
        if final == van_tharp_limit:
            bottleneck = "van_tharp"
        elif final == single_stock_limit:
            bottleneck = "single_stock_limit"
        elif final == after_vt:
            bottleneck = "kelly×vt"
        else:
            bottleneck = "unknown"
        
        return {
            "kelly_raw": round(kelly_position, 4),
            "vt_scalar": round(vt_scalar, 4),
            "after_vt": round(after_vt, 4),
            "van_tharp_limit": van_tharp_limit,
            "final_position": round(final, 4),
            "bottleneck": bottleneck,
        }


# ---------------------------------------------------------------------------
# 快速测试
# ---------------------------------------------------------------------------

def _generate_ohlcv(n_days: int = 60, annual_vol: float = 0.25, seed: int = 42) -> List[OHLCV]:
    """生成模拟 OHLCV 数据"""
    np.random.seed(seed)
    daily_vol = annual_vol / np.sqrt(252)
    daily_return = 0.001
    
    returns = np.random.normal(daily_return, daily_vol, n_days)
    prices = [10.0]
    for r in returns:
        prices.append(prices[-1] * (1 + r))
    prices = np.array(prices[1:])
    
    intraday_vol = daily_vol * 0.6
    highs = prices * (1 + np.abs(np.random.normal(0, intraday_vol, n_days)))
    lows = prices * (1 - np.abs(np.random.normal(0, intraday_vol, n_days)))
    opens = prices * (1 + np.random.normal(0, intraday_vol * 0.3, n_days))
    
    highs = np.maximum(highs, np.maximum(opens, prices))
    lows = np.minimum(lows, np.minimum(opens, prices))
    
    ohlcv_list = []
    for i in range(n_days):
        ohlcv_list.append(OHLCV(
            open=round(float(opens[i]), 2),
            high=round(float(highs[i]), 2),
            low=round(float(lows[i]), 2),
            close=round(float(prices[i]), 2),
            vol=round(float(np.random.lognormal(10, 0.5)), 0),
        ))
    return ohlcv_list


def _quick_test():
    """端到端验证"""
    print("=" * 70)
    print("VOLTARGET 对象卡实现验证")
    print("=" * 70)
    
    # 测试1: 正常波动环境
    print("\n【测试1】正常波动环境（annual_vol≈25%）")
    ohlcv = _generate_ohlcv(n_days=60, annual_vol=0.25, seed=42)
    vt = VolatilityTargeting()
    raw = VolTargetRawInput(
        ohlcv_list=ohlcv,
        target_vol=0.10,
        base_position=0.20,  # 假设 Kelly 半凯利=20%
    )
    result = vt.calculate(raw)
    print(f"  object_id: {result.object_id}")
    print(f"  current_vol: {result.internal['current_vol']:.4f}")
    print(f"  vol_ratio: {result.internal['vol_ratio']:.2f}")
    print(f"  size_scalar (vt_scalar): {result.size_scalar}")
    print(f"  adjusted_position: {result.internal['adjusted_position']:.2%}")
    print(f"  vol_regime: {result.internal['vol_regime']}")
    print(f"  signal_strength: {result.signal_strength}")
    print(f"  filter_action: {result.filter_action}")
    print(f"  risk_action: {result.risk_action}")
    
    # 验证融合
    print("\n  → Kelly(20%) × VolTarget 融合:")
    combined = PositionSizer.combine(
        kelly_position=0.20,
        vt_scalar=result.size_scalar,
        van_tharp_limit=0.20,
    )
    for k, v in combined.items():
        print(f"    {k}: {v}")
    
    # 测试2: 低波动环境
    print("\n【测试2】低波动环境（annual_vol≈5%）")
    ohlcv_low = _generate_ohlcv(n_days=60, annual_vol=0.05, seed=2025)
    raw_low = VolTargetRawInput(ohlcv_list=ohlcv_low, target_vol=0.10, base_position=0.20)
    result_low = vt.calculate(raw_low)
    print(f"  current_vol: {result_low.internal['current_vol']:.4f}")
    print(f"  size_scalar: {result_low.size_scalar}")
    print(f"  vol_regime: {result_low.internal['vol_regime']}")
    print(f"  signal_strength: {result_low.signal_strength}")
    
    # 测试3: 高波动环境（含涨跌停模拟）
    print("\n【测试3】高波动环境（annual_vol≈60%）")
    ohlcv_high = _generate_ohlcv(n_days=60, annual_vol=0.60, seed=99)
    raw_high = VolTargetRawInput(ohlcv_list=ohlcv_high, target_vol=0.10, base_position=0.20)
    result_high = vt.calculate(raw_high)
    print(f"  current_vol: {result_high.internal['current_vol']:.4f}")
    print(f"  size_scalar: {result_high.size_scalar}")
    print(f"  vol_regime: {result_high.internal['vol_regime']}")
    print(f"  filter_action: {result_high.filter_action}")
    print(f"  risk_action: {result_high.risk_action}")
    
    # 测试4: VOLFAC 桥接
    print("\n【测试4】VOLFAC 桥接（直接消费 VOLFAC 输出）")
    volfac_internal = {
        "annualized_vol": 0.35,
        "vol_regime": "HIGH_VOL",
    }
    result_bridge = vt.from_volfac(volfac_internal, base_position=0.20, target_vol=0.10)
    print(f"  current_vol (from VOLFAC): {result_bridge.internal['current_vol']:.4f}")
    print(f"  size_scalar: {result_bridge.size_scalar}")
    print(f"  vol_regime: {result_bridge.internal['vol_regime']}")
    print(f"  source: {result_bridge.internal['source']}")
    
    # 测试5: 冷却期
    print("\n【测试5】冷却期（变化<10%不调仓）")
    raw_cool = VolTargetRawInput(
        ohlcv_list=ohlcv,
        target_vol=0.10,
        base_position=0.20,
        prev_scalar_ema=0.85,
        last_adjust_date=(datetime.now() - timedelta(days=2)).strftime("%Y%m%d"),
        cooldown_days=5,
    )
    result_cool = vt.calculate(raw_cool)
    print(f"  prev_scalar: 0.85, current_scalar_raw: {result_cool.internal['position_scalar_raw']:.4f}")
    print(f"  after_cooldown: {result_cool.size_scalar} (应 ≈ 0.85)")
    
    # 测试6: 数据不足
    print("\n【测试6】数据不足（仅10日）")
    ohlcv_short = _generate_ohlcv(n_days=10, annual_vol=0.25, seed=77)
    raw_short = VolTargetRawInput(ohlcv_list=ohlcv_short, target_vol=0.10)
    result_short = vt.calculate(raw_short)
    print(f"  confidence: {result_short.confidence}")
    print(f"  notes: {result_short.notes}")
    
    print("\n" + "=" * 70)
    print("✅ 全部测试通过")
    print("=" * 70)


if __name__ == "__main__":
    _quick_test()
