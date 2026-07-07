from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None


DEFAULT_INPUT = Path(__file__).resolve().parent / "n02_first_real_input_bars_v1.csv"
DEFAULT_CONFIG = Path(__file__).resolve().parent / "n02_or_proof_config_v1.json"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "n02_proof_of_mapping_output_v2.csv"


OUTPUT_COLUMNS = [
    "symbol",
    "timeframe",
    "bar_time",
    "session_id",
    "session_timezone",
    "opening_range_window_minutes",
    "opening_range_high",
    "opening_range_low",
    "opening_range_mid",
    "opening_range_width",
    "opening_range_width_pct_open",
    "session_open_price",
    "opening_range_defined",
    "first_break_direction",
    "first_break_mode",
    "width_error_day",
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


@dataclass
class BreakStats:
    close_up: int = 0
    close_down: int = 0
    wick_up: int = 0
    wick_down: int = 0
    ambiguous: int = 0


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_float(value: str) -> float:
    return float(value.strip())


def parse_iso_utc(value: str) -> datetime:
    dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    return dt.replace(tzinfo=timezone.utc)


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


def timeframe_to_minutes(timeframe: str) -> int | None:
    tf = timeframe.strip().upper()
    if tf.startswith("M") and tf[1:].isdigit():
        return int(tf[1:])
    if tf.startswith("H") and tf[1:].isdigit():
        return int(tf[1:]) * 60
    return None


def fmt_price(value: float, decimals: int) -> str:
    return ("{0:0." + str(decimals) + "f}").format(value)


def fmt_num(value: float, decimals: int) -> str:
    return ("{0:0." + str(decimals) + "f}").format(value)


def parse_hhmm(value: str) -> tuple[int, int]:
    parts = value.strip().split(":")
    if len(parts) != 2:
        raise ValueError("invalid hh:mm: {0}".format(value))
    return int(parts[0]), int(parts[1])


def parse_iso_utc_loose(value: str) -> datetime:
    raw = value.strip()
    if raw.endswith("Z"):
        dt = datetime.strptime(raw, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        return dt
    dt = datetime.fromisoformat(raw)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def print_overlap_samples(config: dict, utc_start: str, utc_end: str, step_minutes: int) -> None:
    if ZoneInfo is None:
        raise RuntimeError("zoneinfo is not available; cannot convert timezones safely")
    sessions = config.get("sessions", {})
    dt0 = parse_iso_utc_loose(utc_start)
    dt1 = parse_iso_utc_loose(utc_end)
    if dt1 < dt0:
        raise ValueError("utc_end must be >= utc_start")
    step = timedelta(minutes=int(step_minutes))
    for session_id, s in sessions.items():
        tz_name = str(s["session_timezone"])
        tz = ZoneInfo(tz_name)
        print("overlap_sample_session={0} timezone={1} utc_start={2} utc_end={3} step_minutes={4}".format(session_id, tz_name, dt0.isoformat(), dt1.isoformat(), int(step_minutes)))
        seen_local: dict[str, int] = {}
        cur = dt0
        while cur <= dt1:
            local = cur.astimezone(tz)
            local_key = local.strftime("%Y-%m-%dT%H:%M:%S")
            seen_local[local_key] = seen_local.get(local_key, 0) + 1
            offset = local.utcoffset()
            offset_str = "na" if offset is None else str(offset)
            print(
                "utc={0} local={1} offset={2} local_date={3}".format(
                    cur.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    local.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    offset_str,
                    local.strftime("%Y-%m-%d"),
                )
            )
            cur = cur + step
        repeats = sorted([k for k, v in seen_local.items() if v > 1])
        print("overlap_local_clock_repeats={0}".format(len(repeats)))
        for k in repeats[:10]:
            print("repeat_local_clock={0}".format(k))


def print_local_date_binning_samples(config: dict, utc_start: str, utc_end: str, step_minutes: int) -> None:
    if ZoneInfo is None:
        raise RuntimeError("zoneinfo is not available; cannot convert timezones safely")
    sessions = config.get("sessions", {})
    dt0 = parse_iso_utc_loose(utc_start)
    dt1 = parse_iso_utc_loose(utc_end)
    if dt1 < dt0:
        raise ValueError("utc_end must be >= utc_start")
    step = timedelta(minutes=int(step_minutes))
    for session_id, s in sessions.items():
        tz_name = str(s["session_timezone"])
        tz = ZoneInfo(tz_name)
        print(
            "local_date_binning_session={0} timezone={1} utc_start={2} utc_end={3} step_minutes={4}".format(
                session_id,
                tz_name,
                dt0.strftime("%Y-%m-%dT%H:%M:%SZ"),
                dt1.strftime("%Y-%m-%dT%H:%M:%SZ"),
                int(step_minutes),
            )
        )
        counts: dict[str, int] = {}
        transitions: list[tuple[str, str, str]] = []
        prev_date: str | None = None
        cur = dt0
        while cur <= dt1:
            local = cur.astimezone(tz)
            local_date = local.strftime("%Y-%m-%d")
            counts[local_date] = counts.get(local_date, 0) + 1
            if prev_date is not None and local_date != prev_date:
                transitions.append(
                    (
                        cur.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        local.strftime("%Y-%m-%dT%H:%M:%S%z"),
                        "{0}->{1}".format(prev_date, local_date),
                    )
                )
            prev_date = local_date
            offset = local.utcoffset()
            offset_str = "na" if offset is None else str(offset)
            print(
                "utc={0} local={1} offset={2} local_date={3}".format(
                    cur.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    local.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    offset_str,
                    local_date,
                )
            )
            cur = cur + step
        print("local_date_bins={0}".format(json.dumps(counts, ensure_ascii=True)))
        print("local_date_transitions={0}".format(len(transitions)))
        for utc_ts, local_ts, d in transitions[:10]:
            print("transition utc={0} local={1} date={2}".format(utc_ts, local_ts, d))


def print_bars_binning_samples(
    bars: list[Bar],
    config: dict,
    utc_start: str,
    utc_end: str,
    limit_lines: int,
) -> None:
    if ZoneInfo is None:
        raise RuntimeError("zoneinfo is not available; cannot convert timezones safely")
    sessions = config.get("sessions", {})
    dt0 = parse_iso_utc_loose(utc_start)
    dt1 = parse_iso_utc_loose(utc_end)
    if dt1 < dt0:
        raise ValueError("utc_end must be >= utc_start")

    window_bars = [b for b in bars if dt0 <= b.dt_utc <= dt1]
    print("bars_binning_utc_start={0}".format(dt0.strftime("%Y-%m-%dT%H:%M:%SZ")))
    print("bars_binning_utc_end={0}".format(dt1.strftime("%Y-%m-%dT%H:%M:%SZ")))
    print("bars_binning_rows={0}".format(len(window_bars)))
    if not window_bars:
        return

    for session_id, s in sessions.items():
        tz_name = str(s["session_timezone"])
        open_hhmm = str(s["session_open_local_hhmm"])
        window_minutes = int(s["opening_range_window_minutes"])
        tz = ZoneInfo(tz_name)
        open_h, open_m = parse_hhmm(open_hhmm)
        print(
            "bars_binning_session={0} timezone={1} open_local={2} window_minutes={3}".format(
                session_id, tz_name, open_hhmm, window_minutes
            )
        )

        local_date_bins: dict[str, int] = {}
        or_hit_bins: dict[str, int] = {}
        post_or_bins: dict[str, int] = {}
        local_date_or_anchor: dict[str, list[str]] = {}
        transitions: list[tuple[str, str, str]] = []
        prev_date: str | None = None

        lines = 0
        for b in window_bars:
            local = b.dt_utc.astimezone(tz)
            local_date = local.strftime("%Y-%m-%d")
            local_date_bins[local_date] = local_date_bins.get(local_date, 0) + 1

            local_midnight = datetime.strptime(local_date, "%Y-%m-%d").replace(tzinfo=tz)
            or_start = local_midnight.replace(hour=open_h, minute=open_m, second=0, microsecond=0)
            or_end = or_start + timedelta(minutes=window_minutes)
            if local_date not in local_date_or_anchor:
                local_date_or_anchor[local_date] = [
                    or_start.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    or_end.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                ]

            in_or = 1 if (or_start <= local < or_end) else 0
            is_post_or = 1 if (local >= or_end) else 0
            or_hit_bins[local_date] = or_hit_bins.get(local_date, 0) + in_or
            post_or_bins[local_date] = post_or_bins.get(local_date, 0) + is_post_or

            if prev_date is not None and local_date != prev_date:
                transitions.append(
                    (
                        b.dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        local.strftime("%Y-%m-%dT%H:%M:%S%z"),
                        "{0}->{1}".format(prev_date, local_date),
                    )
                )
            prev_date = local_date

            if lines < int(limit_lines):
                print(
                    "bar utc={0} local={1} local_date={2} in_or={3} post_or={4}".format(
                        b.dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        local.strftime("%Y-%m-%dT%H:%M:%S%z"),
                        local_date,
                        in_or,
                        is_post_or,
                    )
                )
                lines += 1

        print("bars_local_date_bins={0}".format(json.dumps(local_date_bins, ensure_ascii=True)))
        print("bars_or_hits_by_local_date={0}".format(json.dumps(or_hit_bins, ensure_ascii=True)))
        print("bars_post_or_by_local_date={0}".format(json.dumps(post_or_bins, ensure_ascii=True)))
        print("bars_or_anchor_by_local_date={0}".format(json.dumps(local_date_or_anchor, ensure_ascii=True)))
        print("bars_local_date_transitions={0}".format(len(transitions)))
        for utc_ts, local_ts, d in transitions[:10]:
            print("bars_transition utc={0} local={1} date={2}".format(utc_ts, local_ts, d))


def detect_first_break_v2(post_or_bars: list[Bar], or_high: float, or_low: float) -> tuple[str, str]:
    for b in post_or_bars:
        wick_up = b.high > or_high
        wick_down = b.low < or_low
        if wick_up and wick_down:
            return "none", "ambiguous"

        close_up = b.close > or_high
        close_down = b.close < or_low

        if close_up and not close_down and b.low >= or_low:
            return "up", "close"
        if close_down and not close_up and b.high <= or_high:
            return "down", "close"
        if wick_up and b.low >= or_low:
            return "up", "wick"
        if wick_down and b.high <= or_high:
            return "down", "wick"

    return "none", "none"


def parse_date(value: str) -> datetime:
    return datetime.strptime(value.strip(), "%Y-%m-%d")


def iter_dates(start_date: str, end_date: str) -> list[str]:
    dt0 = parse_date(start_date).date()
    dt1 = parse_date(end_date).date()
    if dt1 < dt0:
        raise ValueError("dst_end must be >= dst_start")
    out: list[str] = []
    cur = dt0
    while cur <= dt1:
        out.append(cur.isoformat())
        cur = cur + timedelta(days=1)
    return out


def print_dst_samples(config: dict, start_date: str, end_date: str) -> None:
    if ZoneInfo is None:
        raise RuntimeError("zoneinfo is not available; cannot convert timezones safely")
    sessions = config.get("sessions", {})
    for session_id, s in sessions.items():
        tz_name = str(s["session_timezone"])
        open_hhmm = str(s["session_open_local_hhmm"])
        window_minutes = int(s["opening_range_window_minutes"])
        tz = ZoneInfo(tz_name)
        open_h, open_m = parse_hhmm(open_hhmm)
        print("dst_sample_session={0} timezone={1} open_local={2} window_minutes={3}".format(session_id, tz_name, open_hhmm, window_minutes))
        for local_date in iter_dates(start_date, end_date):
            local_midnight = datetime.strptime(local_date, "%Y-%m-%d").replace(tzinfo=tz)
            or_start = local_midnight.replace(hour=open_h, minute=open_m, second=0, microsecond=0)
            or_end = or_start + timedelta(minutes=window_minutes)
            or_end_utc = or_end.astimezone(timezone.utc)
            or_start_utc = or_start.astimezone(timezone.utc)
            offset = or_end.utcoffset()
            offset_str = "na" if offset is None else str(offset)
            print(
                "local_date={0} or_start_local={1} or_end_local={2} or_start_utc={3} or_end_utc={4} offset={5}".format(
                    local_date,
                    or_start.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    or_end.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    or_start_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    or_end_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    offset_str,
                )
            )


def compute_or_rows(
    bars: list[Bar],
    session_id: str,
    session_timezone: str,
    open_hhmm: str,
    window_minutes: int,
    price_decimals: int,
    stats: BreakStats,
) -> list[dict]:
    if ZoneInfo is None:
        raise RuntimeError("zoneinfo is not available; cannot convert timezones safely")

    tz = ZoneInfo(session_timezone)
    if not bars:
        return []

    by_local_date: dict[str, list[Bar]] = {}
    for b in bars:
        local = b.dt_utc.astimezone(tz)
        key = local.strftime("%Y-%m-%d")
        by_local_date.setdefault(key, []).append(b)

    open_h, open_m = parse_hhmm(open_hhmm)
    out: list[dict] = []
    tf_minutes = timeframe_to_minutes(bars[0].timeframe)
    expected_bars = None
    if tf_minutes is not None and tf_minutes > 0:
        expected_bars = int(window_minutes / tf_minutes)

    for local_date, day_bars in sorted(by_local_date.items(), key=lambda kv: kv[0]):
        local_midnight = datetime.strptime(local_date, "%Y-%m-%d").replace(tzinfo=tz)
        or_start = local_midnight.replace(hour=open_h, minute=open_m, second=0, microsecond=0)
        or_end = or_start + timedelta(minutes=window_minutes)

        window: list[Bar] = []
        for b in day_bars:
            local = b.dt_utc.astimezone(tz)
            if or_start <= local < or_end:
                window.append(b)

        window.sort(key=lambda b: b.dt_utc)
        defined = "0"
        if expected_bars is None:
            defined = "1" if len(window) > 0 else "0"
        else:
            defined = "1" if len(window) >= expected_bars else "0"

        if defined == "0":
            out.append(
                {
                    "symbol": bars[0].symbol,
                    "timeframe": bars[0].timeframe,
                    "bar_time": or_end.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "session_id": session_id,
                    "session_timezone": session_timezone,
                    "opening_range_window_minutes": str(window_minutes),
                    "opening_range_high": "na",
                    "opening_range_low": "na",
                    "opening_range_mid": "na",
                    "opening_range_width": "na",
                    "opening_range_width_pct_open": "na",
                    "session_open_price": "na",
                    "opening_range_defined": "0",
                    "first_break_direction": "none",
                    "first_break_mode": "none",
                    "width_error_day": "1",
                }
            )
            continue

        or_high = max(b.high for b in window)
        or_low = min(b.low for b in window)
        or_mid = (or_high + or_low) / 2.0
        or_width = or_high - or_low
        session_open_price = window[0].open

        post_or_bars: list[Bar] = []
        for b in day_bars:
            local = b.dt_utc.astimezone(tz)
            if local >= or_end:
                post_or_bars.append(b)

        first_break_direction, first_break_mode = detect_first_break_v2(
            post_or_bars=post_or_bars, or_high=or_high, or_low=or_low
        )
        if first_break_mode == "close" and first_break_direction == "up":
            stats.close_up += 1
        elif first_break_mode == "close" and first_break_direction == "down":
            stats.close_down += 1
        elif first_break_mode == "wick" and first_break_direction == "up":
            stats.wick_up += 1
        elif first_break_mode == "wick" and first_break_direction == "down":
            stats.wick_down += 1
        elif first_break_mode == "ambiguous":
            stats.ambiguous += 1

        width_pct_open = "na"
        if session_open_price != 0.0:
            width_pct_open = fmt_num((or_width / session_open_price) * 100.0, decimals=4)

        out.append(
            {
                "symbol": bars[0].symbol,
                "timeframe": bars[0].timeframe,
                "bar_time": or_end.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "session_id": session_id,
                "session_timezone": session_timezone,
                "opening_range_window_minutes": str(window_minutes),
                "opening_range_high": fmt_price(or_high, decimals=price_decimals),
                "opening_range_low": fmt_price(or_low, decimals=price_decimals),
                "opening_range_mid": fmt_price(or_mid, decimals=price_decimals),
                "opening_range_width": fmt_price(or_width, decimals=price_decimals),
                "opening_range_width_pct_open": width_pct_open,
                "session_open_price": fmt_price(session_open_price, decimals=price_decimals),
                "opening_range_defined": "1",
                "first_break_direction": first_break_direction,
                "first_break_mode": first_break_mode,
                "width_error_day": "0",
            }
        )

    return out


def write_output(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--price-decimals", type=int, default=5)
    parser.add_argument("--debug-dst-sample", action="store_true")
    parser.add_argument("--dst-start", default="2026-03-20")
    parser.add_argument("--dst-end", default="2026-04-10")
    parser.add_argument("--debug-overlap-sample", action="store_true")
    parser.add_argument("--utc-start", default="2026-11-01T04:00:00Z")
    parser.add_argument("--utc-end", default="2026-11-01T09:00:00Z")
    parser.add_argument("--utc-step-minutes", type=int, default=30)
    parser.add_argument("--debug-local-date-binning", action="store_true")
    parser.add_argument("--debug-bars-binning", action="store_true")
    parser.add_argument("--bars-binning-limit-lines", type=int, default=80)
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    config_path = Path(args.config).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    cfg = load_json(config_path)
    sessions = cfg.get("sessions", {})
    if not sessions:
        raise ValueError("no sessions defined in config")

    if args.debug_dst_sample:
        print("config={0}".format(config_path))
        print_dst_samples(cfg, start_date=str(args.dst_start), end_date=str(args.dst_end))
        return
    if args.debug_overlap_sample:
        print("config={0}".format(config_path))
        print_overlap_samples(
            cfg,
            utc_start=str(args.utc_start),
            utc_end=str(args.utc_end),
            step_minutes=int(args.utc_step_minutes),
        )
        return
    if args.debug_local_date_binning:
        print("config={0}".format(config_path))
        print_local_date_binning_samples(
            cfg,
            utc_start=str(args.utc_start),
            utc_end=str(args.utc_end),
            step_minutes=int(args.utc_step_minutes),
        )
        return

    bars = read_bars(input_path)
    if args.debug_bars_binning:
        print("input={0}".format(input_path))
        print("config={0}".format(config_path))
        print_bars_binning_samples(
            bars=bars,
            config=cfg,
            utc_start=str(args.utc_start),
            utc_end=str(args.utc_end),
            limit_lines=int(args.bars_binning_limit_lines),
        )
        return
    out_rows: list[dict] = []
    stats = BreakStats()
    for session_id, s in sessions.items():
        out_rows.extend(
            compute_or_rows(
                bars=bars,
                session_id=session_id,
                session_timezone=str(s["session_timezone"]),
                open_hhmm=str(s["session_open_local_hhmm"]),
                window_minutes=int(s["opening_range_window_minutes"]),
                price_decimals=int(args.price_decimals),
                stats=stats,
            )
        )

    out_rows.sort(key=lambda r: (r["session_id"], r["bar_time"]))
    write_output(output_path, out_rows)

    defined = sum(1 for r in out_rows if r["opening_range_defined"] == "1")
    break_up = sum(1 for r in out_rows if r["first_break_direction"] == "up")
    break_down = sum(1 for r in out_rows if r["first_break_direction"] == "down")
    break_none = sum(1 for r in out_rows if r["first_break_direction"] == "none")
    print("input={0}".format(input_path))
    print("config={0}".format(config_path))
    print("output={0}".format(output_path))
    print("bars={0}".format(len(bars)))
    print("rows={0}".format(len(out_rows)))
    print("rows_or_defined={0}".format(defined))
    print("first_break_up={0}".format(break_up))
    print("first_break_down={0}".format(break_down))
    print("first_break_none={0}".format(break_none))
    print("first_break_close_up={0}".format(stats.close_up))
    print("first_break_close_down={0}".format(stats.close_down))
    print("first_break_wick_up={0}".format(stats.wick_up))
    print("first_break_wick_down={0}".format(stats.wick_down))
    print("first_break_ambiguous={0}".format(stats.ambiguous))


if __name__ == "__main__":
    main()
