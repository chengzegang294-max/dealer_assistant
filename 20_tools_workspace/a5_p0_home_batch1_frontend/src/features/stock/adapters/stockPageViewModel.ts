import type { DecisionRecord, EventItem } from "@/features/home/types";

export interface StockPageHeaderViewModel {
  stockName: string;
  stockCode: string;
  sourceTags: string[];
  holdingRelationLabel: string;
  latestEventStatusLabel: string;
}

export interface StockRelatedEventCardViewModel {
  eventId: string;
  title: string;
  occurredAt: string;
  category: string;
  processStatusLabel: string;
  isSelected: boolean;
}

export interface StockExplanationViewModel {
  title: string;
  subject: string;
  logic: string;
  impact: string;
  historyAnalogy: string;
  nextReviewPoint: string;
}

export interface StockRecentRecordViewModel {
  action: string;
  reasonTag: string;
  horizon: string;
  note: string;
  submittedAt: string;
  statusLabel: string;
}

export interface StockSupplementEchoViewModel {
  note: string;
  submittedAt: string;
}

export interface StockQaEntryViewModel {
  questions: string[];
  stillNeedEvidenceLabel: string;
}

export interface StockPageViewModels {
  headerViewModel: StockPageHeaderViewModel;
  relatedEventsViewModel: StockRelatedEventCardViewModel[];
  explanationViewModel: StockExplanationViewModel | null;
  recentRecordViewModel: StockRecentRecordViewModel | null;
  qaEntryViewModel: StockQaEntryViewModel;
}

interface BuildStockPageViewModelsArgs {
  stockCode: string;
  stockName: string;
  relatedEvents: EventItem[];
  selectedEvent: EventItem | null;
  latestRecord: DecisionRecord | null;
}

function formatStatus(processStatus: EventItem["summary"]["processStatus"]) {
  return processStatus === "done" ? "已处理" : "未处理";
}

export function buildStockPageViewModels(args: BuildStockPageViewModelsArgs): StockPageViewModels {
  const { stockCode, stockName, relatedEvents, selectedEvent, latestRecord } = args;
  const fallbackHoldingRelation = relatedEvents[0]?.summary.holdingRelation ?? "关注相关";
  const latestStatus = selectedEvent?.summary.processStatus ?? relatedEvents[0]?.summary.processStatus ?? "pending";

  return {
    headerViewModel: {
      stockName,
      stockCode,
      sourceTags: Array.from(new Set(relatedEvents.map((event) => event.sourceCard))).slice(0, 3),
      holdingRelationLabel: fallbackHoldingRelation,
      latestEventStatusLabel: formatStatus(latestStatus),
    },
    relatedEventsViewModel: relatedEvents.map((event) => ({
      eventId: event.summary.eventId,
      title: event.summary.title,
      occurredAt: event.summary.occurredAt,
      category: event.sourceCard,
      processStatusLabel: formatStatus(event.summary.processStatus),
      isSelected: selectedEvent?.summary.eventId === event.summary.eventId,
    })),
    explanationViewModel: selectedEvent
      ? {
          title: selectedEvent.explanation.title,
          subject: selectedEvent.explanation.subject,
          logic: selectedEvent.explanation.logic,
          impact: selectedEvent.explanation.impact,
          historyAnalogy: selectedEvent.explanation.historyAnalogy,
          nextReviewPoint: selectedEvent.explanation.nextReviewPoint,
        }
      : null,
    recentRecordViewModel: latestRecord
      ? {
          action: latestRecord.action,
          reasonTag: latestRecord.reasonTag,
          horizon: latestRecord.horizon,
          note: latestRecord.note,
          submittedAt: latestRecord.submittedAt,
          statusLabel: "已记录",
        }
      : null,
    qaEntryViewModel: {
      questions: [
        "这次事件为什么触发？",
        "这个理由标签是什么意思？",
        "历史类比在说什么？",
        "我上次为什么这样记录？",
      ],
      stillNeedEvidenceLabel: "still_need_evidence",
    },
  };
}
