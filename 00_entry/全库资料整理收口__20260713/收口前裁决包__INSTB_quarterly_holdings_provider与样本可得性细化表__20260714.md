# 收口前裁决包 INSTB quarterly_holdings provider 与样本可得性细化表

更新时间：2026-07-14

## 用途

- 这张细化表只负责把：
  - `INSTB` 当前最小主路线
    - `quarterly_holdings_proxy`
  - 到底该依赖哪些 provider
  - 最小真实样本应长什么样
  - 当前 friction 在哪
  固定成一页可回链的判断表。
- 当前不回答：
  - `INSTB` 正式实现
  - 新 runtime 开发
  - `Level-2` 深挖

## 当前主结论

- 当前 `INSTB` 的 canonical route 仍应固定为：
  - `季度机构持仓快照 -> quarterly_holdings_proxy`
- 当前最同构的主路线不是：
  - `龙虎榜 top_list`
  - `Level-2 / 席位逐笔`
- 当前最稳的 provider 排序是：
  - `Wind / 同花顺 F10` 作为理想主源
  - `AkShare 机构持仓接口族` 作为低成本验证入口
  - `top_list` 只作补充证据，不作等价替身

## 原始合同锚点

- `instb_p0_a_field_contract_v1.tsv` 已明确：
  - `instb_holder_change_pct`
    - 依赖 `quarterly_holdings_or_simulated_proxy`
  - `instb_concentration_change`
    - 依赖 `shareholder_count_delta`
  - `instb_fund_flow_trend`
    - 依赖 `fund_holding_delta`
  - `instb_data_lag_days`
    - 依赖 `report_date_vs_current_date`
  - `instb_signal_freshness`
    - 依赖 `freshness_classifier`
- `object_cards_p1_runtime_dependency_matrix_v1.tsv` 已明确：
  - `INSTB_P0_A`
    - 依赖 `daily_ohlcv_adjusted|institutional_holdings`
    - 默认 proxy 为 `use_daily_ohlcv_plus_quarterly_holdings_proxy`
- `data_availability_audit_contract_v1.tsv` 已明确：
  - `institutional_holdings`
    - `preferred_source = wind_or_f10`
    - `fallback_source = akshare`
    - `degrade_action = skip_instb_execution`

## provider 细化矩阵

| provider | 当前角色 | 当前能支撑的最小字段 | 当前 repo 证据 | friction | 当前判断 |
|---|---|---|---|---|---|
| `Wind 季报机构持仓` | 理想 canonical provider | `instb_total_inst_pct / prev_quarter_total / fund_holding_pct / shareholder_count / report_date` | 对象卡与数据可用性审计都把它列为主源，但仓内还没有 fresh-run 样本 | 成本高、需要账号、当前未实跑 | `理想主源，当前未验证` |
| `同花顺 F10 机构持仓` | 贴近主源的人工/半人工入口 | `fund_holding_pct / total_inst_pct / shareholder_count / report_period` | 对象卡与旧代码把 `Wind / 同花顺 F10` 并列为季度源 | 手工或半自动，规模化较弱 | `可作为一次性样本探查入口` |
| `AkShare 机构持仓接口族` | 低成本验证入口 | 可能支撑 `fund_holding_pct / shareholder_count / report_period` 的子集 | 数据可用性审计明确写入 fallback，但仓内无 fresh-run 实证 | 字段完整度、季度口径、稳定性待证实 | `当前最适合做低成本 probe` |
| `Tushare top_list / 龙虎榜` | 事件级补充证据 | 只能提供席位/事件痕迹，不能稳定给出季度持仓快照 | 仓内只停留在候选层，没有等价证明 | 覆盖离散、难拼成季度快照 | `补充线，不作主线` |
| `Level-2 / 席位逐笔` | 理想增强线 | 理论上可做更细机构行为推断 | 当前无仓内实证，且超出资料整理边界 | 成本最高、实现最重 | `future_only` |

## 最小真实样本合同

- 若只是验证 `INSTB` 是否值得保留观察位，不需要一开始就做全市场季度库。
- 当前最小真实样本建议固定为：
  - `3` 个样本标的
  - `2` 个连续季度
  - `1` 个对应的 `asof_date`
- 最小列建议至少包括：
  - `symbol`
  - `report_period`
  - `report_date`
  - `asof_date`
  - `instb_total_inst_pct`
  - `instb_prev_quarter_total`
  - `instb_fund_holding_pct`
  - `prev_quarter_fund_pct`
  - `instb_shareholder_count`
  - `instb_prev_shareholder_count`
  - `data_source`
  - `sample_note`
- 只要以上列能稳定拿到，就已足够验证：
  - `instb_holder_change_pct`
  - `instb_concentration_change`
  - `instb_fund_flow_trend`
  - `instb_data_lag_days`
  - `instb_signal_freshness`

## 字段可得性判断

| 合同字段 | 最小上游字段 | 当前最稳来源 | 当前判断 |
|---|---|---|---|
| `instb_holder_change_pct` | `instb_total_inst_pct + instb_prev_quarter_total` | `Wind / F10` 优先，`AkShare` 次选 | `NEED_SAMPLE_PROBE` |
| `instb_concentration_change` | `instb_shareholder_count + instb_prev_shareholder_count` | `Wind / F10` 优先 | `NEED_SAMPLE_PROBE` |
| `instb_fund_flow_trend` | `instb_fund_holding_pct + prev_quarter_fund_pct` | `Wind / F10` 优先，`AkShare` 待证 | `NEED_SAMPLE_PROBE` |
| `instb_data_lag_days` | `report_date + asof_date` | 任一季度快照源均可 | `LOW_RISK_DERIVABLE` |
| `instb_signal_freshness` | `report_date + asof_date` | 任一季度快照源均可 | `LOW_RISK_DERIVABLE` |

## 当前 friction

- `friction_1`
  - 当前仓内没有任何一份 `quarterly_holdings` 真实样本 CSV / TSV。
- `friction_2`
  - `AkShare` 只被写成 fallback，尚未验证字段是否足以覆盖 `fund_holding_pct + shareholder_count` 两条关键线。
- `friction_3`
  - `F10` 虽贴近需求，但天然更偏一次性样本验证，不适合作为当前默认批量 provider。
- `friction_4`
  - 即便样本拿到，`INSTB` 仍是季频滞后方法层，不应误写成执行层近实时过滤器。

## 当前裁决

- 当前可以正式写：
  - `INSTB` 的主路线已经固定为 `quarterly_holdings_proxy_first`
  - `top_list` 不是等价主源
  - `Level-2` 不是当前最小补证位
- 当前仍不能写：
  - `INSTB` 已有真实样本链
  - `AkShare` 已稳定覆盖全部季度字段
  - `INSTB` 已具备执行层触发条件

## 当前最小下一步

- 若未来继续给 `INSTB` 一步资源，最小动作应是：
  - 做一次 `3标的 x 2季度` 的 `quarterly_holdings` 样本探查
  - 优先顺序：
    - 先试 `AkShare` 低成本 probe
    - 若字段不齐，再退到 `F10` 一次性人工样本
- 在这一步完成前：
  - `INSTB` 保持 `观察位`
  - 不补低价值映射页
  - 不开新 runtime 线

## 回链

- `收口前裁决包__INSTB_provider与样本可得性审计页__20260714.md`
- `收口前裁决包__MFLOW_vs_INSTB_主负责人裁决记录页__20260714.md`
- `01_active_objects/butler_r0_object_cards_p0/instb_p0_a_field_contract_v1.tsv`
- `01_active_objects/butler_r0_object_cards_p0/object_cards_p1_runtime_dependency_matrix_v1.tsv`
- `10_source_library_archive/batch_110_external_folder_absorb__20260708/02_absorb_index/data_availability_audit_contract_v1.tsv`
- `10_source_library_archive/batch_110_external_folder_absorb__20260708/00_raw_snapshot/OBJECT_CARD_INSTB_P0_A__InstitutionalBehavior_v1.0.md`
