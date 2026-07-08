from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from statistics import mean, pstdev


def load_ohlcv_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        raise ValueError("input csv has no rows")
    required = {"date", "open", "high", "low", "close", "volume"}
    missing = required - set(rows[0].keys())
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")
    return rows


def to_float_series(rows: list[dict[str, str]], key: str) -> list[float]:
    return [float(r[key]) for r in rows]


def percentile_rank(sorted_values: list[float], value: float) -> float:
    if not sorted_values:
        return 50.0
    below = sum(1 for v in sorted_values if v <= value)
    return round((below / len(sorted_values)) * 100.0, 2)


def calc_volfac(rows: list[dict[str, str]]) -> dict[str, object]:
    closes = to_float_series(rows, "close")
    input_rows = len(closes)
    if input_rows < 40:
        return {
            "object_id": "VOLFAC_P0_A",
            "signal_payload": {
                "object_id": "VOLFAC_P0_A",
                "volfac_vol_regime": "NORMAL",
                "volfac_vol_trend": "STABLE",
                "signal_type": "FILTER",
                "signal_strength": 0,
                "filter_action": "PASS",
                "risk_action": "NONE",
                "size_scalar": 1.0,
                "confidence": 0.2,
            },
            "acceptance_flags": {
                "passed_min_rows": False,
                "degraded": True,
                "degrade_reason": "insufficient_data_len_lt_40",
            },
        }

    log_returns = [math.log(closes[i] / closes[i - 1]) for i in range(1, len(closes)) if closes[i - 1] > 0 and closes[i] > 0]
    lookback = min(60, len(log_returns))
    current_std = pstdev(log_returns[-lookback:]) if lookback >= 2 else 0.0
    annualized = current_std * math.sqrt(252.0)

    history = []
    for end in range(lookback, len(log_returns) + 1):
        window = log_returns[end - lookback:end]
        if len(window) >= 2:
            history.append(pstdev(window))
    percentile = percentile_rank(sorted(history), current_std)

    if percentile >= 90:
        regime = "EXTREME"
        signal_strength = -2
        filter_action = "EXCLUDE"
        risk_action = "HALT_DAY_TRADE"
        size_scalar = 0.2
    elif percentile >= 70:
        regime = "HIGH"
        signal_strength = -1
        filter_action = "REDUCE_WEIGHT"
        risk_action = "REDUCE_POSITION"
        size_scalar = 0.6
    elif percentile <= 30:
        regime = "LOW"
        signal_strength = 1
        filter_action = "INCREASE_WEIGHT"
        risk_action = "NONE"
        size_scalar = 1.2
    else:
        regime = "NORMAL"
        signal_strength = 0
        filter_action = "PASS"
        risk_action = "NONE"
        size_scalar = 1.0

    recent_std = pstdev(log_returns[-20:]) if len(log_returns) >= 20 else current_std
    prev_std = pstdev(log_returns[-40:-20]) if len(log_returns) >= 40 else recent_std
    if recent_std > prev_std * 1.1:
        trend = "EXPANDING"
    elif recent_std < prev_std * 0.9:
        trend = "CONTRACTING"
    else:
        trend = "STABLE"

    confidence = 0.9 if input_rows >= 252 else 0.7

    return {
        "object_id": "VOLFAC_P0_A",
        "signal_payload": {
            "object_id": "VOLFAC_P0_A",
            "volfac_id2_std_3m": round(current_std, 8),
            "volfac_annualized_vol": round(annualized, 6),
            "volfac_vol_percentile": percentile,
            "volfac_vol_regime": regime,
            "volfac_vol_trend": trend,
            "signal_type": "FILTER",
            "signal_strength": signal_strength,
            "filter_action": filter_action,
            "risk_action": risk_action,
            "size_scalar": size_scalar,
            "confidence": confidence,
        },
        "acceptance_flags": {
            "passed_min_rows": input_rows >= 40,
            "degraded": input_rows < 252,
            "degrade_reason": "" if input_rows >= 252 else "used_shorter_history_for_percentile",
        },
    }


def calc_bpb(rows: list[dict[str, str]]) -> dict[str, object]:
    closes = to_float_series(rows, "close")
    highs = to_float_series(rows, "high")
    lows = to_float_series(rows, "low")
    opens = to_float_series(rows, "open")
    volumes = to_float_series(rows, "volume")
    input_rows = len(closes)

    if input_rows < 25:
        return {
            "object_id": "BPB_P0_E",
            "signal_payload": {
                "object_id": "BPB_P0_E",
                "bpb_trend_direction": "sideways",
                "bpb_breakout_level": None,
                "bpb_breakout_body_pct": 0.0,
                "bpb_breakout_volume_ratio": 0.0,
                "bpb_is_valid_breakout": False,
                "bpb_pullback_quality": "TOO_EARLY",
                "bpb_signal_type": "WAITING",
                "bpb_signal_strength": 0,
                "bpb_entry_price": None,
                "bpb_stop_loss_price": None,
                "bpb_target_price": None,
            },
            "acceptance_flags": {
                "passed_min_rows": False,
                "degraded": True,
                "degrade_reason": "insufficient_data_len_lt_25",
            },
        }

    sma20 = mean(closes[-20:])
    trend_direction = "up" if closes[-1] > sma20 else "down" if closes[-1] < sma20 else "sideways"
    breakout_level = max(highs[-21:-1])
    last_open = opens[-1]
    last_close = closes[-1]
    last_high = highs[-1]
    last_low = lows[-1]
    last_body = abs(last_close - last_open)
    last_range = max(last_high - last_low, 1e-9)
    breakout_body_pct = round(last_body / last_range, 6)
    vol_base = mean(volumes[-21:-1]) if len(volumes) >= 21 else mean(volumes[:-1])
    breakout_volume_ratio = round((volumes[-1] / vol_base), 6) if vol_base > 0 else 0.0
    is_valid_breakout = last_close > breakout_level and breakout_body_pct >= 0.3 and breakout_volume_ratio >= 1.0

    if is_valid_breakout:
        signal_type = "BPB"
        signal_strength = min(10, max(1, int(5 + breakout_body_pct * 5 + min(breakout_volume_ratio, 3))))
        pullback_depth_ratio = 0.0
        pullback_quality = "TOO_EARLY"
        entry_price = round(last_close, 4)
        stop_loss_price = round(min(lows[-5:]), 4)
        risk_per_share = max(entry_price - stop_loss_price, 1e-6)
        target_price = round(entry_price + 2.0 * risk_per_share, 4)
    else:
        recent_high = max(highs[-10:])
        recent_low = min(lows[-10:])
        width = max(recent_high - recent_low, 1e-9)
        pullback_depth_ratio = round((recent_high - closes[-1]) / width, 6)
        if pullback_depth_ratio <= 0.2:
            pullback_quality = "TOO_EARLY"
            signal_type = "WAITING"
        elif pullback_depth_ratio <= 0.5:
            pullback_quality = "GOOD"
            signal_type = "WAITING"
        elif pullback_depth_ratio <= 0.8:
            pullback_quality = "DEEP"
            signal_type = "TOO_DEEP"
        else:
            pullback_quality = "FAILED"
            signal_type = "BOF"
        signal_strength = 0 if signal_type == "WAITING" else 2
        entry_price = None
        stop_loss_price = None
        target_price = None

    return {
        "object_id": "BPB_P0_E",
        "signal_payload": {
            "object_id": "BPB_P0_E",
            "bpb_trend_direction": trend_direction,
            "bpb_breakout_level": round(breakout_level, 4),
            "bpb_breakout_body_pct": breakout_body_pct,
            "bpb_breakout_volume_ratio": breakout_volume_ratio,
            "bpb_is_valid_breakout": is_valid_breakout,
            "bpb_pullback_depth_ratio": pullback_depth_ratio,
            "bpb_pullback_quality": pullback_quality,
            "bpb_signal_type": signal_type,
            "bpb_signal_strength": signal_strength,
            "bpb_entry_price": entry_price,
            "bpb_stop_loss_price": stop_loss_price,
            "bpb_target_price": target_price,
        },
        "acceptance_flags": {
            "passed_min_rows": input_rows >= 25,
            "degraded": False,
            "degrade_reason": "",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run minimal object-card inference on a single OHLCV csv.")
    parser.add_argument("--object-card", required=True, choices=["VOLFAC_P0_A", "BPB_P0_E"])
    parser.add_argument("--input-csv", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    input_csv = Path(args.input_csv)
    output_json = Path(args.output_json)
    rows = load_ohlcv_rows(input_csv)

    if args.object_card == "VOLFAC_P0_A":
        result = calc_volfac(rows)
    else:
        result = calc_bpb(rows)

    result["input_rows"] = len(rows)
    result["as_of_date"] = rows[-1]["date"]
    result["input_csv"] = str(input_csv).replace("\\", "/")

    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
