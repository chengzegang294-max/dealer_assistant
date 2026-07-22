import {
  decisionActionOptions,
  horizonOptions,
  reasonTagOptions,
  type EventItem,
  type HomeWorkspaceState,
} from "@/features/home/types";
import type {
  DecisionRecordFormViewModel,
  ExplanationCardViewModel,
  MainWorkspaceViewModel,
  SelectedEventSummaryViewModel,
} from "@/features/home/adapters/homeViewModelTypes";

export function createMainWorkspaceViewModel(): MainWorkspaceViewModel {
  return {
    eyebrow: "MainWorkspacePanel",
    title: "主工作区",
    description: "这里同时承接选中事件摘要、解释卡、决策记录草稿和提交回显。",
    emptyStateTitle: "先从左侧选一条今日事件",
    emptyStateDescription: "进入条件：`selectedEventId != null`。当前空状态只保留金融限制上下文，不提前展示草稿或旧回显。",
  };
}

export function createSelectedEventSummaryViewModel(
  selectedEvent: EventItem,
  homeWorkspaceState: HomeWorkspaceState,
): SelectedEventSummaryViewModel {
  return {
    eyebrow: "SelectedEventSummaryBar",
    title: selectedEvent.summary.title,
    metaLine: `${selectedEvent.summary.subject} · ${selectedEvent.summary.occurredAt} · ${selectedEvent.summary.holdingRelation}`,
    processStatus: selectedEvent.summary.processStatus,
    disclosureFlag: selectedEvent.summary.disclosureFlag,
    workspaceState: homeWorkspaceState,
  };
}

export function createExplanationCardViewModel(selectedEvent: EventItem): ExplanationCardViewModel {
  return {
    eyebrow: "ExplanationCard",
    blocks: [
      {
        title: "触发逻辑",
        content: selectedEvent.explanation.logic,
      },
      {
        title: "事件影响",
        content: selectedEvent.explanation.impact,
      },
      {
        title: "历史类比",
        content: selectedEvent.explanation.historyAnalogy,
      },
      {
        title: "下一复查点",
        content: selectedEvent.explanation.nextReviewPoint,
      },
    ],
    openStockActionLabel: selectedEvent.stockCode ? `发出打开标的页动作：${selectedEvent.stockCode}` : null,
    stockCode: selectedEvent.stockCode ?? null,
  };
}

export function createDecisionRecordFormViewModel(eventId: string | null): DecisionRecordFormViewModel {
  return {
    eyebrow: "DecisionRecordForm",
    description: "进入编辑态后，草稿只服务当前事件；切事件时必须强制重建并清空旧回显。",
    draftEventLabel: `draft.eventId = ${eventId ?? "null"}`,
    actionField: {
      label: "动作",
      placeholder: "选择动作",
      options: decisionActionOptions,
    },
    reasonTagField: {
      label: "原因标签",
      placeholder: "选择原因标签",
      options: reasonTagOptions,
    },
    horizonField: {
      label: "观察周期",
      placeholder: "选择观察周期",
      options: horizonOptions,
    },
    noteLabel: "备注",
    notePlaceholder: "记录为什么要继续观察、加入跟踪或暂缓动作。",
    submitButtonLabel: "提交记录",
    retryButtonLabel: "清空回显继续编辑",
  };
}
