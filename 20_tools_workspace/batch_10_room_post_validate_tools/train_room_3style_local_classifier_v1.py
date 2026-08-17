"""
train_room_3style_local_classifier_v1.py
作用（Step 4 凑够≥50条真值验证过的经验判断之后直接跑）：
  完全本地化 sklearn 训练3个独立分类器（情绪=classifier_mood / 风格=classifier_style / 节奏=classifier_rhythm），不用任何外部 LLM API，不用key，纯本地跑，输出毫秒级。
特征（完全从 Prefill 四格 TOP5 + 统计字段抽，不用读 Raw）：
  1. 总消息条数（归一化到 0~1）
  2. 去重活跃作者数（归一化到 0~1）
  3. TOP5 每个关键词的命中次数（独热编码按词典：40+关键词列）
  4. TOP5 每个股票代码的命中次数（按训练时见过的代码词典，没见过的写 UNK 0次）
  5. TOP5 每个作者命中次数（同样按作者词典）
标签：
  classifier_mood → 情绪标签（强多/多/稍多/震荡中性/稍空/空/强空）= 来自 Step3 经验库里「真值验证过对」的情绪标签
  classifier_style → 风格标签（打板/低吸/埋伏/轮动）= 同上
  classifier_rhythm → 节奏标签（高位接力/中位/首板/观望）= 同上
输出：
  batch_10_room_post_validate_tools/models_3style_local/ 下 3 个 .pkl 分类器 + 1 个 feature_dictionary.json（特征词典以后新房间进来看见过没）
用法：
  python train_room_3style_local_classifier_v1.py \
    --rooms-root ../../02_runtime/info_live_room_sampling/rooms \
    --trade-date-list 20260811,20260812,20260813 \
    --manual-label-csv ./manual_100_rules_with_correct_labels.csv \
    --apply
注意：
  - 没凑够 50 条经验标签的话，训练效果差，建议≥50条再训
  - 训练完之后会自动跑 5-fold CV 打印每格准确率，CV准确率低就多喂更多标签，不要硬用
  - 训练/推理全本地化，永不调用外部 API
"""
from __future__ import annotations
import argparse
import csv
import json
import pickle
import re
from collections import Counter, defaultdict
from pathlib import Path


TOPIC_KW_ORDER = [
    "重要公告","题材","板块异动","涨停","连板","复盘","机会","风险","赛道","情绪",
    "接力","龙头","切换","分歧","一致","芯片","AI","算力","消费","医药","新能源",
    "军工","地产","金融","煤炭","钢铁","化工","半导体","储能","光伏","汽车","机器人",
    "数据要素","稀土","有色","华为","苹果","特斯拉","宁德时代","比亚迪","低吸","打板",
    "竞价","首板","二板","三板","中军","补涨","回流","T+0","超跌","高位","低位",
    "补跌","炸板","回封","缩量","放量","缺口","支撑位","压力位","止损","止盈",
    "仓位","加仓","减仓","满仓","空仓","半仓","轮动",
]
STOCK_6D = re.compile(r"\b(?:60[0-3]\d{3}|68[58]\d{3}|00[0-3]\d{3}|30[0-7]\d{3}|0[12][0-9]{4})\b")


def parse_prefill_features(prefill_md: Path) -> dict:
    txt = prefill_md.read_text(encoding="utf-8")
    d = {"total_msgs": 0, "total_authors": 0,
         "kw_top5": Counter(), "code_top5": Counter(), "author_top5": Counter()}
    m = re.search(r"\|\s*总消息条数\s*\|\s*(\d+)\s*\|", txt)
    if m:
        d["total_msgs"] = int(m.group(1))
    m = re.search(r"\|\s*去重活跃作者数\s*\|\s*(\d+)\s*\|", txt)
    if m:
        d["total_authors"] = int(m.group(1))
    m = re.search(r"\|\s*TOP5\s*关键词.*?\|\s*(.*?)\s*\|", txt, re.S)
    if m:
        line = m.group(1)
        for tok in re.split(r"\s+", line):
            if ":" in tok:
                k, n = tok.rsplit(":", 1)
                try:
                    d["kw_top5"][k] += int(n)
                except Exception:
                    pass
    m = re.search(r"\|\s*TOP5\s*股票代码.*?\|\s*(.*?)\s*\|", txt, re.S)
    if m:
        line = m.group(1)
        for tok in re.split(r"\s+", line):
            if ":" in tok:
                k, n = tok.rsplit(":", 1)
                if STOCK_6D.match(k):
                    try:
                        d["code_top5"][k] += int(n)
                    except Exception:
                        pass
    m = re.search(r"\|\s*TOP5\s*活跃作者.*?\|\s*(.*?)\s*\|", txt, re.S)
    if m:
        line = m.group(1)
        for tok in re.split(r"\s+", line):
            if ":" in tok:
                k, n = tok.rsplit(":", 1)
                try:
                    d["author_top5"][k] += int(n)
                except Exception:
                    pass
    return d


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rooms-root", required=True)
    ap.add_argument("--trade-date-list", required=True, help="逗号分隔 YYYYMMDD 列表，至少≥1天，标签越多越好")
    ap.add_argument("--manual-label-csv", required=True,
                    help="手动/Step3沉淀的100条经验标签：列=trade_date,room_name,label_mood,label_style,label_rhythm,correct_count,total_count,accuracy")
    ap.add_argument("--apply", action="store_true", help="写 .pkl 模型文件 + feature_dictionary.json")
    args = ap.parse_args()
    rooms_root = Path(args.rooms_root).resolve()
    dates = [x.strip() for x in args.trade_date_list.split(",") if x.strip()]
    label_csv = Path(args.manual_label_csv).resolve()
    print(f"=== Step4 本地化分类器训练（apply={args.apply}）===")
    print(f"训练日期：{dates}")
    print(f"经验标签CSV：{label_csv}")
    if not label_csv.exists():
        print(f"ERR：标签CSV还没填好，路径不存在：{label_csv} → 先凑够≥50条标签再来。")
        print(f"标签CSV列（表头要写）：trade_date,room_name,label_mood,label_style,label_rhythm,correct_count,total_count,accuracy")
        return 1
    with label_csv.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        labels_by_key: dict[tuple[str, str], dict] = {}
        for r in reader:
            td = (r.get("trade_date") or "").strip()
            rn = (r.get("room_name") or "").strip()
            if not td or not rn:
                continue
            lm = (r.get("label_mood") or "").strip()
            ls = (r.get("label_style") or "").strip()
            lr = (r.get("label_rhythm") or "").strip()
            if not (lm and ls and lr):
                continue
            labels_by_key[(td, rn)] = {"mood": lm, "style": ls, "rhythm": lr,
                                         "correct": int(r.get("correct_count") or 0),
                                         "total": int(r.get("total_count") or 0),
                                         "acc": float(r.get("accuracy") or 0.0)}
    if len(labels_by_key) < 50:
        print(f"WARN：标签数只有 {len(labels_by_key)} 条，建议≥50条再训，现在训出来效果差（可以继续训完参考，但别直接用）。")
    else:
        print(f"OK 标签数：{len(labels_by_key)} 条 ≥50 条，可以训。")
    # 扫描所有 Prefill 抽特征，同时建词典
    all_features: list[tuple[str, str, dict]] = []
    for (td, rn), lab in labels_by_key.items():
        pf = rooms_root / rn / "10_ingest" / f"{rn}_{td}_NOTES_partial_prefill.md"
        if not pf.exists():
            print(f"SKIP 标签({td},{rn})：Prefill 不存在 {pf}")
            continue
        fe = parse_prefill_features(pf)
        all_features.append((td, rn, fe))
    print(f"成功匹配 Prefill 特征：{len(all_features)} 条")
    if not all_features:
        print("ERR：没有一条能匹配到 Prefill → 退出")
        return 1
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import cross_val_score
        import numpy as np
    except Exception as e:
        print(f"ERR：没装 sklearn，跑不了训练：{e}")
        print("先 pip install scikit-learn numpy 再跑。")
        return 1
    # 建全局词典：关键词/代码/作者
    kw_vocab: dict[str, int] = {k: i for i, k in enumerate(TOPIC_KW_ORDER)}
    code_vocab: dict[str, int] = {"__UNK__": 0}
    author_vocab: dict[str, int] = {"__UNK__": 0}
    for _, _, fe in all_features:
        for c in fe["code_top5"]:
            if c not in code_vocab:
                code_vocab[c] = len(code_vocab)
        for a in fe["author_top5"]:
            if a not in author_vocab:
                author_vocab[a] = len(author_vocab)
    base_feats = 2
    KW_DIM = len(kw_vocab)
    CODE_DIM = len(code_vocab)
    AUTH_DIM = len(author_vocab)
    TOTAL_DIM = base_feats + KW_DIM + CODE_DIM + AUTH_DIM
    print(f"特征维度：基础{base_feats}(总消息/作者数) + 关键词{KW_DIM} + 代码{CODE_DIM} + 作者{AUTH_DIM} = 总{TOTAL_DIM} 维")
    # 归一化标尺（消息数最多按 10000 归一，作者最多按 1000 归一）
    NORM_MSG = 10000.0
    NORM_AUTH = 1000.0
    X = np.zeros((len(all_features), TOTAL_DIM), dtype=np.float32)
    y_mood: list[str] = []
    y_style: list[str] = []
    y_rhythm: list[str] = []
    for i, (td, rn, fe) in enumerate(all_features):
        X[i, 0] = min(max(fe["total_msgs"] / NORM_MSG, 0.0), 1.0)
        X[i, 1] = min(max(fe["total_authors"] / NORM_AUTH, 0.0), 1.0)
        for kw, n in fe["kw_top5"].items():
            idx = kw_vocab.get(kw, -1)
            if idx >= 0:
                X[i, base_feats + idx] += float(n)
        for code, n in fe["code_top5"].items():
            j = code_vocab.get(code, code_vocab["__UNK__"])
            X[i, base_feats + KW_DIM + j] += float(n)
        for a, n in fe["author_top5"].items():
            j = author_vocab.get(a, author_vocab["__UNK__"])
            X[i, base_feats + KW_DIM + CODE_DIM + j] += float(n)
        lab = labels_by_key[(td, rn)]
        y_mood.append(lab["mood"])
        y_style.append(lab["style"])
        y_rhythm.append(lab["rhythm"])
    y_mood_arr = np.array(y_mood)
    y_style_arr = np.array(y_style)
    y_rhythm_arr = np.array(y_rhythm)
    def _cv(name: str, y: np.ndarray) -> RandomForestClassifier | None:
        classes = sorted(set(y.tolist()))
        if len(classes) < 2:
            print(f"SKIP 分类器[{name}]：标签类别数 < 2 → 不能训练（多喂点标签再来）")
            return None
        clf = RandomForestClassifier(n_estimators=200, max_depth=12, class_weight="balanced", random_state=42, n_jobs=-1)
        k = min(5, len(y))
        scores = cross_val_score(clf, X, y, cv=k, scoring="accuracy")
        print(f"分类器[{name:<8}] 5折CV准确率：mean={round(float(scores.mean()),3):<5} std={round(float(scores.std()),3):<5} 类别数={len(classes)} 类别={classes}")
        clf.fit(X, y)
        return clf
    print("--- 训练 3 个分类器 ---")
    clf_mood = _cv("情绪", y_mood_arr)
    clf_style = _cv("风格", y_style_arr)
    clf_rhythm = _cv("节奏", y_rhythm_arr)
    if args.apply:
        out_dir = Path(__file__).parent / "models_3style_local"
        out_dir.mkdir(parents=True, exist_ok=True)
        dict_path = out_dir / "feature_dictionary.json"
        dict_path.write_text(json.dumps({
            "base_norm": {"total_msgs_cap": int(NORM_MSG), "total_authors_cap": int(NORM_AUTH)},
            "kw_vocab_order": TOPIC_KW_ORDER,
            "code_vocab": code_vocab,
            "author_vocab": author_vocab,
            "dimension_total": TOTAL_DIM,
            "kw_dim": KW_DIM,
            "code_dim": CODE_DIM,
            "auth_dim": AUTH_DIM,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        for clf, nm in ((clf_mood, "classifier_mood"), (clf_style, "classifier_style"), (clf_rhythm, "classifier_rhythm")):
            if clf is None:
                continue
            p = out_dir / f"{nm}.pkl"
            with p.open("wb") as f:
                pickle.dump(clf, f, protocol=pickle.HIGHEST_PROTOCOL)
            print(f"WROTE {p}")
        print(f"WROTE 特征词典：{dict_path}")
        print("")
        print("训练完成。之后房间自动填3格：")
        print("  python apply_room_3style_local_classifier_v1.py --trade-date YYYYMMDD --apply")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
