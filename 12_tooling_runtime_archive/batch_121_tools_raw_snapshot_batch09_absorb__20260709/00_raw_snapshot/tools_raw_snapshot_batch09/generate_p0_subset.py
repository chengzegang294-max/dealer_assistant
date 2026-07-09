from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Dict, Tuple


TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent
SRC_PATH = PROJECT_ROOT / "10_来源库_SOURCE_LIBRARY" / "02_原子化拆解文件" / "原子规则表.md"
OUT_PATH = PROJECT_ROOT / "docs" / "P0_规则子表_v0.1.md"

MAX_ROWS = 70

CATEGORIES_KEEP = {"趋势", "过滤", "入场", "出场", "风控", "仓位"}

SOURCE_QUOTAS = {
    "GAS核心母版": 28,
    "大隐": 28,
    "量化分析体系V1.1": 12,
    "其他": 12,
}

KW_EMA144 = re.compile(r"(EMA\s*$\s*(CLOSE|C)\s*,\s*144\s*$)|(EMA144)|(144EMA)|(界线)", re.IGNORECASE)
KW_EMA21 = re.compile(r"(EMA\s*$\s*(CLOSE|C)\s*,\s*21\s*$)|(EMA21)|(中线)", re.IGNORECASE)
KW_KD = re.compile(r"(KDJ)|(KD参数)|(KD\b)|(J值)", re.IGNORECASE)
KW_RISK = re.compile(r"(极限止损)|(止损)|(禁止开仓)|(一票否决)|(回撤)|(风控)", re.IGNORECASE)
KW_POSITION = re.compile(r"(满仓)|(试仓)|(加仓)|(减仓)|(仓位)|(清仓)|(总持仓)|(上限)|(30%)|(50%)|(70%)|(80%)|(100%)|(2N)", re.IGNORECASE)
KW_VOL = re.compile(r"(ATR)|(波动率)|(缩量)|(放量)|(成交量)|(量价)", re.IGNORECASE)


@dataclass(frozen=True)
class Rule:
    source: str
    asset: str
    tf: str
    category: str
    iff: str
    veto: str
    then: str
    params: str
    depends: str
    quote: str
    issue: str

    def to_text(self) -> str:
        return " | ".join(
            [
                self.source,
                self.asset,
                self.tf,
                self.category,
                self.iff,
                self.veto,
                self.then,
                self.params,
                self.depends,
                self.quote,
                self.issue,
            ]
        )


def parse_markdown_table(md: str) -> List[Rule]:
    lines = md.splitlines()
    header_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("| 来源文件 |"):
            header_idx = i
            break
    if header_idx is None:
        raise RuntimeError("未找到表头：| 来源文件 | ...")

    rows: List[Rule] = []
    for line in lines[header_idx + 2 :]:
        if not line.strip().startswith("|"):
            break
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) != 11:
            continue
        rows.append(
            Rule(
                source=cols[0],
                asset=cols[1],
                tf=cols[2],
                category=cols[3],
                iff=cols[4],
                veto=cols[5],
                then=cols[6],
                params=cols[7],
                depends=cols[8],
                quote=cols[9],
                issue=cols[10],
            )
        )
    return rows


def group_of(source: str) -> str:
    if source.strip() == "GAS核心母版":
        return "GAS核心母版"
    if "大隐" in source:
        return "大隐"
    if source.strip() == "量化分析体系V1.1":
        return "量化分析体系V1.1"
    return "其他"


def score_rule(r: Rule) -> int:
    text = f"{r.source}\n{r.asset}\n{r.tf}\n{r.category}\n{r.iff}\n{r.veto}\n{r.then}\n{r.params}\n{r.issue}"
    s = 0

    if r.category in {"过滤", "风控"}:
        s += 4
    elif r.category in {"仓位", "出场"}:
        s += 3
    elif r.category in {"趋势"}:
        s += 2
    else:
        s += 1

    if KW_EMA144.search(text):
        s += 8
    if KW_KD.search(text):
        s += 7
    if KW_RISK.search(text):
        s += 5
    if KW_POSITION.search(text):
        s += 4
    if KW_VOL.search(text):
        s += 3
    if KW_EMA21.search(text):
        s += 3

    if r.issue.strip() and r.issue.strip() != "无":
        s += 2

    if "重绘" in text or "repaint" in text.lower():
        s += 2

    return s


def normalize_cell(s: str) -> str:
    s = s.replace("\n", " ").strip()
    s = re.sub(r"\s+", " ", s)
    s = s.replace("|", "｜")
    return s


def unique_key(r: Rule) -> Tuple[str, str, str]:
    return (r.source.strip(), r.iff.strip(), r.then.strip())


def render_md(selected: List[Rule], src_path: Path) -> str:
    lines: List[str] = []
    lines.append("# P0规则子表（自动生成 v0.1）")
    lines.append("")
    lines.append(f"- 来源：{src_path}")
    lines.append("- 目标：用于豆包P0审计（冲突/边界/优先级裁决），不是最终策略全量")
    lines.append("- 主题：EMA144牛熊门控 + 多周期KD同向确认 + 极限止损/仓位硬约束 + 参数冲突样本")
    lines.append("")

    by_group: Dict[str, int] = {}
    by_cat: Dict[str, int] = {}
    for r in selected:
        by_group[group_of(r.source)] = by_group.get(group_of(r.source), 0) + 1
        by_cat[r.category] = by_cat.get(r.category, 0) + 1

    lines.append("## 统计")
    lines.append("")
    lines.append("| 维度 | 计数 |")
    lines.append("|---|---:|")
    for k in sorted(by_group.keys()):
        lines.append(f"| 来源组:{k} | {by_group[k]} |")
    for k in sorted(by_cat.keys()):
        lines.append(f"| 类别:{k} | {by_cat[k]} |")
    lines.append("")

    lines.append("## 规则表（带RuleID）")
    lines.append("")
    lines.append("| RuleID | 来源 | 资产 | 周期 | 类别 | 触发条件(if) | 否决条件(veto) | 动作/结论(then) | 参数 | 冲突/模糊点 |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")

    for idx, r in enumerate(selected, 1):
        rid = f"R{idx:03d}"
        lines.append(
            "| "
            + " | ".join(
                [
                    rid,
                    normalize_cell(r.source),
                    normalize_cell(r.asset),
                    normalize_cell(r.tf),
                    normalize_cell(r.category),
                    normalize_cell(r.iff),
                    normalize_cell(r.veto),
                    normalize_cell(r.then),
                    normalize_cell(r.params),
                    normalize_cell(r.issue),
                ]
            )
            + " |"
        )

    lines.append("")
    lines.append("## 豆包审计提示词（复制到豆包第一条）")
    lines.append("")
    lines.append(
        "\n".join(
            [
                "你是“交易量化规则审计官”，只做逻辑审计与裁决，不写长文教学。",
                "必须遵守口径：D1/4H定趋势；1H定买卖点；EMA=20/144；最大回撤红线25%；低频重仓。",
                "任务：对【P0规则子表(含RuleID) + 可执行草案v0.1】做审计：冲突/边界/优先级/缺失定义。",
                "输出：只允许输出《裁决清单》表格：",
                "IssueID｜严重性(P0/P1/P2)｜涉及RuleID/模块｜问题类型(冲突/边界/优先级/缺失定义)｜问题描述｜裁决(可执行)｜需要补充阈值/数据｜回填到配置的改动点(把X改为Y)",
            ]
        )
    )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    md = SRC_PATH.read_text(encoding="utf-8")
    rules = parse_markdown_table(md)

    candidates = [r for r in rules if r.category in CATEGORIES_KEEP]

    scored = sorted(((score_rule(r), r) for r in candidates), key=lambda x: x[0], reverse=True)

    quotas_left = dict(SOURCE_QUOTAS)
    selected: List[Rule] = []
    seen = set()

    for _, r in scored:
        if len(selected) >= MAX_ROWS:
            break

        g = group_of(r.source)
        if quotas_left.get(g, 0) <= 0:
            continue

        k = unique_key(r)
        if k in seen:
            continue

        selected.append(r)
        seen.add(k)
        quotas_left[g] = quotas_left.get(g, 0) - 1

    OUT_PATH.write_text(render_md(selected, SRC_PATH), encoding="utf-8")
    print(f"[OK] 已生成：{OUT_PATH}")
    print(f"[OK] 规则条数：{len(selected)}（上限 {MAX_ROWS}）")


if __name__ == "__main__":
    main()
