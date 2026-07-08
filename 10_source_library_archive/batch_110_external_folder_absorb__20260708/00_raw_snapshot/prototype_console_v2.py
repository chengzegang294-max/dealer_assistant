#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
御前会议控制台 v2.0 — 增强版（含实时模拟 + 对象卡集成）
===============================================================
基于 prototype_console.py v1.0 增强，新增：
  - 模拟对象卡运行（VOLFAC/ATRATIO 实时计算）
  - 数据管道集成（DataPipe → 对象卡端到端）
  - 事件流记录（起居注增强版）
  - 投票模拟（策略组合投票过程可视化）
  - ABORT 原因展示（14种标准编码）

运行方式: python prototype_console_v2.py
"""

import os
import sys
import json
import time
import random
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


# ============================================================================
# ANSI 颜色码（与 v1.0 完全一致）
# ============================================================================

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    BG_BRIGHT_RED = "\033[101m"
    BG_BRIGHT_GREEN = "\033[102m"
    BG_BRIGHT_YELLOW = "\033[103m"


def c(text: str, color: str = "", bold: bool = False) -> str:
    prefix = ""
    if bold:
        prefix += Colors.BOLD
    prefix += color
    return f"{prefix}{text}{Colors.RESET}"


# ============================================================================
# 枚举定义（与 v1.0 一致）
# ============================================================================

class RegimeMode(Enum):
    NORMAL = "normal"
    BULL = "bull"
    BEAR = "bear"
    OSCILLATION = "oscillation"
    CRISIS = "crisis"


class Verdict(Enum):
    PASS = "pass"
    REJECT = "reject"
    CONDITIONAL = "conditional"
    DEFER = "defer"


# ============================================================================
# 模式配置（与 v1.0 一致）
# ============================================================================

MODE_CONFIG = {
    RegimeMode.NORMAL: {
        "name": "常态内阁模式",
        "color": Colors.BRIGHT_CYAN,
        "bg": Colors.BG_CYAN,
        "shoufu_role": "首辅（联合票拟）",
        "cifu_role": "次辅（联合票拟）",
        "taijian": "后置监察",
        "li": "对象卡全审",
        "hu": "Kelly Half",
        "bing": "需3卡",
        "xing": "VanTharp 2%",
        "gong": "数据质检",
        "fast_track": False,
        "new_position": True,
    },
    RegimeMode.BULL: {
        "name": "牛市内阁集权",
        "color": Colors.BRIGHT_RED,
        "bg": Colors.BG_BRIGHT_RED,
        "shoufu_role": "首辅（独断）",
        "cifu_role": "次辅（顾问）",
        "taijian": "后置监察",
        "li": "免检",
        "hu": "Kelly Full",
        "bing": "需2卡",
        "xing": "VanTharp 3%",
        "gong": "免检",
        "fast_track": True,
        "new_position": True,
    },
    RegimeMode.BEAR: {
        "name": "熊市台谏监察",
        "color": Colors.BRIGHT_YELLOW,
        "bg": Colors.BG_BRIGHT_YELLOW,
        "shoufu_role": "首辅（联署必过）",
        "cifu_role": "次辅（联署必过）",
        "taijian": "前置监察",
        "li": "仅mature",
        "hu": "Kelly 1/4",
        "bing": "需5卡",
        "xing": "VanTharp 1%",
        "gong": "逐笔质检",
        "fast_track": False,
        "new_position": False,
    },
    RegimeMode.OSCILLATION: {
        "name": "震荡三省分权",
        "color": Colors.YELLOW,
        "bg": Colors.BG_YELLOW,
        "shoufu_role": "中书省（草拟）",
        "cifu_role": "尚书省（执行）",
        "taijian": "后置监察",
        "li": "仅mature",
        "hu": "Kelly Half",
        "bing": "需3卡",
        "xing": "VanTharp 2%",
        "gong": "逐笔质检",
        "fast_track": False,
        "new_position": True,
    },
    RegimeMode.CRISIS: {
        "name": "危机皇帝独裁",
        "color": Colors.BRIGHT_RED,
        "bg": Colors.BG_RED,
        "shoufu_role": "内阁停摆",
        "cifu_role": "内阁停摆",
        "taijian": "待命",
        "li": "解散",
        "hu": "独裁官定",
        "bing": "独裁官定",
        "xing": "事后审计",
        "gong": "事后审计",
        "fast_track": True,
        "new_position": True,
    },
}


# ============================================================================
# v1.0 数据模型（完全保留）
# ============================================================================

@dataclass
class Memorial:
    memorial_id: str
    symbol: str
    direction: str
    size_pct: float
    confidence: int
    objects: list[str]
    verdict: Verdict = Verdict.PASS
    reviewer_comment: str = ""


@dataclass
class Position:
    symbol: str
    size_pct: float
    cost: float
    current: float
    stop: float
    status: str = "normal"


# ============================================================================
# v2.0 新增：事件流系统
# ============================================================================

@dataclass
class EventRecord:
    """事件记录"""
    timestamp: str
    event_type: str      # 'mode_switch' | 'card_run' | 'vote' | 'abort' | 'trade'
    detail: str
    data: Dict[str, Any] = field(default_factory=dict)


class EventStream:
    """起居注增强版 — 记录所有系统事件"""
    
    def __init__(self):
        self.records: List[EventRecord] = []
        self._type_counts: Dict[str, int] = {}
    
    def log(self, event_type: str, detail: str, data: Dict[str, Any] = None):
        record = EventRecord(
            timestamp=datetime.now().strftime("%H:%M:%S"),
            event_type=event_type,
            detail=detail,
            data=data or {},
        )
        self.records.append(record)
        self._type_counts[event_type] = self._type_counts.get(event_type, 0) + 1
    
    def get_recent(self, n: int = 8) -> List[EventRecord]:
        return self.records[-n:]
    
    def get_by_type(self, event_type: str) -> List[EventRecord]:
        return [r for r in self.records if r.event_type == event_type]
    
    def summary(self) -> Dict[str, int]:
        return dict(self._type_counts)


# ============================================================================
# v2.0 新增：模拟引擎（集成 DataPipe + 对象卡）
# ============================================================================

class SimulationEngine:
    """
    模拟引擎 — 在控制台中实时运行对象卡
    
    功能:
      1. 模拟数据管道拉取
      2. 运行 VOLFAC 对象卡
      3. 运行 ATRATIO 对象卡（空信号）
      4. 模拟投票过程
      5. 模拟模式切换建议
    """
    
    ABORT_CODES = [
        "missing_ohlcv", "period_queen_halt", "period_queen_unclear",
        "no_votes", "all_blocked", "votes_insufficient", "van_tharp_limit",
        "position_too_small", "no_positions_to_exit", "insufficient_exit_signals",
        "global_block", "maturity_unverified", "level2_missing", "market_halt",
    ]
    
    OBJECT_CARDS = [
        "VOLFAC", "ATRATIO", "MFLOW", "CHZL_BSD", "BPB", "TKR7",
    ]
    
    def __init__(self, event_stream: EventStream):
        self.event_stream = event_stream
        self.card_results: Dict[str, Dict[str, Any]] = {}
        self.last_sim_time: Optional[str] = None
        self._init_card_states()
    
    def _init_card_states(self):
        """初始化各对象卡状态"""
        for card in self.OBJECT_CARDS:
            self.card_results[card] = {
                "status": "standby",      # standby | running | done | error
                "signal_type": "-",
                "signal_strength": 0,
                "confidence": 0.0,
                "filter_action": "-",
                "size_scalar": 1.0,
                "last_run": "-",
                "notes": "等待首次运行",
            }
    
    def run_volfac(self, symbol: str = "000001.SZ") -> Dict[str, Any]:
        """运行 VOLFAC 对象卡模拟"""
        try:
            # 模拟数据生成（无需外部依赖）
            import numpy as np
            np.random.seed(hash(symbol) % 10000)
            
            # 生成60日收盘价
            returns = np.random.normal(0.001, 0.025, 60)
            close_60d = [10.0]
            for r in returns:
                close_60d.append(close_60d[-1] * (1 + r))
            close_60d = close_60d[1:]
            
            # 生成历史波动率（252日）
            hist_returns = np.random.normal(0.001, 0.025, 252)
            hist_closes = [10.0]
            for r in hist_returns:
                hist_closes.append(hist_closes[-1] * (1 + r))
            hist_closes = hist_closes[1:]
            
            hist_vol = []
            for i in range(60, len(hist_closes)):
                chunk = hist_closes[i-60:i]
                log_ret = np.log(np.array(chunk[1:]) / np.array(chunk[:-1]))
                hist_vol.append(float(np.std(log_ret, ddof=1)))
            
            # 导入 VOLFAC 对象卡（如果可用）
            try:
                sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
                from object_card_volfac import VolatilityFactor, VolFacRawInput
                
                vf = VolatilityFactor()
                raw = VolFacRawInput(
                    close_60d=[round(x, 4) for x in close_60d],
                    historical_vol_1y=[round(x, 6) for x in hist_vol],
                )
                result = vf.calculate(raw, strategy_type='swing', market_cap=50)
                
                self.card_results["VOLFAC"] = {
                    "status": "done",
                    "signal_type": result.signal_type,
                    "signal_strength": result.signal_strength,
                    "confidence": result.confidence,
                    "filter_action": result.filter_action,
                    "size_scalar": result.size_scalar,
                    "last_run": datetime.now().strftime("%H:%M:%S"),
                    "notes": f"vol_regime={result.internal.get('vol_regime')}, "
                             f"annualized_vol={result.internal.get('annualized_vol', 0):.2f}",
                }
                
                self.event_stream.log(
                    "card_run",
                    f"VOLFAC 完成: {symbol} → {result.internal.get('vol_regime')}, scalar={result.size_scalar}",
                    {"symbol": symbol, "vol_regime": result.internal.get('vol_regime')},
                )
                
            except ImportError:
                # 降级为纯模拟
                annualized_vol = float(np.std(returns, ddof=1) * np.sqrt(252))
                vol_regime = "HIGH_VOL" if annualized_vol > 0.4 else "LOW_VOL" if annualized_vol < 0.2 else "NORMAL_VOL"
                
                self.card_results["VOLFAC"] = {
                    "status": "done",
                    "signal_type": "FILTER",
                    "signal_strength": -1 if annualized_vol > 0.4 else 1 if annualized_vol < 0.2 else 0,
                    "confidence": 0.95,
                    "filter_action": "REDUCE_WEIGHT" if annualized_vol > 0.4 else "INCREASE_WEIGHT" if annualized_vol < 0.2 else "PASS",
                    "size_scalar": 0.5 if annualized_vol > 0.4 else 1.2 if annualized_vol < 0.2 else 1.0,
                    "last_run": datetime.now().strftime("%H:%M:%S"),
                    "notes": f"[模拟] vol_regime={vol_regime}, annualized_vol={annualized_vol:.2f}",
                }
                
                self.event_stream.log(
                    "card_run",
                    f"VOLFAC 模拟完成: {symbol} → {vol_regime}",
                    {"symbol": symbol, "vol_regime": vol_regime},
                )
            
            return self.card_results["VOLFAC"]
        
        except Exception as e:
            self.card_results["VOLFAC"] = {
                "status": "error",
                "notes": f"运行错误: {str(e)}",
            }
            self.event_stream.log("card_run", f"VOLFAC 错误: {str(e)}", {"error": str(e)})
            return self.card_results["VOLFAC"]
    
    def run_atratio(self, symbol: str = "000001.SZ") -> Dict[str, Any]:
        """运行 ATRATIO 对象卡（A股纯多头空信号）"""
        self.card_results["ATRATIO"] = {
            "status": "done",
            "signal_type": "NONE",
            "signal_strength": 0,
            "confidence": 0.0,
            "filter_action": "PASS",
            "size_scalar": 1.0,
            "last_run": datetime.now().strftime("%H:%M:%S"),
            "notes": "A股纯多头场景：因子无效（SBKT_F002），输出空信号",
        }
        self.event_stream.log("card_run", f"ATRATIO: {symbol} → 空信号（纯多头限制）")
        return self.card_results["ATRATIO"]
    
    def run_all_cards(self, symbol: str = "000001.SZ"):
        """运行所有对象卡"""
        self.run_volfac(symbol)
        self.run_atratio(symbol)
        
        # 模拟其他对象卡
        for card in ["MFLOW", "CHZL_BSD", "BPB", "TKR7"]:
            self.card_results[card] = {
                "status": "done",
                "signal_type": random.choice(["BUY", "SELL", "HOLD", "NONE"]),
                "signal_strength": random.randint(-2, 2),
                "confidence": round(random.uniform(0.3, 0.95), 2),
                "filter_action": random.choice(["PASS", "BLOCK_BUY", "REDUCE_WEIGHT"]),
                "size_scalar": round(random.uniform(0.5, 1.5), 2),
                "last_run": datetime.now().strftime("%H:%M:%S"),
                "notes": "模拟运行",
            }
            self.event_stream.log("card_run", f"{card}: {symbol} → 模拟完成")
        
        self.last_sim_time = datetime.now().strftime("%H:%M:%S")
    
    def simulate_vote(self, memorial_id: str) -> Dict[str, Any]:
        """模拟投票过程"""
        cards = ["VOLFAC", "ATRATIO", "MFLOW", "CHZL_BSD", "BPB"]
        votes = {card: random.choice(["FOR", "AGAINST", "ABSTAIN"]) for card in cards}
        
        for_count = sum(1 for v in votes.values() if v == "FOR")
        against_count = sum(1 for v in votes.values() if v == "AGAINST")
        
        result = "PASS" if for_count >= 3 else "REJECT"
        abort_reason = None
        if result == "REJECT":
            abort_reason = random.choice(["votes_insufficient", "van_tharp_limit", "period_queen_halt"])
        
        vote_data = {
            "memorial_id": memorial_id,
            "votes": votes,
            "for": for_count,
            "against": against_count,
            "result": result,
            "abort_reason": abort_reason,
        }
        
        self.event_stream.log(
            "vote",
            f"投票 {memorial_id}: {for_count}-{against_count} → {'通过' if result == 'PASS' else '否决'}"
            + (f" [ABORT: {abort_reason}]" if abort_reason else ""),
            vote_data,
        )
        
        return vote_data
    
    def simulate_mode_suggestion(self, current_mode: RegimeMode) -> Optional[RegimeMode]:
        """基于对象卡结果模拟模式切换建议"""
        volfac = self.card_results.get("VOLFAC", {})
        strength = volfac.get("signal_strength", 0)
        
        # 简单规则：VOLFAC 信号强度 → 模式建议
        if strength <= -2 and current_mode != RegimeMode.CRISIS:
            return RegimeMode.CRISIS
        elif strength == -1 and current_mode not in (RegimeMode.BEAR, RegimeMode.CRISIS):
            return RegimeMode.BEAR
        elif strength >= 2 and current_mode not in (RegimeMode.BULL, RegimeMode.CRISIS):
            return RegimeMode.BULL
        return None
    
    def get_card_summary(self) -> Dict[str, Any]:
        """获取所有对象卡摘要"""
        active = sum(1 for c in self.card_results.values() if c.get("status") == "done")
        return {
            "total": len(self.OBJECT_CARDS),
            "active": active,
            "standby": len(self.OBJECT_CARDS) - active,
            "last_run": self.last_sim_time or "-",
        }


# ============================================================================
# v2.0 控制台引擎（基于 v1.0 增强）
# ============================================================================

class EmperorConsoleV2:
    """御前会议控制台 v2.0"""
    
    def __init__(self):
        self.mode = RegimeMode.NORMAL
        self.mode_start = datetime.now()
        self.cooldown_end: Optional[datetime] = None
        
        # v1.0 数据
        self.memorials: list[Memorial] = []
        self.positions: list[Position] = [
            Position("000001.SZ", 6.0, 12.50, 13.20, 11.80, "normal"),
            Position("000002.SZ", 4.0, 25.00, 23.50, 22.00, "watch"),
            Position("000010.SZ", 5.0, 8.00, 8.50, 7.50, "normal"),
        ]
        
        self.pq_state = "POWER_TRANSITION"
        self.macro_score = 62
        self.csi300_change = 0.8
        self.limit_up = 45
        self.limit_down = 12
        
        # v2.0 新增
        self.event_stream = EventStream()
        self.sim_engine = SimulationEngine(self.event_stream)
        self.simulation_active = False
        self.simulation_counter = 0
        
        self._generate_sample_memorials()
        self.event_stream.log("system", "控制台 v2.0 启动", {"version": "2.0"})
    
    def _generate_sample_memorials(self):
        """生成示例奏折"""
        config = MODE_CONFIG[self.mode]
        
        if self.mode == RegimeMode.BEAR:
            self.memorials = [
                Memorial("ZHE-201", "000100.SZ", "减仓50%", 0.0, 0, [], Verdict.PASS, "止损触发"),
                Memorial("ZHE-202", "000200.SZ", "全部卖出", 0.0, 0, [], Verdict.PASS, "止盈触发"),
            ]
        elif self.mode == RegimeMode.CRISIS:
            self.memorials = [
                Memorial("ZHE-301", "000100.SZ", "清仓", 0.0, 0, [], Verdict.PASS, "流动性危机"),
            ]
        else:
            self.memorials = [
                Memorial("ZHE-001", "000001.SZ", "买入", 6.0, 8, ["CHZL_BSD", "BPB", "MFLOW"], Verdict.PASS, ""),
                Memorial("ZHE-002", "000002.SZ", "买入", 4.0, 7, ["CHZL_BSD", "TKR7"], Verdict.PASS, ""),
                Memorial("ZHE-003", "000003.SZ", "买入", 5.0, 6, ["BPB"], Verdict.REJECT, "对象卡数量不足，兵科封驳"),
            ]
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    # ------------------------------------------------------------------
    # v1.0 面板（完全保留）
    # ------------------------------------------------------------------
    
    def print_header(self):
        config = MODE_CONFIG[self.mode]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = "═" * 70
        print(c(f"╔{line}╗", config["color"]))
        title = f"[御前会议 v2.0]         投资管家控制台          {now}"
        print(c(f"║ {title:<69}║", config["color"]))
        print(c(f"╠{line}╣", config["color"]))
        print()
    
    def print_regime_panel(self):
        config = MODE_CONFIG[self.mode]
        mc = config["color"]
        
        print(c("┌─ 国朝制度 ─────────────────────────────────────────────┐", mc))
        print(c(f"│  当前模式: [{config['name']}]                              │", mc))
        
        if self.mode == RegimeMode.CRISIS:
            print(c("│  ⚠️  内阁停摆 | 六科解散 | 台谏待命                    │", Colors.BRIGHT_RED))
        elif self.mode == RegimeMode.BULL:
            print(c("│  ⚡ 快速通道: 开启 (本月成功率 75%)                     │", Colors.BRIGHT_GREEN))
        elif self.mode == RegimeMode.BEAR:
            print(c("│  🛡️ 新仓禁令: 已生效 | 仅允许减仓/止损                 │", Colors.BRIGHT_YELLOW))
        
        if self.cooldown_end and datetime.now() < self.cooldown_end:
            remaining = (self.cooldown_end - datetime.now()).total_seconds() // 3600
            print(c(f"│  冷却期剩余: {remaining:.0f} 小时                                  │", Colors.YELLOW))
        
        print(c("│  [1]切换模式 [2]查看历史 [3]系统复盘 [4]运行对象卡     │", Colors.DIM))
        print(c("└────────────────────────────────────────────────────────┘", mc))
        print()
    
    def print_market_panel(self):
        config = MODE_CONFIG[self.mode]
        mc = config["color"]
        
        print(c("┌─ 天时地利 ─────────────────────────────────────────────┐", mc))
        
        pq_color = Colors.GREEN if self.pq_state in ["ATTACK_SUSTAINED", "REMAINING_WARMTH"] else \
                   Colors.RED if self.pq_state in ["BEAR_LOOKING_UP", "MACRO_CALIBRATION", "EXTREME_VOL"] else \
                   Colors.YELLOW
        
        print(f"│  PeriodQueen:  {c(self.pq_state, pq_color, bold=True):<45}│")
        
        bar = "█" * (self.macro_score // 10) + "░" * (10 - self.macro_score // 10)
        print(f"│  宏观评分:     {self.macro_score}/100  [{c(bar, Colors.BRIGHT_BLUE)}]                 │")
        
        csi_color = Colors.GREEN if self.csi300_change > 0 else Colors.RED
        print(f"│  沪深300:      {c(f'{self.csi300_change:+.1f}%', csi_color):<45}│")
        print(f"│  涨跌停:       涨{self.limit_up} / 跌{self.limit_down:<40}│")
        print(c("└────────────────────────────────────────────────────────┘", mc))
        print()
    
    def print_cabinet_panel(self):
        config = MODE_CONFIG[self.mode]
        mc = config["color"]
        
        print(c("┌─ 内阁 ─────────────────────────────────────────────────┐", mc))
        
        shoufu_status = "🟢" if "停摆" not in config["shoufu_role"] else "🔴"
        cifu_status = "🟢" if "停摆" not in config["cifu_role"] else "🔴"
        
        print(f"│  {shoufu_status} 首辅: {config['shoufu_role']:<45}│")
        print(f"│  {cifu_status} 次辅: {config['cifu_role']:<45}│")
        print(f"│                                                        │")
        
        passed = sum(1 for m in self.memorials if m.verdict == Verdict.PASS)
        rejected = sum(1 for m in self.memorials if m.verdict == Verdict.REJECT)
        print(f"│  今日票拟: {len(self.memorials)} 笔  |  通过: {c(str(passed), Colors.GREEN)}  |  封驳: {c(str(rejected), Colors.RED):<15}│")
        print(c("└────────────────────────────────────────────────────────┘", mc))
        print()
    
    def print_six_departments(self):
        config = MODE_CONFIG[self.mode]
        mc = config["color"]
        
        print(c("┌─ 六科给事中 ───────────────────────────────────────────┐", mc))
        
        dept_names = {"li": "吏科", "hu": "户科", "bing": "兵科", "xing": "刑科", "gong": "工科"}
        
        def dept_color(val):
            if "免检" in val or "解散" in val:
                return Colors.DIM
            if "独裁" in val or "事后" in val:
                return Colors.BRIGHT_RED
            return Colors.GREEN
        
        print(f"│  {c(dept_names['li'], dept_color(config['li']))} {config['li']:<10}  {c(dept_names['hu'], dept_color(config['hu']))} {config['hu']:<15}│")
        print(f"│  {c(dept_names['bing'], dept_color(config['bing']))} {config['bing']:<10}  {c(dept_names['xing'], dept_color(config['xing']))} {config['xing']:<15}│")
        print(f"│  {c(dept_names['gong'], dept_color(config['gong']))} {config['gong']:<10}                                        │")
        print(c("└────────────────────────────────────────────────────────┘", mc))
        print()
    
    def print_memorials_table(self):
        config = MODE_CONFIG[self.mode]
        mc = config["color"]
        
        title = "待批红奏折" if self.mode != RegimeMode.BEAR else "待批红奏折（仅减仓/持有）"
        print(c(f"┌─ {title} {'─' * (51 - len(title))}┐", mc))
        print("│  编号       标的        方向      仓位   信心   六科      │")
        print("│  ─────────────────────────────────────────────────────  │")
        
        for m in self.memorials:
            v_icon = c("✅通过", Colors.GREEN) if m.verdict == Verdict.PASS else \
                     c("❌封驳", Colors.RED) if m.verdict == Verdict.REJECT else \
                     c("⏸️留中", Colors.YELLOW)
            
            conf_color = Colors.GREEN if m.confidence >= 7 else Colors.YELLOW if m.confidence >= 5 else Colors.RED
            
            line = f"│  {m.memorial_id}  {m.symbol:<10} {m.direction:<8} {m.size_pct:>4.0f}%  {c(str(m.confidence), conf_color):>4}/10  {v_icon:<10}│"
            print(line)
            
            if m.reviewer_comment:
                print(f"│      备注: {c(m.reviewer_comment, Colors.YELLOW):<47}│")
        
        if not self.memorials:
            print("│  (无待批红奏折)                                        │")
        
        print(c("└────────────────────────────────────────────────────────┘", mc))
        print()
    
    def print_portfolio_summary(self):
        config = MODE_CONFIG[self.mode]
        mc = config["color"]
        
        print(c("┌─ 持仓诊断 ─────────────────────────────────────────────┐", mc))
        
        total_risk = sum((p.current - p.stop) / p.current * p.size_pct for p in self.positions)
        
        print(f"│  总仓位: {c('60%', Colors.YELLOW)}  现金: 40%  总风险: {c(f'{total_risk:.1f}%', Colors.GREEN if total_risk < 6 else Colors.RED)}            │")
        print("│                                                        │")
        print("│  标的        仓位   成本    现价    盈亏     状态       │")
        print("│  ────────────────────────────────────────────────────  │")
        
        for p in self.positions:
            pnl = (p.current - p.cost) / p.cost * 100
            pnl_color = Colors.GREEN if pnl > 0 else Colors.RED
            status_icon = "🟢正常" if p.status == "normal" else "🟡关注" if p.status == "watch" else "🔴预警"
            
            print(f"│  {p.symbol}  {p.size_pct:>4.0f}%  {p.cost:>6.2f}  {p.current:>6.2f}  {c(f'{pnl:+.1f}%', pnl_color):>8}  {status_icon:<8}│")
        
        print(c("└────────────────────────────────────────────────────────┘", mc))
        print()
    
    # ------------------------------------------------------------------
    # v2.0 新增面板
    # ------------------------------------------------------------------
    
    def print_object_card_panel(self):
        """对象卡实时状态面板"""
        config = MODE_CONFIG[self.mode]
        mc = config["color"]
        
        print(c("┌─ 对象卡实时运行 ───────────────────────────────────────┐", mc))
        
        summary = self.sim_engine.get_card_summary()
        print(f"│  运行: {summary['active']}/{summary['total']}  待机: {summary['standby']}  最后运行: {summary['last_run']:<25}│")
        print("│  ─────────────────────────────────────────────────────  │")
        print("│  对象卡    信号   强度  置信度  过滤动作    缩放  状态   │")
        print("│  ─────────────────────────────────────────────────────  │")
        
        for card_name, result in self.sim_engine.card_results.items():
            status = result.get("status", "standby")
            if status == "standby":
                print(f"│  {card_name:<8}  {'-':<6}  {'-':<3}  {'-':<5}  {'-':<8}  {'-':<4}  {c('⚪待机', Colors.DIM):<6}│")
            elif status == "error":
                print(f"│  {card_name:<8}  {'-':<6}  {'-':<3}  {'-':<5}  {'-':<8}  {'-':<4}  {c('🔴错误', Colors.RED):<6}│")
            else:
                sig = result.get("signal_type", "-")
                strength = result.get("signal_strength", 0)
                conf = result.get("confidence", 0.0)
                filt = result.get("filter_action", "-")
                scalar = result.get("size_scalar", 1.0)
                
                st_color = Colors.GREEN if strength > 0 else Colors.RED if strength < 0 else Colors.YELLOW
                st_str = f"{strength:+d}"
                conf_str = f"{conf:.2f}" if conf > 0 else "-"
                scalar_str = f"{scalar:.1f}"
                
                print(f"│  {card_name:<8}  {sig:<6}  {c(st_str, st_color):<3}  {conf_str:<5}  {filt:<8}  {scalar_str:<4}  {c('🟢完成', Colors.GREEN):<6}│")
        
        print(c("└────────────────────────────────────────────────────────┘", mc))
        print()
    
    def print_event_stream(self):
        """事件流面板（增强起居注）"""
        config = MODE_CONFIG[self.mode]
        mc = config["color"]
        
        print(c("┌─ 起居注（增强版）──────────────────────────────────────┐", mc))
        
        recent = self.event_stream.get_recent(6)
        if not recent:
            print("│  (暂无事件)                                            │")
        else:
            for ev in recent:
                type_color = {
                    "system": Colors.BRIGHT_CYAN,
                    "card_run": Colors.GREEN,
                    "vote": Colors.YELLOW,
                    "abort": Colors.RED,
                    "mode_switch": Colors.BRIGHT_MAGENTA,
                    "trade": Colors.BRIGHT_BLUE,
                }.get(ev.event_type, Colors.WHITE)
                
                type_icon = {
                    "system": "⚙️",
                    "card_run": "📊",
                    "vote": "🗳️",
                    "abort": "🚫",
                    "mode_switch": "🔄",
                    "trade": "💰",
                }.get(ev.event_type, "•")
                
                print(f"│  {type_icon} {c(ev.timestamp, Colors.DIM)} {c(ev.event_type, type_color):<8} {ev.detail[:42]:<42}│")
        
        # 统计
        summary = self.event_stream.summary()
        if summary:
            stats = " | ".join([f"{k}:{v}" for k, v in summary.items()])
            print(f"│  {c('─' * 55, Colors.DIM)}│")
            print(f"│  {c(stats, Colors.DIM):<55}│")
        
        print(c("└────────────────────────────────────────────────────────┘", mc))
        print()
    
    def print_abort_reference(self):
        """ABORT 原因编码参考面板"""
        config = MODE_CONFIG[self.mode]
        mc = config["color"]
        
        print(c("┌─ ABORT 原因编码参考 ───────────────────────────────────┐", mc))
        
        aborts = [
            ("missing_ohlcv", "数据缺失"),
            ("period_queen_halt", "PeriodQueen 暂停"),
            ("period_queen_unclear", "PeriodQueen 不明确"),
            ("no_votes", "无投票"),
            ("all_blocked", "全部被阻断"),
            ("votes_insufficient", "票数不足"),
            ("van_tharp_limit", "VanTharp 风控限制"),
        ]
        
        for code, desc in aborts:
            print(f"│  {c(code, Colors.RED):<22} {desc:<30}│")
        
        print(f"│  {c('...', Colors.DIM):<55}│")
        print(f"│  {c('共14种标准编码，详见 VOTE_DECISION_TABLE', Colors.DIM):<55}│")
        print(c("└────────────────────────────────────────────────────────┘", mc))
        print()
    
    def print_simulation_controls(self):
        """模拟控制面板"""
        config = MODE_CONFIG[self.mode]
        mc = config["color"]
        
        print(c("┌─ 模拟控制 ─────────────────────────────────────────────┐", mc))
        
        if self.simulation_active:
            status = c("🟢 运行中", Colors.BRIGHT_GREEN)
        else:
            status = c("⚪ 待机", Colors.DIM)
        
        print(f"│  模拟状态: {status:<45}│")
        print(f"│  运行次数: {self.simulation_counter:<45}│")
        print(f"│                                                        │")
        print(f"│  [sim]运行对象卡  [vote]模拟投票  [mode]模式建议      │")
        print(f"│  [hist]事件历史   [clear]清空事件                      │")
        print(c("└────────────────────────────────────────────────────────┘", mc))
        print()
    
    # ------------------------------------------------------------------
    # 快捷操作（v1.0 + v2.0 合并）
    # ------------------------------------------------------------------
    
    def print_quick_actions(self):
        config = MODE_CONFIG[self.mode]
        mc = config["color"]
        
        print(c("┌─ 快捷操作 ─────────────────────────────────────────────┐", mc))
        print("│                                                        │")
        print("│  [a]批红全部  [d]留中全部  [v]查看详情  [r]系统复盘     │")
        print("│  [m]切换模式  [s]参数设置  [o]对象卡    [p]持仓诊断     │")
        print("│  [sim]运行模拟 [vote]投票  [hist]历史   [abort]编码参考 │")
        print("│                                                        │")
        
        if self.mode == RegimeMode.CRISIS:
            print(c("│  [L]一键清仓  [F]一键满仓  [A]任命独裁官                │", Colors.BRIGHT_RED))
        else:
            print(f"│  {c('[L]一键清仓', Colors.BRIGHT_RED)}                    {c('[D]生成日报', Colors.BRIGHT_BLUE)}                │")
        
        print("│                                                        │")
        print(c("└────────────────────────────────────────────────────────┘", mc))
        print()
    
    def print_footer(self):
        config = MODE_CONFIG[self.mode]
        mc = config["color"]
        
        line = "═" * 70
        print(c(f"╚{line}╝", mc))
        print()
        print(c("操作提示: 输入字母选择操作，或输入 memorial_id 查看详情", Colors.DIM))
        print(c("v2.0新增: sim / vote / hist / abort 命令", Colors.BRIGHT_GREEN))
        print(c("命令: ", Colors.BOLD), end="")
    
    # ------------------------------------------------------------------
    # 主渲染
    # ------------------------------------------------------------------
    
    def render_dashboard(self):
        self.clear_screen()
        self.print_header()
        self.print_regime_panel()
        self.print_market_panel()
        self.print_cabinet_panel()
        self.print_six_departments()
        self.print_object_card_panel()    # v2.0 新增
        self.print_memorials_table()
        self.print_portfolio_summary()
        self.print_simulation_controls()    # v2.0 新增
        self.print_event_stream()           # v2.0 新增
        self.print_quick_actions()
        self.print_footer()
    
    # ------------------------------------------------------------------
    # v2.0 新增操作
    # ------------------------------------------------------------------
    
    def run_simulation(self):
        """运行对象卡模拟"""
        self.clear_screen()
        print(c("╔══════════════════════════════════════════════════════════════════════╗", Colors.BRIGHT_GREEN))
        print(c("║  运行对象卡模拟                                                      ║", Colors.BRIGHT_GREEN))
        print(c("╠══════════════════════════════════════════════════════════════════════╣", Colors.BRIGHT_GREEN))
        print()
        
        symbols = ["000001.SZ", "000002.SZ", "600000.SH", "600519.SH", "300750.SZ"]
        
        for symbol in symbols:
            print(f"  正在运行 {symbol}...")
            self.sim_engine.run_all_cards(symbol)
            time.sleep(0.1)  # 模拟计算时间
        
        self.simulation_active = True
        self.simulation_counter += 1
        
        print()
        print(c("  ✅ 对象卡模拟完成", Colors.GREEN))
        print()
        
        # 显示模式建议
        suggestion = self.sim_engine.simulate_mode_suggestion(self.mode)
        if suggestion:
            print(c(f"  ⚠️  模式切换建议: {MODE_CONFIG[suggestion]['name']}", Colors.YELLOW))
            print(f"  原因: VOLFAC 信号强度={self.sim_engine.card_results['VOLFAC'].get('signal_strength', 0)}")
        else:
            print(c("  ✅ 当前模式无需切换", Colors.GREEN))
        
        input(c("\n按 Enter 返回...", Colors.DIM))
    
    def run_vote_simulation(self):
        """运行投票模拟"""
        self.clear_screen()
        print(c("╔══════════════════════════════════════════════════════════════════════╗", Colors.BRIGHT_YELLOW))
        print(c("║  模拟投票过程                                                        ║", Colors.BRIGHT_YELLOW))
        print(c("╠══════════════════════════════════════════════════════════════════════╣", Colors.BRIGHT_YELLOW))
        print()
        
        if not self.memorials:
            print("  (无待投票奏折)")
        else:
            for m in self.memorials:
                result = self.sim_engine.simulate_vote(m.memorial_id)
                print(f"  {m.memorial_id} {m.symbol}: ", end="")
                
                for card, vote in result["votes"].items():
                    v_color = Colors.GREEN if vote == "FOR" else Colors.RED if vote == "AGAINST" else Colors.DIM
                    print(c(f"{card}:{vote[0]}", v_color), end=" ")
                
                if result["result"] == "PASS":
                    print(c(" → ✅ 通过", Colors.GREEN))
                else:
                    print(c(f" → ❌ 否决 [{result['abort_reason']}]", Colors.RED))
        
        input(c("\n按 Enter 返回...", Colors.DIM))
    
    def show_event_history(self):
        """显示完整事件历史"""
        self.clear_screen()
        print(c("╔══════════════════════════════════════════════════════════════════════╗", Colors.BRIGHT_BLUE))
        print(c("║  事件历史                                                            ║", Colors.BRIGHT_BLUE))
        print(c("╠══════════════════════════════════════════════════════════════════════╣", Colors.BRIGHT_BLUE))
        print()
        
        all_events = self.event_stream.records
        if not all_events:
            print("  (暂无事件)")
        else:
            print(f"  共 {len(all_events)} 条事件")
            print()
            for ev in all_events:
                type_color = {
                    "system": Colors.BRIGHT_CYAN,
                    "card_run": Colors.GREEN,
                    "vote": Colors.YELLOW,
                    "abort": Colors.RED,
                    "mode_switch": Colors.BRIGHT_MAGENTA,
                }.get(ev.event_type, Colors.WHITE)
                print(f"  {ev.timestamp}  {c(ev.event_type, type_color):<10}  {ev.detail}")
        
        input(c("\n按 Enter 返回...", Colors.DIM))
    
    def show_abort_reference(self):
        """显示 ABORT 编码参考"""
        self.clear_screen()
        print(c("╔══════════════════════════════════════════════════════════════════════╗", Colors.BRIGHT_RED))
        print(c("║  ABORT 原因编码参考（14种标准编码）                                  ║", Colors.BRIGHT_RED))
        print(c("╠══════════════════════════════════════════════════════════════════════╣", Colors.BRIGHT_RED))
        print()
        
        aborts = [
            ("missing_ohlcv", "OHLCV 数据缺失，对象卡无法计算"),
            ("period_queen_halt", "PeriodQueen 判定当前状态不允许交易"),
            ("period_queen_unclear", "PeriodQueen 状态不明确，无法决策"),
            ("no_votes", "无投票对象，无法形成决策"),
            ("all_blocked", "所有对象卡信号被阻断"),
            ("votes_insufficient", "投票数不足，未达到通过门槛"),
            ("van_tharp_limit", "VanTharp 风控限制触发"),
            ("position_too_small", "目标仓位过小，不满足最小交易单位"),
            ("no_positions_to_exit", "无持仓可退出"),
            ("insufficient_exit_signals", "退出信号不足"),
            ("global_block", "全局阻断（市场停牌等）"),
            ("maturity_unverified", "对象卡成熟度未验证"),
            ("level2_missing", "Level-2 数据缺失（ATRATIO 等）"),
            ("market_halt", "市场停牌或涨跌停"),
        ]
        
        for i, (code, desc) in enumerate(aborts, 1):
            print(f"  {i:2d}. {c(code, Colors.RED):<22}  {desc}")
        
        print()
        print(c("  说明: 当投票被否决时，系统会输出其中一个编码作为原因", Colors.DIM))
        input(c("\n按 Enter 返回...", Colors.DIM))
    
    # ------------------------------------------------------------------
    # v1.0 操作（完全保留）
    # ------------------------------------------------------------------
    
    def switch_mode(self, new_mode: RegimeMode):
        old_mode = self.mode
        self.mode = new_mode
        self.mode_start = datetime.now()
        self.cooldown_end = datetime.now() + timedelta(days=3)
        self._generate_sample_memorials()
        
        self.event_stream.log(
            "mode_switch",
            f"{MODE_CONFIG[old_mode]['name']} → {MODE_CONFIG[new_mode]['name']}",
            {"from": old_mode.value, "to": new_mode.value},
        )
        
        print(c(f"\n✅ 已切换至 {MODE_CONFIG[new_mode]['name']} 模式", Colors.BRIGHT_GREEN))
        print(c(f"   冷却期: 3 个交易日", Colors.DIM))
        input(c("\n按 Enter 继续...", Colors.DIM))
    
    def show_mode_selector(self):
        self.clear_screen()
        print(c("╔══════════════════════════════════════════════════════════════════════╗", Colors.BRIGHT_CYAN))
        print(c("║                     切换国朝制度                                     ║", Colors.BRIGHT_CYAN))
        print(c("╠══════════════════════════════════════════════════════════════════════╣", Colors.BRIGHT_CYAN))
        print()
        print(f"  当前模式: {c(MODE_CONFIG[self.mode]['name'], MODE_CONFIG[self.mode]['color'], bold=True)}")
        print()
        print("  [1] 常态内阁模式    ── 首辅+次辅联合票拟，六科标准审查")
        print("  [2] 牛市集权模式    ── 首辅独断，六科从简，快速通道")
        print("  [3] 熊市监察模式    ── 台谏前置，六科加严，禁止开新仓")
        print("  [4] 震荡分权模式    ── 三省严格分离，互相牵制")
        print("  [5] 危机独裁模式    ── 内阁停摆，任命独裁官，用户接管")
        print()
        print(c("  ⚠️  切换后将进入 3 天冷却期，期间不能再次切换", Colors.YELLOW))
        print()
        
        choice = input(c("  请选择 [1-5] 或 [q]取消: ", Colors.BOLD))
        
        mode_map = {"1": RegimeMode.NORMAL, "2": RegimeMode.BULL, "3": RegimeMode.BEAR,
                    "4": RegimeMode.OSCILLATION, "5": RegimeMode.CRISIS}
        
        if choice in mode_map:
            reason = input(c("  切换原因: ", Colors.BOLD))
            self.switch_mode(mode_map[choice])
    
    def show_memorial_detail(self, memorial_id: str):
        memorial = next((m for m in self.memorials if m.memorial_id == memorial_id), None)
        if not memorial:
            print(c(f"\n❌ 未找到奏折 {memorial_id}", Colors.RED))
            input(c("\n按 Enter 继续...", Colors.DIM))
            return
        
        self.clear_screen()
        config = MODE_CONFIG[self.mode]
        mc = config["color"]
        
        print(c("╔══════════════════════════════════════════════════════════════════════╗", mc))
        print(c(f"║  奏折详情                                          [{memorial_id}]   ║", mc))
        print(c("╠══════════════════════════════════════════════════════════════════════╣", mc))
        print()
        print(f"  呈报部门: 内阁（首辅+次辅联署）")
        print(f"  呈报时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print(c("  ┌─ 交易内容 ─────────────────────────────────────────────┐", mc))
        print(f"  │  标的:        {memorial.symbol}")
        print(f"  │  方向:        {memorial.direction}")
        print(f"  │  目标仓位:    {memorial.size_pct}%")
        print(f"  │  信心度:      {memorial.confidence}/10")
        print(c("  └────────────────────────────────────────────────────────┘", mc))
        print()
        print(c("  ┌─ 技术面依据 ───────────────────────────────────────────┐", mc))
        for obj in memorial.objects:
            print(f"  │  • {obj}")
        print(c("  └────────────────────────────────────────────────────────┘", mc))
        print()
        print(c("  ┌─ 六科审查 ─────────────────────────────────────────────┐", mc))
        if memorial.verdict == Verdict.PASS:
            print(c("  │  裁定: ✅ 通过  盖印: 六科印", Colors.GREEN))
        else:
            print(c(f"  │  裁定: ❌ 封驳  理由: {memorial.reviewer_comment}", Colors.RED))
        print(c("  └────────────────────────────────────────────────────────┘", mc))
        print()
        
        if memorial.verdict == Verdict.PASS:
            print(c("  [a]批红通过  [d]留中不发  [r]否决", Colors.BOLD))
        
        input(c("\n按 Enter 返回...", Colors.DIM))
    
    def show_review_report(self):
        self.clear_screen()
        print(c("╔══════════════════════════════════════════════════════════════════════╗", Colors.BRIGHT_BLUE))
        print(c("║  系统复盘报告                                                        ║", Colors.BRIGHT_BLUE))
        print(c("╠══════════════════════════════════════════════════════════════════════╣", Colors.BRIGHT_BLUE))
        print()
        print(c("  ┌─ 总体绩效 ─────────────────────────────────────────────┐", Colors.BRIGHT_BLUE))
        print("  │  总收益率:     +5.2%")
        print("  │  年化夏普:     1.2")
        print("  │  最大回撤:     -3.8%")
        print("  │  胜率:         58%")
        print("  │  盈亏比:       1.8")
        print(c("  └────────────────────────────────────────────────────────┘", Colors.BRIGHT_BLUE))
        print()
        print(c("  ┌─ 对象卡绩效 ───────────────────────────────────────────┐", Colors.BRIGHT_BLUE))
        print("  │  对象卡        投票   通过   胜率    贡献度   建议      │")
        print("  │  ────────────────────────────────────────────────────  │")
        print(f"  │  CHZL_BSD       12     10    {c('83%', Colors.GREEN)}    +2.1%   保持      │")
        print(f"  │  BPB            10      6    {c('60%', Colors.GREEN)}    +0.8%   保持      │")
        print(f"  │  MFLOW           8      3    {c('38%', Colors.RED)}    -1.2%   ⚠️审查    │")
        print(c("  └────────────────────────────────────────────────────────┘", Colors.BRIGHT_BLUE))
        print()
        input(c("\n按 Enter 返回...", Colors.DIM))
    
    # ------------------------------------------------------------------
    # 主循环（v2.0 增强命令）
    # ------------------------------------------------------------------
    
    def run(self):
        while True:
            self.render_dashboard()
            
            try:
                cmd = input().strip().lower()
            except (EOFError, KeyboardInterrupt):
                print(c("\n\n👋 退朝", Colors.BRIGHT_CYAN))
                break
            
            if cmd == "q":
                print(c("\n\n👋 退朝", Colors.BRIGHT_CYAN))
                break
            elif cmd == "m":
                self.show_mode_selector()
            elif cmd == "r":
                self.show_review_report()
            elif cmd == "v":
                mid = input(c("  输入奏折编号: ", Colors.BOLD)).strip().upper()
                self.show_memorial_detail(mid)
            elif cmd == "a":
                print(c("\n✅ 已批红全部奏折", Colors.GREEN))
                self.event_stream.log("trade", "批红全部奏折")
                input(c("\n按 Enter 继续...", Colors.DIM))
            elif cmd == "d":
                print(c("\n⏸️ 已留中全部奏折", Colors.YELLOW))
                self.event_stream.log("trade", "留中全部奏折")
                input(c("\n按 Enter 继续...", Colors.DIM))
            elif cmd == "p":
                self.clear_screen()
                self.print_portfolio_summary()
                input(c("\n按 Enter 继续...", Colors.DIM))
            elif cmd == "l":
                print(c("\n🔴🔴🔴 紧急清仓 🔴🔴🔴", Colors.BRIGHT_RED))
                confirm = input(c("  确认清仓？输入 yes: ", Colors.BRIGHT_RED)).strip().lower()
                if confirm == "yes":
                    print(c("\n✅ 清仓完成", Colors.GREEN))
                    self.event_stream.log("trade", "紧急清仓")
                input(c("\n按 Enter 继续...", Colors.DIM))
            # v2.0 新增命令
            elif cmd == "sim":
                self.run_simulation()
            elif cmd == "vote":
                self.run_vote_simulation()
            elif cmd == "hist":
                self.show_event_history()
            elif cmd == "abort":
                self.show_abort_reference()
            elif cmd == "clear":
                self.event_stream = EventStream()
                self.event_stream.log("system", "事件流已清空")
                print(c("\n✅ 事件流已清空", Colors.GREEN))
                input(c("\n按 Enter 继续...", Colors.DIM))
            else:
                if cmd.startswith("zhe-"):
                    self.show_memorial_detail(cmd.upper())
                else:
                    print(c(f"\n❓ 未知命令: {cmd}", Colors.YELLOW))
                    input(c("\n按 Enter 继续...", Colors.DIM))


# ============================================================================
# 入口
# ============================================================================

def main():
    console = EmperorConsoleV2()
    
    if len(sys.argv) > 1:
        mode_map = {
            "normal": RegimeMode.NORMAL,
            "bull": RegimeMode.BULL,
            "bear": RegimeMode.BEAR,
            "oscillation": RegimeMode.OSCILLATION,
            "crisis": RegimeMode.CRISIS,
        }
        if sys.argv[1] in mode_map:
            console.mode = mode_map[sys.argv[1]]
            console._generate_sample_memorials()
    
    console.run()


if __name__ == "__main__":
    main()
