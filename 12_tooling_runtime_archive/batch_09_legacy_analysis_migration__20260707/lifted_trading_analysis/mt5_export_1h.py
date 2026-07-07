from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import sys
import time
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd

import MetaTrader5 as mt5


def _norm_symbol_name(s: str) -> str:
    return str(s).strip()


def _pick_symbol(available: set[str], candidates: list[str]) -> str | None:
    cands = [_norm_symbol_name(x) for x in candidates if str(x).strip()]
    for c in cands:
        if c in available:
            return c
    upper_map = {a.upper(): a for a in available}
    for c in cands:
        u = c.upper()
        if u in upper_map:
            return upper_map[u]
    for c in cands:
        u = c.upper()
        for a in available:
            au = a.upper()
            if au == u:
                return a
            if au.startswith(u):
                return a
            if au.endswith(u):
                return a
            if u in au:
                return a
    return None


def export_symbol_1h(symbol: str, out_csv: str, start: str, end: str) -> None:
    ok = mt5.symbol_select(symbol, True)
    if not ok:
        raise RuntimeError(f"symbol_select failed: {symbol}")

    dt0 = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
    dt1 = datetime.fromisoformat(end).replace(tzinfo=timezone.utc)

    rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_H1, dt0, dt1)
    if rates is None:
        raise RuntimeError(f"copy_rates_range returned None: {symbol}")

    df = pd.DataFrame(rates)
    if df.empty:
        raise RuntimeError(f"no data returned: {symbol}")

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

    out_path = Path(out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, index=False)


def _read_existing_ohlcv_1h(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["date", "time", "open", "high", "low", "close", "volume"])
    df = pd.read_csv(path)
    if df is None or df.empty:
        return pd.DataFrame(columns=["date", "time", "open", "high", "low", "close", "volume"])
    need = {"date", "time", "open", "high", "low", "close"}
    if not need.issubset(set(map(str, df.columns))):
        return pd.DataFrame(columns=["date", "time", "open", "high", "low", "close", "volume"])
    if "volume" not in df.columns:
        df["volume"] = 0.0
    keep = ["date", "time", "open", "high", "low", "close", "volume"]
    df = df[keep].copy()
    return df


def _merge_and_write_ohlcv_1h(existing: pd.DataFrame, incoming: pd.DataFrame, out_path: Path) -> None:
    if existing is None or existing.empty:
        out = incoming.copy()
    elif incoming is None or incoming.empty:
        out = existing.copy()
    else:
        out = pd.concat([existing, incoming], axis=0, ignore_index=True)
    if not out.empty:
        out["datetime"] = out["date"].astype(str) + " " + out["time"].astype(str)
        out = out.drop_duplicates(subset=["datetime"], keep="last").sort_values(["datetime"], ascending=[True]).drop(
            columns=["datetime"]
        )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, index=False)


def export_symbol_1h_update(symbol: str, out_csv: str, start: str, end: str, overlap_hours: int = 48) -> None:
    out_path = Path(out_csv)
    existing = _read_existing_ohlcv_1h(out_path)
    if existing is None or existing.empty:
        export_symbol_1h(symbol, out_csv, start=start, end=end)
        return
    dt_existing = pd.to_datetime(existing["date"].astype(str) + " " + existing["time"].astype(str), errors="coerce", utc=True)
    dt_last = dt_existing.dropna().max()
    if dt_last is None or dt_last != dt_last:
        export_symbol_1h(symbol, out_csv, start=start, end=end)
        return
    dt0_req = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
    dt0 = max(dt0_req, (dt_last.to_pydatetime() - timedelta(hours=int(overlap_hours))))
    dt1 = datetime.fromisoformat(end).replace(tzinfo=timezone.utc)
    if dt1 <= dt0:
        _merge_and_write_ohlcv_1h(existing, pd.DataFrame(), out_path)
        return

    ok = mt5.symbol_select(symbol, True)
    if not ok:
        raise RuntimeError(f"symbol_select failed: {symbol}")
    rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_H1, dt0, dt1)
    if rates is None:
        raise RuntimeError(f"copy_rates_range returned None: {symbol}")
    df = pd.DataFrame(rates)
    if df.empty:
        _merge_and_write_ohlcv_1h(existing, pd.DataFrame(), out_path)
        return
    dt = pd.to_datetime(df["time"], unit="s", utc=True)
    incoming = pd.DataFrame(
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
    _merge_and_write_ohlcv_1h(existing, incoming, out_path)


def _http_get_json(url: str, timeout_sec: int = 60) -> dict[str, Any]:
    req = Request(url, headers={"User-Agent": "trading_analysis/mt5_export_1h"})
    with urlopen(req, timeout=timeout_sec) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    try:
        return json.loads(raw)
    except Exception as e:
        raise RuntimeError(f"invalid json: {type(e).__name__}: {e}; url={url}; head={raw[:200]}") from e


def _twelvedata_time_series(
    symbol: str,
    interval: str,
    start_date: str,
    end_date: str,
    apikey: str,
    timezone_name: str = "UTC",
) -> pd.DataFrame:
    qs = urlencode(
        {
            "symbol": symbol,
            "interval": interval,
            "apikey": apikey,
            "start_date": start_date,
            "end_date": end_date,
            "timezone": timezone_name,
            "order": "ASC",
            "outputsize": 5000,
        }
    )
    url = f"https://api.twelvedata.com/time_series?{qs}"
    data = _http_get_json(url)
    if not isinstance(data, dict):
        raise RuntimeError(f"unexpected response type: {type(data).__name__}")
    if str(data.get("status", "")).lower() == "error":
        code = str(data.get("code", "") or "")
        msg = str(data.get("message", "") or "")
        raise RuntimeError(f"twelvedata error: code={code} message={msg}")
    values = data.get("values", None)
    if values is None and isinstance(data.get("data"), dict):
        values = data["data"].get("values", None)
    if not isinstance(values, list):
        return pd.DataFrame()
    df = pd.DataFrame(values)
    if df.empty:
        return df
    if "datetime" not in df.columns:
        return pd.DataFrame()
    for c in ["open", "high", "low", "close", "volume"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    dt = pd.to_datetime(df["datetime"].astype(str), errors="coerce")
    df["date"] = dt.dt.strftime("%Y.%m.%d")
    df["time"] = dt.dt.strftime("%H:%M")
    if "volume" not in df.columns:
        df["volume"] = 0.0
    keep = ["date", "time", "open", "high", "low", "close", "volume"]
    df = df[keep].dropna(subset=["date", "time", "open", "high", "low", "close"])
    return df


def export_twelvedata_1h(symbol: str, out_csv: str, start: str, end: str, apikey: str) -> None:
    dt0 = datetime.fromisoformat(start).replace(tzinfo=None)
    dt1 = datetime.fromisoformat(end).replace(tzinfo=None)
    if dt1 <= dt0:
        raise ValueError(f"end must be after start: start={start} end={end}")

    step_days = 180
    rows: list[pd.DataFrame] = []
    cur = dt0
    while cur < dt1:
        nxt = min(dt1, cur + timedelta(days=step_days))
        df = _twelvedata_time_series(
            symbol=str(symbol).strip(),
            interval="1h",
            start_date=cur.date().isoformat(),
            end_date=nxt.date().isoformat(),
            apikey=str(apikey).strip(),
            timezone_name="UTC",
        )
        if df is not None and not df.empty:
            rows.append(df)
        cur = nxt
        time.sleep(0.25)

    out = pd.concat(rows, axis=0, ignore_index=True) if rows else pd.DataFrame(columns=["date", "time", "open", "high", "low", "close", "volume"])
    if not out.empty:
        out["datetime"] = out["date"].astype(str) + " " + out["time"].astype(str)
        out = out.drop_duplicates(subset=["datetime"], keep="last").sort_values(["datetime"], ascending=[True]).drop(columns=["datetime"])

    out_path = Path(out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, index=False)


def _parse_symbols_spec(s: str) -> list[tuple[str, str]]:
    raw = str(s or "").strip()
    if not raw:
        return []
    parts = [x.strip() for x in raw.split(",") if x.strip()]
    out: list[tuple[str, str]] = []
    for p in parts:
        if ":" in p:
            a, b = p.split(":", 1)
        elif "=" in p:
            a, b = p.split("=", 1)
        else:
            a, b = p, p
        out_name = str(a).strip().lower()
        src_name = str(b).strip()
        if out_name and src_name:
            out.append((out_name, src_name))
    return out


def _parse_cli(argv: list[str]) -> dict[str, Any]:
    out: dict[str, Any] = {
        "source": "mt5",
        "start": "2016-01-01",
        "end": datetime.now(timezone.utc).date().isoformat(),
        "out_dir": str(Path(__file__).resolve().parent / "data"),
        "symbols": "",
        "apikey": "",
        "mode": "overwrite",
        "overlap_hours": 48,
        "allow_missing": 0,
        "help": 0,
    }
    i = 0
    while i < len(argv):
        k = str(argv[i]).strip()
        if k in {"-h", "--help", "help"}:
            out["help"] = 1
        elif k in {"--source"}:
            i += 1
            out["source"] = str(argv[i]).strip().lower()
        elif k in {"--start", "--from"}:
            i += 1
            out["start"] = str(argv[i]).strip()
        elif k in {"--end", "--to"}:
            i += 1
            out["end"] = str(argv[i]).strip()
        elif k in {"--out-dir"}:
            i += 1
            out["out_dir"] = str(argv[i]).strip()
        elif k in {"--symbols"}:
            i += 1
            out["symbols"] = str(argv[i]).strip()
        elif k in {"--apikey"}:
            i += 1
            out["apikey"] = str(argv[i]).strip()
        elif k in {"--mode"}:
            i += 1
            out["mode"] = str(argv[i]).strip().lower()
        elif k in {"--overlap-hours"}:
            i += 1
            out["overlap_hours"] = int(str(argv[i]).strip())
        elif k in {"--allow-missing"}:
            i += 1
            out["allow_missing"] = int(str(argv[i]).strip())
        else:
            raise ValueError(f"unknown arg: {k}")
        i += 1
    return out


def main() -> None:
    if len(sys.argv) == 1:
        if not mt5.initialize():
            raise RuntimeError(f"mt5.initialize() failed, error={mt5.last_error()}")

        start = "2016-01-01"
        end = datetime.now(timezone.utc).date().isoformat()

        base_dir = str(Path(__file__).resolve().parent / "data")
        exports: dict[str, list[str]] = {
            "xauusd": ["XAUUSD", "XAUUSDm", "XAUUSD."],
            "xagusd": ["XAGUSD", "XAGUSDm", "XAGUSD."],
            "eurusd": ["EURUSD", "EURUSDm", "EURUSD."],
            "gbpusd": ["GBPUSD", "GBPUSDm", "GBPUSD."],
            "usdjpy": ["USDJPY", "USDJPYm", "USDJPY."],
            "usdcad": ["USDCAD", "USDCADm", "USDCAD."],
            "audusd": ["AUDUSD", "AUDUSDm", "AUDUSD."],
            "nzdusd": ["NZDUSD", "NZDUSDm", "NZDUSD."],
            "usdchf": ["USDCHF", "USDCHFm", "USDCHF."],
            "eurjpy": ["EURJPY", "EURJPYm", "EURJPY."],
            "gbpjpy": ["GBPJPY", "GBPJPYm", "GBPJPY."],
            "usoil": ["USOIL", "USOIL.", "USOILm", "WTICOUSD", "XTIUSD", "UKOIL", "BRNUSD"],
            "us500": ["US500", "US500.", "US500m", "SPX500", "SP500", "SPXUSD"],
            "nas100": ["NAS100", "NAS100.", "NAS100m", "US100", "NDX100"],
            "ger40": ["GER40", "GER40.", "GER40m", "DE40", "DAX40"],
        }

        available = {s.name for s in (mt5.symbols_get() or [])}
        for out_name, candidates in exports.items():
            sym = _pick_symbol(available, candidates)
            if sym is None:
                continue
            out_csv = str(Path(base_dir) / f"{out_name.lower()}_1h.csv")
            export_symbol_1h(sym, out_csv, start=start, end=end)

        mt5.shutdown()
        return

    args = _parse_cli(sys.argv[1:])
    if int(args.get("help") or 0) != 0:
        print("Usage:")
        print("  python mt5_export_1h.py")
        print("  python mt5_export_1h.py --source twelvedata --apikey YOUR_KEY --symbols US500:SPX,NAS100:NDX,GER40:DAX --start 2012-01-01 --end 2026-05-20")
        print("  python mt5_export_1h.py --source mt5 --symbols XAUUSD:XAUUSD,EURUSD:EURUSD --start 2016-01-01 --end 2026-05-20")
        print("  python mt5_export_1h.py --source mt5 --mode update --overlap-hours 48 --symbols XAUUSD:XAUUSD --start 2016-01-01 --end 2026-06-02")
        return

    src = str(args.get("source") or "mt5").strip().lower()
    start = str(args.get("start") or "").strip()
    end = str(args.get("end") or "").strip()
    out_dir = Path(str(args.get("out_dir") or "").strip()).expanduser()
    symbols_spec = _parse_symbols_spec(str(args.get("symbols") or ""))
    mode = str(args.get("mode") or "overwrite").strip().lower()
    overlap_hours = int(args.get("overlap_hours") or 48)
    allow_missing = int(args.get("allow_missing") or 0) != 0

    if not symbols_spec:
        raise ValueError("--symbols is required when using CLI mode")
    if mode not in {"overwrite", "update"}:
        raise ValueError(f"unknown --mode: {mode} (expected overwrite/update)")
    if overlap_hours < 0:
        overlap_hours = 0

    if src == "twelvedata":
        apikey = str(args.get("apikey") or "").strip()
        if not apikey:
            apikey = str(os.environ.get("TWELVEDATA_APIKEY", "") or "").strip()
        if not apikey:
            raise ValueError("missing apikey: pass --apikey or set env TWELVEDATA_APIKEY")
        errors: list[tuple[str, str, str]] = []
        for out_sym, src_sym in symbols_spec:
            out_csv = str(out_dir / f"{out_sym}_1h.csv")
            try:
                if mode == "update" and Path(out_csv).exists():
                    existing = _read_existing_ohlcv_1h(Path(out_csv))
                    dt_existing = pd.to_datetime(
                        existing["date"].astype(str) + " " + existing["time"].astype(str), errors="coerce", utc=True
                    )
                    dt_last = dt_existing.dropna().max()
                    dt0_req = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
                    if dt_last is not None and dt_last == dt_last:
                        dt0 = max(dt0_req, (dt_last.to_pydatetime() - timedelta(hours=int(overlap_hours))))
                        start2 = dt0.date().isoformat()
                    else:
                        start2 = start
                    export_twelvedata_1h(src_sym, out_csv, start=start2, end=end, apikey=apikey)
                    incoming = pd.read_csv(out_csv) if Path(out_csv).exists() else pd.DataFrame()
                    _merge_and_write_ohlcv_1h(existing, incoming, Path(out_csv))
                else:
                    export_twelvedata_1h(src_sym, out_csv, start=start, end=end, apikey=apikey)
                print(f"[EXPORT][twelvedata] ok out_sym={out_sym} src_sym={src_sym} out_csv={out_csv}")
            except Exception as e:
                msg = f"{type(e).__name__}: {e}"
                errors.append((out_sym, src_sym, msg))
                print(f"[EXPORT][twelvedata] fail out_sym={out_sym} src_sym={src_sym} err={msg}")
        if errors:
            lines = [f"- {a} <= {b}: {c}" for a, b, c in errors]
            raise RuntimeError("twelvedata export failed for some symbols:\n" + "\n".join(lines))
        return

    if src == "mt5":
        if not mt5.initialize():
            raise RuntimeError(f"mt5.initialize() failed, error={mt5.last_error()}")
        try:
            available = {s.name for s in (mt5.symbols_get() or [])}
            for out_sym, src_sym in symbols_spec:
                sym = _pick_symbol(available, [src_sym, out_sym, f"{out_sym}.", f"{out_sym}m"])
                if sym is None:
                    msg = f"symbol not found in MT5: {out_sym} (requested={src_sym})"
                    if allow_missing:
                        print(f"[EXPORT][mt5] skip {msg}")
                        continue
                    raise RuntimeError(msg)
                out_csv = str(out_dir / f"{out_sym}_1h.csv")
                if mode == "update":
                    export_symbol_1h_update(sym, out_csv, start=start, end=end, overlap_hours=overlap_hours)
                else:
                    export_symbol_1h(sym, out_csv, start=start, end=end)
        finally:
            mt5.shutdown()
        return

    raise ValueError(f"unknown --source: {src}")


if __name__ == "__main__":
    main()
