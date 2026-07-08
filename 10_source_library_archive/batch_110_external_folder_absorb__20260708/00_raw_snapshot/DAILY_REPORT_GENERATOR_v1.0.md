# AI 投研日报生成器设计 v1.0

> **本文档全部内容源于用户（仓库所有者）的想法，由 Kimi 整理为结构化文档供编程 AI 参考。**
> 版本：v1.0 | 状态：设计阶段 | 来源：用户素材"私人投研管家"视频笔记
> 核心目标：每日自动生成结构化投研日报，覆盖宏观/资金/持仓/预警

---

## 一、模块定位

```text
模块名称：DailyReportGenerator（AI 投研日报生成器）
模块层级：独立模块，不进入核心 Pipeline
与系统的关系：
  - 读取 GovernanceEngine 的状态
  - 读取 MacroEnvironmentScorer 的评分
  - 读取 PeriodQueen 的状态
  - 读取持仓数据
  - 输出 Markdown 格式日报

生成时机：
  - 主生成：每日收盘后 17:00（A 股 15:00 收盘，留 2 小时数据处理）
  - 盘中简报：11:30（午间休市）和 14:55（收盘前）——可选
  - 紧急播报：触发重大事件时（如组合回撤 > 10%）

输出格式：
  - Markdown（供人阅读）
  - JSON（供系统消费）
  - 可选：发送到用户指定渠道（飞书/邮件/微信——未来扩展）
```

---

## 二、日报内容结构

### 2.1 日报总览

```markdown
# 📊 投资管家日报 — 2024年6月24日（周一）

> 生成时间：17:30 | 数据截至：15:00 | 制度模式：常态内阁模式

---

## 📌 今日摘要（Executive Summary）

| 维度 | 状态 | 核心结论 |
|------|------|----------|
| 天时 | 🟢 偏暖 | 宏观评分 62/100，利率下行中 |
| 地利 | 🟡 震荡 | 沪深300 +0.8%，涨跌家数比 45:12 |
| 人和 | 🟢 正常 | 内阁票拟3笔，六科通过2笔 |
| 持仓 | 🟢 健康 | 总仓位60%，浮盈+2.1%，无止损触发 |
| 明日 | 🟡 关注 | 关注000100.SZ接近止损线 |

**今日决策**：批红2笔买入，留中1笔，否决0笔
**明日建议**：维持当前仓位，关注宏观利率数据

---

## 一、天时：宏观环境（MacroEnvironmentScorer 输出）

### 1.1 综合评分
**宏观评分：62/100** [████████░░] 🟡 偏暖

### 1.2 五维度详情
| 维度 | 评分 | 趋势 | 解读 |
|------|------|------|------|
| 利率 | 75 ↑ | 下行 | 10年期国债2.35%，处于历史低位，资金成本友好 |
| 汇率 | 55 → | 震荡 | 在岸人民币7.245，小幅贬值，但波动可控 |
| 流动性 | 65 ↑ | 充裕 | M2增速10.5%，市场成交额放大12% |
| 风险偏好 | 60 → | 中性 | 沪深300波动率18.5%，市场情绪平稳 |
| 政策 | 55 → | 中性 | 上周降准释放流动性，无重大政策变化 |

### 1.3 宏观对交易的影响
- **仓位建议**：宏观偏暖，PeriodQueen 仓位上限维持 100%
- **行业倾向**：利率下行利好成长股，关注科技/医药
- **风险提示**：汇率小幅贬值，警惕外资流出对蓝筹的压制

---

## 二、地利：市场行情（Market Overview）

### 2.1 核心指数
| 指数 | 收盘 | 涨跌 | 振幅 | 成交额 | 趋势 |
|------|------|------|------|--------|------|
| 沪深300 | 3,520 | +0.8% | 1.2% | 2,850亿 | 🟡 震荡 |
| 中证500 | 5,280 | +1.2% | 1.5% | 1,920亿 | 🟢 上行 |
| 创业板指 | 1,850 | +0.5% | 1.8% | 1,250亿 | 🟡 震荡 |
| 科创50 | 820 | +1.5% | 2.1% | 580亿 | 🟢 上行 |

### 2.2 市场情绪
- **涨跌家数**：上涨 3,245 家 / 下跌 1,876 家
- **涨跌停**：涨停 45 家 / 跌停 12 家
- **北向资金**：净流入 +28.5 亿
- **主力资金**：净流入 +45.2 亿（科技板块）

### 2.3 板块热度
| 板块 | 涨幅 | 资金流入 | 热度 |
|------|------|----------|------|
| 半导体 | +3.2% | +52亿 | 🔥🔥🔥 |
| 医药 | +2.1% | +28亿 | 🔥🔥 |
| 新能源 | -0.8% | -15亿 | ❄️ |
| 银行 | +0.3% | +8亿 | 🟡 |

---

## 三、人和：系统运行（GovernanceEngine 状态）

### 3.1 制度模式
**当前模式：常态内阁模式**（已连续运行 8 天）
- 首辅：就绪 | 次辅：就绪
- 六科：全部通过
- 台谏：后置监察，无预警

### 3.2 今日票拟
| 编号 | 标的 | 方向 | 仓位 | 信心 | 六科 | 皇帝决策 | 状态 |
|------|------|------|------|------|------|----------|------|
| ZHE-001 | 000001.SZ | 买入 | 6% | 8/10 | ✅通过 | 批红 | ✅已执行 |
| ZHE-002 | 000002.SZ | 买入 | 4% | 7/10 | ✅通过 | 批红 | ✅已执行 |
| ZHE-003 | 000003.SZ | 买入 | 5% | 6/10 | ❌封驳 | - | ⏸️驳回 |

### 3.3 起居注（今日重要事件）
- 09:30 内阁提交 ZHE-001
- 09:31 六科通过 ZHE-001，盖印
- 09:32 皇帝批红 ZHE-001，执行买入
- 09:35 内阁提交 ZHE-002
- ...

---

## 四、持仓：资产诊断（Portfolio Diagnosis）

### 4.1 总体概览
- **总资产**：1,000 万
- **现金**：400 万（40%）
- **股票市值**：600 万（60%）
- **今日盈亏**：+12.5 万（+1.25%）
- **累计收益**：+52 万（+5.2%）
- **最大回撤**：-3.8%

### 4.2 持仓明细
| 标的 | 仓位 | 成本 | 现价 | 今日盈亏 | 累计盈亏 | 止损 | 状态 |
|------|------|------|------|----------|----------|------|------|
| 000001.SZ | 6% | 12.50 | 13.20 | +0.8% | +5.6% | 11.80 | 🟢正常 |
| 000002.SZ | 4% | 25.00 | 23.50 | -1.2% | -6.0% | 22.00 | 🟡关注 |
| 000010.SZ | 5% | 8.00 | 8.50 | +0.5% | +6.3% | 7.50 | 🟢正常 |
| 000100.SZ | 3% | 30.00 | 28.00 | -2.1% | -6.7% | 27.00 | 🔴预警 |

### 4.3 风险扫描
| 风险指标 | 当前值 | 上限 | 状态 |
|----------|--------|------|------|
| 单票最大风险 | 1.8% | 2.0% | 🟢合规 |
| 组合总风险 | 4.2% | 6.0% | 🟢合规 |
| 现金比例 | 40% | >10% | 🟢充足 |
| 行业集中度 | 银行25% | <30% | 🟢合规 |

### 4.4 操作建议
- 🔴 **000100.SZ**：现价 28.00，止损 27.00（距离 3.6%），建议明日密切关注
- 🟡 **000002.SZ**：浮亏 6%，但未触发止损，建议观察 2 日
- 🟢 **其余持仓**：正常，无操作需求

---

## 五、明日关注（Tomorrow's Watchlist）

### 5.1 预警条件检查
| 预警条件 | 当前状态 | 触发阈值 | 距离触发 |
|----------|----------|----------|----------|
| 组合回撤 > 10% | 3.8% | 10% | 6.2% |
| 单票亏损 > 10% | 6.7% | 10% | 3.3% |
| 宏观评分 < 20 | 62 | 20 | 42 |
| 连续亏损 > 5 笔 | 2 笔 | 5 笔 | 3 笔 |

### 5.2 明日事件日历
- 10:00 中国 6 月制造业 PMI（预期 49.5，前值 49.4）
- 14:00 美国 5 月耐用品订单
- 20:30 美国 6 月消费者信心指数

### 5.3 系统待处理
- 1 笔留中奏折（ZHE-003）等待明日重新评估
- 季度财报季临近，准备更新 A5 基本面候选池

---

## 六、偏差分析与自优化（Weekly Only）

> 注：此部分仅在周一的日报中显示

### 6.1 本周偏差统计
| 预测方向 | 实际方向 | 次数 | 偏差类型 |
|----------|----------|------|----------|
| 看多 | 上涨 | 5 | ✅准确 |
| 看多 | 下跌 | 2 | ❌过度乐观 |
| 看空 | 下跌 | 1 | ✅准确 |
| 看空 | 上涨 | 0 | ✅准确 |

### 6.2 本周修正建议
- 系统存在轻微"过度乐观"偏差（2/7 笔）
- 建议：牛市模式下降低信心度门槛 0.5 分

---

> 📜 **起居注**：本日报由投资管家系统自动生成，皇帝（用户）可批红/留中/否决
> 🔄 **数据更新**：宏观数据每日 17:00 更新，持仓数据实时更新
> 📧 **反馈**：如对日报内容有建议，请在控制台输入 `feedback`
```

---

## 三、生成器设计

### 3.1 类设计

```python
from datetime import datetime
from typing import Protocol
import json

class DataProvider(Protocol):
    """数据源协议"""
    def get_macro_score(self, date: str) -> dict: ...
    def get_market_overview(self, date: str) -> dict: ...
    def get_governance_status(self, date: str) -> dict: ...
    def get_portfolio(self, date: str) -> dict: ...
    def get_positions(self, date: str) -> list[dict]: ...
    def get_memorials(self, date: str) -> list[dict]: ...
    def get_logs(self, date: str) -> list[dict]: ...


class DailyReportGenerator:
    """
    AI 投研日报生成器
    
    职责：
    1. 每日收盘后自动拉取系统状态
    2. 生成结构化日报（Markdown + JSON）
    3. 保存到指定目录
    4. 可选：推送到用户渠道
    """
    
    def __init__(self, data_provider: DataProvider, output_dir: str = "reports/daily"):
        self.data = data_provider
        self.output_dir = output_dir
    
    def generate(self, date: str | None = None) -> dict:
        """
        生成日报
        
        Args:
            date: 日期（YYYY-MM-DD），默认今天
        
        Returns:
            {
                "markdown": str,      # Markdown 格式日报
                "json": dict,         # 结构化数据
                "file_path": str,     # 保存路径
            }
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 拉取数据
        macro = self.data.get_macro_score(date)
        market = self.data.get_market_overview(date)
        governance = self.data.get_governance_status(date)
        portfolio = self.data.get_portfolio(date)
        positions = self.data.get_positions(date)
        memorials = self.data.get_memorials(date)
        logs = self.data.get_logs(date)
        
        # 生成各章节
        sections = {
            "summary": self._generate_summary(macro, market, governance, portfolio),
            "macro": self._generate_macro_section(macro),
            "market": self._generate_market_section(market),
            "governance": self._generate_governance_section(governance, memorials, logs),
            "portfolio": self._generate_portfolio_section(portfolio, positions),
            "watchlist": self._generate_watchlist_section(portfolio, positions),
        }
        
        # 组装 Markdown
        markdown = self._assemble_markdown(date, sections)
        
        # 组装 JSON
        json_data = self._assemble_json(date, macro, market, governance, portfolio, positions, memorials)
        
        # 保存
        file_path = self._save(date, markdown, json_data)
        
        return {
            "markdown": markdown,
            "json": json_data,
            "file_path": file_path,
        }
    
    def _generate_summary(self, macro: dict, market: dict,
                          governance: dict, portfolio: dict) -> dict:
        """生成今日摘要"""
        # 计算各项状态
        macro_status = self._interpret_macro(macro["macro_score"])
        market_status = self._interpret_market(market["csi300_change"])
        governance_status = self._interpret_governance(governance)
        portfolio_status = self._interpret_portfolio(portfolio)
        
        return {
            "macro": {"status": macro_status["icon"], "text": macro_status["text"]},
            "market": {"status": market_status["icon"], "text": market_status["text"]},
            "governance": {"status": governance_status["icon"], "text": governance_status["text"]},
            "portfolio": {"status": portfolio_status["icon"], "text": portfolio_status["text"]},
            "decision": f"批红{governance['approved']}笔，留中{governance['deferred']}笔，否决{governance['rejected']}笔",
        }
    
    def _interpret_macro(self, score: float) -> dict:
        if score >= 80: return {"icon": "🟢", "text": "极度友好"}
        elif score >= 60: return {"icon": "🟢", "text": "偏暖"}
        elif score >= 40: return {"icon": "🟡", "text": "震荡"}
        elif score >= 20: return {"icon": "🔴", "text": "偏冷"}
        else: return {"icon": "🔴", "text": "极度不利"}
    
    def _interpret_market(self, change: float) -> dict:
        if change > 1.5: return {"icon": "🟢", "text": "强势"}
        elif change > 0.5: return {"icon": "🟢", "text": "上行"}
        elif change > -0.5: return {"icon": "🟡", "text": "震荡"}
        elif change > -1.5: return {"icon": "🔴", "text": "下行"}
        else: return {"icon": "🔴", "text": "弱势"}
    
    def _interpret_governance(self, governance: dict) -> dict:
        mode = governance.get("mode", "normal")
        if mode == "crisis": return {"icon": "🔴", "text": "紧急"}
        elif mode == "bear": return {"icon": "🟡", "text": "谨慎"}
        else: return {"icon": "🟢", "text": "正常"}
    
    def _interpret_portfolio(self, portfolio: dict) -> dict:
        drawdown = portfolio.get("max_drawdown", 0)
        if drawdown > 10: return {"icon": "🔴", "text": "警戒"}
        elif drawdown > 5: return {"icon": "🟡", "text": "关注"}
        else: return {"icon": "🟢", "text": "健康"}
    
    def _assemble_markdown(self, date: str, sections: dict) -> str:
        """组装 Markdown 日报"""
        # 使用 Jinja2 模板或字符串拼接
        # 详见上文"日报内容结构"
        pass
    
    def _assemble_json(self, date: str, **data) -> dict:
        """组装 JSON 结构化数据"""
        return {
            "date": date,
            "generated_at": datetime.now().isoformat(),
            "data": data,
        }
    
    def _save(self, date: str, markdown: str, json_data: dict) -> str:
        """保存日报"""
        import os
        os.makedirs(self.output_dir, exist_ok=True)
        
        md_path = f"{self.output_dir}/daily_{date}.md"
        json_path = f"{self.output_dir}/daily_{date}.json"
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        return md_path
```

### 3.2 数据源适配器

```python
class GovernanceDataAdapter:
    """
    GovernanceEngine → DailyReportGenerator 的数据适配器
    
    职责：将 GovernanceEngine 的内部状态转换为日报所需的格式
    """
    
    def __init__(self, governance_engine):
        self.engine = governance_engine
    
    def get_macro_score(self, date: str) -> dict:
        """从 MacroEnvironmentScorer 获取"""
        return self.engine.macro_scorer.get_score(date)
    
    def get_governance_status(self, date: str) -> dict:
        """从 GovernanceEngine 获取"""
        return {
            "mode": self.engine.controller.current_mode.value,
            "mode_start": self.engine.controller.mode_start.isoformat(),
            "shoufu_ready": True,
            "cifu_ready": True,
            "approved": len([m for m in self.engine.cabinet.daily_proposals if m.verdict == "pass"]),
            "deferred": 0,  # TODO
            "rejected": len([m for m in self.engine.cabinet.daily_proposals if m.verdict == "reject"]),
        }
    
    def get_memorials(self, date: str) -> list[dict]:
        """获取今日奏折"""
        return [m.to_dict() for m in self.engine.cabinet.daily_proposals]
    
    def get_logs(self, date: str) -> list[dict]:
        """获取今日起居注"""
        return self.engine.audit.query(event_type=None, start=f"{date}T00:00:00", end=f"{date}T23:59:59")
```

---

## 四、生成流程

```text
每日收盘后自动生成流程：

17:00 触发（A股收盘后2小时）
  │
  ├─ Step 1: 拉取宏观数据（MacroEnvironmentScorer）
  │   ├─ 利率：10年期国债收益率
  │   ├─ 汇率：USDCNY
  │   ├─ 流动性：M2 / SHIBOR / 成交额
  │   ├─ 风险偏好：HV20 / VIX
  │   └─ 政策：最近7天政策事件
  │
  ├─ Step 2: 拉取市场数据
  │   ├─ 核心指数：沪深300/中证500/创业板/科创50
  │   ├─ 涨跌家数、涨跌停、北向资金
  │   └─ 板块热度（申万一级行业）
  │
  ├─ Step 3: 拉取系统状态（GovernanceEngine）
  │   ├─ 当前制度模式
  │   ├─ 今日票拟记录
  │   ├─ 六科审查结果
  │   └─ 皇帝决策记录
  │
  ├─ Step 4: 拉取持仓数据
  │   ├─ 总资产、现金、股票市值
  │   ├─ 各持仓盈亏、止损状态
  │   └─ 风险指标扫描
  │
  ├─ Step 5: 生成日报
  │   ├─ Markdown 格式（供人阅读）
  │   └─ JSON 格式（供系统消费）
  │
  └─ Step 6: 保存并通知
      ├─ 保存到 reports/daily/YYYY-MM-DD.{md,json}
      └─ 可选：推送到用户渠道

盘中简报触发（可选）：
  11:30 触发（午间休市）
    ├─ 只生成"市场行情"和"持仓快照"
    └─ 不包含"票拟"和"宏观"（数据不完整）
  
  14:55 触发（收盘前5分钟）
    ├─ 生成"今日预览"（预判收盘状态）
    └─ 提醒用户关注临近止损的持仓

紧急播报触发：
  组合回撤 > 10% → 立即生成紧急日报
  单票亏损 > 15% → 立即生成紧急日报
  市场进入 HALT → 立即生成紧急日报
```

---

## 五、特殊日报

### 5.1 周一日报（Weekly Review）

```text
周一的日报包含额外的"周报"内容：

新增章节：
  - 上周绩效回顾（收益率、夏普、回撤）
  - 上周偏差分析（预测 vs 实际）
  - 本周策略建议（基于 PeriodQueen 和宏观评分）
  - 本周事件日历（重要经济数据、财报发布）

生成时间：周一 17:00（比日常日报多 5 分钟处理时间）
```

### 5.2 财报季日报

```text
财报季（4月/8月/10月）的日报包含额外的"财报预警"：

新增章节：
  - 今日发布财报的持仓标的
  - 财报-preview（预期 vs 一致预期）
  - 财报发布后的操作建议（持仓/减仓/清仓）

触发条件：
  - 持仓中有标的在当日发布财报
  - A5 基本面候选池中有标的在当日发布财报
```

### 5.3 紧急日报

```text
触发条件（满足任一）：
  - 组合回撤 > 10%
  - 单票亏损 > 15%
  - 市场进入 EXTREME_VOL / HALT
  - 宏观评分骤降 > 30 分
  - 用户手动触发

内容特点：
  - 标题带 🔴 紧急标记
  - 只包含关键信息（持仓风险、操作建议）
  - 生成时间：触发后 1 分钟内
  - 必须推送给用户（不能仅保存）
```

---

## 六、实施路线图

```text
Phase 1：数据拉取（Week 1）
  - 实现 GovernanceDataAdapter
  - 实现 MacroDataAdapter
  - 实现 MarketDataAdapter

Phase 2：日报生成（Week 1-2）
  - 实现各章节生成器（_generate_macro_section 等）
  - 实现 Markdown 模板引擎
  - 实现 JSON 组装器

Phase 3：自动化调度（Week 2）
  - 实现定时触发（17:00 每日）
  - 实现紧急播报触发
  - 实现文件保存

Phase 4：用户渠道（Week 3，可选）
  - 飞书机器人推送
  - 邮件发送
  - 控制台内嵌显示

Phase 5：回测集成（Week 3-4）
  - 将日报生成器接入回测引擎
  - 验证日报在回测模式下的正确性
  - 生成历史日报用于复盘
```

---

## 七、对编程 AI 的指令

```text
1. DailyReportGenerator 是独立模块，不进入核心 Pipeline
2. 日报数据源通过 Adapter 模式接入，不直接依赖 GovernanceEngine
3. Markdown 模板使用 Jinja2，支持自定义模板
4. JSON 输出必须包含完整结构化数据（供其他系统消费）
5. 日报保存路径：reports/daily/YYYY-MM-DD.{md,json}
6. 紧急日报生成时间 < 1 分钟
7. 日报中所有数字必须格式化（百分比保留1位小数，金额保留2位小数）
8. 日报中的 emoji 用于快速视觉识别，不影响文字可读性
```

---

> 文件：DAILY_REPORT_GENERATOR_v1.0.md
> 生产者：Kimi（整理用户的"私人投研管家"素材）
> 核心设计：每日自动生成 Markdown + JSON 双格式日报
> 特殊日报：周一周报、财报季日报、紧急日报
