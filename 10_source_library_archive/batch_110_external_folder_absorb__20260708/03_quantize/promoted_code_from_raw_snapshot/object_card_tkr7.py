"""
Object Card: TKR7_P0_E — AO Divergence (Awesome Oscillator Divergence)
文档: OBJECT_CARD_TKR7_P0_E__AO_Divergence_v1.0.md

核心逻辑: 计算AO (5期SMA - 34期SMA of median price)，检测价格-AO背离
A股纯多头场景: 做空/平空相关信号仅作为观察，不生成交易。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import numpy as np
import pandas as pd


@dataclass
class AOInput:
    """AO Divergence 输入数据结构"""
    ohlcv: pd.DataFrame
    # 可选外部状态
    kd_week_extreme_zone: Optional[str] = None  # 'OVERBOUGHT' / 'OVERSOLD' / 'neutral'
    lock_signal: Optional[str] = None


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


class ObjectCardTKR7:
    """
    AO Divergence 对象卡
    object_id: TKR7_P0_E
    """
    OBJECT_ID: str = "TKR7_P0_E"
    LONG_ONLY: bool = True

    def __init__(self) -> None:
        self.prev_divergence: Optional[Dict[str, Any]] = None

    # ------------------------------------------------------------------ #
    def calculate(self, inp: AOInput) -> ObjectCardOutput:
        """主入口方法"""
        ohlcv = inp.ohlcv.copy()
        if len(ohlcv) < 40:
            return self._make_output("NONE", 0, 0.0, "unlocked", "REJECT", "NO_TRADE", 0.0,
                                     reason="insufficient_data")

        # 1. 计算 AO
        ao = self._calculate_ao(ohlcv)

        # 2. 峰值检测
        price_peaks = self._detect_peaks(ohlcv["high"].values, ohlcv["low"].values, min_distance=3)
        ao_peaks = self._detect_peaks_ao(ao, min_distance=3)

        # 3. 背离识别
        div = self._identify_divergence(ohlcv, ao, price_peaks, ao_peaks)

        # 4. 信号生成
        signal = self._generate_signal(div, inp)

        # 5. A股纯多头过滤
        signal = self._apply_long_only_filter(signal)

        return self._signal_to_output(signal, div)

    # ------------------------------------------------------------------ #
    def _make_output(self, *args, reason: str = "") -> ObjectCardOutput:
        # args: signal_type, strength, confidence, lock_status, filter_action, risk_action, size_scalar
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

    def _calculate_ao(self, ohlcv: pd.DataFrame) -> pd.Series:
        """计算 Awesome Oscillator"""
        median_price = (ohlcv["high"] + ohlcv["low"]) / 2.0
        sma5 = median_price.rolling(window=5).mean()
        sma34 = median_price.rolling(window=34).mean()
        ao = sma5 - sma34
        return ao

    def _detect_peaks(self, highs: np.ndarray, lows: np.ndarray, min_distance: int = 3) -> Dict[str, List[Dict[str, Any]]]:
        """检测价格峰值和谷值"""
        peaks = []
        valleys = []
        for i in range(min_distance, len(highs) - min_distance):
            # 峰值: 高点比两边高
            if highs[i] > highs[i - 1] and highs[i] > highs[i + 1]:
                if all(highs[i] >= highs[i - j] for j in range(1, min_distance + 1)) and \
                   all(highs[i] >= highs[i + j] for j in range(1, min_distance + 1)):
                    peaks.append({"index": i, "value": float(highs[i])})
            # 谷值: 低点比两边低
            if lows[i] < lows[i - 1] and lows[i] < lows[i + 1]:
                if all(lows[i] <= lows[i - j] for j in range(1, min_distance + 1)) and \
                   all(lows[i] <= lows[i + j] for j in range(1, min_distance + 1)):
                    valleys.append({"index": i, "value": float(lows[i])})
        return {"peaks": peaks, "valleys": valleys}

    def _detect_peaks_ao(self, ao: pd.Series, min_distance: int = 3) -> Dict[str, List[Dict[str, Any]]]:
        """检测AO峰值和谷值"""
        arr = ao.dropna().values
        idx_map = {i: ao.dropna().index[i] for i in range(len(arr))}
        peaks = []
        valleys = []
        for i in range(min_distance, len(arr) - min_distance):
            if arr[i] > arr[i - 1] and arr[i] > arr[i + 1]:
                if all(arr[i] >= arr[i - j] for j in range(1, min_distance + 1)) and \
                   all(arr[i] >= arr[i + j] for j in range(1, min_distance + 1)):
                    peaks.append({"index": idx_map[i], "value": float(arr[i])})
            if arr[i] < arr[i - 1] and arr[i] < arr[i + 1]:
                if all(arr[i] <= arr[i - j] for j in range(1, min_distance + 1)) and \
                   all(arr[i] <= arr[i + j] for j in range(1, min_distance + 1)):
                    valleys.append({"index": idx_map[i], "value": float(arr[i])})
        return {"peaks": peaks, "valleys": valleys}

    def _identify_divergence(
        self,
        ohlcv: pd.DataFrame,
        ao: pd.Series,
        price_peaks: Dict[str, List[Dict[str, Any]]],
        ao_peaks: Dict[str, List[Dict[str, Any]]],
    ) -> Dict[str, Any]:
        """识别AO背离"""
        p_peaks = price_peaks.get("peaks", [])
        p_valleys = price_peaks.get("valleys", [])
        a_peaks = ao_peaks.get("peaks", [])
        a_valleys = ao_peaks.get("valleys", [])

        if len(p_peaks) < 2 or len(a_peaks) < 2:
            return self._empty_divergence()
        if len(p_valleys) < 2 or len(a_valleys) < 2:
            return self._empty_divergence()

        # 取最近两个峰值
        rp = p_peaks[-2:]
        ap = a_peaks[-2:]
        rv = p_valleys[-2:]
        av = a_valleys[-2:]

        # 常规顶背离: 价格创新高，AO未创新高
        if rp[1]["value"] > rp[0]["value"] and ap[1]["value"] < ap[0]["value"]:
            price_diff = rp[1]["value"] - rp[0]["value"]
            ao_diff = ap[0]["value"] - ap[1]["value"]
            strength = min(1.0, (ao_diff / max(abs(price_diff), 0.001)) * 5)
            conf = self._calc_confidence(ap, rp)
            return {
                "type": "REGULAR_BEAR",
                "strength": round(strength, 2),
                "confidence": conf,
                "age": 0,
                "price_peak_diff": price_diff,
                "ao_peak_diff": ao_diff,
            }

        # 常规底背离: 价格创新低，AO未创新低（AO谷值上升）
        if rv[1]["value"] < rv[0]["value"] and av[1]["value"] > av[0]["value"]:
            price_diff = rv[0]["value"] - rv[1]["value"]
            ao_diff = av[1]["value"] - av[0]["value"]
            strength = min(1.0, (ao_diff / max(abs(price_diff), 0.001)) * 5)
            conf = self._calc_confidence(av, rv)
            return {
                "type": "REGULAR_BULL",
                "strength": round(strength, 2),
                "confidence": conf,
                "age": 0,
                "price_peak_diff": price_diff,
                "ao_peak_diff": ao_diff,
            }

        # 隐藏背离检测（简化: 检查价格回调未破前高/前低，AO方向相反）
        # 隐藏底背离
        if rv[1]["value"] > rv[0]["value"] and av[1]["value"] > av[0]["value"]:
            conf = self._calc_confidence(av, rv)
            return {
                "type": "HIDDEN_BULL",
                "strength": 0.5,
                "confidence": conf,
                "age": 0,
                "price_peak_diff": 0.0,
                "ao_peak_diff": 0.0,
            }
        # 隐藏顶背离
        if rp[1]["value"] < rp[0]["value"] and ap[1]["value"] < ap[0]["value"]:
            conf = self._calc_confidence(ap, rp)
            return {
                "type": "HIDDEN_BEAR",
                "strength": 0.5,
                "confidence": conf,
                "age": 0,
                "price_peak_diff": 0.0,
                "ao_peak_diff": 0.0,
            }

        return self._empty_divergence()

    def _empty_divergence(self) -> Dict[str, Any]:
        return {
            "type": "NONE",
            "strength": 0.0,
            "confidence": 0.0,
            "age": 0,
            "price_peak_diff": 0.0,
            "ao_peak_diff": 0.0,
        }

    def _calc_confidence(
        self,
        ao_points: List[Dict[str, Any]],
        price_points: List[Dict[str, Any]],
    ) -> float:
        """计算背离置信度"""
        conf = 0.5
        if len(ao_points) >= 2:
            prominence = abs(ao_points[1]["value"] - ao_points[0]["value"])
            base = max(abs(ao_points[0]["value"]), 0.001)
            conf += min(0.2, prominence / base * 0.3)
        if len(price_points) >= 2:
            span = price_points[1]["index"] - price_points[0]["index"]
            if 5 <= span <= 20:
                conf += 0.2
            elif 3 <= span < 5:
                conf += 0.1
            elif span > 20:
                conf -= 0.1
        return min(1.0, max(0.0, conf))

    def _generate_signal(self, div: Dict[str, Any], inp: AOInput) -> Dict[str, Any]:
        """基于背离生成信号"""
        div_type = div.get("type", "NONE")
        div_conf = div.get("confidence", 0.0)
        div_strength = div.get("strength", 0.0)

        if div_conf < 0.50 or div_type == "NONE":
            return {"type": "NONE", "strength": 0, "confidence": 0.0, "recommendation": "HOLD"}

        signal_type = "NONE"
        strength = 0
        recommendation = "HOLD"

        if div_type == "REGULAR_BEAR":
            signal_type = "REGULAR_BEAR_CONFIRM"
            strength = int(div_strength * 5 + 2)
            recommendation = "REDUCE_LONG"
            # KD极端区 + 顶背离 = 强制退出
            if inp.kd_week_extreme_zone == "OVERBOUGHT":
                signal_type = "FORCE_EXIT_LONG"
                strength = 10
                recommendation = "CLOSE_LONG"

        elif div_type == "REGULAR_BULL":
            signal_type = "REGULAR_BULL_CONFIRM"
            strength = int(div_strength * 5 + 2)
            recommendation = "REDUCE_SHORT"
            if inp.kd_week_extreme_zone == "OVERSOLD":
                signal_type = "FORCE_EXIT_SHORT"
                strength = 10
                recommendation = "CLOSE_SHORT"

        elif div_type == "HIDDEN_BEAR":
            signal_type = "HIDDEN_BEAR_CONFIRM"
            strength = int(div_strength * 3 + 2)
            recommendation = "HOLD"

        elif div_type == "HIDDEN_BULL":
            signal_type = "HIDDEN_BULL_CONFIRM"
            strength = int(div_strength * 3 + 2)
            recommendation = "HOLD"

        # lock过滤
        lock_status = "locked"
        if inp.lock_signal == "conflicting":
            strength = 0
            div_conf = 0.0
            lock_status = "conflicting"
        elif inp.lock_signal == "unlocked":
            lock_status = "unlocked"
            recommendation = "HOLD"

        return {
            "type": signal_type,
            "strength": min(10, strength),
            "confidence": div_conf,
            "recommendation": recommendation,
            "lock_status": lock_status,
            "div": div,
        }

    def _apply_long_only_filter(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """A股纯多头: 做空信号降级为观察"""
        if not self.LONG_ONLY:
            return signal
        st = signal.get("type", "NONE")
        if st in ("FORCE_EXIT_SHORT", "REGULAR_BEAR_CONFIRM"):
            signal["_original_type"] = st
            signal["type"] = "OBSERVE_BEAR"
            signal["strength"] = max(0, signal.get("strength", 0) - 2)
            signal["recommendation"] = "HOLD"
        return signal

    def _signal_to_output(self, signal: Dict[str, Any], div: Dict[str, Any]) -> ObjectCardOutput:
        """映射到标准8字段输出"""
        st = signal.get("type", "NONE")
        strength = signal.get("strength", 0)
        confidence = signal.get("confidence", 0.0)
        lock_status = signal.get("lock_status", "unlocked")
        rec = signal.get("recommendation", "HOLD")

        if st == "NONE":
            return self._make_output("NONE", 0, 0.0, lock_status, "REJECT", "NO_TRADE", 0.0)

        # 映射 filter_action / risk_action / size_scalar
        if st in ("REGULAR_BULL_CONFIRM", "HIDDEN_BULL_CONFIRM"):
            fa = "APPROVE" if rec != "HOLD" else "OBSERVE"
            ra = "HALF_SIZE" if rec != "HOLD" else "NO_TRADE"
            ss = 0.5 if rec != "HOLD" else 0.0
        elif st == "FORCE_EXIT_LONG":
            fa = "DEGRADE"
            ra = "NO_TRADE"
            ss = 0.0
        elif st in ("REGULAR_BEAR_CONFIRM", "FORCE_EXIT_SHORT"):
            fa = "DEGRADE"
            ra = "NO_TRADE"
            ss = 0.0
        elif st in ("HIDDEN_BEAR_CONFIRM",):
            fa = "OBSERVE"
            ra = "NO_TRADE"
            ss = 0.0
        elif st == "OBSERVE_BEAR":
            fa = "OBSERVE"
            ra = "NO_TRADE"
            ss = 0.0
        else:
            fa = "OBSERVE"
            ra = "NO_TRADE"
            ss = 0.0

        # 对于A股纯多头场景，确保SHORT/EXIT_SHORT信号不下单
        if self.LONG_ONLY and st in ("REGULAR_BEAR_CONFIRM", "FORCE_EXIT_SHORT", "HIDDEN_BEAR_CONFIRM"):
            fa = "OBSERVE"
            ra = "NO_TRADE"
            ss = 0.0

        return self._make_output(st, strength, confidence, lock_status, fa, ra, ss)


# -------------------------------------------------------------------------- #
# Quick Test
# -------------------------------------------------------------------------- #
def _quick_test() -> None:
    """TKR7 快速测试 — 至少3个场景"""
    import numpy as np
    import pandas as pd

    def make_ohlcv(n: int, divergence: Optional[str] = None) -> pd.DataFrame:
        np.random.seed(13)
        base = 100.0
        data = []
        for i in range(n):
            base += np.random.uniform(-0.5, 0.5)
            o = base + np.random.uniform(-0.4, 0.4)
            c = base + np.random.uniform(-0.4, 0.4)
            h = max(o, c) + np.random.uniform(0, 0.3)
            l = min(o, c) - np.random.uniform(0, 0.3)
            v = np.random.uniform(1000, 5000)
            data.append([o, h, l, c, v])
        df = pd.DataFrame(data, columns=["open", "high", "low", "close", "volume"])

        if divergence == "regular_bull":
            # 价格创新低但AO上升 => 底背离
            # 制造两个谷值: 价格第二个更低，AO第二个更高
            df.iloc[25, df.columns.get_loc("low")] = 92.0
            df.iloc[25, df.columns.get_loc("close")] = 92.5
            df.iloc[35, df.columns.get_loc("low")] = 88.0   # 更低的价格谷值
            df.iloc[35, df.columns.get_loc("close")] = 89.0
        elif divergence == "regular_bear":
            # 价格创新高但AO下降 => 顶背离
            df.iloc[25, df.columns.get_loc("high")] = 108.0
            df.iloc[25, df.columns.get_loc("close")] = 107.5
            df.iloc[35, df.columns.get_loc("high")] = 112.0  # 更高的价格峰值
            df.iloc[35, df.columns.get_loc("close")] = 111.0
        return df

    print("=" * 70)
    print("TKR7_P0_E (AO Divergence) 快速测试")
    print("=" * 70)

    # --- 场景1: 常规底背离 ---
    print("\n[场景1] 常规底背离 REGULAR_BULL（价格创新低，AO未创新低）")
    card1 = ObjectCardTKR7()
    df1 = make_ohlcv(60, divergence="regular_bull")
    inp1 = AOInput(ohlcv=df1, kd_week_extreme_zone="OVERSOLD")
    out1 = card1.calculate(inp1)
    print(f"  输出: {out1}")
    assert out1.object_id == "TKR7_P0_E"

    # --- 场景2: 常规顶背离 ---
    print("\n[场景2] 常规顶背离 REGULAR_BEAR（价格创新高，AO未创新高）")
    card2 = ObjectCardTKR7()
    df2 = make_ohlcv(60, divergence="regular_bear")
    inp2 = AOInput(ohlcv=df2, kd_week_extreme_zone="OVERBOUGHT")
    out2 = card2.calculate(inp2)
    print(f"  输出: {out2}")

    # --- 场景3: 数据不足 ---
    print("\n[场景3] 数据不足（期望 NONE / REJECT）")
    card3 = ObjectCardTKR7()
    df3 = make_ohlcv(20)
    out3 = card3.calculate(AOInput(ohlcv=df3))
    print(f"  输出: {out3}")
    assert out3.signal_type == "NONE"
    assert out3.filter_action == "REJECT"

    # --- 场景4: A股纯多头 — 做空信号降级 ---
    print("\n[场景4] A股纯多头 — 做空/平空信号应降级为观察")
    card4 = ObjectCardTKR7()
    df4 = make_ohlcv(60, divergence="regular_bear")
    out4 = card4.calculate(AOInput(ohlcv=df4))
    print(f"  输出: {out4}")
    if "BEAR" in out4.signal_type or "EXIT" in out4.signal_type:
        assert out4.risk_action == "NO_TRADE"
        assert out4.size_scalar == 0.0

    print("\n" + "=" * 70)
    print("TKR7_P0_E 所有测试通过 ✓")
    print("=" * 70)


if __name__ == "__main__":
    _quick_test()
