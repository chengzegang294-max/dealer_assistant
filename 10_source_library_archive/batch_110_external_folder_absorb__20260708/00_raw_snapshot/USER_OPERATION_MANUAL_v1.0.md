# 用户操作手册 v1.0

> **本文档全部内容源于用户（仓库所有者）的想法，由 Kimi 整理为结构化文档供编程 AI 参考。**
> 版本：v1.0 | 状态：设计阶段 | 核心目标：定义投资管家控制台的所有操作命令和用户交互流程

---

## 一、快速入门

### 1.1 启动系统

```bash
# 方式 1：命令行启动（推荐）
cd D:\Stock\trading_assistant
venv\Scripts\activate
python -m src.governance.emperor_console

# 方式 2：快捷方式（Windows）
# 创建桌面快捷方式，目标：
# D:\Stock\trading_assistant\venv\Scripts\python.exe -m src.governance.emperor_console

# 方式 3：指定模式启动
python -m src.governance.emperor_console --mode bull    # 牛市模式
python -m src.governance.emperor_console --mode bear    # 熊市模式
```

### 1.2 首次使用

```text
首次启动后，系统会引导你完成初始化：

1. 数据配置检查
   - 系统检查 data_sources.json 是否配置
   - 如果未配置 → 提示输入 API 密钥

2. 历史数据下载
   - 询问是否下载历史数据（2018-2024）
   - 预计耗时：2-4 小时（取决于网速）
   - 可以跳过，后续再下载

3. 初始化完成
   - 系统显示主仪表盘
   - 默认模式：常态内阁模式
   - 可以开始交易
```

---

## 二、控制台命令速查

### 2.1 主命令

```text
命令格式：
  > [命令] [参数] [选项]

帮助：
  > help                  显示所有命令
  > help [command]        显示具体命令的帮助

仪表盘：
  > dashboard             显示主仪表盘（默认）
  > dashboard --refresh   强制刷新仪表盘

奏折管理：
  > memorial list         列出所有待批红奏折
  > memorial view <id>    查看奏折详情
  > memorial approve <id> [--size <pct>]  批红通过
  > memorial defer <id>   留中不发
  > memorial reject <id>  否决奏折
  > memorial approve all  批红全部（谨慎）

模式切换：
  > mode switch <mode> [--reason "..."]  切换制度模式
  > mode status           查看当前模式状态
  > mode history          查看模式切换历史
  > mode auto [--on/off]  开启/关闭自动切换

持仓管理：
  > portfolio show        显示持仓总览
  > portfolio diagnose    持仓诊断（详细分析）
  > portfolio risk        风险扫描
  > portfolio alert       查看持仓预警

报告：
  > report daily          生成今日日报
  > report weekly         生成周报（周一可用）
  > report review         系统复盘报告
  > report backtest <object_id>  单因子回测报告
  > report export <type> [--format pdf]  导出报告

系统设置：
  > setting show          显示当前设置
  > setting edit <param> <value>  修改参数
  > setting reset         恢复默认设置

对象卡管理：
  > object list           列出所有对象卡
  > object status <id>    查看对象卡状态
  > object activate <id>  激活对象卡
  > object deactivate <id> 停用对象卡
  > object test <id>      测试对象卡

紧急操作：
  > emergency liquidate   一键清仓（需确认）
  > emergency halt        暂停交易
  > emergency resume      恢复交易

退出：
  > exit                  退出控制台
  > quit                  同 exit
```

### 2.2 快捷键

```text
F1  - 批红全部待审奏折
F2  - 留中全部待审奏折
F3  - 查看选中的奏折详情
F4  - 系统复盘
F5  - 切换制度模式
F6  - 参数设置
F7  - 对象卡管理
F8  - 持仓诊断
F9  - 生成日报
F10 - 紧急菜单

Ctrl+C - 取消当前操作
Ctrl+R - 刷新仪表盘
Ctrl+L - 清屏
```

---

## 三、详细操作指南

### 3.1 批红奏折

```text
场景：内阁提交了买入奏折，你决定批准

步骤：
  1. 仪表盘显示待批红奏折列表
  2. 输入编号查看详情：
     > memorial view ZHE-001
     
  3. 查看详情后，决定批红：
     > memorial approve ZHE-001
     
  4. 或指定仓位：
     > memorial approve ZHE-001 --size 0.06
     
  5. 系统确认：
     ✅ 已批红: ZHE-001  000001.SZ  买入  6%  仓位
     📜 圣旨编号: PI-ZHE-001

注意事项：
  - 批红后交易立即执行（不可撤销）
  - 如果不确定，选择"留中"（暂不决策）
  - 批量批红（approve all）需谨慎，建议逐笔审查
```

### 3.2 切换制度模式

```text
场景：市场进入牛市，你想切换到牛市模式

步骤：
  1. 查看当前模式：
     > mode status
     
  2. 切换到牛市模式：
     > mode switch bull --reason "PeriodQueen进入ATTACK_SUSTAINED，沪深300涨2%"
     
  3. 系统确认：
     ⚠️ 确认切换到 [牛市内阁集权] 模式？
     原因: PeriodQueen进入ATTACK_SUSTAINED...
     冷却期: 3 个交易日
     [y/n] > y
     
     ✅ 已切换至 牛市内阁集权 模式
     🟢 快速通道已开启
     ⚡ Van Tharp 上限放宽至 3%
     📉 对象卡门槛降至 2 个

注意事项：
  - 切换后有 3 天冷却期，期间不能再次切换
  - 自动切换（mode auto）会在条件满足时自动切换
  - 极端情况下（危机模式），冷却期可以手动覆盖
```

### 3.3 一键清仓

```text
场景：市场暴跌，你想紧急卖出所有持仓

步骤：
  1. 按下 F10 或输入：
     > emergency liquidate
     
  2. 系统警告：
     🔴🔴🔴 紧急清仓 🔴🔴🔴
     此操作将卖出所有持仓！
     当前持仓：
       000001.SZ  6%  浮盈 +5.6%
       000002.SZ  4%  浮亏 -6.0%
       000010.SZ  5%  浮盈 +6.3%
       000100.SZ  3%  浮亏 -6.7%
     
     确认清仓？输入 yes 继续：
     > yes
     
  3. 系统执行：
     ⏳ 正在执行清仓...
     ✅ 000001.SZ 已卖出  成交价 13.18
     ✅ 000002.SZ 已卖出  成交价 23.48
     ✅ 000010.SZ 已卖出  成交价 8.48
     ✅ 000100.SZ 已卖出  成交价 28.02
     
     📊 清仓完成
     💰 回笼资金: 597 万
     📈 实现盈亏: +2.1 万

注意事项：
  - 清仓不可撤销
  - 清仓后系统自动切换为熊市监察模式
  - 建议在极端情况下使用
```

### 3.4 修改系统参数

```text
场景：你想调整 Van Tharp 风险上限

步骤：
  1. 查看当前参数：
     > setting show
     
  2. 编辑参数：
     > setting edit van_tharp_limit 0.025
     
  3. 系统确认：
     ⚠️ 修改参数 "van_tharp_limit" 从 0.02 到 0.025？
     [y/n] > y
     
     ✅ 参数已更新
     📜 旧值: 0.02  →  新值: 0.025
     ⏰ 生效时间: 立即

可修改的参数列表：
  - van_tharp_limit: Van Tharp 风险上限（默认 0.02）
  - portfolio_risk_limit: 组合风险上限（默认 0.06）
  - max_position_pct: 单票最大仓位（默认 0.15）
  - min_cash_pct: 最低现金比例（默认 0.10）
  - kelly_mode: Kelly 模式（half/conservative/aggressive）
  - entry_min_votes: 常态模式最少票数（默认 3）
  - cooldown_days: 模式切换冷却期（默认 3）
  - fast_track_max_losses: 快速通道最大失败次数（默认 3）

注意事项：
  - 修改参数后立即生效
  - 修改参数会记录到审计日志
  - 不确定时可以先用 --dry-run 预览效果
```

### 3.5 查看日报

```text
场景：你想查看今日生成的投研日报

步骤：
  1. 生成日报：
     > report daily
     
  2. 系统显示：
     📊 投资管家日报 — 2024年6月24日
     ...（日报内容）
     
  3. 导出日报：
     > report export daily --format pdf
     ✅ 日报已导出: reports/daily/2024-06-24.pdf
     
  4. 查看历史日报：
     > report list --type daily --limit 7
     
     日期          模式           总仓位   盈亏    操作
     ──────────────────────────────────────────────────
     2024-06-24  常态内阁模式     60%    +1.25%  买入2笔
     2024-06-23  常态内阁模式     55%    +0.80%  买入1笔
     ...
```

---

## 四、常见问题 FAQ

### 4.1 系统操作

Q: 系统启动后显示"数据缺失"怎么办？
A: 
  1. 检查 data_sources.json 是否配置了 API 密钥
  2. 运行手动数据同步：python scripts/daily_etl.sh
  3. 如果数据源问题，可以尝试使用备用数据源

Q: 控制台显示"对象卡降级运行"是什么意思？
A:
  - 对象卡因数据缺失或计算异常，自动进入降级模式
  - 降级模式下对象卡不生成信号或信号质量降低
  - 建议检查数据质量和对象卡日志

Q: 如何暂停自动交易？
A:
  - 输入：emergency halt
  - 或切换到"熊市监察模式"（自动禁止开新仓）
  - 或提高投票门槛：setting edit entry_min_votes 10

Q: 可以同时在多个电脑上运行吗？
A:
  - 不建议，因为数据目录可能冲突
  - 如果必须，确保使用不同的 data/ 目录
  - 或者使用网络共享存储（NAS）

### 4.2 交易相关

Q: 批红后交易多久执行？
A:
  - 批红后立即执行（模拟回测中）
  - 实际交易中取决于券商接口（未来扩展）
  - 当前版本是纯回测系统，不涉及真实交易

Q: 留中的奏折什么时候重新评估？
A:
  - 次日开盘前自动重新评估
  - 如果条件满足，会重新进入待批红列表
  - 也可以手动触发：memorial review ZHE-003

Q: 止损是自动执行的吗？
A:
  - 回测引擎中：是自动执行
  - 实际交易中：系统会提醒，但需手动确认（安全考虑）
  - 当前版本：自动执行，记录到审计日志

Q: 为什么六科封驳了我的交易？
A:
  - 常见原因：
    1. Van Tharp 风险超标（仓位太大或止损太宽）
    2. 对象卡数量不足（牛市需2个，常态需3个，熊市需5个）
    3. 组合风险超过 6% 上限
    4. 数据质量不合格
  - 查看封驳理由：memorial view ZHE-003

### 4.3 数据与报告

Q: 历史数据从哪里下载？
A:
  - 首次运行：scripts/data_sync.sh --full --start 2018-01-01
  - 日常更新：自动在收盘后执行（定时任务）
  - 手动触发：python scripts/daily_etl.sh

Q: 日报没有生成怎么办？
A:
  - 检查定时任务是否配置正确
  - 手动生成：report daily
  - 检查日志：logs/cron/daily_report.log

Q: 如何导出回测报告？
A:
  - 单因子报告：report backtest CHZL_BSD --export pdf
  - 组合报告：report backtest bundle:TrendFollowing --export pdf
  - 系统报告：report review --export pdf

Q: 数据可以备份到云盘吗？
A:
  - 可以，使用备份脚本：python scripts/backup_data.py --destination "D:/OneDrive/Backup/"
  - 支持：OneDrive / Dropbox / Google Drive（本地同步目录）
  - 注意：备份文件可能很大（50GB+）

### 4.4 故障排查

Q: 系统卡顿怎么办？
A:
  - 检查内存使用（任务管理器）
  - 清理缓存：python scripts/clear_cache.py
  - 重启控制台：exit → 重新启动

Q: 回测结果和上次不一样？
A:
  - 检查是否使用了相同的数据版本
  - 清理缓存后重新运行
  - 检查参数是否有变化

Q: 对象卡为什么一直显示"shell_only"？
A:
  - 该对象卡尚未实现或数据不足
  - 查看对象卡文档了解成熟度要求
  - 可以提供所需数据后手动激活

---

## 五、安全与权限

### 5.1 数据安全

```text
用户数据安全原则：
  - 所有数据存储在用户本地电脑
  - 不上传任何数据到第三方服务器
  - API 密钥只保存在本地 config/ 目录
  - 备份文件加密存储（可选）

建议措施：
  - 定期备份 data/ 目录到外部硬盘
  - API 密钥不要共享给他人
  - 使用强密码保护电脑
```

### 5.2 操作权限

```text
权限分级：

普通用户（默认）：
  - 查看仪表盘、报告
  - 批红/留中/否决奏折
  - 切换制度模式
  - 修改系统参数

管理员（需设置）：
  - 新增/删除对象卡
  - 修改 ETL 配置
  - 查看审计日志
  - 执行数据库维护

当前版本：只有普通用户权限，管理员功能预留
```

---

## 六、更新与升级

### 6.1 系统更新

```bash
# 更新源代码（如果有新版本）
cd D:\Stock\trading_assistant
git pull origin main

# 更新依赖
pip install -r requirements.txt --upgrade

# 重新计算特征（如果数据结构变化）
python scripts/recompute_features.py --full

# 运行测试
pytest src/tests/ --tb=short

# 重启系统
python -m src.governance.emperor_console
```

### 6.2 版本兼容性

```text
版本兼容性规则：
  - 补丁版本（v1.0.1）：直接更新，无需重新计算
  - 次要版本（v1.1.0）：可能需要重新计算特征
  - 主要版本（v2.0.0）：需要完整数据迁移

更新前检查：
  - 备份当前数据
  - 查看 CHANGELOG.md 了解更新内容
  - 在测试环境验证后再更新生产环境
```

---

## 七、联系与支持

```text
问题反馈：
  - 控制台内：输入 feedback
  - 查看日志：logs/ 目录下的相关日志文件
  - 生成诊断报告：python scripts/generate_diagnostic_report.py

诊断信息收集：
  - 运行环境（Python版本、操作系统）
  - 错误日志（最近的错误信息）
  - 系统状态（内存、磁盘、模式）
  - 数据状态（最近ETL结果、数据质量）
```

---

> 文件：USER_OPERATION_MANUAL_v1.0.md
> 生产者：Kimi（用户操作手册）
> 核心内容：控制台命令速查 + 详细操作指南 + 常见问题FAQ
> 目标：让用户在 10 分钟内学会基本操作
