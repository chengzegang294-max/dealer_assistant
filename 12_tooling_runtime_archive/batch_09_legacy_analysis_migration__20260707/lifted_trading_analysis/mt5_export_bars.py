from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

import pandas as pd

import MetaTrader5 as mt5


TIMEFRAME_MAP = {
    "M1": mt5.TIMEFRAME_M1,
    "M2": getattr(mt5, "TIMEFRAME_M2", None),
    "M3": getattr(mt5, "TIMEFRAME_M3", None),
    "M4": getattr(mt5, "TIMEFRAME_M4", None),
    "M5": mt5.TIMEFRAME_M5,
    "M6": getattr(mt5, "TIMEFRAME_M6", None),
    "M10": getattr(mt5, "TIMEFRAME_M10", None),
    "M12": getattr(mt5, "TIMEFRAME_M12", None),
    "M15": mt5.TIMEFRAME_M15,
    "M20": getattr(mt5, "TIMEFRAME_M20", None),
    "M30": mt5.TIMEFRAME_M30,
    "H1": mt5.TIMEFRAME_H1,
    "H2": getattr(mt5, "TIMEFRAME_H2", None),
    "H3": getattr(mt5, "TIMEFRAME_H3", None),
    "H4": mt5.TIMEFRAME_H4,
    "H6": getattr(mt5, "TIMEFRAME_H6", None),
    "H8": getattr(mt5, "TIMEFRAME_H8", None),
    "H12": getattr(mt5, "TIMEFRAME_H12", None),
    "D1": mt5.TIMEFRAME_D1,
    "W1": mt5.TIMEFRAME_W1,
    "MN1": mt5.TIMEFRAME_MN1,
}


def _pick_symbol(available: set[str], requested: str) -> str | None:
    req = str(requested).strip()
    if not req:
        return None
    if req in available:
        return req
    upper_map = {name.upper(): name for name in available}
    req_upper = req.upper()
    if req_upper in upper_map:
        return upper_map[req_upper]
    for name in available:
        name_upper = name.upper()
        if name_upper.startswith(req_upper) or name_upper.endswith(req_upper) or req_upper in name_upper:
            return name
    return None


def _parse_csv_list(raw: str) -> list[str]:
    return [x.strip() for x in str(raw).split(",") if x.strip()]


def _parse_jobs_list(raw: str) -> list[tuple[str, str, str | None, str | None]]:
    jobs: list[tuple[str, str, str | None, str | None]] = []
    for item in _parse_csv_list(raw):
        parts = [x.strip() for x in str(item).split(":")]
        if len(parts) < 2 or len(parts) > 4:
            raise ValueError("invalid job item: {0}; expected SYMBOL:TIMEFRAME[:START[:END]]".format(item))
        symbol = str(parts[0]).strip()
        timeframe = str(parts[1]).strip().upper()
        start = str(parts[2]).strip() if len(parts) >= 3 and str(parts[2]).strip() else None
        end = str(parts[3]).strip() if len(parts) >= 4 and str(parts[3]).strip() else None
        if not symbol or not timeframe:
            raise ValueError("invalid job item: {0}; expected SYMBOL:TIMEFRAME[:START[:END]]".format(item))
        jobs.append((symbol, timeframe, start, end))
    return jobs


def _parse_cli(argv: list[str]) -> dict[str, str]:
    out = {
        "symbol": "",
        "symbols": "",
        "jobs": "",
        "timeframe": "M1",
        "timeframes": "",
        "start": "2016-01-01",
        "end": datetime.now(timezone.utc).date().isoformat(),
        "out": "",
        "out_dir": "",
        "allow_missing": "0",
        "start_is_default": "1",
        "help": "0",
    }
    i = 0
    while i < len(argv):
        key = str(argv[i]).strip()
        if key in {"-h", "--help", "help"}:
            out["help"] = "1"
        elif key == "--symbol":
            i += 1
            out["symbol"] = str(argv[i]).strip()
        elif key == "--symbols":
            i += 1
            out["symbols"] = str(argv[i]).strip()
        elif key == "--jobs":
            i += 1
            out["jobs"] = str(argv[i]).strip()
        elif key == "--timeframe":
            i += 1
            out["timeframe"] = str(argv[i]).strip().upper()
        elif key == "--timeframes":
            i += 1
            out["timeframes"] = str(argv[i]).strip().upper()
        elif key in {"--start", "--from"}:
            i += 1
            out["start"] = str(argv[i]).strip()
            out["start_is_default"] = "0"
        elif key in {"--end", "--to"}:
            i += 1
            out["end"] = str(argv[i]).strip()
        elif key == "--out":
            i += 1
            out["out"] = str(argv[i]).strip()
        elif key == "--out-dir":
            i += 1
            out["out_dir"] = str(argv[i]).strip()
        elif key == "--allow-missing":
            i += 1
            out["allow_missing"] = str(argv[i]).strip()
        else:
            raise ValueError(f"unknown arg: {key}")
        i += 1
    return out


def _usage() -> None:
    print("Usage:")
    print("  python mt5_export_bars.py --symbol EURUSD --timeframe M1 --start 2016-01-01 --end 2026-06-12 --out D:\\Stock\\trading_analysis\\data\\mt_exports_drop\\eurusd_m1_export.csv")
    print("  python mt5_export_bars.py --symbol EURUSD --timeframe H1 --start 2016-01-01 --end 2026-06-12 --out D:\\Stock\\trading_analysis\\data\\mt_exports_drop\\eurusd_h1_export.csv")
    print("  python mt5_export_bars.py --symbols EURUSD,XAUUSD --timeframes M1,H1 --start 2016-01-01 --end 2026-06-12 --out-dir D:\\Stock\\trading_analysis\\data\\mt_exports_drop\\batch")
    print("  python mt5_export_bars.py --jobs EURUSD:M1,EURUSD:H1,XAUUSD:M5 --start 2016-01-01 --end 2026-06-12 --out-dir D:\\Stock\\trading_analysis\\data\\mt_exports_drop\\jobs")
    print("  python mt5_export_bars.py --jobs EURUSD:M1:2026-01-01,EURUSD:H1:2016-01-01,XAUUSD:M5:2026-05-01:2026-06-12 --out-dir D:\\Stock\\trading_analysis\\data\\mt_exports_drop\\jobs")
    print("  Note: date-only --end is treated as inclusive (internally end = next day 00:00Z); full ISO timestamps accept Z suffix (e.g. 2026-06-12T00:00:00Z).")

def _resolve_timeframe(timeframe_name: str) -> tuple[str, int]:
    timeframe_key = str(timeframe_name).strip().upper()
    timeframe = TIMEFRAME_MAP.get(timeframe_key)
    if timeframe is None:
        supported = ", ".join([k for k, v in TIMEFRAME_MAP.items() if v is not None])
        raise ValueError(f"unsupported timeframe: {timeframe_key}; supported={supported}")
    return timeframe_key, timeframe


def _chunk_days_for_timeframe(timeframe_key: str) -> int:
    if timeframe_key == "M1":
        return 7
    if timeframe_key in {"M2", "M3", "M4", "M5", "M6"}:
        return 14
    if timeframe_key in {"M10", "M12", "M15", "M20", "M30"}:
        return 31
    if timeframe_key in {"H1", "H2", "H3", "H4", "H6", "H8", "H12"}:
        return 180
    return 730


def _default_lookback_days_for_timeframe(timeframe_key: str) -> int | None:
    if timeframe_key == "M1":
        return 180
    if timeframe_key in {"M2", "M3", "M4", "M5", "M6"}:
        return 365
    if timeframe_key in {"M10", "M12", "M15", "M20", "M30"}:
        return 730
    return None


def _parse_utc_dt(raw: str, is_end: bool) -> datetime:
    s = str(raw).strip()
    if not s:
        raise ValueError("empty datetime")
    if "T" not in s and len(s) == 10:
        dt = datetime.fromisoformat(s).replace(tzinfo=timezone.utc)
        if is_end:
            return dt + timedelta(days=1)
        return dt
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _effective_start(start: str, end: str, timeframe_key: str, start_is_default: bool) -> str:
    if not start_is_default:
        return start
    lookback_days = _default_lookback_days_for_timeframe(timeframe_key)
    if lookback_days is None:
        return start
    dt_start = _parse_utc_dt(start, is_end=False)
    dt_end = _parse_utc_dt(end, is_end=True)
    candidate = dt_end - timedelta(days=lookback_days)
    if candidate > dt_start:
        return candidate.date().isoformat()
    return start


def _fetch_export_frame(
    available: set[str],
    symbol: str,
    timeframe_name: str,
    start: str,
    end: str,
) -> tuple[str, str, pd.DataFrame]:
    timeframe_key, timeframe = _resolve_timeframe(timeframe_name)
    resolved_symbol = _pick_symbol(available, symbol)
    if resolved_symbol is None:
        raise RuntimeError(f"symbol not found in MT5: requested={symbol}")
    if not mt5.symbol_select(resolved_symbol, True):
        raise RuntimeError(f"symbol_select failed: {resolved_symbol}")

    dt0 = _parse_utc_dt(start, is_end=False)
    dt1 = _parse_utc_dt(end, is_end=True)
    if dt1 <= dt0:
        raise ValueError(f"end must be after start: start={start} end={end}")
    start_ts = int(dt0.timestamp())
    end_ts = int(dt1.timestamp())

    chunk_days = _chunk_days_for_timeframe(timeframe_key)
    frames: list[pd.DataFrame] = []
    cur = dt0
    saw_none = False
    while cur < dt1:
        nxt = min(dt1, cur + timedelta(days=chunk_days))
        rates = mt5.copy_rates_range(resolved_symbol, timeframe, cur, nxt)
        if rates is None:
            saw_none = True
        else:
            df_chunk = pd.DataFrame(rates)
            if not df_chunk.empty:
                frames.append(df_chunk)
        cur = nxt

    if not frames:
        if saw_none:
            raise RuntimeError(f"copy_rates_range returned None across chunks: symbol={resolved_symbol} timeframe={timeframe_key}")
        raise RuntimeError(f"no data returned: symbol={resolved_symbol} timeframe={timeframe_key}")

    df = pd.concat(frames, axis=0, ignore_index=True)
    df = df.drop_duplicates(subset=["time"], keep="last").sort_values(["time"], ascending=[True]).reset_index(drop=True)
    if "time" in df.columns:
        df_in_range = df[(df["time"] >= start_ts) & (df["time"] < end_ts)].copy()
        if df_in_range.empty:
            first_ts = int(df.iloc[0]["time"])
            last_ts = int(df.iloc[-1]["time"])
            first_utc = datetime.fromtimestamp(first_ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            last_utc = datetime.fromtimestamp(last_ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            raise RuntimeError(
                "no data returned within requested range: symbol={0} timeframe={1} start={2} end={3} first_returned_utc={4} last_returned_utc={5}".format(
                    resolved_symbol,
                    timeframe_key,
                    dt0.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    dt1.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    first_utc,
                    last_utc,
                )
            )
        df = df_in_range

    dt = pd.to_datetime(df["time"], unit="s", utc=True)
    out = pd.DataFrame(
        {
            "date": dt.dt.strftime("%Y.%m.%d"),
            "time": dt.dt.strftime("%H:%M"),
            "open": df["open"].astype(float),
            "high": df["high"].astype(float),
            "low": df["low"].astype(float),
            "close": df["close"].astype(float),
            "volume": df.get("tick_volume", df.get("real_volume", 0)).astype(float),
        }
    )
    return resolved_symbol, timeframe_key, out


def _write_export(out: pd.DataFrame, out_csv: str) -> Path:
    out_path = Path(out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, index=False)
    return out_path


def _print_export_summary(resolved_symbol: str, timeframe_key: str, out: pd.DataFrame, out_path: Path) -> None:
    print(f"resolved_symbol={resolved_symbol}")
    print(f"timeframe={timeframe_key}")
    print(f"rows={len(out)}")
    print(f"first_bar={out.iloc[0]['date']} {out.iloc[0]['time']}")
    print(f"last_bar={out.iloc[-1]['date']} {out.iloc[-1]['time']}")
    print(f"output={out_path}")


def export_bars(symbol: str, timeframe_name: str, start: str, end: str, out_csv: str) -> None:
    if not mt5.initialize():
        raise RuntimeError(f"mt5.initialize() failed, error={mt5.last_error()}")
    try:
        available = {s.name for s in (mt5.symbols_get() or [])}
        resolved_symbol, timeframe_key, out = _fetch_export_frame(available, symbol, timeframe_name, start, end)
        out_path = _write_export(out, out_csv)
        _print_export_summary(resolved_symbol, timeframe_key, out, out_path)
    finally:
        mt5.shutdown()


def export_bars_batch(symbols: list[str], timeframes: list[str], start: str, end: str, out_dir: str, allow_missing: bool, start_is_default: bool) -> None:
    if not mt5.initialize():
        raise RuntimeError(f"mt5.initialize() failed, error={mt5.last_error()}")
    try:
        available = {s.name for s in (mt5.symbols_get() or [])}
        base_dir = Path(out_dir)
        base_dir.mkdir(parents=True, exist_ok=True)
        for symbol in symbols:
            for timeframe_name in timeframes:
                try:
                    timeframe_key, _ = _resolve_timeframe(timeframe_name)
                    effective_start = _effective_start(start, end, timeframe_key, start_is_default)
                    resolved_symbol, timeframe_key, out = _fetch_export_frame(available, symbol, timeframe_name, effective_start, end)
                    file_name = "{0}_{1}.csv".format(symbol.strip().lower(), timeframe_key.lower())
                    out_path = _write_export(out, str(base_dir / file_name))
                    print("[BATCH] ok requested_symbol={0} resolved_symbol={1} timeframe={2} start={3} end={4} rows={5} output={6}".format(symbol, resolved_symbol, timeframe_key, effective_start, end, len(out), out_path))
                except Exception as e:
                    msg = "[BATCH] fail requested_symbol={0} timeframe={1} err={2}: {3}".format(symbol, str(timeframe_name).strip().upper(), type(e).__name__, e)
                    if allow_missing:
                        print(msg)
                        continue
                    raise RuntimeError(msg) from e
    finally:
        mt5.shutdown()


def export_bars_jobs(jobs: list[tuple[str, str, str | None, str | None]], start: str, end: str, out_dir: str, allow_missing: bool, start_is_default: bool) -> None:
    if not mt5.initialize():
        raise RuntimeError(f"mt5.initialize() failed, error={mt5.last_error()}")
    try:
        available = {s.name for s in (mt5.symbols_get() or [])}
        base_dir = Path(out_dir)
        base_dir.mkdir(parents=True, exist_ok=True)
        for symbol, timeframe_name, start_override, end_override in jobs:
            try:
                timeframe_key, _ = _resolve_timeframe(timeframe_name)
                job_start = start_override or _effective_start(start, end_override or end, timeframe_key, start_is_default)
                job_end = end_override or end
                resolved_symbol, timeframe_key, out = _fetch_export_frame(available, symbol, timeframe_name, job_start, job_end)
                file_name = "{0}_{1}.csv".format(symbol.strip().lower(), timeframe_key.lower())
                out_path = _write_export(out, str(base_dir / file_name))
                print("[JOBS] ok requested_symbol={0} resolved_symbol={1} timeframe={2} start={3} end={4} rows={5} output={6}".format(symbol, resolved_symbol, timeframe_key, job_start, job_end, len(out), out_path))
            except Exception as e:
                msg = "[JOBS] fail requested_symbol={0} timeframe={1} start={2} end={3} err={4}: {5}".format(symbol, str(timeframe_name).strip().upper(), start_override or start, end_override or end, type(e).__name__, e)
                if allow_missing:
                    print(msg)
                    continue
                raise RuntimeError(msg) from e
    finally:
        mt5.shutdown()


def main() -> None:
    args = _parse_cli(sys.argv[1:])
    batch_symbols = _parse_csv_list(args["symbols"])
    batch_timeframes = [x.upper() for x in _parse_csv_list(args["timeframes"])]
    jobs = _parse_jobs_list(args["jobs"])
    allow_missing = str(args["allow_missing"]).strip() in {"1", "true", "TRUE", "yes", "YES"}
    start_is_default = str(args["start_is_default"]).strip() == "1"
    if args["help"] == "1":
        _usage()
        return
    if jobs:
        if args["out_dir"] == "":
            _usage()
            raise ValueError("jobs mode requires --out-dir")
        export_bars_jobs(
            jobs=jobs,
            start=args["start"],
            end=args["end"],
            out_dir=args["out_dir"],
            allow_missing=allow_missing,
            start_is_default=start_is_default,
        )
        return
    if batch_symbols or batch_timeframes or args["out_dir"]:
        if not batch_symbols or not batch_timeframes or not args["out_dir"]:
            _usage()
            raise ValueError("batch mode requires --symbols, --timeframes, and --out-dir")
        export_bars_batch(
            symbols=batch_symbols,
            timeframes=batch_timeframes,
            start=args["start"],
            end=args["end"],
            out_dir=args["out_dir"],
            allow_missing=allow_missing,
            start_is_default=start_is_default,
        )
        return
    if not args["symbol"] or not args["out"]:
        _usage()
        return
    single_timeframe_key, _ = _resolve_timeframe(args["timeframe"])
    effective_start = _effective_start(args["start"], args["end"], single_timeframe_key, start_is_default)
    export_bars(symbol=args["symbol"], timeframe_name=args["timeframe"], start=effective_start, end=args["end"], out_csv=args["out"])


if __name__ == "__main__":
    main()
