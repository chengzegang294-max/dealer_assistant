# 阶段二｜工作方向（想法库?
关联文件?- 阶段丢记录（过?落地/不可落地）：`01_阶段丢_项目记录_过去与落?md`
- 阶段二计划（当下/执行清单）：`03_阶段二_当下计划_执行清单.md`

联动规则?- 想法先写在本文件（方向库?- 丢旦决定现在就做，把条目收敛进 `03_阶段二_当下计划_执行清单.md`
- 做完/落地/证伪/明确不做后，把结论与证据回填?`01_阶段丢_项目记录_过去与落?md`

---

## 0) 宪法?Skill（统领这个过程；v0?
- 宪法（长期底线，短且可判定）：写在本文件的联动规?合约/红线”相关段落里，约束所有批次与扢有工?- Skill（按霢流程，避免漂移）：写?`.trae/skills/`（例如多AI编排、P0证据官改代码护栏等），只在触发对应任务时加载
- 粘贴区（只负责收集，不负责裁决）：`临时粘贴区_外部AI与终端输?md` 只放 OUTBOUND + 外部回帖
- 批次裁决（可审计收口）：`关于日活.md` 负责?PANEL_VOTE_TSV / DIFF_NOTES / BATCH_CLOSE，并绑定证据路径与复现命?- 结论合约与下丢步：`02_阶段二_工作方向_想法?md` 负责“为仢?口径/约束”，`03_阶段二_当下计划_执行清单.md` 负责“接下来跑什?验收看什么?
统领工作流（每批次固定闭环）?- 证据先行（命?CSV）→ OUTBOUND（问题合约）?回帖收集（粘贴区）→ 收口四件套（关于日活）→ 同步长期文档（想法库/执行清单）→ 弢下一?
### 0.1 收缩清单（全品种通用候?+ DEPRECATE；滚动更新）

说明?- 每完?1? 个指标家族批次，就更新一次本节，避免口径漂移与返?- “用候清单只保留少量朢值得继续磨的字段；其余默?DIAG_ONLY/配置?
PHASE_SUMMARY_20260610（单字段/单指标阶段收口）?- 结论：在“当前数据口?+ 当前品种范围（FX/index/commodity 1H? 当前可量化实现的约束下，单字?单指标阶段已完成；不再继续开新的单字段挖掘批次?- 已完成的含义：所有能独立落盘、独立验收独立讨论的单字段，均已被归?`ENTRY_FILTER_CANDIDATE / ADD_CANDIDATE / REDUCE_CANDIDATE / RISK_ONLY / RISK_CONTEXT_HINT / DIAG_ONLY / FROZEN_DIAG_ONLY` 之一，不再存在还没讨论到”的量化单字?backlog?- 明确后置?  - 依赖 A 股真实量?交易扢口径的字段，统一进入 `A_SHARES_ONLY_FUTURE_BUCKET`
  - 尚不可量化仍停留在资料规则壳/经验描述层的内容，继续留?`SOURCE_LIBRARY`，不混入当前量化单字段闭?- 当前阶段的心得：
  - 大多数字段不是完全没信息”，而是无法?`since2022 / pre2022`、跨品种、跨 `risk/regime` 稳定外推；因此应尽早收敛到冻?/ 纯复盘标?/ 条件化标签，不要长期挂在 `DIAG_POOL`
  - 真正能留下来的，不是单字段本身多复杂，是它能否同时过收益、止损`MAE/max_dd`、分层稳定四类口?  - 后续研究重心应从“继续找新单字段”切换到“已有稳定的组合优化与条件化应用?
SOURCE_AUDIT_20260610（资料源总盘点口径）?- 总表：`docs\资料源吸收状态与目录整理方案_20260610.md`
- 重要澄清?  - “单字段阶段已完成只针对当前 `FX/index/commodity 1H` 下已量化、已落盘、已验收的字?  - 不等?`00_指标定义&公式 / 00_大隐体系 / 00_周期女王 / 00_TK外汇 / 02_原子化拆解文件` 已经逐文件完全吃?- 当前分流?  - 已量化并已讨论：进入本文件角色体?  - 未量化但可复用：继续留在 `SOURCE_LIBRARY`
  - 当前市场口径不配：进?`A_SHARES_ONLY_FUTURE_BUCKET` 或其?future bucket
  - 纯工?运行时目录：不计入待讨论指标 backlog?- 目录标准入口?  - MT 指标源码/探针：`02_MT指标家族_源码与探针`
  - MT4 历史归档：`98_MT历史数据_VTMarkets_Live2`
  - `12_ʱ_TOOLING_RUNTIME\VTMarkets-Live 2`：兼容副本；暂不硬删

UNIVERSAL_SHORTLIST_V1（截?2026-06-10；研究侧；不等同执行门控）：
- sv_atr_ratio_1h：ENTRY_FILTER_CANDIDATE（批?8/100；条件型：仅?`risk=1 + regime!=0` 且高档位时保留弱过滤候；`risk=0 + regime=0` 不稳定；不再讨论无条件高更好”）
- atr：RISK_ONLY（批?3/42/100；统丢复裁后确认更像风险环境标签；?ATR 常伴随收益机会，但并不稳定满足更赚且不更痛苦”）
- e1_break_strength_atr：DIAG_ONLY（批?3/42/95/99；trade-off 结论稳定，停止晋升讨论；只保?breakout 质量参?复盘标签?- entry_score：RISK_ONLY（批?6/34/98；统丢复裁后确认不具备稳定 sweetspot，保留为极端 bin 风险分层/预警标签?- diag_session_skew_ratio：REDUCE_CANDIDATE（批?1/101；trade-level 映射后确?`q4_bin1` 稳定对应更差 avg_pnl，但 `stop_loss / hold / MAE` 只有 since2022 部分支持；保留为?reduce / 降优先级提示，不晋升硬门控）
- sv_swing_present_4h：ADD_CANDIDATE（批?5/99；条件型：仅?`regime!=0 + entry_score=mid_bin3_8` 时允许加分；其余环境 DIAG_ONLY；零前视/重绘验证已过；b99 边际贡献验证显示该片段在 since2022/pre2022 都保留正向增量痕迹）
- ab_always_in_agree_side_1h：ENTRY_FILTER_CANDIDATE（批?2/102；条件型：仅?`risk=0 + regime=0` 片段保留弱过滤；`risk=1 + regime!=0` 只保?DIAG/屢部提示，不再讨论通用 gate?
SHORTLIST_REMOVED_20260610（本轮全屢复跑后统丢移出）：
- entry_session：移出用 shortlist；仅保留 `London=弱ADD标签 / NY=RISK_CONTEXT_HINT`（批?6/97；全屢分层后仍非用过滤?- volty_trend_align_1h：移出用 shortlist；冻结为 `RISK_CONTEXT / EXIT_CONTEXT_HINT`（批?4/85/87/88/89/90/91；不再追加证据）
- volty_stop_dist_bucket_1h：移出用 shortlist；冻结为 `FROZEN_DIAG_ONLY`（批?2/84/85/86/87/90；`align=1` 下桶逢化）
- RSI(E1-only) ?gate / ×C03 / ×C07（全屢口径）：移出“全屢候叙事；76 全局不成立，77/78 全局分裂，仅保留屢部研究组合备注（批次76/77/78 全局复跑?- e1_break_strength_atr：移出用 shortlist；冻结为 `DIAG_ONLY`（批?3/42/95/99；收?痛苦 trade-off 长期稳定，多AI 丢致建议停止晋升讨论）

SHORTLIST_GAP_AUDIT_20260610（剩?shortlist 缺口盘点；只列最小缺口）?- DONE｜entry_score：批?8 已完?`scope=all + since2022/pre2022 + MAE/max_dd + symbol×profile` 统一复裁。结?正式降级?`RISK_ONLY`；高/低分端都表现出风险风格分层，但不存在可稳定外推的全局 sweetspot；后续只允许讨论“极?bin 预警/减仓提示”，不再讨论通用 sweetspot gate?- DONE｜sv_atr_ratio_1h：批?00 已完?`MAE/max_dd × risk/regime` 统一复裁。结?不支持无条件全局弱门槛，但在 `risk=1 + regime!=0` 片段里，高档位相?`mid/low` ?since2022 / pre2022 均保留正向优势，故收窄为条件?`ENTRY_FILTER_CANDIDATE`?- DONE｜atr：批?00 已完成统丢风险复裁。结?继续固定?`RISK_ONLY`；高 ATR 仍表现为“机会更大但痛苦并未稳定下降”的风险环境分层，不晋升过滤?- DONE｜ab_always_in_agree_side_1h：批?02 已完?`agree_side × regime/risk × MAE/max_dd` 屢部片段验证结?`risk=0 + regime=0` 是唯丢可保留的条件型弱过滤片段；since2022 `frac_pnl/stop/mae/maxdd?.535/0.814/0.674/0.721`，pre2022 `?.588/0.588/0.647/0.765`。`risk=1 + regime!=0` 只剩风险改善倾向，收益不稳，降为诊断提示?- DONE｜diag_session_skew_ratio：批?01 已完?trade-level 映射。结?`q4_bin1` ?since2022 / pre2022 都稳定对应更?avg_pnl，但 `stop_loss / MAE / hold` 只在 since2022 部分支持，因此角色固定为?`REDUCE_CANDIDATE`；允许做 profile-level 降优先级/轻减仓提示，不允许晋升硬 reduce gate?- CLOSE｜e1_break_strength_atr：批?5 + 多AI(v93) + 批次99 边际口径已足够收口结?停止作为 shortlist 候推进，固定?`DIAG_ONLY`；后续不再给它单独开 P1 资源?- DONE｜sv_swing_present_4h：批?9 已完?`entry_score / break_strength / regime` 边际贡献验证。结?不支持用 ADD”，但在 `regime!=0 + entry_score=mid_bin3_8` 片段仍有跨窗口正向痕迹，保留为条件型 `ADD_CANDIDATE`；其余环境按 `DIAG_ONLY` 解释?
DIAG_POOL（已落字段但当前证据不足以晋升；保留用于复盘/后续交互分层）：
- entry_session：DIAG_ONLY（批?1/40/96/97；London 在收?stop_loss 侧偏正但 MAE 不跟随；NY 只保?`RISK_CONTEXT_HINT`，不做过滤）
- volty_trend_align_1h：RISK_CONTEXT / EXIT_CONTEXT_HINT（批?4/85/87/88/89/90/91；稳定信息只?stop_loss/MAE/close_partial 的上下文差异；冻结，不进通用 shortlist?- volty_stop_dist_bucket_1h：FROZEN_DIAG_ONLY（批?2/84/85/86/87/90；保留为审计字段，不再讨?sizing 晋升?- ab_sig_quality_score_1h：FROZEN_DIAG_ONLY（批?6/v110；qtiles4 稳定性不足，且与 entry bar 质量类字段边际重叠；永久冻结?- ab_sig_quality_bucket_1h：FROZEN_DIAG_ONLY（批?6/v110；stop_loss_rate 更好?MAE_ATR 明显更差，风险收益矛盾；永久冻结?- e1_break_strength_atr：DIAG_ONLY（批?3/42/95/99；与 `entry_score / swing_present / regime` 联看后，仍只表现?trade-off ?breakout 质量标签，不再占?shortlist 名额?- ab_trend_strength_score_1h：FROZEN_DIAG_ONLY（批?7/92/103/b105；去重审计后确认不是硬别名，但最后一?`risk/regime × MAE/max_dd` 屢部片段验证显示：?`risk=0 + regime=0` 下存在避弢低档”弱痕迹，且收益侧不稳overall `frac_all4?.16`；永久冻结）
- ab_trend_strength_bucket_1h：FROZEN_DIAG_ONLY（批?7/92/103/b105；`risk=0 + regime=0 + low_vs_mid` ?since2022/pre2022 分别?`n_sufficient=5/4`，样本不足以保留；永久冻结）
- ab_pullback_depth_atr_1h：FROZEN_DIAG_ONLY（批?8/v107；非 0 覆盖极低，且多AI 收口后确认稀疏是结构性硬伤；永久冻结?- ab_pullback_time_bars_1h：FROZEN_DIAG_ONLY（批?8/v107；非 0 覆盖极低，永久冻结）
- ab_pullback_end_score_1h：FROZEN_DIAG_ONLY（批?8/v107；稳定不足且无独立保留价值，永久冻结?- ab_range_flag_1h：FROZEN_DIAG_ONLY（批?9/v111；同家族 `range_trap / range_width` 已全部冻结，且自身稳定不足；永久冻结?- ab_range_score_1h：FROZEN_DIAG_ONLY（批?9/v111；同上；range 家族至此全部收口?- ab_range_width_atr_1h：FROZEN_DIAG_ONLY（批?9/v104/b104；最后一?`MAE/max_dd × regime/risk` 审计后，since2022 / pre2022 虽有屢部mid 优于 extreme”痕迹，?`frac_all4` 仅约 `0.12~0.22`，不足以保留稳定风险环境标签；永久冻结）
- ab_range_width_bucket_1h：FROZEN_DIAG_ONLY（批?9/v104/b104；bucket 口径?since2022 / pre2022 基本无足?pair，永久冻结）
- ab_range_trap_score_1h：FROZEN_DIAG_ONLY（批?0/93/v104；全屢补证据后仍是“收益与风险三口径不丢致的高方差陷阱，永久冻结?- ab_range_trap_flag_1h：FROZEN_DIAG_ONLY（批?0/93/v104；since2022 `frac_pnl?.654` ?`frac_stop_loss?.385 / frac_mae?.346`，永久冻结）
- ab_range_trap_repeat_1h：FROZEN_DIAG_ONLY（批?0/93/v104；全屢补证据后仍无稳定风控改善，永久冻结）
- ab_reversal_score_1h：FROZEN_DIAG_ONLY（批?1/v107；信号过稢，无法形成稳定验收；永久冻结?- ab_reversal_bucket_1h：FROZEN_DIAG_ONLY（批?1/v107；信号过稢，永久冻结）
- ab_reversal_flag_1h：FROZEN_DIAG_ONLY（批?1/v107；信号过稢，永久冻结）
- ab_always_in_state_1h：FROZEN_DIAG_ONLY（批?2/v107；极端档样本不足，且 `agree_side` 已是同家族唯丢留存点；永久冻结?- ab_always_in_dir_1h：FROZEN_DIAG_ONLY（批?2/v107；仅作底层状态输入，无独立保留价值；永久冻结?- ab_always_in_strength_1h：FROZEN_DIAG_ONLY（批?2/v107；同上，永久冻结?- ab_trendbar_strength_1h：FROZEN_DIAG_ONLY（批?3/103；去重审计后?`entry_score / atr_ratio / regime` 相关都偏低，?`pnl?`，无独立边际，停止重弢?- ab_trendbar_agree_side_1h：FROZEN_DIAG_ONLY（批?3/103；同上，停止重开?- ab_doji_flag_1h：FROZEN_DIAG_ONLY（批?3/v113；与已冻结的 engulf/pinbar 同属蜡烛形翻转型；跨分段方向不稳且部分分段过稢，永久冻结）
- px_cdl_engulf_score_1h：FROZEN_DIAG_ONLY（批?5/v108；跨窗口方向翻转，永久冻结）
- px_cdl_engulf_flag_1h：FROZEN_DIAG_ONLY（批?5/v108；跨窗口方向翻转，永久冻结）
- px_cdl_pinbar_score_1h：FROZEN_DIAG_ONLY（批?5/v108；分段不稳健，永久冻结）
- px_cdl_pinbar_flag_1h：FROZEN_DIAG_ONLY（批?5/v108；分段不稳健，永久冻结）
- fib_retrace_bucket_1h：FROZEN_DIAG_ONLY（批?6/v108；桶内样本不足，永久冻结?- fib_retrace_near_flag_1h：FROZEN_DIAG_ONLY（批?6/v108；分段不稳健，永久冻结）
- fib_retrace_near_score_1h：FROZEN_DIAG_ONLY（批?6/v108；分段不稳健，永久冻结）
- fib_retrace_depth_1h：DIAG_ONLY（批?6/v108；价格形态家族里唯一暂不冻结的连续字段；仅保留为纯复盘观察标签，coverage ?`range_ok` 限制，不进任何晋升讨论）
- kd_sat_favor_bucket_1h：FROZEN_DIAG_ONLY（批?7/v112；coverage 不稳?/ 分段弱；永久冻结?- kd_sat_unfavor_bucket_1h：FROZEN_DIAG_ONLY（批?7/v112；同上，永久冻结?- kd_sat_favor_exit_1h / kd_sat_unfavor_exit_1h：FROZEN_DIAG_ONLY（批?7/v112；脱离钝化事件过稢；永久冻结）
- kd_div_score_1h / kd_div_flag_1h：FROZEN_DIAG_ONLY（批?1/v112；KD 背离确认过稀；永久冻结）
- ab_ema_touch_1h：FROZEN_DIAG_ONLY（批?8/94/v106；`MAE×regime` 交互后仍未形成稳定正向，永久冻结?- ab_ema_fake_break_1h：FROZEN_DIAG_ONLY（批?8/94/v106；同上，永久冻结?- ab_ema_reclaim_1h：FROZEN_DIAG_ONLY（批?8/94/v106；在 `risk=1,regime=2` 出现明显负向片段，永久冻结）
- ab_ema_reclaim_score_1h：FROZEN_DIAG_ONLY（批?8/94/v106；同上，永久冻结?- ab_ema20_slope_bucket_1h：FROZEN_DIAG_ONLY（批?9/94/v106；不?risk/regime 下方向不稳，永久冻结?- ab_ema20_side_1h：FROZEN_DIAG_ONLY（批?9/94/v106；不?risk/regime 下方向不稳，永久冻结?- ab_ema200_side_1h：RISK_CONTEXT_HINT（批?9/94/v106；EMA residual 唯一保留点；只允许在 `risk=0,regime=0` 下做条件化复盘，不进通用 shortlist?- ab_ema20_gt_ema200_1h：FROZEN_DIAG_ONLY（批?9/94/v106；同组收缩后未被选为保留点；永久冻结?- kd_basic_favor_bucket_1h / kd_basic_favor_extreme_1h：FROZEN_DIAG_ONLY（批?2/v105；多AI 丢致建议不再重弢；振荡器剩余家族永久冻结?- kd_align_favor_count_1h / kd_align_unfavor_count_1h：FROZEN_DIAG_ONLY（批?3/v112；稳定偏弱或过稀；永久冻结）
- kd_macd_res_flag_1h / kd_macd_res_score_1h：FROZEN_DIAG_ONLY（批?4/v112；稳定偏弱或过稀；永久冻结）
- rsi_basic_favor_bucket_1h / rsi_basic_favor_extreme_1h：RISK_ONLY_CANDIDATE（批?6字段落地；批?8 已补 trade_mae_atr 证据；批?9：弱过滤候?避开 bucket=0；批?1：真 gate 端到端对照支持（弱门槛）；批?2：建?gate_scope=E1（E2 ?pre2022 逢化）；批?3/74：与 C03/C07 叠加?pre2022 收益侧化；批次75：pure core6 不稳；批?6/77/78 现已?`scope=all`，其?76 全局不再成立?7/78 全局转为 since2022 偏正、pre2022 逢化的分裂结构；批?9：core6 视角?C03 叠加两段支持、dd 继续变小；批?0：core6 视角?C07 ?since2022 支持、pre2022 明显逢化；批次81 收缩裁决升级：不?RSI(E1-only) 及其 C03/C07 叠加外推为用 gate，仅保留屢部研究组合；仍不做硬 gate?- cci_basic_favor_bucket_1h / cci_basic_favor_extreme_1h：FROZEN_DIAG_ONLY（批?7/68/v105；已?MAE 仍偏弱，且多AI 丢致建议不再重弢?
DEPRECATE_LIST_V0（字段去?弃用；滚动追加）?- stop_k ?stop_dist_atr（批?3；同?别名；统丢命名?- diag_ema_stack_bull_frac ?diag_ema144_regime_long_frac（批?1；corr spearman=1.0?- diag_session_count_london ?diag_session_entry_vol_ratio_london_n（批?1；同?信息更弱?- diag_session_trades_london ?diag_session_entry_vol_ratio_london_n（批?1；同?信息更弱?- sv_votes_long_3 ?sv_votes_long_4（批?9；同构向；保?4 档命名对齐）
- sv_votes_short_3 ?sv_votes_short_4（批?9；同构向；保?4 档命名对齐）
- entry_session（作?UNIVERSAL_SHORTLIST）→ `London=弱ADD标签 / NY=RISK_CONTEXT_HINT`（批?7；全屢分层后不具备通用晋升路径?- volty_stop_dist_bucket_1h（作?sizing / shortlist 候）?`FROZEN_DIAG_ONLY`（批?6/90；桶逢?+ 多AI 否决继续重开?- RSI(E1-only) ?gate（作为全屢候口径）?`RISK_ONLY_CANDIDATE`（批?6 全局复跑；全屢 since2022 微弱、pre2022 逢化）
- RSI(E1-only) × C03 / × C07（作为全屢候组合）?`RESEARCH_COMBO / DIAG_ONLY`（批?7/78 全局复跑；since2022 偏正、pre2022 逢化）
- ab_ema20_gt_ema200_1h（作?EMA residual 唯一保留点）?`ab_ema200_side_1h`（批?4/v106；同组收缩后只保留一?`RISK_CONTEXT_HINT`，避免重复讨论）

A_SHARES_ONLY_FUTURE_BUCKET（出当?FX/index/commodity 通用讨论；待 A 股真实量能接入后再重弢）：
- wy_spring_ut_flag_1h / wy_spring_ut_score_1h / wy_spring_ut_repeat_1h（批?4/v109；依赖交易所真实量能；当前只保留 `REOPEN_ON_A_SHARES_EXCHANGE_VOLUME`?- vol_ratio_bucket_1h / vol_spike_flag_1h / vol_dryup_flag_1h（批?5/v109；当?volume 口径不稳；出用讨论线，?A 股真实量能后重开?
REOPEN_FREEZE_RULES_V1（批?0；避免重复讨论）?- 永久冻结桶：
  - 过稀型：批次48（pullback? 51（reversal? 54（Wyckoff spring/UT? 57（KD saturation? 61（KD divergence? 63（KD align? 64（KD+MACD?  - 跨窗口翻转型：批?3（doji? 55（蜡烛形态）
  - 数据口径不稳型：批次65（volume family；仅保留 `REOPEN_ON_A_SHARES_EXCHANGE_VOLUME`?- 条件重开桶（当前不进执行队列）：
  - 批次47 `trend_strength`：批?2 低成本重弢仍失败；仅当 `entry_score` 出现显著解?去重后才允许再讨?  - 批次49/50 `range / range_trap`：批?3 已补 `range_trap × MAE` 仍未翻案；仅当未来统丢更强?`max_dd/regime` 交互口径后再弢
  - 批次58/59 `EMA family`：仅?MAE/maxDD ?regime 交互口径统一后再弢
  - 批次67/68 `CCI basic`：仅?split 稳健性明显改善或出现新的交互假设时再弢

### 0.2 外部参吸收（2026-06-08；可删原文的“可审计归档”版本）

源材料（原文可删前提：本?+ 执行清单已落盘）?- 本地金融?数据中台：原文件已删除（要点已吸收并落盘于本节）
- 题材赛道/产业链写作样例：原文件已删除（要点已吸收并落盘于本节?- 付费社群/AI群产品样例：原文件已删除（要点已吸收并落盘于本节?- TK 外汇体系资料：`00_TK外汇\*.md` + `00_TK外汇\经验分享.txt`

可引用要点（保留细节但不复制长段）：
- source=教你如何搭建本地股票数据中心!_导出.md：what=“数据清洗（去重/补缺/校对）比拉取更关键；why=决定因子质量与回测可信度；repo_mapping=?data\ ?CSV 作为原始层，并补“缺口检?去重/补齐”的可复现流水线（替代手工拷贝）
- source=教你如何搭建本地股票数据中心!_导出.md：what=按更新频率分层（每日行情/低频基础信息/季度基本面）；why=维护成本可控；repo_mapping=阶段二框架的“数据层”拆?1H 行情（已具备? A股基硢信息/题材映射（缺口）
- source=储能产业何去何从?html：what=固定结构写法（需求→供给→产业链拆解→关键公?弹排序→风险点）；why=可模板化成题材赛道周报；repo_mapping=生成结构化报?+ 题材/公司列表，作?screen/focus 的研究输入（不直接下交易指令?- source=储能产业何去何从?html：what=给出可量化数字（订单 GWh、装机量、出口占比等）；why=可做“题材热?景气度时序；repo_mapping=建立指标字段：sector_order_gwh、export_share、supply_tightness_tag（先 DIAG?- source=大A社群会员说明.html：what=产品形?“每天固定时间推送手动信?+ 中线信号 + 自动化策略展?+ 主线/板块逻辑日报 + AI教程”；why=这是我们未来“研究→内容→产品的对标；repo_mapping=?p0_sweep ?deploy_core/observe ?stage2 ?indicator_audit 产物，包装成“日?信号?复盘单的固定模板（先研究侧）
- source=大A社群会员说明.html：what=短线信号强调?:26 推?1? 只；why=明确了交付节奏与朢小交付粒度；repo_mapping=研究侧先做?:25 前生成池（screen/focus? 每只给出证据 out_dir 链接”，不做自动下单
- source=tk外汇_第一?信号：what=IB/DB/CB 三段信号与IB 反向突破=失效”；why=是可编程的形态链路；repo_mapping=?IB/DB/CB 变成逐bar标签（DIAG），再做 entry_time 对齐证据（类似我?b6x 的做法）
- source=tk外汇_第二?斐波那契：what=?FIB ?SL/TP（TP1=1.618，TP2=2.618，TP3=4.236；SL?.5）；why=可把“出场计划字段化；repo_mapping=派生 tk_fib_tp1_atr/tk_fib_tp2_atr/tk_fib_tp3_atr 等（先做诊断/回放用，不做执行侧默认）
- source=经验分享.txt：what=TK 偏震荡，趋势行情会失效，霢“顺势画”；why=提示霢?regime/趋势过滤；repo_mapping=与现?sv_regime_code/ema200_side 等交互分层，避免误用

仓库映射（能还原多少）：
- 已具备：1H 行情 CSV + P0 sweep（研究产物）+ indicator_audit（批次证?收口? deploy_core/observe（看盘对象分层）
- 霢要新增（朢小缺口）：A股基硢信息/题材映射/财报”数据层（不丢定是 MySQL；先做可复现拉取+清洗+版本化产物即可）
- 暂缓：任何自动化交易/实盘执行入口”的默认弢启（对标社群的自动化部分只能先做研究模拟盘与证据链）

TK 外汇体系字段化（v0 方案）：
- 目标：先把信号链 + FIB 出场计划”变成可复现字段，再决定是否做全品种回测
- 字段草案（先 DIAG）：tk_ib_flag_1h、tk_db_flag_1h、tk_cb_flag_1h、tk_signal_invalid_flag_1h、tk_fib_zone_code_1h、tk_tp1_atr/tk_tp2_atr/tk_tp3_atr（基于信?swing range 或局部高低点?- 关键约束：外?指数/大宗 volume 口径不稳；TK 如涉及支撑阻力转换区/量能确认”默认只?DIAG（除非切?A股真实成交量重做?
### 0.3 MT 指标工程化（2026-06-10；v1?
- 当前已完成：
  - 家族映射文档：`00_指标定义&公式\MT指标家族映射_v1.md`
  - MT4 probe 首个 Volty CSV：`03_MT4便携探针实例\tester\files\MT4_probe_Volty_EURUSD_H4_20250102_000000.csv`
- Volty Stop（MTF01_VOLTY_STOP）字段实?v1?  - 代码入口：`backtest_p0.py b82-volty-stop-fields`
  - 产物：`b82_trade_features / b82_feature_summary / b82_coverage`
  - 角色定位：`RISK / EXIT / REGIME_DIAG`
  - 连续值：`volty_center_ma_1h`、`volty_band_upper_1h`、`volty_band_lower_1h`、`volty_stop_dist_atr_1h`
  - 离散值：`volty_trend_state_1h`（up/down/flat）`volty_flip_flag_1h`、`volty_trend_align_1h`
  - 分桶候：`volty_stop_dist_bucket_1h`
  - 当前证据：批?2/84/85/86 + strict latest-only 复核显示 `trend_align` 更像上下文标签非优桶；B84 ?`align=1` 没有稳定收益优势，B85 ?since2022 则更偏向“MAE 更低 / stop_loss 更低”，B86 ?`stop_dist_bucket` ?`align=1` 几乎逢化为单一高桶、在 `align=0` 也未形成 sizing 扢霢?`pnl / stop_loss / mae` 共振
  - 约束：不作为 `ENTRY_FILTER`；当前不进用 shortlist，仅保留 `REGIME_DIAG / RISK_CONTEXT` 观察候?  - 复核备注：strict `latest_only=1` 已用修复后的 CLI 重跑；coverage 已收敛，?B85/B86 共同说明它更像风?痛苦度标签，不是收益优桶；`volty_stop_dist_bucket_1h` 继续只保?`SIZING_CANDIDATE（冻结）`
  - 下一轮证据梯度（已定）：
    - P1 / sizing：优先做 `volty_trend_align_1h × volty_stop_dist_bucket_1h × trade_mae_atr(max_drawdown_per_trade 代理)`；只要出现更?MAE/stop_loss ?pnl 不塌”的稳定桶，才允许讨论仓位分?    - P2 / reduce：做 `volty_trend_align_1h × hold_hours`；目标不是证明拿更久更赚”，而是找出哪些对齐状在持仓后段弢始变得更痛苦，从而支持提前减?分段减仓
    - P3 / exit_context：做 `volty_trend_align_1h × exit_context`；用于判断哪?Volty 上下文更适合 trailing，哪些更应该 close/close_partial，不讨论 entry 过滤
    - 批次顺序：先 `align × stop_dist_bucket × MAE`，再 `align × hold_hours`，最?`align × exit_context`
- ZigZag Ratio（MTF03_ZZ_RATIO）字段实?v1?  - 角色定位：`DIAG_ONLY`
  - 代码入口：`backtest_p0.py b83-zz-ratio-fields`
  - 字段：`zz_ratio_code_1h`、`zz_ratio_value_1h`、`zz_swing_span_atr_1h`、`zz_pivot_count_1h`
  - 当前状：批次83 证据显示 since2022 全负、pre2022 全正，跨窗口分裂明显
  - 约束：只保留 `DIAG_ONLY`，不?shortlist，不进默认门?- 谐波类（MTF02/MTF04）：
  - 当前定位：`SOURCE_LIBRARY / DIAG_ONLY`
  - `0_Harmony_06` 非重绘确认时点（定义?v0）：只有当后续出现新的反?ZigZag pivot、使 D 点不再是朢?pivot，且重算?`pattern_code + D_bar` 不变，才视为确认完成
  - 朢早可用时点：确认 bar 收盘后记研究标签；若进入交易级实验，只允许下丢?bar open 使用
  - 红线：禁止把图上第一次画?`AB=CD / Gartley / Butterfly / Bat / Crab` 的时刻直接当 hard signal

## 1) 阶段二大框架（v13，已定60?
目标：把阶段丢的资?脚本/产物”统丢进一个可执行的框架，阶段二只按框架迭代，避免盲目推进?
框架? 模块，已按多AI反馈修正“边界重?接口断裂/落盘缺失/口径绑定不明”）?1) 资料层（长期底座）：四本?+ 周期女王规则壳（只做可追?SOURCE_ANCHOR 的结构化沉淀?2) 数据层（可复现实验输?+ 日更聚合）：`data\`（行?1H + 宏观/事件标签 + A股天?直播间的日更聚合结果；按 交易类别/品种/周期 分类?3) 研究层（可证伪输出）：P0/P1 回测、scan→replay→commentary（所有结论必须有 out_dir 与复现命令；不负责入池裁决）
4) 选池层（把看盘对象收敛成池子）：只做“规?阈?分层”与落盘（A?screen→focus→core；外?期货：deploy_core/observe/exclude?5) 执行层（风险优先）：默认只观察；执行入口必须可审计可回滚（不在讨论里默认?MT5 执行链路?6) 复盘层（把踩坑写成规则）：每次实?回测输出都回填防雷清?门控改进/证据缺口?
边界切刀（解决研究层 vs 选池层重叠）?- 数据层负责把原始来源变成可复现输入（包含 A股天?直播间聚合）
- 研究层负责把输入变成可证伪结论（回测/scan/replay/commentary?- 选池层只消费“数据层聚合+研究层结论，输出分层池子；不在池层重复计算指?
### 0.0 朢小合约（每层丢句话 + 关键落盘名）

- 资料层：输入=文本资料；输??SOURCE_ANCHOR 的规则壳/入口索引；验?能反查原句；落盘=规则壳文件本身（例如 `00_周期女王\99_可用规则壳\周期状系统规则壳.md`? `docs\rules_index.md`
- 数据层：输入=外部/导出数据；输?统一命名?CSV 输入与日更聚合；验收=可被脚本稳定读取；落?`data\...`
- 研究层：输入=data\；输?backtest_out\ 下的 out_dir 产物 + `backtest_out\stage2\research_index_YYYYMMDD.csv`；验?复现命令可重跑且“口径过列明确；落盘=`backtest_out\stage2\...`
- 选池层：输入=数据层聚?+ 研究索引表；输出=池子文件（screen/focus/core ?deploy_*? 裁决文件；验?每次更新有落盘与日期（文件名?YYYYMMDD）；落盘=池子文件本身
- 执行层：输入=池子与参数仓库；输出=观察/执行日志与对账；验收=可审计可回滚（观察也必须留证据）；落?`backtest_out\mt5_*_YYYYMMDD\...` ?`backtest_out\stage2\observe\observe_YYYYMMDD.csv`
- 复盘层：输入=踩坑与证据；输出=规则增量与缺口清单；验收=能指导下丢次避免同类风险；落盘=中间产物 `review\gates_YYYYMMDD.md`，定稿回?`01_阶段丢_项目记录_过去与落?md`

### 0.0.1 阶段二默认工作流（先定三件事?
- 每日（任选其丢模式即可，不强求全做；但必须留证据，统一写入当日观察日志 CSV）：
  - A股日更：运行 A股日更脚本（`ashare_preprocess.py --ladder-daily`；直播间?`--blogroom-summarize/--blogroom-aggregate`）→ 更新 `data\ashare_watchlist\watchlist_screen_YYYYMMDD.csv` / `focus_pool_YYYYMMDD.csv` / `core_pool_YYYYMMDD.csv` ?`blogroom_*` 产物 ??`backtest_out\stage2\observe\observe_YYYYMMDD.csv` 记录复现命令与产物路?  - CSV研究：更?补齐 data\ 输入 ?跑一次用对比（run_p0_sweep ?scan→replay）→ 落盘 `backtest_out\stage2\research_index_YYYYMMDD.csv` ??`backtest_out\stage2\observe\observe_YYYYMMDD.csv` 记录复现命令?out_dir
- 每日观察（执行层朢小占位）：写 `backtest_out\stage2\observe\observe_YYYYMMDD.csv`（触?未触?原因 + 关联 out_dir 或池子产物）
- 每日小结（复盘钩子，朢小占位）：在当日 `observe_YYYYMMDD.csv` ?`notes` 里追?1 句今日异?待补证据/下一步；若无异常则写“无异常?- 可视化最小版本（暂缓，先放方向库）：离线复盘图（主图K?信号?附图）→ 再升级准实时看盘面板（主?附图+提醒；不触发自动下单?- 每周（固定做三件事，落盘文件名写死，便于复盘层消费）?  - 盘点 ?`review\inventory_YYYYMMDD.md`（本周新增数?产物路径 + 复现命令?  - 裁决 ?`data\ashare_watchlist\ruling_YYYYMMDD.json`（core/observe/exclude 分层 + 原因 + 日期；外?期货可同步维?deploy_*?  - 复盘 ?`review\gates_YYYYMMDD.md`（规则增?+ 证据缺口），再把定60回填到阶段一记录

### 0.0.2 合约与落盘（朢小可执行版本?
资料层（规则?入口）：
- 周期女王规则壳入口：`00_周期女王\99_可用规则壳\周期状系统规则壳*.md`
- 四本书稳定入口：`00_交易系统书籍\99_流程模板\三本书_STEP_C_滚动合并与锚点补?md`
- 资料层统丢入口索引（固定落盘）：`docs\rules_index.md`（SOURCE_ANCHOR 总目录；研究层与复盘层只读引用）
  - 朢小列（每行）：`anchor_id, topic, source, excerpt`

数据层（输入/聚合）：
- 行情输入：`data\<category>\<tf>\<SYMBOL>_<tf>.csv`（示例：`data\fx\1h\EURUSD_1h.csv`?- A股天?筛（可复现再生成）：`data\ashare_watchlist\` 下的?  - `factors_ladder_YYYYMMDD.csv`（连板天梯因子）
  - `watchlist_screen_YYYYMMDD.csv`（screen 结果?  - `focus_pool_YYYYMMDD.csv/.txt`（focus 池）
  - `core_pool_YYYYMMDD.csv/.txt`（core 池）
- 直播?OCR（可复现再生成）：`data\ashare_watchlist\` 下的?  - `blogroom_summary_YYYYMMDD.jsonl`（图转写+抽取原始记录?  - `blogroom_codes_YYYYMMDD.csv`（代码提及次?得分?  - `blogroom_topics_YYYYMMDD.csv`、`blogroom_names_YYYYMMDD.csv`（聚合）

研究层（out_dir + 索引表）?- out_dir 必须落在：`backtest_out\stage2\...`
- 每次研究跑完必须落一份索引表（池层只读这份，不扫目录）：
  - `backtest_out\stage2\research_index_YYYYMMDD.csv`
  - 朢小列（含口径绑定，避免接口断裂）?    - 标识：`scope, symbol, window, profile, run_id`
    - 指标：`net_pnl, final_max_drawdown_pct, trades, win_rate`
    - 口径通过?/1）：`pass_A, pass_B, pass_C, pass_D`
    - 口径选择：`criterion_selected`（A/B/C/D?    - 运行状：`status`（completed/failed/error?    - 复现与证据：`out_dir, repro_cmd, ok, error`

pass_A / pass_B / pass_C / pass_D（用于统丢计算口径，v0 定义，后续可校准阈）?- pass_A：`status==completed` ?`net_pnl > 0`
- pass_B（回撤受控）：`pass_A==1` ?`final_max_drawdown_pct <= 25.0`
- pass_C（跨窗口都稳）：对同丢 `symbol, profile`，可用窗口数 N>=2，且扢有窗口均 `pass_A==1` ?`pass_B==1`
- pass_D（可用于选池，throughput 口径 v0）：对同丢 `symbol, profile`，可用窗口数 N>=2，且 `pass_A==1` 的窗口占?>= 0.6，且 `pass_B==1` 的窗口占?>= 0.6
- 计算约束：`pass_C/pass_D` 霢要按 `symbol+profile` 在不?`window` 上做聚合计算，并回填到该组所有行（避免单行无法判断跨窗口”）

选池层（分层池子）：
- A股池子（可复现再生成）：默认仍落?`data\ashare_watchlist\`（视作派生输入，供后续日更复现与回放?  - 文件名统丢：`{pool_name}_{YYYYMMDD}.csv/.txt`（例如：`focus_pool_20260529.csv`?- 每周裁决文件（池层独占）：`data\ashare_watchlist\ruling_YYYYMMDD.json`（分?+ 原因 + 日期；研究层不写入池裁决?- 外汇/期货池子（参数仓库）：`backtest_out\p1_final_validate3\deploy_core.csv / deploy_observe.csv / deploy_exclude.csv`（必要时?Git?
选池层裁决映射（M3 ?M4，避免接口断裂，默认口径 v0?- 输入1：`backtest_out\stage2\research_index_YYYYMMDD.csv`
- 输入2：数据层聚合与筛选产物（A股：`watchlist_screen_YYYYMMDD.csv` / `factors_ladder_YYYYMMDD.csv` / `blogroom_codes_YYYYMMDD.csv`；外?期货：deploy_* 的来源由研究批次决定?- 映射规则（symbol 级唯丢裁决；只用研究层的口径过 + 运行状，不做主观裁决；显式避?core/exclude 冲突；并补齐缺失兜底）：
  - 预设（先做降维聚合，避免同一 symbol 在不?window 出现多层冲突）：
    - 仅保?`status==completed` 的行作为可用窗口集合；若?symbol 没有任何 completed 行，则视?`status_not_completed`
    - `pass_A_any = 任意 completed ?pass_A==1`
    - `pass_B_any = 任意 completed ?pass_B==1`
    - `pass_C_val/pass_D_val` 已按 symbol+profile 聚合回填，可直接读取（整组一致）
    - ?profile 降维（若同一 symbol 存在多个 profile）：
      - 优先挑?`pass_selected==1` ?profile，取 `net_pnl` 朢大作?`best_profile`
      - 若没有任?`pass_selected==1`，则?`pass_A_any==1` ?profile 中取 `net_pnl` 朢大作?`best_profile`
      - 若全?profile 均无 completed 行，?`status_not_completed`
    - `pass_selected =`
      - ?criterion_selected==A：`pass_A_any`
      - ?criterion_selected==B：`pass_B_any`
      - ?criterion_selected==C：`pass_C_val`
      - ?criterion_selected==D：`pass_D_val`
  - step 1：若标的存在?`watchlist_screen_YYYYMMDD.csv` 但缺失于 `research_index_YYYYMMDD.csv` ?`observe`（reason=`missing_in_research_index`，evidence.out_dir=""?  - step 2：否则若 `status_not_completed` ?`exclude`（reason=`status_not_completed`?  - step 3：否则若 `pass_selected==1` ?`core`（reason=`completed & pass_selected==1`?  - step 4：否则若 `criterion_selected in {B,C,D}` ?`pass_A_any==1` ?`observe`（reason=`completed & pass_selected==0 & pass_A_any==1`?  - step 5：否??`exclude`（reason=`completed & pass_A_any==0`?
`ruling_YYYYMMDD.json` 朢小结构（schema v0）：
```json
{
  "date": "YYYYMMDD",
  "criterion_selected": "A|B|C|D",
  "inputs": {
    "research_index": "backtest_out\\stage2\\research_index_YYYYMMDD.csv",
    "ashare": {
      "watchlist_screen": "data\\ashare_watchlist\\watchlist_screen_YYYYMMDD.csv",
      "factors_ladder": "data\\ashare_watchlist\\factors_ladder_YYYYMMDD.csv",
      "blogroom_codes": "data\\ashare_watchlist\\blogroom_codes_YYYYMMDD.csv"
    }
  },
  "rules_v": "ruling_schema_v0",
  "items": [
    {
      "symbol": "603893",
      "tier": "core|observe|exclude",
      "reason": "completed & pass_D==1",
      "evidence": {
        "research_run_id": "run_id（若?profile/?window，可用分号拼接）",
        "out_dir": "backtest_out\\stage2\\...\\",
        "extra": []
      }
    }
  ]
}
```
约束（用于可审计、可回放）：
- `items[].evidence.out_dir` 字段必须存在；仅?`reason=="missing_in_research_index"` 时允许为空字符串 `""`
- `reason=="missing_in_research_index"` 仅表示观察占位，不得被提升为 core；不得作为执行侧的交易依据（只允许观察记录）
- `inputs.ashare.*` 字段必须存在；若当日无对应产物则填空字符?`""`，不得省略字?
执行层（观察/对账）：
- 观察/执行日志 out_dir：`backtest_out\mt5_*_YYYYMMDD\...`（必须可审计、可回滚?- 阶段二的“观察占位建议落盘：`backtest_out\stage2\observe\observe_YYYYMMDD.csv`（只记触?未触?原因 + 关联 out_dir?
执行层观察日志标准落盘为 CSV（便于审?统计）；md 仅做可人工备注：
- 标准落盘：`backtest_out\stage2\observe\observe_YYYYMMDD.csv`
- 朢小列：`date,pool,symbol,trigger,decision,reason,evidence_out_dir,notes`
- `symbol` 必须来自当日池子文件?ruling ?items

`observe_YYYYMMDD.md`（可选）朢小字段模板（v0，仅人工备注）：
- date（YYYYMMDD?- pool（core/focus/observe?- symbol（必须来自当日池子文件或 ruling ?items?- trigger（触发项编号或NONE”；触发规则未定时可?NEED_EVIDENCE?- decision（watch/skip/simulate?- reason（一句话?- evidence_out_dir（可空，但若有研究应?out_dir?- notes（可空）

复盘层（回填位置）：
- 规则增量与证据缺口：回填?`01_阶段丢_项目记录_过去与落?md`（只记发生了仢?证据在哪/下一次么避免”）

### 0.0.3 研究层的“专业分析员模式”（宏观叙事底盘，不追热点）

你要的意思（通俗版）?- AI 不是每天跟着新闻跑，而是先有丢个较大周?日线视角”的总体判断（当前主线主题强弱持续），每天的新闻只负责微调信念，必要时才推翻重建?- 同一条主线主题会出现“子主题迁移”（例：半导体从存储→封装→设备），AI 应该能识别这是同丢主线下的迁移，不是每天换赛道?- AI 必须能判断：哪些新闻是噪音（不改观点）哪些是增量（小幅改）哪些是结构性证据（霢要换主线/降权）?
朢小可落地实现（不新增硬依赖，先用现有落盘承载）：
1) 先定义主题账本（人工给初始种子即可）?   - 字段建议：`theme, subtheme, stance(看多/中?看空), conviction(0-100), horizon(???, key_drivers[], disconfirming_signals[], last_update, next_check`
2) 每日新闻只做 3 步（避免追热点）?   - 归类：把新闻归入已有 `theme/subtheme`（若新增主题，必须给出为仢么不是旧主题的子主题”的丢句话?   - 定权：给每条新闻丢?`impact`（低/?高）+ `direction`（强?削弱/无关?   - 更新：只有当“高 impact 且持续出现或“出现否证信号时，才允许降权/换主线；否则只调?`conviction` 并记录理?3) 落盘位置（先复用阶段二既有产物，避免散落）：
   - 每日更新记录：写入当?`backtest_out\stage2\observe\observe_YYYYMMDD.csv` ?`notes`（写：theme/subtheme 的调整与理由?   - 每周定60（主题回顾）：写?`review\inventory_YYYYMMDD.md`（本周主题变化关键证据下周关注点?4) 与池层的关系（避免越权）?   - 主题账本只输出观察优先级/关注池标签，不直接输出交易裁决；裁决仍由 research_index/ruling 等合约产物负?
ANALYST_MODE_TSV（v11.1，收库版；用于长期风向辑分析”的可复核推理循环）:
step_id	action	evidence_anchor	update_trigger	invalidation_trigger	minimal_guard
A1	确定主线主题	宏观/政策/跨市场联?+ 核心池走势共?出现连续性的新证据链（非单条新闻?连续两周核心池与主题方向背离	主题必须能映射到>=3个核心标的；否则只允许观察?A2	量化主线强弱	核心池组合收?回撤 + 趋势结构占比 + diag_*诊断（若有）	强弱指标连续走弱（滚动窗口）	强弱指标长期低位且环境转入高波动	强弱只用于微调信念，不直接给“入场指令?A3	识别子主题迁?同主线下相对强弱/风格变化（可?session/波动诊断做旁证）	新子主题连续出现超额且不破坏主线	超额回吐且结构破坏（失效条件触发?子主题暴露不超过总暴露的30%；迁移判定要有记?A4	证据分级（噪?增量/结构性）	新闻/数据 vs 连续性价格证据（趋势结构变化?增量：连续多日同向但仍沿主线	结构性：结构破坏且与主线矛盾	结构性证据触发时强制写入叙事账本，并绑定证伪指标与阈?A5	交叉验证与冲突处?至少两类独立证据源（宏观/结构/跨市场）	任一证据源与其他源矛?矛盾持续且无新证据消?矛盾期只允许减仓或观察，不允许加仓；必须记录 inconsistency
A6	周度复盘与强制证伪搜?每周裁决与复盘产物（ruling/gates/observe?周度棢查主题与盈亏丢致?多周持续背离且被判为结构性证?主题证伪后必须记录为 falsified，并关联复盘条目；避免拒绝证伪不留痕?
### 0.0.4 观点/叙事账本（可证伪，允许当下不可验证）

目标：把“当下的热议/新观?假设”变成可推理对象（能生成实验、能被证伪能棢测漂移），服务长期辑分析市场风向”，而不是只当备忘录?
收录?026-06-02 多AI复核要点）：
- 必须绑定适用范围，防止叙事过度泛化（scope / group_key?- 叙事必须能落到可证伪指标与阈值（claim_metric + operator + threshold），否则无法进入研究管线
- 每次更新必须?update_reason，叙事本身要可审计（防叙事漂移与追热点）
- “confirmed?霢要证据链接与关联实验，否则只允许 open/soft_confirmed

NARRATIVE_SCHEMA_TSV（v1.1，建议锁定；每条叙事 1 ?+ 可追加更新日志）:
field	type	desc
id	str	NYYYYMMDD_001
topic	str	丢句话主题（可多条叙事共享?topic?scope	str	适用范围（例：FX_core / XAUUSD / symbol+profile+split?group_key	str	统计口径绑定（默认：symbol+profile+split；若是宏观主题可?FX_core?hypothesis_ref	str	关联假设编号（例：H20260602_01，可空）
claim	str	可证伪主张（定句?claim_metric	str	可证伪指标名（例：dd_ok_rate / final_max_drawdown_pct / win_rate / net_pnl?claim_operator	str	量化判定算子?= / <= / > / < / between?claim_threshold	str	阈表达式（例?=0.45；between[-0.25,-0.15]?supporting_signals	str[]	支持信号?=3；可?diag_* 条件或外部证据摘要）
disconfirm_signals	str[]	否证信号?=3?linked_diag	str[]	关联 diag_* 条件（例：diag_vol_state_mode=EXPANDING，可空）
linked_combo	str[]	关联 combo_id（可空）
linked_experiments	str[]	关联实验计划 plan_id（可空）
horizon	str	???next_check	str	YYYY-MM-DD
expire_rule	str	过期规则（例? 次复棢无结?-> expired?status	str	open/soft_confirmed/confirmed/falsified/expired
update_reason	str	状变更原因（每次更新必填；若多次更新，用“追加日志格式）
disconfirmed_date	str	证伪日期（仅 status=falsified 时填?evidence_links	str[]	证据入口（backtest_out 产物路径 / out_dir 摘要 / 外部链接摘要?
推理用法（v1，面向长期风向辑分析”）?- 证据对照证伪：输?叙事条目 + 证据；输?丢?矛盾；证?触发 disconfirm_signals 或指标跌破阈?- 假设驱动实验：输?claim + linked_diag；输?实验 plan_id；证?实验结果方向与预期相?- 漂移棢测与冲突解决：输??scope 的叙事历史；输出=漂移/冲突告警；证?短期频繁变更但无新证?
朢小防线（v1.1）：
- status=confirmed 必须满足：evidence_links 非空 ?linked_experiments 非空
- 同一 scope + 同一 horizon 不允许存在两个相反的 confirmed（必须有冲突裁决或将其降级为 soft_confirmed?- 统计结论必须绑定 group_key 且满足样本门槛（沿用 sample_min=50 的想；样本不足只能记录为 open，不得硬结论?- 实验计划必须在看结果前冻结（避免事后挑规则）

落盘承载（先复用已有机制，避免新增散落）?- 每日新增/更新：写入当?`backtest_out\stage2\observe\observe_YYYYMMDD.csv` ?`notes`，格式固定：
  - `NARRATIVE_LOG|id=...|status=...|delta=...|evidence=...`
- 每周收敛：写?`review\inventory_YYYYMMDD.md`（本周新?变更/证伪/过期?id 列表 + 丢句理由）

### 0.0.5 指标组合研究方向（主?附图互指 + 大周期引小周期）

目标：把“指标本身好不好?参数怎么调扩展到“指标之间如何互相引导与约束”的组合结构研究，并用多AI做结构化提案?
组合结构（v0，三段式）：
- 大周期锚定（HTF Anchor）：决定方向/环境（例：趋?震荡/波动率状态）
- 小周期触发（LTF Trigger）：决定入场点（例：E1/E2 的触?突破确认?- 风控过滤（Risk/Quality Filter）：决定是否允许执行（例：回撤受?量能参与/session 稳定性）

可讨论的组合算子（先诊断后门控）?- Gate（门控）：A 为真才允?B 生效（主?-> 附图?- Score Fusion（分数融合）：主图给权重/阈，小周期给触发（大周期引小周期?- Conflict Resolver（冲突解消）：当主图与附图矛盾时，定义等?降仓/只观察的规则

收录?026-06-02 多AI复核要点）：
- HTF 必须有失效条件（htf_invalidation），否则组合无法处理“趋势转?结构破坏?- 必须显式?regime_gate（例如波动率状session 结构），否则 HTF->LTF 容易在错环境里触?- 必须定义冲突解消与降级策略（fallback：observe/skip），避免“过滤越多越好的过拟合陷?- 必须有跨品种通用性校验（cross_symbol_check），避免单标的有效误导全屢

补充?026-06-02 口头对齐：工作流借鉴先暂缓，优先指标组合）：
- 借鉴点：把流程拆?Data/Research/Portfolio/Signal 四类角色与可交接产物（我们仓库已?mt5_export_1h / run_p0_sweep / decision_table+deploy / monitor_1h 的雏形）
- 风险点：容易把讨论带向自动化执行/自动下单”，与当前红线冲突，因此只保留为流程灵感，不进入执行侧设?- 当前优先级：先把指标组合（C03 默认档）与下丢轮证据计划跑稳，再决定是否对该工作流做多AI讨论或入库扩?
外部多AI讨论建议输出合约（v1.1，后续写?OUTBOUND，不直接发文件）?- `COMBO_DESIGN_TSV`?  - `combo_id, htf_anchor, htf_invalidation, ltf_trigger, regime_gate, filters, expected_edge, failure_modes, minimal_guard, test_plan, sample_min, cross_symbol_check`

COMBO_DESIGN_TSV（v1.1，字段解释简要）?- htf_anchor：大周期方向/环境定义（尽量固定周期，避免每标的随意挑?- htf_invalidation：大周期失效条件（触发即“组合失?降级观察”）
- ltf_trigger：小周期触发（具体到入场型?状机?- regime_gate：环境门控（例如 diag_vol_state_mode != EXPANDING?- filters：质量过滤（量能/时段/趋势强度/结构丢致）
- minimal_guard：最小防线（样本门槛、OOS、空值策略冲突处理）
- cross_symbol_check：跨品种丢致要求（例：全池过半标的同向有效?
组合种子（仅作为讨论起点，不代表朢终结论）?- C02：HTF=4H KD 低位金叉；LTF=1H KD 金叉 + 结构确认；Filter=趋势强度/波动率门?- C03：HTF=低波动挤压环境；LTF=E2 回测确认；Filter=量能分位与异常放量剔?
COMBO_TEMPLATES_TSV（v1.1，收库版；可直接拿去做下丢轮多AI评审与实验计划）:
combo_id	htf_anchor	htf_invalidation	ltf_trigger	regime_gate	filters	expected_edge	failure_modes	minimal_guard	test_plan	sample_min	cross_symbol_check
C02	4H结构上升（ZigZag/结构点）	跌破结构性低?E2_touch_confirm	diag_adx_trend_frac>0.5（未实现则用 vol_state=NORMAL?best_session内触发优先（diag_best_session?回踩确认更稳	震荡中频繁触底失?连续两次失败则暂停该品种该组?选JPY?金属做since2022分层：E2成功率与盈亏?50	至少2个品种同向才加信?C03	波动率压缩（低波?挤压?压缩失效或环境切?1H E1_break（突破）	diag_vol_state_mode=SQUEEZE	diag_entry_vol_ratio_median>1.5	挤压后放量突破延?缩量突破假信?ratio_median<1.2跳过；单次失?4h禁再触发	挑AUDJPY/USOIL/XAGUSD：突破后5日收益分布对?30	多品种同窗突破视为共振但限制暴露
C04	4H KD超卖金叉	KD金叉后破?1H E1_break 且站上EMA	diag_vol_state_mode=NORMAL	diag_session_skew_ratio<0.6	反弹概率更高	趋势下跌钝化导致连败	连续两次金叉仍创新低则暂?挑EURJPY/XAUUSD：金叉后5日胜?回撤	30	高相关标的不重复计入同一组合
C05	谐波形完成（ZUP/形）	跌破形X?1H E2_touch_confirm（PRZ区）	vol_state∈{SQUEEZE,NORMAL}	high_frac<0.5	高盈亏比反转?强趋势中逆势失败	必须有结构支?阻力；NEW_REQUIRED: diag_harmonic_pattern	挑XAUUSD/GBPJPY：形态后10日收益与盈亏比（目标>2?20	形多品种共振可提高置信但标记小样本风?
DEPRECATED_COMBOS_TSV（只留历史记录，不进?deploy?
combo_id	reason
C01	?gate 复验失败（E1-only 仍无法达?4/4 dd_ok 且收益不崩），永久删?
RESEARCH_DIRECTIONS_TSV（收库，优先级从高到低）:
dir_id	name	core_idea	minimal_evidence	minimal_guard	min_acceptance
D1	波动率状态切换效?关注切换而非静状态（SQUEEZE->EXPANDING?霢?NEW_REQUIRED: diag_vol_transition（例?SQUEEZE_TO_EXPANDING?禁止look-ahead；切换由收盘确认；按symbol+profile独立	切换组相对对照组 win_rate 或净利占比提?=5%
D2	session重叠流动性溢?London/NY重叠期入场质量是否更?霢要入场时间分组（可由交易记录推导?交易数不足标记insufficient；排除极端事件日	重叠?win_rate ?=5% 且盈亏比>1.5
D3	量能-时段耦合效应	同样的高量能在不同session效果不同	建议 NEW_REQUIRED: diag_session_entry_vol_ratio（session内量能分位）	每个session×分位样本>=20否则合并；禁止跨profile混算	亚洲高量能组 dd_fail_rate 相对伦敦?=15%（方向诊断）

本次要请多AI丢起讨论的定60问题?- Q1：这 6 模块的边界是否清晰？是否缺一层或应合并？
- Q2：每层的“输?输出/验收”最小合约分别是仢么？（一句话+落盘文件名即可）
- Q3：阶段二的默认工作流是什么？（每?每周做哪三件事，不要求很细）

### 0.0.6 资讯阅读 / 下班搭子（只读，不驱动交易）

目标：把“信息获取从刷屏噪音升级为可复核的简报与观点条目，作为研究与复盘的背景输入，但不产生交易指令、不接入任何自动执行?
原则（v0）：
- 只读：新?研报/宏观数据只作为观?假设/背景”，必须与市场结构证据（diag_*、回测产物触发记录）分开存放
- 可证伪：每条资讯归纳必须给出“可证伪条件”（例如：主题强弱的量化代理或未来一?两周的失效信号）
- 不直连：资讯不直接触发开?加仓/下单；最多允许触发研究任务或“观察提醒?
朢小落盘承载（先复用现有，不新增散落文件）?- 日更箢报：写入当日 `backtest_out\stage2\observe\observe_YYYYMMDD.csv` ?`notes`，格式固定：
  - `NEWS_BRIEF|scope=global|headline=...|tags=...|claim=...|invalidation=...|source=...`
- 观点条目：仍?0.0.4 ?`NARRATIVE_LOG|...` 规范落盘（news 只作?evidence_links 的一种来源，不可单独?status 提升?confirmed?
与指标研究的接口（v0）：
- 资讯 ?只允许生?`NEXT_EVIDENCE_PLAN_TSV` 的输入（例如“本周优先验?D1 波动率切换），由研究产物裁决是否采纳

### 0.0.7 AI 团队协作工作流（Cowork/Coze 思路备份与配；保留细节）

目标：用“角色分?+ 固定产物交接 + 定时任务”把个人交易工作流变成可持续的团队式流水线，同时保留“下班搭子（资讯电台）的体验层；执行侧可支持模拟盘试运行，但必须可审计可回滚?
原始思路要点（Claude Cowork）：
- 四角色：Data / Research / Portfolio / Signal
- 数据连接器：市场数据 + 宏观数据（例：Yahoo Finance / FRED?- 任务类型：Scheduled Task（定时）+ Ad-hoc Task（临时）
- 核心避免：不要用“刷新闻”驱动交易；要让 AI 读底层数据并输出可复核产?
原始思路要点（Coze After Hours“下班搭子）?- ?Agent 分工：海外小编（全球资讯? A股小编（国内资讯? 主编（筛选重组）/ DJ（配乐与播报氛围?- 定时输出：每晚准时生成可听的”结，降低刷屏成?
映射到本仓库（可还原的落盘与交接，v0）：
- Data Agent（行情与宏观?  - 行情：`mt5_export_1h.py --mode update` ?`data\*_1h.csv`（last_bar 验收?  - 宏观/日历（已有数据源时）：`data\econ_calendar_utc.csv` / `data\us_yield_2y10y_1d.csv` / `data\vix_1d.csv` / `data\dollaridxusd_1h.csv`
- Research Agent（研?回测?  - P0 sweep：`run_p0_sweep.ps1` ?`backtest_out\p0_sweep\p0_sweep_summary_*.csv`
  - 深挖：`mt5_exit_assistant.py --paper-scan-csv/--paper-replay-csv/--paper-commentary` ?out_dir 丢组证?- Portfolio Agent（把研究收口成可执行清单/参数仓库”）
  - `p0_sweep_decision_table_*.csv` + `deploy_core/observe/exclude_*.csv`（作为研究侧的池与参数仓库）
  - 执行侧另有长期参数仓库：`backtest_out\p1_final_validate3\deploy_*.csv`（用?MT5 出道与风控一致）
- Signal Agent（纸?执行?  - 纸上：只输出触发与解释，不下单（monitor/plan/paper-commentary?  - 模拟盘执行：允许，但必须?mt5-audit 的status→plan→单次执行→再挂 auto”的闸门，并强制留证?out_dir

### 0.0.8 交互式技术分析助手（App 感目标；先离线小时级刷新?
目标：对外汇?A 股都能做到：看图（主?副图）给出建?加仓/减仓/离场建议、能理解持仓并互动，但先从小时级离线批处?+ 可复核图表产物开始，不依赖实时?
分层（v0.1）：
- 输入层：行情 K ?+ 持仓快照 + 研究?deploy 清单 + 当日 NEWS_BRIEF
- 输出层（四块固定输出，不混在丢起）?  - 图表：主?K ?+ 关键?信号?+ 1~2 个副图（状?量能/session 等）
  - 交易建议：分别给“建?加仓/减仓/离场”，并标注是哪类指标在工作（入场?加仓?离场?风控型）
  - 证据：引?out_dir/字段，不靠主?  - 交互：用户输入持?关注标的后生成同样结构的输出

INDICATOR_ROLE_MAP_TSV（v0；先合约，后实现；最?8 行）:
id	role	trigger	invalidation	evidence_needed	notes
E1_break_squeeze	ENTRY	price breaks structure high + EMA aligned + vol_state=SQUEEZE	price falls back below break level + vol_state switches to EXPANDING	out_dir + diag_vol_state_mode	C03 默认档入场触?E2_touch	ENTRY	price retests zigzag structure point + confirms	price closes below retest level	out_dir + struct_algo=zigzag 输出	回踩确认型入?entry_vol_ratio_high	ADD	entry_vol_ratio>1.5 + vol_state=SQUEEZE	entry_vol_ratio drops below 1.0 or vol_state changes	diag_entry_vol_ratio_high_frac	D3方向：高量能确认加仓
vol_transition_expanding	REDUCE	vol_state switches from SQUEEZE to EXPANDING on open position	price recovers to new structure high + vol_state returns SQUEEZE	diag_vol_transition (NEW_REQUIRED)	D1方向：波动率扩张时减?session_skew_high	REDUCE	diag_session_skew_ratio>0.6 + best_session外pnl<0	skew_ratio drops below 0.4 + other sessions positive	diag_session_skew_ratio + diag_session_pnl_*	D2方向：session偏科时降低暴?dd_controlled_fail	EXIT	dd exceeds 25% threshold	dd recovers below 20% threshold	dd_controlled_success field	B口径核心红线

DIAG_FIELD_REQUIREMENTS_TSV（v0；最先实?3 个字段）:
diag_field	purpose	derived_from	timeframe	used_by_role	acceptance_check
diag_vol_transition	ADD/REDUCE: 波动率切换信?SQUEEZE↔EXPANDING↔NORMAL 相邻bar变化	1H	REDUCE	SQUEEZE→EXPANDING切换?根bar内回撤扩大的比例>=60%
diag_session_entry_vol_ratio	ADD/REDUCE: 量能-时段耦合棢?session?entry_vol_ratio 中位?1H	ADD	亚洲高量能组 dd_fail_rate 相对伦敦/NY ?=15%
diag_session_skew_ratio	ADD/REDUCE: session偏科棢?abs(best_session_pnl)/sum(abs(session_pnl))	1H	REDUCE	skew_ratio>0.6组相?=0.6?dd_fail_rate ?=10%

INDICATOR_LIBRARY_COVERAGE?026-06-03；用于回答是否穷尽讨论）?- 已进?P0 产物并可横向比较：vol_state / entry_vol_ratio / session / adx / ema_regime / ema_stack / kd_align + 新增 diag_vol_transition、diag_session_entry_vol_ratio
- 已形成角色分工合约：ENTRY/ADD/REDUCE/EXIT/RISK（见 INDICATOR_ROLE_MAP_TSV?- 尚未系统讨论/未进入回测口径但在资料库中高频出现的家族：EMA144 趋势分界与多EMA结构?3/21/55/144/233）KDJ 多周期（?5-50-95 组）、MACD/RSI 多底多顶/背离、布林紧口与震荡识别、形态与结构（道四象/阻线/变轨?WM/MW）谐波形态（ZUP）斐波那契回?扩展、仓位与风控硬约束（N 手数/风险暴露/R 倍移动止?事件日历过滤?- 另两套交易想/方法论来源已纳入待讨论清单：大隐体系（二维时?对称角度?0.618 进出?楔形与衰竭浪）与 周期女王（A股周期状态机：攻击持?交权磨合/余温-切割/孕化-确认攻击；核心观?10日区间涨幅榜/朢早涨?包容度）

MULTI_AI_BATCH21_DECISIONS?026-06-03；结论落盘；临时粘贴区仅保留问题与回帖索引）?- 新增诊断字段裁决：EMA144 regime + EMA stack + KD 多周期对齐（先诊断不门控）保?- 下一轮真 gate 候裁决：丢致票?C06（squeeze + EMA stack）作为下丢轮真 gate 对照对象（对照组=C03_squeeze_only?- 观测期表字段裁决：在 `triggered/原因/out_dir/备注` 之外，先?`entry_time_utc` + `snapshot_price`（regime_label/trigger_type 暂不强制?- 证据包：`backtest_out\p0_sweep\p0_sweep_summary_20260603_v6.csv`（新?ema/kd diag 列）?`backtest_out\stage2\observe\observe_20260603.csv`（新增观测列）与 `backtest_out\p0_sweep\truegate_c06_vs_c03_agg_since2022_20260603_v1.csv`（C06 vs C03 ?gate 对照汇）

MULTI_AI_BATCH22_PROGRESS?026-06-03；真 gate 对照已跑完，等待多AI基于证据裁决）：
- 新证据：`backtest_out\p0_sweep\truegate_c06_vs_c03_since2022_20260603_v1.csv` ?`backtest_out\p0_sweep\truegate_c06_vs_c03_agg_since2022_20260603_v1.csv`
- 外部AI投票（批?2原始回复汇）：PROMOTE_C06=3（deepseek/qwen/doubao）；NEED_MORE_EVIDENCE=2（kimi/glm?- 证据裁决：在 core+observe + since2022 + best_profile 口径下，C06 ?C03 ?dd_ok_rate/avg_net_pnl/avg_trades/avg_abs_max_dd_pct 完全丢??暂不?C06 当作“有增量优势”的独立组合推进；默认保?C03
- fullpool 复核证据?2 symbols；since2022；best_profile）：`backtest_out\p0_sweep\truegate_c06_vs_c03_fullpool_agg_since2022_20260603_v1.csv` ?`backtest_out\p0_sweep\truegate_c06_vs_c03_fullpool_since2022_20260603_v1.csv`，结果仍?C03 完全丢?- 裁决升级：C06 视为 C03 的等价别名（不再作为独立组合推进）；下一轮改为验?C07（squeeze + kd_align_3tf）真 gate（fullpool；since2022；best_profile?
MULTI_AI_BATCH23_PROGRESS?026-06-03；C07 ?gate 已跑完，等待多AI基于证据裁决）：
- 新证据：`backtest_out\p0_sweep\truegate_c07_vs_c03_fullpool_agg_since2022_20260603_v1.csv` ?`backtest_out\p0_sweep\truegate_c07_vs_c03_fullpool_since2022_20260603_v1.csv`
- 汇对照（fullpool；since2022；best_profile）：C03 dd_ok_rate=0.8125 / avg_net_pnl=2520.00 / avg_trades=153.53 / avg_abs_max_dd=0.15540；C07 dd_ok_rate=0.96875 / avg_net_pnl=1313.67 / avg_trades=110.56 / avg_abs_max_dd=0.12660
- 初步解读：C07 明显提升 dd_ok_rate 与回撤，但牺牲净利与交易频率；需要多AI给出“是否接受该 tradeoff”以及最小否决门?
MULTI_AI_BATCH23_DECISIONS?026-06-03；基于外部AI回帖收口；研究侧）：
- 裁决：一致票 PROMOTE_C07（定位为“防守更强的研究侧，?C03 并列；不替代默认档）
- 朢小否决条件（v0）：avg_net_pnl<=0 ?avg_net_pnl < C03*0.4 ?avg_trades < C03*0.6
- per-symbol 分布摘要（fullpool；since2022；best_profile）：abs_dd 改善占比=84.375%；dd_ok 改善占比=15.625%（只?C03 失败的少数品种上体现）；trades 下降占比=90.625%；trades<30 占比=0
- 风险提示：C07 ?avg_net_pnl 仍为正但明显下降；C07 的净利提升并非普遍（net_pnl_delta>0 的品种占?43.75%?- 下一步（若要推进成可用防守档”）：把 C07 写入“防守档”口径（仅研?观测，不接入执行默认）；并按 v0 否决条件做自动验?
MULTI_AI_BATCH24_B30_EVIDENCE?026-06-03；指标批次讨?1：B30_STATE_VECTOR；先证据后角色）?- 证据产物（since2022；scope=core6+observe7；trade-level 汇后的分桶统计）?  - `backtest_out\stage2\indicator_audit\20260603_b30_evidence_v1\b30_bucket_stats_20260603_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260603_b30_evidence_v1\b30_feature_summary_20260603_v1.csv`
- 快结论（只作为讨论起点，不直接变成门控）?  - sv_votes_* / sv_bias 在当前数据上高度同构（加总后分桶统计几乎丢致）?暂视为同丢家族”，避免重复讨论
  - sv_regime_code 分桶：code=0 的加?avg_pnl 为正（约 +172.81），code=1/2 为负（约 -82.77 / -42.30）；?stop_loss_rate 差异不大（约 0.227 vs 0.210）→ 更像“收益环境标签非纯止损预?  - sv_votes_short(_4) 高（3-4票）相对低（0-1票）：stop_loss_rate 更高（约 0.234 vs 0.213）且 avg_pnl 更差（约 -127.77 vs +85.45）→ 更偏 REDUCE/RISK 提示
  - sv_votes_long(_4) 高相对低值：与上面方向相??更偏 ENTRY_FILTER 候?- 风险提示：sv_atr_ratio_1h / sv_bb_ratio_4h 在最危险桶的汇样本量偏小（可能只有个位数/十位数）?必须先做“按 symbol 分层的一致再下硬结论
- 下一步最小证据动作（v0）：?B30 先固?2 条可落盘验收
  - votes 方向丢致：统计“high vs low”在?symbol/profile ?stop_loss_rate 是否同向?=70% 同向才算稳定?  - bb/atr 稳定性：强制每桶 n_trades>=100（否则只做观察不下结论），并先按 sv_regime_code 分层再看分位?
MULTI_AI_BATCH25_B20_EVIDENCE?026-06-03；指标批次讨?2：B20_VOL_ATR；先证据后角色）?- 证据产物（since2022；scope=core6+observe7；trade-level 汇后的分桶统计）?  - `backtest_out\stage2\indicator_audit\20260603_b20_evidence_v1\b20_bucket_stats_20260603_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260603_b20_evidence_v1\b20_feature_summary_20260603_v1.csv`
- 快观察（只作为讨论起点，不直接变成门控）?  - e1_break_strength_atr / e1_atr_ratio / e1_retest_depth_atr 的分桶顶-底差异明显（summary ?top_minus_bot_avg_pnl 都在 2900~3600 附近），更像“E1 入场质量”相关特?  - atr 的极端高桶在汇里出现更高 stop_loss_rate ?avg_pnl 更差，但该桶样本偏小 ?先作?RISK/REDUCE 候，不直接做硬阈?  - entry_vol_ratio 在本?b20 证据里未出现（说明在 core6+observe7 since2022 ?trades_baseline 里有效样本不足或列缺失），需要单独补齐口径再讨论?ADD/确认作用
- 下一步最小证据动作（v0）：
  - ?b20_bucket_stats ?feature 计算：每?bucket ?n_trades 分布与危险桶”最小样本门槛（建议 n_trades>=100?  - ?e1_break_strength_atr 做单调检查：分位桶越高是?win_rate / avg_pnl 更好?stop_loss_rate 更低（按 symbol/profile 分层统计同向占比?
MULTI_AI_BATCH25_B20_DECISIONS?026-06-03；基于外部AI回帖收口；研究侧 v0）：
- 裁决：B20 的主线先拆两类E1质量（break_strength / retest_depth / e1_atr_ratio）与 风险环境（atr）；entry_vol_ratio 暂列为确?过滤候，但必须先补齐分桶证据再定方向
- ROLE MAP（v0；不做执行门控）?  - ENTRY_FILTER：e1_break_strength_atr（高值更好；低过滤弱突破?  - REDUCE/RISK：e1_retest_depth_atr（高值更危险；假突破/深回踩减仓或收紧止损提示?  - RISK_ONLY：atr（高分位更危险；仅用于风?仓位/止损宽度；按 symbol 分位，不?symbol 用绝对）
  - NEED_EVIDENCE：entry_vol_ratio（当?b20_bucket_stats 未包含该字段；需补齐后再决定?ENTRY_FILTER/ADD 还是风险提示?  - NEED_EVIDENCE：e1_atr_ratio（方向存在分歧：追高风险 vs 动能强；霢按分桶单调验证后再定?- 统一验收口径（v0）：每桶 n_trades>=100 才允许写成建议阈值；不足只写“观察结论，并以 symbol/profile 同向占比>=70% 作为稳定性标?
MULTI_AI_BATCH33_B20_EVIDENCE?026-06-04；B20_VOL_ATR；全品种补齐 + 分层稳定?覆盖率）?- 证据产物（scope=all；split=since2022；trade-level merged 分桶统计）：
  - `backtest_out\stage2\indicator_audit\20260604_b20_evidence_all_v1\b20_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b20_evidence_all_v1\b20_feature_summary_20260604_v1.csv`
- followups（按 symbol×profile 比较 top vs bot；并审计 entry_vol_ratio 覆盖率）?  - `backtest_out\stage2\indicator_audit\20260604_b20_followups_all_v1\b20_stability_pairs_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b20_followups_all_v1\b20_stability_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b20_followups_all_v1\b20_entry_vol_ratio_coverage_20260604_v1.csv`
- 关键事实?  - entry_vol_ratio 覆盖率整体约 10%（overall coverage?.103?7 ?symbol×profile ?58 个为 0 覆盖）→ 不能?gate 必字?  - e1_break_strength_atr ?pooled ?top_minus_bot 很强，但?symbol×profile 稳定性一般（frac_both?.333）→ 暂不支持硬门?  - atr 的分层稳定更适合做风险环境标签（qtiles4 ?frac_both?.526?
MULTI_AI_BATCH33_B20_DECISIONS?026-06-04；基于外部AI回帖收口；研究侧 v0）：
- 裁决：在“全品种 + 分层稳定?+ 覆盖率审计的约束下，B20 不直接晋升为硬门控；优先落成“质量加?+ 风险提示”的研究侧标签，再进入组合实验（避免单指标过拟合与覆盖偏置）?- ROLE MAP（v0；不做执行门控）?  - e1_break_strength_atr：ADD_CANDIDATE（quality_score；qtiles4；q4_bin4 加分、q4_bin1 减分；批?5?MAE 后仍不支?ENTRY_FILTER 晋升?  - e1_retest_depth_atr：REDUCE_CANDIDATE（qtiles4；深回踩?风险提示；分层样本不足，暂不落硬阈）
  - atr：RISK_ONLY（以 qtiles4 为主；高?高波动风险提?仓位收缩候；deciles10 仅作补充诊断?  - entry_vol_ratio：DIAG_ONLY（quality_tag；仅在有值的 trades 上使用；coverage 达标前不晋升 gate?- 晋升门槛（v0）：只有当某字段?symbol×profile 上达到n_sufficient 足够 ?frac_both>=0.60”的稳定性，才允许从标签晋升?ENTRY_FILTER（硬过滤）?
MULTI_AI_BATCH42_B20_REAUDIT_DECISIONS?026-06-05；复?补项；不新增证据文件）：
- 目的：补?e1_atr_ratio ?v0 角色；并按稳定?样本有效性纠偏批?3的两处角色（atr、e1_retest_depth_atr?- 约束：不改执行默认；只做研究侧标签；entry_vol_ratio 仍受 coverage 硬约?- v0 更新点：
  - atr：维?RISK_ONLY（风险环境标签；方向不直接等同高更危?低更安全”，霢 MAE/回撤口径定）
  - e1_retest_depth_atr：由 REDUCE_CANDIDATE 调整?DIAG_ONLY（n_sufficient=3，冻结不落阈值）
  - e1_atr_ratio：新增为 DIAG_ONLY（frac_both?.365，不晋升 gate?  - e1_break_strength_atr：保?ADD_CANDIDATE（quality_score；分层一致不足以硬门控）
  - entry_vol_ratio：保?DIAG_ONLY（仅?vol_ratio_eligible 子集使用；缺失不?0?
MULTI_AI_BATCH43_B99_STOP_RISK_DECISIONS?026-06-05；全品种；参数类字段收口）：
- 证据产物（since2022；scope=all）：
  - `backtest_out\stage2\indicator_audit\20260605_b99_evidence_all_v1\b99_feature_summary_20260605_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260605_b99_followups_all_v1\b99_followups_stop_atr_summary_20260605_v1.csv`
- v0 裁决（研究侧；不改执行默认）?  - stop_dist_atr：CONFIG_BUCKET（止损率配置档；不做全局推荐?  - stop_k：DEPRECATE（与 stop_dist_atr 同构/别名，统丢命名?  - risk_per_trade：DIAG_ONLY（审?核对字段，不晋升门控?- 说明?.5 vs 2.0 的稳定不足以支持“默认调整；若未来要推荐甜点区，先补 trade_mae_atr/max_drawdown_per_trade

MULTI_AI_BATCH34_B30_B40_B50_EVIDENCE?026-06-04；全品种 B30/B40/B50 收口输入）：
- B30（StateVector；scope=all；split=since2022）：
  - `backtest_out\stage2\indicator_audit\20260604_b30_evidence_all_v1\b30_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b30_evidence_all_v1\b30_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b30_followups_all_v1\b30_stability_summary_20260604_v1.csv`
- B40（E1 retest bars；scope=all；split=since2022）：
  - `backtest_out\stage2\indicator_audit\20260604_b40_evidence_all_v1\b40_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b40_followups_all_v1\b40_stability_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b40_followups_all_v1\b40_interaction_sv_regime_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b40_followups_all_v1\b40_interaction_depth_atr_20260604_v1.csv`
- B50（entry_score / size_mult；scope=all；split=since2022）：
  - `backtest_out\stage2\indicator_audit\20260604_b50_evidence_all_v1\b50_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b50_followups_all_v1\b50_size_mult_agg_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b50_followups_all_v1\b50_entry_score_stability_20260604_v1.csv`

MULTI_AI_BATCH34_B30_B40_B50_DECISIONS?026-06-04；基于外部AI回帖收口；研究侧 v0）：
- 裁决：批?4的外部AI倾向?B40/entry_score 晋升?ENTRY_FILTER，但全品种分层稳定不足（多项 frac_both<0.60）→ 按先标签、后晋升”原则全部降级为研究侧标签，不改执行默认?- 去重与代表字段（v0）：
  - B30：`sv_votes_long_4` ?`sv_bias` 高相??只保?`sv_votes_long_4` 作为结构投票代表字段；`sv_bias` 降级?DIAG_ONLY（解释用?- ROLE MAP（v0；不做执行门控）?  - sv_regime_code：ENTRY_FILTER（regime 标签；与 C03 squeeze 语义丢致）
  - sv_atr_ratio_1h：RISK_ONLY（高波动风险提示?  - sv_bb_ratio_4h：DIAG_ONLY（需?regime 分层再讨论是否为 RISK/REDUCE?  - sv_votes_long_4：DIAG_ONLY（结构投票代表字段；先不晋升 gate?  - sv_votes_short_4：DIAG_ONLY（方向不对称；先不晋升）
  - e1_retest_bars：DIAG_ONLY（scheme=1_vs_ge2；bars=1 preferred 标签?=2 风险提示候；稳定性达标前不晋升）
  - entry_score：RISK_ONLY（极?bin 警示；甜点区不足以晋?gate?  - size_mult：CONFIG_BUCKET（仓位率档位；仅复盘/参数对照?- 晋升门槛（沿?v0）：只有当某字段?symbol×profile 上达到n_sufficient 足够 ?frac_both>=0.60”的稳定性，才允许从标签晋升?ENTRY_FILTER（硬过滤）?
MULTI_AI_BATCH38_B30_VOL_SQUEEZE_ATR_RATIO_EVIDENCE?026-06-04；外部AI回帖 + 本地补证据）?- 讨论对象：sv_bb_ratio_4h / sv_atr_ratio_1h
- 证据产物（scope=all；split=since2022）：
  - `backtest_out\stage2\indicator_audit\20260604_b30_evidence_all_v1\b30_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b30_followups_all_v1\b30_stability_summary_20260604_v1.csv`
  - 补证据（pooled 方向 + 合并桶稳定）：`backtest_out\stage2\indicator_audit\20260604_b30_followups_all_v2\*`
- 关键事实（合并桶 q10→q4；symbol×profile；n>=20）：
  - sv_atr_ratio_1h：n_sufficient=79；frac_both?.658（显著超过晋升门?0.60?  - pooled 合并桶：q4_bin1 avg_pnl?83.39 / stop_loss_rate?.288；q4_bin4 avg_pnl?8.27 / stop_loss_rate?.144（单调改善）
- 关键事实（sv_bb_ratio_4h；pooled bin1~bin4）：
  - q4_bin1/2 ?avg_pnl 为正?q4_bin3/4 为负 ?不支持甜点区”，更像“高值风险更大?
MULTI_AI_BATCH38_B30_VOL_SQUEEZE_ATR_RATIO_DECISIONS?026-06-04；研究侧 v0）：
- sv_atr_ratio_1h：ENTRY_FILTER（弱门槛：避免最?1/4；方?高更好）。默认不接入执行门控，先作为研究侧标签进入组合验证?- sv_bb_ratio_4h：DIAG_ONLY（收益与 MAE 口径不一致：pnl 看高更差，但 MAE/SL 并不支持“高风险”；不晋升过?风险门控）?- NEED_EVIDENCE：trade_mae_atr / max_drawdown_per_trade（笔持仓期最大不利波动；用于区分“只是不容易 hit stop?vs “持仓过程更痛苦”）?
MULTI_AI_BATCH38_B30_MAE_EVIDENCE?026-06-04；补?NEED_EVIDENCE：trade_mae_atr / trade_mfe_atr）：
- 证据产物（since2022；scope=all）：
  - `backtest_out\stage2\indicator_audit\20260604_b30_mae_all_v1\b30_mae_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b30_mae_all_v1\b30_mae_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b30_mae_all_v1\b30_mae_coverage_20260604_v1.csv`
- 关键事实（pooled；按 bucket 汇加权）?  - sv_atr_ratio_1h：高桶的 trade_mae_atr 更小（风险更低），方向与“弱门槛过滤朢低分位一?  - sv_bb_ratio_4h：高桶未表现出更?trade_mae_atr，且 stop_loss_rate 在高桶并不更差（q4_bin3 更低）→ 不支持高风险/减仓”的强结论，仅保留诊断标?
MULTI_AI_BATCH35_B60_SWING_LEVELS_EVIDENCE?026-06-04；B60 新家族；先证据后角色）：
- 证据产物（scope=all；since2022）：
  - `backtest_out\stage2\indicator_audit\20260604_b60_evidence_all_v1\b60_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b60_evidence_all_v1\b60_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b60_followups_all_v1\b60_stability_summary_20260604_v1.csv`
- pooled 起点（feature_summary）：sv_swing_low_4h(qtiles4) top_minus_bot?394.84；sv_swing_high_4h(qtiles4) top_minus_bot?129.41（仅表示 pooled 差异，不代表稳定性）
- 分层约束（stability_summary）：sv_swing_low_4h n_sufficient=0；sv_swing_high_4h n_sufficient=2 ?frac_both=0.0
- coverage（trades_baseline entry 行抽查汇总）：sv_swing_low_4h?9.37%；sv_swing_high_4h?0.59

MULTI_AI_BATCH35_B60_SWING_LEVELS_DECISIONS?026-06-04；基于外部AI回帖收口；研究侧 v0）：
- 裁决：在“全品种 + symbol×profile 分层稳定性的硬约束下，B60 当前只能 DIAG_ONLY（不进过滤池），不讨论任何硬门控与方向阈值?- ROLE MAP（v0；不做执行门控）?  - sv_swing_low_4h：DIAG_ONLY（coverage?9%；分层稳定?0?  - sv_swing_high_4h：DIAG_ONLY（coverage?1%；n_sufficient=2 ?frac_both=0.0?- 方向：暂不下结论（pooled ?top_minus_bot 不能说明单调/甜点区；霢要先?n_sufficient 提升?- 解冻门槛（v0）：当profile 合并 + 降桶 + 降门槛后，满?n_sufficient>=15 ?frac_both>=0.30 才允许讨论晋升（ADD/REDUCE 候）?=0.60 才允许讨?ENTRY_FILTER?- 朢小证据动作（v0）：
  - profile 合并?A_all + ?symbol 桶门?n>=10，重?b60-followups
  - 分桶改为 binary（near/far ?above/below median）以提升桶样?  - split 扩展?pre2022（或 full）做对照，验证是否窗口太短导致不?  - NEED_EVIDENCE：若要评估极值风险，霢定义并落?max_drawdown_per_trade（笔），再做 swing 极桶回撤对照

MULTI_AI_BATCH35_B60_EVIDENCE_DELTA_V2?026-06-04；补证据：布尔字段纳?+ 放宽分层门槛）：
- 新增纳入字段（trades_baseline 中原本为 True/False）：sv_risk_on_mkt / sv_use_struct_vote（以 code=0/1 分桶?- 放宽分层门槛：followups 采用 profile 合并?A_all，且 min_n=10（只用于“是否有丢致迹象的筛查，不用于晋升 gate?- 证据产物（since2022；scope=all）：
  - `backtest_out\stage2\indicator_audit\20260604_b60_evidence_all_v2\b60_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b60_followups_all_v2\b60_stability_summary_20260604_v1.csv`
- 结果摘录（symbol×A_all；min_n=10）：
  - sv_risk_on_mkt(code)：frac_both?.500；frac_stop_loss_better?.719（稳定明显好?swing 两条?  - sv_use_struct_vote(code)：frac_both?.469；frac_stop_loss_better?.625
- v0 更新（研究侧；不做执行门控）?  - sv_risk_on_mkt：RISK_ONLY（风险环境标签；优先用于仓位/止损风险解释?  - sv_use_struct_vote：ADD_CANDIDATE（结构确认加分；不晋?ENTRY_FILTER；pre2022 对照逢化，暂不升级?
MULTI_AI_BATCH44_B60_SWING_PRESENT_EVIDENCE?026-06-07；批?4补证据：swing_present 二桶）：
- 证据产物（since2022；scope=all）：
  - `backtest_out\stage2\indicator_audit\20260607_b60_evidence_all_v4\b60_bucket_stats_20260607_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260607_b60_followups_all_v4\b60_stability_summary_20260607_v1.csv`
- 结果摘录（symbol×A_all；min_n=15）：
  - sv_swing_present_4h(code)：n_sufficient=32；frac_both=0.5313；frac_stop_loss_better=0.8750
- 裁决（研究侧 v0.1）：
  - swing_present 通过“最后一试阈??保留 B60 研究价（?swing_present 做降维替代更稳）
  - sv_swing_high_4h / sv_swing_low_4h：解?PENDING_DEPRECATE，仍保持 DIAG_ONLY（冻结；不晋?gate?
MULTI_AI_BATCH46_B60_PRE2022_CHECK?026-06-08；补证据：pre2022 对照；min_n=10；profile_merge=A_all）：
- 证据产物（scope=all）：
  - since2022：`backtest_out\stage2\indicator_audit\20260608_b60_evidence_since2022_v2\b60_feature_summary_20260608_v1.csv` + `backtest_out\stage2\indicator_audit\20260608_b60_followups_since2022_v2\b60_stability_summary_20260608_v1.csv`
  - pre2022：`backtest_out\stage2\indicator_audit\20260608_b60_evidence_pre2022_v2\b60_feature_summary_20260608_v1.csv` + `backtest_out\stage2\indicator_audit\20260608_b60_followups_pre2022_v2\b60_stability_summary_20260608_v1.csv`
- 结果摘录（symbol×A_all；min_n=10）：
  - sv_swing_high_4h(qtiles4)：pre2022 n_sufficient=16；frac_both=0.250（较 since2022 ??.357 逢化）
  - sv_swing_low_4h(qtiles4)：pre2022 n_sufficient=15；frac_both?.267（较 since2022 ??.364 逢化）
  - sv_swing_present_4h(code)：pre2022 frac_both?.464（仍可作为条件型标签?  - sv_risk_on_mkt(code)：pre2022 frac_both?.393（风险环境标签仍合理?  - sv_use_struct_vote(code)：pre2022 frac_both?.357（维?DIAG_ONLY?- 裁决：不改既定角色（swing_high/low 冻结 DIAG_ONLY；swing_present 条件?ADD_CANDIDATE；risk_on=RISK_ONLY；use_struct_vote=DIAG_ONLY?
MULTI_AI_BATCH36_COMBO_V0_EVIDENCE?026-06-04；组合验?v0；全品种）：
- 目标：把已收口的 v0 标签/桶放到同丢张表里做“组合对照，验证是否存在“收益改善且风险同时改善”的稳定组合（只做研究，不改执行默认?- 证据产物（since2022；scope=all）：
  - `backtest_out\stage2\indicator_audit\20260604_combo_v0_all_v2\combo_v0_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_combo_v0_all_v2\combo_v0_top_20260604_v1.csv`
- 快事实（marginal；仅?bs/depth/bars 缺失的行；每?n>=100；按 n_trades 加权）：
  - sv_risk_on_mkt：risk=0 ?avg_pnl 更高?stop_loss_rate 更低（用于风险标?减仓提示更合理）
  - atr：bin1 明显更差，bin3/4 更好（支?atr=RISK_ONLY 的方向）

MULTI_AI_BATCH36_B31_STRUCT_VOTE_WINDOW_EVIDENCE?026-06-04；votes_3 vs votes_4）：
- 证据产物（since2022；scope=all）：
  - `backtest_out\stage2\indicator_audit\20260604_b31_evidence_all_v1\b31_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b31_followups_all_v1\b31_stability_summary_20260604_v1.csv`
- 关键事实（去重）：sv_bias ?sv_votes_long_3 ?sv_votes_long_4（同样的 top_minus_bot?30.41、同样的 n_sufficient=95 ?frac_both?.400）；sv_votes_short_3 ?sv_votes_short_4（同样的 top_minus_bot?130.41、同样的 n_sufficient=95 ?frac_both?.316?
MULTI_AI_BATCH36_B31_STRUCT_VOTE_WINDOW_DECISIONS?026-06-04；研究侧 v0）：
- 裁决：B31 不新增门控变量；整体区分力很弱（top_minus_bot?30 级别），不晋?gate；并执行“强同构字段去重?- ROLE MAP（v0；不做执行门控）?  - sv_bias：DIAG_ONLY（与 sv_votes_long_4 同构；二选一保留?  - sv_votes_long_4：DIAG_ONLY（与 sv_bias 同构；默认保留以保持?B30 命名丢致）
  - sv_votes_short_4：DIAG_ONLY（与 sv_votes_short_3 同构；保留代表字段）
  - sv_votes_long_3：DEPRECATE/DIAG_ONLY（冗余；不进入组合表主轴?  - sv_votes_short_3：DEPRECATE/DIAG_ONLY（冗余；不进入组合表主轴?
MULTI_AI_BATCH37_B99_PARAMS_EVIDENCE?026-06-04；stop_k / risk_per_trade）：
- 证据产物（since2022；scope=all）：
  - `backtest_out\stage2\indicator_audit\20260604_b99_evidence_all_v3\b99_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b99_evidence_all_v3\b99_bucket_stats_20260604_v1.csv`
- 快事实（pooled；value_code 汇）?  - stop_k=2.0 ?avg_pnl 略更好，?stop_loss_rate 更高 ?不支持改默认，只作为配置标签对照
  - risk_per_trade 是配置档位（?size_mult/风控配置相关），不作为信?
MULTI_AI_BATCH37_B99_PARAMS_DECISIONS?026-06-04；研究侧 v0）：
- stop_k：CONFIG_BUCKET（参数档位对照；禁止直接?ENTRY_FILTER；任何改默认”必须走分层稳定性与否决阈）
- risk_per_trade：CONFIG_BUCKET（风险预算档位；用于复盘/解释，不作为信号?
MULTI_AI_BATCH26_B50_EVIDENCE?026-06-03；指标批次讨?3：B50_SCORE_SIZING；先证据后角色）?- 证据产物（since2022；scope=core6+observe7）：
  - `backtest_out\stage2\indicator_audit\20260603_b50_evidence_v3\b50_bucket_stats_20260603_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260603_b50_evidence_v3\b50_feature_summary_20260603_v1.csv`
- 现状：entry_score 为甜点型”（非单调）；size_mult 为低熵档位（常见?1 / 1.15 等少数取值），在 v3 中已?value_code 分桶补齐证据
 - followups（直接用于验?落阈值）?   - `backtest_out\stage2\indicator_audit\20260603_b50_followups_v1\b50_size_mult_agg_20260603_v1.csv`
   - `backtest_out\stage2\indicator_audit\20260603_b50_followups_v1\b50_entry_score_stability_20260603_v1.csv`

MULTI_AI_BATCH26_B50_DECISIONS?026-06-03；基于外部AI回帖收口；研究侧 v0）：
- 裁决：entry_score 不合“越高越?越低越好”的线门控，更合 ENTRY_FILTER_SWEETSPOT（先排除低分位最差段；高分位段暂不作为更优的理由）size_mult 更像“仓位率档位/配置”，先做档位对照，不直接当交易信号?- ROLE MAP（v0；不做执行门控）?  - entry_score：ENTRY_FILTER_SWEETSPOT（研究侧标签；先排除 bin1-2；bin9-10 降级?observe 标签?  - size_mult：CONFIG_BUCKET（value_code 档位对照：如 size_mult=1 vs 1.15 的风?收益差异?- 统一验收口径（v0）：全局?n_trades>=100；单 symbol 若不足可降到 n_trades>=50 并合并桶；按 symbol×profile 的方向同向占?=70% 才允许写成建议阈值?- 重要发现：在 core6+observe7 的当前口径下，size_mult=1 的样本极少（followups 显示?7 trades），无法得出“档位差异结??size_mult 暂时只能当作“配置标签保留，不进入策略讨?
MULTI_AI_BATCH27_B40_EVIDENCE?026-06-03；指标批次讨?4：B40_E1_GEOMETRY；先证据后角色）?- 证据产物（since2022；scope=core6+observe7）：
  - `backtest_out\stage2\indicator_audit\20260603_b40_evidence_v1\b40_bucket_stats_20260603_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260603_b40_evidence_v1\b40_feature_summary_20260603_v1.csv`
- 现状：e1_retest_bars 主要集中?1/2/3 桶（?0 ?>=5 的桶），霢外部AI基于分桶与分层一致判断其角色（ENTRY_FILTER vs RISK/REDUCE?
MULTI_AI_BATCH27_B40_DECISIONS?026-06-03；基于外部AI回帖收口；研究侧 v0）：
- 裁决：e1_retest_bars 在全屢汇上呈局部非单调”（bucket=2 朢差bucket=3 朢好bucket=1 中），但在单 symbol/profile 维度桶样本不??暂不作为硬门控，仅做研究侧标签与分层变量
- ROLE MAP（v0；不做执行门控）?  - e1_retest_bars=2：RISK/REDUCE_CANDIDATE
  - e1_retest_bars=3：ENTRY_FILTER_PREFERRED
  - e1_retest_bars=1：BASELINE
- 统一验收口径（v0）：全局?n_trades>=100；单 symbol 桶先放宽?n_trades>=20（不足标?insufficient_data）；用合并桶后的方向同向占比>=70%”作为稳定标?
MULTI_AI_BATCH28_B99_EVIDENCE?026-06-04；指标批次讨?5：B99_OTHER；先证据后角色）?- 证据产物（since2022；scope=core6+observe7）：
  - `backtest_out\stage2\indicator_audit\20260603_b99_evidence_v1\b99_bucket_stats_20260603_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260603_b99_evidence_v1\b99_feature_summary_20260603_v1.csv`
- 归一化补证据（stop_dist_atr；离散档位对照；用于验证“甜点区/两端差是否存在）?  - `backtest_out\stage2\indicator_audit\20260603_b99_followups_v3\b99_followups_bucket_stats_20260603_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260603_b99_followups_v3\b99_followups_feature_summary_20260603_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260603_b99_followups_v3\b99_followups_stop_atr_pairs_20260603_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260603_b99_followups_v3\b99_followups_stop_atr_summary_20260603_v1.csv`
- 关键约束：当前证据里?stop 是绝对价/绝对距离”的混合口径，跨品种不可比；任何阈必须先做归丢化（推荐：stop_dist_atr=abs(entry-stop)/atr?
MULTI_AI_BATCH28_B99_DECISIONS?026-06-04；基于外部AI回帖收口；研究侧 v0）：
- 裁决：stop 先定位为 RISK_ONLY（仓?单笔风险参数），不直接当 ENTRY_FILTER。raw stop（绝对）跨品种不可比，必须先归一化后再讨论甜点区”是否稳定?- ROLE MAP（v0；不做执行门控）?  - stop_dist_atr（推荐派生列）：RISK_ONLY
  - 若在 stop_dist_atr 上出现稳定甜点区：最多升级为“轻量过?风险加权”（仍不建议做硬门槛?- 下一步最小证据动作（v0）：
  - ?trade-level merged 表里派生：`stop_dist = abs(entry - stop)`，`stop_dist_atr = stop_dist / atr`
  - ?stop_dist_atr 重新?B99 分位桶证据（建议 deciles10；并?symbol×profile 分层稳定性：全局?n>=100、单 symbol n>=20，不足合并桶/标记 insufficient_data?  - ?B30 ?sv_regime_code 做交互分层，验证“窄止损更易扫损”是否只发生在特?regime（如低波/挤压?- 已跑分层对照?0260603_v1；stop_atr=2.0 vs 1.5；按 symbol×profile；n>=20）：
  - 汇：n_pairs=13?.0 ?frac_pnl_better?.538，但 frac_stop_loss_better?.231、frac_both?.231 ?暂不支持?.0 全局更优”的门控/默认参数变更；仅作为配置标签与风险提示保?
MULTI_AI_BATCH30_DIAG_EVIDENCE?026-06-04；诊断标签：从题到分位桶证据）：
- 数据源约束：`p0_sweep_summary` 是每?symbol×profile 1 ??只能做profile 内跨 symbol 的分位桶”，不能?per-symbol 自己的分位桶，也不能直接映射逐笔 entry-time 过滤
- 证据产物（since2022；scope=all；profile ?qtiles4）：
  - `backtest_out\stage2\indicator_audit\20260604_diag_followups_v2\diag_followups_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_diag_followups_v2\diag_followups_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_diag_followups_v2\diag_followups_corr_20260604_v1.csv`

MULTI_AI_BATCH30_DIAG_DECISIONS?026-06-04；基于外部AI回帖收口；研究侧 v0）：
- 裁决：在当前证据口径下，diag_session_skew_ratio / diag_session_pnl_london ?top/bot 差异明显，但 top ?dd_ok_rate_w 未达到可直接?ENTRY_FILTER”的强度 ?先作?RISK/REDUCE 标签推进，不改执行默认?- ROLE MAP（v0；不做执行门控）?  - diag_session_skew_ratio：REDUCE_CANDIDATE（profile q4_bin1 风险预警；q4_bin4 仅作为加分标签）
  - diag_session_pnl_london：DIAG_ONLY（；霢?entry-time session 证据后再评估 ENTRY_FILTER/ADD?  - diag_kd_1d_k_median：DIAG_ONLY（；待与 C07 交叉决定 ADD vs EXIT?  - diag_entry_n：DIAG_ONLY（滞后诊?过度交易 sanity-check?- 下一步最小证据动作（v0）：
  - NEED_EVIDENCE（交易级）：基于 trades_baseline_* 为每笔交易生?entry_session(Asia/London/NY) 并做 “London-only vs 全时段?的笔对照
  - NEED_EVIDENCE（交叉）：在 C07 gate 通过?trades 子集上，?kd_1d_k_median 做分位桶对照 dd_ok_rate / avg_pnl

MULTI_AI_BATCH31_B10_SESSION_EVIDENCE?026-06-04；entry_time session 逐笔对照证据）：
- session 定义（与 diag 口径丢致；UTC）：hour<8=Asia；hour<16=London；else=NY
- 证据产物（since2022；scope=core_observe）：
  - `backtest_out\stage2\indicator_audit\20260604_b10_evidence_v1\b10_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b10_evidence_v1\b10_bucket_agg_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b10_evidence_v1\b10_london_vs_all_pairs_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_b10_evidence_v1\b10_london_vs_all_summary_20260604_v1.csv`
- 快事实（bucket_agg；core6_observe7）：
  - London avg_pnl?9.84（n=2806）显著高?ALL avg_pnl?.38（n=7109）；NY avg_pnl?35.26（n=2272?  - London vs All（按 symbol×profile；n_london>=20,n_all>=40）：n_pairs=38；frac_pnl_better?.632；frac_stop_loss_better?.711；frac_both?.500

MULTI_AI_BATCH31_B10_SESSION_DECISIONS?026-06-04；v0；先研究侧标记，不做执行门控）：
- 暂定：entry_session=London 作为 ENTRY_FILTER_CANDIDATE（偏“优先时段）；entry_session=NY 作为 RISK_ONLY/REDUCE_CANDIDATE（负期望预警）；Asia ?DIAG_ONLY（样本与 stop_loss_rate 偏高，需进一步分层解释）
- 下一步：如要晋升?gate，必须按 symbol×profile 做方向同向占比并给出朢小否决条件（避免仅靠 pooled 结论?
MULTI_AI_BATCH40_B10_SESSION_EVIDENCE?026-06-05；全品种；entry_time session 逐笔对照证据）：
- 证据产物（since2022；scope=all）：
  - `backtest_out\stage2\indicator_audit\20260605_b10_evidence_all_v1\b10_feature_summary_20260605_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260605_b10_evidence_all_v1\b10_bucket_agg_20260605_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260605_b10_evidence_all_v1\b10_london_vs_all_summary_20260605_v1.csv`
- 关键事实（pooled；bucket_agg）：Asia/London/NY ?avg_pnl 均为负（只体现相对差异，不支持直接硬过滤?- 分层丢致（London vs All；n_pairs=159）：frac_both?.453（边界，可作?ADD_CANDIDATE 讨论，但不足以直接晋?ENTRY_FILTER?
MULTI_AI_BATCH40_B10_SESSION_DECISIONS?026-06-05；研究侧 v0）：
- 裁决：entry_session 维持 DIAG_ONLY（不?London-only / avoid-NY 的硬门控）；London 仅作?ADD_CANDIDATE（边界，霢补交叉与风险口径才虑晋升?- ROLE MAP（v0；不做执行门控）?  - entry_session：DIAG_ONLY
  - London：ADD_CANDIDATE（弱；不落只?London”）
  - Asia：DIAG_ONLY（收益更接近 0，但 stop_loss_rate 更高且持仓更久）
  - NY：DIAG_ONLY（tp2_rate 高但 avg_pnl 更差；未?MAE 前不?RISK_ONLY?- 如要晋升/落阈值：先做 per-symbol 方向丢致（London vs All、NY vs non-NY? session×vol_state 交叉 + trade_mae_atr ?session 分组

MULTI_AI_BATCH96_B10_SESSION_MAE_DECISIONS?026-06-10；entry_session × trade_mae_atr）：
- 证据产物（core6+observe7；since2022/pre2022）：
  - `backtest_out\stage2\indicator_audit\20260610_b96_session_mae_core6observe7_since2022_v1\b96_session_mae_summary_20260610_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260610_b96_session_mae_core6observe7_pre2022_v1\b96_session_mae_summary_20260610_v1.csv`
- 关键事实?  - London：两段都表现?`frac_pnl_better>0.57` ?`frac_stop_loss_better>0.63`，但 `frac_mae_better` 只有 `0.148~0.309`
  - NY：两段都表现?`frac_stop_loss_better>=0.747` ?`frac_mae_better>=0.892`，但 since2022 `frac_pnl_better?.446`，收益侧不稳
  - Asia：三口径均不稳定
- 更新裁决（研究侧；不做执行门控）?  - entry_session：维?`DIAG_ONLY`
  - London：维?`ADD_CANDIDATE（弱）`，但明确不晋?`ENTRY_FILTER`
  - NY：上调为 `RISK_CONTEXT_HINT`（更不痛?朢终止损更少的风险标签），不等同收益更好，也不?avoid-NY 硬过?  - Asia：维?`DIAG_ONLY`
- 若未来继续投入：只允许做 `session × vol_state / regime` 交叉，检?session 是否只是别的环境标签代理；在此之前不讨论执行侧权重或硬时段过滤?
MULTI_AI_BATCH97_B10_SESSION_REGIME_DECISIONS?026-06-10；entry_session × sv_regime_code × sv_risk_on_mkt × MAE；scope=all）：
- 全局口径补充?  - 朢近补证据批次里，`93/94/95/96` 都是 `core6+observe7`，不是全屢 all；`97` 这一轮已改为 `scope=all`
- 关键事实?  - London ?`risk=1,regime=1/2` ?`risk=0,regime=0` 下都重复出现 `frac_mae_better` 很低（约 `0.113~0.280`），即使 `frac_pnl_better / frac_stop_loss_better` 可偏正，依然是更痛苦”的 trade-off
  - NY ?`risk=1,regime=1/2` 下都保持?`frac_stop_loss_better` + ?`frac_mae_better`（约 `0.707~0.934`），`risk=0,regime=0` 下也保留风险侧改善，但收益侧仍弱
- 更新裁决（研究侧；不做执行门控）?  - entry_session：维?`DIAG_ONLY`
  - London：维?`ADD_CANDIDATE（弱）`，但确认它不是简单环境代理，不晋升过?  - NY：`RISK_CONTEXT_HINT` 获得全局 + 分层二次确认，含义仍是更不痛?朢终止损更少，不是收益更好，也不做硬规?  - Asia：维?`DIAG_ONLY`

MULTI_AI_BATCH32_DIAG2_EVIDENCE?026-06-04；ADX/EMA/KD/vol_state；全品种分位桶证据）?- 数据源约束：仍基?`p0_sweep_summary`（每 symbol×profile 1 行）?只能做profile 内跨 symbol 的分位桶”，不能直接映射逐笔 entry-time 过滤
- 证据产物（since2022；scope=all；profile ?qtiles4；可复现命令?关于日活.md）：
  - `backtest_out\stage2\indicator_audit\diag_rank_20260604_v2.csv`
  - `backtest_out\stage2\indicator_audit\20260604_diag_followups_v3\diag_followups_bucket_stats_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_diag_followups_v3\diag_followups_feature_summary_20260604_v1.csv`
  - `backtest_out\stage2\indicator_audit\20260604_diag_followups_v3\diag_followups_corr_20260604_v1.csv`
- 去重结论（证据）：`diag_ema144_regime_long_frac` vs `diag_ema_stack_bull_frac` spearman=1.0（A_relaxed/A_strict/A_universal 全部?1.0）→ 视为重复字段

MULTI_AI_BATCH32_DIAG2_DECISIONS?026-06-04；基于外部AI回帖收口；研究侧 v0）：
- v0 ROLE MAP（研究侧标记；不做执行门控）?  - diag_ema144_regime_long_frac：ADD_CANDIDATE（profile ?q4_bin4 加分）；REDUCE_CANDIDATE（q4_bin1 逆风预警?  - diag_kd_4h_k_median：DIAG_ONLY（；?kd_1d 高相关，先不独立晋升?  - diag_vol_state_squeeze_frac：RISK_ONLY（REGIME_TAG；用于风险提?风险权重；需逐笔证据再定是否可门控）
  - diag_kd_align_3tf_frac：DIAG_ONLY（区分力弱；待交易级再评估）
  - diag_adx_*：DIAG_ONLY（当前框架内优先级低?  - diag_ema_stack_bull_frac：DEPRECATE（与 ema144_regime 完全重复?- 下一步最小证据动作（v0）：
  - NEED_EVIDENCE（交易级）：?EMA/KD/vol_state ?entry-time 状落?trades_baseline（笔分桶），验证是否能从“品种画像推广到“入场时点过滤?
MULTI_AI_BATCH41_DIAG_TOP_DEDUP_DECISIONS?026-06-05；去重为主；研究?v0）：
- 本批不重新定义批?0/32既有角色，只做字段去?+ 保留字段名标准化?- 去重（硬证据）：
  - `diag_ema144_regime_long_frac` vs `diag_ema_stack_bull_frac`：corr spearman=1.0 ?DEPRECATE `diag_ema_stack_bull_frac`
  - London 计数三件套（p0_sweep_summary）：`diag_session_count_london` vs `diag_session_trades_london` spearman=1.0；且?`diag_session_entry_vol_ratio_london_n` spearman?.99961 ?只保?`diag_session_entry_vol_ratio_london_n`，DEPRECATE `diag_session_count_london` / `diag_session_trades_london`
- 保留字段名清单（<=5；用于后续对?报表）：
  - diag_session_skew_ratio
  - diag_session_pnl_london
  - diag_entry_n
  - diag_ema144_regime_long_frac
  - diag_session_entry_vol_ratio_london_n

NEXT_PRIORITIES_TSV?026-06-03；下丢批先讨论→再字段→再实验”的优先级）?priority_id	family	scope	why_now	next_deliverable
P1_ADX_TREND	ADX趋势强度	fx/index/commodities	已有 diag_adx_* 列位但此前仅占位，且只依?OHLC，最易先做成“可对比诊断?diag_adx_* ?entry_time 抽样统计；用?allow2_only_in_trend ?entry_min_votes 的证据分?P1_EMA_REGIME	EMA144分界+多EMA结构(13/21/55/144)	fx/index/commodities	与既有P0规则壳一致（EMA144 同侧/排列），可把“趋势环境显式化并与 vol_state 对照	新增 diag_ema144_regime_long_frac/diag_ema144_regime_short_frac + diag_ema_stack_bull_frac/bear_frac/mixed_frac（entry抽样?P1_KDJ_MTF	KDJ/Stochastic 多周期对?4H/1D/1W)	fx/index/commodities	资料库高频出现（KD共振/5-50-95），且仓库已?kdj() ?resample_ohlcv()，可直接落地为诊断标?新增 diag_kd_align_4h_1d_frac/diag_kd_align_3tf_frac + diag_kd_4h_k_median/diag_kd_1d_k_median（entry抽样?P2_BB_SQUEEZE	布林紧口/震荡识别	fx/index/commodities	与现?vol_state(SQUEEZE)可交叉验证，避免“挤压定义漂移?新增 diag_bb_squeeze_frac 与其?entry 的分层收益对?P2_ASHARE_CYCLE_REGIME	周期女王A股周期状态机	a?先把“想”落成可观测字段?0日涨幅榜/top10/朢早涨?包容度），再谈股与仓?定义 ashare_regime_state（枚举）+ 朢小数据依赖清单（来自 ashare_preprocess 产物?
SOURCE_LIBRARY_FILE_INDEX_TSV（v0；先“索引→摘抄→可测试字段”，不直接等同策略）?source_id	source_path	topic	type	extract_priority
S03_CORE_V12	d:\Stock\trading_analysis\03_迭代后核心母版V1.2\#量化分析体系V1.2.md	母版总览	md	P1
S03_GAS_V12	d:\Stock\trading_analysis\03_迭代后核心母版V1.2\体系GAS_可量化辑拆解归档V1.2.md	GAS 体系	md	P1
S02_ATOMIC_TABLE	d:\Stock\trading_analysis\02_原子化拆解文件\原子规则?md	263条原子规则（趋势/入场/出场/风控/过滤/仓位/消息?md	P0
S02_WYCKOFF_4PHASE	d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_威科夫_价格周期四阶段量化规?md	威科夫四阶段	md	P1
S02_WYCKOFF_SPRING	d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_威科夫_弹簧Spring与上抛UT量化判定.md	Spring/UT	md	P2
S02_HARMONIC_FILTER	d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_谐波交易_入场过滤与止损止盈用规则.md	谐波过滤/止损止盈	md	P1
S02_KD_BASE	d:\Stock\trading_analysis\02_原子化拆解文件\抢术指标_随机指标_KD基础用法量化规则.md	KD 基础	md	P1
S02_VOL_SHAPE	d:\Stock\trading_analysis\02_原子化拆解文件\抢术指标_补充抢术_成交量形态量化识别规?md	成交量形?md	P0
S01_V11_MOTHER	d:\Stock\trading_analysis\01_初整理文档备份_禁止修改\量化分析体系V1.1_核心母版.md	V1.1 母版	md	P2
S01_GAS_MOTHER	d:\Stock\trading_analysis\01_初整理文档备份_禁止修改\体系GAS_核心母版.md	GAS 核心母版	md	P2
S00_MQ4_ZUP	d:\Stock\trading_analysis\00_指标定义&公式\ZUP_v15[1][1].1.mq4	ZUP 谐波指标	mq4	P1
S00_MQ4_STOCH	d:\Stock\trading_analysis\00_指标定义&公式\Stochastic.mq4	随机指标	mq4	P1
S00_TXT_VOLPRICE	d:\Stock\trading_analysis\00_指标定义&公式\[副图指标]量价时空_来自神奇数字系列指标[文华].txt	量价时空	txt	P0
S00_TXT_CYCLE	d:\Stock\trading_analysis\00_指标定义&公式\[副图指标]循环徢复_来自神奇数字系列指标[文华].txt	循环徢?txt	P1
S00_BOOK_TURTLE_RULES	d:\Stock\trading_analysis\00_交易系统书籍\04_海龟交易法则\海龟交易法则_STEP_C_朢终合并版_丢页纸规则?md	海龟规则?md	P1

SOURCE_LIBRARY_INDICATOR_FILE_COVERAGE_NOTES（v0；指标源文件覆盖率与量化难度备注）：
- 说明：当前批次化家族（indicator_batches）只覆盖已经进入 p0_sweep/trades_baseline 的特征列；不在特征列里的“原始指标文件不会自动进入批次，霢要单独做“指标实现→落字段→再纳入批次?- `00_指标定义&公式` 目录概况?026-06-05）：
  - mq4? 个（已入索引 2 个：ZUP/Stochastic；未入索?3 个：0_Harmony_06/a_ZZ/VoltyChannel_Stop_v2_1M?  - txt?3 个（目前只索引了 2 个代表文件；其余多为同名指标的不同版?不同平台脚本?
未入批次/量化难度备注（v0）：
- `00_指标定义&公式\ZUP_v15[1][1].1.mq4`：未量化；难?高（谐波形?zigzag+fibo，存在容差重?重算问题；需先定义非重绘”的形确认时点与输出字段?- `00_指标定义&公式\0_Harmony_06.mq4`：未量化；难?高（谐波形族：AB=CD/Gartley/Butterfly/Bat/Crab；同上）
- `00_指标定义&公式\a_ZZ.mq4`：部分可量化；难?中（zigzag/swing 点可做结?摆动”字段，但必须先定口径：是否允许重绘、如何落?entry-time 可用的特征）
- `00_指标定义&公式\VoltyChannel_Stop_v2_1M.mq4`：可量化但接入成?中（MA+ATR 通道/跟踪止损；更像风控组?出场线，霢要明确输出：通道宽度/方向/距离、以及用于诊断还是用于参数）
- `00_指标定义&公式\Stochastic.mq4`：已部分量化；难?低（仓库已有 KD/KDJ 相关 diag_* 字段，但霢确认周期参数丢致：该文件包含两套参?13/3/3 ?55/13/13?- `00_指标定义&公式\*.txt`（文?神奇数字系列与一牛一熊谓之道”等）：大多未量化；难度=高（语言/平台差异 + 语义命名不自解释 + 多版本同名；建议先做“指标族分组索引→挑 1 个可落字段的朢小子集，再推进）
S00_BOOK_MURPHY_MA	d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\raw_chapters\第九章_移动平均?md	均线体系	md	P2
S00_BOOK_MURPHY_VOL	d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\raw_chapters\第七章_交易量和持仓兴趣.md	量能/持仓兴趣	md	P2
S00_DA_YIN_TRADING_SYS	d:\Stock\trading_analysis\00_大隐体系\3)大隐交易系统\1.大隐操作系统详细讲解和进出场条件规定.mp4.md	大隐交易系统（定量进出场?md	P1
S00_DA_YIN_ANGLE_KD	d:\Stock\trading_analysis\00_大隐体系\2)大隐於朝二维时空抢术讲座系列\6.[第五课]如何用堆成角度线和stochastic oscillator指标组进场和加仓.mp4.md	对称角度?KD进场加仓	md	P1
S00_DA_YIN_KD_SLOGAN	d:\Stock\trading_analysis\00_大隐体系\0)stochastic oscillator指标组的各种讲解\8_1.四句指标组口询.jpg	KD指标组口询（图?jpg	P1
S00_CYCLE_QUEEN_RULES	d:\Stock\trading_analysis\00_周期女王\99_可用规则壳\周期状系统规则壳.md	A股周期状态体系（规则?状机/词典?md	P0

SOURCE_LIBRARY_INDICATOR_DOC_SCAN_V1?026-06-06；基于文件名关键词扫描；先记录，后续再多AI消化）：
- 说明：该清单不等同已量化”它只是把可能与指标/抢术分析相关的资料先纳入可追踪索引；后续按 quant_feasibility 分层推进?  - EASY（可直接拆成字段/规则）：优先来自 `02_原子化拆解文件`（文本已原子化，适合直接落成 feature spec?  - MED（可量化但需明确口径/可用时点）：`03_迭代后核心母版V1.2`、`00_交易系统书籍`、`01_初整理文档备份_禁止修改`
  - HARD（不先做“规则壳/状机/词典”很难量化）：`00_大隐体系`、`00_周期女王`
- 扫描命中统计（TOTAL_HITS=118）：
  - 03_迭代后核心母版V1.2?
  - 02_原子化拆解文件：45
  - 01_初整理文档备份_禁止修改?
  - 00_周期女王?
  - 00_交易系统书籍?1
  - 00_大隐体系?4
- 命中清单（相对路径；按目录分组）?  - 03_迭代后核心母版V1.2/01_核心抢术体系模?[模块]ALBrooks_入场信号与交易执?md
  - 03_迭代后核心母版V1.2/01_核心抢术体系模?[模块]ALBrooks_趋势判定与基硢定义.md
  - 03_迭代后核心母版V1.2/01_核心抢术体系模?[模块]威科夫_四阶段量价突破体?md
  - 03_迭代后核心母版V1.2/01_核心抢术体系模?[模块]斐波那契_回调扩展时间共振体系.md
  - 03_迭代后核心母版V1.2/01_核心抢术体系模?[模块]谐波交易_六大形风控体?md
  - 03_迭代后核心母版V1.2/04_抢术指标用法模?[模块]抢术指标_KD随机指标与补充技术综合分析体?md
  - 03_迭代后核心母版V1.2/04_抢术指标用法模?[模块]时空波浪_计数推动共振分析体系.md
  - 02_原子化拆解文?抢术指标_时空波浪_二维时空共振交易规则.md
  - 02_原子化拆解文?抢术指标_时空波浪_二维时空时间周期规则.md
  - 02_原子化拆解文?抢术指标_时空波浪_推动浪与调整浪量化特?md
  - 02_原子化拆解文?抢术指标_时空波浪_波浪延伸与失败量化判?md
  - 02_原子化拆解文?抢术指标_时空波浪_波浪计数量化规则.md
  - 02_原子化拆解文?抢术指标_补充抢术_价格形量化识别规?md
  - 02_原子化拆解文?抢术指标_补充抢术_成交量形态量化识别规?md
  - 02_原子化拆解文?抢术指标_随机指标_KDJ与MACD共振量化规则.md
  - 02_原子化拆解文?抢术指标_随机指标_KD基础用法量化规则.md
  - 02_原子化拆解文?抢术指标_随机指标_KD背离量化判定规则.md
  - 02_原子化拆解文?抢术指标_随机指标_KD钝化识别与应对规?md
  - 02_原子化拆解文?抢术指标_随机指标_多周期KD共振与过滤规?md
  - 02_原子化拆解文?核心抢术_ALBrooks_EMA均线量化用法规则.md
  - 02_原子化拆解文?核心抢术_ALBrooks_交易区间量化判定与策?md
  - 02_原子化拆解文?核心抢术_ALBrooks_信号棒质量量化评?md
  - 02_原子化拆解文?核心抢术_ALBrooks_入场形?0个量化判?md
  - 02_原子化拆解文?核心抢术_ALBrooks_区间陷阱与假突破识别规则.md
  - 02_原子化拆解文?核心抢术_ALBrooks_反转量化识别与入场规?md
  - 02_原子化拆解文?核心抢术_ALBrooks_总在场内状判定规?md
  - 02_原子化拆解文?核心抢术_ALBrooks_止损位量化设置规?md
  - 02_原子化拆解文?核心抢术_ALBrooks_目标位测量与盈亏比规?md
  - 02_原子化拆解文?核心抢术_ALBrooks_趋势回调量化规则.md
  - 02_原子化拆解文?核心抢术_ALBrooks_趋势强度量化评分.md
  - 02_原子化拆解文?核心抢术_ALBrooks_趋势棒与十字星量化定?md
  - 02_原子化拆解文?核心抢术_威科夫_价格周期四阶段量化规?md
  - 02_原子化拆解文?核心抢术_威科夫_供需关系量价分析规则.md
  - 02_原子化拆解文?核心抢术_威科夫_努力与结果法则量化规?md
  - 02_原子化拆解文?核心抢术_威科夫_复合人操作量化分?md
  - 02_原子化拆解文?核心抢术_威科夫_弹簧Spring与上抛UT量化判定.md
  - 02_原子化拆解文?核心抢术_威科夫_突破回测确认量化规则.md
  - 02_原子化拆解文?核心抢术_斐波那契_回调位量化交易规?md
  - 02_原子化拆解文?核心抢术_斐波那契_多周期共振交易规?md
  - 02_原子化拆解文?核心抢术_斐波那契_弧线支撑阻力分析规则.md
  - 02_原子化拆解文?核心抢术_斐波那契_扇形线趋势分析规?md
  - 02_原子化拆解文?核心抢术_斐波那契_扩展位目标位测量规则.md
  - 02_原子化拆解文?核心抢术_斐波那契_时间周期量化规则.md
  - 02_原子化拆解文?核心抢术_谐波交易_ABCD形量化规?md
  - 02_原子化拆解文?核心抢术_谐波交易_三重推动TripleDrive量化规则.md
  - 02_原子化拆解文?核心抢术_谐波交易_入场过滤与止损止盈用规则.md
  - 02_原子化拆解文?核心抢术_谐波交易_加特利Gartley形量化规?md
  - 02_原子化拆解文?核心抢术_谐波交易_蝙蝠Bat形量化规?md
  - 02_原子化拆解文?核心抢术_谐波交易_蝴蝶Butterfly形量化规?md
  - 02_原子化拆解文?核心抢术_谐波交易_螃蟹Crab形量化规?md
  - 02_原子化拆解文?特色优化_趋势启动点量化识别规?md
  - 02_原子化拆解文?特色优化_趋势衰竭点量化识别规?md
  - 01_初整理文档备份_禁止修改/体系大隐_时空波浪.md
  - 01_初整理文档备份_禁止修改/体系大隐_随机指标.md
  - 01_初整理文档备份_禁止修改/参书_ALBrooks价格行为.md
  - 01_初整理文档备份_禁止修改/参书_威科夫操盘法.md
  - 01_初整理文档备份_禁止修改/参书_斐波那契体系.md
  - 01_初整理文档备份_禁止修改/参书_谐波交易?md
  - 00_周期女王/02_周期自然之力/4.发书了课本导图模板提取_ev.mp4_导出.md
  - 00_周期女王/99_可用规则?周期状系统规则壳.md
  - 00_周期女王/99_可用规则?周期状系统规则壳_个股案例拆解.md
  - 00_周期女王/99_可用规则?周期状系统规则壳_临盘复盘视频.md
  - 00_周期女王/99_可用规则?周期状系统规则壳_自然之力.md
  - 00_交易系统书籍/01_期货市场抢术分析_墨菲/archive/墨菲_STATE_TEMPLATE_V1_朢终版_19切片.md
  - 00_交易系统书籍/01_期货市场抢术分析_墨菲/raw_chapters/第九章_移动平均?md
  - 00_交易系统书籍/01_期货市场抢术分析_墨菲/raw_chapters/第五章_主要反转形?md
  - 00_交易系统书籍/01_期货市场抢术分析_墨菲/raw_chapters/第六章_持续形?md
  - 00_交易系统书籍/01_期货市场抢术分析_墨菲/raw_chapters/第十三章_艾略特波浪理?md
  - 00_交易系统书籍/01_期货市场抢术分析_墨菲/raw_chapters/第四章_趋势的基本概?md
  - 00_交易系统书籍/01_期货市场抢术分析_墨菲/墨菲_STATE_TEMPLATE_V1_全书朢终版_34切片.md
  - 00_交易系统书籍/03_交易系统与方法_Kaufman/archive/Kaufman_STATE_TEMPLATE_V1_朢终版_32切片.md
  - 00_交易系统书籍/03_交易系统与方法_Kaufman/archive/Kaufman_STEP_C_朢终版_STATE_TEMPLATE_V1.md
  - 00_交易系统书籍/03_交易系统与方法_Kaufman/Kaufman_STATE_TEMPLATE_V1_全书朢终版_36切片.md
  - 00_交易系统书籍/04_海龟交易法则/海龟交易法则_STEP_C_朢终合并版_丢页纸规则?md
  - 00_大隐体系/0)stochastic oscillator指标组的各种讲解/0.stochastic oscillator指标组实战应用详细讲?mp4.md
  - 00_大隐体系/0)stochastic oscillator指标组的各种讲解/1.[专业抢术课]stochastic oscillator指标组的深入讲解.mp4.md
  - 00_大隐体系/0)stochastic oscillator指标组的各种讲解/2.持仓量指标概念使用方法与规则在期货交易中的应?mp4.md
  - 00_大隐体系/0)stochastic oscillator指标组的各种讲解/3.[精华尽出]stochastic oscillator指标组设计想、应用方法详?mp4.md
  - 00_大隐体系/0)stochastic oscillator指标组的各种讲解/4.stochastic oscillator指标组钝化后涨跌判断询?mp4.md
  - 00_大隐体系/0)stochastic oscillator指标组的各种讲解/5.如何在MT4软件?建立和设置stochastic oscillator(KD)指标和指标模?mp4.md
  - 00_大隐体系/0)stochastic oscillator指标组的各种讲解/6.关于如何把股票走势图移植到MT4软件?stochastic oscillator指标组和指标模板应用的问?并对股票、期货外汇等全市场品种指标组和指标模板的建立和使用方法做了较为详尽的介绍.mp4.md
  - 00_大隐体系/0)stochastic oscillator指标组的各种讲解/9.指标组口询的视频教学课?mp4.md
  - 00_大隐体系/1)大隐时空波浪相关课程视频/1.大隐时空波浪基础课讲?mp4.md
  - 00_大隐体系/1)大隐时空波浪相关课程视频/10.有关用力度线做空铁矿石的相关抢术问?mp4.md
  - 00_大隐体系/1)大隐时空波浪相关课程视频/15.大隐波浪理论基础课：波浪理论无法克服的致命软?mp4.md
  - 00_大隐体系/1)大隐时空波浪相关课程视频/19.如何用大隐ABC波浪数浪规则进行数浪.mp4.md
  - 00_大隐体系/1)大隐时空波浪相关课程视频/20.三波涨跌和五波涨跌对后市走势的影?大隐ABC波浪专业?.mp4.md
  - 00_大隐体系/1)大隐时空波浪相关课程视频/21.小转大条件下的大隐二维时空波浪技?mp4.md
  - 00_大隐体系/1)大隐时空波浪相关课程视频/23.如何对PTA2101进行大隐二维时空抢术分?mp4.md
  - 00_大隐体系/1)大隐时空波浪相关课程视频/26.[大隐波浪教学课]如何提前判断和确定C浪的大小.mp4.md
  - 00_大隐体系/1)大隐时空波浪相关课程视频/28.[大隐二维时空波浪关键课程]如何正确使用对称角度?如何正确应用黄金分割线进行B转A判断.mp4.md
  - 00_大隐体系/1)大隐时空波浪相关课程视频/29.大隐二维时空波浪理论专业基础?mp4.md
  - 00_大隐体系/1)大隐时空波浪相关课程视频/30.[大隐二维时空波浪进阶课程]如何在大趋势过程中拿住趋势单(中继楔形在趋势过程中的作?.mp4.md
  - 00_大隐体系/1)大隐时空波浪相关课程视频/31.[大隐二维时空波浪提高课程]中继楔形的动力学原理及其实战中的应用.mp4.md
  - 00_大隐体系/1)大隐时空波浪相关课程视频/35.[大隐二维时空波浪基础课教学]如何用好对称角度线进行技术分?mp4.md
  - 00_大隐体系/1)大隐时空波浪相关课程视频/36.[大隐二维时空波浪重要内容]各级别顶底判断和确认抢?mp4.md
  - 00_大隐体系/1)大隐时空波浪相关课程视频/8.力度线应用原?mp4.md
  - 00_大隐体系/2)大隐於朝二维时空抢术讲座系?11.对称角度线和力度线完美配合下的白糖指数走势案例讲?mp4.md
  - 00_大隐体系/2)大隐於朝二维时空抢术讲座系?13.[大隐二维时空抢术基硢课]B转A.mp4.md
  - 00_大隐体系/2)大隐於朝二维时空抢术讲座系?14.对称角度线和黄金分割详尽分析美糖11号指?mp4.md
  - 00_大隐体系/2)大隐於朝二维时空抢术讲座系?15.[大隐二维时空抢术基硢课精华]时间完美和时间背?mp4.md
  - 00_大隐体系/2)大隐於朝二维时空抢术讲座系?24.[教学课]趋势逆转的转弯半?mp4.md
  - 00_大隐体系/2)大隐於朝二维时空抢术讲座系?25.[专业基础课程]如何理解和应用涨跌时空升级问?mp4.md
  - 00_大隐体系/2)大隐於朝二维时空抢术讲座系?26.趋势逆转的必要条件和充分条件.mp4.md
  - 00_大隐体系/2)大隐於朝二维时空抢术讲座系?27.[实战抢能]关于大隐二维时空升级不升级的补充教学视频.mp4.md
  - 00_大隐体系/2)大隐於朝二维时空抢术讲座系?3.[第三课]浪形强弱判断工具(对称角度?.mp4.md
  - 00_大隐体系/2)大隐於朝二维时空抢术讲座系?31.[教学视频课]大隐二维时空波浪数浪规则和指?mp4.md
  - 00_大隐体系/2)大隐於朝二维时空抢术讲座系?35.[大隐二维时空波浪课程]对称角度线升级版：变异角度线抢术原理以及使用要?mp4.md
  - 00_大隐体系/2)大隐於朝二维时空抢术讲座系?5.[第四课]结合实战讲解对称角度?mp4.md
  - 00_大隐体系/2)大隐於朝二维时空抢术讲座系?6.[第五课]如何用堆成角度线和stochastic oscillator指标组进场和加仓.mp4.md
  - 00_大隐体系/2)大隐於朝二维时空抢术讲座系?7.级别于对称角度线之二.mp4.md
  - 00_大隐体系/2)大隐於朝二维时空抢术讲座系?8.级别与对称角度线之三.mp4.md
  - 00_大隐体系/2)大隐於朝二维时空抢术讲座系?9.大隐波浪四种浪形的划分以及对ABC三浪的定?mp4.md
  - 00_大隐体系/3)大隐交易系统/9.[高阶交易抢术]对称角度线形态与安全加仓法深度融合技?mp4.md
  - 00_大隐体系/4)大隐波段交易抢术专?2.[大隐二维时空波浪基础课重要补充]大B浪时空大小对大C浪时空大小的影响和作?mp4.md
  - 00_大隐体系/4)大隐波段交易抢术专?3.[波段操作课程]如何第一时间发现大级别顶?以及如何在大趋势中做趋势和波?mp4.md
  - 00_大隐体系/4)大隐波段交易抢术专?8.[波段进场提高课]深入浅出讲解根据大隐波段形技术进场典型案?收割波段利润的技术和方法.mp4.md
  - 00_大隐体系/6)综合抢术专?1.[综合抢术课程]震荡格局中的压力支撑位与力度线的关系和应?mp4.md

SOURCE_LIBRARY_FILE_INDEX_TSV_EXT?026-06-03；目录全量文件列表；用于覆盖率统计与后续摘抄排期）：
source_path	type	topic_guess
d:\Stock\trading_analysis\03_迭代后核心母版V1.2\#量化分析体系V1.2.md	md	量化分析体系V1.2总览
d:\Stock\trading_analysis\03_迭代后核心母版V1.2\体系GAS_可量化辑拆解归档V1.2.md	md	GAS可量化辑拆解
d:\Stock\trading_analysis\03_迭代后核心母版V1.2\05_交易系统闭环模块\[模块]交易系统_五步骤资金风控复盘心理全体系.md	md	交易系统闭环
d:\Stock\trading_analysis\03_迭代后核心母版V1.2\04_抢术指标用法模块\[模块]时空波浪_计数推动共振分析体系.md	md	时空波浪
d:\Stock\trading_analysis\03_迭代后核心母版V1.2\04_抢术指标用法模块\[模块]抢术指标_KD随机指标与补充技术综合分析体?md	md	KD随机指标
d:\Stock\trading_analysis\03_迭代后核心母版V1.2\03_交易策略执行模块\[模块]交易策略与优化_波段超短特色优化综合体系.md	md	波段/超短/优化
d:\Stock\trading_analysis\03_迭代后核心母版V1.2\02_题材与标的择模块\[模块]题材中军_筛建仓协同撤逢全体?md	md	题材中军
d:\Stock\trading_analysis\03_迭代后核心母版V1.2\01_核心抢术体系模块\[模块]斐波那契_回调扩展时间共振体系.md	md	斐波那契
d:\Stock\trading_analysis\03_迭代后核心母版V1.2\01_核心抢术体系模块\[模块]谐波交易_六大形风控体?md	md	谐波交易
d:\Stock\trading_analysis\03_迭代后核心母版V1.2\01_核心抢术体系模块\[模块]威科夫_四阶段量价突破体?md	md	威科夫四阶段
d:\Stock\trading_analysis\03_迭代后核心母版V1.2\01_核心抢术体系模块\[模块]ALBrooks_趋势判定与基硢定义.md	md	ALBrooks趋势
d:\Stock\trading_analysis\03_迭代后核心母版V1.2\01_核心抢术体系模块\[模块]ALBrooks_入场信号与交易执?md	md	ALBrooks入场
d:\Stock\trading_analysis\02_原子化拆解文件\题材标_中军筛五维量化模?md	md	题材/中军筛模?d:\Stock\trading_analysis\02_原子化拆解文件\题材标_中军龙头补涨协同交易策略.md	md	题材/协同策略
d:\Stock\trading_analysis\02_原子化拆解文件\题材标_中军定义与核心识别标?md	md	题材/中军定义
d:\Stock\trading_analysis\02_原子化拆解文件\题材标_中军买点与仓位管理规?md	md	题材/买点与仓?d:\Stock\trading_analysis\02_原子化拆解文件\题材标_中军卖点与撤逢纪律规则.md	md	题材/卖点与撤逢
d:\Stock\trading_analysis\02_原子化拆解文件\特色优化_震荡区间优化量化策略.md	md	震荡优化
d:\Stock\trading_analysis\02_原子化拆解文件\特色优化_趋势启动点量化识别规?md	md	趋势启动
d:\Stock\trading_analysis\02_原子化拆解文件\特色优化_多维度信号融合量化规?md	md	信号融合
d:\Stock\trading_analysis\02_原子化拆解文件\特色优化_趋势衰竭点量化识别规?md	md	趋势衰竭
d:\Stock\trading_analysis\02_原子化拆解文件\特色优化_仓位动优化量化规?md	md	仓位动优?d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_谐波交易_蝴蝶Butterfly形量化规?md	md	谐波Butterfly
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_谐波交易_螃蟹Crab形量化规?md	md	谐波Crab
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_谐波交易_蝙蝠Bat形量化规?md	md	谐波Bat
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_谐波交易_入场过滤与止损止盈用规则.md	md	谐波通用过滤/止盈止损
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_谐波交易_加特利Gartley形量化规?md	md	谐波Gartley
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_谐波交易_三重推动TripleDrive量化规则.md	md	谐波TripleDrive
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_谐波交易_ABCD形量化规?md	md	谐波AB=CD
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_斐波那契_时间周期量化规则.md	md	斐波那契时间
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_斐波那契_扩展位目标位测量规则.md	md	斐波那契扩展
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_斐波那契_扇形线趋势分析规?md	md	斐波那契扇形
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_斐波那契_弧线支撑阻力分析规则.md	md	斐波那契弧线
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_斐波那契_多周期共振交易规?md	md	斐波那契共振
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_斐波那契_回调位量化交易规?md	md	斐波那契回调
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_威科夫_突破回测确认量化规则.md	md	威科夫回测确?d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_威科夫_复合人操作量化分?md	md	威科夫复合人
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_威科夫_弹簧Spring与上抛UT量化判定.md	md	威科夫Spring/UT
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_威科夫_努力与结果法则量化规?md	md	威科夫努力与结果
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_威科夫_供需关系量价分析规则.md	md	威科夫供霢
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_威科夫_价格周期四阶段量化规?md	md	威科夫四阶段量化
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_ALBrooks_趋势棒与十字星量化定?md	md	ALBrooks趋势?十字?d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_ALBrooks_趋势回调量化规则.md	md	ALBrooks趋势回调
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_ALBrooks_趋势强度量化评分.md	md	ALBrooks趋势强度评分
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_ALBrooks_目标位测量与盈亏比规?md	md	ALBrooks目标?盈亏?d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_ALBrooks_止损位量化设置规?md	md	ALBrooks止损设置
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_ALBrooks_总在场内状判定规?md	md	ALBrooks总在场内
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_ALBrooks_反转量化识别与入场规?md	md	ALBrooks反转入场
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_ALBrooks_区间陷阱与假突破识别规则.md	md	ALBrooks假突?陷阱
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_ALBrooks_入场形?0个量化判?md	md	ALBrooks入场形?d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_ALBrooks_交易区间量化判定与策?md	md	ALBrooks交易区间
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_ALBrooks_EMA均线量化用法规则.md	md	ALBrooks EMA用法
d:\Stock\trading_analysis\02_原子化拆解文件\核心抢术_ALBrooks_信号棒质量量化评?md	md	ALBrooks信号棒评?d:\Stock\trading_analysis\02_原子化拆解文件\抢术指标_随机指标_多周期KD共振与过滤规?md	md	KD多周期共?d:\Stock\trading_analysis\02_原子化拆解文件\抢术指标_随机指标_KD钝化识别与应对规?md	md	KD钝化
d:\Stock\trading_analysis\02_原子化拆解文件\抢术指标_随机指标_KD背离量化判定规则.md	md	KD背离
d:\Stock\trading_analysis\02_原子化拆解文件\抢术指标_随机指标_KD基础用法量化规则.md	md	KD基础
d:\Stock\trading_analysis\02_原子化拆解文件\抢术指标_随机指标_KDJ与MACD共振量化规则.md	md	KDJ+MACD共振
d:\Stock\trading_analysis\02_原子化拆解文件\抢术指标_补充抢术_成交量形态量化识别规?md	md	成交量形?d:\Stock\trading_analysis\02_原子化拆解文件\抢术指标_补充抢术_价格形量化识别规?md	md	价格形?d:\Stock\trading_analysis\02_原子化拆解文件\抢术指标_时空波浪_波浪计数量化规则.md	md	波浪计数
d:\Stock\trading_analysis\02_原子化拆解文件\抢术指标_时空波浪_波浪延伸与失败量化判?md	md	波浪延伸/失败
d:\Stock\trading_analysis\02_原子化拆解文件\抢术指标_时空波浪_推动浪与调整浪量化特?md	md	推动/调整?d:\Stock\trading_analysis\02_原子化拆解文件\抢术指标_时空波浪_二维时空时间周期规则.md	md	二维时空周期
d:\Stock\trading_analysis\02_原子化拆解文件\抢术指标_时空波浪_二维时空共振交易规则.md	md	二维时空共振
d:\Stock\trading_analysis\02_原子化拆解文件\交易系统_风控体系_回撤控制量化规则.md	md	回撤控制
d:\Stock\trading_analysis\02_原子化拆解文件\交易系统_资金管理_仓位配置量化规则.md	md	仓位配置
d:\Stock\trading_analysis\02_原子化拆解文件\交易系统_心理管理_情绪控制量化规则.md	md	心理/情绪
d:\Stock\trading_analysis\02_原子化拆解文件\交易系统_复盘优化_量化复盘规则.md	md	量化复盘
d:\Stock\trading_analysis\02_原子化拆解文件\交易系统_五步骤闭环量化规?md	md	五步骤闭?d:\Stock\trading_analysis\02_原子化拆解文件\交易策略_超短操作_打板与接力量化规?md	md	超短打板/接力（A股）
d:\Stock\trading_analysis\02_原子化拆解文件\交易策略_波段超短_策略切换量化规则.md	md	策略切换
d:\Stock\trading_analysis\02_原子化拆解文件\交易策略_波段操作_选股与择时量化规?md	md	选股/择时（A股）
d:\Stock\trading_analysis\02_原子化拆解文件\交易策略_波段操作_止损止盈量化规则.md	md	波段止损止盈
d:\Stock\trading_analysis\02_原子化拆解文件\原子规则?md	md	原子规则?d:\Stock\trading_analysis\01_初整理文档备份_禁止修改\量化分析体系V1.1_核心母版.md	md	V1.1母版
d:\Stock\trading_analysis\01_初整理文档备份_禁止修改\参书_题材股中?md	md	参书题材中军
d:\Stock\trading_analysis\01_初整理文档备份_禁止修改\参书_谐波交易?md	md	参书谐波
d:\Stock\trading_analysis\01_初整理文档备份_禁止修改\参书_斐波那契体系.md	md	参书斐波
d:\Stock\trading_analysis\01_初整理文档备份_禁止修改\参书_威科夫操盘法.md	md	参书威科?d:\Stock\trading_analysis\01_初整理文档备份_禁止修改\参书_ALBrooks价格行为.md	md	参书ALBrooks
d:\Stock\trading_analysis\01_初整理文档备份_禁止修改\体系补充_特色优化.md	md	特色优化
d:\Stock\trading_analysis\01_初整理文档备份_禁止修改\体系大隐_随机指标.md	md	大隐随机指标
d:\Stock\trading_analysis\01_初整理文档备份_禁止修改\体系大隐_闭环体系.md	md	大隐闭环体系
d:\Stock\trading_analysis\01_初整理文档备份_禁止修改\体系大隐_波段超短.md	md	大隐波段超短
d:\Stock\trading_analysis\01_初整理文档备份_禁止修改\体系大隐_时空波浪.md	md	大隐时空波浪
d:\Stock\trading_analysis\01_初整理文档备份_禁止修改\体系GAS_核心母版.md	md	GAS核心母版
d:\Stock\trading_analysis\00_指标定义&公式\菩提无树_来自神奇数字系列指标[金鼎].txt	txt	菩提无树（金鼎）
d:\Stock\trading_analysis\00_指标定义&公式\明镜非台_来自神奇数字系列指标[金鼎].txt	txt	明镜非台（金鼎）
d:\Stock\trading_analysis\00_指标定义&公式\周复始_来自神奇数字系列指标[金鼎].txt	txt	周复始（金鼎?d:\Stock\trading_analysis\00_指标定义&公式\[副图指标]量价时空_来自神奇数字系列指标[文华]2.0.txt	txt	量价时空（文?.0?d:\Stock\trading_analysis\00_指标定义&公式\[副图指标]量价时空_来自2.0神奇数字指标[文华].txt	txt	量价时空?.0文华?d:\Stock\trading_analysis\00_指标定义&公式\[副图指标]循环徢复_来自神奇数字系列指标[文华]2.0.txt	txt	循环徢复（文华2.0?d:\Stock\trading_analysis\00_指标定义&公式\[副图指标]循环徢复_来自神奇数字系列指标[文华].txt	txt	循环徢复（文华?d:\Stock\trading_analysis\00_指标定义&公式\[副图指标]循环徢复_来自神奇数字和用数字指标[文华].txt	txt	循环徢复（神奇+通用?d:\Stock\trading_analysis\00_指标定义&公式\[副图指标]循环徢复_来自2.0神奇数字指标[文华].txt	txt	循环徢复（2.0文华?d:\Stock\trading_analysis\00_指标定义&公式\[副图指标]周复始_来自神奇数字系列指标[文华]2.0.txt	txt	周复始（文华2.0?d:\Stock\trading_analysis\00_指标定义&公式\[副图指标]周复始_来自神奇数字系列指标[文华].txt	txt	周复始（文华?d:\Stock\trading_analysis\00_指标定义&公式\[副图指标]周复始_来自神奇数字和用数字指标[文华].txt	txt	周复始（神奇+通用?d:\Stock\trading_analysis\00_指标定义&公式\[副图指标]周复始_来自2.0神奇数字指标[文华].txt	txt	周复始（2.0文华?d:\Stock\trading_analysis\00_指标定义&公式\[主图K线形态]回头是岸_来自神奇数字系列指标[文华].txt	txt	回头是岸（主图形态）
d:\Stock\trading_analysis\00_指标定义&公式\[主图K线形态]回头是岸_来自神奇数字和用数字指标[文华].txt	txt	回头是岸（主图形态）
d:\Stock\trading_analysis\00_指标定义&公式\[K线附属指标]飞天遁地_来自神奇数字系列指标[文华].txt	txt	飞天遁地（K线附属）
d:\Stock\trading_analysis\00_指标定义&公式\[K线附属指标]飞天遁地_来自神奇数字和用数字指标[文华].txt	txt	飞天遁地（K线附属）
d:\Stock\trading_analysis\00_指标定义&公式\[K线附属指标]迷知返_来自神奇数字系列指标[文华]2.0.txt	txt	迷知返（K线附?.0?d:\Stock\trading_analysis\00_指标定义&公式\[K线附属指标]进有度_来自神奇数字系列指标[文华].txt	txt	进有度（K线附属）
d:\Stock\trading_analysis\00_指标定义&公式\[K线附属指标]进有度_来自2.0神奇数字指标[文华].txt	txt	进有度（K线附?.0?d:\Stock\trading_analysis\00_指标定义&公式\[K线附属指标]菩提无树_来自神奇数字系列指标[文华].txt	txt	菩提无树（文华）
d:\Stock\trading_analysis\00_指标定义&公式\[K线附属指标]菩提无树_来自神奇数字和用数字指标[文华].txt	txt	菩提无树（神?通用?d:\Stock\trading_analysis\00_指标定义&公式\[K线附属指标]绳趋尺步_来自神奇数字系列指标[文华]2.0.txt	txt	绳趋尺步?.0文华?d:\Stock\trading_analysis\00_指标定义&公式\[K线附属指标]绳趋尺步_来自神奇数字系列指标[文华].txt	txt	绳趋尺步（文华）
d:\Stock\trading_analysis\00_指标定义&公式\[K线附属指标]绳趋尺步_来自2.0神奇数字指标[文华].txt	txt	绳趋尺步?.0文华?d:\Stock\trading_analysis\00_指标定义&公式\[K线附属指标]明镜非台_来自神奇数字系列指标[文华]2.0.txt	txt	明镜非台?.0文华?d:\Stock\trading_analysis\00_指标定义&公式\[K线附属指标]明镜非台_来自神奇数字系列指标[文华].txt	txt	明镜非台（文华）
d:\Stock\trading_analysis\00_指标定义&公式\[K线附属指标]明镜非台_来自神奇数字和用数字指标[文华].txt	txt	明镜非台（神?通用?d:\Stock\trading_analysis\00_指标定义&公式\[K线附属指标]明镜非台_来自2.0神奇数字指标[文华].txt	txt	明镜非台?.0文华?d:\Stock\trading_analysis\00_指标定义&公式\[K线附属指标]审时度势_来自神奇数字系列指标[文华].txt	txt	审时度势（K线附属）
d:\Stock\trading_analysis\00_指标定义&公式\[K线附属指标]审时度势_来自神奇数字和用数字指标[文华].txt	txt	审时度势（神?通用?d:\Stock\trading_analysis\00_指标定义&公式\09：随笔十丢_来自丢牛一熊谓之道.txt	txt	随笔十一（一牛一熊谓之道?d:\Stock\trading_analysis\00_指标定义&公式\09：随笔十_来自丢牛一熊谓之道.txt	txt	随笔十（丢牛一熊谓之道?d:\Stock\trading_analysis\00_指标定义&公式\08：随笔六_来自丢牛一熊谓之道.txt	txt	随笔六（丢牛一熊谓之道?d:\Stock\trading_analysis\00_指标定义&公式\08：随笔八_来自丢牛一熊谓之道.txt	txt	随笔八（丢牛一熊谓之道?d:\Stock\trading_analysis\00_指标定义&公式\08：随笔五_来自丢牛一熊谓之道.txt	txt	随笔五（丢牛一熊谓之道?d:\Stock\trading_analysis\00_指标定义&公式\08：随笔七_来自丢牛一熊谓之道.txt	txt	随笔七（丢牛一熊谓之道?d:\Stock\trading_analysis\00_指标定义&公式\07：随笔四_来自丢牛一熊谓之道.txt	txt	随笔四（丢牛一熊谓之道?d:\Stock\trading_analysis\00_指标定义&公式\07：随笔二_来自丢牛一熊谓之道.txt	txt	随笔二（丢牛一熊谓之道?d:\Stock\trading_analysis\00_指标定义&公式\07：随笔三_来自丢牛一熊谓之道.txt	txt	随笔三（丢牛一熊谓之道?d:\Stock\trading_analysis\00_指标定义&公式\04  通道四象 (通道丢元论的展弢)_来自丢牛一熊谓之道.txt	txt	通道四象
d:\Stock\trading_analysis\00_指标定义&公式\02  阻线 (时空体系)_来自丢牛一熊谓之道.txt	txt	阻线
d:\Stock\trading_analysis\00_指标定义&公式\01  趋势?(朢基本的技术手?_来自丢牛一熊谓之道.txt	txt	趋势?d:\Stock\trading_analysis\00_指标定义&公式\Stochastic.mq4	mq4	随机指标（MT4?d:\Stock\trading_analysis\00_指标定义&公式\ZUP_v15[1][1].1.mq4	mq4	ZUP谐波（MT4?d:\Stock\trading_analysis\00_指标定义&公式\a_ZZ.mq4	mq4	ZigZag（MT4?d:\Stock\trading_analysis\00_指标定义&公式\0_Harmony_06.mq4	mq4	谐波（MT4?d:\Stock\trading_analysis\00_指标定义&公式\VoltyChannel_Stop_v2_1M.mq4	mq4	通道止损（MT4?d:\Stock\trading_analysis\00_交易系统书籍\99_流程模板\三本书_STEP_C_滚动合并与锚点补?md	md	三本书模?d:\Stock\trading_analysis\00_交易系统书籍\02_通向财务自由之路_VanTharp\任务1_通向财务自由之路_14条锚点补?md	md	VanTharp任务1锚点
d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\墨菲_STATE_TEMPLATE_V1_全书朢终版_34切片.md	md	墨菲STATE模板
d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\墨菲_STEP_B_ch01_ch09_ch15_批次4.md	md	墨菲STEP_B批次4
d:\Stock\trading_analysis\00_交易系统书籍\02_通向财务自由之路_VanTharp\VT_4条NEED_EVIDENCE_补齐方案.md	md	VT缺锚点补?d:\Stock\trading_analysis\00_交易系统书籍\03_交易系统与方法_Kaufman\Kaufman_STEP_B_ch24_批次8.md	md	Kaufman批次8
d:\Stock\trading_analysis\00_交易系统书籍\03_交易系统与方法_Kaufman\Kaufman_STATE_TEMPLATE_V1_全书朢终版_36切片.md	md	KaufmanSTATE模板
d:\Stock\trading_analysis\00_交易系统书籍\03_交易系统与方法_Kaufman\Kaufman_STEP_B_ch23_批次7.md	md	Kaufman批次7
d:\Stock\trading_analysis\00_交易系统书籍\03_交易系统与方法_Kaufman\Kaufman_STEP_B_ch21_批次6.md	md	Kaufman批次6
d:\Stock\trading_analysis\00_交易系统书籍\04_海龟交易法则\海龟交易法则_STEP_C_朢终合并版_丢页纸规则?md	md	海龟丢页纸规则
d:\Stock\trading_analysis\00_交易系统书籍\03_交易系统与方法_Kaufman\Kaufman_STEP_B_ch18_ch20_批次5.md	md	Kaufman批次5
d:\Stock\trading_analysis\00_交易系统书籍\03_交易系统与方法_Kaufman\Kaufman_STEP_B_ch09_ch12_批次4.md	md	Kaufman批次4
d:\Stock\trading_analysis\00_交易系统书籍\03_交易系统与方法_Kaufman\Kaufman_STEP_B_ch08_批次3.md	md	Kaufman批次3
d:\Stock\trading_analysis\00_交易系统书籍\03_交易系统与方法_Kaufman\Kaufman_STEP_B_ch03_道氏理论.md	md	Kaufman道氏
d:\Stock\trading_analysis\00_交易系统书籍\03_交易系统与方法_Kaufman\Kaufman_STEP_B_ch02批次1.md	md	Kaufman批次1
d:\Stock\trading_analysis\00_交易系统书籍\03_交易系统与方法_Kaufman\任务2_交易系统与方法_Kaufman_STEP_A.md	md	Kaufman任务2
d:\Stock\trading_analysis\00_交易系统书籍\99_流程模板\三本书_STEP_A_切片计划.md	md	三本书STEP_A
d:\Stock\trading_analysis\00_交易系统书籍\04_海龟交易法则\海龟交易法则_STEP_B_切片提炼_批次3.md	md	海龟STEP_B批次3
d:\Stock\trading_analysis\00_交易系统书籍\04_海龟交易法则\海龟交易法则_STEP_B_切片提炼_批次2.md	md	海龟STEP_B批次2
d:\Stock\trading_analysis\00_交易系统书籍\04_海龟交易法则\海龟交易法则_STEP_B_切片提炼_批次1.md	md	海龟STEP_B批次1
d:\Stock\trading_analysis\00_交易系统书籍\02_通向财务自由之路_VanTharp\book2_通向财务自由之路_STEP_A_B_切片提炼.md	md	VT切片提炼
d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\raw_chapters\第四章_趋势的基本概?md	md	趋势基本概念
d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\raw_chapters\第十章_摆动指数和相反意见理?md	md	摆动指数/相反意见
d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\raw_chapters\第十四章_时间周期.md	md	时间周期
d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\raw_chapters\第十六章_资金管理和交易策?md	md	资金管理/交易策略
d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\raw_chapters\第十五章_计算机和交易系统.md	md	交易系统
d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\raw_chapters\第十二章_三点转向和优化点数图.md	md	三点转向/点数?d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\raw_chapters\第十三章_艾略特波浪理?md	md	艾略特波?d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\raw_chapters\第十丢章_日内点数?md	md	日内点数?d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\raw_chapters\第六章_持续形?md	md	持续形?d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\raw_chapters\第八章_长期图表和商品指?md	md	长期图表/指数
d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\raw_chapters\第五章_主要反转形?md	md	主要反转形?d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\raw_chapters\第二章_道氏理论.md	md	道氏理论
d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\raw_chapters\第九章_移动平均?md	md	移动平均?d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\raw_chapters\第七章_交易量和持仓兴趣.md	md	交易?持仓兴趣
d:\Stock\trading_analysis\00_交易系统书籍\01_期货市场抢术分析_墨菲\raw_chapters\第一章_抢术分析的理论基础.md	md	抢术分析基硢

d:\Stock\trading_analysis\00_大隐体系\0)stochastic oscillator指标组的各种讲解\0.stochastic oscillator指标组实战应用详细讲?mp4.md	md	stochastic oscillator指标组实?d:\Stock\trading_analysis\00_大隐体系\0)stochastic oscillator指标组的各种讲解\1.[专业抢术课]stochastic oscillator指标组的深入讲解.mp4.md	md	stochastic指标组深?d:\Stock\trading_analysis\00_大隐体系\0)stochastic oscillator指标组的各种讲解\2.持仓量指标概念使用方法与规则在期货交易中的应?mp4.md	md	持仓量指?d:\Stock\trading_analysis\00_大隐体系\0)stochastic oscillator指标组的各种讲解\3.[精华尽出]stochastic oscillator指标组设计想、应用方法详?mp4.md	md	stochastic指标组设计想
d:\Stock\trading_analysis\00_大隐体系\0)stochastic oscillator指标组的各种讲解\4.stochastic oscillator指标组钝化后涨跌判断询?mp4.md	md	钝化后涨跌判?d:\Stock\trading_analysis\00_大隐体系\0)stochastic oscillator指标组的各种讲解\5.如何在MT4软件?建立和设置stochastic oscillator(KD)指标和指标模?mp4.md	md	MT4设置KD模板
d:\Stock\trading_analysis\00_大隐体系\0)stochastic oscillator指标组的各种讲解\6.关于如何把股票走势图移植到MT4软件?stochastic oscillator指标组和指标模板应用的问?并对股票、期货外汇等全市场品种指标组和指标模板的建立和使用方法做了较为详尽的介绍.mp4.md	md	股票图移植到MT4
d:\Stock\trading_analysis\00_大隐体系\0)stochastic oscillator指标组的各种讲解\7.如何对比分析不同品种之间的走势差异和强弱牛熊.mp4.md	md	跨品种强弱对?d:\Stock\trading_analysis\00_大隐体系\0)stochastic oscillator指标组的各种讲解\8_1.四句指标组口询.jpg	jpg	KD四句口诀
d:\Stock\trading_analysis\00_大隐体系\0)stochastic oscillator指标组的各种讲解\9.指标组口询的视频教学课?mp4.md	md	口诀教学
d:\Stock\trading_analysis\00_大隐体系\2)大隐於朝二维时空抢术讲座系列\6.[第五课]如何用堆成角度线和stochastic oscillator指标组进场和加仓.mp4.md	md	角度?KD进场加仓
d:\Stock\trading_analysis\00_大隐体系\3)大隐交易系统\1.大隐操作系统详细讲解和进出场条件规定.mp4.md	md	交易系统进出场条?d:\Stock\trading_analysis\00_大隐体系\6)综合抢术专栏\1.[综合抢术课程]震荡格局中的压力支撑位与力度线的关系和应?mp4.md	md	震荡支撑压力/力度?
d:\Stock\trading_analysis\00_周期女王\99_可用规则壳\周期状系统规则壳.md	md	周期状系统规则壳
d:\Stock\trading_analysis\00_周期女王\99_可用规则壳\周期状系统规则壳_自然之力.md	md	规则壳（自然之力?d:\Stock\trading_analysis\00_周期女王\99_可用规则壳\周期状系统规则壳_个股案例拆解.md	md	规则壳（个股案例?d:\Stock\trading_analysis\00_周期女王\99_可用规则壳\周期状系统规则壳_临盘复盘视频.md	md	规则壳（临盘复盘?
QUANTIFIABLE_RULE_EXCERPTS_TSV（v0；来自原子规则表.md”前200行示例；用于后续落到可测?diag/feature）：
rule_id	role	trigger	veto	action	params	required_data	source_hint
R_EMA144_TREND	RISK	close above EMA144 => bull; below => bear	NA	trend_regime	EMA(144)	close	原子规则? GAS核心母版（界?EMA144?R_VOL_CONFIRM	ENTRY	break key level with volume >= 1.5*avg5	volume < 1.5*avg5	filter false_breakout	avg5=5bars	tick_volume	原子规则? 量能匹配过滤?日均?.5倍）
R_ASIA_LOW_VOL_FILTER	RISK	Asia session low-volume move triggers signal	Europe/US overlap volume expansion	filter Asia noise	session=Asia	time+tick_volume	原子规则? 外汇亚洲盘时段无量波动过?R_EVENT_FILTER	RISK	NFP/Fed etc around release window	NA	filter event window	window TBD	events_calendar_utc	原子规则? 重大数据前后过滤
R_VOL_DIVERGENCE_REDUCE	REDUCE	price up but volume shrinking	NA	reduce 50%	NA	close+tick_volume	原子规则? 量价顶背离减?R_HIGH_VOL_STALL_EXIT	EXIT	high volume but no advance / volume down candle	NA	exit all	NA	close+tick_volume	原子规则? 高位放量滞涨/放量下跌清仓
R_VOLATILITY_PROFILE	RISK	high vol symbols (XAUUSD/crosses)	NA	use strict risk profile	k TBD	ATR/volatility	原子规则? 高波动画像启?R_POSITION_CAP_N	RISK	base lot N=equity/10000	max pos > 2N	block new orders	N=equity/10000	equity	原子规则? 朢大持仓不超过2N

DA_YIN_RULE_EXCERPTS_TSV（v0；大隐体系：先摘“可复现”的定量句；用于后续落到可测?diag/feature）：
rule_id	role	trigger	invalidation	params	required_data	source_hint
DY_WEDGE_ENTRY_LONG	ENTRY	wedge exists (>=3 waves) AND internal_subwave breaks 0.618 upward AND pullback does not break prior low	break prior low	fib=0.618; pattern=wedge	price	大隐交易系统: 进出场条件规定（楔形+0.618+回调不破前低?DY_WEDGE_ENTRY_SHORT	ENTRY	wedge exists (>=3 waves) AND internal_subwave breaks 0.618 downward AND pullback does not break prior high	break prior high	fib=0.618; pattern=wedge	price	大隐交易系统: 进出场条件规定（做空对称?DY_NECKLINE_ENTRY	ENTRY	use neckline (support/resistance) as trigger; do not use trendline for entry	break back through neckline	neckline=prior swing level	price	大隐交易系统: “进场不用趋势线，只霢要用颈线?DY_ANGLE_FAKE_TOP_FILTER	RISK	if turning point is inside symmetric angle line => likely fake (true top prob ~10%-20%)	next swing breaks structure high/low inside	fake_top_prob~0.8-0.9	price	大隐角度?KD: 内侧头部多为假（真底概率小）
DY_ANGLE_TRUE_TOP_FILTER	RISK	if turning point is outside symmetric angle line => likely true (prob ~80%-90%)	next swing invalidates by reclaiming angle line	true_top_prob~0.8-0.9	price	大隐角度?KD: 外侧头部大概率真顶部
DY_FORCE_DECAY_PARTIAL_EXIT	EXIT	on trend run, time expands but space contracts (momentum decays)	space expands again (new impulse)	exit_partial=50%	price	大隐角度?KD: 空头衰竭时平丢半留丢半?DY_KD_4LINE_SLOGAN	DIAG	new high then KD golden cross => soon top; new low then dead cross => soon bottom; after golden cross new highs continue; after dead cross new lows continue	NA	NA	price+KD	四句指标组口询图（大隐於朝?
CYCLE_QUEEN_ASHARE_EXCERPTS_TSV（v0；周期女王：A股周期状态机与观测口径；先作为研究层/选池层状态标签）?item_id	type	definition	observable_proxies	suggested_action	source_hint
CQ_ATTACK_SUSTAINED	state	攻击有持续（上涨周期?前交易日领涨/空间板持续不换人；阵型不散；失败可修复（包容度）	可做顺势/围绕头部；少换股	周期状系统规则壳: LEXICON 2.3
CQ_ATTACK_UNSUSTAINED	state	攻击无持续（逢?下降周期?频繁换领?换空间板；前交易日领涨不持续；头部持续下杢	降低频率/以防守为?只做确定性极?周期状系统规则壳: LEXICON 2.4
CQ_HANDOVER	state	交权磨合期（过渡?老领涨示弱且新领涨未明确；多候竞争；盘面反复犹豫	轻仓试错/等待新领涨持续确?周期状系统规则壳: MAP ?CQ_RESIDUAL_HEAT	state	余温（鱼尾巴/惯）	高位反复无法新高；名牌归丢/末期化；风险上升	只虑?不追?周期状系统规则壳: LEXICON 2.5
CQ_CUT_COMPLETE	state	切割完成（周期终点线?满足其一：领涨A杢；或连续杢空间?-4?切换到观察新面孔；禁在切割中重仓	周期状系统规则壳: LEXICON 2.6
CQ_INCUBATION	state	孕化（新周期未确认前?切割后新面孔尝试持续；情绪转暖但阵型未确?只试?不重仓；观察是否形成攻击阵型	周期状系统规则壳: LEXICON 2.7
CQ_CONFIRM_ATTACK	state	确认攻击（攻击阵型成形）	前交易日领涨带扩散；3-4只阵型；情绪回暖；包容度出现	围绕阵型做；识别分期转移	周期状系统规则壳: LEXICON 2.8
CQ_METRIC_10D_TOP10	metric	10日区间涨幅榜前十用于定情绪周期范?10日区间涨幅榜（只看主?0cm?top10变化作为 regime proxy	周期状系统规则壳: LEXICON 2.12
CQ_METRIC_EARLIEST_LIMITUP	metric	前交易日涨停时间朢早且在前十?领涨	涨停时间（前十范围内?领涨识别/阵型构建	周期状系统规则壳: LEXICON 2.13

FORMULA_EXCERPTS_TSV（v0；用于把“指标名”落到可实现公式/参数；先摘最确定的三条）?indicator_id	source_path	params	key_outputs
vol_price_time_v2	d:\Stock\trading_analysis\00_指标定义&公式\[副图指标]量价时空_来自神奇数字系列指标[文华]2.0.txt	XUN=8;HUAN=34;JIE=144;V?EMA(VOL,XUN);V?EMA(VOL,HUAN);V?EMA(VOL,JIE)	?(V?V?AND VOL>V?;?(V?V?AND VOL<V?
cycle_kd_v2	d:\Stock\trading_analysis\00_指标定义&公式\[副图指标]循环徢复_来自神奇数字系列指标[文华]2.0.txt	BEN=3;KUAI=13;MAN=55;SHI=233;K/D三组SMA	揸沽=(??快金叉和)-(??快死叉和)
stochastic_dual_mq4	d:\Stock\trading_analysis\00_指标定义&公式\Stochastic.mq4	(13,3,3) + (55,13,13); iStochastic(pin,tim,...)	a1/a2=?信号(13?; b1/b2=?信号(55?

### 0.0.9 模拟盘自动执行（可；出道协议 v0?
允许范围：仅模拟盘；严格按低频小手数、只吃最?1H、随时可 close_all”的出道协议执行；任何异常立即回?plan/monitor?
朢小协议（v0）：
- 预检：`.\mt5_daily_ops.ps1 -Mode status` ?True；`.\mt5_daily_ops.ps1 -Mode plan` 显示 `[DD] status=OK`
- 首次只跑单次执行留证据（max_loops=1，entry_lot=0.01，entry_max_orders=1，entry_lookback_bars=1?- 弢仓后立刻“锁仓：?`EntryMaxOrders` 设为 0，避免同日重复开?- 当天对账：`.\mt5_daily_ops.ps1 -Mode summary`

### 0.1 讨论用证据摘录（给外部AI，直接复制粘贴）

说明：外部云端模型常无法访问 `d:\Stock\...` 的本机路径，因此请把下面“摘录块”直接放进它们的 EVIDENCE PACK?
摘录A｜阶段二大框架（v13，已定60?
```
框架? 模块）：
1) 资料层：规则?入口索引（SOURCE_ANCHOR，固定落?docs\rules_index.md?2) 数据层：data\（行?1H + 宏观/事件 + A股天?直播间聚合结果）
3) 研究层：回测、scan→replay→commentary（产?out_dir + research_index_YYYYMMDD.csv；不做入池裁决）
4) 选池层：screen→focus→core / deploy_core-observe-exclude（只做分层与落盘；只?research_index，不扫目录）
5) 执行层：默认只观察；观察也要留证据（observe_YYYYMMDD.csv ?out_dir?6) 复盘层：踩坑→规?缺口（回填阶段一记录?
边界切刀?- A股天?直播间聚合属于数据层
- 研究层输?out_dir 证据 + 研究索引表（口径通过列明确，供池层消费）
- 选池层只消费“聚?研究索引表生成池?
资料层统丢入口索引（docs\rules_index.md）最小列（每行）?- anchor_id, topic, source, excerpt

研究索引表（research_index_YYYYMMDD.csv）最小列?- 标识：scope, symbol, window, profile, run_id
- 指标：net_pnl, final_max_drawdown_pct, trades, win_rate
- 口径通过：pass_A/pass_B/pass_C/pass_D?/1?- 口径选择：criterion_selected（A/B/C/D?- 运行状：status（completed/failed/error?- 复现与证据：out_dir, repro_cmd, ok, error

pass_B/C/D v0 定义（摘要）?- pass_B：pass_A==1 ?final_max_drawdown_pct <= 25.0
- pass_C：同丢 symbol/profile 的可用窗口数 N>=2，且扢有窗?pass_A==1 ?pass_B==1
- pass_D：同丢 symbol/profile 的可用窗口数 N>=2，且 pass_A 占比>=0.6 ?pass_B 占比>=0.6
- 计算约束：pass_C/pass_D ?symbol+profile ?window 聚合计算，并回填到该组所有行

数据层（A股聚合产物，固定文件名）?- data\ashare_watchlist\factors_ladder_YYYYMMDD.csv
- data\ashare_watchlist\watchlist_screen_YYYYMMDD.csv
- data\ashare_watchlist\focus_pool_YYYYMMDD.csv/.txt
- data\ashare_watchlist\core_pool_YYYYMMDD.csv/.txt
- data\ashare_watchlist\blogroom_codes_YYYYMMDD.csv（及 blogroom_summary/topics/names?
选池层裁决文件：
- 每周裁决：data\ashare_watchlist\ruling_YYYYMMDD.json（core/observe/exclude + reason + evidence?- 默认映射（v0，symbol 级唯丢裁决；先降维后映射）?  - 先对同一 symbol 做降维：?criterion_selected 计算 pass_selected；若同一 symbol 有多?profile，优先?pass_selected==1 ?profile，取 net_pnl 朢大为 best_profile；否则在 pass_A_any==1 ?profile 中取 net_pnl 朢大为 best_profile
  - 映射：missing_in_research_index→observe；status_not_completed→exclude；pass_selected==1→core?criterion∈{B,C,D}且pass_selected==0且pass_A_any==1)→observe；其他→exclude
- 约束：reason==missing_in_research_index 仅表示观察占位，不得提升?core，不得作为交易依?  - evidence.research_run_id：对?best_profile ?run_id；若涉及?profile/?window 的证据串联，用分号拼?
阶段二默认工作流（最小版）：
- 每日：A股日??CSV研究（二选一），但必须留证据（产物路?复现命令?- 每日观察（执行层占位）：?observe_YYYYMMDD.csv（触?未触?原因 + 关联 out_dir?- 每日小结（复盘钩子）：在 observe_YYYYMMDD.csv ?notes 追加 1 句今日异?待补证据/下一步；若无异常则写“无异常?- 每周：盘点→裁决→复盘（固定落盘：review\inventory_YYYYMMDD.md / data\ashare_watchlist\ruling_YYYYMMDD.json / review\gates_YYYYMMDD.md?```

摘录B｜阶段一“目?缓存/数据/产物”口径（摘要?
```
__pycache__：Python缓存；可删；不进Git
.dc_cache：数据下载缓存；可删但会重新下载；不进Git
data：输入数据入口（MT5导出/淘宝CSV/宏观与事件等? 可复现派生输入（如A股池子与聚合表）
backtest_out：研?回测/纸上执行产物；默认不进Git；仅朢终裁?部署表例?池子落盘约定（阶段二建议）：
- A股：data\ashare_watchlist\ 下的 screen/focus/core（可复现再生成，不强制进Git?- 外汇/期货：deploy_core/observe/exclude（参数仓库类产物，必要时进Git?```

摘录C｜阶段二当下“CSV通用对比”口径（摘要?
```
通用跑法：run_p0_sweep.ps1（归遍历 data\**\*_1h.csv?验收口径（先选一个）：A=net_pnl>0；B=回撤受控；C=跨窗口都稳；D=可用于池（过?60%?复盘只围绕口径：数据质量/默认profile/EXCLUDE与OBSERVE分层
```

## 1) 当前资产盘点（以仓库文件为准?
### 交易系统（四本书?
- Kaufman（状态模板主底座）：`00_交易系统书籍\03_交易系统与方法_Kaufman\Kaufman_STATE_TEMPLATE_V1_全书朢终版_36切片.md`
- 海龟（一页纸规则壳）：`00_交易系统书籍\04_海龟交易法则\海龟交易法则_STEP_C_朢终合并版_丢页纸规则?md`
- 墨菲（状态模板全书版）：`00_交易系统书籍\01_期货市场抢术分析_墨菲\墨菲_STATE_TEMPLATE_V1_全书朢终版_34切片.md`
- Van Tharp?4条术语锚点）：`00_交易系统书籍\02_通向财务自由之路_VanTharp\任务1_通向财务自由之路_14条锚点补?md`
  - 补齐方案（留档）：`00_交易系统书籍\02_通向财务自由之路_VanTharp\VT_4条NEED_EVIDENCE_补齐方案.md`

### 周期女王（已提取 md?
- 目录：`00_周期女王\`
  - 万法归一系统课程（优先）
  - 周期自然之力
  - 个股案例拆解
  - 临盘和复盘视?
### 数据层（用于后续“状态模板落地验证）

- 商品/指数 1H：`d:\Stock\trading_analysis\data\UKOIL_1h.csv`、`xtiusd_1h.csv`、`XCUUSD_1h.csv`、`GBRIDXGBP_1h.csv`
- 宏观与事件：`d:\Stock\trading_analysis\data\macro_1h_*.csv`、`econ_calendar_1h_flags_*.csv`、`vix_1d.csv`、`us_yield_2y10y_1d.csv`、`dollaridxusd_1h.csv`

---

## 2) 状结论（现在是否“完全整理好”）

### 已完成（可用?
- Kaufman：已完成，可作为“状态模?V1 文本底座”?- 海龟：已完成（一页纸规则壳可直接用）?- 墨菲：已完成全书版（34切片），中间批次/旧版本已归档?`01_期货市场抢术分析_墨菲\archive\`?
### 未完全闭环（仍需补证据）

- Van Tharp：已闭环（NEED_EVIDENCE 已清零）?
---

## 4) 周期女王：下丢步么做（建议流程?
目标：把“讲?逐字稿变成可落地的三件套：术语词?+ 状机 + 日常清单?
### 阶段1（只做万法归丢系统课程?
- 输入：`00_周期女王\01_万法归一系统课程\*.md`
- 输出（一次跑出来即可）：
  - INDEX：每个文件的主题与关键术?  - LEXICON：术语词典（每条必须 SOURCE_ANCHOR?  - STATE MACHINE：余?孕化/确认攻击/攻击有持?攻击无持?逢?的转移表
  - DAILY PLAYBOOK：日常执行清单（10-20条）

### 阶段2（扩展另外三类材料）

- 先扩展周期自然之力，再扩展案例拆解，朢后扩展临盘复盘?- 规则：只允许“补证据/补反?补失败模式，不要推翻阶段1的主骨架；如确需推翻必须给出 SOURCE_ANCHOR?
---

## 5) 新对话建议的工作方向（工程侧?
把文本模板落地到可证伪的验证流水线（避免写成玄学笔记）：

1) ?Kaufman/墨菲/海龟 的结?偏置/摩擦/风险/验真伪字段做丢个统丢的字段表（只列字段，不扩写内容）?2) 用现?1H 数据 + 宏观/事件标签，做 2-3 个最小可证伪棢验：
   - 趋势推进 vs 回归：在状切换点前后，波?成交/趋势持续性是否按模板预期变化
   - 摩擦 STRESS：在 VIX/事件窗口或成交异常时，假突破/回撤尾部是否显著变厚
3) 周期女王的状态机出来后，把它映射到同丢套状态字段，只做映射，不做预测?
---

## 6) 弢场给新对话的“固定口径?
- 不要把重要内容写?`d:\Stock\trading_analysis\其他ai的回?md`（该文件允许删除）?- 扢有最终可用结论必须落?`00_交易系统书籍\` / `00_周期女王\` ?`01_阶段丢_项目记录_过去与落?md`?- 任何条目如果?SOURCE_ANCHOR，一律标 NEED_EVIDENCE，不允许脑补?
---

## 7) 想法条目（可先放睢，不急着做）

### 7.1 题材库（半导体）与深度画像机制（想法，不是结论）

目标：用丢个可信池子减少全市场重扫成本；先从半导体/芯片板块弢始，逐步扩展?
仓库形（选型口径）：
- ?C 混合：报表为主（全量结构化可筛?可排?可日更），卡片为辅（只给少量标的做深度画像，长期保留?
深度画像的纳入与逢出（概念规则）：
- 纳入：当标的进入“池子里综合评分较高”（基本?抢术面+题材丢致更强）或属于阶段重点观察，就建?更新深度画像
- 扩容：随睢理解加深，把深度画像覆盖范围逐步增加（先 core/focus，再扩大?- 逢出：标的明确走坏（趋?基本?风险因子破位），再虑停止维护或移除深度画?- 适用范围：A股半导体可先做；外汇/期货中长周期交易的品种也适合做深度画?
瑞芯微大跌讨论的定位（本次先放着）：
- 目的不是证明“唯丢真相”，而是列出“下跌可能在哪里、下次么规避”的风险假设清单
- 当前证据不足时，允许保留猜想，但必须显式标注为想?假设”，避免当成结论

