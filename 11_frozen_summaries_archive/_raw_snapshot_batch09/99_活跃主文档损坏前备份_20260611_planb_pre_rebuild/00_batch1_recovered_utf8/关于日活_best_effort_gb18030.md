# 关于日活（每日该做什?/ 怎么留证据）

说明：当前阶段日活口?复现命令/证据留存”统丢?`01_阶段丢_项目记录_过去与落?md` 为主入口；本文件保留原始细节，后续可再收敛精箢?
目标：把“日常推进固定成可复现动作，避免口径漂移；同时把 MT5 执行链路?CSV 长窗研究解?
## 0) 证据口径（每天只要留三样?
- 日期 + 执行模式（MT5 观察 / MT5 执行 / CSV 研究 / A股日更）
- out_dir 路径（或 data 产物路径?- 丢条可复现命令（复制粘贴可重跑?
## 1) MT5 日活（模拟盘，推荐默认：只观察不下单?
### 1.1 观察模式（不下单?
```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\mt5_exit_assistant.py `
  --dry-run --watch --watch-on-new-h1 1 --interval-sec 30 `
  --pool core `
  --enable-entry 1 --entry-lookback-bars 1 --entry-show-all 0 --entry-status 1 --entry-gate-snapshot 1 `
  --e2-chase-max-atr 1.5 --e2-chase-action block `
  --enable-liquidity-gate 1 --liquidity-max-spread-rel 0.15 `
  --private-names 1 `
  --log-dir .\backtest_out\paper_watch_YYYYMMDD
```

### 1.2 执行模式（慎用，先把 EntryMaxOrders 设为 0/1 控制风险?
```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\mt5_daily_ops.ps1 -Mode plan
.\mt5_daily_ops.ps1 -Mode monitor_1h -IntervalSec 60

# 当前执行池（deploy_core.csv）：XAU + GBPJPY
# GBPJPY：E2 不执行（enable_e2_exec=0），只做 E1；E2 仅观?# 风控红线：最大回?25% 停机；仅允许减仓/出场，不允许新开仓?
# 真要执行：先跑一轮单次执行（max_loops=1）留证据，再决定是否长期?auto
.\.venv\Scripts\python.exe .\mt5_exit_assistant.py `
  --execute --max-loops 1 `
  --pool core `
  --enable-entry 1 --entry-universe pool --entry-scan-pools core,observe --entry-trade-pool core `
  --entry-execute 1 --entry-max-orders 1 --entry-lookback-bars 1 --entry-show-all 1 --entry-status 1 --entry-gate-snapshot 1 `
  --entry-lot 0.01 `
  --e2-chase-max-atr 1.5 --e2-chase-action block `
  --enable-liquidity-gate 1 --liquidity-max-spread-rel 0.15 `
  --vol-ratio-max 2.0 --vol-pct-max 90 --vol-risk-action block `
  --private-names 1 `
  --log-enabled 1 --log-dir .\backtest_out\mt5_live_exec_YYYYMMDD
```

### 1.3 今日留证据模板（执行丢次后要保存什么）

- 日期（本地）+ UTC 日期标签（out_dir 子目录名?- 执行口令（完整复制粘贴版?- 关键输出结论（DD / POS / ENTRY / SUMMARY?- 落盘证据（至?2 个文件）?  - `run_log.csv`
  - `mt5_deals.csv / mt5_orders.csv`（来?`-Mode summary`?
#### 2026-05-22（本地）｜单次执行留证据（UTC=2026-05-21?
- 预检（权限）：`.\mt5_daily_ops.ps1 -Mode status` ??True
- 预检（风?空仓）：`.\mt5_daily_ops.ps1 -Mode plan` ?`status=OK`、`[POS] count=0`、`pool_size=2`
- 单次执行（实盘，max_loops=1）：

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\mt5_exit_assistant.py `
  --execute --max-loops 1 `
  --pool core `
  --enable-entry 1 --entry-universe pool --entry-scan-pools core,observe --entry-trade-pool core `
  --entry-execute 1 --entry-max-orders 1 --entry-lookback-bars 1 --entry-show-all 1 --entry-status 1 --entry-gate-snapshot 1 `
  --entry-lot 0.01 `
  --e2-chase-max-atr 1.5 --e2-chase-action block `
  --enable-liquidity-gate 1 --liquidity-max-spread-rel 0.15 `
  --vol-ratio-max 2.0 --vol-pct-max 90 --vol-risk-action block `
  --private-names 1 `
  --log-enabled 1 --log-dir .\backtest_out\mt5_live_exec_20260522
```

- 执行结果（本次）：`[ENTRY] none`（无弢仓），`[POS] count=0`
- 对账（今日成交）：`.\mt5_daily_ops.ps1 -Mode summary` ?`deals=0 orders=0`
- 证据路径?  - `backtest_out\mt5_live_exec_20260522\2026-05-21\run_log.csv`
  - `backtest_out\mt5_live\2026-05-21\mt5_deals.csv`
  - `backtest_out\mt5_live\2026-05-21\mt5_orders.csv`

## 2) CSV 研究日活（淘宝CSV数据源，跑全指标链路”）

### 2.1 scan（输出全部指标字段：SR + jg_* + pat_* + 风控标签?
```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\mt5_exit_assistant.py `
  --paper-scan-csv --csv-dir .\data `
  --paper-from 2016-05-01 --paper-to 2026-03-01 `
  --paper-symbols XAUUSD,US500,NAS100,US30,GER30 `
  --paper-bobby-signals 1 --paper-bobby-sl-atr 1.5 `
  --log-dir .\backtest_out\paper_csv_all
```

### 2.2 replay（把 signals 回放成笔 outcome + 汇）

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\mt5_exit_assistant.py `
  --paper-replay-csv --paper-dir .\backtest_out\paper_csv_all\2026-03-01 --csv-dir .\data `
  --paper-lookahead-bars 48 --paper-tp1-r 1 --paper-tp2-r 2 --paper-bar-rule sl_first `
  --paper-e2-chase-max 1.5 --paper-e1-diagnose 1
```

### 2.3 commentary（只读叙事，给讨论用?
```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\mt5_exit_assistant.py `
  --paper-commentary --paper-dir .\backtest_out\paper_csv_all\2026-03-01 `
  --commentary-symbol XAUUSD --commentary-topk 8 --commentary-min-n 20
```

### 2.4 对照实验（可选：entry_score 门控；用文件夹前缢区分同名产物?
规则：只?`--log-dir`（out_dir）就能区分同名的 `paper_replay_summary.csv` 等文件；外发时可重命名为 `<out_dir>__paper_replay_summary.csv`?
```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis

# 长窗对照：vol_drop + score_gate(all)
.\.venv\Scripts\python.exe .\mt5_exit_assistant.py `
  --paper-scan-csv --csv-dir .\data `
  --paper-from 2016-05-01 --paper-to 2026-03-01 `
  --paper-symbols XAUUSD,US500,NAS100,US30,GER30 `
  --paper-bobby-signals 1 --paper-bobby-sl-atr 1.5 `
  --vol-ratio-max 2.0 --vol-pct-max 90 --vol-risk-action drop `
  --entry-score-max 4.5 --entry-score-action drop --entry-score-scope all `
  --log-dir .\backtest_out\paper_csv_vol_drop_score_all

.\.venv\Scripts\python.exe .\mt5_exit_assistant.py `
  --paper-replay-csv --paper-dir .\backtest_out\paper_csv_vol_drop_score_all\2026-03-01 --csv-dir .\data `
  --paper-lookahead-bars 48 --paper-tp1-r 1 --paper-tp2-r 2 --paper-bar-rule sl_first `
  --paper-e2-chase-max 1.5 --paper-e1-diagnose 1
```

### 2.5 黄金（XAUUSD）动态阈值（按波动阶段自动切换）

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis

# 推荐 v2：低/中波动更严格，高波动更宽松（atr_rel=ATR/price?# 注意：paper-to 建议填数据最后一天（当前 data\xauusd_1h.csv 朢新到 2026-05-20 04:00Z?.\.venv\Scripts\python.exe .\mt5_exit_assistant.py `
  --paper-scan-csv --csv-dir .\data `
  --paper-from 2016-05-01 --paper-to 2026-03-01 `
  --paper-symbols XAUUSD `
  --paper-bobby-signals 1 --paper-bobby-sl-atr 1.5 `
  --vol-ratio-max 2.0 --vol-pct-max 90 --vol-risk-action drop `
  --entry-score-action drop --entry-score-scope all `
  --entry-score-vol-mode atr_rel_bins --entry-score-vol-cuts 0.0019,0.0027 --entry-score-vol-maxes 4.6,4.6,5.0 `
  --log-dir .\backtest_out\xau_dyn_score_v2_full

.\.venv\Scripts\python.exe .\mt5_exit_assistant.py `
  --paper-replay-csv --paper-dir .\backtest_out\xau_dyn_score_v2_full\2026-03-01 --csv-dir .\data `
  --paper-lookahead-bars 48 --paper-tp1-r 1 --paper-tp2-r 2 --paper-bar-rule sl_first `
  --paper-e2-chase-max 1.5 --paper-e1-diagnose 1
```

### 2.6 外汇（FX）近两年窗（先补齐数据再跑）

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis

# FX 近两年窗（统丢到共同最?1H：当前为 2026-05-19 11:00Z?.\.venv\Scripts\python.exe .\mt5_exit_assistant.py `
  --paper-scan-csv --csv-dir .\data `
  --paper-from 2024-01-01 --paper-to 2026-05-19 `
  --paper-symbols EURUSD,GBPUSD,USDJPY,USDCAD,AUDUSD,NZDUSD,USDCHF,EURJPY,GBPJPY `
  --paper-bobby-signals 1 --paper-bobby-sl-atr 1.5 `
  --vol-ratio-max 2.0 --vol-pct-max 90 --vol-risk-action drop `
  --log-dir .\backtest_out\fx_24toLatest_vol_drop_mt5patch

.\.venv\Scripts\python.exe .\mt5_exit_assistant.py `
  --paper-replay-csv --paper-dir .\backtest_out\fx_24toLatest_vol_drop_mt5patch\2026-05-19 --csv-dir .\data `
  --paper-lookahead-bars 48 --paper-tp1-r 1 --paper-tp2-r 2 --paper-bar-rule sl_first `
  --paper-e2-chase-max 1.5 --paper-e1-diagnose 1
```

### 2.7 外汇（FX）近三年?+ CORE 候严格对?
```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis

# FX 19对（3年窗）：2023-01-01 ?共同朢新（当前?2026-05-19 00:00Z?.\.venv\Scripts\python.exe .\mt5_exit_assistant.py `
  --paper-scan-csv --csv-dir .\data `
  --paper-from 2023-01-01 --paper-to 2026-05-19 `
  --paper-symbols EURUSD,GBPUSD,USDJPY,USDCAD,AUDUSD,NZDUSD,USDCHF,EURJPY,GBPJPY,EURGBP,EURCHF,GBPCHF,EURAUD,EURNZD,AUDJPY,CADJPY,CHFJPY,NZDJPY,AUDNZD `
  --paper-bobby-signals 1 --paper-bobby-sl-atr 1.5 `
  --vol-ratio-max 2.0 --vol-pct-max 90 --vol-risk-action drop `
  --log-dir .\backtest_out\fx_19pairs_23toLatest_vol_drop

.\.venv\Scripts\python.exe .\mt5_exit_assistant.py `
  --paper-replay-csv --paper-dir .\backtest_out\fx_19pairs_23toLatest_vol_drop\2026-05-19 --csv-dir .\data `
  --paper-lookahead-bars 48 --paper-tp1-r 1 --paper-tp2-r 2 --paper-bar-rule sl_first `
  --paper-e2-chase-max 1.5 --paper-e1-diagnose 1

# CORE候（GBPJPY/GBPUSD/EURAUD/CADJPY）对照：E2c<1.5 vs E2c<1.0
.\.venv\Scripts\python.exe .\mt5_exit_assistant.py `
  --paper-scan-csv --csv-dir .\data `
  --paper-from 2023-01-01 --paper-to 2026-05-19 `
  --paper-symbols GBPJPY,GBPUSD,EURAUD,CADJPY `
  --paper-bobby-signals 1 --paper-bobby-sl-atr 1.5 `
  --vol-ratio-max 2.0 --vol-pct-max 90 --vol-risk-action drop `
  --log-dir .\backtest_out\fx_core4_3y_base_e2c1p5

.\.venv\Scripts\python.exe .\mt5_exit_assistant.py `
  --paper-replay-csv --paper-dir .\backtest_out\fx_core4_3y_base_e2c1p5\2026-05-19 --csv-dir .\data `
  --paper-lookahead-bars 48 --paper-tp1-r 1 --paper-tp2-r 2 --paper-bar-rule sl_first `
  --paper-e2-chase-max 1.5 --paper-e1-diagnose 1

.\.venv\Scripts\python.exe .\mt5_exit_assistant.py `
  --paper-replay-csv --paper-dir .\backtest_out\fx_core4_3y_base_e2c1p5\2026-05-19 --csv-dir .\data `
  --paper-lookahead-bars 48 --paper-tp1-r 1 --paper-tp2-r 2 --paper-bar-rule sl_first `
  --paper-e2-chase-max 1.0 --paper-e1-diagnose 1
```

## 3) A股日活（与外汇冻结区解）

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\.venv\Scripts\python.exe .\ashare_preprocess.py `
  --ladder-daily --ladder-min-height 2 --ladder-top-n 60 `
  --adjust qfq --start-date 2024-01-01 --end-date $(Get-Date -Format "yyyy-MM-dd") `
  --focus-n 5 --min-bars 60 `
  --w-ret20 0.30 --w-ret5 0.25 --w-vol20 -0.20 --w-dd60 -0.15 --w-liq 0.10 `
  --w-theme 0.2 --w-fundamental 0.0 `
  --core-window-days 5 --core-min-appear 3 --core-min-score-pct 0.80 `
  --core-min-bars 120 --core-max-abs-dd-60d 0.30 --core-max-n 10
```

## 4) 外部AI批注归档（从临时粘贴区迁移）

说明：此处用于存?PANEL_VOTE_TSV / DIFF_NOTES / BATCH_CLOSE，避免污?`临时粘贴区_外部AI与终端输?md`?
### 2026-06-04 迁移（批?8/27/26/25/24/23/22/21?
==============================
PANEL_VOTE_TSV（批?8；B99_OTHER?==============================
model	Q1_role	Q1_direction	Q2_role_map_summary	Q3_next_evidence_actions	contract_ok	notes
kimi	RISK_ONLY	（无效）?B40 ?bucket 形状误读?B99	stop_raw/ATR_ratio -> RISK_ONLY	补录 stop_distance + ?stop/ATR 分桶	partial	证据引用与本批次不一致（出现 bucket2=-62/bucket3=+146?deepseek	RISK_ONLY	甜点区；raw stop 不可比，建议 stop/ATR 归一?stop -> RISK_ONLY；先?stop_atr_ratio 再评估是否需要过??symbol×profile 分层；用 stop_atr_ratio 重跑分位桶；n>=100/20	ok	引用了摘录里?bin8/bin10 作为例子
glm	RISK_ONLY (+ENTRY_FILTER候?	中间朢优，两端差；霢 stop/ATR 归一?stop: RISK_ONLY +（若甜点区稳定可作为轻量过滤?生成 stop/ATR 桶；?dd_ok/stop_loss_rate；n>=100/20	ok	把甜点区”当成可选过滤，但仍以归丢化为前提
qwen	RISK_ONLY	甜点区；建议 stop/ATR ?stop/price	stop: RISK_ONLY	分层+合并桶；主看 avg_pnl/stop_loss_rate/dd_ok	ok	未给出明确阈值区?doubao	ENTRY_FILTER	甜点区（中间优，两端差）；建?stop/ATR	stop: ENTRY_FILTER（q30~q70?先做 stop/ATR 重跑 deciles；验证中间分位显著优于两?ok	角色偏进场过滤，但与“风险参数语义有冲突

==============================
DIFF_NOTES（批?8：只记录差异?+ 朢小证据动作）
==============================
- model: deepseek/qwen vs doubao
  divergence: stop 的语义角色（RISK_ONLY 的风险参?仓位参数?vs ENTRY_FILTER 的进场过滤）
  why_it_matters: 若把 stop 当作 ENTRY_FILTER，会把本来就该归丢?只影响仓位与单笔风险”的变量误用成决定做不做”的门槛，导致频?样本被硬砍且逻辑不稳
  repo_action: 固定 v0：stop 先归?RISK_ONLY；先落一个可比的派生?stop_dist_atr=abs(entry-stop)/atr；在 stop_dist_atr 上再讨论是否存在稳定甜点区（朢多做轻量过滤/风险加权?  reject_if: ?raw stop（绝对价）上直接给跨品种阈或直接建议“过?q10_bin1/2/10?- model: kimi
  divergence: 引用证据不一致（?B40 ?bucket 形状写成 B99 ?bucket?  why_it_matters: 会把不存在的证据当成结论，导致决策不可审?  repo_action: 其归丢?+ RISK_ONLY”方向可保留为观点，但不计入多数裁决
  reject_if: 继续使用与本批次证据表不丢致的 bucket/数?- model: 全体（共识）
  divergence: raw stop 跨品种不可比，必须归丢化（stop/ATR ?stop/price?  why_it_matters: 当前 b99_bucket_stats 的绝?stop 分位桶只能做单品种内部解读，不能做全池结?阈?  repo_action: 新增丢?b99_v2（或 followups）证据：stop_dist_atr 分位?+ symbol×profile 分层稳定性（n>=100/20；不足合并桶/标记 insufficient_data?  reject_if: 不做归一化就给结?阈?
==============================
BATCH_CLOSE（批?8收口：B99_OTHER v0?==============================
- 裁决：stop（初始止损）先定位为 RISK_ONLY（仓?单笔风险参数），不直接当 ENTRY_FILTER。当?raw stop（绝对价）跨品种不可比，必须先归丢化（建议：stop_dist_atr=abs(entry-stop)/atr）?- v0 ROLE MAP（研究侧标记，不做执行门控）?  - stop_dist_atr：RISK_ONLY
  - 甜点区（若在 stop_dist_atr 上稳定存在）：最多升级为“轻量过?风险加权”（而非硬门槛）；需证据表支?- 下一步最小证据动作（v0）：
  - 证据重跑：用 stop_dist_atr 替代 raw stop 重新做分位桶（建?deciles10）；输出?b99_bucket_stats/b99_feature_summary（v2?  - 分层稳定性：?symbol×profile 棢查中间分位优、两端差”是否同向（全局?n>=100；单 symbol n>=20，不足合并桶/标记 insufficient_data?  - 交互棢查：?stop_dist_atr ?B30 sv_regime_code（低?挤压）做交叉，验证窄止损更易扫损”的 regime 条件
- 已补证据（归丢化后，离散档位对照；20260603_v1）：
  - OUTPUT: d:\Stock\trading_analysis\backtest_out\stage2\indicator_audit\20260603_b99_followups_v3\b99_followups_bucket_stats_20260603_v1.csv
  - OUTPUT: d:\Stock\trading_analysis\backtest_out\stage2\indicator_audit\20260603_b99_followups_v3\b99_followups_feature_summary_20260603_v1.csv
  - OUTPUT: d:\Stock\trading_analysis\backtest_out\stage2\indicator_audit\20260603_b99_followups_v3\b99_followups_stop_atr_pairs_20260603_v1.csv
  - OUTPUT: d:\Stock\trading_analysis\backtest_out\stage2\indicator_audit\20260603_b99_followups_v3\b99_followups_stop_atr_summary_20260603_v1.csv
  - STOP_ATR_PAIR_SUMMARY（stop_atr=2.0 vs 1.5；按 symbol×profile；n>=20）：n_pairs=13; frac_pnl_better=0.538; frac_stop_loss_better=0.231; frac_both=0.231 ?不足以支持?.0 全局更优”的门控结论

通俗讲解（给用户看）?- 这轮我们在做仢么：?B99（stop）的外部AI回帖收口?v0 角色
- 这轮结论是什么：stop 先当 RISK_ONLY；raw stop 不能跨品种用，必须先?stop/ATR 归一化再谈甜点区
- 下一步要做什么：已补 stop_dist_atr 的离散档位对照；当前结果不支持?.0 全局更优”，因此暂不讨论改默认参数，仅保留为研究侧配置标?风险提示（需要时再做单独实验?
==============================
PANEL_VOTE_TSV（批?7；B40_E1_GEOMETRY?==============================
model	Q1_role	Q1_direction	Q2_role_map_summary	Q3_next_evidence_actions	contract_ok	notes
kimi	ENTRY_FILTER + RISK_ONLY	非单调（2朢差；3朢好）	retest=3 ?ENTRY_FILTER；retest=2 ?RISK_ONLY	分层+合并?看与B30/B20交互	ok	明确指出 bucket=2 朢?deepseek	REDUCE/RISK_ONLY + ENTRY_FILTER	越大越好（但强调 2 朢差? 朢好）	retest=2 预警/减仓；retest=3 优先入场	?>=4 ?分层稳定?ok	倾向?2 当减?收紧止损?glm	ENTRY_FILTER	越大越好?=3 更好?retest>=3 保留?-2 过滤	?>=4 ?与波动交?ok	?1 也当成过滤对?qwen	ENTRY_FILTER	越大越好	retest 越大越好	通用分层	partial	未处?bucket=2 朢差的非单调点
doubao	ENTRY_FILTER	越大越好	retest>=3 保留?=2 排除	分层+合并?看与B20组合	ok	提到?=4 单独分析”但当前证据?>=4

==============================
DIFF_NOTES（批?7：只记录差异?+ 朢小证据动作）
==============================
- model: kimi vs glm/qwen/doubao
  divergence: 是否承认“bucket=2 朢差bucket=1 中bucket=3 朢好的非单调形态（而非箢单越大越好）
  why_it_matters: 若用?=3 保留?=2 全过滤的线规则，会把 bucket=1（占比最大）全部砍掉，交易频率会大幅下降；且 bucket=2 的最差点”会被掩?  repo_action: 固定 v0：e1_retest_bars 先作为研究侧标签，不做硬门控；仅?bucket=2 标记?RISK/REDUCE 候，?bucket=3 标记?ENTRY_FILTER_PREFERRED；bucket=1 作为 baseline/neutral
  reject_if: 直接给一刢切过?=2”但不说明对交易频率的影?- model: 全体（共识）
  divergence: 要求?symbol/profile 分层，但当前桶分布在?symbol 维度样本不足
  why_it_matters: 过高的样本门槛会让稳定检验无法进行，从无法收?  repo_action: 先用更粗的合并桶做稳定：比较 bucket=1 vs bucket>=2（或 bucket<=2 vs bucket=3）；?symbol 门槛先用 n>=20（不足标?insufficient_data），全局桶仍要求 n>=100
  reject_if: 坚持?symbol n>=50/100 导致永远无结?- model: doubao/glm
  divergence: 讨论 >=4 ?  why_it_matters: ?>=4 极少或不存在，就不应该成为讨论中?  repo_action: 已核验：当前证据 unique buckets 只有 1/2/3?=4 作为 NEED_EVIDENCE，需在更大窗口（?pre2022）或不同参数下才可能出现
  reject_if: 把不存在的桶当成已存在证?
==============================
BATCH_CLOSE（批?7收口：B40_E1_GEOMETRY v0?==============================
- 裁决：e1_retest_bars 呈局部非单调”：bucket=2 朢差bucket=3 朢好bucket=1 中（?B40_BUCKET_AGG_TSV）由于单 symbol/profile ?bucket=2/3 样本不足，暂不将其做硬门控，仅做研究侧标签与组合分层?- v0 ROLE MAP（研究侧标记，不做执行门控）?  - e1_retest_bars=2：RISK/REDUCE_CANDIDATE（谨慎入场减?收紧止损提示候）
  - e1_retest_bars=3：ENTRY_FILTER_PREFERRED（入场质量加分标签）
  - e1_retest_bars=1：BASELINE（不加分不减分）
- 下一步最小证据动作（v0）：
  - 分层稳定性（先可跑得出来）：?retest 桶合并为 {1} vs {2,3} ?{<=2} vs {3}，在 symbol×profile 上用 n>=20 做方向同向占比统?  - 交互验证：对 retest=2 ?B20 ?e1_retest_depth_atr、以?B30 ?sv_regime_code 做分层，验证? 朢差是否来自某?regime
- 已完成证据动作（合并桶稳定?+ 与B20/B30交互分层?0260603_v1）：
  - OUTPUT: d:\Stock\trading_analysis\backtest_out\stage2\indicator_audit\20260603_b40_followups_v1\b40_stability_pairs_20260603_v1.csv
  - OUTPUT: d:\Stock\trading_analysis\backtest_out\stage2\indicator_audit\20260603_b40_followups_v1\b40_stability_summary_20260603_v1.csv
  - OUTPUT: d:\Stock\trading_analysis\backtest_out\stage2\indicator_audit\20260603_b40_followups_v1\b40_interaction_sv_regime_20260603_v1.csv
  - OUTPUT: d:\Stock\trading_analysis\backtest_out\stage2\indicator_audit\20260603_b40_followups_v1\b40_interaction_depth_atr_20260603_v1.csv
  - STABILITY_SUMMARY（按 symbol×profile；n>=20；方向同向占比）?    - scheme=1_vs_ge2: n_pairs=31; frac_pnl_better=0.742; frac_stop_loss_better=0.710; frac_both=0.645
    - scheme=le2_vs_3: n_pairs=5; frac_pnl_better=0.600; frac_stop_loss_better=0.200; frac_both=0.200

通俗讲解（给用户看）?- 这轮我们在做仢么：?B40（e1_retest_bars）外部AI回帖收口?v0 角色，并标出必须补的朢小证据动?- 这轮新增/变化：多数模型向?=3 更好”，?kimi 指出 bucket=2 才是朢差点；我们按证据采用“非单调+先标签后门控?- 你需要做仢么：不用再发外部AI；我下一步直接跑“合并桶稳定?+ 与B20/B30交互分层”的证据表，然后进入下一?B99_OTHER（stop?
==============================
PANEL_VOTE_TSV（批?6；B50_SCORE_SIZING?==============================
model	Q1_entry_score_role	Q1_entry_score_direction	Q1_size_mult_need_evidence	Q2_role_map_summary	Q3_next_evidence_actions	contract_ok	notes
kimi	RISK_ONLY	非单调（两端差，中间甜点?NEED_EVIDENCE（先查列/再分桶）	entry_score=RISK_ONLY（排除bin1-2?分层+每桶n>=100	ok	强调“甜点非“越高越好?deepseek	ENTRY_FILTER	非单调（甜点区q30~q50?NEED_EVIDENCE（需补分桶统计）	entry_score=ENTRY_FILTER（甜点区?分层+每桶n>=100	ok	给出“过高降级observe”的想法
glm	ENTRY_FILTER	非单调（两端差，中间好）	NEED_EVIDENCE（需分桶统计?entry_score=ENTRY_FILTER（保留bin3-8?分层+每桶n>=100	ok	建议与B30交叉验证
qwen	ENTRY_FILTER	值越大越好（与证据表冲突?NEED_EVIDENCE	entry_score=ENTRY_FILTER	通用分层/合并?partial	方向性判断未对齐已给的deciles?doubao	RISK_ONLY	值越小越危险（偏线）	NEED_EVIDENCE（但提了不存在的参数?entry_score=RISK_ONLY（q25以下风险?分层+每桶n>=100	ok	提议 --include-size-mult（需核实?
==============================
DIFF_NOTES（批?6：只记录差异?+ 朢小证据动作）
==============================
- model: deepseek/glm/qwen vs kimi/doubao
  divergence: entry_score 的角色（ENTRY_FILTER 甜点?vs RISK_ONLY 排除低分位）
  why_it_matters: 这决定我们是“只过滤朢差段”还是保留甜点段并压缩两端，对触发频率与样本稳定性影响很?  repo_action: 固定 v0：把 entry_score 视为“甜点型过滤（ENTRY_FILTER_SWEETSPOT），但只先做研究侧标签；门槛：按 symbol×profile 方向同向占比>=70%；全屢?n>=100，单 symbol 若不足可降到 n>=50 并合并桶
  reject_if: ?entry_score 当作单调线门控（越高越好/越低越好）但不解释为?bin10 并不更好?- model: qwen
  divergence: 方向性写“越大越好，?ENTRY_SCORE_DECILES_AGG_TSV 不一致（bin10 avg_pnl? ?win_rate更低?  why_it_matters: 若照此设置阈值会把甜点型”误做成“追高型?  repo_action: 仅保留其“分?每桶n>=100”的流程建议；不计入方向性多数裁?  reject_if: 不引用证据表字段/数?- model: doubao
  divergence: 提议参数 `--include-size-mult`（当前仓库不存在?  why_it_matters: 这会让执行动作不可复?  repo_action: 标注?NEED_EVIDENCE（需先给出该参数在哪个脚?函数实现”）；本轮我们已?v3 证据补齐 size_mult ?value_code 分桶，无霢该参?  reject_if: 继续引用不存在参?文件
- model: 全体（共识）
  divergence: size_mult 必须先有可用分桶证据才能讨论角色
  why_it_matters: size_mult 在不少文件里可能是低熵常数（如只?1.0/1.15），若不先证明有区分度就不能当指?  repo_action: ?b50_evidence_v3 直接给出 size_mult=value_code ?bucket stats；若仍只?-2个取值，则将 size_mult 降级为配置档位对照，不是交易信号
  reject_if: 没有说明取分?样本?
==============================
BATCH_CLOSE（批?6收口：B50_SCORE_SIZING v0?==============================
- 裁决：entry_score 属于“甜点型”信号质量指标（非单调），合作为 ENTRY_FILTER_SWEETSPOT（研究侧标签先行），不合作为“越高越好的线门控size_mult 不是典型指标，更像仓位率档位”；霢要先?value_code 分桶看不同档位的风险/收益差异，再决定是否用于 ADD/RISK?- v0 ROLE MAP（研究侧标记，不做执行门控）?  - entry_score：ENTRY_FILTER_SWEETSPOT（先排除朢差段：bin1-2；高分段 bin9-10 先降级为 observe，不作为优先入场理由?  - size_mult：CONFIG_BUCKET（先做档位对照，不直接映射到交易信号?- 下一步最小证据动作（v0；不复问外部AI也能跑）?  - ?`b50_evidence_v3` ?size_mult=value_code 结果做档位对照表”（?symbol/profile 加权汇）：size_mult=1 vs 1.15 ?stop_loss_rate/avg_pnl/tp2_rate
  - ?entry_score 做甜点区稳定性：?symbol×profile 统计 bin1-2 vs bin3-8 ?stop_loss_rate ?avg_pnl，同向占?=70% 才允许写阈；全局?n>=100，单 symbol 若不足可降到 n>=50 并合并桶；否则只保留为观察标?  - 已新?followups 产物（用于直接验收）：`backtest_out\stage2\indicator_audit\20260603_b50_followups_v1\b50_size_mult_agg_20260603_v1.csv` ?`...b50_entry_score_stability_20260603_v1.csv`（注意：当前 size_mult=1 样本?7，无法做稳定对照?
通俗讲解（给用户看）?- 这轮我们在做仢么：收口 B50（entry_score/size_mult）外部AI回帖，把它们定成“进场过?风险提示/仓位档位”的 v0 角色
- 这轮新增/变化：新增了批次26的投票汇总与收口；并补齐?b50_evidence_v3 ?size_mult 分桶证据（原先缺口已补）
- 你需要做仢么：不用再发外部AI；下丢步我直接?v0 的档位对?稳定性检验把证据表跑出来，再进入下一?
==============================
PANEL_VOTE_TSV（批?5；B20_VOL_ATR?==============================
model	q1_stoploss_warn_top2	q1_entry_filter_top2	q2_role_map_summary	q3_next_evidence_actions	contract_ok	notes
kimi	e1_retest_depth_atr(>q90);atr(>q90)	entry_vol_ratio(>q75);e1_break_strength_atr(>q75)	clear	q75/q90 + n>=100	ok	entry_vol_ratio 霢按symbol独立分位
deepseek	e1_retest_depth_atr;entry_vol_ratio	e1_break_strength_atr;atr	mixed	entry_vol_ratio给出风险解释	ok	atr不合跨symbol直接阈?glm	e1_atr_ratio;e1_retest_depth_atr	e1_break_strength_atr;q25(vol_ratio low)	clear	q25/q75 + n>=100	ok	指出 entry_vol_ratio 分桶数据缺失霢?qwen	e1_retest_depth_atr	atr	low_compliance	generic	partial	表格只给单项
doubao	atr(high);e1_retest_depth_atr(high)	e1_break_strength_atr(high);entry_vol_ratio(high)	clear	强调组合双高	ok	偏向 entry_vol_ratio=FILTER/ADD

==============================
DIFF_NOTES（批?5：只记录差异?+ 朢小证据动作）
==============================
- model: kimi/doubao vs glm
  divergence: entry_vol_ratio 的方向（高更?vs 低过滤）与角色（ENTRY_FILTER/ADD vs ENTRY_FILTER?  why_it_matters: 这是“确认加?过滤假突破的关键字段，但方向性搞反会导致漏掉强趋势或追高踩雷
  repo_action: NEED_EVIDENCE: 先补?entry_vol_ratio ?b20_bucket_stats 的分桶统计（目前 b20_bucket_stats_20260603_v1.csv 未包含该字段），再按 symbol/profile ?q25/q75 ?win_rate/avg_pnl/stop_loss_rate 对照
  reject_if: 直接给固定阈值（?1.5）但没有说明“按symbol分位”还是跨symbol统一?- model: deepseek vs kimi/doubao
  divergence: deepseek ?entry_vol_ratio 作为 stoploss_warn/风控信号之一；kimi/doubao 把它当作入场质量确认
  why_it_matters: 同一字段可能在极端高值与“中高表现不同（双刃剑），需要分桶不是一句话下结?  repo_action: NEED_EVIDENCE: ?entry_vol_ratio 同时?q75 ?q90 两个门槛（中?vs 极高），分别对照 stop_loss_rate ?avg_pnl
  reject_if: 没有区分 q75/q90 或样本量门槛
- model: 全体（共识）
  divergence: 极端桶样本量过小导致误判
  why_it_matters: 本批 b20 里多个最危险桶可能只有个位数/十位数样本，不能直接收口为硬门控
  repo_action: 固定规则：每?n_trades>=100 才允许写成建议阈值；不足只写“观察结论?  reject_if: 以小样本极端桶直接下硬阈?
==============================
BATCH_CLOSE（批?5收口：B20_VOL_ATR v0?==============================
- 裁决：B20 先分两类：E1质量（break_strength / retest_depth / e1_atr_ratio）与 风险环境（atr）entry_vol_ratio 暂定为确?过滤”，但需要补齐分桶证据后才能定方向?- 暂定 ROLE MAP（v0，先作为研究侧标记，不做执行门控）：
  - ENTRY_FILTER（质量）：e1_break_strength_atr（高值更好；低过滤弱突破?  - REDUCE/RISK（假突破/回撤风险）：e1_retest_depth_atr（高值更危险；用于减?收紧止损提示?  - RISK_ONLY（环境）：atr（高分位更危险；仅用于风?仓位/止损宽度，不跨symbol用绝对）
  - RISK/REDUCE（待证据）：e1_atr_ratio（存在分歧：追高风险 vs 动能强；霢要按分桶单调性验证）
  - NEED_EVIDENCE（缺分桶）：entry_vol_ratio（先补齐 b20_bucket_stats 分桶统计，再决定?ENTRY_FILTER/ADD 还是风险提示?- 下一步最小证据动作（v0）：
  - 补齐 entry_vol_ratio 分桶证据（并?symbol/profile 分层）；同时强制每桶 n_trades>=100
  - 做方向一致统计：?symbol/profile ?high vs low ?stop_loss_rate/avg_pnl 是否同向?=70% 同向才算稳定?
==============================
PANEL_VOTE_TSV（批?4；B30_STATE_VECTOR?==============================
model	q1_stoploss_warn_top3	q1_entry_filter_top2	q2_role_map_summary	q3_next_evidence_actions	contract_ok
kimi	sv_regime_code(expanding);sv_votes_short(high);sv_atr_ratio_1h(very_high)	sv_regime_code(squeeze);sv_votes_long_4(high)	complete	role_bucket_E1~E5	ok
deepseek	sv_atr_ratio_1h;sv_bb_ratio_4h;sv_regime_code	sv_votes_long_4;sv_votes_short_4	partial	role+thresholds	ok
glm	sv_atr_ratio_1h;sv_bb_ratio_4h;sv_regime_code	sv_votes_long;sv_bias	partial	role+5 actions	ok
qwen	sv_atr_ratio_1h	sv_bias	low_compliance	needs evidence	partial
doubao	sv_atr_ratio_1h;sv_votes_short_4(high);sv_bb_ratio_4h(extreme)	sv_regime_code(=0);sv_votes_long_4(high)	complete	role+thresholds	ok

==============================
DIFF_NOTES（批?4：只记录差异?+ 朢小证据动作）
==============================
- model: kimi vs deepseek/glm/doubao
  divergence: kimi ?sv_votes_short 作为主要 REDUCE 预警；其它更偏向 sv_votes_short_4 或不?votes_short
  why_it_matters: 影响“预警时效与阈稳定（1H?vs 4H票）
  repo_action: NEED_EVIDENCE: ?symbol/split/profile ?votes_short ?votes_short_4 的分位数分桶，对?stop_loss_rate ?top_minus_bot_pnl 的单调?  reject_if: 没有给出可复现分桶口?字段引用
- model: deepseek/glm/doubao vs kimi
  divergence: sv_bb_ratio_4h 的角色：deepseek/glm/doubao 更向 REDUCE/EXIT 风险提示；kimi 更偏 EXIT（q90/q10?  why_it_matters: 是否会把“低波压缩误当成减仓（可能反而是突破前的机会?  repo_action: NEED_EVIDENCE: ?sv_regime_code(0/1/2) 三段，再?sv_bb_ratio_4h ?q10/q90 分桶，看 stop_loss_rate ?win_rate 是否方向丢?  reject_if: 建议新增不存在字?改执行链?- model: qwen
  divergence: STRICT 合约不完整（只给了单项）
  why_it_matters: 不可直接用于投票收口
  repo_action: 仅保留为参，不计入多数裁决；若复问则要求?VOTE_TSV 输出
  reject_if: 给出不可复现的经验结论但无证据动?- model: kimi vs deepseek/glm/doubao
  divergence: sv_bias 角色分歧（ADD vs ENTRY_FILTER vs RISK_ONLY?  why_it_matters: 若误用，可能把方向偏置当成进场过滤成漏单/或把加仓信号用于减仓
  repo_action: NEED_EVIDENCE: ?sv_bias ?-1/0/+1 三档（如可用）并对照 trade_pnl / stop_loss_rate；若是连续则?q25/q75 分桶
  reject_if: 霢要新增字段但未给生成脚本

==============================
BATCH_CLOSE（批?4收口：B30_STATE_VECTOR v0?==============================
- 裁决：B30 的共识优先级”先?stop_loss 风险来：sv_atr_ratio_1h / sv_bb_ratio_4h / sv_regime_code 作为 RISK/REDUCE/ENTRY_FILTER 候；sv_votes_long_4 作为 ENTRY_FILTER 候（多数同意?- 暂定 ROLE MAP（v0，先作为研究侧标记，不做执行门控）：
  - ENTRY_FILTER：sv_regime_code（优?=0 SQUEEZE）；sv_votes_long_4（高值更好）
  - REDUCE/RISK：sv_atr_ratio_1h（高分位危险）；sv_bb_ratio_4h（极端分位需?regime 再定）；sv_votes_short / sv_votes_short_4（高值偏危险，待对照?  - ADD：sv_bias（存在分歧；先只观察不下结论?- 下一步最小证据动作（v0）：?E1~E5 做成可落盘分桶统计表（按 symbol/split/profile；优?since2022；可?core6 快跑?- 已完成证据动作（本地已跑；since2022；core6+observe7）：
  - COMMAND: .\.venv\Scripts\python.exe .\backtest_p0.py b30-evidence --date 20260603 --scope core_observe --split since2022 --out_dir .\backtest_out\stage2\indicator_audit\20260603_b30_evidence_v1
  - OUTPUT: backtest_out\stage2\indicator_audit\20260603_b30_evidence_v1\b30_bucket_stats_20260603_v1.csv
  - OUTPUT: backtest_out\stage2\indicator_audit\20260603_b30_evidence_v1\b30_feature_summary_20260603_v1.csv

==============================
BATCH_CLOSE（批?1收口 + 批次22启动?==============================
- 裁决：Q1=OK；Q2=丢致票?C06；Q3=多数 NEED_CHANGE（补充观测期字段?- 已落地（观测期）：`backtest_out\\stage2\\observe\\observe_20260603.csv` 已新?`entry_time_utc`、`snapshot_price`
- 已落地（结论不只停留在粘贴区）：
  - `02_阶段二_工作方向_想法?md`：MULTI_AI_BATCH21_DECISIONS
  - `03_阶段二_当下计划_执行清单.md`?.2（C06 ?gate 验证占位与产物命名）
- 已完成证据动作（批次22输入）：已生?C06 vs C03 ?gate 对照证据 `truegate_c06_vs_c03_agg_since2022_20260603_v1.csv`；下丢步进入基于证据裁决是?PROMOTE_C06”的多AI投票

==============================
PANEL_VOTE_TSV（批?2；来自最新回复汇总）
==============================
model	Q1	Q2	Q3	contract_ok	notes
kimi	NEED_MORE_EVIDENCE	avg_trades<C03*0.7 OR avg_net_pnl<=0	dd_ok;final_max_drawdown_pct;trades	partial	未按VOTE行显式给Q2/Q3，但正文给出规则与列
deepseek	PROMOTE_C06	NEED_EVIDENCE(dd_ok_rate/avg_net_pnl/avg_trades 门槛未给)	dd_ok;net_pnl;trades;final_max_drawdown_pct	partial	VOTE里Q2/Q3写OK，但正文给了invalidation_if与关注列
glm	NEED_MORE_EVIDENCE	avg_net_pnl<=0 OR trades<30	dd_ok;net_pnl;trades	partial	强调先补 agg 数摘?qwen	PROMOTE_C06	trades下降<=50% AND avg_net_pnl不转?dd_ok;avg_net_pnl;trades	partial	格式未严格，但提供可执行否决条件
doubao	PROMOTE_C06	avg_trades下降>30% OR avg_net_pnl转负则否?dd_ok_rate;avg_net_pnl;avg_trades	ok	朢贴近Q2/Q3要求

==============================
DIFF_NOTES（批?2：只记录差异?+ 朢小证据动作）
==============================
- divergence: kimi/glm 选择 NEED_MORE_EVIDENCE，?deepseek/qwen/doubao 倾向 PROMOTE_C06
  why_it_matters: 是否“证据已足够裁决”决定我们是继续加证据，还是直接收口删除伪差异组?  minimal_action: OUTBOUND 已补 `TRUEGATE_C06_VS_C03_AGG_TSV` 数摘录；下一轮仅霢外部AI基于该摘录重投一?Q1（避免没看见数成?NEED_MORE_EVIDENCE?- divergence: 多家模型提出新增文件/字段（如 combo_decision_c06_20260603.csv、EMA144斜率、VoltyChannel_Stop 等）
  why_it_matters: 这类建议若不收敛，会把讨论带离现有证据可复现口径?  minimal_action: 统一要求：新增字?新文?NEED_EVIDENCE（必须先指出落盘位置与生成脚本，否则仅作?EXTRA_THOUGHTS?- divergence: 否决阈不丢致（30%/50%/70% trades 下降门槛?  why_it_matters: 门槛不同会导致同丢证据下结论不?  minimal_action: 先固?1 条最小否决条件（推荐：avg_net_pnl<=0 ?avg_trades<C03*0.7），写入执行清单作为验收口径 v0

==============================
BATCH_CLOSE（批?2收口?==============================
- 裁决：在 scope=core+observe、window=since2022、best_profile 口径下，C06 vs C03 ?gate 汇数值完全一致（?TRUEGATE_C06_VS_C03_AGG_TSV）→ 暂不?C06 作为“有增量优势”的独立组合推进；默认保?C03
- QUESTION_DELTA：minor wording change（补?agg 数摘?+ 修正 OUTPUT CONTRACT ?VOTE 口径?- 下一步最小动作：?fullpool(32 symbols) ?C06 vs C03 since2022 ?gate 对照；若仍一致则?C06 标记为等价别?直接废弃，避免伪差异
- 暂缓项：trigger_type/regime_label 等观测字段扩张（现阶段先控制观测表列数）

通俗讲解（给用户看）?- 这轮我们在做仢么：?fullpool ?C07 vs C03 ?gate，对照KD三周期同向是否能提升稳健性?- 这轮新增/变化：已新增 `TRUEGATE_C07_VS_C03_FULLPOOL_AGG_TSV` 摘录并落盘两份证?CSV?- 你需要做仢么：不用再粘贴；下一步把 OUTBOUND 发给外部AI，让它们基于 C07 vs C03 ?tradeoff 投票（是否接受收益下降换更稳”）?
==============================
PANEL_VOTE_TSV（批?3；来自最新回复汇总）
==============================
model	Q1	Q2	Q3	contract_ok	notes
kimi	PROMOTE_C07	avg_net_pnl<C03*0.4 OR avg_trades<C03*0.6	dd_ok;net_pnl;trades	ok	额外提示：C06 可能未生效（已在批次22收口处理?deepseek	PROMOTE_C07	NEED_EVIDENCE(one_line_rule missing)	dd_ok;net_pnl;final_max_drawdown_pct	partial	VOTE写OK但未给一条可执行否决条件
glm	PROMOTE_C07	avg_net_pnl<=0 OR avg_trades<50	dd_ok;net_pnl;trades	ok	强调 trades 过低会导?sample 风险
qwen	PROMOTE_C07	avg_net_pnl_down<=50% OR avg_trades_down<=50%	dd_ok;net_pnl;final_max_drawdown_pct	ok	给出宽松阈?doubao	PROMOTE_C07	avg_net_pnl_down>50% OR avg_trades_down>35%	dd_ok_rate;avg_net_pnl;avg_abs_max_drawdown_pct	ok	给出中等阈?+ 品种丢致检查建?
==============================
DIFF_NOTES（批?3：只记录差异?+ 朢小证据动作）
==============================
- model: deepseek
  divergence: Q2 未提?one-line veto rule（VOTE 中写 OK?  why_it_matters: 没有可执行阈值就无法自动验收“收?频率下降是否可接受?  repo_action: 采用 kimi 的阈值作?v0（avg_net_pnl<C03*0.4 ?avg_trades<C03*0.6 否决）；并在想法?执行清单落盘
  reject_if: 引用不存在字?文件/flag
- model: kimi vs qwen/doubao/glm
  divergence: Q2 否决阈不同（40%/35%/50%/固定 trades<50?  why_it_matters: 阈不同会导致同一证据下PROMOTE/KEEP”裁决不丢?  repo_action: 固定 v0 阈（pnl>=0.4*C03 ?trades>=0.6*C03 ?avg_net_pnl>0）；若未来更保守，再收紧?doubao ?50%/35%
  reject_if: 把阈值写成无法从 CSV 计算的口?- model: 多家模型（用?  divergence: 提议新增组合（如 C08=squeeze+ema+kd）或做信号重?过滤信号胜率
  why_it_matters: 方向是好的，但需要新增证据表（否则不可复现）
  repo_action: 记录?EXTRA_THOUGHTS；若要推进，先定义过滤掉?entry 集合”落盘字段与生成脚本（NEED_EVIDENCE?  reject_if: 直接要求上门控上线或触发 MT5 自动执行

==============================
BATCH_CLOSE（批?3收口?==============================
- 裁决：Q1 丢致票 PROMOTE_C07（定位为“防守更强的研究侧，?C03 并列，不替代默认档）
- 朢小否决条件（v0）：avg_net_pnl<=0 ?avg_net_pnl < C03*0.4 ?avg_trades < C03*0.6
- 关键事实（fullpool=32；since2022；best_profile）：C07 dd_ok_rate 0.96875（↑? avg_abs_max_dd 0.12660（↓? avg_net_pnl 1313.67（仍为正但↓? avg_trades 110.56（↓?- 暂缓项：C08（squeeze+ema+kd）与“过滤掉的信号胜率分析（霢要新增证据口径与落盘?
通俗讲解（给用户看）?- 这轮我们在做仢么：基于?gate 证据裁决 C07 要不要作为防守档候?- 这轮新增/变化：外部AI丢致票同意 PROMOTE_C07，同时给出了不同的否决阈值；我已固定 v0 阈并写入收口?- 你需要做仢么：?OUTBOUND 发给外部AI就行（如果你还想让它们复核阈值）；否则我就按 v0 阈把 C07 写入三阶段文件的“防守档”并进入观测期?
### 2026-06-04 批次29收口（diag_rank 选题?
==============================
PANEL_VOTE_TSV（批?9；diag_rank?==============================
model	q1_focus_diags	q2_role_map_summary	q3_next_evidence_actions	contract_ok	notes
kimi	diag_session_skew_ratio;diag_session_pnl_london;diag_kd_1d_k_median	skew_ratio=REDUCE(per-symbol分位;可晋升ENTRY_FILTER);london_pnl=DIAG_ONLY→ENTRY_FILTER候?kd_1d_k_median=ADD(K<30或K>70)	5?skew分桶;London-only验证;KD×C07;skew×vol_state正交?三diag联合	ok	KD 阈给了全屢(0~100)，需证据验证跨品种可?deepseek	diag_session_skew_ratio;diag_session_pnl_london;diag_kd_1d_k_median	skew_ratio=REDUCE/RISK_ONLY; london_pnl=ADD; kd_1d_k_median=EXIT/DIAG_ONLY(>80回撤预警)	?symbol×profile 分层；分位桶?dd_ok/avg_pnl/win_rate；强调阈值需按品?ok	?kimi ?kd 的角色相反（ADD vs EXIT?glm	diag_session_skew_ratio;diag_session_pnl_london	skew_ratio=ENTRY_FILTER(top quartile保留/bottom过滤); london_pnl=ENTRY_FILTER(pnl>0保留/<0过滤)	quartiles/正负分桶；n>=100/20；相关去重；?dd_ok_rate	partial	未回答第三（kd/entry_n?qwen	diag_session_skew_ratio;diag_session_pnl_london;diag_entry_n	DIAG_ONLY（均建议 top quartile 但不落具体阈值）	?symbol×profile 分层；看 avg_pnl/dd_ok_rate/trades_count	ok	角色过保守（全部DIAG_ONLY），但题与数值引用合?doubao	diag_session_skew_ratio;diag_session_pnl_london;diag_entry_n	skew_ratio=ENTRY_FILTER(per-symbol q75以上);london_pnl=ENTRY_FILTER(伦敦时段优先);entry_n=ENTRY_FILTER(per-symbol q25~q75)	分层+合并桶；?avg_pnl/dd_ok_rate；统计过滤后 trades 保留?ok	?entry_n 当作 gate 候，但因果方向需谨慎

==============================
DIFF_NOTES（批?9：只记录差异?+ 朢小证据动作）
==============================
- divergence: diag_session_skew_ratio 的角色（ENTRY_FILTER vs REDUCE/RISK_ONLY vs DIAG_ONLY?  why_it_matters: 决定它是“硬过滤交易”还是只做仓?风险加权”，对频率与回撤形影响巨?  minimal_action: 先用 p0_sweep_summary 的行级（symbol×profile）做 quartiles 分桶，并分别?profile 内验?top/bot ?net_pnl ?dd_controlled_success 差异是否同向；若只在少数 profile 成立则降级为 DIAG_ONLY
- divergence: 第三候（diag_kd_1d_k_median vs diag_entry_n?  why_it_matters: kd 候可?C07（KD三周期）联动；entry_n 更像“结?过度交易诊断”，容易因果倒置
  minimal_action: ?entry_n 固定?DIAG_ONLY(sanity check)；把 kd_1d_k_median 作为 P2 候，仅在“与 C07 交叉?dd_ok_rate 提升?trades 不塌”时才晋?- divergence: 阈形式（per-symbol 分位 vs 全局阈）
  why_it_matters: 该批次的数据源是 p0_sweep_summary（每 symbol×profile 只有 1 行），无法做“每?symbol 内分位必须改成在 profile 内跨 symbol 的分位桶”或改用更细粒度数据?  minimal_action: 本轮先采?profile ?quartiles（跨 symbol）；若未来需?per-symbol，必须先落盘更细粒度?entry-time diag 序列（NEED_EVIDENCE?
==============================
BATCH_CLOSE（批?9收口：diag_rank v0?==============================
- 裁决（题优先级）：P1=diag_session_skew_ratio；P1=diag_session_pnl_london；P2=diag_kd_1d_k_median（与 C07 联动）；diag_entry_n 仅作?DIAG_ONLY（过度交?sanity-check），不晋?gate
- v0 ROLE MAP（研究侧标记，不做执行门控）?  - diag_session_skew_ratio：RISK_ONLY/REDUCE_CANDIDATE（若 quartile 证据稳定再虑 ENTRY_FILTER?  - diag_session_pnl_london：ENTRY_FILTER_CANDIDATE（先验证“London-only 子集”是否真的更好）
  - diag_kd_1d_k_median：ADD/EXIT 待证据（先与 C07 交叉决定方向?  - diag_entry_n：DIAG_ONLY
- 下一步最小证据动作（v0；基?p0_sweep_summary_20260603_v6.csv）：
  - ?skew_ratio / london_pnl：在 profile 内做 quartiles 分桶，输出每桶的 net_pnl、dd_controlled_success、trades；并做方向同向占比（?profile?  - ?kd_1d_k_median：先做简?quartiles，再加一张kd × C07（或等价 gate）的交叉表（?dd_controlled_success ?net_pnl 为主?  - 对共线：棢?skew_ratio ?best_session/session_pnl 的相关；若高度相关则只保留一个，避免重复门控

### 2026-06-04 批次30收口（diag_followups：分位桶证据→角色）

==============================
PANEL_VOTE_TSV（批?0；diag_followups?==============================
model	q1_skew_role	q1_london_role	q2_role_map_summary	q3_next_evidence_actions	contract_ok	notes
kimi	REDUCE	DIAG_ONLY	skew=REDUCE(profile_q4_bin1减仓/拒绝; q4_bin4可ADD候?; london_pnl=DIAG_ONLY(历史累计非实?; kd_1d_k=ADD(profile_q4); entry_n=DIAG_ONLY(滞后诊断)	entry_session 落盘；skew跨profile稳定性；kd×C07；skew×vol正交；entry_n因果验证	ok	明确指出“p0_sweep_summary 口径不能直接做笔过滤?deepseek	RISK_ONLY	ADD	skew=RISK_ONLY(高偏科风?; london_pnl=ADD; kd_1d_k=DIAG_ONLY; entry_n=DIAG_ONLY	NEED_EVIDENCE: 交易?entry-time 证据表（?diag_* 绑定到笔交易，再分桶?ok	?london_pnl 的ADD”需要额外证据支持（当前仍是 symbol×profile 级累计）
glm	ENTRY_FILTER	ENTRY_FILTER	skew/london/kd=ENTRY_FILTER(q4); entry_n=DIAG_ONLY	相关性去重；NEED_EVIDENCE: 交易级验证；跨profile稳定?partial	?dd_ok<0.5 仍当 ENTRY_FILTER，偏濢?qwen	DIAG_ONLY	DIAG_ONLY	全部 DIAG_ONLY	NEED_EVIDENCE: 更细粒度/每symbol证据	ok	偏保守但合规
doubao	ENTRY_FILTER	ENTRY_FILTER	skew/london/kd=ENTRY_FILTER(profile_q4_bin4); entry_n=DIAG_ONLY	跨profile丢致；NEED_EVIDENCE: per-symbol/entry-time 桶；相关性；过滤后频?ok	仍向直接?gate，但承认霢交易级验?
==============================
DIFF_NOTES（批?0：只记录差异?+ 朢小证据动作）
==============================
- divergence: skew 的角色（REDUCE/RISK_ONLY vs ENTRY_FILTER?  why_it_matters: 当前证据?top ?dd_ok_rate_w ?< 0.5（A_relaxed: 0.479），将其直接作为 ENTRY_FILTER 可能过度门控；更像风?仓位调节?  minimal_action: 以q4_bin1 作为 REDUCE/RISK_ONLY 预警、q4_bin4 仅作为加分标签先?v0；等交易级证据（entry-time）再讨论是否晋升 gate
- divergence: london_pnl 的语义（DIAG_ONLY vs ENTRY_FILTER/ADD?  why_it_matters: london_pnl ?symbol×profile 的历史累计表现，不是 entry-time 的当前是否伦敦盘”信号；直接?gate 会因果错?  minimal_action: 保持 DIAG_ONLY/候；下一步补 entry_time→session 的笔证据（London-only vs 全时段）后再评估
- divergence: kd_1d_k_median 的方向（ADD vs EXIT/DIAG_ONLY?  why_it_matters: 仅凭 symbol×profile 的分位桶无法区分“趋势强 vs 超买回撤”；必须?C07（KD三周期）联动或做更细粒度证据
  minimal_action: 先降级为 DIAG_ONLY_CANDIDATE；只有在“kd×C07 ?dd_ok_rate 提升?trades 不塌”时才晋升为 ADD/EXIT

==============================
BATCH_CLOSE（批?0收口：diag_followups v0?==============================
- 核心结论：在 p0_sweep_summary 的profile 内跨 symbol 分位桶证据下，`diag_session_skew_ratio` ?`diag_session_pnl_london` 呈现明显?top/bot 差异，但 top ?dd_ok_rate_w 未达到可直接?ENTRY_FILTER”的安全强度 ?先作?RISK/REDUCE 标签推进，不改执行默认?- v0 ROLE MAP（研究侧标记，不做执行门控）?  - diag_session_skew_ratio：REDUCE_CANDIDATE（profile q4_bin1 风险预警；q4_bin4 仅作为加分标签）
  - diag_session_pnl_london：DIAG_ONLY（；霢?entry-time session 证据后再评估 ENTRY_FILTER/ADD?  - diag_kd_1d_k_median：DIAG_ONLY（；待与 C07 交叉决定 ADD vs EXIT?  - diag_entry_n：DIAG_ONLY（滞后诊?过度交易 sanity-check?- 已完成证据动作（批次30输入）：
  - backtest_out\stage2\indicator_audit\20260604_diag_followups_v2\diag_followups_bucket_stats_20260604_v1.csv
  - backtest_out\stage2\indicator_audit\20260604_diag_followups_v2\diag_followups_feature_summary_20260604_v1.csv
  - backtest_out\stage2\indicator_audit\20260604_diag_followups_v2\diag_followups_corr_20260604_v1.csv
- 下一步最小证据动作（v0）：
  - NEED_EVIDENCE（交易级）：基于 trades_baseline_* 为每笔交易生?entry_session(Asia/London/NY) 并做 “London-only vs 全时段?的笔对照
  - NEED_EVIDENCE（交叉）：在 C07 gate 通过?trades 子集上，?kd_1d_k_median 做分位桶对照 dd_ok_rate / avg_pnl

### 2026-06-04 批次31证据（B10_SESSION：entry_session 逐笔对照?
- COMMAND: `.\.venv\Scripts\python.exe .\backtest_p0.py b10-evidence --date 20260604 --scope core_observe --split since2022`
- OUTPUT:
  - `backtest_out\stage2\indicator_audit\20260604_b10_evidence_v1\b10_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b10_evidence_v1\b10_bucket_agg_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b10_evidence_v1\b10_london_vs_all_pairs_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b10_evidence_v1\b10_london_vs_all_summary_20260604_v1.csv`
- 快摘录（bucket_agg；core6_observe7）：
  - ALL: n=7109 avg_pnl=6.38 stop_loss_rate=0.221
  - Asia: n=2015 avg_pnl=15.45 stop_loss_rate=0.292
  - London: n=2806 avg_pnl=39.84 stop_loss_rate=0.201
  - NY: n=2272 avg_pnl=-35.26 stop_loss_rate=0.179
- London vs All（按 symbol×profile；n_london>=20,n_all>=40）：n_pairs=38；frac_pnl_better=0.632；frac_stop_loss_better=0.711；frac_both=0.500

补充?026-06-04）：修复 `p0_sweep_dir` 根目录下的路径解析后，已重跑更完整版本（?truegate_* runs）：
- OUTPUT: `backtest_out\stage2\indicator_audit\20260604_b10_evidence_v2\b10_bucket_agg_20260604_v1.csv`
- OUTPUT: `backtest_out\stage2\indicator_audit\20260604_b10_evidence_v2\b10_london_vs_all_summary_20260604_v1.csv`
- bucket_agg（core6_observe7）：ALL n=12653 avg_pnl=24.77；London n=5267 avg_pnl=63.68；NY n=3756 avg_pnl=-31.25
- london_vs_all_summary：n_pairs=79；frac_pnl_better=0.633；frac_stop_loss_better=0.722；frac_both=0.544

### 2026-06-04 B20 证据补齐（entry_vol_ratio 重新纳入?
- COMMAND: `.\.venv\Scripts\python.exe .\backtest_p0.py b20-evidence --date 20260604 --scope core_observe --split since2022 --out_dir .\backtest_out\stage2\indicator_audit\20260604_b20_evidence_v3`
- OUTPUT:
  - `backtest_out\stage2\indicator_audit\20260604_b20_evidence_v3\b20_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b20_evidence_v3\b20_feature_summary_20260604_v1.csv`

### 2026-06-04 批次32收口（ADX / EMA / KD / vol_state；全品种?
- 输入（外部AI回帖）：`临时粘贴区_外部AI与终端输?md`（BATCH_ID=20260604_v32?- 证据（全品种；scope=all；split=since2022）：
  - `backtest_out\stage2\indicator_audit\diag_rank_20260604_v2.csv`
  - `backtest_out\stage2\indicator_audit\20260604_diag_followups_v3\diag_followups_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_diag_followups_v3\diag_followups_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_diag_followups_v3\diag_followups_corr_20260604_v1.csv`

PANEL_VOTE_TSV（批?2；只汇差异点）：
- kimi：聚?`diag_ema144_regime_long_frac` + `diag_kd_4h_k_median`；ema144=ADD(profile内分?，kd_4h=ADD(全局阈?；ADX=DIAG_ONLY；vol_squeeze=DIAG_ONLY/Regime 标签
- deepseek：聚?`diag_kd_1d_k_median`（但该项已在批次30收口? `diag_ema144_regime_long_frac` + `diag_vol_state_squeeze_frac`；强?NEED_EVIDENCE（更细粒?逐笔?- glm：聚?`diag_kd_1d_k_median` + `diag_ema144_regime_long_frac` + `diag_vol_state_squeeze_frac`；ema144=ENTRY_FILTER；vol_squeeze=RISK_ONLY
- qwen：ema144=DIAG_ONLY(per-symbol 分位)；kd_1d=ENTRY_FILTER（全屢阈）；adx_strong=RISK_ONLY
- doubao：kd_1d/ema144/kd_4h 倾向 ENTRY_FILTER（全屢阈）；承?NEED_EVIDENCE（per-symbol/逐笔? 去重

DIFF_NOTES（批?2：差异点 + 朢小证据动作）?- divergence: EMA144 regime 的阈值形式（全局>0.5 vs per-profile/per-symbol 分位?  minimal_action: 使用现有证据口径（p0_sweep_summary：profile 内跨 symbol ?qtiles4）先?v0；若后续?per-symbol，需要新?per-symbol 分位证据?- divergence: KD_4H 的角色（ADD/ENTRY_FILTER vs DIAG_ONLY?  minimal_action: 由于 `diag_kd_4h_k_median` ?`diag_kd_1d_k_median` spearman?.85~0.91（见 corr），先不并行晋升；优先做“多周期共振”的交易级证据再?- divergence: vol_state_squeeze_frac 的解释（收益高但 dd_ok ?vs regime 标签?  minimal_action: ?RISK_ONLY/REGIME_TAG 先落 v0，不做入场门控；霢要笔?entry-time vol_state 证据才能决定是否应收紧风?过滤?- divergence: ema_stack_bull_frac 是否独立
  minimal_action: corr 显示 ema144_regime_long_frac vs ema_stack_bull_frac spearman=1.0??profile 都是 1.0）→ 视为重复字段，后续只保留丢?
BATCH_CLOSE（批?2收口：v0）：
- v0 ROLE MAP（研究侧标记；不改执行默认）?  - diag_ema144_regime_long_frac：ADD_CANDIDATE（profile ?q4_bin4 加分）；REDUCE_CANDIDATE（q4_bin1 逆风预警?  - diag_kd_4h_k_median：DIAG_ONLY（；?kd_1d 高相关，先不独立晋升?  - diag_vol_state_squeeze_frac：RISK_ONLY（REGIME_TAG；先用于“高回撤风险提示/风险权重”）
  - diag_kd_align_3tf_frac：DIAG_ONLY（区分力弱；待交易级再评估）
  - diag_adx_*：DIAG_ONLY（当前框架内优先级低?  - diag_ema_stack_bull_frac：DEPRECATE（与 ema144_regime 完全重复?- 下一步最小证据动作（必须全品种）?  - NEED_EVIDENCE（交易级）：?EMA/KD/vol_state ?entry-time 状落?trades_baseline（笔分桶），验证是否能从“品种画像推广到“入场时点过滤?
### 2026-06-04 全品种证据补齐（scope=all；since2022?
- B20_VOL_ATR：`backtest_out\stage2\indicator_audit\20260604_b20_evidence_all_v1\*`
- B30_STATE_VECTOR：`backtest_out\stage2\indicator_audit\20260604_b30_evidence_all_v1\*`
- B40_E1_GEOMETRY：`backtest_out\stage2\indicator_audit\20260604_b40_evidence_all_v1\*`
- B50_SCORE_SIZING：`backtest_out\stage2\indicator_audit\20260604_b50_evidence_all_v1\*`

### 2026-06-04 批次33收口（B20_VOL_ATR：全品种?
证据（scope=all；split=since2022）：
- `backtest_out\stage2\indicator_audit\20260604_b20_evidence_all_v1\b20_feature_summary_20260604_v1.csv`
- `backtest_out\stage2\indicator_audit\20260604_b20_evidence_all_v1\b20_bucket_stats_20260604_v1.csv`
- 补证据（分层稳定?+ 覆盖率审计）?  - `backtest_out\stage2\indicator_audit\20260604_b20_followups_all_v1\b20_stability_pairs_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b20_followups_all_v1\b20_stability_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b20_followups_all_v1\b20_entry_vol_ratio_coverage_20260604_v1.csv`

==============================
PANEL_VOTE_TSV（批?3；B20_VOL_ATR?==============================
model	q1_entry_vol_ratio_role	q1_direction	q2_role_map_summary	q3_next_evidence_actions	contract_ok	notes
kimi	DIAG_ONLY	高更好（但覆盖不足）	break_strength=ENTRY_FILTER；retest_depth=REDUCE；atr=RISK_ONLY；entry_vol_ratio=DIAG_ONLY	?symbol×profile；交?正交性；coverage 审计	ok	明确指出 entry_vol_ratio coverage?0%
deepseek	ENTRY_FILTER（仅有时?甜点?高更好（但需谨慎?break_strength=ENTRY_FILTER；retest_depth=REDUCE/RISK；atr=RISK_ONLY(deciles10)；entry_vol_ratio=ENTRY_FILTER（仅当有值）	分层统计 + 缺失率分?ok	强调 ATR 应用 deciles10 抓尾部风?glm	ENTRY_FILTER	高更?entry_vol_ratio/break_strength=ENTRY_FILTER；retest_depth/atr=RISK_ONLY	分层验证 + 交叉验证	partial	未处?coverage 作为硬约?qwen	ENTRY_FILTER	高更好（NEED_EVIDENCE?break_strength/retest_depth/entry_vol_ratio=ENTRY_FILTER；atr=RISK_ONLY	分层统计（泛化）	partial	STRICT 合约较弱
doubao	ENTRY_FILTER	高更?break_strength=ENTRY_FILTER；retest_depth=ENTRY_FILTER；atr=RISK_ONLY；entry_vol_ratio=ENTRY_FILTER	分层统计 + 两套分桶对照	ok	未处?coverage 作为硬约?
==============================
DIFF_NOTES（批?3：只记录差异?+ 朢小证据动作）
==============================
- model: kimi vs glm/qwen/doubao/deepseek
  divergence: entry_vol_ratio 的角色（DIAG_ONLY vs ENTRY_FILTER）与是否把覆盖率不足”作为硬否决条件
  why_it_matters: 覆盖率低会导致?0% trades 没法决策”，把字段当 ENTRY_FILTER 会形成大面积盲区，且会引?profile/symbol 偏置
  repo_action: 固定 v0：entry_vol_ratio ?DIAG_ONLY（仅作为 quality_tag，不参与硬过滤）；必须先?coverage 提升到可接受水平（例?overall>=0.30 且多?symbol/profile ?0）才允许讨论晋升
  reject_if: ?coverage?0% 的前提下，把 entry_vol_ratio 写成“必须过”的 gate
- model: 外部AI（普遍） vs followups 证据
  divergence: break_strength_atr 的晋升强度（外部AI倾向 ENTRY_FILTER；followups 显示分层丢致一般）
  why_it_matters: 若分层一致不足，把它做硬过滤会导致少数品种有效其他品种反?无效”，朢终破坏全品种通用?  repo_action: ?b20_stability_summary 约束 v0：e1_break_strength_atr 先作?ADD_CANDIDATE/quality_score，不做硬过滤；后续仅在frac_both>=0.60 ?n_sufficient 足够”时才允许晋?ENTRY_FILTER
  reject_if: 只引?pooled ?top_minus_bot_avg_pnl（不?symbol×profile 稳定性）就下硬阈?- model: deepseek/glm
  divergence: atr 的分桶方案（deciles10 抓尾?vs qtiles4 更稳?  why_it_matters: atr 作为 RISK_ONLY 的核心是“尾部风险，?deciles10 在小样本 symbol/profile 上容易桶内不?  repo_action: v0：atr ?qtiles4 做主（更稳），deciles10 作为补充诊断（仅在该 symbol/profile 桶样本足够时启用?  reject_if: 给跨 symbol 的绝?atr 阈?
==============================
BATCH_CLOSE（批?3收口：B20_VOL_ATR v0；全品种?==============================
- 核心事实（feature_summary；全品种 pooled 起点）：
  - e1_break_strength_atr（qtiles4）：top_minus_bot_avg_pnl=7110.04；n_trades=12627
  - e1_retest_depth_atr（qtiles4）：top_minus_bot_avg_pnl=4634.04；n_trades=12627
  - atr（deciles10）：top_minus_bot_avg_pnl=6332.78；n_trades=19628
  - entry_vol_ratio（qtiles4）：top_minus_bot_avg_pnl=3085.15；n_trades=2058
- 分层稳定性（symbol×profile；top bucket vs bot bucket；见 b20_stability_summary_20260604_v1.csv）：
  - e1_break_strength_atr（qtiles4）：n_sufficient=61；frac_pnl_better?.531；frac_stop_loss_better?.396；frac_both?.333 ?丢致不足以支持硬门?  - atr（qtiles4）：n_sufficient=22；frac_both?.526 ?更合?RISK_ONLY（风险环境）
  - entry_vol_ratio（qtiles4）：n_sufficient=10；frac_both?.300 ?覆盖不足且稳定弱
- 覆盖率审计（entry_vol_ratio；见 b20_entry_vol_ratio_coverage_20260604_v1.csv）：
  - overall coverage?.103（denom=19628；num=2030）；87 ?symbol×profile ?58 个为 0 覆盖 ?不能作为 gate 必字?- v0 ROLE MAP（研究侧标记；不改执行默认）?  - e1_break_strength_atr：ADD_CANDIDATE（quality_score；qtiles4；q4_bin4 加分、q4_bin1 减分；暂不做 ENTRY_FILTER?  - e1_retest_depth_atr：REDUCE_CANDIDATE（qtiles4；深回踩桶作为风险提示；当前分层样本不足，先不落硬阈值）
  - atr：RISK_ONLY（以 qtiles4 为主；高?高波动风险提?仓位收缩候；deciles10 仅作补充诊断?  - entry_vol_ratio：DIAG_ONLY（quality_tag；仅在有值的 trades 上做加分/提示；coverage 达标前不晋升 gate?- 下一步最小证据动作（v0；不复问外部AI也能跑）?  - ?b20_stability_pairs 做按 profile 汇的丢致统计：分开统计 A_relaxed/A_strict/A_universal（避?pooled 掩盖 profile 偏置?  - ?break_strength_atr 做硬门控可行性门槛：若某 profile ?frac_both<0.60，则?profile 禁止晋升 ENTRY_FILTER（只允许 quality_score?  - 定位 entry_vol_ratio 缺失模式：按 symbol+profile 汇?coverage（已落盘），并列?coverage>0.30 的子集作为可研究晋升候，其余保持 DIAG_ONLY

通俗讲解（给用户看）?- 这轮我们在做仢么：?B20（break_strength / retest_depth / atr / entry_vol_ratio）从“全品种证据表收口成 v0 角色
- 这轮新增/变化：补?symbol×profile 的稳定与 entry_vol_ratio 覆盖率审计，发现 entry_vol_ratio 只有 ~10% trades 有?- 你需要做仢么：不用再发外部AI；下丢步直接按 v0 ?break_strength 先当质量加分、atr 当风险提示，继续推进其它批次指标再做组合

### 2026-06-04 追加证据（批?4输入：B30/B40/B50；全品种?
1) B30 followups（基?b30_bucket_stats；分层稳定）?- COMMAND:
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b30-followups --date 20260604 --scope all --split since2022 --bucket_stats .\backtest_out\stage2\indicator_audit\20260604_b30_evidence_all_v1\b30_bucket_stats_20260604_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260604_b30_followups_all_v1`
- OUTPUT:
  - `backtest_out\stage2\indicator_audit\20260604_b30_followups_all_v1\b30_stability_pairs_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b30_followups_all_v1\b30_stability_summary_20260604_v1.csv`
- 快摘录（stability_summary；n_sufficient / frac_both）：
  - sv_atr_ratio_1h(deciles10)：n_sufficient=24；frac_both?.417
  - sv_bb_ratio_4h(qtiles4)：n_sufficient=87；frac_both?.379
  - sv_regime_code(code)：n_sufficient=91；frac_both?.473

2) B40 followups（基?trades_baseline；合并桶稳定?+ 交互表）?- COMMAND:
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b40-followups --date 20260604 --scope all --split since2022 --out_dir .\backtest_out\stage2\indicator_audit\20260604_b40_followups_all_v1`
- OUTPUT:
  - `backtest_out\stage2\indicator_audit\20260604_b40_followups_all_v1\b40_stability_pairs_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b40_followups_all_v1\b40_stability_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b40_followups_all_v1\b40_interaction_sv_regime_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b40_followups_all_v1\b40_interaction_depth_atr_20260604_v1.csv`
- 快摘录（stability_summary；frac_both）：
  - 1_vs_ge2：n_pairs=74；frac_both?.419
  - le2_vs_3：n_pairs=20；frac_both?.250

3) B50 followups（基?b50_bucket_stats；size_mult 汇?+ entry_score 三段稳定表）?- COMMAND:
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b50-followups --date 20260604 --bucket_stats .\backtest_out\stage2\indicator_audit\20260604_b50_evidence_all_v1\b50_bucket_stats_20260604_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260604_b50_followups_all_v1`
- OUTPUT:
  - `backtest_out\stage2\indicator_audit\20260604_b50_followups_all_v1\b50_size_mult_agg_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b50_followups_all_v1\b50_entry_score_stability_20260604_v1.csv`

### 2026-06-04 批次34收口（B30/B40/B50；全品种?
证据（scope=all；split=since2022）：
- B30?  - `backtest_out\stage2\indicator_audit\20260604_b30_evidence_all_v1\b30_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b30_evidence_all_v1\b30_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b30_followups_all_v1\b30_stability_summary_20260604_v1.csv`
- B40?  - `backtest_out\stage2\indicator_audit\20260604_b40_evidence_all_v1\b40_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b40_followups_all_v1\b40_stability_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b40_followups_all_v1\b40_interaction_sv_regime_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b40_followups_all_v1\b40_interaction_depth_atr_20260604_v1.csv`
- B50?  - `backtest_out\stage2\indicator_audit\20260604_b50_evidence_all_v1\b50_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b50_followups_all_v1\b50_size_mult_agg_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b50_followups_all_v1\b50_entry_score_stability_20260604_v1.csv`

==============================
PANEL_VOTE_TSV（批?4；B30/B40/B50?==============================
model	q1_b30_dedup_keep	q1_b30_regime_role	q1_b30_atr_ratio_role	q1_b30_bb_role	q1_b30_votes_short_role	q2_b40_retest_role	q3_b50_entry_score_role	q3_b50_size_mult_role	contract_ok	notes
kimi	sv_bias（建?drop sv_votes_long_4?ENTRY_FILTER	RISK_ONLY	DIAG_ONLY	DIAG_ONLY	ENTRY_FILTER?_vs_ge2；但依赖 coverage?RISK_ONLY	CONFIG_BUCKET	ok	指出 bias ?votes_long_4 同构/重复
deepseek	sv_votes_long_4（其余降级）	ENTRY_FILTER	RISK_ONLY	RISK_ONLY	DIAG_ONLY	ENTRY_FILTER?_vs_ge2?ENTRY_FILTER_SWEETSPOT	CONFIG_BUCKET	ok	强调 sv_atr_ratio_1h ?stop_loss 预警?glm	sv_votes_long_4（drop sv_bias/short_4?（正文有冲突?RISK_ONLY	（未明确?（未明确?ENTRY_FILTER?_vs_ge2?ENTRY_FILTER_SWEETSPOT	CONFIG_BUCKET	partial	?sv_regime_code 的角色表述与多数不一?qwen	未定（偏保守?DIAG_ONLY	RISK_ONLY	RISK_ONLY	DIAG_ONLY	ENTRY_FILTER?_vs_ge2?RISK_ONLY/DIAG_ONLY	CONFIG_BUCKET	partial	STRICT 合约弱，更多是流程建?doubao	sv_votes_long_4（其余冗余归档）	ENTRY_FILTER	RISK_ONLY	RISK_ONLY	DIAG_ONLY	ENTRY_FILTER?_vs_ge2?ENTRY_FILTER_SWEETSPOT	CONFIG_BUCKET	ok	提出 NEED_EVIDENCE：sv_bb_ratio_4h 与平均单笔最大回撤的关系

==============================
DIFF_NOTES（批?4：差异点 + 收口原则?==============================
- divergence: B30 去重字段选择（sv_bias vs sv_votes_long_4?  why_it_matters: 两高相关且在本批证据上表现接近，保留两个会成重复门控/重复解释
  decision: v0 只保?sv_votes_long_4 作为“结构多头代表字段；sv_bias 降级?DIAG_ONLY（必要时用于解释方向偏置?  reject_if: 同时?sv_bias ?sv_votes_long_4 都做 ENTRY_FILTER
- divergence: B40 e1_retest_bars 是否晋升 ENTRY_FILTER
  why_it_matters: 全品种分层稳定不足（1_vs_ge2 ?frac_both?.419），直接做硬门控易出现少数品种有效其他品种不稳的泛化风险
  decision: v0 先做 DIAG_ONLY/质量标签（bars=1 preferred；bars>=2 风险提示候），不改执行默认；仅当后续在核心池/分层稳定性达?frac_both>=0.60 才讨论晋?  reject_if: 只引?pooled ?top_minus_bot_avg_pnl（不?symbol×profile 稳定性）就下硬阈?- divergence: B50 entry_score 的角色（sweetspot gate vs 风险标签?  why_it_matters: 当前三段棢验显示中段更低止损更稳定，但“中?pnl 朢好仅?37.7%（不具备强一致）
  decision: v0 固定 entry_score=RISK_ONLY（极?bin 警示/减仓提示候），暂不晋?ENTRY_FILTER_SWEETSPOT
  reject_if: ?entry_score 当作单调“越高越好的门控

==============================
BATCH_CLOSE（批?4收口：B30/B40/B50 v0；全品种?==============================
- B30 v0 ROLE MAP（研究侧标记；不改执行默认）?  - sv_regime_code：ENTRY_FILTER（regime 标签；与既有 C03 语义丢致）
  - sv_atr_ratio_1h：RISK_ONLY（高波动风险提示；不做入场过滤）
  - sv_bb_ratio_4h：DIAG_ONLY（需?regime 分层再讨论是否为 RISK/REDUCE?  - sv_votes_long_4：DIAG_ONLY（B30 内唯丢保留的结构投票代表字段；避免?sv_bias 重复?  - sv_votes_short_4：DIAG_ONLY（方向不对称，先不晋升）
- B40 v0 ROLE MAP（研究侧标记；不改执行默认）?  - e1_retest_bars：DIAG_ONLY（scheme=1_vs_ge2；bars=1 作为 preferred 标签?=2 作为风险提示候；稳定性达标前不晋?gate?- B50 v0 ROLE MAP（研究侧标记；不改执行默认）?  - size_mult：CONFIG_BUCKET（仓位率档位；仅复盘/参数对照?  - entry_score：RISK_ONLY（极?bin 警示；甜点区不足以晋?gate?- 下一步最小证据动作（v0）：
  - ?B30 ?sv_bb_ratio_4h 做极值风险补证据：在 trades_baseline 逐笔层面补一?max_drawdown_per_trade（NEED_EVIDENCE：需先定义与落盘口径），再做 q10/q90 对照
  - 复验 e1_retest_bars ?core6_observe7 子池的稳定（与全品种对比），决定是否允许“仅核心池晋?  - ?entry_score ?b50_entry_score_stability ?symbol×profile 汇：只允许排?bin1-2”这类轻量降噪，不做“保?mid 段的强门?
通俗讲解（给用户看）?- 这轮我们在做仢么：?B30/B40/B50 的外部AI回复收口?v0 角色（全品种口径?- 这轮新增/变化：外部AI普遍想把 B40/entry_score 做硬过滤，但分层稳定性不够，我们先降级为标签，避免过拟合
- 你需要做仢么：不用再发外部AI；我下一步开新批次做“未覆盖指标家族”（trades_baseline ?k/N/M/X 等形态字段）

### 2026-06-04 追加证据（批?5输入：B60_SWING_LEVELS；全品种?
- COMMAND:
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b60-evidence --date 20260604 --scope all --split since2022 --out_dir .\backtest_out\stage2\indicator_audit\20260604_b60_evidence_all_v1`
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b60-followups --date 20260604 --scope all --split since2022 --bucket_stats .\backtest_out\stage2\indicator_audit\20260604_b60_evidence_all_v1\b60_bucket_stats_20260604_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260604_b60_followups_all_v1`
- OUTPUT:
  - `backtest_out\stage2\indicator_audit\20260604_b60_evidence_all_v1\b60_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b60_evidence_all_v1\b60_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b60_followups_all_v1\b60_stability_pairs_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b60_followups_all_v1\b60_stability_summary_20260604_v1.csv`
- 快摘录（feature_summary；pooled 起点）：
  - sv_swing_low_4h(qtiles4)：n_trades=3461；top_minus_bot_avg_pnl?394.84
  - sv_swing_high_4h(qtiles4)：n_trades=3768；top_minus_bot_avg_pnl?129.41
- 关键约束（stability_summary；symbol×profile）：
  - sv_swing_high_4h：n_pairs=74，但 n_sufficient=2（桶内样本不足）
  - sv_swing_low_4h：n_sufficient=0（无法做分层稳定性判断）

### 2026-06-04 批次35收口（B60_SWING_LEVELS；全品种?
证据（scope=all；split=since2022）：
- `backtest_out\stage2\indicator_audit\20260604_b60_evidence_all_v1\b60_feature_summary_20260604_v1.csv`
- `backtest_out\stage2\indicator_audit\20260604_b60_evidence_all_v1\b60_bucket_stats_20260604_v1.csv`
- `backtest_out\stage2\indicator_audit\20260604_b60_followups_all_v1\b60_stability_summary_20260604_v1.csv`
- coverage（从 p0_sweep ?trades_baseline 逐笔抽查汇；?signal 非空视为 entry 行）?  - overall_total_entries=23657
  - sv_swing_low_4h coverage?.1937?582/23657?  - sv_swing_high_4h coverage?.2059?871/23657?
==============================
PANEL_VOTE_TSV（批?5；B60?==============================
model	q1_role_swing_low	q1_role_swing_high	q1_direction_low	q1_direction_high	q2_next_actions_summary	contract_ok	notes
kimi	DIAG_ONLY	DIAG_ONLY	高更好（pooled?高更好（pooled?coverage 审计/阈放?pooled 单调?品种类型/互斥性检?ok	强调分层稳定性崩盘（n_sufficient=0/2?deepseek	DIAG_ONLY	DIAG_ONLY	低区或两端差（试探）	低区或两端差（试探）	扩展 split ?pre2022；合?profile；主指标 avg_pnl+stop_loss_rate	ok	强调可能由少数品种驱?glm	DIAG_ONLY	DIAG_ONLY	不确?不确??n>=10；binary 分桶；NEED_EVIDENCE max_drawdown_per_trade	ok	建议减少桶数提升 n_sufficient
qwen	ENTRY_FILTER（但证据不足?ENTRY_FILTER（但证据不足?高更好（直接?pooled 推）	高更好（直接?pooled 推）	重复强调“需要更多数据?partial	忽略 n_sufficient=0/2 的硬约束
doubao	DIAG_ONLY（自相矛盾：先写 ENTRY_FILTER 又写暂存诊断?DIAG_ONLY（同上）	低位更优（推断）	低位更优（推断）	NEED_EVIDENCE max_drawdown；拆?session/regime	partial	方向?pooled ?top_minus_bot 不一致，且分层不?
==============================
DIFF_NOTES（批?5：差异点 + 收口原则?==============================
- divergence: 方向（高更好 vs 低更?vs 两端差）
  why_it_matters: 当前只有 pooled ?top_minus_bot（无法确定单?甜点区），且分层稳定性几乎为 0 ?方向讨论属于“假精确?  decision: v0 不给方向阈；先固?DIAG_ONLY，再用更少桶/更低门槛?n_sufficient 拉起来后再讨论方?  reject_if: 仅凭 top_minus_bot_avg_pnl 就直接下“高/低更好的硬门控结?- divergence: 是否晋升 ENTRY_FILTER
  why_it_matters: sv_swing_low_4h n_sufficient=0；sv_swing_high_4h n_sufficient=2 ?frac_both=0.0 ?全品种分层不支持 gate
  decision: v0 全部锁定 DIAG_ONLY（不进过滤池），避免“少数品种有效的过拟?  reject_if: ?n_sufficient<15 ?frac_both<0.30 时推进任何硬过滤

==============================
BATCH_CLOSE（批?5收口：B60 v0；全品种?==============================
- v0 ROLE MAP（研究侧标记；不改执行默认）?  - sv_swing_low_4h：DIAG_ONLY（pooled 差异大，但分层稳定?0；coverage?9%?  - sv_swing_high_4h：DIAG_ONLY（n_sufficient=2 ?frac_both=0.0；coverage?1%?- 决策理由（一句话）：在全品种 + symbol×profile 分层稳定性的硬约束下，B60 当前只能做诊断标签，不能做用过滤/加减仓门控?- 下一步最小证据动作（用于决定是否解冻 B60）：
  - 降维与放宽：profile 合并?A_all + ?symbol 桶门槛从 n>=20 放宽?n>=10，重?n_sufficient / frac_both
  - 改桶：从 qtiles4 改成 binary（near vs far / above vs below median），减少桶数提升样本?  - 扩窗口：split 扩展?pre2022（或 full）做对照，验证稳定是否来自窗口太短?  - NEED_EVIDENCE：若要评估极值风险，霢要定义并落盘 max_drawdown_per_trade，再?swing 极桶的回撤对?
通俗讲解（给用户看）?- 这轮我们在做仢么：把摆动高低点（B60）从“看起来有差异推进到“能不能当用门控”的裁决
- 这轮新增/变化：确?coverage?0%，但分层稳定性几乎为 0（n_sufficient=0/2）→ 先锁?DIAG_ONLY
- 你需要做仢么：不用再发外部AI；下丢步我按降?二桶+扩窗口把 B60 的稳定补齐，再决定是否解?
### 2026-06-04 追加证据（B60 v2：布尔字段纳?+ 放宽分层门槛?
- 变更点（证据口径不变；只是把 trades_baseline 里的 True/False 字段纳入分桶，并?followups 放宽分层门槛）：
  - b60-evidence：支持把 True/False 解析?code=0/1 分桶（新增覆盖：sv_risk_on_mkt / sv_use_struct_vote?  - b60-followups：支?`--min-n` ?`--profile-merge`（用于提?n_sufficient?- COMMAND（since2022；scope=all）：
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b60-evidence --date 20260604 --scope all --split since2022 --q 4 --out_dir .\backtest_out\stage2\indicator_audit\20260604_b60_evidence_all_v2`
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b60-followups --date 20260604 --scope all --split since2022 --min-n 10 --profile-merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260604_b60_evidence_all_v2\b60_bucket_stats_20260604_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260604_b60_followups_all_v2`
- OUTPUT?  - `backtest_out\stage2\indicator_audit\20260604_b60_evidence_all_v2\b60_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b60_followups_all_v2\b60_stability_summary_20260604_v1.csv`
- 快摘录（stability_summary；symbol×A_all；min_n=10）：
  - sv_risk_on_mkt(code)：n_sufficient=32；frac_both?.500；frac_stop_loss_better?.719
  - sv_use_struct_vote(code)：n_sufficient=32；frac_both?.469；frac_stop_loss_better?.625
  - sv_swing_high_4h(qtiles4)：n_sufficient=14；frac_both?.357
  - sv_swing_low_4h(qtiles4)：n_sufficient=11；frac_both?.364
- 补充：把 swing 两列强制降桶?q=2（binary；since2022；min_n=10；A_all）后，n_sufficient 提升?28/30，但 frac_both 下降??.286/0.300 ?仍不支持晋升 gate

### 2026-06-08 追加证据（B60 v5：pre2022 对照；min_n=10；profile_merge=A_all?
- 目的：完成扩窗口?pre2022”的对照，判?B60 的稳定是否只来自 since2022 窗口
- COMMAND（scope=all）：
  - since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b60-evidence --date 20260608 --scope all --split since2022 --out_dir .\backtest_out\stage2\indicator_audit\20260608_b60_evidence_since2022_v2` + `b60-followups --min_n 10 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b60_evidence_since2022_v2\b60_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b60_followups_since2022_v2`
  - pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b60-evidence --date 20260608 --scope all --split pre2022 --out_dir .\backtest_out\stage2\indicator_audit\20260608_b60_evidence_pre2022_v2` + `b60-followups --min_n 10 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b60_evidence_pre2022_v2\b60_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b60_followups_pre2022_v2`
- OUTPUT?  - since2022：`backtest_out\stage2\indicator_audit\20260608_b60_evidence_since2022_v2\b60_feature_summary_20260608_v1.csv` + `backtest_out\stage2\indicator_audit\20260608_b60_followups_since2022_v2\b60_stability_summary_20260608_v1.csv`
  - pre2022：`backtest_out\stage2\indicator_audit\20260608_b60_evidence_pre2022_v2\b60_feature_summary_20260608_v1.csv` + `backtest_out\stage2\indicator_audit\20260608_b60_followups_pre2022_v2\b60_stability_summary_20260608_v1.csv`
- 快摘录（stability_summary；symbol×A_all；min_n=10）：
  - sv_swing_high_4h(qtiles4)：since2022 n_sufficient=14 frac_both?.357；pre2022 n_sufficient=16 frac_both=0.250
  - sv_swing_low_4h(qtiles4)：since2022 n_sufficient=11 frac_both?.364；pre2022 n_sufficient=15 frac_both?.267
  - sv_swing_present_4h(code)：since2022 frac_both?.531；pre2022 frac_both?.464
  - sv_risk_on_mkt(code)：since2022 frac_both=0.500；pre2022 frac_both?.393
  - sv_use_struct_vote(code)：since2022 frac_both?.469；pre2022 frac_both?.357
- 结论：pre2022 整体偏弱（尤?swing_high/low），因此不改角色裁决（swing_high/low 仍冻?DIAG_ONLY；swing_present 维持条件?ADD_CANDIDATE；risk_on 维持 RISK_ONLY；use_struct_vote 维持 DIAG_ONLY?
### 2026-06-04 组合验证 v0（全品种；先看标签组合是否一致改善）

- COMMAND?  - `.\.venv\Scripts\python.exe .\backtest_p0.py combo-v0 --date 20260604 --scope all --split since2022 --out_dir .\backtest_out\stage2\indicator_audit\20260604_combo_v0_all_v2`
- OUTPUT?  - `backtest_out\stage2\indicator_audit\20260604_combo_v0_all_v2\combo_v0_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_combo_v0_all_v2\combo_v0_top_20260604_v1.csv`
- 快摘录（marginal；仅统计 bs/depth/bars 缺失的行；每?n>=100；按 n_trades 加权）：
  - sv_risk_on_mkt：risk=0 ?avg_pnl?2.99；stop_loss_rate?.241；risk=1 ?avg_pnl?157.05；stop_loss_rate?.254
  - sv_use_struct_vote：struct=0 ?avg_pnl?32.01；stop_loss_rate?.255；struct=1 ?avg_pnl?80.63；stop_loss_rate?.235
  - atr(qtiles4)：bin3/4 ?avg_pnl 更高（≈16.84/33.34）且 bin3 ?stop_loss_rate 更低（≈0.217）；bin1 明显更差（avg_pnl?214?
### 2026-06-04 新指标家族（批次36输入：B31_STRUCT_VOTE_WINDOW；votes_3 vs votes_4?
- 目标：验?`sv_votes_long_3/short_3` 是否提供不同?`sv_votes_long_4/short_4` 的信息，决定是否霢要纳入讨?组合
- COMMAND?  - `.\.venv\Scripts\python.exe .\backtest_p0.py b31-evidence --date 20260604 --scope all --split since2022 --out_dir .\backtest_out\stage2\indicator_audit\20260604_b31_evidence_all_v2`
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b31-followups --date 20260604 --scope all --split since2022 --bucket_stats .\backtest_out\stage2\indicator_audit\20260604_b31_evidence_all_v2\b31_bucket_stats_20260604_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260604_b31_followups_all_v2`
- OUTPUT?  - `backtest_out\stage2\indicator_audit\20260604_b31_evidence_all_v2\b31_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b31_followups_all_v2\b31_stability_summary_20260604_v1.csv`
- 摘录（feature_summary；pooled；votes 高组-低组）：
  - sv_votes_long_3 / sv_votes_long_4：top_minus_bot_avg_pnl?30.41；n_trades?2397
  - sv_votes_short_3 / sv_votes_short_4：top_minus_bot_avg_pnl?130.41；n_trades?2397
- 摘录（stability_summary；symbol×profile；sufficient 全部可用）：
  - sv_votes_long_3 / sv_votes_long_4：n_sufficient=95；frac_both?.400
  - sv_votes_short_3 / sv_votes_short_4：n_sufficient=95；frac_both?.316

### 2026-06-04 追加：indicator-audit v2（把 trades_baseline 新字段纳入全量扫”）

- 目的：让“全量扫丢遍→自动分批”能覆盖 trades_baseline 里已存在但此前没纳入的字段（sv_use_struct_vote / votes_3 / swing / k/N/M/X/stop_k/risk_per_trade?- COMMAND?  - `.\.venv\Scripts\python.exe .\backtest_p0.py indicator-audit --date 20260604 --out_dir .\backtest_out\stage2\indicator_audit\20260604_v2`
  - `.\.venv\Scripts\python.exe .\backtest_p0.py indicator-batches --date 20260604 --features_csv .\backtest_out\stage2\indicator_audit\20260604_v2\indicator_audit_features.csv --out_dir .\backtest_out\stage2\indicator_audit\20260604_batches_v2`
- OUTPUT?  - `backtest_out\stage2\indicator_audit\20260604_v2\indicator_audit_features.csv`
  - `backtest_out\stage2\indicator_audit\20260604_batches_v2\indicator_batch_items_20260604_v1.csv`
- 快摘录（batch_items；加?top_minus_bot_w）：
  - B30 新增字段：sv_risk_on_mkt / sv_use_struct_vote / sv_votes_*_3 / sv_swing_high_4h / sv_swing_low_4h
  - B99 新增字段：stop_k / risk_per_trade

### 2026-06-04 追加证据（B99 v3：stop_k / risk_per_trade 分桶?
- COMMAND?  - `.\.venv\Scripts\python.exe .\backtest_p0.py b99-evidence --date 20260604 --scope all --split since2022 --out_dir .\backtest_out\stage2\indicator_audit\20260604_b99_evidence_all_v3`
- OUTPUT?  - `backtest_out\stage2\indicator_audit\20260604_b99_evidence_all_v3\b99_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b99_evidence_all_v3\b99_bucket_stats_20260604_v1.csv`
- 摘录（value_code；pooled 加权）：
  - stop_k=1.500：n?8465；avg_pnl?38.44；stop_loss_rate?.211
  - stop_k=2.000：n?906；avg_pnl?.13；stop_loss_rate?.249
  - risk_per_trade=0.023：n?1435；avg_pnl?32.18；stop_loss_rate?.216
  - risk_per_trade=0.020：n?024；avg_pnl?2.34；stop_loss_rate?.251

### 2026-06-04 组合验证 v0（二次突进：只看 bs/depth/bars 同时存在的子集）

- 数据源：`backtest_out\stage2\indicator_audit\20260604_combo_v0_all_v2\combo_v0_bucket_stats_20260604_v1.csv`
- 过滤口径：bs_bin!=na ?depth_bin!=na ?bars_grp!=na；并要求 n_trades>=100
- 结果：仅 7 行（trades_sum=772），样本仍偏少；暂不用于晋升 gate，只作组合交互是否得补样本的线索

==============================
PANEL_VOTE_TSV（批?8；B30_VOL_SQUEEZE_ATR_RATIO?==============================
batch_id	q1_focus_diags	q2_role_map_summary	q3_next_evidence_actions
20260604_v38	sv_bb_ratio_4h;sv_atr_ratio_1h	多数：sv_atr_ratio_1h=RISK_ONLY（方向需以证据为准，建议?MAE）；sv_bb_ratio_4h=ADD/或RISK（分歧较大，建议先做 pooled bin 方向验证 + ?regime_code 正交?1)bb_ratio pooled(bin1~bin4)方向验证?)atr_ratio 合并?q10→q4)提升稳定性；3)atr_ratio×vol_state/×regime_code 正交性；4)NEED_EVIDENCE: trade_mae_atr / max_drawdown_per_trade?)验证“极端桶回撤是否更大?
==============================
DIFF_NOTES（批?8?==============================
- kimi/deepseek/千问/豆包?sv_atr_ratio_1h 的方向上存在口径误读风险：需要用 pooled 分桶与合并桶稳定性（q10→q4）确认高/低更危险”?- ?sv_bb_ratio_4h：外部AI提出“甜点区/两端差的假设，但霢先用 pooled(bin1~bin4)验证；若 bin1 朢优则不支持甜点区?
==============================
BATCH_CLOSE（批?8；以证据拍板?==============================
- 证据（scope=all；split=since2022）：
  - `backtest_out\stage2\indicator_audit\20260604_b30_evidence_all_v1\b30_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b30_followups_all_v1\b30_stability_summary_20260604_v1.csv`
  - 补证据（pooled bin 方向 + atr_ratio 合并桶稳定?+ bb_ratio×regime proxy）：`backtest_out\stage2\indicator_audit\20260604_b30_followups_all_v2\*`
- 新增补证据（批次38新增；不改执行辑）：
  - `backtest_out\stage2\indicator_audit\20260604_b30_followups_all_v2\b30_pooled_bins_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b30_followups_all_v2\b30_atr_ratio_deciles_merged_q4_pooled_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b30_followups_all_v2\b30_atr_ratio_deciles_merged_q4_stability_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b30_followups_all_v2\b30_bb_ratio_x_regime_interaction_proxy_20260604_v1.csv`
- 裁决（研究侧 v0；默认不接入执行门控）：
  - sv_atr_ratio_1h：ENTRY_FILTER（弱门槛：避免最?1/4；高值更好）。依据：合并桶稳定?frac_both?.658（n_sufficient=79），?pooled 合并桶单调（bin4 avg_pnl?8.27 ?stop_loss_rate?.144，bin1 avg_pnl?83.39 ?stop_loss_rate?.288）?  - sv_bb_ratio_4h：DIAG_ONLY（收益与 MAE 双口径不丢致，不晋升风?过滤）依据：收益口径?pooled bin1/2 avg_pnl 为正?bin3/4 为负；但 MAE 口径下高 bb_ratio 并未表现出更?mae_mean，且 stop_loss_rate 也非单调恶化，更像状?结构性解释变量非稳定风控门控?- NEED_EVIDENCE（决定是否把 atr_ratio 从弱门槛”升级为“硬过滤/或仅风险标签”）?  - trade_mae_atr / max_drawdown_per_trade：需要笔的持仓期朢大不利波动（MAE）在 ATR 单位下的分桶对照，用于判断低 atr_ratio 是否只是更容?hit stop，还是持仓过程更痛苦”?
### 2026-06-04 补齐 NEED_EVIDENCE（批?8）：trade_mae_atr / trade_mfe_atr（笔；ATR归一化）

- COMMAND?  - `.\.venv\Scripts\python.exe .\backtest_p0.py b30-mae --date 20260604 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260604_b30_mae_all_v1`
- OUTPUT?  - `backtest_out\stage2\indicator_audit\20260604_b30_mae_all_v1\b30_mae_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b30_mae_all_v1\b30_mae_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b30_mae_all_v1\b30_mae_coverage_20260604_v1.csv`（priced_pct=1.0，说明笔窗口能完整对齐到 1H 行情?- 关键事实（pooled；按 bucket 汇加权）?  - sv_atr_ratio_1h(deciles10)：q10_bin1 mae_mean?.875、mae_p90?.905；q10_bin10 mae_mean?.345、mae_p90?.266（高 atr_ratio 持仓期最大不利波动更小）
  - sv_bb_ratio_4h(qtiles4)：q4_bin1 mae_mean?.589；q4_bin4 mae_mean?.486（高 bb_ratio 并未表现出更?MAE?- 结论更新（研究侧 v0）：
  - sv_atr_ratio_1h：维持高更好、低更差”的方向；弱门槛（排除最?/4）更合理
  - sv_bb_ratio_4h：回撤（MAE）口径下不支持高更差”，?DIAG_ONLY 处理（不晋升 RISK_ONLY/过滤?
### 2026-06-04 新指标家族（批次39输入：B31_STRUCT_VOTE_WINDOW；votes_3 vs votes_4 + bias?
- COMMAND?  - `.\.venv\Scripts\python.exe .\backtest_p0.py b31-evidence --date 20260604 --scope all --split since2022 --out_dir .\backtest_out\stage2\indicator_audit\20260604_b31_evidence_all_v1`
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b31-followups --date 20260604 --scope all --split since2022 --bucket_stats .\backtest_out\stage2\indicator_audit\20260604_b31_evidence_all_v1\b31_bucket_stats_20260604_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260604_b31_followups_all_v1`
- OUTPUT?  - `backtest_out\stage2\indicator_audit\20260604_b31_evidence_all_v1\b31_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b31_evidence_all_v1\b31_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b31_followups_all_v1\b31_stability_summary_20260604_v1.csv`
- 快摘录（feature_summary；pooled 加权；top_minus_bot_avg_pnl）：
  - sv_bias(bias_code)：n?2397；top_minus_bot?30.41
  - sv_votes_long_3(votes_01234)：n?2397；top_minus_bot?30.41
  - sv_votes_long_4(votes_01234)：n?2397；top_minus_bot?30.41
  - sv_votes_short_3(votes_01234)：n?2397；top_minus_bot?130.41
  - sv_votes_short_4(votes_01234)：n?2397；top_minus_bot?130.41
- 分层摘录（stability_summary；symbol×profile；sufficient 对）?  - sv_bias：n_pairs=95；n_sufficient=95；frac_both?.400；frac_stop_loss_better?.579
  - sv_votes_long_4：n_pairs=95；n_sufficient=95；frac_both?.400；frac_stop_loss_better?.579
  - sv_votes_short_4：n_pairs=95；n_sufficient=95；frac_both?.316；frac_stop_loss_better?.400

==============================
PANEL_VOTE_TSV（批?9；B31_STRUCT_VOTE_WINDOW?==============================
batch_id	q1_focus_diags	q2_role_map_summary	q3_next_evidence_actions
20260604_v39	sv_bias;sv_votes_long_3;sv_votes_long_4;sv_votes_short_3;sv_votes_short_4	多数：指出强同构/冗余”（bias≡votes_long_3≡votes_long_4；votes_short_3≡votes_short_4），并向全部 DIAG_ONLY（不晋升 gate?若要进一步严谨：补相关系?共线性证据（pearson/spearman；按 symbol×profile ?pooled），以及 votes×sv_regime_code 的交叉表看是否只?regime 代理变量

==============================
DIFF_NOTES（批?9?==============================
- model: kimi
  divergence: 明确主张全部 DIAG_ONLY，并提出“仅保留朢小保留集 {sv_bias, sv_votes_short_4}?  why_it_matters: 与证据一致（top_minus_bot?30 太弱；且统计完全同构意味睢维护成本高增量信息接?0?  repo_action: 在想法库/执行清单里固化去重规则，避免后续组合表重复加入同构字?  reject_if: ?- model: deepseek
  divergence: 主张 sv_bias=ENTRY_FILTER，votes_4=ADD（高票加分）
  why_it_matters: 若把弱区分力信号直接晋升为门控，容易引入“伪过滤/伪加分并恶化泛化
  repo_action: 维持研究?DIAG_ONLY；若未来要晋升，先要求top_minus_bot 至少上千级别?frac_both>=0.60”或提供额外证据（交叉正?组合边际?  reject_if: 引入不存在字段（?dd_ok_rate）或要求改执?MT5
- model: 千问
  divergence: ?votes_long_* 直接判为 ENTRY_FILTER、votes_short_* 判为 REDUCE
  why_it_matters: 与当?top_minus_bot?30 的弱区分力不匹配
  repo_action: ?deepseek：不晋升 gate，仅保留为诊断标签并去重
  reject_if: ?- model: 豆包
  divergence: 倾向 votes_long_4=ENTRY_FILTER、votes_short_4=RISK_ONLY（但同时承认同构与弱区分力）
  why_it_matters: 指向“可用作轻量标签/权重”但目前证据不足以晋?  repo_action: 固化?DIAG_ONLY + 去重；后续若要讨论权重，必须先补“组合边际收?风险”证?  reject_if: ?
==============================
BATCH_CLOSE（批?9；以证据拍板?==============================
- 证据（scope=all；split=since2022）：
  - `backtest_out\stage2\indicator_audit\20260604_b31_evidence_all_v1\b31_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b31_evidence_all_v1\b31_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b31_followups_all_v1\b31_stability_summary_20260604_v1.csv`
- 裁决（研究侧 v0；默认不接入执行门控）：
  - B31 这组“投票窗/偏置”整体区分力很弱（top_minus_bot?30 级别），不足以讨?ENTRY_FILTER/ADD/REDUCE 的晋?  - 统一定：sv_bias / sv_votes_long_3 / sv_votes_long_4 / sv_votes_short_3 / sv_votes_short_4 全部 DIAG_ONLY
  - 去重规则（v0）：sv_votes_long_3 视为冗余（DEPRECATE）；sv_votes_short_3 视为冗余（DEPRECATE）；sv_bias ?sv_votes_long_4 同构（二选一；默认保?sv_votes_long_4 作为代表字段，保持与既有 B30 命名丢致）
- 下一步：不再投入额外证据；若未来在组合验证里看到明显边际，再单独弢批次做组合边际收?风险”验?
### 2026-06-05 追加证据（批?0输入：B10_SESSION；全品种?
- COMMAND?  - `.\.venv\Scripts\python.exe .\backtest_p0.py b10-evidence --date 20260605 --scope all --split since2022 --out_dir .\backtest_out\stage2\indicator_audit\20260605_b10_evidence_all_v1`
- OUTPUT?  - `backtest_out\stage2\indicator_audit\20260605_b10_evidence_all_v1\b10_feature_summary_20260605_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260605_b10_evidence_all_v1\b10_bucket_agg_20260605_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260605_b10_evidence_all_v1\b10_london_vs_all_summary_20260605_v1.csv`
- 快摘录（pooled；b10_bucket_agg）：
  - Asia：avg_pnl?5.38；stop_loss_rate?.285；tp2_rate?.449
  - London：avg_pnl?21.33；stop_loss_rate?.212；tp2_rate?.583
  - NY：avg_pnl?53.95；stop_loss_rate?.175；tp2_rate?.667
- 分层丢致（symbol×profile；b10_london_vs_all_summary）：n_pairs=159；frac_both?.453（接近可讨论晋升”的门槛?- 补充摘录（b10_london_vs_all_pairs；delta 分布；n_pairs=159）：
  - delta_avg_pnl（London-ALL）分位：q10?205.43；q50?9.34；q90?26.70
  - delta_stop_loss_rate（London-ALL）分位：q10?0.0631；q50?0.0094；q90?.0553

==============================
PANEL_VOTE_TSV（批?0；B10_SESSION?==============================
batch_id	q1_focus_diags	q2_role_map_summary	q3_next_evidence_actions
20260605_v40	entry_session(Asia/London/NY)	多数：entry_session 整体=DIAG_ONLY（当?pooled 下各 session avg_pnl 均为负，只能讨论“相对差异）；London=ADD_CANDIDATE（边界：frac_both?.453）；Asia/NY=DIAG_ONLY（trade-off 强，不做硬过滤）	1)?symbol×profile ?London vs All / NY vs non-NY 的方向一致；2)session×vol_state?×3）交叉；3)?MAE 口径（trade_mae_atr ?session 分组?
==============================
DIFF_NOTES（批?0?==============================
- model: kimi
  divergence: ?London 明确定位?ADD（），同时主?session 整体不做硬门?  why_it_matters: 与当前证据匹配（frac_both?.453 边界值；pooled ?session avg_pnl 均为负）
  repo_action: BATCH_CLOSE 中按“DIAG_ONLY + London ADD_CANDIDATE”收口，并把“分层一致?交叉?MAE口径”列为后续最小证据动?  reject_if: ?- model: deepseek
  divergence: 倾向给出 ADD/RISK_ONLY（含“纽约回?降低仓位”）
  why_it_matters: 在未?MAE / 单笔回撤口径前，直接?RISK_ONLY 易误把低 stop_loss_rate + 更差 pnl”的结构当作风险更高
  repo_action: 维持 NY=DIAG_ONLY；把“NY 是否更痛苦推迟到 trade_mae_atr ?session 分组后再判断
  reject_if: 任何执行侧直接改仓位/弢?- model: glm
  divergence: 直接给出仓位加减?10%/-10%）与多图输出清单
  why_it_matters: 触碰执行建议且产物要求偏离当前项目最小合约（我们先要 CSV/可复现证据，不先做图?  repo_action: 仅保留其“不要硬过滤、先?MAE/交叉”的证据思路；拒绝仓位改动与图产物清?  reject_if: 任何执行侧建?自动化执?- model: 千问
  divergence: 倾向?entry_session 直接判为 ENTRY_FILTER/ADD
  why_it_matters: 当前 pooled 下各 session avg_pnl 均为负；且分?frac_both?.453 仍是边界值，不足以直接晋升过?  repo_action: 维持 DIAG_ONLY / ADD_CANDIDATE，不晋升 ENTRY_FILTER
  reject_if: ?- model: 豆包
  divergence: 倾向“ENTRY_FILTER 辅助加权/权重调整?  why_it_matters: 权重属于执行侧决策；在未给出 per-symbol 稳定性与 MAE 前不落地
  repo_action: 先把 session 定为 DIAG_ONLY/London ADD_CANDIDATE；后续若补证据显示稳定增量再讨论权重
  reject_if: 任何执行侧直接改仓位/脚本

==============================
BATCH_CLOSE（批?0；以证据拍板?==============================
- 证据（scope=all；split=since2022）：
  - `backtest_out\stage2\indicator_audit\20260605_b10_evidence_all_v1\b10_feature_summary_20260605_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260605_b10_evidence_all_v1\b10_bucket_agg_20260605_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260605_b10_evidence_all_v1\b10_london_vs_all_summary_20260605_v1.csv`
- 裁决（研究侧 v0；默认不接入执行门控）：
  - entry_session：DIAG_ONLY（当?pooled 下各 session avg_pnl 均为负，先不讨论“硬过滤/只做某时段）
  - London：ADD_CANDIDATE（边界；仅做“相对加?优先解释”，不做 London-only?  - Asia：DIAG_ONLY（avg_pnl 更接?0 ?stop_loss_rate 更高、持仓更久，trade-off 强）
  - NY：DIAG_ONLY（avg_pnl 朢差但 stop_loss_rate 朢低tp2_rate 朢高，trade-off 强；不在?MAE 情况下贴 RISK?- 下一步最小证据动作（若未来要晋升/落阈值才做；否则不再投入）：
  - per-symbol：London vs All、NY vs non-NY 的方向一致（?symbol×profile；单?n>=20?  - 交叉：session×vol_state?×3；看 London 是否只是 NORMAL 的代理）
  - 风险口径：trade_mae_atr ?entry_session 分组（用于判?NY/Asia 的更痛苦”是否成立）

==============================
PANEL_VOTE_TSV（批?1；DIAG_TOP_DEDUP?==============================
batch_id	q1_focus_diags	q2_role_map_summary	q3_next_evidence_actions
20260605_v41	diag_session_skew_ratio;diag_session_pnl_london;diag_entry_n;diag_ema144_regime_long_frac;diag_ema_stack_bull_frac;diag_session_entry_vol_ratio_london_n;diag_session_count_london;diag_session_trades_london	多数：本批以“去重为主（不改批次30/32既有 role）；skew_ratio 仍是朢强的 REDUCE_CANDIDATE；pnl_london/entry_n 维持 DIAG_ONLY；去重：DEPRECATE ema_stack_bull_frac；London 计数三件套只保留 entry_vol_ratio_london_n	补证据：London 计数三件套在 p0_sweep_summary 上做 spearman 相关性；若近?1.0 则去重生效；若要“诊断→门控”需补交易级 entry-time 证据

==============================
DIFF_NOTES（批?1?==============================
- model: kimi
  divergence: ?ema144_regime_long_frac 定为 ADD（非 DIAG_ONLY），并建议保?diag_session_entry_vol_ratio_london_n 作为 London 计数三件套代?  why_it_matters: ema144_regime 作为“趋势环境可用于解释/分层，但在当?diag 口径下仍属于后视画像；London 三件套确实高度同构，保留语义更丰富更合理
  repo_action: ema144_regime_long_frac 仍按 DIAG_ONLY 收口；保?entry_vol_ratio_london_n、弃?count/trades；并把同构证据（spearman?）落?  reject_if: ?- model: deepseek
  divergence: 倾向?diag_session_pnl_london 判为 REDUCE_CANDIDATE，且三件套保?trades_london
  why_it_matters: pnl_london 属于后视画像，用作门控有前视偏差风险；三件套保留哪个主要是语?信息量权?  repo_action: pnl_london 固定 DIAG_ONLY；三件套保留 entry_vol_ratio_london_n（更贴近“量?时段暴露”），弃?count/trades
  reject_if: ?- model: glm
  divergence: ?diag_entry_n 判为 RISK_ONLY，并?pnl_london 判为 REDUCE_CANDIDATE
  why_it_matters: entry_n 更像“结?症状”（过度交易画像），不宜直接贴风险门控；pnl_london 同样后视
  repo_action: entry_n 固定 DIAG_ONLY；pnl_london 固定 DIAG_ONLY；强调诊断→门控”必须补交易级证?  reject_if: ?- model: 千问
  divergence: ?ema144_regime ?ema_stack 的去重结论摇摆（两都?DEPRECATE 且要求互为证据）
  why_it_matters: ?corr spearman=1.0 的硬证据冲突
  repo_action: 直接?corr 证据去重：保?ema144_regime_long_frac，DEPRECATE ema_stack_bull_frac
  reject_if: ?- model: 豆包
  divergence: ?diag_session_skew_ratio 判为 RISK_ONLY（且方向表述为高值更优）
  why_it_matters: skew_ratio 的高/低语义需回到定义；但不影响结论：它是朢强的“坏档预警?  repo_action: 统一?REDUCE_CANDIDATE 收口（避免直接当门控/风控弢关），并把方向在后续交易级证据里再钉?  reject_if: ?
==============================
BATCH_CLOSE（批?1；以证据拍板?==============================
- 证据（scope=all；split=since2022）：
  - `backtest_out\stage2\indicator_audit\diag_rank_20260605_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260605_diag_followups_v2\diag_followups_feature_summary_20260605_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260605_diag_followups_v2\diag_followups_corr_20260605_v1.csv`
  - 同构补证据（p0_sweep_summary；spearman）：diag_session_entry_vol_ratio_london_n vs diag_session_count_london?.99961；diag_session_count_london vs diag_session_trades_london=1.0
- 裁决（研究侧 v0；默认不接入执行门控）：
  - diag_session_skew_ratio：REDUCE_CANDIDATE（优先级朢高；rank spearman_net_pnl?.7802 ?top_dd_ok_minus_bot?.5227?  - diag_session_pnl_london：DIAG_ONLY（后视画像；禁止当入场门控）
  - diag_entry_n：DIAG_ONLY（滞?症状；用?sanity-check?  - diag_ema144_regime_long_frac：维持批?2裁决（ADD/REDUCE 候；本批只做去重，不重新定）
  - 去重（v0）：
    - DEPRECATE：diag_ema_stack_bull_frac（与 diag_ema144_regime_long_frac corr spearman=1.0?    - 保留：diag_session_entry_vol_ratio_london_n（代表字段；?count/trades spearman?.0?    - DEPRECATE：diag_session_count_london / diag_session_trades_london（同构）
- 下一步最小证据动作（只有当要“诊断→门控/权重”才做）?  - 交易级：把?diag 的entry-time 状落?trades_baseline，做逐笔分桶（避?profile 画像的前视风险）

### 2026-06-05 批次42复审/增补（B20_VOL_ATR：补?e1_atr_ratio + 修正 v0?
说明?- 批次33已对 B20 做过全品种收口；批次42不新增证据文件，只基于相同证据做“补?+ 纠偏”（?e1_atr_ratio 纳入；并按稳定?覆盖率重新约束角色）?
证据（scope=all；split=since2022；与批次33丢致）?- `backtest_out\stage2\indicator_audit\20260604_b20_evidence_all_v1\b20_feature_summary_20260604_v1.csv`
- `backtest_out\stage2\indicator_audit\20260604_b20_evidence_all_v1\b20_bucket_stats_20260604_v1.csv`
- `backtest_out\stage2\indicator_audit\20260604_b20_followups_all_v1\b20_stability_summary_20260604_v1.csv`
- `backtest_out\stage2\indicator_audit\20260604_b20_followups_all_v1\b20_entry_vol_ratio_coverage_20260604_v1.csv`

==============================
PANEL_VOTE_TSV（批?2；B20_VOL_ATR?==============================
model	q1_role_map_summary	q2_entry_vol_ratio_policy	contract_ok	notes
kimi	atr=ADD；break_strength=REDUCE_CANDIDATE；e1_atr_ratio=DIAG_ONLY；retest_depth=DIAG_ONLY；entry_vol_ratio=DIAG_ONLY(条件保留)	coverage>=30% ?eligible；其?insufficient_coverage	ok	强调 retest_depth n_sufficient=3；entry_vol_ratio 覆盖率硬约束
deepseek	break_strength=ENTRY_FILTER；atr=RISK_ONLY；retest_depth=DIAG_ONLY；e1_atr_ratio=DIAG_ONLY；entry_vol_ratio=DIAG_ONLY+限定profile	只在 coverage 高的子集讨论；缺失不?	ok	?atr “高波动更危险作为前提，但与 stop_loss_better 的证据需再对?glm	atr=RISK_ONLY(甜点?；break_strength=ADD；e1_atr_ratio=DIAG_ONLY；retest_depth=DIAG_ONLY；entry_vol_ratio=DIAG_ONLY(条件保留)	建议缺失桶（Missing vs Present）对?partial	夹带执行侧措辞（仓位/止损）→ 本项目只保留证据动作
千问	多数=ADD/DIAG_ONLY（泛化）	认可 entry_vol_ratio ?DIAG_ONLY，且 NEED_EVIDENCE: MAE/max_dd	ok	合约偏泛，价值在“补风险口径?豆包	break_strength=ENTRY_FILTER；atr=RISK_ONLY；e1_atr_ratio=ENTRY_FILTER；retest_depth=DIAG_ONLY；entry_vol_ratio=DIAG_ONLY	coverage>=30% 子集验证；并?NEED_EVIDENCE: MAE/max_dd	ok	把稳定不足字段晋升为 ENTRY_FILTER（与 n_sufficient/frac_both 证据冲突?
==============================
DIFF_NOTES（批?2?==============================
- model: kimi
  divergence: ?atr 从风险标签改判为 ADD（强调稳定?frac_both?.526 ?stop_loss 同向改善?  why_it_matters: atr ?top/bot 方向在现有口径下是高桶更好，但这不等价于“风险更小；若要把它当门?加分，必须补 MAE/回撤口径避免“更赚但更痛苦?  repo_action: 维持 atr=RISK_ONLY（沿用批?3的风险环境标签定位），并新增 NEED_EVIDENCE: trade_mae_atr / max_drawdown_per_trade 用于明确风险形?  reject_if: ?- model: deepseek / 豆包
  divergence: 倾向?break_strength / e1_atr_ratio 直接晋升 ENTRY_FILTER
  why_it_matters: 两的分层丢致不足（break_strength frac_both?.333；atr_ratio frac_both?.365），不满足先标签后晋升的门槛
  repo_action: 维持 break_strength=ADD_CANDIDATE、atr_ratio=DIAG_ONLY；禁止直接晋升硬门控
  reject_if: 仅凭 pooled top_minus_bot 下硬阈?
==============================
BATCH_CLOSE（批?2；B20_VOL_ATR v0 更新点）
==============================
- 不新增证据文件；只做补项/纠偏（相对批?3）：
  - 新增纳入：e1_atr_ratio（补?v0 角色?  - 修正：e1_retest_depth_atr ?v0 角色（按样本有效性收紧）
- v0 ROLE MAP（研究侧标记；默认不接入执行门控）：
  - atr：RISK_ONLY（以 qtiles4 为主；风险环境标签；方向不直接等同高更危?低更安全”，霢 MAE/回撤口径定）
  - e1_break_strength_atr：ADD_CANDIDATE（quality_score；q4_bin4 加分、q4_bin1 减分；分?frac_both?.333 ?不做 ENTRY_FILTER?  - e1_atr_ratio：DIAG_ONLY（分?frac_both?.365 ?不晋?gate；仅解释/分层?  - e1_retest_depth_atr：DIAG_ONLY（n_sufficient=3 ?冻结，不落阈值）
  - entry_vol_ratio：DIAG_ONLY（条件变量；coverage 达标前不晋升 gate?- entry_vol_ratio 使用口径（v0）：
  - 仅对 coverage>=0.30 ?symbol×profile 标记?vol_ratio_eligible；其余标?insufficient_coverage
  - 缺失值不?0；缺失本身可作为“Missing 桶做对照诊断（不做过滤）
- 下一步最小证据动作（只有当要晋升/落阈值才做）?  - NEED_EVIDENCE（风险口径）：trade_mae_atr / max_drawdown_per_trade（用于判?atr/break_strength 是否“更赚但更痛苦）

### 2026-06-05 批次43收口（B99_OTHER：stop_k / stop_dist_atr / risk_per_trade；全品种?
证据（scope=all；split=since2022）：
- `backtest_out\stage2\indicator_audit\20260605_b99_evidence_all_v1\b99_feature_summary_20260605_v1.csv`
- `backtest_out\stage2\indicator_audit\20260605_b99_evidence_all_v1\b99_bucket_stats_20260605_v1.csv`
- `backtest_out\stage2\indicator_audit\20260605_b99_followups_all_v1\b99_followups_feature_summary_20260605_v1.csv`
- `backtest_out\stage2\indicator_audit\20260605_b99_followups_all_v1\b99_followups_stop_atr_pairs_20260605_v1.csv`
- `backtest_out\stage2\indicator_audit\20260605_b99_followups_all_v1\b99_followups_stop_atr_summary_20260605_v1.csv`

==============================
PANEL_VOTE_TSV（批?3；B99_OTHER?==============================
model	q1_role_map_summary	q2_stop_atr_1p5_vs_2p0_summary	contract_ok	notes
kimi	stop_k=DEPRECATE；stop_dist_atr=CONFIG_BUCKET；risk_per_trade=CONFIG_BUCKET	1.5 vs 2.0：稳定弱（frac_both?.281?ok	同构判断合理；但?stop_loss 方向有误读风险（霢?pairs ?delta 为准?deepseek	stop_dist_atr=CONFIG_BUCKET；stop_k=DIAG_ONLY；risk_per_trade=DIAG_ONLY	同意不做默认推荐；建议分层重?ok	接受“参数不是信号?glm	stop_dist_atr/stop_k=CONFIG_BUCKET；risk_per_trade=DIAG_ONLY	同意不做默认推荐；建议补 MAE	partial	夹带执行侧措辞（止损/仓位）→ 本项目只保留证据动作
千问	stop_dist_atr=CONFIG_BUCKET；risk_per_trade=DIAG_ONLY；stop_k=RISK_ONLY	同意霢?MAE/max_dd 才能推荐	ok	?stop_k 判为 RISK_ONLY 与同构证据冲?豆包	raw stop=DEPRECATE；stop_dist_atr=CONFIG_BUCKET；risk_per_trade=RISK_ONLY	建议多档位扫描甜点区	ok	?risk_per_trade 判为 RISK_ONLY 缺乏分层稳定性证?
==============================
DIFF_NOTES（批?3?==============================
- model: kimi
  divergence: ?stop_k 明确判为?stop_dist_atr 同构并建?DEPRECATE
  why_it_matters: b99_feature_summary ?top_minus_bot 完全相同?921.80），?followups ?stop_dist_atr 复现同??重复字段会撑爆后续对?  repo_action: v0 统一只保?stop_dist_atr，stop_k 记为别名/DEPRECATE
  reject_if: ?- model: 千问
  divergence: ?stop_k 判为 RISK_ONLY
  why_it_matters: 与同构证据冲突（stop_k≡stop_dist_atr），?1.5 vs 2.0 的分层稳定不足以做风险门?  repo_action: 拒绝该定性；改为 DEPRECATE
  reject_if: ?- model: 豆包
  divergence: ?risk_per_trade 判为 RISK_ONLY
  why_it_matters: risk_per_trade 更像派生校验字段；未给出稳定?正交性证据，不应晋升
  repo_action: 固定 risk_per_trade=DIAG_ONLY（审?核对用），不做门?  reject_if: ?
==============================
BATCH_CLOSE（批?3；以证据拍板?==============================
- 关键事实?  - stop_k ?stop_dist_atr ?pooled ?top_minus_bot_avg_pnl 完全相同（均?921.80）→ 视为同构/别名
  - stop_atr=1.5 vs 2.0（symbol×profile pairs；n_pairs=32）：
    - 1.5 相对更好：frac_pnl_better=0.5000；frac_stop_loss_better=0.3125；frac_both=0.2813
    - 2.0 相对更好（由 pairs ?delta 推回）：pnl 更好占比=0.5000；stop_loss 更好占比=0.6875；pnl+stop_loss 同时更好占比=0.4688
  - 结论：两档位不存在同向碾压的稳定优势（pnl 对半；且 only 32 pairs?- v0 ROLE MAP（研究侧标记；默认不接入执行门控）：
  - stop_dist_atr：CONFIG_BUCKET（止损率配置档；允许在品?环境下做对照，但不做全局默认推荐?  - stop_k：DEPRECATE（统丢?stop_dist_atr 命名?  - risk_per_trade：DIAG_ONLY（审?核对用；不作为门?评分?- 下一步最小证据动作（只有当要讨论“推荐档?甜点区才做）?  - NEED_EVIDENCE：trade_mae_atr / max_drawdown_per_trade（区分?.0 只是扛更久更痛苦?vs ?.0 减少噪音止损且风险可控）

### 2026-06-06 批次44收口（B60_SWING_LEVELS + BOOL 字段；全品种?
证据（scope=all；split=since2022）：
- `backtest_out\stage2\indicator_audit\20260606_b60_evidence_all_v3\b60_feature_summary_20260606_v1.csv`
- `backtest_out\stage2\indicator_audit\20260606_b60_evidence_all_v3\b60_bucket_stats_20260606_v1.csv`
- `backtest_out\stage2\indicator_audit\20260606_b60_followups_all_v3\b60_stability_summary_20260606_v1.csv`

==============================
PANEL_VOTE_TSV（批?4；B60_SWING_LEVELS?==============================
model	q1_role_map_summary	q2_swing_invest_summary	contract_ok	notes
kimi	sv_risk_on_mkt=ADD; sv_use_struct_vote=ADD; swing_high/low=DIAG_ONLY	建议?swing_* ?binary 朢后一试，不达标则 DEPRECATE	ok	?risk_on 归为“环境标签较合理；但“risk_on=1 更好”需在最终口径里避免前视/不可实时?deepseek	sv_risk_on_mkt=RISK_ONLY; sv_use_struct_vote=ENTRY_FILTER; swing_*=DIAG_ONLY	同意 swing_* binary + 扩窗口；不达标则 DEPRECATE	ok	?risk_on=1 解读为风险更高与当前证据（stop_loss_better 高）冲突
glm	sv_risk_on_mkt=RISK_ONLY; sv_use_struct_vote=ENTRY_FILTER; swing_*=DIAG_ONLY	建议 swing 覆盖率报?+ binary 棢?partial	夹带执行侧措辞（仓位/止损），仅采纳证据动?千问	sv_risk_on_mkt=RISK_ONLY; sv_use_struct_vote=ENTRY_FILTER; swing_*=DIAG_ONLY	建议扩窗?binary；可?MAE/max_dd	ok	总体可用，但?use_struct_vote 直接?ENTRY_FILTER 风险较大（门槛不足）
豆包	sv_risk_on_mkt=RISK_ONLY(口径混乱); sv_use_struct_vote=ENTRY_FILTER辅助; swing_*=DIAG_ONLY	同意 binary + 扩窗口；不达标则 DEPRECATE	ok	?risk_on 的方向自相矛盾（?code=0 更优但又?code=1 风险预警?
==============================
DIFF_NOTES（批?4?==============================
- model: kimi
  divergence: ?sv_risk_on_mkt 定位?ADD（非 RISK_ONLY），并强调其稳定性（frac_both=0.50?  why_it_matters: sv_risk_on_mkt 的分层一致显著高?swing_*，是本批唯一可能晋升为用环境标签”的字段；但其是否可实时获取决定能否用于 entry-time
  repo_action: v0 先落?RISK_ONLY（环境标签），并追加 NEED_EVIDENCE（数据源实时?延迟）决定是否允许做 entry-time 加减?  reject_if: ?- model: deepseek
  divergence: ?sv_use_struct_vote 直接判为 ENTRY_FILTER
  why_it_matters: frac_both?.469（接近但未达到硬门控”门槛），直接晋?ENTRY_FILTER 可能引发过拟合与误杀
  repo_action: v0 固定?ADD_CANDIDATE（结构确认加分），并要求先做正交性（use_struct_vote×sv_regime_code / ×sv_risk_on_mkt）再讨论晋升
  reject_if: ?- model: glm
  divergence: 强调 swing_* 可能是缺失本身有信息”，建议?Null vs Non-Null 的二值桶
  why_it_matters: swing_* ?n_sufficient 仍偏低，pooled 可能被少数品种主导；把是否有摆动点作为特征可提升样本并减少重绘口径争?  repo_action: 追加证据动作：swing_present(flag) ?binary 分桶 + 覆盖率报告；达不到阈值则 DEPRECATE swing_*（保留字段不再研究）
  reject_if: ?
==============================
BATCH_CLOSE（批?4；以证据拍板?==============================
- 关键事实（symbol×A_all；min_n=10）：
  - sv_risk_on_mkt(code)：n_sufficient=32；frac_stop_loss_better?.719；frac_both?.500（四者最稳）
  - sv_use_struct_vote(code)：n_sufficient=32；frac_both?.469（接近门槛）
  - swing_high/low：n_sufficient?4/11；frac_both?.357/0.364（仍偏低?- v0 ROLE MAP（研究侧标记；默认不接入执行门控）：
  - sv_risk_on_mkt：RISK_ONLY（风险环境标签；优先解释/分层；是否允?entry-time 加减分取决于数据源实时）
  - sv_use_struct_vote：ADD_CANDIDATE（结构确认加分；不晋?ENTRY_FILTER?  - sv_swing_high_4h：DIAG_ONLY（冻结；样本仍不足）
  - sv_swing_low_4h：DIAG_ONLY（冻结；样本仍不足）
- 下一步最小证据动作（只做丢次最后一试，不过则停止投入）?  - swing_present(flag)：Null vs Non-Null 二桶（验证有摆动点本身是否有信息?  - split 扩展?pre2022/full 或放宽单 symbol 门槛（只用于提升 n_sufficient，不用于晋升 gate?  - 解冻/继续投入阈：n_sufficient>=15 ?frac_both>=0.30；否则将 swing_* 加入 DEPRECATE_LIST（字段保留但不再研究?  - NEED_EVIDENCE：trade_mae_atr / max_drawdown_per_trade（若要讨论摆动极值是否更痛苦/更易回撤”）

### 2026-06-07 批次44补证据（B60 swing_present 二桶；全品种?
- COMMAND（scope=all；split=since2022）：
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b60-evidence --date 20260607 --scope all --split since2022 --q 4 --out_dir .\backtest_out\stage2\indicator_audit\20260607_b60_evidence_all_v4`
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b60-followups --date 20260607 --scope all --split since2022 --min-n 15 --profile-merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b60_evidence_all_v4\b60_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b60_followups_all_v4`
- OUTPUT?  - `backtest_out\stage2\indicator_audit\20260607_b60_evidence_all_v4\b60_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b60_evidence_all_v4\b60_feature_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b60_followups_all_v4\b60_stability_summary_20260607_v1.csv`
- 快摘录（stability_summary；symbol×A_all；min_n=15）：
  - sv_swing_present_4h(code)：n_pairs=32；n_sufficient=32；frac_pnl_better=0.5625；frac_stop_loss_better=0.8750；frac_both=0.5313
- 补证据裁决（批次44 v0.1）：
  - swing_present(flag) 通过“最后一试的继续投入阈（n_sufficient>=15 ?frac_both>=0.30?  - sv_swing_high_4h / sv_swing_low_4h：解?PENDING_DEPRECATE，仍保持 DIAG_ONLY（冻结；不晋?gate；后续只讨论是否?swing_present 作为更稳的降维替代）

- 组合验证补充（combo_v0 v3；仅作研究侧参，不改执行默认）：
  - OUTPUT：`backtest_out\stage2\indicator_audit\20260607_combo_v0_all_v3\combo_v0_bucket_stats_20260607_v1.csv`
  - pooled 加权对照（只?swing_present=0/1；按 n_trades 加权）：
    - swing_present=0：avg_pnl_w?36.75；stop_loss_rate_w?.2403（n?4112?    - swing_present=1：avg_pnl_w?18.26；stop_loss_rate_w?.1879（n?374?
### 2026-06-07 追加证据（B60 swing_present × risk_on × regime 交互分层；全品种?
- COMMAND（scope=all；split=since2022；profile 合并 A_all；min_n=20）：
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b60-swing-present-interaction --date 20260607 --scope all --split since2022 --min-n 20 --profile-merge 1 --out_dir .\backtest_out\stage2\indicator_audit\20260607_b60_swing_present_interaction_all_v3`
- OUTPUT?  - `backtest_out\stage2\indicator_audit\20260607_b60_swing_present_interaction_all_v3\b60_swing_present_interaction_pairs_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b60_swing_present_interaction_all_v3\b60_swing_present_interaction_summary_20260607_v1.csv`
- 快摘录（summary；sufficient pairs 统计）：
  - risk=1 & regime!=0：n_sufficient=104；frac_both?.567
  - risk=0 & regime=0：n_sufficient=89；frac_both?.393
  - overall(sufficient_only)：n_sufficient=193；frac_both?.487

### 2026-06-07 批次45收口（B60 swing_present + 交互分层；全品种?
证据（scope=all；split=since2022）：
- `backtest_out\stage2\indicator_audit\20260607_b60_followups_all_v4\b60_stability_summary_20260607_v1.csv`
- `backtest_out\stage2\indicator_audit\20260607_b60_swing_present_interaction_all_v3\b60_swing_present_interaction_summary_20260607_v1.csv`
- `backtest_out\stage2\indicator_audit\20260607_combo_v0_all_v3\combo_v0_bucket_stats_20260607_v1.csv`
- 零前?重绘验证（prefix vs full；entry_time 抽样丢致）?  - `backtest_out\stage2\indicator_audit\20260607_b60_swing_lookahead_audit_all_v1\b60_swing_lookahead_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b60_swing_lookahead_audit_all_v1\b60_swing_lookahead_samples_20260607_v1.csv`
- pre2022 稳健性对照（scope=all；split=pre2022）：
  - `backtest_out\stage2\indicator_audit\20260607_b60_followups_pre2022_v1\b60_stability_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b60_swing_present_interaction_pre2022_v1\b60_swing_present_interaction_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_combo_v0_pre2022_v1\combo_v0_bucket_stats_20260607_v1.csv`
- trade_mae_atr / max_drawdown_per_trade（以 1H high/low 计算持仓期最大不利波动；ATR 归一化）?  - since2022：`backtest_out\stage2\indicator_audit\20260607_b60_swing_present_mae_all_v2\b60_swing_present_mae_summary_20260607_v1.csv`
  - pre2022：`backtest_out\stage2\indicator_audit\20260607_b60_swing_present_mae_pre2022_v2\b60_swing_present_mae_summary_20260607_v1.csv`

COMMAND（可复现）：
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b60-evidence --date 20260607 --scope all --split pre2022 --q 4 --out_dir .\backtest_out\stage2\indicator_audit\20260607_b60_evidence_pre2022_v1` + `b60-followups --min-n 15 --profile-merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b60_evidence_pre2022_v1\b60_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b60_followups_pre2022_v1` + `b60-swing-present-interaction --min-n 20 --profile-merge 1 --out_dir .\backtest_out\stage2\indicator_audit\20260607_b60_swing_present_interaction_pre2022_v1` + `combo-v0 --out_dir .\backtest_out\stage2\indicator_audit\20260607_combo_v0_pre2022_v1`
- MAE since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b60-swing-present-mae --date 20260607 --scope all --split since2022 --min_n 20 --profile-merge 1 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b60_swing_present_mae_all_v2`
- MAE pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b60-swing-present-mae --date 20260607 --scope all --split pre2022 --min_n 20 --profile-merge 1 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b60_swing_present_mae_pre2022_v2`

==============================
PANEL_VOTE_TSV（批?5；B60 swing_present?==============================
model	q1_role_map_summary	q2_interaction_ruling	q3_need_evidence	contract_ok	notes
kimi	sv_swing_present_4h=ADD（条件型；全屢 frac_both=0.5313；risk=1&regime!=0 增强?0.5673；risk=0&regime=0 逢化为 DIAG_ONLY?存在显著环境依赖；允许条件型 ADD（研究侧标签）；reject_if 包含 pre2022/共线/前视	霢?pre2022 稳健?+ 零前视验?+ trade_mae_atr	ok	强调“binary 降维”是质变；反对直?ENTRY_FILTER
deepseek	sv_swing_present_4h=ADD_CANDIDATE（不晋升强过滤）	同意仅在 risk=1&regime!=0 作为弱过?加分；risk=0&regime=0 禁用	ok	同样要求 pre2022/MAE/实时?partial	语气带优先入?加仓”，只采纳为研究侧标?glm	sv_swing_present_4h=RISK_ONLY（偏风控标签?同意条件性风险分层标签；强调震荡/低风险环境失?ok	要求 pre2022 + 重绘/前视排查 + 组合边际贡献	partial	夹带执行侧仓?止损”，仅采纳证据动作与 reject_if
千问	sv_swing_present_4h=RISK_ONLY（体?同意仅在 risk=1&regime!=0 使用；其它环境禁?ok	要求 MAE/max_dd + pre2022/full + 实时?ok	较保守；不支持直接过?豆包	sv_swing_present_4h=ENTRY_FILTER_CANDIDATE（弱过滤?同意 risk=1&regime!=0 下用作弱过滤；其它环境禁?ok	要求 pre2022 + 组合叠加效果 + 无前?ok	倾向“只保留 swing_present=1”，风险较大

==============================
DIFF_NOTES（批?5?==============================
- model: 豆包
  divergence: ?sv_swing_present_4h 直接判为 ENTRY_FILTER_CANDIDATE，并建议?risk=1&regime!=0 “仅保留 swing_present=1?  why_it_matters: pooled 加权?swing_present=1 仍为负（avg_pnl_w?18.26），且过滤将砍掉?60% trades（swing_present=0）→ 若存在前?共线/窗口漂移，会引发误杀与过拟合
  repo_action: v0.2 固定为条件型 ADD 标签”（研究侧），不做过滤；仅保?reject_if ?NEED_EVIDENCE 作为晋升前置条件
  reject_if: ?- model: glm/千问
  divergence: ?sv_swing_present_4h 归为 RISK_ONLY（非 ADD?  why_it_matters: 该字段同时在 avg_pnl ?stop_loss 上表现同向（frac_both>0.5；且 risk=1&regime!=0 frac_both?.567），更像“质?结构确认”非纯风险标?  repo_action: v0.2 定义?ADD（条件型）；低效环境（risk=0&regime=0）明确化为 DIAG_ONLY
  reject_if: ?- 共识缺口（所有模型一致强调）
  divergence: 是否存在前视/重绘（zigzag/swing 类常见）
  why_it_matters: ?swing_present ?entry_time 仍不确定，则任何“过?加分”都会在实盘失真
  repo_action: 固定 NEED_EVIDENCE：零前视验证；未通过前仅允许 DIAG_ONLY
  reject_if: ?
==============================
BATCH_CLOSE（批?5；以证据拍板?==============================
- 关键事实（symbol×A_all；min_n=15 / 20）：
  - swing_present 全局：n_sufficient=32；frac_stop_loss_better?.875；frac_both?.531
  - 交互分层（sufficient_only）：risk=1&regime!=0 frac_both?.567；risk=0&regime=0 frac_both?.393；overall?.487
  - pooled 加权（combo_v0）：swing_present=1 ?avg_pnl_w?18.26 好于 0 ?-36.75，且 stop_loss_rate_w?.1879 低于 0 ?0.2403
  - pre2022 稳健性（symbol×A_all）：
    - swing_present 全局：n_sufficient=28；frac_both?.464
    - 交互分层（sufficient_only）：risk=1&regime!=0 frac_both?.485；risk=0&regime=0 frac_both?.353；overall?.44
  - MAE/朢大不利波动（risk=1&regime!=0；symbol×A_all；min_n=20）：
    - since2022：median(Δmae_atr_mean)= -0.147；mean(Δmae_atr_mean)= -0.137（swing_present=1 更不痛苦?    - pre2022：median(Δmae_atr_mean)= -0.082；mean(Δmae_atr_mean)= -0.082（仍更不痛苦，但弱于 since2022?- v0.2 ROLE MAP（研究侧标记；默认不接入执行门控）：
  - sv_swing_present_4h：ADD_CANDIDATE（条件型；仅?risk=1&regime!=0 时作为加?结构确认标签”，其它环境 DIAG_ONLY；不?ENTRY_FILTER?  - sv_swing_high_4h / sv_swing_low_4h：DIAG_ONLY（冻结；数桶不再投入；以 swing_present 降维替代?- reject_if（未通过则全部?DIAG_ONLY，不讨论过滤/加分）：
  - PASSED：零前视/重绘排查（prefix vs full；since2022；scope=all；samples_per_symbol=30）：total_sampled=960；total_mismatch=0
  - PARTIAL_PASSED：pre2022 稳健性对照（存在逢化但未崩；保持同向；维持“条件型 ADD”，不晋升过滤）
  - PASSED：trade_mae_atr / max_drawdown_per_trade（以 MAE_ATR 代理朢大不利波动；risk=1&regime!=0 子环?Δmae_atr_mean < 0?
### 2026-06-07 批次46收口（资料型指标→字段落地：ALBrooks 信号棒质量评?v0；全品种?
证据（scope=all；doji_body_ratio=0.05）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260607_b46_signalbar_since2022_v1\b46_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b46_followups_since2022_v1\b46_stability_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b46_signalbar_since2022_v1\b46_spearman_corr_20260607_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260607_b46_signalbar_pre2022_v1\b46_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b46_followups_pre2022_v1\b46_stability_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b46_signalbar_pre2022_v1\b46_spearman_corr_20260607_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b46-signalbar-evidence --date 20260607 --scope all --split since2022 --doji_body_ratio 0.05 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b46_signalbar_since2022_v1` + `b46-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b46_signalbar_since2022_v1\b46_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b46_followups_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b46-signalbar-evidence --date 20260607 --scope all --split pre2022 --doji_body_ratio 0.05 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b46_signalbar_pre2022_v1` + `b46-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b46_signalbar_pre2022_v1\b46_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b46_followups_pre2022_v1`

==============================
PANEL_VOTE_TSV（批?6；ALBrooks 信号棒评?v0?==============================
model	q1_feature_spec_summary	q2_role_map	q3_min_validation_actions	contract_ok	notes
kimi	建议 v0 只做 entry bar 几何字段 + score + bucket（doji<0.05；bucket 4档）	ADD_CANDIDATE；great=ADD(+1)；bad=REDUCE_CANDIDATE（不?ENTRY_FILTER?同构棢测→pooled→symbol×A_all 稳定?ok	强调“背?同色棒先不做以避免前?共线
deepseek	v0 ?5 个原子字?+ score + bucket（doji<0.1 建议?ADD_CANDIDATE；不建议 bad<3 直接过滤	pooled→稳定→同构棢?ok	倾向只加分标?glm	v0 原子字段+score+bucket；建议后续拼?regime ?adjusted_score	ADD_CANDIDATE（弱/条件）；bad 倾向强减?拒绝	同构→pooled→抽样人工核?partial	含执行侧表述，仅采纳字段/验证动作
千问	字段表完整；doji 阈建议更宽（0.2?DIAG_ONLY（更保守?pooled→稳定→同构棢?ok	偏谨?豆包	字段/阈建议混杂；bucket 划分不同（bad<0 等）	DIAG_ONLY（先研究?同构→pooled→稳定?ok	阈与分桶不一致，霢以证据重?
==============================
DIFF_NOTES（批?6?==============================
- divergence: doji 阈（0.05 vs 0.1 vs 0.2）与 bucket 划分?~3 vs 其它?  repo_action: v0 固定 doji_body_ratio=0.05（可命令行切换），bucket 采用 bad<3/ok3-4/good5-7/great>=8?~3?  why_it_matters: 阈会改变 bucket 分布与样本量，从而影响稳定；必须用全品种证据裁决
- divergence: 是否允许 bad 桶做过滤/减仓
  repo_action: v0 不做过滤，只保留 DIAG/候标签；是否减仓霢要在“稳定?+ MAE/max_dd”过后再讨论
  why_it_matters: 单K线几何字段易受周?环境影响，直接过滤风险大

==============================
BATCH_CLOSE（批?6；以证据拍板?==============================
- 数据规模：since2022 pooled n?3657（coverage ?100%）；pre2022 pooled n?3394
- 稳定性（symbol×A_all；min_n=20）：
  - since2022：bucket(code4) frac_both?.438；score(qtiles4) frac_both?.263
  - pre2022：bucket(code4) frac_both?.259；score(qtiles4) frac_both?.263
- 同构（spearman；pooled）：
  - vs trade_pnl：≈0（since2022=-0.017；pre2022=-0.002?  - vs entry_score：弱相关（since2022=-0.117；pre2022=-0.087?  - vs e1_break_strength_atr：弱相关（since2022=-0.150；pre2022=-0.146?- v0 ROLE MAP?  - ab_sig_quality_score_1h：DIAG_ONLY（qtiles4 稳定性不足）
  - ab_sig_quality_bucket_1h：DIAG_ONLY（存?tradeoff：交互分层下 stop_loss_rate 更好，但 MAE_ATR 明显更差；不支持“加?过滤”晋升）
- 追加证据（交互分层；bucket<=1 vs bucket>=2；symbol×A_all；min_n=20）：
  - since2022：`backtest_out\stage2\indicator_audit\20260607_b46_signalbar_interaction_since2022_v1\b46_signalbar_interaction_summary_20260607_v1.csv`
    - risk=0 & regime=0：n_sufficient=53；frac_both?.472
    - risk=1 & regime!=0：n_sufficient=101；frac_both?.317
    - overall(sufficient_only)：n_sufficient=154；frac_both?.370
  - pre2022：`backtest_out\stage2\indicator_audit\20260607_b46_signalbar_interaction_pre2022_v1\b46_signalbar_interaction_summary_20260607_v1.csv`
    - risk=0 & regime=0：n_sufficient=21；frac_both?.476
    - risk=1 & regime!=0：n_sufficient=71；frac_both?.408
    - overall(sufficient_only)：n_sufficient=92；frac_both?.424
- v0.1 使用口径（研究侧；不接执行门控）?  - label: ab_sig_quality_bucket_1h>=2 视为“质量加分标签（bucket<=1 视为普?偏弱?  - best_env: risk=0 & regime=0（两段历史都更稳?  - reject_if: pre2022 出现方向反转 ?交互分层 n_sufficient 明显崩塌?20?
- 追加证据（MAE_ATR；bucket<=1 vs bucket>=2；symbol×A_all；min_n=20）：
  - since2022：`backtest_out\stage2\indicator_audit\20260607_b46_signalbar_mae_since2022_v1\b46_signalbar_mae_summary_20260607_v1.csv`
    - risk=0 & regime=0：n_sufficient=53；frac_mae_better?.075；median(Δmae_atr_mean)?0.298
    - risk=1 & regime!=0：n_sufficient=101；frac_mae_better?.020
  - pre2022：`backtest_out\stage2\indicator_audit\20260607_b46_signalbar_mae_pre2022_v1\b46_signalbar_mae_summary_20260607_v1.csv`
    - risk=0 & regime=0：n_sufficient=21；frac_mae_better?.190；median(Δmae_atr_mean)?0.389
    - risk=1 & regime!=0：n_sufficient=71；frac_mae_better?.070
  - 结论：bucket>=2 更像“更不容易触发止损，但持仓期朢大不利波动更大（更痛苦）”，因此只保?DIAG 用?
### 2026-06-07 批次47收口（资料型指标→字段落地：ALBrooks 趋势强度量化评分 v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260607_b47_trend_strength_since2022_v1\b47_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b47_trend_strength_since2022_v1\b47_feature_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b47_trend_strength_since2022_v1\b47_spearman_corr_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b47_followups_since2022_v2\b47_stability_summary_20260607_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260607_b47_trend_strength_pre2022_v1\b47_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b47_trend_strength_pre2022_v1\b47_feature_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b47_trend_strength_pre2022_v1\b47_spearman_corr_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b47_followups_pre2022_v2\b47_stability_summary_20260607_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b47-trend-strength-evidence --date 20260607 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b47_trend_strength_since2022_v1` + `b47-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b47_trend_strength_since2022_v1\b47_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b47_followups_since2022_v2`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b47-trend-strength-evidence --date 20260607 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b47_trend_strength_pre2022_v1` + `b47-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b47_trend_strength_pre2022_v1\b47_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b47_followups_pre2022_v2`

==============================
BATCH_CLOSE（批?7；以证据拍板?==============================
- 数据规模：since2022 pooled n?3657（coverage ?100%）；pre2022 pooled n?3394
- 分层稳定性（symbol×A_all；min_n=20）：
  - since2022：bucket(code4) frac_both=0.4375；score(qtiles4) frac_both=0.45
  - pre2022：bucket(code4) frac_both?.370；score(qtiles4) frac_both?.381
  - 注：followups ?bucket 对照采用合并桶（code4<=1 vs code4>=2），以避免极端桶样本不足导致 n_sufficient=0?- 同构/去重风险（spearman；pooled）：
  - vs trade_pnl：≈0（since2022=-0.019；pre2022=-0.028?  - vs entry_score：中等相关（since2022?.356；pre2022?.353?- v0 ROLE MAP?  - ab_trend_strength_score_1h：DIAG_ONLY（可用于复盘/分层，但不支持晋升为加分/过滤?  - ab_trend_strength_bucket_1h：DIAG_ONLY（合并桶后可跑出稳定性，但幅度与稳健性不足以晋升?- 多AI讨论：不霢要（证据已能裁决；若未来要再投入，仅建议先补 MAE/max_dd 再虑“更?更弱”阈值重设）

### 2026-06-07 批次48收口（资料型指标→字段落地：ALBrooks 趋势回调量化规则 v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260607_b48_trend_pullback_since2022_v2\b48_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b48_trend_pullback_since2022_v2\b48_feature_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b48_trend_pullback_since2022_v2\b48_spearman_corr_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b48_followups_since2022_v2\b48_stability_summary_20260607_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260607_b48_trend_pullback_pre2022_v2\b48_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b48_trend_pullback_pre2022_v2\b48_feature_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b48_trend_pullback_pre2022_v2\b48_spearman_corr_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b48_followups_pre2022_v2\b48_stability_summary_20260607_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b48-trend-pullback-evidence --date 20260607 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b48_trend_pullback_since2022_v2` + `b48-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b48_trend_pullback_since2022_v2\b48_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b48_followups_since2022_v2`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b48-trend-pullback-evidence --date 20260607 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b48_trend_pullback_pre2022_v2` + `b48-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b48_trend_pullback_pre2022_v2\b48_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b48_followups_pre2022_v2`

==============================
BATCH_CLOSE（批?8；以证据拍板?==============================
- 数据规模：since2022 pooled n?3657；pre2022 pooled n?3394
- 关键问题：非 0 桶覆盖极低（since2022 合计：time_bucket>=1 仅≈44 笔；depth_bucket>=1 仅≈190 笔），导致分层稳定?n_sufficient 极少（多数特征无法稳定评估）
- 分层稳定性（symbol×A_all；min_n=20；bucket 合并对照 code4<=1 vs code4>=2）：
  - since2022：depth_bucket n_sufficient=2；time_bucket n_sufficient=15；两者方向均为深/久更差（frac_both=0?  - pre2022：depth_bucket n_sufficient=2；time_bucket n_sufficient=10；同样深/久更差（frac_both=0?- v0 ROLE MAP?  - ab_pullback_depth_atr_1h / ab_pullback_depth_bucket_1h：DIAG_ONLY（稀疏；仅用于复盘标记极深回调）
  - ab_pullback_time_bars_1h / ab_pullback_time_bucket_1h：DIAG_ONLY（稀疏；暂不晋升风险/过滤?  - ab_pullback_end_score_1h：DIAG_ONLY（稳定不足）
- 多AI讨论：不霢要（证据已表明稀疏问题是主瓶颈；若未来要再投入，霢先重做回调识别口径以提高?0 覆盖?
### 2026-06-07 批次49收口（资料型指标→字段落地：ALBrooks 交易区间量化判定 v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260607_b49_trading_range_since2022_v1\b49_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b49_trading_range_since2022_v1\b49_feature_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b49_trading_range_since2022_v1\b49_spearman_corr_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b49_followups_since2022_v1\b49_stability_summary_20260607_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260607_b49_trading_range_pre2022_v1\b49_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b49_trading_range_pre2022_v1\b49_feature_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b49_trading_range_pre2022_v1\b49_spearman_corr_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b49_followups_pre2022_v1\b49_stability_summary_20260607_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b49-trading-range-evidence --date 20260607 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b49_trading_range_since2022_v1` + `b49-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b49_trading_range_since2022_v1\b49_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b49_followups_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b49-trading-range-evidence --date 20260607 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b49_trading_range_pre2022_v1` + `b49-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b49_trading_range_pre2022_v1\b49_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b49_followups_pre2022_v1`

==============================
BATCH_CLOSE（批?9；以证据拍板?==============================
- 数据规模：since2022 pooled n?3657（coverage ?100%）；pre2022 pooled n?3394
- 分层稳定性（symbol×A_all；min_n=20）：
  - since2022：range_flag(code4) frac_both?.281；range_score(qtiles4) frac_both?.158；range_width_atr(qtiles4) frac_both?.111；width_bucket(code4) frac_both?.286
  - pre2022：range_flag(code4) frac_both?.280；range_score(qtiles4) frac_both?.278；range_width_atr(qtiles4) frac_both?.240；width_bucket(code4) frac_both?.211
- 同构/去重风险（spearman；pooled）：
  - vs trade_pnl：≈0（range_score since2022?0.021；pre2022?0.015?  - vs entry_score：负相关（range_score since2022?0.191；pre2022?0.201?  - vs e1_break_strength_atr：弱相关（range_score since2022?0.054；pre2022?0.042?- v0 ROLE MAP?  - ab_range_flag_1h / ab_range_score_1h：DIAG_ONLY（稳定不足以晋升 gate/加分；用于复盘区间环境标记）
  - ab_range_width_atr_1h / ab_range_width_bucket_1h：DIAG_ONLY（窄/宽区间标签；后续若要晋升霢?MAE/max_dd?- 多AI讨论：不霢要（证据已能裁决；当前不足以形成晋升争议?
### 2026-06-07 批次50收口（资料型指标→字段落地：ALBrooks 交易区间陷阱与假突破识别 v0；全品种?
说明?- 为避免与既有 `b50-*`（entry_score/size_mult 家族）命令冲突，本批次的实现采用 `b50r-*` 命名?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260607_b50r_range_trap_since2022_v4\b50r_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b50r_range_trap_since2022_v4\b50r_feature_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b50r_range_trap_since2022_v4\b50r_spearman_corr_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b50r_followups_since2022_v4\b50r_stability_summary_20260607_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260607_b50r_range_trap_pre2022_v4\b50r_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b50r_range_trap_pre2022_v4\b50r_feature_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b50r_range_trap_pre2022_v4\b50r_spearman_corr_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b50r_followups_pre2022_v4\b50r_stability_summary_20260607_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b50r-range-trap-evidence --date 20260607 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b50r_range_trap_since2022_v4` + `b50r-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b50r_range_trap_since2022_v4\b50r_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b50r_followups_since2022_v4`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b50r-range-trap-evidence --date 20260607 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b50r_range_trap_pre2022_v4` + `b50r-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b50r_range_trap_pre2022_v4\b50r_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b50r_followups_pre2022_v4`

==============================
BATCH_CLOSE（批?0；以证据拍板?==============================
- 数据规模：since2022 pooled n?3657；pre2022 pooled n?3394
- 分层稳定性（symbol×A_all；min_n=20）：
  - since2022：trap_score(code4) n_sufficient=25；frac_pnl_better?.56；frac_stop_loss_better?.20；frac_both?.16
  - pre2022：trap_score(code4) n_sufficient=13；frac_pnl_better?.385；frac_stop_loss_better?.077；frac_both?.077
  - trap_flag(code4)：两段历史均 n_sufficient=0（信号过稢，无法做 0/1 对照的稳定验收）
- 同构/去重风险（spearman；pooled；since2022）：
  - trap_score vs trade_pnl?0.014（很弱）
  - trap_score vs entry_score?0.093（弱相关；不构成“同?别名”）
- v0 ROLE MAP?  - ab_range_trap_score_1h：DIAG_ONLY（当前更像收益可能略有改善但止损口径不一致，不晋?gate/加分?  - ab_range_trap_flag_1h：DIAG_ONLY（过稢?  - ab_range_trap_repeat_1h：DIAG_ONLY（样本不足且方向不稳?- 多AI讨论：不霢要（证据已能否决晋升；若未来再投入，仅建议先?MAE/max_dd 后再讨论“是否可作为风险回避/减仓”）

### 2026-06-07 批次51收口（资料型指标→字段落地：ALBrooks 反转量化识别与入场规?v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260607_b51_reversal_since2022_v1\b51_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b51_reversal_since2022_v1\b51_feature_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b51_reversal_since2022_v1\b51_spearman_corr_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b51_followups_since2022_v1\b51_stability_summary_20260607_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260607_b51_reversal_pre2022_v1\b51_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b51_reversal_pre2022_v1\b51_feature_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b51_reversal_pre2022_v1\b51_spearman_corr_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b51_followups_pre2022_v1\b51_stability_summary_20260607_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b51-reversal-evidence --date 20260607 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b51_reversal_since2022_v1` + `b51-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b51_reversal_since2022_v1\b51_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b51_followups_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b51-reversal-evidence --date 20260607 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b51_reversal_pre2022_v1` + `b51-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b51_reversal_pre2022_v1\b51_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b51_followups_pre2022_v1`

==============================
BATCH_CLOSE（批?1；以证据拍板?==============================
- 数据规模：since2022 pooled n?3657；pre2022 pooled n?3394
- 分层稳定性（symbol×A_all；min_n=20）：
  - since2022：bucket(code4) n_sufficient=0；flag(code4) n_sufficient=0（信号过稢，无法形成稳定验收）
  - pre2022：bucket(code4) n_sufficient=0；flag(code4) n_sufficient=0（同上）
- spearman（pooled）：
  - reversal_score vs trade_pnl：≈0（since2022?0.002；pre2022?0.002?  - reversal_flag vs trade_pnl：很弱（since2022?0.007；pre2022?0.019?  - reversal_score vs entry_score：弱负相关（since2022?0.126；pre2022?0.100?- v0 ROLE MAP?  - ab_reversal_score_1h / ab_reversal_bucket_1h / ab_reversal_flag_1h：DIAG_ONLY（当前实现信号过稢；不足以晋升 gate/加分?- 多AI讨论：不霢要（证据可直接否决晋升；若未来再投入，优先目标是“提高非 0 覆盖”再重跑稳定性）

### 2026-06-07 批次52收口（资料型指标→字段落地：ALBrooks 总在场内 Always-In 状判?v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260607_b52_always_in_since2022_v1\b52_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b52_always_in_since2022_v1\b52_feature_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b52_always_in_since2022_v1\b52_spearman_corr_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b52_followups_since2022_v1\b52_stability_summary_20260607_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260607_b52_always_in_pre2022_v1\b52_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b52_always_in_pre2022_v1\b52_feature_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b52_always_in_pre2022_v1\b52_spearman_corr_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b52_followups_pre2022_v1\b52_stability_summary_20260607_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b52-always-in-evidence --date 20260607 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b52_always_in_since2022_v1` + `b52-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b52_always_in_since2022_v1\b52_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b52_followups_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b52-always-in-evidence --date 20260607 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b52_always_in_pre2022_v1` + `b52-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b52_always_in_pre2022_v1\b52_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b52_followups_pre2022_v1`

==============================
BATCH_CLOSE（批?2；以证据拍板?==============================
- 数据规模：since2022 pooled n?3657；pre2022 pooled n?3394
- 分层稳定性（symbol×A_all；min_n=20）：
  - since2022：ab_always_in_agree_side_1h(code4) n_sufficient=27/32；frac_both?.444；ab_always_in_dir_1h(code4) frac_both?.357
  - pre2022：ab_always_in_agree_side_1h(code4) n_sufficient=25/28；frac_both?.600；ab_always_in_dir_1h(code4) frac_both?.417
  - state/strength：极端档样本不足（since2022 n_sufficient=1；pre2022 n_sufficient=8），不用于晋升判?- spearman（pooled）：
  - agree_side vs trade_pnl：弱正（since2022?0.019；pre2022?0.011?  - dir/state vs trade_pnl：很弱（? 级别?- v0 ROLE MAP?  - ab_always_in_agree_side_1h：ENTRY_FILTER_CANDIDATE（同向更好；晋升硬门控前霢?MAE/max_dd，避免更赚但更痛苦）
  - ab_always_in_dir_1h / ab_always_in_state_1h / ab_always_in_strength_1h：DIAG_ONLY（作为复盘标签；不晋?gate?- 多AI讨论：不霢要（已明确能晋升的只可能?agree_side”，而晋升前置是 MAE/max_dd 证据，不是参数讨论）

晋升前置补证据（trade_mae_atr / max_drawdown_per_trade；口径同批次46?H OHLC 在持仓窗口内计算；按 entry ATR 归一化）?- since2022：`backtest_out\stage2\indicator_audit\20260607_b52_always_in_mae_since2022_v1\b52_always_in_mae_summary_20260607_v1.csv`
  - pooled（symbol×A_all；min_n=20）：frac_pnl_better?.565；frac_mae_better?.645；frac_max_dd_better?.597；frac_all3(pnl&mae&max_dd)?.250
- pre2022：`backtest_out\stage2\indicator_audit\20260607_b52_always_in_mae_pre2022_v1\b52_always_in_mae_summary_20260607_v1.csv`
  - pooled（symbol×A_all；min_n=20）：frac_pnl_better?.547；frac_mae_better?.653；frac_max_dd_better?.773；frac_all3(pnl&mae&max_dd)?.373
- COMMAND?  - since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b52-always-in-mae --date 20260607 --scope all --split since2022 --min_n 20 --profile_merge 1 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b52_always_in_mae_since2022_v1`
  - pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b52-always-in-mae --date 20260607 --scope all --split pre2022 --min_n 20 --profile_merge 1 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b52_always_in_mae_pre2022_v1`

晋升裁决（是否进入可讨论硬门控）?- 结论：暂不晋升到“可讨论硬门控（两段历史 pooled ?frac_all3 远低?0.60；说明并非普适同?更赚且更不痛苦的强门控）
- 保留：ab_always_in_agree_side_1h 维持 ENTRY_FILTER_CANDIDATE（更偏降低止?降低痛苦”的候标签；若要继续推进硬门控，霢给出更强的一致证据或明确的条件化子环境）

### 2026-06-07 批次53收口（资料型指标→字段落地：ALBrooks 趋势棒与十字星量化定?v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260607_b53_trendbar_doji_since2022_v1\b53_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b53_trendbar_doji_since2022_v1\b53_feature_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b53_trendbar_doji_since2022_v1\b53_spearman_corr_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b53_followups_since2022_v1\b53_stability_summary_20260607_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260607_b53_trendbar_doji_pre2022_v1\b53_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b53_trendbar_doji_pre2022_v1\b53_feature_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b53_trendbar_doji_pre2022_v1\b53_spearman_corr_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b53_followups_pre2022_v1\b53_stability_summary_20260607_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b53-trendbar-doji-evidence --date 20260607 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b53_trendbar_doji_since2022_v1` + `b53-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b53_trendbar_doji_since2022_v1\b53_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b53_followups_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b53-trendbar-doji-evidence --date 20260607 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b53_trendbar_doji_pre2022_v1` + `b53-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b53_trendbar_doji_pre2022_v1\b53_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b53_followups_pre2022_v1`

==============================
BATCH_CLOSE（批?3；以证据拍板?==============================
- 数据规模：since2022 pooled n?3657；pre2022 pooled n?3394
- 分层稳定性（symbol×A_all；min_n=20）：
  - since2022：trendbar_strength(code4) frac_both?.406；trendbar_agree_side(code4) frac_both?.312；doji_flag(code4) n_sufficient=6/32（过稢?  - pre2022：trendbar_strength(code4) frac_both?.393；trendbar_agree_side(code4) frac_both?.385；doji_flag(code4) frac_both?.222（方向不稳）
- spearman（pooled）：
  - trendbar_strength vs trade_pnl?0.012；trendbar_agree_side vs trade_pnl?0.008；doji_flag vs trade_pnl?0.012（均很弱?- v0 ROLE MAP?  - ab_trendbar_strength_1h / ab_trendbar_agree_side_1h / ab_doji_flag_1h：DIAG_ONLY（基硢形标签；稳定性不足以晋升 gate/加分?- 多AI讨论：不霢要（证据足以否决晋升；后续如要推进应先做“与位置/区间/总在场内”交互分层再谈）

### 2026-06-07 批次54收口（资料型指标→字段落地：威科?弹簧Spring/上抛UT 量化判定 v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260607_b54_wyckoff_spring_ut_since2022_v1\b54_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b54_wyckoff_spring_ut_since2022_v1\b54_feature_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b54_wyckoff_spring_ut_since2022_v1\b54_spearman_corr_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b54_followups_since2022_v1\b54_stability_summary_20260607_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260607_b54_wyckoff_spring_ut_pre2022_v1\b54_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b54_wyckoff_spring_ut_pre2022_v1\b54_feature_summary_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b54_wyckoff_spring_ut_pre2022_v1\b54_spearman_corr_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b54_followups_pre2022_v1\b54_stability_summary_20260607_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b54-wyckoff-spring-ut-evidence --date 20260607 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b54_wyckoff_spring_ut_since2022_v1` + `b54-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b54_wyckoff_spring_ut_since2022_v1\b54_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b54_followups_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b54-wyckoff-spring-ut-evidence --date 20260607 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260607_b54_wyckoff_spring_ut_pre2022_v1` + `b54-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260607_b54_wyckoff_spring_ut_pre2022_v1\b54_bucket_stats_20260607_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260607_b54_followups_pre2022_v1`

==============================
BATCH_CLOSE（批?4；以证据拍板?==============================
- 数据规模：since2022 pooled n?3657；pre2022 pooled n?3394
- 分层稳定性（symbol×A_all；min_n=20）：
  - wy_spring_ut_flag_1h / wy_spring_ut_score_1h：两段历史均 n_sufficient=0（信号过稢，无法验收）
  - wy_spring_ut_repeat_1h：since2022 frac_both?.800（但 n_sufficient=5/32）；pre2022 frac_both?.000（n_sufficient=9/28；不稳健?- spearman（pooled）：flag/score ?trade_pnl ?0；repeat ?trade_pnl 弱正（since2022?0.020?- v0 ROLE MAP?  - wy_spring_ut_flag_1h / wy_spring_ut_score_1h / wy_spring_ut_repeat_1h：DIAG_ONLY（当前实现以“回到区间内 + 信号棒评分确认；样本与稳健不足以晋升 gate/加分?- 备注（成交量约束）：
  - MARKER: REOPEN_ON_A_SHARES_EXCHANGE_VOLUME（Wyckoff_Spring_UT；外?指数/大宗先天不讨论晋升；A股数据接入后重开本段再裁决）
  - Wyckoff ?Spring/UT 原教义非常强调成交量（缩量下?诱空、放量回收UT 的诱多量能等），这是形成立的重要条件之一
  - 当前项目?1H 数据确实?`volume` 列，但在外汇/指数/大宗品种里常?tick volume 或经纪商口径，和交易扢真实成交量不等价；且若数据源缺失 volume 时会被填 0（见 backtest_p0.py ?load_ohlcv_1h?  - 因此本批次只把量能作为弱约束（break bar ?volume 不持续放大），结论只?DIAG_ONLY 收口；若未来切换?A ?交易扢真实量能数据，可重开该家族并把量能条件升级为硬约束再回测
- 多AI讨论：不霢要（结论由稀疏与稳健性不足直接否决晋升；若要再投入应先做 coverage 提升或转到更高周期）

### 2026-06-08 批次55收口（资料型指标→字段落地：补充抢术_价格形识别（吞没/锤子?射击之星）v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260608_b55_candle_patterns_since2022_v1\b55_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b55_candle_patterns_since2022_v1\b55_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b55_candle_patterns_since2022_v1\b55_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b55_followups_since2022_v1\b55_stability_summary_20260608_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260608_b55_candle_patterns_pre2022_v1\b55_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b55_candle_patterns_pre2022_v1\b55_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b55_candle_patterns_pre2022_v1\b55_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b55_followups_pre2022_v1\b55_stability_summary_20260608_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b55-candle-patterns-evidence --date 20260608 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b55_candle_patterns_since2022_v1` + `b55-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b55_candle_patterns_since2022_v1\b55_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b55_followups_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b55-candle-patterns-evidence --date 20260608 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b55_candle_patterns_pre2022_v1` + `b55-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b55_candle_patterns_pre2022_v1\b55_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b55_followups_pre2022_v1`

==============================
BATCH_CLOSE（批?5；以证据拍板?==============================
- 数据规模：since2022 pooled n?3657；pre2022 pooled n?3394
- 分层稳定性（symbol×A_all；min_n=20）：
  - since2022：engulf_flag frac_both?.281；engulf_score frac_both?.375；pinbar_flag n_sufficient=15/32（frac_both?.400）；pinbar_score n_sufficient=19/32（frac_both?.368?  - pre2022：engulf_flag frac_both?.538；engulf_score frac_both?.556；pinbar_flag/score n_sufficient=9/27（frac_both?.556?- 分段丢致：since2022 vs pre2022 ?top_minus_bot_avg_pnl 上出现方向反转（例如 engulf_flag：since2022 明显为负、pre2022 为正），不具备全品种通用可晋升的证据
- spearman（pooled）：?trade_pnl 相关性近 0（|rho|<0.02），仅能作为形标?- v0 ROLE MAP?  - px_cdl_engulf_score_1h / px_cdl_engulf_flag_1h / px_cdl_pinbar_score_1h / px_cdl_pinbar_flag_1h：DIAG_ONLY（形态标签；不晋?gate/加分?- 多AI讨论：不霢要（证据已足够否决晋升；若未来要推进应加“位?趋势/区间背景”交互分层再谈）

### 2026-06-08 批次56收口（资料型指标→字段落地：斐波那契回调位（0.236/0.382/0.5/0.618/0.786）v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260608_b56_fib_retrace_since2022_v1\b56_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b56_fib_retrace_since2022_v1\b56_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b56_fib_retrace_since2022_v1\b56_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b56_followups_since2022_v1\b56_stability_summary_20260608_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260608_b56_fib_retrace_pre2022_v1\b56_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b56_fib_retrace_pre2022_v1\b56_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b56_fib_retrace_pre2022_v1\b56_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b56_followups_pre2022_v1\b56_stability_summary_20260608_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b56-fib-retrace-evidence --date 20260608 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b56_fib_retrace_since2022_v1` + `b56-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b56_fib_retrace_since2022_v1\b56_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b56_followups_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b56-fib-retrace-evidence --date 20260608 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b56_fib_retrace_pre2022_v1` + `b56-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b56_fib_retrace_pre2022_v1\b56_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b56_followups_pre2022_v1`

==============================
BATCH_CLOSE（批?6；以证据拍板?==============================
- 数据规模：since2022 pooled n?3657；pre2022 pooled n?3394
- 分层稳定性（symbol×A_all；min_n=20）：
  - fib_retrace_bucket_1h：两段均 n_sufficient 很低（since2022=2/32；pre2022=1/28），无法验收
  - fib_retrace_near_flag_1h / fib_retrace_near_score_1h：since2022 frac_both?.375（n_sufficient=16/32）；pre2022 frac_both?.200（n_sufficient=5/28；不稳健?- spearman（pooled）：?trade_pnl 相关性近 0（|rho|<0.01?- v0 ROLE MAP?  - fib_retrace_bucket_1h / fib_retrace_near_flag_1h / fib_retrace_near_score_1h / fib_retrace_depth_1h：DIAG_ONLY（回调位“触?接近”标签；不晋?gate/加分?- 多AI讨论：不霢要（证据已足够否决晋升；若未来要推进应与趋势/区间/反转形做交互分层再谈?
### 2026-06-08 批次57收口（资料型指标→字段落地：KD 钝化/脱离钝化（基?1D K 值对齐到 1H；按交易方向?favor/unfavor）v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260608_b57_kd_saturation_since2022_v1\b57_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b57_kd_saturation_since2022_v1\b57_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b57_kd_saturation_since2022_v1\b57_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b57_followups_since2022_v1\b57_stability_summary_20260608_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260608_b57_kd_saturation_pre2022_v1\b57_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b57_kd_saturation_pre2022_v1\b57_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b57_kd_saturation_pre2022_v1\b57_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b57_followups_pre2022_v1\b57_stability_summary_20260608_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b57-kd-saturation-evidence --date 20260608 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b57_kd_saturation_since2022_v1` + `b57-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b57_kd_saturation_since2022_v1\b57_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b57_followups_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b57-kd-saturation-evidence --date 20260608 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b57_kd_saturation_pre2022_v1` + `b57-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b57_kd_saturation_pre2022_v1\b57_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b57_followups_pre2022_v1`

==============================
BATCH_CLOSE（批?7；以证据拍板?==============================
- 数据规模：since2022 pooled n?3657；pre2022 pooled n?3394
- 分层稳定性（symbol×A_all；min_n=20）：
  - kd_sat_favor_bucket_1h：since2022 n_pairs 太少（该特征?bucket_stats 中覆盖不稳定）；pre2022 spearman 也为 NaN（有效样本不?几乎常量?  - kd_sat_unfavor_bucket_1h：since2022 frac_both?.375（n_sufficient=32/32）；pre2022 frac_both?.321（n_sufficient=28/28；方向偏弱）
  - kd_sat_*_exit_1h：两段均极稀（大?n_sufficient=0），不作为可验收特征
- spearman（pooled）：?trade_pnl 相关性很弱（多数 |rho|?.00x?- v0 ROLE MAP?  - kd_sat_favor_bucket_1h / kd_sat_unfavor_bucket_1h / kd_sat_favor_exit_1h / kd_sat_unfavor_exit_1h / kd_sat_favor_extreme_1h：DIAG_ONLY（钝化标签；不晋?gate/加分?- 多AI讨论：不霢要（证据不足以晋升；若未来要推进应与“趋?区间/总在场内”做交互分层再谈?
### 2026-06-08 批次58收口（资料型指标→字段落地：EMA 支撑/阻力的回收（touch/fake_break/reclaim）v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260608_b58_ema_reclaim_since2022_v1\b58_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b58_ema_reclaim_since2022_v1\b58_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b58_ema_reclaim_since2022_v1\b58_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b58_followups_since2022_v1\b58_stability_summary_20260608_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260608_b58_ema_reclaim_pre2022_v1\b58_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b58_ema_reclaim_pre2022_v1\b58_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b58_ema_reclaim_pre2022_v1\b58_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b58_followups_pre2022_v1\b58_stability_summary_20260608_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b58-ema-reclaim-evidence --date 20260608 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b58_ema_reclaim_since2022_v1` + `b58-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b58_ema_reclaim_since2022_v1\b58_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b58_followups_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b58-ema-reclaim-evidence --date 20260608 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b58_ema_reclaim_pre2022_v1` + `b58-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b58_ema_reclaim_pre2022_v1\b58_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b58_followups_pre2022_v1`

==============================
BATCH_CLOSE（批?8；以证据拍板?==============================
- 数据规模：since2022 pooled n?3657；pre2022 pooled n?3394
- 分层稳定性（symbol×A_all；min_n=20）：
  - ab_ema_touch_1h / ab_ema_fake_break_1h：两段均 n_sufficient=0（触发过稢?  - ab_ema_reclaim_1h：since2022 frac_both?.313；pre2022 frac_both?.407（方向偏弱，且不构成晋升证据?  - ab_ema_reclaim_score_1h：since2022 frac_both?.313；pre2022 frac_both?.370（方向偏弱；?pooled spearman 跨分段符号不丢致）
- spearman（pooled）：?trade_pnl 相关性很弱（|rho|?.01 以内；部分特?since2022 vs pre2022 方向相反?- v0 ROLE MAP?  - ab_ema_touch_1h / ab_ema_fake_break_1h / ab_ema_reclaim_1h / ab_ema_reclaim_score_1h：DIAG_ONLY（EMA 位置/回收形标签；不晋?gate/加分?- 多AI讨论：不霢要（证据不足以晋升；若未来要推进应与“趋?区间/总在场内/反转形做交互分层再谈?
### 2026-06-08 批次59收口（资料型指标→字段落地：EMA20 斜率/相对位置 + 日线EMA200宏观侧（对齐?H）v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260608_b59_ema_regime_since2022_v1\b59_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b59_ema_regime_since2022_v1\b59_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b59_ema_regime_since2022_v1\b59_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b59_followups_since2022_v1\b59_stability_summary_20260608_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260608_b59_ema_regime_pre2022_v1\b59_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b59_ema_regime_pre2022_v1\b59_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b59_ema_regime_pre2022_v1\b59_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b59_followups_pre2022_v1\b59_stability_summary_20260608_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b59-ema-regime-evidence --date 20260608 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b59_ema_regime_since2022_v1` + `b59-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b59_ema_regime_since2022_v1\b59_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b59_followups_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b59-ema-regime-evidence --date 20260608 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b59_ema_regime_pre2022_v1` + `b59-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b59_ema_regime_pre2022_v1\b59_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b59_followups_pre2022_v1`

==============================
BATCH_CLOSE（批?9；以证据拍板?==============================
- 数据规模：since2022 pooled n?3657；pre2022 pooled n?3394
- 分层稳定性（symbol×A_all；min_n=20）：
  - ab_ema20_gt_ema200_1h：since2022 frac_both?.469；pre2022 frac_both?.370（方向偏弱，不构成晋升证据）
  - ab_ema200_side_1h：since2022 frac_both?.406；pre2022 frac_both?.259（分段明显变弱）
  - ab_ema20_side_1h / ab_ema20_slope_bucket_1h：两?frac_both?.375（偏弱）
- spearman（pooled）：?trade_pnl 相关性很弱（|rho|?.03 以内?- v0 ROLE MAP?  - ab_ema20_slope_bucket_1h / ab_ema20_side_1h / ab_ema200_side_1h / ab_ema20_gt_ema200_1h：DIAG_ONLY（趋?宏观侧标签；不晋?gate/加分?- 多AI讨论：不霢要（证据不足以晋升；若未来要推进应与“区?反转/风险( MAE,maxDD )”做交互分层再谈?
### 2026-06-08 批次61收口（资料型指标→字段落地：KD 背离（顶背离/底背离；1D pivot 确认 + 次日反转K线确认；对齐?H）v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260608_b61_kd_divergence_since2022_v1\b61_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b61_kd_divergence_since2022_v1\b61_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b61_kd_divergence_since2022_v1\b61_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b61_followups_since2022_v1\b61_stability_summary_20260608_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260608_b61_kd_divergence_pre2022_v1\b61_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b61_kd_divergence_pre2022_v1\b61_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b61_kd_divergence_pre2022_v1\b61_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b61_followups_pre2022_v1\b61_stability_summary_20260608_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b61-kd-divergence-evidence --date 20260608 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b61_kd_divergence_since2022_v1` + `b61-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b61_kd_divergence_since2022_v1\b61_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b61_followups_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b61-kd-divergence-evidence --date 20260608 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b61_kd_divergence_pre2022_v1` + `b61-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b61_kd_divergence_pre2022_v1\b61_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b61_followups_pre2022_v1`

==============================
BATCH_CLOSE（批?1；以证据拍板?==============================
- 数据规模：since2022 pooled n?3657；pre2022 pooled n?3394
- 分层稳定性（symbol×A_all；min_n=20）：两段?n_sufficient=0（信号极稢，无法验收；pooled ?top_minus_bot 不可用作晋升依据?- spearman（pooled）：?trade_pnl 相关性近 0（since2022 为负、pre2022 为正，且绝对值很小）
- v0 ROLE MAP?  - kd_div_score_1h / kd_div_flag_1h：DIAG_ONLY（背离确认标签；过稀，不晋升 gate/加分?- 多AI讨论：不霢要（证据不足以讨论晋升；若未来要推进应放宽确认链或改为背离预?无确?”的诊断版本再看 coverage?
### 2026-06-08 批次62收口（资料型指标→字段落地：KD 基础极（1D K 对齐 1H；按方向?favor_k 分桶/极标记）v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260608_b62_kd_basic_since2022_v1\b62_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b62_kd_basic_since2022_v1\b62_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b62_kd_basic_since2022_v1\b62_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b62_followups_since2022_v1\b62_stability_summary_20260608_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260608_b62_kd_basic_pre2022_v1\b62_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b62_kd_basic_pre2022_v1\b62_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b62_kd_basic_pre2022_v1\b62_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b62_followups_pre2022_v1\b62_stability_summary_20260608_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b62-kd-basic-evidence --date 20260608 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b62_kd_basic_since2022_v1` + `b62-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b62_kd_basic_since2022_v1\b62_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b62_followups_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b62-kd-basic-evidence --date 20260608 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b62_kd_basic_pre2022_v1` + `b62-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b62_kd_basic_pre2022_v1\b62_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b62_followups_pre2022_v1`

==============================
BATCH_CLOSE（批?2；以证据拍板?==============================
- 数据规模：since2022 pooled n?3486；pre2022 pooled n?3386
- 分层稳定性（symbol×A_all；min_n=20）：
  - kd_basic_favor_bucket_1h：since2022 frac_both?.375；pre2022 frac_both?.350（弱?  - kd_basic_favor_extreme_1h：since2022/pre2022 n_sufficient=0（极值信号过稢，无法验收）
- v0 ROLE MAP?  - kd_basic_favor_bucket_1h / kd_basic_favor_extreme_1h：DIAG_ONLY（KD 位置标签；不晋升 gate/加分?
### 2026-06-08 批次63收口（资料型指标→字段落地：KD 多周期对齐（1D + 4H K 对齐 1H；按方向统计 favor/unfavor 计数）v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260608_b63_kd_multitf_align_since2022_v1\b63_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b63_kd_multitf_align_since2022_v1\b63_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b63_kd_multitf_align_since2022_v1\b63_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b63_followups_since2022_v1\b63_stability_summary_20260608_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260608_b63_kd_multitf_align_pre2022_v1\b63_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b63_kd_multitf_align_pre2022_v1\b63_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b63_kd_multitf_align_pre2022_v1\b63_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b63_followups_pre2022_v1\b63_stability_summary_20260608_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b63-kd-multitf-align-evidence --date 20260608 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b63_kd_multitf_align_since2022_v1` + `b63-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b63_kd_multitf_align_since2022_v1\b63_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b63_followups_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b63-kd-multitf-align-evidence --date 20260608 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b63_kd_multitf_align_pre2022_v1` + `b63-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b63_kd_multitf_align_pre2022_v1\b63_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b63_followups_pre2022_v1`

==============================
BATCH_CLOSE（批?3；以证据拍板?==============================
- 数据规模：since2022 pooled n?3486；pre2022 pooled n?3386
- 分层稳定性（symbol×A_all；min_n=20）：
  - kd_align_favor_count_1h：since2022/pre2022 n_sufficient=0（信号过稢，无法验收）
  - kd_align_unfavor_count_1h：since2022 frac_both?.438；pre2022 frac_both?.385（弱?- v0 ROLE MAP?  - kd_align_favor_count_1h / kd_align_unfavor_count_1h：DIAG_ONLY（多周期 KD 丢致标签；不晋?gate/加分?
### 2026-06-08 批次64收口（资料型指标→字段落地：KD + MACD 共振?D；hist ?hist_slope；对?1H）v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260608_b64_kd_macd_resonance_since2022_v1\b64_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b64_kd_macd_resonance_since2022_v1\b64_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b64_kd_macd_resonance_since2022_v1\b64_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b64_followups_since2022_v1\b64_stability_summary_20260608_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260608_b64_kd_macd_resonance_pre2022_v1\b64_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b64_kd_macd_resonance_pre2022_v1\b64_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b64_kd_macd_resonance_pre2022_v1\b64_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b64_followups_pre2022_v1\b64_stability_summary_20260608_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b64-kd-macd-resonance-evidence --date 20260608 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b64_kd_macd_resonance_since2022_v1` + `b64-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b64_kd_macd_resonance_since2022_v1\b64_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b64_followups_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b64-kd-macd-resonance-evidence --date 20260608 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b64_kd_macd_resonance_pre2022_v1` + `b64-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b64_kd_macd_resonance_pre2022_v1\b64_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b64_followups_pre2022_v1`

==============================
BATCH_CLOSE（批?4；以证据拍板?==============================
- 数据规模：since2022 pooled n?3486；pre2022 pooled n?3386
- 分层稳定性（symbol×A_all；min_n=20）：
  - kd_macd_res_flag_1h：since2022 frac_both?.344；pre2022 frac_both?.462（偏弱且分段不一致）
  - kd_macd_res_score_1h：since2022/pre2022 n_sufficient=0（桶过稀，无法验收）
- v0 ROLE MAP?  - kd_macd_res_flag_1h / kd_macd_res_score_1h：DIAG_ONLY（共振标签；不晋?gate/加分?
### 2026-06-08 批次65收口（资料型指标→字段落地：1H 成交量形态（volume/MA ratio：dryup/spike + 分桶）v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260608_b65_volume_patterns_since2022_v1\b65_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b65_volume_patterns_since2022_v1\b65_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b65_volume_patterns_since2022_v1\b65_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b65_followups_since2022_v1\b65_stability_summary_20260608_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260608_b65_volume_patterns_pre2022_v1\b65_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b65_volume_patterns_pre2022_v1\b65_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b65_volume_patterns_pre2022_v1\b65_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b65_followups_pre2022_v1\b65_stability_summary_20260608_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b65-volume-patterns-evidence --date 20260608 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b65_volume_patterns_since2022_v1` + `b65-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b65_volume_patterns_since2022_v1\b65_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b65_followups_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b65-volume-patterns-evidence --date 20260608 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b65_volume_patterns_pre2022_v1` + `b65-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b65_volume_patterns_pre2022_v1\b65_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b65_followups_pre2022_v1`

==============================
BATCH_CLOSE（批?5；以证据拍板?==============================
- 数据规模：since2022 pooled n?3486；pre2022 pooled n?3286
- 分层稳定性（symbol×A_all；min_n=20）：
  - vol_ratio_bucket_1h：since2022 frac_both?.533；pre2022 frac_both?.391（分段不丢致）
  - vol_spike_flag_1h：since2022 frac_both?.375；pre2022 frac_both?.222（弱?  - vol_dryup_flag_1h：since2022 frac_both?.233；pre2022 frac_both?.091（弱?- 口径限制：外?指数/大宗?volume 多为 tick volume 或口径不丢致，不允许把该家族升级为 gate/加分；仅做诊断标签留?- v0 ROLE MAP?  - vol_ratio_bucket_1h / vol_spike_flag_1h / vol_dryup_flag_1h：DIAG_ONLY（量能形态标签；MARKER: REOPEN_ON_A_SHARES_EXCHANGE_VOLUME?
### 2026-06-08 批次66收口（资料型指标→字段落地：RSI 基础极（1D RSI 对齐 1H；按方向?favor_rsi 分桶/极标记）v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260608_b66_rsi_basic_since2022_v1\b66_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b66_rsi_basic_since2022_v1\b66_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b66_rsi_basic_since2022_v1\b66_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b66_followups_since2022_v1\b66_stability_summary_20260608_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260608_b66_rsi_basic_pre2022_v1\b66_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b66_rsi_basic_pre2022_v1\b66_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b66_rsi_basic_pre2022_v1\b66_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b66_followups_pre2022_v1\b66_stability_summary_20260608_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b66-rsi-basic-evidence --date 20260608 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b66_rsi_basic_since2022_v1` + `b66-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b66_rsi_basic_since2022_v1\b66_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b66_followups_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b66-rsi-basic-evidence --date 20260608 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b66_rsi_basic_pre2022_v1` + `b66-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b66_rsi_basic_pre2022_v1\b66_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b66_followups_pre2022_v1`

==============================
BATCH_CLOSE（批?6；以证据拍板?==============================
- 数据规模：since2022 pooled n?3486；pre2022 pooled n?3386
- 分层稳定性（symbol×A_all；min_n=20）：
  - rsi_basic_favor_bucket_1h：since2022 frac_stop_loss_better?.778；frac_both?.444；pre2022 frac_stop_loss_better?.864；frac_both?.545（偏“风险侧”有效，?pnl 改善不稳?  - rsi_basic_favor_extreme_1h：since2022/pre2022 spearman 为空（极值事件过稢，不可用作晋升依据）
- spearman（pooled）：rsi_basic_favor_bucket_1h ?trade_pnl ?0（since2022?0.011；pre2022?.016?- v0 ROLE MAP?  - rsi_basic_favor_bucket_1h / rsi_basic_favor_extreme_1h：DIAG_ONLY（RSI 位置标签；偏“止损更好但未补 MAE/maxDD，不晋升 gate/加分?
### 2026-06-08 批次67收口（资料型指标→字段落地：CCI 基础极（1D CCI 对齐 1H；按方向?favor_cci 分桶/极标记）v0；全品种?
证据（scope=all）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260608_b67_cci_basic_since2022_v1\b67_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b67_cci_basic_since2022_v1\b67_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b67_cci_basic_since2022_v1\b67_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b67_followups_since2022_v1\b67_stability_summary_20260608_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260608_b67_cci_basic_pre2022_v1\b67_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b67_cci_basic_pre2022_v1\b67_feature_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b67_cci_basic_pre2022_v1\b67_spearman_corr_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b67_followups_pre2022_v1\b67_stability_summary_20260608_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b67-cci-basic-evidence --date 20260608 --scope all --split since2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b67_cci_basic_since2022_v1` + `b67-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b67_cci_basic_since2022_v1\b67_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b67_followups_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b67-cci-basic-evidence --date 20260608 --scope all --split pre2022 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b67_cci_basic_pre2022_v1` + `b67-followups --min_n 20 --profile_merge 1 --bucket_stats .\backtest_out\stage2\indicator_audit\20260608_b67_cci_basic_pre2022_v1\b67_bucket_stats_20260608_v1.csv --out_dir .\backtest_out\stage2\indicator_audit\20260608_b67_followups_pre2022_v1`

==============================
BATCH_CLOSE（批?7；以证据拍板?==============================
- 数据规模：since2022 pooled n?3486；pre2022 pooled n?3386
- 分层稳定性（symbol×A_all；min_n=20）：
  - cci_basic_favor_bucket_1h：since2022 frac_stop_loss_better?.793；frac_both?.448；pre2022 frac_stop_loss_better?.808；frac_both?.615（偏“风险侧”有效，?since2022 vs pre2022 ?top_minus_bot 方向不一致）
  - cci_basic_favor_extreme_1h：since2022/pre2022 spearman 为空（极值事件过稢，不可用作晋升依据）
- spearman（pooled）：cci_basic_favor_bucket_1h ?trade_pnl ?0（since2022?.008；pre2022?.011?- v0 ROLE MAP?  - cci_basic_favor_bucket_1h / cci_basic_favor_extreme_1h：DIAG_ONLY（CCI 位置标签；偏“止损更好但分段方向不稳，且未补 MAE/maxDD，不晋升 gate/加分?
### 2026-06-08 批次68证据（MAE 验证：RSI/CCI 的风险侧有效性补证据；trade_mae_atr / trade_mfe_atr；全品种?
证据（scope=all；profile_merge=1；min_n=20）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260608_b68_osc_mae_since2022_v1\b68_mae_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b68_osc_mae_since2022_v1\b68_mae_pairs_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b68_osc_mae_since2022_v1\b68_mae_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b68_osc_mae_since2022_v1\b68_mae_coverage_20260608_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260608_b68_osc_mae_pre2022_v1\b68_mae_bucket_stats_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b68_osc_mae_pre2022_v1\b68_mae_pairs_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b68_osc_mae_pre2022_v1\b68_mae_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b68_osc_mae_pre2022_v1\b68_mae_coverage_20260608_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b68-osc-mae-evidence --date 20260608 --scope all --split since2022 --min_n 20 --profile_merge 1 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b68_osc_mae_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b68-osc-mae-evidence --date 20260608 --scope all --split pre2022 --min_n 20 --profile_merge 1 --csv_dir .\data --out_dir .\backtest_out\stage2\indicator_audit\20260608_b68_osc_mae_pre2022_v1`

==============================
BATCH_CLOSE（批?8；以证据拍板?==============================
- 目标：验?B66/B67 的止损更好是否对应真实风险下降（MAE/ATR 更小?- RSI（rsi_basic_favor_bucket_1h；按 symbol×A_all；min_n=20）：
  - since2022：n_pairs=37；frac_mae_better?.811；frac_stop_loss_better?.595；frac_both_mae_stop?.541
  - pre2022：n_pairs=32；frac_mae_better?.688；frac_stop_loss_better?.781；frac_both_mae_stop?.531
- CCI（cci_basic_favor_bucket_1h；按 symbol×A_all；min_n=20）：
  - since2022：n_pairs=126；frac_mae_better?.595；frac_stop_loss_better?.571；frac_both_mae_stop?.397
  - pre2022：n_pairs=71；frac_mae_better?.493；frac_stop_loss_better?.577；frac_both_mae_stop?.380
- 结论（v0）：
  - RSI：风险侧证据成立（MAE 更小 + 止损更好在两段都能复现）?rsi_basic_favor_bucket_1h 进入 RISK_ONLY_CANDIDATE（仍不做?gate；下丢步才讨论“避弢朢差桶”的弱门槛）
  - CCI：风险侧证据偏弱/分段不稳 ?维持 DIAG_ONLY

### 2026-06-08 批次69证据（RSI bucket 弱过滤模拟：避开朢差桶；keep/drop 对照；全品种?
证据（scope=all；min_n=20；profile_merge=0）：
- since2022（drop_bucket=0）：
  - `backtest_out\stage2\indicator_audit\20260608_b69_rsi_filter_sim_since2022_drop0_v4\b69_filter_pairs_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b69_rsi_filter_sim_since2022_drop0_v4\b69_filter_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b69_rsi_filter_sim_since2022_drop0_v4\b69_filter_coverage_20260608_v1.csv`
- pre2022（drop_bucket=0）：
  - `backtest_out\stage2\indicator_audit\20260608_b69_rsi_filter_sim_pre2022_drop0_v4\b69_filter_pairs_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b69_rsi_filter_sim_pre2022_drop0_v4\b69_filter_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b69_rsi_filter_sim_pre2022_drop0_v4\b69_filter_coverage_20260608_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b69-rsi-filter-sim-evidence --date 20260608 --scope all --split since2022 --min_n 20 --drop_bucket 0 --out_dir .\backtest_out\stage2\indicator_audit\20260608_b69_rsi_filter_sim_since2022_drop0_v4`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b69-rsi-filter-sim-evidence --date 20260608 --scope all --split pre2022 --min_n 20 --drop_bucket 0 --out_dir .\backtest_out\stage2\indicator_audit\20260608_b69_rsi_filter_sim_pre2022_drop0_v4`

==============================
BATCH_CLOSE（批?9；以证据拍板?==============================
- 目标：把“RSI 风险侧有效（B68）推进到“弱过滤是否可行”（是否能在不丢太多 trades 的情况下，稳定改善风险侧与收益侧?- 方案：rsi_basic_favor_bucket_1h 避开 bucket=0（最差桶；即 favor_rsi<=oversold?- since2022：n_pairs=31；frac_pnl_better?.581；frac_stop_loss_better?.516；frac_mae_better?.677；median_keep_pct?.855
- pre2022：n_pairs=27；frac_pnl_better?.593；frac_stop_loss_better?.630；frac_mae_better?.593；median_keep_pct?.882
- 结论（v0）：弱过滤避弢 bucket=0”在两段都能复现（风险侧更稳；交易数量损失中等偏小）?进入“可讨论的弱门槛候（仍不接入执行门控；下丢步用 p0_sweep 做端到端门控回测验证?
### 2026-06-08 批次70证据（CCI bucket 弱过滤模拟：避开朢差桶；keep/drop 对照；全品种?
证据（scope=all；min_n=20；profile_merge=0）：
- since2022（drop_bucket=0）：
  - `backtest_out\stage2\indicator_audit\20260608_b70_cci_filter_sim_since2022_drop0_v4\b70_filter_pairs_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b70_cci_filter_sim_since2022_drop0_v4\b70_filter_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b70_cci_filter_sim_since2022_drop0_v4\b70_filter_coverage_20260608_v1.csv`
- pre2022（drop_bucket=0）：
  - `backtest_out\stage2\indicator_audit\20260608_b70_cci_filter_sim_pre2022_drop0_v4\b70_filter_pairs_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b70_cci_filter_sim_pre2022_drop0_v4\b70_filter_summary_20260608_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260608_b70_cci_filter_sim_pre2022_drop0_v4\b70_filter_coverage_20260608_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b70-cci-filter-sim-evidence --date 20260608 --scope all --split since2022 --min_n 20 --drop_bucket 0 --out_dir .\backtest_out\stage2\indicator_audit\20260608_b70_cci_filter_sim_since2022_drop0_v4`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b70-cci-filter-sim-evidence --date 20260608 --scope all --split pre2022 --min_n 20 --drop_bucket 0 --out_dir .\backtest_out\stage2\indicator_audit\20260608_b70_cci_filter_sim_pre2022_drop0_v4`

==============================
BATCH_CLOSE（批?0；以证据拍板?==============================
- since2022：n_pairs=126；frac_pnl_better?.476；frac_stop_loss_better?.548；frac_mae_better?.603；median_keep_pct?.719
- pre2022：n_pairs=71；frac_pnl_better?.563；frac_stop_loss_better?.606；frac_mae_better?.437；median_keep_pct?.716
- 结论（v0）：风险侧（MAE）在 pre2022 不支持（方向反复）→ 不作为弱门槛候；维持 DIAG_ONLY

### 2026-06-09 批次71证据（RSI bucket ?gate 验证：baseline 端到端重跑对照；drop_bucket=0；全品种?
证据（scope=all；split=since2022 / pre2022；min_window_days=365；profile=A_universal 参数集）?- since2022?  - `backtest_out\stage2\indicator_audit\20260609_b71_rsi_truegate_since2022_v1\b71_truegate_detail_20260609_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260609_b71_rsi_truegate_since2022_v1\b71_truegate_agg_20260609_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260609_b71_rsi_truegate_pre2022_v1\b71_truegate_detail_20260609_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260609_b71_rsi_truegate_pre2022_v1\b71_truegate_agg_20260609_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b71-rsi-truegate-sweep --date 20260609 --scope all --split since2022 --drop_bucket 0 --enable-score-sizing 1 --enable-score-filter 0 --e1-bb-squeeze-veto 0 --e1-bb-squeeze-penalty 0.6 --e1-fail-k 1.5 --enable-e1-atr-regime-gate 0 --enable-e2-break-confirm 1 --e2-touch-requires-strong 1 --out_dir .\backtest_out\stage2\indicator_audit\20260609_b71_rsi_truegate_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b71-rsi-truegate-sweep --date 20260609 --scope all --split pre2022 --drop_bucket 0 --enable-score-sizing 1 --enable-score-filter 0 --e1-bb-squeeze-veto 0 --e1-bb-squeeze-penalty 0.6 --e1-fail-k 1.5 --enable-e1-atr-regime-gate 0 --enable-e2-break-confirm 1 --e2-touch-requires-strong 1 --out_dir .\backtest_out\stage2\indicator_audit\20260609_b71_rsi_truegate_pre2022_v1`

==============================
BATCH_CLOSE（批?1；以证据拍板?==============================
- 目标：把 B69 ?post-hoc “弱过滤候升级到 baseline 端到端重跑（避免规模效应/持仓互斥导致的假象）
- 方案：新增真 gate（默认关闭）：`enable_entry_rsi_bucket_gate=1` ?`entry_rsi_drop_bucket=0`
- since2022（symbols=32；agg 平均口径）：
  - avg_base_net_pnl?11100.04；avg_gate_net_pnl?7844.44；avg_delta_net_pnl?3255.61
  - avg_base_final_max_dd_pct?0.2499；avg_gate_final_max_dd_pct?0.2431（dd 变小?- pre2022（symbols=28；agg 平均口径）：
  - avg_base_net_pnl?11875.77；avg_gate_net_pnl?9531.92；avg_delta_net_pnl?2343.85
  - avg_base_final_max_dd_pct?0.2524；avg_gate_final_max_dd_pct?0.2488（dd 变小?- 结论（v0）：支持把避弢 rsi_basic_favor_bucket_1h ?bucket=0”列为弱门槛 ENTRY_FILTER_CANDIDATE（研究侧；默认不启用；后续再做与现有 gate 的叠?冲突评估?
### 2026-06-09 批次72证据（RSI ?gate 作用域拆解：?E1 vs ?E2；drop_bucket=0；全品种?
证据（scope=all；min_window_days=365；profile=A_universal 参数集）?- since2022?  - ?E1：`backtest_out\stage2\indicator_audit\20260609_b72_rsi_truegate_e1_since2022_v3\b71_truegate_agg_20260609_v1.csv`
  - ?E2：`backtest_out\stage2\indicator_audit\20260609_b72_rsi_truegate_e2_since2022_v3\b71_truegate_agg_20260609_v1.csv`
- pre2022?  - ?E1：`backtest_out\stage2\indicator_audit\20260609_b72_rsi_truegate_e1_pre2022_v3\b71_truegate_agg_20260609_v1.csv`
  - ?E2：`backtest_out\stage2\indicator_audit\20260609_b72_rsi_truegate_e2_pre2022_v3\b71_truegate_agg_20260609_v1.csv`

==============================
BATCH_CLOSE（批?2；以证据拍板?==============================
- since2022（symbols=32；avg_delta_net_pnl）：仅E1?995.65；仅E2?1498.25
- pre2022（symbols=28；avg_delta_net_pnl）：仅E1?2344.64；仅E2?672.23（有害）
- 结论（v0）：若启?RSI bucket ?gate，优先限?`entry_rsi_gate_scope="e1"`（避免对 E2 产生 pre2022 逢化）

### 2026-06-09 批次73证据（RSI(E1-only) × C03(squeeze-only) 叠加：端到端对照；drop_bucket=0；全品种?
证据（scope=all；min_window_days=365；profile=A_universal 参数集；C03=entry_vol_state_gate_mode=2）：
- since2022：`backtest_out\stage2\indicator_audit\20260609_b73_rsi_truegate_c03_since2022_v1\b71_truegate_agg_20260609_v1.csv`
- pre2022：`backtest_out\stage2\indicator_audit\20260609_b73_rsi_truegate_c03_pre2022_v1\b71_truegate_agg_20260609_v1.csv`

==============================
BATCH_CLOSE（批?3；以证据拍板?==============================
- since2022：avg_delta_net_pnl?938.40；avg_delta_final_max_dd_pct?0.00725（dd 变小?- pre2022：avg_delta_net_pnl?211.12；avg_delta_final_max_dd_pct?0.00519（dd 变小?pnl 逢化）
- 结论（v0）：?C03 叠加时收益侧分段不稳（pre2022 逢化）?暂不把RSI gate + C03”作为可推广组合；仅保留为研究侧可叠加（偏风险侧?
### 2026-06-09 批次74证据（RSI(E1-only) × C07(squeeze + kd_3tf) 叠加：端到端对照；drop_bucket=0；全品种?
证据（scope=all；min_window_days=365；profile=A_universal 参数集；C07=C03 + enable_entry_kd_3tf_gate=1）：
- since2022：`backtest_out\stage2\indicator_audit\20260609_b74_rsi_truegate_c07_since2022_v1\b71_truegate_agg_20260609_v1.csv`
- pre2022：`backtest_out\stage2\indicator_audit\20260609_b74_rsi_truegate_c07_pre2022_v1\b71_truegate_agg_20260609_v1.csv`

==============================
BATCH_CLOSE（批?4；以证据拍板?==============================
- since2022：avg_delta_net_pnl?1350.94；avg_delta_final_max_dd_pct?0.01160（dd 变小?- pre2022：avg_delta_net_pnl?395.60；avg_delta_final_max_dd_pct?0.01197（dd 变小?pnl 逢化）
- 结论（v0）：?C07 叠加同样出现 pre2022 收益侧??暂不晋升“叠加组合；仅保留为研究侧风险压制备?
### 2026-06-09 批次75证据（RSI(E1-only) ?gate：core6 部署池视角；drop_bucket=0?
证据?- since2022：`backtest_out\stage2\indicator_audit\20260609_b75_rsi_truegate_core6_since2022_v1\b71_truegate_agg_20260609_v1.csv`
- pre2022：`backtest_out\stage2\indicator_audit\20260609_b75_rsi_truegate_core6_pre2022_v1\b71_truegate_agg_20260609_v1.csv`

==============================
BATCH_CLOSE（批?5；以证据拍板?==============================
- since2022（symbols=6）：avg_delta_net_pnl?7873.48；avg_delta_final_max_dd_pct?0.01606（dd 变小?- pre2022（symbols=3）：avg_delta_net_pnl?1204.26；avg_delta_final_max_dd_pct?0.00420（dd 变小?pnl 逢化）
- 结论（v0）：在纯 core6 范围内样本太小且 pre2022 逢??不单独晋升core6 专用门槛?
### 2026-06-09 批次76证据（RSI(E1-only) ?gate：core6+observe7 部署池视角；drop_bucket=0?
证据?- since2022：`backtest_out\stage2\indicator_audit\20260609_b76_rsi_truegate_coreobs_since2022_v1\b71_truegate_agg_20260609_v1.csv`
- pre2022：`backtest_out\stage2\indicator_audit\20260609_b76_rsi_truegate_coreobs_pre2022_v1\b71_truegate_agg_20260609_v1.csv`

==============================
BATCH_CLOSE（批?6；以证据拍板?==============================
- since2022（symbols=13）：avg_delta_net_pnl?3913.76；avg_delta_final_max_dd_pct?0.00848（dd 变小?- pre2022（symbols=10）：avg_delta_net_pnl?875.46；avg_delta_final_max_dd_pct?0.00068（dd 略变小）
- 结论（v0）：?core6+observe7 视角，两段都支持 ?这比?core6 更像可讨论的部署池口?
### 2026-06-09 XBreaking.ex5 / ex4 朢小测试结论（MT5 环境探针?
已完成：
- 确认本机 MT5 链路存在：`D:\Work\MT5\terminal64.exe`、`D:\Work\MT5\MetaEditor64.exe`
- 确认数据目录：`C:\Users\91883\AppData\Roaming\MetaQuotes\Terminal\AC48B16F101CC6359ADC4B870ED6B744`
- 已把 `XBreaking.ex5` 复制?`MQL5\Indicators\XBreaking.ex5`
- 已创建并成功编译朢小探?EA?  - 源码：`d:\Stock\trading_analysis\XBreakingProbe.mq5`
  - 编译日志：`backtest_out\stage2\indicator_audit\20260609_xbreaking_probe_compile_repo.log`
  - 配置：`d:\Stock\trading_analysis\XBreakingProbe.ini`

结论（当前轮）：
- ex5 本身可作?MT5 指标文件放入 `MQL5\Indicators`
- 探针 EA 可编译，说明“调用链脚手架已搭好
- 重新?MT5 关闭后重跑：tester 已真实起跑并成功结束（见 terminal 日志?- probe 结果：`Common\Files\XBreaking_probe_EURUSD_H1_20250101_220500.csv`
  - `handle=10 / init_err=0`
  - `buffer0: copied=200, err=0`
  - `buffer1..7: copied=-1, err=4806`
- 结论（当前可证实口径）：`XBreaking.ex5` 能在 MT5 中被 `iCustom` 成功加载；当前至少存在可?buffer0，其?buffer 是否存在/有要等后续按参数或可视化再深?- ex4 属于 MT4 编译产物，不能直接在 MT5 中作?`iCustom` 指标测试

### 2026-06-09 MT4 指标链路朢小结论（源码编译口径?
证据?- `backtest_out\stage2\indicator_audit\20260609_mt_compile\MT4IndicatorProbe_mt4_compile.log`
- `backtest_out\stage2\indicator_audit\20260609_mt_compile\VoltyChannel_Stop_v2_1M_mt4_compile.log`
- `backtest_out\stage2\indicator_audit\20260609_mt_compile\0_Harmony_06_mt4_compile_v2.log`
- `backtest_out\stage2\indicator_audit\20260609_mt_compile\a_ZZ_mt4_compile_v2.log`
- `backtest_out\stage2\indicator_audit\20260609_mt_compile\ZUP_v15_1__1_.1_mt4_compile.log`

结论（当前轮）：
- 可直接编译过?  - `VoltyChannel_Stop_v2_1M.mq4`
  - `ZUP_v15[1][1].1.mq4`
  - `0_Harmony_06.mq4`（已修掉 `long` 变量名与新编译器冲突?  - `a_ZZ.mq4`（已修掉 `long` 变量名与新编译器冲突?- `XBreaking.ex4` 为仅二进?MT4 指标：当前仓库内无法源码级审查；理论上可?MT4 使用，但本轮未拿到自?tester ?probe 产物
- MT4 自动 tester 已过 portable + 登录上下?+ 本地 history 映射真实起跑?  - smoke：`tester\files\smoke_moving_average_portable.htm`
  - Volty：`tester\files\mt4probe_volty_portable.htm`
  - tester log：`03_MT4便携探针实例\tester\logs\20260609.log`
- 2026-06-10 补证据：`MT4Probe_Volty` ?CSV 已真实落盘，说明 MT4 probe 链路已打通：
  - CSV：`03_MT4便携探针实例\tester\files\MT4_probe_Volty_EURUSD_H4_20250102_000000.csv`
  - 日志：`03_MT4便携探针实例\tester\logs\20260610.log`
  - 关键结果：mode1/mode4/mode5/mode6/mode7 可读；mode0/mode2/mode3 为空但无报错；`used_common=0`，说明本次直接写?tester 本地 `tester\files`

### 2026-06-09 批次77证据（RSI(E1-only) × C03：core6+observe7 视角；drop_bucket=0?
证据?- since2022：`backtest_out\stage2\indicator_audit\20260609_b77_rsi_truegate_coreobs_c03_since2022_v1\b71_truegate_agg_20260609_v1.csv`
- pre2022：`backtest_out\stage2\indicator_audit\20260609_b77_rsi_truegate_coreobs_c03_pre2022_v1\b71_truegate_agg_20260609_v1.csv`

==============================
BATCH_CLOSE（批?7；以证据拍板?==============================
- since2022（symbols=13）：avg_delta_net_pnl?1410.19；avg_delta_final_max_dd_pct?0.00972（dd 变小?- pre2022（symbols=10）：avg_delta_net_pnl?1938.48；avg_delta_final_max_dd_pct?0.01029（dd 变小?- 结论（v0）：?core6+observe7 视角，与 C03 叠加两段都支??可列为部署池研究候组合?
### 2026-06-09 批次78证据（RSI(E1-only) × C07：core6+observe7 视角；drop_bucket=0?
证据?- since2022：`backtest_out\stage2\indicator_audit\20260609_b78_rsi_truegate_coreobs_c07_since2022_v1\b71_truegate_agg_20260609_v1.csv`
- pre2022：`backtest_out\stage2\indicator_audit\20260609_b78_rsi_truegate_coreobs_c07_pre2022_v1\b71_truegate_agg_20260609_v1.csv`

==============================
BATCH_CLOSE（批?8；以证据拍板?==============================
- since2022（symbols=13）：avg_delta_net_pnl?1132.80；avg_delta_final_max_dd_pct?0.01338（dd 变小?- pre2022（symbols=10）：avg_delta_net_pnl?1563.65；avg_delta_final_max_dd_pct?0.01745（dd 变小?- 结论（v0）：?core6+observe7 视角，与 C07 叠加两段都支持；风险压制更明??与批?7并列为部署池研究候组?
### 2026-06-09 批次79证据（RSI(E1-only) × C03：core6 视角；drop_bucket=0?
证据?- since2022：`backtest_out\stage2\indicator_audit\20260609_b79_rsi_truegate_core6_c03_since2022_v1\b71_truegate_agg_20260609_v1.csv`
- pre2022：`backtest_out\stage2\indicator_audit\20260609_b79_rsi_truegate_core6_c03_pre2022_v1\b71_truegate_agg_20260609_v1.csv`

==============================
BATCH_CLOSE（批?9；以证据拍板?==============================
- since2022（symbols=6）：avg_delta_net_pnl?377.97；avg_delta_final_max_dd_pct?0.00849（dd 变小?- pre2022（symbols=3）：avg_delta_net_pnl?453.30；avg_delta_final_max_dd_pct?0.00891（dd 变小?- 结论（v0）：?core6 视角，与 C03 叠加两段都支持；相较批次75?pure core6，组合口径更??可列为core6 研究候组合?
### 2026-06-09 批次80证据（RSI(E1-only) × C07：core6 视角；drop_bucket=0?
证据?- since2022：`backtest_out\stage2\indicator_audit\20260609_b80_rsi_truegate_core6_c07_since2022_v1\b71_truegate_agg_20260609_v1.csv`
- pre2022：`backtest_out\stage2\indicator_audit\20260609_b80_rsi_truegate_core6_c07_pre2022_v1\b71_truegate_agg_20260609_v1.csv`

==============================
BATCH_CLOSE（批?0；以证据拍板?==============================
- since2022（symbols=6）：avg_delta_net_pnl?451.90；avg_delta_final_max_dd_pct?0.00772（dd 变小?- pre2022（symbols=3）：avg_delta_net_pnl?1025.30；avg_delta_final_max_dd_pct?0.01283（dd 变小?- 结论（v0）：?core6 视角，与 C07 叠加呈收?回撤分裂”结构：since2022 支持、pre2022 明显逢化；因此不如批次79稳定，不列为 core6 通用候组?
### 2026-06-10 批次76/77/78补充（RSI(E1-only) / ×C03 / ×C07：全屢 scope=all 复跑?
证据?- 批次76（RSI(E1-only) ?gate；全屢）：
  - since2022：`backtest_out\stage2\indicator_audit\20260610_b76_rsi_truegate_all_since2022_v1\b71_truegate_agg_20260610_v1.csv`
  - pre2022：`backtest_out\stage2\indicator_audit\20260610_b76_rsi_truegate_all_pre2022_v1\b71_truegate_agg_20260610_v1.csv`
- 批次77（RSI(E1-only) × C03；全屢）：
  - since2022：`backtest_out\stage2\indicator_audit\20260610_b77_rsi_truegate_all_c03_since2022_v1\b71_truegate_agg_20260610_v1.csv`
  - pre2022：`backtest_out\stage2\indicator_audit\20260610_b77_rsi_truegate_all_c03_pre2022_v1\b71_truegate_agg_20260610_v1.csv`
- 批次78（RSI(E1-only) × C07；全屢）：
  - since2022：`backtest_out\stage2\indicator_audit\20260610_b78_rsi_truegate_all_c07_since2022_v1\b71_truegate_agg_20260610_v1.csv`
  - pre2022：`backtest_out\stage2\indicator_audit\20260610_b78_rsi_truegate_all_c07_pre2022_v1\b71_truegate_agg_20260610_v1.csv`

COMMAND（可复现）：
- 批次76?  - `.\.venv\Scripts\python.exe .\backtest_p0.py b71-rsi-truegate-sweep --date 20260610 --scope all --split since2022 --drop_bucket 0 --entry-rsi-gate-scope e1 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b76_rsi_truegate_all_since2022_v1`
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b71-rsi-truegate-sweep --date 20260610 --scope all --split pre2022 --drop_bucket 0 --entry-rsi-gate-scope e1 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b76_rsi_truegate_all_pre2022_v1`
- 批次77?  - `.\.venv\Scripts\python.exe .\backtest_p0.py b71-rsi-truegate-sweep --date 20260610 --scope all --split since2022 --drop_bucket 0 --entry-rsi-gate-scope e1 --entry-vol-state-gate-mode 2 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b77_rsi_truegate_all_c03_since2022_v1`
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b71-rsi-truegate-sweep --date 20260610 --scope all --split pre2022 --drop_bucket 0 --entry-rsi-gate-scope e1 --entry-vol-state-gate-mode 2 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b77_rsi_truegate_all_c03_pre2022_v1`
- 批次78?  - `.\.venv\Scripts\python.exe .\backtest_p0.py b71-rsi-truegate-sweep --date 20260610 --scope all --split since2022 --drop_bucket 0 --entry-rsi-gate-scope e1 --entry-vol-state-gate-mode 2 --enable-entry-kd-3tf-gate 1 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b78_rsi_truegate_all_c07_since2022_v1`
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b71-rsi-truegate-sweep --date 20260610 --scope all --split pre2022 --drop_bucket 0 --entry-rsi-gate-scope e1 --entry-vol-state-gate-mode 2 --enable-entry-kd-3tf-gate 1 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b78_rsi_truegate_all_c07_pre2022_v1`

BATCH_CLOSE（补充裁决）?- 批次76（全屢）：
  - since2022（symbols=32）：avg_delta_net_pnl?59.72；avg_delta_final_max_dd_pct?0.00157
  - pre2022（symbols=28）：avg_delta_net_pnl?448.74；avg_delta_final_max_dd_pct?0.00095
  - symbol 计数：since2022 `pnl_pos=14/32, dd_better=16/32, both=12/32`；pre2022 `10/28, 9/28, 7/28`
  - 结论：全屢复跑后不再支持用部署池口径；仅保留在 core6+observe7 视角曾偏正的历史备注，不做全屢晋升
- 批次77（全屢）：
  - since2022（symbols=32）：avg_delta_net_pnl?1363.51；avg_delta_final_max_dd_pct?0.00436
  - pre2022（symbols=28）：avg_delta_net_pnl?561.54；avg_delta_final_max_dd_pct?0.00225
  - symbol 计数：since2022 `pnl_pos=18/32, dd_better=19/32, both=14/32`；pre2022 `15/28, 17/28, 14/28`
  - 结论：全屢口径下变成since2022 收益/回撤都偏正，pre2022 回撤改善但收益均值化的分裂结构；因此只保留?`RESEARCH_COMBO / DIAG_ONLY`，不列入通用 shortlist
- 批次78（全屢）：
  - since2022（symbols=32）：avg_delta_net_pnl?1283.63；avg_delta_final_max_dd_pct?0.00532
  - pre2022（symbols=28）：avg_delta_net_pnl?1010.71；avg_delta_final_max_dd_pct?0.00288
  - symbol 计数：since2022 `pnl_pos=18/32, dd_better=19/32, both=15/32`；pre2022 `15/28, 16/28, 13/28`
  - 结论：全屢口径下仍呈防守更强但 pre2022 收益逢化更明显”的结构；比批次77更偏防守 trade-off，同样只保留?`RESEARCH_COMBO / DIAG_ONLY`
- 统一裁决?  - 批次76/77/78 的旧结论仅在 `core6+observe7` 屢部口径成立，不再外推为全屢可保留?  - 若后续重弢，只值得讨论 `77 vs 78` ?`since2022` 或特?regime 下的条件化使用，不再讨论通用晋升

### 2026-06-10 通用 shortlist 收缩（基?93/94/95/96/97 ?76/77/78 全局复跑?
收缩目标?- 把局部口径成立但全局不稳”的条目统一移出 `UNIVERSAL_SHORTLIST`
- 把本轮已经完成全屢复跑且结论明确降级的项，写入 `DEPRECATE_LIST / SHORTLIST_REMOVED`

本轮保留? 项）?- `sv_atr_ratio_1h`
- `atr`
- `e1_break_strength_atr`
- `entry_score`
- `diag_session_skew_ratio`
- `sv_swing_present_4h`
- `ab_always_in_agree_side_1h`

本轮统一移出 shortlist?- `entry_session`：不再作为用候；仅保?`London=弱ADD标签 / NY=RISK_CONTEXT_HINT`
- `volty_trend_align_1h`：不再作为用候；冻结?`RISK_CONTEXT / EXIT_CONTEXT_HINT`
- `volty_stop_dist_bucket_1h`：不再作?sizing / shortlist 候；冻结?`FROZEN_DIAG_ONLY`
- `RSI(E1-only) ?gate` 的全屢候口径：不再成立
- `RSI(E1-only) × C03 / × C07` 的全屢候组合口径：降级?`RESEARCH_COMBO / DIAG_ONLY`

收缩统计?- `UNIVERSAL_SHORTLIST` 当前条数?
- 本轮新增 `DEPRECATE`?

落盘同步?- `02_阶段二_工作方向_想法?md`：已更新 `UNIVERSAL_SHORTLIST_V1 / SHORTLIST_REMOVED_20260610 / DEPRECATE_LIST_V0`
- `03_阶段二_当下计划_执行清单.md`：已更新“本周收缩状态（2026-06-10）?
### 2026-06-10 剩余 shortlist 缺口盘点

盘点对象（当?7 项）?- `sv_atr_ratio_1h / atr / e1_break_strength_atr / entry_score / diag_session_skew_ratio / sv_swing_present_4h / ab_always_in_agree_side_1h`

缺口分级?- DONE（已完成统一复裁）：
  - `entry_score`：批?8 已完?`scope=all + since2022/pre2022 + trade-level MAE/max_dd` 统一复裁；正式从 `ENTRY_FILTER_SWEETSPOT` 降级?`RISK_ONLY`，shortlist 合约已稳定?- P1（仍有晋升可能，但缺统一风险/条件化证据）?  - `sv_atr_ratio_1h`：since2022 已补 MAE，方向成立；?pre2022 的统丢 MAE/max_dd ?`regime/risk` 条件分层?  - `atr`：RISK_ONLY 稳定；缺统一 trade-level `MAE/max_dd`，尚未完全说清高 ATR 是否只是更赚但更痛苦”?  - `ab_always_in_agree_side_1h`：已?MAE/max_dd，但 pooled `frac_all3` 仍明显低于硬门槛；缺条件化子环境定位?  - `diag_session_skew_ratio`：画像层证据强；缺交易级映射，仍不能从画像直接晋升门?减仓?- P2（结论大体稳，只差边际价值确认）?  - `e1_break_strength_atr`：trade-off 已稳定；仅当能找?`regime/risk` 下更赚且不更痛苦”的片段时才值得继续?  - `sv_swing_present_4h`：证据最完整；只差与现有 shortlist 字段的增量解?边际贡献验证?
建议顺序?- 先做 `sv_atr_ratio_1h / atr` 的统丢风险口径
- 然后?`ab_always_in_agree_side_1h / diag_session_skew_ratio`
- 朢后才?`e1_break_strength_atr / sv_swing_present_4h` 是否还得追加

### 2026-06-10 批次98证据（entry_score 统一复裁?
证据?- `backtest_out\stage2\indicator_audit\20260610_b98_entry_score_recuts_all_since2022_v1\*`
- `backtest_out\stage2\indicator_audit\20260610_b98_entry_score_recuts_all_pre2022_v1\*`
- 复现命令?  - `.\.venv\Scripts\python.exe .\backtest_p0.py b98-entry-score-recuts --date 20260610 --scope all --split since2022 --min_n 20 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b98_entry_score_recuts_all_since2022_v1`
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b98-entry-score-recuts --date 20260610 --scope all --split pre2022 --min_n 20 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b98_entry_score_recuts_all_pre2022_v1`

关键修复?- `b98` 初版只把 `entry_score` 合并?trade-level，未带入 `atr`，导?`trade_mae_atr / trade_max_drawdown_atr` 全空?- 已修?`_trade_level_merged_for_features(..., ["entry_score", "atr"])`，重跑后两段 `coverage.priced_pct` 均恢复到 1.0，风险列已打通?
统一复裁摘要?- since2022?  - `high_vs_mid`：`frac_pnl_better?.566`，但 `frac_mae_better?.616 / frac_max_dd_better?.515` 都指?`mid_bin3_8` 更稳；仅 `stop_loss` 不支持把 mid 当成稳定甜区?  - `low_vs_mid`：`frac_pnl_better?.590 / frac_stop_loss_better?.770` 指向 `mid_bin3_8` 效率更高，但 `frac_mae_better?.250 / frac_max_dd_better?.380` 说明低分端更抗痛苦?  - `low_vs_high`：`frac_stop_loss_better?.758` 偏向高分端，?`frac_mae_better?.273 / frac_max_dd_better?.394` 偏向低分端?- pre2022?  - `high_vs_mid`：`frac_mae_better?.651 / frac_max_dd_better?.540` 继续偏向 `mid_bin3_8` 更稳，`stop_loss` 仍不支持稳定甜区叙事?  - `low_vs_mid`：`frac_pnl_better?.391 / frac_stop_loss_better?.516 / frac_mae_better?.297 / frac_max_dd_better?.516`，方向继续混杂?  - `low_vs_high`：`frac_pnl_better?.349 / frac_stop_loss_better?.683 / frac_mae_better?.286 / frac_max_dd_better?.476`，仍是风险风格差异，不是单一优区?
裁决?- `entry_score` 正式降级?`RISK_ONLY`，不再保?`ENTRY_FILTER_SWEETSPOT` 叙事?- 理由：统丢口径下，`low / mid / high` 三段长期呈现“收益止损率、MAE、max_dd` 彼此拉扯”的分层结构，没有哪个区间能在两个时间窗里稳定满足更赚且不更痛苦”?- 允许保留的唯丢用法：极端低?高分的风险分层预警或轻量减仓提示?- 不允许的外推：把 `entry_score` 当成通用 sweetspot gate，或写成“越高越?越低越好”的线门控?
### 2026-06-10 多AI收口（v91/v92/v93?
证据?- 回帖来源：`临时粘贴区_外部AI与终端输?md`
- 新增实跑?  - `backtest_out\stage2\indicator_audit\20260610_b99_swing_present_marginal_all_since2022_v1\*`
  - `backtest_out\stage2\indicator_audit\20260610_b99_swing_present_marginal_all_pre2022_v1\*`
- 复现命令?  - `.\.venv\Scripts\python.exe .\backtest_p0.py b99-swing-present-marginal --date 20260610 --scope all --split since2022 --min_n 20 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b99_swing_present_marginal_all_since2022_v1`
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b99-swing-present-marginal --date 20260610 --scope all --split pre2022 --min_n 20 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b99_swing_present_marginal_all_pre2022_v1`

PANEL_VOTE_TSV:
- `v91_RISK_FAMILY`
  - `kimi`: `Q1=C; Q2=B`
  - `deepseek`: `Q1=C; Q2=B`
  - `豆包`: `Q1=C; Q2=C`
- `v92_CONTEXT_FAMILY`
  - `kimi`: `Q1=B; Q2=C`
  - `deepseek`: `Q1=B; Q2=A`
  - `豆包`: `Q1=C; Q2=B`
- `v93_INCREMENTAL_FAMILY`
  - `kimi`: `Q1=B; Q2=B`
  - `deepseek`: `Q1=B; Q2=B`
  - `豆包`: `Q1=B; Q2=B`

DIFF_NOTES:
- `v91` 基本无分歧：3/3 都要求把 `sv_atr_ratio_1h + atr` 打包做统丢风险复裁；仅?`sv_atr_ratio_1h` 朢终能否保留弱过滤”存?`B/C` 差异，所?repo_action 采取保守口径：先不晋升，等统丢 `MAE/max_dd × regime/risk` 结果后再决定?`ENTRY_FILTER_CANDIDATE` 还是 `RISK_ONLY`?- `v92` 分歧集中在角色，而不是下丢步动作：都同?`diag_session_skew_ratio` ?trade-level 映射优先级更高，`agree_side` 只得做局部环境验证；repo_action=保留 `diag_session_skew_ratio=REDUCE_CANDIDATE`，`agree_side` 暂不硬降级，但下丢轮只允许找局部片段，不再讨论通用硬门控?- `v93` 无实质分歧：3/3 都支持先?`swing_present` 的边际贡献验证，并停止给 `break_strength` 继续争取晋升资源”；repo_action=新增批次99实跑后立刻收口?
BATCH_CLOSE:
- `v91_RISK_FAMILY`?  - 批次100证据?    - `backtest_out\stage2\indicator_audit\20260610_b100_risk_family_recuts_all_since2022_v1\*`
    - `backtest_out\stage2\indicator_audit\20260610_b100_risk_family_recuts_all_pre2022_v1\*`
    - 复现命令?      - `.\.venv\Scripts\python.exe .\backtest_p0.py b100-risk-family-recuts --date 20260610 --scope all --split since2022 --min_n 20 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b100_risk_family_recuts_all_since2022_v1`
      - `.\.venv\Scripts\python.exe .\backtest_p0.py b100-risk-family-recuts --date 20260610 --scope all --split pre2022 --min_n 20 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b100_risk_family_recuts_all_pre2022_v1`
  - 关键结果?    - `atr`?      - since2022 `risk=1 + regime!=0`：`high_vs_mid` ?`frac_pnl_better?.671`，但 `frac_stop_loss_better?.443 / frac_mae_better?.529 / frac_max_dd_better?.386`，仍是更赚但不更稳的风险 trade-off?      - pre2022 `risk=1 + regime!=0`：`high_vs_mid` ?`0.551 / 0.531 / 0.286 / 0.327`，收益与痛苦继续拉扯?      - 结论：`atr` 继续固定?`RISK_ONLY`?    - `sv_atr_ratio_1h`?      - since2022 `risk=1 + regime!=0`：`high_vs_mid` 的group_b=mid 更好”比例仅 `pnl?.477 / stop?.169 / mae?.108 / max_dd?.169`，说明高档位整体优于 mid；`low_vs_high` 中高档位对低档位优势更强?      - pre2022 `risk=1 + regime!=0`：`high_vs_mid` 的mid 更好”比例仅 `0.381 / 0.214 / 0.333 / 0.310`，再次支持高档位优于 mid；`low_vs_high` 中高档位继续明显优于低档位?      - ?`risk=0 + regime=0` 片段不稳定，无法支持无条件高更好”?  - 裁决：`sv_atr_ratio_1h` 不再保留无条件弱门槛叙事，收窄为 `risk=1 + regime!=0` 下的条件?`ENTRY_FILTER_CANDIDATE`；`atr` 固定?`RISK_ONLY`?  - 下一步：`v91` 收口完成，后续切?`diag_session_skew_ratio` ?trade-level 映射，不再重复为 `atr` 家族补同类证据?- `v92_CONTEXT_FAMILY`?  - 批次101证据?    - `backtest_out\stage2\indicator_audit\20260610_b101_diag_session_skew_tradelevel_all_since2022_v1\*`
    - `backtest_out\stage2\indicator_audit\20260610_b101_diag_session_skew_tradelevel_all_pre2022_v1\*`
    - 复现命令?      - `.\.venv\Scripts\python.exe .\backtest_p0.py b101-diag-session-skew-tradelevel --date 20260610 --scope all --split since2022 --min_n 20 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b101_diag_session_skew_tradelevel_all_since2022_v1`
      - `.\.venv\Scripts\python.exe .\backtest_p0.py b101-diag-session-skew-tradelevel --date 20260610 --scope all --split pre2022 --min_n 20 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b101_diag_session_skew_tradelevel_all_pre2022_v1`
  - 关键结果?    - since2022?      - `bin1_vs_bin4`：`frac_pnl_better=1.0 / frac_stop_loss_better=1.0 / frac_hold_better?.333 / frac_mae_better?.667`
      - `bin1_vs_rest`：`frac_pnl_better=1.0 / frac_stop_loss_better=1.0 / frac_hold_better=0.0 / frac_mae_better?.667`
    - pre2022?      - `bin1_vs_bin4`：`frac_pnl_better=1.0 / frac_stop_loss_better?.333 / frac_hold_better=0.0 / frac_mae_better=0.0`
      - `bin1_vs_rest`：`frac_pnl_better=1.0 / frac_stop_loss_better?.333 / frac_hold_better=0.0 / frac_mae_better=0.0`
    - 解释：`q4_bin1` 在两个窗口里都稳定对应更?avg_pnl，但 `stop_loss / MAE / hold_hours` 的劣势只?since2022 部分成立，pre2022 不足以支持更硬的风险门控?  - 裁决：`diag_session_skew_ratio` 维持 `REDUCE_CANDIDATE`，但口径固定为弱 reduce / 降优先级提示”，不晋升硬 reduce gate?  - 当前角色：`diag_session_skew_ratio=REDUCE_CANDIDATE` 已收口；`ab_always_in_agree_side_1h` 保留但只许讨论局部子环境，不再讨论用 gate?  - 下一步：`v92` ?skew 映射已完成，后续直接切到 `agree_side × regime/risk × MAE/max_dd` 的局部片段验证?- `v93_INCREMENTAL_FAMILY`?  - 批次99结果?    - since2022 `ALL`: `n_sufficient=65 / frac_pnl_better?.462 / frac_stop_loss_better?.615 / frac_both?.415`
    - pre2022 `ALL`: `n_sufficient=12 / frac_pnl_better?.583 / frac_stop_loss_better?.667 / frac_both?.500`
    - `regime!=0 + mid_bin3_8 + bs_bin=na`?      - since2022：`n_sufficient=11 / frac_pnl_better?.636 / frac_stop_loss_better?.818 / frac_both?.636`
      - pre2022：`n_sufficient=6 / frac_pnl_better?.667 / frac_stop_loss_better?.667 / frac_both?.667`
  - 裁决：`sv_swing_present_4h` 保留为条件型 `ADD_CANDIDATE`，但条件收窄?`regime!=0 + entry_score=mid_bin3_8`；`e1_break_strength_atr` 正式逢?shortlist，固定为 `DIAG_ONLY`?  - 理由：`swing_present` ?overall 上不是稳定用加分，但?`regime!=0 + score_mid` 的边际口径下，since2022 / pre2022 都保留正向痕迹；`break_strength` ?panel 与历?MAE 证据下都只表现为收益-痛苦 trade-off 标签，不再得继续争取晋升?
- `v102_AGREE_SIDE_SEGMENTS`?  - 批次102证据?    - `backtest_out\stage2\indicator_audit\20260610_b102_agree_side_segments_all_since2022_v1\*`
    - `backtest_out\stage2\indicator_audit\20260610_b102_agree_side_segments_all_pre2022_v1\*`
    - 复现命令?      - `.\.venv\Scripts\python.exe .\backtest_p0.py b102-agree-side-segments --date 20260610 --scope all --split since2022 --min_n 20 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b102_agree_side_segments_all_since2022_v1`
      - `.\.venv\Scripts\python.exe .\backtest_p0.py b102-agree-side-segments --date 20260610 --scope all --split pre2022 --min_n 20 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b102_agree_side_segments_all_pre2022_v1`
  - 关键结果?    - since2022?      - `risk=0 + regime=0`：`n_sufficient=43 / frac_pnl?.535 / frac_stop_loss?.814 / frac_mae?.674 / frac_maxdd?.721 / frac_all3?.279`
      - `risk=1 + regime!=0`：`n_sufficient=84 / frac_pnl=0.500 / frac_stop_loss?.583 / frac_mae?.583 / frac_maxdd=0.500 / frac_all3?.143`
    - pre2022?      - `risk=0 + regime=0`：`n_sufficient=17 / frac_pnl?.588 / frac_stop_loss?.588 / frac_mae?.647 / frac_maxdd?.765 / frac_all3?.294`
      - `risk=1 + regime!=0`：`n_sufficient=66 / frac_pnl?.424 / frac_stop_loss?.606 / frac_mae?.576 / frac_maxdd?.682 / frac_all3?.152`
    - overall?      - since2022：`frac_pnl?.512 / frac_stop_loss?.661 / frac_mae?.614 / frac_maxdd?.575`
      - pre2022：`frac_pnl?.458 / frac_stop_loss?.602 / frac_mae?.590 / frac_maxdd?.699`
  - 裁决：`ab_always_in_agree_side_1h` 不支持用 gate，但保留?`risk=0 + regime=0` 下的条件型弱过滤候?  - 反向裁决：`risk=1 + regime!=0` 不再保留过滤候，只保留为“同向时通常更不痛苦、但收益不稳定的诊断提示?  - 下一步：shortlist 现存缺口已清零；后续若继续推进，应切到新家族或重新开丢轮收?多AI 讨论?
### 2026-06-10 多AI收口（v103/v104/v105? 批次103去重审计

证据?- 回帖来源：`临时粘贴区_外部AI与终端输?md`
- 新增实跑?  - `backtest_out\stage2\indicator_audit\20260610_b103_trend_family_dedupe_all_since2022_v1\*`
  - `backtest_out\stage2\indicator_audit\20260610_b103_trend_family_dedupe_all_pre2022_v1\*`
- 复现命令?  - `.\.venv\Scripts\python.exe .\backtest_p0.py b103-trend-family-dedupe --date 20260610 --scope all --split since2022 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b103_trend_family_dedupe_all_since2022_v1`
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b103-trend-family-dedupe --date 20260610 --scope all --split pre2022 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b103_trend_family_dedupe_all_pre2022_v1`

PANEL_VOTE_TSV:
- `v103_TREND_FAMILY_REOPEN`
  - `kimi`: `Q1=C; Q2=A`
  - `deepseek`: `Q1=C; Q2=A`
  - `glm`: `Q1=C; Q2=A`
  - `qwen`: `Q1=B; Q2=C`
  - `豆包`: `Q1=C; Q2=A`
- `v104_RANGE_FAMILY_REOPEN`
  - `kimi`: `Q1=A; Q2=A`
  - `deepseek`: `Q1=A; Q2=A`
  - `glm`: `Q1=A; Q2=A`
  - `qwen`: `Q1=A; Q2=B`
  - `豆包`: `Q1=A; Q2=A`
- `v105_OSCILLATOR_LEFTOVERS`
  - `kimi`: `Q1=A; Q2=A`
  - `deepseek`: `Q1=A; Q2=A`
  - `glm`: `Q1=A; Q2=A`
  - `qwen`: `Q1=A; Q2=A`
  - `豆包`: `Q1=A; Q2=A`

DIFF_NOTES:
- `v103` 的主分歧不在“是否保留旧问题”，而在“先冻结还是先去重?/5 选择 `Q1=C; Q2=A`，repo_action=先做批次103 去重审计，再把问题压缩为单一动作，不再保留整组问题?- `v104` 基本无分歧：`range_trap` 永久冻结；只给纯 `range_width` 丢次最后的 `MAE/max_dd × regime/risk` 审计?- `v105` 完全丢致：`CCI/KD basic` 永久冻结，不再保留为旧问题或待讨论池?
BATCH_CLOSE:
- `v103_TREND_FAMILY_REOPEN`?  - 批次103结果?    - since2022?      - `ab_trend_strength_score_1h`：`pooled_r_trade_pnl?0.018 / pooled_r_entry_score?.356 / pooled_r_sv_atr_ratio?.030 / pooled_r_sv_regime_code?.331`
      - `ab_trendbar_strength_1h`：`pooled_r_trade_pnl?0.003 / pooled_r_entry_score?.079 / pooled_r_sv_atr_ratio?.106 / pooled_r_sv_regime_code?.014`
      - `ab_trendbar_agree_side_1h`：`pooled_r_trade_pnl?0.001 / pooled_r_entry_score?.085 / pooled_r_sv_atr_ratio?.103 / pooled_r_sv_regime_code?.022`
    - pre2022?      - `ab_trend_strength_score_1h`：`pooled_r_trade_pnl?0.028 / pooled_r_entry_score?.353 / pooled_r_sv_atr_ratio?.072 / pooled_r_sv_regime_code?.196`
      - `ab_trendbar_strength_1h`：`pooled_r_trade_pnl?0.006 / pooled_r_entry_score?.103 / pooled_r_sv_atr_ratio?.113 / pooled_r_sv_regime_code?.014`
      - `ab_trendbar_agree_side_1h`：`pooled_r_trade_pnl?0.003 / pooled_r_entry_score?.107 / pooled_r_sv_atr_ratio?.110 / pooled_r_sv_regime_code?.023`
  - 裁决?    - `ab_trendbar_strength_1h / ab_trendbar_agree_side_1h`：冻结为 `FROZEN_DIAG_ONLY`；不再保留旧问题?    - `ab_trend_strength_*`：去重审计显示不是硬别名，但全局 `pnl?`；若继续，只允许朢后一?`risk/regime × MAE/max_dd` 屢部片段验证，之后必须二一：片段成立或永久冻结?- `v104_RANGE_FAMILY_REOPEN`?  - 裁决：`ab_range_trap_score_1h / flag_1h / repeat_1h` 永久冻结?`FROZEN_DIAG_ONLY`；不再保留旧问题?  - 保留的唯丢动作：只?`ab_range_width_atr_1h / bucket` 做最后一?`MAE/max_dd × regime/risk` 审计?- `v105_OSCILLATOR_LEFTOVERS`?  - 裁决：`CCI basic / KD basic` 整组永久冻结?`FROZEN_DIAG_ONLY`；不再保留旧问题?  - 理由：RSI 全量验证后都未保住用 gate 叙事，CCI/KD 证据更弱，不再重复投入?
### 2026-06-10 批次104证据（range_width 朢后一?MAE/max_dd × risk/regime 审计?
证据?- 新增实跑?  - `backtest_out\stage2\indicator_audit\20260610_b104_range_width_segments_all_since2022_v1\*`
  - `backtest_out\stage2\indicator_audit\20260610_b104_range_width_segments_all_pre2022_v1\*`
- 复现命令?  - `.\.venv\Scripts\python.exe .\backtest_p0.py b104-range-width-segments --date 20260610 --scope all --split since2022 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b104_range_width_segments_all_since2022_v1`
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b104-range-width-segments --date 20260610 --scope all --split pre2022 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b104_range_width_segments_all_pre2022_v1`

BATCH_CLOSE:
- `ab_range_width_atr_1h / ab_range_width_bucket_1h`?  - since2022?    - `risk=0 + regime=0 + high_vs_mid`：`frac_pnl?.588 / frac_stop_loss?.706 / frac_mae?.529 / frac_max_dd?.588 / frac_all4?.118`
    - `risk=1 + regime!=0 + high_vs_mid`：`?.505 / 0.657 / 0.414 / 0.606 / 0.172`
  - pre2022?    - `risk=0 + regime=0 + low_vs_mid`：`?.514 / 0.405 / 0.622 / 0.405 / 0.135`
    - `risk=1 + regime!=0 + high_vs_mid`：`?.701 / 0.776 / 0.567 / 0.448 / 0.224`
  - `bucket` 口径?    - since2022 / pre2022 基本都没有足?pair；唯丢出现?since2022 `1` ?sufficient pair 不具备收口价值?  - 裁决?    - `ab_range_width_atr_1h / ab_range_width_bucket_1h` 永久冻结?`FROZEN_DIAG_ONLY`?    - 理由：虽然个别分段出现mid 优于 extreme”的屢部痕迹，但跨窗口 `frac_all4` 始终偏低，且 `bucket` 口径过稀，不足以保留为稳?`RISK_CONTEXT_HINT`?
### 2026-06-10 批次105证据（trend_strength 朢后一?risk/regime × MAE/max_dd 屢部片段验证）

证据?- 新增实跑?  - `backtest_out\stage2\indicator_audit\20260610_b105_trend_strength_segments_all_since2022_v1\*`
  - `backtest_out\stage2\indicator_audit\20260610_b105_trend_strength_segments_all_pre2022_v1\*`
- 复现命令?  - `.\.venv\Scripts\python.exe .\backtest_p0.py b105-trend-strength-segments --date 20260610 --scope all --split since2022 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b105_trend_strength_segments_all_since2022_v1`
  - `.\.venv\Scripts\python.exe .\backtest_p0.py b105-trend-strength-segments --date 20260610 --scope all --split pre2022 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b105_trend_strength_segments_all_pre2022_v1`

BATCH_CLOSE:
- `ab_trend_strength_score_1h / ab_trend_strength_bucket_1h`?  - since2022?    - `bucket / risk=0 + regime=0 + low_vs_mid`：`frac_pnl?.800 / frac_stop_loss?.800 / frac_mae?.800 / frac_max_dd?.800 / frac_all4?.400`，但?`n_sufficient=5`
    - `score / risk=0 + regime=0 + low_vs_mid`：`?.325 / 0.675 / 0.775 / 0.750 / 0.150`
    - `score / risk=1 + regime!=0 + high_vs_mid`：`?.561 / 0.455 / 0.500 / 0.591 / 0.106`
  - pre2022?    - `bucket / risk=0 + regime=0 + low_vs_mid`：`?.750 / 1.000 / 0.500 / 0.500 / 0.250`，但?`n_sufficient=4`
    - `score / risk=0 + regime=0 + low_vs_mid`：`?.522 / 0.783 / 0.565 / 0.652 / 0.304`
    - `score / risk=1 + regime!=0 + high_vs_mid`：`?.574 / 0.556 / 0.241 / 0.481 / 0.093`
  - 总览?    - since2022 overall：`frac_all4?.161`
    - pre2022 overall：`frac_all4?.164`
  - 裁决?    - `ab_trend_strength_score_1h / ab_trend_strength_bucket_1h` 永久冻结?`FROZEN_DIAG_ONLY`?    - 理由：局部仅?`risk=0 + regime=0` 下避弢低档”痕迹，?`bucket` 口径样本过小，`score` 口径收益侧不稳，跨窗口都达不到可保留的稳定片段阈值；朢后一次机会用完后正式冻结?
### 2026-06-10 多AI收口（v106/v107/v108/v109?
证据?- 回帖来源：`临时粘贴区_外部AI与终端输?md`
- 本地已有锚点?  - EMA family：批?4 全局补跑结论不变，`ab_ema200_side_1h / ab_ema20_gt_ema200_1h` 仅在 `risk=0,regime=0` 下保留条件化正向，其?EMA residual 无稳定晋升路?  - pullback：批?8 已确认覆盖低/过稀”是主硬?  - fib retrace：批?6 pooled `|rho(trade_pnl)|<0.01`，bucket/near 系列仅支?`DIAG_ONLY`
  - volume family：批?5 已明确当?FX/index/commodity volume 口径不稳，只保留 `REOPEN_ON_A_SHARES_EXCHANGE_VOLUME`

PANEL_VOTE_TSV:
- `v106_EMA_RESIDUAL_FAMILY`
  - `kimi`: `Q1=A; Q2=A`
  - `deepseek`: `Q1=A; Q2=A`
  - `glm`: `Q1=A; Q2=A`
  - `qwen`: `Q1=A; Q2=B`
  - `豆包`: `Q1=A; Q2=A`
- `v107_SPARSE_STATE_FAMILY`
  - `kimi`: `Q1=A; Q2=C`
  - `deepseek`: `Q1=A; Q2=C`
  - `glm`: `Q1=A; Q2=C`
  - `qwen`: `Q1=B; Q2=A`
  - `豆包`: `Q1=B; Q2=A`
- `v108_PRICE_PATTERN_FAMILY`
  - `kimi`: `Q1=A; Q2=A`
  - `deepseek`: `Q1=B; Q2=C`
  - `glm`: `Q1=B; Q2=C`
  - `qwen`: `Q1=A; Q2=A`
  - `豆包`: `Q1=A; Q2=A`
- `v109_A_SHARES_ONLY_MARKERS`
  - `kimi`: `Q1=A; Q2=A`
  - `deepseek`: `Q1=A; Q2=A`
  - `glm`: `Q1=A; Q2=A`
  - `qwen`: `Q1=A; Q2=A`
  - `豆包`: `Q1=A; Q2=A`

DIFF_NOTES:
- `v106`?  - 主分歧不在是否冻?EMA residual”，而在“若只保留一个复盘点，?`ab_ema200_side_1h` 还是 `ab_ema20_gt_ema200_1h`”?  - repo_action：按多数票与压缩原则，只保留 `ab_ema200_side_1h` ?`RISK_CONTEXT_HINT`，`ab_ema20_gt_ema200_1h` 冻结，避免同组重复占位?- `v107`?  - 3/5 主张整组冻结?/5 主张保留 `always_in_state/dir/strength` 为纯复盘标签?  - repo_action：按多数票冻结整组；理由?`agree_side` 已是同家族唯丢留存字段，再保留 residual 只会重复占位?- `v108`?  - 3/5 主张“蜡烛冻?+ 仅留 `fib_retrace_depth_1h` 观察”，2/5 主张整组冻结?  - repo_action：保?`fib_retrace_depth_1h=DIAG_ONLY` 作为唯一观察点，不再给它单独弢执行动作；其余价格形态字段冻结?- `v109`?  - 无实质分歧?  - repo_action：把依赖交易扢真实量能的字段明确移出当?FX/index/commodity 通用讨论线，转入 `A_SHARES_ONLY_FUTURE_BUCKET`?
BATCH_CLOSE:
- `v106_EMA_RESIDUAL_FAMILY`?  - `ab_ema_touch_1h / ab_ema_fake_break_1h / ab_ema_reclaim_1h / ab_ema_reclaim_score_1h / ab_ema20_slope_bucket_1h / ab_ema20_side_1h`：`FROZEN_DIAG_ONLY`
  - `ab_ema200_side_1h`：保留为唯一 `RISK_CONTEXT_HINT`，仅?`risk=0 + regime=0` 条件化复?  - `ab_ema20_gt_ema200_1h`：`FROZEN_DIAG_ONLY`
- `v107_SPARSE_STATE_FAMILY`?  - `ab_pullback_depth_atr_1h / ab_pullback_time_bars_1h / ab_pullback_end_score_1h / ab_reversal_score_1h / ab_reversal_bucket_1h / ab_reversal_flag_1h / ab_always_in_state_1h / ab_always_in_dir_1h / ab_always_in_strength_1h`：`FROZEN_DIAG_ONLY`
  - `ab_always_in_agree_side_1h`：维持既有收口，不受本轮影响
- `v108_PRICE_PATTERN_FAMILY`?  - `px_cdl_engulf_score_1h / px_cdl_engulf_flag_1h / px_cdl_pinbar_score_1h / px_cdl_pinbar_flag_1h / fib_retrace_bucket_1h / fib_retrace_near_flag_1h / fib_retrace_near_score_1h`：`FROZEN_DIAG_ONLY`
  - `fib_retrace_depth_1h`：`DIAG_ONLY`；仅保留为纯复盘观察标签，不进入新执行动?- `v109_A_SHARES_ONLY_MARKERS`?  - `wy_spring_ut_flag_1h / wy_spring_ut_score_1h / wy_spring_ut_repeat_1h / vol_ratio_bucket_1h / vol_spike_flag_1h / vol_dryup_flag_1h`：转?`A_SHARES_ONLY_FUTURE_BUCKET`
  - 长期规则：凡依赖交易扢真实量能的字段，丢律出当?FX/index/commodity 通用线，仅在 `A_SHARES_EXCHANGE_VOLUME` 接入后重弢

### 2026-06-10 多AI收口（v110/v111/v112/v113?
证据?- 回帖来源：`临时粘贴区_外部AI与终端输?md`
- 本地已有锚点?  - signal quality：批?6 已确?`score=qtiles4` 稳定性不足，`bucket` 存在 `stop_loss_rate` 改善?`MAE_ATR` 恶化的矛盾结?  - range core：批?9 已确?`ab_range_flag_1h / ab_range_score_1h` 稳定性不足；且同家族 `range_trap / range_width` 已全部冻?  - KD extended：批?7/61/63/64 已分别确?coverage 不稳健过稢或稳定偏?  - pattern leftover：批?3 已确?`ab_doji_flag_1h` 跨分段方向不稳；批次56/v108 已把 `fib_retrace_depth_1h` 降为纯复盘观?
PANEL_VOTE_TSV:
- `v110_SIGNAL_QUALITY_FAMILY`
  - `kimi`: `Q1=A; Q2=C`
  - `deepseek`: `Q1=A; Q2=C`
  - `glm`: `Q1=A; Q2=C`
  - `qwen`: `Q1=A; Q2=C`
  - `豆包`: `Q1=B; Q2=A`
- `v111_RANGE_CORE_RESIDUAL`
  - `kimi`: `Q1=A; Q2=C`
  - `deepseek`: `Q1=A; Q2=C`
  - `glm`: `Q1=A; Q2=C`
  - `qwen`: `Q1=A; Q2=C`
  - `豆包`: `Q1=A; Q2=C`
- `v112_KD_EXTENDED_FAMILY`
  - `kimi`: `Q1=A; Q2=C`
  - `deepseek`: `Q1=A; Q2=C`
  - `glm`: `Q1=A; Q2=C`
  - `qwen`: `Q1=A; Q2=C`
  - `豆包`: `Q1=A; Q2=C`
- `v113_PATTERN_LEFTOVER_OBSERVE`
  - `kimi`: `Q1=A; Q2=A`
  - `deepseek`: `Q1=A; Q2=A`
  - `glm`: `Q1=A; Q2=A`
  - `qwen`: `Q1=A; Q2=A`
  - `豆包`: `Q1=A; Q2=A`

DIFF_NOTES:
- `v110`?  - 主分歧仅?`豆包` 倾向保留 `ab_sig_quality_score_1h` 作为纯复盘标签，其余 4 票主张整组冻结?  - repo_action：按多数票冻?`ab_sig_quality_score_1h / ab_sig_quality_bucket_1h`；理由是该组已具备稳定不?+ 风险收益矛盾”的双重否决，不再占?`DIAG_POOL`?- `v111`?  - 无实质分歧?  - repo_action：`ab_range_flag_1h / ab_range_score_1h` 丢并冻结，range 家族全部收口?- `v112`?  - 无实质分歧?  - repo_action：`kd_sat / kd_div / kd_align / kd_macd_res` 整组冻结，KD 家族全部收口?- `v113`?  - 无实质分歧?  - repo_action：`ab_doji_flag_1h` 永久冻结；`fib_retrace_depth_1h` 继续仅作纯复盘观察，不开新执行动作?
BATCH_CLOSE:
- `v110_SIGNAL_QUALITY_FAMILY`?  - `ab_sig_quality_score_1h / ab_sig_quality_bucket_1h`：`FROZEN_DIAG_ONLY`
- `v111_RANGE_CORE_RESIDUAL`?  - `ab_range_flag_1h / ab_range_score_1h`：`FROZEN_DIAG_ONLY`
  - 备注：range 家族全部收口完毕
- `v112_KD_EXTENDED_FAMILY`?  - `kd_sat_favor_bucket_1h / kd_sat_unfavor_bucket_1h / kd_sat_favor_exit_1h / kd_sat_unfavor_exit_1h / kd_div_score_1h / kd_div_flag_1h / kd_align_favor_count_1h / kd_align_unfavor_count_1h / kd_macd_res_flag_1h / kd_macd_res_score_1h`：`FROZEN_DIAG_ONLY`
  - 备注：KD 家族全部收口完毕
- `v113_PATTERN_LEFTOVER_OBSERVE`?  - `ab_doji_flag_1h`：`FROZEN_DIAG_ONLY`
  - `fib_retrace_depth_1h`：`DIAG_ONLY`；仅保留为纯复盘观察标签，不进入新执行动?
### 2026-06-10 阶段切换记录（单字段阶段 -> 稳定候组合优化）

结论?- 当前 FX/index/commodity 1H 口径下，可量化单字段/单指标阶段已完成?- 之后不再新增“无边界单字段挖掘；只有在出现新增数据口径明确新证据、或用户明确要求重开时，才允许重弢旧家族?
阶段小结?- 已完成：
  - 单字?单指标的独立证据、批次收口多AI 复审、长期角色归?  - `DIAG_POOL` 大幅压缩；大多数历史字段已进?`FROZEN_DIAG_ONLY`
- 明确保留?  - 候侧：`sv_atr_ratio_1h / sv_swing_present_4h / diag_session_skew_ratio / ab_always_in_agree_side_1h / rsi_basic_*`
  - 上下文侧：`atr / entry_score / ab_ema200_side_1h`
  - 纯观察侧：`fib_retrace_depth_1h`
- 明确后置?  - `A_SHARES_ONLY_FUTURE_BUCKET`
  - `SOURCE_LIBRARY` 中仍不可量化的规则壳

心得?- 单字段阶段最重要的不是尽量多留，而是尽快识别哪些字段只能做标签哪些字段必须冻结，避免历史包袱越滚越大?- 阶段切换后，评价标准应从“单字段是否有点信息”切换为“组合后是否能稳定提升收?风险口径”?
### 2026-06-10 资料源盘点与目录整理

证据?- 总表：`docs\资料源吸收状态与目录整理方案_20260610.md`
- 目录核对结果?  - `02_mt指标测试` ?`02_MT指标家族_源码与探针` 文件名一致哈希一?  - `12_ʱ_TOOLING_RUNTIME\VTMarkets-Live 2` ?`98_MT历史数据_VTMarkets_Live2` 文件数量丢致（213?
结论?- “当前单字段阶段已完成成立，但它只覆盖当?`FX/index/commodity 1H` 下已经量化并完成证据闭环的字段?- 不能把它外推为所有资料目录都已文件完全吸收?- 资料源角色统丢如下?  - `00_指标定义&公式 / 00_大隐体系 / 00_周期女王 / 00_TK外汇 / 02_原子化拆解文件`：`SOURCE_LIBRARY` 为主
  - `00_交易系统书籍`：规则底?状模板，基本已具稳定入口
  - `03_MT4便携探针实例 / 12_ʱ_TOOLING_RUNTIME\mt4_probe_instance`：工具运行时资产
  - `98_MT历史数据_VTMarkets_Live2`：标?MT4 历史归档入口
  - `12_ʱ_TOOLING_RUNTIME\VTMarkets-Live 2`：兼容副本，暂不删除

动作?- 保留：`02_MT指标家族_源码与探针`
- 删除：`02_mt指标测试`
- 备注：组合优化阶段默认不再从来源库继续开新单字段，除非出现新增数据口径或明确重开理由

### 2026-06-10 批次81证据（RSI 部署池收缩批 + MT 指标家族映射 v1?
证据?- 批次75：`backtest_out\stage2\indicator_audit\20260609_b75_rsi_truegate_core6_since2022_v1\*`
- 批次76：`backtest_out\stage2\indicator_audit\20260609_b76_rsi_truegate_coreobs_since2022_v1\*`
- 批次77：`backtest_out\stage2\indicator_audit\20260609_b77_rsi_truegate_coreobs_c03_since2022_v1\*`
- 批次78：`backtest_out\stage2\indicator_audit\20260609_b78_rsi_truegate_coreobs_c07_since2022_v1\*`
- 批次79：`backtest_out\stage2\indicator_audit\20260609_b79_rsi_truegate_core6_c03_since2022_v1\*`
- 批次80：`backtest_out\stage2\indicator_audit\20260609_b80_rsi_truegate_core6_c07_since2022_v1\*`
- MT 指标家族映射：`00_指标定义&公式\MT指标家族映射_v1.md`

==============================
BATCH_CLOSE（批?1；以证据拍板?==============================
- 部署池收缩：`core6+observe7` 视角下，`C03/C07` 两段都支持，可继续保留为部署池研究；`core6` 视角下，`C03` 两段支持、`C07` ?since2022 支持?pre2022 明显逢化的分裂结构
- 裁决（v0）：?`core6` 只保?`RSI(E1-only) × C03` 作为研究候；`RSI(E1-only) × C07` 不列?core6 通用候组?- MT 指标家族映射（v1）：先收敛为 5 个家族：`Volty Stop / Harmonic Basic / ZZ Ratio / Harmonic Framework / Breakout Binary`
- 工程优先级（v0）：优先?`Volty Stop` 当作 `RISK/EXIT` 家族推进，再?`ZZ Ratio` 当作结构诊断标签推进；谐波类继续保留资料库定位，二进制类继续 probe/effect 验证
- 复核备注（v0）：截至本轮，连续推进与收口已做到批?1；其?81 为收缩批/工程化批”，不是新增?gate 实验?
### 2026-06-10 批次82证据（Volty Stop 字段实现 v1；core6 双窗口）

证据?- since2022?  - `backtest_out\stage2\indicator_audit\20260610_b82_volty_stop_fields_core6_since2022_v1\b82_trade_features_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b82_volty_stop_fields_core6_since2022_v1\b82_feature_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b82_volty_stop_fields_core6_since2022_v1\b82_coverage_20260610_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260610_b82_volty_stop_fields_core6_pre2022_v1\b82_trade_features_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b82_volty_stop_fields_core6_pre2022_v1\b82_feature_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b82_volty_stop_fields_core6_pre2022_v1\b82_coverage_20260610_v1.csv`
- 代码入口?  - `backtest_p0.py` 新增命令：`b82-volty-stop-fields`

==============================
BATCH_CLOSE（批?2；以证据拍板?==============================
- 实现状：`Volty Stop` 已从文档草案进入代码实现；当前可落盘字段包括 `volty_center_ma_1h / volty_band_upper_1h / volty_band_lower_1h / volty_trend_state_1h / volty_flip_flag_1h / volty_active_stop_1h / volty_stop_dist_atr_1h / volty_band_width_pct_1h / volty_trend_align_1h / volty_stop_dist_bucket_1h`
- since2022（core6）：
  - coverage ?100%
  - `volty_trend_align_1h` ?mean_top_minus_bot≈`+20.51`，更像顺?逆势上下文标签?  - `volty_stop_dist_atr_1h` ?mean_top_minus_bot≈`-248.85`，说明离活动止损越远”在 since2022 整体更差
  - `volty_band_width_pct_1h` ?mean_top_minus_bot≈`-234.51`，宽通道并不稳定占优
- pre2022（core6）：
  - `volty_trend_align_1h` mean_top_minus_bot≈`+65.54`
  - `volty_stop_dist_atr_1h` mean_top_minus_bot≈`+227.32`
  - `volty_band_width_pct_1h` mean_top_minus_bot≈`+345.78`
  - ?since2022 出现明显分裂，说?`Volty` 更合作为 `RISK/EXIT/DIAG` 组件，不是直接升格为通用?gate
- 结论（v1）：`Volty Stop` 字段实现可保留并继续推进，但当前只保?`RISK / EXIT / REGIME_DIAG` 角色，不进入默认 entry gate 候?- 复核备注（v1）：`coverage` 中存在同 symbol/profile 重复，是因为 `p0_sweep` 下存在多份历?run 并被丢并纳入；不影响字段落盘本身，但本?summary 先按“探索聚合解读，后续若要晋升霢补latest-run 去重口径?
### 2026-06-10 批次83证据（ZZ Ratio 字段实现 v1 + Volty latest-run 去重口径?
证据?- ZZ Ratio since2022?  - `backtest_out\stage2\indicator_audit\20260610_b83_zz_ratio_fields_core6_since2022_v1\b83_trade_features_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b83_zz_ratio_fields_core6_since2022_v1\b83_feature_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b83_zz_ratio_fields_core6_since2022_v1\b83_coverage_20260610_v1.csv`
- ZZ Ratio pre2022?  - `backtest_out\stage2\indicator_audit\20260610_b83_zz_ratio_fields_core6_pre2022_v1\b83_trade_features_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b83_zz_ratio_fields_core6_pre2022_v1\b83_feature_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b83_zz_ratio_fields_core6_pre2022_v1\b83_coverage_20260610_v1.csv`
- Volty latest-run 去重?  - `backtest_out\stage2\indicator_audit\20260610_b82_volty_stop_fields_core6_since2022_latest_v1\b82_feature_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b82_volty_stop_fields_core6_since2022_latest_v1\b82_coverage_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b82_volty_stop_fields_core6_pre2022_latest_v1\b82_feature_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b82_volty_stop_fields_core6_pre2022_latest_v1\b82_coverage_20260610_v1.csv`

==============================
BATCH_CLOSE（批?3；以证据拍板?==============================
- ZZ Ratio 实现状：已进?`backtest_p0.py b83-zz-ratio-fields`；当前可落盘字段包括 `zz_ratio_value_1h / zz_ratio_code_1h / zz_swing_span_atr_1h / zz_pivot_count_1h`
- ZZ Ratio 结果?  - since2022：四个字段的 mean_top_minus_bot 全为负（?`-28~-98`?  - pre2022：四个字段的 mean_top_minus_bot 全为正（?`+163~+544`?  - 结论（v1）：`ZZ Ratio` 跨窗口分裂明显，只保?`DIAG_ONLY`，不进入 shortlist，不进入默认门控
- Volty latest-run 去重?  - 后续已用修复后的 CLI 完成 strict `latest_only=1` 重跑?    - `backtest_out\stage2\indicator_audit\20260610_b82_volty_stop_fields_core6_since2022_latest_strict_v2\*`
    - `backtest_out\stage2\indicator_audit\20260610_b82_volty_stop_fields_core6_pre2022_latest_strict_v2\*`
  - strict latest-only 下，`coverage` 已收敛为每个 `symbol/split/profile` 丢条；核心结论未改?  - 结论（v1）：`Volty` 仍不进入通用 shortlist；但 `volty_trend_align_1h` 可保留为 `REGIME_DIAG / RISK_CONTEXT` 观察候?- 复核备注（v2）：至此 MT 指标工程化已做到批次83?2 ?Volty 字段实现批，83 ?ZZ 实现 + Volty latest-run 严格复核批；当前更合?`trend_align` 视为诊断标签而非优桶

### 2026-06-10 批次84证据（Volty trend_align followups + 0_Harmony_06 非重绘确认时点定义60?
证据?- Volty trend_align evidence?  - `backtest_out\stage2\indicator_audit\20260610_b84_volty_trend_align_core6_since2022_v1\b84_feature_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b84_volty_trend_align_core6_pre2022_v1\b84_feature_summary_20260610_v1.csv`
  - strict latest-only 复跑?    - `backtest_out\stage2\indicator_audit\20260610_b84_volty_trend_align_core6_since2022_latest_strict_v2\b84_feature_summary_20260610_v1.csv`
    - `backtest_out\stage2\indicator_audit\20260610_b84_volty_trend_align_core6_pre2022_latest_strict_v2\b84_feature_summary_20260610_v1.csv`
- Volty trend_align followups?  - `backtest_out\stage2\indicator_audit\20260610_b84_volty_trend_align_followups_core6_since2022_v1\b84_stability_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b84_volty_trend_align_followups_core6_since2022_v1\b84_stability_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b84_volty_trend_align_followups_core6_pre2022_v1\b84_stability_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b84_volty_trend_align_followups_core6_pre2022_v1\b84_stability_summary_20260610_v1.csv`
  - strict latest-only 复跑?    - `backtest_out\stage2\indicator_audit\20260610_b84_volty_trend_align_followups_core6_since2022_latest_strict_v2\b84_stability_summary_20260610_v1.csv`
    - `backtest_out\stage2\indicator_audit\20260610_b84_volty_trend_align_followups_core6_pre2022_latest_strict_v2\b84_stability_summary_20260610_v1.csv`
- Harmony 定义稿：
  - `00_指标定义&公式\MT指标家族映射_v1.md`

==============================
BATCH_CLOSE（批?4；以证据拍板?==============================
- Volty trend_align 结果?  - since2022：`top_minus_bot_avg_pnl=-123.49`，即 `align=1` 相对 `align=0` 并未形成收益优势
  - pre2022：`top_minus_bot_avg_pnl=-43.92`，方向同样不支持?`align=1` 视作优桶
  - 稳定性：since2022 `n_pairs=17 / n_sufficient=9 / frac_pnl_better=0.444 / frac_stop_loss_better=0 / frac_both=0`；pre2022 `n_pairs=8 / n_sufficient=1 / frac_both=0`
- strict latest-only 复核?  - since2022：`n_trades` 从旧聚合?`7394` 收敛?`3193`，`top_minus_bot_avg_pnl=-121.84`；followups ?`n_pairs=17 / n_sufficient=5 / frac_pnl_better=0.400 / frac_both=0`
  - pre2022：结果不变，仍为 `top_minus_bot_avg_pnl=-43.92`，followups `n_pairs=8 / n_sufficient=1 / frac_both=0`
- Volty 裁决（v1）：`volty_trend_align_1h` 继续保留?`REGIME_DIAG / RISK_CONTEXT`；不进入 shortlist，不晋升 entry gate
- Harmony 定义稿（v0）：
  - `0_Harmony_06` 扢有形态都写在 `ind[4]`，对应当前最?ZigZag pivot ?D 点；因此图上首现只能视为预警，天然带重绘风险
  - 只有当后续出现新的反?ZigZag pivot、使 D 点不再是朢?pivot，且重算?`pattern_code + D_bar` 保持不变，才视为“非重绘确认完成?  - 朢早可用时点：确认 bar 收盘后记研究标签；若未来接交易级实验，只允许下一?bar open 使用
- 复核备注（v1）：strict latest-only 已补跑完成；批次84 结论不变，只是把“待复核”升级为“已严格复核且仍不晋升?
### 2026-06-10 批次85证据（Volty trend_align × MAE / max_drawdown_per_trade 交互复核?
证据?- since2022?  - `backtest_out\stage2\indicator_audit\20260610_b85_volty_trend_align_mae_core6_since2022_latest_strict_v1\b85_volty_mae_stats_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b85_volty_trend_align_mae_core6_since2022_latest_strict_v1\b85_volty_mae_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b85_volty_trend_align_mae_core6_since2022_latest_strict_v1\b85_volty_mae_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b85_volty_trend_align_mae_core6_since2022_latest_strict_v1\b85_volty_mae_coverage_20260610_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260610_b85_volty_trend_align_mae_core6_pre2022_latest_strict_v1\b85_volty_mae_stats_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b85_volty_trend_align_mae_core6_pre2022_latest_strict_v1\b85_volty_mae_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b85_volty_trend_align_mae_core6_pre2022_latest_strict_v1\b85_volty_mae_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b85_volty_trend_align_mae_core6_pre2022_latest_strict_v1\b85_volty_mae_coverage_20260610_v1.csv`

==============================
BATCH_CLOSE（批?5；以证据拍板?==============================
- 口径说明：本批把 `trade_mae_atr` 作为 `max_drawdown_per_trade` ?1H OHLC 代理口径；用于判?`volty_trend_align_1h` 是否只是“更不容?hit stop / 更不痛苦”，还是也能带来更高收益
- since2022（strict latest-only）：
  - `n_pairs=17 / n_sufficient=5`
  - `frac_pnl_better=0.400`
  - `frac_stop_loss_better=0.800`
  - `frac_mae_better=0.800`
  - `frac_all3_better=0.400`
  - 含义：`align=1` 更常见的是MAE 更低、止损率更低”，但收益并不占优；它更像风?痛苦度标签，而不是收益优选桶
- pre2022（strict latest-only）：
  - `n_pairs=8 / n_sufficient=1`
  - 唯一 sufficient pair 同时支持 pnl / stop_loss / mae，但样本不足，不足以改写全局角色
- 结论（v1）：`volty_trend_align_1h` 可加强为 `REGIME_DIAG / RISK_CONTEXT` 的风险侧证据，但仍不进入 shortlist，不晋升 entry gate；若未来继续推进，只能往 `sizing / reduce / exit context` 方向补证据，不能反向解读成用入场过滤

### 2026-06-10 批次86证据（Volty align × stop_dist_bucket × MAE?
证据?- since2022?  - `backtest_out\stage2\indicator_audit\20260610_b86_volty_align_stopdist_mae_core6_since2022_latest_strict_v1\b86_volty_stopdist_mae_stats_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b86_volty_align_stopdist_mae_core6_since2022_latest_strict_v1\b86_volty_stopdist_mae_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b86_volty_align_stopdist_mae_core6_since2022_latest_strict_v1\b86_volty_stopdist_mae_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b86_volty_align_stopdist_mae_core6_since2022_latest_strict_v1\b86_volty_stopdist_mae_coverage_20260610_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260610_b86_volty_align_stopdist_mae_core6_pre2022_latest_strict_v1\b86_volty_stopdist_mae_stats_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b86_volty_align_stopdist_mae_core6_pre2022_latest_strict_v1\b86_volty_stopdist_mae_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b86_volty_align_stopdist_mae_core6_pre2022_latest_strict_v1\b86_volty_stopdist_mae_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b86_volty_align_stopdist_mae_core6_pre2022_latest_strict_v1\b86_volty_stopdist_mae_coverage_20260610_v1.csv`

==============================
BATCH_CLOSE（批?6；以证据拍板?==============================
- 口径说明：本批在同一 `volty_trend_align_1h` 内，?`volty_stop_dist_bucket_1h` 合并?`stop_bucket<=1` vs `stop_bucket>=2`，并继续?`trade_mae_atr` 代理 `max_drawdown_per_trade`；目标是判断 stop_dist 是否能提?sizing / reduce 价?- since2022（strict latest-only）：
  - 汇：`align=0` ?`n_pairs=15 / n_sufficient=1 / frac_pnl_better=0.000 / frac_stop_loss_better=0.000 / frac_mae_better=1.000 / frac_all3_better=0.000`
  - 分桶覆盖：`align=0` ?`bucket0/1/2/3` 总交易数?`31 / 111 / 128 / 36`；`align=1` 几乎逢化为单一高桶，`bucket2/3=4 / 2883`，不存在 `bucket<=1` 可比样本
  - 唯一 sufficient pair（GBPJPY / A_relaxed / align=0）：`stop_bucket>=2` 相对 `stop_bucket<=1` ?`delta_avg_pnl=-55.40`、`delta_stop_loss_rate=0.000`、`delta_mae_atr_mean=-0.216` ?只体现略不痛苦，没有形成收益或止损率优势
- pre2022（strict latest-only）：
  - 汇：`align=0` ?`n_pairs=8 / n_sufficient=0`
  - 含义：历史窗同样无法形成可复现的 stop_dist sizing 证据；`align=1` 也没有足够的桶内分层可比?- 结论（v1）：`volty_stop_dist_bucket_1h` 暂不晋升 `CONFIG_BUCKET`；继续保留为 `SIZING_CANDIDATE（冻结）`
- 关键原因（v1）：
  - `align=1` ?`stop_dist_bucket` 高度共线，几乎全部落?`bucket>=2`，导致最想服?sizing 的顺势环境里反缺少有效分?  - `align=0` 虽能形成少量分桶，但首轮只复现出“MAE 略降”没?`pnl / stop_loss` 共振，不足以支撑 sizing ?reduce 规则
- 下一步（v1）：Volty 主线转入批次87 `align × hold_hours`，优先寻找持仓后?pain-up but pnl-flat/down”的提前减仓证据；批?8 再看 `exit context`

### 2026-06-10 批次87证据（Volty align × hold_hours；服?reduce / 提前减仓?
证据?- since2022?  - `backtest_out\stage2\indicator_audit\20260610_b87_volty_align_holdhours_core6_since2022_latest_strict_v1\b87_volty_holdhours_stats_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b87_volty_align_holdhours_core6_since2022_latest_strict_v1\b87_volty_holdhours_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b87_volty_align_holdhours_core6_since2022_latest_strict_v1\b87_volty_holdhours_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b87_volty_align_holdhours_core6_since2022_latest_strict_v1\b87_volty_holdhours_coverage_20260610_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260610_b87_volty_align_holdhours_core6_pre2022_latest_strict_v1\b87_volty_holdhours_stats_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b87_volty_align_holdhours_core6_pre2022_latest_strict_v1\b87_volty_holdhours_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b87_volty_align_holdhours_core6_pre2022_latest_strict_v1\b87_volty_holdhours_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b87_volty_align_holdhours_core6_pre2022_latest_strict_v1\b87_volty_holdhours_coverage_20260610_v1.csv`

==============================
BATCH_CLOSE（批?7；以证据拍板?==============================
- 口径说明：在同一 `volty_trend_align_1h` 内，对比 `early=hold_hours<=6h` vs `late=hold_hours>=24h`，并?`trade_mae_atr` 代理 `max_drawdown_per_trade`?H OHLC 窗口?- since2022（strict latest-only）：
  - `align=0`：`n_pairs=15 / n_sufficient=0`（样本不足，无法导出 reduce 结论?  - `align=1`：`n_pairs=18 / n_sufficient=6 / frac_pnl_better=1.000 / frac_stop_loss_better=1.000 / frac_mae_worse=0.833 / frac_pain_up_pnl_not_up=0.000`
  - 含义：在 `align=1` 环境下，“持更久?=24h）更常见的是收益更好、止损率更低，但 MAE 更大（更痛苦）；未发现后段更痛苦且收益不增的提前减仓证据
- pre2022（strict latest-only）：
  - `align=0`：`n_pairs=5 / n_sufficient=0`
  - `align=1`：`n_pairs=6 / n_sufficient=5 / frac_pnl_better=1.000 / frac_stop_loss_better=0.800 / frac_mae_worse=0.800 / frac_pain_up_pnl_not_up=0.000`
  - 含义：与 since2022 同向：late 更赚但更痛苦；止损率改善多数成立，但存在反例（某?symbol×profile ?late 反更易止损）
- 结论（v1）：
  - reduce：不支持“按持仓时间提前减仓”作为用规则
  - risk/sizing：`align=1` ?late ?MAE 更大，提示若要拿更久，可能需要更保守的风险预算或更宽的风险容忍，但这?trade-off，不等同 reduce 信号
- 下一步（v1）：转批?8 `align × exit context`，优先服?trailing/close 逻辑；hold_hours 只保留为风险权衡标签

- 灵敏度复跑（v2；strict latest-only；用于对比不?early/late 切法）：
  - S1：early<=2h vs late>=12h?    - since2022：`align=0 n_sufficient=0`；`align=1 n_sufficient=11 / frac_pnl_better=1.0 / frac_stop_loss_better?.455 / frac_mae_worse=1.0`
    - pre2022：`align=0 n_sufficient=0`；`align=1 n_sufficient=6 / frac_pnl_better=1.0 / frac_stop_loss_better=0.0 / frac_mae_worse?.833`
    - 证据：`backtest_out\stage2\indicator_audit\20260610_b87s1_hold_e2_l12_core6_*_latest_strict_v2\*`
  - S2：early<=6h vs late>=48h?    - since2022：`align=0 n_sufficient=0`；`align=1 n_sufficient=3 / frac_pnl_better=1.0 / frac_stop_loss_better?.667 / frac_mae_worse?.667`
    - pre2022：`align=0 n_sufficient=0`；`align=1 n_sufficient=4 / frac_pnl_better=1.0 / frac_stop_loss_better=1.0 / frac_mae_worse=0.5`
    - 证据：`backtest_out\stage2\indicator_audit\20260610_b87s2_hold_e6_l48_core6_*_latest_strict_v2\*`
  - S3：early<=12h vs late>=24h?    - since2022：`align=0 n_sufficient=0`；`align=1 n_sufficient=6 / frac_pnl_better=1.0 / frac_stop_loss_better=1.0 / frac_mae_worse?.667`
    - pre2022：`align=0 n_sufficient=0`；`align=1 n_sufficient=5 / frac_pnl_better=1.0 / frac_stop_loss_better=0.8 / frac_mae_worse=0.6`
    - 证据：`backtest_out\stage2\indicator_audit\20260610_b87s3_hold_e12_l24_core6_*_latest_strict_v2\*`

### 2026-06-10 批次88证据（Volty align × exit context；服?trailing / close?
证据（exit context ?proxy：基?`stop_loss_any/tp2_any/win` 派生，不包含 trailing/partial-close 真实标记）：
- since2022?  - `backtest_out\stage2\indicator_audit\20260610_b88_volty_align_exit_context_core6_since2022_latest_strict_v1\b88_volty_exit_context_rates_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b88_volty_align_exit_context_core6_since2022_latest_strict_v1\b88_volty_exit_context_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b88_volty_align_exit_context_core6_since2022_latest_strict_v1\b88_volty_exit_context_summary_20260610_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260610_b88_volty_align_exit_context_core6_pre2022_latest_strict_v1\b88_volty_exit_context_rates_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b88_volty_align_exit_context_core6_pre2022_latest_strict_v1\b88_volty_exit_context_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b88_volty_align_exit_context_core6_pre2022_latest_strict_v1\b88_volty_exit_context_summary_20260610_v1.csv`
- min_n=10 复跑（提?n_sufficient，用于稳定观察）?  - `backtest_out\stage2\indicator_audit\20260610_b88s1_exitctx_min10_core6_since2022_latest_strict_v1\b88_volty_exit_context_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b88s1_exitctx_min10_core6_pre2022_latest_strict_v1\b88_volty_exit_context_summary_20260610_v1.csv`

==============================
BATCH_CLOSE（批?8；以证据拍板?==============================
- since2022（min_n=20）：
  - `n_pairs=17 / n_sufficient=5`
  - `frac_stop_loss_lower=0.800`、`frac_tp2_higher=1.000`、`frac_avg_pnl_better=0.400`
  - `frac_win_no_tp2_higher=0.000`、`frac_loss_no_stop_lower=0.000`
- since2022（min_n=10）：
  - `n_pairs=17 / n_sufficient=12`
  - `frac_stop_loss_lower?.667`、`frac_tp2_higher?.917`、`frac_avg_pnl_better?.417`
  - `frac_win_no_tp2_higher=0.250`、`frac_loss_no_stop_lower?.083`
- pre2022（min_n=10）：
  - `n_pairs=8 / n_sufficient=4`
  - `frac_stop_loss_lower=1.000`、`frac_tp2_higher=1.000`、`frac_avg_pnl_better=0.250`
- 结论（v1）：?proxy 口径下，`align=1` 更像“更不容易止损更容易?tp2”的 exit 环境标签；但缺少 trailing/partial-close 的真实出场语境字段，暂不据此?trailing/close 逻辑

### 2026-06-10 多AI收口（BATCH_ID=20260610_v88_VOLTY_ALIGN_DEEPEN?
==============================
PANEL_VOTE_TSV
==============================

```tsv
model	q1_vote	q2_main_risk	q3_next_action	contract_ok	notes
kimi	B	align=1共线逢?b87小样?切法敏感	补真实exit字段并重跑b88；可扩大到core6+observe7	yes	朢完整；明确entry/sizing/reduce 冻结，只保留 exit 侧?deepseek	B	align=1下stop_dist_bucket共线逢?补真?exit_reason/close_partial/trailing_hit/bars_to_exit/mfe_atr 后重?yes	方法论最稳；强调 proxy 不能区分真实 exit 语境
glm	B	align=1共线坍塌与归因混?NEED_EVIDENCE: 真实 exit 字段化后重跑 b88	partial	格式不是单行 VOTE，但结论与多数一?千问	B	小样本（n_sufficient 低）	补真?exit 字段并重?b88	yes	更强调样本量风险
豆包	B	stop_dist 共线逢?+ hold_hours 幸存者偏?补真?exit 字段并重跑真 b88	yes	补充“hold 更久”可能是幸存者偏?```

==============================
DIFF_NOTES
==============================
- 共识点：5/5 都?`Q1=B`，即 Volty 不再晋升 entry/sizing/reduce，只允许继续做一次真?exit_context 字段化的验证
- 分歧?：主要风险归因不?  - kimi / deepseek / glm / 豆包：更强调 `align=1` 共线逢化导?b86/b87 容易出现“假强?  - 千问：更强调 `n_sufficient` 过低
  - repo_action：两者都采纳；下丢步同时补真实字段，并加一?`core6+observe7` 扩样复跑
- 分歧?：是否还值得?Volty 继续投入
  - 多数意见：只值得补一?exit 字段工程费；若真 b88 仍平庸，则应冻结/降级
  - repo_action：已按该思路执行；新增真?exit 字段并重跑真 b88

==============================
BATCH_CLOSE（多AI投票后的执行裁决?==============================
- 裁决：采?`Q1=B`
  - `volty_trend_align_1h` 固定定位?`RISK_CONTEXT / EXIT_CONTEXT_HINT`
  - 明确排除：`ENTRY_GATE / 通用SIZING / 通用REDUCE`
- 朢小动作：已执行真?exit_context 字段化并重跑?b88（见下节批次89?- 暂缓项：
  - 不继续讨?stop_dist sizing；除非先解?`stop_dist` ?`align`
  - 不把 hold_hours 用作 reduce；目前只?trade-off，没有pain-up but pnl-flat/down?
### 2026-06-10 批次89证据（Volty true exit context replay；真?exit 字段?
实现?- 已把以下真实字段写入 `b82_trade_features`?  - `tp1_any / trail_stop_hit_any / extreme_stop_any / stop_any / stop_be_any`
  - `close_partial_any / exit_legs / exit_reason_final / exit_reason_group / bars_to_exit`
  - `trade_mae_atr / trade_mfe_atr`
- 说明：以上字段均?`trades_baseline_*.csv` 的真?`reason / pnl / exit_time` 推导，不?proxy

证据?- core6 strict latest-only?  - `backtest_out\stage2\indicator_audit\20260610_b82_volty_stop_fields_core6_since2022_latest_strict_v3\b82_trade_features_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b82_volty_stop_fields_core6_pre2022_latest_strict_v3\b82_trade_features_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b88t_volty_align_exit_context_true_core6_since2022_latest_strict_v1\b88t_volty_exit_context_true_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b88t_volty_align_exit_context_true_core6_pre2022_latest_strict_v1\b88t_volty_exit_context_true_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b88t_s1_min10_core6_since2022_latest_strict_v1\b88t_volty_exit_context_true_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b88t_s1_min10_core6_pre2022_latest_strict_v1\b88t_volty_exit_context_true_summary_20260610_v1.csv`
- core6+observe7 strict latest-only（扩样复跑）?  - `backtest_out\stage2\indicator_audit\20260610_b82_volty_stop_fields_core6observe7_since2022_latest_strict_v3\b82_trade_features_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b82_volty_stop_fields_core6observe7_pre2022_latest_strict_v3\b82_trade_features_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b88t_s2_min10_core6observe7_since2022_latest_strict_v1\b88t_volty_exit_context_true_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b88t_s2_min10_core6observe7_pre2022_latest_strict_v1\b88t_volty_exit_context_true_summary_20260610_v1.csv`

==============================
BATCH_CLOSE（批?9；真 b88 以证据拍板）
==============================
- core6 / since2022?  - min_n=20：`n_pairs=17 / n_sufficient=5 / frac_stop_loss_final_lower=1.000 / frac_close_partial_higher=1.000 / frac_tp2_final_higher=0 / frac_trail_stop_final_higher=0 / frac_avg_pnl_better=0.400 / frac_mae_better=0.800 / frac_mfe_better=0.200`
  - min_n=10：`n_pairs=17 / n_sufficient=12 / frac_stop_loss_final_lower=0.750 / frac_close_partial_higher?.833 / frac_tp2_final_higher=0 / frac_trail_stop_final_higher?.083 / frac_trailing_hit_higher?.083 / frac_avg_pnl_better?.417 / frac_mae_better=0.750 / frac_mfe_better?.333`
- core6+observe7 / since2022（扩样后更关键）?  - `n_pairs=38 / n_sufficient=22 / frac_stop_loss_final_lower?.773 / frac_close_partial_higher?.818 / frac_tp2_final_higher=0 / frac_trail_stop_final_higher?.227 / frac_trailing_hit_higher?.227 / frac_avg_pnl_better?.409 / frac_mae_better?.773 / frac_mfe_better?.318`
- core6+observe7 / pre2022?  - `n_pairs=29 / n_sufficient=14 / frac_stop_loss_final_lower?.714 / frac_close_partial_higher?.714 / frac_tp2_final_higher=0 / frac_trail_stop_final_higher?.357 / frac_trailing_hit_higher?.357 / frac_avg_pnl_better?.357 / frac_mae_better?.571 / frac_mfe_better?.357`
- 关键差异（真 b88 vs proxy b88）：
  - proxy 里`tp2_any` 更高”成立；但真 b88 ?`final_exit_reason=tp2` 并没有提升，`frac_tp2_final_higher=0`
  - ?b88 真正稳定的不是更多最?tp2”，而是?    - `final stop_loss` 更低
    - `close_partial_any` 更高
    - `MAE` 更低
  - `trail_stop_final / trailing_hit_any` 只有弱改善，且远不够支撑“trailing optimizer?- 汇结论（v2）：
  - `volty_trend_align_1h` 可以保留?`EXIT_CONTEXT_HINT`，但其作用更接近“较少最终止?+ 更常发生分批止盈/保本离场”，不是“更容易朢?tp2?  - 因此：Volty 不晋?`TRAILING_OPTIMIZER`，也不建议改 close 逻辑默认?  - 若继续研究，朢多只补一?`max_duration_in_drawdown` / `drawdown_duration`，验证更痛苦但能活下来的持仓过程；否则可以先冻结

### 2026-06-10 多AI收口（BATCH_ID=20260610_v90_REOPEN_OR_PIVOT?
==============================
PANEL_VOTE_TSV
==============================

```tsv
model	q1_volty_next	q2_reopen_old_pool	q3_pick_family	q4_freeze_list	contract_ok	notes
kimi	A	A	N/A	过稀(48/51/54/61)+翻转(55)+口径不稳(65)	partial	唯一主张再补丢?drawdown_duration；其余与多数丢?deepseek	B	B	A	48/51/54/55/61/65 永久冻结?9-50/58-59/67-68 条件冻结	yes	唯一主张只重弢 trend_strength 丢?glm	B	A	E	稢疏型/翻转?volume口径型硬冻；47同构观察	partial	格式非单?VOTE，但结论清晰
千问	B	A	E	过稀?48/51/54/61)+跨窗口翻转型(55)+volume口径不稳?65)	yes	明确反对继续投入 Volty
豆包	B	A	N/A	永久冻结过稀?48/51/54/61)+跨窗口翻转型(55)+volume口径不稳?65)	yes	强调 Volty 收益端无优势、旧池重弢性价比低
```

==============================
DIFF_NOTES
==============================
- 共识?：`Q2` 基本丢致，旧否决池不得现在重开
  - 5/5 都反对批量重弢”；deepseek 虽给 `Q2=B/Q3=A`，也只建议在 `trend_strength` 上做丢次低成本复核
  - repo_action：采纳多数，旧否决池整体继续冻结；仅在长期文档写“条件重弢规则”，不新弢批次
- 共识?：永久冻结桶已明?  - 过稀型：48/51/54/61
  - 跨窗口翻转型?5
  - volume 口径不稳型：65（仅保留 `REOPEN_ON_A_SHARES_EXCHANGE_VOLUME`?  - repo_action：同步写入长期文档冻结规?- 分歧点：Volty 是否还得?`drawdown_duration`
  - kimi：建议做朢后一轮；理由?MAE 只测幅度，duration 可能提供正交信息
  - 其余 4 家：反对；理由是?b88 已把 Volty 定位压缩?`RISK_CONTEXT / EXIT_CONTEXT_HINT`，继续追加证据边际收益低
  - repo_action：采纳多数，当前先冻?Volty；不立即实现 `drawdown_duration`

==============================
BATCH_CLOSE（v90 裁决?==============================
- Volty?  - 采用 `Q1=B`
  - 当前正式冻结?`RISK_CONTEXT / EXIT_CONTEXT_HINT`
  - 暂不继续?`max_duration_in_drawdown / drawdown_duration`
  - 若未来重弢，前提必须是：已有持仓时?回撤持续时间字段可低成本落盘，且能证明与 `trade_mae_atr` 不同?- v47-v80 旧否决池?  - 采用 `Q2=A`
  - 本轮不重弢任何家族
  - `trend_strength / range-range_trap / EMA / CCI` 只保留条件重弢”备注，不进入当前执行队?- 资源转向?  - Volty 家族先停止追加证?  - 旧否决池不再做多AI轮询，除非出现新数据?新口?新前置条?
==============================
REOPEN_RULES（写给以后避免反复讨论）
==============================
- `trend_strength`（批?7）：仅当 `entry_score` 去重/解后，且霢要验证非线交互时，才允许重开
- `range / range_trap`（批?9/50）：仅当收益口径与止损口径矛盾被统一后，才允许重弢
- `EMA family`（批?8/59）：仅当 MAE/maxDD ?regime 交互口径统一后，才允许重弢
- `CCI basic`（批?7/68）：仅当出现更稳 split 证据或新的交互假设，才允许重弢
- `pullback / reversal / Wyckoff / KD divergence / candle / volume`：默认不重开；只有底层数据源或口径发生根本变化时才讨?
### 2026-06-10 批次91证据（Volty drawdown_duration；按 Kimi 建议补最后一轮）

实现?- 已在 `b82_trade_features` 新增?  - `max_drawdown_duration_hours`
  - `drawdown_duration_hours_total`
- 口径?  - 基于 1H 持仓窗口?`close` 序列
  - LONG：`close < entry` 视为 underwater；SHORT：`close > entry` 视为 underwater
  - `max_drawdown_duration_hours` = 朢长连?underwater bars ?  - `drawdown_duration_hours_total` = 全持仓期 underwater bars 总数

证据?- `backtest_out\stage2\indicator_audit\20260610_b82_volty_stop_fields_core6_since2022_latest_strict_v4\b82_trade_features_20260610_v1.csv`
- `backtest_out\stage2\indicator_audit\20260610_b82_volty_stop_fields_core6observe7_since2022_latest_strict_v4\b82_trade_features_20260610_v1.csv`
- `backtest_out\stage2\indicator_audit\20260610_b90d_volty_drawdown_duration_core6_since2022_latest_strict_v1\b90d_volty_drawdown_duration_summary_20260610_v1.csv`
- `backtest_out\stage2\indicator_audit\20260610_b90d_volty_drawdown_duration_core6_pre2022_latest_strict_v1\b90d_volty_drawdown_duration_summary_20260610_v1.csv`
- `backtest_out\stage2\indicator_audit\20260610_b90d_volty_drawdown_duration_core6observe7_since2022_latest_strict_v1\b90d_volty_drawdown_duration_summary_20260610_v1.csv`
- `backtest_out\stage2\indicator_audit\20260610_b90d_volty_drawdown_duration_core6observe7_pre2022_latest_strict_v1\b90d_volty_drawdown_duration_summary_20260610_v1.csv`

==============================
BATCH_CLOSE（批?1?==============================
- core6 / since2022?  - `n_pairs=17 / n_sufficient=12 / frac_avg_pnl_better?.417 / frac_mae_better=0.750 / frac_dd_duration_better?.167 / frac_total_dd_duration_better=0.500`
- core6+observe7 / since2022?  - `n_pairs=38 / n_sufficient=22 / frac_avg_pnl_better?.409 / frac_mae_better?.773 / frac_dd_duration_better?.318 / frac_total_dd_duration_better?.591`
- core6+observe7 / pre2022?  - `n_pairs=29 / n_sufficient=14 / frac_avg_pnl_better?.357 / frac_mae_better?.571 / frac_dd_duration_better?.429 / frac_total_dd_duration_better?.643`
- 结论?  - `drawdown_duration` 没有?Volty 带来正向翻案
  - `max_drawdown_duration_hours` ?since2022 / core6+observe7 下只?`?.318` 对是更优，明显弱?`trade_mae_atr`
  - `drawdown_duration_hours_total` 有一定改善，但幅度不足以改变 Volty 现有定位
  - 因此：Kimi 建议的最后一?duration 验证”已执行，但结果不支持重弢 Volty
- 裁决?  - `volty_trend_align_1h` 继续维持 `RISK_CONTEXT / EXIT_CONTEXT_HINT`
  - 不再追加 `drawdown_duration` 后续批次

### 2026-06-10 批次92证据（Trend Strength reopen；按 DeepSeek 建议低成本复核）

证据?- since2022?  - `backtest_out\stage2\indicator_audit\20260610_b47r_trend_strength_core6observe7_since2022_v1\b47_feature_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b47r_trend_strength_core6observe7_since2022_v1\b47_spearman_corr_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b47r_followups_core6observe7_since2022_v1\b47_stability_summary_20260610_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260610_b47r_trend_strength_core6observe7_pre2022_v1\b47_feature_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b47r_trend_strength_core6observe7_pre2022_v1\b47_spearman_corr_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b47r_followups_core6observe7_pre2022_v1\b47_stability_summary_20260610_v1.csv`

==============================
BATCH_CLOSE（批?2?==============================
- since2022?  - `top_minus_bot_avg_pnl=-373.05`（score qtiles4?  - `top_minus_bot_avg_pnl=-690.95`（bucket code4?  - `spearman(trade_pnl)?0.028`
  - `spearman(entry_score)?.371`
  - `frac_pnl_better?.385~0.462`，未过半
- pre2022?  - `top_minus_bot_avg_pnl=+219.84`（score qtiles4?  - `top_minus_bot_avg_pnl=+140.16`（bucket code4?  - `spearman(trade_pnl)?0.031`
  - `spearman(entry_score)?.317`
  - `frac_both` ?`0.111~0.333`
- 结论?  - 低成本重弢后，`trend_strength` 仍保留原来的核心问题?    - ?`trade_pnl` 近乎 0 相关
    - ?`entry_score` 仍有中等同构风险
    - since2022 / pre2022 方向继续分裂
  - 因此：DeepSeek 建议?reopen 已执行，但结果不支持重开 `trend_strength`
- 裁决?  - `ab_trend_strength_score_1h / bucket` 继续保持 `DIAG_ONLY`
  - 从条件重弢候进丢步降为仅?entry_score 完成显著解时再讨论?
### 2026-06-10 批次93证据（Range Trap × MAE；补风险侧复核）

说明?- 旧批?0的长期结论是：若未来还要继续投入 `range_trap`，必须先?`MAE/max_dd`，再讨论它是否可作为 `RISK_AVOID / REDUCE` 候?- 本轮只做朢小补证据，不改原?`b50r-*` 定义；新增独立命?`b93-range-trap-mae`?
证据?- since2022?  - `backtest_out\stage2\indicator_audit\20260610_b93_range_trap_mae_core6observe7_since2022_v1\b93_range_trap_mae_bucket_stats_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b93_range_trap_mae_core6observe7_since2022_v1\b93_range_trap_mae_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b93_range_trap_mae_core6observe7_since2022_v1\b93_range_trap_mae_summary_20260610_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260610_b93_range_trap_mae_core6observe7_pre2022_v1\b93_range_trap_mae_bucket_stats_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b93_range_trap_mae_core6observe7_pre2022_v1\b93_range_trap_mae_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b93_range_trap_mae_core6observe7_pre2022_v1\b93_range_trap_mae_summary_20260610_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b93-range-trap-mae --date 20260610 --scope core6_observe7 --split since2022 --min_n 10 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b93_range_trap_mae_core6observe7_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b93-range-trap-mae --date 20260610 --scope core6_observe7 --split pre2022 --min_n 10 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b93_range_trap_mae_core6observe7_pre2022_v1`

==============================
BATCH_CLOSE（批?3?==============================
- since2022?  - `ab_range_trap_flag_1h`：`n_pairs=31 / frac_pnl_better?.839 / frac_stop_loss_better?.323 / frac_mae_better?.355 / frac_both_mae_stop?.129`
  - `ab_range_trap_repeat_1h`：`n_pairs=34 / frac_pnl_better?.676 / frac_stop_loss_better?.353 / frac_mae_better?.559 / frac_both_mae_stop?.324`
  - `ab_range_trap_score_1h`：`n_pairs=17 / frac_pnl_better?.529 / frac_stop_loss_better?.412 / frac_mae_better?.294 / frac_both_mae_stop?.176`
- pre2022?  - `ab_range_trap_flag_1h`：`n_pairs=6 / frac_stop_loss_better?.167 / frac_mae_better=0.0`
  - `ab_range_trap_repeat_1h`：`n_pairs=11 / frac_pnl_better?.636 / frac_stop_loss_better?.273 / frac_mae_better?.364 / frac_both_mae_stop?.091`
  - `ab_range_trap_score_1h`：`n_pairs=2`，样本不足，不具备收口价?- 解读?  - `trap_score` 主线没有翻案：收益侧朢多略偏正，但 `stop_loss` ?`MAE` 并未同步改善
  - `trap_repeat` ?since2022 ?`MAE` 略有改善，但 `stop_loss` 改善仍弱，pre2022 也不能复?  - 因此这轮补完风险侧后，`range_trap` 仍不满足 `RISK_AVOID / REDUCE` 候?- 裁决?  - `ab_range_trap_score_1h / ab_range_trap_flag_1h / ab_range_trap_repeat_1h` 继续维持 `DIAG_ONLY`
  - 旧批?0里先?MAE 再讨论的前置条件已完成；结果仍不支持晋升
  - `range / range_trap` 暂不再优先推进，除非后续统一更强?`max_dd/regime` 交互口径

### 2026-06-10 批次93补充（Range Trap × MAE：全屢 scope=all 复跑?
证据?- since2022?  - `backtest_out\stage2\indicator_audit\20260610_b93_range_trap_mae_all_since2022_v1\b93_range_trap_mae_summary_20260610_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260610_b93_range_trap_mae_all_pre2022_v1\b93_range_trap_mae_summary_20260610_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b93-range-trap-mae --date 20260610 --scope all --split since2022 --min_n 10 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b93_range_trap_mae_all_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b93-range-trap-mae --date 20260610 --scope all --split pre2022 --min_n 10 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b93_range_trap_mae_all_pre2022_v1`

补充结论?- 全局复跑后，原否决结论不变且更稳?  - since2022?    - `ab_range_trap_flag_1h`：`n_pairs=52 / frac_pnl_better?.654 / frac_stop_loss_better?.385 / frac_mae_better?.346 / frac_both_mae_stop?.154`
    - `ab_range_trap_repeat_1h`：`n_pairs=72 / frac_pnl_better?.569 / frac_stop_loss_better?.431 / frac_mae_better=0.500 / frac_both_mae_stop?.306`
    - `ab_range_trap_score_1h`：`n_pairs=24 / frac_pnl_better?.417 / frac_stop_loss_better?.417 / frac_mae_better=0.375 / frac_both_mae_stop?.208`
  - pre2022?    - `ab_range_trap_flag_1h`：`n_pairs=19 / frac_pnl_better?.526 / frac_stop_loss_better?.263 / frac_mae_better?.316 / frac_both_mae_stop?.158`
    - `ab_range_trap_repeat_1h`：`n_pairs=39 / frac_pnl_better?.462 / frac_stop_loss_better?.359 / frac_mae_better?.487 / frac_both_mae_stop?.256`
- 解释?  - `repeat` 仍是家族里相对最像有信息”的片段，但无论全局还是旧口径，都卡?`stop_loss` 改善不足，不能晋升为 `RISK_AVOID / REDUCE`
  - `flag / score` 在全屢口径下同样没有形成稳定三口径丢致?- 裁决不变?  - `ab_range_trap_score_1h / ab_range_trap_flag_1h / ab_range_trap_repeat_1h` 继续 `DIAG_ONLY`
  - `range / range_trap` 可视为本轮已完成“全屢补证据后正式冻结?
### 2026-06-10 批次94证据（EMA family：MAE × sv_regime_code × sv_risk_on_mkt 交互?
说明?- 旧批?9结论是分段弱/不稳健，但真正缺口是：没有把 EMA 字段放进 `MAE` ?`regime` 的交互口径里做审计式复核?- 本批次只补证据，不改 b58/b59 原有口径；新增独立命?`b94-ema-family-mae-regime`?
证据?- since2022?  - `backtest_out\stage2\indicator_audit\20260610_b94_ema_mae_regime_core6observe7_since2022_v1\b94_ema_mae_regime_bucket_stats_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b94_ema_mae_regime_core6observe7_since2022_v1\b94_ema_mae_regime_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b94_ema_mae_regime_core6observe7_since2022_v1\b94_ema_mae_regime_summary_20260610_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260610_b94_ema_mae_regime_core6observe7_pre2022_v1\b94_ema_mae_regime_bucket_stats_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b94_ema_mae_regime_core6observe7_pre2022_v1\b94_ema_mae_regime_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b94_ema_mae_regime_core6observe7_pre2022_v1\b94_ema_mae_regime_summary_20260610_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b94-ema-family-mae-regime --date 20260610 --scope core6_observe7 --split since2022 --min_n 10 --profile_merge 1 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b94_ema_mae_regime_core6observe7_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b94-ema-family-mae-regime --date 20260610 --scope core6_observe7 --split pre2022 --min_n 10 --profile_merge 1 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b94_ema_mae_regime_core6observe7_pre2022_v1`

==============================
BATCH_CLOSE（批?4?==============================
- 代表性正向片段（risk=0, regime=0）：
  - since2022：`ab_ema20_gt_ema200_1h`：`n_pairs=61 / frac_pnl_better?.754 / frac_stop_loss_better?.525 / frac_mae_better?.459 / frac_both_mae_stop?.361`
  - pre2022：`ab_ema20_gt_ema200_1h`：`n_pairs=23 / frac_pnl_better?.739 / frac_stop_loss_better?.826 / frac_mae_better?.609 / frac_both_mae_stop?.522`
  - since2022：`ab_ema200_side_1h`：`n_pairs=55 / frac_pnl_better?.745 / frac_stop_loss_better?.582 / frac_mae_better?.491 / frac_both_mae_stop?.364`
  - pre2022：`ab_ema200_side_1h`：`n_pairs=23 / frac_pnl_better?.826 / frac_stop_loss_better?.696 / frac_mae_better?.478 / frac_both_mae_stop?.435`
- 明显负向片段（risk=1, regime=2）：
  - since2022：`ab_ema_reclaim_1h`：`n_pairs=50 / frac_pnl_better=0.32 / frac_stop_loss_better=0.38 / frac_mae_better=0.04`
- 解读?  - EMA 宏观侧（`ema200_side/ema20_gt_ema200`）在 `risk=0 & regime=0` 里出现收?风险同时更好”的丢致片段，但它是强条件化标签，不具备用晋升路径
  - EMA reclaim/touch 类字段在部分 regime 下出现明显负向（尤其 `risk=1 & regime=2`），不合作为通用加分/门控
- 裁决?  - EMA family 继续维持 `DIAG_ONLY`
  - 仅允许把 `ab_ema200_side_1h / ab_ema20_gt_ema200_1h` 作为 `RISK_CONTEXT_HINT（条件化：risk=0 & regime=0）` 做复盘标记，不进入用 shortlist

### 2026-06-10 批次94补充（EMA family：全屢 scope=all 复跑?
证据?- since2022?  - `backtest_out\stage2\indicator_audit\20260610_b94_ema_mae_regime_all_since2022_v1\b94_ema_mae_regime_summary_20260610_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260610_b94_ema_mae_regime_all_pre2022_v1\b94_ema_mae_regime_summary_20260610_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b94-ema-family-mae-regime --date 20260610 --scope all --split since2022 --min_n 10 --profile_merge 1 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b94_ema_mae_regime_all_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b94-ema-family-mae-regime --date 20260610 --scope all --split pre2022 --min_n 10 --profile_merge 1 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b94_ema_mae_regime_all_pre2022_v1`

补充结论?- 全局复跑后，原结论不变：
  - `risk=0, regime=0` 下，`ab_ema20_gt_ema200_1h` 仍是朢强正向片段：since2022 `frac_pnl_better?.722 / frac_stop_loss_better?.632 / frac_mae_better?.474 / frac_both_mae_stop?.376`；pre2022 `?.590 / 0.672 / 0.459 / 0.377`
  - `ab_ema200_side_1h` 同样保留条件化正向：since2022 `?.674 / 0.620 / 0.465 / 0.357`；pre2022 `?.645 / 0.613 / 0.435 / 0.355`
  - `ab_ema_reclaim_1h` ?`risk=1, regime=2` 的明显负向也被全屢复跑保留：since2022 `frac_pnl_better?.315 / frac_stop_loss_better?.404 / frac_mae_better?.034`
- 裁决不变?  - EMA family 继续 `DIAG_ONLY`
  - `ab_ema200_side_1h / ab_ema20_gt_ema200_1h` 仍只允许作为 `RISK_CONTEXT_HINT（条件化：risk=0 & regime=0）`

### 2026-06-10 批次95证据（E1 Break Strength × MAE；补“更赚但更痛苦复核）

说明?- 旧批?3/42 ?`e1_break_strength_atr` 的定位是 `ADD_CANDIDATE（quality_score）`，但缺口是：没有用笔 MAE（ATR归一）复核它是否存在“收益提升但持仓过程更痛苦的 trade-off?- 本批次只补证据，不改变任何执行默认?
证据?- since2022?  - `backtest_out\stage2\indicator_audit\20260610_b95_e1_break_strength_mae_core6observe7_since2022_v3\b95_e1_break_strength_mae_bucket_stats_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b95_e1_break_strength_mae_core6observe7_since2022_v3\b95_e1_break_strength_mae_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b95_e1_break_strength_mae_core6observe7_since2022_v3\b95_e1_break_strength_mae_summary_20260610_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260610_b95_e1_break_strength_mae_core6observe7_pre2022_v3\b95_e1_break_strength_mae_bucket_stats_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b95_e1_break_strength_mae_core6observe7_pre2022_v3\b95_e1_break_strength_mae_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b95_e1_break_strength_mae_core6observe7_pre2022_v3\b95_e1_break_strength_mae_summary_20260610_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b95-e1-break-strength-mae --date 20260610 --scope core_observe --split since2022 --min_n 10 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b95_e1_break_strength_mae_core6observe7_since2022_v3`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b95-e1-break-strength-mae --date 20260610 --scope core_observe --split pre2022 --min_n 10 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b95_e1_break_strength_mae_core6observe7_pre2022_v3`

==============================
BATCH_CLOSE（批?5?==============================
- since2022（core6+observe7；qtiles4 top vs bottom；n>=10）：
  - `n_pairs=82 / n_sufficient=59 / frac_pnl_better?.610 / frac_stop_loss_better?.458 / frac_mae_better?.407 / frac_all3_better?.254`
- pre2022（core6+observe7；qtiles4 top vs bottom；n>=10）：
  - `n_pairs=27 / n_sufficient=26 / frac_pnl_better=0.500 / frac_stop_loss_better?.346 / frac_mae_better?.577 / frac_all3_better?.231`
- 解读?  - since2022：高 break_strength 的收益侧更常为正，但风险侧（stop_loss/MAE）并未同步改善，偏更赚但更痛?更不稳的典型 trade-off?  - pre2022：收益侧不出优势，止损侧更差?MAE 偏好，呈现分裂，不支持任何形式的 gate 晋升?- 裁决?  - `e1_break_strength_atr` 维持 `ADD_CANDIDATE（quality_score）`，不晋升 `ENTRY_FILTER`，也不做 hard gate?  - 后续若要落入“弱门槛”，必须先出现：`frac_all3_better>=0.60` 的稳定（symbol×profile）或找到明确的条件化片段（regime/risk_on 交互）再讨论?
### 2026-06-10 批次95补充（E1 Break Strength × MAE：全屢 scope=all 复跑?
证据?- since2022?  - `backtest_out\stage2\indicator_audit\20260610_b95_e1_break_strength_mae_all_since2022_v1\b95_e1_break_strength_mae_summary_20260610_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260610_b95_e1_break_strength_mae_all_pre2022_v1\b95_e1_break_strength_mae_summary_20260610_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b95-e1-break-strength-mae --date 20260610 --scope all --split since2022 --min_n 10 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b95_e1_break_strength_mae_all_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b95-e1-break-strength-mae --date 20260610 --scope all --split pre2022 --min_n 10 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b95_e1_break_strength_mae_all_pre2022_v1`

补充结论?- 全局复跑后，trade-off 结论更稳?  - since2022：`n_pairs=157 / n_sufficient=119 / frac_pnl_better?.563 / frac_stop_loss_better?.403 / frac_mae_better?.412 / frac_all3_better?.227`
  - pre2022：`n_pairs=81 / n_sufficient=75 / frac_pnl_better?.507 / frac_stop_loss_better?.387 / frac_mae_better?.493 / frac_all3_better=0.240`
- ?`core6+observe7` 相比，全屢口径下收益优势被摊薄，风险侧改善仍未成立，因此更赚但更痛?更不稳依旧成立，且更不支持任?gate 晋升?- 裁决不变?  - `e1_break_strength_atr` 继续维持 `ADD_CANDIDATE（quality_score）`
  - 不晋?`ENTRY_FILTER` / hard gate

### 2026-06-10 批次96证据（Session family：entry_session × MAE?
说明?- 批次40已经?`entry_session` 收口成：整体 `DIAG_ONLY`、`London=ADD_CANDIDATE（弱）`、`Asia/NY` 暂不贴风险标签?- 当时明确缺口是：必须?`trade_mae_atr`，否则无法判?NY/Asia 的更痛苦/更不痛苦”是否真实成立?
证据?- since2022?  - `backtest_out\stage2\indicator_audit\20260610_b96_session_mae_core6observe7_since2022_v1\b96_session_mae_bucket_stats_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b96_session_mae_core6observe7_since2022_v1\b96_session_mae_bucket_agg_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b96_session_mae_core6observe7_since2022_v1\b96_session_mae_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b96_session_mae_core6observe7_since2022_v1\b96_session_mae_summary_20260610_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260610_b96_session_mae_core6observe7_pre2022_v1\b96_session_mae_bucket_stats_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b96_session_mae_core6observe7_pre2022_v1\b96_session_mae_bucket_agg_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b96_session_mae_core6observe7_pre2022_v1\b96_session_mae_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b96_session_mae_core6observe7_pre2022_v1\b96_session_mae_summary_20260610_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b96-session-mae --date 20260610 --scope core_observe --split since2022 --min_n 10 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b96_session_mae_core6observe7_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b96-session-mae --date 20260610 --scope core_observe --split pre2022 --min_n 10 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b96_session_mae_core6observe7_pre2022_v1`

==============================
BATCH_CLOSE（批?6?==============================
- pooled bucket_agg（core6+observe7）：
  - since2022：`London avg_pnl?5.36 / stop_loss_rate?.203 / mae_atr_mean?.633`；`NY avg_pnl?32.86 / stop_loss_rate?.191 / mae_atr_mean?.355`；`Asia avg_pnl?7.50 / stop_loss_rate?.289 / mae_atr_mean?.603`
  - pre2022：`London avg_pnl?7.30 / stop_loss_rate?.209 / mae_atr_mean?.879`；`NY avg_pnl?4.10 / stop_loss_rate?.165 / mae_atr_mean?.296`；`Asia avg_pnl?103.20 / stop_loss_rate?.317 / mae_atr_mean?.509`
- session vs non-session（symbol×profile；min_n=10）：
  - since2022?    - `London`：`n_pairs=102 / n_sufficient=97 / frac_pnl_better?.577 / frac_stop_loss_better?.691 / frac_mae_better?.309 / frac_all3_better?.175`
    - `NY`：`n_pairs=101 / n_sufficient=83 / frac_pnl_better?.446 / frac_stop_loss_better?.747 / frac_mae_better?.892 / frac_all3_better?.434`
    - `Asia`：`n_pairs=98 / n_sufficient=72 / frac_pnl_better=0.500 / frac_stop_loss_better?.194 / frac_mae_better?.292 / frac_all3_better?.097`
  - pre2022?    - `London`：`n_pairs=27 / n_sufficient=27 / frac_pnl_better?.667 / frac_stop_loss_better?.630 / frac_mae_better?.148 / frac_all3_better?.148`
    - `NY`：`n_pairs=27 / n_sufficient=27 / frac_pnl_better?.593 / frac_stop_loss_better?.815 / frac_mae_better=1.000 / frac_all3_better?.519`
    - `Asia`：`n_pairs=27 / n_sufficient=22 / frac_pnl_better?.364 / frac_stop_loss_better?.091 / frac_mae_better?.364 / frac_all3_better?.045`
- 解读?  - `London`：收益与 stop_loss 方向经常更好，但 MAE 明显不跟随，属于“更会赚?更少朢终止损，但持仓过程更痛苦”的 trade-off；因此不支持 London-only 或硬过滤?  - `NY`：`MAE` ?`stop_loss_rate` 的改善都很强，说明更不痛苦是真信息；?since2022 的收益侧仍弱?non-NY，因此不能把它简单贴成更差时段或“应回避时段”?  - `Asia`：三口径都不稳定，继续维持弱信息标签?- 裁决?  - `entry_session` 整体继续 `DIAG_ONLY`
  - `London` 继续保留 `ADD_CANDIDATE（弱）`，但明确不晋?`ENTRY_FILTER`
  - `NY` 可上调为 `RISK_CONTEXT_HINT`：含义是“持仓过程更不痛?朢终止损更少，不是“收益更好或“应硬回?硬优先?  - `Asia` 继续 `DIAG_ONLY`
- 下一步最小证据动作（仅当还要继续投资源时）：
  - `session × vol_state / regime` 交叉，检?London 是否只是 `NORMAL` ?`risk=0` 的代?  - 若未来要做执行侧解释，只允许作为复盘/风险标签，不允许直接改仓位默认?
### 2026-06-10 批次97证据（Session family：entry_session × sv_regime_code × sv_risk_on_mkt × MAE；全屢口径?
说明?- 这是对批?6的直接追击：棢?`London/NY` 的结论是否只是环境代理?- 本批次刻意改?`scope=all`，用于回答最近补证据批次有没有跑全局”的问题；结论是：`批次93-96` 之前都只跑了 `core6+observe7`，`批次97` 这次是明确全屢复跑?
证据?- since2022?  - `backtest_out\stage2\indicator_audit\20260610_b97_session_regime_mae_all_since2022_v1\b97_session_regime_mae_bucket_stats_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b97_session_regime_mae_all_since2022_v1\b97_session_regime_mae_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b97_session_regime_mae_all_since2022_v1\b97_session_regime_mae_summary_20260610_v1.csv`
- pre2022?  - `backtest_out\stage2\indicator_audit\20260610_b97_session_regime_mae_all_pre2022_v1\b97_session_regime_mae_bucket_stats_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b97_session_regime_mae_all_pre2022_v1\b97_session_regime_mae_pairs_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b97_session_regime_mae_all_pre2022_v1\b97_session_regime_mae_summary_20260610_v1.csv`

COMMAND（可复现）：
- since2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b97-session-regime-mae --date 20260610 --scope all --split since2022 --min_n 10 --profile_merge 1 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b97_session_regime_mae_all_since2022_v1`
- pre2022：`.\.venv\Scripts\python.exe .\backtest_p0.py b97-session-regime-mae --date 20260610 --scope all --split pre2022 --min_n 10 --profile_merge 1 --out_dir .\backtest_out\stage2\indicator_audit\20260610_b97_session_regime_mae_all_pre2022_v1`

==============================
BATCH_CLOSE（批?7?==============================
- 全局 summary（profile_merge=A_all；session vs non-session）：
  - since2022?    - `risk=1, regime=1`：`London frac_pnl_better?.540 / frac_stop_loss_better?.552 / frac_mae_better?.241`；`NY?.588 / 0.825 / 0.913 / frac_all3?.538`
    - `risk=1, regime=2`：`London?.538 / 0.575 / 0.151`；`NY?.478 / 0.707 / 0.815 / frac_all3?.413`
    - `risk=0, regime=0`：`London?.538 / 0.555 / 0.280`；`NY?.448 / 0.619 / 0.843 / frac_all3?.403`
  - pre2022?    - `risk=1, regime=1`：`London?.465 / 0.465 / 0.183`；`NY?.508 / 0.820 / 0.934 / frac_all3?.492`
    - `risk=1, regime=2`：`London?.380 / 0.479 / 0.113`；`NY?.565 / 0.790 / 0.887 / frac_all3?.500`
    - `risk=0, regime=0`：`London?.479 / 0.521 / 0.169`；`NY?.421 / 0.579 / 0.877 / frac_all3?.298`
- 解读?  - `London` 的问题在分层后依然存在：即使控制 `risk/regime`，它也反复表现为“收益或朢终止损可偏正，但 `MAE` 明显不跟随，说明它不是简单的环境代理，仍是典?trade-off?  - `NY` ?`RISK_CONTEXT_HINT` ?`risk=1, regime=1/2` 下仍稳定成立：`stop_loss_rate` ?`MAE` 几乎持续双改善；这说明更不痛苦不是批?6聚合口径下的假象?  - `risk=0, regime=0` ?NY 的收益侧仍弱，因此它仍不能被解释成收益更好时段或“应硬优先时段?- 裁决?  - `entry_session` 整体继续 `DIAG_ONLY`
  - `London` 继续维持 `ADD_CANDIDATE（弱）`，明确不晋升 `ENTRY_FILTER`
  - `NY` ?`RISK_CONTEXT_HINT` 得到全局口径 + 环境分层的二次确认，可继续保留；但仍禁止转成 avoid-NY / prefer-NY 的硬规则
  - `Asia` 继续 `DIAG_ONLY`

### 2026-06-10 数据更新（MT5 朢近两?1H 增量?
说明?- 现有 `data\*_1h.csv` 朢近一次集中更新停?`2026-06-02`
- 本次使用仓库现成脚本 `mt5_export_1h.py` ?`mode=update` 的两周增量更新，时间窗设?`2026-05-26 -> 2026-06-10`

COMMAND（可复现）：
- 首次尝试（失败原因：`usoil` 在当?MT5 中不?`USOIL` 命名）：
  - `.\.venv\Scripts\python.exe .\mt5_export_1h.py --source mt5 --mode update --overlap-hours 48 --start 2026-05-26 --end 2026-06-10 --out-dir .\data --symbols xauusd:XAUUSD,xagusd:XAGUSD,eurusd:EURUSD,gbpusd:GBPUSD,usdjpy:USDJPY,usdcad:USDCAD,audusd:AUDUSD,nzdusd:NZDUSD,usdchf:USDCHF,eurjpy:EURJPY,gbpjpy:GBPJPY,usoil:USOIL,us500:US500,nas100:NAS100,ger40:GER40`
- 修正后成功命令：
  - `.\.venv\Scripts\python.exe .\mt5_export_1h.py --source mt5 --mode update --overlap-hours 48 --start 2026-05-26 --end 2026-06-10 --allow-missing 1 --out-dir .\data --symbols xauusd:XAUUSD,xagusd:XAGUSD,eurusd:EURUSD,gbpusd:GBPUSD,usdjpy:USDJPY,usdcad:USDCAD,audusd:AUDUSD,nzdusd:NZDUSD,usdchf:USDCHF,eurjpy:EURJPY,gbpjpy:GBPJPY,usoil:XTIUSD,us500:US500,ger40:DE40,nas100:NAS100`

结果?- 已更新到 `2026-06-10` 写盘时间的文件：
  - `xauusd_1h.csv / xagusd_1h.csv / eurusd_1h.csv / gbpusd_1h.csv / usdjpy_1h.csv / usdcad_1h.csv / audusd_1h.csv / nzdusd_1h.csv / usdchf_1h.csv / eurjpy_1h.csv / gbpjpy_1h.csv / usoil_1h.csv / us500_1h.csv / ger40_1h.csv`
- 当前 MT5 终端缺失?  - `nas100`（`NAS100/US100/NDX100` 均未出现在当?MT5 symbols_get；因此保留旧文件，未更新?- 末端样本抽查?  - `eurusd_1h.csv` 朢新已?`2026.06.10 00:00`
  - `xauusd_1h.csv` 朢新已?`2026.06.09 23:00`
  - `us500_1h.csv` 朢新已?`2026.06.09 23:00`

