from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parents[1]
PARAMS_PATH = RUNTIME_DIR / "n01_p0_runtime_params_template_v1.json"
DEFAULT_INPUT = Path(__file__).resolve().parent / "n01_first_real_input_bars_v1.csv"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "n01_proof_of_mapping_output_v1.csv"


OUTPUT_COLUMNS = [
    "symbol",
    "timeframe",
    "bar_time",
    "atr_value",
    "atr_ratio",
    "atr_percentile",
    "atr_percentile_regime",
    "squeeze_is_on",
    "squeeze_tier",
    "squeeze_fired",
    "compression_quality_score",
]


@dataclass(frozen=True)
class Bar:
    symbol: str
    timeframe: str
    bar_time: str
    open: float
    high: float
    low: float
    close: float


def load_params() -> dict:
    with PARAMS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_float(value: str) -> float:
    return float(value.strip())


def read_bars(path: Path) -> list[Bar]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        bars: list[Bar] = []
        for row in reader:
            bars.append(
                Bar(
                    symbol=row["symbol"],
                    timeframe=row["timeframe"],
                    bar_time=row["bar_time"],
                    open=parse_float(row["open"]),
                    high=parse_float(row["high"]),
                    low=parse_float(row["low"]),
                    close=parse_float(row["close"]),
                )
            )
    bars.sort(key=lambda b: b.bar_time)
    return bars


def true_range(curr: Bar, prev_close: float | None) -> float:
    hl = curr.high - curr.low
    if prev_close is None:
        return hl
    hc = abs(curr.high - prev_close)
    lc = abs(curr.low - prev_close)
    return max(hl, hc, lc)


def sma(values: list[float]) -> float:
    return sum(values) / float(len(values))


def percentile_rank(value: float, window: list[float]) -> float:
    if not window:
        raise ValueError("percentile window must not be empty")
    less = sum(1 for item in window if item < value)
    equal = sum(1 for item in window if item == value)
    return ((less + (0.5 * equal)) / float(len(window))) * 100.0


def regime_from_percentile(value: float | None) -> str:
    if value is None:
        return "unknown"
    if value > 90.0:
        return "extreme"
    if value > 70.0:
        return "elevated"
    if value >= 30.0:
        return "normal"
    if value >= 10.0:
        return "calm"
    return "squeeze"


def stddev(values: list[float]) -> float:
    if not values:
        raise ValueError("stddev requires at least one value")
    mean = sma(values)
    variance = sum((v - mean) ** 2 for v in values) / float(len(values))
    return variance ** 0.5


def squeeze_tier_from_bands(
    bb_upper: float,
    bb_lower: float,
    kc_upper_high: float,
    kc_lower_high: float,
    kc_upper_mid: float,
    kc_lower_mid: float,
    kc_upper_low: float,
    kc_lower_low: float,
) -> str:
    high_sqz = bb_lower >= kc_lower_high or bb_upper <= kc_upper_high
    mid_sqz = bb_lower >= kc_lower_mid or bb_upper <= kc_upper_mid
    low_sqz = bb_lower >= kc_lower_low or bb_upper <= kc_upper_low
    if high_sqz:
        return "high"
    if mid_sqz:
        return "medium"
    if low_sqz:
        return "low"
    return "off"


def clamp(value: float, lo: float, hi: float) -> float:
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value


def safe_div(n: float, d: float) -> float | None:
    if d == 0.0:
        return None
    return n / d


def normalized_score_from_ratio(ratio: float, good_at: float, bad_at: float) -> float:
    if bad_at == good_at:
        return 0.0
    t = (ratio - good_at) / (bad_at - good_at)
    return 1.0 - clamp(t, 0.0, 1.0)


def compute_compression_quality_score(
    bars: list[Bar],
    trs: list[float],
    atrs: list[float | None],
    baseline_atrs: list[float | None],
    range_window: int,
    noise_window: int,
    containment_window: int,
) -> list[float | None]:
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    opens = [b.open for b in bars]

    out: list[float | None] = []
    for i in range(len(bars)):
        atr = atrs[i]
        baseline_atr = baseline_atrs[i]
        if atr is None or baseline_atr is None or baseline_atr == 0.0:
            out.append(None)
            continue
        if i + 1 < max(range_window, noise_window, containment_window):
            out.append(None)
            continue

        atr_ratio = atr / baseline_atr
        atr_score = normalized_score_from_ratio(atr_ratio, good_at=0.60, bad_at=1.10)

        r_hi = max(highs[i - range_window + 1 : i + 1])
        r_lo = min(lows[i - range_window + 1 : i + 1])
        recent_range = r_hi - r_lo
        tr_window = trs[i - range_window + 1 : i + 1]
        # Compare window span to window total movement on the same scale.
        baseline_range = sum(tr_window)
        range_ratio = safe_div(recent_range, baseline_range)
        if range_ratio is None:
            out.append(None)
            continue
        range_score = normalized_score_from_ratio(range_ratio, good_at=0.17, bad_at=0.34)

        bodies: list[float] = []
        for j in range(i - noise_window + 1, i + 1):
            rng = highs[j] - lows[j]
            if rng <= 0.0:
                continue
            bodies.append(abs(closes[j] - opens[j]) / rng)
        body_quality = sma(bodies) if bodies else 0.0

        changes: list[float] = []
        for j in range(i - noise_window + 1, i + 1):
            if j == 0:
                continue
            changes.append(closes[j] - closes[j - 1])
        flips = 0
        prev_sign: int | None = None
        for ch in changes:
            sign = 0
            if ch > 0.0:
                sign = 1
            elif ch < 0.0:
                sign = -1
            if sign == 0:
                continue
            if prev_sign is not None and sign != prev_sign:
                flips += 1
            prev_sign = sign
        flip_ratio = flips / float(max(1, len(changes)))
        noise_score = clamp((0.70 * body_quality) + (0.30 * (1.0 - flip_ratio)), 0.0, 1.0)

        c_hi = max(highs[i - containment_window + 1 : i + 1])
        c_lo = min(lows[i - containment_window + 1 : i + 1])
        c_rng = c_hi - c_lo
        if c_rng <= 0.0:
            out.append(None)
            continue
        inner_lo = c_lo + (0.25 * c_rng)
        inner_hi = c_hi - (0.25 * c_rng)
        inside = 0
        for j in range(i - containment_window + 1, i + 1):
            if inner_lo <= closes[j] <= inner_hi:
                inside += 1
        containment_score = inside / float(containment_window)

        score = (
            (30.0 * atr_score)
            + (30.0 * range_score)
            + (20.0 * noise_score)
            + (20.0 * containment_score)
        )
        out.append(clamp(score, 0.0, 100.0))

    return out


def fmt_num(value: float, decimals: int = 6) -> str:
    return ("{0:0." + str(decimals) + "f}").format(value)


def write_output(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument(
        "--decimals",
        type=int,
        default=6,
        help="number formatting decimals for atr fields",
    )
    args = parser.parse_args()

    params = load_params()
    atr_len = int(params["atr_config"]["atr_length"])
    baseline_len = int(params["atr_config"]["atr_baseline_length"])
    percentile_window = int(params["atr_config"]["atr_percentile_window"])
    squeeze_len = 20
    bb_mult = 2.0
    kc_mult_high = 1.0
    kc_mult_mid = 1.5
    kc_mult_low = 2.0
    range_window = 20
    noise_window = 10
    containment_window = 24

    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    bars = read_bars(input_path)
    if len(bars) < atr_len:
        raise ValueError("not enough bars for atr_length={0}".format(atr_len))

    trs: list[float] = []
    atrs: list[float | None] = []
    prev_close: float | None = None
    for b in bars:
        tr = true_range(b, prev_close)
        trs.append(tr)
        prev_close = b.close
        if len(trs) >= atr_len:
            atrs.append(sma(trs[-atr_len:]))
        else:
            atrs.append(None)

    baseline_atrs: list[float | None] = []
    for i in range(len(atrs)):
        window = [v for v in atrs[max(0, i - baseline_len + 1) : i + 1] if v is not None]
        if len(window) >= baseline_len:
            baseline_atrs.append(sma(window[-baseline_len:]))
        else:
            baseline_atrs.append(None)

    atr_percentiles: list[float | None] = []
    for i in range(len(atrs)):
        window = [v for v in atrs[max(0, i - percentile_window + 1) : i + 1] if v is not None]
        if len(window) >= percentile_window and atrs[i] is not None:
            atr_percentiles.append(percentile_rank(atrs[i], window[-percentile_window:]))
        else:
            atr_percentiles.append(None)

    closes = [b.close for b in bars]
    squeeze_tiers: list[str] = []
    for i in range(len(bars)):
        if i + 1 < squeeze_len or atrs[i] is None:
            squeeze_tiers.append("off")
            continue
        close_window = closes[i - squeeze_len + 1 : i + 1]
        bb_basis = sma(close_window)
        dev = bb_mult * stddev(close_window)
        bb_upper = bb_basis + dev
        bb_lower = bb_basis - dev
        kc_basis = sma(close_window)
        dev_kc = sma([v for v in trs[i - squeeze_len + 1 : i + 1]])
        squeeze_tiers.append(
            squeeze_tier_from_bands(
                bb_upper=bb_upper,
                bb_lower=bb_lower,
                kc_upper_high=kc_basis + (dev_kc * kc_mult_high),
                kc_lower_high=kc_basis - (dev_kc * kc_mult_high),
                kc_upper_mid=kc_basis + (dev_kc * kc_mult_mid),
                kc_lower_mid=kc_basis - (dev_kc * kc_mult_mid),
                kc_upper_low=kc_basis + (dev_kc * kc_mult_low),
                kc_lower_low=kc_basis - (dev_kc * kc_mult_low),
            )
        )

    compression_scores = compute_compression_quality_score(
        bars=bars,
        trs=trs,
        atrs=atrs,
        baseline_atrs=baseline_atrs,
        range_window=range_window,
        noise_window=noise_window,
        containment_window=containment_window,
    )

    out_rows: list[dict] = []
    for i, b in enumerate(bars):
        atr = atrs[i]
        baseline = baseline_atrs[i]
        atr_percentile_value = atr_percentiles[i]
        squeeze_tier = squeeze_tiers[i]
        squeeze_is_on = "1" if squeeze_tier != "off" else "0"
        prev_tier = squeeze_tiers[i - 1] if i > 0 else "off"
        squeeze_fired = "1" if squeeze_tier == "off" and prev_tier != "off" else "0"
        atr_value = "na" if atr is None else fmt_num(atr, decimals=args.decimals)
        atr_ratio = "na"
        if atr is not None and baseline is not None and baseline != 0.0:
            atr_ratio = fmt_num(atr / baseline, decimals=4)
        atr_percentile = "na" if atr_percentile_value is None else fmt_num(atr_percentile_value, decimals=2)
        compression_score_value = compression_scores[i]
        compression_score = "na" if compression_score_value is None else fmt_num(compression_score_value, decimals=2)
        out_rows.append(
            {
                "symbol": b.symbol,
                "timeframe": b.timeframe,
                "bar_time": b.bar_time,
                "atr_value": atr_value,
                "atr_ratio": atr_ratio,
                "atr_percentile": atr_percentile,
                "atr_percentile_regime": regime_from_percentile(atr_percentile_value),
                "squeeze_is_on": squeeze_is_on,
                "squeeze_tier": squeeze_tier,
                "squeeze_fired": squeeze_fired,
                "compression_quality_score": compression_score,
            }
        )

    write_output(output_path, out_rows)

    computed_atr = sum(1 for v in atrs if v is not None)
    computed_ratio = sum(1 for v in baseline_atrs if v is not None)
    computed_percentile = sum(1 for v in atr_percentiles if v is not None)
    computed_squeeze_on = sum(1 for v in squeeze_tiers if v != "off")
    computed_squeeze_fired = sum(
        1 for i, v in enumerate(squeeze_tiers) if v == "off" and i > 0 and squeeze_tiers[i - 1] != "off"
    )
    computed_compression_score = sum(1 for v in compression_scores if v is not None)
    print("input={0}".format(input_path))
    print("output={0}".format(output_path))
    print("bars={0}".format(len(bars)))
    print("atr_length={0}".format(atr_len))
    print("baseline_length={0}".format(baseline_len))
    print("percentile_window={0}".format(percentile_window))
    print("atr_values_computed={0}".format(computed_atr))
    print("atr_ratio_computed={0}".format(computed_ratio))
    print("atr_percentile_computed={0}".format(computed_percentile))
    print("squeeze_on_rows={0}".format(computed_squeeze_on))
    print("squeeze_fired_rows={0}".format(computed_squeeze_fired))
    print("compression_quality_score_non_na={0}".format(computed_compression_score))
    print("last_bar_time={0}".format(bars[-1].bar_time))


if __name__ == "__main__":
    main()
