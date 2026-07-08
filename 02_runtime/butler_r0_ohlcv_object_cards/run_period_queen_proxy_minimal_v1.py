from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from statistics import mean, pstdev


REQUIRED_COLUMNS = {"date", "open", "high", "low", "close", "symbol"}


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


def safe_return(a: float, b: float) -> float:
    return (a / b - 1.0) if b > 0 else 0.0


def classify_state(rows: list[dict[str, str]]) -> tuple[str, dict[str, object]]:
    closes = [f(r, "close") for r in rows]
    highs = [f(r, "high") for r in rows]
    input_rows = len(rows)
    last_close = closes[-1]
    ret_5 = safe_return(last_close, closes[-6]) if input_rows >= 6 else 0.0
    ret_20 = safe_return(last_close, closes[-21]) if input_rows >= 21 else 0.0
    ret_60 = safe_return(last_close, closes[-61]) if input_rows >= 61 else 0.0
    recent_high_20 = max(highs[-20:]) if input_rows >= 20 else max(highs)
    new_high = last_close >= recent_high_20 * 0.995
    pct_changes = [safe_return(closes[i], closes[i - 1]) for i in range(1, len(closes))]
    pos_10 = sum(1 for v in pct_changes[-10:] if v > 0)
    up_limit_proxy = sum(1 for v in pct_changes[-10:] if v >= 0.095)
    down_limit_proxy = sum(1 for v in pct_changes[-10:] if v <= -0.095)
    vol20 = pstdev([math.log(closes[i] / closes[i - 1]) for i in range(1, len(closes)) if closes[i] > 0 and closes[i - 1] > 0][-20:]) if len(closes) >= 21 else 0.0

    if ret_20 > 0.18 and pos_10 >= 7 and new_high:
        state = "ATTACK_SUSTAINED"
    elif ret_20 > 0.08 and pos_10 >= 6:
        state = "ATTACK_CONFIRMED"
    elif ret_5 > 0.02 and ret_20 > 0:
        state = "POWER_TRANSITION"
    elif ret_20 > 0 and ret_5 < 0:
        state = "REMAINING_WARMTH"
    elif ret_20 < -0.12 and down_limit_proxy >= 1:
        state = "CUTTING_COMPLETE"
    elif ret_20 < -0.05:
        state = "ATTACK_UNSUSTAINED"
    else:
        state = "GESTATION"

    features = {
        "ret_5": ret_5,
        "ret_20": ret_20,
        "ret_60": ret_60,
        "new_high": new_high,
        "positive_days_10": pos_10,
        "up_limit_proxy": up_limit_proxy,
        "down_limit_proxy": down_limit_proxy,
        "vol20": vol20,
    }
    return state, features


def state_mapping(state: str) -> tuple[str, float, int, str, str, float]:
    mapping = {
        "ATTACK_SUSTAINED": ("FULL", 1.0, 3, "PASS", "NONE", 0.85),
        "ATTACK_CONFIRMED": ("FULL", 0.7, 3, "PASS", "NONE", 0.75),
        "POWER_TRANSITION": ("REDUCED", 0.3, 4, "REDUCE_WEIGHT", "REDUCE_POSITION", 0.6),
        "REMAINING_WARMTH": ("EXIT_ONLY", 0.0, 2, "REDUCE_WEIGHT", "REDUCE_POSITION", 0.55),
        "ATTACK_UNSUSTAINED": ("HALT", 0.0, 5, "EXCLUDE", "HALT_NEW_POSITION", 0.45),
        "CUTTING_COMPLETE": ("HALT", 0.0, 99, "EXCLUDE", "HALT_NEW_POSITION", 0.4),
        "GESTATION": ("REDUCED", 0.3, 4, "REDUCE_WEIGHT", "NONE", 0.5),
    }
    return mapping[state]


def calc_output(rows: list[dict[str, str]]) -> dict[str, object]:
    latest = rows[-1]
    input_rows = len(rows)
    if input_rows < 60:
        return {
            "object_id": "PERIOD_QUEEN_P0_F",
            "input_rows": input_rows,
            "as_of_date": latest["date"],
            "signal_payload": {
                "object_id": "PERIOD_QUEEN_P0_F",
                "pq_state": "GESTATION",
                "pq_trading_permission": "HALT",
                "pq_position_max_size": 0.0,
                "pq_entry_min_votes_adjusted": 99,
                "pq_allowed_objects": [],
                "pq_forbidden_objects": ["ALL"],
            },
            "acceptance_flags": {
                "passed_min_rows": False,
                "degraded": True,
                "degrade_reason": "insufficient_data_len_lt_60",
            },
        }

    state, features = classify_state(rows)
    permission, max_size, min_votes, filter_action, risk_action, confidence = state_mapping(state)
    symbol = latest["symbol"]
    recent_closes = [f(r, "close") for r in rows[-10:]]
    leading_stock_new_high = features["new_high"]
    allowed_objects_map = {
        "ATTACK_SUSTAINED": ["CHZL_BSD", "BPB", "VP", "TKR7", "VOLFAC", "VOLTARGET"],
        "ATTACK_CONFIRMED": ["CHZL_BSD", "BPB", "VP", "TKR7", "VOLFAC", "VOLTARGET"],
        "POWER_TRANSITION": ["YTC", "BPB", "VOLFAC", "VOLTARGET"],
        "REMAINING_WARMTH": ["TKR7", "CHZL_BSD", "VOLFAC"],
        "ATTACK_UNSUSTAINED": [],
        "CUTTING_COMPLETE": [],
        "GESTATION": ["CHZL_BSD", "YTC", "BPB", "VOLFAC"],
    }
    allowed = allowed_objects_map[state]
    all_objects = ["CHZL_BSD", "BPB", "VP", "TKR7", "YTC", "MFLOW", "INSTB", "VOLFAC", "VOLTARGET", "KELLY", "PERIOD_QUEEN", "ATRATIO"]
    forbidden = [obj for obj in all_objects if obj not in allowed]
    tide_force_score = min(1.0, abs(features["ret_20"]) * 3.0) if features["ret_20"] < 0 else 0.0
    tolerance_score = min(1.0, max(0.0, features["ret_5"] + 0.2))
    attack_formation_count = sum(1 for c in recent_closes if c >= mean(recent_closes))

    return {
        "object_id": "PERIOD_QUEEN_P0_F",
        "input_rows": input_rows,
        "as_of_date": latest["date"],
        "evidence_mode": "proxy_single_symbol_market_regime",
        "signal_payload": {
            "object_id": "PERIOD_QUEEN_P0_F",
            "pq_state": state,
            "pq_state_prev": "",
            "pq_state_duration": 1,
            "pq_state_confidence": confidence,
            "pq_transition_trigger": f"ret20={features['ret_20']:.4f}|ret5={features['ret_5']:.4f}|new_high={features['new_high']}",
            "pq_leading_stock": symbol,
            "pq_leading_stock_sustained": features["positive_days_10"] >= 6,
            "pq_leading_stock_new_high": leading_stock_new_high,
            "pq_space_board_sustained": features["up_limit_proxy"] >= 2,
            "pq_space_board_count": features["up_limit_proxy"],
            "pq_attack_formation_count": attack_formation_count,
            "pq_attack_formation_valid": attack_formation_count >= 6,
            "pq_tolerance_exist": tolerance_score >= 0.4,
            "pq_tolerance_score": round(tolerance_score, 6),
            "pq_tide_force_exist": tide_force_score >= 0.4,
            "pq_tide_force_score": round(tide_force_score, 6),
            "pq_ten_day_rank": [symbol],
            "pq_ten_day_rank_change": 0,
            "pq_cutting_condition_met": state in {"ATTACK_UNSUSTAINED", "CUTTING_COMPLETE"},
            "pq_gestation_new_faces": 1 if state == "GESTATION" else 0,
            "pq_gestation_new_faces_sustained": False,
            "pq_trading_permission": permission,
            "pq_position_max_size": max_size,
            "pq_strategy_bundle": state.lower(),
            "pq_allowed_objects": allowed,
            "pq_forbidden_objects": forbidden,
            "pq_entry_min_votes_adjusted": min_votes,
        },
        "acceptance_flags": {
            "passed_min_rows": True,
            "degraded": True,
            "degrade_reason": "single_symbol_proxy_instead_of_market_breadth_rank_board_inputs",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal PERIOD_QUEEN proxy runner using a single daily sample.")
    parser.add_argument("--input-csv", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    rows = load_rows(Path(args.input_csv))
    payload = calc_output(rows)
    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
