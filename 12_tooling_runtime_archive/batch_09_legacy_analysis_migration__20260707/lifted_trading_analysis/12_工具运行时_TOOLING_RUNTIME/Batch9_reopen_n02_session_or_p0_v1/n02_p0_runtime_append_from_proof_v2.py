from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parent
CSV_PATH = RUNTIME_DIR / "n02_p0_fields_runtime_v2.csv"
PROOF_PATH = RUNTIME_DIR / "real_input_samples" / "n02_proof_of_mapping_output_v2.csv"

CSV_COLUMNS = [
    "symbol",
    "timeframe",
    "bar_time",
    "session_id",
    "session_timezone",
    "opening_range_window_minutes",
    "opening_range_high",
    "opening_range_low",
    "opening_range_mid",
    "opening_range_width",
    "opening_range_width_pct_open",
    "session_open_price",
    "opening_range_defined",
    "first_break_direction",
    "first_break_mode",
    "width_error_day",
]


def parse_iso_utc(value: str) -> str:
    return str(value).strip()


def assert_header(path: Path) -> None:
    with path.open("r", encoding="utf-8", newline="") as f:
        header = next(csv.reader(f))
    if header != CSV_COLUMNS:
        raise ValueError("header mismatch: {0}".format(path))


def read_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def row_key(row: dict) -> tuple[str, str, str, str]:
    return (
        row.get("symbol", ""),
        row.get("timeframe", ""),
        row.get("bar_time", ""),
        row.get("session_id", ""),
    )


def dedupe_rows(rows: list[dict]) -> list[dict]:
    seen: dict[tuple[str, str, str, str], dict] = {}
    for row in rows:
        seen[row_key(row)] = row
    return [seen[k] for k in sorted(seen.keys(), key=lambda x: (x[2], x[3]))]


def write_rows(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def print_coverage(rows: list[dict]) -> None:
    total = len(rows)
    defined = sum(1 for r in rows if r.get("opening_range_defined") == "1")
    undefined = total - defined
    print("or_defined_rows={0}".format(defined))
    print("or_undefined_rows={0}".format(undefined))
    print("or_defined_ratio={0}".format(defined / total if total else 0.0))

    total_by_session: dict[str, int] = defaultdict(int)
    defined_by_session: dict[str, int] = defaultdict(int)
    width_error_by_session: dict[str, int] = defaultdict(int)
    for r in rows:
        sid = r.get("session_id", "")
        total_by_session[sid] += 1
        if r.get("opening_range_defined") == "1":
            defined_by_session[sid] += 1
        if r.get("width_error_day") == "1":
            width_error_by_session[sid] += 1

    for sid in sorted(total_by_session.keys()):
        t = total_by_session[sid]
        d = defined_by_session.get(sid, 0)
        w = width_error_by_session.get(sid, 0)
        print("session_id={0} or_defined={1} total={2} ratio={3}".format(sid, d, t, d / t if t else 0.0))
        print("session_id={0} width_error_day={1} total={2} ratio={3}".format(sid, w, t, w / t if t else 0.0))

    first_break_direction: dict[str, int] = defaultdict(int)
    first_break_mode: dict[str, int] = defaultdict(int)
    for r in rows:
        first_break_direction[r.get("first_break_direction", "")] += 1
        first_break_mode[r.get("first_break_mode", "")] += 1
    print("first_break_direction_counts={0}".format(json.dumps(dict(sorted(first_break_direction.items())), ensure_ascii=True)))
    print("first_break_mode_counts={0}".format(json.dumps(dict(sorted(first_break_mode.items())), ensure_ascii=True)))


def build_coverage_report(rows: list[dict]) -> dict:
    total = len(rows)
    defined = sum(1 for r in rows if r.get("opening_range_defined") == "1")
    undefined = total - defined

    by_session: dict[str, dict] = {}
    total_by_session: dict[str, int] = defaultdict(int)
    defined_by_session: dict[str, int] = defaultdict(int)
    width_error_by_session: dict[str, int] = defaultdict(int)
    for r in rows:
        sid = r.get("session_id", "")
        total_by_session[sid] += 1
        if r.get("opening_range_defined") == "1":
            defined_by_session[sid] += 1
        if r.get("width_error_day") == "1":
            width_error_by_session[sid] += 1

    for sid in sorted(total_by_session.keys()):
        t = total_by_session[sid]
        d = defined_by_session.get(sid, 0)
        w = width_error_by_session.get(sid, 0)
        by_session[sid] = {
            "total_rows": t,
            "or_defined_rows": d,
            "or_defined_ratio": d / t if t else 0.0,
            "width_error_day_rows": w,
            "width_error_day_ratio": w / t if t else 0.0,
        }

    first_break_direction: dict[str, int] = defaultdict(int)
    first_break_mode: dict[str, int] = defaultdict(int)
    for r in rows:
        first_break_direction[r.get("first_break_direction", "")] += 1
        first_break_mode[r.get("first_break_mode", "")] += 1

    return {
        "total_rows": total,
        "or_defined_rows": defined,
        "or_undefined_rows": undefined,
        "or_defined_ratio": defined / total if total else 0.0,
        "by_session": by_session,
        "first_break_direction_counts": dict(sorted(first_break_direction.items())),
        "first_break_mode_counts": dict(sorted(first_break_mode.items())),
    }


def maybe_write_report(path: str, report: dict) -> None:
    if not path:
        return
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding="utf-8")


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
    maybe_write_report(str(args.report_json), report)
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
