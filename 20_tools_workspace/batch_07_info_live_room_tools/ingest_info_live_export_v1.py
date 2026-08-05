from __future__ import annotations

import argparse
import json
from pathlib import Path


def clean_text(value: object) -> str:
    return " ".join(str(value or "").replace("\r", "\n").split())


def slug_like(value: str) -> str:
    text = clean_text(value)
    if not text:
        return "unknown"
    sanitized = (
        text.replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
        .replace("*", "_")
        .replace("?", "_")
        .replace("\"", "_")
        .replace("<", "_")
        .replace(">", "_")
        .replace("|", "_")
        .replace(" ", "_")
    )
    return sanitized[:48] or "unknown"


def build_markdown(data: dict, source_path: Path) -> str:
    sample_date = clean_text(data.get("sample_date", ""))
    room_anchor = clean_text(data.get("room_anchor", ""))
    topic_anchor = clean_text(data.get("topic_anchor", ""))
    display_date = clean_text(data.get("display_date", ""))
    display_time = clean_text(data.get("display_time", ""))
    excerpt = clean_text(data.get("excerpt", ""))
    image_evidence = clean_text(data.get("image_evidence", ""))
    source_url = clean_text(data.get("source_url", ""))
    access_mode = clean_text(data.get("access_mode", ""))
    notes = clean_text(data.get("notes", ""))
    page_url = clean_text(data.get("page_url", ""))
    exported_at = clean_text(data.get("exported_at", ""))

    return f"""# 信息直播间导出摘录草稿

- source_json: `{source_path}`
- exported_at: `{exported_at}`
- source_family: `信息直播间`
- source_url: `{source_url}`
- page_url: `{page_url}`
- access_mode: `{access_mode}`
- sample_date: `{sample_date}`
- room_anchor: `{room_anchor}`
- topic_anchor: `{topic_anchor}`
- display_date: `{display_date}`
- display_time: `{display_time}`
- image_evidence: `{image_evidence}`
- a5_role_layer: `explanation_layer_or_side_evidence`
- notes: `{notes}`

## Excerpt

```text
{excerpt}
```
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert info-live current-page export JSON into a markdown draft."
    )
    parser.add_argument("--input", required=True, help="Path to exported JSON file")
    parser.add_argument("--out-dir", required=True, help="Directory to place markdown draft")
    args = parser.parse_args()

    input_path = Path(args.input)
    out_dir = Path(args.out_dir)

    if not input_path.exists():
        raise FileNotFoundError(str(input_path))

    data = json.loads(input_path.read_text(encoding="utf-8"))

    sample_date = clean_text(data.get("sample_date", "")) or "unknown_date"
    room_anchor = slug_like(data.get("room_anchor", "")) or "unknown_room"
    topic_anchor = slug_like(data.get("topic_anchor", "")) or "unknown_topic"

    file_name = f"info_live_export_draft__{sample_date}__{room_anchor}__{topic_anchor}.md"
    out_path = out_dir / file_name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_markdown(data, input_path), encoding="utf-8")

    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
