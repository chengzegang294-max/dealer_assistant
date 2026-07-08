# 数据管道 ETL 详细设计 v1.0

> **本文档全部内容源于用户（仓库所有者）的想法，由 Kimi 整理为结构化文档供编程 AI 参考。**
> 版本：v1.0 | 状态：设计阶段 | 来源：用户问题2（标准化进库流程）+ 数据审计清单
> 核心目标：定义新资料进库的标准化流程、全库文件夹结构、数据质量管理规范

---

## 一、数据管道总览

```text
┌─────────────────────────────────────────────────────────────────────┐
│                        数据管道架构                                  │
│                                                                     │
│   数据源层                    管道层                    存储层       │
│   ─────────                  ───────                  ──────       │
│                                                                     │
│  ┌──────────┐               ┌──────────┐             ┌──────────┐  │
│  │ tushare  │──────────────→│ Extract  │             │  raw/    │  │
│  │ akshare  │──────────────→│ （提取） │────────────→│ 原始数据 │  │
│  │ Wind     │──────────────→│          │             │          │  │
│  │ 手动上传 │──────────────→│          │             └──────────┘  │
│  └──────────┘               └──────────┘                  │        │
│                                     │                     │        │
│                                     ▼                     ▼        │
│                              ┌──────────┐             ┌──────────┐  │
│                              │ Validate │             │ processed│  │
│                              │ （验证） │────────────→│ 清洗数据 │  │
│                              └──────────┘             │          │  │
│                                     │                 └──────────┘  │
│                                     ▼                      │       │
│                              ┌──────────┐                  │       │
│                              │Transform │                  │       │
│                              │ （转换） │──────────────────┘       │
│                              └──────────┘                          │
│                                     │                               │
│                                     ▼                               │
│                              ┌──────────┐             ┌──────────┐  │
│                              │  Load    │────────────→│ Feature  │  │
│                              │ （加载） │             │ Store    │  │
│                              └──────────┘             │ 特征缓存 │  │
│                                                       └──────────┘  │
└─────────────────────────────────────────────────────────────────────┘

数据流向：raw → validate → transform → load → feature_store
数据不回流：processed 数据不修改 raw，feature_store 不修改 processed
```

---

## 二、标准化文件夹结构

### 2.1 仓库根目录

```
D:\Stock\trading_assistant\          # 主仓库（当前工作目录）
│
├── data\                              # 【数据层】所有数据放这里
│   ├── raw\                          # 原始数据（不可修改，只追加）
│   │   ├── daily_ohlcv\            # 日 OHLCV（前复权）
│   │   │   └── YYYY\               # 按年分目录
│   │   │       └── daily_ohlcv_YYYYMMDD.parquet
│   │   ├── minute_ohlcv\           # 分钟级 OHLCV（按需存储）
│   │   │   ├── 60min\             # 60分钟
│   │   │   ├── 15min\             # 15分钟
│   │   │   └── 5min\              # 5分钟
│   │   ├── wind_fund_flow\        # Wind 资金流向
│   │   ├── financial_reports\     # 财报数据（季报/年报）
│   │   │   ├── balance_sheet\    # 资产负债表
│   │   │   ├── income_statement\ # 利润表
│   │   │   └── cash_flow\        # 现金流量表
│   │   ├── macro_data\            # 宏观数据
│   │   │   ├── interest_rate\    # 利率（国债收益率）
│   │   │   ├── exchange_rate\    # 汇率
│   │   │   ├── liquidity\        # 流动性（M2/SHIBOR）
│   │   │   └── policy\           # 政策事件（JSON格式）
│   │   └── index_constituents\    # 指数成分股（沪深300/中证500等）
│   │
│   ├── processed\                    # 清洗后的数据（可重新生成）
│   │   ├── feature_store\          # 特征缓存（核心）
│   │   │   ├── structure\        # 结构层特征（缠论笔/中枢）
│   │   │   ├── execution\        # 执行层特征（VP/MFLOW/波动率）
│   │   │   ├── risk\             # 风控层特征（Kelly/VolTarget）
│   │   │   ├── selection\        # 选股层特征（A5财报/DY评分）
│   │   │   └── fundamental\      # 基本面特征（PE/PB/ROE）
│   │   │
│   │   └── backtest_results\       # 回测结果
│   │       ├── single_factor\    # 单因子回测结果
│   │       ├── combined\         # 组合回测结果
│   │       └── out_of_sample\    # 样本外测试结果
│   │
│   └── metadata\                    # 元数据（数据目录与质量）
│       ├── data_catalog.json       # 数据目录（所有数据文件索引）
│       ├── data_quality_report.md  # 数据质量报告（自动生成）
│       ├── version_control.log     # 数据版本控制日志
│       └── etl_schedule.yaml       # ETL 调度配置
│
├── src\                               # 【源代码层】
│   ├── backtest_engine\             # 回测引擎
│   ├── governance\                  # 治理架构
│   ├── data_pipeline\              # 数据管道（本模块）
│   │   ├── extractors\            # 提取器（从数据源获取）
│   │   │   ├── tushare_extractor.py
│   │   │   ├── akshare_extractor.py
│   │   │   ├── wind_extractor.py
│   │   │   └── local_extractor.py
│   │   ├── transformers\          # 转换器（清洗、标准化）
│   │   │   ├── ohlcv_transformer.py
│   │   │   ├── fundamental_transformer.py
│   │   │   ├── macro_transformer.py
│   │   │   └── feature_engineer.py
│   │   ├── loaders\              # 加载器（入库）
│   │   │   ├── parquet_loader.py
│   │   │   ├── feature_store_loader.py
│   │   │   └── catalog_updater.py
│   │   ├── validators\            # 验证器（质量检查）
│   │   │   ├── ohlcv_validator.py
│   │   │   ├── fundamental_validator.py
│   │   │   └── completeness_validator.py
│   │   ├── etl_orchestrator.py    # ETL 编排器（主入口）
│   │   └── schedule.py            # 定时调度
│   ├── fundamental\                # A5财报选股层
│   ├── dy_scoring\                # DY评分层
│   ├── utils\                      # 工具函数
│   └── tests\                      # 单元测试
│
├── docs\                               # 【文档层】
│   ├── objects\                     # 对象卡文档
│   ├── architecture\               # 架构文档
│   ├── reference\                  # 参考资料
│   │   ├── basic_knowledge\       # 基础认知库
│   │   ├── asset_profiles\        # 标的基本面库
│   │   ├── indicator_tools\       # 指标工具库
│   │   └── strategy_rules\        # 个人策略库
│   └── reports\                   # 回测报告 + 日报
│
├── config\                             # 【配置层】
│   ├── backtest_config.yaml        # 回测参数
│   ├── object_registry.json        # 对象卡注册表
│   ├── data_sources.json           # 数据源配置（API密钥等）
│   ├── strategy_bundles.yaml       # 策略组合配置
│   └── etl_config.yaml            # ETL 配置
│
├── notebooks\                          # 【分析 notebook】
│   ├── exploration\                # 探索性分析
│   ├── validation\                # 验证分析
│   └── reports\                   # 报告生成
│
├── logs\                               # 【日志层】
│   ├── backtest\                   # 回测日志
│   ├── data_pipeline\             # 数据管道日志
│   ├── governance\                # 治理审计日志
│   └── risk_audit\               # 风控审计日志
│
└── scripts\                            # 【脚本层】
    ├── data_sync.sh               # 数据同步脚本
    ├── backtest_run.sh           # 回测运行脚本
    ├── report_generate.sh       # 报告生成脚本
    └── daily_etl.sh             # 每日 ETL 脚本
```

### 2.2 关键目录权限规则

```text
raw/          → 只读（除 ETL 管道外，任何代码不得写入）
processed/    → 可读写（但保留重新生成的能力）
metadata/     → 可读写（ETL 自动更新）
config/       → 只读（修改需用户确认）
logs/         → 追加写入（不可修改历史日志）
```

---

## 三、新资料进库标准化流程

### 3.1 流程图

```text
新资料进库六步法：

Step 1: 分类（必须人工判断）
  输入: 新资料（文件/数据/API）
  问题: 这是什么类型的资料？
  判断:
    ├─ OHLCV 数据     → raw/ohlcv/
    ├─ 财报数据       → raw/financial_reports/
    ├─ 宏观数据       → raw/macro_data/
    ├─ 资金流向       → raw/wind_fund_flow/
    ├─ 对象卡定义     → docs/objects/
    ├─ 参考资料       → docs/reference/
    ├─ 策略/规则      → docs/architecture/ 或 config/
    └─ 配置参数       → config/

Step 2: 命名（自动化检查）
  工具: naming_validator.py
  检查项:
    ├─ 是否符合命名规范？
    ├─ 文件名是否唯一？
    └─ 时间戳/版本号是否完整？
  
  命名规范:
    数据文件: {type}_{symbol}_{start_date}_{end_date}_{version}.parquet
      例: daily_ohlcv_000001_sz_20180101_20241231_v1.0.parquet
    
    对象卡:  OBJECT_CARD_{id}_{name}_v{version}.md
      例: OBJECT_CARD_MFLOW_P0_A__MoneyFlow_v1.0.md
    
    参考资料: {source}_{topic}_{date}_v{version}.md
      例: video_周期女王_20240128_v1.0.md
    
    配置文件: {name}_config_v{version}.{ext}
      例: backtest_config_v1.0.yaml

Step 3: 元数据登记（自动化）
  工具: catalog_updater.py
  更新: data/metadata/data_catalog.json
  
  登记字段:
    {
      "file_path": "data/raw/daily_ohlcv/2024/daily_ohlcv_20240624.parquet",
      "file_name": "daily_ohlcv_20240624.parquet",
      "type": "daily_ohlcv",
      "symbols": ["000001.SZ", "000002.SZ", ...],
      "date_range": ["2024-06-24", "2024-06-24"],
      "source": "tushare",
      "created_at": "2024-06-24T17:00:00+08:00",
      "version": "1.0",
      "size_bytes": 12345678,
      "row_count": 5000,
      "hash_sha256": "abc123...",
      "status": "active",        // active / deprecated / archived
      "etl_job_id": "etl-20240624-001",
      "quality_score": 95,       // 0-100
    }

Step 4: 数据质量检查（自动化）
  工具: data_quality_checker.py
  
  通用检查（所有数据）:
    □ 文件可读取（无损坏）
    □ 编码正确（UTF-8）
    □ 时间戳连续（无跳变）
    □ 无未来日期
  
  OHLCV 专用检查:
    □ 缺失率 < 5%
    □ 复权一致性（close ≈ amount/volume）
    □ 价格范围合理（无负值、无极端跳变 > 20%）
    □ 成交量一致性（vol > 0 当 price > 0）
    □ 时间对齐（日线 15:00，分钟级无重复）
  
  财报专用检查:
    □ 报表平衡（资产 = 负债 + 权益）
    □ 科目完整性（无缺失核心科目）
    □ 同比一致性（本期 vs 上期变化合理）
  
  宏观专用检查:
    □ 数据来源可靠（央行/统计局/Wind）
    □ 时间对齐（月度数据统一为月末）
    □ 异常值标记（超出 3 个标准差的数据标记为可疑）

Step 5: 版本控制（自动化）
  工具: version_controller.py
  
  操作:
    1. 计算文件 SHA256 哈希
    2. 写入 version_control.log
    3. 如果文件已存在 → 比较哈希
       - 哈希相同 → 跳过（无变化）
       - 哈希不同 → 创建新版本（自动递增 version）
    4. 旧版本标记为 deprecated（保留但不使用）

Step 6: 通知同步（自动化）
  工具: notification_dispatcher.py
  
  通知内容:
    - 新资料类型和路径
    - 数据质量评分
    - 影响的下游模块（需要重新计算特征）
  
  通知对象:
    - 数据管道日志（logs/data_pipeline/）
    - 受影响的对象卡（通过 object_registry.json 查找）
    - 用户（控制台消息）
```

### 3.2 进库流程的代码实现

```python
class DataOnboardingPipeline:
    """
    新资料进库管道
    
    六步流程的编排器
    """
    
    def __init__(self):
        self.naming_validator = NamingValidator()
        self.catalog_updater = CatalogUpdater()
        self.quality_checker = DataQualityChecker()
        self.version_controller = VersionController()
        self.notifier = NotificationDispatcher()
    
    def onboard(self, file_path: Path, data_type: str,
                source: str, metadata: dict) -> dict:
        """
        新资料进库主入口
        
        Args:
            file_path: 新资料文件路径
            data_type: 资料类型（ohlcv/fundamental/macro/...）
            source: 数据来源（tushare/akshare/wind/manual）
            metadata: 额外元数据
        
        Returns:
            {
                "success": bool,
                "file_path": str,
                "catalog_entry": dict,
                "quality_report": dict,
                "version": str,
                "notifications": list,
            }
        """
        result = {"success": False, "steps": []}
        
        try:
            # Step 1: 分类（已在外部完成，这里验证）
            target_dir = self._get_target_dir(data_type)
            
            # Step 2: 命名检查
            naming_ok, naming_msg = self.naming_validator.check(file_path, data_type)
            result["steps"].append({"step": "naming", "ok": naming_ok, "msg": naming_msg})
            if not naming_ok:
                raise ValueError(f"命名检查失败: {naming_msg}")
            
            # Step 3: 元数据登记
            catalog_entry = self.catalog_updater.register(
                file_path, data_type, source, metadata
            )
            result["catalog_entry"] = catalog_entry
            result["steps"].append({"step": "catalog", "ok": True})
            
            # Step 4: 质量检查
            quality_report = self.quality_checker.check(file_path, data_type)
            result["quality_report"] = quality_report
            result["steps"].append({"step": "quality", "ok": quality_report["passed"]})
            
            if not quality_report["passed"]:
                # 质量不通过 → 进入隔离区，不进入主库
                quarantine_path = self._move_to_quarantine(file_path)
                result["quarantine_path"] = str(quarantine_path)
                raise ValueError(f"质量检查失败: {quality_report['failures']}")
            
            # Step 5: 版本控制
            version = self.version_controller.register(file_path, target_dir)
            result["version"] = version
            result["steps"].append({"step": "version", "ok": True})
            
            # Step 6: 通知
            notifications = self.notifier.dispatch(
                event="DATA_ONBOARDED",
                data={
                    "file_path": str(file_path),
                    "data_type": data_type,
                    "quality_score": quality_report["score"],
                    "affected_modules": self._find_affected_modules(data_type),
                }
            )
            result["notifications"] = notifications
            result["steps"].append({"step": "notify", "ok": True})
            
            result["success"] = True
            
        except Exception as e:
            result["error"] = str(e)
            self.notifier.dispatch(
                event="DATA_ONBOARD_FAILED",
                data={"file_path": str(file_path), "error": str(e)}
            )
        
        return result
    
    def _get_target_dir(self, data_type: str) -> Path:
        """根据类型获取目标目录"""
        type_map = {
            "daily_ohlcv": "data/raw/daily_ohlcv",
            "minute_ohlcv": "data/raw/minute_ohlcv",
            "financial_report": "data/raw/financial_reports",
            "macro": "data/raw/macro_data",
            "fund_flow": "data/raw/wind_fund_flow",
        }
        return Path(type_map.get(data_type, "data/raw/misc"))
    
    def _find_affected_modules(self, data_type: str) -> list[str]:
        """查找受影响的下游模块"""
        # 从 object_registry.json 中查找依赖该数据类型的对象卡
        # 简化实现
        return []
```

---

## 四、ETL 日常调度

### 4.1 每日 ETL 流程

```text
每日收盘后 15:30 自动触发：

Job 1: OHLCV 同步（优先级：P0，耗时：~10分钟）
  ├─ 拉取当日日 OHLCV（全 A 股）
  ├─ 质量检查
  ├─ 写入 raw/daily_ohlcv/YYYY/MM/
  └─ 更新 catalog

Job 2: 资金流向同步（优先级：P0，耗时：~5分钟）
  ├─ 拉取 Wind 资金流向
  ├─ 质量检查
  ├─ 写入 raw/wind_fund_flow/
  └─ 更新 catalog

Job 3: 宏观数据同步（优先级：P1，耗时：~3分钟）
  ├─ 拉取利率/汇率/SHIBOR
  ├─ 质量检查
  ├─ 写入 raw/macro_data/
  └─ 更新 catalog

Job 4: 特征计算（优先级：P0，耗时：~30分钟）
  ├─ 读取当日 raw 数据
  ├─ 计算各对象卡所需特征
  ├─ 写入 processed/feature_store/
  └─ 更新 catalog

Job 5: 质量报告生成（优先级：P2，耗时：~2分钟）
  ├─ 扫描当日所有新入库数据
  ├─ 生成质量评分
  ├─ 写入 metadata/data_quality_report.md
  └─ 异常数据告警

失败处理：
  - 任一步骤失败 → 整体标记为 FAILED
  - 失败步骤重试 3 次
  - 3 次仍失败 → 发送告警（控制台 + 日志）
  - 已完成的步骤不回滚
```

### 4.2 财报季 ETL 流程

```text
财报季（4月/8月/10月）额外流程：

Job 6: 财报同步（优先级：P0，触发：财报发布后）
  ├─ 拉取最新季报/年报
  ├─ 质量检查（报表平衡、科目完整）
  ├─ 写入 raw/financial_reports/
  ├─ 触发 A5 基本面选股重算
  └─ 更新 catalog

Job 7: A5 候选池更新（优先级：P0，依赖：Job 6）
  ├─ 运行排雷检查
  ├─ 运行财务评分
  ├─ 运行估值评估
  ├─ 生成新的 A5 候选池
  └─ 通知选股层更新
```

---

## 五、数据质量管理

### 5.1 质量评分体系

```python
class DataQualityChecker:
    """数据质量检查器"""
    
    def check_ohlcv(self, df: pl.DataFrame) -> dict:
        """
        OHLCV 数据质量检查
        
        Returns:
            {
                "passed": bool,
                "score": int,           # 0-100
                "checks": {
                    "missing_rate": {"passed": bool, "value": float, "threshold": 0.05},
                    "price_consistency": {"passed": bool, "issues": list},
                    "volume_consistency": {"passed": bool, "issues": list},
                    "timestamp_continuity": {"passed": bool, "gaps": list},
                    "adjustment_check": {"passed": bool, "anomalies": list},
                },
                "failures": list,       # 失败的检查项
            }
        """
        checks = {}
        failures = []
        
        # 1. 缺失率检查
        missing_rate = df.null_count().sum() / (len(df) * len(df.columns))
        checks["missing_rate"] = {
            "passed": missing_rate < 0.05,
            "value": missing_rate,
            "threshold": 0.05,
        }
        if missing_rate >= 0.05:
            failures.append(f"缺失率 {missing_rate:.2%} 超过阈值 5%")
        
        # 2. 价格一致性（close ≈ amount / volume）
        implied_close = df["amount"] / df["volume"]
        deviation = (df["close"] - implied_close).abs() / df["close"]
        max_deviation = deviation.max()
        checks["price_consistency"] = {
            "passed": max_deviation < 0.10,
            "value": max_deviation,
            "threshold": 0.10,
        }
        if max_deviation >= 0.10:
            failures.append(f"价格一致性偏差 {max_deviation:.2%} 超过阈值 10%")
        
        # 3. 成交量一致性
        zero_vol_with_price = ((df["volume"] == 0) & (df["close"] > 0)).sum()
        checks["volume_consistency"] = {
            "passed": zero_vol_with_price == 0,
            "issues": zero_vol_with_price,
        }
        if zero_vol_with_price > 0:
            failures.append(f"{zero_vol_with_price} 条记录成交量为0但价格非0")
        
        # 4. 时间连续性
        # TODO: 检查是否有缺失交易日
        
        # 5. 复权检查
        # TODO: 检查是否有极端跳变
        
        # 计算总分
        check_results = [c["passed"] for c in checks.values() if "passed" in c]
        score = sum(check_results) / len(check_results) * 100 if check_results else 0
        
        return {
            "passed": len(failures) == 0,
            "score": int(score),
            "checks": checks,
            "failures": failures,
        }
```

### 5.2 质量报告格式

```markdown
# 数据质量报告 — 2024-06-24

## 当日入库统计
| 数据类型 | 文件数 | 总大小 | 行数 | 平均质量分 |
|----------|--------|--------|------|-----------|
| 日 OHLCV | 1 | 12MB | 5000 | 95 |
| 资金流向 | 1 | 3MB | 5000 | 98 |
| 宏观数据 | 3 | 0.5MB | 50 | 100 |

## 质量检查详情

### 日 OHLCV
- ✅ 缺失率: 0.1% (阈值 5%)
- ✅ 价格一致性: 最大偏差 2.3% (阈值 10%)
- ✅ 成交量一致性: 无异常
- ⚠️ 时间连续性: 发现 1 个缺口 (2024-06-17 缺失，端午节休市)
- ✅ 复权检查: 无极端跳变

**综合评分: 95/100**

### 异常告警
- 🟡 000003.SZ 当日成交量为0（停牌），已标记

## 历史质量趋势
[插入质量评分 7 日趋势图]
```

---

## 六、对编程 AI 的指令

```text
1. 所有原始数据必须写入 raw/，processed/ 只存放可重新生成的数据
2. 所有数据文件使用 Parquet 格式（压缩率高、读写快）
3. 所有数据文件必须登记到 data_catalog.json
4. 质量检查不通过的进入隔离区（quarantine/），不进入主库
5. ETL 失败时，已完成的步骤不回滚，只记录失败原因
6. 特征缓存（feature_store/）使用按 symbol + date 分区
7. 数据管道日志必须记录每个 Job 的开始/结束/耗时/状态
8. 定时调度使用 cron 或 schedule 库，支持失败后重试
```

---

> 文件：DATA_PIPELINE_ETL_v1.0.md
> 生产者：Kimi（整理用户的"标准化进库流程"需求）
> 核心设计：六步进库法 + 标准化文件夹结构 + 数据质量管理
> 新增模块：DataOnboardingPipeline + DataQualityChecker + ETL Orchestrator
