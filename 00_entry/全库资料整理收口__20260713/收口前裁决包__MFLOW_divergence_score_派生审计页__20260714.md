# 收口前裁决包 MFLOW divergence_score 派生审计页

更新时间：2026-07-14

## 用途

- 这份审计页只负责回答：
  - `mflow_divergence_score` 是否可以用“现有真实源 + 最小派生规则”站住为 `proxy` 字段
  - 当前派生规则是否具备可解释性与可复现性
- 当前不回答：
  - 最终稳定公式
  - 是否进入生产级实现

## 当前审计输入

- 资金源（真实）：
  - `02_runtime/ashare_p0_first_round_validation/data/t02_sources/moneyflow_tushare/t02_moneyflow_tushare_batch__sample20_q2__20260401_20260630.csv`
- 日线 OHLCV（真实）：
  - `02_runtime/ashare_p0_first_round_validation/data/t02_sources/daily_tushare/t02_daily_tushare_batch__sample20_q2__20260401_20260630.csv`
- 当前样本窗口：
  - `2026-04-01 -> 2026-06-30`
  - `symbols=20`
  - `rows=1200`

## 派生口径 v0

- 定义：
  - `price_ret = (close - open) / open`
  - `flow_ratio = main_fund_net_inflow_ratio`
- divergence 触发条件：
  - `price_ret > 0` 且 `flow_ratio < 0`
  - 或 `price_ret < 0` 且 `flow_ratio > 0`
- divergence_score_v0：
  - 若不触发 divergence：`0`
  - 若触发 divergence：
    - `min(1.0, abs(price_ret)*10 + abs(flow_ratio)*5)`
- 当前说明：
  - 这个 v0 不是“最终公式”，而是为了审计：
    - 是否存在稳定可复现的“价-流背离信号”
    - 背离强度是否能被压缩到 `[0,1]`

## 实证结果（sample20_q2）

- join 结果：
  - `moneyflow rows=1200`
  - `daily rows=1200`
  - `joined rows=1200`
- 可复现产物：
  - `02_runtime/ashare_p0_first_round_validation/artifacts/mflow_divergence_score_v0/mflow_divergence_score_v0_summary_latest.json`
  - `02_runtime/ashare_p0_first_round_validation/artifacts/mflow_divergence_score_v0/mflow_divergence_score_v0_detail_latest.tsv`
  - `02_runtime/ashare_p0_first_round_validation/artifacts/mflow_divergence_score_v0/mflow_divergence_score_v0_symbol_counts_latest.tsv`
- 背离触发密度：
  - `divergence_rows=218`
  - `divergence_rate=0.1817`
  - 分解：
    - `price_up_flow_down=175`
    - `price_down_flow_up=43`
- 背离强度分布（v0）：
  - `score_mean_all=0.0633`
  - `score_mean_divergence_only=0.3483`
  - `p50=0.2871`
  - `p90=0.6803`
  - `p95=0.8512`
- 价-流相关性（样本内）：
  - `corr(price_ret, flow_ratio)=0.6299`

## 当前结论

- 当前可以裁决为：
  - `mflow_divergence_score` 是可派生的 `proxy` 字段
  - 且已具备最小可复现审计链（真实源 + v0 规则 + 明确统计）
- 但当前也必须保留边界：
  - v0 派生用的是 `open->close` 日内收益，不等价于 `close->close` 趋势背离
  - 当前只在 `sample20_q2` 上审计成立，不外推成“全市场长期稳定”
  - 当前 `T02` 候选宽表已可由 `daily_tushare` 作为底表生成（open/high/low/close 已就绪），但 divergence 派生链尚未并入主 runner

## 风险与降级

- 主要风险：
  - 把 `v0` 当成最终指标公式
  - 把样本内统计当成全市场结论
- 可接受降级：
  - 在对象卡层把 `mflow_divergence_score` 标记为：
    - `proxy_derivable_audited_v0`
  - 仅用于解释链与过滤层的候选信号，不用于仓位/下单层
- 若未来需要更强版本：
  - 需要把 divergence 派生链正式接入 `T02 real_input` 的 runner/派生层
  - 需要重新定义：
    - `price_ret` 的时间窗
    - `score` 的缩放与抗噪处理

## 主负责人裁决

- 当前裁决：
  - `mflow_divergence_score` 的派生审计已通过（proxy 级）
- 对 `MFLOW` 状态的影响：
  - `MFLOW` 可以继续保持为“第二批观察中的优先审计对象”
  - 但仍不等于“完整字段闭环已完成”

## 回链

- `收口前裁决包__MFLOW_provider与样本可得性审计页__20260714.md`
- `收口前裁决包__MFLOW_字段映射审计页__20260714.md`
- `收口前裁决包__MFLOW_vs_INSTB_多AI讨论前情提要与裁决框架__20260714.md`
- `02_runtime/ashare_p0_first_round_validation/fetch_t02_daily_batch_tushare_v1.py`
- `02_runtime/ashare_p0_first_round_validation/analyze_mflow_divergence_score_v0_from_t02_real_input_v1.py`
- `02_runtime/ashare_p0_first_round_validation/data/t02_sources/daily_tushare/t02_daily_tushare_batch__sample20_q2__20260401_20260630.csv`
- `02_runtime/ashare_p0_first_round_validation/data/t02_sources/moneyflow_tushare/t02_moneyflow_tushare_batch__sample20_q2__20260401_20260630.csv`
- `02_runtime/ashare_p0_first_round_validation/artifacts/mflow_divergence_score_v0/mflow_divergence_score_v0_summary_latest.json`
