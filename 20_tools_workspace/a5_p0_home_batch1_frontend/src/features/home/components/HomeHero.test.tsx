import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";

import { HomeHero } from "@/features/home/components/HomeHero";

describe("HomeHero", () => {
  it("renders market width metric as the first hero status card", () => {
    const markup = renderToStaticMarkup(
      <HomeHero
        eyebrow="Batch1 Home"
        title="A股 P0 工作台"
        description="围绕今日事件流展开。"
        axisTitle="当前主轴"
        axisSummary="今日事件流"
        totalEvents={6}
        queuedEventCount={2}
        statusMetrics={[
          {
            title: "市场宽度",
            value: "热度抬升，指数顺风，行业共振开始增强",
            hint: "市场宽度语义组（沪深涨跌停），只做首页轻背景说明",
          },
          {
            title: "持仓风险",
            value: "still_need_evidence",
            hint: "只做解释增强，不做交易判断",
          },
          {
            title: "事件数量",
            value: "6",
            hint: "只统计当前事件流",
          },
        ]}
      />,
    );

    expect(markup.indexOf("市场宽度")).toBeGreaterThan(-1);
    expect(markup.indexOf("市场宽度语义组（沪深涨跌停），只做首页轻背景说明")).toBeGreaterThan(-1);
    expect(markup.indexOf("市场宽度")).toBeLessThan(markup.indexOf("持仓风险"));
  });
});
