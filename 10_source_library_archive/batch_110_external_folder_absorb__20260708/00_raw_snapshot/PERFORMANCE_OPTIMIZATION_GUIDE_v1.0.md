# 性能优化指南 v1.0

> **本文档全部内容源于用户（仓库所有者）的想法，由 Kimi 整理为结构化文档供编程 AI 参考。**
> 版本：v1.0 | 状态：设计阶段 | 核心目标：定义数据处理、特征计算、回测执行的性能基准和优化策略

---

## 一、性能基准

```text
┌─────────────────────────────────────────────────────────────────────┐
│                        性能基准要求                                  │
│                                                                     │
│  操作                          │ 目标耗时     │ 数据量        │ 工具  │
│  ──────────────────────────────┼─────────────┼──────────────┼────── │
│  加载 5000 只日 OHLCV          │ < 5 秒       │ 5000×1000 行 │ polars│
│  加载 500 只 60min OHLCV       │ < 3 秒       │ 500×5000 行  │ polars│
│  单只标的特征计算（全对象卡）     │ < 1 秒       │ 1000 行      │ polars│
│  全 A 股特征计算（单对象卡）      │ < 30 秒      │ 5000×1000 行 │ polars│
│  单因子回测（1 年）              │ < 2 分钟     │ 5000×250 行  │ polars│
│  组合回测（1 年，7 对象卡）       │ < 10 分钟    │ 5000×250 行  │ polars│
│  系统回测（3 年）                │ < 30 分钟    │ 5000×750 行  │ polars│
│  每日 ETL（收盘后）              │ < 15 分钟    │ 全量         │ polars│
│  控制台渲染                      │ < 500 毫秒   │ -            │ ANSI  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

内存基准：
  - 常驻内存：日 OHLCV（5000 只 × 1000 日）≈ 500 MB
  - 按需加载：60min OHLCV（500 只 × 3 个月）≈ 50 MB
  - 特征缓存：Feature Store（每日增量）≈ 100 MB
  - 总内存预算：< 2 GB（单机运行）
```

---

## 二、数据处理优化

### 2.1 polars 优先原则

```text
【强制规则】所有新代码使用 polars，pandas 仅用于兼容旧代码

polars 优势：
  - 速度：比 pandas 快 5-30 倍（取决于操作）
  - 内存：比 pandas 节省 2-5 倍内存
  - 并行：自动利用多核（无需额外代码）
  - 惰性：支持 LazyFrame，延迟执行优化

迁移指南：
  pandas → polars 常见替换：
  
  pd.read_csv() → pl.read_csv()
  df.groupby() → df.group_by()
  df.merge() → df.join()
  df.apply() → 避免使用，改用 with_columns() + pl.col()
  df.iterrows() → 避免使用，改用表达式

示例：
  ```python
  # pandas（慢）
  df["sma_20"] = df["close"].rolling(window=20).mean()
  
  # polars（快）
  df = df.with_columns(
      pl.col("close").rolling_mean(window_size=20).alias("sma_20")
  )
  ```
```

### 2.2 数据加载优化

```python
class DataLoader:
    """
    数据加载器（优化版）
    """
    
    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = data_dir
        self.cache: dict[str, pl.DataFrame] = {}  # 内存缓存
    
    def load_daily_ohlcv(self, symbols: list[str],
                         start: str, end: str) -> pl.DataFrame:
        """
        批量加载日 OHLCV（优化版）
        
        优化策略：
        1. 按日期范围过滤，不加载全量
        2. 使用 Parquet 格式（比 CSV 快 10 倍）
        3. 内存缓存，避免重复加载
        4. 只加载需要的列（projection pushdown）
        5. 使用 scan_parquet（惰性加载）
        """
        cache_key = f"daily_{start}_{end}_{len(symbols)}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # 使用 scan_parquet 惰性加载
        lazy_frames = []
        for symbol in symbols:
            path = f"{self.data_dir}/daily_ohlcv/{symbol}.parquet"
            
            # 惰性加载 + 日期过滤 + 列选择
            lf = pl.scan_parquet(path).filter(
                (pl.col("date") >= start) & (pl.col("date") <= end)
            ).select([
                "date", "open", "high", "low", "close", "volume", "amount", "symbol"
            ])
            
            lazy_frames.append(lf)
        
        # 合并并执行（只执行一次）
        combined = pl.concat(lazy_frames).collect()
        
        # 缓存
        self.cache[cache_key] = combined
        
        return combined
    
    def clear_cache(self):
        """清理缓存（每日收盘后调用）"""
        self.cache.clear()
```

### 2.3 内存管理策略

```text
分层加载策略：

第一层（常驻内存）：
  - 日 OHLCV（最近 500 日，5000 只）
  - 周线 OHLCV（从日线合成，不额外存储）
  - 对象卡注册表（object_registry.json）
  - 策略组合配置（strategy_bundles.yaml）
  总内存：~500 MB

第二层（按需加载，LRU 缓存）：
  - 60min OHLCV（关注的 500 只，最近 3 个月）
  - 15min OHLCV（关注的 100 只，最近 1 个月）
  - 5min OHLCV（关注的 50 只，最近 1 周）
  - 财报数据（基本面候选池，最近 2 期）
  总内存：~300 MB，LRU 大小 100

第三层（实时计算，不缓存）：
  - 1min OHLCV（仅日内策略使用）
  - 特征计算中间结果
  - 回测中间结果
  总内存：~200 MB，用完即释放

缓存淘汰策略：
  - 使用 functools.lru_cache 或 cachetools
  - 容量：100（第二层）/ 50（第三层）
  - TTL：第二层 1 小时，第三层 10 分钟
  - 每日收盘后强制清理所有缓存
```

---

## 三、特征计算优化

### 3.1 向量化计算

```python
# 反例：循环计算（慢）
def calculate_atr_slow(df: pd.DataFrame, period: int = 14) -> pd.Series:
    atr = []
    for i in range(len(df)):
        if i == 0:
            atr.append(df.iloc[i]["high"] - df.iloc[i]["low"])
        else:
            tr1 = df.iloc[i]["high"] - df.iloc[i]["low"]
            tr2 = abs(df.iloc[i]["high"] - df.iloc[i-1]["close"])
            tr3 = abs(df.iloc[i]["low"] - df.iloc[i-1]["close"])
            atr.append(max(tr1, tr2, tr3))
    return pd.Series(atr).rolling(window=period).mean()

# 正例：向量化计算（快 100 倍）
def calculate_atr_fast(df: pl.DataFrame, period: int = 14) -> pl.Series:
    return df.with_columns(
        pl.max_horizontal([
            pl.col("high") - pl.col("low"),
            (pl.col("high") - pl.col("close").shift(1)).abs(),
            (pl.col("low") - pl.col("close").shift(1)).abs(),
        ]).alias("tr")
    ).with_columns(
        pl.col("tr").rolling_mean(window_size=period).alias("atr")
    )["atr"]
```

### 3.2 预计算与缓存

```python
class FeatureStore:
    """
    特征缓存（预计算 + 增量更新）
    """
    
    def __init__(self, cache_dir: str = "data/processed/feature_store"):
        self.cache_dir = cache_dir
    
    def precompute_features(self, symbol: str, date: str) -> dict:
        """
        预计算所有对象卡所需的特征
        
        优化策略：
        1. 一次性计算所有特征（避免重复读取数据）
        2. 使用 LazyFrame 延迟执行
        3. 只保存需要的特征列
        4. 按 symbol/date 分区存储
        """
        # 加载原始数据
        ohlcv = pl.scan_parquet(f"data/raw/daily_ohlcv/{symbol}.parquet")
        
        # 一次性计算所有特征（使用 LazyFrame）
        features = ohlcv.with_columns([
            # 技术指标
            pl.col("close").rolling_mean(20).alias("sma_20"),
            pl.col("close").rolling_mean(60).alias("sma_60"),
            pl.col("close").rolling_std(20).alias("std_20"),
            
            # 波动率
            (pl.col("high") - pl.col("low")).alias("range"),
            pl.col("range").rolling_mean(20).alias("atr_20"),
            
            # 成交量
            pl.col("volume").rolling_mean(20).alias("vol_sma_20"),
            (pl.col("volume") / pl.col("vol_sma_20")).alias("vol_ratio"),
            
            # 价格动量
            (pl.col("close") / pl.col("close").shift(20) - 1).alias("momentum_20"),
            (pl.col("close") / pl.col("close").shift(60) - 1).alias("momentum_60"),
        ])
        
        # 只执行一次，保存结果
        result = features.collect()
        
        # 保存到 Feature Store
        output_path = f"{self.cache_dir}/{symbol}/{date}.parquet"
        result.write_parquet(output_path)
        
        return {"path": output_path, "rows": len(result)}
    
    def incremental_update(self, symbol: str, new_date: str) -> dict:
        """
        增量更新特征（只计算新增日期）
        """
        # 读取已有特征
        existing = pl.read_parquet(f"{self.cache_dir}/{symbol}/latest.parquet")
        
        # 计算新日期特征
        new_features = self.precompute_features(symbol, new_date)
        
        # 合并（避免全量重算）
        updated = pl.concat([existing, new_features])
        
        # 保存
        updated.write_parquet(f"{self.cache_dir}/{symbol}/latest.parquet")
        
        return {"updated_rows": len(updated)}
```

### 3.3 并行计算

```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import multiprocessing as mp

class ParallelFeatureCalculator:
    """
    并行特征计算器
    """
    
    def __init__(self, n_workers: int | None = None):
        # 默认使用 CPU 核心数 - 1（留一个给系统）
        self.n_workers = n_workers or max(1, mp.cpu_count() - 1)
    
    def calculate_for_all_symbols(self, symbols: list[str],
                                   calculator: callable) -> dict:
        """
        对所有标的并行计算特征
        
        策略：
        - CPU 密集型（数值计算）→ ProcessPoolExecutor
        - IO 密集型（数据加载）→ ThreadPoolExecutor
        """
        results = {}
        
        with ProcessPoolExecutor(max_workers=self.n_workers) as executor:
            # 提交所有任务
            futures = {
                executor.submit(calculator, symbol): symbol
                for symbol in symbols
            }
            
            # 收集结果
            for future in futures:
                symbol = futures[future]
                try:
                    results[symbol] = future.result(timeout=30)
                except Exception as e:
                    results[symbol] = {"error": str(e)}
        
        return results
    
    def calculate_batch(self, symbols: list[str], date: str) -> pl.DataFrame:
        """
        批量计算（使用 polars 内置并行）
        
        polars 的 group_by 操作自动并行，无需手动处理
        """
        # 加载所有数据
        df = self.load_all_symbols(symbols, date)
        
        # polars 自动并行计算
        result = df.group_by("symbol").agg([
            pl.col("close").rolling_mean(20).alias("sma_20"),
            pl.col("close").rolling_std(20).alias("std_20"),
            pl.col("volume").sum().alias("total_volume"),
        ])
        
        return result
```

---

## 四、回测执行优化

### 4.1 事件驱动 vs 向量化回测

```text
两种回测模式：

模式 A：事件驱动（逐日/逐笔模拟）
  - 适用：精细模拟（滑点、订单簿、T+1）
  - 缺点：慢（每只标的每轮循环）
  - 速度：~500 只/秒

模式 B：向量化回测（矩阵运算）
  - 适用：快速筛选（信号生成、绩效统计）
  - 优点：极快（一次性计算全量）
  - 速度：~5000 只/秒

推荐策略：
  - 单因子回测：向量化（快速筛选）
  - 组合回测：事件驱动（精细模拟）
  - 系统回测：混合模式（向量化预选 + 事件驱动精细回测）

混合模式实现：
  ```python
  class HybridBacktestEngine:
      def run(self, strategy, start, end):
          # 阶段 1：向量化快速筛选（找出有信号的日期/标的）
          candidates = self.vectorized_screen(strategy, start, end)
          
          # 阶段 2：事件驱动精细回测（只对有信号的候选执行）
          results = self.event_driven_backtest(candidates, strategy)
          
          return results
  ```
```

### 4.2 回测加速技巧

```python
class BacktestOptimizer:
    """
    回测优化器
    """
    
    def optimize(self, engine: BacktestEngine) -> BacktestEngine:
        """
        应用优化策略
        """
        # 1. 数据预加载（避免回测中重复 IO）
        engine.preload_data()
        
        # 2. 特征预计算（回测前计算所有特征）
        engine.precompute_features()
        
        # 3. 使用 Numba 加速循环（如果必须使用循环）
        engine.compile_with_numba()
        
        # 4. 禁用不必要的日志（回测中不写审计日志）
        engine.disable_audit_logging()
        
        # 5. 批量订单处理（合并同日订单）
        engine.batch_orders = True
        
        return engine
    
    def compile_with_numba(self):
        """
        使用 Numba JIT 编译加速关键函数
        
        注意：Numba 只支持 numpy 数组，不支持 polars DataFrame
        适用场景：纯数值计算（如 Kelly 公式、止损计算）
        """
        from numba import jit
        
        @jit(nopython=True)
        def calculate_kelly_fast(wins, losses, avg_win, avg_loss):
            """Kelly 公式加速版"""
            win_rate = wins / (wins + losses)
            b = avg_win / avg_loss if avg_loss > 0 else 1.0
            return win_rate - (1 - win_rate) / b
```

---

## 五、存储优化

### 5.1 Parquet 最佳实践

```text
Parquet 格式选择：
  - 压缩：zstd（压缩率高，解压快）
  - 编码：delta（时间序列）/ dictionary（分类数据）
  - 行组大小：100,000（平衡读写性能）
  - 分区：按 symbol / date 分区

写入优化：
  ```python
  df.write_parquet(
      path,
      compression="zstd",
      statistics=True,  # 启用统计信息（加速过滤）
      row_group_size=100000,
  )
  ```

读取优化：
  ```python
  # 只读需要的列（projection pushdown）
  pl.scan_parquet(path).select(["close", "volume"]).collect()
  
  # 只读需要的行（predicate pushdown）
  pl.scan_parquet(path).filter(pl.col("date") >= "2024-01-01").collect()
  ```
```

### 5.2 特征缓存策略

```text
缓存层级：

L1 缓存（内存）：
  - 最近 3 日特征（热数据）
  - 使用 Python dict / lru_cache
  - TTL：1 小时

L2 缓存（磁盘 SSD）：
  - 最近 30 日特征（温数据）
  - 使用 Parquet 文件
  - 路径：data/processed/feature_store/{symbol}/{date}.parquet

L3 存储（磁盘 HDD）：
  - 历史特征（冷数据）
  - 使用压缩 Parquet
  - 路径：data/archive/feature_store/{year}/{symbol}.parquet

缓存更新策略：
  - 每日收盘后：更新 L1/L2 缓存
  - 每月：归档到 L3
  - 每季度：清理 L3（保留 2 年）
```

---

## 六、控制台优化

### 6.1 渲染优化

```python
class ConsoleRenderer:
    """
    控制台渲染优化
    
    目标：渲染时间 < 500 毫秒
    """
    
    def __init__(self):
        self._last_render = ""
        self._cache = {}
    
    def render(self, dashboard_data: dict) -> str:
        """
        渲染仪表盘（优化版）
        
        优化策略：
        1. 只渲染变化的部分（增量渲染）
        2. 使用字符串拼接而非格式化
        3. 缓存静态部分（如边框、标题）
        4. 避免重复计算
        """
        # 检查数据变化
        data_hash = hash(json.dumps(dashboard_data, sort_keys=True))
        if data_hash == self._cache.get("hash"):
            return self._cache["output"]
        
        # 渲染（使用列表拼接，比 += 快）
        lines = []
        lines.append(self._render_header(dashboard_data))
        lines.append(self._render_regime_panel(dashboard_data))
        lines.append(self._render_market_panel(dashboard_data))
        lines.append(self._render_cabinet_panel(dashboard_data))
        lines.append(self._render_memorials(dashboard_data))
        lines.append(self._render_portfolio(dashboard_data))
        lines.append(self._render_quick_actions(dashboard_data))
        lines.append(self._render_footer(dashboard_data))
        
        output = "\n".join(lines)
        
        # 缓存
        self._cache["hash"] = data_hash
        self._cache["output"] = output
        
        return output
    
    def _render_header(self, data: dict) -> str:
        """渲染头部（缓存）"""
        # 静态部分只生成一次
        if "header" not in self._cache:
            self._cache["header"] = "╔" + "═" * 70 + "╗"
        return self._cache["header"]
```

---

## 七、监控与诊断

### 7.1 性能监控

```python
import time
from functools import wraps

class PerformanceMonitor:
    """性能监控器"""
    
    metrics: dict[str, list[float]] = {}
    
    @staticmethod
    def timed(label: str):
        """装饰器：记录函数执行时间"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - start
                
                PerformanceMonitor.record(label, elapsed)
                
                return result
            return wrapper
        return decorator
    
    @staticmethod
    def record(label: str, elapsed: float):
        """记录性能指标"""
        if label not in PerformanceMonitor.metrics:
            PerformanceMonitor.metrics[label] = []
        PerformanceMonitor.metrics[label].append(elapsed)
    
    @staticmethod
    def report() -> dict:
        """生成性能报告"""
        report = {}
        for label, times in PerformanceMonitor.metrics.items():
            report[label] = {
                "count": len(times),
                "total": sum(times),
                "mean": sum(times) / len(times),
                "max": max(times),
                "min": min(times),
            }
        return report

# 使用示例
@PerformanceMonitor.timed("object_card_calculation")
def calculate_chzl_bsd(data):
    # ... 计算逻辑
    pass
```

### 7.2 内存诊断

```python
import tracemalloc

class MemoryProfiler:
    """内存分析器"""
    
    def __init__(self):
        tracemalloc.start()
    
    def snapshot(self, label: str = "") -> dict:
        """内存快照"""
        current, peak = tracemalloc.get_traced_memory()
        
        # 获取内存分配详情
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics("lineno")[:10]
        
        return {
            "label": label,
            "current_mb": current / 1024 / 1024,
            "peak_mb": peak / 1024 / 1024,
            "top_allocators": [
                {"file": stat.traceback.format()[-1], "size_mb": stat.size / 1024 / 1024}
                for stat in top_stats
            ],
        }
```

---

## 八、对编程 AI 的指令

```text
1. 所有新代码使用 polars，pandas 仅用于兼容
2. 特征计算使用向量化，避免循环
3. 数据加载使用 scan_parquet + 惰性过滤
4. 回测使用混合模式（向量化筛选 + 事件驱动精细回测）
5. 内存使用分层策略，每日收盘后清理缓存
6. 使用 @PerformanceMonitor.timed 装饰器监控关键函数
7. 性能测试必须有明确阈值，超过即失败
8. 代码提交前必须运行性能基准测试，确认无退化
```

---

> 文件：PERFORMANCE_OPTIMIZATION_GUIDE_v1.0.md
> 生产者：Kimi（性能优化设计）
> 核心设计：polars 优先 + 向量化计算 + 预计算缓存 + 混合回测模式
> 性能目标：全 A 股单因子回测 < 2 分钟 / 系统回测 < 30 分钟
