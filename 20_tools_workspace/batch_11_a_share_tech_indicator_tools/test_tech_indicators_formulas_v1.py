"""
test_tech_indicators_formulas_v1.py
===================================
Cursor 技术指标公式标准答案测试（不依赖真实数据，固定 60 个收盘价序列）

用法：
    python test_tech_indicators_formulas_v1.py
    （可选）环境里装了 pandas / pandas-ta 时，会自动跑标准答案交叉验证

任何时候写完新的指标计算函数（比如 calc_daily_bar_pool_with_indicators_v1.py
或 calc_index_daily_indicators_v1.py 里的 MA/MACD/RSI/BOLL 逻辑），都把
你的结果和本脚本输出的 REFERENCE 对比。不一致 = 公式写错了。
"""
from __future__ import annotations

import csv
import math
import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple

# ======================================================================
# 1. 固定测试收盘价序列（60 个：含上升 1-30 / 下降 31-50 / 震荡 51-60 三段）
# ======================================================================
TEST_CLOSE: List[float] = [
    101.0, 102.5, 103.2, 105.8, 106.1, 107.3, 108.9, 110.4, 112.0, 113.6,  # 0-9  上升段
    115.2, 116.8, 118.4, 120.0, 121.5, 123.1, 124.7, 126.2, 127.8, 129.3,  # 10-19
    130.9, 132.4, 133.9, 135.4, 136.8, 138.3, 139.7, 141.1, 142.5, 143.8,  # 20-29
    145.1, 146.4, 147.6, 148.8, 150.0, 148.5, 147.0, 145.5, 143.9, 142.3,  # 30-39 下降段
    140.7, 139.1, 137.5, 135.9, 134.3, 132.7, 131.2, 129.7, 128.2, 126.8,  # 40-49
    125.5, 124.3, 123.2, 122.2, 121.4, 120.7, 120.1, 119.7, 119.4, 119.2,  # 50-59 震荡段
]


# ======================================================================
# 2. 教科书公式实现（就是标准答案，任何其他实现都要和这里对得上）
# ======================================================================

def ma(series: List[float], n: int) -> List[Optional[float]]:
    """一、简单移动平均：前 N 天算术平均；前 N-1 天 = NA"""
    out: List[Optional[float]] = [None] * len(series)
    s = 0.0
    for i in range(len(series)):
        s += series[i]
        if i >= n:
            s -= series[i - n]
        if i >= n - 1:
            out[i] = s / n
    return out


def ema(series: List[float], n: int) -> List[float]:
    """
    二、指数移动平均：
        EMA_today = EMA_prev * (N-1)/(N+1) + today * 2/(N+1)
        首日 EMA = 首日 close（而不是 SMA(N)，避免首日不一致）
    """
    out: List[float] = [0.0] * len(series)
    k = 2.0 / (n + 1.0)
    out[0] = series[0]
    for i in range(1, len(series)):
        out[i] = out[i - 1] * (1.0 - k) + series[i] * k
    return out


def macd(series: List[float], fast: int = 12, slow: int = 26, signal: int = 9
         ) -> Tuple[List[float], List[float], List[float]]:
    """
    三、MACD（标准参数 12, 26, 9）：
        DIF  = EMA(C, 12) - EMA(C, 26)
        DEA  = EMA(DIF, 9)
        MACD柱 = 2 * (DIF - DEA)  （很多软件都 x2，保持一致）
    """
    e12 = ema(series, fast)
    e26 = ema(series, slow)
    dif = [e12[i] - e26[i] for i in range(len(series))]
    dea = ema(dif, signal)
    bar = [2.0 * (dif[i] - dea[i]) for i in range(len(series))]
    return dif, dea, bar


def rsi(series: List[float], n: int) -> List[Optional[float]]:
    """
    四、RSI（Wilder 平滑法，不是 SMA，也不是 EMA_twice）：
        delta = today - yesterday
        gains[n-1..] = max(delta, 0)
        losses[n-1..] = max(-delta, 0)
        第一个 avg_g / avg_l = 前 N 个 delta 的简单平均
        后续 Wilder 平滑：avg = (prev_avg * (N-1) + today_delta) / N
        RSI = 100 - 100 / (1 + RS)，  RS = avg_g / avg_l  （avg_l=0 时 RSI=100）
    """
    out: List[Optional[float]] = [None] * len(series)
    if len(series) <= n:
        return out
    gains: List[float] = []
    losses: List[float] = []
    for i in range(1, len(series)):
        d = series[i] - series[i - 1]
        gains.append(max(d, 0.0))
        losses.append(max(-d, 0.0))
    avg_g = sum(gains[:n]) / n
    avg_l = sum(losses[:n]) / n
    out[n] = 100.0 - 100.0 / (1.0 + (avg_g / max(avg_l, 1e-12)))
    for i in range(n + 1, len(series)):
        g = gains[i - 1]
        l = losses[i - 1]
        avg_g = (avg_g * (n - 1) + g) / n
        avg_l = (avg_l * (n - 1) + l) / n
        out[i] = 100.0 - 100.0 / (1.0 + (avg_g / max(avg_l, 1e-12)))
    return out


def boll(series: List[float], n: int = 20, k: float = 2.0
         ) -> Tuple[List[Optional[float]], List[Optional[float]], List[Optional[float]]]:
    """
    五、BOLL（N=20，K 倍标准差 = 2）：
        中轨 = MA(C, 20)
        σ    = sqrt( (1/N) * Σ (C_i - 中轨)^2 )   （总体标准差，分母 N 不是 N-1）
        上轨 = 中轨 + K*σ
        下轨 = 中轨 - K*σ
    """
    mid = ma(series, n)
    up: List[Optional[float]] = [None] * len(series)
    lo: List[Optional[float]] = [None] * len(series)
    for i in range(len(series)):
        if mid[i] is None:
            continue
        win = series[i - n + 1:i + 1]
        mean = mid[i]
        assert mean is not None
        var = sum((x - mean) ** 2 for x in win) / n
        sigma = math.sqrt(var)
        up[i] = mean + k * sigma
        lo[i] = mean - k * sigma
    return up, mid, lo


# ======================================================================
# 3. 用 pandas-ta 交叉验证（有装就跑，没装就跳过）
#    注意：行业内有 3 类经典定义差异，必须在交叉验证里分别对齐，否则永远 FAIL：
#    1) EMA 定义分两种：
#        定义A「教科书第一笔用 close[0]」=我们自己的 ema()
#        定义B「pandas-ta / ta-lib 统一用法」=先用 SMA(N) 做第N笔EMA，
#            然后第N+1笔开始套公式 2/(N+1)。我们 ema_sma_align() 就是这个版本
#    2) RSI 定义分两种：
#        Wilder 平滑 vs. EMA 平滑(ta-lib)。pandas-ta rsi 默认 Wilder，但是会在
#        length+1 开始给值（从 length 开始给，和我们不同步），前几项对齐即可，
#        后面会收敛到相同。
#    3) BOLL 的 sigma 分母分两种：总体(N) vs 样本(N-1)
#        pandas-ta bbands 默认是 样本(N-1)=ddof=1；我们这里是 总体(N)=ddof=0。
#        所以给 BOLL 单独做一个 bbands_ddof1_align=样本标准差版本做对齐
# ======================================================================
def ema_sma_align(series: List[float], n: int) -> List[Optional[float]]:
    """pandas-ta 的 EMA 定义：第 N-1 笔用 SMA(N)，之后 EMA_t = EMA_{t-1}*(N-1)/(N+1) + C_t*2/(N+1)；前 N-1 笔=NA"""
    out: List[Optional[float]] = [None] * len(series)
    if len(series) < n:
        return out
    s = sum(series[:n]) / n
    out[n - 1] = s
    k = 2.0 / (n + 1.0)
    for i in range(n, len(series)):
        prev = out[i - 1]
        assert prev is not None
        out[i] = prev * (1.0 - k) + series[i] * k
    return out


def macd_sma_align(series: List[float], fast: int = 12, slow: int = 26, signal: int = 9
                   ) -> Tuple[List[Optional[float]], List[Optional[float]], List[Optional[float]]]:
    """pandas-ta 的 MACD：EMA12/EMA26 都先以 SMA(N) 初始化；MACD柱默认不 x2（只x1）。
    返回顺序=(DIF线, DEA信号线, MACD直方图=DIF-DEA=和pandas-ta一致)"""
    e12 = ema_sma_align(series, fast)
    e26 = ema_sma_align(series, slow)
    dif: List[Optional[float]] = [None] * len(series)
    for i in range(len(series)):
        if e12[i] is None or e26[i] is None:
            continue
        dif[i] = float(e12[i]) - float(e26[i])  # type: ignore[arg-type]
    # DEA = EMA_sma_align( DIF序列(遇到None前补齐跳过的方式喂) , signal=9 )
    # pandas-ta 直接用 pd.Series 调用 .ema(signal)，所以前 (slow-1) + (signal-1) 项=NaN
    # 我们直接传 dif 给 ema_sma_align，但是 ema_sma_align 把前N-1个当做None跳过，
    # 它要求输入是实值 -> 所以先把 dif 中第一个非 None 之后切成子数组，喂给
    # ema_sma_align 得到 dea 子数组，再拼回去。
    first_i = next((i for i, v in enumerate(dif) if v is not None), len(dif))
    dif_slice = [float(x) for x in dif[first_i:] if x is not None]
    dea_slice = ema_sma_align(dif_slice, signal)  # List[Optional[float]]
    dea: List[Optional[float]] = [None] * len(series)
    bar: List[Optional[float]] = [None] * len(series)
    for j, v in enumerate(dea_slice):
        if v is not None:
            dea[first_i + j] = float(v)
    for i in range(len(series)):
        if dif[i] is not None and dea[i] is not None:
            bar[i] = float(dif[i]) - float(dea[i])  # pandas-ta 默认 MACD_hist = DIF - DEA，不乘2
    return dif, dea, bar


def rsi_ema_pandasta(series: List[float], n: int) -> List[Optional[float]]:
    """
    pandas-ta rsi 默认=EMA 平滑（和 Wilder 不同，不要搞混）：
        delta = today - prev
        gain_ema  = EMA(max(delta,0), n, alpha=1/n  即 Wilder 等效平滑)
        loss_ema  = EMA(max(-delta,0), n, alpha=1/n)
        所以本质上就是 pandas-ta rsi 的默认实现：它的alpha=1/n，等价于Wilder
        但是它从 index=n-1=13（第14天）就给第一个值，而我们 Wilder 版从 index=14
        给。所以直接套用这个定义。
    """
    out: List[Optional[float]] = [None] * len(series)
    if len(series) <= n:
        return out
    gains, losses = [], []
    for i in range(1, len(series)):
        d = series[i] - series[i - 1]
        gains.append(max(d, 0.0))
        losses.append(max(-d, 0.0))
    alpha = 1.0 / n
    avg_g = gains[0]
    avg_l = losses[0]
    # EMA 平均（alpha=1/n = Wilder 等效，和 pandas-ta 一致）
    # pandas-ta 从 index=n（即第 n+1 天，从0算起i=n 时）给值，这里直接对齐
    for i in range(1, len(gains)):
        avg_g = alpha * gains[i] + (1.0 - alpha) * avg_g
        avg_l = alpha * losses[i] + (1.0 - alpha) * avg_l
        idx_series = i + 1
        if i >= n - 1:
            out[idx_series] = 100.0 - 100.0 / (1.0 + (avg_g / max(avg_l, 1e-12)))
    return out


def boll_sample_std(series: List[float], n: int = 20, k: float = 2.0
                    ) -> Tuple[List[Optional[float]], List[Optional[float]], List[Optional[float]]]:
    """pandas-ta bbands：中轨=SMA(N)，上/下轨用的是 N-1 样本标准差 ddof=1。"""
    mid = ma(series, n)
    up: List[Optional[float]] = [None] * len(series)
    lo: List[Optional[float]] = [None] * len(series)
    for i in range(len(series)):
        if mid[i] is None:
            continue
        win = series[i - n + 1:i + 1]
        mean = mid[i]
        assert mean is not None
        if n <= 1:
            var = 0.0
        else:
            var = sum((x - mean) ** 2 for x in win) / (n - 1)
        sigma = math.sqrt(var)
        up[i] = mean + k * sigma
        lo[i] = mean - k * sigma
    return up, mid, lo


def try_pandas_ta_crosscheck() -> Optional[str]:
    import sys as _sys
    from pathlib import Path as _Path
    local_target = _Path(__file__).resolve().parent / "_pipsite_pandas_ta"
    if local_target.exists() and str(local_target) not in _sys.path:
        _sys.path.insert(0, str(local_target))
    try:
        import pandas as pd          # type: ignore
        import pandas_ta as ta       # type: ignore
    except Exception as e:
        return f"[pandas-ta 交叉验证 SKIP] 未安装：{e}"

    s = pd.Series(TEST_CLOSE, name="CLOSE")
    ref_ma5 = ta.sma(s, 5)
    ref_ma10 = ta.sma(s, 10)
    ref_ma20 = ta.sma(s, 20)
    ref_ema12 = ta.ema(s, 12)
    ref_ema26 = ta.ema(s, 26)
    macd_df = ta.macd(s, fast=12, slow=26, signal=9)
    # pandas-ta macd 的列顺序 = [DIF(=MACD_line), 柱(MACD_hist=x1不乘2), DEA(=MACD_signal)]
    ref_dif = macd_df.iloc[:, 0]
    ref_bar = macd_df.iloc[:, 1]
    ref_dea = macd_df.iloc[:, 2]
    ref_rsi14 = ta.rsi(s, 14)
    boll_df = ta.bbands(s, length=20, std=2.0)
    ref_boll_mid = boll_df.iloc[:, 1]
    ref_boll_u = boll_df.iloc[:, 2]
    ref_boll_l = boll_df.iloc[:, 0]

    our_ma5 = ma(TEST_CLOSE, 5)
    our_ma10 = ma(TEST_CLOSE, 10)
    our_ma20 = ma(TEST_CLOSE, 20)
    our_ema12 = ema_sma_align(TEST_CLOSE, 12)
    our_ema26 = ema_sma_align(TEST_CLOSE, 26)
    our_dif, our_dea, our_bar = macd_sma_align(TEST_CLOSE)
    our_rsi14 = rsi_ema_pandasta(TEST_CLOSE, 14)
    our_boll_u, our_boll_mid, our_boll_l = boll_sample_std(TEST_CLOSE)

    def cmp(name: str, ours: List[Optional[float]], theirs: pd.Series, tol: float = 1e-8,
            skip_first_n: int = 0) -> str:
        diffs = 0
        max_abs = 0.0
        for i in range(len(ours)):
            if i < skip_first_n:
                continue
            o = ours[i]
            t = theirs.iloc[i]
            if o is None:
                if pd.notna(t):
                    diffs += 1
                continue
            if pd.isna(t):
                diffs += 1
                continue
            d = abs(float(o) - float(t))
            if d > tol:
                diffs += 1
                max_abs = max(max_abs, d)
        status = "[PASS]" if diffs == 0 else f"[FAIL] diffs={diffs} max_abs_e={max_abs:.3e}"
        return f"  {name:<20s}: {status}"

    lines = ["\n===== 【pandas-ta 标准答案交叉验证（统一用 ta-lib / pandas-ta 业界定义）】====="]
    lines.append(cmp("MA5  (SMA)", our_ma5, ref_ma5))
    lines.append(cmp("MA10 (SMA)", our_ma10, ref_ma10))
    lines.append(cmp("MA20 (SMA)", our_ma20, ref_ma20))
    lines.append(cmp("EMA12 (SMA 初始化)", our_ema12, ref_ema12, 1e-6))
    lines.append(cmp("EMA26 (SMA 初始化)", our_ema26, ref_ema26, 1e-6))
    lines.append(cmp("MACD DIF (SMA对齐)", our_dif, ref_dif, 1e-6))
    lines.append(cmp("MACD DEA (Signal=EMA9)", our_dea, ref_dea, 1e-6))
    lines.append(cmp("MACD柱(x1, hist)", our_bar, ref_bar, 1e-6))
    lines.append(cmp("RSI14 (EMA平滑, 业界标准)", our_rsi14, ref_rsi14, 5e-6, skip_first_n=14))
    lines.append(cmp("BOLL 中轨(MA20)", our_boll_mid, ref_boll_mid))
    lines.append(cmp("BOLL 上轨(N-1样本σ)", our_boll_u, ref_boll_u, 1e-6))
    lines.append(cmp("BOLL 下轨(N-1样本σ)", our_boll_l, ref_boll_l, 1e-6))
    return "\n".join(lines)



# ======================================================================
# 4. 主函数：打印首末参考值 + 导出完整 reference CSV（给 Cursor 对照）
# ======================================================================

def main() -> int:
    print("=" * 70)
    print("  Cursor 技术指标公式标准答案测试  |  固定 60 个收盘价序列")
    print("=" * 70)
    print(f"样本数  : {len(TEST_CLOSE)}")
    print(f"前 5 价 : {TEST_CLOSE[:5]}")
    print(f"后 5 价 : {TEST_CLOSE[-5:]}")

    # --- 计算所有指标 ---
    ma5  = ma(TEST_CLOSE, 5)
    ma10 = ma(TEST_CLOSE, 10)
    ma20 = ma(TEST_CLOSE, 20)
    ema12 = ema(TEST_CLOSE, 12)
    ema26 = ema(TEST_CLOSE, 26)
    dif, dea, bar = macd(TEST_CLOSE)
    rsi6  = rsi(TEST_CLOSE, 6)
    rsi12 = rsi(TEST_CLOSE, 12)
    rsi14 = rsi(TEST_CLOSE, 14)
    rsi24 = rsi(TEST_CLOSE, 24)
    boll_u, boll_mid, boll_l = boll(TEST_CLOSE)

    # --- 首天有值 + 末日(第60天) 参考值快速打印 ---
    def pr(name: str, arr: List[Optional[float]], i: int, nd: int = 4) -> None:
        v = arr[i]
        s = "NA" if v is None else f"{v:.{nd}f}"
        print(f"  第 {i+1:>3} 天  {name:<18s}: {s}")

    print("\n[一、MA（简单移动平均）→ 第N天首次有值 + 最后一天(第60天) REFERENCE]")
    for name, arr, first_i in [("MA5",  ma5,  4),
                                ("MA10", ma10, 9),
                                ("MA20", ma20, 19)]:
        pr(f"{name} 首日", arr, first_i, 4)
        pr(f"{name} 末日", arr, 59, 4)

    print("\n[二、EMA → 首日(第1天)+末日]")
    for name, arr in [("EMA12", ema12), ("EMA26", ema26)]:
        pr(f"{name} 首日", arr, 0, 6)
        pr(f"{name} 末日", arr, 59, 6)

    print("\n[三、MACD(12,26,9) → DIF / DEA / MACD柱(x2) 首日+末日]")
    for name, arr in [("DIF", dif), ("DEA", dea), ("MACD柱x2", bar)]:
        pr(f"{name} 首日", arr, 0, 8)
        pr(f"{name} 末日", arr, 59, 8)

    print("\n[四、RSI(Wilder 平滑) → RSI6/12/14/24 首次有值日+末日]")
    for name, arr, first_i in [("RSI6",  rsi6,  6),
                                ("RSI12", rsi12, 12),
                                ("RSI14", rsi14, 14),
                                ("RSI24", rsi24, 24)]:
        pr(f"{name} 首日", arr, first_i, 6)
        pr(f"{name} 末日", arr, 59, 6)

    print("\n[五、BOLL(N=20, K=2σ) → 首日(第20天)/末日 上/中/下轨]")
    for name, arr, first_i in [("BOLL_U 上轨", boll_u, 19),
                                ("BOLL_M 中轨", boll_mid, 19),
                                ("BOLL_L 下轨", boll_l, 19)]:
        pr(f"{name} 首日", arr, first_i, 4)
        pr(f"{name} 末日", arr, 59, 4)

    # --- pandas-ta 交叉验证 ---
    cc = try_pandas_ta_crosscheck()
    print(cc)

    # --- 导出完整 60 行 REFERENCE CSV（给 Cursor 当合同） ---
    out_dir = Path(__file__).resolve().parent
    csv_path = out_dir / "batch_11_tech_indicators_reference_values_20260813.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow([
            "i_day(1~60)", "CLOSE_fixed",
            "MA5", "MA10", "MA20",
            "EMA12", "EMA26", "DIF", "DEA", "MACD_BAR_x2",
            "RSI6", "RSI12", "RSI14", "RSI24",
            "BOLL_U(20,2σ)", "BOLL_M(MA20)", "BOLL_L(20,2σ)",
        ])
        for i in range(len(TEST_CLOSE)):
            def fv(v: Optional[float]) -> str:
                return "" if v is None else f"{v:.10f}"
            w.writerow([
                i + 1, f"{TEST_CLOSE[i]:.4f}",
                fv(ma5[i]), fv(ma10[i]), fv(ma20[i]),
                fv(ema12[i]), fv(ema26[i]), fv(dif[i]), fv(dea[i]), fv(bar[i]),
                fv(rsi6[i]), fv(rsi12[i]), fv(rsi14[i]), fv(rsi24[i]),
                fv(boll_u[i]), fv(boll_mid[i]), fv(boll_l[i]),
            ])
    print("\n[OK] REFERENCE CSV 已导出（Cursor 写任何计算逻辑都对照这个文件：")
    print(f"   {csv_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
