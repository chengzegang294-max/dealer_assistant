# A5 covariance_model_id 最小稳定性检查准备页

更新时间：2026-07-16

## 用途

- 在 `benchmark_relative_sample_covariance` 的 first fresh-run 已完成后，
  把下一手正式收缩到“最小稳定性检查准备”。
- 这页不做新的实跑。
- 这页只负责：
  - 说明为什么 first fresh-run 还不足以 `ready`
  - 冻结最小稳定性检查该检查什么
  - 说明当前不该提前扩到哪些方向

## 当前结论

- 当前 `covariance_model_id` 已完成：
  - `first_fresh_run_completed__not_ready`
- 当前最顺下一手不是：
  - 直接宣称唯一模型已冻结
  - 直接重开多家族并跑
  - 直接把三段输出往 `ready` 推
- 当前最顺下一手是：
  - 基于同一 `candidate_family`
  - 基于同一 `benchmark_id`
  - 基于同一 `asset_universe_id`
  - 补一轮最小稳定性检查

## 一、为什么 first fresh-run 还不够

- 当前已证明：
  - 单家族可跑
  - 单窗口可跑
  - `20 x 20` 协方差矩阵为 PSD
- 当前还没证明：
  - 相邻窗口下矩阵结构是否稳定
  - 当前候选是否已足以冻结唯一实现模型
  - 输出层能否据此解除 `not_output_passed`

## 二、最小稳定性检查范围

- 只检查：
  - `benchmark_relative_sample_covariance`
- 只比较：
  - 相邻或可比的另一个 `60 x 1d` 窗口
- 统一不改：
  - `benchmark_id = CSI300`
  - `asset_universe_id = a5_top_liquid_20`
  - `lookback_days = 60`
  - `frequency = 1d`

## 三、至少要检查什么

- 检查 1：
  - `matrix_shape` 是否仍为 `[20, 20]`
- 检查 2：
  - `diagonal_positive` 是否仍为 `true`
- 检查 3：
  - `is_psd` 是否仍为 `true`
- 检查 4：
  - `min_eigenvalue` 是否仍保持非负或近似非负
- 检查 5：
  - 总体方差规模是否未出现离谱漂移

## 四、当前暂缓

- 暂缓：
  - shrinkage 参数扫描
  - factor-implied covariance 并跑
  - 唯一模型定稿
  - ready 宣称

## 五、主负责人裁决

- 当前先做什么：
  - 先把稳定性检查范围压到最小
- 当前为什么先做这个：
  - 因为 first fresh-run 已经说明“能跑”，
    现在更值钱的是判断“是不是只跑通了一次”
- 当前不做什么：
  - 不因为一次 PSD 成功就直接升成 ready

## 六、一句话口径

- 当前这页已完成其准备职责；
  下一手已从：
  - `最小稳定性检查准备`
  推进到：
  - `最小稳定性检查执行`

## 回链

- `A5_covariance_model_id_first_fresh_run执行页__20260716.md`
- `A5_covariance_model_id_最小稳定性检查执行页__20260716.md`
- `A5_covariance_model_id_本体实跑最小准备页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
