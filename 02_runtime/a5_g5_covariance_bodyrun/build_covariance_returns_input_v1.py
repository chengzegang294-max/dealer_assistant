from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def require_runtime_params(payload: dict[str, Any]) -> list[str]:
    required = [
        "candidate_model_family",
        "portfolio_date",
        "benchmark_id",
        "asset_universe_id",
        "returns_window_spec",
        "tracking_error_limit",
        "active_risk_aversion",
    ]
    return [field for field in required if field not in payload]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build asset returns, benchmark returns, and active returns inputs for covariance first fresh-run."
    )
    parser.add_argument("--runtime-params-json", required=True)
    parser.add_argument("--asset-ohlcv-csv", required=True)
    parser.add_argument("--benchmark-series-csv", required=True)
    parser.add_argument("--universe-csv", required=True)
    parser.add_argument("--asset-returns-csv", required=True)
    parser.add_argument("--benchmark-returns-csv", required=True)
    parser.add_argument("--active-returns-csv", required=True)
    parser.add_argument("--summary-json", required=True)
    args = parser.parse_args()

    runtime_params_path = Path(args.runtime_params_json)
    asset_ohlcv_path = Path(args.asset_ohlcv_csv)
    benchmark_series_path = Path(args.benchmark_series_csv)
    universe_path = Path(args.universe_csv)
    asset_returns_path = Path(args.asset_returns_csv)
    benchmark_returns_path = Path(args.benchmark_returns_csv)
    active_returns_path = Path(args.active_returns_csv)
    summary_path = Path(args.summary_json)

    summary: dict[str, Any] = {
        "producer": "build_covariance_returns_input_v1.py",
        "scope": "covariance first fresh-run returns input builder",
        "status": "started",
        "runtime_params_json": str(runtime_params_path).replace("\\", "/"),
        "asset_ohlcv_csv": str(asset_ohlcv_path).replace("\\", "/"),
        "benchmark_series_csv": str(benchmark_series_path).replace("\\", "/"),
        "universe_csv": str(universe_path).replace("\\", "/"),
        "asset_returns_csv": str(asset_returns_path).replace("\\", "/"),
        "benchmark_returns_csv": str(benchmark_returns_path).replace("\\", "/"),
        "active_returns_csv": str(active_returns_path).replace("\\", "/"),
    }

    try:
        import pandas as pd  # type: ignore
    except Exception as exc:  # pragma: no cover
        summary["status"] = "failed"
        summary["failure_reason"] = "dependency_import_failed"
        summary["failure_detail"] = str(exc)
        write_json(summary_path, summary)
        return 2

    runtime_params = load_json(runtime_params_path)
    missing = require_runtime_params(runtime_params)
    if missing:
        summary["status"] = "failed"
        summary["failure_reason"] = "runtime_params_missing_fields"
        summary["missing_fields"] = missing
        write_json(summary_path, summary)
        return 3

    if runtime_params["candidate_model_family"] != "benchmark_relative_sample_covariance":
        summary["status"] = "failed"
        summary["failure_reason"] = "candidate_family_mismatch"
        write_json(summary_path, summary)
        return 4

    lookback_days = int(runtime_params["returns_window_spec"]["lookback_days"])
    benchmark_id = str(runtime_params["benchmark_id"])
    asset_universe_id = str(runtime_params["asset_universe_id"])

    asset_df = pd.read_csv(asset_ohlcv_path, dtype={"trade_date": str, "symbol": str})
    benchmark_df = pd.read_csv(benchmark_series_path, dtype={"trade_date": str})
    universe_df = pd.read_csv(universe_path, dtype={"symbol": str})

    required_asset_cols = {"trade_date", "symbol", "close", "pre_close"}
    required_benchmark_cols = {"trade_date", "benchmark_return_1d", "benchmark_id", "benchmark_index_code"}
    required_universe_cols = {"symbol"}

    if not required_asset_cols.issubset(asset_df.columns):
        summary["status"] = "failed"
        summary["failure_reason"] = "asset_ohlcv_missing_columns"
        summary["missing_columns"] = sorted(required_asset_cols.difference(asset_df.columns))
        write_json(summary_path, summary)
        return 5
    if not required_benchmark_cols.issubset(benchmark_df.columns):
        summary["status"] = "failed"
        summary["failure_reason"] = "benchmark_series_missing_columns"
        summary["missing_columns"] = sorted(required_benchmark_cols.difference(benchmark_df.columns))
        write_json(summary_path, summary)
        return 6
    if not required_universe_cols.issubset(universe_df.columns):
        summary["status"] = "failed"
        summary["failure_reason"] = "universe_missing_columns"
        summary["missing_columns"] = sorted(required_universe_cols.difference(universe_df.columns))
        write_json(summary_path, summary)
        return 7

    expected_symbols = sorted(universe_df["symbol"].dropna().astype(str).unique().tolist())
    asset_df = asset_df[asset_df["symbol"].isin(expected_symbols)].copy()
    asset_df["close"] = asset_df["close"].astype(float)
    asset_df["pre_close"] = asset_df["pre_close"].astype(float)
    asset_df["asset_return_1d"] = asset_df["close"] / asset_df["pre_close"] - 1.0
    asset_df["asset_universe_id"] = asset_universe_id

    benchmark_df = benchmark_df[benchmark_df["benchmark_id"] == benchmark_id].copy()
    benchmark_df["benchmark_return_1d"] = benchmark_df["benchmark_return_1d"].astype(float)
    benchmark_df = benchmark_df.sort_values("trade_date").reset_index(drop=True)

    asset_dates = set(asset_df["trade_date"].astype(str))
    benchmark_dates = set(benchmark_df["trade_date"].astype(str))
    common_dates = sorted(asset_dates.intersection(benchmark_dates))
    if len(common_dates) < lookback_days:
        summary["status"] = "failed"
        summary["failure_reason"] = "insufficient_common_trade_dates"
        summary["common_trade_dates"] = len(common_dates)
        summary["required_lookback_days"] = lookback_days
        write_json(summary_path, summary)
        return 8

    selected_dates = common_dates[-lookback_days:]
    asset_df = asset_df[asset_df["trade_date"].isin(selected_dates)].copy()
    benchmark_df = benchmark_df[benchmark_df["trade_date"].isin(selected_dates)].copy()

    asset_count_by_date = (
        asset_df.groupby("trade_date")["symbol"].nunique().sort_index().to_dict()
    )
    incomplete_dates = [
        trade_date
        for trade_date, count in asset_count_by_date.items()
        if int(count) != len(expected_symbols)
    ]
    if incomplete_dates:
        summary["status"] = "failed"
        summary["failure_reason"] = "asset_universe_not_complete_for_selected_window"
        summary["incomplete_dates"] = incomplete_dates
        write_json(summary_path, summary)
        return 9

    asset_returns = asset_df.loc[
        :,
        ["trade_date", "symbol", "asset_return_1d", "close", "pre_close", "asset_universe_id"],
    ].copy()
    asset_returns = asset_returns.rename(
        columns={"close": "asset_close", "pre_close": "asset_pre_close"}
    )
    asset_returns = asset_returns.sort_values(["trade_date", "symbol"]).reset_index(drop=True)

    benchmark_returns = benchmark_df.loc[
        :,
        [
            "trade_date",
            "benchmark_id",
            "benchmark_index_code",
            "benchmark_return_1d",
            "close",
        ],
    ].copy()
    benchmark_returns = benchmark_returns.rename(columns={"close": "benchmark_close"})
    benchmark_returns = benchmark_returns.sort_values("trade_date").reset_index(drop=True)

    active_returns = asset_returns.merge(
        benchmark_returns.loc[:, ["trade_date", "benchmark_id", "benchmark_return_1d"]],
        how="inner",
        on="trade_date",
    )
    active_returns["active_return_1d"] = (
        active_returns["asset_return_1d"] - active_returns["benchmark_return_1d"]
    )
    active_returns["candidate_model_family"] = runtime_params["candidate_model_family"]
    active_returns = active_returns.loc[
        :,
        [
            "trade_date",
            "symbol",
            "candidate_model_family",
            "benchmark_id",
            "asset_universe_id",
            "asset_return_1d",
            "benchmark_return_1d",
            "active_return_1d",
        ],
    ].copy()
    active_returns = active_returns.sort_values(["trade_date", "symbol"]).reset_index(drop=True)

    asset_returns_path.parent.mkdir(parents=True, exist_ok=True)
    benchmark_returns_path.parent.mkdir(parents=True, exist_ok=True)
    active_returns_path.parent.mkdir(parents=True, exist_ok=True)
    asset_returns.to_csv(asset_returns_path, index=False, encoding="utf-8")
    benchmark_returns.to_csv(benchmark_returns_path, index=False, encoding="utf-8")
    active_returns.to_csv(active_returns_path, index=False, encoding="utf-8")

    summary["status"] = "success"
    summary["selected_trade_dates"] = len(selected_dates)
    summary["first_trade_date"] = selected_dates[0]
    summary["last_trade_date"] = selected_dates[-1]
    summary["symbol_count"] = len(expected_symbols)
    summary["benchmark_id"] = benchmark_id
    summary["asset_universe_id"] = asset_universe_id
    summary["candidate_model_family"] = runtime_params["candidate_model_family"]
    summary["asset_rows"] = int(len(asset_returns))
    summary["benchmark_rows"] = int(len(benchmark_returns))
    summary["active_rows"] = int(len(active_returns))
    summary["audit_note"] = "returns_input_built_from_existing_tushare_daily_assets"
    write_json(summary_path, summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
