# GLM_TASK_08 — 第二优先级执行层对象卡字段化

> 任务编号：GLM_TASK_08  
> 主题：第二优先级执行层对象（TK-R7 AO 背离 / Brooks BPB / YTC TST/BOF/BPB）  
> 阶段：结构化提取，不编码  
> 生产者：GLM（需基于已有素材 + 搜索知识）  
> 交付格式：Markdown 对象卡，每对象一份，统一存于用户仓库  
> 前置必读：GLM_MATERIAL_PACKAGE_INDEX.md 中标记的"必读文件"

---

## 一、背景

第一优先级执行层对象（CHZL_BSD 止损 / TK-R6 回撤阻挡 / TK-R8 资格壳）已完成字段冻结并入库。当前仓库已有 6 个对象进入"已冻结核心字段 / proxy_quantizable_now"状态：
- CHZL_BSD（执行层）、TK-R6（执行层）、TK-R8（执行层）
- VP_P0_E（执行层）、KELLY_P0_R（风控层）、VOLTARGET_P0_R（风控层）

**第二优先级执行层对象**尚未完成字段化，它们是：
- **TK-R7 AO 背离**：Awesome Oscillator 柱体与价格的背离
- **Brooks BPB**：Al Brooks 的 Breakout Pullback 模式
- **YTC TST/BOF/BPB**：Lance Beggs 的微观结构（假突破/突破失败/突破回测）

这些对象在第一优先级交付的 `GLM_DELIVERY_07_TIER1_EXECUTION_FIELDS_v2.0.md` 中已有**蓝图级描述**，但缺少完整的字段冻结、伪代码、互锁逻辑和测试断言。

---

## 二、素材来源

### 2.1 第一优先级交付中的蓝图（必读）

**GLM_DELIVERY_07_TIER1_EXECUTION_FIELDS_v2.0.md** 中已给出：

**TK-R7 AO 背离**：
- 逻辑：AO 柱体颜色/高度与价格的背离
- 字段：`ao_divergence_type` (`REGULAR`/`HIDDEN`/`NONE`), `ao_peak_diff`
- 联动：当 `kd_week_extreme_zone=OVERBOUGHT` 且 `ao_divergence=REGULAR_SELL` 时，锁定 `FORCE_EXIT`

**Brooks BPB**：
- 逻辑：强趋势线突破后的第一次回调
- 字段：`bpb_count` (第几次回调，通常只取 1st/2nd), `bpb_magnitude` (回调幅度%)
- 联动：仅当 `chzl_trend_type=TREND_UP` 时激活 BPB 监测

**YTC TST/BOF/BPB**：
- 逻辑：
  - TST (Test of Extremes): 假突破极值
  - BOF (Breakout Failure): 突破后迅速收回
  - BPB (Breakout Pullback): 突破后的有效回踩
- 字段：`ytc_signal_type`, `ytc_trigger_bar_idx`

### 2.2 已有对象卡（互锁参考）

- `TK外汇核心概念对象卡_Kimi版_v1.0.md` — TK-R7 已有初步定义（AO 背离识别）
- `GLM_DELIVERY_05_TK_FOREX_OPTIMIZATION_v1.0.md` — TK-R7 与 TK-R6/R8 的联合使用逻辑
- `全仓库功能映射大表_v2.0.md` — 确认这三个对象在 55 个对象中的位置

### 2.3 外部体系素材（Kimi 已有 CUTPACK）

- **Brooks 三本书**：A1 组已切割，但 CUTPACK 中 BPB 部分尚未单独提取
- **YTC Price Action**：A1 组已有 `迷你结构/批发/零售/陷阱` 概念，TST/BOF/BPB 在 YTC 教程中有详细定义
- **Bill Williams AO**：Awesome Oscillator 是标准指标，公式公开（34期 SMA - 5期 SMA 的中位数价格）

---

## 三、任务要求

### 3.1 交付物

为以下 **3 个第二优先级执行层对象** 编写字段化对象卡：

| # | 对象名称 | 对象 ID | 功能层 | 成熟度 | 素材来源 |
|---|---------|--------|-------|-------|---------|
| 1 | TK-R7 AO 背离 | TKR7_P0_E | P0_E（执行层） | proxy_quantizable_now | GLM_DELIVERY_07 + TK外汇对象卡 |
| 2 | Brooks BPB | BPB_P0_E | P0_E（执行层） | proxy_quantizable_now | GLM_DELIVERY_07 + Brooks 素材 |
| 3 | YTC TST/BOF/BPB | YTC_P0_E | P0_E（执行层） | proxy_quantizable_now | GLM_DELIVERY_07 + YTC 素材 |

### 3.2 每个对象卡必须包含的章节

**严格遵循 `OBJECT_CARD_VP_P0_E__VolumeProfile_v1.0.md` 的格式**：

1. **基本定义**：该对象描述什么，与现有指标的区别
2. **核心概念与字段冻结**：
   - 基础字段（原始输入，如 AO 值、价格、趋势线状态）
   - 派生字段（计算后，如背离类型、回调幅度）
   - 信号字段（如 `ao_signal_type`, `bpb_signal_type`, `ytc_signal_type`）
3. **计算逻辑（伪代码）**：
   - 对于 TK-R7：AO 计算 + 背离识别（峰值比较）
   - 对于 BPB：趋势线突破检测 + 回调深度计算
   - 对于 YTC：极值测试 + 突破失败检测 + 突破回测确认
   - 所有公式必须标注来源
4. **与现有指标的互锁逻辑**（至少 4 组）：
   - 与 KD MTF 的互锁（如：AO 背离只在 KD 极端区有效）
   - 与 Volty 的互锁（如：BPB 在 Volty 趋势状态下不同处理）
   - 与 VP 的互锁（如：YTC BPB 在 VP 的 HVN 区域确认）
   - 与缠论 BSD 的互锁（如：TK-R7 与 BSD 1Buy 的背离确认共振）
   - 与 TK-R6/R8 的互锁（如：BPB 只在 R6 状态为 TOUCH_BOUNCE 时有效）
5. **失效模式**：什么时候该对象不可用
6. **A 股特殊适配**：涨停/跌停、T+1、散户行为影响
7. **成熟度与数据需求**：

### 3.3 特别要求

#### TK-R7 AO 背离 的特别要求：

- AO 公式：Awesome Oscillator = SMA(中位数价格, 5) - SMA(中位数价格, 34)
- 中位数价格 = (High + Low) / 2
- 背离定义：
  - **Regular Divergence（常规背离）**：价格创新高但 AO 未创新高（顶背离）/ 价格创新低但 AO 未创新低（底背离）
  - **Hidden Divergence（隐藏背离）**：价格回调但 AO 未回调（趋势延续信号）
- 必须包含 `ao_divergence_type` 枚举：`REGULAR_BULL`, `REGULAR_BEAR`, `HIDDEN_BULL`, `HIDDEN_BEAR`, `NONE`
- 必须包含 `ao_peak_diff`：价格峰值差 vs AO 峰值差的比例
- 必须明确：AO 背离是**过滤器**（确认信号），不是**触发器**（独立入场信号）
- 联动要求：当 `kd_week_extreme_zone=OVERBOUGHT` 且 `ao_divergence=REGULAR_BEAR` 时 → 强制退出（FORCE_EXIT）

#### Brooks BPB 的特别要求：

- 必须区分：
  - **Breakout Pullback（有效回测）**：突破后回调到突破点附近，然后继续原方向
  - **Failed Breakout（假突破）**：突破后迅速回到原区间
  - **First Pullback / Second Pullback**：只取前两次回调，第三次不交易
- 必须包含 `bpb_count`：1st / 2nd / 3rd+（3rd+ 标记为拒绝）
- 必须包含 `bpb_magnitude`：回调幅度 %（相对于突破 K 线的实体）
- 必须包含 `bpb_trend_strength`：突破前的趋势强度评分（与 LBR ADX 或 KD alignment 关联）
- 联动要求：仅当 `chzl_trend_type=TREND_UP`（或 TREND_DOWN）时激活 BPB 监测；震荡市不激活
- 必须包含 Brooks 的 "Always In" 方向过滤：与 Brooks Always In 状态互锁

#### YTC TST/BOF/BPB 的特别要求：

- 必须区分三种信号类型：
  - **TST (Test of Extremes)**：价格测试极值（前高/前低）后迅速收回，形成假突破
  - **BOF (Breakout Failure)**：突破后 1-3 根 K 线内回到原区间
  - **BPB (Breakout Pullback)**：突破后回调到突破区域，然后继续（有效突破）
- 必须包含 `ytc_signal_type` 枚举：`TST_LONG`, `TST_SHORT`, `BOF_LONG`, `BOF_SHORT`, `BPB_LONG`, `BPB_SHORT`, `NONE`
- 必须包含 `ytc_trigger_bar_idx`：触发信号的 K 线索引（用于回溯验证）
- 必须包含 `ytc_confirmation_count`：确认信号需要的后续 K 线数量（如 BPB 需要 2 根确认）
- 必须包含 YTC 的 "S/R 框架" 前提：这三个信号都依赖于 YTC S/R 框架的预定义支撑/阻力区
- 联动要求：与 YTC_SRF（三周期 S/R 框架）互锁——如果 S/R 框架未定义，YTC 信号无效

---

## 四、已提供的参考文件（GLM 必须读取）

请 GLM 在编写对象卡前按以下顺序阅读：

### 第一步：格式模板（必读）
1. `OBJECT_CARD_VP_P0_E__VolumeProfile_v1.0.md` — 对象卡格式模板
2. `OBJECT_CARD_KELLY_P0_R__KellyCriterion_v1.0.md` — 互锁逻辑风格参考

### 第二步：现有交付（必读）
3. `GLM_DELIVERY_07_TIER1_EXECUTION_FIELDS_v2.0.md` — 第二优先级蓝图（第 4 节）
4. `GLM_DELIVERY_05_TK_FOREX_OPTIMIZATION_v1.0.md` — TK 体系优化（R7 定义）
5. `TK外汇核心概念对象卡_Kimi版_v1.0.md` — TK 对象卡（R7 初步定义）

### 第三步：仓库索引（必读）
6. `全仓库功能映射大表_v2.0.md` — 确认新对象与已有 55 个对象的关系

### 第四步：素材索引（按需）
7. `执行层字段化优先级清单.md` — 10 个对象的完整排序和理由

---

## 五、交付路径

GLM 完成后，将 3 个 Markdown 文件的内容直接写入回复中，或保存到指定路径。Kimi 会负责：
- 格式化（统一命名规范、字段风格）
- 审核（与现有对象的一致性检查）
- 入库（并入全仓库功能映射大表 v2.1）

---

## 六、优先级与范围

**第一优先级（必须完成）**：
- TK-R7 AO 背离 — 已有明确字段定义（`ao_divergence_type`, `ao_peak_diff`），只需补全互锁和伪代码

**第二优先级（尽量完成）**：
- Brooks BPB — 已有蓝图，需要细化回调深度和趋势强度
- YTC TST/BOF/BPB — 已有蓝图，需要区分三种信号和确认机制

---

## 七、格式规范提醒（重要）

1. **不要编码**：只写伪代码和字段定义，不要写完整的 Python 可执行代码
2. **保守标注**：只有常规 OHLCV 数据可直接落地的条目保留 `proxy_quantizable_now`；依赖复杂指标组合的降级为 `needs_extra_data`
3. **互锁必须完整**：每个对象至少与 KD MTF、Volty、VP、缠论 BSD 互锁
4. **所有产出必须携带**：producer / source_path / status 元数据
5. **文件命名**：`OBJECT_CARD_{ID}__{中文名}_v1.0.md`

---

> 任务发起人：Kimi  
> 时间：2026-06-24  
> 状态：已发送，等待 GLM 交付
