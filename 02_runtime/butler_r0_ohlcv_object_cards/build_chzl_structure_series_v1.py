from __future__ import annotations

import argparse
import csv
from pathlib import Path


REQUIRED_COLUMNS = {"date", "open", "high", "low", "close", "volume", "symbol"}
OUTPUT_COLUMNS = [
    "symbol",
    "timeframe",
    "bar_date",
    "fractal_type",
    "bi_direction",
    "zs_state",
    "zs_zg",
    "zs_zd",
    "divergence_flag",
    "bsd_type",
    "stop_logic",
    "note",
    "source_mode",
    "bi_start_date",
    "bi_end_date",
    "bi_start_price",
    "bi_end_price",
    "fractal_price",
]


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f"input csv has no rows: {csv_path}")
    missing = REQUIRED_COLUMNS - set(rows[0].keys())
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")
    return rows


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


def detect_fractals(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    fractals: list[dict[str, object]] = []
    for i in range(1, len(rows) - 1):
        prev_row, row, next_row = rows[i - 1], rows[i], rows[i + 1]
        high = f(row, "high")
        low = f(row, "low")
        if (
            high > f(prev_row, "high")
            and high > f(next_row, "high")
            and low > f(prev_row, "low")
            and low > f(next_row, "low")
        ):
            fractals.append(
                {
                    "idx": i,
                    "bar_date": row["date"],
                    "type": "top",
                    "price": high,
                    "symbol": row["symbol"],
                }
            )
        elif (
            low < f(prev_row, "low")
            and low < f(next_row, "low")
            and high < f(prev_row, "high")
            and high < f(next_row, "high")
        ):
            fractals.append(
                {
                    "idx": i,
                    "bar_date": row["date"],
                    "type": "bottom",
                    "price": low,
                    "symbol": row["symbol"],
                }
            )
    return fractals


def form_bis(fractals: list[dict[str, object]]) -> list[dict[str, object]]:
    if len(fractals) < 2:
        return []
    bis: list[dict[str, object]] = []
    start = fractals[0]
    for curr in fractals[1:]:
        if start["type"] == "bottom" and curr["type"] == "top":
            direction = "up"
        elif start["type"] == "top" and curr["type"] == "bottom":
            direction = "down"
        else:
            continue
        bis.append(
            {
                "start_idx": start["idx"],
                "end_idx": curr["idx"],
                "start_date": start["bar_date"],
                "end_date": curr["bar_date"],
                "direction": direction,
                "high": max(float(start["price"]), float(curr["price"])),
                "low": min(float(start["price"]), float(curr["price"])),
                "start_price": float(start["price"]),
                "end_price": float(curr["price"]),
                "fractal_type": curr["type"],
                "fractal_price": float(curr["price"]),
                "symbol": curr["symbol"],
            }
        )
        start = curr
    return bis


def simulate_zhongshu(recent_bis: list[dict[str, object]]) -> dict[str, object] | None:
    if len(recent_bis) < 3:
        return None
    zg = min(float(b["high"]) for b in recent_bis[-3:])
    zd = max(float(b["low"]) for b in recent_bis[-3:])
    if zg <= zd:
        return None
    return {"state": "active", "zg": zg, "zd": zd}


def detect_auto_bsd(
    bis: list[dict[str, object]],
    idx: int,
    zs: dict[str, object] | None,
    prev_buy_low: float | None,
) -> tuple[str, str, bool, float | None]:
    last_bi = bis[idx]
    prev_bi = bis[idx - 1] if idx >= 1 else None
    bsd_type = "NONE"
    stop_logic = ""
    divergence_flag = False
    next_prev_buy_low = prev_buy_low

    if last_bi["direction"] == "up" and prev_bi and prev_bi["direction"] == "down":
        if float(prev_bi["end_price"]) < float(prev_bi["start_price"]):
            bsd_type = "1B"
            stop_logic = "FRACTAL_BREAK"
            divergence_flag = True
            next_prev_buy_low = float(prev_bi["end_price"])

    if last_bi["direction"] == "down" and prev_bi and prev_bi["direction"] == "up":
        if prev_buy_low is not None and float(last_bi["end_price"]) > prev_buy_low:
            bsd_type = "2B"
            stop_logic = "PREV_SWING"
            divergence_flag = True

    if last_bi["direction"] == "up" and prev_bi and prev_bi["direction"] == "up" and zs:
        if float(prev_bi["end_price"]) > float(zs["zg"]) and float(last_bi["low"]) > float(zs["zg"]):
            bsd_type = "3B"
            stop_logic = "ZS_REENTRY"
            divergence_flag = True

    return bsd_type, stop_logic, divergence_flag, next_prev_buy_low


def build_structure_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    fractals = detect_fractals(rows)
    bis = form_bis(fractals)
    structure_rows: list[dict[str, str]] = []
    prev_buy_low: float | None = None
    symbol = rows[-1]["symbol"]

    for idx, bi in enumerate(bis):
        zs = simulate_zhongshu(bis[: idx + 1])
        bsd_type, stop_logic, divergence_flag, prev_buy_low = detect_auto_bsd(bis, idx, zs, prev_buy_low)
        structure_rows.append(
            {
                "symbol": symbol,
                "timeframe": "1d",
                "bar_date": str(bi["end_date"]),
                "fractal_type": str(bi["fractal_type"]),
                "bi_direction": str(bi["direction"]),
                "zs_state": str(zs["state"]) if zs else "inactive",
                "zs_zg": f"{float(zs['zg']):.4f}" if zs else "",
                "zs_zd": f"{float(zs['zd']):.4f}" if zs else "",
                "divergence_flag": "true" if divergence_flag else "false",
                "bsd_type": bsd_type,
                "stop_logic": stop_logic,
                "note": "auto_structure_series_v1",
                "source_mode": "auto_series",
                "bi_start_date": str(bi["start_date"]),
                "bi_end_date": str(bi["end_date"]),
                "bi_start_price": f"{float(bi['start_price']):.4f}",
                "bi_end_price": f"{float(bi['end_price']):.4f}",
                "fractal_price": f"{float(bi['fractal_price']):.4f}",
            }
        )
    return structure_rows


def write_rows(output_tsv: Path, rows: list[dict[str, str]]) -> None:
    output_tsv.parent.mkdir(parents=True, exist_ok=True)
    with output_tsv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build semi-auto CHZL_BSD structure series from daily OHLCV.")
    parser.add_argument("--daily-csv", required=True)
    parser.add_argument("--output-tsv", required=True)
    args = parser.parse_args()

    rows = load_rows(Path(args.daily_csv))
    structure_rows = build_structure_rows(rows)
    if not structure_rows:
        raise ValueError("no structure rows generated")
    write_rows(Path(args.output_tsv), structure_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
