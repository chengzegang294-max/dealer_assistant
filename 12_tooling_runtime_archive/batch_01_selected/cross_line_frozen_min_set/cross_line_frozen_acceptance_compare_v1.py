from __future__ import annotations

import json
from pathlib import Path

from cross_line_frozen_manifest_index_v1 import (
    build_candidate_manifest,
    pv_manifest_items,
    read_json,
    rsj_manifest_items,
)


class ValidationError(RuntimeError):
    pass


def parse_bool(raw: str) -> bool:
    if raw == "True":
        return True
    if raw == "False":
        return False
    raise ValidationError("unexpected boolean literal: {0}".format(raw))


def unwrap_line(line: str, prefix: str) -> str:
    stripped = line.strip()
    suffix = "`"
    if not stripped.startswith(prefix) or not stripped.endswith(suffix):
        raise ValidationError("unexpected line format: {0}".format(line))
    return stripped[len(prefix) : -len(suffix)]


def read_index_blocks(index_md: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    capture = False
    for raw_line in index_md.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.strip() == "## 当前跨线索引":
            capture = True
            continue
        if capture:
            if line.startswith("- `") and line.endswith("`"):
                if current is not None:
                    rows.append(current)
                current = {"candidate": unwrap_line(line, "- `")}
                continue
            if line.startswith("  - `manifest_count = ") and line.endswith("`"):
                if current is None:
                    raise ValidationError("manifest_count found before candidate header")
                current["manifest_count"] = int(unwrap_line(line, "- `manifest_count = "))
                continue
            if line.startswith("  - `all_manifest_files_exist = ") and line.endswith("`"):
                if current is None:
                    raise ValidationError("all_manifest_files_exist found before candidate header")
                current["all_manifest_files_exist"] = parse_bool(
                    unwrap_line(line, "- `all_manifest_files_exist = ")
                )
                continue
            if line.startswith("  - `manifest_freeze = ") and line.endswith("`"):
                if current is None:
                    raise ValidationError("manifest_freeze found before candidate header")
                current["manifest_freeze"] = unwrap_line(line, "- `manifest_freeze = ")
                continue
            if line.startswith("## "):
                break
    if current is not None:
        rows.append(current)
    if not rows:
        raise ValidationError("cross line index markdown has no candidate block")
    return rows


def build_expected_blocks(runtime_root: Path) -> list[dict[str, object]]:
    rsj_params = read_json(
        runtime_root / "rsj_state_p0_v1" / "rsj_state_p0_runtime_params_template_v1.json"
    )
    pv_params = read_json(
        runtime_root / "pv_corr_state_p0_v1" / "pv_corr_state_p0_runtime_params_template_v1.json"
    )
    rsj_runtime_dir = Path(str(rsj_params["runtime_dir"]))
    pv_runtime_dir = Path(str(pv_params["runtime_dir"]))
    rsj_manifest = build_candidate_manifest(
        str(rsj_params["candidate_id"]),
        rsj_runtime_dir,
        rsj_manifest_items(rsj_params),
    )
    pv_manifest = build_candidate_manifest(
        str(pv_params["candidate_id"]),
        pv_runtime_dir,
        pv_manifest_items(pv_params),
    )
    return [
        {
            "candidate": rsj_manifest["candidate"],
            "manifest_count": rsj_manifest["manifest_count"],
            "all_manifest_files_exist": rsj_manifest["all_manifest_files_exist"],
            "manifest_freeze": str(rsj_params["manifest_freeze_file"]),
        },
        {
            "candidate": pv_manifest["candidate"],
            "manifest_count": pv_manifest["manifest_count"],
            "all_manifest_files_exist": pv_manifest["all_manifest_files_exist"],
            "manifest_freeze": str(pv_params["manifest_freeze_file"]),
        },
    ]


def main() -> None:
    runtime_root = Path(__file__).resolve().parent
    index_md = runtime_root / "cross_line_frozen_manifest_index_v1.md"
    indexed_blocks = read_index_blocks(index_md)
    expected_blocks = build_expected_blocks(runtime_root)
    if indexed_blocks != expected_blocks:
        raise ValidationError(
            "cross line index mismatch: indexed={0} expected={1}".format(
                indexed_blocks, expected_blocks
            )
        )

    print("validation_mode=cross_line_frozen_acceptance_compare")
    print("index_md_exists={0}".format(index_md.exists()))
    print("indexed_candidate_count={0}".format(len(indexed_blocks)))
    print("expected_candidate_count={0}".format(len(expected_blocks)))
    print("rows_match=true")
    print("candidate_ids={0}".format(json.dumps([item["candidate"] for item in indexed_blocks], ensure_ascii=True)))
    print("write_attempted=false")
    print("cross_line_frozen_acceptance_compare_passed=true")


if __name__ == "__main__":
    main()
