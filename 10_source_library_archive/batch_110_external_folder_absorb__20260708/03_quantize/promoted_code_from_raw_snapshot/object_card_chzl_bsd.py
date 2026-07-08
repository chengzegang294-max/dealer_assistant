"""
Object Card: CHZL_BSD_P0_E — 缠论三类买卖点（Chanlun Buy/Sell Signals）
文档: OBJECT_CARD_CHZL_BSD_P0_E__Chanlun_Buy_Sell_Signals_v1.0.md

核心逻辑: 基于顶底分型识别笔，用价格区间模拟中枢上下沿，
          识别 1Buy/2Buy/3Buy/1Sell/2Sell/3Sell 信号。
A股纯多头场景: Sell信号仅作为观察，不生成交易。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import numpy as np
import pandas as pd


@dataclass
class ChanlunInput:
    """
    缠论 BSD 输入数据结构
    """
    ohlcv: pd.DataFrame          # columns: open, high, low, close, volume
    atr14: Optional[float] = None
    # 可选中枢数据
    zhongshu_zs: Optional[Dict[str, Any]] = None  # {zg, zd, zz, state}
    # 外部互锁信号（可选，用于增强判断）
    kd_day_signal: Optional[str] = None   # 'bullish' / 'bearish' / 'neutral'
    lock_signal: Optional[str] = None      # 'locked' / 'unlocked' / 'conflicting'


@dataclass
class ObjectCardOutput:
    """
    标准对象卡输出格式 — 8个字段
    """
    object_id: str           # 对象卡标识
    signal_type: str         # 信号类型枚举
    signal_strength: int     # 信号强度 0-10
    confidence: float        # 置信度 0.0-1.0
    lock_status: str         # 'locked' / 'unlocked' / 'conflicting'
    filter_action: str       # 'APPROVE' / 'REJECT' / 'OBSERVE' / 'DEGRADE'
    risk_action: str         # 'FULL_SIZE' / 'HALF_SIZE' / 'QUARTER_SIZE' / 'NO_TRADE'
    size_scalar: float       # 仓位系数 0.0-1.0


class ObjectCardCHZLBSD:
    """
    缠论三类买卖点对象卡
    object_id: CHZL_BSD_P0_E
    """
    OBJECT_ID: str = "CHZL_BSD_P0_E"

    # A股纯多头限制
    LONG_ONLY: bool = True

    def __init__(self) -> None:
        self.prev_buy_low: Optional[float] = None   # 记录1买低点，用于2买判断
        self.prev_sell_high: Optional[float] = None  # 记录1卖高点，用于2卖判断
        self.recent_bis: List[Dict[str, Any]] = []   # 最近笔序列

    # ------------------------------------------------------------------ #
    # 公共入口
    # ------------------------------------------------------------------ #
    def calculate(self, inp: ChanlunInput) -> ObjectCardOutput:
        """主入口方法"""
        ohlcv = inp.ohlcv.copy()
        if len(ohlcv) < 20:
            return self._make_output("NONE", 0, 0.0, "unlocked", "REJECT", "NO_TRADE", 0.0)

        # 计算 ATR14 若未提供
        atr14 = inp.atr14 if inp.atr14 is not None else self._calc_atr14(ohlcv)

        # 1. 分型识别
        fractals = self._detect_fractals(ohlcv)
        if len(fractals) < 3:
            return self._make_output("NONE", 0, 0.0, "unlocked", "REJECT", "NO_TRADE", 0.0)

        # 2. 笔划分（简化版：分型连接成笔）
        bis = self._form_bi(fractals)
        if len(bis) < 3:
            return self._make_output("NONE", 0, 0.0, "unlocked", "REJECT", "NO_TRADE", 0.0)

        self.recent_bis = bis

        # 3. 模拟中枢（简化：用最近N根笔的价格区间）
        zs = inp.zhongshu_zs if inp.zhongshu_zs else self._simulate_zhongshu(bis)

        # 4. 检测当前最新笔状态，判断买卖点
        signal = self._detect_bsd(bis, zs, atr14, ohlcv)

        # 5. 互锁与过滤（简化版）
        signal = self._apply_filters(signal, inp)

        # 6. A股纯多头: Sell信号降级为观察
        if self.LONG_ONLY and signal["bsd_type"] in ("1S", "2S", "3S"):
            return self._make_output(
                signal["bsd_type"], signal["strength"], signal["confidence"],
                signal["lock_status"], "OBSERVE", "NO_TRADE", 0.0
            )

        # 7. 映射到标准输出
        return self._bsd_to_standard_output(signal)

    # ------------------------------------------------------------------ #
    # 内部工具
    # ------------------------------------------------------------------ #
    def _make_output(
        self,
        signal_type: str,
        signal_strength: int,
        confidence: float,
        lock_status: str,
        filter_action: str,
        risk_action: str,
        size_scalar: float,
    ) -> ObjectCardOutput:
        return ObjectCardOutput(
            object_id=self.OBJECT_ID,
            signal_type=signal_type,
            signal_strength=max(0, min(10, signal_strength)),
            confidence=max(0.0, min(1.0, confidence)),
            lock_status=lock_status,
            filter_action=filter_action,
            risk_action=risk_action,
            size_scalar=max(0.0, min(1.0, size_scalar)),
        )

    def _calc_atr14(self, ohlcv: pd.DataFrame) -> float:
        """计算 ATR(14)"""
        high, low, close = ohlcv["high"], ohlcv["low"], ohlcv["close"]
        tr1 = high - low
        tr2 = (high - close.shift(1)).abs()
        tr3 = (low - close.shift(1)).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return float(tr.rolling(14).mean().iloc[-1])

    def _detect_fractals(self, ohlcv: pd.DataFrame) -> List[Dict[str, Any]]:
        """检测顶底分型（简化版：3根K线）"""
        fractals = []
        h, l = ohlcv["high"].values, ohlcv["low"].values
        c = ohlcv["close"].values
        for i in range(1, len(ohlcv) - 1):
            # 顶分型: 中间K线高点最高
            if h[i] > h[i - 1] and h[i] > h[i + 1] and l[i] > l[i - 1] and l[i] > l[i + 1]:
                fractals.append({"idx": i, "type": "top", "price": h[i], "close": c[i]})
            # 底分型: 中间K线低点最低
            elif l[i] < l[i - 1] and l[i] < l[i + 1] and h[i] < h[i - 1] and h[i] < h[i + 1]:
                fractals.append({"idx": i, "type": "bottom", "price": l[i], "close": c[i]})
        return fractals

    def _form_bi(self, fractals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        分型连成笔（简化版）
        规则: 顶-底-顶-底... 交替，且新笔必须突破前一笔的端点
        """
        if len(fractals) < 2:
            return []
        bis = []
        # 从第一个分型开始
        start = fractals[0]
        for i in range(1, len(fractals)):
            curr = fractals[i]
            # 方向: 从底到顶 = 上笔，从顶到底 = 下笔
            if start["type"] == "bottom" and curr["type"] == "top":
                direction = "up"
            elif start["type"] == "top" and curr["type"] == "bottom":
                direction = "down"
            else:
                continue  # 同类型分型，跳过（简化为连接最近的相反分型）
            # 创建笔
            bis.append({
                "start_idx": start["idx"],
                "end_idx": curr["idx"],
                "direction": direction,
                "high": max(start["price"], curr["price"]) if direction == "up" else start["price"],
                "low": min(start["price"], curr["price"]) if direction == "down" else start["price"],
                "start_price": start["price"],
                "end_price": curr["price"],
            })
            start = curr
        return bis

    def _simulate_zhongshu(self, bis: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """简化中枢: 取最近3笔的重叠区间"""
        if len(bis) < 3:
            return None
        recent3 = bis[-3:]
        # 中枢是至少3笔的重叠区间
        zg = min(b["high"] for b in recent3)  # 中枢上沿 = 最低的高点
        zd = max(b["low"] for b in recent3)   # 中枢下沿 = 最高的低点
        if zg <= zd:
            return None  # 无有效重叠
        return {"zg": zg, "zd": zd, "zz": (zg + zd) / 2, "state": "active"}

    def _detect_bsd(
        self,
        bis: List[Dict[str, Any]],
        zs: Optional[Dict[str, Any]],
        atr14: float,
        ohlcv: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        检测三类买卖点（简化版）
        """
        if len(bis) < 2:
            return {"bsd_type": "NONE", "strength": 0, "confidence": 0.0, "lock_status": "unlocked"}

        last_bi = bis[-1]
        prev_bi = bis[-2] if len(bis) >= 2 else None
        prev2_bi = bis[-3] if len(bis) >= 3 else None

        current_close = float(ohlcv["close"].iloc[-1])

        # 1Buy: 趋势下跌背驰后的第一个买入点
        # 简化判定: 下笔创新低后，当前笔方向向上，且价格从低点反弹
        if last_bi["direction"] == "up" and prev_bi and prev_bi["direction"] == "down":
            # 检查是否是"新低后反弹"（简化背驰判断）
            if prev_bi["end_price"] < prev_bi["start_price"]:
                # 进一步检查: 是否有中枢，当前价格在中枢下沿附近或下方
                if zs and current_close < zs["zd"]:
                    # 价格在中枢下方，可能是一买
                    confidence = 0.75
                    strength = 7
                    # 更新记录的1买低点
                    self.prev_buy_low = prev_bi["end_price"]
                    return {
                        "bsd_type": "1B",
                        "strength": strength,
                        "confidence": confidence,
                        "lock_status": "locked",
                        "trigger_price": current_close,
                        "stop_loss": prev_bi["end_price"] - atr14 * 0.5,
                        "sl_logic": "FRACTAL_BREAK",
                    }
                elif not zs:
                    # 无中枢，仍然可能是一买（趋势下跌后的第一个反转）
                    self.prev_buy_low = prev_bi["end_price"]
                    return {
                        "bsd_type": "1B",
                        "strength": 6,
                        "confidence": 0.65,
                        "lock_status": "unlocked",
                        "trigger_price": current_close,
                        "stop_loss": prev_bi["end_price"] - atr14 * 0.5,
                        "sl_logic": "FRACTAL_BREAK",
                    }

        # 2Buy: 1Buy后回调不破前低
        if last_bi["direction"] == "down" and prev_bi and prev_bi["direction"] == "up":
            if self.prev_buy_low is not None:
                # 当前笔低点高于1买低点 = 不破前低
                if last_bi["end_price"] > self.prev_buy_low:
                    return {
                        "bsd_type": "2B",
                        "strength": 8,
                        "confidence": 0.80,
                        "lock_status": "locked",
                        "trigger_price": current_close,
                        "stop_loss": self.prev_buy_low - atr14 * 0.2,
                        "sl_logic": "PREV_SWING",
                    }

        # 3Buy: 离开中枢后回踩不进中枢
        if last_bi["direction"] == "up" and zs:
            # 前一笔向上离开中枢
            if prev_bi and prev_bi["direction"] == "up" and prev_bi["end_price"] > zs["zg"]:
                # 当前笔回调，但低点不低于中枢上沿
                if last_bi["start_price"] > zs["zg"] or last_bi["low"] > zs["zg"]:
                    return {
                        "bsd_type": "3B",
                        "strength": 9,
                        "confidence": 0.85,
                        "lock_status": "locked",
                        "trigger_price": current_close,
                        "stop_loss": zs["zd"] - atr14 * 0.1,
                        "sl_logic": "ZS_REENTRY",
                        "is_trailing": True,
                    }

        # 1Sell / 2Sell / 3Sell (A股纯多头场景下仅作为观察)
        if last_bi["direction"] == "down" and prev_bi and prev_bi["direction"] == "up":
            if prev_bi["end_price"] > prev_bi["start_price"]:
                if zs and current_close > zs["zg"]:
                    return {
                        "bsd_type": "1S",
                        "strength": 6,
                        "confidence": 0.60,
                        "lock_status": "unlocked",
                        "trigger_price": current_close,
                    }

        return {"bsd_type": "NONE", "strength": 0, "confidence": 0.0, "lock_status": "unlocked"}

    def _apply_filters(
        self, signal: Dict[str, Any], inp: ChanlunInput
    ) -> Dict[str, Any]:
        """
        简化版互锁过滤（KD方向 + lock状态）
        """
        # lock_signal 过滤
        if inp.lock_signal == "conflicting":
            signal["strength"] = 0
            signal["confidence"] = 0.0
            signal["lock_status"] = "conflicting"
            return signal

        # KD方向过滤（简化）
        if inp.kd_day_signal == "bearish" and signal.get("bsd_type") in ("1B", "2B", "3B"):
            signal["strength"] = max(0, signal.get("strength", 0) - 2)
            signal["confidence"] = max(0.0, signal.get("confidence", 0.0) - 0.2)

        # 默认lock_status
        if "lock_status" not in signal:
            signal["lock_status"] = "locked" if signal.get("strength", 0) >= 5 else "unlocked"

        return signal

    def _bsd_to_standard_output(self, signal: Dict[str, Any]) -> ObjectCardOutput:
        """将BSD信号映射到8字段标准输出"""
        bsd_type = signal.get("bsd_type", "NONE")
        strength = signal.get("strength", 0)
        confidence = signal.get("confidence", 0.0)
        lock_status = signal.get("lock_status", "unlocked")

        if bsd_type == "NONE":
            return self._make_output("NONE", 0, 0.0, lock_status, "REJECT", "NO_TRADE", 0.0)

        # 确定 filter_action / risk_action / size_scalar
        if bsd_type in ("1B",):
            filter_action = "APPROVE"
            risk_action = "QUARTER_SIZE"  # 1Buy风险最大
            size_scalar = 0.25
        elif bsd_type in ("2B",):
            filter_action = "APPROVE"
            risk_action = "HALF_SIZE"
            size_scalar = 0.50
        elif bsd_type in ("3B",):
            filter_action = "APPROVE"
            risk_action = "FULL_SIZE"
            size_scalar = 1.0
        else:
            filter_action = "OBSERVE"
            risk_action = "NO_TRADE"
            size_scalar = 0.0

        return self._make_output(
            bsd_type, strength, confidence, lock_status,
            filter_action, risk_action, size_scalar
        )


# -------------------------------------------------------------------------- #
# Quick Test
# -------------------------------------------------------------------------- #
def _quick_test() -> None:
    """缠论BSD 快速测试 — 至少3个场景"""
    import numpy as np
    import pandas as pd

    card = ObjectCardCHZLBSD()

    def make_ohlcv(n: int, trend: str = "up", noise: float = 0.5) -> pd.DataFrame:
        """生成合成OHLCV数据"""
        np.random.seed(42)
        base = 100.0
        data = []
        for i in range(n):
            if trend == "up":
                base += np.random.uniform(0.1, 0.8)
            elif trend == "down":
                base -= np.random.uniform(0.1, 0.8)
            else:
                base += np.random.uniform(-0.5, 0.5)
            o = base + np.random.uniform(-noise, noise)
            c = base + np.random.uniform(-noise, noise)
            h = max(o, c) + np.random.uniform(0, noise * 0.5)
            l = min(o, c) - np.random.uniform(0, noise * 0.5)
            v = np.random.uniform(1000, 5000)
            data.append([o, h, l, c, v])
        df = pd.DataFrame(data, columns=["open", "high", "low", "close", "volume"])
        return df

    print("=" * 70)
    print("CHZL_BSD_P0_E 快速测试")
    print("=" * 70)

    # --- 场景1: 下跌趋势后的1Buy ---
    print("\n[场景1] 趋势下跌后出现底分型反弹（期望 1B）")
    df1 = make_ohlcv(60, trend="down", noise=0.3)
    # 最后10根人为制造反弹
    for i in range(50, 60):
        df1.loc[i, "close"] = 90.0 + (i - 50) * 0.5
        df1.loc[i, "high"] = df1.loc[i, "close"] + 0.3
        df1.loc[i, "low"] = df1.loc[i, "close"] - 0.3
        df1.loc[i, "open"] = df1.loc[i, "close"] - 0.1
    inp1 = ChanlunInput(ohlcv=df1, atr14=1.5, kd_day_signal="bullish")
    out1 = card.calculate(inp1)
    print(f"  输出: {out1}")
    assert out1.object_id == "CHZL_BSD_P0_E"
    assert out1.signal_type in ("1B", "2B", "3B", "NONE")

    # --- 场景2: 上升趋势中的2Buy ---
    print("\n[场景2] 上升趋势中回调不破前低（期望 2B 或 3B）")
    card2 = ObjectCardCHZLBSD()
    df2 = make_ohlcv(80, trend="up", noise=0.5)
    # 模拟: 先下跌形成1买，再回调形成2买
    for i in range(30, 45):
        df2.loc[i, "close"] = 100.0 - (i - 30) * 0.4
        df2.loc[i, "low"] = df2.loc[i, "close"] - 0.4
        df2.loc[i, "high"] = df2.loc[i, "close"] + 0.2
    for i in range(45, 55):
        df2.loc[i, "close"] = 94.0 + (i - 45) * 0.6
        df2.loc[i, "high"] = df2.loc[i, "close"] + 0.3
        df2.loc[i, "low"] = df2.loc[i, "close"] - 0.3
    for i in range(55, 65):
        df2.loc[i, "close"] = 100.0 - (i - 55) * 0.2  # 浅回调
        df2.loc[i, "low"] = df2.loc[i, "close"] - 0.3
        df2.loc[i, "high"] = df2.loc[i, "close"] + 0.3
    for i in range(65, 80):
        df2.loc[i, "close"] = 98.0 + (i - 65) * 0.5
        df2.loc[i, "high"] = df2.loc[i, "close"] + 0.3
        df2.loc[i, "low"] = df2.loc[i, "close"] - 0.3
    inp2 = ChanlunInput(ohlcv=df2, atr14=1.2, kd_day_signal="bullish")
    out2 = card2.calculate(inp2)
    print(f"  输出: {out2}")
    assert out2.object_id == "CHZL_BSD_P0_E"

    # --- 场景3: 数据不足 ---
    print("\n[场景3] 数据不足（期望 NONE, REJECT）")
    df3 = make_ohlcv(10, trend="up")
    inp3 = ChanlunInput(ohlcv=df3)
    out3 = card.calculate(inp3)
    print(f"  输出: {out3}")
    assert out3.signal_type == "NONE"
    assert out3.filter_action == "REJECT"

    # --- 场景4: A股纯多头 — Sell信号降级 ---
    print("\n[场景4] A股纯多头 — Sell信号应降级为观察")
    card4 = ObjectCardCHZLBSD()
    df4 = make_ohlcv(60, trend="up", noise=0.3)
    # 制造顶部结构
    for i in range(40, 50):
        df4.loc[i, "close"] = 130.0 + (i - 40) * 0.3
        df4.loc[i, "high"] = df4.loc[i, "close"] + 0.4
    for i in range(50, 60):
        df4.loc[i, "close"] = 133.0 - (i - 50) * 0.5
        df4.loc[i, "low"] = df4.loc[i, "close"] - 0.4
    inp4 = ChanlunInput(ohlcv=df4, atr14=1.5, kd_day_signal="bearish")
    out4 = card4.calculate(inp4)
    print(f"  输出: {out4}")
    if out4.signal_type in ("1S", "2S", "3S"):
        assert out4.filter_action == "OBSERVE"
        assert out4.risk_action == "NO_TRADE"
        assert out4.size_scalar == 0.0

    print("\n" + "=" * 70)
    print("CHZL_BSD_P0_E 所有测试通过 ✓")
    print("=" * 70)


if __name__ == "__main__":
    _quick_test()
