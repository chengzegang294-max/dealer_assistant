from __future__ import annotations

import argparse
import json
import os
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


BATCH_DIR = Path(__file__).resolve().parent
ARTIFACT_ROOT = BATCH_DIR / "artifacts"


@dataclass(frozen=True)
class FamilySpec:
    name: str
    csv_patterns: tuple[str, ...]
    report_patterns: tuple[str, ...]
    log_patterns: tuple[str, ...]
    log_keywords: tuple[str, ...]
    repo_dirs: dict[str, Path]


@dataclass(frozen=True)
class MatchInfo:
    path: Path
    matched_keywords: tuple[str, ...] = ()
    matched_filename_keywords: tuple[str, ...] = ()


FAMILY_SPECS: dict[str, FamilySpec] = {
    "volty": FamilySpec(
        name="volty",
        csv_patterns=("MT4_probe_Volty_*.csv",),
        report_patterns=("mt4probe_volty_portable*.htm", "mt4probe_volty_portable*.html"),
        log_patterns=("*.log",),
        log_keywords=("MT4Probe_Volty", "MT4_probe_Volty", "VoltyChannel_Stop", "Volty"),
        repo_dirs={
            "csv": ARTIFACT_ROOT / "volty" / "csv",
            "report": ARTIFACT_ROOT / "volty" / "tester_report",
            "log": ARTIFACT_ROOT / "volty" / "log",
        },
    ),
    "xbreaking": FamilySpec(
        name="xbreaking",
        csv_patterns=("XBreaking_probe_*.csv",),
        report_patterns=(
            "*xbreaking*probe*report*.htm",
            "*xbreaking*probe*report*.html",
            "*XBreaking*probe*.htm",
            "*XBreaking*probe*.html",
        ),
        log_patterns=("*.log",),
        log_keywords=("XBreakingProbe", "XBreaking_probe", "XBreaking"),
        repo_dirs={
            "csv": ARTIFACT_ROOT / "xbreaking" / "csv",
            "report": ARTIFACT_ROOT / "xbreaking" / "tester_report",
            "log": ARTIFACT_ROOT / "xbreaking" / "log",
        },
    ),
}


def terminal_container_roots() -> list[Path]:
    roots: list[Path] = []
    for env_key in ("APPDATA", "LOCALAPPDATA"):
        base = os.environ.get(env_key)
        if not base:
            continue
        root = Path(base).expanduser() / "MetaQuotes" / "Terminal"
        if root.exists() and root.is_dir():
            roots.append(root)
    return roots


def mt_terminal_roots() -> list[Path]:
    roots: list[Path] = []
    for container in terminal_container_roots():
        for child in container.iterdir():
            if child.is_dir():
                roots.append(child)
    return roots


def common_files_dirs() -> list[Path]:
    dirs: list[Path] = []
    for container in terminal_container_roots():
        p = container / "Common" / "Files"
        if p.exists() and p.is_dir():
            dirs.append(p)
    return dirs


def candidate_search_dirs(kind: str) -> list[Path]:
    dirs: list[Path] = []
    if kind == "csv":
        for root in mt_terminal_roots():
            for rel in ("MQL4/Files", "MQL5/Files", "tester/files"):
                p = root / rel
                if p.exists() and p.is_dir():
                    dirs.append(p)
        dirs.extend(common_files_dirs())
    elif kind == "report":
        for root in mt_terminal_roots():
            for rel in ("tester/files", "MQL4/Files", "MQL5/Files"):
                p = root / rel
                if p.exists() and p.is_dir():
                    dirs.append(p)
        dirs.extend(common_files_dirs())
    elif kind == "log":
        for root in mt_terminal_roots():
            for rel in ("logs", "tester/logs", "MQL4/Logs", "MQL5/Logs"):
                p = root / rel
                if p.exists() and p.is_dir():
                    dirs.append(p)
    return dedupe_paths(dirs)


def dedupe_paths(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    result: list[Path] = []
    for path in paths:
        key = str(path.resolve())
        if key in seen:
            continue
        seen.add(key)
        result.append(path)
    return result


def patterns_for(spec: FamilySpec, kind: str) -> tuple[str, ...]:
    if kind == "csv":
        return spec.csv_patterns
    if kind == "report":
        return spec.report_patterns
    if kind == "log":
        return spec.log_patterns
    raise ValueError(f"unsupported kind: {kind}")


def effective_log_keywords(spec: FamilySpec, override_keywords: list[str]) -> tuple[str, ...]:
    if override_keywords:
        cleaned = [x.strip() for x in override_keywords if x.strip()]
        return tuple(cleaned)
    return spec.log_keywords


def try_read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-16", "utf-16-le", "gb18030", "latin-1"):
        try:
            return path.read_text(encoding=encoding, errors="ignore")
        except Exception:
            continue
    return ""


def tail_lines_text(text: str, tail_lines: int) -> str:
    if tail_lines <= 0:
        return text
    lines = text.splitlines()
    if len(lines) <= tail_lines:
        return text
    return "\n".join(lines[-tail_lines:])


def matched_log_keywords(path: Path, keywords: tuple[str, ...], tail_lines: int) -> tuple[str, ...]:
    if not keywords:
        return ()
    text = tail_lines_text(try_read_text(path), tail_lines)
    text_lower = text.lower()
    matched = [kw for kw in keywords if kw.lower() in text_lower]
    return tuple(matched)


def matched_filename_keywords(path: Path, keywords: list[str]) -> tuple[str, ...]:
    cleaned = [x.strip() for x in keywords if x.strip()]
    if not cleaned:
        return ()
    name_lower = path.name.lower()
    matched = [kw for kw in cleaned if kw.lower() in name_lower]
    return tuple(matched)


def build_log_excerpt(path: Path, keywords: tuple[str, ...], tail_lines: int, context_lines: int = 1) -> str:
    text = tail_lines_text(try_read_text(path), tail_lines)
    if not text:
        return ""
    lines = text.splitlines()
    if not lines:
        return ""
    if not keywords:
        return "\n".join(lines[-min(len(lines), max(tail_lines, 40)):])

    matched_indexes: list[int] = []
    lowered_keywords = [kw.lower() for kw in keywords]
    for idx, line in enumerate(lines):
        lower_line = line.lower()
        if any(kw in lower_line for kw in lowered_keywords):
            matched_indexes.append(idx)

    if not matched_indexes:
        return "\n".join(lines[-min(len(lines), max(tail_lines, 40)):])

    selected: set[int] = set()
    for idx in matched_indexes:
        start = max(0, idx - context_lines)
        end = min(len(lines), idx + context_lines + 1)
        for j in range(start, end):
            selected.add(j)

    ordered = sorted(selected)
    excerpt_lines: list[str] = []
    prev = None
    for idx in ordered:
        if prev is not None and idx != prev + 1:
            excerpt_lines.append("...")
        excerpt_lines.append(lines[idx])
        prev = idx
    return "\n".join(excerpt_lines)


def dedupe_match_infos(items: list[MatchInfo]) -> list[MatchInfo]:
    merged: dict[str, MatchInfo] = {}
    for item in items:
        key = str(item.path.resolve())
        if key not in merged:
            merged[key] = item
            continue
        existing = merged[key]
        combined = tuple(dict.fromkeys(existing.matched_keywords + item.matched_keywords))
        combined_filename = tuple(
            dict.fromkeys(existing.matched_filename_keywords + item.matched_filename_keywords)
        )
        merged[key] = MatchInfo(
            path=existing.path,
            matched_keywords=combined,
            matched_filename_keywords=combined_filename,
        )
    return list(merged.values())


def match_sort_key(item: MatchInfo) -> tuple[int, int, float]:
    return (
        len(item.matched_keywords),
        len(item.matched_filename_keywords),
        item.path.stat().st_mtime,
    )


def find_matches(
    spec: FamilySpec,
    kind: str,
    limit: int,
    log_keyword_override: list[str] | None = None,
    log_filename_keywords: list[str] | None = None,
    log_tail_lines: int = 0,
) -> list[MatchInfo]:
    found: list[MatchInfo] = []
    patterns = patterns_for(spec, kind)
    log_keywords = effective_log_keywords(spec, log_keyword_override or [])
    for base_dir in candidate_search_dirs(kind):
        for pattern in patterns:
            if kind == "log":
                candidates = base_dir.glob(pattern)
            else:
                candidates = base_dir.rglob(pattern)
            for path in candidates:
                if path.is_file():
                    if kind == "log":
                        filename_matched = matched_filename_keywords(path, log_filename_keywords or [])
                        if log_filename_keywords and not filename_matched:
                            continue
                        matched = matched_log_keywords(path, log_keywords, log_tail_lines)
                        if not matched and not filename_matched:
                            continue
                        found.append(
                            MatchInfo(
                                path=path,
                                matched_keywords=matched,
                                matched_filename_keywords=filename_matched,
                            )
                        )
                    else:
                        found.append(MatchInfo(path=path))
    found = dedupe_match_infos(found)
    found.sort(key=match_sort_key, reverse=True)
    return found[:limit]


def select_latest(
    spec: FamilySpec,
    kind: str,
    log_keyword_override: list[str] | None = None,
    log_filename_keywords: list[str] | None = None,
    log_tail_lines: int = 0,
) -> MatchInfo:
    matches = find_matches(
        spec,
        kind,
        limit=1,
        log_keyword_override=log_keyword_override,
        log_filename_keywords=log_filename_keywords,
        log_tail_lines=log_tail_lines,
    )
    if not matches:
        raise FileNotFoundError(
            build_not_found_message(spec, kind, log_keyword_override or [], log_filename_keywords or [], log_tail_lines)
        )
    return matches[0]


def select_latest_in_repo(spec: FamilySpec, kind: str) -> MatchInfo:
    repo_dir = spec.repo_dirs[kind]
    patterns = patterns_for(spec, kind)
    candidates: list[Path] = []
    for pattern in patterns:
        candidates.extend(repo_dir.glob(pattern))
    candidates = [p for p in candidates if p.exists() and p.is_file()]
    if not candidates:
        raise FileNotFoundError(f"repo artifacts not found: family={spec.name} kind={kind} dir={repo_dir.resolve()}")
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return MatchInfo(path=candidates[0])


def parse_kv_semicolon_lines(text: str) -> tuple[dict[str, str], dict[int, dict[str, str]]]:
    header: dict[str, str] = {}
    modes: dict[int, dict[str, str]] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = [x.strip() for x in line.split(";") if x.strip() != ""]
        if not parts:
            continue
        if parts[0] == "mode" and len(parts) >= 3:
            try:
                mode = int(parts[1])
            except Exception:
                continue
            stats: dict[str, str] = {}
            i = 2
            while i + 1 < len(parts):
                stats[parts[i]] = parts[i + 1]
                i += 2
            modes[mode] = stats
            continue
        if len(parts) >= 2:
            header[parts[0]] = parts[1]
    return header, modes


def parse_optional_float(raw: str | None) -> float | None:
    if raw is None:
        return None
    s = str(raw).strip()
    if not s:
        return None
    try:
        v = float(s)
    except Exception:
        return None
    if abs(v - 2147483647.0) < 1e-6:
        return None
    return v


def parse_optional_int(raw: str | None) -> int | None:
    if raw is None:
        return None
    s = str(raw).strip()
    if not s:
        return None
    try:
        return int(float(s))
    except Exception:
        return None


def derive_trend_state(trend_value: float | None) -> str:
    if trend_value is None:
        return "unknown"
    if trend_value > 0:
        return "up"
    if trend_value < 0:
        return "down"
    return "unknown"


def normalize_volty_probe_summary(csv_path: Path) -> dict[str, Any]:
    text = csv_path.read_text(encoding="utf-8", errors="ignore")
    header, modes = parse_kv_semicolon_lines(text)
    out: dict[str, Any] = {}
    out["probe_source_csv"] = csv_path.name
    out["symbol"] = header.get("symbol", "")
    out["chart_tf"] = parse_optional_int(header.get("chart_tf", ""))
    out["indicator_tf"] = parse_optional_int(header.get("indicator_tf", ""))
    out["indicator_name"] = header.get("indicator_name", "")
    out["max_modes"] = parse_optional_int(header.get("max_modes", ""))
    out["max_shifts"] = parse_optional_int(header.get("max_shifts", ""))
    out["used_common"] = parse_optional_int(header.get("used_common", ""))
    out["status"] = header.get("status", "")

    for mode in range(0, 8):
        stats = modes.get(mode, {})
        out[f"mode{mode}_non_empty"] = parse_optional_int(stats.get("non_empty", ""))
        out[f"mode{mode}_err_count"] = parse_optional_int(stats.get("err_count", ""))
        out[f"mode{mode}_first_valid"] = parse_optional_float(stats.get("first_valid", ""))
        out[f"mode{mode}_last_valid"] = parse_optional_float(stats.get("last_valid", ""))

    out["volty_up_stop_last"] = out.get("mode0_last_valid")
    out["volty_dn_stop_last"] = out.get("mode1_last_valid")
    out["volty_flip_up_last"] = out.get("mode2_last_valid")
    out["volty_flip_down_last"] = out.get("mode3_last_valid")
    out["volty_lower_band_last"] = out.get("mode4_last_valid")
    out["volty_upper_band_last"] = out.get("mode5_last_valid")
    trend_last = out.get("mode6_last_valid")
    out["volty_trend_last"] = trend_last
    out["volty_trend_state"] = derive_trend_state(trend_last if isinstance(trend_last, float) else None)
    return out


def parse_series_semicolon_lines(text: str) -> tuple[dict[str, str], list[dict[str, str]]]:
    header: dict[str, str] = {}
    series_rows: list[dict[str, str]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = [x.strip() for x in line.split(";") if x.strip() != ""]
        if not parts:
            continue
        if parts[0] == "series" and len(parts) >= 3:
            stats: dict[str, str] = {"series": "1"}
            i = 2
            while i + 1 < len(parts):
                stats[parts[i]] = parts[i + 1]
                i += 2
            series_rows.append(stats)
            continue
        if parts[0] == "mode":
            continue
        if len(parts) >= 2:
            header[parts[0]] = parts[1]
    return header, series_rows


def map_mode_to_volty_field(mode: int) -> str:
    if mode == 0:
        return "volty_up_stop"
    if mode == 1:
        return "volty_dn_stop"
    if mode == 2:
        return "volty_flip_up_value"
    if mode == 3:
        return "volty_flip_down_value"
    if mode == 4:
        return "volty_lower_band_raw"
    if mode == 5:
        return "volty_upper_band_raw"
    if mode == 6:
        return "volty_trend"
    return "unknown_suspect_all_zero"


def normalize_volty_probe_series(csv_path: Path) -> dict[str, Any]:
    text = csv_path.read_text(encoding="utf-8", errors="ignore")
    header, series_rows = parse_series_semicolon_lines(text)
    out: dict[str, Any] = {}
    out["probe_source_csv"] = csv_path.name
    out["symbol"] = header.get("symbol", "")
    out["chart_tf"] = parse_optional_int(header.get("chart_tf", ""))
    out["indicator_tf"] = parse_optional_int(header.get("indicator_tf", ""))
    out["indicator_name"] = header.get("indicator_name", "")
    out["max_modes"] = parse_optional_int(header.get("max_modes", ""))
    out["max_shifts"] = parse_optional_int(header.get("max_shifts", ""))
    out["used_common"] = parse_optional_int(header.get("used_common", ""))
    out["status"] = header.get("status", "")

    normalized_rows: list[dict[str, Any]] = []
    for row in series_rows:
        mode = parse_optional_int(row.get("mode", ""))
        shift = parse_optional_int(row.get("shift", ""))
        bar_time = row.get("bar_time", "")
        value = parse_optional_float(row.get("value", ""))
        err = parse_optional_int(row.get("err", ""))
        if mode is None or shift is None:
            continue
        normalized_rows.append(
            {
                "bar_time": bar_time,
                "mode": mode,
                "shift": shift,
                "field": map_mode_to_volty_field(mode),
                "value": value,
                "err": err,
            }
        )

    out["series_row_count"] = len(normalized_rows)
    out["rows"] = normalized_rows
    return out


def build_not_found_message(
    spec: FamilySpec,
    kind: str,
    log_keyword_override: list[str],
    log_filename_keywords: list[str],
    log_tail_lines: int,
) -> str:
    lines: list[str] = []
    lines.append(f"family={spec.name}")
    lines.append(f"kind={kind}")
    lines.append("found=false")
    lines.append(f"repo_target={spec.repo_dirs[kind].resolve()}")
    lines.append(f"patterns={json.dumps(patterns_for(spec, kind), ensure_ascii=True)}")
    if kind == "log":
        lines.append(
            "log_keywords={0}".format(json.dumps(effective_log_keywords(spec, log_keyword_override), ensure_ascii=True))
        )
        lines.append("log_filename_keywords={0}".format(json.dumps(log_filename_keywords, ensure_ascii=True)))
        lines.append(f"log_tail_lines={log_tail_lines}")
    lines.append(
        "search_dirs={0}".format(
            json.dumps([str(p) for p in candidate_search_dirs(kind)[:20]], ensure_ascii=True)
        )
    )
    return "\n".join(lines)


def safe_copy(src: Path, dst_dir: Path) -> Path:
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    if dst.exists():
        stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        dst = dst_dir / f"{src.stem}_{stamp}{src.suffix}"
    shutil.copy2(src, dst)
    return dst


def write_log_excerpt_file(dst: Path, excerpt_text: str) -> Path:
    excerpt_path = dst.with_name(f"{dst.stem}__excerpt.txt")
    excerpt_path.write_text(excerpt_text, encoding="utf-8")
    return excerpt_path


def print_matches(
    spec: FamilySpec,
    kind: str,
    matches: list[MatchInfo],
    log_keyword_override: list[str],
    log_filename_keywords: list[str],
    log_tail_lines: int,
) -> None:
    print(f"family={spec.name}")
    print(f"kind={kind}")
    print(f"repo_target={spec.repo_dirs[kind].resolve()}")
    if kind == "log":
        print("log_keywords={0}".format(json.dumps(effective_log_keywords(spec, log_keyword_override), ensure_ascii=True)))
        print("log_filename_keywords={0}".format(json.dumps(log_filename_keywords, ensure_ascii=True)))
        print(f"log_tail_lines={log_tail_lines}")
    print(f"match_count={len(matches)}")
    serialised = [
        {
            "path": str(item.path.resolve()),
            "mtime": datetime.fromtimestamp(item.path.stat().st_mtime).isoformat(timespec="seconds"),
            "size": item.path.stat().st_size,
            "matched_keywords": list(item.matched_keywords),
            "matched_filename_keywords": list(item.matched_filename_keywords),
        }
        for item in matches
    ]
    print("matches={0}".format(json.dumps(serialised, ensure_ascii=True)))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", required=True, choices=sorted(FAMILY_SPECS))
    parser.add_argument("--kind", required=True, choices=("csv", "report", "log"))
    parser.add_argument("--list", action="store_true", help="list candidate files only")
    parser.add_argument("--copy-latest", action="store_true", help="copy latest matched file into batch artifacts")
    parser.add_argument("--source", default="", help="copy an explicit source path instead of auto-selecting latest")
    parser.add_argument("--limit", type=int, default=10, help="max candidates to print when listing")
    parser.add_argument(
        "--log-keyword",
        action="append",
        default=[],
        help="log content keyword filter; can be passed multiple times",
    )
    parser.add_argument(
        "--log-filename-keyword",
        action="append",
        default=[],
        help="log filename keyword filter; can be passed multiple times",
    )
    parser.add_argument(
        "--log-tail-lines",
        type=int,
        default=0,
        help="when kind=log, only scan the last N lines for keyword matching; 0 means full file",
    )
    parser.add_argument("--normalize-volty-summary", action="store_true", help="normalize volty probe summary csv")
    parser.add_argument("--normalize-volty-series", action="store_true", help="normalize volty probe series csv")
    parser.add_argument("--input", default="", help="explicit input file path for normalization")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    spec = FAMILY_SPECS[args.family]

    if args.normalize_volty_summary:
        if args.family != "volty" or args.kind != "csv":
            raise SystemExit("--normalize-volty-summary requires --family volty --kind csv")
        if args.input:
            csv_path = Path(args.input).expanduser().resolve()
        else:
            csv_path = select_latest_in_repo(spec, "csv").path
        if not csv_path.exists() or not csv_path.is_file():
            raise FileNotFoundError(f"input not found: {csv_path}")
        normalized = normalize_volty_probe_summary(csv_path)
        print("format=volty_probe_summary_normalized_v1")
        print("normalized={0}".format(json.dumps(normalized, ensure_ascii=True)))
        return

    if args.normalize_volty_series:
        if args.family != "volty" or args.kind != "csv":
            raise SystemExit("--normalize-volty-series requires --family volty --kind csv")
        if args.input:
            csv_path = Path(args.input).expanduser().resolve()
        else:
            csv_path = select_latest_in_repo(spec, "csv").path
        if not csv_path.exists() or not csv_path.is_file():
            raise FileNotFoundError(f"input not found: {csv_path}")
        normalized = normalize_volty_probe_series(csv_path)
        print("format=volty_probe_series_normalized_v1")
        print("normalized={0}".format(json.dumps(normalized, ensure_ascii=True)))
        return

    if args.list:
        matches = find_matches(
            spec,
            args.kind,
            limit=max(args.limit, 1),
            log_keyword_override=args.log_keyword,
            log_filename_keywords=args.log_filename_keyword,
            log_tail_lines=args.log_tail_lines,
        )
        print_matches(spec, args.kind, matches, args.log_keyword, args.log_filename_keyword, args.log_tail_lines)
        return

    if args.source:
        selected_path = Path(args.source).expanduser().resolve()
        selected = MatchInfo(
            path=selected_path,
            matched_keywords=matched_log_keywords(
                selected_path,
                effective_log_keywords(spec, args.log_keyword),
                args.log_tail_lines,
            )
            if args.kind == "log"
            else (),
            matched_filename_keywords=matched_filename_keywords(selected_path, args.log_filename_keyword)
            if args.kind == "log"
            else (),
        )
        if not selected.path.exists() or not selected.path.is_file():
            raise FileNotFoundError(f"source not found: {selected.path}")
    elif args.copy_latest:
        selected = select_latest(
            spec,
            args.kind,
            log_keyword_override=args.log_keyword,
            log_filename_keywords=args.log_filename_keyword,
            log_tail_lines=args.log_tail_lines,
        )
    else:
        raise SystemExit("use --list or --copy-latest or provide --source")

    dst = safe_copy(selected.path, spec.repo_dirs[args.kind])
    print(f"family={spec.name}")
    print(f"kind={args.kind}")
    if args.kind == "log":
        print("log_keywords={0}".format(json.dumps(effective_log_keywords(spec, args.log_keyword), ensure_ascii=True)))
        print("log_filename_keywords={0}".format(json.dumps(args.log_filename_keyword, ensure_ascii=True)))
        print(f"log_tail_lines={args.log_tail_lines}")
        print("matched_keywords={0}".format(json.dumps(list(selected.matched_keywords), ensure_ascii=True)))
        print(
            "matched_filename_keywords={0}".format(json.dumps(list(selected.matched_filename_keywords), ensure_ascii=True))
        )
        excerpt = build_log_excerpt(
            selected.path,
            selected.matched_keywords,
            args.log_tail_lines,
        )
        excerpt_path = write_log_excerpt_file(dst, excerpt)
        print(f"excerpt_written_to={excerpt_path}")
    print(f"source={selected.path}")
    print(f"copied_to={dst}")


if __name__ == "__main__":
    main()
