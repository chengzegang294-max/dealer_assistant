# 瑞芯微 (603893.SH) — 对象卡系统聚合分析
# 演示模式：使用模拟K线数据跑完全部12张对象卡
# 时间：2026-07-07 收盘

import sys, json, math, random, numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum

# ============================================================
# 模拟K线数据生成（基于真实价格锚点）
# ============================================================
# 已知锚点：
#   2025-01-20: 144.0 (业绩预增前)
#   2025-01-24: 157.26 (涨停后高点161)
#   2025-05-30: 144.3 (回调)
#   2025-08-27: 163.60 (半年报后)
#   2025-09-10: 197.08
#   2026-07-07: 190.71 (当前，+8.28%)
# ============================================================

@dataclass
class KLine:
    date: str
    open: float
    high: float
    low: float
    close: float
    vol: int
    amount: float

# 基于真实事件节点生成252日模拟K线
def generate_rkx_klines() -> List[KLine]:
    klines = []
    base = 100.0
    # 从2025-07往回推252个交易日约1年
    # 简化为从2025-07-01开始生成到2026-07-07
    
    # 阶段1: 2025-01 ~ 2025-03 震荡筑底 80-110
    dates1 = []
    d = datetime(2025, 1, 2)
    while d <= datetime(2025, 3, 31):
        if d.weekday() < 5:
            dates1.append(d.strftime('%Y-%m-%d'))
        d += timedelta(days=1)
    
    price = 95.0
    for dt in dates1:
        change = random.gauss(0.002, 0.025)
        if dt == '2025-01-21':  # 业绩预增公告日
            change = 0.05  # 大涨
        elif dt in ['2025-01-22', '2025-01-23', '2025-01-24']:
            change = 0.03  # 连续上涨
        price *= (1 + change)
        price = max(80, min(130, price))
        o = price * (1 + random.gauss(0, 0.005))
        c = price
        h = max(o, c) * (1 + abs(random.gauss(0, 0.01)))
        l = min(o, c) * (1 - abs(random.gauss(0, 0.01)))
        v = int(random.gauss(150000, 50000))
        klines.append(KLine(dt, round(o,2), round(h,2), round(l,2), round(c,2), max(10000,v), round(v*c,2)))
    
    # 阶段2: 2025-04 ~ 2025-06 回调震荡 130-150
    dates2 = []
    d = datetime(2025, 4, 1)
    while d <= datetime(2025, 6, 30):
        if d.weekday() < 5:
            dates2.append(d.strftime('%Y-%m-%d'))
        d += timedelta(days=1)
    
    price = 140.0
    for dt in dates2:
        change = random.gauss(-0.001, 0.02)
        if dt == '2025-04-23':  # 股权激励
            change = 0.04
        elif dt == '2025-05-30':
            price = 144.3  # 锚定已知价格
        price *= (1 + change)
        price = max(125, min(155, price))
        o = price * (1 + random.gauss(0, 0.005))
        c = price
        h = max(o, c) * (1 + abs(random.gauss(0, 0.01)))
        l = min(o, c) * (1 - abs(random.gauss(0, 0.01)))
        v = int(random.gauss(120000, 40000))
        klines.append(KLine(dt, round(o,2), round(h,2), round(l,2), round(c,2), max(10000,v), round(v*c,2)))
    
    # 阶段3: 2025-07 ~ 2025-09 半年报行情上涨 150-200
    dates3 = []
    d = datetime(2025, 7, 1)
    while d <= datetime(2025, 9, 30):
        if d.weekday() < 5:
            dates3.append(d.strftime('%Y-%m-%d'))
        d += timedelta(days=1)
    
    price = 145.0
    for dt in dates3:
        change = random.gauss(0.003, 0.022)
        if dt == '2025-08-27':  # 半年报后大涨
            change = 0.06
            price = 163.60
        elif dt == '2025-09-10':
            price = 197.08  # 锚定
        price *= (1 + change)
        price = max(140, min(210, price))
        o = price * (1 + random.gauss(0, 0.005))
        c = price
        h = max(o, c) * (1 + abs(random.gauss(0, 0.012)))
        l = min(o, c) * (1 - abs(random.gauss(0, 0.012)))
        v = int(random.gauss(180000, 60000))
        klines.append(KLine(dt, round(o,2), round(h,2), round(l,2), round(c,2), max(10000,v), round(v*c,2)))
    
    # 阶段4: 2025-10 ~ 2026-06 高位震荡 170-210
    dates4 = []
    d = datetime(2025, 10, 1)
    while d <= datetime(2026, 6, 30):
        if d.weekday() < 5:
            dates4.append(d.strftime('%Y-%m-%d'))
        d += timedelta(days=1)
    
    price = 185.0
    for dt in dates4:
        change = random.gauss(0.001, 0.018)
        price *= (1 + change)
        price = max(165, min(210, price))
        o = price * (1 + random.gauss(0, 0.005))
        c = price
        h = max(o, c) * (1 + abs(random.gauss(0, 0.01)))
        l = min(o, c) * (1 - abs(random.gauss(0, 0.01)))
        v = int(random.gauss(160000, 50000))
        klines.append(KLine(dt, round(o,2), round(h,2), round(l,2), round(c,2), max(10000,v), round(v*c,2)))
    
    # 阶段5: 2026-07 当前
    klines.append(KLine('2026-07-07', 176.13, 190.71, 175.80, 190.71, 205214, 39136362))
    
    # 去重并排序
    seen = set()
    unique = []
    for k in klines:
        if k.date not in seen:
            seen.add(k.date)
            unique.append(k)
    unique.sort(key=lambda x: x.date)
    return unique

# ============================================================
# 工具函数
# ============================================================
def atr(klines: List[KLine], n=14) -> float:
    if len(klines) < n + 1:
        return 0.0
    trs = []
    for i in range(-n, 0):
        k = klines[i]
        prev = klines[i-1]
        tr = max(k.high - k.low, abs(k.high - prev.close), abs(k.low - prev.close))
        trs.append(tr)
    return sum(trs) / len(trs)

def ema(values: List[float], n: int) -> List[float]:
    if len(values) < n:
        return values
    k = 2 / (n + 1)
    result = [sum(values[:n]) / n]
    for v in values[n:]:
        result.append(v * k + result[-1] * (1 - k))
    return result

def sma(values: List[float], n: int) -> List[float]:
    result = []
    for i in range(len(values)):
        if i < n - 1:
            result.append(sum(values[:i+1]) / (i+1))
        else:
            result.append(sum(values[i-n+1:i+1]) / n)
    return result

def ao(klines: List[KLine]) -> List[float]:
    mp = [(k.high + k.low) / 2 for k in klines]
    s5 = sma(mp, 5)
    s34 = sma(mp, 34)
    return [s5[i] - s34[i] if i < len(s34) else 0 for i in range(len(s5))]

# ============================================================
# 对象卡运行
# ============================================================
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

def run_period_queen(klines: List[KLine]) -> CardResult:
    """周期女王：基于波动率和趋势强度识别市场状态"""
    recent = klines[-60:]
    returns = [klines[i].close / klines[i-1].close - 1 for i in range(-30, 0)]
    vol = np.std(returns) * math.sqrt(252)
    trend = (klines[-1].close - klines[-20].close) / klines[-20].close
    
    # 判断状态
    if vol > 0.5:
        state = "POWER_TRANSITION"
    elif trend > 0.15:
        state = "ATTACK_SUSTAINED"
    elif trend > 0.05:
        state = "ATTACK_INITIAL"
    elif trend < -0.15:
        state = "CUTTING_COMPLETE"
    elif trend < -0.05:
        state = "CUTTING_START"
    else:
        state = "CONSOLIDATION"
    
    # 权限映射
    perm_map = {
        "ATTACK_SUSTAINED": "FULL", "ATTACK_INITIAL": "FULL",
        "CONSOLIDATION": "REDUCED", "POWER_TRANSITION": "REDUCED",
        "CUTTING_START": "EXIT_ONLY", "CUTTING_COMPLETE": "HALT"
    }
    
    return CardResult(
        object_id="PERIOD_QUEEN_P0_F",
        signal_type=f"STATE_{state}",
        signal_strength=round(abs(trend) * 10, 1),
        confidence=0.65,
        lock_status="UNLOCKED",
        filter_action="PASS",
        risk_action=f"PERMISSION_{perm_map.get(state, 'REDUCED')}",
        size_scalar=1.0 if state in ["ATTACK_SUSTAINED", "ATTACK_INITIAL"] else 0.5,
        detail={"volatility_annual": round(vol, 3), "trend_20d": round(trend, 3), "state": state}
    )

def run_volfac(klines: List[KLine]) -> CardResult:
    """波动率因子"""
    returns = [klines[i].close / klines[i-1].close - 1 for i in range(-60, 0)]
    vol = np.std(returns) * math.sqrt(252)
    
    # 历史分位（模拟）
    hist_vols = [np.std(returns[max(0,i-20):i]) * math.sqrt(252) for i in range(20, len(returns))]
    percentile = sum(1 for v in hist_vols if v < vol) / max(1, len(hist_vols))
    
    if percentile > 0.8:
        regime = "EXTREME_VOL"
        sig = "SELL"
    elif percentile > 0.6:
        regime = "HIGH_VOL"
        sig = "HOLD"
    elif percentile < 0.2:
        regime = "LOW_VOL"
        sig = "BUY"
    else:
        regime = "NORMAL"
        sig = "HOLD"
    
    return CardResult(
        object_id="VOLFAC_P0_A",
        signal_type=sig,
        signal_strength=round((percentile - 0.5) * 4, 1),
        confidence=0.7,
        lock_status="UNLOCKED",
        filter_action="PASS" if regime != "EXTREME_VOL" else "BLOCK",
        risk_action="DOWNSIZE" if regime == "HIGH_VOL" else "NORMAL",
        size_scalar=round(0.25 / max(vol, 0.1), 2),
        detail={"annual_vol": round(vol, 3), "percentile": round(percentile, 2), "regime": regime}
    )

def run_voltarget(klines: List[KLine], volfac: CardResult) -> CardResult:
    """波动率目标仓位"""
    target_vol = 0.25
    current_vol = volfac.detail.get("annual_vol", 0.3)
    scalar = target_vol / max(current_vol, 0.05)
    scalar = min(scalar, 2.0)
    
    return CardResult(
        object_id="VOLTARGET_P0_R",
        signal_type="VOL_ADJUST",
        signal_strength=round(scalar, 2),
        confidence=0.75,
        lock_status="UNLOCKED",
        filter_action="PASS",
        risk_action="SCALE_POSITION",
        size_scalar=round(scalar, 2),
        detail={"target_vol": target_vol, "current_vol": round(current_vol, 3), "position_scalar": round(scalar, 2)}
    )

def run_chzl(klines: List[KLine]) -> CardResult:
    """缠论分型"""
    # 简化：检查最近是否形成底分型
    if len(klines) < 5:
        return CardResult("CHZL_BSD_P0_E", "NEUTRAL", 0, 0.5, "UNLOCKED", "PASS", "NORMAL", 1.0, {})
    
    k1, k2, k3 = klines[-3], klines[-2], klines[-1]
    # 底分型：中间K线低点最低
    bottom_fractal = k2.low < k1.low and k2.low < k3.low and k2.high < k1.high and k2.high < k3.high
    top_fractal = k2.high > k1.high and k2.high > k3.high and k2.low > k1.low and k2.low > k3.low
    
    if bottom_fractal:
        sig, strength = "BUY", 1.5
    elif top_fractal:
        sig, strength = "SELL", -1.5
    else:
        sig, strength = "NEUTRAL", 0.0
    
    return CardResult(
        object_id="CHZL_BSD_P0_E",
        signal_type=sig,
        signal_strength=strength,
        confidence=0.6,
        lock_status="UNLOCKED",
        filter_action="PASS" if sig != "SELL" else "BLOCK",
        risk_action="NORMAL",
        size_scalar=1.0,
        detail={"bottom_fractal": bottom_fractal, "top_fractal": top_fractal}
    )

def run_bpb(klines: List[KLine]) -> CardResult:
    """Brooks突破回调"""
    if len(klines) < 30:
        return CardResult("BPB_P0_E", "NEUTRAL", 0, 0.5, "UNLOCKED", "PASS", "NORMAL", 1.0, {})
    
    # 找20日高点
    highs = [k.high for k in klines[-20:]]
    max_high = max(highs)
    max_idx = highs.index(max_high)
    
    # 突破后回调到38.2%-61.8%
    if max_idx >= len(highs) - 5:  # 最近突破
        fib382 = max_high - (max_high - min(k.low for k in klines[-20:])) * 0.382
        fib618 = max_high - (max_high - min(k.low for k in klines[-20:])) * 0.618
        current = klines[-1].close
        
        if fib618 <= current <= fib382:
            return CardResult(
                object_id="BPB_P0_E",
                signal_type="BUY",
                signal_strength=1.8,
                confidence=0.55,
                lock_status="UNLOCKED",
                filter_action="PASS",
                risk_action="NORMAL",
                size_scalar=1.0,
                detail={"fib_zone": "38.2%-61.8%", "breakout_high": round(max_high, 2)}
            )
    
    return CardResult("BPB_P0_E", "NEUTRAL", 0, 0.5, "UNLOCKED", "PASS", "NORMAL", 1.0, {})

def run_tkr7(klines: List[KLine]) -> CardResult:
    """AO背离"""
    ao_vals = ao(klines)
    if len(ao_vals) < 10:
        return CardResult("TKR7_P0_E", "NEUTRAL", 0, 0.5, "UNLOCKED", "PASS", "NORMAL", 1.0, {})
    
    # 简化：检查价格和AO是否同向
    price_trend = klines[-1].close - klines[-5].close
    ao_trend = ao_vals[-1] - ao_vals[-5]
    
    if price_trend > 0 and ao_trend < 0:
        sig, strength = "SELL", -1.5  # 顶背离
    elif price_trend < 0 and ao_trend > 0:
        sig, strength = "BUY", 1.5   # 底背离
    else:
        sig, strength = "NEUTRAL", 0.0
    
    return CardResult(
        object_id="TKR7_P0_E",
        signal_type=sig,
        signal_strength=strength,
        confidence=0.6,
        lock_status="UNLOCKED",
        filter_action="PASS" if sig != "SELL" else "BLOCK",
        risk_action="NORMAL",
        size_scalar=1.0,
        detail={"ao_current": round(ao_vals[-1], 3), "ao_trend": round(ao_trend, 3)}
    )

def run_mflow(klines: List[KLine]) -> CardResult:
    """资金流向"""
    # 基于量价关系模拟
    recent = klines[-10:]
    up_vol = sum(k.vol for k in recent if k.close > k.open)
    down_vol = sum(k.vol for k in recent if k.close < k.open)
    total_vol = up_vol + down_vol
    
    if total_vol == 0:
        ratio = 0.5
    else:
        ratio = up_vol / total_vol
    
    if ratio > 0.65:
        sig, strength = "BUY", 1.5
    elif ratio < 0.35:
        sig, strength = "SELL", -1.5
    else:
        sig, strength = "NEUTRAL", 0.0
    
    return CardResult(
        object_id="MFLOW_P0_A",
        signal_type=sig,
        signal_strength=strength,
        confidence=0.55,
        lock_status="UNLOCKED",
        filter_action="PASS" if sig != "SELL" else "BLOCK",
        risk_action="NORMAL",
        size_scalar=1.0,
        detail={"up_down_ratio": round(ratio, 2)}
    )

def run_instb(klines: List[KLine]) -> CardResult:
    """机构行为"""
    # 简化：用大单流入模拟（基于成交量突增）
    vol_ma = sum(k.vol for k in klines[-20:]) / 20
    recent_vol = klines[-1].vol
    
    if recent_vol > vol_ma * 2:
        sig, strength = "BUY", 1.2  # 放量视为吸筹
    elif recent_vol < vol_ma * 0.5:
        sig, strength = "SELL", -0.8  # 缩量视为派发
    else:
        sig, strength = "NEUTRAL", 0.0
    
    return CardResult(
        object_id="INSTB_P0_A",
        signal_type=sig,
        signal_strength=strength,
        confidence=0.5,
        lock_status="UNLOCKED",
        filter_action="PASS",
        risk_action="NORMAL",
        size_scalar=1.0,
        detail={"vol_vs_ma20": round(recent_vol / vol_ma, 2)}
    )

def run_kelly(klines: List[KLine]) -> CardResult:
    """凯利公式"""
    returns = [klines[i].close / klines[i-1].close - 1 for i in range(-60, 0)]
    wins = [r for r in returns if r > 0]
    losses = [r for r in returns if r < 0]
    
    if not wins or not losses:
        return CardResult("KELLY_P0_R", "NEUTRAL", 0, 0.5, "UNLOCKED", "PASS", "NORMAL", 1.0, {})
    
    win_rate = len(wins) / len(returns)
    avg_win = sum(wins) / len(wins)
    avg_loss = abs(sum(losses) / len(losses))
    
    if avg_loss == 0:
        kelly = 0
    else:
        kelly = win_rate - (1 - win_rate) / (avg_win / avg_loss)
    
    half_kelly = max(0, kelly / 2)
    
    return CardResult(
        object_id="KELLY_P0_R",
        signal_type="POSITION_SIZE",
        signal_strength=round(half_kelly, 3),
        confidence=0.6,
        lock_status="UNLOCKED",
        filter_action="PASS",
        risk_action="SCALE_POSITION",
        size_scalar=round(min(half_kelly, 1.0), 2),
        detail={"half_kelly": round(half_kelly, 3), "win_rate": round(win_rate, 2)}
    )

def run_vp(klines: List[KLine]) -> CardResult:
    """成交量分布"""
    # 计算POC（成交量最大价格区间）
    price_vol = {}
    for k in klines[-30:]:
        bucket = round(k.close / 5) * 5  # 5元一个区间
        price_vol[bucket] = price_vol.get(bucket, 0) + k.vol
    
    poc = max(price_vol, key=price_vol.get)
    current = round(klines[-1].close / 5) * 5
    
    if current > poc + 10:
        sig, strength = "SELL", -1.0  # 偏离POC上方
    elif current < poc - 10:
        sig, strength = "BUY", 1.0    # 偏离POC下方
    else:
        sig, strength = "NEUTRAL", 0.0  # 在POC附近
    
    return CardResult(
        object_id="VP_P0_E",
        signal_type=sig,
        signal_strength=strength,
        confidence=0.55,
        lock_status="UNLOCKED",
        filter_action="PASS",
        risk_action="NORMAL",
        size_scalar=1.0,
        detail={"poc_zone": poc, "current_zone": current}
    )

def run_ytc(klines: List[KLine]) -> CardResult:
    """YTC微观结构"""
    k = klines[-1]
    body = abs(k.close - k.open)
    range_ = k.high - k.low
    
    if range_ == 0:
        ratio = 0
    else:
        ratio = body / range_
    
    # 大阳线 = 强势买入信号
    if ratio > 0.7 and k.close > k.open:
        sig, strength = "BUY", 1.5
    elif ratio > 0.7 and k.close < k.open:
        sig, strength = "SELL", -1.5
    else:
        sig, strength = "NEUTRAL", 0.0
    
    return CardResult(
        object_id="YTC_P0_E",
        signal_type=sig,
        signal_strength=strength,
        confidence=0.5,
        lock_status="UNLOCKED",
        filter_action="PASS" if sig != "SELL" else "BLOCK",
        risk_action="NORMAL",
        size_scalar=1.0,
        detail={"body_range_ratio": round(ratio, 2)}
    )

def run_atratio(klines: List[KLine]) -> CardResult:
    """活跃度比率（A股纯多头）"""
    recent_vol = klines[-1].vol
    vol_ma20 = sum(k.vol for k in klines[-20:]) / 20
    ratio = recent_vol / vol_ma20 if vol_ma20 > 0 else 1.0
    
    # 纯多头：只有BUY/NEUTRAL，无SELL
    if ratio > 2.0:
        sig, strength = "BUY", 1.2
    elif ratio > 1.5:
        sig, strength = "BUY", 0.8
    else:
        sig, strength = "NEUTRAL", 0.0
    
    return CardResult(
        object_id="ATRATIO_P0_A",
        signal_type=sig,
        signal_strength=strength,
        confidence=0.5,
        lock_status="UNLOCKED",
        filter_action="PASS",
        risk_action="NORMAL",
        size_scalar=1.0,
        detail={"vol_ratio": round(ratio, 2)}
    )

# ============================================================
# 聚合分析
# ============================================================
def aggregate_signals(results: List[CardResult]) -> Dict:
    buy_votes = [r for r in results if r.signal_type == "BUY"]
    sell_votes = [r for r in results if r.signal_type == "SELL"]
    neutral = [r for r in results if r.signal_type == "NEUTRAL"]
    
    # 加权投票
    buy_score = sum(r.signal_strength * r.confidence for r in buy_votes)
    sell_score = sum(abs(r.signal_strength) * r.confidence for r in sell_votes)
    
    # 综合仓位系数
    size_scalars = [r.size_scalar for r in results if r.signal_type in ["BUY", "VOL_ADJUST", "POSITION_SIZE"]]
    avg_size = sum(size_scalars) / len(size_scalars) if size_scalars else 1.0
    
    # PERIOD_QUEEN权限检查
    pq = next((r for r in results if r.object_id == "PERIOD_QUEEN_P0_F"), None)
    permission = pq.risk_action if pq else "PERMISSION_REDUCED"
    
    return {
        "buy_votes": len(buy_votes),
        "sell_votes": len(sell_votes),
        "neutral_votes": len(neutral),
        "buy_score": round(buy_score, 2),
        "sell_score": round(sell_score, 2),
        "net_score": round(buy_score - sell_score, 2),
        "avg_size_scalar": round(avg_size, 2),
        "permission": permission,
        "final_signal": "BUY" if buy_score > sell_score + 1.0 else ("SELL" if sell_score > buy_score + 1.0 else "NEUTRAL"),
        "blockers": [r.object_id for r in results if r.filter_action == "BLOCK"]
    }

def analyze_rkx(ctx):
    random.seed(42)
    np.random.seed(42)
    
    print("=" * 60)
    print("瑞芯微 (603893.SH) 对象卡系统聚合分析")
    print("分析日期: 2026-07-07")
    print("当前价格: 190.71 (涨幅 +8.28%)")
    print("=" * 60)
    
    klines = generate_rkx_klines()
    print(f"\n生成模拟K线: {len(klines)} 个交易日")
    print(f"区间: {klines[0].date} ~ {klines[-1].date}")
    print(f"价格范围: {min(k.close for k in klines):.2f} ~ {max(k.close for k in klines):.2f}")
    
    # 运行所有对象卡
    print("\n" + "=" * 60)
    print("对象卡独立运行结果")
    print("=" * 60)
    
    results = []
    
    pq = run_period_queen(klines)
    results.append(pq)
    print(f"\n📊 {pq.object_id}")
    print(f"   信号: {pq.signal_type} | 强度: {pq.signal_strength} | 置信: {pq.confidence}")
    print(f"   权限: {pq.risk_action} | 详情: {pq.detail}")
    
    vf = run_volfac(klines)
    results.append(vf)
    print(f"\n📊 {vf.object_id}")
    print(f"   信号: {vf.signal_type} | 强度: {vf.signal_strength} | 置信: {vf.confidence}")
    print(f"   过滤: {vf.filter_action} | 详情: {vf.detail}")
    
    vt = run_voltarget(klines, vf)
    results.append(vt)
    print(f"\n📊 {vt.object_id}")
    print(f"   信号: {vt.signal_type} | 强度: {vt.signal_strength} | 置信: {vt.confidence}")
    print(f"   仓位系数: {vt.size_scalar} | 详情: {vt.detail}")
    
    for runner, name in [
        (run_chzl, "缠论分型"), (run_bpb, "突破回调"), (run_tkr7, "AO背离"),
        (run_mflow, "资金流向"), (run_instb, "机构行为"), (run_kelly, "凯利公式"),
        (run_vp, "成交量分布"), (run_ytc, "YTC微观"), (run_atratio, "活跃度")
    ]:
        r = runner(klines)
        results.append(r)
        print(f"\n📊 {r.object_id} ({name})")
        print(f"   信号: {r.signal_type} | 强度: {r.signal_strength} | 置信: {r.confidence}")
        if r.detail:
            print(f"   详情: {r.detail}")
    
    # 聚合
    print("\n" + "=" * 60)
    print("聚合投票结果")
    print("=" * 60)
    
    agg = aggregate_signals(results)
    print(f"\n🗳️ 投票统计:")
    print(f"   BUY 票: {agg['buy_votes']} | SELL 票: {agg['sell_votes']} | NEUTRAL: {agg['neutral_votes']}")
    print(f"   BUY加权得分: {agg['buy_score']}")
    print(f"   SELL加权得分: {agg['sell_score']}")
    print(f"   净得分: {agg['net_score']}")
    print(f"   平均仓位系数: {agg['avg_size_scalar']}")
    print(f"   环境权限: {agg['permission']}")
    print(f"   阻塞对象卡: {agg['blockers'] if agg['blockers'] else '无'}")
    
    print(f"\n🏁 最终信号: {agg['final_signal']}")
    
    # 基本面摘要
    print("\n" + "=" * 60)
    print("基本面锚点（来自公开信息）")
    print("=" * 60)
    fundamentals = {
        "股票代码": "603893.SH",
        "公司全称": "瑞芯微电子股份有限公司",
        "主营业务": "AIoT芯片设计（SoC）",
        "旗舰产品": "RK3588, RK3576, RV11系列",
        "2024营收": "31.36亿元 (+46.94%)",
        "2024净利润": "5.95亿元 (+341.01%)",
        "2024EPS": "1.42元 (+343.75%)",
        "总市值": "约800亿元",
        "半导体排名": "板块第11/160",
        "最新价格": "190.71元 (+8.28%)",
        "PE_TTM估": "约134倍（高估值）",
        "催化剂": "AI端侧需求、汽车电子、机器人芯片"
    }
    for k, v in fundamentals.items():
        print(f"   {k}: {v}")
    
    # 综合建议
    print("\n" + "=" * 60)
    print("系统综合建议")
    print("=" * 60)
    
    if agg['final_signal'] == "BUY":
        rec = "🔵 多头配置"
        action = f"可建仓/加仓，建议仓位系数 {agg['avg_size_scalar']:.1f}x"
    elif agg['final_signal'] == "SELL":
        rec = "🔴 减仓/回避"
        action = "建议减仓或观望"
    else:
        rec = "⚪ 中性观望"
        action = "维持现有仓位，等待更明确信号"
    
    print(f"\n   建议: {rec}")
    print(f"   操作: {action}")
    print(f"   环境: {agg['permission']}")
    print(f"\n   ⚠️  重要提示:")
    print(f"      1. 当前PE约134倍，估值处于历史高位")
    print(f"      2. 2024年业绩暴增341%已充分price in")
    print(f"      3. 股价从2025年初144元涨至当前190元，涨幅32%")
    print(f"      4. 半导体周期敏感，需关注2025H2业绩能否持续")
    print(f"      5. 今日大涨8.28%，注意短期回调风险")
    
    # 保存结果
    result = {
        "stock": "603893.SH",
        "name": "瑞芯微",
        "date": "2026-07-07",
        "price": 190.71,
        "change_pct": 8.28,
        "card_results": [
            {
                "object_id": r.object_id,
                "signal_type": r.signal_type,
                "signal_strength": r.signal_strength,
                "confidence": r.confidence,
                "filter_action": r.filter_action,
                "size_scalar": r.size_scalar
            } for r in results
        ],
        "aggregate": agg,
        "fundamentals": fundamentals
    }
    
    output_path = f"{ctx['runDir']}/rkx_analysis_20260707.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 分析结果已保存: {output_path}")
    return {"output_path": output_path, "summary": agg}
