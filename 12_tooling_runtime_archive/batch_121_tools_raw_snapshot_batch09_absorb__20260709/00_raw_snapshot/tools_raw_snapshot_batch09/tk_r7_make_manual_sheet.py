import argparse
from datetime import datetime
from pathlib import Path


HEADER = [
    "date_tag",
    "symbol",
    "timeframe",
    "direction",
    "ao_divergence_present",
    "ao_divergence_side",
    "ao_risk_adjust_note",
    "tp_context",
    "notes",
    "evidence_ref",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--name", default="tkr7_manual_audit_sheet_v1.tsv")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    path = out_dir / args.name
    if path.exists():
        return 0

    date_tag = datetime.now().strftime("%Y%m%d")
    header_line = "\t".join(HEADER)
    example_line = "\t".join(
        [
            date_tag,
            "EURUSD",
            "H1",
            "long",
            "0",
            "none",
            "no_divergence",
            "near_tp2",
            "",
            "",
        ]
    )
    path.write_text(header_line + "\n" + example_line + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
