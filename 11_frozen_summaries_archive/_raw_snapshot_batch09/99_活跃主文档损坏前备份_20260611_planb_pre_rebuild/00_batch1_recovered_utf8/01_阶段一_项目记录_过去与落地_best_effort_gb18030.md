# 阶段丢｜项目记录（过去/落地/不可落地?
更新时间?026-05-09

更新时间?026-05-11（补充：Ollama 在本项目中的核心定位与落地后协作模式”）

更新时间?026-05-14（L2 补空窗模块决议：v2 转正为用候；v1 降级?XAUUSD 白名单；已用真实数据复测并把“L2 单独记账 + 摩擦口径”落地）

更新时间?026-05-15（MT5 模拟实战闭环：历史扫信号 + 纸上成交回放；不用等丢周样本也能复现讨论）

更新时间?026-05-15（补充：Kimi ?73 个文?+ mq4 转译的全量复??重整“原子化落地清单（已?将做/待定/不做），并明确缺失维度的补齐路线?
更新时间?026-05-16（E2 chase 门控软开关落地：默认关闭；支?off/tag/block/drop；并完成三窗口裁决：E2_base 全窗口偏弱，E2c(chase<1.5) 为唯丢稳定正向桶）

更新时间?026-05-16（指标维度审计：确认缺失不止“量能，还包括波动率机制/状微观结?流动性时?会话效应”；补齐路线按先诊断标签→再门控→再仓位映射”推进）

更新时间?026-05-20（能力边界与下一步：黄金单标的优化定?+ 类股评人式辑分析模块规划 + 指数数据源缺口；并补?A 股情绪基硢设施：连板天梯与直播间数据接入）

更新时间?026-05-20（外部CSV数据源接入：淘宝CSV（UTC/EET）→ 统一落地 H1 ?全指?scan→replay→commentary 跑，替代“指数长窗依?MT5 demo”）

更新时间?026-05-21（entry_score 门控对照：同名产物文件用 out_dir 作为“文件夹前缀”区分；新增 score_gate 多窗口复现口径）

更新时间?026-06-01（P0 sweep 结果可外部复核：固化 OUTBOUND/INBOUND 粘贴规范；分层规则升级为 B_v2，避?observe 混入整体亏损标的；run_p0_sweep 产物新增 *_v2 决策/部署表；新增诊断标签落盘：diag_vol_state_* / diag_entry_vol_ratio_* / diag_session_*?
更新时间?026-06-03（P0 sweep 扩展诊断字段并验收：p0_sweep_summary.csv 新增 diag_vol_transition / diag_session_entry_vol_ratio（含?session 统计）；deploy 表新?diag_vol_state_gate；阶段二想法库完?C01 永久删除记录与指标生命周期分工合约）

更新时间?026-06-10（阶段二旧家族收缩闭环：`range_width` ?`trend_strength` 的最后一次局部片段验证已完成并冻结；临时粘贴区改回只用于“新问题 + 外部AI回复”，不再承载裁决?
更新时间?026-06-10（多AI 新一轮收缩收口：`EMA residual / sparse state / price pattern / A股专属量价` 已统丢裁决；用线继续收窄，A股真实量能相关字段转?future bucket?
更新时间?026-06-10（多AI 继续压缩 DIAG_POOL：`signal_quality / range core residual / KD extended / doji leftover` 已统丢裁决；仅?`ab_ema200_side_1h` ?`fib_retrace_depth_1h` 两类非执行观察标签）

更新时间?026-06-10（阶段切换小结：单字?单指标阶段在当前口径下已完成；后续正式转入稳定组合优?条件化应用阶段，不再继续无边界扩张单字段池）

更新时间?026-06-10（资料源总盘点与目录整理：补?`docs\资料源吸收状态与目录整理方案_20260610.md`；明确哪些目录已吸收、哪些仅是来源库/规则?工具资产，并完成小重复目录收口）

关联文件（阶段二有序推进的三份主文档）：
- 阶段二方向（未来/想法库）：`02_阶段二_工作方向_想法?md`
- 阶段二计划（当下/执行清单）：`03_阶段二_当下计划_执行清单.md`
- 临时粘贴区（只放新问?外部AI回复）：`临时粘贴区_外部AI与终端输?md`

## 关键节点小结?026-06-10?
- 单字段阶段结论：当前 FX/index/commodity 1H 口径下，扢有可量化单字?单指标都已完成独立讨论与收口，不再存在还没轮到讨论的?backlog?- 收口后的三类去向?  - 可继续推进的稳定候：进入 `UNIVERSAL_SHORTLIST_V1`
  - 只保留解?风险作用的标签：落在 `RISK_ONLY / RISK_CONTEXT_HINT / DIAG_ONLY`
  - 已证伪或不稳健的字段：落?`FROZEN_DIAG_ONLY`
- 明确后置?  - A 股真实量能依赖字??`A_SHARES_ONLY_FUTURE_BUCKET`
  - 仍不可量化的资料规则??`SOURCE_LIBRARY`
- 经验与心得：
  - 单字段研究最容易失控的点，不是跑不出结果”，而是“有丢点信息就丢直舍不得关；后面必须坚持“能冻结就冻结，能压成标签就不要继续占执行资源?  - 真正值得保留的，不是看起来解释很多的字段，是能同时经受住跨窗口跨品种、跨 `risk/regime` ?`MAE/max_dd` 口径的字?  - 阶段切换后，研究重心应从“找新单字段”改成把少数已保留字段在组合里用明白?
## 资料源盘点小结（2026-06-10?
- 新增总表：`docs\资料源吸收状态与目录整理方案_20260610.md`
- 本次澄清?  - “单字段阶段已完成不等于“所有资料目录都已文件完全吃透?  - 已完成的是当?`FX/index/commodity 1H` 口径下的可量化单字段闭环
  - 未完成但已归位的是：TK 外汇、大隐波浪周期女王GAS/神奇数字、谐?波浪等来源库内容
- 目录整理结论?  - `02_MT指标家族_源码与探针` 设为 MT 指标源码/探针标准入口
  - `02_mt指标测试` 判定为重复目录并清理
  - `98_MT历史数据_VTMarkets_Live2` 设为 MT4 历史归档标准入口
  - `12_ʱ_TOOLING_RUNTIME\VTMarkets-Live 2` 继续保留为兼容副本，暂不硬删

## 目录与缓存说明（阶段丢遗留资产的边界）

- `__pycache__\`：Python 自动生成的字节码缓存目录；可删除；不属于资产；不?Git?- `.dc_cache\`：数据下?聚合的本地缓存（包含 `.zst` ?`.bi5` 等）；可删除但会导致下次重新下载；不?Git?- `data\`：原生数据与外部数据入口（MT5导出/淘宝CSV/宏观与事件等）约定：只放“输入数?可复现输入，不放回测产物?- `backtest_out\`：所有研?回测/纸上执行的落盘产物约定：默认不进 Git；只有最终裁?部署参数仓库”例外（?`backtest_out\p1_final_validate3\deploy_*.csv`）?
数据整理规则（建议口径，便于阶段二有序推进）?- `data\`（输入数据）按交易类?品种/周期”组织；示例?  - `data\fx\1h\EURUSD_1h.csv`
  - `data\commodities\1h\XAUUSD_1h.csv`
  - `data\index\1h\NAS100_1h.csv`
  - `data\macro\1d\vix_1d.csv`
  - `data\events\econ_calendar_1h_flags_*.csv`
- `backtest_out\`（生成产物）按实验名/out_dir”组织；保留原则?  - 必保留（可追溯决策）：`deploy_*.csv`、`*_decision_table.csv`、以及关键汇总表
  - 其余默认可删（可复现再生成）：笔回放、长日志、临时对照批?
根目录脚本（入口性质，暂不搬家）?- `run_p0_sweep.ps1`：归遍历 `data\**\*_1h.csv`（排?`data\ashare_watchlist\`）的批量对比回测入口；输?`p0_sweep_summary.csv` + `*_v2` 决策/部署表（用于“用指标是否有用”的横向对比?- `run_ab_baseline.ps1`：A/B 基线对照入口（用于工程增?vs 严格文档口径”的差异核验?- `mt5_daily_ops.ps1`：MT5 日活与对账工具入口（status/plan/summary 等；默认以安全为先）

根目?Python 入口（入口质，暂不搬家）?- `mt5_exit_assistant.py`：MT5 观察/执行、CSV scan→replay→commentary 的统丢入口
- `mt5_export_1h.py`：从 MT5 导出 1H 数据?`data\` 或走 TwelveData
- `backtest_p0.py`：P0 基线回测与指标计算入?- `ashare_preprocess.py`：A股天梯→screen→focus→core 与直播间 OCR 聚合入口
- `generate_p0_subset.py`：生?P0 子集/规则表的辅助脚本

阶段丢资产箢表（只列你后面会复用的入口）?- 目录拆分：`00_周期女王` / `00_指标定义&公式` / `00_交易系统书籍` / `00_大隐体系`
- 周期女王规则壳入口：`00_周期女王\99_可用规则壳\`
- 四本书稳定入口：`00_交易系统书籍\99_流程模板\三本书_STEP_C_滚动合并与锚点补?md`
- A股日更脚本入口：`ashare_preprocess.py`（天梯→screen→focus→core；直播间 OCR：`blogroom_*`?- 抢术面指标源码：`00_指标定义&公式\*.mq4`

## 已完成（关键落地?
### 工程与路?- 项目根目录统丢?`d:\Stock\trading_analysis`，并修复回测脚本中残留的旧路径硬编码?
### GitHub（版本留痕：以后?Git 当保存键”）
- 仓库地址：https://github.com/er-geng-fan-tang/trading-analysis.git （分支：main?- 基本原则?  - 任何“策?执行/参数仓库（deploy_*.csv?日活口径/审计口径”的变更，都必须先落到本地文件，再用 Git 形成丢次提交（commit），朢?push ?GitHub?  - `backtest_out` 里大部分是跑出来的产物（默认忽略）；只有 `backtest_out\p1_final_validate3\deploy_*.csv` 这类“部署池/参数仓库”才进入版本管理?
#### 工作方式（本地留历史为主，GitHub 只做可备份）

- 日常目标：只?Git 在本地记录变动历史；不强?push。GitHub 当可选异地备?同步”?- 日常朢小流程（只写本地历史，不上网）：

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
git status -sb
git add -A
git commit -m "今天做了仢?
```

- 霢要同?备份时再 push（可选）?  - 换电?重装系统前做丢?  - 做到丢个里程碑”想固化到云?  - 霢要另丢台机器拉同一份代?
```powershell
git push
```

- 弢工前如果你确实要跟远端同步（可）?
```powershell
git pull
```

#### 保姆教程（最小可用版?
1) 第一次（只做丢次）
- 安装 Git（Windows）：建议?Git for Windows，并确保能在 PowerShell 里运?`git -v`
- 设置提交身份（只影响提交里显示的名字/邮箱）：

```powershell
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

- 登录/鉴权（只做一次）：第丢?`git push` 通常会弹出浏览器登录 GitHub（Git Credential Manager）；按提示登录即可若你用的是 Token/密码管理器，?GitHub 提示操作?- 克隆仓库到本地（推荐新目录；如果你已?`d:\Stock\trading_analysis` 工作，可跳过 clone）：

```powershell
git clone https://github.com/er-geng-fan-tang/trading-analysis.git 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
```

2) 每天用法（你只要记住?6 条）
- 看当前改了什么：

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
git status -sb
```

- 把改动加入暂存区”（准备提交）：

```powershell
git add -A
```

- 提交丢次（给这次改动起名字；一句话说明即可）：

```powershell
git commit -m "xxx（例如：mt5 执行口径/部署池更新）"
```

- 推到 GitHub（相当于“云端保存）?
```powershell
git push
```

- 弢工前先同步别?另一台机器的改动?
```powershell
git pull
```

- 快看历史提交（只看最?10 条）?
```powershell
git log --oneline -n 10
```

3) 误操作救命（朢常用 3 个）
- 还没 commit，想把某个文件改回去?
```powershell
git restore -- path\to\file
```

- 已经 commit 了，但想撤销“上丢条提交（保留文件改动在本地，方便继续改）?
```powershell
git reset --soft HEAD~1
```

- 已经 commit 了，但想彻底回到上一条提交（危险：会丢本地改动）?
```powershell
git reset --hard HEAD~1
```

#### 附录A：P0规则子表（自动生?v0.1｜原文内嵌）

# P0规则子表（自动生?v0.1?
- 来源：d:\Stock\trading_analysis\02_原子化拆解文件\原子规则?md
- 目标：用于豆包P0审计（冲?边界/优先级裁决），不是最终策略全?- 主题：EMA144宏观分界/极限风控?+ EMA结构(13/21/55) + 多周期KD确认(接口) + 仓位硬约?+ 参数冲突样本

## P0 入场触发模块?H，可执行草案 v0.3?- 周期锁：本模块仅允许?1H 上计算与输出入场信号；D1/4H仅用于Regime/Confirm计算，不得输出入场触发（F004?- 信号判定时点：统丢?1H K线收盘后按收盘价判定；父周期指标仅使用已收盘的最后一根D1/4H值（避免盘中漂移）（K003/K020?- 适用前置（强制三重门控）（F003）：
  - Regime合规：使用上丢根已收盘4H值：Close_4H ?EMA144_4H 同侧；若 Close_4H == EMA144_4H 视为不合规（禁止弢仓）（K011?  - Confirm合规：EMA13_4H / EMA21_4H / EMA55_4H 结构与交易方向一致（例如多头排列：EMA13_4H>EMA21_4H>EMA55_4H；空头对称）
  - KD同向：KDAlign(D1,4H)=同向（见下方KDAlign朢小定义）（K009?  - 否决链路：Regime/Confirm/KDAlign 任一不合规，?E1/E2 全部禁止触发
- 信号互斥（P0强制）（豆包复审R001）：同一?H K线若 E1 ?E2 同时触发，仅允许触发 1 个信号，且优先级固定 E1 > E2；同丢?H K线最多产生一个入场信?- 持仓约束（P0默认）：同一标的同时仅允许持有一笔同向仓位；不做对冲/反向同时持仓（可后续P1再讨论）（K010?- 波动率基准：ATR = ATR(1H,14)
- 参数候池（用于P1回测裁参；P0固定默认值）（F005/F006/F008）：
  - k ?{0.20, 0.25, 0.33}，P0默认 k=0.25
  - N ?{20}（P1可扩展?{14,20,34}?  - M ?{3}（P1可扩展?{2,3,5}?  - 回溯窗口 X ?{5}（P1可扩展?{3,5,8}?  - 实体过滤系数 body_k ?{0.5}（P1可扩展?{0.4,0.5,0.6}?  - 触碰朢小穿透系?touch_k ?{0.2}（用于过滤EMA毛刺触碰?  - 影线系数 shadow_k ?{0.3}（P1可扩展?{0.2,0.3,0.4}?  - 止损系数 stop_k ?{1.5}（P1可扩展?{1.0,1.5,2.0}?
### KDAlign朢小定义（P0可执行，P1可替换参数）
- KD默认参数（P0暂定）：KDJ(9,3,3)；P1允许按波动率分桶裁参并替换该默认?- 多头同向：D1?H同时满足 K>D
- 空头同向：D1?H同时满足 K<D
- 中?不合规：任一周期出现 K==D 视为不合规（不允许入场触发）；或 D1 ?4H 丢多一空视为矛盾（不允许入场触发）

### 规则E1：B1 结构突破 + 回踩确认（Breakout-Retest?- 参数：N=20，M=3，容差带=±k*ATR
- 突破位定义（消除自引用）（F001）：
  - BreakoutLevelLong = REF(HHV(High_1H, N), 1)
  - BreakoutLevelShort = REF(LLV(Low_1H, N), 1)
- 回踩窗口计数口径：M 从突破完成的下一?H K线开始计数（K004?- Retest判定：触及与确认可以发生在不同K线，但二者都必须位于同一个M窗口内（K004?- 做多触发?  - Breakout：Close_1H > BreakoutLevelLong
  - Touch：在M窗口内存在一根K线满?Low_1H ?BreakoutLevelLong + k*ATR ?High_1H ?BreakoutLevelLong - k*ATR（闭区间触及?  - Confirm：在M窗口内存在一根K线满?Close_1H ?BreakoutLevelLong
- 做空触发?  - Breakout：Close_1H < BreakoutLevelShort
  - Touch：在M窗口内存在一根K线满?Low_1H ?BreakoutLevelShort + k*ATR ?High_1H ?BreakoutLevelShort - k*ATR（闭区间触及?  - Confirm：在M窗口内存在一根K线满?Close_1H ?BreakoutLevelShort

### 规则E2：A1 EMA21 回踩-收复（Pullback Reclaim?- 状锁（避免无回调误触发）（F002）：
  - 回溯窗口：X?H?  - 多头触碰事件：在“触发K线之前的近X根内存在 Low_1H ?EMA21(1H) - touch_k*ATR（不含触发K线，禁止同K线触?收复）（K017?  - 空头触碰事件：在“触发K线之前的近X根内存在 High_1H ?EMA21(1H) + touch_k*ATR（不含触发K线，禁止同K线触?跌回）（K017?- 做多触发：存在触碰事件后，且触发K线位于该触碰事件之后的X根窗口内，出现收复K线：Close_1H > EMA21(1H) ?Close>Open（K005?- 做空触发：存在触碰事件后，且触发K线位于该触碰事件之后的X根窗口内，出现跌回K线：Close_1H < EMA21(1H) ?Close<Open（K005?- 过滤（降低噪声）（F006）：触发K线实体长?|Close-Open| ?body_k*ATR
- 影线穿约束（降低假收复）（F009）：
  - 多头：触发K?Low_1H ?EMA21(1H) - shadow_k*ATR
  - 空头：触发K?High_1H ?EMA21(1H) + shadow_k*ATR

## 外汇/股票扩展分析接口（P1/工程增强：仅观测或过滤，不得覆盖P0三重门控?- 原则：任何外部数据（情绪/资金?新闻/挂单/事件）只允许作为“P1过滤/风险提示/仓位上限”使用，不得替代或绕?P0 ?Regime/Confirm/KDAlign，也不得触发入场（触发仍必须来自 1H ?E1/E2）?- 目标：把“需要外汇与权益类分析吗”拆成可落地的数据字段，后续可直接接?backtest_p0 / mt5_exit_assistant 的输入口径中（但默认关闭）?
### 外汇（FX）分析字段（建议优先级：事件 > 情绪 > 挂单?| 字段 | 频率 | 口径 | 用（允许动作?|
|---|---|---|---|
| fx_event_risk_24h | 事件驱动 | 未来24h内是否存在红色高影响事件（按交易标的相关货币?| 仅过滤新弢?降低仓位上限（不得反向开仓） |
| fx_positioning_bias | 日更 | 零售多空持仓差（long% - short%）或分位?| 仅风险提?仓位上限；不做方向开仓依?|
| fx_order_cluster_score | 日更/小时 | 挂单密集?止损密集区对当前价的压制/支撑强度评分 | 仅用于止?止盈候位辅助，不得触发入?|

### 权益类（A?美股）分析字段（建议优先级：事件 > 流动?> 题材强度?| 字段 | 频率 | 口径 | 用（允许动作?|
|---|---|---|---|
| eq_event_risk | 事件驱动 | 业绩/公告/监管/财报?重大政策等事件风险分?| 仅过滤新弢?降低仓位上限 |
| eq_liquidity_score | 日更/盘中 | 流动性评分（成交?换手/价差等） | 仅过滤（低流动禁入） |
| eq_theme_strength | 日更/盘中 | 题材/板块强度分数或排?| 仅用于标的池排序/权重”，不作为入场触?|

## v0.2 收敛口径（采用最终复审裁决清单的推荐/指定项）
- 周期口径：P0仅允?D1 / 4H / 1H；所有非标周期规则保留为P1观测项（无任何交易触发权限）（F001?- EMA口径：P0固定 EMA=13/21/55/144?44EMA为Regime与极限风控线；非标EMA/HRY33等仅可作辅助参（不得拥有门控/止损否决权）；非标乘数统丢替换为标准乘数（F002?- 趋势架构：Regime=144EMA（一级否决权）；Confirm=EMA结构(13/21/55)+多周期KD同向（KD仅输出同?矛盾接口）；其他趋势判定仅作辅助参（F004/F010?- 逆势试仓：P0严格禁止?44EMA方向弢仓；R002移出P0执行库（F007?
## v0.2 关键阈字段（可执行最小版，优先用于风控闭环）
- 回撤25%（以初始本金为基准，日度统计）：
  - 本金基准：以启动时静态初始本金为基准；若发生出入金需手动重置该基?  - 回撤公式：drawdown = (InitialEquity - CurrentEquity) / InitialEquity
  - 统计时点：每日北京时?00:00 快照统计
  - 触发动作：立即停止所有新弢仓；对存量持仓执行砍不健康→降曝至目标风险暴露的顺序处置
  - 目标风险暴露（P0朢小定义）：将全账户风险暴露降至不高于30%，且禁止加仓
- 初始止损（P0朢小可执行定义）（K008）：
  - 多头：InitialStop = EntryPrice - stop_k*ATR
  - 空头：InitialStop = EntryPrice + stop_k*ATR
- 不健康持仓（P0中推荐）?  - Confirm反向持续 confirm_n=2?H周期）（K006/K014?  - 初始止损触发：以收盘价跌?突破 InitialStop 判定，且霢 stop_hold_bars=3 ?1H K线内未收?  - 砍仓顺序：极限止损持仓（跌破/突破144EMA风控线）?Regime+Confirm反向持仓 ?浮亏降曝持仓（梯度减仓）（F003?- Neutral（P0中推荐）：禁止新弢?禁止任何加仓；现有持仓挂载保本动态止损（以ATR为基准）；保留不超过30%底仓（F005?- 止损绑定周期（P0中推荐）：止损判定统丢绑定1H；单指标反向信号仅减?0%；D1+4H共振反向才全额清仓（F006?
## v0.2 RuleID处置表（执行权限回填?- P0执行（可触发交易动作）：R001、R007、R050、R051
- P0执行（仅持仓管理/减仓，不得作为开仓依据）：R004
- P0执行但需标准化系?口径后再用：R052?.142?.0?- P0仅观测（辅助参，无门?否决/强制出场权限）：R029、R030、R066
- 移入P1观测/回测（非标周?形主?非标KD参数/画像模糊霢参数化）：R003、R006、R008、R009、R010、R011、R012、R013、R014、R015、R016、R017、R018、R019、R020、R021、R022、R023、R024、R025、R026、R027、R028、R031、R034、R035、R036、R042、R043、R044、R045、R046、R047、R048、R053、R054、R055、R056、R057、R058、R059、R060、R061、R062、R063、R064、R065、R067、R068、R069
- 作废：R002（势试仓，P0严格禁用）R039与R070（重复归口持仓管理）（F007?
## 统计

| 维度 | 计数 |
|---|---:|
| 来源?GAS核心母版 | 20 |
| 来源?其他 | 10 |
| 来源?大隐 | 28 |
| 来源?量化分析体系V1.1 | 12 |
| 类别:仓位 | 13 |
| 类别:入场 | 3 |
| 类别:出场 | 21 |
| 类别:趋势 | 10 |
| 类别:过滤 | 18 |
| 类别:风控 | 5 |

## 豆包复审提示词（思模式，复制到豆包第丢条）

你是“交易量化规则审计官（复审）”，请用严谨推理而不是长文?必须遵守口径：P0仅D1/4H/1H；EMA=13/21/55/144；Regime=144EMA；Confirm=EMA结构(13/21/55)+多周期KD同向（KD仅接口，不在P0硬裁参数）；朢大回撤红?5%（初始本金基准，日度统计）；低频重仓?任务：对【P0规则子表(含RuleID) + v0.2收敛口径与阈值字段做复审：冲?边界/优先?缺失定义，并棢查RuleID处置表是否自洽?输出：只允许输出《复审裁决清单表格：
IssueID｜严重?P0/P1/P2)｜涉及模?RuleID｜问题类型｜问题描述｜裁?可执?｜需要补充阈?数据｜回填到配置的改动点(把X改为Y)

#### 附录B：原子化落地清单（已?/ 将做 / 不做｜原文内嵌）

原子化落地清单（已做 / 将做 / 不做?更新时间?026-05-15

丢、当前用主干”已经落地的原子（能跑能复现、能落盘?1) 多周期方向与确认（D1 + H4 + H1?   - 作用：大周期定方向，小周期找触发（大引小?   - 代码：mt5_exit_assistant.py + backtest_p0.py（compute_trend_flags?   - 输出：GateSnapshot / entries_suggested_v2.csv / paper_replay_trades.csv

2) EMA 系（结构/方向尺子?   - 作用：用均线结构判断顺势、并作为“距离原子的参照
   - 已用字段：ema21_1h（以?4H ?EMA 组）

3) ATR 尺度化（统一尺子?   - 作用：止损触发距离追单距离R 倍数全部?ATR 标准化，跨品种可?   - 已用字段：atr、r0、TP1/TP2（R）chase_dist_atr（abs(entry-ema21_1h)/atr?
4) 突破-回测-确认（触发状态机?   - 作用：把“方向正确变成可执行触发点?   - 体现：E1/E2 ?break/retest/touch/confirm 逻辑（状态机扫描?
5) 震荡指标（KD / 随机指标的一部分?   - 作用：作为多周期共振门控的一部分（不是装饰）
   - 已用字段：kd_long/kd_short + kd_k_4h/kd_d_4h + kd_k_1d/kd_d_1d
   - 说明：你“大隐指标组5-50-95”的那套参数与多周期结构，还没完全复刻；目前用的是项?Params 里的 kdj 参数?
6) 风控红线（DD 25% 停机?   - 作用：不让系统在不利阶段持续加仓/弢?   - 体现：HALTED 后禁止新弢?
7) L2 补空窗（L2_TIME_GAPFILL?   - 作用：降低连续空窗（节奏问题?   - 状：独立运行，不依赖 E1/E2 的成?
二已落地为诊断工具的原子（不直接交易，但用于判断是否该进入主干）
1) E2 追单距离门控（E2c?   - 定义：chase_dist_atr = abs(entry - ema21_1h) / atr
   - 发现：E2 的亏损主力来?chase_dist_atr >= 1.5 的追单毒桶?   - 三窗口一致：E2c(<1.5) 从系统亏损拉到接近打?转正，但仍只做纸上监控，不实盘执?   - 工具化：paper-replay 支持 --paper-e2-chase-max 1.5 自动输出 E2_base/E2c/E1+E2c 汇?
2) bar_rule 口径显式化（sl_first/tp_first?   - 作用：把“同根K线先打SL还是先打TP”的隐含假设显式化，避免讨论跑偏
   - 结论：属于二阶影响，主矛盾不在这?
三正在推?/ 将做（按“先通用、先可解释先低风险排序）
1) W1（周线）补进门控快照（形成真正的“三线顺?顺下”视角）
   - 目标：在 gate snapshot 输出里同时看到周?KD 同向情况，以及三线同向的结果

2) “信号棒质量/趋势?十字星等 ALBrooks 可量化字段（先诊断，后门控）
   - 目标：回?E1 的亏损样本是否集中在“低质量K线形态?
3) 2B 顶底 ?衰竭?23（先变诊断标签，不直接进执行?   - 目标：先把结构识别拆成可计算的摆动点/幅度?回收确认，再?paper-replay 做跨窗口验证

四暂不做 / 目前不合做（原因：不可复现过强主观或霢要更重的数据?1) 纯主观波浪计数（没有固定口径就无法复跑）
2) 霢?tick 级别才能严谨还原的同根先后顺?滑点细节”（目前?sl_first/tp_first 两口径夹逼）
3) 仅靠视频讲解才能落地、但无法给出可计算规则的内容（除非你给出口径?阈表?
五当前交易执行口径（丢句话版，避免打转?- E1：主干允许执行（顺势+确认更严格）
- E2：不执行只记录；E2c(chase_dist_atr<1.5) 只做纸上监控
- L2：补空窗独立运行

### P0 风控红线（停机线?- 在实盘执行侧与回测侧保持丢致：朢大回撤达?25% 后进入停机状态（禁止新开仓，仅允许减?出场/风控处理），并在运行输出中可见?
### 回测与部署口径收敛（CORE / DROP?- 回测侧形成按品种的参数预设（CORE_PRESET_V1）与 DROP 清单，并提供导出部署?CSV 的能力：
  - `backtest_out\p1_final_validate3\deploy_core.csv`
  - `backtest_out\p1_final_validate3\deploy_observe.csv`
  - `backtest_out\p1_final_validate3\deploy_exclude.csv`
- 当前 CORE（以 `deploy_core.csv` 为准）：`XAU, GBPJPY`（外汇阶?只放 GBPJPY；E2 不执行）
- 当前 OBSERVE（以 `deploy_observe.csv` 为准）：`NAS100`（以?FX 画像候仍留痕，不进入阶段1执行?- 当前 EXCLUDE（以 `deploy_exclude.csv` 为准）：?3 年窗画像表为准（?`backtest_out\fx_profile_reco_3y_20260521.csv`?- 说明：部署池 CSV 同时作为“参数仓库复用：允许为单标的记录已验证的朢优参数（例如 gold_only ?chase 阈Bobby 止损倍数、禁用项），用于长期持久化与迭代对照?
### MT5 数据源裁决（历史可用性）
- 背景：同?symbol 在不同服务器数据深度差异巨大，必须先验收“历?bars 密度”再跑长窗回测?- 验收命令：`.\.venv\Scripts\python.exe .\mt5_exit_assistant.py --mt5-history-check --mt5-history-from 2012-01-01 --mt5-history-to 2013-01-01 --mt5-history-tf H1 --mt5-history-symbols US500,US30,NAS100,GER40,UK100,XAUUSD,XAGUSD,EURUSD`
- 当前结论（以抽查输出为准）：
  - 外汇主数据源：ICMarketsSC-Demo?012 ?EURUSD ?6000+ bars，断档少?  - 金属主数据源：Deriv-Demo?012 ?XAU/XAG ?6000+ bars），备?ForexTimeFXTM-Demo02（XAU/XAG ?5600+ bars?  - 指数数据源：MT5 demo 长窗仍缺（已验证多家?2012 年仅 1~300 bars 或不可用）；已改走外?CSV 数据源做长窗研究与回?
### 外部 CSV 数据源（淘宝CSV）裁决与接入（用于长窗研?回测?- 原则：长窗研究不再依?MT5 demo 的历史深度；MT5 仅用于实?模拟盘执行链路?- 数据落盘位置（原始文件夹）：
  - `data\XAUUSD CSV\XAUUSD CSV\`（含 M1/5m/15m/30m/1H/4H/D/W/M，Time (UTC)?  - `data\USA500IDXUSD_1 Min_Bid_2015.04.21_2026.04.27\`（US500，Time (UTC)?  - `data\USATECHIDXUSD_1 Min_Bid_2015.04.21_2026.04.27\`（NAS100，Time (UTC)?  - `data\USA30IDXUSD_1 Min_Bid_2013.09.30_2026.03.01\`（US30，Time (UTC)?  - `data\DEUIDXEUR_1 Min_Bid_2013.09.30_2026.03.15\`（GER30/德指代理，Time (EET)，需做时区转换含夏令时）
- 统一口径（内部使用）：全部转换到 UTC ?H1 并输出到 `data\*_1h.csv` 后再进入回测/扫描（避免跨品种对齐漂移）?- 已落成的 H1 标准文件（UTC，字?date,time,open,high,low,close,volume）：
  - `data\xauusd_1h.csv`
  - `data\us500_1h.csv`
  - `data\nas100_1h.csv`
  - `data\us30_1h.csv`
  - `data\ger30_1h.csv`

### 全指标链路（CSV）：scan ?replay ?commentary（只读，不触发交易）
- scan（输出全部诊断字段：SR + jg_* + pat_* + 风控标签，落?`entries_suggested_v7.csv`）：
  - `.\.venv\Scripts\python.exe .\mt5_exit_assistant.py --paper-scan-csv --csv-dir .\data --paper-from 2016-05-01 --paper-to 2026-03-01 --paper-symbols XAUUSD,US500,NAS100,US30,GER30 --paper-bobby-signals 1 --paper-bobby-sl-atr 1.5 --log-dir .\backtest_out\paper_csv_all`
- replay（把 signals 回放成笔 outcome + 汇，落盘 `paper_replay_trades.csv / paper_replay_summary.csv`）：
  - `.\.venv\Scripts\python.exe .\mt5_exit_assistant.py --paper-replay-csv --paper-dir .\backtest_out\paper_csv_all\2026-03-01 --csv-dir .\data --paper-lookahead-bars 48 --paper-tp1-r 1 --paper-tp2-r 2 --paper-bar-rule sl_first --paper-e2-chase-max 1.5 --paper-e1-diagnose 1`
- commentary（类股评人式只读输出，面向讨论）?  - `.\.venv\Scripts\python.exe .\mt5_exit_assistant.py --paper-commentary --paper-dir .\backtest_out\paper_csv_all\2026-03-01 --commentary-symbol XAUUSD --commentary-topk 8 --commentary-min-n 20`
- 本次长窗结论（口径：2016-05-01?026-03-01?品种，lookahead=48，TP1=1R/TP2=2R，sl_first）：
  - TOTAL：n=6269，avg_r=-0.1635
  - E2 门控裁决（chase_dist_atr < 1.5）：E2_base n=2693 avg_r=-0.2926；E2c n=494 avg_r=+0.0729；E1+E2c n=3903 avg_r=-0.0351

### entry_score 门控对照（scan 阶段，可复现?- 目标：把“后验筛?entry_score<阈变?scan 阶段可控门控，且默认不改变历史口径（不传?off）?- 参数（mt5_exit_assistant.py）：
  - `--entry-score-max 4.5`
  - `--entry-score-action off|tag|block|drop`（做回放对照时用 drop；做“执行侧跳过”时?block?  - `--entry-score-scope all|e2`（all=对所有信号生效；e2=仅对 E2 生效?  - （可选：按波动阶段动态阈值）`--entry-score-vol-mode atr_rel_bins --entry-score-vol-cuts cut1,cut2 --entry-score-vol-maxes max_low,max_mid,max_high`
- 同名文件的区分规则：扢有产物都?`entries_suggested_v7.csv / paper_replay_trades.csv / paper_replay_summary.csv`，必须用 out_dir 作为“文件夹前缀”区分?  - 例：`backtest_out\paper_csv_vol_drop_score_all\2026-03-01\paper_replay_summary.csv`
  - 外发给其?AI 时的命名建议：`paper_csv_vol_drop_score_all__paper_replay_summary.csv`（只改文件名，不改目录结构）
- 固定口径（CSV 长窗?016-05-01?026-03-01）对照目录：
  - baseline：`backtest_out\paper_csv_all\2026-03-01\paper_replay_summary.csv`
  - vol_drop（高量能风险直接丢弃）：`backtest_out\paper_csv_vol_drop\2026-03-01\paper_replay_summary.csv`
  - vol_drop + score_gate(all)：`backtest_out\paper_csv_vol_drop_score_all\2026-03-01\paper_replay_summary.csv`
  - vol_drop + score_gate(e2)：`backtest_out\paper_csv_vol_drop_score_e2\2026-03-01\paper_replay_summary.csv`
- 复现命令（CSV 长窗，vol_drop + score_gate(all)）：
  - scan?    - `.\.venv\Scripts\python.exe .\mt5_exit_assistant.py --paper-scan-csv --csv-dir .\data --paper-from 2016-05-01 --paper-to 2026-03-01 --paper-symbols XAUUSD,US500,NAS100,US30,GER30 --paper-bobby-signals 1 --paper-bobby-sl-atr 1.5 --vol-ratio-max 2.0 --vol-pct-max 90 --vol-risk-action drop --entry-score-max 4.5 --entry-score-action drop --entry-score-scope all --log-dir .\backtest_out\paper_csv_vol_drop_score_all`
  - replay?    - `.\.venv\Scripts\python.exe .\mt5_exit_assistant.py --paper-replay-csv --paper-dir .\backtest_out\paper_csv_vol_drop_score_all\2026-03-01 --csv-dir .\data --paper-lookahead-bars 48 --paper-tp1-r 1 --paper-tp2-r 2 --paper-bar-rule sl_first --paper-e2-chase-max 1.5 --paper-e1-diagnose 1`
- 三窗口稳定复现（同口径：CSV，vol_drop + score_gate(all)；只?paper-from/paper-to ?log-dir）：
  - 2023-2024：`backtest_out\score_gate_2324\2024-12-31\paper_replay_summary.csv`
  - 2025：`backtest_out\score_gate_2025\2025-12-31\paper_replay_summary.csv`
  - 2026YTD：`backtest_out\score_gate_2026ytd\2026-03-01\paper_replay_summary.csv`
 - 黄金（XAUUSD）波动阶段→阈快速校准证据（基于 `paper_csv_vol_drop\2026-03-01\paper_replay_trades.csv`，桶=E1+E2c<1.5，atr_rel=ATR/price 三分位）?   - 产物：`backtest_out\xau_score_threshold_by_atrbin_20260521.csv`（不?atr_bin 下，entry_score_max 网格?n/avg_r 对照? - 黄金（XAUUSD）动态阈?v2（先稳后赚，作为当前默认候；仍保持开关默?off）：
   - 参数：`--entry-score-vol-mode atr_rel_bins --entry-score-vol-cuts 0.0019,0.0027 --entry-score-vol-maxes 4.6,4.6,5.0`
   - 长窗?016-05-01?026-03-01）：`backtest_out\xau_dyn_score_v2_full\2026-03-01\paper_replay_summary.csv`
     - `__TOTAL__ E1+E2c<1.5 n=230 avg_r=0.100000`
   - 窗口1?023-2024）：`backtest_out\xau_dyn_score_v2_2324\2024-12-31\paper_replay_summary.csv`
     - `__TOTAL__ E1+E2c<1.5 n=44 avg_r=0.295455`
   - 窗口2?025）：`backtest_out\xau_dyn_score_v2_2025\2025-12-31\paper_replay_summary.csv`
     - `__TOTAL__ E1+E2c<1.5 n=30 avg_r=0.200000`
- 窗口3（近两年?024-01-01→最新可?1H）：XAUUSD 目前 CSV 朢新到 2026-05-20 04:00Z（含 MT5 追加段），用该窗口作为更稳的近两年验证窗”：
  - `backtest_out\xau_dyn_score_v2_24toLatest\2026-05-20\paper_replay_summary.csv`
  - `__TOTAL__ E1+E2c<1.5 n=58 avg_r=0.206897`
 - 朢终裁决（黄金先封口）：以近两年窗为准，确认将 v2 作为黄金默认参数（仅 gold_only 画像包默认；通用主干保持默认 off，避免影响其它品种）?   - 对照（同窗同回放口径）：
     - vol_drop（无 entry_score 门控）：`backtest_out\xau_24toLatest_vol_drop\2026-05-20\paper_replay_summary.csv` ?`E1+E2c<1.5 n=175 avg_r=0.102857`
     - vol_drop + 静?entry_score_max=4.5（all/drop）：`backtest_out\xau_24toLatest_vol_drop_score45\2026-05-20\paper_replay_summary.csv` ?`E1+E2c<1.5 n=28 avg_r=0.000000`
     - v2（动态阈值，按波动档位）：`backtest_out\xau_dyn_score_v2_24toLatest\2026-05-20\paper_replay_summary.csv` ?`E1+E2c<1.5 n=58 avg_r=0.206897`

- 外汇（FX）近两年窗（2024-01-01→最新可?1H）补齐与分层（先补齐再跑；按品种给出画像建议）：
  - 当前 FX 1H 覆盖（data\*_1h.csv）：9 个（majors：EURUSD/GBPUSD/USDJPY/USDCAD/AUDUSD/NZDUSD/USDCHF；cross：EURJPY/GBPJPY?  - ?MT5 补齐后共同最新：`2026-05-19 11:00Z`（作?FX 统一 paper-to?  - 证据目录：`backtest_out\fx_24toLatest_vol_drop_mt5patch\2026-05-19\paper_replay_summary.csv`
    - `__TOTAL__ E1+E2c<1.5 n=1490 avg_r=0.002013`（用参数?FX 近两年整体接?0 ?必须按品?阶段做画像参数表?  - 品种分层建议（写入部署池 CSV，作为参数仓库先落盘，不默认进入 CORE）：
    - OBSERVE：`backtest_out\p1_final_validate3\deploy_observe.csv`（GBPJPY/GBPUSD/AUDUSD/EURUSD/EURJPY?    - EXCLUDE：`backtest_out\p1_final_validate3\deploy_exclude.csv`（NZDUSD/USDJPY/USDCHF/USDCAD?  - 扩展（用户用 MT5 导出补齐的交叉盘/日元系）：新?10 ?FX 对（EURGBP/EURCHF/GBPCHF/EURAUD/EURNZD/AUDJPY/CADJPY/CHFJPY/NZDJPY/AUDNZD），统一使用共同朢?`2026-05-19 00:00Z` 跑近两年窗：
    - 证据目录：`backtest_out\fx_19pairs_24toLatest_vol_drop\2026-05-19\paper_replay_summary.csv`
      - `__TOTAL__ E1+E2c<1.5 n=2773 avg_r=-0.014064`（用参数在扩?FX 宇宙上仍偏弱 ?继续按品种画像）
    - 画像总表（每品种 n/avg_r/tier/建议）：`backtest_out\fx_profile_reco_20260521.csv`
  - 近三年窗?023-01-01→共同最新）：AUDJPY/CADJPY/AUDNZD ?Deriv-Demo 可补齐到 2023 起，因此 FX 19 对可统一跑近三年验证窗：
    - 证据目录：`backtest_out\fx_19pairs_23toLatest_vol_drop\2026-05-19\paper_replay_summary.csv`
      - `__TOTAL__ E1+E2c<1.5 n=3906 avg_r=-0.040451`
    - 画像总表?年窗）：`backtest_out\fx_profile_reco_3y_20260521.csv`
  - 朢终裁决（FX 先不封口，但给出“默认画像建议以便后续执行侧落地）：
    - 结论：用参数?FX 全体上仍为负?年窗），因此必须分品种当前只?GBPJPY ?3 年窗达到“可作为 CORE 候的稳定正期望?    - 默认画像建议（v1）：FX 执行侧默认启?E2 追价距离门控（e2_chase_max_atr=1.0，action=block），并优先只交易 E1；E2 仅作为观察信号（或在严格 e2c<1.0 时才考虑）?    - 关键对照证据（CORE 候?4 对）：`backtest_out\fx_core4_3y_base_e2c1p5\2026-05-19\paper_replay_summary.csv`
      - E2c<1.5：`__TOTAL__ E1+E2c<1.5 n=874 avg_r=0.088101`
      - E2c<1.0：同目录 replay ?`--paper-e2-chase-max 1.0` ?`__TOTAL__ E1+E2c<1 n=774 avg_r=0.102067`

### 2026-05-24｜试错节点：通用“慢变量状模板v0（state4 × E1/E2?
- CheckpointID：`CP_STATE4_V0_20260524`（如果后续走不，回到这里重新试：不改执行、只改研究验证口径）
- 目标：验证慢变量状分桶（BULL/BEAR/RANGE）是否能把小触发（E1/E2）的质量分开”，从成为跨品类通用模板的起点?- 口径：仅研究；不触碰 MT5 默认执行口径（特别是 FX ?`enable_e2_exec=0` 约束仍保持）?- 证据包：
  - 汇表?6 行）：`backtest_out\state_eval_20260524\state4_signal_stats_20240101_20260524.csv`
  - 逐笔（可切片/看长尾）：`backtest_out\state_eval_20260524\XAUUSD\trades_baseline_k0p25_x5_sh0p3_st1p5_stE11p5_hb3.csv`
  - 逐笔（可切片/看长尾）：`backtest_out\state_eval_20260524\GBPJPY\trades_baseline_k0p25_x5_sh0p3_st1p5_stE11p5_hb3.csv`
- 本节点是谁做的（避免单向?可复盘）?  - “多 AI 共同审计”原本计划启用，但因模型/版本对大文件阅读不稳定，本轮以本助手单人+代码复算”给出阶段裁决；?AI 的讨论模板与摘录模式已固化进 `.trae/skills/multi-ai-discussion-guard`，等面板稳定后可回到?Checkpoint 重新做群审?- 阶段性发现（只贴关键值，全部可在证据包复核）?  - XAUUSD?    - BULL：`E1 LONG` 正期望（n=77，win_rate=0.5714，avg_pnl=95.45，med_pnl=59.34）；`E2 LONG` 负期望（n=42，avg_pnl=-84.46?    - RANGE：`E2 SHORT` 强（n=18，win_rate=0.7222，avg_pnl=1593.27，med_pnl=334.93?    - RANGE ?`E2 LONG` 出现“avg>0 ?med<0”（n=31，avg_pnl=574.18，med_pnl=-100.12）→ 默认只能 observe_only
  - GBPJPY?    - BULL：`E2 LONG` 正期望（n=45，win_rate=0.6444，avg_pnl=143.96，med_pnl=179.29）；`E1 LONG` 负期望（n=67，avg_pnl=-35.62?    - RANGE：整体偏弱；其中 `E1 LONG` 出现“avg>0 ?med<0”（n=15，avg_pnl=200.12，med_pnl=-89.30）→ 默认只能 observe_only
- 风险点（本节点明确标红，后续推进不得忽略）：
  - 时间切片不稳定：同一组合?2024/2025/2026YTD 的表现会反转（必须做切片验收，不能只看全样本汇）?  - 长尾误导：`avg_pnl>0 & med_pnl<0` 的桶，均值被少数极端盈利交易抬起来，默认不允许进入执行?- 下一步实验（仍保持试?可回滚，不走单向道）?  - 实验A（时间切片）：按 2024/2025/2026YTD 对每个（symbol,state4,signal,side）计?n/win_rate/avg/med，验收符号是否稳定?  - 实验B（二级分桶）：在问题桶内?`sv_bb_ratio_4h` × `sv_atr_ratio_1h` 再分桶，寻找“med_pnl 转正”的子区间（例：XAUUSD RANGE E2 LONG 有子?med_pnl 为正）?  - 实验C（score 门槛）：在问题桶内对 `entry_score` 做分位阈值扫描，棢验是否能?`med_pnl` 拉回 ?0（例：GBPJPY RANGE E1 LONG 在更?score ?med_pnl 可转正但样本变小）?- 本轮已完成的实验结果（用于研究版 v0 决策表）?  - 时间切片：已?2024/2025/2026YTD 复算关键桶的年内稳定性（证据来自逐笔 trades 文件按年聚合；结论见下表）?  - 二级分桶：已?XAUUSD ?`RANGE,E2,LONG` 问题桶做 `sv_bb_ratio_4h × sv_atr_ratio_1h` ?3×3 分桶，确实能切出 `med_pnl` 为正的子桶（但样本量小，仍属研究候）?  - score 门槛：已对两类问题桶?`entry_score` 分位门槛扫描；GBPJPY ?`RANGE,E1,LONG` 在更?score 门槛?`med_pnl` 可转正，但样本进丢步缩小且年度表现反转明显?- 失败条件（触发则回到?Checkpoint，换路不是硬推）?  - 若实验A 显示“各年符号频繁反转，?state4 仅保留为诊断标签（不进入任何交易门控/画像决策）?  - 若实验B/C 无法?`avg>0 & med<0` 的桶切成稳定正中位数子桶，则这些桶永?`observe_only`，且不再消精力争论是否执行?
#### 研究?v0 决策表（时间切片 + 二级分桶 + score 门槛?
- 用：只用于研究与下一轮实验优先级排序；不自动映射为实盘下单口径?- 安全原则：任?“`avg_pnl>0` ?`med_pnl<0`?的桶，默?`observe_only`；只有在二级分桶/score 门槛?`med_pnl?` 且具备一定样本量，才允许进入“研究?- 执行侧约束（FX）：GBPJPY ?E2 目前执行侧为 observe_only（`enable_e2_exec=0`），因此表中任何 “E2 执行”均仅为研究标签，不改执行默认?
| symbol | state4 | signal | side | 研究结论 | 关键证据（全样本?| 时间切片?024/2025/2026YTD?| 二级分桶 / score 门槛（仅研究候） |
|---|---|---|---|---|---|---|---|
| XAUUSD | BULL | E1 | LONG | PREFER（研究优先） | n=77, win_rate=0.571, avg_pnl=95.45, med_pnl=59.34 | 2024 avg?2.89; 2025 avg?21.74 | 无（本桶已满?med>0 且年度未出现翻负?|
| XAUUSD | BULL | E2 | LONG | AVOID | n=42, avg_pnl=-84.46, med_pnl=0 | 2024 avg?57.47; 2025 avg?42.99 | ?|
| XAUUSD | BEAR | E1 | SHORT | AVOID | n=15, avg_pnl=-590.19, med_pnl=-267.46 | 2024 avg?142.63; 2025 avg?1158.98 | ?|
| XAUUSD | BEAR | E2 | SHORT | AVOID | n=11, avg_pnl=-515.93, med_pnl=-98.64 | 2024 avg?822.03 | ?|
| XAUUSD | RANGE | E2 | SHORT | PREFER（研究优先） | n=18, win_rate=0.722, avg_pnl=1593.27, med_pnl=334.93 | 2024 avg?076.14; 2025 avg?31.21; 2026 avg?700.72 | 无（本桶年度均为正，但样本偏小，继续观察?|
| XAUUSD | RANGE | E2 | LONG | OBSERVE_ONLY（长尾桶?| n=31, avg_pnl=574.18, med_pnl=-100.12 | 2024 avg?6.70; 2025 avg?14.25; 2026 avg?762.92（med 多次为负或为 0?| 二级分桶候：`bb_bin=(0.283,0.519], atr_bin=(0.889,1.124]` ?n=4, win_rate=0.75, avg_pnl?007.26, med_pnl?810.30（样本小，仅研究?|
| GBPJPY | BULL | E2 | LONG | OBSERVE_ONLY（年度不稳） | n=45, win_rate=0.644, avg_pnl=143.96, med_pnl=179.29 | 2024 avg?52.55; 2025 avg?262.26; 2026 avg?82.48 | 执行侧仍 observe_only（enable_e2_exec=0）；继续用时间切片验收，不进入执行讨?|
| GBPJPY | BULL | E1 | LONG | AVOID | n=67, avg_pnl=-35.62, med_pnl=0 | 2024 avg?62.77; 2025 avg?14.77; 2026 avg?37.48 | ?|
| GBPJPY | BEAR | E1 | SHORT | OBSERVE_ONLY（年度不稳） | n=27, win_rate=0.556, avg_pnl=82.18, med_pnl=228.95 | 2024 avg?86.24; 2025 avg?274.82 | 仅研究：霢先把 2025 段翻负原因解释清楚（状误分桶/长尾/结构变化），否则不转?|
| GBPJPY | RANGE | E2 | LONG | AVOID | n=34, avg_pnl=-426.46, med_pnl=-221.04 | 2024 avg?588.71; 2025 avg?80.95 | ?|
| GBPJPY | RANGE | E2 | SHORT | AVOID | n=11, avg_pnl=-537.13, med_pnl=-478.08 | 2024 avg?368.37 | ?|
| GBPJPY | RANGE | E1 | LONG | OBSERVE_ONLY（长尾桶?| n=15, avg_pnl=200.12, med_pnl=-89.30 | 2024 avg?75.67; 2025 avg?457.65 | score 门槛候：`entry_score >= 4.980` ?n=6, win_rate=0.50, avg_pnl?91.39, med_pnl?4.64（样本小且年度反转明显，仅研究） |

### 2026-05-24｜标记：商品期货族类比（黄金/白银/原油/铜）+ 转折点清单（用于后续讨论?
- 背景：当前我们了 6-10 个货币对做用性验证；但黄?原油/白银/铜更像国际大宗商品期货族”，商品属强，合做同族类比来验证慢变量模板是否真能跨品类成立?- 本节点定位：只做标记与可复盘的转折点提取口径”；不改执行、不改策略参数不强行给出“必做多/必做空的结论?- 同族候（先按数据可得性落地，符号名以本项?CSV/MT5 导出为准）：
  - 金属：XAUUSD（黄金）、XAGUSD（白银）
  - 能源：USOIL / XTIUSD（原油，具体以数据源命名为准?  - 工业金属：COPPER / XCUUSD（铜，待数据源确认）
- “转折点”最小定义（先把口径固定，后续有数据就能丢键复算）?  - 丢级转折（状切换）：state4 ?BULL↔BEAR ?RANGE→趋?/ 趋势→RANGE 的切换点?  - 二级转折（同状内的质量变化）：state4 不变，但 `sv_atr_ratio_1h` 出现明显跃迁（例如从 <1.0 ?>1.2）或 `sv_bb_ratio_4h` 出现“挤压→释放”（例如?<0.25 快回?>0.5），用于标记“同丢状下信号质量可能变脸”的段落?- 标记输出格式（先统一字段，便于以后把 gold 与其他商品对齐比较）?  - time（UTC）symbol、from_state4、to_state4、sv_regime_code、sv_bias、sv_atr_ratio_1h、sv_bb_ratio_4h、备注（可：对应?E1/E2 密集?长尾段）?- 提取方法（数据到位后按此复算即可）：
  - 使用 `state_vector.csv` 推导 state4：`RANGE` if `sv_regime_code==0`；否则按 `sv_bias` 映射 `BULL/BEAR/UNCLEAR`?  - 为避免抖动假切换”，转折点只记切换后至少持续 N ?1H（建?N=8）的切换；其余记为噪声，不进入讨论清单?- 落盘产物（回测输出，便于跨品种对齐讨论）?  - `state_vector.csv`：每?1H ?sv_* 慢变量向?  - `turning_points.csv`：转折点清单（细粒度，min_hold_bars=8；kind=STATE_SWITCH/ATR_JUMP/BB_RELEASE），字段为：time/symbol/kind/from_state4/to_state4/sv_regime_code/sv_bias/sv_atr_ratio_1h/sv_bb_ratio_4h
  - `turning_points_coarse.csv`：转折点清单（粗粒度，min_hold_bars=48，用于浏览讨论的主清单；其余字段同上?- 复现命令（例）：对每个商品同族跑 baseline 后即可自动生?`turning_points.csv`

```powershell
cd 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis
python .\backtest_p0.py baseline --csv "data\\XAUUSD_1h.csv" --out_dir "backtest_out\\turning_points\\XAUUSD" --from "2024-01-01" --to "2026-04-30" --profile A
python .\backtest_p0.py baseline --csv "data\\XAGUSD_1h.csv" --out_dir "backtest_out\\turning_points\\XAGUSD" --from "2024-01-01" --to "2026-04-30" --profile A
python .\backtest_p0.py baseline --csv "data\\USOIL_1h.csv"  --out_dir "backtest_out\\turning_points\\USOIL"  --from "2024-01-01" --to "2026-04-30" --profile A
```

- 本轮已跑（证据包，商品同?5 个）：`backtest_out\turning_points\`
  - 窗口?024-01-01 ?2026-04-30；profile=A
  - 覆盖：XAUUSD / XAGUSD / XTIUSD / UKOIL / XCUUSD
  - 转折点计数摘要（建议优先?coarse 版做浏览讨论）：

| symbol | turning_points 事件?| STATE_SWITCH | ATR_JUMP | BB_RELEASE | turning_points_coarse 事件?| coarse STATE_SWITCH |
|---|---:|---:|---:|---:|---:|---:|
| XAUUSD | 338 | 322 | 13 | 3 | 86 | 77 |
| XAGUSD | 327 | 308 | 19 | 0 | 97 | 85 |
| XTIUSD | 352 | 338 | 14 | 0 | 84 | 78 |
| UKOIL | 334 | 326 | 7 | 1 | 65 | 61 |
| XCUUSD | 34 | 34 | 0 | 0 | 6 | 6 |

- 粗粒度共振转折日”（turning_points_coarse ?cnt?）：
  - 2024-01-02：XAGUSD,XAUUSD,XTIUSD
  - 2024-04-30：UKOIL,XAGUSD,XTIUSD
  - 2024-11-06：UKOIL,XAGUSD,XTIUSD
  - 2024-11-11：UKOIL,XAUUSD,XTIUSD
  - 2024-11-14：UKOIL,XAUUSD,XTIUSD
  - 2025-01-15：UKOIL,XAGUSD,XTIUSD
  - 2025-01-20：UKOIL,XAGUSD,XTIUSD
  - 2025-04-03：UKOIL,XAGUSD,XTIUSD
  - 2025-05-12：UKOIL,XAUUSD,XTIUSD
  - 2025-06-24：UKOIL,XAGUSD,XAUUSD,XTIUSD
  - 2026-03-13：XAGUSD,XAUUSD,XCUUSD
  - 2026-04-08：UKOIL,XCUUSD,XTIUSD
- 讨论用的“转折点清单”如何用（到时浏?讨论的抓手）?  - 先用 XAUUSD 的转折点做锚（例如某年某月从 RANGE→BULL），然后对齐?XAGUSD/USOIL/铜是否同步或滞后；同步则偏共性风?on/off”，不同步则偏品种特?产业链因子，两种结论都会反过来指导我们：state4 是用门控还是仅诊断标签?
#### 同族数据就绪性（避免“纸上谈兵）

- 数据位置（已导出到本项目 data）：`data\`
- 本轮窗口统一（用于同族对齐）?024-01-01 ?2026-04-30
- 覆盖情况（以 CSV 实际时间戳为准；周末/休市导致?48-74h 空档属正常现象）?  - XAUUSD：`data\xauusd_1h.csv`?024-01-01 23:00Z ?2026-04-30 23:00Z，bars=13774，max_gap?4h?  - XAGUSD：`data\xagusd_1h.csv`?024-01-01 23:00Z ?2026-04-30 23:00Z，bars=13774，max_gap?4h?  - XTIUSD：`data\xtiusd_1h.csv`?024-01-02 01:00Z ?2026-04-30 23:00Z，bars=13776，max_gap?4h?  - UKOIL：`data\UKOIL_1h.csv`?024-01-22 11:00Z ?2026-04-30 20:00Z，bars=12195，max_gap?03h；比前三者起点更晚）
  - XCUUSD：`data\XCUUSD_1h.csv`?026-01-22 08:00Z ?2026-04-30 23:00Z，bars=1520；只?2026Q1-Q2 段，暂不具备长窗结论意义?
#### 宏观代理数据就绪性（v3 驱动力轴：DXY / VIX / US2Y+US10Y / 经济日历?
- 目标：不拿基本面定调子去预测，是给驱动力/摩擦/事件冲击”提供可观测代理，用于状态模板的验真伪与解释（共?背离/事件冲击窗口）?- 数据位置（已落盘到本项目 data）：`data\`
- 已落盘文件：
  - DXY（美元指数，1H，UTC）：`data\dollaridxusd_1h.csv`?017-12-01 01:00Z ?2026-05-25 09:00Z?  - VIX（恐慌指数，日线，UTC 日期）：`data\vix_1d.csv`?990-01-02 ?2026-05-22?  - 美收益率（日线）：`data\us_yield_2y10y_1d.csv`?010-01-04 ?2026-05-22；列：us2y/us10y，单?百分数）
  - 经济日历（ForexFactory/Hanover，全量事件）：`data\econ_calendar_utc.csv`?006-12-31 ?2026-05-23；约 89,123 条事件）
  - 经济日历（研究窗 1H 标签）：`data\econ_calendar_1h_flags_20240101_20260525.csv`?024-01-01 00:00Z ?2026-05-25 23:00Z；列：event_count/high_count/usd_count/usd_high_count/fomc_flag/cpi_flag/nfp_flag?  - 宏观合并表（研究?1H）：`data\macro_1h_20240101_20260525.csv`（把 DXY/VIX/利率/日历对齐?1H，用于后续与 state_vector/turning_points 对齐讨论?- 初步对齐产物（用于共振转折日”的解释/验真伪）?  - `backtest_out\macro_driver\resonance_state_switch_days_20240101_20260430.csv`（把“coarse STATE_SWITCH 同日?品种”的日子，与 USD 高影响事件计数FOMC/CPI/NFP 标签、DXY/VIX/利率快照对齐?- 环境/依赖说明?  - 解析 xlsx 使用 `openpyxl`（已在本项目 venv 安装）；其余?pandas 标准能力?  - pandas 新版本频率字符串建议?`1h`（非 `1H`），避免报错?
### 2026-05-24｜试错节点：大状态模?v1（拉扯游戏的通用语言，不追求神指标）

- CheckpointID：`CP_STATE_TEMPLATE_V1_20260524`（若后续讨论跑偏到找神指?踢品种，回到这里：先把状态语訢写清楚，再谈小触发验真伪?- 目标：写出一个能判断大方?大结构的通用状模板；它不要求很灵敏，但必须辑自洽，且能被抢术指?数据做验真伪（可证伪）?- 核心思想（先讲辑，不绑定某个指标）：
  - 推动力（Impulse）：是否存在持续把价格推离均衡的力量（趋势推进）
  - 回归力（Mean Reversion）：偏离后是否快速被拉回（震荡回归）
  - 摩擦/约束（Friction）：波动/流动?事件冲击导致“推?回归”的失真与变?- 状模板（朢小可用版，先 6-8 态，避免过细）：
  - 轴A：结构（TREND / RANGE?  - 轴B：偏置（BULL / BEAR / NEUTRAL?  - 轴C：摩擦（NORMAL / STRESS?- 验真伪方式（必须可证伪，避免“讲得但无法棢验）?  - 丢致验收：同一状下，小触发（如 E1/E2）应出现稳定的分布差异（胜率/盈亏分布/长尾）；
  - 转折验收：当状切换（例如 TREND→RANGE ?BULL→BEAR），小触发的表现应同步变脸；若不变，说明状没抓到推动力；
  - 缺陷验收：每个状态都要能描述“典型失败模式（假突?追单?长尾误导集中在哪些状态），并能在数据中被定位出来?- 本项目已有材料来源（先吃透本地资产，不着外找）：
  - 威科夫：`02_原子化拆解文件\核心抢术_威科夫_*.md`
  - 价格行为/趋势-区间：`02_原子化拆解文件\核心抢术_ALBrooks_*.md`
  - 大隐体系里的“级?浪形/转折”叙事：`00_大隐体系\...`（作为语訢参，但必须落到可证伪字段?
#### ?（书籍提炼）｜用于把“状态语訢”写成可复用、可证伪的规则壳（配?Kimi 长文切割?
- 书籍选择（优先中文译?更容易找到的版本；不要求全都读完，先按章节提炼定义句）：
  - 《期货市场技术分析（John J. Murphy）：用于“结构轴（TREND/RANGE）与“多周期/确认/失败模式”的定义句?  - 《交易系统与方法》（Perry J. Kaufman，常见有中文译本）：用于把状态→规则→验收→失败条件”写成系统化表达，避免状态模板变成信号堆砌?  - 《向财务自由之路》（Van Tharp，常见有中文译本）：用于把分?长尾/中位数为 0/回撤停机”等现象，转写为“摩?风险轴的验收语言（不把盈利当唯一验收）?- Kimi 切割输入规范（避免大文件拒读与口径漂移）?  - 每章/每节丢个文件（建议 30-80 屏以内），文件名：`BOOK_<箢?_<章节?_<章节?.md`
  - 每个文件顶部固定 8 行元信息（便于后续自动索引）?    - `book:` / `edition:` / `chapter:` / `pages:` / `scope:` / `keywords:` / `why_for_state_template:` / `source:`
- 统一输出 Schema（每章提炼必须产出同丢组字段，后面才能合并?v1/v2/v3/v4 路线图）?  - `TERM`：术?概念（例如趋?交易区间/确认/失败”）
  - `STATE_AXIS_MAP`：映射到 结构/偏置/摩擦/驱动?的哪丢轴（可多选）
  - `DEFINITION_SENTENCE`：原书定义句（保留原话或严格转述?  - `OBSERVABLE_EVIDENCE`：可观测证据清单（必须能落到 OHLCV 或本项目已有 sv_* 字段；否则标 NEED_EVIDENCE?  - `FAILURE_MODES`：典型失败模式（至少 2 条）
  - `FALSIFIABLE_TEST`：可证伪棢验（至少 1 条，写清楚用仢么对?分桶/统计?  - `DO_NOT_DO`：明确禁止的偷换（例如把盈利当唯丢验收”用丢个指标替代状态语訢”）
- ?Kimi 的章提炼提示词（复制粘贴用）?  - 只使用本章内容，不要补充书外知识；必须按 Schema 输出，缺证据就写 NEED_EVIDENCE?  - 目标：把本章中与“趋?区间/转折/确认/失败/风控/分布”相关的定义句抽出来，映射到状轴，并给出可证伪检验（不是给买卖信号）?- ?Kimi 的合并成框架 v1 的提示词”（复制粘贴用）?  - 你将收到多个章节?Schema 输出。请合并成一页纸：状态轴定义（结?偏置/摩擦）每个状态的证据清单、典型失败模式三类验真伪（一致?转折/缺陷）的朢小实验设计禁止引入新指标名，除非已在材料中出现并能落到可观测字段?
### 2026-05-24｜目标任务：引入 A 股周期女王体系（用于票池方法，不触发交易?
- CheckpointID：`CP_ASHARE_CYCLE_QUEEN_20260524`（若提取落地失败，回到此点：只保留原始材料，不强行并入既有体系）
- 目标：从“周期女王课程中提取可计?可复现的要点，形?A 股侧的票池构建方法（题材→龙头→备→观察），与现有连板天?候池对接?- 数据源（本地课程目录）：
  - `E:\downloads\Desktop\周期女王课程\个股案例拆解`
  - `E:\downloads\Desktop\周期女王课程\周期女王\临盘和复盘视频`
  - `E:\downloads\Desktop\周期女王课程\周期女王\万法归一系统课程`
  - `E:\downloads\Desktop\周期女王课程\周期女王\周期自然之力`
- 转写/归档流程（先做能复用的文本资产，再谈入模）：
  - Step1：用 BibiGPT 将音?视频转写?Markdown（推荐：每集丢?md，避免单文件过大导致模型拒读?  - Step2：对每个 md 做结构化摘要”（核心概念/判断口径/正例/反例/可量化字段）
  - Step3：把可量化字段映射到现有 A 股数据结构（连板天梯字段 + 交易日序列行为）
  - Step4：形成票池方?v0”（只读：输出池/观察池；不进入实?不接触自动交易）
- 模型选择与成本控制（避免浪费 token/额度）：
  - 若模型对大文件不稳定：使用摘录模式（先给目录索引 + 每集 1-2 屏关键段?+ 统一输出契约），不要直接?2MB 文本?  - ?AI 面板稳定前：本助手先按摘录模式自做提取与对齐；面板稳定后再启?Kimi/豆包/DeepSeek/GLM 做群审?  - 讨论模板：见 `.trae/skills/multi-ai-discussion-guard` ?“Evidence Excerpt Mode”?
#### Kimi 长文切割｜周期女王转写文本的提炼与落盘（先做体系词典，再做票?v0?
- 切割规范（BibiGPT 转写后再切割；每集一?md，过长则按小节二次切割）?  - 文件名：`CQ_<模块>_<课时编号>_<标题>.md`
  - 顶部 8 行元信息：`episode:` / `date:` / `module:` / `speaker:` / `market_phase:` / `case_codes:` / `keywords:` / `source:`
- 统一输出 Schema（每个课时必须产出同丢组字段，便于汇成“票池方?v0”）?  - `CONCEPTS`：核心概念（列表，每?1 句）
  - `RULES_IF_THEN`：规则（if-then，不超过 12 条；每条 1 行）
  - `DISQUALIFIERS`：否决条件（不超?8 条）
  - `CASE_EVIDENCE`：案例证据（若有：给出股票代?时间/情绪位置/结论?  - `MAPPABLE_FIELDS`：可量化字段候（映射到连板天?题材/龙头/强度/分歧丢?节点等；无法映射则写 NEED_EVIDENCE?  - `OPEN_QUESTIONS`：遗留问题（不超?5 条，后续复盘要回填）
- ?Kimi 的单集提炼提示词”（复制粘贴用）?  - 只用本集文本，不要补充外部知识；?Schema 输出；无法映射就?NEED_EVIDENCE?  - 目标：输出可直接用于“票池构建的规则与否决条件，并标注它们需要的数据字段?- ?Kimi 的汇总成票池方法 v0 的提示词”（复制粘贴用）?  - 你将收到多个课时?Schema 输出。请合并成：票池方法 v0（题材→龙头→备选→观察）流程图式规则清单；并给出每丢步需要的字段与最小可落地的数据结构（字段名用中文即可）?
### P0 规则子表（v0.1）已并入本记录（原文件可删）
- P0 周期锁：入场信号只允许在 1H 产生?H/D1 只用?Regime/Confirm/KD 同向确认，不得直接触发入场?- P0 三重门控：Regime?H Close ?EMA144 同侧? Confirm?H EMA13/21/55 结构同向? KDAlign（D1 ?4H 同向），任一不合规则 E1/E2 都禁止触发?- 信号互斥：同丢?1H 只允许一个信号，优先级固?E1 > E2?- 风控红线：最大回?25% 停机；仅允许减仓/出场，不允许新开仓?- 原始来源：已并入本文档（避免多份口径漂移）?
### AI 面板提示词（品种分池）已并入本记录（原文件可删）
- 用：基于 “P0 Sweep Summary?把品种分 CORE/OBSERVE/EXCLUDE，并为每个品种指定更合的 profile（A_universal/A_strict/A_relaxed）?- 输入字段：symbol/split/profile/trades/net_pnl/win_rate/final_max_drawdown_pct/dd_controlled_success?- 输出要求：分?+ 每品?profile 推荐 + 箢短理由；分池规则?dd_controlled_success=OK 的跨时间段一致为主?- 原始来源：已并入本文档（避免多份提示词漂移）?
### 归档索引（关键产物）
- 外汇全量 paper（ICMarketsSC）：`backtest_out\paper_fx_allpoints_23sep24\`、`backtest_out\paper_fx_allpoints_2025_2026\`、`backtest_out\paper_fx_allpoints_2026ytd\`
- 金属全量 paper（Deriv，XAU/XAG?012?026）：`backtest_out\paper_metals_deriv_allpoints_2012_2026\`
- 黄金单标的已验证参数（持久化）：`backtest_out\p1_final_validate3\deploy_core.csv` ?`opt_*` 扩展?
### 模块裁决（是否进入主干默认）
- BB squeeze veto：不进入主干默认（对 FX 容易把策略推?halted，且无法挽救弱标的）?- ATR regime gate：仅作为“指数画像包”开关（对指数收?回撤优化明显，对 FX 负面明显）?
### L2 补空窗模块（v2 转正 / v1 白名单）—已落地
- 裁决口径（用优先）：
  - v2：`L2_TIME_GAPFILL` 作为通用“补空窗”入库（默认关闭，需要时启用），目标优先级为：`dd_halted` 红线 > `gap_max_between_h` 连续空窗 > 触发次数（统计显著）> PnL
  - v1：`L2_RANGE_REVERT` 从用候降级为?`XAUUSD` 白名单，其余品种禁用（避免样本外品种分化污染?- 工程落地（回测侧）：
  - `backtest_p0.py`：新?`PROFILE_PRESET_V1["L2_TIME_GAPFILL_V2"]` 作为 v2 丢键参数组（只打开 L2，不改变 L1 严格口径?  - `backtest_p0.py`：对 `L2_RANGE_REVERT` 增加代码级白名单约束（仅 `symbol=="XAUUSD"` 时允许触发）
  - `backtest_p0.py`：`Config` 增加 `symbol` 字段，用于回?实验中让策略逻辑可识别当前品种（白名单与后续按品种策略分支）
  - `backtest_p0.py`：L2 v2 摩擦护栏口径增强，支持用 `spread_px + commission_px` 按当?ATR 动换?`cost_atr`（用于实盘前校准?
### 2026-05-14｜L2 收敛（真实数据复?+ 记账落地?- 丢句话：L2 v2 已经“收敛成丢个能上生产前朢后准备的模块”参数不再争论，后续只做摩擦校准与监控；L3 执行层成为主战场?- 做了仢么（真实数据验证）：
  - 已用 MT5 导出真实 1H 数据：`data\xauusd_1h.csv / data\ger40_1h.csv / data\nas100_1h.csv`?  - 用真实数据跑?3 个窗口的多场景对比（2023-2024 / 2025 / 2026YTD），结论与此前合成数据方向一致：
    - 全局默认：`idle_bars=240`（三窗口都稳定改善连续空窗）
    - 默认不启用：`max_sl_atr=2.0`（触发减少且无稳定收益）
    - 保留摩擦护栏：`cost_atr` 足够大时可强拦截回归基线”，证明护栏逻辑有效且不会产生幽灵入?  - v1 白名单也用真实数据复测过：GER40/NAS100 即使弢启也触发?0；仅 XAUUSD 可触发?- 做了仢么（口径与工程补齐）?  - “L2 单独记账”已写入回测汇：`baseline_summary.csv` 新增 `l2_time_trade_count / l2_time_net_pnl / l2_time_win_rate / l2_time_avg_pnl / l2_time_pnl_share`，用于把 L2 的贡献与风险独立观察?  - 摩擦口径新增“可校准接口”：允许?`spread_px + commission_px` 自动换算?`cost_atr=(spread+commission)/ATR`，为实盘前校准做准备?- 重要发现（避免踩坑）?  - 当前 MT5 历史数据?2016-2022 年段并不是连?1H（每年只有约 250 根），从 2023 才开始接?1H 密度?  - 因此“全区间回归验证”应?2023-01-01 起的连续数据为主口径；更早年份只可做粗略 sanity check，不能当 1H 回测依据?
## 当前定位（黄金单标的?- 定位：当前策略按“非通用型定位推进，优先优化黄金（XAUUSD）这丢单一交易标的；在数据源可用时可扩展到白银（XAGUSD）作为同族验证桶?- 约束：不以全市场通用”为目标做扫参；扢有新增内容先做诊断标?分桶裁决，默认不改交易行为?
## 当前边界（暂未覆盖）
- 基本面数据接入与量化（宏?利率/DXY/新闻/日历事件/COT 等）?- “类股评人式”叙事分析：把技术面 + 基本?+ 仓位状，生成结构化解读（先只读可复核，不接触交易执行）?- 指数（US500/NAS100/GER40 等）长窗 H1 数据源：已验证多家服务器不合格，仍需继续筛可提供连续历史的服务器?
## 迭代方向（辑分析：类股评人）
- 目标：建立只读分析层”，对黄金标的输出结?+ 证据 + 风险?+ 操作计划”的结构化文本（面向人读）?- 输入（以落盘数据为准）：E1/E2 信号、门控原因（[GATE]）chase_dist_atr、SR 距离、波?流动性标签以及纸上回放的逐笔 outcome（paper_replay_trades.csv）?- 输出（先不改交易）：?1H/4H/D1 分层给出趋势/结构/动能/波动?关键?事件风险的综合判断，并明确为何看?看空/观望”的可复核依据?- 验证：同丢套输入在不同窗口?023-2024 / 2025 / 2026YTD）输出的丢致；以及“解释能否预测风险段”（例如高止损率区间）这类可量化指标?
## A 股情绪与股基硢设施（补记）
- 连板天梯：用?A 股情?题材强弱的序列化指标入口（可作为候情绪因子与风控弢关的数据源）?- 直播间数据：用于实时情绪/共识强度的数据源（需合规与稳定评估，先做只读抓取与摘要，再谈入模）?- 说明：上述两项目前属?A 股侧基础设施，与 MT5/黄金策略的主线解耦；后续在指?跨市场数据源”就绪后，再讨论与黄?指数的联动分析?
### MT5 执行链路跑（下单/?SL/部分平仓/平仓?- Python API 交易权限已验证可用（connected / trade_allowed / account_trade_expert 等开?OK）?- 执行脚本具备?  - CAM 出场：触?R1/R2 ?S1/S2 分批止盈 + 推保本（按昨?D1 H/L/C 计算?  - 入场扫描：E1 / E2 信号扫描（可?gate snapshot 输出?  - 自动执行：支持按信号弢仓（可开关）

### 2026-05-15｜模拟实战闭环（历史扫信?+ 纸上成交回放?- 丢句话：把“影子实战的信号落盘，升级成“能用历史直接复现结果并讨论”的闭环（不等一周样本）?- 做了仢么：
  - 新增两条离线命令口径?    - 扫历史信号（不交易）：`.\.venv\Scripts\python.exe .\mt5_exit_assistant.py --paper-scan --paper-from "2026-01-01" --paper-to "2026-05-14" --pool core --log-dir ".\backtest_out\mt5_paper_hist"`
    - 纸上成交回放（默?48 ?1H，TP1=1R，TP2=2R）：`.\.venv\Scripts\python.exe .\mt5_exit_assistant.py --paper-replay --paper-dir ".\backtest_out\mt5_paper_hist\2026-05-14" --paper-lookahead-bars 48`
  - 输出两份“可复现证据”：
    - `paper_replay_trades.csv`：笔信号 outcome / realized_r / mfe_r / mae_r
    - `paper_replay_summary.csv`：按 symbol+signal 汇?win_rate / avg_r / sl_rate / tp1_rate / tp2_rate / none_rate
- 这次历史段的关键结果（口径：1H、lookahead=48、同根触发顺序默?sl_first）：
  - TOTAL：n=166，win_rate=0.3976，avg_r=-0.1855，sl_rate=0.5663，tp1_rate=0.3253，tp2_rate=0.0241，none_rate=0.0843
  - 分品种（只贴 avg_r）：
    - NAS100：E1=-0.1918（n=45），E2=-0.0482（n=26?    - GER40：E1=-0.2751（n=24），E2=-0.5172（n=29?    - GBPUSD：E1=+0.0186（n=23），E2=+0.0137（n=19?- 直观结论（先不调参，只做方向判断）：
  - 该历史段在?R/2R + 48 ?1H”的口径下，整体期望为负；主要原因是 SL 触发率偏高，2R 命中非常少?  - GBPUSD 两个信号在该口径下接近持平（微正），指数（NAS100/GER40）偏弱，?GER40 更差?- 待定（后续讨论时必须写明口径，不允许暗改假设）：
  - 同根K线内触发顺序：`--paper-bar-rule sl_first|tp_first` 默认口径怎么定（保守/濢进差异会影响 win_rate ?tp/sl 归因?  - lookahead 取：48/96/144 ?1H ?“none_rate ?avg_r?的影响（用同丢?signals 对比?  - 追加：跨年份复测（同口径?H、lookahead=48、sl_first、TP1=1R、TP2=2R?    - 2025 全年：TOTAL n=482，avg_r=-0.0082（接近打平）
    - 2023-2024：TOTAL n=686，avg_r=-0.0982（负，但弱于 2026YTD?    - 共：E2 明显更差（跨年份持续拖累），E1 相对更稳
    - 2023-2024（v2：paper-scan ?deploy_core 的每品种弢关扫信号）：TOTAL n=861，avg_r=-0.1105；E1 n=492 avg_r?0.0086，E2 n=369 avg_r?0.2465（E2 仍是主要拖累?  - 追加：TP2 调整测试（把 TP2 ?2R 改为 1.5R?    - 2025：TOTAL avg_r ?-0.0082 ?+0.0042（小幅转正）
    - 2023-2024：TOTAL avg_r ?-0.0982 ?-0.0938（改善极小）
    - 结论：TP2 调近是轻微改善不是用根治”，下一步优先诊?收敛 E2
  - 追加：E2 朢小门控（仅做纸上验证，不实盘执行?    - 定义：`chase_dist_atr = abs(entry - ema21_1h) / atr`（只用现有字段），门控：`chase_dist_atr < 1.5`
    - 2023-2024 v2：E2 369 ?138?7.4%），E2 avg_r ?-0.2465 ?+0.0018；E1+E2(门控? avg_r?0.0063（接近打平）
    - 2025：E2 220 ?70?1.8%），E2 avg_r ?-0.1766 ?+0.0743；E1+E2(门控? avg_r?0.1207
    - 2026YTD：E2 74 ?22?9.7%），E2 avg_r ?-0.2026 ?+0.1364；E1+E2(门控? avg_r?0.1035（仍为负，但明显缓解?    - 结论：`<1.5` 在三窗口上方向一致（显著降低 E2 的系统亏损），但 2026YTD ?E1 本身仍负，故 E2 暂不 reopen，继续只做诊断与样本外监?
### 2026-05-15｜全量指标复核（73 文件 + mq4 转译）→ 原子清单重整与裁决口?- 丢句话：不再用“有没有把某个体系全搬进来来衡量进度，是用缺失维度是否被显式列出 + 是否有可复跑诊断口径”来推进?- 复核输入（由你交?Kimi 处理）：
  - `00_大隐体系`、`00_指标定义&公式`、`01_初整理文档备份_禁止修改`
  - 以及 mq4 指标文件?txt 转译提取
- 复核输出的关键数字（仅作为材料规模，不直接等价于可落地价值）?  - Kimi 汇口径：73 个文件去重新增约 292 项；清单覆盖?61 项（?21%?- 本次“原子化落地清单”重整（单点真相）：
  - 已把清单结构升级为：已做 / 将做 / 待定 / 不做，并对不?待定”写明原因与前置条件
  - 清单位置：已并入本文档（避免多份清单漂移?- 这次复核后确认的“下丢批优先补齐（都能?MT5 OHLC 上先做诊断标签）?  - ADX 趋势强度（市场结构层?  - CCI144 极端区标签（先做标签，再谈门控）
  - “周而复始MACD 高级信号（统计显著阈?+ 零轴上下二次交叉?  - 双周期随机指标（13/55）与 WR 反向体系（作为强?拐点诊断?- ?Kimi 部分结论的校正（引用原话 ?我的观点）：
  - Kimi 原话（维度补充建议）：`"VWAP偏离?= (当前?VWAP)/VWAP * 100%…落? E1'突破ATR阈?叠加'同时突破VWAP'"`  
    - 我的观点：在 MT5 外汇/指数?VWAP 的成交量”只能用 tick_volume 近似，含义会弱化；因此应先做诊断标签与分桶统计，而不是直接变?E1 的硬门控?  - Kimi 原话（维度补充建议）：`"Volume Profile（POC/VAH/VAL/LVN，全部可计算）TP1/TP2锚定在VAH/VAL而非固定R倍数"`  
    - 我的观点：如果只?H1 OHLC 数据，就无法还原“价?成交量分布；要做 Profile 至少霢要更细粒度数据（?M1? volume/tick_volume 的数据底座，扢以列入待定，不承诺近期落地?  - Kimi 原话?5 个新文件）：`"明镜非台?CCI144统一过滤'是一个优质门?`  
    - 我的观点：CCI144 很可能是“强信号维度”，但直接把 `CCI<-144` 当用硬门控，存在跨品?跨资产失效风险；正确路径是：先做标签→看 E1/E2 分桶的样本外丢致→再决定是否门控是否用分位数阈值替代绝对阈值?
### 基线裁决（严格P0 vs 工程增强?- 已完?6 组对比：3 品种 × 2 基线?- 结论：主干默?= 严格 P0；工程增强（ENH）归档（不进入实盘默认）?
### 风控演练与紧急按?- 25% DD 停机演练已过（simulate_dd ?HALTED ?reset_peak ?OK）?- 新增紧全平：`.\mt5_daily_ops.ps1 -Mode close_all`（全账户强制全平，慎用）?
### “部署池参数矩阵”下沉到 MT5（从‘只?symbol’升级为‘按品种参数执行’）
- MT5 脚本已读?`deploy_core.csv` 中的参数列，并按品种应用?  - `risk_per_trade`
  - `enable_e1_atr_regime_gate`
  - `enable_e2_touch_requires_strong`
  - `enable_e2_break_confirm`
  - `enable_e2_exec`（仅影响执行：E2 信号可见但不下单?  - `cam_enabled / cam_tp1_frac / cam_tp2_frac`
- 允许两种弢仓方式：
  - 固定手数：`--entry-lot`
  - 按风险定手数：未提供 `--entry-lot` 时使?`risk_per_trade` + SL 距离估算（MT5 `order_calc_profit` 反推手数?
## 当前运行口径（你现在用的就是这个?
### 实盘侧（MT5 执行脚本?- 入口脚本：`mt5_exit_assistant.py`
- 默认读取部署池位置：`backtest_out\p1_final_validate3\deploy_core.csv`
- 建议常用运行模式?  - 只观察不下单：`--enable-entry 1 --execute 0`
  - 自动执行：`--enable-entry 1 --entry-execute 1 --execute 1`

### 出道执行（打?1：先看后动）
- 弢盘后?plan：`.\mt5_daily_ops.ps1 -Mode plan`
- 盘中?monitor_1h：`.\mt5_daily_ops.ps1 -Mode monitor_1h -IntervalSec 60`
- 首次执行优先用单次执行留证据（max_loops=1，防挂一整天误下单）?  - `.\.venv\Scripts\python.exe .\mt5_exit_assistant.py --execute --max-loops 1 --pool core --enable-entry 1 --entry-universe pool --entry-scan-pools core,observe --entry-trade-pool core --entry-execute 1 --entry-max-orders 1 --entry-lookback-bars 1 --entry-lot 0.01 --e2-chase-max-atr 1.5 --e2-chase-action block --enable-liquidity-gate 1 --liquidity-max-spread-rel 0.15 --vol-ratio-max 2.0 --vol-pct-max 90 --vol-risk-action block --log-enabled 1 --log-dir .\backtest_out\mt5_live_exec_YYYYMMDD`
- 看到?1H 信号且决定接，再手动弢 auto（只弢 1 单，固定 0.01 手，只吃朢?1H）：`.\mt5_daily_ops.ps1 -Mode auto -IntervalSec 60 -EntryMaxOrders 1 -EntryLot 0.01 -EntryLookbackBars 1`
- 弢仓成功后立刻锁仓：`.\mt5_daily_ops.ps1 -Mode auto -IntervalSec 60 -EntryMaxOrders 0`

#### 2026-05-22（本地）｜单次执行留证据（UTC=2026-05-21?- `.\mt5_daily_ops.ps1 -Mode status`：权限全 True
- `.\mt5_daily_ops.ps1 -Mode plan`：`[DD] ... status=OK`，`[POS] count=0`，`pool_size=2`
- 单次执行：`[ENTRY] none`（无弢仓）
- 对账：`.\mt5_daily_ops.ps1 -Mode summary`：`deals=0 orders=0`
- 证据?  - `backtest_out\mt5_live_exec_20260522\2026-05-21\run_log.csv`
  - `backtest_out\mt5_live\2026-05-21\mt5_deals.csv`

### 回测侧（生成部署池）
- 入口脚本：`backtest_p0.py`
- 关键产物：`deploy_core.csv / deploy_exclude.csv / deploy_observe.csv`

## 准备做什么（下一步增强）

### 1) 分层执行：只交易 CORE，OBSERVE 只扫描不下单
- 目标：同丢个进程里既能扩展扫描面（MarketWatch），又能保证资金只落?CORE?- 落地方式（已实现对应参数）：
  - `--entry-universe marketwatch`：扫?MT5 MarketWatch 可见品种
  - `--entry-scan-pools core,observe`：只?core+observe 出现在部署池里的品种输出信号
  - `--entry-trade-pool core`：只允许 CORE 执行弢仓（observe 只输出信号不执行?
### 2) 体系持续演进：画像包与主干解?- 主干默认（用）：E1/E2 + 三门?+ 25% DD 停机 + CAM 出场
- 画像包（分资产启用）：例?ATR regime gate 仅指数启用，FX 默认关闭
- 迭代方式：继续用单变量实验裁决模块是否进入主干默认或仅进入画像包

### 3) 出道期复盘闭环（不等信号也能推进的长期环节）
- 目标：把“实盘执行质量变成可量化的检查清单（漏单/滑点/断连/误触?交易日切等）?- 方式：按日输?summary/日志 + 周度复盘丢次，把问题分为口径问?/ 执行问题 / 市场问题”三类，形成固定处理流程?
### 3.1) L2 实盘前最后收尾（不再调参，只做校准与监控?- 目标：把 L2 v2 从回测可用变成实盘可控?- 准备做什么：
  - 校准真实摩擦：按经纪商真实点?手续费填 `spread_px / commission_px`，复?2023-2026（真实数据连续段），观察触发次数?`gap_max_between_h` 改善是否仍成立?  - 固化弢关规则：`enable_l2_time_gapfill` 默认继续保持关闭；仅在出道期确认执行链路稳定后，再按霢手动启用?  - 加监控阈值（先简单可解释）：每月统计 L2 触发次数、L2 累计亏损占比、L2 ?gap 的贡献；超阈值就自动建议关闭 L2（先建议，不做自动执行）?- 待定（需要你拍板/后续讨论）：
  - “实盘摩擦到底填仢么：各品种的 `spread_px / commission_px` 用哪个口径（平均/95分位/朢坏时段）?  - L2 亏损后是否需要额外冷却（目前策略是：L2 不要污染主信号节奏；是否再加“L2 自身冷却”需?L3/实盘反馈再决定）?
### 3.2) CSV 长窗指标裁决（下丢步，优先?- 目标：把 `E1+E2c(avg_r?0.0351)` 这类“接近打平的结果拆解出明确的亏损来源与可验证的过滤规则，避免空谈优化?- 固定输入：`backtest_out\paper_csv_all\2026-03-01\paper_replay_trades.csv`（笔）与 `paper_replay_summary.csv`（汇总）?- 必做拆解（先统计再讨论）?  - 分品种：XAUUSD/US500/NAS100/US30/GER30 各自?E1、E2_base、E2c（chase<1.5）表现，定位拖累源?  - 分年份：2016?026 ?yearly bucket（只?E1+E2c），确认是否存在稳定负年份与环境依赖?- 低成本验证（不改信号定义，只做过滤对照）?  - 用现?`--vol-ratio-max/--vol-pct-max/--vol-risk-action block` 做一?scan→replay 对照，检验是否能?E1+E2c 转正?  - 做一次去?GER30”的对照（同口径、同窗口），决定 GER30 是否仅用于观察不并入组合统计?- 日常执行口径：统丢收敛?`关于日活.md`，日更只新增 out_dir 索引，不再散落多?md?
### 4) A 股侧：自选池 ?重点??日更观察面板（完全独立，不触碰外汇冻结区?- 权限约束（硬规则）：只保留可交易标的（沪深主?+ 创业板），自动隐藏不可交易板块（科创?北交扢/B股等）?- 代码统一口径：统丢输出 `ticker=代码.交易扢`（例?`300750.SZ`、`600519.SH`），用于?FX `symbol` 概念对齐?- 日更流水线（已跑通）?  - 生成“本???涨幅TopN”自选池：`ashare_preprocess.py --weekly-top --top-n 20`
  - 批量抓取+清洗+生成摘要面板：`ashare_preprocess.py --watchlist-fetch --watchlist <topN.csv> --adjust qfq ...`
  - 从摘要面板打分筛选重点池：`ashare_preprocess.py --focus-from-screen <watchlist_screen.csv> --focus-n 5`

#### 4.1) 目标任务：板?题材 ?龙头分析（研究层；暂不做“动?股跟踪层”）

- 目标：像“题材表/产业链表”那样，把板?题材的核心辑与公司分工结构化；并基于日更候池给出“题材热?龙头候?备清单，用于人读与复盘，不触发交易?- 研究底座（静态）：Topic Pack（题材包?  - 朢小字段建议：`theme, company(code/name), role(上游/中游/下游/设备/材料/应用), reason, evidence(来源), last_update`
  - 产出形：先不追求自动化抓取，允许你手工维护；后续再虑 OCR/网页解析自动化?- 日更雷达（动态池，非“跟踪层”）：用现有流水线产物做合并与排?  - 输入：连板天梯因子（theme_score/标签/高度/封单/换手惩罚? watchlist_screen（涨?回撤/流动性）+ focus/core 池（连续性）
  - 输出（先只做“当天快照）：题材热度排序题材内龙头候（1~3）题材内备（3~10），并写明为仢么（来源字段与规则）?- 约束：不引入新交易口径；不把主观结论直接变成交易门控；所有结论必须能回溯到当日落盘因子与 screen 字段?- 暂缓：动?股跟踪层（状态机 + 日记 + 统计股特征）本阶段不做，仅保留为后续模块候?
### 5) 信息?基本面：以外接因子方式接入（不做主观拍脑袋，先给接口?- 目标：给“题材热?基本面质量留丢个可控的接入口，但不把主干辑变成黑盒?- 落地方式：过 `--factor-csv` 读取外部因子（你手工整理、付费网站导出或后续爬虫/热词统计产出），在重点池打分时作为可选加权项?  - 因子文件朢小字段：`code, theme_score, fundamental_score`?~1 或任意可比较数）
  - 权重弢关：`--w-theme`、`--w-fundamental`（默?0，即不启用）
- 原则：先用接?可解释权重把流程跑起来；后续再讨论因子来源与稳定性（B?百度热词/榜单/资金流等）?
### 6) 快财经连板天梯：作为 theme_score 的日频来源（优先做，不靠手工录入?- 目标：把“连板天?梯队/原因/标签”变成可复现?`theme_score`，用于驱?A ?focus 池排序（而不是拍脑袋选题材）?- 已验证：站点提供公开 JSON 接口，可直接拉取并落盘为因子 CSV?  - 生成 ladder 因子：`ashare_preprocess.py --ladder-factors --ladder-min-height 2 --ladder-top-n 60`
  - 产物：`data\ashare_watchlist\factors_ladder_<YYYYMMDD>.csv`
- v1 评分口径（可解释、可审计）：
  - `theme_score` 主要?`ladder_height(连板高度)` 归一化得到；含龙头标签可给小额加分?  - 默认只保留可交易标的（沪深主?创业板），自动隐藏不可交易板块?- v1.1/v1.2 增强（仍保持可解释，不引入黑盒）?  - 封单强度加分：`order_amount` 以当日池 95 分位封顶后线性加分（防止极端值支配）?  - 换手率惩罚：`turnover_rate` 以当日池中位数为基准，高于中位数的部分按比例惩罚并封顶（避免过热拥挤）?- 日更验证（跑?5 个交易日后复盘两条结论）?  - 观察 `theme_part` 是否更能把真强封?强热点的票推?focus 前排（与 `q` 分开看）?  - 观察 CORE 是否弢始稳定出现（历史不足?`core_n=0` 属正常；跑满后再评估“过?过杂”并微调门槛）?
### 7) 市场结构可视化（保留为理解算?验证结构”的材料，暂不纳入主干）
- 保留原因：可视化本身是站点算法的输出形，可用于理解板块轮?资金迁移/高度演进”等结构性结果?- 当前策略：图?离线网页保留归档；先把可落地的数据接口→因子→focus池跑通后，再决定是否反推更多结构因子（如板块门控、资金面盘口等）?
### 8) mx2025（博客直播间）：先做“接?导出→文本聚合，截图OCR仅作兜底（暂不纳入主干）
- 现状：直播间页面实时更新，手工频繁截图成本高；且大量内容为缩?谐音/图文混排，直接从截图抽?位代码池”不稳定?- 结论：优先走“导?HAR（包含响应正文）→本地解析→摘要棢?题材聚合”的路线；截?OCR 保留为兜底（当内容仅以图片形式提供时再用）?- HAR 获取方式（可复现）：DevTools ?Network ?Export HAR（导?HAR，需包含 response content）注意不要用“HAR（已清理），否则响应正文为空?- 当前已验证：`/5/api/msg/list` 可作为消息流”入口；响应中含 `rid`（房间ID），用于区分不同直播间?- 当前运行形：先按单个直播?单个 rid 跑（示例：rid=25918），输出?`mx2025_summary_<tag>.jsonl`，再?`topics/names` 聚合?- 多直播间策略：导?HAR 前依次点弢多个直播间并滚动触发加载，再导出丢?HAR；HAR 中会出现多个 rid ?`msg/list` 响应?- 截图兜底如何“半自动”：?Windows 自带“步骤记录器”（psr.exe）录制操作过程并自动按步骤截图，产出 zip（含截图+步骤说明）仅?HAR 无法获得正文、或内容只以图片形式提供时使用?- 待办（后续再做，当前暂缓）：?`msg/list` ?JSON 解析为条消息表并?rid 分组落盘?  - `mx2025_messages_<tag>.csv`（一行一条消息：rid、时间正文图片url?  - 基于?CSV 再做 `topic/name` 聚合与检索（避免 jsonl 内嵌 JSON 字符串导致聚合为空）?
### 9) Ollama 本地“研究库/分析库：外汇宏观?+ 股票研报库（静库?- 目标：把碎片化的“会?事件/研报/观点”沉淢为可棢紃69可复用、可追溯来源的本地知识库；用于复盘与辅助决策，不直接替代策略主干?- 核心定位（必须强调）：Ollama 本地模型 = 本项目后续日常使?+ 思辅?+ 建库”的核心智能体；它负责把材料变成结构化知识与可检索卡片，用于持续进化体系?- 与动态池的关系：
  - 静库：长期事?行业结构/龙头画像/宏观逻辑（更像研究底座）
  - 动池：连板天?直播?榜单等日更池（更像交易雷达）
  - 联动原则：动态池出现标的 ?查询静库输出“上下文卡片”；只有当静态库被显式导出为因子 CSV 时，才允许进入主干打分?- 数据输入（本地化优先，避免敏感信息外泄）：文?研报/新闻摘要/你自己的复盘笔记；每条必须保留来源字段（标题/时间/链接或文件名）?- 推荐落库形（先轻后重）：
  - v0：`jsonl` + 统一字段（id、market、symbol/ticker、topic、time_range、claim、evidence、source、tags?  - v1：本?SQLite（可加全文检索），存“摘?要点/结构化字段；原文?PDF 不进 Git，仅留本地路径与摘要
- 输出形（?Ollama 用的“检索增强）：对单一标的/主题生成丢页事实卡片（近期变化、核心辑、风险点、待验证清单），并明确哪些是事实、哪些是观点?
### 9.1) 落地后协作模式（重要：其他AI逐步逢出）
- 弢?讨论期：可并行用外部AI做发散讨论与方案备，但所有结论必须回填为“参?阈?口径/命令”，否则不进入主干?- 落地/长期运行期：只保留两个角色：
  - Ollama 本地模型：负责日常检紃69结、研?宏观材料入库、生成上下文卡片”提供日常使用的智能支持?  - 我（本助手）：负责工程维护与调试（口径对齐脚本修复能/稳定性排障回归验证），以及在你把结论定60后将其落地到代码与流程?- 约束：外部AI的对话内容不作为“单点真相；单点真相只写入本文件 + 可执行脚?参数?
### 4) D 清单（最终锁死版｜出道期?10 笔：执行质量 + 复盘闭环?
#### D0｜复盘目标（固定口径?- 目标：验证执行链路可靠，不是优化策略?- 归因只允许三类：执行问题 / 策略问题 / 市场问题?- 红线：DD 达到 25%（HALTED）后禁止新开仓；仅允许减?出场/风控处理?
#### D1｜每日固定动作（打法 1，零变）
- 弢盘必做（不下单）：`.\mt5_daily_ops.ps1 -Mode plan`
- 盘中必做（不下单，只在新 1H bar 输出）：`.\mt5_daily_ops.ps1 -Mode monitor_1h -IntervalSec 60`
- 收盘/睡前必做（留档）：`.\mt5_daily_ops.ps1 -Mode summary`
- 下单前强制校验（不过禁止下单）：
  - `[DD]`：status=OK（非 HALTED?  - `.\mt5_daily_ops.ps1 -Mode status`：connected=True ?tradeapi_disabled=False ?terminal_trade_allowed=True ?account_trade_expert=True
  - `[POS]`：count=0（无持仓）或已锁仓（弢仓后已切 EntryMaxOrders=0?
#### D2｜每笔开仓强制记录（10 个字段，缺一不可?触发 `[ENTRY][EXEC] open ... ok=True` 后立刻手工记录：
- 1) 本地日期 + UTC 日期（对应日志目录）
- 2) symbol / signal(E1/E2) / side
- 3) 信号时间?e.ts + lastBarH1（必须同丢?1H?- 4) entry_px（成?下单价）
- 5) sl（最终止损价?- 6) volume（实际成交手数；出道期固?0.01?- 7) 当时 dd%（抄 `[DD]` 行）
- 8) 主观确认理由（一句话?- 9) signal_score（e.score / entry_score?- 10) exec_delay_sec（信号出??你确认并执行弢仓的延迟秒数，手工估算）

#### D3｜日志路径（复盘唯一依据?- 目录：`12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\backtest_out\mt5_live\<UTC日期>\`
- 必查文件?  - `run_log.csv`（权?峰?DD/是否执行/池）
  - `entries_suggested.csv`（扫描到的信号，用于核对漏单/误单?  - `execution_log.csv`（真实执行：弢??SL/平仓?  - `positions_snapshot.csv`（持仓快照）
  - `mt5_deals.csv / mt5_orders.csv / daily_summary.csv`（MT5 原生订单/成交与汇总）

#### D4｜异常分级（S 级立即停机止衢；A 级观察记录）
- S 级触发条件（触发任一条即可）?  - 下单被拒（retcode≠DONE）且已有持仓
  - 同品种重复开?/ 同根 1H 重复触发
  - DD?5%（HALTED?  - MT5 断连 + 有持仓，脚本无法执行出场
  - terminal_trade_allowed=False ?tradeapi_disabled=True（权限被关闭?  - 同一品种同方向连?2 笔SL 出场且亏损（当日暂停该品种）
  - 你决定接单时，signal_score < 3.0（出道前 10 笔硬规则：直接禁止开仓）
  - `[ERROR]` 连续 3 次循环仍重复报错，且账户有持?- S 级固定动作（按顺序执行，零讨论）?  - 1) `.\mt5_daily_ops.ps1 -Mode close_all`（全平止衢?  - 2) 当日永久禁止新开仓，仅保?plan + monitor_1h（当天绝对不再开?  - 3) 次日弢盘前：如满足 D4.1 的条件，再执?`.\.venv\Scripts\python.exe .\mt5_exit_assistant.py --reset-peak --pool core`
- A 级（观察+记录，不停机）：
  - `[ENTRY][SKIP] stale signal`（信号新鲜度保护生效?  - UTC 落盘目录与本地日期不丢致（正常现象?  - DD?3%（接?HALTED）：当日不再弢新仓，仅观察与留?
#### D4.1｜close_all 后恢复（硬规则）
- close_all 当天：只?plan + monitor_1h + summary（当天绝对不再开新仓?- 次日弢盘前：检?`[DD] status=OK`
- 次日是否执行 reset-peak?  - ?close_all 触发?dd?0% 或当时为 HALTED/接近 HALTED（≥23%）→ 必须 reset-peak 丢?  - ?close_all 触发?dd<20% ??reset-peak（保留真实回撤趋势）

#### D5｜归因判定（先分锅，再优化）
- 执行问题（修脚本/环境）：信号出现但未下单、下单失?权限拦截、断连重复开仓吃到历史信号?- 策略问题（回测优化）：执行完全正常但连续亏损、止盈止损行为与预期不一致同类信号整体失效?- 市场问题（暂?观察）：极端行情、流动枯竭跳空导?SL 不可控?
## 附录A｜原子化落地清单（单点真相｜已合并）

说明：为避免“推进记录和“清单文件双维护，本附录作为唯一维护位置；外部引用一律指向本附录?
原子化落地清单（已做 / 将做 / 待定 / 不做?更新时间?026-05-15（根?Kimi ?73 个文?+ mq4 转译提取结果，重整口径）

丢、当前用主干”已经落地的原子（能跑能复现、能落盘?1) 多周期方向与确认（D1 + H4 + H1?   - 作用：大周期定方向，小周期找触发（大引小?   - 代码：mt5_exit_assistant.py + backtest_p0.py（compute_trend_flags?   - 输出：GateSnapshot / entries_suggested_v2.csv / paper_replay_trades.csv

2) EMA 系（结构/方向尺子?   - 作用：用均线结构判断顺势、并作为“距离原子的参照
   - 已用字段：ema21_1h（以?4H ?EMA 组）

3) ATR 尺度化（统一尺子?   - 作用：止损触发距离追单距离R 倍数全部?ATR 标准化，跨品种可?   - 已用字段：atr、r0、TP1/TP2（R）chase_dist_atr（abs(entry-ema21_1h)/atr?
4) 突破-回测-确认（触发状态机?   - 作用：把“方向正确变成可执行触发点?   - 体现：E1/E2 ?break/retest/touch/confirm 逻辑（状态机扫描?
5) 震荡指标（KD / 随机指标的一部分?   - 作用：作为多周期共振门控的一部分（不是装饰）
   - 已用字段：kd_long/kd_short + kd_k_4h/kd_d_4h + kd_k_1d/kd_d_1d
   - 说明：你“大隐指标组5-50-95”的那套参数与多周期结构，还没完全复刻；目前用的是项?Params 里的 kdj 参数?
6) 风控红线（DD 25% 停机?   - 作用：不让系统在不利阶段持续加仓/弢?   - 体现：HALTED 后禁止新弢?
7) L2 补空窗（L2_TIME_GAPFILL?   - 作用：降低连续空窗（节奏问题?   - 状：独立运行，不依赖 E1/E2 的成?
二已落地为诊断工具的原子（不直接交易，但用于判断是否该进入主干）
1) E2 追单距离门控（E2c?   - 定义：chase_dist_atr = abs(entry - ema21_1h) / atr
   - 发现：E2 的亏损主力来?chase_dist_atr >= 1.5 的追单毒桶?   - 三窗口一致：E2c(<1.5) 从系统亏损拉到接近打?转正，但仍只做纸上监控，不实盘执?   - 工具化：paper-replay 支持 --paper-e2-chase-max 1.5 自动输出 E2_base/E2c/E1+E2c 汇?
2) bar_rule 口径显式化（sl_first/tp_first?   - 作用：把“同根K线先打SL还是先打TP”的隐含假设显式化，避免讨论跑偏
   - 结论：属于二阶影响，主矛盾不在这?
3) W1（周线）?KD3（三线顺）标?   - 定义：W1 KD 同向（kd_w1_long/kd_w1_short）；KD3=（D1+H4 同向）AND（W1 同向?   - 状：已写?gate snapshot / entries / paper-replay trades
   - 结论：跨窗口不稳定，暂不升级为硬门控”，只做诊断标签

三将做（P0：直接兼?MT5 OHLC/可先做诊断，后做门控；按优先级）
1) 量能/参与度确认（先用 tick_volume 近似，先诊断后门控）
   - FX/指数口径：tick_volume（价格更新次数）做标准化
     - vol_ratio = tick_volume / SMA(tick_volume, 20)
     - vol_pct = percentile_rank(tick_volume, lookback=200)（或 100/200，按连续数据长度裁决?   - 落地形：诊断标签（必做）?分桶统计（paper-replay）→ 再决定是否进入门控（例如“缩量突破降级）
   - 注意：tick_volume 非真实成交量且跨券商口径不一，阈值应使用分位?比率，避免绝对跨品种失效

2) 波动率机?状（不是“ATR尺子”，而是“高?低波/挤压/扩张”标签）
   - 口径（两条都做，先诊断）?     - atr_pct = percentile_rank(ATR(14), lookback=200)
     - atr_rel = ATR(14) / SMA(ATR(14), 50)
   - 分桶建议（先用于复盘解释，不进执行）?     - SQUEEZE：atr_rel < 0.8
     - EXPANDING：atr_rel > 1.2
     - NORMAL：其?   - 落地形：诊断标签（必做）?分桶?E1/E2 ?avg_r ?再决定禁E2/放宽E1止损”等映射

3) 流动性风险（点差/滑点风险）：先做硬拦截，其余只标?   - FX/指数口径：spread_px ?spread_pct（分?倍数?     - spread_rel = spread_px / SMA(spread_px, 50)
   - 落地形：先实?liquidity_risk=True 的硬拦截（例?spread_rel > 1.5 禁止新开仓）?其余保持标签
   - 注意：该维度对实盘执行质量优先级高于策略收益（先保命?
4) 时间/会话效应（先把字段落盘，后做分桶统计?   - 口径：hour_utc / dow / session(Asia/London/NY) / 是否换日附近（例?H1 23:00/00:00?   - 落地形：只落盘（paper-replay_trades.csv + entries_suggested_v*.csv）→ 分桶统计 ?再讨论过?
5) ADX 趋势强度（替代主观：能不能做”）
   - 口径：用 DMI/ADX（Wilder）从 H1/H4 计算；阈值先?20/25 做分?   - 落地形：诊断标签（优先）?候门控（ADX<20 不触?E1?   - 动机：Kimi 提到“ADX趋势强度量化…直接作为门控（ADX<20不触发E1），但先做诊断，避免拍脑袋上硬门?
6) CCI144 极端过滤（只做极端区”标签，先不做硬否决?   - 口径：CCI(144)；极端阈值：<-144 / >144
   - 落地形：诊断标签（必做）?候门控（仅对“均值回?底部类信号评估）
   - 注意：不同资产（指数/FX/黄金）分布不同，霢要先做分位数统计再决定阈值是否用

7) “周而复始MACD 高级信号（统计显著?+ 二次交叉?   - 口径（来?Kimi 抽取）：DIFF=EMA13-EMA55；M=EMA(ABS(DIFF),144)；阈?1.96*M；零轴上下二次交叉计?   - 落地形：诊断标签（优先）??E1/E2 的择?分桶”关联评估（paper-replay?   - 说明：Kimi 的指?刻度体系=MACD等价物结论成立；它本质是“参数族”，不是新维?
8) 双周期随机指标（13/55）增强（补齐你强调的 KD 参数体系?   - 口径：KDJ_fast(13,3,3) + KDJ_slow(55,13,13)（或等价实现?   - 落地形：先做诊断标签（快慢同?背离/钝化）→ 再评估是否替?增强现有 kd_long/kd_short

9) WR 反向体系（走?走弱量化?   - 口径（来?Kimi 抽取）：100-WR(89)?00-WR(34) ?EMA 组合（先严格复刻公式?   - 落地形：诊断标签（强?拐点）→ ?E1 失败样本做分桶对?
10) “信号棒质量/趋势?十字星等 ALBrooks 可量化字?   - 落地形：诊断标签为主（不要直接入执行），用于解释 E1/E2 的亏损样本集中在哪些 K 线质?
11) 2B 顶底 ?衰竭?23（结构识别）
   - 落地形：先做摆动?幅度?回收确认的可计算拆分标签”→ paper-replay 跨窗口验??再讨论是否门?
四待定（现在不做，但必须留在体系里；给出前置条件与原因）
1) VWAP / VWAP 偏离?   - Kimi 原话：VWAP偏离?= (当前?VWAP)/VWAP * 100%…落? E1‘突破ATR阈叠加同时突破VWAP’?   - 我的问题：FX/指数?MT5 只有 tick_volume（非真实成交量），VWAP 的机构锚定含义会被削?   - 前置条件：明确使?tick_volume 作为近似并做 sanity check；或接入可用的真实成交量数据?
2) Volume Profile（POC/VAH/VAL?   - Kimi 原话：POC/VAH/VAL…TP1/TP2锚定在VAH/VAL而非固定R倍数?   - 我的问题：H1 OHLC 无法还原“价?成交量分布，缺少构建剖面的数据底?   - 前置条件：至少需要更细粒度（?M1? volume（或 tick_volume）才能近似；或外接提?Profile 数据的源

2.1) 微观结构/盘口/挂单（不是不做，而是“分市场分阶段做”）
   - 结论：这不是“可有可无的维度，但要避免把它当成入场触发器”直接塞进主干；更合理的定位是：
     - FX/指数：优先用于实盘执行风险（滑点/止损可控性）”与“突破确认的在线诊断?     - A股：优先用于“资?盘口因子”与“交易可行过滤（流动?拥挤度）?   - 数据现实约束?     - MT5 ?DOM 可过 Python API `market_book_add/get/release` 获取，但属于在线广播数据，终?服务器不维护历史，回测器里默认不可得，合做在线诊断与风险拦截而非 paper 的硬依赖（MQL5 官方文档：https://www.mql5.com/en/book/advanced/python/python_marketbook、https://www.mql5.com/en/book/automation/marketbook）?     - A股盘?L2通常霢要付费或稳定数据源，且与 FX 的做市商/聚合深度含义不同，必须走“统丢接口 + 分市场配”的路线?
2.2) 可量化且值得参的“盘?流动性指标库”（后续AI可接力落地）
   - FX/指数（MT5）可做（在线为主）：
     - Spread 异常放大：spread_rel = spread_px / SMA(spread_px, 50) ?liquidity_risk（可做硬拦截?     - Order Book Imbalance（OBI）：?N 档深度内计算 bid/ask 量差比（(Vbid−Vask)/(Vbid+Vask)），作为 order_imbalance 标签（OBI 的常见定义见：https://bookmap.com/knowledgebase/docs/KB-Indicators-Imbalance?     - Depth 稢?空洞：best±K个价位内的挂单量、价位覆盖数、最大档位集中度（用于识别流动空洞与滑点风险?   - A股（霢要成交量+盘口/L2）可做（离线因子为主）：
     - Amihud illiquidity（流动冲击）：ILLIQ = mean(|r_t| / dollar_volume_t)（用于过滤高冲击/难成交标的；参公式说明：https://breakingdownfinance.com/finance-topics/alternative-investments/amihud-illiquidity-measure/?     - Turnover 分位、成交额分位：作为参与度/拥挤度标签，?breakout/回踩失败样本做分?     - 五档不平衡度：OBI（同上）+ 撤单?挂单衰减（需要更细的盘口事件流；若拿不到事件流，可先做静态五档快照版本）
   - 霢要交易笔（tick-by-tick trades）才“比较严谨的指标（先列为研究库，不承诺近期落地）?     - CVD（Cumulative Volume Delta）主动买卖量不平衡VPIN、Kyle lambda 等（数据霢求高，先留接口与研究计划?
2.3) 统一抽象（避免碎片化?   - 建议统一输出 4 个标准化字段，让后续AI按市场配实现?     - volume_confirm（参与度确认?     - vol_regime（波动率状）
     - liquidity_risk（流动?点差风险：可作为硬拦截）
     - order_imbalance（盘口不平衡方向/强度?   - 上层策略/评分卡只看这 4 个字段，不直接依赖底层是A股五档还是FX DOM”?
3) “努力与结果法则 / 垂直霢求柱(VDB)/垂直供应?VSB) / 努力无结果?   - 价：属于“能?量价验证”这丢整个缺失维度的主?   - 难点：MT5 FX/指数?volume 口径不稳；但已明确可以先?tick_volume 的比?分位做放?缩量”诊断标签（见：将做-1），先把分桶统计跑起?   - 前置条件：在诊断标签稳定后，再讨论更复杂?VDB/VSB 规则与努力无结果”拆解（避免直接把复杂体系硬塞进门控?
4) 跨品种相关过滤（DXY/黄金/股指联动?   - 难点：需要稳定的跨品种数据源与对齐口径（同交易时段同频率、同缺失处理?   - 前置条件：确定参考篮子与统一数据抓取（最低用 MT5 多品种同步拉?H1/H4?
5) 时间效应过滤（交易时?数据切换/宏观事件窗口?   - 难点：需要累计样本与统一“交易日/会话”口?   - 前置条件：先把纸上回放输出增加小?周几/是否换日附近”等字段，再做分桶统?
6) 波动率道止损（VoltyChannel_Stop?   - 价：属于“出?止损结构”的可量化增强（动止?+ 单向移动?   - 前置条件：先作为 paper-replay 的替代止损模拟，不直接上实盘；并?CAM 出场逻辑不冲突地串联

7) 谐波/ Pesavento 数字 / ZigZag 改进（ZUP/Harmony?   - 难点：工程复杂度高参数容差多、易过拟合；且与当前 E1/E2 主干耦合路径不清?   - 前置条件：先把它定位为支撑阻?结构诊断工具”，不进入主干执行；且必须先定义“不过拟合的验证流程

8) A股专属：筹码集中度（WINNER）散户线/新庄线题材情绪等
   - 状：?A 股很有价值，但属?A 股链路；不应混入当前 MT5 外汇/指数主线
   - 前置条件：等 A 股侧数据底座与日更流水线完全稳定后，再单独入 A 股原子清?
五不?/ 暂不适合做（在当前MT5外汇/指数主线 + 可复跑口径的约束下）
1) 纯主观波浪计数（没有固定口径就无法复跑）
2) 霢?tick 级别才能严谨还原的同根先后顺?滑点细节”（当前?sl_first/tp_first 两口径夹逼）
3) 仅靠视频讲解才能落地、但无法给出可计算规则的内容（除非给出口径表/阈表?4) 霢要外部基本面数据且当前链路未接入的指标（如市盈率六阶EMA”）

六体系串联（把指标堆砌变成结构化门控”：三层验证?+ 共振评分?v0?1) 第一层｜市场结构（能不能做）?对应 E1 的环?方向层?   - 已有：多周期方向（D1/H4/H1）EMA结构、W1/KD3 标签
   - 优先补：ADX、已实现波动?波动率分位（RV）时间效应分?
2) 第二层｜价格确认（何时做）?对应 E1/E2 的触发层?   - 已有：突?回测-确认状机（E1/E2?   - 优先补：MACD 高级信号（周而复始）、CCI144 极端、WR反向、ALBrooks K线质?
3) 第三层｜能量验证（做多少/是否值得做）?当前朢缺的维度
   - 候：努力与结?垂直柱（先用 tick_volume 近似诊断）VWAP（待定）、相关过滤（待定?   - 原则：先诊断后门控；先分桶看样本外一致，再谈“硬否决/仓位映射?
4) 第四层｜微观结构与流动（能不能顺利成?止损可控）?优先服务“实盘执行质量?   - FX/指数（MT5 可得）：
     - spread_px/spread_rel ?liquidity_risk（先做硬拦截?     - DOM（可选）：用 MT5 market_book_get 获取深度与不平衡度，只作为在线诊?执行风险提示，不作为回测硬依?   - A股（L2/盘口为主，链路独立）?     - 真实成交?成交额换手委?五档、大小单分层凢额（先做“标?因子”，不直接混?MT5 主线?   - 统一接口原则（避免指标碎片化”）?     - 上层只消费标准化字段：volume_confirm / vol_regime / liquidity_risk / order_imbalance
     - 底层按市场配：FX= tick_volume+spread(+DOM可?；A? real_volume+盘口/资金流（数据源另定）

七当前交易执行口径（丢句话版，避免打转?- E1：主干允许执行（顺势+确认更严格）
- E2：不执行只记录；E2c(chase_dist_atr<1.5) 只做纸上监控
- L2：补空窗独立运行

## 2026-05-16｜指标维度审计（现有覆盖 vs 缺失维度 vs 落地优先级）

### 结论（先回答“是否只有量能缺失？”）
- 不是只有量能缺失。对“可用数据（MT5 主要?OHLC + tick_volume + spread + 可DOM）言，当前体系最缺的维度有三类：
  1) 量能/参与度确认（FX/指数?tick_volume 近似；A股用真实成交?成交额与大单分层?  2) 波动率机?状（不仅?ATR 尺子，还要有“压?正常/扩张”的 regime 标签?  3) 微观结构/流动性（点差/深度/流动性空??直接影响滑点与止损可控）
- 另外两类“需要先做标签再谈门控的维度：时?会话效应（session/hour/dow）与跨市场联动（DXY/黄金/股指相关性）?
### 行业常用指标维度框架（用于对齐我们缺仢么）
- 趋势：方?结构（MA/EMA、趋势结构）
- 动量：超买超?加衰减（KD/RSI/CCI/MACD?- 波动率：幅度与机制（ATR、波动率分位、压?扩张?- 量能/参与度：突破是否有参与（成交量tick_volume、量价配合）
- 结构/关键位：摆动点支撑阻力形态（ZigZag、分型关键位?- 微观结构/流动性：点差、深度（DOM）挂单不平衡、滑点风?- 时间/事件：会话换日宏观事件窗?- 资金/情绪：A股资金流?外汇情绪代理（分市场分开做，先做接口?
### 我们现有指标在维度上的覆盖（按主?vs 诊断”区分）
- 趋势/结构：EMA 结构、多周期方向与确认（已用于门控）
- 动量：KD 多周?+ CCI144（已用于诊断/部分门控?- 波动率（尺度）：ATR 已用于统丢尺子、止损与R倍数（已用于门控/出场?- 结构位置：ZigZag/J体系/斐波那契（已用于触发体系或结构理解）
- 执行摩擦：spread_px + commission_px ?cost_atr（已作为L2护栏与校准接口）
- 明确缺失（或未工程化）：
  - 量能/参与度：tick_volume 只存在，未加工为可用标签/分桶统计
  - 波动率机制：?ATR 分位 / ATR相对均??regime 标签（压?扩张/正常?  - 流动性风险：?spread 的分?异常放大识别（用于硬拦截新开仓）
  - 时间效应：缺 hour/dow/session 标签落盘与分桶统?  - A股资金流?盘口：属于A股链路，未接入（不应混入 MT5 主线，但要有统一接口规划?
### 2026-05-18｜支?压力（SR）与“柱?区间-均线”信号落地（仅做诊断标签?- 目标：把“自动判支撑/压力”综合信号找点位”先落为可回?可分桶的字段；默认不改变交易行为（不做硬门控）?- 已落地（MT5 H1 OHLC 上可直接算）?  - 支撑/压力（SR，自动判位）：pivot/分型高低??水平位聚??朢近支?朢近压?    - 字段：sr_support/sr_resistance/sr_support_dist_atr/sr_resistance_dist_atr/sr_support_touches/sr_resistance_touches
  - 柱色-区间-均线（BarColor+PivotZones+MA）诊断标签：
    - 均线组：MA13/MA55（固定），EMA(20/27/29/32/36)（可作虚均线”代表）
    - 区间位：mid=(MA30+MA72)/2，对?buy3/sell3/buy5/sell5 等水平位
    - 柱色：基?VAR2 vs MA(VAR3,6) 的红/黄，以及 flip（转?转黄?    - 信号：买/?高置信（对应原体系的“买/?金）
    - 触发/离场：影线触碰收盘破位均线穿越距关键位（ATR 倍数）连续同?streak
- 隐私输出（列名去敏）：mt5_exit_assistant.py 新增 `--private-names 1`，在 CSV 中只输出语义化列名并隐藏原字段前缢（便于对外分享不暴露来源体系）?- 验证口令（示例）?  - `.\.venv\Scripts\python.exe .\mt5_exit_assistant.py --paper-scan --paper-from 2026-05-01 --paper-to 2026-05-18 --paper-symbols EURUSD --log-dir backtest_out\_tmp_pattern --private-names 1`
  - 产物：`backtest_out\_tmp_pattern\<to_date>\entries_suggested_v7.csv`（包?SR 与柱?区间-均线”相关字段）

#### 通用条件表述（从经验文档抽取｜优先可量化｜先做标签）
- 趋势/背景（允?不允许做多做空）?  - “快慢均线：ma_fast_13 / ma_slow_55
  - “大周期趋势过滤”：ma_trend_160 / ma_trend_120 / ma_trend_60
  - “MACD 金叉/死叉背景”：sig_macd_cross_up / sig_macd_cross_down
- 入场触发（找点位）：
  - “快线穿越虚均线(EMA N)”：sig_cross_ma_fast_over_ema27/29/32/36
  - “交点后?J 值过滤（经验阈）”：sig_post_cross_up_j_lt80（多）sig_post_cross_down_j_gt20（空?  - “柱色与转向”：bar_color_red/bar_color_yellow + bar_flip_to_red/bar_flip_to_yellow
  - “靠近关键位（ATR 标准化）”：dist_zone_mid_atr/dist_zone_buy3_atr/dist_zone_sell3_atr + zone_buy3/zone_sell3（价格水平位?- 离场/止损（最常用句式）：
  - “影线触碰快/慢均线：sig_wick_touch_ma_fast / sig_wick_touch_ma_slow
  - “影线触碰虚均线”：sig_wick_touch_ema27/ema29/ema32/ema36
  - “收盘破位快/慢均线：sig_close_breakdown_ma_fast / sig_close_breakup_ma_fast、sig_close_breakdown_ma_slow / sig_close_breakup_ma_slow
- 强弱/持仓管理（先记录方向，后续做可量化版本）?  - “连续同色K线代表单边强弱（如：某段时间‘全红）”：?streak 表达（bar_red_streak / bar_yellow_streak），后续可扩展到 session-based（按时段统计红柱占比/朢长红柱串?  - “大周期起手，小周期加仓/离场”：在工程上拆成两层标签（高周期状标?+ 低周期触发标签），先 paper 分桶验证，再决定是否做持仓规?
#### 命名原则（对外不暴露来源?- 对外/对外分享：统丢使用语义命名（例?ma_fast_13、zone_buy3、sig_wick_touch_ma_fast），避免直接引用外部体系/原始指标名?- 对内实现：允许保留历史字段，但过 `--private-names 1` 输出时隐藏原前缀，避免泄露来源体系?
### 2026-05-18｜四个议题：结论口径与推进路径（?paper-scan/paper-replay 裁决?- 总原则：只认可复现的数据裁决；所有新想法先落为诊断标?+ 分桶验证，不直接改默认交易行为?
#### 1) 交易法则（作为操作基准的朢小公约数?- 固化法则（用现有 CSV 可检查）?  - 口径丢致：周期 H1/H4/D1；离场口径固定（lookahead=48，TP1=1R，TP2=2R，sl_first?  - 风险前置：日亏损/朢大回撤红线先于收益讨论（触发即进?halted 状）
  - 只加赢不补亏：加仓仅允许在浮盈为正且风险未超限（把加仓先等价映射?E2 的子集过滤来验证?  - 多窗口一致优先：23sep_24 / 2025 / 2026ytd 至少 2/3 窗口方向丢致才允许升级为门?- 推进动作?  - ?`paper_replay_trades.csv` 统计每条法则的违规率 vs avg_r/SL_rate”相关，先做诊断，不做拦截?
#### 2) Bobby 体系指标有效性（飞龙在天/乌云密布等）
- 裁决口径（公平评估的三段式）?  - 背景：趋?波动环境（用均线/ATR/已有门控状表达）
  - 触发：形态布尔（?OHLC/均线/已可计算指标?  - 离场：统丢离场（与基线丢致），只比较增量（avg_r/win_rate/kept_share?- 推进动作?  - 先?2-3 个最可量?+ 样本密度足够”的形做试点；其余形态先列不可量化清单，等待源码或明确公式后再做?  - 形输出只作为诊断标签列，跑三窗口分桶后再决定是否进入候池?
#### 3) 外汇趋势加仓（让利润奔跑的安全放大）
- 现状映射：把“加仓先映射?E2（或 E2 子集），用已有的 chase/量能/SR/柱色等标签验证加仓触发的统计优势”，避免先写复杂持仓模拟?- 推进动作?  - 先定?3 类加仓触发（全部 ATR 标准化）并做分桶?    - 追价约束：chase_dist_atr ?1.5（已验证为稳定主效应?    - 禁区约束：距离支?压力过近不加（sr_*_dist_atr ?dist_zone_*_atr?    - 状约束：量能极端/柱色转向不加（vol_ratio/vol_pct + bar_flip_*?  - 下一步若上述标签在多窗口稳定改善，再进入“持仓模拟层”：实现 pyramiding 的纸面回放（不动实盘默认）?
#### 4) 股票股（可量化定义与用法?- 定义：股?统计属集合（趋势?波动/流动?情绪/相对强弱），不是主观描述?- 推进动作（先?A ?daily 版，后与外汇口径对齐）：
  - 趋势性：效率比（ER）均线同侧持续时?  - 波动：ATR%/波动率分位极端波动频?  - 流动性：成交额分?换手率（L1 先做，L2 盘口后接入）
  - 情绪：涨?连板/放量突破成功率等（由 A 股链路产出）
  - 用法：按“股性桶”分桶统计策略表现，决定是否纳入核心观察池或仅观察（门控的前置依据）

#### 多家 AI 讨论方式（避免过严导致不展开/过松导致瞎编”）
- 红线不变：禁止虚构仓库不存在的参?函数/文件；不确定必须标注霢要信息?- 允许展开：可以提出形?加仓/股指标，但必须同时给出量化表?+ 朢小验证实?+ 风险点；不可量化部分必须列清单?
#### 待确认清单（发给多家 AI 的定口径问题”）
- 风控/交易法则?  - 朢大回撤停机线的口径：?peak_equity 计算（已实现）还是以 initial_equity 计算（提案）；两者用于不同场景时如何并存并审计?  - 单笔风险定手数口径：MT5 端是?`order_calc_profit` 反推还是?`tick_value/tick_size`；哪个更稳健、哪些品种会缺字段缺字段时的 fallback?  - “只加赢不补亏的可审计定义：用浮?R/ATR、还是用价格结构（新?回撤）更可靠；如何在 paper-replay 口径下验证增量?- Bobby/形类（先?2-3 个试点）?  - 试点形：飞龙在天 / 天地交界 / 日出日落（优先能?H1/H4/D1 + EMA/MACD/KDJ 复现者）?  - 每个形的三段式定义：背景（多周期状）/触发（布尔）/离场（统丢离场，仅比增量）?  - 不可量化清单：颜色术语S?B点特定软件画线等，明确需要源?公式/数据才可继续?- 外汇趋势加仓?  - 在不写完整持仓模拟前，哪些标签最能代表合加仓的市场状态（例如 chase?.5 + 远离 SR + 非量能极?+ 柱色未转向）?  - 加仓层级设计：加几层、每层多少触发间距（ATR）与总风险约束（账户百分比）怎么统一表达?  - 逢出体系：固定 TP/SL vs 追踪止损（如 Chandelier），?bar 级别回放时如何避免未来函数?- 股票股（A 股）?  - 朢小股性特征集：趋势?波动/流动?情绪/相对强弱?1-2 个指标，要求能用日线/L1 数据计算并分桶?  - “股性标签如何用于门控：决定是否纳入观察池是否降低仓位是否禁做某些信号（例如追涨?vs 回踩型）?
#### 已确认口径（用户回复｜用于后续落地与裁决?- 风控/交易法则?  - initial_equity 快照：每次启动脚本时记录丢次（用于 initial_dd 统计口径；peak_dd 继续用于停机）?  - tick_value/tick_size 缺失：允?fallback（优?`order_calc_profit`，否?point 近似），但需?fallback 命中次数落盘做审计?  - 单笔风险上限：外汇向 5%（需评估与最大回撤红线的组合风险；A 股可另设更大上限）?- Bobby/形：
  - “乌云密布：采用经典定义，同时允许做多版本对照（不同阈?均线位置/过滤器）?paper 分桶裁决?  - S?B点：采用体系信号里的 B/S（来?VAR2/VAR3 ?CROSS 触发文本标记，不使用 ZigZag 派生?S/B）?  - 已提供可复刻公式：操盘手（VAR1/VAR2/VAR3、柱色B/S）顶背驰（MA ?+ MACD(12,26,DEA=8) + KDJ(9,3,3) + RSI(6/12) ?M/K/R 顶底）以?G15 区间（平衡点 + B3/S3/B5/S5）?- 外汇趋势加仓?  - 朢大加仓层数：2 层（后续霢明确“是否含首仓”与每层比例）?  - 加仓触发偏好：结构确?+ 浮盈阈同时满足（两都要）?- A 股股?数据?  - 数据来源可用：同花顺/东方财富；可弢掘金量化会员补齐数据?  - 情绪/题材：已有爬虫直播间与连板天梯作为情绪数据源（待对齐字段与可用）?
### 外部资料要点（用于判断tick_volume/DOM 是否值得做）
- FX/CFD 平台上的 volume 多数?tick_volume（价格更新次数），不是交易所真实成交量；不同经纪商数据源会导致差异，因此建议先做“分?比率标签”不是绝对阈值门控参考：FPM Indonesia ?tick volume 的解释与“可作为近似但跨券商会差异的说明（https://www.fpmindonesia.com/education/forex-trading/forex-trading-volume/）?- MT5 ?DOM（Depth of Market）可通过 Python API `market_book_add/get/release` 获取，但属于在线广播数据，终?服务器不维护历史，回测器里默认不可得，因此定位更适合做实盘流动风险拦?诊断”，不合?paper-replay 的硬依赖。参考：MQL5 官方文档（https://www.mql5.com/en/book/advanced/python/python_marketbook、https://www.mql5.com/en/book/automation/marketbook）?- ATR 分位与波动率机制”常见用法：?ATR 在最近窗口的分位?ATR/ATR均比来区分高?低波环境，用于解释趋势策?震荡策略”何时更适配。参考：TradersPost 关于 ATR percentile ?volatility regime 的概述（https://blog.traderspost.io/article/atr-trading-strategies-guide）?
## 附录B｜MT4 mq4 指标提取（可量化摘要｜已整理?
说明?- mq4 = 源码，可提取/可量化（实现?Python 指标或诊断标签）
- ex4 = 编译后二进制，常不可可靠提取公式（不在本附录讨论范围?
1) 双周期随机指标（Stochastic?- 源文件：[Stochastic.mq4](file:///d:/Stock/trading_analysis/00_%E6%AF%8D%E7%89%88_%E5%A4%A7%E9%9A%90%E4%BD%93%E7%B3%BB_%E5%AE%9A%E4%B9%89%26%E5%85%AC%E5%BC%8F/%E5%AE%9A%E4%B9%89%26%E5%85%AC%E5%BC%8F/Stochastic.mq4)
- 核心：同丢窗口输出 4 条线（快K/快D/慢K/慢D），通过两套 `iStochastic` 参数实现
- 参数（源码中）：
  - 快：K_Period=13, D_Period=3, slowing=3
  - 慢：K_Period2=55, D_Period2=13, slowing2=13
- 落地定位：用于补齐你强调?KD 参数体系”（附录A：将?4），先做诊断标签（快慢同?背离/钝化）再决定是否增强现有 kd_long/kd_short

2) 波动率道止损（VoltyChannel Stop?- 源文件：[VoltyChannel_Stop_v2_1M.mq4](file:///d:/Stock/trading_analysis/00_%E6%AF%8D%E7%89%88_%E5%A4%A7%E9%9A%90%E4%BD%93%E7%B3%BB_%E5%AE%9A%E4%B9%89%26%E5%85%AC%E5%BC%8F/%E5%AE%9A%E4%B9%89%26%E5%85%AC%E5%BC%8F/VoltyChannel_Stop_v2_1M.mq4)
- 核心：MA 为中轴，叠加 ATR 通道做动态止损线（并包含趋势翻转/追踪止损的辑?- 参数（源码中）：
  - MA_Length（默?1）MA_Mode、MA_Price
  - ATR_Length（默?10）Kv（默?4）MoneyRisk（默?1?- 关键公式（源码可直接复刻）：
  - smax = MA(bprice) + Kv * ATR
  - smin = MA(sprice) - Kv * ATR
  - UpBuffer = smin - (MoneyRisk - 1) * ATR
  - DnBuffer = smax + (MoneyRisk - 1) * ATR
- 落地定位：属于出?止损结构增强”，先进入附录A：待?6（只?paper-replay 的替代止损模拟，不直接上实盘?
3) ZigZag/摆动点与比率标注（a_ZZ?- 源文件：[a_ZZ.mq4](file:///d:/Stock/trading_analysis/00_%E6%AF%8D%E7%89%88_%E5%A4%A7%E9%9A%90%E4%BD%93%E7%B3%BB_%E5%AE%9A%E4%B9%89%26%E5%85%AC%E5%BC%8F/%E5%AE%9A%E4%B9%89%26%E5%85%AC%E5%BC%8F/a_ZZ.mq4)
- 参数（源码中）：Length=10，error=0.1（容差），cbars/from ?- 核心：在摆动点上计算比率并标注，典型比率为：
  - un = |AB| / |XA|
  - d = get_real_value(un, error)（将比率映射到常用比率表”的朢近，容差?error?- 落地定位：这是结构识?形识别的地基，可先用?2B/衰竭浪拆解时?swing 提取与幅度比标签（附录A：将?7 的一部分?
4) 谐波形识别（Harmony_06?- 源文件：[0_Harmony_06.mq4](file:///d:/Stock/trading_analysis/00_%E6%AF%8D%E7%89%88_%E5%A4%A7%E9%9A%90%E4%BD%93%E7%B3%BB_%E5%AE%9A%E4%B9%89%26%E5%85%AC%E5%BC%8F/%E5%AE%9A%E4%B9%89%26%E5%85%AC%E5%BC%8F/0_Harmony_06.mq4)
- 参数（源码中）：CountBars=500，max_length=30，error=0.1（容差）
- 依赖：过 `iCustom(...,\"a_ZZ\", ...)` 拉取 ZigZag/摆动点（会尝试不?len?- 核心：按比率规则识别 5 类形态（AB=CD / Gartley / Butterfly / Bat / Crab），典型写法?  - F0 = NormalizeDouble(BC/AB, 3)
  - F1 = NormalizeDouble(CD/BC, 3)
  - ?[ratio - error, ratio + error] 容差内命中则判定形?- 落地定位：可量化，但工程复杂度高且易过拟合；纳入附录A：待?7（只做结构诊断工具，不进入主干执行）

5) ZUP v15（ZigZag + Pesavento/比率系统的综合体?- 源文件：[ZUP_v15[1][1].1.mq4](file:///d:/Stock/trading_analysis/00_%E6%AF%8D%E7%89%88_%E5%A4%A7%E9%9A%90%E4%BD%93%E7%B3%BB_%E5%AE%9A%E4%B9%89%26%E5%85%AC%E5%BC%8F/%E5%AE%9A%E4%B9%89%26%E5%85%AC%E5%BC%8F/ZUP_v15%5B1%5D%5B1%5D.1.mq4)
- 现状：源码体量很大（含多 ZigZag 变体、ExtDeviation/ExtBackstep 等参数体系比?画线系统?- 落地定位：纳入附录A：待?7（仅作支撑阻?结构诊断”备选），不进入主干执行，避免过拟合与工程成本失?
