import os
import re
import csv
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup, Tag
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

OUTPUT_DIR = r"D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_workbench_design_map__20260811\injected_html_out"
TSV_PATH = r"D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_workbench_design_map__20260811\design_field_mapping_v2_upgrade_to_120rows__20260811.tsv"

HTML_FILES = [
    (
        "buy_ui",
        r"D:\Stock\trading_assistant\10_source_library_archive\batch_149_tdx_custom_terminal_external_folder_absorb__20260719\00_raw_snapshot\from_temp_staging__20260806\羽搧綸巾   经典酷黑   灵动版\HGPlugins\transaction\RES\Zyy\ajax\condition\html\buy_ui.html",
    ),
    (
        "condition",
        r"D:\Stock\trading_assistant\10_source_library_archive\batch_149_tdx_custom_terminal_external_folder_absorb__20260719\00_raw_snapshot\from_temp_staging__20260806\羽搧綸巾   经典酷黑   灵动版\HGPlugins\transaction\RES\Zyy\ajax\condition\html\condition.html",
    ),
    (
        "东财天梯",
        r"D:\Stock\trading_assistant\10_source_library_archive\batch_149_tdx_custom_terminal_external_folder_absorb__20260719\00_raw_snapshot\from_temp_staging__20260806\羽搧綸巾   经典酷黑   灵动版\company\东财天梯.html",
    ),
    (
        "涨停龙虎",
        r"D:\Stock\trading_assistant\10_source_library_archive\batch_149_tdx_custom_terminal_external_folder_absorb__20260719\00_raw_snapshot\pages\涨停龙虎.html",
    ),
    (
        "个股全情",
        r"D:\Stock\trading_assistant\10_source_library_archive\batch_149_tdx_custom_terminal_external_folder_absorb__20260719\00_raw_snapshot\from_temp_staging__20260806\羽搧綸巾   经典酷黑   灵动版\company\个股全情.html",
    ),
]

SLOT_VALUES = {
    "name / 股票名称": "贵州茅台",
    "totalStocks 总连板池": "86",
    "code / 代码": "600519",
    "封单率 limit_up_suc_rate": "61.5%",
    "NOTES.今日要点 人话摘要": "T1=12.1 情绪偏暖，梯队结构健康，关注5板以上高标分歧机会，板块轮动加快，主线题材持续性需观察。",
    "P1:盘中确认 10:00-13:30": "主力净流+38.2亿，黄白二线开口向上，连板家数稳定在42家，炸板率回落至18%，确认有效突破。",
    "first_limit_up_time 首封时间": "09:35:22",
    "P1:竞价段 9:15-9:30": "高开1.8%，竞价量比2.3，封单额12.5亿，抢筹迹象明显，高标一致预期强。",
    "level / continue_num 连板数": "5",
    "actual_turnover_rate 换手率": "7.25%",
    "auto_position/tags 定位标签": "总龙头|情绪标|赛道核心",
    "梯队分布 5B/3B/2B/1B": "5B×2 / 3B×3 / 2B×9 / 1B×86",
    "memberCount 成分股数": "128",
    "NOTES.值得沉淀长期库": "是 | 核心逻辑：白酒消费复苏+国企估值重塑，机构持仓集中度82%，Q3业绩预增+22%。",
    "pauseRatio 日级炸板率": "23.4%",
    "market_cap 流通市值": "72.5亿",
    "pe_ratio 市盈率(动)": "32.8",
    "hybk 东财行业板块字段": "白酒",
    "n 东财股票名字段": "五 粮 液",
    "c 东财股票代码字段": "000858",
    "leader_stock 板块领涨股": "山西汾酒",
    "rank 资金榜排名": "#3",
    "selected_sector 精选板块集合": "白酒|CRO|光伏储能|人工智能|中字头",
    "ths_hot 同花顺热榜板块": "白酒概念",
    "rank_top 人气榜Top10": "贵州茅台|五粮液|宁德时代|比亚迪|中芯国际|中国平安|山西汾酒|药明康德|隆基绿能|紫金矿业",
}

EXT_SELECTOR_OVERRIDES = {
    "pauseRatio 日级炸板率": ("id", "pauseratio"),
    "market_cap 流通市值": ("class", "marketcap"),
    "pe_ratio 市盈率(动)": ("id", "peratio"),
    "hybk 东财行业板块字段": ("id", "hybk"),
    "n 东财股票名字段": ("class", "n"),
    "c 东财股票代码字段": ("id", "c"),
    "leader_stock 板块领涨股": ("class", "leaderstock"),
    "rank 资金榜排名": ("id", "rank"),
    "selected_sector 精选板块集合": ("id", "selectedsector"),
    "ths_hot 同花顺热榜板块": ("class", "thshot"),
    "rank_top 人气榜Top10": ("class", "ranktop"),
}


def parse_anchor_to_selector(anchor_text, slot_name):
    if slot_name in EXT_SELECTOR_OVERRIDES:
        return EXT_SELECTOR_OVERRIDES[slot_name]

    if not anchor_text:
        return None

    patterns = [
        (r"_id_([a-zA-Z0-9_]+?)(?:[^\w]|$)", "id"),
        (r"_class_([a-zA-Z0-9_]+?)(?:[^\w]|$)", "class"),
        (r"(?<![a-zA-Z0-9])id_([a-zA-Z0-9_]+?)(?:[^\w]|$)", "id"),
        (r"(?<![a-zA-Z0-9])class_([a-zA-Z0-9_]+?)(?:[^\w]|$)", "class"),
    ]

    for pat, stype in patterns:
        match = re.search(pat, anchor_text)
        if match:
            return (stype, match.group(1))

    return None


def load_mapping_from_tsv(tsv_path):
    mapping = []
    with open(tsv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader, None)
        for row in reader:
            if len(row) < 8:
                continue
            match_type = row[7].strip()
            if match_type not in ("id命中", "class命中"):
                continue
            slot_name = row[1].strip()
            anchor = row[2].strip()
            sel = parse_anchor_to_selector(anchor, slot_name)
            if sel is None:
                print(f"  [SKIP] 无法解析选择器: slot={slot_name}, anchor={anchor}")
                continue
            sel_type, sel_val = sel
            mapping.append((slot_name, sel_type, sel_val))
    return mapping


def set_element_value(el, value):
    tag_name = (el.name or "").lower()
    if tag_name == "input":
        el["value"] = value
        return True
    elif tag_name in ("textarea", "select", "option"):
        el.string = value
        return True
    else:
        has_real_children = False
        if isinstance(el, Tag):
            for child in el.children:
                if isinstance(child, Tag):
                    has_real_children = True
                    break

        if has_real_children:
            replaced = False
            from bs4 import NavigableString
            for child in list(el.children):
                if isinstance(child, NavigableString) and str(child).strip():
                    child.replace_with(value)
                    replaced = True
                    break
            if not replaced:
                el.insert(0, value)
        else:
            el.clear()
            if isinstance(el, Tag):
                el.append(value)
            else:
                el.string = value
        return True


def inject_bs4(html_content, mapping, slot_values):
    soup = BeautifulSoup(html_content, "html.parser")
    hit_map = {}
    cache = []

    for slot_name, sel_type, sel_val in mapping:
        el = None
        if sel_type == "id":
            el = soup.find(id=sel_val)
        elif sel_type == "class":
            el = soup.find(class_=sel_val)
            if el is None:
                for candidate in soup.find_all(attrs={"class": True}):
                    classes = candidate.get("class", [])
                    if isinstance(classes, str):
                        classes = classes.split()
                    if sel_val in classes:
                        el = candidate
                        break
        cache.append((slot_name, sel_type, sel_val, el))

    def el_depth(e):
        d = 0
        p = e.parent if e is not None else None
        while p is not None:
            d += 1
            p = p.parent
        return d

    cache.sort(key=lambda t: -el_depth(t[3]))

    placeholders_to_add = []
    for slot_name, sel_type, sel_val, el in cache:
        value = slot_values.get(slot_name, f"MISSING_VALUE_{slot_name}")
        hit = False
        if el is not None:
            try:
                set_element_value(el, value)
                hit = True
            except Exception:
                hit = False
        hit_map[(slot_name, sel_type, sel_val)] = hit
        if not hit:
            placeholders_to_add.append(f"<!-- TODO:{slot_name} -->")

    if placeholders_to_add:
        try:
            target = soup.body or soup.find("body") or soup
            if hasattr(target, "append"):
                for ph in placeholders_to_add:
                    target.append(ph)
            elif hasattr(soup, "insert"):
                for ph in placeholders_to_add:
                    soup.insert(0, ph)
        except Exception:
            pass

    return str(soup), hit_map


def inject_regex(html_content, mapping, slot_values):
    result = html_content
    hit_map = {}

    for slot_name, sel_type, sel_val in mapping:
        value = slot_values.get(slot_name, f"MISSING_VALUE_{slot_name}")
        hit = False

        if sel_type == "id":
            id_pat = re.compile(
                r'<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?\sid\s*=\s*"' + re.escape(sel_val) + r'"[^>]*?(/?>)',
                re.DOTALL | re.IGNORECASE,
            )
            m = id_pat.search(result)
            if m:
                tag_name = m.group(1).lower()
                close_hint = m.group(2)
                is_self_close = "/" in close_hint

                if tag_name == "input" or is_self_close:
                    attr_pat = re.compile(
                        r'(<[a-zA-Z][a-zA-Z0-9]*\b[^>]*?\sid\s*=\s*"' + re.escape(sel_val) + r'"[^>]*?)(?:\svalue\s*=\s*"[^"]*")?([^>]*?/?>)',
                        re.DOTALL | re.IGNORECASE,
                    )
                    new_result, n = attr_pat.subn(
                        lambda mm: mm.group(1) + f' value="{value}"' + mm.group(2),
                        result,
                        count=1,
                    )
                    if n > 0:
                        result = new_result
                        hit = True
                else:
                    close_pat = re.compile(
                        r'<(' + re.escape(tag_name) + r')\b[^>]*?\sid\s*=\s*"' + re.escape(sel_val) + r'"[^>]*>((?:(?!</\1>).)*)</\1>',
                        re.DOTALL | re.IGNORECASE,
                    )
                    cm = close_pat.search(result)
                    if cm:
                        repl = cm.group(0)
                        inner_start = cm.start(2) - cm.start(0)
                        inner_end = cm.end(2) - cm.start(0)
                        new_repl = repl[:inner_start] + value + repl[inner_end:]
                        result = result[:cm.start()] + new_repl + result[cm.end():]
                        hit = True

        elif sel_type == "class":
            class_pat = re.compile(
                r'<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?\sclass\s*=\s*"[^"]*\b' + re.escape(sel_val) + r'\b[^"]*"[^>]*?(/?>)',
                re.DOTALL | re.IGNORECASE,
            )
            m = class_pat.search(result)
            if m:
                tag_name = m.group(1).lower()
                close_hint = m.group(2)
                is_self_close = "/" in close_hint

                if tag_name == "input" or is_self_close:
                    attr_pat = re.compile(
                        r'(<[a-zA-Z][a-zA-Z0-9]*\b[^>]*?\sclass\s*=\s*"[^"]*\b' + re.escape(sel_val) + r'\b[^"]*"[^>]*?)(?:\svalue\s*=\s*"[^"]*")?([^>]*?/?>)',
                        re.DOTALL | re.IGNORECASE,
                    )
                    new_result, n = attr_pat.subn(
                        lambda mm: mm.group(1) + f' value="{value}"' + mm.group(2),
                        result,
                        count=1,
                    )
                    if n > 0:
                        result = new_result
                        hit = True
                else:
                    close_pat = re.compile(
                        r'<(' + re.escape(tag_name) + r')\b[^>]*?\sclass\s*=\s*"[^"]*\b' + re.escape(sel_val) + r'\b[^"]*"[^>]*>((?:(?!</\1>).)*)</\1>',
                        re.DOTALL | re.IGNORECASE,
                    )
                    cm = close_pat.search(result)
                    if cm:
                        repl = cm.group(0)
                        inner_start = cm.start(2) - cm.start(0)
                        inner_end = cm.end(2) - cm.start(0)
                        new_repl = repl[:inner_start] + value + repl[inner_end:]
                        result = result[:cm.start()] + new_repl + result[cm.end():]
                        hit = True

        hit_map[(slot_name, sel_type, sel_val)] = hit

        if not hit:
            placeholder = f"<!-- TODO:{slot_name} -->"
            body_m = re.search(r"<body[^>]*>", result, re.IGNORECASE)
            if body_m:
                pos = body_m.end()
            else:
                pos = result.find(">")
                if pos != -1:
                    pos += 1
            if pos != -1 and pos < len(result):
                result = result[:pos] + placeholder + result[pos:]

    return result, hit_map


def inject_html(html_content, mapping, slot_values):
    if BS4_AVAILABLE:
        return inject_bs4(html_content, mapping, slot_values)
    else:
        return inject_regex(html_content, mapping, slot_values)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    mapping = load_mapping_from_tsv(TSV_PATH)
    print(f"[INFO] 加载 TSV 映射: {len(mapping)} 条 id/class 命中插槽")
    if len(mapping) != 25:
        print(f"[WARN] 期望 25 条，实际 {len(mapping)} 条")
    for i, (sn, st, sv) in enumerate(mapping, 1):
        sel = f"#{sv}" if st == "id" else f".{sv}"
        print(f"  [{i:2d}] {sn:40s} -> {sel}")

    print("\n" + "="*70)
    print("[INFO] 5 份典型 HTML 文件（路径 + 大小）:")
    print("="*70)
    for key, fpath in HTML_FILES:
        sz = os.path.getsize(fpath)
        print(f"  [{key:10s}] {fpath} | {sz:,} bytes")

    report_rows = []
    total_hit = 0
    total_checks = 0

    for html_key, html_path in HTML_FILES:
        with open(html_path, "r", encoding="utf-8", errors="replace") as f:
            html_content = f.read()

        new_html, hit_map = inject_html(html_content, mapping, SLOT_VALUES)

        row_hits = []
        for slot_name, sel_type, sel_val in mapping:
            is_hit = hit_map.get((slot_name, sel_type, sel_val), False)
            row_hits.append("HIT" if is_hit else "MISS")
            total_hit += (1 if is_hit else 0)
            total_checks += 1

        report_rows.append([html_key, html_path] + row_hits)

        out_name = f"{html_key}_prefilled_sample.html"
        out_path = os.path.join(OUTPUT_DIR, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"\n[WRITE] {out_path} ({len(new_html):,} bytes)")

    report_path = os.path.join(OUTPUT_DIR, "inject_report.tsv")
    with open(report_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        header = ["HTML键名", "HTML路径"] + [f"{sn}|{'#'+sv if st=='id' else '.'+sv}" for sn, st, sv in mapping]
        writer.writerow(header)
        for r in report_rows:
            writer.writerow(r)

    print("\n" + "="*70)
    print("[INFO] inject_report.tsv 前 15 行预览:")
    print("="*70)
    with open(report_path, "r", encoding="utf-8-sig") as f:
        for idx, line in enumerate(f, 1):
            if idx > 15:
                break
            trimmed = line.rstrip("\n")
            if len(trimmed) > 220:
                trimmed = trimmed[:220] + "..."
            print(f"  L{idx:02d}: {trimmed}")

    hit_rate_pct = (total_hit / total_checks * 100) if total_checks > 0 else 0.0
    print("\n" + "="*70)
    print(f"[SUMMARY] 25插槽 × 5HTML 总检查数: {total_checks}")
    print(f"[SUMMARY] 命中数: {total_hit} / 未命中数: {total_checks - total_hit}")
    print(f"[SUMMARY] 25插槽总命中率: {hit_rate_pct:.1f}%")
    print(f"[SUMMARY] BeautifulSoup4 可用: {'YES' if BS4_AVAILABLE else 'NO (使用正则降级)'}")
    print("="*70)


if __name__ == "__main__":
    main()
