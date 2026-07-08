#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
御前会议控制台原型 v1.0
======================
纯 ANSI 颜色实现，无需 rich 库
支持 5 种制度模式、奏折管理、六科审查、起居注

运行方式: python prototype_console.py
"""

import os
import sys
import json
import time
import random
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional


# ============================================================================
# ANSI 颜色码
# ============================================================================

class Colors:
    """ANSI 颜色码"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # 前景色
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # 亮前景色
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    
    # 背景色
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
    """给文本添加颜色"""
    prefix = ""
    if bold:
        prefix += Colors.BOLD
    prefix += color
    return f"{prefix}{text}{Colors.RESET}"


# ============================================================================
# 枚举定义
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
# 模式配置
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
# 数据模型
# ============================================================================

@dataclass
class Memorial:
    """奏折"""
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
    """持仓"""
    symbol: str
    size_pct: float
    cost: float
    current: float
    stop: float
    status: str = "normal"


# ============================================================================
# 控制台引擎
# ============================================================================

class EmperorConsole:
    """御前会议控制台"""
    
    def __init__(self):
        self.mode = RegimeMode.NORMAL
        self.mode_start = datetime.now()
        self.cooldown_end: Optional[datetime] = None
        
        # 模拟数据
        self.memorials: list[Memorial] = []
        self.positions: list[Position] = [
            Position("000001.SZ", 6.0, 12.50, 13.20, 11.80, "normal"),
            Position("000002.SZ", 4.0, 25.00, 23.50, 22.00, "watch"),
            Position("000010.SZ", 5.0, 8.00, 8.50, 7.50, "normal"),
        ]
        self.logs: list[str] = []
        
        self.pq_state = "POWER_TRANSITION"
        self.macro_score = 62
        self.csi300_change = 0.8
        self.limit_up = 45
        self.limit_down = 12
        
        self._generate_sample_memorials()
    
    def _generate_sample_memorials(self):
        """生成示例奏折"""
        config = MODE_CONFIG[self.mode]
        
        if self.mode == RegimeMode.BEAR:
            # 熊市：只有减仓
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
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """打印头部"""
        config = MODE_CONFIG[self.mode]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        line = "═" * 70
        print(c(f"╔{line}╗", config["color"]))
        title = f"[御前会议]              投资管家控制台          {now}"
        print(c(f"║ {title:<69}║", config["color"]))
        print(c(f"╠{line}╣", config["color"]))
        print()
    
    def print_regime_panel(self):
        """打印制度面板"""
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
        
        print(c("│  [1]切换模式 [2]查看历史 [3]系统复盘                   │", Colors.DIM))
        print(c("└────────────────────────────────────────────────────────┘", mc))
        print()
    
    def print_market_panel(self):
        """打印市场面板"""
        mc = MODE_CONFIG[self.mode]["color"]
        
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
        """打印内阁面板"""
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
        """打印六科状态"""
        config = MODE_CONFIG[self.mode]
        mc = config["color"]
        
        print(c("┌─ 六科给事中 ───────────────────────────────────────────┐", mc))
        
        # 科名到显示名的映射
        dept_names = {
            "li": "吏科", "hu": "户科", "bing": "兵科",
            "xing": "刑科", "gong": "工科"
        }
        
        # 显示颜色
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
        """打印待批红奏折表"""
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
        """打印持仓摘要"""
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
    
    def print_quick_actions(self):
        """打印快捷操作"""
        config = MODE_CONFIG[self.mode]
        mc = config["color"]
        
        print(c("┌─ 快捷操作 ─────────────────────────────────────────────┐", mc))
        print("│                                                        │")
        print("│  [a]批红全部  [d]留中全部  [v]查看详情  [r]系统复盘     │")
        print("│  [m]切换模式  [s]参数设置  [o]对象卡    [p]持仓诊断     │")
        print("│                                                        │")
        
        if self.mode == RegimeMode.CRISIS:
            print(c("│  [L]一键清仓  [F]一键满仓  [A]任命独裁官                │", Colors.BRIGHT_RED))
        else:
            print(f"│  {c('[L]一键清仓', Colors.BRIGHT_RED)}                    {c('[D]生成日报', Colors.BRIGHT_BLUE)}                │")
        
        print("│                                                        │")
        print(c("└────────────────────────────────────────────────────────┘", mc))
        print()
    
    def print_logs(self):
        """打印起居注"""
        config = MODE_CONFIG[self.mode]
        mc = config["color"]
        
        print(c("┌─ 起居注（最近5条）─────────────────────────────────────┐", mc))
        
        sample_logs = [
            f"{datetime.now().strftime('%H:%M')}  内阁提交 ZHE-001  买入 000001.SZ",
            f"{datetime.now().strftime('%H:%M')}  六科通过 ZHE-001  盖印",
            f"{datetime.now().strftime('%H:%M')}  内阁提交 ZHE-002  买入 000002.SZ",
            f"{datetime.now().strftime('%H:%M')}  六科通过 ZHE-002  盖印",
            f"{datetime.now().strftime('%H:%M')}  内阁提交 ZHE-003  → 兵科封驳",
        ]
        
        for log in sample_logs[-5:]:
            print(f"│  {log:<55}│")
        
        print(c("└────────────────────────────────────────────────────────┘", mc))
        print()
    
    def print_footer(self):
        """打印底部"""
        config = MODE_CONFIG[self.mode]
        mc = config["color"]
        
        line = "═" * 70
        print(c(f"╚{line}╝", mc))
        print()
        print(c("操作提示: 输入字母选择操作，或输入 memorial_id 查看详情", Colors.DIM))
        print(c("命令: ", Colors.BOLD), end="")
    
    def render_dashboard(self):
        """渲染主仪表盘"""
        self.clear_screen()
        self.print_header()
        self.print_regime_panel()
        self.print_market_panel()
        self.print_cabinet_panel()
        self.print_six_departments()
        self.print_memorials_table()
        self.print_portfolio_summary()
        self.print_quick_actions()
        self.print_logs()
        self.print_footer()
    
    def switch_mode(self, new_mode: RegimeMode):
        """切换模式"""
        old_mode = self.mode
        self.mode = new_mode
        self.mode_start = datetime.now()
        self.cooldown_end = datetime.now() + timedelta(days=3)
        self._generate_sample_memorials()
        
        print(c(f"\n✅ 已切换至 {MODE_CONFIG[new_mode]['name']} 模式", Colors.BRIGHT_GREEN))
        print(c(f"   冷却期: 3 个交易日", Colors.DIM))
        input(c("\n按 Enter 继续...", Colors.DIM))
    
    def show_mode_selector(self):
        """显示模式选择器"""
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
        
        mode_map = {
            "1": RegimeMode.NORMAL,
            "2": RegimeMode.BULL,
            "3": RegimeMode.BEAR,
            "4": RegimeMode.OSCILLATION,
            "5": RegimeMode.CRISIS,
        }
        
        if choice in mode_map:
            reason = input(c("  切换原因: ", Colors.BOLD))
            self.switch_mode(mode_map[choice])
    
    def show_memorial_detail(self, memorial_id: str):
        """显示奏折详情"""
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
        """显示系统复盘报告"""
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
    
    def run(self):
        """主循环"""
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
                input(c("\n按 Enter 继续...", Colors.DIM))
            elif cmd == "d":
                print(c("\n⏸️ 已留中全部奏折", Colors.YELLOW))
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
                input(c("\n按 Enter 继续...", Colors.DIM))
            else:
                # 尝试作为奏折编号查看
                if cmd.startswith("zhe-"):
                    self.show_memorial_detail(cmd.upper())


# ============================================================================
# 入口
# ============================================================================

def main():
    """主入口"""
    console = EmperorConsole()
    
    # 支持命令行参数切换模式
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
