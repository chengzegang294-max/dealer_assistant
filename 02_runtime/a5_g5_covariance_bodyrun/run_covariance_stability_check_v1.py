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
        description="Compare current and adjacent covariance fresh-runs for minimum stability checking."
    )
    parser.add_argument("--current-fresh-json", required=True)
    parser.add_argument("--current-matrix-csv", required=True)
    parser.add_argument("--adjacent-fresh-json", required=True)
    parser.add_argument("--adjacent-matrix-csv", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    current_fresh_path = Path(args.current_fresh_json)
    current_matrix_path = Path(args.current_matrix_csv)
    adjacent_fresh_path = Path(args.adjacent_fresh_json)
    adjacent_matrix_path = Path(args.adjacent_matrix_csv)
    output_json = Path(args.output_json)

    result: dict[str, Any] = {
        "producer": "run_covariance_stability_check_v1.py",
        "scope": "covariance minimum stability check",
        "status": "started",
        "evidence_mode": "hard",
        "current_fresh_json": str(current_fresh_path).replace("\\", "/"),
        "current_matrix_csv": str(current_matrix_path).replace("\\", "/"),
        "adjacent_fresh_json": str(adjacent_fresh_path).replace("\\", "/"),
        "adjacent_matrix_csv": str(adjacent_matrix_path).replace("\\", "/"),
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

    current_fresh = load_json(current_fresh_path)
    adjacent_fresh = load_json(adjacent_fresh_path)
    current_matrix = pd.read_csv(current_matrix_path, index_col=0)
    adjacent_matrix = pd.read_csv(adjacent_matrix_path, index_col=0)

    if list(current_matrix.index) != list(current_matrix.columns):
        result["status"] = "failed"
        result["failure_reason"] = "current_matrix_index_columns_mismatch"
        write_json(output_json, result)
        return 3
    if list(adjacent_matrix.index) != list(adjacent_matrix.columns):
        result["status"] = "failed"
        result["failure_reason"] = "adjacent_matrix_index_columns_mismatch"
        write_json(output_json, result)
        return 4
    if list(current_matrix.index) != list(adjacent_matrix.index):
        result["status"] = "failed"
        result["failure_reason"] = "matrix_symbol_order_mismatch"
        write_json(output_json, result)
        return 5

    current_arr = current_matrix.to_numpy(dtype=float)
    adjacent_arr = adjacent_matrix.to_numpy(dtype=float)

    trace_current = float(np.trace(current_arr))
    trace_adjacent = float(np.trace(adjacent_arr))
    fro_current = float(np.linalg.norm(current_arr, ord="fro"))
    fro_adjacent = float(np.linalg.norm(adjacent_arr, ord="fro"))
    fro_diff = float(np.linalg.norm(current_arr - adjacent_arr, ord="fro"))
    max_fro = max(fro_current, fro_adjacent, 1e-12)
    relative_fro_diff = float(fro_diff / max_fro)
    trace_ratio = float(trace_current / max(trace_adjacent, 1e-12))
    relative_trace_gap = float(abs(trace_current - trace_adjacent) / max(trace_current, trace_adjacent, 1e-12))

    current_diag = np.diag(current_arr)
    adjacent_diag = np.diag(adjacent_arr)
    diag_ratio_mean = float(np.mean(current_diag / np.maximum(adjacent_diag, 1e-12)))

    structural_pass = (
        current_fresh.get("fresh_run_passed") is True
        and adjacent_fresh.get("fresh_run_passed") is True
        and current_fresh.get("diagonal_positive") is True
        and adjacent_fresh.get("diagonal_positive") is True
        and current_fresh.get("is_psd") is True
        and adjacent_fresh.get("is_psd") is True
        and current_fresh.get("matrix_shape") == adjacent_fresh.get("matrix_shape") == [20, 20]
        and current_fresh.get("asset_count") == adjacent_fresh.get("asset_count") == 20
        and current_fresh.get("effective_trade_dates") == adjacent_fresh.get("effective_trade_dates") == 60
    )
    scale_gap_within_guardrail = relative_trace_gap <= 0.60
    stability_check_passed = bool(structural_pass and scale_gap_within_guardrail)

    result.update(
        {
            "status": "success",
            "stability_check_passed": stability_check_passed,
            "structural_pass": structural_pass,
            "scale_gap_within_guardrail": scale_gap_within_guardrail,
            "current_window": {
                "first_trade_date": current_fresh.get("first_trade_date"),
                "last_trade_date": current_fresh.get("last_trade_date"),
                "min_eigenvalue": current_fresh.get("min_eigenvalue"),
            },
            "adjacent_window": {
                "first_trade_date": adjacent_fresh.get("first_trade_date"),
                "last_trade_date": adjacent_fresh.get("last_trade_date"),
                "min_eigenvalue": adjacent_fresh.get("min_eigenvalue"),
            },
            "matrix_shape": current_fresh.get("matrix_shape"),
            "symbol_count": current_fresh.get("asset_count"),
            "trace_current": trace_current,
            "trace_adjacent": trace_adjacent,
            "trace_ratio_current_over_adjacent": trace_ratio,
            "relative_trace_gap": relative_trace_gap,
            "fro_norm_current": fro_current,
            "fro_norm_adjacent": fro_adjacent,
            "fro_norm_diff": fro_diff,
            "relative_fro_diff": relative_fro_diff,
            "diag_ratio_mean_current_over_adjacent": diag_ratio_mean,
            "audit_note": "minimum_stability_check_across_two_60d_windows",
            "forbidden_claim": "risk_model_ready",
        }
    )
    write_json(output_json, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
