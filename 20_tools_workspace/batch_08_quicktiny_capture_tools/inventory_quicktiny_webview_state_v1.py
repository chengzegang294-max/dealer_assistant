from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


INTERESTING_NAMES = {
    "cookies",
    "history",
    "local storage",
    "indexeddb",
    "cache",
    "code cache",
    "service worker",
    "network",
    "preferences",
    "web data",
    "login data",
    "session storage",
}


def clean_text(value: object) -> str:
    return " ".join(str(value or "").replace("\r", "\n").split())


def iso_mtime(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime).isoformat(sep=" ", timespec="seconds")


def looks_interesting(path: Path) -> bool:
    name = path.name.lower()
    if name in INTERESTING_NAMES:
        return True
    if path.suffix.lower() in {".ldb", ".log", ".sqlite", ".db"}:
        return True
    return any(token in name for token in ["history", "cookie", "storage", "cache", "worker"])


@dataclass
class InterestingEntry:
    relative_path: str
    kind: str
    size_bytes: int
    modified_at: str


def scan_top_level(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not root.exists():
        return rows
    for child in sorted(root.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
        row = {
            "name": child.name,
            "kind": "dir" if child.is_dir() else "file",
            "modified_at": iso_mtime(child),
        }
        if child.is_file():
            row["size_bytes"] = child.stat().st_size
        else:
            sub_counter = Counter("dir" if p.is_dir() else "file" for p in child.iterdir())
            row["child_dir_count"] = sub_counter.get("dir", 0)
            row["child_file_count"] = sub_counter.get("file", 0)
        rows.append(row)
    return rows


def scan_interesting(root: Path, max_entries: int) -> list[InterestingEntry]:
    entries: list[InterestingEntry] = []
    if not root.exists():
        return entries
    for path in root.rglob("*"):
        if len(entries) >= max_entries:
            break
        if not looks_interesting(path):
            continue
        kind = "dir" if path.is_dir() else "file"
        size_bytes = 0 if path.is_dir() else path.stat().st_size
        entries.append(
            InterestingEntry(
                relative_path=str(path.relative_to(root)),
                kind=kind,
                size_bytes=size_bytes,
                modified_at=iso_mtime(path),
            )
        )
    return entries


def build_payload(install_dir: Path, webview_dir: Path, max_entries: int) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "install_dir": str(install_dir),
        "install_dir_exists": install_dir.exists(),
        "webview_dir": str(webview_dir),
        "webview_dir_exists": webview_dir.exists(),
        "install_top_level": scan_top_level(install_dir),
        "webview_top_level": scan_top_level(webview_dir),
        "webview_interesting_entries": [entry.__dict__ for entry in scan_interesting(webview_dir, max_entries)],
    }
    exe_path = install_dir / "quicktiny-stock-ladder-desktop.exe"
    payload["desktop_exe_exists"] = exe_path.exists()
    if exe_path.exists():
        payload["desktop_exe_modified_at"] = iso_mtime(exe_path)
        payload["desktop_exe_size_bytes"] = exe_path.stat().st_size
    return payload


def build_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# quicktiny / 连板天梯 本地安装与 WebView 数据面盘点",
        "",
        f"- generated_at: `{payload['generated_at']}`",
        f"- install_dir_exists: `{payload['install_dir_exists']}`",
        f"- webview_dir_exists: `{payload['webview_dir_exists']}`",
        f"- desktop_exe_exists: `{payload['desktop_exe_exists']}`",
        "",
        "## 安装目录顶层",
        "",
    ]

    install_top = payload.get("install_top_level", [])
    if install_top:
        for row in install_top[:20]:
            if row["kind"] == "dir":
                lines.append(
                    "- `{}` | dir | child_dirs=`{}` | child_files=`{}`".format(
                        row["name"], row.get("child_dir_count", 0), row.get("child_file_count", 0)
                    )
                )
            else:
                lines.append("- `{}` | file | size=`{}`".format(row["name"], row.get("size_bytes", 0)))
    else:
        lines.append("- 安装目录不存在或为空")

    lines.extend(["", "## WebView 顶层", ""])
    webview_top = payload.get("webview_top_level", [])
    if webview_top:
        for row in webview_top[:30]:
            if row["kind"] == "dir":
                lines.append(
                    "- `{}` | dir | child_dirs=`{}` | child_files=`{}`".format(
                        row["name"], row.get("child_dir_count", 0), row.get("child_file_count", 0)
                    )
                )
            else:
                lines.append("- `{}` | file | size=`{}`".format(row["name"], row.get("size_bytes", 0)))
    else:
        lines.append("- WebView 目录不存在或为空")

    lines.extend(["", "## 重点存储痕迹", ""])
    interesting = payload.get("webview_interesting_entries", [])
    if interesting:
        for row in interesting[:80]:
            lines.append(
                "- `{}` | `{}` | size=`{}` | mtime=`{}`".format(
                    row["relative_path"], row["kind"], row["size_bytes"], row["modified_at"]
                )
            )
    else:
        lines.append("- 当前未扫到重点存储痕迹")

    lines.extend(
        [
            "",
            "## 一句话口径",
            "",
            "- 这份盘点先解决“本机到底有什么”这个问题，不直接宣称已抓到数据；后续抓取、网络请求观察、缓存抽样都以这里的目录事实为起点。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inventory quicktiny desktop install folder and EBWebView local data."
    )
    parser.add_argument("--install-dir", required=True, help="Path to quicktiny install directory")
    parser.add_argument("--webview-dir", required=True, help="Path to EBWebView local data directory")
    parser.add_argument("--output-json", required=True, help="Path to output JSON")
    parser.add_argument("--output-md", required=True, help="Path to output markdown")
    parser.add_argument(
        "--max-interesting-entries",
        type=int,
        default=200,
        help="Maximum number of interesting WebView entries to record",
    )
    args = parser.parse_args()

    install_dir = Path(args.install_dir)
    webview_dir = Path(args.webview_dir)
    payload = build_payload(install_dir, webview_dir, args.max_interesting_entries)

    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)

    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    output_md.write_text(build_markdown(payload), encoding="utf-8")

    print(str(output_json))
    print(str(output_md))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
