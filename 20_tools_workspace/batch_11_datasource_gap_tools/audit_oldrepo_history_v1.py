import os
import re
import json
import csv
from datetime import datetime
from collections import Counter, defaultdict

OLD_REPO_ROOT = r"D:\Stock\trading_assistant"
OUTPUT_DIR = r"D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_datasource_gap__20260811"

date_pattern = re.compile(r'(20\d{6})')

def scan_dir_for_json_tsv(root_path):
    dir_stats = defaultdict(lambda: {"json": 0, "tsv": 0, "total": 0, "size_bytes": 0})
    for dirpath, dirnames, filenames in os.walk(root_path):
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            fp = os.path.join(dirpath, f)
            try:
                sz = os.path.getsize(fp)
            except:
                sz = 0
            if ext == '.json':
                dir_stats[dirpath]["json"] += 1
                dir_stats[dirpath]["total"] += 1
                dir_stats[dirpath]["size_bytes"] += sz
            elif ext == '.tsv':
                dir_stats[dirpath]["tsv"] += 1
                dir_stats[dirpath]["total"] += 1
                dir_stats[dirpath]["size_bytes"] += sz
    items = []
    for d, s in dir_stats.items():
        if s["total"] >= 3:
            items.append((d, s["total"], s["json"], s["tsv"], s["size_bytes"]))
    items.sort(key=lambda x: x[1], reverse=True)
    return items

def pick_history_dirs(all_dirs, root):
    keywords = ["history", "snapshot", "archive", "daily", "batch", "forex", "index", "longhubang", "ohlcv", "kline", "capture", "sampling"]
    scored = []
    for d, total, j, t, sz in all_dirs:
        rel = d.lower()
        score = 0
        for kw in keywords:
            if kw in rel:
                score += 10
        if score == 0:
            score = 1
        scored.append((score, total, d, j, t, sz))
    scored.sort(reverse=True)
    top3 = []
    seen = set()
    for s, tot, d, j, t, sz in scored:
        parent_ok = True
        for (existing_d, *_) in top3:
            if d.startswith(existing_d + os.sep) or existing_d.startswith(d + os.sep):
                parent_ok = False
                break
        if parent_ok and len(top3) < 3:
            top3.append((d, tot, j, t, sz))
        if len(top3) >= 3:
            break
    if len(top3) < 3:
        for s, tot, d, j, t, sz in scored:
            existing_dirs = [x[0] for x in top3]
            if d not in existing_dirs:
                top3.append((d, tot, j, t, sz))
            if len(top3) >= 3:
                break
    return top3[:3]

def audit_dir(dir_path):
    result = {
        "dir_path": dir_path,
        "total_files": 0,
        "json_files": 0,
        "tsv_files": 0,
        "total_size_mb": 0.0,
        "dates_set": set(),
        "date_file_counts": defaultdict(int),
        "json_field_sets": [],
        "empty_or_shell": 0,
        "sample_files": [],
    }
    total_size = 0
    file_count = 0
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext not in ('.json', '.tsv'):
                continue
            fp = os.path.join(dirpath, f)
            file_count += 1
            try:
                sz = os.path.getsize(fp)
            except:
                sz = 0
            total_size += sz
            if ext == '.json':
                result["json_files"] += 1
            else:
                result["tsv_files"] += 1
            m = date_pattern.search(f)
            if m:
                d = m.group(1)
                result["dates_set"].add(d)
                result["date_file_counts"][d] += 1
            if len(result["sample_files"]) < 20:
                result["sample_files"].append(fp)
            if ext == '.json':
                try:
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                        content = fh.read()
                    if len(content.strip()) < 50:
                        result["empty_or_shell"] += 1
                    else:
                        try:
                            data = json.loads(content)
                            if isinstance(data, dict):
                                fields = tuple(sorted(data.keys()))
                                result["json_field_sets"].append(fields)
                            elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                                fields = tuple(sorted(data[0].keys()))
                                result["json_field_sets"].append(fields)
                            else:
                                result["empty_or_shell"] += 0
                        except:
                            result["empty_or_shell"] += 1
                except:
                    result["empty_or_shell"] += 1
            else:
                try:
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                        lines = fh.readlines()
                    if len(lines) < 2 or (len(lines) == 2 and len(lines[1].strip()) < 10):
                        result["empty_or_shell"] += 1
                except:
                    result["empty_or_shell"] += 1
    result["total_files"] = file_count
    result["total_size_mb"] = round(total_size / (1024 * 1024), 2)
    return result

def compute_coverage(audit):
    dates = sorted(audit["dates_set"])
    if not dates:
        return {
            "earliest": "",
            "latest": "",
            "span_days": 0,
            "covered_days": 0,
            "coverage_pct": 0.0,
            "min_per_date": 0,
            "max_per_date": 0,
            "avg_per_date": 0.0,
            "dates_below_1": 0,
        }
    d1 = datetime.strptime(dates[0], '%Y%m%d')
    d2 = datetime.strptime(dates[-1], '%Y%m%d')
    span = (d2 - d1).days + 1
    covered = len(dates)
    below1 = sum(1 for d in dates if audit["date_file_counts"][d] < 1)
    vals = list(audit["date_file_counts"].values())
    return {
        "earliest": dates[0],
        "latest": dates[-1],
        "span_days": span,
        "covered_days": covered,
        "coverage_pct": round(covered / span * 100, 2) if span > 0 else 0.0,
        "min_per_date": min(vals) if vals else 0,
        "max_per_date": max(vals) if vals else 0,
        "avg_per_date": round(sum(vals) / len(vals), 2) if vals else 0.0,
        "dates_below_1": below1,
    }

def compute_schema_stability(audit):
    if not audit["json_field_sets"]:
        return {"unique_schemas": 0, "dominant_schema_pct": 0.0, "dominant_fields": "", "total_checked": 0}
    cnt = Counter(audit["json_field_sets"])
    total = sum(cnt.values())
    dom_fields, dom_count = cnt.most_common(1)[0]
    return {
        "unique_schemas": len(cnt),
        "dominant_schema_pct": round(dom_count / total * 100, 2),
        "dominant_fields": ",".join(list(dom_fields)[:15]),
        "total_checked": total,
    }

def main():
    print("=" * 80)
    print("阶段1: 扫描旧仓全部目录，统计 .json/.tsv 文件数...")
    all_dirs = scan_dir_for_json_tsv(OLD_REPO_ROOT)
    print(f"  找到含 ≥3 个 json/tsv 的目录共 {len(all_dirs)} 个")
    for i, (d, tot, j, t, sz) in enumerate(all_dirs[:15], 1):
        print(f"  TOP{i:2d}: {tot:4d}个 (json:{j:3d}, tsv:{t:3d}) {round(sz/1024/1024,2):>7.2f}MB  {d}")
    
    print("\n阶段2: 筛选 3 大历史类目录...")
    top3 = pick_history_dirs(all_dirs, OLD_REPO_ROOT)
    labels = ["longhubang_history", "forex_history", "index_history"]
    final_dirs = []
    for i, (d, tot, j, t, sz) in enumerate(top3):
        label = labels[i]
        print(f"  #{i+1} [{label}] -> {d}  ({tot}个文件, {round(sz/1024/1024,2)}MB)")
        final_dirs.append((label, d))
    
    print("\n阶段3: 对每个目录执行 4 项深度审计...")
    audits = []
    rows = []
    for label, d in final_dirs:
        print(f"\n  审计: {label} -> {d}")
        a = audit_dir(d)
        cov = compute_coverage(a)
        sch = compute_schema_stability(a)
        total_f = a["total_files"]
        shell_pct = round(a["empty_or_shell"] / total_f * 100, 2) if total_f > 0 else 0.0
        audits.append({
            "label": label, "path": d, "audit": a, "cov": cov, "sch": sch,
            "shell_pct": shell_pct, "total_files": total_f,
            "json_files": a["json_files"], "tsv_files": a["tsv_files"],
            "size_mb": a["total_size_mb"], "empty_or_shell": a["empty_or_shell"],
        })
        rows.append({
            "类别标签": label,
            "实际目录路径": d,
            "总文件数": total_f,
            "JSON文件数": a["json_files"],
            "TSV文件数": a["tsv_files"],
            "总大小MB": a["total_size_mb"],
            "最早日期": cov["earliest"],
            "最新日期": cov["latest"],
            "跨度天": cov["span_days"],
            "有数据天数": cov["covered_days"],
            "覆盖率%": cov["coverage_pct"],
            "每日期最小文件数": cov["min_per_date"],
            "每日期最大文件数": cov["max_per_date"],
            "每日期平均文件数": cov["avg_per_date"],
            "文件数<1的日期数": cov["dates_below_1"],
            "JSON结构唯一Schema数": sch["unique_schemas"],
            "Schema一致性%": sch["dominant_schema_pct"],
            "主Schema字段数": len(sch["dominant_fields"].split(",")) if sch["dominant_fields"] else 0,
            "主Schema字段(前15)": sch["dominant_fields"],
            "抽样JSON数": sch["total_checked"],
            "空壳/异常文件数": a["empty_or_shell"],
            "空壳率%": shell_pct,
        })
    
    tsv_path = os.path.join(OUTPUT_DIR, "oldrepo_13yr_history_reusability__20260811.tsv")
    fieldnames = list(rows[0].keys()) if rows else []
    with open(tsv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nTSV 已写入: {tsv_path}")
    
    print("\n" + "=" * 80)
    print("REUSABILITY TSV 全表:")
    print("=" * 80)
    with open(tsv_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    print(content)
    
    md_lines = []
    md_lines.append("# 旧仓13年历史数据搬运执行卡 __20260811")
    md_lines.append("")
    md_lines.append("> 生成时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    md_lines.append("> 范围: 仅旧仓 `D:\\Stock\\trading_assistant\\` 内 3 大历史类目录")
    md_lines.append("> 输出: `oldrepo_13yr_history_reusability__20260811.tsv` (明细表) + 本执行卡")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 0. 目录识别结果")
    md_lines.append("")
    md_lines.append("| 编号 | 逻辑标签 | 实际目录 | 总文件 | 大小MB |")
    md_lines.append("|------|----------|----------|--------|--------|")
    for i, x in enumerate(audits, 1):
        md_lines.append(f"| {i} | {x['label']} | `{x['path']}` | {x['total_files']} | {x['size_mb']} |")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 1. 分类搬运裁决（绿=直接搬 / 黄=先抽样质检 / 红=不建议搬）")
    md_lines.append("")
    
    NEW_RUNTIME = r"d:\Stock\dealer_assistant\02_runtime"
    decisions = []
    for x in audits:
        cov = x["cov"]
        sch = x["sch"]
        sp = x["shell_pct"]
        score = 0
        reasons = []
        if cov["coverage_pct"] >= 70:
            score += 2
            reasons.append(f"覆盖率{cov['coverage_pct']}%≥70%")
        elif cov["coverage_pct"] >= 30:
            score += 1
            reasons.append(f"覆盖率{cov['coverage_pct']}%偏低")
        else:
            reasons.append(f"覆盖率{cov['coverage_pct']}%过低")
        if sch["dominant_schema_pct"] >= 80 and x["json_files"] > 0:
            score += 2
            reasons.append(f"Schema一致性{sch['dominant_schema_pct']}%≥80%")
        elif sch["dominant_schema_pct"] >= 50 and x["json_files"] > 0:
            score += 1
            reasons.append(f"Schema一致性{sch['dominant_schema_pct']}%中等")
        elif x["json_files"] == 0:
            score += 1
            reasons.append("无JSON(TSV为主)")
        else:
            reasons.append(f"Schema一致性{sch['dominant_schema_pct']}%低")
        if sp <= 5:
            score += 2
            reasons.append(f"空壳率{sp}%≤5%")
        elif sp <= 20:
            score += 1
            reasons.append(f"空壳率{sp}%中等")
        else:
            reasons.append(f"空壳率{sp}%过高")
        if score >= 5:
            decision = "🟢 直接搬"
            target_suffix_map = {
                "longhubang_history": "quicktiny_capture\\longhubang_daily_snapshots",
                "forex_history": "quicktiny_capture\\forex_daily_snapshots",
                "index_history": "quicktiny_capture\\index_daily_snapshots",
            }
            ts = target_suffix_map.get(x["label"], "quicktiny_capture\\" + x["label"])
            target = os.path.join(NEW_RUNTIME, ts)
        elif score >= 3:
            decision = "🟡 先抽样质检"
            target = "先质检后定"
        else:
            decision = "🔴 不建议搬"
            target = "暂不搬"
        decisions.append({**x, "score": score, "decision": decision, "target": target, "reasons": reasons})
    
    md_lines.append("| 类别 | 裁决 | 评分/6 | 覆盖 | Schema一致 | 空壳率 | 新仓目标目录 | 判定理由 |")
    md_lines.append("|------|------|--------|------|------------|--------|--------------|----------|")
    for d in decisions:
        md_lines.append(f"| {d['label']} | {d['decision']} | {d['score']}/6 | {d['cov']['coverage_pct']}% | {d['sch']['dominant_schema_pct']}% | {d['shell_pct']}% | `{d['target']}` | {'；'.join(d['reasons'])} |")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 2. 抽样质检清单（仅🟡项需要）")
    md_lines.append("")
    md_lines.append("| 类别 | 质检动作 | 样本量 | 通过阈值 | 预计时间 |")
    md_lines.append("|------|----------|--------|----------|----------|")
    for d in decisions:
        if "🟡" in d["decision"]:
            md_lines.append(f"| {d['label']} | (1)随机抽30文件打开校验结构与非空；(2)首尾日期各抽5个验字段完整；(3)异常值扫描 | min(30, {max(d['total_files']//10, 5)}) | Schema一致≥90%且空壳率<10% | ~30min |")
        elif "🟢" in d["decision"]:
            md_lines.append(f"| {d['label']} | 免质检，直接进入搬运流程 | - | - | - |")
        else:
            md_lines.append(f"| {d['label']} | 🔴 暂不质检 | - | - | - |")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 3. 预估搬运时间 & 命令")
    md_lines.append("")
    md_lines.append("### 3.1 预估时间表")
    md_lines.append("")
    md_lines.append("| 类别 | 大小MB | 文件数 | 预计拷贝时间 | 校验时间 | 合计 |")
    md_lines.append("|------|--------|--------|--------------|----------|------|")
    total_mb = 0
    total_files = 0
    total_copy_sec = 0
    total_verify_sec = 0
    for d in decisions:
        mb = d["size_mb"]
        n = d["total_files"]
        if "🔴" in d["decision"]:
            copy_sec = 0
            verify_sec = 0
        else:
            copy_sec = max(5, int(mb * 0.5 + n * 0.05))
            verify_sec = max(10, int(n * 0.02)) if "🟢" in d["decision"] else max(30, int(n * 0.1))
        total_mb += mb
        total_files += n
        total_copy_sec += copy_sec
        total_verify_sec += verify_sec
        def fmt(sec):
            if sec >= 60:
                return f"{sec//60}min{sec%60}s"
            return f"{sec}s"
        md_lines.append(f"| {d['label']} | {mb} | {n} | {fmt(copy_sec)} | {fmt(verify_sec)} | {fmt(copy_sec+verify_sec)} |")
    def fmt2(sec):
        if sec >= 3600:
            return f"{sec//3600}h{(sec%3600)//60}min"
        if sec >= 60:
            return f"{sec//60}min{sec%60}s"
        return f"{sec}s"
    md_lines.append(f"| **合计(搬绿+黄)** | **{round(total_mb,2)}** | **{total_files}** | **{fmt2(total_copy_sec)}** | **{fmt2(total_verify_sec)}** | **{fmt2(total_copy_sec+total_verify_sec)}** |")
    md_lines.append("")
    md_lines.append("### 3.2 搬运命令（Windows PowerShell / Robocopy）")
    md_lines.append("")
    md_lines.append("```powershell")
    md_lines.append("# ============ 旧仓→新仓 历史数据搬运脚本 ============")
    md_lines.append("# 仅执行 🟢直接搬 项目；🟡需先执行 2. 质检通过后再解注释执行")
    md_lines.append("")
    md_lines.append("$ErrorActionPreference = 'Continue'")
    md_lines.append("")
    for i, d in enumerate(decisions, 1):
        src = d["path"]
        tgt = d["target"]
        if "🟢" in d["decision"]:
            md_lines.append(f"# #{i} {d['label']}  🟢直接搬")
            md_lines.append(f"robocopy '{src}' '{tgt}' *.json *.tsv /E /COPY:DAT /R:2 /W:1 /LOG+:'{OUTPUT_DIR}\\robocopy_{d['label']}.log' /NP /NFL")
            md_lines.append("")
        elif "🟡" in d["decision"]:
            md_lines.append(f"# #{i} {d['label']}  🟡待质检通过后执行（先解注释）")
            md_lines.append(f"# robocopy '{src}' '{tgt}' *.json *.tsv /E /COPY:DAT /R:2 /W:1 /LOG+:'{OUTPUT_DIR}\\robocopy_{d['label']}.log' /NP /NFL")
            md_lines.append("")
        else:
            md_lines.append(f"# #{i} {d['label']}  🔴 暂不搬")
            md_lines.append("")
    md_lines.append("# ============ 搬运后完整性校验 ============")
    md_lines.append("# 对每个目标目录数文件数 vs 源目录，差异>1%需重跑")
    md_lines.append("Write-Host '搬运完成，请人工对照 reusability TSV 校验文件数与大小'")
    md_lines.append("```")
    md_lines.append("")
    md_lines.append("### 3.3 命令说明")
    md_lines.append("")
    md_lines.append("- **Robocopy 参数**: `/E` 递归含空子目录；`/COPY:DAT` 保留数据+属性+时间戳；`/R:2 /W:1` 失败重试2次每次等1秒；`/LOG+` 追加日志；`/NP /NFL` 减少刷屏")
    md_lines.append("- **拷贝速度假设**: 本地SSD→SSD按 ~200MB/s 估算，小文件额外开销 50ms/文件")
    md_lines.append("- **校验规则**: 绿项随机抽 5% 验 md5；黄项100%验首字段存在性")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 4. 风险与回退")
    md_lines.append("")
    md_lines.append("1. **Schema漂移**: 若搬运后发现字段不一致，以 `主Schema字段(前15)` 为基准做 diff，生成 `schema_drift_report__YYYYMMDD.tsv`")
    md_lines.append("2. **空壳文件**: 空壳率>5% 的日期段，回退到旧仓重取或直接丢弃该段")
    md_lines.append("3. **大小不一致**: robocopy 后若目标总大小比源少 > 0.5%，用 `/PURGE` 重跑一次目标目录")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 5. 附录：各目录抽样文件清单")
    md_lines.append("")
    for d in audits:
        md_lines.append(f"### {d['label']} ({d['path']})")
        md_lines.append("")
        md_lines.append("```")
        for sf in d["audit"]["sample_files"][:10]:
            md_lines.append(f"  {sf}")
        md_lines.append("```")
        md_lines.append("")
    
    md_path = os.path.join(OUTPUT_DIR, "oldrepo_13yr_history_exec_card__20260811.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_lines))
    print(f"\nMD 执行卡已写入: {md_path}")
    
    print("\n" + "=" * 80)
    print("EXEC_CARD 前 30 行:")
    print("=" * 80)
    for i, line in enumerate(md_lines[:30], 1):
        print(f"{i:2d}| {line}")
    
    return tsv_path, md_path

if __name__ == "__main__":
    main()
