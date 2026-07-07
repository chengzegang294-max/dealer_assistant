from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

RUNTIME_DIR = Path(__file__).resolve().parent
CSV_PATH = RUNTIME_DIR / "n02_ib_fields_runtime_v1.csv"
PROOF_PATH = RUNTIME_DIR / "real_input_samples" / "n02_ib_proof_of_mapping_output_v1.csv"

CSV_COLUMNS = [
    "symbol",
    "timeframe",
    "session_id",
    "session_timezone",
    "session_local_date",
    "ib_window_minutes",
    "ib_start_utc",
    "ib_end_utc",
    "ib_high",
    "ib_low",
    "ib_range",
    "ib_mid",
    "bars_in_ib_window",
    "ib_defined",
]


def assert_header(path: Path) -> None:
    with path.open("r", encoding="utf-8", newline="") as f:
        header = next(csv.reader(f))
    if header != CSV_COLUMNS:
        raise ValueError("header mismatch: {0}".format(path))


def read_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def row_key(row: dict) -> tuple[str, str, str, str, str]:
    return (
        row.get("symbol", ""),
        row.get("timeframe", ""),
        row.get("session_id", ""),
        row.get("session_local_date", ""),
        row.get("ib_window_minutes", ""),
    )


def dedupe_rows(rows: list[dict]) -> list[dict]:
    seen: dict[tuple[str, str, str, str, str], dict] = {}
    for row in rows:
        seen[row_key(row)] = row
    return [
        seen[k]
        for k in sorted(seen.keys(), key=lambda x: (x[3], x[2], x[4], x[0], x[1]))
    ]


def write_rows(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def print_coverage(rows: list[dict]) -> None:
    total = len(rows)
    defined = sum(1 for r in rows if r.get("ib_defined") == "1")
    undefined = total - defined
    print("ib_defined_rows={0}".format(defined))
    print("ib_undefined_rows={0}".format(undefined))
    print("ib_defined_ratio={0}".format(defined / total if total else 0.0))

    total_by_session: dict[str, int] = defaultdict(int)
    defined_by_session: dict[str, int] = defaultdict(int)
    total_by_session_weekday: dict[str, int] = defaultdict(int)
    defined_by_session_weekday: dict[str, int] = defaultdict(int)
    for r in rows:
        session_id = r.get("session_id", "")
        total_by_session[session_id] += 1
        if r.get("ib_defined") == "1":
            defined_by_session[session_id] += 1
        local_date = r.get("session_local_date", "")
        try:
            is_weekday = date.fromisoformat(local_date).weekday() < 5
        except ValueError:
            is_weekday = False
        if is_weekday:
            total_by_session_weekday[session_id] += 1
            if r.get("ib_defined") == "1":
                defined_by_session_weekday[session_id] += 1

    for session_id in sorted(total_by_session.keys()):
        t = total_by_session[session_id]
        d = defined_by_session.get(session_id, 0)
        print(
            "session_id={0} defined={1} total={2} ratio={3}".format(
                session_id, d, t, d / t if t else 0.0
            )
        )

    weekday_total = sum(total_by_session_weekday.values())
    weekday_defined = sum(defined_by_session_weekday.values())
    print("ib_weekday_defined_rows={0}".format(weekday_defined))
    print("ib_weekday_total_rows={0}".format(weekday_total))
    print(
        "ib_weekday_defined_ratio={0}".format(
            weekday_defined / weekday_total if weekday_total else 0.0
        )
    )
    for session_id in sorted(total_by_session_weekday.keys()):
        t = total_by_session_weekday[session_id]
        d = defined_by_session_weekday.get(session_id, 0)
        print(
            "session_id_weekday={0} defined={1} total={2} ratio={3}".format(
                session_id, d, t, d / t if t else 0.0
            )
        )


def build_coverage_report(rows: list[dict]) -> dict:
    total = len(rows)
    defined = sum(1 for r in rows if r.get("ib_defined") == "1")
    undefined = total - defined

    total_by_session: dict[str, int] = defaultdict(int)
    defined_by_session: dict[str, int] = defaultdict(int)
    total_by_session_weekday: dict[str, int] = defaultdict(int)
    defined_by_session_weekday: dict[str, int] = defaultdict(int)
    for r in rows:
        session_id = r.get("session_id", "")
        total_by_session[session_id] += 1
        if r.get("ib_defined") == "1":
            defined_by_session[session_id] += 1
        local_date = r.get("session_local_date", "")
        try:
            is_weekday = date.fromisoformat(local_date).weekday() < 5
        except ValueError:
            is_weekday = False
        if is_weekday:
            total_by_session_weekday[session_id] += 1
            if r.get("ib_defined") == "1":
                defined_by_session_weekday[session_id] += 1

    by_session = {}
    for session_id in sorted(total_by_session.keys()):
        t = total_by_session[session_id]
        d = defined_by_session.get(session_id, 0)
        by_session[session_id] = {
            "defined": d,
            "total": t,
            "ratio": d / t if t else 0.0,
        }

    by_session_weekday = {}
    for session_id in sorted(total_by_session_weekday.keys()):
        t = total_by_session_weekday[session_id]
        d = defined_by_session_weekday.get(session_id, 0)
        by_session_weekday[session_id] = {
            "defined": d,
            "total": t,
            "ratio": d / t if t else 0.0,
        }

    weekday_total = sum(total_by_session_weekday.values())
    weekday_defined = sum(defined_by_session_weekday.values())

    return {
        "total_rows": total,
        "defined_rows": defined,
        "undefined_rows": undefined,
        "defined_ratio": defined / total if total else 0.0,
        "by_session": by_session,
        "weekday_only": {
            "total_rows": weekday_total,
            "defined_rows": weekday_defined,
            "undefined_rows": weekday_total - weekday_defined,
            "defined_ratio": weekday_defined / weekday_total if weekday_total else 0.0,
            "by_session": by_session_weekday,
        },
    }


def maybe_write_report(path: str, report: dict) -> None:
    if not path:
        return
    report_path = Path(path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding="utf-8")




def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proof", default=str(PROOF_PATH))
    parser.add_argument("--dest", default=str(CSV_PATH))
    parser.add_argument("--persist", action="store_true")
    parser.add_argument("--report-json", default="")
    args = parser.parse_args()

    proof_path = Path(args.proof)
    dest_path = Path(args.dest)

    assert_header(proof_path)
    assert_header(dest_path)

    runtime_rows = read_rows(dest_path)
    proof_rows = read_rows(proof_path)
    merged_rows = dedupe_rows(runtime_rows + proof_rows)

    print("mode={0}".format("persist" if args.persist else "dry_run"))
    print("proof_path={0}".format(proof_path))
    print("dest_path={0}".format(dest_path))
    print("runtime_rows_before={0}".format(len(runtime_rows)))
    print("proof_rows={0}".format(len(proof_rows)))
    print("runtime_rows_after_append={0}".format(len(merged_rows)))
    print_coverage(merged_rows)
    report = build_coverage_report(merged_rows)
    maybe_write_report(args.report_json, report)
    if merged_rows:
        print("first_runtime_row={0}".format(json.dumps(merged_rows[0], ensure_ascii=True)))
        print("last_runtime_row={0}".format(json.dumps(merged_rows[-1], ensure_ascii=True)))

    if args.persist:
        write_rows(dest_path, merged_rows)
        print("persisted_to={0}".format(dest_path))
    else:
        print("dry_run_only=true")


if __name__ == "__main__":
    main()
