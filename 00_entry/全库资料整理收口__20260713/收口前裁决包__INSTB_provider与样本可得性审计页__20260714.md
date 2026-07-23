# 收口前裁决包 INSTB provider 与样本可得性审计页

更新时间：2026-07-14

## 用途

- 这份审计页只回答一件事：
  - `INSTB` 当前是否已经具备“值得进入第二批观察裁决”的最小 provider 与样本可得性基础。
- 当前不回答：
  - 正式实现
  - 默认执行链接线
  - 是否立即开新批次

## 当前对象定位

- 对象：
  - `INSTB`
- 当前深度：
  - `sample_contract_ready`
- 当前角色：
  - 方法层 / 机构行为观察对象
- 当前不做：
  - 不把 `INSTB` 写成首批补采
  - 不把 `龙虎榜/Level-2` 直接当作当前必须补齐的硬前提
  - 不把 `top_list` 冒写成 `quarterly_holdings` 等价主源

## 当前合同锚点

- 当前字段合同入口：
  - `01_active_objects/butler_r0_object_cards_p0/instb_p0_a_field_contract_v1.tsv`
- 当前 acceptance 入口：
  - `01_active_objects/butler_r0_object_cards_p0/object_cards_p0_acceptance_matrix_v1.tsv`
- 当前 runtime 依赖入口：
  - `01_active_objects/butler_r0_object_cards_p0/object_cards_p1_runtime_dependency_matrix_v1.tsv`
- 当前最小输入样本形状：
  - `daily_ohlcv_plus_quarterly_holdings_snapshot`
- 当前默认 runtime proxy：
  - `use_daily_ohlcv_plus_quarterly_holdings_proxy`

## 当前最小字段合同

- 当前合同核心字段包括：
  - `instb_holder_change_pct`
  - `instb_concentration_change`
  - `instb_fund_flow_trend`
  - `instb_data_lag_days`
  - `instb_signal_freshness`
  - `instb_composite_score`
  - `instb_signal_type`
  - `instb_signal_strength`
  - `instb_method_layer_use`
  - `instb_data_mode`
- 当前字段语义说明：
  - 这套合同更像“季频机构持仓行为解释层”
  - 不是“盘口级席位/龙虎榜即时执行信号”

## provider 候选矩阵

| provider | 当前角色 | 当前证据 | 优点 | 风险 | 当前判断 |
|---|---|---|---|---|---|
| `季度机构持仓数据` | 当前最贴合对象合同的主路线 | acceptance / runtime 依赖矩阵已明确写成 `quarterly_holdings_snapshot` | 与当前字段合同最同构，适合方法层解释 | 季频、滞后强，不适合作为执行层主触发 | `首选审计入口` |
| `龙虎榜 top_list` | 可作为机构行为补充证据 | provider guide 提到 Tushare 可拿到基础 `top_list` | 免费或低门槛，能提供事件级席位痕迹 | 事件驱动、覆盖不连续，难直接变成季度持仓代理 | `补充入口，不作主入口` |
| `Level-2 / 席位逐笔` | 理想高颗粒路线 | provider guide 明确归为付费升级层 | 颗粒最细，若做席位/机构行为会更强 | 付费重、当前仓内无实证、超出当前第二批观察边界 | `理想参考，不作当前第一刀` |
| `AkShare / F10 机构持仓` | 免费或半免费替代 | 数据可用性文档列为候选，但仓内还无 fresh-run 实证 | 成本低，可能支持快速样本验证 | 字段完整度与季度口径稳定性待确认 | `备用审计入口` |

## 当前已知证据

- 当前仓内已经有：
  - `INSTB` 字段合同
  - acceptance 样本合同
  - runtime 依赖矩阵
- 当前仓内还没有：
  - `quarterly_holdings` 真实抓取脚手架
  - `龙虎榜/Level-2` fresh-run 产物
  - `quarterly_holdings` 真实样本 CSV / TSV
- 当前仓内现在已经补出：
  - `INSTB quarterly_holdings provider / 样本可得性细化表`
    - 已把 canonical route、最小样本合同与 provider friction 固定成单页
- 当前最重要的已知结论：
  - `INSTB` 并不是“完全没定义”的空壳
  - 但它也还没像 `MFLOW` 那样形成真实样本链和可复现审计 runner

## 当前缺口

- `NEED_EVIDENCE: canonical provider`
  - 当前还没拍板：
    - `AkShare` 是否足以承担一次性低成本 probe
    - `F10` 是否需要作为 probe 兜底入口
- `NEED_EVIDENCE: 样本可得性`
  - 当前仓内还没有一份 `INSTB` 的真实样本 CSV / TSV
- `NEED_EVIDENCE: 字段完整度`
  - 当前还没验证免费源是否能稳定支持：
    - `holder_change_pct`
    - `shareholder_count_delta`
    - `fund_holding_delta`
    - `signal_freshness`
- `NEED_EVIDENCE: 方法层边界`
  - 当前需要明确：
    - `INSTB` 是长期保持在方法层
    - 还是未来可能进入执行过滤层

## 风险与降级

- 当前最大风险不是“没有故事可讲”。
- 当前最大风险是：
  - 把 `龙虎榜/Level-2` 这种高成本路线误写成当前必须条件
  - 进而把 `INSTB` 误判成“只能长期冻结”
- 当前可接受降级口径：
  - 允许先把 `INSTB` 视为：
    - `quarterly_holdings_proxy_first`
  - 即：
    - 先用季度机构持仓解释层做方法层验证
    - 不追求盘口级、席位级实时行为
- 当前不可接受口径：
  - 不应把 `INSTB` 冒写成“已具备执行层数据”
  - 不应把 `top_list` 直接当作 `quarterly_holdings` 等价替身

## 主负责人裁决

- 当前裁决：
  - `INSTB` 值得保留在第二批观察
  - 但当前不应压过 `MFLOW`
  - `quarterly_holdings_proxy_first` 已固定为当前最稳主路线
- 裁决原因：
  - `INSTB` 的合同壳已经存在，说明不是无意义对象
  - 但它当前只有合同层证据，没有像 `MFLOW` 那样的真实样本闭环
  - 就“最小可审计闭环”而言，`MFLOW` 明显走得更前

## 当前最小下一步

- 1. 若目标是尽快进入多家 AI 讨论：
  - 当前这页已经足够作为 `INSTB` 的 first-hop 底稿
- 2. 若目标是把 `INSTB` 再向前推一格：
  - 当前这一步已补成正式细化表：
    - `收口前裁决包__INSTB_quarterly_holdings_provider与样本可得性细化表__20260714.md`
  - 再下一刀才是：
    - 一次 `3标的 x 2季度` 的真实样本探查
- 3. 当前不建议优先补：
  - `Level-2`
  - `席位逐笔`
  - `高成本龙虎榜深挖`

## 回链

- `待补采参考交易系统候选清单__20260713.md`
- `参考交易系统补采优先级表__20260713.md`
- `收口前裁决包__MFLOW_vs_INSTB_多AI讨论前情提要与裁决框架__20260714.md`
- `收口前裁决包__INSTB_quarterly_holdings_provider与样本可得性细化表__20260714.md`
- `01_active_objects/butler_r0_object_cards_p0/instb_p0_a_field_contract_v1.tsv`
- `01_active_objects/butler_r0_object_cards_p0/object_cards_p0_acceptance_matrix_v1.tsv`
- `01_active_objects/butler_r0_object_cards_p0/object_cards_p1_runtime_dependency_matrix_v1.tsv`
- `10_source_library_archive/batch_110_external_folder_absorb__20260708/00_raw_snapshot/DATA_AVAILABILITY_AUDIT_v1.0.md`
- `10_source_library_archive/batch_110_external_folder_absorb__20260708/00_raw_snapshot/DATA_PROVIDER_GUIDE_v1.0.md`
