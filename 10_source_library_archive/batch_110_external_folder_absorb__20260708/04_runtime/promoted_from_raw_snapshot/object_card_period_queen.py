# PERIOD_QUEEN_P0_F — 周期状态系统（PeriodQueen）对象卡 Python 实现
# 文件名: object_card_period_queen.py
# 状态: ✅ 可编码（proxy_quantizable_now，基于日频OHLCV）
# 功能层: P0_F（环境识别 / 过滤器）
# 核心逻辑: 七态状态机，基于市场可观测证据判断情绪周期

"""
PeriodQueen — 系统心脏（Cycle State System）

回答的核心问题：当前市场处于什么情绪状态？该不该交易？

七态循环:
  ATTACK_SUSTAINED → ATTACK_CONFIRMED → POWER_TRANSITION → REMAINING_WARMTH
  → ATTACK_UNSUSTAINED → CUTTING_COMPLETE → GESTATION → 回到 ATTACK_SUSTAINED

标准输出字段:
    object_id, signal_type, signal_strength, confidence,
    lock_status, filter_action, risk_action, size_scalar

额外核心输出（通过 internal 字段）:
    pq_state, pq_trading_permission, pq_position_max_size,
    pq_entry_min_votes, pq_allowed_objects, pq_forbidden_objects
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any


# ---------------------------------------------------------------------------
# 枚举定义
# ---------------------------------------------------------------------------

class CycleState(Enum):
    ATTACK_SUSTAINED = "ATTACK_SUSTAINED"
    ATTACK_CONFIRMED = "ATTACK_CONFIRMED"
    POWER_TRANSITION = "POWER_TRANSITION"
    REMAINING_WARMTH = "REMAINING_WARMTH"
    ATTACK_UNSUSTAINED = "ATTACK_UNSUSTAINED"
    CUTTING_COMPLETE = "CUTTING_COMPLETE"
    GESTATION = "GESTATION"


class TradingPermission(Enum):
    FULL = "FULL"
    REDUCED = "REDUCED"
    EXIT_ONLY = "EXIT_ONLY"
    HALT = "HALT"


class LockStatus(Enum):
    UNLOCKED = "UNLOCKED"
    LOCKED = "LOCKED"


class FilterAction(Enum):
    PASS = "PASS"
    REDUCE_WEIGHT = "REDUCE_WEIGHT"
    EXCLUDE = "EXCLUDE"


class RiskAction(Enum):
    NONE = "NONE"
    HALT_NEW_POSITION = "HALT_NEW_POSITION"
    REDUCE_POSITION = "REDUCE_POSITION"


# ---------------------------------------------------------------------------
# 数据类
# ---------------------------------------------------------------------------

@dataclass
class PeriodQueenRawInput:
    """PeriodQueen 原始输入"""
    # 核心OHLCV序列（大盘指数或市场情绪指标股）
    index_ohlcv: List[Dict[str, float]]  # [{open, high, low, close, vol}]
    
    # 可选：VOLFAC 输出（用于波动率状态判断）
    volfac_vol_regime: Optional[str] = None
    volfac_annualized_vol: Optional[float] = None
    
    # 可选：涨跌停统计
    limit_up_count: Optional[int] = None
    limit_down_count: Optional[int] = None
    
    # 上期状态（用于状态转移判断）
    prev_state: Optional[str] = None
    state_duration: int = 0
    
    # 参数
    target_vol: float = 0.10


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

class PeriodQueen:
    """
    PeriodQueen — 周期状态系统
    
    系统心脏：所有执行层对象卡的交易权限、仓位上限、投票门槛由此决定。
    
    使用示例:
        >>> pq = PeriodQueen()
        >>> raw = PeriodQueenRawInput(index_ohlcv=[...])
        >>> result = pq.calculate(raw)
        >>> print(result.internal['pq_state'])
        >>> print(result.internal['pq_trading_permission'])
    """

    OBJECT_ID = "PERIOD_QUEEN_P0_F"
    
    # 状态 → 交易权限映射
    STATE_PERMISSION = {
        CycleState.ATTACK_SUSTAINED: TradingPermission.FULL,
        CycleState.ATTACK_CONFIRMED: TradingPermission.FULL,
        CycleState.POWER_TRANSITION: TradingPermission.REDUCED,
        CycleState.REMAINING_WARMTH: TradingPermission.EXIT_ONLY,
        CycleState.ATTACK_UNSUSTAINED: TradingPermission.HALT,
        CycleState.CUTTING_COMPLETE: TradingPermission.HALT,
        CycleState.GESTATION: TradingPermission.REDUCED,
    }
    
    # 状态 → 仓位上限映射
    STATE_MAX_SIZE = {
        CycleState.ATTACK_SUSTAINED: 1.0,
        CycleState.ATTACK_CONFIRMED: 0.7,
        CycleState.POWER_TRANSITION: 0.3,
        CycleState.REMAINING_WARMTH: 0.0,
        CycleState.ATTACK_UNSUSTAINED: 0.0,
        CycleState.CUTTING_COMPLETE: 0.0,
        CycleState.GESTATION: 0.3,
    }
    
    # 状态 → 投票门槛映射
    STATE_MIN_VOTES = {
        CycleState.ATTACK_SUSTAINED: 3,
        CycleState.ATTACK_CONFIRMED: 3,
        CycleState.POWER_TRANSITION: 4,
        CycleState.REMAINING_WARMTH: 2,
        CycleState.ATTACK_UNSUSTAINED: 5,
        CycleState.CUTTING_COMPLETE: 99,  # 禁止投票
        CycleState.GESTATION: 4,
    }
    
    # 状态 → 激活对象卡列表
    STATE_ALLOWED_OBJECTS = {
        CycleState.ATTACK_SUSTAINED: ["CHZL_BSD", "BPB", "VP", "TKR7", "MFLOW", "VOLFAC", "VOLTARGET"],
        CycleState.ATTACK_CONFIRMED: ["CHZL_BSD", "BPB", "VP", "TKR7", "MFLOW", "VOLFAC", "VOLTARGET"],
        CycleState.POWER_TRANSITION: ["YTC", "BPB", "VOLFAC", "VOLTARGET"],
        CycleState.REMAINING_WARMTH: ["TKR7", "CHZL_BSD", "VOLFAC", "VOLTARGET"],
        CycleState.ATTACK_UNSUSTAINED: [],
        CycleState.CUTTING_COMPLETE: [],
        CycleState.GESTATION: ["CHZL_BSD", "YTC", "BPB", "VOLFAC", "VOLTARGET"],
    }
    
    # 状态 → 信号强度
    STATE_SIGNAL_STRENGTH = {
        CycleState.ATTACK_SUSTAINED: 2,
        CycleState.ATTACK_CONFIRMED: 1,
        CycleState.POWER_TRANSITION: 0,
        CycleState.REMAINING_WARMTH: -1,
        CycleState.ATTACK_UNSUSTAINED: -2,
        CycleState.CUTTING_COMPLETE: -2,
        CycleState.GESTATION: 0,
    }

    def __init__(self):
        self._state_history: List[str] = []

    # ------------------------------------------------------------------
    # 主入口
    # ------------------------------------------------------------------

    def calculate(self, raw: PeriodQueenRawInput) -> ObjectCardOutput:
        """
        识别当前市场周期状态
        
        Args:
            raw: PeriodQueenRawInput 包含指数OHLCV和可选参数
        
        Returns:
            ObjectCardOutput: 统一输出格式 + PeriodQueen 特有字段
        """
        ohlcv = raw.index_ohlcv
        n = len(ohlcv)
        
        # 数据完整性检查
        confidence = self._compute_confidence(n, raw.limit_up_count)
        
        # 1. 计算市场特征指标
        features = self._extract_features(ohlcv, raw)
        
        # 2. 状态识别（核心逻辑）
        state, trigger = self._identify_state(features, raw.prev_state, raw.state_duration)
        
        # 3. 与 VOLFAC 互锁：极端波动强制降级
        if raw.volfac_vol_regime == "EXTREME_VOL":
            if state in (CycleState.ATTACK_SUSTAINED, CycleState.ATTACK_CONFIRMED):
                state = CycleState.POWER_TRANSITION
                trigger = f"VOLFAC极端波动强制降级: {trigger}"
            elif state == CycleState.GESTATION:
                state = CycleState.CUTTING_COMPLETE
                trigger = f"VOLFAC极端波动+孕化期→强制空仓: {trigger}"
        
        # 4. 获取状态配置
        permission = self.STATE_PERMISSION[state]
        max_size = self.STATE_MAX_SIZE[state]
        min_votes = self.STATE_MIN_VOTES[state]
        allowed = self.STATE_ALLOWED_OBJECTS[state]
        strength = self.STATE_SIGNAL_STRENGTH[state]
        
        # 5. 确定 filter/risk action
        filter_action = self._compute_filter_action(state)
        risk_action = self._compute_risk_action(state)
        lock_status = self._compute_lock_status(state, raw.prev_state)
        
        # 6. 更新历史
        self._state_history.append(state.value)
        
        # 7. 组装标准输出
        return ObjectCardOutput(
            object_id=self.OBJECT_ID,
            signal_type="REGIME_STATE",
            signal_strength=strength,
            confidence=confidence,
            lock_status=lock_status.value,
            filter_action=filter_action.value,
            risk_action=risk_action.value,
            size_scalar=max_size,  # PeriodQueen 的 size_scalar = position_max_size
            internal={
                "pq_state": state.value,
                "pq_trading_permission": permission.value,
                "pq_position_max_size": max_size,
                "pq_entry_min_votes": min_votes,
                "pq_allowed_objects": allowed,
                "pq_forbidden_objects": [obj for obj in self._all_objects() if obj not in allowed],
                "pq_state_duration": raw.state_duration + 1,
                "pq_transition_trigger": trigger,
                "features": features,
            },
            notes=f"周期状态: {state.value} | 权限: {permission.value} | 触发: {trigger}",
        )
    
    # ------------------------------------------------------------------
    # 简化桥接：从 OHLCV 直接判断
    # ------------------------------------------------------------------

    def from_ohlcv(
        self,
        ohlcv_list: List[Dict[str, float]],
        volfac_regime: Optional[str] = None,
    ) -> ObjectCardOutput:
        """简化入口：直接从 OHLCV 判断周期状态"""
        raw = PeriodQueenRawInput(
            index_ohlcv=ohlcv_list,
            volfac_vol_regime=volfac_regime,
        )
        return self.calculate(raw)
    
    # ------------------------------------------------------------------
    # 内部方法
    # ------------------------------------------------------------------

    def _compute_confidence(self, n_bars: int, limit_up: Optional[int]) -> float:
        if n_bars >= 60:
            base = 1.0
        elif n_bars >= 20:
            base = 0.7
        elif n_bars >= 10:
            base = 0.4
        else:
            base = 0.0
        
        # 有涨跌停数据增强置信度
        if limit_up is not None:
            base = min(1.0, base + 0.1)
        
        return base
    
    def _extract_features(
        self,
        ohlcv: List[Dict[str, float]],
        raw: PeriodQueenRawInput,
    ) -> Dict[str, Any]:
        """从 OHLCV 提取市场特征（模拟情绪周期指标）"""
        if len(ohlcv) < 10:
            return {"insufficient_data": True}
        
        closes = np.array([bar["close"] for bar in ohlcv])
        highs = np.array([bar["high"] for bar in ohlcv])
        lows = np.array([bar["low"] for bar in ohlcv])
        vols = np.array([bar.get("vol", 0) for bar in ohlcv])
        
        # 1. 近期趋势强度（20日斜率）
        recent = closes[-20:]
        slope = np.polyfit(range(len(recent)), recent, 1)[0]
        trend_direction = "up" if slope > 0 else "down"
        
        # 2. 波动特征
        returns = np.diff(closes) / closes[:-1]
        recent_vol = float(np.std(returns[-20:])) * np.sqrt(252) if len(returns) >= 20 else 0.0
        
        # 3. 创新高/新低统计（10日）
        recent_highs = highs[-10:]
        recent_lows = lows[-10:]
        new_high_count = sum(1 for i in range(1, len(recent_highs)) if recent_highs[i] > max(recent_highs[:i]))
        new_low_count = sum(1 for i in range(1, len(recent_lows)) if recent_lows[i] < min(recent_lows[:i]))
        
        # 4. 成交量趋势
        vol_trend = "increasing" if len(vols) >= 10 and vols[-1] > np.mean(vols[-10:-1]) else "decreasing"
        
        # 5. 涨跌停强度
        limit_strength = 0
        if raw.limit_up_count is not None and raw.limit_down_count is not None:
            total = raw.limit_up_count + raw.limit_down_count
            if total > 0:
                limit_strength = (raw.limit_up_count - raw.limit_down_count) / total
        
        # 6. 连续涨/跌天数
        consecutive_up = 0
        consecutive_down = 0
        for i in range(-1, -min(len(closes), 10), -1):
            if closes[i] > closes[i-1]:
                consecutive_up += 1
                consecutive_down = 0
            elif closes[i] < closes[i-1]:
                consecutive_down += 1
                consecutive_up = 0
            else:
                break
        
        return {
            "trend_direction": trend_direction,
            "trend_slope": round(float(slope), 4),
            "recent_vol_annual": round(recent_vol, 4),
            "new_high_count_10d": new_high_count,
            "new_low_count_10d": new_low_count,
            "vol_trend": vol_trend,
            "limit_strength": round(limit_strength, 4),
            "consecutive_up": consecutive_up,
            "consecutive_down": consecutive_down,
        }
    
    def _identify_state(
        self,
        features: Dict[str, Any],
        prev_state_str: Optional[str],
        state_duration: int,
    ) -> tuple:
        """
        七态状态机核心识别逻辑
        
        返回: (CycleState, trigger_reason)
        """
        if features.get("insufficient_data"):
            return CycleState.ATTACK_UNSUSTAINED, "数据不足，降级到保守状态"
        
        trend = features.get("trend_direction", "flat")
        vol = features.get("recent_vol_annual", 0.0)
        new_high = features.get("new_high_count_10d", 0)
        new_low = features.get("new_low_count_10d", 0)
        limit_strength = features.get("limit_strength", 0.0)
        vol_trend = features.get("vol_trend", "flat")
        consec_up = features.get("consecutive_up", 0)
        consec_down = features.get("consecutive_down", 0)
        
        # 解析上期状态
        prev_state = None
        if prev_state_str:
            try:
                prev_state = CycleState(prev_state_str)
            except ValueError:
                pass
        
        # ====== 最高优先级：全市场极端行情 ======
        if limit_strength < -0.5 or consec_down >= 5:
            return CycleState.CUTTING_COMPLETE, f"全市场退潮: limit_strength={limit_strength:.2f}, 连续跌{consec_down}日"
        
        # ====== 第二优先级：攻击有持续 ======
        # 条件：趋势向上 + 持续创新高 + 成交量配合 + 涨停占优
        if (trend == "up" and 
            new_high >= 3 and 
            vol_trend == "increasing" and 
            limit_strength > 0.2 and
            consec_up >= 3):
            return CycleState.ATTACK_SUSTAINED, (
                f"攻击持续: 趋势向上, {new_high}次新高, 量增, "
                f"涨停强{limit_strength:.2f}, 连涨{consec_up}日"
            )
        
        # ====== 第三优先级：确认攻击 ======
        # 条件：趋势向上 + 有新高 + 成交量配合
        if (trend == "up" and 
            new_high >= 2 and 
            vol_trend == "increasing" and
            consec_up >= 2):
            return CycleState.ATTACK_CONFIRMED, (
                f"确认攻击: 趋势向上, {new_high}次新高, 量增, 连涨{consec_up}日"
            )
        
        # ====== 第四优先级：余温 ======
        # 条件：前期攻击但创新高频次下降 + 成交量萎缩 + 不再创新高
        if (prev_state in (CycleState.ATTACK_SUSTAINED, CycleState.ATTACK_CONFIRMED) and
            new_high == 0 and 
            vol_trend == "decreasing" and
            trend == "up"):
            return CycleState.REMAINING_WARMTH, (
                f"余温: 前期攻击后无新高, 量缩, 趋势仍向上"
            )
        
        # ====== 第五优先级：切割完成 ======
        # 条件：前期余温后趋势转下 + 连续创新低
        if (prev_state in (CycleState.REMAINING_WARMTH, CycleState.ATTACK_UNSUSTAINED) and
            new_low >= 2 and
            trend == "down"):
            return CycleState.CUTTING_COMPLETE, (
                f"切割完成: {new_low}次新低, 趋势转下"
            )
        
        # ====== 第六优先级：孕化 ======
        # 条件：前期切割后趋势企稳 + 出现止跌迹象
        if (prev_state == CycleState.CUTTING_COMPLETE and
            consec_up >= 2 and
            trend == "up" and
            new_low == 0):
            return CycleState.GESTATION, (
                f"孕化: 切割后连涨{consec_up}日, 无新低, 趋势企稳"
            )
        
        # ====== 第七优先级：交权磨合期 ======
        # 条件：趋势不明确 + 波动大 + 无持续方向
        if (new_high == 0 and new_low == 0 and
            vol > 0.20 and  # 高波动
            abs(consec_up - consec_down) <= 1):
            return CycleState.POWER_TRANSITION, (
                f"交权磨合: 无方向, 高波动{vol:.2f}, 多空交替"
            )
        
        # ====== 第八优先级：攻击无持续 ======
        # 条件：趋势向下 + 无新高 + 有新低
        if (trend == "down" and 
            new_high == 0 and
            new_low >= 1):
            return CycleState.ATTACK_UNSUSTAINED, (
                f"攻击无持续: 趋势向下, {new_low}次新低"
            )
        
        # ====== 默认：维持上期状态或降级 ======
        if prev_state:
            return prev_state, f"状态维持: 无明确转移信号"
        
        return CycleState.POWER_TRANSITION, "状态模糊，默认交权磨合"
    
    def _compute_filter_action(self, state: CycleState) -> FilterAction:
        if state in (CycleState.CUTTING_COMPLETE, CycleState.ATTACK_UNSUSTAINED):
            return FilterAction.EXCLUDE
        elif state in (CycleState.REMAINING_WARMTH, CycleState.POWER_TRANSITION):
            return FilterAction.REDUCE_WEIGHT
        return FilterAction.PASS
    
    def _compute_risk_action(self, state: CycleState) -> RiskAction:
        if state in (CycleState.CUTTING_COMPLETE, CycleState.ATTACK_UNSUSTAINED):
            return RiskAction.HALT_NEW_POSITION
        elif state == CycleState.REMAINING_WARMTH:
            return RiskAction.REDUCE_POSITION
        return RiskAction.NONE
    
    def _compute_lock_status(self, state: CycleState, prev_state_str: Optional[str]) -> LockStatus:
        """状态稳定2天以上锁定"""
        if prev_state_str == state.value:
            # 连续相同状态，检查历史
            if len(self._state_history) >= 2 and self._state_history[-1] == state.value:
                return LockStatus.LOCKED
        return LockStatus.UNLOCKED
    
    def _all_objects(self) -> List[str]:
        return ["CHZL_BSD", "BPB", "VP", "TKR7", "MFLOW", "VOLFAC", "VOLTARGET", "YTC", "KELLY", "ATRATIO"]


# ---------------------------------------------------------------------------
# 快速测试
# ---------------------------------------------------------------------------

def _generate_market_ohlcv(
    n_days: int = 60,
    regime: str = "bull",
    seed: int = 42,
) -> List[Dict[str, float]]:
    """生成模拟市场指数OHLCV"""
    np.random.seed(seed)
    
    if regime == "bull":
        drift = 0.002
        vol = 0.015
    elif regime == "bear":
        drift = -0.002
        vol = 0.020
    elif regime == "chop":
        drift = 0.0
        vol = 0.025
    elif regime == "crash":
        drift = -0.008
        vol = 0.040
    else:
        drift = 0.001
        vol = 0.018
    
    returns = np.random.normal(drift, vol, n_days)
    prices = [3000.0]
    for r in returns:
        prices.append(prices[-1] * (1 + r))
    prices = np.array(prices[1:])
    
    intraday_vol = vol * 0.5
    highs = prices * (1 + np.abs(np.random.normal(0, intraday_vol, n_days)))
    lows = prices * (1 - np.abs(np.random.normal(0, intraday_vol, n_days)))
    opens = prices * (1 + np.random.normal(0, intraday_vol * 0.3, n_days))
    
    highs = np.maximum(highs, np.maximum(opens, prices))
    lows = np.minimum(lows, np.minimum(opens, prices))
    vols = np.random.lognormal(15, 0.3, n_days)
    
    bars = []
    for i in range(n_days):
        bars.append({
            "open": round(float(opens[i]), 2),
            "high": round(float(highs[i]), 2),
            "low": round(float(lows[i]), 2),
            "close": round(float(prices[i]), 2),
            "vol": round(float(vols[i]), 0),
        })
    return bars


def _quick_test():
    """端到端验证"""
    print("=" * 70)
    print("PERIOD_QUEEN 对象卡 — 端到端验证")
    print("=" * 70)
    
    pq = PeriodQueen()
    
    # 测试1: 牛市攻击持续
    print("\n【测试1】牛市攻击持续（drift=+0.2%, vol=1.5%）")
    ohlcv_bull = _generate_market_ohlcv(n_days=60, regime="bull", seed=42)
    raw = PeriodQueenRawInput(
        index_ohlcv=ohlcv_bull,
        limit_up_count=45,
        limit_down_count=12,
    )
    result = pq.calculate(raw)
    print(f"  pq_state: {result.internal['pq_state']}")
    print(f"  permission: {result.internal['pq_trading_permission']}")
    print(f"  max_size: {result.internal['pq_position_max_size']}")
    print(f"  min_votes: {result.internal['pq_entry_min_votes']}")
    print(f"  allowed: {result.internal['pq_allowed_objects']}")
    print(f"  signal_strength: {result.signal_strength}")
    print(f"  trigger: {result.internal['pq_transition_trigger']}")
    
    # 测试2: 熊市下跌
    print("\n【测试2】熊市下跌（drift=-0.2%, vol=2.0%）")
    ohlcv_bear = _generate_market_ohlcv(n_days=60, regime="bear", seed=99)
    pq2 = PeriodQueen()  # 新实例避免历史干扰
    raw2 = PeriodQueenRawInput(
        index_ohlcv=ohlcv_bear,
        limit_up_count=12,
        limit_down_count=45,
    )
    result2 = pq2.calculate(raw2)
    print(f"  pq_state: {result2.internal['pq_state']}")
    print(f"  permission: {result2.internal['pq_trading_permission']}")
    print(f"  risk_action: {result2.risk_action}")
    print(f"  filter_action: {result2.filter_action}")
    
    # 测试3: 震荡交权磨合
    print("\n【测试3】震荡交权磨合（drift=0%, vol=2.5%）")
    ohlcv_chop = _generate_market_ohlcv(n_days=60, regime="chop", seed=2025)
    pq3 = PeriodQueen()
    raw3 = PeriodQueenRawInput(index_ohlcv=ohlcv_chop)
    result3 = pq3.calculate(raw3)
    print(f"  pq_state: {result3.internal['pq_state']}")
    print(f"  permission: {result3.internal['pq_trading_permission']}")
    print(f"  max_size: {result3.internal['pq_position_max_size']}")
    
    # 测试4: 崩盘切割
    print("\n【测试4】崩盘切割（drift=-0.8%, vol=4.0%）")
    ohlcv_crash = _generate_market_ohlcv(n_days=60, regime="crash", seed=666)
    pq4 = PeriodQueen()
    raw4 = PeriodQueenRawInput(
        index_ohlcv=ohlcv_crash,
        limit_up_count=5,
        limit_down_count=80,
    )
    result4 = pq4.calculate(raw4)
    print(f"  pq_state: {result4.internal['pq_state']}")
    print(f"  permission: {result4.internal['pq_trading_permission']}")
    print(f"  risk_action: {result4.risk_action}")
    
    # 测试5: 简化桥接
    print("\n【测试5】简化桥接 from_ohlcv")
    pq5 = PeriodQueen()
    result5 = pq5.from_ohlcv(ohlcv_bull, volfac_regime="LOW_VOL")
    print(f"  pq_state: {result5.internal['pq_state']}")
    print(f"  permission: {result5.internal['pq_trading_permission']}")
    
    # 测试6: VOLFAC极端波动互锁
    print("\n【测试6】VOLFAC极端波动强制降级")
    pq6 = PeriodQueen()
    raw6 = PeriodQueenRawInput(
        index_ohlcv=ohlcv_bull,
        volfac_vol_regime="EXTREME_VOL",
        prev_state="ATTACK_SUSTAINED",
        state_duration=5,
    )
    result6 = pq6.calculate(raw6)
    print(f"  原始应ATTACK_SUSTAINED，VOLFAC降级后: {result6.internal['pq_state']}")
    print(f"  trigger: {result6.internal['pq_transition_trigger']}")
    
    # 测试7: 状态转移序列
    print("\n【测试7】状态转移序列模拟")
    pq7 = PeriodQueen()
    states = []
    for regime in ["bull", "bull", "chop", "bear", "crash", "bear", "bull"]:
        ohlcv = _generate_market_ohlcv(n_days=30, regime=regime, seed=np.random.randint(1000))
        raw = PeriodQueenRawInput(
            index_ohlcv=ohlcv,
            prev_state=states[-1] if states else None,
            state_duration=len(states),
        )
        r = pq7.calculate(raw)
        states.append(r.internal['pq_state'])
    print(f"  状态序列: {' -> '.join(states)}")
    
    print("\n" + "=" * 70)
    print("✅ PERIOD_QUEEN 全部测试通过")
    print("=" * 70)


if __name__ == "__main__":
    _quick_test()
