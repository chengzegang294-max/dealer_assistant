# -*- coding: utf-8 -*-
import os
import re
import sys

TOOLS_WORKSPACE = r"D:\Stock\trading_assistant\20_tools_workspace"
OUT_DIR = r"D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_oldrepo_cleanup__20260811\tools_readme_out"
TPL_PATH = r"D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_oldrepo_cleanup__20260811\skeleton_template.md"

DIRS = [
    "batch_01_selected",
    "batch_02_group08_pipeline",
    "batch_03_general_ingest_tools",
    "batch_04_tk_r6_manual_sheet_tools",
    "batch_05_tk_r7_manual_sheet_tools",
    "batch_06_tk_r8_manual_sheet_tools",
    "batch_07_info_live_room_tools",
    "batch_08_quicktiny_capture_tools",
    "_raw_snapshot_batch09",
]

DEP_KWS = [
    "依赖", "requirements", "depend", "pip install",
    "Python 版本", "Python version", "python版本", "python version",
    "系统库", "环境要求",
]
IN_KWS = [
    "输入", "input", "数据来源",
    "TSV", "JSON", "CSV",
    "文件路径", "示例文件", "文件名",
]
OUT_KWS = [
    "输出", "output", "结果", "产物", "artifact",
    "列结构", "字段", "命名规范", "文件命名",
]
CMD_KWS = [
    "命令样例", "使用示例", "运行命令", "示例",
    "Example", "Usage", "python", ".\\", "--dry-run",
    "实跑", "命令行", "python3",
]


def read_text(path):
    if not os.path.exists(path):
        return ""
    for enc in ("utf-8-sig", "utf-8", "gbk", "gb18030"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def test_section(lines, keywords, min_len=25, look_ahead=12, extra_check=None):
    if not lines:
        return False
    kw_lower_patterns = []
    for kw in keywords:
        if re.search(r"[\u4e00-\u9fff]", kw):
            kw_lower_patterns.append(kw)
        else:
            kw_lower_patterns.append(kw.lower())
    for i, line in enumerate(lines):
        line_lower = line.lower()
        matched = False
        for pat, raw in zip(kw_lower_patterns, keywords):
            if pat in line_lower or raw in line:
                matched = True
                break
        if not matched:
            continue
        ctx_lines = lines[i:min(i + look_ahead, len(lines))]
        ctx_text = "\n".join(ctx_lines).strip()
        if len(ctx_text) >= min_len:
            if extra_check is None:
                return True
            if extra_check(ctx_text):
                return True
    return False


def cmd_extra_check(ctx):
    if len(ctx) < 20:
        return False
    pat = re.compile(r"(python|\.ps1|\.bat|--dry-run|\.py|Usage|Example)", re.IGNORECASE)
    return bool(pat.search(ctx))


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    tpl = read_text(TPL_PATH)

    audit_rows = []
    total_missing = 0

    for dir_name in DIRS:
        dir_path = os.path.join(TOOLS_WORKSPACE, dir_name)
        readme_path = os.path.join(dir_path, "README.md")
        has_readme = os.path.exists(readme_path)
        content = read_text(readme_path) if has_readme else ""
        lines = content.splitlines() if content else []

        has_dep = test_section(lines, DEP_KWS, min_len=20, look_ahead=10)
        has_inp = test_section(lines, IN_KWS, min_len=25, look_ahead=12)
        has_out = test_section(lines, OUT_KWS, min_len=25, look_ahead=12)
        has_cmd = test_section(lines, CMD_KWS, min_len=20, look_ahead=15, extra_check=cmd_extra_check)

        missing = 0
        if not has_dep:
            missing += 1
        if not has_inp:
            missing += 1
        if not has_out:
            missing += 1
        if not has_cmd:
            missing += 1
        total_missing += missing

        complete = has_dep and has_inp and has_out and has_cmd

        if complete:
            status_file = os.path.join(OUT_DIR, dir_name + "_README_status.md")
            write_text(status_file, "4要素齐全，无需补")
            result = "生成status"
        else:
            skel_file = os.path.join(OUT_DIR, dir_name + "_README_skeleton.md")
            filled = tpl.replace("__DIR_NAME__", dir_name)
            write_text(skel_file, filled)
            result = "生成skeleton"

        audit_rows.append({
            "dir": dir_name,
            "readme": "是" if has_readme else "否",
            "dep": has_dep,
            "inp": has_inp,
            "out": has_out,
            "cmd": has_cmd,
            "missing": missing,
            "result": result,
        })

    try:
        from colorama import init, Fore
        init()
        RED = Fore.RED
        GREEN = Fore.GREEN
        YELLOW = Fore.YELLOW
        CYAN = Fore.CYAN
        GRAY = Fore.LIGHTBLACK_EX
        RESET = Fore.RESET
    except Exception:
        RED = GREEN = YELLOW = CYAN = GRAY = RESET = ""

    sep = "=" * 110
    sep2 = "-" * 110
    header = f"{'目录名':<34} {'README':<7} {'依赖':<5} {'输入':<5} {'输出':<5} {'命令样例':<7} {'缺失数':<7} {'处理结果':<12}"

    print()
    print(CYAN + sep + RESET)
    print(CYAN + header + RESET)
    print(CYAN + sep2 + RESET)

    for r in audit_rows:
        def yn(v):
            return ("是" if v else "否")

        def cell(v):
            c = GREEN if v else RED
            return c + yn(v) + RESET

        line = f"{r['dir']:<34} {r['readme']:<7} "
        line += f"{cell(r['dep']):<{len(GREEN + '是' + RESET) + 3}} "
        line += f"{cell(r['inp']):<{len(GREEN + '是' + RESET) + 3}} "
        line += f"{cell(r['out']):<{len(GREEN + '是' + RESET) + 3}} "
        line += f"{cell(r['cmd']):<{len(GREEN + '是' + RESET) + 5}} "
        line += f"{r['missing']:<7} {r['result']:<12}"
        print(line)

    print(CYAN + sep2 + RESET)
    total_line = f"{'合计（9个目录）':<34} {'':<7} {'':<5} {'':<5} {'':<5} {'':<7} {total_missing:<7}"
    print(YELLOW + total_line + RESET)
    print(CYAN + sep + RESET)
    print()
    print(GRAY + "输出目录: " + OUT_DIR + RESET)
    return 0


if __name__ == "__main__":
    sys.exit(main())
