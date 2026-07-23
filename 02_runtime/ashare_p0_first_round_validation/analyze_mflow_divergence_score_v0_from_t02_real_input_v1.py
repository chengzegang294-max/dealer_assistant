from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT_CSV = ROOT / "artifacts" / "t02_real_input_build" / "t02_real_input_candidate_latest.csv"
DEFAULT_OUTPUT_DIR = ROOT / "artifacts" / "mflow_divergence_score_v0"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_tsv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Derive a v0 divergence score from T02 real input candidate table."
    )
    parser.add_argument("--input-csv", default=str(DEFAULT_INPUT_CSV))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    return parser.parse_args()


def to_float(value: Any) -> float | None:
    s = str(value).strip()
    if not s:
        return None
    try:
        return float(s)
    except Exception:
        return None


def safe_quantile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    if q <= 0:
        return float(min(values))
    if q >= 1:
        return float(max(values))
    values_sorted = sorted(values)
    idx = int(round((len(values_sorted) - 1) * q))
    return float(values_sorted[max(0, min(len(values_sorted) - 1, idx))])


def main() -> int:
    args = parse_args()
    input_csv = Path(args.input_csv)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "mflow_divergence_score_v0_summary_latest.json"
    detail_path = output_dir / "mflow_divergence_score_v0_detail_latest.tsv"
    per_symbol_path = output_dir / "mflow_divergence_score_v0_symbol_counts_latest.tsv"

    summary: dict[str, Any] = {
        "producer": "analyze_mflow_divergence_score_v0_from_t02_real_input_v1.py",
        "scope": "MFLOW divergence_score v0 派生审计（基于 T02 real_input candidate）",
        "status": "started",
        "input_csv": str(input_csv).replace("\\", "/"),
        "output_dir": str(output_dir).replace("\\", "/"),
        "rule": {
            "price_ret": "(close-open)/open",
            "flow_ratio": "main_fund_net_inflow_ratio",
            "divergence_flag": "price_ret>0 & flow_ratio<0 OR price_ret<0 & flow_ratio>0",
            "score_v0": "min(1.0, abs(price_ret)*10 + abs(flow_ratio)*5) if divergence_flag else 0",
        },
    }

    if not input_csv.exists():
        summary["status"] = "failed"
        summary["failure_reason"] = "input_csv_not_found"
        write_json(summary_path, summary)
        return 2

    detail_cols = [
        "trade_date",
        "symbol",
        "symbol_name",
        "market_regime_label",
        "industry_name",
        "open",
        "close",
        "price_ret",
        "main_fund_net_inflow_ratio",
        "divergence_score_v0",
    ]
    with input_csv.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        required = ["trade_date", "symbol", "open", "close", "main_fund_net_inflow_ratio"]
        missing = [c for c in required if c not in fieldnames]
        if missing:
            summary["status"] = "failed"
            summary["failure_reason"] = "missing_required_columns"
            summary["missing_columns"] = missing
            write_json(summary_path, summary)
            return 4

        rows_joined = 0
        divergence_rows = 0
        c_price_up_flow_down = 0
        c_price_down_flow_up = 0
        score_sum_all = 0.0
        scores_divergence: list[float] = []
        detail_rows: list[dict[str, Any]] = []
        per_symbol: dict[str, dict[str, Any]] = {}

        corr_n = 0
        sum_x = 0.0
        sum_y = 0.0
        sum_x2 = 0.0
        sum_y2 = 0.0
        sum_xy = 0.0

        for row in reader:
            rows_joined += 1
            symbol = str(row.get("symbol", "")).strip()
            open_v = to_float(row.get("open"))
            close_v = to_float(row.get("close"))
            flow_ratio = to_float(row.get("main_fund_net_inflow_ratio"))

            price_ret: float | None = None
            if open_v is not None and close_v is not None and open_v != 0:
                price_ret = (close_v - open_v) / open_v

            divergence_flag = False
            if price_ret is not None and flow_ratio is not None:
                if price_ret > 0 and flow_ratio < 0:
                    divergence_flag = True
                    c_price_up_flow_down += 1
                elif price_ret < 0 and flow_ratio > 0:
                    divergence_flag = True
                    c_price_down_flow_up += 1

            score_v0 = 0.0
            if divergence_flag and price_ret is not None and flow_ratio is not None:
                score_v0 = abs(price_ret) * 10 + abs(flow_ratio) * 5
                if score_v0 > 1.0:
                    score_v0 = 1.0

            score_sum_all += score_v0

            if price_ret is not None and flow_ratio is not None:
                corr_n += 1
                sum_x += price_ret
                sum_y += flow_ratio
                sum_x2 += price_ret * price_ret
                sum_y2 += flow_ratio * flow_ratio
                sum_xy += price_ret * flow_ratio

            if divergence_flag:
                divergence_rows += 1
                scores_divergence.append(score_v0)
                detail_row: dict[str, Any] = {col: row.get(col, "") for col in detail_cols}
                detail_row["price_ret"] = price_ret
                detail_row["divergence_score_v0"] = score_v0
                detail_rows.append(detail_row)

                if symbol not in per_symbol:
                    per_symbol[symbol] = {"divergence_rows": 0, "score_sum": 0.0, "scores": []}
                per_symbol[symbol]["divergence_rows"] += 1
                per_symbol[symbol]["score_sum"] += score_v0
                per_symbol[symbol]["scores"].append(score_v0)

    corr = None
    if corr_n >= 2:
        num = corr_n * sum_xy - sum_x * sum_y
        den_x = corr_n * sum_x2 - sum_x * sum_x
        den_y = corr_n * sum_y2 - sum_y * sum_y
        if den_x > 0 and den_y > 0:
            corr = float(num / ((den_x ** 0.5) * (den_y ** 0.5)))

    detail_rows.sort(
        key=lambda r: (str(r.get("trade_date", "")), -float(r.get("divergence_score_v0") or 0.0))
    )
    write_tsv(detail_path, detail_rows, detail_cols)

    symbol_rows: list[dict[str, Any]] = []
    for symbol, payload in per_symbol.items():
        scores = list(payload["scores"])
        mean_score = float(payload["score_sum"] / payload["divergence_rows"]) if payload["divergence_rows"] else 0.0
        symbol_rows.append(
            {
                "symbol": symbol,
                "divergence_rows": int(payload["divergence_rows"]),
                "mean_score": mean_score,
                "p90_score": safe_quantile(scores, 0.9),
            }
        )

    symbol_rows.sort(key=lambda r: (int(r["divergence_rows"]), float(r["mean_score"])), reverse=True)
    write_tsv(per_symbol_path, symbol_rows, ["symbol", "divergence_rows", "mean_score", "p90_score"])

    summary["status"] = "success"
    summary["rows_joined"] = rows_joined
    summary["divergence_rows"] = divergence_rows
    summary["divergence_rate"] = float(divergence_rows / rows_joined) if rows_joined else 0.0
    summary["divergence_breakdown"] = {
        "price_up_flow_down": c_price_up_flow_down,
        "price_down_flow_up": c_price_down_flow_up,
    }
    summary["score_distribution"] = {
        "score_mean_all": float(score_sum_all / rows_joined) if rows_joined else 0.0,
        "score_mean_divergence_only": float(sum(scores_divergence) / divergence_rows) if divergence_rows else None,
        "score_p50_divergence_only": safe_quantile(scores_divergence, 0.5),
        "score_p90_divergence_only": safe_quantile(scores_divergence, 0.9),
        "score_p95_divergence_only": safe_quantile(scores_divergence, 0.95),
    }
    summary["corr_price_ret_vs_inflow_ratio"] = corr
    summary["output_files"] = {
        "summary_json": str(summary_path).replace("\\", "/"),
        "detail_tsv": str(detail_path).replace("\\", "/"),
        "symbol_counts_tsv": str(per_symbol_path).replace("\\", "/"),
    }

    write_json(summary_path, summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
