from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


STRUCTURE_COLUMNS = {
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
    missing = STRUCTURE_COLUMNS - set(rows[0].keys())
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


def merge_rows(
    auto_rows: list[dict[str, str]],
    seed_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    merged = {row["bar_date"]: dict(row) for row in auto_rows}
    for row in seed_rows:
        base = dict(merged.get(row["bar_date"], {}))
        base.update({k: v for k, v in row.items() if v != ""})
        base.setdefault("source_mode", "manual_seed")
        base["source_mode"] = "seed_override"
        merged[row["bar_date"]] = base
    return sorted(merged.values(), key=lambda r: r["bar_date"])


def build_daily_price_map(daily_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["date"]: row for row in daily_rows}


def infer_stop_loss(
    row: dict[str, str],
    signal_rows: list[dict[str, str]],
    daily_price_map: dict[str, dict[str, str]],
) -> float | None:
    logic = (row.get("stop_logic") or "").strip()
    daily_row = daily_price_map.get(row["bar_date"])
    if not daily_row:
        return None
    if logic == "FRACTAL_BREAK":
        return float(daily_row["low"])
    if logic == "PREV_SWING":
        current_idx = signal_rows.index(row)
        if current_idx > 0:
            prev_signal = signal_rows[current_idx - 1]
            prev_daily = daily_price_map.get(prev_signal["bar_date"])
            if prev_daily:
                return float(prev_daily["low"])
        return float(daily_row["low"])
    if logic == "ZS_REENTRY" and (row.get("zs_zd") or "").strip():
        return float(row["zs_zd"])
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal CHZL_BSD stub based on auto structure series with seed override.")
    parser.add_argument("--daily-csv", required=True)
    parser.add_argument("--weekly-csv", required=True)
    parser.add_argument("--structure-series-tsv", required=True)
    parser.add_argument("--annotation-tsv")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    daily_rows = load_csv_rows(Path(args.daily_csv))
    weekly_rows = load_csv_rows(Path(args.weekly_csv))
    auto_rows = load_annotation_rows(Path(args.structure_series_tsv))
    annotations = load_annotation_rows(Path(args.annotation_tsv)) if args.annotation_tsv else []
    merged_rows = merge_rows(auto_rows, annotations)
    daily_price_map = build_daily_price_map(daily_rows)

    daily_dates = {row["date"] for row in daily_rows}
    for row in merged_rows:
        if row["bar_date"] not in daily_dates:
            raise ValueError(f"annotation date not found in daily sample: {row['bar_date']}")

    signal_rows = [row for row in merged_rows if (row["bsd_type"] or "").strip() not in {"", "NONE"}]
    anchor = signal_rows[-1] if signal_rows else merged_rows[-1]
    bsd_type = (anchor["bsd_type"] or "NONE").strip()
    signal_strength = map_signal_strength(bsd_type)
    signal_confidence = map_confidence(bsd_type)
    filter_action = "OBSERVE" if bsd_type.endswith("S") else ("APPROVE" if bsd_type != "NONE" else "REJECT")
    risk_action = "HALF_SIZE" if bsd_type in {"1B", "2B"} else ("FULL_SIZE" if bsd_type == "3B" else "NO_TRADE")
    size_scalar = 0.5 if bsd_type in {"1B", "2B"} else (0.75 if bsd_type == "3B" else 0.0)
    trigger_price = float(daily_price_map[anchor["bar_date"]]["close"]) if anchor["bar_date"] in daily_price_map else None
    stop_loss_price = infer_stop_loss(anchor, signal_rows, daily_price_map) if signal_rows else None
    evidence_mode = "semi_auto_structure_with_seed_override" if annotations else "semi_auto_structure_only"
    degrade_reason = (
        "semi_auto_structure_series_with_manual_seed_override"
        if annotations
        else "semi_auto_structure_series_without_manual_seed"
    )

    payload = {
        "object_id": "CHZL_BSD_P0_E",
        "input_rows": {
            "daily": len(daily_rows),
            "weekly": len(weekly_rows),
            "structure_series_rows": len(auto_rows),
            "annotation_rows": len(annotations),
            "merged_rows": len(merged_rows),
        },
        "as_of_date": anchor["bar_date"],
        "evidence_mode": evidence_mode,
        "anchor_source_mode": anchor.get("source_mode", "unknown"),
        "signal_payload": {
            "object_id": "CHZL_BSD_P0_E",
            "chzl_fractal_type": anchor["fractal_type"] or "none",
            "chzl_bi_direction": anchor["bi_direction"] or "none",
            "chzl_zs_state": anchor["zs_state"] or "none",
            "chzl_zs_zg": float(anchor["zs_zg"]) if (anchor["zs_zg"] or "").strip() else None,
            "chzl_zs_zd": float(anchor["zs_zd"]) if (anchor["zs_zd"] or "").strip() else None,
            "chzl_divergence_flag": as_bool(anchor["divergence_flag"]),
            "chzl_bsd_type": bsd_type,
            "chzl_trigger_price": trigger_price,
            "chzl_stop_loss_price": stop_loss_price,
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
            "passed_auto_structure_binding": True,
            "degraded": True,
            "degrade_reason": degrade_reason,
        },
        "note": anchor["note"],
    }

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
