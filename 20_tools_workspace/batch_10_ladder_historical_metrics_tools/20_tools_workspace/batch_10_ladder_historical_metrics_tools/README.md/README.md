# batch_10 · 连板天梯 12 冻结指标全历史批量回写工具 v1

落地日期：2026-08-11
工作目录（当前，不写新仓）：`D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_10_ladder_historical_tools__20260811\`
验收后搬新仓：`20_tools_workspace\batch_10_ladder_historical_metrics_tools\`

---

## 为什么要做这个（不得不做的理由）

6 件冻结落地件里有 **3 件是跨日指标**，只靠单日 `calc_810_metrics.py` 根本无法验证命中率：

| 冻结规则 | 需要什么 | 没有这个脚本的后果 |
|---|---|---|
| 连续 3 天「天梯热 × sector 低分散 × 对齐度=0」→ 🔴 强制休息 | 至少 5+ 交易日连续指标序列 | 规则永远是拍脑袋，不知道历史上触发过几次、对不对 |
| Kimi T1 动态阈值（首板>80=20%、<60=30%、之间=25%） | 全历史首板数分布 + T1 命中率回测 | 阈值切换永远拍 25% 中间档，不知道 20/30 档触发过几天 |
| GLM Purity ≥2 板 3 天滚动平均 | 连续 N 天 Purity 序列 | 只看单日 Purity=61.5%，不知道是突然抱团还是连续 3 天小抱团 |

另外 P1 6 栏模板的「第 1 栏 矩阵结论」和「第 6 栏 操作约束」里的假强警示（sector 前 5 <100亿 且 最高板比昨日高）是**跨日比较**，必须有这个脚本每天 append 到 `metrics_history.tsv` 才能出。

---

## 依赖

```
Python 3.12+（用新仓 .venv 即可）
标准库：argparse / csv / json / collections / dataclasses / datetime / pathlib / typing
无第三方依赖（不装 pandas，保持最小依赖和快速启动）
```

---

## 输入

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--ladder-dir` | `d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\ladder_daily_snapshots` | 放 `ladder_day_min__YYYYMMDD.json` 的目录 |
| `--sector-dir` | `d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\sector_daily_snapshots` | 放 `sector_capital_flow_snapshot__YYYYMMDD.json` 的目录 |
| `--output-tsv` | `d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\metrics_history.tsv` | 输出 TSV（存在就 append，不存在写 header） |
| `--start-date` / `--end-date` | None | 可选 YYYYMMDD 过滤，一般不用 |
| `--dry-run` | off | 只跑 8/10 两个真实文件并做指标断言，不写 TSV |

---

## 输出 TSV 16 列（严格顺序，和最小字段合同 7.2 冻结公式一一对应）

| 列名 | 算法来源 | 8/10 实测值 |
|---|---|---|
| `date` | 文件名里的 YYYYMMDD | 20260810 |
| `max_level` | 板高最高值 | 5 |
| `total_stocks` | 全梯队总连板数（首板+中高位） | 99 |
| `ge2_stocks` | ≥2板数（Purity 分子分母口径） | 13 |
| `first_panel_count` | 首板数（T1 动态阈值判断依据） | 86 |
| `T1_dynamic_threshold` | 首板>80=20% / <60=30% / 中间=25% | 20.0 |
| `T1_pct` | 全口径 Top1 题材 / total_stocks × 100 | 12.1 |
| `T3_pct` | 全口径 Top3 题材合 / total_stocks × 100 | 23.2 |
| `Purity_ge2_pct` | ≥2板 Top1 题材 / ge2_stocks × 100（GLM ≥2板强制口径） | 61.5 |
| `sector_top5_sum_yi` | sector 前 5 主力净流入合计（亿） | 72.5 |
| `align_top3_top5_count` | 天梯 Top3 题材 ∩ sector 前 5（字面/语义重叠，0=严重背离） | 0 |
| `consecutive_divergence_days` | 连续「对齐度=0 且 sector<100亿」天数（≥3 触发休息） | 1 |
| `top4_di_list` | 高位按 DI 排序 Top4：`open_num × level`，用 `\|` 分隔 | `15\|0\|12\|0` |
| `top4_risk_list` | 高位 Top4 风险档 R/Y/G，用 `\|` 分隔 | `R\|G\|R\|Y` |
| `p1_position_advice` | 综合 4 条冻结规则给文字建议（机器草稿，人工再拍板） | 见下 |
| `fake_strength_warning` | YES/NO：sector 前 5 <100亿 且 最高板 > 昨日 | NO |

---

## 命令样例

### 1. Dry-run（**先跑这个验收，确认公式没错**）
```powershell
& d:\Stock\dealer_assistant\.venv\Scripts\python.exe `
  D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_10_ladder_historical_tools__20260811\calc_ladder_metrics_batch_v1.py `
  --dry-run
```

预期输出：
```
=== [DRY-RUN] 8/10 单日指标校验 ===
date=20260810 最高板=5 总数=99 首板=86
T1阈值=20% T1=12.1% T3=23.2% Purity≥2板=61.5%
sector前5合计=72.5亿 对齐度=0/3 连续背离=1天
top4 DI=[15, 0, 12, 0] top4 风险=['R', 'G', 'R', 'Y']
P1建议: T1分散→多看少动；中高位抱团→盯前排  假强警示=NO
[DRY-RUN OK] 8/10 核心指标匹配（容差±0.5 / 整数严格）
```

### 2. 全历史回写（第一次跑会写 header + 所有历史日期）
```powershell
& d:\Stock\dealer_assistant\.venv\Scripts\python.exe `
  calc_ladder_metrics_batch_v1.py `
  --output-tsv .\metrics_history.tsv
```
（注意上面这条是写旧仓当前目录的 TSV；验收通过后去掉 output-tsv 参数让它写新仓默认路径）

### 3. 每日收盘追加（日常跑，append 模式，默认不覆盖旧数据）
```powershell
& d:\Stock\dealer_assistant\.venv\Scripts\python.exe calc_ladder_metrics_batch_v1.py
```
扫 ladder/sector 两个 snapshot 目录，找到 metrics_history.tsv 里没有的日期就 append。

---

## 缺字段兜底 9 条（严格执行最小字段合同 7.3）

| 缺字段 | 处理 | 为什么这么做 |
|---|---|---|
| `primary_theme` 是 null/空串 | 记为 `"UNKNOWN"`，参与 T1/T3 但不参与 Purity 的 Top1 判定（实际 UNKNOWN 不会是第一，兜底而已） | 不崩溃，UNKNOWN 永远不会是主线题材 |
| `open_num` 缺失/null | 按 `0` 处理 → DI=0，不会触发 R/Y 档 | 分歧指数宁可少算不多算，避免假警示 |
| `trading_amount` 或 `order_amount` 为 0 | `seal_ratio=0` → 触发 R 档（<0.3） | 封单比 0 就是没封住，判 R 最保守 |
| `turnover_rate` 缺失 | 按 0，不触发 R/Y（换率档）；只要封单/DI 不 R/Y 就是 G | 换率缺失是偶发，不因为它独判 R/Y 太激进 |
| `first_limit_up_time` 不是整数时间戳 | ts_to_hhmm 返回 "?"，不影响公式（本脚本不直接用封板时间档算风险，只出个股列表） | 封板 4 档是 P1 高标 9 列的人工快筛，机器批量不做断言 |
| sector JSON 里 `rows` / `data.rows` / `records` 全为空 | sector_top5_sum_yi=0，对齐度=0，连续背离计数器加 1 | sector 没数据=最保守，当 0 处理 |
| ladder JSON 里某一天 `dates` 为空 | 当天 total_stocks=0，所有指标=0 或空串，跳过计数 | 允许某些天没抓到 ladder |
| ladder 文件名没 YYYYMMDD | 用 stem 前 8 位当日期，不是 8 位数字就 stem 原串 | 路径兼容 |
| `limit_up_type` 缺失 | 空串，不影响风险档计算（风险档只看 seal/DI/tr） | 板类型是快筛显示字段，不是决策字段 |

---

## 搬新仓前验收 CheckList（必须全过再搬）

- ✅ `--dry-run` 出 `[DRY-RUN OK]`，8/10 9 个核心指标全匹配（本 README 截图标注的实测值）
- ✅ 全历史回写至少跑通 ≥3 天（8/7, 8/8, 8/10），TSV 里 `consecutive_divergence_days` 的连续天数对得上（比如如果 8/7 也是对齐度=0 且 sector<100亿 → 8/8 该是 2 天）
- ✅ 随便改一个 EXPECTED_0810 值（比如 T1_pct=13）再跑 dry-run 必须 FAIL（断言逻辑工作正常，不会静默通过）
- ✅ `pyright calc_ladder_metrics_batch_v1.py` 零报错（Type Hint 全覆盖）

---

## 与 P1 6 栏冻结版的对接关系

| P1 6 栏 | 本脚本提供什么 | 人还需要做什么 |
|---|---|---|
| 1. 矩阵结论（2×2） | T1_pct vs T1_threshold（集中/分散）× sector_top5_sum vs 100亿（高/低分散）+ 对齐度 0/1/2/3 文字注解 | 最后拍仓位档 1/4→2/3→1/2 只用 1 秒 |
| 2. 断层梯队 | max_level + level_counter（本脚本没直接列，但 DayMetrics 里有 `level_counter` 预留可扩）+ 断层档位（本脚本输出 max_level 与 ge2_stocks 可人工算断层） | 填断层哪一板空着（1 秒） |
| 3. 高标 9 列监控 | top4_di_list + top4_risk_list（前 4 只够了，再多人工看 ladder 原始 JSON） | 人工补封板时间档（极早/强/午/晚 4 档，1 秒扫一眼） |
| 4. 题材集中度 4 指标 | T1_threshold + T1_pct + T3_pct + Purity_ge2_pct 4 个数字 1:1 直接抄 | 不用做，直接抄 |
| 5. 24 房预期差 | 本脚本不提供（rooms 家族产出，独立 T0-3） | 看 rooms/家族 SENTINEL + A 桶 9 房近 3 天提票统计（10 秒） |
| 6. 操作约束 4 行 | p1_position_advice 机器草稿 + fake_strength_warning + consecutive_divergence_days | 人工改两句措辞（10 秒，草稿已经把 4 行文字全给了） |

→ **P1 前 4 栏 100% 机器可算，人工只需复制粘贴；后 2 栏人工 20 秒。**
