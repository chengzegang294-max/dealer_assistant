# A5 G5 Portfolio Tracking Error Validation

## 作用

- 本目录承接 `portfolio_tracking_error` 的最小执行验证工作线。
- 当前只做两类最小执行证据：
  - success generation
  - failure generation
- 当前不做：
  - 正式风险引擎实现
  - 回测
  - 参数搜索

## 目录结构

- `runtime_execution_card_v1.md`
  - 当前执行边界、入口和推荐顺序
- `artifact_index_v1.tsv`
  - 当前脚本、模板、产物索引
- `data/`
  - success / failure 最小输入模板
- `artifacts/`
  - 真实执行结果
- `generate_portfolio_tracking_error_v1.py`
  - 最小 tracking error 生成器

## 当前状态

- 当前已落：
  - 最小 success 输入模板
  - 最小 failure 输入模板
  - 最小 generator
- 当前目标是：
  - 证明 `portfolio_tracking_error` 不再只停在样例口径页
  - 形成 success / failure 两条可复现执行证据
- 当前最新增强：
  - success case 已实际消费 `covariance_matrix_latest.csv`
  - failure case 已验证协方差输入缺失会中止
- 当前仍不允许写成：
  - `output_passed`
  - `benchmark 风险输出 ready`
  - `covariance_model_id ready`

## repo 回链

- `00_entry/全库资料整理收口__20260713/A5_portfolio_tracking_error_降级风险口径可审计样例页__20260716.md`
- `00_entry/全库资料整理收口__20260713/A5_portfolio_tracking_error_actual_generation_execution页__20260718.md`
