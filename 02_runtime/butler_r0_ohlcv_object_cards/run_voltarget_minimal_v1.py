from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from statistics import mean, pstdev


REQUIRED_COLUMNS = {"date", "open", "high", "low", "close"}


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


def calc_atr14(rows: list[dict[str, str]]) -> float:
    if len(rows) < 15:
        return 0.0
    tr_values: list[float] = []
    prev_close = f(rows[0], "close")
    for row in rows[1:]:
        high = f(row, "high")
        low = f(row, "low")
        close = f(row, "close")
        tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        tr_values.append(tr)
        prev_close = close
    return mean(tr_values[-14:]) if len(tr_values) >= 14 else mean(tr_values)


def calc_output(rows: list[dict[str, str]], target_vol: float, base_position: float) -> dict[str, object]:
    closes = [f(r, "close") for r in rows]
    input_rows = len(rows)
    latest = rows[-1]

    if input_rows < 20:
        return {
            "object_id": "VOLTARGET_P0_R",
            "input_rows": input_rows,
            "as_of_date": latest["date"],
            "signal_payload": {
                "object_id": "VOLTARGET_P0_R",
                "vt_target_vol": target_vol,
                "vt_atr14": 0.0,
                "vt_current_price": closes[-1],
                "vt_log_return_std_20": 0.0,
                "vt_current_vol": 0.0,
                "vt_vol_ratio": 0.0,
                "vt_position_scalar": 1.0,
                "vt_scalar_ema": 1.0,
                "vt_adjusted_position": base_position,
                "vt_vol_regime": "normal_vol",
            },
            "acceptance_flags": {
                "passed_min_rows": False,
                "degraded": True,
                "degrade_reason": "insufficient_data_len_lt_20",
            },
        }

    log_returns = [math.log(closes[i] / closes[i - 1]) for i in range(1, len(closes)) if closes[i] > 0 and closes[i - 1] > 0]
    log_std_20 = pstdev(log_returns[-20:]) if len(log_returns) >= 20 else pstdev(log_returns) if len(log_returns) >= 2 else 0.0
    annualized_vol = log_std_20 * math.sqrt(252.0)
    atr14 = calc_atr14(rows)
    price = closes[-1]
    atr_vol = (atr14 / price) * math.sqrt(252.0) if price > 0 else 0.0
    current_vol = annualized_vol if annualized_vol > 0 else atr_vol
    vol_ratio = current_vol / target_vol if target_vol > 0 else 1.0
    position_scalar = 1.0 / vol_ratio if vol_ratio > 0 else 1.0
    position_scalar = max(0.2, min(2.0, position_scalar))
    scalar_ema = position_scalar
    adjusted_position = base_position * scalar_ema

    if current_vol >= target_vol * 2.0:
        vol_regime = "extreme_vol"
    elif current_vol >= target_vol * 1.3:
        vol_regime = "high_vol"
    elif current_vol <= target_vol * 0.7:
        vol_regime = "low_vol"
    else:
        vol_regime = "normal_vol"

    return {
        "object_id": "VOLTARGET_P0_R",
        "input_rows": input_rows,
        "as_of_date": latest["date"],
        "signal_payload": {
            "object_id": "VOLTARGET_P0_R",
            "vt_target_vol": round(target_vol, 6),
            "vt_atr14": round(atr14, 6),
            "vt_current_price": round(price, 6),
            "vt_log_return_std_20": round(log_std_20, 8),
            "vt_current_vol": round(current_vol, 6),
            "vt_vol_ratio": round(vol_ratio, 6),
            "vt_position_scalar": round(position_scalar, 6),
            "vt_scalar_ema": round(scalar_ema, 6),
            "vt_adjusted_position": round(adjusted_position, 6),
            "vt_vol_regime": vol_regime,
        },
        "acceptance_flags": {
            "passed_min_rows": True,
            "degraded": annualized_vol == 0.0,
            "degrade_reason": "" if annualized_vol > 0 else "fallback_to_atr_vol",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal VOLTARGET runner using daily OHLCV.")
    parser.add_argument("--input-csv", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--target-vol", type=float, default=0.10)
    parser.add_argument("--base-position", type=float, default=1.0)
    args = parser.parse_args()

    rows = load_rows(Path(args.input_csv))
    payload = calc_output(rows, target_vol=args.target_vol, base_position=args.base_position)
    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
