from __future__ import annotations

import csv
import json
import os
from datetime import datetime
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parent
PARAMS_PATH = RUNTIME_DIR / "rsj_state_p0_runtime_params_template_v1.json"
ALLOWED_SOURCE_TIERS = {
    "proof_only",
    "synthetic_window",
    "archive_history",
    "repo_history_audited",
}


class ValidationError(RuntimeError):
    pass


def ensure_archive_only_run_allowed() -> None:
    if os.environ.get("ALLOW_ARCHIVE_ONLY_RUN") != "1":
        raise SystemExit(
            "ARCHIVE_ONLY: set ALLOW_ARCHIVE_ONLY_RUN=1 and use repo-first entry points under "
            "01_active_objects/ 02_runtime/ 04_active_main_docs/ before running this legacy validator."
        )


def load_params() -> dict:
    with PARAMS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_iso8601(value: str) -> None:
    normalized = value.replace("Z", "+00:00")
    datetime.fromisoformat(normalized)


def read_header(header_path: Path) -> list[str]:
    line = header_path.read_text(encoding="utf-8").strip()
    if not line:
        raise ValidationError("header file is empty")
    return line.split(",")


def read_rows(sample_csv: Path) -> list[dict[str, str]]:
    with sample_csv.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def to_positive_int(value: str, field_name: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValidationError(f"{field_name} must be int: {value}") from exc
    if parsed <= 0:
        raise ValidationError(f"{field_name} must be > 0: {value}")
    return parsed


def to_non_negative_float(value: str, field_name: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise ValidationError(f"{field_name} must be float: {value}") from exc
    if parsed < 0:
        raise ValidationError(f"{field_name} must be >= 0: {value}")
    return parsed


def validate_rows(rows: list[dict[str, str]], expected_header: list[str]) -> dict[str, object]:
    if not rows:
        raise ValidationError("sample csv has no data rows")

    trade_ids: set[str] = set()
    source_tiers: set[str] = set()

    for index, row in enumerate(rows, start=1):
        trade_id = row["trade_id"].strip()
        if not trade_id:
            raise ValidationError(f"row {index}: trade_id is empty")
        if trade_id in trade_ids:
            raise ValidationError(f"row {index}: duplicate trade_id: {trade_id}")
        trade_ids.add(trade_id)

        parse_iso8601(row["bar_time"].strip())
        to_positive_int(row["window_bars"].strip(), "window_bars")
        rv_up = to_non_negative_float(row["rv_up"].strip(), "rv_up")
        rv_down = to_non_negative_float(row["rv_down"].strip(), "rv_down")
        if (rv_up + rv_down) <= 0:
            raise ValidationError(f"row {index}: rv_up + rv_down must be > 0")

        source_tier = row["input_source_tier"].strip()
        if source_tier not in ALLOWED_SOURCE_TIERS:
            raise ValidationError(f"row {index}: invalid input_source_tier: {source_tier}")
        source_tiers.add(source_tier)

        for field_name in expected_header:
            if row[field_name] is None:
                raise ValidationError(f"row {index}: missing field value: {field_name}")

    return {
        "rows_loaded": len(rows),
        "trade_id_unique": True,
        "invalid_rows": 0,
        "input_source_tiers": sorted(source_tiers),
    }


def main() -> None:
    ensure_archive_only_run_allowed()
    params = load_params()
    runtime_dir = Path(params["runtime_dir"])
    header_path = runtime_dir / params["raw_window_input_header_file"]
    sample_csv = runtime_dir / params["raw_window_sample_input_csv"]
    expected_header = read_header(header_path)
    rows = read_rows(sample_csv)

    with sample_csv.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        actual_header = reader.fieldnames or []

    if actual_header != expected_header:
        raise ValidationError(
            "header mismatch: expected={0} actual={1}".format(expected_header, actual_header)
        )

    summary = validate_rows(rows, expected_header)

    print("validation_mode=archive_history_read_only")
    print("sample_csv_exists={0}".format(sample_csv.exists()))
    print("header_match=true")
    print("rows_loaded={0}".format(summary["rows_loaded"]))
    print("trade_id_unique={0}".format(summary["trade_id_unique"]))
    print("invalid_rows={0}".format(summary["invalid_rows"]))
    print(
        "input_source_tiers={0}".format(
            json.dumps(summary["input_source_tiers"], ensure_ascii=True)
        )
    )
    print("archive_only=true")
    print("path_policy=repo_first")
    print("write_attempted=false")
    print("validation_passed=true")


if __name__ == "__main__":
    main()
