import argparse
import hashlib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Cluster:
    cluster_id: str
    cluster_name: str
    folder_name: str


CLUSTERS: list[Cluster] = [
    Cluster("TX-01", "择时/指标/大盘信号", "TX-01_择时_指标_大盘信号"),
    Cluster("TX-02", "因子/价值/财务/机器学习", "TX-02_因子_价值_财务_ML"),
    Cluster("TX-03", "行业/ETF/轮动/指数增强", "TX-03_行业_ETF_轮动_指数增强"),
    Cluster("TX-04", "期货/趋势/动量系统", "TX-04_期货_趋势_动量系统"),
    Cluster("TX-05", "配对/统计套利/相关性", "TX-05_配对_统计套利_相关性"),
    Cluster("TX-06", "资金流/事件驱动/公告类", "TX-06_资金流_事件驱动"),
    Cluster("TX-07", "杂项/练习/向导/待筛", "TX-07_杂项_练习_待筛"),
]

CLUSTER_BY_ID = {c.cluster_id: c for c in CLUSTERS}


def sha1_short(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()[:10]


def normalize_title(stem: str) -> str:
    return stem.strip().replace("\u3000", " ")


def classify_by_filename(name: str) -> str:
    n = name.lower()
    low_quality_markers = [
        "作业",
        "测试",
        "test",
        "向导",
        "再测",
        "新手",
        "小白",
        "说明",
        "自选",
        "收益策略",
    ]
    if any(m.lower() in n for m in low_quality_markers):
        return "TX-07"

    futures_markers = ["期货", "海龟", "合约", "移仓", "多品种", "商品", "动量效应", "动量模型"]
    if any(m.lower() in n for m in futures_markers):
        return "TX-04"

    pair_markers = ["配对", "价差", "协整", "pairs", "cointegration", "套利"]
    if any(m.lower() in n for m in pair_markers):
        return "TX-05"

    flow_event_markers = ["北向", "港资", "资金流", "聪明钱", "事件", "公告", "增持", "减持", "送转", "股东"]
    if any(m.lower() in n for m in flow_event_markers):
        return "TX-06"

    rotation_markers = ["轮动", "行业", "etf", "沪深300", "hs300", "中证500", "申万", "基金", "定投", "增强"]
    if any(m.lower() in n for m in rotation_markers):
        return "TX-03"

    factor_ml_markers = [
        "因子",
        "多因子",
        "pb",
        "pe",
        "roe",
        "capm",
        "价值",
        "成长",
        "随机森林",
        "svm",
        "lstm",
        "机器学习",
        "回归",
        "估值",
        "财务",
    ]
    if any(m.lower() in n for m in factor_ml_markers):
        return "TX-02"

    timing_markers = ["rsrs", "macd", "kdj", "kd", "均线", "ma", "dmi", "bias", "布林", "trix", "gftd", "择时", "止损"]
    if any(m.lower() in n for m in timing_markers):
        return "TX-01"

    return "TX-07"


def try_decode(data: bytes, encoding: str) -> tuple[str, int]:
    text = data.decode(encoding, errors="replace")
    replacement = text.count("\ufffd")
    return text, replacement


def guess_encoding(data: bytes) -> tuple[str, str]:
    if data.startswith(b"\xff\xfe") or data.startswith(b"\xfe\xff"):
        enc = "utf-16"
        text, _ = try_decode(data, enc)
        return enc, text
    if data.startswith(b"\xef\xbb\xbf"):
        enc = "utf-8-sig"
        text, _ = try_decode(data, enc)
        return enc, text

    candidates = ["utf-8", "gb18030", "cp936", "big5", "utf-16"]
    best_enc = "utf-8"
    best_text, best_bad = try_decode(data, "utf-8")
    for enc in candidates[1:]:
        text, bad = try_decode(data, enc)
        if bad < best_bad:
            best_enc, best_text, best_bad = enc, text, bad
        elif bad == best_bad and enc == "gb18030" and best_enc in {"utf-8", "cp936"}:
            best_enc, best_text = enc, text
    return best_enc, best_text


def iter_txt_files(src_dir: Path) -> Iterable[Path]:
    for p in sorted(src_dir.glob("*.txt")):
        if p.is_file():
            yield p


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", errors="strict")


def make_md(title: str, origin_path: str, encoding_guess: str, cluster_id: str, cluster_name: str, body: str) -> str:
    normalized = body.replace("\r\n", "\n").replace("\r", "\n")
    return (
        f"# {title}\n\n"
        f"- source_type: txt_strategy_sample_raw\n"
        f"- project_role: A股 future research/data capability\n"
        f"- origin_path: {origin_path}\n"
        f"- origin_encoding_guess: {encoding_guess}\n"
        f"- cluster_id: {cluster_id}\n"
        f"- cluster_name: {cluster_name}\n\n"
        f"```text\n{normalized}\n```\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--src-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    src_dir = Path(args.src_dir)
    out_dir = Path(args.out_dir)

    if not src_dir.exists():
        raise FileNotFoundError(str(src_dir))

    batch_id = datetime.now().strftime("%Y%m%d") + "_txt_to_md_" + sha1_short(str(src_dir))
    index_lines = ["batch_id\tsrc_path\tmd_path\tencoding\tcluster_id\tcluster_name"]

    counts: dict[str, int] = {c.cluster_id: 0 for c in CLUSTERS}
    total = 0

    for txt_path in iter_txt_files(src_dir):
        raw = txt_path.read_bytes()
        enc, text = guess_encoding(raw)
        title = normalize_title(txt_path.stem)
        cluster_id = classify_by_filename(title)
        cluster = CLUSTER_BY_ID[cluster_id]

        md_name = txt_path.with_suffix(".md").name
        md_path = out_dir / cluster.folder_name / md_name
        md_content = make_md(
            title=title,
            origin_path=str(txt_path),
            encoding_guess=enc,
            cluster_id=cluster.cluster_id,
            cluster_name=cluster.cluster_name,
            body=text,
        )
        write_text(md_path, md_content)

        index_lines.append(f"{batch_id}\t{txt_path}\t{md_path}\t{enc}\t{cluster.cluster_id}\t{cluster.cluster_name}")
        counts[cluster.cluster_id] += 1
        total += 1

    summary_lines = [
        "# txt 源码 -> md 归档（自动生成）",
        "",
        f"- batch_id: {batch_id}",
        f"- src_dir: {src_dir}",
        f"- out_dir: {out_dir}",
        f"- total_txt: {total}",
        "",
        "## 分桶计数",
        "",
    ]
    for c in CLUSTERS:
        summary_lines.append(f"- {c.cluster_id} {c.cluster_name}: {counts[c.cluster_id]}")

    summary_lines.extend(
        [
            "",
            "## 索引文件",
            "",
            "- `txt_md_index_v1.tsv`：每个文件的源路径、目标 md 路径、编码猜测、分桶信息",
            "",
        ]
    )

    write_text(out_dir / "README_放这里.md", "\n".join(summary_lines) + "\n")
    write_text(out_dir / "txt_md_index_v1.tsv", "\n".join(index_lines) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
