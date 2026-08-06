# A5 六张真实案例采样记录卡 occurredAt 补证汇总页

更新时间：2026-07-27

## 一、这页用途

- 本页只做：
  - 把六张正式案例卡在 `occurredAt` 维度上的当前状态收成一页
  - 明确这一轮补证后，六张卡一致推进到了哪里

## 二、当前六张卡统一补证结果

| sample_id | sample_date | occurredAt 当前状态 | occurredAt_window | occurredAt_exact |
| --- | --- | --- | --- | --- |
| `A5_REAL_CASE_001` | `2026-07-20` | `date_level_confirmed__runtime_window_confirmed` | `2026-07-20 09:00-15:15` | `still_need_evidence` |
| `A5_REAL_CASE_002` | `2026-07-20` | `date_level_confirmed__runtime_window_confirmed` | `2026-07-20 09:00-15:15` | `still_need_evidence` |
| `A5_REAL_CASE_003` | `2026-07-20` | `date_level_confirmed__runtime_window_confirmed` | `2026-07-20 09:00-15:15` | `still_need_evidence` |
| `A5_REAL_CASE_004` | `2026-07-20` | `date_level_confirmed__runtime_window_confirmed` | `2026-07-20 09:00-15:15` | `still_need_evidence` |
| `A5_REAL_CASE_005` | `2026-07-20` | `date_level_confirmed__runtime_window_confirmed` | `2026-07-20 09:00-15:15` | `still_need_evidence` |
| `A5_REAL_CASE_006` | `2026-07-20` | `date_level_confirmed__runtime_window_confirmed` | `2026-07-20 09:00-15:15` | `still_need_evidence` |

## 三、这一轮真正解决了什么

- 这一轮真正解决了：
  1. 六张卡不再只有一句笼统的
     `occurredAt: still_need_evidence`
  2. 六张卡当前统一推进到了：
     - 日期粒度已确认
     - 运行时窗口粒度已确认
     - 精确时刻仍待证
  3. 后续再补时间时，
     不再需要重新解释日期层和窗口层

## 四、这一轮没有越过什么边界

- 当前没有越过：
  1. 没有伪写精确 `hh:mm:ss`
  2. 没有把页面运行时窗口冒充成单事件精确时刻
  3. 没有把时间补证升级成金融有效性结论

## 五、主负责人裁决

- 当前正式裁决为：
  1. 六张卡的 `occurredAt` 第一轮补证已完成
  2. 当前下一段若还继续补时间，
     只围绕：
     `单事件精确时刻`
  3. 但按当前仓内证据，
     这条线已触到新的证据边界
  4. 当前状态已经足够支撑第一轮六卡矩阵继续作为正式样本包存在

## 六、一句话口径

- 六张真实案例采样记录卡当前已经统一推进到
  `日期粒度 + 运行时窗口粒度`
  的时间证据层，
  单事件精确时刻这一层当前已触到证据边界。
