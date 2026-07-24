export type IndicatorSemanticGroupKey = "market_width" | "funding_activity" | "industry_index_reference";

export interface IndicatorSemanticGroupDefinition {
  key: IndicatorSemanticGroupKey;
  label: string;
  sourceCards: string[];
  allowedPages: Array<"home" | "stock" | "qa">;
  primaryRole: string;
}

export const marketWidthSourceCards = ["沪深涨跌停"] as const;
export const fundingActivitySourceCards = ["打板资金", "上榜资金"] as const;
export const industryIndexReferenceSourceCards = ["HYDB行业对比", "ZSDB指数对比"] as const;

export const indicatorSemanticGroupDefinitions: IndicatorSemanticGroupDefinition[] = [
  {
    key: "market_width",
    label: "市场宽度",
    sourceCards: [...marketWidthSourceCards],
    allowedPages: ["home", "stock", "qa"],
    primaryRole: "首页最轻背景说明候选",
  },
  {
    key: "funding_activity",
    label: "资金活跃",
    sourceCards: [...fundingActivitySourceCards],
    allowedPages: ["stock", "qa"],
    primaryRole: "事件说明与资金解释",
  },
  {
    key: "industry_index_reference",
    label: "行业 / 指数参照",
    sourceCards: [...industryIndexReferenceSourceCards],
    allowedPages: ["stock", "qa"],
    primaryRole: "标的解释骨架与背景参照",
  },
];

export const semanticGroupRepresentedSourceCards = indicatorSemanticGroupDefinitions.flatMap((group) => group.sourceCards);

const indicatorSemanticRoleSummaryByKey: Record<IndicatorSemanticGroupKey, string> = {
  industry_index_reference: "当前解释骨架：行业 / 指数参照",
  funding_activity: "当前事件说明补强：资金活跃",
  market_width: "当前轻背景说明：市场宽度",
};

const indicatorSemanticGroupHintByKey: Record<IndicatorSemanticGroupKey, string> = {
  market_width: "市场宽度语义组（沪深涨跌停），只做首页轻背景说明",
  funding_activity: "资金活跃语义组（打板资金 / 上榜资金），只做事件说明补强",
  industry_index_reference: "行业 / 指数参照语义组（HYDB行业对比 / ZSDB指数对比），只做解释骨架与背景参照",
};

const indicatorSemanticRoleOrder: IndicatorSemanticGroupKey[] = [
  "industry_index_reference",
  "funding_activity",
  "market_width",
];

export function getIndicatorSemanticGroupByKey(groupKey: IndicatorSemanticGroupKey) {
  return indicatorSemanticGroupDefinitions.find((group) => group.key === groupKey) ?? null;
}

export function getIndicatorSemanticGroupBySourceCard(sourceCard: string) {
  return indicatorSemanticGroupDefinitions.find((group) => group.sourceCards.includes(sourceCard)) ?? null;
}

export function getIndicatorSemanticGroupLabel(sourceCard: string) {
  return getIndicatorSemanticGroupBySourceCard(sourceCard)?.label ?? null;
}

export function getIndicatorSemanticGroupKey(sourceCard: string) {
  return getIndicatorSemanticGroupBySourceCard(sourceCard)?.key ?? null;
}

export function getIndicatorSemanticGroupsForPage(page: "home" | "stock" | "qa") {
  return indicatorSemanticGroupDefinitions.filter((group) => group.allowedPages.includes(page));
}

export function getIndicatorSemanticRoleSummary(sourceCard: string) {
  const groupKey = getIndicatorSemanticGroupKey(sourceCard);
  return groupKey ? indicatorSemanticRoleSummaryByKey[groupKey] : null;
}

export function buildIndicatorSemanticRoleSummaries(sourceCards: string[]) {
  const detectedKeys = new Set<IndicatorSemanticGroupKey>();

  sourceCards.forEach((sourceCard) => {
    const groupKey = getIndicatorSemanticGroupKey(sourceCard);
    if (groupKey) {
      detectedKeys.add(groupKey);
    }
  });

  return indicatorSemanticRoleOrder
    .filter((groupKey) => detectedKeys.has(groupKey))
    .map((groupKey) => indicatorSemanticRoleSummaryByKey[groupKey]);
}

export function getIndicatorSemanticGroupHint(groupKey: IndicatorSemanticGroupKey) {
  return indicatorSemanticGroupHintByKey[groupKey];
}
