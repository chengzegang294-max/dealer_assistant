from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def normalize_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if "." not in symbol:
        raise ValueError("baostock requires symbol like 300302.SZ or 600000.SH")
    code, market = symbol.split(".")
    market_map = {"SH": "sh", "SZ": "sz"}
    if market not in market_map:
        raise ValueError(f"unsupported market suffix: {market}")
    return f"{market_map[market]}.{code}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal BaoStock daily OHLCV probe.")
    parser.add_argument("--symbol", required=True, help="e.g. 300302.SZ")
    parser.add_argument("--start-date", required=True, help="YYYYMMDD")
    parser.add_argument("--end-date", required=True, help="YYYYMMDD")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    start_date = f"{args.start_date[:4]}-{args.start_date[4:6]}-{args.start_date[6:8]}"
    end_date = f"{args.end_date[:4]}-{args.end_date[4:6]}-{args.end_date[6:8]}"
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    bs_symbol = normalize_symbol(args.symbol)
    date_tag = f"{args.start_date}_{args.end_date}"
    base_name = f"baostock_daily_probe__{args.symbol.replace('.', '_')}__{date_tag}"
    meta_path = output_dir / f"{base_name}__metadata.json"
    csv_path = output_dir / f"{base_name}.csv"

    metadata: dict[str, Any] = {
        "probe_name": "baostock_daily_probe_v1",
        "symbol": args.symbol,
        "bs_symbol": bs_symbol,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "producer": "baostock_daily_probe_v1.py",
        "repo_role": "probe_output",
        "status": "started",
        "output_csv": str(csv_path).replace("\\", "/"),
    }

    try:
        import baostock as bs  # type: ignore
    except Exception as e:  # pragma: no cover
        metadata["status"] = "failed"
        metadata["failure_reason"] = "baostock_import_failed"
        metadata["failure_detail"] = str(e)
        write_json(meta_path, metadata)
        return 2

    login_rs = None
    try:
        login_rs = bs.login()
        if getattr(login_rs, "error_code", "0") != "0":
            metadata["status"] = "failed"
            metadata["failure_reason"] = "baostock_login_failed"
            metadata["failure_detail"] = getattr(login_rs, "error_msg", "")
            write_json(meta_path, metadata)
            return 3

        rs = bs.query_history_k_data_plus(
            bs_symbol,
            "date,code,open,high,low,close,volume,amount,pctChg",
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="2",
        )
        if getattr(rs, "error_code", "0") != "0":
            metadata["status"] = "failed"
            metadata["failure_reason"] = "baostock_query_failed"
            metadata["failure_detail"] = getattr(rs, "error_msg", "")
            write_json(meta_path, metadata)
            return 4

        rows: list[list[str]] = []
        while rs.next():
            rows.append(rs.get_row_data())
        if not rows:
            metadata["status"] = "failed"
            metadata["failure_reason"] = "empty_dataframe"
            write_json(meta_path, metadata)
            return 5

        df = pd.DataFrame(rows, columns=rs.fields)
        df.to_csv(csv_path, index=False, encoding="utf-8")

        metadata["status"] = "success"
        metadata["rows"] = int(len(df))
        metadata["columns"] = list(df.columns)
        metadata["first_trade_date"] = str(df.iloc[0]["date"])
        metadata["last_trade_date"] = str(df.iloc[-1]["date"])
        write_json(meta_path, metadata)
        return 0
    except Exception as e:  # pragma: no cover
        metadata["status"] = "failed"
        metadata["failure_reason"] = "baostock_api_error"
        metadata["failure_detail"] = str(e)
        write_json(meta_path, metadata)
        return 6
    finally:
        try:
            if login_rs is not None:
                bs.logout()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
