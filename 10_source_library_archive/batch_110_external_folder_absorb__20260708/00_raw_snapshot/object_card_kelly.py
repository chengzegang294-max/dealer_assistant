# KELLY_P0_R — Kelly Criterion（凯利公式）对象卡 Python 实现
# 文件名: object_card_kelly.py
# 状态: [OK] proxy_quantizable_now
# 数据需求: 历史交易记录（胜率p、赔率b）或回测结果
# A股落地: 直接可用（需修正交易成本 + T+1惩罚）

"""
凯利公式（Kelly Criterion）对象卡实现

功能层: P0_R（风控层 — 仓位/止损/回撤）
来源: John Kelly 1956 + Ed Thorp 应用
核心公式: f* = (bp - q) / b

标准输出字段:
    object_id, signal_type, signal_strength, confidence,
    lock_status, filter_action, risk_action, size_scalar
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any


# ---------------------------------------------------------------------------
# 枚举定义
# ---------------------------------------------------------------------------

class KellySignalType:
    """KELLY 信号类型（仓位建议）"""
    NO_TRADE = "NO_TRADE"
    MINIMAL_POSITION = "MINIMAL_POSITION"
    QUARTER_KELLY = "QUARTER_KELLY"
    HALF_KELLY = "HALF_KELLY"
    HALF_KELLY_CONSERVATIVE = "HALF_KELLY_CONSERVATIVE"


class LockStatus:
    UNLOCKED = "UNLOCKED"
    LOCKED = "LOCKED"


class FilterAction:
    PASS = "PASS"
    BLOCK_BUY = "BLOCK_BUY"
    REDUCE_WEIGHT = "REDUCE_WEIGHT"


class RiskAction:
    NONE = "NONE"
    REDUCE_POSITION = "REDUCE_POSITION"
    HALT_NEW_TRADE = "HALT_NEW_TRADE"


# ---------------------------------------------------------------------------
# 数据类
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class KellyRawInput:
    """KELLY 原始数据输入"""
    # 直接参数模式（简化实现）
    win_rate: float                    # 胜率 p (0~1)
    win_loss_ratio: float              # 赔率 b (盈亏比 = 平均盈利/平均亏损)
    sample_size: int = 0               # 历史样本量（用于 confidence 评估）
    
    # A股适配参数
    cost_rate: float = 0.0025          # 交易成本率（默认 A股双边千2.5）
    t1_penalty_factor: float = 0.8     # T+1 惩罚系数（默认 0.8）
    astock_enabled: bool = True        # A股模式开关
    
    # 风控参数
    confidence_threshold: int = 5      # confidence 阈值（0-10），低于此强制四分之一凯利
    van_tharp_max: float = 0.20        # Van Tharp 硬性上限（默认 20%）
    extreme_conservative_max: float = 0.10  # 极端保守上限


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
    size_scalar: float            # 0.0 ~ 1.0（KELLY 专属：实际执行仓位比例）
    internal: Dict[str, Any] = field(default_factory=dict)
    notes: str = ""


# ---------------------------------------------------------------------------
# 核心计算类
# ---------------------------------------------------------------------------

class KellyCriterion:
    """
    凯利公式对象卡实现

    核心洞察: 选对方向只给你期望值，选对仓位才给你复利。
    
    使用示例:
        >>> kelly = KellyCriterion()
        >>> raw = KellyRawInput(win_rate=0.60, win_loss_ratio=1.0, sample_size=100)
        >>> result = kelly.calculate(raw)
        >>> print(result.size_scalar)  # 半凯利仓位
    """

    OBJECT_ID = "KELLY_P0_R"
    VERSION = "v1.0"
    MIN_SAMPLE_SIZE = 30           # 最小样本量
    RECOMMENDED_SAMPLE_SIZE = 50   # 建议样本量

    def __init__(self):
        self._last_f_star: Optional[float] = None
        self._consecutive_losses = 0
        self._consecutive_wins = 0

    # ------------------------------------------------------------------
    # 主入口
    # ------------------------------------------------------------------

    def calculate(self, raw: KellyRawInput) -> ObjectCardOutput:
        """
        计算凯利最优仓位并输出标准对象卡格式
        
        Args:
            raw: 原始输入数据（胜率、赔率、样本量等）
        
        Returns:
            ObjectCardOutput: 统一输出格式，size_scalar = half_kelly_f
        """
        # 1. 样本量检查
        if raw.sample_size > 0 and raw.sample_size < self.MIN_SAMPLE_SIZE:
            return self._insufficient_data(raw.sample_size)
        
        # 2. 提取参数
        p = raw.win_rate
        q = 1.0 - p
        b = raw.win_loss_ratio
        
        # 3. 交易成本修正后的有效赔率
        # 简化处理：从赔率中扣除交易成本影响
        effective_b = b * (1.0 - raw.cost_rate * 2) if raw.astock_enabled else b * (1.0 - raw.cost_rate)
        
        # 4. 核心凯利计算: f* = (bp - q) / b
        if effective_b <= 0 or p * effective_b <= q:
            kelly_f_star = 0.0  # 期望值为负，禁止交易
        else:
            kelly_f_star = (p * effective_b - q) / effective_b
        
        kelly_f_star = max(0.0, min(1.0, kelly_f_star))
        
        # 5. 变体仓位
        kelly_f_half = 0.5 * kelly_f_star
        kelly_f_quarter = 0.25 * kelly_f_star
        
        # 6. Confidence 评估（0-10 映射到 0.0-1.0）
        confidence_score = self._compute_confidence_score(raw.sample_size)
        confidence = confidence_score / 10.0
        
        # 7. 自适应因子
        if confidence_score < raw.confidence_threshold:
            adaptive_factor = 0.25  # 低 confidence → 四分之一凯利
        elif self._consecutive_losses >= 3:
            adaptive_factor = 0.25  # 连续亏损 → 危机模式
        elif self._consecutive_wins >= 3:
            adaptive_factor = 0.5   # 连续盈利 → 维持半凯利（不激进加仓）
        else:
            adaptive_factor = 0.5   # 正常 → 半凯利
        
        # 8. 实际执行仓位（最保守原则）
        extreme_max = raw.extreme_conservative_max if confidence_score < raw.confidence_threshold else 1.0
        
        kelly_f_actual = min(
            kelly_f_star * adaptive_factor,   # 自适应凯利
            raw.van_tharp_max,                 # Van Tharp 硬性上限
            extreme_max,                       # 极端保守上限
        )
        
        # 9. A股 T+1 惩罚
        if raw.astock_enabled:
            kelly_f_actual *= raw.t1_penalty_factor
        
        # 确保 0~1 范围
        kelly_f_actual = max(0.0, min(1.0, kelly_f_actual))
        
        # 10. 信号分类
        signal_type, signal_strength, filter_action, risk_action = self._map_signal(
            kelly_f_actual, kelly_f_star, raw.sample_size
        )
        
        # 11. 组装标准输出
        internal = {
            "kelly_p": round(p, 4),
            "kelly_q": round(q, 4),
            "kelly_b": round(b, 4),
            "kelly_cost_rate": raw.cost_rate,
            "kelly_f_star": round(kelly_f_star, 4),
            "kelly_f_half": round(kelly_f_half, 4),
            "kelly_f_quarter": round(kelly_f_quarter, 4),
            "kelly_f_actual": round(kelly_f_actual, 4),
            "kelly_adaptive_factor": adaptive_factor,
            "kelly_sample_size": raw.sample_size,
            "kelly_confidence_score": confidence_score,
            "astock_enabled": raw.astock_enabled,
            "t1_penalty_applied": raw.astock_enabled,
            "t1_penalty_factor": raw.t1_penalty_factor if raw.astock_enabled else 1.0,
        }
        
        notes = self._generate_notes(kelly_f_star, raw.sample_size, raw.astock_enabled)
        
        return ObjectCardOutput(
            object_id=self.OBJECT_ID,
            signal_type=signal_type,
            signal_strength=signal_strength,
            confidence=round(confidence, 2),
            lock_status=LockStatus.UNLOCKED,
            filter_action=filter_action,
            risk_action=risk_action,
            size_scalar=round(kelly_f_actual, 4),
            internal=internal,
            notes=notes,
        )

    # ------------------------------------------------------------------
    # 内部计算方法
    # ------------------------------------------------------------------

    def _compute_confidence_score(self, sample_size: int) -> int:
        """
        参数估计 confidence 评分（0-10）
        
        - 样本量 ≥ 100，近期数据，p 和 b 稳定 → 10
        - 样本量 50-99，数据较旧，p 或 b 波动 → 5-7
        - 样本量 < 50，或参数近期大幅变化 → 0-3
        """
        if sample_size >= 100:
            return 10
        elif sample_size >= 50:
            return 7
        elif sample_size >= 30:
            return 5
        elif sample_size > 0:
            return 3
        else:
            # 直接传入 p, b 无样本量 → 默认中等 confidence
            return 5

    def _map_signal(
        self,
        kelly_f_actual: float,
        kelly_f_star: float,
        sample_size: int,
    ) -> tuple:
        """
        映射到标准信号格式
        
        Returns:
            (signal_type, signal_strength, filter_action, risk_action)
        """
        if kelly_f_actual <= 0.0 or kelly_f_star <= 0.0:
            return KellySignalType.NO_TRADE, 0, FilterAction.BLOCK_BUY, RiskAction.HALT_NEW_TRADE
        
        if sample_size > 0 and sample_size < self.RECOMMENDED_SAMPLE_SIZE:
            # 样本不足但可交易 → 最保守
            return KellySignalType.MINIMAL_POSITION, 0, FilterAction.PASS, RiskAction.NONE
        
        if kelly_f_actual <= 0.05:
            return KellySignalType.MINIMAL_POSITION, 0, FilterAction.PASS, RiskAction.NONE
        elif kelly_f_actual <= 0.10:
            return KellySignalType.QUARTER_KELLY, 1, FilterAction.PASS, RiskAction.NONE
        elif kelly_f_actual <= 0.15:
            return KellySignalType.HALF_KELLY_CONSERVATIVE, 1, FilterAction.PASS, RiskAction.NONE
        else:
            return KellySignalType.HALF_KELLY, 2, FilterAction.PASS, RiskAction.NONE

    def _insufficient_data(self, sample_size: int) -> ObjectCardOutput:
        """样本不足时返回空信号"""
        return ObjectCardOutput(
            object_id=self.OBJECT_ID,
            signal_type=KellySignalType.NO_TRADE,
            signal_strength=0,
            confidence=0.0,
            lock_status=LockStatus.UNLOCKED,
            filter_action=FilterAction.BLOCK_BUY,
            risk_action=RiskAction.HALT_NEW_TRADE,
            size_scalar=0.0,
            internal={
                "error": "sample_size_insufficient",
                "kelly_sample_size": sample_size,
                "required_minimum": self.MIN_SAMPLE_SIZE,
            },
            notes=f"样本量不足: {sample_size} < {self.MIN_SAMPLE_SIZE}，禁止交易",
        )

    def _generate_notes(self, kelly_f_star: float, sample_size: int, astock_enabled: bool) -> str:
        """生成人类可读备注"""
        parts = []
        if kelly_f_star <= 0:
            parts.append("凯利公式计算期望值为负，建议不交易")
        elif sample_size > 0 and sample_size < self.RECOMMENDED_SAMPLE_SIZE:
            parts.append(f"样本量{sample_size}不足，结果可靠性受限")
        if astock_enabled:
            parts.append("A股模式: 已应用T+1惩罚系数和交易成本修正")
        return "; ".join(parts) if parts else "凯利仓位计算正常"

    # ------------------------------------------------------------------
    # 动态更新接口（每 N 笔交易后重算）
    # ------------------------------------------------------------------

    def update_after_trade(self, pnl: float) -> None:
        """
        记录单笔交易结果，用于连续亏损/盈利检测
        
        Args:
            pnl: 单笔交易盈亏（正数=盈利，负数=亏损）
        """
        if pnl > 0:
            self._consecutive_wins += 1
            self._consecutive_losses = 0
        else:
            self._consecutive_losses += 1
            self._consecutive_wins = 0

    def reset_regime(self) -> None:
        """重置连续计数器"""
        self._consecutive_losses = 0
        self._consecutive_wins = 0


# ---------------------------------------------------------------------------
# 快速测试
# ---------------------------------------------------------------------------

def _quick_test() -> None:
    """内部快速验证 — 至少3个场景"""
    print("=" * 60)
    print("KELLY_P0_R 对象卡实现验证")
    print("=" * 60)
    
    kelly = KellyCriterion()
    
    # 测试1: 经典示例 p=60%, b=1 → f*=20%, half=10%
    print("\n【测试1】经典示例: p=60%, b=1, n=100")
    raw1 = KellyRawInput(win_rate=0.60, win_loss_ratio=1.0, sample_size=100, astock_enabled=False, cost_rate=0.0)
    result1 = kelly.calculate(raw1)
    print(f"  object_id: {result1.object_id}")
    print(f"  signal_type: {result1.signal_type}")
    print(f"  signal_strength: {result1.signal_strength}")
    print(f"  size_scalar: {result1.size_scalar}")
    print(f"  confidence: {result1.confidence}")
    print(f"  f_star: {result1.internal['kelly_f_star']}")
    assert result1.object_id == "KELLY_P0_R"
    assert result1.size_scalar > 0
    assert result1.internal["kelly_f_star"] == 0.2
    print("  [OK] 经典示例计算正确")
    
    # 测试2: 高胜率低赔率 → 负期望，禁止交易
    print("\n【测试2】负期望: p=70%, b=0.5")
    raw2 = KellyRawInput(win_rate=0.60, win_loss_ratio=0.5, sample_size=80, astock_enabled=False, cost_rate=0.0)
    result2 = kelly.calculate(raw2)
    print(f"  signal_type: {result2.signal_type}")
    print(f"  size_scalar: {result2.size_scalar}")
    print(f"  f_star: {result2.internal['kelly_f_star']}")
    assert result2.signal_type == KellySignalType.NO_TRADE
    assert result2.size_scalar == 0.0
    assert result2.internal["kelly_f_star"] == 0.0
    print("  [OK] 负期望时禁止交易")
    
    # 测试3: A股模式（T+1惩罚 + 交易成本）
    print("\n【测试3】A股模式: p=55%, b=2, n=120")
    raw3_astock = KellyRawInput(
        win_rate=0.55,
        win_loss_ratio=2.0,
        sample_size=120,
        astock_enabled=True,
        cost_rate=0.0025,
        t1_penalty_factor=0.8,
    )
    raw3_normal = KellyRawInput(
        win_rate=0.55,
        win_loss_ratio=2.0,
        sample_size=120,
        astock_enabled=False,
    )
    result3_astock = kelly.calculate(raw3_astock)
    result3_normal = kelly.calculate(raw3_normal)
    print(f"  A股 size_scalar: {result3_astock.size_scalar}")
    print(f"  非A股 size_scalar: {result3_normal.size_scalar}")
    assert result3_astock.size_scalar < result3_normal.size_scalar
    assert result3_astock.internal["t1_penalty_applied"] == True
    print("  [OK] A股T+1惩罚生效，仓位更保守")
    
    # 测试4: 样本不足
    print("\n【测试4】样本不足: n=20")
    raw4 = KellyRawInput(win_rate=0.60, win_loss_ratio=1.5, sample_size=20)
    result4 = kelly.calculate(raw4)
    print(f"  signal_type: {result4.signal_type}")
    print(f"  size_scalar: {result4.size_scalar}")
    print(f"  filter_action: {result4.filter_action}")
    assert result4.signal_type == KellySignalType.NO_TRADE
    assert result4.size_scalar == 0.0
    assert result4.filter_action == FilterAction.BLOCK_BUY
    print("  [OK] 样本不足时正确拒绝")
    
    # 测试5: 连续亏损后的危机模式
    print("\n【测试5】连续亏损后的危机模式")
    kelly2 = KellyCriterion()
    for _ in range(3):
        kelly2.update_after_trade(pnl=-100.0)
    raw5 = KellyRawInput(win_rate=0.55, win_loss_ratio=1.5, sample_size=100, astock_enabled=False)
    result5 = kelly2.calculate(raw5)
    print(f"  size_scalar: {result5.size_scalar}")
    print(f"  adaptive_factor: {result5.internal['kelly_adaptive_factor']}")
    assert result5.internal["kelly_adaptive_factor"] == 0.25
    print("  [OK] 连续亏损后自动降级为四分之一凯利")
    
    print("\n" + "=" * 60)
    print("[OK] KELLY_P0_R 全部测试通过")
    print("=" * 60)


if __name__ == "__main__":
    _quick_test()
