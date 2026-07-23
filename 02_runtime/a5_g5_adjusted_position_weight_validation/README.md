# A5 G5 Adjusted Position Weight Validation

## 作用

- 本目录承接 `adjusted_position_weight` 的最小执行验证工作线。
- 当前只做三类最小执行证据：
  - success generation
  - failure generation
  - formula failure generation
- 当前不做：
  - 最终组合实现
  - 回测
  - `G5` 整段通过裁决

## 目录结构

- `runtime_execution_card_v1.md`
  - 当前执行边界、入口和推荐顺序
- `artifact_index_v1.tsv`
  - 当前脚本、模板、产物索引
- `data/`
  - success / failure 最小输入模板
- `artifacts/`
  - 真实执行结果
- `generate_adjusted_position_weight_v1.py`
  - 最小最终融合生成器

## 当前状态

- 当前目标是：
  - 证明 `adjusted_position_weight` 不再只停在样例口径页
  - 形成 success / failure / formula failure 三条可复现执行证据
- 当前最新增强：
  - success case 已实际消费 `tw_actual_generation_success_latest.json`
  - success case 已实际消费 `pte_actual_generation_success_latest.json`
  - failure case 已验证上游 `target_weight` 产物缺失会中止
  - formula failure case 已验证 `final_size_scalar_below_abort_threshold` 会中止
- 当前仍不允许写成：
  - `output_passed`
  - `组合层最终权重 ready`

## repo 回链

- `00_entry/全库资料整理收口__20260713/A5_adjusted_position_weight_最终融合failure样例页__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_adjusted_position_weight_actual_generation_execution页__20260718.md`
