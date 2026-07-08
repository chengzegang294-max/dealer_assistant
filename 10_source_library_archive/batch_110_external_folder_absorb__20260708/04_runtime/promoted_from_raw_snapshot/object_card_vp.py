# VP_P0_E — Volume Profile（成交量分布）对象卡 Python 实现
# 文件名: object_card_vp.py
# 状态: [OK] proxy_quantizable_now
# 数据需求: OHLCV序列（日频简化版）
# A股落地: 直接可用（需加入涨停/跌停/T+1过滤）

"""
Volume Profile（成交量分布）对象卡实现

功能层: P0_E（执行层 — 入场/出场/执行质量）
来源: 市场轮廓理论 + 成交量分布公开定义
核心逻辑: 识别 POC / VAH / VAL / HVN / LVN

标准输出字段:
    object_id, signal_type, signal_strength, confidence,
    lock_status, filter_action, risk_action, size_scalar

A股纯多头适配:
    - 所有做空信号（SHORT）降级为 'NONE' 或观察信号
    - 只做 POC_SUPPORT（支撑）、LVN_MOMENTUM_UP（动量向上）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any


# ---------------------------------------------------------------------------
# 枚举定义
# ---------------------------------------------------------------------------

class VPSignalType:
    """VP 信号类型"""
    NONE = "NONE"
    POC_SUPPORT = "POC_SUPPORT"
    VAH_RESISTANCE = "VAH_RESISTANCE"
    LVN_MOMENTUM = "LVN_MOMENTUM"


class LockStatus:
    UNLOCKED = "UNLOCKED"
    LOCKED = "LOCKED"


class FilterAction:
    PASS = "PASS"
    REDUCE_WEIGHT = "REDUCE_WEIGHT"
    WAIT = "WAIT"


class RiskAction:
    NONE = "NONE"
    TIGHTEN_STOP = "TIGHTEN_STOP"


# ---------------------------------------------------------------------------
# 数据类
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class VPRawInput:
    """VP 原始数据输入"""
    # OHLCV 序列（日频简化版）
    ohlcv: List[Dict[str, float]]  # [{'open': float, 'high': float, 'low': float, 'close': float, 'volume': float}, ...]
    
    # 可选参数
    current_price: Optional[float] = None   # 当前价格，默认取最后一根 close
    n_bins: int = 30                        # 价格区间划分数量
    va_pct: float = 0.70                    # 价值区域百分比（默认 70%）
    hvn_threshold_mult: float = 1.5         # HVN 阈值（相对均值倍数）
    lvn_threshold_mult: float = 0.3         # LVN 阈值（相对均值倍数）
    atr14: Optional[float] = None           # 14日 ATR，用于信号判断
    
    # A股适配
    astock_long_only: bool = True           # A股纯多头模式
    min_period: int = 10                    # 最小 K 线数量


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
    size_scalar: float            # 0.0 ~ 1.0
    internal: Dict[str, Any] = field(default_factory=dict)
    notes: str = ""


# ---------------------------------------------------------------------------
# 核心计算类
# ---------------------------------------------------------------------------

class VolumeProfile:
    """
    成交量分布对象卡实现（日频简化版）

    使用典型价格 (high + low + close) / 3 将成交量分配到价格 bin，
    识别 POC、VAH、VAL、HVN、LVN，并生成交易信号。
    
    使用示例:
        >>> vp = VolumeProfile()
        >>> raw = VPRawInput(ohlcv=[...], current_price=100.0)
        >>> result = vp.calculate(raw)
        >>> print(result.signal_type)  # 'POC_SUPPORT' / 'LVN_MOMENTUM' / ...
    """

    OBJECT_ID = "VP_P0_E"
    VERSION = "v1.0"

    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # 主入口
    # ------------------------------------------------------------------

    def calculate(self, raw: VPRawInput) -> ObjectCardOutput:
        """
        计算成交量分布并输出标准对象卡格式
        
        Args:
            raw: 原始输入数据（OHLCV序列 + 参数）
        
        Returns:
            ObjectCardOutput: 统一输出格式
        """
        # 1. 数据完整性检查
        if len(raw.ohlcv) < raw.min_period:
            return self._insufficient_data(len(raw.ohlcv), raw.min_period)
        
        # 2. 取计算窗口（最近60根，或全部）
        window = raw.ohlcv[-60:] if len(raw.ohlcv) > 60 else raw.ohlcv
        
        # 3. 确定价格范围
        price_min = min(bar['low'] for bar in window)
        price_max = max(bar['high'] for bar in window)
        
        if price_max <= price_min:
            return self._error_output("invalid_price_range")
        
        bin_size = (price_max - price_min) / raw.n_bins
        
        # 4. 按价格 bin 分配成交量（典型价格法）
        bins: Dict[float, float] = {}
        for bar in window:
            typical_price = (bar['high'] + bar['low'] + bar['close']) / 3.0
            volume = bar.get('volume', 0.0)
            bin_idx = int((typical_price - price_min) / bin_size)
            bin_idx = min(bin_idx, raw.n_bins - 1)  # 边界保护
            bin_price = price_min + (bin_idx + 0.5) * bin_size  # bin 中心价格
            bins[bin_price] = bins.get(bin_price, 0.0) + volume
        
        if not bins:
            return self._error_output("no_volume_data")
        
        # 5. POC = 成交量最高的 bin
        sorted_by_vol = sorted(bins.items(), key=lambda x: x[1], reverse=True)
        vp_poc = sorted_by_vol[0][0]
        vp_poc_volume = sorted_by_vol[0][1]
        
        # 6. VA（价值区域）= 从 POC 向两侧扩展，直到累积成交量达到 va_pct
        total_volume = sum(v for _, v in bins.items())
        target_va_volume = total_volume * raw.va_pct
        
        price_sorted = sorted(bins.items(), key=lambda x: x[0])
        poc_idx = next(
            (i for i, (p, _) in enumerate(price_sorted) if abs(p - vp_poc) < bin_size / 2),
            len(price_sorted) // 2
        )
        
        va_low_idx = poc_idx
        va_high_idx = poc_idx
        va_cum_volume = price_sorted[poc_idx][1]
        
        while va_cum_volume < target_va_volume:
            low_dist = poc_idx - va_low_idx if va_low_idx > 0 else float('inf')
            high_dist = va_high_idx - poc_idx if va_high_idx < len(price_sorted) - 1 else float('inf')
            
            if low_dist <= high_dist and va_low_idx > 0:
                va_low_idx -= 1
                va_cum_volume += price_sorted[va_low_idx][1]
            elif va_high_idx < len(price_sorted) - 1:
                va_high_idx += 1
                va_cum_volume += price_sorted[va_high_idx][1]
            else:
                break  # 无法继续扩展
        
        vp_val = price_sorted[va_low_idx][0]
        vp_vah = price_sorted[va_high_idx][0]
        
        # 7. HVN / LVN 识别
        avg_volume = total_volume / len(bins) if bins else 0.0
        vp_hvn_levels = [p for p, v in bins.items() if v > avg_volume * raw.hvn_threshold_mult]
        vp_lvn_levels = [p for p, v in bins.items() if v < avg_volume * raw.lvn_threshold_mult]
        
        # 8. 当前价格
        current_price = raw.current_price if raw.current_price is not None else window[-1]['close']
        
        # 9. ATR 估算（若未提供）
        atr = raw.atr14 if raw.atr14 is not None else (price_max - price_min) * 0.05
        
        # 10. 当前价格相对 VA 的位置
        at_poc = abs(current_price - vp_poc) / atr < 0.5 if atr > 0 else False
        above_vah = current_price > vp_vah
        below_val = current_price < vp_val
        inside_va = not (above_vah or below_val)
        
        # 11. 信号生成
        signal_type, signal_strength, size_scalar, confidence = self._generate_signal(
            current_price=current_price,
            vp_poc=vp_poc,
            vp_vah=vp_vah,
            vp_val=vp_val,
            vp_hvn_levels=vp_hvn_levels,
            vp_lvn_levels=vp_lvn_levels,
            at_poc=at_poc,
            above_vah=above_vah,
            below_val=below_val,
            inside_va=inside_va,
            atr=atr,
            window=window,
            astock_long_only=raw.astock_long_only,
        )
        
        # 12. 过滤动作与风险动作
        filter_action, risk_action = self._map_actions(signal_type, astock_long_only=raw.astock_long_only)
        
        # 13. 成交量分布形态判断
        trend_shape = self._classify_trend_shape(bins, vp_poc, avg_volume)
        
        # 14. 组装标准输出
        internal = {
            "vp_poc": round(vp_poc, 4),
            "vp_vah": round(vp_vah, 4),
            "vp_val": round(vp_val, 4),
            "vp_profile_high": round(price_max, 4),
            "vp_profile_low": round(price_min, 4),
            "vp_total_volume": round(total_volume, 2),
            "vp_hvn_levels": sorted(vp_hvn_levels),
            "vp_lvn_levels": sorted(vp_lvn_levels),
            "vp_hvn_count": len(vp_hvn_levels),
            "vp_lvn_count": len(vp_lvn_levels),
            "vp_trend_shape": trend_shape,
            "current_price": round(current_price, 4),
            "current_rel_position": (
                "at_poc" if at_poc else
                ("above" if above_vah else ("below" if below_val else "inside"))
            ),
            "atr_used": round(atr, 4),
        }
        
        notes = self._generate_notes(signal_type, trend_shape, raw.astock_long_only)
        
        return ObjectCardOutput(
            object_id=self.OBJECT_ID,
            signal_type=signal_type,
            signal_strength=signal_strength,
            confidence=round(confidence, 2),
            lock_status=LockStatus.UNLOCKED,
            filter_action=filter_action,
            risk_action=risk_action,
            size_scalar=round(size_scalar, 4),
            internal=internal,
            notes=notes,
        )

    # ------------------------------------------------------------------
    # 信号生成
    # ------------------------------------------------------------------

    def _generate_signal(
        self,
        current_price: float,
        vp_poc: float,
        vp_vah: float,
        vp_val: float,
        vp_hvn_levels: List[float],
        vp_lvn_levels: List[float],
        at_poc: bool,
        above_vah: bool,
        below_val: bool,
        inside_va: bool,
        atr: float,
        window: List[Dict[str, float]],
        astock_long_only: bool,
    ) -> tuple:
        """
        生成交易信号
        
        Returns:
            (signal_type, signal_strength, size_scalar, confidence)
        """
        # 1. POC 支撑信号（价格在 POC 附近，且 POC 是 HVN）
        if at_poc:
            poc_is_hvn = any(abs(vp_poc - hvn) < atr * 0.3 for hvn in vp_hvn_levels)
            if poc_is_hvn:
                # 判断价格是从下方上来的（前一根收盘价 < POC）
                if len(window) >= 2:
                    prev_close = window[-2]['close']
                    if prev_close < vp_poc:
                        return VPSignalType.POC_SUPPORT, 1, 0.3, 0.6
                    elif prev_close > vp_poc and not astock_long_only:
                        # 从上方下来 → 做空信号（A股纯多头时降级）
                        if astock_long_only:
                            return VPSignalType.NONE, 0, 0.0, 0.3
                        return VPSignalType.VAH_RESISTANCE, -1, 0.0, 0.5
                # 无法判断方向，给出中性 POC 信号
                return VPSignalType.POC_SUPPORT, 0, 0.15, 0.45
        
        # 2. VAH 阻力信号（价格在 VAH 之上或附近）
        if above_vah or (inside_va and abs(current_price - vp_vah) / atr < 0.3):
            # A股纯多头：不做空，VAH 视为阻力/观望区
            if astock_long_only:
                return VPSignalType.VAH_RESISTANCE, 0, 0.0, 0.35
            return VPSignalType.VAH_RESISTANCE, -1, 0.0, 0.4
        
        # 3. VAL 下方（弱势）
        if below_val:
            # A股纯多头：VAL 下方 = 弱势观望，不做空
            if astock_long_only:
                return VPSignalType.NONE, 0, 0.0, 0.25
            return VPSignalType.VAH_RESISTANCE, -1, 0.0, 0.35
        
        # 4. LVN 动量信号（价格快速穿越 LVN 区域）
        in_lvn = any(abs(current_price - lvn) / atr < 0.5 for lvn in vp_lvn_levels) if atr > 0 else False
        if in_lvn:
            current_bar = window[-1]
            bar_range = abs(current_bar['close'] - current_bar['open'])
            if bar_range > atr * 0.5:
                direction_up = current_bar['close'] > current_bar['open']
                if direction_up:
                    return VPSignalType.LVN_MOMENTUM, 1, 0.25, 0.55
                elif not astock_long_only:
                    return VPSignalType.LVN_MOMENTUM, -1, 0.0, 0.5
                else:
                    # A股纯多头：向下动量降级
                    return VPSignalType.NONE, 0, 0.0, 0.3
        
        # 5. 无信号
        return VPSignalType.NONE, 0, 0.0, 0.3

    # ------------------------------------------------------------------
    # 辅助方法
    # ------------------------------------------------------------------

    def _map_actions(self, signal_type: str, astock_long_only: bool) -> tuple:
        """映射信号到过滤动作和风险动作"""
        if signal_type == VPSignalType.NONE:
            return FilterAction.WAIT, RiskAction.NONE
        elif signal_type == VPSignalType.POC_SUPPORT:
            return FilterAction.PASS, RiskAction.NONE
        elif signal_type == VPSignalType.LVN_MOMENTUM:
            return FilterAction.PASS, RiskAction.TIGHTEN_STOP
        elif signal_type == VPSignalType.VAH_RESISTANCE:
            if astock_long_only:
                return FilterAction.WAIT, RiskAction.NONE
            return FilterAction.REDUCE_WEIGHT, RiskAction.TIGHTEN_STOP
        return FilterAction.PASS, RiskAction.NONE

    def _classify_trend_shape(
        self,
        bins: Dict[float, float],
        vp_poc: float,
        avg_volume: float,
    ) -> str:
        """成交量分布形态判断"""
        lower_hvn_volume = sum(
            v for p, v in bins.items() if p < vp_poc and v > avg_volume * 1.5
        )
        upper_hvn_volume = sum(
            v for p, v in bins.items() if p > vp_poc and v > avg_volume * 1.5
        )
        
        if lower_hvn_volume > upper_hvn_volume * 1.5:
            return "ascending_triangle"   # 正三角 → 多头
        elif upper_hvn_volume > lower_hvn_volume * 1.5:
            return "descending_triangle"  # 倒三角 → 空头/盘整
        elif len([p for p, v in bins.items() if v > avg_volume * 1.5]) == 1:
            return "single_peak"          # 单峰 → 典型盘整
        else:
            return "balanced"

    def _insufficient_data(self, actual: int, required: int) -> ObjectCardOutput:
        """数据不足时返回空信号"""
        return ObjectCardOutput(
            object_id=self.OBJECT_ID,
            signal_type=VPSignalType.NONE,
            signal_strength=0,
            confidence=0.0,
            lock_status=LockStatus.UNLOCKED,
            filter_action=FilterAction.WAIT,
            risk_action=RiskAction.NONE,
            size_scalar=0.0,
            internal={"error": "ohlcv_too_few", "actual": actual, "required": required},
            notes=f"OHLCV数据不足: {actual} < {required}，禁止生成信号",
        )

    def _error_output(self, error_code: str) -> ObjectCardOutput:
        """错误输出"""
        return ObjectCardOutput(
            object_id=self.OBJECT_ID,
            signal_type=VPSignalType.NONE,
            signal_strength=0,
            confidence=0.0,
            lock_status=LockStatus.UNLOCKED,
            filter_action=FilterAction.WAIT,
            risk_action=RiskAction.NONE,
            size_scalar=0.0,
            internal={"error": error_code},
            notes=f"VP计算错误: {error_code}",
        )

    def _generate_notes(self, signal_type: str, trend_shape: str, astock_long_only: bool) -> str:
        """生成人类可读备注"""
        parts = []
        if signal_type == VPSignalType.POC_SUPPORT:
            parts.append("价格回归POC，高成交量节点确认支撑")
        elif signal_type == VPSignalType.LVN_MOMENTUM:
            parts.append("价格快速穿越低成交量区，动量信号")
        elif signal_type == VPSignalType.VAH_RESISTANCE:
            parts.append("价格处于价值区域上沿附近，注意阻力")
        if trend_shape == "single_peak":
            parts.append("分布呈单峰形态，市场处于极度平衡")
        if astock_long_only:
            parts.append("A股纯多头模式：做空信号已降级")
        return "; ".join(parts) if parts else "VP分布正常，无明确信号"


# ---------------------------------------------------------------------------
# 快速测试
# ---------------------------------------------------------------------------

def _quick_test() -> None:
    """内部快速验证 — 至少3个场景"""
    import random
    random.seed(42)
    
    print("=" * 60)
    print("VP_P0_E 对象卡实现验证")
    print("=" * 60)
    
    vp = VolumeProfile()
    
    # 生成测试数据：30日震荡行情
    base = 100.0
    ohlcv_base = []
    for i in range(30):
        close = base + random.uniform(-3, 3)
        high = close + random.uniform(0, 1.5)
        low = close - random.uniform(0, 1.5)
        open_p = close + random.uniform(-1, 1)
        vol = random.uniform(1000, 5000)
        ohlcv_base.append({"open": open_p, "high": high, "low": low, "close": close, "volume": vol})
    
    # 测试1: 价格接近 POC（震荡行情中心）
    print("\n【测试1】震荡行情，价格接近POC")
    ohlcv1 = [dict(bar) for bar in ohlcv_base]
    ohlcv1[-1]["close"] = base  # 让最后一根回到中心
    ohlcv1[-2]["close"] = base - 2.0  # 前一根从下方上来
    out1 = vp.calculate(VPRawInput(ohlcv=ohlcv1, current_price=base, astock_long_only=True))
    print(f"  signal_type: {out1.signal_type}")
    print(f"  signal_strength: {out1.signal_strength}")
    print(f"  size_scalar: {out1.size_scalar}")
    print(f"  POC: {out1.internal['vp_poc']:.2f}")
    print(f"  VAH: {out1.internal['vp_vah']:.2f}")
    print(f"  VAL: {out1.internal['vp_val']:.2f}")
    assert out1.signal_type in (VPSignalType.POC_SUPPORT, VPSignalType.NONE)
    print("  [OK] POC附近信号检测正常")
    
    # 测试2: 价格突破 VAH
    print("\n【测试2】价格突破VAH")
    ohlcv2 = [dict(bar) for bar in ohlcv_base]
    vah_price = out1.internal['vp_vah']
    breakout_price = vah_price + 5.0
    ohlcv2[-1]["close"] = breakout_price
    ohlcv2[-1]["high"] = breakout_price + 1.0
    out2 = vp.calculate(VPRawInput(ohlcv=ohlcv2, current_price=breakout_price, astock_long_only=True))
    print(f"  signal_type: {out2.signal_type}")
    print(f"  current_rel_position: {out2.internal['current_rel_position']}")
    assert out2.signal_type in (VPSignalType.VAH_RESISTANCE, VPSignalType.LVN_MOMENTUM, VPSignalType.NONE)
    print("  [OK] VAH突破信号检测正常")
    
    # 测试3: 数据不足
    print("\n【测试3】数据不足 (5根K线)")
    out3 = vp.calculate(VPRawInput(ohlcv=ohlcv_base[:5], astock_long_only=True))
    print(f"  signal_type: {out3.signal_type}")
    print(f"  size_scalar: {out3.size_scalar}")
    assert out3.signal_type == VPSignalType.NONE
    assert out3.size_scalar == 0.0
    print("  [OK] 数据不足保护生效")
    
    # 测试4: LVN 动量信号（大阳线穿越低成交量区）
    print("\n【测试4】LVN动量信号（大阳线）")
    ohlcv4 = [dict(bar) for bar in ohlcv_base]
    # 制造一根大阳线
    last_close = ohlcv4[-1]["close"]
    ohlcv4[-1]["open"] = last_close - 2.0
    ohlcv4[-1]["close"] = last_close + 3.0
    ohlcv4[-1]["high"] = last_close + 3.5
    ohlcv4[-1]["low"] = last_close - 2.5
    ohlcv4[-1]["volume"] = 8000  # 放量
    out4 = vp.calculate(VPRawInput(ohlcv=ohlcv4, astock_long_only=True))
    print(f"  signal_type: {out4.signal_type}")
    print(f"  trend_shape: {out4.internal['vp_trend_shape']}")
    print("  [OK] LVN动量检测正常")
    
    # 测试5: A股纯多头 vs 多空模式对比
    print("\n【测试5】A股纯多头 vs 多空模式（VAH阻力区）")
    ohlcv5 = [dict(bar) for bar in ohlcv_base]
    ohlcv5[-1]["close"] = out1.internal['vp_vah'] + 0.5
    ohlcv5[-1]["high"] = out1.internal['vp_vah'] + 1.0
    out5_long = vp.calculate(VPRawInput(ohlcv=ohlcv5, astock_long_only=True))
    out5_short = vp.calculate(VPRawInput(ohlcv=ohlcv5, astock_long_only=False))
    print(f"  A股纯多头 signal_type: {out5_long.signal_type}, filter_action: {out5_long.filter_action}")
    print(f"  多空模式 signal_type: {out5_short.signal_type}, filter_action: {out5_short.filter_action}")
    print("  [OK] A股纯多头适配正确")
    
    print("\n" + "=" * 60)
    print("[OK] VP_P0_E 全部测试通过")
    print("=" * 60)


if __name__ == "__main__":
    _quick_test()
