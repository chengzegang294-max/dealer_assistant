import csv
import hashlib
from pathlib import Path

ROOT = Path(r"D:\Stock\dealer_assistant")
SRC_TSV = ROOT / r"02_runtime\quicktiny_capture\batch_08_daily_close__20260811\derived\ladder_day_min__20260811.tsv"
OUT_TSV = ROOT / r"02_runtime\quicktiny_capture\batch_08_daily_close__20260811\derived\ladder_16col__20260811.tsv"

COLS16 = [
    "trade_date", "board_level", "code", "name", "level", "continue_num",
    "change_rate", "latest", "first_limit_up_time", "last_limit_up_time",
    "primary_theme", "limit_up_type", "open_num", "trading_amount",
    "order_amount", "turnover_rate",
]

rows_out = []
mismatch_board_level = 0
with SRC_TSV.open("r", encoding="utf-8", newline="") as f:
    r = csv.DictReader(f, delimiter="\t")
    for row in r:
        if str(row.get("board_level") or "") != str(row.get("level") or ""):
            mismatch_board_level += 1
        out = {}
        for c in COLS16:
            v = row.get(c)
            if v is None:
                v = ""
            if c == "primary_theme" and not v:
                v = "UNKNOWN"
            elif c == "limit_up_type" and not v:
                v = "OTHER"
            elif c in ("trading_amount", "order_amount"):
                if v is None or v == "":
                    v = "0"
            out[c] = v
        rows_out.append(out)


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


with OUT_TSV.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS16, delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(rows_out)

rows5 = []
with OUT_TSV.open("r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i >= 6:
            break
        rows5.append(line.rstrip("\n"))

tab_h = rows5[0].count("\t")
tab_r1 = rows5[1].count("\t") if len(rows5) > 1 else -1
print("ROWS_OUT=%d" % len(rows_out))
print("MISMATCH_BOARD_LEVEL=%d" % mismatch_board_level)
print("TAB15_HEADER=%d ROW1_TABS=%d" % (tab_h, tab_r1))
print("SHA256_16COL=%s" % sha(OUT_TSV))
print("COLS_ORDER=%s" % "|".join(COLS16))
