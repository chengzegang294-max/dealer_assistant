from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Set, Tuple


@dataclass(frozen=True)
class ExtractionResult:
    name: str
    input_path: Path
    output_path: Path
    symbol_candidates: List[str]


_ASCII_RUN_RE = re.compile(rb"[ -~]{3,}")
_UTF16LE_RUN_RE = re.compile(rb"(?:[\x20-\x7e]\x00){3,}")
_SYMBOL_RE = re.compile(r"^[A-Z0-9][A-Z0-9._]{1,28}[A-Z0-9]$")


def _extract_string_pool(data: bytes) -> Set[str]:
    pool: Set[str] = set()
    for raw in _ASCII_RUN_RE.findall(data):
        try:
            s = raw.decode("ascii", "ignore").strip("\x00").strip()
        except Exception:
            continue
        if s:
            pool.add(s)

    for m in _UTF16LE_RUN_RE.finditer(data):
        try:
            s = m.group().decode("utf-16le", "ignore").strip("\x00").strip()
        except Exception:
            continue
        if s:
            pool.add(s)

    return pool


def _filter_symbol_candidates(pool: Iterable[str]) -> List[str]:
    out: Set[str] = set()
    for s in pool:
        if not s:
            continue
        if _SYMBOL_RE.match(s) and any("A" <= ch <= "Z" for ch in s):
            out.add(s)
    return sorted(out)


def extract_symbol_candidates(input_path: Path) -> List[str]:
    data = input_path.read_bytes()
    pool = _extract_string_pool(data)
    return _filter_symbol_candidates(pool)


def write_list(path: Path, lines: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _parse_kv_arg(text: str) -> Tuple[str, Path]:
    if "=" not in text:
        raise argparse.ArgumentTypeError("expect NAME=PATH")
    name, path = text.split("=", 1)
    name = name.strip()
    path = path.strip().strip('"')
    if not name:
        raise argparse.ArgumentTypeError("empty NAME")
    return name, Path(path)


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%dT%H%M%S")


def build_note(results: Sequence[ExtractionResult], out_dir: Path, stamp: str) -> str:
    lines: List[str] = []
    lines.append("# MT5 Broker Symbol Candidate Extraction Note")
    lines.append("")
    lines.append(f"- stamp: `{stamp}`")
    lines.append("- input_kind: `MetaQuotes Terminal bases/*/symbols/*.dat`")
    lines.append("- method: `ASCII + UTF-16LE string scan -> symbol-like regex filter`")
    lines.append("- caveat: 这些 `.dat` 不是公开文档格式，输出是“候选 symbol 字符串集合”，更接近 MarketWatch/selected 的近似，不等同于 broker 全量可交易品种清单。")
    lines.append("")
    lines.append("## Inputs / Outputs")
    for r in results:
        lines.append(f"- `{r.name}`")
        lines.append(f"  - input: `{r.input_path}`")
        lines.append(f"  - output: `{r.output_path}`")
        lines.append(f"  - candidate_count: `{len(r.symbol_candidates)}`")
    lines.append("")
    lines.append("## Suggested Next Step (if needs exact list)")
    lines.append("- 在 MT5 端通过脚本导出 `SymbolsTotal/SymbolName` 得到全量 MarketWatch 与全量 Symbols 列表（需要 MT5 端执行权限与脚本落盘）。")
    return "\n".join(lines) + "\n"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out-dir",
        required=True,
        help="Output directory for extracted lists",
    )
    parser.add_argument(
        "--input",
        action="append",
        required=True,
        type=_parse_kv_arg,
        help="NAME=PATH, can be repeated",
    )
    parser.add_argument(
        "--compare-selected",
        action="store_true",
        help="If provided and both *_selected inputs exist, write common/only lists",
    )
    args = parser.parse_args(argv)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = _now_stamp()

    results: List[ExtractionResult] = []
    for name, p in args.input:
        cands = extract_symbol_candidates(p)
        out_path = out_dir / f"broker_symbol_candidates_{name}_{stamp}.txt"
        write_list(out_path, cands)
        results.append(
            ExtractionResult(
                name=name,
                input_path=p,
                output_path=out_path,
                symbol_candidates=cands,
            )
        )
        print(f"{name}: {len(cands)} -> {out_path}")

    if args.compare_selected:
        sel_ic = None
        sel_tmgm = None
        for r in results:
            if r.name.endswith("_selected") and "ICMarkets" in r.name:
                sel_ic = set(r.symbol_candidates)
            if r.name.endswith("_selected") and ("TradeMaxGlobal" in r.name or "TMGM" in r.name):
                sel_tmgm = set(r.symbol_candidates)
        if sel_ic is not None and sel_tmgm is not None:
            common = sorted(sel_ic & sel_tmgm)
            only_ic = sorted(sel_ic - sel_tmgm)
            only_tmgm = sorted(sel_tmgm - sel_ic)
            write_list(out_dir / f"broker_symbol_candidates_common_selected_{stamp}.txt", common)
            write_list(out_dir / f"broker_symbol_candidates_only_icmarkets_selected_{stamp}.txt", only_ic)
            write_list(out_dir / f"broker_symbol_candidates_only_tmgm_selected_{stamp}.txt", only_tmgm)
            print(f"selected_common: {len(common)}")
            print(f"selected_only_icmarkets: {len(only_ic)}")
            print(f"selected_only_tmgm: {len(only_tmgm)}")

    note_path = out_dir / f"broker_symbol_candidates_NOTE_{stamp}.md"
    note_path.write_text(build_note(results, out_dir, stamp), encoding="utf-8")
    print(f"note: {note_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

