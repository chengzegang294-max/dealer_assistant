from __future__ import annotations

from pathlib import Path
import csv


REPO_ROOT = Path(__file__).resolve().parents[1]
GROUP08_ROOT = (
    REPO_ROOT
    / "10_来源库_SOURCE_LIBRARY"
    / "01_Kimi拆书待入库"
    / "GROUP_08_A股量化_数据研究"
)

MOVE_PLAN_TSV = GROUP08_ROOT / "GROUP_08_external_move_plan_v1.tsv"
DELETE_PLAN_TSV = GROUP08_ROOT / "GROUP_08_external_delete_candidate_plan_v1.tsv"

OUT_MOVE_PS1 = GROUP08_ROOT / "GROUP_08_external_move_plan_dryrun_v1.ps1"
OUT_DELETE_PS1 = GROUP08_ROOT / "GROUP_08_external_delete_candidate_dryrun_v1.ps1"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def ps_quote_literal(text: str) -> str:
    return "'" + text.replace("'", "''") + "'"


def write_lines(path: Path, lines: list[str]) -> None:
    path.write_text("\r\n".join(lines) + "\r\n", encoding="utf-8-sig")


def to_int(text: str) -> int:
    try:
        return int((text or "0").strip())
    except Exception:
        return 0


def build_move_ps1(rows: list[dict[str, str]]) -> list[str]:
    lines: list[str] = []
    lines.append("param([switch]$Execute)")
    lines.append("$DryRun = -not $Execute")
    lines.append("Set-StrictMode -Version Latest")
    lines.append('$ErrorActionPreference = "Stop"')
    lines.append("")

    for r in rows:
        src = (r.get("source_path_before") or "").strip()
        dst = (r.get("suggested_dest_path") or "").strip()
        paper_id = (r.get("paper_id") or "").strip()
        if not src or not dst:
            continue

        outside_b = to_int(r.get("outside_refs_basename", "0"))
        outside_f = to_int(r.get("outside_refs_fullpath", "0"))
        outside_total = outside_b + outside_f

        lines.append(f'Write-Host {ps_quote_literal("MOVE " + paper_id)}')
        lines.append(f"$src = {ps_quote_literal(src)}")
        lines.append(f"$dst = {ps_quote_literal(dst)}")
        lines.append('if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }')
        if outside_total > 0:
            lines.append(
                f'Write-Warning {ps_quote_literal(f"outside_group08_refs>0 for {paper_id}: basename={outside_b} fullpath={outside_f}")}'
            )
        lines.append("$dstDir = Split-Path -Parent $dst")
        lines.append("if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }")
        lines.append("if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }")
        lines.append("")

    return lines


def build_delete_ps1(rows: list[dict[str, str]]) -> list[str]:
    lines: list[str] = []
    lines.append("param([switch]$Execute)")
    lines.append("$DryRun = -not $Execute")
    lines.append("Set-StrictMode -Version Latest")
    lines.append('$ErrorActionPreference = "Stop"')
    lines.append("")

    for r in rows:
        src = (r.get("delete_candidate_path") or "").strip()
        paper_id = (r.get("paper_id") or "").strip()
        if not src:
            continue

        outside_b = to_int(r.get("outside_refs_basename", "0"))
        outside_f = to_int(r.get("outside_refs_fullpath", "0"))
        outside_total = outside_b + outside_f

        lines.append(f'Write-Host {ps_quote_literal("DELETE_CANDIDATE " + paper_id)}')
        lines.append(f"$src = {ps_quote_literal(src)}")
        lines.append('if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }')
        if outside_total > 0:
            lines.append(
                f'Write-Warning {ps_quote_literal(f"outside_group08_refs>0 for {paper_id}: basename={outside_b} fullpath={outside_f}")}'
            )
        lines.append("if ($DryRun) { Remove-Item -LiteralPath $src -Force -WhatIf } else { Remove-Item -LiteralPath $src -Force }")
        lines.append("")

    return lines


def main() -> None:
    move_rows = read_tsv(MOVE_PLAN_TSV)
    delete_rows = read_tsv(DELETE_PLAN_TSV)

    move_lines = build_move_ps1(move_rows)
    delete_lines = build_delete_ps1(delete_rows)

    write_lines(OUT_MOVE_PS1, move_lines)
    write_lines(OUT_DELETE_PS1, delete_lines)

    print(f"wrote_move={OUT_MOVE_PS1}")
    print(f"wrote_delete={OUT_DELETE_PS1}")
    print(f"move_rows={len(move_rows)}")
    print(f"delete_candidate_rows={len(delete_rows)}")


if __name__ == "__main__":
    main()
