import json
from pathlib import Path

p = Path(r"D:\Stock\dealer_assistant\02_runtime\info_live_room_sampling\batch_08_rooms_backfill__20260812\00_raw\info_live_incremental_export__20260811_180810.json")
with p.open("r", encoding="utf-8") as f:
    j = json.load(f)

def show_keys(node, prefix="top", depth=0, max_depth=3):
    if depth > max_depth:
        return
    if isinstance(node, dict):
        print(f"[{prefix}] dict keys({len(node)}): {' | '.join(node.keys())}")
        for k, v in node.items():
            t = type(v).__name__
            if isinstance(v, (dict, list)) and len(v) > 0:
                show_keys(v, f"{prefix}.{k}", depth + 1, max_depth)
            else:
                if isinstance(v, str) and len(v) < 120:
                    print(f"  {prefix}.{k} = {t}: {v}")
                else:
                    print(f"  {prefix}.{k} = {t} (len={len(v) if hasattr(v,'__len__') else '?'})")
    elif isinstance(node, list):
        print(f"[{prefix}] list len={len(node)}")
        if node:
            show_keys(node[0], f"{prefix}[0]", depth + 1, max_depth)
            if len(node) > 1:
                pass  # 不爆栈，只看首元素
    else:
        print(f"[{prefix}] scalar {type(node).__name__}: {str(node)[:80]}")


show_keys(j, "ROOT", max_depth=3)

# 额外：搜最常见的消息数组候选键 (top/data/*/ 长度 > 50)
print("\n=== 候选消息数组（len>=50 的 list）===")
def walk(node, path="ROOT", depth=0):
    if depth > 4:
        return
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, list) and len(v) >= 50:
                print(f"  LIST {path}.{k}  len={len(v)}  sample0_keys: {list(v[0].keys())[:12] if v and isinstance(v[0],dict) else 'NOT_DICT'}")
            walk(v, f"{path}.{k}", depth + 1)
    elif isinstance(node, list):
        for idx, item in enumerate(node[:3]):
            walk(item, f"{path}[{idx}]", depth + 1)

walk(j)
