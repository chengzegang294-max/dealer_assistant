from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REQUIRED_COLUMNS = {"date", "open", "high", "low", "close", "volume"}


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("input csv has no rows")
    missing = REQUIRED_COLUMNS - set(rows[0].keys())
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")
    return rows


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


def allocate_profile(rows: list[dict[str, str]], n_bins: int = 24) -> tuple[list[tuple[float, float]], float, float]:
    price_min = min(f(r, "low") for r in rows)
    price_max = max(f(r, "high") for r in rows)
    if price_max <= price_min:
        price_max = price_min + 1e-6
    bin_size = (price_max - price_min) / n_bins
    bins = [0.0 for _ in range(n_bins)]
    for row in rows:
        typical = (f(row, "high") + f(row, "low") + f(row, "close")) / 3.0
        idx = int((typical - price_min) / bin_size)
        idx = min(max(idx, 0), n_bins - 1)
        bins[idx] += f(row, "volume")
    profile = [(price_min + (i + 0.5) * bin_size, v) for i, v in enumerate(bins)]
    return profile, price_min, price_max


def calc_value_area(profile: list[tuple[float, float]], va_pct: float = 0.70) -> tuple[float, float, float]:
    total = sum(v for _, v in profile)
    poc_price = max(profile, key=lambda x: x[1])[0]
    poc_idx = next(i for i, (p, _) in enumerate(profile) if p == poc_price)
    target = total * va_pct
    cum = profile[poc_idx][1]
    left = right = poc_idx
    while cum < target and (left > 0 or right < len(profile) - 1):
        left_vol = profile[left - 1][1] if left > 0 else -1.0
        right_vol = profile[right + 1][1] if right < len(profile) - 1 else -1.0
        if right_vol >= left_vol and right < len(profile) - 1:
            right += 1
            cum += profile[right][1]
        elif left > 0:
            left -= 1
            cum += profile[left][1]
        else:
            break
    return poc_price, profile[right][0], profile[left][0]


def classify_shape(profile: list[tuple[float, float]], poc: float, price_min: float, price_max: float) -> str:
    volumes = [v for _, v in profile]
    avg_vol = sum(volumes) / len(volumes)
    hvn = [p for p, v in profile if v > avg_vol * 1.5]
    if len(hvn) <= 1:
        return "single_peak"
    mid = (price_min + price_max) / 2.0
    hvn_avg = sum(hvn) / len(hvn)
    if poc > mid and hvn_avg > mid:
        return "ascending"
    if poc < mid and hvn_avg < mid:
        return "descending"
    return "balanced"


def calc_output(rows: list[dict[str, str]]) -> dict[str, object]:
    if len(rows) < 10:
        return {
            "object_id": "VP_P0_E",
            "input_rows": len(rows),
            "as_of_date": rows[-1]["date"],
            "signal_payload": {
                "object_id": "VP_P0_E",
                "vp_poc": 0.0,
                "vp_vah": 0.0,
                "vp_val": 0.0,
                "vp_hvn_levels": [],
                "vp_lvn_levels": [],
                "vp_current_rel_position": "inside",
                "vp_trend_shape": "balanced",
                "vp_signal_type": "NONE",
                "vp_signal_strength": 0,
                "vp_suggested_stop": None,
                "vp_suggested_target": None,
            },
            "acceptance_flags": {
                "passed_min_rows": False,
                "degraded": True,
                "degrade_reason": "window_lt_10",
            },
        }

    window = rows[-60:] if len(rows) > 60 else rows
    profile, price_min, price_max = allocate_profile(window)
    poc, vah, val = calc_value_area(profile)
    avg_vol = sum(v for _, v in profile) / len(profile)
    hvn = sorted(round(p, 4) for p, v in profile if v > avg_vol * 1.5)
    lvn = sorted(round(p, 4) for p, v in profile if v < avg_vol * 0.3)
    close = f(window[-1], "close")
    prev_close = f(window[-2], "close")
    rel_position = "inside"
    if abs(close - poc) <= (price_max - price_min) / 24.0:
        rel_position = "at_poc"
    elif close > vah:
        rel_position = "above"
    elif close < val:
        rel_position = "below"
    shape = classify_shape(profile, poc, price_min, price_max)
    volume_ratio = f(window[-1], "volume") / max(sum(f(r, "volume") for r in window[:-1]) / max(len(window) - 1, 1), 1e-6)

    signal_type = "NONE"
    signal_strength = 0
    suggested_stop = None
    suggested_target = None
    if rel_position == "above" and volume_ratio >= 1.1:
        signal_type = "VA_BREAKOUT"
        signal_strength = min(10, int(5 + volume_ratio * 2))
        suggested_stop = round(vah, 4)
        suggested_target = round(close + (close - vah), 4)
    elif rel_position == "at_poc" and close >= prev_close:
        signal_type = "POC_REVERSION"
        signal_strength = 6
        suggested_stop = round(val, 4)
        suggested_target = round(vah, 4)
    elif lvn and close >= max(lvn) and close > prev_close:
        signal_type = "LVN_MOMENTUM"
        signal_strength = 7
        suggested_stop = round(poc, 4)
        suggested_target = round(close + (close - poc), 4)
    elif hvn and val <= close <= vah:
        signal_type = "HVN_CONSOLIDATION"
        signal_strength = 3

    return {
        "object_id": "VP_P0_E",
        "input_rows": len(rows),
        "as_of_date": window[-1]["date"],
        "signal_payload": {
            "object_id": "VP_P0_E",
            "vp_poc": round(poc, 4),
            "vp_vah": round(vah, 4),
            "vp_val": round(val, 4),
            "vp_hvn_levels": hvn,
            "vp_lvn_levels": lvn,
            "vp_current_rel_position": rel_position,
            "vp_trend_shape": shape,
            "vp_signal_type": signal_type,
            "vp_signal_strength": signal_strength,
            "vp_suggested_stop": suggested_stop,
            "vp_suggested_target": suggested_target,
        },
        "acceptance_flags": {
            "passed_min_rows": True,
            "degraded": False,
            "degrade_reason": "",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal VP runner on daily OHLCV sample.")
    parser.add_argument("--input-csv", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    rows = load_rows(Path(args.input_csv))
    payload = calc_output(rows)
    output = Path(args.output_json)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
