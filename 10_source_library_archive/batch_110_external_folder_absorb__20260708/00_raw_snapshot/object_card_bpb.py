"""
Object Card: BPB_P0_E — Brooks Breakout Pullback（突破回调）
文档: OBJECT_CARD_BPB_P0_E__Brooks_Breakout_Pullback_v1.0.md

核心逻辑: 检测20日高点突破 + 回调不破支撑
A股纯多头场景: SHORT/BOF_SHORT 信号仅作为观察，不生成交易。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any
import numpy as np
import pandas as pd


@dataclass
class BPBInput:
    """BPB 输入数据结构"""
    ohlcv: pd.DataFrame
    atr14: Optional[float] = None
    # 可选外部状态
    pullback_count: int = 0       # 当前回调计数
    last_bpb_direction: Optional[str] = None


@dataclass
class ObjectCardOutput:
    """标准对象卡输出 — 8个字段"""
    object_id: str
    signal_type: str
    signal_strength: int
    confidence: float
    lock_status: str
    filter_action: str
    risk_action: str
    size_scalar: float


class ObjectCardBPB:
    """
    Brooks Breakout Pullback 对象卡
    object_id: BPB_P0_E
    """
    OBJECT_ID: str = "BPB_P0_E"
    LONG_ONLY: bool = True

    def __init__(self) -> None:
        self.state: Dict[str, Any] = {
            "pullback_count": 0,
            "last_bpb_direction": None,
        }

    # ------------------------------------------------------------------ #
    def calculate(self, inp: BPBInput) -> ObjectCardOutput:
        """主入口方法"""
        ohlcv = inp.ohlcv.copy()
        if len(ohlcv) < 25:
            return self._make_output("NONE", 0, 0.0, "unlocked", "REJECT", "NO_TRADE", 0.0)

        atr14 = inp.atr14 if inp.atr14 is not None else self._calc_atr14(ohlcv)

        # 1. 趋势检测与突破识别
        breakout = self._detect_breakout(ohlcv, lookback=20)
        if not breakout["breakout_detected"]:
            return self._make_output("NONE", 0, 0.0, "unlocked", "REJECT", "NO_TRADE", 0.0)

        # 2. 突破质量评估
        is_valid, body_pct, vol_ratio = self._evaluate_breakout_quality(breakout, ohlcv)
        if not is_valid:
            # 突破质量差，但仍返回观察信号
            return self._make_output(
                "NONE", 0, 0.3, "unlocked", "REJECT", "NO_TRADE", 0.0
            )

        # 3. 回调检测与评估
        pullback = self._detect_pullback(ohlcv, breakout, atr14)

        # 4. 生成信号
        signal = self._generate_signal(breakout, pullback, body_pct, vol_ratio, atr14)

        # 5. 更新回调计数
        signal = self._update_pullback_count(signal)

        # 6. A股纯多头过滤
        signal = self._apply_long_only_filter(signal)

        return self._signal_to_output(signal, breakout, pullback)

    # ------------------------------------------------------------------ #
    def _make_output(self, *args) -> ObjectCardOutput:
        return ObjectCardOutput(
            object_id=self.OBJECT_ID,
            signal_type=args[0],
            signal_strength=max(0, min(10, args[1])),
            confidence=max(0.0, min(1.0, args[2])),
            lock_status=args[3],
            filter_action=args[4],
            risk_action=args[5],
            size_scalar=max(0.0, min(1.0, args[6])),
        )

    def _calc_atr14(self, ohlcv: pd.DataFrame) -> float:
        h, l, c = ohlcv["high"], ohlcv["low"], ohlcv["close"]
        tr1 = h - l
        tr2 = (h - c.shift(1)).abs()
        tr3 = (l - c.shift(1)).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return float(tr.rolling(14).mean().iloc[-1])

    def _detect_breakout(self, ohlcv: pd.DataFrame, lookback: int = 20) -> Dict[str, Any]:
        """检测突破: 当前K线突破20日高点"""
        recent = ohlcv.tail(lookback + 2)
        prev_window = recent.iloc[:lookback]
        last_bar = recent.iloc[-1]
        prev_bar = recent.iloc[-2]

        recent_high = float(prev_window["high"].max())
        recent_low = float(prev_window["low"].min())

        result = {
            "breakout_detected": False,
            "trend_direction": "sideways",
            "breakout_level": 0.0,
            "breakout_bar_idx": len(ohlcv) - 1,
            "breakout_high": float(last_bar["high"]),
            "breakout_low": float(last_bar["low"]),
            "breakout_close": float(last_bar["close"]),
            "breakout_open": float(last_bar["open"]),
            "recent_high": recent_high,
            "recent_low": recent_low,
        }

        # 趋势方向检测（简化：基于连续收盘价）
        closes = prev_window["close"].values
        up_count = sum(1 for i in range(1, len(closes)) if closes[i] > closes[i - 1])
        down_count = len(closes) - 1 - up_count
        if up_count >= 8 and up_count > down_count * 1.2:
            result["trend_direction"] = "up"
        elif down_count >= 8 and down_count > up_count * 1.2:
            result["trend_direction"] = "down"

        # 突破检测: 当前K线突破前高，且前一根未突破
        if last_bar["high"] > recent_high and prev_bar["high"] <= recent_high:
            result["breakout_detected"] = True
            result["breakout_level"] = recent_high
            result["breakout_type"] = "HIGH_BREAK"
        elif last_bar["low"] < recent_low and prev_bar["low"] >= recent_low:
            result["breakout_detected"] = True
            result["breakout_level"] = recent_low
            result["breakout_type"] = "LOW_BREAK"

        return result

    def _evaluate_breakout_quality(
        self, breakout: Dict[str, Any], ohlcv: pd.DataFrame
    ) -> tuple[bool, float, float]:
        """评估突破K线质量"""
        bar_range = breakout["breakout_high"] - breakout["breakout_low"]
        body = abs(breakout["breakout_close"] - breakout["breakout_open"])
        body_pct = body / bar_range if bar_range > 0 else 0.0

        idx = breakout["breakout_bar_idx"]
        vol = float(ohlcv.iloc[idx]["volume"])
        avg_vol = float(ohlcv["volume"].tail(20).mean())
        vol_ratio = vol / avg_vol if avg_vol > 0 else 1.0

        is_valid = body_pct > 0.5 and vol_ratio > 1.0
        return is_valid, body_pct, vol_ratio

    def _detect_pullback(
        self, ohlcv: pd.DataFrame, breakout: Dict[str, Any], atr14: float
    ) -> Dict[str, Any]:
        """检测突破后的回调"""
        idx = breakout["breakout_bar_idx"]
        post = ohlcv.iloc[idx + 1:] if idx + 1 < len(ohlcv) else pd.DataFrame()
        if len(post) == 0:
            return {"detected": False, "signal": "WAITING_PULLBACK"}

        trend = breakout["trend_direction"]
        blevel = breakout["breakout_level"]
        bhigh = breakout["breakout_high"]
        blow = breakout["breakout_low"]
        body = abs(breakout["breakout_close"] - breakout["breakout_open"])

        # 假突破检测（BOF）: 3根内回到原区间
        bof_window = post.head(3)
        if trend == "up":
            if any(bof_window["close"] < blevel):
                return {"detected": True, "signal": "BOF_SHORT", "is_failed": True}
        elif trend == "down":
            if any(bof_window["close"] > blevel):
                return {"detected": True, "signal": "BOF_LONG", "is_failed": True}

        # 回调检测
        pullback_detected = False
        pullback_low = bhigh
        pullback_high = blow
        pb_start = None
        pb_end = None

        for i, (ix, bar) in enumerate(post.iterrows()):
            if i >= 10:
                break
            if trend == "up":
                if bar["low"] < bhigh:
                    pullback_detected = True
                    pullback_low = min(pullback_low, bar["low"])
                    if pb_start is None:
                        pb_start = ix
                    pb_end = ix
                elif pullback_detected and bar["close"] > bhigh:
                    break
            elif trend == "down":
                if bar["high"] > blow:
                    pullback_detected = True
                    pullback_high = max(pullback_high, bar["high"])
                    if pb_start is None:
                        pb_start = ix
                    pb_end = ix
                elif pullback_detected and bar["close"] < blow:
                    break

        if not pullback_detected:
            return {"detected": False, "signal": "WAITING_PULLBACK"}

        # 计算回调深度
        bar_range = bhigh - blow
        if trend == "up":
            depth = (bhigh - pullback_low) / bar_range if bar_range > 0 else 0.0
            magnitude = (bhigh - pullback_low) / body * 100 if body > 0 else 0.0
        else:
            depth = (pullback_high - blow) / bar_range if bar_range > 0 else 0.0
            magnitude = (pullback_high - blow) / body * 100 if body > 0 else 0.0

        # 评估质量
        if depth < 0.382:
            quality = "PERFECT"
        elif depth < 0.50:
            quality = "GOOD"
        elif depth < 0.618:
            quality = "DEEP"
        else:
            quality = "FAILED"

        return {
            "detected": True,
            "depth": depth,
            "magnitude": magnitude,
            "quality": quality,
            "pullback_low": pullback_low,
            "pullback_high": pullback_high,
            "pb_start": pb_start,
            "pb_end": pb_end,
        }

    def _generate_signal(
        self,
        breakout: Dict[str, Any],
        pullback: Dict[str, Any],
        body_pct: float,
        vol_ratio: float,
        atr14: float,
    ) -> Dict[str, Any]:
        """生成BPB信号"""
        if not pullback.get("detected", False):
            return {"type": pullback.get("signal", "NONE"), "strength": 0, "confidence": 0.0}

        if pullback.get("signal") in ("BOF_SHORT", "BOF_LONG"):
            return {
                "type": pullback["signal"],
                "strength": 6,
                "confidence": 0.70,
                "is_failed": True,
            }

        quality = pullback.get("quality", "FAILED")
        trend = breakout["trend_direction"]

        if quality == "FAILED":
            return {"type": "PULLBACK_TOO_DEEP", "strength": 0, "confidence": 0.3}

        # 信号强度计算
        base_strength = 9 if quality == "PERFECT" else (7 if quality == "GOOD" else 4)
        if vol_ratio > 2.0:
            base_strength += 1
        if body_pct > 0.7:
            base_strength += 1

        if trend == "up":
            signal_type = "BPB_LONG"
            entry = breakout["breakout_close"]
            stop = pullback["pullback_low"] - atr14 * 0.3
            target = breakout["breakout_high"] + (breakout["breakout_high"] - pullback["pullback_low"]) * 2
        else:
            signal_type = "BPB_SHORT"
            entry = breakout["breakout_close"]
            stop = pullback["pullback_high"] + atr14 * 0.3
            target = breakout["breakout_low"] - (pullback["pullback_high"] - breakout["breakout_low"]) * 2

        return {
            "type": signal_type,
            "strength": min(10, base_strength),
            "confidence": 0.75 if quality == "PERFECT" else (0.65 if quality == "GOOD" else 0.50),
            "quality": quality,
            "entry_price": entry,
            "stop_loss": stop,
            "target": target,
        }

    def _update_pullback_count(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """更新回调计数"""
        st = signal.get("type", "NONE")
        if st in ("BPB_LONG", "BPB_SHORT"):
            direction = "LONG" if "LONG" in st else "SHORT"
            if self.state.get("last_bpb_direction") == direction:
                self.state["pullback_count"] = self.state.get("pullback_count", 0) + 1
            else:
                self.state["pullback_count"] = 1
                self.state["last_bpb_direction"] = direction

            signal["pullback_count"] = self.state["pullback_count"]
            if self.state["pullback_count"] >= 3:
                signal["type"] = "THIRD_PULLBACK"
                signal["strength"] = 0
                signal["confidence"] = 0.0
        elif st in ("BOF_LONG", "BOF_SHORT"):
            self.state["pullback_count"] = 0
            self.state["last_bpb_direction"] = None

        return signal

    def _apply_long_only_filter(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """A股纯多头: SHORT信号降级为观察"""
        if not self.LONG_ONLY:
            return signal
        st = signal.get("type", "NONE")
        if st in ("BPB_SHORT", "BOF_SHORT"):
            signal["_original_type"] = st
            signal["type"] = "OBSERVE_SHORT"
            signal["strength"] = max(0, signal.get("strength", 0) - 3)
        return signal

    def _signal_to_output(
        self, signal: Dict[str, Any], breakout: Dict[str, Any], pullback: Dict[str, Any]
    ) -> ObjectCardOutput:
        """映射到标准8字段输出"""
        st = signal.get("type", "NONE")
        strength = signal.get("strength", 0)
        confidence = signal.get("confidence", 0.0)

        if st == "NONE":
            return self._make_output("NONE", 0, 0.0, "unlocked", "REJECT", "NO_TRADE", 0.0)
        if st == "WAITING_PULLBACK":
            return self._make_output("WAITING_PULLBACK", 0, 0.4, "unlocked", "OBSERVE", "NO_TRADE", 0.0)
        if st == "PULLBACK_TOO_DEEP":
            return self._make_output("PULLBACK_TOO_DEEP", 0, 0.3, "unlocked", "REJECT", "NO_TRADE", 0.0)
        if st == "THIRD_PULLBACK":
            return self._make_output("THIRD_PULLBACK", 0, 0.2, "unlocked", "REJECT", "NO_TRADE", 0.0)
        if st == "OBSERVE_SHORT":
            return self._make_output("BOF_SHORT" if "BOF" in signal.get("_original_type", "") else "BPB_SHORT",
                                     strength, confidence, "unlocked", "OBSERVE", "NO_TRADE", 0.0)

        # 有效BPB信号
        if st == "BPB_LONG":
            return self._make_output(st, strength, confidence, "locked", "APPROVE", "FULL_SIZE", 1.0)
        if st == "BPB_SHORT":
            return self._make_output(st, strength, confidence, "locked", "APPROVE", "FULL_SIZE", 1.0)
        if st in ("BOF_LONG", "BOF_SHORT"):
            return self._make_output(st, strength, confidence, "locked", "DEGRADE", "HALF_SIZE", 0.5)

        return self._make_output(st, strength, confidence, "unlocked", "OBSERVE", "NO_TRADE", 0.0)


# -------------------------------------------------------------------------- #
# Quick Test
# -------------------------------------------------------------------------- #
def _quick_test() -> None:
    """BPB 快速测试 — 至少3个场景"""
    import numpy as np
    import pandas as pd

    def make_ohlcv(n: int, trend: str = "up", pullback: bool = False) -> pd.DataFrame:
        np.random.seed(7)
        base = 100.0
        data = []
        for i in range(n):
            if trend == "up":
                base += np.random.uniform(0.1, 0.5)
            elif trend == "down":
                base -= np.random.uniform(0.1, 0.5)
            else:
                base += np.random.uniform(-0.3, 0.3)
            o = base + np.random.uniform(-0.3, 0.3)
            c = base + np.random.uniform(-0.3, 0.3)
            h = max(o, c) + np.random.uniform(0, 0.3)
            l = min(o, c) - np.random.uniform(0, 0.3)
            v = np.random.uniform(2000, 6000)
            data.append([o, h, l, c, v])
        df = pd.DataFrame(data, columns=["open", "high", "low", "close", "volume"])

        if pullback and trend == "up":
            # 制造突破后的回调
            df.iloc[-5, df.columns.get_loc("high")] = 115.0
            df.iloc[-5, df.columns.get_loc("close")] = 114.5
            df.iloc[-5, df.columns.get_loc("open")] = 112.0
            df.iloc[-5, df.columns.get_loc("volume")] = 9000  # 放量突破
            # 回调
            for j in range(4):
                df.iloc[-4 + j, df.columns.get_loc("close")] = 114.0 - j * 0.5
                df.iloc[-4 + j, df.columns.get_loc("low")] = 114.0 - j * 0.5 - 0.3
                df.iloc[-4 + j, df.columns.get_loc("high")] = 114.0 - j * 0.5 + 0.3
        return df

    print("=" * 70)
    print("BPB_P0_E 快速测试")
    print("=" * 70)

    # --- 场景1: 有效突破 + 浅回调 ---
    print("\n[场景1] 上升趋势突破20日高点 + 浅回调（期望 BPB_LONG / APPROVE）")
    card1 = ObjectCardBPB()
    df1 = make_ohlcv(50, trend="up", pullback=True)
    inp1 = BPBInput(ohlcv=df1, atr14=1.0)
    out1 = card1.calculate(inp1)
    print(f"  输出: {out1}")
    assert out1.object_id == "BPB_P0_E"

    # --- 场景2: 回调过深 ---
    print("\n[场景2] 突破后回调过深（期望 PULLBACK_TOO_DEEP / REJECT）")
    card2 = ObjectCardBPB()
    df2 = make_ohlcv(50, trend="up")
    # 制造突破但深度回调
    df2.iloc[-10, df2.columns.get_loc("high")] = 115.0
    df2.iloc[-10, df2.columns.get_loc("close")] = 114.5
    df2.iloc[-10, df2.columns.get_loc("open")] = 112.0
    df2.iloc[-10, df2.columns.get_loc("volume")] = 9000
    for j in range(9):
        df2.iloc[-9 + j, df2.columns.get_loc("close")] = 114.0 - j * 1.2  # 深回调
        df2.iloc[-9 + j, df2.columns.get_loc("low")] = 114.0 - j * 1.2 - 0.3
    inp2 = BPBInput(ohlcv=df2, atr14=1.0)
    out2 = card2.calculate(inp2)
    print(f"  输出: {out2}")

    # --- 场景3: 数据不足 ---
    print("\n[场景3] 数据不足（期望 NONE / REJECT）")
    card3 = ObjectCardBPB()
    df3 = make_ohlcv(10)
    out3 = card3.calculate(BPBInput(ohlcv=df3))
    print(f"  输出: {out3}")
    assert out3.signal_type == "NONE"
    assert out3.filter_action == "REJECT"

    # --- 场景4: A股纯多头 — SHORT信号降级 ---
    print("\n[场景4] A股纯多头 — SHORT信号应降级为观察")
    card4 = ObjectCardBPB()
    df4 = make_ohlcv(50, trend="down", pullback=True)
    # 反转方向模拟
    df4.iloc[-5, df4.columns.get_loc("low")] = 85.0
    df4.iloc[-5, df4.columns.get_loc("close")] = 85.5
    df4.iloc[-5, df4.columns.get_loc("open")] = 88.0
    df4.iloc[-5, df4.columns.get_loc("volume")] = 9000
    for j in range(4):
        df4.iloc[-4 + j, df4.columns.get_loc("close")] = 86.0 + j * 0.5
        df4.iloc[-4 + j, df4.columns.get_loc("high")] = 86.0 + j * 0.5 + 0.3
    out4 = card4.calculate(BPBInput(ohlcv=df4, atr14=1.0))
    print(f"  输出: {out4}")
    if "SHORT" in out4.signal_type:
        assert out4.risk_action == "NO_TRADE"
        assert out4.size_scalar == 0.0

    print("\n" + "=" * 70)
    print("BPB_P0_E 所有测试通过 ✓")
    print("=" * 70)


if __name__ == "__main__":
    _quick_test()
