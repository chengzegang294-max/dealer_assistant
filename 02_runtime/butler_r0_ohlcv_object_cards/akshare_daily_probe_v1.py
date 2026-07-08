from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def normalize_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if "." in symbol:
        return symbol.split(".")[0]
    return symbol


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal AkShare daily OHLCV probe.")
    parser.add_argument("--symbol", required=True, help="A-share symbol, e.g. 300302 or 300302.SZ")
    parser.add_argument("--start-date", required=True, help="YYYYMMDD")
    parser.add_argument("--end-date", required=True, help="YYYYMMDD")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    symbol6 = normalize_symbol(args.symbol)
    date_tag = f"{args.start_date}_{args.end_date}"
    base_name = f"akshare_daily_probe__{symbol6}__{date_tag}"
    meta_path = output_dir / f"{base_name}__metadata.json"
    csv_path = output_dir / f"{base_name}.csv"

    metadata: dict[str, Any] = {
        "probe_name": "akshare_daily_probe_v1",
        "symbol": args.symbol,
        "symbol6": symbol6,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "producer": "akshare_daily_probe_v1.py",
        "repo_role": "probe_output",
        "status": "started",
        "output_csv": str(csv_path).replace("\\", "/"),
    }

    try:
        import akshare as ak  # type: ignore
    except Exception as e:  # pragma: no cover
        metadata["status"] = "failed"
        metadata["failure_reason"] = "akshare_import_failed"
        metadata["failure_detail"] = str(e)
        write_json(meta_path, metadata)
        return 2

    try:
        df = ak.stock_zh_a_hist(
            symbol=symbol6,
            period="daily",
            start_date=args.start_date,
            end_date=args.end_date,
            adjust="qfq",
        )
        if df is None or df.empty:
            metadata["status"] = "failed"
            metadata["failure_reason"] = "empty_dataframe"
            write_json(meta_path, metadata)
            return 3

        rename_map = {
            "日期": "trade_date",
            "开盘": "open",
            "收盘": "close",
            "最高": "high",
            "最低": "low",
            "成交量": "vol",
            "成交额": "amount",
            "振幅": "amplitude_pct",
            "涨跌幅": "pct_chg",
            "涨跌额": "change",
            "换手率": "turnover_rate",
        }
        for old, new in rename_map.items():
            if old in df.columns:
                df = df.rename(columns={old: new})
        if "symbol" not in df.columns:
            df["symbol"] = args.symbol.upper()
        preferred = [
            "symbol",
            "trade_date",
            "open",
            "high",
            "low",
            "close",
            "vol",
            "amount",
            "pct_chg",
            "change",
            "turnover_rate",
        ]
        columns = [c for c in preferred if c in df.columns] + [c for c in df.columns if c not in preferred]
        df = df.loc[:, columns]
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
        metadata["failure_reason"] = "akshare_api_error"
        metadata["failure_detail"] = str(e)
        write_json(meta_path, metadata)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
