# STRATEGY_BUNDLES_v1.0 — 策略组合与三层决策流

> 版本：v1.0 | 状态：纲领配套文档 | 与 SYSTEM_ARCHITECTURE_DRAFT.md 和 PERIOD_QUEEN 对象卡配合使用  
> 目标：定义每个 `regime_state` 对应的策略组合、对象卡激活列表、仓位策略，以及完整的决策流

---

## 1. 文档定位

**为什么需要这份文档**

`PERIOD_QUEEN_P0_F` 对象卡定义了七态状态机和状态识别逻辑，但它只回答"当前是什么状态"。这份文档回答：**知道状态后，系统应该做什么？**

它是纲领的"操作手册"：把第一层（环境识别）的输出，转化为第二层（策略选择）和第三层（执行管理）的具体指令。

---

## 2. 策略组合总览

| 策略组合 | 适用状态 | 交易权限 | 核心思想 | 风险等级 |
|----------|----------|----------|----------|----------|
| **TrendFollowing** | ATTACK_SUSTAINED | FULL | 趋势跟踪，重仓持有领涨 | 中（趋势确认后风险可控） |
| **BuildPosition** | ATTACK_CONFIRMED | FULL | 阵型确认，建仓跟进 | 中-低（阵型提供安全边际） |
| **TrialEntry** | GESTATION | REDUCED | 试错建仓，轻仓验证 | 高（新周期未确认） |
| **WaitAndSee** | POWER_TRANSITION | REDUCED | 观望过渡，轻仓试错 | 高（方向不明） |
| **GradualExit** | REMAINING_WARMTH | EXIT_ONLY | 逐步退出，只出不进 | 中（末期惯性可能延续） |
| **HoldCash** | ATTACK_UNSUSTAINED | HALT | 空仓等待，禁止交易 | 低（无交易风险） |
| **HoldCash** | CUTTING_COMPLETE | HALT | 空仓等待，禁止交易 | 低（无交易风险） |

---

## 3. 策略组合详细定义

### 3.1 TrendFollowing — 趋势跟踪（ATTACK_SUSTAINED）

```yaml
strategy_name: "TrendFollowing"
applicable_regime: "ATTACK_SUSTAINED"
permission: "FULL"
max_position_size: 1.0
entry_min_votes: 3

# 核心逻辑：
# 1. 领涨持续 + 空间板持续 + 阵型有效 + 包容度存在 + 无退潮力量
# 2. 市场处于最强上涨状态，允许重仓趋势跟踪
# 3. 优先捕捉 3Buy（离开中枢）和 1st pullback（首次回调）

# 激活对象卡（按优先级排序）：
activated_objects:
  - CHZL_BSD_P0_E:    # 缠论买卖点
      priority: 1
      allowed_types: ["3Buy", "2Buy"]  # 1Buy 在趋势中禁用（避免抄底思维）
      note: "3Buy 优先，趋势确认后离开中枢是最佳入场点"
  
  - BPB_P0_E:         # 突破回调
      priority: 2
      allowed_types: ["1st_pullback", "2nd_pullback"]
      note: "1st pullback 优先，2nd 限制（ callback_depth < 0.618 ）"
  
  - VP_P0_E:          # 成交量分布
      priority: 3
      allowed_types: ["VA_BREAKOUT_LONG", "POC_REGRESSION_BUY"]
      note: "VA 突破确认，POC 回归作为加仓点"
  
  - TKR7_P0_E:        # AO 背离
      priority: 4
      allowed_types: ["NONE"]  # 趋势中无背离，不触发信号
      note: "仅作为监控，出现背离时预警趋势可能结束"
  
  - MFLOW_P0_A:       # 资金流向
      priority: 5
      allowed_types: ["MAIN_FORCE_IN", "OPEN_RUSH_BUY"]
      note: "主力流入确认趋势，早盘抢筹增强信号"

# 风控参数：
risk_params:
  van_tharp_max_risk: 0.02
  kelly_mode: "half_kelly"  # 半凯利
  voltarget_target_vol: "normal"  # 根据市值分层
  
# 仓位策略：
position_strategy:
  - 单票上限: 0.20
  - 组合上限: 1.0
  - 加仓条件: "已有持仓盈利 + 回调缩量 + 领涨持续"
  - 减仓条件: "领涨示弱 或 出现 AO 背离预警"

# 退出条件：
exit_conditions:
  - "pq_state 从 ATTACK_SUSTAINED 转移到 POWER_TRANSITION 或 REMAINING_WARMTH"
  - "CHZL_BSD 发出 1Sell 或 3Sell"
  - "TKR7 出现常规顶背离（age < 5）"
  - "MFLOW 发出 MAIN_FORCE_OUT（主力出逃）"
```

### 3.2 BuildPosition — 建仓确认（ATTACK_CONFIRMED）

```yaml
strategy_name: "BuildPosition"
applicable_regime: "ATTACK_CONFIRMED"
permission: "FULL"
max_position_size: 0.7
entry_min_votes: 3

# 核心逻辑：
# 1. 阵型形成但可能刚启动或分期转移
# 2. 允许建仓，但比 ATTACK_SUSTAINED 略保守（max_position_size = 0.7）
# 3. 优先捕捉 2Buy（回测前低）和 2nd pullback（二次回调）

activated_objects:
  - CHZL_BSD_P0_E:
      priority: 1
      allowed_types: ["2Buy", "3Buy"]
      note: "2Buy 优先（回测前低），3Buy 作为突破确认"
  
  - BPB_P0_E:
      priority: 2
      allowed_types: ["2nd_pullback"]
      note: "2nd pullback 可交易（但 depth < 0.5 ）"
  
  - YTC_P0_E:
      priority: 3
      allowed_types: ["BPB", "TST"]
      note: "S/R 框架内的回测和测试入场"
  
  - MFLOW_P0_A:
      priority: 4
      allowed_types: ["MAIN_FORCE_IN", "MAIN_FORCE_OUT"]
      note: "主力流入增强建仓，主力流出阻断"

risk_params:
  van_tharp_max_risk: 0.02
  kelly_mode: "half_kelly"
  voltarget_target_vol: "normal"

position_strategy:
  - 单票上限: 0.15
  - 组合上限: 0.7
  - 建仓方式: "分批建仓（50% 先试，确认后加至 70%）"
  - 减仓条件: "领涨换人频繁 或 阵型瓦解"

exit_conditions:
  - "pq_state 转移到 ATTACK_UNSUSTAINED 或 POWER_TRANSITION"
  - "CHZL_BSD 发出 1Sell"
  - "MFLOW 连续 2 日 MAIN_FORCE_OUT"
```

### 3.3 TrialEntry — 试错建仓（GESTATION）

```yaml
strategy_name: "TrialEntry"
applicable_regime: "GESTATION"
permission: "REDUCED"
max_position_size: 0.3
entry_min_votes: 4  # 提高门槛，过滤噪音

# 核心逻辑：
# 1. 新周期启动但未确认，允许试错
# 2. 轻仓（10-30%），严格止损
# 3. 优先捕捉 1Buy（背驰抄底）和 BOF（突破失败反转）

activated_objects:
  - CHZL_BSD_P0_E:
      priority: 1
      allowed_types: ["1Buy"]
      note: "1Buy 优先（背驰抄底），2Buy/3Buy 禁用（趋势未确认）"
      stop_adjustment: "放宽止损（bi.low - 0.3ATR，孕化期波动大）"
  
  - YTC_P0_E:
      priority: 2
      allowed_types: ["BOF", "TST"]
      note: "突破失败反转（BOF）和测试入场（TST）"
  
  - BPB_P0_E:
      priority: 3
      allowed_types: ["1st_pullback"]
      note: "首次回调（但 volume_integrity_score > 0.7 ）"
      restrictions: "仅允许 1st pullback，2nd 禁用"
  
  - MFLOW_P0_A:
      priority: 4
      allowed_types: ["MAIN_FORCE_IN", "OPEN_RUSH_BUY"]
      note: "主力吸筹确认，早盘抢筹增强"

risk_params:
  van_tharp_max_risk: 0.01  # 更严格（1%）
  kelly_mode: "quarter_kelly"  # 四分之一凯利（更保守）
  voltarget_target_vol: "low"  # 目标波动率更低

position_strategy:
  - 单票上限: 0.05  # 单票最多 5%
  - 组合上限: 0.3
  - 建仓方式: "一次性试仓（不加仓）"
  - 止损: "严格止损（1.5ATR 或 3% 固定止损）"

exit_conditions:
  - "pq_state 转移到 REMAINING_WARMTH 或 ATTACK_UNSUSTAINED"
  - "CHZL_BSD 1Buy 止损触发"
  - "MFLOW 发出 MAIN_FORCE_OUT（主力流出）→ 立即退出"
  - "试错失败（3 日内无盈利）→ 强制退出"
```

### 3.4 WaitAndSee — 观望过渡（POWER_TRANSITION）

```yaml
strategy_name: "WaitAndSee"
applicable_regime: "POWER_TRANSITION"
permission: "REDUCED"
max_position_size: 0.3
entry_min_votes: 4  # 提高门槛

# 核心逻辑：
# 1. 交权磨合期，方向不明
# 2. 允许轻仓试错，但严格限制
# 3. 优先捕捉 TST（测试）和 2nd pullback（限制交易）

activated_objects:
  - YTC_P0_E:
      priority: 1
      allowed_types: ["TST"]
      note: "测试入场（TST），验证 S/R 有效性"
      restrictions: "ytc_srf_is_valid 必须 True"
  
  - BPB_P0_E:
      priority: 2
      allowed_types: ["2nd_pullback"]
      note: "2nd pullback（限制交易），callback_depth < 0.5"
      restrictions: "仅 2nd，1st 禁用（避免追涨）"
  
  - CHZL_BSD_P0_E:
      priority: 3
      allowed_types: ["2Buy"]
      note: "2Buy（回测前低），但 strength -2"
      restrictions: "signal_strength 最高 5"

risk_params:
  van_tharp_max_risk: 0.01
  kelly_mode: "quarter_kelly"
  voltarget_target_vol: "low"

position_strategy:
  - 单票上限: 0.05
  - 组合上限: 0.3
  - 建仓方式: "轻仓试探，不追趋势"
  - 止损: "严格止损（1.5ATR）"

exit_conditions:
  - "pq_state 转移到 ATTACK_UNSUSTAINED 或 REMAINING_WARMTH"
  - "任何对象卡发出反向信号"
  - "3 日内方向不明确 → 强制退出"
```

### 3.5 GradualExit — 逐步退出（REMAINING_WARMTH）

```yaml
strategy_name: "GradualExit"
applicable_regime: "REMAINING_WARMTH"
permission: "EXIT_ONLY"
max_position_size: 0.0
entry_min_votes: 2  # 降低门槛，方便退出

# 核心逻辑：
# 1. 余温阶段，末期惯性
# 2. 只减仓，不加仓（只出不进）
# 3. 优先捕捉 1Sell（背驰逃顶）和 AO 背离

activated_objects:
  - TKR7_P0_E:
      priority: 1
      allowed_types: ["REGULAR_TOP_DIVERGENCE", "HIDDEN_TOP_DIVERGENCE"]
      note: "顶背离优先（常规/隐藏），age < 5 时预警，age < 3 时强制退出"
      signal_strength_boost: "+1（余温期背离更可靠）"
  
  - CHZL_BSD_P0_E:
      priority: 2
      allowed_types: ["1Sell", "2Sell"]
      note: "1Sell（背驰确认）优先，2Sell（回测前高）辅助"
      restrictions: "所有 Buy 信号强制设为 NONE"
  
  - VOLTARGET_P0_R:
      priority: 3
      allowed_types: ["REDUCE_SIZE", "HALT_NEW"]
      note: "强制降仓，禁止新入场"
      scalar_override: "0.5"  # 强制减半

risk_params:
  van_tharp_max_risk: 0.02
  kelly_mode: "crisis"  # 危机模式
  voltarget_target_vol: "high"  # 高波动环境

position_strategy:
  - 单票上限: 0.0
  - 组合上限: 0.0
  - 操作: "只减仓，不新增"
  - 减仓节奏: "分批减仓（50% → 30% → 10% → 0%）"
  - 止损: "收紧止损（-0.2ATR，末期风险高）"

exit_conditions:
  - "pq_state 转移到 CUTTING_COMPLETE"
  - "TKR7 出现常规顶背离（任何 age）"
  - "CHZL_BSD 1Sell 确认"
  - "持仓全部清仓"
```

### 3.6 HoldCash — 空仓等待（ATTACK_UNSUSTAINED / CUTTING_COMPLETE）

```yaml
strategy_name: "HoldCash"
applicable_regime: ["ATTACK_UNSUSTAINED", "CUTTING_COMPLETE"]
permission: "HALT"
max_position_size: 0.0
entry_min_votes: 999  # 不可能达到，禁止任何新入场

# 核心逻辑：
# 1. 攻击无持续或切割完成，市场处于下降周期或真空期
# 2. 禁止任何新入场，仅处理已有持仓的止损
# 3. 所有对象卡禁用

activated_objects:
  - NONE  # 不激活任何 EXECUTION 对象卡

# 允许的风控操作：
allowed_risk_actions:
  - FORCE_CLOSE: "已有持仓风险突破 2% 时强制平仓"
  - STOP_LOSS: "正常止损执行"

position_strategy:
  - 操作: "持有现金，等待 pq_state 转移到 GESTATION 或 ATTACK_SUSTAINED"
  - 已有持仓: "正常止损，不新增"

exit_conditions:
  - "pq_state 转移到 GESTATION → 允许 TrialEntry"
  - "pq_state 转移到 ATTACK_SUSTAINED → 允许 TrendFollowing"
```

---

## 4. 三层决策流完整示例

### 示例 1：从孕化到趋势跟踪的完整决策链

```
Day 1：切割完成 → 孕化
  ┌──────────────────────────────────────────────────────┐
  │ 第一层：环境识别                                      │
  │   pq_state = CUTTING_COMPLETE                        │
  │   pq_trading_permission = HALT                       │
  │   → 第二层：HoldCash（空仓等待）                     │
  │   → 第三层：所有 EXECUTION 对象卡禁用                │
  └──────────────────────────────────────────────────────┘

Day 3：新面孔出现，持续 2 日
  ┌──────────────────────────────────────────────────────┐
  │ 第一层：环境识别                                      │
  │   pq_state = GESTATION                               │
  │   pq_trading_permission = REDUCED                  │
  │   pq_position_max_size = 0.3                         │
  │                                                      │
  │ 第二层：策略选择                                      │
  │   strategy_bundle = TrialEntry                     │
  │   激活对象卡：[CHZL_BSD(1Buy), YTC(BOF), BPB(1st)]  │
  │   entry_min_votes = 4                                │
  │                                                      │
  │ 第三层：执行管理                                      │
  │   对象卡计算：                                         │
  │     CHZL_BSD：1Buy，strength=7，stop=bi.low-0.3ATR  │
  │     YTC：BOF，strength=6                              │
  │     BPB：1st pullback，strength=5                   │
  │   互锁检查：                                           │
  │     CHZL_BSD × MFLOW：主力流入 → 增强（strength+1） │
  │   投票池：3 票（< 4）→ 不触发（门槛未达）           │
  │   → 不执行，继续观察                                 │
  └──────────────────────────────────────────────────────┘

Day 5：阵型形成，领涨持续
  ┌──────────────────────────────────────────────────────┐
  │ 第一层：环境识别                                      │
  │   pq_state = ATTACK_CONFIRMED                        │
  │   pq_trading_permission = FULL                       │
  │   pq_position_max_size = 0.7                         │
  │                                                      │
  │ 第二层：策略选择                                      │
  │   strategy_bundle = BuildPosition                    │
  │   激活对象卡：[CHZL_BSD(2Buy/3Buy), BPB(2nd), YTC]  │
  │   entry_min_votes = 3                                │
  │                                                      │
  │ 第三层：执行管理                                      │
  │   对象卡计算：                                         │
  │     CHZL_BSD：3Buy，strength=8                        │
  │     BPB：2nd pullback，strength=6                     │
  │     MFLOW：MAIN_FORCE_IN，strength=7                 │
  │   投票池：3 票（≥ 3）→ PASS                          │
  │   风控调制：                                           │
  │     Kelly：f*=0.18 → size_scalar=0.36（半凯利）    │
  │     VolTarget：当前波动率 12% < 目标 20% → scalar=1.33│
  │     PeriodQueen：max_size=0.7                         │
  │     最终 size_scalar = min(0.36, 1.33, 0.7) = 0.36  │
  │   执行：买入，仓位=0.36×标准仓位                     │
  └──────────────────────────────────────────────────────┘

Day 7：攻击有持续，领涨继续新高
  ┌──────────────────────────────────────────────────────┐
  │ 第一层：环境识别                                      │
  │   pq_state = ATTACK_SUSTAINED                        │
  │   pq_trading_permission = FULL                       │
  │   pq_position_max_size = 1.0                         │
  │                                                      │
  │ 第二层：策略选择                                      │
  │   strategy_bundle = TrendFollowing                   │
  │   激活对象卡：[CHZL_BSD(3Buy), BPB(1st), VP, MFLOW] │
  │   entry_min_votes = 3                                │
  │                                                      │
  │ 第三层：执行管理                                      │
  │   对象卡计算：                                         │
  │     CHZL_BSD：3Buy，strength=9                        │
  │     BPB：1st pullback，strength=8                     │
  │     VP：VA_BREAKOUT_LONG，strength=7                  │
  │     MFLOW：OPEN_RUSH_BUY，strength=7                  │
  │   投票池：4 票（≥ 3）→ PASS                          │
  │   风控调制：                                           │
  │     Kelly：f*=0.22 → size_scalar=0.44                │
  │     VolTarget：scalar=1.33                           │
  │     PeriodQueen：max_size=1.0                         │
  │     最终 size_scalar = min(0.44, 1.33, 1.0) = 0.44   │
  │   执行：加仓至 0.44×标准仓位                         │
  └──────────────────────────────────────────────────────┘
```

### 示例 2：从趋势跟踪到逐步退出的完整决策链

```
Day 10：领涨无法新高，出现顶背离
  ┌──────────────────────────────────────────────────────┐
  │ 第一层：环境识别                                      │
  │   pq_state = REMAINING_WARMTH                        │
  │   pq_trading_permission = EXIT_ONLY                  │
  │   pq_position_max_size = 0.0                         │
  │                                                      │
  │ 第二层：策略选择                                      │
  │   strategy_bundle = GradualExit                      │
  │   激活对象卡：[TKR7, CHZL_BSD(1Sell), VOLTARGET]     │
  │   entry_min_votes = 2（降低门槛，方便退出）          │
  │                                                      │
  │ 第三层：执行管理                                      │
  │   对象卡计算：                                         │
  │     TKR7：常规顶背离，strength=9，age=3              │
  │     CHZL_BSD：1Sell，strength=8                      │
  │   投票池：2 票（≥ 2）→ PASS（退出策略门槛=2）       │
  │   风控调制：                                           │
  │     VOLTARGET：强制 scalar=0.5（降仓 50%）          │
  │     Kelly：危机模式 → 不新增，只处理现有持仓         │
  │   执行：减仓 50%（卖出持仓的一半）                   │
  └──────────────────────────────────────────────────────┘

Day 12：切割完成，空仓
  ┌──────────────────────────────────────────────────────┐
  │ 第一层：环境识别                                      │
  │   pq_state = CUTTING_COMPLETE                        │
  │   pq_trading_permission = HALT                       │
  │   pq_position_max_size = 0.0                         │
  │                                                      │
  │ 第二层：策略选择                                      │
  │   strategy_bundle = HoldCash                         │
  │   激活对象卡：NONE                                    │
  │                                                      │
  │ 第三层：执行管理                                      │
  │   执行：剩余持仓全部止损/止盈，持有现金              │
  │   等待 pq_state 转移到 GESTATION                     │
  └──────────────────────────────────────────────────────┘
```

---

## 5. 对象卡激活矩阵

### 5.1 按 regime_state 的对象卡激活表

| 对象卡 | ATTACK_SUS | ATTACK_CONF | POWER_TRANS | REMAINING_WARMTH | ATTACK_UNSUS | CUTTING_COMPLETE | GESTATION |
|--------|-----------|-------------|-------------|------------------|-------------|------------------|-----------|
| **CHZL_BSD** | 3Buy,2Buy | 2Buy,3Buy | 2Buy(strength-2) | 1Sell,2Sell | 禁用 | 禁用 | 1Buy |
| **BPB** | 1st,2nd | 2nd | 2nd(限制) | 禁用 | 禁用 | 禁用 | 1st(限制) |
| **VP** | VA突破,POC回归 | VA突破 | 禁用 | 禁用 | 禁用 | 禁用 | 禁用 |
| **TKR7** | 监控(无信号) | 监控 | 禁用 | 顶背离 | 禁用 | 禁用 | 禁用 |
| **YTC** | BPB | BPB,TST | TST | 禁用 | 禁用 | 禁用 | BOF,TST |
| **MFLOW** | 主力流入,早盘抢筹 | 主力流入 | 监控 | 主力流出(预警) | 禁用 | 禁用 | 主力吸筹 |
| **VOLFAC** | 正常 | 正常 | 正常 | 高波动降仓 | 正常 | 正常 | 正常 |
| **VOLTARGET** | 正常 | 正常 | 正常 | 强制scalar=0.5 | 正常 | HALT_NEW | 正常 |
| **KELLY** | 半凯利 | 半凯利 | 四分之一凯利 | 危机模式 | 危机模式 | 危机模式 | 四分之一凯利 |
| **Van Tharp** | 2% | 2% | 1% | 2% | 2% | 2% | 1% |

### 5.2 按 regime_state 的投票门槛

| regime_state | entry_min_votes | 说明 |
|--------------|----------------|------|
| ATTACK_SUSTAINED | 3 | 正常门槛 |
| ATTACK_CONFIRMED | 3 | 正常门槛 |
| POWER_TRANSITION | 4 | 提高门槛，过滤噪音 |
| REMAINING_WARMTH | 2 | 降低门槛，方便退出 |
| ATTACK_UNSUSTAINED | 999 | 禁止任何新入场 |
| CUTTING_COMPLETE | 999 | 禁止任何新入场 |
| GESTATION | 4 | 提高门槛，过滤噪音 |

### 5.3 按 regime_state 的仓位上限

| regime_state | max_position_size | 单票上限 | 说明 |
|--------------|------------------|----------|------|
| ATTACK_SUSTAINED | 1.0 | 0.20 | 标准仓位（Kelly优化） |
| ATTACK_CONFIRMED | 0.7 | 0.15 | 建仓仓位（分批） |
| POWER_TRANSITION | 0.3 | 0.05 | 试仓仓位（轻仓） |
| REMAINING_WARMTH | 0.0 | 0.00 | 只出不进 |
| ATTACK_UNSUSTAINED | 0.0 | 0.00 | 空仓 |
| CUTTING_COMPLETE | 0.0 | 0.00 | 空仓 |
| GESTATION | 0.3 | 0.05 | 试仓仓位（严格止损） |

---

## 6. 与纲领的接口定义

### 6.1 第一层 → 第二层接口

```python
# PERIOD_QUEEN 输出 → STRATEGY_BUNDLES 输入
interface_layer1_to_layer2 = {
    "pq_state": str,                    # 周期状态
    "pq_state_confidence": float,       # 状态置信度
    "pq_trading_permission": str,       # 交易权限
    "pq_position_max_size": float,      # 仓位上限
    "pq_entry_min_votes_adjusted": int, # 调整后的投票门槛
    "pq_strategy_bundle": str,          # 策略组合名称
    "pq_allowed_objects": list,         # 允许的对象卡列表
    "pq_forbidden_objects": list,       # 禁止的对象卡列表
}
```

### 6.2 第二层 → 第三层接口

```python
# STRATEGY_BUNDLES 输出 → EXECUTION 输入
interface_layer2_to_layer3 = {
    "strategy_bundle": str,             # 策略组合名称
    "activated_objects": list,          # 激活的对象卡及其参数
    "entry_min_votes": int,             # 投票门槛
    "risk_params": dict,              # 风控参数
    "position_strategy": dict,        # 仓位策略
    "exit_conditions": list,          # 退出条件
}
```

### 6.3 第三层 → 交易执行接口

```python
# EXECUTION 输出 → 最终交易信号
interface_layer3_to_trade = {
    "final_signal_type": str,           # LONG / SHORT / ABORT
    "final_signal_strength": int,       # 0-10
    "final_size_scalar": float,         # 最终仓位缩放
    "final_stop_adjustment": float,     # 止损调整
    "triggered_objects": list,          # 触发本次交易的对象卡
    "regime_state": str,                # 当时的周期状态
    "strategy_bundle": str,             # 使用的策略组合
}
```

---

## 7. 对编程 AI 的实现要求

### 7.1 策略组合引擎

```python
class StrategyBundleEngine:
    """
    策略组合引擎：根据 regime_state 选择策略组合，激活对象卡，调整参数
    """
    
    def __init__(self, config_file="STRATEGY_BUNDLES_v1.0.yaml"):
        self.bundles = self._load_bundles(config_file)
    
    def select_bundle(self, pq_state, pq_confidence):
        """
        根据周期状态选择策略组合
        
        参数:
            pq_state: 周期状态（来自 PERIOD_QUEEN）
            pq_confidence: 状态置信度
        
        返回:
            strategy_bundle: dict with activated_objects, entry_min_votes, risk_params, etc.
        """
        # 如果置信度 < 0.3，降级到更保守的状态
        if pq_confidence < 0.3:
            pq_state = self._degrade_state(pq_state)
        
        return self.bundles[pq_state]
    
    def _degrade_state(self, pq_state):
        """状态降级：不确定时选择更保守的状态"""
        degrade_map = {
            "ATTACK_SUSTAINED": "ATTACK_CONFIRMED",
            "ATTACK_CONFIRMED": "POWER_TRANSITION",
            "POWER_TRANSITION": "ATTACK_UNSUSTAINED",
            "GESTATION": "ATTACK_UNSUSTAINED",
            "REMAINING_WARMTH": "ATTACK_UNSUSTAINED",
            # ATTACK_UNSUSTAINED 和 CUTTING_COMPLETE 已是最保守，不再降级
        }
        return degrade_map.get(pq_state, pq_state)
    
    def filter_objects(self, all_objects, allowed_objects, forbidden_objects):
        """
        根据允许/禁止列表过滤对象卡
        """
        filtered = []
        for obj in all_objects:
            if obj.object_id in forbidden_objects:
                obj.signal_type = "NONE"  # 强制禁用
            elif obj.object_id in allowed_objects:
                filtered.append(obj)
        return filtered
```

### 7.2 仓位调制器

```python
class PositionModulator:
    """
    仓位调制器：整合三层风控（Kelly + VolTarget + PeriodQueen）
    """
    
    def calculate_final_size(self, kelly_scalar, voltarget_scalar, pq_max_size):
        """
        最终仓位 = min(Kelly, VolTarget, PeriodQueen_max)
        """
        return min(kelly_scalar, voltarget_scalar, pq_max_size)
    
    def adjust_for_regime(self, base_size, pq_state):
        """
        根据状态额外调整仓位
        """
        adjustments = {
            "ATTACK_SUSTAINED": 1.0,
            "ATTACK_CONFIRMED": 0.7,
            "POWER_TRANSITION": 0.3,
            "GESTATION": 0.3,
            "REMAINING_WARMTH": 0.0,  # 只出不进
            "ATTACK_UNSUSTAINED": 0.0,
            "CUTTING_COMPLETE": 0.0,
        }
        return base_size * adjustments.get(pq_state, 0.0)
```

---

> 文件：STRATEGY_BUNDLES_v1.0.md  
> 生产者：Kimi  
> 状态：纲领配套文档，与 PERIOD_QUEEN 对象卡和 SYSTEM_ARCHITECTURE_DRAFT 配合使用  
> 核心交付：
> - 7 个策略组合的详细定义（对象卡激活列表、风控参数、仓位策略、退出条件）
> - 对象卡激活矩阵（按 regime_state 的完整表格）
> - 投票门槛和仓位上限的完整映射
> - 三层决策流的完整示例（从孕化到趋势跟踪，从趋势跟踪到退出）
> - 对编程 AI 的实现要求（StrategyBundleEngine + PositionModulator）
