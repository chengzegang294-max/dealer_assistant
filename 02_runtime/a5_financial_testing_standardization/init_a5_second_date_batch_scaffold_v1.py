from __future__ import annotations

import argparse
from pathlib import Path


def readme_text(batch_name: str, sample_date: str, source_software: str) -> str:
    return f"""# {batch_name}

更新时间：{sample_date}

## 作用

- 本批次只收：
  - A5 第二日期样本最小补证截图
- 当前来源软件：
  - `{source_software}`

## 当前批次内容

- 已预留截图位：
  1. `00_raw_snapshot/user_screenshots/{sample_date}__市场情绪总览.png`
  2. `00_raw_snapshot/user_screenshots/{sample_date}__市场宽度涨停跌停.png`
  3. `00_raw_snapshot/user_screenshots/{sample_date}__龙虎榜异动资金.png`

## 入口文件

- `provenance.md`
- `manifest_v1.tsv`

## 一句话口径

- 本批次是第二日期样本接入现有验收链的最小来源批次。
"""


def provenance_text(temp_root: str, batch_name: str, sample_date: str) -> str:
    return f"""# provenance

更新时间：{sample_date}

## 临时材料处理记录

- 临时路径：`{temp_root}\\市场情绪总览.png`
  - 材料类型：`用户截图 / 页面总览`
  - 是否值得吸收：`yes`
  - 正式去向：`10_source_library_archive/{batch_name}/00_raw_snapshot/user_screenshots/{sample_date}__市场情绪总览.png`
  - 是否允许继续留在暂时存放：`yes`
  - 删除条件：`待本轮主线确认不再依赖临时副本后可删除`

- 临时路径：`{temp_root}\\市场宽度涨停跌停.png`
  - 材料类型：`用户截图 / 市场宽度`
  - 是否值得吸收：`yes`
  - 正式去向：`10_source_library_archive/{batch_name}/00_raw_snapshot/user_screenshots/{sample_date}__市场宽度涨停跌停.png`
  - 是否允许继续留在暂时存放：`yes`
  - 删除条件：`待本轮主线确认不再依赖临时副本后可删除`

- 临时路径：`{temp_root}\\龙虎榜异动资金.png`
  - 材料类型：`用户截图 / 龙虎榜异动资金`
  - 是否值得吸收：`yes`
  - 正式去向：`10_source_library_archive/{batch_name}/00_raw_snapshot/user_screenshots/{sample_date}__龙虎榜异动资金.png`
  - 是否允许继续留在暂时存放：`yes`
  - 删除条件：`待本轮主线确认不再依赖临时副本后可删除`

## 当前口径

- `暂时存放/` 只作临时中转，
  当前正式来源回链应优先指向本批次而不是临时路径。
"""


def manifest_text(sample_date: str) -> str:
    return "\n".join(
        [
            "relative_path\tmaterial_type\tsample_date\tstatus\tsource_note",
            f"00_raw_snapshot/user_screenshots/{sample_date}__市场情绪总览.png\tuser_screenshot_market_overview\t{sample_date}\tpending_absorb\tfrom 暂时存放 待吸收",
            f"00_raw_snapshot/user_screenshots/{sample_date}__市场宽度涨停跌停.png\tuser_screenshot_market_breadth\t{sample_date}\tpending_absorb\tfrom 暂时存放 待吸收",
            f"00_raw_snapshot/user_screenshots/{sample_date}__龙虎榜异动资金.png\tuser_screenshot_lhb_abnormal_funds\t{sample_date}\tpending_absorb\tfrom 暂时存放 待吸收",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize minimal second-date source batch scaffold for A5.")
    parser.add_argument("--batch-root", required=True)
    parser.add_argument("--sample-date", required=True)
    parser.add_argument("--source-software", default="东方财富 PC 客户端")
    parser.add_argument("--temp-root", default=r"d:\Stock\trading_assistant\暂时存放")
    args = parser.parse_args()

    batch_root = Path(args.batch_root).resolve()
    batch_name = batch_root.name
    sample_date = args.sample_date.strip()
    screenshots_dir = batch_root / "00_raw_snapshot" / "user_screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    (batch_root / "README.md").write_text(
        readme_text(batch_name, sample_date, args.source_software), encoding="utf-8"
    )
    (batch_root / "provenance.md").write_text(
        provenance_text(args.temp_root, batch_name, sample_date), encoding="utf-8"
    )
    (batch_root / "manifest_v1.tsv").write_text(manifest_text(sample_date), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
