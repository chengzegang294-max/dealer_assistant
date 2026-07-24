export interface IndicatorContextTag {
  label: string;
  detail: string;
}

import {
  fundingActivitySourceCards,
  getIndicatorSemanticGroupLabel,
  industryIndexReferenceSourceCards,
  marketWidthSourceCards,
  semanticGroupRepresentedSourceCards,
} from "@/features/indicator/utils/semanticGroups";

export const semanticIndicatorSourceCards = [...marketWidthSourceCards, ...fundingActivitySourceCards] as const;
export const backgroundIndicatorSourceCards = [...industryIndexReferenceSourceCards] as const;
export const representativeIndicatorSourceCards = [
  ...semanticGroupRepresentedSourceCards,
] as const;

export function isRepresentativeIndicatorSourceCard(sourceCard: string) {
  return representativeIndicatorSourceCards.includes(
    sourceCard as (typeof representativeIndicatorSourceCards)[number],
  );
}

export function isBackgroundIndicatorSourceCard(sourceCard: string) {
  return backgroundIndicatorSourceCards.includes(sourceCard as (typeof backgroundIndicatorSourceCards)[number]);
}

export function getIndicatorContextRole(sourceCard: string) {
  return isBackgroundIndicatorSourceCard(sourceCard) ? "背景解释" : "技术指标语义源";
}

export function createIndicatorContextTag(sourceCard: string): IndicatorContextTag {
  return {
    label: getIndicatorContextRole(sourceCard),
    detail: sourceCard,
  };
}

export function buildIndicatorContextSummary(prefix: string, tag: IndicatorContextTag | null) {
  if (!tag) {
    return null;
  }
  const semanticGroupLabel = getIndicatorSemanticGroupLabel(tag.detail);

  return semanticGroupLabel
    ? `${prefix}：${tag.label} / ${tag.detail} · 语义组：${semanticGroupLabel}`
    : `${prefix}：${tag.label} / ${tag.detail}`;
}

export function orderRepresentativeSourceCards(availableSourceCards: string[], selectedSourceCard: string | null = null) {
  const availableRepresentativeSourceCards = Array.from(
    new Set(availableSourceCards.filter((sourceCard) => isRepresentativeIndicatorSourceCard(sourceCard))),
  );

  if (
    selectedSourceCard &&
    isRepresentativeIndicatorSourceCard(selectedSourceCard) &&
    availableRepresentativeSourceCards.includes(selectedSourceCard)
  ) {
    return [
      selectedSourceCard,
      ...representativeIndicatorSourceCards.filter(
        (sourceCard) => sourceCard !== selectedSourceCard && availableRepresentativeSourceCards.includes(sourceCard),
      ),
    ];
  }

  return representativeIndicatorSourceCards.filter((sourceCard) =>
    availableRepresentativeSourceCards.includes(sourceCard),
  );
}

export function pickPreferredBackgroundSourceCard(availableSourceCards: string[]) {
  return (
    ["ZSDB指数对比", "HYDB行业对比"] as const
  ).find((sourceCard) => availableSourceCards.includes(sourceCard)) ?? null;
}
