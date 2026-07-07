from __future__ import annotations

import argparse
import csv
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None


RUNTIME_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]
DROP_DIR = REPO_ROOT / "data" / "mt_exports_drop"
DEFAULT_DEST = Path(__file__).resolve().parent / "n02_first_real_input_bars_v1.csv"


CANONICAL_COLUMNS = ["symbol", "timeframe", "bar_time", "open", "high", "low", "close"]


@dataclass(frozen=True)
class ParsedRow:
    dt: datetime
    open: str
    high: str
    low: str
    close: str


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def try_parse_dt(value: str) -> datetime:
    value = value.strip().strip('"').strip("'")
    candidates = [
        "%Y.%m.%d %H:%M:%S",
        "%Y.%m.%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%d.%m.%Y %H:%M:%S",
        "%d.%m.%Y %H:%M",
    ]
    for fmt in candidates:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError("unsupported datetime format: {0}".format(value))


def normalize_header(name: str) -> str:
    return name.strip().strip("\ufeff").lower()


def read_mt5_rows(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        sample = f.read(4096)
        f.seek(0)
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        reader = csv.reader(f, dialect=dialect)
        header = next(reader)
        rows = list(reader)
    return header, rows


def find_metaquotes_files_dir_candidates() -> list[Path]:
    candidates: list[Path] = []
    for env_key in ("APPDATA", "LOCALAPPDATA"):
        base = os.environ.get(env_key)
        if not base:
            continue
        terminal_root = Path(base) / "MetaQuotes" / "Terminal"
        if not terminal_root.exists():
            continue
        for child in terminal_root.iterdir():
            if not child.is_dir():
                continue
            for sub in (Path("MQL5") / "Files", Path("MQL4") / "Files"):
                p = child / sub
                if p.exists() and p.is_dir():
                    candidates.append(p)
    return candidates


def list_drop_csvs(drop_dir: Path, pattern: str) -> list[Path]:
    if not drop_dir.exists():
        return []
    if not drop_dir.is_dir():
        return []
    return sorted([p for p in drop_dir.glob(pattern) if p.is_file()], key=lambda p: p.stat().st_mtime, reverse=True)


def pick_latest_drop_csv(drop_dir: Path, pattern: str) -> Path:
    items = list_drop_csvs(drop_dir, pattern)
    if not items:
        raise FileNotFoundError("no csv found in drop_dir: {0}".format(drop_dir))
    return items[0]


def build_input_not_found_message(input_path: Path) -> str:
    lines: list[str] = []
    lines.append("input csv not found: {0}".format(input_path))
    lines.append("suggestion_1=export your MT4/MT5 csv to an existing folder")
    lines.append("suggestion_2=put the export into: {0}".format(DROP_DIR))
    if DROP_DIR.exists():
        sample = sorted([p.name for p in DROP_DIR.glob("*.csv")])[:20]
        lines.append("drop_dir_exists=true")
        lines.append("drop_dir_csv_sample={0}".format(json.dumps(sample, ensure_ascii=True)))
    else:
        lines.append("drop_dir_exists=false")
    mq_dirs = find_metaquotes_files_dir_candidates()
    if mq_dirs:
        lines.append("metaquotes_files_dirs={0}".format(json.dumps([str(p) for p in mq_dirs[:10]], ensure_ascii=True)))
        base = input_path.name
        matches: list[str] = []
        for d in mq_dirs:
            m = d / base
            if m.exists():
                matches.append(str(m))
        if matches:
            lines.append("metaquotes_match={0}".format(json.dumps(matches[:10], ensure_ascii=True)))
    else:
        lines.append("metaquotes_files_dirs=[]")
    return "\n".join(lines)


def parse_rows(
    header: list[str],
    raw_rows: list[list[str]],
    source_timezone: str,
    date_col: str | None,
    time_col: str,
    open_col: str,
    high_col: str,
    low_col: str,
    close_col: str,
) -> list[ParsedRow]:
    idx = {normalize_header(name): i for i, name in enumerate(header)}
    required = [time_col, open_col, high_col, low_col, close_col]
    for key in required:
        if normalize_header(key) not in idx:
            raise ValueError("missing required column: {0}".format(key))
    if date_col is not None and normalize_header(date_col) not in idx:
        raise ValueError("missing required column: {0}".format(date_col))

    if ZoneInfo is None:
        raise RuntimeError("zoneinfo is not available; cannot convert timezones safely")

    tz = ZoneInfo(source_timezone)
    parsed: list[ParsedRow] = []
    for raw in raw_rows:
        if not raw or len(raw) < len(header):
            continue
        if date_col is None:
            dt_str = raw[idx[normalize_header(time_col)]]
        else:
            dt_str = "{0} {1}".format(
                raw[idx[normalize_header(date_col)]],
                raw[idx[normalize_header(time_col)]],
            )
        dt_naive = try_parse_dt(dt_str)
        dt_local = dt_naive.replace(tzinfo=tz)
        dt_utc = dt_local.astimezone(timezone.utc)
        parsed.append(
            ParsedRow(
                dt=dt_utc,
                open=raw[idx[normalize_header(open_col)]].strip(),
                high=raw[idx[normalize_header(high_col)]].strip(),
                low=raw[idx[normalize_header(low_col)]].strip(),
                close=raw[idx[normalize_header(close_col)]].strip(),
            )
        )
    parsed.sort(key=lambda r: r.dt)
    return parsed


def to_iso_utc(dt: datetime) -> str:
    if dt.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def backup_if_exists(path: Path) -> None:
    if not path.exists():
        return
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    bak = path.with_name("{0}.bak_{1}".format(path.name, ts))
    path.replace(bak)


def write_canonical(
    dest: Path,
    symbol: str,
    timeframe: str,
    rows: list[ParsedRow],
) -> None:
    backup_if_exists(dest)
    with dest.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CANONICAL_COLUMNS)
        writer.writeheader()
        for r in rows:
            writer.writerow(
                {
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "bar_time": to_iso_utc(r.dt),
                    "open": r.open,
                    "high": r.high,
                    "low": r.low,
                    "close": r.close,
                }
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="", help="path to MT4/MT5 exported csv")
    parser.add_argument("--latest", action="store_true")
    parser.add_argument("--drop-dir", default=str(DROP_DIR))
    parser.add_argument("--drop-pattern", default="*.csv")
    parser.add_argument("--list-drop", action="store_true")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--timeframe", required=True)
    parser.add_argument("--source-timezone", required=True)
    parser.add_argument("--dest", default=str(DEFAULT_DEST))
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="parse and print summary without writing output csv",
    )
    parser.add_argument(
        "--schema",
        default="auto",
        choices=["auto", "mt5_standard", "time_only"],
        help="auto tries to detect; mt5_standard expects Date+Time columns; time_only expects Time includes full datetime",
    )
    parser.add_argument(
        "--date-col",
        default="Date",
        help="used when schema is mt5_standard",
    )
    parser.add_argument(
        "--time-col",
        default="Time",
    )
    parser.add_argument("--open-col", default="Open")
    parser.add_argument("--high-col", default="High")
    parser.add_argument("--low-col", default="Low")
    parser.add_argument("--close-col", default="Close")
    args = parser.parse_args()

    drop_dir = Path(args.drop_dir).expanduser().resolve()
    drop_items = list_drop_csvs(drop_dir, str(args.drop_pattern))
    if args.list_drop:
        print("drop_dir={0}".format(drop_dir))
        print("drop_dir_exists={0}".format(str(drop_dir.exists()).lower()))
        print("drop_csv_count={0}".format(len(drop_items)))
        print("drop_csv_sample={0}".format(json.dumps([str(p) for p in drop_items[:20]], ensure_ascii=True)))
        return

    if args.latest:
        input_path = pick_latest_drop_csv(drop_dir, str(args.drop_pattern))
    else:
        raw = str(args.input).strip()
        if not raw:
            raise SystemExit("--input is required unless --latest is set")
        input_path = Path(raw).expanduser().resolve()

    if not input_path.exists():
        raise FileNotFoundError(build_input_not_found_message(input_path))
    dest = Path(args.dest).expanduser().resolve()
    header, raw_rows = read_mt5_rows(input_path)

    header_norm = {normalize_header(h) for h in header}
    detected_schema = args.schema
    if args.schema == "auto":
        if "date" in header_norm and "time" in header_norm:
            detected_schema = "mt5_standard"
        else:
            detected_schema = "time_only"

    date_col = args.date_col if detected_schema == "mt5_standard" else None
    parsed = parse_rows(
        header=header,
        raw_rows=raw_rows,
        source_timezone=args.source_timezone,
        date_col=date_col,
        time_col=args.time_col,
        open_col=args.open_col,
        high_col=args.high_col,
        low_col=args.low_col,
        close_col=args.close_col,
    )

    if not parsed:
        raise ValueError("no rows parsed from input")

    print("input={0}".format(input_path))
    print("drop_dir={0}".format(drop_dir))
    print("drop_pattern={0}".format(args.drop_pattern))
    print("dest={0}".format(dest))
    print("schema={0}".format(detected_schema))
    print("source_timezone={0}".format(args.source_timezone))
    print("header={0}".format(json.dumps(header, ensure_ascii=True)))
    print("rows={0}".format(len(parsed)))
    print("first_bar_time_utc={0}".format(to_iso_utc(parsed[0].dt)))
    print("last_bar_time_utc={0}".format(to_iso_utc(parsed[-1].dt)))

    if args.dry_run:
        print("dry_run_only=true")
        return

    write_canonical(
        dest=dest,
        symbol=args.symbol,
        timeframe=args.timeframe,
        rows=parsed,
    )
    print("written=true")


if __name__ == "__main__":
    main()
