from __future__ import annotations

import json
import os
from pathlib import Path

from pv_corr_state_p0_runtime_append_stub_v1 import load_params


class ValidationError(RuntimeError):
    pass


def ensure_archive_only_run_allowed() -> None:
    if os.environ.get("ALLOW_ARCHIVE_ONLY_RUN") != "1":
        raise SystemExit(
            "ARCHIVE_ONLY: set ALLOW_ARCHIVE_ONLY_RUN=1 and use repo-first entry points under "
            "01_active_objects/ 02_runtime/ 04_active_main_docs/ before running this legacy validator."
        )


def read_preview_rows(preview_csv: Path) -> list[str]:
    lines = preview_csv.read_text(encoding="utf-8").splitlines()
    if len(lines) < 2:
        raise ValidationError("preview csv has no data rows")
    return lines[1:]


def read_acceptance_rows(acceptance_md: Path) -> list[str]:
    rows: list[str] = []
    capture = False
    for raw_line in acceptance_md.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.strip() in {"- preview csv 当前内容：", "- preview csv 当时内容："}:
            capture = True
            continue
        if capture:
            if line.startswith("  - `") and line.endswith("`"):
                rows.append(line.strip()[3:-1])
                continue
            if line.startswith("## "):
                break
            if line.strip() == "":
                continue
            break
    if not rows:
        raise ValidationError("acceptance markdown has no preview csv row block")
    return rows


def main() -> None:
    ensure_archive_only_run_allowed()
    params = load_params()
    runtime_dir = Path(params["runtime_dir"])
    preview_csv = runtime_dir / params["replay_preview_csv"]
    acceptance_md = runtime_dir / params["replay_preview_acceptance_file"]

    preview_rows = read_preview_rows(preview_csv)
    acceptance_rows = read_acceptance_rows(acceptance_md)
    if preview_rows != acceptance_rows:
        raise ValidationError(
            "preview rows mismatch: preview={0} acceptance={1}".format(
                preview_rows, acceptance_rows
            )
        )

    print("validation_mode=archive_preview_acceptance_compare")
    print("preview_csv_exists={0}".format(preview_csv.exists()))
    print("acceptance_md_exists={0}".format(acceptance_md.exists()))
    print("preview_row_count={0}".format(len(preview_rows)))
    print("acceptance_row_count={0}".format(len(acceptance_rows)))
    print("rows_match=true")
    print("preview_trade_ids={0}".format(json.dumps([row.split(",")[0] for row in preview_rows], ensure_ascii=True)))
    print("archive_only=true")
    print("path_policy=repo_first")
    print("write_attempted=false")
    print("archive_preview_acceptance_validation_passed=true")


if __name__ == "__main__":
    main()
