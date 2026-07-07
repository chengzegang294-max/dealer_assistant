# 阶段二｜当下计划（执行清单）

更新时间?026-06-10（单字段阶段已收口；下一阶段切换为稳定组合优?条件化应用）

关联文件?
- 阶段丢记录（过?落地/不可落地）：`01_阶段丢_项目记录_过去与落?md`
- 阶段二方向（未来/想法库）：`02_阶段二_工作方向_想法?md`
- 临时粘贴区（外部AI回复/终端输出）：`临时粘贴区_外部AI与终端输?md`

## 1) 当前要做仢么（从方向库”收敛来?

### 1.0 阶段切换摘要?026-06-10?

- 本阶段结论：单字?单指标阶段已完成；后续不再新增单字段还有没有用的大范围讨论?
- 本阶段边界：
  - 已纳入：当前 FX/index/commodity 1H 口径下可量化、可独立落盘、可独立验收的字?
  - 未纳入：A 股真实量能依赖字段仍不可量化的资料规则壳
- 下一阶段目标：只围绕“已有稳定?条件保留项做组合优化、条件化应用、以及最小必要的?gate 对照，不再回到单字段扫库模式?
- 下一阶段优先对象?
  - `sv_atr_ratio_1h`（条件型 `ENTRY_FILTER_CANDIDATE`?
  - `sv_swing_present_4h`（条件型 `ADD_CANDIDATE`?
  - `diag_session_skew_ratio`（弱 `REDUCE_CANDIDATE`?
  - `ab_always_in_agree_side_1h`（条件型弱过滤）
  - `rsi_basic_favor_bucket_1h / extreme_1h`（`RISK_ONLY_CANDIDATE`；仅作为组合研究对象，不单独外推为用 gate?
  - `atr / entry_score / ab_ema200_side_1h`（风?上下文标签）
- 这一阶段的经验口径：
  - 先把单字段全部收口，再做组合，比“边挖新字段边拼组合”更?
  - 组合阶段默认只使用已收口字段；任何新字段重开都必须满足新增数据口径或新增明确证据”的前提

### 1.1 资料源盘点与目录整理?026-06-10?

- 总表：`docs\资料源吸收状态与目录整理方案_20260610.md`
- 本轮新增口径?
  - 不把“来源库是否都文件吃透与“当前单字段阶段是否完成”混为一?
  - 组合优化弢始前，先用表固定各目录角色：来源?/ 已量化已讨论 / future bucket / 工具运行?
- 已执行：
  - 设定 `02_MT指标家族_源码与探针` ?MT 指标源码/探针标准入口
  - 清理小重复目录：`02_mt指标测试`
  - 设定 `98_MT历史数据_VTMarkets_Live2` ?MT4 历史归档标准入口
- 暂不执行?
  - `12_ʱ_TOOLING_RUNTIME\VTMarkets-Live 2` 先保留为兼容副本；待后续单独审计依赖后再决定是否删除
- 进入组合优化前的边界?
  - 不再默认?`00_* / 02_原子化拆解文件` 弢新单字段
  - 只在现有稳定候与条件标签中做组合

1) 框架收口：阶段二大框?v13 已定稿（停止“讨论框架，改为按合约产生产物）
2) 资料层补齐：已落?`docs\rules_index.md`（SOURCE_ANCHOR 总目录，研究/复盘只读引用?
2.1) A股补充资料：周期女王“周期状态系统规则壳”已纳入阶段二想法库索引（用于后续把 A股情?周期状做成可落盘?regime 标签?
3) 数据落地：把 1H 行情 CSV 准备齐（优先 MT5 丢键导出；次淘?历史 CSV 直接拷贝?data\?
4) 跑用对比：跑 `run_p0_sweep.ps1` 产出 `backtest_out\p0_sweep\p0_sweep_summary.csv`
5) 定口径与分层：验收口径?B，并已升级为 B_v2（避?observe 混入整体亏损标的），固化产物?
   - `backtest_out\p0_sweep\p0_sweep_decision_table_YYYYMMDD_v2.csv`
   - `backtest_out\p0_sweep\deploy_core_YYYYMMDD_v2.csv`
   - `backtest_out\p0_sweep\deploy_observe_YYYYMMDD_v2.csv`
   - `backtest_out\p0_sweep\deploy_exclude_YYYYMMDD_v2.csv`
5.1) 观测期（日更占位，不等同自动交易）：初始化当日观察表 `backtest_out\stage2\observe\observe_YYYYMMDD.csv`（按朢?deploy_core/observe 列表生成），用于记录 diag_vol_state_gate + defense_mode + triggered/原因/out_dir/备注 + entry_time_utc + snapshot_price
5.2) 下一轮研究裁决（批次21）：丢致票选择 C06（squeeze + EMA stack）进入真 gate”验证，对照组为 C03_squeeze_only；产物必须输出到 `backtest_out\p0_sweep\truegate_c06_*_YYYYMMDD_vN.csv`（同口径对照 dd_ok_rate/avg_net_pnl/avg_trades/avg_max_dd_pct?
   - 已产出证据（since2022；core+observe；best_profile）：`backtest_out\p0_sweep\truegate_c06_vs_c03_since2022_20260603_v1.csv` ?`backtest_out\p0_sweep\truegate_c06_vs_c03_agg_since2022_20260603_v1.csv`
   - 口径说明：C03=sv_regime_code==0；C06=C03 ?ema13>ema21>ema55(4H)（空头为反向排列）；通过 `--entry-vol-state-gate-mode 2` + `--enable-entry-ema-stack-gate 1` 实现（默认关闭，仅研究用?
   - 当前结果：C06 ?C03 在该口径下数值完全一??下一步改为确认是否删?C06（避免伪差异）或保留为等价别名（便于沟）?
   - 下一步最小证据：fullpool(32 symbols) since2022 复跑 C06 vs C03 ?gate 对照；若仍一致则废弃 C06 作为独立组合
   - fullpool 证据已完成：`backtest_out\p0_sweep\truegate_c06_vs_c03_fullpool_agg_since2022_20260603_v1.csv`（汇总）?`backtest_out\p0_sweep\truegate_c06_vs_c03_fullpool_since2022_20260603_v1.csv`（品种）；结果仍完全丢??C06 不再作为独立组合推进
5.3) 下一轮真 gate（批?3候）：验?C07（squeeze + kd_align_3tf）对?C03（fullpool；since2022；best_profile）；产物：`backtest_out\p0_sweep\truegate_c07_vs_c03_fullpool_*_YYYYMMDD_vN.csv`
   - 已产出证据：`backtest_out\p0_sweep\truegate_c07_vs_c03_fullpool_since2022_20260603_v1.csv` ?`backtest_out\p0_sweep\truegate_c07_vs_c03_fullpool_agg_since2022_20260603_v1.csv`
   - 外部AI裁决（批?3）：丢致票 PROMOTE_C07（作为防守档候，?C03 并列，不替代默认档）
   - 否决阈?v0：avg_net_pnl<=0 ?avg_net_pnl < C03*0.4 ?avg_trades < C03*0.6（用于后续自动验收）
5.4) 指标“全量扫丢遍（先留证据再整理）：从 `backtest_out\p0_sweep\**\trades_baseline_*.csv` 自动汇入场→出场（含止盈/止损/减仓原因），落盘?
   - 运行：`.\.venv\Scripts\python.exe .\backtest_p0.py indicator-audit --date YYYYMMDD`
   - 产物：`backtest_out\stage2\indicator_audit\YYYYMMDD_v1\indicator_audit_runs.csv` ?`indicator_audit_features.csv`
   - 诊断排行：`.\.venv\Scripts\python.exe .\backtest_p0.py diag-rank --date YYYYMMDD` ?`backtest_out\stage2\indicator_audit\diag_rank_YYYYMMDD_v1.csv`
   - 批次整理（用于分批讨论）：`.\.venv\Scripts\python.exe .\backtest_p0.py indicator-batches --date YYYYMMDD` ?`backtest_out\stage2\indicator_audit\YYYYMMDD_batches_v1\indicator_batches_YYYYMMDD_v1.csv`
5.4.1) 指标家族?? 批次就收缩一次（防漂移）：每完成 1? 个家族批次，更新 `02_阶段二_工作方向_想法?md` ?`UNIVERSAL_SHORTLIST_V0` ?`DEPRECATE_LIST_V0`（并保持箢短可维护?
   - B30 证据落盘（StateVector 分桶统计；用于预?过滤/加减仓角色讨论）：`.\.venv\Scripts\python.exe .\backtest_p0.py b30-evidence --date YYYYMMDD --scope core_observe --split since2022` ?`backtest_out\stage2\indicator_audit\YYYYMMDD_b30_evidence_v1\b30_bucket_stats_YYYYMMDD_v1.csv`
- B30 followups（分层稳定；基于 b30_bucket_stats ?symbol×profile ?top-vs-bot / low-vs-high 对照）：`.\.venv\Scripts\python.exe .\backtest_p0.py b30-followups --date YYYYMMDD --scope all --split since2022 --bucket_stats <b30_bucket_stats.csv>` ?`backtest_out\stage2\indicator_audit\YYYYMMDD_b30_followups_v1\b30_stability_summary_YYYYMMDD_v1.csv`
   - B40 证据落盘（E1 几何：retest bars 分桶统计；用于过?风险提示”角色讨论）：`.\.venv\Scripts\python.exe .\backtest_p0.py b40-evidence --date YYYYMMDD --scope core_observe --split since2022` ?`backtest_out\stage2\indicator_audit\YYYYMMDD_b40_evidence_v1\b40_bucket_stats_YYYYMMDD_v1.csv`
   - 批次27收口（B40 v0）：e1_retest_bars 先只做研究侧标签（不硬门控）；retest=2 标记 RISK/REDUCE 候，retest=3 标记 ENTRY_FILTER_PREFERRED，retest=1 作为 baseline
   - 批次27下一步证据：做合并桶稳定性（{1} vs {2,3} ?{<=2} vs {3}），?symbol×profile 上用 n>=20 统计方向同向占比；并?B20(e1_retest_depth_atr)/B30(sv_regime_code) 做交互分?
   - B20 证据落盘（Vol/ATR/E1 强度分桶统计；用于风?质量/过滤”角色讨论）：`.\.venv\Scripts\python.exe .\backtest_p0.py b20-evidence --date YYYYMMDD --scope core_observe --split since2022` ?`backtest_out\stage2\indicator_audit\YYYYMMDD_b20_evidence_v1\b20_bucket_stats_YYYYMMDD_v1.csv`
   - 批次25收口（B20 v0）：先把 `e1_break_strength_atr` 记为 ENTRY_FILTER 候`e1_retest_depth_atr` 记为 REDUCE/RISK 候`atr` 记为 RISK_ONLY；`entry_vol_ratio` 霢要先补齐分桶证据后再定方向（当前 b20_bucket_stats 未包含）
- 批次33收口（B20 全品种；v0 更新口径）：补齐 scope=all 的分桶证?+ symbol×profile 稳定?+ entry_vol_ratio 覆盖率审计后，调整为“先标签、后晋升”：
  - 证据：`backtest_out\stage2\indicator_audit\20260604_b20_evidence_all_v1\*`
  - 补证据：`backtest_out\stage2\indicator_audit\20260604_b20_followups_all_v1\*`
  - v0（研究侧；批?3初版）：e1_break_strength_atr=ADD_CANDIDATE；e1_retest_depth_atr=REDUCE_CANDIDATE；atr=RISK_ONLY；entry_vol_ratio=DIAG_ONLY（coverage?0% 时不允许晋升 gate?
  - 批次42复审（B20 v0 补项/纠偏；见 关于日活.md 批次42）：
    - atr=RISK_ONLY（风险环境标签；是否“更赚但更痛苦留?MAE/回撤口径?
    - e1_break_strength_atr=ADD_CANDIDATE（quality_score；不晋升 ENTRY_FILTER?
    - e1_atr_ratio=DIAG_ONLY（补项）
    - e1_retest_depth_atr=DIAG_ONLY（n_sufficient=3 冻结?
    - entry_vol_ratio=DIAG_ONLY（仅 vol_ratio_eligible 子集；coverage>=0.30?
   - B50 证据落盘（Score/Sizing 分桶统计；用于过?仓位”角色讨论）：`.\.venv\Scripts\python.exe .\backtest_p0.py b50-evidence --date YYYYMMDD --scope core_observe --split since2022` ?`backtest_out\stage2\indicator_audit\YYYYMMDD_b50_evidence_vN\b50_bucket_stats_YYYYMMDD_v1.csv`（v3 起支?size_mult=value_code 分桶?
  - 批次26收口（B50 v0）：entry_score=ENTRY_FILTER_SWEETSPOT（先排除 bin1-2；bin9-10 降级?observe 标签；不做线性越高越好门控）；size_mult=CONFIG_BUCKET（先做档位对照：size_mult=1 vs 1.15 ?stop_loss_rate/avg_pnl/tp2_rate?
  - 批次98补裁?026-06-10）：`scope=all + since2022/pre2022 + trade-level MAE/max_dd` 已完成统丢复裁；结论改写为 `entry_score=RISK_ONLY`（极?bin 风险分层/预警），不再保留 `ENTRY_FILTER_SWEETSPOT`
   - B50 followups（用于直接验收阈?档位差异）：`.\.venv\Scripts\python.exe .\backtest_p0.py b50-followups --date YYYYMMDD` ?`backtest_out\stage2\indicator_audit\YYYYMMDD_b50_followups_v1\b50_entry_score_stability_YYYYMMDD_v1.csv` ?`b50_size_mult_agg_YYYYMMDD_v1.csv`（若 size_mult=1 样本极少则仅保留为配置标签）
   - 批次27证据已跑完（B40 followups：合并桶稳定?+ 与B20/B30交互分层）：
     - `backtest_out\stage2\indicator_audit\20260603_b40_followups_v1\b40_stability_summary_20260603_v1.csv`
     - `backtest_out\stage2\indicator_audit\20260603_b40_followups_v1\b40_interaction_sv_regime_20260603_v1.csv`
     - `backtest_out\stage2\indicator_audit\20260603_b40_followups_v1\b40_interaction_depth_atr_20260603_v1.csv`
   - B99 证据落盘（stop 分位桶统计；用于“风?仓位参数”角色讨论）：`.\.venv\Scripts\python.exe .\backtest_p0.py b99-evidence --date YYYYMMDD --scope core_observe --split since2022` ?`backtest_out\stage2\indicator_audit\YYYYMMDD_b99_evidence_v1\b99_bucket_stats_YYYYMMDD_v1.csv`
   - 批次28收口（B99 v0）：stop 先定位为 RISK_ONLY；raw stop（绝对价）跨品种不可比，必须先派?stop_dist_atr=abs(entry-stop)/atr 再讨论甜点区”（朢多做轻量过滤/风险加权，不做硬门槛?
   - B99 followups（归丢?stop_dist_atr + 1.5 vs 2.0 档位对照）：`.\.venv\Scripts\python.exe .\backtest_p0.py b99-followups --date YYYYMMDD --scope core_observe --split since2022` ?`backtest_out\stage2\indicator_audit\YYYYMMDD_b99_followups_v1\b99_followups_stop_atr_summary_YYYYMMDD_v1.csv`
   - 批次28补证据结论（20260603_v1）：stop_atr=2.0 vs 1.5 的分层对照不稳定（n_pairs=13?.0 ?frac_pnl_better?.538，但 frac_both?.231）→ 暂不讨论改默认参数，仅作为配置标?风险提示保留
  - 批次43补证据（全品种；since2022）：`.\.venv\Scripts\python.exe .\backtest_p0.py b99-evidence --date 20260605 --scope all --split since2022 --out_dir .\backtest_out\stage2\indicator_audit\20260605_b99_evidence_all_v1` + `b99-followups --bucket_stats ...`（见 关于日活.md 批次43?
  - 批次43 v0：stop_dist_atr=CONFIG_BUCKET；stop_k=DEPRECATE（别名）；risk_per_trade=DIAG_ONLY?.5 vs 2.0 不做全局默认推荐（pnl 对半、稳定不足）
   - 批次30证据（diag_followups：profile 内跨 symbol ?qtiles4 分位桶）：`.\.venv\Scripts\python.exe .\backtest_p0.py diag-followups --date YYYYMMDD --scope all --split since2022` ?`backtest_out\stage2\indicator_audit\YYYYMMDD_diag_followups_v1\diag_followups_bucket_stats_YYYYMMDD_v1.csv`
   - 批次30收口（v0）：diag_session_skew_ratio 先做 REDUCE_CANDIDATE；diag_session_pnl_london/kd_1d_k_median ?DIAG_ONLY（）；diag_entry_n 固定 DIAG_ONLY（滞后诊断）
   - 批次30下一步最小证据（NEED_EVIDENCE）：基于 trades_baseline_* 生成 entry_session(Asia/London/NY) 并做 “London-only vs 全时段?的笔对照（用于把 session ?diag 从品种画像推进到“入场时点过滤）
   - 批次31证据已跑完（B10_SESSION：entry_time→session 逐笔分层）：`.\.venv\Scripts\python.exe .\backtest_p0.py b10-evidence --date YYYYMMDD --scope core_observe --split since2022` ?
     - `backtest_out\stage2\indicator_audit\YYYYMMDD_b10_evidence_v1\b10_bucket_agg_YYYYMMDD_v1.csv`
     - `backtest_out\stage2\indicator_audit\YYYYMMDD_b10_evidence_v1\b10_london_vs_all_summary_YYYYMMDD_v1.csv`
     - 验收优先看：London avg_pnl 是否显著 > ALL；以?london_vs_all_summary ?frac_pnl_better / frac_stop_loss_better
   - 批次40补证据（B10_SESSION；全品种；since2022）：`.\.venv\Scripts\python.exe .\backtest_p0.py b10-evidence --date 20260605 --scope all --split since2022 --out_dir .\backtest_out\stage2\indicator_audit\20260605_b10_evidence_all_v1`（见 关于日活.md 批次40收口?
   - 批次40 v0：entry_session=DIAG_ONLY；London=ADD_CANDIDATE（弱，不?London-only）；Asia/NY=DIAG_ONLY（trade-off 强；未补 MAE 前不?RISK?
   - 批次32证据（ADX/EMA/KD/vol_state；全品种；profile 内跨 symbol 分位桶）?
    - 跑法：`.\.venv\Scripts\python.exe .\backtest_p0.py diag-followups --date YYYYMMDD --scope all --split since2022 --diag-cols "diag_ema144_regime_long_frac,diag_kd_4h_k_median,diag_kd_1d_k_median,diag_kd_align_3tf_frac,diag_vol_state_squeeze_frac,diag_adx_median,diag_adx_strong_frac,diag_adx_trend_frac"`
     - 产物：`backtest_out\stage2\indicator_audit\YYYYMMDD_diag_followups_vN\diag_followups_bucket_stats_YYYYMMDD_v1.csv`（同目录还有 feature_summary/corr?
    - 关键去重验收：批?2/41 已确?`diag_ema_stack_bull_frac` ?`diag_ema144_regime_long_frac` 完全同构（spearman=1.0）→ 后续只保?ema144_regime_long_frac
     - v0（研究侧）：ema144_regime_long_frac=ADD/REDUCE 候；kd_4h=DIAG_ONLY（与 kd_1d 高相关）；vol_state_squeeze_frac=RISK_ONLY(regime_tag)；adx*=DIAG_ONLY
     - 下一步最小证据：NEED_EVIDENCE（交易级）把 EMA/KD/vol_state ?entry-time 状落?trades_baseline（笔分桶），验证能否做入场过?风险加权
   - 批次41去重收口（DIAG_TOP_DEDUP）：DEPRECATE `diag_ema_stack_bull_frac`；London 计数三件套只保留 `diag_session_entry_vol_ratio_london_n`（`count_london`/`trades_london` 同构?
  - 批次44补证据（B60_SWING_LEVELS；全品种；since2022；profile 合并 A_all + min_n=10）：`.\.venv\Scripts\python.exe .\backtest_p0.py b60-evidence --date 20260606 --scope all --split since2022 --q 4 --out_dir .\backtest_out\stage2\indicator_audit\20260606_b60_evidence_all_v3` + `b60-followups --min-n 10 --profile-merge 1 --bucket_stats ...`（见 关于日活.md 批次44?
- 批次44 v0：sv_risk_on_mkt=RISK_ONLY；sv_use_struct_vote=ADD_CANDIDATE；sv_swing_* = DIAG_ONLY（冻结）
- 批次44“最后一试已完成（swing_present 二桶?0260607；min_n=15）：`.\.venv\Scripts\python.exe .\backtest_p0.py b60-evidence --date 20260607 --scope all --split since2022 --q 4 --out_dir .\backtest_out\stage2\indicator_audit\20260607_b60_evidence_all_v4` + `b60-followups --min-n 15 --profile-merge 1 --bucket_stats ...` ?sv_swing_present_4h：n_sufficient=32 ?frac_both=0.5313（过阈）；解?sv_swing_* ?PENDING_DEPRECATE（仍保持 DIAG_ONLY 冻结；不晋升 gate?
 - 批次45收口（swing_present×risk_on×regime?0260607；min_n=20）：`.\.venv\Scripts\python.exe .\backtest_p0.py b60-swing-present-interaction --date 20260607 --scope all --split since2022 --min-n 20 --profile-merge 1 --out_dir .\backtest_out\stage2\indicator_audit\20260607_b60_swing_present_interaction_all_v3`（见 关于日活.md 批次45?
   - v0.2：sv_swing_present_4h=ADD_CANDIDATE（条件型：仅 risk=1&regime!=0 允许加分；其余环?DIAG_ONLY；不做过滤）
   - PASSED：零前视/重绘验证（prefix vs full?0260607；scope=all；samples_per_symbol=30；total_sampled=960；total_mismatch=0）：`.\.venv\Scripts\python.exe .\backtest_p0.py b60-swing-lookahead-audit --date 20260607 --scope all --split since2022 --csv_dir .\data --samples_per_symbol 30 --out_dir .\backtest_out\stage2\indicator_audit\20260607_b60_swing_lookahead_audit_all_v1`
   - DONE：pre2022 稳健性对照（同向但化；不晋升过滤，仅保留条件型 ADD? trade_mae_atr/max_drawdown_per_trade（以 MAE_ATR 代理朢大不利波动；swing_present=1 更不痛苦?
  - DONE：补?swing_high/low ?pre2022 对照?0260608；profile_merge=A_all；min_n=10）：pre2022 ?frac_both ?swing_high/low 逢化到 0.250/0.267 ?保持 DIAG_ONLY（冻结）

- 批次46（资料型指标→字段落地；EASY；ALBrooks 信号棒质量评分）?
  - OUTBOUND：`临时粘贴区_外部AI与终端输?md`（BATCH_ID=20260607_v46?
  - DONE：已实现 b46-signalbar-evidence + followups，并?since2022/pre2022 全品?
  - DONE：已做交互分层（bucket<=1 vs bucket>=2；risk_on×regime；since2022/pre2022?
  - DONE：已?MAE_ATR 证据（bucket<=1 vs bucket>=2；since2022/pre2022）→ tradeoff 明显（stop_loss_rate 更好?MAE 更差）→ 维持 DIAG_ONLY（见 关于日活.md 批次46?

- 批次47（资料型指标→字段落地；ALBrooks 趋势强度量化评分）：
  - DONE：已实现 b47-trend-strength-evidence + followups，并?since2022/pre2022 全品?
  - DONE：followups bucket 采用合并桶（code4<=1 vs code4>=2）避免极端桶样本不足
  - CLOSE：两个字段均暂定 DIAG_ONLY（见 关于日活.md 批次47；spearman ?pnl? 且与 entry_score?.35?

- 批次48（资料型指标→字段落地；ALBrooks 趋势回调量化规则）：
  - DONE：已实现 b48-trend-pullback-evidence + followups，并?since2022/pre2022 全品?
  - CLOSE：全?DIAG_ONLY（主问题=?0 桶覆盖极低，无法形成可晋升的稳定性证据；?关于日活.md 批次48?

- 批次49（资料型指标→字段落地；ALBrooks 交易区间量化判定）：
  - DONE：已实现 b49-trading-range-evidence + followups，并?since2022/pre2022 全品?
  - CLOSE：全?DIAG_ONLY（稳定不足以晋升 gate/加分；见 关于日活.md 批次49?

- 批次50（资料型指标→字段落地；ALBrooks 交易区间陷阱与假突破识别）：
  - DONE：已实现 b50r-range-trap-evidence + followups（命令名 b50r-* 用于避开既有 b50-* 冲突），并跑 since2022/pre2022 全品?
  - CLOSE：全?DIAG_ONLY（trap_flag 过稀；trap_score 收益与止损口径不丢致；?关于日活.md 批次50?

- 批次51（资料型指标→字段落地；ALBrooks 反转量化识别与入场规则）?
  - DONE：已实现 b51-reversal-evidence + followups，并?since2022/pre2022 全品?
  - CLOSE：全?DIAG_ONLY（信号过稢导致 n_sufficient=0；见 关于日活.md 批次51?

6) 外部参吸收（2026-06-08；先停指标批次推进，转入“资料→可落盘计划）
- 本地金融?数据中台（参考：教你如何搭建本地股票数据中心）：把拉取→去重→补缺→校对→版本化产物”落到数据层，作为后续题?财报/概念映射的底座（?想法?0.2?
- 题材赛道/产业链结（参考：储能产业何去何从？）：定义题材周报结构化模板 + 朢小可行数据来源与验收（见 想法?0.2?
- 付费AI群对标（参：大A社群会员说明）：定义我们自己的交付物（信号单/日报/复盘单）与证据链，不启用任何默认自动交易（见 想法?0.2?
- TK 外汇体系字段化：先把 IB/DB/CB + FIB 出场计划字段化（DIAG），再决定是否做全品种回测；用户目标路径 `00_TK外汇` 当前不存?为空，暂?`参视频（整理后删除）\tk外汇\*` 作为源材料（?想法?0.2?

- 批次52（资料型指标→字段落地；ALBrooks 总在场内 Always-In 状判定）?
  - DONE：已实现 b52-always-in-evidence + followups，并?since2022/pre2022 全品?
  - CLOSE：agree_side=ENTRY_FILTER_CANDIDATE（已?MAE/max_dd，但不足以晋升可讨论硬门控；其余字段 DIAG_ONLY；见 关于日活.md 批次52?

- 批次53（资料型指标→字段落地；ALBrooks 趋势棒与十字星量化定义）?
  - DONE：已实现 b53-trendbar-doji-evidence + followups，并?since2022/pre2022 全品?
  - CLOSE：全?DIAG_ONLY（趋势棒/十字星作为基硢形标签，当前稳定性不足以晋升 gate/加分；见 关于日活.md 批次53?

- 批次54（资料型指标→字段落地；威科?弹簧Spring/上抛UT 量化判定）：
  - DONE：已实现 b54-wyckoff-spring-ut-evidence + followups，并?since2022/pre2022 全品?
  - CLOSE：全?DIAG_ONLY（信号过稢；repeat 分段不稳健；?关于日活.md 批次54?
  - MARKER: REOPEN_ON_A_SHARES_EXCHANGE_VOLUME（外?指数/大宗：不讨论晋升；A股数据接入后重开该家族并升级“成交量”为硬约束再回测?
 
- 批次55（资料型指标→字段落地；补充抢术_价格形识别（吞没/锤子?射击之星））?
  - DONE：已实现 b55-candle-patterns-evidence + followups，并?since2022/pre2022 全品?
  - CLOSE：全?DIAG_ONLY（since2022/pre2022 分段方向不一致；?关于日活.md 批次55?

- 批次56（资料型指标→字段落地；斐波那契回调位（0.236/0.382/0.5/0.618/0.786））?
  - DONE：已实现 b56-fib-retrace-evidence + followups，并?since2022/pre2022 全品?
  - CLOSE：全?DIAG_ONLY（桶内样本不?分段不稳健；?关于日活.md 批次56?

- 批次57（资料型指标→字段落地；KD 钝化/脱离钝化?D 对齐 1H；按方向?favor/unfavor））?
  - DONE：已实现 b57-kd-saturation-evidence + followups，并?since2022/pre2022 全品?
  - CLOSE：全?DIAG_ONLY（coverage/分段弱；exit 过稀；见 关于日活.md 批次57?

- 批次58（资料型指标→字段落地；EMA 支撑/阻力的回收（touch/fake_break/reclaim））?
  - DONE：已实现 b58-ema-reclaim-evidence + followups，并?since2022/pre2022 全品?
  - CLOSE：全?DIAG_ONLY（touch/fake_break 过稀；reclaim/score 分段弱；?关于日活.md 批次58?

- 批次59（资料型指标→字段落地；EMA20 斜率/相对位置 + 日线EMA200宏观侧（对齐?H））?
  - DONE：已实现 b59-ema-regime-evidence + followups，并?since2022/pre2022 全品?
  - CLOSE：全?DIAG_ONLY（分段弱/不晋升；?关于日活.md 批次59?

- 批次61（资料型指标→字段落地；KD 背离（顶背离/底背离；1D pivot + 次日反转K线确认；对齐?H））?
  - DONE：已实现 b61-kd-divergence-evidence + followups，并?since2022/pre2022 全品?
  - CLOSE：全?DIAG_ONLY（信号极稢；n_sufficient=0；见 关于日活.md 批次61?
 
- 批次62（资料型指标→字段落地；KD 基础极（1D K 对齐 1H；按方向?favor_k 分桶/极标记））：
  - DONE：已实现 b62-kd-basic-evidence + followups，并?since2022/pre2022 全品?
  - CLOSE：全?DIAG_ONLY（分段弱/或过稢；见 关于日活.md 批次62?

- 批次63（资料型指标→字段落地；KD 多周期对齐（1D + 4H K 对齐 1H；按方向统计 favor/unfavor））?
  - DONE：已实现 b63-kd-multitf-align-evidence + followups，并?since2022/pre2022 全品?
  - CLOSE：全?DIAG_ONLY（分段弱/或过稢；见 关于日活.md 批次63?

- 批次64（资料型指标→字段落地；KD + MACD 共振?D；对?1H））?
  - DONE：已实现 b64-kd-macd-resonance-evidence + followups，并?since2022/pre2022 全品?
  - CLOSE：全?DIAG_ONLY（分段弱/或过稢；见 关于日活.md 批次64?

- 批次65（资料型指标→字段落地；1H 成交量形态（volume/MA ratio：dryup/spike + 分桶））?
  - DONE：已实现 b65-volume-patterns-evidence + followups，并?since2022/pre2022 全品?
  - CLOSE：全?DIAG_ONLY（volume 口径不稳，不允许晋升；见 关于日活.md 批次65；MARKER: REOPEN_ON_A_SHARES_EXCHANGE_VOLUME?

- 批次66（资料型指标→字段落地；RSI 基础极（1D RSI 对齐 1H；按方向?favor_rsi 分桶/极标记））：
  - DONE：已实现 b66-rsi-basic-evidence + followups，并?since2022/pre2022 全品?
  - CLOSE：DIAG_ONLY（偏风险侧但未补 MAE/maxDD，不晋升；见 关于日活.md 批次66?

- 批次67（资料型指标→字段落地；CCI 基础极（1D CCI 对齐 1H；按方向?favor_cci 分桶/极标记））：
  - DONE：已实现 b67-cci-basic-evidence + followups，并?since2022/pre2022 全品?
  - CLOSE：DIAG_ONLY（分段方向不?且未?MAE/maxDD，不晋升；见 关于日活.md 批次67?

- 批次68（补证据：RSI/CCI 风险侧验证；trade_mae_atr / trade_mfe_atr）：
  - DONE：已实现 b68-osc-mae-evidence，并?since2022/pre2022 全品种（profile_merge=1?
  - CLOSE：RSI=RISK_ONLY_CANDIDATE（MAE+止损改善可复现；不做?gate）；CCI 维持 DIAG_ONLY（见 关于日活.md 批次68?

- 批次69（弱过滤模拟：RSI bucket 避开朢差桶；keep/drop 对照）：
  - DONE：已实现 b69-rsi-filter-sim-evidence，并?since2022/pre2022 全品种（drop_bucket=0?
  - CLOSE：进入可讨论的弱门槛候（避开 bucket=0 在两段复现；但仍不接入执行门控；?关于日活.md 批次69?

- 批次70（弱过滤模拟：CCI bucket 避开朢差桶；keep/drop 对照）：
  - DONE：已实现 b70-cci-filter-sim-evidence，并?since2022/pre2022 全品种（drop_bucket=0?
  - CLOSE：pre2022 ?MAE 方向不支??不作为弱门槛候；维持 DIAG_ONLY（见 关于日活.md 批次70?

- 批次71（真 gate 验证：RSI bucket 端到端重跑对照；drop_bucket=0）：
  - DONE：已实现 b71-rsi-truegate-sweep，并?since2022/pre2022 全品种（min_window_days=365；A_universal 参数集）
  - CLOSE：两?agg 平均口径?net_pnl ?max_dd 同向改善 ?弱门?ENTRY_FILTER_CANDIDATE（研究侧；默认不启用；见 关于日活.md 批次71?

- 批次72（真 gate 作用域拆解：?E1 vs ?E2）：
  - DONE：已完成 E1-only / E2-only 对照（since2022/pre2022?
  - CLOSE：E2-only ?pre2022 逢??若启用仅?gate_scope=E1（见 关于日活.md 批次72?

- 批次73（RSI(E1-only) × C03(squeeze-only) 叠加验证）：
  - DONE：已完成 since2022/pre2022 端到端对?
  - CLOSE：pre2022 收益侧??不晋升叠加组合（?关于日活.md 批次73?

- 批次74（RSI(E1-only) × C07(squeeze+kd_3tf) 叠加验证）：
  - DONE：已完成 since2022/pre2022 端到端对?
  - CLOSE：pre2022 收益侧??不晋升叠加组合（?关于日活.md 批次74?

- 批次75（RSI(E1-only) ?gate：core6 部署池视角）?
  - DONE：已完成 since2022/pre2022 对照
  - CLOSE：pure core6 样本小且 pre2022 逢??不单独晋升部署池门槛（见 关于日活.md 批次75?

- 批次76（RSI(E1-only) ?gate：core6+observe7 部署池视角）?
  - DONE：已完成 since2022/pre2022 对照
  - DONE：已?`scope=all` ?since2022/pre2022 全局复跑
  - CLOSE：局?`core6+observe7` 口径曾两段支持，但全屢复跑逢化为 since2022 微弱正pre2022 转负?dd 也不再改?
  - CLOSE：不再保留全屢部署池口径，仅保留局部历史备?

- 批次77（RSI(E1-only) × C03：core6+observe7 视角）：
  - DONE：已完成 since2022/pre2022 对照
  - DONE：已?`scope=all` ?since2022/pre2022 全局复跑
  - CLOSE：全屢复跑?since2022 仍偏正，?pre2022 变成“dd 改善、收益均值化的分裂结构
  - CLOSE：降级为 `RESEARCH_COMBO / DIAG_ONLY`，不列入通用 shortlist

- 批次78（RSI(E1-only) × C07：core6+observe7 视角）：
  - DONE：已完成 since2022/pre2022 对照
  - DONE：已?`scope=all` ?since2022/pre2022 全局复跑
  - CLOSE：全屢复跑?since2022 仍有收益/回撤双改善，?pre2022 收益逢化比批次77更明?
  - CLOSE：保留更偏防守的研究组合”备注，但同样降级为 `RESEARCH_COMBO / DIAG_ONLY`

- 批次79（RSI(E1-only) × C03：core6 视角）：
  - DONE：已完成 since2022/pre2022 对照
  - CLOSE：两段都支持?dd 变小 ?可列?core6 研究候组合（?关于日活.md 批次79?

- 批次80（RSI(E1-only) × C07：core6 视角）：
  - DONE：已完成 since2022/pre2022 对照
  - CLOSE：since2022 支持?pre2022 明显逢??不列?core6 通用候组合（?关于日活.md 批次80?

- 批次81（RSI 部署池收缩批 + MT 指标家族映射 v1）：
  - DONE：已完成批次75-80 的部署池收缩裁决
  - CLOSE：core6 仅保?`RSI(E1-only) × C03` 为研究；`C07` 不列?core6 通用候组合（?关于日活.md 批次81?
  - DONE：已落盘 `00_指标定义&公式\MT指标家族映射_v1.md`
  - NOTE：截至当前，批次推进与收口已做到批次81?1 为收缩批/工程化批，便于后续复?

- 批次82（Volty Stop 字段实现 v1）：
  - DONE：`backtest_p0.py` 已新?`b82-volty-stop-fields`
  - DONE：已产出 core6 since2022/pre2022 双窗口证?
  - CLOSE：Volty 当前只保?`RISK / EXIT / REGIME_DIAG` 角色，不列为默认 entry gate 候（?关于日活.md 批次82?
  - NOTE：summary 先按探索性聚合解释；若要晋升，需?latest-run 去重口径

- 批次83（ZZ Ratio 字段实现 v1 + Volty latest-run 去重）：
  - DONE：`backtest_p0.py` 已新?`b83-zz-ratio-fields`
  - DONE：已产出 ZZ Ratio core6 since2022/pre2022 双窗口证?
  - DONE：已完成 Volty strict `latest_only=1` 双窗口重跑，产物位于 `20260610_b82_volty_stop_fields_core6_*_latest_strict_v2`
  - CLOSE：ZZ Ratio 只保?`DIAG_ONLY`；Volty 不进通用 shortlist，仅保留 `REGIME_DIAG / RISK_CONTEXT` 观察候?

- 批次84（Volty trend_align followups + Harmony 非重绘确认时点定义60）：
  - DONE：已完成 `volty_trend_align_1h` ?pairs/followups 双窗口证据（core6；since2022/pre2022?
  - DONE：已基于 strict latest-only 输入重跑 B84；结论不?
  - DONE：已?`0_Harmony_06` 的非重绘确认时点”定义60写入 `00_指标定义&公式\MT指标家族映射_v1.md`
  - CLOSE：`volty_trend_align_1h` 继续只保?`REGIME_DIAG / RISK_CONTEXT`；`0_Harmony_06` 继续只保?`DIAG_ONLY / SOURCE_LIBRARY`
  - NEXT：若继续推进 Volty，只值得做与 MAE/回撤口径的交互复核；不是再讨论其 entry gate 晋升

- 批次85（Volty trend_align × MAE / max_drawdown_per_trade 交互复核）：
  - DONE：`backtest_p0.py` 已新?`b85-volty-trend-align-mae`
  - DONE：已基于 strict latest-only ?`b82_trade_features` 跑出 since2022/pre2022 双窗口证?
  - CLOSE：`align=1` ?since2022 更像“更不痛?/ 更少 hit stop”的风险侧标签，但收益不占优；继续只保留 `REGIME_DIAG / RISK_CONTEXT`
  - NEXT：如果还要继?Volty，只允许徢 `sizing / reduce / exit context` 补证据，不再讨论 entry gate 晋升

- 批次86（Volty align × stop_dist_bucket × MAE；下丢优先级最高）?
  - DONE：`backtest_p0.py` 已新?`b86-volty-align-stopdist-mae`
  - DONE：已基于 strict latest-only ?`b82_trade_features` 跑出 since2022/pre2022 双窗口证?
  - CLOSE：首?sizing 证据不足；since2022 ?`align=0` ?`n_pairs=15 / n_sufficient=1 / frac_pnl_better=0 / frac_stop_loss_better=0 / frac_mae_better=1 / frac_all3_better=0`，pre2022 ?`n_sufficient=0`
  - CLOSE：`align=1` 基本逢化为 `stop_bucket=3`（since2022 聚合?`bucket2/3=4 / 2883`），说明在最想服?sizing 的顺势环境里，`stop_dist_bucket` 暂不具备可用分层
  - NEXT：`volty_stop_dist_bucket_1h` 暂不晋升 `CONFIG_BUCKET`，继续保留为 `SIZING_CANDIDATE（冻结）`；下丢步转批次87 `align × hold_hours`

- 批次87（Volty align × hold_hours；服?reduce / 提前减仓）：
  - DONE：`backtest_p0.py` 已新?`b87-volty-align-holdhours`
  - DONE：已基于 strict latest-only ?`b82_trade_features` 跑出 since2022/pre2022 双窗口证?
  - CLOSE：未发现“持仓后?pain-up but pnl-flat/down”的通用提前减仓证据；`align=0` 两段?`n_sufficient=0`
  - CLOSE：`align=1` 在两段均表现?`late(>=24h)` 相对 `early(<=6h)` 的收益更好止损率更低（多数），但 MAE 更大（更痛苦）→ 属于 trade-off，不晋升 REDUCE 规则
  - NEXT：转批次88 `align × exit context`，把 Volty 用于 trailing/close 逻辑，不是用 hold_hours ?reduce

- 批次88（Volty align × exit context；服?trailing / close 逻辑）：
  - DONE：`backtest_p0.py` 已新?`b88-volty-align-exit-context`
  - DONE：已基于 strict latest-only ?`b82_trade_features` 跑出 since2022/pre2022 双窗口证?
  - NOTE：由?`b82_trade_features` 缺少 trailing/partial-close 的真实出场语境字段，本批先用 proxy exit_context（由 `stop_loss_any/tp2_any/win` 派生）代?
  - CLOSE：proxy 口径?`align=1` 更常见stop_loss 更低、tp2 更高”，但不足以支持?trailing/close 逻辑（缺少真?exit_reason 维度?
  - CLOSE2：多AI收口 5/5 ?`Q1=B`，同意只继续丢次真?exit_context 字段化，其余 entry/sizing/reduce 路线冻结
  - NEXT：已转批?9，补真实字段并重跑真 b88

- 批次89（Volty true exit context replay；真?exit 字段）：
  - DONE：`backtest_p0.py` 已把真实 exit 字段写入 `b82_trade_features`：`exit_reason_final / exit_reason_group / close_partial_any / trail_stop_hit_any / bars_to_exit / trade_mae_atr / trade_mfe_atr`
  - DONE：`backtest_p0.py` 已新?`b88t-volty-align-exit-context-true`
  - DONE：已?`core6` ?`core6+observe7` ?since2022/pre2022 ?b88 证据
  - CLOSE：真 b88 推翻?proxy 里的“更?tp2”乐观结论；稳定留下的是 `final stop_loss` 更低、`close_partial_any` 更高、`MAE` 更低
  - CLOSE：`tp2_final` 没有提升、`trail_stop_final` 只有弱改??Volty 不晋?`TRAILING_OPTIMIZER`
  - NEXT：转批次90 让多AI裁决“是否再?drawdown_duration?

- 批次90（Volty freeze or pivot；旧否决池重弢裁决）：
  - DONE：已向多AI发出 `v47-v80 旧否决池是否重开 + Volty 下一步二选一` 的统丢 OUTBOUND，并完成回帖收口
  - CLOSE：多AI多数票支?`Q1=B` ?Volty 暂不继续?`max_duration_in_drawdown / drawdown_duration`，现阶段直接冻结?`RISK_CONTEXT / EXIT_CONTEXT_HINT`
  - CLOSE：多AI丢致反对旧否决池批量重弢；本轮不新开 `trend_strength / range / EMA / CCI` 批次
  - CLOSE：永久冻结桶已明确为：过稢型（48/51/54/61）跨窗口翻转型（55）volume 口径不稳型（65?
  - NEXT：若未来出现新数据源/新口径，仅按想法库里?`REOPEN_FREEZE_RULES_V1` 条件重开；当前执行队列不包含 Volty drawdown_duration 与旧否决池重弢

- 批次91（Volty drawdown_duration；按 Kimi 建议的最后一轮）?
  - DONE：`backtest_p0.py` 已把 `max_drawdown_duration_hours / drawdown_duration_hours_total` 写入 `b82_trade_features`
  - DONE：`backtest_p0.py` 已新?`b90d-volty-drawdown-duration`
  - DONE：已?`core6` ?`core6+observe7` ?since2022/pre2022 双窗口证?
  - CLOSE：`drawdown_duration` 没有形成?Volty 的新增正向信息；since2022 `frac_dd_duration_better` ?`0.167~0.318`
  - CLOSE：Volty 保持冻结；不再继续挖 duration ?

- 批次92（Trend Strength reopen；按 DeepSeek 建议低成本复核）?
  - DONE：已复跑 `b47-trend-strength-evidence + b47-followups`（core6+observe7，since2022/pre2022?
  - CLOSE：低成本重开未翻案；since2022 `top_minus_bot_avg_pnl<0`、pre2022 `>0`，继续跨窗口翻转
  - CLOSE：`spearman(trade_pnl)?`、`spearman(entry_score)?.32~0.37`，同?无效问题仍在
  - NEXT：`trend_strength` 不进入当前执行队列；仅在 `entry_score` 明显解后再讨?

- 批次93（Range Trap × MAE；补风险侧复核）?
  - DONE：`backtest_p0.py` 已新?`b93-range-trap-mae`
  - DONE：已?`core6+observe7` ?since2022/pre2022 双窗口证?
  - DONE：已?`scope=all` ?since2022/pre2022 全局复跑
  - CLOSE：`range_trap` 补完 `MAE` 后仍未翻案；`trap_score` 仍表现为收益侧最多略偏正、但 `stop_loss / MAE` 不同步改?
  - CLOSE：全屢复跑?`trap_repeat` 仍是相对朢强片段，?`stop_loss` 改善不足，仍不支?`RISK_AVOID / REDUCE`
  - CLOSE：`trap_repeat` ?since2022 ?`MAE` 有局部改善，?`stop_loss` 改善偏弱，pre2022 不能复现
  - NEXT：`range / range_trap` 暂不再优先推进；若未来要重开，需统一更强?`max_dd/regime` 交互口径

- 批次94（EMA family：MAE × regime 交互口径）：
  - DONE：`backtest_p0.py` 已新?`b94-ema-family-mae-regime`
  - DONE：已?`core6+observe7` ?since2022/pre2022 双窗口证据（profile_merge=1?
  - DONE：已?`scope=all` ?since2022/pre2022 全局复跑
  - CLOSE：宏观侧 `ema200_side/ema20_gt_ema200` ?`risk=0 & regime=0` 下出现收?风险更好”的条件化片段，但不具备通用晋升路径
  - CLOSE：全屢复跑后条件化正向片段?`reclaim` 负向片段都保留，原裁决不?
  - CLOSE：`ab_ema_reclaim_*` ?`risk=1 & regime=2` 出现明显负向片段，不晋升
  - NEXT：EMA family 继续 `DIAG_ONLY`；仅允许条件化复盘标签，不进通用 shortlist

- 批次95（E1 Break Strength × MAE；补“更赚但更痛苦复核）?
  - DONE：`backtest_p0.py` 已新?`b95-e1-break-strength-mae`
  - DONE：已?`core6+observe7` ?since2022/pre2022 双窗口证据（min_n=10?
  - DONE：已?`scope=all` ?since2022/pre2022 全局复跑
  - CLOSE：since2022 `frac_pnl_better?.610` ?`frac_stop_loss_better?.458 / frac_mae_better?.407`，偏 trade-off
  - CLOSE：全屢复跑?since2022 收敛?`?.563 / 0.403 / 0.412`，收益优势被摊薄，trade-off 反更?
  - CLOSE：pre2022 收益侧不出优势止损侧更差?MAE 偏好，分裂不支持 gate
  - NEXT：`e1_break_strength_atr` 维持 `ADD_CANDIDATE（quality_score）`，不晋升 ENTRY_FILTER；若要做弱门槛需先出现强稳定性或明确条件化片?

- 批次96（Session family：entry_session × MAE）：
  - DONE：`backtest_p0.py` 已新?`b96-session-mae`
  - DONE：已?`core6+observe7` ?since2022/pre2022 双窗口证据（min_n=10?
  - CLOSE：`London` 收益/stop_loss 偏正，但 MAE 不跟随，继续只保留弱 `ADD_CANDIDATE`
  - CLOSE：`NY` ?`stop_loss / MAE` 改善很强，但收益侧不稳，收口?`RISK_CONTEXT_HINT`，不?avoid-NY 硬过?
  - CLOSE：`Asia` 三口径不稳，继续 `DIAG_ONLY`
  - NEXT：仅当后续还要继续推?session 家族时，再做 `session × vol_state / regime` 交叉；当前不进入执行侧默认改?

- 批次97（Session family：entry_session × sv_regime_code × sv_risk_on_mkt × MAE；全屢口径）：
  - DONE：`backtest_p0.py` 已新?`b97-session-regime-mae`
  - DONE：已?`scope=all` ?since2022/pre2022 双窗口证据（profile_merge=1, min_n=10?
  - NOTE：最近补证据批次里，`93/94/95/96` 都不是全屢 all，是 `core6+observe7`；本批次97已补全全屢口径
  - CLOSE：`London` 在环境分层后仍是收益/止损偏正?`MAE` 明显更差?trade-off，不晋升过滤
  - CLOSE：`NY` ?`RISK_CONTEXT_HINT` ?`risk=1, regime=1/2` 下继续成立，保留为风险标签，不转硬规?
  - NEXT：session 家族先收口，不再优先投入；若后续重开，只考虑和持仓管?逢出上下文做低成本联动验证

- 待复跑全屢清单（worth rerun；优先级从高到低）：
  - DONE：批?4（EMA family：MAE × regime）→ 已补 `scope=all`
  - DONE：批?5（E1 Break Strength × MAE）→ 已补 `scope=all`
  - DONE：批?3（Range Trap × MAE）→ 已补 `scope=all`；全屢复跑后否决结论不?
  - DONE：批?6（RSI(E1-only) ?gate：core6+observe7）→ 已补 `scope=all`；结论降级，不保留全屢候地?
  - DONE：批?7（RSI(E1-only) × C03：core6+observe7）→ 已补 `scope=all`；降级为 `RESEARCH_COMBO / DIAG_ONLY`
  - DONE：批?8（RSI(E1-only) × C07：core6+observe7）→ 已补 `scope=all`；降级为 `RESEARCH_COMBO / DIAG_ONLY`
  - COVERED：批?6 不单独复跑；其核心问题已被批?7 ?`scope=all + regime/risk` 覆盖

- 本周收缩状（2026-06-10）：
  - UNIVERSAL_SHORTLIST：收缩为 6 项（`sv_atr_ratio_1h / atr / entry_score / diag_session_skew_ratio / sv_swing_present_4h / ab_always_in_agree_side_1h`?
  - 新增 DEPRECATE? 项（`entry_session` ?shortlist 地位、`volty_stop_dist_bucket_1h` ?sizing 候地位`RSI(E1-only)` 的全屢候口径`RSI(E1-only) × C03/C07` 的全屢候组合口径`e1_break_strength_atr` ?shortlist 地位?
  - 已统丢移出 shortlist：`entry_session / volty_trend_align_1h / volty_stop_dist_bucket_1h / RSI(E1-only) ?gate / ×C03 / ×C07 / e1_break_strength_atr` 的全屢候叙?
  - DONE：`entry_score` 已由批次98 统一复裁收口，角色固定为 `RISK_ONLY`
  - DONE：`sv_atr_ratio_1h / atr` 已由批次100 统一风险复裁收口；`sv_atr_ratio_1h` 收窄?`risk=1 + regime!=0` 下的条件型弱过滤，`atr` 固定?`RISK_ONLY`
  - DONE：`diag_session_skew_ratio` 已由批次101 完成 trade-level 映射；保留为?`REDUCE_CANDIDATE`，不晋升?reduce gate
  - DONE：`ab_always_in_agree_side_1h` 已由批次102 完成屢部片段验证；?`risk=0 + regime=0` 保留条件型弱过滤，其他环境降为诊断提?
  - DONE：`sv_swing_present_4h` 已由批次99 边际贡献验证收口，保留为 `regime!=0 + entry_score=mid_bin3_8` 的条件型 ADD
  - DONE：`e1_break_strength_atr` 已由批次95+99+多AI 收口，固定为 `DIAG_ONLY`
  - DONE：`v103/v104/v105` 已完成多AI 收缩；`range_trap / CCI / KD basic / trendbar` 不再保留为旧问题
  - DONE：`b103` 已完?trend family 去重审计；`trend_strength` ?`entry_score / regime` 仅中低相关（?`0.35 / 0.20~0.33`），不是硬别名，?pooled `pnl?`
  - DONE：`b104` 已完?`ab_range_width_atr_1h / bucket` 的最后一?`MAE/max_dd × regime/risk` 审计；结?无稳定跨窗口子环境，`range_width` 永久冻结
  - DONE：`b105` 已完?`ab_trend_strength_*` 的最后一?`risk/regime × MAE/max_dd` 屢部片段验证；结论=无足够稳定的跨窗口片段，`trend_strength` 永久冻结
  - DONE：`v106` 已完?EMA residual family 多AI 收口；`ab_ema200_side_1h` 保留为唯丢 `RISK_CONTEXT_HINT`，其?EMA residual 永久冻结
  - DONE：`v107` 已完?sparse state family 多AI 收口；`pullback / reversal / always_in residual` 永久冻结
  - DONE：`v108` 已完?price pattern family 多AI 收口；`candlestick` 永久冻结，`fib_retrace_depth_1h` 仅保留纯复盘观察
  - DONE：`v109` 已完?A-shares-only markers 多AI 收口；`wy_spring_ut_* / volume family` 已转?`A_SHARES_ONLY_FUTURE_BUCKET`
  - DONE：`v110` 已完?signal quality family 多AI 收口；`ab_sig_quality_score_1h / bucket_1h` 永久冻结
  - DONE：`v111` 已完?range core residual 多AI 收口；`ab_range_flag_1h / score_1h` 永久冻结，range 家族全部收口
  - DONE：`v112` 已完?KD extended family 多AI 收口；`kd_sat / kd_div / kd_align / kd_macd_res` 永久冻结，KD 家族全部收口
  - DONE：`v113` 已完?pattern leftover 收口；`ab_doji_flag_1h` 永久冻结，`fib_retrace_depth_1h` 仅保留纯复盘观察
  - NEXT：旧问题清零；本?DIAG_POOL 收缩已全部收口；剩余仅保?`ab_ema200_side_1h`（`RISK_CONTEXT_HINT`）与 `fib_retrace_depth_1h`（纯复盘观察）两类非执行标签

- 剩余 shortlist 缺口盘点?026-06-10）：
  - NEXT_DISCUSSIONS?
    - CLOSE：`sv_atr_ratio_1h + atr` 已由 v91 + b100 收口
    - CLOSE：`diag_session_skew_ratio` 已由 v92 + b101 收口
    - CLOSE：`ab_always_in_agree_side_1h` 已由 v102 + b102 收口
    - CLOSE：`e1_break_strength_atr + sv_swing_present_4h` 已由 v93 + b99 收口
    - CLOSE：`range_trap` 已由 v104 永久冻结；不再保留旧问题
    - CLOSE：`CCI/KD basic` 已由 v105 永久冻结；不再保留旧问题
    - CLOSE：`ab_range_width_atr_1h / bucket` 已由 b104 收口并冻?
    - CLOSE：`ab_trend_strength_score_1h / bucket` 已由 b105 收口并冻?
    - CLOSE：`EMA residual / sparse state / price pattern / A-shares-only markers` 已由 v106/v107/v108/v109 收口
    - CLOSE：`signal_quality / range core residual / KD extended / doji leftover` 已由 v110/v111/v112/v113 收口

- XBreaking.ex5 朢?MT5 探针?
  - DONE：已确认 terminal/metaeditor/data path；已编译探针 EA；在 MT5 关闭后命令行 tester 已真实起?
  - CLOSE：`XBreaking.ex5` 可被 MT5 `iCustom` 加载，至?buffer0 可读（见 关于日活.md XBreaking 段）

- MT4 指标链路?
  - DONE：`VoltyChannel_Stop_v2_1M / ZUP_v15[1][1].1 / 0_Harmony_06 / a_ZZ` 已可在当?MT4 编译器下通过（Harmony/a_ZZ 已修保留字冲突）
  - DONE：命令行 tester 已过 portable + 登录上下?+ history 映射真实起跑，并已产?smoke/Volty tester report（见 关于日活.md MT4 段）
  - DONE：`MT4_probe_Volty_*.csv` 已落盘到 `03_MT4便携探针实例\tester\files\MT4_probe_Volty_EURUSD_H4_20250102_000000.csv`
  - CLOSE：卡点已从tester/CSV 落盘”切换为“如何把 probe 结果转成稳定字段/家族映射?

- MT 指标工程化（Volty v0）：
  - DONE：已?`Volty Stop` 写入 `00_指标定义&公式\MT指标家族映射_v1.md`
  - DONE：已完成字段实现 v1，并落盘 `b82_trade_features / b82_feature_summary / b82_coverage`
  - CLOSE：当前定位为 `RISK / EXIT / REGIME_DIAG`，不直接?entry gate

- MT 指标工程化（ZZ Ratio v0）：
  - DONE：已完成字段实现 v1，并落盘 `b83_trade_features / b83_feature_summary / b83_coverage`
  - CLOSE：当前只保留 `DIAG_ONLY`
   - 全品种证据补齐（scope=all；since2022；用于后续组合讨论）?
     - `backtest_out\stage2\indicator_audit\20260604_b20_evidence_all_v1\*`
     - `backtest_out\stage2\indicator_audit\20260604_b30_evidence_all_v1\*`
     - `backtest_out\stage2\indicator_audit\20260604_b40_evidence_all_v1\*`
     - `backtest_out\stage2\indicator_audit\20260604_b50_evidence_all_v1\*`
  - 批次34收口（B30/B40/B50；全品种；v0）：按先标签、后晋升”的门槛（frac_both>=0.60）收口，避免直接硬门控：
    - B30：sv_regime_code=ENTRY_FILTER；sv_atr_ratio_1h=RISK_ONLY（初版）；sv_bb_ratio_4h=DIAG_ONLY（初版）；sv_votes_long_4=DIAG_ONLY（代表字段）；sv_votes_short_4=DIAG_ONLY
     - B40：e1_retest_bars=DIAG_ONLY（scheme=1_vs_ge2；bars=1 preferred 标签?=2 风险提示候；稳定性达标前不晋升）
     - B50：entry_score=RISK_ONLY（极?bin 警示）；size_mult=CONFIG_BUCKET
  - 批次38收口（B30 两个波动相关特征补证据后 v0 更新）：
    - sv_atr_ratio_1h：ENTRY_FILTER（弱门槛：避免最?1/4；方?高更好；证据=deciles10 合并?q10→q4 ?frac_both?.658?
    - sv_bb_ratio_4h：DIAG_ONLY（收益与 MAE 口径不一致：不晋升过?风险门控?
    - NEED_EVIDENCE：trade_mae_atr / max_drawdown_per_trade（用于决定是否把“弱门槛”升级为硬过滤）
   - 下一批未覆盖指标家族（批?5：B60_SWING_LEVELS；sv_swing_high_4h / sv_swing_low_4h）：
     - 跑法：`.\.venv\Scripts\python.exe .\backtest_p0.py b60-evidence --date YYYYMMDD --scope all --split since2022` ?`backtest_out\stage2\indicator_audit\YYYYMMDD_b60_evidence_all_v1\b60_feature_summary_YYYYMMDD_v1.csv`
     - 分层稳定：`.\.venv\Scripts\python.exe .\backtest_p0.py b60-followups --date YYYYMMDD --scope all --split since2022` ?`backtest_out\stage2\indicator_audit\YYYYMMDD_b60_followups_all_v1\b60_stability_summary_YYYYMMDD_v1.csv`
     - v0（当前收口）：两者先 DIAG_ONLY（全品种分层 n_sufficient 很低；禁止晋?gate?
     - 朢小补证据：profile 合并 + ?symbol 桶门槛放宽到 n>=10 + binary 分桶 + split 扩展?pre2022/full 后，再看 n_sufficient>=15 ?frac_both>=0.30 是否成立
     - 补充（v2）：b60-evidence 支持 True/False 字段→code 分桶（sv_risk_on_mkt / sv_use_struct_vote）；b60-followups 支持 `--min-n` ?`--profile-merge`
   - 组合验证 v0（全品种；先验证“标签组合是否一致改善，不改执行默认）：
     - 跑法：`.\.venv\Scripts\python.exe .\backtest_p0.py combo-v0 --date YYYYMMDD --scope all --split since2022` ?`backtest_out\stage2\indicator_audit\YYYYMMDD_combo_v0_all_v1\combo_v0_bucket_stats_YYYYMMDD_v1.csv`
    - 已补?0260607 combo_v0 v3 纳入 swing_present 分组（见 关于日活.md 批次44补证据段）：`backtest_out\stage2\indicator_audit\20260607_combo_v0_all_v3\*`
   - 新指标家族（B31_STRUCT_VOTE_WINDOW；votes_3 vs votes_4 去重验证）：
     - 跑法：`.\.venv\Scripts\python.exe .\backtest_p0.py b31-evidence --date YYYYMMDD --scope all --split since2022` ?`backtest_out\stage2\indicator_audit\YYYYMMDD_b31_evidence_all_v1\b31_feature_summary_YYYYMMDD_v1.csv`
     - 分层稳定：`.\.venv\Scripts\python.exe .\backtest_p0.py b31-followups --date YYYYMMDD --scope all --split since2022` ?`backtest_out\stage2\indicator_audit\YYYYMMDD_b31_followups_all_v1\b31_stability_summary_YYYYMMDD_v1.csv`
     - v0（批?9收口；研究侧）：整体区分力很弱（top_minus_bot?30 级别）→ 全部 DIAG_ONLY；去重：sv_votes_long_3/short_3=DEPRECATE；sv_bias ?sv_votes_long_4 同构（二选一；默认保?sv_votes_long_4 作为代表字段?
   - 新指标家族（批次37：B99_PARAMS；stop_k / risk_per_trade）：
     - 跑法：`.\.venv\Scripts\python.exe .\backtest_p0.py b99-evidence --date YYYYMMDD --scope all --split since2022` ?`backtest_out\stage2\indicator_audit\YYYYMMDD_b99_evidence_all_vN\b99_feature_summary_YYYYMMDD_v1.csv`（value_code 会包?stop_k/risk_per_trade?
6) 诊断标签（TOP4，先诊断不门控）：统丢 `diag_*` schema(v0) 并落盘到 `baseline_metrics.csv` ?`p0_sweep_summary.csv`
   - TOP4：波动率状（SQUEEZE/EXPANDING/NORMAL? 量能参与（tick_volume ?entry_vol_ratio? session（Asia/London/NY? ADX（先占位，后实现?
   - 本轮新增并已验收进入 `p0_sweep_summary.csv`：`diag_vol_transition`、`diag_session_entry_vol_ratio`（含 Asia/London/NY median ?n?
   - 本轮新增并已验收进入 `p0_sweep_summary.csv`：`diag_adx_*`、`diag_ema144_regime_*`、`diag_ema_stack_*`、`diag_kd_align_*`（均?entry_time 抽样统计；先诊断不门控）
   - 本轮新增并已验收进入 deploy 表：`diag_vol_state_gate`（core 默认 C03_SQUEEZE_ONLY；observe/exclude ?NONE?
   - 朢小验收：?symbol+profile+split 分组统计；样本不足（入场<50）标?insufficient_data，不允许硬结?
7) 观点/叙事账本（可证伪，允许当下不可验证）：把“热议观?假设”落盘为可追踪条目，按周复核（承载方案见 `02_阶段二_工作方向_想法?md` ?0.0.4?
8) 指标组合研究（主?附图互指 + 大周期引小周期）：把“指标择/调参”扩展为“组合结构的实验与对比（承载方案?`02_阶段二_工作方向_想法?md` ?0.0.5?
9) 每周落盘（复盘可追溯）：`review\inventory_YYYYMMDD.md` / `review\gates_YYYYMMDD.md`（只写产物路?复现命令+本周踩坑”）
10) 资讯阅读/下班搭子（只读，不驱动交易）：把“新?研报/宏观要点”落成可证伪条目，只允许触发研究/观察，不允许触发执行（承载方案见 `02_阶段二_工作方向_想法?md` ?0.0.6?
11) AI 团队协作工作流（Cowork/Coze）：?Data/Research/Portfolio/Signal 的输?输出/定时任务”固化为可交接产物（承载方案?`02_阶段二_工作方向_想法?md` ?0.0.7?
12) 交互式技术分析助手（App 感，先离线小时级）：主图/副图 + 建仓/加仓/减仓/离场建议（承载方案见 `02_阶段二_工作方向_想法?md` ?0.0.8?
13) 模拟盘自动执行（可）：按出道协议执行与留证据（承载方案见 `02_阶段二_工作方向_想法?md` ?0.0.9?

## 2) 把所?1H CSV 通用跑一遍（对比用）

目标：把“现有所?1H CSV（技术面数据）按同一套流程跑丢遍，生成可对比的汇表?

### 2.1 准备（先确认数据是否齐）

- 棢查：`d:\Stock\trading_analysis\data\` 下是否存?`*_1h.csv`（例?`XAUUSD_1h.csv`?
- 若本?data 目录为空?
  - 方案A：把你已有的淘宝/历史 CSV 直接拷贝?`data\`
  - 方案B：用 `mt5_export_1h.py` ?MT5 导出（可先不带参数运行默认导出一批常用品种到 `data\`?

### 2.2 通用跑法（对比用：优先推荐这丢套）

1) 批量对比回测（会自动遍历 `data\*.csv`）：

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
.\run_p0_sweep.ps1
```

产物?
- `backtest_out\p0_sweep\p0_sweep_summary.csv`（用于横向比较：每个 symbol × split × profile?

2) 若你要的是全指标字段产出→再回放”（scan→replay）：
- 直接?`关于日活.md` ?`2.1 scan` ?`2.2 replay` 执行（用不同 `--log-dir` 区分不同批次?

### 2.3 结果怎么看（朢少看三张表）

- `backtest_out\p0_sweep\p0_sweep_summary.csv`：对比不同标的不同窗口不?profile 的净?回撤/胜率
- `backtest_out\p1_final_validate3\p1_final_decision_table.csv`：最?CORE/OBSERVE/EXCLUDE 的裁决依?
- `backtest_out\p1_final_validate3\deploy_core.csv`：执行侧参数仓库（哪些标的允许执行E2 是否执行等）

### 2.4 下一步要做的事情（先把口径钉死，再回头复盘）

1) 先定丢个验收口径（只?1 个即可）?
- A：只要正期望（net_pnl > 0）就算有?
- B：必须回撤受控（dd_controlled_success=OK）才算有?
- C：必须跨窗口都稳（since2022 ?pre2022 都要过）
- D：必须可用于“池”（例如通过?> 60% 才算通用?

2) 只围绕验收口径做复盘（不先改策略）：
- 哪些品种是数据太?数据质量问题”导致误判（窗口不足、非OHLC混入、时间格式异常）
- 哪个 profile 才能作为“用默认”（A_universal / A_relaxed / A_strict 的择依据?
- 哪些品种应该被剔除（EXCLUDE）或降级观察（OBSERVE），而不是简单结论指标没用?


