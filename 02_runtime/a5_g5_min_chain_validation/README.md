# A5 G5 Minimal Chain Validation

## 作用

- 本目录承接 `G5` 三段输出的最小串联执行验证。
- 当前串联顺序固定为：
  - `target_weight`
  - `portfolio_tracking_error`
  - `adjusted_position_weight`
- 当前只做：
  - 一条 success 链
  - 一条 `portfolio_tracking_error` failure 链
  - 一条 `adjusted_position_weight` failure 链
  - 一份 same-batch boundary audit
- 当前不做：
  - `output_passed`
  - `G5 implementation ready`
  - 正式组合执行

## 当前状态

- 当前已具备：
  - 三段单段 runtime 入口
  - 一条最小 chain runner
- 当前目标是：
  - 证明三段不再只是各自可跑
  - 形成链级 success / `pte_failure` / `apw_failure` 执行证据
  - 把三段 frozen 边界是否已被 same-batch 运行证据覆盖，压成可复跑 audit JSON

## repo 回链

- `00_entry/全库资料整理收口__20260713/A5_G5_min_chain_execution页__20260718.md`
- `00_entry/全库资料整理收口__20260713/A5_G5主链闭合状态页__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_adjusted_position_weight解除not_output_passed正式边界_运行事实补裁页__20260723.md`
