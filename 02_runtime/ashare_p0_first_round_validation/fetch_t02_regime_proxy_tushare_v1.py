from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = ROOT / "data" / "t02_sources" / "regime"


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


def calendar_shift(date_str: str, days: int) -> str:
    return (datetime.strptime(date_str, "%Y%m%d") + timedelta(days=days)).strftime("%Y%m%d")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch a lightweight market regime proxy for T02 using broad-index daily data."
    )
    parser.add_argument("--start-date", required=True, help="YYYYMMDD")
    parser.add_argument("--end-date", required=True, help="YYYYMMDD")
    parser.add_argument(
        "--index-code",
        default="000300.SH",
        help="Broad index used as the regime proxy. Default: CSI 300.",
    )
    parser.add_argument(
        "--lookback-days",
        type=int,
        default=5,
        help="Rolling trading-day window used for regime classification.",
    )
    parser.add_argument(
        "--rolling-return-threshold",
        type=float,
        default=2.0,
        help="Absolute rolling return threshold in percent for G01/G02.",
    )
    parser.add_argument(
        "--min-direction-days",
        type=int,
        default=3,
        help="Minimum up/down days inside the rolling window.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for regime CSV and metadata.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    date_tag = f"{args.start_date}_{args.end_date}"
    safe_index_code = args.index_code.replace(".", "_")
    base_name = f"t02_regime_proxy_tushare__{safe_index_code}__{date_tag}"
    csv_path = output_dir / f"{base_name}.csv"
    metadata_path = output_dir / f"{base_name}__metadata.json"

    metadata: dict[str, Any] = {
        "producer": "fetch_t02_regime_proxy_tushare_v1.py",
        "scope": "A股 P0 首轮离线验证 T02 市场阶段代理表",
        "status": "started",
        "index_code": args.index_code,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "token_source": None,
        "output_csv": str(csv_path).replace("\\", "/"),
        "lookback_days": args.lookback_days,
        "rolling_return_threshold_pct": args.rolling_return_threshold,
        "min_direction_days": args.min_direction_days,
        "regime_definition": {
            "G01_普涨": "rolling_pct_sum >= threshold and up_days >= min_direction_days",
            "G02_普跌": "rolling_pct_sum <= -threshold and down_days >= min_direction_days",
            "G03_震荡": "otherwise",
        },
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
        padded_start = calendar_shift(args.start_date, -21)
        pro = ts.pro_api(token)
        df = pro.index_daily(ts_code=args.index_code, start_date=padded_start, end_date=args.end_date)
        if df is None or df.empty:
            metadata["status"] = "failed"
            metadata["failure_reason"] = "index_daily_empty"
            write_json(metadata_path, metadata)
            return 4

        required_cols = ["trade_date", "pct_chg", "close"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            metadata["status"] = "failed"
            metadata["failure_reason"] = "index_daily_missing_columns"
            metadata["missing_columns"] = missing_cols
            write_json(metadata_path, metadata)
            return 5

        df = df.loc[:, [col for col in ["trade_date", "pct_chg", "close"] if col in df.columns]].copy()
        df["trade_date"] = df["trade_date"].astype(str)
        df["pct_chg"] = df["pct_chg"].astype(float)
        df = df.sort_values("trade_date").reset_index(drop=True)
        df["up_day"] = (df["pct_chg"] > 0).astype(int)
        df["down_day"] = (df["pct_chg"] < 0).astype(int)
        df["rolling_pct_sum"] = df["pct_chg"].rolling(args.lookback_days, min_periods=args.lookback_days).sum()
        df["rolling_up_days"] = df["up_day"].rolling(args.lookback_days, min_periods=args.lookback_days).sum()
        df["rolling_down_days"] = df["down_day"].rolling(args.lookback_days, min_periods=args.lookback_days).sum()

        def classify(row: Any) -> str:
            rolling_pct_sum = row["rolling_pct_sum"]
            rolling_up_days = row["rolling_up_days"]
            rolling_down_days = row["rolling_down_days"]
            if pd.isna(rolling_pct_sum):
                return "G03_震荡"
            if (
                float(rolling_pct_sum) >= float(args.rolling_return_threshold)
                and float(rolling_up_days) >= float(args.min_direction_days)
            ):
                return "G01_普涨"
            if (
                float(rolling_pct_sum) <= -float(args.rolling_return_threshold)
                and float(rolling_down_days) >= float(args.min_direction_days)
            ):
                return "G02_普跌"
            return "G03_震荡"

        df["market_regime_label"] = df.apply(classify, axis=1)
        df = df[df["trade_date"] >= args.start_date].copy()
        if df.empty:
            metadata["status"] = "failed"
            metadata["failure_reason"] = "filtered_output_empty"
            write_json(metadata_path, metadata)
            return 6

        df["regime_proxy_index_code"] = args.index_code
        df["data_source"] = f"tushare:index_daily:{args.index_code}"
        df["asof_date"] = df["trade_date"]
        df["notes"] = (
            f"proxy_from_{args.index_code}_rolling_{args.lookback_days}d_pct_sum_threshold_"
            f"{args.rolling_return_threshold}_pct"
        )
        output_columns = [
            "trade_date",
            "market_regime_label",
            "regime_proxy_index_code",
            "rolling_pct_sum",
            "rolling_up_days",
            "rolling_down_days",
            "data_source",
            "asof_date",
            "notes",
        ]
        df.to_csv(csv_path, columns=output_columns, index=False, encoding="utf-8")

        regime_counts = {
            str(label): int(count)
            for label, count in df["market_regime_label"].value_counts().sort_index().items()
        }
        metadata["status"] = "success"
        metadata["rows"] = int(len(df))
        metadata["columns"] = output_columns
        metadata["first_trade_date"] = str(df.iloc[0]["trade_date"])
        metadata["last_trade_date"] = str(df.iloc[-1]["trade_date"])
        metadata["regime_counts"] = regime_counts
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
