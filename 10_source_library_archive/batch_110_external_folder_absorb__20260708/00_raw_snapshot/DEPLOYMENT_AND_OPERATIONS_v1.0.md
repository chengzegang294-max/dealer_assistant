# 部署与运维文档 v1.0

> **本文档全部内容源于用户（仓库所有者）的想法，由 Kimi 整理为结构化文档供编程 AI 参考。**
> 版本：v1.0 | 状态：设计阶段 | 核心目标：定义系统部署、日常运维、监控告警的规范

---

## 一、部署架构

### 1.1 单机部署模式（默认）

```text
┌─────────────────────────────────────────────────────────────────────┐
│                        单机部署架构                                  │
│                                                                     │
│  ┌─────────────┐                                                    │
│  │  用户电脑    │                                                    │
│  │  Windows 10 │                                                    │
│  │  16GB RAM   │                                                    │
│  │  SSD 500GB  │                                                    │
│  └──────┬──────┘                                                    │
│         │                                                           │
│         ▼                                                           │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     Python 3.10 + venv                        │   │
│  │                                                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │   │
│  │  │ 控制台   │  │ 回测引擎 │  │ 数据管道 │  │ 日报生成 │    │   │
│  │  │ (主进程) │  │ (子进程) │  │ (定时)  │  │ (定时)  │    │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │   │
│  │                                                             │   │
│  │  数据存储：                                                   │   │
│  │  ├─ 内存：日 OHLCV（500MB）                                   │   │
│  │  ├─ SSD：Feature Store + raw data（~50GB）                 │   │
│  │  └─ 日志：logs/（每日轮转，保留30天）                         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  数据源：                                                            │
│  ├─ tushare（在线 API）                                             │
│  ├─ akshare（在线 API）                                             │
│  ├─ Wind（本地终端，用户已有）                                       │
│  └─ 手动上传（财报/政策文件）                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

部署目标：
  - 单台 Windows 电脑即可运行
  - 不需要 Docker / Kubernetes / 云服务器
  - 用户数据完全本地存储
  - 数据源按需在线拉取
```

### 1.2 最小系统要求

```text
硬件要求：
  - CPU：Intel i5 / AMD Ryzen 5 及以上（支持多核）
  - 内存：16 GB（推荐 32 GB）
  - 磁盘：SSD 500 GB（数据增长后需扩展）
  - 网络：稳定互联网（用于数据拉取）

软件要求：
  - 操作系统：Windows 10/11（64位）或 macOS 12+
  - Python：3.10 或 3.11（不支持 3.12，部分库未兼容）
  - Git：2.30+（版本控制）
  - 可选：Git Bash（命令行工具）

Python 依赖：
  - polars >= 0.20
  - pandas >= 2.0（兼容用）
  - numpy >= 1.24
  - tushare >= 1.3
  - akshare >= 1.12
  - pytest >= 7.0
  - pyyaml >= 6.0
  - 完整依赖列表见 requirements.txt
```

---

## 二、安装指南

### 2.1 首次安装

```bash
# Step 1: 克隆仓库（或复制到本地）
cd D:\Stock
git clone https://github.com/user/trading_assistant.git
# 或手动复制文件夹

cd trading_assistant

# Step 2: 创建虚拟环境
python -m venv venv

# Step 3: 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Step 4: 安装依赖
pip install -r requirements.txt

# Step 5: 验证安装
python -c "import polars; print(f'polars version: {polars.__version__}')"
python -c "import tushare; print('tushare OK')"
python -c "import akshare; print('akshare OK')"

# Step 6: 配置数据源（API 密钥）
copy config\data_sources.template.json config\data_sources.json
# 编辑 config\data_sources.json，填入你的 API 密钥

# Step 7: 初始化数据目录
python scripts\init_data_dirs.py

# Step 8: 运行首次数据同步（下载历史数据）
python scripts\data_sync.sh --full --start 2018-01-01

# Step 9: 运行测试
pytest src/tests/ --tb=short

# Step 10: 启动控制台
python -m src.governance.emperor_console
```

### 2.2 配置文件模板

```json
// config/data_sources.json（用户需填写）
{
  "tushare": {
    "token": "YOUR_TUSHARE_TOKEN_HERE",
    "enabled": true,
    "rate_limit": "200/min"
  },
  "akshare": {
    "enabled": true,
    "rate_limit": "unlimited"
  },
  "wind": {
    "enabled": true,
    "path": "C:/Wind/Wind.Net.Client/wind",
    "note": "需要安装 Wind 终端并登录"
  },
  "manual_upload": {
    "enabled": true,
    "path": "data/manual/"
  }
}
```

```yaml
# config/backtest_config.yaml
backtest:
  initial_capital: 10_000_000  # 初始资金 1000 万
  commission_rate: 0.0003      # 佣金 0.3‰
  slippage_rate: 0.0001        # 滑点 0.1‰
  
data:
  start_date: "2018-01-01"
  end_date: "2024-12-31"
  stock_pool: "all_a_share"    # all_a_share / hs300 / zz500 / custom
  
execution:
  mode: "event_driven"         # event_driven / vectorized / hybrid
  
logging:
  level: "INFO"               # DEBUG / INFO / WARNING / ERROR
  file: "logs/backtest/backtest.log"
  max_size: "100MB"
  backup_count: 10
```

---

## 三、日常运维流程

### 3.1 每日收盘后运维

```bash
# 1. 数据同步（15:30 自动触发，或手动执行）
python scripts/daily_etl.sh

# 内部流程：
#   a) 拉取当日日 OHLCV
#   b) 拉取资金流向
#   c) 拉取宏观数据
#   d) 质量检查
#   e) 更新 Feature Store
#   f) 生成日报

# 2. 检查日报（17:00 生成）
cat reports/daily/$(date +%Y-%m-%d).md

# 3. 检查日志（确认无错误）
tail -n 50 logs/data_pipeline/etl_$(date +%Y%m%d).log

# 4. 检查数据质量
python scripts/check_data_quality.py --date $(date +%Y-%m-%d)
```

### 3.2 每周运维

```bash
# 周一：周报生成（自动在日报中包含）
# 检查内容：
#   - 上周绩效回顾
#   - 对象卡贡献度变化
#   - 系统偏差分析

# 周五：数据备份
python scripts/backup_data.py
# 备份内容：
#   - data/raw/（增量）
#   - data/processed/feature_store/（增量）
#   - logs/（压缩）
#   - config/（全量）
# 备份路径：backup/weekly/YYYY-MM-DD/
```

### 3.3 每月运维

```bash
# 月初：日志清理
python scripts/rotate_logs.py --keep 30
# 保留 30 天日志，删除更早的

# 月中：数据归档
python scripts/archive_data.py --older-than 90
# 90 天前的数据归档到 data/archive/

# 月末：性能检查
python scripts/performance_report.py
# 检查：
#   - 数据加载速度是否退化
#   - 特征计算速度是否退化
#   - 回测速度是否退化
#   - 内存使用是否异常
```

### 3.4 财报季运维

```bash
# 4月/8月/10月：财报同步
python scripts/sync_financial_reports.py --quarter Q1
# 自动：
#   - 拉取最新财报
#   - 运行 A5 基本面选股
#   - 更新候选池
#   - 通知用户
```

---

## 四、定时任务（Cron）

### 4.1 Windows 任务计划程序

```powershell
# 创建每日数据同步任务（Windows Task Scheduler）
# 使用 PowerShell 脚本

$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File D:\Stock\trading_assistant\scripts\daily_etl.ps1"
$Trigger = New-ScheduledTaskTrigger -Daily -At 3:30pm
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd
$Principal = New-ScheduledTaskPrincipal -UserId "USER" -LogonType Interactive

Register-ScheduledTask -TaskName "TradingAssistant_DailyETL" `
    -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal

# 创建日报生成任务
$Action2 = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File D:\Stock\trading_assistant\scripts\generate_daily_report.ps1"
$Trigger2 = New-ScheduledTaskTrigger -Daily -At 5:00pm

Register-ScheduledTask -TaskName "TradingAssistant_DailyReport" `
    -Action $Action2 -Trigger $Trigger2 -Settings $Settings -Principal $Principal
```

### 4.2 Cron 表达式（Linux/macOS）

```bash
# 编辑 crontab
crontab -e

# 添加以下行：
# 每日 15:30 数据同步
30 15 * * * cd /path/to/trading_assistant && venv/bin/python scripts/daily_etl.py >> logs/cron/daily_etl.log 2>&1

# 每日 17:00 生成日报
0 17 * * * cd /path/to/trading_assistant && venv/bin/python scripts/generate_daily_report.py >> logs/cron/daily_report.log 2>&1

# 每周五 18:00 数据备份
0 18 * * 5 cd /path/to/trading_assistant && venv/bin/python scripts/backup_data.py >> logs/cron/weekly_backup.log 2>&1

# 每月 1 日 02:00 日志清理
0 2 1 * * cd /path/to/trading_assistant && venv/bin/python scripts/rotate_logs.py >> logs/cron/monthly_cleanup.log 2>&1
```

---

## 五、监控与告警

### 5.1 日志监控

```python
# scripts/log_monitor.py
import os
import re
from datetime import datetime, timedelta

class LogMonitor:
    """日志监控器"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self.alert_keywords = [
            "ERROR", "CRITICAL", "FATAL",
            "exception", "traceback",
            "data_quality_failed",
            "etl_failed",
        ]
    
    def scan_recent_logs(self, minutes: int = 60) -> list[dict]:
        """扫描最近日志中的告警"""
        alerts = []
        cutoff = datetime.now() - timedelta(minutes=minutes)
        
        for root, _, files in os.walk(self.log_dir):
            for file in files:
                if not file.endswith(".log"):
                    continue
                
                filepath = os.path.join(root, file)
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                if mtime < cutoff:
                    continue
                
                with open(filepath, "r", encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        for keyword in self.alert_keywords:
                            if keyword in line:
                                alerts.append({
                                    "file": filepath,
                                    "line": line_num,
                                    "keyword": keyword,
                                    "content": line.strip(),
                                    "time": mtime,
                                })
        
        return alerts
    
    def check_disk_space(self, threshold: float = 0.85) -> dict:
        """检查磁盘空间"""
        import shutil
        
        total, used, free = shutil.disk_usage(".")
        usage_ratio = used / total
        
        return {
            "total_gb": total / (1024**3),
            "used_gb": used / (1024**3),
            "free_gb": free / (1024**3),
            "usage_ratio": usage_ratio,
            "alert": usage_ratio > threshold,
        }
    
    def check_memory(self, threshold: float = 0.90) -> dict:
        """检查内存使用"""
        import psutil
        
        mem = psutil.virtual_memory()
        
        return {
            "total_gb": mem.total / (1024**3),
            "used_gb": mem.used / (1024**3),
            "available_gb": mem.available / (1024**3),
            "usage_ratio": mem.percent / 100,
            "alert": mem.percent / 100 > threshold,
        }
    
    def run_health_check(self) -> dict:
        """运行健康检查"""
        return {
            "timestamp": datetime.now().isoformat(),
            "log_alerts": self.scan_recent_logs(),
            "disk": self.check_disk_space(),
            "memory": self.check_memory(),
            "overall_healthy": True,  # 综合判断
        }
```

### 5.2 告警规则

```text
告警分级：

🔴 紧急告警（立即通知）
  - 触发条件：
    - ETL 连续失败 3 次
    - 磁盘空间 < 10%
    - 内存使用 > 95%
    - 回测引擎崩溃
    - 数据管道完全失效
  - 通知方式：
    - 控制台弹窗
    - 日志标记 [EMERGENCY]
    - 发送到用户指定渠道（飞书/邮件）

🟡 警告告警（每日汇总）
  - 触发条件：
    - ETL 单次失败但已恢复
    - 磁盘空间 < 20%
    - 内存使用 > 80%
    - 数据质量评分 < 90
    - 对象卡降级运行
  - 通知方式：
    - 日报中包含警告摘要
    - 控制台状态栏标记

🟢 信息通知（仅日志）
  - 触发条件：
    - 日常 ETL 成功完成
    - 日报生成成功
    - 数据备份完成
  - 通知方式：
    - 仅记录日志
    - 不通知用户
```

---

## 六、日志轮转

### 6.1 日志结构

```
logs/
├── backtest/                  # 回测日志
│   ├── backtest_20240601.log
│   ├── backtest_20240602.log
│   └── ...
│
├── data_pipeline/             # 数据管道日志
│   ├── etl_20240601.log
│   ├── etl_20240602.log
│   └── ...
│
├── governance/                # 治理审计日志
│   ├── audit_20240601.jsonl
│   ├── audit_20240602.jsonl
│   └── ...
│
├── risk_audit/                # 风控审计日志
│   ├── risk_20240601.jsonl
│   └── ...
│
├── cron/                      # 定时任务日志
│   ├── daily_etl.log
│   ├── daily_report.log
│   └── ...
│
└── system/                    # 系统日志
    ├── health_check.log
    └── performance.log
```

### 6.2 轮转策略

```python
# scripts/rotate_logs.py
import os
import gzip
import shutil
from datetime import datetime, timedelta
from pathlib import Path

class LogRotator:
    """日志轮转器"""
    
    def __init__(self, log_dir: str = "logs", keep_days: int = 30):
        self.log_dir = log_dir
        self.keep_days = keep_days
    
    def rotate(self):
        """执行日志轮转"""
        cutoff = datetime.now() - timedelta(days=self.keep_days)
        
        for root, _, files in os.walk(self.log_dir):
            for file in files:
                if not file.endswith(".log"):
                    continue
                
                filepath = Path(root) / file
                mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
                
                if mtime < cutoff:
                    # 压缩旧日志
                    self._compress(filepath)
                    # 删除原文件
                    filepath.unlink()
        
        # 清理 90 天前的压缩日志
        self._cleanup_archives(cutoff - timedelta(days=60))
    
    def _compress(self, filepath: Path):
        """压缩日志文件"""
        archive_path = filepath.with_suffix(".log.gz")
        
        with open(filepath, "rb") as f_in:
            with gzip.open(archive_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
    
    def _cleanup_archives(self, cutoff: datetime):
        """清理归档日志"""
        for root, _, files in os.walk(self.log_dir):
            for file in files:
                if not file.endswith(".log.gz"):
                    continue
                
                filepath = Path(root) / file
                mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
                
                if mtime < cutoff:
                    filepath.unlink()
```

---

## 七、数据备份与恢复

### 7.1 备份策略

```text
备份层级：

Level 1：每日增量备份
  - 内容：当日新数据（raw/ + processed/ 增量）
  - 频率：每日收盘后
  - 保留：7 天
  - 路径：backup/daily/YYYY-MM-DD/

Level 2：每周全量备份
  - 内容：完整 data/ 目录 + config/ 目录
  - 频率：每周五
  - 保留：4 周
  - 路径：backup/weekly/YYYY-MM-DD/

Level 3：每月归档备份
  - 内容：完整仓库（data/ + src/ + config/ + docs/）
  - 频率：每月 1 日
  - 保留：12 个月
  - 路径：backup/monthly/YYYY-MM/
  - 存储：外部硬盘 / 云盘（可选）

备份命令：
  python scripts/backup_data.py --level weekly --destination D:/Backup/
```

### 7.2 恢复流程

```bash
# 数据恢复流程
# 场景：误删除数据或硬盘损坏

# Step 1: 确认最新可用备份
ls -la backup/weekly/ | tail -5

# Step 2: 停止所有运行中的进程
# 关闭控制台
# 关闭回测引擎

# Step 3: 恢复数据
python scripts/restore_data.py --source backup/weekly/2024-06-21/ --target data/

# Step 4: 验证数据完整性
python scripts/check_data_integrity.py

# Step 5: 重新计算特征（如果 processed/ 被删除）
python scripts/recompute_features.py --start 2024-06-01

# Step 6: 重启系统
python -m src.governance.emperor_console
```

---

## 八、故障排查指南

### 8.1 常见问题

```text
问题 1：ETL 失败
  症状：每日数据同步未执行
  检查：
    1. logs/data_pipeline/etl_YYYYMMDD.log 查看错误信息
    2. 检查 API 密钥是否过期（tushare/akshare）
    3. 检查网络连接
  解决：
    1. 手动运行：python scripts/daily_etl.sh
    2. 更新 API 密钥
    3. 如果是数据源问题，使用备用数据源

问题 2：内存不足
  症状：系统卡顿或崩溃
  检查：
    1. 任务管理器查看内存使用
    2. logs/system/performance.log 查看内存趋势
  解决：
    1. 减少常驻内存数据量（config/backtest_config.yaml 中调整）
    2. 增加虚拟内存（Windows 页面文件）
    3. 关闭不必要的进程

问题 3：对象卡计算错误
  症状：某对象卡持续输出 NONE
  检查：
    1. logs/backtest/ 查看对象卡错误日志
    2. 检查输入数据是否有异常值
  解决：
    1. 重启对象卡（控制台中停用再激活）
    2. 检查数据质量
    3. 如果问题持续，标记为 degraded

问题 4：回测结果不一致
  症状：同一策略两次回测结果不同
  检查：
    1. 确认使用相同的数据版本
    2. 检查随机种子是否固定
    3. 检查是否有缓存污染
  解决：
    1. 清理缓存：python scripts/clear_cache.py
    2. 重新运行回测
    3. 对比两次回测的审计日志

问题 5：控制台无响应
  症状：控制台界面卡住
  检查：
    1. 检查是否有大量数据处理任务在后台运行
    2. 检查日志是否有异常
  解决：
    1. Ctrl+C 退出控制台
    2. 检查是否有僵尸进程
    3. 重新启动控制台
```

---

## 九、对编程 AI 的指令

```text
1. 部署脚本必须使用跨平台兼容的代码（Windows/Linux/macOS）
2. 所有运维脚本必须有 --dry-run 选项（模拟执行，不实际修改）
3. 备份脚本必须验证备份完整性（SHA256 校验）
4. 日志轮转必须保留至少 30 天
5. 告警通知必须有降级机制（如果飞书失败，尝试邮件）
6. 健康检查必须每日自动运行，结果写入日志
7. 所有运维操作必须记录审计日志（who/what/when）
8. 恢复流程必须有明确的 Step-by-Step 文档
```

---

> 文件：DEPLOYMENT_AND_OPERATIONS_v1.0.md
> 生产者：Kimi（运维运维设计）
> 核心设计：单机部署 + 定时任务 + 日志轮转 + 三级备份
> 部署目标：Windows 单台电脑，用户数据完全本地存储
