# INSTB_P0_A — 机构行为因子（Institutional Behavior）对象卡 Python 实现
# 文件名: object_card_instb.py
# 状态: needs_extra_data（季频滞后，数据获取成本高）
# A 股落地: 方法层可用，支持季报数据 + OHLCV 量价模拟降级

"""
机构行为因子对象卡实现

功能层: P0_A（选股层 / 方法层）
来源: 华泰证券《多因子系列 8：单因子测试之机构行为因子》
SBKT_F007 固化结论: 核心因子 instb_holder_change_pct，持仓调整期约 30 个交易日

标准输出字段:
    object_id, signal_type, signal_strength, confidence,
    lock_status, filter_action, risk_action, size_scalar

使用原则:
    - INSTB 不直接干预 KD/缠论/TK 等执行层信号
    - 仅作为背景信息，辅助判断行业偏好和选股池构建
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# 枚举定义
# ---------------------------------------------------------------------------

class InstbSignal(Enum):
    NONE = "NONE"
    ACCUMULATION = "ACCUMULATION"
    DISTRIBUTION = "DISTRIBUTION"
    FUND_INFLOW = "FUND_INFLOW"
    FUND_OUTFLOW = "FUND_OUTFLOW"


class FilterAction(Enum):
    PASS = "PASS"
    CONTEXT_ONLY = "CONTEXT_ONLY"
    ENHANCE = "ENHANCE"
    DOWNGRADE = "DOWNGRADE"
    BLOCK = "BLOCK"


class RiskAction(Enum):
    NONE = "NONE"
    REDUCE_POSITION = "REDUCE_POSITION"


class LockStatus(Enum):
    UNLOCKED = "UNLOCKED"
    LOCKED = "LOCKED"


class SignalFreshness(Enum):
    FRESH = "FRESH"
    STALE = "STALE"
    OUTDATED = "OUTDATED"


# ---------------------------------------------------------------------------
# 数据类
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class InstbQuarterlyInput:
    """季报机构持仓数据（Wind / 同花顺 F10）"""
    instb_total_inst_pct: Optional[float] = None       # 本季度机构总持仓占比
    instb_prev_quarter_total: Optional[float] = None   # 上季度机构总持仓占比
    instb_shareholder_count: Optional[int] = None      # 本季度股东户数
    instb_prev_shareholder_count: Optional[int] = None # 上季度股东户数
    instb_fund_holding_pct: Optional[float] = None     # 本季度公募基金持仓占比
    prev_quarter_fund_pct: Optional[float] = None      # 上季度公募基金持仓占比
    report_date: Optional[str] = None                  # 季报披露日期 (YYYY-MM-DD)


@dataclass(frozen=True)
class InstbSimulatedInput:
    """OHLCV 模拟输入（无季报数据时使用）"""
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
    prev_close: float
    volume_5d_avg: float
    volume_20d_avg: Optional[float] = None
    close_20d: Optional[List[float]] = None


@dataclass(frozen=True)
class InstbInternal:
    """INSTB 内部计算结果"""
    holder_change_pct: float      # 机构持仓变动百分比
    concentration_change: float   # 筹码集中度变化
    fund_flow_trend: str          # 基金流向趋势
    data_lag_days: int            # 数据滞后天数
    signal_freshness: str         # 信号新鲜度
    composite_score: float        # 综合评分 0.0-1.0
    data_mode: str                # 'quarterly' 或 'simulated'


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

class InstitutionalBehaviorFactor:
    """
    机构行为因子对象卡实现

    使用示例（季报数据）:
        >>> instb = InstitutionalBehaviorFactor()
        >>> q = InstbQuarterlyInput(instb_total_inst_pct=0.35, instb_prev_quarter_total=0.30, ...)
        >>> result = instb.calculate(quarterly_data=q, current_date=datetime.now())

    使用示例（OHLCV 模拟）:
        >>> sim = InstbSimulatedInput(open=10.0, high=10.5, low=9.8, close=10.2, ...)
        >>> result = instb.calculate(simulated_data=sim)
    """

    OBJECT_ID = "INSTB_P0_A"
    HOLDER_CHANGE_ACCUM = 0.05     # 机构增持阈值
    HOLDER_CHANGE_DIST = -0.05     # 机构减持阈值
    CONCENTRATION_ACCUM = 1.10     # 筹码集中阈值
    CONCENTRATION_DIST = 0.90      # 筹码分散阈值
    FUND_CHANGE_STRONG_IN = 0.05   # 基金大幅增持阈值
    FUND_CHANGE_MODERATE_IN = 0.02
    FUND_CHANGE_MODERATE_OUT = -0.02
    FUND_CHANGE_STRONG_OUT = -0.05
    LAG_FRESH = 15                 # 新鲜度阈值
    LAG_STALE = 45

    def __init__(self):
        self._last_scores: List[float] = []
        self._TREND_LOOKBACK = 3

    # ------------------------------------------------------------------
    # 主入口
    # ------------------------------------------------------------------

    def calculate(
        self,
        quarterly_data: Optional[InstbQuarterlyInput] = None,
        simulated_data: Optional[InstbSimulatedInput] = None,
        current_date: Optional[datetime] = None,
    ) -> ObjectCardOutput:
        """
        计算机构行为因子并输出标准对象卡格式

        Args:
            quarterly_data: 季报机构持仓数据（优先）
            simulated_data: OHLCV 模拟数据（降级）
            current_date: 当前日期（用于计算季报滞后）

        Returns:
            ObjectCardOutput: 统一输出格式
        """
        if quarterly_data is not None and self._has_quarterly_data(quarterly_data):
            internal = self._compute_from_quarterly(quarterly_data, current_date or datetime.now())
            confidence = 1.0 if internal.signal_freshness == "FRESH" else (
                0.7 if internal.signal_freshness == "STALE" else 0.3
            )
        elif simulated_data is not None:
            internal = self._compute_from_simulated(simulated_data)
            confidence = 0.5  # 模拟数据置信度更低
        else:
            return ObjectCardOutput(
                object_id=self.OBJECT_ID,
                signal_type=InstbSignal.NONE.value,
                signal_strength=0,
                confidence=0.0,
                lock_status=LockStatus.UNLOCKED.value,
                filter_action=FilterAction.PASS.value,
                risk_action=RiskAction.NONE.value,
                size_scalar=1.0,
                internal={"data_mode": "none", "error": "no data provided"},
                notes="未提供任何输入数据，信号不可用",
            )

        # 更新历史综合评分（用于锁定判断）
        self._last_scores.append(internal.composite_score)
        if len(self._last_scores) > self._TREND_LOOKBACK:
            self._last_scores.pop(0)

        # 信号生成
        signal_type, signal_strength, filter_action = self._generate_signal(internal)

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
                "holder_change_pct": round(internal.holder_change_pct, 4),
                "concentration_change": round(internal.concentration_change, 4),
                "fund_flow_trend": internal.fund_flow_trend,
                "data_lag_days": internal.data_lag_days,
                "signal_freshness": internal.signal_freshness,
                "composite_score": round(internal.composite_score, 4),
                "data_mode": internal.data_mode,
            },
            notes=self._generate_notes(internal, confidence),
        )

    # ------------------------------------------------------------------
    # 内部计算方法
    # ------------------------------------------------------------------

    def _has_quarterly_data(self, q: InstbQuarterlyInput) -> bool:
        """检查是否具备足够季报数据"""
        return (
            q.instb_total_inst_pct is not None
            and q.instb_prev_quarter_total is not None
            and q.instb_prev_quarter_total > 0
        )

    def _compute_from_quarterly(
        self, q: InstbQuarterlyInput, current_date: datetime
    ) -> InstbInternal:
        """基于季报数据计算机构行为因子"""
        # 1. 机构持仓变动百分比
        holder_change_pct = (
            (q.instb_total_inst_pct - q.instb_prev_quarter_total)
            / q.instb_prev_quarter_total
        )

        # 2. 筹码集中度变化
        if q.instb_shareholder_count and q.instb_prev_shareholder_count and q.instb_shareholder_count > 0:
            concentration_change = q.instb_prev_shareholder_count / q.instb_shareholder_count
        else:
            concentration_change = 1.0

        # 3. 基金流向趋势
        fund_change = 0.0
        if q.instb_fund_holding_pct is not None and q.prev_quarter_fund_pct is not None:
            fund_change = q.instb_fund_holding_pct - q.prev_quarter_fund_pct
        fund_flow_trend = self._classify_fund_flow(fund_change)

        # 4. 数据滞后天数与新鲜度
        data_lag_days = 999
        signal_freshness = "OUTDATED"
        if q.report_date:
            report_date = datetime.strptime(q.report_date, "%Y-%m-%d")
            data_lag_days = (current_date - report_date).days
            signal_freshness = self._classify_freshness(data_lag_days)

        # 5. 综合评分
        composite_score = 0.0
        if signal_freshness in ("FRESH", "STALE"):
            composite_score = (
                max(0, holder_change_pct) * 0.4
                + max(0, concentration_change - 1) * 0.3
                + (1 if fund_flow_trend in ("STRONG_INFLOW", "MODERATE_INFLOW") else 0) * 0.3
            )
            composite_score = min(1.0, composite_score)

        return InstbInternal(
            holder_change_pct=holder_change_pct,
            concentration_change=concentration_change,
            fund_flow_trend=fund_flow_trend,
            data_lag_days=data_lag_days,
            signal_freshness=signal_freshness,
            composite_score=composite_score,
            data_mode="quarterly",
        )

    def _compute_from_simulated(self, sim: InstbSimulatedInput) -> InstbInternal:
        """
        基于 OHLCV 量价关系模拟机构行为

        核心假设：
        - 放量滞涨（大成交量 + 小实体 K 线 + 上影线） → 机构派发 DISTRIBUTION
        - 缩量回调（成交量萎缩 + 小幅下跌） → 机构吸筹 ACCUMULATION（洗盘）
        - 放量突破（成交量放大 + 大阳线） → 机构建仓/加仓
        - 缩量上涨（成交量萎缩 + 阳线） → 机构锁仓，筹码稳定
        """
        # 价格变化
        price_change = (sim.close_price - sim.open_price) / sim.open_price if sim.open_price != 0 else 0.0
        daily_change = (sim.close_price - sim.prev_close) / sim.prev_close if sim.prev_close != 0 else 0.0
        body = abs(sim.close_price - sim.open_price)
        range_ = sim.high_price - sim.low_price
        body_ratio = body / range_ if range_ > 0 else 1.0
        upper_shadow = (sim.high_price - max(sim.open_price, sim.close_price)) / range_ if range_ > 0 else 0.0

        # 成交量比率
        vol_ratio_5d = sim.volume / sim.volume_5d_avg if sim.volume_5d_avg > 0 else 1.0
        vol_ratio_20d = sim.volume / sim.volume_20d_avg if sim.volume_20d_avg and sim.volume_20d_avg > 0 else vol_ratio_5d

        # 模拟机构持仓变动百分比
        # 放量滞涨 = 派发；缩量回调 = 吸筹
        if vol_ratio_5d > 1.5 and body_ratio < 0.3 and daily_change > -0.01:
            # 放量滞涨（十字星/小实体）→ 派发
            holder_change_pct = -0.08
        elif vol_ratio_5d > 1.3 and price_change > 0.02:
            # 放量突破大阳线 → 建仓
            holder_change_pct = 0.06
        elif vol_ratio_5d < 0.7 and daily_change < -0.01:
            # 缩量回调 → 洗盘吸筹
            holder_change_pct = 0.04
        elif vol_ratio_5d < 0.8 and daily_change > 0:
            # 缩量上涨 → 锁仓稳定
            holder_change_pct = 0.01
        else:
            holder_change_pct = 0.0

        # 模拟筹码集中度变化（基于量价配合）
        if vol_ratio_5d < 0.7 and abs(daily_change) < 0.02:
            # 缩量整理 → 筹码集中
            concentration_change = 1.15
        elif vol_ratio_5d > 1.5 and body_ratio < 0.3:
            # 放量滞涨 → 筹码分散（散户接盘）
            concentration_change = 0.85
        elif vol_ratio_5d > 1.3 and price_change > 0:
            # 放量突破 → 筹码集中（机构收集）
            concentration_change = 1.10
        else:
            concentration_change = 1.0

        # 基金流向趋势（基于模拟）
        if holder_change_pct > 0.05:
            fund_flow_trend = "STRONG_INFLOW"
        elif holder_change_pct > 0.02:
            fund_flow_trend = "MODERATE_INFLOW"
        elif holder_change_pct < -0.05:
            fund_flow_trend = "STRONG_OUTFLOW"
        elif holder_change_pct < -0.02:
            fund_flow_trend = "MODERATE_OUTFLOW"
        else:
            fund_flow_trend = "STABLE"

        # 综合评分
        composite_score = (
            max(0, holder_change_pct) * 0.4
            + max(0, concentration_change - 1) * 0.3
            + (1 if fund_flow_trend in ("STRONG_INFLOW", "MODERATE_INFLOW") else 0) * 0.3
        )
        composite_score = min(1.0, composite_score)

        return InstbInternal(
            holder_change_pct=holder_change_pct,
            concentration_change=concentration_change,
            fund_flow_trend=fund_flow_trend,
            data_lag_days=0,
            signal_freshness="FRESH",  # 模拟数据视为当日有效
            composite_score=composite_score,
            data_mode="simulated",
        )

    def _classify_fund_flow(self, fund_change: float) -> str:
        """分类基金流向趋势"""
        if fund_change > self.FUND_CHANGE_STRONG_IN:
            return "STRONG_INFLOW"
        elif fund_change > self.FUND_CHANGE_MODERATE_IN:
            return "MODERATE_INFLOW"
        elif fund_change > self.FUND_CHANGE_MODERATE_OUT:
            return "STABLE"
        elif fund_change > self.FUND_CHANGE_STRONG_OUT:
            return "MODERATE_OUTFLOW"
        else:
            return "STRONG_OUTFLOW"

    def _classify_freshness(self, lag_days: int) -> str:
        """分类信号新鲜度"""
        if lag_days < self.LAG_FRESH:
            return "FRESH"
        elif lag_days < self.LAG_STALE:
            return "STALE"
        else:
            return "OUTDATED"

    def _generate_signal(self, internal: InstbInternal) -> tuple[InstbSignal, int, FilterAction]:
        """
        生成机构行为信号

        返回: (signal_type, signal_strength, filter_action)
        注：INSTB 不直接干预执行层，filter_action 默认 PASS / CONTEXT_ONLY
        """
        # 数据过期 → 无信号
        if internal.signal_freshness == "OUTDATED" and internal.data_mode == "quarterly":
            return InstbSignal.NONE, 0, FilterAction.PASS

        # 机构吸筹（持仓增加 + 筹码集中）
        if internal.holder_change_pct > self.HOLDER_CHANGE_ACCUM and internal.concentration_change > self.CONCENTRATION_ACCUM:
            return InstbSignal.ACCUMULATION, +1, FilterAction.CONTEXT_ONLY

        # 机构派发（持仓减少 + 筹码分散）
        if internal.holder_change_pct < self.HOLDER_CHANGE_DIST and internal.concentration_change < self.CONCENTRATION_DIST:
            return InstbSignal.DISTRIBUTION, -1, FilterAction.CONTEXT_ONLY

        # 基金大幅流入
        if internal.fund_flow_trend in ("STRONG_INFLOW", "MODERATE_INFLOW"):
            return InstbSignal.FUND_INFLOW, +1, FilterAction.CONTEXT_ONLY

        # 基金大幅流出
        if internal.fund_flow_trend in ("STRONG_OUTFLOW", "MODERATE_OUTFLOW"):
            return InstbSignal.FUND_OUTFLOW, -1, FilterAction.CONTEXT_ONLY

        return InstbSignal.NONE, 0, FilterAction.PASS

    def _compute_lock_status(self, internal: InstbInternal) -> LockStatus:
        """连续 3 期综合评分同向且 >0.7 或 <0.3 则锁定"""
        if len(self._last_scores) < self._TREND_LOOKBACK:
            return LockStatus.UNLOCKED
        last3 = self._last_scores[-self._TREND_LOOKBACK:]
        if all(s > 0.7 for s in last3):
            return LockStatus.LOCKED
        if all(s < 0.3 for s in last3):
            return LockStatus.LOCKED
        return LockStatus.UNLOCKED

    def _compute_risk_action(self, internal: InstbInternal, signal_type: InstbSignal) -> RiskAction:
        """风险动作判断"""
        if signal_type == InstbSignal.DISTRIBUTION:
            return RiskAction.REDUCE_POSITION
        if signal_type == InstbSignal.FUND_OUTFLOW and internal.signal_freshness == "FRESH":
            return RiskAction.REDUCE_POSITION
        return RiskAction.NONE

    def _compute_size_scalar(self, internal: InstbInternal, signal_type: InstbSignal) -> float:
        """仓位缩放（方法层参考，幅度较小）"""
        if signal_type == InstbSignal.ACCUMULATION:
            return 1.1
        elif signal_type == InstbSignal.FUND_INFLOW:
            return 1.05
        elif signal_type == InstbSignal.DISTRIBUTION:
            return 0.8
        elif signal_type == InstbSignal.FUND_OUTFLOW:
            return 0.85
        return 1.0

    def _generate_notes(self, internal: InstbInternal, confidence: float) -> str:
        parts = []
        if internal.data_mode == "simulated":
            parts.append("使用 OHLCV 量价关系模拟机构行为")
        if internal.data_mode == "quarterly":
            parts.append(f"季报滞后 {internal.data_lag_days} 天，新鲜度: {internal.signal_freshness}")
        if internal.holder_change_pct != 0:
            direction = "增持" if internal.holder_change_pct > 0 else "减持"
            parts.append(f"模拟机构持仓变动: {internal.holder_change_pct:.2%} ({direction})")
        if internal.concentration_change != 1.0:
            conc = "集中" if internal.concentration_change > 1 else "分散"
            parts.append(f"筹码{conc}: {internal.concentration_change:.2f}")
        return "; ".join(parts) if parts else ""


# ---------------------------------------------------------------------------
# 快速测试
# ---------------------------------------------------------------------------

def _quick_test():
    """内部快速验证 — 至少覆盖 3 个场景"""
    instb = InstitutionalBehaviorFactor()

    print("=" * 60)
    print("INSTB_P0_A 对象卡测试输出")
    print("=" * 60)

    today = datetime(2025, 7, 7)

    # --- 场景 1: 季报数据 - 机构大幅增持 + 筹码集中 ---
    print("\n【场景 1】季报数据 - 机构吸筹（ACCUMULATION）")
    q1 = InstbQuarterlyInput(
        instb_total_inst_pct=0.38,
        instb_prev_quarter_total=0.30,
        instb_shareholder_count=8500,
        instb_prev_shareholder_count=10000,
        instb_fund_holding_pct=0.15,
        prev_quarter_fund_pct=0.10,
        report_date="2025-06-30",
    )
    r1 = instb.calculate(quarterly_data=q1, current_date=today)
    _print_result(r1)

    # --- 场景 2: 季报数据 - 机构减持 + 筹码分散 ---
    print("\n【场景 2】季报数据 - 机构派发（DISTRIBUTION）")
    q2 = InstbQuarterlyInput(
        instb_total_inst_pct=0.22,
        instb_prev_quarter_total=0.30,
        instb_shareholder_count=15000,
        instb_prev_shareholder_count=10000,
        instb_fund_holding_pct=0.08,
        prev_quarter_fund_pct=0.12,
        report_date="2025-06-30",
    )
    r2 = instb.calculate(quarterly_data=q2, current_date=today)
    _print_result(r2)

    # --- 场景 3: OHLCV 模拟 - 放量滞涨（派发模拟） ---
    print("\n【场景 3】OHLCV 模拟 - 放量滞涨（DISTRIBUTION 模拟）")
    sim1 = InstbSimulatedInput(
        open_price=20.0,
        high_price=20.3,
        low_price=19.9,
        close_price=20.05,
        volume=500000,
        prev_close=20.0,
        volume_5d_avg=200000,
        volume_20d_avg=220000,
    )
    r3 = instb.calculate(simulated_data=sim1)
    _print_result(r3)

    # --- 场景 4: OHLCV 模拟 - 缩量回调（吸筹模拟） ---
    print("\n【场景 4】OHLCV 模拟 - 缩量回调（ACCUMULATION 模拟）")
    sim2 = InstbSimulatedInput(
        open_price=20.0,
        high_price=20.1,
        low_price=19.5,
        close_price=19.7,
        volume=80000,
        prev_close=20.0,
        volume_5d_avg=150000,
        volume_20d_avg=160000,
    )
    r4 = instb.calculate(simulated_data=sim2)
    _print_result(r4)

    # --- 场景 5: 季报数据过期 ---
    print("\n【场景 5】季报数据过期（OUTDATED）")
    q3 = InstbQuarterlyInput(
        instb_total_inst_pct=0.35,
        instb_prev_quarter_total=0.30,
        instb_shareholder_count=9000,
        instb_prev_shareholder_count=10000,
        report_date="2025-01-01",
    )
    r5 = instb.calculate(quarterly_data=q3, current_date=today)
    _print_result(r5)


def _print_result(result: ObjectCardOutput) -> None:
    for k, v in result.__dict__.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    _quick_test()
