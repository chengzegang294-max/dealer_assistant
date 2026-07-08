# 单元测试规范 v1.0

> **本文档全部内容源于用户（仓库所有者）的想法，由 Kimi 整理为结构化文档供编程 AI 参考。**
> 版本：v1.0 | 状态：设计阶段 | 核心目标：定义所有模块的测试标准，确保系统可验证、可复现、可维护

---

## 一、测试总体要求

```text
覆盖率目标：
  - 核心逻辑（Pipeline/Vote/Risk）→ 覆盖率 ≥ 90%
  - 对象卡 → 覆盖率 ≥ 80%
  - 工具函数 → 覆盖率 ≥ 70%
  - 治理架构 → 覆盖率 ≥ 75%
  - 数据管道 → 覆盖率 ≥ 80%

测试原则：
  1. 测试即文档：每个测试用例说明一个使用场景
  2. 快速反馈：单个测试 < 1 秒，全量测试 < 5 分钟
  3. 隔离性：测试之间不共享状态
  4. 可复现：固定随机种子，消除不确定性
  5. 自动化：CI/CD 自动运行，失败即阻断合并
```

---

## 二、测试目录结构

```
src/tests/
├── conftest.py                    # pytest 全局配置和 fixtures
├── fixtures/                      # 测试数据（合成数据，非生产数据）
│   ├── sample_ohlcv.csv          # 示例 OHLCV 数据
│   ├── sample_fundamental.json   # 示例财报数据
│   ├── sample_macro.json         # 示例宏观数据
│   └── synthetic_generator.py   # 合成数据生成器
│
├── unit/                          # 单元测试
│   ├── test_objects/             # 对象卡测试
│   │   ├── test_chzl_bsd.py     # 缠论买卖点测试
│   │   ├── test_bpb.py          # 突破回调测试
│   │   ├── test_mflow.py        # 资金流向测试
│   │   ├── test_kelly.py        # Kelly 测试
│   │   └── test_period_queen.py # 周期女王测试
│   │
│   ├── test_vote_engine.py       # 投票引擎测试
│   ├── test_risk_engine.py       # 风控引擎测试
│   ├── test_data_pipeline.py     # 数据管道测试
│   ├── test_governance.py        # 治理架构测试
│   └── test_utils.py             # 工具函数测试
│
├── integration/                   # 集成测试
│   ├── test_pipeline_end_to_end.py     # 端到端 Pipeline 测试
│   ├── test_governance_with_engine.py # 治理架构与回测引擎集成测试
│   ├── test_data_to_feature.py       # 数据到特征流水线测试
│   └── test_regime_switching.py      # 制度模式切换测试
│
├── regression/                    # 回归测试
│   ├── test_backtest_regression.py   # 回测结果回归测试
│   └── test_object_card_regression.py # 对象卡输出回归测试
│
└── performance/                   # 性能测试
    ├── test_data_loading_speed.py    # 数据加载速度测试
    ├── test_feature_calc_speed.py   # 特征计算速度测试
    └── test_backtest_speed.py       # 回测速度测试
```

---

## 三、测试数据规范

### 3.1 合成数据生成器

```python
# tests/fixtures/synthetic_generator.py
import numpy as np
import pandas as pd
import polars as pl
from datetime import datetime, timedelta

class SyntheticDataGenerator:
    """合成数据生成器：生成不依赖生产数据的测试数据"""
    
    def __init__(self, seed: int = 42):
        self.rng = np.random.RandomState(seed)
    
    def generate_ohlcv(self, symbol: str = "000001.SZ",
                       start: str = "2024-01-01",
                       days: int = 100,
                       trend: str = "up") -> pl.DataFrame:
        """
        生成合成 OHLCV 数据
        
        Args:
            symbol: 股票代码
            start: 开始日期
            days: 交易日数量
            trend: 趋势类型（up/down/sideways/volatile）
        
        Returns:
            polars DataFrame with columns: [date, open, high, low, close, volume, amount]
        """
        dates = pd.date_range(start=start, periods=days, freq='B')  # 工作日
        
        base_price = 10.0
        if trend == "up":
            returns = self.rng.normal(0.001, 0.02, days)
        elif trend == "down":
            returns = self.rng.normal(-0.001, 0.02, days)
        elif trend == "sideways":
            returns = self.rng.normal(0, 0.01, days)
        else:  # volatile
            returns = self.rng.normal(0, 0.05, days)
        
        prices = base_price * np.exp(np.cumsum(returns))
        
        # 生成 OHLC
        opens = prices * (1 + self.rng.normal(0, 0.005, days))
        closes = prices * (1 + self.rng.normal(0, 0.005, days))
        highs = np.maximum(opens, closes) * (1 + self.rng.uniform(0, 0.02, days))
        lows = np.minimum(opens, closes) * (1 - self.rng.uniform(0, 0.02, days))
        
        # 生成成交量
        volumes = self.rng.lognormal(15, 1, days).astype(int)
        amounts = closes * volumes * (1 + self.rng.normal(0, 0.1, days))
        
        df = pl.DataFrame({
            "date": dates.strftime("%Y-%m-%d").tolist(),
            "open": np.round(opens, 2),
            "high": np.round(highs, 2),
            "low": np.round(lows, 2),
            "close": np.round(closes, 2),
            "volume": volumes,
            "amount": np.round(amounts, 2),
        })
        
        return df
    
    def generate_fundamental(self, symbol: str = "000001.SZ") -> dict:
        """生成合成财报数据"""
        return {
            "symbol": symbol,
            "report_date": "2024-03-31",
            "roe": 0.18,
            "revenue_growth": 0.25,
            "net_profit": 1_000_000_000,
            "operating_cash_flow": 900_000_000,
            "total_assets": 10_000_000_000,
            "total_liabilities": 5_000_000_000,
            "goodwill": 500_000_000,
            "pledge_ratio": 0.15,
        }
    
    def generate_macro(self, date: str = "2024-06-24") -> dict:
        """生成合成宏观数据"""
        return {
            "date": date,
            "cgb10y": 2.35,
            "usdcny": 7.245,
            "m2_yoy": 10.5,
            "shibor_overnight": 1.85,
            "hv20_csi300": 0.185,
            "vix": 16.2,
            "policy_events": [],
        }
```

### 3.2 Fixtures 配置

```python
# tests/conftest.py
import pytest
from tests.fixtures.synthetic_generator import SyntheticDataGenerator

@pytest.fixture(scope="session")
def data_generator():
    """全局合成数据生成器"""
    return SyntheticDataGenerator(seed=42)

@pytest.fixture
def sample_ohlcv_up(data_generator):
    """上涨趋势合成数据"""
    return data_generator.generate_ohlcv(trend="up")

@pytest.fixture
def sample_ohlcv_down(data_generator):
    """下跌趋势合成数据"""
    return data_generator.generate_ohlcv(trend="down")

@pytest.fixture
def sample_ohlcv_sideways(data_generator):
    """震荡趋势合成数据"""
    return data_generator.generate_ohlcv(trend="sideways")

@pytest.fixture
def sample_fundamental():
    """合成财报数据"""
    return SyntheticDataGenerator().generate_fundamental()

@pytest.fixture
def sample_macro():
    """合成宏观数据"""
    return SyntheticDataGenerator().generate_macro()
```

---

## 四、对象卡测试规范

### 4.1 测试模板

```python
# tests/unit/test_objects/test_chzl_bsd.py
import pytest
import numpy as np
from src.backtest_engine.objects.chzl_bsd import CHZLBSD

class TestCHZLBSD:
    """
    CHZL_BSD 对象卡测试
    
    测试原则：
    1. 每个方法至少 1 个正常用例 + 2 个边界用例
    2. 测试命名：test_{方法}_{场景}_{预期结果}
    3. 断言必须包含具体数值，不能用 assert True
    """
    
    @pytest.fixture
    def chzl_bsd(self):
        """初始化对象卡"""
        return CHZLBSD()
    
    # ========== 正常用例 ==========
    
    def test_calculate_up_trend_generates_3buy(self, chzl_bsd, sample_ohlcv_up):
        """
        上涨趋势中应生成 3Buy 信号
        
        Given: 上涨趋势合成数据
        When: 运行 CHZL_BSD 计算
        Then: 应检测到至少 1 个 3Buy 信号
        """
        result = chzl_bsd.calculate(sample_ohlcv_up)
        
        buy_signals = [r for r in result if r["signal_type"] == "3Buy"]
        assert len(buy_signals) > 0, "上涨趋势中应至少检测到 1 个 3Buy"
        
        # 验证 3Buy 信号结构
        first_buy = buy_signals[0]
        assert first_buy["signal_strength"] >= 5
        assert first_buy["signal_strength"] <= 10
        assert "entry_price" in first_buy
        assert "stop_loss" in first_buy
    
    def test_calculate_down_trend_generates_1sell(self, chzl_bsd, sample_ohlcv_down):
        """
        下跌趋势中应生成 1Sell 信号
        """
        result = chzl_bsd.calculate(sample_ohlcv_down)
        
        sell_signals = [r for r in result if r["signal_type"] == "1Sell"]
        assert len(sell_signals) > 0, "下跌趋势中应至少检测到 1 个 1Sell"
    
    # ========== 边界用例 ==========
    
    def test_calculate_empty_dataframe_returns_none(self, chzl_bsd):
        """
        空数据应返回 NONE 信号
        """
        import polars as pl
        empty_df = pl.DataFrame()
        
        result = chzl_bsd.calculate(empty_df)
        
        assert result["signal_type"] == "NONE"
        assert result["maturity_status"] == "degraded"
        assert "degraded_reason" in result
    
    def test_calculate_single_row_returns_none(self, chzl_bsd):
        """
        单条数据不足以计算缠论结构
        """
        import polars as pl
        single_row = pl.DataFrame({
            "date": ["2024-01-01"],
            "open": [10.0],
            "high": [10.5],
            "low": [9.5],
            "close": [10.2],
            "volume": [1000000],
            "amount": [10000000],
        })
        
        result = chzl_bsd.calculate(single_row)
        
        assert result["signal_type"] == "NONE"
        assert result["degraded_reason"] == "insufficient_data: need at least 20 bars"
    
    def test_calculate_with_nan_returns_none(self, chzl_bsd, sample_ohlcv_up):
        """
        数据包含 NaN 应降级处理
        """
        import polars as pl
        import numpy as np
        
        # 注入 NaN
        df_with_nan = sample_ohlcv_up.with_columns(
            pl.when(pl.col("date") == "2024-01-15")
            .then(None)
            .otherwise(pl.col("close"))
            .alias("close")
        )
        
        result = chzl_bsd.calculate(df_with_nan)
        
        assert result["signal_type"] == "NONE"
        assert "nan_detected" in result.get("degraded_reason", "")
    
    def test_calculate_limit_up_price(self, chzl_bsd, sample_ohlcv_up):
        """
        涨停价格应正确处理（A股特殊规则）
        """
        import polars as pl
        
        # 模拟涨停（high = low = close = 涨停价）
        limit_up_df = sample_ohlcv_up.with_columns(
            pl.when(pl.col("date") == "2024-01-20")
            .then(pl.col("close") * 1.1)
            .otherwise(pl.col("high"))
            .alias("high"),
            pl.when(pl.col("date") == "2024-01-20")
            .then(pl.col("close") * 1.1)
            .otherwise(pl.col("low"))
            .alias("low"),
            pl.when(pl.col("date") == "2024-01-20")
            .then(pl.col("close") * 1.1)
            .otherwise(pl.col("close"))
            .alias("close"),
        )
        
        result = chzl_bsd.calculate(limit_up_df)
        
        # 不应因涨停而崩溃
        assert result is not None
        assert "signal_type" in result
    
    # ========== 标准输出接口测试 ==========
    
    def test_output_has_all_standard_fields(self, chzl_bsd, sample_ohlcv_up):
        """
        输出必须包含所有标准字段
        """
        result = chzl_bsd.calculate(sample_ohlcv_up)
        
        required_fields = [
            "object_id", "object_name", "function_bucket", "process_layer",
            "timestamp", "symbol", "timeframe",
            "signal_type", "signal_strength", "signal_confidence",
            "maturity_status", "data_requirement",
        ]
        
        for field in required_fields:
            assert field in result, f"缺少标准字段: {field}"
    
    def test_signal_strength_in_valid_range(self, chzl_bsd, sample_ohlcv_up):
        """
        signal_strength 必须在 0-10 范围内
        """
        result = chzl_bsd.calculate(sample_ohlcv_up)
        
        strength = result.get("signal_strength", 0)
        assert 0 <= strength <= 10, f"signal_strength={strength} 超出范围"
```

### 4.2 测试用例设计原则

```text
每个对象卡必须测试的边界场景：

1. 数据缺失：
   - 空 DataFrame
   - 单条数据
   - 数据量不足（低于对象卡最小要求）
   - 包含 NaN
   - 包含重复时间戳

2. 极端行情：
   - 涨停（high=low=close）
   - 跌停
   - 连续涨停/跌停
   - 巨幅跳空（>10%）
   - 成交量为0（停牌）

3. 数据异常：
   - high < low（价格倒挂）
   - close > high（价格越界）
   - volume < 0（成交量为负）
   - amount < 0（成交额为负）

4. 时间异常：
   - 时间戳不连续（节假日/停牌）
   - 时间戳重复
   - 时间戳乱序

5. 复权异常：
   - 除权除息日价格跳变
   - 复权因子不一致
```

---

## 五、核心引擎测试规范

### 5.1 投票引擎测试

```python
# tests/unit/test_vote_engine.py
class TestVoteDecisionEngine:
    """投票引擎测试"""
    
    def test_node_001_data_validation_pass(self):
        """数据验证通过"""
        engine = VoteDecisionEngine()
        objects = {
            "CHZL_BSD": {"signal_type": "LONG", "signal_strength": 8},
            "BPB": {"signal_type": "LONG", "signal_strength": 7},
        }
        
        result, data = engine.node_001_data_validation(objects)
        assert result == "PASS"
    
    def test_node_001_data_validation_missing_object(self):
        """数据缺失时 ABORT"""
        engine = VoteDecisionEngine()
        objects = {}  # 空对象
        
        result, data = engine.node_001_data_validation(objects)
        assert result == "ABORT"
        assert data["abort_reason"] == "data_insufficient"
    
    def test_node_002_period_queen_halt(self):
        """PeriodQueen 禁止时 ABORT"""
        engine = VoteDecisionEngine()
        pq_output = {"current_state": "HALT", "allow_trading": False}
        
        result, data = engine.node_002_period_queen_check(pq_output)
        assert result == "ABORT"
        assert data["abort_reason"] == "period_queen_halt"
    
    def test_voting_insufficient_votes(self):
        """票数不足时 ABORT"""
        engine = VoteDecisionEngine()
        objects = {
            "CHZL_BSD": {"signal_type": "LONG", "signal_strength": 8},
            # 只有 1 个对象卡，entry_min_votes=3
        }
        pq_output = {"current_state": "ATTACK_SUSTAINED", "entry_min_votes": 3}
        
        result, data = engine.execute(objects, pq_output, {}, {}, {})
        assert result == "ABORT"
        assert data["abort_reason"] == "votes_insufficient"
    
    def test_voting_same_bucket_exceeds_limit(self):
        """同一 function_bucket 票数超限"""
        engine = VoteDecisionEngine()
        objects = {
            "CHZL_BSD": {"signal_type": "LONG", "signal_strength": 8, "function_bucket": "EXECUTION"},
            "CHZL_BI": {"signal_type": "LONG", "signal_strength": 7, "function_bucket": "EXECUTION"},
            "CHZL_ZS": {"signal_type": "LONG", "signal_strength": 6, "function_bucket": "EXECUTION"},
            # 3 个都来自 EXECUTION，超过 max_same_bucket_votes=2
        }
        pq_output = {"current_state": "ATTACK_SUSTAINED", "max_same_bucket_votes": 2}
        
        result, data = engine.execute(objects, pq_output, {}, {}, {})
        # 应该只取 EXECUTION 中 strength 最高的 2 个
        assert data["votes_from_execution"] <= 2
```

### 5.2 风控引擎测试

```python
# tests/unit/test_risk_engine.py
class TestRiskArchitectureEngine:
    """风控引擎测试"""
    
    def test_van_tharp_limit_enforced(self):
        """Van Tharp 硬性上限必须执行"""
        engine = RiskArchitectureEngine()
        
        entry_price = 100.0
        stop_loss = 90.0  # 10% 止损
        total_capital = 1_000_000
        planned_size = 0.05  # 计划 5% 仓位
        
        # 单票风险 = |100-90| * 5% / 1M = 0.5%，低于 2% 上限 → 通过
        result = engine.van_tharp_check(entry_price, stop_loss, total_capital, planned_size)
        assert result["passed"] is True
        
        # 单票风险 = |100-90| * 30% / 1M = 3%，超过 2% 上限 → 否决
        planned_size = 0.30
        result = engine.van_tharp_check(entry_price, stop_loss, total_capital, planned_size)
        assert result["passed"] is False
        assert result["max_allowed_size"] < 0.30
    
    def test_kelly_calculation(self):
        """Kelly 公式计算正确"""
        engine = RiskArchitectureEngine()
        
        trade_log = [
            {"pnl": 0.05}, {"pnl": -0.03}, {"pnl": 0.08}, {"pnl": 0.02}, {"pnl": -0.01},
        ]
        
        kelly = engine.kelly_calculate(trade_log)
        
        # 胜率 = 3/5 = 0.6
        # 平均盈利 = (0.05+0.08+0.02)/3 = 0.05
        # 平均亏损 = (0.03+0.01)/2 = 0.02
        # b = 0.05/0.02 = 2.5
        # f* = 0.6 - 0.4/2.5 = 0.44
        # half_kelly = 0.22
        assert 0.15 < kelly["kelly_f"] < 0.30
        assert 0.07 < kelly["half_kelly"] < 0.15
    
    def test_voltarget_reduces_size_in_high_vol(self):
        """高波动率时 VolTarget 应降低仓位"""
        engine = RiskArchitectureEngine()
        
        volfac_data = {"vol_20d": 0.30}  # 30% 年化波动率
        target_vol = 0.15
        
        vt = engine.voltarget_calculate(volfac_data, target_vol)
        
        # 波动率 30% > 目标 15% → 仓位应降低
        assert vt["vt_size_scalar"] < 1.0
        assert vt["vt_size_scalar"] < 0.6  # 至少降到 60% 以下
```

---

## 六、集成测试规范

### 6.1 端到端 Pipeline 测试

```python
# tests/integration/test_pipeline_end_to_end.py
class TestEndToEndPipeline:
    """端到端 Pipeline 测试"""
    
    def test_full_pipeline_single_trade(self, sample_ohlcv_up, sample_fundamental, sample_macro):
        """
        完整 Pipeline：从数据到交易执行
        
        验证：
        1. DataLoader 正确加载数据
        2. 对象卡正确计算信号
        3. PeriodQueen 正确判断状态
        4. VoteDecisionEngine 正确投票
        5. RiskArchitectureEngine 正确风控
        6. ExecutionEngine 正确执行
        7. 交易记录正确生成
        """
        # 1. 初始化引擎
        data_loader = DataLoader()
        backtest_engine = BacktestEngine()
        
        # 2. 加载数据
        data_loader.load_ohlcv(sample_ohlcv_up)
        data_loader.load_fundamental(sample_fundamental)
        data_loader.load_macro(sample_macro)
        
        # 3. 运行回测
        result = backtest_engine.run_single_day(
            date="2024-01-15",
            symbol="000001.SZ",
        )
        
        # 4. 验证结果结构
        assert "trade_decision" in result
        assert "objects_output" in result
        assert "risk_assessment" in result
        assert "audit_log" in result
        
        # 5. 验证交易决策
        if result["trade_decision"]["action"] == "BUY":
            assert "entry_price" in result["trade_decision"]
            assert "stop_loss" in result["trade_decision"]
            assert "size_pct" in result["trade_decision"]
            
            # 验证 Van Tharp 合规
            risk = result["risk_assessment"]
            assert risk["van_tharp_passed"] is True
            assert risk["portfolio_risk"] < 0.06  # 6% 上限
    
    def test_full_pipeline_with_regime_switch(self):
        """
        制度模式切换场景测试
        
        验证：
        1. 牛市模式自动切换
        2. 对象卡参数自动调整
        3. 六科审查规则变化
        4. 交易执行正常
        """
        engine = GovernanceEngine()
        
        # 模拟 PeriodQueen 切换到 ATTACK_SUSTAINED
        engine.controller.switch_mode(
            RegimeMode.BULL,
            trigger="PeriodQueen=ATTACK_SUSTAINED"
        )
        
        # 验证模式已切换
        assert engine.controller.current_mode == RegimeMode.BULL
        
        # 验证六科规则已放宽
        strategy = engine.controller.get_strategy()
        assert strategy.van_tharp_limit() == 0.03  # 牛市放宽到 3%
        assert strategy.min_objects_for_entry() == 2  # 牛市降为 2 个
```

---

## 七、回归测试规范

### 7.1 回测结果回归

```python
# tests/regression/test_backtest_regression.py
class TestBacktestRegression:
    """
    回测结果回归测试
    
    目的：确保代码变更不导致回测结果意外变化
    """
    
    REGRESSION_BASELINE = {
        "chzl_bsd_2020_2024": {
            "total_return": 0.523,
            "sharpe_ratio": 1.12,
            "max_drawdown": -0.18,
            "win_rate": 0.58,
        },
        "bpb_2020_2024": {
            "total_return": 0.456,
            "sharpe_ratio": 0.98,
            "max_drawdown": -0.22,
            "win_rate": 0.52,
        },
    }
    
    TOLERANCE = 0.05  # 允许 5% 的偏差
    
    def test_chzl_bsd_regression(self):
        """CHZL_BSD 回测结果不应与基线偏差过大"""
        baseline = self.REGRESSION_BASELINE["chzl_bsd_2020_2024"]
        
        # 运行当前版本的回测
        result = run_backtest("CHZL_BSD", "2020-01-01", "2024-12-31")
        
        # 验证关键指标
        assert abs(result["total_return"] - baseline["total_return"]) < self.TOLERANCE
        assert abs(result["sharpe_ratio"] - baseline["sharpe_ratio"]) < self.TOLERANCE
        assert abs(result["max_drawdown"] - baseline["max_drawdown"]) < self.TOLERANCE
```

---

## 八、性能测试规范

```python
# tests/performance/test_data_loading_speed.py
class TestDataLoadingPerformance:
    """数据加载性能测试"""
    
    def test_load_5000_stocks_daily_under_5_seconds(self):
        """加载 5000 只股票的日 OHLCV 数据应在 5 秒内完成"""
        import time
        
        data_loader = DataLoader()
        
        start = time.time()
        data = data_loader.load_daily_ohlcv(symbols=get_all_stocks(), date="2024-06-24")
        elapsed = time.time() - start
        
        assert elapsed < 5.0, f"加载耗时 {elapsed:.2f} 秒，超过 5 秒阈值"
    
    def test_feature_calculation_under_1_second_per_symbol(self):
        """单只标的的特征计算应在 1 秒内完成"""
        import time
        
        feature_engineer = FeatureEngineer()
        
        start = time.time()
        features = feature_engineer.calculate_all("000001.SZ", "2024-06-24")
        elapsed = time.time() - start
        
        assert elapsed < 1.0, f"特征计算耗时 {elapsed:.2f} 秒，超过 1 秒阈值"
```

---

## 九、测试运行命令

```bash
# 运行全部测试
pytest src/tests/ -v --tb=short

# 运行单元测试
pytest src/tests/unit/ -v

# 运行集成测试
pytest src/tests/integration/ -v

# 运行回归测试
pytest src/tests/regression/ -v

# 运行性能测试（标记为 slow）
pytest src/tests/performance/ -v -m slow

# 生成覆盖率报告
pytest src/tests/ --cov=src --cov-report=html --cov-report=term

# 只运行失败的测试
pytest src/tests/ --lf

# 并行运行（使用 pytest-xdist）
pytest src/tests/ -n auto
```

---

## 十、对编程 AI 的指令

```text
1. 每个模块必须有对应的测试文件
2. 测试数据必须使用 fixtures/synthetic_generator.py 生成，禁止用生产数据
3. 测试命名必须清晰：test_{被测函数}_{场景}_{预期结果}
4. 断言必须包含具体数值，不能用 assert True
5. 边界测试必须覆盖：空数据、单条数据、NaN、涨停、停牌、价格倒挂
6. 集成测试必须验证模块间的数据传递格式正确
7. 性能测试必须有明确的阈值，超过阈值即失败
8. 回归测试的基线数据必须版本化（存放到 tests/fixtures/baselines/）
```

---

> 文件：TESTING_SPECIFICATION_v1.0.md
> 生产者：Kimi（测试规范设计）
> 核心设计：三级测试（单元/集成/回归）+ 合成数据生成器 + 性能阈值
> 覆盖率目标：核心 90% / 对象卡 80% / 工具 70%
