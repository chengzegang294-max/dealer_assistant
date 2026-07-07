# 技术指标_波动率_RSJ市场情绪冷暖剂_后续对象定义入口_v1

## 作用

- 把 `S桶 -> 03_券商研报` 中最适合迁移到 `FX/商品` 主线的一类纯时间序列对象，先收成明确入口。
- 当前目标不是直接把 `RSJ` 变成主线硬门控，而是先固定：
  - 来源锚点
  - 最小输入
  - 最小输出
  - 诊断层角色
  - 与现有 `N01 vol state / 四轴状态模板` 的边界

## 当前定位

- 层级：
  - `02_原子化拆解文件` 后续对象层
- 当前角色：
  - `next_object_entry`
  - `DIAG_ONLY_OBJECT_CANDIDATE`
  - `state_or_timing_label`
- 不是：
  - 当前已接入的交易门控
  - 当前默认择时模块
  - 当前自动执行入口

## 为什么先从 RSJ 开

- 在 `yes = 9` 的候选里，它是最接近“纯时间序列波动率状态”对象的一条：
  - 不要求 `Level2 / 逐笔 / 订单簿`
  - 只依赖收益率序列
  - 适合先做 `diag-only / proof-of-mapping`
- 相比 `价量相关性`：
  - 对成交量质量依赖更小
  - 在 `FX/商品` 上更容易先形成最小可验证映射
- 相比 `SemiBeta / 特异波动率`：
  - `RSJ` 更像可直接进入状态标签层的对象
  - 与当前 `N01 vol state` 的协同更直观

## 来源锚点

- 主来源：
  - `S桶\03_券商研报\01_高频微观\20200728-财通证券-高频波动率择时指标：RSJ市场情绪冷暖剂.pdf`
- 当前吸收结论：
  - `can_map_to_fx = yes`
  - `data_dependency = 分钟线/指数数据`
  - 当前更像 `波动率情绪择时标签`，不是单独策略

## 最小输入

- 基础行情：
  - `symbol`
  - `timeframe`
  - `bar_time`
  - `open`
  - `high`
  - `low`
  - `close`
- 第一版最小依赖：
  - 可重建连续收益率序列
  - 可在固定窗口内拆分正负收益波动
- 第一版不强求：
  - `真实成交量`
  - `Level2`
  - `订单簿`

## 最小输出

- `rsj_score`
  - 连续窗口下的 `RSJ` 数值
- `rsj_state`
  - `warm / cold / neutral / unknown`
- `rsj_extreme_flag`
  - `extreme_high / extreme_low / none / unknown`
- `rsj_timing_bias`
  - `risk_on / risk_off / wait / unknown`

## 最小对齐逻辑

- `RSJ` 当前先承接为：
  - 波动率与情绪的混合状态标签
- 第一版只做：
  - 固定窗口统计
  - 标签分层
  - `proof-of-mapping`
- 第一版不做：
  - 入场条件
  - 仓位倍率
  - 与其他因子的加权合成

## 与现有主线的边界

- 与 `Batch9 N01 vol state`：
  - `N01` 是更宽的波动率状态层
  - `RSJ` 更像其中一个可候选补充标签
  - 当前不能反向改写 `N01` 默认口径
- 与 `四轴状态模板`：
  - 更适合挂到 `volatility_regime_state` 的补充观察层
  - 不单独升级为策略

## 最小验收定义

- 有一份对象入口文件：
  - 输入/输出/边界明确
- 有一份后续最小合同草案：
  - 至少冻结 `rsj_score / rsj_state / rsj_timing_bias`
- 有一份 `proof-of-mapping`：
  - 说明如何从收益率序列得到 `RSJ` 数值与标签
- 不得提前宣称：
  - 已进入主线默认择时
  - 已成为执行链路风控开关

## 当前裁决

- `RSJ` 当前应固定为：
  - `yes=9` 中第一优先的纯时间序列对象之一
  - 先落 `diag-only / proof-of-mapping`
  - 先服务于 `状态标签层`

## 下一步

- 若继续推进同一条线，优先顺序应为：
  - 已落 `RSJ P0 最小合同`
  - 已落 `proof-of-mapping` 样本
  - 已落 `runtime notes / output header`
  - 已落 `params template / append stub / runtime csv`
  - 已完成一次 `dry-run + persist`
  - 已落 `append_from_raw_window` 接口空壳
  - 已完成一次 `append_from_raw_window --dry-run`
  - 已冻结 `raw-window input contract`
  - 已落 `raw-window sample schema / sample input`
  - 下一步再决定是否值得进入真正的 raw-window 真实绑定

## 已落盘文件

- `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_min_contract_v1.md`
- `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_proof_of_mapping_v1.md`
- `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_runtime_notes_v1.md`
- `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_fields_output_header_v1.txt`
- `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_runtime_params_template_v1.json`
- `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_runtime_append_stub_v1.py`
- `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_runtime_append_acceptance_v1.md`
- `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_fields_runtime_v1.csv`
- `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_append_from_raw_window_stub_v1.py`
- `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_raw_window_stub_acceptance_v1.md`
- `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_raw_window_input_contract_v1.md`
- `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_raw_window_input_header_v1.txt`
- `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_raw_window_sample_schema_v1.md`
- `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\real_input_samples\rsj_state_p0_raw_window_sample_input_v1.csv`
- `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\real_input_samples\rsj_state_p0_proof_input_v1.csv`
- `12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\real_input_samples\rsj_state_p0_proof_output_v1.csv`
