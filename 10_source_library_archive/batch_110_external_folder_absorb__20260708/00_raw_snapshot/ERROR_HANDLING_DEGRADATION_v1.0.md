# 错误处理与降级策略 v1.0

> **本文档全部内容源于用户（仓库所有者）的想法，由 Kimi 整理为结构化文档供编程 AI 参考。**
> 版本：v1.0 | 状态：设计阶段 | 核心目标：定义系统在各层级失效时的降级行为，确保"不崩、不傻、不盲"

---

## 一、设计原则

```text
核心原则："不崩、不傻、不盲"

不崩：
  - 单个对象卡失效，系统继续运行
  - 数据缺失时，使用默认值或降级模式
  - 极端行情时，触发保护机制而非崩溃

不傻：
  - 降级必须有明确的信号（不能静默降级导致误判）
  - 所有降级行为记录到审计日志
  - 降级后的输出必须标记为 "degraded"

不盲：
  - 用户必须知道系统当前处于降级状态
  - 控制台显示当前有哪些模块降级
  - 降级超过阈值时，触发告警
```

---

## 二、错误分级体系

```text
┌─────────────────────────────────────────────────────────────────────┐
│                      错误分级与响应矩阵                              │
│                                                                     │
│  级别    │ 名称        │ 影响范围    │ 自动响应        │ 用户通知   │
│  ────────┼────────────┼────────────┼────────────────┼─────────── │
│  L0      │ 信息        │ 无         │ 记录日志        │ 无         │
│  L1      │ 警告        │ 单个对象卡  │ 降级运行        │ 控制台提示 │
│  L2      │ 错误        │ 单个模块    │ 跳过该模块      │ 弹窗提示   │
│  L3      │ 严重        │ 整个系统    │ 进入安全模式    │ 紧急通知   │
│  L4      │ 致命        │ 数据完整性  │ 暂停所有交易    │ 立即通知   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 三、逐层降级策略

### 3.1 数据层降级

```text
场景 1：OHLCV 数据缺失
  触发：某标的数据文件损坏或缺失
  级别：L1（警告）
  降级行为：
    1. 该标的数据标记为 "unavailable"
    2. 所有依赖该数据的对象卡输出 signal_type = "NONE"
    3. 记录缺失原因（"data_missing: daily_ohlcv_000001_sz_20240624"）
    4. 通知 ETL 管道重新拉取该数据
  恢复条件：
    - 数据重新拉取成功 → 自动恢复

场景 2：分钟级数据缺失
  触发：15min/5min 数据未加载
  级别：L0（信息）
  降级行为：
    1. 从日线合成近似分钟级数据（精度降低）
    2. 对象卡输出标记 "data_source: synthesized"
    3. 不阻断交易，但在日志中记录

场景 3：财报数据延迟
  触发：财报季某标的财报未发布
  级别：L1（警告）
  降级行为：
    1. A5 评分使用该标的上期财报
    2. 标记 "financial_data: stale"
    3. 评分降级（最高分不超过 7/10）
    4. 新财报发布后自动恢复

场景 4：宏观数据缺失
  触发：M2 数据未更新（月频，滞后）
  级别：L0（信息）
  降级行为：
    1. 使用最新可用 M2 数据
    2. MacroEnvironmentScorer 标记 "macro_data: delayed"
    3. 流动性维度评分使用替代指标（SHIBOR + 成交额）
```

### 3.2 对象卡层降级

```text
场景 5：单个对象卡计算异常
  触发：CHZL_BSD 因数据异常导致计算失败
  级别：L1（警告）
  降级行为：
    1. 该对象卡输出：
       {
         "signal_type": "NONE",
         "signal_strength": 0,
         "maturity_status": "degraded",
         "degraded_reason": "calculation_error: division_by_zero",
       }
    2. 投票时该对象卡不计入票数
    3. 控制台显示对象卡状态：🟡 degraded
    4. 记录异常堆栈到日志
  恢复条件：
    - 下一周期计算成功 → 自动恢复

场景 6：对象卡数据不足（未来桶）
  触发：INSTB 需要 Level-2 数据但未提供
  级别：L1（警告）
  降级行为：
    1. 该对象卡被标记为 "needs_extra_data"
    2. 不参与投票（默认不激活）
    3. 控制台显示：🔶 等待数据
  恢复条件：
    - 用户提供 Level-2 数据 → 手动激活

场景 7：对象卡互锁冲突
  触发：CHZL_BSD 和 KD MTF 同时发出反向信号
  级别：L1（警告）
  降级行为：
    1. 两者信号都标记为 "conflicted"
    2. 该标的进入 "观察模式"（不交易）
    3. 触发 "内阁会议"（如果启用明朝内阁模式）
    4. 记录冲突到审计日志

场景 8：对象卡参数漂移
  触发：连续 10 笔交易该对象卡的胜率 < 30%
  级别：L2（错误）
  降级行为：
    1. 该对象卡自动降级为 "shell_only"
    2. 不再参与投票
    3. 触发 "系统复盘"，建议用户审查
    4. 记录到 "对象卡失效库"
```

### 3.3 投票层降级

```text
场景 9：投票不足
  触发：激活对象卡数量 < entry_min_votes
  级别：L1（警告）
  降级行为：
    1. VoteDecisionEngine 输出：ABORT
    2. abort_reason = "votes_insufficient"
    3. 建议用户检查对象卡激活状态
    4. 不执行交易

场景 10：投票全通过但风险超标
  触发：Van Tharp 检查失败
  级别：L2（错误）
  降级行为：
    1. RiskArchitectureEngine 否决交易
    2. 输出：ABORT, abort_reason = "van_tharp_limit"
    3. 建议降低仓位或扩大止损
    4. 不执行交易

场景 11：PeriodQueen 禁止交易
  触发：PQ 状态 = HALT 或 EXTREME_VOL
  级别：L2（错误）
  降级行为：
    1. 所有交易申请自动 ABORT
    2. abort_reason = "period_queen_halt"
    3. 系统自动切换为 "熊市监察模式"
    4. 控制台显示：🔴 交易暂停
```

### 3.4 治理层降级

```text
场景 12：制度模式切换失败
  触发：自动切换条件满足但冷却期未过
  级别：L1（警告）
  降级行为：
    1. 维持当前模式
    2. 记录 "mode_switch_deferred: cooldown_active"
    3. 控制台显示：⏳ 冷却期剩余 X 天
    4. 用户可手动覆盖（需确认）

场景 13：六科审查系统故障
  触发：六科中的某一科计算异常
  级别：L2（错误）
  降级行为：
    1. 故障科标记为 "degraded"
    2. 使用简化审查（只检查 Van Tharp）
    3. 控制台显示：⚠️ 六科审查简化中
    4. 记录故障原因

场景 14：控制台无响应
  触发：用户无法操作控制台
  级别：L3（严重）
  降级行为：
    1. 系统进入 "自动模式"
    2. 使用默认参数继续运行
    3. 所有交易自动批红（信任模式）
    4. 发送紧急通知到用户备用渠道
```

### 3.5 系统层降级

```text
场景 15：回测引擎崩溃
  触发：回测过程中内存溢出
  级别：L3（严重）
  降级行为：
    1. 保存当前回测状态（checkpoint）
    2. 释放内存，清理临时数据
    3. 使用更小股票池重新启动回测
    4. 通知用户回测失败及原因

场景 16：Feature Store 损坏
  触发：特征缓存文件损坏
  级别：L2（错误）
  降级行为：
    1. 删除损坏的缓存文件
    2. 从 raw 数据重新计算特征
    3. 标记为 "rebuild_in_progress"
    4. 计算完成后恢复

场景 17：数据管道完全失效
  触发：所有数据源无法连接
  级别：L4（致命）
  降级行为：
    1. 系统进入 "离线模式"
    2. 使用最后可用数据运行（最多延迟 3 天）
    3. 所有对象卡标记为 "stale_data"
    4. 暂停所有新交易，只管理已有持仓
    5. 每小时尝试重连数据源
    6. 连续 24 小时无法恢复 → 发送紧急通知
```

---

## 四、降级状态机

```python
class DegradationStateMachine:
    """
    降级状态机
    
    每个模块独立维护自己的降级状态
    """
    
    STATES = {
        "normal": "正常运行",
        "degraded": "降级运行",
        "bypassed": "已跳过",
        "halted": "已暂停",
        "offline": "离线模式",
    }
    
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.state = "normal"
        self.degradation_history = []
        self.recovery_attempts = 0
    
    def degrade(self, reason: str, level: str = "L1") -> None:
        """触发降级"""
        old_state = self.state
        
        if level == "L1":
            self.state = "degraded"
        elif level == "L2":
            self.state = "bypassed"
        elif level == "L3":
            self.state = "halted"
        elif level == "L4":
            self.state = "offline"
        
        self.degradation_history.append({
            "timestamp": datetime.now().isoformat(),
            "from": old_state,
            "to": self.state,
            "reason": reason,
            "level": level,
        })
        
        # 记录审计日志
        audit_log.warning(
            f"模块 {self.module_name} 降级: {old_state} -> {self.state}, 原因: {reason}"
        )
    
    def recover(self) -> bool:
        """尝试恢复"""
        if self.state == "normal":
            return True
        
        self.recovery_attempts += 1
        
        # 模拟恢复检查
        recovery_success = self._check_recovery()
        
        if recovery_success:
            old_state = self.state
            self.state = "normal"
            self.recovery_attempts = 0
            
            audit_log.info(
                f"模块 {self.module_name} 恢复: {old_state} -> normal"
            )
            return True
        else:
            audit_log.warning(
                f"模块 {self.module_name} 恢复失败（第 {self.recovery_attempts} 次尝试）"
            )
            return False
    
    def _check_recovery(self) -> bool:
        """检查是否可以恢复"""
        # 子类实现具体的恢复检查逻辑
        return True
    
    def is_operational(self) -> bool:
        """检查是否可操作"""
        return self.state in ["normal", "degraded"]
    
    def get_status(self) -> dict:
        """获取当前状态"""
        return {
            "module": self.module_name,
            "state": self.state,
            "description": self.STATES[self.state],
            "history": self.degradation_history[-5:],  # 最近 5 条
            "recovery_attempts": self.recovery_attempts,
        }
```

---

## 五、全局降级协调器

```python
class GlobalDegradationCoordinator:
    """
    全局降级协调器
    
    职责：
    1. 监控所有模块的降级状态
    2. 当多个模块同时降级时，触发全局响应
    3. 向用户报告当前系统健康度
    """
    
    def __init__(self):
        self.modules: dict[str, DegradationStateMachine] = {}
        self.global_health_score = 100  # 0-100
    
    def register_module(self, name: str, dsm: DegradationStateMachine) -> None:
        """注册模块"""
        self.modules[name] = dsm
    
    def update_health_score(self) -> None:
        """更新全局健康度"""
        total_modules = len(self.modules)
        if total_modules == 0:
            self.global_health_score = 100
            return
        
        normal_count = sum(1 for m in self.modules.values() if m.state == "normal")
        self.global_health_score = int(normal_count / total_modules * 100)
    
    def get_system_status(self) -> dict:
        """获取系统整体状态"""
        self.update_health_score()
        
        degraded_modules = [
            name for name, dsm in self.modules.items()
            if dsm.state != "normal"
        ]
        
        return {
            "global_health_score": self.global_health_score,
            "total_modules": len(self.modules),
            "normal_modules": len(self.modules) - len(degraded_modules),
            "degraded_modules": degraded_modules,
            "module_details": {
                name: dsm.get_status()
                for name, dsm in self.modules.items()
            },
            "recommendation": self._get_recommendation(),
        }
    
    def _get_recommendation(self) -> str:
        """生成系统建议"""
        if self.global_health_score >= 90:
            return "系统健康，正常运行"
        elif self.global_health_score >= 70:
            return f"系统轻度降级（{self.global_health_score}%），建议关注降级模块"
        elif self.global_health_score >= 50:
            return f"系统中度降级（{self.global_health_score}%），建议审查并修复"
        else:
            return f"系统严重降级（{self.global_health_score}%），建议暂停交易并排查"
```

---

## 六、用户通知规范

```text
降级通知分级：

🟢 信息级（L0）：
  - 通知方式：仅日志记录
  - 示例："15min 数据使用日线合成"
  - 用户不感知

🟡 警告级（L1）：
  - 通知方式：控制台状态栏更新
  - 示例："CHZL_BSD 降级运行：数据缺失"
  - 用户看到黄色标记，但不弹窗

🟠 错误级（L2）：
  - 通知方式：控制台弹窗 + 日志
  - 示例："六科审查简化中：工科计算异常"
  - 用户看到弹窗，但系统继续运行

🔴 严重级（L3）：
  - 通知方式：控制台弹窗 + 声音 + 邮件
  - 示例："系统进入安全模式：回测引擎崩溃"
  - 用户必须确认

⚫ 致命级（L4）：
  - 通知方式：全屏告警 + 声音 + 短信/电话（未来）
  - 示例："数据管道完全失效，系统离线"
  - 用户必须立即处理
```

---

## 七、降级恢复测试

```text
测试要求：

1. 单元测试：
   - 每个对象卡必须测试"数据缺失"场景
   - 每个对象卡必须测试"计算异常"场景
   - 验证降级输出是否符合规范

2. 集成测试：
   - 模拟数据源断开 → 验证系统进入离线模式
   - 模拟内存溢出 → 验证回测引擎降级
   - 模拟对象卡互锁冲突 → 验证观察模式

3. 混沌测试（Chaos Engineering）：
   - 随机删除 raw/ 中的数据文件
   - 随机注入异常值到 OHLCV
   - 随机延迟数据到达时间
   - 验证系统是否能优雅降级

4. 恢复测试：
   - 降级后恢复数据源 → 验证自动恢复
   - 降级后手动修复 → 验证手动恢复
```

---

## 八、对编程 AI 的指令

```text
1. 每个模块必须实现 DegradationStateMachine
2. 所有降级行为必须记录审计日志
3. 降级输出必须包含 "degraded_reason" 字段
4. 不允许静默降级（必须有日志或通知）
5. 恢复机制必须自动尝试（至少 3 次）
6. 控制台必须显示全局健康度评分
7. 降级超过 24 小时必须触发告警
8. 单元测试必须覆盖降级场景
```

---

> 文件：ERROR_HANDLING_DEGRADATION_v1.0.md
> 生产者：Kimi（系统鲁棒性设计）
> 核心设计：五级错误分级 + 逐层降级策略 + 全局协调器
> 目标：确保系统在极端情况下"不崩、不傻、不盲"
