from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


TOP_LEVEL_REQUIRED_FIELDS = [
    "registry_id",
    "input_csv",
    "market_proxy_csv",
    "as_of_date",
    "cards_run",
    "vote_input_snapshot",
    "aggregate_summary",
    "final_decision_card",
    "size_policy_card",
]

VOTE_SNAPSHOT_REQUIRED_FIELDS = [
    "object_id",
    "card_role",
    "signal_type",
    "signal_direction",
    "signal_strength",
    "confidence",
    "filter_action",
    "risk_action",
    "size_scalar",
]


def read_plan_row(path: Path, registry_id: str) -> dict[str, str]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            if row.get("registry_id") == registry_id:
                return row
    raise ValueError(f"registry_id not found in sample plan: {registry_id}")


def read_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("acceptance output must be a json object")
    return payload


def normalize_blockers(value: object) -> str:
    if isinstance(value, list):
        return "|".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def pipe_split(value: str) -> list[str]:
    return [item for item in value.split("|") if item]


def missing_fields(payload: dict[str, object], required_fields: list[str]) -> list[str]:
    return [field for field in required_fields if field not in payload]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate registry_v0 output against minimal acceptance expectations.")
    parser.add_argument("--sample-plan", required=True)
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    output_payload = read_json(Path(args.input_json))
    registry_id = str(output_payload.get("registry_id", ""))
    if not registry_id:
        raise ValueError("registry_id missing in input json")
    plan_row = read_plan_row(Path(args.sample_plan), registry_id)

    vote_snapshot = output_payload.get("vote_input_snapshot", [])
    final_card = output_payload.get("final_decision_card", {})
    size_card = output_payload.get("size_policy_card", {})
    summary = output_payload.get("aggregate_summary", {})
    cards_run = output_payload.get("cards_run", [])
    if (
        not isinstance(vote_snapshot, list)
        or not isinstance(final_card, dict)
        or not isinstance(size_card, dict)
        or not isinstance(summary, dict)
        or not isinstance(cards_run, list)
    ):
        raise ValueError("registry output missing expected card objects")

    top_level_missing = missing_fields(output_payload, TOP_LEVEL_REQUIRED_FIELDS)
    snapshot_missing_by_object: dict[str, list[str]] = {}
    for idx, item in enumerate(vote_snapshot):
        if not isinstance(item, dict):
            snapshot_missing_by_object[f"index_{idx}"] = VOTE_SNAPSHOT_REQUIRED_FIELDS.copy()
            continue
        object_id = str(item.get("object_id", f"index_{idx}"))
        snapshot_missing_by_object[object_id] = missing_fields(item, VOTE_SNAPSHOT_REQUIRED_FIELDS)
    snapshot_missing_compact = {key: value for key, value in snapshot_missing_by_object.items() if value}

    expected_cards_run = pipe_split(plan_row["expected_cards_run"])
    actual_cards_run = [str(item) for item in cards_run]
    snapshot_object_ids = [
        str(item.get("object_id", f"index_{idx}")) if isinstance(item, dict) else f"index_{idx}"
        for idx, item in enumerate(vote_snapshot)
    ]

    checks = [
        {
            "field": "top_level_required_fields",
            "expected": "present",
            "actual": "|".join(top_level_missing) if top_level_missing else "present",
        },
        {
            "field": "cards_run",
            "expected": "|".join(expected_cards_run),
            "actual": "|".join(actual_cards_run),
        },
        {
            "field": "vote_snapshot_count",
            "expected": plan_row["expected_vote_snapshot_count"],
            "actual": str(len(vote_snapshot)),
        },
        {
            "field": "vote_snapshot_objects_match_cards_run",
            "expected": "|".join(expected_cards_run),
            "actual": "|".join(snapshot_object_ids),
        },
        {
            "field": "vote_snapshot_required_fields",
            "expected": "present",
            "actual": json.dumps(snapshot_missing_compact, ensure_ascii=False, sort_keys=True) if snapshot_missing_compact else "present",
        },
        {
            "field": "buy_votes",
            "expected": plan_row["expected_buy_votes"],
            "actual": str(summary.get("buy_votes", "")),
        },
        {
            "field": "sell_votes",
            "expected": plan_row["expected_sell_votes"],
            "actual": str(summary.get("sell_votes", "")),
        },
        {
            "field": "neutral_votes",
            "expected": plan_row["expected_neutral_votes"],
            "actual": str(summary.get("neutral_votes", "")),
        },
        {
            "field": "final_signal",
            "expected": plan_row["expected_final_signal"],
            "actual": str(final_card.get("final_signal", "")),
        },
        {
            "field": "trade_gate",
            "expected": plan_row["expected_trade_gate"],
            "actual": str(final_card.get("trade_gate", "")),
        },
        {
            "field": "blockers",
            "expected": plan_row["expected_blockers"],
            "actual": normalize_blockers(final_card.get("blockers", [])),
        },
        {
            "field": "permission",
            "expected": plan_row["expected_permission"],
            "actual": str(final_card.get("permission", "")),
        },
        {
            "field": "hard_block",
            "expected": plan_row["expected_hard_block"].lower(),
            "actual": str(final_card.get("hard_block", "")).lower(),
        },
        {
            "field": "size_policy",
            "expected": plan_row["expected_size_policy"],
            "actual": str(size_card.get("size_policy", "")),
        },
        {
            "field": "recommended_size_scalar",
            "expected": "0.0" if plan_row["expected_size_policy"] == "blocked_to_zero" else "nonzero",
            "actual": str(size_card.get("recommended_size_scalar", "")),
        },
        {
            "field": "summary_final_signal_matches_final_card",
            "expected": str(summary.get("final_signal", "")),
            "actual": str(final_card.get("final_signal", "")),
        },
        {
            "field": "summary_blockers_match_final_card",
            "expected": normalize_blockers(summary.get("blockers", [])),
            "actual": normalize_blockers(final_card.get("blockers", [])),
        },
    ]

    failed = []
    for check in checks:
        if check["field"] == "recommended_size_scalar":
            passed = float(check["actual"]) == 0.0 if check["expected"] == "0.0" else float(check["actual"]) > 0.0
        elif check["field"] in {"top_level_required_fields", "vote_snapshot_required_fields"}:
            passed = check["actual"] == "present"
        else:
            passed = check["expected"] == check["actual"]
        check["passed"] = passed
        if not passed:
            failed.append(check["field"])

    result = {
        "registry_id": registry_id,
        "input_json": str(Path(args.input_json)).replace("\\", "/"),
        "sample_plan": str(Path(args.sample_plan)).replace("\\", "/"),
        "as_of_date": output_payload.get("as_of_date", ""),
        "summary_snapshot": {
            "cards_run": cards_run,
            "vote_snapshot_count": len(vote_snapshot),
            "vote_snapshot_object_ids": snapshot_object_ids,
            "final_signal": final_card.get("final_signal", ""),
            "trade_gate": final_card.get("trade_gate", ""),
            "permission": final_card.get("permission", ""),
            "blockers": final_card.get("blockers", []),
            "hard_block": final_card.get("hard_block", False),
            "size_policy": size_card.get("size_policy", ""),
            "recommended_size_scalar": size_card.get("recommended_size_scalar", None),
            "aggregate_final_signal": summary.get("final_signal", ""),
        },
        "checks": checks,
        "acceptance_status": "pass" if not failed else "fail",
        "failed_fields": failed,
    }

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
