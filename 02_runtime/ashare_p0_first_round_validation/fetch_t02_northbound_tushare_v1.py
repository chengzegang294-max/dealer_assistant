from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = ROOT / "data" / "t02_sources" / "northbound_tushare"


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
        description="Fetch T02 northbound source table from Tushare moneyflow_hsgt."
    )
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
    base_name = f"t02_northbound_tushare__{date_tag}"
    csv_path = output_dir / f"{base_name}.csv"
    metadata_path = output_dir / f"{base_name}__metadata.json"

    metadata: dict[str, Any] = {
        "producer": "fetch_t02_northbound_tushare_v1.py",
        "scope": "A股 P0 首轮离线验证 T02 北向真实源表",
        "status": "started",
        "start_date": args.start_date,
        "end_date": args.end_date,
        "token_source": None,
        "output_csv": str(csv_path).replace("\\", "/"),
        "join_level": "trade_date",
    }

    token, token_source = load_tushare_token()
    metadata["token_source"] = token_source
    if not token:
        metadata["status"] = "failed"
        metadata["failure_reason"] = "tushare_token_missing"
        write_json(metadata_path, metadata)
        return 2

    try:
        import tushare as ts  # type: ignore
    except Exception as e:  # pragma: no cover
        metadata["status"] = "failed"
        metadata["failure_reason"] = "tushare_import_failed"
        metadata["failure_detail"] = str(e)
        write_json(metadata_path, metadata)
        return 3

    try:
        pro = ts.pro_api(token)
        df = pro.moneyflow_hsgt(start_date=args.start_date, end_date=args.end_date)
        if df is None or df.empty:
            metadata["status"] = "failed"
            metadata["failure_reason"] = "moneyflow_hsgt_empty"
            write_json(metadata_path, metadata)
            return 4

        preferred = [c for c in ["trade_date", "north_money", "hgt", "sgt"] if c in df.columns]
        df = df.loc[:, preferred].sort_values("trade_date")
        rename_map = {"north_money": "northbound_net_inflow"}
        df = df.rename(columns=rename_map)
        df["data_source"] = "tushare:moneyflow_hsgt"
        df["asof_date"] = df["trade_date"]
        df["notes"] = "trade_date_level_northbound_series"
        df.to_csv(csv_path, index=False, encoding="utf-8")

        metadata["status"] = "success"
        metadata["rows"] = int(len(df))
        metadata["columns"] = list(df.columns)
        metadata["first_trade_date"] = str(df.iloc[0]["trade_date"])
        metadata["last_trade_date"] = str(df.iloc[-1]["trade_date"])
        write_json(metadata_path, metadata)
        return 0
    except Exception as e:  # pragma: no cover
        metadata["status"] = "failed"
        metadata["failure_reason"] = "tushare_api_error"
        metadata["failure_detail"] = str(e)
        write_json(metadata_path, metadata)
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
