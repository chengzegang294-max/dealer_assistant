from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from statistics import mean


REQUIRED_COLUMNS = {"date", "open", "high", "low", "close", "volume"}


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        raise ValueError(f"input csv has no rows: {csv_path}")
    missing = REQUIRED_COLUMNS - set(rows[0].keys())
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")
    return rows


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


def build_output(
    daily_rows: list[dict[str, str]],
    weekly_rows: list[dict[str, str]],
) -> dict[str, object]:
    daily_len = len(daily_rows)
    weekly_len = len(weekly_rows)
    latest = daily_rows[-1]

    if daily_len < 20 or weekly_len < 8:
        return {
            "object_id": "YTC_P0_E",
            "input_rows": {"daily": daily_len, "weekly": weekly_len},
            "as_of_date": latest["date"],
            "signal_payload": {
                "object_id": "YTC_P0_E",
                "ytc_srf_tf_level": None,
                "ytc_srf_htf_level": None,
                "ytc_srf_zone_width": 0.0,
                "ytc_srf_is_valid": False,
                "ytc_srf_type": "none",
                "ytc_signal_type": "NONE",
                "ytc_signal_subtype": "NONE",
                "ytc_direction": "NONE",
                "ytc_signal_strength": 0,
                "ytc_signal_confidence": 0.0,
                "ytc_filter_action": "WAIT",
                "ytc_risk_action": "NONE",
                "ytc_size_scalar": 0.0,
                "ytc_astock_period_limit": "daily_weekly",
                "ytc_abort_reason": "insufficient_daily_or_weekly_rows",
            },
            "acceptance_flags": {
                "passed_min_rows": False,
                "degraded": True,
                "degrade_reason": "insufficient_daily_or_weekly_rows",
            },
        }

    recent_weekly = weekly_rows[-8:]
    htf_resistance = max(f(r, "high") for r in recent_weekly)
    htf_support = min(f(r, "low") for r in recent_weekly)
    avg_weekly_range = mean(f(r, "high") - f(r, "low") for r in recent_weekly)
    zone_width = max(avg_weekly_range * 0.25, 1e-6)

    last_open = f(latest, "open")
    last_high = f(latest, "high")
    last_low = f(latest, "low")
    last_close = f(latest, "close")
    prev_close = f(daily_rows[-2], "close")

    signal_type = "NONE"
    signal_subtype = "NONE"
    direction = "NONE"
    strength = 0
    confidence = 0.45
    filter_action = "WAIT"
    risk_action = "NONE"
    size_scalar = 0.0
    sr_type = "none"
    tf_level = None
    abort_reason = ""

    near_support = abs(last_low - htf_support) <= zone_width
    broke_above_resistance = last_high > htf_resistance
    failed_above_resistance = broke_above_resistance and last_close < htf_resistance
    bp_long = prev_close > htf_resistance and last_low <= (htf_resistance + zone_width) and last_close >= htf_resistance

    if failed_above_resistance:
        signal_type = "P"
        signal_subtype = "BOF_WEAK"
        direction = "SHORT"
        strength = -1
        confidence = 0.55
        filter_action = "WAIT"
        sr_type = "RESISTANCE"
        tf_level = round(htf_resistance, 4)
        abort_reason = "astock_long_only_short_side_degraded_to_pause"
    elif bp_long:
        signal_type = "BP"
        signal_subtype = "BP_SHALLOW"
        direction = "LONG"
        strength = 1
        confidence = 0.62
        filter_action = "PASS"
        risk_action = "TIGHTEN_STOP"
        size_scalar = 0.5
        sr_type = "RESISTANCE"
        tf_level = round(htf_resistance, 4)
    elif near_support and last_close > last_open:
        signal_type = "TST"
        signal_subtype = "TST_SWING_LOW"
        direction = "LONG"
        strength = 1
        confidence = 0.58
        filter_action = "PASS"
        risk_action = "TIGHTEN_STOP"
        size_scalar = 0.4
        sr_type = "SUPPORT"
        tf_level = round(htf_support, 4)
    else:
        abort_reason = "no_daily_weekly_event_detected"

    return {
        "object_id": "YTC_P0_E",
        "input_rows": {"daily": daily_len, "weekly": weekly_len},
        "as_of_date": latest["date"],
        "signal_payload": {
            "object_id": "YTC_P0_E",
            "ytc_srf_tf_level": tf_level,
            "ytc_srf_htf_level": round(htf_resistance if sr_type == "RESISTANCE" else htf_support, 4) if sr_type != "none" else None,
            "ytc_srf_zone_width": round(zone_width, 6),
            "ytc_srf_is_valid": True,
            "ytc_srf_type": sr_type,
            "ytc_signal_type": signal_type,
            "ytc_signal_subtype": signal_subtype,
            "ytc_direction": direction,
            "ytc_signal_strength": strength,
            "ytc_signal_confidence": confidence,
            "ytc_filter_action": filter_action,
            "ytc_risk_action": risk_action,
            "ytc_size_scalar": size_scalar,
            "ytc_astock_period_limit": "daily_weekly",
            "ytc_abort_reason": abort_reason,
        },
        "acceptance_flags": {
            "passed_min_rows": True,
            "degraded": True,
            "degrade_reason": "daily_weekly_only_without_intraday_60m_5m",
        },
    }


def write_json(output_json: Path, payload: dict[str, object]) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal YTC daily+weekly degraded runner.")
    parser.add_argument("--daily-csv", required=True)
    parser.add_argument("--weekly-csv", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    daily_rows = load_rows(Path(args.daily_csv))
    weekly_rows = load_rows(Path(args.weekly_csv))
    payload = build_output(daily_rows, weekly_rows)
    write_json(Path(args.output_json), payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
