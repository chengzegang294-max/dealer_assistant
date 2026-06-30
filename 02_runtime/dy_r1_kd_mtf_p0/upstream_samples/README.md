# Upstream Samples

## 当前状态

- 本目录预留给 `DY-R1 / KD_MTF_P0` 的上游 canonical bars 样本。
- 第一份完整 `n01_first_real_input_bars_v1.csv` 大样本已正式导入本目录。
- 当前文件规模：
  - `8977` 行

## 为什么当前还能运行

- 当前 `append stub` 只读取本目录里的 `proof_output_v1.csv`。
- 因此本运行时层已经可以独立做 `dry-run / --persist`。
- 若要在新目录里继续做 `H1 -> 4h/day/week -> proof_input/proof_output` 重建，当前所需的大样本已经就位。

## 下一步

- 把对象层与文档层中的相关路径统一改成本目录本地样本路径。
- 后续直接在新目录里继续 proof 重建与 `b` 补样。
