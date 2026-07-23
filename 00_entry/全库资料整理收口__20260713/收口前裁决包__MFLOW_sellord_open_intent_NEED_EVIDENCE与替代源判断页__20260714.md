# 收口前裁决包 MFLOW sellord_open_intent NEED_EVIDENCE 与替代源判断页

更新时间：2026-07-14

## 用途

- 这份判断页只负责回答：
  - `MFLOW` 当前两项最强特征缺口
    - `mflow_sellord_ratio`
    - `mflow_open_intent`
  - 到底属于：
    - 当前可接入替代源
    - 还是只能保留为 `NEED_EVIDENCE`
- 当前不回答：
  - 新 provider 采购
  - runtime 新开发
  - 指标正式实现

## 当前问题定义

- `mflow_sellord_ratio`
  - 原始定义来自：
    - `mfd_sellord / (mfd_sellord + mfd_buyord)`
  - 本质上依赖：
    - 主力卖出单数
    - 主力买入单数
- `mflow_open_intent`
  - 原始定义来自：
    - `mfd_volinflowrate_open_m`
  - 本质上依赖：
    - 集合竞价 / 开盘阶段主力净流入率

## 原始对象卡锚点

- 原始对象卡明确写了：
  - `mflow_sellord`
    - 主力流出单数（大单+超大单卖出笔数）
  - `mflow_buyord`
    - 主力流入单数
  - `mflow_volinflowrate_open`
    - 开盘主力净流入率（集合竞价阶段）
- 对应派生口径也明确写了：
  - `mflow_sellord_ratio = mflow_sellord / 总成交单数`
  - `mflow_open_intent = classify(mfd_volinflowrate_open_m)`
- 这些定义见：
  - `10_source_library_archive/batch_110_external_folder_absorb__20260708/00_raw_snapshot/OBJECT_CARD_MFLOW_P0_A__MoneyFlow_v1.0.md`

## 当前仓内真实可用源

- 当前 `MFLOW` 真正打通的真实源是：
  - `Tushare moneyflow + daily`
- 它当前稳定支撑的字段只有：
  - `main_fund_net_inflow`
  - `main_fund_net_inflow_ratio`
  - 以及配套 `daily OHLCV`
- 当前仓内没有发现：
  - `mfd_sellord`
  - `mfd_buyord`
  - `mfd_volinflowrate_open_m`
  的真实抓取链、批量 CSV 或可复现 runner

## 历史线索与证据强度

### 一、原始定义层

- `DATA_AVAILABILITY_AUDIT_v1.0.md` 明确把以下字段列为 `MFLOW` 核心输入：
  - `mfd_sellord`
  - `mfd_buyord`
  - `mfd_volinflowrate_open_m`
  - `mfd_netinflow`
- 但同页当前状态写的是：
  - `UNKNOWN（待确认）`
- 这说明：
  - 它们是“设计上想要的数据”
  - 不是“当前仓内已打通的数据”

### 二、proof-of-mapping 线

- 仓内存在 `SBKT_F014` 的证明链：
  - `02_runtime/s_bucket_f014_proof_of_mapping_v1/`
- 它证明的是：
  - `mfd_sellord_raw + mfd_volinflowrate_open_m_raw`
  如何映射到 `F014` 的字段级入口合同
- 但该 proof 明确写了：
  - `mapping_only`
  - `不写回主 runtime CSV`
  - `不宣称已真实接入`
- 且输入样本只有：
  - `3` 行手工样例
- 因而它的证据强度只能算：
  - `mapping_proof_only`
  - 不能当作当前 `MFLOW` 的真实替代源

### 三、当前 T02 真实链

- 当前 `T02` 真实链已经足够支撑：
  - `mflow_net_inflow`
  - `mflow_inflow_ratio`
  - `mflow_divergence_score(v0)`
- 但当前没有任何证据表明：
  - `Tushare moneyflow` 可低成本恢复：
    - `mflow_sellord_ratio`
    - `mflow_open_intent`

## 替代源判断

| 字段 | 当前最接近来源 | 能否作为当前仓内真实替代源 | 判断 | 原因 |
|---|---|---|---|---|
| `mflow_sellord_ratio` | `SBKT_F014 proof-of-mapping` 的 `mfd_sellord_raw` 样例 | `否` | `NEED_EVIDENCE 保留` | 只有 mapping proof，无真实日频抓取链，无批量样本，无 canonical provider |
| `mflow_open_intent` | `SBKT_F014 proof-of-mapping` 的 `mfd_volinflowrate_open_m_raw` 样例 | `否` | `NEED_EVIDENCE 保留` | 只有 mapping proof，无真实集合竞价/开盘阶段资金字段来源 |
| `mflow_net_inflow` | `Tushare moneyflow` | `是` | `可直接使用` | 当前真实链已打通 |
| `mflow_inflow_ratio` | `main_fund_net_inflow_ratio` | `是` | `可 direct/proxy 站住` | 当前 metadata 已固定计算口径 |

## 当前可接受降级

- 对 `mflow_sellord_ratio`：
  - 当前只能接受：
    - `missing_with_degrade`
    - 或 `default/use_0_5_if_total_orders_missing`
  - 当前不能接受：
    - 把 `SBKT_F014` 的 `3` 行 proof 样例写成真实 provider
- 对 `mflow_open_intent`：
  - 当前只能接受：
    - `missing_with_default`
    - 或 `default_NEUTRAL`
  - 当前不能接受：
    - 把历史对象卡里的阈值分类器写成“当前已具备真实开盘主力净流入率”

## 当前不成立的说法

- 当前不能写：
  - `MFLOW` 已完成完整字段闭环
  - `Tushare moneyflow` 已等价恢复 `mfd_sellord + mfd_volinflowrate_open_m`
  - `SBKT_F014 proof-of-mapping` 已经证明这两个字段当前仓内可真实接入

## 当前成立的说法

- 当前可以写：
  - `MFLOW` 已形成第一轮 proxy 审计闭环
  - 其中：
    - `mflow_net_inflow`
    - `mflow_inflow_ratio`
    - `mflow_divergence_score(v0)`
    已有真实链或派生审计支撑
  - 但：
    - `mflow_sellord_ratio`
    - `mflow_open_intent`
    目前仍停留在历史定义层与 mapping proof 层，必须保留为 `NEED_EVIDENCE`

## 主负责人裁决

- 当前裁决：
  - `mflow_sellord_ratio`
    - 保留为 `NEED_EVIDENCE`
    - 不再把它当作当前阶段必须强行补齐的硬阻塞
  - `mflow_open_intent`
    - 保留为 `NEED_EVIDENCE`
    - 当前允许使用 `default_NEUTRAL` 边界，不冒充真实开盘流入分类
- 裁决原因：
  - 当前仓内没有这两个字段的真实抓取链
  - 现有 `SBKT_F014` 只证明“历史字段映射存在”，不证明“当前真实源可得”
  - 若继续硬追，会把主线从“收口前裁决”滑向“新数据线重开”

## 当前最小下一步

- 1. 在 `MFLOW` provider 审计页与字段映射页明确写死：
  - 这两个字段当前是：
    - `historical_contract_defined__current_real_source_missing`
- 2. 在主负责人裁决页明确写死：
  - 它们属于 `NEED_EVIDENCE`
  - 不是本轮阻塞 `MFLOW` 先审的硬前提
- 3. 若未来真要重开这两个字段：
  - 单独作为“高质量 provider 恢复线”处理
  - 不混入当前 `proxy` 审计闭环

## 回链

- `收口前裁决包__MFLOW_provider与样本可得性审计页__20260714.md`
- `收口前裁决包__MFLOW_字段映射审计页__20260714.md`
- `收口前裁决包__MFLOW_vs_INSTB_主负责人裁决记录页__20260714.md`
- `10_source_library_archive/batch_110_external_folder_absorb__20260708/00_raw_snapshot/OBJECT_CARD_MFLOW_P0_A__MoneyFlow_v1.0.md`
- `10_source_library_archive/batch_110_external_folder_absorb__20260708/00_raw_snapshot/DATA_AVAILABILITY_AUDIT_v1.0.md`
- `02_runtime/s_bucket_f014_proof_of_mapping_v1/README.md`
- `02_runtime/s_bucket_f014_proof_of_mapping_v1/real_input_samples/f014_proof_input_sample_v1.csv`
- `02_runtime/s_bucket_f014_proof_of_mapping_v1/s_bucket_f014_proof_of_mapping_v1.py`
