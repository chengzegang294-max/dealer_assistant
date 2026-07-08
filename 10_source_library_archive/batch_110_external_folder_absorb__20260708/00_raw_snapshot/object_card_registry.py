"""
ObjectCardRegistry - 对象卡统一调度器 v1.0

用法示例:
    from object_card_registry import ObjectCardRegistry, generate_klines_anchored, KLine
    
    registry = ObjectCardRegistry()
    klines = generate_klines_anchored(base_price=100, end_price=120, n_days=252)
    result = registry.analyze("000001.SZ", klines, stock_name="平安银行")
    
    # 输出报告
    report = registry.generate_report(result)
    print(report)
    
    # 获取聚合信号
    print(f"最终信号: {result.final_signal}")
    print(f"仓位系数: {result.avg_size_scalar}")
"""

import json, math, random, numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class KLine:
    date: str
    open: float
    high: float
    low: float
    close: float
    vol: int
    amount: float

@dataclass
class CardResult:
    object_id: str
    signal_type: str
    signal_strength: float
    confidence: float
    lock_status: str
    filter_action: str
    risk_action: str
    size_scalar: float
    detail: Dict
    
    def to_dict(self):
        return {
            "object_id": self.object_id,
            "signal_type": self.signal_type,
            "signal_strength": self.signal_strength,
            "confidence": self.confidence,
            "lock_status": self.lock_status,
            "filter_action": self.filter_action,
            "risk_action": self.risk_action,
            "size_scalar": self.size_scalar,
            "detail": self.detail
        }

@dataclass
class AggregateResult:
    stock_code: str
    stock_name: str
    date: str
    price: float
    buy_votes: int
    sell_votes: int
    neutral_votes: int
    buy_score: float
    sell_score: float
    net_score: float
    avg_size_scalar: float
    permission: str
    final_signal: str
    blockers: List[str]
    card_results: List[Dict]
    fundamentals: Optional[Dict] = None
    user_cost: Optional[float] = None

# ---- 工具函数 ----
def sma(values, n):
    result = []
    for i in range(len(values)):
        if i < n - 1:
            result.append(sum(values[:i+1]) / (i+1))
        else:
            result.append(sum(values[i-n+1:i+1]) / n)
    return result

def ao_indicator(klines):
    mp = [(k.high + k.low) / 2 for k in klines]
    s5, s34 = sma(mp, 5), sma(mp, 34)
    return [s5[i] - s34[i] if i < len(s34) else 0 for i in range(len(s5))]

# ---- 12张对象卡实现 ----
def card_period_queen(klines):
    returns = [klines[i].close / klines[i-1].close - 1 for i in range(-30, 0)]
    vol = np.std(returns) * math.sqrt(252)
    trend = (klines[-1].close - klines[-20].close) / klines[-20].close
    if vol > 0.5: state = "POWER_TRANSITION"
    elif trend > 0.15: state = "ATTACK_SUSTAINED"
    elif trend > 0.05: state = "ATTACK_INITIAL"
    elif trend < -0.15: state = "CUTTING_COMPLETE"
    elif trend < -0.05: state = "CUTTING_START"
    else: state = "CONSOLIDATION"
    perm = {"ATTACK_SUSTAINED":"FULL","ATTACK_INITIAL":"FULL","CONSOLIDATION":"REDUCED","POWER_TRANSITION":"REDUCED","CUTTING_START":"EXIT_ONLY","CUTTING_COMPLETE":"HALT"}
    return CardResult("PERIOD_QUEEN_P0_F", f"STATE_{state}", round(abs(trend)*10,1), 0.65, "UNLOCKED", "PASS", f"PERMISSION_{perm.get(state,'REDUCED')}", 1.0 if state in ["ATTACK_SUSTAINED","ATTACK_INITIAL"] else 0.5, {"volatility_annual":round(vol,3),"trend_20d":round(trend,3),"state":state})

def card_volfac(klines):
    returns = [klines[i].close / klines[i-1].close - 1 for i in range(-60, 0)]
    vol = np.std(returns) * math.sqrt(252)
    hist_vols = [np.std(returns[max(0,i-20):i]) * math.sqrt(252) for i in range(20, len(returns))]
    percentile = sum(1 for v in hist_vols if v < vol) / max(1, len(hist_vols))
    regime = "EXTREME_VOL" if percentile > 0.8 else ("HIGH_VOL" if percentile > 0.6 else ("LOW_VOL" if percentile < 0.2 else "NORMAL"))
    sig = "SELL" if regime == "EXTREME_VOL" else ("HOLD" if regime in ["HIGH_VOL","NORMAL"] else "BUY")
    return CardResult("VOLFAC_P0_A", sig, round((percentile-0.5)*4,1), 0.7, "UNLOCKED", "BLOCK" if regime=="EXTREME_VOL" else "PASS", "DOWNSIZE" if regime=="HIGH_VOL" else "NORMAL", round(0.25/max(vol,0.1),2), {"annual_vol":round(vol,3),"percentile":round(percentile,2),"regime":regime})

def card_voltarget(klines, volfac_result):
    target_vol, current_vol = 0.25, volfac_result.detail.get("annual_vol", 0.3)
    scalar = min(target_vol / max(current_vol, 0.05), 2.0)
    return CardResult("VOLTARGET_P0_R", "VOL_ADJUST", round(scalar,2), 0.75, "UNLOCKED", "PASS", "SCALE_POSITION", round(scalar,2), {"target_vol":target_vol,"current_vol":round(current_vol,3),"position_scalar":round(scalar,2)})

def card_chzl(klines):
    if len(klines) < 5: return CardResult("CHZL_BSD_P0_E", "NEUTRAL", 0, 0.5, "UNLOCKED", "PASS", "NORMAL", 1.0, {})
    k1, k2, k3 = klines[-3], klines[-2], klines[-1]
    bf = k2.low < k1.low and k2.low < k3.low and k2.high < k1.high and k2.high < k3.high
    tf = k2.high > k1.high and k2.high > k3.high and k2.low > k1.low and k2.low > k3.low
    sig, strength = ("BUY",1.5) if bf else (("SELL",-1.5) if tf else ("NEUTRAL",0.0))
    return CardResult("CHZL_BSD_P0_E", sig, strength, 0.6, "UNLOCKED", "BLOCK" if sig=="SELL" else "PASS", "NORMAL", 1.0, {"bottom_fractal":bf,"top_fractal":tf})

def card_bpb(klines):
    if len(klines) < 30: return CardResult("BPB_P0_E", "NEUTRAL", 0, 0.5, "UNLOCKED", "PASS", "NORMAL", 1.0, {})
    highs = [k.high for k in klines[-20:]]
    max_high, max_idx = max(highs), highs.index(max(highs))
    if max_idx >= len(highs) - 5:
        low20 = min(k.low for k in klines[-20:])
        fib382 = max_high - (max_high - low20) * 0.382
        fib618 = max_high - (max_high - low20) * 0.618
        current = klines[-1].close
        if fib618 <= current <= fib382:
            return CardResult("BPB_P0_E", "BUY", 1.8, 0.55, "UNLOCKED", "PASS", "NORMAL", 1.0, {"fib_zone":"38.2%-61.8%","breakout_high":round(max_high,2)})
    return CardResult("BPB_P0_E", "NEUTRAL", 0, 0.5, "UNLOCKED", "PASS", "NORMAL", 1.0, {})

def card_tkr7(klines):
    ao_vals = ao_indicator(klines)
    if len(ao_vals) < 10: return CardResult("TKR7_P0_E", "NEUTRAL", 0, 0.5, "UNLOCKED", "PASS", "NORMAL", 1.0, {})
    pt, at = klines[-1].close - klines[-5].close, ao_vals[-1] - ao_vals[-5]
    sig, strength = ("SELL",-1.5) if pt>0 and at<0 else (("BUY",1.5) if pt<0 and at>0 else ("NEUTRAL",0.0))
    return CardResult("TKR7_P0_E", sig, strength, 0.6, "UNLOCKED", "BLOCK" if sig=="SELL" else "PASS", "NORMAL", 1.0, {"ao_current":round(ao_vals[-1],3),"ao_trend":round(at,3)})

def card_mflow(klines):
    recent = klines[-10:]
    up_vol = sum(k.vol for k in recent if k.close > k.open)
    down_vol = sum(k.vol for k in recent if k.close < k.open)
    total = up_vol + down_vol
    ratio = up_vol / total if total > 0 else 0.5
    sig, strength = ("BUY",1.5) if ratio > 0.65 else (("SELL",-1.5) if ratio < 0.35 else ("NEUTRAL",0.0))
    return CardResult("MFLOW_P0_A", sig, strength, 0.55, "UNLOCKED", "BLOCK" if sig=="SELL" else "PASS", "NORMAL", 1.0, {"up_down_ratio":round(ratio,2)})

def card_instb(klines):
    vol_ma = sum(k.vol for k in klines[-20:]) / 20
    rv = klines[-1].vol
    sig, strength = ("BUY",1.2) if rv > vol_ma * 2 else (("SELL",-0.8) if rv < vol_ma * 0.5 else ("NEUTRAL",0.0))
    return CardResult("INSTB_P0_A", sig, strength, 0.5, "UNLOCKED", "PASS", "NORMAL", 1.0, {"vol_vs_ma20":round(rv/vol_ma,2)})

def card_kelly(klines):
    returns = [klines[i].close / klines[i-1].close - 1 for i in range(-60, 0)]
    wins = [r for r in returns if r > 0]
    losses = [r for r in returns if r < 0]
    if not wins or not losses: return CardResult("KELLY_P0_R", "NEUTRAL", 0, 0.5, "UNLOCKED", "PASS", "NORMAL", 1.0, {})
    wr, aw, al = len(wins)/len(returns), sum(wins)/len(wins), abs(sum(losses)/len(losses))
    kelly = 0 if al == 0 else wr - (1-wr)/(aw/al)
    hk = max(0, kelly/2)
    return CardResult("KELLY_P0_R", "POSITION_SIZE", round(hk,3), 0.6, "UNLOCKED", "PASS", "SCALE_POSITION", round(min(hk,1.0),2), {"half_kelly":round(hk,3),"win_rate":round(wr,2)})

def card_vp(klines):
    price_vol = {}
    for k in klines[-30:]:
        bucket = round(k.close / 5) * 5
        price_vol[bucket] = price_vol.get(bucket, 0) + k.vol
    poc = max(price_vol, key=price_vol.get)
    current = round(klines[-1].close / 5) * 5
    sig, strength = ("SELL",-1.0) if current > poc+10 else (("BUY",1.0) if current < poc-10 else ("NEUTRAL",0.0))
    return CardResult("VP_P0_E", sig, strength, 0.55, "UNLOCKED", "PASS", "NORMAL", 1.0, {"poc_zone":poc,"current_zone":current})

def card_ytc(klines):
    k = klines[-1]
    body, range_ = abs(k.close - k.open), k.high - k.low
    ratio = body / range_ if range_ > 0 else 0
    sig, strength = ("BUY",1.5) if ratio > 0.7 and k.close > k.open else (("SELL",-1.5) if ratio > 0.7 and k.close < k.open else ("NEUTRAL",0.0))
    return CardResult("YTC_P0_E", sig, strength, 0.5, "UNLOCKED", "BLOCK" if sig=="SELL" else "PASS", "NORMAL", 1.0, {"body_range_ratio":round(ratio,2)})

def card_atratio(klines):
    rv, vm = klines[-1].vol, sum(k.vol for k in klines[-20:]) / 20
    ratio = rv / vm if vm > 0 else 1.0
    sig, strength = ("BUY",1.2) if ratio > 2.0 else (("BUY",0.8) if ratio > 1.5 else ("NEUTRAL",0.0))
    return CardResult("ATRATIO_P0_A", sig, strength, 0.5, "UNLOCKED", "PASS", "NORMAL", 1.0, {"vol_ratio":round(ratio,2)})


class ObjectCardRegistry:
    """对象卡统一调度器 v1.0"""
    
    def __init__(self):
        self.cards = [
            ("PERIOD_QUEEN", card_period_queen, []),
            ("VOLFAC", card_volfac, []),
            ("CHZL_BSD", card_chzl, []),
            ("BPB", card_bpb, []),
            ("TKR7", card_tkr7, []),
            ("MFLOW", card_mflow, []),
            ("INSTB", card_instb, []),
            ("KELLY", card_kelly, []),
            ("VP", card_vp, []),
            ("YTC", card_ytc, []),
            ("ATRATIO", card_atratio, []),
        ]
    
    def run_all(self, klines: List[KLine]) -> List[CardResult]:
        results = []
        volfac_result = None
        for name, func, deps in self.cards:
            if name == "VOLFAC":
                r = func(klines)
                volfac_result = r
            else:
                r = func(klines)
            results.append(r)
        if volfac_result:
            results.append(card_voltarget(klines, volfac_result))
        return results
    
    def aggregate(self, results: List[CardResult]) -> Dict:
        buy_votes = [r for r in results if r.signal_type == "BUY"]
        sell_votes = [r for r in results if r.signal_type == "SELL"]
        neutral = [r for r in results if r.signal_type == "NEUTRAL"]
        buy_score = sum(r.signal_strength * r.confidence for r in buy_votes)
        sell_score = sum(abs(r.signal_strength) * r.confidence for r in sell_votes)
        size_scalars = [r.size_scalar for r in results if r.signal_type in ["BUY", "VOL_ADJUST", "POSITION_SIZE"] and r.size_scalar > 0]
        avg_size = sum(size_scalars) / len(size_scalars) if size_scalars else 1.0
        pq = next((r for r in results if r.object_id == "PERIOD_QUEEN_P0_F"), None)
        permission = pq.risk_action if pq else "PERMISSION_REDUCED"
        net = buy_score - sell_score
        final = "BUY" if net > 1.5 else ("SELL" if net < -1.5 else "NEUTRAL")
        return {
            "buy_votes": len(buy_votes), "sell_votes": len(sell_votes), "neutral_votes": len(neutral),
            "buy_score": round(buy_score, 2), "sell_score": round(sell_score, 2), "net_score": round(net, 2),
            "avg_size_scalar": round(avg_size, 2), "permission": permission,
            "final_signal": final, "blockers": [r.object_id for r in results if r.filter_action == "BLOCK"]
        }
    
    def analyze(self, stock_code: str, klines: List[KLine], stock_name: str = "",
                fundamentals: Optional[Dict] = None, user_cost: Optional[float] = None) -> AggregateResult:
        results = self.run_all(klines)
        agg = self.aggregate(results)
        return AggregateResult(
            stock_code=stock_code, stock_name=stock_name, date=klines[-1].date, price=klines[-1].close,
            buy_votes=agg["buy_votes"], sell_votes=agg["sell_votes"], neutral_votes=agg["neutral_votes"],
            buy_score=agg["buy_score"], sell_score=agg["sell_score"], net_score=agg["net_score"],
            avg_size_scalar=agg["avg_size_scalar"], permission=agg["permission"], final_signal=agg["final_signal"],
            blockers=agg["blockers"], card_results=[r.to_dict() for r in results],
            fundamentals=fundamentals, user_cost=user_cost
        )
    
    def generate_report(self, result: AggregateResult) -> str:
        lines = []
        def out(s): lines.append(s)
        out(f"# {result.stock_name} ({result.stock_code}) 对象卡系统分析报告")
        out(f"\n**分析日期**: {result.date}  ")
        out(f"**当前价格**: {result.price:.2f} 元")
        if result.user_cost:
            out(f"**用户成本**: {result.user_cost:.2f} 元")
            loss_pct = (result.price - result.user_cost) / result.user_cost * 100
            out(f"**当前盈亏**: {loss_pct:+.2f}%")
        out("")
        if result.fundamentals:
            out("## 基本面锚点")
            for k, v in result.fundamentals.items():
                out(f"- **{k}**: {v}")
            out("")
        out("## 对象卡独立运行结果")
        out("")
        out("| 对象卡 | 信号 | 强度 | 置信度 | 过滤 | 风控 | 仓位系数 |")
        out("|--------|------|------|--------|------|------|----------|")
        for cr in result.card_results:
            out(f"| {cr['object_id']} | {cr['signal_type']} | {cr['signal_strength']} | {cr['confidence']} | {cr['filter_action']} | {cr['risk_action']} | {cr['size_scalar']} |")
        out("")
        out("## 聚合投票结果")
        out("")
        out(f"- **BUY 票**: {result.buy_votes}")
        out(f"- **SELL 票**: {result.sell_votes}")
        out(f"- **NEUTRAL**: {result.neutral_votes}")
        out(f"- **BUY加权得分**: {result.buy_score}")
        out(f"- **SELL加权得分**: {result.sell_score}")
        out(f"- **净得分**: {result.net_score}")
        out(f"- **平均仓位系数**: {result.avg_size_scalar}")
        out(f"- **环境权限**: {result.permission}")
        out(f"- **阻塞对象卡**: {', '.join(result.blockers) if result.blockers else '无'}")
        out("")
        signal_emoji = {"BUY": "🔵", "SELL": "🔴", "NEUTRAL": "⚪"}
        emoji = signal_emoji.get(result.final_signal, "⚪")
        out(f"## 🏁 最终信号: {emoji} {result.final_signal}")
        out("")
        if result.final_signal == "BUY":
            out(f"> **建议**: 多头配置，可建仓/加仓，建议仓位系数 {result.avg_size_scalar:.1f}x")
        elif result.final_signal == "SELL":
            out("> **建议**: 减仓/回避，建议减仓或观望")
        else:
            out("> **建议**: 中性观望，维持现有仓位，等待更明确信号")
        out("")
        return "\n".join(lines)


def generate_klines_anchored(base_price: float, end_price: float, n_days: int = 252,
                              volatility: float = 0.025, seed: int = 42,
                              trend_bias: float = 0.0) -> List[KLine]:
    random.seed(seed)
    np.random.seed(seed)
    end_date = datetime(2026, 7, 7)
    klines = []
    price = base_price
    for i in range(n_days - 1):
        d = end_date - timedelta(days=n_days - 1 - i)
        while d.weekday() >= 5:
            d -= timedelta(days=1)
        change = random.gauss(trend_bias, volatility)
        price *= (1 + change)
        price = max(base_price * 0.3, min(base_price * 3, price))
        o = price * (1 + random.gauss(0, 0.005))
        c = price
        h = max(o, c) * (1 + abs(random.gauss(0, 0.01)))
        l = min(o, c) * (1 - abs(random.gauss(0, 0.01)))
        v = max(10000, int(random.gauss(150000, 50000)))
        klines.append(KLine(d.strftime('%Y-%m-%d'), round(o,2), round(h,2), round(l,2), round(c,2), v, round(v*c,2)))
    d = end_date
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    prev_close = klines[-1].close if klines else base_price
    last_change = (end_price - prev_close) / prev_close
    o = end_price / (1 + last_change * random.uniform(0.3, 0.7))
    h = max(o, end_price) * (1 + abs(random.gauss(0, 0.005)))
    l = min(o, end_price) * (1 - abs(random.gauss(0, 0.005)))
    v = max(10000, int(random.gauss(180000, 60000)))
    klines.append(KLine(d.strftime('%Y-%m-%d'), round(o,2), round(h,2), round(l,2), round(end_price,2), v, round(v*end_price,2)))
    return klines


if __name__ == "__main__":
    # 示例运行
    registry = ObjectCardRegistry()
    klines = generate_klines_anchored(base_price=100, end_price=120, n_days=252)
    result = registry.analyze("000001.SZ", klines, stock_name="示例股票")
    print(registry.generate_report(result))
