import { describe, expect, it } from "vitest";

import {
  buildStillNeedEvidenceRiskSummary,
  buildStillNeedEvidenceSummary,
  indicatorProductCopy,
} from "@/features/indicator/content/productCopy";

describe("indicator product copy", () => {
  it("provides unified explanation and restriction copy", () => {
    expect(indicatorProductCopy.mainPathSummary).toContain("事件流 -> 解释 -> 记录 -> 回看");
    expect(indicatorProductCopy.explanationOnlySummary).toContain("只做有上下文的解释增强");
    expect(indicatorProductCopy.noFreeInputSummary).toContain("不开放自由输入");
  });

  it("builds still-need-evidence summaries consistently", () => {
    expect(buildStillNeedEvidenceSummary("still_need_evidence")).toBe(
      "still_need_evidence，当前说明只做解释增强，不升格成确定性结论。",
    );
    expect(buildStillNeedEvidenceRiskSummary("still_need_evidence")).toBe(
      "still_need_evidence，当前说明只做解释增强，不升格成确定性结论。 不输出自由荐股或价格预测。",
    );
  });
});
