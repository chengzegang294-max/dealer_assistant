# VOTE_DECISION_TABLE_P0_E — 投票判定决策表 v1.0

> 版本：v1.0 | 状态：可执行判定表 | 与 BACKTEST_FRAMEWORK_DESIGN_v1.0.md 和 STRATEGY_BUNDLES_v1.0.md 配合使用
> 目标：将投票规则从文字描述转化为编程 AI 可直接实现的 if-then 决策树
> 核心原则：每个判定节点有明确的条件、分支、输出，无歧义

---

## 1. 判定表结构说明

### 1.1 判定节点格式

每个判定节点按以下格式编写：

```text
节点编号：NODE_XXX
判定条件：[明确的布尔条件]
TRUE 分支 → [下一节点或输出结果]
FALSE 分支 → [下一节点或输出结果]
关键阈值：[任何数值阈值]
降级路径：[条件不满足时的降级处理]
```

### 1.2 判定流程总览

```
START
  │
  ▼
NODE_001: 数据验证检查
  │
  ├─ PASS → NODE_002: PERIOD_QUEEN 交易权限检查
  │         │
  │         ├─ HALT → ABORT（禁止交易）
  │         │
  │         ├─ EXIT_ONLY → NODE_100（退出策略判定链）
  │         │
  │         └─ FULL/REDUCED → NODE_003（入场策略判定链）
  │
  └─ FAIL → ABORT（数据缺失）
```

---

## 2. 第一层：数据验证与交易权限

### NODE_001: 数据验证检查

```text
节点编号：NODE_001
判定条件：
  (1) 日 OHLCV 数据完整（无缺失且 timestamp 在 K 线收盘后）
  AND (2) 所有激活对象卡的 data_requirement 与当前数据环境匹配
  AND (3) 无任何对象卡输出 maturity_status = "FROZEN_FIELDS"（未验证）
  
TRUE 分支 → NODE_002
FALSE 分支 → ABORT（原因：数据缺失或成熟度不足）

降级路径：
  - 若日 OHLCV 缺失 → ABORT，记录 "missing_ohlcv"
  - 若某对象卡 data_requirement 不匹配 → 该对象卡 SKIP，其他继续
  - 若某对象卡 maturity_status = "FROZEN_FIELDS" → 该对象卡 SKIP，但需记录警告

实现代码：
  ```python
  def node_001_data_validation(self, objects, data_env):
      abort_reason = None
      
      # 检查日 OHLCV
      if not data_env.has_daily_ohlcv:
          return "ABORT", "missing_ohlcv"
      
      # 检查每个对象卡的数据需求
      valid_objects = []
      for obj in objects:
          if obj.data_requirement == "LEVEL2" and not data_env.has_level2:
              obj.signal_type = "NONE"  # 降级
              obj.maturity_status = "SKIP_LEVEL2_MISSING"
          elif obj.maturity_status == "FROZEN_FIELDS":
              obj.signal_type = "NONE"  # 未验证的对象卡不启用
              obj.maturity_status = "SKIP_UNVERIFIED"
          else:
              valid_objects.append(obj)
      
      return "NODE_002", valid_objects
  ```
```

### NODE_002: PERIOD_QUEEN 交易权限检查

```text
节点编号：NODE_002
判定条件：
  PERIOD_QUEEN 对象卡已计算完成
  AND pq_state_confidence >= 0.3
  
分支逻辑：
  IF pq_trading_permission == "HALT":
    → ABORT（原因：period_queen_halt）
    → 所有 EXECUTION 对象卡 signal_type 强制设为 "NONE"
    → 仅允许已有持仓的止损处理
  
  ELIF pq_trading_permission == "EXIT_ONLY":
    → NODE_100（退出策略判定链）
    → 所有 LONG 信号强制设为 "NONE"
    → 仅允许 SHORT/EXIT 信号进入投票池
  
  ELIF pq_trading_permission == "REDUCED":
    → NODE_003（入场策略判定链）
    → 所有 signal_strength 上限为 7
    → entry_min_votes = 4（TrialEntry/WaitAndSee 策略）
  
  ELIF pq_trading_permission == "FULL":
    → NODE_003（入场策略判定链）
    → entry_min_votes = 3（正常）
  
  ELSE（状态模糊）：
    → ABORT（原因：period_queen_unclear）
    → 降级到 "ATTACK_UNSUSTAINED" 处理

降级路径：
  - pq_state_confidence < 0.3 → 降级到 ATTACK_UNSUSTAINED（HALT）
  - PERIOD_QUEEN 对象卡缺失 → 默认 HALT（保守策略）

实现代码：
  ```python
  def node_002_period_queen_check(self, pq_output):
      if pq_output['pq_state_confidence'] < 0.3:
          return "ABORT", "period_queen_unclear"
      
      permission = pq_output['pq_trading_permission']
      
      if permission == "HALT":
          return "ABORT", "period_queen_halt"
      elif permission == "EXIT_ONLY":
          return "NODE_100", {"entry_min_votes": 2}
      elif permission == "REDUCED":
          return "NODE_003", {"entry_min_votes": 4, "max_strength": 7}
      elif permission == "FULL":
          return "NODE_003", {"entry_min_votes": 3}
      else:
          return "ABORT", "period_queen_unknown_permission"
  ```
```

---

## 3. 第二层：入场策略判定链（NODE_003 → NODE_099）

### NODE_003: 收集投票池

```text
节点编号：NODE_003
判定条件：收集所有激活对象卡的输出

处理逻辑：
  1. 遍历所有被 strategy_bundle 激活的对象卡
  2. 对每个对象卡执行验证：
     - signal_type ∈ {"LONG", "SHORT", "FILTER_PASS"}
     - signal_strength >= 5（执行层）或 >= 3（过滤器/风控层）
     - lock_status ∈ {"LOCKED", "UNLOCKED"}
     - signal_confidence >= 0.3
     - maturity_status ∈ {"SINGLE_FACTOR_BT", "COMBINED_BT", "OUT_OF_SAMPLE", "PROXY_QUANTIZABLE"}
  3. 通过验证的对象卡进入 vote_pool
  4. 记录每个对象卡的：object_id, signal_type, signal_strength, confidence

输出：vote_pool（有投票权的对象卡列表）
下一节点：NODE_004

降级路径：
  - 若 vote_pool 为空 → ABORT（原因：no_votes）
  - 若 vote_pool 只有 1-2 个对象 → 不立即 ABORT，继续到 NODE_004 看是否满足门槛

实现代码：
  ```python
  def node_003_collect_votes(self, activated_objects, params):
      vote_pool = []
      
      for obj in activated_objects:
          # 验证投票资格
          if obj.signal_type not in ["LONG", "SHORT", "FILTER_PASS"]:
              continue
          if obj.signal_strength < 5 and obj.function_bucket == "EXECUTION":
              continue
          if obj.lock_status in ["CONFLICT", "EXPIRED"]:
              continue
          if obj.signal_confidence < 0.3:
              continue
          if obj.maturity_status not in ["SINGLE_FACTOR_BT", "COMBINED_BT", "OUT_OF_SAMPLE", "PROXY_QUANTIZABLE"]:
              continue
          
          vote_pool.append({
              "object_id": obj.object_id,
              "signal_type": obj.signal_type,
              "signal_strength": obj.signal_strength,
              "confidence": obj.signal_confidence,
              "function_bucket": obj.function_bucket,
          })
      
      if not vote_pool:
          return "ABORT", "no_votes"
      
      return "NODE_004", vote_pool
  ```
```

### NODE_004: 过滤器否决检查

```text
节点编号：NODE_004
判定条件：检查是否有 FILTER 层对象输出 BLOCK

处理逻辑：
  1. 遍历所有 FILTER 层对象（MFLOW, VOLFAC, ATRATIO 等）
  2. 若 filter_action == "BLOCK" 且 target_object_id 匹配 vote_pool 中的对象：
     → 该对象的投票被扣除（从 "赞成" 变为 "弃权"）
  3. 若 filter_action == "BLOCK" 且 target_object_id 为 "GLOBAL" 或空：
     → 所有 vote_pool 中的对象投票被扣除（全部弃权）
  4. 若 filter_action == "ENHANCE"：
     → 该对象的 signal_strength +1（不超过 10）
  5. 若 filter_action == "DOWNGRADE"：
     → 该对象的 signal_strength -1（不低于 0）

输出：filtered_vote_pool（扣除/增强后的投票池）
下一节点：NODE_005

降级路径：
  - 若所有 vote 被 BLOCK → ABORT（原因：all_blocked）
  - 若 GLOBAL_BLOCK 触发 → ABORT（原因：global_block）

实现代码：
  ```python
  def node_004_filter_veto(self, vote_pool, filter_objects):
      filtered_votes = {v["object_id"]: v for v in vote_pool}
      
      for fobj in filter_objects:
          if fobj.filter_action == "BLOCK":
              if not fobj.target_object_id or fobj.target_object_id == "GLOBAL":
                  # 全局阻断
                  for vid in filtered_votes:
                      filtered_votes[vid]["signal_type"] = "ABSTAIN"
                      filtered_votes[vid]["block_reason"] = f"global_block_by_{fobj.object_id}"
              else:
                  # 针对特定对象
                  target = fobj.target_object_id
                  if target in filtered_votes:
                      filtered_votes[target]["signal_type"] = "ABSTAIN"
                      filtered_votes[target]["block_reason"] = f"blocked_by_{fobj.object_id}"
          
          elif fobj.filter_action == "ENHANCE":
              target = fobj.target_object_id
              if target in filtered_votes:
                  filtered_votes[target]["signal_strength"] = min(10, filtered_votes[target]["signal_strength"] + 1)
          
          elif fobj.filter_action == "DOWNGRADE":
              target = fobj.target_object_id
              if target in filtered_votes:
                  filtered_votes[target]["signal_strength"] = max(0, filtered_votes[target]["signal_strength"] - 1)
      
      # 检查是否全部弃权
      active_votes = [v for v in filtered_votes.values() if v["signal_type"] != "ABSTAIN"]
      if not active_votes:
          return "ABORT", "all_blocked"
      
      return "NODE_005", active_votes
  ```
```

### NODE_005: 计算赞成票

```text
节点编号：NODE_005
判定条件：统计 vote_pool 中的赞成票

处理逻辑：
  1. 统计 signal_type == "LONG" 或 "FILTER_PASS" 的票数
  2. 统计 signal_type == "SHORT" 的票数（A 股纯多头下不统计）
  3. 计算加权总分（多周期共振加分）：
     - 周线票 × 1.5
     - 日线票 × 1.0
     - 分钟票 × 0.8
  4. 检查同一 function_bucket 的票数限制（最多 2 票）

输出：vote_summary（赞成票、反对票、加权总分、票数限制检查）
下一节点：NODE_006

实现代码：
  ```python
  def node_005_count_votes(self, vote_pool, timeframe_weights=None):
      if timeframe_weights is None:
          timeframe_weights = {"WEEKLY": 1.5, "DAILY": 1.0, "60MIN": 0.8, "15MIN": 0.8, "5MIN": 0.8}
      
      long_votes = []
      short_votes = []
      bucket_count = {}
      
      for v in vote_pool:
          # 同一 bucket 限制最多 2 票
          bucket = v["function_bucket"]
          bucket_count[bucket] = bucket_count.get(bucket, 0) + 1
          if bucket_count[bucket] > 2:
              continue  # 超过 2 票的不计入
          
          if v["signal_type"] == "LONG" or v["signal_type"] == "FILTER_PASS":
              long_votes.append(v)
          elif v["signal_type"] == "SHORT":
              short_votes.append(v)
      
      # 计算加权总分
      long_score = sum(v["signal_strength"] * timeframe_weights.get(v.get("timeframe", "DAILY"), 1.0) for v in long_votes)
      short_score = sum(v["signal_strength"] * timeframe_weights.get(v.get("timeframe", "DAILY"), 1.0) for v in short_votes)
      
      return "NODE_006", {
          "long_count": len(long_votes),
          "short_count": len(short_votes),
          "long_score": long_score,
          "short_score": short_score,
          "long_votes": long_votes,
      }
  ```
```

### NODE_006: 投票门槛检查

```text
节点编号：NODE_006
判定条件：赞成票数量 >= entry_min_votes AND 加权总分 >= 3.0

处理逻辑：
  1. 从 PERIOD_QUEEN 或 STRATEGY_BUNDLE 获取 entry_min_votes
     - FULL 状态：entry_min_votes = 3
     - REDUCED 状态：entry_min_votes = 4
     - EXIT_ONLY 状态：entry_min_votes = 2
  2. 检查 long_count >= entry_min_votes
  3. 检查 long_score >= 3.0（加权总分最低门槛）
  4. 若 long_score >= 5.0 → 多周期共振加分，signal_strength +1

TRUE 分支（通过）→ NODE_007（风控调制）
FALSE 分支（未通过）→ ABORT（原因：votes_insufficient）

降级路径：
  - 若 long_count = 2 但 long_score >= 4.0 → 可降级为观察（不交易但记录）
  - 若 long_count >= 3 但 long_score < 3.0 → 信号质量不足，ABORT

实现代码：
  ```python
  def node_006_vote_threshold(self, vote_summary, params):
      entry_min_votes = params.get("entry_min_votes", 3)
      long_count = vote_summary["long_count"]
      long_score = vote_summary["long_score"]
      
      if long_count >= entry_min_votes and long_score >= 3.0:
          # 多周期共振加分
          if long_score >= 5.0:
              vote_summary["resonance_bonus"] = 1
          else:
              vote_summary["resonance_bonus"] = 0
          return "NODE_007", vote_summary
      else:
          return "ABORT", f"votes_insufficient: count={long_count}, score={long_score}"
  ```
```

### NODE_007: 风控调制（三层风控）

```text
节点编号：NODE_007
判定条件：所有风控层对象计算完成

处理逻辑：
  1. 第一层：Van Tharp 2% 硬性上限检查
     - 若当前持仓 + 新交易的风险 > 2% → FORCE_CLOSE → ABORT
  2. 第二层：Kelly Criterion 动态优化
     - 计算 f*（基于历史交易日志）
     - 应用半凯利/四分之一凯利/自适应模式
     - 输出 kelly_size_scalar
  3. 第三层：Volatility Targeting 环境系数
     - 计算当前波动率 vs 目标波动率
     - 输出 vt_size_scalar
  4. 最终 size_scalar = min(kelly_size_scalar, vt_size_scalar, pq_position_max_size)
  5. 若最终 size_scalar <= 0.05 → 视为禁止交易 → ABORT

输出：risk_modulated_signal（含最终 size_scalar、stop_adjustment、风险状态）
下一节点：NODE_008

降级路径：
  - Van Tharp 触发 → ABORT，原因：van_tharp_limit
  - Kelly 数据不足（<30 笔）→ 使用默认半凯利（f*=0.25）
  - VolTarget 数据缺失 → 使用默认 scalar=1.0
  - 最终 scalar 过小 → ABORT，原因：position_too_small

实现代码：
  ```python
  def node_007_risk_modulation(self, vote_summary, risk_objects, pq_output, current_positions):
      # 1. Van Tharp 检查
      for pos in current_positions:
          if pos.risk_pct > 0.02:
              return "ABORT", "van_tharp_limit"
      
      # 2. Kelly 计算
      kelly_scalar = 0.25  # 默认半凯利
      for robj in risk_objects:
          if robj.object_id == "KELLY_P0_R":
              kelly_scalar = robj.size_scalar
      
      # 3. VolTarget 计算
      vt_scalar = 1.0
      for robj in risk_objects:
          if robj.object_id == "VOLTARGET_P0_R":
              vt_scalar = robj.size_scalar
      
      # 4. 最终 scalar
      final_scalar = min(kelly_scalar, vt_scalar, pq_output["pq_position_max_size"])
      
      if final_scalar <= 0.05:
          return "ABORT", "position_too_small"
      
      vote_summary["final_size_scalar"] = final_scalar
      vote_summary["kelly_scalar"] = kelly_scalar
      vote_summary["vt_scalar"] = vt_scalar
      
      return "NODE_008", vote_summary
  ```
```

### NODE_008: 生成最终信号

```text
节点编号：NODE_008
判定条件：所有前置检查通过

处理逻辑：
  1. 确定 direction：
     - 若 long_count > short_count → "LONG"
     - 若 short_count > long_count（且允许做空）→ "SHORT"
     - 否则 → "ABORT"
  2. 确定 final_signal_strength：
     - 平均赞成票的 signal_strength
     - 加上多周期共振加分（若 long_score >= 5.0）
     - 上限为 10
  3. 确定 entry_price：
     - 取所有触发对象的 entry_price 范围（min, max）
     - 或统一使用当前收盘价
  4. 确定 stop_loss：
     - 取所有触发对象的 stop_adjustment 的加权平均
     - 加上 risk_objects 的 stop_adjustment
  5. 确定 triggered_objects：所有投赞成票的对象卡列表
  6. 确定 regime_state 和 strategy_bundle：从 PERIOD_QUEEN 获取

输出：final_trade_signal（完整交易信号）
状态：EXEC

实现代码：
  ```python
  def node_008_generate_final_signal(self, vote_summary, pq_output, strategy_bundle):
      long_votes = vote_summary["long_votes"]
      
      # 确定 direction
      direction = "LONG" if vote_summary["long_count"] > 0 else "ABORT"
      
      # 确定 strength
      avg_strength = sum(v["signal_strength"] for v in long_votes) / len(long_votes)
      final_strength = min(10, int(avg_strength + vote_summary.get("resonance_bonus", 0)))
      
      # 收集触发对象
      triggered = [v["object_id"] for v in long_votes]
      
      return "EXEC", {
          "final_signal_type": direction,
          "final_signal_strength": final_strength,
          "final_size_scalar": vote_summary["final_size_scalar"],
          "final_stop_adjustment": vote_summary.get("stop_adjustment", 0.0),
          "triggered_objects": triggered,
          "regime_state": pq_output["pq_state"],
          "strategy_bundle": strategy_bundle,
          "timestamp": datetime.now(),
      }
  ```
```

---

## 4. 退出策略判定链（NODE_100 → NODE_199）

### NODE_100: 退出策略入口

```text
节点编号：NODE_100
判定条件：pq_trading_permission == "EXIT_ONLY"

处理逻辑：
  1. 只收集 signal_type ∈ {"SHORT", "EXIT"} 的信号
  2. 允许 LONG 信号作为 "EXIT"（A 股纯多头下，LONG=买入，但 EXIT_ONLY 时只出不进）
  3. entry_min_votes = 2（降低门槛，方便退出）
  4. 检查已有持仓：
     - 若无持仓 → ABORT（无仓位可退出）
     - 若有持仓 → 继续

输出：exit_vote_pool
下一节点：NODE_101

实现代码：
  ```python
  def node_100_exit_strategy_entry(self, vote_pool, current_positions, pq_output):
      if not current_positions:
          return "ABORT", "no_positions_to_exit"
      
      exit_votes = []
      for v in vote_pool:
          if v["signal_type"] in ["SHORT", "EXIT"]:
              exit_votes.append(v)
          # 在 EXIT_ONLY 状态下，某些 LONG 信号可转化为 EXIT（如 1Sell）
          elif v["signal_type"] == "LONG" and "Sell" in v.get("object_id", ""):
              exit_votes.append(v)
      
      return "NODE_101", exit_votes
  ```
```

### NODE_101: 退出信号检查

```text
节点编号：NODE_101
判定条件：exit_votes >= 2（EXIT_ONLY 状态下的门槛）

处理逻辑：
  1. 统计 exit_votes 数量
  2. 若 >= 2 → 通过
  3. 若 < 2 但已有持仓风险 > 2% → 强制退出（Van Tharp 硬性上限）
  4. 若 < 2 且无硬性风险 → 不退出，继续持仓

TRUE 分支 → NODE_102（生成退出信号）
FALSE 分支 → HOLD（不退出，继续持有）

实现代码：
  ```python
  def node_101_exit_threshold(self, exit_votes, current_positions, params):
      entry_min_votes = params.get("entry_min_votes", 2)
      
      # 检查硬性风险
      for pos in current_positions:
          if pos.risk_pct > 0.02:
              return "NODE_102", {"forced_exit": True, "reason": "van_tharp_limit"}
      
      if len(exit_votes) >= entry_min_votes:
          return "NODE_102", {"forced_exit": False, "exit_votes": exit_votes}
      else:
          return "HOLD", "insufficient_exit_signals"
  ```
```

### NODE_102: 生成退出信号

```text
节点编号：NODE_102
判定条件：通过退出检查

输出：exit_signal
  - direction: "EXIT"（A 股纯多头下）
  - position_size: 减仓比例（由 VOLTARGET 或策略决定）
  - triggered_objects: 触发退出的对象卡
  - regime_state: 当前状态

实现代码：
  ```python
  def node_102_generate_exit_signal(self, exit_votes, pq_output, risk_objects):
      # 确定减仓比例
      exit_ratio = 0.5  # 默认减仓 50%
      for robj in risk_objects:
          if robj.object_id == "VOLTARGET_P0_R":
              exit_ratio = 1.0 - robj.size_scalar
      
      return "EXEC", {
          "final_signal_type": "EXIT",
          "exit_ratio": exit_ratio,
          "triggered_objects": [v["object_id"] for v in exit_votes],
          "regime_state": pq_output["pq_state"],
          "strategy_bundle": "GradualExit",
      }
  ```
```

---

## 5. ABORT 处理规范

### 5.1 ABORT 原因编码

```text
ABORT 原因必须记录以下字段：

abort_reason_code: str     # 标准化编码，如 "votes_insufficient"
abort_reason_desc: str     # 人类可读描述
abort_node: str            # 触发 ABORT 的节点编号（如 NODE_006）
abort_timestamp: str       # 时间戳
abort_regime_state: str    # 当时的周期状态
abort_vote_count: int      # 当时的投票数（如有）
abort_vote_score: float    # 当时的加权总分（如有）
abort_risk_status: str     # 风控状态（如触发 Van Tharp）
abort_data_status: str     # 数据状态（如缺失）

标准编码列表：
  "missing_ohlcv"          - 日 OHLCV 数据缺失
  "period_queen_halt"      - 周期女王禁止交易
  "period_queen_unclear"   - 周期状态模糊
  "no_votes"               - 无对象卡投票
  "all_blocked"            - 所有信号被过滤器阻断
  "votes_insufficient"     - 投票数不足（如 count=2, need=3）
  "van_tharp_limit"        - Van Tharp 2% 硬性上限触发
  "position_too_small"     - 仓位过小（scalar <= 0.05）
  "no_positions_to_exit"   - 无持仓可退出
  "insufficient_exit_signals" - 退出信号不足
  "global_block"           - 全局过滤器阻断
  "maturity_unverified"      - 对象卡成熟度未验证
  "level2_missing"         - Level-2 数据缺失
  "market_halt"            - 市场停牌（涨跌停等）
```

### 5.2 ABORT 后的处理流程

```text
1. 记录 ABORT 到审计日志（包含所有字段）
2. 通知风控模块（如 Van Tharp 触发，可能需要强制平仓）
3. 不生成任何交易指令
4. 继续监控下一 K 线（不阻塞 Pipeline）
5. 周期性复盘：统计各 ABORT 原因的出现频率，优化系统
```

---

## 6. 完整判定流可视化

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              START                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                              ┌──────────────┐
                              │   NODE_001   │
                              │ 数据验证检查 │
                              └──────┬───────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │ FAIL           │ PASS           │
                    ▼                │                ▼
              ┌──────────┐           │          ┌──────────────┐
              │  ABORT   │           │          │   NODE_002   │
              │ 数据缺失 │           │          │ PERIOD_QUEEN │
              └──────────┘           │          │  交易权限检查│
                                     │          └──────┬───────┘
                                     │                 │
                    ┌────────────────┼────────────────┼──────────────┐
                    │                │                │              │
                    ▼                ▼                ▼              ▼
              ┌──────────┐    ┌──────────┐   ┌──────────┐    ┌──────────┐
              │  ABORT   │    │ NODE_100 │   │ NODE_003 │    │  ABORT   │
              │  HALT    │    │ 退出策略 │   │ 入场策略 │    │ 状态模糊 │
              │          │    │ 判定链   │   │ 判定链   │    │          │
              └──────────┘    └────┬─────┘   └────┬─────┘    └──────────┘
                                   │              │
                                   ▼              ▼
                            ┌──────────┐    ┌──────────┐
                            │ NODE_101 │    │ NODE_003 │
                            │ 退出检查 │    │ 收集投票 │
                            └────┬─────┘    └────┬─────┘
                                 │               │
                    ┌────────────┼──────────┐   │
                    │ FAIL       │ PASS     │   │
                    ▼            │          ▼   │
              ┌──────────┐       │     ┌────────┴────────┐
              │  HOLD    │       │     │   NODE_004    │
              │ 继续持有 │       │     │ 过滤器否决检查│
              └──────────┘       │     └───────┬────────┘
                                 │             │
                                 │    ┌────────┼────────┐
                                 │    │ FAIL   │ PASS   │
                                 │    ▼        │        ▼
                                 │ ┌────────┐  │  ┌──────────┐
                                 │ │ ABORT  │  │  │ NODE_005 │
                                 │ │全部阻断│  │  │ 计算赞成票│
                                 │ └────────┘  │  └────┬─────┘
                                 │             │       │
                                 │             │       ▼
                                 │             │  ┌──────────┐
                                 │             │  │ NODE_006 │
                                 │             │  │ 投票门槛 │
                                 │             │  └────┬─────┘
                                 │             │       │
                                 │    ┌────────┼───────┼────────┐
                                 │    │ FAIL   │       │ PASS   │
                                 │    ▼        │       │        ▼
                                 │ ┌────────┐  │       │  ┌──────────┐
                                 │ │ ABORT  │  │       │  │ NODE_007 │
                                 │ │票数不足│  │       │  │ 风控调制 │
                                 │ └────────┘  │       │  └────┬─────┘
                                 │             │       │       │
                                 │    ┌────────┼───────┼───────┼────────┐
                                 │    │ FAIL   │       │       │ PASS   │
                                 │    ▼        │       │       │        ▼
                                 │ ┌────────┐  │       │       │  ┌──────────┐
                                 │ │ ABORT  │  │       │       │  │ NODE_008 │
                                 │ │风控触发│  │       │       │  │ 生成信号 │
                                 │ └────────┘  │       │       │  └────┬─────┘
                                 │             │       │       │       │
                                 │             │       │       │       ▼
                                 │             │       │       │  ┌──────────┐
                                 │             │       │       │  │   EXEC   │
                                 │             │       │       │  │ 执行交易 │
                                 │             │       │       │  └──────────┘
                                 │             │       │       │
                                 ▼             ▼       ▼       ▼
                            ┌──────────────────────────────────────────────┐
                            │               AUDIT LOG                      │
                            │  记录所有节点、投票、风控、ABORT 原因         │
                            └──────────────────────────────────────────────┘
```

---

## 7. 对编程 AI 的实现要求

### 7.1 判定表引擎

```python
class VoteDecisionEngine:
    """
    投票判定引擎：按照判定表执行完整的投票流程
    """
    
    def __init__(self, config):
        self.config = config
        self.audit_log = []
    
    def execute(self, objects, pq_output, risk_objects, current_positions, strategy_bundle):
        """
        执行完整的判定流程
        
        返回:
            result: "EXEC" / "ABORT" / "HOLD"
            signal: dict with trade details / abort reasons
        """
        # NODE_001: 数据验证
        result, data = self.node_001(objects)
        if result == "ABORT":
            return self._log_and_return(result, data)
        
        # NODE_002: PERIOD_QUEEN 检查
        result, data = self.node_002(pq_output, data)
        if result == "ABORT":
            return self._log_and_return(result, data)
        elif result == "NODE_100":
            return self._exit_chain(data, risk_objects, current_positions, pq_output)
        
        # NODE_003-008: 入场判定链
        return self._entry_chain(data, risk_objects, current_positions, pq_output, strategy_bundle)
    
    def _entry_chain(self, vote_pool, risk_objects, positions, pq_output, strategy_bundle):
        # NODE_003: 收集投票
        result, data = self.node_003(vote_pool)
        if result == "ABORT":
            return self._log_and_return(result, data)
        
        # NODE_004: 过滤器否决
        result, data = self.node_004(data)
        if result == "ABORT":
            return self._log_and_return(result, data)
        
        # NODE_005: 计算赞成票
        result, data = self.node_005(data)
        
        # NODE_006: 投票门槛
        result, data = self.node_006(data, pq_output)
        if result == "ABORT":
            return self._log_and_return(result, data)
        
        # NODE_007: 风控调制
        result, data = self.node_007(data, risk_objects, positions, pq_output)
        if result == "ABORT":
            return self._log_and_return(result, data)
        
        # NODE_008: 生成信号
        result, data = self.node_008(data, pq_output, strategy_bundle)
        return self._log_and_return(result, data)
    
    def _exit_chain(self, vote_pool, risk_objects, positions, pq_output):
        # NODE_100-102: 退出判定链
        result, data = self.node_100(vote_pool, positions)
        if result == "ABORT":
            return self._log_and_return(result, data)
        elif result == "HOLD":
            return self._log_and_return(result, data)
        
        result, data = self.node_101(data, positions)
        if result == "HOLD":
            return self._log_and_return(result, data)
        
        result, data = self.node_102(data, pq_output, risk_objects)
        return self._log_and_return(result, data)
    
    def _log_and_return(self, result, data):
        self.audit_log.append({
            "result": result,
            "data": data,
            "timestamp": datetime.now(),
        })
        return result, data
```

---

> 文件：VOTE_DECISION_TABLE_P0_E_v1.0.md
> 生产者：Kimi
> 状态：可执行判定表，可直接转化为代码
> 核心交付：
> - 8 个入场判定节点（NODE_001 到 NODE_008）+ 3 个退出判定节点（NODE_100-102）
> - 每个节点有明确的判定条件、TRUE/FALSE 分支、降级路径、实现代码
> - 完整的判定流可视化图
> - ABORT 原因编码规范（14 种标准编码）
> - VoteDecisionEngine 类伪代码（可直接实现）
