import argparse
import csv
import os


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="outp", required=True)
    ap.add_argument("--only-reason", default="same_hash_as_keep")
    args = ap.parse_args()

    rows = []
    with open(args.inp, "r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            if row.get("action_suggestion") != "DROP":
                continue
            if args.only_reason and row.get("reason") != args.only_reason:
                continue
            rows.append(row)

    os.makedirs(os.path.dirname(os.path.abspath(args.outp)), exist_ok=True)
    with open(args.outp, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["path", "name", "dir_rel", "size_bytes", "sha256", "norm_key", "copies", "reason"])
        for row in rows:
            w.writerow(
                [
                    row.get("path", ""),
                    row.get("name", ""),
                    row.get("dir_rel", ""),
                    row.get("size_bytes", ""),
                    row.get("sha256", ""),
                    row.get("norm_key", ""),
                    row.get("copies", ""),
                    row.get("reason", ""),
                ]
            )

    print(f"delete_candidates={len(rows)}")
    print(f"out={os.path.abspath(args.outp)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

