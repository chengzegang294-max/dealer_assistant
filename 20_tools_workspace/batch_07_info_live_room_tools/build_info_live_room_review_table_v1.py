from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def clean_text(value: object) -> str:
    return " ".join(str(value or "").replace("\r", "\n").split())


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_rows(data: dict) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for room in data.get("rooms", []):
        preview = clean_text(room.get("latest_preview_text", ""))
        rows.append(
            {
                "room_anchor": clean_text(room.get("room_anchor", "")),
                "latest_time_text": clean_text(room.get("latest_time_text", "")),
                "latest_date_badge": clean_text(room.get("latest_date_badge", "")),
                "content_form_hint": clean_text(room.get("content_form_hint", "")),
                "notification_hint": clean_text(room.get("notification_hint", "")),
                "latest_preview_text": preview,
                "review_bucket": "",
                "review_notes": "",
            }
        )
    return rows


def write_tsv(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "room_anchor",
        "latest_time_text",
        "latest_date_badge",
        "content_form_hint",
        "notification_hint",
        "latest_preview_text",
        "review_bucket",
        "review_notes",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a review table from info-live room list export JSON."
    )
    parser.add_argument("--input", required=True, help="Path to room list JSON")
    parser.add_argument("--output", required=True, help="Path to TSV file")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    data = load_json(input_path)
    write_tsv(build_rows(data), output_path)
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
