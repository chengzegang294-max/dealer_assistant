# 交易系统纲领：三层决策架构 v1.0

> 目标：将碎片化的对象卡、素材、规则统一到一个决策链中
> 核心思想：不同来源的碎片不是竞争者，而是同一决策链上的不同环节

---

## 1. 问题诊断：为什么碎片需要纲领

当前仓库有：
- 12+ 张对象卡（缠论、KD、VP、BPB、YTC、TK、Kelly、VolTarget、MFLOW、VOLFAC）
- 周期女王七态情绪周期
- 原子规则表 263 条（GAS 12 指标）
- AL Brooks 20 形态
- 大隐体系（时空波浪、二维时空）
- A 股竞价规则 25 条
- 经典书籍（Van Tharp、海龟、墨菲、Kaufman）

**问题**：每个碎片都回答"怎么看市场"，但没有一个框架回答"在什么状态下用什么工具看"。结果是：
- 攻击有持续时，缠论 3Buy 和 BPB 1st pullback 可能同时触发，谁优先？
- 余温阶段，AO 背离是退出信号还是做空信号？（A 股纯多头不能做空）
- 交权磨合期，所有对象卡都发信号，但此时应该观望还是轻仓试错？

**纲领的作用**：给每个碎片分配一个"决策环节"，让它们在正确的环节发挥作用。

---

## 2. 三层决策架构

```
┌─────────────────────────────────────────────────────────────────────┐
│ 第一层：环境识别（Market Regime）                                   │
│ 回答：当前市场处于什么状态？该不该交易？                            │
│                                                                     │
│ 输入：周期女王七态 + 波动率状态 + 缠论走势类型 + KD 多周期对齐       │
│ 输出：regime_state（交易状态机）                                    │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ 周期女王     │  │ VOLFAC       │  │ 缠论趋势     │             │
│  │ 七态         │  │ 波动率状态   │  │ 走势类型     │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│         │                │                │                         │
│         ▼                ▼                ▼                         │
│  ┌──────────────────────────────────────────────────────┐          │
│  │  regime_state:                                       │          │
│  │    - ATTACK_SUSTAINED（攻击有持续）→ 允许趋势跟踪    │          │
│  │    - ATTACK_CONFIRMED（确认攻击）→ 允许建仓          │          │
│  │    - POWER_TRANSITION（交权磨合）→ 观望/轻仓试错     │          │
│  │    - REMAINING_WARMTH（余温）→ 只减仓，不加仓        │          │
│  │    - ATTACK_UNSUSTAINED（攻击无持续）→ 禁止新入场    │          │
│  │    - CUTTING_COMPLETE（切割完成）→ 空仓/等待孕化    │          │
│  │    - GESTATION（孕化）→ 允许试错建仓                  │          │
│  └──────────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼ regime_state 注入
┌─────────────────────────────────────────────────────────────────────┐
│ 第二层：策略选择（Strategy Selection）                              │
│ 回答：用什么策略组合？在哪里交易？                                    │
│                                                                     │
│ 输入：regime_state + 对象卡信号池                                   │
│ 输出：strategy_bundle（策略组合）+ target_objects（激活对象卡列表）    │
│                                                                     │
│  根据 regime_state 激活不同对象卡组合：                              │
│                                                                     │
│  regime_state = ATTACK_SUSTAINED:                                   │
│    → 策略 = "趋势跟踪"                                              │
│    → 激活对象卡 = [CHZL_BSD(3Buy), BPB(1st), VP(VA突破), MFLOW(确认)]│
│    → 仓位 = 标准（Kelly 优化 + VolTarget 调制）                     │
│                                                                     │
│  regime_state = REMAINING_WARMTH:                                   │
│    → 策略 = "逐步退出"                                              │
│    → 激活对象卡 = [TKR7(AO背离), CHZL_BSD(1Sell), VOLTARGET(降仓)] │
│    → 仓位 = 减仓（只出不进）                                        │
│                                                                     │
│  regime_state = POWER_TRANSITION:                                   │
│    → 策略 = "观望/轻仓试错"                                         │
│    → 激活对象卡 = [YTC(TST), BPB(2nd限制), 低仓位]                   │
│    → 仓位 = 试仓（10-30%）                                          │
│                                                                     │
│  regime_state = GESTATION:                                          │
│    → 策略 = "试错建仓"                                              │
│    → 激活对象卡 = [CHZL_BSD(1Buy), YTC(BOF), MFLOW(吸筹确认)]       │
│    → 仓位 = 试仓（10-30%）                                          │
│                                                                     │
│  regime_state = ATTACK_UNSUSTAINED / CUTTING_COMPLETE:              │
│    → 策略 = "禁止新入场"                                            │
│    → 激活对象卡 = [无]                                              │
│    → 仓位 = 0（仅处理已有持仓止损）                                 │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼ strategy_bundle 注入
┌─────────────────────────────────────────────────────────────────────┐
│ 第三层：执行管理（Execution Management）                            │
│ 回答：下多少？什么时候执行？                                          │
│                                                                     │
│ 输入：strategy_bundle + 所有激活对象卡的信号                          │
│ 输出：final_trade_signal（最终交易信号）                            │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ 互锁检查     │  │ 投票融合     │  │ 风控调制     │             │
│  │ 对象卡间     │  │ entry_min_votes│  │ 三层风控     │             │
│  │ 冲突/共振    │  │ = 3          │  │ VanTharp/Kelly│            │
│  └──────────────┘  │ /VolTarget   │  └──────────────┘             │
│         │           └──────────────┘                                │
│         │                    │                                       │
│         ▼                    ▼                                       │
│  ┌──────────────────────────────────────────────────────┐          │
│  │  final_trade_signal:                                   │          │
│  │    - symbol, direction, entry_price, stop_loss       │          │
│  │    - position_size（由风控层调制后的最终仓位）       │          │
│  │    - triggered_objects（触发本次交易的对象卡列表）    │          │
│  │    - regime_state（当时的市场状态）                   │          │
│  │    - strategy_bundle（使用的策略组合）               │          │
│  └──────────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. 纲领与现有对象卡的关系

### 3.1 第一层：环境识别（现有对象卡在此层的角色）

| 对象卡 | 在环境识别层的角色 | 输出字段 |
|--------|-------------------|----------|
| **周期女王**（待创建） | **核心状态机**：七态决定整个系统的交易权限 | `regime_state` |
| VOLFAC | 波动率环境：高波动时所有策略降级，低波动时允许加仓 | `volfac_vol_regime` |
| 缠论趋势（CHZL_TREND） | 结构环境：趋势/盘整决定策略方向 | `chzl_trend_type` |
| KD MTF | 多周期对齐：周期冲突时观望，对齐时确认 | `kd_alignment_tier` |
| YTC S/R | 框架有效性：S/R 无效时所有 YTC 信号不激活 | `ytc_srf_is_valid` |
| MFLOW（宏观） | 资金环境：主力整体流出时进入防御模式 | `mflow_market_sentiment` |

### 3.2 第二层：策略选择（现有对象卡在此层的角色）

| 策略 | regime_state | 激活对象卡 | 仓位策略 |
|------|-------------|-----------|---------|
| 趋势跟踪 | ATTACK_SUSTAINED | CHZL_BSD(3Buy), BPB(1st), VP(VA突破), TKR7(确认), MFLOW(确认) | 标准（Kelly优化） |
| 建仓确认 | ATTACK_CONFIRMED | CHZL_BSD(2Buy), BPB(2nd), YTC(BPB), MFLOW(流入) | 标准（50-70%） |
| 试错建仓 | GESTATION | CHZL_BSD(1Buy), YTC(BOF), BPB(1st限制), MFLOW(吸筹) | 试仓（10-30%） |
| 逐步退出 | REMAINING_WARMTH | TKR7(AO背离), CHZL_BSD(1Sell), VOLTARGET(降仓) | 减仓（只出不进） |
| 轻仓试错 | POWER_TRANSITION | YTC(TST), BPB(2nd限制), 低仓位 | 试仓（10-30%） |
| 禁止新入场 | ATTACK_UNSUSTAINED / CUTTING_COMPLETE | 无 | 0（仅止损） |
| 空仓等待 | 其他 | 无 | 0 |

### 3.3 第三层：执行管理（现有对象卡在此层的角色）

| 对象卡 | 在执行管理层的角色 | 输出字段 |
|--------|-------------------|----------|
| Van Tharp（硬性上限） | **绝对否决**：任何交易若导致单票风险 > 2% → 强制 ABORT | `risk_action=FORCE_CLOSE` |
| Kelly | 动态优化：根据历史胜率调整仓位 | `size_scalar` |
| VolTarget | 环境调制：高波动时降仓，低波动时允许加仓 | `vt_size_scalar` |
| 互锁引擎 | 冲突检测：对象卡间冲突时降级/阻断 | `lock_status=CONFLICT` |
| 投票池 | 信号融合：≥3 票通过才能执行 | `final_signal_type` |

---

## 4. 决策流程示例

### 示例 1：攻击有持续 → 趋势跟踪

```
步骤 1（环境识别）：
  周期女王：攻击有持续（前一天领涨持续，阵型不散）
  VOLFAC：NORMAL_VOL（正常波动，20-80%分位）
  缠论趋势：上升趋势（离开中枢后不回抽）
  KD MTF：alignment_tier = s（三周期对齐）
  → regime_state = ATTACK_SUSTAINED
  → 交易权限：允许趋势跟踪，标准仓位

步骤 2（策略选择）：
  激活对象卡：[CHZL_BSD, BPB, VP, TKR7, MFLOW]
  策略 = "趋势跟踪"
  对象卡输出：
    - CHZL_BSD：3Buy，strength=8，stop=zs.zd-0.1ATR
    - BPB：1st pullback，strength=7，callback_depth=0.382
    - VP：VA_BREAKOUT_LONG，strength=6
    - TKR7：无背离（趋势中无背离），strength=0
    - MFLOW：MAIN_FORCE_IN，strength=8

步骤 3（执行管理）：
  互锁检查：
    - CHZL_BSD × MFLOW：主力流入确认 3Buy → 增强（strength +1）
    - BPB × VP：VA 突破确认回调 → 增强
    - TKR7：无信号，不参与投票
  投票池：
    - CHZL_BSD(8) + BPB(7) + VP(6) + MFLOW(8) = 4 票 ≥ 3 → PASS
  风控调制：
    - Van Tharp：单票风险 < 2% → PASS
    - Kelly：历史胜率 45% → f*=0.18 → size_scalar=0.36（半凯利）
    - VolTarget：当前波动率 15% < 目标 20% → scalar=1.33
    - 最终 size_scalar = min(0.36, 1.33) = 0.36
  最终信号：
    - direction=LONG，entry_price=当前价，stop_loss=zs.zd-0.1ATR
    - position_size=0.36×标准仓位，triggered_objects=[CHZL_BSD,BPB,VP,MFLOW]
    - regime_state=ATTACK_SUSTAINED，strategy_bundle=趋势跟踪
```

### 示例 2：余温 → 逐步退出

```
步骤 1（环境识别）：
  周期女王：余温（高位反复，末期惯性，名牌归一）
  VOLFAC：HIGH_VOL（波动率 > 80%分位）
  缠论趋势：趋势末期（背驰后未确认反转）
  KD MTF：周线 OVERBOUGHT
  → regime_state = REMAINING_WARMTH
  → 交易权限：只减仓，不加仓

步骤 2（策略选择）：
  激活对象卡：[TKR7, CHZL_BSD, VOLTARGET]
  策略 = "逐步退出"
  对象卡输出：
    - TKR7：常规顶背离，strength=9，age=3
    - CHZL_BSD：1Sell（背驰确认），strength=8
    - VOLTARGET：HIGH_VOL → scalar=0.5

步骤 3（执行管理）：
  互锁检查：
    - TKR7 × CHZL_BSD：AO 背离 + 缠论背驰 → 双重确认
    - VOLTARGET：高波动强制降仓 → size_scalar=0.5
  投票池：
    - TKR7(9) + CHZL_BSD(8) = 2 票（< 3）
    - 但 regime_state = REMAINING_WARMTH 时，退出策略的投票门槛降低为 ≥ 2
    - 2 票 ≥ 2 → PASS（退出策略的特殊规则）
  风控调制：
    - Van Tharp：已有持仓风险检查 → 若 > 2% 强制减仓
    - Kelly：不调整（退出信号不需要 Kelly）
    - VolTarget：HIGH_VOL → 强制减仓 50%
  最终信号：
    - direction=SELL（减仓），position_size=现有持仓 × 0.5
    - triggered_objects=[TKR7, CHZL_BSD, VOLTARGET]
    - regime_state=REMAINING_WARMTH，strategy_bundle=逐步退出
```

---

## 5. 纲领与素材库的关系

### 5.1 周期女王体系 → 第一层（环境识别）

```text
周期女王七态是核心状态机：
- 不是信号源，而是"交易权限开关"
- 每个状态定义：允许什么策略、激活什么对象卡、仓位上限是多少
- 状态转换规则：基于可观测证据（如"攻击阵型是否持续""是否有真风雨切割"）

状态转换图：
  ATTACK_SUSTAINED ──[持续失效]──► ATTACK_UNSUSTAINED
         │                              │
         ▼[进入末期]                    ▼[切割条件触发]
  REMAINING_WARMTH ◄──[惯性]───       CUTTING_COMPLETE
         │                              │
         ▼[新面孔尝试]                  ▼[新周期启动]
  GESTATION ◄──[确认成功]─── ATTACK_CONFIRMED
         │                              ▲
         ▼[磨合失败]                    │[形成阵型]
  POWER_TRANSITION ──[确认成功]────────┘
```

### 5.2 原子规则表（GAS 12 指标）→ 第二层（策略内）

```text
GAS 指标不是独立对象卡，而是嵌入策略的"评分组件"：

在"趋势跟踪"策略中：
- 明镜非台：多指标共振评分 ≥ 3 分 → 增强信号
- 八字箴言：动量确认 → 增强信号
- 五里趋势：DIFF 金叉 + 拐点 → 入场时机
- 循环往复：趋势强度评分 0-3 分 → 仓位映射

在"反转/退出"策略中：
- 否极泰来：顶底背离 → 反转信号
- 物极必反：RSI 超买超卖 → 极端状态确认
- 高山低谷：波峰波谷 → 目标止盈位

处理原则：
- GAS 指标中已有对应对象卡的（如 KD、MACD、成交量）→ 用现有对象卡，GAS 参数作为参考
- GAS 指标中独有的（如五里神马、八字箴言）→ 作为策略内的"评分组件"，不单独创建对象卡
```

### 5.3 AL Brooks 20 形态 → 第二层（BPB 子类型）

```text
AL Brooks 20 形态是 BPB 的细化：
- BPB 对象卡已定义：突破质量、回调深度、1st/2nd 限制
- 20 形态补充：具体的入场形态枚举（M1-M20）

在"趋势跟踪"策略中：
- M1（EMA 突破）、M4（EMA 旗形）、M8（突破回调）→ 与 BPB 1st pullback 对应
- M3（EMA 二次测试）、M9（双底）→ 与 CHZL_BSD 2Buy 对应

在"反转/退出"策略中：
- M13（高潮反转）、M11（三重推动）→ 与 TKR7 AO 背离对应
- M14（区间突破反转）→ 与 YTC BOF 对应

处理原则：
- 不创建新对象卡，而是在 BPB 对象卡中增加 `bpb_sub_type` 字段（M1-M20）
- 策略选择时，根据 regime_state 选择允许的形态子集
```

### 5.4 大隐体系 → 第一层/第二层

```text
大隐体系的 DY_R1（多周期 KD）→ 已有对象卡，归入 KD MTF
大隐体系的 DY_R2（时空波浪）→ 结构层，与缠论走势类型重叠
  - 建议：作为缠论走势类型的补充，不单独创建对象卡
大隐体系的 DY_R3（交易策略）→ 第二层，作为策略模板
  - 建议：将 DY_R3 的交易规则转化为策略选择逻辑
```

### 5.5 A 股竞价规则 → 第一层（早盘环境）

```text
A 股竞价规则是 MFLOW 的早盘细分：
- 9:15-9:20 可撤单（假单诱导）→ mflow_open_intent 谨慎解读
- 9:20-9:25 不可撤单（更真实）→ mflow_open_intent 可信度提高
- 白点未匹配量、红绿柱 → 早盘情绪判断
- 9:25 真实成交 → 早盘意图确认

处理原则：
- 不创建新对象卡，而是作为 MFLOW 对象卡的 `mflow_open_intent` 字段的细化规则
- 在"试错建仓"策略中，早盘抢筹（STRONG_BUY）增强信号
- 在"逐步退出"策略中，早盘抛售（STRONG_SELL）加速退出
```

### 5.6 经典书籍 → 第一层/第三层

```text
Van Tharp → 第三层（风控硬性上限）
  - 已有对象卡：Van Tharp 2% 硬性上限

海龟交易法则 → 第二层（突破策略）
  - 与 BPB 和 Turtle 对象卡重叠
  - 建议：作为 BPB 策略的一个子类型

墨菲 → 第一层（趋势定义）
  - 与缠论趋势类型和 KD MTF 重叠
  - 建议：作为趋势判定的辅助参考

Kaufman → 第三层（适应性系统）
  - 与 VolTarget 的 adaptive 模式重叠
  - 建议：作为 VolTarget 的参考参数
```

---

## 6. 纲领的扩展性

这个三层架构可以容纳未来新增的任何素材：

```text
新增素材 → 判断归属 → 插入对应层

1. 新增情绪/周期/状态素材 → 第一层（环境识别）
   例如：你拿到一个新的情绪周期课程 → 作为周期女王七态的补充或替代状态机

2. 新增技术信号/入场方法素材 → 第二层（策略选择）
   例如：你拿到 Wyckoff 积累派发课程 → 作为"试错建仓"策略的一个对象卡

3. 新增风控/仓位管理素材 → 第三层（执行管理）
   例如：你拿到一个新的资金管理方法 → 作为 Kelly 的替代或补充

4. 新增选股因子素材 → 第二层（策略选择）的选股层
   例如：你拿到新的 S_BUCKET 研报 → 提取因子，作为 MFLOW/VOLFAC 的补充

处理原则：
- 新增素材必须先回答：它属于哪一层？它回答什么决策问题？
- 如果无法明确归属，先放入"方法层"（不干预执行，只作为参考）
- 如果与现有对象卡重叠，补充到现有对象卡，不创建新对象卡
```

---

## 7. 下一步：将纲领落实为可运行系统

### 7.1 需要创建的新对象卡

| 对象卡 | 功能层 | 必要性 | 说明 |
|--------|--------|--------|------|
| **PERIOD_QUEEN_P0_F** | FILTER | **核心** | 周期女王七态状态机，统领整个系统 |
| **DY_R3_P0_E** | EXECUTION | 高 | 大隐交易策略，作为策略模板 |

### 7.2 需要补充的现有对象卡

| 对象卡 | 补充字段 | 说明 |
|--------|----------|------|
| BPB | `bpb_sub_type`（M1-M20） | AL Brooks 形态枚举 |
| MFLOW | `mflow_open_intent` 细化规则 | A 股竞价规则 |
| KD_MTF | 验证与 DY_R1 的字段一致性 | 大隐体系整合 |
| CHZL_TREND | 与 DY_R2 的映射 | 时空波浪补充 |

### 7.3 需要编写的新文档

| 文档 | 用途 |
|------|------|
| `STRATEGY_BUNDLES_v1.0.md` | 定义每个 regime_state 对应的策略组合和对象卡激活列表 |
| `REGIME_TRANSITION_RULES_v1.0.md` | 定义周期女王七态之间的转换条件和可观测证据 |
| `PERIOD_QUEEN_P0_F__CycleStateSystem_v1.0.md` | 周期女王对象卡（字段冻结） |

---

> 文件：SYSTEM_ARCHITECTURE_DRAFT.md  
> 生产者：Kimi  
> 状态：纲领设计阶段，定义三层决策架构和碎片归属  
> 核心交付：
> - 周期女王七态 → 第一层（环境识别状态机）
> - 所有技术对象卡 → 第二层（策略选择，按状态激活）
> - 所有风控对象卡 → 第三层（执行管理，投票+风控）
> - GAS/AL Brooks/大隐/竞价/经典书籍 → 各层内的组件或参数
