# 外部交易系统参考汇总 v1.0

> 版本：v1.0 | 状态：参考文档 | 用途：为编程 AI 提供外部系统的设计借鉴和对比基准  
> 搜索范围：量化回测框架、多因子系统、多智能体交易、缠论自动化  
> 筛选原则：只收录与当前仓库"对象卡+互锁+投票"架构有直接可比性的系统

---

## 1. KA-MATS — 多智能体交易系统（Crypto）

> 来源：GitHub - kunal14901/KA-MATS  
> 相关性：⭐⭐⭐⭐⭐（投票机制、风控否决、多智能体架构与我们的对象卡高度对应）

### 1.1 核心架构

```
Data Agent → Alt Data Agent → Market Analyst → Thesis Agent → Strategy Agent
                                                               │
                                                               ▼
                                              ┌────────────────────────────┐
                                              │     SWARM CONSENSUS VOTE   │
                                              │  5 agents, quorum ≥ 3/5    │
                                              │     APPROVE → Risk Manager│
                                              │     REJECT  → (logged)     │
                                              └────────────────────────────┘
                                                               │
                                                               ▼
                                              ┌────────────────────────────┐
                                              │      Risk Manager          │
                                              │  Half-Kelly sizing         │
                                              │  Portfolio heat            │
                                              │  Daily loss limit          │
                                              │  Hard DD backstop          │
                                              └────────────────────────────┘
                                                               │
                                                               ▼
                                              ┌────────────────────────────┐
                                              │      Execution Agent       │
                                              └────────────────────────────┘
```

### 1.2 与我们的系统对比

| 维度 | KA-MATS | 我们的系统（设计） |
|------|---------|-------------------|
| **投票机制** | 5 agents，quorum ≥ 3/5 | 多对象卡，entry_min_votes = 3 |
| **风控否决** | Risk Manager 是 absolute veto（一票否决） | Van Tharp 2% 硬性上限 + VolTarget HALT_NEW |
| **智能体类型** | 5 个智能体（对抗、LLM、贝叶斯、市场状态、置信度） | 12 张对象卡（结构/能量/执行/风控/选股） |
| **策略确定性** | "Deterministic core — LLM is veto-only" | 所有对象卡均为确定性规则，无 LLM 干预 |
| **回测验证** | Walk-forward validated（样本外测试） | 四阶段验收：伪代码→单因子→组合→样本外 |
| **熔断机制** | WR < 38% 时 circuit breaker 暂停所有交易 | Kelly 危机模式（连续亏损 3 笔）+ VolTarget 极端波动 |
| **失败设计** | "Fail-open design"（非关键 agent 失败时继续） | 数据缺失时对象卡降级/跳过，不影响系统运行 |

### 1.3 可借鉴的设计

```text
借鉴 1：Swarm Consensus Vote 的审计追踪
  - KA-MATS：每个被 REJECT 的信号都被记录原因
  - 我们的系统：VOTE_POOL 中的 'ABORT' 信号需记录原因（票数不足/风控否决/过滤器阻断）
  - 实现建议：在统一输出接口中增加 'abort_reason' 字段

借鉴 2：Risk Manager 的 pre-trade 和 post-trade 分离
  - KA-MATS：Risk Manager 在交易前检查（pre-trade check）和交易后更新（post-trade update）
  - 我们的系统：风控层在投票前调制（pre-vote）和投票后强制执行（post-vote）
  - 对应：Van Tharp 2% 是 post-trade（持仓后检查）；VolTarget 是 pre-trade（开仓前调制）

借鉴 3：Fail-open design
  - KA-MATS：非关键 agent 失败时 pipeline 继续
  - 我们的系统：DataLoader 的降级策略（对象卡数据缺失时跳过，不影响其他对象卡）
  - 实现建议：在 DataLoader 中实现 "SKIP_OBJECT_CARD" 和 "DEGRADE_TIMEFRAME" 两种降级模式
```

---

## 2. Quant67 — 六层接口统一架构

> 来源：quant67.com / 量化交易系统架构：研究、回测、模拟、实盘四套环境  
> 相关性：⭐⭐⭐⭐（接口驱动的统一架构与我们的对象卡统一输出接口高度一致）

### 2.1 核心抽象

```python
# 六层接口定义（Python Protocol）

class DataSource(Protocol):
    def historical_bars(self, symbol, start, end, freq) -> pd.DataFrame: ...
    def stream_bars(self, symbols, freq) -> Iterator[Bar]: ...

class FeaturePipeline(Protocol):
    version: str
    def transform(self, bars: pd.DataFrame) -> pd.DataFrame: ...

class SignalGenerator(Protocol):
    def predict(self, features: pd.DataFrame) -> pd.Series: ...

class PortfolioConstructor(Protocol):
    def target_weights(self, alpha, current_positions) -> pd.Series: ...

class OrderRouter(Protocol):
    def submit(self, order: Order) -> str: ...
    def cancel(self, client_order_id: str) -> None: ...

class RiskManager(Protocol):
    def pre_trade_check(self, order: Order) -> Optional[str]: ...  # None=通过, str=拒因
    def post_trade_update(self, fill: Fill) -> None: ...
    def kill_switch(self) -> bool: ...
```

### 2.2 与我们的系统对比

| 维度 | Quant67 | 我们的系统（设计） |
|------|---------|-------------------|
| **接口抽象** | 6 层 Protocol（DataSource → FeaturePipeline → SignalGenerator → PortfolioConstructor → OrderRouter → RiskManager） | 6 功能层（结构 → 能量 → 执行 → 风控 → 选股 → 组合构建） |
| **数据流** | DataSource → FeaturePipeline → SignalGenerator → PortfolioConstructor → OrderRouter | DataLoader → 对象卡计算 → 互锁检查 → 过滤器 → 风控调制 → 投票池 → 执行 |
| **风控位置** | RiskManager 独立层，pre_trade_check + post_trade_update + kill_switch | 风控层在投票前和投票后两次介入 |
| **多环境** | 研究 / 回测 / 模拟 / 实盘 四套环境 | 目前只有回测设计，未来可扩展模拟/实盘 |
| **并发回测** | 支持大规模并发（Ray/Dask），任务幂等，结果缓存 | 尚未设计，但可借鉴（对象卡独立计算天然可并行） |

### 2.3 可借鉴的设计

```text
借鉴 1：Protocol 接口定义
  - Quant67：用 Python Protocol 定义每层接口，实现松耦合
  - 我们的系统：对象卡统一输出接口（第 2.1 节）可借鉴 Protocol 思路
  - 实现建议：将对象卡统一输出接口改为 Protocol 形式，方便编程 AI 实现

借鉴 2：回测任务幂等性
  - Quant67："同样的输入必须产出同样的输出"，要求随机数种子、数据快照、依赖版本固化
  - 我们的系统：回测参数（entry_min_votes, stop_k, atr_n）已冻结，但需明确版本控制
  - 实现建议：每次回测记录参数版本、数据哈希、对象卡版本号，确保可复现

借鉴 3：中间结果缓存
  - Quant67：对 (数据快照, 特征版本) 的中间结果做缓存，避免反复重算特征
  - 我们的系统：对象卡计算（如缠论笔/中枢）计算量大，应缓存结果
  - 实现建议：FeaturePipeline 的 transform 结果存入 Feature Store，按 (symbol, date, version) 索引
```

---

## 3. B3 Pipeline — 巴西股市特征发现引擎

> 来源：GitHub - nickmaglowsch/b3-pipeline-data-and-backtest-framework  
> 相关性：⭐⭐⭐⭐（IC-based 因子评估 + Feature Store + 自动剪枝，与我们的因子测试流程高度对应）

### 3.1 核心架构

```
Data Pipeline → Feature Store → Feature Discovery Engine → Backtest Engine
     │                │                    │
     ▼                ▼                    ▼
SQLite/IBOV   registry.json        IC Evaluation
                                   (Spearman rank corr)
                                   4 forward horizons
                                   Pruning: NaN → IC → Correlation → Cap
```

### 3.2 Feature Discovery 流程（12 步）

| 步骤 | 内容 | 与我们的系统对应 |
|------|------|----------------|
| 1 | 加载数据 | DataLoader.get_daily_ohlcv() |
| 2 | 初始化 Feature Store | 检查数据哈希，缓存失效时重算 |
| 3 | 计算 Universe Mask | 流动性过滤（ADTV ≥ R$1M, price ≥ R$1, 200+ days） | 我们的选股池：剔除 ST、退市、上市不足 1 年 |
| 4 | 生成 Level 0 + Level 1 特征 | 基础信号 + rank/zscore 变换 | 对象卡的基础字段（如 mflow_sellord_ratio） |
| 5 | 评估 Level 0+1 | IC 计算 | 我们的单因子回测验收 |
| 6 | 选择 Top 特征进入 Level 2 | 基于 IC_IR 筛选 | 我们的 proxy_quantizable_now 判定 |
| 7 | 生成 Level 2 特征 | delta, ratio, product 等算子 | 对象卡的派生字段（如 mflow_divergence_score） |
| 8 | 评估 Level 2 | 再次 IC 计算 | 组合回测 |
| 9 | 剪枝 | NaN 过滤 → IC 阈值 → 相关性去重 → 上限 500 | 我们的重叠/替代分析（overlaps_with） |
| 10 | 导出特征目录 | JSON 格式供回测消费 | 对象卡统一输出接口 |
| 11 | 生成报告 | 图表和文本 | 回测报告 |
| 12 | 保存 Feature Store | 持久化 | 数据缓存 |

### 3.3 IC 评估指标（与 SBKT_F014/F006 对应）

| B3 指标 | 说明 | 我们的对应指标 |
|---------|------|---------------|
| `mean_ic` | 平均 IC | SBKT_F014 中的 IC>0 占比 |
| `ic_ir` | IC Information Ratio = mean_ic / ic_std | SBKT_F014 中的 IR |
| `ic_t_stat` | IC 统计显著性 | 我们的 signal_confidence |
| `pct_positive_ic` | IC > 0 的比例 | SBKT_F014 中的 IC>0 占比 |
| `turnover` | 1 - 平均秩自相关（交易成本代理） | 我们的换手率约束（未设计，需补充） |
| `decay_1d/5d/20d` | 滞后特征值的 IC（信号持久性） | 我们的信号衰减检查（如 YTC 的 EXPIRED 超时） |
| `train/test split` | 前 70% vs 后 30% 的 IC（过拟合检测） | 我们的样本外测试（Week 7-8） |

### 3.4 可借鉴的设计

```text
借鉴 1：Feature Store 缓存机制
  - B3：每个特征一个 Parquet 文件，按 (date, ticker, value) 长格式存储
  - 我们的系统：对象卡输出字段多，需要类似的缓存机制
  - 实现建议：每个对象卡每个时间框架输出一个 Parquet 文件，按 (symbol, date) 索引
  - 好处：回测时直接加载预计算的特征，避免重复计算（特别是缠论笔/中枢）

借鉴 2：IC 驱动的因子评估
  - B3：用 Spearman rank correlation 评估每个特征，4 个前瞻周期（5d/10d/20d/60d）
  - 我们的系统：单因子回测验收需明确"用什么指标评估因子有效性"
  - 实现建议：
    - 日频对象卡（MFLOW/VOLFAC）用 5d/10d 前瞻
    - 周线对象卡（KD MTF/缠论趋势）用 20d/60d 前瞻
    - 验收指标：|mean_ic| > 0.02 且 ic_ir > 0.5

借鉴 3：相关性去重（Correlation Dedup）
  - B3：两个特征 Spearman 相关 > 0.90 时，保留 IC_IR 更高的
  - 我们的系统：对象卡之间有 overlaps_with 关系，但尚未量化
  - 实现建议：在组合回测阶段，计算各对象卡输出信号的相关性矩阵，若 > 0.90 则标记为冗余
```

---

## 4. vnpy — 多因子回测引擎

> 来源：CSDN / vnpy 量化策略开发实战  
> 相关性：⭐⭐⭐（回测引擎设计、参数搜索、过拟合处理有参考价值）

### 4.1 回测引擎参数设置

```python
from vnpy.alpha.strategy.backtesting import BacktestingEngine
from datetime import datetime

engine = BacktestingEngine(lab)

engine.set_parameters(
    vt_symbols=component_symbols[:100],  # 标的池
    interval=Interval.DAILY,              # 时间框架
    start=datetime(2017, 1, 1),         # 回测起点
    end=datetime(2020, 8, 31),            # 回测终点
    capital=1000000,                     # 初始资金
    annual_days=240                       # 年化交易日
)

engine.add_strategy(CSI300LGBStrategy, {}, signal_df)
engine.load_data()
engine.run_backtesting()

# 绩效评估
daily_df = engine.calculate_result()
statistics = engine.calculate_statistics()
engine.show_chart()
engine.show_performance("000300.SSE")  # 基准对比
```

### 4.2 常见问题与解决方案（与我们的系统对照）

| 问题 | vnpy 方案 | 我们的系统方案 |
|------|----------|---------------|
| 过拟合 | 增加正则化、交叉验证、简化模型、增加数据量 | 我们的成熟度升级验收（v1.0→v1.4），样本外测试强制要求 |
| 策略失效 | 考虑交易成本与滑点、样本外测试、定期重训练、严格止损 | 我们的 A 股适配：双边 0.25% 成本、T+1 惩罚、涨跌停处理 |
| 计算性能 | 用 polars 替代 pandas、并行计算、数据预处理流水线、缓存中间结果 | 我们的 Feature Store 缓存、对象卡并行计算（未来扩展） |

### 4.3 可借鉴的设计

```text
借鉴 1：回测引擎的模块化接口
  - vnpy：BacktestingEngine 提供 set_parameters / add_strategy / load_data / run_backtesting / calculate_statistics
  - 我们的系统：回测框架设计文档中定义了 Pipeline，但尚未细化到类/方法级别
  - 实现建议：编程 AI 实现时，参考 vnpy 的 BacktestingEngine 接口设计，但适配我们的对象卡架构

借鉴 2：基准对比（show_performance）
  - vnpy：支持以沪深 300 为基准对比策略表现
  - 我们的系统：回测验收中要求与"无信号"基准和"买入持有"基准对比
  - 实现建议：回测引擎必须支持至少两种基准：纯现金持有（0%）和买入持有（等权指数）

借鉴 3：polars 替代 pandas
  - vnpy：建议用 polars 替代 pandas 提升性能
  - 我们的系统：A 股全市场 5000+ 标的，日频数据量巨大，polars 是明智选择
  - 实现建议：DataLoader 和 FeaturePipeline 默认使用 polars，pandas 仅作为兼容层
```

---

## 5. 缠论自动化工具（国内生态）

> 来源：通达信/飞狐交易师缠论指标、知乎/雪球/百度知道多篇文章  
> 相关性：⭐⭐⭐（缠论自动化实现的技术细节，验证我们的对象卡字段定义是否完整）

### 5.1 国内缠论工具的核心功能（从多篇搜索结果提炼）

```text
功能 1：自动分笔
  - 黄色线表示分笔
  - 自动识别顶分型和底分型
  - 旧笔规则：顶底之间 ≥ 2 根独立 K 线
  - 我们的对象卡：CHZL_BI 已定义 bi_direction / bi_high / bi_low / bi_status

功能 2：自动线段
  - 蓝色线表示线段
  - 线段由至少三笔构成（特征序列法）
  - 我们的对象卡：CHZL_BI 是基础，线段是更高层结构，当前对象卡体系中未单独定义线段对象
  - 缺口：是否需要补充 CHZL_XD（线段）对象卡？→ 建议暂不补充，用 CHZL_BI + CHZL_ZS 覆盖

功能 3：自动中枢
  - 橙色框体 = 笔中枢
  - 蓝色框体 = 线段中枢
  - 我们的对象卡：CHZL_ZS 已定义 ZG / ZD / ZZ / ZS_state
  - 验证：国内工具的中枢识别与我们的对象卡定义一致（三段重叠区间）

功能 4：自动买卖点
  - 紫色数字 = 1Buy/2Buy/3Buy
  - 绿色数字 = 1Sell/2Sell/3Sell
  - 我们的对象卡：CHZL_BSD 已定义 bsd_type / bsd_stop_price / bsd_is_trailing
  - 验证：国内工具的买卖点逻辑与我们的对象卡一致（背驰/回测前低/离开中枢）

功能 5：多周期支持
  - 支持日 K/周 K/月 K/60min/30min/15min/5min
  - 我们的对象卡：支持多时间框架（DAILY/WEEKLY/60MIN/15MIN/5MIN）
```

### 5.2 国内缠论工具的局限性（与我们的对象卡对比）

| 局限 | 国内工具 | 我们的对象卡优势 |
|------|----------|-----------------|
| 平台锁定 | 通达信/飞狐交易师专用，无法跨平台 | 对象卡是纯文本规范，任何平台可复现 |
| 回测困难 | 看盘口一一核对，无法批量回测 | 字段冻结后可直接批量回测 |
| 参数主观 | 中枢级别、线段定义有分歧 | 对象卡明确旧笔规则、明确参数 |
| 无风控 | 仅标记买卖点，无止损/仓位管理 | BSD 对象卡已定义三类止损和 Kelly/VolTarget 联动 |
| 无互锁 | 独立指标，不与其他系统配合 | 对象卡之间有明确的互锁规则 |

### 5.3 可借鉴的技术细节

```text
借鉴 1：通达信缠论指标公式的实现方式
  - 国内工具用通达信公式语言实现缠论，语法类似 C
  - 我们的系统：Python 实现，但可参考通达信公式的逻辑顺序（分型 → 笔 → 中枢 → 买卖点）
  - 实现建议：编程 AI 实现时，按此顺序分模块计算，每步输出与对象卡字段一致

借鉴 2："泽熙缠论"的优化处理
  - 泽熙缠论优化了一些特殊缠论定义，使其更适配实战（波段+低吸）
  - 我们的对象卡：已明确旧笔规则，但需验证是否处理"包含关系"和"新笔/旧笔分歧"
  - 实现建议：在缠论笔推导代码中，明确标注使用的是"旧笔规则"，避免新旧笔混淆

借鉴 3：MACD 面积计算
  - 国内工具用 MACD 柱状图面积判断背驰
  - 我们的对象卡：CHZL_BEICHI 已定义 MACD 面积公式（a段 vs c段）
  - 验证：国内工具的背驰逻辑与我们的对象卡一致，但需确认 MACD 参数（12,26,9）
```

---

## 6. 综合对比：我们的系统定位

### 6.1 与四个参考系统的对比矩阵

| 维度 | KA-MATS | Quant67 | B3 Pipeline | vnpy | 我们的系统（设计） |
|------|---------|---------|-------------|------|-------------------|
| **市场** | Crypto | 通用 | 巴西股市 | 通用 | A 股为主 + 外汇 |
| **架构** | 多智能体 | 六层接口 | Pipeline+Feature Store | 模块化引擎 | 对象卡+互锁+投票 |
| **信号来源** | 5 agents | 策略 Protocol | 因子发现 | 策略类 | 12 张对象卡 |
| **投票机制** | 3/5 quorum | 无（PortfolioConstructor 分配权重） | 无（IC 筛选） | 无 | entry_min_votes=3 |
| **风控** | Risk Manager 绝对否决 | RiskManager pre/post trade | 无独立风控 | 止损/仓位 | 三层风控（Van Tharp + Kelly + VolTarget） |
| **回测验证** | Walk-forward | 四套环境 | IC 评估 + 回测 | 标准回测 | 四阶段验收 |
| **数据缓存** | 无 | 无 | Feature Store | 无 | 建议 Feature Store |
| **并发** | 无 | Ray/Dask | 无 | 无 | 对象卡天然可并行 |
| **成熟度** | 已实现 | 已实现 | 已实现 | 已实现 | 架构设计阶段 |

### 6.2 我们的系统独特优势

```text
优势 1：对象卡的可插拔设计
  - 12 张对象卡各自独立，可单独验证、单独升级、单独替换
  - 新对象卡只需符合统一输出接口，即可无缝接入系统
  - 对比：KA-MATS 的 5 agents 是固定架构，难以扩展

优势 2：成熟度分级管理
  - 每个对象卡有明确的 maturity_status（FROZEN_FIELDS → PROXY_QUANTIZABLE）
  - 系统可以混合运行不同成熟度的对象卡（如 proxy_quantizable 的 VOLFAC + 已冻结的 CHZL_BSD）
  - 对比：其他系统没有显式的成熟度分级

优势 3：A 股特化适配
  - T+1、涨跌停、小盘股分层、资金流向等均为 A 股定制
  - 对比：其他系统要么通用（Quant67/vnpy），要么针对其他市场（B3/巴西、KA-MATS/Crypto）

优势 4：哲学约束（不编码内容，但影响架构）
  - 只读结构，不预测
  - 拒绝强行公式化哲学/心法
  - 成熟度保守原则（只有常规数据可落地的保留 proxy_quantizable_now）
  - 对比：其他系统没有明确的"NOT_QUANT_YET"或"shell_only"分类
```

### 6.3 我们的系统待改进项（从参考系统学到）

```text
待改进 1：Feature Store 缓存机制（从 B3 学习）
  - 当前：无缓存设计，每次回测重新计算所有对象卡
  - 改进：每个对象卡每个时间框架输出一个 Parquet 文件，按 (symbol, date, version) 索引
  - 优先级：高（缠论笔/中枢计算量大，缓存收益高）

待改进 2：并发回测（从 Quant67 学习）
  - 当前：单线程设计（未考虑并发）
  - 改进：每个对象卡独立计算，可用 multiprocessing.Pool 并行
  - 优先级：中（第一批回测只有 4 个对象卡，并发收益有限；但后续 12 个对象卡并发收益大）

待改进 3：换手率约束（从 B3 学习）
  - 当前：对象卡无换手率评估
  - 改进：在单因子回测中增加 turnover 指标（1 - 平均秩自相关）
  - 优先级：低（A 股 T+1 本身限制了换手率，但长期仍需要评估）

待改进 4：回测基准对比（从 vnpy 学习）
  - 当前：验收标准中有"无信号"基准，但未明确实现方式
  - 改进：回测引擎必须支持至少两种基准（纯现金持有 + 买入持有）
  - 优先级：中（组合回测阶段必须用到）

待改进 5：审计追踪（从 KA-MATS 学习）
  - 当前：VOTE_POOL 中的 ABORT 信号未记录原因
  - 改进：在统一输出接口中增加 'abort_reason' 字段
  - 优先级：中（方便调试和优化）
```

---

## 7. 附录：参考系统链接

| 系统 | 链接 | 类型 | 关键参考点 |
|------|------|------|-----------|
| KA-MATS | https://github.com/kunal14901/KA-MATS | GitHub | 投票机制、风控否决、Fail-open |
| Quant67 | https://quant67.com/post/quant/27-trading-system-arch | 博客 | 六层接口、并发回测、中间缓存 |
| B3 Pipeline | https://github.com/nickmaglowsch/b3-pipeline-data-and-backtest-framework | GitHub | Feature Store、IC 评估、相关性去重 |
| vnpy | CSDN 文章 | 教程 | 回测引擎接口、基准对比、性能优化 |

---

> 文件：EXTERNAL_SYSTEM_REFERENCE_v1.0.md  
> 生产者：Kimi（基于 kimi_search_v2 搜索结果整理）  
> 状态：参考文档，与 BACKTEST_FRAMEWORK_DESIGN_v1.0.md 配合使用  
> 建议：编程 AI 实现时，优先借鉴 KA-MATS 的投票审计和 Quant67 的接口设计，B3 的 Feature Store 作为未来优化方向
