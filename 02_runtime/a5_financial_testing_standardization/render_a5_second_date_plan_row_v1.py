from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a second-date A5 input-pack TSV row without editing the sample plan.")
    parser.add_argument("--sample-date", required=True)
    parser.add_argument("--source-family", required=True)
    parser.add_argument("--source-root", required=True)
    args = parser.parse_args()

    sample_date = args.sample_date.strip()
    source_family = args.source_family.strip()
    source_root = str(Path(args.source_root).resolve())
    input_pack_id = f"A5_R2_EASTMONEY_SCREENSHOT_INPUT_PACK_{sample_date}_V1"
    required_files = "|".join(
        [
            f"00_raw_snapshot/user_screenshots/{sample_date}__市场情绪总览.png",
            f"00_raw_snapshot/user_screenshots/{sample_date}__市场宽度涨停跌停.png",
            f"00_raw_snapshot/user_screenshots/{sample_date}__龙虎榜异动资金.png",
        ]
    )
    acceptance_name = f"a5_input_pack_acceptance_{source_family}_{sample_date.replace('-', '')}.json"
    acceptance_output_json = (
        "02_runtime/a5_financial_testing_standardization/acceptance_outputs/" + acceptance_name
    )

    print(
        "\t".join(
            [
                input_pack_id,
                sample_date,
                source_family,
                source_root,
                required_files,
                "",
                acceptance_output_json,
            ]
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
