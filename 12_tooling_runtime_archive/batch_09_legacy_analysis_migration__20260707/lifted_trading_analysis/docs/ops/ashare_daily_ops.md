# A股日更操作说明

适用范围：A股（沪深主板 + 创业板），数据与选股链路独立于外汇冻结区，不影响周一出道。

---

## 0) 核心定位（先说清楚）

这套链路的定位不是“立刻交易”，而是把A股的“热点/情绪/题材”数据化成一条可复现流水线：

连板天梯（热点来源）→ 候选池（Candidate Pool）→ 指标摘要（Screen）→ 重点池（Focus Pool）→ 核心观察池（CORE）

你每天只需要复制粘贴一条命令，系统会产出当天的 focus 和 core 文件，方便复盘与持续迭代。

---

## 1) 术语与口径（对外统一）

### 1.1 名词

- Candidate Pool / Watchlist（候选池/自选池来源）：今天要看的股票列表
- Factors（因子）：附着在股票上的特征，用于评分与解释（如 theme_score）
- Theme / Sentiment（题材/情绪）：热点强度，本链路来自“连板天梯”
- Screen / Screening Table（筛选摘要表）：为候选池计算技术面/风险/流动性指标后的表
- Focus Pool（重点池）：按综合分排序取TopN（默认5）
- CORE（核心观察池）：在多个交易日里“稳定出现且质量达标”的更小集合

### 1.2 score 的口径（必须牢记）

- score 是“当天候选池内”的相对排序分，不具备跨天绝对可比性
- score 已拆分为：score = quant_score + theme_part + fund_part

其中：
- quant_score：量化主干（趋势/风险/流动性）
- theme_part：题材情绪贡献（w_theme * z(theme_score)）
- fund_part：基本面贡献（默认关闭 w_fundamental=0）

---

## 2) 输出文件（产物在哪里）

所有文件默认输出到：

`12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\ashare_watchlist\`

### 2.1 factors（候选池+题材因子）

- factors_ladder_YYYYMMDD.csv
  - 含：code,ticker,name,theme_score,ladder_height,open_num,tags,industry,reason_type,source,date,fundamental_score

### 2.2 screen（候选池指标摘要）

- watchlist_screen_YYYYMMDD.csv
  - 含：ret_5d, ret_20d, vol_20d_ann, max_dd_60d, avg_amount_20d, n_bars, last_close, last_date, clean_csv 等

### 2.3 focus（重点池TopN）

- focus_pool_YYYYMMDD.csv
- focus_pool_YYYYMMDD.txt（每行一个 code，便于复制）
  - 含：score, quant_score, theme_part, fund_part, score_pct 等

### 2.4 core（核心观察池）

- core_pool_YYYYMMDD.csv
- core_pool_YYYYMMDD.txt
  - 由最近N天的 focus_pool_*.csv 统计得到（历史不足时为空是正常的）

---

## 3) 一键日更（推荐：每天收盘后跑一次）

先进入目录：

cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis

### 3.1 标准模式（日常默认）

```powershell
.\.venv\Scripts\python.exe .\ashare_preprocess.py `
  --ladder-daily --ladder-min-height 2 --ladder-top-n 60 `
  --adjust qfq --start-date 2024-01-01 --end-date $(Get-Date -Format "yyyy-MM-dd") `
  --focus-n 5 --min-bars 60 `
  --w-ret20 0.30 --w-ret5 0.25 --w-vol20 -0.20 --w-dd60 -0.15 --w-liq 0.10 `
  --w-theme 0.2 --w-fundamental 0.0 `
  --core-window-days 5 --core-min-appear 3 --core-min-score-pct 0.80 `
  --core-min-bars 120 --core-max-abs-dd-60d 0.30 --core-max-n 10
```

### 3.2 宽松 CORE（第1周/CORE为空时）

```powershell
.\.venv\Scripts\python.exe .\ashare_preprocess.py `
  --ladder-daily --ladder-min-height 2 --ladder-top-n 60 `
  --adjust qfq --start-date 2024-01-01 --end-date $(Get-Date -Format "yyyy-MM-dd") `
  --focus-n 5 --min-bars 60 `
  --w-ret20 0.30 --w-ret5 0.25 --w-vol20 -0.20 --w-dd60 -0.15 --w-liq 0.10 `
  --w-theme 0.2 --w-fundamental 0.0 `
  --core-window-days 5 --core-min-appear 2 --core-min-score-pct 0.70 `
  --core-min-bars 120 --core-max-abs-dd-60d 0.40 --core-max-n 10
```

### 3.3 严格 CORE（主线清晰/想过滤杂毛）

```powershell
.\.venv\Scripts\python.exe .\ashare_preprocess.py `
  --ladder-daily --ladder-min-height 2 --ladder-top-n 60 `
  --adjust qfq --start-date 2024-01-01 --end-date $(Get-Date -Format "yyyy-MM-dd") `
  --focus-n 5 --min-bars 60 `
  --w-ret20 0.30 --w-ret5 0.25 --w-vol20 -0.20 --w-dd60 -0.15 --w-liq 0.10 `
  --w-theme 0.2 --w-fundamental 0.0 `
  --core-window-days 7 --core-min-appear 4 --core-min-score-pct 0.90 `
  --core-min-bars 120 --core-min-avg-amount-20d 500000000 --core-max-abs-dd-60d 0.25 --core-max-n 10
```

---

## 4) 评分细则（可解释、可复现）

### 4.1 Z-score 标准化

对每个指标在“当天候选池”内做标准化：

z(x) = (x - mean(x)) / std(x)

std 很小（几乎没差异）时，该项贡献视为0。

### 4.2 quant_score（量化主干）

默认权重：

- w_ret20 = 0.30
- w_ret5 = 0.25
- w_vol20 = -0.20
- w_dd60 = -0.15
- w_liq = 0.10

公式：

quant_score =
  w_ret20 * z(ret_20d)
  + w_ret5 * z(ret_5d)
  + w_vol20 * z(vol_20d_ann)
  + w_dd60 * z(abs(max_dd_60d))
  + w_liq * z(avg_amount_20d)

### 4.3 theme_score（题材/情绪来源：连板天梯）

theme_score = clip(base + bonus - penalty, 0, 1)

- base：ladder_height / 当天最大 ladder_height
- bonus：tags 含“龙头/总龙头” → +0.1
- penalty：open_num（开板次数）每+1 → -0.05，最多扣0.10

进入总分：

theme_part = w_theme * z(theme_score)

### 4.4 CORE 的定义（v1）

在最近 core_window_days 天里：

- appear ≥ core_min_appear
- 且 score_pct ≥ core_min_score_pct 的“好出现次数”也 ≥ core_min_appear
- 并满足质量门槛（bars/回撤/可选流动性）

---

## 5) 常见问题（排查）

### 5.1 CORE 为空

正常情况：刚开始历史不足。至少跑满 3~5 个交易日才可能出现 CORE。

如果跑满后仍为空：

- 用“宽松 CORE”模式先验证流程
- 或降低门槛：core_min_appear / core_min_score_pct

### 5.2 输出里出现你不能交易的板块

本链路已默认过滤，只保留：沪深主板 + 创业板。若仍出现异常，说明源站字段或代码解析变了，再回报我处理。

### 5.3 网络波动导致 ladder 拉取失败

稍后重试。站点可能临时波动或被网络/代理拦截。

---

## 6) 与外汇侧并行（互不影响）

- 外汇侧：严格按 mt5_daily_ops.md 的冻结流程执行
- A股侧：每天收盘后运行本文件的“一键日更”

两边输出文件完全独立，不会互相覆盖、不共享参数、不改外汇冻结区。

