# GLM 任务指令：缠论结构化提取 + 与 KD MTF P0 互锁设计

## 任务目标

请帮我把**缠论**（缠中说禅）的核心概念提取成"可字段化的最小对象卡"，并设计它与**KD MTF P0**的互锁关系。

## 背景信息

我已有的一套指标叫 **KD MTF P0**，它的字段定义如下：

| 字段 | 说明 |
|------|------|
| `kd_week_bias` | 周线KD方向（up/down） |
| `kd_day_signal` | 日线KD信号（cross_up/cross_down/none） |
| `kd_4h_confirm` | 4小时KD确认（confirm/none） |
| `kd_alignment_tier` | 三周期一致性（s=共振/a=部分/b=待确认/conflict=冲突） |
| `kd_direction_filter` | 方向过滤（long_preferred/short_preferred/wait） |
| `kd_week_extreme_zone` | 周线极端区（overbought/oversold/normal） |

KD MTF P0 的哲学是：**只读结构，不预测**。它告诉"现在是什么状态"，不告诉"未来会怎么走"。

缠论的核心概念包括：**分型、笔、线段、中枢、走势类型、背驰、三类买卖点**。

## 输出要求

### 第一部分：缠论核心概念对象卡

请把缠论的以下 7 个核心概念，每个都按这个格式输出：

```markdown
### [概念编号] [概念名] — 缠论

| 字段 | 内容 |
|------|------|
| **object_id** | CHZL_[概念名缩写] |
| **object_name** | [中文名] |
| **source_anchor** | 缠论《教你炒股票》108课 |
| **source_path** | http://blog.sina.com.cn/chzhshch |
| **function_bucket** | [结构层/能量层/执行层/风控层] |
| **process_layer** | [原始数据/特征/因子/信号/过滤器/打分/仓位/执行约束/复盘评估] |
| **scope_tags** | [日频/高频/日内/横截面/时序/单资产/多资产] |
| **maturity_level** | [只读概念/已摘公式/已知输入输出/可做DIAG_ONLY/可进入候选组合/已验证不推荐] |
| **input_requirement** | [需要什么输入数据] |
| **output_form** | [输出什么字段/标签/数值] |
| **best_use_case** | [最佳使用场景] |
| **cannot_do_yet** | [目前不能做什么] |
| **combines_with** | [能和谁组合] |
| **overlaps_with** | [与谁重叠] |
| **failure_modes** | [在什么条件下失效] |
| **evidence_note** | [可验证证据] |
| **proxy_quantizable_now** | [是否可直接量化：yes / needs_extra_data / future_bucket / shell_only] |
```

**7 个必须覆盖的概念**：
1. **分型**（顶分型/底分型）
2. **笔**（由分型连接的最小结构单元）
3. **线段**（由笔构成的更高级结构）
4. **中枢**（价格重叠区域，缠论最核心的结构概念）
5. **走势类型**（趋势 vs 盘整，由中枢定义）
6. **背驰**（力度衰竭，MACD面积辅助判断）
7. **三类买卖点**（第一类=背驰点，第二类=回抽不破，第三类=不回到中枢）

### 第二部分：缠论 vs KD MTF P0 互锁设计

请回答以下问题：

1. **缠论能替代 KD MTF P0 吗？**
   - 为什么能或不能？
   - 两者的根本区别是什么？

2. **缠论能补充 KD MTF P0 的哪些不足？**
   - KD MTF P0 现在的"缺口"是什么？（提示：`b` 样本长期为0，`h4_confirm` 只在精确相等时触发）
   - 缠论的哪个概念可以填补这些缺口？

3. **互锁条件设计**
   - 请设计一个"KD MTF P0 + 缠论中枢"的最小互锁规则：
     - 当 `kd_alignment_tier = s` 时，缠论中枢应该是什么状态？
     - 当缠论出现"第三类买卖点"时，KD MTF P0 应该是什么状态？
     - 当两者冲突时，优先级怎么定？
   - 请设计一个"KD MTF P0 + 缠论背驰"的最小互锁规则：
     - 当 `kd_week_extreme_zone = overbought` 时，缠论背驰如何作为"能量确认"？
     - 当缠论背驰出现时，KD MTF P0 的 `kd_direction_filter` 应该如何调整？

4. **字段映射草案**
   - 如果要把缠论输出为与 KD MTF P0 同格式的 CSV 字段，请给出最小字段列表：
     - `chzl_fractal_type`（分型类型）
     - `chzl_bi_direction`（笔方向）
     - `chzl_xd_level`（线段级别）
     - `chzl_zhongshu_state`（中枢状态）
     - `chzl_trend_type`（走势类型）
     - `chzl_beichi_flag`（背驰标志）
     - `chzl_buy_sell_tier`（买卖点级别）
   - 每个字段的值域建议是什么？
   - 每个字段与 KD MTF P0 的哪个字段最相关？

### 第三部分：可落地建议

请给出"如果我要在下周开始落地"的最小行动清单：

1. 第一周做什么？（最小对象定义）
2. 第二周做什么？（proof-of-mapping 样本）
3. 第三周做什么？（互锁条件测试）
4. 哪些需要人工程序员实现？哪些可以用现有工具？

## 注意事项

1. **不要只给概念解释**：每个对象卡必须能说清"输入是什么、输出是什么、怎么用"。
2. **诚实标注成熟度**：缠论的背驰判断依赖 MACD 面积，这是主观性较强的，请标注为 `needs_extra_data` 或 `shell_only`。
3. **与 KD MTF P0 的关系要明确**：不是"替代"，是"补充"或"互锁"。
4. **中文输出优先**：缠论是中文概念，用中文解释，但字段名用英文（为了和 KD MTF P0 的字段对齐）。
5. **如果某个概念在缠论原著中定义模糊，请标注**：`source_ambiguity = [具体哪里模糊]`。

## 一句话记忆

> 不是"介绍缠论"，而是"把缠论拆成可和 KD MTF P0 互锁的最小对象"。
