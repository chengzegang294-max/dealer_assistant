from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ANNOTATION_COLUMNS = {
    "symbol",
    "timeframe",
    "bar_date",
    "fractal_type",
    "bi_direction",
    "zs_state",
    "zs_zg",
    "zs_zd",
    "divergence_flag",
    "bsd_type",
    "stop_logic",
    "note",
}


def load_csv_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_annotation_rows(tsv_path: Path) -> list[dict[str, str]]:
    with tsv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)
    if not rows:
        raise ValueError(f"annotation has no rows: {tsv_path}")
    missing = ANNOTATION_COLUMNS - set(rows[0].keys())
    if missing:
        raise ValueError(f"annotation missing columns: {sorted(missing)}")
    return rows


def as_bool(value: str) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes"}


def map_signal_strength(bsd_type: str) -> int:
    return {
        "1B": 7,
        "2B": 8,
        "3B": 9,
        "1S": 6,
        "2S": 7,
        "3S": 8,
    }.get(bsd_type, 0)


def map_confidence(bsd_type: str) -> float:
    return {
        "1B": 0.68,
        "2B": 0.78,
        "3B": 0.84,
        "1S": 0.62,
        "2S": 0.72,
        "3S": 0.8,
    }.get(bsd_type, 0.0)


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal CHZL_BSD stub based on manual annotation seed.")
    parser.add_argument("--daily-csv", required=True)
    parser.add_argument("--weekly-csv", required=True)
    parser.add_argument("--annotation-tsv", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    daily_rows = load_csv_rows(Path(args.daily_csv))
    weekly_rows = load_csv_rows(Path(args.weekly_csv))
    annotations = load_annotation_rows(Path(args.annotation_tsv))

    daily_dates = {row["date"] for row in daily_rows}
    for row in annotations:
        if row["bar_date"] not in daily_dates:
            raise ValueError(f"annotation date not found in daily sample: {row['bar_date']}")

    signal_rows = [row for row in annotations if (row["bsd_type"] or "").strip() not in {"", "NONE"}]
    anchor = signal_rows[-1] if signal_rows else annotations[-1]
    bsd_type = (anchor["bsd_type"] or "NONE").strip()
    signal_strength = map_signal_strength(bsd_type)
    signal_confidence = map_confidence(bsd_type)
    filter_action = "OBSERVE" if bsd_type.endswith("S") else ("APPROVE" if bsd_type != "NONE" else "REJECT")
    risk_action = "HALF_SIZE" if bsd_type in {"1B", "2B"} else ("FULL_SIZE" if bsd_type == "3B" else "NO_TRADE")
    size_scalar = 0.5 if bsd_type in {"1B", "2B"} else (0.75 if bsd_type == "3B" else 0.0)

    payload = {
        "object_id": "CHZL_BSD_P0_E",
        "input_rows": {
            "daily": len(daily_rows),
            "weekly": len(weekly_rows),
            "annotation_rows": len(annotations),
        },
        "as_of_date": anchor["bar_date"],
        "evidence_mode": "weak_manual_seed",
        "signal_payload": {
            "object_id": "CHZL_BSD_P0_E",
            "chzl_fractal_type": anchor["fractal_type"] or "none",
            "chzl_bi_direction": anchor["bi_direction"] or "none",
            "chzl_zs_state": anchor["zs_state"] or "none",
            "chzl_zs_zg": float(anchor["zs_zg"]) if (anchor["zs_zg"] or "").strip() else None,
            "chzl_zs_zd": float(anchor["zs_zd"]) if (anchor["zs_zd"] or "").strip() else None,
            "chzl_divergence_flag": as_bool(anchor["divergence_flag"]),
            "chzl_bsd_type": bsd_type,
            "chzl_trigger_price": None,
            "chzl_stop_loss_price": None,
            "chzl_sl_logic": anchor["stop_logic"] or "",
            "chzl_is_trailing": False,
            "chzl_signal_strength": signal_strength,
            "chzl_signal_confidence": signal_confidence,
            "chzl_filter_action": filter_action,
            "chzl_risk_action": risk_action,
            "chzl_size_scalar": size_scalar,
            "chzl_limit_fractal_type": "normal",
            "chzl_suspend_merge_logic": False,
            "chzl_abort_reason": "" if bsd_type != "NONE" else "no_seed_signal",
        },
        "acceptance_flags": {
            "passed_annotation_binding": True,
            "degraded": True,
            "degrade_reason": "manual_annotation_seed_without_auto_chanlun_engine",
        },
        "note": anchor["note"],
    }

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
