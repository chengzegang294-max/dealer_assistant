# GLM 素材包清单（GLM_Material_Package_Index）

> 用途：每次给 GLM 发任务时，将此清单作为前置上下文，让 GLM 了解仓库格式和已有资产  
> 更新日期：2026-06-24  
> 适用：GLM_TASK_07 及后续任务

---

## 一、必读文件（格式模板层）

给 GLM 任何任务前，必须先读以下文件了解仓库格式规范：

### 1. 对象卡格式模板

**`OBJECT_CARD_VP_P0_E__VolumeProfile_v1.0.md`** — 最完整的格式参考
- 包含：基本定义 → 核心概念与字段冻结（基础/派生/信号）→ 计算逻辑伪代码 → 与现有指标互锁（4组）→ 多周期联立 → 失效模式 → A股适配 → 成熟度评估
- **GLM 必须严格遵循此格式**，每份对象卡至少包含以上 8 个章节

**`OBJECT_CARD_KELLY_P0_R__KellyCriterion_v1.0.md`** — 风控层格式参考
- 包含：公式变体 → 输入/计算/动态调整字段 → 伪代码 → 与现有风控层互锁（Van Tharp/Volty/KD/执行层）→ 失效模式 → A股适配

**`OBJECT_CARD_VOLTARGET_P0_R__VolatilityTargeting_v1.0.md`** — 风控层格式参考
- 包含：核心公式 → 字段冻结 → 多资产组合版本 → 与 Kelly/Van Tharp/Volty/KD 互锁 → 多周期联立

### 2. 互锁逻辑风格参考

**`GLM_DELIVERY_05_TK_FOREX_OPTIMIZATION_v1.0.md`** — TK 外汇优化交付
- 包含：IB/DB/CB 边界条件 + R6 5级状态机 + R7 AO背离 + R8 ABC资格 + TK×缠论交叉映射
- **互锁逻辑的写法风格参考此文件**（用 `互锁规则 X × Y：` 格式）

**`GLM_DELIVERY_04_CHANLUN_FULL_QUANT_v1.0.md`** — 缠论全量化交付
- 包含：FX/BI/BC/BSD 伪代码 + 字段冻结 + SQL 融合视图 `v_chanlun_kd_lock`
- **字段冻结风格参考此文件**（用 SQL 风格字段定义）

### 3. 全仓库功能映射大表

**`全仓库功能映射大表_v2.0.md`** — 当前仓库所有对象的完整索引
- 55 个对象，6 个功能层
- **GLM 写新对象卡前，必须先查看此表，确认新对象与已有对象的关系**（互补/重叠/替代）

---

## 二、素材来源文件（GLM 按需读取）

根据 GLM 任务方向，选择性读取以下文件：

### 方向 A：缠论相关（已完结，仅供参考）

| 文件 | 内容 | 读取时机 |
|------|------|---------|
| `GLM_TASK_02_CHANLUN_OBJECT_CARD.md` | 缠论对象卡任务指令 | 仅参考历史 |
| `GLM_TASK_04_CHANLUN_FULL_QUANT_FORMULA.md` | 缠论全量化任务指令 | 仅参考历史 |
| `CHZL_ZS_量化公式与互锁视图_v1.0.md` | 缠论中枢 SQL 公式 | 写缠论互锁时必读 |
| `GLM_DELIVERY_04_CHANLUN_FULL_QUANT_v1.0.md` | 缠论全量化交付 | 写缠论互锁时必读 |
| `GLM_DELIVERY_06_TIER1_EXECUTION_FIELDS_v1.0.md` | 第一优先级执行层字段 | 写 BSD 止损时必读 |
| `GLM_DELIVERY_07_TIER1_EXECUTION_FIELDS_v2.0.md` | 第一优先级交付（含 BSD/R6/R8 完整版） | **当前必读** |

### 方向 B：TK 外汇相关（已完结，仅供参考）

| 文件 | 内容 | 读取时机 |
|------|------|---------|
| `TK外汇核心概念对象卡_Kimi版_v1.0.md` | Kimi 编写的 TK 7 对象卡 | 写 TK 互锁时必读 |
| `GLM_TASK_05_TK_FOREX_OPTIMIZATION.md` | TK 优化任务指令 | 仅参考历史 |
| `GLM_DELIVERY_05_TK_FOREX_OPTIMIZATION_v1.0.md` | TK 优化交付 | 写 TK 互锁时必读 |

### 方向 C：A 股特殊因子（GLM_TASK_07 进行中）

| 文件 | 内容 | 读取时机 |
|------|------|---------|
| `GLM_TASK_07_A股特殊因子字段化提取.md` | A股因子任务指令 | **当前任务，必读** |
| `GLM_SEARCH_01_执行层补充_跨市场_风控_另类数据_v1.0.md` | 搜索汇总（VP/订单流/Kelly/另类数据） | 写风控/另类数据时必读 |
| `S_BUCKET_功能映射表_v1.tsv`（外部路径） | S_BUCKET 16 个对象的功能映射 | 写 A股因子时必读 |

### 方向 D：第二优先级执行层（GLM_TASK_08 待发）

| 文件 | 内容 | 读取时机 |
|------|------|---------|
| `执行层字段化优先级清单.md` | 10 个对象的优先级排序 | 写第二优先级时必读 |
| `GLM_DELIVERY_07_TIER1_EXECUTION_FIELDS_v2.0.md` | 第一优先级交付（含第二优先级蓝图） | **当前必读** |
| `后续方向建议清单.md` | 后续方向建议 | 仅参考 |

---

## 三、格式规范速查（GLM 必须遵守）

### 3.1 文件命名

```
OBJECT_CARD_{ID}__{中文名}_v{版本}.md
```

示例：`OBJECT_CARD_VP_P0_E__VolumeProfile_v1.0.md`

### 3.2 文件头必须包含

```markdown
# {ID} — {中文名} 对象卡

> 功能层：P0_X（X = S/E/R/A/C/G）
> 成熟度：proxy_quantizable_now / needs_extra_data / 已冻结核心字段
> 生产者：GLM / Kimi
> 来源：{素材来源}
> 状态：{待讨论 / 已冻结核心字段，待代码实现}
```

### 3.3 字段定义格式

```text
字段名              类型            含义
```

示例：
```text
vp_poc              FLOAT           控制点（Point of Control）：该周期内成交量最高的价格
vp_signal_type      ENUM            当前 VP 产生的信号类型：
                                    -- 'NONE' = 无信号
                                    -- 'VA_BREAKOUT_LONG' = 突破 VAH 做多
```

### 3.4 伪代码风格

- 使用 Python 风格，但**不要写完整可执行代码**
- 用中文注释说明意图
- 包含公式来源注释（如"来自 SBKT_F014 正文"）

### 3.5 互锁逻辑格式

```text
互锁规则 {对象A} × {对象B}：

1. 规则描述...
2. 规则描述...
3. 若冲突 → 处理方式...
```

### 3.6 成熟度保守原则

- 只有常规 A 股数据（OHLCV、资金流向、龙虎榜）可直接落地的条目保留 `proxy_quantizable_now`
- 依赖 Level-2、NLP、另类数据的条目降级为 `needs_extra_data`
- 哲学/心法/直觉类内容归为 `NOT_QUANT_YET` 或 `shell_only`

### 3.7 所有产出必须携带元数据

```text
producer: GLM
source_path: {素材来源路径}
status: {已冻结 / 待讨论 / 待审核}
```

---

## 四、GLM 任务历史索引

| 任务编号 | 主题 | 状态 | 交付文件 |
|---------|------|------|---------|
| GLM_TASK_02 | 缠论对象卡 | 已完成 | 缠论 7 概念卡 |
| GLM_TASK_04 | 缠论全量化公式 | 已完成 | GLM_DELIVERY_04 |
| GLM_TASK_05 | TK 外汇优化 | 已完成 | GLM_DELIVERY_05 |
| GLM_TASK_06 | 回测框架设计 | 已完成 | 执行层字段化优先级清单 |
| GLM_TASK_07 | A 股特殊因子 | **进行中** | 等待交付 |
| GLM_TASK_08 | 第二优先级执行层 | **待发** | 待编写 |

---

> 文件：GLM_MATERIAL_PACKAGE_INDEX.md  
> 生产者：Kimi  
> 状态：已冻结，每次发 GLM 任务时作为前置上下文附带
