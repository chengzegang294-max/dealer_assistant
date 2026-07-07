from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, cast


BATCH_DIR = Path(__file__).resolve().parent
ARTIFACT_ROOT = BATCH_DIR / "artifacts"
PROJECT_ROOT = BATCH_DIR.parents[2]
ENVIRONMENT_INVENTORY_LATEST = BATCH_DIR / "environment_snapshots" / "mt_environment_inventory_latest.json"


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
        report_patterns=(
            "mt4probe_volty_portable*.htm",
            "mt4probe_volty_portable*.html",
            "mt4probe_volty_dumpseries_portable*.htm",
            "mt4probe_volty_dumpseries_portable*.html",
        ),
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
            "xbreaking_probe*.htm",
            "xbreaking_probe*.html",
            "mt4probe_xbreaking*.htm",
            "mt4probe_xbreaking*.html",
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


def portable_instance_roots() -> list[Path]:
    roots: list[Path] = []
    override = os.environ.get("MT_PORTABLE_INSTANCE_ROOT", "").strip()
    if override:
        candidate = Path(override).expanduser()
        if candidate.exists() and candidate.is_dir():
            roots.append(candidate)
    candidates = [
        PROJECT_ROOT
        / "12_tooling_runtime_archive"
        / "batch_05_legacy_mt4_probe_assets__20260706"
        / "03_MT4便携探针实例",
        PROJECT_ROOT / "12_tooling_runtime_archive" / "batch_05_legacy_mt4_probe_assets__20260706" / "mt4_probe_instance",
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            roots.append(candidate)
    return dedupe_paths(roots)


def candidate_search_dirs(kind: str) -> list[Path]:
    dirs: list[Path] = []
    if kind == "csv":
        for root in mt_terminal_roots():
            for rel in ("MQL4/Files", "MQL5/Files", "tester/files"):
                p = root / rel
                if p.exists() and p.is_dir():
                    dirs.append(p)
        for root in portable_instance_roots():
            for rel in ("tester/files", "MQL4/Files", "MQL5/Files"):
                p = root / rel
                if p.exists() and p.is_dir():
                    dirs.append(p)
        dirs.extend(common_files_dirs())
    elif kind == "report":
        for root in mt_terminal_roots():
            if root.exists() and root.is_dir():
                dirs.append(root)
            for rel in ("tester/files", "MQL4/Files", "MQL5/Files"):
                p = root / rel
                if p.exists() and p.is_dir():
                    dirs.append(p)
        for root in portable_instance_roots():
            if root.exists() and root.is_dir():
                dirs.append(root)
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
        for root in portable_instance_roots():
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
    for encoding in ("utf-16", "utf-16-le", "utf-8", "gb18030", "latin-1"):
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


def path_specificity_rank(path: Path) -> tuple[int, int]:
    lower = str(path.resolve()).replace("/", "\\").lower()
    is_tester_log = int("\\tester\\logs\\" in lower or "\\agent-" in lower)
    is_terminal_log = int("\\logs\\" in lower)
    return (is_tester_log, is_terminal_log)


def match_sort_key(item: MatchInfo) -> tuple[int, int, int, int, float]:
    return (
        len(item.matched_keywords),
        len(item.matched_filename_keywords),
        *path_specificity_rank(item.path),
        item.path.stat().st_mtime,
    )


def find_matches(
    spec: FamilySpec,
    kind: str,
    limit: int,
    log_keyword_override: Optional[list[str]] = None,
    log_filename_keywords: Optional[list[str]] = None,
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
    log_keyword_override: Optional[list[str]] = None,
    log_filename_keywords: Optional[list[str]] = None,
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


def parse_optional_float(raw: Optional[str]) -> Optional[float]:
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


def parse_optional_int(raw: Optional[str]) -> Optional[int]:
    if raw is None:
        return None
    s = str(raw).strip()
    if not s:
        return None
    try:
        return int(float(s))
    except Exception:
        return None


def derive_trend_state(trend_value: Optional[float]) -> str:
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


def files_identical(src: Path, dst: Path) -> bool:
    try:
        if src.stat().st_size != dst.stat().st_size:
            return False
        return src.read_bytes() == dst.read_bytes()
    except Exception:
        return False


def safe_copy(src: Path, dst_dir: Path) -> Path:
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    if dst.exists():
        if files_identical(src, dst):
            return dst
        stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        dst = dst_dir / f"{src.stem}_{stamp}{src.suffix}"
    shutil.copy2(src, dst)
    return dst


def write_log_excerpt_file(dst: Path, excerpt_text: str) -> Path:
    excerpt_path = dst.with_name(f"{dst.stem}__excerpt.txt")
    excerpt_path.write_text(excerpt_text, encoding="utf-8")
    return excerpt_path


def resolve_archive_root(spec: FamilySpec, archive_tag: str) -> Optional[Path]:
    tag = str(archive_tag or "").strip()
    if not tag:
        return None
    return ARTIFACT_ROOT / spec.name / "validation_matrix" / tag


def resolve_repo_target_dir(spec: FamilySpec, kind: str, archive_tag: str) -> Path:
    archive_root = resolve_archive_root(spec, archive_tag)
    if archive_root is None:
        return spec.repo_dirs[kind]
    kind_dir = {"csv": "csv", "report": "report", "log": "log"}[kind]
    return archive_root / kind_dir


def read_json_object(path: Path) -> dict[str, Any]:
    if not path.exists() or not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if isinstance(data, dict):
        return cast(dict[str, Any], data)
    return {}


def json_object_member(mapping: dict[str, Any], key: str) -> dict[str, Any]:
    value = mapping.get(key)
    if isinstance(value, dict):
        return cast(dict[str, Any], value)
    return {}


def json_object_list_member(mapping: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = mapping.get(key)
    if not isinstance(value, list):
        return []
    result: list[dict[str, Any]] = []
    for raw_item in cast(list[Any], value):
        if isinstance(raw_item, dict):
            result.append(cast(dict[str, Any], raw_item))
    return result


def list_child_dirs(path: Path) -> list[Path]:
    result: list[Path] = []
    if not path.exists() or not path.is_dir():
        return result
    for child in path.iterdir():
        if child.is_dir():
            result.append(child)
    return result


def count_files_in_dir(path: Path) -> int:
    if not path.exists() or not path.is_dir():
        return 0
    count = 0
    for child in path.iterdir():
        if child.is_file():
            count += 1
    return count


_TERMINAL_HASH_RE = re.compile(r"MetaQuotes\\Terminal\\([0-9A-Fa-f]{32})\\")


def extract_terminal_data_root_hash(value: str) -> str:
    match = _TERMINAL_HASH_RE.search(value)
    if match is None:
        return ""
    return match.group(1).upper()


def load_mt5_environment_inventory_by_hash() -> dict[str, dict[str, str]]:
    payload = read_json_object(ENVIRONMENT_INVENTORY_LATEST)
    items = payload.get("items")
    if not isinstance(items, list):
        return {}
    out: dict[str, dict[str, str]] = {}
    for raw_item in cast(list[Any], items):
        if not isinstance(raw_item, dict):
            continue
        item = cast(dict[str, Any], raw_item)
        platform = str(item.get("platform", "")).strip().lower()
        if platform != "mt5":
            continue
        data_root_hash = str(item.get("data_root_hash", "")).strip().upper()
        if not data_root_hash:
            continue
        out[data_root_hash] = {
            "environment_label": str(item.get("environment_label", "")).strip(),
            "server": str(item.get("server", "")).strip(),
            "login": str(item.get("login", "")).strip(),
            "access_server": str(item.get("access_server", "")).strip(),
        }
    return out


def infer_mt5_data_root_hash_from_run_summary(run_summary: dict[str, Any]) -> str:
    files_obj = json_object_member(run_summary, "files")
    for file_meta in files_obj.values():
        if not isinstance(file_meta, dict):
            continue
        meta = cast(dict[str, Any], file_meta)
        source = str(meta.get("source", "")).strip()
        if not source:
            continue
        inferred = extract_terminal_data_root_hash(source)
        if inferred:
            return inferred
    return ""


def build_validation_matrix_index_for_family(family: str) -> dict[str, Any]:
    spec = FAMILY_SPECS[family]
    validation_matrix_root = ARTIFACT_ROOT / spec.name / "validation_matrix"
    archive_dirs = list_child_dirs(validation_matrix_root)
    decorated: list[tuple[float, Path]] = []
    for archive_dir in archive_dirs:
        run_summary_path = archive_dir / "run_summary.json"
        if run_summary_path.exists():
            decorated.append((run_summary_path.stat().st_mtime, archive_dir))
        else:
            decorated.append((archive_dir.stat().st_mtime, archive_dir))
    decorated.sort(key=lambda item: item[0], reverse=True)
    archive_dirs = [item[1] for item in decorated]

    inventory_by_hash = load_mt5_environment_inventory_by_hash()
    archives: list[dict[str, Any]] = []
    summary_archive_count = 0
    manifest_archive_count = 0
    environment_inferred_count = 0
    selection_mode_missing_count = 0
    selection_mode_missing_archive_tags: list[str] = []
    manifest_source_backed_archive_count = 0
    manifest_full_source_backed_archive_count = 0
    manifest_mixed_provenance_archive_count = 0
    manifest_repo_existing_only_archive_count = 0
    environment_labels_seen: list[str] = []
    inventory_environment_labels: list[str] = []
    for inventory_item in inventory_by_hash.values():
        inventory_label = str(inventory_item.get("environment_label", "")).strip()
        if inventory_label and inventory_label not in inventory_environment_labels:
            inventory_environment_labels.append(inventory_label)
    latest_archive_tag = ""
    latest_archive_root = ""
    latest_selection_mode = ""
    latest_environment_label = ""
    latest_manifest_record_count = 0
    latest_manifest_kinds: list[str] = []
    latest_manifest_source_record_count = 0
    latest_manifest_repo_existing_record_count = 0
    latest_manifest_fresh_run_index_record_count = 0
    latest_manifest_historical_recovered_record_count = 0
    latest_manifest_has_source_backed_records = False
    latest_manifest_is_full_source_backed = False
    latest_manifest_is_mixed_provenance = False
    latest_manifest_is_repo_existing_only = False
    latest_run_summary_path = ""
    latest_ingest_manifest_path = ""
    latest_run_summary_present = False
    latest_ingest_manifest_present = False
    recommended_cross_environment_seed_score = -1
    recommended_cross_environment_seed_archive_tag = ""
    recommended_cross_environment_seed_symbol = ""
    recommended_cross_environment_seed_chart_period = ""
    recommended_cross_environment_seed_indicator_period = ""
    recommended_cross_environment_seed_from_date = ""
    recommended_cross_environment_seed_to_date = ""
    recommended_cross_environment_seed_report_stem = ""
    recommended_cross_environment_seed_selection_mode = ""

    for archive_dir in archive_dirs:
        run_summary_path = archive_dir / "run_summary.json"
        ingest_manifest_path = archive_dir / "ingest_manifest.json"
        run_summary = read_json_object(run_summary_path)
        ingest_manifest = read_json_object(ingest_manifest_path)
        environment = json_object_member(run_summary, "environment")
        manifest_records = json_object_list_member(ingest_manifest, "records")
        environment_inferred = False

        selection_mode_value = str(environment.get("selection_mode", "")).strip()
        selection_mode_missing = not bool(selection_mode_value)
        if selection_mode_missing:
            selection_mode_missing_count += 1
            if len(selection_mode_missing_archive_tags) < 30:
                selection_mode_missing_archive_tags.append(archive_dir.name)

        env_data_root_hash = str(environment.get("data_root_hash", "")).strip().upper()
        if not env_data_root_hash:
            env_data_root_hash = infer_mt5_data_root_hash_from_run_summary(run_summary)
            if env_data_root_hash:
                environment_inferred = True

        env_label = str(environment.get("environment_label", "")).strip()
        env_server = str(environment.get("server", "")).strip()
        env_login = str(environment.get("login", "")).strip()
        env_access_server = str(environment.get("access_server", "")).strip()
        if env_data_root_hash and env_data_root_hash in inventory_by_hash:
            inventory_item = inventory_by_hash[env_data_root_hash]
            if not env_label and inventory_item.get("environment_label"):
                env_label = inventory_item["environment_label"]
                environment_inferred = True
            if not env_server and inventory_item.get("server"):
                env_server = inventory_item["server"]
                environment_inferred = True
            if not env_login and inventory_item.get("login"):
                env_login = inventory_item["login"]
                environment_inferred = True
            if not env_access_server and inventory_item.get("access_server"):
                env_access_server = inventory_item["access_server"]
                environment_inferred = True

        if environment_inferred:
            environment_inferred_count += 1
        if env_label and env_label not in environment_labels_seen:
            environment_labels_seen.append(env_label)

        manifest_kinds: list[str] = []
        manifest_source_record_count = 0
        manifest_repo_existing_record_count = 0
        manifest_fresh_run_index_record_count = 0
        manifest_historical_recovered_record_count = 0
        for record in manifest_records:
            kind_value = str(record.get("kind", "")).strip()
            if kind_value and kind_value not in manifest_kinds:
                manifest_kinds.append(kind_value)
            source_path_value = str(record.get("source_path", "")).strip()
            evidence_mode_value = str(record.get("evidence_mode", "")).strip()
            if source_path_value:
                manifest_source_record_count += 1
            else:
                manifest_repo_existing_record_count += 1
            if evidence_mode_value == "fresh_run_index":
                manifest_fresh_run_index_record_count += 1
            elif evidence_mode_value == "historical_recovered":
                manifest_historical_recovered_record_count += 1

        manifest_has_source_backed_records = manifest_source_record_count > 0
        manifest_is_full_source_backed = bool(manifest_records) and manifest_source_record_count == len(manifest_records)
        manifest_is_mixed_provenance = manifest_source_record_count > 0 and manifest_repo_existing_record_count > 0
        manifest_is_repo_existing_only = bool(manifest_records) and manifest_source_record_count == 0
        if manifest_has_source_backed_records:
            manifest_source_backed_archive_count += 1
        if manifest_is_full_source_backed:
            manifest_full_source_backed_archive_count += 1
        if manifest_is_mixed_provenance:
            manifest_mixed_provenance_archive_count += 1
        if manifest_is_repo_existing_only:
            manifest_repo_existing_only_archive_count += 1

        csv_dir = archive_dir / "csv"
        report_dir = archive_dir / "report"
        log_dir = archive_dir / "log"
        archive_mtime_ts = run_summary_path.stat().st_mtime if run_summary_path.exists() else archive_dir.stat().st_mtime
        archive_info: dict[str, Any] = {
            "archive_tag": archive_dir.name,
            "archive_root": str(archive_dir.resolve()),
            "archive_mtime": datetime.fromtimestamp(archive_mtime_ts).isoformat(timespec="seconds"),
            "has_run_summary": run_summary_path.exists(),
            "run_summary_path": str(run_summary_path.resolve()) if run_summary_path.exists() else "",
            "has_ingest_manifest": ingest_manifest_path.exists(),
            "ingest_manifest_path": str(ingest_manifest_path.resolve()) if ingest_manifest_path.exists() else "",
            "symbol": str(run_summary.get("symbol", "")).strip(),
            "chart_period": str(run_summary.get("chart_period", "")).strip(),
            "indicator_period": str(run_summary.get("indicator_period", "")).strip(),
            "from_date": str(run_summary.get("from_date", "")).strip(),
            "to_date": str(run_summary.get("to_date", "")).strip(),
            "report_stem": str(run_summary.get("report_stem", "")).strip(),
            "selection_mode": selection_mode_value,
            "selection_mode_missing": selection_mode_missing,
            "environment_label": env_label,
            "environment_server": env_server,
            "environment_login": env_login,
            "environment_access_server": env_access_server,
            "environment_data_root_hash": env_data_root_hash,
            "environment_inferred": environment_inferred,
            "manifest_record_count": len(manifest_records),
            "manifest_kinds": manifest_kinds,
            "manifest_source_record_count": manifest_source_record_count,
            "manifest_repo_existing_record_count": manifest_repo_existing_record_count,
            "manifest_fresh_run_index_record_count": manifest_fresh_run_index_record_count,
            "manifest_historical_recovered_record_count": manifest_historical_recovered_record_count,
            "manifest_has_source_backed_records": manifest_has_source_backed_records,
            "manifest_is_full_source_backed": manifest_is_full_source_backed,
            "manifest_is_mixed_provenance": manifest_is_mixed_provenance,
            "manifest_is_repo_existing_only": manifest_is_repo_existing_only,
            "csv_file_count": count_files_in_dir(csv_dir),
            "report_file_count": count_files_in_dir(report_dir),
            "log_file_count": count_files_in_dir(log_dir),
        }
        seed_score = 0
        if archive_info["selection_mode"] == "inventory_selector":
            seed_score += 40
        elif archive_info["selection_mode"] == "data_root_override":
            seed_score += 25
        elif not archive_info["selection_mode_missing"]:
            seed_score += 10
        if archive_info["manifest_has_source_backed_records"]:
            seed_score += 20
        if archive_info["has_run_summary"] and archive_info["has_ingest_manifest"]:
            seed_score += 10
        if archive_info["csv_file_count"] >= 1 and archive_info["report_file_count"] >= 1 and archive_info["log_file_count"] >= 2:
            seed_score += 10
        if archive_info["environment_label"]:
            seed_score += 5
        if archive_info["from_date"] and archive_info["to_date"]:
            seed_score += 5
        archive_info["cross_environment_seed_score"] = seed_score
        archives.append(archive_info)

        if archive_info["has_run_summary"]:
            summary_archive_count += 1
        if archive_info["has_ingest_manifest"]:
            manifest_archive_count += 1

        if not latest_archive_tag:
            latest_archive_tag = archive_info["archive_tag"]
            latest_archive_root = archive_info["archive_root"]
            latest_selection_mode = archive_info["selection_mode"]
            latest_environment_label = archive_info["environment_label"]
            latest_manifest_record_count = archive_info["manifest_record_count"]
            latest_manifest_kinds = list(archive_info["manifest_kinds"])
            latest_manifest_source_record_count = archive_info["manifest_source_record_count"]
            latest_manifest_repo_existing_record_count = archive_info["manifest_repo_existing_record_count"]
            latest_manifest_fresh_run_index_record_count = archive_info["manifest_fresh_run_index_record_count"]
            latest_manifest_historical_recovered_record_count = archive_info[
                "manifest_historical_recovered_record_count"
            ]
            latest_manifest_has_source_backed_records = bool(archive_info["manifest_has_source_backed_records"])
            latest_manifest_is_full_source_backed = bool(archive_info["manifest_is_full_source_backed"])
            latest_manifest_is_mixed_provenance = bool(archive_info["manifest_is_mixed_provenance"])
            latest_manifest_is_repo_existing_only = bool(archive_info["manifest_is_repo_existing_only"])
            latest_run_summary_path = archive_info["run_summary_path"]
            latest_ingest_manifest_path = archive_info["ingest_manifest_path"]
            latest_run_summary_present = bool(archive_info["has_run_summary"])
            latest_ingest_manifest_present = bool(archive_info["has_ingest_manifest"])
        if seed_score > recommended_cross_environment_seed_score:
            recommended_cross_environment_seed_score = seed_score
            recommended_cross_environment_seed_archive_tag = archive_info["archive_tag"]
            recommended_cross_environment_seed_symbol = archive_info["symbol"]
            recommended_cross_environment_seed_chart_period = archive_info["chart_period"]
            recommended_cross_environment_seed_indicator_period = archive_info["indicator_period"]
            recommended_cross_environment_seed_from_date = archive_info["from_date"]
            recommended_cross_environment_seed_to_date = archive_info["to_date"]
            recommended_cross_environment_seed_report_stem = archive_info["report_stem"]
            recommended_cross_environment_seed_selection_mode = archive_info["selection_mode"]

    return {
        "format": "validation_matrix_index_v1",
        "family": spec.name,
        "validation_matrix_root": str(validation_matrix_root.resolve()),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "environment_inventory_snapshot": str(ENVIRONMENT_INVENTORY_LATEST.resolve())
        if ENVIRONMENT_INVENTORY_LATEST.exists()
        else "",
        "archive_count": len(archives),
        "summary_archive_count": summary_archive_count,
        "manifest_archive_count": manifest_archive_count,
        "environment_inferred_count": environment_inferred_count,
        "selection_mode_missing_count": selection_mode_missing_count,
        "selection_mode_missing_archive_tags": selection_mode_missing_archive_tags,
        "manifest_source_backed_archive_count": manifest_source_backed_archive_count,
        "manifest_full_source_backed_archive_count": manifest_full_source_backed_archive_count,
        "manifest_mixed_provenance_archive_count": manifest_mixed_provenance_archive_count,
        "manifest_repo_existing_only_archive_count": manifest_repo_existing_only_archive_count,
        "inventory_mt5_environment_count": len(inventory_environment_labels),
        "inventory_mt5_environment_labels": inventory_environment_labels,
        "validation_matrix_environment_label_count": len(environment_labels_seen),
        "validation_matrix_environment_labels": environment_labels_seen,
        "cross_environment_ready": len(inventory_environment_labels) >= 2,
        "cross_environment_verified": len(environment_labels_seen) >= 2,
        "recommended_cross_environment_seed_score": recommended_cross_environment_seed_score,
        "recommended_cross_environment_seed_archive_tag": recommended_cross_environment_seed_archive_tag,
        "recommended_cross_environment_seed_symbol": recommended_cross_environment_seed_symbol,
        "recommended_cross_environment_seed_chart_period": recommended_cross_environment_seed_chart_period,
        "recommended_cross_environment_seed_indicator_period": recommended_cross_environment_seed_indicator_period,
        "recommended_cross_environment_seed_from_date": recommended_cross_environment_seed_from_date,
        "recommended_cross_environment_seed_to_date": recommended_cross_environment_seed_to_date,
        "recommended_cross_environment_seed_report_stem": recommended_cross_environment_seed_report_stem,
        "recommended_cross_environment_seed_selection_mode": recommended_cross_environment_seed_selection_mode,
        "latest_archive_tag": latest_archive_tag,
        "latest_archive_root": latest_archive_root,
        "latest_run_summary_path": latest_run_summary_path,
        "latest_run_summary_present": latest_run_summary_present,
        "latest_ingest_manifest_path": latest_ingest_manifest_path,
        "latest_ingest_manifest_present": latest_ingest_manifest_present,
        "latest_selection_mode": latest_selection_mode,
        "latest_environment_label": latest_environment_label,
        "latest_manifest_record_count": latest_manifest_record_count,
        "latest_manifest_kinds": latest_manifest_kinds,
        "latest_manifest_source_record_count": latest_manifest_source_record_count,
        "latest_manifest_repo_existing_record_count": latest_manifest_repo_existing_record_count,
        "latest_manifest_fresh_run_index_record_count": latest_manifest_fresh_run_index_record_count,
        "latest_manifest_historical_recovered_record_count": latest_manifest_historical_recovered_record_count,
        "latest_manifest_has_source_backed_records": latest_manifest_has_source_backed_records,
        "latest_manifest_is_full_source_backed": latest_manifest_is_full_source_backed,
        "latest_manifest_is_mixed_provenance": latest_manifest_is_mixed_provenance,
        "latest_manifest_is_repo_existing_only": latest_manifest_is_repo_existing_only,
        "archives": archives,
    }


def write_validation_matrix_index_for_family(family: str) -> Path:
    spec = FAMILY_SPECS[family]
    validation_matrix_root = ARTIFACT_ROOT / spec.name / "validation_matrix"
    validation_matrix_root.mkdir(parents=True, exist_ok=True)
    payload = build_validation_matrix_index_for_family(family)
    index_path = validation_matrix_root / "validation_matrix_index_latest.json"
    index_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    return index_path


def backfill_ingest_manifest_from_archive(spec: FamilySpec, archive_tag: str) -> Path:
    archive_root = resolve_archive_root(spec, archive_tag)
    if archive_root is None:
        raise FileNotFoundError(f"archive root not found for tag: {archive_tag}")

    run_summary_path = archive_root / "run_summary.json"
    run_summary: dict[str, Any] = {}
    if run_summary_path.exists():
        run_summary = read_json_object(run_summary_path)
    sources_by_basename: dict[str, list[str]] = {}
    if run_summary:
        files_obj = run_summary.get("files")
        if isinstance(files_obj, dict):
            for file_meta in files_obj.values():
                if not isinstance(file_meta, dict):
                    continue
                meta = cast(dict[str, Any], file_meta)
                source = str(meta.get("source", "")).strip()
                if not source:
                    continue
                base = Path(source).name.strip().lower()
                if base:
                    sources_by_basename.setdefault(base, []).append(source)

    manifest_path = archive_root / "ingest_manifest.json"
    payload = read_json_object(manifest_path)
    records = json_object_list_member(payload, "records")

    existing_by_key: dict[tuple[str, str], int] = {}
    for idx, existing in enumerate(records):
        kind_value = str(existing.get("kind", "")).strip()
        repo_path_value = str(existing.get("repo_path", "")).strip()
        if kind_value and repo_path_value:
            existing_by_key[(kind_value, repo_path_value)] = idx

    discovered: list[dict[str, Any]] = []
    kind_dir_pairs = [
        ("csv", archive_root / "csv"),
        ("report", archive_root / "report"),
        ("log", archive_root / "log"),
        ("runtime_config", archive_root / "runtime_config"),
    ]

    now_stamp = datetime.now().isoformat(timespec="seconds")
    for kind, dir_path in kind_dir_pairs:
        if not dir_path.exists() or not dir_path.is_dir():
            continue
        for child in dir_path.iterdir():
            if not child.is_file():
                continue
            inferred_source_path = ""
            source_stat_path = child
            evidence_mode = "historical_recovered"
            note = "backfilled from repo archive directory; original source unknown"
            candidates = sources_by_basename.get(child.name.strip().lower(), []) if sources_by_basename else []
            if candidates:
                existing_candidates: list[Path] = []
                for value in candidates:
                    candidate_path = Path(value)
                    if candidate_path.exists() and candidate_path.is_file():
                        existing_candidates.append(candidate_path)

                if len(existing_candidates) == 1:
                    inferred_source_path = str(existing_candidates[0])
                    source_stat_path = existing_candidates[0]
                    evidence_mode = "fresh_run_index"
                    note = "backfilled from repo archive directory; source inferred from run_summary.json"
                elif len(existing_candidates) > 1:
                    target_size = child.stat().st_size
                    best = min(existing_candidates, key=lambda p: abs(p.stat().st_size - target_size))
                    inferred_source_path = str(best)
                    source_stat_path = best
                    evidence_mode = "fresh_run_index"
                    note = "backfilled from repo archive directory; source inferred from run_summary.json (multiple candidates; picked closest size)"
                else:
                    inferred_source_path = str(candidates[0]).strip()
                    evidence_mode = "fresh_run_index"
                    note = "backfilled from repo archive directory; source inferred from run_summary.json (source missing; using archive file metadata)"
            repo_path = str(child.resolve())
            record: dict[str, Any] = {
                "family": spec.name,
                "kind": kind,
                "archive_tag": archive_tag,
                "copied_at": now_stamp,
                "selection_mode": "run_summary" if inferred_source_path else "repo_existing",
                "source_path": inferred_source_path,
                "source_mtime": datetime.fromtimestamp(source_stat_path.stat().st_mtime).isoformat(timespec="seconds"),
                "source_size": source_stat_path.stat().st_size,
                "repo_target_dir": str(dir_path.resolve()),
                "repo_path": repo_path,
                "matched_keywords": [],
                "matched_filename_keywords": [],
                "log_keyword_override": [],
                "log_filename_keywords": [],
                "log_tail_lines": 0,
                "excerpt_path": "",
                "evidence_mode": evidence_mode,
                "note": note,
            }
            discovered.append(record)

    for record in discovered:
        key = (str(record.get("kind", "")).strip(), str(record.get("repo_path", "")).strip())
        if not key[0] or not key[1]:
            continue
        if key in existing_by_key:
            records[existing_by_key[key]] = record
        else:
            existing_by_key[key] = len(records)
            records.append(record)

    output = {
        "format": "probe_artifact_ingest_manifest_v1",
        "family": spec.name,
        "archive_tag": archive_tag,
        "archive_root": str(archive_root.resolve()),
        "updated_at": now_stamp,
        "records": records,
    }
    manifest_path.write_text(json.dumps(output, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def backfill_missing_ingest_manifests(spec: FamilySpec, limit: int = 0) -> list[Path]:
    validation_matrix_root = ARTIFACT_ROOT / spec.name / "validation_matrix"
    archive_dirs = list_child_dirs(validation_matrix_root)
    archive_dirs.sort(key=lambda p: p.stat().st_mtime, reverse=True)

    created: list[Path] = []
    for archive_dir in archive_dirs:
        manifest_path = archive_dir / "ingest_manifest.json"
        if manifest_path.exists():
            continue
        created.append(backfill_ingest_manifest_from_archive(spec, archive_dir.name))
        if limit > 0 and len(created) >= limit:
            break
    return created


def write_archive_ingest_manifest(
    spec: FamilySpec,
    archive_tag: str,
    kind: str,
    selected: MatchInfo,
    repo_target_dir: Path,
    copied_to: Path,
    args: argparse.Namespace,
    excerpt_path: Optional[Path],
) -> Optional[Path]:
    archive_root = resolve_archive_root(spec, archive_tag)
    if archive_root is None:
        return None

    manifest_path = archive_root / "ingest_manifest.json"
    payload = read_json_object(manifest_path)
    records = json_object_list_member(payload, "records")

    source_path = str(selected.path.resolve())
    copied_to_path = str(copied_to.resolve())
    record = {
        "family": spec.name,
        "kind": kind,
        "archive_tag": archive_tag,
        "copied_at": datetime.now().isoformat(timespec="seconds"),
        "selection_mode": "source" if args.source else "copy_latest",
        "source_path": source_path,
        "source_mtime": datetime.fromtimestamp(selected.path.stat().st_mtime).isoformat(timespec="seconds"),
        "source_size": selected.path.stat().st_size,
        "repo_target_dir": str(repo_target_dir.resolve()),
        "repo_path": copied_to_path,
        "matched_keywords": list(selected.matched_keywords),
        "matched_filename_keywords": list(selected.matched_filename_keywords),
        "log_keyword_override": list(args.log_keyword),
        "log_filename_keywords": list(args.log_filename_keyword),
        "log_tail_lines": args.log_tail_lines,
        "excerpt_path": str(excerpt_path.resolve()) if excerpt_path is not None else "",
    }

    updated = False
    for idx, existing in enumerate(records):
        if existing.get("kind") == kind and existing.get("source_path") == source_path:
            records[idx] = record
            updated = True
            break
    if not updated:
        records.append(record)

    payload["format"] = "probe_artifact_ingest_manifest_v1"
    payload["family"] = spec.name
    payload["archive_tag"] = archive_tag
    payload["archive_root"] = str(archive_root.resolve())
    payload["updated_at"] = datetime.now().isoformat(timespec="seconds")
    payload["records"] = sorted(records, key=lambda item: (str(item.get("kind", "")), str(item.get("source_path", ""))))
    manifest_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    return manifest_path


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
    parser.add_argument("--kind", default="", choices=("csv", "report", "log"))
    parser.add_argument("--list", action="store_true", help="list candidate files only")
    parser.add_argument("--copy-latest", action="store_true", help="copy latest matched file into batch artifacts")
    parser.add_argument("--source", default="", help="copy an explicit source path instead of auto-selecting latest")
    parser.add_argument(
        "--archive-tag",
        default="",
        help="if set, copy into artifacts/<family>/validation_matrix/<archive_tag>/<kind>/ instead of the default batch artifacts dir",
    )
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
    parser.add_argument(
        "--write-validation-matrix-index",
        action="store_true",
        help="write artifacts/<family>/validation_matrix/validation_matrix_index_latest.json",
    )
    parser.add_argument(
        "--backfill-ingest-manifest-from-archive",
        action="store_true",
        help="for --archive-tag, write ingest_manifest.json by scanning existing archive directory; infer source_path from run_summary.json when present",
    )
    parser.add_argument(
        "--backfill-missing-ingest-manifests",
        action="store_true",
        help="scan artifacts/<family>/validation_matrix/* and backfill missing ingest_manifest.json (historical_recovered)",
    )
    parser.add_argument(
        "--backfill-limit",
        type=int,
        default=0,
        help="when used with --backfill-missing-ingest-manifests, limit number of archives to backfill; 0 means all",
    )
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

    if args.write_validation_matrix_index and not args.list and not args.copy_latest and not args.source:
        index_path = write_validation_matrix_index_for_family(args.family)
        print("format=validation_matrix_index_v1")
        print(f"family={spec.name}")
        print(f"validation_matrix_index={index_path}")
        return

    if args.backfill_ingest_manifest_from_archive:
        if not args.archive_tag:
            raise SystemExit("--backfill-ingest-manifest-from-archive requires --archive-tag")
        manifest_path = backfill_ingest_manifest_from_archive(spec, args.archive_tag)
        print("format=probe_artifact_ingest_manifest_v1")
        print(f"family={spec.name}")
        print(f"archive_tag={args.archive_tag}")
        print(f"ingest_manifest={manifest_path}")
        index_path = write_validation_matrix_index_for_family(spec.name)
        print(f"validation_matrix_index={index_path}")
        return

    if args.backfill_missing_ingest_manifests:
        created = backfill_missing_ingest_manifests(spec, max(args.backfill_limit, 0))
        index_path = write_validation_matrix_index_for_family(spec.name)
        print("format=probe_artifact_ingest_manifest_bulk_backfill_v1")
        print(f"family={spec.name}")
        print(f"backfill_count={len(created)}")
        print("backfilled_manifests={0}".format(json.dumps([str(p) for p in created], ensure_ascii=True)))
        print(f"validation_matrix_index={index_path}")
        return

    if (args.list or args.copy_latest or args.source) and not args.kind:
        raise SystemExit("--list/--copy-latest/--source requires --kind {csv,report,log}")

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

    repo_target_dir = resolve_repo_target_dir(spec, args.kind, args.archive_tag)
    dst = safe_copy(selected.path, repo_target_dir)
    excerpt_path: Optional[Path] = None
    print(f"family={spec.name}")
    print(f"kind={args.kind}")
    print(f"repo_target={repo_target_dir.resolve()}")
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
    manifest_path = write_archive_ingest_manifest(
        spec=spec,
        archive_tag=args.archive_tag,
        kind=args.kind,
        selected=selected,
        repo_target_dir=repo_target_dir,
        copied_to=dst,
        args=args,
        excerpt_path=excerpt_path,
    )
    print(f"source={selected.path}")
    print(f"copied_to={dst}")
    if manifest_path is not None:
        print(f"ingest_manifest={manifest_path}")
    if args.archive_tag:
        index_path = write_validation_matrix_index_for_family(spec.name)
        print(f"validation_matrix_index={index_path}")


if __name__ == "__main__":
    main()
