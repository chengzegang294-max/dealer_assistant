from __future__ import annotations

import argparse
import json
from pathlib import Path


CARD_ORDER = [
    {
        "card_id": "A5_R2_CARD_001",
        "title": "HYDB行业对比 / 沪深涨跌停 -> 上榜资金",
        "status": "pending_formal_rebuild",
    },
    {
        "card_id": "A5_R2_CARD_002",
        "title": "ZSDB指数对比 / 沪深涨跌停 -> 打板资金",
        "status": "pending_formal_rebuild",
    },
    {
        "card_id": "A5_R2_CARD_003",
        "title": "HYDB行业对比 / ZSDB指数对比 -> 上榜资金",
        "status": "pending_formal_rebuild",
    },
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the three-card formal rebuild execution bundle for second-date pass.")
    parser.add_argument("--postpass-backfill-json", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    postpass_path = Path(args.postpass_backfill_json).resolve()
    payload = json.loads(postpass_path.read_text(encoding="utf-8-sig"))
    sample_date = str(payload.get("sample_date", "")).strip()
    ready = bool(payload.get("ready_for_formal_backfill"))

    output = {
        "bundle_id": "A5_SECOND_DATE_THREE_CARD_EXECUTION_BUNDLE_V1",
        "sample_date": sample_date,
        "postpass_backfill_json": str(postpass_path),
        "ready_for_three_card_formal_rebuild": ready,
        "cards": CARD_ORDER if ready else [],
        "still_need_evidence": [] if ready else ["second_date_postpass_backfill_not_ready"],
    }
    Path(args.output_json).write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
