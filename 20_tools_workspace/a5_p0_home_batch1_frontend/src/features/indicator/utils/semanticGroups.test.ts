import { describe, expect, it } from "vitest";

import {
  buildIndicatorSemanticRoleSummaries,
  getIndicatorSemanticGroupByKey,
  getIndicatorSemanticGroupBySourceCard,
  getIndicatorSemanticGroupHint,
  getIndicatorSemanticGroupKey,
  getIndicatorSemanticGroupLabel,
  getIndicatorSemanticRoleSummary,
  getIndicatorSemanticGroupsForPage,
  semanticGroupRepresentedSourceCards,
} from "@/features/indicator/utils/semanticGroups";

describe("semanticGroups", () => {
  it("统一提供 sourceCard 到语义组的映射", () => {
    expect(getIndicatorSemanticGroupKey("沪深涨跌停")).toBe("market_width");
    expect(getIndicatorSemanticGroupLabel("打板资金")).toBe("资金活跃");
    expect(getIndicatorSemanticGroupLabel("HYDB行业对比")).toBe("行业 / 指数参照");
    expect(getIndicatorSemanticGroupBySourceCard("启动点")).toBeNull();
  });

  it("统一提供语义组定义与页面边界", () => {
    expect(getIndicatorSemanticGroupByKey("market_width")).toEqual({
      key: "market_width",
      label: "市场宽度",
      sourceCards: ["沪深涨跌停"],
      allowedPages: ["home", "stock", "qa"],
      primaryRole: "首页最轻背景说明候选",
    });

    expect(getIndicatorSemanticGroupsForPage("home").map((group) => group.label)).toEqual(["市场宽度"]);
    expect(getIndicatorSemanticGroupsForPage("stock").map((group) => group.label)).toEqual([
      "市场宽度",
      "资金活跃",
      "行业 / 指数参照",
    ]);
    expect(semanticGroupRepresentedSourceCards).toEqual([
      "沪深涨跌停",
      "打板资金",
      "上榜资金",
      "HYDB行业对比",
      "ZSDB指数对比",
    ]);
  });

  it("统一提供语义组角色短句与固定顺序", () => {
    expect(getIndicatorSemanticRoleSummary("沪深涨跌停")).toBe("当前轻背景说明：市场宽度");
    expect(getIndicatorSemanticRoleSummary("上榜资金")).toBe("当前事件说明补强：资金活跃");
    expect(getIndicatorSemanticRoleSummary("HYDB行业对比")).toBe("当前解释骨架：行业 / 指数参照");
    expect(getIndicatorSemanticGroupHint("market_width")).toBe("市场宽度语义组（沪深涨跌停），只做首页轻背景说明");
    expect(buildIndicatorSemanticRoleSummaries(["上榜资金", "ZSDB指数对比"])).toEqual([
      "当前解释骨架：行业 / 指数参照",
      "当前事件说明补强：资金活跃",
    ]);
  });
});
