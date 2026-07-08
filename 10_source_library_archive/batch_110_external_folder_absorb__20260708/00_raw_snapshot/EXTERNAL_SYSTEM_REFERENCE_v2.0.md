# 外部系统参考 v2.0 — 国内量化交易系统补充资料

> **文档编号**: REF-EXT-v2.0
> **创建日期**: 2026-07-07
> **更新说明**: 响应"还找新系统吗"指令，追加搜索国内主流A股量化框架，作为编码AI的架构参考与避坑指南。
> **与既有文档关系**: 本文件为 `EXTERNAL_SYSTEM_REFERENCE_v1.0.md` 的增量补充，不替代原有4大系统（QuantConnect Lean、Backtrader、vnpy、Qlib），而是扩展国内生态全景。

---

## 1. 搜索方法说明

| 维度 | 查询1 | 查询2 | 查询3 |
|------|-------|-------|-------|
| 关键词 | `A股量化交易系统 开源框架 回测引擎 国内` | `quantitative trading system architecture A-share China` | `vnpy backtrader backtest A股 对比 量化平台` |
| 结果数 | 10条 | 10条 | 10条 |
| 数据时点 | 2026-07-07 | 2026-07-07 | 2026-07-07 |

> 所有信息均来自公开网络检索，仅作为架构参考。我们不直接使用这些系统的代码，而是借鉴其设计思想、模块划分和A股适配方案。

---

## 2. 国内框架全景对比表

| 框架 | 核心类型 | 性能 | 实盘支持 | 社区活跃度 | A股适配 | 与我们的关系 |
|------|----------|------|----------|------------|---------|-------------|
| **vnpy** (VeighNa) | 事件驱动/平台 | 中等 | ⭐⭐⭐⭐⭐ 核心功能 | 非常活跃 | 原生支持 | **对标参考**：模块划分、Gateway接口、风控模块设计 |
| **WonderTrader** (wtpy) | C++核心+Python接口 | 高 | ⭐⭐⭐⭐⭐ | 活跃 | 原生支持 | **性能参考**：C++核心分层、UFT高频引擎、服务/应用分层 |
| **Hikyuu** | C++/Python混合 | 高 | ⭐⭐⭐⭐ | 较活跃 | 原生支持 | **组件化参考**：积木化系统交易、C++核心加速、条件选股 |
| **Qlib** (微软) | 向量化/AI | 高 | ⭐⭐ 较弱 | 活跃(MS) | 支持但非核心 | **AI管道参考**：标准化数据格式、Alpha158因子、模型训练管道 |
| **Backtrader** | 事件驱动 | 中等 | ⭐⭐⭐ 支持 | 活跃 | 需适配 | **事件驱动参考**：精细订单模拟、多数据源、参数优化 |
| **VectorBT** | 向量化 | 极高 | ⭐⭐ 较弱 | 活跃 | 需适配 | **向量化参考**：NumPy/Numba批量计算、多参数扫描、Plotly可视化 |
| **SimTradeLab** | 事件驱动 | 中等 | ⭐⭐ 回测为主 | 新兴 | 原生支持 | **PTrade兼容参考**：语法兼容、事件生命周期、Web界面 |
| **Zipline** | 事件驱动 | 中等 | ⭐⭐ 需扩展 | 社区维护 | 需适配 | **历史参考**：Quantopian遗产，风险分析模块 |
| **PyBroker** | 向量化 | 高 | ⭐ 不支持 | 较低 | 需适配 | **极简参考**：现代API、类型提示、快速原型 |
| **QuantConnect Lean** | 模块化 | 高 | ⭐⭐⭐⭐ | 活跃 | 需适配 | **架构参考**：IDataFeed/ITransactionHandler等5大接口 |

---

## 3. 关键框架深度拆解

### 3.1 vnpy (VeighNa) — 国内实盘标杆

- **GitHub**: 28.4K Stars，国内用户最多的量化开源项目
- **核心架构**: 事件驱动多线程引擎 (`event`模块)
- **交易接口**: 40+接口，覆盖CTP/富途/币安等，统一Gateway接口
- **模块划分** (与我们治理架构的对照):
  - `strategy` → StrategyBundles（策略包）
  - `risk_manager` → SixDepartments（六科给事中）+ RiskGuard（风控对象卡）
  - `database` → DataPipeline（数据管道）
  - `alpha` (vnpy 4.0新增) → AI多因子/ML策略开发，含Lasso/LightGBM/MLP
- **vnpy 4.0 新亮点**: 新增 `vnpy.alpha` 模块，专用于AI量化策略，提供dataset/model/strategy/lab/notebook五层结构
- **我们可借鉴**: Gateway接口的抽象方式、CTP实盘接入、风控模块的前端规则限制（流控/撤单次数限制）
- **我们不必照搬**: GUI界面（我们采用纯CLI+ANSI仪表盘）、MongoDB依赖（我们优先Parquet）

### 3.2 WonderTrader (wtpy) — 高性能C++核心

- **核心**: C++底层引擎，Python应用层SDK
- **架构**: 服务层(C++ Core) + 应用层(Python) 清晰分层
- **回测**: 支持HFT高频和中低频回测
- **性能优势**: 数据处理和事件驱动效率显著高于纯Python方案
- **我们可借鉴**: 服务/应用分层思想、C++核心加速策略（未来优化方向）、UFT引擎设计（高频场景参考）
- **我们不必照搬**: C++核心（初期Python优先，后期可嫁接）、高频交易场景（我们的核心是中低频）

### 3.3 Hikyuu — 积木化系统交易

- **核心**: C++/Python混合，超快数据加载
- **性能标杆**: A股全市场1913万日K线，HDF5首次加载6秒，计算166毫秒
- **设计理念**: 系统交易理念组件化，积木化积累
  - 系统指示器 → 条件选股 → 信号指示器 → 止损/止盈 → 资金管理
- **我们可借鉴**: 积木化组件设计（与我们的对象卡思想高度契合）、HDF5存储方案、全市场快速计算
- **我们不必照搬**: 整体架构较重，社区规模小于vnpy

### 3.4 Qlib (微软) — AI量化管道

- **背景**: 微软亚洲研究院，17.5K Stars
- **核心定位**: AI量化研究平台，不是实盘工具
- **标准化**: Qlib Dataloader统一数据格式
- **Alpha158**: 内置K线形态/价格趋势/时序波动等多维度因子
- **模型集成**: LightGBM/LSTM/XGBoost
- **我们可借鉴**: 因子工程标准化管道、Alpha158因子库（可移植为对象卡）、模型评估基准
- **我们不必照搬**: 向量化回测精度（我们需要事件驱动）、实盘非核心功能

### 3.5 SimTradeLab — PTrade兼容的社区框架

- **灵感来源**: PTrade事件驱动架构
- **生命周期**: `initialize` → `before_trading_start` → `handle_data`
- **数据支持**: CSV/AkShare/Tushare，智能切换主备数据源
- **Web界面**: 策略管理/回测执行/结果分析/报告中心
- **PTrade兼容**: 语法高度兼容，策略可双向迁移
- **我们可借鉴**: PTrade兼容层的API设计（如果我们未来需要对接券商）、事件生命周期命名、数据源自动切换机制
- **我们不必照搬**: Web界面（我们纯CLI）、社区成熟度（较新）

---

## 4. 学术研究前沿

### 4.1 "Mask-First" A股量化系统 (arXiv 2025)

- **核心思想**: 每个计算算子显式接受并传播布尔可交易mask，消除滚动窗口算子在下游过滤前摄入非可执行价格的污染
- **成果**: 合成数据Sharpe 2.05，真实A股数据Sharpe 1.63（2022-2024）
- **贡献分解**: mask合约贡献0.44 Sharpe，Adjusted-MSE损失贡献0.27，GBM增强贡献0.19，Ledoit-Wolf收缩贡献0.18
- **结论**: 在有填充缺口的微观结构市场中，数据质量工程主导模型架构作为alpha来源
- **我们可借鉴**: mask-first数据管道设计（避免ST/停牌/涨跌停的污染传播）、因子纯度控制

### 4.2 多日期周转深度学习系统 (arXiv 2025)

- **框架**: 5个互联模块：截面预测 → 开盘信号分布 → 动态仓位规模 → 网格优化止盈止损 → 多粒度波动率择时
- **数据**: 2010-2020训练，2021-2024测试
- **表现**: 年化15.2%，最大回撤4.8%，Sharpe 1.87，日持仓50-100只，最大持有9天
- **我们可借鉴**: 多模块管道设计、截面预测+择时滤波分离、动态仓位规模（市值+流动性约束）、网格优化退出参数

---

## 5. 选型矩阵（如果我们需要用外部框架）

> 声明：当前架构决策是**自研为主**，以下仅作为极端情况（如快速实盘上线）的备选方案。

| 我们的需求 | 首选外部框架 | 原因 |
|-----------|-------------|------|
| 纯回测研究 | Backtrader/VectorBT | 灵活、文档全、社区大 |
| 国内实盘一体化 | vnpy | 40+接口、CTP原生、风控完善 |
| 高性能回测 | WonderTrader/Hikyuu | C++核心、HDF5、事件驱动高效 |
| AI/ML因子研究 | Qlib | 微软维护、Alpha158、模型管道完整 |
| 快速A股原型 | SimTradeLab | PTrade兼容、AkShare免费数据源 |
| 参数扫描优化 | VectorBT | 向量化、Numba加速、多参数组合 |

---

## 6. 技术栈与中间件参考

| 中间件 | 用途 | 我们当前方案 | 备选 |
|--------|------|-----------|------|
| **数据存储** | 历史行情存储 | Parquet + zstd | HDF5 (Hikyuu/WonderTrader) |
| **数据接口** | A股实时/历史数据 | Wind API + 自有数据源 | AkShare/Tushare (免费) |
| **计算引擎** | 特征计算/回测 | Python + polars | NumPy/Numba (VectorBT) |
| **事件系统** | 事件驱动回测 | 自研事件引擎 | vnpy event engine |
| **可视化** | 回测结果展示 | matplotlib/seaborn | Plotly (VectorBT/SimTradeLab) |
| **数据库** | 元数据/交易记录 | 本地文件/Parquet | MongoDB (vnpy) / SQLite (Backtrader) |
| **Web服务** | 远程监控 | 暂无 | vnpy web_trader / SimTradeLab Web界面 |

---

## 7. 与既有系统架构的对照映射

```
我们的三层决策架构                          外部框架对应模块
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PeriodQueen (环境识别)      ←────→    Hikyuu 系统指示器 / Qlib 市场状态模型
StrategyBundles (策略选择)  ←────→    vnpy strategy engine / Backtrader Strategy
Vote+Risk (执行管理)        ←────→    vnpy risk_manager / WonderTrader 风控层
DataPipeline (数据管道)      ←────→    vnpy database / Qlib Dataloader / SimTradeLab多数据源
Governance (治理)           ←────→    vnpy 4.0 alpha.lab (研究流程管理)
DY Scoring (元评分)         ←────→    Qlib 模型评估基准 / Alpha158因子集合
A5 Fundamental (基本面)    ←────→    Qlib 基本面特征 / SimTradeLab 条件选股
```

---

## 8. 设计原则：借鉴但不依赖

1. **接口设计参考**: vnpy的Gateway抽象、Qlib的Dataloader标准化、Backtrader的Data Feed接口
2. **性能优化参考**: WonderTrader的C++分层、Hikyuu的HDF5存储、VectorBT的NumPy/Numba向量化
3. **A股适配参考**: 涨跌停/ST处理（mask-first论文）、集合竞价（多日期周转论文）、T+1约束（vnpy CTA模块）
4. **风控机制参考**: vnpy risk_manager的流控/撤单限制、Lean的ITransactionHandler订单生命周期
5. **AI管道参考**: Qlib的dataset→model→strategy→lab流程、Alpha158因子库

**绝不照搬**: 任何外部框架的完整架构、GUI界面、数据库依赖、特定云平台绑定。

---

## 9. 对编程AI的指令

> 本文件作为 `EXTERNAL_SYSTEM_REFERENCE_v1.0.md` 的v2.0补充，放入 `docs/reference/` 目录。
> 编程AI在实现以下模块时，应查阅本文件获取设计参考：

- **数据管道 (`src/data_pipeline/`)**: 参考 Qlib Dataloader 标准化、SimTradeLab 多数据源切换、Hikyuu HDF5 方案
- **事件引擎 (`src/backtest_engine/`)**: 参考 Backtrader 事件驱动模型、vnpy event engine 多线程设计、Lean 的 IDataFeed/ITransactionHandler 接口划分
- **风控模块 (`src/governance/risk_guard.py`)**: 参考 vnpy risk_manager 的前端规则限制（流控/撤单次数）
- **因子计算 (`src/fundamental/`, `src/backtest_engine/factors/`)**: 参考 Qlib Alpha158 因子库、mask-first 论文的污染消除方法
- **治理控制台 (`prototype_console.py`)**: 参考 SimTradeLab 的 Web 界面信息面板设计（但保持纯 ANSI 终端）
- **AI模块 (`src/ai/`, 未来)**: 参考 Qlib dataset/model/strategy/lab/notebook 五层结构、vnpy 4.0 alpha 模块

---

**END OF DOCUMENT**
