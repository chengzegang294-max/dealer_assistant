import type {
  HomeHeroViewModel,
  HomeHeroViewModelInput,
  StockSearchBarViewModel,
} from "@/features/home/adapters/homeViewModelTypes";

export function createHomeHeroViewModel(input: HomeHeroViewModelInput): HomeHeroViewModel {
  return {
    eyebrow: "A股 P0 Batch1",
    title: "今日事件流工作台",
    description: "当前主路径固定为“事件流 - 解释卡 - 决策记录 - 回看”。本页只实现 Batch1 最小闭环，不扩到标的深挖页或问答页。",
    axisTitle: "首页唯一主轴：今日事件流",
    axisSummary: `当前事件总数 ${input.totalEvents} / 待处理 ${input.queuedEventCount}`,
    totalEvents: input.totalEvents,
    queuedEventCount: input.queuedEventCount,
    statusMetrics: [
      {
        title: "市场摘要",
        value: input.marketSummary,
        hint: "来自六卡字段总表的压缩环境结论",
      },
      {
        title: "待处理事件",
        value: `${input.queuedEventCount} 条`,
        hint: "点击右侧摘要可回流到主工作区",
      },
      {
        title: "风险提示",
        value: input.holdingRiskHint,
        hint: input.disclosureLabel,
      },
    ],
  };
}

export function createStockSearchBarViewModel(): StockSearchBarViewModel {
  return {
    entryLabel: "StockSearchEntry",
    placeholder: "输入标的代码，例如 300750",
    openActionLabel: "发出打开动作",
    disclosureButtonLabel: "查看限制说明",
  };
}
