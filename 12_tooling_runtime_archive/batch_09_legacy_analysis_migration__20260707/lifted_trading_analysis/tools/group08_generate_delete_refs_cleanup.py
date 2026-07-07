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

DELETE_PLAN_TSV = GROUP08_ROOT / "GROUP_08_external_delete_candidate_plan_v1.tsv"
OUT_TSV = GROUP08_ROOT / "GROUP_08_delete_candidates_ref_cleanup_list_v1.tsv"
OUT_MD = GROUP08_ROOT / "GROUP_08_delete_candidates_ref_cleanup_list_v1.md"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def iter_text_files(root: Path) -> list[Path]:
    exts = {".md", ".tsv", ".txt", ".py", ".json", ".yml", ".yaml"}
    files: list[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in exts:
            continue
        if ".git" in p.parts:
            continue
        files.append(p)
    return files


def read_lines(path: Path) -> list[str]:
    for enc in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            text = path.read_text(encoding=enc, errors="ignore")
            return text.splitlines()
        except Exception:
            continue
    return []


def classify_fix_action(path: Path, line_text: str, token_type: str) -> str:
    p = str(path).replace("\\", "/")
    if p.endswith("/10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/S_BUCKET_INDEX__2026-06-17.tsv"):
        return "KEEP_SNAPSHOT_INDEX"
    if "/tools/" in p.replace("\\", "/"):
        return "OPTIONAL_TOOL_REF"
    if str(GROUP08_ROOT).lower().replace("\\", "/") in p.lower():
        return "IGNORE_GROUP08_INTERNAL"

    if "00_external_import_staging" in line_text.replace("\\", "/"):
        return "IGNORE_ALREADY_STAGING"

    if token_type == "fullpath" and "d:\\stock\\cut_file" in line_text.lower():
        return "REPLACE_WITH_STAGING"

    if token_type == "basename":
        return "REVIEW_BASENAME_ONLY"

    return "REVIEW"


def write_md(path: Path, rows: list[dict[str, str]]) -> None:
    by_pid: dict[str, list[dict[str, str]]] = {}
    for r in rows:
        by_pid.setdefault(r["paper_id"], []).append(r)

    lines: list[str] = []
    lines.append("# GROUP_08 delete 候选 8 条：清引用清单 v1")
    lines.append("")
    lines.append("本清单只列出 `GROUP_08` 目录之外的引用命中，用于进入“真删除窗口”前清理引用。")
    lines.append("")

    for pid in sorted(by_pid.keys()):
        items = by_pid[pid]
        title = next((x.get("title_anchor") for x in items if x.get("title_anchor")), "")
        lines.append(f"## {pid} {title}".rstrip())
        lines.append("")

        def key_fn(x: dict[str, str]) -> tuple[str, str, str, int]:
            file_path = x.get("match_file", "")
            token_type = x.get("token_type", "")
            token = x.get("token", "")
            try:
                ln = int(x.get("line_no", "0"))
            except Exception:
                ln = 0
            return (file_path, token_type, token, ln)

        for r in sorted(items, key=key_fn):
            lines.append(f"- file: {r.get('match_file','')}")
            lines.append(f"  - token_type: {r.get('token_type','')}")
            lines.append(f"  - token: {r.get('token','')}")
            lines.append(f"  - line: {r.get('line_no','')}")
            lines.append(f"  - fix_action: {r.get('fix_action','')}")
            repl = r.get("suggested_replacement", "")
            if repl:
                lines.append(f"  - suggested_replacement: {repl}")
            snippet = (r.get("line_text") or "").strip()
            if snippet:
                lines.append(f"  - snippet: {snippet}")
        lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    delete_rows = read_tsv(DELETE_PLAN_TSV)
    if not delete_rows:
        raise SystemExit(f"empty delete plan: {DELETE_PLAN_TSV}")

    delete_by_id = {r["paper_id"]: r for r in delete_rows}

    targets: list[tuple[str, str, str, str, str]] = []
    for r in delete_rows:
        pid = r["paper_id"]
        title = (r.get("src_rel_under_root") or "").strip()
        src = (r.get("delete_candidate_path") or "").strip()
        staging = (r.get("repo_staging_path_after") or "").strip()
        base = Path(src).name if src else ""
        if base:
            targets.append((pid, title, "basename", base, staging))
        if src:
            targets.append((pid, title, "fullpath", src, staging))

    repo_files = iter_text_files(REPO_ROOT)
    g08_prefix = str(GROUP08_ROOT).lower().replace("\\", "/")

    out_rows: list[dict[str, str]] = []
    for pid, title, token_type, token, staging in targets:
        for p in repo_files:
            p_norm = str(p).lower().replace("\\", "/")
            if p_norm.startswith(g08_prefix):
                continue
            lines = read_lines(p)
            for i, line in enumerate(lines, start=1):
                if token and token in line:
                    fix_action = classify_fix_action(p, line, token_type)
                    suggested = (
                        staging
                        if token_type == "fullpath" and staging and fix_action == "REPLACE_WITH_STAGING"
                        else ""
                    )
                    out_rows.append(
                        {
                            "paper_id": pid,
                            "title_anchor": title,
                            "token_type": token_type,
                            "token": token,
                            "match_file": str(p),
                            "line_no": str(i),
                            "line_text": line.strip(),
                            "fix_action": fix_action,
                            "suggested_replacement": suggested,
                        }
                    )

    out_rows.sort(
        key=lambda x: (
            x.get("paper_id", ""),
            x.get("match_file", ""),
            x.get("token_type", ""),
            int(x.get("line_no", "0") or "0"),
        )
    )
    write_tsv(
        OUT_TSV,
        out_rows,
        [
            "paper_id",
            "title_anchor",
            "token_type",
            "token",
            "match_file",
            "line_no",
            "line_text",
            "fix_action",
            "suggested_replacement",
        ],
    )
    write_md(OUT_MD, out_rows)

    print(f"delete_candidates={len(delete_rows)}")
    print(f"ref_hits_outside_group08={len(out_rows)}")
    print(f"out_tsv={OUT_TSV}")
    print(f"out_md={OUT_MD}")


if __name__ == "__main__":
    main()
