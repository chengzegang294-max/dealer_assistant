# 风险管理_VanTharp_R乘数_期望与头寸规模_后续对象定义入口_v1

## 作用

- 把 `00_交易系统书籍\02_通向财务自由之路_VanTharp` 中最值得重开的对象收成一个明确入口。
- 当前目标不是直接做资金引擎或真实仓位控制，而是先固定：
  - 进入条件
  - 最小输入
  - 最小输出
  - 诊断层角色
  - 与现有来源层/运行时层的边界

## 当前定位

- 层级：
  - `02_原子化拆解文件` 后续对象层
- 当前角色：
  - `next_object_entry`
  - `DIAG_ONLY_OBJECT_CANDIDATE`
- 不是：
  - 当前已接入的真实头寸规模引擎
  - 当前自动执行仓位控制
  - 当前可直接用于实盘下单的风险模块

## 为什么先从 VanTharp 开

- 在 `00_交易系统书籍` 里，它是最容易压成“最小可验证对象”的一类：
  - `R乘数` 定义清楚
  - `期望收益` 定义清楚
  - `百分比风险头寸规模` 有明确公式
- 相比 `墨菲 / Kaufman`：
  - 更少依赖主观图形解释
  - 更容易写成固定输入/输出
  - 更适合作 `diag-only / proof-of-mapping`
- 相比直接重开整本：
  - `R乘数 / 期望 / 头寸规模` 是可先单独落地的最小闭环

## 来源锚点

- 主来源：
  - `00_交易系统书籍\02_通向财务自由之路_VanTharp\book2_通向财务自由之路_STEP_A_B_切片提炼.md`
- 当前优先吸收的切片：
  - `ch07-s1 | R乘数与期望收益`
  - `ch14-s1 | 头寸规模模型`
- 当前承接方式：
  - 以 `STEP_A_B_切片提炼.md` 为合同主源
  - 暂不回退到整本图片资产层

## 最小输入

- 交易级最小输入：
  - `entry_price`
  - `stop_price`
  - `exit_price`
  - `position_size`
  - `account_equity`
  - `risk_percent`
- 样本级最小输入：
  - `trade_id`
  - `symbol`
  - `entry_time`
  - `exit_time`
  - `gross_pnl`
  - `commission`
  - `slippage`
- 组合级第一版不强求：
  - `correlation_cluster`
  - `portfolio_heat`
  - `multi-system allocation`

## 最小输出

- 单笔级：
  - `initial_risk_amount_used`
  - `r_multiple`
  - `position_size_by_percent_risk`
- 样本级：
  - `expectancy_r`
  - `trade_count`
  - `expectancy_confidence_state`
- 诊断级：
  - `risk_model_state`
    - `valid / invalid / unknown`
  - `position_sizing_state`
    - `conservative / acceptable / aggressive / unknown`

## 最小对齐逻辑

- `R乘数`
  - 定义为：`(实际盈亏) / (初始风险)`
- `期望收益`
  - 定义为：`R乘数序列的平均值`
- `百分比风险头寸规模`
  - 定义为：`(account_equity * risk_percent) / 单笔初始风险`
- 第一版先只做：
  - `trade-level mapping`
  - `sample-level diagnostics`
- 第一版不做：
  - 真正资金曲线驱动
  - 多品种组合热度约束
  - 实盘头寸自动调整

## 最小验收定义

- 有一份对象合同草案：
  - 输入/输出/边界明确
- 有一份最小样本映射草案：
  - 至少能说明单笔 `R乘数` 如何算
  - 至少能说明样本 `expectancy_r` 如何算
- 有一份当前角色裁决：
  - `DIAG_ONLY_OBJECT_CANDIDATE`
- 不得提前宣称：
  - 已接入交易执行链路
  - 已成为仓位引擎默认模块
  - 已具备组合级真实风控能力

## 当前 gaps

- `commission / slippage` 是否纳入第一版 `R乘数` 口径，需要单独冻结。
- `bootstrap 置信区间 / 破产概率` 这些检验适合第二阶段，不塞进第一版最小合同。
- 当前不应把 `头寸规模` 直接连到自动执行入口。

## 当前裁决

- `VanTharp` 当前不再只是“交易心理/方法学背景书”。
- 更准确的角色应固定为：
  - `00_交易系统书籍` 首批可重开对象之一
  - 优先角色是 `R-multiple / expectancy / sizing diag-layer`
  - 先落 `diag-only / proof-of-mapping`

## 下一步

- 若继续推进同一条线，优先顺序应为：
  - 已完成：
    - 最小合同草案：
      - `12_工具运行时_TOOLING_RUNTIME\vantharp_risk_p0_v1\vantharp_risk_p0_min_contract_v1.md`
    - 第一份 proof-of-mapping：
      - `12_工具运行时_TOOLING_RUNTIME\vantharp_risk_p0_v1\vantharp_risk_p0_proof_of_mapping_v1.md`
      - `12_工具运行时_TOOLING_RUNTIME\vantharp_risk_p0_v1\real_input_samples\vantharp_risk_p0_proof_input_v1.csv`
      - `12_工具运行时_TOOLING_RUNTIME\vantharp_risk_p0_v1\real_input_samples\vantharp_risk_p0_proof_output_v1.csv`
    - v2 双口径冻结与对照 proof：
      - `12_工具运行时_TOOLING_RUNTIME\vantharp_risk_p0_v1\vantharp_risk_p0_fields_output_header_v2.txt`
      - `12_工具运行时_TOOLING_RUNTIME\vantharp_risk_p0_v1\real_input_samples\vantharp_risk_p0_proof_input_v2.csv`
      - `12_工具运行时_TOOLING_RUNTIME\vantharp_risk_p0_v1\real_input_samples\vantharp_risk_p0_proof_output_v2.csv`
  - 下一步优先：
    - 把真实数据源的字段映射到两种模式之一（按单账户/单券商冻结）：
      - `statement_amount`：来自 `交割单/成交明细` 的金额字段
      - `entry_stop_calc`：来自 `entry/stop/点值换算` 的计算字段
    - 再决定是否需要：
      - `append stub`（把 proof 行追加到统一 trade-level runtime csv）
