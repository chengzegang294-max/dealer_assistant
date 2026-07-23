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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the first benchmark-relative sample covariance fresh-run from active returns."
    )
    parser.add_argument("--runtime-params-json", required=True)
    parser.add_argument("--active-returns-csv", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--matrix-csv", required=True)
    args = parser.parse_args()

    runtime_params_path = Path(args.runtime_params_json)
    active_returns_path = Path(args.active_returns_csv)
    output_json = Path(args.output_json)
    matrix_csv = Path(args.matrix_csv)

    result: dict[str, Any] = {
        "run_id": "covariance_bodyrun_fresh_latest",
        "producer": "run_covariance_bodyrun_fresh_v1.py",
        "scope": "covariance_bodyrun_fresh",
        "status": "started",
        "evidence_mode": "hard",
        "runtime_params_json": str(runtime_params_path).replace("\\", "/"),
        "active_returns_csv": str(active_returns_path).replace("\\", "/"),
        "matrix_csv": str(matrix_csv).replace("\\", "/"),
    }

    try:
        import numpy as np  # type: ignore
        import pandas as pd  # type: ignore
    except Exception as exc:  # pragma: no cover
        result["status"] = "failed"
        result["failure_reason"] = "dependency_import_failed"
        result["failure_detail"] = str(exc)
        write_json(output_json, result)
        return 2

    runtime_params = load_json(runtime_params_path)
    if runtime_params.get("candidate_model_family") != "benchmark_relative_sample_covariance":
        result["status"] = "failed"
        result["failure_reason"] = "candidate_family_mismatch"
        write_json(output_json, result)
        return 3

    active_returns = pd.read_csv(active_returns_path, dtype={"trade_date": str, "symbol": str})
    required_cols = {
        "trade_date",
        "symbol",
        "candidate_model_family",
        "benchmark_id",
        "asset_universe_id",
        "asset_return_1d",
        "benchmark_return_1d",
        "active_return_1d",
    }
    if not required_cols.issubset(active_returns.columns):
        result["status"] = "failed"
        result["failure_reason"] = "active_returns_missing_columns"
        result["missing_columns"] = sorted(required_cols.difference(active_returns.columns))
        write_json(output_json, result)
        return 4

    if active_returns["candidate_model_family"].nunique() != 1:
        result["status"] = "failed"
        result["failure_reason"] = "candidate_family_not_unique"
        write_json(output_json, result)
        return 5
    if active_returns["candidate_model_family"].iloc[0] != runtime_params["candidate_model_family"]:
        result["status"] = "failed"
        result["failure_reason"] = "active_returns_candidate_family_mismatch"
        write_json(output_json, result)
        return 6

    lookback_days = int(runtime_params["returns_window_spec"]["lookback_days"])
    expected_benchmark_id = str(runtime_params["benchmark_id"])
    expected_universe_id = str(runtime_params["asset_universe_id"])
    if active_returns["benchmark_id"].nunique() != 1 or active_returns["benchmark_id"].iloc[0] != expected_benchmark_id:
        result["status"] = "failed"
        result["failure_reason"] = "benchmark_id_mismatch"
        write_json(output_json, result)
        return 7
    if active_returns["asset_universe_id"].nunique() != 1 or active_returns["asset_universe_id"].iloc[0] != expected_universe_id:
        result["status"] = "failed"
        result["failure_reason"] = "asset_universe_id_mismatch"
        write_json(output_json, result)
        return 8

    active_returns["active_return_1d"] = active_returns["active_return_1d"].astype(float)
    pivot = active_returns.pivot(index="trade_date", columns="symbol", values="active_return_1d")
    pivot = pivot.sort_index().sort_index(axis=1)

    if len(pivot.index) != lookback_days:
        result["status"] = "failed"
        result["failure_reason"] = "unexpected_trade_date_count"
        result["trade_date_count"] = int(len(pivot.index))
        result["required_lookback_days"] = lookback_days
        write_json(output_json, result)
        return 9
    if pivot.isna().any().any():
        result["status"] = "failed"
        result["failure_reason"] = "active_returns_contains_na"
        write_json(output_json, result)
        return 10

    covariance_df = pivot.cov()
    eigvals = np.linalg.eigvalsh(covariance_df.to_numpy())
    min_eigenvalue = float(np.min(eigvals))
    diagonal = np.diag(covariance_df.to_numpy())
    diagonal_positive = bool((diagonal > 0).all())
    is_psd = bool(min_eigenvalue >= -1e-10)

    matrix_csv.parent.mkdir(parents=True, exist_ok=True)
    covariance_df.to_csv(matrix_csv, encoding="utf-8")

    covariance_model_id = (
        f"benchmark_relative_sample_covariance__{expected_benchmark_id}"
        f"__lookback{lookback_days}__{expected_universe_id}__v1"
    )
    result.update(
        {
            "status": "success",
            "fresh_run_passed": diagonal_positive and is_psd,
            "candidate_family": runtime_params["candidate_model_family"],
            "covariance_model_id": covariance_model_id,
            "portfolio_date": runtime_params["portfolio_date"],
            "benchmark_id": expected_benchmark_id,
            "asset_universe_id": expected_universe_id,
            "returns_window_spec": runtime_params["returns_window_spec"],
            "matrix_shape": [int(covariance_df.shape[0]), int(covariance_df.shape[1])],
            "effective_trade_dates": int(len(pivot.index)),
            "asset_count": int(len(pivot.columns)),
            "diagonal_positive": diagonal_positive,
            "is_psd": is_psd,
            "min_eigenvalue": min_eigenvalue,
            "first_trade_date": str(pivot.index[0]),
            "last_trade_date": str(pivot.index[-1]),
            "notes": "first_body_matrix_fresh_run_completed__still_not_ready",
            "forbidden_claim": "risk_model_ready",
            "matrix_output_csv": str(matrix_csv).replace("\\", "/"),
        }
    )
    write_json(output_json, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
