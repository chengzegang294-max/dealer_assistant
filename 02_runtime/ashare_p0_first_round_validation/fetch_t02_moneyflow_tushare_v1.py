from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = ROOT / "data" / "t02_sources" / "moneyflow_tushare"


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
    parser = argparse.ArgumentParser(
        description="Fetch T02 moneyflow source table from Tushare moneyflow + daily."
    )
    parser.add_argument("--symbol", required=True, help="Tushare ts_code, e.g. 000001.SZ")
    parser.add_argument("--start-date", required=True, help="YYYYMMDD")
    parser.add_argument("--end-date", required=True, help="YYYYMMDD")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for source CSV and metadata.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    date_tag = f"{args.start_date}_{args.end_date}"
    base_name = f"t02_moneyflow_tushare__{args.symbol.replace('.', '_')}__{date_tag}"
    csv_path = output_dir / f"{base_name}.csv"
    metadata_path = output_dir / f"{base_name}__metadata.json"

    metadata: dict[str, Any] = {
        "producer": "fetch_t02_moneyflow_tushare_v1.py",
        "scope": "A股 P0 首轮离线验证 T02 主力资金真实源表",
        "status": "started",
        "symbol": args.symbol,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "token_source": None,
        "output_csv": str(csv_path).replace("\\", "/"),
        "ratio_formula": "main_fund_net_inflow_ratio = net_mf_amount / (daily.amount / 10.0)",
        "ratio_unit_note": "moneyflow.net_mf_amount uses 万元; daily.amount uses 千元; ratio saved as decimal 0~1",
    }

    token, token_source = load_tushare_token()
    metadata["token_source"] = token_source
    if not token:
        metadata["status"] = "failed"
        metadata["failure_reason"] = "tushare_token_missing"
        write_json(metadata_path, metadata)
        return 2

    try:
        import pandas as pd  # type: ignore
        import tushare as ts  # type: ignore
    except Exception as e:  # pragma: no cover
        metadata["status"] = "failed"
        metadata["failure_reason"] = "dependency_import_failed"
        metadata["failure_detail"] = str(e)
        write_json(metadata_path, metadata)
        return 3

    try:
        pro = ts.pro_api(token)
        moneyflow_df = pro.moneyflow(
            ts_code=args.symbol,
            start_date=args.start_date,
            end_date=args.end_date,
        )
        daily_df = pro.daily(
            ts_code=args.symbol,
            start_date=args.start_date,
            end_date=args.end_date,
        )
        if moneyflow_df is None or moneyflow_df.empty:
            metadata["status"] = "failed"
            metadata["failure_reason"] = "moneyflow_empty"
            write_json(metadata_path, metadata)
            return 4
        if daily_df is None or daily_df.empty:
            metadata["status"] = "failed"
            metadata["failure_reason"] = "daily_empty"
            write_json(metadata_path, metadata)
            return 5

        moneyflow_df = moneyflow_df.loc[:, [c for c in ["ts_code", "trade_date", "net_mf_amount"] if c in moneyflow_df.columns]]
        daily_df = daily_df.loc[:, [c for c in ["ts_code", "trade_date", "amount"] if c in daily_df.columns]]
        merged_df = moneyflow_df.merge(
            daily_df,
            on=["ts_code", "trade_date"],
            how="left",
            suffixes=("", "_daily"),
        )
        if "amount" not in merged_df.columns:
            metadata["status"] = "failed"
            metadata["failure_reason"] = "daily_amount_missing"
            write_json(metadata_path, metadata)
            return 6

        merged_df["symbol"] = merged_df["ts_code"]
        merged_df["symbol_name"] = args.symbol
        merged_df["main_fund_net_inflow"] = merged_df["net_mf_amount"]
        merged_df["main_fund_net_inflow_ratio"] = merged_df.apply(
            lambda row: (
                float(row["net_mf_amount"]) / (float(row["amount"]) / 10.0)
                if row.get("amount") not in (None, "", 0) and float(row["amount"]) != 0.0
                else None
            ),
            axis=1,
        )
        merged_df["data_source"] = "tushare:moneyflow+daily"
        merged_df["asof_date"] = merged_df["trade_date"]
        merged_df["notes"] = "ratio_from_net_mf_amount_div_daily_amount_wanyuan"

        output_df = merged_df.loc[
            :,
            [
                "trade_date",
                "symbol",
                "symbol_name",
                "main_fund_net_inflow",
                "main_fund_net_inflow_ratio",
                "data_source",
                "asof_date",
                "notes",
            ],
        ].sort_values("trade_date")
        output_df.to_csv(csv_path, index=False, encoding="utf-8")

        metadata["status"] = "success"
        metadata["rows"] = int(len(output_df))
        metadata["columns"] = list(output_df.columns)
        metadata["first_trade_date"] = str(output_df.iloc[0]["trade_date"])
        metadata["last_trade_date"] = str(output_df.iloc[-1]["trade_date"])
        write_json(metadata_path, metadata)
        return 0
    except Exception as e:  # pragma: no cover
        metadata["status"] = "failed"
        metadata["failure_reason"] = "tushare_api_error"
        metadata["failure_detail"] = str(e)
        write_json(metadata_path, metadata)
        return 7


if __name__ == "__main__":
    raise SystemExit(main())
