import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";

import { ExplanationCard } from "@/features/home/components/workspace/ExplanationCard";

describe("ExplanationCard", () => {
  it("renders summary before tags and blocks", () => {
    const markup = renderToStaticMarkup(
      <ExplanationCard
        viewModel={{
          eyebrow: "ExplanationCard",
          sourceTags: [
            {
              label: "背景解释",
              detail: "ZSDB指数对比",
            },
          ],
          sourceSummaryLine: "当前优先回链：背景解释 / ZSDB指数对比 · 语义组：行业 / 指数参照",
          blocks: [
            {
              title: "触发逻辑",
              content: "指数涨幅转强且分时承接改善。",
            },
          ],
          openStockActionLabel: "发出打开标的页动作：000001",
          stockCode: "000001",
        }}
        onOpenStockPage={vi.fn()}
      />,
    );

    expect(markup.indexOf("当前优先回链：背景解释 / ZSDB指数对比 · 语义组：行业 / 指数参照")).toBeGreaterThan(-1);
    expect(markup.indexOf("背景解释 · ZSDB指数对比")).toBeGreaterThan(-1);
    expect(markup.indexOf("触发逻辑")).toBeGreaterThan(-1);
    expect(markup.indexOf("当前优先回链：背景解释 / ZSDB指数对比 · 语义组：行业 / 指数参照")).toBeLessThan(
      markup.indexOf("背景解释 · ZSDB指数对比"),
    );
    expect(markup.indexOf("背景解释 · ZSDB指数对比")).toBeLessThan(markup.indexOf("触发逻辑"));
  });
});
