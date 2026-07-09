from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

import pandas as pd


if not os.environ.get("ALLOW_ARCHIVE_ONLY_RUN"):
    raise RuntimeError("ARCHIVE_ONLY: legacy tool. Set ALLOW_ARCHIVE_ONLY_RUN=1 to run intentionally.")

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from tk_r4_usd_half_risk_scheme_b import default_out_dir, default_position_level_csv, format_terminal_summary, run_scheme_b
from tk_r4_usd_half_risk_role_finalize import format_terminal_role_summary, run_role_finalize
from tk_r4_usd_overlap_heterogeneity_audit import run_heterogeneity
from tk_r4_usd_overlap_negative_pockets import run_negative_pockets
from tk_r4_risk_corr_audit import run_risk_corr_audit


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Wrapper/orchestrator for TK-R4 USD-only Scheme B runs.")
    p.add_argument("--preset", default="", choices=["", "fast", "full"])
    p.add_argument("--split", default="all", choices=["since2022", "pre2022", "all"])
    p.add_argument("--mode", default="both", choices=["off", "on", "both"])
    p.add_argument("--date_tag", default="20260611")
    p.add_argument("--half_risk_scale", type=float, default=0.5)
    p.add_argument("--finalize_role", type=int, default=1)
    p.add_argument("--support_min", type=int, default=3)
    p.add_argument("--ensure_watchlist", type=int, default=1)
    p.add_argument("--ensure_position_level", type=int, default=0)
    p.add_argument("--p0_sweep_dir", default=str(Path("backtest_out") / "p0_sweep"))
    p.add_argument("--print_coverage", type=int, default=1)
    p.add_argument("--validate_off_equals_baseline", type=int, default=1)
    p.add_argument("--write_manifest", type=int, default=1)
    p.add_argument(
        "--out_root",
        default=str(Path("backtest_out") / "stage2" / "indicator_audit"),
        help="Base directory used when auto-building out_dir paths.",
    )
    return p.parse_args()


def _splits(split: str) -> list[str]:
    if split == "all":
        return ["since2022", "pre2022"]
    return [split]


def _modes(mode: str) -> list[bool]:
    if mode == "both":
        return [False, True]
    return [mode == "on"]


def _auto_out_dir(out_root: Path, split: str, enabled: bool, date_tag: str) -> Path:
    auto_dir = default_out_dir(split=split, enable_usd_half_risk=enabled, date_tag=date_tag)
    return out_root / auto_dir.name


def _find_existing_watchlist(out_root: Path, date_tag: str) -> Path | None:
    direct = out_root / f"{date_tag}_b123_tk_r4_usd_overlap_negative_pockets_v1" / f"b123_usd_overlap_negative_watchlist_{date_tag}_v1.csv"
    if direct.exists():
        return direct
    name = f"b123_usd_overlap_negative_watchlist_{date_tag}_v1.csv"
    candidates = list(out_root.rglob(name))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def _ensure_watchlist(out_root: Path, date_tag: str, half_risk_scale: float, support_min: int) -> tuple[Path | None, str]:
    existing = _find_existing_watchlist(out_root=out_root, date_tag=date_tag)
    if existing is not None:
        return existing, "existing"

    for split in ["since2022", "pre2022"]:
        b122_dir = out_root / f"{date_tag}_b122_tk_r4_usd_overlap_heterogeneity_{split}_v1"
        b122_symbol = b122_dir / f"b122_usd_overlap_by_symbol_{date_tag}_v1.csv"
        b122_profile_symbol = b122_dir / f"b122_usd_overlap_profile_symbol_{date_tag}_v1.csv"
        if not (b122_symbol.exists() and b122_profile_symbol.exists()):
            position_level_csv = default_position_level_csv(split=split, date_tag=date_tag)
            if not position_level_csv.exists():
                return None, "missing_position_level"
            run_heterogeneity(
                position_level_csv=position_level_csv,
                out_dir=b122_dir,
                date_tag=date_tag,
                half_risk_scale=float(half_risk_scale),
                support_min=int(support_min),
            )

    since_dir = out_root / f"{date_tag}_b122_tk_r4_usd_overlap_heterogeneity_since2022_v1"
    pre_dir = out_root / f"{date_tag}_b122_tk_r4_usd_overlap_heterogeneity_pre2022_v1"
    since_symbol_csv = since_dir / f"b122_usd_overlap_by_symbol_{date_tag}_v1.csv"
    pre_symbol_csv = pre_dir / f"b122_usd_overlap_by_symbol_{date_tag}_v1.csv"
    since_profile_symbol_csv = since_dir / f"b122_usd_overlap_profile_symbol_{date_tag}_v1.csv"
    pre_profile_symbol_csv = pre_dir / f"b122_usd_overlap_profile_symbol_{date_tag}_v1.csv"
    if not (since_symbol_csv.exists() and pre_symbol_csv.exists() and since_profile_symbol_csv.exists() and pre_profile_symbol_csv.exists()):
        return None, "missing_inputs"

    b123_dir = out_root / f"{date_tag}_b123_tk_r4_usd_overlap_negative_pockets_v1"
    _out_neg, out_watch, _out_sum, _neg_df, _watch_df, _summary_df = run_negative_pockets(
        since_symbol_csv=since_symbol_csv,
        pre_symbol_csv=pre_symbol_csv,
        since_profile_symbol_csv=since_profile_symbol_csv,
        pre_profile_symbol_csv=pre_profile_symbol_csv,
        out_dir=b123_dir,
        date_tag=date_tag,
        support_min=int(support_min),
    )
    out_watch = Path(out_watch)
    return (out_watch if out_watch.exists() else None), "generated"


def _coverage_from_position_level_csv(position_level_csv: Path) -> dict[str, object]:
    if not position_level_csv.exists():
        return {"exists": False}
    df = pd.read_csv(position_level_csv, usecols=lambda c: c in {"symbol", "profile", "split"})
    if df.empty:
        return {"exists": True, "n_positions": 0, "n_symbols": 0, "n_profiles": 0, "symbols": ""}
    symbols = sorted(set(df["symbol"].astype(str)))
    profiles = sorted(set(df["profile"].astype(str))) if "profile" in df.columns else []
    split_vals = sorted(set(df["split"].astype(str))) if "split" in df.columns else []
    return {
        "exists": True,
        "split_vals": " | ".join(split_vals[:4]),
        "n_positions": int(len(df)),
        "n_symbols": int(len(symbols)),
        "n_profiles": int(len(profiles)),
        "symbols": " | ".join(symbols[:20]),
    }


def _watchlist_brief(watch_contract_df) -> str:
    if watch_contract_df is None or watch_contract_df.empty:
        return "watchlist: empty"
    lines = ["watchlist:"]
    counts = (
        watch_contract_df.groupby(["scope", "priority"], sort=True)
        .size()
        .reset_index(name="n")
        .sort_values(["scope", "priority"], kind="mergesort")
    )
    for _, r in counts.iterrows():
        lines.append(f"  {r['scope']} {r['priority']}: {int(r['n'])}")
    sym = watch_contract_df.loc[watch_contract_df["scope"] == "symbol"].copy()
    if not sym.empty:
        keys = list(sym["group_key"].astype(str).head(10))
        lines.append("  symbol_top: " + " | ".join(keys))
    ps = watch_contract_df.loc[
        (watch_contract_df["scope"] == "profile_symbol")
        & (watch_contract_df["priority"] == "high_watch")
    ].copy()
    if not ps.empty:
        keys = list(ps["group_key"].astype(str).head(10))
        lines.append("  profile_symbol_high_watch_top: " + " | ".join(keys))
    return "\n".join(lines)


def _bucket_of_path(p: str) -> str:
    s = str(p).replace("/", "\\")
    base = Path(s).name
    if "_b118_" in s or base.startswith("b118_"):
        return "b118"
    if "_b120_" in s or base.startswith("b120_"):
        return "b120"
    if "_b122_" in s or base.startswith("b122_"):
        return "b122"
    if "_b123_" in s or base.startswith("b123_"):
        return "b123"
    if "_b124_" in s or base.startswith("b124_"):
        return "b124"
    return "other"


def _group_outputs(outputs: list[str]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {"b118": [], "b120": [], "b122": [], "b123": [], "b124": [], "other": []}
    for p in sorted(set(outputs)):
        grouped[_bucket_of_path(p)].append(p)
    return {k: v for k, v in grouped.items() if v}


def _find_latest_by_name(out_root: Path, filename: str) -> Path | None:
    candidates = list(out_root.rglob(filename))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def _find_direct_or_latest(out_root: Path, direct: Path, filename: str) -> Path | None:
    if direct.exists():
        return direct
    return _find_latest_by_name(out_root=out_root, filename=filename)


def _build_inputs_index(out_root: Path, date_tag: str, watchlist_csv: Path | None) -> dict[str, object]:
    idx: dict[str, object] = {}

    b118: dict[str, str] = {}
    for split in ["since2022", "pre2022"]:
        direct = out_root / f"{date_tag}_b118_tk_r4_risk_corr_{split}_v1" / f"b118_position_level_{date_tag}_v1.csv"
        found = _find_direct_or_latest(out_root=out_root, direct=direct, filename=f"b118_position_level_{date_tag}_v1.csv")
        b118[f"{split}_position_level_csv"] = "" if found is None else str(found)
    idx["b118"] = b118

    b122: dict[str, str] = {}
    for split in ["since2022", "pre2022"]:
        direct_dir = out_root / f"{date_tag}_b122_tk_r4_usd_overlap_heterogeneity_{split}_v1"
        by_symbol = _find_direct_or_latest(
            out_root=out_root,
            direct=direct_dir / f"b122_usd_overlap_by_symbol_{date_tag}_v1.csv",
            filename=f"b122_usd_overlap_by_symbol_{date_tag}_v1.csv",
        )
        by_ps = _find_direct_or_latest(
            out_root=out_root,
            direct=direct_dir / f"b122_usd_overlap_profile_symbol_{date_tag}_v1.csv",
            filename=f"b122_usd_overlap_profile_symbol_{date_tag}_v1.csv",
        )
        b122[f"{split}_by_symbol_csv"] = "" if by_symbol is None else str(by_symbol)
        b122[f"{split}_profile_symbol_csv"] = "" if by_ps is None else str(by_ps)
    idx["b122"] = b122

    b123: dict[str, str] = {}
    if watchlist_csv is not None:
        b123["watchlist_csv"] = str(watchlist_csv)
        b123_dir = watchlist_csv.parent
        neg = b123_dir / f"b123_usd_overlap_negative_pockets_{date_tag}_v1.csv"
        summ = b123_dir / f"b123_usd_overlap_negative_summary_{date_tag}_v1.csv"
        b123["negative_pockets_csv"] = str(neg) if neg.exists() else ""
        b123["summary_csv"] = str(summ) if summ.exists() else ""
    else:
        found_watch = _find_latest_by_name(out_root=out_root, filename=f"b123_usd_overlap_negative_watchlist_{date_tag}_v1.csv")
        b123["watchlist_csv"] = "" if found_watch is None else str(found_watch)
        if found_watch is not None:
            b123_dir = found_watch.parent
            neg = b123_dir / f"b123_usd_overlap_negative_pockets_{date_tag}_v1.csv"
            summ = b123_dir / f"b123_usd_overlap_negative_summary_{date_tag}_v1.csv"
            b123["negative_pockets_csv"] = str(neg) if neg.exists() else ""
            b123["summary_csv"] = str(summ) if summ.exists() else ""
        else:
            b123["negative_pockets_csv"] = ""
            b123["summary_csv"] = ""
    idx["b123"] = b123

    return idx


def _format_inputs_index(idx: dict[str, object]) -> str:
    lines: list[str] = ["inputs_index:"]
    b118 = idx.get("b118", {})
    if isinstance(b118, dict):
        for k in ["since2022_position_level_csv", "pre2022_position_level_csv"]:
            v = str(b118.get(k, "")).strip()
            lines.append(f"  b118 {k}: {v}")
    b122 = idx.get("b122", {})
    if isinstance(b122, dict):
        for split in ["since2022", "pre2022"]:
            v1 = str(b122.get(f"{split}_by_symbol_csv", "")).strip()
            v2 = str(b122.get(f"{split}_profile_symbol_csv", "")).strip()
            lines.append(f"  b122 {split}_by_symbol_csv: {v1}")
            lines.append(f"  b122 {split}_profile_symbol_csv: {v2}")
    b123 = idx.get("b123", {})
    if isinstance(b123, dict):
        for k in ["watchlist_csv", "negative_pockets_csv", "summary_csv"]:
            v = str(b123.get(k, "")).strip()
            lines.append(f"  b123 {k}: {v}")
    return "\n".join(lines)


def _validate_off_equals_baseline(summary_df: pd.DataFrame) -> dict[str, object]:
    sub = summary_df.loc[summary_df["scenario"] == "scheme_b_minus_base"]
    if sub.empty:
        return {"ok": False, "reason": "missing_scheme_b_minus_base"}
    r = sub.iloc[0].to_dict()
    sum_pnl = float(pd.to_numeric(pd.Series([r.get("sum_pnl")]), errors="coerce").iloc[0])
    max_dd = float(pd.to_numeric(pd.Series([r.get("max_drawdown_pnl")]), errors="coerce").iloc[0])
    avg_r = float(pd.to_numeric(pd.Series([r.get("avg_r_mult")]), errors="coerce").iloc[0])
    eps = 1e-9
    ok = (abs(sum_pnl) <= eps) and (abs(max_dd) <= eps) and (abs(avg_r) <= eps)
    return {
        "ok": bool(ok),
        "eps": eps,
        "delta_sum_pnl": sum_pnl,
        "delta_max_drawdown_pnl": max_dd,
        "delta_avg_r_mult": avg_r,
    }


def main() -> None:
    args = parse_args()
    if str(args.preset).strip().lower() == "fast":
        args.split = "all"
        args.mode = "both"
        args.finalize_role = 1
        args.ensure_watchlist = 1
        args.print_coverage = 1
        args.write_manifest = 1
    if str(args.preset).strip().lower() == "full":
        args.split = "all"
        args.mode = "both"
        args.finalize_role = 1
        args.ensure_watchlist = 1
        args.ensure_position_level = 1
        args.print_coverage = 1
        args.write_manifest = 1
    date_tag = str(args.date_tag).strip()
    out_root = Path(args.out_root)

    on_outputs: dict[str, dict[str, Path]] = {}
    all_outputs: list[str] = []
    coverage_rows: list[str] = []
    coverage_json: dict[str, dict[str, object]] = {}
    validation_json: dict[str, dict[str, object]] = {}
    validation_rows: list[str] = []
    provenance: dict[str, object] = {"position_level": {}, "b122": {}, "b123": "unknown", "b124": "unknown"}
    for split in _splits(str(args.split).strip().lower()):
        position_level_csv = default_position_level_csv(split=split, date_tag=date_tag)
        pl_pre_exists = position_level_csv.exists()
        if bool(int(args.ensure_position_level)) and not position_level_csv.exists():
            b118_dir = out_root / f"{date_tag}_b118_tk_r4_risk_corr_{split}_v1"
            run_risk_corr_audit(
                p0_sweep_dir=args.p0_sweep_dir,
                split=split,
                out_dir=b118_dir,
                date_tag=date_tag,
            )
            position_level_csv = default_position_level_csv(split=split, date_tag=date_tag)
        if position_level_csv.exists():
            provenance["position_level"][str(split)] = "existing" if pl_pre_exists else "generated"
        else:
            provenance["position_level"][str(split)] = "missing"
        if bool(int(args.print_coverage)):
            cov = _coverage_from_position_level_csv(position_level_csv)
            coverage_json[str(split)] = cov
            if cov.get("exists"):
                line = (
                    f"coverage split={split}: "
                    f"positions={cov.get('n_positions')}, "
                    f"symbols={cov.get('n_symbols')}, "
                    f"profiles={cov.get('n_profiles')}, "
                    f"symbols_top={cov.get('symbols')}"
                )
            else:
                line = f"coverage split={split}: missing position_level_csv={position_level_csv}"
            coverage_rows.append(line)
            print(line)
        for enabled in _modes(str(args.mode).strip().lower()):
            out_cfg, out_rows, out_sum, summary_df = run_scheme_b(
                position_level_csv=position_level_csv,
                out_dir=_auto_out_dir(out_root=out_root, split=split, enabled=enabled, date_tag=date_tag),
                date_tag=date_tag,
                enable_usd_half_risk=enabled,
                half_risk_scale=float(args.half_risk_scale),
            )
            print(format_terminal_summary(summary_df, split=split, enabled=enabled))
            if (not enabled) and bool(int(args.validate_off_equals_baseline)):
                v = _validate_off_equals_baseline(summary_df)
                validation_json[str(split)] = v
                line = (
                    f"validation split={split} off_equals_baseline="
                    + ("ok" if bool(v.get("ok")) else "fail")
                    + f" delta_sum_pnl={float(v.get('delta_sum_pnl', float('nan'))):+.6f}"
                    + f" delta_max_dd={float(v.get('delta_max_drawdown_pnl', float('nan'))):+.6f}"
                    + f" delta_avg_r={float(v.get('delta_avg_r_mult', float('nan'))):+.12f}"
                )
                validation_rows.append(line)
                print(line)
            print(out_cfg)
            print(out_rows)
            print(out_sum)
            all_outputs.extend([str(out_cfg), str(out_rows), str(out_sum)])
            if enabled:
                on_outputs[str(split)] = {"out_cfg": Path(out_cfg), "out_sum": Path(out_sum)}

    if bool(int(args.finalize_role)):
        if ("since2022" in on_outputs) and ("pre2022" in on_outputs):
            watchlist_csv = None
            watchlist_source = "unknown"
            if bool(int(args.ensure_watchlist)):
                pre_b122: dict[str, bool] = {}
                for split in ["since2022", "pre2022"]:
                    b122_dir = out_root / f"{date_tag}_b122_tk_r4_usd_overlap_heterogeneity_{split}_v1"
                    pre_b122[str(split)] = (
                        (b122_dir / f"b122_usd_overlap_by_symbol_{date_tag}_v1.csv").exists()
                        and (b122_dir / f"b122_usd_overlap_profile_symbol_{date_tag}_v1.csv").exists()
                    )
                pre_b123 = _find_existing_watchlist(out_root=out_root, date_tag=date_tag) is not None
                watchlist_csv, watchlist_source = _ensure_watchlist(
                    out_root=out_root,
                    date_tag=date_tag,
                    half_risk_scale=float(args.half_risk_scale),
                    support_min=int(args.support_min),
                )
                if watchlist_source == "missing_position_level" and bool(int(args.ensure_position_level)):
                    for split in ["since2022", "pre2022"]:
                        b118_dir = out_root / f"{date_tag}_b118_tk_r4_risk_corr_{split}_v1"
                        run_risk_corr_audit(
                            p0_sweep_dir=args.p0_sweep_dir,
                            split=split,
                            out_dir=b118_dir,
                            date_tag=date_tag,
                        )
                    watchlist_csv, watchlist_source = _ensure_watchlist(
                        out_root=out_root,
                        date_tag=date_tag,
                        half_risk_scale=float(args.half_risk_scale),
                        support_min=int(args.support_min),
                    )
                for split in ["since2022", "pre2022"]:
                    b122_dir = out_root / f"{date_tag}_b122_tk_r4_usd_overlap_heterogeneity_{split}_v1"
                    now_b122 = (
                        (b122_dir / f"b122_usd_overlap_by_symbol_{date_tag}_v1.csv").exists()
                        and (b122_dir / f"b122_usd_overlap_profile_symbol_{date_tag}_v1.csv").exists()
                    )
                    if pre_b122.get(str(split)) and now_b122:
                        provenance["b122"][str(split)] = "existing"
                    elif (not pre_b122.get(str(split))) and now_b122:
                        provenance["b122"][str(split)] = "generated"
                    else:
                        provenance["b122"][str(split)] = "missing"
                if watchlist_source == "existing":
                    provenance["b123"] = "existing"
                elif watchlist_source == "generated":
                    provenance["b123"] = "generated"
                else:
                    provenance["b123"] = "missing" if not pre_b123 else "existing"
            if watchlist_csv is None:
                watchlist_csv = _find_existing_watchlist(out_root=out_root, date_tag=date_tag)
                watchlist_source = "existing" if watchlist_csv is not None else watchlist_source
            if watchlist_csv is None:
                print("usd_half_risk_role_finalize skipped (watchlist not found)")
                return
            role_out_dir = out_root / f"{date_tag}_b124_tk_r4_usd_half_risk_role_finalize_v1"
            out_role, out_watch, out_val, role_df, watch_contract_df, validation_df = run_role_finalize(
                since_config_csv=on_outputs["since2022"]["out_cfg"],
                since_summary_csv=on_outputs["since2022"]["out_sum"],
                pre_summary_csv=on_outputs["pre2022"]["out_sum"],
                watchlist_csv=watchlist_csv,
                out_dir=role_out_dir,
                date_tag=date_tag,
            )
            print(f"watchlist_csv={watchlist_csv} source={watchlist_source}")
            print(
                "provenance: "
                + f"b118_position_level={provenance.get('position_level')}, "
                + f"b122={provenance.get('b122')}, "
                + f"b123_watchlist={provenance.get('b123')}"
            )
            role_text = format_terminal_role_summary(role_df, validation_df, watch_contract_df)
            watch_text = _watchlist_brief(watch_contract_df)
            print(role_text)
            print(watch_text)

            all_outputs.extend([str(out_role), str(out_watch), str(out_val)])
            provenance["b124"] = "generated"

            cmd_fast = (
                ".\\.venv\\Scripts\\python.exe .\\tk_r4_usd_half_risk_scheme_b_runner.py "
                f"--split all --mode both --date_tag {date_tag} "
                f"--finalize_role 1 --ensure_watchlist 1 --support_min {int(args.support_min)}"
            )
            cmd_full = cmd_fast + f" --ensure_position_level 1 --p0_sweep_dir {args.p0_sweep_dir}"
            cmd_fast_preset = (
                ".\\.venv\\Scripts\\python.exe .\\tk_r4_usd_half_risk_scheme_b_runner.py "
                f"--preset fast --date_tag {date_tag} --support_min {int(args.support_min)}"
            )
            cmd_full_preset = (
                ".\\.venv\\Scripts\\python.exe .\\tk_r4_usd_half_risk_scheme_b_runner.py "
                f"--preset full --date_tag {date_tag} --support_min {int(args.support_min)} --p0_sweep_dir {args.p0_sweep_dir}"
            )
            print("repro_cmd_fast: " + cmd_fast)
            print("repro_cmd_full: " + cmd_full)
            print("repro_cmd_fast_preset: " + cmd_fast_preset)
            print("repro_cmd_full_preset: " + cmd_full_preset)

            brief_path = role_out_dir / f"b124_usd_half_risk_terminal_brief_{date_tag}_v1.txt"
            brief_path.write_text(
                "\n".join(
                    [
                        f"watchlist_csv={watchlist_csv} source={watchlist_source}",
                        *coverage_rows,
                        *validation_rows,
                        role_text,
                        watch_text,
                        "repro_cmd_fast: " + cmd_fast,
                        "repro_cmd_full: " + cmd_full,
                        "repro_cmd_fast_preset: " + cmd_fast_preset,
                        "repro_cmd_full_preset: " + cmd_full_preset,
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            print(brief_path)
            print(out_role)
            print(out_watch)
            print(out_val)

            if bool(int(args.write_manifest)):
                manifest_path = role_out_dir / f"b124_usd_half_risk_run_manifest_{date_tag}_v1.json"
                outputs_all = sorted(set(all_outputs + [str(brief_path)]))
                inputs_index = _build_inputs_index(out_root=out_root, date_tag=date_tag, watchlist_csv=Path(watchlist_csv) if watchlist_csv else None)
                missing_inputs: list[str] = []
                for k, v in inputs_index.items():
                    if isinstance(v, dict):
                        for kk, vv in v.items():
                            if isinstance(vv, str) and vv.strip() == "":
                                missing_inputs.append(f"{k}.{kk}")
                inputs_text = _format_inputs_index(inputs_index)
                print(inputs_text)
                brief_path.write_text(brief_path.read_text(encoding="utf-8") + inputs_text + "\n", encoding="utf-8")
                validation_failed = False
                for _split, v in validation_json.items():
                    if isinstance(v, dict) and (v.get("ok") is False):
                        validation_failed = True
                        break
                if missing_inputs:
                    status = "missing_inputs"
                elif validation_failed:
                    status = "validation_failed"
                else:
                    status = "ok"
                manifest = {
                    "tool": "tk_r4_usd_half_risk_scheme_b_runner",
                    "date_tag": date_tag,
                    "preset": str(args.preset).strip(),
                    "out_root": str(out_root),
                    "p0_sweep_dir": str(args.p0_sweep_dir),
                    "support_min": int(args.support_min),
                    "half_risk_scale": float(args.half_risk_scale),
                    "ensure_position_level": bool(int(args.ensure_position_level)),
                    "ensure_watchlist": bool(int(args.ensure_watchlist)),
                    "print_coverage": bool(int(args.print_coverage)),
                    "validate_off_equals_baseline": bool(int(args.validate_off_equals_baseline)),
                    "finalize_role": bool(int(args.finalize_role)),
                    "watchlist_csv": str(watchlist_csv),
                    "watchlist_source": watchlist_source,
                    "provenance": provenance,
                    "coverage": coverage_json,
                    "validation": validation_json,
                    "inputs_index": inputs_index,
                    "repro_cmd_fast": cmd_fast,
                    "repro_cmd_full": cmd_full,
                    "repro_cmd_fast_preset": cmd_fast_preset,
                    "repro_cmd_full_preset": cmd_full_preset,
                    "outputs": outputs_all,
                    "outputs_grouped": _group_outputs(outputs_all),
                    "missing_inputs": missing_inputs,
                    "status": status,
                }
                manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                print(manifest_path)
        else:
            print("usd_half_risk_role_finalize skipped (need since2022+pre2022 enabled=1 runs)")


if __name__ == "__main__":
    main()
