# 数据可用性审计清单 v1.0

> 版本：v1.0 | 状态：待逐项人工确认 | 目标：为编程 AI 提供明确的数据边界条件  
> 覆盖：12 张对象卡的全部数据需求 | 审计结果决定回测排期的可行性

---

## 1. 审计说明

### 1.1 为什么需要这份清单

排期表假设数据已就绪，但**实际数据环境可能不完全匹配**。如果编程 AI 在编码时假设数据存在而实际缺失，会导致回测框架无法运行。这份清单的目的是：**在编码前，逐条确认数据可用性，并给出替代方案或降级路径**。

### 1.2 审计格式

每项数据需求按以下格式记录：

```text
数据项：[名称]
必需性：MUST（没有则该对象卡无法运行）/ SHOULD（没有则功能降级）/ NICE（有则增强，无则跳过）
当前状态：AVAILABLE（已有）/ PARTIAL（部分有）/ MISSING（缺失）/ UNKNOWN（待确认）
获取路径：已有的数据文件路径或获取方式
替代方案：若缺失，用什么替代
降级路径：若替代也无，该对象卡如何降级
审计人：[待填写]
审计日期：[待填写]
```

---

## 2. 基础数据层（所有对象卡的共同输入）

### 2.1 日 OHLCV（前复权）

```text
数据项：日 OHLCV（前复权）
字段：date, open, high, low, close, volume, amount, symbol, adjust_factor
时间范围：2018-01-01 至 2025-06-30（至少 7 年半）
股票池：全 A 股（剔除 ST、退市、上市不足 1 年）

必需性：MUST（所有对象卡的基础输入）
当前状态：UNKNOWN（待确认）
获取路径：
  - 备选 1：D:\Stock\trading_analysis\data\ 目录下是否有历史数据？
  - 备选 2：D:\Stock\trading_assistant\data\ 目录下是否有历史数据？
  - 备选 3：使用 akshare / tushare / baostock 下载
  
替代方案：
  - 若全 A 股数据缺失，可用沪深 300 + 中证 500 + 中证 1000 成分股（约 1800 只）
  - 若时间范围不足，回测区间缩短至数据可用区间

降级路径：
  - 若完全缺失：所有回测工作无法进行，需先获取数据

审计人：[待填写]
审计日期：[待填写]
```

### 2.2 周线 OHLCV

```text
数据项：周线 OHLCV（前复权）
字段：同日线，但时间框架为周

必需性：MUST（KD MTF 多周期、YTC S/R 框架、缠论走势类型需要周线）
当前状态：UNKNOWN（待确认）
获取路径：
  - 从日线合成（pandas resample('W')）
  - 或已有现成周线数据
  
替代方案：
  - 从日线合成是标准做法，无需额外获取

降级路径：
  - 若日线缺失，周线也无法合成

审计人：[待填写]
审计日期：[待填写]
```

### 2.3 分钟级 OHLCV（60min / 15min / 5min）

```text
数据项：分钟级 OHLCV
时间范围：2019-01-01 至 2025-06-30（分钟级数据通常不会保留 2018 年前）
股票池：与日线一致

必需性：SHOULD（YTC 多周期 S/R 需要 60min；VP 分钟级需要 5min；TK 策略需要 1H/15min）
当前状态：UNKNOWN（待确认）
获取路径：
  - 备选 1：D:\Stock\trading_analysis\data\ 目录下是否有分钟级数据？
  - 备选 2：使用 akshare / tushare pro（付费）下载
  - 备选 3：使用聚宽 / 米筐 / 天勤的分钟级数据

替代方案：
  - 若 5min 缺失，VP 分钟级可用日频 VA 突破替代（精度降低）
  - 若 60min 缺失，YTC 多周期可用日线+周线两周期替代（丢失 60min 信号）

降级路径：
  - 若所有分钟级缺失：YTC 降级为纯日线框架；VP 只用日频；TK 策略暂不纳入

审计人：[待填写]
审计日期：[待填写]
```

---

## 3. 选股层数据

### 3.1 Wind 资金流向数据（MFLOW 核心）

```text
数据项：Wind 资金流向因子（50 个因子中核心 2 个）
核心字段：
  - mfd_sellord：主力流出单数（大单+超大单卖出笔数）
  - mfd_buyord：主力流入单数
  - mfd_volinflowrate_open_m：开盘主力净流入率（集合竞价阶段）
  - mfd_netinflow：净流入金额
  - 时间范围：2018-01-01 至 2025-06-30
  - 频率：日频（T 日收盘后公布 T 日数据）

必需性：MUST（MFLOW 对象卡的核心输入）
当前状态：UNKNOWN（待确认）
获取路径：
  - 备选 1：Wind 终端（若已有账号）→ 导出每日资金流向数据
  - 备选 2：同花顺 iFinD（若已有账号）→ 资金流向模块
  - 备选 3：东方财富 Choice（免费版可能有基础资金流向）
  - 备选 4：akshare → stock_individual_fund_flow（免费，但字段可能不完整）

替代方案：
  - 若 Wind 50 因子缺失：
    → 用 akshare 的 stock_individual_fund_flow 提取：主力净流入、散户净流入、大单净流入
    → 效果降级：akshare 的字段定义与 Wind 不同，IC 可能降低，但方向性一致
  - 若所有资金流向数据缺失：
    → MFLOW 对象卡降级为 "依赖 PV Corr 成交量确认"，主力/散户概念不可用

降级路径：
  - 若完全缺失：MFLOW 从 proxy_quantizable_now 降级为 needs_extra_data，第一批回测跳过

审计人：[待填写]
审计日期：[待填写]
```

### 3.2 主动成交逐笔数据（ATRATIO，有条件激活）

```text
数据项：Level-2 逐笔委托/成交数据
核心字段：
  - 逐笔委托时间（精确到毫秒）
  - 逐笔委托方向（买/卖）
  - 逐笔成交量
  - 逐笔成交价格
  - 时间范围：2020-01-01 至 2025-06-30（Level-2 数据通常不会太早）
  - 频率：逐笔（实时）或 3s 切片（历史）

必需性：MUST（ATRATIO 核心输入）/ 但 ATRATIO 本身在 A 股纯多头下 LIMITED
当前状态：UNKNOWN（待确认）
获取路径：
  - 交易所 Level-2 数据（需授权，成本高）
  - 第三方数据商（如通联数据、聚源、天勤）

替代方案：
  - 无免费替代方案

降级路径：
  - ATRATIO 在 A 股纯多头下已知无效（SBKT_F002 结论）
  - 即使数据缺失，也不影响核心系统（ATRATIO 本就不在核心组合中）
  - 建议：永久放入 future_bucket，不投入回测资源

审计人：[待填写]
审计日期：[待填写]
```

### 3.3 季报机构持仓数据（INSTB 方法层）

```text
数据项：季报机构持仓数据
核心字段：
  - 机构总持仓占比（季度末）
  - 公募基金持仓占比
  - 社保基金持仓占比
  - QFII 持仓占比
  - 保险资金持仓占比
  - 股东户数（季度末）
  - 时间范围：2018Q1 至 2025Q1
  - 频率：季频

必需性：SHOULD（INSTB 方法层，不干预执行）
当前状态：UNKNOWN（待确认）
获取路径：
  - 备选 1：Wind 终端 → 机构持仓模块
  - 备选 2：同花顺 F10 → 机构持仓
  - 备选 3：akshare → stock_institute_hold（可能有）
  - 备选 4：手动从季报 PDF 中提取（ labor-intensive，不推荐）

替代方案：
  - 若缺失：INSTB 回测延期，但不影响核心系统（INSTB 是方法层，不是执行层）

降级路径：
  - 永久标记为 needs_extra_data，仅在方法层使用

审计人：[待填写]
审计日期：[待填写]
```

---

## 4. 结构层数据（缠论）

### 4.1 缠论笔/中枢历史序列

```text
数据项：缠论笔/中枢/分型历史序列
核心字段：
  - 分型：fx_date, fx_type（顶/底）, fx_price, fx_strength, fx_confirm
  - 笔：bi_start_date, bi_end_date, bi_direction（向上/向下）, bi_high, bi_low, bi_status（完成/延伸）
  - 中枢：zs_start_date, zs_end_date, zg（中枢高点）, zd（中枢低点）, zz（中枢中轴）, zs_state（形成/维持/破坏）
  - 时间范围：2018-01-01 至 2025-06-30

必需性：MUST（CHZL_BSD 核心输入，没有笔/中枢则无法判断买卖点）
当前状态：UNKNOWN（待确认）
获取路径：
  - 备选 1：D:\Stock\trading_analysis\ 下是否有现成缠论推导代码？
    → 检查文件：ashare_preprocess.py（37K）是否包含缠论逻辑？
    → 检查文件：backtest_p0.py（37K）是否包含笔/中枢计算？
  - 备选 2：从 OHLCV 实时推导（需编程实现）
    → 分型：顶分型 = 中间 K 线高点高于左右两根 K 线高点
    → 笔：旧笔规则 = 顶底之间至少 2 根独立 K 线
    → 中枢：三段重叠区间
  - 备选 3：使用第三方库（如 `chanlun` 等开源实现）

替代方案：
  - 若已有推导代码：直接复用，需验证输出字段与对象卡定义一致
  - 若需重新推导：预计需要 3-5 天编程实现

降级路径：
  - 若完全无法推导：CHZL_BSD 从执行层降级为 shell_only，系统暂用 BPB/YTC/TKR7 替代
  - 但缠论是系统的核心结构层，建议优先解决

审计人：[待填写]
审计日期：[待填写]
```

### 4.2 缠论背驰历史序列

```text
数据项：缠论背驰（MACD 面积对比）
核心字段：
  - 背驰段 a（进入段）和 c（离开段）的 MACD 面积
  - 背驰方向（顶背驰/底背驰）
  - 背驰 confidence（0-1）
  - 背驰确认价格

必需性：MUST（CHZL_BSD 的 1Buy/1Sell 核心判断依据）
当前状态：UNKNOWN（依赖笔/中枢的推导结果）
获取路径：
  - 从笔/中枢序列推导：
    → 进入段 a = 从分型到中枢的笔段
    → 离开段 c = 从中枢到下一分型的笔段
    → MACD 面积 = 该段内所有 K 线的 MACD 柱状图之和（取绝对值）

替代方案：
  - 无替代方案，背驰是缠论的核心逻辑

降级路径：
  - 若无法计算 MACD 面积：可用 RSI 背离或 AO 背离（TKR7）替代，但效果不同

审计人：[待填写]
审计日期：[待填写]
```

---

## 5. 风控层数据

### 5.1 交易日志（KELLY 核心输入）

```text
数据项：历史交易日志（盈亏记录）
核心字段：
  - trade_date（交易日期）
  - symbol（标的）
  - direction（LONG/SHORT）
  - entry_price（入场价）
  - exit_price（出场价）
  - profit_loss（盈亏金额）
  - r_multiple（R 倍数，盈亏 / 初始风险）
  - 时间范围：至少最近 30 笔交易（Kelly 最低要求）

必需性：MUST（KELLY 对象卡需要历史交易日志计算 f*）
当前状态：UNKNOWN（待确认）
获取路径：
  - 备选 1：backtest_p0.py 的历史回测结果中是否有交易日志？
  - 备选 2：从其他对象卡（VP/BPB/YTC）的单因子回测中导出交易日志
  - 备选 3：手动模拟交易日志（不推荐，数据质量差）

替代方案：
  - 若完全没有交易日志：
    → KELLY 对象卡降级为 "使用默认半凯利（f* = 0.25）"
    → 不回测 Kelly 的自适应逻辑，仅验证半凯利在组合中的效果

降级路径：
  - 若完全缺失：KELLY 从 proxy_quantizable_now 降级为 shell_only，仓位管理先用 Van Tharp 2%

审计人：[待填写]
审计日期：[待填写]
```

### 5.2 ATR14 历史序列

```text
数据项：ATR14（14 日平均真实波幅）
核心字段：
  - atr14（每日的 ATR14 值）
  - 时间范围：2018-01-01 至 2025-06-30

必需性：MUST（VOLTARGET、CHZL_BSD 止损、TK 策略均需要 ATR）
当前状态：UNKNOWN（可从 OHLCV 计算）
获取路径：
  - 从 OHLCV 计算：TR = max(high-low, |high-prev_close|, |low-prev_close|)，ATR14 = TR 的 14 日EMA
  - 检查 backtest_p0.py 中是否已有 ATR 计算逻辑

替代方案：
  - 无需替代，ATR14 是标准指标，任何 OHLCV 数据都能推导

降级路径：
  - 无降级路径（ATR14 是基础计算）

审计人：[待填写]
审计日期：[待填写]
```

---

## 6. 外汇数据（TK 策略验证）

### 6.1 外汇 OHLCV（EURUSD、GBPUSD、USDJPY）

```text
数据项：外汇主要货币对 OHLCV
时间范围：2018-01-01 至 2025-06-30
时间框架：1H（主要）+ 4H（上下文）+ 15min（精细执行）

必需性：SHOULD（TK 策略回测需要外汇数据，但 TK 是外汇体系，A 股核心系统不依赖）
当前状态：UNKNOWN（待确认）
获取路径：
  - 备选 1：Dukascopy 免费历史数据下载
  - 备选 2：OANDA 历史 API
  - 备选 3：MetaTrader 5 导出
  - 备选 4：FXCM 历史数据

替代方案：
  - 若外汇数据缺失：TK 策略（R6/R7/R8）回测延期，但不影响 A 股核心系统

降级路径：
  - TK 策略从 proxy_quantizable_now 降级为 needs_extra_data，等外汇数据就绪后再验证

审计人：[待填写]
审计日期：[待填写]
```

---

## 7. 数据质量检查清单

### 7.1 完整性检查

```text
检查项 1：日 OHLCV 缺失率
  - 方法：统计 2018-2024 每只股票的有效交易日数量 / 理论交易日数量
  - 标准：缺失率 < 5%（即每年缺失 < 12 个交易日）
  - 处理：缺失率 > 5% 的标的从股票池中剔除

检查项 2：前复权一致性
  - 方法：检查复权因子是否连续，是否存在复权跳跃
  - 标准：复权后价格序列无负值、无极端跳变（单日涨跌幅 < 44%，即科创板/创业板涨停限制）
  - 处理：异常复权的标的剔除或标记

检查项 3：成交量一致性
  - 方法：检查 volume 和 amount 是否匹配（amount / volume ≈ 均价，应在 low 和 high 之间）
  - 标准：不匹配率 < 1%
  - 处理：不匹配的数据行标记为可疑，不参与计算

检查项 4：分钟级数据对齐
  - 方法：检查分钟级 K 线是否与日线 K 线一致（分钟级 close 的 last 值 = 日线 close）
  - 标准：误差 < 0.1%
  - 处理：误差大的分钟级数据需重新下载或从日线合成
```

### 7.2 异常值检查

```text
检查项 5：涨跌停标记
  - 方法：识别 close = high = low（一字涨停/跌停）或 close = high（涨停）或 close = low（跌停）的日期
  - 标准：正常市场中涨停/跌停占比 < 10%（极端行情除外）
  - 处理：涨停/跌停日标记为 limit_up / limit_down，参与 ATR 修正

检查项 6：停牌识别
  - 方法：识别 volume = 0 或连续多日无数据的标的
  - 标准：停牌期间标记为 suspended，不参与计算
  - 处理：停牌超过 10 个交易日的标的从股票池中剔除

检查项 7：新股/次新股过滤
  - 方法：识别上市日期 < 1 年的标的
  - 标准：上市不足 252 个交易日（约 1 年）的标的标记为 new_stock
  - 处理：new_stock 不进入选股池（VOLFAC 历史分位不准，MFLOW 数据可能缺失）
```

---

## 8. 数据审计结论表（待填写）

| 数据项 | 当前状态 | 获取路径 | 替代方案 | 降级路径 | 审计人 | 审计日期 |
|--------|----------|----------|----------|----------|--------|----------|
| 日 OHLCV（前复权） | | | | | | |
| 周线 OHLCV | | | | | | |
| 分钟级 OHLCV | | | | | | |
| Wind 资金流向 | | | | | | |
| Level-2 逐笔数据 | | | | | | |
| 季报机构持仓 | | | | | | |
| 缠论笔/中枢序列 | | | | | | |
| 缠论背驰序列 | | | | | | |
| 交易日志（KELLY） | | | | | | |
| ATR14 序列 | | | | | | |
| 外汇 OHLCV | | | | | | |

---

## 9. 对编程 AI 的数据边界说明

### 9.1 必须假设的数据

以下数据是编程 AI 在实现回测框架时必须假设**已存在**的。如果实际缺失，回测框架无法运行：

```text
MUST_HAVE_DATA = [
    "日 OHLCV（前复权，至少 2019-2024，全 A 股）",
    "周线 OHLCV（从日线合成）",
    "ATR14（从 OHLCV 计算）",
]
```

### 9.2 条件激活的数据

以下数据是编程 AI 在实现时需要设计**条件分支**的：如果数据存在则激活该对象卡，如果不存在则跳过：

```text
CONDITIONAL_DATA = {
    "Wind 资金流向": "若存在 → 激活 MFLOW_P0_A；若不存在 → MFLOW 跳过，系统继续运行",
    "分钟级 OHLCV": "若存在 → 激活 VP 分钟级 + YTC 60min；若不存在 → VP 只用日频，YTC 只用日线+周线",
    "缠论笔/中枢": "若存在 → 激活 CHZL_BSD；若不存在 → CHZL_BSD 跳过，用 BPB/YTC 替代",
    "交易日志": "若存在 → 激活 KELLY 自适应；若不存在 → KELLY 用默认半凯利（f*=0.25）",
    "外汇 OHLCV": "若存在 → 激活 TK-R6/R7/R8；若不存在 → TK 策略跳过，不影响 A 股系统",
}
```

### 9.3 可忽略的数据

以下数据编程 AI 不需要考虑，因为它们不影响核心系统运行：

```text
OPTIONAL_DATA = [
    "Level-2 逐笔数据（ATRATIO 纯多头无效，已放入 future_bucket）",
    "季报机构持仓（INSTB 方法层，不干预执行）",
    "另类数据（NLP、舆情、卫星数据等，未纳入当前系统）",
]
```

---

## 10. 编程 AI 的数据接口规范

### 10.1 数据加载器的统一接口

编程 AI 在实现回测框架时，应设计一个统一的数据加载器，屏蔽底层数据源的差异：

```python
# 伪代码：数据加载器统一接口（供编程 AI 参考）

class DataLoader:
    """
    统一数据加载器，屏蔽底层数据源差异
    所有对象卡通过 DataLoader 获取数据，不直接访问文件或 API
    """
    
    def __init__(self, config):
        self.config = config
        self.available_data = self._scan_data_availability()
    
    def _scan_data_availability(self):
        """扫描数据可用性，返回数据状态字典"""
        # 实现：检查各数据文件是否存在、时间范围是否完整
        pass
    
    def get_daily_ohlcv(self, symbol, start_date, end_date, adjusted=True):
        """获取日 OHLCV"""
        # 必须实现
        pass
    
    def get_weekly_ohlcv(self, symbol, start_date, end_date, adjusted=True):
        """获取周线 OHLCV（可合成或独立）"""
        # 默认从日线合成，但支持独立加载
        pass
    
    def get_minute_ohlcv(self, symbol, timeframe, start_date, end_date):
        """获取分钟级 OHLCV（条件激活）"""
        # timeframe ∈ ['60min', '15min', '5min']
        # 如果数据缺失，返回 None，调用方需处理
        pass
    
    def get_money_flow(self, symbol, start_date, end_date):
        """获取资金流向数据（条件激活）"""
        # 如果 Wind 数据缺失，返回 None
        # 如果 akshare 替代数据可用，返回替代数据并标记 source='akshare'
        pass
    
    def get_chanlun_data(self, symbol, start_date, end_date):
        """获取缠论笔/中枢/背驰数据（条件激活）"""
        # 如果已有预计算文件，加载
        # 如果没有，实时推导（计算量大，需缓存）
        pass
    
    def get_trade_log(self, strategy_name, start_date, end_date):
        """获取交易日志（条件激活）"""
        # 用于 KELLY 计算
        pass
    
    def get_atr14(self, symbol, start_date, end_date, n=14):
        """获取 ATR14（可从 OHLCV 计算，但支持预计算）"""
        # 默认从 OHLCV 实时计算，但支持加载预计算文件加速
        pass
    
    def check_data_availability(self, data_name):
        """检查某类数据是否可用"""
        return self.available_data.get(data_name, False)
    
    def get_data_report(self):
        """生成数据可用性报告（用于审计）"""
        # 返回所有数据项的状态、路径、缺失率、时间范围
        pass
```

### 10.2 数据缺失时的降级策略

```python
# 伪代码：数据缺失时的降级策略（供编程 AI 参考）

class DataFallback:
    """
    数据降级策略：当某类数据缺失时，如何降级对象卡或系统
    """
    
    FALLBACK_RULES = {
        "money_flow": {
            "missing_action": "SKIP_OBJECT_CARD",
            "target": "MFLOW_P0_A",
            "fallback": None,  # 无替代，直接跳过
            "system_impact": "选股层少一个过滤器，系统可继续运行"
        },
        "minute_ohlcv": {
            "missing_action": "DEGRADE_TIMEFRAME",
            "target": ["VP_P0_E", "YTC_P0_E"],
            "fallback": "使用日频替代分钟级",
            "system_impact": "精度降低，但核心信号保留"
        },
        "chanlun_data": {
            "missing_action": "SKIP_OBJECT_CARD",
            "target": "CHZL_BSD_P0_E",
            "fallback": "用 BPB_P0_E 和 YTC_P0_E 替代",
            "system_impact": "执行层少一个信号源，需其他对象卡补足投票"
        },
        "trade_log": {
            "missing_action": "USE_DEFAULT",
            "target": "KELLY_P0_R",
            "fallback": "f_star=0.25（半凯利）",
            "system_impact": "Kelly 不自适应，但 Van Tharp 2% 仍有效"
        },
        "forex_ohlcv": {
            "missing_action": "SKIP_MODULE",
            "target": ["TK_R6_P0_E", "TK_R7_P0_E", "TK_R8_P0_E"],
            "fallback": None,
            "system_impact": "TK 外汇模块不激活，不影响 A 股系统"
        }
    }
```

---

> 文件：DATA_AVAILABILITY_AUDIT_v1.0.md  
> 生产者：Kimi  
> 状态：待逐项人工确认，确认后作为编程 AI 的数据边界条件文档  
> 建议：用户在 [审计人] 和 [审计日期] 处逐项填写后，与编程 AI 共享此文档
