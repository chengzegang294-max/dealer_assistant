# 大隐体系（DY）整合到现有交易系统 v1.0

> **本文档全部内容源于用户（仓库所有者）的想法，由 Kimi 整理为结构化文档供编程 AI 参考。**
> 版本：v1.0 | 状态：整合设计阶段 | 核心目标：将 DY 大隐体系映射到现有对象卡，明确重叠与补充关系

---

## 一、大隐体系概述

### 1.1 DY 是什么

```text
DY = 大隐，来自用户素材库中的"大隐体系"
是一套基于 A 股市场的综合交易框架，核心思想：

1. 结构定位：通过多周期共振判断市场位置
2. 量能验证：成交量是结构的"灵魂"
3. 时机选择：不在拐点猜方向，在确认后跟随
4. 仓位管理：根据确定性动态调整仓位

DY 体系的三条核心规则（来自用户素材）：
  DY_R1：结构确认规则 — 多周期方向一致才出手
  DY_R2：量能验证规则 — 关键位置的成交量必须配合
  DY_R3：仓位匹配规则 — 确定性越高，仓位越重
```

### 1.2 DY 与现有系统的重叠分析

```text
DY_R1（结构确认）→ 与现有对象卡的重叠：
  ├─ CHZL_TREND（缠论趋势结构）—— 核心重叠
  │   DY_R1 要求"多周期方向一致"
  │   CHZL_TREND 已经通过笔/中枢/背驰判断方向
  │   → DY_R1 是对 CHZL_TREND 的"多周期扩展"
  │
  ├─ KD MTF（多周期 KD）—— 部分重叠
  │   DY_R1 要求多周期共振
  │   KD MTF 已经在做跨周期 KD 极端区对齐
  │   → DY_R1 更强调"方向一致性"而非"极端值"
  │
  └─ YTC（多周期 S/R）—— 功能互补
      DY_R1 强调方向
      YTC 强调支撑阻力位
      → 两者结合：方向 + 关键位置 = 完整结构定位

DY_R2（量能验证）→ 与现有对象卡的重叠：
  ├─ MFLOW（资金流向）—— 核心重叠
  │   DY_R2 要求"关键位置成交量配合"
  │   MFLOW 已经通过资金流向判断主力意图
  │   → DY_R2 是对 MFLOW 的"位置敏感性扩展"
  │
  ├─ VP（成交量分布）—— 功能互补
  │   DY_R2 强调"突破时的放量"
  │   VP 强调"VA 突破/POC 偏离"
  │   → VP 可以作为 DY_R2 的"关键位置"定义工具
  │
  └─ VOLTARGET（波动率目标）—— 无重叠
      DY_R2 是方向性量能判断
      VOLTARGET 是仓位管理工具
      → 两者独立

DY_R3（仓位匹配）→ 与现有对象卡的重叠：
  ├─ KELLY（凯利公式）—— 核心重叠
  │   DY_R3 要求"确定性越高，仓位越重"
  │   Kelly 公式本身就是"根据胜率/盈亏比计算最优仓位"
  │   → DY_R3 是 KELLY 的"直觉化表述"
  │
  ├─ PeriodQueen（情绪周期）—— 功能互补
  │   DY_R3 强调"单票确定性"
  │   PeriodQueen 强调"市场环境允许的最大仓位"
  │   → PeriodQueen 是 DY_R3 的"天花板约束"
  │
  └─ Van Tharp（硬性上限）—— 无重叠
      DY_R3 是"上限内的动态调整"
      Van Tharp 是"绝对上限"
      → Van Tharp 是 DY_R3 的"安全网"
```

---

## 二、DY 规则映射到现有对象卡

### 2.1 DY_R1：结构确认规则 → 多周期对齐框架

```text
规则定义：
  "只有当日线、周线、60分钟三个周期方向一致时，才允许生成买入信号"

现有系统的覆盖情况：
  ✓ CHZL_TREND：日线趋势判断（上涨/下跌/盘整）
  ✓ CHZL_BSD：日线买卖点（3Buy/2Buy/1Buy）
  ✓ KD MTF：周线 KD 极端区（超卖区=潜在底部）
  ✗ 60分钟周期：现有系统缺少独立的 60min 对象卡

映射方案：
  不新建独立 DY_R1 对象卡，而是扩展现有对象卡：

  1. CHZL_TREND 增加多周期字段：
     ```python
     chzl_trend_output = {
         # 原有字段...
         "trend_state_daily": "up",      # 日线趋势
         "trend_state_weekly": "up",     # 周线趋势（新增）
         "trend_state_60min": "up",      # 60min趋势（新增）
         "alignment_score": 3,           # 对齐分数（3=全对齐，0=全背离）
         "dy_r1_passed": True,           # DY_R1 是否通过
     }
     ```

  2. KD MTF 增加方向一致性检查：
     ```python
     kd_mtf_output = {
         # 原有字段...
         "weekly_kd_zone": "oversold",   # 周线超卖区
         "daily_kd_zone": "oversold",    # 日线超卖区（新增）
         "alignment_with_trend": True,   # 与 CHZL_TREND 方向一致（新增）
     }
     ```

  3. 投票机制调整：
     ```python
     # 在 VoteDecisionEngine 中增加 DY_R1 检查
     def node_003_dy_r1_check(self, objects):
         chzl = objects.get("CHZL_TREND")
         kd = objects.get("KD_MTF")
         
         if chzl and chzl.get("alignment_score", 0) >= 2:
             # 至少两个周期对齐
             return "PASS", {"dy_r1": "passed"}
         else:
             return "ABORT", {"dy_r1": "failed", "reason": "多周期未对齐"}
     ```

实现优先级：P1（高）
数据需求：60min OHLCV（已有）
```

### 2.2 DY_R2：量能验证规则 → 位置敏感型资金流

```text
规则定义：
  "在关键位置（突破前高、回踩支撑位）时，成交量必须大于前 5 日均量的 1.5 倍"

现有系统的覆盖情况：
  ✓ MFLOW：资金流向判断（主力流入/流出）
  ✓ VP：成交量分布（POC、VA、HVN/LVN）
  ✗ 缺少"位置 + 量能"的联合判断

映射方案：
  不新建独立 DY_R2 对象卡，而是扩展 MFLOW：

  1. MFLOW 增加位置敏感型字段：
     ```python
     mflow_output = {
         # 原有字段...
         "volume_ratio": 1.8,            # 当日成交量 / 前5日均量（新增）
         "volume_at_key_level": True,    # 是否在关键位置放量（新增）
         "key_level_type": "breakout",   # 关键位置类型：breakout/pullback/support（新增）
         "dy_r2_passed": True,           # DY_R2 是否通过
     }
     ```

  2. VP 提供关键位置定义：
     ```python
     # VP 输出作为 MFLOW 的输入
     vp_output = {
         "poc": 12.50,
         "va_high": 13.00,
         "va_low": 12.00,
         "key_levels": ["VAH", "VAL", "POC"],  # 关键位置列表
     }
     
     # MFLOW 检查：当前价格是否在 VP 关键位置附近 + 是否放量
     ```

  3. 实现逻辑：
     ```python
     class MFlowP0A:
         def check_dy_r2(self, price, volume, vp_data):
             """检查 DY_R2：位置 + 量能"""
             # 1. 判断是否在关键位置
             near_key_level = self._is_near_key_level(price, vp_data)
             
             # 2. 判断是否放量
             avg_volume_5d = self._get_avg_volume(5)
             volume_ratio = volume / avg_volume_5d
             
             # 3. DY_R2 通过条件
             dy_r2_passed = near_key_level and volume_ratio >= 1.5
             
             return {
                 "volume_ratio": volume_ratio,
                 "volume_at_key_level": near_key_level,
                 "dy_r2_passed": dy_r2_passed,
             }
     ```

实现优先级：P1（高）
数据需求：日 OHLCV（已有）+ VP 特征（已有）
```

### 2.3 DY_R3：仓位匹配规则 → 确定性评分系统

```text
规则定义：
  "根据信号的综合确定性评分，动态调整仓位：
    确定性 ≥ 9 → 满仓（15%）
    确定性 7-8 → 重仓（10%）
    确定性 5-6 → 中仓（6%）
    确定性 3-4 → 轻仓（3%）
    确定性 < 3 → 观望"

现有系统的覆盖情况：
  ✓ KELLY：根据胜率/盈亏比计算最优仓位
  ✓ PeriodQueen：根据情绪周期设定仓位上限
  ✗ 缺少"信号综合确定性评分"

映射方案：
  不新建独立 DY_R3 对象卡，而是扩展投票机制：

  1. 引入"确定性评分"概念：
     ```python
     certainty_score = (
         chzl_strength * 0.3 +      # 缠论信号强度（30%）
         mflow_strength * 0.25 +     # 资金流向强度（25%）
         dy_r1_score * 0.20 +        # 多周期对齐（20%）
         dy_r2_score * 0.15 +        # 量能验证（15%）
         kd_alignment * 0.10         # KD 对齐（10%）
     )
     ```

  2. 与 Kelly 的协同：
     ```python
     def calculate_final_size(self, certainty_score, kelly_f, pq_max_size):
         """
         DY_R3 + Kelly 协同计算仓位
         
         逻辑：
         1. Kelly 给出理论最优仓位（基于历史统计）
         2. DY_R3 根据当前信号质量给出"信心折扣"
         3. PeriodQueen 给出市场环境上限
         
         最终仓位 = min(Kelly * DY_R3_discount, PQ_max, VanTharp_limit)
         """
         # DY_R3 折扣映射
         dy_r3_discount = {
             10: 1.0, 9: 1.0,
             8: 0.85, 7: 0.85,
             6: 0.70, 5: 0.70,
             4: 0.50, 3: 0.50,
             2: 0.30, 1: 0.0, 0: 0.0,
         }
         
         discount = dy_r3_discount.get(int(certainty_score), 0.5)
         kelly_adjusted = kelly_f * discount
         
         return min(kelly_adjusted, pq_max_size)
     ```

  3. 投票机制调整：
     ```python
     # 在 VoteDecisionEngine 中增加 DY_R3 节点
     def node_004_dy_r3_sizing(self, objects, kelly_data, pq_output):
         certainty = self._calculate_certainty(objects)
         kelly_f = kelly_data.get("half_kelly_scalar", 0.09)
         pq_max = pq_output.get("max_position", 1.0)
         
         final_size = self.calculate_final_size(certainty, kelly_f, pq_max)
         
         return "PASS", {
             "certainty_score": certainty,
             "dy_r3_discount": dy_r3_discount.get(int(certainty), 0.5),
             "final_size_pct": final_size,
         }
     ```

实现优先级：P2（中）
数据需求：现有对象卡输出 + VP 特征
```

---

## 三、DY 体系的新增对象卡评估

### 3.1 是否需要新建 DY 对象卡？

```text
评估结论：不需要新建独立的 DY_R1/R2/R3 对象卡

理由：
  1. DY 的三条规则已经被现有对象卡"分布式覆盖"
     - DY_R1 → CHZL_TREND + KD MTF（扩展多周期字段）
     - DY_R2 → MFLOW + VP（扩展位置敏感型字段）
     - DY_R3 → KELLY + PeriodQueen（扩展确定性评分）

  2. 新建对象卡会导致冗余
     - DY_R1 和 CHZL_TREND 功能高度重叠
     - DY_R2 和 MFLOW 功能高度重叠
     - 冗余对象卡会增加系统复杂度，降低可维护性

  3. "扩展而非新建"符合系统成熟原则
     - 在现有对象卡上增加字段，风险更低
     - 不需要额外的回测验证
     - 保持对象卡数量精简

替代方案：
  在现有系统中增加"DY 评分层"（DY Scoring Layer）
  - 不是独立对象卡
  - 是一个"元评分模块"，读取各对象卡输出，计算综合 DY 评分
  - 输出：certainty_score + dy_r1_passed + dy_r2_passed + dy_r3_recommendation
```

### 3.2 DY 评分层设计

```python
class DYScoringLayer:
    """
    DY 评分层：元评分模块
    不是独立对象卡，而是读取各对象卡输出，计算综合评分
    """
    
    def __init__(self):
        self.weights = {
            "chzl_trend": 0.30,
            "kd_mtf": 0.10,
            "mflow": 0.25,
            "bpb": 0.15,
            "tkr7": 0.10,
            "ytc": 0.10,
        }
    
    def calculate(self, objects: dict, vp_data: dict) -> dict:
        """
        计算 DY 综合评分
        
        Returns:
            {
                "dy_r1_passed": bool,       # 多周期对齐
                "dy_r2_passed": bool,       # 量能验证
                "certainty_score": float,   # 综合确定性 0-10
                "recommended_size_pct": float,  # 推荐仓位
                "breakdown": dict,          # 各维度得分明细
            }
        """
        # DY_R1：多周期对齐
        chzl = objects.get("CHZL_TREND", {})
        alignment_score = chzl.get("alignment_score", 0)
        dy_r1_passed = alignment_score >= 2
        
        # DY_R2：量能验证
        mflow = objects.get("MFLOW", {})
        dy_r2_passed = mflow.get("dy_r2_passed", False)
        
        # 综合确定性评分
        certainty = 0.0
        breakdown = {}
        
        for obj_id, weight in self.weights.items():
            obj = objects.get(obj_id.upper(), {})
            strength = obj.get("signal_strength", 0)  # 0-10
            contribution = strength * weight
            certainty += contribution
            breakdown[obj_id] = {
                "strength": strength,
                "weight": weight,
                "contribution": contribution,
            }
        
        # DY_R1/DY_R2 加成/惩罚
        if dy_r1_passed:
            certainty += 0.5
        if dy_r2_passed:
            certainty += 0.5
        
        certainty = min(certainty, 10.0)
        
        # 推荐仓位
        size_map = {
            10: 0.15, 9: 0.15,
            8: 0.10, 7: 0.10,
            6: 0.06, 5: 0.06,
            4: 0.03, 3: 0.03,
            2: 0.01, 1: 0.0, 0: 0.0,
        }
        recommended_size = size_map.get(int(certainty), 0.03)
        
        return {
            "dy_r1_passed": dy_r1_passed,
            "dy_r2_passed": dy_r2_passed,
            "certainty_score": round(certainty, 2),
            "recommended_size_pct": recommended_size,
            "breakdown": breakdown,
        }
```

---

## 四、DY 体系与 PeriodQueen 的联动

```text
DY 评分层与 PeriodQueen 的联动规则：

1. PeriodQueen 作为"大环境过滤器"：
   - 即使 DY 评分很高（certainty=9），如果 PeriodQueen = HALT → 不允许交易
   - PeriodQueen 的 max_size 是 DY 推荐仓位的"天花板"

2. DY 评分作为"单票精细调节器"：
   - 在 PeriodQueen 允许的范围内，DY 评分决定具体仓位
   - 例：PeriodQueen 允许 FULL（15%），DY 评分 8 → 实际仓位 10%

3. 联合决策矩阵：
   ```
                PeriodQueen
                ATTACK  POWER   GESTATION  BEAR    HALT
   DY=10        15%     12%     8%        3%      0%
   DY=8-9       12%     10%     6%        2%      0%
   DY=6-7       10%     8%      5%        1%      0%
   DY=4-5       6%      5%      3%        0%      0%
   DY<4         0%      0%      0%        0%      0%
   ```
```

---

## 五、实施路线图

```text
Phase 1：扩展现有对象卡（Week 1-2）
  - CHZL_TREND：增加多周期字段（weekly, 60min）
  - KD_MTF：增加日线 KD 字段
  - MFLOW：增加位置敏感型字段（volume_ratio, key_level）
  
Phase 2：实现 DY 评分层（Week 2-3）
  - 创建 DYScoringLayer 类
  - 集成到 VoteDecisionEngine
  - 调整投票权重
  
Phase 3：回测验证（Week 3-4）
  - 对比"有 DY 评分" vs "无 DY 评分"的绩效
  - 验证指标：夏普比率、最大回撤、胜率
  - 目标：夏普提升 > 0.1，回撤降低 > 2%
  
Phase 4：参数调优（Week 4-5）
  - DY 评分权重调优
  - 仓位映射表调优
  - 与 Kelly/PeriodQueen 的协同调优
```

---

## 六、对编程 AI 的明确指令

```text
1. 不新建 DY_R1/R2/R3 独立对象卡
2. 在现有对象卡上增加 DY 相关字段（见 2.1/2.2/2.3）
3. 创建 DYScoringLayer 元评分模块（不是对象卡）
4. DYScoringLayer 的输出作为投票机制的输入
5. 所有 DY 字段必须有默认值（backward compatible）
6. 回测时必须对比"有 DY"和"无 DY"两种配置
```

---

> 文件：DY_INTEGRATION_v1.0.md
> 生产者：Kimi（整理用户的大隐体系素材）
> 核心结论：DY 三条规则无需新建对象卡，通过扩展现有对象卡 + DY 评分层实现
> 新增模块：DYScoringLayer（元评分模块，非对象卡）
