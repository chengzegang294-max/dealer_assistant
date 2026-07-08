from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


def load_tushare_token() -> tuple[str | None, str]:
    env_token = (os.environ.get("TUSHARE_TOKEN") or "").strip()
    if env_token:
        return env_token, "env:TUSHARE_TOKEN"

    home_token = Path.home() / ".tushare" / "token"
    if home_token.exists():
        token = home_token.read_text(encoding="utf-8").strip()
        if token:
            return token, str(home_token)

    return None, "missing"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal Tushare daily OHLCV probe.")
    parser.add_argument("--symbol", required=True, help="Tushare ts_code, e.g. 300302.SZ")
    parser.add_argument("--start-date", required=True, help="YYYYMMDD")
    parser.add_argument("--end-date", required=True, help="YYYYMMDD")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    date_tag = f"{args.start_date}_{args.end_date}"
    base_name = f"tushare_daily_probe__{args.symbol.replace('.', '_')}__{date_tag}"
    meta_path = output_dir / f"{base_name}__metadata.json"
    csv_path = output_dir / f"{base_name}.csv"

    metadata: dict[str, Any] = {
        "probe_name": "tushare_daily_probe_v1",
        "symbol": args.symbol,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "producer": "tushare_daily_probe_v1.py",
        "repo_role": "probe_output",
        "status": "started",
        "token_source": None,
        "output_csv": str(csv_path).replace("\\", "/"),
    }

    token, token_source = load_tushare_token()
    metadata["token_source"] = token_source
    if not token:
        metadata["status"] = "failed"
        metadata["failure_reason"] = "tushare_token_missing"
        write_json(meta_path, metadata)
        return 2

    try:
        import tushare as ts  # type: ignore
    except Exception as e:  # pragma: no cover
        metadata["status"] = "failed"
        metadata["failure_reason"] = "tushare_import_failed"
        metadata["failure_detail"] = str(e)
        write_json(meta_path, metadata)
        return 3

    try:
        pro = ts.pro_api(token)
        df = pro.daily(ts_code=args.symbol, start_date=args.start_date, end_date=args.end_date)
        if df is None or df.empty:
            metadata["status"] = "failed"
            metadata["failure_reason"] = "empty_dataframe"
            write_json(meta_path, metadata)
            return 4

        preferred = ["ts_code", "trade_date", "open", "high", "low", "close", "pre_close", "change", "pct_chg", "vol", "amount"]
        columns = [c for c in preferred if c in df.columns] + [c for c in df.columns if c not in preferred]
        df = df.loc[:, columns].sort_values("trade_date")
        df.to_csv(csv_path, index=False, encoding="utf-8")

        metadata["status"] = "success"
        metadata["rows"] = int(len(df))
        metadata["columns"] = list(df.columns)
        metadata["first_trade_date"] = str(df.iloc[0]["trade_date"])
        metadata["last_trade_date"] = str(df.iloc[-1]["trade_date"])
        write_json(meta_path, metadata)
        return 0
    except Exception as e:  # pragma: no cover
        metadata["status"] = "failed"
        metadata["failure_reason"] = "tushare_api_error"
        metadata["failure_detail"] = str(e)
        write_json(meta_path, metadata)
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
