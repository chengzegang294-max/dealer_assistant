# PERIOD_QUEEN_P0_F — 周期状态系统（Cycle State System）对象卡

> 功能层：P0_F（过滤器 / 环境识别）  
> 成熟度：proxy_quantizable_now（需要 10 日区间涨幅榜数据，A 股已普及）  
> 生产者：Kimi（基于周期女王规则壳 v1.0 字段化）  
> 来源：万法归一系统课程 20240122–20240331 逐字稿  
> 状态：已冻结核心字段，作为系统第一层（环境识别）的核心状态机

---

## 1. 基本定义

周期状态系统（Cycle State System）是基于 A 股情绪周期的**环境过滤器**。它回答的核心问题是：**当前市场处于什么情绪状态？该不该交易？**  

**核心洞察**：A 股的情绪周期不是线性涨跌，而是**七态循环**：攻击有持续 → 确认攻击 → 交权磨合期 → 余温 → 攻击无持续 → 切割完成 → 孕化 → 回到攻击有持续。每个状态有明确的交易权限和禁忌。

**与现有对象卡的关系**：
- 周期女王不是信号源（不生成买卖信号），而是**交易权限开关**（regime_state）
- 它决定第二层（策略选择）激活哪些对象卡、允许什么仓位、禁止什么行为
- 所有执行层对象卡（CHZL_BSD、BPB、VP、TKR7 等）的投票结果，只有在周期女王允许交易的状态下才能触发执行

---

## 2. 核心概念与字段冻结

### 2.1 七态状态机（已冻结）

```text
pq_state                    ENUM    -- 周期状态（核心输出）：
                                        -- 'ATTACK_SUSTAINED' = 攻击有持续（上涨周期，允许趋势跟踪）
                                        -- 'ATTACK_CONFIRMED' = 确认攻击（阵型形成，允许建仓）
                                        -- 'POWER_TRANSITION' = 交权磨合期（过渡阶段，观望/轻仓试错）
                                        -- 'REMAINING_WARMTH' = 余温（末期惯性，只减仓不加仓）
                                        -- 'ATTACK_UNSUSTAINED' = 攻击无持续（下降周期，禁止新入场）
                                        -- 'CUTTING_COMPLETE' = 切割完成（空仓等待，禁止一切交易）
                                        -- 'GESTATION' = 孕化（新周期启动，允许试错建仓）

pq_state_prev               ENUM    -- 上一周期状态（用于判断状态转移方向）

pq_state_duration           INT     -- 当前状态持续天数（状态切换后重新计数）

pq_state_confidence         FLOAT(0-1)  -- 状态识别置信度：
                                            -- 0.0-0.3 = 状态模糊，可能误判
                                            -- 0.3-0.7 = 状态基本清晰，但有噪音
                                            -- 0.7-1.0 = 状态高度确认
                                            -- 状态模糊时，默认降级到更保守的状态

pq_transition_trigger       STRING  -- 触发本次状态转移的原因简述
```

### 2.2 状态识别核心指标（可观测证据）

```text
pq_leading_stock            STRING  -- 当前领涨个股（10日区间涨幅榜前十个，涨停时间最早者）
pq_leading_stock_sustained  BOOL    -- 领涨是否持续：前交易日领涨今日是否继续涨/涨停
pq_leading_stock_new_high   BOOL    -- 领涨是否创新高（收盘价）

pq_space_board_sustained    BOOL    -- 空间板是否持续：前交易日空间板今日是否继续涨
pq_space_board_count        INT     -- 当前空间板高度（连板数）

pq_attack_formation_count   INT   -- 攻击阵型个股数（10日区间涨幅榜前十个中，协同上涨的个股数）
pq_attack_formation_valid   BOOL    -- 攻击阵型是否有效：≥3-4只个股协同，且前交易日领涨+空间板双持续

pq_tolerance_exist          BOOL    -- 包容度是否存在：失败个股（炸板/断板）次日是否有修复（地天板/反包）
pq_tolerance_score          FLOAT(0-1)  -- 包容度评分：前十个中有修复的个股比例

pq_tide_force_exist         BOOL    -- 退潮力量是否存在：头部个股是否持续跌/A杀
pq_tide_force_score           FLOAT(0-1)  -- 退潮力量评分：前十个中下跌个股比例

pq_ten_day_rank[]           ARRAY<STRING>  -- 10日区间涨幅榜前十个（主板10cm，每日更新）
pq_ten_day_rank_change      INT     -- 较上一日排名变化数（换人数）

pq_cutting_condition_met    BOOL    -- 切割条件是否满足：
                                        -- 条件1：上一龙领涨直接A杀持续跌
                                        -- 条件2：每天杀一个空间板（连续3-4个）
                                        -- 满足其一即切割完成

pq_gestation_new_faces      INT     -- 孕化阶段新面孔数（完成切割后，尝试上涨的新个股数）
pq_gestation_new_faces_sustained  BOOL  -- 新面孔是否持续（至少2日）
```

### 2.3 交易权限字段（已冻结）

```text
pq_trading_permission       ENUM    -- 交易权限：
                                        -- 'FULL' = 允许交易（标准仓位）
                                        -- 'REDUCED' = 允许交易（减仓/试仓）
                                        -- 'EXIT_ONLY' = 只减仓，不加仓（只出不进）
                                        -- 'HALT' = 禁止新入场（仅处理已有持仓）

pq_position_max_size        FLOAT   -- 最大仓位比例（0.0-1.0）：
                                        -- FULL = 1.0（Kelly优化后的标准仓位）
                                        -- REDUCED = 0.3（试仓，10-30%）
                                        -- EXIT_ONLY = 0.0（只出不进，已有持仓正常止损）
                                        -- HALT = 0.0（禁止任何新仓位）

pq_strategy_bundle          STRING  -- 当前状态对应的策略组合名称
                                        -- 与 STRATEGY_BUNDLES_v1.0.md 中的策略名对应

pq_allowed_objects[]        ARRAY<STRING>  -- 当前状态允许激活的对象卡列表
pq_forbidden_objects[]      ARRAY<STRING>  -- 当前状态禁止激活的对象卡列表

pq_entry_min_votes_adjusted  INT    -- 调整后的投票门槛：
                                        -- 正常状态 = 3
                                        -- 退出策略（REMAINING_WARMTH）= 2（降低门槛，方便退出）
                                        -- 试错状态（GESTATION/POWER_TRANSITION）= 4（提高门槛，过滤噪音）
```

---

## 3. 状态机定义与转移条件

### 3.1 状态转移图

```
[上涨周期]                                                    [下降周期]
                                                                    
  ┌──────────────┐      切割完成      ┌──────────────┐     确认攻击      ┌──────────────┐
  │  攻击有持续   │◄─────────────────│     孕化      │◄────────────────│  余温/切割   │
  │  ATTACK_SUS  │                   │   GESTATION   │                  │   WARMTH     │
  └──────┬───────┘                   └──────┬───────┘                  └──────┬───────┘
         │                                   ▲                                    │
         │         领涨示弱+交权              │           切割完成                │
         │         +新领涨持续               │                                   │
         │         (分期转移)                │           未切割完:                │
         │                                   │           杀空间板3-4个           │
         ▼                                   │           或领涨A杀              │
  ┌──────────────┐                           │                                    │
  │  交权磨合期   │───────────────────────────┘                                    │
  │  POWER_TRANS  │         未形成持续+余翁未清                                      │
  └──────┬───────┘                                                              │
         │         持续无承接:                                                    │
         │         频繁换人+杀空间                                               │
         │         (全面退潮)                                                    │
         ▼                                                                        ▼
  ┌──────────────┐                                                          ┌──────────────┐
  │  攻击无持续   │◄─────────────────────────────────────────────────────────│  余温补跌    │
  │  ATTACK_UNS  │                                                          │  WARMTH_FALL │
  └──────────────┘                                                          └──────────────┘
         ▲
         │
         │ 确认攻击
         │（阵型+包容度）
         │
  ┌──────────────┐
  │  确认攻击     │
  │  ATTACK_CONF │
  └──────────────┘
```

### 3.2 状态转移条件详表

| 当前状态 | 转移目标 | 触发条件 | 否决条件 | 置信度要求 |
|----------|----------|----------|----------|-----------|
| ATTACK_SUSTAINED | POWER_TRANSITION | 领涨示弱（无法新高/收盘价不创新高）；原攻击阵型松动 | 领涨只是断板但次日修复（假示弱） | ≥ 0.6 |
| ATTACK_SUSTAINED | REMAINING_WARMTH | 领涨多次无法新高；攻击阵型瓦解；个股高位反复但无法突破 | 单日调整后继续新高（正常分期） | ≥ 0.7 |
| POWER_TRANSITION | ATTACK_SUSTAINED | 新领涨明确持续（前交易日领涨+空间板双持续）；攻击阵型重新聚合 | 新领涨只是一日游；无新领涨持续 | ≥ 0.7 |
| POWER_TRANSITION | ATTACK_UNSUSTAINED | 频繁换领涨/换空间板；新领涨无持续；出现退潮力量 | 短暂换人间歇后持续恢复 | ≥ 0.6 |
| POWER_TRANSITION | GESTATION | 未形成持续+余翁未清（切割未完全） | 新领涨已明确持续 | ≥ 0.5 |
| REMAINING_WARMTH | CUTTING_COMPLETE | 条件1：上一龙领涨直接A杀持续跌；条件2：每天杀空间板3-4个 | 只是小幅回调未A杀；只杀一个空间板 | ≥ 0.8 |
| CUTTING_COMPLETE | GESTATION | 完成切割后出现新面孔个股；新面孔开始尝试持续 | 切割完成后无新面孔（真空期） | ≥ 0.5 |
| GESTATION | ATTACK_CONFIRMED | 前交易日领涨持续；形成攻击阵型（3-4只协同）；有包容度扩散 | 只是个股单独持续无阵型；带不出全局扩散 | ≥ 0.7 |
| GESTATION | REMAINING_WARMTH | 孕化失败：特发信息型（余温未完全切割，再杀空间后入至暗）或中式传媒型（带不出全局扩散） | 孕化期个股短暂回调后重新持续并带出阵型 | ≥ 0.6 |
| ATTACK_CONFIRMED | POWER_TRANSITION | 状态持续领涨换人（分期转移制）；部分个股掉队但阵型不散 | 一掉就全面瓦解（退潮非分期） | ≥ 0.6 |
| ATTACK_CONFIRMED | ATTACK_UNSUSTAINED | 频繁换领涨/空间板；触发切割条件；头部出现退潮力量 | 短暂换人间阵重新聚合 | ≥ 0.6 |
| ATTACK_UNSUSTAINED | REMAINING_WARMTH | 频繁换人+杀空间（全面退潮） | 短暂下跌后迅速恢复 | ≥ 0.6 |

---

## 4. 计算逻辑（伪代码）

### 4.1 状态识别核心函数

```python
def identify_cycle_state(market_data, prev_state, state_duration):
    """
    识别当前市场周期状态
    
    参数:
        market_data: dict with [ten_day_rank, leading_stock, space_board, 
                                  attack_formation, tolerance, tide_force, cutting_condition]
        prev_state: 上一周期状态
        state_duration: 当前状态持续天数
    
    返回:
        dict with pq_* fields
    """
    
    # 1. 提取核心可观测证据
    leading_sustained = market_data['leading_stock_sustained']
    leading_new_high = market_data['leading_stock_new_high']
    space_board_sustained = market_data['space_board_sustained']
    formation_count = market_data['attack_formation_count']
    formation_valid = market_data['attack_formation_valid']
    tolerance_exist = market_data['tolerance_exist']
    tolerance_score = market_data['tolerance_score']
    tide_force_exist = market_data['tide_force_exist']
    tide_force_score = market_data['tide_force_score']
    cutting_met = market_data['cutting_condition_met']
    new_faces = market_data['gestation_new_faces']
    new_faces_sustained = market_data['gestation_new_faces_sustained']
    
    # 2. 状态识别逻辑（优先级从高到低）
    
    # 最高优先级：切割条件（无论当前什么状态，切割条件满足即进入 CUTTING_COMPLETE）
    if cutting_met:
        return {
            'pq_state': 'CUTTING_COMPLETE',
            'pq_state_confidence': 0.9,
            'pq_trading_permission': 'HALT',
            'pq_position_max_size': 0.0,
            'pq_transition_trigger': '切割条件满足：领涨A杀或连续杀空间板',
        }
    
    # 第二优先级：攻击有持续（最强上涨信号）
    if leading_sustained and leading_new_high and space_board_sustained and formation_valid and tolerance_exist and not tide_force_exist:
        return {
            'pq_state': 'ATTACK_SUSTAINED',
            'pq_state_confidence': min(1.0, 0.7 + tolerance_score * 0.3),
            'pq_trading_permission': 'FULL',
            'pq_position_max_size': 1.0,
            'pq_transition_trigger': '领涨持续+空间板持续+阵型有效+包容度存在+无退潮',
        }
    
    # 第三优先级：确认攻击（阵型形成但可能刚启动或分期转移）
    if leading_sustained and space_board_sustained and formation_count >= 3 and tolerance_exist:
        return {
            'pq_state': 'ATTACK_CONFIRMED',
            'pq_state_confidence': min(1.0, 0.6 + tolerance_score * 0.3),
            'pq_trading_permission': 'FULL',
            'pq_position_max_size': 0.7,  # 确认攻击允许建仓，但略保守于攻击有持续
            'pq_transition_trigger': '领涨持续+空间板持续+阵型≥3只+包容度存在',
        }
    
    # 第四优先级：余温（高位反复但无法新高）
    if not leading_new_high and not space_board_sustained and tide_force_exist and not cutting_met:
        return {
            'pq_state': 'REMAINING_WARMTH',
            'pq_state_confidence': min(1.0, 0.5 + tide_force_score * 0.4),
            'pq_trading_permission': 'EXIT_ONLY',
            'pq_position_max_size': 0.0,
            'pq_transition_trigger': '领涨无法新高+空间板不持续+退潮力量存在+未切割',
        }
    
    # 第五优先级：攻击无持续（频繁换人）
    if not leading_sustained and not space_board_sustained and market_data['ten_day_rank_change'] >= 3:
        return {
            'pq_state': 'ATTACK_UNSUSTAINED',
            'pq_state_confidence': min(1.0, 0.5 + tide_force_score * 0.4),
            'pq_trading_permission': 'HALT',
            'pq_position_max_size': 0.0,
            'pq_transition_trigger': '领涨不持续+空间板不持续+频繁换人（换≥3个）',
        }
    
    # 第六优先级：交权磨合期（过渡阶段）
    if not leading_sustained and not space_board_sustained and formation_count >= 2 and not tide_force_exist:
        return {
            'pq_state': 'POWER_TRANSITION',
            'pq_state_confidence': 0.5,
            'pq_trading_permission': 'REDUCED',
            'pq_position_max_size': 0.3,
            'pq_transition_trigger': '领涨不持续+空间板不持续+但仍有候选（≥2只）+无退潮',
        }
    
    # 第七优先级：孕化（新面孔尝试）
    if new_faces >= 2 and new_faces_sustained and not cutting_met:
        return {
            'pq_state': 'GESTATION',
            'pq_state_confidence': min(1.0, 0.4 + new_faces * 0.1),
            'pq_trading_permission': 'REDUCED',
            'pq_position_max_size': 0.3,
            'pq_transition_trigger': f'切割后新面孔≥{new_faces}只且持续',
        }
    
    # 默认：状态模糊，降级到最保守状态
    return {
        'pq_state': 'ATTACK_UNSUSTAINED',  # 状态模糊时默认禁止交易
        'pq_state_confidence': 0.3,
        'pq_trading_permission': 'HALT',
        'pq_position_max_size': 0.0,
        'pq_transition_trigger': '状态模糊，降级到保守状态',
    }
```

### 4.2 每日执行清单（DAILY PLAYBOOK）

```python
def daily_playbook(ten_day_rank_data):
    """
    每日必做的 14 步检查
    
    参数:
        ten_day_rank_data: 通达信/同花顺 10日区间涨幅榜前十个（主板10cm）
    
    返回:
        dict with daily_check results
    """
    
    checks = {}
    
    # 步骤 1-2：确定领涨
    checks['step_1'] = "打开10日区间涨幅榜，只看主板10cm前十个"
    checks['step_2'] = "确定前交易日涨停时间最早的个股（领涨）"
    
    # 步骤 3-4：判断持续度
    checks['step_3'] = "判断前交易日领涨今天是否持续"
    checks['step_4'] = "判断空间板是否持续"
    
    # 步骤 5-7：判断环境
    checks['step_5'] = "观察前十中是否有退潮力量（个股持续跌/A杀）"
    checks['step_6'] = "判断攻击阵型是否完整（3-4只协同）"
    checks['step_7'] = "检查失败个股是否有修复（包容度）"
    
    # 步骤 8-12：决策
    checks['step_8'] = "若攻击有持续且阵型完整 → 持有或参与领涨"
    checks['step_9'] = "若领涨一字买不到 → 找换手协同（非必须）"
    checks['step_10'] = "若攻击无持续/频繁换人 → 空仓休息"
    checks['step_11'] = "若处于交权磨合期 → 观察等待，不重仓"
    checks['step_12'] = "若处于余温阶段 → 全部舍弃不参与"
    
    # 步骤 13-14：持仓管理
    checks['step_13'] = "检查持仓个股是否自强（日日新高）"
    checks['step_14'] = "记录当日状态判断和应对"
    
    return checks
```

---

## 5. 与现有对象卡的互锁逻辑（已冻结）

### 5.1 与所有执行层对象卡的互锁

```text
互锁规则 PERIOD_QUEEN × 所有 EXECUTION 对象卡：

1. 交易权限前置检查：
   - pq_trading_permission = 'HALT' → 所有 EXECUTION 对象卡的 signal_type 强制设为 'NONE'
   - pq_trading_permission = 'EXIT_ONLY' → 只允许 signal_type = 'SHORT'（减仓/退出），'LONG' 强制设为 'NONE'
   - pq_trading_permission = 'REDUCED' → 允许 LONG，但 signal_strength 最高为 7（不超过）
   - pq_trading_permission = 'FULL' → 正常执行，不受限制

2. 投票门槛调整：
   - pq_state = 'REMAINING_WARMTH' → entry_min_votes = 2（降低门槛，方便退出）
   - pq_state = 'GESTATION' 或 'POWER_TRANSITION' → entry_min_votes = 4（提高门槛，过滤噪音）
   - pq_state = 'ATTACK_SUSTAINED' 或 'ATTACK_CONFIRMED' → entry_min_votes = 3（正常）

3. 对象卡激活/禁用：
   - pq_state = 'ATTACK_SUSTAINED' → 激活 [CHZL_BSD, BPB, VP, TKR7, MFLOW]
   - pq_state = 'REMAINING_WARMTH' → 激活 [TKR7, CHZL_BSD, VOLTARGET]，禁用 [BPB, VP, MFLOW(增强)]
   - pq_state = 'GESTATION' → 激活 [CHZL_BSD(1Buy), YTC(BOF), BPB(1st限制)]
   - pq_state = 'POWER_TRANSITION' → 激活 [YTC(TST), BPB(2nd限制)]
   - pq_state = 'ATTACK_UNSUSTAINED' / 'CUTTING_COMPLETE' → 禁用所有 EXECUTION 对象卡
```

### 5.2 与 VOLFAC 的互锁

```text
互锁规则 PERIOD_QUEEN × VOLFAC：

1. 高波动期与情绪周期的共振：
   - volfac_vol_regime = 'EXTREME_VOL' + pq_state = 'REMAINING_WARMTH' → 双重警告，强制 EXIT_ONLY
   - volfac_vol_regime = 'LOW_VOL' + pq_state = 'ATTACK_SUSTAINED' → 理想环境，允许 FULL 仓位

2. 小盘股波动率分层：
   - pq_state = 'ATTACK_SUSTAINED' 且领涨是小盘股 → VOLFAC 的 target_vol 提高到 20%
```

### 5.3 与 CHZL_BSD 的互锁

```text
互锁规则 PERIOD_QUEEN × CHZL_BSD：

1. 缠论买卖点与情绪周期的映射：
   - pq_state = 'ATTACK_SUSTAINED' → CHZL_BSD 优先 3Buy（离开中枢），1Buy/2Buy 降级
   - pq_state = 'GESTATION' → CHZL_BSD 优先 1Buy（背驰抄底），3Buy 禁用（趋势未确认）
   - pq_state = 'REMAINING_WARMTH' → CHZL_BSD 优先 1Sell（背驰逃顶），所有 Buy 信号降级
   - pq_state = 'POWER_TRANSITION' → CHZL_BSD 所有信号 strength -2（过渡期噪音大）

2. 止损调整：
   - pq_state = 'GESTATION' → 1Buy 止损放宽（bi.low - 0.3ATR，因为孕化期波动大）
   - pq_state = 'REMAINING_WARMTH' → 所有止损收紧（-0.2ATR，因为末期风险高）
```

### 5.4 与 MFLOW 的互锁

```text
互锁规则 PERIOD_QUEEN × MFLOW：

1. 资金流向与情绪周期的共振：
   - pq_state = 'ATTACK_SUSTAINED' + mflow_inflow_ratio > 0.05 → 资金流入确认攻击持续，信号增强
   - pq_state = 'REMAINING_WARMTH' + mflow_inflow_ratio > 0.05 → 资金流入可能是诱多（余温期），信号降级
   - pq_state = 'GESTATION' + mflow_inflow_ratio > 0.05 → 资金流入确认孕化成功，信号增强

2. 早盘意图：
   - pq_state = 'GESTATION' + mflow_open_intent = 'STRONG_BUY' → 早盘抢筹确认新周期启动
   - pq_state = 'REMAINING_WARMTH' + mflow_open_intent = 'STRONG_BUY' → 早盘抢筹可能是诱多，降级
```

### 5.5 与 KELLY / VOLTARGET 的互锁

```text
互锁规则 PERIOD_QUEEN × KELLY / VOLTARGET：

1. 仓位上限调制：
   - pq_position_max_size 作为 Kelly size_scalar 的上限
   - 最终 size_scalar = min(kelly_size_scalar, voltarget_size_scalar, pq_position_max_size)
   - 例如：Kelly 建议 0.5，VolTarget 允许 1.0，但 pq_position_max_size = 0.3（孕化期）→ 最终 = 0.3

2. 危机模式：
   - pq_state = 'ATTACK_UNSUSTAINED' 连续 3 日 → 触发 Kelly 危机模式（无论交易结果如何）
   - pq_state = 'CUTTING_COMPLETE' → VolTarget 强制 HALT_NEW（无论波动率如何）
```

---

## 6. 失效模式（已冻结）

```text
PERIOD_QUEEN 失效条件：

1. 数据缺失：
   - 10日区间涨幅榜数据缺失（某些小盘或ST股不在榜单）→ 用通达信/同花顺的排名数据替代
   - 涨停时间数据缺失（一字板无法判断涨停时间）→ 溯源前一日涨停时间，或标记为 earliest
   - 数据延迟（T+1 公布）→ 周期女王基于昨日数据判断今日状态，有1日滞后

2. 极端行情：
   - 全市场涨停（千股涨停）→ 10日区间涨幅榜失效（所有股都在前十），标记为 'extreme_market'
   - 全市场跌停（千股跌停）→ 直接判定为 CUTTING_COMPLETE，无需等待切割条件
   - 连续一字板（无换手）→ 领涨无法判断持续性，标记为 'limit_up_only'

3. 状态误判：
   - 假持续（单日领涨持续但次日直接A杀）→ 状态从 ATTACK_SUSTAINED 误判，次日纠正
   - 假交权（短暂换人后迅速恢复）→ 状态从 POWER_TRANSITION 误判回 ATTACK_SUSTAINED
   - 应对：状态切换后至少观察 2 个交易日再确认，避免频繁切换

4. 市场风格切换：
   - 10cm 切换到 20cm/30cm（科创板/创业板主导）→ 10日区间涨幅榜前十个可能全是 20cm
   - 应对：增加 20cm/30cm 的观察窗口，或调整榜单范围

5. 北向资金主导：
   - 北向资金大幅流入但内资情绪差 → 周期女王基于内资情绪判断，可能与北向行为冲突
   - 应对：增加北向资金流向作为辅助指标，但不改变核心判断逻辑
```

---

## 7. 成熟度与数据需求

| 维度 | 评估 |
|------|------|
| **所需数据** | 10日区间涨幅榜（通达信/同花顺）、涨停时间、涨跌停数据、个股持续性（日K） |
| **计算复杂度** | 中（主要是数据整理和条件判断） |
| **实时性能** | 日频更新（每日收盘后计算，次日开盘前可用） |
| **回测可行性** | 高（历史涨幅榜数据可回溯） |
| **A 股落地** | 可直接落地（数据普及） |
| **外汇/期货/币圈落地** | 不适用（情绪周期是 A 股特定概念） |
| **跨周期** | 日频为主，日内可基于早盘数据做初步判断 |

---

> 文件：OBJECT_CARD_PERIOD_QUEEN_P0_F__CycleStateSystem_v1.0.md  
> 生产者：Kimi（基于周期女王规则壳 v1.0 字段化）  
> 状态：已冻结核心字段，作为系统第一层（环境识别）的核心状态机  
> 关键设计：
> - 七态状态机，每个状态有明确的交易权限和对象卡激活列表
> - 状态转移基于可观测证据（领涨持续度、阵型完整性、包容度、退潮力量）
> - 与所有现有对象卡有互锁规则，特别是投票门槛和仓位上限的调制
> - 作为纲领的"心脏"，其他对象卡都是它的"四肢"
