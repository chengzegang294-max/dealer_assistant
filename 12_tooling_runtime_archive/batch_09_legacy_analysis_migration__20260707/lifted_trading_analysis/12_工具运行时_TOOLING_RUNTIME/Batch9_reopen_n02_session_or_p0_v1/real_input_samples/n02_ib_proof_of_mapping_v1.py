from __future__ import annotations

import argparse
import csv
import glob
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from collections import defaultdict

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None


DEFAULT_INPUT = Path(__file__).resolve().parent / "n02_first_real_input_bars_v1.csv"
DEFAULT_CONFIG = Path(__file__).resolve().parent / "n02_or_proof_config_v1.json"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "n02_ib_proof_of_mapping_output_v1.csv"


OUTPUT_COLUMNS = [
    "symbol",
    "timeframe",
    "session_id",
    "session_timezone",
    "session_local_date",
    "ib_window_minutes",
    "ib_start_utc",
    "ib_end_utc",
    "ib_high",
    "ib_low",
    "ib_range",
    "ib_mid",
    "bars_in_ib_window",
    "ib_defined",
]


@dataclass(frozen=True)
class Bar:
    symbol: str
    timeframe: str
    dt_utc: datetime
    open: float
    high: float
    low: float
    close: float


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_iso_utc(value: str) -> datetime:
    dt = datetime.strptime(value.strip(), "%Y-%m-%dT%H:%M:%SZ")
    return dt.replace(tzinfo=timezone.utc)


def parse_float(value: str) -> float:
    return float(value.strip())


def read_bars(path: Path) -> list[Bar]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        bars: list[Bar] = []
        for row in reader:
            bars.append(
                Bar(
                    symbol=row["symbol"],
                    timeframe=row["timeframe"],
                    dt_utc=parse_iso_utc(row["bar_time"]),
                    open=parse_float(row["open"]),
                    high=parse_float(row["high"]),
                    low=parse_float(row["low"]),
                    close=parse_float(row["close"]),
                )
            )
    bars.sort(key=lambda b: b.dt_utc)
    return bars


def has_glob_chars(value: str) -> bool:
    return any(ch in value for ch in ["*", "?", "["])


def resolve_input_paths(patterns: list[str], base_dir: Path) -> list[Path]:
    resolved: list[Path] = []
    for raw in patterns:
        s = str(raw).strip()
        if not s:
            continue

        p = Path(s)
        if not p.is_absolute():
            p = base_dir / p

        if has_glob_chars(str(p)):
            matches = [Path(x) for x in glob.glob(str(p), recursive=True)]
            for m in sorted(matches):
                if m.is_file():
                    resolved.append(m)
            continue

        if not p.is_file():
            raise FileNotFoundError(str(p))
        resolved.append(p)

    deduped: dict[str, Path] = {}
    for p in resolved:
        deduped[str(p.resolve())] = p
    return [deduped[k] for k in sorted(deduped.keys())]


def read_bars_many(paths: list[Path]) -> list[Bar]:
    bars: list[Bar] = []
    for p in paths:
        bars.extend(read_bars(p))

    deduped: dict[tuple[str, str, datetime], Bar] = {}
    for b in bars:
        deduped[(b.symbol, b.timeframe, b.dt_utc)] = b

    out = list(deduped.values())
    out.sort(key=lambda b: (b.symbol, b.timeframe, b.dt_utc))
    return out


def parse_session_input_specs(values: list[str]) -> dict[str, list[str]]:
    by_session: dict[str, list[str]] = defaultdict(list)
    for raw in values:
        s = str(raw).strip()
        if not s:
            continue
        if "=" not in s:
            raise ValueError("invalid --session-input (expected session_id=path): {0}".format(s))
        session_id, path = s.split("=", 1)
        session_id = session_id.strip()
        path = path.strip()
        if not session_id or not path:
            raise ValueError("invalid --session-input (expected session_id=path): {0}".format(s))
        by_session[session_id].append(path)
    return dict(by_session)


def build_groups(
    bars: list[Bar],
    symbol_filter: str,
    timeframe_filter: str,
) -> dict[tuple[str, str], list[Bar]]:
    groups: dict[tuple[str, str], list[Bar]] = {}
    for b in bars:
        if symbol_filter and b.symbol != symbol_filter:
            continue
        if timeframe_filter and b.timeframe != timeframe_filter:
            continue
        groups.setdefault((b.symbol, b.timeframe), []).append(b)
    for k in list(groups.keys()):
        groups[k].sort(key=lambda x: x.dt_utc)
    return groups


def parse_hhmm(value: str) -> tuple[int, int]:
    parts = value.strip().split(":")
    if len(parts) != 2:
        raise ValueError("invalid hh:mm: {0}".format(value))
    return int(parts[0]), int(parts[1])


def fmt_utc(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fmt_num(value: float, decimals: int) -> str:
    return ("{0:0." + str(decimals) + "f}").format(value)


def safe_zoneinfo(name: str) -> ZoneInfo:
    if ZoneInfo is None:
        raise RuntimeError("zoneinfo is not available; cannot convert timezones safely")
    return ZoneInfo(name)


def build_local_date_bins(bars: list[Bar], session_timezone: str) -> dict[str, list[Bar]]:
    tz = safe_zoneinfo(session_timezone)
    bins: dict[str, list[Bar]] = {}
    for b in bars:
        local_date = b.dt_utc.astimezone(tz).strftime("%Y-%m-%d")
        bins.setdefault(local_date, []).append(b)
    for k in list(bins.keys()):
        bins[k].sort(key=lambda x: x.dt_utc)
    return bins


def compute_ib_for_local_date(
    bars_for_date: list[Bar],
    session_timezone: str,
    session_open_local_hhmm: str,
    ib_window_minutes: int,
    skip_partial_days: bool,
) -> dict | None:
    tz = safe_zoneinfo(session_timezone)
    h, m = parse_hhmm(session_open_local_hhmm)
    local_date = bars_for_date[0].dt_utc.astimezone(tz).date()
    local_open = datetime(local_date.year, local_date.month, local_date.day, h, m, tzinfo=tz)
    ib_start = local_open.astimezone(timezone.utc)
    ib_end = ib_start + timedelta(minutes=int(ib_window_minutes))

    window = [b for b in bars_for_date if ib_start <= b.dt_utc < ib_end]
    if not window:
        if skip_partial_days:
            tf = str(bars_for_date[0].timeframe).strip().upper()
            step: timedelta | None = None
            if tf.startswith("M") and tf[1:].isdigit():
                step = timedelta(minutes=int(tf[1:]))
            elif tf.startswith("H") and tf[1:].isdigit():
                step = timedelta(hours=int(tf[1:]))

            if step is not None:
                if bars_for_date[0].dt_utc > ib_start:
                    return None
                if bars_for_date[-1].dt_utc < (ib_end - step):
                    return None

        return {
            "ib_start_utc": fmt_utc(ib_start),
            "ib_end_utc": fmt_utc(ib_end),
            "ib_high": "",
            "ib_low": "",
            "ib_range": "",
            "ib_mid": "",
            "bars_in_ib_window": "0",
            "ib_defined": "0",
        }

    ib_high = max(b.high for b in window)
    ib_low = min(b.low for b in window)
    ib_range = ib_high - ib_low
    ib_mid = (ib_high + ib_low) / 2.0

    return {
        "ib_start_utc": fmt_utc(ib_start),
        "ib_end_utc": fmt_utc(ib_end),
        "ib_high": fmt_num(ib_high, 5),
        "ib_low": fmt_num(ib_low, 5),
        "ib_range": fmt_num(ib_range, 5),
        "ib_mid": fmt_num(ib_mid, 5),
        "bars_in_ib_window": str(len(window)),
        "ib_defined": "1",
    }


def write_rows(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in OUTPUT_COLUMNS})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--inputs", nargs="*", default=[])
    parser.add_argument("--session-input", action="append", default=[])
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--ib-window-minutes", type=int, default=60)
    parser.add_argument("--session-id", default="")
    parser.add_argument("--symbol", default="")
    parser.add_argument("--timeframe", default="")
    parser.add_argument("--skip-partial-days", action="store_true")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    if args.inputs:
        input_paths = resolve_input_paths([str(x) for x in args.inputs], base_dir=base_dir)
    else:
        input_paths = resolve_input_paths([str(args.input)], base_dir=base_dir)

    bars = read_bars_many(input_paths)
    config = load_json(Path(args.config))
    sessions = config.get("sessions", {})

    requested_session_id = str(args.session_id).strip()
    if requested_session_id:
        sessions = {k: v for k, v in sessions.items() if str(k) == requested_session_id}
        if not sessions:
            raise SystemExit("unknown session_id: {0}".format(requested_session_id))

    rows: list[dict] = []
    symbol_filter = str(args.symbol).strip()
    timeframe_filter = str(args.timeframe).strip()

    session_input_specs = parse_session_input_specs(list(args.session_input))

    for session_id, s in sessions.items():
        tz_name = str(s["session_timezone"])
        open_hhmm = str(s["session_open_local_hhmm"])
        bars_for_session = bars
        if session_input_specs:
            patterns = session_input_specs.get(str(session_id), [])
            if patterns:
                paths = resolve_input_paths(patterns, base_dir=base_dir)
                bars_for_session = read_bars_many(paths)

        groups = build_groups(bars_for_session, symbol_filter=symbol_filter, timeframe_filter=timeframe_filter)
        for (symbol, timeframe), bars_for_group in sorted(groups.items(), key=lambda x: x[0]):
            local_bins = build_local_date_bins(bars_for_group, tz_name)
            for local_date, bars_for_date in sorted(local_bins.items(), key=lambda x: x[0]):
                head = bars_for_date[0]
                core = compute_ib_for_local_date(
                    bars_for_date=bars_for_date,
                    session_timezone=tz_name,
                    session_open_local_hhmm=open_hhmm,
                    ib_window_minutes=int(args.ib_window_minutes),
                    skip_partial_days=bool(args.skip_partial_days),
                )
                if core is None:
                    continue
                rows.append(
                    {
                        "symbol": head.symbol,
                        "timeframe": head.timeframe,
                        "session_id": str(session_id),
                        "session_timezone": tz_name,
                        "session_local_date": local_date,
                        "ib_window_minutes": str(int(args.ib_window_minutes)),
                        **core,
                    }
                )

    write_rows(Path(args.output), rows)
    print("ib_proof_of_mapping_rows={0}".format(len(rows)))
    print("ib_proof_of_mapping_output={0}".format(Path(args.output).resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
