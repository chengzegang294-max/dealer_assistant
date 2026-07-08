from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


CATALOG_HEADERS = [
    "symbol",
    "timeframe",
    "provider",
    "date_range",
    "repo_path",
    "source_type",
    "source_csv",
    "source_metadata",
    "generator_entry",
    "current_role",
    "evidence_mode",
    "note",
]

OUTPUT_HEADERS = [
    "date",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "amount",
    "pct_chg",
    "symbol",
    "provider_code",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def normalize_symbol(symbol: str) -> tuple[str, str]:
    symbol = symbol.strip().upper()
    if "." not in symbol:
        raise ValueError("baostock requires symbol like 300302.SZ or 600000.SH")
    code, market = symbol.split(".")
    market_map = {"SH": "sh", "SZ": "sz"}
    if market not in market_map:
        raise ValueError(f"unsupported market suffix: {market}")
    return symbol, f"{market_map[market]}.{code}"


def to_dash_date(yyyymmdd: str) -> str:
    if len(yyyymmdd) != 8 or not yyyymmdd.isdigit():
        raise ValueError(f"invalid yyyymmdd date: {yyyymmdd}")
    return f"{yyyymmdd[:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:8]}"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def read_catalog(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader)


def write_catalog(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CATALOG_HEADERS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def upsert_catalog_row(path: Path, new_row: dict[str, str]) -> None:
    rows = read_catalog(path)
    replaced = False
    for idx, row in enumerate(rows):
        if row.get("repo_path") == new_row["repo_path"]:
            rows[idx] = new_row
            replaced = True
            break
    if not replaced:
        rows.append(new_row)
    rows.sort(key=lambda r: (r["symbol"], r["date_range"], r["provider"], r["repo_path"]))
    write_catalog(path, rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch A-share daily OHLCV from BaoStock into formal runtime raw input.")
    parser.add_argument("--symbol", required=True, help="e.g. 300302.SZ")
    parser.add_argument("--start-date", required=True, help="YYYYMMDD")
    parser.add_argument("--end-date", required=True, help="YYYYMMDD")
    parser.add_argument(
        "--output-dir",
        default="02_runtime/butler_r0_ohlcv_object_cards/data/raw/daily_ohlcv",
        help="Repo-relative output directory for formal raw daily OHLCV input.",
    )
    args = parser.parse_args()

    repo = repo_root()
    symbol, bs_symbol = normalize_symbol(args.symbol)
    start_date = to_dash_date(args.start_date)
    end_date = to_dash_date(args.end_date)

    output_dir = (repo / args.output_dir).resolve()
    date_tag = f"{args.start_date}_{args.end_date}"
    base_name = f"{symbol.replace('.', '_')}__1d__baostock__{date_tag}"
    csv_path = output_dir / f"{base_name}.csv"
    meta_path = output_dir / f"{base_name}__metadata.json"
    catalog_path = output_dir / "catalog_v1.tsv"
    generator_rel = "02_runtime/butler_r0_ohlcv_object_cards/baostock_daily_fetch_to_raw_v1.py"
    repo_csv = str(csv_path.relative_to(repo)).replace("\\", "/")
    repo_meta = str(meta_path.relative_to(repo)).replace("\\", "/")

    metadata: dict[str, Any] = {
        "fetch_name": "baostock_daily_fetch_to_raw_v1",
        "symbol": symbol,
        "bs_symbol": bs_symbol,
        "timeframe": "1d",
        "provider": "Baostock",
        "start_date": args.start_date,
        "end_date": args.end_date,
        "producer": "baostock_daily_fetch_to_raw_v1.py",
        "repo_role": "formal_raw_daily_ohlcv",
        "catalog_path": str(catalog_path.relative_to(repo)).replace("\\", "/"),
        "output_csv": repo_csv,
        "status": "started",
    }

    try:
        import baostock as bs  # type: ignore
    except Exception as exc:  # pragma: no cover
        metadata["status"] = "failed"
        metadata["failure_reason"] = "baostock_import_failed"
        metadata["failure_detail"] = str(exc)
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

        rows: list[dict[str, str]] = []
        while rs.next():
            raw = dict(zip(rs.fields, rs.get_row_data()))
            rows.append(
                {
                    "date": raw["date"],
                    "open": raw["open"],
                    "high": raw["high"],
                    "low": raw["low"],
                    "close": raw["close"],
                    "volume": raw["volume"],
                    "amount": raw["amount"],
                    "pct_chg": raw["pctChg"],
                    "symbol": symbol,
                    "provider_code": raw["code"],
                }
            )

        if not rows:
            metadata["status"] = "failed"
            metadata["failure_reason"] = "empty_dataframe"
            write_json(meta_path, metadata)
            return 5

        write_csv(csv_path, rows)

        metadata["status"] = "success"
        metadata["rows"] = len(rows)
        metadata["columns"] = OUTPUT_HEADERS
        metadata["first_trade_date"] = rows[0]["date"]
        metadata["last_trade_date"] = rows[-1]["date"]
        write_json(meta_path, metadata)

        upsert_catalog_row(
            catalog_path,
            {
                "symbol": symbol,
                "timeframe": "1d",
                "provider": "Baostock",
                "date_range": f"{args.start_date}-{args.end_date}",
                "repo_path": repo_csv,
                "source_type": "formal_fetch",
                "source_csv": repo_csv,
                "source_metadata": repo_meta,
                "generator_entry": generator_rel,
                "current_role": "formal_online_input",
                "evidence_mode": "hard",
                "note": "由当前终端通过 Baostock 正式拉取并自动写入 catalog，可直接供后续 runtime 引用",
            },
        )
        return 0
    except Exception as exc:  # pragma: no cover
        metadata["status"] = "failed"
        metadata["failure_reason"] = "baostock_api_error"
        metadata["failure_detail"] = str(exc)
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
