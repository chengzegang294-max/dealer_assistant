import { describe, expect, it } from "vitest";

import { createHomeHeroViewModel } from "@/features/home/adapters/homeTopSectionViewModel";
import { getIndicatorSemanticGroupHint } from "@/features/indicator/utils/semanticGroups";

describe("homeTopSectionViewModel", () => {
  it("把首页第一张状态卡收成市场宽度轻背景说明", () => {
    const heroViewModel = createHomeHeroViewModel({
      totalEvents: 6,
      queuedEventCount: 2,
      marketSummary: "热度抬升，指数顺风，行业共振开始增强",
      holdingRiskHint: "只做解释增强，不做交易判断",
      disclosureLabel: "still_need_evidence",
    });

    expect(heroViewModel.statusMetrics[0]).toEqual({
      title: "市场宽度",
      value: "热度抬升，指数顺风，行业共振开始增强",
      hint: getIndicatorSemanticGroupHint("market_width"),
    });
  });
});
