# 开发者交接手册 — 对象卡量化交易系统

> **版本**: v1.0  
> **日期**: 2026-07-07  
> **作者**: 当前AI助手 → 下一任编程AI  
> **仓库路径**: `E:\downloads\Desktop\找系统\特征`  
> **总文件数**: 110+ 文件（88个 .md + 22个 .py）

---

## 一、项目愿景（这是我们在做什么）

**目标**: 构建一个针对A股纯多头的量化交易系统，核心特点是**对象化信号卡片**（Object Cards）+ **投票聚合决策**。

**关键原则**（不可违背）：
1. **拒绝大而全的评分系统** — 坚持最小代理与候选池过滤
2. **保守量化标注** — 只有常规A股数据可直接落地的条目保留 `proxy_quantizable_now`，依赖Level-2/龙虎榜/NLP/另类数据的条目降级为 `needs_extra_data`/`future_bucket`/`shell_only`
3. **哲学/心法/直觉类内容归为 `NOT_QUANT_YET`** — 拒绝强行公式化
4. **回测诚实性** — 任何策略上线前必须通过 CSCV-PBO 检验（PBO<50%为硬门槛）
5. **A股约束** — T+1、涨跌停、纯多头、无做空

**三层决策架构**（已冻结，不可改动）：

```
Layer 1: PeriodQueen (环境识别层) — 决定当前市场状态，输出权限
    ↓
Layer 2: StrategyBundles (策略选择层) — 根据状态选择激活哪些对象卡
    ↓
Layer 3: Vote + Risk (执行管理层) — 对象卡投票聚合 + 风控 + 仓位管理
```

---

## 二、系统架构（五层端到端链路）

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 0: 数据管道 (Data Pipeline)                          │
│  - SimulatedDataSource / AkShare / Tushare 三源切换          │
│  - 远程环境AkShare可能被防火墙拦截，自动fallback到模拟数据     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: 环境识别 (PeriodQueen) — 系统心脏                 │
│  - 七态状态机: ATTACK_SUSTAINED / ATTACK_INITIAL /           │
│    CONSOLIDATION / POWER_TRANSITION / CUTTING_START /        │
│    CUTTING_COMPLETE / EXTREME_VOL                            │
│  - 输出: TradingPermission (FULL/REDUCED/EXIT_ONLY/HALT)    │
│  - 所有执行层对象卡的权限/仓位上限/投票门槛由此决定            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: 对象卡信号生成 (Object Cards) — 12张可运行卡片      │
│  - 每张卡片是一个独立模块，有统一输入/输出接口                  │
│  - 环境层 P0_F × 执行层 P0_E × A股因子 P0_A × 风控 P0_R      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: 投票聚合 + 风控 (Vote & Risk)                      │
│  - 加权投票: signal_strength × confidence                   │
│  - 权限检查: PERIOD_QUEEN 状态决定 BUY/SELL 是否有效         │
│  - 阻塞过滤: filter_action=BLOCK 的对象卡一票否决            │
│  - 仓位管理: VOLTARGET × KELLY 融合输出最终 size_scalar     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 4: 执行层 (Execution) — 信号到实盘/回测                │
│  - 回测框架 (待实现): CSCV-PBO 诚实性检验                    │
│  - 控制台: prototype_console_v2.py 五态面板 + 事件流           │
└─────────────────────────────────────────────────────────────┘
```

---

## 三、对象卡接口规范（这是核心契约）

### 3.1 输入: `RawInput`（每类对象卡有自己的Input结构）

所有执行层对象卡至少接收 OHLCV 数据。A股特殊因子卡额外接收资金流向/龙虎榜等数据。

### 3.2 输出: `ObjectCardOutput`（8个标准字段，**必须严格遵守**）

```python
@dataclass
class ObjectCardOutput:
    object_id: str          # 格式: {NAME}_{P0_X}，如 "CHZL_BSD_P0_E"
    signal_type: str        # "BUY" | "SELL" | "NEUTRAL" | "VOL_ADJUST" | "POSITION_SIZE" | 状态机枚举
    signal_strength: float  # 范围: -2.0 ~ +2.0（BUY为正，SELL为负，NEUTRAL=0）
    confidence: float       # 范围: 0.0 ~ 1.0
    lock_status: str        # "LOCKED" | "UNLOCKED"
    filter_action: str      # "PASS" | "BLOCK" | "REVIEW"
    risk_action: str        # "NORMAL" | "DOWNSIZE" | "HALT" | "SCALE_POSITION" | 权限字符串
    size_scalar: float      # 仓位缩放系数: 0.0 ~ 2.0
    detail: Dict            # 诊断信息，用于日志和调试
```

### 3.3 信号强度约定（非常重要，确保聚合时一致性）

| signal_type | signal_strength | 含义 |
|-------------|-----------------|------|
| BUY | 0.5 ~ 2.0 | 多头信号，数值越大越强 |
| SELL | -0.5 ~ -2.0 | 空头/回避信号（A股纯多头下SELL通常降级为HOLD/NEUTRAL） |
| NEUTRAL | 0.0 | 无信号 |
| VOL_ADJUST | 0.1 ~ 2.0 | 波动率目标输出的仓位系数 |
| POSITION_SIZE | 0.0 ~ 1.0 | 凯利公式输出的仓位比例 |

**⚠️ 注意**: 有些旧版对象卡可能使用了 0-10 范围，统一收口时必须映射到上述标准。

---

## 四、文件清单（按功能分类）

### 4.1 核心对象卡规范（12张 .md）

| 文件 | 对象ID | 用途 | 优先级 |
|------|--------|------|--------|
| `OBJECT_CARD_PERIOD_QUEEN_P0_F__CycleStateSystem_v1.0.md` | PERIOD_QUEEN_P0_F | 七态周期识别，系统心脏 | 最高 |
| `OBJECT_CARD_VOLFAC_P0_A__VolatilityFactor_v1.0.md` | VOLFAC_P0_A | 波动率因子 | 高 |
| `OBJECT_CARD_VOLTARGET_P0_R__VolatilityTargeting_v1.0.md` | VOLTARGET_P0_R | 波动率目标仓位 | 高 |
| `OBJECT_CARD_CHZL_BSD_P0_E__Chanlun_Buy_Sell_Signals_v1.0.md` | CHZL_BSD_P0_E | 缠论分型/笔/中枢 | 中 |
| `OBJECT_CARD_BPB_P0_E__Brooks_Breakout_Pullback_v1.0.md` | BPB_P0_E | 突破回调质量 | 中 |
| `OBJECT_CARD_TKR7_P0_E__AO_Divergence_v1.0.md` | TKR7_P0_E | AO背离 | 中 |
| `OBJECT_CARD_MFLOW_P0_A__MoneyFlow_v1.0.md` | MFLOW_P0_A | 资金流向 | 中 |
| `OBJECT_CARD_INSTB_P0_A__InstitutionalBehavior_v1.0.md` | INSTB_P0_A | 机构行为 | 中 |
| `OBJECT_CARD_KELLY_P0_R__KellyCriterion_v1.0.md` | KELLY_P0_R | 半凯利仓位 | 中 |
| `OBJECT_CARD_VP_P0_E__VolumeProfile_v1.0.md` | VP_P0_E | 成交量分布 | 中 |
| `OBJECT_CARD_YTC_P0_E__YTC_Microstructure_v1.0.md` | YTC_P0_E | YTC微观结构 | 中 |
| `OBJECT_CARD_ATRATIO_P0_A__ActiveTradeRatio_v1.0.md` | ATRATIO_P0_A | 活跃度比率 | 低 |

**命名规范**: `OBJECT_CARD_{OBJECT_ID}__{Description}_v{version}.md`

**对象ID编码规则**:
- `P0_F` — Environment/Filter（环境识别层）
- `P0_E` — Execution（纯技术执行层）
- `P0_A` — A-share special（A股特殊因子）
- `P0_R` — Risk（风控层）

### 4.2 可运行Python代码（核心实现）

| 文件 | 用途 | 依赖 | 状态 |
|------|------|------|------|
| `object_card_registry.py` | ⭐ **统一调度器** — 输入股票代码，跑完全部12张卡，输出聚合信号 | numpy | ✅ 新交付 |
| `object_card_period_queen.py` | PeriodQueen 完整实现 | numpy | ✅ 验证通过 |
| `object_card_volfac.py` | VolFac 波动率因子 | numpy | ✅ 验证通过 |
| `object_card_voltarget.py` | VolTarget 仓位管理 | numpy | ✅ 验证通过 |
| `object_card_chzl_bsd.py` | 缠论分型 | numpy | ✅ 验证通过 |
| `object_card_bpb.py` | Brooks突破回调 | numpy | ✅ 验证通过 |
| `object_card_tkr7.py` | AO背离 | numpy | ✅ 验证通过 |
| `object_card_mflow.py` | 资金流向（真实/模拟双模式） | - | ✅ 验证通过 |
| `object_card_instb.py` | 机构行为 | - | ✅ 验证通过 |
| `object_card_kelly.py` | 凯利公式 | numpy | ✅ 验证通过 |
| `object_card_vp.py` | 成交量分布 | numpy | ✅ 验证通过 |
| `object_card_ytc.py` | YTC微观结构 | - | ✅ 验证通过 |
| `object_card_atratio.py` | 活跃度比率 | - | ✅ 验证通过 |
| `data_pipeline.py` | 数据管道（三源切换） | akshare, numpy | ⚠️ 远程不可用，本地正常 |
| `prototype_console_v2.py` | 控制台v2.0（五态面板+投票+事件流） | - | ✅ 可运行 |
| `rkx_analysis.py` | 瑞芯微分析演示脚本 | numpy | ✅ 可运行 |

### 4.3 架构设计文档（必读）

| 文件 | 必读等级 | 说明 |
|------|----------|------|
| `TRADING_SYSTEM_BLUEPRINT_v1.0.md` | ⭐⭐⭐ | **系统总蓝图** — 五层端到端链路，必须先看这个 |
| `SYSTEM_ARCHITECTURE_DRAFT.md` | ⭐⭐ | 系统架构初稿 |
| `MING_CABINET_HYBRID_ARCHITECTURE_v1.0.md` | ⭐⭐ | 明柜混合架构设计 |
| `GOVERNANCE_ARCHITECTURE_CHINA_v1.0.md` | ⭐⭐ | A股治理架构（五态动态切换） |
| `RISK_ARCHITECTURE_P0_R_v1.0.md` | ⭐⭐ | 风控架构 |
| `STRATEGY_BUNDLES_v1.0.md` | ⭐⭐ | 策略包设计（如何根据PeriodQueen状态选择激活对象卡） |
| `VOTE_DECISION_TABLE_P0_E_v1.0.md` | ⭐⭐ | 投票决策表（投票门槛和规则） |
| `BACKTEST_FRAMEWORK_DESIGN_v1.0.md` | ⭐⭐ | 回测框架设计（CSCV-PBO） |
| `DATA_PIPELINE_ETL_v1.0.md` | ⭐ | 数据管道ETL设计 |
| `MASTER_PROGRAMMING_INSTRUCTION_v1.0.md` | ⭐⭐⭐ | **主编程指令** — 开发规范、命名规则、输出格式要求 |

### 4.4 索引和审计文件

| 文件 | 说明 |
|------|------|
| `MASTER_INDEX_v1.0.md` | 全仓库110文件分类索引（快速查找文件） |
| `A_AUDIT_REPORT_v1.0.md` | 92份文档一致性审计报告（VOLFAC/ATRATIO补充标准字段） |
| `B_EXPERIMENT_B_EXP_20260707_223225_REPORT.md` | B实验报告（数据管道验证） |

### 4.5 外部策略原材料（历史记录，参考用）

`EXTERNAL_STRATEGY_RAW_MATERIAL_v1.0.md` ~ `v7.0.md`：多版本迭代的外部策略参考，记录系统进化轨迹。不必修改，仅供了解设计思路。

### 4.6 GLM交付物（前期AI助手的产出）

`GLM_MATERIAL_PACKAGE_INDEX.md`、`GLM_TASK_*.md`、`GLM_DELIVERY_*.md`：前期AI助手（GLM）的任务指令和交付物。如果后续开发需要了解原始需求，可以查阅。

---

## 五、如何上手开发（快速启动指南）

### 5.1 运行对象卡系统（最简单）

```python
# 在仓库目录下运行
from object_card_registry import ObjectCardRegistry, generate_klines_anchored

registry = ObjectCardRegistry()

# 生成模拟K线（base_price起始价, end_price终点价, n_days交易日数）
klines = generate_klines_anchored(base_price=100, end_price=120, n_days=252)

# 运行完整分析
result = registry.analyze(
    stock_code="000001.SZ",
    klines=klines,
    stock_name="平安银行",
    fundamentals={"PE": 8.5, "PB": 0.8},  # 可选
    user_cost=8.5  # 如果有持仓成本，可选
)

# 查看结果
print(result.final_signal)       # BUY / SELL / NEUTRAL
print(result.net_score)          # 净得分（>1.5为BUY，<-1.5为SELL）
print(result.permission)         # PERMISSION_FULL / REDUCED / EXIT_ONLY / HALT
print(result.avg_size_scalar)    # 建议仓位系数

# 生成Markdown报告
report = registry.generate_report(result)
with open("report.md", "w", encoding="utf-8") as f:
    f.write(report)
```

### 5.2 运行控制台（可视化）

```bash
cd E:\downloads\Desktop\找系统\特征
python prototype_console_v2.py
```

控制台会展示：五态治理模式面板 + 对象卡实时投票 + 事件流记录。

### 5.3 接入真实数据（本地环境）

```python
from data_pipeline import DataPipe

pipe = DataPipe(source="akshare")  # 或 "tushare"
series = pipe.get_daily("000001.SZ", n_days=252)

# 转成对象卡输入
volfac_input = pipe.to_volfac_input(series)
# ... 然后传给对应对象卡
```

**⚠️ 注意**: 远程服务器上AkShare可能被防火墙拦截，会自动降级到模拟数据。本地运行通常正常。

---

## 六、已知问题与注意事项（避免踩坑）

### 6.1 数据管道
- **问题**: 远程环境AkShare爬虫被防火墙拦截，返回 `Connection aborted` / `RemoteDisconnected`
- **解决方案**: 已内置 `SimulatedDataSource` fallback，生产环境请在本地运行或配置代理

### 6.2 对象卡输出格式不一致
- **问题**: 部分旧版对象卡 `signal_strength` 值范围有差异（有的用0-10，有的用-2~+2）
- **解决方案**: `ObjectCardRegistry` 的聚合函数已标准化处理，但新增对象卡时必须遵守 `-2.0~+2.0` 约定

### 6.3 PeriodQueen精度
- **问题**: 简化实现基于OHLCV统计特征模拟情绪周期，与真实"领涨股/空间板"数据有差距
- **后续优化**: 生产环境需接入真实涨跌停榜单（如通达信/同花顺数据接口）

### 6.4 A股纯多头约束
- **问题**: 部分执行层对象卡（如BPB、TKR7）在原始设计中可能有做空信号，在A股环境下必须降级
- **解决方案**: ATRATIO_P0_A 已明确将所有Sell信号置为 `confidence=0.0`，其他卡需要类似处理

### 6.5 回测框架缺失
- **问题**: CSCV-PBO回测诚实性检验框架尚未编码实现
- **优先级**: 高 — 这是策略上线的硬门槛

---

## 七、待办事项（下一任AI的工作列表）

按优先级排序：

1. **ObjectCardRegistry 接入真实数据** — 把 `generate_klines_anchored` 替换为 `data_pipeline.get_daily()`，实现真实股票分析
2. **回测框架 BACKTEST_FRAMEWORK** — 实现CSCV-PBO组合交叉验证，PBO<50%为硬门槛
3. **对象卡互锁联调** — CHZL_BSD × BPB × TKR7 共振检测（如缠论底分型 + AO底背离 + 突破回调支撑同时出现时，信号强度应大幅提升）
4. **PERIOD_QUEEN 接入真实数据** — 接入真实涨跌停榜单、空间板数据、领涨股数据替代模拟统计
5. **A股纯多头 Sell信号收口** — 遍历所有执行层对象卡，确认做空信号在A股环境下已正确降级
6. **控制台 v3.0** — 增加实时数据接入、自动刷新、邮件/飞书推送
7. **策略包 StrategyBundles** — 根据PeriodQueen状态动态选择激活哪些对象卡（如熊市只激活CHZL_BSD和KELLY）
8. **性能优化** — 对象卡并行运行（目前Registry是串行的，12张卡可以并行计算）

---

## 八、命名规范与代码风格（必须遵守）

### 8.1 文件命名
```
OBJECT_CARD_{OBJECT_ID}__{Description}_v{version}.md    # 对象卡规范
object_card_{short_name}.py                             # 对象卡实现
{subsystem}_{description}_v{version}.md                 # 子系统设计文档
```

### 8.2 代码风格
- Python 3.12+
- 使用 `dataclasses` 定义数据模型
- 对象卡实现必须返回 `ObjectCardOutput`（8个标准字段）
- 所有量化参数必须显式声明，不允许魔法数字
- A股特殊处理（涨跌停、T+1）必须加注释说明

### 8.3 输出格式
- Markdown 报告使用标准表格和层级标题
- JSON 输出必须包含 `aggregate` 和 `card_results` 两个顶级字段
- 中文标签使用全角标点，英文术语保留原样

---

## 九、关键联系人与资源

- **仓库路径**: `E:\downloads\Desktop\找系统\特征`
- **代码仓库**: `D:\Stock\trading_assistant`（历史代码，部分文件可能已过时）
- **Python环境**: Daimon managed runtime（`C:\Users\91883\AppData\Roaming\kimi-desktop\daimon-share\daimon\runtime\python`）
- **关键依赖**: `numpy`, `akshare`（可选，仅本地有效）

---

## 十、免责声明

本系统所有分析基于技术指标和公开数据，**不构成投资建议**。对象卡系统目前处于原型验证阶段，使用模拟数据运行，生产环境部署前必须完成回测框架和实盘验证。

---

*本手册由AI助手生成，随系统演进定期更新。如有疑问，先读 `TRADING_SYSTEM_BLUEPRINT_v1.0.md` 和 `MASTER_PROGRAMMING_INSTRUCTION_v1.0.md`。*
