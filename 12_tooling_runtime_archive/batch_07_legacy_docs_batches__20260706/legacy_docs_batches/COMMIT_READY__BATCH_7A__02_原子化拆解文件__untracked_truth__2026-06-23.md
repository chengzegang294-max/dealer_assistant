# Commit Ready Batch 7A - 02_原子化拆解文件 untracked truth - 2026-06-23

## 目标

- stage the `18` untracked truth files under `02_原子化拆解文件`
- keep the batch limited to new files only
- exclude the lone modified tracked file from this pack

## 精确暂存文件

- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/A股竞价规则_R01_9点15到9点20可撤单与假单诱导_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/A股竞价规则_R02_9点20到9点25不可撤单与挂单更真实_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/A股竞价规则_R03_白点未匹配量与红绿柱观察卡_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/A股竞价规则_R04_9点25真实成交与9点25前飙升片段卡_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/A股竞价规则_R21_9点20前涨停封单可撤单片段卡_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/A股竞价规则_R22_9点20前后可信度分界_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/A股竞价规则_R23_白点多与量能活跃不等于直接涨停片段卡_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/A股竞价规则_R25_撮合量放大与抛压变化片段卡_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/kd_mtf_p0_contract_notes_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/kd_mtf_p0_field_header_v1.txt`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/kd_mtf_p0_field_sample_v1.csv`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/技术指标_波动率_RSJ市场情绪冷暖剂_后续对象定义入口_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/技术指标_量价关系_高频价量相关性因子_后续对象定义入口_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/技术指标_随机指标_多周期KD共振_P0_最小实施草案_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/技术指标_随机指标_多周期KD共振_后续对象定义入口_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/技术指标_随机指标_多周期KD共振_真实字段输出路径草案_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/趋势系统交易_四轴状态模板_后续对象定义入口_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/风险管理_VanTharp_R乘数_期望与头寸规模_后续对象定义入口_v1.md`

## 本包排除项

- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/核心技术_威科夫_弹簧Spring与上抛UT量化判定.md`
- reason:
  - tracked modified file
  - held for separate manual review

## 建议提交信息

- `docs: add Batch 7A atomic rule untracked truth pack`

## 暂存命令

- use:
  - `docs/commit_ready_stage_batch_7A__atomic_untracked_truth__2026-06-23.ps1`
  - `docs/commit_ready_batch_7A__atomic_untracked_truth__paths.txt`
