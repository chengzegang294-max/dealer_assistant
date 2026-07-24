import { describe, expect, it } from "vitest";

import {
  buildIndicatorContextSummary,
  createIndicatorContextTag,
  isBackgroundIndicatorSourceCard,
  isRepresentativeIndicatorSourceCard,
  orderRepresentativeSourceCards,
  pickPreferredBackgroundSourceCard,
} from "@/features/indicator/utils/contextPriority";

describe("contextPriority", () => {
  it("统一判断代表指标与背景角色", () => {
    expect(isRepresentativeIndicatorSourceCard("打板资金")).toBe(true);
    expect(isRepresentativeIndicatorSourceCard("启动点")).toBe(false);
    expect(isBackgroundIndicatorSourceCard("ZSDB指数对比")).toBe(true);
    expect(isBackgroundIndicatorSourceCard("打板资金")).toBe(false);
  });

  it("统一生成标签与短句", () => {
    const backgroundTag = createIndicatorContextTag("ZSDB指数对比");
    const semanticTag = createIndicatorContextTag("打板资金");

    expect(backgroundTag).toEqual({
      label: "背景解释",
      detail: "ZSDB指数对比",
    });
    expect(semanticTag).toEqual({
      label: "技术指标语义源",
      detail: "打板资金",
    });
    expect(buildIndicatorContextSummary("当前优先回链", backgroundTag)).toBe(
      "当前优先回链：背景解释 / ZSDB指数对比 · 语义组：行业 / 指数参照",
    );
  });

  it("统一生成代表指标顺序与背景优先级", () => {
    expect(orderRepresentativeSourceCards(["HYDB行业对比", "ZSDB指数对比", "打板资金"], "打板资金")).toEqual([
      "打板资金",
      "HYDB行业对比",
      "ZSDB指数对比",
    ]);
    expect(orderRepresentativeSourceCards(["HYDB行业对比", "ZSDB指数对比"])).toEqual([
      "HYDB行业对比",
      "ZSDB指数对比",
    ]);
    expect(pickPreferredBackgroundSourceCard(["HYDB行业对比", "ZSDB指数对比"])).toBe("ZSDB指数对比");
    expect(pickPreferredBackgroundSourceCard(["HYDB行业对比"])).toBe("HYDB行业对比");
  });
});
