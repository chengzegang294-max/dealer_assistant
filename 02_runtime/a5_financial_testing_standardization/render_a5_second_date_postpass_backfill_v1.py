from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Render second-date post-pass backfill package from workflow summary.")
    parser.add_argument("--workflow-summary", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    summary_path = Path(args.workflow_summary).resolve()
    summary = json.loads(summary_path.read_text(encoding="utf-8-sig"))
    sample_date = str(summary.get("sample_date", "")).strip()
    input_pack_passed = bool(summary.get("input_pack_passed"))
    multi_pack_gate_passed = bool(summary.get("multi_pack_gate_passed"))

    ready = input_pack_passed and multi_pack_gate_passed
    targets = [
        "00_entry/全库资料整理收口__20260713/A5_金融测试标准化验收清单页__20260730.md",
        "00_entry/全库资料整理收口__20260713/A5_工程测试过门槛与金融测试进入门槛重排页__20260730.md",
        "00_entry/全库资料整理收口__20260713/A5_真实案例采样第二轮案例扩展起手顺序页__20260727.md",
        "04_active_main_docs/batch_01_selected/00_主线检索索引.md",
        "04_active_main_docs/batch_01_selected/03_阶段二_当下计划_执行清单.md",
        "00_entry/全库资料整理收口__20260713/README.md",
    ]

    payload = {
        "backfill_id": "A5_SECOND_DATE_POSTPASS_BACKFILL_V1",
        "sample_date": sample_date,
        "workflow_summary": str(summary_path),
        "ready_for_formal_backfill": ready,
        "required_conditions": {
            "input_pack_passed": input_pack_passed,
            "multi_pack_gate_passed": multi_pack_gate_passed,
        },
        "targets": targets if ready else [],
        "still_need_evidence": [] if ready else ["second_date_workflow_not_fully_passed"],
    }
    Path(args.output_json).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
