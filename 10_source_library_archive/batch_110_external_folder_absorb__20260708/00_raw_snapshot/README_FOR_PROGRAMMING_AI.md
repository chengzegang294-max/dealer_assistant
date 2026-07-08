# 快速启动指南：给编程 AI 的入场手册

> **⚠️ 重要：如果你是第一次看到这份文档，请先阅读 `PROGRAMMING_AI_ULTIMATE_TASK_PACKAGE_v1.0.md`。**
> 那份文档是"总任务书"，告诉你从哪开始、按什么顺序读、按什么顺序写。
> 本文档是"入场手册"，补充环境配置和项目背景。两份文档都要读。

> 版本：v1.0 | 目标读者：编程 AI | 阅读时间：5 分钟

---

## 一、项目概况

### 1.1 这是什么项目

```text
项目名称：投资管家（Investment Steward）
项目目标：构建一个 A 股量化交易系统
核心特色：
  1. 中国本土治理架构（明朝内阁混合制，五态动态切换）
  2. 技术面 + 基本面 + 风控 三权分立
  3. 对象卡体系（Object Card）——可插拔的指标/策略原子
  4. 纯多头 A 股策略（T+1, 涨跌停, 小盘股分层）

技术栈：
  - 语言：Python 3.10+
  - 数据处理：polars（优先）/ pandas（兼容）
  - 回测：自研 BacktestEngine（非 vnpy/Backtrader）
  - 数据源：tushare / akshare / Wind（本地缓存）
  - 存储：Parquet（特征缓存）/ JSONL（日志）
  - 测试：pytest + hypothesis
```

### 1.2 仓库结构

```
D:\Stock\trading_assistant\          # 主仓库（当前工作目录）
├── data\                              # 数据层
│   ├── raw\                          # 原始数据（不可修改）
│   ├── processed\                    # 清洗后的数据（Feature Store）
│   └── metadata\                    # 元数据（data_catalog.json）
│
├── src\                               # 源代码层
│   ├── backtest_engine\             # 回测引擎（核心）
│   │   ├── data\                   # DataLoader
│   │   ├── objects\                # 对象卡实现
│   │   ├── pipeline\               # Pipeline 执行
│   │   ├── vote\                   # VoteDecisionEngine
│   │   ├── risk\                   # RiskArchitectureEngine
│   │   ├── execution\              # ExecutionEngine
│   │   └── performance\            # 绩效评估 + 报告生成
│   │
│   ├── governance\                  # 治理架构（明朝内阁混合制）
│   │   ├── cabinet.py              # 内阁（票拟）
│   │   ├── six_departments.py      # 六科给事中（审查）
│   │   ├── taijian.py             # 台谏系统（监察）
│   │   ├── regime_modes.py         # 五种制度模式策略
│   │   ├── controller.py           # 模式切换控制器
│   │   └── emperor_console.py      # 皇帝控制台（用户接口）
│   │
│   ├── data_pipeline\              # 数据管道（ETL）
│   │   ├── extractors\            # 数据提取器
│   │   ├── transformers\          # 数据转换器
│   │   ├── loaders\              # 数据加载器
│   │   └── validators\            # 数据验证器
│   │
│   ├── fundamental\                # A5 财报选股层
│   │   ├── mine_sweep.py          # 排雷检查
│   │   ├── scoring.py             # 财务评分
│   │   ├── valuation.py           # 估值评估（DCF + PE/PB）
│   │   └── selector.py            # A5FundamentalSelector
│   │
│   ├── dy_scoring\                # DY 评分层（大隐体系）
│   │   └── dy_layer.py            # DYScoringLayer
│   │
│   ├── utils\                      # 工具函数
│   └── tests\                      # 单元测试
│
├── docs\                            # 文档层
│   ├── objects\                    # 对象卡文档
│   ├── architecture\              # 架构文档
│   ├── reference\                 # 参考资料
│   └── reports\                  # 回测报告
│
├── config\                          # 配置层
│   ├── backtest_config.yaml       # 回测参数
│   ├── object_registry.json       # 对象卡注册表
│   ├── data_sources.json          # 数据源配置
│   └── strategy_bundles.yaml      # 策略组合配置
│
├── notebooks\                       # 分析 notebook
├── logs\                            # 日志层
└── scripts\                         # 脚本层
```

---

## 二、阅读顺序（强制）

```text
你必须按以下顺序阅读文档。每读完一份，在脑海中确认"我理解了这个文档的核心要求"，再进入下一份。

Step 1（2 分钟）：
  阅读本文档（README_FOR_PROGRAMMING_AI.md）
  目标：了解项目概况、阅读顺序、编码规范

Step 2（5 分钟）：
  阅读 INDEX_v2.0.md（文档总索引）
  目标：了解全部文档的分布和状态

Step 3（10 分钟）：
  阅读 SYSTEM_ARCHITECTURE_DRAFT.md
  目标：理解三层决策架构的核心逻辑

Step 4（15 分钟）：
  阅读 MASTER_PROGRAMMING_INSTRUCTION_v1.0.md
  目标：理解编码规范、接口标准、测试要求

Step 5（按任务选择）：
  
  如果你被分配实现【对象卡】：
    → 阅读 OBJECT_CARD_*.md（选择对应的对象卡）
    → 阅读 BACKTEST_FRAMEWORK_DESIGN_v1.0.md（了解 Pipeline 接口）
    → 阅读 GAS_12_INDICATOR_MAP_P0_A_v1.0.md（了解指标映射）
    → 开始编码
  
  如果你被分配实现【回测引擎】：
    → 阅读 BACKTEST_FRAMEWORK_DESIGN_v1.0.md
    → 阅读 VOTE_DECISION_TABLE_P0_E_v1.0.md
    → 阅读 RISK_ARCHITECTURE_P0_R_v1.0.md
    → 开始编码
  
  如果你被分配实现【治理架构】：
    → 阅读 MING_CABINET_HYBRID_ARCHITECTURE_v1.0.md
    → 阅读 EMPEROR_CONSOLE_UI_v1.0.md
    → 参考 governance_architecture.py（接口设计）
    → 开始编码
  
  如果你被分配实现【数据管道】：
    → 阅读 DATA_AVAILABILITY_AUDIT_v1.0.md
    → 阅读 USER_IDEAS_INTEGRATION_v1.0.md（ETL 章节）
    → 开始编码
  
  如果你被分配实现【选股层】：
    → 阅读 A5_FUNDAMENTAL_INTEGRATION_v1.0.md
    → 阅读 DY_INTEGRATION_v1.0.md
    → 开始编码
```

---

## 三、编码规范（强制遵守）

### 3.1 Python 代码规范

```text
1. 类型提示（Type Hints）：
   - 所有函数参数和返回值必须有类型提示
   - 使用 Python 3.10+ 的 Union 语法（| 而非 Union[]）
   - 例：def calculate(self, price: float | None = None) -> dict[str, Any]

2. 文档字符串（Docstrings）：
   - 所有类和方法必须有 Google 风格的 docstring
   - 必须包含：Args, Returns, Raises, Example
   
3. 命名规范：
   - 类名：PascalCase（RegimeModeController）
   - 函数/方法：snake_case（calculate_final_size）
   - 常量：UPPER_SNAKE_CASE（VAN_THARP_LIMIT）
   - 私有方法：_leading_underscore

4. 导入规范：
   - 标准库 → 第三方库 → 本地模块
   - 禁止使用 from module import *（污染命名空间）
   
5. 异常处理：
   - 不允许裸 except:
   - 必须捕获具体异常类型
   - 异常必须记录到日志，不能静默吞掉
```

### 3.2 数据处理规范

```text
1. 优先使用 polars 处理数据：
   - 日频数据：pandas 也可以
   - 分钟级数据：必须用 polars
   - 特征缓存：用 polars 写入 Parquet

2. 数据不可变性：
   - DataFrame 传入函数后，函数内部不得修改原始 DataFrame
   - 必须 copy() 或 clone() 后再操作

3. 缺失值处理：
   - 不允许强制填充（fillna）引入噪音
   - 缺失值必须标记为 NaN/None，并在对象卡中处理为 NONE 信号

4. 复权一致性：
   - 所有价格数据使用前复权
   - 回测时必须验证复权一致性（close ≈ amount/volume）
```

### 3.3 对象卡输出规范（最重要）

```python
# 所有对象卡必须输出的标准字段
STANDARD_OUTPUT = {
    # 身份标识
    "object_id": str,           # 例: "CHZL_BSD_P0_E"
    "object_name": str,         # 例: "缠论买卖点"
    "function_bucket": str,     # SELECTOR / EXECUTION / RISK / FILTER
    "process_layer": str,       # L1_ENV / L2_CANDIDATE / L3_ENTRY
    
    # 时间标识
    "timestamp": str,           # ISO 8601 格式
    "symbol": str,              # 例: "000001.SZ"
    "timeframe": str,           # DAILY / WEEKLY / 60MIN / 15MIN
    
    # 信号内容
    "signal_type": str,         # LONG / SHORT / NONE / ABORT
    "signal_strength": int,     # 0-10
    "signal_confidence": float, # 0.0-1.0
    
    # 互锁信息
    "lock_status": str,         # LOCKED / UNLOCKED
    "lock_reason": str,         # 互锁原因
    "filter_action": str,       # PASS / BLOCK / DEGRADE
    "target_object_id": str,    # 目标对象卡（互锁时）
    
    # 风控信息
    "risk_action": str,         # ACCEPT / REJECT / ADJUST
    "size_scalar": float,       # 仓位调节系数
    "stop_adjustment": float,   # 止损调节系数
    
    # 成熟度信息
    "maturity_status": str,     # proxy_quantizable_now / needs_extra_data / shell_only
    "data_requirement": str,    # 数据需求描述
    "effectiveness_scope": str, # 有效性范围描述
}
```

### 3.4 测试规范

```text
1. 测试覆盖率：
   - 核心逻辑（Pipeline/Vote/Risk）→ 覆盖率 ≥ 90%
   - 对象卡 → 覆盖率 ≥ 80%
   - 工具函数 → 覆盖率 ≥ 70%

2. 测试类型：
   - 单元测试：test_*.py，每个函数至少 1 个正常用例 + 2 个边界用例
   - 集成测试：test_integration_*.py，测试模块间协作
   - 回测验证：test_backtest_*.py，验证回测结果与手工计算一致

3. 测试命名：
   - 测试函数：test_{被测函数}_{场景}_{预期结果}
   - 例：test_calculate_kelly_high_winrate_returns_full_kelly

4. 测试数据：
   - 禁止使用生产数据做测试
   - 使用 fixtures 生成合成数据
   - 固定随机种子（random.seed(42)）确保可复现
```

---

## 四、关键设计原则

### 4.1 "只读结构，不预测"

```text
系统的核心哲学：
  - 对象卡不预测价格涨跌
  - 对象卡只识别"结构是否确认"
  - 交易是"结构确认后的风险暴露"，不是"价格预测"

编码体现：
  - 对象卡输出 signal_type = "LONG" 不代表"预测涨"
  - 代表"趋势结构确认，允许承担多头风险"
  - 止损必须同时输出（每笔交易必须有止损）
```

### 4.2 "承认不确定性"

```text
来自因子大赛的洞察：
  - 不要追求预测准确率
  - 追求"合理的风险暴露"
  - Kelly 公式和 VolTarget 是核心工具

编码体现：
  - 所有对象卡必须输出 confidence（置信度）
  - 低 confidence 的信号必须降级或废弃
  - 系统必须记录"预测 vs 实际"的偏差，用于自优化
```

### 4.3 "最小代理"

```text
用户的核心偏好：
  - 拒绝大而全的评分系统
  - 拒绝总仓位控制模型
  - 坚持最小代理与候选池过滤

编码体现：
  - 对象卡只输出信号，不决定仓位
  - 仓位由 RiskArchitecture（Kelly + VolTarget）决定
  - PeriodQueen 只决定"能不能做"，不决定"做多少"
```

---

## 五、常见问题（FAQ）

### Q1：我应该先实现哪个模块？

```text
推荐的实现顺序：

Phase 1（基础设施）：
  1. DataLoader（数据加载）
  2. FeatureStore（特征缓存）
  3. AuditLogger（审计日志）

Phase 2（核心引擎）：
  4. BacktestEngine（回测框架）
  5. VoteDecisionEngine（投票机制）
  6. RiskArchitectureEngine（风控架构）

Phase 3（对象卡）：
  7. PeriodQueen（情绪周期）← 必须先实现，它是"心脏"
  8. CHZL 系列（缠论结构）
  9. BPB / VP / TKR7 / YTC（执行层）
  10. MFLOW / VOLFAC（选股层）
  11. KELLY / VOLTARGET（风控层）

Phase 4（治理层）：
  12. GovernanceEngine（治理架构）
  13. EmperorConsole（控制台）

Phase 5（选股层）：
  14. A5FundamentalSelector（财报选股）
  15. DYScoringLayer（大隐评分）

Phase 6（报告）：
  16. BacktestReportGenerator（报告生成）
  17. DailyReportGenerator（日报生成）
```

### Q2：一个对象卡应该多大？

```text
代码量参考：
  - 简单对象卡（如 KD MTF）：50-100 行
  - 中等对象卡（如 VP）：200-300 行
  - 复杂对象卡（如 CHZL_BSD）：500-800 行

原则：
  - 一个对象卡一个文件
  - 核心逻辑不超过 3 个类
  - 辅助函数提取到 utils/
```

### Q3：如何处理 A 股特殊规则？

```text
T+1：
  - 买入后当天不能卖出
  - 回测时必须检查持仓天数 ≥ 1

涨跌停：
  - 涨停价 = 前收 * 1.1（ST 为 1.05）
  - 跌停价 = 前收 * 0.9（ST 为 0.95）
  - 价格触及涨跌停 → 无法成交 → 标记为 limit_atr_corrector

小盘股分层：
  - 市值 < 50 亿 → 流动性差 → 降低仓位上限
  - 市值 50-200 亿 → 正常处理
  - 市值 > 200 亿 → 流动性好 → 正常处理

纯多头：
  - 不允许做空
  - signal_type = "SHORT" 时，只用于"减仓/卖出"
```

### Q4：如何与用户的控制台交互？

```text
控制台是"观察者模式"：
  - 控制台不直接调用引擎方法
  - 引擎通过事件通知控制台
  - 控制台只读引擎状态，不修改

事件类型：
  - MEMORIAL_SUBMITTED（奏折提交）
  - REVIEW_COMPLETED（审查完成）
  - EDICT_ISSUED（圣旨下达）
  - TRADE_EXECUTED（交易执行）
  - REGIME_SWITCH（模式切换）
```

---

## 六、检查清单（编码前必读）

```text
□ 我已阅读本文档
□ 我已阅读 INDEX_v2.0.md
□ 我已阅读 SYSTEM_ARCHITECTURE_DRAFT.md
□ 我已阅读 MASTER_PROGRAMMING_INSTRUCTION_v1.0.md
□ 我清楚自己的任务属于哪个模块
□ 我已阅读对应模块的详细设计文档
□ 我理解对象卡的 STANDARD_OUTPUT 规范
□ 我理解 A 股的 T+1/涨跌停/纯多头约束
□ 我承诺使用类型提示
□ 我承诺编写测试用例
□ 我承诺记录审计日志
```

---

> 文件：README_FOR_PROGRAMMING_AI.md
> 生产者：Kimi（编程 AI 入场手册）
> 用途：任何编程 AI 必须从此文档开始阅读
> 阅读时间：5 分钟
> 核心目标：让编程 AI 在 30 分钟内理解项目全貌并开始编码
