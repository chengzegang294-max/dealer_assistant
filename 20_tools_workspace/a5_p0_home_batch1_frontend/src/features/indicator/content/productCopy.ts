export const indicatorProductCopy = {
  mainPathSummary: "当前主路径固定为“事件流 -> 解释 -> 记录 -> 回看”。",
  explanationOnlySummary: "当前只做有上下文的解释增强，不升格成确定性结论。",
  noSpeculationSummary: "不输出自由荐股或价格预测。",
  noFreeInputSummary: "不开放自由输入。",
  stockPageRoleSummary:
    "当前是标的解释页，只回答最近发生了什么、为什么触发、之前怎么处理过、还能回哪里继续看。",
  stockQaEntrySummary: "当前已开放推荐问题下钻，结果页只回答和当前事件直接绑定的问题，不开放自由输入。",
  stockQaEntryCapabilitySummary: "先用推荐问题查看结果回答；自由输入问答留到后续批次，不在这轮打开。",
  qaPageRoleSummary: "当前是问答结果页，只做有上下文的解释增强，不做自由聊天、自由荐股或价格预测。",
  qaAnswerStructureSummary: "当前回答固定收成：问题条、来源条、核心回答区、下一步动作条、金融限制提醒条。",
};

export function buildStillNeedEvidenceSummary(label: string) {
  return `${label}，当前说明只做解释增强，不升格成确定性结论。`;
}

export function buildStillNeedEvidenceRiskSummary(label: string) {
  return `${buildStillNeedEvidenceSummary(label)} 不输出自由荐股或价格预测。`;
}
