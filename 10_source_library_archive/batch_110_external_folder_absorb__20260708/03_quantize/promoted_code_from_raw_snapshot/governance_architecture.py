"""
明朝内阁混合架构：Python 接口与类设计 v1.0
=====================================================
本文档全部内容源于用户（仓库所有者）的想法，由 Kimi 整理为可直接给编程 AI 实现的代码框架。

设计目标：
  1. 所有类有完整的类型提示（Python 3.10+）
  2. 所有方法有文档字符串说明
  3. 各模式下的逻辑通过策略模式实现，避免大量 if-else
  4. 消息通信通过 dataclass 实现，格式统一
  5. 审计日志自动记录，不可绕过

核心模块：
  - governance_engine.py   : 总控引擎（对外入口）
  - regime_modes.py        : 五种制度模式（策略模式）
  - cabinet.py             : 内阁（票拟）
  - six_departments.py     : 六科给事中（审查）
  - taijian_system.py      : 台谏系统（监察）
  - three_provinces.py     : 三省系统（分权）
  - emperor_console.py     : 皇帝控制台（用户接口）
  - memorial_documents.py  : 奏折/审查意见书（消息格式）
  - audit_logger.py        : 审计日志（起居注）
"""

from __future__ import annotations

import json
import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Protocol, Any
from pathlib import Path


# ============================================================================
# 1. 枚举与常量定义
# ============================================================================

class RegimeMode(Enum):
    """制度模式枚举"""
    NORMAL = "normal"           # 常态：明朝内阁
    BULL = "bull"               # 牛市：内阁集权
    BEAR = "bear"               # 熊市：台谏监察
    OSCILLATION = "oscillation" # 震荡：三省分权
    CRISIS = "crisis"           # 危机：皇帝独裁


class PeriodQueenState(Enum):
    """PeriodQueen 七态枚举"""
    GESTATION = "gestation"
    ATTACK_SUSTAINED = "attack_sustained"
    REMAINING_WARMTH = "remaining_warmth"
    POWER_TRANSITION = "power_transition"
    MACULAR_FADE = "macular_fade"
    BEAR_LOOKING_UP = "bear_looking_up"
    MACRO_CALIBRATION = "macro_calibration"
    EXTREME_VOL = "extreme_vol"
    HALT = "halt"


class Verdict(Enum):
    """审查裁定枚举"""
    PASS = "pass"           # 通过，盖印
    REJECT = "reject"       # 封驳（否决）
    CONDITIONAL = "conditional"  # 附条件通过
    DEFER = "defer"         # 留中（暂不决策）


class ObjectMaturity(Enum):
    """对象卡成熟度枚举"""
    SHELL_ONLY = "shell_only"
    PROXY_QUANTIZABLE = "proxy_quantizable_now"
    NEEDS_EXTRA_DATA = "needs_extra_data"
    FUTURE_BUCKET = "future_bucket"


# 制度模式 ↔ PeriodQueen 状态映射表
REGIME_MODE_MAP: dict[PeriodQueenState, RegimeMode] = {
    PeriodQueenState.ATTACK_SUSTAINED: RegimeMode.BULL,
    PeriodQueenState.REMAINING_WARMTH: RegimeMode.BULL,
    PeriodQueenState.POWER_TRANSITION: RegimeMode.NORMAL,
    PeriodQueenState.MACULAR_FADE: RegimeMode.NORMAL,
    PeriodQueenState.GESTATION: RegimeMode.OSCILLATION,
    PeriodQueenState.BEAR_LOOKING_UP: RegimeMode.BEAR,
    PeriodQueenState.MACRO_CALIBRATION: RegimeMode.BEAR,
    PeriodQueenState.EXTREME_VOL: RegimeMode.CRISIS,
    PeriodQueenState.HALT: RegimeMode.CRISIS,
}


# ============================================================================
# 2. 消息格式（奏折制度）
# ============================================================================

@dataclass
class MemorialDocument:
    """
    奏折：内阁/三省提交的提案文档
    对应现实中的"奏折"——臣子向皇帝呈报的正式文书
    """
    memorial_id: str                          # 奏折编号，如 ZHE-20240624-001
    submitter: str                            # 呈报部门："内阁/中书省/经理层"
    regime_mode: RegimeMode                   # 当前制度模式
    
    # 交易内容
    symbol: str                               # 标的代码
    direction: str                            # LONG / SHORT / HOLD
    entry_price: float | None = None          # 入场价
    stop_loss: float | None = None            # 止损价
    target_size_pct: float | None = None      # 目标仓位（%）
    
    # 依据
    fundamental_basis: dict[str, Any] = field(default_factory=dict)
    technical_basis: dict[str, Any] = field(default_factory=dict)
    object_cards: list[str] = field(default_factory=list)  # 引用的对象卡 ID
    confidence_score: int = 5                 # 信心度 0-10
    
    # 元数据
    timestamp: datetime = field(default_factory=datetime.now)
    memo_hash: str = ""                       # 内容哈希，防篡改
    
    def __post_init__(self):
        if not self.memo_hash:
            self.memo_hash = self._compute_hash()
    
    def _compute_hash(self) -> str:
        """计算奏折内容哈希，确保不可篡改"""
        content = f"{self.memorial_id}{self.symbol}{self.direction}{self.timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ReviewDocument:
    """
    审查意见书：六科/门下省/台谏的审查结果
    对应现实中的"批红"或"封驳书"
    """
    review_id: str                            # 审查编号
    original_memorial_id: str                 # 对应的奏折编号
    reviewer: str                             # 审查部门
    
    verdict: Verdict                          # 裁定结果
    reason: str = ""                          # 理由
    restrictions: list[str] = field(default_factory=list)  # 附加限制条件
    
    # 各科的详细审查结果
    department_results: dict[str, dict] = field(default_factory=dict)
    
    # 参数调整（如 Kelly 模式、Van Tharp 上限）
    kelly_mode: str = "half"                  # aggressive / half / conservative / quarter
    van_tharp_limit: float = 0.02             # 0.03 / 0.02 / 0.01
    min_objects: int = 3                      # 2 / 3 / 5
    max_position_pct: float = 1.0             # 1.0 / 0.5 / 0.3 / 0.08
    
    # 元数据
    timestamp: datetime = field(default_factory=datetime.now)
    stamp: str = ""                           # "六科印" / "门下省印" / 空
    
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ImperialEdict:
    """
    圣旨/中旨：皇帝的最终决策
    对应现实中的"批红"或"中旨"
    """
    edict_id: str
    memorial_id: str
    
    decision: str                             # APPROVE / REJECT / DEFER
    final_size_pct: float | None = None       # 最终裁定仓位
    
    emperor_comment: str = ""                 # 皇帝批语（可选）
    is_zhongzhi: bool = False                 # 是否中旨（绕过正常流程）
    
    timestamp: datetime = field(default_factory=datetime.now)


# ============================================================================
# 3. 审计日志（起居注）
# ============================================================================

class AuditLogger:
    """
    起居注：记录系统所有决策链
    对应现实中的"起居注"——记录皇帝日常言行的官方史书
    """
    
    def __init__(self, log_dir: Path = Path("logs/governance")):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.current_log: list[dict] = []
    
    def log_memorial(self, memorial: MemorialDocument) -> None:
        """记录奏折提交"""
        self._write({
            "event": "MEMORIAL_SUBMITTED",
            "data": memorial.to_dict(),
        })
    
    def log_review(self, review: ReviewDocument) -> None:
        """记录审查结果"""
        self._write({
            "event": "REVIEW_COMPLETED",
            "data": review.to_dict(),
        })
    
    def log_edict(self, edict: ImperialEdict) -> None:
        """记录皇帝决策"""
        self._write({
            "event": "EDICT_ISSUED",
            "data": {
                "edict_id": edict.edict_id,
                "memorial_id": edict.memorial_id,
                "decision": edict.decision,
                "final_size_pct": edict.final_size_pct,
                "is_zhongzhi": edict.is_zhongzhi,
                "timestamp": edict.timestamp.isoformat(),
            },
        })
    
    def log_mode_switch(self, from_mode: RegimeMode, to_mode: RegimeMode,
                        trigger: str) -> None:
        """记录模式切换"""
        self._write({
            "event": "REGIME_SWITCH",
            "from": from_mode.value,
            "to": to_mode.value,
            "trigger": trigger,
        })
    
    def log_trade_execution(self, symbol: str, direction: str,
                            size: float, price: float) -> None:
        """记录交易执行"""
        self._write({
            "event": "TRADE_EXECUTED",
            "symbol": symbol,
            "direction": direction,
            "size": size,
            "price": price,
        })
    
    def _write(self, record: dict) -> None:
        """写入日志"""
        record["logged_at"] = datetime.now().isoformat()
        self.current_log.append(record)
        
        # 每日落盘一次
        if len(self.current_log) >= 100:
            self._flush()
    
    def _flush(self) -> None:
        """将内存日志写入磁盘"""
        if not self.current_log:
            return
        
        date_str = datetime.now().strftime("%Y%m%d")
        log_file = self.log_dir / f"audit_{date_str}.jsonl"
        
        with open(log_file, "a", encoding="utf-8") as f:
            for record in self.current_log:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        
        self.current_log.clear()
    
    def query(self, event_type: str | None = None,
              start: datetime | None = None,
              end: datetime | None = None) -> list[dict]:
        """查询日志"""
        # 简化实现：实际应该从磁盘加载并过滤
        results = self.current_log
        if event_type:
            results = [r for r in results if r.get("event") == event_type]
        return results


# ============================================================================
# 4. 制度模式策略（策略模式）
# ============================================================================

class RegimeModeStrategy(ABC):
    """
    制度模式策略基类
    每种模式实现自己的票拟规则、审查规则、仓位规则
    """
    
    def __init__(self, audit_logger: AuditLogger):
        self.audit = audit_logger
    
    @property
    @abstractmethod
    def mode(self) -> RegimeMode:
        """返回对应的制度模式"""
        ...
    
    # ---------- 内阁票拟规则 ----------
    
    @abstractmethod
    def can_unilateral_propose(self) -> bool:
        """首辅是否可以独断票拟（不需要次辅联署）"""
        ...
    
    @abstractmethod
    def min_confidence_for_propose(self) -> int:
        """票拟所需的最低信心度"""
        ...
    
    @abstractmethod
    def require_joint_signature(self) -> bool:
        """是否要求首辅+次辅联署"""
        ...
    
    # ---------- 六科审查规则 ----------
    
    @abstractmethod
    def kelly_mode(self) -> str:
        """Kelly 计算模式"""
        ...
    
    @abstractmethod
    def van_tharp_limit(self) -> float:
        """Van Tharp 风险上限"""
        ...
    
    @abstractmethod
    def min_objects_for_entry(self) -> int:
        """入场所需的最少对象卡数量"""
        ...
    
    @abstractmethod
    def allow_shell_only_objects(self) -> bool:
        """是否允许 shell_only 对象卡参与"""
        ...
    
    @abstractmethod
    def review_method(self) -> str:
        """审查方式：realtime / batch / post_hoc"""
        ...
    
    @abstractmethod
    def max_position_pct(self) -> float:
        """单票最大仓位"""
        ...
    
    # ---------- 台谏规则 ----------
    
    @abstractmethod
    def taijian_position(self) -> str:
        """台谏位置：front（前置）/ rear（后置）/ standby（待命）"""
        ...
    
    # ---------- 特殊机制 ----------
    
    @abstractmethod
    def has_fast_track(self) -> bool:
        """是否有快速通道"""
        ...
    
    @abstractmethod
    def allow_new_positions(self) -> bool:
        """是否允许开新仓"""
        ...


class NormalCabinetStrategy(RegimeModeStrategy):
    """常态内阁模式策略"""
    
    @property
    def mode(self) -> RegimeMode:
        return RegimeMode.NORMAL
    
    def can_unilateral_propose(self) -> bool:
        return False  # 必须联合票拟
    
    def min_confidence_for_propose(self) -> int:
        return 5
    
    def require_joint_signature(self) -> bool:
        return True
    
    def kelly_mode(self) -> str:
        return "half"
    
    def van_tharp_limit(self) -> float:
        return 0.02
    
    def min_objects_for_entry(self) -> int:
        return 3
    
    def allow_shell_only_objects(self) -> bool:
        return False
    
    def review_method(self) -> str:
        return "realtime"
    
    def max_position_pct(self) -> float:
        return 1.0
    
    def taijian_position(self) -> str:
        return "rear"  # 后置监察
    
    def has_fast_track(self) -> bool:
        return False
    
    def allow_new_positions(self) -> bool:
        return True


class BullMarketStrategy(RegimeModeStrategy):
    """牛市内阁集权模式策略"""
    
    @property
    def mode(self) -> RegimeMode:
        return RegimeMode.BULL
    
    def can_unilateral_propose(self) -> bool:
        return True  # 首辅可以独断
    
    def min_confidence_for_propose(self) -> int:
        return 5
    
    def require_joint_signature(self) -> bool:
        return False
    
    def kelly_mode(self) -> str:
        return "aggressive"  # full Kelly
    
    def van_tharp_limit(self) -> float:
        return 0.03  # 放宽到 3%
    
    def min_objects_for_entry(self) -> int:
        return 2  # 降为 2 个
    
    def allow_shell_only_objects(self) -> bool:
        return True  # 允许 shell_only
    
    def review_method(self) -> str:
        return "batch"  # 批量审查
    
    def max_position_pct(self) -> float:
        return 1.0
    
    def taijian_position(self) -> str:
        return "rear"
    
    def has_fast_track(self) -> bool:
        return True  # 有快速通道
    
    def allow_new_positions(self) -> bool:
        return True


class BearMarketStrategy(RegimeModeStrategy):
    """熊市台谏监察模式策略"""
    
    @property
    def mode(self) -> RegimeMode:
        return RegimeMode.BEAR
    
    def can_unilateral_propose(self) -> bool:
        return False
    
    def min_confidence_for_propose(self) -> int:
        return 7  # 信心度要求更高
    
    def require_joint_signature(self) -> bool:
        return True  # 必须联署，任何一方不同意就不能票拟
    
    def kelly_mode(self) -> str:
        return "conservative"  # quarter Kelly
    
    def van_tharp_limit(self) -> float:
        return 0.01  # 严格到 1%
    
    def min_objects_for_entry(self) -> int:
        return 5  # 提高到 5 个
    
    def allow_shell_only_objects(self) -> bool:
        return False  # 仅 mature
    
    def review_method(self) -> str:
        return "realtime"  # 逐笔实时审查
    
    def max_position_pct(self) -> float:
        return 0.03  # 单票上限 3%
    
    def taijian_position(self) -> str:
        return "front"  # 前置监察
    
    def has_fast_track(self) -> bool:
        return False
    
    def allow_new_positions(self) -> bool:
        return False  # 禁止开新仓


class OscillationStrategy(RegimeModeStrategy):
    """震荡期三省分权模式策略"""
    
    @property
    def mode(self) -> RegimeMode:
        return RegimeMode.OSCILLATION
    
    def can_unilateral_propose(self) -> bool:
        return False
    
    def min_confidence_for_propose(self) -> int:
        return 6
    
    def require_joint_signature(self) -> bool:
        return True
    
    def kelly_mode(self) -> str:
        return "half"
    
    def van_tharp_limit(self) -> float:
        return 0.02
    
    def min_objects_for_entry(self) -> int:
        return 3
    
    def allow_shell_only_objects(self) -> bool:
        return False
    
    def review_method(self) -> str:
        return "realtime"
    
    def max_position_pct(self) -> float:
        return 0.08  # 单票上限 8%
    
    def taijian_position(self) -> str:
        return "rear"
    
    def has_fast_track(self) -> bool:
        return False
    
    def allow_new_positions(self) -> bool:
        return True  # 允许，但限制严格


class CrisisStrategy(RegimeModeStrategy):
    """危机皇帝独裁模式策略"""
    
    @property
    def mode(self) -> RegimeMode:
        return RegimeMode.CRISIS
    
    def can_unilateral_propose(self) -> bool:
        return True  # 独裁官独断
    
    def min_confidence_for_propose(self) -> int:
        return 0  # 独裁模式下不要求信心度
    
    def require_joint_signature(self) -> bool:
        return False
    
    def kelly_mode(self) -> str:
        return "emergency"  # 独裁官自行决定
    
    def van_tharp_limit(self) -> float:
        return 0.05  # 临时放宽，但每笔需记录理由
    
    def min_objects_for_entry(self) -> int:
        return 0  # 独裁模式下不要求对象卡
    
    def allow_shell_only_objects(self) -> bool:
        return True
    
    def review_method(self) -> str:
        return "post_hoc"  # 事后审计
    
    def max_position_pct(self) -> float:
        return 1.0  # 独裁官决定
    
    def taijian_position(self) -> str:
        return "standby"  # 待命，情报收集
    
    def has_fast_track(self) -> bool:
        return True  # 所有交易都是快速通道
    
    def allow_new_positions(self) -> bool:
        return True  # 独裁官决定


# 策略工厂
STRATEGY_REGISTRY: dict[RegimeMode, type[RegimeModeStrategy]] = {
    RegimeMode.NORMAL: NormalCabinetStrategy,
    RegimeMode.BULL: BullMarketStrategy,
    RegimeMode.BEAR: BearMarketStrategy,
    RegimeMode.OSCILLATION: OscillationStrategy,
    RegimeMode.CRISIS: CrisisStrategy,
}


# ============================================================================
# 5. 模式切换控制器
# ============================================================================

class RegimeModeController:
    """
    制度模式切换控制器
    根据 PeriodQueen 状态和市场指标，自动/手动切换制度模式
    """
    
    def __init__(self, audit_logger: AuditLogger):
        self.audit = audit_logger
        self.current_mode: RegimeMode = RegimeMode.NORMAL
        self.current_strategy: RegimeModeStrategy = NormalCabinetStrategy(audit_logger)
        self.mode_history: list[dict] = []
        self.cooldown_end: datetime | None = None
        self.fast_track_failures: int = 0  # 快速通道失败计数
    
    def get_strategy(self) -> RegimeModeStrategy:
        """获取当前策略"""
        return self.current_strategy
    
    def check_auto_switch(self, pq_state: PeriodQueenState,
                          market_data: dict,
                          performance: dict) -> RegimeMode | None:
        """
        检查是否需要自动切换模式
        
        Args:
            pq_state: PeriodQueen 当前状态
            market_data: 市场数据字典（含指数涨跌、成交量等）
            performance: 绩效数据字典（含连胜/连败、回撤等）
        
        Returns:
            需要切换到的新模式，或 None（不切换）
        """
        # 检查冷却期
        if self.cooldown_end and datetime.now() < self.cooldown_end:
            return None
        
        # 1. 根据 PeriodQueen 状态判断
        new_mode = REGIME_MODE_MAP.get(pq_state)
        if new_mode is None:
            new_mode = RegimeMode.NORMAL
        
        # 2. 技术指标异常覆盖
        if self._check_market_extreme(market_data):
            new_mode = RegimeMode.CRISIS
        
        # 3. 绩效异常覆盖
        if self._check_performance_degradation(performance):
            if self.current_mode == RegimeMode.BULL:
                # 牛市模式下绩效恶化 → 降级为常态
                new_mode = RegimeMode.NORMAL
        
        # 4. 快速通道失败检查
        if self.current_mode == RegimeMode.BULL and self.fast_track_failures >= 3:
            new_mode = RegimeMode.NORMAL  # 关闭快速通道
        
        if new_mode != self.current_mode:
            return new_mode
        
        return None
    
    def switch_mode(self, new_mode: RegimeMode, trigger: str) -> None:
        """
        执行模式切换
        
        Args:
            new_mode: 新模式
            trigger: 切换触发原因
        """
        old_mode = self.current_mode
        
        # 记录历史
        self.mode_history.append({
            "timestamp": datetime.now().isoformat(),
            "from": old_mode.value,
            "to": new_mode.value,
            "trigger": trigger,
        })
        
        # 切换策略
        self.current_mode = new_mode
        strategy_cls = STRATEGY_REGISTRY[new_mode]
        self.current_strategy = strategy_cls(self.audit)
        
        # 记录日志
        self.audit.log_mode_switch(old_mode, new_mode, trigger)
        
        # 设置冷却期
        self.cooldown_end = datetime.now() + timedelta(days=3)
        
        # 重置快速通道失败计数
        if new_mode != RegimeMode.BULL:
            self.fast_track_failures = 0
    
    def manual_switch(self, new_mode: RegimeMode, reason: str) -> None:
        """用户手动切换模式"""
        self.switch_mode(new_mode, f"MANUAL: {reason}")
    
    def record_fast_track_failure(self) -> None:
        """记录一次快速通道失败"""
        self.fast_track_failures += 1
    
    def _check_market_extreme(self, market_data: dict) -> bool:
        """检查市场是否进入极端状态"""
        csi300_change = market_data.get("csi300_daily_change", 0)
        limit_down_count = market_data.get("limit_down_count", 0)
        
        if csi300_change < -0.07:  # 沪深 300 单日跌幅 > 7%
            return True
        if limit_down_count > 500:  # 跌停家数 > 500
            return True
        
        return False
    
    def _check_performance_degradation(self, performance: dict) -> bool:
        """检查绩效是否恶化"""
        consecutive_losses = performance.get("consecutive_losses", 0)
        max_drawdown = performance.get("max_drawdown", 0)
        
        if consecutive_losses >= 5:
            return True
        if max_drawdown > 0.15:
            return True
        
        return False


# ============================================================================
# 6. 内阁（票拟）
# ============================================================================

class FundamentalMinister:
    """首辅大学士：基本面视角"""
    
    def __init__(self):
        self.watchlist: set[str] = set()  # 选股池
        self.sector_weights: dict[str, float] = {}  # 行业配置
    
    def update_watchlist(self, symbols: list[str]) -> None:
        """更新选股池"""
        self.watchlist = set(symbols)
    
    def evaluate(self, symbol: str, fundamental_data: dict) -> dict:
        """
        评估标的基本面
        
        Returns:
            {
                "in_watchlist": bool,
                "pe": float,
                "pb": float,
                "roe": float,
                "score": int,  # 0-10
                "verdict": "pass" / "fail",
                "reason": str,
            }
        """
        # TODO: 实现基本面评估逻辑
        return {
            "in_watchlist": symbol in self.watchlist,
            "score": 7,
            "verdict": "pass",
            "reason": "基本面良好",
        }
    
    def unilateral_propose(self, symbol: str, objects: dict,
                           strategy: RegimeModeStrategy) -> MemorialDocument:
        """
        首辅独断票拟（牛市模式使用）
        """
        memorial_id = f"ZHE-{datetime.now().strftime('%Y%m%d')}-{hash(symbol) % 1000:03d}"
        
        return MemorialDocument(
            memorial_id=memorial_id,
            submitter="首辅大学士（独断）",
            regime_mode=strategy.mode,
            symbol=symbol,
            direction="LONG",
            fundamental_basis={"source": "首辅独断", "reason": "牛市模式，首辅有权独断"},
            confidence_score=8,
        )


class TechnicalMinister:
    """次辅大学士：技术面视角"""
    
    def __init__(self):
        self.activated_objects: list[str] = []  # 当前激活的对象卡
    
    def evaluate(self, symbol: str, object_outputs: dict) -> dict:
        """
        评估标的技术面
        
        Args:
            object_outputs: 各对象卡的输出结果
        
        Returns:
            {
                "signals": list[str],  # 发出信号的对象卡
                "vote_count": int,
                "strength": int,  # 综合强度 0-10
                "verdict": "pass" / "fail",
                "reason": str,
            }
        """
        # TODO: 实现技术面评估逻辑
        signals = [oid for oid, out in object_outputs.items()
                   if out.get("signal_type") == "LONG"]
        
        return {
            "signals": signals,
            "vote_count": len(signals),
            "strength": 7,
            "verdict": "pass" if len(signals) >= 3 else "fail",
            "reason": f"{len(signals)} 个对象卡发出信号",
        }
    
    def joint_propose(self, symbol: str, fundamental_eval: dict,
                      technical_eval: dict,
                      strategy: RegimeModeStrategy) -> MemorialDocument | None:
        """
        联合票拟（常态/熊市/震荡模式使用）
        
        Returns:
            MemorialDocument（票拟成功）或 None（票拟失败）
        """
        # 检查信心度
        confidence = min(fundamental_eval.get("score", 0),
                        technical_eval.get("strength", 0))
        if confidence < strategy.min_confidence_for_propose():
            return None
        
        # 检查是否允许开新仓
        if not strategy.allow_new_positions():
            return None
        
        memorial_id = f"ZHE-{datetime.now().strftime('%Y%m%d')}-{hash(symbol) % 1000:03d}"
        
        return MemorialDocument(
            memorial_id=memorial_id,
            submitter="内阁（首辅+次辅联署）",
            regime_mode=strategy.mode,
            symbol=symbol,
            direction="LONG",
            fundamental_basis=fundamental_eval,
            technical_basis=technical_eval,
            object_cards=technical_eval.get("signals", []),
            confidence_score=confidence,
        )


class Cabinet:
    """
    内阁：负责票拟（交易提案）
    """
    
    def __init__(self, audit_logger: AuditLogger):
        self.audit = audit_logger
        self.shoufu = FundamentalMinister()
        self.cifu = TechnicalMinister()
        self.daily_proposals: list[MemorialDocument] = []
    
    def propose(self, symbol: str, fundamental_data: dict,
                object_outputs: dict,
                strategy: RegimeModeStrategy) -> MemorialDocument | None:
        """
        内阁票拟主入口
        
        根据当前制度模式，选择独断或联合票拟
        """
        # 1. 基本面评估
        fundamental_eval = self.shoufu.evaluate(symbol, fundamental_data)
        
        # 如果不在选股池，直接失败
        if not fundamental_eval.get("in_watchlist", False):
            return None
        
        # 2. 技术面评估
        technical_eval = self.cifu.evaluate(symbol, object_outputs)
        
        # 3. 根据模式选择票拟方式
        memorial: MemorialDocument | None = None
        
        if strategy.can_unilateral_propose():
            # 首辅独断（牛市/危机模式）
            memorial = self.shoufu.unilateral_propose(symbol, object_outputs, strategy)
            # 若次辅有强烈反对意见，记录但不阻止
            if technical_eval.get("verdict") == "fail":
                memorial.technical_basis["cifu_warning"] = "次辅反对，但首辅独断"
        else:
            # 联合票拟（常态/熊市/震荡模式）
            if strategy.require_joint_signature():
                # 需要联署：首辅和次辅都同意
                if fundamental_eval.get("verdict") != "pass":
                    return None
                if technical_eval.get("verdict") != "pass":
                    return None
            
            memorial = self.cifu.joint_propose(
                symbol, fundamental_eval, technical_eval, strategy
            )
        
        if memorial:
            self.daily_proposals.append(memorial)
            self.audit.log_memorial(memorial)
        
        return memorial
    
    def get_daily_summary(self) -> dict:
        """获取今日票拟摘要"""
        total = len(self.daily_proposals)
        passed_to_review = total  # 所有票拟都送审
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_proposed": total,
            "passed_to_review": passed_to_review,
        }
    
    def suspend(self) -> None:
        """内阁停摆（危机模式）"""
        self.daily_proposals.clear()


# ============================================================================
# 7. 六科给事中（审查）
# ============================================================================

class Department(ABC):
    """单科审查基类"""
    
    @abstractmethod
    def review(self, memorial: MemorialDocument,
               strategy: RegimeModeStrategy,
               portfolio: dict) -> dict:
        """
        审查奏折
        
        Returns:
            {
                "pass": bool,
                "reason": str,
                "adjustments": dict,  # 参数调整建议
            }
        """
        ...


class LiKeDepartment(Department):
    """吏科：对象卡成熟度审查"""
    
    def review(self, memorial: MemorialDocument,
               strategy: RegimeModeStrategy,
               portfolio: dict) -> dict:
        
        if strategy.allow_shell_only_objects():
            return {"pass": True, "reason": "牛市/危机模式，允许所有对象卡", "adjustments": {}}
        
        # 检查所有引用的对象卡是否成熟
        for oid in memorial.object_cards:
            # TODO: 从对象卡注册表查询成熟度
            maturity = ObjectMaturity.PROXY_QUANTIZABLE  # 简化
            if maturity in [ObjectMaturity.SHELL_ONLY, ObjectMaturity.FUTURE_BUCKET]:
                return {
                    "pass": False,
                    "reason": f"对象卡 {oid} 成熟度不足 ({maturity.value})",
                    "adjustments": {},
                }
        
        return {"pass": True, "reason": "所有对象卡成熟度合格", "adjustments": {}}


class HuKeDepartment(Department):
    """户科：资金管理审查（Kelly + VolTarget）"""
    
    def review(self, memorial: MemorialDocument,
               strategy: RegimeModeStrategy,
               portfolio: dict) -> dict:
        
        # 根据策略模式计算 Kelly
        kelly_mode = strategy.kelly_mode()
        
        # TODO: 实际 Kelly 计算
        kelly_f = 0.18  # 简化
        
        if kelly_mode == "aggressive":
            scalar = kelly_f
        elif kelly_mode == "half":
            scalar = kelly_f / 2
        elif kelly_mode == "conservative":
            scalar = kelly_f / 4
        else:
            scalar = kelly_f / 2
        
        # 检查是否超过最大仓位
        if memorial.target_size_pct and memorial.target_size_pct > strategy.max_position_pct():
            return {
                "pass": False,
                "reason": f"仓位 {memorial.target_size_pct} 超过上限 {strategy.max_position_pct()}",
                "adjustments": {"max_position_pct": strategy.max_position_pct()},
            }
        
        return {
            "pass": True,
            "reason": f"Kelly 模式={kelly_mode}, scalar={scalar:.2f}",
            "adjustments": {"kelly_scalar": scalar},
        }


class BingKeDepartment(Department):
    """兵科：交易信号审查"""
    
    def review(self, memorial: MemorialDocument,
               strategy: RegimeModeStrategy,
               portfolio: dict) -> dict:
        
        min_objects = strategy.min_objects_for_entry()
        actual_objects = len(memorial.object_cards)
        
        if actual_objects < min_objects:
            return {
                "pass": False,
                "reason": f"对象卡数量不足：{actual_objects} < {min_objects}",
                "adjustments": {},
            }
        
        return {
            "pass": True,
            "reason": f"对象卡数量合格：{actual_objects} >= {min_objects}",
            "adjustments": {},
        }


class XingKeDepartment(Department):
    """刑科：风险审查（Van Tharp）"""
    
    def review(self, memorial: MemorialDocument,
               strategy: RegimeModeStrategy,
               portfolio: dict) -> dict:
        
        limit = strategy.van_tharp_limit()
        
        # TODO: 实际 Van Tharp 计算
        # risk = |entry - stop| * size / total_capital
        risk = 0.015  # 简化
        
        if risk > limit:
            return {
                "pass": False,
                "reason": f"Van Tharp 风险 {risk:.2%} 超过上限 {limit:.2%}",
                "adjustments": {"van_tharp_limit": limit},
            }
        
        return {
            "pass": True,
            "reason": f"Van Tharp 风险 {risk:.2%} <= {limit:.2%}",
            "adjustments": {},
        }


class GongKeDepartment(Department):
    """工科：数据质量审查"""
    
    def review(self, memorial: MemorialDocument,
               strategy: RegimeModeStrategy,
               portfolio: dict) -> dict:
        
        # TODO: 实际数据质量检查
        # 检查数据缺失、异常等
        
        return {"pass": True, "reason": "数据质量合格", "adjustments": {}}


class SixDepartments:
    """
    六科给事中：负责审查奏折
    """
    
    def __init__(self, audit_logger: AuditLogger):
        self.audit = audit_logger
        self.departments: dict[str, Department] = {
            "li": LiKeDepartment(),
            "hu": HuKeDepartment(),
            "bing": BingKeDepartment(),
            "xing": XingKeDepartment(),
            "gong": GongKeDepartment(),
        }
    
    def review(self, memorial: MemorialDocument,
               strategy: RegimeModeStrategy,
               portfolio: dict) -> ReviewDocument:
        """
        六科联合审查
        
        Returns:
            ReviewDocument：审查意见书
        """
        review_id = f"SHEN-{memorial.memorial_id}"
        department_results: dict[str, dict] = {}
        
        # 逐科审查
        all_passed = True
        first_failure_reason = ""
        
        for name, dept in self.departments.items():
            result = dept.review(memorial, strategy, portfolio)
            department_results[name] = result
            
            if not result["pass"]:
                all_passed = False
                if not first_failure_reason:
                    first_failure_reason = result["reason"]
        
        # 生成审查意见书
        if all_passed:
            verdict = Verdict.PASS
            reason = "五科全部通过"
            stamp = "六科印"
        else:
            verdict = Verdict.REJECT
            reason = first_failure_reason
            stamp = ""
        
        review = ReviewDocument(
            review_id=review_id,
            original_memorial_id=memorial.memorial_id,
            reviewer="六科给事中",
            verdict=verdict,
            reason=reason,
            department_results=department_results,
            kelly_mode=strategy.kelly_mode(),
            van_tharp_limit=strategy.van_tharp_limit(),
            min_objects=strategy.min_objects_for_entry(),
            max_position_pct=strategy.max_position_pct(),
            stamp=stamp,
        )
        
        self.audit.log_review(review)
        
        return review


# ============================================================================
# 8. 台谏系统
# ============================================================================

class TaiJianSystem:
    """
    台谏系统：御史台 + 谏官
    """
    
    def __init__(self, audit_logger: AuditLogger):
        self.audit = audit_logger
        self.warnings: list[dict] = []  # 谏言记录
        self.impeachments: list[dict] = []  # 纠劾记录
    
    def pre_trade_warning(self, memorial: MemorialDocument,
                          market_data: dict) -> dict | None:
        """
        事前谏言（熊市模式前置使用）
        
        Returns:
            谏言书，或 None（无风险）
        """
        # TODO: 实现风险预警逻辑
        # 检查市场波动率、标的近期表现等
        
        return None
    
    def post_trade_audit(self, symbol: str, trade_result: dict) -> dict | None:
        """
        事后纠劾（所有模式都使用）
        
        Returns:
            纠劾书，或 None（无违规）
        """
        # TODO: 实现合规审查逻辑
        # 检查是否违反止损规则、是否超仓等
        
        return None
    
    def intelligence_report(self, market_data: dict) -> dict:
        """
        情报报告（危机模式使用）
        
        Returns:
            市场情报摘要
        """
        return {
            "volatility_level": market_data.get("volatility", "normal"),
            "market_breadth": market_data.get("breadth", "neutral"),
            "sentiment": market_data.get("sentiment", "neutral"),
        }


# ============================================================================
# 9. 皇帝控制台
# ============================================================================

class EmperorConsole:
    """
    皇帝控制台：用户交互接口
    对应现实中的"御前会议"
    """
    
    def __init__(self, governance_engine: GovernanceEngine):
        self.engine = governance_engine
    
    def get_dashboard(self) -> dict:
        """
        获取控制台仪表盘数据
        
        Returns:
            {
                "regime_mode": str,
                "period_queen_state": str,
                "cabinet_status": dict,
                "pending_memorials": list,
                "today_trades": list,
                "portfolio_summary": dict,
            }
        """
        return {
            "regime_mode": self.engine.controller.current_mode.value,
            "period_queen_state": self.engine.pq_state.value if self.engine.pq_state else "unknown",
            "cabinet_status": self.engine.cabinet.get_daily_summary(),
            "pending_memorials": [m.to_dict() for m in self.engine.pending_memorials],
            "today_trades": self.engine.today_trades,
            "portfolio_summary": self.engine.portfolio,
        }
    
    def approve_memorial(self, memorial_id: str,
                         final_size_pct: float | None = None) -> ImperialEdict:
        """批红：通过奏折"""
        edict = ImperialEdict(
            edict_id=f"PI-{memorial_id}",
            memorial_id=memorial_id,
            decision="APPROVE",
            final_size_pct=final_size_pct,
        )
        self.engine.execute_edict(edict)
        return edict
    
    def reject_memorial(self, memorial_id: str,
                        comment: str = "") -> ImperialEdict:
        """否决奏折"""
        edict = ImperialEdict(
            edict_id=f"PI-{memorial_id}",
            memorial_id=memorial_id,
            decision="REJECT",
            emperor_comment=comment,
        )
        self.engine.execute_edict(edict)
        return edict
    
    def defer_memorial(self, memorial_id: str) -> ImperialEdict:
        """留中：暂不决策"""
        edict = ImperialEdict(
            edict_id=f"PI-{memorial_id}",
            memorial_id=memorial_id,
            decision="DEFER",
        )
        self.engine.execute_edict(edict)
        return edict
    
    def issue_zhongzhi(self, symbol: str, direction: str,
                       size_pct: float, reason: str) -> ImperialEdict:
        """
        中旨：绕过正常流程，直接下令
        慎用！
        """
        memorial_id = f"ZHONGZHI-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 创建虚拟奏折
        memorial = MemorialDocument(
            memorial_id=memorial_id,
            submitter="皇帝中旨",
            regime_mode=RegimeMode.CRISIS,
            symbol=symbol,
            direction=direction,
            target_size_pct=size_pct,
            fundamental_basis={"source": "中旨", "reason": reason},
        )
        
        edict = ImperialEdict(
            edict_id=f"PI-{memorial_id}",
            memorial_id=memorial_id,
            decision="APPROVE",
            final_size_pct=size_pct,
            is_zhongzhi=True,
        )
        
        self.engine.execute_edict(edict)
        return edict
    
    def switch_regime_mode(self, new_mode: RegimeMode, reason: str) -> None:
        """手动切换制度模式"""
        self.engine.controller.manual_switch(new_mode, reason)
    
    def emergency_liquidate(self) -> None:
        """一键清仓"""
        # TODO: 实现清仓逻辑
        pass


# ============================================================================
# 10. 总控引擎（GovernanceEngine）
# ============================================================================

class GovernanceEngine:
    """
    治理引擎：对外主入口
    协调内阁、六科、台谏、模式切换等所有模块
    """
    
    def __init__(self, log_dir: Path = Path("logs/governance")):
        # 基础设施
        self.audit = AuditLogger(log_dir)
        
        # 核心模块
        self.controller = RegimeModeController(self.audit)
        self.cabinet = Cabinet(self.audit)
        self.six_departments = SixDepartments(self.audit)
        self.taijian = TaiJianSystem(self.audit)
        
        # 状态
        self.pq_state: PeriodQueenState | None = None
        self.pending_memorials: list[MemorialDocument] = []
        self.today_trades: list[dict] = []
        self.portfolio: dict = {
            "positions": {},
            "cash_pct": 1.0,
            "total_risk": 0.0,
        }
    
    def run_daily_cycle(self, pq_state: PeriodQueenState,
                        market_data: dict,
                        fundamental_data: dict,
                        object_outputs: dict) -> list[ImperialEdict]:
        """
        每日治理循环主入口
        
        流程：
        1. 检查模式切换
        2. 内阁票拟
        3. 六科审查
        4. 台谏监察（前置/后置）
        5. 生成待批红奏折
        
        Returns:
            需要用户批红的奏折列表
        """
        self.pq_state = pq_state
        
        # 1. 检查模式切换
        new_mode = self.controller.check_auto_switch(
            pq_state, market_data, self._get_performance()
        )
        if new_mode:
            self.controller.switch_mode(new_mode, f"PeriodQueen={pq_state.value}")
        
        strategy = self.controller.get_strategy()
        
        # 2. 内阁票拟（逐个标的）
        proposals: list[MemorialDocument] = []
        for symbol in self._get_watchlist():
            memorial = self.cabinet.propose(
                symbol, fundamental_data.get(symbol, {}),
                object_outputs.get(symbol, {}), strategy
            )
            if memorial:
                proposals.append(memorial)
        
        # 3. 六科审查
        reviews: list[ReviewDocument] = []
        for memorial in proposals:
            review = self.six_departments.review(memorial, strategy, self.portfolio)
            reviews.append(review)
        
        # 4. 台谏监察（熊市前置）
        if strategy.taijian_position() == "front":
            for memorial in proposals:
                warning = self.taijian.pre_trade_warning(memorial, market_data)
                if warning:
                    # 谏言前置：标记为需要额外关注
                    memorial.fundamental_basis["taijian_warning"] = warning
        
        # 5. 生成待批红列表
        pending: list[MemorialDocument] = []
        for memorial, review in zip(proposals, reviews):
            if review.verdict == Verdict.PASS:
                pending.append(memorial)
            # REJECT 的奏折不进入待批红列表
        
        self.pending_memorials = pending
        
        # 在牛市快速通道模式下，自动批红
        if strategy.has_fast_track():
            edicts = []
            for memorial in pending:
                # 检查快速通道条件
                if self._check_fast_track(memorial):
                    edict = ImperialEdict(
                        edict_id=f"AUTO-{memorial.memorial_id}",
                        memorial_id=memorial.memorial_id,
                        decision="APPROVE",
                        final_size_pct=memorial.target_size_pct,
                    )
                    self.execute_edict(edict)
                    edicts.append(edict)
            return edicts
        
        # 其他模式：返回待批红列表，等待用户决策
        return []
    
    def execute_edict(self, edict: ImperialEdict) -> None:
        """
        执行圣旨
        """
        self.audit.log_edict(edict)
        
        if edict.decision == "APPROVE":
            # 执行交易
            # TODO: 调用交易执行模块
            self.today_trades.append({
                "symbol": edict.memorial_id,  # 简化，实际从 memorial 查
                "size_pct": edict.final_size_pct,
                "timestamp": datetime.now(),
            })
            self.audit.log_trade_execution(
                edict.memorial_id, "LONG",
                edict.final_size_pct or 0, 0.0
            )
        
        # 从待批红列表移除
        self.pending_memorials = [
            m for m in self.pending_memorials
            if m.memorial_id != edict.memorial_id
        ]
    
    def _get_watchlist(self) -> list[str]:
        """获取选股池"""
        # TODO: 从 DataLoader 获取
        return []
    
    def _get_performance(self) -> dict:
        """获取当前绩效数据"""
        # TODO: 从回测模块获取
        return {
            "consecutive_losses": 0,
            "max_drawdown": 0.0,
        }
    
    def _check_fast_track(self, memorial: MemorialDocument) -> bool:
        """检查是否符合快速通道条件"""
        # TODO: 实现快速通道条件检查
        return True


# ============================================================================
# 11. 使用示例
# ============================================================================

def main_example():
    """
    使用示例：完整的一日治理循环
    """
    # 1. 初始化引擎
    engine = GovernanceEngine()
    console = EmperorConsole(engine)
    
    # 2. 模拟数据
    pq_state = PeriodQueenState.ATTACK_SUSTAINED  # 牛市
    market_data = {
        "csi300_daily_change": 0.02,
        "volatility": 0.15,
        "limit_down_count": 0,
    }
    fundamental_data = {
        "000001.SZ": {"pe": 12, "pb": 1.5, "roe": 0.18},
    }
    object_outputs = {
        "000001.SZ": {
            "CHZL_BSD": {"signal_type": "LONG", "strength": 8},
            "BPB": {"signal_type": "LONG", "strength": 7},
            "MFLOW": {"signal_type": "LONG", "strength": 6},
        },
    }
    
    # 3. 运行每日循环
    auto_edicts = engine.run_daily_cycle(
        pq_state, market_data, fundamental_data, object_outputs
    )
    
    # 4. 查看仪表盘
    dashboard = console.get_dashboard()
    print(f"当前模式: {dashboard['regime_mode']}")
    print(f"待批红奏折: {len(dashboard['pending_memorials'])} 份")
    
    # 5. 用户批红（如有待批红奏折）
    for memorial_dict in dashboard["pending_memorials"]:
        memorial_id = memorial_dict["memorial_id"]
        # 用户决定批红
        console.approve_memorial(memorial_id, final_size_pct=0.09)
    
    # 6. 查看今日交易
    print(f"今日执行交易: {len(engine.today_trades)} 笔")


if __name__ == "__main__":
    main_example()
