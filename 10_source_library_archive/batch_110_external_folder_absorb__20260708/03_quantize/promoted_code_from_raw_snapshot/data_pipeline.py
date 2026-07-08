# data_pipeline.py — A股量化数据管道原型
# 状态: ✅ 可编码（Phase 1: 框架 + 模拟数据验证）
# 数据源: Tushare Pro / AkShare（需安装） / 模拟数据（内置）
# 输出: 标准化数据对象，直接供对象卡消费

"""
数据管道原型 — 为对象卡层提供标准化数据输入

架构设计:
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │  DataSource │────→│  Normalizer │────→│  CacheLayer │
    │ (Tushare/   │     │ (标准化输出) │     │ (Parquet/   │
    │  AkShare/   │     │             │     │  Memory)    │
    │  Simulated) │     │             │     │             │
    └─────────────┘     └─────────────┘     └─────────────┘
                                                    │
                                                    ▼
                                            ┌─────────────┐
                                            │ ObjectCard  │
                                            │ (VOLFAC/    │
                                            │  ATRATIO/   │
                                            │  etc.)      │
                                            └─────────────┘

设计原则:
    1. 数据源可插拔: Tushare / AkShare / 模拟数据 / 本地 CSV 统一接口
    2. 输出标准化: 所有对象卡消费统一的数据结构
    3. 本地缓存: Parquet 格式，按日更新，避免重复拉取
    4. 最小依赖: Phase 1 用内置模拟数据，Phase 2 接入真实数据源
"""

from __future__ import annotations

import os
import json
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable
from enum import Enum


# ---------------------------------------------------------------------------
# 标准化数据结构（所有对象卡消费的数据格式）
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class OHLCVBar:
    """单根K线标准化数据"""
    ts_code: str          # 股票代码，如 '000001.SZ'
    trade_date: str       # 交易日期，如 '20250701'
    open: float
    high: float
    low: float
    close: float
    vol: float            # 成交量（手）
    amount: float         # 成交额（千元）


@dataclass(frozen=True)
class StockPriceSeries:
    """单只股票时间序列（对象卡直接消费的数据结构）"""
    ts_code: str
    freq: str             # 'daily' | '5min' | '1min'
    bars: List[OHLCVBar]
    
    # 便捷属性
    @property
    def close_list(self) -> List[float]:
        return [b.close for b in self.bars]
    
    @property
    def high_list(self) -> List[float]:
        return [b.high for b in self.bars]
    
    @property
    def low_list(self) -> List[float]:
        return [b.low for b in self.bars]
    
    @property
    def vol_list(self) -> List[float]:
        return [b.vol for b in self.bars]
    
    @property
    def date_list(self) -> List[str]:
        return [b.trade_date for b in self.bars]
    
    def to_volfac_raw(self, lookback_days: int = 60) -> Dict[str, Any]:
        """
        转换为 VOLFAC 对象卡输入格式
        
        Returns:
            dict 可直接传给 VolFacRawInput(**dict)
        """
        from object_card_volfac import VolFacRawInput
        
        closes = self.close_list[-lookback_days:]
        return {
            'close_60d': closes,
            'close_5m': None,  # 日频数据无5分钟
            'high_5m': None,
            'low_5m': None,
            'historical_vol_1y': None,  # 需要额外历史数据
        }


@dataclass
class DataPipeState:
    """数据管道运行状态"""
    last_update: Optional[str] = None
    cached_count: int = 0
    source: str = "simulated"
    error_log: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# 数据源抽象层
# ---------------------------------------------------------------------------

class DataSourceType(Enum):
    SIMULATED = "simulated"       # 内置模拟数据（无需外部依赖）
    TUSHARE = "tushare"           # Tushare Pro（需 token）
    AKSHARE = "akshare"           # AkShare（免 token，需安装）
    LOCAL_CSV = "local_csv"       # 本地 CSV/Parquet 文件


class BaseDataSource:
    """数据源抽象基类"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
    
    def fetch_daily(self, ts_code: str, start_date: str, end_date: str) -> StockPriceSeries:
        """获取日频数据"""
        raise NotImplementedError
    
    def fetch_intraday(self, ts_code: str, freq: str, 
                        start_date: str, end_date: str) -> StockPriceSeries:
        """获取日内数据（需 Level-2 或分钟线）"""
        raise NotImplementedError


class SimulatedDataSource(BaseDataSource):
    """
    模拟数据源 — 无需外部依赖，用随机游走生成真实价格序列
    
    参数:
        annual_return: 年化收益率（默认 8%）
        annual_vol: 年化波动率（默认 30%）
        initial_price: 初始价格（默认 10.0）
        seed: 随机种子（可复现）
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.annual_return = self.config.get('annual_return', 0.08)
        self.annual_vol = self.config.get('annual_vol', 0.30)
        self.initial_price = self.config.get('initial_price', 10.0)
        self.seed = self.config.get('seed', 42)
    
    def _generate_bars(self, ts_code: str, n_days: int) -> List[OHLCVBar]:
        """生成 n 日模拟K线"""
        np.random.seed(self.seed)
        
        daily_return = self.annual_return / 252
        daily_vol = self.annual_vol / np.sqrt(252)
        
        returns = np.random.normal(daily_return, daily_vol, n_days)
        prices = [self.initial_price]
        for r in returns:
            prices.append(prices[-1] * (1 + r))
        prices = np.array(prices[1:])
        
        # 模拟 OHLC（基于收盘价 ± 日内波动）
        intraday_vol = daily_vol * 0.6  # 日内波动约60%日波动
        highs = prices * (1 + np.abs(np.random.normal(0, intraday_vol, n_days)))
        lows = prices * (1 - np.abs(np.random.normal(0, intraday_vol, n_days)))
        opens = prices * (1 + np.random.normal(0, intraday_vol * 0.3, n_days))
        
        # 确保 OHLC 关系
        highs = np.maximum(highs, np.maximum(opens, prices))
        lows = np.minimum(lows, np.minimum(opens, prices))
        
        vols = np.random.lognormal(10, 0.5, n_days)  # 成交量
        amounts = vols * prices * 10  # 成交额
        
        end_date = datetime.now()
        bars = []
        for i in range(n_days):
            date = (end_date - timedelta(days=n_days - 1 - i)).strftime('%Y%m%d')
            bars.append(OHLCVBar(
                ts_code=ts_code,
                trade_date=date,
                open=round(float(opens[i]), 2),
                high=round(float(highs[i]), 2),
                low=round(float(lows[i]), 2),
                close=round(float(prices[i]), 2),
                vol=round(float(vols[i]), 0),
                amount=round(float(amounts[i]), 2),
            ))
        return bars
    
    def fetch_daily(self, ts_code: str, start_date: str = None, 
                    end_date: str = None, n_days: int = 252) -> StockPriceSeries:
        bars = self._generate_bars(ts_code, n_days)
        return StockPriceSeries(ts_code=ts_code, freq='daily', bars=bars)


class TushareDataSource(BaseDataSource):
    """
    Tushare Pro 数据源 — 需要 API token
    
    安装: pip install tushare
    使用: 需要 ~/.tushare/token 或环境变量 TUSHARE_TOKEN
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.token = self.config.get('token') or os.environ.get('TUSHARE_TOKEN')
        if not self.token:
            raise RuntimeError("Tushare token 未配置。请设置 TUSHARE_TOKEN 环境变量或传入 token 参数")
    
    def _get_pro_api(self):
        import tushare as ts
        ts.set_token(self.token)
        return ts.pro_api()
    
    def fetch_daily(self, ts_code: str, start_date: str, end_date: str) -> StockPriceSeries:
        pro = self._get_pro_api()
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        
        bars = []
        for _, row in df.iterrows():
            bars.append(OHLCVBar(
                ts_code=ts_code,
                trade_date=row['trade_date'],
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
                vol=row['vol'],
                amount=row['amount'],
            ))
        bars.reverse()  # Tushare 返回最新在前，需反转
        return StockPriceSeries(ts_code=ts_code, freq='daily', bars=bars)


class AkShareDataSource(BaseDataSource):
    """
    AkShare 数据源 — 免 token，需安装 akshare
    
    安装: pip install akshare
    """
    
    def fetch_daily(self, ts_code: str, start_date: str, end_date: str) -> StockPriceSeries:
        import akshare as ak
        
        # AkShare 代码格式转换：000001.SZ → sz000001
        code = ts_code.split('.')[0]
        market = 'sh' if ts_code.endswith('.SH') else 'sz'
        ak_code = f"{market}{code}"
        
        df = ak.stock_zh_a_hist(
            symbol=ak_code, period="daily",
            start_date=start_date, end_date=end_date,
            adjust="qfq"  # 前复权
        )
        
        bars = []
        for _, row in df.iterrows():
            bars.append(OHLCVBar(
                ts_code=ts_code,
                trade_date=row['日期'].replace('-', ''),
                open=row['开盘'],
                high=row['最高'],
                low=row['最低'],
                close=row['收盘'],
                vol=row['成交量'],
                amount=row['成交额'],
            ))
        return StockPriceSeries(ts_code=ts_code, freq='daily', bars=bars)


# ---------------------------------------------------------------------------
# 数据管道核心
# ---------------------------------------------------------------------------

class DataPipe:
    """
    数据管道 — 统一入口
    
    使用示例:
        >>> pipe = DataPipe(source='simulated')
        >>> series = pipe.get_daily('000001.SZ', n_days=252)
        >>> volfac_input = series.to_volfac_raw(lookback_days=60)
    """
    
    CACHE_DIR = os.path.expanduser("~/.quant_cache")
    
    def __init__(self, source: str = 'simulated', config: Dict[str, Any] = None):
        self.source_type = DataSourceType(source)
        self.config = config or {}
        self.state = DataPipeState(source=source)
        
        # 初始化数据源
        self._source = self._init_source()
        
        # 内存缓存
        self._memory_cache: Dict[str, StockPriceSeries] = {}
    
    def _init_source(self) -> BaseDataSource:
        if self.source_type == DataSourceType.SIMULATED:
            return SimulatedDataSource(self.config)
        elif self.source_type == DataSourceType.TUSHARE:
            return TushareDataSource(self.config)
        elif self.source_type == DataSourceType.AKSHARE:
            return AkShareDataSource(self.config)
        elif self.source_type == DataSourceType.LOCAL_CSV:
            raise NotImplementedError("LOCAL_CSV 数据源尚未实现")
        else:
            raise ValueError(f"未知数据源: {self.source_type}")
    
    def get_daily(self, ts_code: str, n_days: int = 252,
                   start_date: str = None, end_date: str = None) -> StockPriceSeries:
        """
        获取日频数据
        
        Args:
            ts_code: 股票代码，如 '000001.SZ'
            n_days: 获取日数（模拟数据模式）
            start_date/end_date: 日期范围（真实数据源模式），如 '20240101'
        
        Returns:
            StockPriceSeries
        """
        cache_key = f"{ts_code}_{self.source_type.value}_{n_days}"
        
        # 检查内存缓存
        if cache_key in self._memory_cache:
            self.state.cached_count += 1
            return self._memory_cache[cache_key]
        
        try:
            if self.source_type == DataSourceType.SIMULATED:
                series = self._source.fetch_daily(ts_code, n_days=n_days)
            else:
                if not start_date or not end_date:
                    end = datetime.now()
                    start = end - timedelta(days=n_days)
                    end_date = end.strftime('%Y%m%d')
                    start_date = start.strftime('%Y%m%d')
                series = self._source.fetch_daily(ts_code, start_date, end_date)
            
            self._memory_cache[cache_key] = series
            self.state.last_update = datetime.now().isoformat()
            return series
        
        except Exception as e:
            self.state.error_log.append(f"{datetime.now()}: {ts_code} - {str(e)}")
            raise
    
    def get_multi(self, ts_codes: List[str], n_days: int = 252) -> Dict[str, StockPriceSeries]:
        """批量获取"""
        return {code: self.get_daily(code, n_days) for code in ts_codes}
    
    def to_volfac_input(self, series: StockPriceSeries, 
                         historical_series: StockPriceSeries = None) -> Dict[str, Any]:
        """
        将 StockPriceSeries 转换为 VOLFAC 对象卡输入
        
        Args:
            series: 主序列（至少60日）
            historical_series: 可选的历史序列（用于计算1年分位）
        """
        closes = series.close_list
        
        hist_vol = None
        if historical_series and len(historical_series.bars) >= 252:
            # 计算历史滚动 id2_std_3m
            hist_closes = historical_series.close_list
            hist_vol = []
            for i in range(60, len(hist_closes)):
                chunk = hist_closes[i-60:i]
                log_returns = np.log(np.array(chunk[1:]) / np.array(chunk[:-1]))
                hist_vol.append(float(np.std(log_returns, ddof=1)))
        
        return {
            'close_60d': closes[-60:] if len(closes) >= 60 else closes,
            'close_5m': None,
            'high_5m': None,
            'low_5m': None,
            'historical_vol_1y': hist_vol,
        }
    
    def get_state(self) -> Dict[str, Any]:
        """获取管道状态"""
        return {
            'source': self.state.source,
            'last_update': self.state.last_update,
            'cached_count': self.state.cached_count,
            'error_count': len(self.state.error_log),
            'recent_errors': self.state.error_log[-5:],
        }


# ---------------------------------------------------------------------------
# 快速测试: 端到端验证 DataPipe → VOLFAC
# ---------------------------------------------------------------------------

def _quick_test():
    """端到端验证：数据管道 → VOLFAC 对象卡"""
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from object_card_volfac import VolatilityFactor, VolFacRawInput
    
    print("=" * 70)
    print("数据管道原型 — 端到端验证")
    print("=" * 70)
    
    # 1. 初始化模拟数据管道
    print("\n【Step 1】初始化模拟数据管道")
    pipe = DataPipe(source='simulated', config={'annual_vol': 0.35, 'seed': 2025})
    print(f"  数据源: {pipe.state.source}")
    print(f"  缓存目录: {pipe.CACHE_DIR}")
    
    # 2. 获取单只股票数据
    print("\n【Step 2】拉取模拟数据（000001.SZ, 252日）")
    series = pipe.get_daily('000001.SZ', n_days=252)
    print(f"  代码: {series.ts_code}")
    print(f"  数据量: {len(series.bars)} 根K线")
    print(f"  日期范围: {series.date_list[0]} ~ {series.date_list[-1]}")
    print(f"  价格范围: {min(series.low_list):.2f} ~ {max(series.high_list):.2f}")
    
    # 3. 转换为 VOLFAC 输入
    print("\n【Step 3】转换为 VOLFAC 输入格式")
    volfac_dict = pipe.to_volfac_input(series)
    print(f"  close_60d: {len(volfac_dict['close_60d'])} 日")
    print(f"  historical_vol_1y: {volfac_dict['historical_vol_1y'] is None}")
    
    # 4. 运行 VOLFAC 对象卡
    print("\n【Step 4】运行 VOLFAC 对象卡")
    vf = VolatilityFactor()
    raw = VolFacRawInput(**volfac_dict)
    result = vf.calculate(raw, strategy_type='swing', market_cap=80)
    
    print(f"  object_id: {result.object_id}")
    print(f"  signal_strength: {result.signal_strength}")
    print(f"  confidence: {result.confidence}")
    print(f"  filter_action: {result.filter_action}")
    print(f"  risk_action: {result.risk_action}")
    print(f"  size_scalar: {result.size_scalar}")
    print(f"  vol_regime: {result.internal.get('vol_regime')}")
    print(f"  annualized_vol: {result.internal.get('annualized_vol')}")
    
    # 5. 批量获取测试
    print("\n【Step 5】批量获取（5只股票）")
    codes = ['000001.SZ', '000002.SZ', '600000.SH', '600519.SH', '300750.SZ']
    multi = pipe.get_multi(codes, n_days=252)
    for code, s in multi.items():
        volfac_d = pipe.to_volfac_input(s)
        r = VolatilityFactor().calculate(VolFacRawInput(**volfac_d), strategy_type='swing', market_cap=50)
        print(f"  {code}: vol_regime={r.internal.get('vol_regime'):12s} "
              f"strength={r.signal_strength:+d} size_scalar={r.size_scalar:.2f}")
    
    # 6. 管道状态
    print("\n【Step 6】管道状态")
    state = pipe.get_state()
    for k, v in state.items():
        print(f"  {k}: {v}")
    
    print("\n" + "=" * 70)
    print("✅ 端到端验证通过: DataPipe → VOLFAC 对象卡")
    print("=" * 70)
    print("\n下一步: 安装 tushare/akshare 后，将 source='simulated' 替换为 'tushare' 或 'akshare'")


if __name__ == "__main__":
    _quick_test()
