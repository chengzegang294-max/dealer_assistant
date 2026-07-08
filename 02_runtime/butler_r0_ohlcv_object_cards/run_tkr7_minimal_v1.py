from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REQUIRED_COLUMNS = {"date", "high", "low", "close"}


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


def rolling_mean(values: list[float], window: int) -> list[float | None]:
    out: list[float | None] = []
    for i in range(len(values)):
        if i + 1 < window:
            out.append(None)
        else:
            sub = values[i + 1 - window : i + 1]
            out.append(sum(sub) / window)
    return out


def local_extrema(values: list[float], kind: str, radius: int = 3) -> list[dict[str, float | int]]:
    out: list[dict[str, float | int]] = []
    for i in range(radius, len(values) - radius):
        current = values[i]
        left = values[i - radius : i]
        right = values[i + 1 : i + 1 + radius]
        if kind == "high":
            if all(current >= v for v in left + right):
                out.append({"index": i, "value": current})
        else:
            if all(current <= v for v in left + right):
                out.append({"index": i, "value": current})
    return out


def calc_output(rows: list[dict[str, str]]) -> dict[str, object]:
    if len(rows) < 34:
        return {
            "object_id": "TKR7_P0_E",
            "input_rows": len(rows),
            "as_of_date": rows[-1]["date"],
            "signal_payload": {
                "object_id": "TKR7_P0_E",
                "ao_value": 0.0,
                "ao_direction": "unknown",
                "ao_divergence_type": "NONE",
                "ao_divergence_strength": 0.0,
                "ao_divergence_confidence": 0.0,
                "ao_divergence_age": 0,
                "ao_signal_type": "NONE",
                "ao_signal_strength": 0,
                "ao_recommendation": "STANDBY",
            },
            "acceptance_flags": {
                "passed_min_rows": False,
                "degraded": True,
                "degrade_reason": "insufficient_data_len_lt_34",
            },
        }

    median = [(f(r, "high") + f(r, "low")) / 2.0 for r in rows]
    sma5 = rolling_mean(median, 5)
    sma34 = rolling_mean(median, 34)
    ao: list[float] = []
    for a, b in zip(sma5, sma34):
        ao.append((a - b) if a is not None and b is not None else 0.0)
    ao_value = ao[-1]
    ao_prev = ao[-2]
    if ao_prev <= 0 < ao_value:
        ao_direction = "crossing_up"
    elif ao_prev >= 0 > ao_value:
        ao_direction = "crossing_down"
    elif ao_value > 0:
        ao_direction = "positive"
    else:
        ao_direction = "negative"

    highs = [f(r, "high") for r in rows]
    lows = [f(r, "low") for r in rows]
    price_highs = local_extrema(highs, "high")
    price_lows = local_extrema(lows, "low")
    ao_highs = local_extrema(ao, "high")
    ao_lows = local_extrema(ao, "low")

    divergence_type = "NONE"
    strength = 0.0
    confidence = 0.0
    age = 0
    signal_type = "NONE"
    signal_strength = 0
    recommendation = "STANDBY"

    if len(price_lows) >= 2 and len(ao_lows) >= 2:
        p1, p2 = price_lows[-2], price_lows[-1]
        a1, a2 = ao_lows[-2], ao_lows[-1]
        if float(p2["value"]) < float(p1["value"]) and float(a2["value"]) > float(a1["value"]):
            divergence_type = "REGULAR_BULL"
            strength = min(1.0, abs(float(a2["value"]) - float(a1["value"])) / max(abs(float(a1["value"])), 0.001))
            confidence = 0.75
            age = len(rows) - 1 - int(p2["index"])
            signal_type = "CONFIRM"
            signal_strength = min(10, int(4 + strength * 6))
            recommendation = "HOLD"
        elif float(p2["value"]) > float(p1["value"]) and float(a2["value"]) < float(a1["value"]):
            divergence_type = "HIDDEN_BULL"
            strength = 0.5
            confidence = 0.62
            age = len(rows) - 1 - int(p2["index"])
            signal_type = "CONFIRM"
            signal_strength = 5
            recommendation = "HOLD"

    if divergence_type == "NONE" and len(price_highs) >= 2 and len(ao_highs) >= 2:
        p1, p2 = price_highs[-2], price_highs[-1]
        a1, a2 = ao_highs[-2], ao_highs[-1]
        if float(p2["value"]) > float(p1["value"]) and float(a2["value"]) < float(a1["value"]):
            divergence_type = "REGULAR_BEAR"
            strength = min(1.0, abs(float(a1["value"]) - float(a2["value"])) / max(abs(float(a1["value"])), 0.001))
            confidence = 0.78
            age = len(rows) - 1 - int(p2["index"])
            signal_type = "FORCE_EXIT"
            signal_strength = min(10, int(5 + strength * 5))
            recommendation = "CLOSE"
        elif float(p2["value"]) < float(p1["value"]) and float(a2["value"]) > float(a1["value"]):
            divergence_type = "HIDDEN_BEAR"
            strength = 0.45
            confidence = 0.6
            age = len(rows) - 1 - int(p2["index"])
            signal_type = "FORCE_EXIT"
            signal_strength = 5
            recommendation = "REDUCE"

    return {
        "object_id": "TKR7_P0_E",
        "input_rows": len(rows),
        "as_of_date": rows[-1]["date"],
        "signal_payload": {
            "object_id": "TKR7_P0_E",
            "ao_value": round(ao_value, 6),
            "ao_direction": ao_direction,
            "ao_divergence_type": divergence_type,
            "ao_divergence_strength": round(strength, 6),
            "ao_divergence_confidence": round(confidence, 6),
            "ao_divergence_age": age,
            "ao_signal_type": signal_type,
            "ao_signal_strength": signal_strength,
            "ao_recommendation": recommendation,
        },
        "acceptance_flags": {
            "passed_min_rows": True,
            "degraded": divergence_type == "NONE",
            "degrade_reason": "" if divergence_type != "NONE" else "no_recent_divergence_detected",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal TKR7 AO divergence runner.")
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
