import argparse
from datetime import datetime
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheet", required=True)
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--date-tag", default="")
    args = parser.parse_args()

    sheet = Path(args.sheet)
    if not sheet.exists():
        raise FileNotFoundError(str(sheet))

    header = sheet.read_text(encoding="utf-8").splitlines()[0]
    ncols = len(header.split("\t"))
    if ncols <= 1:
        raise ValueError("invalid header: expected TSV with >=2 columns")

    date_tag = (args.date_tag or "").strip() or datetime.now().strftime("%Y%m%d")
    line = date_tag + ("\t" * (ncols - 1))
    if not line.endswith("\t"):
        line = line + "\t"

    append_lines = (line + "\n") * max(0, int(args.n))
    if append_lines:
        with sheet.open("a", encoding="utf-8", newline="") as f:
            f.write(append_lines)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
