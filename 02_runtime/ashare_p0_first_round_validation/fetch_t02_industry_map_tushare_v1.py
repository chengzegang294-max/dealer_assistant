from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = ROOT / "data" / "t02_sources" / "industry_tushare"


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
        description="Fetch T02 industry map from Tushare stock_basic."
    )
    parser.add_argument(
        "--list-status",
        default="L",
        help="Stock list status, default L.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for source CSV and metadata.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    base_name = f"t02_industry_map_tushare__list_status_{args.list_status}"
    csv_path = output_dir / f"{base_name}.csv"
    metadata_path = output_dir / f"{base_name}__metadata.json"

    metadata: dict[str, Any] = {
        "producer": "fetch_t02_industry_map_tushare_v1.py",
        "scope": "A股 P0 首轮离线验证 T02 行业映射真实源表",
        "status": "started",
        "list_status": args.list_status,
        "token_source": None,
        "output_csv": str(csv_path).replace("\\", "/"),
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
        df = pro.stock_basic(
            exchange="",
            list_status=args.list_status,
            fields="ts_code,symbol,name,industry,list_date",
        )
        if df is None or df.empty:
            metadata["status"] = "failed"
            metadata["failure_reason"] = "stock_basic_empty"
            write_json(metadata_path, metadata)
            return 4

        df["industry_code"] = ""
        df["industry_name"] = df["industry"].fillna("")
        df["data_source"] = "tushare:stock_basic"
        df["asof_date"] = df["list_date"].fillna("")
        df["notes"] = "industry_code_unavailable_in_stock_basic"
        df["symbol"] = df["ts_code"]
        output_df = df.loc[
            :,
            ["symbol", "name", "industry_code", "industry_name", "data_source", "asof_date", "notes"],
        ].rename(columns={"name": "symbol_name"})
        output_df.to_csv(csv_path, index=False, encoding="utf-8")

        metadata["status"] = "success"
        metadata["rows"] = int(len(output_df))
        metadata["columns"] = list(output_df.columns)
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
